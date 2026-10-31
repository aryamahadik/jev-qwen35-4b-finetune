"""PREREG Ruling A32 (c): the A31 (b) render-check boundary fix in decontam_g13.py. Synthetic fixtures only (tmp
files); no real eval or training file is read.

An edge word of a piece that touches a placeholder, an f-string value, a `+` operand or a %-format match with no space
between is dropped (the value glues onto it when rendered: '{n}th' -> '5th'); the bare %-spec has no space flag, so
prose like '50% sure' is not a format spec; a literal with no piece of >= 2 words left is unprovable (binds).
"""
import sys
from pathlib import Path

CB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CB))
import decontam_g13 as g  # noqa: E402

FAM = "F3"                                          # a family set: its training rows are its own non-seed units


def _status(literal: str, row: str) -> str:
    """seed_render status of one hit literal against one training row of a family set."""
    assert FAM not in g.SEED_SETS
    units = [{"key": "row:1", "seed": False, "texts": [("state", row)]}]
    st, _ = g.seed_render({FAM: {"k": literal}}, {FAM: units})
    return st[FAM]["k"]


def _old_pieces(raw: str):
    """The pre-A32 seed_pieces (plain split, space in the bare %-spec flags), to show the flaw the fix removes."""
    old = g.re.compile(r"\{[^{}]*\}|%\(\w+\)[#0 +-]*\d*(?:\.\d+)?[A-Za-z]|%[#0 +-]*\d*(?:\.\d+)?[sdifrxXeEgGc]"
                       r"|\$\{?\w+\}?|\n")
    return sorted({" " + " ".join(ws) + " " for p in old.split(raw) for ws in [g.words(p)] if len(ws) >= 2}) or None


def test_percent_prose_is_not_a_format_spec():
    lit = "50% sure of the answer here"
    assert _old_pieces(lit) == [" ure of the answer here "]                    # the flaw: '% s' read as a spec
    assert g.seed_pieces(lit) == [" 50 sure of the answer here "]
    assert _status(lit, "I am 50% sure of the answer here, said the clerk.") == "rendered"
    for lit in ("Over 50% did agree with the plan", "About 10% chance of rain by the evening"):
        assert g.seed_pieces(lit) == [" " + " ".join(g.words(lit)) + " "]
        assert _status(lit, f"Note: {lit}.") == "rendered"
    assert _status("50% sure of the answer here", "Nothing like it is in this row at all.") == "not_rendered"


def test_placeholder_touching_word_is_dropped():
    lit = "The {n}th place goes to the runner"
    assert _old_pieces(lit) == [" th place goes to the runner "]                 # never in '... 5th place ...'
    assert g.seed_pieces(lit) == [" place goes to the runner "]
    assert _status(lit, "The 5th place goes to the runner from the north.") == "rendered"
    assert _status(lit, "A row about something else entirely here.") == "not_rendered"
    assert g.seed_pieces("Read {a}bc de{f} now") is None                         # both edge words dropped: none left
    assert g.seed_pieces("Word{x} then two more{y}") == [" then two "]
    assert g.seed_pieces("Cost ${amount}k was paid in full") == [" was paid in full "]
    assert g.seed_pieces("Is it {x} true\nthat %s or %(b)s holds here") == [" holds here ", " is it "]   # A31 kept
    assert _status("The {n}th place", "The 5th place") == "unprovable"           # < 2 words left: binds


def test_percent_spec_touching_word_is_dropped():
    lit = "Rank %dth among the many runners"
    assert g.seed_pieces(lit) == [" among the many runners ", ]
    assert _status(lit, "Rank 3th among the many runners today.") == "rendered"
    lit = "Score %(pts)spts out of the ten given"
    assert g.seed_pieces(lit) == [" out of the ten given ", ]
    assert _status(lit, "Score 7pts out of the ten given.") == "rendered"
    assert g.seed_pieces("Took %5.2fs to finish the whole job") == [" to finish the whole job "]
    assert g.seed_pieces("Took %5.2f s to finish") == [" s to finish "]   # spaced: nothing glues


def test_fstring_value_edge(tmp_path):
    src = ('A = f"The {n}th place goes to the runner"\n'
           'B = "The " + str(n) + "th lap ends at the gate"\n'
           'C = f"{x} drifts on the evening tide"\n'
           'D = "A plain literal with no join here"\n'
           's = ""\n'
           's += "nd row of the long table"\n')
    lits = g.py_literals_at(src, marked=True)
    assert [t for t, _ in g.py_literals_at(src)] == [t for t, _, _ in lits]   # literal texts and order unchanged
    rt = {t: r for t, _, r in lits}
    assert rt["th place goes to the runner"] == "{}th place goes to the runner"
    assert rt["th lap ends at the gate"] == "{}th lap ends at the gate"
    assert rt["The "] == "The {}"
    assert rt[" drifts on the evening tide"] == "{} drifts on the evening tide"
    assert rt["A plain literal with no join here"] == "A plain literal with no join here"
    assert rt["nd row of the long table"] == "{}nd row of the long table"
    assert g.seed_pieces(rt["th place goes to the runner"]) == [" place goes to the runner "]
    assert g.seed_pieces(rt[" drifts on the evening tide"]) == [" drifts on the evening tide "]   # space: kept

    gen = tmp_path / "lean" / "c_src" / FAM / "gen"
    gen.mkdir(parents=True)
    (gen / "t.py").write_text(src)
    units, _ = g.seed_units(gen, tmp_path / "lean")
    by_text = {u["texts"][0][1]: u for u in units}
    assert by_text["th place goes to the runner"]["render_text"] == "{}th place goes to the runner"
    assert "render_text" not in by_text["A plain literal with no join here"]
    rows = [{"key": "row:1", "rows": [], "seed": False,
             "texts": [("state", "The 5th place goes to the runner. The 2th lap ends at the gate.")]}]
    keys = [by_text[t]["key"] for t in ("th place goes to the runner", "th lap ends at the gate",
                                         "A plain literal with no join here", "nd row of the long table")]
    by_key = {FAM: {u["key"]: u for u in units + rows}}
    hbs = {FAM: {"lab": {"m": {"s": keys}}}}
    g.seed_render_annotate(hbs, by_key)
    got = [by_key[FAM][k]["render"] for k in keys]
    assert got == ["rendered", "rendered", "not_rendered", "not_rendered"]
