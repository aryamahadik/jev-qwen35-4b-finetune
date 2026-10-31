"""Dev tool (A45 d, T35 pass 3): profile of error-model outputs by model on no-line vs line rows. argv: seed0 seed1"""
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
    A = collections.defaultdict(lambda: [0, 0]); G = [0, 0]; W = [0, 0]; nab = 0; nl = 0
    for s in range(s0, s1):
        for smp in ("S1", "S2", "S3", "S4"):
            try:
                kind, idx = M.slot_of(smp, s)
                if kind != "choice": continue
                ab = M.choice_plan(smp, s).gold_abstain
                spec = p.sample(s, smp)
            except Exception:
                continue
            outs = {n: m.fn(spec) for n, m in p.error_models().items()}
            if ab:
                nab += 1
                for n, a in outs.items():
                    if a in (None, M.NONE_KEY) or len(a.split(":", 1)[1]) < M.MIN_PATTERN: continue
                    A[n][0] += a.endswith("$"); A[n][1] += 1
            else:
                nl += 1
                ans = p.solve_a(spec)
                G[0] += ans.endswith("$"); G[1] += 1
                for n, a in outs.items():
                    if a in (None, M.NONE_KEY, ans) or len(a.split(":", 1)[1]) < M.MIN_PATTERN: continue
                    W[0] += a.endswith("$"); W[1] += 1
    print("rows abstain", nab, "line", nl)
    for n, (d, t) in sorted(A.items()): print(f"  abs {n:35s} {d}/{t}")
    print("gold $", G, "wrong cands $", W)
