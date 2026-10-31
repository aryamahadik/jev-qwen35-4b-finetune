"""Tests for the A100 waiver in select_candidate.py (PREREG Record A100): with a valid waiver a candidate is eligible iff its failed
checks are a subset of {b_transfer}; otherwise nothing changes. Synthetic records and tmp files; no Modal, no OHS path.
  cd lean/c2_build/train && ../../../.venv/bin/python -B -m pytest -q tests/test_waiver_a100_select.py"""
import json
import sys
import textwrap
from pathlib import Path

import numpy as np
import pytest

TRAIN = Path(__file__).resolve().parents[1]
C2B = TRAIN.parent
sys.path.insert(0, str(TRAIN))
sys.path.insert(0, str(C2B))
import select_candidate as sc  # noqa: E402
import waiver_a100 as wv  # noqa: E402

QUOTE = wv.A100_QUOTE
N = 400


def rec(name, acc_g=0.9, acc_r=0.7, fail=(), seed=0):
    """A candidate record: gproxy and rmixdev items (same ids and clusters for every candidate) and the 11 booleans."""
    rng = np.random.default_rng(seed)
    items = {}
    for comp, acc in (("gproxy", acc_g), ("rmixdev", acc_r)):
        items[comp] = {"id": [f"{comp}{i}" for i in range(N)], "cluster": [f"c{i // 2}" for i in range(N)],
                       "correct": [int(x) for x in (rng.random(N) < acc)]}
    return {"candidate": name, "items": items, "eligibility": {k: k not in fail for k in sc.ELIG_KEYS}}


def grid_names():
    return ["final_a10", "final_a08", "last3_a09", "earlylate_a05"]


def recs_with(**fails):
    return {n: rec(n, fail=fails.get(n, ()), seed=i) for i, n in enumerate(grid_names())}


def test_eligible_without_a_waiver_is_unchanged():
    assert sc.eligible({"eligibility": {k: True for k in sc.ELIG_KEYS}}) == (True, [])
    assert sc.eligible(rec("x", fail=("b_transfer",))) == (False, ["b_transfer"])
    assert sc.eligible(rec("x", fail=("b_transfer",)), ()) == (False, ["b_transfer"])
    assert sc.eligible({}) == (False, list(sc.ELIG_KEYS))


def test_a100_waived_b_is_eligible_but_nothing_else_is():
    w = ("b_transfer",)
    assert sc.eligible(rec("x", fail=("b_transfer",)), w) == (True, [])
    assert sc.eligible(rec("x", fail=()), w) == (True, [])
    for other in ("a_learning", "c1_D1", "c2_D2", "c3_D3", "c4_D4", "c5_D5", "c6_D6", "c7_D9", "d_complement", "gproxy_rule_4_3"):
        assert sc.eligible(rec("x", fail=("b_transfer", other)), w) == (False, [other])      # b plus any other failure stays ineligible
        assert sc.eligible(rec("x", fail=(other,)), w) == (False, [other])
    r = rec("x")
    r["eligibility"]["b_transfer"] = None                       # not measured: the waiver covers a FAILED (b), not a missing one
    assert sc.eligible(r, w) == (False, ["b_transfer"])
    r["eligibility"].pop("b_transfer")
    assert sc.eligible(r, w) == (False, ["b_transfer"])
    r["eligibility"]["b_transfer"] = "False"                    # a string is not a boolean failure
    assert sc.eligible(r, w) == (False, ["b_transfer"])
    assert sc.eligible(rec("x", fail=("b_transfer",)), ("a_learning",)) == (False, ["b_transfer"])   # only the keys it is given


def test_a100_choose_all_fail_b_no_waiver_none_with_waiver_final_step():
    recs = {n: rec(n, fail=("b_transfer",), seed=i) for i, n in enumerate(grid_names())}
    plain = sc.choose(recs, 200)
    assert plain["chosen"] is None and plain["status"].startswith("NO CANDIDATE") and "waiver" not in plain
    assert all("waived_failed" not in r for r in plain["candidates"].values())
    w = sc.choose(recs, 200, waived=("b_transfer",))
    assert w["chosen"] in grid_names() and w["waiver"]["record"] == "A100" and w["waiver"]["banner"] == "check (b) waived by the owner (PREREG A100)"
    assert all(r["eligible"] and r["failed_checks"] == ["b_transfer"] and r["waived_failed"] == ["b_transfer"] for r in w["candidates"].values())
    assert w["rule"] == "A42-D 9.5"


def test_a100_a_candidate_failing_d9_plus_b_stays_out_and_the_final_step_rule_is_unchanged():
    recs = recs_with(**{n: ("b_transfer",) for n in grid_names()})
    recs["final_a08"]["eligibility"]["c7_D9"] = False           # D9 plus (b)
    recs["last3_a09"]["eligibility"]["a_learning"] = False      # (a) plus (b)
    w = sc.choose(recs, 200, waived=("b_transfer",))
    assert w["candidates"]["final_a08"]["eligible"] is False and w["candidates"]["final_a08"]["failed_checks"] == ["b_transfer", "c7_D9"]
    assert w["candidates"]["last3_a09"]["eligible"] is False
    assert w["candidates"]["final_a10"]["eligible"] and w["candidates"]["earlylate_a05"]["eligible"]
    # 9.5 unchanged: the final step is eligible, so it stays unless the best-S eligible one has CI LB > 0 over it
    assert w["chosen"] == "final_a10" or (w["best_eligible"] == w["chosen"] and w["ci_vs_final"]["lo"] > 0)
    only_one = recs_with(**{n: ("b_transfer", "c7_D9") for n in grid_names()})
    assert sc.choose(only_one, 200, waived=("b_transfer",))["chosen"] is None                   # every candidate also fails D9: none


def test_a100_final_step_ineligible_picks_the_highest_s_eligible_and_better_candidate_needs_the_ci():
    recs = {n: rec(n, acc_g=0.9, acc_r=0.7, fail=("b_transfer",), seed=3) for n in grid_names()}     # identical items: every S equal
    w = sc.choose(recs, 300, waived=("b_transfer",))
    assert w["chosen"] == "final_a10" and w["status"] == "final step is the highest-S eligible candidate"          # tie goes to the final step
    recs["final_a10"]["eligibility"]["c3_D3"] = False
    w = sc.choose(recs, 300, waived=("b_transfer",))
    assert w["chosen"] != "final_a10" and w["status"].startswith("final step not eligible")
    better = {n: rec(n, acc_g=0.9, acc_r=0.7, fail=("b_transfer",), seed=3) for n in grid_names()}
    better["last3_a09"] = rec("last3_a09", acc_g=0.99, acc_r=0.95, fail=("b_transfer",), seed=3)
    w = sc.choose(better, 2000, waived=("b_transfer",))
    assert w["chosen"] == "last3_a09" and w["ci_vs_final"]["lo"] > 0 and w["status"].startswith("CI lower bound > 0")


# ---- the CLI ----------------------------------------------------------------------------------------------------------------
def prereg_text():
    body = textwrap.fill(f'**Record A100 (OWNER words, verbatim): "{QUOTE}"** answering the choice.', 118)
    return "".join(f"> {ln}\n" for ln in body.splitlines())


@pytest.fixture
def cli(tmp_path):
    root = tmp_path / "lean"
    (root / "c2_build/train").mkdir(parents=True)
    (root / wv.OWNER_GO_C2).write_text(f'- Record A100: "{QUOTE}"\n')
    (root / wv.PREREG_FINAL_MD).write_text(prereg_text())
    reads = tmp_path / "reads"
    reads.mkdir()
    recs = {n: rec(n, fail=("b_transfer",), seed=i) for i, n in enumerate(grid_names())}
    for n, r in recs.items():
        (reads / f"{n}.json").write_text(json.dumps(r))
    grid = tmp_path / "grid.json"
    grid.write_text(json.dumps({"grid_sha256": "g" * 64, "candidates": [{"name": n, "adapter_sha256": f"{i:064x}"} for i, n in enumerate(grid_names())]}))
    argv = lambda out, cand: ["--reads", str(reads), "--grid", str(grid), "--out", str(out), "--candidate-out", str(cand), "--resamples", "200",
                              "--root", str(root)]
    return root, tmp_path, argv


def test_a100_cli_with_a_valid_record_prints_the_banner_and_writes_the_chosen_files(cli, capsys):
    root, tmp, argv = cli
    (root / wv.RECORD).write_text(json.dumps({"record": "A100", "quote": QUOTE, "waives": ["b_transfer"], "waived_rule": "b"}))
    assert sc.main(argv(tmp / "CH.json", tmp / "CAND.json")) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[0] == "check (b) waived by the owner (PREREG A100)" and json.loads(out[-1])["chosen"] == "final_a10"
    ch = json.loads((tmp / "CH.json").read_text())
    assert ch["waiver"]["waived"] == ["b_transfer"] and ch["chosen_adapter_sha256"] == f"{0:064x}"
    cand = json.loads((tmp / "CAND.json").read_text())
    assert cand["name"] == "q35_4b_c2" and cand["grid_candidate"] == "final_a10" and cand["adapter_sha256"] == f"{0:064x}"


def test_a100_cli_with_no_or_a_bad_record_is_byte_identical_to_before(cli, capsys):
    root, tmp, argv = cli
    assert sc.main(argv(tmp / "CH0.json", tmp / "CAND0.json")) == 1                         # no record: NO CANDIDATE, as at A98
    plain = capsys.readouterr()
    assert json.loads(plain.out.splitlines()[-1])["chosen"] is None and len(plain.out.splitlines()) == 1 and plain.err == ""
    assert not (tmp / "CAND0.json").exists()
    for bad in ({"record": "A100", "quote": QUOTE[:-25], "waives": ["b_transfer"], "waived_rule": "b"},
                {"record": "A100", "quote": QUOTE, "waives": ["a_learning"], "waived_rule": "b"}):
        (root / wv.RECORD).write_text(json.dumps(bad))
        assert sc.main(argv(tmp / "CH1.json", tmp / "CAND1.json")) == 1
        got = capsys.readouterr()
        assert got.out == plain.out and "no waiver applied" in got.err
        assert (tmp / "CH1.json").read_text() == (tmp / "CH0.json").read_text() and not (tmp / "CAND1.json").exists()
    (root / wv.OWNER_GO_C2).write_text("- no A100 here\n")                                  # the quote not in the owner file
    (root / wv.RECORD).write_text(json.dumps({"record": "A100", "quote": QUOTE, "waives": ["b_transfer"], "waived_rule": "b"}))
    assert sc.main(argv(tmp / "CH2.json", tmp / "CAND2.json")) == 1 and not (tmp / "CAND2.json").exists()
