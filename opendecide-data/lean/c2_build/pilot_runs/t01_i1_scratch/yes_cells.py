import sys, json, collections
sys.path.insert(0, '.')
import pilot, pilot_loaders as PL
import negcount
from scipy.stats import binomtest
n = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
with PL.open_family("T01") as kit:
    b = pilot.build_pilot(kit, n, run_g15=False, log=lambda m: None)
    g = pilot.g10(b.infos, b.units, kit.plugin)
    c = g["checks"]["yes_rate_cells"]
    print(json.dumps(c, indent=1)[:2500])
    # per-form yes rates and overall by qform
    yn = [i for i in b.infos if i.row["qtype"] == "noul"]
    per = collections.defaultdict(list)
    for i in yn:
        per[i.row["meta"]["qform"]].append(int(i.row["gold"]))
    for q, v in sorted(per.items()):
        print("%-20s n=%4d yes %.3f" % (q, len(v), sum(v) / len(v)))
    cells = collections.defaultdict(list)
    for i in yn:
        cells[(i.row["meta"]["wording_id"], negcount.count(i.question).k_all)].append(int(i.row["gold"]))
    ps = sorted((binomtest(sum(v), len(v), 0.5).pvalue, k, len(v), sum(v)) for k, v in cells.items() if len(v) >= 8)
    print("cells", len(cells), "smallest p:", ps[:6])
