"""A25 (a)/(b) in the B5 record: look commands convert with preds_to_gate.py and pass --ref-name C1; sealed CIs are the
frozen scorer's 2,000 / seed 7, dev CIs 10,000 / seed 0; the sealed confirm is tied to the converter's sha256. CPU only;
never runs the sealed scorer, never reads sealed data."""
import copy
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import score_nd_cli as s  # noqa: E402


def test_look_commands_convert_and_pass_c1():
    cm = s.commands()
    looks = [k for k, v in cm.items() if " look --kind " in v]
    assert set(looks) >= {"S1", "S2", "C"}
    for k in looks:
        v = cm[k]
        assert v.startswith("set -o pipefail; ") and str(s.CONVERTER) in v and v.count(str(s.CONVERTER)) == 2
        assert "--ref-name C1 " in v and "q35_4b_main500k_pre.gate.jsonl" in v and v.count(".gate.jsonl") == 2
        assert v.index(str(s.CONVERTER)) < v.index("score_nd.py look")      # converted BEFORE the scorer reads


def test_bootstrap_constants_from_a25b():
    assert s.prereg_boot() == (2000, 7)
    assert s.dev_boot() == (10000, 0)
    rec = s.a25_fields({})
    assert rec["bootstrap_sealed"]["resamples"] == 2000 and rec["bootstrap_dev"]["resamples"] == 10000
    assert "2,000" in rec["bootstrap_note"] and "10,000" in rec["bootstrap_note"]


def _good():
    c = json.loads((HERE / "SCORE_ND_CLI.json").read_text())["sealed_confirm"]
    return copy.deepcopy(c)


@pytest.mark.parametrize("edit,match", [
    (lambda c: c.update(converter_sha256="0" * 64), "another preds_to_gate.py"),
    (lambda c: c.update(tie_fixed_order_ok=False), "fixed order"),
    (lambda c: c["bootstrap"].update(resamples=10000, seed=0), "bootstrap"),
    (lambda c: c.pop("refused_look_logged"), "missing"),
    (lambda c: c.update(converted_format_ok=False), "converted prediction format"),
    (lambda c: c.update(refused_look_logged="unknown"), "true or false")])
def test_confirm_problem_refuses(edit, match):
    c = _good()
    want = s.a15()["scorer_sha256"]
    assert s.confirm_problem(c, want) is None
    edit(c)
    e = s.confirm_problem(c, want)
    assert e and match in e, e


def test_record_on_disk_verifies():
    assert s.verify() is None


def test_verify_refuses_a_look_without_ref_name_c1(tmp_path):
    rec = json.loads((HERE / "SCORE_ND_CLI.json").read_text())
    rec["commands"]["S1"] = rec["commands"]["S1"].replace("--ref-name C1 ", "--ref-name q35_4b_main500k_pre ")
    p = tmp_path / "cli.json"
    p.write_text(json.dumps(rec))
    assert "--ref-name C1" in s.verify(p)


def test_verify_refuses_without_dev_proof(tmp_path, monkeypatch):
    import preds_to_gate
    monkeypatch.setattr(preds_to_gate, "PROOF", tmp_path / "none.json")
    monkeypatch.setattr(preds_to_gate.proof_problem, "__defaults__", (tmp_path / "none.json",))
    e = s.verify()
    assert e and "A25 (a)" in e and "prove" in e
