"""mix_c2 refuses incomplete C2 G13 logs (16 Oct 2026 guard review). Synthetic logs only, written under tmp_path; the
build() cases reuse test_mix_c2.py's `flow` fixture (every disk boundary faked). Run from lean/:
  ../.venv/bin/python -m pytest -q c2_build/tests/test_mix_c2_g13_logs.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import c2io  # noqa: E402
import mix_c2 as m  # noqa: E402
from test_mix_c2 import flow  # noqa: E402,F401  (fixture)


def log(tmp_path, name, **kw) -> Path:
    d = {"set": name.removesuffix(".json"), "run": "candidates", "tool": m.G13_TOOL, "drop_ids": ["r1", "r2"],
         "complete": True, "incomplete_why": [], "inputs_at_start": {"candidates_c2.jsonl": "a" * 64}} | kw
    d = {k: v for k, v in d.items() if v is not None}
    p = tmp_path / name
    p.write_text(json.dumps(d))
    return p


def probs(tmp_path, *files):
    return m.g13_log_problems(c2io.C2InputLog(), [str(f) for f in files])


def test_a_complete_guarded_log_is_fine(tmp_path):
    assert probs(tmp_path, log(tmp_path, "c2_cand_T28.json")) == []
    assert probs(tmp_path, log(tmp_path, "c2_final.json", run="final")) == []


def test_an_incomplete_log_is_refused(tmp_path):
    p = probs(tmp_path, log(tmp_path, "c2_cand_T28.json", complete=False, incomplete_why=["method 5 off"]))
    assert len(p) == 1 and "incomplete G13 log" in p[0] and "1 reasons" in p[0]
    # complete true with reasons listed, complete missing, reasons missing: all incomplete
    assert any("incomplete" in x for x in probs(tmp_path, log(tmp_path, "c2_cand_T01.json", incomplete_why=["x changed"])))
    assert any("incomplete" in x for x in probs(tmp_path, log(tmp_path, "c2_cand_T06.json", complete=None)))
    assert any("incomplete" in x for x in probs(tmp_path, log(tmp_path, "c2_cand_T07.json", incomplete_why=None)))
    assert any("incomplete" in x for x in probs(tmp_path, log(tmp_path, "c2_cand_T12.json", complete="yes")))


def test_a_log_with_a_changed_input_note_is_incomplete(tmp_path):
    why = ["c2_mixdev.jsonl changed during the run: re-run (sha256 aaaaaaaaaaaa at the start, bbbbbbbbbbbb now)"]
    p = probs(tmp_path, log(tmp_path, "c2_cand_T28.json", complete=False, incomplete_why=why))
    assert len(p) == 1 and "incomplete" in p[0]


def test_a_pre_guard_log_is_refused_but_a_seed_log_is_not(tmp_path):
    for run, name in (("candidates", "c2_cand_T28.json"), ("carry", "c2_carry_F5.json"), ("final", "c2_final.json")):
        p = probs(tmp_path, log(tmp_path, name, run=run, inputs_at_start=None))
        assert len(p) == 1 and "pre-guard G13 log" in p[0] and "re-run" in p[0], (run, p)
    assert any("pre-guard" in x for x in probs(tmp_path, log(tmp_path, "c2_cand_T01.json", inputs_at_start={})))
    assert any("pre-guard" in x for x in probs(tmp_path, log(tmp_path, "c2_cand_T06.json", run=None, inputs_at_start=None)))
    assert probs(tmp_path, log(tmp_path, "c2_seed_T28.json", run="seed", inputs_at_start=None)) == []


def test_only_c2_g13_logs_are_checked(tmp_path, monkeypatch):
    other = tmp_path / "some_list.json"
    other.write_text(json.dumps({"drop_ids": ["r9"]}))                       # not a C2 G13 log: read as before
    assert probs(tmp_path, other) == []
    r1 = tmp_path / "pool_drops_r1.json"
    r1.write_text(json.dumps({"set": "pool_drops_r1", "drop_ids": ["r9"], "complete": False}))
    monkeypatch.setattr(m, "POOL_DROPS_R1", r1)                                # the round-1 list is never checked
    assert probs(tmp_path, r1) == []
    odd = log(tmp_path, "my_list.json", complete=False, incomplete_why=["x"])   # identified by its tool, not its name
    assert len(probs(tmp_path, odd)) == 1
    named = tmp_path / "c2_hand_made.json"                                     # named like a C2 log, written by hand
    named.write_text(json.dumps({"drop_ids": ["r9"]}))
    assert any("not a g13_c2.py record" in x for x in probs(tmp_path, named))


def test_g13_drop_ids_final_stops_and_a_dry_run_lists_the_problem(tmp_path):
    bad = log(tmp_path, "c2_cand_T28.json", complete=False, incomplete_why=["x"], drop_ids=["r1", "r2"])
    ilog = c2io.C2InputLog()
    final = type("A", (), {"final": True})()
    with pytest.raises(SystemExit, match="G13 drop lists must be complete") as e:
        m.g13_drop_ids(final, ilog, [str(bad)], [])
    assert "c2_cand_T28" in str(e.value) and "no training file written" in str(e.value)
    dry, pr = type("A", (), {"final": False})(), []
    ids, used = m.g13_drop_ids(dry, ilog, [str(bad)], pr)
    assert ids == {"r1", "r2"} and used[0]["ids"] == 2                          # more drops, never fewer
    assert len(pr) == 1 and "incomplete G13 log" in pr[0]
    ok, pr = log(tmp_path, "c2_cand_T01.json"), []
    assert m.g13_drop_ids(final, ilog, [str(ok)], pr)[0] == {"r1", "r2"} and pr == []


def test_build_dry_run_lists_the_problem_and_still_drops_the_ids(flow, tmp_path):
    args, writes, inp = flow
    bad = log(tmp_path, "c2_cand_T28.json", complete=False, incomplete_why=["method 5 off"], drop_ids=[inp["drop_one"]])
    rep = m.build(args(decontam_drops=[str(bad)]))
    assert any("incomplete G13 log" in p and "c2_cand_T28" in p for p in rep["problems"]), rep["problems"]
    assert rep["g13_rows_dropped"] >= 1 and list(writes) == [str(m.WORK / "dryrun_c2.json")]
    ok = log(tmp_path, "c2_cand_T01.json", drop_ids=[inp["drop_one"]])
    rep = m.build(args(decontam_drops=[str(ok)]))
    assert not any("G13 log" in p for p in rep["problems"])


def test_build_final_stops_before_reading_a_block(flow, monkeypatch, tmp_path):
    args, writes, inp = flow
    monkeypatch.setattr(m, "ohs4_problem", lambda sha, text, pinned=None: None)
    man, gp = tmp_path / "never_train.json", tmp_path / "gproxy.jsonl"
    man.write_text('{"anchors": [{"name": "bfcl", "sha256": "' + "a" * 64 + '"}]}')
    gp.write_text('{"id": "g1"}\n')
    bad = log(tmp_path, "c2_cand_T28.json", complete=False, incomplete_why=["method 5 off"])
    old = log(tmp_path, "c2_cand_T01.json", inputs_at_start=None)
    for f in (bad, old):
        with pytest.raises(SystemExit, match="G13 drop lists must be complete"):
            m.build(args(final=True, ohs4_sha="e" * 64, decontam_drops=[str(f)], never_train_manifest=man, gproxy_file=gp))
    assert writes == {}                                                         # nothing read, nothing written
    monkeypatch.setattr(m, "minimum_to_train", lambda entered: (True, {"ok": True}))
    ok = log(tmp_path, "c2_cand_T06.json")
    with pytest.raises(SystemExit) as e:                                        # a good log gets past the G13 check
        m.build(args(final=True, ohs4_sha="e" * 64, decontam_drops=[str(ok)], never_train_manifest=man, gproxy_file=gp))
    assert "G13 drop lists must be complete" not in str(e.value)
    assert str(m.OUT_TRAIN) not in writes
