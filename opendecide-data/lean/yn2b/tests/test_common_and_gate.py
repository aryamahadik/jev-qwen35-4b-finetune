"""yn2b_common (write guards, manifest, kd counts) and teacher_gate_2b (Option B / arm C)."""
from __future__ import annotations

import json

import pytest

import teacher_gate_2b as tg
import yn2b_common as yc
from conftest import ch_row, write_jsonl, yn_row


# ---------------------------------------------------------------------------------------------- yn2b_common
def test_guard_out_refuses_frozen_inputs_and_existing(tmp_path):
    with pytest.raises(SystemExit):
        yc.guard_out(yc.LEAN / "data/v14_parts/train_2b_golden_kd.jsonl")
    with pytest.raises(SystemExit):
        yc.guard_out(yc.LEAN / "runs/q35_2b_main.json")
    with pytest.raises(SystemExit):
        yc.guard_out(yc.LEAN / "train_decoder.py")
    f = tmp_path / "in.jsonl"
    f.write_text("{}\n")
    with pytest.raises(SystemExit):
        yc.guard_out(f, inputs=(f,), overwrite=True)  # an input is never an output, even with overwrite
    with pytest.raises(SystemExit):
        yc.guard_out(f)  # exists
    assert yc.guard_out(f, overwrite=True) == f.resolve()
    assert yc.guard_out(tmp_path / "new.jsonl") == (tmp_path / "new.jsonl").resolve()


def test_manifest_append_is_append_only(tmp_path, _tmp_manifest):
    p = write_jsonl(tmp_path / "a.jsonl", [{"x": 1}, {"x": 2}])
    yc.manifest_outputs("t", [p])
    yc.manifest_outputs("t", [p])
    lines = [json.loads(l) for l in _tmp_manifest.read_text().splitlines()]
    assert len(lines) == 2 and lines[0]["rows"] == 2 and lines[0]["sha256"] == yc.sha256_file(p)


def test_counts_kd_matches_trainer_rules():
    rows = [yn_row(1, teacher=0.9), yn_row(2, teacher=0.2, teacher_src="blend50"),
            yn_row(3, source="gd_gen2_probability", teacher=0.3, teacher_src="exact"), yn_row(4),
            ch_row(5, teacher={"A": 0.5, "B": 0.3, "C": 0.2})]
    assert yc.counts_kd(rows) == (3, 1)  # blend50 stripped; kd_full = the gd_gen2_probability yes/no row


# ---------------------------------------------------------------------------------------------- teacher gate
def _rows():
    return [
        yn_row(1, gold=1, teacher=0.3),                                  # wrong side -> gated
        yn_row(2, gold=1, teacher=0.7),                                  # right -> kept
        yn_row(3, gold=0, teacher=0.5),                                  # p = 0.5 with gold no -> wrong -> gated
        yn_row(4, gold=1, teacher=0.1, source="gd_ohs_like_human"),      # out of scope -> kept
        yn_row(5, gold=1, teacher=0.1, source="gd_gen2_probability", teacher_src="exact"),  # kd_full exact: kept
        ch_row(6, gold="A", teacher={"A": 0.4, "B": 0.4, "C": 0.2}),     # tie on top -> wrong -> gated
        ch_row(7, gold="A", teacher={"A": 0.6, "B": 0.3, "C": 0.1}),     # right -> kept
        ch_row(8, gold="A", teacher={"A": 0.1, "B": 0.8, "C": 0.1}, source="gd_gen2_probability"),  # choice in scope
        yn_row(9, gold=1, teacher=0.2, teacher_src="q35_4b_E_clean_copy"),  # copies are not gated by the rule
        yn_row(10, gold=1, teacher=0.2, source="gd_gen2_long_policy"),   # extra gen2 source in scope -> gated
    ]


def test_gate_rows_rule_and_scope():
    rows = _rows()
    before = json.dumps(rows, sort_keys=True)
    out, s = tg.gate_rows(rows, [])
    assert json.dumps(rows, sort_keys=True) == before, "the input rows must not be modified"
    gated = {r["id"] for r in out if r["meta"].get("teacher_gate") == tg.GATED_TAG}
    assert gated == {"r1", "r3", "r6", "r8", "r10"}
    for r in out:
        if r["id"] in gated:
            assert "teacher" not in r["meta"] and "teacher_src" not in r["meta"] and "teacher4b" in r["meta"]
    assert s["kd_targets"] == s["kd_targets_before"] - 5
    assert s["kd_full"] == s["kd_full_before"] == 1
    assert [r["id"] for r in out] == [r["id"] for r in rows]


def test_gate_keeps_complement_and_inv_consistent():
    a = yn_row(1, gold=1, teacher=0.5)   # p = 0.5, gold yes -> gives gold (kept by the rule)
    b = yn_row(2, gold=0, teacher=0.5)   # p = 0.5, gold no -> wrong (gated) -> a must be gated too
    c = yn_row(3, gold=1, teacher=0.2)   # gated
    d = yn_row(4, gold=1, teacher=0.9, teacher_src="q35_4b_E_clean_copy", role="attacked")
    rels = [{"type": "complement", "a": "r1", "b": "r2"}, {"type": "inv", "a": "r3", "b": "r4"}]
    out, s = tg.gate_rows([a, b, c, d], rels)
    assert {r["id"] for r in out if r["meta"].get("teacher_gate")} == {"r1", "r2", "r3", "r4"}
    assert s["forced"] == {"complement_partner_gated": 1, "inv_clean_copy_gated": 1}


def test_gate_file_streaming_equals_in_memory_and_never_touches_input(tmp_path):
    rows = _rows()
    inp = write_jsonl(tmp_path / "in.jsonl", rows)
    rel = write_jsonl(tmp_path / "rel.jsonl", [])
    sha = yc.sha256_file(inp)
    s = tg.gate_file(inp, rel, tmp_path / "out.jsonl")
    assert yc.sha256_file(inp) == sha
    mem, s2 = tg.gate_rows(rows, [])
    got = [json.loads(l) for l in open(tmp_path / "out.jsonl")]
    assert got == mem
    assert s["kd_targets"] == s2["kd_targets"] and s["gated"] == s2["gated"]
    # unchanged rows are byte-identical lines
    src_lines, out_lines = open(inp).read().splitlines(), open(tmp_path / "out.jsonl").read().splitlines()
    for r, a, b in zip(rows, src_lines, out_lines):
        if r["id"] not in {"r1", "r3", "r6", "r8", "r10"}:
            assert a == b


def test_gate_cli_refuses_to_overwrite_input(tmp_path):
    inp = write_jsonl(tmp_path / "in.jsonl", _rows())
    with pytest.raises(SystemExit):
        tg.main(["--data-dir", str(tmp_path), "--in", "in.jsonl", "--rel", "", "--out", "in.jsonl", "--overwrite"])
    s = tg.main(["--data-dir", str(tmp_path), "--in", "in.jsonl", "--rel", "", "--out", "c.jsonl"])
    assert s["gated"] == 5 and (tmp_path / "c.jsonl").exists()


def test_abstain_zone_numbers():
    r_wrong = yn_row(1, gold=1, teacher=0.3)      # 0.5*0.95 + 0.5*0.3 = 0.625 -> inside (0.2, 0.8); gated -> 0.95
    r_right = yn_row(2, gold=1, teacher=0.9)      # 0.925 -> outside
    _, s = tg.gate_rows([r_wrong, r_right], [])
    assert s["yes_no_targets_in_0.2_0.8_before"] == 0.5 and s["yes_no_targets_in_0.2_0.8_after"] == 0.0


def test_exclude_ids_are_never_gated(tmp_path):
    rows = _rows()
    out, s = tg.gate_rows(rows, [], exclude={"r1", "r6"})
    gated = {r["id"] for r in out if r["meta"].get("teacher_gate")}
    assert gated == {"r3", "r8", "r10"} and s["excluded_known_bad"] == 2
    f = tmp_path / "bad.json"
    f.write_text(json.dumps({"all_ids": ["r1"]}))
    assert tg.load_exclude(f) == {"r1"}
    assert tg.load_exclude("") == frozenset()
