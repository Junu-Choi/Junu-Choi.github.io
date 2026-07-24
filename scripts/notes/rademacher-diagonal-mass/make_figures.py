"""Experiments + figures for the note "Rademacher's vanishing advantage".

Regenerates every figure under public/notes/rademacher-diagonal-mass/figures/
and a results.json with the numbers quoted in the note body.

Run from the repo root:  python3 scripts/notes/rademacher-diagonal-mass/make_figures.py
"""

import json
import math
from pathlib import Path

import numpy as np
import torch
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# ───────────────────────────────────────────── display style
# Albergo-style paper display: CM math text, thin spines, no chartjunk,
# transparent background (the site renders figures on its ivory panel).

INK = "#191C1E"
BLUE = "#33567E"   # Rademacher, throughout
RUST = "#C0653B"   # Gaussian, throughout
SAGE = "#5B8266"   # third series
GRAY = "#8C9097"    # guides / references

SITE_CMAP = LinearSegmentedColormap.from_list(
    "site", ["#F5F6F3", "#CBD6DE", "#8AA2B8", "#33567E", "#152740"]
)

mpl.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 9,
    "axes.linewidth": 0.7,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.direction": "out", "ytick.direction": "out",
    "xtick.major.size": 3, "ytick.major.size": 3,
    "xtick.major.width": 0.7, "ytick.major.width": 0.7,
    "xtick.minor.size": 1.8, "ytick.minor.size": 1.8,
    "xtick.minor.width": 0.5, "ytick.minor.width": 0.5,
    "axes.labelsize": 10,
    "legend.frameon": False, "legend.fontsize": 8.5,
    "savefig.dpi": 300, "savefig.bbox": "tight", "savefig.transparent": True,
    "text.color": INK, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK,
})

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
OUT = ROOT / "public/notes/rademacher-diagonal-mass/figures"
OUT.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(0)
torch.manual_seed(0)
torch.set_default_dtype(torch.float64)

results: dict = {}


def rho_of(H: np.ndarray) -> float:
    """Diagonal-mass ratio rho(A) = sum_i A_ii^2 / ||A||_F^2."""
    return float((np.diag(H) ** 2).sum() / (H ** 2).sum())


# ───────────────────────────────────────────── the mixing family
# f_lam(x) = sum_i c_i tanh(h_i),  h = M x,  M = (1-lam) I + lam W.
# Hessian is exact: H = M^T diag(c_i g''(h_i)) M.

D_FAM = 48


def family_hessian(lam: float, seed: int = 0) -> np.ndarray:
    r = np.random.default_rng(seed)
    W = r.normal(size=(D_FAM, D_FAM)) / math.sqrt(D_FAM)
    c = r.normal(size=D_FAM)
    x = r.normal(size=D_FAM)
    M = (1 - lam) * np.eye(D_FAM) + lam * W
    h = M @ x
    t = np.tanh(h)
    g2 = -2 * t * (1 - t ** 2)          # tanh''
    return (M.T * (c * g2)) @ M


def quad_forms(H: np.ndarray, kind: str, n: int, seed: int) -> np.ndarray:
    r = np.random.default_rng(seed)
    d = H.shape[0]
    if kind == "rademacher":
        Z = r.integers(0, 2, size=(n, d)) * 2.0 - 1.0
    else:
        Z = r.normal(size=(n, d))
    return ((Z @ H) * Z).sum(axis=1)


# ── Figure 1: |H| heatmaps at lam = 0, 1/2, 1 ────────────────────────────

lams_show = [0.0, 0.5, 1.0]
fig, axes = plt.subplots(1, 3, figsize=(6.6, 2.25))
for ax, lam in zip(axes, lams_show):
    H = family_hessian(lam, seed=0)
    A = np.abs(H)
    ax.imshow(A, cmap=SITE_CMAP, vmin=0, vmax=np.quantile(A, 0.995),
              interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(True); s.set_linewidth(0.6); s.set_color(GRAY)
    ax.set_xlabel(rf"$\lambda = {lam:g}$", fontsize=10, labelpad=6)
fig.subplots_adjust(wspace=0.08)
fig.savefig(OUT / "hessians.png")
plt.close(fig)

# ── Figure 2: single-probe distributions at lam = 0 and lam = 1 ─────────

N_HIST = 40_000
fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.45))
for ax, lam in zip(axes, [0.0, 1.0]):
    H = family_hessian(lam, seed=0)
    tr = float(np.trace(H))
    qr = quad_forms(H, "rademacher", N_HIST, seed=1)
    qg = quad_forms(H, "gaussian", N_HIST, seed=2)
    lo, hi = np.quantile(qg, [0.001, 0.999])
    pad = 0.05 * (hi - lo)
    bins = np.linspace(lo - pad, hi + pad, 90)
    ax.hist(qg, bins=bins, density=True, histtype="stepfilled",
            color=RUST, alpha=0.28, lw=0)
    ax.hist(qg, bins=bins, density=True, histtype="step", color=RUST, lw=1.1)
    if np.ptp(qr) < 1e-9:
        # exactly diagonal H: the Rademacher estimate is deterministic
        ax.axvline(tr, color=BLUE, lw=2.2)
    else:
        ax.hist(qr, bins=bins, density=True, histtype="stepfilled",
                color=BLUE, alpha=0.32, lw=0)
        ax.hist(qr, bins=bins, density=True, histtype="step", color=BLUE, lw=1.1)
    ax.axvline(tr, color=INK, lw=0.7, ls=(0, (4, 3)))
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel(rf"$\xi^\top\! A_\lambda\, \xi\quad (\lambda = {lam:g})$",
                  fontsize=10)
axes[0].legend(handles=[
    mpl.lines.Line2D([], [], color=BLUE, lw=1.6, label="Rademacher"),
    mpl.lines.Line2D([], [], color=RUST, lw=1.6, label="Gaussian"),
], loc="lower left", bbox_to_anchor=(0.0, 1.0), ncols=2,
   handlelength=1.4, borderaxespad=0.0)
fig.subplots_adjust(wspace=0.1)
fig.savefig(OUT / "probes.png")
plt.close(fig)

# ── Figure 3: the variance identity along the family ─────────────────────

N_VAR = 40_000
SEEDS_FAM = range(8)
lams = np.linspace(0, 1, 21)
theory = np.zeros((len(SEEDS_FAM), len(lams)))
empirical = np.zeros_like(theory)
for i, s in enumerate(SEEDS_FAM):
    for j, lam in enumerate(lams):
        H = family_hessian(float(lam), seed=s)
        theory[i, j] = 1.0 - rho_of(H)
        vr = quad_forms(H, "rademacher", N_VAR, seed=10 + s).var()
        vg = quad_forms(H, "gaussian", N_VAR, seed=60 + s).var()
        empirical[i, j] = vr / vg

fig, ax = plt.subplots(figsize=(6.6, 2.9))
tm, ts = theory.mean(0), theory.std(0)
em, es = empirical.mean(0), empirical.std(0)
ax.fill_between(lams, tm - ts, tm + ts, color=INK, alpha=0.10, lw=0)
ax.plot(lams, tm, color=INK, lw=1.2)
ax.errorbar(lams, em, yerr=es, fmt="o", ms=3.6, color=BLUE,
            elinewidth=0.8, capsize=0, zorder=5)
ax.annotate(r"$1 - \rho(A_\lambda)$", xy=(0.42, float(np.interp(0.42, lams, tm))),
            xytext=(0.52, 0.3), textcoords=ax.transAxes, fontsize=10,
            arrowprops=dict(arrowstyle="-", lw=0.6, color=INK,
                            shrinkA=2, shrinkB=2))
ax.set_xlabel(r"$\lambda$", fontsize=11)
ax.set_ylabel(r"$\mathrm{Var}_{\mathrm{Rad}} / \mathrm{Var}_{\mathrm{Gauss}}$",
              fontsize=10)
ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.03, 1.03)
fig.savefig(OUT / "identity.png")
plt.close(fig)

results["identity_max_abs_dev"] = float(np.abs(empirical - theory).max())

# ───────────────────────────────────────────── rho vs dimension (MLPs)

ACTS = {"tanh": torch.tanh, "gelu": torch.nn.functional.gelu,
        "softplus": torch.nn.functional.softplus}
DIMS = [8, 16, 32, 64, 128, 256, 512]
WIDTH = 256
N_SEEDS = 8


def mlp_hessian(act, d: int, seed: int) -> np.ndarray:
    g = torch.Generator().manual_seed(seed)

    def lin(i, o):
        w = torch.empty(o, i); b = torch.empty(o)
        bound = 1 / math.sqrt(i)
        w.uniform_(-bound, bound, generator=g)
        b.uniform_(-bound, bound, generator=g)
        return w, b

    W1, b1 = lin(d, WIDTH); W2, b2 = lin(WIDTH, WIDTH); W3, b3 = lin(WIDTH, 1)

    def f(x):
        h = act(x @ W1.T + b1)
        h = act(h @ W2.T + b2)
        return (h @ W3.T + b3).squeeze()

    x = torch.randn(d, generator=g)
    H = torch.autograd.functional.hessian(f, x)
    return H.numpy()


rho_dim = {name: np.zeros((N_SEEDS, len(DIMS))) for name in ACTS}
for name, act in ACTS.items():
    for j, d in enumerate(DIMS):
        for s in range(N_SEEDS):
            rho_dim[name][s, j] = rho_of(mlp_hessian(act, d, seed=1000 * j + s))

# fit the log-log slope per activation (all seeds pooled)
slopes = {}
for name in ACTS:
    X = np.log(np.repeat(DIMS, N_SEEDS)).astype(float)
    Y = np.log(rho_dim[name].T.ravel())
    slopes[name] = float(np.polyfit(X, Y, 1)[0])
results["rho_vs_d_slopes"] = slopes
results["rho_at_d512"] = {n: float(rho_dim[n][:, -1].mean()) for n in ACTS}
results["rho_at_d8"] = {n: float(rho_dim[n][:, 0].mean()) for n in ACTS}

# ───────────────────────────────────────────── rho along training

D_TRAIN, STEPS, EVAL_EVERY, BATCH = 64, 6000, 200, 256
N_TEST_PTS = 6


class Net(torch.nn.Module):
    def __init__(self, d, seed):
        super().__init__()
        torch.manual_seed(seed)
        self.l1 = torch.nn.Linear(d, WIDTH)
        self.l2 = torch.nn.Linear(WIDTH, WIDTH)
        self.l3 = torch.nn.Linear(WIDTH, 1)

    def forward(self, x):
        h = torch.tanh(self.l1(x))
        h = torch.tanh(self.l2(h))
        return self.l3(h).squeeze(-1)


def rho_now(net, xs) -> float:
    vals = []
    for x in xs:
        H = torch.autograd.functional.hessian(lambda z: net(z), x)
        vals.append(rho_of(H.detach().numpy()))
    return float(np.mean(vals))


teacher = Net(D_TRAIN, seed=7)
for p in teacher.parameters():
    p.requires_grad_(False)

TARGETS = {
    "generic": lambda x: teacher(x),
    "separable": lambda x: torch.sin(1.5 * x).sum(-1) / math.sqrt(D_TRAIN),
}

test_pts = [torch.randn(D_TRAIN, generator=torch.Generator().manual_seed(500 + i))
            for i in range(N_TEST_PTS)]

train_curves = {}
final_losses = {}
for tag, target in TARGETS.items():
    net = Net(D_TRAIN, seed=3)
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    g = torch.Generator().manual_seed(11)
    steps_log, rho_log = [0], [rho_now(net, test_pts)]
    for step in range(1, STEPS + 1):
        x = torch.randn(BATCH, D_TRAIN, generator=g)
        loss = ((net(x) - target(x)) ** 2).mean()
        opt.zero_grad(); loss.backward(); opt.step()
        if step % EVAL_EVERY == 0:
            steps_log.append(step); rho_log.append(rho_now(net, test_pts))
    train_curves[tag] = (steps_log, rho_log)
    with torch.no_grad():
        xe = torch.randn(8192, D_TRAIN, generator=torch.Generator().manual_seed(99))
        ye = target(xe)
        final_losses[tag] = {
            "mse": float(((net(xe) - ye) ** 2).mean()),
            "r2": float(1 - ((net(xe) - ye) ** 2).mean() / ye.var()),
        }

results["training_final_rho"] = {t: c[1][-1] for t, c in train_curves.items()}
results["training_init_rho"] = {t: c[1][0] for t, c in train_curves.items()}
results["training_fit"] = final_losses

# ── Figure 4: scaling with d (left) and along training (right) ──────────

fig, (axL, axR) = plt.subplots(1, 2, figsize=(6.6, 2.7))

colors = {"tanh": BLUE, "gelu": RUST, "softplus": SAGE}
for name in ACTS:
    m = rho_dim[name].mean(0)
    axL.plot(DIMS, m, "-o", ms=3.4, lw=1.1, color=colors[name], label=name)
    for s in range(N_SEEDS):
        axL.plot(DIMS, rho_dim[name][s], "o", ms=1.6, color=colors[name],
                 alpha=0.25, zorder=1)
ref = rho_dim["tanh"].mean(0)[0] * DIMS[0] / np.asarray(DIMS, float)
axL.plot(DIMS, ref, ls=(0, (4, 3)), lw=0.9, color=GRAY, zorder=0)
axL.text(DIMS[-2], ref[-2] * 1.45, r"$\propto 1/d$", color=GRAY, fontsize=9)
axL.set_xscale("log", base=2); axL.set_yscale("log")
axL.set_xlabel(r"input dimension $d$", fontsize=10)
axL.set_ylabel(r"$\rho(\nabla^2 f)$", fontsize=10)
axL.set_xticks(DIMS, [str(d) for d in DIMS])
axL.legend(loc="lower left", handlelength=1.6)

for tag, color in [("separable", BLUE), ("generic", RUST)]:
    steps_log, rho_log = train_curves[tag]
    axR.plot(steps_log, rho_log, "-", lw=1.2, color=color, label=tag)
axR.axhline(rho_dim["tanh"].mean(0)[DIMS.index(D_TRAIN)],
            ls=(0, (4, 3)), lw=0.9, color=GRAY)
axR.text(0.98, rho_dim["tanh"].mean(0)[DIMS.index(D_TRAIN)] * 1.35,
         r"init, $d = 64$", color=GRAY, fontsize=8.5,
         ha="right", transform=axR.get_yaxis_transform())
axR.set_yscale("log")
axR.set_xlabel("training step", fontsize=10)
axR.set_ylabel(r"$\rho(\nabla^2 f)$", fontsize=10)
axR.legend(loc="upper right", bbox_to_anchor=(0.98, 0.78), handlelength=1.6)

fig.subplots_adjust(wspace=0.38)
fig.savefig(OUT / "scaling.png")
plt.close(fig)

(OUT / "results.json").write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
