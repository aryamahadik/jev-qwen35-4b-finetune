"""F6 gen3_def_literal: the label program (dl_core.decide), its uniqueness rule, the shortcut solvers and the row tags,
on hand-written facts. CPU only; writes nothing."""
from __future__ import annotations

import copy
import random
import sys
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
import dl_core as dc  # noqa: E402
import dl_packs as dp  # noqa: E402
import dl_sample as ds  # noqa: E402
import mv_core as mv  # noqa: E402


def facts(**kw):
    """A customs 'fruit' item: AND of net weight >= 500 kg and chilled; exclusion: packed in drums unless sealed."""
    f = {"pack": "customs", "term": "customs:fruit", "entity": "consignment", "joiner": "all",
         "elements": [{"attr": "net_weight", "kind": "num", "op": ">=", "limit": 500},
                      {"attr": "chilled", "kind": "flag", "want": True}],
         "exclusions": [{"trigger": {"attr": "packing", "kind": "cat", "values": ["drums"]},
                         "unless": {"attr": "sealed", "kind": "flag", "want": True}}],
         "deem": None,
         "outside": {"regime": "the Inland Freight Code", "cond": {"attr": "moisture", "kind": "num", "op": "<",
                                                                       "limit": 10}, "effect": "excl"},
         "r_card": False, "r_facts": False,
         "values": {"net_weight": 500, "chilled": True, "packing": "crates", "sealed": False, "moisture": 8},
         "order": ["net_weight", "chilled", "packing", "sealed", "moisture"],
         "usage": {"text": "Botanically, the tomato is the fruit of the tomato plant.", "verdict": True},
         "record": None}
    f.update(kw)
    return f


def test_and_definition_boundary_inclusive():
    f = facts()
    assert dc.decide(f, "is")[0] is True
    assert dc.decide(dict(f, values={**f["values"], "net_weight": 499}), "is")[0] is False


def test_not_and_jb_questions():
    f = facts()
    assert dc.decide(f, "not")[0] is False and dc.decide(f, "jb")[0] is True


def test_exclusion_and_unless():
    f = facts(values={**facts()["values"], "packing": "drums"})
    assert dc.decide(f, "is")[0] is False                       # the exclusion applies
    g = facts(values={**f["values"], "sealed": True})
    assert dc.decide(g, "is")[0] is True                        # ... unless the container was sealed
    h = facts(values={**f["values"], "sealed": None})
    assert dc.decide(h, "is")[0] is False                       # an unrecorded 'unless' part does not rescue


def test_missing_values():
    f = facts(values={**facts()["values"], "chilled": None})
    assert dc.decide(f, "is")[0] is False                       # an unrecorded element is not met
    g = facts(values={**facts()["values"], "packing": None})
    assert dc.decide(g, "is")[0] is True                        # an unrecorded trigger does not exclude
    assert dc.missing_tag(f) == "missing_info:decisive"
    assert dc.missing_tag(g) == "missing_info:decisive"         # recording 'drums' would change the outcome
    h = facts(values={**facts()["values"], "moisture": 8, "origin": None}, order=facts()["order"] + ["origin"])
    assert dc.missing_tag(h) == "missing_info:irrelevant"


def test_or_definition_and_uniqueness():
    f = facts(joiner="any", values={**facts()["values"], "net_weight": 100})
    assert dc.decide(f, "is")[0] is True                        # one element suffices
    two = facts(joiner="any")
    assert mv.is_undefined(dc.decide(two, "is")[0])            # two independent sufficient reasons
    both_fail = facts(values={**facts()["values"], "net_weight": 1, "chilled": False})
    assert mv.is_undefined(dc.decide(both_fail, "is")[0])      # two failing AND elements


def test_element_fail_plus_exclusion_is_undefined():
    f = facts(values={**facts()["values"], "net_weight": 1, "packing": "drums"})
    assert mv.is_undefined(dc.decide(f, "is")[0])


def test_deeming_clause_and_outside_rule_in_card():
    f = facts(values={**facts()["values"], "net_weight": 1},
              deem={"attr": "origin", "kind": "cat", "values": ["a free-trade zone"]})
    f["values"]["origin"] = "a free-trade zone"
    assert dc.decide(f, "is")[0] is True                        # deemed, although an element fails
    g = facts(r_card=True)                                     # the outside rule (moisture < 10%) as an exclusion
    assert dc.decide(g, "is")[0] is False
    h = facts(r_card=True, outside={**facts()["outside"], "effect": "incl"},
              values={**facts()["values"], "net_weight": 1})
    assert dc.decide(h, "is")[0] is True                        # ... or as the deeming clause
    k = facts(r_facts=True)
    assert dc.decide(k, "is")[0] is True                        # in the facts only: ignored


def test_judge_and_choice():
    f = facts(record=True)
    assert dc.decide(f, "judge")[0] is True and dc.decide(f, "judge_n")[0] is False
    assert dc.decide(dict(f, record=False), "judge")[0] is False
    assert mv.is_undefined(dc.decide(facts(), "judge")[0])
    assert dc.decide(facts(), "choice")[0] == "none"
    assert dc.decide(facts(values={**facts()["values"], "chilled": False}), "choice")[0] == ("el", 1)
    assert dc.decide(facts(values={**facts()["values"], "packing": "drums"}), "choice")[0] == ("ex", 0)
    assert dc.decide(facts(r_card=True), "choice")[0] == ("r",)
    assert mv.is_undefined(dc.decide(facts(joiner="any", values={**facts()["values"], "net_weight": 1}),
                                     "choice")[0])


def test_shortcuts_answer_only_with_their_cue():
    f = facts()
    sv = dc.shortcut_verdicts(f)
    assert sv["world_knowledge"] is True and "other_regime" not in sv and "ignore_exclusions" not in sv
    assert sv["strict_limits"] is False                         # 500 kg read as 'more than 500 kg'
    g = facts(values={**f["values"], "packing": "drums", "sealed": True})
    sv = dc.shortcut_verdicts(g)
    assert sv["trigger_excludes"] is False and sv["ignore_exclusions"] is True
    h = facts(r_facts=True)
    assert dc.shortcut_verdicts(h)["other_regime"] is False


def test_exception_groups():
    assert dc.exc_group(facts()) is None
    assert dc.exc_group(facts(values={**facts()["values"], "packing": "drums"})) == "exc:allow_deny"
    assert dc.exc_group(facts(values={**facts()["values"], "packing": "drums", "sealed": True})) == "exc:deny_allow"
    near = facts(exclusions=[{"trigger": {"attr": "storage", "kind": "num", "op": ">=", "limit": 30},
                              "unless": None}], values={**facts()["values"], "storage": 29},
                 order=facts()["order"] + ["storage"])
    assert dc.exc_group(near) == "exc:near_miss"


@pytest.mark.parametrize("tier", ["easy", "standard", "judge", "hard"])
def test_sampler_hits_its_targets_and_decide_agrees(tier):
    rng = random.Random(7)
    pool = mv.NamePool("train")
    made = 0
    for i in range(300):
        truth = i % 2 == 0
        dk = ("path", "deem", "rincl")[i % 3] if truth else ("elem", "excl", "rexcl")[i % 3]
        excg = "allow_deny" if dk in ("excl", "rexcl") else None
        ctx = {"gid": dp.terms_for("train")[i % len(dp.terms_for("train"))], "tier": tier, "dk": dk, "truth": truth,
               "excg": excg, "miss": None, "r_place": "card" if dk in ("rincl", "rexcl") else "none"}
        try:
            f = ds.sample(rng, ctx, pool)
        except ds.SampleFail:
            continue
        made += 1
        g, _ = dc.decide(f, "is")
        assert g == truth
        assert f["outside"]["cond"]["attr"] not in [c["attr"] for c in f["elements"]]
        assert dc.holds(f["outside"]["cond"], f["values"]) is True     # the outside rule always holds
    assert made > 100


def test_value_for_boundaries():
    a = dp.PACKS["customs"].attr("net_weight")
    c = {"attr": "net_weight", "kind": "num", "op": ">", "limit": 500}
    rng = random.Random(1)
    assert ds.value_for(rng, a, c, False, "at") == 500
    assert ds.value_for(rng, a, c, True, "off1") == 501
    for _ in range(50):
        v = ds.value_for(rng, a, c, True, "far")
        assert v > 502 and dc.holds(c, {"net_weight": v})


def test_twin_flip_is_one_atom():
    f = facts()
    g = copy.deepcopy(f)
    g["values"]["chilled"] = False
    assert dc.decide(g, "is")[0] is False and dc.decide(f, "is")[0] is True
