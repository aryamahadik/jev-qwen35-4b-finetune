"""G12 dedup (independent F2 checker). C_DATA_SPEC 8 G12 + F2 G0 7:
- exact hash: sha256 of the model-visible row (qtype, card, instructions, state, options): 0 duplicates;
- MinHash near-dups (datasketch, MIT): word 5-gram shingles of the row-specific text (question + state + options; the
  shared card and wording are left out so that two different problems on one card are not called duplicates),
  128 permutations, LSH threshold 0.9; pairs are verified by exact shingle Jaccard >= 0.9; pairs inside one planned
  twin set (twin_of / relation file / shared call_id) are allowed;
- structure hash (meta.structure_hash): one surface form per structure, except planned twins (and format variants,
  which F2 does not emit as separate rows); also cross-file overlap vs qc_sample and mixdev_S5 (report; S5 must be
  disjoint, G13 method 6 is the orchestrator's). Usage: g12.py <name>"""
import json, sys, hashlib, re
from collections import defaultdict, Counter
from datasketch import MinHash, MinHashLSH
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
TOK = re.compile(r"\S+")


def exact_key(r):
    s = json.dumps([r["qtype"], r.get("card") or "", r["instructions"], r["state"], r.get("options")], ensure_ascii=False)
    return hashlib.sha256(s.encode()).hexdigest()


def shingles(r):
    v = L.views(r); t = TOK.findall((v["q"] + " " + v["state"] + " " + " | ".join(v["opts"])).lower())
    return {" ".join(t[i:i + 5]) for i in range(max(1, len(t) - 4))}


def main():
    rows = L.load(NAME); rel = L.load_relations(NAME)
    parent = {r["id"]: r["id"] for r in rows}

    def find(k):
        while parent[k] != k:
            parent[k] = parent[parent[k]]; k = parent[k]
        return k

    def union(a, b):
        if a in parent and b in parent:
            parent[find(a)] = find(b)
    for r in rows:
        if r["meta"].get("twin_of"):
            union(r["id"], r["meta"]["twin_of"])
    for x in rel:
        union(x["a"], x["b"])
    byc = defaultdict(list)
    for r in rows:
        byc[r["call_id"]].append(r["id"])
    for ids in byc.values():
        for i in ids[1:]:
            union(ids[0], i)
    ex = Counter(exact_key(r) for r in rows); dup_exact = sum(c - 1 for c in ex.values() if c > 1)
    lsh = MinHashLSH(threshold=0.9, num_perm=128); sh = {}; mh = {}
    for r in rows:
        s = shingles(r); sh[r["id"]] = s; m = MinHash(num_perm=128)
        for g in s:
            m.update(g.encode())
        mh[r["id"]] = m; lsh.insert(r["id"], m)
    pairs = set()
    for r in rows:
        for o in lsh.query(mh[r["id"]]):
            if o != r["id"]:
                pairs.add(tuple(sorted((r["id"], o))))
    near = []
    for a, b in pairs:
        j = len(sh[a] & sh[b]) / max(1, len(sh[a] | sh[b]))
        if j >= 0.9:
            near.append((a, b, round(j, 3), find(a) == find(b)))
    unplanned = [p for p in near if not p[3]]
    sg = defaultdict(list)
    for r in rows:
        sg[r["meta"]["structure_hash"]].append(r["id"])
    multi = {h: ids for h, ids in sg.items() if len(ids) > 1}
    bad_struct = {h: ids for h, ids in multi.items() if len({find(i) for i in ids}) > 1}
    cross = {}
    for other in ("qc_sample", "mixdev_S5"):
        if other == NAME:
            continue
        hs = {json.loads(l)["meta"]["structure_hash"] for l in open(L.OUT / f"{other}.jsonl")}
        cross[other] = sum(1 for h in sg if h in hs)
    out = {"gate": "G12", "file": f"out/{NAME}.jsonl", "rows": len(rows), "exact_duplicates": dup_exact,
           "near_dup_pairs_ge_0.9": len(near), "near_dup_pairs_unplanned": len(unplanned), "unplanned_examples": unplanned[:20],
           "structure_groups_multi": len(multi), "structure_groups_not_one_twin_set": len(bad_struct),
           "structure_bad_examples": dict(list(bad_struct.items())[:10]), "structure_overlap_with": cross,
           "pass": dup_exact == 0 and not unplanned and not bad_struct and cross.get("mixdev_S5", 0) == 0}
    (L.QC / f"g12_{NAME}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if "examples" not in k}))


if __name__ == "__main__":
    main()
