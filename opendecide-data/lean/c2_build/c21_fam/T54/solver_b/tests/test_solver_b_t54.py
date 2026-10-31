"""CPU tests for T54 solver B. Hand-built records only (no generator) for the rule tables, plus an import-graph test and a
gold-blindness test. The generator-driven agreement test is at the bottom and is skipped if the generator cannot be imported."""
import ast
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SB = os.path.dirname(HERE)
FAM = os.path.dirname(SB)
ROOT = os.path.dirname(FAM)
for p in (SB, ROOT, FAM):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest  # noqa: E402

import t54_solver_b as sb  # noqa: E402
import t54_render_b as rb  # noqa: E402

STDLIB_OK = {"copy", "re", "collections", "hashlib", "json", "os", "sys"}


# ------------------------------------------------------------------------------------------- independence / blindness
@pytest.mark.parametrize("fname", ["t54_solver_b.py", "t54_render_b.py"])
def test_solverB_independent_import_graph(fname):
    tree = ast.parse(open(os.path.join(SB, fname)).read())
    mods = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            mods |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom):
            mods.add((n.module or "").split(".")[0])
    assert mods <= STDLIB_OK, mods
    src = open(os.path.join(SB, fname)).read()
    for banned in ("t54_solver_a", "tool_engine", "t54_generator", "t54_gates"):
        assert banned not in src.replace('"' + banned + '"', ""), banned


def _tool(tid, verb, ent, params, rw="read", idem=True, group=None):
    return dict(tid=tid, verb=verb, entity=ent, name="%s_%s" % (verb, ent), rw=rw, idempotent=idem,
                group=group or "g:%s:%s" % (verb, ent), desc="x",
                params=[dict(name=n, role=None, required=r, type="str", default=d) for (n, r, d) in params])


def _arg(param, src, value="v1", required=True, default=None):
    return dict(param=param, required=required, role=None, type="str", default=default, value=value, source=src)


def _s1(tools, args, cards=("card.t54.strict_ask",), typ="tool", group="g:get:aa", extra=None):
    r = dict(sub_block="s1_need4", cards=list(cards), card=cards[0], facts=[], tools=tools,
             options=[dict(label=l, letter=c, text="t") for l, c in zip(("CALL", "ASK", "NO_TOOL", "ANSWER"), "ABCD")],
             intent=dict(type=typ, target_group=group, entity="aa", verb="get", args=args), rendered=dict(text=""),
             gold="CALL", gold_letter="A")
    if extra:
        r.update(extra)
    return r


def test_solve_ignores_stored_gold():
    t = [_tool("t0", "get", "aa", [("aa_id", True, None)])]
    r = _s1(t, [_arg("aa_id", "user_turn")])
    r2 = copy.deepcopy(r)
    r2["gold"] = "ASK"
    r2["gold_letter"] = "B"
    assert sb.solve(r).label == sb.solve(r2).label == "CALL"
    v = sb.strip_gold(r)
    assert "gold" not in v and "gold_letter" not in v


# ------------------------------------------------------------------------------------------------------------------ S1
def test_s1_rule_order_and_cards():
    t = [_tool("t0", "get", "aa", [("aa_id", True, None), ("n", True, "dflt")])]
    # all sourced -> CALL
    assert sb.solve(_s1(t, [_arg("aa_id", "user_turn"), _arg("n", "user_turn")])).label == "CALL"
    # n has no source: strict card ignores the default -> ASK; defaults_ok accepts it -> CALL
    a = [_arg("aa_id", "user_turn"), _arg("n", "none", default="dflt")]
    assert sb.solve(_s1(t, a)).label == "ASK"
    assert sb.solve(_s1(t, a, cards=("card.t54.defaults_ok",))).label == "CALL"
    # no default and no source: ASK even under defaults_ok
    t2 = [_tool("t0", "get", "aa", [("aa_id", True, None), ("n", True, None)])]
    a2 = [_arg("aa_id", "user_turn"), _arg("n", "none")]
    assert sb.solve(_s1(t2, a2, cards=("card.t54.defaults_ok",))).label == "ASK"
    # tool absent -> NO_TOOL beats ASK
    assert sb.solve(_s1([_tool("t9", "get", "bb", [("bb_id", True, None)], group="g:get:bb")], a2)).label == "NO_TOOL"


def test_s1_equivalence_group_counts_as_present():
    t = [_tool("t0", "read", "aa", [("aa_id", True, None)], group="g:get:aa")]
    assert sb.solve(_s1(t, [_arg("aa_id", "user_turn")], group="g:get:aa")).label == "CALL"


def test_s1_answer_needs_a_located_span():
    fact = dict(fact_id="f1", where="context", entity="aa", field="f", value="zz-77", ref="aa-1")
    r = _s1([], [], typ="info", extra=dict(facts=[fact], rendered=dict(text="... zz-77 ...")))
    r["intent"]["answer"] = dict(fact_id="f1", where="context", value="zz-77")
    assert sb.solve(r).label == "ANSWER"
    r["rendered"] = dict(text="no value here")                 # span not in the rendered context
    res = sb.solve(r)
    assert res.label is None and res.abstain == "answer_span_unlocatable"
    r["rendered"] = dict(text="zz-77")
    r["intent"]["answer"]["fact_id"] = "f9"                    # pointer to a fact that is not in the record
    assert sb.solve(r).label is None


# ------------------------------------------------------------------------------------------------------------------ S3
def _s3(tools, args, calls=(), cards=("card.t54.strict_ask",), group="g:get:aa"):
    r = _s1(tools, args, cards=cards, group=group)
    r["sub_block"] = "s3_limit"
    r["calls"] = list(calls)
    r["options"] = [dict(label=l, letter=c, text="t") for l, c in zip(("CALL", "ASK", "NO_TOOL", "RESULT_MISSING"), "ABCD")]
    return r


def test_s3_branches():
    t = [_tool("t0", "get", "aa", [("aa_id", True, None), ("k", True, None)])]
    call_ok = dict(tool="x", tid="tr", args=[], out=[["k", "1"]], supplies="k")
    call_missing = dict(tool="x", tid="tr", args=[], out=None, supplies="k")
    assert sb.solve(_s3(t, [_arg("aa_id", "user_turn"), _arg("k", "prior_tool_output")], [call_ok])).label == "CALL"
    assert sb.solve(_s3(t, [_arg("aa_id", "user_turn"), _arg("k", "missing_result")], [call_missing])).label == "RESULT_MISSING"
    # the output is absent on the call although the source label says it was found: second signal wins, flagged
    res = sb.solve(_s3(t, [_arg("aa_id", "user_turn"), _arg("k", "prior_tool_output")], [call_missing]))
    assert res.label == "RESULT_MISSING" and "source_says_output_but_call_has_none" in res.flags
    assert sb.solve(_s3(t, [_arg("aa_id", "user_turn"), _arg("k", "none")], [])).label == "ASK"
    assert sb.solve(_s3([], [_arg("aa_id", "user_turn")])).label == "NO_TOOL"


# ------------------------------------------------------------------------------------------------------------------ S4
def _s4(state, write_idem, readers, args=None, read_out=None):
    w = _tool("t0", "close", "aa", [("aa_id", True, None)], rw="write", idem=write_idem, group="g:close:aa")
    tools = [w] + ([_tool("tr", "get", "aa", [("aa_id", True, None)])] if readers else [])
    r = _s1(tools, args or [_arg("aa_id", "user_turn")], cards=("card.t54.strict_ask", "card.t54.read_before_write"),
            group="g:close:aa")
    r["sub_block"] = "s4_precond"
    r["fact"] = dict(id="f1", state=state, entity="aa", done_word="closed", other_word="open")
    r["calls"] = [dict(tool="get_aa", tid="tr", args=[], out=read_out, fact_call=True)] if read_out else []
    r["options"] = [dict(label=l, letter=c, text="t") for l, c in zip(("WRITE", "READ_FIRST", "DONE_NO_CALL", "ASK"), "ABCD")]
    return r


def test_s4_table():
    assert sb.solve(_s4("observed_true", False, True, read_out=[["state", "closed"]])).label == "DONE_NO_CALL"
    assert sb.solve(_s4("observed_false", False, True, read_out=[["state", "open"]])).label == "WRITE"
    assert sb.solve(_s4("observed_false", False, True, [_arg("aa_id", "none")], read_out=[["state", "open"]])).label == "ASK"
    assert sb.solve(_s4("unobserved", True, False)).label == "WRITE"
    assert sb.solve(_s4("unobserved", False, True)).label == "READ_FIRST"
    assert sb.solve(_s4("unobserved", False, False)).label == "ASK"
    res = sb.solve(_s4("observed_true", False, True, read_out=[["state", "open"]]))
    assert "fact_state_vs_read_output_mismatch" in res.flags


# ------------------------------------------------------------------------------------------------------------------ S5
def _s5(prov_args, cards=("card.t54.strict_ask",), declared=()):
    args = []
    for (kind, extra, ctx) in prov_args:
        prov = dict(kind=kind)
        prov.update(extra)
        args.append(dict(param="p", required=True, type="str", value="v", role=None, prov=prov, src_value="v", ctx=ctx))
    return dict(sub_block="s5_argground", cards=list(cards), card=cards[0], declared_conversions=list(declared), call=dict(args=args),
                options=[dict(label="GROUNDED", letter="A", text="t"), dict(label="UNGROUNDED", letter="B", text="t")], facts=[])


def test_s5_table():
    assert sb.solve(_s5([("user_turn", {}, "user"), ("prior_output_same_role", {}, "output")])).label == "GROUNDED"
    assert sb.solve(_s5([("user_turn", {}, "user"), ("none", {}, "user")])).label == "UNGROUNDED"
    assert sb.solve(_s5([("wrong_role", {}, "output_wrong")])).label == "UNGROUNDED"
    # a card default is grounded only when the card allows defaults
    assert sb.solve(_s5([("card_default", {}, "default")], cards=("card.t54.defaults_ok",))).label == "GROUNDED"
    assert sb.solve(_s5([("card_default", {}, "default")])).label == "UNGROUNDED"
    # a unit conversion counts only when the card declares it
    tr = ("transform", dict(base="user_turn", transform="kg_to_g"), "user")
    assert sb.solve(_s5([tr], declared=("kg_to_g",))).label == "GROUNDED"
    assert sb.solve(_s5([tr])).label == "UNGROUNDED"
    assert sb.solve(_s5([("transform", dict(base="user_turn", transform="case"), "user")])).label == "GROUNDED"


# ------------------------------------------------------------------------------------------------------------------ S6
def test_s6_longest_path_levels():
    d = dict(nodes=["a", "b", "c", "d"], edges=[["a", "b"], ["b", "c"]], done=["a"],
             node_tools=[dict(id=n, tool="t" + n, group="g:" + n, alias=None) for n in "abcd"],
             step_no=dict(a=1, b=2, c=3, d=4),
             args=dict(a=[], b=[dict(param="x", value=None, from_step=1)], c=[dict(param="x", value=None, from_step=2)], d=[]))
    opts = [dict(label="L%d" % i, canon=c) for i, c in enumerate((["g:b", "g:d"], ["g:b"], ["g:b", "g:c", "g:d"], ["g:d", "g:z"]))]
    r = dict(sub_block="s6_parseq", dag=d, s6_options=opts, options=[dict(label=o["label"], letter="ABCD"[i], text="t")
                                                                    for i, o in enumerate(opts)], facts=[])
    res = sb.solve(r)
    assert res.label == "L0" and res.letter == "A" and not res.flags
    # a back-reference chain a->b->c with a not done: only a (and d) are ready
    d["done"] = []
    opts[0]["canon"] = ["g:a", "g:d"]
    assert sb.solve(r).label == "L0"
    # two options equal to the ready set -> abstain, never a guess
    opts[1]["canon"] = ["g:d", "g:a"]
    assert sb.solve(r).label is None


# ------------------------------------------------------------------------------------------------------------------ S2
def test_s2_requires_exactly_one_satisfying_option():
    tools = [_tool("t0", "update", "aa", [("aa_id", True, None), ("f", True, None)], group="g:update:aa"),
             _tool("t1", "set", "aa", [("aa_id", True, None), ("status", True, None)], group="g:update:aa"),
             _tool("t2", "delete", "aa", [("aa_id", True, None)], group="g:remove:aa")]
    opts = [dict(label=t["name"], letter="ABC"[i], text='%s(aa_id="1")' % t["name"]) for i, t in enumerate(tools)]
    r = dict(sub_block="s2_pick", tools=tools, options=opts, facts=[], cards=["card.t54.strict_ask"],
             intent=dict(type="tool", target_group="g:update:aa", entity="aa", verb="update",
                         args=[_arg("aa_id", "user_turn"), _arg("f", "user_turn")]))
    assert sb.solve(r).label == "update_aa"            # the schema (parameter f) tells update from set
    r["intent"]["args"] = [_arg("aa_id", "user_turn")]  # both update_aa and set_aa now cover the request
    assert sb.solve(r).label is None


# ------------------------------------------------------------------------------------------------- generator agreement
def test_agreement_on_in_memory_sample():
    try:
        import t54_generator as gen
    except Exception as e:  # pragma: no cover
        pytest.skip("generator not importable: %s" % e)
    recs = gen.generate_in_memory(total=400, seed="b-test-agree", standin=True)
    bad = [(r["sub_block"], r["gold"]) for r in recs if sb.solve(r).label != r["gold"]]
    assert len(bad) / len(recs) <= 0.01, bad[:5]
    assert all(sb.solve(r).letter == r["gold_letter"] for r in recs)


def test_render_parser_agrees_where_it_decides():
    try:
        import t54_generator as gen
    except Exception as e:  # pragma: no cover
        pytest.skip("generator not importable: %s" % e)
    recs = gen.generate_in_memory(total=300, seed="b-test-render", standin=True)
    dec = dis = 0
    for r in recs:
        if r["sub_block"] == "s1_need4":
            continue  # S1 has the two reported fidelity classes; covered by the harness report
        k, v = rb.solve_text(r["sub_block"], r["rendered"]["text"])
        if k == "letter":
            dec += 1
            dis += int(v != r["gold_letter"])
    assert dec > 150 and dis / dec <= 0.01
