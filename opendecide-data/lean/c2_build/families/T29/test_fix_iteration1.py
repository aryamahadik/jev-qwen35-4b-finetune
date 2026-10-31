"""c2_build/families/T29/test_fix_iteration1.py: tests of the T29 fix iteration 1 (PILOT_VERDICT FIX-1..9; G0 v1.2).

CPU only, in memory: no test writes a file. Most tests use the stand-in ctx of fixtures.py and the six stand-in packs;
the "pool" tests open the real frozen pools through pilot_loaders (read only, sha256-checked). Run (from lean/):
  ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T29/test_fix_iteration1.py
Checks: placement of the card (FIX-2), equal-length labels (FIX-7), the confirmation clause and the quarantined forms
(FIX-1), the double-negation form, its polarity rule and its fallback (FIX-6), twin / premise tags and card depth (FIX-8),
one partner per yes/no unit, yes rate / abstain / verdict balance at pilot size (FIX-3, FIX-4, FIX-5, kit choiceplan),
registers and the pack pool (FIX-9), and the Haiku brief of the double-negation round.
"""
from __future__ import annotations

import collections
import contextlib
import dataclasses
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pytest  # noqa: E402

from c2_kit import cards as CARDS  # noqa: E402
from c2_kit import pipeline, polarity  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from families.T29 import authoring as A  # noqa: E402
from families.T29 import balance_sim as BS  # noqa: E402
from families.T29 import fixtures as FX  # noqa: E402
from families.T29 import plugin as P  # noqa: E402
from families.T29 import solver_b as B  # noqa: E402
import negcount  # noqa: E402  (c_src/common: on sys.path once c2_kit.paths is imported)

TRAIN = ("S1", "S2", "S3", "S4")


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T29Plugin(lexicon=ctx.lexicon, packs=P.PACKS)


@pytest.fixture(scope="module")
def pool():
    """The real frozen pools (read only): plugin, ctx."""
    import pilot_loaders as PL
    with contextlib.ExitStack() as st:
        kit = st.enter_context(PL.open_family("T29"))
        yield kit


@pytest.fixture(scope="module")
def sim_rows(plugin):
    """Three pilot-size row mixes (1,000 rows each, different seed bases), without rendering."""
    return [BS.simulate(plugin, 1000, 900_000 + j * 7_000_000) for j in range(3)]


# ------------------------------------------------------------------------------------------------ FIX-2: placement

def test_a_yes_no_row_prints_the_card_once_and_a_choice_row_keeps_it_in_the_instructions(plugin, ctx):
    seen = collections.Counter()
    for seed in range(60):
        for smp in TRAIN:
            rr = plugin.render(plugin.sample(seed, smp), ctx)
            row = rr.row
            rules, question = CARDS.split_rules(row)
            assert rules.startswith("Policy") and P.CLOSED_WORLD in rules
            style = row["meta"]["defs_style"].rsplit("_", 1)[1]
            assert style in ("compact", "short")                       # G0 v1.5: no row is served in the full phrasing
            if row["qtype"] == "noul":
                assert row["card"] == rules and row["instructions"] == question
                assert "Rules:" not in row["instructions"] and "\n" not in question
                assert row["meta"]["defs_style"] == f"rules_in_card_{style}"
                assert not any(ln.startswith(("- Yes: ", "- No: ")) for ln in row["card"].split("\n"))
            else:
                assert row["card"] is None and rules in row["instructions"]
                assert row["meta"]["defs_style"] == f"rules_in_instructions_{style}"
            seen[row["qtype"]] += 1
    assert seen["noul"] > 40 and seen["choice"] > 40


def test_the_question_region_is_the_whole_instructions_of_a_yes_no_row(plugin, ctx):
    spec = next(s for s in (plugin.sample(i, "S1") for i in range(80)) if s.qform.startswith("yn_"))
    rr = plugin.render(spec, ctx)
    fld, a, b = rr.regions[rr.wording_id]
    assert fld == "instructions" and (a, b) == (0, len(rr.row["instructions"]))


# ------------------------------------------------------------------------------------------------ FIX-7: labels

def test_verdict_labels_and_code_words_have_one_length():
    assert {len(t) for t in P.VERDICT_TEXT.values()} == {18}
    assert {len(w) for w in P.CODE_WORDS} == {6} and len(set(P.CODE_WORDS)) == 4
    assert set(B.OPTION_KEY) == set(P.VERDICT_TEXT.values())


def test_no_verdict_option_is_the_longest_by_itself(plugin, ctx):
    n = 0
    for seed in range(120):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            if spec.qform != "ch_verdict":
                continue
            opts = plugin.render(spec, ctx).row["options"]
            assert len({len(o) for o in opts}) == 1                  # all options tie: gold-is-longest is exactly 1 / k
            n += 1
    assert n > 100


def test_the_new_labels_are_not_in_any_frozen_wording(pool):
    texts = " ".join(sk.text.lower() for sk in pool.ctx.skins.values() if sk.kind == "wording")
    for t in list(P.VERDICT_TEXT.values()) + list(P.CODE_WORDS):
        assert t.lower() not in texts, t


# ------------------------------------------------------------------------------------------------ FIX-1: confirmation

def test_the_card_says_what_counts_as_an_explicit_confirmation(plugin, ctx):
    clause = "A quoted user line that clearly tells the agent to run the named call counts as one."
    assert P.CONFIRM_LINE.endswith(clause) and P.CONFIRM_LINE in B.CONFIRM_LINES        # the full phrasing (G0 S13)
    assert {P.CARD_ITEMS["confirm"].text(s) for s in ("full", "compact", "short")} == B.CONFIRM_LINES
    assert P.CARD_SPEC.problems() == []                  # compact / short keep slots, numbers, operators, negation count
    shown = hidden = 0
    for seed in range(80):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            rules = CARDS.split_rules(plugin.render(spec, ctx).row)[0]
            assert any(ln in B.CONFIRM_LINES for ln in rules.split("\n")) == bool(spec.structure["conv"])
            shown += bool(spec.structure["conv"])
            hidden += not spec.structure["conv"]
    assert shown > 40 and hidden > 40


def test_the_formal_directive_confirmation_forms_are_never_drawn(pool):
    pl = pool.plugin
    reg = pool.ctx.lexicon
    for f in P.QUARANTINED_FORMS:
        assert f in reg.forms and reg.status(f) == "admitted"           # still in the frozen registry ...
    drawn = set()
    for seed in range(400):
        for smp in TRAIN:
            spec = pl.sample(seed, smp)
            if spec.structure["conv"]:
                drawn.add(spec.slots["CONF"].value[1])
    assert len(drawn) > 30 and not drawn & P.QUARANTINED_FORMS          # ... and never drawn
    assert len(pl._form_ids(P.CONF_EXPLICIT)) == 44 - 3


# ------------------------------------------------------------------------------------------------ FIX-6: double negation

def test_the_double_negation_form_is_declared_consistently(plugin):
    q = plugin.QFORMS[P.DNEG_FORM]
    assert (q.qtype, q.predicate, q.polarity, q.complement_kind) == ("noul", "go_now", 1, None)
    assert P.YES_VERDICTS[P.DNEG_FORM] == P.YES_VERDICTS["yn_go"] == ("go",) and B.YES_SET[P.DNEG_FORM] == {"go"}
    assert P.COMPLEMENTS[P.DNEG_FORM] == ("yn_not_go",)                  # G-TW: an option-framing partner adds a cue
    assert KP.validate_plugin(plugin) == []


def test_double_negation_rows_pass_every_gate_and_keep_the_yn_go_gold(plugin, ctx):
    n_dneg = n_base = 0
    for seed in range(400):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            if spec.qform == "yn_go":
                n_base += 1
            if spec.qform != P.DNEG_FORM:
                continue
            n_dneg += 1
            res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
            assert res.ok, res.problems[:3]
            assert plugin.solve_a(spec) == plugin.solve_a(spec.replace(qform="yn_go"))
            for rr in res.rendered:
                if rr.row["meta"]["qform"] == P.DNEG_FORM:
                    c = negcount.count(rr.row["instructions"])
                    assert (c.k_syn, c.k_all) == (2, 2)
                else:
                    assert rr.row["meta"]["qform"] == "yn_not_go" and rr.row["role"] != "base"
    assert n_dneg >= 30 and 0.07 <= n_dneg / (n_dneg + n_base) <= 0.17


def test_double_negation_falls_back_to_yn_go_while_no_clean_wording_is_admitted(pool):
    pl = pool.plugin
    assert pl.dneg_ok == {False: False, True: False}
    forms = collections.Counter(pl.sample(seed, smp).qform for seed in range(500) for smp in TRAIN)
    assert forms[P.DNEG_FORM] == 0 and forms["yn_go"] > 100


# ------------------------------------------------------------------------------------------------ polarity rule

def test_the_wrong_gold_wording_class_is_refused(plugin):
    """T35 G5-H: "is it not the case that they do not bar ..." has two nots AND a blocking word: yes = may NOT."""
    bad = ["Is it not the case that the agent does not bar {ACTION} on {TARGET} right away?",
           "Isn't it the case that the agent may not run {ACTION} on {TARGET} right away?",
           "Is it not true that the call {ACTION} on {TARGET} is not blocked from running right away?"]
    good = ["Is it not the case that the agent may not run {ACTION} on {TARGET} straight away?",
            "Under this policy, is it not true that the agent is not cleared to run {ACTION} on {TARGET} right away?"]
    for t in bad:
        assert A.wording_problems(P.DNEG_FORM, t), t
    for t in good:
        assert A.wording_problems(P.DNEG_FORM, t) == [], t
    # one "not" under a "yes = may run" form reverses the meaning: refused; the same text under yn_not_go is right
    one_not = "Is it true that the agent may not run {ACTION} on {TARGET} straight away?"
    assert polarity.form_problems(P.T29Plugin, "yn_go", one_not)
    assert polarity.form_problems(P.T29Plugin, "yn_not_go", one_not) == []


def test_a_failing_wording_is_left_out_of_the_context_and_caught_in_a_row(plugin):
    """Inject an admitted double-negation wording that breaks the rule: ctx_for leaves it out, and a row rendered with it
    anyway fails G-LEX in check_rendered (the safety net)."""
    c = FX.ctx()
    text = "Is it not the case that the agent does not bar {ACTION} on {TARGET} right away?"
    sem = FX.question_sem(FX.F, P.DNEG_FORM)
    fid = c.lexicon.add(text, sem, slots=dict(FX.CALL), family=FX.F, held_out=False).form_id
    c.lexicon.unit_test_all()
    for e in range(c.lexicon.forms[fid].required):
        c.lexicon.record_extraction(fid, f"fixture:stand-in-{e + 1}", sem)
    c.skins["W-BAD-DNEG"] = FX.make_skin("W-BAD-DNEG", FX.F, text, dict(FX.CALL), kind="wording", register="question",
                                         qform=P.DNEG_FORM, lexicon_ids=(fid,))
    pl = P.T29Plugin(lexicon=c.lexicon, packs=P.PACKS)
    assert "W-BAD-DNEG" in pl.quarantined_wordings(c)
    assert "W-BAD-DNEG" not in pl.ctx_for(None, c).skins
    spec = next(s for s in (pl.sample(i, "S1") for i in range(400)) if s.qform == P.DNEG_FORM)
    rr = pl.render(spec, c, wording=c.skin("W-BAD-DNEG"))
    probs = pipeline.check_rendered(pl, spec, rr, c, run_g15=False)
    assert any(g == "G-LEX" and "polarity" in d for g, d in probs), probs


def test_the_frozen_wordings_all_pass_the_rule_so_none_is_quarantined(pool):
    pl, ctx = pool.plugin, pool.ctx
    assert pl.quarantined_wordings(ctx) == {}
    n = 0
    for sk in ctx.skins.values():
        if sk.kind == "wording" and polarity.checked_form(P.T29Plugin, sk.qform) is not None:
            assert polarity.form_problems(P.T29Plugin, sk.qform, sk.text) == [], sk.skin_id
            n += 1
    assert n >= 85                                    # yn_go 34 + yn_not_go 21 + yn_ask 30: the forms the rule applies to
    assert {"yn_refuse", "yn_permitted", "yn_not_forbidden"} == set(P.T29Plugin.POLARITY_SKIP)


# ------------------------------------------------------------------------------------------------ FIX-8: tags, depth

def test_twin_and_premise_rows_carry_their_own_tags_and_the_cards_depth(plugin):
    n_twin = n_prem = 0
    for seed in range(300):
        for smp in TRAIN:
            base = plugin.sample(seed, smp)
            for prop in plugin.relations(base):
                if prop.kind not in ("twin", "premise_removal"):
                    continue
                s2 = plugin.derive(prop.spec)
                tags, steps = plugin._tags(s2)
                assert tuple(s2.tags) == tuple(tags) and s2.depth == steps and s2.deep == (steps >= 3)
                assert s2.depth == base.depth                         # card depth: unchanged by a one-slot edit
                if prop.kind == "premise_removal":
                    n_prem += 1
                    assert "alarming_reversible_go" not in s2.tags and "harmless_irreversible" not in s2.tags
                    assert {"missing_decisive"} <= set(s2.tags)
                else:
                    n_twin += 1
    assert n_twin > 150 and n_prem > 30


def _requests_of_card(plugin, spec):
    """The Specs of the SAME card for every candidate request (v1.5 / 2c design: the card lists 3-5 candidate actions and
    the question names one, so the verdict is moved by the request while the card stays fixed)."""
    k, req = spec.structure["cands"], spec.structure["req"]
    cands, common = [], None
    for j in range(k):
        vs, _ = plugin._cand_view(spec.slots, {}, j, req)
        cands.append({n: s for n, s in vs.items() if n in P.CAND_NAMES})
        common = {n: s for n, s in vs.items() if n not in P.CAND_NAMES}
    cd = {"common": common, "structure": spec.structure,
          "meta": (spec.seed, spec.sampler, spec.qform, spec.card_id, spec.pack)}
    return [plugin._make_spec(cd, j, cands=cands) for j in range(k)]


def test_depth_is_the_same_for_every_verdict(sim_rows, plugin):
    """The old test compared the depth mix of the verdicts of single-call rows (spread <= 6 pp). With a candidate list the
    verdict is chosen by the REQUEST on a fixed card, so the equivalent invariant is exact: every request of one card has
    the same depth, whatever its verdict (spread 0, stricter than 6 pp), and the card's depth is its structural depth."""
    moved = cards = 0
    for seed in range(250):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            if spec.qform == "ch_rule":
                continue
            sibs = _requests_of_card(plugin, spec)
            assert len(sibs) == spec.structure["cands"] and 3 <= len(sibs) <= 5
            assert sibs[spec.structure["req"]].slots == spec.slots          # the rebuild reproduces the sampled request
            steps = {plugin._tags(s)[1] for s in sibs}                      # the depth every request of the card gets
            assert steps == {spec.depth} and spec.deep == (spec.depth >= 3), (seed, smp)
            assert spec.depth == P._card_depth(spec.structure["rules"])
            verdicts = {plugin._verdict_c(plugin._rule_truths(s), plugin._confirmed_c(s)) for s in sibs}
            cards += 1
            moved += len(verdicts) >= 2
    assert moved / cards >= 0.95, (moved, cards)       # the request really does move the verdict on (nearly) every card
    rows = [r for rs in sim_rows for r in rs]
    assert sum(r["deep"] for r in rows) / len(rows) <= 0.10


# ------------------------------------------------------------------------------------------------ FIX-3/4/5 + kit

def test_a_yes_no_unit_holds_a_twin_or_a_complement_never_both(plugin):
    n = 0
    for seed in range(500):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            if not spec.qform.startswith("yn_"):
                continue
            kinds = [p.kind for p in plugin.relations(spec)]
            assert (kinds.count("complement") + kinds.count("twin")) == 1, kinds
            n += 1
    assert n > 700


def test_pilot_size_balance(sim_rows, plugin):
    for rows in sim_rows:
        yn = [r for r in rows if r["qtype"] == "noul"]
        assert 0.45 <= len(yn) / len(rows) <= 0.55
        assert abs(sum(r["answer"] for r in yn) / len(yn) - 0.5) <= 0.02          # G10 yes rate (47.2% in the pilot)
        assert 0.10 <= sum(plugin.QFORMS[r["qform"]].complement_kind == "syntactic" for r in yn) / len(yn)
        comp = [r for r in yn if r["role"] == "complement"]
        assert sum(plugin.QFORMS[r["qform"]].complement_kind != "syntactic" for r in comp) / len(comp) >= 0.30
        assert 0.20 <= sum(r["role"] == "twin" for r in rows) / len(rows) <= 0.25
        assert 0.05 <= sum(r["role"] == "equiv" for r in rows) / len(rows) <= 0.10
        assert abs(sum(bool(plugin.QFORMS[r["qform"]].yes_is_bad) for r in yn) / len(yn) - 0.5) <= 0.05
        for q in ("yn_go", "yn_ask", "yn_refuse"):
            rs = [r for r in yn if r["qform"] == q]
            assert abs(sum(r["answer"] for r in rs) / len(rs) - 0.5) <= 0.10, q   # no question form predicts the gold


def test_cannot_decide_is_one_quarter_of_the_rows_that_show_it(plugin):
    """Kit choiceplan 1 / k: k = 4 where CANNOT DECIDE is shown (19.3% in the pilot, which made it predictive); every
    verdict is about 1 / 4 there and about 1 / 3 where it is hidden."""
    rows = BS.simulate(plugin, 6000, 31_000_000)
    cv = [r for r in rows if r["qform"] == "ch_verdict"]
    shown = collections.Counter(r["answer"] for r in cv if r["shown"])
    hidden = collections.Counter(r["answer"] for r in cv if not r["shown"])
    n_s, n_h = sum(shown.values()), sum(hidden.values())
    assert n_s > 1000 and n_h > 500 and "cannot" not in hidden
    for v in ("go", "ask", "refuse", "cannot"):
        assert abs(shown[v] / n_s - 0.25) <= 0.04, shown
    for v in ("go", "ask", "refuse"):
        assert abs(hidden[v] / n_h - 1 / 3) <= 0.05, hidden


# ------------------------------------------------------------------------------------------------ FIX-9

def test_registers_are_drawn_with_the_weights_and_none_passes_15_percent(plugin):
    share = collections.Counter()
    for smp in TRAIN:
        c = collections.Counter(plugin._register_for(plugin.sample(seed, smp), f"T29|{seed}|{smp}|x") for seed in range(2000))
        for reg, w in dict(P.REGISTER_W[smp]).items():
            assert abs(c[reg] / 2000 - w) <= 0.04, (smp, reg)
        for reg, k in c.items():
            share[reg] += k / (4 * 2000)
    assert set(share) == set(P.T29Plugin.REGISTERS) - set(P.T29Plugin.HELD_OUT_REGISTERS)
    assert max(share.values()) <= 0.145, share                       # 12.5% each (21.9% / 20.5% in the pilot)


def test_the_pack_pool_gives_one_pack_to_each_card(pool):
    pl = pool.plugin
    assert len(pl.packs) == 79 and len({p["org"] for p in pl.packs}) == 79
    used = {}
    for smp in pl.SAMPLERS:
        for idx in range(P.N_CARDS_S5 if smp == "S5" else P.N_CARDS):
            used[(smp, idx)] = pl.pack_for(smp, idx)["id"]
    assert len(used) == 74 and len(set(used.values())) == 74
    specs = [pl.sample(seed, smp) for seed in range(40) for smp in TRAIN]
    assert {s.pack for s in specs} <= set(used.values()) and len({s.pack for s in specs}) >= 40
    with pytest.raises(KP.ContractError):
        P.T29Plugin(lexicon=pool.ctx.lexicon, packs=[{**P.PACKS[0], "prefix": "x1"}])


def test_pool_pack_values_pass_gsl_when_rendered(pool):
    """Every pack of the pool serves a card end to end (G2, G3, G-SL, G-LEX, G-TW): one unit per pack."""
    pl, ctx = pool.plugin, pool.ctx
    seen, bad = set(), []
    for seed in range(1200):
        spec = pl.sample(seed, TRAIN[seed % 4])
        if spec.pack in seen:
            continue
        seen.add(spec.pack)
        res = pipeline.build_unit(pl, spec, ctx, run_g15=False)
        if not res.ok:
            bad.append((spec.pack, res.problems[:2]))
    assert len(seen) == 64 and bad == []                      # the 64 training cards (S5 is not drawn here)


# ------------------------------------------------------------------------------------------------ Haiku brief

def test_the_double_negation_round_is_gold_free_and_fixes_the_frame():
    tasks = A.build_dneg_tasks()
    assert A.check(tasks, A.ROOT_DNEG) == []
    assert [t.outputs for t in tasks] == [48, 6] and [t.held_out for t in tasks] == [False, True]
    text = "\n".join(t.text(A.ROOT_DNEG) for t in tasks).lower()
    assert "is it not the case that" in text and "never a contracted frame" in text
    for w in P.T29Plugin.LABEL_WORDS:
        assert f" {w} " not in f" {text} ".replace("\n", " "), w
    for t in list(P.VERDICT_TEXT.values()) + list(P.CODE_WORDS):
        assert t.lower() not in text
    assert all(str(t.answer_file(A.ROOT_DNEG)).startswith(str(A.HERE / "haiku" / "dneg")) for t in tasks)
    sem = A.question_sem(A.FAMILY, A.DNEG)
    assert sem == "q.t29.yn_go_dneg" and "two negations" in A.DNEG_SEM_MEANING
    assert dataclasses.is_dataclass(tasks[0])


def test_the_manifests_record_the_g0_they_were_authored_under():
    old, _ = A.files(A.build_tasks())
    assert '"g0_sha256": "' + P.G0_AUTHORED_SHA256 in old["TASKS.json"] and '"version": "v1"' in old["TASKS.json"]
    new, manifest = A.files(A.build_dneg_tasks(), A.ROOT_DNEG, version=A.VERSION_DNEG, g0_sha256=P.T29Plugin.G0_SHA256)
    assert manifest["version"] == "dneg1" and manifest["g0_sha256"] == P.T29Plugin.G0_SHA256 != P.G0_AUTHORED_SHA256
