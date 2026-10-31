"""transfer/T36/fit_option_table.py: fit the frozen option table (plugin.py section "A48 w5") on BUILD seed bases only.

Build seed base 3,000,000 (fit), 4,000,000 (held-out check); the G6 / G7 measurements use the pilot base 900,000 and the
fresh dev base 7,000,000. From lean/c2_build:
  collect --base B --seeds N --m 8 --out F.pkl      M feasible proposals per choice seed (the sampler's own draws), r_f of each
  fit --in F.pkl --out option_table.json           max-entropy tilt: accepted mean of every r_f -> 0 (per-seed normalised)
  check --in F.pkl [--table option_table.json]      accepted mean z^2 over features (1.0 = noise) before / after the table
"""
from __future__ import annotations
import argparse, json, math, pickle, random, sys, time
from collections import defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
if str(C2) not in sys.path:
    sys.path.insert(0, str(C2))
SAMPLERS = ("S1", "S2", "S3", "S4")
_W = {}


def _init():
    import contextlib
    import pilot_loaders as PL
    from transfer.T36 import plugin as P
    P._TILT = {}
    stack = contextlib.ExitStack()
    kit = stack.enter_context(PL.open_family("T36"))
    _W.update(P=P, plugin=kit.plugin, stack=stack)


def _seeds(args):
    base, lo, hi, M = args
    P, pl = _W["P"], _W["plugin"]
    out = []
    for idx in range(lo, hi):
        for sm in SAMPLERS:
            seed = base + idx
            kind, _ = P.slot_of(sm, seed)
            if kind != "choice":
                continue
            plan, outcome = P.choice_plan(sm, seed)
            rng = random.Random(f"{P.FAMILY}|{sm}|{seed}")
            props = []
            for t in range(P.MAX_TRIES):
                spec = pl._draw(rng, seed, sm, P.CHOICE_FORM, None, outcome, t // P.BLOCK_TRIES)
                if spec is None:
                    continue
                os_ = pl._options(spec, strict=True)
                if os_ is None:
                    continue
                props.append(pl.option_r(os_))
                if len(props) >= M:
                    break
            if props:
                out.append({"seed": seed, "sampler": sm, "k": plan.k, "outcome": outcome, "props": props})
    return out


def collect(a):
    from multiprocessing import Pool
    chunks = [(a.base, i, min(i + 20, a.seeds), a.m) for i in range(0, a.seeds, 20)]
    t0 = time.time()
    rows = []
    with Pool(a.workers, initializer=_init) as pool:
        for r in pool.imap_unordered(_seeds, chunks):
            rows += r
    rows.sort(key=lambda r: (r["seed"], r["sampler"]))
    Path(a.out).write_bytes(pickle.dumps(rows))
    print(f"collected {len(rows)} choice seeds x <= {a.m} proposals in {time.time() - t0:.0f}s ->", a.out, flush=True)


class _Mat:
    """The proposals as a sparse matrix R (proposal x feature), per-seed groups, for vectorised moments."""
    def __init__(self, rows, feats=None):
        import numpy as np
        from scipy import sparse
        idx = {} if feats is None else {f: i for i, f in enumerate(feats)}
        grow = feats is None
        ri, ci, vv, seed_of = [], [], [], []
        n = 0
        for si, row in enumerate(rows):
            for r in row["props"]:
                for f, v in r.items():
                    if f not in idx:
                        if not grow:
                            continue
                        idx[f] = len(idx)
                    ri.append(n); ci.append(idx[f]); vv.append(v)
                seed_of.append(si)
                n += 1
        self.feats = sorted(idx, key=idx.get)
        self.R = sparse.csr_matrix((vv, (ri, ci)), shape=(n, len(idx)))
        self.R2 = self.R.multiply(self.R).tocsr()
        self.seed = np.array(seed_of)
        self.nseed = len(rows)
        self.np = np


def _acc(M, w, c):
    np = M.np
    s = M.R @ w
    a = np.exp(np.minimum(0.0, s - c))
    Z = np.bincount(M.seed, weights=a, minlength=M.nseed)
    cnt = np.bincount(M.seed, minlength=M.nseed)
    q = a / Z[M.seed]                                   # per-seed normalised accepted weight
    return q, float((Z / cnt).mean())


def _moments(M, w, c):
    q, acc = _acc(M, w, c)
    return M.R.T @ q, M.R2.T @ q, acc, M.nseed


def _calib(M, w, target):
    lo, hi = -10.0, 30.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if _acc(M, w, mid)[1] > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def fit(a):
    import numpy as np
    rows = pickle.loads(Path(a.inp).read_bytes())
    M0 = _Mat(rows)
    cnt = np.asarray((M0.R != 0).sum(axis=0)).ravel() / max(1, len(M0.seed) // M0.nseed)   # ~ seeds showing f
    keep = [f for f, c_ in zip(M0.feats, cnt) if c_ >= a.min_n]
    M = _Mat(rows, keep)
    w = np.zeros(len(keep))
    c = 0.0
    for it in range(a.iters):
        c = _calib(M, w, a.accept) if it else 0.0
        m1, m2, acc, n = _moments(M, w, c)
        z = m1 / np.sqrt(np.maximum(m2, 1e-9))
        print(f"iter {it:2d}: features {len(keep)} accept {acc:.2f} c {c:.2f}  max|z| {np.abs(z).max():.2f}  "
              f"mean z^2 {(z * z).mean():.2f}  |w|max {np.abs(w).max():.2f}", flush=True)
        w = np.clip(w - a.eta * m1 / (m2 + a.ridge), -a.clip, a.clip)
    c = _calib(M, w, a.accept)
    m1, m2, acc, n = _moments(M, w, c)
    out = {"note": "A48 w5 frozen option table (plugin.py): acceptance min(1, exp(sum_f w_f r_f - accept_c))", "accept_c": round(c, 4),
           "fit": {"base": a.base_label, "seeds": n, "m": len(rows[0]["props"]), "iters": a.iters, "eta": a.eta, "ridge": a.ridge,
                   "clip": a.clip, "min_n": a.min_n, "accept_target": a.accept, "features": len(keep), "final_accept": round(acc, 3)},
           "weights": {f: round(float(x), 4) for f, x in sorted(zip(keep, w))}}
    Path(a.out).write_text(json.dumps(out, indent=0))
    print("wrote", a.out, len(keep), "weights; accept_c", out["accept_c"], "mean accept", round(acc, 3))


def check(a):
    import numpy as np
    rows = pickle.loads(Path(a.inp).read_bytes())
    d = json.loads(Path(a.table).read_text()) if a.table else {"weights": {}, "accept_c": 0.0}
    M0 = _Mat(rows)
    cnt = np.asarray((M0.R != 0).sum(axis=0)).ravel() / max(1, len(M0.seed) // M0.nseed)
    keep = [f for f, c_ in zip(M0.feats, cnt) if c_ >= 20]
    M = _Mat(rows, keep)
    w = np.array([d["weights"].get(f, 0.0) for f in keep])
    m1, m2, acc, n = _moments(M, w, d["accept_c"])
    z = m1 / np.sqrt(np.maximum(m2, 1e-9))
    o = np.argsort(z)
    print(f"{n} seeds, accept {acc:.2f}, {len(keep)} features: mean z^2 {(z*z).mean():.2f} (1.0 = noise)  max|z| {np.abs(z).max():.2f}  "
          f"lowest {keep[o[0]]} {z[o[0]]:.2f}  highest {keep[o[-1]]} {z[o[-1]]:.2f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect"); c.add_argument("--base", type=int, required=True); c.add_argument("--seeds", type=int, default=3000)
    c.add_argument("--m", type=int, default=8); c.add_argument("--out", required=True); c.add_argument("--workers", type=int, default=3)
    c.set_defaults(f=collect)
    f = sub.add_parser("fit"); f.add_argument("--in", dest="inp", required=True); f.add_argument("--out", required=True)
    f.add_argument("--iters", type=int, default=30); f.add_argument("--eta", type=float, default=0.7)
    f.add_argument("--ridge", type=float, default=30.0); f.add_argument("--clip", type=float, default=4.0)
    f.add_argument("--accept", type=float, default=0.5); f.add_argument("--min-n", type=int, default=20)
    f.add_argument("--base-label", default="3000000"); f.set_defaults(f=fit)
    k = sub.add_parser("check"); k.add_argument("--in", dest="inp", required=True); k.add_argument("--table", default=None)
    k.set_defaults(f=check)
    args = ap.parse_args(); args.f(args)
