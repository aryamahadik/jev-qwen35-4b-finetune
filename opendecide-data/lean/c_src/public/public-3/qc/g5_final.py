#!/usr/bin/env python3
"""G5 result for public-3 (repair r1 version). The flag-only reader (an independent Claude session, never a public-3
author) reads qc/g5_render.jsonl (drawn by qc/g5_sample.py) and LOGS every verdict in qc/g5_flags.jsonl, one JSON line
per read batch or recheck; this script derives the result from that log only (no verdict lists in code), so every
move is on record:
  {"dataset": ds, "idx": [lo, hi], "wrong": [...], "ambiguous": [...], "note": "..."}          a read batch
  {"dataset": ds, "recheck": idx, "from": "wrong"|"ambiguous"|"ok", "to": "wrong"|"ambiguous"|"ok", "note": "..."}
Indices are positions in each dataset's sample order (qc/g5_sample_ids.json). The reader never sets or edits a label.
Spec 8 G5, public rows: dataset-level decision only: a dataset with > 8% clearly wrong golds (> 8 of 100) is dropped.
"Clearly wrong" = a careful reader applying the row's own card would answer differently with high confidence and the
gold is not a defensible reading; anything weaker is "ambiguous" (reported; the <= 1% ambiguous bar is for families).
Every batch range must be covered exactly once. Writes qc/g5.json."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    s = json.load(open(HERE / "g5_sample_ids.json"))
    state, covered, log = {}, {}, []
    for ln in open(HERE / "g5_flags.jsonl"):
        e = json.loads(ln)
        ds = e["dataset"]
        st = state.setdefault(ds, {})
        if "recheck" in e:
            i = e["recheck"]
            assert st.get(i, "ok") == e["from"], (ds, i, "recheck 'from' does not match the logged verdict")
            st[i] = e["to"]
            log.append({"dataset": ds, "idx": i, "from": e["from"], "to": e["to"], "note": e.get("note", "")})
            continue
        lo, hi = e["idx"]
        cov = covered.setdefault(ds, set())
        assert not cov & set(range(lo, hi + 1)), (ds, "batch ranges overlap")
        cov |= set(range(lo, hi + 1))
        assert not set(e["wrong"]) & set(e["ambiguous"]), (ds, lo)
        for i in e["wrong"]:
            assert lo <= i <= hi
            st[i] = "wrong"
        for i in e["ambiguous"]:
            assert lo <= i <= hi
            st[i] = "ambiguous"
    out, prob = {}, []
    for ds, ids in s["ids"].items():
        assert covered.get(ds) == set(range(len(ids))), (ds, "every sampled row must be read exactly once")
        w = sorted(i for i, v in state.get(ds, {}).items() if v == "wrong")
        a = sorted(i for i, v in state.get(ds, {}).items() if v == "ambiguous")
        fail = len(w) > 0.08 * len(ids)
        out[ds] = {"read": len(ids), "clearly_wrong": len(w), "ambiguous": len(a),
                   "bar": "> 8% clearly wrong drops the dataset", "pass": not fail,
                   "clearly_wrong_ids": [ids[i] for i in w], "ambiguous_ids": [ids[i] for i in a],
                   "rechecks": [x for x in log if x["dataset"] == ds]}
        if fail:
            prob.append(f"{ds}: {len(w)}/{len(ids)} clearly wrong > 8% -> spec G5: drop the dataset")
    res = {"gate": "G5", "pass": not prob, "problems": prob, "seed": s["seed"], "per_dataset": out,
           "reader": "independent Claude session (not a public-3 author), flag-only; verdicts from qc/g5_flags.jsonl"}
    (HERE / "g5.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k: (v["clearly_wrong"], v["ambiguous"], v["pass"]) for k, v in out.items()}), prob)


if __name__ == "__main__":
    main()
