"""ejs-5/jev-benchmark -> OpenDecide rows (one row per benchmark decision, 868 in total).

  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python bench/ejs5/convert.py
  # tests: --src <synthetic dir> --out <file>

The task specs come from run_public_bench.py, read by AST (ejs5lib.bench_spec): the question each model was asked
(TASKS[t]["ask"]), the criteria and the level names (LEVELS). Nothing is reworded.

  route  (choice, 2 options)  options = the criteria keys in order; card = "- key: description" (the author's criteria)
  triage (choice, 4 options)  same
  score  (Size, 4 levels)     options = LEVELS (tiny, small, medium, large) in order; card = "- level: description"
                              (the author's criteria list, index-aligned with LEVELS, as in its frontier prompt);
                              read as a 4-option choice, decided by the EXPECTED level (ejs5lib.decide)
  gate   (Risk, yes/no)       qtype noul; the question only, no card (Jev's request had no criteria either)

state = the item's text exactly as the author sent it to Jev ("state": r["text"]). Gold: the item's label (choice /
size: the option string; risk: 1 = yes, 0 = no). group_id = the commit sha (a commit can appear in several tasks: the
bootstrap unit). meta.date / meta.late come from commit_dates.json (late = on or after 2026-06-01).

Prints counts and hashes only. Writes <out> and <out>.meta.json (sha256 of the rows file and of every input).
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

import ejs5lib as E


def build_rows(src: Path, code: Path, dates_path: Path | None):
    spec = E.bench_spec(code)
    T, LEVELS = spec["TASKS"], spec["LEVELS"]
    dates = json.loads(dates_path.read_text()) if dates_path and dates_path.exists() else {}
    out, inputs = [], {"run_public_bench.py": spec["sha256"]}
    for task in E.TASKS:
        sp = T[task]
        f = src / sp["file"]
        inputs[sp["file"]] = E.sha256_file(f)
        items = json.loads(f.read_text(encoding="utf-8"))
        seen = set()
        for it in items:
            sha = it["id"]
            if sha in seen:
                raise SystemExit(f"{task}: duplicate commit id within the task (count only: 1)")
            seen.add(sha)
            rid = f"ejs5_{task}_{sha}"
            date = dates.get(sha)
            row = {"id": rid, "group_id": sha, "call_id": rid, "split": "ejs5", "track": "external",
                   "source": f"ejs5_{task}", "state": it["text"], "instructions": sp["ask"]}
            kind = sp["kind"]
            if kind == "choice":
                opts = list(sp["criteria"].keys())
                row.update(qtype="choice", options=opts,
                           card="\n".join(f"- {k}: {v}" for k, v in sp["criteria"].items()), gold=it["label"])
                if it["label"] not in opts:
                    raise SystemExit(f"{task}: a label outside the criteria keys (count only)")
            elif kind == "score":
                if len(sp["criteria"]) != len(LEVELS):
                    raise SystemExit(f"{task}: {len(sp['criteria'])} criteria for {len(LEVELS)} levels")
                row.update(qtype="choice", options=list(LEVELS),
                           card="\n".join(f"- {LEVELS[i]}: {d}" for i, d in enumerate(sp["criteria"])), gold=it["label"])
                if it["label"] not in LEVELS:
                    raise SystemExit(f"{task}: a label outside LEVELS (count only)")
            elif kind == "noul":
                if it["label"] not in ("yes", "no"):
                    raise SystemExit(f"{task}: a label outside yes/no (count only)")
                row.update(qtype="noul", options=None, card=None, gold=1 if it["label"] == "yes" else 0)
            else:
                raise SystemExit(f"{task}: unknown kind {kind!r}")
            row["meta"] = {"bench": "ejs-5/jev-benchmark", "task": task, "kind": kind, "commit": sha, "date": date,
                           "late": bool(date and date[:10] >= E.LATE_FROM)}
            out.append(row)
    if dates_path:
        inputs[dates_path.name] = E.sha256_file(dates_path)
    return out, inputs, spec


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(E.QUAR), help="folder with public_{route,triage,score,gate}.json")
    ap.add_argument("--bench-code", default=None, help="run_public_bench.py (default: <src>/run_public_bench.py)")
    ap.add_argument("--dates", default=None, help="commit_dates.json (default: <src>/commit_dates.json)")
    ap.add_argument("--out", default=None, help="rows file (default: <src>/ejs5_rows.jsonl)")
    ap.add_argument("--expect-n", type=int, default=868, help="refuse if the row count differs (0 = no check)")
    a = ap.parse_args(argv)
    src = Path(a.src).resolve()
    code = Path(a.bench_code).resolve() if a.bench_code else src / "run_public_bench.py"
    dates = Path(a.dates).resolve() if a.dates else src / "commit_dates.json"
    out = Path(a.out).resolve() if a.out else src / "ejs5_rows.jsonl"
    rows, inputs, spec = build_rows(src, code, dates)
    if a.expect_n and len(rows) != a.expect_n:
        raise SystemExit(f"{len(rows)} rows, expected {a.expect_n}")
    out.parent.mkdir(parents=True, exist_ok=True)
    E.write_jsonl_atomic(out, rows)
    by = collections.Counter(r["meta"]["task"] for r in rows)
    late = collections.Counter(r["meta"]["task"] for r in rows if r["meta"]["late"])
    nodate = sum(1 for r in rows if r["meta"]["date"] is None)
    meta = {"rows_file": out.name, "rows_sha256": E.sha256_file(out), "n_rows": len(rows), "by_task": dict(by),
            "n_commits": len({r["group_id"] for r in rows}), "late_from": E.LATE_FROM, "late_rows": sum(late.values()),
            "late_by_task": dict(late), "late_commits": len({r["group_id"] for r in rows if r["meta"]["late"]}),
            "rows_without_date": nodate, "inputs_sha256": inputs, "levels": spec["LEVELS"],
            "n_options": {t: (len(spec["TASKS"][t]["criteria"]) if spec["TASKS"][t]["kind"] != "noul" else 2)
                          for t in E.TASKS},
            "convert_py_sha256": E.sha256_file(__file__), "ejs5lib_py_sha256": E.sha256_file(E.__file__)}
    E.write_json_atomic(out.with_name(out.name + ".meta.json"), meta)
    print(f"wrote {out.name}: {len(rows)} rows {dict(by)}; {meta['n_commits']} commits; "
          f"late (>= {E.LATE_FROM}) {meta['late_rows']} rows / {meta['late_commits']} commits; "
          f"rows without a date {nodate}")
    print(f"rows sha256 {meta['rows_sha256']}; run_public_bench.py sha256 {inputs['run_public_bench.py']}")
    return meta


if __name__ == "__main__":
    main()
