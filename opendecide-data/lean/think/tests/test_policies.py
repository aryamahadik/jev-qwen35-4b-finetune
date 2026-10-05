"""policies.py on CPU with a scripted fake engine: tries, vote, fallback, parsing identical to think_run.py."""
import re

import pytest
from conftest import ScriptEngine, mc_row, yn_row

import policies as P
import think_engine as te


def tp_for(engine, tok, dio):
    return te.ThinkPath(engine, tok, dio)


def test_vote_majority_and_ties():
    assert P.vote(["a", "b", "a", None]) == ("a", {"a": 2, "b": 1})
    assert P.vote(["a", "b", "b", "a"], c1_key="b")[0] == "b"  # tie -> C1's key when tied
    assert P.vote(["a", "b", "b", "a"], c1_key="z")[0] == "a"  # else first seen
    assert P.vote([None, None]) == (None, {})


def test_short_cot_runs_four_tries_in_one_call_and_votes(tok, dio):
    rows = [mc_row("r1", "q one", ["x", "y", "z"], "y"), mc_row("r2", "q two", ["u", "v"], "u")]
    eng = ScriptEngine({"q one": [" B.", " B", "C", "B"], "q two": ["A", "zzz", "B", "A"]})
    recs = P.short_cot(tp_for(eng, tok, dio), [{"id": r["id"], "row": r} for r in rows], c1_keys={"r2": "v"})
    assert eng.calls[0] == (8, 300)  # 2 items x 4 tries, budget 300, one think call
    by = {r["id"]: r for r in recs}
    assert by["r1"]["pred_key"] == "y" and by["r1"]["votes"] == {"y": 3, "z": 1}
    assert by["r2"]["pred_key"] == "u" and by["r2"]["parsed_tries"] == 3  # 'zzz' has no capital letter
    assert all(r["think_tokens"] == 50 for r in recs)


def test_short_cot_steer_is_in_the_think_block(tok, dio):
    rows = [mc_row("r1", "q", ["x", "y"], "x")]
    seen = []

    class Spy(ScriptEngine):
        def generate(self, prompts, params):
            seen.extend(prompts)
            return super().generate(prompts, params)

    P.short_cot(tp_for(Spy({"q": "A"}), tok, dio), [{"id": "r1", "row": rows[0]}], tries=1)
    assert seen[0].endswith("<think>\n" + P.SHORT_STEER)
    assert seen[1].startswith(seen[0]) and seen[1].endswith("</think>\n\n")  # natural end: think + "</think>\n\n"


def test_parse_matches_think_run(tok, dio):
    """think_run.py: first \\b([A-Z])\\b of the 8 answer tokens; yes/no rows: the 'Yes' letter -> yes, else no."""
    rows = [yn_row("y1", "s1", 1), yn_row("y2", "s2", 0), mc_row("m1", "s3", ["p", "q"], "q")]
    eng = ScriptEngine({"s1": " A. Yes", "s2": "I pick B", "s3": " Q is wrong; B"})
    recs = P.run_policy(tp_for(eng, tok, dio), [{"id": r["id"], "row": r} for r in rows], "capped_think",
                        deer=dict(te.DEER, tau=2.0))  # tau 2: never exits early
    by = {r["id"]: r for r in recs}
    assert by["y1"]["final_key"] == "yes" and by["y2"]["final_key"] == "no"
    assert by["m1"]["letter"] == "Q" and by["m1"]["pred_key"] is None  # 'Q' is out of range -> unparsed
    assert by["m1"]["fallback"] is True and by["m1"]["final_key"] is None  # no C1 key given
    m = re.search(r"\b([A-Z])\b", " Q is wrong; B")
    assert m.group(1) == "Q"


def test_fallback_to_c1_and_capped_flag(tok, dio):
    rows = [mc_row("r1", "s", ["a", "b"], "b")]
    eng = ScriptEngine({"s": "no letter here"}, think_len=5000)
    recs = P.run_routed(tp_for(eng, tok, dio), rows, {"r1": {"route": True, "policy": "full_think", "c1_key": "b"}},
                        budget=64)
    assert recs[0]["fallback"] and recs[0]["final_key"] == "b"
    assert recs[0]["capped"] == 1 and recs[0]["think_tokens"] == 64


def test_capped_think_deer_exit(tok, dio):
    rows = [mc_row("r1", "s", ["a", "b"], "a")]
    eng = ScriptEngine({"s": "A"}, think_len=5000)
    recs = P.capped_think(tp_for(eng, tok, dio), [{"id": "r1", "row": rows[0]}])
    r = recs[0]
    assert r["exit"] == "deer" and r["probes"] == 1 and r["think_tokens"] == 128 and r["capped"] == 0


def test_run_routed_only_routed_rows_and_policy(tok, dio):
    rows = [mc_row("r1", "s1", ["1", "2"], "1"), mc_row("r2", "s2", ["a", "b"], "a"), mc_row("r3", "s3", ["a", "b"], "a")]
    dec = {"r1": {"route": True, "policy": "short_cot", "c1_key": "2"},
           "r2": {"route": True, "policy": "capped_think", "c1_key": "a"},
           "r3": {"route": False, "policy": "fast", "c1_key": "a"}}
    recs = P.run_routed(tp_for(ScriptEngine({"s1": "A", "s2": "A", "s3": "A"}), tok, dio), rows, dec)
    assert sorted((r["id"], r["policy"]) for r in recs) == [("r1", "short_cot"), ("r2", "capped_think")]


def test_unknown_policy(tok, dio):
    with pytest.raises(ValueError):
        P.run_policy(tp_for(ScriptEngine({}), tok, dio), [], "long_think")
