"""Render interactive Kantorovich Attention animations for the Astra preview.

Uses the exact 3D raised Blue Marble Earth plates, 3D pinched lattice wells,
lit 3D transport tubes, twisting unravelling strand bundles, bipartite tally
strips, and trained-network 180-tile global score matrices from the Astra
manuscript (fig2c_h18.py & fig2b_h18.py) on the #F8F9FA DeepMind surface.
"""
import glob
import importlib.util
import json
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, patheffects
from matplotlib.colors import to_rgb
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Polygon, Rectangle
from matplotlib.transforms import Affine2D
import numpy as np
from PIL import Image

for _f in glob.glob("/data/junuchoi/hyperlane_wb2_prep/fig4b_sprint/M1/fonts_ttf/*.ttf"):
    font_manager.fontManager.addfont(_f)

OUT = Path(__file__).resolve().parents[2] / "public" / "figures" / "astra"
FIG2_DIR = Path("/data/junuchoi/hyperlane_wb2_prep/paper_eff/docs/paper_arxiv/figures/src/fig2_ka")

os.environ["EARTH_AB"] = "A"
os.environ["C3D_MODE"] = "c3d"
os.environ["DM_OT_PLAN"] = str(FIG2_DIR / "ot_panelc_plan.json")


def _load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_bm = _load_mod("bluemarble_earthAB", FIG2_DIR / "bluemarble_earthAB.py")
_t3 = _load_mod("tile3d_c3d", FIG2_DIR / "tile3d_c3d.py")
_cst = _load_mod("v5_c3d", FIG2_DIR / "variant_h18" / "build" / "v5_c3d.py")
_d3 = _load_mod("fig2b_D3", FIG2_DIR / "fig2b_D3.py")

BG = "#F8F9FA"
INK, MUTED, LIGHT = "#202124", "#5F6368", "#64748B"
BLUE, VERM, VIOLET, VIOLET_T = "#2F9BE0", "#F29A2E", "#6A4BC9", "#4B2FA6"

plt.rcParams.update({
    "font.family": "TeX Gyre Heros",
    "font.size": 9.5,
    "text.color": INK,
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
    "lines.solid_joinstyle": "round",
    "lines.solid_capstyle": "round",
    "mathtext.fontset": "stixsans",
})


def tint(c, f):
    return tuple((1 - f) * np.array(to_rgb(c)) + f)


def image_from_figure(fig):
    fig.canvas.draw()
    result = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy())
    plt.close(fig)
    return result


def save_animation(name, frames, durations=None, still_idx=-1):
    sample = Image.new("RGB", (128 * len(frames), 92), BG)
    for index, frame in enumerate(frames):
        sample.paste(frame.resize((128, 92)), (128 * index, 0))
    palette = sample.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    if durations is None:
        cycle = indexed + indexed[-2:0:-1]
        durs = [60] * len(cycle)
        durs[0], durs[len(frames) - 1] = 2200, 2600
    else:
        cycle = indexed
        durs = durations
    cycle[0].save(
        OUT / f"{name}.gif",
        save_all=True,
        append_images=cycle[1:],
        duration=durs,
        loop=0,
        optimize=False,
        disposal=1,
    )
    frames[still_idx].save(OUT / f"{name}-still.png", optimize=True)
    return {"width": frames[0].width, "height": frames[0].height, "frames": len(cycle), "duration_ms": sum(durs)}


# ==============================================================================
# PART 1: Two-sided 3D tile routing (Pull -> Push -> Kantorovich Attention)
# ==============================================================================
EARTH = _bm.Earth(str(FIG2_DIR))
TT, KT = 7, 2
S_T = np.array([
    [0.0, -0.3, -1.3, -1.1, 0.9, 1.6, 1.3],
    [-0.3, -0.9, 1.7, 0.5, -1.1, -1.6, -0.8],
    [0.9, 1.4, -1.6, -2.3, 0.7, 1.8, 1.7],
    [-1.0, -0.6, 1.6, 1.3, -2.3, -1.6, -1.0],
    [0.0, -1.4, 1.0, 0.7, 1.0, -0.7, -1.4],
    [-1.2, -1.7, 2.0, 1.7, -1.5, -2.1, -1.7],
    [-0.4, -1.0, 1.9, 1.3, -0.2, -2.0, -2.1],
])
ORDER_T = [1, 3, 5, 2, 6, 0, 4]
POS_T = {t: n for n, t in enumerate(ORDER_T)}
I_T = 5
POS2 = {1: (0, 1), 3: (1, 3), 5: (3, 2), 2: (4, 0), 6: (5, 3), 0: (5, 2), 4: (5, 0)}
TOY_UV = {POS2[t] for t in range(TT)}


def _topk(rows):
    P = np.zeros((TT, TT), int)
    for a in range(TT):
        c = sorted([b for b in range(TT) if b != a], key=lambda b: -(S_T[a, b] if rows else S_T[b, a]))
        if rows:
            P[a, c[:KT]] = 1
        else:
            P[c[:KT], a] = 1
    return P


P_PULL = _topk(True)
P_PUSH = _topk(False)
P_KA = np.maximum(P_PULL, P_PUSH)
N_I = [j for j in range(TT) if P_PULL[I_T, j]]
R_I = [r for r in range(TT) if P_PUSH[r, I_T]]

NX2, NY2, NPX2 = 6, 4, 72
LAT2_0, LON2_0 = -10, 270
_bm_raw = EARTH.equirect(LAT2_0, LAT2_0 + NY2 * 20, LON2_0, LON2_0 + NX2 * 20, NX2 * NPX2, NY2 * NPX2, ss=2)
_par2 = np.add.outer(NY2 - 1 - np.arange(NY2 * NPX2) // NPX2, np.arange(NX2 * NPX2) // NPX2) % 2
MAP2_RGB = _bm.checker(_bm.treat(_bm_raw), _par2)
MAP2_CTX = _bm.checker(_bm.treat(_bm_raw, lift=_bm.LIFT_CTX), _par2)


def _bevel_earth(img):
    return _t3.shade_img(img, max(2.0, 0.08 * img.shape[1]), lattice=_t3.BOARD_LATTICE)


def _tile_img(u, v, src):
    return src[(NY2 - 1 - v) * NPX2 : (NY2 - v) * NPX2, u * NPX2 : (u + 1) * NPX2]


BEVEL_CACHE = {}
for _u in range(NX2):
    for _v in range(NY2):
        _src = MAP2_RGB if (_u, _v) in TOY_UV else MAP2_CTX
        BEVEL_CACHE[(_u, _v)] = _bevel_earth(_tile_img(_u, _v, _src))

EL_B, DIST_B, HB = 24.5, 28.0, 3.4
OFF_B = 5 / 2 + _cst.GAP_W / 2
CAM = _cst.Camera(0.0, EL_B, DIST_B, (NX2 / 2 - OFF_B, NY2 / 2, 0.3))


def _proj(u, v, h):
    return CAM.proj(np.stack(np.broadcast_arrays(np.asarray(u, float), np.asarray(v, float), np.asarray(h, float)), -1))


_cn = _proj([0, NX2, NX2, 0] * 2, [0, 0, NY2, NY2] * 2, [0.0] * 4 + [HB] * 4)
_EXT = (_cn[:, 0].min(), _cn[:, 0].max(), _cn[:, 1].min(), _cn[:, 1].max())

TUBE_C = {
    BLUE: ("#1F6FA8", BLUE, "#8DC8EE"),
    VERM: ("#A85A0C", VERM, "#F7C485"),
}


def routing_frame(mode_label, bar_col, progress, pull_w, push_w, phase_rad):
    """Render one 720x518 frame of the two-sided 3D tile routing animation."""
    FW, FH = 5.0, 3.6
    fig = plt.figure(figsize=(FW, FH), dpi=144, facecolor=BG)
    ov = fig.add_axes([0, 0, 1, 1], facecolor=BG)
    ov.set_xlim(0, FW)
    ov.set_ylim(0, FH)
    ov.axis("off")

    # Header & progress bar (matching geometry_in_motion.py)
    fig.text(0.055, 0.935, mode_label, color=bar_col, fontsize=10.5, fontweight="bold")
    score_val = 14.1 * pull_w * (1 - 0.5 * push_w) + 14.5 * push_w * (1 - 0.5 * pull_w)
    if pull_w > 0.5 and push_w > 0.5:
        score_val = 14.1 + 7.7 * min(pull_w, push_w)
    fig.text(0.945, 0.935, f"Score  {score_val:.1f} / 21.9", ha="right", fontsize=10.2, fontweight="bold", color=INK)
    fig.lines.extend([
        plt.Line2D([0.055, 0.945], [0.892, 0.892], transform=fig.transFigure, color="#DADCE0", lw=1.8),
        plt.Line2D([0.055, 0.055 + 0.89 * progress], [0.892, 0.892], transform=fig.transFigure, color=bar_col, lw=2.3),
    ])

    # ---- Left side: Bipartite sender/receiver strips & tallies (x = 0.50 .. 1.80) ----
    LX0, LW = 0.50, 1.30
    TSW = LW / TT
    SHH = TSW * 0.78
    Y_SEND = 2.18
    Y_RECV = 1.24

    ov.text(LX0 + LW / 2, 2.94, "Bipartite transport (K = 2)", ha="center", va="center", fontsize=9.2, color=MUTED, fontweight="bold")
    ov.text(LX0 - 0.05, Y_SEND + SHH / 2, "senders", ha="right", va="center", fontsize=7.8, color=MUTED)
    ov.text(LX0 - 0.05, Y_RECV + SHH / 2, "receivers", ha="right", va="center", fontsize=7.8, color=MUTED)

    def cx(t):
        return LX0 + (POS_T[t] + 0.5) * TSW

    def s_curve(x0, y0, x1, y1, n=50):
        t = np.linspace(0.0, 1.0, n)[:, None]
        ym = 0.5 * (y0 + y1)
        p0, p1, p2, p3 = np.array([x0, y0]), np.array([x0, ym]), np.array([x1, ym]), np.array([x1, y1])
        return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3

    # Background & bold bipartite curves
    if pull_w > 0.02:
        for i, j in zip(*np.nonzero(P_PULL)):
            if i == I_T and j in N_I:
                continue
            C_ = s_curve(cx(j), Y_SEND, cx(i), Y_RECV + SHH)
            ov.plot(C_[:, 0], C_[:, 1], color=tint(BLUE, 0.60), lw=0.65, alpha=float(pull_w), zorder=2.5)
        for n_, j in enumerate(N_I):
            dx = (-0.18 if n_ == 0 else 0.18) * TSW
            C_ = s_curve(cx(j), Y_SEND, cx(I_T) + dx, Y_RECV + SHH)
            sub_n = max(2, int(round(len(C_) * min(1.0, pull_w * 1.15))))
            ov.plot(C_[:sub_n, 0], C_[:sub_n, 1], color=BLUE, lw=1.65, alpha=float(min(1.0, pull_w * 1.2)), zorder=4.2)

    if push_w > 0.02:
        for i, j in zip(*np.nonzero(P_PUSH)):
            if j == I_T and i in R_I:
                continue
            C_ = s_curve(cx(j), Y_SEND, cx(i), Y_RECV + SHH)
            ov.plot(C_[:, 0], C_[:, 1], color=tint(VERM, 0.52), lw=0.65, ls=(0, (2.2, 1.4)), alpha=float(push_w), zorder=2.6)
        for n_, r in enumerate(R_I):
            dx = (-0.18 if n_ == 0 else 0.18) * TSW
            C_ = s_curve(cx(I_T) + dx, Y_SEND, cx(r), Y_RECV + SHH)
            sub_n = max(2, int(round(len(C_) * min(1.0, push_w * 1.15))))
            ov.plot(C_[:sub_n, 0], C_[:sub_n, 1], color=VERM, lw=1.65, ls=(0, (2.5, 1.4)), alpha=float(min(1.0, push_w * 1.2)), zorder=4.3)

    # Effective adjacency for tallies & hatching
    P_EFF = np.zeros((TT, TT), int)
    if pull_w >= 0.45 and push_w >= 0.45:
        P_EFF = P_KA
    elif pull_w >= push_w:
        P_EFF = P_PULL
    else:
        P_EFF = P_PUSH
    rb, rd = P_EFF.sum(0), P_EFF.sum(1)

    for y_strip, counts, is_send in ((Y_SEND, rb, True), (Y_RECV, rd, False)):
        for t in range(TT):
            p = POS_T[t]
            x0 = LX0 + p * TSW + 0.012
            w0 = TSW - 0.024
            is_i = t == I_T
            fc = "#FFFFFF" if is_i else "#EAECEF"
            ec = INK if is_i else "#CBD5E1"
            lw = 1.2 if is_i else 0.6
            ov.add_patch(Rectangle((x0, y_strip), w0, SHH, fc=fc, ec=ec, lw=lw, zorder=3.5))
            if counts[t] == 0 and not is_i:
                for h0 in (-0.4, 0.0, 0.4):
                    u0, u1 = max(0.0, h0), min(1.0, 1.0 + h0)
                    v0, v1 = max(0.0, -h0), min(1.0, 1.0 - h0)
                    ov.plot([x0 + u0 * w0, x0 + u1 * w0], [y_strip + v0 * SHH, y_strip + v1 * SHH], color="#94A3B8", lw=0.7, zorder=3.7)
            if is_i:
                ov.text(x0 + w0 / 2, y_strip + SHH / 2, "i", fontsize=8.5, fontstyle="italic", fontweight="bold", ha="center", va="center", color=INK, zorder=4.0)

            # Tally bars
            bw = 0.56 * TSW
            bh, bg = 0.038, 0.013
            if pull_w >= 0.45 and push_w >= 0.45:
                cols = ([VERM] * KT + [BLUE] * max(0, counts[t] - KT)) if is_send else ([BLUE] * KT + [VERM] * max(0, counts[t] - KT))
            elif pull_w >= push_w:
                cols = [BLUE] * counts[t]
            else:
                cols = [VERM] * counts[t]
            for n in range(max(len(cols), KT)):
                ty = (y_strip + SHH + 0.022 + n * (bh + bg)) if is_send else (y_strip - 0.022 - (n + 1) * (bh + bg))
                if n < len(cols):
                    ov.add_patch(Rectangle((cx(t) - bw / 2, ty), bw, bh, fc=cols[n], ec="none", zorder=4.0))
                else:
                    ov.add_patch(Rectangle((cx(t) - bw / 2, ty), bw, bh, fc="white", ec=INK, lw=0.55, zorder=4.0))

    # K floor lines
    bh, bg = 0.038, 0.013
    yk_up = Y_SEND + SHH + 0.022 + KT * (bh + bg) - bg / 2
    yk_dn = Y_RECV - 0.022 - KT * (bh + bg) + bg / 2
    ov.plot([LX0, LX0 + LW], [yk_up, yk_up], color=MUTED, lw=0.7, ls=(0, (1.2, 1.6)), zorder=4.5)
    ov.plot([LX0, LX0 + LW], [yk_dn, yk_dn], color=MUTED, lw=0.7, ls=(0, (1.2, 1.6)), zorder=4.5)
    ov.text(LX0 + LW + 0.03, yk_up, "K", fontsize=7.6, fontstyle="italic", color=MUTED, va="center")
    ov.text(LX0 + LW + 0.03, yk_dn, "K", fontsize=7.6, fontstyle="italic", color=MUTED, va="center")

    if int((rb == 0).sum()) > 0:
        ux = np.mean([cx(t) for t in range(TT) if rb[t] == 0])
        ov.text(ux, yk_up + 0.05, "unread", fontsize=7.5, color="#C2410C", fontweight="bold", ha="center")
    if int((rd == 0).sum()) > 0:
        rx = np.mean([cx(t) for t in range(TT) if rd[t] == 0])
        ov.text(rx, yk_dn - 0.08, "reads none", fontsize=7.5, color="#C2410C", fontweight="bold", ha="center")

    # ---- Right side: 3D Raised Earth Plates & Twisting Tubes (x = 2.58 .. 4.80) ----
    BX0, BW = 2.58, 2.22
    BY_TOP = 2.66
    x0_, x1_, y0_, y1_ = _EXT
    KB = BW / (x1_ - x0_)

    ov.text(BX0 + BW / 2, 2.94, "3D tile transfers around query i", ha="center", va="center", fontsize=9.2, color=MUTED, fontweight="bold")

    def BP(u, v, h):
        q = _proj(u, v, h)
        return np.stack([
            BX0 + (q[..., 0] - x0_) * KB,
            BY_TOP - (y1_ - q[..., 1]) * KB,
        ], -1)

    def quad(u, v, h, nu=1.0, nv=1.0):
        return BP([u, u + nu, u + nu, u], [v, v, v + nv, v + nv], h)

    def face_img(u, v, h, img, z, alpha=1.0):
        Q = quad(u, v, h)
        S_ = np.array([[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]], float)
        M = np.linalg.lstsq(S_, Q, rcond=None)[0]
        tr = Affine2D.from_values(M[0, 0], M[0, 1], M[1, 0], M[1, 1], M[2, 0], M[2, 1]) + ov.transData
        e = 0.01
        im = ov.imshow(img, extent=[-e, 1 + e, -e, 1 + e], origin="upper", interpolation="bilinear", transform=tr, zorder=z, aspect="auto", alpha=alpha)
        im.set_clip_path(Polygon(Q, closed=True, transform=ov.transData))

    def draw_plane(h, z, alpha):
        for u in range(NX2):
            for v in range(NY2):
                face_img(u, v, h, BEVEL_CACHE[(u, v)], z, alpha=alpha)
        for k in range(1, NX2):
            P_ = BP([k, k], [0, NY2], h)
            ov.plot(P_[:, 0], P_[:, 1], color="white", lw=0.45, zorder=z + 0.2)
        for k in range(1, NY2):
            P_ = BP([0, NX2], [k, k], h)
            ov.plot(P_[:, 0], P_[:, 1], color="white", lw=0.45, zorder=z + 0.2)
        ov.add_patch(Polygon(quad(0, 0, h, NX2, NY2), closed=True, fill=False, ec=LIGHT, lw=0.45, zorder=z + 0.3))
        for (u, v) in TOY_UV:
            ov.add_patch(Polygon(_cst.inset_poly(quad(u, v, h), 0.6 / 72), closed=True, fill=False, ec=MUTED, lw=0.55, zorder=z + 0.25))

    def mark_tile(t, h, kind, col, z, alpha=1.0):
        u, v = POS2[t]
        Q = quad(u, v, h)
        if kind == "i":
            ov.add_patch(Polygon(Q, closed=True, fc="white", ec=INK, lw=1.0, zorder=z))
            c_ = BP(u + (0.72 if h == 0 else 0.5), v + (0.38 if h == 0 else 0.5), h)
            ti = ov.text(c_[0], c_[1], "i", fontsize=7.6, fontstyle="italic", fontweight="bold", color=INK, ha="center", va="center", zorder=z + 2.0)
            ti.set_path_effects([patheffects.withStroke(linewidth=2.2, foreground="white")])
        else:
            ov.add_patch(Polygon(Q, closed=True, fc=col, ec="none", alpha=0.30 * alpha, zorder=z))
            ov.add_patch(Polygon(_cst.inset_poly(Q, 0.5 / 72), closed=True, fill=False, ec=col, lw=1.0, alpha=alpha, zorder=z + 0.05))

    def lit_tube(Q, cols, w, z, alpha=1.0):
        if len(Q) < 2 or alpha <= 0.02:
            return
        dark, base, light = cols
        Qp = np.asarray(Q) * 72
        d = np.gradient(Qp, axis=0)
        d /= np.maximum(np.hypot(d[:, 0], d[:, 1]), 1e-9)[:, None]
        n = np.c_[-d[:, 1], d[:, 0]]
        n *= np.sign(n @ np.array([-0.6, 0.8]) + 1e-9)[:, None]
        ov.plot(*(Qp / 72).T, color="white", lw=w + 0.55, alpha=alpha, zorder=z - 0.003)
        ov.plot(*(Qp / 72).T, color=dark, lw=w, alpha=alpha, zorder=z)
        ov.plot(*((Qp + n * 0.12 * w) / 72).T, color=base, lw=0.64 * w, alpha=alpha, zorder=z + 0.001)
        ov.plot(*((Qp + n * 0.22 * w) / 72).T, color=light, lw=0.28 * w, alpha=alpha, zorder=z + 0.002)

    def bundle(U, Eb, cols, n_strands, phase, z=1.72, alpha=1.0):
        if alpha <= 0.05:
            return
        s = np.linspace(0, 1, 48)
        tau = 1.7 * np.pi
        rho = 0.36
        for k in range(n_strands):
            ph = phase + 2 * np.pi * k / n_strands
            rk = rho * (0.62 if k % 2 else 1.0)
            r = 0.035 + (rk - 0.035) * s ** 1.3
            a = ph - tau * (1 - s)
            P = U[None] + (Eb - U)[None] * s[:, None] + np.c_[r * np.cos(a), r * np.sin(a), np.zeros_like(s)]
            Q = BP(P[:, 0], P[:, 1], P[:, 2])
            ov.plot(Q[:, 0], Q[:, 1], color="white", lw=0.80, alpha=alpha, zorder=z - 0.002)
            ov.plot(Q[:, 0], Q[:, 1], color=cols[1] if k % 2 == 0 else cols[0], lw=0.48, alpha=alpha, zorder=z)

    def bez3(P0, P1, P2, P3, n=60):
        t = np.linspace(0, 1, n)[:, None]
        return (1 - t) ** 3 * P0 + 3 * (1 - t) ** 2 * t * P1 + 3 * (1 - t) * t ** 2 * P2 + t ** 3 * P3

    # Lower queries plate
    draw_plane(0.0, 1.0, 1.0)
    mark_tile(I_T, 0.0, "i", INK, 1.5)
    if push_w > 0.02:
        for r in R_I:
            mark_tile(r, 0.0, "pick", VERM, 1.52, alpha=float(push_w))

    # Upper keys/values plate
    draw_plane(HB, 2.0, _cst.UPPER_ALPHA)
    mark_tile(I_T, HB, "i", INK, 2.45)
    if pull_w > 0.02:
        for j in N_I:
            mark_tile(j, HB, "pick", BLUE, 2.42, alpha=float(pull_w))
        routed_uv = {POS2[I_T]} | {POS2[j] for j in N_I}
        for u in range(NX2):
            for v in range(NY2):
                if (u, v) not in routed_uv:
                    c_ = BP(u + 0.5, v + 0.5, HB)
                    ov.add_patch(Circle(tuple(c_), 0.018, fc=LIGHT, ec=INK, lw=0.35, alpha=float(pull_w), zorder=2.35))

    # 3D tubes & twisting strands between plates
    S_pt = lambda ta: np.array([POS2[ta][0] + 0.5, POS2[ta][1] + 0.5, HB])
    E_pt = lambda tb: np.array([POS2[tb][0] + 0.5, POS2[tb][1] + 0.5, 0.0])
    UNRAVEL_Z = 0.85

    if pull_w > 0.02:
        Ei = E_pt(I_T)
        U = Ei + np.array([0, 0, UNRAVEL_Z])
        for ta in [I_T] + N_I:
            P0 = S_pt(ta)
            curve3 = bez3(P0, P0 + [0, 0, -0.9], U + [0, 0, 0.9], U)
            Q = BP(curve3[:, 0], curve3[:, 1], curve3[:, 2])
            lit_tube(Q, TUBE_C[BLUE], 1.35, 1.70, alpha=float(pull_w))
        bundle(U, Ei, TUBE_C[BLUE], 7, phase_rad, z=1.72, alpha=float(pull_w))

    if push_w > 0.02:
        for tb in [I_T] + R_I:
            P0, Eb = S_pt(I_T), E_pt(tb)
            U = Eb + np.array([0, 0, UNRAVEL_Z])
            curve3 = bez3(P0, P0 + [0, 0, -0.9], U + [0, 0, 0.9], U)
            Q = BP(curve3[:, 0], curve3[:, 1], curve3[:, 2])
            lit_tube(Q, TUBE_C[VERM], 1.35, 1.74, alpha=float(push_w))
            bundle(U, Eb, TUBE_C[VERM], 5, -phase_rad + (0.6 if tb == I_T else 0.0), z=1.75, alpha=float(push_w))

    p_top_l = BP(0, NY2 / 2, HB)
    p_bot_l = BP(0, NY2 / 2, 0.0)
    ov.text(p_top_l[0] - 0.05, p_top_l[1], "keys,\nvalues", ha="right", va="center", fontsize=7.4, color=MUTED)
    ov.text(p_bot_l[0] - 0.05, p_bot_l[1], "queries", ha="right", va="center", fontsize=7.4, color=MUTED)

    # Bottom metrics (matching geometry_in_motion.py)
    n_unread_s = int((rb == 0).sum())
    n_unread_r = int((rd == 0).sum())
    fig.text(0.055, 0.11, "MARGINAL COVERAGE (K = 2 FLOOR)", fontsize=9.0, color=MUTED)
    if n_unread_s == 0 and n_unread_r == 0:
        fig.text(0.055, 0.04, "0 unread on both sides", color=VIOLET_T, fontsize=11.5, fontweight="bold")
        fig.text(0.56, 0.04, r"Two-sided top-$K$ (no solver)", color=INK, fontsize=10.8)
    elif pull_w >= push_w:
        fig.text(0.055, 0.04, f"{n_unread_s} of 7 senders unread", color=BLUE, fontsize=11.5, fontweight="bold")
        fig.text(0.56, 0.04, r"Gather $K = 2$ into $i$", color=MUTED, fontsize=10.8)
    else:
        fig.text(0.055, 0.04, f"{n_unread_r} of 7 receivers read none", color="#C2410C", fontsize=11.5, fontweight="bold")
        fig.text(0.56, 0.04, r"Scatter $i$ to $K = 2$", color=MUTED, fontsize=10.8)

    return image_from_figure(fig)


# ==============================================================================
# PART 2: Global coverage on the trained network's scores (180 20-deg tiles)
# ==============================================================================
D_GLOBE = _d3.load()
SEG_COAST = _d3.coasts()
K_G, T_G, GW_G, LATS_G, EDGES_G = _d3.K, _d3.T, _d3.GW, _d3.LATS, _d3.EDGES
CLS_G = ["#FFFFFF", "#E6EBF2", "#A9B6C8", "#4A5B74", "#111827"]
HATCH_G, COAST_G = "#94A3B8", "#3B4A60"

# Precompute 3D raised cell overlay for the 18x10 global map
CW_G = 3.92
MH_G = CW_G / 2
PPI_G = 300
_sx_g = CW_G / 360.0
_xe_g = np.array([20 * c * _sx_g for c in range(GW_G + 1)]) * PPI_G
_ye_g = np.array([(90 - la) * _sx_g for la in LATS_G]) * PPI_G


def _cells_overlay(xe, ye, bev_px, k_hi=0.40, k_lo=0.40, grad=0.06):
    Wp, Hp = int(round(xe[-1])), int(round(ye[-1]))
    y, x = np.mgrid[0:Hp, 0:Wp] + 0.5
    c = np.clip(np.searchsorted(xe, x[0], side="right") - 1, 0, len(xe) - 2)
    r = np.clip(np.searchsorted(ye, y[:, 0], side="right") - 1, 0, len(ye) - 2)
    x0, x1 = xe[c][None, :], xe[c + 1][None, :]
    y0, y1 = ye[r][:, None], ye[r + 1][:, None]
    D = np.stack(np.broadcast_arrays(x - x0, y - y0, x1 - x, y1 - y)) / bev_px
    k = np.argmin(D, 0)
    wgt = np.clip(1 - D.min(0), 0, 1) ** 1.6
    t = ((x - x0) / (x1 - x0) + (y - y0) / (y1 - y0)) / 2
    return _t3.overlay_from(wgt * (k <= 1), wgt * (k >= 2), t, k_hi=k_hi, k_lo=k_lo, grad=grad)


GLOBE_OVERLAY_3D = _cells_overlay(_xe_g, _ye_g, 0.45 / 72 * PPI_G)

RB_PULL = D_GLOBE["rb"]["pull"].astype(float)
RB_KA = D_GLOBE["rb"]["ka"].astype(float)


def coverage_frame(s):
    """Render one 720x518 frame of the global coverage animation for s in [0, 1]."""
    FW, FH = 5.0, 3.6
    fig = plt.figure(figsize=(FW, FH), dpi=144, facecolor=BG)
    ov = fig.add_axes([0, 0, 1, 1], facecolor=BG)
    ov.set_xlim(0, FW)
    ov.set_ylim(0, FH)
    ov.axis("off")

    rng = np.random.default_rng(20261027)
    thresh = rng.uniform(0.04, 0.92, size=T_G)
    active = np.clip((s - thresh + 0.12) / 0.12, 0.0, 1.0)
    if s <= 0.001:
        active[:] = 0.0
    elif s >= 0.999:
        active[:] = 1.0
    rb_cur = np.round(RB_PULL + active * (RB_KA - RB_PULL)).astype(int)
    cls_cur = np.digitize(rb_cur, EDGES_G[1:-1])
    n_unread = int((rb_cur == 0).sum())

    # Header & progress bar
    title_str = r"Pull alone  $\rightarrow$  Two-sided top-$K$ ($K = 8$)"
    fig.text(0.055, 0.935, title_str, color=MUTED if s < 0.5 else VIOLET_T, fontsize=10.5, fontweight="bold")
    endpoint = s <= 0.001 or s >= 0.999
    fig.text(
        0.945,
        0.935,
        f"{n_unread} / 180 unread" if endpoint else "",
        ha="right",
        fontsize=10.5,
        fontweight="bold",
        color="#C2410C" if n_unread > 0 else VIOLET_T,
    )
    fig.lines.extend([
        plt.Line2D([0.055, 0.945], [0.892, 0.892], transform=fig.transFigure, color="#DADCE0", lw=1.8),
        plt.Line2D([0.055, 0.055 + 0.89 * s], [0.892, 0.892], transform=fig.transFigure, color=VIOLET if s > 0.1 else BLUE, lw=2.3),
    ])

    # ---- Global 3D Raised-Tile Map (18 x 10 tiles of 20 deg, fits well below progress bar) ----
    XM, YM = (FW - CW_G) / 2, 1.06
    sx = CW_G / 360.0
    yy = lambda lat: YM + (lat + 90.0) * sx

    for t in range(T_G):
        r, c = divmod(t, GW_G)
        xa, xb = XM + 20 * c * sx, XM + (20 * c + 20) * sx
        ya, yb = yy(LATS_G[r + 1]), yy(LATS_G[r])
        k = int(cls_cur[t])
        ov.add_patch(Rectangle((xa, ya), xb - xa, yb - ya, fc=CLS_G[k], ec="none", zorder=1.0))
        if k == 0:
            for f0 in (-0.5, 0.0, 0.5):
                u0, u1 = max(0.0, f0), min(1.0, 1.0 + f0)
                v0, v1 = max(0.0, -f0), min(1.0, 1.0 - f0)
                ov.add_line(
                    Line2D(
                        [xa + u0 * (xb - xa), xa + u1 * (xb - xa)],
                        [ya + v0 * (yb - ya), ya + v1 * (yb - ya)],
                        color=HATCH_G,
                        lw=0.55,
                        zorder=1.5,
                    )
                )

    ov.imshow(
        GLOBE_OVERLAY_3D,
        extent=[XM, XM + CW_G, YM, YM + MH_G],
        interpolation="bilinear",
        aspect="auto",
        zorder=1.8,
    )
    for la in LATS_G[1:-1]:
        ov.add_line(Line2D([XM, XM + CW_G], [yy(la)] * 2, color="white", lw=0.45, zorder=2.2))
    for c in range(1, GW_G):
        ov.add_line(Line2D([XM + 20 * c * sx] * 2, [YM, YM + MH_G], color="white", lw=0.45, zorder=2.2))
    for seg in SEG_COAST:
        ov.add_line(Line2D(XM + seg[:, 0] * sx, yy(seg[:, 1]), color=COAST_G, lw=0.48, alpha=0.82, zorder=2.6))
    ov.add_patch(Rectangle((XM, YM), CW_G, MH_G, fc="none", ec=LIGHT, lw=0.6, zorder=3.0))

    # ---- Class key directly below map ----
    YK = 0.74
    SW, KH = 0.38, 0.105
    KX0 = XM
    labels = ["0 (unread)", "1–7", "8–15", "16–31", "≥ 32"]
    for k in range(5):
        kx = KX0 + k * SW
        ov.add_patch(Rectangle((kx, YK), SW, KH, fc=CLS_G[k], ec="none", zorder=3.5))
        if k == 0:
            for f0 in (-0.5, 0.0, 0.5):
                u0, u1 = max(0.0, f0), min(1.0, 1.0 + f0)
                v0, v1 = max(0.0, -f0), min(1.0, 1.0 - f0)
                ov.add_line(Line2D([kx + u0 * SW, kx + u1 * SW], [YK + v0 * KH, YK + v1 * KH], color=HATCH_G, lw=0.55, zorder=3.7))
        ov.text(kx + SW / 2, YK - 0.095, labels[k], fontsize=7.4, color=MUTED, ha="center", va="center")
    ov.add_patch(Rectangle((KX0, YK), 5 * SW, KH, fc="none", ec=LIGHT, lw=0.55, zorder=4.0))
    ov.add_line(Line2D([KX0 + 2 * SW] * 2, [YK - 0.025, YK + KH + 0.025], color=INK, lw=1.0, ls=(0, (1.2, 1.4)), zorder=5.0))
    ov.text(KX0 + 2 * SW + 0.03, YK + KH / 2, "K = 8", fontsize=7.6, color=INK, fontstyle="italic", fontweight="bold", va="center")
    ov.text(KX0 + 5 * SW + 0.34, YK + KH / 2, "Readers per tile (trained L2 head)", fontsize=7.8, color=MUTED, va="center")

    # ---- Bottom metrics (matching geometry_in_motion.py) ----
    fig.text(0.055, 0.11, "TRAINED NETWORK (4,608 SCORE MATRICES)", fontsize=9.0, color=MUTED)
    if s <= 0.001:
        fig.text(0.055, 0.04, "Unread  28% on average (2° tiles)", color=BLUE, fontsize=11.2, fontweight="bold")
    elif s >= 0.999:
        fig.text(0.055, 0.04, "Unread  0% (by construction)", color=VIOLET_T, fontsize=11.2, fontweight="bold")
        fig.text(0.58, 0.04, "OT gain  94–98%", color=INK, fontsize=11.2, fontweight="bold")

    return image_from_figure(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    routing_frames = []
    routing_durs = []
    for k in range(16):
        ph = 2 * np.pi * k / 16
        w_in = min(1.0, (k + 2) / 6.0)
        routing_frames.append(routing_frame(r"Pull alone  (Gather $K$ senders $\rightarrow i$)", BLUE, 0.33 * (k / 15), w_in, 0.0, ph))
        routing_durs.append(550 if k == 15 else 65)
    for k in range(16):
        ph = 2 * np.pi * k / 16
        w_out = min(1.0, (k + 2) / 6.0)
        routing_frames.append(routing_frame(r"Push alone  (Scatter $i \rightarrow K$ receivers)", VERM, 0.33 + 0.33 * (k / 15), 0.0, w_out, ph))
        routing_durs.append(550 if k == 15 else 65)
    for k in range(24):
        ph = 2 * np.pi * k / 24
        w_both = min(1.0, (k + 2) / 6.0)
        routing_frames.append(
            routing_frame(
                r"Kantorovich Attention  (Pull $\cup$ Push)",
                VIOLET,
                0.66 + 0.34 * min(1.0, k / 10.0),
                w_both,
                w_both,
                ph,
            )
        )
        routing_durs.append(900 if k == 23 else 65)

    r_info = save_animation("ka-routing", routing_frames, durations=routing_durs, still_idx=-1)

    steps = (1 - np.cos(np.linspace(0, np.pi, 37))) / 2
    cov_frames = [coverage_frame(float(s)) for s in steps]
    c_info = save_animation("ka-coverage", cov_frames, durations=None, still_idx=-1)

    print(json.dumps({"ka_routing": r_info, "ka_coverage": c_info}, indent=2))


if __name__ == "__main__":
    main()
