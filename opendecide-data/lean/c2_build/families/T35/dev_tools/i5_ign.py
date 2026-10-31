import sys, collections
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2])); sys.path.insert(0, str(HERE.parent))
import pilot_loaders as PL, run_pilot_i4 as R
R.install_loader()
with PL.open_family("T35") as kit:
    p = kit.plugin; M = sys.modules[type(p).__module__]
    n = 0
    for s in range(900000, 900300):
        smp = "S1"
        try:
            kind, idx = M.slot_of(smp, s)
            if kind != "choice" or not M.choice_plan(smp, s).gold_abstain: continue
            spec = p.sample(s, smp)
        except Exception: continue
        a = p.error_models()["robots_ignore_end_anchor"].fn(spec)
        env = spec.env()
        if a in (None, M.NONE_KEY): continue
        print(M.raw_path(env["URL"]), "|", a, "|", [M.line_key(env, x) for g in spec.structure["groups"] for x in g["lines"]])
        n += 1
        if n > 10: break
