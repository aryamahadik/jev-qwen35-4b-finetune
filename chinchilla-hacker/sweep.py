"""Step 3: the experiment grid. Every run is one call to train.run().

Stages (run them in this order):
  lr       pilot: which learning rate is fair to every model size?
  isoflop  the core of the paper (Approach 2): for each compute budget, train models of
           many sizes, each for exactly budget/FLOPs-per-token characters
  gopher   the paper's headline test at our scale: same compute, a big model on few tokens
           (Gopher's ratio) vs a small model on many tokens (Chinchilla's ratio)
  cosine   Appendix B / Figure A1: a cosine schedule longer than the run hurts

Usage:  python sweep.py isoflop [--workers 2]
Runs are saved in runs/*.json, so a stopped sweep resumes where it left off.
"""
import argparse
import math
import multiprocessing as mp
import os

from flops import n_params, train_flops_per_token
from train import CTX, RUNS, VOCAB, Stream, heads, lr_for, run

V = len(VOCAB)

# Model family (n_layer, d_model): 21 shapes from 17K to 6.3M parameters, each ~1.2-1.5x the last,
# with width/depth kept between 16 and 32.
LADDER = [(2, 24), (2, 32), (2, 40), (2, 48), (2, 56), (2, 64), (3, 64), (3, 80), (3, 96), (4, 96), (4, 112),
          (4, 128), (5, 128), (5, 144), (5, 160), (6, 176), (6, 192), (7, 208), (7, 224), (8, 240), (8, 256)]


def size(L, d):
    return n_params(L, d, CTX, V)


def stage_lr():
    shapes = [(2, 32), (2, 64), (3, 96), (4, 128), (5, 160)]
    return [dict(name=f"lr_L{L}_d{d}_lr{lr:g}", n_layer=L, d_model=d, flops=1e13, lr=lr, stage="lr")
            for L, d in shapes for lr in (1e-3, 2e-3, 4e-3, 8e-3, 1.6e-2, 3.2e-2)]


# Compute budgets: half-decades from 1e12 FLOPs (the paper used 9 budgets, 6e18 ... 3e21).
BUDGETS = [1e12, 10**12.5, 1e13, 10**13.5]


MIN_STEPS, TRY_SMALLER_BELOW = 400, 3000


def steps_for(L, d, C, B):
    return C / train_flops_per_token(L, d, heads(d), CTX, V) / (B * CTX)


def batches_for(L, d, C):
    """Batch sizes (sequences of 64 characters) to try for one (model, budget); we keep the best run.
    Attempt 1 used 64 (4K characters) for every run; at small budgets the bigger models then got only
    300-700 optimizer steps and looked far worse than they are. Now: start at 64 and also try 32, then 16,
    while the run has fewer than 3,000 steps. (Diagnostics: runs that already had 3,000+ steps did not
    improve with a smaller batch.) Batches giving fewer than 400 steps are skipped."""
    out = []
    for B in (64, 32, 16):
        n = steps_for(L, d, C, B)
        if n >= MIN_STEPS:
            out.append(B)
        if n >= TRY_SMALLER_BELOW:
            break
    return out or [16]


def guess_opt(C):
    """Rough optimum from the diagnostic runs (~40-65K params at 1e12, ~240K at 3e13). Only used to centre
    each budget's window of sizes; the window (~10x wide) is where the parabola looks for the real optimum."""
    return 65e3 * (C / 1e12) ** 0.38


def stage_isoflop():
    runs = []
    for C in BUDGETS:
        for L, d in LADDER:
            if guess_opt(C) / 3.5 <= size(L, d) <= guess_opt(C) * 3:
                for B in batches_for(L, d, C):
                    runs.append(dict(name=f"iso_C{C:.2e}_L{L}_d{d}" + (f"_b{B}" if B != 64 else ""), n_layer=L,
                                     d_model=d, flops=C, lr=lr_for(d), batch=B, stage="isoflop",
                                     save=C == BUDGETS[-1]))
    return runs


def nearest(N):
    """The model shape in our family whose parameter count is closest to N."""
    return min(LADDER, key=lambda s: abs(math.log(size(*s) / N)))


def optimum(C):
    """Compute-optimal size at budget C, from the finished IsoFLOP runs (Approach 2)."""
    from analyze import isoflop_fits, load_iso
    return next(f["N_opt"] for f in isoflop_fits(load_iso()) if f["budget"] == C)


def stage_gopher():
    """Paper Section 4 at our scale, at 3.2e13 FLOPs. mini-Chinchilla = our compute-optimal size;
    mini-Gopher = 4x the parameters (Gopher/Chinchilla = 280B/70B), so ~4x fewer tokens.
    To be fair, mini-Gopher also gets a second, lower learning rate and keeps its better run."""
    C = 10**13.5
    n = optimum(C)
    (Lc, dc), (Lg, dg) = nearest(n), nearest(4 * n)
    sfx = lambda B: f"_b{B}" if B != 64 else ""  # noqa: E731
    return [dict(name=f"h2h_chinchilla_L{Lc}_d{dc}{sfx(B)}", n_layer=Lc, d_model=dc, flops=C, lr=lr_for(dc),
                 batch=B, stage="gopher", role="chinchilla", save=True) for B in batches_for(Lc, dc, C)] + \
           [dict(name=f"h2h_gopher_L{Lg}_d{dg}_lr{lr:g}{sfx(B)}", n_layer=Lg, d_model=dg, flops=C, lr=lr,
                 batch=B, stage="gopher", role="gopher", save=True)
            for B in batches_for(Lg, dg, C) for lr in (lr_for(dg), lr_for(dg) / 2)]


def stage_cosine():
    """Paper Appendix B / Figure A1: same model, same steps; only the cosine cycle length changes."""
    C = 1e13
    L, d = nearest(optimum(C))
    return [dict(name=f"cos_{cyc:g}x_L{L}_d{d}", n_layer=L, d_model=d, flops=C, lr=lr_for(d), cycle=cyc,
                 stage="cosine") for cyc in (1.0, 1.25, 1.5, 2.0, 5.0)]


STAGES = {"lr": stage_lr, "isoflop": stage_isoflop, "gopher": stage_gopher, "cosine": stage_cosine}

_streams = {}


def _init():
    _streams[64] = Stream()


def _work(cfg):
    B = cfg.get("batch", 64)
    if B not in _streams:
        _streams[B] = Stream(batch=B)
    r = run(stream=_streams[B], **cfg)
    return r["name"], r["params"], r["tokens"], r["val_loss"], r["seconds"]


def execute(configs, workers):
    todo = [c for c in configs if not os.path.exists(os.path.join(RUNS, c["name"] + ".json"))]

    def cost(c):  # rough seconds: FLOPs / measured laptop speed, which grows with model size
        fpt = train_flops_per_token(c["n_layer"], c["d_model"], heads(c["d_model"]), CTX, V)
        flops = c.get("flops") or c["tokens"] * fpt
        return flops / (2.5e11 * (size(c["n_layer"], c["d_model"]) / 3e4) ** 0.25)

    todo.sort(key=cost, reverse=True)  # longest first, so the workers finish together
    print(f"{len(configs)} runs, {len(todo)} to do, about {sum(map(cost, todo)) / 60 / workers:.0f} min", flush=True)
    with mp.get_context("spawn").Pool(workers, initializer=_init) as pool:
        for name, N, D, loss, sec in pool.imap_unordered(_work, todo):
            print(f"  {name:28s} N={N:>9,} D={D:>12,}  val loss {loss:.4f}  ({sec:.0f}s)", flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("stage", choices=list(STAGES))
    p.add_argument("--workers", type=int, default=2)
    a = p.parse_args()
    execute(STAGES[a.stage](), a.workers)
