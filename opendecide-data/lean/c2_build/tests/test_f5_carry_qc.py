"""Tests for zed_orch/f5_carry_qc.py (the F5 carry-over QC-record writer, Ruling A66 a). Synthetic gate-output files in a
temp folder; fault injection proves every re-derivation check bites (one fault, one failing gate). No OHS / sealed path
is opened. Run from lean/:
  ../.venv/bin/python -m pytest -q c2_build/tests/test_f5_carry_qc.py
"""
from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(C2B / "zed_orch"))
import f5_carry_qc as w  # noqa: E402

SAMPLERS = {"S1": 50, "S2": 50, "S3": 50, "S4": 50}
CAND_SHA = "a" * 64


def live_base() -> dict:
    return {"rows": 200, "qc_sample_rows": 150, "mixdev_rows": 40, "samplers": dict(SAMPLERS), "gold_yes": 100,
            "gold_by_sampler": {k: 25 for k in SAMPLERS}, "relations": 20, "relation_kinds": {"complement": 5, "equiv": 5, "inv": 10},
            "units": 95, "unit_sizes": {1: 80, 2: 10, 3: 5}, "cards": 120, "packs": 32, "choice_rows": 0, "cand_sha": CAND_SHA,
            "dups": 0}


def gate_files() -> dict:
    """{relative path: content} of a passing set of gate-output files for live_base()."""
    lv = live_base()
    n = {"candidates_r1": lv["rows"], "qc_sample": lv["qc_sample_rows"], "mixdev_S5": lv["mixdev_rows"]}
    f: dict = {}
    f["solverB/mismatch.json"] = {"files": {"candidates_r1.jsonl": 200, "qc_sample.jsonl": 150, "mixdev_S5.jsonl": 40},
                                  "rows_checked": 390, "agree": 390, "agree_pct": 100.0, "n_mismatch": 0, "n_undetermined": 0,
                                  "n_unparsed": 0, "by_sampler": {"S1:agree": 200, "S2:agree": 190}, "mismatches": [], "unparsed": []}
    for s, c in n.items():
        f[f"out/{s}.gates.json"] = {"set": s, "G3": {"rows": c, "rows_ok": c, "pass": True, "errors": []},
                                    "G15": {"ok": c, "units": lv["units"] if s == "candidates_r1" else 7, "unit_over_3": 0,
                                            "rel_split": 0, "pass": True, "errors": [], "token_cap": 1900,
                                            "served_tokens": {"max": 1898, "min": 400, "median": 1200, "p95": 1800}}}
        f[f"out/{s}.G4.json"] = {"set": s, "counts": {"S1:rows": 50, "S1:MR1:pass": 40, "S1:MR1:n/a": 10, "S2:rows": 50, "S2:MR5:pass": 50},
                                 "errors": []}
    tot = {"n": 300, "agree": 299, "agreement": 0.9967, "clearly_wrong": 0, "ambiguous": 0}
    f["qc/g5_wording.json"] = {"sha256": CAND_SHA, "pass": True, "sample": {"n": 300}, "total": dict(tot),
                               "carried": {"n": 287, "agree": 286, "clearly_wrong": 0, "ambiguous": 0},
                               "fresh": {"n": 13, "agree": 13, "clearly_wrong": 0, "ambiguous": 0}}
    f["qc/g5_wording_pre_g10fix.json"] = {"pass": True, "total": {"n": 300, "agree": 299, "clearly_wrong": 0, "ambiguous": 0}}
    f["qc/g5_a32.json"] = {"pass": True, "total": {"n": 300, "agree": 298, "clearly_wrong": 0, "ambiguous": 0}}
    f["qc/g5_r2.json"] = {"pass": True, "n_answered": 300, "n_clearly_wrong": 0, "n_ambiguous": 0}
    gated = {k: 0.4 for k in w.G6_GATED}
    f["qc/g6_qc_sample.json"] = {"set": "qc_sample", "n": 150, "gated": gated, "max_gated": 0.4, "bar": 0.52, "pass": True}
    for s in ("candidates_r1", "qc_sample"):
        f[f"qc/g7_{s}.json"] = {"set": s, "rows": n[s], "features_tested": 8000, "n_fail": 0, "fails": [],
                                "n_fail_at_50k_denominator": 0, "n_fail_text": 0, "n_fail_meta": 0, "pass": True}
        cells = {k: {"cells": {"x": {"n": 300, "yes": 0.5}}} for k in w.G10_A_CELLS}
        cells["sampler"] = {"cells": {k: {"n": v, "yes": 0.5} for k, v in SAMPLERS.items()}}
        quotas = {}
        for k, (lo, hi) in w.G10_Q_RANGE.items():
            quotas[k] = {"v": (lo + hi) / 2 if lo is not None and hi is not None else (lo if lo is not None else (hi if hi else 0))}
        quotas["cards"] = {"v": lv["cards"] if s == "candidates_r1" else 80}
        quotas["attack_present_vs_label"] = {"chi2_p": 0.5}
        quotas["verbatim_overlap"] = {"share_of_jq>=1": 0.2, "yes": 0.5}
        quotas["per_card_rate_vs_r_card"] = {"n_off": 0}
        f[f"qc/g10_{s}.json"] = {"set": s, "rows": n[s], "A_construction": {"overall": {"n": n[s], "yes": 0.5, "pass": True}, **cells},
                                 "A_quotas": quotas, "B_wording_bin_kall": {"n_fail_raw": 0, "feasible_rows_after_exact_balancing": 4000}}
        f[f"qc/g12_{s}.json"] = {"rows": n[s], "exact_dup_model_view": 0, "exact_dup_raw_fields": 0,
                                 "minhash_question_plus_record": {"pairs_ge_0.8": 4, "planned_twin_pairs": 4, "non_twin_pairs": 0},
                                 "minhash_record_only_info": {"base_pairs_ge_0.8": 3, "non_pair_base_pairs": 0},
                                 "structure_hash_generator": {"hashes_spanning_bases": 0, "bases_with_several_hashes": 0},
                                 "structure_hash_independent": {"keys_spanning_non_twin_bases": 0}}
        f[f"qc/g15_g18_{s}.json"] = {"rows": n[s], "loader_check_fail": 0, "roundtrip_gold_fail": 0, "relations": lv["relations"],
                                     "relation_types": dict(lv["relation_kinds"]), "relations_split_call_id": 0,
                                     "relations_missing_rows": 0, "relations_gold_inconsistent": 0, "call_units": lv["units"],
                                     "unit_size_hist": {str(k): v for k, v in lv["unit_sizes"].items()}, "units_gt3": 0,
                                     "units_long_gt2": 0, "tokens_full_chat_prompt": {"max": 1898, "rows_gt_1900_F5_cap": 0, "rows_gt_7900": 0},
                                     "G18": {"ordinal_rows": 0, "applies": False, "pass": True}, "G15_pass": True}
    f["qc/g8_candidates_r1.json"] = {"rows": 200, "pass": False}              # raw old-rule verdict: report-only, never gates
    f["qc/g11_candidates_r1.json"] = {"rows": 200, "counts": {"by_sampler": dict(SAMPLERS), "training_samplers": ["S1", "S2", "S3", "S4"],
                                                              "S5_rows": 0, "max_sampler_rows": 50, "packs": 32, "cards": 120,
                                                              "cards_with_one_sampler_pack": 120, "held_out_style_rows": 0},
                                      "two_pct": {"frame_x_template": {"max_share": 0.0087}, "question_skeleton": {"max_share": 0.0059}},
                                      "seeds_rouge_l": {"wordings": {"pairs_ge_0.7": 0}}}
    return f


def r1_gates() -> dict:
    """The round-1 record's gates block as it must agree with gate_files()."""
    f = gate_files()
    return {"G2": {"agree": 390}, "G6": {"max_gated_grouped_by_card": 0.4}, "G7": {"features_tested": [8000, 8000]},
            "G11": {"counts": {"max_sampler_rows": 50}}, "G5": {"total": f["qc/g5_wording.json"]["total"]}}


def put(root: Path, files: dict) -> None:
    for rel, d in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(d))


def set_path(d, path, value):
    for k in path[:-1]:
        d = d[k]
    d[path[-1]] = value


@pytest.fixture
def root(tmp_path):
    assert w.c2io.refusal(tmp_path) is None
    put(tmp_path, gate_files())
    return tmp_path


def run(root, live=None, r1=None):
    reader = w.GateReader(root)
    gates, problems = w.rederive_gates(reader, live or live_base(), r1_gates() if r1 is None else r1)
    return gates, problems, reader


def test_baseline_passes_and_records_shas(root):
    gates, problems, reader = run(root)
    assert problems == [], problems
    assert all(v["pass"] for v in gates.values())
    assert set(gates) >= {"G2", "G3", "G4", "G5", "G6", "G7", "G8", "G10", "G11", "G12", "G15", "G18", "round1_consistency"}
    assert gates["G8"]["gated"] is False
    # every gate file read is sha-bound and the shas equal the bytes on disk
    assert len(reader.files) == len(gate_files())
    for rel, meta in reader.files.items():
        assert meta["sha256"] == w.sha256_file(root / rel)
    assert set(gates["G6"]["files"]) == {"qc/g6_qc_sample.json"}


# (gate, file, path into the JSON, bad value): one fault, the named gate must fail
FAULTS = [
    ("G2", "solverB/mismatch.json", ["n_mismatch"], 1),
    ("G2", "solverB/mismatch.json", ["agree"], 389),
    ("G2", "solverB/mismatch.json", ["n_undetermined"], 2),
    ("G2", "solverB/mismatch.json", ["n_unparsed"], 1),
    ("G2", "solverB/mismatch.json", ["mismatches"], [{"id": "x"}]),
    ("G2", "solverB/mismatch.json", ["files", "candidates_r1.jsonl"], 199),        # stale: other candidates file
    ("G2", "solverB/mismatch.json", ["rows_checked"], 391),
    ("G2", "solverB/mismatch.json", ["agree_pct"], 99.0),
    ("G3", "out/candidates_r1.gates.json", ["G3", "rows_ok"], 199),
    ("G3", "out/qc_sample.gates.json", ["G3", "errors"], ["bad row"]),
    ("G3", "out/mixdev_S5.gates.json", ["G3", "rows"], 41),
    ("G4", "out/candidates_r1.G4.json", ["errors"], ["MR1 fail"]),
    ("G4", "out/qc_sample.G4.json", ["counts", "S1:MR1:fail"], 3),
    ("G4", "out/mixdev_S5.G4.json", ["counts"], {"S1:rows": 50}),                   # no passing checks at all
    ("G4", "out/candidates_r1.G4.json", ["counts", "S1:rows"], 51),                 # above the live sampler rows
    ("G5", "qc/g5_wording.json", ["sha256"], "b" * 64),                             # stale candidates sha
    ("G5", "qc/g5_wording.json", ["pass"], False),
    ("G5", "qc/g5_wording.json", ["total", "clearly_wrong"], 1),
    ("G5", "qc/g5_wording.json", ["fresh", "clearly_wrong"], 1),
    ("G5", "qc/g5_wording.json", ["total", "ambiguous"], 4),
    ("G5", "qc/g5_wording.json", ["total", "n"], 299),
    ("G5", "qc/g5_wording.json", ["total", "agree"], 300),
    ("G5", "qc/g5_wording.json", ["total", "agreement"], 0.99),
    ("G5", "qc/g5_wording_pre_g10fix.json", ["pass"], False),
    ("G5", "qc/g5_a32.json", ["total", "clearly_wrong"], 1),
    ("G5", "qc/g5_r2.json", ["n_ambiguous"], 4),
    ("G6", "qc/g6_qc_sample.json", ["gated", "a_question.lr_grouped"], 0.5201),
    ("G6", "qc/g6_qc_sample.json", ["gated", "d_meta.gbt_grouped"], 0.53),
    ("G6", "qc/g6_qc_sample.json", ["n"], 149),
    ("G6", "qc/g6_qc_sample.json", ["max_gated"], 0.3),                             # reported max not the max of the values
    ("G7", "qc/g7_candidates_r1.json", ["n_fail"], 1),
    ("G7", "qc/g7_qc_sample.json", ["fails"], [{"feature": "x"}]),
    ("G7", "qc/g7_candidates_r1.json", ["n_fail_at_50k_denominator"], 1),
    ("G7", "qc/g7_qc_sample.json", ["features_tested"], 0),
    ("G7", "qc/g7_candidates_r1.json", ["rows"], 199),
    ("G10", "qc/g10_candidates_r1.json", ["A_construction", "overall", "yes"], 0.53),
    ("G10", "qc/g10_candidates_r1.json", ["A_construction", "k_neg", "cells", "x", "yes"], 0.53),
    ("G10", "qc/g10_qc_sample.json", ["A_construction", "j_t", "cells", "x", "yes"], 0.54),
    ("G10", "qc/g10_candidates_r1.json", ["A_construction", "cue_family", "cells", "x", "yes"], 0.54),
    ("G10", "qc/g10_candidates_r1.json", ["A_quotas", "yes_is_bad_share", "v"], 0.44),
    ("G10", "qc/g10_qc_sample.json", ["A_quotas", "decoy_rows", "v"], 0.09),
    ("G10", "qc/g10_candidates_r1.json", ["A_quotas", "deep_rows", "v"], 0.11),
    ("G10", "qc/g10_candidates_r1.json", ["A_quotas", "label_check_form_rows", "v"], 1),
    ("G10", "qc/g10_candidates_r1.json", ["A_quotas", "attack_present_vs_label", "chi2_p"], 0.01),
    ("G10", "qc/g10_candidates_r1.json", ["A_quotas", "verbatim_overlap", "share_of_jq>=1"], 0.14),
    ("G10", "qc/g10_candidates_r1.json", ["A_quotas", "per_card_rate_vs_r_card", "n_off"], 1),
    ("G10", "qc/g10_candidates_r1.json", ["B_wording_bin_kall", "n_fail_raw"], 1),
    ("G10", "qc/g10_qc_sample.json", ["B_wording_bin_kall", "feasible_rows_after_exact_balancing"], 3599),
    ("G10", "qc/g10_candidates_r1.json", ["A_construction", "sampler", "cells", "S1", "n"], 49),   # live cross-binding
    ("G10", "qc/g10_candidates_r1.json", ["A_quotas", "cards", "v"], 121),
    ("G11", "qc/g11_candidates_r1.json", ["counts", "S5_rows"], 1),
    ("G11", "qc/g11_candidates_r1.json", ["counts", "max_sampler_rows"], 2501),
    ("G11", "qc/g11_candidates_r1.json", ["counts", "packs"], 29),
    ("G11", "qc/g11_candidates_r1.json", ["counts", "held_out_style_rows"], 1),
    ("G11", "qc/g11_candidates_r1.json", ["counts", "cards_with_one_sampler_pack"], 119),
    ("G11", "qc/g11_candidates_r1.json", ["counts", "training_samplers"], ["S1", "S2", "S3"]),
    ("G11", "qc/g11_candidates_r1.json", ["two_pct", "frame_x_template", "max_share"], 0.0201),
    ("G11", "qc/g11_candidates_r1.json", ["two_pct", "question_skeleton", "max_share"], 0.021),
    ("G11", "qc/g11_candidates_r1.json", ["seeds_rouge_l", "wordings", "pairs_ge_0.7"], 1),
    ("G11", "qc/g11_candidates_r1.json", ["counts", "by_sampler"], {"S1": 51, "S2": 49, "S3": 50, "S4": 50}),
    ("G12", "qc/g12_candidates_r1.json", ["exact_dup_model_view"], 1),
    ("G12", "qc/g12_qc_sample.json", ["exact_dup_raw_fields"], 2),
    ("G12", "qc/g12_candidates_r1.json", ["minhash_question_plus_record", "non_twin_pairs"], 1),
    ("G12", "qc/g12_qc_sample.json", ["structure_hash_generator", "hashes_spanning_bases"], 1),
    ("G12", "qc/g12_candidates_r1.json", ["structure_hash_independent", "keys_spanning_non_twin_bases"], 1),
    ("G12", "qc/g12_qc_sample.json", ["rows"], 151),
    ("G15", "out/candidates_r1.gates.json", ["G15", "unit_over_3"], 1),
    ("G15", "out/qc_sample.gates.json", ["G15", "rel_split"], 1),
    ("G15", "out/mixdev_S5.gates.json", ["G15", "served_tokens", "max"], 1901),
    ("G15", "out/candidates_r1.gates.json", ["G15", "token_cap"], 2000),               # a loosened cap in the file is refused
    ("G15", "out/candidates_r1.gates.json", ["G15", "units"], 94),
    ("G15", "qc/g15_g18_candidates_r1.json", ["tokens_full_chat_prompt", "max"], 1901),
    ("G15", "qc/g15_g18_qc_sample.json", ["units_gt3"], 1),
    ("G15", "qc/g15_g18_candidates_r1.json", ["loader_check_fail"], 1),
    ("G15", "qc/g15_g18_candidates_r1.json", ["roundtrip_gold_fail"], 1),
    ("G15", "qc/g15_g18_candidates_r1.json", ["relations_split_call_id"], 1),
    ("G15", "qc/g15_g18_candidates_r1.json", ["relations"], 21),
    ("G15", "qc/g15_g18_candidates_r1.json", ["unit_size_hist", "3"], 6),
    ("G18", "qc/g15_g18_candidates_r1.json", ["G18", "ordinal_rows"], 1),
    ("G18", "qc/g15_g18_qc_sample.json", ["G18", "applies"], True),
]


@pytest.mark.parametrize("gate,rel,path,bad", FAULTS, ids=[f"{g}:{Path(r).stem}:{'.'.join(map(str, p))}={b}" for g, r, p, b in FAULTS])
def test_fault_injection_bites(root, gate, rel, path, bad):
    p = root / rel
    d = json.loads(p.read_text())
    set_path(d, path, bad)
    p.write_text(json.dumps(d))
    gates, problems, _ = run(root)
    assert not gates[gate]["pass"], f"{gate} did not fail on {rel} {path}={bad}"
    assert problems


def test_round1_consistency_bites(root):
    r1 = r1_gates()
    for mut in (lambda g: g["G2"].__setitem__("agree", 389), lambda g: g["G6"].__setitem__("max_gated_grouped_by_card", 0.41),
                lambda g: g["G7"].__setitem__("features_tested", [8000, 7999]),
                lambda g: g["G11"]["counts"].__setitem__("max_sampler_rows", 49),
                lambda g: g["G5"]["total"].__setitem__("agree", 298)):
        g = copy.deepcopy(r1)
        mut(g)
        gates, problems, _ = run(root, r1=g)
        assert not gates["round1_consistency"]["pass"] and problems


def test_missing_gate_file_never_passes(root):
    for rel in gate_files():
        gate = (root / rel)
        saved = gate.read_bytes()
        gate.unlink()
        gates, problems, _ = run(root)
        assert problems, rel
        assert not all(v["pass"] for v in gates.values()), rel
        gate.write_bytes(saved)
    assert run(root)[1] == []


def test_unparsable_gate_file_never_passes(root):
    (root / "qc/g6_qc_sample.json").write_text("{not json")
    gates, problems, _ = run(root)
    assert not gates["G6"]["pass"] and problems


def test_bars_come_from_the_writer_not_the_file(root):
    """A file that claims a looser bar / its own pass flag does not move the writer's bar."""
    p = root / "qc/g6_qc_sample.json"
    d = json.loads(p.read_text())
    d["gated"]["c_card_noq.gbt_grouped"] = 0.60
    d["max_gated"] = 0.60
    d["bar"] = 0.70
    d["pass"] = True
    p.write_text(json.dumps(d))
    assert not run(root)[0]["G6"]["pass"]
    p = root / "out/candidates_r1.gates.json"
    d = json.loads(p.read_text())
    d["G15"]["token_cap"] = 4000
    d["G15"]["served_tokens"]["max"] = 3000
    d["G15"]["pass"] = True
    p.write_text(json.dumps(d))
    assert not run(root)[0]["G15"]["pass"]


def test_edited_gate_file_changes_recorded_sha(root):
    _, _, r0 = run(root)
    p = root / "qc/g12_qc_sample.json"
    d = json.loads(p.read_text())
    d["minhash_question_plus_record"]["pairs_ge_0.8"] = 5
    p.write_text(json.dumps(d))
    _, _, r1 = run(root)
    assert r0.files["qc/g12_qc_sample.json"]["sha256"] != r1.files["qc/g12_qc_sample.json"]["sha256"]


LIVE_FAULTS = [("rows", 201), ("qc_sample_rows", 151), ("mixdev_rows", 41), ("gold_yes", 99), ("units", 96), ("relations", 21),
               ("cards", 121), ("packs", 33), ("cand_sha", "c" * 64), ("dups", 1), ("choice_rows", 1),
               ("samplers", {"S1": 51, "S2": 49, "S3": 50, "S4": 50}), ("unit_sizes", {1: 81, 2: 10, 3: 5}),
               ("relation_kinds", {"complement": 6, "equiv": 5, "inv": 10})]


@pytest.mark.parametrize("key,bad", LIVE_FAULTS, ids=[k for k, _ in LIVE_FAULTS])
def test_live_stats_cross_binding_bites(root, key, bad):
    live = live_base()
    live[key] = bad
    gates, problems, _ = run(root, live=live)
    assert problems and not all(v["pass"] for v in gates.values()), key


def test_g10_cue_family_cells_below_n_min_are_not_gated(root):
    p = root / "qc/g10_candidates_r1.json"
    d = json.loads(p.read_text())
    d["A_construction"]["cue_family"]["cells"]["small"] = {"n": 199, "yes": 0.6}      # n_min is 200 for cue_family
    p.write_text(json.dumps(d))
    assert run(root)[0]["G10"]["pass"]
    d["A_construction"]["cue_family"]["cells"]["small"] = {"n": 200, "yes": 0.6}
    p.write_text(json.dumps(d))
    assert not run(root)[0]["G10"]["pass"]


def test_g8_is_report_only_for_yes_no(root):
    gates, problems, _ = run(root)           # the file's raw verdict is pass False and the gate still passes
    assert gates["G8"]["pass"] and problems == []
    live = live_base()
    live["choice_rows"] = 3                  # choice rows would make G8 gate: refused here
    assert not run(root, live=live)[0]["G8"]["pass"]


def test_reader_refuses_never_open_paths(tmp_path):
    (tmp_path / "out").mkdir()
    (tmp_path / "out" / "sealed_check_summary.json").write_text("{}")
    reader = w.GateReader(tmp_path)
    with pytest.raises(w.c2io.C2Refused):
        reader.json("out/sealed_check_summary.json")
    assert reader.files == {}
    d = tmp_path / "ohs_x"
    d.mkdir()
    (d / "a.json").write_text("{}")
    with pytest.raises(w.c2io.C2Refused):
        w.GateReader(tmp_path).json("ohs_x/a.json")


def test_writer_never_names_a_sealed_or_ohs_path():
    src = Path(w.__file__).read_text()
    code = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith("#") and "GATE_NEVER_RE =" not in l)   # the guard regex itself
    quoted = re.findall(r"""["']([^"'\n]*)["']""", code.split("GATES_PENDING = [")[0])
    assert not [q for q in quoted if re.search(r"ohs|sealed_brief|sealed_check_summary|preread|quarantine|longbench", q, re.I)]
    assert "sealed_check_summary" not in "".join(w.GATE_FILES[k][s] for k in w.GATE_FILES for s in w.GATE_FILES[k])


def test_jsonl_lines_split_on_newline_only(tmp_path):
    p = tmp_path / "x.jsonl"
    rows = [{"id": "a", "t": "x y\u0085z\x1cw"}, {"id": "b", "t": "q\x0bq\x0cq"}, {"id": "c", "t": "plain"}]
    p.write_bytes(("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n\n").encode())
    assert len(p.read_text(encoding="utf-8").splitlines()) > 3          # splitlines would over-count: why it is not used
    assert w.count_jsonl_rows(p) == 3
    assert [json.loads(x)["id"] for x in w.jsonl_lines(p)] == ["a", "b", "c"]
    assert w.GateReader(tmp_path).count_rows("x.jsonl") == 3


def test_backup_existing_none_when_no_record(tmp_path):
    assert w.backup_existing(tmp_path / "QC_REPORT.json", tmp_path / "bk", "T") is None
    assert not (tmp_path / "bk").exists()


def test_backup_before_write_and_original_preserved(tmp_path):
    out, bk = tmp_path / "qc" / "QC_REPORT.json", tmp_path / "bk"
    out.parent.mkdir()
    out.write_text('{"old": 1}')
    seen = {}

    def writer(path, obj):
        seen["backups"] = sorted(p.name for p in bk.iterdir())            # the backup exists BEFORE the record is replaced
        seen["old_still"] = Path(path).read_text()
        Path(path).write_text(json.dumps(obj))
        return w.sha256_file(path)

    res = w.write_record({"new": 2}, out, bk, "20261017T090000Z", writer=writer)
    assert seen["backups"] == ["QC_REPORT.pre_write_20261017T090000Z.json"] and seen["old_still"] == '{"old": 1}'
    assert json.loads(out.read_text()) == {"new": 2}
    assert Path(res["backup"]["path"]).read_text() == '{"old": 1}' and res["backup"]["sha256"] == w.sha256_file(res["backup"]["path"])
    # a second write the same second does not overwrite the first backup
    res2 = w.write_record({"new": 3}, out, bk, "20261017T090000Z", writer=writer)
    assert res2["backup"]["path"] != res["backup"]["path"]
    assert Path(res["backup"]["path"]).read_text() == '{"old": 1}' and json.loads(Path(res2["backup"]["path"]).read_text()) == {"new": 2}


def test_failed_backup_stops_the_write(tmp_path):
    out = tmp_path / "QC_REPORT.json"
    out.write_text('{"old": 1}')
    blocker = tmp_path / "bk"
    blocker.write_text("a file, not a folder")              # backup folder cannot be made
    called = []
    with pytest.raises(Exception):
        w.write_record({"new": 2}, out, blocker, "T", writer=lambda p, o: called.append(1))
    assert called == [] and out.read_text() == '{"old": 1}'


def test_first_write_has_no_backup_and_writes_only_the_record(tmp_path):
    out, bk = tmp_path / "qc" / "QC_REPORT.json", tmp_path / "bk"

    def writer(path, obj):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(obj))
        return "sha"

    res = w.write_record({"a": 1}, out, bk, "T", writer=writer)
    assert res["backup"] is None and not bk.exists() and sorted(p.name for p in tmp_path.rglob("*") if p.is_file()) == ["QC_REPORT.json"]


def test_gates_pending_names_g13_ohsac_sealed_and_crowd_selection():
    text = " | ".join(w.GATES_PENDING)
    assert "G13" in text and "OHS-AC" in text and "sealed_check" in text and "crowd selection" in text and "c2_select.py carry" in text
    assert len(w.GATES_PENDING) == 3


def test_bars_are_the_preregistered_values():
    assert w.G6_BAR == 0.52 and w.G15_TOKEN_CAP == 1900 and w.G5_MAX_AMBIGUOUS == 3 and w.G10_B_TARGET_ROWS == 3600
    assert (w.G11_MAX_SAMPLER_ROWS, w.G11_MIN_PACKS, w.G11_MIN_TRAIN_SAMPLERS, w.G11_TWO_PCT) == (2500, 30, 4, 0.02)
    assert w.G10_Q_RANGE["yes_is_bad_share"] == (0.45, 0.55) and w.G10_Q_RANGE["attack_rows_share"] == (0.04, 0.06)
    assert w.G10_A_CELLS["cue_family"] == (0.03, 200) and w.G10_A_CELLS["sampler"] == (0.02, 1) and w.G10_OVERALL_TOL == 0.02


def test_writer_has_no_other_write_paths():
    src = Path(w.__file__).read_text()
    assert "write_text(" not in src and "write_bytes(" not in src
    assert not re.search(r"open\([^)]*['\"]w", src)
    assert src.count("writer or c2io.write_json") == 1 and src.count("shutil.copy2") == 1


@pytest.mark.skipif(not (w.R1_QC.exists() and w.F5.exists()), reason="round-1 F5 data not on this machine")
def test_dry_run_writes_nothing_and_passes(capsys):
    before = (w.OUTQ.exists(), w.OUTQ.stat().st_mtime_ns if w.OUTQ.exists() else None, sorted(p.name for p in w.BACKUP_DIR.glob("*")))
    rc = w.main([])
    after = (w.OUTQ.exists(), w.OUTQ.stat().st_mtime_ns if w.OUTQ.exists() else None, sorted(p.name for p in w.BACKUP_DIR.glob("*")))
    assert before == after
    out = capsys.readouterr().out
    assert "dry run: nothing written" in out and rc in (0, 1)
