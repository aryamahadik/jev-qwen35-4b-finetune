#!/usr/bin/env python3
"""Recheck r1 (independent): cross-parse check of public-3 records against formats-2's independent parse of the same
upstream files (c_src/formats/formats-2/records/*.jsonl; MAMS ACSA/ATSA, EDOS, XED). For every record a mixed or mtdev
row uses: same record id exists, same normalized text sha256, same annotation, and for MAMS / EDOS the official split
recorded by formats-2 is 'train' (spec 3.1: train split only). Counts only. Writes qc/g1_xparse.json."""
import ast, json
from collections import Counter
from pathlib import Path
import qclib as Q
F2 = Q.P3.parents[1] / "formats/formats-2/records"
P3REC = Q.P3 / "tmp/records"


def load(p):
    return {x["id"]: x for x in map(json.loads, open(p, encoding="utf-8"))}


def main():
    res, prob = {}, []
    rows = [(n, r) for n in Q.MIXED + ("public3_mtdev.jsonl",) for r in Q.load(n)]
    for scheme in ("mams_acsa", "mams_atsa", "edos", "xed"):
        f2, p3 = load(F2 / f"{scheme}.jsonl"), load(P3REC / f"{scheme}.jsonl")
        c = Counter()
        for n, r in rows:
            u = r["meta"]["record_uid"]
            for uid in (u if isinstance(u, list) else [u]):
                if not uid.startswith(f"rec.{scheme}."):
                    continue
                c["uses"] += 1
                a, b = p3.get(uid), f2.get(uid)
                if a is None or b is None:
                    c["missing_" + ("p3" if a is None else "f2")] += 1
                    continue
                c["text_sha_equal"] += a["norm_sha256"][:40] == b["norm_sha256"][:40]
                aa = a["ann"] if isinstance(a["ann"], dict) else ast.literal_eval(a["ann"])
                c["ann_equal"] += aa == b["ann"] or (scheme == "mams_atsa" and
                                                    [(t["term"], t["polarity"]) for t in aa["terms"]] ==
                                                    [(t["term"], t["polarity"]) for t in b["ann"]["terms"]])
                hl = r["meta"].get("human_label")
                if scheme == "edos":
                    c["human_label_matches_ann"] += hl == {k: b["ann"][k] for k in hl} if isinstance(hl, dict) else False
                if scheme in ("mams_acsa", "edos"):
                    c["f2_split_train"] += b.get("split") == "train"
                    c["needs_train"] += 1
        res[scheme] = dict(c)
        if c["missing_p3"] or c["missing_f2"] or c["text_sha_equal"] != c["uses"] or c["ann_equal"] != c["uses"] \
                or c["f2_split_train"] != c["needs_train"]:
            prob.append(scheme)
    out = {"check": "cross-parse vs formats-2 (text, labels, official train split)", "pass": not prob, "problems": prob,
           "per_scheme": res}
    (Q.HERE / "g1_xparse.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out))


if __name__ == "__main__":
    main()
