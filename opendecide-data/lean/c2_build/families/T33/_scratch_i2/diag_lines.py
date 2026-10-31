import sys
from pathlib import Path
from collections import Counter, defaultdict
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import pilot_loaders as PL
c = defaultdict(Counter)
with PL.open_family("T33") as kit:
    pl = kit.plugin
    for s in ("S1", "S2", "S3", "S4", "S5"):
        for seed in range(900000, 900000 + 1500):
            sp = pl.sample(seed, s)
            c[len(sp.structure["steps"])][len(sp.structure["lines"])] += 1
for n in sorted(c):
    t = sum(c[n].values())
    print(n, t, {k: round(v / t, 3) for k, v in sorted(c[n].items())})
