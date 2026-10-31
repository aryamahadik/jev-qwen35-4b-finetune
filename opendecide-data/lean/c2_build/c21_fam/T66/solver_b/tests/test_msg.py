import pytest

from T66.solver_b import msg_b, msg_diff, msg_lex, textparse as tp
from helpers import diff_of, msg_ctx

BASE_LINES = " def fa(x):\n     y = x\n     y = y * 3\n     return y\n"


def mk(old, new):
    """a one-hunk diff replacing the line(s) `old` by `new` inside a small function"""
    body = ""
    for ln in BASE_LINES.rstrip("\n").split("\n"):
        if old and ln.strip() == old[0].strip():
            body += "".join("-%s\n" % o for o in old) + "".join("+%s\n" % n for n in new)
        else:
            body += ln + "\n"
    return diff_of(body)


def kind(diff):
    d = msg_diff.analyse(diff)
    return d["kind"] if d["ok"] else "?" + d["why"]


def test_diff_kinds_per_change_class():
    g = "def fa(x):\n    y = x\n"
    assert kind(diff_of(" def fa(x):\n     y = x\n+    if y < 0:\n+        raise ValueError(\"bad\")\n     y = y * 3\n     return y\n")) == "CH-1"
    assert kind(diff_of(" def fa(x):\n-    for i in range(x):\n+    for i in range(x + 1):\n         y = i\n")) == "CH-2"
    assert kind(diff_of(" x = 1\n-    if y < 3:\n+    if y <= 3:\n     return y\n")) == "CH-2"
    assert kind(diff_of("-def fa(x):\n+def fb(x):\n     y = x\n")) == "CH-3"
    assert kind(diff_of("-def fa(x, k=1):\n+def fa(x, k=2):\n     y = x\n")) == "CH-5"
    assert kind(diff_of("-def fa(x):\n+def fa(x, k):\n     y = x\n")) == "CH-6"
    assert kind(diff_of("-        raise ValueError(\"old\")\n+        raise ValueError(\"new\")\n")) == "CH-8"
    assert kind(diff_of("     y = x\n+    log.append(\"seen\")\n     return y\n")) == "CH-9"
    assert kind(diff_of("     y = x\n-    y = y * 3\n+    y = y * 4\n     return y\n")) == "CH-10"


def test_default_removed_has_alternative_reading():
    d = msg_diff.analyse(diff_of("-def fa(x, k=1):\n+def fa(x, k):\n     y = x\n"))
    assert d["kind"] == "CH-6" and d["alt"] == ("CH-5",)


def test_trivial_edits_have_no_behavioural_unit():
    for body in ("-    y = y * 3\n+    y=y*3\n", "+# a comment\n     y = x\n", " def fa(x):\n+    \"\"\"docstring\"\"\"\n     y = x\n"):
        d = msg_diff.analyse(diff_of(body))
        assert not d["ok"] and d["why"] == "no behavioural unit"


def test_trivial_hunks_do_not_hide_the_behavioural_one():
    body = "+# note\n-    y = y * 3\n+    y = y * 4\n-    z = z + 1\n+    z=z+1\n"
    assert kind(diff_of(body)) == "CH-10"


def test_multiline_docstring_lines_are_trivial():
    body = " def fa(x):\n-    \"\"\"first line\n-    second line\"\"\"\n+    \"\"\"first line\n+    second, reworded\"\"\"\n     y = x\n"
    d = msg_diff.analyse(diff_of(body))
    assert not d["ok"] and d["why"] == "no behavioural unit"


def test_two_behavioural_kinds_abstain():
    body = "-def fa(x, k=1):\n+def fa(x, k=2):\n-    y = y * 3\n+    y = y * 4\n"
    assert not msg_diff.analyse(diff_of(body))["ok"]


def test_diff_parser_errors():
    with pytest.raises(tp.ParseError):
        tp.parse_diff("not a diff")
    assert len(tp.parse_diff(diff_of("-a\n+b\n"))) == 1


MESSAGES = {
    "CH-1": ["Add a guard that rejects negative input in fa", "fa now raises ValueError when x is None", "Validate the argument before fa does any work"],
    "CH-2": ["Fix off-by-one in the loop bound of fa", "fa skipped the last item, now included", "Use <= instead of < in the boundary check"],
    "CH-3": ["Rename fa to something clearer", "fa renamed to match what it does", "Give fa a better name"],
    "CH-5": ["Change the default of the k parameter in fa", "fa now defaults k to 2", "Default k to False when it is not passed"],
    "CH-6": ["fa takes an extra k parameter now", "Add a required argument to fa", "fa now requires the k argument"],
    "CH-8": ["Reword the error message raised by fa", "Make the error text in fa clearer", "fa now reports bad input with a friendlier error string"],
    "CH-9": ["Add logging to fa", "fa now logs each value it receives", "Emit a debug trace line in fa"],
    "CH-10": ["Change the multiplier constant in fa from 3 to 4", "Raise the limit in fa from 100 to 250", "Tweak the scaling factor in fa"],
    "TRIV-fmt": ["Reformat fa to fix spacing", "Whitespace cleanup in fa", "Tidy the layout of fa"],
    "TRIV-comment": ["Add a comment to fa", "Fix a stale comment in fa", "Add a TODO note in fa"],
    "TRIV-doc": ["Update the fa docstring", "Expand the docstring of fa", "Docstring wording for fa"],
}


@pytest.mark.parametrize("want,msgs", sorted(MESSAGES.items()))
def test_message_kind_lexicon(want, msgs):
    for m in msgs:
        got, sc = msg_lex.classify(m, ["fa"], min_top=3, min_margin=2)          # cue coverage at the loose setting
        assert got == want, (m, sorted(sc.items(), key=lambda kv: -kv[1])[:3])


def test_message_identifiers_are_removed_before_matching():
    sc = msg_lex.scores("Touch the renamer zone", ["renamer"])
    assert sc["CH-3"] == 0                                     # the word is an identifier of the diff, not a verb


DIFFS = {
    "CH-1": " def fa(x):\n     y = x\n+    if y < 0:\n+        raise ValueError(\"bad\")\n     return y\n",
    "CH-2": " def fa(x):\n-    for i in range(x):\n+    for i in range(x + 1):\n         y = i\n",
    "CH-3": "-def fa(x):\n+def fb(x):\n     y = x\n",
    "CH-5": "-def fa(x, k=1):\n+def fa(x, k=2):\n     y = x\n",
    "CH-8": "-        raise ValueError(\"old\")\n+        raise ValueError(\"new\")\n",
    "CH-9": "     y = x\n+    log.append(\"seen\")\n     return y\n",
    "CH-10": "     y = x\n-    y = y * 3\n+    y = y * 4\n     return y\n",
}


def test_truth_table_diff_kind_by_message_kind(monkeypatch):
    """YES iff the message kind is the diff kind; any other behavioural kind or a trivial kind is NO (the affinity pairs abstain). Loose thresholds: cue coverage."""
    monkeypatch.setattr(msg_lex, "MIN_TOP", 3)
    monkeypatch.setattr(msg_lex, "MIN_MARGIN", 2)
    for dk, body in DIFFS.items():
        for mk_, msgs in MESSAGES.items():
            label, why = msg_b.solve(msg_ctx(diff_of(body), msgs[0]))
            if mk_ == dk:
                assert label == "YES", (dk, mk_, why)
            elif mk_ in msg_b.AFFINITY.get(dk, ()):
                assert label is None
            else:
                assert label == "NO", (dk, mk_, why)


def test_unknown_message_abstains():
    assert msg_b.solve(msg_ctx(diff_of(DIFFS["CH-10"]), "Misc updates"))[0] is None


def test_trivial_only_diff_cannot_be_decided():
    label, why = msg_b.solve(msg_ctx(diff_of("-    y = y * 3\n+    y=y*3\n"), "Reformat fa"))
    assert label is None and "diff" in why


def test_section_errors_abstain():
    assert msg_b.solve("Definitions only")[0] is None


def test_strict_default_abstains_on_mixed_messages_and_decides_clear_ones():
    clear = msg_ctx(diff_of(DIFFS["CH-10"]), "Change the multiplier constant in fa from 3 to 4")
    assert msg_b.solve(clear) == ("YES", "same kind")
    mixed = msg_ctx(diff_of(DIFFS["CH-1"]), "Tracing the stack is simpler since fa asks for it")       # trace (logging) vs asks for (parameter)
    assert msg_b.solve(mixed)[0] is None
    assert (msg_lex.MIN_TOP, msg_lex.MIN_MARGIN) == (5, 4)
