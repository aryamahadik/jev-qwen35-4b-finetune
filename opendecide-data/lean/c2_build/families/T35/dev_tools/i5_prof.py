"""Dev tool (A45 d, T35 pass 3): profile of the SHOWN lines (error-model look-alikes) of no-line vs line rows, from sampled specs.
argv: seed0 seed1. Prints per-flag shares and the profile TV(gold lines, no-line rows' lines)."""
import sys, collections
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2])); sys.path.insert(0, str(HERE.parent))
import pilot_loaders as PL, run_pilot_i4 as R
R.install_loader()
s0, s1 = int(sys.argv[1]), int(sys.argv[2])
with PL.open_family("T35") as kit:
    p = kit.plugin; M = sys.modules[type(p).__module__]
    G = collections.Counter(); A = collections.Counter(); W = collections.Counter(); na = nl = 0; cntA = []
    for s in range(s0, s1):
        for smp in ("S1", "S2", "S3", "S4"):
            try:
                kind, idx = M.slot_of(smp, s)
                if kind != "choice": continue
                ab = M.choice_plan(smp, s).gold_abstain
                spec = p.sample(s, smp)
                ans = p.solve_a(spec)
                ms = p.matched_models(spec, ans)
            except Exception:
                continue
            shown = {m.fn(spec) for m in ms.values()} - {None, M.NONE_KEY}
            if ab:
                na += 1; cntA.append(len(shown))
                for a in shown: A[M.line_profile(a)] += 1
            else:
                nl += 1; G[M.line_profile(ans)] += 1
                for a in shown - {ans}: W[M.line_profile(a)] += 1
    nG, nA, nW = sum(G.values()), sum(A.values()), sum(W.values())
    names = ["star", "dollar", "q", "cap", "ext", "slash", "digit", "allow"]
    print("rows no-line", na, "line", nl, "mean shown no-line", sum(cntA) / max(1, len(cntA)))
    for i, n in enumerate(names):
        f = lambda C, N: sum(c for k, c in C.items() if k[i]) / N
        print(f"{n:7s} gold {f(G,nG):.3f} no-line {f(A,nA):.3f} wrong {f(W,nW):.3f}")
    keys = set(G) | set(A); print("TV(gold,no-line)", round(0.5 * sum(abs(G[k] / nG - A[k] / nA) for k in keys), 3),
                                  "TV(gold,wrong)", round(0.5 * sum(abs(G[k] / nG - W[k] / nW) for k in set(G) | set(W)), 3))
