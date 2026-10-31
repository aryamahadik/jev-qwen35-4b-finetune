"""Choice rows on DEV seeds (argv: seed_base, n_rows): gold-vs-wrong surface flags of the line options and the G6 choice views."""
import collections
import sys
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(C2))
import numpy as np  # noqa: E402
import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from families.T35 import plugin as P  # noqa: E402

base, n = int(sys.argv[1]), int(sys.argv[2])
assert base != PI.SEED_BASE, "dev seeds only"
with PL.open_family("T35") as kit:
    b = PI.build_pilot(kit, n, seed_base=base, run_g15=False)
    ch = [i for i in b.infos if i.row["qtype"] == "choice"]
    print("choice rows", len(ch), "drops", b.stats["drops_by_gate"])
    names = ("star", "dollar", "query", "upper", "ext", "slash", "digit", "allow")
    gold, wrong = collections.defaultdict(list), collections.defaultdict(list)
    for i in ch:
        for o in i.row["options"]:
            if o == P.NONE_TEXT:
                continue
            key = ("allow:" if o.startswith("Allow") else "disallow:") + o.split(": ", 1)[1]
            for nm, v in zip(names, P.line_profile(key)):
                (gold if o == i.row["gold"] else wrong)[nm].append(float(v))
    print("gold vs wrong line flags", {nm: (round(float(np.mean(gold[nm])), 3), round(float(np.mean(wrong[nm])), 3)) for nm in names})
    r = PI.g6_choice(ch)
    print("G6 choice n", r["n"], "chance", r["chance"], {v: r[v] for v in ("a_question", "b_options", "c_card_without_question", "d_meta")})
