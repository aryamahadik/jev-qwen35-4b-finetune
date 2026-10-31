#!/usr/bin/env python3
"""Compose public-1/qc/QC_REPORT.json (endgame-prep-5 independent QC agent) from the gate outputs in qc/
(gate_g1, gate_g15, gate_bal, gate_g6), the flag-only G5 verdicts (g5_verdicts.jsonl, latest verdict per sampled row),
the sealed_check summaries (qc/sealedqc/) and the full sha256 of the files mixer.py --final binds (PUBLIC_FILES and
PUBLIC_RESERVE for public-1). Counts and ids only; no row text."""
from __future__ import annotations

import collections
import hashlib
import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
P1 = HERE.parent
LEAN = P1.parents[2]

BOUND = {"public1_rows_r1.jsonl": "out/public1_rows_r1.jsonl", "public1_reserve.jsonl": "out/public1_reserve.jsonl"}
INFO_FILES = {"public1_mtdev.jsonl": "out/public1_mtdev.jsonl", "public1_templates.jsonl": "out/public1_templates.jsonl",
              "manifest_public1.json": "manifest_public1.json"}
G5_BAR = {"c_pub_squad2": (300, 0.05, "clearly wrong or ambiguous"), "c_pub_musique": (100, 0.08, "clearly wrong"),
          "c_pub_2wiki": (100, 0.08, "clearly wrong"), "c_pub_quality": (100, 0.08, "clearly wrong")}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def nrows(p):
    with open(p) as f:
        return sum(1 for ln in f if ln.strip())


def j(name):
    return json.loads((HERE / name).read_text())


def g5():
    last = {}
    for ln in open(HERE / "g5_verdicts.jsonl"):
        x = json.loads(ln)
        last[(x["ds"], x["idx"])] = x
    sample = j("g5_sample_qc.json")
    out, ok_all = {}, True
    for ds, ids in sample.items():
        n_req, bar, what = G5_BAR[ds]
        v = [last.get((ds, i)) for i in range(len(ids))]
        c = collections.Counter(x["v"] for x in v if x)
        read = sum(c.values())
        bad = c["wrong"] + (c["amb"] if "ambiguous" in what else 0)
        rate = bad / max(1, read)
        p = read >= n_req and rate <= bar
        ok_all &= p
        out[ds] = {"sample_n": len(ids), "read": read, "ok": c["ok"], "wrong": c["wrong"], "ambiguous": c["amb"],
                   "unverified": c["unv"], "bar": f"drop dataset if > {int(bar * 100)}% {what}",
                   "rate_counted": round(rate, 4), "pass": bool(p),
                   "flagged_ids": {k: [x["id"] for x in v if x and x["v"] == k] for k in ("wrong", "amb") if c[k]}}
    out["musique_wrong_pattern"] = ("all 8 are yes/no answerability rows labelled 'every step is stated' where one hop "
                                    "of the chain is not literally stated in the shown paragraphs (T-REx-style relation: "
                                    "death place, screenwriter, sibling, instrument, alma mater, birthplace) or, once, the "
                                    "answer is stated but the row is labelled unanswerable; 0 flags on choice rows")
    out["method"] = ("independent seeded sample (sha256('public1-qc-g5', id) order over rows_r1 + reserve, spec sizes "
                     "300/100/100/100), flag-only, reading only decoder_io.user_msg (cygnet, schema_branch_mark, seeded "
                     "option order) with the gold letter; SQuAD/MuSiQue/2Wiki read whole; QuALITY read through the same "
                     "rendered text with question/option-matched windows plus keyword views, widened until each gold "
                     "could be confirmed or refuted; no label edited")
    out["pass"] = bool(ok_all)
    return out


def g6_summary():
    if not (HERE / "gate_g6.json").exists():
        return {"pass": False, "status": "not finished"}
    d = j("gate_g6.json")
    cells = {}
    for scope in ("qc_sample", "rows", "pool"):
        for cell, views in d.get(scope, {}).items():
            for v, x in views.items():
                if "best" in x:
                    cells[f"{scope}|{cell}|{v}"] = {"best": x["best"], "chance": x["chance"], "n": x["n"],
                                                    "pass": x["pass"]}
    judged = {k: v for k, v in cells.items() if k.startswith("qc_sample|")}
    worst = sorted(judged.items(), key=lambda kv: kv[1]["best"] - kv[1]["chance"], reverse=True)[:8]
    return {"pass": d["pass"], "fail": d["fail"], "cells_judged_qc_sample": len(judged),
            "qc_sample_files": d.get("qc_sample_files"),
            "worst_margin_cells_qc_sample": {k: v for k, v in worst},
            "info_fail_rows_pool": d.get("info_fail_small_n", {}), "note": d.get("note")}


def unused_summary():
    """spec 3.1 (v2) only-unused-records + passage dedup vs C1's sources (qc/qc_unused.py -> gate_unused.json)."""
    if not (HERE / "gate_unused.json").exists():
        return {"pass": False, "status": "not run"}
    d = j("gate_unused.json")
    return {k: d.get(k) for k in ("pass", "failing_rows", "failing_ids_first20", "files", "secs")} | {
        "rule": "a row fails on any full state / line (>= 6 words) / sentence (>= 8 words) / option (>= 6 words) equal "
                "to a golden_train unit, or ANY shared word 10-gram with golden_train (indexes rebuilt from "
                "data/v14_parts/golden_train.jsonl here, not the builder's)"}


def g5_status(g5_out):
    """G5 verdicts are only valid for the rows they read: if the sampled ids are no longer in the bound files, the
    read is stale and G5 is pending (a separate session re-samples and reads; the builder never reads G5)."""
    ids = set()
    for rel in BOUND.values():
        for ln in open(P1 / rel):
            ids.add(json.loads(ln)["id"])
    sample = j("g5_sample_qc.json")
    stale = {ds: sum(1 for i in v if i not in ids) for ds, v in sample.items()}
    if any(stale.values()):
        return {"pass": False, "status": "PENDING: rows regenerated in repair round 1; previous read is stale",
                "sampled_ids_missing_now": stale, "previous_read": g5_out}
    return g5_out


def main():
    g1, g15, bal = j("gate_g1.json"), j("gate_g15.json"), j("gate_bal.json")
    files = {name: {"path": rel, "sha256": sha(P1 / rel), "rows": nrows(P1 / rel)} for name, rel in BOUND.items()}
    info = {name: {"path": rel, "sha256": sha(P1 / rel)} for name, rel in INFO_FILES.items()}
    sealed = {}
    for f in sorted((HERE / "sealedqc").glob("*.summary.json")):
        s = json.loads(f.read_text())
        sealed[f.name.replace(".summary.json", "")] = {k: s.get(k) for k in ("rows", "rows_hit", "rows_clean",
                                                                             "rows_report_only", "checker_sha256",
                                                                             "suite_sha256")}
    sealed_pass = all(v["rows_hit"] == 0 for v in sealed.values()) and len(sealed) == 4
    gates = {
        "G1_provenance_licence": {
            "pass": g1["pass"], "fail": g1["fail"], "row_meta_missing": g1["row_meta_missing"],
            "datasets": {s: {k: x[k] for k in ("rows", "licence", "licence_allowed", "record_in_register_1_2",
                                               "has_url_commit", "rows_meta_licence_incomplete", "rows_share_alike",
                                               "parents_declared", "saved_record_sha_match", "pass")} |
                         {"reread_now": {k: x["reread_now"][k] for k in ("url", "same_bytes_as_recorded",
                                                                          "licence_stated", "utc")}}
                         for s, x in g1["datasets"].items()},
            "quality_document_text": g1["quality_text_licence"], "oanc_terms_reread": g1["oanc_terms_reread"]},
        "denylist_3H": {"pass": g1["denylist"]["exit"] == 0, "exit": g1["denylist"]["exit"],
                        "lines": g1["denylist"]["lines"], "program_sha256": g1["denylist"]["denylist_program_sha256"],
                        "query": "qc/denylist_query_qc.json", "verdicts": "qc/denylist_verdicts_qc.json"},
        "G5_blind_read": g5_status(g5()),
        "unused_records_3_1": unused_summary(),
        "G6_partial_input": g6_summary(),
        "G7_feature_z": {
            "pass": not any(k.startswith("G7") for k in bal["fail"]),
            "rule": "one-sided binomial per unigram/bigram/metadata feature, p0 = 1/k, Bonferroni alpha 0.01 over all "
                    "features tested per set; option position is not tested (train_decoder re-shuffles options on "
                    "every draw, spec 2.1 'the trainer shuffles again at train time')",
            "by_set": {f"{sc}|{s}": {"features_tested": x["features_tested"], "failing": x["failing_features"],
                                     "top": x["top_failing"][:4]}
                       for sc in ("rows", "pool") for s, x in bal[f"G7_{sc}"].items()}},
        "G10_balance": {
            "pass": not any(k.startswith("G10") for k in bal["fail"]),
            "fail": {k: v for k, v in bal["fail"].items() if k.startswith("G10")},
            "yes_rate_by_dataset": bal["G10_rows"]["yes_rate_by_dataset"],
            "yes_rate_cells": {sc: {k: bal[f"G10_{sc}"].get(k) for k in ("yn_cells_k_all", "yn_cells_k_syn", "min_cell_n",
                                                                         "cells_outside_50pm2_k_all",
                                                                         "cells_outside_50pm2_k_syn")}
                               for sc in ("rows", "pool")},
            "cell_rule": "spec 8 exactly: EVERY cell dataset x wording_id x difficulty_bin x negation count in 50 +/- 2 "
                         "(no small-cell exemption), negation count read as negcount.k_all(instructions) and as "
                         "negcount.k_syn(framing question); a cell off-band under either fails",
            "longest_is_gold_per_bucket": {sc: bal[f"G10_{sc}"].get("longest_is_gold") for sc in ("rows", "pool")},
            "longest_is_gold_per_dataset": {sc: bal[f"G10_{sc}"]["longest_is_gold_per_dataset"] for sc in ("rows", "pool")},
            "gold_letter_chi2_p": {k: v["chi2_p"] for k, v in bal["G10_rows"]["gold_letter"].items()},
            "abstain_wrong_share": {sc: bal[f"G10_{sc}"]["abstain"] for sc in ("rows", "pool")},
            "attack_rows": bal["G10_rows"]["attack_rows"]},
        "G12_dedup": {"pass": not any(k.startswith("G12") for k in bal["fail"]),
                      "rows": bal["G12_rows"], "pool": bal["G12_pool"],
                      "rule": "exact hash 0; MinHash word 5-grams Jaccard >= 0.8 (verified exactly) across group_ids; "
                              "structure_hash one group per value; same item text across groups 0"},
        "G15_loader": {"pass": g15["pass"], "fail": g15["fail"],
                       **{p: {k: v for k, v in g15[p].items() if k != "loader_fail_kinds"} for p in ("rows", "reserve", "dev")},
                       "read_20_per_dataset": g15["read_20_per_dataset"]},
        "dev_separation": {"pass": not any(bal["dev_separation"].values()), "clashes": bal["dev_separation"]},
        "sealed_check": {"pass": sealed_pass, "files": sealed,
                         "checker": "lean/sealed_nd/qc/sealed_check.py (run as a program; qc/run_sealed_qc.sh)"},
        "G13_decontamination": {"status": "not run here: orchestrator counts-only tool (RUNBOOK section B); "
                                          "not counted in this record's pass"},
    }
    required = [k for k in gates if k != "G13_decontamination"]
    failed = [k for k in required if not gates[k].get("pass")]
    rep = {
        "builder": "public-1", "record": "qc/QC_REPORT.json",
        "checker": ("repair round 1 (PREREG A29 a): gates re-run by the repair:public-1 session with the qc/ scripts "
                    "(spec 8 exact); the 6 Oct record by the independent endgame-prep-5 QC agent is qc/QC_REPORT_prev.json. "
                    "An independent re-check and a fresh G5 read by a separate session are still required"),
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "spec": "C_DATA_SPEC v4 section 8: public rows pass G1, G6 (on our framings), G7, G10, G12, G13, G15 and a G5 "
                "read of 100 rows per dataset (300 for SQuAD 2.0); 3.H deny-list; sealed_check",
        "pass": not failed, "failed_gates": failed, "required_gates": required,
        "files": files, "info_files": info,
        "gates": gates,
        "checker_scripts": {f"qc/{p.name}": sha(p) for p in sorted(HERE.glob("*.py"))} |
                           {"qc/run_sealed_qc.sh": sha(HERE / "run_sealed_qc.sh")},
        "checker_fixes": [
            "choice gold is stored as option text: gold index via options.index(gold) (first run mis-indexed it)",
            "G1: the register needs the official record URL, not the commit; per-row text note is wording-free "
            "('Wikipedia' / QuALITY per-article check), not a literal 'text:' tag",
            "abstain regex: a bare 'neither' matched a film title; abstain phrasings only",
            "G7/G6: stored option position dropped (not model-visible: options re-shuffled every draw)",
            "repair r1 (A29 a): G10 yes-rate cells: the non-spec small-cell binomial rule removed; every cell in "
            "50 +/- 2 under both negation-count readings",
            "repair r1: G10 longest-is-gold gating per dataset AND per (dataset, k) bucket; gold-letter chi-square in "
            "every bucket (n >= 5k exemption removed)",
            "repair r1: G6 judged on the spec's separate QC sample (>= 5,000 rows per Wikipedia set, tmp/qcs_<ds>.json; "
            "QuALITY rows + reserve, fewer real rows); best of LR/GBT <= chance + 2 pp, no p-value condition",
            "repair r1: spec 3.1 (v2) unused-records / golden_train 10-gram gate added (qc/qc_unused.py)",
        ],
        "repair": "builder fixed (record selection, option construction, abstain policy, balance logic) and every "
                  "output regenerated; no row hand-edited, relabelled or cherry-picked",
    }
    (HERE / "QC_REPORT.json").write_text(json.dumps(rep, indent=1, default=str))
    print("pass", rep["pass"], "failed", failed)


if __name__ == "__main__":
    main()
