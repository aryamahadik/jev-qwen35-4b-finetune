"""Independent real-mix simulation from cached token lengths (pool_*.json). CPU only, counts only."""
import json, sys, random, statistics as st
from collections import defaultdict, Counter
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean")
import train_decoder as td
import decoder_io

QUOTA = {"replay": 90000, "F1": 5400, "F2": 3150, "F3": 4500, "F4": 3600, "F5": 3600, "F6": 3600, "F7": 3150,
         "F8": 2250, "F9": 4050, "F10": 3600, "F11": 3600, "F12": 2700, "F13": 2225, "public": 8575, "COMMIT": 6000}
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 424242
NSTEP = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
MODE = sys.argv[3] if len(sys.argv) > 3 else "quota"
rng = random.Random(SEED)
td._est_tokens = lambda r: r["est"]          # runtime patch in this scratch process only (packing uses the cached estimate)

rows, rels, LEN, BLK = [], [], {}, {}
POOLS, TAKE, RELS = {}, {}, {}
split_rel = Counter()
for b, q in QUOTA.items():
    P = json.load(open(f"pool_{b}.json"))
    R = {r["id"]: r for r in P["rows"] if P["len"][r["id"]] <= 7900}
    cid = {i: r["call_id"] for i, r in R.items()}
    for x in P["rels"]:
        if x["type"] != "inv" and x["a"] in cid and x["b"] in cid and cid[x["a"]] != cid[x["b"]]:
            split_rel[b] += 1
    # selection units: call_id + every relation (closure), as the mixer keeps whole relation units
    par = {}
    def f(k):
        while par.get(k, k) != k:
            k = par[k]
        return k
    for x in P["rels"]:
        if x["a"] in R and x["b"] in R:
            a, c = f(cid[x["a"]]), f(cid[x["b"]])
            if a != c:
                par[c] = a
    U = defaultdict(list)
    for i, r in R.items():
        U[f(r["call_id"])].append(i)
    keys = sorted(U)
    rng.shuffle(keys)
    take, n = set(), 0
    POOLS[b] = (U, keys, R, P["len"])
    for k in keys:
        if n >= q:
            break
        take.update(U[k]); n += len(U[k])
    TAKE[b] = take
    RELS[b] = P["rels"]

if MODE == "cap":
    def islong(b, k): return any(POOLS[b][3][i] >= 2000 for i in POOLS[b][0][k])
    newb = [b for b in QUOTA if b != "replay"]
    sel = {b: [k for k in POOLS[b][1] if set(POOLS[b][0][k]) <= TAKE[b]] for b in newb}
    longn = {b: sum(len(POOLS[b][0][k]) for k in sel[b] if islong(b, k)) for b in newb}
    keep = 0.09 * sum(QUOTA[b] for b in newb) / sum(longn.values())
    deficit = 0
    for b in newb:
        U, keys, R, LN = POOLS[b]
        lk = [k for k in sel[b] if islong(b, k)]
        drop = lk[int(round(len(lk) * keep)):]
        t = set(TAKE[b])
        for k in drop:
            t -= set(U[k])
        spare = [k for k in keys if not islong(b, k) and not (set(U[k]) & TAKE[b])]
        while len(t) < QUOTA[b] and spare:
            t |= set(U[spare.pop()])
        deficit += max(0, QUOTA[b] - len(t))
        TAKE[b] = t
    fam = [b for b in newb if b.startswith("F") and b != "F13"]
    j = 0
    while deficit > 0:
        b = fam[j % len(fam)]; j += 1
        U, keys, R, LN = POOLS[b]
        spare = [k for k in keys if not islong(b, k) and not (set(U[k]) & TAKE[b])]
        if spare:
            TAKE[b] |= set(U[spare[0]]); deficit -= len(U[spare[0]])
    print("cap mode: kept long fraction %.3f" % keep, {b: len(TAKE[b]) for b in newb})
for b in QUOTA:
    U, keys, R, LN = POOLS[b]
    take = TAKE[b]
    for i in take:
        r = R[i]
        rows.append({"id": i, "call_id": r["call_id"], "qtype": r["qtype"], "options": list(range(r["nopt"])),
                     "est": r["est"], "ord": r["ord"]})
        LEN[i] = LN[i]; BLK[i] = b
    rels += [x for x in RELS[b] if x["a"] in take and x["b"] in take]

new = [r for r in rows if BLK[r["id"]] != "replay"]
tn = sum(LEN[r["id"]] for r in new)
lr = [r for r in new if LEN[r["id"]] >= 2000]
print("rows", len(rows), "rels", len(rels), "mean tok/row %.0f" % (sum(LEN.values()) / len(LEN)),
      "| new rows: long(>=2000) row share %.3f token share %.3f" % (len(lr) / len(new), sum(LEN[r["id"]] for r in lr) / tn))
print("non-inv relations across call_ids (pool):", dict(split_rel))
bt = Counter(); bn = Counter()
for i, b in BLK.items():
    bt[b] += LEN[i]; bn[b] += 1
T = sum(bt.values())
print("tok/row by block:", {b: round(bt[b] / bn[b]) for b in QUOTA}, "token share replay %.2f F13 %.3f" % (bt["replay"] / T, bt["F13"] / T))

units, merged = td.make_units(rows, rels)
uid = {r["id"]: k for k, u in enumerate(units) for r in u}
rbr = defaultdict(list)
for x in rels:
    rbr[x["a"]].append(x)
random.seed(SEED)
twin_rng = random.Random(SEED + 1)
gen = td.batches(units, 16)
CFG = [(4096, 64), (4096, 256), (6144, 256), (8192, 64), (8192, 256), (10240, 256), (12288, 256)]
acc = defaultdict(list)
for step in range(NSTEP):
    b = next(gen)
    perms = [random.sample(range(len(r["options"])), len(r["options"])) if r["qtype"] == "choice"
             else random.sample([0, 1], 2) for r in b]
    tw = td.pick_twins(b, perms, 0.3, twin_rng)
    tl = defaultdict(list)
    for i, r in enumerate(b):
        tl[i].append(LEN[r["id"]])
    for i, _ in tw:
        tl[i].append(LEN[b[i]["id"]])
    acc["rows"].append(len(b)); acc["twins"].append(len(tw))
    acc["real"].append(sum(sum(v) for v in tl.values()))
    pos = {r["id"]: i for i, r in enumerate(b)}
    for B, Pm in CFG:
        decoder_io.PAD_MULTIPLE = Pm
        g = td._micro_groups(b, uid, tw, B)
        pad = 0
        gi = {}
        for k, idx in enumerate(g):
            seq = [l for i in idx for l in tl[i]]
            pad += len(seq) * (-(-max(seq) // Pm) * Pm)
            for i in idx:
                gi[i] = k
        sp = sum(1 for r in b for x in rbr.get(r["id"], []) if x["b"] in pos and gi[pos[x["a"]]] != gi[pos[x["b"]]])
        acc[f"pad{B}_{Pm}"].append(pad); acc[f"nmb{B}_{Pm}"].append(len(g)); acc[f"split{B}_{Pm}"].append(sp)
    decoder_io.PAD_MULTIPLE = 256
res = {k: round(st.mean(v), 3) for k, v in acc.items() if not k.startswith("split")}
res.update({k: sum(v) for k, v in acc.items() if k.startswith("split")})
print(json.dumps(res))
json.dump(res, open(f"sim_{SEED}_{MODE}.json", "w"))
