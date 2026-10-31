"""f11_carry_qc.py: the C2 re-gate record of the F11 carry-over pool (C2_DATA_SPEC 2.1 / 3.19; c2io CARRY contract).
CPU only, counts only, no model call, NO G13 run. The ONE writer of lean/data/c2_parts/F11/qc/QC_REPORT.json. The record is
computed from on-disk records and live checks, never by hand: {"pass", "passed_utc", "fix_iterations", "files": {name:
{"sha256", "rows"}}, ...} bound to the round-1 candidates file c_src/F11/out/candidates_r1.jsonl (+ its relations file), the same
contract as qc_full_c2.finalize and the SB5 / F5 finalizers. pass is computed; passed_utc is set only when pass is true.

What it checks (spec 3.19: "F11 (QC pass; needs a G13 re-run after the 8 Oct wording fixes): <= 1,000 rows, prefer its XED / MAMS
real-text codebook rows"; PREREG A31 (b), A34 (b), A37 (e)):
  R1  the round-1 record c_src/F11/qc/QC_REPORT.json: pass true, failed_gates [], problems [], recheck + check_5001 pass,
      G2 solver B 0 mismatches on the live pools; mixer.qc_binding [] against the files on disk; every recorded pool sha256
      equals the file on disk (nothing regenerated since the round-1 pass).
  R2  the round-1 G9 re-read (c_src/F11/qc/g9_reread.json): 0 clearly wrong, 0 ambiguous, bound to this candidates sha.
  R3  live C2 checks: c2io.candidate_problems (no S5 / dev_only rows, no duplicate ids), the round-1 MANIFEST + relation checks
      (crowd_select.load_family), relation endpoints exist, G-TW 100% (complement: gold flips; equiv: gold equal), formats-1
      refuse_held_out strict, every row has ONE C1 label of the one C1 view (A18.2 / A37 e), shard set = this file, the
      round-1 selection (crowd_r1/select_F11.json) is bound to this file.
  R4  the 8 Oct wording fix is not in the rows: every candidate row that still carries the OLD SEM-15 wording is in the round-1
      G13 drop list (logs/decontam_counts/F11.json, same candidates sha, complete true); the rows that can be carried hold none.
  R5  the selectable pool (round-1 selected whole units, minus the round-1 G13 drops) holds the 1,000-row ceiling with room, and
      the XED / MAMS preferred part is counted (a dry in-memory c2_select.select_carry; nothing written to crowd_c2/).
  R6  the carry cutoff: Tue 20 Oct 2026 23:59 UTC (spec 3.19) has not passed when the record is written.
Usage (from c2_build):  ../../.venv/bin/python -B zed_orch/carry_f11/tools/f11_carry_qc.py [--write]
Without --write nothing is written (report only; work/f11_carry_report.json is the only file, counts only).
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parents[3]          # lean/c2_build
sys.path.insert(0, str(HERE))

import c2io  # noqa: E402
import c2_select as sel  # noqa: E402
import crowd_select as cs  # noqa: E402
from mixio import sha256_file  # noqa: E402

LEAN = c2io.LEAN
FAM = "F11"
R1 = LEAN / "c_src" / FAM
R1_QC = R1 / "qc" / "QC_REPORT.json"
R1_G9 = R1 / "qc" / "g9_reread.json"
R1_G13 = LEAN / "logs" / "decontam_counts" / "F11.json"
OUTQ = c2io.C2_PARTS / FAM / "qc" / c2io.QC
WORK = Path(__file__).resolve().parents[1] / "work"
CARRY_CUTOFF = "2026-10-20T23:59:00+00:00"          # spec 3.19 / A37 (d): carry-over pools, Tue 20 Oct 23:59 UTC
# The 8 Oct wording fix (WORDING_FIXES.md Task B): SEM-15 'Only if' reading rule, lex.py:120. The OLD text collided with sealed-source
# wording (>= 5-word substrings), the NEW text did too little to collide. Rows were NOT regenerated.
OLD_SEM15 = "names a condition that must also hold"
NEW_SEM15 = "adds a condition that is required too"


def utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--now", default=None, help="ISO time to stamp (default: now); refused after the carry cutoff")
    a = ap.parse_args()
    c2io.require_a38()
    now = a.now or utc_now()
    problems: list[str] = []
    rec: dict = {"family": FAM, "stage": "C2 carry-over re-gate (spec 3.19)", "tool": "c2_build/zed_orch/carry_f11/tools/f11_carry_qc.py"}
    ilog = sel.LinkGuardedInputLog()
    f = c2io.fam_files(FAM)
    cand, relf, mixdev = f["cand"], f["rel"], f["mixdev"]

    # ---- R1: the round-1 record
    sys.path.insert(0, str(LEAN / "c_build"))
    import mixer as mx  # noqa: E402
    r1 = json.loads(R1_QC.read_text(encoding="utf-8"))
    bind = mx.qc_binding(r1, {cand.name: cand, relf.name: relf})
    pool_bad = [n for n, s in (r1.get("pool_sha256") or {}).items() if not (R1 / "out" / n).exists() or sha256_file(R1 / "out" / n) != s]
    sub = {k: (r1.get(k) or {}).get("pass") for k in ("recheck", "check_5001")}
    solver_b = r1.get("g2_solver_b") or {}
    r1_ok = (r1.get("pass") is True and not r1.get("failed_gates") and not r1.get("problems") and not bind and not pool_bad
             and all(v is True for v in sub.values()) and solver_b.get("pass") is True and solver_b.get("mismatches") == 0
             and solver_b.get("pools_match_current") is True)
    rec["round1_record"] = {"file": "c_src/F11/qc/QC_REPORT.json", "sha256": sha256_file(R1_QC), "pass": r1.get("pass"),
                            "written_utc": r1.get("written_utc"), "failed_gates": r1.get("failed_gates"), "problems": r1.get("problems"),
                            "recheck_pass": sub["recheck"], "check_5001_pass": sub["check_5001"],
                            "g2_solver_b": {k: solver_b.get(k) for k in ("pass", "mismatches", "pools_match_current", "rows")},
                            "qc_binding_problems": bind, "pool_files_checked": len(r1.get("pool_sha256") or {}),
                            "pool_files_differing": pool_bad, "round1_repair_rounds": 1 if r1.get("repair_r1") else 0}
    if not r1_ok:
        problems.append(f"R1 round-1 record: binding {bind}, pool files {pool_bad}, sub {sub}")

    # ---- R2: the round-1 G9 re-read
    rows, rels, shas = sel.family_inputs(ilog, FAM)            # cs.load_family: MANIFEST + relation checks, raises on a mismatch
    g9 = json.loads(R1_G9.read_text(encoding="utf-8"))
    g9_ok = (g9.get("clearly_wrong") == [] and g9.get("ambiguous") == [] and g9.get("candidates_sha256") == shas["candidates_sha256"]
             and g9.get("n_read") == 651)
    rec["round1_g9"] = {"file": "c_src/F11/qc/g9_reread.json", "sha256": sha256_file(R1_G9), "n_read": g9.get("n_read"),
                        "clearly_wrong": len(g9.get("clearly_wrong") or []), "ambiguous": len(g9.get("ambiguous") or []),
                        "bound_to_this_candidates_file": g9.get("candidates_sha256") == shas["candidates_sha256"]}
    if not g9_ok:
        problems.append("R2 round-1 G9 re-read: not 651 rows / 0 wrong / 0 ambiguous on this candidates file")

    # ---- R3: live checks
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
    import mix_c2  # noqa: E402
    ho_rep: dict = {}
    refused = mix_c2.refuse_held_out(ilog, {FAM: rows}, ho_rep)
    sd = sel.R1_SHARDS / FAM
    shard_meta = json.loads((sd / "shards.json").read_text(encoding="utf-8"))
    shard_ok = shard_meta.get("candidates_sha256") == shas["candidates_sha256"]
    pg, view = sel.load_c1(ilog, rows, sd / f"labels_{c2io.C1}", sd)     # refuses a non-C1 / TTA / permuted view and a missing label
    r1sel = ilog.json(sel.R1_SELECT / f"select_{FAM}.json")
    sel_ids = set(r1sel["selected_ids"])
    live = {"candidate_problems": cp, "rows": len(rows), "relations": len(rels), "relation_kinds": dict(kinds),
            "relation_endpoint_missing": len(miss), "g_tw_violations": twbad, "units": len(units),
            "formats1_refuse_held_out_strict": ho_rep["fmt1_refuse_held_out"][FAM], "formats1_refused": refused,
            "shard_set_candidates_sha_equal": shard_ok, "c1_labels": len(pg),
            "c1_labels_missing": sum(1 for r in rows if r["id"] not in pg), "c1_view": view,
            "round1_select_candidates_sha_equal": r1sel.get("candidates_sha256") == shas["candidates_sha256"],
            "round1_selected": len(sel_ids), "round1_selected_not_candidates": len(sel_ids - set(by)),
            "sampler": dict(Counter((r.get("meta") or {}).get("sampler") for r in rows))}
    rec["live_checks"] = live
    if (cp or miss or twbad or refused or not shard_ok or live["c1_labels_missing"] or not live["round1_select_candidates_sha_equal"]
            or live["round1_selected_not_candidates"]):
        problems.append(f"R3 live checks failed: {json.dumps(live, default=str)[:900]}")

    # ---- R4: the old SEM-15 wording is only in rows the round-1 G13 already dropped
    g13 = json.loads(R1_G13.read_text(encoding="utf-8"))
    g13_train = (g13.get("inputs_sha256") or {}).get("train") or {}
    g13_ok = (g13.get("complete") is True and not g13.get("incomplete_why")
              and list(g13_train.values()) == [shas["candidates_sha256"]])
    drop = set(map(str, g13.get("drop_ids") or []))
    old_rows = {r["id"] for r in rows if OLD_SEM15 in json.dumps(r, ensure_ascii=False)}
    new_rows = {r["id"] for r in rows if NEW_SEM15 in json.dumps(r, ensure_ascii=False)}
    rec["wording_fix_8oct"] = {"rows_with_old_sem15_wording": len(old_rows), "of_which_in_round1_g13_drops": len(old_rows & drop),
                               "old_wording_rows_NOT_dropped": len(old_rows - drop), "rows_with_new_wording": len(new_rows),
                               "rows_regenerated_after_fix": False,
                               "lex_py_sha256_now": sha256_file(R1 / "gen" / "lex.py"),
                               "lex_py_sha256_pre_wording": sha256_file(R1 / "gen" / "tmp" / "lex.py.pre_wording"),
                               "note": "the 8 Oct fix edited the generator only; the candidates file is the 6 Oct build. Every row with the old text "
                                       "is in the round-1 drop list, so no carried row holds it"}
    rec["round1_g13_log"] = {"file": "logs/decontam_counts/F11.json", "sha256": sha256_file(R1_G13), "complete": g13.get("complete"),
                             "incomplete_why": len(g13.get("incomplete_why") or []), "drop_ids": len(drop), "drop_units": g13.get("drop_units"),
                             "train_sha256_equals_candidates": g13_ok, "tool_sha256_then": g13.get("tool_sha256"),
                             "targets_then": sorted((g13.get("targets") or {}).keys()),
                             "seeds_clean": g13.get("seeds_clean"), "seed_hit_lines": g13.get("seed_hit_lines"),
                             "drop_ids_not_candidates": len(drop - set(by))}
    if not g13_ok or old_rows - drop or drop - set(by):
        problems.append("R4 wording fix / round-1 G13 log: log not complete or not on this file, or an old-wording row is not dropped")

    # ---- R5: the selectable pool and a dry in-memory selection (nothing written)
    pool, prel, info = sel.carry_pool(FAM, rows, rels, sel_ids)
    pool_ids = {r["id"] for r in pool}
    pref_all = [r for r in pool if sel.preferred(FAM, r)]
    live_pool = [r for r in pool if r["id"] not in drop]
    pref_live = [r for r in live_pool if sel.preferred(FAM, r)]
    dry = sel.select_carry(FAM, rows, rels, pg, c2io.CARRY[FAM], sel_ids, sel.SEED, drop)
    chosen = dry["selected_ids"]
    dry_rows = [by[i] for i in chosen]
    rec["selectable_pool"] = info | {"target": c2io.CARRY[FAM], "units": len(cs.units_of(pool, prel)),
                                     "pool_rows_after_round1_g13_drops": len(live_pool),
                                     "xed_mams_rows_in_pool": len(pref_all), "xed_mams_rows_after_round1_drops": len(pref_live),
                                     "other_rows_after_round1_drops": len(live_pool) - len(pref_live)}
    rec["selection_dry_run"] = {"note": "in memory, exclude = the ROUND-1 G13 drops only (the real selection runs after the carry G13); not written to crowd_c2/",
                                "selected": len(chosen), "target": c2io.CARRY[FAM],
                                "preferred_selected": (dry.get("carry_pool") or {}).get("preferred_selected"),
                                "preferred_rows_in_pool": (dry.get("carry_pool") or {}).get("preferred_rows"),
                                "xed_mams_rows_in_selection": sum(1 for r in dry_rows if sel.preferred(FAM, r)),
                                "report_pass": (dry.get("report") or {}).get("pass"),
                                "report_checks_false": [k for k, v in ((dry.get("report") or {}).get("checks") or {}).items() if v is not True],
                                "bins": (dry.get("report") or {}).get("bins"),
                                "selected_ids_sha256": c2io.mixio.h64(*chosen) if hasattr(c2io.mixio, "h64") else None,
                                "qtype": dict(Counter(str(r.get("qtype")) for r in dry_rows)),
                                "preferred_pool_bins_after_round1_drops": dict(Counter(cs.bin_of(pg.get(r["id"])) for r in pref_live)),
                                "other_pool_bins_after_round1_drops": dict(Counter(cs.bin_of(pg.get(r["id"])) for r in live_pool if not sel.preferred(FAM, r))),
                                "why_not_all_preferred": "c2_select.select_carry runs crowd_select.select on the preferred units with the crowd bin budgets "
                                                         "(hard / medium / easy shares, seeded easy thinning); units it does not take are not refilled from the "
                                                         "preferred side, the rest part fills the shortfall (spec 3.19 'prefer', code unchanged)"}
    if len(live_pool) < c2io.CARRY[FAM] or len(chosen) < c2io.CARRY[FAM]:
        problems.append(f"R5 selectable pool {len(live_pool)} / dry selection {len(chosen)} < ceiling {c2io.CARRY[FAM]}")

    # ---- R6: the cutoff
    t_now = datetime.datetime.fromisoformat(now)
    if t_now > datetime.datetime.fromisoformat(CARRY_CUTOFF):
        problems.append(f"R6 carry cutoff {CARRY_CUTOFF} has passed (spec 3.19): the pool is left out, no refill")

    ok = not problems
    rec |= {"pass": ok, "passed_utc": now if ok else None,
            "fix_iterations": 0,
            "fix_iterations_note": "C2 fix iterations (spec 5.3 / A48 a): none. The candidates file is byte-identical to the one that passed the round-1 "
                                   "gates and was crowd-read; the 8 Oct wording fix touched the generator only and no row was regenerated. The round-1 "
                                   "repair history (one G7/G12/G15 repair round on 6 Oct) is in c_src/F11/qc/QC_REPORT.json.",
            "reasons_not_passed": problems,
            "files": {cand.name: {"sha256": shas["candidates_sha256"], "rows": len(rows)},
                      relf.name: {"sha256": shas["relations_sha256"], "rows": len(rels)}},
            "mixdev": {"mixdev_S5.jsonl": {"sha256": sha256_file(mixdev), "rows": sum(1 for _ in open(mixdev, "rb")), "layout": "round-1 (carry-over)",
                                           "note": "never trained; mix_c2.dev_items reads it as the F11 round-1 dev part"}},
            "crowd": "round-1 C1 labels (data/c_crowd_r1_shards/F11/labels_q35_4b_main500k): one view of C1, no TTA, merged, schema_branch_mark, "
                     "same settings as the C2 crowd reads; the candidates file is the one that was read, so no new read",
            "deferred_gates": ["G13 against the NEW targets: g13_c2.py carry --block F11 (orchestrator batch); the OLD targets stand on the "
                               "round-1 log logs/decontam_counts/F11.json (same candidates sha, complete true), passed to c2_select --exclude-ids and "
                               "mix_c2 --decontam-drops as a plain list",
                               "C2 selection: c2_select.py carry --fam F11 --exclude-ids <F11.json> <c2_carry_F11.json> (G9 re-read list in g5_reread_F11.json)",
                               "A42-D 8.5 source-name check of XED / MAMS: orchestrator (input prepared: zed_orch/carry_f11/SOURCES_F11_85.json)"]}
    brief = {k: rec[k] for k in ("pass", "passed_utc", "fix_iterations", "reasons_not_passed", "files")}
    print(json.dumps(brief, indent=1))
    for k in ("round1_record", "round1_g9", "wording_fix_8oct", "round1_g13_log", "selectable_pool", "selection_dry_run"):
        print(k, json.dumps(rec[k], default=str)[:1100])
    print("live", json.dumps({k: v for k, v in live.items() if k != "c1_view"}, default=str)[:900])
    WORK.mkdir(parents=True, exist_ok=True)
    c2io.write_json(WORK / "f11_carry_report.json", rec)
    if a.write:
        if not ok:
            print("NOT written: the record would not pass")
            return 1
        sha = c2io.write_json(OUTQ, rec)
        again = json.loads(OUTQ.read_text(encoding="utf-8"))
        probs = mx.qc_binding(again, {cand.name: cand, relf.name: relf})
        adm = mix_c2.admission(FAM, again, probs, cutoff=CARRY_CUTOFF)
        print("written", OUTQ.relative_to(LEAN), sha, "qc_binding", probs, "mix_c2.admission(carry cutoff)", adm)
        return 0 if not probs and not adm else 1
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
