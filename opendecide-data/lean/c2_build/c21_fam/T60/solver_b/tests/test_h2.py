"""H2 KEEP-OR-DROP: reference grammar L1-L4, statuses, supersession, contingency steps, reminders, plus a randomised cross product checked
against a spec-side oracle that is written in this file (pointer based, so it is a different computation from the text-side ablation)."""
import json
import os
import random

import fixtures as fx
from fixtures import ev, plan_line as pl
import hook
import t60b_h2 as h2


def lab(counts, plan, events, qturn, qtype, qh, qv, **kw):
    r = hook.solver_b(fx.h2_view(counts, plan, events, qturn, qtype, qh, qv, **kw))
    assert not r.abstain, r.reason
    return r.label


def test_l1_needed_and_unneeded():
    events = [ev("get", "ent", "hh", 5), ev("V", "kk", "ent", 9), ev("check", "ent")]
    plan = [pl(1, "todo", "sync", "ent", [fx.ref_l1("hh")])]
    assert lab(False, plan, events, 1, "R", "hh", 5) == "KEEP"
    assert lab(False, plan, events, 2, "V", "kk", 9) == "DROP"


def test_done_step_takes_nothing():
    events = [ev("get", "ent", "hh", 5)]
    plan = [pl(1, "done", "sync", "ent", [fx.ref_l1("hh")]), pl(2, "todo", "sync", "ent", [])]
    assert lab(False, plan, events, 1, "R", "hh", 5) == "DROP"


def test_l2_every_type():
    events = [ev("V", "va", "e1", 1), ev("get", "e2", "vb", 2), ev("D", "vc", "e3", 3), ev("create", "e4", "vd", 4), ev("export", "e5", "/w/x.snap")]
    plan = [pl(1, "todo", "sync", "e1", [fx.ref_l2("V", "e1")]), pl(2, "todo", "sync", "e2", [fx.ref_l2("R", "e2")]),
            pl(3, "todo", "sync", "e3", [fx.ref_l2("D", "e3")]), pl(4, "todo", "sync", "e4", [fx.ref_l2("S", "e4")]),
            pl(5, "todo", "sync", "e5", [fx.ref_l2("P", "e5")])]
    for t, (typ, h, v) in enumerate([("V", "va", 1), ("R", "vb", 2), ("D", "vc", 3), ("S", "vd", 4), ("P", "path", "/w/x.snap")], start=1):
        assert lab(False, plan, events, t, typ, h, v) == "KEEP"
    # the same role words with the wrong type do not reach a fact of another type
    plan2 = [pl(1, "todo", "sync", "e1", [fx.ref_l2("D", "e1")])]
    assert lab(False, plan2, events, 1, "V", "va", 1) == "DROP"


def test_l3_ordinal_counts_get_outputs_only_and_does_not_shift():
    events = [ev("get", "a", "h1", 1), ev("create", "b", "hx", 7), ev("check", "c"), ev("get", "d", "h2", 2), ev("export", "e", "/w/p.snap"),
              ev("read", "e", "/w/p.snap", "hc", 8), ev("get", "f", "h3", 3)]
    plan = [pl(1, "todo", "sync", "f", [fx.ref_l3("third")])]
    assert lab(False, plan, events, 7, "R", "h3", 3) == "KEEP"          # the third get call is turn 7
    assert lab(False, plan, events, 1, "R", "h1", 1) == "DROP"          # removing the first get would shift ordinals; redaction does not
    assert lab(False, plan, events, 4, "R", "h2", 2) == "DROP"
    assert lab(False, plan, events, 2, "S", "hx", 7) == "DROP"          # a create_ output is never counted
    assert lab(False, plan, events, 6, "R", "hc", 8) == "DROP"          # nor a read_ output


def test_l4_pointer_keeps_pointer_drops_content():
    events = [ev("export", "snap", "/w/s.snap"), ev("read", "snap", "/w/s.snap", "body", 99)]
    plan = [pl(1, "todo", "sync", "snap", [fx.ref_ptr("snap")])]
    assert lab(False, plan, events, 1, "P", "path", "/w/s.snap") == "KEEP"
    assert lab(False, plan, events, 2, "R", "body", 99) == "DROP"


def test_l4_chain_follows_the_derived_step():
    events = [ev("get", "a", "ha", 1), ev("get", "b", "hb", 2)]
    plan = [pl(1, "todo", "derive", "a", [fx.ref_l1("ha")]), pl(2, "todo", "sync", "b", [fx.ref_chain(1)])]
    assert lab(False, plan, events, 1, "R", "ha", 1) == "KEEP"
    assert lab(False, plan, events, 2, "R", "hb", 2) == "DROP"
    # the id style 'step s1' is read too
    plan2 = [pl(1, "todo", "derive", "a", [fx.ref_l1("ha")]), pl(2, "todo", "sync", "b", [fx.ref_chain(1, sid_style=True)])]
    assert lab(False, plan2, events, 1, "R", "ha", 1) == "KEEP"
    # a chain to a DONE step needs nothing from the context
    plan3 = [pl(1, "done", "derive", "a", [fx.ref_l1("ha")]), pl(2, "todo", "sync", "b", [fx.ref_chain(1)])]
    assert lab(False, plan3, events, 1, "R", "ha", 1) == "DROP"


def test_supersession_depths_1_2_3():
    for depth in (1, 2, 3):
        events = [ev("create", "ent", "key", 10 + i) for i in range(depth + 1)]
        plan = [pl(1, "todo", "sync", "ent", [fx.ref_l1("key")])]
        for t in range(1, depth + 1):
            assert lab(False, plan, events, t, "S", "key", 10 + t - 1) == "DROP", (depth, t)
        assert lab(False, plan, events, depth + 1, "S", "key", 10 + depth) == "KEEP"


def test_supersession_for_user_values_and_decisions():
    events = [ev("V", "k", "ent", 1), ev("check", "ent"), ev("V", "k", "ent", 2), ev("D", "m", "ent", 3), ev("D", "m", "ent", 4)]
    plan = [pl(1, "todo", "sync", "ent", [fx.ref_l1("k"), fx.ref_l1("m")])]
    assert lab(False, plan, events, 1, "V", "k", 1) == "DROP"
    assert lab(False, plan, events, 3, "V", "k", 2) == "KEEP"
    assert lab(False, plan, events, 4, "D", "m", 3) == "DROP"
    assert lab(False, plan, events, 5, "D", "m", 4) == "KEEP"


def test_same_handle_other_entity_is_a_different_fact():
    events = [ev("V", "k", "e1", 1), ev("V", "k", "e2", 2)]
    plan = [pl(1, "todo", "sync", "e1", [fx.ref_l1("k")])]
    assert lab(False, plan, events, 1, "V", "k", 1) == "KEEP"
    assert lab(False, plan, events, 2, "V", "k", 2) == "DROP"


def test_contingency_steps_follow_the_card():
    events = [ev("V", "k", "ent", 1), ev("get", "x", "h", 2)]
    plan = [pl(1, "todo", "sync", "x", [fx.ref_l1("h")]), pl(2, "todo", "verify", "ent", [fx.ref_l1("k")], host=1)]
    assert lab(True, plan, events, 1, "V", "k", 1) == "KEEP"           # k01: recovery steps count
    assert lab(False, plan, events, 1, "V", "k", 1) == "DROP"          # k02: they do not
    done_host = [pl(1, "done", "sync", "x", [fx.ref_l1("h")]), pl(2, "todo", "verify", "ent", [fx.ref_l1("k")], host=1)]
    assert lab(True, done_host, events, 1, "V", "k", 1) == "DROP"      # a done host cannot fail


def test_reminder_is_the_same_fact_but_a_second_statement_is_not():
    plan = [pl(1, "todo", "sync", "ent", [fx.ref_l1("k")])]
    events = [ev("V", "k", "ent", 7), ev("check", "ent"), ev("M", "k", "ent", 7)]
    assert lab(False, plan, events, 1, "V", "k", 7) == "KEEP"          # the reminder is redacted with it
    events2 = [ev("V", "k", "ent", 7), ev("check", "ent"), ev("V", "k", "ent", 8)]
    assert lab(False, plan, events2, 1, "V", "k", 7) == "DROP"         # a later statement of the same role with a NEW value replaces it
    assert lab(False, plan, events2, 3, "V", "k", 8) == "KEEP"
    # a later statement of the same role with the SAME value is same-value supersession: outside the spec (Opus ruling Q1) -> abstain
    events3 = [ev("V", "k", "ent", 7), ev("check", "ent"), ev("V", "k", "ent", 7)]
    for qt in (1, 3):
        r = hook.solver_b(fx.h2_view(False, plan, events3, qt, "V", "k", 7))
        assert r.abstain and r.reason == "parse_gap:h2_same_value_supersession", (qt, r)


def _assert_abstains(plan, events, qturn, qtype, qh, qv, why):
    view = fx.h2_view(False, plan, events, qturn, qtype, qh, qv)
    r = hook.solver_b(view)
    assert r.abstain and r.label is None and r.letter is None, r
    assert r.reason == "parse_gap:" + why, r.reason
    assert hook.render_b(view) == ("abstain", "parse_gap:" + why)


def test_ruling_q1_same_value_in_a_chain_abstains_at_every_depth_and_position():
    plan = [pl(1, "todo", "sync", "ent", [fx.ref_l1("k")])]
    # depth 1: A -> A
    _assert_abstains(plan, [ev("V", "k", "ent", 5), ev("V", "k", "ent", 5)], 1, "V", "k", 5, "h2_same_value_supersession")
    # depth 2: A -> B -> A (not adjacent) and A -> A -> B (adjacent), quoted fact anywhere in the chain
    for vals in ((5, 6, 5), (5, 5, 6), (6, 5, 5)):
        events = [ev("V", "k", "ent", v) for v in vals]
        for qt in (1, 2, 3):
            _assert_abstains(plan, events, qt, "V", "k", vals[qt - 1], "h2_same_value_supersession")
    # depth 3: A -> B -> C -> A
    events = [ev("create", "ent", "k", v) for v in (11, 12, 13, 11)]
    for qt in (1, 2, 3, 4):
        _assert_abstains(plan, events, qt, "S", "k", (11, 12, 13, 11)[qt - 1], "h2_same_value_supersession")
    # decisions and tool results chains too
    _assert_abstains([pl(1, "todo", "sync", "ent", [fx.ref_l1("m")])], [ev("D", "m", "ent", 3), ev("D", "m", "ent", 4), ev("D", "m", "ent", 3)],
                     2, "D", "m", 4, "h2_same_value_supersession")
    _assert_abstains([pl(1, "todo", "sync", "ent", [fx.ref_l1("h")])], [ev("get", "ent", "h", 9), ev("check", "ent"), ev("get", "ent", "h", 9)],
                     3, "R", "h", 9, "h2_same_value_supersession")
    # one value stated in two ways (user statement and a tool result of the same handle and entity) is the same chain
    _assert_abstains(plan, [ev("V", "k", "ent", 5), ev("create", "ent", "k", 5)], 1, "V", "k", 5, "h2_same_value_supersession")


def test_ruling_q1_a_repeated_value_in_another_chain_still_abstains_when_the_quote_is_elsewhere():
    plan = [pl(1, "todo", "sync", "e1", [fx.ref_l1("k")]), pl(2, "todo", "sync", "e2", [fx.ref_l1("m")])]
    events = [ev("V", "k", "e1", 1), ev("V", "m", "e2", 4), ev("V", "m", "e2", 4)]
    _assert_abstains(plan, events, 1, "V", "k", 1, "h2_same_value_supersession")


def test_ruling_q1_distinct_values_and_same_value_in_other_roles_still_label():
    plan = [pl(1, "todo", "sync", "e1", [fx.ref_l1("k")]), pl(2, "todo", "sync", "e2", [fx.ref_l1("k")])]
    # pairwise distinct chain: labelled as before
    chain = [ev("V", "k", "e1", 1), ev("V", "k", "e1", 2), ev("V", "k", "e1", 3), ev("V", "k", "e1", 4)]
    assert lab(False, plan, chain, 1, "V", "k", 1) == "DROP" and lab(False, plan, chain, 4, "V", "k", 4) == "KEEP"
    # the same value under another entity or another handle is a different role, not a chain
    assert lab(False, plan, [ev("V", "k", "e1", 7), ev("V", "k", "e2", 7)], 1, "V", "k", 7) == "KEEP"
    plan_h = [pl(1, "todo", "sync", "e1", [fx.ref_l1("k"), fx.ref_l1("m")])]
    assert lab(False, plan_h, [ev("V", "k", "e1", 7), ev("V", "m", "e1", 7)], 2, "V", "m", 7) == "KEEP"


def test_ruling_q1_repeat_marker_on_a_supersession_chain_abstains():
    plan = [pl(1, "todo", "sync", "ent", [fx.ref_l1("k")])]
    # a reminder of an OLD value after its revision, and of the latest value: both repeat a value inside a chain
    for rem in (5, 6):
        _assert_abstains(plan, [ev("V", "k", "ent", 5), ev("V", "k", "ent", 6), ev("M", "k", "ent", rem)], 2, "V", "k", 6,
                         "h2_repeat_marker_in_supersession_chain")
    # a reminder of a fact that has no revision is still the same fact seen again (mark.t60.repeat), and is labelled as before
    assert lab(False, plan, [ev("V", "k", "ent", 5), ev("check", "ent"), ev("M", "k", "ent", 5)], 1, "V", "k", 5) == "KEEP"


def test_emphasis_text_is_not_part_of_the_value():
    events = [ev("V", "k", "ent", 5, "a striking value"), ev("D", "m", "ent", 6, "a notable value"), ev("get", "ent", "h", "gat-1", "a remarkable value")]
    plan = [pl(1, "todo", "sync", "ent", [fx.ref_l1("k"), fx.ref_l1("m"), fx.ref_l1("h")])]
    assert lab(False, plan, events, 1, "V", "k", 5) == "KEEP"
    assert lab(False, plan, events, 2, "D", "m", 6) == "KEEP"
    assert lab(False, plan, events, 3, "R", "h", "gat-1") == "KEEP"


def test_two_references_in_one_step():
    events = [ev("get", "ent", "ha", 1), ev("get", "ent", "hb", 2), ev("get", "ent", "hc", 3)]
    plan = [pl(1, "todo", "sync", "ent", [fx.ref_l1("ha"), fx.ref_l3("second")])]
    assert lab(False, plan, events, 1, "R", "ha", 1) == "KEEP"
    assert lab(False, plan, events, 2, "R", "hb", 2) == "KEEP"
    assert lab(False, plan, events, 3, "R", "hc", 3) == "DROP"


def test_quote_must_match_the_transcript_or_b_abstains():
    events = [ev("get", "ent", "hh", 5)]
    plan = [pl(1, "todo", "sync", "ent", [fx.ref_l1("hh")])]
    for qturn, qtype, qh, qv in ((2, "R", "hh", 5), (1, "R", "hh", 6), (1, "V", "hh", 5), (1, "R", "zz", 5)):
        r = hook.solver_b(fx.h2_view(False, plan, events, qturn, qtype, qh, qv))
        assert r.abstain, (qturn, qtype, qh, qv)


def test_unknown_shapes_abstain():
    events = [ev("get", "ent", "hh", 5)]
    bad_ref = [pl(1, "todo", "sync", "ent", ["the third mention of the thing"])]
    assert hook.solver_b(fx.h2_view(False, bad_ref, events, 1, "R", "hh", 5)).abstain
    odd_user = [["User: Please remember that the answer is 4."]] + events
    plan = [pl(1, "todo", "sync", "ent", [fx.ref_l1("hh")])]
    assert hook.solver_b(fx.h2_view(False, plan, odd_user, 2, "R", "hh", 5)).abstain
    no_card = fx.h2_context(False, plan, events, 1, "R", "hh", 5).replace("A step that runs only on failure", "A step that runs on a Tuesday").replace("(rollback, retry, read-back) ", "")
    assert hook.solver_b(fx.view("h2", no_card, fx.H2_OPTS, fx.H2_Q)).abstain


def test_counts_recovery_wording_variants():
    pool = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "pools", "wording_pool_v1.json")))
    for s in pool["clause.k_recover_on"]:
        assert h2.parse_counts_recovery(["x", "Keep a fact.", s]) is True, s
    for s in pool["clause.k_recover_off"]:
        assert h2.parse_counts_recovery(["x", "Keep a fact.", s]) is False, s


def test_coverage_helper_reports_resolved_references():
    events = [ev("get", "ent", "hh", 5), ev("export", "q", "/w/a")]
    plan = [pl(1, "todo", "sync", "ent", [fx.ref_l1("hh"), fx.ref_l3("first")]), pl(2, "todo", "sync", "q", [fx.ref_ptr("q"), fx.ref_l2("D", "nobody")])]
    ctx = fx.h2_context(False, plan, events, 1, "R", "hh", 5)
    tot, res, by = h2.coverage(ctx)
    assert (tot, res) == (4, 3) and by["L2"] == [1, 0]


# ----------------------------------------------------------------------------------------------------------------------
# randomised cross product against a pointer-based oracle (spec side)
# ----------------------------------------------------------------------------------------------------------------------
WORDS = ["baro", "delu", "fikan", "gomi", "hepa", "jura", "kelo", "limbu", "morda", "nesi", "ofar", "pudi", "quen", "rasto", "sulo", "tavi"]
HANDLES = ["hdl%02d" % i for i in range(40)]


def make_spec(rng):
    ents = rng.sample(WORDS, 5)
    facts = []                                            # id, kind, handle, entity, value
    used_role = set()
    k = 0

    def add(kind, ent, handle=None):
        nonlocal k
        k += 1
        h = "path" if kind == "export" else (handle or HANDLES[k])
        facts.append({"id": k, "kind": kind, "handle": h, "entity": ent, "value": ("/w/%d.snap" % k) if kind == "export" else str(100 + k)})
        return facts[-1]

    for ent in ents[:4]:
        for kind in rng.sample(["V", "D", "get", "create", "export"], rng.randint(1, 3)):
            if (kind, ent) in used_role:
                continue
            used_role.add((kind, ent))
            add(kind, ent)
    # superseding statements (same handle and entity, later)
    for f in list(facts):
        if f["kind"] in ("V", "D", "create", "get") and rng.random() < 0.4:
            g = add(f["kind"], f["entity"], f["handle"])
    return facts


KIND_TYPE = {"V": "V", "D": "D", "get": "R", "create": "S", "export": "P"}


def render_events(facts, rng):
    evs, turn_of = [], {}
    order = list(facts)                                   # transcript order = id order (supersessions come later)
    for f in order:
        k = f["kind"]
        if k in ("V", "D"):
            evs.append(ev(k, f["handle"], f["entity"], f["value"]))
        elif k in ("get", "create"):
            evs.append(ev(k, f["entity"], f["handle"], f["value"]))
        else:
            evs.append(ev("export", f["entity"], f["value"]))
        turn_of[f["id"]] = len(evs)
        if rng.random() < 0.3:
            evs.append(ev("check", "zed"))
    return evs, turn_of


def oracle(facts, plan, counts, quote_id):
    """Pointer based: every ref names its target by the spec; resolution to the latest same (handle, entity); chain = needs of the step."""
    latest = {}
    for f in facts:
        if f["kind"] != "export":
            latest[(f["handle"], f["entity"])] = f["id"]
    by_id = {f["id"]: f for f in facts}

    def run(s):
        if s["status"] != "todo":
            return False
        if s["host"] is None:
            return True
        return counts and run(plan[s["host"] - 1])

    def needs(s, seen=()):
        out = set()
        for r in s["refs"]:
            if r[0] == "fact":
                t = by_id[r[1]]
                out.add(latest.get((t["handle"], t["entity"]), t["id"]) if t["kind"] != "export" else t["id"])
            elif r[0] == "chain":
                tgt = plan[r[1] - 1]
                if tgt["status"] == "todo" and r[1] not in seen:
                    out |= needs(tgt, seen + (r[1],))
        return out

    want = set()
    for s in plan:
        if run(s):
            want |= needs(s)
    return "KEEP" if quote_id in want else "DROP"


def make_plan(rng, facts):
    n = rng.randint(3, 7)
    plan = []
    get_facts = [f for f in facts if f["kind"] == "get"]
    for i in range(1, n + 1):
        status = rng.choice(["todo", "todo", "todo", "done"])
        host = None
        if i > 1 and rng.random() < 0.25 and plan[rng.randrange(len(plan))]["status"] == "todo":
            host = rng.randint(1, i - 1)
        refs, texts = [], []
        for _ in range(rng.choice([0, 1, 1, 2])):
            f = rng.choice(facts)
            lv = rng.choice([1, 1, 2, 3, 4])
            if lv == 4 and f["kind"] == "export":
                refs.append(("fact", f["id"]))
                texts.append(fx.ref_ptr(f["entity"]))
            elif lv == 4 and i > 1:
                j = rng.randint(1, i - 1)
                refs.append(("chain", j))
                texts.append(fx.ref_chain(j, sid_style=rng.random() < 0.5))
            elif lv == 3 and f["kind"] == "get":
                refs.append(("fact", f["id"]))
                texts.append(fx.ref_l3(h2.ORDINALS[get_facts.index(f)]))
            elif lv == 2 and f["kind"] != "get" or (lv == 2 and f["kind"] == "get"):
                refs.append(("fact", f["id"]))
                texts.append(fx.ref_l2(KIND_TYPE[f["kind"]], f["entity"]))
            else:
                if f["kind"] == "export":
                    refs.append(("fact", f["id"]))
                    texts.append(fx.ref_ptr(f["entity"]))
                else:
                    refs.append(("fact", f["id"]))
                    texts.append(fx.ref_l1(f["handle"]))
        by_id = {f["id"]: f for f in facts}
        ent = by_id[[r for r in refs if r[0] == "fact"][0][1]]["entity"] if any(r[0] == "fact" for r in refs) else rng.choice(WORDS[8:])
        plan.append({"status": status, "host": host, "refs": refs, "texts": texts, "entity": ent})
    return plan


def unique_roles(facts, plan):
    """L2 references must name one fact: drop the plan if two facts share (type, entity) with different handles, or an L2 ref hits a
    superseded fact (the oracle and the grammar then disagree on purpose: L2 means 'the' value of that role)."""
    roles = {}
    for f in facts:
        roles.setdefault((KIND_TYPE[f["kind"]], f["entity"]), set()).add(f["handle"])
    return all(len(v) == 1 for v in roles.values())


def test_randomised_cross_product_against_pointer_oracle():
    rng = random.Random(60606)
    n_checked = n_keep = 0
    for _ in range(2500):
        facts = make_spec(rng)
        if not unique_roles(facts, None):
            continue
        plan = make_plan(rng, facts)
        # a spec-level pointer to a superseded fact through L2/L3/L4: the grammar resolves by role, so point at the latest one
        evs, turn_of = render_events(facts, rng)
        counts = rng.random() < 0.5
        plan_lines = []
        for i, s in enumerate(plan, start=1):
            plan_lines.append(pl(i, s["status"], "sync", s["entity"], s["texts"], host=s["host"]))
        # a reference that lands on a superseded fact (through a role description, an ordinal or a pointer text) takes the CURRENT value of that
        # role (G0-lite 3.4: a superseded fact is not needed, the current value is); the oracle replaces every target by the latest same-role fact
        q = rng.choice(facts)
        qtype = KIND_TYPE[q["kind"]]
        view = fx.h2_view(counts, plan_lines, evs, turn_of[q["id"]], qtype, q["handle"], q["value"])
        res = hook.solver_b(view)
        assert not res.abstain, res.reason
        want = oracle(facts, plan, counts, q["id"])
        assert res.label == want, (counts, plan_lines, q)
        n_checked += 1
        n_keep += res.label == "KEEP"
    assert n_checked > 800 and 0.15 < n_keep / n_checked < 0.85
