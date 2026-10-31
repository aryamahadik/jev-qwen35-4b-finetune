"""mix_c2 refuses incomplete, unguarded or stale C2 G13 logs (16 Oct 2026 guard reviews 1-3). Synthetic logs only, written
under tmp_path; the build() cases reuse test_mix_c2.py's `flow` fixture (every disk boundary faked). The log builder and the
isolated layout (`g13w`, `g13_log`) are test_c2_select.py's: the mixer and `c2_select --exclude-ids` run ONE function
(c2_select.g13_log_problems). Run from lean/:
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
import c2_select as sel  # noqa: E402
import mix_c2 as m  # noqa: E402
from test_c2_select import PLAIN_LISTS, _refused_folder, g13_log as log, g13w, leak, stale_msg  # noqa: E402,F401  (fixtures)
from test_mix_c2 import flow  # noqa: E402,F401  (fixture)


def probs(*files):
    return m.g13_log_problems(c2io.C2InputLog(), [str(f) for f in files])


def test_a_complete_guarded_log_is_fine(g13w):
    assert probs(log(g13w, "c2_cand_T28.json")) == []
    assert probs(log(g13w, "c2_final.json", run="final")) == []
    assert probs(log(g13w, "c2_carry_F5.json", run="carry")) == []


def test_an_incomplete_log_is_refused(g13w):
    p = probs(log(g13w, "c2_cand_T28.json", complete=False, incomplete_why=["method 5 off"]))
    assert len(p) == 1 and "incomplete G13 log" in p[0] and "1 reasons" in p[0]
    # complete true with reasons listed, complete missing, reasons missing: all incomplete
    assert any("incomplete" in x for x in probs(log(g13w, "c2_cand_T01.json", incomplete_why=["x changed"])))
    assert any("incomplete" in x for x in probs(log(g13w, "c2_cand_T06.json", complete=None)))
    assert any("incomplete" in x for x in probs(log(g13w, "c2_cand_T07.json", incomplete_why=None)))
    assert any("incomplete" in x for x in probs(log(g13w, "c2_cand_T12.json", complete="yes")))


def test_a_log_with_a_changed_input_note_is_incomplete(g13w):
    why = ["c2_mixdev.jsonl changed during the run: re-run (sha256 aaaaaaaaaaaa at the start, bbbbbbbbbbbb now)"]
    p = probs(log(g13w, "c2_cand_T28.json", complete=False, incomplete_why=why))
    assert len(p) == 1 and "incomplete" in p[0]


def test_a_pre_guard_log_is_refused_but_a_seed_log_is_not(g13w):
    for run, name in (("candidates", "c2_cand_T28.json"), ("carry", "c2_carry_F5.json"), ("final", "c2_final.json")):
        p = probs(log(g13w, name, run=run, inputs_at_start=None))
        assert len(p) == 1 and "pre-guard G13 log" in p[0] and "re-run" in p[0], (run, p)
    assert any("pre-guard" in x for x in probs(log(g13w, "c2_cand_T01.json", inputs_at_start={})))
    no_run = log(g13w, "c2_cand_T06.json", inputs_at_start=None)               # no "run" key: read from the set-name prefix
    d = json.loads(no_run.read_text())
    d.pop("run")
    no_run.write_text(json.dumps(d))
    assert any("pre-guard" in x for x in probs(no_run))
    assert probs(log(g13w, "c2_seed_T28.json", run="seed", inputs_at_start=None)) == []


def test_only_c2_g13_logs_are_checked(g13w, monkeypatch):
    other = g13w.tmp / "some_list.json"
    other.write_text(json.dumps({"drop_ids": ["r9"]}))                       # not a C2 G13 log: read as before
    assert probs(other) == []
    r1 = g13w.tmp / "pool_drops_r1.json"
    r1.write_text(json.dumps({"set": "pool_drops_r1", "drop_ids": ["r9"], "complete": False}))
    monkeypatch.setattr(m, "POOL_DROPS_R1", r1)                                # the round-1 list is never checked
    assert probs(r1) == []
    odd = log(g13w, "my_list.json", complete=False, incomplete_why=["x"])       # identified by its tool, not its name
    assert len(probs(odd)) == 1
    named = g13w.tmp / "c2_hand_made.json"                                     # named like a C2 log, written by hand
    named.write_text(json.dumps({"drop_ids": ["r9"]}))
    assert any("not a g13_c2.py record" in x for x in probs(named))


def test_the_mixer_calls_the_shared_check(g13w, monkeypatch):
    """mix_c2.g13_log_problems is c2_select.g13_log_problems with the mixer's tool name and the round-1 list exempt."""
    f = log(g13w, "c2_cand_T28.json")
    seen = {}

    def stub(ilog, files, **kw):
        seen.update(files=list(files), **kw)
        return ["c2_cand_T28: stub problem"]

    monkeypatch.setattr(sel, "g13_log_problems", stub)
    assert probs(f) == ["c2_cand_T28: stub problem"]
    assert seen["tool"] == m.G13_TOOL == "c2_build/g13_c2.py" and list(seen["exempt"]) == [m.POOL_DROPS_R1]


CASES = {
    "fine": {}, "incomplete": {"complete": False, "incomplete_why": ["x"]}, "no_reasons": {"incomplete_why": None},
    "complete_str": {"complete": "yes"}, "pre_guard": {"inputs_at_start": None}, "empty_ias": {"inputs_at_start": {}},
    "wrong_tool": {"tool": "c2_build/other.py"}, "stale": "stale_train", "stale_dev": "stale_dev",
    "tool_removed": {"tool": None}, "names_only_gone": "names_only_gone",
}


@pytest.mark.parametrize("case", sorted(CASES))
def test_the_mixer_and_exclude_ids_refuse_exactly_the_same_logs(g13w, case):
    """One check: whatever the mixer lists as a problem, --exclude-ids refuses, and the same text; whatever it passes, a
    --exclude-ids run reads."""
    kw = CASES[case]
    f = log(g13w, "c2_cand_T28.json", **(kw if isinstance(kw, dict) else {}))
    if kw == "stale_train":
        c2io.fam_files("T28")["cand"].write_text("changed\n")
    elif kw == "stale_dev":
        (g13w.dev / "c2_transfer_dev.jsonl").write_text("changed\n")
    elif kw == "names_only_gone":                                                       # an older record: names, no paths
        f = log(g13w, "c2_cand_T28.json", inputs_at_start_paths=None)
        (g13w.dev / "c2_transfer_dev.jsonl").unlink()
    mixer = probs(f)
    shared = sel.g13_log_problems(c2io.C2InputLog(), [str(f)], tool=m.G13_TOOL, exempt=[m.POOL_DROPS_R1])
    assert mixer == shared
    if mixer:
        with pytest.raises(SystemExit) as e:
            sel.drop_ids_of(c2io.C2InputLog(), [str(f)])
        assert all(x in str(e.value) for x in mixer)
    else:
        assert sel.drop_ids_of(c2io.C2InputLog(), [str(f)]) == {"r1", "r2"}


def test_a_log_made_before_the_candidates_or_a_dev_file_changed_is_stale_for_the_mixer(g13w):
    f = log(g13w, "c2_cand_T28.json")
    assert probs(f) == []
    c2io.fam_files("T28")["cand"].write_text("rebuilt\n")                              # the candidates were rebuilt
    assert probs(f) == [stale_msg("c2_cand_T28", "candidates_c2.jsonl", "T28")]
    f = log(g13w, "c2_cand_T28.json")
    mixdev = g13w.dev / "T28" / "mixdev_S5.jsonl"                                       # a new dev file (glob target)
    mixdev.parent.mkdir()
    mixdev.write_text("{}\n")
    assert probs(f) == [stale_msg("c2_cand_T28", "mixdev_S5.jsonl", "T28")]
    f = log(g13w, "c2_cand_T28.json")
    (g13w.dev / "c2_mixdev.jsonl").write_text("rebuilt\n")                              # a dev file changed
    assert probs(f) == [stale_msg("c2_cand_T28", "c2_mixdev.jsonl", "T28")]
    final = log(g13w, "c2_final.json", run="final")
    (c2io.C2_PARTS / "c2_train.jsonl").write_text("remixed\n")
    assert stale_msg("c2_final", "c2_train.jsonl", "final") in probs(final)


def test_g13_drop_ids_final_stops_and_a_dry_run_lists_the_problem(g13w):
    bad = log(g13w, "c2_cand_T28.json", complete=False, incomplete_why=["x"], drop_ids=["r1", "r2"])
    ilog = c2io.C2InputLog()
    final = type("A", (), {"final": True})()
    with pytest.raises(SystemExit, match="G13 drop lists must be complete") as e:
        m.g13_drop_ids(final, ilog, [str(bad)], [])
    assert "c2_cand_T28" in str(e.value) and "no training file written" in str(e.value)
    dry, pr = type("A", (), {"final": False})(), []
    ids, used = m.g13_drop_ids(dry, ilog, [str(bad)], pr)
    assert ids == {"r1", "r2"} and used[0]["ids"] == 2                          # more drops, never fewer
    assert len(pr) == 1 and "incomplete G13 log" in pr[0]
    ok, pr = log(g13w, "c2_cand_T01.json"), []
    assert m.g13_drop_ids(final, ilog, [str(ok)], pr)[0] == {"r1", "r2"} and pr == []
    c2io.fam_files("T01")["cand"].write_text("rebuilt after the G13 run\n")           # stale: --final stops, dry run lists
    with pytest.raises(SystemExit, match="stale G13 log") as e:
        m.g13_drop_ids(final, ilog, [str(ok)], [])
    assert "re-run G13 for T01" in str(e.value)
    ids, _ = m.g13_drop_ids(dry, ilog, [str(ok)], pr)
    assert ids == {"r1", "r2"} and pr == [stale_msg("c2_cand_T01", "candidates_c2.jsonl", "T01")]


def test_build_dry_run_lists_the_problem_and_still_drops_the_ids(flow, g13w):
    args, writes, inp = flow
    bad = log(g13w, "c2_cand_T28.json", complete=False, incomplete_why=["method 5 off"], drop_ids=[inp["drop_one"]])
    rep = m.build(args(decontam_drops=[str(bad)]))
    assert any("incomplete G13 log" in p and "c2_cand_T28" in p for p in rep["problems"]), rep["problems"]
    assert rep["g13_rows_dropped"] >= 1 and list(writes) == [str(m.WORK / "dryrun_c2.json")]
    ok = log(g13w, "c2_cand_T01.json", drop_ids=[inp["drop_one"]])
    rep = m.build(args(decontam_drops=[str(ok)]))
    assert not any("G13 log" in p for p in rep["problems"])
    c2io.fam_files("T01")["cand"].write_text("rebuilt after the G13 run\n")
    rep = m.build(args(decontam_drops=[str(ok)]))
    assert any("stale G13 log" in p and "re-run G13 for T01" in p for p in rep["problems"]), rep["problems"]


def test_build_final_stops_before_reading_a_block(flow, g13w, monkeypatch):
    args, writes, inp = flow
    tmp_path = g13w.tmp
    monkeypatch.setattr(m, "ohs4_problem", lambda sha, text, pinned=None: None)
    man, gp = tmp_path / "never_train.json", tmp_path / "gproxy.jsonl"
    man.write_text('{"anchors": [{"name": "bfcl", "sha256": "' + "a" * 64 + '"}]}')
    gp.write_text('{"id": "g1"}\n')
    bad = log(g13w, "c2_cand_T28.json", complete=False, incomplete_why=["method 5 off"])
    old = log(g13w, "c2_cand_T01.json", inputs_at_start=None)
    stale = log(g13w, "c2_cand_T12.json")
    c2io.fam_files("T12")["cand"].write_text("rebuilt after the G13 run\n")
    for f in (bad, old, stale):
        with pytest.raises(SystemExit, match="G13 drop lists must be complete"):
            m.build(args(final=True, ohs4_sha="e" * 64, decontam_drops=[str(f)], never_train_manifest=man, gproxy_file=gp, credit_usd=100.0))
    assert writes == {}                                                         # nothing read, nothing written
    monkeypatch.setattr(m, "minimum_to_train", lambda entered: (True, {"ok": True}))
    ok = log(g13w, "c2_cand_T06.json")
    with pytest.raises(SystemExit) as e:                                        # a good log gets past the G13 check
        m.build(args(final=True, ohs4_sha="e" * 64, decontam_drops=[str(ok)], never_train_manifest=man, gproxy_file=gp, credit_usd=100.0))
    assert "G13 drop lists must be complete" not in str(e.value)
    assert str(m.OUT_TRAIN) not in writes


def test_a_gone_dev_file_is_stale_for_the_mixer_also_in_a_names_only_record(g13w):
    f = log(g13w, "c2_cand_T28.json", inputs_at_start_paths=None)
    assert probs(f) == []
    (g13w.dev / "c2_mixdev.jsonl").unlink()
    assert probs(f) == ["c2_cand_T28: stale G13 log (c2_mixdev.jsonl changed after the run (gone)): re-run G13 for T28"]


def test_a_g13_record_with_its_tool_key_removed_is_still_checked_by_the_mixer(g13w):
    p = probs(log(g13w, "my_copy.json", block="T28", tool=None, complete=False, incomplete_why=["x"]))
    assert any("not a g13_c2.py record" in x for x in p) and any("incomplete G13 log" in x for x in p), p
    assert probs(log(g13w, "my_copy.json", block="T28")) == []


def test_the_mixer_reads_a_non_g13_list_as_before_while_exclude_ids_keeps_its_complete_gate(g13w):
    """mix_c2 never checked a list that is not a C2 G13 log (it reads its drop ids), and still does not. c2_select
    --exclude-ids always required complete = true of EVERY such file (the three plain lists, REPLAY_DENY_A46.json,
    REPLAY_UNSCREENED_A46.json and pool_drops_r1.json, included), and still does."""
    f6 = g13w.tmp / "F6.json"
    f6.write_text(json.dumps({"set": "F6", "tool": "c_build/decontam_g13.py", "drop_ids": ["r9"], "complete": False,
                              "incomplete_why": ["x"]}))
    assert probs(f6) == []
    with pytest.raises(SystemExit, match="G13 log is not complete"):
        sel.drop_ids_of(c2io.C2InputLog(), [str(f6)])
    for name, body in PLAIN_LISTS.items():                                     # the mixer reads these (--decontam-drops) ...
        f = g13w.tmp / name
        f.write_text(json.dumps(body))
        assert probs(f) == [], name
        with pytest.raises(SystemExit, match="G13 log is not complete"):          # ... --exclude-ids never did
            sel.drop_ids_of(c2io.C2InputLog(), [str(f)])


# ---- guard review 4 (16 Oct 2026) -------------------------------------------------------------------------------------------
def test_the_round1_list_is_exempt_by_its_resolved_path_not_by_a_name(g13w, monkeypatch):
    """The mixer exempts logs/decontam_counts/pool_drops_r1.json (spec 5.4). A stale or incomplete G13 record under that FILE
    NAME in another folder, or under a name that merely holds it, is still checked and refused."""
    rec = json.loads(log(g13w, "c2_cand_T28.json", complete=False, incomplete_why=["x"]).read_text())
    real = g13w.tmp / "real" / "pool_drops_r1.json"
    (g13w.tmp / "real").mkdir()
    (g13w.tmp / "other").mkdir()
    copies = [g13w.tmp / "other" / "pool_drops_r1.json", g13w.tmp / "my_pool_drops_r1.json",
              g13w.tmp / "pool_drops_r1_copy.json", g13w.tmp / "pool_drops_r2.json",
              g13w.tmp / "other" / "pool_drops_r1.json.bak"]
    for f in (real, *copies):
        f.write_text(json.dumps(rec))
    monkeypatch.setattr(m, "POOL_DROPS_R1", real)
    assert probs(real) == []                                                       # the exempt path itself: skipped, as before
    stale = log(g13w, "c2_cand_T01.json")                                          # a stale record at the exempt path: skipped too
    stale_rec = json.loads(stale.read_text())
    real.write_text(json.dumps(stale_rec))
    c2io.fam_files("T01")["cand"].write_text("rebuilt after the G13 run\n")
    assert probs(real) == []
    real.write_text(json.dumps(rec))
    for f in copies:
        p = probs(f)
        assert any("incomplete G13 log" in x for x in p), (f.name, p)             # name / substring is no exemption
        with pytest.raises(SystemExit, match="incomplete G13 log"):
            m.g13_drop_ids(type("A", (), {"final": True})(), c2io.C2InputLog(), [str(f)], [])
    monkeypatch.setattr(m, "POOL_DROPS_R1", copies[0].parent / "nowhere_r1.json")  # the exemption moves with the constant
    assert probs(real) != [] and probs(copies[0]) != []


def test_the_mixers_input_log_does_not_follow_a_link_into_a_refused_folder(g13w, leak):
    import os
    hid = _refused_folder(g13w.tmp)
    link = g13w.tmp / "benign_drop.json"
    os.symlink(hid / "drop.json", link)                                            # a plain list (not a G13 log): the mixer reads those
    ok = g13w.tmp / "ok_drop.json"
    ok.write_text(json.dumps({"drop_ids": ["z"]}))
    ilog = m.MixInputLog()
    assert isinstance(ilog, sel.LinkGuardedInputLog) and ilog.check(ok) == ok
    leak.clear()
    for call in (lambda: ilog.check(link), lambda: ilog.json(link), lambda: ilog.record(link),
                 lambda: m.g13_log_problems(ilog, [str(link)]),
                 lambda: m.g13_drop_ids(type("A", (), {"final": False})(), ilog, [str(ok), str(link)], []),
                 lambda: m.mx.decontam_drop_ids(ilog, [str(link)])):
        with pytest.raises(c2io.C2Refused):
            call()
    assert leak == [] and {Path(k).name for k in ilog.entries} <= {"ok_drop.json"}, (leak, ilog.entries)   # the link was never logged


def test_a_g13_log_that_is_a_link_into_a_refused_folder_stops_the_mixer_even_in_a_dry_run(flow, g13w, leak):
    import os
    args, writes, inp = flow
    hid = _refused_folder(g13w.tmp)
    link = g13w.tmp / "c2_cand_T28.json"
    os.symlink(hid / "log.json", link)
    leak.clear()
    with pytest.raises(c2io.C2Refused):
        m.build(args(decontam_drops=[str(link)]))
    assert leak == [], leak


def test_the_mixer_still_exempts_the_round_1_list_by_its_real_path(g13w):
    """The mixer's exemption (spec 5.4, the original behaviour) is unchanged: a G13-shaped record AT m.POOL_DROPS_R1 is skipped,
    by path; --exclude-ids has no such exemption (test_c2_select)."""
    rec = json.loads(log(g13w, "c2_cand_T28.json", complete=False, incomplete_why=["x"]).read_text())

    class Faked(c2io.C2InputLog):
        def json(self, p):
            return rec if Path(p).resolve() == m.POOL_DROPS_R1.resolve() else super().json(p)

    assert m.g13_log_problems(Faked(), [str(m.POOL_DROPS_R1)]) == []
    other = g13w.tmp / "pool_drops_r1.json"

    class Faked2(Faked):
        def json(self, p):
            return rec if Path(p).resolve() == other.resolve() else super().json(p)

    other.write_text(json.dumps(rec))
    assert m.g13_log_problems(Faked2(), [str(other)]) != []
