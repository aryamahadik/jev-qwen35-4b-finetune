"""T28 i1 diagnostic: G10 gold-is-longest contributions by question form and role (in memory)."""
import sys, collections
sys.dont_write_bytecode = True
sys.path.insert(0, ".")
import pilot, pilot_loaders as PL
from collections import defaultdict
n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
with PL.open_family("T28") as kit:
    b = pilot.build_pilot(kit, n, log=None, run_g15=False)
d = defaultdict(lambda: [0.0, 0.0, 0])
T = [0.0, 0.0, 0]
for i in b.infos:
    r = i.row
    if r["qtype"] != "choice":
        continue
    o = r["options"]; lens = [len(x) for x in o]; top = [j for j, x in enumerate(lens) if x == max(lens)]
    gi = o.index(r["gold"]); hit = (1 / len(top)) if gi in top else 0.0
    for key in (r["meta"]["qform"], "ROLE:" + r["role"] + "|" + r["meta"]["qform"]):
        d[key][0] += hit; d[key][1] += 1 / len(o); d[key][2] += 1
    T[0] += hit; T[1] += 1 / len(o); T[2] += 1
for q, v in sorted(d.items()):
    print(f"{q:28s} n={v[2]:4d} hit={v[0]:7.2f} exp={v[1]:7.2f} pp={100*(v[0]-v[1])/v[2]:7.2f}  contrib_pp_of_all={100*(v[0]-v[1])/T[2]:6.2f}")
print("ALL", T[2], round(100 * (T[0] - T[1]) / T[2], 2))
