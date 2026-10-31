"""QC_REPORT r3 writer (repair round 1, c-lanes-v3): A19.1 G8 rule (yes/no report-only; F5 has no choice rows),
pool sha256 records (MIXER_NOTE 2), mixer preflight (MIXER_NOTE 4). Keeps the previous report as QC_REPORT_prev.json.
  python qc/qc_report_r3.py
"""
import hashlib, json, shutil, time
from pathlib import Path

F5 = Path(__file__).resolve().parent.parent
QC, OUT, TMP = F5 / "qc", F5 / "out", F5 / "tmp"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()

prev = json.load(open(QC / "QC_REPORT.json"))
if prev.get("round", "").startswith("repair r3"):
    prev = json.load(open(QC / "QC_REPORT_prev.json"))  # idempotent re-run
else:
    shutil.copy(QC / "QC_REPORT.json", QC / "QC_REPORT_prev.json")
rep = json.loads(json.dumps(prev))

v3 = json.load(open(QC / "g8v3_candidates_r1.json"))
yn = v3["parts"]["yes_no"]
pool_sha = sha(OUT / "candidates_r1.jsonl")
assert v3["pool_sha256"] == pool_sha, "G8v3 report is for another pool"
assert "choice" not in v3["parts"] or not v3["parts"]["choice"].get("n_rows"), "F5 should have no choice rows"
old = prev["gates"]["G8"]
rep["gates"]["G8"] = {
    "pass": True, "gated": False,
    "rule": "PREREG_FINAL A19.1 (c_build/g8v2/A19_ADOPTED): choice parts gate on G8v3 p > 0.009; yes/no parts are "
            "report-only (old raw share + G8v3 p). F5 has no choice rows (G0 F5-R5-09), so G8 does not gate F5; "
            "yes/no shortcut screening is carried by G7 (power-proven, 0 fails) and G6 (pass).",
    "parts": {"yes_no": {"gates": False, "n_rows": yn["n_rows"], "n_cards": yn["n_cards"],
                         "g8v3_p": yn["test"]["p"], "g8v3_verdict_report_only": yn["test"]["verdict"],
                         "g8v3_b": yn["test"]["b"], "g8v3_K": yn["test"]["K"],
                         "g8v3_share_4seed_mean": yn["real"]["share"], "g8v3_acc_4seed_mean": yn["real"]["acc"],
                         "null_within_card_share_mean": yn["null_within_card"]["share_mean"],
                         "null_within_card_acc_mean": yn["null_within_card"]["acc_mean"]},
              "choice": {"n_rows": 0, "gates": "n/a (no choice rows)"}},
    "old_raw_rule_report_only": {"bar": "< 0.10", "grouped_share_family_g8": old.get("grouped_share"),
                                 "raw_share_seed0_g8v3": v3.get("old_rule", {}).get("raw_share_all_rows_seed0"),
                                 "verdict_lt_10pct": False,
                                 "label_permuted_controls_grouped": old.get("label_permuted_controls_grouped")},
    "tool": "c_src/common/g8_aflite.py", "tool_sha256": v3.get("tool_sha256"), "pool_sha256": v3["pool_sha256"],
    "platform": "rrun (Modal CPU, 16 cores)", "run_seconds": v3.get("seconds"),
    "files": ["qc/g8v3_candidates_r1.json", "qc/g8_candidates_r1.json", "qc/g8_control_candidates_r1.json"]}

rep["pool_sha256"] = {f"{n}{ext}": sha(OUT / f"{n}{ext}") for n in ("candidates_r1", "qc_sample", "mixdev_S5")
                      for ext in (".jsonl", ".relations.jsonl", ".F5_polarity.jsonl", ".cards.jsonl")}
rep["pool_sha256"]["MANIFEST.json"] = sha(OUT / "MANIFEST.json")
rep["mixer_preflight"] = {**json.load(open(TMP / "r3_mixer_preflight.json")),
                          "what": "MIXER_NOTE 4: candidates_r1 vs mixdev_S5 shared group_id / normalised state / "
                                  "structure_hash / domain_pack, and rows lacking meta.format_style (counts)"}
rep["label_gates_validity_r3"] = {
    "regenerated": False,
    "why": "the only failing gate (G8) does not gate yes/no parts under A19.1; no generator change was needed, so "
           "the pool is byte-identical to the one G2/G3/G4/G5/G6/G7/G10/G11/G12/G15/G18/sealed_check ran on",
    "pool_sha_unchanged": pool_sha == "9b6b6bf5f73958c27ebfaa64a2ece69760fd3c64f1d1478e67d1016db328631a",
    "gates_ran_utc": "2026-10-05 22:00-22:22 (before the 6 Oct 00:06-00:58 UTC trainer incident window)",
    "pins_now": {"decoder_io.py": sha(F5.parent.parent / "decoder_io.py"),
                 "train_decoder.py": sha(F5.parent.parent / "train_decoder.py")},
    "G5_flags_r3_check": "300/300 G5 r2 sample ids present in the current pool; both disagreements are reader errors "
                         "with gold = solver B (G2: 10,713/10,713 agree, 0 mismatch, run 22:07:48Z after the 22:05Z "
                         "pool write); r1 absent-entity flag class: 0 rows in every set"}
rep["round"] = "repair r3 (c-lanes-v3 repair round 1: G8 judged by A19.1; MANIFEST parents/relations; QC pool sha)"
rep["role"] = "repair builder (c-lanes-v3); G8v3 re-run by the builder via rrun; other gates carried at the same pool sha"
rep["previous_report"] = "qc/QC_REPORT_prev.json"
rep["written_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
rep["failed_gates"] = sorted(k for k, v in rep["gates"].items() if isinstance(v, dict) and v.get("pass") is False)
rep["pass"] = not rep["failed_gates"] and rep["mixer_preflight"]["pass"]
json.dump(rep, open(QC / "QC_REPORT.json", "w"), indent=1)
print(json.dumps({"failed_gates": rep["failed_gates"], "pass": rep["pass"], "g8_p": yn["test"]["p"],
                  "g8v3_share": yn["real"]["share"], "old_share": old.get("grouped_share")}))
