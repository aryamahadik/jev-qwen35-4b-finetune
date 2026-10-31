"""G12 dedup (independent F3 checker). Spec 8 G12 + F3 G0 section 6 (one surface form per structure_hash; the only
exception is an attack twin, which shares its clean row's hash; F3 emits no format-variant rows).
 (1) exact hash of the model-visible row (card, instructions, state, options as a set): 0 duplicates;
 (2) exact hash of normalized (instructions + state) ignoring options and card: reported;
 (3) structure_hash: every hash with > 1 row must be exactly an attack (inv) pair;
 (4) MinHash (datasketch, 128 perms, word 5-gram shingles of question + state) near-duplicates at Jaccard >= 0.8
     between rows of DIFFERENT group_id (rows of one log and its twins are planned near-duplicates); candidates are
     verified with exact shingle Jaccard; gate: 0 verified pairs;
 (5) cross-file: candidates vs mixdev_S5 (spec 10: no shared group_id or normalized text; MinHash too) and candidates
     vs qc_sample (reported).
Usage: g12.py (writes qc/g12_candidates_r1.json)"""
import hashlib, json, re, time
from collections import Counter, defaultdict
from datasketch import MinHash, MinHashLSH
import qc_lib as L

T0 = time.time()
TH = 0.8


def log(m):
    print(f"[{time.time() - T0:7.1f}s] {m}", flush=True)


def norm(s):
    return re.sub(r"\s+", " ", s.strip().lower())


def h(s):
    return hashlib.sha256(s.encode()).hexdigest()


def full_key(r):
    return h(json.dumps([norm(r.get("card") or ""), norm(r["instructions"]), norm(r["state"]),
                         sorted(norm(o) for o in (r["options"] or []))]))


def shingles(r):
    w = re.findall(r"\w+", (L.views(r)["q"] + " " + r["state"]).lower())
    return {" ".join(w[i:i + 5]) for i in range(max(1, len(w) - 4))}


def mh(sh):
    m = MinHash(num_perm=128, seed=1)
    m.update_batch([s.encode() for s in sh])
    return m


def jac(a, b):
    return len(a & b) / max(1, len(a | b))


def near_pairs(rowsA, shA, rowsB=None, shB=None, same_file=True):
    lsh = MinHashLSH(threshold=TH, num_perm=128); MA = []
    for i, s in enumerate(shA):
        m = mh(s); MA.append(m); lsh.insert(str(i), m)
    log(f"lsh built {len(MA)}")
    pairs = []
    if same_file:
        for i, m in enumerate(MA):
            for j in map(int, lsh.query(m)):
                if j > i and rowsA[i]["group_id"] != rowsA[j]["group_id"]:
                    jj = jac(shA[i], shA[j])
                    if jj >= TH:
                        pairs.append([rowsA[i]["id"], rowsA[j]["id"], round(jj, 4)])
    else:
        for k, s in enumerate(shB):
            for j in map(int, lsh.query(mh(s))):
                jj = jac(s, shA[j])
                if jj >= TH:
                    pairs.append([rowsB[k]["id"], rowsA[j]["id"], round(jj, 4)])
    return pairs


def main():
    rows, _ = L.load("candidates_r1"); n = len(rows)
    out = {"gate": "G12", "file": "out/candidates_r1.jsonl", "rows": n, "minhash_threshold": TH}
    fk = Counter(full_key(r) for r in rows)
    out["exact_full_row_duplicates"] = sum(c - 1 for c in fk.values() if c > 1)
    isk = Counter(h(norm(r["instructions"]) + "\x00" + norm(r["state"])) for r in rows)
    out["report_same_instructions_and_state"] = sum(c - 1 for c in isk.values() if c > 1)
    rels = L.load_relations("candidates_r1")
    inv = set()
    for x in rels:
        if x.get("type") == "inv":
            inv.add(frozenset([x["a"], x["b"]]))
    out["relation_types"] = dict(Counter(x.get("type") for x in rels))
    byh = defaultdict(list)
    for r in rows:
        byh[r["meta"]["structure_hash"]].append(r)
    multi = {k: v for k, v in byh.items() if len(v) > 1}
    bad = []
    for k, v in multi.items():
        ids = {r["id"] for r in v}
        ok = len(v) == 2 and any(ids <= s for s in inv) and sum(bool("attack" in (r["meta"].get("edge") or [])) for r in v) == 1
        if not ok:
            bad.append(sorted(ids))
    out["structure_hash"] = {"distinct": len(byh), "hashes_with_gt1_row": len(multi), "of_which_attack_pairs": len(multi) - len(bad),
                             "violations": len(bad), "violation_examples": bad[:10], "inv_relations": len(inv)}
    log("exact + structure done")
    sh = [shingles(r) for r in rows]
    pairs = near_pairs(rows, sh)
    out["minhash_cross_group_pairs"] = len(pairs); out["minhash_examples"] = pairs[:10]
    log(f"minhash in-file pairs {len(pairs)}")
    cross = {}
    for other in ("mixdev_S5", "qc_sample"):
        ro, _ = L.load(other)
        g_ov = len({r["group_id"] for r in rows} & {r["group_id"] for r in ro})
        t_ov = len({h(norm(r["instructions"]) + norm(r["state"])) for r in rows} & {h(norm(r["instructions"]) + norm(r["state"])) for r in ro})
        s_ov = len({r["meta"]["structure_hash"] for r in rows} & {r["meta"]["structure_hash"] for r in ro})
        sp = near_pairs(rows, sh, ro, [shingles(r) for r in ro], same_file=False)
        cross[other] = {"rows": len(ro), "shared_group_ids": g_ov, "shared_normalized_text": t_ov, "shared_structure_hash": s_ov,
                        "minhash_pairs": len(sp), "minhash_examples": sp[:5]}
        log(f"cross {other} {cross[other]}")
    out["cross_file"] = cross
    d = cross["mixdev_S5"]
    out["pass"] = (out["exact_full_row_duplicates"] == 0 and out["structure_hash"]["violations"] == 0
                   and out["minhash_cross_group_pairs"] == 0 and d["shared_group_ids"] == 0
                   and d["shared_normalized_text"] == 0 and d["minhash_pairs"] == 0)
    out["seconds"] = round(time.time() - T0, 1)
    (L.QC / "g12_candidates_r1.json").write_text(json.dumps(out, indent=1))
    log(f"done pass={out['pass']}")


if __name__ == "__main__":
    main()
