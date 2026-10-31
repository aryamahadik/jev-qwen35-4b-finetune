"""families/T35/test_fix_i1.py: tests for pilot fix iteration 1 (PILOT_VERDICT F1-F4; G0_SPEC.md v4). In memory only (A37 f).

  F2  4xx / 5xx statuses are capped (they decide alone, so G6's metadata view reads them); a status line stays on ~15% of rows
  F3  the ch_line display plan: slot blocks, abstain gold exactly 1/k per block of k rows, position and rank uniform, the plan
      carried by every realised option set, "no line" wrong exactly as often as the plan says
  F4  the choice / yes-no base slots (46.6% choice) so that yes/no rows are about 70% of the ROWS
  cards   compact phrasings keep every rule (c2_kit.cards.variant_problems), the status item stands only with a status line,
          style shares, real-token mean
  look-alikes   wrong lines are error-model outputs shaped like the deciders (profile), no query string on ch_line rows

Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T35/test_fix_i1.py
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

from c2_kit import cards as CARDS  # noqa: E402
from c2_kit import pipeline  # noqa: E402
from c2_kit.choiceplan import plan_report  # noqa: E402
from families.T35 import fixtures as FX  # noqa: E402
from families.T35 import plugin as P  # noqa: E402
from families.T35 import solver_b as B  # noqa: E402

TRAIN = ("S1", "S2", "S3", "S4")


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T35Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def units(plugin, ctx):
    out = []
    for smp in TRAIN:
        for seed in range(P.W_SLOTS * 3):
            out.append(pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False))
    return out


# ------------------------------------------------------------------------------------------------ F4: slots

def test_every_slot_block_holds_exactly_its_choice_bases():
    for smp in TRAIN + ("S5",):
        for blk in range(6):
            got = [P.slot_of(smp, blk * P.W_SLOTS + i) for i in range(P.W_SLOTS)]
            assert sum(k == "choice" for k, _ in got) == P.N_CHOICE_SLOTS
            assert sorted(i for k, i in got if k == "choice") == list(
                range(blk * P.N_CHOICE_SLOTS, (blk + 1) * P.N_CHOICE_SLOTS))
            assert sorted(i for k, i in got if k == "yesno") == list(
                range(blk * (P.W_SLOTS - P.N_CHOICE_SLOTS), (blk + 1) * (P.W_SLOTS - P.N_CHOICE_SLOTS)))


def test_the_slot_depends_on_the_seed_alone_not_on_a_label():
    a = [P.slot_of("S2", s) for s in range(200)]
    assert a == [P.slot_of("S2", s) for s in range(200)]
    assert a != [P.slot_of("S3", s) for s in range(200)]          # another sampler stream
    assert 0.40 <= P.N_CHOICE_SLOTS / P.W_SLOTS <= 0.50


def test_yes_no_cells_are_balanced_in_every_block_of_four_bases():
    for smp in TRAIN:
        for blk in range(30):
            cells = {P.T35Plugin._cell(smp, 4 * blk + i) for i in range(4)}
            assert len(cells) == 4


# ------------------------------------------------------------------------------------------------ F3: the plan

def _plans(smp, n_blocks=12):
    out = []
    for seed in range(n_blocks * P.W_SLOTS):
        kind, c = P.slot_of(smp, seed)
        if kind == "choice":
            out.append((c, P.choice_plan(smp, seed)))
    return [p for _c, p in sorted(out, key=lambda x: x[0])]


def test_abstain_gold_is_exactly_one_in_k_in_every_block_of_k_rows():
    for smp in TRAIN:
        by_k = collections.defaultdict(list)
        for p in _plans(smp):
            by_k[p.k].append(p)
        assert set(by_k) == {3, 4}
        for k, ps in by_k.items():
            for i in range(0, len(ps) - k + 1, k):
                blk = ps[i:i + k]
                assert sum(p.gold_abstain for p in blk) == 1, (smp, k, i)
                assert sorted(p.pos for p in blk) == list(range(k))          # position: each place once per block
                assert all(p.abstain_share == 1 / k and p.show_abstain for p in blk)
                assert all((p.rank is None) == p.gold_abstain for p in blk)
        assert abs(len(by_k[3]) - len(by_k[4])) <= 1


def test_the_plan_is_the_rows_own_and_is_read_by_the_sampler_and_the_renderer(plugin, ctx):
    n_none = n = 0
    for smp in TRAIN:
        for seed in range(P.W_SLOTS):
            spec = plugin.sample(seed, smp)
            if spec.qform != P.CHOICE_FORM:
                continue
            plan = P.choice_plan(smp, seed)
            assert plan.row_key == plugin.row_key(spec)
            gold = plugin.solve_a(spec)
            assert (gold == P.NONE_KEY) == plan.gold_abstain          # label-first: structure was drawn to the plan
            os_ = plugin.render(spec, ctx).option_set
            assert os_.meta["plan"]["k"] == len(os_.options) == plan.k and os_.gold_index == plan.pos
            assert os_.meta["length_balance"] and os_.abstain_shown
            n += 1
            n_none += gold == P.NONE_KEY
    assert n > 60 and 0.25 <= n_none / n <= 0.42


def test_realised_option_sets_pass_the_kit_plan_report(units):
    sets = [rr.option_set for u in units for rr in u.rendered if rr.option_set is not None]
    assert len(sets) > 150
    rep = plan_report(sets)
    assert rep["pass"], rep["failing"]
    assert abs(rep["longest_gold_pp"]) <= 2.0
    shares = {c: v["share"] for c, v in rep["abstain_cells"].items()}
    assert 0.28 <= shares["k3|shown=True"] <= 0.38 and 0.20 <= shares["k4|shown=True"] <= 0.30


# ------------------------------------------------------------------------------------------------ look-alike options

def test_choice_rows_carry_no_query_string(plugin):
    n = 0
    for smp in TRAIN:
        for seed in range(P.W_SLOTS * 2):
            spec = plugin.sample(seed, smp)
            if spec.qform == P.CHOICE_FORM:
                n += 1
                assert "?" not in spec.slots["URL"].value
    assert n > 100


def test_wrong_lines_are_error_model_outputs_with_a_real_pattern(units, plugin):
    seen = 0
    models = set(plugin.error_models())
    for u in units:
        for rr in u.rendered:
            os_ = rr.option_set
            if os_ is None:
                continue
            for o in os_.options:
                if o.role == "error":
                    seen += 1
                    assert o.err and set(o.err) <= models
                    assert len(o.key.split(":", 1)[1]) >= P.MIN_PATTERN
    assert seen > 300 and "robots_allow_wins" in models


def test_wrong_lines_look_like_the_deciders(units):
    """The pilot residual: a wrong line was star-free, longer and often anchored; a root line was never gold. Gold and wrong
    lines now agree on the visible surface flags (a loose bound: ~380 rows)."""
    gold, wrong = collections.defaultdict(list), collections.defaultdict(list)
    for u in units:
        for rr in u.rendered:
            os_ = rr.option_set
            if os_ is None:
                continue
            for o in os_.options:
                if o.role not in ("gold", "error") or (o.role == "gold" and os_.meta["gold_is_abstain"]):
                    continue
                tgt = gold if o.role == "gold" else wrong
                for name, v in zip(("star", "dollar", "query", "upper", "ext", "slash", "digit", "allow"),
                                   P.line_profile(o.key)):
                    tgt[name].append(float(v))
    assert len(gold["star"]) > 150
    bound = {"star": 0.10, "dollar": 0.12, "upper": 0.10, "slash": 0.15, "allow": 0.10}   # the pilot gaps were 0.14-0.16
    for name, tol in bound.items():
        g, w = sum(gold[name]) / len(gold[name]), sum(wrong[name]) / len(wrong[name])
        assert abs(g - w) <= tol, (name, round(g, 3), round(w, 3))


# ------------------------------------------------------------------------------------------------ F2: status

def test_status_rows_are_capped_and_the_status_line_stays_common(units):
    rows = [r for u in units for r in u.rows]
    yn = [r for r in rows if r["qtype"] == "noul"]
    ns = [r for r in yn if re.search(r"fetch status: (?:4\d\d|5\d\d|no response)", r["state"])]
    shown = [r for r in rows if "robots.txt fetch status" in r["state"]]
    assert len(yn) > 300
    assert len(ns) / len(yn) <= 0.05                       # G6 caps the share (0.5 + s / 2 <= 0.52 means s <= 4%)
    assert 0.07 <= len(shown) / len(rows) <= 0.25          # spec 3.2: a status on about 15% of rows (mostly 200)


def test_status_twins_start_from_a_status_and_flip_by_it(plugin):
    n = 0
    for smp in TRAIN:
        for seed in range(P.W_SLOTS * 6):
            spec = plugin.sample(seed, smp)
            for prop in plugin.relations(spec):
                if prop.kind == "twin" and prop.changed_slot == "STATUS":
                    n += 1
                    assert "STATUS" in spec.slots
                    assert plugin.solve_a(plugin.derive(prop.spec)) == prop.expect != plugin.solve_a(spec)
    assert n >= 3


# ------------------------------------------------------------------------------------------------ cards

def _items(text: str) -> dict:
    out = {}
    for m in re.finditer(r"^(?:(\d)\. )?(Group|Path|Match|robots\.txt (?:fetch )?status)[^\n]*", text, re.M):
        out[m.group(2)] = m.group(0)
    return out


def test_compact_phrasings_keep_every_rule():
    full = _items(P.card_template("full", True))
    comp = _items(P.card_template("compact", True))
    assert set(full) == set(comp) and len(full) == 4
    for name in full:
        a, b = re.sub(r"^\d\. ", "", full[name]), re.sub(r"^\d\. ", "", comp[name])
        assert CARDS.variant_problems(a, b) == [], (name, CARDS.variant_problems(a, b))
        assert len(b) < len(a)
    for style in ("full", "compact", "short"):                                   # both clauses and the closed world stay
        t = P.card_template(style, False)
        assert "{LONGEST}" in t and "{TIE}" in t and t.endswith(P.CLOSED_WORLD)
        assert "status" not in t.lower().replace("robots.txt status", "")


def test_the_status_item_stands_on_a_card_exactly_when_the_request_shows_a_status(units):
    n = 0
    for u in units:
        for r in u.rows:
            text = r["card"] if r["qtype"] == "noul" else r["instructions"]
            has_item = bool(re.search(r"robots\.txt (?:fetch )?status", text))
            assert has_item == ("robots.txt fetch status:" in r["state"]), r["id"]
            n += 1
    assert n > 500


def test_solver_b_refuses_a_card_whose_status_item_disagrees_with_the_request(plugin, ctx):
    spec = next(s for s in (plugin.sample(i, "S1") for i in range(200)) if "STATUS" not in s.slots
                and s.qform != P.CHOICE_FORM)
    rr = plugin.render(spec, ctx)
    row = dict(rr.row)
    style = spec.structure["card"]
    with_status = P.K.fill(P.card_template(style, True), spec.all_slots(), rr.forms).text
    row["card"] = with_status
    with pytest.raises(B.ParseError):
        B.parse(row, ctx)


def test_card_style_shares_are_the_g0_shares():
    n = 20000
    got = collections.Counter(CARDS.draw_style(f"k{i}", P.CARD_SHARES) for i in range(n))
    for style, share in P.CARD_SHARES.items():
        assert abs(got[style] / n - share) <= 0.01, style
    assert P.CARD_SHARES["short"] <= CARDS.SHORT_CAP


def test_mean_real_tokens_stay_under_the_spec_bar(units):
    rows = [r for u in units for r in u.rows]
    rep = CARDS.token_report(rows)
    if not rep["counted_by"].startswith("mixer.token_counts"):
        pytest.skip("pinned tokenizer not on this machine")
    assert rep["mean"] <= 800 and rep["max"] <= 2000, rep
    assert 0.60 <= rep["yes_no_share"] <= 0.80                                    # rows, not specs (F4)


def test_defs_style_names_the_card_field_and_style(units):
    seen = collections.Counter(r["meta"]["defs_style"] for u in units for r in u.rows)
    assert set(seen) <= {f"rules_in_{f}_{s}" for f in ("card", "instructions") for s in ("full", "compact", "short")}
    assert len(seen) >= 5
    sr = CARDS.style_report([r for u in units for r in u.rows])
    assert 0.08 <= sr["short_or_none_share"] <= 0.22


# ------------------------------------------------------------------------------------------------ qform-level label balance

def test_every_form_is_exactly_half_yes_among_the_bases_of_full_blocks(plugin):
    """One negative form per block of 4 yes/no bases (and one positive form): the block's two bases of a polarity hold both
    outcomes, so each form is exactly 50% yes. (First pilot_i1: the forms wandered +/- 5 pp, so the metadata and question
    views read the qform with 54%.)"""
    for smp in TRAIN:
        by = collections.defaultdict(lambda: [0, 0])
        for seed in range(P.W_SLOTS * 12):
            spec = plugin.sample(seed, smp)
            if spec.qform != P.CHOICE_FORM:
                by[spec.qform][0] += plugin.solve_a(spec)
                by[spec.qform][1] += 1
        used = {q: v for q, v in by.items() if v[1] >= 20}
        assert len(used) >= 4
        for q, (yes, n) in used.items():
            assert abs(yes - n / 2) <= 1, (smp, q, yes, n)        # a partial last block leaves at most one base over


def test_every_partner_form_is_half_yes_too(plugin):
    for smp in TRAIN:
        by = collections.defaultdict(lambda: [0, 0])
        for seed in range(P.W_SLOTS * 12):
            spec = plugin.sample(seed, smp)
            for prop in plugin.relations(spec):
                if prop.kind == "complement":
                    by[prop.qform][0] += plugin.solve_a(spec.replace(qform=prop.qform))
                    by[prop.qform][1] += 1
        assert len(by) == 4
        for q, (yes, n) in by.items():
            assert n >= 10 and abs(yes - n / 2) <= 2, (smp, q, yes, n)


def test_twins_exist_for_may_fetch_rows_nearly_as_often_as_for_blocked_rows(plugin):
    """Twin availability followed the outcome (may fetch 61%, blocked 96%) because a "no line matches" row has no line to
    flip: twins skewed toward "may fetch" and with them every form's yes rate. The pattern twin (one pattern slot of an
    applying Disallow line becomes one that matches) closes most of the gap."""
    tab = {True: [0, 0], False: [0, 0]}
    for smp in TRAIN:
        for seed in range(P.W_SLOTS * 8):
            spec = plugin.sample(seed, smp)
            if spec.qform == P.CHOICE_FORM:
                continue
            allowed = P.decide(spec).allowed
            tab[allowed][1] += 1
            tab[allowed][0] += plugin._twin(spec) is not None
    a, b = tab[True][0] / tab[True][1], tab[False][0] / tab[False][1]
    assert a >= 0.72 and b >= 0.88 and b - a <= 0.25, (a, b)


def test_pattern_twins_change_one_pattern_slot_and_flip_by_construction(plugin):
    n = 0
    for smp in TRAIN:
        for seed in range(P.W_SLOTS * 6):
            spec = plugin.sample(seed, smp)
            if spec.qform == P.CHOICE_FORM:
                continue
            for prop in plugin.relations(spec):
                if prop.kind == "twin" and prop.changed_slot.startswith("P"):
                    n += 1
                    twin = plugin.derive(prop.spec)
                    d0, d1 = P.decide(spec), P.decide(twin)
                    assert d0.rules_by == "nomatch" and d0.allowed and not d1.allowed and d1.rules_by == "line"
                    assert twin.slots[prop.changed_slot].value != spec.slots[prop.changed_slot].value
                    assert twin.slots["E" + prop.changed_slot[1:]].value == "disallow"
                    assert plugin.solve_a(twin) == prop.expect
    assert n >= 25
