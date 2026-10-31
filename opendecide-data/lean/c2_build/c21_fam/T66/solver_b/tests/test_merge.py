import pytest

from T66.solver_b import merge_b, textparse as tp
from helpers import merge_ctx

BASE = "def pa(x):\n    return x + 1\n\n\ndef pb(x):\n    return x * 2\n"
VIEW = ("def pa(x):\n    return x + 1\n\n\n<<<<<<< ours\ndef pb(x):\n    return x * 3\n||||||| base\ndef pb(x):\n    return x * 2\n=======\n"
        "def pb(x):\n    return x * 2\n\n\ndef pc(x):\n    return x - 1\n>>>>>>> theirs\n")
TA = "from m import pb\n\ndef test_a_1():\n    assert pb(2) == 6\n"
TB = "from m import pc\n\ndef test_b_1():\n    assert pc(2) == 1\n"
REF = "def pa(x):\n    return x + 1\n\n\ndef pb(x):\n    return x * 3\n\n\ndef pc(x):\n    return x - 1\n"


def solve(res, ta=TA, tb=TB, view=VIEW, stem="m"):
    return merge_b.solve(merge_ctx(stem, view, ta, tb, res))


def test_reference_is_yes():
    assert solve(REF)[0] == "YES"


def test_truth_table_two_suites():
    only_a = REF.replace("\n\ndef pc(x):\n    return x - 1\n", "\n")          # side B lost
    only_b = REF.replace("x * 3", "x * 2")                                        # side A lost
    neither = BASE
    assert solve(REF)[0] == "YES"
    assert solve(only_a)[0] == "NO"
    assert solve(only_b)[0] == "NO"
    assert solve(neither)[0] == "NO"


def test_marker_residue_is_no():
    res = REF.replace("def pa", "<<<<<<< ours\ndef pa")
    label, why = solve(res)
    assert (label, why) == ("NO", "marker residue")


def test_syntax_break_is_no():
    label, why = solve(REF.replace("def pc(x):", "def pc(x)"))
    assert label == "NO" and "parse" in why


def test_semantic_break_that_parses_is_no():
    assert solve(REF.replace("x - 1", "x + 1"))[0] == "NO"


def test_duplicate_definition_last_wins_like_python():
    dup = REF + "\n\ndef pb(x):\n    return x * 2\n"
    assert solve(dup)[0] == "NO"                      # the later definition shadows the first: suite A fails


def test_wrong_order_through_state_dependency():
    view = VIEW
    ta = "from m import out\n\ndef test_a_1():\n    assert out[0] == 'a'\n"
    tb = "from m import out\n\ndef test_b_1():\n    assert out[1] == 'b'\n"
    good = "out = []\nout.append('a')\nout.append('b')\n"
    bad = "out = []\nout.append('b')\nout.append('a')\n"
    assert merge_b.solve(merge_ctx("m", view, ta, tb, good))[0] == "YES"
    assert merge_b.solve(merge_ctx("m", view, ta, tb, bad))[0] == "NO"


def test_runtime_error_in_module_body_is_no():
    assert solve(REF + "\nboom = undefined_name\n")[0] == "NO"


def test_unsupported_construct_abstains():
    label, why = solve(REF + "\nimport os\n")
    assert label is None and why.startswith("unsupported")


def test_malformed_sections_abstain():
    assert merge_b.solve("Definitions only")[0] is None
    assert solve(REF, view="no markers here\n")[0] is None


def test_stem_mismatch_abstains():
    ctx = merge_ctx("m", VIEW, TA, TB, REF).replace("Proposed resolution of m.py", "Proposed resolution of other.py")
    assert merge_b.solve(ctx)[0] is None


def test_conflict_view_parser_hunks():
    n, hunks = merge_b.parse_conflict_view(VIEW)
    assert len(hunks) == 1 and n > 0
    assert hunks[0].ours[0].startswith("def pb") and "pc" in "\n".join(hunks[0].theirs) and hunks[0].base == ["def pb(x):", "    return x * 2"]
    with pytest.raises(tp.ParseError):
        merge_b.parse_conflict_view("<<<<<<< ours\nx\n")
