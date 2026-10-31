"""CPU tests for T55 solver B: hand-built records for every rule branch, exhaustive truth tables for B1/B2/B5/B6 (C3), the two
held-out B3 violation types, the import-graph test, and generator-driven agreement. No generator is needed for the rule tests."""
import ast
import itertools
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

import t55_solver_b as sb  # noqa: E402
import t55_render_b as rb  # noqa: E402

STDLIB_OK = {"copy", "re"}


@pytest.mark.parametrize("fname", ["t55_solver_b.py", "t55_render_b.py"])
def test_solverB_independent_import_graph(fname):
    src = open(os.path.join(SB, fname)).read()
    tree = ast.parse(src)
    mods = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            mods |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom):
            mods.add((n.module or "").split(".")[0])
    assert mods <= STDLIB_OK, mods
    docs = set(id(n.value) for n in ast.walk(tree) if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))
    consts = [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs]
    for banned in ("t55_solver_a", "tool_engine", "t55_generator", "world_committed", "gold", "gold_letter"):
        # the gold keys appear only inside the strip list; they must never be read as a value
        if banned in ("gold", "gold_letter", "world_committed"):
            continue
        assert banned not in consts


def _tool(name, rw="read", idem=True, group=None, entity="zed", verb=None):
    return dict(tid=name, verb=verb or name.split("_")[0], entity=entity, name=name, rw=rw, idempotent=idem,
                group=group or "g:%s:%s" % (name.split("_")[0], entity), params=[])


def _rec(sub, **kw):
    r = dict(sub_block=sub, options=[dict(label=l, letter=c, text="t") for l, c in
                                     zip(("RETRY", "FIX_ARGS", "SWITCH_TOOL", "ASK", "STOP", "ACCEPT", "RETRY_KEYED", "READ_BACK",
                                          "RETRY_PLAIN", "NO_RETRY", "CONTINUE_ALT", "ESCALATE", "KEEP_POLLING", "BREAK_LOOP_ALT"),
                                         "ABCDEFGHIJKLMN")],
             user_values=[], tools=[], escalation={}, attempt=1, R_cap=2)
    r.update(kw)
    return r


def test_solve_never_reads_stored_gold_or_world():
    r = _rec("b5_deny_escalate", card_b5=dict(K_c=3, K_t=None, K_w=None, W=None, window=False),
             denials=dict(n_c=1, n_t=1, n_w=None, alt_exists=True, goal_blocked_hard=False), gold="STOP", gold_letter="E",
             world_committed=True)
    assert sb.solve(r).label == "CONTINUE_ALT"
    assert "gold" not in sb.strip_gold(r) and "world_committed" not in sb.strip_gold(r)


# ---------------------------------------------------------------------------------------------------------------------- B1
def _b1(cls, a=1, cap=2, tool=None, others=(), key=False, esc=None, field=None, uv=(), curval="v-1x"):
    tool = tool or _tool("get_zed", "read", True, group="g:get:zed", verb="get")
    args = [["zed_id", curval]] + ([["idempotency_key", "k-1"]] if key else [])
    return _rec("b1_classic", tools=[tool] + list(others), call=dict(tool_tid=tool["tid"], name=tool["name"], args=args),
                error=dict(**{"class": cls, "field": field}), attempt=a, R_cap=cap, escalation=esc or {}, user_values=list(uv))


def test_b1_truth_table_exhaustive():
    eq_tool = _tool("lookup_zed", "read", True, group="g:get:zed", verb="lookup")
    kinds = {"read": _tool("get_zed", "read", True, group="g:get:zed", verb="get"),
             "idem": _tool("close_zed", "write", True, group="g:close:zed", verb="close"),
             "plain": _tool("remove_zed", "write", False, group="g:remove:zed", verb="remove")}
    for cls, a, cap, kind, key, has_eq in itertools.product(
            ("transient_unavailable", "rate_limited"), (1, 2, 3), (2, 3), kinds, (False, True), (False, True)):
        tool = kinds[kind]
        others = [dict(eq_tool, group=tool["group"], name="alt_zed")] if has_eq else []
        r = _b1(cls, a, cap, tool, others, key)
        res = sb.solve(r)
        safe = kind != "plain" or key
        if not safe:
            assert res.abstain == "non_idempotent_write_without_key_is_b2"
            continue
        exp = "RETRY" if a < cap else ("SWITCH_TOOL" if has_eq else "ASK")
        assert res.label == exp, (cls, a, cap, kind, key, has_eq)
    # class table without attempt dependence
    for esc_q, esc_u, has_eq in itertools.product(("ASK", "STOP"), ("ASK", "STOP"), (False, True)):
        tool = kinds["read"]
        others = [dict(eq_tool, group=tool["group"], name="alt_zed")] if has_eq else []
        esc = dict(quota_exhausted=esc_q, unsupported_op=esc_u)
        assert sb.solve(_b1("auth_denied", tool=tool, others=others, esc=esc)).label == "ASK"
        assert sb.solve(_b1("irrecoverable", tool=tool, others=others, esc=esc)).label == "STOP"
        assert sb.solve(_b1("invalid_unnamed", tool=tool, others=others, esc=esc)).label == ("SWITCH_TOOL" if has_eq else "ASK")
        assert sb.solve(_b1("unsupported_op", tool=tool, others=others, esc=esc)).label == ("SWITCH_TOOL" if has_eq else esc_u)
        assert sb.solve(_b1("quota_exhausted", tool=tool, others=others, esc=esc)).label == ("SWITCH_TOOL" if has_eq else esc_q)
    # invalid_named_arg: corrected value present (and different) in context -> FIX_ARGS, else ASK
    assert sb.solve(_b1("invalid_named_arg", field="zed_id", uv=[["zed_id", "v-1"]])).label == "FIX_ARGS"
    assert sb.solve(_b1("invalid_named_arg", field="zed_id", uv=[])).label == "ASK"
    assert sb.solve(_b1("invalid_named_arg", field="zed_id", uv=[["zed_id", "v-1x"]])).label == "ASK"   # nothing to correct to


# ---------------------------------------------------------------------------------------------------------------------- B2
def test_b2_replay_equals_rule_table_exhaustively():
    """C3 for B2: the event-sourced replay equals the rule table on the full truth table of visible facts."""
    for idem, key, rp, step in itertools.product((False, True), (False, True), (False, True), (1, 2)):
        tool = _tool("set_zed", "write", idem, group="g:update:zed", verb="set")
        tools = [tool] + ([_tool("get_zed", "read", True, group="g:get:zed")] if rp else [])
        for committed in ((True, False) if step == 2 else (None,)):
            r = _rec("b2_ambig_write", tools=tools,
                     call=dict(tool_tid=tool["tid"], name="set_zed", args=[["zed_id", "z-1"]] + ([["idempotency_key", "k"]] if key else [])),
                     readback=None if step == 1 else dict(tool="get_zed", committed=committed))
            res = sb.solve(r)
            assert res.label is not None and "replay_vs_rule_table_mismatch" not in res.flags, (idem, key, rp, step, committed)
            if step == 2:
                assert res.label == ("NO_RETRY" if committed else "RETRY_PLAIN")
            elif idem or key:
                assert res.label == "RETRY_KEYED"
            else:
                assert res.label == ("READ_BACK" if rp else "ASK")


def test_b2_world_flag_is_not_read():
    tool = _tool("set_zed", "write", False, group="g:update:zed", verb="set")
    base = dict(tools=[tool], call=dict(tool_tid=tool["tid"], name="set_zed", args=[["zed_id", "z-1"]]), readback=None)
    assert sb.solve(_rec("b2_ambig_write", world_committed=True, **base)).label == sb.solve(_rec("b2_ambig_write", world_committed=False, **base)).label == "ASK"


# ---------------------------------------------------------------------------------------------------------------------- B3
def _b3(result, ctx, rw="read", a=1, eq=False):
    tool = _tool("get_zed", rw, rw == "read", group="g:get:zed" if rw == "read" else "g:set:zed", verb="get")
    tools = [tool] + ([_tool("lookup_zed", "read", True, group=tool["group"], verb="lookup")] if eq else [])
    return _rec("b3_implicit", tools=tools, call=dict(tool_tid="x", name="get_zed", args=[]), result=result, ctx=ctx, attempt=a,
                b3=dict(vtype="negative_value", violating=True))


def test_b3_order_c1():
    ctx = dict(stated_count=None, prior_ids=None, reference=None, unique=False, order=None, nonneg_fields=["f"], intended_args=None,
               prior_args=None, call_args={})
    ok = dict(items=None, fields={"f": 0}, total=None, echo=None)
    bad = dict(items=None, fields={"f": -3}, total=None, echo=None)
    assert sb.solve(_b3(ok, ctx)).label == "ACCEPT"                                     # (1)
    assert sb.solve(_b3(bad, ctx, rw="write")).label == "ASK"                          # (3) write
    assert sb.solve(_b3(bad, ctx, a=1)).label == "RETRY"                               # (4) read, first
    assert sb.solve(_b3(bad, ctx, a=2, eq=True)).label == "SWITCH_TOOL"                # (5) read, recurrence + equivalent
    assert sb.solve(_b3(bad, ctx, a=2, eq=False)).label == "ASK"                       # (5) no equivalent
    # (2) arg-induced beats the write rule: scale mismatch caused by the call's own argument
    ctx2 = dict(ctx, nonneg_fields=[], reference=dict(field="g", value=45), call_args={"g": 450})
    r = dict(items=None, fields={"g": 450}, total=None, echo=None)
    assert sb.solve(_b3(r, ctx2, rw="write")).label == "FIX_ARGS"
    ctx3 = dict(ctx2, call_args={"g": 45})                                              # data-induced: the argument matches
    assert sb.solve(_b3(r, ctx3, rw="write")).label == "ASK"


def test_b3_each_checker_and_the_heldout_two():
    base = dict(stated_count=None, prior_ids=None, reference=None, unique=False, order=None, nonneg_fields=[], intended_args=None,
                prior_args=None, call_args={})
    cases = [
        (dict(items=[], fields={}, total=None, echo=None), dict(base, stated_count=5), "RETRY"),
        (dict(items=[], fields={}, total=None, echo=None), dict(base, stated_count=0), "ACCEPT"),
        (dict(items=["a-2"], fields={}, total=None, echo=None), dict(base, prior_ids=["a-1"], call_args={"id": "a-1"}), "RETRY"),
        (dict(items=["a-1"], fields={}, total=None, echo=None), dict(base, prior_ids=["a-1"], call_args={"id": "a-1"}), "ACCEPT"),
        (dict(items=[1, 2, 3], fields={}, total=7, echo=None), base, "RETRY"),
        (dict(items=[2, 2, 2], fields={}, total=6, echo=None), base, "ACCEPT"),
        (dict(items=None, fields={"g": 3400}, total=None, echo=None), dict(base, reference=dict(field="g", value=34), call_args={"g": 34}), "RETRY"),
        (dict(items=None, fields={"g": 40}, total=None, echo=None), dict(base, reference=dict(field="g", value=34), call_args={"g": 34}), "ACCEPT"),
        (dict(items=None, fields={}, total=None, echo={"limit": 5}),
         dict(base, prior_args={"limit": 5}, intended_args={"limit": 9}, call_args={"limit": 9}), "RETRY"),
        (dict(items=None, fields={}, total=None, echo={"limit": 9}),
         dict(base, prior_args={"limit": 5}, intended_args={"limit": 9}, call_args={"limit": 9}), "ACCEPT"),
        # the two held-out types (not generated in the main set; coded from the G0-lite list)
        (dict(items=["a", "b", "a"], fields={}, total=None, echo=None), dict(base, unique=True), "RETRY"),
        (dict(items=["a", "b", "c"], fields={}, total=None, echo=None), dict(base, unique=True), "ACCEPT"),
        (dict(items=[3, 1, 2], fields={}, total=None, echo=None), dict(base, order="asc"), "RETRY"),
        (dict(items=[1, 2, 3], fields={}, total=None, echo=None), dict(base, order="asc"), "ACCEPT"),
    ]
    for res, ctx, exp in cases:
        assert sb.solve(_b3(res, ctx)).label == exp, (res, exp)


# ------------------------------------------------------------------------------------------------------------- B5 / B6 tables
def test_b5_truth_table_exhaustive():
    for nc, nt, nw, alt, hard, window in itertools.product((0, 1, 2, 3, 4), (0, 9, 10, 19, 20), (None, 0, 9, 10), (False, True),
                                                           (False, True), (False, True)):
        card = dict(K_c=3, K_t=None if window else 20, K_w=10 if window else None, W=50 if window else None, window=window)
        r = _rec("b5_deny_escalate", card_b5=card, denials=dict(n_c=nc, n_t=nt, n_w=nw if window else None, alt_exists=alt,
                                                                 goal_blocked_hard=hard))
        over = nc >= 3 or (not window and nt >= 20) or (window and nw is not None and nw >= 10)
        exp = "ESCALATE" if over else ("STOP" if hard else ("CONTINUE_ALT" if alt else "ESCALATE"))
        assert sb.solve(r).label == exp, (nc, nt, nw, alt, hard, window)


def _poll(progress, counter=None, status=None):
    return [dict(progress=p, counter=(counter[i] if counter else None), status=(status[i] if status else None)) for i, p in enumerate(progress)]


def test_b6_c2_order():
    card = dict(P_cap=10, L=3, transitions=[["queued", "running"]], non_waitable=False)
    adv = _poll([1, 2, 3, 4])
    flat = _poll([4, 4, 4, 4, 4])
    r = lambda obs, used, alt, **cd: _rec("b6_loop_poll", card_b6=dict(card, **cd), poll=dict(obs=obs, calls_used=used, alt_exists=alt))
    assert sb.solve(r(adv, 3, False)).label == "KEEP_POLLING"                          # (1)
    assert sb.solve(r(adv, 10, False)).label == "ESCALATE"                             # (2)
    assert sb.solve(r(_poll([4, 4, 4]), 3, True)).label == "KEEP_POLLING"              # (3) flat for 2 < L
    assert sb.solve(r(flat, 5, True)).label == "BREAK_LOOP_ALT"                        # (4)
    assert sb.solve(r(flat, 5, False, non_waitable=True)).label == "STOP"              # (5)
    assert sb.solve(r(flat, 5, False)).label == "ESCALATE"                             # (6)
    # (4) before (5): an alternative wins over a non-waitable goal
    assert sb.solve(r(flat, 5, True, non_waitable=True)).label == "BREAK_LOOP_ALT"
    # declared status transition and counter advance count as change; a decrease does not
    assert sb.solve(r(_poll([None, None], status=["queued", "running"]), 3, False)).label == "KEEP_POLLING"
    assert sb.solve(r(_poll([9, 9, 9, 9], counter=[1, 1, 1, 2]), 3, False)).label == "KEEP_POLLING"
    assert sb.solve(r(_poll([9, 8, 7, 6]), 5, True)).label == "BREAK_LOOP_ALT"
    # reading switch: the literal window reading calls an early advance "changed"
    obs = _poll([1, 2, 3, 3, 3, 3])
    assert sb.solve_b6(sb.strip_gold(r(obs, 5, True)), reading="last_step").label == "BREAK_LOOP_ALT"


# ------------------------------------------------------------------------------------------------- generator agreement
def test_agreement_on_in_memory_sample():
    try:
        import t55_generator as gen
    except Exception as e:  # pragma: no cover
        pytest.skip("generator not importable: %s" % e)
    recs = gen.generate_in_memory(total=300, seed="b-test-agree", standin=True)
    bad = [(r["sub_block"], r["gold"]) for r in recs if sb.solve(r).label != r["gold"]]
    assert len(bad) / len(recs) <= 0.01, bad[:5]
    for r in recs:
        kind, val, _ = rb.solve_text(r["rendered"]["text"])
        assert kind == "abstain" or val == r["gold_letter"]
