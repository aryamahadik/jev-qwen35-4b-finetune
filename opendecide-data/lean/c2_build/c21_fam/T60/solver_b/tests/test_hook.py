"""Plug points: result shape, option text -> label for every pool wording, letters, render_b, abstain paths."""
import json
import os

import fixtures as fx
import hook
import t60b_text as tx

POOL = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "pools", "wording_pool_v1.json")


def test_result_has_the_attributes_the_pipeline_reads():
    r = hook.solver_b(fx.h1_view(3, 100, 2, 400, 3, 0, 0, 100))
    assert (r.label, r.letter, r.abstain) == ("DELEGATE", "A", False) and hasattr(r, "reason")
    kind, val = hook.render_b(fx.h1_view(3, 100, 2, 400, 3, 0, 0, 100))[:2]
    assert (kind, val) == ("letter", "A")
    kind, val = hook.render_b(fx.h1_view(3, 100, 2, 400, 3, 0, 0, 100, order=(1, 0)))[:2]
    assert (kind, val) == ("letter", "B")


def test_every_pool_option_wording_is_classified():
    pool = json.load(open(POOL))
    want = {"h1": ("DELEGATE", "DO_HERE"), "h2": ("KEEP", "DROP"), "h3": ("PLAN", "ACT")}
    n = 0
    for head, labs in want.items():
        for lab in labs:
            for t in pool["opt." + lab]:
                assert tx.classify_option(head, t) == lab, (head, lab, t)
                n += 1
    assert n >= 25


def test_every_pool_question_wording_names_its_head():
    pool = json.load(open(POOL))
    for head in ("h1", "h2", "h3"):
        for q in pool["q." + head]:
            assert tx.head_from_question("Question: " + q) == head, q


def test_letter_comes_from_option_text_not_from_the_label_field():
    v = fx.h1_view(3, 100, 2, 400, 3, 0, 0, 100)
    for o in v["options"]:
        o["label"] = "DO_HERE"                                    # a lying label field must change nothing
    assert hook.solver_b(v).letter == "A"
    v2 = fx.h1_view(3, 100, 2, 400, 3, 0, 0, 100)
    v2["options"][0]["text"], v2["options"][1]["text"] = v2["options"][1]["text"], v2["options"][0]["text"]
    assert hook.solver_b(v2).letter == "B"


def test_render_b_reads_the_rendered_option_lines():
    v = fx.h3_view(5, 3, [("rename the item a-1", 9, "cannot be undone")] * 3, order=[], flow=[(1, 2)], opt_order=(1, 0))
    assert hook.solver_b(v).label == "PLAN" and hook.render_b(v) == ("letter", "B")
    v["rendered"]["options_text"] = "A) Write out a plan before acting\nB) Act now without a plan"
    assert hook.render_b(v) == ("letter", "A")                    # a rendered text that disagrees with the options list shows up here


def test_abstain_paths_never_guess():
    v = fx.h1_view(3, 100, 2, 400, 3, 0, 0, 100)
    bad = dict(v, options=[{"letter": "A", "label": "x", "text": "Do something else"}, v["options"][1]])
    r = hook.solver_b(bad)
    assert r.abstain and r.label is None and r.reason
    assert hook.render_b(dict(v, rendered=dict(v["rendered"], options_text="no options here")))[0] == "abstain"
    assert hook.solver_b({"family": "T60"}).abstain
    assert hook.solver_b(dict(v, sub_block="h3")).abstain         # the head in the view must agree with the text
    v2 = dict(v, rendered=dict(v["rendered"], question="Question: What is the weather?", context="nothing"))
    assert hook.solver_b(v2).abstain


def test_two_options_with_the_same_meaning_abstain():
    v = fx.h2_view(False, [fx.plan_line(1, "todo", "sync", "e", [])], [fx.ev("get", "e", "h", 1)], 1, "R", "h", 1)
    v["options"][1]["text"] = "Keep this fact in the summary"
    assert hook.solver_b(v).abstain


def test_parse_view_exposes_the_recovered_facts():
    v = fx.h3_view(5, 3, [("rename the item a-1", 9, "cannot be undone")] * 3, order=[(1, 2)], flow=[(1, 2), (2, 3)])
    out = hook.parse_view(v)
    assert out["head"] == "h3" and out["label"] == "PLAN"
    assert out["parsed"]["order"] == [("s1", "s2")] and out["parsed"]["flow"] == [("s1", "s2"), ("s2", "s3")]
    assert out["parsed"]["card"] == {"H": 5, "n": 3}
