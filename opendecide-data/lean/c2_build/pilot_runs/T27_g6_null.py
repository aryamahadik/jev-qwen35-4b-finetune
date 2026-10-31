"""T27 diagnostic (not a gate): the pilot's choice G6 under permuted golds (each choice row's gold replaced by a uniformly
random option), at the dumped rows' n: the null distribution of every view / model accuracy. In memory only."""
import copy, json, random, sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, ".")
import pilot
path, T = sys.argv[1], int(sys.argv[2])
rows = [json.loads(l) for l in open(path)]
ch = [r for r in rows if r["qtype"] == "choice"]
def info(r):
    rules, _, q = r["instructions"].rpartition("\n\n")
    ctx = "\n".join(x for x in (r.get("card") or "", rules, r["state"]) if x.strip())
    return pilot.RowInfo(r, None, None, 0, q, ctx, None)
base = pilot.g6_choice([info(r) for r in ch])
print("REAL", json.dumps({k: v for k, v in base.items() if k not in ("n",)}), flush=True)
rng = random.Random(7)
out = []
for t in range(T):
    t0 = time.time()
    rr = []
    for r in ch:
        r2 = copy.deepcopy(r)
        r2["gold"] = rng.choice(r2["options"])
        rr.append(r2)
    res = pilot.g6_choice([info(r) for r in rr])
    row = {v: res[v] for v in ("a_question", "b_options", "c_card_without_question", "d_meta")}
    out.append(row)
    print(t, round(time.time() - t0), json.dumps(row), flush=True)
