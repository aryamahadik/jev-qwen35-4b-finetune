"""Step 4: the paper's three ways to find the compute-optimal model size, applied to our runs.

  Approach 1  minimum over training curves        (paper Section 3.1, Figure 2)
  Approach 2  IsoFLOP profiles                     (paper Section 3.2, Figure 3)
  Approach 3  fit L(N, D) = E + A/N^alpha + B/D^beta (paper Section 3.3, Figure 4)

Each approach gives exponents a, b in  N_opt ~ C^a  and  D_opt ~ C^b  (paper Table 2).
Writes figures/*.png and results.json (the numbers the HTML demo and the slides use).
"""
import glob
import json
import os

import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp

from flops import train_flops_per_token
from sweep import LADDER, TRY_SMALLER_BELOW, size
from train import CTX, VOCAB, heads

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
V = len(VOCAB)
RNG = np.random.default_rng(0)

PAPER = {  # numbers quoted from the paper
    "a": {"approach1": 0.50, "approach2": 0.49, "approach3": 0.46, "kaplan": 0.73},
    "b": {"approach1": 0.50, "approach2": 0.51, "approach3": 0.54, "kaplan": 0.27},
    "fit": {"E": 1.69, "A": 406.4, "B": 410.7, "alpha": 0.34, "beta": 0.28},
}


def load(stage):
    runs = [json.load(open(p)) for p in glob.glob(os.path.join(HERE, "runs", "*.json"))]
    return sorted((r for r in runs if r.get("stage") == stage), key=lambda r: (r.get("budget") or 0, r["params"]))


def load_iso():
    """The IsoFLOP grid: for each (budget, model) keep the run with the best batch size (lowest loss)."""
    best = {}
    for r in load("isoflop"):
        k = (r["budget"], r["n_layer"], r["d_model"])
        if k not in best or r["val_loss"] < best[k]["val_loss"]:
            best[k] = r
    return sorted(best.values(), key=lambda r: (r["budget"], r["params"]))


# FLOPs per token for any parameter count, interpolated along our model family (log-log).
# Smooth fit over our model family: FLOPs per token = 6N (1 + k N^-g); attention adds most for small models.
_N = np.array([size(L, d) for L, d in LADDER], dtype=float)
_R = np.array([train_flops_per_token(L, d, heads(d), CTX, V) for L, d in LADDER]) / (6 * _N)
_G, _LK = np.polyfit(np.log(_N), np.log(_R - 1), 1)
FPT_K, FPT_G = float(np.exp(_LK)), float(-_G)


def fpt(N):
    N = np.asarray(N, dtype=float)
    return 6 * N * (1 + FPT_K * N ** -FPT_G)


def power_law(C, y):
    """Least-squares line in log-log space: y = k * C^slope. Returns (slope, k)."""
    slope, icpt = np.polyfit(np.log10(C), np.log10(y), 1)
    return float(slope), float(10**icpt)


def bootstrap(runs, fn, n=100, frac=0.8):
    """The paper's error bars: refit on 80% of the runs, 100 times; report 10th/90th percentiles."""
    vals = []
    for _ in range(n):
        pick = RNG.choice(len(runs), size=int(frac * len(runs)), replace=False)
        try:
            vals.append(fn([runs[i] for i in pick]))
        except (ValueError, np.linalg.LinAlgError, FloatingPointError):
            pass
    vals = np.array(vals)
    return [[float(np.percentile(vals[:, j], 10)), float(np.percentile(vals[:, j], 90))] for j in range(vals.shape[1])]


# ---------------------------------------------------------------- Approach 2: IsoFLOP profiles
def isoflop_fits(runs):
    """For every budget: fit a parabola to loss vs log(N) and take its lowest point."""
    out = []
    for C in sorted({r["budget"] for r in runs}):
        pts = [r for r in runs if r["budget"] == C]
        if len(pts) < 3:
            raise ValueError("need 3 points for a parabola")
        x = np.log10([r["params"] for r in pts])
        y = np.array([r["val_loss"] for r in pts])
        p2, p1, p0 = np.polyfit(x, y, 2)
        if p2 <= 0:
            raise ValueError("no minimum")
        xm = -p1 / (2 * p2)
        N = 10**xm
        out.append(dict(budget=C, coef=[p2, p1, p0], N_opt=N, D_opt=C / float(fpt(N)),
                        loss_opt=p0 - p1**2 / (4 * p2), inside=bool(x.min() <= xm <= x.max())))
    return out


def approach2(runs):
    fits = isoflop_fits(runs)
    C = np.array([f["budget"] for f in fits])
    a, ka = power_law(C, [f["N_opt"] for f in fits])
    b, kb = power_law(C, [f["D_opt"] for f in fits])

    def exps(sample):
        f = isoflop_fits(sample)
        c = [g["budget"] for g in f]
        return power_law(c, [g["N_opt"] for g in f])[0], power_law(c, [g["D_opt"] for g in f])[0]

    ci = bootstrap(runs, exps)
    return dict(per_budget=fits, a=a, kN=ka, b=b, kD=kb, a_ci=ci[0], b_ci=ci[1])


# ------------------------------------------------------- Approach 1: minimum over training curves
def envelope(runs, grid):
    """For every FLOP count, which run has the lowest (smoothed) training loss right there?"""
    best_loss = np.full(len(grid), np.inf)
    best_N = np.full(len(grid), np.nan)
    for r in runs:
        c = np.array(r["curve"])
        f, loss = c[:, 1], c[:, 2]
        loss = np.convolve(np.pad(loss, 2, mode="edge"), np.ones(5) / 5, mode="valid")  # smooth
        ok = (grid >= f[0]) & (grid <= f[-1])
        li = np.interp(np.log(grid[ok]), np.log(f), loss)
        better = li < best_loss[ok]
        idx = np.where(ok)[0][better]
        best_loss[idx], best_N[idx] = li[better], r["params"]
    return best_loss, best_N


def approach1(runs):
    budgets = sorted({r["budget"] for r in runs})
    grid = np.logspace(np.log10(budgets[0]), np.log10(budgets[-1]), 60)

    def fit(sample):
        loss, N = envelope(sample, grid)
        return power_law(grid, N)[0], power_law(grid, grid / fpt(N))[0]

    loss, N = envelope(runs, grid)
    a, ka = power_law(grid, N)
    b, kb = power_law(grid, grid / fpt(N))
    ci = bootstrap(runs, fit)
    return dict(grid=grid.tolist(), env_loss=loss.tolist(), env_N=N.tolist(),
                a=a, kN=ka, b=b, kD=kb, a_ci=ci[0], b_ci=ci[1])


# ------------------------------------------------------------ Approach 3: parametric loss fit
def _objective(theta, lN, lD, lL, delta=1e-3):
    """Huber loss between predicted and observed log-loss, with its gradient (paper Eq. 3)."""
    a, b, e, alpha, beta = theta
    t = np.stack([a - alpha * lN, b - beta * lD, np.full_like(lN, e)])
    pred = logsumexp(t, axis=0)  # log(A/N^alpha + B/D^beta + E), with A=e^a, B=e^b, E=e^e
    r = pred - lL
    small = np.abs(r) <= delta
    loss = np.where(small, 0.5 * r**2, delta * (np.abs(r) - 0.5 * delta)).sum()
    g = np.where(small, r, delta * np.sign(r))
    w = np.exp(t - pred)  # softmax weights of the three terms
    grad = np.array([(g * w[0]).sum(), (g * w[1]).sum(), (g * w[2]).sum(),
                     (g * -w[0] * lN).sum(), (g * -w[1] * lD).sum()])
    return loss, grad


def fit_parametric(runs, inits=None):
    lN = np.log([r["params"] for r in runs])
    lD = np.log([r["tokens"] for r in runs])
    lL = np.log([r["val_loss"] for r in runs])
    if inits is None:  # the paper's initialisation grid (Appendix D.2)
        inits = [(a, b, e, al, be) for al in np.arange(0, 2.01, 0.5) for be in np.arange(0, 2.01, 0.5)
                 for e in np.arange(-1, 1.01, 0.5) for a in range(0, 26, 5) for b in range(0, 26, 5)]
    best = None
    for x0 in inits:
        res = minimize(_objective, x0, args=(lN, lD, lL), jac=True, method="L-BFGS-B")
        if best is None or res.fun < best.fun:
            best = res
    a, b, e, alpha, beta = best.x
    return dict(E=float(np.exp(e)), A=float(np.exp(a)), B=float(np.exp(b)), alpha=float(alpha),
                beta=float(beta), a=float(beta / (alpha + beta)), b=float(alpha / (alpha + beta)),
                theta=best.x.tolist(), huber=float(best.fun))


def predict(fit, N, D):
    return fit["E"] + fit["A"] / np.power(N, fit["alpha"]) + fit["B"] / np.power(D, fit["beta"])


def approach3(runs):
    fit = fit_parametric(runs)
    warm = [fit["theta"]] + [list(np.array(fit["theta"]) + RNG.normal(0, 0.5, 5)) for _ in range(4)]
    ci = bootstrap(runs, lambda s: (lambda f: (f["a"], f["b"]))(fit_parametric(s, warm)))
    G = (fit["alpha"] * fit["A"] / (fit["beta"] * fit["B"])) ** (1 / (fit["alpha"] + fit["beta"]))
    pred = predict(fit, np.array([r["params"] for r in runs]), np.array([r["tokens"] for r in runs]))
    rel = np.abs(pred / np.array([r["val_loss"] for r in runs]) - 1)
    return dict(fit, G=G, a_ci=ci[0], b_ci=ci[1], mean_abs_err=float(rel.mean()))


def frontier_numeric(fit, C):
    """Best N for each budget C, minimising the fitted loss along our exact-FLOP isoFLOP line."""
    Ns = np.logspace(3.5, 8, 2000)
    return np.array([Ns[np.argmin(predict(fit, Ns, c / fpt(Ns)))] for c in np.atleast_1d(C)])


# ------------------------------------------------------------------------------------ figures
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

INK, MUTED, GRID = "#1b2230", "#5d6678", "#e4e7ee"
OURS, PAPERC, KAPLAN = "#e8590c", "#3b5bdb", "#8a919e"
RAMP = LinearSegmentedColormap.from_list("budget", ["#63c5b5", "#2f8fb0", "#3653a6", "#4a2a86"])
SIZE_RAMP = LinearSegmentedColormap.from_list("size", ["#f3b562", "#e8590c", "#a5264a", "#4a2a86"])


def style():
    for f in glob.glob(os.path.join(HERE, "assets", "fonts", "*.ttf")):
        font_manager.fontManager.addfont(f)
    plt.rcParams.update({
        "font.family": "IBM Plex Sans", "font.size": 10.5, "axes.titlesize": 12, "axes.titleweight": "semibold",
        "axes.titlelocation": "left", "axes.titlepad": 10, "axes.labelsize": 10.5, "axes.labelcolor": INK,
        "axes.edgecolor": "#b9bfcc", "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK,
        "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID,
        "grid.linewidth": 0.7, "axes.axisbelow": True, "legend.frameon": False, "legend.fontsize": 9.5,
        "savefig.dpi": 200, "savefig.bbox": "tight", "savefig.facecolor": "white", "mathtext.fontset": "dejavusans",
    })


def budget_colors(budgets):
    return {C: RAMP(i / max(1, len(budgets) - 1)) for i, C in enumerate(sorted(budgets))}


def sci(x, digits=1):
    """3.16e13 -> '3.2×10¹³' for labels."""
    e = int(np.floor(np.log10(x)))
    m = x / 10**e
    sup = str(e).translate(str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹"))
    return f"10{sup}" if abs(m - 1) < 0.05 else f"{m:.{digits}f}×10{sup}"


def human(n):
    """29216 -> '29K', 1.56e6 -> '1.6M', 2.8e11 -> '280B'."""
    for unit, v in (("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if n >= v:
            return f"{n / v:.0f}{unit}" if n / v >= 10 else f"{n / v:.1f}{unit}"
    return f"{n:.0f}"


def nice_log(ax, which="x", fmt=None):
    """Label a log axis at 1-2-5 steps (e.g. 20K, 50K, 100K) instead of only at powers of ten."""
    from matplotlib.ticker import FixedLocator, FuncFormatter, NullFormatter
    axis = ax.xaxis if which == "x" else ax.yaxis
    lo, hi = ax.get_xlim() if which == "x" else ax.get_ylim()
    ticks = [m * 10**e for e in range(int(np.floor(np.log10(lo))) - 1, int(np.ceil(np.log10(hi))) + 1)
             for m in (1, 2, 5) if lo <= m * 10**e <= hi]
    if len(ticks) >= 2:
        axis.set_major_locator(FixedLocator(ticks))
        axis.set_major_formatter(FuncFormatter(lambda v, _: (fmt or human)(v)))
        axis.set_minor_formatter(NullFormatter())


def ref_line(ax, x, y_at, x0, slope, **kw):
    """A reference power law with the given slope through the point (x0, y_at)."""
    ax.plot(x, y_at * (np.asarray(x) / x0) ** slope, **kw)


def save(fig, name):
    os.makedirs(FIG, exist_ok=True)
    fig.savefig(os.path.join(FIG, name))
    plt.close(fig)


def fig_isoflop(runs, a2):
    budgets = sorted({r["budget"] for r in runs})
    col = budget_colors(budgets)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.1), gridspec_kw={"width_ratios": [1.45, 1, 1]})
    ax = axes[0]
    for f in a2["per_budget"]:
        pts = [r for r in runs if r["budget"] == f["budget"]]
        x = np.log10([r["params"] for r in pts])
        xs = np.linspace(x.min() - 0.08, x.max() + 0.08, 100)
        ax.plot(10**xs, np.polyval(f["coef"], xs), color=col[f["budget"]], lw=1.8, alpha=0.9)
        ax.scatter([r["params"] for r in pts], [r["val_loss"] for r in pts], s=26, color=col[f["budget"]],
                   edgecolor="white", linewidth=0.6, zorder=3, label=f"{sci(f['budget'])} FLOPs")
        ax.scatter([f["N_opt"]], [f["loss_opt"]], marker="*", s=190, color=col[f["budget"]],
                   edgecolor=INK, linewidth=0.8, zorder=4)
    ax.set_xscale("log")
    nice_log(ax, "x")
    ax.set_xlabel("Parameters N")
    ax.set_ylabel("Validation loss (nats per character)")
    ax.set_title("IsoFLOP curves: same compute, different model sizes")
    ax.legend(loc="upper right", title="compute budget", title_fontsize=9)
    C = np.array([f["budget"] for f in a2["per_budget"]])
    cx = np.logspace(np.log10(C.min()) - 0.25, np.log10(C.max()) + 0.25, 50)
    for ax, key, k, e, pe, ke, label in [
            (axes[1], "N_opt", a2["kN"], a2["a"], PAPER["a"]["approach2"], PAPER["a"]["kaplan"], "Optimal parameters N"),
            (axes[2], "D_opt", a2["kD"], a2["b"], PAPER["b"]["approach2"], PAPER["b"]["kaplan"], "Optimal training tokens D")]:
        y = np.array([f[key] for f in a2["per_budget"]])
        mid = np.exp(np.mean(np.log(C)))
        ymid = k * mid**e
        ref_line(ax, cx, ymid, mid, ke, color=KAPLAN, ls="--", lw=1.4, label=f"Kaplan slope {ke}")
        ax.plot(cx, k * cx**e, color=OURS, lw=2.2, label=f"our fit: slope {e:.2f}")
        ax.scatter(C, y, s=110, marker="*", color=[col[c] for c in C], edgecolor=INK, linewidth=0.8, zorder=3)
        ax.set_xscale("log")
        ax.set_yscale("log")
        nice_log(ax, "y")
        ax.set_xlabel("Compute C (FLOPs)")
        ax.set_title(label)
        ax.legend(loc="upper left")
        ax.text(0.97, 0.05, f"paper: {pe}", transform=ax.transAxes, ha="right", color=PAPERC, fontsize=10)
    save(fig, "fig_isoflop.png")


def fig_iso_parts(runs, a2):
    """The same content as fig_isoflop.png, as two bigger figures for slides."""
    budgets = sorted({r["budget"] for r in runs})
    col = budget_colors(budgets)
    fig, ax = plt.subplots(figsize=(8.6, 4.9))
    for f in a2["per_budget"]:
        pts = [r for r in runs if r["budget"] == f["budget"]]
        x = np.log10([r["params"] for r in pts])
        xs = np.linspace(x.min() - 0.08, x.max() + 0.08, 100)
        ax.plot(10**xs, np.polyval(f["coef"], xs), color=col[f["budget"]], lw=2)
        ax.scatter([r["params"] for r in pts], [r["val_loss"] for r in pts], s=34, color=col[f["budget"]],
                   edgecolor="white", linewidth=0.7, zorder=3, label=f"{sci(f['budget'])} FLOPs")
        ax.scatter([f["N_opt"]], [f["loss_opt"]], marker="*", s=240, color=col[f["budget"]], edgecolor=INK,
                   linewidth=0.9, zorder=4)
    ax.set_xscale("log")
    nice_log(ax, "x")
    ax.set_xlabel("Parameters N")
    ax.set_ylabel("Validation loss (nats per character)")
    ax.set_title("IsoFLOP curves: every dot in a colour used the same compute")
    ax.legend(loc="upper right", title="compute budget", title_fontsize=9.5)
    save(fig, "fig_iso_curves.png")

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.3))
    C = np.array([f["budget"] for f in a2["per_budget"]])
    cx = np.logspace(np.log10(C.min()) - 0.25, np.log10(C.max()) + 0.25, 50)
    mid = np.exp(np.mean(np.log(C)))
    for ax, key, k, e, pe, ke, label in [
            (axes[0], "N_opt", a2["kN"], a2["a"], PAPER["a"]["approach2"], PAPER["a"]["kaplan"], "Optimal parameters N"),
            (axes[1], "D_opt", a2["kD"], a2["b"], PAPER["b"]["approach2"], PAPER["b"]["kaplan"], "Optimal training characters D")]:
        y = np.array([f[key] for f in a2["per_budget"]])
        ref_line(ax, cx, k * mid**e, mid, ke, color=KAPLAN, ls="--", lw=1.5, label=f"Kaplan et al. slope {ke}")
        ref_line(ax, cx, k * mid**e, mid, pe, color=PAPERC, lw=1.4, alpha=0.8, label=f"Chinchilla slope {pe}")
        ax.plot(cx, k * cx**e, color=OURS, lw=2.6, label=f"our fit: slope {e:.2f}")
        ax.scatter(C, y, s=150, marker="*", color=[col[c] for c in C], edgecolor=INK, linewidth=0.9, zorder=3)
        ax.set_xscale("log")
        ax.set_yscale("log")
        nice_log(ax, "y")
        ax.set_xlabel("Compute C (FLOPs)")
        ax.set_title(label)
        ax.legend(loc="upper left")
    save(fig, "fig_iso_scaling.png")


def fig_paper_scale():
    """The paper's own fitted law (Eq. 2, Appendix D.2) at real scale, with C = 6ND."""
    f = PAPER["fit"]
    law = lambda N, D: f["E"] + f["A"] / N ** f["alpha"] + f["B"] / D ** f["beta"]  # noqa: E731
    models = [("GPT-3", 175e9, 300e9), ("Gopher", 280e9, 300e9), ("Jurassic-1", 178e9, 300e9),
              ("MT-NLG", 530e9, 270e9), ("Chinchilla", 70e9, 1.4e12)]
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.6), gridspec_kw={"wspace": 0.3})
    ax = axes[0]
    C = 5.76e23  # Gopher's and Chinchilla's shared training budget (paper Table 3 / Section 4)
    N = np.logspace(9.3, 12.3, 300)
    ax.plot(N, law(N, C / (6 * N)), color=PAPERC, lw=2.6, label=f"IsoFLOP curve at {sci(C, 2)} FLOPs")
    nb = N[np.argmin(law(N, C / (6 * N)))]
    ax.scatter([nb], [law(nb, C / (6 * nb))], marker="*", s=260, color=PAPERC, edgecolor=INK, zorder=4)
    for name, n, d in models[1:2] + models[4:]:
        ax.scatter([n], [law(n, d)], s=90, color=OURS if name == "Chinchilla" else "white", edgecolor=INK, lw=1.4, zorder=5)
        right = name == "Chinchilla"
        ax.annotate(f"{name}: {human(n)} params,\n{human(d)} tokens, loss {law(n, d):.3f}", (n, law(n, d)),
                    xytext=(12, -26) if right else (-12, 12), textcoords="offset points", fontsize=9.5,
                    ha="left" if right else "right")
    ax.annotate(f"best by Eq. 2: {human(nb)}", (nb, law(nb, C / (6 * nb))), xytext=(0, -20),
                textcoords="offset points", fontsize=9.5, ha="center", color=PAPERC)
    ax.set_xscale("log")
    ax.set_ylim(law(nb, C / (6 * nb)) - 0.02, law(nb, C / (6 * nb)) + 0.2)
    ax.set_xlabel("Parameters N")
    ax.set_ylabel("Predicted loss (paper Eq. 2)")
    ax.set_title("One budget, two models: Gopher sits far right of the minimum")
    ax.legend(loc="upper left")
    ax = axes[1]
    Cs = np.logspace(20, 26, 80)
    Ns = np.logspace(7, 14, 1500)
    ax.plot(Cs, [Ns[np.argmin(law(Ns, c / (6 * Ns)))] for c in Cs], color=PAPERC, lw=2.2, label="best N by Eq. 2")
    ax.plot(Cs, np.sqrt(Cs / 120), color=OURS, lw=2.2, ls="--", label="20 tokens per parameter")
    for name, n, d in models:
        ax.scatter([6 * n * d], [n], s=70, color=OURS if name == "Chinchilla" else "white", edgecolor=INK, lw=1.3, zorder=4)
        if name != "Jurassic-1":  # sits on top of GPT-3
            ax.annotate("GPT-3, Jurassic-1" if name == "GPT-3" else name, (6 * n * d, n), xytext=(-9, 3),
                        textcoords="offset points", fontsize=9.5, ha="right", va="center")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Training compute C = 6ND (FLOPs)")
    ax.set_ylabel("Parameters N")
    ax.set_title("2021's giants were too big for their compute")
    ax.legend(loc="upper left")
    save(fig, "fig_paper_scale.png")


DIAG = [  # (diagnostic run, the batch-64 run with the same model and budget)
    ("diag_C1e12_L2_d40_b16", "iso_C1.00e+12_L2_d40"), ("diag_C1e12_L2_d48_b16", "iso_C1.00e+12_L2_d48"),
    ("diag_C1e12_L2_d64_b16", "iso_C1.00e+12_L2_d64"), ("diag_C1e13_L3_d96_b32", "iso_C1.00e+13_L3_d96"),
    ("diag_C1e13_L2_d56_b32", "iso_C1.00e+13_L2_d56"), ("diag_C3e13_L4_d112_b32", "iso_C3.16e+13_L4_d112"),
    ("diag_C3e13_L3_d80_b32", "iso_C3.16e+13_L3_d80")]


def diagnostics():
    """Same model, same compute, same data: only the batch (so the number of optimizer steps) changes."""
    out = []
    for small, big in DIAG:
        ps, pb = (os.path.join(HERE, "runs", n + ".json") for n in (small, big))
        if os.path.exists(ps) and os.path.exists(pb):
            s, b = json.load(open(ps)), json.load(open(pb))
            out.append(dict(params=b["params"], budget=b["budget"], steps64=b["steps"], steps_small=s["steps"],
                            batch_small=s["batch"], loss64=b["val_loss"], loss_small=s["val_loss"]))
    return out


def fig_batch_fix(att1, a2_att1, a2, diag):
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.4), gridspec_kw={"wspace": 0.28})
    ax = axes[0]
    C1 = np.array([f["budget"] for f in a2_att1["per_budget"]])
    cx = np.logspace(np.log10(C1.min()) - 0.2, np.log10(C1.max()) + 0.2, 50)
    for fits, color, label, marker in [(a2_att1, KAPLAN, "attempt 1: same batch for every run", "s"),
                                       (a2, OURS, "attempt 2: best of up to 3 batch sizes per run", "*")]:
        C = np.array([f["budget"] for f in fits["per_budget"]])
        ax.scatter(C, [f["N_opt"] for f in fits["per_budget"]], marker=marker, s=150 if marker == "*" else 60,
                   color=color, edgecolor=INK, lw=0.8, zorder=3)
        ax.plot(cx, fits["kN"] * cx ** fits["a"], color=color, lw=2.2, label=f"{label}  (a = {fits['a']:.2f})")
    ax.set_xscale("log")
    ax.set_yscale("log")
    nice_log(ax, "y")
    ax.set_xlabel("Compute C (FLOPs)")
    ax.set_ylabel("Compute-optimal parameters")
    ax.set_title("Starving small-budget runs of steps tilts the answer toward Kaplan")
    ax.legend(loc="upper left", fontsize=9)
    ax = axes[1]
    if diag:
        x = [d["steps64"] for d in diag]
        y = [d["loss_small"] - d["loss64"] for d in diag]
        ax.axhline(0, color=MUTED, lw=1)
        ax.axvspan(10, TRY_SMALLER_BELOW, color=GRID, alpha=0.7, lw=0)
        ax.scatter(x, y, s=70, color=[OURS if v < -0.01 else KAPLAN for v in y], edgecolor=INK, zorder=3)
        for d, xi, yi in zip(diag, x, y):
            if yi < -0.01:
                ax.annotate(f"{human(d['params'])} params @ {sci(d['budget'])}", (xi, yi), xytext=(8, -3),
                            textcoords="offset points", fontsize=8.5, color=MUTED)
        ax.text(0.97, 0.45, "grey: 1,900+ steps,\nno real gain", transform=ax.transAxes, ha="right", fontsize=9, color=MUTED)
        ax.set_xscale("log")
        ax.set_xlim(200, 9000)
        nice_log(ax, "x", fmt=lambda v: f"{v:,.0f}")
        ax.text(0.03, 0.96, f"shaded: fewer than {TRY_SMALLER_BELOW:,} steps,\nwhere we also try smaller batches",
                transform=ax.transAxes, fontsize=9.5, va="top")
        ax.set_xlabel("Optimizer steps with the original batch (4,096 characters)")
        ax.set_ylabel("Loss change with a smaller batch")
        ax.set_title("Same model, compute and data; only the batch changes")
    save(fig, "fig_batch_fix.png")


def fig_envelope(runs, a1):
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.1), gridspec_kw={"width_ratios": [1.45, 1, 1]})
    ax = axes[0]
    Ns = sorted({r["params"] for r in runs})
    lo, hi = np.log(min(Ns)), np.log(max(Ns))
    for r in runs:
        c = np.array(r["curve"])
        ax.plot(c[:, 1], c[:, 2], color=SIZE_RAMP((np.log(r["params"]) - lo) / (hi - lo)), lw=0.9, alpha=0.75)
    grid = np.array(a1["grid"])
    ax.plot(grid, a1["env_loss"], color=INK, lw=2.4, label="lowest loss at each FLOP count")
    ax.set_xscale("log")
    ax.set_xlim(grid[0] / 30, grid[-1] * 1.3)
    last = [np.array(r["curve"])[-1, 2] for r in runs]
    ax.set_ylim(min(last) - 0.05, min(last) + 1.0)
    ax.set_xlabel("Training FLOPs so far")
    ax.set_ylabel("Training loss (smoothed)")
    ax.set_title("Every training curve, and their lower envelope")
    ax.text(0.03, 0.04, "jumps: just past each budget,\nonly unfinished runs are left", transform=ax.transAxes,
            fontsize=9, color=MUTED)
    sm = plt.cm.ScalarMappable(cmap=SIZE_RAMP, norm=matplotlib.colors.LogNorm(min(Ns), max(Ns)))
    cb = fig.colorbar(sm, ax=ax, pad=0.01)
    cb.set_label("parameters", color=MUTED)
    ax.legend(loc="upper right", facecolor="white", framealpha=0.9, frameon=True, edgecolor="none")
    for ax, y, e, k, pe, ke, label in [
            (axes[1], np.array(a1["env_N"]), a1["a"], a1["kN"], PAPER["a"]["approach1"], PAPER["a"]["kaplan"], "Winning model size"),
            (axes[2], grid / fpt(np.array(a1["env_N"])), a1["b"], a1["kD"], PAPER["b"]["approach1"], PAPER["b"]["kaplan"], "Winning token count")]:
        mid = np.exp(np.mean(np.log(grid)))
        ref_line(ax, grid, k * mid**e, mid, ke, color=KAPLAN, ls="--", lw=1.4, label=f"Kaplan slope {ke}")
        ax.scatter(grid, y, s=12, color=SIZE_RAMP(0.55), alpha=0.8, zorder=3)
        ax.plot(grid, k * grid**e, color=OURS, lw=2.2, label=f"our fit: slope {e:.2f}")
        ax.set_xscale("log")
        ax.set_yscale("log")
        nice_log(ax, "y")
        ax.set_xlabel("Compute C (FLOPs)")
        ax.set_title(label)
        ax.legend(loc="upper left")
        ax.text(0.97, 0.05, f"paper: {pe}", transform=ax.transAxes, ha="right", color=PAPERC, fontsize=10)
    save(fig, "fig_envelope.png")


def fig_parametric(runs, a3, budgets):
    col = budget_colors(budgets)
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.4))
    ax = axes[0]
    C = np.logspace(np.log10(min(budgets)) - 0.6, np.log10(max(budgets)) + 0.6, 220)
    N = np.logspace(np.log10(min(r["params"] for r in runs)) - 0.3, np.log10(max(r["params"] for r in runs)) + 0.3, 220)
    CC, NN = np.meshgrid(C, N)
    L = predict(a3, NN, CC / fpt(NN))
    levels = np.linspace(np.percentile(L, 3), np.percentile(L, 80), 14)
    cs = ax.contourf(CC, NN, L, levels=levels, cmap=RAMP.reversed(), alpha=0.9, extend="both")
    ax.contour(CC, NN, L, levels=levels, colors="white", linewidths=0.4, alpha=0.6)
    fr = frontier_numeric(a3, C)
    ax.plot(C, fr, color=OURS, lw=2.6, label="efficient frontier (lowest loss)")
    for c in budgets:
        ax.axvline(c, color="white", lw=1, ls=":", alpha=0.9)
    ax.scatter([r["flops"] for r in runs], [r["params"] for r in runs], s=14, color="white", edgecolor=INK,
               linewidth=0.5, zorder=3, label="our training runs")
    ax.set_xscale("log")
    ax.set_yscale("log")
    nice_log(ax, "y")
    ax.grid(False)
    ax.set_xlabel("Compute C (FLOPs)")
    ax.set_ylabel("Parameters N")
    ax.set_title("Fitted loss L(N, D) as a map")
    cb = fig.colorbar(cs, ax=ax, pad=0.01)
    cb.set_label("predicted loss", color=MUTED)
    ax.legend(loc="upper left", facecolor="white", framealpha=0.85, frameon=True, edgecolor="none")
    ax = axes[1]
    for c in budgets:
        pts = [r for r in runs if r["budget"] == c]
        n = np.logspace(np.log10(min(r["params"] for r in pts)) - 0.15, np.log10(max(r["params"] for r in pts)) + 0.15, 120)
        ax.plot(n, predict(a3, n, c / fpt(n)), color=col[c], lw=1.8)
        ax.scatter([r["params"] for r in pts], [r["val_loss"] for r in pts], s=26, color=col[c], edgecolor="white",
                   linewidth=0.6, zorder=3, label=f"{sci(c)} FLOPs")
        nb = frontier_numeric(a3, c)[0]
        ax.scatter([nb], predict(a3, nb, c / fpt(nb)), marker="*", s=170, color=col[c], edgecolor=INK, lw=0.8, zorder=4)
    ax.set_xscale("log")
    nice_log(ax, "x")
    ax.set_xlabel("Parameters N")
    ax.set_ylabel("Validation loss")
    ax.set_title(f"Fitted curves (lines) vs our runs (dots): mean error {100 * a3['mean_abs_err']:.1f}%")
    ax.legend(loc="upper right")
    save(fig, "fig_parametric.png")


def fig_summary(a1, a2, a3, budgets, head):
    """Our version of the paper's Figure 1: three approaches agree; Kaplan's slope does not."""
    fig, ax = plt.subplots(figsize=(8.4, 4.9))
    C = np.logspace(np.log10(min(budgets)) - 0.2, np.log10(max(budgets)) + 1.0, 100)
    ax.axvspan(max(budgets), C[-1], color=GRID, alpha=0.55, lw=0)
    ax.text(max(budgets) * 1.12, 0.97, "extrapolation", transform=ax.get_xaxis_transform(), va="top",
            color=MUTED, fontsize=9)
    ax.plot(C, a1["kN"] * C**a1["a"], color="#12b886", lw=2.2, label=f"Approach 1: minimum over training curves (a = {a1['a']:.2f})")
    ax.plot(C, a2["kN"] * C**a2["a"], color=OURS, lw=3.4, label=f"Approach 2: IsoFLOP profiles (a = {a2['a']:.2f})")
    ax.plot(C, frontier_numeric(a3, C), color="#7048e8", lw=2.2, ls=(0, (5, 3)),
            label=f"Approach 3: parametric fit (a = {a3['a']:.2f})")
    c0 = min(budgets)
    ref_line(ax, C, a2["kN"] * c0**a2["a"], c0, PAPER["a"]["kaplan"], color=KAPLAN, lw=1.8, ls="--",
             label="Kaplan et al. (2020) slope, a = 0.73")
    if head:
        for key, marker, name in [("gopher", "s", "mini-Gopher"), ("chinchilla", "*", "mini-Chinchilla")]:
            r = head[key]
            ax.scatter([r["flops"]], [r["params"]], marker=marker, s=190 if marker == "*" else 80,
                       color="white" if key == "gopher" else OURS, edgecolor=INK, lw=1.2, zorder=5)
            ax.annotate(name, (r["flops"], r["params"]), xytext=(9, -3 if key == "gopher" else -14),
                        textcoords="offset points", fontsize=10, weight="semibold")
    ax.set_xscale("log")
    ax.set_yscale("log")
    nice_log(ax, "y")
    ax.set_xlabel("Compute C (FLOPs)")
    ax.set_ylabel("Compute-optimal parameters N")
    ax.set_title("Two approaches match the paper; all three stay below Kaplan's 0.73")
    ax.legend(loc="upper left", fontsize=9)
    save(fig, "fig_summary.png")


def fig_head_to_head(head):
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.1), gridspec_kw={"width_ratios": [1, 1.5]})
    ax = axes[0]
    order = [("gopher", "mini-Gopher", "white"), ("chinchilla", "mini-Chinchilla", OURS)]
    lo = min(head[k]["val_loss"] for k in ("gopher", "chinchilla"))
    hi = max(head[k]["val_loss"] for k in ("gopher", "chinchilla"))
    for i, (k, name, c) in enumerate(order):
        r = head[k]
        ax.plot([i, i], [lo - 0.5 * (hi - lo), r["val_loss"]], color=GRID, lw=6, solid_capstyle="round", zorder=1)
        ax.scatter([i], [r["val_loss"]], s=260, color=c, edgecolor=INK, lw=1.4, zorder=3,
                   marker="s" if k == "gopher" else "*")
        ax.annotate(f"{r['val_loss']:.3f}", (i, r["val_loss"]), xytext=(18, -4), textcoords="offset points",
                    weight="semibold", fontsize=12)
    ax.set_ylim(lo - 0.6 * (hi - lo), hi + 0.6 * (hi - lo))
    ax.set_xlim(-0.6, 1.8)
    ax.set_xticks([0, 1])
    ax.set_xticklabels([f"{n}\n{human(head[k]['params'])} params\n{human(head[k]['tokens'])} chars"
                        for k, n, _ in order])
    ax.set_ylabel("Validation loss (lower is better)")
    ax.set_title(f"Same compute ({sci(head['chinchilla']['budget'])} FLOPs)")
    ax.grid(axis="x", visible=False)
    ax = axes[1]
    for k, name, c in order:
        cv = np.array(head[k]["curve"])
        ax.plot(cv[:, 1], cv[:, 2], color=INK if k == "gopher" else OURS, lw=2, ls="--" if k == "gopher" else "-",
                label=f"{name}: {human(head[k]['params'])} params")
    ax.set_xscale("log")
    cv = np.array(head["gopher"]["curve"])
    ax.set_ylim(lo - 0.08, lo + 1.0)
    ax.set_xlim(cv[0, 1] * 3, cv[-1, 1] * 1.1)
    ax.set_xlabel("Training FLOPs so far")
    ax.set_ylabel("Training loss")
    ax.set_title("Training curves: the small model on more data ends lower")
    ax.legend(loc="upper right")
    save(fig, "fig_head_to_head.png")


def fig_cosine(runs):
    runs = sorted(runs, key=lambda r: r["cycle"])
    cmap = LinearSegmentedColormap.from_list("cyc", [OURS, "#a5264a", "#4a2a86", "#8a919e"])
    colors = [cmap(i / max(1, len(runs) - 1)) for i in range(len(runs))]
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.9), gridspec_kw={"width_ratios": [1, 1.25, 0.9]})
    for r, c in zip(runs, colors):
        cv = np.array(r["curve"])
        label = "matched (paper)" if r["cycle"] == 1 else f"{r['cycle']:g}× too long"
        axes[0].plot(cv[:, 0] / 1e6, cv[:, 3] * 1e3, color=c, lw=2, label=label)
        n = len(cv) // 3
        sm = np.convolve(cv[:, 2], np.ones(9) / 9, mode="valid")
        axes[1].plot(cv[4:-4, 0][n:] / 1e6, sm[n:], color=c, lw=1.8)
    axes[0].set_title("Learning-rate schedule")
    axes[0].set_xlabel("Characters seen (millions)")
    axes[0].set_ylabel(r"Learning rate ($\times 10^{-3}$)")
    axes[0].legend(fontsize=9)
    axes[1].set_title("Training loss (last two-thirds of the run)")
    axes[1].set_xlabel("Characters seen (millions)")
    ax = axes[2]
    xs = np.arange(len(runs))
    ax.plot(xs, [r["val_loss"] for r in runs], color=INK, lw=1.2, zorder=1)
    ax.scatter(xs, [r["val_loss"] for r in runs], color=colors, s=70, edgecolor=INK, zorder=2)
    ax.set_xticks(xs)
    ax.set_xticklabels([f"{r['cycle']:g}×" for r in runs])
    ax.set_xlim(-0.4, len(runs) - 0.6)
    ax.set_xlabel("Cosine cycle length ÷ run length")
    ax.set_ylabel("Final validation loss")
    ax.set_title("Overshooting the schedule hurts")
    save(fig, "fig_cosine.png")


def fig_lr(runs):
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    shapes = sorted({(r["n_layer"], r["d_model"]) for r in runs}, key=lambda s: size(*s))
    top = min(max(r["val_loss"] for r in runs), min(r["val_loss"] for r in runs) + 0.62)
    for i, (L, d) in enumerate(shapes):
        rs = sorted((r for r in runs if (r["n_layer"], r["d_model"]) == (L, d)), key=lambda r: r["lr"])
        c = SIZE_RAMP(i / max(1, len(shapes) - 1))
        ys = [min(r["val_loss"], top) for r in rs]
        ax.plot([r["lr"] for r in rs], ys, "-", color=c, lw=1.8, label=f"{human(rs[0]['params'])} params (d={d})")
        for r, y in zip(rs, ys):
            ax.scatter([r["lr"]], [y], marker="^" if r["val_loss"] > top else "o", s=46 if r["val_loss"] > top else 26,
                       color=c, zorder=3)
        best = min(rs, key=lambda r: r["val_loss"])
        ax.scatter([best["lr"]], [best["val_loss"]], s=170, facecolor="none", edgecolor=c, lw=1.6, zorder=4)
    ax.set_ylim(None, top + 0.03)
    ax.set_xscale("log")
    ax.set_xlabel("Peak learning rate")
    ax.set_ylabel("Validation loss")
    ax.set_title(f"Learning-rate check at {sci(runs[0]['budget'])} FLOPs (circle = best)")
    ax.legend(fontsize=9, loc="upper left", bbox_to_anchor=(1.01, 1.0), title="triangles: run went\nunstable (off chart)",
              title_fontsize=8.5)
    save(fig, "fig_lr.png")


# ------------------------------------------------------------------------------ samples
def samples(run, prompts=("Once upon a time", "Lily wanted to", "The little dog"), length=260, seed=0):
    import torch

    from model import GPT
    m = GPT(V, CTX, run["n_layer"], run["d_model"], run["n_head"])
    m.load_state_dict(torch.load(os.path.join(HERE, "runs", run["name"] + ".pt"), map_location="cpu"))
    m.eval()
    stoi = {c: i for i, c in enumerate(VOCAB)}
    out = []
    for i, p in enumerate(prompts):
        g = torch.Generator().manual_seed(seed + i)
        ids = m.generate(torch.tensor([[stoi[c] for c in p]]), length, temperature=0.8, generator=g)[0].tolist()
        out.append("".join(VOCAB[j] for j in ids).split("\x04")[0].strip())
    return out


# ------------------------------------------------------------------------------ main
def thin(curve, n=48):
    c = np.array(curve)
    idx = np.unique(np.round(np.geomspace(1, len(c), n)).astype(int) - 1)
    return [[float(c[i, 1]), round(float(c[i, 2]), 4)] for i in idx]


def main():
    style()
    iso = load_iso()
    budgets = sorted({r["budget"] for r in iso})
    a2, a1, a3 = approach2(iso), approach1(iso), approach3(iso)
    att1 = [r for s in ("isoflop", "isoflop_b64") for r in load(s) if r.get("attempt1")]
    a2_att1 = approach2(att1)
    diag = diagnostics()
    fig_batch_fix(att1, a2_att1, a2, diag)
    fig_isoflop(iso, a2)
    fig_iso_parts(iso, a2)
    fig_paper_scale()
    fig_envelope(iso, a1)
    fig_parametric(iso, a3, budgets)

    head = None
    hh = load("gopher")
    gophers = [r for r in hh if r.get("role") == "gopher"]
    chins = [r for r in hh if r.get("role") == "chinchilla"]
    if gophers and chins:
        head = {"gopher": min(gophers, key=lambda r: r["val_loss"]), "chinchilla": chins[0]}
        head_lrs = [{"batch": r.get("batch", 64), "lr": r["lr"], "val_loss": r["val_loss"]} for r in gophers]
        fig_head_to_head(head)
        for k in head:
            head[k] = dict({x: head[k][x] for x in ("name", "params", "tokens", "flops", "budget", "val_loss",
                                                   "n_layer", "d_model")},
                           curve=thin(head[k]["curve"], 80), samples=samples(head[k]), lr=head[k]["lr"])
        head["gopher_lrs"] = head_lrs
    fig_summary(a1, a2, a3, budgets, head)
    cos = load("cosine")
    if cos:
        fig_cosine(cos)
    lr = load("lr")
    if lr:
        fig_lr(lr)

    all_runs = [json.load(open(p)) for p in glob.glob(os.path.join(HERE, "runs", "*.json"))]
    all_runs = [r for r in all_runs if not r.get("reused_from")]  # 5 diagnostics were reused as IsoFLOP runs
    results = {
        "meta": {"runs": len(all_runs), "flops": sum(r["flops"] for r in all_runs),
                 "seconds": sum(r["seconds"] for r in all_runs), "device": "Apple M4 laptop (MPS)",
                 "vocab": len(VOCAB), "ctx": CTX, "train_chars": 196988853},
        "fpt_fit": {"k": FPT_K, "g": FPT_G},
        "ladder": [{"n_layer": L, "d_model": d, "params": size(L, d),
                    "fpt": train_flops_per_token(L, d, heads(d), CTX, V)} for L, d in LADDER],
        "budgets": budgets,
        "isoflop": [{k: r[k] for k in ("budget", "params", "tokens", "flops", "val_loss", "n_layer", "d_model", "lr", "batch", "steps")}
                    | {"curve": thin(r["curve"])} for r in iso],
        "approach1": {k: a1[k] for k in ("a", "b", "kN", "kD", "a_ci", "b_ci")}
                     | {"grid": a1["grid"], "env_N": a1["env_N"], "env_loss": a1["env_loss"]},
        "approach2": {k: a2[k] for k in ("a", "b", "kN", "kD", "a_ci", "b_ci")}
                     | {"per_budget": [{k: f[k] for k in ("budget", "coef", "N_opt", "D_opt", "loss_opt", "inside")}
                                       for f in a2["per_budget"]]},
        "approach3": {k: a3[k] for k in ("E", "A", "B", "alpha", "beta", "a", "b", "G", "a_ci", "b_ci", "mean_abs_err")},
        "attempt1": {"isoflop": [{k: r[k] for k in ("budget", "params", "tokens", "flops", "val_loss", "n_layer", "d_model")}
                                 for r in att1],
                     "approach2": {k: a2_att1[k] for k in ("a", "b", "kN", "kD", "a_ci", "b_ci")}
                     | {"per_budget": [{k: f[k] for k in ("budget", "coef", "N_opt", "D_opt", "loss_opt")}
                                       for f in a2_att1["per_budget"]]}},
        "diagnostics": diag,
        "min_steps": TRY_SMALLER_BELOW,
        "head_to_head": head,
        "cosine": [{"cycle": r["cycle"], "val_loss": r["val_loss"], "params": r["params"], "tokens": r["tokens"],
                    "curve": [[c[0], round(c[2], 4), c[3]] for c in r["curve"][::2]]} for r in cos],
        "lr_pilot": [{k: r[k] for k in ("params", "d_model", "n_layer", "lr", "val_loss", "budget")} for r in lr],
        "paper": PAPER,
    }
    json.dump(results, open(os.path.join(HERE, "results.json"), "w"))

    print(f"\n{'':24s}{'a (N_opt ~ C^a)':>22s}{'b (D_opt ~ C^b)':>22s}")
    for name, key, r in [("Approach 1", "approach1", a1), ("Approach 2", "approach2", a2), ("Approach 3", "approach3", a3)]:
        print(f"{name:24s}{r['a']:>8.2f} [{r['a_ci'][0]:.2f}, {r['a_ci'][1]:.2f}]"
              f"{r['b']:>9.2f} [{r['b_ci'][0]:.2f}, {r['b_ci'][1]:.2f}]   paper: {PAPER['a'][key]:.2f} / {PAPER['b'][key]:.2f}")
    print(f"{'Kaplan et al. (2020)':24s}{0.73:>8.2f}{0.27:>23.2f}")
    print(f"{'Attempt 1 (fixed batch)':24s}{a2_att1['a']:>8.2f} [{a2_att1['a_ci'][0]:.2f}, {a2_att1['a_ci'][1]:.2f}]")
    print("\nIsoFLOP minima:")
    for f in a2["per_budget"]:
        print(f"  C={f['budget']:.2e}  N_opt={f['N_opt']:>10,.0f}  D_opt={f['D_opt']:>12,.0f}  "
              f"chars/param={f['D_opt'] / f['N_opt']:6.1f}  loss={f['loss_opt']:.4f}  inside={f['inside']}")
    print(f"\nApproach 3: E={a3['E']:.3f} A={a3['A']:.1f} B={a3['B']:.1f} alpha={a3['alpha']:.3f} "
          f"beta={a3['beta']:.3f}  mean error {100 * a3['mean_abs_err']:.2f}%")
    if head:
        for k, r in head.items():
            if k != "gopher_lrs":
                print(f"{k:11s} N={r['params']:>9,} D={r['tokens']:>12,.0f} loss={r['val_loss']:.4f} lr={r['lr']:g}")
        print("mini-Gopher tries:", sorted((t["batch"], t["lr"], round(t["val_loss"], 4)) for t in head["gopher_lrs"]))


if __name__ == "__main__":
    main()
