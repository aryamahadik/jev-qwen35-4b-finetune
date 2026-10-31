"""families/T24/test_plugin.py: in-memory tests for the T24 plugin (A37 f: no test writes a file; rows live in memory).

Covers the task's bars: solver A == solver B (and the G3 parse, G-SL, G-LEX, schema, options) on >= 5,000 sampled
specs; relation units through every program gate (G2, G3, G4, G-SL, G-LEX, G-TW, schema, and G15 on a few);
minimal-edit twins differ in one slot and flip exactly as constructed; complements are opposite; cosmetic edits keep
the rule AST; gold balance and trap shares on 2,000 specs; edit length does not predict the label; G-SL on the
built-in placeholder skins (no gold-label word or literal value outside slots); determinism by seed (also across hash
seeds); error-model distractors; and injected bugs that the gates must catch.

Run (from lean/):  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T24
"""
from __future__ import annotations

import collections
import dataclasses
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import gsl, pipeline  # noqa: E402
from c2_kit import plugin as P  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit import rules as RL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.cards import split_rules  # noqa: E402
from c2_kit.distractors import CATALOG, check_named, position_counts  # noqa: E402
from c2_kit.paths import COMMON  # noqa: E402  (puts c_src/common on sys.path)
from c2_kit.relations import slot_diff  # noqa: E402
from families.T24 import fixtures as FX  # noqa: E402
from families.T24 import plugin as T  # noqa: E402
from families.T24 import solver_b as B  # noqa: E402

CLOSED_WORLD = T.CLOSED_WORLD

import negcount  # noqa: E402  (c_src/common, read-only)

assert COMMON.is_dir()

TRAIN = ("S1", "S2", "S3", "S4")
YN = tuple(q for q, f in T.T24Plugin.QFORMS.items() if f.qtype == "noul")
HERE_FILES = {"__init__.py", "G0_SPEC.md", "plugin.py", "solver_b.py", "fixtures.py", "test_plugin.py", "authoring.py",
              "test_authoring.py", "haiku", "pools", "pilot", "pilot_i1", "pool_freeze.py", "extract_stage.py", "redo2.py",
              "test_redo2.py", "balance_check.py", "run_pilot_i1.py", "test_balance.py", "run_pilot_i2.py",
              "pilot_i2", "_backup_i2"}


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return T.T24Plugin(lexicon=ctx.lexicon, packs=T.STANDIN_PACKS)           # the 10 + 2 stand-ins: tests only


@pytest.fixture(scope="module")
def specs2000(plugin):
    return [plugin.sample(seed, smp) for seed in range(500) for smp in TRAIN]


def _material(spec) -> int:
    return int(T.outcome_a(spec, 1) != T.outcome_a(spec, 2))


# ------------------------------------------------------------------------------------------------ contract

def test_plugin_meets_the_strict_contract(plugin):
    assert P.validate_plugin(plugin, strict=True) == []
    assert P.check_independence(plugin) == []
    assert plugin.PARADIGM_A != plugin.PARADIGM_B
    assert len(T.HERE.joinpath("G0_SPEC.md").read_text(encoding="utf-8").splitlines()) <= 200
    src = Path(B.__file__).read_text(encoding="utf-8")
    assert "families.T24.plugin" not in src and "from . import plugin" not in src and "c2_kit.rules" not in src


def test_domains_and_pools_are_clean():
    for key, dom in T.DOMAINS.items():                     # the 12 stand-ins and the 79 frozen pool packs
        assert T.check_domain(dom) == [], key
    assert len(T.STANDIN_TRAIN) == 10 and len(T.STANDIN_HELD) == 2 and T.TRAIN_DOMAINS == T.STANDIN_TRAIN
    sp = T.STANDIN_PACKS
    train_cards = {T.domain_for(s, c, sp).key for s in TRAIN for c in range(T.N_CARDS)}
    assert train_cards == set(T.STANDIN_TRAIN)
    assert {T.domain_for("S5", c, sp).key for c in range(T.N_CARDS_HELD)} == set(T.STANDIN_HELD)
    for n in T.CUSTOMERS:
        S.name_slot(n)
    labels = {w for w in T.T24Plugin.LABEL_WORDS if " " not in w}
    for dom in T.DOMAINS.values():                # label words never collide with a fact surface
        for s in dom.cats + dom.conds + dom.dates + (dom.amount,):
            assert not set(s.split()) & labels, s
    phrases = [w for w in T.T24Plugin.LABEL_WORDS if " " in w]
    for dom in T.DOMAINS.values():                # ... nor does a pack's fact hold another pack's outcome name
        for s in dom.cats + dom.conds + dom.dates + (dom.amount,):
            assert not [w for w in phrases if re.search(rf"(?<![a-z]){re.escape(w)}(?![a-z])", s)], s
    for d in T.DOMAINS.values():                  # LABEL_WORDS see the outcome names of every pack (F1)
        assert set(d.outcomes) <= set(T.T24Plugin.LABEL_WORDS) | {w for w in d.outcomes if w in labels}


def test_the_frozen_pack_pool_is_wired_in_one_pack_per_card():
    """F1: T24Plugin() deals the 75 + 4 frozen pool packs; the 32 training cards use 32 different packs, S5 the 4
    held-out ones; the pool is sha-checked against its MANIFEST."""
    assert T.POOL_ERROR is None and T.POOL_PACKS is not None
    assert len(T.POOL_PACKS.train) == 75 and len(T.POOL_PACKS.held) == 4
    assert all(not T.DOMAINS[k].held_out for k in T.POOL_PACKS.train)
    assert all(T.DOMAINS[k].held_out for k in T.POOL_PACKS.held)
    assert T.check_domain(T.DOMAINS[T.POOL_PACKS.train[0]]) == []
    cards = {(s, c): T.domain_for(s, c, T.POOL_PACKS).key for s in TRAIN for c in range(T.N_CARDS)}
    assert len(set(cards.values())) == 32 >= 25                                    # one pack per card (spec 3.0)
    assert set(cards.values()) <= set(T.POOL_PACKS.train)
    assert {T.domain_for("S5", c, T.POOL_PACKS).key for c in range(T.N_CARDS_HELD)} == set(T.POOL_PACKS.held)
    assert not set(cards.values()) & set(T.STANDIN_DOMAINS)                        # no stand-in on a real card
    with pytest.raises(T.ContractError):                                           # a changed pool file is refused
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copy(T.POOL_DIR / "MANIFEST.json", tmp)
            Path(tmp, "packs.json").write_bytes(T.POOL_DIR.joinpath("packs.json").read_bytes() + b" ")
            T.load_pool_packs(Path(tmp))


def test_lexicon_forms_pass_unit_tests_and_wordings_keep_their_negation_counts(ctx):
    reg = ctx.lexicon
    assert all(f.unit_ok for f in reg.forms.values()), [f.text for f in reg.forms.values() if not f.unit_ok]
    assert reg.gate()["pass"]
    for sem, kind, _ in FX.SEMS:
        n = sum(1 for f in reg.forms.values() if f.sem_id == sem)
        assert n >= 3, sem
        assert all(reg.forms[f].required == (3 if kind == "window" else 2) for f in reg.forms if f.startswith(sem))
    want = {"yn_changes": (0, 0), "yn_same": (0, 0), "ch_v2": (0, 0), "yn_not_change": (1, 1),
            "yn_fail_change": (1, 0), "yn_dneg": (2, 2)}
    for _wid, qf, text in FX.WORDINGS + FX.HELD_WORDINGS:
        c = negcount.count(text)
        assert (c.k_all, c.k_syn) == want[qf], (text, c)


# ------------------------------------------------------------------------------------------------ A == B

def test_solver_a_equals_solver_b_on_5000_specs(plugin, ctx):
    """G2 (and G3, G-SL, G-LEX, schema, options) on 1,000 seeds x 5 samplers: every row passes check_rendered."""
    seen = collections.Counter()
    fails = []
    for seed in range(1000):
        for smp in plugin.SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            probs = pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False)
            if probs:
                fails.append((seed, smp, probs[:2]))
                continue
            view = plugin.parse(rr.row, ctx)
            assert plugin.solve_b(view) == plugin.solve_a(spec) == rr.answer
            seen[("qform", spec.qform)] += 1
            seen[("edit", spec.structure["edit"]["kind"], spec.structure["edit"]["variant"])] += 1
            seen[("container", spec.structure["container"])] += 1
            seen[("domain", spec.pack)] += 1
            seen[("mode", next(t for t in spec.tags if t.startswith("mode_")))] += 1
            seen[("register", rr.register)] += 1
    assert not fails, fails[:5]
    assert sum(v for k, v in seen.items() if k[0] == "qform") == 5000
    assert {k[1] for k in seen if k[0] == "qform"} == set(plugin.QFORMS)
    assert {k[1] for k in seen if k[0] == "container"} == {"lines", "table", "update", "diff"}
    assert {k[1] for k in seen if k[0] == "domain"} == set(T.STANDIN_DOMAINS)
    assert {k[1] for k in seen if k[0] == "mode"} == {"mode_flip", "mode_same", "mode_masked", "mode_untouched",
                                                      "mode_cosmetic"}
    edits = {(k[1], k[2]) for k in seen if k[0] == "edit"}
    assert edits == {("anchor", "anchor"), ("limit", "value"), ("cosmetic", "none")} | {
        (k, v) for k, vs in T.VARIANTS.items() for v, _ in vs}
    assert {k[1] for k in seen if k[0] == "register"} == set(plugin.REGISTERS)


# ------------------------------------------------------------------------------------------------ relations

def test_relation_units_pass_every_gate(plugin, ctx):
    units, kinds = [], collections.Counter()
    for seed in range(300):
        for smp in plugin.SAMPLERS:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=(seed < 3))
            assert res.ok, (seed, smp, res.problems[:3])
            units.append(res)
            for r in res.rows:
                kinds[r["role"]] += 1
                assert R.validate_row(r) == []
                assert R.approx_tokens(r) <= R.MAX_TOKENS
                assert r["meta"]["dev_only"] == (smp == "S5" or r["meta"]["c2"]["register"] in
                                                 plugin.HELD_OUT_REGISTERS)
    rep = pipeline.overlay_report(units, plugin)
    rows = rep["rows"]
    assert rep["complement_share_of_yes_no"] >= 0.20 and rep["non_syntactic_share_of_pairs"] >= 0.30
    assert 0.20 <= rep["twin_share"] <= 0.25, rep["twin_share"]
    assert 0.05 <= rep["equiv_share"] <= 0.10 and rep["attack_share"] == 0
    assert 0.45 <= rep["yes_no"] / rows <= 0.55
    assert 0.47 <= rep["yes_rate"] <= 0.53
    assert set(kinds) == {"base", "complement", "twin", "equiv"}
    questions = [split_rules(r)[1] for u in units for r in u.rows if r["qtype"] == "noul"]
    k_syn = [negcount.count(q).k_syn for q in questions]
    assert sum(k >= 1 for k in k_syn) / len(k_syn) >= 0.10                           # spec 3.0 syntactic negation
    assert sum(k >= 2 for k in k_syn) / len(k_syn) >= 0.02                           # spec 3.0 double negation
    lengths = [R.approx_tokens(r) for u in units for r in u.rows]
    assert max(lengths) <= R.MAX_TOKENS and sum(lengths) / len(lengths) <= 1100      # approximate (3 chars / token)
    s5 = [r for u in units for r in u.rows if r["meta"]["sampler"] == "S5"]
    assert s5 and all(r["meta"]["wording_id"].startswith("WH-") for r in s5)        # held-out wordings on S5 only
    assert not any(r["meta"]["wording_id"].startswith("WH-") for u in units for r in u.rows
                   if r["meta"]["sampler"] != "S5")


def test_twins_differ_in_one_slot_and_flip_exactly_as_constructed(plugin, ctx, specs2000):
    kinds = collections.Counter()
    for spec in specs2000:
        t = plugin.twin(spec)
        if t is None:
            continue
        twin = plugin.derive(t.spec)
        assert slot_diff(spec, twin) == {t.changed_slot}
        assert plugin.solve_a(twin) == t.expect != plugin.solve_a(spec)
        rr = plugin.render(twin, ctx)
        assert plugin.solve_b(plugin.parse(rr.row, ctx)) == t.expect
        kinds[t.note] += 1
    assert set(kinds) == {f"twin {k}" for k in ("request", "amount", "category", "condition", "revised")}, kinds
    # every changed outcome can be undone by one slot; a cosmetic edit can never be made to change the outcome, and an
    # untouched / masked case often needs two slots, so those rows simply carry no twin (overlay share: 20-25%)
    assert sum(kinds.values()) >= 0.75 * len(specs2000)
    for spec in specs2000:
        if "mode_flip" in spec.tags:
            assert plugin.twin(spec) is not None or spec.qform == "ch_v2"
        if "mode_cosmetic" in spec.tags and spec.qform in YN:
            assert plugin.twin(spec) is None


def test_complements_are_opposite_and_every_form_follows_the_outcomes(plugin, specs2000):
    for spec in specs2000:
        o1, o2 = T.outcome_a(spec, 1), T.outcome_a(spec, 2)
        for q in YN:
            f = plugin.QFORMS[q]
            want = int((o1 != o2) == (f.polarity == 1))
            assert plugin.solve_a(spec.replace(qform=q)) == want
        assert plugin.solve_a(spec.replace(qform="ch_v2")) == o2
        if spec.qform in YN:
            partner = plugin.partner(spec)
            a, b = plugin.QFORMS[spec.qform], plugin.QFORMS[partner]
            assert a.predicate == b.predicate and a.polarity == -b.polarity
            assert plugin.solve_a(spec.replace(qform=partner)) == 1 - plugin.solve_a(spec)


def test_metamorphic_relations_keep_the_answer(plugin, specs2000):
    notes = collections.Counter()
    for spec in specs2000[:1000]:
        g4 = [p for p in plugin.relations(spec) if p.kind == "metamorphic"]
        assert len(g4) >= 3
        for prop in g4:
            assert plugin.solve_a(plugin.derive(prop.spec)) == plugin.solve_a(spec), prop.note
            notes[prop.note] += 1
    assert len(notes) == 5


def test_cosmetic_edits_keep_the_ast_and_semantic_edits_change_it(plugin, specs2000):
    """Spec 3.12 admission: a cosmetic rewording gives an AST identical to V1's (rules.ast_equal); the forms differ."""
    n_cos = 0
    for spec in specs2000:
        a1, a2 = plugin.version_asts(spec)
        kind = spec.structure["edit"]["kind"]
        if kind == "cosmetic":
            n_cos += 1
            assert RL.ast_equal(a1, a2)
            assert any(spec.slots[T.sn(1, k)].value[1] != spec.slots[T.sn(2, k)].value[1]
                       for k in spec.structure["v1"])                              # a clause really is reworded
        else:
            assert not RL.ast_equal(a1, a2), spec.structure["edit"]
    assert n_cos >= 100


# ------------------------------------------------------------------------------------------------ balance

def test_gold_balance_and_trap_shares_on_2000_specs(plugin, specs2000):
    n = len(specs2000)
    yn = [s for s in specs2000 if s.qform in YN]
    assert 0.43 <= len(yn) / n <= 0.49
    assert 0.48 <= sum(plugin.solve_a(s) for s in yn) / len(yn) <= 0.52                # gold yes 50 +- 2
    for q in YN:
        ss = [s for s in yn if s.qform == q]
        assert 0.44 <= sum(plugin.solve_a(s) for s in ss) / len(ss) <= 0.56, q
    mat = [_material(s) for s in specs2000]
    assert 0.48 <= sum(mat) / n <= 0.52
    tags = collections.Counter(t for s in specs2000 for t in s.tags)
    share = {k: v / n for k, v in tags.items()}
    assert 0.27 <= share["cosmetic_or_irrelevant"] <= 0.33                           # spec 3.12: 30%
    assert 0.18 <= share["anchor_flip"] <= 0.22                                       # spec 3.12: 20%
    assert share["date_scope_excludes_case"] >= 0.03 and share["mode_masked"] >= 0.05
    assert share["boundary_day"] >= 0.35 and share["boundary_amount"] >= 0.30         # cases sit at boundaries
    assert sum(s.deep for s in specs2000) / n <= 0.10
    v2 = collections.Counter(plugin.solve_a(s) for s in specs2000 if s.qform == "ch_v2")
    tot = sum(v2.values())
    # v2.2 (F3): the roles are balanced inside each option bucket (test_balance.py); pooled over k = 2 and 3 the base
    # rows are about pos .43 / neg .40 / alt .17 (alt exists in the 3-option bucket only)
    assert 0.36 <= v2["pos"] / tot <= 0.50 and 0.33 <= v2["neg"] / tot <= 0.47 and 0.10 <= v2["alt"] / tot <= 0.24
    by_out2 = collections.defaultdict(list)
    for s, m in zip(specs2000, mat):
        by_out2[T.outcome_a(s, 2)].append(m)
    for o in ("pos", "neg"):
        assert 0.44 <= sum(by_out2[o]) / len(by_out2[o]) <= 0.56, o                  # V2's outcome hides the label


def _stump(xs: list, ys: list) -> float:
    best = 0.5
    for th in sorted(set(xs)):
        for sgn in (1, -1):
            best = max(best, sum((sgn * (x - th) >= 0) == bool(y) for x, y in zip(xs, ys)) / len(ys))
    return best


def test_edit_length_does_not_predict_the_label(plugin, ctx, specs2000):
    """Spec 3.12: edit length must not predict the label (best single-threshold accuracy <= 0.55 per feature)."""
    feats = collections.defaultdict(list)
    for spec in specs2000:
        o1, o2 = spec.structure["v1"], spec.structure["v2"]
        shared = set(o1) & set(o2)
        changed = [k for k in shared if T._changed(spec, k)] + sorted(set(o1) ^ set(o2))
        st = plugin.render(spec, ctx).row["state"]
        feats["changed_lines"].append(len(changed))
        feats["clauses_v1"].append(len(o1))
        feats["clauses_v2"].append(len(o2))
        feats["clause_delta"].append(len(o2) - len(o1))
        feats["state_chars"].append(len(st))
        feats["reordered"].append(int([k for k in o1 if k in o2] != [k for k in o2 if k in o1]))
    ys = [_material(s) for s in specs2000]
    for name, xs in feats.items():
        assert _stump(xs, ys) <= 0.55, (name, _stump(xs, ys))


def test_card_rates_span_20_to_80_and_average_one_half():
    for smp, n in (("S1", T.N_CARDS), ("S5", T.N_CARDS_HELD)):
        rates = [T._card_rate(smp, c) for c in range(n)]
        assert all(0.2 <= r <= 0.8 for r in rates) and abs(sum(rates) / n - 0.5) < 1e-12


# ------------------------------------------------------------------------------------------------ G-SL

def _pool_values() -> set:
    out = set(T.CUSTOMERS)
    for d in T.DOMAINS.values():
        out |= set(d.cats + d.conds + d.dates + d.outcomes) | {d.amount, d.title}
    return out


def test_builtin_skins_pass_gsl(plugin, ctx):
    pools = _pool_values()
    for sk in ctx.skins.values():
        if sk.author_mode == "F":
            continue
        v = gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                              name_allow=plugin.NAME_ALLOW)
        assert v == [], (sk.skin_id, v)
        lit = K.PH_RE.sub(" ", sk.text)
        if sk.kind == "skin":                                  # no gold-label word, no blank line, the customer slot
            assert not any(re.search(rf"(?<![a-z]){re.escape(w)}(?![a-z])", lit.lower())
                           for w in plugin.LABEL_WORDS), sk.skin_id
            assert "\n\n" not in sk.text and "CUSTOMER" in sk.decl
        assert not re.search(r"\d", lit), sk.skin_id                           # no literal value outside slots
        assert not [p for p in pools if re.search(rf"(?<![\w-]){re.escape(p)}(?![\w-])", lit)], sk.skin_id
    free = ctx.skin("SK-FREE-1")
    rest = free.text.replace(dict(free.brief)["CUSTOMER"], " ")
    assert gsl.lint_freeform(free.text, dict(free.brief), label_words=plugin.LABEL_WORDS) == []
    assert not re.search(r"\d", rest)


def test_program_templates_hold_no_literal_values(plugin, specs2000):
    """Program text (card, record, version containers) carries rule constants only: no digit, date, month, weekday,
    currency sign, address or name outside the placeholders; every fact value enters through a slot."""
    texts = []
    for dom in T.DOMAINS.values():
        texts += [T.rules_text(dom, "full"), T.rules_text(dom, "short"), T.record_template(dom)]
    for spec in specs2000[:200]:
        for c in ("lines", "table", "update", "diff"):
            texts.append(T.versions_template(spec, c))
    for _sem, text in FX.CLAUSES:
        texts.append(text)
    for t in texts:
        lit = K.PH_RE.sub(" ", t)
        assert not re.search(r"\d", lit), lit[:80]
        assert not re.search(r"[$€£%@]|https?://|\.example", lit), lit[:80]
        assert not set(re.findall(r"[A-Za-z]+", lit)) & (gsl.MONTHS | gsl.WEEKDAYS), lit[:80]
        assert not [n for n in T.CUSTOMERS if n in lit], lit[:80]
    for _sem, text in FX.CLAUSES:                              # clause forms: no fact word outside their slots
        lit = K.PH_RE.sub(" ", text)
        assert not [p for p in _pool_values() - {"amount"} if re.search(rf"(?<![\w-]){re.escape(p)}(?![\w-])", lit)]


def test_gsl_catches_a_skin_that_leaks_the_label(plugin, ctx):
    leak = dataclasses.replace(ctx.skin("SK-CHAT-1"), skin_id="SK-LEAK",
                               text="{CUSTOMER}: hi, case {CASE_ID} is the same under the new policy, nothing changed.")
    c2 = dataclasses.replace(ctx, skins={**ctx.skins, "SK-LEAK": leak})
    spec = plugin.sample(5, "S1")
    probs = pipeline.check_rendered(plugin, spec, plugin.render(spec, c2, skin=leak), c2, run_g15=False)
    rules = {p.split(":", 1)[0] for g, p in probs if g == "G-SL"}
    assert {"gold_label", "negation"} <= rules


# ------------------------------------------------------------------------------------------------ determinism

def _digest(plugin, ctx, n=60) -> str:
    h = hashlib.sha256()
    for seed in range(n):
        for smp in plugin.SAMPLERS:
            spec = plugin.sample(seed, smp)
            h.update(json.dumps(spec.facts(), sort_keys=True, default=str).encode())
            h.update(json.dumps(plugin.render(spec, ctx).row, sort_keys=True).encode())
    return h.hexdigest()


def test_generation_is_deterministic_by_seed(plugin, ctx):
    a = pipeline.build_unit(plugin, plugin.sample(17, "S4"), ctx, run_g15=False).rows
    b = pipeline.build_unit(plugin, plugin.sample(17, "S4"), ctx, run_g15=False).rows
    assert a and a == b
    assert plugin.sample(17, "S4").facts() != plugin.sample(18, "S4").facts()
    c = FX.ctx()
    assert _digest(plugin, ctx) == _digest(T.T24Plugin(lexicon=c.lexicon, packs=T.STANDIN_PACKS), c)


def test_generation_does_not_depend_on_the_hash_seed(plugin, ctx):
    code = ("import sys; sys.dont_write_bytecode = True; sys.path.insert(0, %r)\n"
            "from families.T24 import fixtures as FX, plugin as T, test_plugin as TP\n"
            "c = FX.ctx(); print(TP._digest(T.T24Plugin(lexicon=c.lexicon, packs=T.STANDIN_PACKS), c, 20))") % str(C2_BUILD)
    outs = set()
    for hs in ("1", "4242"):
        env = {**os.environ, "PYTHONHASHSEED": hs, "PYTHONDONTWRITEBYTECODE": "1"}
        res = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env, timeout=300)
        assert res.returncode == 0, res.stderr[-2000:]
        outs.add(res.stdout.strip())
    assert outs == {_digest(plugin, ctx, 20)}


# ------------------------------------------------------------------------------------------------ distractors

def test_error_models_name_wrong_options(plugin, ctx):
    sets = []
    for seed in range(500):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            if spec.qform != "ch_v2":
                continue
            os_ = plugin.render(spec, ctx).option_set
            assert check_named(os_) == []
            for o in os_.options:
                assert set(o.err) <= set(plugin.error_models()) and all(e in CATALOG for e in o.err)
            sets.append(os_)
    named = sum(1 for s in sets for o in s.options if o.role == "error")
    wrong = sum(1 for s in sets for o in s.options if o.role != "gold")
    assert named / wrong >= 0.90, named / wrong                # the rest keep the kit role 'closed' (S15)
    used = collections.Counter(e for s in sets for o in s.options for e in o.err)
    assert set(used) == set(plugin.error_models()), set(plugin.error_models()) - set(used)
    for k, counts in position_counts(sets).items():
        assert min(counts) / sum(counts) >= 0.8 / k, (k, counts)


# ------------------------------------------------------------------------------------------------ gates have teeth

def _gate_failures(plugin, ctx, n=40) -> collections.Counter:
    out = collections.Counter()
    for seed in range(n):
        for smp in ("S1", "S2", "S3"):
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            for g, _ in res.problems:
                out[g] += 1
    return out


def test_g2_catches_a_solver_a_inclusivity_bug(plugin, ctx, monkeypatch):
    monkeypatch.setitem(T.OP_SYM, "ge", ">")                        # A reads "at least" as "more than"
    assert _gate_failures(plugin, ctx)["G2"] > 0


def test_g2_catches_a_solver_b_day_zero_bug(plugin, ctx, monkeypatch):
    monkeypatch.setattr(B, "OUTCOME_SQL", B.OUTCOME_SQL.replace("julianday(f.req) -", "1 + julianday(f.req) -"))
    assert _gate_failures(plugin, ctx)["G2"] > 0


def test_g3_catches_a_record_that_prints_the_wrong_date(plugin, ctx, monkeypatch):
    real = T.record_template
    monkeypatch.setattr(T, "record_template", lambda dom: real(dom).replace("{D2}", "{D1}", 1))
    assert _gate_failures(plugin, ctx)["G3"] > 0


def test_gtw_catches_a_wrong_twin_prediction(plugin, ctx, monkeypatch):
    real = T.predict

    def no_special(v):                                              # the prediction forgets special time limits
        return {k: p for k, p in v.items() if k not in ("ovc", "ovd")}
    monkeypatch.setattr(T, "predict", lambda q, v1, v2, case: real(q, no_special(v1), no_special(v2), case))
    assert _gate_failures(plugin, ctx, n=60)["G-TW"] > 0


def test_tests_write_no_file():
    """A37 f: the family folder holds code, its spec, the Haiku task files (haiku/, after A38), the frozen pools
    (pools/) and the pilot outputs (pilot/, pilot_i1/, written by pilot.py / run_pilot_i1.py, never by a test); no
    row, pool or cache file anywhere else."""
    assert set(os.listdir(T.HERE)) <= HERE_FILES | {"__pycache__"}
    ok_dirs = {"haiku", "pools", "pilot", "pilot_i1", "pilot_i2", "_backup_i2"}
    assert not [p for p in T.HERE.rglob("*") if p.suffix in (".jsonl", ".json", ".csv", ".parquet")
                and not ok_dirs & set(p.relative_to(T.HERE).parts)]
    assert not [p for p in T.HERE.rglob("*.jsonl") if not ok_dirs & set(p.relative_to(T.HERE).parts)]


# ------------------------------------------------------------------------------------------------ Haiku pass (v2)

def test_g0_is_frozen_after_the_haiku_pass():
    """H43: the plugin pins this file's sha; the pass that v2 resolves is recorded with the sha it read."""
    assert T.T24Plugin.G0_SHA256 == hashlib.sha256(T.HERE.joinpath("G0_SPEC.md").read_bytes()).hexdigest()
    rec = T.T24Plugin.G0_AMBIGUITY_PASS
    assert rec["task_id"] == "c2-data-stage-a/amb:T24" and rec["points"] == rec["resolved"] == 45
    amb = json.loads(T.HERE.joinpath(rec["record"]).read_text(encoding="utf-8"))
    assert amb["n_points"] == len(amb["points"]) == 45 and rec["read_g0_sha256"] in amb["input"]
    g0 = T.HERE.joinpath("G0_SPEC.md").read_text(encoding="utf-8")
    for h in range(1, 46):                                                         # every point is listed and resolved
        assert re.search(rf"\bH{h}\b", g0.split("## 4.")[1].split("## 5.")[0]), h
        assert re.search(rf"\bH{h}\b", g0.split("## 5.")[1]), h                     # ... and resolved in section 5


def _g0_card(box: str, dom) -> str:
    pos, alt, neg = dom.outcomes
    return (box.replace("{title}", dom.title).replace("{money field}", dom.amount).replace("{NEG}", neg)
            .replace("{ALT}", alt).replace("{POS}", pos)
            .replace("{c1, c2, ... and cn}", T._list(dom.cats)).replace("{k1, k2 and k3}", T._list(dom.conds)))


def test_card_v22_is_quoted_in_the_g0_and_states_the_count_rules():
    """H3-H6, H15, H16, H45 (v2) and F2 (v2.2): the card states calendar days, the printed count, day zero, both
    special scopes, the inclusive window and that a special clause replaces only the limit; the G0 boxes hold the full
    and the short card verbatim (pack constants as placeholders)."""
    dom = T.DOMAINS["retail"]
    full, short = T.rules_text(dom, "full"), T.rules_text(dom, "short")
    for card in (full, short):
        assert "A special time-limit clause replaces only the limit, for" in card
        assert "whose date it names lies in its window (both end dates included)" in card
        assert "calendar days from the date named in the time-limit clause" in card and "day zero" in card
        assert "printed in the record" in card and CLOSED_WORLD in card
    assert "Late means a day count above the limit." in full
    boxes = T.HERE.joinpath("G0_SPEC.md").read_text(encoding="utf-8").split("```")
    assert _g0_card(boxes[1].strip("\n"), dom) == full and _g0_card(boxes[3].strip("\n"), dom) == short
    assert T.card_spec(dom).problems() == []                       # the short phrasing keeps every rule marker
    for d in T.DOMAINS.values():
        assert T.card_spec(d).problems() == [], d.key


def test_card_placement_style_share_and_defs_style(plugin, ctx):
    """F2: yes/no rows carry the card in row.card (printed once), choice rows in the instructions before the
    question; ~15% of units carry the short style, the same on every row of a unit (G-TW: complements share the
    card); solver B parses both styles."""
    styles = collections.Counter()
    for seed in range(120):
        for smp in TRAIN:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            assert res.ok, res.problems[:2]
            unit_styles = set()
            for r in res.rows:
                rules, question = split_rules(r)
                assert CLOSED_WORLD in rules
                if r["qtype"] == "noul":
                    assert r["card"] and r["card"] == rules and "\n\n" not in r["instructions"]
                    assert r["meta"]["defs_style"].startswith("rules_in_card_")
                else:
                    assert r["card"] is None and r["instructions"] == rules + "\n\n" + question
                    assert r["meta"]["defs_style"].startswith("rules_in_instructions_")
                unit_styles.add(r["meta"]["defs_style"].rsplit("_", 1)[1])
            assert len(unit_styles) == 1, unit_styles
            styles[unit_styles.pop()] += 1
    n = sum(styles.values())
    assert abs(styles["short"] / n - T.SHORT_CARD_SHARE) <= 0.03, styles


def test_construction_outcome_equals_solver_a(specs2000):
    """H31: the generator's target (direct_outcome) is a draw filter; gold is solver A. They agree on every spec."""
    for spec in specs2000:
        dom, v1, v2, case = T.facts(spec)
        assert (T.direct_outcome(v1, case), T.direct_outcome(v2, case)) == (T.outcome_a(spec, 1), T.outcome_a(spec, 2))


def test_one_pack_per_card_and_stricter_pack_checks():
    """H34, H35: card c of the i-th training sampler takes pack (8 i + c) mod P; S5 card c takes held-out pack c mod P;
    check_domain refuses a title without 'policy', a bad date field and label words in pack strings."""
    for packs in (T.STANDIN_PACKS, T.POOL_PACKS):
        for i, smp in enumerate(TRAIN):
            for c in range(T.N_CARDS):
                assert T.domain_for(smp, c, packs).key == packs.train[(8 * i + c) % len(packs.train)]
    counts = collections.Counter(T.domain_for(s, c, T.STANDIN_PACKS).key for s in TRAIN for c in range(T.N_CARDS))
    assert min(counts.values()) >= 3
    good = T.DOMAINS["retail"]
    for bad in (dataclasses.replace(good, title="returns rules"),
                dataclasses.replace(good, dates=("order date", "request date")),
                dataclasses.replace(good, dates=("order day", "delivery date")),
                dataclasses.replace(good, title="returns change policy"),
                dataclasses.replace(good, cats=("electronics", "clothing", "credit cards", "toys")),
                dataclasses.replace(good, conds=("unopened", "opened", "not sealed"))):
        assert T.check_domain(bad), bad
