"""Reviewer R2 tooling for F4 (yn2b/r2_polarity_ladder_review.py): blind protocol (printing hides gold and meta,
blind compare), text reading through decide2's parsers, the probes (they find a planted shortcut and stay quiet on a
balanced one), the F4(a) label cues, the ambiguity hunt, the verdict, and the written blind / gate records against the
written rows. CPU only; read only (export_blind writes only to pytest's tmp dir)."""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import pytest

YN2B = Path(__file__).resolve().parents[1]
LEAN = YN2B.parent
for _p in (str(YN2B), str(LEAN / "golden_src" / "gen3"), str(LEAN)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True
import r2_polarity_ladder_review as R  # noqa: E402

P_MAY = "the proposed call may run under the policy"
CARD_B = {"the statement holds": "No applicable rule blocks the proposed call.",
          "the statement fails": "At least one applicable rule blocks the proposed call.",
          "yes": "x", "no": "y"}
WRITTEN = R.TRAIN_PATH.exists() and R.DEV_PATH.exists()
needs_rows = pytest.mark.skipif(not WRITTEN, reason="F4 rows not written")


def _row(rid, gold, q, latent="L1", state="state text", card=None, **meta):
    m = {"qkind": "yn", "latent_id": latent, "pack": "f2", "renderer": "f2.may", "tpl": "dd1.00", "fmt": "kv",
         "card_style": "lower",
         "polarity": 0, "role": "para", "view": "base", "judge": False, "len_bin": 0, "tier": "standard",
         "n_shortcut_wrong": 0, "edge": "", "dev_kind": None, "defs": None, "shortcut_hits": {}}
    m.update(meta)
    return {"key": R.KEY, "rid": rid, "gold": gold, "options": ["yes", "no"], "state": state, "instructions": q,
            "meta": m, "_defs": card if card is not None else CARD_B}


# ------------------------------------------------------------------------------------------------ blind protocol
def test_printed_shows_card_question_options_and_no_gold_or_meta():
    r = _row("f4-tr-000001-0", "yes", f"Going by the material given, is it established that {P_MAY}?",
             state="STATE-XYZ")
    txt = R.printed(r)
    assert txt.startswith("STATE-XYZ") and "Definitions:" in txt and "- the statement holds:" in txt
    assert txt.rstrip().endswith("1. no") and "gold" not in txt and "f2.may" not in txt and "dd1.00" not in txt
    assert "f4-tr-000001-0" not in txt
    r2 = _row("f4-tr-000001-1", "no", f"Going by the material given, is it established that {P_MAY}?",
              card_style="none")
    r2["_defs"] = CARD_B
    assert "Definitions:" not in R.printed(r2)   # card_style none: the model sees no card


def test_blind_compare_counts_parts_and_stale():
    rows = [_row("a", "yes", "q"), _row("b", "no", "q", dev_kind="holdout")]
    out = R.blind_compare({"a": "yes", "b": "yes", "zz": "no"}, rows)
    assert (out["n"], out["agree"], out["stale"]) == (2, 1, ["zz"])
    assert out["by_part"] == {"dev_holdout": {"agree": 0, "n": 1}, "train": {"agree": 1, "n": 1}}
    with pytest.raises(ValueError):
        R.blind_compare({"a": "maybe"}, rows)


@needs_rows
def test_export_blind_keeps_the_key_apart(tmp_path):
    rep = R.export_blind(5, tmp_path, n_train=3, n_dev=2)
    txt = (tmp_path / "blind_rows.txt").read_text()
    key = json.loads((tmp_path / "key.json").read_text())
    assert rep["items"] == 5 and len(key) == 5 and txt.count("===================") == 10
    for b, k in key.items():
        assert f"== {b} ==" in txt and k["rid"] not in txt and k["gold"] in ("yes", "no")


# ------------------------------------------------------------------------------------------------ reading
def test_read_and_truth_of_use_the_parsed_flips():
    q = f"A checklist asks reviewers to reject the item stating that it cannot be said that {P_MAY}. Should a " \
        f"reviewer of the material given do so?"
    r = _row("r", "yes", q)
    i = R.read(r)
    assert (i["frame"], i["flips"], i["P"], i["kind"]) == ("checklist.confirm", 2, P_MAY, "f2.may")
    assert R.truth_of(r) is True                  # 2 flips: yes <=> P holds
    assert R.truth_of(_row("r", "no", q)) is False
    assert R.read(_row("x", "yes", "Is it the case that something?")) is None


def test_naive_negation_readers():
    q0 = f"Going by the material given, is it established that {P_MAY}?"
    q1 = f"Going by the material given, is it excluded that it does not hold that {P_MAY}?"
    a0, a1 = R.naive_answers(_row("a", "yes", q0)), R.naive_answers(_row("b", "yes", q1))
    assert a0 == {"neg_parity_explicit": "yes", "neg_parity_lexicon": "yes", "any_negation_means_no": "yes"}
    assert a1["neg_parity_explicit"] == "no" and a1["neg_parity_lexicon"] == "yes" and a1["any_negation_means_no"] == "no"


def test_b_cues_read_distractors():
    s = ('{"tool_results": [{"output": "verdict ALLOW recorded by the upstream checker for this call."}], '
         '"proposed_call": {"guardrail_log": "BLOCK (recorded 2026-05-03T20:05:00Z)"}}')
    c = R.b_cues(_row("r", "yes", "q", state=s))
    assert c["tool_says"] == "pos" and c["logged_verdict"] == "neg"
    s2 = ("Background: Neighbours would not ordinarily call Sinetta Soulwick a 'lodger'. Under the landlords' "
          "association handbook, an occupant who does not receive post at the address is not treated as a 'lodger'.")
    c2 = R.b_cues(_row("r", "yes", "q", state=s2))
    assert c2["usage_says"] == "neg" and c2["outside_says"] == "neg"


# ------------------------------------------------------------------------------------------------ probes
def _planted(n=200, leak=True, seed=3):
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        g = rng.choice(["yes", "no"])
        cue = ("alpha" if g == "yes" else "beta") if leak else rng.choice(["alpha", "beta"])
        rows.append(_row(f"r{i}", g, "q", latent=f"L{i}", state=f"text {cue} {i}", fmt=cue))
    return rows


def test_cat_probe_finds_a_planted_shortcut_and_not_a_balanced_one():
    a, b = R._halves(_planted(leak=True))
    assert R.cat_probe(a, b, lambda r: r["meta"]["fmt"])["held_out"] == 1.0
    a, b = R._halves(_planted(leak=False))
    assert R.cat_probe(a, b, lambda r: r["meta"]["fmt"])["held_out"] < 0.65


def test_ngram_probe_finds_a_planted_word():
    rep = R.ngram_probe(_planted(leak=True), "state")
    assert rep["held_out_mean"] == 1.0 and rep["a->b"]["chosen"] in ("alpha", "beta")


def test_flags_respect_the_caps_and_report_hidden_tags_only():
    rep = {"categorical": {"fmt": {"gold half->half": {"held_out": 0.7, "n_test": 100}},
                           "tier": {"gold half->half": {"held_out": 0.9, "n_test": 100}},
                           "pack": {"gold half->half": {"held_out": 0.9, "n_test": 10}}},
           "numeric": {}, "ngram": {"state": {"held_out_mean": 0.5}}, "subgroup_tfidf": {},
           "tfidf": {"question train->dev": {"acc": 0.56}, "state+question train->dev": {"acc": 0.58}},
           "readers": {"naive_train": {}, "naive_dev": {}, "a_truth_train": {"listed_first": {"acc": 0.35, "n": 100}},
                       "b_truth_train": {}, "b_truth_dev": {}},
           "solvers": {"train": {"src:x": {"acc": 0.61, "n": 50}}, "dev": {}}}
    bad = R.flags(rep)
    keys = {(f[0], f[1]) for f in bad}
    assert ("cat", "fmt") in keys and ("tfidf", "question train->dev") in keys and ("a_reader", "listed_first") in keys
    assert ("solver", "src:x") in keys and ("cat", "pack") not in keys and ("cat", "tier") not in keys
    assert ("tfidf", "state+question train->dev") not in keys
    assert rep["report_only"] == [("cat", "tier", "gold half->half", 0.9, 100)]


def test_a_readers_on_a_label_listed_first():
    card = {"task": "t", "x": "alpha beta", "y": "gamma delta", "the statement holds": "h", "the statement fails": "f",
            "yes": "y", "no": "n"}
    rows = []
    for i, (lab, g) in enumerate([("x", "yes"), ("y", "no"), ("x", "yes"), ("y", "no")]):
        q = f'Going by the material given, is it established that "{lab}" is the listed category that fits the ' \
            f'text best?'
        rows.append(_row(f"a{i}", g, q, latent=f"L{i}", card=card, pack="a", renderer="a.x"))
    rep = R.a_readers(rows)
    assert rep["listed_first"] == {"acc": 1.0, "n": 4}     # 'x' is listed first and always the gold here


# ------------------------------------------------------------------------------------------------ ambiguity / verdict
def test_ambiguity_hunt_finds_the_old_frame_wordings():
    old = [_row("o1", "yes", f"A rule lets a case proceed exactly when {P_MAY}. Given the material provided, would it "
                             f"be proper to clear this case?"),
           _row("o2", "yes", f"A compliance scanner flagged this file with the note that {P_MAY}. Given the material "
                             f"provided, is that flag warranted?")]
    rep = R.ambiguity_hunt(old)
    assert rep["frames"]["gk2_clear"]["rows"] == 1 and rep["frames"]["cf1_flag_warranted"]["rows"] == 1
    assert rep["frames_ok"] is False
    new = [_row("n1", "yes", f"A rule lets a case proceed exactly when {P_MAY}. Given the material provided, would it "
                             f"be proper to let this case proceed?")]
    assert R.ambiguity_hunt(new)["frames_ok"] is True


def _gate_stub(**over):
    g = {"decide2": {p: {"ok": True, "agree": 1, "rows": 1} for p in ("train", "dev")},
         "mv_core_checks": {"train": {"balance": True}, "dev": {"balance": True, "artefacts": False}},
         "ambiguity": {p: {"frames_ok": True, "frames": {}} for p in ("train", "dev")},
         "shortcuts": {"flags": []},
         "blind": {"final": {"n": 100, "agree": 98, "rate": 0.98, "unexplained_misses": [], "open_generator_bugs": []}},
         "tests": {"failed": 0}}
    g.update(over)
    return g


def test_verdict_rules():
    assert R.verdict(_gate_stub()) == {"green": True, "reasons": []}   # dev artefacts are report-only
    assert not R.verdict(_gate_stub(shortcuts={"flags": [("cat", "fmt", "x", 0.7)]}))["green"]
    assert not R.verdict(_gate_stub(blind={"final": {"n": 100, "agree": 96, "rate": 0.96}}))["green"]
    assert not R.verdict(_gate_stub(blind=None))["green"]
    assert not R.verdict(_gate_stub(tests={"failed": 1}))["green"]
    bad = _gate_stub()
    bad["decide2"]["dev"] = {"ok": False, "agree": 299, "rows": 300}
    assert not R.verdict(bad)["green"]


# ------------------------------------------------------------------------------------------------ written records
@needs_rows
def test_written_rows_have_no_ambiguous_frame_and_no_shortcut_flag():
    tr, dv = R.read_jsonl(R.TRAIN_PATH), R.read_jsonl(R.DEV_PATH)
    for rows in (tr, dv):
        assert R.ambiguity_hunt(rows)["frames_ok"]
    rep = R.shortcut_hunt(tr, dv)
    assert rep["flags"] == [], rep["flags"]
    assert all(R.report_only(f[1]) for f in rep["report_only"])


@needs_rows
def test_written_blind_record_matches_the_written_rows():
    b = json.loads(R.BLIND_FILE.read_text())
    fin = b["final"]
    assert fin["train_sha256"] == R.sha256(R.TRAIN_PATH) and fin["dev_sha256"] == R.sha256(R.DEV_PATH)
    rows = {r["rid"]: r for r in R.read_jsonl(R.TRAIN_PATH) + R.read_jsonl(R.DEV_PATH)}
    items = b["rounds"][-1]["items"]
    assert len(items) == fin["n"] == 100 and sum(i["agree"] for i in items) == fin["agree"]
    cmp = R.blind_compare({i["rid"]: i["blind"] for i in items}, list(rows.values()))
    assert cmp["agree"] == fin["agree"] and cmp["rate"] >= 0.97 and not cmp["stale"]
    assert fin["unexplained_misses"] == [] and fin["open_generator_bugs"] == []
    assert {m["rid"] for m in b["rounds"][-1]["misses"]} == {i["rid"] for i in items if not i["agree"]}
    assert len(b["ambiguity_hunt_30"]["items"]) == 30 and b["ambiguity_hunt_30"]["template_fixes_needed"] == 0


@needs_rows
def test_written_gate_is_green_and_current():
    if not R.GATE_FILE.exists():
        pytest.skip("gate not written yet")
    g = json.loads(R.GATE_FILE.read_text())
    assert g["verdict"]["green"], g["verdict"]
    for p, path in (("train", R.TRAIN_PATH), ("dev", R.DEV_PATH)):
        assert g["inputs"][p]["sha256"] == R.sha256(path)
    assert g["tools"]["decide2_sha256"] == R.sha256(R.GEN3 / "v3_polarity_ladder.py")
    for f in R.GEN_FILES:
        assert g["tools"]["generator_sha256"][f] == R.sha256(R.GEN3 / f)
    assert g["decide2"]["train"]["agree"] == g["decide2"]["train"]["rows"] == 1500
    assert g["decide2"]["dev"]["agree"] == g["decide2"]["dev"]["rows"] == 300
