"""G12 cross-check, hash only (counts printed, never row text): DI-TS candidates + own dev vs (a) C2 dev/eval files (mixdev_S5 of every family, c2_transfer_dev),
(b) C2 replay shards and C1 replay shards. Exact normalised state hash, and word-3-gram Jaccard >= 0.9 against dev/eval files. Usage: python -I dedupe_vs_c2.py <lean_dir> <di_train_dir>"""
import sys, glob, json, re, hashlib
LEAN, D = sys.argv[1], sys.argv[2]
norm = lambda s: re.sub(r"\s+", " ", s.lower()).strip()
h = lambda s: hashlib.sha256(s.encode()).hexdigest()[:20]
def shingles(s):
    w = norm(s).split(); return frozenset(" ".join(w[i:i+3]) for i in range(max(1, len(w)-2)))
mine = []
for f in ("candidates_stage.jsonl", "mixdev_S5_stage.jsonl"):
    for l in open(f"{D}/DI-TS/stage/{f}", encoding="utf8"):
        r = json.loads(l); mine.append((r["id"], f, norm(r["state"]), r))
byhash = {}
for i, f, st, r in mine: byhash.setdefault(h(st), []).append(i)
bysh = {i: shingles(r["state"]) for i, f, st, r in mine}
hits = {"exact_dev_eval": set(), "near_dev_eval": set(), "exact_replay_c1": set()}
files = sorted(glob.glob(f"{LEAN}/data/c2_parts/*/out/mixdev_S5.jsonl")) + [f"{LEAN}/data/c2_transfer_dev.jsonl", f"{LEAN}/data/dev.jsonl"]
# inverted index of my shingles for the near check
inv = {}
for i, sh in bysh.items():
    for s in sh: inv.setdefault(s, set()).add(i)
n_ref = 0
for f in files:
    for l in open(f, encoding="utf8"):
        try: r = json.loads(l)
        except Exception: continue
        st = r.get("state")
        if not isinstance(st, str): continue
        n_ref += 1
        for i in byhash.get(h(norm(st)), []): hits["exact_dev_eval"].add(i)
        sh = shingles(st); cand = {}
        for s in sh:
            for i in inv.get(s, ()): cand[i] = cand.get(i, 0) + 1
        for i, c in cand.items():
            if c / max(1, len(sh | bysh[i])) >= 0.9 * 0 + 0.9 and len(sh & bysh[i]) / len(sh | bysh[i]) >= 0.9: hits["near_dev_eval"].add(i)
n_rep = 0
for f in sorted(glob.glob(f"{LEAN}/data/c2_replay_shards/*.jsonl")) + sorted(glob.glob(f"{LEAN}/data/c_replay_r1_shards/*.jsonl")) + sorted(glob.glob(f"{LEAN}/data/c2_crowd_shards/*.jsonl")) + sorted(glob.glob(f"{LEAN}/data/c_crowd_r1_shards/*.jsonl")):
    for l in open(f, encoding="utf8"):
        m = re.search(r'"state": "((?:[^"\\]|\\.)*)"', l)
        if not m: continue
        n_rep += 1
        try: st = json.loads('"' + m.group(1) + '"')
        except Exception: continue
        for i in byhash.get(h(norm(st)), []): hits["exact_replay_c1"].add(i)
out = {"my_rows": len(mine), "dev_eval_rows_compared": n_ref, "replay_c1_rows_compared": n_rep, "files": len(files), **{k: len(v) for k, v in hits.items()}, "hit_ids": {k: sorted(v) for k, v in hits.items()}}
json.dump(out, open(f"{D}/DI-TS/stage/DEDUPE_VS_C2.json", "w"), indent=1)
print({k: v for k, v in out.items() if k != "hit_ids"})
