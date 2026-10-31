"""G12 dedup (independent F4 checker). C_DATA_SPEC 8 G12 + F4 G0 11:
- exact hash of the model-visible row (card + instructions + state + options + gold): 0 duplicates; also 0 duplicate
  ids;
- MinHash near-duplicates (datasketch, MIT; 5-word shingles of the record `state`, 128 perms, LSH Jaccard >= 0.9):
  pairs across different lineages (group_id) are reported and must be 0 (inside one group they are planned twins or
  format variants);
- structure hash: one surface form per structure, except planned twins and format variants: a structure_hash must
  not occur in two lineages (group_ids);
- cross-file: candidates_r1 vs qc_sample vs mixdev_S5 share no structure_hash, no group_id and no normalized record
  text (the QC sample is a separate sample; the S5 dev never shares a group or text with training rows, spec 10).
Usage: g12.py"""
import hashlib, json, re
from collections import defaultdict, Counter
import qc_lib as L

FILES = ("candidates_r1", "qc_sample", "mixdev_S5")
norm = lambda s: re.sub(r"\s+", " ", s.strip().lower())


def full(r):
    return "\x1e".join([r.get("card") or "", r["instructions"], r["state"], "\x1f".join(r["options"] or []), str(r["gold"])])


def visible(r):
    return "\x1e".join([r.get("card") or "", r["instructions"], r["state"], "\x1f".join(r["options"] or [])])


def main():
    from datasketch import MinHash, MinHashLSH
    data = {f: L.load(f) for f in FILES}
    res = {"gate": "G12", "files": {}}
    for f, rows in data.items():
        ids = Counter(r["id"] for r in rows)
        h = Counter(hashlib.sha256(norm(full(r)).encode()).hexdigest() for r in rows)
        hv = Counter(hashlib.sha256(norm(visible(r)).encode()).hexdigest() for r in rows)  # recheck:F4: gold left out
        sh = defaultdict(set)
        for r in rows:
            sh[r["meta"]["structure_hash"]].add(r["group_id"])
        cross_struct = {k: len(v) for k, v in sh.items() if len(v) > 1}
        lsh = MinHashLSH(threshold=0.9, num_perm=128); mh = {}
        for r in rows:
            w = norm(r["state"]).split(); m = MinHash(num_perm=128)
            for i in range(max(1, len(w) - 4)):
                m.update(" ".join(w[i:i + 5]).encode())
            mh[r["id"]] = m; lsh.insert(r["id"], m)
        grp = {r["id"]: r["group_id"] for r in rows}
        near = set()
        for r in rows:
            for o in lsh.query(mh[r["id"]]):
                if o != r["id"] and grp[o] != grp[r["id"]]:
                    near.add(tuple(sorted((r["id"], o))))
        res["files"][f] = {"rows": len(rows), "dup_ids": sum(1 for v in ids.values() if v > 1),
                           "exact_dup_rows": sum(v - 1 for v in h.values() if v > 1),
                           "exact_dup_visible_rows": sum(v - 1 for v in hv.values() if v > 1),
                           "structure_hashes": len(sh), "structure_hash_in_2plus_groups": len(cross_struct),
                           "near_dup_pairs_cross_group": len(near), "near_dup_examples": sorted(near)[:5]}
    cross = {}
    for i, a in enumerate(FILES):
        for b in FILES[i + 1:]:
            A, B = data[a], data[b]
            cross[f"{a}|{b}"] = {
                "shared_structure_hash": len({r["meta"]["structure_hash"] for r in A} & {r["meta"]["structure_hash"] for r in B}),
                "shared_group_id": len({r["group_id"] for r in A} & {r["group_id"] for r in B}),
                "shared_record_text": len({norm(r["state"]) for r in A} & {norm(r["state"]) for r in B}),
                "shared_full_row": len({norm(full(r)) for r in A} & {norm(full(r)) for r in B}),
                "shared_domain_pack": len({r["meta"]["domain_pack"] for r in A} & {r["meta"]["domain_pack"] for r in B})}
    res["cross_file"] = cross
    # recheck:F4: visible-content duplicates (gold left out), shared record text (spec 10 / docstring) and, against the
    # S5 dev, shared domain packs (spec 10 held-out packs; mixer note 4) now decide too
    ok_files = all(v["dup_ids"] == 0 and v["exact_dup_rows"] == 0 and v["exact_dup_visible_rows"] == 0
                   and v["structure_hash_in_2plus_groups"] == 0
                   and v["near_dup_pairs_cross_group"] == 0 for v in res["files"].values())
    ok_cross = all(v["shared_structure_hash"] == 0 and v["shared_group_id"] == 0 and v["shared_full_row"] == 0
                   and v["shared_record_text"] == 0 and ("mixdev_S5" not in k or v["shared_domain_pack"] == 0)
                   for k, v in cross.items())
    res["pass"] = ok_files and ok_cross
    json.dump(res, open(L.QC / "g12.json", "w"), indent=1)
    print(json.dumps({"pass": res["pass"], "files": {k: {kk: vv for kk, vv in v.items() if kk != "near_dup_examples"}
                                                     for k, v in res["files"].items()}, "cross": cross}))


if __name__ == "__main__":
    main()
