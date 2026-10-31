"""T28 i1 diagnostic: the pilot's choice G6 under permuted golds (each choice row's gold replaced by a uniformly random
option): the null distribution of every view / model accuracy minus chance, at the pilot's n. In memory only."""
import copy, random, statistics, sys
sys.dont_write_bytecode = True
sys.path.insert(0, ".")
import pilot, pilot_loaders as PL
T = int(sys.argv[1]) if len(sys.argv) > 1 else 10
with PL.open_family("T28") as kit:
    b = pilot.build_pilot(kit, 1000, log=None, run_g15=False)
ch = [i for i in b.infos if i.row["qtype"] == "choice"]
real = pilot.g6_choice(ch)
print("real", {k: v for k, v in real.items() if k not in ("n",)})
acc = {}
for t in range(T):
    rng = random.Random(t)
    fake = []
    for i in ch:
        j = copy.copy(i)
        j.row = dict(i.row)
        j.row["gold"] = rng.choice(i.row["options"])
        fake.append(j)
    r = pilot.g6_choice(fake)
    for v in ("a_question", "b_options", "c_card_without_question", "d_meta"):
        for m in ("lr", "gbt"):
            acc.setdefault((v, m), []).append(r[v][m] - r["chance"])
for k, v in acc.items():
    print(k, "null mean %.4f sd %.4f max %.4f" % (statistics.mean(v), statistics.pstdev(v), max(v)))
