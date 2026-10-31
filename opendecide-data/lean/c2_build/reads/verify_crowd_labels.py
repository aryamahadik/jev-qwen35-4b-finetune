"""reads/verify_crowd_labels.py: check the C1 crowd labels of data/c2_crowd_shards/<FAM> against c2_select's preconditions
WITHOUT running select (A37 e). CPU only, read only; prints counts and hashes, never row text.

For each family (default: those listed in crowd_c2/crowd_tasks_c2.json):
  - the candidate file and relation file still match the MANIFEST and the shards' source sha (c2_select.family_inputs);
  - every shard is done (shard_golden.shard_done: ids, row count, shard sha256) and all shards share ONE view;
  - the view is C1's, one view, no TTA / permutation (c2_select.view_problem; settings tta_choice false);
  - every candidate row has EXACTLY ONE label (no candidate without one, no id labelled twice); labels of rows that left the
    candidate file after the read are reported as surplus; every current candidate row must be identical to the row that was read;
  - c2_select.c1_pg runs (the p_g of every row) and every probability set is a probability distribution over the row's
    answer keys (yes/no: {yes, no}; choice: the row's options).
Run from lean/c2_build:  ../../.venv/bin/python -B reads/verify_crowd_labels.py [--fam T28 ...]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2B = HERE.parent
sys.path.insert(0, str(C2B))
import c2io  # noqa: E402
import c2_select as sel  # noqa: E402

sys.path.insert(0, str(c2io.LEAN))
import shard_golden as sg  # noqa: E402


def check_family(ilog, fam: str) -> dict:
    rows, _, shas = sel.family_inputs(ilog, fam)
    sd = sel.SHARDS / fam
    ld = sd / f"labels_{c2io.C1}"
    out = {"family": fam, "candidate_rows": len(rows), "candidates_sha256": shas["candidates_sha256"][:16],
           "shards": len(sg.shard_files(sd)), "problems": []}
    man = json.loads((sd / "shards.json").read_text())
    # The candidate file may have changed since the shards were written (another agent trims it). That is fine only when
    # every current candidate row is byte-identical (as JSON) to the row that was read: the labels then still belong to it.
    out["shards_written_from_this_candidates_file"] = man.get("candidates_sha256") == shas["candidates_sha256"]
    read_rows = {}
    for s in sg.shard_files(sd):
        for x in sg.read_jsonl(s):
            read_rows[x["id"]] = json.dumps(x, sort_keys=True)
    out["rows_read"] = len(read_rows)
    out["candidates_not_in_shards"] = sum(1 for r in rows if r["id"] not in read_rows)
    out["candidates_changed_since_read"] = sum(1 for r in rows if r["id"] in read_rows
                                               and read_rows[r["id"]] != json.dumps(r, sort_keys=True))
    if out["candidates_not_in_shards"] or out["candidates_changed_since_read"]:
        out["problems"].append("a candidate row is new or differs from the row that was read")
    # exactly one label per candidate row (labels of rows that left the candidates since the read are surplus, not an error)
    seen = Counter()
    for s in sg.shard_files(sd):
        lp, _ = sg.label_paths(ld, s)
        if not lp.exists():
            out["problems"].append(f"{lp.name}: missing")
            continue
        for x in sg.read_jsonl(lp):
            seen[x["id"]] += 1
            if x.get("model") != c2io.C1:
                out["problems"].append(f"{lp.name}: label model {x.get('model')!r}")
                break
    cand = {r["id"] for r in rows}
    out["labels"] = sum(seen.values())
    out["labels_for_candidates"] = sum(seen[i] for i in cand)
    out["surplus_labels_for_rows_no_longer_candidates"] = len(set(seen) - cand)
    out["candidates_without_label"] = len(cand - set(seen))
    out["candidates_with_other_than_one_label"] = sum(1 for i in cand if seen[i] > 1)
    if out["candidates_without_label"] or out["candidates_with_other_than_one_label"] or any(v != 1 for v in seen.values()):
        out["problems"].append("not exactly one C1 label per candidate row")
    if out["problems"]:
        return out
    pg, view = sel.load_c1(ilog, rows, ld, sd)            # raises SystemExit if a shard is not done / the view is not C1's
    out["view_problem"] = sel.view_problem(view)
    out["view_settings"] = view["settings"]
    labels, _ = sg.load_labels(ld, sd, return_view=True)
    bad = 0
    for r in rows:
        p = labels[r["id"]]
        keys = {"yes", "no"} if r["qtype"] == "noul" else set(r["options"] or [])
        if set(p) != keys or abs(sum(p.values()) - 1.0) > 1e-3 or any(not (0 <= v <= 1) or math.isnan(v) for v in p.values()):
            bad += 1
    out["rows_with_bad_probability_set"] = bad
    if bad:
        out["problems"].append(f"{bad} rows with a probability set that is not a distribution over the row's answers")
    if out["view_problem"]:
        out["problems"].append(out["view_problem"])
    bins = Counter("easy" if v > 0.97 else "hard" if v <= 0.30 else "medium" for v in pg.values())
    out["pg_bins"] = dict(bins)
    metas = [json.loads(sg.label_paths(ld, s)[1].read_text()) for s in sg.shard_files(sd)]
    out["read_sec"] = round(sum(m.get("sec", 0) for m in metas), 1)
    out["rows_per_sec"] = round(len(rows) / max(out["read_sec"], 1e-9), 2)
    out["engines"] = sorted({m.get("engine_fast_read", {}).get("sglang_version") or "?" for m in metas})
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fam", nargs="*", default=None)
    ap.add_argument("--out", default="")
    a = ap.parse_args(argv)
    fams = a.fam or list(json.loads((sel.OUT / "crowd_tasks_c2.json").read_text())["families"])
    ilog = c2io.C2InputLog()
    res = [check_family(ilog, f) for f in fams]
    for r in res:
        print(json.dumps({k: v for k, v in r.items() if k != "view_settings"}))
    n_bad = sum(1 for r in res if r["problems"])
    print(f"families {len(res)}, with problems {n_bad}, candidate rows {sum(r['candidate_rows'] for r in res)}, "
          f"labels {sum(r.get('labels', 0) for r in res)}, labels for candidates {sum(r.get('labels_for_candidates', 0) for r in res)}")
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=1))
    return 1 if n_bad else 0


if __name__ == "__main__":
    sys.exit(main())
