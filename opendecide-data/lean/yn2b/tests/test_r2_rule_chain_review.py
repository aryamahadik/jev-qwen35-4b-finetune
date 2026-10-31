"""Reviewer R2 tooling for F1 (yn2b/r2_rule_chain_review.py) and the R2 fixes in the F1 generator
(golden_src/gen3/gen3_rule_chain.py, rc_skins.py, rc_render.py, rc_core.py, rc_numeric.py): blind compare, question
mapping, readers and flags, verdict, the generator's cue / clause-group / wrong-outcome helpers, and the written rows
(no cheap reader above 60%, no open reading, no incoherent facts, gate and blind records consistent with the data).
CPU only; read only (data/ and the real MANIFEST are never written)."""
from __future__ import annotations

import json
import random
import sys
from collections import Counter
from pathlib import Path

import pytest

YN2B = Path(__file__).resolve().parents[1]
LEAN = YN2B.parent
for _p in (str(YN2B), str(LEAN / "golden_src" / "gen3")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True
import r2_rule_chain_review as R  # noqa: E402
import gen3_rule_chain as G  # noqa: E402
import rc_core as RC  # noqa: E402
import rc_skins as SK  # noqa: E402

HAVE_ROWS = R.TRAIN_PATH.exists() and R.DEV_PATH.exists()
written = pytest.mark.skipif(not HAVE_ROWS, reason="F1 rows not written")


def _row(rid, gold, options=("yes", "no"), qkind="yn", latent="L1", **meta):
    m = {"qkind": qkind, "judge": False, "latent_id": latent, "view": "base", "dev_kind": None,
         "pack": "a_hoa_bylaws", "plant_dir": None, "shortcut_hits": {}, "edge": "", "fmt": "kv", "tpl": "pos1",
         "defs": None}
    m.update(meta)
    return {"rid": rid, "key": "gen3_rule_chain", "gold": gold, "options": list(options), "state": "s",
            "instructions": "q?", "meta": m}


@pytest.fixture(scope="module")
def parts():
    if not HAVE_ROWS:
        pytest.skip("F1 rows not written")
    return {"train": R.read_jsonl(R.TRAIN_PATH), "dev": R.read_jsonl(R.DEV_PATH)}


# ------------------------------------------------------------------------------------------------ pure helpers
def test_blind_compare_counts_misses_and_stale():
    rows = [_row("a", "yes"), _row("b", "no"),
            _row("c", "x", options=("x", "y"), qkind="choice", dev_kind="holdout")]
    out = R.blind_compare({"a": "yes", "b": "yes", "c": "x", "gone": "yes"}, rows)
    assert (out["n"], out["agree"], out["stale"]) == (3, 2, ["gone"])
    assert out["misses"] == [{"rid": "b", "blind": "yes", "gold": "no", "pack": "a_hoa_bylaws"}]
    assert out["by_part"] == {"dev_holdout": {"agree": 1, "n": 1}, "train": {"agree": 1, "n": 2}}
    with pytest.raises(ValueError):
        R.blind_compare({"a": "maybe"}, rows)


def test_target_group_and_question_mapping():
    jb = _row("j", "B", options=("A", "B"), qkind="jb")
    assert R.group_of(jb) == "binary" and R.target(jb) == "no" and R.target(_row("a", "yes")) == "yes"
    ch = _row("c", "y", options=("x", "y", "z"), qkind="choice")
    assert R.group_of(ch) == "choice" and R.target(ch) == "1"
    yn = _row("y", "yes")
    for q, holds, want in (("pos", True, "yes"), ("pos", False, "no"), ("inv", True, "no"), ("inv", False, "yes"),
                           ("jdg", True, "yes"), ("jinv", True, "no")):
        assert R.holds_answer(yn, {"q": q}, holds) == want, (q, holds)
    assert R.holds_answer(jb, {"q": "jbq"}, True) == "A" and R.holds_answer(jb, {"q": "jbf"}, False) == "B"
    assert R.holds_answer(yn, {"q": "out"}, True) is None and R.holds_answer(yn, None, True) is None


def test_bins_and_reference_numbers():
    bins = ["less than $590", "$590 to $789", "$790 to $989", "$990 or more"]
    assert [R._bin_of(bins, x) for x in (10, 590, 789, 790, 5000)] == [bins[0], bins[1], bins[1], bins[2], bins[3]]
    assert R._bin_of(bins, None) is None
    assert R._ref_num("Section 3.2 (time limit)") == pytest.approx(3.02)
    assert R._ref_num("Rule 12 (exclusion)") == 12.0 and R._ref_num("Table 1 (category limits)") == 1.0


def _rep(**over):
    rep = {"binary": {"categorical": {}, "numeric": {}, "tfidf": {}, "readers_train": {}, "readers_dev": {},
                      "ngram_state": {"held_out_mean": 0.5}},
           "choice": {"categorical": {}, "numeric": {}, "tfidf": {}, "option_readers_train": {},
                      "option_readers_dev": {}, "ngram_state": {"held_out_mean": 0.2}},
           "solvers": {"train": {}, "dev": {}}, "ablation_solvers": {"train": {}, "dev": {}},
           "plants": {"train": {"rows": 10, "obey_plant_acc": 0.5}, "dev": {"rows": 0, "obey_plant_acc": 0}}}
    for k, v in over.items():
        rep[k[0]][k[1]] = v
    return rep


def test_flags_partial_reasoning_small_sample_and_report_only():
    rep = _rep()
    rep["binary"]["readers_train"] = {"doc_missing_means_docs": {"acc": 0.7, "coverage": 0.3, "n": 500,
                                                                 "latents": 300}}
    rep["binary"]["readers_dev"] = {"named_cue_present": {"acc": 0.7, "coverage": 0.3, "n": 40, "latents": 20}}
    rep["binary"]["readers_train"]["named_cue_present"] = {"acc": 0.55, "coverage": 0.3, "n": 500, "latents": 300}
    rep["choice"]["option_readers_train"] = {
        "amt:bin_of_min(request,max limit)": {"acc": 0.7, "coverage": 1.0, "n": 300, "latents": 200},
        "amt:bin_of_request": {"acc": 0.7, "coverage": 1.0, "n": 300, "latents": 200}}
    rep["binary"]["categorical"] = {"edge:exception": {"half->half": {"held_out": 0.9}},
                                    "tpl": {"train->dev": {"held_out": 0.61}}}
    bad = R.flags(rep)
    names = {b[1] for b in bad}
    assert names == {"reader:doc_missing_means_docs", "option:amt:bin_of_request", "cat:tpl"}
    assert [x[1] for x in rep["small_sample"]] == ["reader:named_cue_present"]
    assert {x[1] for x in rep["report_only"]} == {"cat:edge:exception", "option:amt:bin_of_min(request,max limit)"}
    rep2 = _rep()
    rep2["plants"]["train"]["obey_plant_acc"] = 0.7
    assert R.flags(rep2) == [("plants", "obey_plant", "train", 0.7)]


def test_verdict_reasons():
    g = {"decide2": {"train": {"disagree": 0, "undefined": 0, "structure": {"ok": True}}},
         "readings": {"_ok": True}, "coherence": {"train": {"zero_quantity": {"rows": 3}}},
         "mv_core_checks": {"train": {"balance": True}}, "shortcuts": {"flags": []},
         "blind": {"final": {"rate": 1.0, "open_generator_bugs": 0}}, "tests": {"failed": 0}}
    assert R.verdict(g) == {"green": True, "reasons": []}
    g["coherence"]["train"]["received_before_event"] = {"rows": 1}
    g["blind"] = None
    v = R.verdict(g)
    assert not v["green"] and len(v["reasons"]) == 2


# ------------------------------------------------------------------------------------------------ generator fixes
def test_cue_codes_and_clause_groups():
    sk = SK.skin("warranty_returns")
    case = {"docs": True, "flags": {f: False for f in sk["flags"]}}
    assert G.cue_codes(sk, case) == set()
    case["docs"] = None
    assert G.cue_codes(sk, case) == {"DOCS"}
    excl = next(f for f, x in sk["flags"].items() if x["role"] == "excl")
    case.update(docs=False, flags={**case["flags"], excl: True})
    assert G.cue_codes(sk, case) == {"DOCS", "EXCL"}
    assert {G.CLAUSE_GROUP[k] for k in ("lim_gen", "lim_tab")} == {"limit"} and G.CLAUSE_GROUP["excexc"] == "exc"


def test_kind_balance_prefers_groups_a_kind_reader_wins():
    kb = G.KindBalance()
    kb.add("req", {"req", "exc"}, 10)
    kb.add("exc", {"exc", "excl"}, 2)
    # req: gold in every row that offers it; excl: offered, never gold yet (prior 1/2); exc: gold 2 of 12 offers
    assert kb.need("req") > kb.need("excl") > kb.need("exc")


def test_wrong_outcome_never_names_an_absent_cue_and_prefers_the_tempting_one():
    b = G.RuleChainBuilder.__new__(G.RuleChainBuilder)
    rng = random.Random(3)
    code = "FULL"
    others = [c for c in SK.CODES if c != code]
    for _ in range(200):     # no cue in the case: DOCS / EXCL are never named, whatever the solvers say
        c = b._wrong_x(code, {"keyword_overlap": "DOCS", "ignore_exceptions": "EXCL"}, set(), others, rng)
        assert "DOCS" not in c and "EXCL" not in c and code not in c
    firsts = Counter(b._wrong_x(code, {"ignore_exceptions": "INELIG"}, {"DOCS"}, others, rng)[0] for _ in range(400))
    assert firsts["DOCS"] / 400 > 0.8          # the document is missing: 'document missing' is the tempting outcome


def test_exclusion_labels_fit_every_exclusion_they_stand_for():
    assert SK.SKINS["warranty_returns"]["outcomes"]["EXCL"] == "refund refused - item excluded from the warranty"
    assert SK.SKINS["pharmacy_formulary"]["outcomes"]["EXCL"] == "not covered - fill excluded by the formulary"
    for (skin, _f), (word, _why) in R.EXCL_LABEL_MISFIT.items():
        assert word not in f" {SK.SKINS[skin]['outcomes']['EXCL']} "


def test_positive_eligibility_quantities_never_sample_zero():
    sk = SK.skin("shipping_tariff")
    rng = random.Random(0)
    for _ in range(300):
        thr = RC._thr(rng, sk)
        assert RC._elig_value(rng, sk, "le", thr, True, None) > 0
    assert "shipping_tariff" in RC.POSITIVE_ELIG and "hoa_bylaws" not in RC.POSITIVE_ELIG


# ------------------------------------------------------------------------------------------------ written rows
@written
def test_no_open_reading_and_no_incoherent_fact(parts):
    rd = R.readings(parts)
    assert rd["_ok"], rd
    for p in ("train", "dev"):
        for name in ("decisive_outcome=code+amount", "business_limit=count", "nb_pct_direction=strict",
                     "nb_revision_by_date=True", "excl_label_wording"):
            assert rd[p][name]["changed"] == 0, (p, name, rd[p][name]["examples"])
        coh = R.coherence_hunt(parts[p])
        assert not any(coh.get(k, {}).get("rows") for k in R.COHERENCE_BLOCKING), coh
        for r in parts[p]:
            i = R.read_f1a(r)
            if i and i["skin"] in RC.POSITIVE_ELIG:
                assert i["case"].elig.v > 0, r["rid"]


@written
def test_no_cheap_reader_above_the_cap_on_train(parts):
    tr = parts["train"]
    br = R.binary_readers(tr)
    for k in ("doc_missing_means_docs", "excl_flag_means_excl", "named_cue_present", "cue_means_refused",
              "trust_record"):
        assert br[k]["acc"] <= R.CAP, (k, br[k])
    assert abs(br["obey_plant"]["acc"] - 0.5) <= 0.1, br["obey_plant"]
    cr = R.choice_readers(tr)
    for k in ("amt:bin_of_request", "dec:requirement_option", "dec:limit_option", "dec:exception_option",
              "out:cue_outcome", "out:first", "out:last", "amt:first", "dec:first"):
        assert cr[k]["acc"] <= R.CAP, (k, cr[k])


@written
def test_partial_amount_rows_put_the_request_above_the_gold_range(parts):
    n = 0
    for r in parts["train"] + parts["dev"]:
        if r["meta"]["tpl"] not in ("amt1", "amt2") or r["meta"]["view"] == "contrast":
            continue        # a contrast twin keeps the base row's ranges; only its gold range is balanced
        o = R.solve(r)
        if o["code"] != "PARTIAL" or r["gold"] == r["options"][-1]:
            continue
        n += 1
        assert R._bin_of(r["options"], R.read_f1a(r)["amount"]) != r["gold"], r["rid"]
    assert n > 50


@written
def test_extra_requirement_option_labels_use_the_right_article(parts):
    for r in parts["train"] + parts["dev"]:
        for o in r["options"]:
            if "extra requirement for " in o:
                art, noun = o.split("extra requirement for ", 1)[1].split(" ", 1)
                assert art == ("an" if noun[0] in "aeiou" else "a"), (r["rid"], o)


@written
def test_written_gate_and_blind_records_match_the_written_rows():
    if not R.GATE_FILE.exists() or not R.BLIND_FILE.exists():
        pytest.skip("gate / blind records not written yet")
    g = json.loads(R.GATE_FILE.read_text())
    b = json.loads(R.BLIND_FILE.read_text())
    sha = {p: R.sha256(q) for p, q in (("train", R.TRAIN_PATH), ("dev", R.DEV_PATH))}
    if {p: g["inputs"][p]["sha256"] for p in sha} != sha:
        pytest.skip("written rows differ from the gate inputs")
    assert g["verdict"]["green"], g["verdict"]
    fin = b["final"]
    assert (fin["train_sha256"], fin["dev_sha256"]) == (sha["train"], sha["dev"])
    assert fin["rate"] >= 0.97 and fin["open_generator_bugs"] == 0
    last = b["rounds"][-1]
    rows = R.read_jsonl(R.TRAIN_PATH) + R.read_jsonl(R.DEV_PATH)
    rc = R.blind_compare({x["rid"]: x["blind"] for x in last["items"]}, rows)
    assert rc["n"] == len(last["items"]) == 100 and rc["agree"] == fin["agree"] and not rc["stale"]
    assert Counter(x["part"] for x in last["items"]) == {"train": 60, "dev_holdout": 40}
