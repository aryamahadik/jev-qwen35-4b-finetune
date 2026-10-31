"""Unit tests of the F6 decide2 (golden_src/gen3/v3_def_literal.py) on HAND-WRITTEN rows: the definition grammar, the
verb-phrase catalogue, the five state formats, the question templates and the decision rule. No generator code is
used: the rows below are typed from the surface described in yn2b/F6_DEF_LITERAL_NOTES.md."""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))

import dl_packs as P  # noqa: E402  (surface data only)
import v3_def_literal as v3  # noqa: E402

DEF = ("An applicant is a 'life member' only if all of the following hold: (a) the applicant has been a member for at "
       "least 15 years; (b) the applicant is aged more than 60 years. It is not a 'life member' if the applicant has "
       "not paid this year's dues in full, unless the applicant has served on a club committee. It is also not a "
       "'life member' if the applicant lives in the harbour district or the river valley. An applicant who owns a registered boat also counts as a "
       "'life member' even if the listed conditions are not met, provided no exclusion applies. A fact the file does "
       "not record counts as not established.")
CLAUSE = "Bylaw 48"
INSTR = "Bylaws of the Northmere Rowing Club"
CARD = {CLAUSE: DEF,
        "yes": f"the applicant meets {CLAUSE} as written, so it is a 'life member' under the {INSTR}; everyday usage "
               "and other rule books do not change this.",
        "no": f"the applicant does not meet {CLAUSE} as written, so it is not a 'life member' under the {INSTR}; "
              "everyday usage and other rule books do not change this."}
# the facts: membership 15 years, age 61, dues not paid, committee yes, district the Old Town, boat not recorded
FIELDS = [("years of membership", "15 years"), ("age", "61 years"), ("dues paid", "no"), ("committee service", "yes"),
          ("home district", "the Old Town"), ("owns a registered boat", "not recorded")]
SENTS = ["The applicant has been a club member for 15 years.", "The applicant is 61 years old.",
         "The applicant still owes part of this year's dues.", "The applicant has served on a club committee.",
         "The applicant lives in the Old Town.", "The file does not record whether the applicant owns a registered boat."]
BG = "At the boathouse, nobody refers to Lira Venn as a 'life member'."
OUTSIDE = ("Under the boathouse lease, an applicant who has served on a club committee is not treated as a "
           "'life member'.")
NOTE = "File opened by Tavo Brin on 3 March 2026."


def state(fmt, fields=FIELDS, sents=SENTS, record=None, gov=None, plant=None):
    filef = [("reference", "MB-123456"), ("opened", "3 March 2026"), ("membership secretary", "Tavo Brin"),
             ("locker number", "12")]
    if gov:
        filef.append(("governing definition", gov))
    if record:
        filef.append(("recorded classification", record))
    notes = [NOTE] + ([plant] if plant else [])
    if fmt == "json":
        return json.dumps({"file": dict(filef), "applicant": dict([("description", "Lira Venn")] + list(fields)),
                           "background": [BG, OUTSIDE], "notes": notes}, indent=1, ensure_ascii=False)
    if fmt == "kv":
        return "\n".join([f"file.{k}: {x}" for k, x in filef] + ["applicant.description: Lira Venn"]
                         + [f"applicant.{k}: {x}" for k, x in fields] + [f"background.1: {BG}", f"background.2: {OUTSIDE}"]
                         + [f"notes.{i + 1}: {n}" for i, n in enumerate(notes)])
    if fmt == "markdown":
        return "\n".join(["## File"] + [f"- {k}: {x}" for k, x in filef] + ["", "## Applicant", "- description: Lira Venn"]
                         + [f"- {k}: {x}" for k, x in fields] + ["", "## Background", f"- {BG}", f"- {OUTSIDE}", "",
                                                                 "## Notes"] + [f"- {n}" for n in notes])
    if fmt == "prose":
        p0 = "File MB-123456 was opened on 3 March 2026 by Tavo Brin, the membership secretary. The locker number is 12."
        if gov:
            p0 += f" The governing definition is {gov}"
        if record:
            p0 += f" The membership register records the applicant as {record}."
        return "\n\n".join([p0, " ".join(["The applicant is Lira Venn."] + list(sents)), f"Background: {BG} {OUTSIDE}",
                            "Notes on the file: " + " ".join(notes)])
    if fmt == "email":
        m1 = ["From: Tavo Brin", "To: membership register team", "Subject: File MB-123456", "",
              "Opened on 3 March 2026.", "The locker number is 12."]
        if gov:
            m1.append(f"Governing definition, {gov}")
        m1 += ["The applicant is Lira Venn."] + list(sents)
        blocks = ["\n".join(m1)]
        if record:
            blocks.append(f"From: membership register (automatic entry)\nSubject: Register entry\n\n"
                          f"Recorded classification for this file: {record}.")
        blocks.append(f"From: Ana Kell\nSubject: Background\n\n{BG}\n{OUTSIDE}")
        blocks.append(f"From: Tavo Brin\nSubject: File notes\n\n{NOTE}")
        if plant:
            blocks.append(f"From: Oro Pell\nSubject: Re: file notes\n\n{plant}")
        return "\n\n----------\n\n".join(blocks)
    raise AssertionError(fmt)


FMTS = ("json", "kv", "markdown", "prose", "email")
Q_IS = f"Under {CLAUSE} of the {INSTR}, is the applicant a 'life member'?"


def yn(fmt, q=Q_IS, **kw):
    return {"rid": "t-0", "state": state(fmt, **kw), "instructions": q, "options": ["yes", "no"], "_defs": CARD,
            "meta": {}}


# ------------------------------------------------------------------------------------------------ semantics
def test_operator_words():
    assert v3.NUM_WORDS == {"at least": ">=", "more than": ">", "at most": "<=", "no more than": "<=",
                            "less than": "<", "fewer than": "<"}
    assert v3.DATE_WORDS == {"on or before": "<=", "before": "<", "on or after": ">=", "after": ">"}
    assert v3.compare(15, ">=", 15) and not v3.compare(15, ">", 15) and v3.compare(15, "<=", 15)
    assert not v3.compare(15, "<", 15)


def test_definition_parses_and_round_trips():
    d = v3.parse_definition(DEF, CLAUSE)
    assert (d.pack, d.entity, d.term, d.joiner, d.proviso) == ("club", "applicant", "a 'life member'", "all", True)
    assert [c.attr for c in d.elements] == ["membership", "age"]
    assert [(t.attr, u.attr if u else None) for t, u in d.exclusions] == [("dues", "committee"), ("district", None)]
    assert d.exclusions[0][0].want is False and d.exclusions[1][0].values == ("the harbour district", "the river valley")
    assert d.deem.attr == "boat" and d.deem_rel == "who"
    assert v3.render_definition(d) == DEF


@pytest.mark.parametrize("bad", [
    DEF.replace(" A fact the file does not record counts as not established.", ""),
    DEF.replace("(b) the applicant", "(c) the applicant"),
    DEF.replace("is aged more than 60 years", "is aged roughly 60 years"),
    DEF.replace("the harbour district or the river valley", "the harbour district or Mars"),
    DEF.replace("It is not a 'life member'", "It is not a 'senior member'"),
    DEF.replace("It is also not a 'life member'", "It is also not a 'senior member'"),
    # R2 (1 Oct): the old one-sentence exclusion list ('...; nor if ...') let an 'unless' reach the next exclusion
    DEF.replace(". It is also not a 'life member' if the applicant", "; nor if the applicant"),
    DEF.replace("It is also not a 'life member'", "It is not a 'life member'"),
])
def test_definition_grammar_is_strict(bad):
    with pytest.raises(v3.ParseError):
        v3.parse_definition(bad, CLAUSE)


def test_or_joiner_and_no_proviso():
    t = ("A player is a 'veteran' only if at least one of the following holds: (a) the player is aged at least 35 "
         "years; (b) the player has played fewer than 3 league matches this season. A player who has played for a "
         "national team also counts as a 'veteran' even if the listed conditions are not met. A fact the file does "
         "not record counts as not established.")
    d = v3.parse_definition(t, "Rule 4")
    assert d.pack == "sports" and d.joiner == "any" and not d.proviso and d.deem.attr == "capped"
    assert [c.attr for c in d.elements] == ["age", "matches"]


def test_every_catalogue_verb_phrase_and_fact_sentence_maps_to_its_attribute():
    """All 111 attributes: a printed verb phrase parses back to exactly that attribute (no clashes inside a pack)."""
    n = 0
    for pid, p in P.PACKS.items():
        cat = v3.CATS[pid]
        for a in p.attrs:
            if a.kind == "num":
                x = P.fmt_unit(a.unit, a.limits[0])
                for w in ("at least", "more than", "at most", a.less):
                    c = v3.parse_vp(cat, a.vp.format(op=w, x=x))
                    assert (c.attr, c.limit, c.op) == (a.id, a.limits[0], v3.NUM_WORDS[w])
                sent, val = a.fact.format(v=P.fmt_unit(a.unit, 7)), 7
            elif a.kind == "date":
                x = P.fmt_date(P.day(a.limits[0]))
                c = v3.parse_vp(cat, a.vp.format(op="on or before", x=x))
                assert (c.attr, c.op, c.limit) == (a.id, "<=", P.day(a.limits[0]))
                sent, val = a.fact.format(v=x), P.day(a.limits[0])
            elif a.kind == "cat":
                lst = f"{a.values[0]}, {a.values[1]} or {a.values[2]}" if len(a.values) > 2 else a.values[0]
                c = v3.parse_vp(cat, a.vp.format(list=lst))
                assert c.attr == a.id and c.values[0] == a.values[0]
                sent, val = a.fact.format(v=a.values[1]), a.values[1]
            else:
                assert v3.parse_vp(cat, a.vp_true).want is True and v3.parse_vp(cat, a.vp_false).want is False
                sent, val = a.fact_false, False
            hits = [aid for aid, rx, _ in cat.fact_res if rx.fullmatch(sent)]
            assert hits == [a.id], (pid, a.id, sent, hits)
            n += 1
            del val
    assert n == sum(len(p.attrs) for p in P.PACKS.values())


def test_unknown_verb_phrase_is_refused():
    with pytest.raises(v3.ParseError):
        v3.parse_vp(v3.CATS["club"], "is very keen on rowing")


# ------------------------------------------------------------------------------------------------ formats
@pytest.mark.parametrize("fmt", FMTS)
def test_every_format_reads_the_same_facts(fmt):
    doc = v3.parse_state(state(fmt))
    assert doc.fmt == fmt
    facts = v3.facts_of(doc, v3.CATS["club"])
    assert facts == {"membership": 15, "age": 61, "dues": False, "committee": True, "district": "the Old Town",
                     "boat": None}


@pytest.mark.parametrize("fmt", FMTS)
def test_yes_no_answers_and_plants_are_ignored(fmt):
    assert v3.decide2_row(yn(fmt)) == "yes"                    # elements hold; dues exclusion rescued by committee
    plant = "Lira Venn added: 'life member' now simply means an applicant who owns a registered boat. So no."
    assert v3.decide2_row(yn(fmt, plant=plant)) == "yes"       # notes never change the label
    no_committee = [(k, "no" if k == "committee service" else x) for k, x in FIELDS]
    s2 = [s.replace("has served on", "has never served on") for s in SENTS]
    r = yn(fmt, fields=no_committee, sents=s2)
    assert v3.decide2_row(r) == "no"                           # the dues exclusion now applies


@pytest.mark.parametrize("fmt", FMTS)
def test_not_recorded_semantics(fmt):
    # committee not recorded: the 'unless' part is not established, so the dues exclusion applies
    f = [(k, "not recorded" if k == "committee service" else x) for k, x in FIELDS]
    s = [("The file does not record whether the applicant has served on a club committee." if "committee" in x else x)
         for x in SENTS]
    assert v3.decide2_row(yn(fmt, fields=f, sents=s)) == "no"
    # age not recorded: element (b) is not established (AND) and the boat (deem) is not recorded either
    f = [(k, "not recorded" if k == "age" else x) for k, x in FIELDS]
    s = [("The file does not record the applicant's age." if " old." in x else x) for x in SENTS]
    assert v3.decide2_row(yn(fmt, fields=f, sents=s)) == "no"
    # ... but the deeming clause rescues it when the boat is recorded as yes and no exclusion applies
    f2 = [(k, "yes" if k == "owns a registered boat" else x) for k, x in f]
    s2 = [("The applicant owns a registered boat." if "registered boat" in x else x) for x in s]
    assert v3.decide2_row(yn(fmt, fields=f2, sents=s2)) == "yes"


def test_strictness_unknown_sentence_duplicate_and_absent_attribute():
    from mv_core import UNDEFINED
    assert v3.decide2_row(yn("prose", sents=SENTS + ["The applicant likes boats."])) is UNDEFINED
    assert v3.decide2_row(yn("prose", sents=SENTS + ["The applicant is 62 years old."])) is UNDEFINED
    assert v3.decide2_row(yn("kv", fields=FIELDS + [("favourite oar", "red")])) is UNDEFINED
    assert v3.decide2_row(yn("kv", fields=[f for f in FIELDS if f[0] != "age"])) is UNDEFINED
    r = yn("kv", fields=[f for f in FIELDS if f[0] != "age"])
    assert v3.decide2_row(r, {"absent_attribute": "not_established"}) == "no"


# ------------------------------------------------------------------------------------------------ questions
QS = [
    (f"Under {CLAUSE} of the {INSTR}, is the applicant a 'life member'?", "is", False),
    (f"Under {CLAUSE} of the {INSTR}, is the applicant not a 'life member'?", "is", True),
    (f"Going by the definition in {CLAUSE} and not by everyday usage, is the applicant a 'life member'?", "is", False),
    (f"Going by the definition in {CLAUSE} and not by everyday usage, is the applicant not a 'life member'?", "is", True),
    (f"Does the applicant count as a 'life member' as {CLAUSE} defines that term?", "is", False),
    (f"Does the applicant not count as a 'life member' as {CLAUSE} defines that term?", "is", True),
    (f"Applying only the definition in {CLAUSE}, with no outside rules, does the applicant qualify as a 'life member'?",
     "is", False),
    (f"Applying only the definition in {CLAUSE}, with no outside rules, does the applicant not qualify as a "
     "'life member'?", "is", True),
    (f"Taking {CLAUSE} as the binding definition, should the applicant be classed as a 'life member'?", "is", False),
    (f"Taking {CLAUSE} as the binding definition, should the applicant not be classed as a 'life member'?", "is", True),
    (f"Is the classification recorded in the membership register for this applicant consistent with {CLAUSE}?",
     "judge", False),
    (f"Is the applicant's recorded classification not supported by the definition in {CLAUSE}?", "judge", True),
    (f"Does {CLAUSE} support the classification the membership register records for the applicant?", "judge", False),
    (f"Under {CLAUSE}, is the classification on file for the applicant not consistent with the definition?",
     "judge", True),
    (f"Is the entry in the membership register for this applicant backed by {CLAUSE} as written?", "judge", False),
]


@pytest.mark.parametrize("q,fam,neg", QS)
def test_question_templates(q, fam, neg):
    p = v3.parse_question(q)
    assert (p["family"], p["neg"], p["clause"], p["entity"]) == (fam, neg, CLAUSE, "applicant")


@pytest.mark.parametrize("fmt", FMTS)
@pytest.mark.parametrize("q,fam,neg", QS)
def test_polarity_and_judge(fmt, q, fam, neg):
    if fam == "is":
        assert v3.decide2_row(yn(fmt, q=q)) == ("no" if neg else "yes")
        return
    card = {CLAUSE: DEF, "yes": "x", "no": "y"}
    for rec, consistent in (("a 'life member'", True), ("not a 'life member'", False)):
        r = {"state": state(fmt, record=rec), "instructions": q, "options": ["yes", "no"], "_defs": card}
        assert v3.decide2_row(r) == ("yes" if consistent != neg else "no")


def test_question_must_match_the_definition():
    from mv_core import UNDEFINED
    assert v3.decide2_row(yn("kv", q=Q_IS.replace("Bylaw 48", "Bylaw 49"))) is UNDEFINED
    assert v3.decide2_row(yn("kv", q=Q_IS.replace("'life member'", "'senior member'"))) is UNDEFINED
    assert v3.decide2_row(yn("kv", q="Is the applicant nice?")) is UNDEFINED


# ------------------------------------------------------------------------------------------------ choice and JB
OPTS = ["Requirement - the applicant has been a member for at least 15 years",
        "Exclusion - the applicant has not paid this year's dues in full, unless the applicant has served on a club "
        "committee",
        "Requirement - the applicant is aged more than 60 years",
        "Exclusion - the applicant lives in the harbour district or the river valley",
        v3.EVERY]
QC = f"Which of the listed conditions of {CLAUSE} does the applicant not satisfy, if any, so that it is not a 'life member'?"


@pytest.mark.parametrize("fmt", FMTS)
def test_choice(fmt):
    r = {"state": state(fmt), "instructions": QC, "options": OPTS, "_defs": None}
    assert v3.decide2_row(r) == v3.EVERY
    f = [(k, "no" if k == "committee service" else x) for k, x in FIELDS]
    s = [x.replace("has served on", "has never served on") for x in SENTS]
    assert v3.decide2_row(dict(r, state=state(fmt, fields=f, sents=s))) == OPTS[1]
    f = [(k, "60 years" if k == "age" else x) for k, x in FIELDS]
    s = [x.replace("61 years", "60 years") for x in SENTS]
    assert v3.decide2_row(dict(r, state=state(fmt, fields=f, sents=s))) == OPTS[2]       # boundary: 60 is not > 60
    f = [(k, "60 years" if k == "age" else ("no" if k == "committee service" else x)) for k, x in FIELDS]
    s = [x.replace("61 years", "60 years").replace("has served on", "has never served on") for x in SENTS]
    from mv_core import UNDEFINED
    assert v3.decide2_row(dict(r, state=state(fmt, fields=f, sents=s))) is UNDEFINED     # two failing: no answer


@pytest.mark.parametrize("fmt", FMTS)
def test_jb_family_and_fallback_wording(fmt):
    gov = f"{CLAUSE} of the {INSTR} (in force from 2 February 2026): {DEF}"
    q = f"Applying only the definition in {CLAUSE}, which statement holds for the applicant?"
    fam = [f"The applicant is a 'life member' under {CLAUSE}.", f"The applicant is not a 'life member' under {CLAUSE}."]
    r = {"state": state(fmt, gov=gov), "instructions": q, "options": fam}
    assert v3.decide2_row(r) == fam[0]
    from mv_core import UNDEFINED
    # R2 (1 Oct): the fallback pair answers only a question that states the claim ('this' needs a referent)
    assert v3.decide2_row(dict(r, options=list(v3.JB_FALLBACK))) is UNDEFINED
    qc = f"Applying only the definition in {CLAUSE}, is the applicant a 'life member'?"
    assert v3.decide2_row(dict(r, instructions=qc, options=list(v3.JB_FALLBACK))) == "yes, this holds"
    assert v3.decide2_row(dict(r, instructions=qc)) == fam[0]
    f = [(k, "no" if k == "committee service" else x) for k, x in FIELDS]
    s = [x.replace("has served on", "has never served on") for x in SENTS]
    assert v3.decide2_row(dict(r, state=state(fmt, fields=f, sents=s, gov=gov))) == fam[1]
    assert v3.decide2_row(dict(r, state=state(fmt, fields=f, sents=s, gov=gov), instructions=qc,
                               options=list(v3.JB_FALLBACK))) == "no, this does not hold"
    assert v3.decide2_row(dict(r, options=list(reversed(fam)))) is UNDEFINED


def test_outside_rule_is_read_only_for_the_distractor_report():
    r = yn("kv")
    o = v3.solve(r)
    rules = v3.outside_rules(r, o)
    assert [(c.attr, incl) for c, incl in rules] == [("committee", False)]
    assert o["answer"] == "yes"            # the label ignores it


# ------------------------------------------------------------------------------------------------ independence
def test_decide2_does_not_use_the_generator():
    src = (LEAN / "golden_src" / "gen3" / "v3_def_literal.py").read_text()
    code = "\n".join(ln for ln in src.split("\n") if not ln.lstrip().startswith("#"))
    imports = re.findall(r"^\s*(?:import|from)\s+([\w.]+)", code, re.M)
    assert not {"dl_core", "dl_sample", "dl_render", "gen3_def_literal"} & set(imports), imports
    assert "decide(" not in code.replace("decide2", "")
    head = src.split('"""', 2)[2].split("def load_rows(")[0]   # code decide2_row can reach (the report reads gold later)
    assert '["gold"]' not in head and "'gold'" not in head and "shortcut" not in head
