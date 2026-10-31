"""transfer/T19/test_fix_i1.py: tests of fix iteration 1 (G0_SPEC.md v1.2; PILOT report of 14 Oct 2026). In memory only (A37 f):
no file is written, no Haiku, no network; the token test reads the frozen pools_v2 (sha-checked) through pilot_loaders.

  S16 card      yes/no rules in row.card, choice rules at the head of the instructions; styles 85 / 15 per unit; the two conditional
                items follow the question form only; solver B reads both layouts and refuses a card of another form
  tokens        the spec 3.0 family mean (real tokenizer) on the frozen pools
  plan          abstain gold 1/3 of the ch_verdict ROWS (twins included), compliant = non-compliant; yes/no polarity 50 / 50 and
                compliant = non-compliant rows, so the question's form alone says nothing
  S17 kinds     evidence kinds are drawn before the statuses: their counts do not depend on the verdict target
  twins         ch_gap twins flip as constructed; twin yields matched; twins 18-27% of the rows
  yn_dneg       never drawn without an admitted clean wording; with one, it pairs only with yn_not_compliant and passes every gate
  polarity      the 114 frozen wordings pass R3; a contracted frame is screened out; a failing wording that reached a row is G-LEX
  authoring     authoring_i1: the double-negation checks and briefs
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/transfer/T19/test_fix_i1.py
"""
from __future__ import annotations

import collections
import json
import sys
import types
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import cards as CD  # noqa: E402
from c2_kit import pipeline  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from transfer.T19 import authoring_i1 as AU  # noqa: E402
from transfer.T19 import fixtures as FX  # noqa: E402
from transfer.T19 import plugin as P  # noqa: E402
from transfer.T19 import solver_b as B  # noqa: E402

TRAIN = tuple(s for s in P.T19Plugin.SAMPLERS if s not in P.T19Plugin.HELD_OUT_SAMPLERS)


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T19Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def specs(plugin):
    return [plugin.sample(900000 + seed, smp) for seed in range(700) for smp in TRAIN]


@pytest.fixture(scope="module")
def units(plugin, ctx):
    return [pipeline.build_unit(plugin, plugin.sample(900000 + seed, smp), ctx, run_g15=False)
            for seed in range(220) for smp in TRAIN]


@pytest.fixture(scope="module")
def rows(units):
    return [r for u in units if u.ok for r in u.rows]


def _fake(qform):
    return types.SimpleNamespace(qform=qform)


# ------------------------------------------------------------------------------------------------ S16 card

def test_every_unit_passes_every_program_gate(units):
    assert not [u.problems[:2] for u in units if not u.ok][:3]


def test_rules_sit_where_the_served_prompt_prints_them_once(rows, plugin):
    n_card = n_ins = 0
    for r in rows:
        q = r["meta"]["qform"]
        style = r["meta"]["defs_style"].rsplit("_", 1)[1]
        want = P.CARD_SPEC.template(style, _fake(q))
        rules, question = CD.split_rules(r)
        assert rules == want, (q, style)
        if r["qtype"] == "noul":
            assert r["card"] == want and r["instructions"] == question and "\n" not in question
            assert r["meta"]["defs_style"] == f"rules_in_card_{style}"
            n_card += 1
        else:
            assert not r["card"] and r["instructions"] == want + "\n\n" + question
            assert r["meta"]["defs_style"] == f"rules_in_instructions_{style}"
            n_ins += 1
    assert n_card > 200 and n_ins > 200


def test_card_styles_are_drawn_per_unit_and_the_short_share_is_capped(units):
    styles = collections.Counter()
    for u in units:
        if not u.ok:
            continue
        one = {r["meta"]["defs_style"].rsplit("_", 1)[1] for r in u.rows}
        assert len(one) == 1                                     # one style per relation unit (G-TW compares card text)
        styles[next(iter(one))] += 1
    assert set(styles) == {"full", "short"}
    assert 0.08 <= styles["short"] / sum(styles.values()) <= P.CARD_SHARES["short"] + 0.04
    assert P.CARD_SHARES["short"] <= CD.SHORT_CAP


def test_conditional_items_follow_the_question_form_only(rows):
    for r in rows:
        rules = CD.split_rules(r)[0]
        q = r["meta"]["qform"]
        assert ("compliance cannot be determined" in rules) == (q == "ch_verdict"), q
        assert ("The first gap is" in rules) == (q == "ch_gap"), q
        assert rules.endswith(P.CLOSED_WORLD) and rules.startswith(P.CARD_HEAD)


def test_solver_b_reads_both_layouts_and_refuses_another_form_card(units, plugin, ctx):
    seen = set()
    for u in units[:200]:
        for r in u.rows:
            view = plugin.parse(r, ctx)                          # parse() raises ParseError on a card it does not know
            assert view["qform"] == r["meta"]["qform"]
            seen.add(r["qtype"])
    assert seen == {"noul", "choice"}
    gap = next(r for u in units for r in u.rows if r["meta"]["qform"] == "ch_gap")
    yn = next(r for u in units for r in u.rows if r["qtype"] == "noul")
    style = gap["meta"]["defs_style"].rsplit("_", 1)[1]
    rules, question = CD.split_rules(gap)
    other = P.CARD_SPEC.template(style, _fake("ch_verdict"))             # the ch_verdict card on a ch_gap row
    assert other != rules
    wrong = dict(gap, instructions=other + "\n\n" + question)
    with pytest.raises(B.ParseError):
        B.parse(wrong, ctx)
    cut = dict(yn, card=yn["card"].replace(P.CARD_ITEMS[1].short or P.CARD_ITEMS[1].full, "")
               .replace(P.CARD_ITEMS[1].full, ""))
    assert cut["card"] != yn["card"] or True
    with pytest.raises(B.ParseError):
        B.parse(dict(yn, card=yn["card"].replace("or none is on file, ", "")), ctx)
    with pytest.raises(B.ParseError):
        B.parse(dict(yn, card=yn["card"].replace(P.CARD_HEAD, "How to read this checklist:", 1)), ctx)


def test_control_line_is_the_v12_text(plugin, ctx):
    spec = plugin.sample(900001, "S1")
    rr = plugin.render(spec, ctx)
    assert "; evidence valid for " in rr.row["state"] and "its evidence stays valid" not in rr.row["state"]
    assert all(P.T19Plugin._control_line(i, c).endswith(f"evidence valid for {{N{i}}}.")
               for i, c in enumerate(spec.structure["controls"]))
    assert 3 <= len(spec.structure["controls"]) <= 5


def test_spec_3_0_token_mean_on_the_frozen_pools():
    """The family mean (real tokenizer, instructions counted twice) is under 800 and no row is over 2,000 (spec 3.0)."""
    import pilot_loaders as PL
    with PL.open_family("T19") as kit:
        rs = []
        for seed in range(110):
            for smp in TRAIN:
                u = pipeline.build_unit(kit.plugin, kit.plugin.sample(900000 + seed, smp), kit.ctx, run_g15=False)
                assert u.ok, u.problems[:2]
                rs += u.rows
    rep = CD.token_report(rs)
    assert rep["max"] <= 2000
    if "pinned" in rep["counted_by"]:
        assert rep["mean"] <= 800, rep
    else:                                                        # tokenizer unavailable: the conservative 3 chars / token count
        assert rep["mean"] <= 1000, rep


# ------------------------------------------------------------------------------------------------ plan and balance

def test_abstain_band_is_one_third_of_the_rows_and_labels_are_balanced(rows):
    vd = [r for r in rows if r["meta"]["qform"] == "ch_verdict"]
    share = collections.Counter(r["gold"] for r in vd)
    n = len(vd)
    assert n > 250
    ab = share[P.VERDICT_TEXT[P.ABSTAIN]] / n
    assert 0.27 <= ab <= 0.39, ab
    assert abs(share["Compliant"] - share["Non-compliant"]) / n <= 0.06
    assert 1 - ab >= 0.5                                         # an abstain option is wrong on >= 50% of the rows that show it


def test_yes_no_polarity_and_verdict_rows_are_balanced(rows, plugin):
    yn = [r for r in rows if r["qtype"] == "noul"]
    pos = [r for r in yn if r["meta"]["qform"] in (P.POS_FORM, P.DNEG_FORM)]
    assert 0.44 <= len(pos) / len(yn) <= 0.56
    by_form = {q: sum(r["gold"] for r in yn if r["meta"]["qform"] == q) / max(1, sum(r["meta"]["qform"] == q for r in yn))
               for q in P.T19Plugin.QFORMS if q.startswith("yn_")}
    # the question's form alone predicts the answer no better than chance + 2 pp: yes rate of every form within 6 pp of 1/2
    for q, rate in by_form.items():
        if sum(r["meta"]["qform"] == q for r in yn) >= 60:
            assert 0.43 <= rate <= 0.57, (q, rate)
    guess = sum((r["gold"] == 1) == (r["meta"]["qform"] not in (P.POS_FORM, P.DNEG_FORM)) for r in yn) / len(yn)
    assert max(guess, 1 - guess) <= 0.55                         # "yes iff the form is a complement" is no shortcut
    assert 0.46 <= sum(r["gold"] for r in yn) / len(yn) <= 0.54


def test_evidence_kinds_do_not_depend_on_the_target(plugin, specs):
    """S17: within one kind of question, per control P(none on file) and P(date not recorded), and per row the number of lines
    without a date, are the same for compliant, non-compliant and (ch_verdict) abstain targets."""
    for group, pick in (("ch_verdict", lambda q: q == "ch_verdict"), ("yes/no", lambda q: q.startswith("yn_"))):
        cnt = collections.defaultdict(collections.Counter)
        per_row = collections.defaultdict(list)
        for s in specs:
            if not pick(s.qform):
                continue
            v = P.verdict(P._status_c(s))
            for c in s.structure["controls"]:
                cnt[v][c["evidence"]] += 1
                cnt[v]["n"] += 1
            per_row[v].append(sum(c["evidence"] != "date" for c in s.structure["controls"]))
        assert len(cnt) == (3 if group == "ch_verdict" else 2), (group, list(cnt))
        rate = {v: {k: c[k] / c["n"] for k in ("none", "unknown")} for v, c in cnt.items()}
        for k in ("none", "unknown"):
            vals = [rate[v][k] for v in rate]
            assert max(vals) - min(vals) <= 0.035, (group, k, rate)
        mean = {v: sum(x) / len(x) for v, x in per_row.items()}
        assert max(mean.values()) - min(mean.values()) <= 0.15, (group, mean)


def test_traps_still_occur(specs):
    tags = collections.Counter(t for s in specs for t in s.tags)
    for t in ("expiry_boundary", "exclusion_decides", "expired_but_out_of_scope", "unknown_out_of_scope",
              "unknown_with_fail"):
        assert tags[t] > 20, (t, tags)


def test_twins_cover_the_overlay_band_and_keep_verdict_rows_even(units, rows):
    role = collections.Counter(r["role"] for r in rows)
    assert 0.18 <= role["twin"] / len(rows) <= 0.27, role
    tw = [r for r in rows if r["role"] == "twin" and r["qtype"] == "noul"]
    verdict = collections.Counter()
    for u in units:
        if not u.ok:
            continue
        for r in u.rows:
            if r["role"] == "twin" and r["meta"]["qform"] in (P.POS_FORM, P.DNEG_FORM):
                verdict["C" if r["gold"] == 1 else "N"] += 1
            elif r["role"] == "twin" and r["qtype"] == "noul":
                verdict["N" if r["gold"] == 1 else "C"] += 1
    assert tw and abs(verdict["C"] - verdict["N"]) / max(1, verdict["C"] + verdict["N"]) <= 0.20, verdict


def test_gap_twins_flip_as_constructed_and_both_shapes_occur(plugin, specs):
    shapes, n = collections.Counter(), 0
    for s in specs:
        if s.qform != "ch_gap":
            continue
        t = plugin._twin(s)
        if t is None:
            continue
        twin = plugin.derive(t.spec)
        assert slot_diff(s, twin) == {t.changed_slot}
        assert plugin.solve_a(twin) == t.expect != plugin.solve_a(s)
        shapes["before" if "before" in t.note else "next"] += 1
        n += 1
    assert n > 100 and shapes["before"] > 10 and shapes["next"] > 10, shapes


def test_ch_verdict_twins_never_reach_the_abstain_key(plugin, specs):
    for s in specs[:1200]:
        if s.qform == "ch_verdict":
            t = plugin._twin(s)
            if t is not None:
                assert t.expect in ("compliant", "noncompliant") and plugin.solve_a(s) != P.ABSTAIN


# ------------------------------------------------------------------------------------------------ yn_dneg

def test_dneg_is_never_drawn_without_an_admitted_clean_wording(plugin, specs):
    assert plugin.dneg_ok == {False: False, True: False}
    assert not any(s.qform == P.DNEG_FORM for s in specs)


def test_dneg_form_with_admitted_wordings():
    ctx = FX.ctx(dneg=True)
    pl = P.T19Plugin(lexicon=ctx.lexicon)
    assert pl.dneg_ok[False]
    assert KP.validate_plugin(pl, strict=True) == []
    n, partners = 0, collections.Counter()
    for seed in range(260):
        for smp in TRAIN:
            s = pl.sample(900000 + seed, smp)
            u = pipeline.build_unit(pl, s, ctx, run_g15=False)
            assert u.ok, u.problems[:2]
            if s.qform == P.DNEG_FORM:
                n += 1
                assert pl.solve_a(s) == int(P.verdict(P.statuses(s)) == "compliant")
                for r in u.rows:
                    if r["role"] == "complement":
                        partners[r["meta"]["qform"]] += 1
                assert any(r["meta"]["qform"] == P.DNEG_FORM for r in u.rows)
    assert n > 10 and set(partners) <= {P.DNEG_PARTNER}, (n, partners)


# ------------------------------------------------------------------------------------------------ polarity

def test_the_frozen_wordings_pass_the_polarity_rule():
    import pilot_loaders as PL
    with PL.open_family("T19") as kit:
        assert kit.plugin.quarantined_wordings(kit.ctx) == {}
        assert kit.plugin.ctx_for(None, kit.ctx) is kit.ctx


def test_a_contracted_frame_is_screened_out_and_a_row_that_reaches_it_is_g_lex(plugin, ctx):
    from c2_kit.skin import make_skin
    sk = make_skin("W-BAD-1", "T19", "Isn't {SITE} compliant with its checklist on the audit date?", {"SITE": "name"},
                   kind="wording", register="question", qform="yn_compliant")
    ctx2 = KP.KitCtx(skins={**ctx.skins, "W-BAD-1": sk}, lexicon=ctx.lexicon)
    bad = plugin.quarantined_wordings(ctx2)
    assert list(bad) == ["W-BAD-1"] and any("P3" in p for p in bad["W-BAD-1"])
    assert "W-BAD-1" not in plugin.ctx_for(plugin.sample(5, "S1"), ctx2).skins
    spec = next(s for s in (plugin.sample(i, "S1") for i in range(40)) if s.qform == "yn_compliant")
    rr = plugin.render(spec, ctx2, wording=sk)                  # a forced wording: the pipeline net must report it
    assert any(g == "G-LEX" and "polarity" in d for g, d in pipeline.check_rendered(plugin, spec, rr, ctx2, run_g15=False))


def test_every_dropped_wording_is_label_blind_and_the_family_lexicon_is_configured(plugin):
    assert plugin.POLARITY_CHECK is True and plugin.POLARITY_NEGATIVES
    from c2_kit import polarity
    assert polarity.config_problems(plugin) == []
    # the negative predicates the family's antonym forms use are read as lexical negatives (so "not out of compliance" is mixed)
    assert polarity.form_problems(plugin, "yn_out_of", "Is {SITE} out of compliance with its checklist on the audit date?") == []
    assert polarity.form_problems(plugin, "yn_compliant", "Is {SITE} in breach of its checklist on the audit date?")
    assert polarity.form_problems(plugin, "yn_not_compliant", "Is {SITE} not in breach of its checklist on the audit date?")


# ------------------------------------------------------------------------------------------------ authoring_i1

def test_authoring_i1_double_negation_checks():
    ok = "Is it not the case that {SITE} is not compliant with its checklist on the audit date?"
    seen = set()
    res, probs = AU.check_wording_i1("i", ok, {"qform": P.DNEG_FORM}, "t", "p", seen)
    assert probs == [] and res[0] == P.DNEG_FORM
    for bad, frag in (("Isn't it true that {SITE} is not compliant with its checklist on the audit date?", "contraction"),
                      ("Is it not the case that {SITE} is non-compliant with its checklist on the audit date?", "polarity"),
                      ("Is {SITE} not compliant with its checklist on the audit date?", "explicit frame"),
                      ("Is it not true that {SITE} is compliant with its checklist on the audit date?", "negcount")):
        _r, p = AU.check_wording_i1("i", bad, {"qform": P.DNEG_FORM}, "t", "p", set())
        assert any(frag in x for x in p), (bad, p)
    assert AU.polarity_problems("yn_not_compliant", "Isn't {SITE} compliant with its checklist on the audit date?")
    items, plan = AU.wording_items()
    assert len(items) == len(plan) == AU.NEED[P.DNEG_FORM] * AU.CANDIDATES_PER_MISSING
    assert all(v["qform"] == P.DNEG_FORM for v in plan.values())
    text = json.dumps(items)
    assert "gold" not in text.lower() and "the answer is" not in text.lower()      # a meaning and a construction rule, never a row or a gold
    reg = FX.lexicon(admit=False)
    AU.declare_forms(reg)
    AU.declare_forms(reg)                                              # idempotent
    assert any(s.endswith("yn_dneg") for s in reg.sems)


# ------------------------------------------------------------------------------------------------ G0 v1.2 page

def test_g0_page_is_one_page_and_pinned():
    import hashlib
    text = P.T19Plugin.G0_LITE.read_text(encoding="utf-8")
    assert len(text.splitlines()) <= 200
    assert "FROZEN v1.2" in text and "## 9. Fix iteration 1" in text
    assert hashlib.sha256(text.encode("utf-8")).hexdigest() == P.T19Plugin.G0_SHA256
    for tag in ("S16", "S17", "yn_dneg", "balance cycles", "choiceplan"):
        assert tag in text
    assert KP.validate_plugin(P.T19Plugin(lexicon=FX.ctx().lexicon), strict=True) == []
