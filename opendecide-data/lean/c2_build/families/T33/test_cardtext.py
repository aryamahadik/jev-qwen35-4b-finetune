"""families/T33/test_cardtext.py: the rules block (pilot fix F5, length; spec 3.0 definition styles). In memory only.

Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T33/test_cardtext.py
  variants     the short phrasing keeps slots, numbers, operator words and the negation count of the full one
  need-to-know a bullet / clause appears exactly when the row needs it (value, money, duration, tries, table)
  placement    yes/no rows: the block is row.card and the instructions are the question; choice rows: the block heads the
               instructions; cards.split_rules recovers both
  styles       full and short are drawn from the seed; a complement pair shares its card; short is about 15%
  solver B     accepts every style, refuses a missing or an extra bullet (its own copy of the texts)
"""
from __future__ import annotations

import collections
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import cards, pipeline  # noqa: E402
from families.T33 import cardtext as CT  # noqa: E402
from families.T33 import fixtures as FX  # noqa: E402
from families.T33 import plugin as T  # noqa: E402
from families.T33 import solver_b as B  # noqa: E402


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return T.T33Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def rendered(plugin, ctx):
    out = []
    for seed in range(220):
        for smp in ("S1", "S2", "S3", "S4"):
            spec = plugin.sample(seed, smp)
            out.append((spec, plugin.render(spec, ctx)))
    return out


def test_short_phrasings_keep_every_rule():
    assert CT.variant_problems() == []


def test_a_bad_short_phrasing_is_caught():
    full = CT.TIE_CHECK["full"]
    for bad in (full.replace("; if none fails, answer None", ""), "Answer None.",
                "Answer the lowest-numbered failing check; answer None."):
        assert cards.variant_problems(full, bad), bad


def test_bullets_appear_exactly_when_the_row_needs_them(rendered):
    seen = collections.Counter()
    for spec, rr in rendered:
        n = CT.needs_of(spec)
        rules, _q = cards.split_rules(rr.row)
        has = lambda frag: frag in rules                                    # noqa: E731
        assert has("Result:") == n.value, (spec.sampler, spec.seed)
        assert has("rows_written") == n.rows
        cents = has("amount_cents is cents") or has("amount_cents: cents")
        ms = has("duration_ms is milliseconds") or has("duration_ms: milliseconds")
        assert cents == n.money and ms == n.dur
        assert has("Table:") == (n.table and n.value)
        assert has("polls are not tries") == n.tries
        if spec.structure["sub"] == "a":
            assert has("a check on a value not in the log fails") == n.value_dep
        else:
            assert has("amount or row count differs") or not (n.money and n.rows)
            assert has("its amount differs from the result") == (n.money and not n.rows)
            assert has("its row count differs from the result") == (n.rows and not n.money)
            assert has("differs from the result") == n.value
        assert has("The log is complete and the only evidence")
        for k in ("value", "money", "rows", "dur", "tries", "table"):
            seen[k] += bool(getattr(n, k))
    assert all(v > 20 for v in seen.values()), seen           # every need occurs in the sample


def test_placement_yes_no_in_card_choice_in_instructions(rendered):
    kinds = collections.Counter()
    for spec, rr in rendered:
        row = rr.row
        rules, question = cards.split_rules(row)
        if row["qtype"] == "noul":
            assert row["card"] == rules and row["instructions"] == question and "\n\n" not in question
            assert row["meta"]["defs_style"].startswith("rules_in_card_")
        else:
            assert row["card"] is None and row["instructions"] == rules + "\n\n" + question
            assert row["meta"]["defs_style"].startswith("rules_in_instructions_")
            assert "\n\n" not in rules
        assert rules.startswith(CT.LOG_HEAD) and rules.endswith(CT.CLOSED_WORLD)
        kinds[row["qtype"]] += 1
    assert kinds["noul"] and kinds["choice"]


def test_styles_come_from_the_seed_and_short_is_about_15_percent(plugin, ctx, rendered):
    styles = collections.Counter(rr.row["meta"]["defs_style"].rsplit("_", 1)[1] for _s, rr in rendered)
    assert set(styles) == {"compact", "short"}                 # full is the reference text: never drawn
    assert 0.09 <= styles["short"] / sum(styles.values()) <= 0.21
    for spec, rr in rendered[::7]:
        assert rr.row["meta"]["defs_style"].endswith(CT.draw_style(spec.seed, spec.sampler))
    assert CT.STYLE_SHARES["short"] <= cards.SHORT_CAP
    with pytest.raises(cards.CardError):
        cards.draw_style("k", {"full": 0.7, "short": 0.3})          # more than the G0 share: refused by the kit


def test_a_complement_pair_shares_one_card(plugin, ctx):
    pairs = 0
    for seed in range(300):
        spec = plugin.sample(seed, "S1")
        res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
        assert res.ok, res.problems[:2]
        by_role = collections.defaultdict(list)
        for r in res.rows:
            by_role[r["role"]].append(r)
        if by_role["complement"]:
            assert by_role["complement"][0]["card"] == by_role["base"][0]["card"]
            pairs += 1
    assert pairs > 10


def test_whole_blocks_keep_every_rule_of_the_full_block(rendered):
    """Not only the pieces: a rendered compact / short block, with its slots filled back to the full block's, keeps
    the full block's slots, numbers, operator words and negation count (cards.variant_problems on the whole text)."""
    import re
    done = collections.Counter()
    for spec, rr in rendered[::3]:
        rules, _q = cards.split_rules(rr.row)
        style = rr.row["meta"]["defs_style"].rsplit("_", 1)[1]
        assert style in ("compact", "short")
        crit = re.search(r"Success criterion for step (\S+?):", rules)
        subs = {"STEP": crit.group(1)} if crit else {}
        for m in re.finditer(r"^\((\d)\) (.+)$", rules, re.M):
            subs["CHK" + m.group(1)] = m.group(2)
        full = CT.block_template(spec, "full")
        for k, v in subs.items():
            full = full.replace("{" + k + "}", v)
        # apostrophes of one flat line pair up as "quoted literals" in the kit's heuristic; the block quotes nothing
        got = [x for x in cards.variant_problems(full, rules) if not x.startswith("quoted literals")]
        assert not got, (spec.sampler, spec.seed, style, got)
        assert len(rules) < len(full)
        done[style] += 1
    assert done["compact"] and done["short"]


def test_solver_b_expects_the_cardtext_blocks_in_every_style(plugin, ctx, rendered):
    """Solver B's own copy equals the generator's block for the full style too (it accepts all three)."""
    import re
    n = 0
    for spec, rr in rendered[::9]:
        rules, _q = cards.split_rules(rr.row)
        crit = re.search(r"Success criterion for step (\S+?):", rules)
        checks = re.findall(r"^\(\d\) .+$", rules, re.M)
        need = CT.needs_of(spec)
        nd = {"money": need.money, "rows": need.rows, "dur": need.dur, "tries": need.tries, "dep": need.value_dep,
              "table": need.table}
        for style in CT.STYLES_ALL:
            tmpl = CT.block_template(spec, style)
            for k in range(1, 4):
                tmpl = tmpl.replace("{CHK%d}" % k, checks[k - 1][4:] if k <= len(checks) else "")
            if crit:
                tmpl = tmpl.replace("{STEP}", crit.group(1))
            want = B._expected_rules(style, spec.qform, spec.structure["sub"], nd, crit.group(1) if crit else None,
                                     checks)
            assert "\n".join(want) == tmpl, (style, spec.sampler, spec.seed)
        n += 1
    assert n > 20


def test_solver_b_accepts_both_styles_and_reads_the_row(plugin, ctx, rendered):
    n = collections.Counter()
    for spec, rr in rendered[::5]:
        view = plugin.parse(rr.row, ctx)
        assert plugin.solve_b(view) == plugin.solve_a(spec)
        n[rr.row["meta"]["defs_style"].rsplit("_", 1)[1]] += 1
    assert n["compact"] and n["short"]


@pytest.mark.parametrize("what", ["drop_result", "extra_units", "drop_closed", "wrong_style_mix"])
def test_solver_b_refuses_a_block_that_is_not_need_to_know(plugin, ctx, rendered, what):
    spec, rr = next((s, r) for s, r in rendered if CT.needs_of(s).value and r.row["meta"]["defs_style"].endswith("compact")
                    and r.row["qtype"] == "noul")
    row = dict(rr.row)
    card = row["card"]
    if what == "drop_result":
        import re
        card = re.sub(r" Result:[^.]*\.", "", card, count=1)
    elif what == "extra_units":
        if "duration_ms: milliseconds" in rr.row["card"]:
            pytest.skip("this row already has the unit line")
        card = card.replace(CT.LOG_ITEMS[1].compact, CT.LOG_ITEMS[1].compact + " duration_ms: milliseconds.")
    elif what == "drop_closed":
        card = card.replace(CT.CLOSED_WORLD, "")
    else:                                             # a short line inside a compact block
        card = card.replace(CT.LOG_ITEMS[0].compact, CT.LOG_ITEMS[0].short)
    row["card"] = card
    with pytest.raises(B.ParseError):
        B.parse(row, ctx)
