import sys
from pathlib import Path
from collections import defaultdict
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import numpy as np, pilot_loaders as PL
g = defaultdict(list)
with PL.open_family("T33") as kit:
    pl = kit.plugin
    for s in ("S1", "S2", "S3", "S4", "S5"):
        for seed in range(900000, 900000 + 2500):
            sp = pl.sample(seed, s)
            if sp.qform != "ch_failed_check":
                continue
            st = sp.structure
            vec, checks = st["intent"]["checks"], st["checks"]
            ff = next((i for i, v in enumerate(vec) if not v), None)
            gold = "none" if ff is None else checks[ff]
            lines = st["lines"]
            tries = sum(1 for l in lines if l["kind"] == "try") if lines else 0
            polls = sum(1 for l in lines if l["kind"] == "poll")
            jobs = sum(1 for l in lines if l.get("job"))
            g[gold].append((len(lines), tries, polls, jobs, len(st["steps"]), int("crit.max_tries" in checks)))
for k, v in sorted(g.items()):
    a = np.mean(v, axis=0)
    print("G", k, len(v), [round(float(x), 2) for x in a], "(lines,tries,polls,jobs,steps,tries_listed)")
