"""Tests for c2_kit.cards: compact rule cards (spec 3.0 length: family mean <= 800 rendered tokens, instructions
counted twice), card styles, placement and the token report."""
from __future__ import annotations

import pytest

from c2_kit import cards as C
from c2_kit import pipeline
from c2_kit import rows as R
from c2_kit import skin as K
from c2_kit import slots as S
from c2_kit.reference import r00

ITEMS = (
    C.CardItem("group", full='A group applies if one of its User-agent values equals the crawler\'s token, ignoring '
                             'case; if none applies, the "*" group applies.',
               compact='A group applies if a User-agent value equals the token (ignoring case); if none does, the '
                       '"*" group applies.',
               short='Group: token equal (ignoring case), if none the "*" group.'),
    C.CardItem("longest", full="Among the matching lines, the line with the longest pattern decides.",
               compact="Of the matching lines, the longest pattern decides."),
    C.CardItem("limit", full="An amount of more than {LIMIT} needs approval.",
               compact="Amounts more than {LIMIT} need approval."),
    C.CardItem("status", full="A 4xx status means the crawler may fetch any URL.",
               compact="4xx status: may fetch any URL.", when=lambda spec: spec["status"]),
)


def _card(**kw):
    return C.CardSpec("T99", ITEMS, heads={"full": "Rules:", "compact": "Rules (short):"}, tail="These rules are complete.",
                      **kw)


def test_variants_keep_meaning_markers():
    assert _card().problems() == []
    full = 'Amounts of at least {LIMIT} need approval; the "*" group applies only if no group matches, within 30 days.'
    assert C.variant_problems(full, 'At least {LIMIT}: approval; "*" group only if no group matches, within 30 '
                                    'days.') == []
    assert any("slots" in p for p in C.variant_problems(full, 'At least the limit: approval; "*" group only if no '
                                                              'group matches, within 30 days.'))
    assert any("quoted" in p for p in C.variant_problems(full, "At least {LIMIT}: approval; the star group only if "
                                                               "no group matches, within 30 days."))
    assert any("numbers" in p for p in C.variant_problems(full, 'At least {LIMIT}: approval; "*" only if no group '
                                                                'matches, within 31 days.'))
    assert any("operator" in p for p in C.variant_problems(full, 'At least {LIMIT}: approval; "*" group if no group '
                                                                 'matches, within 30 days.'))       # "only" dropped
    assert any("negation" in p for p in C.variant_problems(full, 'At least {LIMIT}: approval; "*" group only if a '
                                                                 'group matches, within 30 days.'))
    assert any("operator" in p for p in C.variant_problems(full, 'At least {LIMIT}: approval; "*" group only if '
                                                                 'every group fails to match, within 30 days.'))
    assert any("operator" in p for p in C.variant_problems("Take the longest pattern.", "Take the first pattern."))


def test_templates_per_style_and_conditional_items():
    card = _card()
    full = card.template("full", {"status": True})
    compact = card.template("compact", {"status": False})
    assert full.startswith("Rules:\n1. A group applies") and full.endswith("These rules are complete.")
    assert "4. A 4xx status" in full and "4xx" not in compact and compact.startswith("Rules (short):")
    assert len(compact) < len(full)
    short = card.template("short", {"status": True})
    assert "Group: token equal" in short and "Of the matching lines" in short    # short falls back to compact
    with pytest.raises(C.CardError):
        card.template("none", {"status": True})                                   # no G0 reason
    with pytest.raises(C.CardError):
        card.template("compact")                                                  # conditional items need the spec
    assert C.CardSpec("T99", ITEMS[:3], none_reason="the rules are the reader's own").template("none") == ""


def test_conditional_cards_may_not_cite_item_numbers_and_bullets_may_not_define_yes_no():
    bad = C.CardSpec("T99", ITEMS + (C.CardItem("over", full="The status overrides items 1-3."),))
    assert any("by number" in p for p in bad.problems())
    yes = C.CardSpec("T99", (C.CardItem("y", full="Yes: the request is in scope."),), numbered=False)
    assert any("Yes option" in p for p in yes.problems())


def test_style_draw_is_label_blind_and_capped():
    shares = {"compact": 0.85, "short": 0.15}
    draws = [C.draw_style(f"row-{i}", shares) for i in range(10000)]
    assert draws == [C.draw_style(f"row-{i}", shares) for i in range(10000)]
    assert abs(draws.count("short") / 10000 - 0.15) < 0.015
    with pytest.raises(C.CardError):
        C.draw_style("x", {"compact": 0.8, "short": 0.2})                 # above the G0's 15%
    assert C.draw_style("x", {"compact": 0.8, "short": 0.2}, short_cap=0.2) in ("compact", "short")
    with pytest.raises(C.CardError):
        C.draw_style("x", {"compact": 0.5})


def test_place_rules_uses_the_field_printed_once():
    slots = {"LIMIT": S.cents_slot(5000)}
    filled = K.fill("Rules:\n1. Amounts more than {LIMIT} need approval.", slots, {})
    tb = R.TextBuilder()
    assert C.place_rules(tb, filled, "noul") == "card"
    tb.add("instructions", "Does this need approval?")
    assert tb.text("card").startswith("Rules:") and tb.text("instructions") == "Does this need approval?"
    assert any(sp.slot == "LIMIT" and sp.field == "card" for sp in tb.spans)
    tb2 = R.TextBuilder()
    assert C.place_rules(tb2, filled, "choice") == "instructions"
    assert tb2.text("instructions").endswith("approval.\n\n") and tb2.text("card") is None
    tb3 = R.TextBuilder().add("instructions", "Which?")
    with pytest.raises(C.CardError):
        C.place_rules(tb3, filled, "choice")                              # rules go before the question
    with pytest.raises(C.CardError):
        C.place_rules(R.TextBuilder(), "Rules:\n- No: the request is refused.", "noul")
    assert C.defs_style("card", "compact") == "rules_in_card_compact" and C.defs_style("none", "none") == "no_card"
    assert C.split_rules({"card": "R", "instructions": "Q?"}) == ("R", "Q?")
    assert C.split_rules({"card": None, "instructions": "R1\nR2\n\nQ?"}) == ("R1\nR2", "Q?")
    assert C.split_rules({"card": None, "instructions": "Q?"}) == ("", "Q?")


class _R00Card(r00.R00):
    """R00 with its rule placed by place_rules: on yes/no rows the rule moves to row.card (solver B is R00's own,
    so this only checks the kit side: placement, spans, G-SL, schema and the G15 loader round trip)."""

    def render(self, spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        rr = super().render(spec, ctx, skin=skin, wording=wording, forms=forms, attack=attack)
        if rr.row["qtype"] != "noul":
            return rr
        rule, _sep, question = rr.row["instructions"].partition("\n\n")
        row = dict(rr.row, card=rule, instructions=question)
        row["meta"] = dict(row["meta"], defs_style="rules_in_card_full")
        return type(rr)(row, rr.spans, rr.forms, rr.option_set, rr.skin_id, rr.wording_id, rr.attack_id, rr.register,
                        rr.regions)


def test_card_placement_halves_the_rule_cost_on_yes_no_rows(ctx, plugin):
    p = _R00Card(lexicon=ctx.lexicon)
    specs = [s for s in (plugin.sample(i, "S1") for i in range(60)) if s.qform.startswith("yn_")][:10]
    old = [plugin.render(s, ctx).row for s in specs]
    new = [p.render(s, ctx).row for s in specs]
    a, b = C.token_report(old, real=False), C.token_report(new, real=False)
    assert b["mean"] < a["mean"] and a["after_placement"] == pytest.approx(b["mean"], abs=2)
    for r in new:
        assert R.validate_row(r) == [] and R.g15_check(r)["ok"]


def test_token_report_projection_math():
    rule = "r" * 300                                   # 100 approx tokens
    yn = {"qtype": "noul", "state": "s" * 300, "card": None, "instructions": rule + "\n\n" + "q" * 30, "options": None}
    ch = {"qtype": "choice", "state": "s" * 300, "card": None, "instructions": rule + "\n\n" + "q" * 30,
          "options": ["a", "b"]}
    rep = C.token_report([yn, ch], bar=200, real=False)
    assert rep["rules_mean"] == {"yes_no": 100, "choice": 100}
    assert rep["after_placement"] == pytest.approx(rep["mean"] - 50)          # one yes/no row of two saves 100
    ratio = rep["rules_ratio_needed"]
    assert ratio is not None and 0 < ratio < 1
    # after placement the rules cost (100 + 2 * 100) / 2 = 150 per row; shrinking them by `ratio` reaches the bar
    assert rep["after_placement"] - (1 - ratio) * 150 == pytest.approx(200, abs=0.6)
    assert C.token_report([yn], bar=10_000, real=False)["rules_ratio_needed"] == 1.0
    assert C.token_report([yn], bar=1, real=False)["rules_ratio_needed"] is None


def test_style_report():
    rows = [{"meta": {"defs_style": "rules_in_card_compact"}}] * 85 + [{"meta": {"defs_style": "rules_in_card_short"}}] * 15
    rep = C.style_report(rows)
    assert rep["short_or_none_share"] == 0.15 and rep["verdict"] == "report"


def test_kit_unit_still_passes_with_a_card(ctx):
    """A whole relation unit of the card-placing R00 variant passes the kit gates other than R00's own parser."""
    p = _R00Card(lexicon=ctx.lexicon)
    spec = next(s for s in (p.sample(i, "S1") for i in range(80)) if s.qform == "yn_approved")
    rr = p.render(spec, ctx)
    probs = [g for g, _d in pipeline.check_rendered(p, spec, rr, ctx, run_g15=True)]
    assert set(probs) <= {"G3", "G2"}         # R00's solver B reads its rule from the instructions (expected here)
