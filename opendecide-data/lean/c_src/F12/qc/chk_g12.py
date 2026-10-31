"""G12 dedup (independent F12 checker, check:F12, c-lanes-v3; test as in the F9 / F11 checkers):
- exact hash: sha256 of the model-visible row (qtype, card, instructions, state, options): 0 duplicates;
- MinHash near-dups (datasketch, MIT): word 5-gram shingles of question paragraph + state + options, 128 perms, LSH
  threshold 0.9, verified by exact shingle Jaccard >= 0.9; pairs inside one planned twin set (shared group_id or
  call_id, or a relation pair) are allowed; others are near-dups to be removed (keep one);
- structure hash (meta.structure_hash): one surface form per structure, except planned twins and format variants
  (same group_id); collisions across group_ids are reported as failures;
- separation from the mix-tuning dev (mixer note 4): no group_id, normalised state, structure_hash or domain_pack
  shared with out/mixdev_S5.jsonl; every row carries meta.format_style. Usage: chk_g12.py <name>"""
import json, sys, hashlib, re
from collections import defaultdict, Counter
from datasketch import MinHash, MinHashLSH
import chk_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"


def norm(s):
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def main():
    rows, side = L.load(NAME); by = {r["id"]: r for r in rows}
    rel = L.relations(NAME)
    relp = {frozenset((x["a"], x["b"])) for x in rel}
    h = Counter(hashlib.sha256(json.dumps([r["qtype"], r.get("card"), r["instructions"], r["state"], r["options"]]).encode()).hexdigest() for r in rows)
    exact = sum(v - 1 for v in h.values() if v > 1)
    lsh = MinHashLSH(threshold=0.9, num_perm=128); sh = {}
    for r in rows:
        t = (L.qtext(r, side.get(r["id"])) + " " + r["state"] + " " + " ".join(r["options"] or [])).lower().split()
        s = {" ".join(t[i:i + 5]) for i in range(max(1, len(t) - 4))}; sh[r["id"]] = s
        m = MinHash(num_perm=128)
        for x in s:
            m.update(x.encode())
        lsh.insert(r["id"], m)
    near, allowed, seen = [], 0, set()
    for r in rows:
        m = MinHash(num_perm=128)
        for x in sh[r["id"]]:
            m.update(x.encode())
        for o in lsh.query(m):
            if o == r["id"] or (o, r["id"]) in seen:
                continue
            seen.add((r["id"], o))
            a, b = sh[r["id"]], sh[o]; j = len(a & b) / max(1, len(a | b))
            if j < 0.9:
                continue
            ro = by[o]
            if ro["group_id"] == r["group_id"] or ro["call_id"] == r["call_id"] or frozenset((o, r["id"])) in relp:
                allowed += 1
            else:
                near.append((r["id"], o, round(j, 3)))
    sg = defaultdict(set)
    for r in rows:
        sg[r["meta"].get("structure_hash")].add(r["group_id"])
    coll = {k: len(v) for k, v in sg.items() if k and len(v) > 1}
    out = {"gate": "G12", "file": f"out/{NAME}.jsonl", "pool_sha256": L.sha(L.OUT / f"{NAME}.jsonl"), "rows": len(rows), "exact_duplicates": exact,
           "near_dup_pairs_outside_twin_sets": len(near), "near_dup_examples": near[:20], "near_dup_pairs_in_twin_sets": allowed,
           "structure_hash_collisions_across_groups": len(coll), "structure_hash_collision_examples": list(coll.items())[:10],
           "missing_structure_hash": sum(1 for r in rows if not r["meta"].get("structure_hash")),
           "missing_format_style": sum(1 for r in rows if not r["meta"].get("format_style"))}
    if NAME != "mixdev_S5":
        dev, _ = L.load("mixdev_S5")
        sets = {k: set() for k in ("group_id", "state", "structure_hash", "domain_pack")}
        for d in dev:
            sets["group_id"].add(d["group_id"]); sets["state"].add(norm(d["state"]))
            sets["structure_hash"].add(d["meta"].get("structure_hash")); sets["domain_pack"].add(d["meta"].get("domain_pack"))
        ov = {"group_id": sum(r["group_id"] in sets["group_id"] for r in rows),
              "state": sum(norm(r["state"]) in sets["state"] for r in rows),
              "structure_hash": sum(r["meta"].get("structure_hash") in sets["structure_hash"] for r in rows),
              "domain_pack": sum(r["meta"].get("domain_pack") in sets["domain_pack"] for r in rows)}
        out["mixdev_overlap_rows"] = ov
    else:
        ov = {}
    out["pass"] = (exact == 0 and not near and not coll and out["missing_structure_hash"] == 0
                   and out["missing_format_style"] == 0 and not any(ov.values()))
    (L.QC / f"g12_{NAME}.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({k: v for k, v in out.items() if "examples" not in k}))


if __name__ == "__main__":
    main()
