"""Reviewer R2 tooling for F6 (yn2b/r2_def_literal_review.py): blind compare, text cues and reader heuristics,
shortcut flags (reasoning tags report-only), coherence hunt, unless-scope readings, verdict, and the written gate and
blind records against the written rows. CPU only; read only."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

YN2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(YN2B))
sys.dont_write_bytecode = True
import r2_def_literal_review as R  # noqa: E402

DEF = ("An applicant is a 'life member' only if all of the following hold: (a) the applicant has been a member for at "
       "least 15 years; (b) the applicant is aged more than 60 years. It is not a 'life member' if the applicant has "
       "not paid this year's dues in full, unless the applicant has served on a club committee. It is also not a "
       "'life member' if the applicant lives in the harbour district or the river valley. An applicant who owns a "
       "registered boat also counts as a 'life member' even if the listed conditions are not met, provided no "
       "exclusion applies. A fact the file does not record counts as not established.")
CARD = {"Bylaw 48": DEF, "yes": "the applicant meets Bylaw 48 as written", "no": "the applicant does not meet it"}


def _row(rid, gold, options=("yes", "no"), qkind="yn", latent="L1", state="s", q="q?", **meta):
    m = {"qkind": qkind, "judge": False, "latent_id": latent, "view": "base", "dev_kind": None, "pack": "club",
         "plant_dir": None, "shortcut_hits": {}, "edge": "", "fmt": "kv", "tpl": "is0", "defs": None}
    m.update(meta)
    return {"rid": rid, "gold": gold, "options": list(options), "state": state, "instructions": q, "meta": m}


def _kv(fields, record=None, bg=()):
    lines = ["file.reference: MB-123456", "file.opened: 3 March 2026", "file.membership secretary: Tavo Brin"]
    if record:
        lines.append(f"file.recorded classification: {record}")
    lines += ["applicant.description: Pera Lund"] + [f"applicant.{k}: {v}" for k, v in fields]
    lines += [f"background.{i + 1}: {b}" for i, b in enumerate(bg)] + ["notes.1: File opened by Tavo Brin on 3 March "
                                                                      "2026."]
    return "\n".join(lines)


FIELDS = [("years of membership", "20 years"), ("age", "61 years"), ("dues paid", "yes"),
          ("home district", "the Old Town"), ("owns a registered boat", "no"), ("committee service", "no")]


# ------------------------------------------------------------------------------------------------ blind compare
def test_blind_compare_counts_misses_and_stale():
    rows = [_row("a", "yes"), _row("b", "no"), _row("c", "x", options=("x", "y"), qkind="choice", dev_kind="holdout")]
    out = R.blind_compare({"a": "yes", "b": "yes", "c": "x", "gone": "yes"}, rows)
    assert (out["n"], out["agree"], out["stale"]) == (3, 2, ["gone"])
    assert out["misses"] == [{"rid": "b", "blind": "yes", "gold": "no", "pack": "club"}]
    assert out["by_part"] == {"dev_holdout": {"agree": 1, "n": 1}, "train": {"agree": 1, "n": 2}}
    with pytest.raises(ValueError):
        R.blind_compare({"a": "maybe"}, rows)


def test_target_reads_jb_first_option_as_yes():
    jb = _row("b", "S is false.", options=("S is true.", "S is false."), qkind="jb")
    assert R.group_of(jb) == "binary" and R.target(jb) == "no" and R.target(_row("a", "yes")) == "yes"
    ch = _row("c", "y", options=("x", "y", "z"), qkind="choice")
    assert R.group_of(ch) == "choice" and R.target(ch) == "1"


# ------------------------------------------------------------------------------------------------ text reading
def test_states_claim():
    assert R.states_claim("Is the applicant a 'senior member' under the definition in Bylaw 28?")
    assert R.states_claim("Under Rule 4 of the X, does the player count as a 'veteran'?")
    assert R.states_claim("Applying only the definition in Rule 4, is the bid a 'small business'?")
    assert not R.states_claim("Which statement fits the bid under the definition in Rule 10?")
    assert not R.states_claim("Taking Section 12 as the binding definition, which outcome applies to the incident?")
    assert not R.states_claim("Under Rule 4 of the X, is the player a 'veteran' or not?")


def test_text_cues_and_reader_heuristics():
    st = _kv(FIELDS, bg=("Under the county sports council's rules, an applicant who has never served on a club "
                         "committee is not treated as a 'life member'.",
                         "At the boathouse, Pera Lund is commonly referred to as a 'life member'."))
    r = dict(_row("a", "yes", state=st, q="Does the applicant count as a 'life member' as Bylaw 48 defines that "
                                          "term?"), _defs=CARD)
    c = R.text_cues(r)
    assert (c["usage"], c["outside"], c["record"], c["missing"]) == (True, False, None, False)
    assert (c["joiner"], c["n_excl"], c["n_el"], c["deem"], c["unless"]) == ("all", 2, 2, True, True)
    h = R.reader_heuristics([r])
    assert h["obey_usage"]["acc"] == 1.0 and h["obey_outside_rule"]["acc"] == 0.0
    assert h["deeming_means_is"]["acc"] == 1.0 and h["exclusion_means_not"]["acc"] == 0.0
    judge = dict(_row("j", "no", state=_kv(FIELDS, record="not a 'life member'"),
                      q="Is the applicant's recorded classification supported by the definition in Bylaw 48?",
                      judge=True), _defs=CARD)
    assert R.text_cues(judge)["record"] is False
    assert R.answer_if_applies(judge, True) == "no" and R.answer_if_applies(judge, False) == "yes"


def test_flags_report_only_and_verdict():
    rep = {g: {"categorical": {"fmt": {"train->dev": {"held_out": 0.7}},
                               "edge:exc:allow_deny": {"half->half": {"held_out": 0.65}}},
               "ngram_state": {"held_out_mean": 0.5}, "ngram_question_options": {"held_out_mean": 0.5}}
           for g in ("binary", "choice")}
    rep["binary"]["tfidf"] = {"question train->dev": {"acc": 0.56}}
    rep["binary"]["readers_train"] = {"deeming_means_is": {"acc": 0.69, "coverage": 0.33}}
    rep["solvers"] = {"train": {"swap_joiner": {"acc": 0.3, "n": 100}}}
    rep["plants"] = {"train": {"rows": 10, "obey_plant_acc": 0.5}}
    fl = R.flags(rep)
    assert ("binary", "cat:fmt", "train->dev", 0.7) in fl and ("binary", "tfidf:question train->dev", "", 0.56) in fl
    assert ("binary", "reader:deeming_means_is", "train", 0.69) in fl
    assert not [f for f in fl if "edge:" in f[1]] and rep["report_only"]
    g = {"decide2": {"train": {"disagree": 0, "undefined": 0, "structure": {"equiv:ok": 3}}},
         "readings": {"_ok": True}, "coherence": {"train": {}}, "mv_core_checks": {"train": {"balance": True}},
         "shortcuts": {"flags": []}, "blind": {"final": {"rate": 0.98, "open_generator_bugs": 0}},
         "tests": {"failed": 0}}
    assert R.verdict(g) == {"green": True, "reasons": []}
    g["coherence"] = {"dev": {"months_vs_move_in": {"rows": 2, "decisive": 2, "rids": []}}}
    assert not R.verdict(g)["green"]


# ------------------------------------------------------------------------------------------------ coherence
def test_coherence_hunt_flags_contradictions():
    old = [("years of membership", "35 years"), ("age", "19 years")] + FIELDS[2:]
    r = dict(_row("a", "no", state=_kv(old), q="Does the applicant count as a 'life member' as Bylaw 48 defines "
                                                "that term?"), _defs=CARD)
    ch = R.coherence_hunt([r])
    assert ch["duration_over_age"]["rows"] == 1 and ch["duration_over_age"]["decisive"] == 1
    late = FIELDS + [("application date", "1 June 2026")]
    r2 = dict(r, rid="b", state=_kv(late))
    assert R.coherence_hunt([r2])["event_after_opened"]["rows"] == 1
    assert R.coherence_hunt([dict(r, rid="c", state=_kv(FIELDS))]) == {}
    fb = dict(r, rid="d", options=list(R.FALLBACK), instructions="Which statement fits the applicant under the "
                                                                  "definition in Bylaw 48?")
    assert R.coherence_hunt([fb])["jb_fallback_no_claim"]["rows"] == 1


def test_unless_scope_reading_needs_the_sentence_form():
    st = _kv([(k, ("no" if k == "dues paid" else ("yes" if k == "committee service" else
                                                  ("the river valley" if k == "home district" else v))))
              for k, v in FIELDS])
    r = dict(_row("a", "no", state=st, q="Does the applicant count as a 'life member' as Bylaw 48 defines that "
                                         "term?"), _defs=CARD)
    out = R.unless_scope([r])
    assert out["unless_carries_forward"]["changed"] == 1 and out["unless_carries_forward"]["settled_by"]
    old = dict(r, _defs={**CARD, "Bylaw 48": DEF.replace(". It is also not a 'life member' if the applicant",
                                                         "; nor if the applicant")})
    out = R.unless_scope([old])
    assert out["unless_carries_forward"]["definitions_in_old_list_form"] == 1
    assert out["unless_carries_forward"]["settled_by"] is None


# ------------------------------------------------------------------------------------------------ written records
@pytest.mark.skipif(not (R.TRAIN_PATH.exists() and R.DEV_PATH.exists()), reason="F6 rows not written")
def test_decide2_and_coherence_on_written_rows():
    rows = R.read_jsonl(R.TRAIN_PATH)
    rels = R.read_jsonl(R.REL_PATHS["train"])
    d = R.decide2_check(rows, rels)
    assert d["disagree"] == 0 and d["undefined"] == 0 and not any(k.endswith(":bad") for k in d["structure"])
    dev = R.read_jsonl(R.DEV_PATH)
    assert R.coherence_hunt(rows) == {} and R.coherence_hunt(dev) == {}
    rd = R.readings({"train": rows, "dev": dev})
    assert rd["_ok"]
    assert rd["train"]["unless_carries_forward"]["definitions_in_old_list_form"] == 0


@pytest.mark.skipif(not R.GATE_FILE.exists(), reason="no gate written yet")
def test_written_gate_matches_the_written_rows():
    g = json.loads(R.GATE_FILE.read_text())
    for p, path in (("train", R.TRAIN_PATH), ("dev", R.DEV_PATH)):
        if R.sha256(path) != g["inputs"][p]["sha256"]:
            pytest.skip("written rows differ from the gate inputs (rows rebuilt since)")
    assert g["verdict"]["green"], g["verdict"]
    for p in ("train", "dev"):
        assert g["decide2"][p]["disagree"] == 0 and g["decide2"][p]["undefined"] == 0
        assert g["coherence"][p] == {}


@pytest.mark.skipif(not R.BLIND_FILE.exists(), reason="no blind record written yet")
def test_blind_record_is_consistent():
    b = json.loads(R.BLIND_FILE.read_text())
    for rnd in b["rounds"]:
        n = len(rnd["items"])
        assert n == rnd["result"]["n"] and sum(x["agree"] for x in rnd["items"]) == rnd["result"]["agree"]
        assert all(x["blind"] for x in rnd["items"])
        for x in rnd["items"]:
            if not x["agree"]:
                assert x.get("note"), x["rid"]   # every miss is traced
    assert [r["result"]["n"] for r in b["rounds"]][:2] == [100, 100]
    for rnd in b["rounds"][:2]:
        assert rnd["result"]["by_part"]["train"]["n"] == 60 and rnd["result"]["by_part"]["dev_holdout"]["n"] == 40
    final = b["final"]
    assert final["rate"] >= 0.97 and final["open_generator_bugs"] == 0
    rnd = [r for r in b["rounds"] if r["build"] == "final"][0]
    if R.sha256(R.TRAIN_PATH) == rnd["train_sha256"] and R.sha256(R.DEV_PATH) == rnd["dev_sha256"]:
        rows = R.read_jsonl(R.TRAIN_PATH) + R.read_jsonl(R.DEV_PATH)
        items = rnd["items"] + b["rounds"][1]["items"]
        cmp = R.blind_compare({x["rid"]: x["blind"] for x in items}, rows)
        assert cmp["agree"] == final["agree"] and not cmp["stale"]
