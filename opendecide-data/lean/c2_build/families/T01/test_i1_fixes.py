"""families/T01/test_i1_fixes.py: regression for the T01 pilot fix iteration 1 (G0_SPEC_v4.md section 12; C2_DATA_SPEC 6.4
step 6). Written from the as-is pilot (14 Oct 2026): G10 double negation 0% (spec 3.0 asks >= 2% of yes/no rows) and G6 /
G7 option cues that show at the full-generation sample size (5,000 rows: choice accuracy +4.5 pp over chance, 14 G7 choice
features, among them opt:000 = the printed threshold, meta:qform=ch_due&kind:verbatim_in_text, ch_total gold longest 64 of
73 against 39 expected). In memory only (A37 f): nothing is written, no model runs.

Run (from lean/c2_build):  ../../.venv/bin/python -m pytest -q families/T01/test_i1_fixes.py
"""
from __future__ import annotations

import collections
import hashlib
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot_loaders as PL  # noqa: E402
from c2_kit import pipeline, polarity  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from families.T01 import fixtures as FX  # noqa: E402
from families.T01 import haiku_dneg as D  # noqa: E402
from families.T01 import plugin as P  # noqa: E402
import negcount  # noqa: E402  (c_src/common, put on sys.path by c2_kit)

TRAIN = ("S1", "S2", "S3", "S4", "S6")
DROP_MSGS = ("the error models leave a side of the gold empty", "an option copies a printed date")


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T01(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def ctx_dneg():
    return FX.ctx(dneg=True)


@pytest.fixture(scope="module")
def plugin_dneg(ctx_dneg):
    return P.T01(lexicon=ctx_dneg.lexicon)


@pytest.fixture(scope="module")
def frozen():
    with PL.open_family("T01") as kit:
        yield kit


def _render(plugin, ctx, spec):
    try:
        return plugin.render(spec, ctx)
    except K.RenderError as e:
        assert any(m in str(e) for m in DROP_MSGS), e
        return None


def _rows(plugin, ctx, qforms, n_seeds=260, samplers=TRAIN):
    out = []
    for smp in samplers:
        for seed in range(n_seeds):
            spec = plugin.sample(seed, smp)
            if spec.qform in qforms:
                rr = _render(plugin, ctx, spec)
                if rr is not None:
                    out.append((spec, rr))
    return out


def _vis(rr):
    return (rr.row["state"] + "\n" + rr.row["instructions"]).lower()


# ------------------------------------------------------------------------------------------------ F2: option cues

def test_every_option_shares_the_golds_visible_cues(plugin, ctx):
    """G0 v4 12.2: printed or not, equal digit count (a count, an amount): no content-free rule finds the gold."""
    seen = collections.Counter()
    for spec, rr in _rows(plugin, ctx, set(P.CUE_MATCH_FORMS)):
        os_ = rr.option_set
        vis = _vis(rr)
        printed = plugin._printed_values(spec)
        rk = plugin._option_renderer(spec, rr.forms)
        sigs = {plugin._cue_sig(spec.qform, o.key, rk, vis, printed) for o in os_.options}
        assert len(sigs) == 1, (spec.qform, spec.seed, [o.text for o in os_.options], sigs)
        if spec.qform == "ch_days":
            assert all(o.key >= 1 for o in os_.options)          # an impossible count (0 days) is never an option
        seen[spec.qform] += 1
    assert set(seen) == set(P.CUE_MATCH_FORMS) and min(seen.values()) >= 30, seen


def test_the_cue_rule_removes_what_the_g7_probe_found(plugin, ctx):
    """On 5,000 iteration-0 rows ch_due showed a verbatim option in the gold 23% of rows and in a wrong option 16%; ch_total
    gold was the longest of 3 on 88% of the sets whose lengths differ. Now no option is verbatim in a set where the gold is
    not, and an amount set has one length."""
    due = _rows(plugin, ctx, {"ch_due"}, n_seeds=400, samplers=("S6",))
    tot = _rows(plugin, ctx, {"ch_total"}, n_seeds=400, samplers=("S4",))
    assert len(due) > 40 and len(tot) > 40
    for spec, rr in due + tot:
        vis = _vis(rr)
        flags = {len(o) > 3 and o.lower() in vis for o in rr.row["options"]}
        assert len(flags) == 1
    for spec, rr in tot:
        assert len({len(o) for o in rr.row["options"]}) == 1


def test_receipt_day_options_are_never_copies_of_the_record(plugin, ctx):
    """ch_receipt_day cannot share value cues (the record prints every nearby date, 1.6% of sets would remain); its
    options are shown in a date form the record never prints, so none is a verbatim copy of anything printed."""
    rows = _rows(plugin, ctx, {"ch_receipt_day"}, n_seeds=500, samplers=("S6",))
    assert len(rows) > 40
    for spec, rr in rows:
        vis = _vis(rr)
        assert not any(len(o) > 3 and o.lower() in vis for o in rr.row["options"])
        assert rr.row["qtype"] == "choice" and len(rr.row["options"]) == 2


def test_choice_answers_have_no_gap_at_the_limit(plugin):
    """A count or an amount drawn around the limit in one contiguous range (G7 opt:61 days; opt:000 = the threshold)."""
    at_limit = band = n_days = n_tot = 0
    for seed in range(4000):
        spec = plugin.sample(seed, "S1")
        if spec.qform == "ch_days":
            v = spec.env()
            n_days += 1
            at_limit += plugin.solve_a(spec) in (v["N_MAX"], v["N_MAX"] + 1)
            assert "boundary" not in spec.tags or plugin.solve_a(spec) in (v["N_MAX"], v["N_MAX"] + 1)
    for seed in range(4000):
        spec = plugin.sample(seed, "S4")
        if spec.qform == "ch_total":
            v = spec.env()
            n_tot += 1
            total = plugin.solve_a(spec)
            band += abs(total - v["THRESHOLD"]) <= 0.05 * v["THRESHOLD"]
            assert 0.6 * v["THRESHOLD"] - 100 <= total <= 1.4 * v["THRESHOLD"]
    assert n_days > 150 and 0.03 <= at_limit / n_days <= 0.10, (at_limit, n_days)    # was 0 outside a boundary row
    assert n_tot > 100 and 0.08 <= band / n_tot <= 0.17, (band, n_tot)                # uniform: 12.5%


def test_closed_cash_labels_are_uniform(plugin, ctx):
    labels, texts = collections.Counter(), collections.Counter()
    n = 0
    for seed in range(900000, 906000):                              # the pilot's seed range (v3 was 30 / 30 / 15 / 25)
        spec = plugin.sample(seed, "S4")
        if spec.qform == "ch_cash_which":
            labels[plugin.solve_a(spec)] += 1
            n += 1
    assert n > 1500
    for lab in P.CASH_LABELS:
        assert abs(labels[lab] / n - 0.25) <= 0.035, labels
    lens = {lab: len(P.CASH_TEXT[lab]) for lab in P.CASH_LABELS}      # every row shows the same four texts, so the
    assert [lab for lab, x in lens.items() if x == max(lens.values())] == ["out"]    # gold is the longest exactly when
    assert [lab for lab, x in lens.items() if x == min(lens.values())] == ["both"]    # its label is "out" (25%), the
    rows = _rows(plugin, ctx, {"ch_cash_which"}, n_seeds=150, samplers=("S4",))      # shortest when it is "both" (25%)
    assert rows and all(sorted(r.row["options"]) == sorted(P.CASH_TEXT.values()) for _, r in rows)


# ------------------------------------------------------------------------------------------------ F1: double negation

def test_without_an_admitted_double_negation_wording_the_form_is_never_drawn(plugin, frozen):
    assert plugin.dneg_ok == {q: False for q in P.DNEG_FORMS.values()}
    for p in (plugin, frozen.plugin):
        assert not any(p.sample(seed, smp).qform in P.DNEG_FORMS.values() for seed in range(300) for smp in TRAIN)
    assert frozen.plugin.dneg_ok == {q: False for q in P.DNEG_FORMS.values()}   # the frozen pool: none of the 6 forms


def test_double_negation_forms_pass_every_program_gate(plugin_dneg, ctx_dneg):
    assert all(plugin_dneg.dneg_ok.values())
    rows, n_dneg, n_units, drops = [], 0, 0, 0
    qforms = collections.Counter()
    for smp in TRAIN:
        for seed in range(500):
            spec = plugin_dneg.sample(seed, smp)
            if spec.qform not in P.DNEG_FORMS.values():
                continue
            n_dneg += 1
            res = pipeline.build_unit(plugin_dneg, spec, ctx_dneg, run_g15=False)
            assert res.ok, (spec.qform, seed, res.problems)         # G2, G3, G4, G-SL, G-LEX, G-TW: all in one unit
            n_units += 1
            qforms[spec.qform] += 1
            base = next(b for b, d in P.DNEG_FORMS.items() if d == spec.qform)
            assert plugin_dneg.solve_a(spec) == plugin_dneg.solve_a(spec.replace(qform=base))   # not not P = P
            for r in res.rows:
                q = r["instructions"].rsplit("\n\n", 1)[1]
                c = negcount.count(q)
                if r["meta"]["qform"] == spec.qform:
                    assert (c.k_all, c.k_syn) == (2, 2), q
                    assert r["meta"]["qform"] == spec.qform
                rows.append(r)
            comps = [rr for rr in res.rendered if rr.row["role"] == "complement"]
            for rr in comps:                                        # the only partner: the single-negation form
                assert plugin_dneg.QFORMS[rr.row["meta"]["qform"]].complement_kind == "syntactic"
    assert set(qforms) == set(P.DNEG_FORMS.values()) and min(qforms.values()) >= 8, qforms
    yn = [r for r in rows if r["qtype"] == "noul"]
    assert sum(negcount.count(r["instructions"].rsplit("\n\n", 1)[1]).k_syn >= 2 for r in yn) / len(yn) >= 0.5


def test_double_negation_share_of_yes_no_bases(plugin_dneg):
    n_yn = n_dn = 0
    for smp in TRAIN:
        for seed in range(2000):
            spec = plugin_dneg.sample(seed, smp)
            if plugin_dneg.QFORMS[spec.qform].qtype == "noul":
                n_yn += 1
                n_dn += spec.qform in P.DNEG_FORMS.values()
    assert abs(n_dn / n_yn - P.P_DNEG) <= 0.03, (n_dn, n_yn)       # >= 2% of yes/no rows even after drops (spec 3.0)


def test_frozen_scripts_keep_their_26_question_forms():
    assert len(P.T01.FROZEN_QFORMS) == 26 and len(P.T01.QFORMS) == 32
    assert not set(P.DNEG_FORMS.values()) & set(P.T01.FROZEN_QFORMS)
    for dq in P.DNEG_FORMS.values():
        q = P.T01.QFORMS[dq]
        assert q.polarity == 1 and q.qtype == "noul" and q.complement_kind is None
        assert P.KIND_OF[dq] == P.KIND_OF[next(b for b, d in P.DNEG_FORMS.items() if d == dq)]


# ------------------------------------------------------------------------------------------------ F3: polarity and rulings

def test_polarity_screen_on_the_frozen_pool(frozen):
    """The frozen pool is clean under P1-P3 (checked on all 177 yes/no wordings with the family's antonym phrases); the
    strict frame rule P4 flags two, and the three wordings of G0 v4 12.4 are quarantined: 5 of 271, nothing else."""
    bad = frozen.plugin.quarantined_wordings(frozen.ctx)
    texts = {frozen.ctx.skin(sid).text for sid in bad}
    assert len(bad) == 5 and set(P.WORDING_QUARANTINE) <= texts and len(P.WORDING_QUARANTINE) == 3
    assert "Does the request from {PERSON} not need written quotes?" in texts
    assert "Does the {ACTION} for case {REF} count as not filed in time under the filing rule?" in texts
    assert sum(1 for s in frozen.ctx.skins.values() if s.kind == "wording") == 271
    for sid, probs in bad.items():
        assert probs and all(isinstance(p, str) for p in probs)
    for s in frozen.ctx.skins.values():                           # no P1 / P2 / P3 anywhere (no over-rejection either)
        if s.kind == "wording" and s.skin_id not in bad:
            assert polarity.form_problems(frozen.plugin, s.qform, s.text) == [], s.skin_id


def test_units_on_the_frozen_pool_never_use_a_quarantined_wording(frozen):
    plugin, ctx = frozen.plugin, frozen.ctx
    bad = plugin.quarantined_wordings(ctx)
    n_ok = 0
    for smp in TRAIN:
        for seed in range(80):
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            assert not [d for g, d in res.problems if g == "G-LEX"], res.problems
            for rr in res.rendered:
                assert rr.wording_id not in bad
            n_ok += res.ok
    assert n_ok > 250


def test_a_p4_wording_that_reaches_a_row_fails_glex(frozen):
    plugin, ctx = frozen.plugin, frozen.ctx
    bad = plugin.quarantined_wordings(ctx)
    sid = next(s for s, p in bad.items() if p[0].startswith("P4") and ctx.skin(s).qform == "yn_no_quotes")
    spec = next(sp for sp in (plugin.sample(seed, "S4") for seed in range(400)) if sp.qform == "yn_quotes")
    spec = spec.replace(qform="yn_no_quotes")
    rr = plugin.render(spec, ctx, wording=ctx.skin(sid))
    probs = pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False)
    assert any(g == "G-LEX" and sid in d and "polarity" in d for g, d in probs), probs


# ------------------------------------------------------------------------------------------------ the double-negation brief

def test_the_double_negation_authoring_round():
    b, plan = D.build_batch()
    assert len(plan) == 72 and sum(len(c["items"]) for c in b.chunks) == 72 and max(len(c["items"]) for c in b.chunks) <= 48
    assert {m["qform"] for m in plan.values()} == set(P.DNEG_FORMS.values())
    for _iid, m in plan.items():
        assert set(m["slots"]) <= {"PERSON", "REF", "REF_DATE", "ACTION", "PERIL", "DAY"}
    brief = D.DNEG_BRIEF["yn_dneg_on_time"][1][1]
    assert "never say the response was 'sent' or 'arrived'" in brief
    assert "is it not the case that" in D.SHAPE and "contracted" in D.SHAPE and "blocking" in D.SHAPE


GOOD = [("yn_dneg_over", "Under the card's rule, is it not the case that {PERSON} is not over the stay limit?", ["PERSON"]),
        ("yn_dneg_timely", "Is it not true that the {ACTION} in case {REF} was not filed in time?", ["ACTION", "REF"]),
        ("yn_dneg_covered", "According to the rule card, is it not the case that the {PERIL} loss is not covered?",
         ["PERIL"]),
        ("yn_dneg_quotes", "Going by the record, is it not true that request {REF} does not call for written quotes?",
         ["REF"]),
        ("yn_dneg_cash_report", "Is it not true that no cash report is needed for {DAY} in ledger {REF}?",
         ["DAY", "REF"]),
        ("yn_dneg_on_time", "Is it not the case that the response to notice {REF} was not on time under the receipt rule?",
         ["REF"])]
BAD = {"contracted frame": ("yn_dneg_over", "Isn't it true that {PERSON} is not over the stay limit?", ["PERSON"]),
       "negation over a negative predicate": ("yn_dneg_timely", "Is it not the case that the {ACTION} was not filed late?",
                                              ["ACTION"]),
       "one negation": ("yn_dneg_covered", "Is it true that the {PERIL} loss is not covered?", ["PERIL"]),
       "subject-not frame": ("yn_dneg_covered", "Is the {PERIL} loss not not covered?", ["PERIL"]),
       "three negations": ("yn_dneg_over", "Is it not the case that {PERSON} is not never over the stay limit?",
                           ["PERSON"]),
       "sent, not received": ("yn_dneg_on_time", "Is it not true that the response to notice {REF} was not sent on time?",
                              ["REF"]),
       "fixture copy": ("yn_dneg_quotes", "Is it not the case that request {REF} does not need written quotes?", ["REF"])}


@pytest.mark.parametrize("q,text,slots", GOOD)
def test_the_checker_admits_the_safe_shape(q, text, slots):
    got, probs = D.check_wording("x", text, {"qform": q, "slots": slots, "kind": P.KIND_OF[q]}, seen=set())
    assert probs == [] and got[0] == q


@pytest.mark.parametrize("why", sorted(BAD))
def test_the_checker_refuses_every_failure_mode(why):
    q, text, slots = BAD[why]
    got, probs = D.check_wording("x", text, {"qform": q, "slots": slots, "kind": P.KIND_OF[q]}, seen=set())
    assert probs, why


# ------------------------------------------------------------------------------------------------ G0 v4

def test_g0_versions_and_the_pool_era_sha():
    here = Path(P.__file__).resolve().parent
    assert hashlib.sha256((here / "G0_SPEC.md").read_bytes()).hexdigest() == P.T01.G0_SHA256_AUTHORED
    assert hashlib.sha256((here / "G0_SPEC_v4.md").read_bytes()).hexdigest() == P.T01.G0_SHA256
    assert P.T01.G0_SHA256 != P.T01.G0_SHA256_AUTHORED and Path(P.T01.G0_LITE).name == "G0_SPEC_v4.md"
    v4 = (here / "G0_SPEC_v4.md").read_text(encoding="utf-8")
    for token in ("## 12.", "12.1", "12.2", "12.3", "12.4", "12.5", "12.6", "12.7"):
        assert token in v4


def test_cash_which_label_is_dealt_in_seed_blocks():
    """G0 v4 12.7: stateless, seed-deterministic, 25% each to within one row per block of seed pairs."""
    from collections import Counter
    for sampler, base in (("S4", 0), ("S4", 900000)):
        blk = P.CASH_BLOCK_PAIRS
        seeds = [s for p in range(base // 2, base // 2 + 4 * blk) if P._cash_which_pair(sampler, p) for s in (2 * p, 2 * p + 1)]
        assert seeds
        first = {s: P._cash_which_label(sampler, s) for s in seeds}
        P._CASH_DEAL.clear()
        assert first == {s: P._cash_which_label(sampler, s) for s in reversed(seeds)}
        by_block = {}
        for s in seeds:
            by_block.setdefault(s // 2 // blk, []).append(first[s])
        for labels in by_block.values():
            cnt = Counter(labels)
            assert set(cnt) <= {"in", "out", "both", "neither"}
            assert max(cnt.values()) - min(cnt.get(k, 0) for k in ("in", "out", "both", "neither")) <= 1
