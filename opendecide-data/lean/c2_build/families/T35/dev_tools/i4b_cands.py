import sys, collections
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2])); sys.path.insert(0, str(HERE.parent))
import pilot_loaders as PL, run_pilot_i4 as R
R.install_loader()
import plugin as P
with PL.open_family("T35") as kit:
    p = kit.plugin; M = sys.modules[type(p).__module__]
    shown = 0; dol = collections.Counter(); tot = collections.Counter()
    for s in range(900000, 900400):
        smp = "S1"
        try:
            kind, idx = M.slot_of(smp, s)
            if kind != "choice" or not M.choice_plan(smp, s).gold_abstain: continue
            spec = p.sample(s, smp)
        except Exception as e:
            continue
        ms = p.matched_models(spec, p.solve_a(spec))
        outs = {n: m.fn(spec) for n, m in p.error_models().items()}
        cands = {a for a in outs.values() if a not in (None, M.NONE_KEY) and len(a.split(":", 1)[1]) >= M.MIN_PATTERN}
        env = spec.env(); flines = [M.line_key(env, n) for g in spec.structure["groups"] for n in g["lines"]]
        for a in cands:
            tot["cand"] += 1; dol["cand"] += a.split(":",1)[1].endswith("$")
        shown_keys = {m.fn(spec) for m in ms.values()} - {None, M.NONE_KEY}
        for a in shown_keys:
            tot["shown"] += 1; dol["shown"] += a.split(":",1)[1].endswith("$")
        for a in flines:
            tot["file"] += 1; dol["file"] += a.split(":",1)[1].endswith("$")
        if shown < 3:
            shown += 1; print(s, "DP-ish", env["URL"]); print(" file:", flines); print(" cands:", sorted(cands)); print(" shown:", sorted(shown_keys))
    print({k: (dol[k], tot[k]) for k in tot})
