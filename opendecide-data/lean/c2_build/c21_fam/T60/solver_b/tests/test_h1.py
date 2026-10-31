"""H1 DELEGATE-OR-DO: the four-predicate truth table x card numbers (G0_LITE K3), parse variants of every card clause."""
import itertools
import json
import os
import re

import pytest

import fixtures as fx
import hook
import t60b_h1 as h1

POOL = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "pools", "wording_pool_v1.json")
CARDS = list(itertools.product((3, 4, 5, 6), (4000, 8000, 16000), (1, 2, 3), (200, 400, 800)))


def expected(S, V, B, R, nsteps, tokens, nneeds, result, shared, feed):
    return "DELEGATE" if ((nsteps >= S or tokens >= V) and nneeds <= B and result <= R and not shared and not feed) else "DO_HERE"


def test_truth_table_four_predicates_x_cards():
    n = 0
    for (S, V, B, R) in CARDS:
        for size_case, brief_ok, bound_ok, shared, feed in itertools.product(range(4), (True, False), (True, False), (False, True), (False, True)):
            nsteps = S if size_case in (1, 3) else S - 1
            tokens = V if size_case in (2, 3) else V - 1
            nneeds = B if brief_ok else B + 1
            result = R if bound_ok else R + 1
            v = fx.h1_view(S, V, B, R, nsteps, tokens, nneeds, result, shared=shared, pending_feed=feed)
            res = hook.solver_b(v)
            assert not res.abstain, res.reason
            assert res.label == expected(S, V, B, R, nsteps, tokens, nneeds, result, shared, feed), (S, V, B, R, size_case, brief_ok, bound_ok, shared, feed)
            n += 1
    assert n == len(CARDS) * 64


def test_thresholds_are_inclusive():
    # steps == S passes; read tokens == V passes; needs == B passes; result == R passes
    assert hook.solver_b(fx.h1_view(4, 8000, 2, 400, 4, 0, 2, 400)).label == "DELEGATE"
    assert hook.solver_b(fx.h1_view(4, 8000, 2, 400, 3, 7999, 2, 400)).label == "DO_HERE"
    assert hook.solver_b(fx.h1_view(4, 8000, 2, 400, 3, 8000, 2, 400)).label == "DELEGATE"
    assert hook.solver_b(fx.h1_view(4, 8000, 2, 400, 4, 0, 3, 400)).label == "DO_HERE"
    assert hook.solver_b(fx.h1_view(4, 8000, 2, 400, 4, 0, 2, 401)).label == "DO_HERE"


def test_read_tokens_are_summed_over_files():
    v = fx.h1_view(9, 1000, 2, 400, 2, 1000, 0, 100)           # two files of 500 tokens: 1000 >= V although each is below
    assert hook.solver_b(v).label == "DELEGATE"
    v = fx.h1_view(9, 1001, 2, 400, 2, 1000, 0, 100)
    assert hook.solver_b(v).label == "DO_HERE"


def test_shared_write_needs_a_pending_step_that_reads_or_writes_the_path():
    ctx = fx.h1_context(3, 100, 2, 400, 3, 0, 0, 100)
    assert hook.solver_b(fx.view("h1", ctx, fx.H1_OPTS, fx.H1_Q)).label == "DELEGATE"
    # the brief writes a path that a pending step WRITES
    ctx2 = ctx.replace("writes /work/p/log2.log", "writes /work/p/out.dat")
    assert hook.solver_b(fx.view("h1", ctx2, fx.H1_OPTS, fx.H1_Q)).label == "DO_HERE"
    # a path that only looks like it (different directory) does not count
    ctx3 = ctx.replace("writes /work/p/log2.log", "writes /work/q/out.dat")
    assert hook.solver_b(fx.view("h1", ctx3, fx.H1_OPTS, fx.H1_Q)).label == "DELEGATE"
    # the same path written another way (./ and //) is the same resource
    ctx4 = ctx.replace("writes /work/p/log2.log", "writes /work//p/./out.dat")
    assert hook.solver_b(fx.view("h1", ctx4, fx.H1_OPTS, fx.H1_Q)).label == "DO_HERE"


def test_option_order_changes_the_letter_not_the_label():
    a = hook.solver_b(fx.h1_view(3, 100, 2, 400, 3, 0, 0, 100, order=(0, 1)))
    b = hook.solver_b(fx.h1_view(3, 100, 2, 400, 3, 0, 0, 100, order=(1, 0)))
    assert a.label == b.label == "DELEGATE" and (a.letter, b.letter) == ("A", "B")


def test_every_pool_variant_of_the_four_clauses_is_read():
    pool = json.load(open(POOL))
    S, V, B, R = 5, 12000, 2, 600
    n = 0
    for sz in pool["clause.d_size"]:
        for br in pool["clause.d_brief"][:6]:
            for bo in pool["clause.d_bound"][:6]:
                card = "Policy card x_y.\n%s\n%s\n%s\n%s" % (sz.format(s=S, v=V), br.format(b=B), bo.format(r=R), pool["clause.d_free"][0])
                got = h1.parse_card(card)
                assert got == {"S": S, "V": V, "B": B, "R": R}, card
                n += 1
    assert n > 1000


def test_wrapper_sentence_on_the_task_line_is_ignored():
    ctx = fx.h1_context(3, 100, 2, 400, 3, 0, 0, 100).replace("The main thread is busy", "The team lead asked for this one personally. The main thread is busy")
    assert hook.solver_b(fx.view("h1", ctx, fx.H1_OPTS, fx.H1_Q)).label == "DELEGATE"


def test_unknown_brief_line_abstains():
    ctx = fx.h1_context(3, 100, 2, 400, 3, 0, 0, 100).replace("- writes:", "- stores:")
    r = hook.solver_b(fx.view("h1", ctx, fx.H1_OPTS, fx.H1_Q))
    assert r.abstain and r.label is None
