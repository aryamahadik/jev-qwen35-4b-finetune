"""F1 clause engine (golden_src/gen3/rc_core.py): hand-built documents check every rule the documents state, the
shortcut modes, the decisive-clause analysis, the exception-group classifier and the plan-based sampler."""
from __future__ import annotations

import random
import sys
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
import mv_core as mv  # noqa: E402
import rc_core as RC  # noqa: E402
import rc_skins as SK  # noqa: E402

SKIN = "municipal_fee"   # elig: attendance at most N (max); time: before the event


def base_doc(**kw):
    doc = {"skin": SKIN, "style": "code", "place": "Tovan", "org": "Tovan Works", "count": "calendar",
           "holidays": [], "prec": "specific", "dstyle": "iso", "version": "2025-06-01", "phr": "tr",
           "clauses": [{"id": "r_el", "kind": "req", "gate": "elig", "op": "le", "value": "200", "via": None,
                        "sec": "requirements"},
                       {"id": "r_tm", "kind": "req", "gate": "time", "n": 20, "incl": True, "sec": "requirements"},
                       {"id": "r_dc", "kind": "req", "gate": "docs", "sec": "requirements"},
                       {"id": "e1", "kind": "excl", "cats": [], "conds": [{"t": "flag", "f": "alcohol"}],
                        "sec": "exclusions"},
                       {"id": "lg", "kind": "lim_gen", "limit": 800, "sec": "limits"},
                       {"id": "lt", "kind": "lim_tab", "rows": [["resident", 500], ["school", 900]],
                        "sec": "limits"}]}
    doc.update(kw)
    return doc


def base_case(**kw):
    c = {"ref": "W1234567", "name": "Dara Kelso", "cat": "resident", "type": "community event permit",
         "elig": "150", "event": "2026-05-30", "request": "2026-05-01", "docs": True,
         "flags": {f: False for f in SK.SKINS[SKIN]["flags"]}, "amount": 300, "record": None, "decoy": None}
    c.update(kw)
    return c


def code(doc, case, mode=None):
    return RC.evaluate(doc, case, mode)["code"]


def test_full_and_partial_with_specific_limit():
    d = base_doc()
    assert code(d, base_case(amount=500)) == "FULL"          # exactly at the category limit: not more than it
    assert code(d, base_case(amount=510)) == "PARTIAL"
    tr = RC.evaluate(d, base_case(amount=510))
    assert tr["granted"] == 500 and tr["limit"] == ["lt", 500]


@pytest.mark.parametrize("prec,amount,want", [("specific", 600, "PARTIAL"), ("lower", 600, "PARTIAL"),
                                              ("later", 600, "PARTIAL"), ("specific", 450, "FULL")])
def test_precedence_modes(prec, amount, want):
    d = base_doc(prec=prec)
    assert code(d, base_case(amount=amount)) == want


def test_precedence_later_and_named_pick_the_general_limit():
    d = base_doc(prec="later")
    d["clauses"] = [c for c in d["clauses"] if c["id"] != "lg"] + [{"id": "lg", "kind": "lim_gen", "limit": 800,
                                                                   "sec": "limits"}]
    assert RC.evaluate(d, base_case(amount=700))["limit"] == ["lg", 800]      # general limit now comes later
    d2 = base_doc(prec="named")
    d2["clauses"].append({"id": "pn", "kind": "prec_named", "a": "lt", "b": "lg", "sec": "limits"})
    assert RC.evaluate(d2, base_case(amount=700))["code"] == "FULL"          # $800 prevails over $500


def test_eligibility_boundary_inclusive_and_exclusive():
    d = base_doc()
    assert code(d, base_case(elig="200")) == "FULL"
    d["clauses"][0]["op"] = "lt"
    assert code(d, base_case(elig="200")) == "INELIG"
    assert code(d, base_case(elig="200"), "all_inclusive") == "FULL"


def test_time_requirement_before_event_calendar():
    d = base_doc()                       # at least 20 days before 2026-05-30 -> on or before 2026-05-10
    assert code(d, base_case(request="2026-05-10")) == "FULL"
    assert code(d, base_case(request="2026-05-11")) == "LATE"
    d["clauses"][1]["incl"] = False      # more than 20 days before -> before 2026-05-10
    assert code(d, base_case(request="2026-05-10")) == "LATE"


def test_time_requirement_business_days_with_holidays():
    d = base_doc(count="business", holidays=["2026-05-25"])
    d["clauses"][1]["n"] = 5
    # 5 business days before Sat 2026-05-30, skipping Mon 2026-05-25: Fri 29, Thu 28, Wed 27, Tue 26, Fri 22
    assert RC.deadline(d, base_case(), 5, "before").isoformat() == "2026-05-22"
    assert code(d, base_case(request="2026-05-22")) == "FULL"
    assert code(d, base_case(request="2026-05-23")) == "LATE"


def test_docs_missing_is_not_included():
    d = base_doc()
    assert code(d, base_case(docs=None)) == "DOCS"
    assert code(d, base_case(docs=False)) == "DOCS"


def test_exception_waiver_and_exception_to_exception():
    d = base_doc()
    d["clauses"].append({"id": "x1", "kind": "exc", "target": "r_dc", "mode": "waive", "cats": ["resident"],
                         "conds": [{"t": "flag", "f": "free"}], "sec": "exceptions"})
    case = base_case(docs=False)
    case["flags"]["free"] = True
    assert code(d, case) == "FULL"
    assert code(d, case, "ignore_exceptions") == "DOCS"
    other = dict(case, cat="school")
    assert code(d, other) == "DOCS"                     # the category condition fails
    d["clauses"].append({"id": "xx", "kind": "excexc", "target": "x1", "cats": [],
                         "conds": [{"t": "flag", "f": "repeat"}], "sec": "exceptions"})
    case["flags"]["repeat"] = True
    assert code(d, case) == "DOCS"
    assert RC.groups(d, case) == {"allow_deny": ["x1"]}


def test_period_exception():
    d = base_doc()
    d["clauses"].append({"id": "x1", "kind": "exc", "target": "r_tm", "mode": "period", "n2": 10, "cats": [],
                         "conds": [{"t": "flag", "f": "hardship"}], "sec": "exceptions"})
    case = base_case(request="2026-05-15")
    assert code(d, case) == "LATE"
    case["flags"]["hardship"] = True
    assert code(d, case) == "FULL"
    assert code(d, base_case(request="2026-05-25", flags=dict(case["flags"]))) == "LATE"


def test_exclusion_and_its_exception():
    d = base_doc()
    case = base_case()
    case["flags"]["alcohol"] = True
    assert code(d, case) == "EXCL"
    assert code(d, case, "ignore_exceptions") == "FULL"
    d["clauses"].append({"id": "x2", "kind": "exc", "target": "e1", "mode": "waive", "cats": ["resident"],
                         "conds": [{"t": "flag", "f": "charity"}], "sec": "exceptions"})
    assert code(d, case) == "EXCL"
    case["flags"]["charity"] = True
    assert code(d, case) == "FULL"
    assert RC.groups(d, case) == {"deny_allow": ["e1"]}


def test_amendments_in_force_not_yet_withdrawn():
    d = base_doc()
    am = {"id": "a1", "kind": "amend", "k": 1, "target": "r_tm", "field": "n", "old": "20", "new": "30",
          "eff": "2026-04-15", "withdrawn": False, "sec": "amendments"}
    d["clauses"].append(am)
    case = base_case(request="2026-05-05")              # 25 days before: passes 20, fails 30
    assert code(d, case) == "LATE"
    assert code(d, case, "ignore_amendments") == "FULL"
    am["eff"] = "2026-05-06"                            # not yet in force on the received date
    assert code(d, case) == "FULL"
    assert code(d, case, "latest_dated") == "LATE"
    am["eff"], am["withdrawn"] = "2026-04-15", True
    assert code(d, case) == "FULL"


def test_two_refusal_grounds_are_undefined_and_first_ground_wins_in_modes():
    d = base_doc()
    g, tr = RC.decide(d, base_case(docs=False, elig="300"))
    assert mv.is_undefined(g) and tr["n_fails"] == 2 and tr["code"] == "INELIG"


def test_pivotal_unique_and_first_match():
    d = base_doc()
    d["clauses"].append({"id": "x1", "kind": "exc", "target": "r_dc", "mode": "waive", "cats": [],
                         "conds": [{"t": "flag", "f": "free"}], "sec": "exceptions"})
    case = base_case(docs=False)
    case["flags"]["free"] = True
    assert RC.pivotal(d, case) == ["x1"]
    assert code(d, case, "first_match") == "DOCS"       # the exception comes after the requirement
    sc = RC.shortcut_traces(d, case)
    assert sc["ignore_exceptions"]["code"] == "DOCS" and sc["ignore_amendments"] is None


def test_steps_and_near_miss():
    d = base_doc()
    d["clauses"].append({"id": "x1", "kind": "exc", "target": "r_dc", "mode": "waive", "cats": ["school"],
                         "conds": [{"t": "flag", "f": "free"}], "sec": "exceptions"})
    case = base_case(docs=False)
    case["flags"]["free"] = True
    assert RC.groups(d, case) == {"near_miss": ["x1"]}
    assert 1 <= RC.steps(d, case, RC.evaluate(d, case)) <= 5


FEAS = {"INELIG": [None, "near_miss", "allow_deny", "deny_allow"], "LATE": [None, "near_miss", "allow_deny"],
        "DOCS": [None, "allow_deny", "deny_allow"], "EXCL": ["allow_deny"], "PARTIAL": [None, "deny_allow", "near_miss"],
        "FULL": [None, "deny_allow", "near_miss"]}


@pytest.mark.parametrize("skin", sorted(SK.SKINS))
def test_sampler_realises_planned_code_and_group(skin):
    rng = random.Random(11)
    b = RC.Builder(rng, mv.NamePool("train"))
    made = 0
    for code_, groups in FEAS.items():
        for grp in groups:
            for _ in range(20):
                plan = {"code": code_, "group": grp, "n_distract": 5, "amend": rng.choice([None, "in_force", "not_yet"]),
                        "business": rng.random() < 0.3, "defn": rng.random() < 0.4, "n_repealed": 2,
                        "prec_case": code_ in SK.GRANTS and rng.random() < 0.5}
                try:
                    doc, case = b.sample(skin, "code", plan)
                except mv.Reject:
                    continue
                g, tr = RC.decide(doc, case)
                assert not mv.is_undefined(g)
                assert g == code_, (skin, plan, g)
                assert set(RC.groups(doc, case, tr)) == ({grp} if grp else set()), (skin, plan)
                made += 1
                break
    assert made >= 14


def test_skin_texts_are_option_safe():
    for k, sk in SK.SKINS.items():
        outs = list(sk["outcomes"].values())
        assert len(set(outs)) == 6
        for o in outs:
            assert ": " not in o and "\n" not in o and len(o) <= 200
            assert not mv.judge_violations(o), (k, o)
        assert set(SK.HO_TEXT[k]["proc"]).isdisjoint(sk["proc"])
