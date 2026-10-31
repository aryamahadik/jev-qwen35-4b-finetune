import sys, json, importlib
from pathlib import Path
sys.dont_write_bytecode = True
C2 = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build'
sys.path.insert(0, C2)
import pilot
from families.T06 import plugin as T
rp = importlib.import_module('families.T06.run_pilot')
N = int(sys.argv[1]); out = sys.argv[2]
if len(sys.argv) > 3: T.TWIN_NONE_KEEP = float(sys.argv[3])
with rp._t06() as kit:
    b = pilot.build_pilot(kit, N, run_g15=False)
rows = []
for i in b.infos:
    if i.row["qtype"] != "choice" or i.row["meta"]["qform"] != "ch_rule":
        continue
    f = T.facts(i.spec)
    pos = f.possession.toordinal()
    ends = {k: e - pos for k, e in T._ends(f).items()}
    rows.append({"gold": i.row["gold"], "opts": i.row["options"], "card": i.row["meta"]["card_id"], "reason": f.reason, "goods": f.goods,
                 "seal": f.seal, "policy": f.policy, "n_rej": f.n_rej, "n_wd": f.n_wd, "p": f.p, "handover": f.handover,
                 "d": (f.requested - f.possession).days, "d_deliv": (f.requested - f.delivered).days, "d_ord": (f.requested - f.ordered).days,
                 "ends": ends, "counts": bool(i.spec.structure["counts"]), "style": f.style, "variant": i.spec.structure.get("card"),
                 "sampler": i.spec.sampler, "state": i.row["state"], "ins": i.row["instructions"], "q": i.question, "ctx": i.context,
                 "twin": bool(i.row["meta"].get("twin_of")), "gold_key": T.T06Plugin.solve_a(kit.plugin, i.spec), "display": list(T._applicable(f))})
Path(out).write_text(json.dumps(rows))
print(len(rows))
