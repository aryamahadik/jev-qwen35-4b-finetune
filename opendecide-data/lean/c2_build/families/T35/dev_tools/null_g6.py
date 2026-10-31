"""Permutation null of the pilot's choice G6 (argv: n_perm): the pilot's 303 choice rows, gold re-drawn within each row."""
import json
import random
import sys
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(C2))
import numpy as np  # noqa: E402
import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402


class _I:
    def __init__(self, row, q, c, rr):
        self.row, self.question, self.context, self.rr = row, q, c, rr


with PL.open_family("T35") as kit:
    b = PI.build_pilot(kit, 1000, seed_base=PI.SEED_BASE, run_g15=False)
    ch = [i for i in b.infos if i.row["qtype"] == "choice"]
    obs = PI.g6_choice(ch)
    res = {v: {"lr": [], "gbt": []} for v in ("a_question", "b_options", "c_card_without_question", "d_meta")}
    for t in range(int(sys.argv[1])):
        rnd = random.Random(t)
        out = PI.g6_choice([_I({**i.row, "gold": rnd.choice(i.row["options"])}, i.question, i.context, i.rr) for i in ch])
        for v in res:
            for m in ("lr", "gbt"):
                res[v][m].append(out[v][m])
    print("observed", json.dumps(obs))
    print("null (mean, sd, max)", json.dumps({v: {m: (round(float(np.mean(a)), 3), round(float(np.std(a)), 3), round(max(a), 3))
                                                     for m, a in d.items()} for v, d in res.items()}))
    print("null draws passing all 8 views:", sum(all(res[v][m][t] <= obs["chance"] + 0.02 for v in res for m in res[v])
                                                for t in range(int(sys.argv[1]))), "of", sys.argv[1])
