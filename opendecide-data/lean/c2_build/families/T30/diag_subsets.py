"""families/T30/diag_subsets.py: G6 excess over pilot-size subsets of one large build (in memory; prints only)."""
import collections
import random
import sys
import time
from pathlib import Path

import numpy as np

sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
if str(C2) not in sys.path:
    sys.path.insert(0, str(C2))
import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402

base, nbuild, reps = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
with PL.open_family("T30") as kit:
    b = PI.build_pilot(kit, nbuild, seed_base=base, run_g15=False, log=None)
    units = collections.defaultdict(list)
    for i in b.infos:
        units[i.unit].append(i)
    ids = list(units)
    rng = random.Random(5)
    res = collections.defaultdict(list)
    t0 = time.time()
    for rep in range(reps):
        rng.shuffle(ids)
        sel, n = [], 0
        for u in ids:
            sel += units[u]
            n += len(units[u])
            if n >= 1000:
                break
        yn = [i for i in sel if i.row["qtype"] == "noul"]
        ch = [i for i in sel if i.row["qtype"] == "choice"]
        a, c = PI.g6_yes_no(yn), PI.g6_choice(ch)
        for v in ("a_question", "c_card_without_question", "d_meta"):
            for m in ("lr", "gbt"):
                res[("yn", v, m)].append(a[v][m] - 0.5)
        for v in ("a_question", "b_options", "c_card_without_question", "d_meta"):
            for m in ("lr", "gbt"):
                res[("ch", v, m)].append(c[v][m] - c["chance"])
        print("rep", rep, round(time.time() - t0), flush=True)
    for k, v in res.items():
        print(k, "mean excess %.4f sd %.4f P(excess>0.02) %.2f" % (np.mean(v), np.std(v), np.mean([x > 0.02 for x in v])))
    n = len(res[("yn", "a_question", "lr")])
    print("all-pass fraction", sum(all(res[k][j] <= 0.02 for k in res) for j in range(n)), n)
