"""C3 (Opus ruling, T55): the exhaustive truth-table test must cover B3 as well: rule table = A's evaluator = B's evaluator on every
cell of (violation type x cause x violating/valid x tool kind x attempt x equivalent listed). The B1, B2, B5, B6 tables are in
test_solver_b_t55.py; the B3 table was only checked by order examples, so it is closed here."""
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

import t55_gates as gates  # noqa: E402
import t55_solver_b as sb  # noqa: E402
from tool_engine import invariants, perturb, util  # noqa: E402


def _tool(name, rw, group):
    return dict(tid=name, verb=name.split("_")[0], entity="zed", name=name, rw=rw, idempotent=(rw == "read"), group=group, params=[])


def _b_record(result, ctx, rw, a, eq):
    t = _tool("get_zed", rw, "g:get:zed")
    tools = [t] + ([_tool("lookup_zed", rw, "g:get:zed")] if eq else [])
    return dict(sub_block="b3_implicit", options=[], tools=tools, call=dict(tool_tid="get_zed", name="get_zed", args=[]),
                result=result, ctx=ctx, attempt=a, b3=dict(vtype="x", violating=True))


def test_b3_rule_table_equals_a_equals_b_on_every_cell():
    rng = util.rng_for("c3-b3")
    n = 0
    for vt in perturb.VIOLATION_TYPES:                          # all eight, held-out two included
        for cause in ("data", "arg"):
            if cause == "arg" and vt not in invariants.ARG_CAPABLE:
                continue
            for violating in (True, False):
                base = invariants.make_base(vt, rng, "kol", "qty", cause)
                result, ctx = invariants.materialise(base, violating)
                for rw, a, eq in itertools.product(("read", "write"), (1, 2, 3), (False, True)):
                    cause_arg = violating and invariants.cause(vt, result, ctx) == "arg"
                    want = gates.b3_rule_table(violating, cause_arg, rw, a, eq)
                    rec_a = dict(result=result, ctx=ctx, attempt=a, call=dict(tool_tid="t0", args=[]),
                                 tools=[dict(tid="t0", rw=rw, idempotent=rw == "read", group="g:x", entity="e", verb="v", params=[])] +
                                 ([dict(tid="te", rw=rw, idempotent=rw == "read", group="g:x", entity="e", verb="w", params=[])] if eq else []))
                    got_a = gates.sa.b3_label(rec_a)
                    got_b = sb.solve(_b_record(result, ctx, rw, a, eq))
                    assert got_b.abstain is None
                    assert want == got_a == got_b.label, (vt, cause, violating, rw, a, eq, want, got_a, got_b.label)
                    n += 1
    assert n == 264
