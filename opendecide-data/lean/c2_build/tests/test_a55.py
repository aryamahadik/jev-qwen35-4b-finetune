"""Tests for the A55 tools (zed_orch/a55_*.py): the d1 collision rule, the dev-only overlay, the Haiku task builders' pure parts,
the top-up sizing and the seed-base rules. Fast: no family kit is opened except where a tiny fixture is built in memory."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
C2B = HERE.parent
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(C2B / "zed_orch"))

import a55_common as C  # noqa: E402
import a55_overlay as OV  # noqa: E402
import a55_topup as T  # noqa: E402
from c2_kit.lexicon import LexiconRegistry  # noqa: E402


# ---------------------------------------------------------------------------------------------------- helpers
def row(i, state, options=None, **meta):
    return {"id": f"T12-{i}", "state": state, "instructions": "", "options": options or [], "qtype": "noul", "gold": 0,
            "meta": {"family": "T12", "wording_id": f"w{i}", "card_id": f"c{i}", "domain_pack": f"t12-pack-{i}",
                     "c2": {"skin_id": f"s{i}", "register": "memo"}, **meta}}


# ---------------------------------------------------------------------------------------------------- d1
def test_numeral_item_and_normalisation():
    assert C.numeral_item(("ng", "the invoice is 4500 usd"))
    assert not C.numeral_item(("ng", "the invoice is paid in full"))
    assert C.is_value("r1") and C.is_value("2025") and not C.is_value("usd")
    assert C.nl("  a \t b  c ") == "a b c"


def test_collisions_line_id_and_item():
    cand = [row(1, "Header line here\nTotal due 4500 USD for the order\nOrder ref INV-48211 filed",
                ["The invoice should be released to payment now"]),
            row(2, "Another memo about a supplier\nTotal due 4500 USD for the order")]
    ci = C.CandIndex("T12", cand)
    same_line = row(9, "A different first line entirely\nTotal due   4500 USD for the order")
    c = ci.collisions(same_line, "line")
    assert c["line"] == 1 and c["id"] == 0
    same_id = row(10, "Nothing in common here at all\nOrder ref INV-48211 filed")
    assert ci.collisions(same_id, "line")["id"] == 1
    other = row(11, "Nothing in common here at all\nOrder ref INV-99999 filed late")
    c = ci.collisions(other, "item")
    assert not C.CandIndex.hit(c)
    assert C.CandIndex.hit(ci.collisions(same_line, "line"))


def test_item_level_needs_a_numeral():
    cand = [row(1, "Words only here that repeat in the dev row exactly as written one two three four five six")]
    ci = C.CandIndex("T12", cand)
    dev = row(2, "Words only here that repeat in the dev row exactly as written one two three four five six")
    c = ci.collisions(dev, "item")
    assert c["item"] == 0 and c["line"] == 0                      # no numeral: not the d1 rule's business


# ---------------------------------------------------------------------------------------------------- seeds
def test_seed_base_733_is_disjoint_and_3m_is_not():
    got = T.choose_base("T12")
    assert got["base"] == 733_000_000 and got["bases"] == [733_000_000, 734_000_000, 735_000_000]
    with pytest.raises(SystemExit):
        T.choose_base("T12", 3_000_000)
    with pytest.raises(SystemExit):
        T.choose_base("T12", 733_000_001)                          # not divisible by 32


def test_fallback_when_733_is_in_use(monkeypatch):
    real = T.recorded_bases

    def used(fam=None):
        d = real(fam)
        d[733_000_000] = ["test"]
        return d
    monkeypatch.setattr(T, "recorded_bases", used)
    assert T.choose_base("T12")["base"] == 743_000_000
    monkeypatch.setattr(T, "recorded_bases", lambda fam=None: {**real(fam), 733_000_000: ["x"], 743_000_000: ["y"]})
    with pytest.raises(SystemExit):
        T.choose_base("T12")


def test_redraw_class_residue():
    assert 733_000_000 % C.REDRAW_STRIDE == 33_000_000 and 743_000_000 % C.REDRAW_STRIDE == 43_000_000
    assert not T.overlaps(T.seed_intervals(733_000_000), [iv for b in T.RULING_BASES for iv in T.seed_intervals(b)])


# ---------------------------------------------------------------------------------------------------- sizing
def test_topup_decision_formula(monkeypatch):
    import a55_measure as M
    monkeypatch.setattr(M, "qc_keep_rate", lambda fam: {"q": 0.9})
    m = {"target": 600, "E": 560, "E_low": 500, "E_high": 600, "rows": 800}
    d = M.topup_decision("T24", m)
    s, q = 560 / 800, 0.9
    assert d["topup"] and d["X"] == math.ceil((1.06 * 600 - 560) / (s * q))
    assert d["trigger_E_below"] == 618.0
    assert not M.topup_decision("T24", {**m, "E": 618})["topup"]     # E >= 1.03 x target: no top-up
    assert not M.topup_decision("T25", {**m, "E": 100})["topup"]     # T25 has no L2
    assert M.topup_decision("T12", {**m, "target": 800, "E": 823})["trigger_E_below"] == 824.0


def test_targets_and_thresholds_match_the_ruling():
    assert {f: C.TARGET[f] for f in C.FAMILIES} == {"T24": 600, "T25": 600, "T06": 900, "T07": 800, "T23": 800, "T26": 1400, "T28": 2400, "T12": 800}
    thr = {f: round(1.03 * t) for f, t in C.TARGET.items()}
    assert thr["T24"] == 618 and thr["T06"] == 927 and thr["T07"] == 824 and thr["T26"] == 1442 and thr["T28"] == 2472
    assert C.D1_STRIDE % 32 == 0 and all(C.D1_STRIDE % k == 0 for k in range(1, 17))


# ---------------------------------------------------------------------------------------------------- overlay (tiny fixture)
class FakeKit:
    def __init__(self, plugin, ctx):
        self.plugin, self.ctx = plugin, ctx


def _registry():
    reg = LexiconRegistry("T24")
    reg.declare("t24.exc", "other", "cases in the named category are excluded")
    reg.declare("t24.alt", "other", "cases with the named condition get the named outcome")
    return reg


def test_overlay_adds_forms_and_shadows_admitted_forms(tmp_path, monkeypatch):
    reg = _registry()
    base = reg.add("The {C} category is excluded and receives nothing", "t24.exc", slots={"C": "category"}, family="T24")
    reg.unit_test(base.form_id)
    reg.record_extraction(base.form_id, "e1", "t24.exc")
    reg.record_extraction(base.form_id, "e2", "t24.exc")
    texts = ["Anything in the {C} group is left out entirely", "No cover is given to the {C} group at all",
             "Cases filed under {C} receive no cover whatsoever", "The policy leaves the {C} group without any cover"]
    forms = []
    for i, t in enumerate(texts):
        fid = f"t24.exc#{__import__('hashlib').sha256(t.encode()).hexdigest()[:8]}"
        forms.append({"form_id": fid, "unit": "t24.exc", "sem_id": "t24.exc", "kind": "other", "text": t, "slots": {"C": "category"},
                      "haiku_task_id": "T24-x-000", "haiku_prompt_sha": "p" * 64, "extractions": [["e1", "t24.exc"], ["e2", "t24.exc"]]})
    fr = {"units": {"t24.exc": {"used": True, "admitted": 4}, "t24.alt": {"used": False, "admitted": 2}}, "forms": forms,
          "self_sha256": "abc"}
    (tmp_path / "FROZEN.json").write_text(json.dumps(fr))

    class Plug:
        HELD_OUT_SAMPLERS = ("S5",)
        lexicon = reg
        _form_cache = {"t24.exc": [base.form_id]}

        def admitted_forms(self, sem):
            return [base.form_id]
    p = Plug()
    kit = FakeKit(p, types_ctx(reg))
    rec = OV.add_to_kit("T24", kit, root=tmp_path)
    assert rec["forms"] == 4 and rec["units_used"] == ["t24.exc"] and rec["units_skipped"] == ["t24.alt"]
    got = p.admitted_forms("t24.exc")
    assert len(got) == 4 and base.form_id not in got
    assert all(reg.forms[f].held_out and reg.status(f) == "admitted" for f in got)
    OV.remove_shadows(kit)
    assert p.admitted_forms("t24.exc") == [base.form_id]          # the shadow is gone
    assert "admitted_forms" not in p.__dict__


def types_ctx(reg):
    import types
    return types.SimpleNamespace(lexicon=reg, skins={})


def test_overlay_with_too_few_forms_keeps_training_forms(tmp_path):
    reg = _registry()
    base = reg.add("The {C} category is excluded and receives nothing", "t24.exc", slots={"C": "category"}, family="T24")
    reg.unit_test(base.form_id)
    t = "Anything in the {C} group is left out entirely"
    fid = f"t24.exc#{__import__('hashlib').sha256(t.encode()).hexdigest()[:8]}"
    fr = {"units": {"t24.exc": {"used": True, "admitted": 1}},
          "forms": [{"form_id": fid, "unit": "t24.exc", "sem_id": "t24.exc", "kind": "other", "text": t, "slots": {"C": "category"},
                     "haiku_task_id": "T24-x-000", "haiku_prompt_sha": "p" * 64, "extractions": [["e1", "t24.exc"], ["e2", "t24.exc"]]}]}
    (tmp_path / "FROZEN.json").write_text(json.dumps(fr))

    class Plug:
        HELD_OUT_SAMPLERS = ("S5",)
        lexicon = reg

        def admitted_forms(self, sem):
            return ["training"]
    p = Plug()
    kit = FakeKit(p, types_ctx(reg))
    OV.add_to_kit("T24", kit, root=tmp_path)
    assert p.admitted_forms("t24.exc") == ["training"]             # 1 < 4 admitted: the sem keeps its training forms


def test_overlay_inactive_without_frozen_file(tmp_path):
    reg = _registry()

    class Plug:
        lexicon = reg
    kit = FakeKit(Plug(), types_ctx(reg))
    assert OV.add_to_kit("T24", kit, root=tmp_path) == {"frozen": False}
    assert OV.add_to_kit("T23", kit, root=tmp_path) == {}           # a family without an overlay


# ---------------------------------------------------------------------------------------------------- devforms (pure parts)
def test_openings_and_dev_dir():
    import a55_devforms as D
    ops = D.openings(["Cases whose {M} is above {X} qualify", "Cases whose {M} is below {X} fail", "Only cases whose {M} is {X}"])
    assert ops[0] == "Cases whose {M}"
    assert D.dev_dir("T24").as_posix().endswith("zed_orch/a55_dev/T24")
    assert D.norm("  A  b ") == "a b"
    assert set(D.ADAPTERS) == {"T24", "T06", "T07", "T25"}


def test_ohs4_counts_refuses_an_unscanned_checker():
    import a55_devforms as D
    reg = _registry()
    f = reg.add("The {C} category is excluded and receives nothing", "t24.exc", slots={"C": "category"}, family="T24")
    cands = [{"form_id": f.form_id, "text": f.text}]
    with pytest.raises(SystemExit):
        D.ohs4_counts("T24", reg, cands, checker=lambda recs: {"status": "missing"})
    ok = D.ohs4_counts("T24", reg, cands, checker=lambda recs: {"status": "scanned", "hit_ids": []})
    assert ok["hit_forms"] == [] and ok["records"] == 2
    hit = D.ohs4_counts("T24", reg, cands, checker=lambda recs: {"status": "scanned", "hit_ids": [recs[0]["id"]]})
    assert hit["hit_forms"] == [f.form_id]
