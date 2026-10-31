"""QC_REPORT writer, check:F3 (workflow c-lanes-v3, independent checker). Reads the gate outputs in qc/ that were run
on the current pools, hashes the pools, and writes qc/QC_REPORT.json. Counts and verdicts only; no row text.
Binding rules: spec 8 as extracted in c_spec/BUILDER_BRIEF.md; G6/G7 metadata = only what the model sees (spec 8 (d)
list, qc/specmeta.py); G8 = spec bar (< 10%) because c_build/g8v2/A19_ADOPTED does not exist, G8v2 (A19, shared
tool) reported beside it. Usage: make_qc_report_r3.py"""
import datetime, hashlib, json
from pathlib import Path

LEAN = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
F3 = LEAN / "c_src/F3"
QC = F3 / "qc"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def lines(p):
    with open(p, "rb") as f:
        return sum(1 for _ in f)


def J(name):
    p = QC / name
    return json.loads(p.read_text()) if p.exists() else None


POOLS = ["candidates_r1.jsonl", "candidates_r1.relations.jsonl", "candidates_r1.sidecar.jsonl", "qc_sample.jsonl",
         "qc_sample.relations.jsonl", "qc_sample.sidecar.jsonl", "mixdev_S5.jsonl", "mixdev_S5.relations.jsonl",
         "mixdev_S5.sidecar.jsonl"]
inputs = {n: sha(F3 / "out" / n) for n in POOLS if (F3 / "out" / n).exists()}
rows = {n: lines(F3 / "out" / n) for n in POOLS if (F3 / "out" / n).exists()}
A19 = (LEAN / "c_build/g8v2/A19_ADOPTED").exists()

g5, g6, g6p = J("g5.json"), J("g6_specmeta.json"), J("g6.json")
g7c, g7q = J("g7_specmeta_candidates_r1.json"), J("g7_specmeta_qc_sample.json")
g7cp, g7qp = J("g7_candidates_r1.json"), J("g7_qc_sample.json")
g8, g8v2 = J("g8_candidates_r1.json"), J("g8v2_candidates_r1.json")
g10, g11, g12, g15, g18 = (J("g10_candidates_r1.json"), J("g11_candidates_r1.json"), J("g12_candidates_r1.json"),
                           J("g15_candidates_r1.json"), J("g18.json"))


def g6_summary(d):
    out = {}
    for part in ("yes_no", "choice"):
        for k, v in (d or {}).get(part, {}).items():
            if isinstance(v, dict) and "best" in v:
                ch = v.get("chance", v.get("chance_mean_1_over_k"))
                out[f"{part}.{k}"] = {"best": round(v["best"], 4), "chance": round(ch, 4),
                                      "margin_pp": round(100 * (v["best"] - ch), 2), "pass": v["pass"]}
    return out


def g7_summary(d):
    if not d:
        return None
    yn = d.get("yes_no", {})
    return {"pass": d.get("pass"), "yes_no_features": yn.get("features_tested"), "yes_no_fail": yn.get("n_fail"),
            "null_fails": {k: v.get("n_fail") for k, v in yn.items() if k.startswith("null")},
            "choice_options_fail": d.get("choice_options", {}).get("n_fail"),
            "choice_abstain_fail": d.get("choice_abstain", {}).get("n_fail")}


def g8_summary(d):
    if not d:
        return None
    keep = {}
    for k, v in d.items():
        if k in ("gate", "file", "pool", "adapter", "solver", "solver_check", "model", "cache", "seconds", "jobs",
                 "rule_text", "q95_method"):
            continue
        keep[k] = v
    return keep


g8_spec_share = (g8 or {}).get("grouped_by_card", {}).get("predictable_share")
g8_spec_pass = (g8 or {}).get("pass")
gates = {
    "G5": {"pass": bool(g5 and g5["pass"]), "file": "qc/g5.json", "seed": 5001, "n": 300,
           **(g5 or {}).get("result", {})},
    "G6": {"pass": bool(g6 and g6.get("pass")), "file": "qc/g6_specmeta.json", "data": "out/qc_sample.jsonl",
           "cv": "GroupKFold(5) by meta.card_id", "rule": "acc <= chance + 2 pp",
           "metadata_features": "spec 8 (d) list only (what the model sees; qc/specmeta.py)",
           "views": g6_summary(g6),
           "report_only_with_hidden_sidecar_tags": {"file": "qc/g6.json", "pass": (g6p or {}).get("pass"),
                                                     "views": g6_summary(g6p)}},
    "G7": {"pass": bool(g7c and g7q and g7c.get("pass") and g7q.get("pass")),
           "files": ["qc/g7_specmeta_candidates_r1.json", "qc/g7_specmeta_qc_sample.json"],
           "metadata_features": "spec 8 (d) list only (what the model sees)",
           "candidates_r1": g7_summary(g7c), "qc_sample": g7_summary(g7q),
           "report_only_with_hidden_sidecar_tags": {"candidates_r1": g7_summary(g7cp), "qc_sample": g7_summary(g7qp),
                                                     "note": "fails only on the hidden QC-sidecar tag meta:sc_mechanisms (not shown to the model) under the drawn-card-rate null; every text and spec-(d) feature passes"}},
    "G8": {"A19_ADOPTED": A19,
           "judged_by": "A19 G8v2 (shared tool)" if A19 else "spec 8 bar: predictable share < 10% (qc/g8.py)",
           "spec": {"file": "qc/g8_candidates_r1.json", "pass": g8_spec_pass, "share": g8_spec_share,
                    "bar": "< 0.10", "run": "Modal CPU via rrun (run 20261005T211955_F3_3f893bf4); a local MPS run of the same script on the same pool (previous check instance) gave 0.1628 / control 0.1737, kept in qc/tmp/",
                    **{k: {kk: vv for kk, vv in (g8 or {}).get(k, {}).items() if kk in ("predictable_share", "yes_no_share", "choice_share", "by_sampler")}
                       for k in ("grouped_by_card", "instance_level", "control_permuted_labels_grouped")},
                    "real_minus_permuted_control_pp": round(100 * (g8_spec_share - (g8 or {}).get("control_permuted_labels_grouped", {}).get("predictable_share", 0)), 2) if g8_spec_share is not None else None},
           "g8v2_shared_tool": {"file": "qc/g8v2_candidates_r1.json", "pass": (g8v2 or {}).get("pass"),
                                "old_raw_share": (g8v2 or {}).get("old_rule"),
                                "parts": {pt: {"real_share": v["real"]["share"], "acc": v["real"]["acc"], "chance": v.get("chance"),
                                          "q95_within": v.get("null_within_card", {}).get("q95"), "q95_global": v.get("null_global", {}).get("q95"),
                                          "threshold": v.get("threshold"), "pass_share": v.get("pass_share"), "pass_acc": v.get("pass_acc"),
                                          "partition_seed_spread": v.get("partition_seed_spread", {}).get("shares")}
                                     for pt, v in (g8v2 or {}).get("parts", {}).items()},
                                "run": "Modal CPU via rrun, --jobs 16 (run 20261005T212010_F3_eb9cd955)"},
           "infeasibility_note": "tmp/repair/INFEASIBLE_G8.md (builder, 5 Oct): the < 10% bar sits below the cue-free floor of this procedure (permuted-label control above 10%); A19 records the same finding for F1/F4/F5"},
    "G10": {"pass": bool(g10 and g10.get("pass")), "file": "qc/g10_candidates_r1.json",
            "pool_checks_pass": (g10 or {}).get("pool_checks_pass"),
            "selection_targets": len((g10 or {}).get("selected_set_targets", [])),
            "targets_infeasible": (g10 or {}).get("targets_infeasible"),
            "targets_outside_band_on_pool_but_feasible": len((g10 or {}).get("targets_outside_band_on_pool", [])),
            "note": (g10 or {}).get("note"),
            "v4_rules_not_applicable": "commit gate/match rates, message-only route, ordinal level shares (F3 has no ordinal rows), replay hard-label rates"},
    "G11": {"pass": bool(g11 and g11.get("pass")), "file": "qc/g11_candidates_r1.json",
            "cards": (g11 or {}).get("counts", {}).get("cards", {}).get("value"),
            "packs": (g11 or {}).get("counts", {}).get("packs", {}).get("value"),
            "max_question_skeleton_share": (g11 or {}).get("surface_templates", {}).get("max_question_skeleton_share"),
            "seed_rouge_l_pairs_ge_0_7": {k: v.get("pairs_ge_0_7") for k, v in (g11 or {}).get("claude_seeds_rouge_l", {}).items() if isinstance(v, dict)},
            "unrun": (g11 or {}).get("unrun")},
    "G12": {"pass": bool(g12 and g12.get("pass")), "file": "qc/g12_candidates_r1.json",
            "exact_duplicates": (g12 or {}).get("exact_full_row_duplicates"),
            "minhash_cross_group_pairs": (g12 or {}).get("minhash_cross_group_pairs"),
            "structure_hash_violations": (g12 or {}).get("structure_hash", {}).get("violations"),
            "cross_file": (g12 or {}).get("cross_file")},
    "G15": {"pass": bool(g15 and g15.get("pass")), "file": "qc/g15_candidates_r1.json",
            **{k: (g15 or {}).get(k) for k in ("check_rows_fail", "gold_letter_map_ok", "fmt1_loader_check_fail",
                                               "units_over_3_rows", "long_units_over_2_rows", "real_tokens")},
            "rendered_prompts_read": "300 (this check's G5 blind read)"},
    "G18": {"pass": bool(g18 and g18.get("pass")), "file": "qc/g18.json", "ordinal_rows": (g18 or {}).get("ordinal_rows")},
}
g8_pass = (g8v2 or {}).get("pass") if A19 else g8_spec_pass
gates["G8"]["pass"] = bool(g8_pass)
failed = [g for g, v in gates.items() if not v["pass"]]
report = {
    "report": "F3 QC_REPORT, check:F3 (workflow c-lanes-v3; independent checker, never a generator or solver author). "
              "Gate scripts: qc/g*.py (checker-written) run on the pools below; G6/G8/G8v2 on Modal CPU via c_build/rrun.py, "
              "G7/G10/G11/G12/G15/G18 locally, all after the 20:50 local (00:50 UTC) regeneration.",
    "written_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "inputs_sha256": inputs, "rows": rows,
    "pool_sha256": {"candidates_r1.jsonl": inputs.get("candidates_r1.jsonl"),
                    "relations": inputs.get("candidates_r1.relations.jsonl")},
    "gen_version": json.loads((F3 / "out/MANIFEST.json").read_text()).get("gen_version"),
    "gates": gates,
    "builder_checks_seen": {"source": "out/candidates_r1.gates.json, out/*.sealedqc.summary.json (builder outputs, read only)",
                            "sealed_check_rows_hit": json.loads((F3 / "out/candidates_r1.sealedqc.summary.json").read_text()).get("rows_hit")},
    "previous_report": "qc/tmp/QC_REPORT_r2_prev.json (pool 6a601f34..., FAIL G6 G7 G8 G10)",
    "failed_gates": failed,
    "pass": not failed,
}
(QC / "QC_REPORT.json").write_text(json.dumps(report, indent=1))
print(json.dumps({"pass": report["pass"], "failed": failed, "A19": A19, "g8_spec_share": g8_spec_share,
                  "g8v2_pass": (g8v2 or {}).get("pass"), "cand_sha": inputs.get("candidates_r1.jsonl", "")[:16]}))
