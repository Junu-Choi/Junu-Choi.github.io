"""Render DeepMind-style PTM Figure 2 (Covariant matching cycle) on #F8F9FA."""
import glob
import os
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, PathPatch, Polygon
from matplotlib.path import Path as MPath

FONT_DIR = os.environ.get("FIGURE_FONT_DIR")  # TeX Gyre Heros .ttf files, if not installed system-wide
for _f in glob.glob(os.path.join(FONT_DIR, "*.ttf")) if FONT_DIR else []:
    font_manager.fontManager.addfont(_f)

OUT_SVG = Path(__file__).resolve().parents[2] / "public" / "figures" / "ptm" / "figure-2.svg"
BG = "#F8F9FA"
BLUE, TEAL, RUST, INK, MUTED = "#1A73E8", "#0D9488", "#E05A33", "#202124", "#5F6368"
HEIGHT, A = 0.355, 0.30

plt.rcParams.update({
    "font.family": "TeX Gyre Heros",
    "font.size": 8.0,
    "mathtext.fontset": "stixsans",
    "pdf.fonttype": 42,
    "svg.fonttype": "path",
    "svg.hashsalt": "ptm-matching-dm3",
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
    "lines.solid_capstyle": "round",
})


def rotation(degrees):
    theta = np.deg2rad(degrees)
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


def target(u):
    t, v = u[..., 0], u[..., 1]
    raw = np.stack((0.70 * t + 1.35 * np.tanh(2 * t), 0.30 * v + 0.21 * np.sin(1.2 * t)), axis=-1)
    return raw @ rotation(12).T


def target_inv(z):
    raw = z @ rotation(12)
    t = raw[..., 0].copy() / 2
    lo, hi = np.full_like(t, -18.0), np.full_like(t, 18.0)
    for _ in range(60):
        t = (lo + hi) / 2
        smaller = 0.70 * t + 1.35 * np.tanh(2 * t) < raw[..., 0]
        lo, hi = np.where(smaller, t, lo), np.where(smaller, hi, t)
    v = (raw[..., 1] - 0.21 * np.sin(1.2 * t)) / 0.30
    return np.stack((t, v), axis=-1)


def target_det(u):
    return 0.30 * (0.70 + 2.70 / np.cosh(2 * u[..., 0]) ** 2)


PARAMS = [
    (0.76, 0.96, 0.58, 0.31, -25),
    (0.85, 0.80, 0.39, 0.27, -17),
    (0.86, 0.74, 0.25, 0.22, -10),
]


def noisy(u, k):
    a, b, gamma, c, angle = PARAMS[k]
    t, v = u[..., 0], u[..., 1]
    return np.stack((a * t, b * np.exp(gamma * np.tanh(t)) * v + c * np.tanh(1.4 * t)), -1) @ rotation(angle).T


def noisy_inv(x, k):
    a, b, gamma, c, angle = PARAMS[k]
    raw = x @ rotation(angle)
    t = raw[..., 0] / a
    v = (raw[..., 1] - c * np.tanh(1.4 * t)) / (b * np.exp(gamma * np.tanh(t)))
    return np.stack((t, v), -1)


def noisy_det(u, k):
    a, b, gamma, _, _ = PARAMS[k]
    return a * b * np.exp(gamma * np.tanh(u[..., 0]))


def gaussian(u, mean, var):
    return np.exp(-0.5 * np.sum((u - mean) ** 2 / var, axis=-1)) / (2 * np.pi * np.sqrt(np.prod(var)))


def xy(center, scale, points):
    return np.asarray(center) + scale * points


def contours(ax, center, scale, forward_inv, jacdet, mean, var, kind):
    limit = 4.2 if kind == "input" else 3.75
    xs = np.linspace(-limit, limit, 261)
    ys = np.linspace(-limit, limit, 261)
    xx, yy = np.meshgrid(xs, ys)
    z = np.stack((xx, yy), -1)
    u = forward_inv(z)
    jac = jacdet(u)
    ref, cur = gaussian(u, np.zeros(2), np.ones(2)) / jac, gaussian(u, mean, var) / jac
    X, Y = center[0] + scale * xx, center[1] + scale * yy
    levels = np.r_[np.array([0.12, 0.28, 0.48, 0.72]) * ref.max(), 1.001 * max(cur.max(), ref.max())]
    ax.contourf(X, Y, cur, levels=levels, colors=["#E4EEFC", "#BDD6FA", "#7CACF8", "#2B7DE9"], zorder=4)
    ax.contour(X, Y, cur, levels=[0.12 * ref.max()], colors=[BLUE], linewidths=0.65, zorder=5)
    ax.contour(X, Y, ref, levels=np.array([0.12, 0.48]) * ref.max(), colors=[INK], linewidths=[0.78, 0.58], linestyles=[(0, (3.2, 2.2))], zorder=6)


def grid(ax, center, scale, k):
    radius = 1.65
    for fixed in np.linspace(-1.35, 1.35, 7):
        bound = np.sqrt(radius**2 - fixed**2)
        t = np.linspace(-bound, bound, 100)
        for u in [np.stack((t, np.full_like(t, fixed)), -1), np.stack((np.full_like(t, fixed), t), -1)]:
            p = xy(center, scale, noisy(u, k))
            ax.plot(p[:, 0], p[:, 1], color=INK, lw=0.45, alpha=0.28, zorder=7)
    if k == 0:
        for t in [-1.0, 0.9]:
            u = np.array([[t - 0.17, -0.17], [t + 0.17, -0.17], [t + 0.17, 0.17], [t - 0.17, 0.17]])
            p = xy(center, scale, noisy(u, k))
            ax.add_patch(Polygon(p, facecolor=RUST, edgecolor=RUST, lw=0.45, alpha=0.65, zorder=8))


def bezier(ax, points, color, lw, alpha=1, arrow=False, zorder=3):
    path = MPath(points, [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4])
    if arrow:
        ax.add_patch(FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=8.5, color=color, lw=lw, alpha=alpha, zorder=zorder))
    else:
        ax.add_patch(PathPatch(path, fill=False, color=color, lw=lw, alpha=alpha, zorder=zorder))


def main():
    fig = plt.figure(figsize=(6.4, 6.4 * HEIGHT), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=BG)
    ax.set(xlim=(0, 1), ylim=(0, HEIGHT), aspect="equal")
    ax.axis("off")
    ncenters = [(0.115, 0.232), (0.440, 0.232), (0.765, 0.232)]
    ccenters = [(0.235, 0.082), (0.560, 0.082), (0.885, 0.082)]
    nscale, cscale = 0.023, 0.024
    m0, v0 = np.array([1.15, -0.28]), np.array([0.29, 0.50])

    for k, (nc, cc) in enumerate(zip(ncenters, ccenters)):
        mean, var = A**k * m0, 1 + A ** (2 * k) * (v0 - 1)
        contours(ax, nc, nscale, lambda x, k=k: noisy_inv(x, k), lambda u, k=k: noisy_det(u, k), mean, var, "input")
        grid(ax, nc, nscale, k)
        contours(ax, cc, cscale, target_inv, target_det, mean, var, "clean")
        for u in [np.array([-1.15, -0.65]), np.array([-1.15, 0.55]), np.array([1.05, -0.65]), np.array([1.05, 0.55])]:
            start, end = xy(nc, nscale, noisy(u, k)), xy(cc, cscale, target(u))
            bezier(ax, [start, start + np.array([0.056, -0.015]), end + np.array([-0.043, 0.032]), end], INK, 0.48, 0.16, zorder=2)
        start, end = np.array(nc) + [0.024, -0.034], np.array(cc) + [-0.018, 0.041]
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=8.5, lw=1.1, color=INK, zorder=9))

    for k in range(2):
        c, n = np.array(ccenters[k]), np.array(ncenters[k + 1])
        start, end = c + [0.051, 0.011], n + [-0.035, 0.031]
        bezier(ax, [start, start + [0.048, 0.023], end + [-0.039, 0.022], end], TEAL, 1.6, arrow=True, zorder=10)
        for shift in [-0.008, 0.008]:
            p = [start + [0, shift], start + [0.048, 0.023 + shift], end + [-0.039, 0.022 + shift], end + [0, shift]]
            bezier(ax, p, TEAL, 0.48, 0.28, zorder=2)

    cell_left = xy(ncenters[0], nscale, noisy(np.array([-1.0, 0.0]), 0))
    cell_right = xy(ncenters[0], nscale, noisy(np.array([0.9, 0.0]), 0))
    ax.plot([0.048, cell_left[0] - 0.005], [0.242, cell_left[1] + 0.003], color=RUST, lw=0.68, zorder=9)
    ax.plot([0.048, cell_right[0] - 0.006], [0.162, cell_right[1] - 0.005], color=RUST, lw=0.68, zorder=9)

    ax.plot([0.018, 0.042], [0.338, 0.338], color=INK, lw=0.85, ls=(0, (3, 2)))
    ax.add_patch(Polygon([[0.236, 0.335], [0.260, 0.335], [0.260, 0.341], [0.236, 0.341]], facecolor="#7CACF8", edgecolor=BLUE, lw=0.45))

    ax.plot([0.280, 0.518], [0.024, 0.024], color=INK, alpha=0.28, lw=0.55)
    ax.plot([0.605, 0.843], [0.024, 0.024], color=INK, alpha=0.28, lw=0.55)
    for x in [0.511, 0.836]:
        ax.plot([x - 0.008, x, x - 0.008], [0.027, 0.024, 0.021], color=INK, alpha=0.48, lw=0.55)

    ax.text(0.048, 0.338, r"Reference law ($q_k, \pi$)", fontsize=7.6, color=INK, va="center")
    ax.text(0.266, 0.338, r"Current law ($p_k, \rho_k$)", fontsize=7.6, color=BLUE, va="center")

    ax.text(0.115, 0.304, r"Input $p_k$ vs. $q_k$", fontsize=7.8, color=INK, ha="center", va="center", fontweight="bold")
    ax.text(0.440, 0.304, r"Rematched $p_{k+1} = q_{k+1}$", fontsize=7.8, color=INK, ha="center", va="center", fontweight="bold")
    ax.text(0.765, 0.304, r"Input $p_{k+2}$", fontsize=7.8, color=INK, ha="center", va="center", fontweight="bold")

    ax.text(0.012, 0.246, "Volume", fontsize=7.3, color=RUST, va="center", fontweight="bold")
    ax.text(0.012, 0.156, "Conditioning", fontsize=7.3, color=RUST, va="center", fontweight="bold")

    ax.text(0.194, 0.165, r"$\Psi_k$", fontsize=8.4, color=INK, va="center")
    ax.text(0.519, 0.165, r"$\Psi_{k+1}$", fontsize=8.4, color=INK, va="center")
    ax.text(0.844, 0.165, r"$\Psi_{k+2}$", fontsize=8.4, color=INK, va="center")

    ax.text(0.334, 0.184, r"Rematching $K_{k+1}$", fontsize=7.4, color=TEAL, ha="center", va="center", fontweight="bold")
    ax.text(0.659, 0.184, r"$K_{k+2}$", fontsize=7.8, color=TEAL, ha="center", va="center", fontweight="bold")

    ax.text(0.235, 0.022, r"Clean $\rho_k$ vs. $\pi$", fontsize=7.6, color=INK, ha="center", va="center")
    ax.text(0.560, 0.022, r"Closer $\rho_{k+1}$", fontsize=7.6, color=INK, ha="center", va="center")
    ax.text(0.885, 0.022, r"Matched $\rho_{k+2} \approx \pi$", fontsize=7.6, color=INK, ha="center", va="center")

    fig.savefig(OUT_SVG, facecolor=BG, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print("Saved", OUT_SVG)


if __name__ == "__main__":
    main()
