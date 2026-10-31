"""SECONDARY number only (PREREG_ejs5 section 3, owner decision of 3 Oct 2026): the single read of a 2-view run.

  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python bench/ejs5/derive_1v.py c1_main500k
  # then: score_ejs5.py c1_main500k_1v_secondary   (reported as secondary, never used for a claim)

A 2-view run (run_ejs5.py --readout 2view) stores, per row, the A5 readout in "probs" and the identity view (the
single read) in "probs_1v". This copies the run to <runs>/<name>_1v_secondary/ with probs := probs_1v, so that
score_ejs5.py scores the single read with exactly the same code. No model is read, no gold is read, nothing is scored
or printed here except counts. timing.json is not copied (the stored latency is the 2-view time of each row).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import ejs5lib as E


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run", help="a complete 2-view run: name under --runs-dir, or a dir")
    ap.add_argument("--runs-dir", default=str(E.RUNS))
    a = ap.parse_args(argv)
    src = Path(a.run) if Path(a.run).is_dir() else Path(a.runs_dir) / a.run
    man = json.loads((src / "manifest.json").read_text())
    if man.get("status") != "complete" or man.get("readout") != "2view":
        raise SystemExit(f"{src.name}: not a complete 2-view run (status {man.get('status')}, readout "
                         f"{man.get('readout')})")
    out = src.with_name(src.name + "_1v_secondary")
    if out.exists():
        raise SystemExit(f"{out} exists")
    preds = E.read_jsonl(src / "preds.jsonl")
    if any("probs_1v" not in p for p in preds):
        raise SystemExit(f"{src.name}: a row has no probs_1v")
    recs = [{**{k: v for k, v in p.items() if k not in ("probs", "probs_1v")}, "probs": p["probs_1v"]} for p in preds]
    out.mkdir(parents=True)
    E.write_jsonl_atomic(out / "preds.jsonl", recs)
    E.write_json_atomic(out / "manifest.json", {
        **{k: v for k, v in man.items() if k not in ("name", "readout")},
        "name": out.name, "readout": "single (identity view of the 2-view run)", "secondary_only": True,
        "derived_from": {"run": src.name, "preds_sha256": E.sha256_file(src / "preds.jsonl"),
                         "manifest_sha256": E.sha256_file(src / "manifest.json"),
                         "derive_1v_py_sha256": E.sha256_file(__file__)}})
    print(f"wrote {out}: {len(recs)} rows (probs = the single read); score it as SECONDARY: "
          f"score_ejs5.py {out.name}")
    return out


if __name__ == "__main__":
    main()
