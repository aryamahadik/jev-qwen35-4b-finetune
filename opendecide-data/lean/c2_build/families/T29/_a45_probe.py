"""Scratch probe (iteration 4): P(requested effect | gold verdict) and sample() speed over base specs."""
import sys, time
from collections import Counter
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import pilot_loaders as PL  # noqa: E402
n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
with PL.open_family("T29") as kit:
    P = kit.plugin
    c, t0, fail = Counter(), time.time(), 0
    for i in range(n):
        smp = P.SAMPLERS[i % len(P.SAMPLERS)]
        try:
            sp = P.sample(900000 + i, smp)
        except Exception as e:  # noqa: BLE001
            fail += 1; continue
        if sp.qform.startswith("yn"):
            g = "yes" if P.solve_a(sp) else "no"; g = (sp.qform in ("yn_go",)) and g  # noqa
        v = P._verdict_c(P._rule_truths(sp), P._confirmed_c(sp))
        c[(v, sp.slots["EFFECT"].value if hasattr(sp.slots["EFFECT"], "value") else str(sp.slots["EFFECT"].params))] += 1
    print("sec", round(time.time() - t0), "fail", fail, "samplers", P.SAMPLERS)
    effs = sorted({k[1] for k in c})
    for v in ("go", "ask", "refuse", "cannot"):
        tot = sum(c[(v, e)] for e in effs)
        print(v, tot, [round(c[(v, e)] / max(tot, 1), 2) for e in effs])
    print(effs)
