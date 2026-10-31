"""G12 dedup (independent F6 checker). C_DATA_SPEC v4 8 G12 + F6 G0 8:
- exact hash of the model-visible row (card + instructions + state + options + gold): 0 duplicates; 0 duplicate ids;
- MinHash near-duplicates (datasketch, MIT; 5-word shingles, 128 perms, LSH Jaccard >= 0.9) on record + question
  (state-only reported as info): pairs across different lineages must be 0. A lineage is a selection block: rows joined
  by group_id (twin sets) or by a relations-file unit (complement / equiv / inv), closed under both;
- structure hash: one surface form per structure except planned twins and format variants: a structure_hash must not
  occur in two lineages;
- cross-file: candidates_r1 vs qc_sample vs mixdev_S5 share no structure_hash, group_id, record text or full row.
Usage: g12.py"""
import hashlib, json, re
from collections import defaultdict, Counter
import qc_lib as q

FILES = ("candidates_r1", "qc_sample", "mixdev_S5")
norm = lambda s: re.sub(r"\s+", " ", s.strip().lower())
full = lambda r: "\x1e".join([r.get("card") or "", r["instructions"], r["state"], "\x1f".join(r["options"] or []), str(r["gold"])])


def lineages(rows, rels):
    par = {r["id"]: r["id"] for r in rows}
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    def u(a, b):
        if a in par and b in par: par[f(a)] = f(b)
    first = {}
    for r in rows:
        g = r.get("group_id")
        if g is not None:
            if g in first: u(r["id"], first[g])
            else: first[g] = r["id"]
    for x in rels: u(x["a"], x["b"])
    return {r["id"]: f(r["id"]) for r in rows}


def near(rows, lin, text):
    from datasketch import MinHash, MinHashLSH
    lsh = MinHashLSH(threshold=0.9, num_perm=128); mh = {}
    for r in rows:
        w = norm(text(r)).split(); m = MinHash(num_perm=128)
        for i in range(max(1, len(w) - 4)): m.update(" ".join(w[i:i + 5]).encode())
        mh[r["id"]] = m; lsh.insert(r["id"], m)
    out = set()
    for r in rows:
        for o in lsh.query(mh[r["id"]]):
            if o != r["id"] and lin[o] != lin[r["id"]]: out.add(tuple(sorted((r["id"], o))))
    return out


def main():
    data = {f: q.load(f)[0] for f in FILES}
    res = {"gate": "G12", "files": {}}
    for f, rows in data.items():
        lin = lineages(rows, q.load_rel(f))
        ids = Counter(r["id"] for r in rows)
        h = Counter(hashlib.sha256(norm(full(r)).encode()).hexdigest() for r in rows)
        sh = defaultdict(set)
        for r in rows: sh[r["meta"]["structure_hash"]].add(lin[r["id"]])
        nq = near(rows, lin, lambda r: r["state"] + "\n" + q.split_q(r["instructions"])[0])
        ns = near(rows, lin, lambda r: r["state"])
        res["files"][f] = {"rows": len(rows), "lineages": len(set(lin.values())), "dup_ids": sum(1 for v in ids.values() if v > 1),
                           "exact_dup_rows": sum(v - 1 for v in h.values() if v > 1), "structure_hashes": len(sh),
                           "structure_hash_in_2plus_lineages": sum(1 for v in sh.values() if len(v) > 1),
                           "near_dup_pairs_cross_lineage_state_question": len(nq),
                           "near_dup_rows_involved": len({x for p in nq for x in p}),
                           "info_near_dup_pairs_cross_lineage_state_only": len(ns)}
        q.progress(f"G12 {f} done")
    cross = {}
    for i, a in enumerate(FILES):
        for b in FILES[i + 1:]:
            A, B = data[a], data[b]
            cross[f"{a}|{b}"] = {
                "shared_structure_hash": len({r["meta"]["structure_hash"] for r in A} & {r["meta"]["structure_hash"] for r in B}),
                "shared_group_id": len({r["group_id"] for r in A if r.get("group_id")} & {r["group_id"] for r in B if r.get("group_id")}),
                "shared_record_text": len({norm(r["state"]) for r in A} & {norm(r["state"]) for r in B}),
                "shared_full_row": len({norm(full(r)) for r in A} & {norm(full(r)) for r in B})}
    res["cross_file"] = cross
    v = res["files"]["candidates_r1"]
    res["pass_candidates"] = (v["dup_ids"] == 0 and v["exact_dup_rows"] == 0 and v["structure_hash_in_2plus_lineages"] == 0
                              and v["near_dup_pairs_cross_lineage_state_question"] == 0)
    res["pass_cross"] = all(c["shared_structure_hash"] == 0 and c["shared_group_id"] == 0 and c["shared_full_row"] == 0
                            and c["shared_record_text"] == 0 for c in cross.values())
    res["pass"] = res["pass_candidates"] and res["pass_cross"]
    json.dump(res, open(q.QC / "g12.json", "w"), indent=1)
    print(json.dumps({"pass": res["pass"], "files": res["files"], "cross": cross}))


if __name__ == "__main__":
    main()
