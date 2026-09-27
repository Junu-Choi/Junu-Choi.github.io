"""Render analytic illustrations for the PTM publication preview (CPU only).

Requirements: numpy, matplotlib, Pillow. Run from any directory with Python.
The endpoint map and mixture parameters follow the manuscript's geometric
illustrations. These are analytic examples, not fitted maps or experiment data.
Conditioning changes a Gaussian denoising kernel; the convolved density is NOT
a posterior heat marginal. No manuscript files are read or modified.
"""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
import numpy as np
from PIL import Image

OUT = Path(__file__).resolve().parents[2] / "public" / "figures" / "ptm"
BG, INK, MUTED = "#f6f6f7", "#30363e", "#596974"
BLUE, TEAL, RUST = "#2878b5", "#238a83", "#c16a43"
TEAL_TEXT, RUST_TEXT = "#196d67", "#99512f"
COLORS = ["#e3eef7", "#b5d1e6", "#75a9cd", "#347fb3"]
CELLS = [(-1.0, -0.6, -0.2, 0.2), (0.6, 1.0, -0.2, 0.2)]
MEANS = np.array([[-1.65, -1.05], [-0.15, 1.6], [1.65, -0.75]])
WEIGHTS = np.array([0.32, 0.36, 0.32])
BASE_COV = np.array([[0.08, 0.025], [0.025, 0.05]])
A = np.array([[np.cos(np.pi / 6), np.sin(np.pi / 6)]])
TAU, R = 0.8, 0.08
GRID = np.linspace(-7, 7, 501)
XX, YY = np.meshgrid(GRID, GRID)
POINTS = np.stack([XX, YY], axis=-1)
DX = GRID[1] - GRID[0]
MASSES = np.array([0.9, 0.75, 0.5, 0.25])
STEPS = (1 - np.cos(np.linspace(0, np.pi, 49))) / 2

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10,
    "text.color": INK, "figure.facecolor": BG, "axes.facecolor": BG,
    "lines.solid_joinstyle": "round", "mathtext.fontset": "dejavusans",
})


def boundary(cell):
    x0, x1, y0, y1 = cell
    t = np.linspace(0, 1, 121)
    return np.concatenate([
        np.column_stack((x0 + (x1 - x0) * t, np.full_like(t, y0))),
        np.column_stack((np.full_like(t, x1), y0 + (y1 - y0) * t)),
        np.column_stack((x1 - (x1 - x0) * t, np.full_like(t, y1))),
        np.column_stack((np.full_like(t, x0), y1 - (y1 - y0) * t)),
    ])


def transform(points, s):
    result = points.copy()
    result[:, 1] *= 0.8**s * np.exp(0.65 * s * result[:, 0])
    return result


def area_ratio(cell, s):
    x0, x1, _, _ = cell
    rate = 0.65 * s
    if s == 0:
        return 1.0
    return 0.8**s * np.exp(rate * x0) * np.expm1(rate * (x1 - x0)) / (rate * (x1 - x0))


def frame_base(label, s):
    fig = plt.figure(figsize=(5, 3.6), dpi=128)
    fig.text(0.06, 0.935, label, color=MUTED, fontsize=11)
    fig.text(0.94, 0.935, f"{s:.2f}", ha="right", family="DejaVu Sans Mono", fontsize=11)
    fig.lines.extend([
        plt.Line2D([0.06, 0.94], [0.89, 0.89], transform=fig.transFigure, color="#dce2e6", lw=1.3),
        plt.Line2D([0.06, 0.06 + 0.88 * s], [0.89, 0.89], transform=fig.transFigure, color=BLUE, lw=1.3),
    ])
    return fig


def image_from_figure(fig):
    fig.canvas.draw()
    result = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy())
    plt.close(fig)
    return result


def volume_frame(s):
    fig = frame_base("Deformation  s", s)
    for x, value, title in [(0.035, 0.0, "Source"), (0.535, s, "Mapped")]:
        ax = fig.add_axes([x, 0.16, 0.43, 0.64])
        ax.add_patch(Polygon(transform(boundary((-1, 1, -1, 1)), value), facecolor=BLUE, alpha=0.10, edgecolor="none"))
        for cell, color, name in zip(CELLS, [TEAL, RUST], ["A", "B"]):
            ax.add_patch(Polygon(transform(boundary(cell), value), facecolor=color, alpha=0.70, edgecolor="none"))
            center = transform(np.array([[(cell[0] + cell[1]) / 2, 0.0]]), value)[0]
            ax.text(center[0], center[1] - 0.39, name, ha="center", va="top", color=TEAL_TEXT if name == "A" else RUST_TEXT, fontsize=11)
        t = np.linspace(-1, 1, 161)
        for edge in np.linspace(-1, 1, 6):
            for line in [np.column_stack((t, t * 0 + edge)), np.column_stack((t * 0 + edge, t))]:
                mapped = transform(line, value)
                ax.plot(*mapped.T, color=INK, lw=0.65, alpha=0.57)
        ax.set(xlim=(-1.55, 1.55), ylim=(-1.7, 1.7), aspect="equal")
        ax.axis("off")
        fig.text(x + 0.215, 0.80, title, ha="center", fontsize=11, color=MUTED)
    fig.text(0.5, 0.48, "→", ha="center", fontsize=18, color=MUTED)
    fig.text(0.06, 0.11, "AREA / SOURCE AREA", fontsize=9.5, color=MUTED)
    fig.text(0.06, 0.04, f"A  × {area_ratio(CELLS[0], s):.2f}", color=TEAL_TEXT, fontsize=13.5)
    fig.text(0.56, 0.04, f"B  × {area_ratio(CELLS[1], s):.2f}", color=RUST_TEXT, fontsize=13.5)
    return image_from_figure(fig)


def covariance(s):
    return np.linalg.inv(np.eye(2) / TAU + s * A.T @ A / R)


def density(cov):
    total_cov = BASE_COV + cov
    inv = np.linalg.inv(total_cov)
    result = np.zeros_like(XX)
    for mean, weight in zip(MEANS, WEIGHTS):
        delta = POINTS - mean
        quadratic = np.einsum("...i,ij,...j->...", delta, inv, delta)
        result += weight * np.exp(-quadratic / 2)
    return result / (2 * np.pi * np.sqrt(np.linalg.det(total_cov)))


def conditioning_frame(s):
    fig = frame_base("Observation strength  λ", s)
    ax = fig.add_axes([0.07, 0.155, 0.86, 0.69])
    cov = covariance(s)
    pdf = density(cov)
    sorted_pdf = np.sort(pdf.ravel())[::-1]
    cumulative = np.cumsum(sorted_pdf) * DX**2
    levels = sorted_pdf[np.searchsorted(cumulative, MASSES)]
    assert cumulative[-1] > 0.99999
    # All displayed 90% contours must fit the visible axes, not just the grid.
    inside = (np.abs(XX) <= 4.5) & (np.abs(YY) <= 3.5)
    assert np.max(pdf[~inside]) < levels[0]
    ax.contourf(XX, YY, pdf, levels=[*levels, pdf.max() * 1.01], colors=COLORS)
    ax.contour(XX, YY, pdf, levels=levels[1:], colors=BLUE, linewidths=0.45, alpha=0.65)
    ax.contour(XX, YY, pdf, levels=[levels[0]], colors=INK, linewidths=0.65, linestyles=[(0, (4, 3))])
    ax.add_patch(Ellipse((0, 0), 2 * np.sqrt(TAU), 2 * np.sqrt(TAU), fill=False, edgecolor=MUTED, alpha=0.5, lw=0.8, linestyle=(0, (2, 3))))
    eig, rotation = np.linalg.eigh(cov)
    angle = np.degrees(np.arctan2(rotation[1, -1], rotation[0, -1]))
    ax.add_patch(Ellipse((0, 0), 2 * np.sqrt(eig[-1]), 2 * np.sqrt(eig[0]), angle=angle, fill=False, edgecolor=RUST, lw=1.7))
    ax.set(xlim=(-4.5, 4.5), ylim=(-3.5, 3.5), aspect="equal")
    ax.axis("off")
    fig.text(0.06, 0.11, "KERNEL VARIANCE", fontsize=9.5, color=MUTED)
    fig.text(0.06, 0.04, f"Observed  {eig[0]:.3f}", color=RUST_TEXT, fontsize=11.5)
    fig.text(0.56, 0.04, f"Unobserved  {eig[1]:.3f}", color=MUTED, fontsize=11.5)
    return image_from_figure(fig), float(cumulative[-1])


def save_animation(name, frames):
    # A shared, undithered palette avoids flicker in the background and contours.
    sample = Image.new("RGB", (128 * len(frames), 92), BG)
    for index, frame in enumerate(frames):
        sample.paste(frame.resize((128, 92)), (128 * index, 0))
    palette = sample.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    cycle = indexed + indexed[-2:0:-1]
    durations = [80] * len(cycle)
    durations[0], durations[len(frames) - 1] = 1000, 1600
    cycle[0].save(OUT / f"{name}.gif", save_all=True, append_images=cycle[1:], duration=durations, loop=0, optimize=False, disposal=1)
    frames[-1].save(OUT / f"{name}-still.png", optimize=True)
    return {"width": frames[0].width, "height": frames[0].height, "frames": len(cycle), "duration_ms": sum(durations)}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    volumes, conditions, masses = [], [], []
    max_area_error = 0.0
    for s in STEPS:
        assert np.min(0.8**s * np.exp(0.65 * s * GRID)) > 0
        for cell in CELLS:
            polygon = transform(boundary(cell), s)
            x, y = polygon.T
            polygon_area = abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))) / 2
            exact = (cell[1] - cell[0]) * (cell[3] - cell[2]) * area_ratio(cell, s)
            error = abs(polygon_area / exact - 1)
            assert error < 1e-6
            max_area_error = max(max_area_error, error)
        expected = [TAU / (1 + s * TAU / R), TAU]
        np.testing.assert_allclose(np.linalg.eigvalsh(covariance(s)), expected, rtol=1e-12)
        volumes.append(volume_frame(s))
        frame, mass = conditioning_frame(s)
        conditions.append(frame)
        masses.append(mass)
    diagnostics = {
        "kind": "Analytic illustration, not experimental evidence or posterior heat marginals",
        "volume_map": "F_s(u,v) = (u, 0.8^s exp(0.65 s u) v)",
        "jacobian_determinant": "0.8^s exp(0.65 s u) > 0",
        "source_cells": CELLS,
        "endpoint_area_ratios": [area_ratio(cell, 1) for cell in CELLS],
        "maximum_relative_area_check_error": max_area_error,
        "kernel_covariance": "C_lambda = (I / tau + lambda A^T A / R)^(-1)",
        "tau": TAU, "R": R, "A": A.tolist(),
        "mixture_means": MEANS.tolist(), "mixture_weights": WEIGHTS.tolist(),
        "mixture_component_covariance": BASE_COV.tolist(),
        "density": "p0 convolved with N(0, C_lambda)",
        "contour_enclosed_masses": MASSES.tolist(),
        "minimum_grid_mass": min(masses),
        "visible_contours_checked": True,
        "endpoint_kernel_eigenvalues": np.linalg.eigvalsh(covariance(1)).tolist(),
        "animations": {
            "volume": save_animation("volume", volumes),
            "conditioning": save_animation("conditioning", conditions),
        },
    }
    (OUT / "geometry.json").write_text(json.dumps(diagnostics, indent=2) + "\n")
    print(json.dumps(diagnostics, indent=2))


if __name__ == "__main__":
    main()
