"""Render DeepMind-style PTM empirical showcase figures on #F8F9FA.

Produces two responsive assets in public/figures/ptm/:
  1. benchmark-overview.webp : Wide 2-panel banner for /papers/#ptm combining
     (a) 3 image restoration tasks (PR, HDR, NL) with 48x48 zoom insets & PSNR
     and (b) 4 InverseBench scientific inverse problems (reconstructions + metrics).
  2. hero-results.webp : Compact high-legibility card for the Home page Papers row
     combining (a) top restoration zoom comparisons and (b) InverseBench strip.

Environment variables:
  FIGURE_FONT_DIR : directory containing TeX Gyre Heros .ttf files (optional)
  PTM_QUAL_DIR    : path to publication/story/figure_evidence/qualitative
  PTM_IB_DIR      : path to inversebench_uniform_20261019/runs
  PTM_FWI_DIR     : path to inversebench_search/fwi/test
"""
import glob
import json
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np
from PIL import Image
import torch

FONT_DIR = os.environ.get("FIGURE_FONT_DIR")
for _f in glob.glob(os.path.join(FONT_DIR, "*.ttf")) if FONT_DIR else []:
    font_manager.fontManager.addfont(_f)

OUT_DIR = Path(__file__).resolve().parents[2] / "public" / "figures" / "ptm"
QUAL_DIR = Path(os.environ["PTM_QUAL_DIR"])
IB_DIR = Path(os.environ["PTM_IB_DIR"])
FWI_DIR = Path(os.environ["PTM_FWI_DIR"])

BG = "#F8F9FA"
CARD_BG = "#FFFFFF"
BORDER = "#DADCE0"
INK = "#202124"
MUTED = "#5F6368"
BLUE = "#1A73E8"
TEAL = "#0D9488"
GOLD = "#F0E442"

plt.rcParams.update({
    "font.family": "TeX Gyre Heros",
    "font.size": 8.5,
    "mathtext.fontset": "stixsans",
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
})


def load_qual_data():
    return json.loads((QUAL_DIR / "TILES.json").read_text())


def draw_zoom_tile(ax, img, crop, corner, highlight_ptm=False):
    h, w = img.shape[:2]
    ax.imshow(img, interpolation="none", extent=(0, w, h, 0))
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    if crop is not None:
        r0, c0, n = crop
        ax.add_patch(Rectangle((c0, r0), n, n, fill=False, ec=GOLD, lw=1.0, zorder=3))
        side = 0.45 * h
        x0 = 0 if corner[1] == "l" else w - side
        y0 = 0 if corner[0] == "t" else h - side
        ax.imshow(
            img[r0 : r0 + n, c0 : c0 + n],
            interpolation="none",
            extent=(x0, x0 + side, y0 + side, y0),
            zorder=4,
        )
        ax.add_patch(Rectangle((x0, y0), side, side, fill=False, ec=GOLD, lw=1.35, zorder=5))

    if highlight_ptm:
        ax.add_patch(Rectangle((1.0, 1.0), w - 2.0, h - 2.0, fill=False, ec=BLUE, lw=1.8, zorder=6))


def load_ib_samples():
    # 1. Black Hole (aligned)
    bh_path = IB_DIR / "bh_test/bh_30a684c7/c11/evaluation/PoEM-GR/bh_30a684c7_test_c11/result_55.pt"
    bh_d = torch.load(bh_path, map_location="cpu", weights_only=False)
    bh_rec = bh_d["recon"][0, 0].double()
    bh_gt = bh_d["target"][0, 0].double()
    cc = torch.fft.ifft2(torch.fft.fft2(bh_rec) * torch.fft.fft2(bh_gt).conj()).real
    sh_r, sh_c = divmod(int(torch.argmax(cc)), bh_rec.shape[1])
    bh_rec = torch.roll(bh_rec, shifts=(-sh_r, -sh_c), dims=(0, 1)).numpy()
    bh_gt = bh_gt.numpy()

    # 2. Scattering 60 receivers
    scat_path = IB_DIR / "scat_test/scat_79756f1a/r60_c0/evaluation/PoEM-GR/scat_79756f1a_test_r60_c0/result_15.pt"
    scat_d = torch.load(scat_path, map_location="cpu", weights_only=False)
    scat_rec = scat_d["recon"][0, 0].numpy()
    scat_gt = scat_d["target"][0, 0].numpy()

    # 3. Knee MRI 4x
    mri_path = IB_DIR / "mri_test/mri_ebd55640/c1/evaluation/PoEM-GR/mri_ebd55640_test_c1/result_29.pt"
    mri_d = torch.load(mri_path, map_location="cpu", weights_only=False)
    mri_rec = mri_d["recon"][0].norm(dim=0).numpy()
    mri_gt = mri_d["target"][0].norm(dim=0).numpy()

    # 4. Full Waveform Inversion
    fwi_path = FWI_DIR / "F3_t8/evaluation/PoEM-GR/test_F3_t8/result_8.pt"
    fwi_d = torch.load(fwi_path, map_location="cpu", weights_only=False)
    fwi_rec = fwi_d["recon"][0, 0].numpy()
    fwi_gt = fwi_d["target"][0, 0].numpy()

    return {
        "bh": (bh_rec, bh_gt),
        "scat": (scat_rec, scat_gt),
        "mri": (mri_rec, mri_gt),
        "fwi": (fwi_rec, fwi_gt),
    }


def render_image_tile(arr, cmap, vmin, vmax):
    norm = np.clip((arr - vmin) / max(vmax - vmin, 1e-12), 0.0, 1.0)
    rgba = matplotlib.colormaps[cmap](norm)
    return (rgba[:, :, :3] * 255).round().astype(np.uint8)


def build_wide_banner(qual_data, ib):
    W, H = 12.0, 5.85
    fig = plt.figure(figsize=(W, H), dpi=200, facecolor=BG)

    # Top section headers
    fig.text(0.012, 0.955, "a.", fontsize=11.5, fontweight="bold", color=MUTED, va="center")
    fig.text(0.030, 0.955, "Image Restoration with Zoom Callouts (256×256)", fontsize=11.5, fontweight="bold", color=INK, va="center")
    fig.text(
        0.030, 0.918,
        r"100-image cohorts: PTM leads all 8 FFHQ tasks in PSNR & energy score at 5.0–7.9× lower denoiser cost ($D_{\mathsf{eff}}$) than DAPS",
        fontsize=8.1, color=MUTED, va="center",
    )

    # Vertical divider
    fig.lines.append(plt.Line2D([0.542, 0.542], [0.03, 0.97], transform=fig.transFigure, color=BORDER, lw=1.0))

    fig.text(0.558, 0.955, "b.", fontsize=11.5, fontweight="bold", color=MUTED, va="center")
    fig.text(0.576, 0.955, "Scientific Inverse Problems (InverseBench)", fontsize=11.5, fontweight="bold", color=INK, va="center")
    fig.text(
        0.576, 0.918,
        "Single-particle PTM attains the #1 primary metric on all 4 physical benchmarks vs. training-free baselines",
        fontsize=7.5, color=MUTED, va="center",
    )

    # Left panel: 3 qualitative rows x 5 columns
    rows_spec = [
        ("imagenet", "phase_retrieval", "Phase\nRetrieval", "ImageNet"),
        ("ffhq", "hdr", "HDR\nRestoration", "FFHQ"),
        ("ffhq", "nonlinear_blur", "Nonlinear\nBlur", "FFHQ"),
    ]
    cols_spec = [
        ("y", "Observation y"),
        ("b2", "2nd-best baseline"),
        ("b1", "Best baseline"),
        ("ptm", "PTM (Ours)"),
        ("gt", "Ground truth"),
    ]

    left_x0 = 0.060
    tile_w = 0.087
    tile_h = tile_w * (W / H)
    gap_x = 0.0085
    col_headers_y = 0.868

    for c_idx, (col_key, col_title) in enumerate(cols_spec):
        xc = left_x0 + c_idx * (tile_w + gap_x) + tile_w / 2
        fig.text(
            xc, col_headers_y, col_title,
            ha="center", va="center",
            fontsize=8.3,
            fontweight="bold" if col_key == "ptm" else "normal",
            color=BLUE if col_key == "ptm" else INK,
        )

    row_tops = [0.840, 0.560, 0.280]
    for r_idx, (ds, task, task_label, ds_label) in enumerate(rows_spec):
        row = next(r for r in qual_data["rows"] if r["ds"] == ds and r["task"] == task)
        top_y = row_tops[r_idx]
        bot_y = top_y - tile_h
        ymid = (top_y + bot_y) / 2

        fig.text(0.031, ymid + 0.015, task_label, ha="center", va="center", fontsize=8.3, fontweight="bold", color=INK, linespacing=1.15)
        fig.text(0.031, ymid - 0.036, f"({ds_label})", ha="center", va="center", fontsize=7.4, color=MUTED)

        b1_psnr = row["tiles"]["b1"]["psnr_stored"]
        b2_psnr = row["tiles"]["b2"]["psnr_stored"]
        ptm_psnr = row["tiles"]["ptm"]["psnr_stored"]
        gain = ptm_psnr - max(b1_psnr, b2_psnr)

        for c_idx, (col_key, _) in enumerate(cols_spec):
            x0 = left_x0 + c_idx * (tile_w + gap_x)
            ax = fig.add_axes([x0, bot_y, tile_w, tile_h])
            img = np.asarray(Image.open(QUAL_DIR / "tiles" / f"{ds}_{task}_{col_key}.png"))
            crop = None if (col_key == "y" and row["abbr"] == "PR") else row["crop"]
            draw_zoom_tile(ax, img, crop, row["inset_corner"], highlight_ptm=(col_key == "ptm"))

            xc = x0 + tile_w / 2
            ytxt = bot_y - 0.024
            if col_key in ("b2", "b1"):
                t = row["tiles"][col_key]
                fig.text(xc, ytxt, f"{t['method']}  {t['psnr_stored']:.2f} dB", ha="center", va="center", fontsize=7.6, color=INK)
            elif col_key == "ptm":
                fig.text(xc, ytxt, f"{ptm_psnr:.2f} dB (+{gain:.2f})", ha="center", va="center", fontsize=7.8, fontweight="bold", color=BLUE)
            elif col_key == "y":
                note = r"$\log_{10} |F(x)|$" if row["abbr"] == "PR" else ("Clipped range" if row["abbr"] == "HDR" else "Blurred input")
                fig.text(xc, ytxt, note, ha="center", va="center", fontsize=7.3, color=MUTED)
            elif col_key == "gt":
                fig.text(xc, ytxt, "Reference", ha="center", va="center", fontsize=7.3, color=MUTED)

    # Right panel: 2x2 grid of InverseBench tasks
    bh_rec, bh_gt = ib["bh"]
    scat_rec, scat_gt = ib["scat"]
    mri_rec, mri_gt = ib["mri"]
    fwi_rec, fwi_gt = ib["fwi"]

    ib_cards = [
        {
            "title": "Black-Hole Interferometry (EHT)",
            "rec": render_image_tile(bh_rec, "afmhot", 0.0, bh_gt.max()),
            "gt": render_image_tile(bh_gt, "afmhot", 0.0, bh_gt.max()),
            "ptm_metric": r"PTM  28.40 dB  ($\tilde{\chi}^2_{\mathsf{cp}}$ 1.147)",
            "base_metric": "vs. PnP-DM 26.07 · DAPS 25.60 dB",
            "badge": "+2.33 dB · #1 closure",
        },
        {
            "title": "Inverse Scattering (Helmholtz, 60 rec.)",
            "rec": render_image_tile(scat_rec, "viridis", 0.0, scat_gt.max()),
            "gt": render_image_tile(scat_gt, "viridis", 0.0, scat_gt.max()),
            "ptm_metric": "PTM  33.11 dB  (.978 SSIM)",
            "base_metric": "vs. DDNM 29.24 · RED-diff 27.07 dB",
            "badge": "+3.87 dB (360 rec: 40.19 dB)",
        },
        {
            "title": "Multi-Coil Knee MRI (4× raw k-space)",
            "rec": render_image_tile(mri_rec, "gray", 0.0, np.percentile(mri_gt, 99.5)),
            "gt": render_image_tile(mri_gt, "gray", 0.0, np.percentile(mri_gt, 99.5)),
            "ptm_metric": r"PTM  29.11 dB  ($D_{\mathsf{eff}} = 286$)",
            "base_metric": "vs. RED-diff 28.71 · DAPS 28.61 dB",
            "badge": "#1 training-free PSNR",
        },
        {
            "title": "Acoustic Full Waveform Inversion (FWI)",
            "rec": render_image_tile(fwi_rec, "turbo", fwi_gt.min(), fwi_gt.max()),
            "gt": render_image_tile(fwi_gt, "turbo", fwi_gt.min(), fwi_gt.max()),
            "ptm_metric": r"PTM‡  0.036 Rel. $L_2$  (0.049 noise init)",
            "base_metric": "vs. L-BFGS‡ 0.070 · DAPS‡ 0.201",
            "badge": "1.9× lower error vs. L-BFGS‡",
        },
    ]

    rx_cols = [0.562, 0.782]
    ry_rows = [0.515, 0.075]
    card_w = 0.206
    card_h = 0.365

    for idx, card in enumerate(ib_cards):
        cx = rx_cols[idx % 2]
        cy = ry_rows[idx // 2]

        rect = FancyBboxPatch(
            (cx, cy), card_w, card_h,
            boxstyle="round,pad=0.004,rounding_size=0.014",
            facecolor=CARD_BG, edgecolor=BORDER, lw=0.8,
            transform=fig.transFigure, zorder=1,
        )
        fig.patches.append(rect)

        fig.text(cx + 0.010, cy + card_h - 0.026, card["title"], fontsize=8.2, fontweight="bold", color=INK, va="center", zorder=3)

        im_w = 0.086
        im_h = im_w * (W / H)
        im_y = cy + 0.118
        ax_rec = fig.add_axes([cx + 0.012, im_y, im_w, im_h], zorder=3)
        ax_rec.imshow(card["rec"], interpolation="bilinear")
        ax_rec.set_xticks([]); ax_rec.set_yticks([])
        for s in ax_rec.spines.values():
            s.set_edgecolor(BLUE); s.set_linewidth(1.5)
        fig.text(cx + 0.012 + im_w / 2, im_y + im_h + 0.014, "PTM (Ours)", ha="center", va="center", fontsize=7.3, fontweight="bold", color=BLUE, zorder=4)

        ax_gt = fig.add_axes([cx + card_w - im_w - 0.012, im_y, im_w, im_h], zorder=3)
        ax_gt.imshow(card["gt"], interpolation="bilinear")
        ax_gt.set_xticks([]); ax_gt.set_yticks([])
        for s in ax_gt.spines.values():
            s.set_edgecolor(BORDER); s.set_linewidth(0.8)
        fig.text(cx + card_w - im_w / 2 - 0.012, im_y + im_h + 0.014, "Ground truth", ha="center", va="center", fontsize=7.3, color=MUTED, zorder=4)

        fig.text(cx + 0.010, cy + 0.082, card["ptm_metric"], fontsize=7.9, fontweight="bold", color=BLUE, va="center", zorder=4)
        fig.text(cx + 0.010, cy + 0.050, card["base_metric"], fontsize=7.2, color=MUTED, va="center", zorder=4)
        fig.text(cx + 0.010, cy + 0.018, card["badge"], fontsize=7.4, fontweight="bold", color=TEAL, va="center", zorder=4)

    out_path = OUT_DIR / "benchmark-overview.webp"
    fig.canvas.draw()
    pil_img = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:, :, :3])
    pil_img.save(out_path, "WEBP", quality=94, method=6)
    plt.close(fig)
    print("Saved", out_path, pil_img.size)


def build_home_card(qual_data, ib):
    W, H = 8.6, 6.45
    fig = plt.figure(figsize=(W, H), dpi=200, facecolor=BG)

    # Section a: Image restoration with zoom callouts
    fig.text(0.015, 0.966, "a. Image Restoration with Zoom Callouts", fontsize=10.6, fontweight="bold", color=INK, va="center")
    fig.text(0.985, 0.966, r"#1 PSNR across all 8 FFHQ tasks · 5–8× lower $D_{\mathsf{eff}}$", fontsize=8.5, fontweight="bold", color=BLUE, ha="right", va="center")

    rows_spec = [
        ("imagenet", "phase_retrieval", "Phase\nRetrieval"),
        ("ffhq", "hdr", "HDR\nRestoration"),
    ]
    cols_spec = [
        ("y", "Observation y"),
        ("b1", "Strongest baseline"),
        ("ptm", "PTM (Ours)"),
        ("gt", "Ground truth"),
    ]

    left_x0 = 0.115
    tile_w = 0.202
    tile_h = tile_w * (W / H)
    gap_x = 0.018

    for c_idx, (col_key, col_title) in enumerate(cols_spec):
        xc = left_x0 + c_idx * (tile_w + gap_x) + tile_w / 2
        fig.text(
            xc, 0.922, col_title,
            ha="center", va="center", fontsize=8.8,
            fontweight="bold" if col_key == "ptm" else "normal",
            color=BLUE if col_key == "ptm" else INK,
        )

    row_tops = [0.902, 0.594]
    for r_idx, (ds, task, task_label) in enumerate(rows_spec):
        row = next(r for r in qual_data["rows"] if r["ds"] == ds and r["task"] == task)
        top_y = row_tops[r_idx]
        bot_y = top_y - tile_h
        ymid = (top_y + bot_y) / 2
        fig.text(0.052, ymid, task_label, ha="center", va="center", fontsize=9.0, fontweight="bold", color=INK, linespacing=1.15)

        b1_psnr = row["tiles"]["b1"]["psnr_stored"]
        b2_psnr = row["tiles"]["b2"]["psnr_stored"]
        best_base = row["tiles"]["b1"] if b1_psnr >= b2_psnr else row["tiles"]["b2"]
        best_col = "b1" if b1_psnr >= b2_psnr else "b2"
        ptm_psnr = row["tiles"]["ptm"]["psnr_stored"]
        gain = ptm_psnr - best_base["psnr_stored"]

        for c_idx, (col_key, _) in enumerate(cols_spec):
            actual_col = best_col if col_key == "b1" else col_key
            x0 = left_x0 + c_idx * (tile_w + gap_x)
            ax = fig.add_axes([x0, bot_y, tile_w, tile_h])
            img = np.asarray(Image.open(QUAL_DIR / "tiles" / f"{ds}_{task}_{actual_col}.png"))
            crop = None if (actual_col == "y" and row["abbr"] == "PR") else row["crop"]
            draw_zoom_tile(ax, img, crop, row["inset_corner"], highlight_ptm=(col_key == "ptm"))

            xc = x0 + tile_w / 2
            ytxt = bot_y - 0.021
            if col_key == "b1":
                fig.text(xc, ytxt, f"{best_base['method']}  {best_base['psnr_stored']:.2f} dB", ha="center", va="center", fontsize=8.2, color=INK)
            elif col_key == "ptm":
                fig.text(xc, ytxt, f"{ptm_psnr:.2f} dB (+{gain:.2f} dB)", ha="center", va="center", fontsize=8.5, fontweight="bold", color=BLUE)
            elif col_key == "y":
                note = r"Fourier $\log_{10} |F(x)|$" if row["abbr"] == "PR" else "Clipped dynamic range"
                fig.text(xc, ytxt, note, ha="center", va="center", fontsize=7.8, color=MUTED)
            elif col_key == "gt":
                fig.text(xc, ytxt, "Reference", ha="center", va="center", fontsize=7.8, color=MUTED)

    # Horizontal divider
    fig.lines.append(plt.Line2D([0.015, 0.985], [0.282, 0.282], transform=fig.transFigure, color=BORDER, lw=1.0))

    # Section b: InverseBench Scientific Inverse Problems
    fig.text(0.015, 0.254, "b. Scientific Inverse Problems (InverseBench)", fontsize=10.4, fontweight="bold", color=INK, va="center")
    fig.text(0.985, 0.254, "Blue frame: PTM · Grey: Ground truth · #1 on all 4 tasks", fontsize=8.1, fontweight="bold", color=TEAL, ha="right", va="center")

    bh_rec, bh_gt = ib["bh"]
    scat_rec, scat_gt = ib["scat"]
    mri_rec, mri_gt = ib["mri"]
    fwi_rec, fwi_gt = ib["fwi"]

    ib_strip = [
        (
            "Black Hole (EHT)",
            render_image_tile(bh_rec, "afmhot", 0.0, bh_gt.max()),
            render_image_tile(bh_gt, "afmhot", 0.0, bh_gt.max()),
            "PTM 28.40 dB",
            "+2.33 dB vs. PnP-DM",
        ),
        (
            "Scattering (60 rec.)",
            render_image_tile(scat_rec, "viridis", 0.0, scat_gt.max()),
            render_image_tile(scat_gt, "viridis", 0.0, scat_gt.max()),
            "PTM 33.11 dB",
            "+3.87 dB vs. DDNM",
        ),
        (
            "Knee MRI (4× raw)",
            render_image_tile(mri_rec, "gray", 0.0, np.percentile(mri_gt, 99.5)),
            render_image_tile(mri_gt, "gray", 0.0, np.percentile(mri_gt, 99.5)),
            "PTM 29.11 dB",
            "#1 training-free PSNR",
        ),
        (
            "Full Waveform Inv.",
            render_image_tile(fwi_rec, "turbo", fwi_gt.min(), fwi_gt.max()),
            render_image_tile(fwi_gt, "turbo", fwi_gt.min(), fwi_gt.max()),
            r"PTM‡ 0.036 Rel. $L_2$",
            "1.9× lower vs. L-BFGS‡",
        ),
    ]

    card_w = 0.230
    card_h = 0.218
    gap_c = 0.016
    start_x = 0.015
    base_y = 0.012

    for idx, (title, rec_arr, gt_arr, m_main, m_sub) in enumerate(ib_strip):
        cx = start_x + idx * (card_w + gap_c)
        rect = FancyBboxPatch(
            (cx, base_y), card_w, card_h,
            boxstyle="round,pad=0.003,rounding_size=0.014",
            facecolor=CARD_BG, edgecolor=BORDER, lw=0.8,
            transform=fig.transFigure, zorder=1,
        )
        fig.patches.append(rect)

        xc = cx + card_w / 2
        fig.text(xc, base_y + card_h - 0.020, title, ha="center", va="center", fontsize=8.2, fontweight="bold", color=INK, zorder=4)

        im_w = 0.084
        im_h = im_w * (W / H)
        im_y = base_y + 0.064

        ax_rec = fig.add_axes([cx + 0.020, im_y, im_w, im_h], zorder=3)
        ax_rec.imshow(rec_arr, interpolation="bilinear")
        ax_rec.set_xticks([]); ax_rec.set_yticks([])
        for s in ax_rec.spines.values():
            s.set_edgecolor(BLUE); s.set_linewidth(1.3)

        ax_gt = fig.add_axes([cx + card_w - im_w - 0.020, im_y, im_w, im_h], zorder=3)
        ax_gt.imshow(gt_arr, interpolation="bilinear")
        ax_gt.set_xticks([]); ax_gt.set_yticks([])
        for s in ax_gt.spines.values():
            s.set_edgecolor(BORDER); s.set_linewidth(0.8)

        fig.text(xc, base_y + 0.040, m_main, ha="center", va="center", fontsize=8.2, fontweight="bold", color=BLUE, zorder=4)
        fig.text(xc, base_y + 0.015, m_sub, ha="center", va="center", fontsize=7.4, fontweight="bold", color=TEAL, zorder=4)

    out_path = OUT_DIR / "hero-results.webp"
    fig.canvas.draw()
    pil_img = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:, :, :3])
    pil_img.save(out_path, "WEBP", quality=94, method=6)
    plt.close(fig)
    print("Saved", out_path, pil_img.size)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    qual_data = load_qual_data()
    ib = load_ib_samples()
    build_wide_banner(qual_data, ib)
    build_home_card(qual_data, ib)


if __name__ == "__main__":
    main()
