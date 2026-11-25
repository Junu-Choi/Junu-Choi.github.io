import { spawn, spawnSync } from "node:child_process";
import { existsSync, createReadStream, statSync, writeFileSync, chmodSync } from "node:fs";
import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, "..");
const distDir = path.join(rootDir, "dist");
const outPdf = path.join(distDir, "Junu_Choi_CV.pdf");
const publicPdf = path.join(rootDir, "public", "Junu_Choi_CV.pdf");

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".webp": "image/webp",
  ".jpeg": "image/jpeg",
  ".jpg": "image/jpeg",
  ".ico": "image/x-icon",
  ".woff2": "font/woff2",
};

function findChrome() {
  if (process.env.CHROME_BIN && existsSync(process.env.CHROME_BIN)) {
    return process.env.CHROME_BIN;
  }
  for (const cmd of ["google-chrome-stable", "google-chrome", "chromium-browser", "chromium"]) {
    const res = spawnSync("which", [cmd], { encoding: "utf8" });
    if (res.status === 0 && res.stdout.trim()) return res.stdout.trim();
  }
  const home = process.env.HOME || "";
  if (home) {
    const pwDir = path.join(home, ".cache", "ms-playwright");
    const res = spawnSync("find", [pwDir, "-maxdepth", "3", "-name", "chrome", "-type", "f"], {
      encoding: "utf8",
    });
    const first = (res.stdout || "").split("\n").map((s) => s.trim()).find(Boolean);
    if (first && existsSync(first)) return first;
  }
  return null;
}

function renderPdfViaCDP(chromeBin, cvUrl) {
  return new Promise((resolve, reject) => {
    const child = spawn(
      chromeBin,
      [
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--remote-debugging-pipe",
      ],
      { stdio: ["ignore", "ignore", "pipe", "pipe", "pipe"] }
    );

    const pipeOut = child.stdio[3];
    const pipeIn = child.stdio[4];
    let nextId = 1;
    const pending = new Map();
    const listeners = new Map();
    let buf = "";

    const timer = setTimeout(() => {
      child.kill("SIGKILL");
      reject(new Error("Timed out waiting for Chrome PDF generation"));
    }, 20000);

    function cleanup() {
      clearTimeout(timer);
      try {
        child.kill("SIGTERM");
      } catch {}
    }

    pipeIn.setEncoding("utf8");
    pipeIn.on("data", (chunk) => {
      buf += chunk;
      let idx;
      while ((idx = buf.indexOf("\0")) !== -1) {
        const raw = buf.slice(0, idx);
        buf = buf.slice(idx + 1);
        if (!raw) continue;
        const msg = JSON.parse(raw);
        if (msg.id && pending.has(msg.id)) {
          const { res, rej } = pending.get(msg.id);
          pending.delete(msg.id);
          if (msg.error) rej(new Error(msg.error.message || JSON.stringify(msg.error)));
          else res(msg.result);
        } else if (msg.method && listeners.has(msg.method)) {
          const fn = listeners.get(msg.method);
          listeners.delete(msg.method);
          fn(msg);
        }
      }
    });

    child.on("error", (err) => {
      cleanup();
      reject(err);
    });

    function send(method, params = {}, sessionId = undefined) {
      const id = nextId++;
      const payload = sessionId ? { id, method, params, sessionId } : { id, method, params };
      return new Promise((res, rej) => {
        pending.set(id, { res, rej });
        pipeOut.write(JSON.stringify(payload) + "\0");
      });
    }

    function waitForEvent(method) {
      return new Promise((res) => {
        listeners.set(method, res);
      });
    }

    (async () => {
      try {
        const { targetId } = await send("Target.createTarget", { url: "about:blank" });
        const { sessionId } = await send("Target.attachToTarget", { targetId, flatten: true });
        await send("Page.enable", {}, sessionId);
        await send("Emulation.setEmulatedMedia", { media: "print" }, sessionId);

        const loaded = waitForEvent("Page.loadEventFired");
        await send("Page.navigate", { url: cvUrl }, sessionId);
        await loaded;

        await send(
          "Runtime.evaluate",
          {
            expression:
              "document.fonts.ready.then(() => new Promise((r) => setTimeout(r, 150)))",
            awaitPromise: true,
          },
          sessionId
        );

        const { data } = await send(
          "Page.printToPDF",
          {
            printBackground: true,
            preferCSSPageSize: true,
            displayHeaderFooter: false,
          },
          sessionId
        );

        cleanup();
        resolve(Buffer.from(data, "base64"));
      } catch (err) {
        cleanup();
        reject(err);
      }
    })();
  });
}

const chromeBin = findChrome();
if (!chromeBin) {
  console.warn("[build-cv-pdf] No Chrome/Chromium binary found; keeping existing Junu_Choi_CV.pdf.");
  process.exit(0);
}

const server = http.createServer((req, res) => {
  const urlPath = decodeURIComponent((req.url || "/").split("?")[0]);
  let filePath = path.join(distDir, urlPath);
  if (existsSync(filePath) && statSync(filePath).isDirectory()) {
    filePath = path.join(filePath, "index.html");
  }
  if (!existsSync(filePath)) {
    res.writeHead(404);
    res.end("Not found");
    return;
  }
  const ext = path.extname(filePath).toLowerCase();
  res.writeHead(200, { "Content-Type": MIME[ext] || "application/octet-stream" });
  createReadStream(filePath).pipe(res);
});

server.listen(0, "127.0.0.1", async () => {
  const addr = server.address();
  const port = typeof addr === "object" && addr ? addr.port : 4339;
  const cvUrl = `http://127.0.0.1:${port}/cv/`;

  try {
    const pdfBuf = await renderPdfViaCDP(chromeBin, cvUrl);
    writeFileSync(outPdf, pdfBuf);
    chmodSync(outPdf, 0o644);
    writeFileSync(publicPdf, pdfBuf);
    chmodSync(publicPdf, 0o644);
    console.log(`[build-cv-pdf] Generated clickable PDF: ${outPdf} (${pdfBuf.length} bytes)`);
    server.closeAllConnections?.();
    server.close();
    process.exit(0);
  } catch (err) {
    server.closeAllConnections?.();
    server.close();
    if (existsSync(outPdf)) {
      console.warn(`[build-cv-pdf] ${err.message}; keeping existing ${outPdf}.`);
      process.exit(0);
    }
    console.error("[build-cv-pdf] Failed to generate PDF:", err);
    process.exit(1);
  }
});
