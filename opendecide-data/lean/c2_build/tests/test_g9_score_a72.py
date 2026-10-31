"""A72 step 1 (A43 d): g9_score asks Opus to confirm the Sonnet "ambiguous" verdicts too (stage confirm_amb) and `final` counts as ambiguous only what Opus
confirms, over all rows read and over the seeded-sample rows. In a temp folder; no model is called. Run from lean/:
  ../.venv/bin/python -B -m pytest -q c2_build/tests/test_g9_score_a72.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(C2B / "zed_orch" / "g9_reread"))
import g9_score as g  # noqa: E402

FAM = "ZZ"
MARK = "## Items (JSON; answer every item exactly once, keyed by its qid)\n\n"


@pytest.fixture
def fam(monkeypatch):
    import shutil
    import uuid
    tmp_path = Path(__file__).resolve().parent / f"_scratch_g9_a72_{uuid.uuid4().hex[:8]}"      # the C2 writers only write under lean/
    tmp_path.mkdir()
    monkeypatch.setattr(g, "OUT", tmp_path)
    yield from _build(tmp_path)
    shutil.rmtree(tmp_path, ignore_errors=True)


def _build(tmp_path):
    d = tmp_path / "fam" / FAM
    (d / "adjudication" / "tasks").mkdir(parents=True)
    (d / "confirm").mkdir()
    (tmp_path / "key").mkdir()
    items = [{"aid": f"a{i}", "qid": f"q{i}", "text": f"t{i}"} for i in range(5)]
    tf = d / "adjudication" / "tasks" / f"{FAM}-ADJ-000.md"
    tf.write_text("header\n" + MARK + json.dumps(items))
    (d / "adjudication" / "manifest.json").write_text(json.dumps({"tasks": [{"task_file": str(tf), "task_id": f"{FAM}-ADJ-000"}]}))
    akey = {f"a{i}": f"row{i}" for i in range(5)}
    (d / "adjudication" / "key.json").write_text(json.dumps({"key": akey}))
    verdicts = {"a0": "ambiguous", "a1": "ambiguous", "a2": "ambiguous", "a3": "gold_ok", "a4": "gold_ok"}
    (d / "adjudication" / "first_pass.json").write_text(json.dumps({"verdicts": {a: {"verdict": v, "reason": "r"} for a, v in verdicts.items()},
                                                                      "problems": [], "unanswered": []}))
    (d / "score.json").write_text(json.dumps({"n_read": 200, "n_sample_rows": 100, "queue": [], "quarantined": [], "quarantined_n_ge_20": [], "control": []}))
    (d / "sonnet_flags.json").write_text(json.dumps({"wrong_gold_rows": [], "ambiguous_rows": ["row0", "row1", "row2"]}))
    (d / "confirm" / "manifest.json").write_text(json.dumps({"family": FAM, "stage": "confirm", "tasks": []}))
    (d / "confirm" / "key.json").write_text(json.dumps({"key": {}}))
    (tmp_path / "key" / f"{FAM}.json").write_text(json.dumps({"sample_ids": ["row0", "row3", "rowX"], "row_ids": []}))
    yield d


def test_confirm_amb_writes_a_separate_stage_and_leaves_stage_confirm_alone(fam, capsys):
    before = (fam / "confirm" / "manifest.json").read_bytes()
    g.cmd_confirm_amb([FAM], set())
    man = json.loads((fam / "confirm_amb" / "manifest.json").read_text())
    assert len(man["tasks"]) == 1 and man["tasks"][0]["task_id"] == f"{FAM}-CAMB-000" and man["tasks"][0]["aids"] == ["a0", "a1", "a2"]
    assert json.loads((fam / "confirm_amb" / "key.json").read_text())["key"] == {"a0": "row0", "a1": "row1", "a2": "row2"}
    assert (fam / "confirm" / "manifest.json").read_bytes() == before                        # the wrong_gold stage (and its answers) are untouched
    txt = Path(man["tasks"][0]["task_file"]).read_text()
    assert "ambiguous flags" in txt and "first_flag" in txt and "t3" not in txt              # only the ambiguous items go to Opus


def test_final_waits_for_opus_and_never_falls_back_to_the_sonnet_count(fam, capsys):
    g.cmd_final([FAM], set())
    out = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert out["confirm_amb_missing"] and not (fam / "G9_RESULT.json").exists()
    g.cmd_confirm_amb([FAM], set())
    capsys.readouterr()
    g.cmd_final([FAM], set())
    out = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert out["confirm_amb_incomplete"] and out["unanswered"] == 3 and not (fam / "G9_RESULT.json").exists()


def test_final_counts_only_opus_confirmed_ambiguous_over_all_rows_read_and_over_the_sample(fam, capsys):
    g.cmd_confirm_amb([FAM], set())
    man = json.loads((fam / "confirm_amb" / "manifest.json").read_text())
    ans = Path(man["tasks"][0]["answer_file"])
    ans.write_text(json.dumps([{"aid": "a0", "verdict": "ambiguous", "reason": "x"}, {"aid": "a1", "verdict": "gold_ok", "reason": "x"},
                               {"aid": "a2", "verdict": "ambiguous", "reason": "x"}]))
    capsys.readouterr()
    g.cmd_final([FAM], set())
    res = json.loads((fam / "G9_RESULT.json").read_text())
    assert res["sonnet_ambiguous_first_pass"] == 3 and res["ambiguous_rows"] == 2 and res["confirmed_ambiguous_ids"] == ["row0", "row2"]
    assert res["ambiguous_rate_of_read"] == 2 / 200 and res["ambiguous_rows_in_sample"] == 1 and res["ambiguous_rate_of_sample"] == 1 / 100
    assert res["opus_confirm_amb"] == {"gold_ok": 1, "wrong_gold": 0, "ambiguous": 2} and not res["generator_bug"]


def test_a_family_with_no_sonnet_ambiguous_flag_needs_no_second_stage(fam, capsys):
    (fam / "sonnet_flags.json").write_text(json.dumps({"wrong_gold_rows": [], "ambiguous_rows": []}))
    g.cmd_final([FAM], set())
    res = json.loads((fam / "G9_RESULT.json").read_text())
    assert res["ambiguous_rows"] == 0 and res["ambiguous_rate_of_read"] == 0 and res["ambiguous_rate_of_sample"] == 0


def test_a_wrong_gold_found_in_the_ambiguous_stage_is_reported_and_marks_the_generator_bug_field_unchanged(fam, capsys):
    g.cmd_confirm_amb([FAM], set())
    man = json.loads((fam / "confirm_amb" / "manifest.json").read_text())
    Path(man["tasks"][0]["answer_file"]).write_text(json.dumps([{"aid": a, "verdict": "wrong_gold" if a == "a1" else "gold_ok", "reason": "x"}
                                                                for a in ("a0", "a1", "a2")]))
    g.cmd_final([FAM], set())
    res = json.loads((fam / "G9_RESULT.json").read_text())
    assert res["confirmed_wrong_gold_from_amb_stage"] == ["row1"] and res["ambiguous_rows"] == 0
