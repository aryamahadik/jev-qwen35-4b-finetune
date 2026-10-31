"""T27 diagnostic: twin transition matrix of ch_next bases (spec level, nothing rendered)."""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, "."); sys.path.insert(0, "families/T27")
import run_pilot as RP
from collections import Counter
N = int(sys.argv[1]) if len(sys.argv) > 1 else 600
with RP._t27() as kit:
    plugin = kit.plugin
    from families.T27 import plugin as P
    tr, nb, emitted = Counter(), Counter(), Counter()
    for smp in ("S1", "S2", "S3", "S4"):
        for seed in range(900000, 900000 + N):
            sp = plugin.sample(seed, smp)
            if sp.qform != "ch_next":
                continue
            b = plugin.solve_a(sp)
            nb[b] += 1
            for rel in plugin.relations(sp):
                if rel.kind == "twin":
                    tr[(b, rel.expect)] += 1
                    emitted[b] += 1
    tw = Counter()
    for (b, t), n in tr.items():
        tw[t] += n
    print("bases", dict(nb)); print("twin transitions", dict(tr)); print("twin labels", dict(tw))
    rows_per_label = Counter()
    # overall label share over (bases + equiv/attack copies ~ 0.27 of bases + twins)
    copies = 0.14 + 0.09
    for b, n in nb.items():
        rows_per_label[b] += n * (1 + copies)
    for t, n in tw.items():
        rows_per_label[t] += n
    tot = sum(rows_per_label.values())
    print({k: round(v / tot, 3) for k, v in rows_per_label.items()})
