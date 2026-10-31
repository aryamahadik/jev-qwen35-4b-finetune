"""Tests for c2_kit.skin (slot-locked renderer, agreement, spans, parser) and c2_kit.lexicon (registry, G-LEX)."""
from __future__ import annotations

import datetime as dt
import json
import random

import pytest
import yaml

from c2_kit import skin as K
from c2_kit import slots as S
from c2_kit.lexicon import LexiconError, LexiconRegistry

DAY = ("day", "days")


@pytest.mark.parametrize("text,art", [
    ("user", "a"), ("unpaid invoice", "an"), ("hour", "an"), ("hotel", "a"), ("one-time fee", "a"), ("8-day", "an"),
    ("11-day", "an"), ("18", "an"), ("110", "a"), ("11,000", "an"), ("1,100", "a"), ("80", "an"), ("SLA", "an"),
    ("URL", "a"), ("HR file", "an"), ("F", "an"), ("European", "a"), ("urgent", "an"), ("unit", "a"),
    ("$12 fee", "a"), ("apple", "an"), ("software", "a"), ("utility", "a"), ("upgrade", "an")])
def test_articles(text, art):
    assert K.article(text) == art


def _slots():
    return {"N": S.count_slot(1, DAY), "M": S.count_slot(8, DAY), "WHO": S.name_slot("Ana Ruiz"),
            "ENV": S.category_slot("prod", {"prod": ["production", "prod"], "stage": ["staging"]}),
            "AMT": S.cents_slot(120000), "DUE": S.date_slot(dt.date(2026, 3, 5)), "ID": S.id_slot("INV-7")}


def test_fill_agreement_modifiers_and_spans():
    sl = _slots()
    tpl = ("{A|ENV} change by {poss|WHO} team, {N} late and {M:adj} window; {N|record is|records are} open. "
           "{cap|ENV} total {AMT} due {DUE:iso} for {ID}.")
    f = K.fill(tpl, sl, {"ENV": "s0", "AMT": "symbol"})
    assert f.text == ("A production change by Ana Ruiz's team, 1 day late and 8-day window; record is open. "
                      "Production total $1,200.00 due 2026-03-05 for INV-7.")
    for sp in f.spans:
        if sp.role == "value" and sp.slot == "AMT":
            assert f.text[sp.start:sp.end] == "$1,200.00"
    assert {sp.slot for sp in f.spans} == set(sl)
    sl2 = dict(sl, N=S.count_slot(3, DAY))
    assert "3 days late" in K.fill(tpl, sl2).text and "records are open" in K.fill(tpl, sl2).text


def test_fill_refuses_bad_templates():
    sl = _slots()
    with pytest.raises(K.RenderError):
        K.fill("{NOPE} x", sl)
    with pytest.raises(K.RenderError):
        K.fill("{WHO|a|b} x", sl)                       # agreement needs a count
    with pytest.raises(K.RenderError):
        K.fill("{ who} x {WHO", sl)                    # malformed
    sk = K.make_skin("s", "R00", "{WHO} and {WHO}", {"WHO": "name"})
    with pytest.raises(K.RenderError):
        sk.fill(sl)                                      # appears twice, required once
    sk = K.make_skin("s", "R00", "{WHO} and {WHO}", {"WHO": "name"}, counts={"WHO": (1, 2)})
    assert sk.fill(sl).text == "Ana Ruiz and Ana Ruiz"
    with pytest.raises(K.RenderError):
        K.make_skin("s", "R00", "{WHO}", {"WHO": "date"}).fill(sl)   # declared kind differs


def test_json_and_yaml_registers_parse_after_fill():
    sl = dict(_slots(), Q=S.category_slot("y", {"y": ["yes"], "n": ["no"]}))
    j = K.fill('{"who": {WHO}, "note": "for {ID}, {N} late", "cents": {AMT:int_cents}, "env": {ENV}}', sl,
               escape="json")
    obj = json.loads(j.text)
    assert obj == {"who": "Ana Ruiz", "note": "for INV-7, 1 day late", "cents": 120000, "env": "production"}
    y = K.fill("who: {WHO}\nanswer: {Q}\ndue: {DUE:iso}\nnote: filed for {ID} late\n", sl, escape="yaml")
    obj = yaml.safe_load(y.text)
    assert obj["answer"] == "yes" and obj["due"] == "2026-03-05" and obj["note"] == "filed for INV-7 late"
    schema = K.schema_of(sl)
    tpl = '{"who": {WHO}, "note": "for {ID}, {N} late", "cents": {AMT:int_cents}, "env": {ENV}}'
    got = K.parse_structured(tpl, j.text, schema, "json")
    assert got == {"WHO": "Ana Ruiz", "ID": "INV-7", "N": 1, "AMT": 120000, "ENV": "prod"}
    got = K.parse_structured("who: {WHO}\nanswer: {Q}\ndue: {DUE:iso}\n", "who: Ana Ruiz\nanswer: \"yes\"\n"
                             "due: \"2026-03-05\"\n", schema, "yaml")
    assert got == {"WHO": "Ana Ruiz", "Q": "y", "DUE": "2026-03-05"}


def test_clause_slots_fill_inner_slots_with_their_own_spans():
    reg = LexiconRegistry("t")
    reg.declare("cmp.le", "comparator", "at most the bound")
    f = reg.add("no more than {X}", "cmp.le", slots={"X": "cents"})
    sl = {"LIMIT": S.cents_slot(5000), "CMP": reg.clause(f.form_id, bind={"X": "LIMIT"})}
    out = K.fill("Amounts {CMP} pass.", sl, {"LIMIT": "symbol"})
    assert out.text == "Amounts no more than $50.00 pass."
    roles = {(sp.slot, sp.role): out.text[sp.start:sp.end] for sp in out.spans}
    assert roles[("CMP", "clause")] == "no more than $50.00" and roles[("LIMIT", "value")] == "$50.00"


def test_template_parser_round_trips_and_checks_grammar():
    rng = random.Random(5)
    tpl = "{A|ENV} run for {WHO} on {DUE}: {N} late, {AMT} owed, {M:adj} hold, {N|item|items} in {ID}."
    for _ in range(200):
        sl = {"N": S.count_slot(rng.randrange(0, 40), DAY), "M": S.count_slot(rng.randrange(1, 20), DAY),
              "WHO": S.name_slot(rng.choice(["Ana Ruiz", "Oscar Lind", "Eve"])),
              "ENV": S.category_slot(rng.choice(["prod", "stage"]), {"prod": ["production"], "stage": ["staging"]}),
              "AMT": S.cents_slot(rng.randrange(0, 10 ** 7)),
              "DUE": S.date_slot(dt.date(2026, 1, 1) + dt.timedelta(days=rng.randrange(400))), "ID": S.id_slot("A-1")}
        forms = {k: rng.choice(S.free_forms(v)) for k, v in sl.items()}
        txt = K.fill(tpl, sl, forms).text
        got = K.match_template(tpl, txt, K.schema_of(sl))
        assert got == {k: S.canonical(v) for k, v in sl.items()}, txt
    good = K.fill(tpl, sl).text
    with pytest.raises(K.TemplateMismatch):
        K.match_template(tpl, good.replace("A staging", "An staging").replace("A production", "An production"),
                         K.schema_of(sl))
    with pytest.raises(K.TemplateMismatch):
        K.match_template("{N} late, {N|item|items}", "3 days late, item", K.schema_of(sl))
    with pytest.raises(K.TemplateMismatch):
        K.match_template("{WHO} and {WHO}", "Ana Ruiz and Eve", K.schema_of(sl))


def test_mode_f_fill_swaps_brief_values():
    sk = K.make_skin("f", "R00", "Ana Ruiz paid on 5 March 2026.", {"WHO": "name", "DUE": "date"}, author_mode="F",
                     brief={"WHO": "Ana Ruiz", "DUE": "5 March 2026"}, haiku_task_id="t", haiku_prompt_sha="0" * 64)
    out = sk.fill({"WHO": S.name_slot("Eve Moss"), "DUE": S.date_slot(dt.date(2026, 4, 1))}, {"DUE": "iso"})
    assert out.text == "Eve Moss paid on 2026-04-01."
    assert [out.text[s.start:s.end] for s in out.spans] == ["Eve Moss", "2026-04-01"]
    with pytest.raises(K.RenderError):
        K.fill_freeform("Ann and Anna", {"A": "Ann", "B": "Ann"}, {"A": S.name_slot("X"), "B": S.name_slot("Y")})
    with pytest.raises(K.RenderError):
        K.make_skin("f2", "R00", "{WHO} paid", {"WHO": "name"}, author_mode="F")


# ------------------------------------------------------------------------------------------------ lexicon

def _reg():
    reg = LexiconRegistry("t")
    reg.declare("cmp.le", "comparator", "less than or equal to the bound")
    reg.declare("cmp.lt", "comparator", "strictly less than the bound")
    reg.declare("cmp.gt", "comparator", "strictly greater than the bound")
    reg.declare("prec.P1", "precedence", "deny beats ask beats allow")
    return reg


def test_add_validates_forms():
    reg = _reg()
    reg.add("no more than {X}", "cmp.le", slots={"X": "cents"})
    for bad in [lambda: reg.add("No  more than {X}", "cmp.le", slots={"X": "cents"}),     # duplicate text
                lambda: reg.add("at most {X}", "cmp.zz", slots={"X": "cents"}),           # undeclared sem
                lambda: reg.add("{X}{Y}", "cmp.le", slots={"X": "cents", "Y": "cents"}),   # adjacent
                lambda: reg.add("at most {a|X}", "cmp.le", slots={"X": "cents"}),         # modifier
                lambda: reg.add("at most {X}", "cmp.le", slots={"X": "clause"}),
                lambda: reg.add("x {X}", "cmp.le", slots={"X": "cents"}, source="haiku")]:  # no task id
        with pytest.raises(LexiconError):
            bad()


def test_unit_tests_parse_alone_and_in_sentences():
    reg = _reg()
    a = reg.add("no more than {X}", "cmp.le", slots={"X": "cents"})
    b = reg.add("more than {X}", "cmp.gt", slots={"X": "cents"})
    c = reg.add("{X} or less", "cmp.le", slots={"X": "cents"})
    assert reg.unit_test_all() == {a.form_id: True, b.form_id: True, c.form_id: True}
    sem, fid, vals = reg.parse_exact("no more than $1,200.00", {"X": S.cents_slot(0).schema})
    assert (sem, fid, vals) == ("cmp.le", a.form_id, {"X": 120000})
    ms = reg.scan("Claims of no more than $50.00 pass; more than $90.00 fail.", {"X": S.cents_slot(0).schema})
    assert [(m.sem_id, m.values["X"]) for m in ms] == [("cmp.le", 5000), ("cmp.gt", 9000)]


def test_unit_test_catches_ambiguous_forms():
    reg = LexiconRegistry("t")
    reg.declare("s.one", "other", "first meaning")
    reg.declare("s.two", "other", "second meaning")
    a = reg.add("{P} or less", "s.one", slots={"P": "name"})
    reg.add("{Q} less", "s.two", slots={"Q": "name"})
    assert reg.unit_test(a.form_id) is False
    assert any("meanings" in p or "scans" in p for p in a.unit_problems)


def test_admission_two_of_two_three_of_three_and_rejection():
    reg = _reg()
    f = reg.add("no more than {X}", "cmp.le", slots={"X": "cents"})
    p = reg.add("deny rules beat ask rules, which beat allow rules", "prec.P1")
    g = reg.add("less than {X}", "cmp.lt", slots={"X": "cents"})
    reg.unit_test_all()
    assert reg.status(f.form_id) == "pending"
    reg.record_extraction(f.form_id, "haiku:a", "cmp.le")
    assert reg.status(f.form_id) == "pending"
    reg.record_extraction(f.form_id, "haiku:b", "cmp.le")
    assert reg.status(f.form_id) == "admitted"                  # 2/2
    for e in ("haiku:a", "haiku:b"):
        reg.record_extraction(p.form_id, e, "prec.P1")
    assert reg.status(p.form_id) == "pending"                   # precedence needs 3/3
    reg.record_extraction(p.form_id, "haiku:c", "prec.P1")
    assert reg.status(p.form_id) == "admitted"
    reg.record_extraction(g.form_id, "haiku:a", "cmp.lt")
    reg.record_extraction(g.form_id, "haiku:b", "cmp.le")       # one disagreement rejects for good
    reg.record_extraction(g.form_id, "haiku:c", "cmp.lt")
    assert reg.status(g.form_id) == "rejected"
    with pytest.raises(LexiconError):
        reg.record_extraction(f.form_id, "haiku:a", "cmp.le")   # extractors are independent
    gate = reg.gate([f.form_id, p.form_id])
    assert gate["pass"]
    gate = reg.gate([f.form_id, g.form_id, "cmp.le#nothere"])
    assert not gate["pass"] and g.form_id in gate["not_admitted"] and gate["unknown"] == ["cmp.le#nothere"]
    with pytest.raises(LexiconError):
        reg.parse_exact("less than $5.00", {"X": S.cents_slot(0).schema}, admitted_only=True)


def test_lexicon_items_are_gold_free_and_persist():
    reg = _reg()
    f = reg.add("no more than {X}", "cmp.le", slots={"X": "cents"})
    reg.unit_test_all()
    (fid, item), = reg.lexicon_items()
    assert fid == f.form_id and set(item) == {"text", "choices"}
    assert "cmp.le" not in json.dumps(item) and len(item["choices"]) == 3
    assert reg.meaning_to_sem("comparator", "less than or equal to the bound") == "cmp.le"
    reg.record_extraction(f.form_id, "haiku:a", "cmp.le")
    reg.record_extraction(f.form_id, "haiku:b", "cmp.le")
    reg.declare_antonym("cmp.le", "cmp.gt")
    back = LexiconRegistry.from_json(json.loads(json.dumps(reg.to_json())))
    assert back.sha256() == reg.sha256() and back.status(f.form_id) == "admitted"
    assert back.is_antonym("cmp.gt", "cmp.le")
