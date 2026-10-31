"""c2_build/families/T07/test_plugin.py: in-memory tests for the T07 plugin (no file is written: A37 f).

Covers: the plugin contract (strict); solver A = solver B and parse = canonical on >= 5,000 sampled specs; Mode F rows
(the fact-lock, the re-derived template, the lexicon scan, G3-H fields); every relation unit through the kit gates;
twins that differ in exactly one slot (one parsed fact) and flip as constructed; complements with opposite gold;
metamorphic relations; balance by construction on 2,000 specs (per form, per wording, yes = bad, controls); trap,
overlay and length targets of G0 section 2; G-SL on the built-in placeholder skins and on the program templates;
determinism by seed; the boundary semantics of every condition in both solvers; and injected bugs that G2 / G3 / G-TW /
G-LEX must catch.

Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T07
"""
from __future__ import annotations

import collections
import dataclasses
import datetime as dt
import re
import statistics
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import g3h, gsl, pipeline  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.paths import never_open  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from families.T07 import fixtures as FX  # noqa: E402
from families.T07 import plugin as P  # noqa: E402
from families.T07 import solver_b as B  # noqa: E402

import negcount  # noqa: E402  (c_src/common, on sys.path through c2_kit.paths)

TRAIN = ("S1", "S2", "S3", "S4")
YN = ("yn_gets", "yn_dneg_gets", "yn_misses", "yn_not_gets", "yn_fails_to")


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T07Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def base_specs(plugin):
    """2,000 base specs: seeds 0-499 of each training sampler."""
    return [plugin.sample(seed, smp) for smp in TRAIN for seed in range(500)]


@pytest.fixture(scope="module")
def units(plugin, ctx, base_specs):
    """Every base spec (+ 200 S5 specs) through pipeline.build_unit (G2, G3, G4, G-SL, G-LEX, G-TW, schema)."""
    out = [pipeline.build_unit(plugin, s, ctx, run_g15=False) for s in base_specs]
    return out + [pipeline.build_unit(plugin, plugin.sample(seed, "S5"), ctx, run_g15=False) for seed in range(200)]


def _facts(view: dict) -> dict:
    """A parsed view flattened to one entry per fact (twin pair checks)."""
    out = {f"record.{k}": v for k, v in view["record"].items()}
    for mark, conds in view["footnotes"]:
        for i, (sem, bound) in enumerate(conds):
            out[f"footnote{mark}.{i}"] = (sem, bound)
    for k in ("qform", "store", "customer", "order_id", "item", "asked"):
        out[k] = view[k]
    out["ladder"] = tuple(view["ladder"])
    out["headlines"] = tuple(tuple(h) for h in view["headlines"])
    return out


# ------------------------------------------------------------------------------------------------ contract

def test_plugin_meets_the_strict_contract(plugin):
    assert KP.validate_plugin(plugin, strict=True) == []
    assert KP.check_independence(plugin) == []
    assert plugin.PARADIGM_A != plugin.PARADIGM_B
    assert len(P.T07Plugin.G0_LITE.read_text(encoding="utf-8").splitlines()) <= 200          # G0 v2 (14 Oct 2026)


def test_fixture_lexicon_is_admitted_and_unambiguous(ctx):
    reg = ctx.lexicon
    assert reg.gate()["pass"], reg.gate()
    assert all(f.unit_ok for f in reg.forms.values()), {k: f.unit_problems for k, f in reg.forms.items()
                                                         if not f.unit_ok}
    for sem in P.SEMS:                                          # G4 paraphrase needs a second admitted form
        assert sum(1 for f in reg.forms.values() if f.sem_id == sem) >= 2, sem
    for qf in P.T07Plugin.QFORMS:
        for held in (False, True):
            assert any(s.kind == "wording" and s.qform == qf and s.held_out == held for s in ctx.skins.values())
    assert set(B.SEM) == set(P.SEMS)


def test_this_package_opens_no_never_open_path():
    for f in P.HERE.iterdir():
        assert never_open(f) is None, f


def test_closed_sets_agree_and_surfaces_are_unique():
    pairs = ((P.HEADLINES, B.HEADLINES), (P.BENEFITS, B.BENEFITS), (P.REGIONS, B.REGIONS),
             (P.CATEGORIES, B.CATEGORIES), (P.STATUSES, B.STATUSES), (P.TIERS, B.TIERS))
    for a, b in pairs:
        assert a == b
    surfaces = [s.casefold() for t, _ in pairs for v in t.values() for s in v]
    keys = [k for t, _ in pairs[2:] for k in t] + list(P.HEADLINES)
    assert len(set(surfaces)) == len(surfaces) and len(set(keys)) == len(keys)


# ------------------------------------------------------------------------------------------------ G2 / G3

def test_solver_a_equals_solver_b_on_5000_specs(plugin, ctx):
    n, golds, modes = 0, collections.Counter(), collections.Counter()
    for smp in plugin.SAMPLERS:
        for seed in range(1250 if smp != "S5" else 250):
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            view = plugin.parse(rr.row, ctx)
            a = plugin.solve_a(spec)
            assert plugin.solve_b(view) == a, (smp, seed, spec.qform)
            assert {k: v for k, v in view.items() if k != "options"} == plugin.canonical(spec), (smp, seed)
            if rr.row["qtype"] == "choice":
                assert view["options"][rr.row["options"].index(rr.row["gold"])] == a
            assert pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False) == [], (smp, seed)
            golds[(spec.qform, a if not isinstance(a, str) else a.split(":")[0])] += 1
            modes[rr.row["meta"]["c2"]["author_mode"]] += 1
            n += 1
    assert n >= 5000
    assert {a for (q, a) in golds if q == "ch_failing"} == set(P.DIMS) | {"none"}
    assert {a for (q, a) in golds if q == "ch_offers"} == {"both", "only", "neither"}
    assert all(golds[(q, 0)] and golds[(q, 1)] for q in YN)
    assert modes["T"] and modes["F"]


def _mode_f_specs(plugin, skin, want=3, limit=40000):
    samplers = ("S5",) if skin.held_out else TRAIN
    out = []
    for seed in range(limit):
        for smp in samplers:
            spec = plugin.sample(seed, smp)
            if plugin.compatible(skin, spec):
                out.append(spec)
        if len(out) >= want:
            break
    return out


def test_mode_f_rows_pass_the_fact_lock_and_both_solvers(plugin, ctx):
    free = [s for s in ctx.skins.values() if s.author_mode == "F"]
    assert len(free) >= 4
    for sk in free:
        specs = _mode_f_specs(plugin, sk)
        assert len(specs) >= 3, sk.skin_id
        for spec in specs:
            rr = plugin.render(spec, ctx, skin=sk)
            assert "Fine print" not in rr.row["state"]                     # the fine print lives in the free text
            assert pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False) == [], sk.skin_id
            view = B.parse(rr.row, ctx)
            assert B.solve_b(view) == plugin.solve_a(spec)
            res = pipeline.build_unit(plugin, spec, ctx, run_g15=False, skin=sk)
            assert res.ok, (sk.skin_id, res.problems[:3])
            fields = plugin.extract_fields(spec)                            # G3-H: a perfect extraction passes,
            truth = plugin.extract_view(spec)                               # a wrong rule is caught
            ok, diffs = g3h.compare(truth, _as_written(truth, fields), fields)
            assert ok, diffs
            bad = dict(_as_written(truth, fields))
            dim = spec.structure["promises"][0]["conds"][0][0]
            bad[f"{dim}_rule"] = "absent"
            assert g3h.compare(truth, bad, fields)[0] is False
            assert g3h.extraction_item(rr.row["state"], fields)["schema"]


def _as_written(truth: dict, fields: list) -> dict:
    """An extractor's answer: values as text (dates ISO, amounts in dollars), rules as enum choices."""
    out = {}
    for f in fields:
        v = truth[f.name]
        if v is None or f.kind in ("enum", "name", "category"):
            out[f.name] = v
        elif f.kind == "date":
            out[f.name] = v
        else:
            out[f.name] = S.render(S.cents_slot(v), "symbol")
    return out


def test_g15_loader_round_trip_on_a_sample(plugin, ctx):
    for smp in plugin.SAMPLERS:
        for seed in range(4):
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=True)
            assert res.ok, (smp, seed, res.problems)


# ------------------------------------------------------------------------------------------------ relations

def test_every_unit_passes_every_program_gate(units):
    bad = [(u.rendered[0].row["meta"]["sampler"] if u.rendered else None, u.problems[:2]) for u in units if not u.ok]
    assert not bad, bad[:5]


def test_overlay_shares_meet_spec_4_1(plugin, units):
    rep = pipeline.overlay_report(units[:2000], plugin)
    assert rep["complement_share_of_yes_no"] >= 0.20
    assert rep["non_syntactic_share_of_pairs"] >= 0.30
    assert 0.20 <= rep["twin_share"] <= 0.25, rep["twin_share"]
    assert 0.05 <= rep["equiv_share"] <= 0.10, rep["equiv_share"]
    assert 0.02 <= rep["attack_share"] <= 0.06, rep["attack_share"]
    assert abs(rep["yes_rate"] - 0.5) <= 0.03
    assert rep["abstain"]["pass"] and rep["abstain"]["wrong_share"] >= 0.5
    chi2_01 = {1: 6.63, 2: 9.21, 3: 11.34, 4: 13.28, 5: 15.09, 6: 16.81, 7: 18.48, 8: 20.09}
    for k, counts in rep["gold_positions"].items():          # G10: gold position uniform per bucket (p > 0.01)
        mean = sum(counts) / k
        assert sum((c - mean) ** 2 / mean for c in counts) < chi2_01[k - 1], (k, counts)
    rows = [r for u in units for r in u.rows]
    assert max(collections.Counter(r["call_id"] for r in rows).values()) <= 3
    yn = [r for r in rows if r["qtype"] == "noul"]
    assert 0.45 <= len(yn) / len(rows) <= 0.55


def test_twins_differ_in_one_slot_and_flip_as_constructed(plugin, ctx, base_specs):
    seen = collections.Counter()
    for spec in base_specs:
        for prop in plugin.relations(spec):
            if prop.kind != "twin":
                continue
            twin = plugin.derive(prop.spec)
            assert slot_diff(spec, twin) == {prop.changed_slot}
            a, b = plugin.solve_a(spec), plugin.solve_a(twin)
            assert b == prop.expect and a != b, (spec.sampler, spec.seed, prop.note)
            rr = plugin.render(spec, ctx)
            key = f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"
            forms = pipeline._forms_for(twin, rr.forms, key, {prop.changed_slot})       # as build_unit does
            rt = plugin.render(twin, ctx, skin=ctx.skin(rr.skin_id), wording=ctx.skin(rr.wording_id), forms=forms)
            va, vb = B.parse(rr.row, ctx), B.parse(rt.row, ctx)
            fa, fb = _facts(va), _facts(vb)
            assert len([k for k in fa if fa[k] != fb[k]]) == 1                     # solver B sees one fact move
            assert (B.solve_b(va), B.solve_b(vb)) == (a, b)
            seen[prop.note] += 1
    assert {n.split(":")[0] for n in seen} == set(P.DIMS), seen
    assert {n.split(":")[1] for n in seen} == {"attr", "bound"}
    assert sum(seen.values()) >= 600


def test_complements_have_opposite_gold_and_one_predicate(plugin, units):
    pairs, kinds = 0, collections.Counter()
    for u in units:
        by_id = {r["id"]: r for r in u.rows}
        for rel in u.rels:
            if rel["type"] != "complement":
                continue
            a, b = by_id[rel["a"]], by_id[rel["b"]]
            qa, qb = plugin.QFORMS[a["meta"]["qform"]], plugin.QFORMS[b["meta"]["qform"]]
            assert a["gold"] + b["gold"] == 1 and qa.predicate == qb.predicate and qa.polarity != qb.polarity
            assert a["state"] == b["state"]
            assert P.CLOSED_WORLD in a["instructions"] and P.CLOSED_WORLD in b["instructions"]
            kinds[(qa if qa.polarity == -1 else qb).complement_kind] += 1
            pairs += 1
    assert pairs >= 300
    assert set(kinds) == {"antonym", "syntactic", "implicit"}


def test_metamorphic_relations_hold_in_both_solvers(plugin, ctx, base_specs):
    notes = collections.Counter()
    for spec in base_specs[:800]:
        for prop in plugin.relations(spec):
            if prop.kind != "metamorphic":
                continue
            m = plugin.derive(prop.spec)
            assert plugin.solve_a(m) == plugin.solve_a(spec), prop.note
            rr = plugin.render(m, ctx)
            assert B.solve_b(B.parse(rr.row, ctx)) == plugin.solve_a(spec), prop.note
            notes[prop.note] += 1
    assert len(notes) >= 5, notes


# ------------------------------------------------------------------------------------------------ balance and traps

def test_gold_balance_on_2000_specs(plugin, ctx, base_specs, units):
    yn = [s for s in base_specs if s.qform in YN]
    assert abs(len(yn) / len(base_specs) - 0.45) <= 0.02              # base share; rows are checked in the overlay
    for qf in YN:
        xs = [plugin.solve_a(s) for s in yn if s.qform == qf]
        assert sum(xs) * 2 == len(xs), qf                         # antithetic pairs: exactly half yes
    by_wording = collections.defaultdict(list)
    for s in yn:
        by_wording[plugin.render(s, ctx).wording_id].append(plugin.solve_a(s))
    for w, xs in by_wording.items():
        assert abs(sum(xs) / len(xs) - 0.5) <= 0.02, w            # pairs share their wording
    bad = sum(1 for s in yn if plugin.QFORMS[s.qform].yes_is_bad) / len(yn)
    assert 0.45 <= bad <= 0.55
    rows = [r for u in units[:2000] for r in u.rows if r["qtype"] == "noul"]            # with their partners
    assert 0.45 <= sum(plugin.QFORMS[r["meta"]["qform"]].yes_is_bad for r in rows) / len(rows) <= 0.55
    cells = collections.defaultdict(lambda: [0, 0])                      # G0 v2 S17: "None" is gold on 1/k per k-cell
    for s in base_specs:
        if s.qform == "ch_failing":
            k = len(P.failing_dims(s.structure)) + 1
            cells[k][0] += 1
            cells[k][1] += plugin.solve_a(s) == "none"
    assert set(cells) >= {2, 3, 4}
    for k, (n_k, a_k) in cells.items():
        assert abs(a_k - n_k / k) <= 4, (k, n_k, a_k)                     # strata of k rows: +/- 1 per sampler and cell
    co = collections.Counter(plugin.solve_a(s).split(":")[0] for s in base_specs if s.qform == "ch_offers")
    n = sum(co.values())
    assert 0.20 <= co["both"] / n <= 0.30 and 0.20 <= co["neither"] / n <= 0.30

    def control(s):
        a = plugin.solve_a(s)
        return a == "both" if s.qform == "ch_offers" else (a == "none" if s.qform == "ch_failing"
                                                            else bool(a) == P.YES_MEANS_GETS[s.qform])
    assert 0.30 <= sum(control(s) for s in base_specs) / len(base_specs) <= 0.40      # spec 3.16 controls 35%


def test_pairs_are_antithetic_and_cards_mirrored(plugin):
    for smp in TRAIN:
        for k in range(300):
            a, b = plugin.sample(2 * k, smp), plugin.sample(2 * k + 1, smp)
            assert a.qform == b.qform and a.structure == b.structure and a.pack == b.pack
            ca, cb = int(a.card_id[-2:]), int(b.card_id[-2:])
            assert ca + cb == P.N_CARDS[smp] - 1
            if a.qform in YN:
                gets = [plugin.solve_a(x) == int(P.YES_MEANS_GETS[x.qform]) for x in (a, b)]
                assert sum(gets) == 1
    rates = [P.card_rate(c, 16) for c in range(16)]
    assert min(rates) >= 0.2 and max(rates) <= 0.8 and abs(statistics.mean(rates) - 0.5) < 1e-9


def test_trap_shares_meet_g0_targets(units, base_specs):
    rows = [r for u in units[:2000] for r in u.rows]
    edge = collections.Counter(e for r in rows for e in r["meta"]["edge"])
    share = {k: v / len(rows) for k, v in edge.items()}
    assert 0.55 <= share["fine_print_later"] <= 0.80, share["fine_print_later"]
    assert share["time_bound_ends_on_order_date"] >= 0.05
    assert 0.40 <= share["two_headlines"] <= 0.65
    assert share["shared_dim"] >= 0.15
    assert share["date_edge"] >= 0.05 and share["spend_edge"] >= 0.05 and share["spend_near"] >= 0.05
    assert share["exclusion"] >= 0.30
    assert sum(s.deep for s in base_specs) / len(base_specs) <= 0.10


def test_bounds_alone_never_hint_at_the_outcome(plugin):
    """Label-blindness of the value draw (G0 S21): per dimension, guessing a condition's outcome from its bound value
    alone does no better than the prior (bounds are drawn before the record value)."""
    tab = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for smp in TRAIN:
        for seed in range(1500):
            s = plugin.sample(seed, smp)
            v = s.env()
            for c in plugin._conds(s):
                b = v[c[3]]
                key = b.month if c[2] == "date" else b
                tab[c[2]][key][plugin.cond_pass(s, c)] += 1
    for dim, by_bound in tab.items():
        n = sum(sum(x.values()) for x in by_bound.values())
        prior = max(sum(x[True] for x in by_bound.values()), sum(x[False] for x in by_bound.values())) / n
        acc = sum(max(x.values()) for x in by_bound.values()) / n
        assert acc <= prior + 0.02, (dim, acc, prior)


def test_negation_quotas_on_yes_no_rows(units):
    yn = [r for u in units[:2000] for r in u.rows if r["qtype"] == "noul"]
    k = [negcount.count(r["instructions"].split("\n\n")[-1]).k_syn for r in yn]
    assert sum(1 for x in k if x >= 1) / len(yn) >= 0.10
    assert sum(1 for x in k if x >= 2) / len(yn) >= 0.02


def test_construction_invariants(plugin, base_specs):
    for s in base_specs:
        v, stc = s.env(), s.structure
        ladder = [v[t] for t in stc["ladder"]]
        for p, i, dim, bslot, cslot, sem in plugin._conds(s):
            assert P.SEMS[sem][0] == dim and "{" + bslot in s.slots[cslot].value[2]
            if dim == "tier":                                          # "and above" never names the lowest level,
                r = ladder.index(v[bslot])                               # "and below" never the highest
                assert r >= 1 if P.SEMS[sem][1] == "min" else r <= len(ladder) - 2
            if dim == "status":
                assert v[bslot] != "regular_price"
            if dim == "spend":
                assert v[bslot] in P.SPEND_GRID
        dims = [[c[0] for c in pr["conds"]] for pr in stc["promises"]]
        assert all(len(set(d)) == len(d) for d in dims)                  # one condition per dimension per footnote
        if s.qform == "ch_failing":
            fails = [c for c in plugin._conds(s) if c[0] == stc["asked"] and not plugin.cond_pass(s, c)]
            assert len(fails) <= 1
        assert (s.qform == "ch_offers") == (stc["asked"] is None) and ("ASKED" in s.slots) == (stc["asked"] is not None)


def test_lengths(units):
    rows = [r for u in units for r in u.rows]
    toks = [R.approx_tokens(r) for r in rows]
    assert max(toks) <= R.MAX_TOKENS
    assert statistics.mean(t * R.CHARS_PER_TOKEN / 4 for t in toks) <= 800      # ~4 characters per real token


def test_boundary_semantics_of_every_condition_in_both_solvers(plugin, base_specs):
    """Each condition at, one unit inside and one unit outside its bound, read by solver A (AST), the construction
    view and solver B's admitted set."""
    d0, one = dt.date(2026, 5, 10), dt.timedelta(days=1)
    cases = {"t07.date.le": [(d0, True), (d0 - one, True), (d0 + one, False)],
             "t07.date.lt": [(d0, False), (d0 - one, True), (d0 + one, False)],
             "t07.date.ge": [(d0, True), (d0 - one, False), (d0 + one, True)],
             "t07.spend.ge": [(5000, True), (4999, False), (5001, True)],
             "t07.spend.gt": [(5000, False), (4999, False), (5001, True)]}
    base = next(s for s in base_specs if s.qform == "yn_gets" and len(s.structure["promises"]) == 1
                and len(s.structure["promises"][0]["conds"]) == 1 and s.structure["promises"][0]["conds"][0][0]
                in ("date", "spend"))
    dim, bslot, cslot = base.structure["promises"][0]["conds"][0]
    for sem, rows in cases.items():
        d = P.SEMS[sem][0]
        stc = {**base.structure, "promises": [{**base.structure["promises"][0],
                                               "conds": [[d, f"P1_{d.upper()}", f"P1_Q_{d.upper()}"]]}]}
        slots = {k: v for k, v in base.slots.items() if k not in (bslot, cslot)}
        fid = plugin._form_ids(sem, "S1")[0]
        slots[f"P1_Q_{d.upper()}"] = plugin.lexicon.clause(fid, bind={"X": f"P1_{d.upper()}"})
        slots[f"P1_{d.upper()}"] = S.date_slot(d0) if d == "date" else S.cents_slot(5000)
        for value, passes in rows:
            attr = S.date_slot(value) if d == "date" else S.cents_slot(value)
            s = base.replace(structure=stc, slots={**slots, P.ATTR[d]: attr})
            assert plugin.solve_a(s) == int(passes), (sem, value)
            assert plugin.cond_pass(s, plugin._conds(s)[0]) == passes
            bound = d0.isoformat() if d == "date" else 5000
            point = value.toordinal() if d == "date" else value
            assert B._contains(B._admits(sem, bound, []), point) == passes, (sem, value)
    ladder = ["green", "blue", "black"]
    for cust, up, down in (("blue", True, True), ("black", True, False), ("green", False, True)):
        assert B._contains(B._admits("t07.tier.min", "blue", ladder), ladder.index(cust)) == up
        assert B._contains(B._admits("t07.tier.max", "blue", ladder), ladder.index(cust)) == down
    for sem, x, passes in (("t07.region.in", "arvale", True), ("t07.region.in", "hollin", False),
                           ("t07.region.out", "arvale", False), ("t07.region.out", "hollin", True)):
        assert B._contains(B._admits(sem, "arvale", []), x) == passes
    assert B._meet(("iv", None, 9), ("iv", 3, None)) == ("iv", 3, 9)
    assert B._meet(("set", False, frozenset({"a"})), ("set", True, frozenset({"a", "b"}))) == ("set", True,
                                                                                               frozenset({"b"}))


# ------------------------------------------------------------------------------------------------ G-SL

LIT_FORBIDDEN = re.compile(r"\d|\$|%|\b(?:" + "|".join(S.MONTHS + S.WEEKDAYS) + r")\b")


def test_builtin_placeholder_skins_pass_gsl(plugin, ctx):
    for sk in ctx.skins.values():
        if sk.author_mode == "T":
            v = gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                                  name_allow=plugin.NAME_ALLOW)
            assert v == [], (sk.skin_id, v)
        if sk.kind == "skin" and sk.author_mode == "T":
            assert set(sk.decl) == {"STORE"}, sk.skin_id                       # G0 S14: Mode T skins hold no fact
            lit = re.sub(r"\{[^{}]*\}", " ", sk.text)
            assert not LIT_FORBIDDEN.search(lit), sk.skin_id
            words = set(re.findall(r"[a-z]+", lit.lower()))
            assert not words & {"only", "excludes", "excluded", "valid", "members", "minimum", "before", "after",
                                "over", "qualify", "eligible", "free"}, sk.skin_id
        if sk.author_mode == "F":
            lit = sk.text
            for _name, val in sk.brief:
                lit = lit.replace(val, " ")
            assert not LIT_FORBIDDEN.search(lit), sk.skin_id
            assert set(sk.decl) - {"STORE"} and sk.lexicon_ids, sk.skin_id
    for sk in ctx.skins.values():                                      # Mode F only in the free-form registers
        if sk.author_mode == "F":
            assert sk.register not in P.EQUIV_REGISTERS + P.EQUIV_REGISTERS_HELD


def test_program_templates_hold_no_literal_values(plugin):
    stc = {"ladder": ["TL0", "TL1", "TL2"], "promises": [], "foot_order": [], "layout": "near"}
    texts = [plugin._card_tpl(stc), plugin._card_tpl({**stc, "card": "short"}), P.BANNER_HEAD, P.RECORD_JSON_HEAD,
             P.RECORD_JSON_BODY, P.ATTACK_PREFIX,
             *P.RECORD_TPL.values(), *P.TERMS_HEAD.values(), *P.DIM_TEXT.values(), P.NONE_TEXT, P.OFFER_BOTH,
             P.OFFER_NEITHER]
    for t in texts:
        lit = re.sub(r"\{[A-Z][A-Z0-9_]*\}", " ", t)
        assert not LIT_FORBIDDEN.search(lit), t
        assert not set(re.findall(r"[a-z]+", lit.lower())) & {"qualify", "eligible", "entitled"}, t


def test_gsl_catches_a_leaky_skin_and_a_leaky_free_text(plugin, ctx):
    base = ctx.skin("SK-SMS-1")
    spec = next(s for s in (plugin.sample(i, "S1") for i in range(50)) if plugin.compatible(base, s))
    for extra in (" Only members save.", " Ends 5 March.", " You are eligible.", " Not for clearance."):
        leaky = dataclasses.replace(base, skin_id="SK-LEAK", text=base.text + extra)
        c2 = dataclasses.replace(ctx, skins={**ctx.skins, "SK-LEAK": leaky})
        probs = pipeline.check_rendered(plugin, spec, plugin.render(spec, c2, skin=leaky), c2, run_g15=False)
        assert any(g == "G-SL" for g, _ in probs), extra
    free = ctx.skin("SK-FREE-SMS-1")
    fspec = _mode_f_specs(plugin, free, want=1)[0]
    for extra in (" Offer not valid online.", " Limit 2 per customer."):
        leaky = dataclasses.replace(free, skin_id="SK-LEAK-F", text=free.text + extra)
        c2 = dataclasses.replace(ctx, skins={**ctx.skins, "SK-LEAK-F": leaky})
        probs = pipeline.check_rendered(plugin, fspec, plugin.render(fspec, c2, skin=leaky), c2, run_g15=False)
        assert any(g == "G-SL" for g, _ in probs), extra


# ------------------------------------------------------------------------------------------------ determinism

def test_generation_is_deterministic_by_seed(plugin, ctx):
    for smp in plugin.SAMPLERS:
        a, b = plugin.sample(41, smp), plugin.sample(41, smp)
        assert a.structure_hash() == b.structure_hash() and a.tags == b.tags
        ra = pipeline.build_unit(plugin, a, ctx, run_g15=False).rows
        rb = pipeline.build_unit(plugin, b, ctx, run_g15=False).rows
        assert ra == rb
    assert len({plugin.sample(s, "S1").structure_hash() for s in range(200)}) == 200
    assert plugin.sample(7, "S1").structure_hash() != plugin.sample(7, "S2").structure_hash()


def test_s5_rows_are_dev_only(units):
    s5 = [r for u in units[2000:] for r in u.rows]
    assert s5 and all(r["meta"]["dev_only"] for r in s5)
    assert all(R.validate_row(r, training=True) for r in s5)
    assert all(not r["meta"]["dev_only"] for u in units[:200] for r in u.rows)


# ------------------------------------------------------------------------------------------------ error models

def test_wrong_options_come_from_named_error_models(plugin, ctx, base_specs):
    produced, named, wrong = collections.Counter(), collections.Counter(), collections.Counter()
    for spec in base_specs:
        if spec.qform not in ("ch_failing", "ch_offers"):
            continue
        rr = plugin.render(spec, ctx)
        for o in rr.option_set.options:
            if o.role == "gold":
                continue
            kind = "none" if o.key == "none" else spec.qform
            wrong[kind] += 1
            named[kind] += bool(o.err)
            produced.update(o.err)
        assert set(rr.row["meta"]["opt_err"]) == set(rr.row["options"]) - {rr.row["gold"]}
    assert set(produced) == set(P.EM_VARIANTS), set(P.EM_VARIANTS) - set(produced)    # every model is exercised
    assert named["none"] == wrong["none"]                                             # a wrong "None" is named
    assert named["ch_offers"] / wrong["ch_offers"] >= 0.75
    assert named["ch_failing"] / wrong["ch_failing"] >= 0.45      # closed-set labels (G0 S17; open issue)


def test_error_models_are_one_rule_swaps(plugin, base_specs):
    models = plugin.error_models()
    for spec in base_specs[:600]:
        if spec.qform == "ch_failing":
            assert models["ignore_qualifier"].fn(spec) == "none"
            if len(spec.structure["promises"]) == 1:
                assert models["t07_wrong_footnote"].fn(spec) is None
        if spec.qform == "ch_offers":
            assert models["ignore_qualifier"].fn(spec) == "both"
        if spec.qform in YN:
            assert all(m.fn(spec) is None for m in models.values())


# ------------------------------------------------------------------------------------------------ injected bugs

def _gate_failures(plugin, ctx, n=200, units_too=False):
    out = collections.Counter()
    for smp in TRAIN:
        for seed in range(n // 4):
            spec = plugin.sample(seed, smp)
            if units_too:
                probs = pipeline.build_unit(plugin, spec, ctx, run_g15=False).problems
            else:
                try:
                    rr = plugin.render(spec, ctx)
                except pipeline.RENDER_ERRORS:              # build_unit drops such a unit as a render failure
                    out["render"] += 1
                    continue
                probs = pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False)
            for g, _ in probs:
                out[g] += 1
    return out


def test_g2_catches_a_solver_b_boundary_bug(plugin, ctx, monkeypatch):
    monkeypatch.setitem(B.SEM, "t07.spend.ge", ("spend", "above"))          # "or more" read as "over" in solver B
    assert _gate_failures(plugin, ctx, 800)["G2"] > 0


def test_g2_catches_a_solver_a_boundary_bug(plugin, ctx, monkeypatch):
    monkeypatch.setitem(P.A_OP, "le", "<")                                  # "on or before" read as "before" in A
    assert _gate_failures(plugin, ctx, 800)["G2"] > 0


def test_g2_catches_a_solver_b_set_algebra_bug(plugin, ctx, monkeypatch):
    real = B._meet
    monkeypatch.setattr(B, "_meet", lambda s, t: s if s[0] == "set" else real(s, t))
    monkeypatch.setitem(B.SEM, "t07.region.out", ("region", "member"))     # exclusion read as restriction
    assert _gate_failures(plugin, ctx, 400)["G2"] > 0


def test_g3_catches_a_record_that_prints_the_wrong_fact(plugin, ctx, monkeypatch):
    t = P.RECORD_TPL["lines"].replace("{CATEGORY}", "{@}").replace("{STATUS}", "{CATEGORY}").replace("{@}", "{STATUS}")
    monkeypatch.setitem(P.RECORD_TPL, "lines", t)
    assert _gate_failures(plugin, ctx, 200)["G3"] > 0


def test_g3_catches_a_card_that_misstates_the_rule(plugin, ctx, monkeypatch):
    monkeypatch.setattr(P, "CARD_TPL", P.CARD_TPL.replace(", and only then", ""))
    monkeypatch.setattr(P, "CARD_SHORT_TPL", P.CARD_SHORT_TPL.replace("exactly when", "when"))
    assert _gate_failures(plugin, ctx, 120)["G3"] > 0


def test_card_styles_are_label_blind(plugin, base_specs):
    short = [s for s in base_specs if s.structure["card"] == "short"]
    assert 0.10 <= len(short) / len(base_specs) <= 0.20
    yn = [s for s in short if s.qform in YN]
    assert abs(sum(plugin.solve_a(s) for s in yn) / len(yn) - 0.5) < 1e-9          # pairs share the card


def test_gtw_catches_a_wrong_twin_prediction(plugin, ctx, monkeypatch):
    real = P.T07Plugin._twin

    def wrong(self, spec):                                   # predicts the base answer (no flip): G-TW must refuse
        t = real(self, spec)
        return None if t is None else dataclasses.replace(t, expect=self.solve_a(spec))

    monkeypatch.setattr(P.T07Plugin, "_twin", wrong)
    assert _gate_failures(plugin, ctx, 200, units_too=True)["G-TW"] > 0


def test_glex_refuses_unadmitted_condition_wordings(plugin):
    raw = FX.ctx(admit=False)
    p = P.T07Plugin(lexicon=raw.lexicon)
    with pytest.raises(KP.ContractError):
        p.sample(1, "S1")                                    # sample() draws admitted forms only
    good = FX.ctx()
    spec = P.T07Plugin(lexicon=good.lexicon).sample(1, "S1")
    rr = P.T07Plugin(lexicon=good.lexicon).render(spec, good)
    assert any(g == "G-LEX" for g, _ in pipeline.lex_problems(spec, rr, raw))


# ------------------------------------------------------------------------------------------------ review fix: twin mix

def test_abstain_share_holds_on_every_emitted_row(plugin, ctx):
    """Minimal-edit twins mirror their base: fixing the one failing item of a base lands on the abstain key, so
    unthinned twins piled up there (38% of all emitted ch_failing rows against a G0 target of 25%). Twins onto the key
    are thinned (kit relations.abstain_twin_kept, 1/(k-1)^2 per k since G0 v2); P(gold | key shown) over ALL emitted rows
    (base, twin, equiv, inv) is within 5 pp of the mean 1/k."""
    shown = gold = 0
    chance = 0.0
    roles = collections.Counter()
    for seed in range(700):
        for smp in ("S1", "S2", "S3", "S4"):
            spec = plugin.sample(seed, smp)
            if spec.qform != "ch_failing":
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
    assert shown >= 300 and roles["twin"] >= 30, (shown, roles)
    assert abs(gold - chance) / shown <= 0.05, (gold / shown, chance / shown, roles)       # G0 v2 S17: 1/k per row


# ------------------------------------------------------------------------------------------------ G0 v1 (amb:T07)

def test_g0_v1_resolutions_hold_on_every_spec(plugin, base_specs):
    """H1 ASKED is a printed headline's benefit; H2 one ladder per row; H3 the customer holds a level of it; H5 one
    item; H6 no name holds a surface; H7 no regular-price record under a status condition; H39 dates in the window."""
    surfaces = {x.casefold() for t in (P.HEADLINES, P.BENEFITS, P.REGIONS, P.CATEGORIES, P.STATUSES, P.TIERS)
                for v in t.values() for x in v}
    lo, hi = P.DATE0, P.DATE0 + dt.timedelta(days=329)
    for s in base_specs + [plugin.sample(seed, "S5") for seed in range(200)]:
        v, stc = s.env(), s.structure
        heads = [v[pr["slot"]] for pr in stc["promises"]]
        if s.qform == "ch_offers":
            assert "ASKED" not in s.slots
        else:
            assert v["ASKED"] == heads[stc["asked"]]
        ladder = tuple(v[t] for t in stc["ladder"])
        assert ladder in P.LADDERS and v["TIER"] in ladder
        assert isinstance(plugin.canonical(s)["item"], str)
        assert P.DATE0 + dt.timedelta(days=40) <= v["ORDER_DATE"] <= P.DATE0 + dt.timedelta(days=289)
        for _p, _i, dim, bslot, _c, _sem in plugin._conds(s):
            if dim == "tier":
                assert v[bslot] in ladder
            if dim == "date":
                assert lo <= v[bslot] <= hi
            if dim == "status":
                assert v["STATUS"] != "regular_price" and v[bslot] != "regular_price"
    for name in P.STORES + P.STORES_HELD + P.CUSTOMERS + P.CUSTOMERS_HELD:
        assert not any(re.search(r"(?<![a-z])" + re.escape(x) + r"(?![a-z])", name.casefold()) for x in surfaces), name


def test_ch_failing_options_one_per_dimension_scoped_none(plugin, ctx, base_specs):
    """H15-H17: one option per dimension (asked dimensions all listed), the scoped None text, the order-subtotal label;
    solver B reads every option back to its key."""
    labels = collections.Counter()
    for s in base_specs:
        if s.qform != "ch_failing":
            continue
        rr = plugin.render(s, ctx)
        opts = rr.row["options"]
        keys = B.parse(rr.row, ctx)["options"]
        asked = [c[0] for c in s.structure["promises"][s.structure["asked"]]["conds"]]
        assert P.NONE_TEXT in opts and len(set(keys)) == len(keys) == len(opts) and set(asked) <= set(keys)
        labels.update(opts)
    assert labels["The order-subtotal condition"] and not labels["The minimum-spend condition"]
    assert P.NONE_TEXT == "None: the order meets every condition in the fine print for this offer"


def test_mode_f_star_run_rule_in_both_solvers(plugin, ctx):
    """H21, H26: a Mode F text holds one `*`, directly followed by its condition sentences. compatible() (solver A
    side) and solver B's parser refuse a second `*` and a condition sentence before the `*`."""
    import copy
    free = ctx.skin("SK-FREE-EMAIL-1")
    spec = _mode_f_specs(plugin, free, want=1)[0]
    rr = plugin.render(spec, ctx, skin=free)
    state = rr.row["state"]
    cases = ((free.text.replace("Hello from", "*Hello from"), state.replace("Hello from", "*Hello from")),
             (free.text.replace("*Valid on", "Valid on").replace("Delivery to", "*Delivery to"),
              state.replace("*Valid on", "Valid on").replace("Delivery to", "*Delivery to")))
    for text, new_state in cases:
        bad = dataclasses.replace(free, skin_id="SK-FREE-BAD", text=text)
        assert not P.T07Plugin(lexicon=ctx.lexicon).compatible(bad, spec)
        c2 = dataclasses.replace(ctx, skins={**ctx.skins, "SK-FREE-BAD": bad})
        row = copy.deepcopy(rr.row)
        row["state"] = new_state
        row["meta"]["c2"]["skin_id"] = "SK-FREE-BAD"
        with pytest.raises(B.ParseError):
            B.parse(row, c2)
    assert B.solve_b(B.parse(rr.row, ctx)) == plugin.solve_a(spec)


def test_g0_is_frozen_with_its_haiku_pass():
    amb = P.T07Plugin.G0_AMBIGUITY_PASS
    assert amb["task_id"] == "c2-data-stage-a/amb:T07" and amb["points"] == amb["resolved"] == 47
    text = P.HERE.joinpath("G0_SPEC.md").read_text(encoding="utf-8")
    assert "FROZEN v1" in text and all(re.search(rf"\bH{i}\b", text) for i in range(1, 48))
