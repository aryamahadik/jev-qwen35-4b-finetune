"""G12 dedup (independent F1 checker). (1) exact hash of the model-visible row (card + instructions + state + options)
-> 0 duplicates; (2) MinHash LSH near-dups (datasketch, 128 perms, word 5-shingles of the state text, Jaccard >= 0.9)
-> pairs listed by kind (same unit / same contrast set / other); (3) structure hash: one surface form per structure
except planned twins and format variants (same group_id). Run over candidates_r1 + qc_sample + mixdev_S5 jointly
(cross-file overlap reported). Counts only."""
import hashlib, json, re, time
from collections import defaultdict, Counter
from datasketch import MinHash, MinHashLSH
import qc_lib as q

T0 = time.time()
FILES = ("candidates_r1", "qc_sample", "mixdev_S5")
rows = []
for f in FILES:
    rr, _ = q.load(f)
    rows += [(f, r) for r in rr]
print("rows", len(rows), flush=True)
norm = lambda s: " ".join(s.split()).lower()
exact = defaultdict(list)
for f, r in rows:
    h = hashlib.sha256(norm(q.full_text(r) + "\n" + "\n".join(r["options"] or [])).encode()).hexdigest()
    exact[h].append((f, r["id"]))
ex_dup = [v for v in exact.values() if len(v) > 1]
# structure hash collisions outside the row's own group
sh = defaultdict(list)
for f, r in rows:
    sh[r["meta"]["structure_hash"]].append((f, r["id"], r["group_id"]))
sh_bad = [v for v in sh.values() if len({g for _, _, g in v}) > 1]
sh_kinds = Counter(tuple(sorted({f for f, _, _ in v})) for v in sh_bad)
print("exact/struct done", round(time.time() - T0, 1), flush=True)
TOK = re.compile(r"[a-z0-9]+")
lsh = MinHashLSH(threshold=0.9, num_perm=128)
mh = {}
for n, (f, r) in enumerate(rows):
    t = TOK.findall(r["state"].lower()); m = MinHash(num_perm=128)
    for i in range(max(1, len(t) - 4)):
        m.update(" ".join(t[i:i + 5]).encode())
    key = f"{f}|{r['id']}"; mh[key] = m; lsh.insert(key, m)
    if n % 3000 == 0:
        print("minhash", n, round(time.time() - T0, 1), flush=True)
by = {f"{f}|{r['id']}": r for f, r in rows}
pairs = set()
for k, m in mh.items():
    for o in lsh.query(m):
        if o != k:
            pairs.add(tuple(sorted((k, o))))
kinds = Counter()
for a, b in pairs:
    ra, rb = by[a], by[b]
    fa, fb = a.split("|")[0], b.split("|")[0]
    if ra["group_id"] == rb["group_id"]:
        kinds["same_group (twins / unit / format variant)"] += 1
    elif ra["meta"]["card_id"] == rb["meta"]["card_id"]:
        kinds[f"same_card_diff_group:{fa}~{fb}"] += 1
    else:
        kinds[f"diff_card:{fa}~{fb}"] += 1
out = {"gate": "G12", "files": FILES, "rows": len(rows), "exact_duplicate_groups": len(ex_dup),
       "exact_duplicate_rows": sum(len(v) for v in ex_dup),
       "structure_hash_collisions_across_groups": len(sh_bad), "structure_collision_file_sets": {"+".join(k): v for k, v in sh_kinds.items()},
       "minhash_pairs_ge_0.9": len(pairs), "minhash_pair_kinds": dict(kinds)}
near_bad = sum(v for k, v in kinds.items() if not k.startswith("same_group"))
out["near_dup_pairs_outside_group"] = near_bad
out["pass"] = len(ex_dup) == 0 and len(sh_bad) == 0 and near_bad == 0
out["seconds"] = round(time.time() - T0, 1)
(q.QC / "g12.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out))
