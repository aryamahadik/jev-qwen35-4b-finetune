"""transfer/T36/test_pilot_i1.py: tests of the Stage B pilot fix iteration 1 (PILOT_VERDICT F1-F7, G0 v2.2). In memory only
(A37 f: no file is written; no Haiku, no network).

  F1  the ch_pick plan: stratified slots, the None gold = 1/k in every block, k, position and gold rank from the plan,
      structures redrawn (never relabelled) until solver A agrees; twins of one-inside bases land on None
  F2  the rank among the version options is the planned one (version order); the eight new error models by hand; every
      model is independent of the listing order
  F3  a wrong option has the gold's kind, length and zero-final status; the version under review's kind does not tell
      the answer
  F4  the shares: yes/no cells, ch_pick share
  F5  yn_double: drawn only while a clean admitted wording exists; the polarity rule screens every wording; the
      complement partner is yn_not_meets
  F7  the card: row-specific items, row.card on yes/no rows, the head of the instructions on choice rows, one card for a
      row and its partners, the mean length by the real tokenizer
  F8  the same rows under every PYTHONHASHSEED
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/transfer/T36/test_pilot_i1.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import cards as CARDS  # noqa: E402
from c2_kit import choiceplan, pipeline  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit.skin import make_skin  # noqa: E402
from transfer.T36 import double_neg as DN  # noqa: E402
from transfer.T36 import fixtures as FX  # noqa: E402
from transfer.T36 import plugin as P  # noqa: E402
from transfer.T36.test_plugin import _spec  # noqa: E402

TRAIN = ("S1", "S2", "S3", "S4")


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T36Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def choice_specs(plugin):
    out = []
    for smp in TRAIN:
        for seed in range(0, 480):
            if P.slot_of(smp, seed)[0] == "choice":
                out.append(plugin.sample(seed, smp))
    return out


@pytest.fixture(scope="module")
def units(plugin, ctx):
    out = []
    for seed in range(0, 240):
        for smp in TRAIN:
            out.append(pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False))
    return out


def _chi2_p(counts):
    return choiceplan.chi2_uniform_p(list(counts))


# ------------------------------------------------------------------------------------------------ F1: the plan

def test_slots_are_stratified():
    for smp in P.T36Plugin.SAMPLERS:
        for blk in range(60):
            kinds = [P.slot_of(smp, blk * P.W_SLOTS + i)[0] for i in range(P.W_SLOTS)]
            assert kinds.count("choice") == P.N_CHOICE_SLOTS
        idx = [P.slot_of(smp, s) for s in range(P.W_SLOTS * 5)]
        for kind in ("choice", "yesno"):
            seq = [i for k, i in idx if k == kind]
            assert seq == list(range(len(seq)))                 # the index among its kind counts 0, 1, 2 ... in seed order


def test_choice_plan_cells_are_exact():
    plans = {3: [], 4: []}
    for smp in TRAIN:
        for seed in range(P.W_SLOTS * 120):
            if P.slot_of(smp, seed)[0] == "choice":
                plan, out = P.choice_plan(smp, seed)
                plans[plan.k].append((plan, out))
    for k, rows in plans.items():
        assert len(rows) > 1000
        outs = collections.Counter(o for _p, o in rows)
        assert abs(outs["A"] / len(rows) - 1 / k) < 0.02, (k, outs)
        assert abs(outs["N1"] / len(rows) - 1 / k) < 0.02, (k, outs)
        assert all(p.gold_abstain == (o == "A") for p, o in rows)
        pos = collections.Counter(p.pos for p, _ in rows)
        assert _chi2_p([pos[i] for i in range(k)]) > 0.05
        ranks = collections.Counter(p.rank for p, o in rows if o != "A")
        assert set(ranks) == set(range(k - 1))
        assert _chi2_p([ranks[i] for i in range(k - 1)]) > 0.05
        assert all(p.rank is None for p, o in rows if o == "A")
        assert all(abs(p.abstain_share - 1 / k) < 1e-12 for p, _ in rows)


def test_specs_reach_their_plan_and_the_options_follow_it(plugin, choice_specs):
    assert len(choice_specs) > 800
    for spec in choice_specs:
        plan, outcome = P.choice_plan(spec.sampler, spec.seed)
        gold = plugin.solve_a(spec)
        assert (gold == P.NONE_KEY) == plan.gold_abstain
        env = spec.env()
        n_in = sum(P.meets(spec, env[n]) for n in spec.structure["published"])
        assert n_in == {"A": 0, "N1": 1}.get(outcome, n_in) and (outcome != "N2" or n_in >= 2)
        os_ = plugin._options(spec, strict=True)
        assert os_ is not None and len(os_.options) == plan.k == P.option_count(plugin.row_key(spec))
        assert os_.gold_index == plan.pos and os_.options[plan.pos].role == "gold"
        assert any(o.text == P.NONE_TEXT for o in os_.options)
        assert os_.meta["gold_is_abstain"] == plan.gold_abstain
        if not plan.gold_abstain:
            key = P._k if spec.structure["eco"] == "npm" else P._pk
            below = sum(1 for o in os_.options if o.role == "error" and key(o.key) < key(gold))
            assert below == plan.rank == os_.meta["gold_rank"]          # F2: the rank in version order is the planned one
            assert len([o for o in os_.options if o.role != "abstain"]) == plan.k - 1


def test_none_share_and_balance_over_all_rows(units, plugin):
    """plan_report over every option set of the passing units (bases, twins, equiv, attack): the None gold is 1/k in every
    (k, shown) cell, the position and the rank are uniform, gold-is-longest is 1/k within the +/- 2 pp bar."""
    sets = [rr.option_set for u in units if u.ok for rr in u.rendered if rr.option_set is not None]
    assert len(sets) > 600
    rep = choiceplan.plan_report(sets, longest_pp=2.5)
    assert not [f for f in rep["failing"] if f.startswith("k")], rep
    for key, c in rep["abstain_cells"].items():
        k = int(key[1])
        assert abs(c["share"] - 1 / k) < 0.04, (key, c)
    assert rep["positions_chi2_p"] and all(p > 0.01 for p in rep["positions_chi2_p"].values())
    assert abs(rep["longest_gold_pp"]) <= 2.5


def test_twins_of_one_inside_bases_land_on_none(plugin, choice_specs):
    """F1: the twins' None share is 1/k too (an N1 base's minimal-edit twin overwrites its only inside version)."""
    n = lands = 0
    by_outcome = collections.Counter()
    for spec in choice_specs[:900]:
        outcome = P.choice_plan(spec.sampler, spec.seed)[1]
        for prop in plugin.relations(spec):
            if prop.kind == "twin":
                n += 1
                if prop.expect == P.NONE_KEY:
                    lands += 1
                    by_outcome[outcome] += 1
    assert n > 150
    assert set(by_outcome) == {"N1"}                       # only a one-inside base can land on none
    assert 0.15 < lands / n < 0.45, (lands, n)


def test_reached_plans_are_never_dropped(plugin):
    """No seed of the training or held-out samplers fails to reach its plan (a dropped seed would be selection on the
    plan's cell): 0 of 1,500 draws here."""
    for smp in P.T36Plugin.SAMPLERS:
        for seed in range(300):
            plugin.sample(seed, smp)


# ------------------------------------------------------------------------------------------------ F2: error models

def _models(spec):
    return {n: m.fn(spec) for n, m in P.T36Plugin().error_models().items()}


def test_new_error_models_by_hand():
    vs = ["1.2.9", "1.9.0", "2.0.0", "3.1.0"]
    s = _spec("npm", [["^1.2.3"]], vs, qform="ch_pick")
    m = _models(s)
    assert P.pick(s) == "1.9.0"
    assert m["t36_upper_ignored"] == "3.1.0"                      # only the lower bound counts: the highest from 1.2.3 up
    assert m["t36_lowest_listed"] == "1.2.9" and m["t36_second_listed"] == "2.0.0"
    assert m["t36_second_meeting"] == "1.2.9"                     # meeting: 1.2.9, 1.9.0 -> the second highest
    assert m["t36_below_range"] is None and m["t36_above_range"] == "3.1.0"   # lowest above the bound 2.0.0 (not 2.0.0 itself)
    assert m["t36_major_only"] == "1.2.9"                         # MAJOR only: 1.2.9 and 1.9.0 tie, the lowest wins
    assert m["t36_minor_only"] == "1.9.0"
    s2 = _spec("pep", [["~=1.4.2"]], ["1.3", "1.4.2", "1.4.7", "1.5", "2.0"], qform="ch_pick")
    m2 = _models(s2)
    assert P.pick(s2) == "1.4.7"
    assert m2["t36_upper_ignored"] == "2.0" and m2["t36_below_range"] == "1.3" and m2["t36_above_range"] is None
    assert m2["t36_lowest_listed"] == "1.3" and m2["t36_second_listed"] == "1.5"
    s3 = _spec("npm", [[">=1.2.0", "<1.5.0"]], ["1.0.0", "1.2.3", "1.4.0", "1.9.9"], qform="ch_pick")
    m3 = _models(s3)
    assert P.pick(s3) == "1.4.0" and m3["t36_below_range"] == "1.0.0" and m3["t36_above_range"] == "1.9.9"
    assert m3["t36_second_meeting"] == "1.2.3"


def test_every_error_model_ignores_the_listing_order(plugin, choice_specs):
    """The reversed listing (G4) must not move any model's pick: the tie rules use version order, never list order."""
    n = 0
    for spec in choice_specs[:400]:
        rev = spec.replace(structure={**spec.structure, "published": list(reversed(spec.structure["published"]))})
        assert _models(spec) == _models(rev), (spec.sampler, spec.seed)
        n += 1
    assert n == 400


def test_the_models_fill_every_cell_without_relabelling(plugin, choice_specs):
    names = collections.Counter()
    for spec in choice_specs:
        os_ = plugin._options(spec, strict=True)
        for o in os_.options:
            for e in o.err:
                names[e] += 1
    assert len(names) >= 14, names                      # most of the 19 models appear as options
    assert {"t36_major_only", "t36_lowest_listed", "t36_second_meeting", "t36_below_range"} <= set(names), names


# ------------------------------------------------------------------------------------------------ F3: shape

def test_a_wrong_option_has_the_golds_kind_length_and_last_number_bucket(plugin, choice_specs):
    n = 0
    for spec in choice_specs:
        eco = spec.structure["eco"]
        os_ = plugin._options(spec, strict=True)
        vs = [o.text for o in os_.options if o.text != P.NONE_TEXT]
        sig = {(P.kind_of(eco, v), len(v), P.final_bucket(eco, v)) for v in vs}
        assert len(sig) == 1, (spec.sampler, spec.seed, vs)
        if os_.gold.text != P.NONE_TEXT:
            assert sig == {(P.kind_of(eco, os_.gold.text), len(os_.gold.text), P.final_bucket(eco, os_.gold.text))}
        else:
            assert next(iter(sig))[0] == "plain"
        n += 1
    assert n > 800


def test_the_version_under_review_does_not_tell_the_answer(plugin):
    """F3: a post-release was under review on 27 pilot rows and the answer was yes on 26. Now the kind (plain, pre-release,
    post-release) is drawn from the seed and the side from the plan: each kind is about half yes."""
    by = collections.defaultdict(lambda: [0, 0])
    for smp in TRAIN:
        for seed in range(0, 1100):
            if P.slot_of(smp, seed)[0] != "yesno":
                continue
            spec = plugin.sample(seed, smp)
            cand = spec.env()["CAND"]
            k = P.kind_of(spec.structure["eco"], cand)
            by[k][0] += 1
            by[k][1] += P.meets(spec, cand)
    assert by["plain"][0] > 1000 and by["pre"][0] > 100 and by["post"][0] > 50
    for k, (n, y) in by.items():
        assert abs(y / n - 0.5) < 0.12, (k, n, y)


def test_the_version_under_review_ends_in_zero_on_either_side(plugin):
    """F3: a narrow range such as ~1.4.2 has no zero-final version inside, so zero-final candidates were outside. Now
    whether the version under review is zero-final is drawn from the seed: the same share on both sides of the range."""
    side = {True: [0, 0], False: [0, 0]}
    for smp in TRAIN:
        for seed in range(0, 1100):
            if P.slot_of(smp, seed)[0] != "yesno":
                continue
            spec = plugin.sample(seed, smp)
            cand = spec.env()["CAND"]
            meets = P.meets(spec, cand)
            side[meets][0] += 1
            side[meets][1] += P.zero_final(spec.structure["eco"], cand)
    for meets, (n, z) in side.items():
        assert n > 800 and abs(z / n - P.Q_ZERO) < 0.04, (meets, n, z)


# ------------------------------------------------------------------------------------------------ F4: shares

def test_yes_no_cells_and_overlay_shares(units, plugin):
    rows = [r for u in units if u.ok for r in u.rows]
    yn = [r for r in rows if r["qtype"] == "noul"]
    assert 0.45 <= len(yn) / len(rows) <= 0.55
    assert abs(sum(r["gold"] for r in yn) / len(yn) - 0.5) <= 0.025
    bad = [r for r in yn if plugin.QFORMS[r["meta"]["qform"]].yes_is_bad]
    assert abs(len(bad) / len(yn) - 0.5) <= 0.05
    rep = pipeline.overlay_report(units, plugin)
    assert 0.19 <= rep["twin_share"] <= 0.26 and 0.05 <= rep["equiv_share"] <= 0.10
    assert rep["complement_share_of_yes_no"] >= 0.2


# ------------------------------------------------------------------------------------------------ F5: yn_double

def test_yn_double_is_drawn_only_while_a_clean_wording_is_admitted(plugin):
    assert plugin.double_ok == {False: False, True: False}           # the frozen pools have none
    forms = collections.Counter(plugin.sample(s, "S1").qform for s in range(480))
    assert forms["yn_double"] == 0 and forms["yn_meets"] > 0


@pytest.fixture(scope="module")
def dctx():
    return FX.ctx(double=True)


@pytest.fixture(scope="module")
def dplugin(dctx):
    return P.T36Plugin(lexicon=dctx.lexicon)


def test_polarity_screen_keeps_the_clean_wordings_and_quarantines_the_rest(dctx, dplugin):
    assert dplugin.double_ok == {False: True, True: True} and dplugin.quarantined_wordings(dctx) == {}
    reg = dctx.lexicon
    skins = dict(dctx.skins)
    for wid, qf, text, rule in FX.BAD_DOUBLE_WORDINGS:
        f = reg.add(text, P.question_sem(P.FAMILY, qf), slots={"CAND": "id", "PKG": "id"}, family=P.FAMILY)
        skins[wid] = make_skin(wid, P.FAMILY, text, {"CAND": "id", "PKG": "id"}, kind="wording", register="question",
                               qform=qf, lexicon_ids=(f.form_id,))
    bad = P.T36Plugin(lexicon=reg)
    ctx2 = type(dctx)(skins=skins, lexicon=reg)
    q = bad.quarantined_wordings(ctx2)
    assert set(q) == {w for w, _f, _t, _r in FX.BAD_DOUBLE_WORDINGS}
    for wid, _qf, _t, rule in FX.BAD_DOUBLE_WORDINGS:
        assert any(p.startswith(rule) for p in q[wid]), (wid, q[wid])
    screened = bad.ctx_for(None, ctx2)
    assert not set(q) & set(screened.skins) and "W-DBL-1" in screened.skins
    for wid, qf, text, _s in FX.DOUBLE_WORDINGS:                       # the authoring check of double_neg.py agrees
        assert DN.wording_problems(bad, text) == [], wid


def test_yn_double_rows_pass_every_program_gate(dctx, dplugin):
    n = 0
    seen = collections.Counter()
    for smp in TRAIN:
        for seed in range(0, 480):
            spec = dplugin.sample(seed, smp)
            if spec.qform != "yn_double":
                continue
            n += 1
            u = pipeline.build_unit(dplugin, spec, dctx, run_g15=(n % 15 == 0))
            assert u.ok, u.problems[:2]
            meets = P.meets(spec, spec.env()["CAND"])
            assert u.rows[0]["gold"] == int(meets) and u.rows[0]["meta"]["qform"] == "yn_double"
            for r in u.rows[1:]:
                seen[r["meta"]["qform"]] += (r["role"] == "complement")
    assert n > 40
    assert set(k for k, v in seen.items() if v) <= {"yn_not_meets"}     # the exact syntactic complement
    assert seen["yn_not_meets"] > 5


def test_yn_double_share_follows_the_blocks(dplugin):
    pos = dbl = 0
    for smp in TRAIN:
        for seed in range(0, 1200):
            if P.slot_of(smp, seed)[0] != "yesno":
                continue
            q = dplugin.sample(seed, smp).qform
            pos += q in ("yn_meets", "yn_double")
            dbl += q == "yn_double"
    assert abs(dbl / pos - P.P_DOUBLE) < 0.04, (dbl, pos)


def test_polarity_screen_passes_the_frozen_wordings(plugin, ctx):
    assert plugin.quarantined_wordings(ctx) == {}
    for wid, qf, text, _s in FX.WORDINGS:
        assert POL.form_problems(plugin, qf, text) == [], wid


# ------------------------------------------------------------------------------------------------ F7: the card

def test_the_card_has_the_rules_the_range_needs():
    def ids(spec):
        card = P.card_text(spec)
        by = {i.full: i.item_id for i in P.CARD_ITEMS[spec.structure["eco"]]}
        return [by["".join(line[2:])] for line in card.split("\n")[1:-1]]
    assert P.card_text(_spec("npm", [["^1.4.2"]], ["1.5.0"], "1.5.0")).split("\n")[0] == P.HEADING["npm"]
    assert P.card_text(_spec("npm", [["^1.4.2"]], ["1.5.0"], "1.5.0")).endswith(P.CLOSED_WORLD)
    assert ids(_spec("npm", [["^1.4.2"]], ["1.5.0"], "1.5.0")) == ["ver", "caret", "gate", "inout"]
    assert ids(_spec("npm", [["~1.4.2"]], ["1.5.0"], qform="ch_pick")) == ["ver", "tilde", "gate", "pick"]
    assert ids(_spec("npm", [["^1.4.2-beta.2"], [">=3.0.0", "<3.1.0"]], ["1.5.0"], "1.5.0")) == [
        "ver", "tags", "cmp", "caret", "parts", "alts", "gate", "inout"]
    assert ids(_spec("npm", [["1.2.3", "2.3.4"]], ["1.5.0"], "1.5.0", hyphen=[True])) == ["ver", "hyphen", "gate", "inout"]
    assert ids(_spec("npm", [["1.x"]], ["1.5.0"], "1.5.0")) == ["ver", "xr", "gate", "inout"]
    assert ids(_spec("npm", [["=1.2.3"]], ["1.2.3"], "1.2.3")) == ["ver", "cmp", "gate", "inout"]
    assert ids(_spec("pep", [["~=1.4.2"]], ["1.5"], "1.5")) == ["ver", "wild", "compat", "gate", "inout"]
    assert ids(_spec("pep", [["==1.4.*"]], ["1.5"], qform="ch_pick")) == ["ver", "wild", "gate", "pick"]
    assert ids(_spec("pep", [[">=1.4", "!=1.5", "<2.0"]], ["1.5"], "1.5")) == ["ver", "cmp", "comma", "gate", "inout"]
    assert ids(_spec("pep", [["<=2.0"]], ["1.5"], "1.5")) == ["ver", "cmp", "gate", "inout"]


def test_the_card_goes_where_the_served_prompt_prints_it_once(units, plugin):
    n_yn = n_ch = 0
    for u in units[:300]:
        for rr in u.rendered:
            row = rr.row
            wording = rr.wording_id
            if row["qtype"] == "noul":
                assert row["card"] and row["card"].endswith(P.CLOSED_WORLD) and "\n\n" not in row["card"]
                assert "\n" not in row["instructions"] and row["meta"]["defs_style"] == "rules_in_card_full"
                n_yn += 1
            else:
                assert not row["card"] and row["instructions"].count("\n\n") == 1
                assert row["meta"]["defs_style"] == "rules_in_instructions_full"
                n_ch += 1
            rules, question = CARDS.split_rules(row)
            assert rules.startswith("How to read ") and rules.endswith(P.CLOSED_WORLD) and "\n" not in question
            assert wording and rr.regions[wording][0] == "instructions"
    assert n_yn > 150 and n_ch > 150


def test_a_row_and_its_partners_print_one_card(units):
    n = 0
    for u in units:
        if not u.ok:
            continue
        cards = {CARDS.split_rules(r)[0] for r in u.rows}
        assert len(cards) == 1, [r["role"] for r in u.rows]
        n += 1
    assert n > 700


def test_mean_length_is_under_the_bar_by_the_real_tokenizer(units):
    rows = [r for u in units if u.ok for r in u.rows]
    rep = CARDS.token_report(rows)
    assert rep["max"] <= 2000
    if "pinned" in rep["counted_by"]:                          # the pinned Qwen3.5-4B tokenizer is present
        assert rep["mean"] <= 780, rep                         # spec 3.0 bar 800 (target 780); the v2.1 mean was 1,206.9
    else:
        assert rep["mean"] <= 800 * 1.3


# ------------------------------------------------------------------------------------------------ F8: determinism

_CODE = """
import hashlib, json, sys
sys.path.insert(0, %(c2)r)
from c2_kit import pipeline
from transfer.T36 import fixtures as FX, plugin as P
ctx = FX.ctx()
pl = P.T36Plugin(lexicon=ctx.lexicon)
h = hashlib.sha256()
for seed in range(0, 48):
    for smp in ("S1", "S2", "S3", "S4"):
        u = pipeline.build_unit(pl, pl.sample(seed, smp), ctx, run_g15=False)
        h.update(json.dumps(u.rows, sort_keys=True).encode())
        h.update(json.dumps([[a, b] for a, b in u.problems]).encode())
print(h.hexdigest())
"""


def test_generation_is_the_same_under_every_hash_seed():
    """The pilot found twin rows that changed with PYTHONHASHSEED (_pool_guess sorted a set by a key that ties for 3.6 and
    3.6.0). Two interpreters with different seeds write the same rows."""
    out = []
    for hs in ("1", "424242"):
        env = {**os.environ, "PYTHONHASHSEED": hs}
        r = subprocess.run([sys.executable, "-B", "-c", _CODE % {"c2": str(C2_BUILD)}], capture_output=True, text=True,
                           env=env, timeout=600, cwd=str(C2_BUILD))
        assert r.returncode == 0, r.stderr[-800:]
        out.append(r.stdout.strip())
    assert len(out[0]) == 64 and out[0] == out[1]


def test_pool_writers_use_the_pool_sha_not_the_plugins():
    for name in ("freeze.py", "freeze_v2.py", "redo2.py", "authoring.py"):
        text = (P.HERE / name).read_text()
        assert "P.POOL_G0_SHA256" in text and "P.T36Plugin.G0_SHA256" not in text, name
    assert hashlib.sha256((P.HERE / "G0_SPEC_v2.1.md").read_bytes()).hexdigest() == P.POOL_G0_SHA256
    man = json.loads((P.HERE / "pools_v2" / "MANIFEST.json").read_text()) if (P.HERE / "pools_v2" / "MANIFEST.json").is_file() \
        else None
    if man:
        assert man["g0_sha256"] == P.POOL_G0_SHA256


def test_double_neg_brief_builds_and_is_gold_free():
    b = DN.build()
    assert len(b.key) == DN.WORDING_COUNT and b.kind == "author_wording"
    blob = json.dumps(b.chunks)
    assert '"gold"' not in blob and "yn_double" not in blob.replace("t36|wording|yn_double", "")
    assert all(c["answer_file"].endswith(".json") for c in b.chunks)
    assert "EXACTLY TWO negation words" in b.prompt
