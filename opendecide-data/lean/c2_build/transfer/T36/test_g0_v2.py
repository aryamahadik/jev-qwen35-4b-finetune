"""transfer/T36/test_g0_v2.py: in-memory tests for the G0 v2 resolutions (Haiku pass amb:T36, H1-H33). No file is
written; no Haiku, no network.

  cards        plugin and solver-B copies equal; inside / outside and the resolver's pick printed (H4, H5)
  hand gold    gate cases worked out by hand from G0 R4, R7, R9 (H2, H3, H4, H11); both solvers
  never        R3, R5, R6, R8 forms never generated (H2, H14, H17-H20)
  options      ch_pick k = the plan's k (option_count(row key)), never lowered; None shown on every ch_pick row (H6, H7)
  packs        check_pack; one pack per card; S5 held-out packs (R19)
  balance      one meets / one does not in every all-yes/no block (H22); ch_pick twins keep the list size (H25)
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/transfer/T36
"""
from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import gsl  # noqa: E402
from c2_kit.skin import make_skin  # noqa: E402
from transfer.T36 import fixtures as FX  # noqa: E402
from transfer.T36 import plugin as P  # noqa: E402
from transfer.T36 import solver_b as B  # noqa: E402
from transfer.T36.test_plugin import _spec, _view  # noqa: E402

SAMPLERS = P.T36Plugin.SAMPLERS


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T36Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def specs(plugin):
    return [plugin.sample(seed, smp) for seed in range(600) for smp in SAMPLERS]


def test_g0_is_v22_and_short():
    text = P.T36Plugin.G0_LITE.read_text()
    assert "v2, FROZEN" in text and "**v2.2**" in text and len(text.splitlines()) <= 200
    assert P.T36Plugin.G0_AMBIGUITY_PASS["points"] == P.T36Plugin.G0_AMBIGUITY_PASS["resolved"] == 33


def test_cards_are_copies_and_state_the_v2_rules():
    """v2.2: the card is row-specific; plugin.CARD_ITEMS and solver B's ITEM are copies, in the same order."""
    for eco, items in P.CARD_ITEMS.items():
        assert [i.item_id for i in items] == list(B.ORDER[eco])
        assert {i.item_id: i.full for i in items} == B.ITEM[eco]
        assert P.HEADING[eco] == B.HEAD[eco]
    assert P.CLOSED_WORLD == B.CLOSED
    npm = {i.item_id: i.full for i in P.CARD_ITEMS["npm"]}
    pep = {i.item_id: i.full for i in P.CARD_ITEMS["pep"]}
    assert "inside the range when it meets" in npm["inout"] and "outside the range when it does not" in npm["inout"]
    assert "The resolver installs the highest listed version that meets" in npm["pick"]
    assert "itself writes a version" in npm["gate"] and "do not count" in npm["gate"]
    assert "post-releases included; a pre-release among them still needs" in pep["wild"]


V21_CARD = {    # the v2.1 cards (G0_SPEC_v2.1.md section 1.2), every rule on every row
    "npm": (
        'A version is MAJOR.MINOR.PATCH, optionally followed by "-" and a pre-release tag such as "beta.2". Compare versions by '
        'MAJOR, then MINOR, then PATCH, each as a number. A version with a pre-release tag comes before the same version without '
        'one. Two tags compare part by part: numbers as numbers, words alphabetically, a number before a word, and a shorter tag '
        'first when all its parts match (tag parts are separated by ".").\n'
        '">=V", ">V", "<=V", "<V" and "=V" compare with V; a bare "V" means "=V".\n'
        '"^V" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 '
        'means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n'
        '"~V" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.\n'
        '"A - B" means >=A <=B. "1.4.x" means >=1.4.0 <1.5.0, and "1.x" means >=1.0.0 <2.0.0.\n'
        'Parts separated by spaces must all hold. "||" separates alternatives: the range is met when one alternative is met.\n'
        'A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same '
        'MAJOR.MINOR.PATCH and a pre-release tag (bounds that "^", "~" or "x" imply do not count).\n'
        'A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie '
        'between the bounds.\n'
        'The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver '
        'installs none of them.'),
    "pep": (
        'A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a '
        'before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with '
        'zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the '
        'next release.\n'
        '">=V", ">V", "<=V", "<V", "==V" and "!=V" compare with V.\n'
        '"==1.4.*" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a '
        'pre-release among them still needs the pre-release rule below.\n'
        '"~=V" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and '
        '~=1.4 means >=1.4 and ==1.*.\n'
        'Specifiers separated by commas must all hold.\n'
        'A version with a pre-release meets the specifiers only if one of them, other than a "!=" one, names a pre-release version; '
        'this holds for every set of specifiers.\n'
        'The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range '
        'when it does not, even when its numbers lie between the bounds.\n'
        'The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver '
        'installs none of them.'),
}


def test_v22_items_say_what_the_v21_card_said():
    """Splitting the card per rule changed no word: all items of a style, in order, are the v2.1 card text (the closing
    sentence and the headings are the same constants)."""
    for eco, items in P.CARD_ITEMS.items():
        joined = "\n".join(i.full for i in items)
        assert " ".join(joined.split()) == " ".join(V21_CARD[eco].split())
    assert P.HEADING["npm"] == "How to read this version range (npm style):"
    assert P.HEADING["pep"] == "How to read these version specifiers (Python packaging style):"


def test_g0_quotes_every_item_verbatim_and_the_sha_is_pinned():
    import hashlib
    text = " ".join(P.T36Plugin.G0_LITE.read_text().split())
    for items in P.CARD_ITEMS.values():
        for it in items:
            assert " ".join(it.full.split()) in text, it.item_id
    assert hashlib.sha256(P.T36Plugin.G0_LITE.read_bytes()).hexdigest() == P.T36Plugin.G0_SHA256
    old = P.HERE / "G0_SPEC_v2.1.md"
    assert hashlib.sha256(old.read_bytes()).hexdigest() == P.POOL_G0_SHA256 != P.T36Plugin.G0_SHA256


# ------------------------------------------------------------------------------------------------ hand gold

HAND = [  # (style, alternatives, hyphen flags, version, meets?) by hand from G0 R4, R7, R9
    ("pep", [[">=1.0", "<2"]], None, "1.5rc1", False),             # H2: the gate in a plain window
    ("pep", [["<=2.0"]], None, "2.0rc1", False),                   # H2
    ("pep", [["==1.4.*"]], None, "1.4.1rc1", False),               # H3 (b): prefix matches, gate refuses
    ("pep", [["==1.4.*"]], None, "1.4.1.post2", True),             # R6: post-releases included
    ("pep", [["~=1.4.2rc1"]], None, "1.4.3rc1", True),             # R6 / H18: named pre-release opens the gate
    ("pep", [["~=1.4.2rc1"]], None, "1.5", False),                 # prefix 1.4 from the release part
    ("npm", [["^1.2.3"]], None, "1.3.0-rc.1", False),              # H4: numerically within, outside the range
    ("npm", [["^1.2.3"]], None, "2.0.0-rc.1", False),              # H11: a computed bound names no tag
    ("npm", [["1.2.0", "1.3.0-beta.2"]], [True], "1.3.0-beta.1", True),   # H11: either end of a hyphen range
    ("npm", [[">=1.2.0", "<1.3.0-rc.1"]], None, "1.3.0-alpha", True),     # H11: any written comparator
    ("npm", [[">=1.2.0", "<1.3.0-rc.1"]], None, "1.3.0-rc.1", False),
    ("npm", [["~1.3.0-beta"], ["2.x"]], None, "1.3.0-beta.2", True),      # gate per alternative
    ("npm", [["2.x"], ["~1.3.0-beta"]], None, "2.0.0-beta", False),
]


@pytest.mark.parametrize("case", HAND, ids=[f"{c[0]}:{c[1]}:{c[3]}" for c in HAND])
def test_v2_hand_gold(case):
    eco, alts, hyph, v, want = case
    spec = _spec(eco, alts, [v], v, hyphen=hyph)
    assert P.meets(spec, v) is want
    for qf in ("yn_meets", "yn_outside", "yn_not_meets", "yn_fails"):
        exp = int(want) if qf == "yn_meets" else int(not want)
        assert B.solve_b(_view(eco, alts, hyph, [v], v, qf)) == exp == P.answer_for(qf, want)


def test_v2_hand_pick_highest_meeting_not_highest_listed():
    vs = ["1.2.9", "1.3.0-rc.1", "1.2.10", "2.0.0"]
    s = _spec("npm", [["^1.2.3"]], vs, qform="ch_pick")
    assert P.pick(s) == "1.2.10" == B.solve_b(_view("npm", [["^1.2.3"]], None, vs, None, "ch_pick"))
    assert P.pick(s, frozenset({"t36_prerelease_ignored"})) == "1.3.0-rc.1"      # H8: gate off
    assert P.pick(s, ignore_range=True) == "2.0.0"
    s2 = _spec("npm", [["^0.4.2"]], ["0.4.9", "0.9.0", "1.0.0"], qform="ch_pick")
    assert P.pick(s2) == "0.4.9" and P.pick(s2, frozenset({"t36_caret_as_major"})) == "0.9.0"   # H31


# ------------------------------------------------------------------------------------------------ never generated

NPM_COMP = re.compile(r"(?:\^|~|>=|<=|>|<|=)?\d+\.\d+\.\d+(?:-[a-z]+(?:\.\d+)?)?|\d+\.(?:\d+\.)?x")
PEP_COMP = re.compile(r"(?:~=|==|!=|<=|>=|<|>)\d+\.\d+(?:\.\d+)?(?:(?:a|b|rc)\d+)?|==\d+\.\d+\.\*")


def test_never_generated_forms(specs):
    n_pep = n_npm = 0
    for spec in specs:
        env = spec.env()
        eco = spec.structure["eco"]
        comps = [env[n] for alt in spec.structure["alts"] for n in alt]
        vs = P.published(spec)
        if eco == "npm":
            n_npm += 1
            assert all(NPM_COMP.fullmatch(c) for c in comps), comps
            assert not any(re.fullmatch(r"\^0\.0\.0(?:-.*)?", c) for c in comps), comps          # H14
            for v in vs:
                trip, pre = P.npm_parts(v)
                assert pre is None or re.fullmatch(r"[a-z]+(?:\.\d+)?", pre), v                  # H16
        else:
            n_pep += 1
            assert all(PEP_COMP.fullmatch(c) for c in comps), comps                               # H19, H20
            assert not any(c.startswith("!=") and P.pep_parts(c[2:])[1] for c in comps)           # R8
            for c in comps:
                if c.startswith("~="):
                    assert P.pep_parts(c[2:])[3] is None and len(P.pep_parts(c[2:])[0]) >= 2      # H18
                m = re.fullmatch(r"(>|<)([\d.]+)", c)
                if m:
                    vr = P.pep_parts(m[2])[0]
                    for v in vs:
                        rel, pre, _n, post = P.pep_parts(v)
                        same = P.pep_key(m[2]) [0] == P.pep_key(".".join(map(str, rel)))[0]
                        assert not (same and (post is not None if m[1] == ">" else pre)), (c, v, vr)   # R8
            for v in vs:
                assert re.fullmatch(r"\d+\.\d+(?:\.\d+)?(?:(?:a|b|rc)\d+|\.post\d+)?", v), v      # H17
    assert n_npm > 500 and n_pep > 500


def test_r8_gate_pairs_in_plain_windows_are_generated(specs):
    """H2: R8 is the complete list, so pre-releases inside plain numeric windows ARE generated (and refused)."""
    hits = 0
    for spec in specs:
        if spec.structure["eco"] != "pep":
            continue
        for v in P.published(spec):
            if P.pep_parts(v)[1] and not P.meets(spec, v) and P.meets(spec, v, frozenset({"t36_prerelease_ignored"})):
                hits += 1
    assert hits > 50


# ------------------------------------------------------------------------------------------------ options

def test_option_count_is_never_lowered(plugin, ctx, specs):
    n = 0
    for spec in specs[:900]:
        if spec.qform != "ch_pick":
            continue
        rr = plugin.render(spec, ctx)
        key = plugin.row_key(spec)
        assert len(rr.row["options"]) == P.option_count(key)
        assert P.NONE_TEXT in rr.row["options"]
        assert len(set(rr.row["options"])) == len(rr.row["options"])
        n += 1
    assert n > 200


# ------------------------------------------------------------------------------------------------ packs

def test_packs(plugin, specs):
    assert all(P.check_pack(p, plugin.LABEL_WORDS) == [] for p in P.STANDIN_PACKS)
    bad = [P.Pack("x1", "Harbor Lantern", ("fern-cache", "fern-cache", "ok-db"), ("Dana Okafor", "Lena Whitcombe")),
           P.Pack("x2", "Harbor Lantern", ("fern2-cache", "tide-log", "ok-db"), ("Dana Okafor", "Lena Whitcombe")),
           P.Pack("x3", "Latest Lantern", ("fern-cache", "tide-log", "oak-db"), ("Dana Okafor", "Lena Whitcombe")),
           P.Pack("x4", "Lowmoor Desk", ("fern-cache", "tide-log", "oak-db"), ("Dana Okafor", "Lena Whitcombe")),
           P.Pack("x5", "Harbor Lantern", ("fern-cache", "tide-log", "oak-db"), ("Dana", "Lena Whitcombe")),
           P.Pack("x6", "harbor lantern", ("fern-cache", "tide-log", "oak-db"), ("Dana Okafor", "Lena Whitcombe"))]
    for p in bad:
        assert P.check_pack(p, plugin.LABEL_WORDS), p.key
    by_key = {p.key: p for p in P.STANDIN_PACKS}
    for spec in specs[:1000]:
        pk = by_key[spec.pack]
        env = spec.env()
        assert pk.held_out == (spec.sampler == "S5")
        assert env["PKG"] in pk.packages and env["PERSON"] in pk.people and env["PROJECT"] == pk.project
        assert env["PROJECT_ID"] == P.project_id(pk.project)
    with pytest.raises(Exception):
        P.T36Plugin(packs=[p for p in P.STANDIN_PACKS if not p.held_out])


def test_label_words_catch_order_and_verdict_words(plugin):
    for word in ("latest", "newest", "upgraded", "installed", "met", "within", "stable"):
        sk = make_skin("SK-X", "T36", f"{{PERSON}} on {{PKG}} in {{PROJECT}}: the {word} one.",
                       {"PERSON": "name", "PKG": "id", "PROJECT": "name"}, register="dev_chat")
        assert any(v.rule == "gold_label" for v in gsl.lint_template(sk, label_words=plugin.LABEL_WORDS)), word


def test_question_meanings_cover_the_forms():
    """The five meanings of the frozen pools plus the v2.2 meaning of yn_double (kept out of the frozen dict: a sixth meaning
    would change the choices every frozen G-LEX extraction item showed)."""
    assert set(P.QUESTION_MEANINGS) | set(P.QUESTION_MEANINGS_V22) == set(P.T36Plugin.QFORMS)
    assert not set(P.QUESTION_MEANINGS) & set(P.QUESTION_MEANINGS_V22)
    assert all(k.startswith("q.t36.decoy_") for k in P.QUESTION_DECOYS)
    assert len(set(P.QUESTION_MEANINGS.values()) | set(P.QUESTION_DECOYS.values())) == 8


# ------------------------------------------------------------------------------------------------ balance, twins

def test_blocks_balance_meets_status(plugin, specs):
    """v2.2: every block of 4 yes/no bases holds each (meets, negative form) cell once (yn_cell)."""
    by = collections.defaultdict(list)
    for s in specs:
        kind, y = P.slot_of(s.sampler, s.seed)
        if kind == "yesno":
            by[(s.sampler, y // 4)].append(s)
    n = 0
    for (smp, blk), ss in by.items():
        if len(ss) < 4:
            continue
        cells = collections.Counter((P.meets(s, s.env()["CAND"]), s.qform in P.NEG_FORMS) for s in ss)
        assert cells == {(True, False): 1, (False, False): 1, (True, True): 1, (False, True): 1}, (smp, blk, cells)
        n += 1
    assert n > 100


def test_choice_twins_keep_the_list_size(plugin, specs):
    n = 0
    for spec in specs[:1500]:
        if spec.qform != "ch_pick":
            continue
        for prop in plugin.relations(spec):
            if prop.kind == "twin":
                assert len(P.published(prop.spec)) == len(P.published(spec))
                assert P.published(prop.spec) != P.published(spec)
                n += 1
    assert n > 50
