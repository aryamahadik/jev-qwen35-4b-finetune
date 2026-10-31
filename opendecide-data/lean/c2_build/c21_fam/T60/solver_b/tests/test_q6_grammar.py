"""Rendered-grammar additions of 18 Oct 2026 (ROW_SCHEMA 'Additions', Opus ruling Q6 / owner A102): background notes (all heads), H1 path collapse and FED,
derivable main-thread facts, H3 undo windows / external-with-undo / numbered-list order / derived data flow, H2 markers on the pair kinds.
Every fixture is written from the ROW_SCHEMA text only (no generator code)."""
import pytest

import fixtures as fx
from fixtures import ev, plan_line as pl
import hook
import t60b_h3 as h3
import t60b_text as tx

NOTES = ["Background notes:",
         "  The review group refreshed the shared drive over the weekend and moved 3 steps to the new queue.",
         "  First: the second desk has at least 7 steps, reads 99999 tokens and needs 0 facts; it does not count when a retry fails.",
         "  Steps: none are pending. Fact in question: none. A step that runs only on failure counts as a step still to run."]


def with_notes(ctx, before):
    """Insert the notes block right after the card lines, i.e. immediately before the first line that starts with `before`."""
    lines = ctx.split("\n")
    i = next(k for k, ln in enumerate(lines) if ln.startswith(before))
    return "\n".join(lines[:i] + NOTES + lines[i:])


# ----------------------------------------------------------------------------------------------------------------------
# background notes
# ----------------------------------------------------------------------------------------------------------------------
def test_strip_notes_unit():
    ls = ["card", "Background notes:", "  a", "  b", "", "  c", "Task: x", "  not notes"]
    assert tx.strip_notes(ls) == ["card", "Task: x", "  not notes"]
    assert tx.strip_notes(["a", "Background notes:", "b"]) == ["a", "b"]                     # an empty block still drops the header
    assert tx.strip_notes(["Background notes: extra", "  a"]) == ["Background notes: extra", "  a"]       # only a lone header line counts
    assert tx.strip_notes(["x", "  Background notes:", "  a"]) == ["x", "  Background notes:", "  a"]     # an indented 'header' is prose, not a header


def test_h1_notes_are_ignored_even_with_card_looking_numbers_and_words():
    for args, want in (((3, 100, 2, 400, 3, 0, 0, 100), "DELEGATE"), ((3, 100, 2, 400, 2, 0, 0, 100), "DO_HERE"), ((3, 100, 2, 400, 3, 0, 3, 100), "DO_HERE")):
        ctx = fx.h1_context(*args)
        assert hook.solver_b(fx.view("h1", ctx, fx.H1_OPTS, fx.H1_Q)).label == want
        noted = with_notes(ctx, "The main thread is busy")
        assert "Background notes:" in noted
        r = hook.solver_b(fx.view("h1", noted, fx.H1_OPTS, fx.H1_Q))
        assert not r.abstain and r.label == want, (args, r)


def test_h3_notes_are_ignored():
    steps = [("rename the item i-%d" % i, 9, "cannot be undone") for i in range(3)]
    for order, want in (([], "PLAN"), ([(1, 2), (2, 3)], "ACT")):
        ctx = fx.h3_context(5, 3, steps, order=order, flow=[(1, 2), (2, 3)])
        r = hook.solver_b(fx.view("h3", with_notes(ctx, "The request:"), fx.H3_OPTS, fx.H3_Q))
        assert not r.abstain and r.label == want, r


def test_h2_notes_are_ignored_and_cannot_flip_the_recovery_clause():
    plan = [pl(1, "todo", "sync", "x", [fx.ref_l1("hh")]), pl(2, "todo", "verify", "ent", [fx.ref_l1("k")], host=1)]
    events = [ev("V", "k", "ent", 1), ev("get", "x", "hh", 2)]
    for counts, want in ((True, "KEEP"), (False, "DROP")):
        ctx = fx.h2_context(counts, plan, events, 1, "V", "k", 1)
        assert hook.solver_b(fx.view("h2", ctx, fx.H2_OPTS, fx.H2_Q)).label == want
        noted = with_notes(ctx, "Task:")
        r = hook.solver_b(fx.view("h2", noted, fx.H2_OPTS, fx.H2_Q))
        assert not r.abstain and r.label == want, (counts, r)


def test_notes_with_a_blank_line_inside_the_block_and_before_the_next_section():
    ctx = fx.h1_context(3, 100, 2, 400, 3, 0, 0, 100)
    lines = ctx.split("\n")
    i = next(k for k, ln in enumerate(lines) if ln.startswith("The main thread is busy"))
    block = ["Background notes:", "  First paragraph of prose with 5 steps.", "", "  Second paragraph of prose with 6 facts."]
    noted = "\n".join(lines[:i] + block + lines[i:])
    assert hook.solver_b(fx.view("h1", noted, fx.H1_OPTS, fx.H1_Q)).label == "DELEGATE"


# ----------------------------------------------------------------------------------------------------------------------
# H1: path collapse, SHARED, FED, derivable facts
# ----------------------------------------------------------------------------------------------------------------------
BASE = dict(S=3, V=100, B=2, R=400, nsteps=3, read_tokens=100, nneeds=0, result=100)


def h1_label(mut):
    ctx = fx.h1_context(BASE["S"], BASE["V"], BASE["B"], BASE["R"], BASE["nsteps"], BASE["read_tokens"], BASE["nneeds"], BASE["result"])
    ctx = mut(ctx)
    r = hook.solver_b(fx.view("h1", ctx, fx.H1_OPTS, fx.H1_Q))
    assert not r.abstain, r.reason
    return r.label


def test_h1_baseline_is_delegate():
    assert h1_label(lambda c: c) == "DELEGATE"


@pytest.mark.parametrize("spelling", ["/work/p/a.dat", "/work/p/./a.dat", "/work/p/q/../a.dat", "/work//p/a.dat", "/work/p/x/y/../../a.dat"])
def test_h1_fed_file_in_any_collapsed_spelling_forces_do_here(spelling):
    # a pending main step WRITES the file that the subtask would read (the read tokens still count towards SIZE)
    assert h1_label(lambda c: c.replace("writes /work/p/log2.log", "writes " + spelling)) == "DO_HERE"


@pytest.mark.parametrize("spelling", ["/work/p/a.dat", "/work/p/./a.dat", "/work/p/q/../a.dat"])
def test_h1_fed_file_spelled_differently_on_the_subtask_side(spelling):
    assert h1_label(lambda c: c.replace("- reads /work/p/a.dat (", "- reads %s (" % spelling).replace("writes /work/p/log2.log", "writes /work/p/a.dat")) == "DO_HERE"


def test_h1_a_pending_step_that_only_reads_the_file_does_not_feed_it():
    assert h1_label(lambda c: c.replace("reads /work/p/in2.cfg;", "reads /work/p/a.dat;")) == "DELEGATE"


def test_h1_a_different_directory_is_not_fed():
    assert h1_label(lambda c: c.replace("writes /work/p/log2.log", "writes /work/q/a.dat")) == "DELEGATE"
    assert h1_label(lambda c: c.replace("writes /work/p/log2.log", "writes /work/p/q/../../a.dat")) == "DELEGATE"       # collapses to /work/a.dat


@pytest.mark.parametrize("spelling", ["/work/p/log1.log", "/work/p/./log1.log", "/work/p/z/../log1.log", "/work//p//log1.log"])
def test_h1_shared_write_with_path_collapse(spelling):
    assert h1_label(lambda c: c.replace("- writes: /work/p/out.dat", "- writes: " + spelling)) == "DO_HERE"
    assert h1_label(lambda c: c.replace("- writes: /work/p/out.dat", "- writes: " + spelling).replace("writes /work/p/log1.log", "writes /work/p/other.log")
                    .replace("reads /work/p/in1.cfg", "reads " + spelling)) == "DO_HERE"        # a pending READ of the written path also shares it


def test_h1_fed_file_volume_still_counts_for_size_but_fed_still_blocks():
    # size passes ONLY through the read tokens (2 steps < S=3), the fed file is one of the two files: FREE fails, so DO_HERE; unfed it is DELEGATE
    ctx = fx.h1_context(3, 100, 2, 400, 2, 100, 0, 100)
    assert hook.solver_b(fx.view("h1", ctx, fx.H1_OPTS, fx.H1_Q)).label == "DELEGATE"
    fed = ctx.replace("writes /work/p/log2.log", "writes /work/p/b.dat")
    assert hook.solver_b(fx.view("h1", fed, fx.H1_OPTS, fx.H1_Q)).label == "DO_HERE"


def test_h1_derivable_main_thread_facts_are_plain_facts_and_only_named_handles_count():
    def mut(c):
        return c.replace("- the alpha is 10", "- the alpha is the bravo plus 4").replace("- the charlie is 12", "- the charlie is the delta plus 15")
    # B = 2: two handles named (one of them derivable) still pass; the derivable fact lines add nothing to the count
    ctx = fx.h1_context(3, 100, 2, 400, 3, 0, 2, 100)
    assert "- the alpha is 10" in ctx
    assert hook.solver_b(fx.view("h1", mut(ctx), fx.H1_OPTS, fx.H1_Q)).label == "DELEGATE"
    ctx3 = fx.h1_context(3, 100, 2, 400, 3, 0, 3, 100)
    assert hook.solver_b(fx.view("h1", mut(ctx3), fx.H1_OPTS, fx.H1_Q)).label == "DO_HERE"          # three NAMED handles: B + 1
    # naming the derived handle in the brief counts like any other (the brief predicate is about the named handles)
    ctx_named = fx.h1_context(3, 100, 2, 400, 3, 0, 2, 100)
    assert hook.solver_b(fx.view("h1", mut(ctx_named), fx.H1_OPTS, fx.H1_Q)).label == "DELEGATE"


# ----------------------------------------------------------------------------------------------------------------------
# H3: undo windows, external with an undo path, numbered list, derived data flow
# ----------------------------------------------------------------------------------------------------------------------
EXT_UNDO = "reaches people outside the team (can be undone for 9 more days)"


def test_h3_effect_phrases_unit():
    assert h3.effect_undoable(EXT_UNDO) is False                                              # external although an undo path exists
    assert h3.effect_undoable("reaches people outside the team (can be undone for 1 more day)") is False
    assert h3.effect_undoable("can be undone for 5 more days (the step runs in 3 days)") is True        # 5 - 3 = 2
    assert h3.effect_undoable("can be undone for 5 more days (the step runs in 4 days)") is True        # 5 - 4 = 1 (boundary)
    assert h3.effect_undoable("can be undone for 5 more days (the step runs in 5 days)") is False       # 5 - 5 = 0: counts as cannot be undone
    assert h3.effect_undoable("can be undone for 5 more days (the step runs in 9 days)") is False
    assert h3.effect_undoable("can be undone for 1 more day (the step runs in 0 days)") is True
    assert h3.effect_undoable("can be undone for 5 more days (the step runs in 1 day)") is True
    assert h3.effect_undoable("can be undone for 14 more days") is True                                  # without the parenthesis E = 0
    assert h3.effect_undoable("can be undone for 0 more days") is False
    with pytest.raises(Exception):
        h3.effect_undoable("can be undone for 5 more days (the step runs soon)")


def _h3(steps, order=(), flow=((1, 2),), H=5, n_min=3, numbered=False):
    ctx = fx.h3_context(H, n_min, steps, order=list(order), flow=list(flow))
    if numbered:
        ctx = ctx.replace("- no order is given", "- the steps are numbered in the order in which they are to be carried out")
    return ctx


def lab3(ctx):
    r = hook.solver_b(fx.view("h3", ctx, fx.H3_OPTS, fx.H3_Q))
    assert not r.abstain, r.reason
    return r.label


def test_h3_external_with_undo_path_is_high_stakes_and_a_delayed_window_can_make_a_step_irreversible():
    ok = "can be undone for 14 more days"
    base = [("rename the item i-0", 1, ok), ("rename the item i-1", 1, ok), ("rename the item i-2", 1, ok)]
    assert lab3(_h3(base)) == "ACT"                                                             # nothing high stakes
    assert lab3(_h3([base[0], base[1], ("rename the item i-2", 1, EXT_UNDO)])) == "PLAN"        # external, undo path or not
    assert lab3(_h3([base[0], base[1], ("rename the item i-2", 1, "can be undone for 5 more days (the step runs in 3 days)")])) == "ACT"
    assert lab3(_h3([base[0], base[1], ("rename the item i-2", 1, "can be undone for 5 more days (the step runs in 5 days)")])) == "PLAN"
    assert lab3(_h3([base[0], base[1], ("rename the item i-2", 1, "can be undone for 5 more days (the step runs in 4 days)")])) == "ACT"


def test_h3_numbered_list_states_every_consecutive_pair_and_their_closure():
    steps = [("rename the item i-%d" % i, 9, "cannot be undone") for i in range(4)]
    # all four steps are high stakes, n = 4 >= 3, so the label is decided by R3 alone
    assert lab3(_h3(steps, flow=[(1, 2), (2, 3), (3, 4)], numbered=True)) == "ACT"
    assert lab3(_h3(steps, flow=[(1, 3)], numbered=True)) == "ACT"                                # closure
    assert lab3(_h3(steps, flow=[(1, 4), (2, 4)], numbered=True)) == "ACT"
    assert lab3(_h3(steps, flow=[(2, 1)], numbered=True)) == "PLAN"                               # s1 uses the output of s2: not the stated direction
    assert lab3(_h3(steps, flow=[(1, 2)], numbered=False)) == "PLAN"                              # no order stated at all
    # the numbered statement and an explicit order statement together: the union
    ctx = _h3(steps, order=[(4, 1)], flow=[(4, 1), (1, 2)])
    ctx = ctx.replace("- Do step s4 before step s1.", "- Do step s4 before step s1.\n- the steps are numbered in the order in which they are to be carried out")
    ctx = ctx.replace("- Step s4 has to come before step s1.", "- Step s4 has to come before step s1.\n- the steps are numbered in the order in which they are to be carried out")
    assert "numbered in the order" in ctx and lab3(ctx) == "ACT"


def test_h3_numbered_statement_with_no_order_given_is_a_conflict_and_a_shuffled_listing_is_ambiguous():
    steps = [("rename the item i-%d" % i, 9, "cannot be undone") for i in range(3)]
    ctx = _h3(steps, numbered=True).replace("Order given in the request:", "Order given in the request:\n- no order is given")
    r = hook.solver_b(fx.view("h3", ctx, fx.H3_OPTS, fx.H3_Q))
    assert r.abstain and r.reason == "parse_gap:h3_order_conflict"
    # the listing order disagrees with the numbering: the text does not say which one is meant -> abstain (listed for Opus)
    ctx = _h3(steps, numbered=True)
    lines = ctx.split("\n")
    i = next(k for k, ln in enumerate(lines) if ln.startswith("- s1:"))
    lines[i], lines[i + 1] = lines[i + 1], lines[i]
    r = hook.solver_b(fx.view("h3", "\n".join(lines), fx.H3_OPTS, fx.H3_Q))
    assert r.abstain and r.reason == "parse_gap:h3_numbered_listing_order_ambiguous"


def test_h3_derived_value_flow_line_is_the_same_dependency():
    steps = [("rename the item i-%d" % i, 9, "cannot be undone") for i in range(3)]
    plain = _h3(steps, flow=[(1, 2)])
    derived = plain.replace("- s2 uses the output of s1", "- s2 uses a value derived from the output of s1")
    assert derived != plain and lab3(plain) == lab3(derived) == "PLAN"
    stated = _h3(steps, order=[(1, 2)], flow=[(1, 2)])
    assert lab3(stated.replace("- s2 uses the output of s1", "- s2 uses a value derived from the output of s1")) == "ACT"
    r = hook.solver_b(fx.view("h3", plain.replace("- s2 uses the output of s1", "- s2 uses a value from s1"), fx.H3_OPTS, fx.H3_Q))
    assert r.abstain and r.reason == "parse_gap:h3_flow_line"


# ----------------------------------------------------------------------------------------------------------------------
# H2: markers on the pair kinds (emphasis suffix on the fact line, a path: line included; identifier-shaped and large values; repeat)
# ----------------------------------------------------------------------------------------------------------------------
def lab2(counts, plan, events, qt, qtype, qh, qv):
    r = hook.solver_b(fx.h2_view(counts, plan, events, qt, qtype, qh, qv))
    assert not r.abstain, r.reason
    return r.label


@pytest.mark.parametrize("suffix", ["", " (a striking value)", " (a remarkable value)", " (a notable value)"])
def test_h2_pointer_pair_with_an_emphasis_suffix_on_the_path_line(suffix):
    export = ev("export", "snap", "/w/s.snap")
    export[-1] += suffix
    events = [export, ev("read", "snap", "/w/s.snap", "body", 99)]
    plan = [pl(1, "todo", "sync", "snap", [fx.ref_ptr("snap")])]
    for quoted in ("/w/s.snap", "/w/s.snap" + suffix):                       # the quote may or may not repeat the suffix
        assert lab2(False, plan, events, 1, "P", "path", quoted) == "KEEP"
    body = ev("read", "snap", "/w/s.snap", "body", 99)
    body[-1] += suffix
    assert lab2(False, plan, [ev("export", "snap", "/w/s.snap"), body], 2, "R", "body", "99") == "DROP"


@pytest.mark.parametrize("value", ["gat-27xq", "7a3f9c2e11", 9000000, "12345678901234567890"])
def test_h2_identifier_shaped_and_large_values_are_plain_values(value):
    events = [ev("get", "ent", "hh", value, "a striking value"), ev("V", "k", "ent", value)]
    plan = [pl(1, "todo", "sync", "ent", [fx.ref_l1("hh")])]
    assert lab2(False, plan, events, 1, "R", "hh", str(value)) == "KEEP"
    assert lab2(False, plan, events, 2, "V", "k", str(value)) == "DROP"


def test_h2_step_done_and_recovery_pairs_with_markers():
    events = [ev("V", "k", "ent", 5, "a notable value"), ev("check", "ent"), ev("M", "k", "ent", 5)]       # repeat marker on a non-supersession fact
    todo = [pl(1, "todo", "sync", "ent", [fx.ref_l1("k")])]
    done = [pl(1, "done", "sync", "ent", [fx.ref_l1("k")]), pl(2, "todo", "sync", "ent", [])]
    assert lab2(False, todo, events, 1, "V", "k", "5") == "KEEP"
    assert lab2(False, done, events, 1, "V", "k", "5") == "DROP"
    recov = [pl(1, "todo", "sync", "x", [fx.ref_l1("hh")]), pl(2, "todo", "verify", "ent", [fx.ref_l1("k")], host=1)]
    ev2 = [ev("V", "k", "ent", 5, "a remarkable value"), ev("get", "x", "hh", 2)]
    assert lab2(True, recov, ev2, 1, "V", "k", "5") == "KEEP" and lab2(False, recov, ev2, 1, "V", "k", "5") == "DROP"


def test_h2_supersession_chain_with_markers_on_distinct_values_and_a_repeat_on_it_abstains():
    events = [ev("V", "k", "ent", 1, "a striking value"), ev("V", "k", "ent", 2, "a notable value"), ev("V", "k", "ent", 3)]
    plan = [pl(1, "todo", "sync", "ent", [fx.ref_l1("k")])]
    assert [lab2(False, plan, events, t, "V", "k", str(t)) for t in (1, 2, 3)] == ["DROP", "DROP", "KEEP"]
    events_rep = events + [ev("M", "k", "ent", 3)]                                                  # 'repeat never occurs on a supersession chain'
    r = hook.solver_b(fx.h2_view(False, plan, events_rep, 3, "V", "k", "3"))
    assert r.abstain and r.reason == "parse_gap:h2_repeat_marker_in_supersession_chain"


# ----------------------------------------------------------------------------------------------------------------------
# H2: a reference (any level) that lands on a superseded fact takes the CURRENT value of that role (G0-lite 3.4)
# ----------------------------------------------------------------------------------------------------------------------
def test_h2_ordinal_reference_onto_a_superseded_record_takes_the_current_record():
    # two get calls return the same role (handle hh, entity ent): record 1 is superseded by record 2
    events = [ev("get", "ent", "hh", 11), ev("check", "ent"), ev("get", "ent", "hh", 12)]
    plan_first = [pl(1, "todo", "sync", "ent", [fx.ref_l3("first")])]                       # names the OLD record by position
    plan_second = [pl(1, "todo", "sync", "ent", [fx.ref_l3("second")])]
    for plan in (plan_first, plan_second):
        assert lab2(False, plan, events, 1, "R", "hh", "11") == "DROP"                      # the superseded record is not needed
        assert lab2(False, plan, events, 3, "R", "hh", "12") == "KEEP"                      # the current value is
    # an ordinal onto a record that is NOT superseded is unchanged
    events2 = [ev("get", "ent", "hh", 11), ev("get", "ent2", "hh", 12)]
    plan = [pl(1, "todo", "sync", "ent", [fx.ref_l3("first")])]
    assert lab2(False, plan, events2, 1, "R", "hh", "11") == "KEEP" and lab2(False, plan, events2, 2, "R", "hh", "12") == "DROP"


def test_h2_role_description_and_pointer_references_onto_superseded_facts_take_the_current_value():
    events = [ev("create", "ent", "key", 21), ev("create", "ent", "key", 22), ev("export", "snap", "/w/a.snap"), ev("export", "snap", "/w/b.snap")]
    plan = [pl(1, "todo", "sync", "ent", [fx.ref_l2("S", "ent")]), pl(2, "todo", "sync", "snap", [fx.ref_ptr("snap")])]
    assert [lab2(False, plan, events, t, "S", "key", str(20 + t)) for t in (1, 2)] == ["DROP", "KEEP"]
    assert lab2(False, plan, events, 3, "P", "path", "/w/a.snap") == "DROP" and lab2(False, plan, events, 4, "P", "path", "/w/b.snap") == "KEEP"
