"""c2_build/families/T29/test_plugin.py: in-memory tests for the T29 plugin (C2_DATA_SPEC 3.4, 4.1; G0_SPEC.md).

CPU only, in memory: no test writes a file (A37 f: no C2 data before A38); the skins, wordings and lexicon forms are
the Claude-written stand-ins in fixtures.py. Run (from lean/):
  ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T29
Checks:
  contract     validate_plugin(strict=True) == []; solver B shares no code path with solver A
  G2 / G3      solver A == solver B and parse(row) == canonical facts on 5,000 sampled specs (1,000 per sampler),
               with G-SL, G-LEX and the row schema on every row
  exactness    on rows with a missing field, solver A's Kleene verdict equals the verdict set over explicit
               completions of that field (solver A's own resolve path on complete specs)
  pipeline     relation units through G2, G3, G4, G-SL, G-LEX, G-TW and schema (G15 on a sample); overlay shares
  relations    twins differ in exactly one input slot and the gold flips exactly as predicted; premise removal
               gives cannot decide; complements are opposite
  balance      2,000 training specs: question-form shares, yes rate, abstain shown, yes = bad outcome, gold
               position, trap shares, deep share, per-card yes rates; verdict shares on every ch_verdict row of the
               relation units (premise-removal twins supply most CANNOT DECIDE golds)
  G6 pre-check visible display facts (CANNOT DECIDE shown, a field missing, conversation kind) barely move the gold;
               the card's composition (atom types, tiers, rule counts) does not move it at all
  G-SL         the built-in placeholder skins carry no gold-label word and no literal value outside their slots
  determinism  the same seed gives the same spec and rows, also in a fresh process with another hash seed
  bugs         injected bugs in solver B, solver A, the option texts, the card text and a twin prediction are caught
"""
from __future__ import annotations

import collections
import dataclasses
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pytest  # noqa: E402

from c2_kit import cards as CARDS  # noqa: E402
from c2_kit import gsl, pipeline  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from families.T29 import fixtures as FX  # noqa: E402
from families.T29 import plugin as P  # noqa: E402
from families.T29 import solver_b as B  # noqa: E402

TRAIN = ("S1", "S2", "S3", "S4")


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T29Plugin(lexicon=ctx.lexicon, packs=P.PACKS)          # the six program stand-in packs (tests only)


@pytest.fixture(scope="module")
def train_specs(plugin):
    return [plugin.sample(seed, smp) for seed in range(500) for smp in TRAIN]


# ------------------------------------------------------------------------------------------------ contract

def test_plugin_meets_the_strict_contract(plugin):
    assert KP.validate_plugin(plugin, strict=True) == []
    assert KP.check_independence(plugin) == []
    assert plugin.PARADIGM_A != plugin.PARADIGM_B
    assert len(Path(plugin.G0_LITE).read_text(encoding="utf-8").splitlines()) <= 200


def test_solver_b_imports_nothing_from_solver_a():
    src = Path(B.__file__).read_text(encoding="utf-8")
    assert "families.T29.plugin" not in src and "from . import plugin" not in src
    assert "c2_kit.rules" not in src and "glob_a" not in src


# ------------------------------------------------------------------------------------------------ G2 / G3 on 5,000

def test_solver_a_equals_solver_b_on_5000_specs(plugin, ctx):
    n, missing, verdicts, problems = 0, 0, collections.Counter(), []
    for seed in range(1000):
        for smp in plugin.SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            gold = plugin.solve_a(spec)
            view = B.parse(rr.row, ctx)
            facts = {k: v for k, v in view.items() if k != "options"}
            if facts != plugin.canonical_for(spec, rr.row["meta"]["c2"]["author_mode"]):
                problems.append((seed, smp, "G3"))
            b = B.solve_b(view)
            if b != gold or rr.answer != gold:
                problems.append((seed, smp, "G2", gold, b))
            if rr.row["qtype"] == "choice":
                if view["options"][rr.row["options"].index(rr.row["gold"])] != gold:
                    problems.append((seed, smp, "option key"))
            for gate, detail in pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False):
                problems.append((seed, smp, gate, detail))
            n += 1
            verdicts[(spec.qform, gold)] += 1
            missing += bool(plugin._card_missing(spec))
    assert n == 5000
    assert problems == []
    assert missing > 1000 and verdicts[("ch_verdict", "cannot")] > 50   # the missing-field paths are exercised
    assert sum(v for (q, _), v in verdicts.items() if q == "ch_rule") > 100


def test_kleene_verdict_equals_explicit_completions(plugin):
    """Solver A's Kleene path on a row with a missing field == the verdicts of the completed rows (resolve path)."""
    checked = collections.Counter()
    for seed in range(400):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            if spec.qform != "ch_verdict" or plugin._missing(spec):
                continue
            v = spec.env()
            for f in spec.structure["fields"]:
                if f not in P.MISSABLE or f not in spec.slots:
                    continue
                gap = plugin.derive(spec.with_slot(f, None))
                outs = {plugin.solve_a(plugin.derive(spec.with_slot(f, s))) for s in _completions(spec, f, v)}
                want = outs.pop() if len(outs) == 1 else "cannot"
                assert plugin.solve_a(gap) == want, (seed, smp, f)
                checked[want == "cannot"] += 1
    assert checked[True] > 50 and checked[False] > 50


def _completions(spec, field, v):
    th = [v[k] for k in v if k.startswith("T_")]
    nums = sorted({x for t in th for x in (t - 1, t, t + 1)} | {0, 1})
    pack = next(p for p in P.PACKS if p["id"] == spec.pack)
    if field == "N_RECORDS":
        return [S.count_slot(x, P.U_RECORD) for x in nums if x >= 1]
    if field == "AMOUNT":
        return [S.cents_slot(x) for x in nums if x >= 0]
    if field == "LAST_EDIT":
        return [S.datetime_slot(v["NOW"] - dt.timedelta(minutes=x)) for x in nums if x >= 0]
    if field == "DEST_DOMAIN":
        return [S.id_slot(d) for d in (pack["org"],) + pack["lookalike"] + pack["partners"]]
    pool = {"OWNER_TEAM": P.TEAMS, "ENV": P.ENVS, "DATA_CLASS": P.CLASSES}[field]
    return [S.category_slot(k, pool) for k in sorted(pool)]


# ------------------------------------------------------------------------------------------------ pipeline

@pytest.fixture(scope="module")
def units(plugin, ctx):
    """1,000 relation units (200 seeds x 5 samplers): G15 on the first 15, every other gate on all."""
    out = []
    for seed in range(200):
        for smp in plugin.SAMPLERS:
            out.append((seed, smp, pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=seed < 3)))
    return out


def test_relation_units_pass_every_gate(plugin, units):
    bad = [(seed, smp, res.problems[:3]) for seed, smp, res in units if not res.ok]
    assert bad == []
    ok = [res for _, _, res in units]
    for seed, smp, res in units:
        if smp == "S5":
            assert all(r["meta"]["dev_only"] for r in res.rows)
            assert all(R.validate_row(r, training=True) for r in res.rows)
    rep = pipeline.overlay_report(ok, plugin)
    rows = [r for u in ok for r in u.rows]
    roles = collections.Counter(r["role"] for r in rows)
    assert rep["complement_share_of_yes_no"] >= 0.20 and rep["non_syntactic_share_of_pairs"] >= 0.30
    assert 0.20 <= rep["twin_share"] <= 0.25
    assert 0.05 <= rep["equiv_share"] <= 0.10
    assert 0.03 <= rep["attack_share"] <= 0.08
    assert 0.03 <= roles["premise_removal"] / len(rows) <= 0.07
    assert rep["abstain"]["pass"] and rep["abstain"]["wrong_share"] >= 0.5
    assert max(collections.Counter(r["call_id"] for r in rows).values()) <= 3
    assert all(R.approx_tokens(r) <= R.MAX_TOKENS for r in rows)
    # the candidate-list design (G0 v1.5): ONE shared-header table of 3-5 candidate lines on every row, a seed-only count
    # with mean 3.5, the same card text (and table) on a unit's complement / twin partners of the same card, the card
    # style from the unit key (never the question or the label)
    for seed, smp, res in units:
        spec = plugin.sample(seed, smp)
        assert spec.structure["cands"] == P_N_CANDS(seed, smp)
        for r in res.rows:
            tables = [b for b in r["state"].split("\n\n") if b.startswith(("Proposed calls", "admin-console> list"))]
            lines = tables[0].split("\n")
            head = 3 if lines[0] == "Proposed calls:" else 2 if lines[0].startswith("admin-console") else 1
            assert len(tables) == 1 and len(lines) - head == spec.structure["cands"], (seed, smp)
    n = [plugin.sample(seed, smp).structure["cands"] for seed, smp, _ in units]
    mean = sum(nc * w for nc, w in P.N_CANDS_W) / sum(w for _, w in P.N_CANDS_W)      # the G0 count mix (v1.6: 3 on every card)
    assert set(n) == {nc for nc, _ in P.N_CANDS_W} and abs(sum(n) / len(n) - mean) <= 0.06
    styles = collections.Counter(r["meta"]["defs_style"].rsplit("_", 1)[1] for _, _, res in units for r in res.rows)
    assert set(styles) == {"compact", "short"} and styles["short"] / sum(styles.values()) <= 0.15 + 0.02


def P_N_CANDS(seed, smp):
    """The candidate count a seed draws (seed and sampler only; P.N_CANDS_W)."""
    u, acc = P.uhash(P.FAMILY, "ncand", smp, seed), 0.0
    for nc, w in P.N_CANDS_W:
        acc += w
        if u < acc:
            return nc
    return P.N_CANDS_W[-1][0]


def test_verdict_shares_on_all_choice_rows(units):
    """Spec 3.4 balance over every ch_verdict row (bases, twins, premise-removal partners, equiv / inv copies)."""
    ch = [rr for _, _, res in units for rr in res.rendered if rr.row["meta"]["qform"] == "ch_verdict"]
    vc = collections.Counter(rr.answer for rr in ch)
    assert abs(vc["cannot"] / len(ch) - 0.15) <= 0.04, vc
    for k in ("go", "ask", "refuse"):
        assert abs(vc[k] / len(ch) - 0.85 / 3) <= 0.05, (k, vc)
    shown = [rr for rr in ch if rr.option_set.abstain_shown]
    assert 0.55 <= len(shown) / len(ch) <= 0.75
    assert sum(rr.answer != "cannot" for rr in shown) / len(shown) >= 0.5


def _visible(plugin, spec, shown):
    """The display facts a partial-input reader sees without reading the rules: CANNOT DECIDE shown, a field shown
    as (missing) in any candidate's snapshot, and the conversation kind (none / mention / explicit). (G0 v1.4: whether
    the conversation confirms the REQUESTED call is a fact of the question and the card together, not of the card.)"""
    conv = "none"
    if spec.structure["conv"]:
        conv = "mention" if spec.env()["CONF"] == P.CONF_MENTION else "explicit"
    return shown, plugin._card_missing(spec), conv


def _row_specs(plugin, spec):
    """(row spec, CANNOT DECIDE shown) for the base and every emitted partner (equiv / inv copies repeat the base)."""
    shown = spec.qform == "ch_verdict" and spec.structure["show_abstain"]
    out = [(spec, shown)]
    for prop in plugin.relations(spec):
        if prop.kind == "complement":
            out.append((spec.replace(qform=prop.qform), False))
        elif prop.kind in ("equiv", "inv"):
            out.append((spec, shown))
        elif prop.kind == "twin":
            out.append((plugin.derive(prop.spec), shown))
        elif prop.kind == "premise_removal":
            out.append((plugin.derive(prop.spec), True))
    return out


def test_visible_facts_do_not_predict_the_gold(plugin):
    """G6 pre-check (partial input), held out: the best constant answer per partition of the visible display facts
    (per question form), fitted on half of 4,000 training bases with all their relation rows and scored on the
    other half (2-fold), beats the best constant per question form by <= 3.5 pp on ch_verdict rows and <= 1.5 pp on
    yes/no rows. The ch_verdict residue is semantic (an explicit confirmation of this call rules out ASK FIRST, and
    conversation twins teach exactly that): about 2.5 pp before the C2 pilot's G6."""
    rows = []
    for seed in range(1000):
        for smp in TRAIN:
            base = plugin.sample(seed, smp)
            for s, shown in _row_specs(plugin, base):
                rows.append((seed % 2, s.qform, _visible(plugin, s, shown), plugin.solve_a(s)))
    for qtype, cap in (("choice", 0.035), ("noul", 0.015)):
        sub = [r for r in rows if plugin.QFORMS[r[1]].qtype == qtype and r[1] != "ch_rule"]
        gain = 0.0
        for fold in (0, 1):
            part, form = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
            for f, q, vis, gold in sub:
                if f != fold:
                    part[(q,) + vis][gold] += 1
                    form[q][gold] += 1
            for f, q, vis, gold in sub:
                if f == fold:
                    by_part = (part.get((q,) + vis) or form[q]).most_common(1)[0][0]
                    gain += ((by_part == gold) - (form[q].most_common(1)[0][0] == gold)) / len(sub)
        assert gain <= cap, (qtype, round(gain, 4))


# ------------------------------------------------------------------------------------------------ relations

def test_twins_flip_exactly_as_predicted_and_complements_are_opposite(plugin, train_specs):
    n_twin = n_prem = n_comp = 0
    changed = collections.Counter()
    for spec in train_specs:
        base = plugin.solve_a(spec)
        for prop in plugin.relations(spec):
            if prop.kind == "twin":
                twin = plugin.derive(prop.spec)
                assert slot_diff(spec, twin) == {prop.changed_slot}
                assert plugin.solve_a(twin) == prop.expect != base
                changed[prop.changed_slot] += 1
                n_twin += 1
            elif prop.kind == "premise_removal":
                gap = plugin.derive(prop.spec)
                assert slot_diff(spec, gap) == {prop.changed_slot} and prop.changed_slot not in gap.slots
                assert plugin.solve_a(gap) == "cannot" != base
                n_prem += 1
            elif prop.kind == "complement":
                partner = plugin.QFORMS[prop.qform]
                assert partner.polarity == -1 and partner.predicate == plugin.QFORMS[spec.qform].predicate
                assert base + plugin.solve_a(spec.replace(qform=prop.qform)) == 1
                n_comp += 1
            elif prop.kind == "metamorphic":
                assert plugin.solve_a(plugin.derive(prop.spec)) == (base if prop.expect == "same" else prop.expect)
        if spec.qform in P.COMPLEMENTS:                       # every declared complement form, not only the drawn one
            for q2 in P.COMPLEMENTS[spec.qform]:
                assert base + plugin.solve_a(spec.replace(qform=q2)) == 1
    assert n_twin > 400 and n_prem > 30 and n_comp > 200
    assert len(changed) >= 8                                    # twins move many different slots


# ------------------------------------------------------------------------------------------------ balance

def test_label_balance_on_2000_specs(plugin, ctx, train_specs):
    specs = train_specs
    assert len(specs) == 2000
    q = collections.Counter(s.qform for s in specs)
    for form, share in P.QFORM_SHARES:
        assert abs(q[form] / len(specs) - share) <= 0.03, form
    ver = [s for s in specs if s.qform == "ch_verdict"]
    shown = [s for s in ver if s.structure["show_abstain"]]
    assert abs(len(shown) / len(ver) - 0.60) <= 0.05                 # label-blind, before the gold
    assert abs(sum(plugin.solve_a(s) == "cannot" for s in shown) / len(shown) - P.CANNOT_SHOWN) <= 0.03
    assert all(plugin._card_missing(s) for s in shown)                 # every shown card has a (missing) field
    decided = collections.Counter(plugin.solve_a(s) for s in ver if plugin.solve_a(s) != "cannot")
    for k in ("go", "ask", "refuse"):
        assert abs(decided[k] / sum(decided.values()) - 1 / 3) <= 0.05, (k, decided)
    yn = [s for s in specs if s.qform.startswith("yn_")]
    assert abs(sum(plugin.solve_a(s) for s in yn) / len(yn) - 0.5) <= 0.03
    assert abs(sum(bool(plugin.QFORMS[s.qform].yes_is_bad) for s in yn) / len(yn) - 0.5) <= 0.05
    rates = [P._rate(smp, i, P.N_CARDS) for smp in TRAIN for i in range(P.N_CARDS)]
    assert min(rates) >= 0.2 and max(rates) <= 0.8 and abs(sum(rates) / len(rates) - 0.5) < 1e-9
    tags = collections.Counter(t for s in specs for t in s.tags)
    share = {k: v / len(specs) for k, v in tags.items()}
    bands = {"threshold_boundary": (0.15, 0.30), "harmless_irreversible": (0.10, 0.20),
             "alarming_reversible_go": (0.10, 0.22), "owner_triggers": (0.10, 0.20),
             "confirm_other_call": (0.06, 0.14), "missing_irrelevant": (0.20, 0.40)}
    for k, (lo, hi) in bands.items():
        assert lo <= share.get(k, 0) <= hi, (k, share.get(k))
    assert sum(s.deep for s in specs) / len(specs) <= 0.10
    tone = collections.Counter((P.ACTION_TONE[s.env()["ACTION"]], plugin._verdict_c(
        plugin._rule_truths(s), plugin._confirmed_c(s))) for s in specs)
    alarming = sum(c for (t, _), c in tone.items() if t == "alarming") / sum(tone.values())
    for v in ("go", "ask", "refuse"):                           # tone is drawn independently of the verdict
        assert abs(tone[("alarming", v)] / (tone[("alarming", v)] + tone[("benign", v)]) - alarming) <= 0.06
    pos = collections.defaultdict(collections.Counter)
    for s in ver:
        rr = plugin.render(s, ctx)
        pos[len(rr.row["options"])][rr.option_set.gold_index] += 1
    for k, c in pos.items():
        tot = sum(c.values())
        assert all(abs(c[i] / tot - 1 / k) <= 0.08 for i in range(k)), (k, c)


def test_card_composition_is_label_blind(plugin):
    """A card-only reader learns nothing: the verdict mix given an atom type on the card, its tier, the number of
    rules, of forbidden rules or of two-part rules stays at the prior within 4 standard errors (round-1 lesson 4;
    a G6 / G7 pre-check on 6,000 training specs; the rule-count cue this replaced sat at about 5 SE)."""
    specs = [plugin.sample(seed, smp) for seed in range(1500) for smp in TRAIN]
    verdict = {id(s): plugin._verdict_c(plugin._rule_truths(s), plugin._confirmed_c(s)) for s in specs}
    prior = collections.Counter(verdict.values())
    n = len(specs)
    groups = collections.defaultdict(set)
    for s in specs:
        rules = s.structure["rules"]
        for r in rules:
            for a in r["atoms"]:
                groups[("atom", a)].add(id(s))
                groups[("atom_tier", a, r["tier"])].add(id(s))
        groups[("n_rules", len(rules))].add(id(s))
        groups[("n_forbid", sum(r["tier"] == "forbid" for r in rules))].add(id(s))
        groups[("n_pairs", sum(len(r["atoms"]) == 2 for r in rules))].add(id(s))
    tested = 0
    for key, ids in groups.items():
        if len(ids) < 400:
            continue
        c = collections.Counter(verdict[i] for i in ids)
        for v in ("go", "ask", "refuse"):
            p0 = prior[v] / n
            se = (p0 * (1 - p0) / len(ids)) ** 0.5
            assert abs(c[v] / len(ids) - p0) <= 4 * se, (key, v, round(c[v] / len(ids), 3), round(p0, 3))
            tested += 1
    assert tested > 60


# ------------------------------------------------------------------------------------------------ G-SL

def test_builtin_skins_pass_gsl_and_hold_no_label_word_or_value(plugin, ctx):
    label_forms = gsl._label_forms(plugin.LABEL_WORDS)
    for sk in ctx.skins.values():
        if sk.author_mode == "F":
            fills = dict(sk.brief)
            assert gsl.lint_freeform(sk.text, fills, label_words=plugin.LABEL_WORDS) == [], sk.skin_id
            continue
        assert gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                                 name_allow=plugin.NAME_ALLOW) == [], sk.skin_id
        if sk.kind == "skin":
            lit = gsl._literal(sk.text).lower()
            assert not any(ch.isdigit() for ch in lit), sk.skin_id
            assert not set(gsl._WORD.findall(lit)) & label_forms, sk.skin_id
            assert {"REQUESTER", "REASON"} <= set(sk.decl), sk.skin_id
    leaky = dataclasses.replace(ctx.skin("SK-CHAT-1"), skin_id="SK-LEAK",
                                text=ctx.skin("SK-CHAT-1").text + " It is fine to go ahead, nothing to ask.")
    found = {v.rule for v in gsl.lint_template(leaky, label_words=plugin.LABEL_WORDS, name_allow=plugin.NAME_ALLOW)}
    assert {"gold_label", "negation"} <= found
    numbered = dataclasses.replace(ctx.skin("SK-MEMO-1"), skin_id="SK-NUM", text="Note from {REQUESTER} about "
                                   "{REASON}: run it on {TARGET} for 200 records today.")
    found = {v.rule for v in gsl.lint_template(numbered, label_words=plugin.LABEL_WORDS)}
    assert {"number", "relative_time"} <= found


def test_lexicon_forms_are_admitted_and_unambiguous(ctx):
    assert all(f.unit_ok for f in ctx.lexicon.forms.values())
    assert ctx.lexicon.gate()["pass"]


# ------------------------------------------------------------------------------------------------ determinism

def test_generation_is_deterministic(plugin, ctx):
    fresh_ctx = FX.ctx()
    fresh = P.T29Plugin(lexicon=fresh_ctx.lexicon, packs=P.PACKS)
    for seed in (0, 7, 31, 99):
        for smp in plugin.SAMPLERS:
            a, b = plugin.sample(seed, smp), fresh.sample(seed, smp)
            assert a.structure_hash() == b.structure_hash() and a.tags == b.tags
            ra = pipeline.build_unit(plugin, a, ctx, run_g15=False).rows
            rb = pipeline.build_unit(fresh, b, fresh_ctx, run_g15=False).rows
            assert ra == rb
    assert plugin.sample(5, "S1").structure_hash() != plugin.sample(6, "S1").structure_hash()


_PROBE = """
import sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, %r)
from families.T29 import plugin as P, fixtures as FX
c = FX.ctx(); p = P.T29Plugin(lexicon=c.lexicon, packs=P.PACKS)
out = []
for s in range(40):
    for smp in p.SAMPLERS:
        sp = p.sample(s, smp)
        out.append([sp.structure_hash(), p.render(sp, c).row["id"]])
print(json.dumps(out))
"""


def test_determinism_across_processes_and_hash_seeds():
    outs = []
    for hs in ("1", "2"):
        env = {**os.environ, "PYTHONHASHSEED": hs, "PYTHONDONTWRITEBYTECODE": "1"}
        res = subprocess.run([sys.executable, "-c", _PROBE % str(C2_BUILD)], capture_output=True, text=True, env=env,
                             timeout=300, check=True)
        outs.append(json.loads(res.stdout))
    assert outs[0] == outs[1]


# ------------------------------------------------------------------------------------------------ injected bugs

def _gate_failures(plugin, ctx, n=60, samplers=("S1", "S2", "S3")):
    out = collections.Counter()
    for seed in range(n):
        for smp in samplers:
            try:
                spec = plugin.sample(seed, smp)
            except KP.ContractError:
                out["sample"] += 1
                continue
            res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
            for g, _ in res.problems:
                out[g] += 1
    return out


def test_g2_catches_a_solver_b_boundary_bug(plugin, ctx, monkeypatch):
    monkeypatch.setitem(B.SQL_OP, "cmp.ge", ">")              # "at least" read as strict
    assert _gate_failures(plugin, ctx)["G2"] > 0


def test_a_solver_a_boundary_bug_is_caught(plugin, ctx, monkeypatch):
    monkeypatch.setitem(P.CMP_OP, "cmp.gt", ">=")             # solver A reads "more than" as "at least"
    f = _gate_failures(plugin, ctx)
    assert f["sample"] + f["G2"] > 0


def test_g2_catches_mislabelled_option_texts(plugin, ctx, monkeypatch):
    monkeypatch.setitem(P.VERDICT_TEXT, "go", "Refuse it outright")
    monkeypatch.setitem(P.VERDICT_TEXT, "refuse", "Go ahead right now")
    assert _gate_failures(plugin, ctx)["G2"] > 0


def test_g3_catches_a_card_that_prints_the_wrong_tier(plugin, ctx, monkeypatch):
    monkeypatch.setitem(P.TIER_TEXT, "forbid", "needs confirmation")
    monkeypatch.setitem(P.TIER_TEXT, "confirm", "forbidden")
    f = _gate_failures(plugin, ctx)
    assert f["G3"] > 0 and f["G2"] > 0


def test_gtw_catches_a_wrong_twin_prediction(plugin, ctx, monkeypatch):
    real = P.T29Plugin._twin

    def wrong(self, spec):
        prop = real(self, spec)
        if prop is not None and spec.qform.startswith("yn_"):
            prop = dataclasses.replace(prop, expect=1 - prop.expect)
        return prop

    monkeypatch.setattr(P.T29Plugin, "_twin", wrong)
    assert _gate_failures(plugin, ctx, samplers=("S1", "S2", "S3", "S4"))["G-TW"] > 0


def test_g2_catches_a_kleene_shortcut_in_solver_b(plugin, ctx, monkeypatch):
    monkeypatch.setattr(B, "_witnesses", lambda field, atoms, view: [_witness_one(field, atoms, view)])
    assert _gate_failures(plugin, ctx, n=120)["G2"] > 0       # one guessed value instead of the completions


def _witness_one(field, atoms, view):
    return 0 if field in ("records", "amount", "minutes") else "\x00another value"


# ------------------------------------------------------------------------------------------------ review fix: twin mix

def test_abstain_share_holds_on_every_emitted_row(plugin, ctx):
    """Minimal-edit twins mirror their base: fixing the one failing item of a base lands on the abstain key, so
    unthinned twins piled up there (39% of all emitted ch_rule rows against a G0 target of 1 / k, about 20%). Twins onto
    the key are thinned (kit relations.abstain_twin_kept); P(gold | key shown) over ALL emitted rows (base, twin, equiv,
    inv) is now within 5 pp of the target."""
    shown = gold = 0
    chance = 0.0
    roles = collections.Counter()
    for seed in range(2500):
        for smp in ("S1", "S2", "S3", "S4"):
            spec = plugin.sample(seed, smp)
            if spec.qform != "ch_rule":
                continue
            res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
            for rr in (res.rendered if res.ok else []):
                os_ = rr.option_set
                if os_ is None or not any(o.key == "none" for o in os_.options):
                    continue
                shown += 1
                gold += os_.gold.key == "none"
                chance += 1 / len(os_.options)
                roles[rr.row["role"]] += 1
    target = chance / shown
    assert shown >= 300 and roles["twin"] >= 30, (shown, roles)
    assert abs(gold / shown - target) <= 0.05, (gold / shown, target, roles)


# ------------------------------------------------------------------------------------------------ G0 v1.1 resolutions

def test_g0_ambiguity_resolutions_hold_on_bases_and_partners(plugin, ctx):
    """G0 section 5 (B1-B27) as invariants on 2,000 training bases + 500 S5 bases and every relation partner spec:
    whole-minute times with LAST <= NOW and exact printed minutes (B1-B3); offsets and windows (B5, B17); amount /
    destination couplings and missing-field limits (B7-B10); thresholds >= 1 and strict tier orders (B14, B16); the
    answer-code legend lists exactly the offered verdicts and the missing-data line follows B23."""
    from c2_kit import distractors as D
    specs = []
    for seed in range(500):
        for smp in plugin.SAMPLERS:
            base = plugin.sample(seed, smp)
            specs.append(base)
            for prop in plugin.relations(base):
                if prop.spec is not None:
                    specs.append(plugin.derive(prop.spec))
    th_min = {"bulk": 1, "pay": 1, "undo": 1, "recent": 1}
    n_codes = n_codes3 = 0
    for s in specs:
        v, st = s.env(), s.structure
        now = v.get("NOW")                                  # shown only when a rule reads it or as the distractor
        if now is not None:
            assert now.second == 0 and now.microsecond == 0                                        # B1, B3
            assert int(now.utcoffset().total_seconds() // 60) in P.OFFSETS                         # B5
        if v.get("LAST_EDIT") is not None:
            assert v["LAST_EDIT"].second == 0 and v["LAST_EDIT"] <= now                            # B1, B2
            assert v["ELAPSED"] * 60 == (now - v["LAST_EDIT"]).total_seconds()                     # exact minutes
        if st["hours"] is not None:
            a, b, _ = st["hours"]
            assert 0 <= a < b <= 1439                                                               # B17
        for r in st["rules"]:
            assert "off_hours" not in r["atoms"] or r["atoms"] == ["off_hours"]                     # B17
        missing = plugin._missing(s)
        assert set(missing) <= set(P.MISSABLE) and len(missing) <= 1                                # B9
        if "AMOUNT" in s.slots and v["EFFECT"] != "pay":
            assert v["AMOUNT"] == 0                                                                 # B7
        if "DEST_DOMAIN" in s.slots and v["EFFECT"] not in P.OUTBOUND:
            assert v["DEST_DOMAIN"] == v["ORG_DOMAIN"]                                              # B7
        if "AMOUNT" in missing:
            assert v["EFFECT"] == "pay"
        if "DEST_DOMAIN" in missing:
            assert v["EFFECT"] in P.OUTBOUND
        ths = {}
        for r in st["rules"]:
            for a in r["atoms"]:
                if a in P.THRESHOLD_ATOMS:
                    t = v[P._th_names(a, r["tier"])[0]]
                    assert t >= th_min[a]                                                           # B14
                    ths[(a, r["tier"])] = t
        for a in ("bulk", "pay"):
            if (a, "forbid") in ths and (a, "confirm") in ths:
                assert ths[(a, "forbid")] > ths[(a, "confirm")]                                     # B16
        for a in ("undo", "recent"):
            if (a, "forbid") in ths and (a, "confirm") in ths:
                assert ths[(a, "forbid")] < ths[(a, "confirm")]                                     # B16
        gold = plugin.solve_a(s)
        offered = s.qform == "ch_verdict" and (st["show_abstain"] or gold == "cannot")
        if missing and not offered:
            assert gold != "cannot"                                                                 # B10
        if s.sampler in ("S1", "S2") and s.qform in ("ch_verdict", "yn_go"):
            rr = plugin.render(s, ctx)
            card = CARDS.split_rules(rr.row)[0]                                                      # G0 v1.2 S13
            assert ("Missing data: " in card) == (plugin._card_missing(s) or offered)                          # B23
            if st["codes"]:
                legend = [ln for ln in card.split("\n") if ln.startswith("Answer codes: ")]
                assert len(legend) == 1
                codes = [c.split(" = ")[0] for c in legend[0][len("Answer codes: "):-1].split(", ")]
                assert sorted(codes) == sorted(rr.row["options"])                                   # B23
                n_codes += 1
                n_codes3 += len(codes) == 3
    assert "Ops" not in plugin.NAME_ALLOW                                                           # B27
    assert set(P.ERROR_NAMES) - {n for n in P.ERROR_NAMES if n.startswith("t29_")} == {
        "first_match", "add_exclusive_endpoint", "drop_inclusive_endpoint", "skip_offset_conversion"}
    assert all(n in D.CATALOG for n in P.ERROR_NAMES)                                               # B28
    assert n_codes > 20 and 0 < n_codes3 < n_codes                                                  # both legends
    assert plugin.G0_AMBIGUITY_PASS["resolved"] == plugin.G0_AMBIGUITY_PASS["points"] == 30


def test_requested_effect_class_is_independent_of_the_gold(plugin):
    """A45 b (T29 iteration 4): the requested candidate's position and effect class are seed-only draws and the sub-seed
    loop realises the gold on it, so the effect class the question names says nothing about the verdict (before: change ->
    go 55% against 27% pooled; delete -> ask 44%). P(effect | verdict) stays at the effect prior within 4 standard errors,
    and every effect class occurs for every verdict; the card-side effects (the candidates' lines) are unchanged."""
    specs = [plugin.sample(seed, smp) for seed in range(700) for smp in TRAIN]
    rows = [(plugin._verdict_c(plugin._rule_truths(s), plugin._confirmed_c(s)), s.env()["EFFECT"]) for s in specs]
    prior = collections.Counter(e for _, e in rows)
    for v in ("go", "ask", "refuse"):
        sub = [e for vv, e in rows if vv == v]
        c = collections.Counter(sub)
        assert set(c) == set(P.EFFECTS), (v, c)
        for e in P.EFFECTS:
            p0 = prior[e] / len(rows)
            se = (p0 * (1 - p0) / len(sub)) ** 0.5
            assert abs(c[e] / len(sub) - p0) <= 4 * se, (v, e, round(c[e] / len(sub), 3), round(p0, 3))
    for s in specs[:200]:                                        # the requested index is the seed-only draw
        n = s.structure["cands"]
        assert s.structure["req"] == min(n - 1, int(P.uhash(P.FAMILY, "reqidx", s.sampler, s.seed) * n))
