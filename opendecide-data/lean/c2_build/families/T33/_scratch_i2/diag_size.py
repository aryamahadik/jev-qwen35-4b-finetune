"""Scratch: card-size features by gold type per choice qform (report only)."""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import numpy as np
import pilot, pilot_loaders as PL
from collections import defaultdict
with PL.open_family("T33") as kit:
    b = pilot.build_pilot(kit, 6000, run_g15=False)
g = defaultdict(list)
for i in b.infos:
    r = i.row
    if r["qtype"] != "choice":
        continue
    cat, num = pilot.meta_features(i)
    kinds = pilot.option_kinds(i)
    gk = [k for o, k in zip(r["options"], kinds) if o == r["gold"]][0]
    typ = "abstain" if "kind:abstain" in gk else "other"
    g[(cat["qform"], typ)].append(dict(num, nsteps=len(i.row["meta"].get("steps", []) or [])))
for key in sorted(g):
    v = g[key]
    print(key, len(v), {f: round(float(np.mean([x[f] for x in v])), 2) for f in ("n_lines", "len_state", "n_numbers", "k", "len_card", "depth", "mag_max")})
