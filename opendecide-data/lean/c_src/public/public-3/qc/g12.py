#!/usr/bin/env python3
"""G12 dedup for public-3 (independent checker, prep5/B4; own code, counts only, never prints row text).

On rows_r1 + reserve (the mixed files, together, since a refill puts reserve rows next to rows_r1):
  exact     : sha256 of the model-visible row (qtype, card, instructions, state, options): 0 duplicates.
  near-dup  : MinHash (datasketch, MIT) on word 5-gram shingles of loose(instructions + state + options), 128
              permutations, LSH threshold 0.9, verified by exact shingle Jaccard >= 0.9; pairs in one planned twin set
              (twin_of / group_id / call_id) are allowed. Rule "keep one": 0 unplanned pairs may remain.
  record    : the same loose record text (qclib.record_texts) shown in two rows outside one planned twin set: 0
              (builder rule "records per text = 1"; spec 3.1 unused records).
  structure : meta.structure_hash: one surface form per structure, except planned twins / format variants (rows of
              one group_id or twin set): 0 violations.
  mtdev     : no group_id, call_id, structure_hash, record id or loose record text shared with out/public3_mtdev.
Writes qc/g12.json."""
import hashlib, json
from collections import Counter, defaultdict
from datasketch import MinHash, MinHashLSH
import qclib as Q


def exact_key(r):
    return hashlib.sha256(json.dumps([r["qtype"], r["card"], r["instructions"], r["state"], r["options"]],
                                     ensure_ascii=False).encode()).hexdigest()


def shingles(r):
    w = Q.loose("\n".join([r["instructions"] or "", r["state"] or ""] + list(r["options"] or []))).split()
    return {" ".join(w[i:i + 5]) for i in range(max(1, len(w) - 4))}


def main():
    rows = [r for n in Q.MIXED for r in Q.load(n)]
    dev = Q.load("public3_mtdev.jsonl")
    parent = {}

    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)
    for r in rows:   # planned twin sets: twin_of, group_id, call_id
        union("id:" + r["id"], "g:" + r["group_id"])
        union("id:" + r["id"], "c:" + r["call_id"])
        if r["meta"].get("twin_of"):
            union("id:" + r["id"], "id:" + r["meta"]["twin_of"])
    tset = {r["id"]: find("id:" + r["id"]) for r in rows}
    res, prob = {"rows": len(rows), "twin_sets": len(set(tset.values()))}, []
    ek = Counter(exact_key(r) for r in rows)
    res["exact_dup_rows"] = sum(v - 1 for v in ek.values() if v > 1)
    lsh, sh = MinHashLSH(threshold=0.9, num_perm=128), {}
    for r in rows:
        s = shingles(r)
        sh[r["id"]] = s
        m = MinHash(num_perm=128)
        for x in s:
            m.update(x.encode())
        lsh.insert(r["id"], m)
        r["_mh"] = m
    pairs = set()
    for r in rows:
        for o in lsh.query(r["_mh"]):
            if o != r["id"]:
                a, b = sorted((r["id"], o))
                pairs.add((a, b))
    near = planned = 0
    for a, b in pairs:
        j = len(sh[a] & sh[b]) / len(sh[a] | sh[b])
        if j >= 0.9:
            if tset[a] == tset[b]:
                planned += 1
            else:
                near += 1
    res["near_dup_pairs_unplanned"], res["near_dup_pairs_planned"] = near, planned
    rt = defaultdict(set)
    for r in rows:
        for t in Q.record_texts(r)[0]:
            rt[Q.h(Q.loose(t))].add(tset[r["id"]])
    res["record_text_in_2plus_twin_sets"] = sum(len(v) > 1 for v in rt.values())
    st = defaultdict(lambda: defaultdict(set))
    for r in rows:
        st[r["meta"]["structure_hash"]][tset[r["id"]]].add(exact_key(r))
    res["structure_hashes"] = len(st)
    res["structure_violations"] = sum(1 for v in st.values() if len(v) > 1)
    dk = {"group_id": lambda r: {r["group_id"]}, "call_id": lambda r: {r["call_id"]},
          "structure_hash": lambda r: {r["meta"]["structure_hash"]},
          "record_uid": lambda r: set(r["meta"]["record_uid"]) if isinstance(r["meta"]["record_uid"], list)
          else {r["meta"]["record_uid"]},
          "record_text": lambda r: {Q.h(Q.loose(t)) for t in Q.record_texts(r)[0]},
          "exact_row": lambda r: {exact_key(r)}}
    res["shared_with_mtdev"] = {k: len(set().union(*(f(r) for r in rows)) & set().union(*(f(r) for r in dev)))
                                for k, f in dk.items()}
    for k in ("exact_dup_rows", "near_dup_pairs_unplanned", "record_text_in_2plus_twin_sets", "structure_violations"):
        if res[k]:
            prob.append(k)
    if any(res["shared_with_mtdev"].values()):
        prob.append("mtdev overlap")
    out = {"gate": "G12", "pass": not prob, "problems": prob, **res}
    (Q.HERE / "g12.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out)[:1500])


if __name__ == "__main__":
    main()
