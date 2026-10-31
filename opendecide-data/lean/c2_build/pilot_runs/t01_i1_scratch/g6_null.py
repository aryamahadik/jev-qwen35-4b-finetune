"""T01 scratch: G6 choice permutation null at pilot size (gold permuted within each row). Report only."""
import sys, copy, random
sys.path.insert(0, '.')
import pilot, pilot_loaders as PL
import numpy as np
mod = sys.argv[1] if len(sys.argv) > 1 else "T01"
reps = int(sys.argv[2]) if len(sys.argv) > 2 else 10
with PL.open_family(mod) as kit:
    b = pilot.build_pilot(kit, 1000, run_g15=False, log=lambda m: None)
    infos = b.infos
    ch = [i for i in infos if i.row["qtype"] == "choice"]
    yn = [i for i in infos if i.row["qtype"] == "noul"]
    rng = random.Random(7)
    print("n choice", len(ch), "n yn", len(yn), flush=True)
    mx = []
    for t in range(reps):
        sh = []
        for i in ch:
            j = copy.copy(i); r = dict(i.row); r["gold"] = rng.choice(r["options"]); j.row = r; sh.append(j)
        r = pilot.g6_choice(sh)
        d = {v: max(r[v].values()) - r["chance"] for v in ("a_question", "b_options", "c_card_without_question", "d_meta")}
        mx.append(max(d.values()))
        print(t, {k: round(v, 4) for k, v in d.items()}, flush=True)
    print("choice null: max-view minus chance mean %.4f max %.4f share>0.02 %.2f" % (np.mean(mx), max(mx), np.mean([m > 0.02 for m in mx])), flush=True)
    mxy = []
    for t in range(reps):
        sh = []
        for i in yn:
            j = copy.copy(i); r = dict(i.row); r["gold"] = rng.randint(0, 1); j.row = r; sh.append(j)
        r = pilot.g6_yes_no(sh)
        d = {v: max(r[v].values()) - 0.5 for v in ("a_question", "c_card_without_question", "d_meta")}
        mxy.append(max(d.values()))
        print("yn", t, {k: round(v, 4) for k, v in d.items()}, flush=True)
    print("yn null: max-view minus 0.5 mean %.4f max %.4f share>0.02 %.2f" % (np.mean(mxy), max(mxy), np.mean([m > 0.02 for m in mxy])), flush=True)
