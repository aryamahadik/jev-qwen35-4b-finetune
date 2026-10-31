"""Simulate trainer steps (batches + _micro_groups + real token lengths) for a block composition. Counts only."""
from lib import *
import glob, time, statistics as st
from collections import defaultdict, Counter
SC = LEAN + "/c_src/"
FAM = {"F1": 5400, "F2": 3150, "F3": 4500, "F4": 3600, "F5": 3600, "F6": 3600, "F7": 3150, "F8": 2250, "F9": 4050,
       "F10": 3600, "F11": 3600, "F12": 2700, "F13": 2225}
QUOTA = {"replay": 90000, **FAM, "public": 8575, "commit": 6000}

def by_call(rows):
    u = defaultdict(list)
    for r in rows: u[r["call_id"]].append(r)
    return list(u.values())

def pool(block):
    if block == "replay":
        rows = [r for f in sorted(glob.glob(LEAN + "/data/c_replay_r1_shards/shard_*.jsonl")) for r in read_jsonl(f)]
    elif block == "public":
        rows = [r for f in ("public-1/out/public1_rows_r1.jsonl", "public-2/out/rows_r1.jsonl", "public-3/out/public3_rows_r1.jsonl")
                for r in read_jsonl(SC + "public/" + f)]
    elif block == "commit":
        rows = read_jsonl(SC + "COMMIT/out/candidates_r1.jsonl")
    else:
        rows = read_jsonl(SC + block + "/out/candidates_r1.jsonl")
    return rows

def lengths(rows):
    out = {}
    for i in range(0, len(rows), 256):
        ch = rows[i:i + 256]
        for r, n in zip(ch, ntok([prompt(r, None) for r in ch])): out[r["id"]] = n
    return out

def draw(units, n_rows, rng):
    u = units[:]; rng.shuffle(u); got, k = [], 0
    while k < len(u) and sum(len(x) for x in got) < n_rows:
        got.append(u[k]); k += 1
    return got

def simulate(units, lens, n_steps, seed, budget=8192, perm_twin=0.3):
    rnd = random.Random(seed); units = units[:]
    uid = {r["id"]: k for k, u in enumerate(units) for r in u}
    rnd.shuffle(units); feats = []; cur = []
    it = iter(units)
    while len(feats) < n_steps:
        try: u = next(it)
        except StopIteration:
            rnd.shuffle(units); it = iter(units); continue
        cur.extend(u)
        if len(cur) >= 16:
            tw = [(i, None) for i, r in enumerate(cur) if r["qtype"] == "choice" and len(r["options"]) > 1 and rnd.random() < perm_twin]
            feats.append(step_feats(cur, [None] * len(cur), tw, uid, budget, False, lens)); cur = []
    return feats

def summ(feats):
    return {k: round(st.mean(f[k] for f in feats), 1) for k in ("rows", "twins", "n_seq", "n_micro", "pad_tok", "real_tok", "max_len")}
