"""c2_build/families/T07/test_i1_fixes.py: the T07 fix iteration 1 (C2_DATA_SPEC 6.4 step 6; G0_SPEC_v2.md section 8).

The first T07 pilot (families/T07/pilot/, 1,001 rows) passed every program gate except G6 and G10:
  F1  the ch_failing "None" option was gold on a flat 25% of its rows (21% of the k = 2 rows, 0% of nothing else moved):
      G6 choice +4 to +6 pp on every view, G10 gold-is-longest -5.1 pp. Now: None is gold on exactly 1/k of the rows of a
      k-cell (strata of k rows per window of 4,096 seeds), its display slot is exactly uniform per k, the ch_offers
      outcome is stratified, and the ch_failing twin keep rate is 1/(k-1)^2.
  F2  polarity (kit c2_kit.polarity, the T35 G5-H lesson): 6 contracted yn_dneg_gets wordings ("Isn't it the case that ...
      doesn't get ...?") of the frozen pool read either way; they are quarantined at generation (ctx_for), the G-LEX safety
      net refuses one that reaches a row, and lint_wording_v2 refuses a re-authored one.
Nothing here writes a file; the real frozen pools are loaded read-only (load_v2).

Run (from lean/c2_build):  ../../.venv/bin/python -B -m pytest -q families/T07/test_i1_fixes.py
"""
from __future__ import annotations

import collections
import hashlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import pipeline  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit.choiceplan import plan_report  # noqa: E402
from families.T07 import authoring as A  # noqa: E402
from families.T07 import fixtures as FX  # noqa: E402
from families.T07 import load_v2 as LV  # noqa: E402
from families.T07 import plugin as P  # noqa: E402

TRAIN = ("S1", "S2", "S3", "S4")


@pytest.fixture(scope="module")
def real_ctx():
    return LV.make_ctx(LV.load_pools())


@pytest.fixture(scope="module")
def real_plugin(real_ctx):
    return P.T07Plugin(lexicon=real_ctx.lexicon)


@pytest.fixture(scope="module")
def fx_ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def fx_plugin(fx_ctx):
    return P.T07Plugin(lexicon=fx_ctx.lexicon)


# ------------------------------------------------------------------------------------------------ F2: polarity

def test_the_six_contracted_dneg_wordings_are_quarantined_and_nothing_else(real_plugin, real_ctx):
    bad = real_plugin.quarantined_wordings(real_ctx)
    assert len(bad) == 6
    held = collections.Counter(real_ctx.skin(sid).held_out for sid in bad)
    assert held == {False: 3, True: 3}
    for sid, probs in bad.items():
        sk = real_ctx.skin(sid)
        assert sk.qform == "yn_dneg_gets"
        assert any(p.startswith("P3") for p in probs), probs
        assert "n't" in sk.text.lower() or "isn't" in sk.text.lower() or "doesn't" in sk.text.lower()
    screened = real_plugin.ctx_for(None, real_ctx)
    left = collections.Counter((s.qform, s.held_out) for s in screened.skins.values() if s.kind == "wording")
    assert left[("yn_dneg_gets", False)] == 9 and left[("yn_dneg_gets", True)] == 9      # 12 / 6 authored (+6 held-out wordings of the A54 layer)
    assert left[("yn_misses", False)] == 22 and left[("yn_misses", True)] == 7            # no over-rejection
    for qf in ("yn_gets", "yn_not_gets", "yn_fails_to", "ch_failing", "ch_offers"):
        assert sum(1 for s in real_ctx.skins.values() if s.kind == "wording" and s.qform == qf) == \
            sum(v for (q, _h), v in left.items() if q == qf), qf
    assert all(sid in real_ctx.skins for sid in bad)                       # the raw pool is untouched (never edited)


def test_render_never_picks_a_quarantined_wording(real_plugin, real_ctx):
    bad = set(real_plugin.quarantined_wordings(real_ctx))
    n = 0
    for smp in TRAIN + ("S5",):
        for seed in range(600):
            spec = real_plugin.sample(seed, smp)
            if spec.qform != "yn_dneg_gets":
                continue
            rr = real_plugin.render(spec, real_ctx)
            assert rr.wording_id not in bad
            n += 1
    assert n >= 60


def test_glex_safety_net_flags_a_wording_that_reaches_a_row(real_plugin, real_ctx):
    sid = sorted(real_plugin.quarantined_wordings(real_ctx))[0]
    wording = real_ctx.skin(sid)
    spec = next(s for s in (real_plugin.sample(i, "S1") for i in range(400)) if s.qform == "yn_dneg_gets")
    rr = real_plugin.render(spec, real_ctx, wording=wording)
    probs = pipeline.check_rendered(real_plugin, spec, rr, real_ctx, run_g15=False)
    assert any(g == "G-LEX" and "polarity" in d for g, d in probs), probs


@pytest.mark.parametrize("qform,text,codes", [
    ("yn_dneg_gets", "Isn't it the case that {CUSTOMER} doesn't get {ASKED} on order {ORDER_ID}?", ["P3"]),
    ("yn_dneg_gets", "Is it not the case that {CUSTOMER} does not get {ASKED} on order {ORDER_ID}?", []),
    ("yn_dneg_gets", "Is it not the case that {CUSTOMER} does not lose out on {ASKED} on order {ORDER_ID}?", ["P1"]),
    ("yn_misses", "Does order {ORDER_ID} from {CUSTOMER} lose out on {ASKED}?", []),
    ("yn_misses", "Does order {ORDER_ID} from {CUSTOMER} forfeit {ASKED}?", []),
    ("yn_misses", "Does order {ORDER_ID} from {CUSTOMER} get {ASKED}?", ["P2"]),
    ("yn_not_gets", "Is it true that {CUSTOMER} does not get {ASKED} on order {ORDER_ID}?", []),
    ("yn_not_gets", "Is it true that {CUSTOMER} does not lose out on {ASKED} on order {ORDER_ID}?", ["P1"]),
    ("yn_fails_to", "Does order {ORDER_ID} from {CUSTOMER} fail to get {ASKED}?", []),
    ("yn_gets", "Does order {ORDER_ID} from {CUSTOMER} get {ASKED}?", []),
    ("yn_gets", "Does order {ORDER_ID} from {CUSTOMER} forfeit {ASKED}?", ["P2"]),
    ("yn_not_gets", "Is order {ORDER_ID} from {CUSTOMER} not given {ASKED}?", ["P4"]),       # strict frames
])
def test_polarity_rules_on_t07_wordings(qform, text, codes):
    got = [p.split()[0] for p in POL.form_problems(P.T07Plugin, qform, text)]
    assert got == codes, (text, got)


def test_lint_wording_v2_refuses_the_six_and_v1_lint_is_unchanged(real_plugin, real_ctx):
    for sid in real_plugin.quarantined_wordings(real_ctx):
        sk = real_ctx.skin(sid)
        assert A.lint_wording(sk.qform, sk.text) == [] or all("polarity" not in x for x in A.lint_wording(
            sk.qform, sk.text))
        v2 = A.lint_wording_v2(sk.qform, sk.text)
        assert any(x.startswith("polarity: P3") for x in v2), (sk.text, v2)
    ok = "Is it not the case that {CUSTOMER} does not get {ASKED} on order {ORDER_ID} under the advertised terms?"
    assert A.lint_wording_v2("yn_dneg_gets", ok) == []
    assert "explicit outer frame" in A.REAUTHOR_BRIEF_DNEG or "explicit outer frame" in " ".join(
        A.REAUTHOR_BRIEF_DNEG.split())


def test_fixture_wordings_screened_by_strict_frames_leave_every_form_a_wording(fx_plugin, fx_ctx):
    screened = fx_plugin.ctx_for(None, fx_ctx)
    for qf in P.T07Plugin.QFORMS:
        for held in (False, True):
            assert any(s.kind == "wording" and s.qform == qf and s.held_out == held for s in screened.skins.values())


# ------------------------------------------------------------------------------------------------ F1: the plan

def _base_specs(plugin, n=1000):
    return [plugin.sample(seed, smp) for smp in TRAIN for seed in range(n)]


def test_none_is_gold_on_one_in_k_in_every_k_cell(fx_plugin):
    specs = _base_specs(fx_plugin)
    cells = collections.defaultdict(lambda: [0, 0])
    for s in specs:
        if s.qform == "ch_failing":
            k = len(P.failing_dims(s.structure)) + 1
            cells[k][0] += 1
            cells[k][1] += fx_plugin.solve_a(s) == "none"
            assert (fx_plugin.solve_a(s) == "none") == fx_plugin.row_plan(s.sampler, s.seed, "ch_failing").gold_abstain
    assert set(cells) >= {2, 3, 4, 5}
    for k, (n, a) in cells.items():
        assert abs(a - n / k) <= 4, (k, n, a)                     # one partial block per sampler and cell, at most
    assert abs(cells[2][1] / cells[2][0] - 0.5) <= 0.02          # the k = 2 cell the first pilot had at 21%


def test_none_display_slot_is_uniform_per_k_and_the_gold_position_is_too(fx_plugin, fx_ctx):
    slots = collections.defaultdict(collections.Counter)
    gold_pos = collections.defaultdict(collections.Counter)
    for smp in TRAIN:
        for seed in range(500):
            s = fx_plugin.sample(seed, smp)
            if s.qform != "ch_failing":
                continue
            rr = fx_plugin.render(s, fx_ctx)
            k = len(rr.row["options"])
            none_at = rr.row["options"].index(P.NONE_TEXT)
            slots[k][none_at] += 1
            gold_pos[k][rr.option_set.gold_index] += 1
            assert none_at == fx_plugin.row_plan(smp, seed, "ch_failing").abstain_slot
    for k, c in slots.items():
        if sum(c.values()) >= 5 * k:
            assert max(c.values()) - min(c.values()) <= 4, (k, c)
            assert set(c) == set(range(k))
    from c2_kit.choiceplan import chi2_uniform_p
    for k, c in gold_pos.items():
        if sum(c.values()) >= 5 * k:
            assert chi2_uniform_p([c[i] for i in range(k)]) > 0.01, (k, c)


def test_a_wrong_none_option_is_named_by_error_models_and_a_gold_none_is_not_wrong(fx_plugin, fx_ctx):
    named = wrong = 0
    for smp in TRAIN:
        for seed in range(300):
            s = fx_plugin.sample(seed, smp)
            if s.qform != "ch_failing":
                continue
            rr = fx_plugin.render(s, fx_ctx)
            ab = [o for o in rr.option_set.options if o.key == "none"]
            assert len(ab) == 1
            if ab[0].role == "abstain":                      # a wrong None: one named error model at least
                wrong += 1
                named += bool(ab[0].err)
                assert set(rr.row["meta"]["opt_err"]) == set(rr.row["options"]) - {rr.row["gold"]}
            else:
                assert ab[0].role == "gold" and rr.row["gold"] == P.NONE_TEXT
    assert wrong >= 100 and named == wrong, (named, wrong)


def test_the_plan_check_reads_the_construction_not_solver_a(fx_plugin, monkeypatch):
    """A solver-A bug must reach G2, not stop the sampler: sample() checks the plan against the construction's gold."""
    monkeypatch.setattr(fx_plugin, "solve_a", lambda spec: "date")
    assert fx_plugin.sample(24, "S1") is not None


def test_ch_offers_outcome_is_stratified_and_the_gold_is_the_longest_option_one_in_four(fx_plugin, fx_ctx):
    out, longest, n = collections.Counter(), 0.0, 0
    for smp in TRAIN:
        for seed in range(600):
            s = fx_plugin.sample(seed, smp)
            if s.qform != "ch_offers":
                continue
            out[fx_plugin.row_plan(smp, seed, "ch_offers").outcome] += 1
            rr = fx_plugin.render(s, fx_ctx)
            lens = [len(o) for o in rr.row["options"]]
            top = [i for i, x in enumerate(lens) if x == max(lens)]
            longest += (1 / len(top)) if rr.option_set.gold_index in top else 0.0
            n += 1
    assert set(out) == {0, 1, 2, 3} and max(out.values()) - min(out.values()) <= 4, out
    assert abs(longest / n - 0.25) <= 0.02, (longest / n, n)


def test_a_twin_prints_the_same_closed_option_list_and_every_unit_passes(fx_plugin, fx_ctx):
    n_twin = 0
    for smp in TRAIN:
        for seed in range(250):
            s = fx_plugin.sample(seed, smp)
            if s.qform not in ("ch_failing", "ch_offers"):
                continue
            res = pipeline.build_unit(fx_plugin, s, fx_ctx, run_g15=False)
            assert res.ok, res.problems
            base = res.rows[0]
            for r in res.rows[1:]:
                if r["role"] in ("twin", "equiv", "attack"):
                    assert r["options"] == base["options"]
                    n_twin += r["role"] == "twin"
    assert n_twin >= 60


def test_plan_report_passes_on_every_emitted_choice_row(fx_plugin, fx_ctx):
    sets = []
    for smp in TRAIN:
        for seed in range(400):
            s = fx_plugin.sample(seed, smp)
            if s.qform in ("ch_failing", "ch_offers"):
                res = pipeline.build_unit(fx_plugin, s, fx_ctx, run_g15=False)
                assert res.ok
                sets += [rr.option_set for rr in res.rendered if rr.option_set is not None]
    rep = plan_report(sets)
    # the kit's length-rank check is for open sets whose options are built to a planned LENGTH rank; a closed label set has
    # fixed texts, so only the abstain cells, the positions and gold-is-longest apply (the pilot's G10 reads the same)
    failing = [f for f in rep["failing"] if not f.startswith("length rank")]
    assert failing == [], rep
    assert abs(rep["longest_gold_pp"]) <= 2.0
    assert rep["rows"] >= 1000
    for key, c in rep["abstain_cells"].items():
        assert c["p_binom"] > 0.01, (key, c)


def test_twin_keep_rate_is_one_over_dimension_labels_squared():
    assert [P.twin_none_keep(c) for c in (1, 2, 3, 4, 5)] == [1.0, 0.25, 1 / 9, 1 / 16, 1 / 25]
    for k in (2, 3, 4, 5, 6):                         # twins' None share = (1-a) kappa / ((1-a) kappa + a) = a
        a, kappa = 1 / k, P.twin_none_keep(k - 1)
        assert abs((1 - a) * kappa / ((1 - a) * kappa + a) - a) < 1e-12


def test_streams_cross_a_window_boundary_and_are_replayable(fx_ctx):
    a, b = P.T07Plugin(lexicon=fx_ctx.lexicon), P.T07Plugin(lexicon=fx_ctx.lexicon)
    w = 2 * P.WINDOW_PAIRS
    seeds = list(range(w - 40, w + 40))
    for smp in ("S1", "S4"):
        for sd in seeds:
            sa, sb = a.sample(sd, smp), b.sample(w - 40 + (sd - (w - 40)), smp)
            assert sa.structure == sb.structure and a.solve_a(sa) == b.solve_a(sb)
            if sa.qform in ("ch_failing", "ch_offers"):
                assert a.row_plan(smp, sd, sa.qform) == b.row_plan(smp, sd, sa.qform)
    # an instance asked for a late seed first gives the same plan as one that walked up to it
    late = P.T07Plugin(lexicon=fx_ctx.lexicon)
    s = next(late.sample(sd, "S2") for sd in range(900000, 900200) if late.sample(sd, "S2").qform == "ch_failing")
    walked = P.T07Plugin(lexicon=fx_ctx.lexicon)
    assert walked.row_plan("S2", s.seed, "ch_failing") == late.row_plan("S2", s.seed, "ch_failing")


# ------------------------------------------------------------------------------------------------ the G0 v2 pin

def test_g0_v2_is_pinned_and_keeps_the_authored_spec():
    v2 = P.T07Plugin.G0_LITE
    assert v2.name == "G0_SPEC_v2.md"
    text = v2.read_text(encoding="utf-8")
    assert hashlib.sha256(text.encode()).hexdigest() == P.T07Plugin.G0_SHA256
    assert len(text.splitlines()) <= 200 and "FROZEN v2" in text and "## 8. v2" in text
    v1 = P.HERE.joinpath("G0_SPEC.md").read_text(encoding="utf-8")
    assert hashlib.sha256(v1.encode()).hexdigest() == P.T07Plugin.G0_SHA256_AUTHORED != P.T07Plugin.G0_SHA256
    assert "FROZEN v1" in v1
    flat = " ".join(text.split())
    for needle in ("exactly 1/k", "1/(k-1)^2", "polarity", "quarantined"):
        assert needle in flat, needle


# ------------------------------------------------------------------------------------------------ determinism

_DET = r"""
import hashlib, json, sys
sys.path.insert(0, {root!r})
from c2_kit import pipeline
from families.T07 import fixtures as FX, plugin as P
ctx = FX.ctx(); pl = P.T07Plugin(lexicon=ctx.lexicon)
h = hashlib.sha256()
for smp in ("S1", "S2", "S3", "S4", "S5"):
    for seed in range(80):
        r = pipeline.build_unit(pl, pl.sample(seed, smp), ctx, run_g15=False)
        for row in r.rows:
            h.update(json.dumps(row, sort_keys=True, ensure_ascii=False).encode())
print(h.hexdigest())
"""


def test_rows_do_not_depend_on_the_hash_seed():
    out = []
    for hs in ("1", "4242"):
        env = dict(os.environ, PYTHONHASHSEED=hs)
        r = subprocess.run([sys.executable, "-B", "-c", _DET.format(root=str(C2_BUILD))], capture_output=True,
                           text=True, env=env, check=True)
        out.append(r.stdout.strip())
    assert out[0] == out[1] and len(out[0]) == 64
