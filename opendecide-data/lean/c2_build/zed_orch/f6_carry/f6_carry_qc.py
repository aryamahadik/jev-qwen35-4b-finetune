"""f6_carry_qc.py: the C2 re-gate record of the F6 carry-over pool (C2_DATA_SPEC 2.1 / 3.19; c2io CARRY contract).
Modelled on zed_orch/f5_carry_qc.py (same record shape, same live checks). CPU only, counts only, no model call, NO G13 run.
The ONE writer of lean/data/c2_parts/F6/qc/QC_REPORT.json. The record is computed from on-disk records and live checks, never by
hand: {"pass", "passed_utc", "fix_iterations", "files": {name: {"sha256", "rows"}}, ...} bound to the round-1 candidates file
c_src/F6/out/candidates_r1.jsonl (+ its relations file) and to the A32b rebuild (the v2 pools), exactly the contract of
qc_full_c2.finalize. pass is computed; passed_utc is set only when pass is true and the carry cutoff has not passed.

What it checks (spec 3.19: "F6 (QC pass; its v2 rebuild still owes the G5 delta, QC finalize, crowd/select/G9 redo and its own G13)"):
  R1  the block's OWN finalize record c_src/F6/qc/QC_REPORT.json (tmp/a32b/finalize_qc.py write): pass true, failing_gates [],
      G5 complete (answered all 600 sample rows, 0 clearly wrong, ambiguous <= 6), every gate except G9 has pass true, the label
      gates pass, mixer.qc_binding [] against the files on disk, every recorded pool sha256 equals the file on disk and the
      POOLS_READY_A32 marker.
  R2  live C2 checks: c2io.candidate_problems, the round-1 MANIFEST + relation checks (crowd_select.load_family), relation
      endpoints exist, G-TW 100% (complement: gold flips; equiv: gold equal), formats-1 refuse_held_out strict, exact duplicates 0,
      the crowd shard set is this candidates file and every row has ONE C1 label of the one C1 view (A18.2 / A37 e), the round-1
      selection record crowd_r1/select_F6.json is bound to this file.
  R3  the selectable pool (round-1 selected whole units) holds the <= 1,000-row ceiling with room (a dry in-memory carry_pool).
  R4  the carry cutoff Tue 20 Oct 2026 23:59 UTC has not passed when the record is written.
Deferred (stated in the record): G13 carry run (orchestrator batch) and the G9 selection + re-read after its drops.
Usage (from c2_build):  ../../.venv/bin/python -B zed_orch/f6_carry/f6_carry_qc.py [--write] [--now ISO]
Without --write nothing is written (report only).
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parents[2]          # lean/c2_build
sys.path.insert(0, str(HERE))

import c2io  # noqa: E402
import c2_select as sel  # noqa: E402
import crowd_select as cs  # noqa: E402
from mixio import sha256_file  # noqa: E402

LEAN = c2io.LEAN
FAM = "F6"
R1 = LEAN / "c_src" / FAM
R1_QC = R1 / "qc" / "QC_REPORT.json"
OUTQ = c2io.C2_PARTS / FAM / "qc" / c2io.QC
CARRY_CUTOFF = "2026-10-20T23:59:00+00:00"          # spec 3.19 / A37 (d): carry-over pools, Tue 20 Oct 23:59 UTC


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--now", default=None)
    ap.add_argument("--dryrun-shards-root", default=None, help="report-only dry run: read the crowd shards/labels from this root instead of data/c_crowd_r1_shards")
    ap.add_argument("--dryrun-select-dir", default=None, help="report-only dry run: read select_F6.json from this folder instead of c_build/crowd_r1")
    a = ap.parse_args()
    if (a.dryrun_shards_root or a.dryrun_select_dir) and a.write:
        raise SystemExit("--dryrun-* options cannot be combined with --write")
    if a.dryrun_shards_root:
        sel.R1_SHARDS = Path(a.dryrun_shards_root)
    if a.dryrun_select_dir:
        sel.R1_SELECT = Path(a.dryrun_select_dir)
    c2io.require_a38()
    problems: list[str] = []
    rec: dict = {"family": FAM, "stage": "C2 carry-over re-gate (spec 3.19)", "tool": "c2_build/zed_orch/f6_carry/f6_carry_qc.py"}

    # ---- R1: the block's own finalize record
    r1 = json.loads(R1_QC.read_text(encoding="utf-8"))
    f = c2io.fam_files(FAM)
    cand, relf = f["cand"], f["rel"]
    sys.path.insert(0, str(LEAN / "c_build"))
    import mixer as mx  # noqa: E402
    bind = mx.qc_binding(r1, {cand.name: cand, relf.name: relf})
    gates = r1.get("gates", {})
    bad_gates = sorted(g for g, v in gates.items() if g != "G9" and not (isinstance(v, dict) and v.get("pass") is True))
    g5 = gates.get("G5", {})
    g5_ok = g5.get("complete") is True and g5.get("answered") == 600 and g5.get("clearly_wrong") == 0 and (g5.get("ambiguous") or 0) <= 6
    pool_bad = []
    for name, sha in (r1.get("pool_sha256") or {}).items():
        p = R1 / "out" / name
        if not p.exists() or sha256_file(p) != sha:
            pool_bad.append(name)
    for name, sha in (r1.get("relations_sha256") or {}).items():
        p = R1 / "out" / name
        if not p.exists() or sha256_file(p) != sha:
            pool_bad.append(name)
    marker = (R1 / "tmp/POOLS_READY_A32").read_text(encoding="utf-8")
    marker_ok = all(sha256_file(R1 / "out" / n) in marker for n in ("candidates_r1.jsonl", "qc_sample.jsonl", "mixdev_S5.jsonl"))
    lg = (r1.get("label_gates") or {}).get("pass")
    r1_ok = (r1.get("pass") is True and not r1.get("failing_gates") and not bind and not bad_gates and not pool_bad and g5_ok
             and marker_ok and lg is True)
    rec["block_finalize_record"] = {"file": "c_src/F6/qc/QC_REPORT.json", "sha256": sha256_file(R1_QC), "pass": r1.get("pass"),
                                    "written_utc": r1.get("written_utc"), "failing_gates": r1.get("failing_gates"),
                                    "gates": {g: v.get("pass") for g, v in gates.items()}, "g5": {k: g5.get(k) for k in (
                                        "answered", "agree_with_gold", "disagree", "clearly_wrong", "ambiguous", "unanswered", "complete")},
                                    "label_gates_pass": lg, "qc_binding_problems": bind, "gates_not_pass_true": bad_gates,
                                    "pool_files_differing": pool_bad, "pools_ready_marker_matches_disk": marker_ok}
    if not r1_ok:
        problems.append(f"block finalize record: pass {r1.get('pass')}, binding {bind}, gates {bad_gates}, pool files {pool_bad}, "
                        f"g5_ok {g5_ok}, marker {marker_ok}, label gates {lg}")

    # ---- R2: live checks
    ilog = sel.LinkGuardedInputLog()
    rows, rels, shas = sel.family_inputs(ilog, FAM)          # cs.load_family: MANIFEST + sha checks, raises on a mismatch
    cp = c2io.candidate_problems(FAM, rows)
    by = {r["id"]: r for r in rows}
    miss = [x for x in rels if x["a"] not in by or x["b"] not in by]
    twbad, kinds = 0, Counter()
    for x in rels:
        if x["a"] in by and x["b"] in by:
            ga, gb = by[x["a"]]["gold"], by[x["b"]]["gold"]
            kinds[x["type"]] += 1
            if x["type"] == "complement" and ga == gb:
                twbad += 1
            elif x["type"] == "equiv" and ga != gb:
                twbad += 1
            elif x["type"] not in ("complement", "equiv", "inv"):
                twbad += 1
    units = cs.units_of(rows, rels)
    sizes = Counter(len(u) for u in units)
    seen, dups = set(), 0
    for r in rows:
        k = json.dumps([r.get("state"), r.get("instructions"), r.get("options"), r.get("card")], sort_keys=True)
        dups += k in seen
        seen.add(k)
    import mix_c2  # noqa: E402
    ho_rep: dict = {}
    refused = mix_c2.refuse_held_out(ilog, {FAM: rows}, ho_rep)
    sd = sel.R1_SHARDS / FAM
    shard_meta = json.loads((sd / "shards.json").read_text(encoding="utf-8"))
    shard_ok = shard_meta.get("candidates_sha256") == shas["candidates_sha256"]
    pg, view = sel.load_c1(ilog, rows, sd / f"labels_{c2io.C1}", sd)
    r1sel = ilog.json(sel.R1_SELECT / f"select_{FAM}.json")
    sel_ok = r1sel.get("candidates_sha256") == shas["candidates_sha256"]
    live = {"candidate_problems": cp, "rows": len(rows), "relations": len(rels), "relation_kinds": dict(kinds),
            "relation_endpoint_missing": len(miss), "g_tw_violations": twbad, "unit_sizes": dict(sizes),
            "exact_duplicate_rows": dups, "formats1_refuse_held_out_strict": ho_rep["fmt1_refuse_held_out"][FAM],
            "formats1_refused": refused, "shard_set_candidates_sha_equal": shard_ok,
            "c1_labels": len(pg), "c1_labels_missing": sum(1 for r in rows if r["id"] not in pg), "c1_view": view,
            "round1_select_candidates_sha_equal": sel_ok, "round1_select_crowd": r1sel.get("crowd"),
            "gold": dict(Counter(r["gold"] for r in rows)), "sampler": dict(Counter((r.get("meta") or {}).get("sampler") for r in rows))}
    rec["live_checks"] = live
    if cp or miss or twbad or dups or refused or not shard_ok or live["c1_labels_missing"] or not sel_ok:
        problems.append(f"live checks failed: {live}")

    # ---- R3: the selectable pool
    pool, prel, info = sel.carry_pool(FAM, rows, rels, set(r1sel.get("selected_ids") or []))
    rec["selectable_pool"] = info | {"target": c2io.CARRY[FAM], "units": len(cs.units_of(pool, prel)),
                                     "room_for_g13_drops_rows": len(pool) - c2io.CARRY[FAM]}
    if not pool:                                  # F6 is '<=' (spec 3.19): a short pool is fine, an empty one is not
        problems.append("selectable pool is empty")

    # ---- R4: the carry cutoff
    now = a.now or datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    if datetime.datetime.fromisoformat(now) > datetime.datetime.fromisoformat(CARRY_CUTOFF):
        problems.append(f"carry cutoff {CARRY_CUTOFF} has passed ({now})")

    ok = not problems
    rec |= {"pass": ok, "passed_utc": now if ok else None,
            "fix_iterations": 0,
            "fix_iterations_note": "C2 re-gate fix iterations (spec 5.3): none, as for the F5 carry record. The F6 v2 rebuild (A32 b: seed "
                                   "literal fix + deterministic regen + G5 delta) is the step spec 3.19 names as owed, not a C2 fix round; "
                                   "its history is in c_src/F6/qc/QC_REPORT.json (history) and c_src/F6/tmp/HANDOFF_a32.md",
            "reasons_not_passed": problems,
            "files": {cand.name: {"sha256": shas["candidates_sha256"], "rows": len(rows)},
                      relf.name: {"sha256": shas["relations_sha256"], "rows": len(rels)}},
            "mixdev": {"mixdev_S5.jsonl": {"sha256": sha256_file(f["mixdev"]),
                                           "rows": sum(1 for _ in open(f["mixdev"], "rb")), "layout": "round-1 (carry-over)"}},
            "deferred_gates": ["G13 decontamination against the new targets: g13_c2.py carry --block F6 (orchestrator batch)",
                               "G9 selection on the G13 drops + re-read: c2_select.py carry --fam F6 --exclude-ids <c2_carry_F6.json>"],
            "crowd": "C1 one-view labels of the v2 candidates (data/c_crowd_r1_shards/F6/labels_q35_4b_main500k; read 17 Oct 2026 on od-l4b "
                     "SGLang S1 with crowd_driver.sh --views 1); the round-1 3-model crowd of the pre-A32 pool no longer applies"}
    print(json.dumps({k: rec[k] for k in ("pass", "passed_utc", "fix_iterations", "reasons_not_passed", "files")}, indent=1))
    print(json.dumps(rec["live_checks"], default=str)[:1800])
    print(json.dumps(rec["selectable_pool"]))
    if a.write:
        sha = c2io.write_json(OUTQ, rec)
        probs = mx.qc_binding(json.loads(OUTQ.read_text(encoding="utf-8")), {cand.name: cand, relf.name: relf})
        print("written", OUTQ, sha, "qc_binding", probs)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
