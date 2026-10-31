"""c2_build/families/T12/test_i1_fixes.py: tests of the T12 fix iteration 1 (G0_SPEC_v2_2.md; the Stage B pilot verdict
F1-F4; kit changes: cards, polarity). CPU only, in memory: nothing is written.

  F1  wording screen   the 4 premise wordings of ch_price_line, the 2 price-check wordings that tie the check to the
                       decision and the 1 contracted-frame held-out yn_dneg_release wording are quarantined by their
                       TEXT (7 of 217 pool wordings); every other pool wording stays; no row uses a quarantined one;
                       authoring.check_wording(screen=True) rejects them, screen=False (the frozen pool stage) does not
  F2  packs            the 32 training cards use 32 distinct packs (spec 3.0: >= 25, one per card); S5 uses others
  F3  length           yes/no rules sit in row.card (printed once), choice rules at the head of the instructions; both
                       card styles parse back and keep every CardItem marker; the mean of the pool-ctx rows is under
                       the spec 3.0 bar (real tokenizer) and no row exceeds 2,000; no date and no line total is printed
  pol polarity         the kit rule P1-P3 with the T12 negative predicates
  G0                   G0_SPEC_v2_2.md is the pinned page (<= 200 lines); G0_SPEC.md (v2.1) keeps the authored sha
Run (from lean/):  ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T12/test_i1_fixes.py
"""
from __future__ import annotations

import collections
import hashlib
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pytest  # noqa: E402

from c2_kit import cards as CARDS  # noqa: E402
from c2_kit import pipeline  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from c2_kit.cards import split_rules  # noqa: E402
from families.T12 import authoring as A  # noqa: E402
from families.T12 import fixtures as FX  # noqa: E402
from families.T12 import freeze_v2 as FZ  # noqa: E402
from families.T12 import plugin as P  # noqa: E402
from families.T12 import solver_b as B  # noqa: E402
from families.T12 import wording_screen as WS  # noqa: E402

TRAIN = ("S1", "S2", "S3", "S4")
HERE = Path(__file__).resolve().parent

F1_TEXTS = (
    "Under the AP policy, which line of invoice {INVOICE_ID}, if any, fails the price check and drives the end result?",
    "Which line on invoice {INVOICE_ID}, if any, fails the price check and so shapes the result this policy reaches?",
    "Is the outcome for invoice {INVOICE_ID} under this policy driven by any line that fails the price check, and which "
    "line, if any?",
    "Does the policy's treatment of invoice {INVOICE_ID} point to any line that fails the price check, and which line, "
    "if any?",
)
PRICE_TIE_TEXTS = (
    "Does what the policy decides for invoice {INVOICE_ID} mean it fails the price check taken on its own?",
    "When the policy decides on invoice {INVOICE_ID}, does that invoice fail the price check taken on its own?",
)
CONTRACTED = "Isn't it accurate that bill {INVOICE_ID} is not released for payment, according to the card?"


@pytest.fixture(scope="module")
def pools():
    return FZ.load_pools()


@pytest.fixture(scope="module")
def pool_ctx(pools):
    return FZ.make_ctx(pools)


@pytest.fixture(scope="module")
def pool_plugin(pools, pool_ctx):
    with FZ.packs_installed(pools):
        yield P.T12Plugin(lexicon=pool_ctx.lexicon)


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T12Plugin(lexicon=ctx.lexicon)


# ------------------------------------------------------------------------------------------------ F1: wording screen

def test_premise_rule_flags_the_f1_wordings_and_nothing_else_on_ch_price_line():
    for t in F1_TEXTS:
        assert WS.premise_problems(t, "ch_price_line"), t
    ok = ("Which line on invoice {INVOICE_ID} fails the price check, if any?",
          "Looking at the outcome for invoice {INVOICE_ID} as this policy sets it, which line, if any, fails the price "
          "check?",
          "Given the outcome this policy gives invoice {INVOICE_ID}, which line, if any, fails the price check?")
    for t in ok:
        assert WS.premise_problems(t, "ch_price_line") == [], t
    for t in PRICE_TIE_TEXTS:
        assert WS.premise_problems(t, "yn_over_tol") and WS.premise_problems(t, "yn_within_tol"), t
    assert WS.premise_problems("Taken on its own, does invoice {INVOICE_ID} fail the price check?", "yn_over_tol") == []
    assert WS.premise_problems(F1_TEXTS[0], "ch_action") == []              # the rule is per form


def test_the_pool_quarantine_is_exactly_the_seven_wordings(pool_plugin, pool_ctx):
    bad = pool_plugin.quarantined_wordings(pool_ctx)
    texts = {pool_ctx.skin(sid).text: sid for sid in bad}
    assert len(bad) == 7
    assert set(F1_TEXTS) | set(PRICE_TIE_TEXTS) | {CONTRACTED} == set(texts)
    assert sum(1 for s in pool_ctx.skins.values() if s.kind == "wording") == 217
    screened = pool_plugin.ctx_for(None, pool_ctx)
    assert not set(bad) & set(screened.skins)
    assert set(pool_ctx.skins) - set(screened.skins) == set(bad)
    n_price = [s for s in screened.skins.values() if s.kind == "wording" and s.qform == "ch_price_line"]
    assert len(n_price) == 14                                              # 18 in the pool, 4 quarantined
    assert any(s.held_out for s in n_price)                                # S5 keeps its held-out wordings


def test_no_row_uses_a_quarantined_wording(pool_plugin, pool_ctx, pools):
    bad = set(pool_plugin.quarantined_wordings(pool_ctx))
    used = collections.Counter()
    with FZ.packs_installed(pools):
        for seed in range(120):
            for smp in pool_plugin.SAMPLERS:
                spec = pool_plugin.sample(seed, smp)
                rr = pool_plugin.render(spec, pool_ctx)
                used[rr.wording_id] += 1
                for p in pool_plugin.relations(spec):
                    if p.kind == "complement":
                        s2 = spec.replace(qform=p.qform)
                        used[pool_plugin.render(s2, pool_ctx).wording_id] += 1
    assert used and not set(used) & bad


def test_check_wording_screen_flag_is_opt_in_so_the_frozen_pool_stage_is_unchanged():
    for t in F1_TEXTS:
        assert A.check_wording(t, "ch_price_line") == [], A.check_wording(t, "ch_price_line")      # pool stage (frozen)
        assert any("premise" in p for p in A.check_wording(t, "ch_price_line", screen=True)), t
    assert any("P3" in p for p in A.check_wording(CONTRACTED, "yn_dneg_release", held_out=True, screen=True))
    for _wid, qf, text, held in FX.WORDINGS:                                # the stand-ins pass the screen too
        assert A.check_wording(text, qf, held_out=held, screen=True) == [], (text, A.check_wording(
            text, qf, held_out=held, screen=True))


def test_polarity_rule_with_the_t12_negative_predicates(plugin):
    fp = lambda q, t: POL.form_problems(plugin, q, t)                      # noqa: E731
    assert fp("yn_dneg_release", "Is it not true that invoice {INVOICE_ID} is not released for payment?") == []
    assert fp("yn_not_release", "Is invoice {INVOICE_ID} not released for payment under this policy?") == []
    assert fp("yn_payment_stopped", "Does this policy stop payment of invoice {INVOICE_ID}?") == []
    assert fp("yn_over_tol", "Taken on its own, does invoice {INVOICE_ID} fail the price check?") == []
    assert fp("yn_within_tol", "Taken on its own, does invoice {INVOICE_ID} pass the price check?") == []
    assert any("P3" in p for p in fp("yn_not_release", "Isn't invoice {INVOICE_ID} released for payment?"))
    # a syntactic negation over a negative predicate: the inverted class of the T35 pilot (P1)
    assert any("P1" in p for p in fp("yn_payment_stopped", "Is it not the case that the policy stops payment of "
                                                           "invoice {INVOICE_ID}?"))
    assert any("P1" in p for p in fp("yn_over_tol", "Does invoice {INVOICE_ID} not fail the price check on its own?"))
    # a negative predicate in a positive-polarity form reads with the wrong polarity (P2)
    assert any("P2" in p for p in fp("yn_release", "Does the policy block payment of invoice {INVOICE_ID}?"))
    assert POL.config_problems(plugin) == []


# ------------------------------------------------------------------------------------------------ F2: packs

def test_cards_use_distinct_packs_one_per_card(pool_plugin, pools):
    assert P.N_CARDS == 8 and len(pools["packs"]) == 46
    with FZ.packs_installed(pools):
        cards = {}
        for smp in pool_plugin.SAMPLERS:
            n = P.N_CARDS_S5 if smp == "S5" else P.N_CARDS
            for idx in range(n):
                c = pool_plugin._draw_card(smp, idx, n)
                cards[(smp, idx)] = c["pack"]["id"]
        train = [v for (s, _), v in cards.items() if s != "S5"]
        held = [v for (s, _), v in cards.items() if s == "S5"]
        assert len(train) == 32 and len(set(train)) == 32                  # one pack per card, >= 25 (spec 3.0)
        assert len(set(held)) == len(held) and not set(held) & set(train)  # S5 packs are disjoint
        seen = {pool_plugin.sample(seed, smp).pack for seed in range(200) for smp in TRAIN}
        assert len(seen) == 32


# ------------------------------------------------------------------------------------------------ F3: cards and length

def test_every_card_item_variant_keeps_its_markers():
    for it in P.CARD_ITEMS:
        for style in ("compact", "short"):
            txt = getattr(it, style)
            if txt is not None:
                assert CARDS.variant_problems(it.full, txt) == [], (it.item_id, style)
    assert CARDS.draw_style("x|S1|1", P.CARD_SHARES) in ("full", "short")
    assert P.CARD_SHARES["short"] <= CARDS.SHORT_CAP
    assert P.CLOSED_WORLD == P.T12Plugin.CLOSED_WORLD_SENTENCE


def test_rules_are_placed_where_the_prompt_prints_them_and_solver_b_reads_them(plugin, ctx):
    seen = collections.Counter()
    for seed in range(120):
        for smp in plugin.SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            row, ds = rr.row, rr.row["meta"]["defs_style"]
            rules, question = split_rules(row)
            assert P.CLOSED_WORLD in rules and "\n\n" not in rules.strip("\n")
            if row["qtype"] == "noul":
                assert row["card"] == rules and row["instructions"] == question and "\n\n" not in question
                assert ds == f"rules_in_card_{spec.structure['card_style']}"
            else:
                assert row["card"] is None and row["instructions"] == rules + "\n\n" + question
                assert ds == f"rules_in_instructions_{spec.structure['card_style']}"
            view = B.parse(row, ctx)
            assert view["card_style"] == spec.structure["card_style"]
            assert pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False) == []
            seen[ds] += 1
    assert set(seen) == {"rules_in_card_full", "rules_in_card_short", "rules_in_instructions_full",
                         "rules_in_instructions_short"}


def test_card_style_is_label_blind_and_shared_by_a_unit(plugin, ctx):
    short = {0: 0, 1: 0}
    n = {0: 0, 1: 0}
    for seed in range(400):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            g = plugin.solve_a(spec) if spec.qform.startswith("yn_") else None
            if g is not None:
                short[g] += spec.structure["card_style"] == "short"
                n[g] += 1
            for p in plugin.relations(spec):                               # twins, equiv and complements share it
                if p.kind in ("twin", "complement"):
                    st2 = (p.spec.structure if p.spec is not None else spec.structure)["card_style"]
                    assert st2 == spec.structure["card_style"]
    share = {g: short[g] / n[g] for g in n}
    assert all(0.10 <= v <= 0.20 for v in share.values()), share           # about 15% (spec 3.0), both golds
    assert abs(share[0] - share[1]) <= 0.04


def test_no_date_and_no_line_total_is_printed(plugin, ctx):
    for seed in range(60):
        for smp in plugin.SAMPLERS:
            spec = plugin.sample(seed, smp)
            row = plugin.render(spec, ctx).row
            state = row["state"].lower()
            assert not re.search(r"\b(date|dated)\b|receipt_date|invoice_date", state), row["state"]
            for word in ("line total", "line_total"):
                assert word not in state, (word, row["state"])
            assert "GR_DATE" not in spec.slots and "INV_DATE" not in spec.slots
            assert not any(k.startswith(("PO_LT", "INV_LT")) for k in spec.all_slots())
            assert "gr_date" not in plugin.canonical(spec) and "po_total" not in plugin.canonical(spec)["lines"][0]
            assert "total" in state                                        # the document totals stay


def test_the_family_mean_is_under_the_spec_bar_and_no_row_is_over_2000(pool_plugin, pool_ctx, pools):
    """Spec 3.0: family mean <= 800, every row <= 2,000 (instructions twice, the card once), counted with the pinned
    Qwen3.5-4B tokenizer (c_build/mixer.token_counts) on a pilot-like row mix over the frozen pools_v2 ctx."""
    rows = []
    with FZ.packs_installed(pools):
        for seed in range(150):
            for smp in TRAIN:
                res = pipeline.build_unit(pool_plugin, pool_plugin.sample(seed, smp), pool_ctx, run_g15=False)
                assert res.ok, res.problems[:2]
                rows += res.rows
    rep = CARDS.token_report(rows)
    if rep["counted_by"].startswith("rows.approx"):
        pytest.skip("the pinned tokenizer is not available")
    assert rep["max"] <= 2000
    assert rep["mean"] <= 800, rep
    assert 0.45 <= rep["yes_no_share"] <= 0.55


def test_ch_action_and_ch_price_line_golds_are_balanced_inside_a_block(plugin):
    """G0 v2.2 R15 / R16: over any run of consecutive seeds inside a block of BLOCK seeds, for each stratum (ch_action:
    the card's check set; ch_price_line: the line count) every outcome (each action; none and each line) is the gold
    within +- 1 across the four training samplers taken together (one shared sequence), so a pilot sample is not
    unbalanced by chance (which an options-only reader would learn: Stage B patterns, G6). The pilot's seeds
    900000-900145 and another run both qualify; S5 has a sequence of its own."""
    assert P.BLOCK >= 1024
    n_checked = 0
    for samplers in (TRAIN, ("S5",)):
        for run in (range(900000, 900146), range(902000, 902200)):
            assert run[0] // P.BLOCK == run[-1] // P.BLOCK
            act, line = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
            for seed in run:
                for smp in samplers:
                    spec = plugin.sample(seed, smp)
                    if spec.qform == "ch_action":
                        act[tuple(sorted(spec.structure["checks"]))][plugin.solve_a(spec)] += 1
                    elif spec.qform == "ch_price_line":
                        ans = plugin.solve_a(spec)
                        line[spec.structure["n"]][ans if ans == P.NONE_LINE else plugin._items(spec).index(ans)] += 1
            for checks, cnt in act.items():
                vals = [cnt[a] for a in P._verdicts(checks)]
                assert max(vals) - min(vals) <= 1, (samplers, run[0], checks, dict(cnt))
                n_checked += 1
            for n, cnt in line.items():
                vals = [cnt[o] for o in [P.NONE_LINE] + list(range(n))]
                assert max(vals) - min(vals) <= 1, (samplers, run[0], n, dict(cnt))
                n_checked += 1
    assert n_checked >= 20


def test_skins_wordings_and_registers_spread_over_the_pool(pool_plugin, pool_ctx, pools):
    """G0 v2.2 R21: the register draw is low-discrepancy and the skin and wording picks are round-robin over a block, so a
    1,000-row pilot keeps every register under 15%, every wording under 2% and no skin above a few units (spec 3.0)."""
    regs, skins, wordings, n = collections.Counter(), collections.Counter(), collections.Counter(), 0
    with FZ.packs_installed(pools):
        for seed in range(900000, 900146):
            for smp in TRAIN:
                spec = pool_plugin.sample(seed, smp)
                rr = pool_plugin.render(spec, pool_ctx)
                regs[rr.register] += 1
                skins[rr.skin_id] += 1
                wordings[rr.wording_id] += 1
                n += 1
    assert max(regs.values()) / n <= 0.15 and min(regs.values()) / n >= 0.10, dict(regs)
    assert max(wordings.values()) / n <= 0.02, wordings.most_common(3)
    assert max(skins.values()) <= 3, skins.most_common(3)                    # base units only; units add twin rows


def test_distribution_constants_follow_g0_v2_2(plugin):
    assert abs(sum(w for _, w in P.LINES_W) - 1) < 1e-9 and [k for k, _ in P.LINES_W] == [1, 2, 3, 4]
    assert abs(sum(s for _, s in P.QFORM_SHARES) - 1) < 1e-9
    assert (P.DUP_P, P.LIMIT_P) == (0.4, 0.4)
    specs = [plugin.sample(s, smp) for s in range(300) for smp in TRAIN]
    for chk in ("dup", "limit"):
        assert abs(sum(chk in s.structure["checks"] for s in specs) / len(specs) - 0.4) <= 0.04
    yn = sum(s.qform.startswith("yn_") for s in specs) / len(specs)
    assert abs(yn - 0.45) <= 0.04


# ------------------------------------------------------------------------------------------------ G0 pins

def test_the_g0_pages_are_pinned():
    v22 = HERE / "G0_SPEC_v2_2.md"
    assert Path(P.T12Plugin.G0_LITE) == v22
    assert hashlib.sha256(v22.read_bytes()).hexdigest() == P.T12Plugin.G0_SHA256
    assert len(v22.read_text(encoding="utf-8").splitlines()) <= 200
    v21 = HERE / "G0_SPEC.md"                                              # untouched: the pools were authored under it
    assert hashlib.sha256(v21.read_bytes()).hexdigest() == P.G0_SHA256_AUTHORED != P.T12Plugin.G0_SHA256
    text = v22.read_text(encoding="utf-8")
    assert "v2.2, FROZEN" in text and "## 7. v2.2 changes" in text
    assert KP.validate_plugin(P.T12Plugin(lexicon=FX.ctx().lexicon), strict=True) == []
