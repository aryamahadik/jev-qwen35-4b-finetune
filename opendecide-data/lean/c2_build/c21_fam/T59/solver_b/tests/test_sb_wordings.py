"""Every wording variant of the T59 wording pool (pools/wording_pool_v1.json) is parsed by solver B (card clauses, user turns, planned step,
options). The pool is READ here only as a list of template strings; no generator code is imported."""
import json
import os

import pytest

import sb_fixtures as F
from solver_b import hook, parse

POOL = os.path.join(F.FAM_T59, "pools", "wording_pool_v1.json")
pytestmark = pytest.mark.skipif(not os.path.isfile(POOL), reason="wording pool not found")


def pool():
    with open(POOL) as fh:
        return json.load(fh)


ACTIONS = ["delete", "remove", "archive", "cancel", "send", "export", "move", "reserve", "schedule", "set the status of", "rename", "create",
           "add", "update", "get", "list", "lock", "restore"]


def fill(tpl, **kw):
    return tpl.format(**kw)


def facts():
    return parse.Facts()


def test_card_clauses_every_variant():
    p = pool()
    for t in p["clause.title"]:
        f = facts()
        assert parse._card_line(f, fill(t, title="nultit_vuzemon")) and f.card["title"] == "nultit_vuzemon"
    for t in p["clause.undo_proceed"]:
        f = facts()
        assert parse._card_line(f, t) and f.card["mode"] == "ON"
    for t in p["clause.ask_on_ambiguity"]:
        f = facts()
        assert parse._card_line(f, t) and f.card["mode"] == "OFF"
    for t in p["clause.stakes_threshold"]:
        f = facts()
        assert parse._card_line(f, fill(t, h=20, unit_pl="beboskets")) and f.card["H"] == 20 and f.card["unit"] == "beboskets"
    for t in p["clause.defaults_on"]:
        f = facts()
        assert parse._card_line(f, t) and f.card["defaults"] is True
    for t in p["clause.defaults_off"]:
        f = facts()
        assert parse._card_line(f, t) and f.card["defaults"] is False
    for t in p["clause.read_on"]:
        f = facts()
        assert parse._card_line(f, t) and f.card["read_first"] is True
    for t in p["clause.read_off"]:
        f = facts()
        assert parse._card_line(f, t) and f.card["read_first"] is False
    for t in p["clause.retry_cap"]:
        for n in (2, 3):
            f = facts()
            assert parse._card_line(f, fill(t, cap=n)) and f.card["retry"] == n
    srcs = ["the user's message", "the tool result", "the project notes"]
    keys = {"the user's message": "user", "the tool result": "tool", "the project notes": "notes"}
    for t in p["clause.precedence"]:
        for w in srcs:
            for l in srcs:
                if w == l:
                    continue
                f = facts()
                assert parse._card_line(f, fill(t, win=w, lose=l)) and f.card["prec"] == (keys[w], keys[l])
    for t in p["clause.precedence_cap"]:
        for w in ("amount", "cap"):
            f = facts()
            assert parse._card_line(f, fill(t, win=w)) and f.card["prec_cap"] == w


def test_requests_every_variant_and_alarm():
    p = pool()
    alarms = [""] + [a + " " for a in p["req.alarm"]]
    for al in alarms:
        for act in ACTIONS:
            cap = act[:1].upper() + act[1:]
            for t in p["req.act"]:
                for hold in ("", fill(p["req.ref_hold"][0], size=7, unit_pl="refodins"), fill(p["req.ref_hold"][1], size=7, unit_pl="refodins")):
                    r = parse._user_request(facts(), al + fill(t, action=act, action_cap=cap, entity="fupalu", ref="fup-457", hold=hold))
                    assert r and r["form"] == "plain" and r["verb"] == act and r["noun"] == "fupalu" and r["ref"] == "fup-457", (t, act)
                    if hold:
                        assert r["size"] == 7
            for t in p["req.act_q"]:
                r = parse._user_request(facts(), al + fill(t, action=act, action_cap=cap, entity="satkefa", q="kabeva"))
                assert r and r["form"] == "for" and r["verb"] == act and r["q"] == "kabeva" and r["noun"] == "satkefa", (t, act)
            for t in p["req.act_field"]:
                r = parse._user_request(facts(), al + fill(t, action=act, action_cap=cap, entity="rakalo", field="gafevul", q="fotuza"))
                assert r and r["form"] == "field" and r["verb"] == act and r["field"] == "gafevul" and r["q"] == "fotuza", (t, act)
            for t in p["req.cap"]:
                r = parse._user_request(facts(), al + fill(t, action=act, action_cap=cap, amount=7, unit_pl="fanditis", entity="kotzatmut", ref="kot-1829"))
                assert r and r["form"] == "cap" and r["verb"] == act and r["amount"] == 7 and r["ref"] == "kot-1829", (t, act)
            for t in p["req.fact"]:
                r = parse._user_request(facts(), al + fill(t, action=act, action_cap=cap, entity="dotolki", ref="dot-5048", value="fesobu"))
                assert r and r["form"] == "fact" and r["verb"] == act and r["value"] == "fesobu", (t, act)
            for t in p["req.fact_ask"]:
                r = parse._user_request(facts(), al + fill(t, action=act, action_cap=cap, entity="dotolki", ref="dot-5048", fact="name"))
                assert r and r["form"] == "fact_ask" and r["verb"] == act and r["fact"] == "name", (t, act)


def test_user_lines_every_variant():
    p = pool()
    for t in p["req.value"]:
        f = facts()
        parse._user_line(f, fill(t, role="status", value="sigma"), False)
        assert f.values == {"status": "sigma"}
        f = facts()
        parse._user_line(f, fill(t, role="when", value="2026-12-06"), False)
        assert f.values == {"when": "2026-12-06"}
    for t in p["req.cands"]:
        f = facts()
        parse._user_line(f, fill(t, role="name", list="a, b, c"), False)
        assert f.cands == {"name": ["a", "b", "c"]} and not f.values
    for t in p["req.delegation"]:
        for role in ("name", "choice of file", "choice of rasufi", "priority"):
            f = facts()
            parse._user_line(f, fill(t, role=role), False)
            assert f.deleg == [role]
    for t in p["req.qualifier"]:
        f = facts()
        parse._user_line(f, fill(t, field="pelgossot", q="kabeva"), False)
        assert f.qual == ("one", "pelgossot", "kabeva")
    for t in p["req.qualifier_both"]:
        f = facts()
        parse._user_line(f, fill(t, fa="pelgossot", fb="solpismat", q="kabeva"), False)
        assert f.qual == ("both", "pelgossot", "solpismat", "kabeva")
    for t in p["req.expect"]:
        f = facts()
        parse._user_line(f, fill(t, entity="rakalo"), False)
        assert f.expect
    for t in p["req.prereq"]:
        f = facts()
        parse._user_line(f, fill(t, parent="gevomu", pid="gev-4051"), False)
        assert f.prereq is not None and f.prereq[:2] == ("lock", "gevomu") and not f.unknown_user
    for t in p["req.cap_stmt"] + p["req.cap2_stmt"]:
        f = facts()
        parse._user_line(f, fill(t, unit="fanditi", price=3, cap=18), False)
        assert f.cap and f.cap["price"] == 3 and f.cap["cap"] == 18
    for t in p["req.fact_note"]:
        f = facts()
        parse._user_line(f, fill(t, fact="name", value="dopeze"), False)
        assert f.notes == [("name", "dopeze")]
    for t in p["req.list_intro"]:
        f = facts()
        parse._user_line(f, t, False)
        assert not f.unknown_user
    f = facts()
    parse._user_line(f, "It holds 12 posirgas.", False)
    assert f.size == 12
    f = facts()
    parse._user_line(f, "The archive directory /work/keza-domo/archive has to be created first.", False)
    assert f.prereq == ("mkdir", "/work/keza-domo/archive")


def test_planned_lines_and_options():
    p = pool()
    for t in p["planned"]:
        ctx = "\n".join(F.card("ON") + ["Tools:", "Conversation:", "User: Please remove the satkefa sat-1813.", fill(t, call='remove_satkefa(satkefa_id="sat-1813")')])
        f = parse.parse_context(ctx)
        assert f.planned and f.planned.name == "remove_satkefa" and f.planned.args == {"satkefa_id": "sat-1813"}, t
    for t in p["opt.ASK"]:
        assert parse.classify_option(t) == "ASK", t
    for t in p["opt.PROCEED"]:
        assert parse.classify_option(t) == "PROCEED", t
    # the letters come from the TEXT of the options, whichever order they are printed in
    for a in p["opt.ASK"][::7]:
        for b in p["opt.PROCEED"][::9]:
            assert parse.parse_options("A) %s\nB) %s" % (a, b)) == {"ASK": "A", "PROCEED": "B"}
            assert parse.parse_options("A) %s\nB) %s" % (b, a)) == {"PROCEED": "A", "ASK": "B"}


def test_unclassifiable_options_abstain():
    assert parse.parse_options("A) Do something\nB) Do something else") is None
    assert parse.parse_options("A) Carry on without asking\nB) Go ahead without asking") is None
    assert parse.parse_options("A) Stop and ask the user first\nB) Pause and ask the person first") is None


def test_question_text_is_irrelevant():
    p = pool()
    noun = "fupalu"
    ts = [F.op_tool("rename", noun, [("name", "str", False, None)]), F.read_tool("list", noun)] + F.filler()
    base = F.build(F.card("OFF"), ts, ["Please rename the fupalu fup-457.", "It holds 7 refodins.", "Options for the name: a, b."], [],
                   'Planned next step: rename_fupalu(fupalu_id="fup-457", name="a")')
    want = hook.solver_b(base)
    assert want.label == "ASK"
    for q in p["q.mid"][::10] + p["q.early"][::10]:
        v = dict(base)
        v["rendered"] = dict(base["rendered"], question="Question: " + q, text=base["rendered"]["context"] + "\n\nQuestion: " + q + "\n" + base["rendered"]["options_text"])
        assert hook.solver_b(v).label == want.label
