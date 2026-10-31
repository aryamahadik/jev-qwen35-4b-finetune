"""transfer/T21/test_fix_i1.py: tests for pilot fix iteration 1 (PILOT_VERDICT FIX-1 to FIX-8; G0_SPEC.md v1.3). In memory only
(A37 f); the frozen pools_v2/ are read, never written. No Haiku, no model.

  FIX-1   polarity screen + quarantine record + the i1 wording lint (only the contracted wording is refused)
  FIX-2   role-blind clause ids (one section, one minor set, equal option lengths)
  FIX-3/4 base form and twin shares; twin rows are 50% capped; the cap clause is gold 1/k on choice rows
  FIX-5   sampler schedule (S4 at 0.85) and the pilot wrapper
  FIX-6   the double-negation form (drawn only once a clean wording exists)
  FIX-7   card placement (yes/no row.card, choice rules close the state) and the two styles
  FIX-8   skeleton first: nothing visible predicts capped; no single-clause card; meta.depth is the chain length
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/transfer/T21/test_fix_i1.py
"""
from __future__ import annotations

import collections
import os
import subprocess
import sys
import types
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import cards as KC  # noqa: E402
from c2_kit import pipeline  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from transfer.T21 import authoring_i1 as AI  # noqa: E402
from transfer.T21 import card as CARD_MOD  # noqa: E402
from transfer.T21 import fixtures as FX  # noqa: E402
from transfer.T21 import freeze_v2 as FV  # noqa: E402
from transfer.T21 import haiku_author as HA  # noqa: E402
from transfer.T21 import plugin as P  # noqa: E402
from transfer.T21 import run_pilot_i1 as RUN  # noqa: E402
from transfer.T21 import solver_b as B  # noqa: E402
import negcount  # noqa: E402  (c_src/common, put on sys.path by c2_kit.paths)

TRAIN = ("S1", "S2", "S3", "S4")
CONTRACTED = "T21-WD-yn_not_capped-10e86065"
QUARANTINED = (CONTRACTED, "T21-SK-contract_ticket.006", "T21-MF-claims_log.003")


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T21Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def pools():
    return FV.load_pools()


def seeds(smp: str, n: int, base: int = 900_000):
    return range(base, base + n)


@pytest.fixture(scope="module")
def specs(plugin):
    return {smp: [plugin.sample(s, smp) for s in seeds(smp, 1200)] for smp in TRAIN}


@pytest.fixture(scope="module")
def units(plugin, ctx):
    out = []
    for smp in TRAIN:
        for s in seeds(smp, 90):
            out.append(pipeline.build_unit(plugin, plugin.sample(s, smp), ctx, run_g15=(s % 15 == 0)))
    return out


def _yes_no(specs):
    return [s for v in specs.values() for s in v if s.qform != P.CHOICE_FORM]


def _choice(specs):
    return [s for v in specs.values() for s in v if s.qform == P.CHOICE_FORM]


# ------------------------------------------------------------------------------------------------ FIX-1

def test_polarity_screen_flags_only_the_contracted_wording(pools):
    ctx = FV.make_ctx(pools, quarantine=False)
    plugin = FV.make_plugin(pools)
    assert plugin.quarantined_wordings(ctx) == {CONTRACTED: [
        "P3 contracted negative question frame (a negative polar question reads either way)"]}
    # every other wording of the 97: reads with its form's polarity under T21's own predicate lexicon
    assert sum(1 for s in ctx.skins.values() if s.kind == "wording") == 98


def test_quarantine_record_removes_the_three_pieces(pools):
    q = FV.load_quarantine()
    assert sorted(q) == sorted(QUARANTINED)
    ctx = FV.make_ctx(pools)
    assert not set(QUARANTINED) & set(ctx.skins)
    assert sum(1 for s in ctx.skins.values() if s.kind == "wording" and s.qform == "yn_not_capped") == 13
    assert sum(1 for s in ctx.skins.values() if s.kind == "skin" and s.register == "contract_ticket"
               and s.author_mode == "T") == 11
    assert sum(1 for s in ctx.skins.values() if s.kind == "skin" and s.register == "claims_log"
               and s.author_mode == "F") == 4
    fresh = FV.load_pools()
    fresh.skins.pop(QUARANTINED[1])
    with pytest.raises(ValueError):                                  # a record that names a piece that is not there
        FV.make_ctx(fresh)


def test_the_i1_wording_lint_refuses_only_the_contracted_wording(pools):
    ctx = FV.make_ctx(pools, quarantine=False)
    bad, seen = {}, set()
    for sid, sk in sorted(ctx.skins.items()):
        if sk.kind == "wording" and sk.qform != "ch_clause":
            _obj, v = AI.check_wording_i1(sid, sk.text, {"qform": sk.qform}, "t", "p", seen)
            if v:
                bad[sid] = v
    assert list(bad) == [CONTRACTED]
    assert any("contraction" in x for x in bad[CONTRACTED]) and any("P3" in x for x in bad[CONTRACTED])


@pytest.mark.parametrize("qform,text,ok", [
    ("yn_not_capped", "Is this claim not capped by clause {CAP_ID}?", True),
    ("yn_not_capped", "Does the cap of clause {CAP_ID} not limit the liability for this claim?", True),
    ("yn_not_capped", "Isn't this claim capped by clause {CAP_ID}?", False),
    ("yn_not_capped", "Doesn't the cap of clause {CAP_ID} limit this claim?", False),
    ("yn_not_capped", "Is it not the case that this claim is uncapped by clause {CAP_ID}?", False),   # not over a negative
    ("yn_double_neg", "Is it not the case that this claim is not capped by clause {CAP_ID}?", True),
    ("yn_double_neg", "Under these clauses, is it not true that the cap of clause {CAP_ID} does not limit the liability "
                      "for this claim?", True),
    ("yn_double_neg", "Isn't it the case that this claim is not capped by clause {CAP_ID}?", False),
    ("yn_double_neg", "Is it not the case that this claim is uncapped by clause {CAP_ID}?", False),
    ("yn_double_neg", "Is it not the case that the cap of clause {CAP_ID} fails to limit this claim?", False),
    ("yn_double_neg", "Is this claim not capped by clause {CAP_ID}?", False),                            # one negation only
    ("yn_uncapped", "Is this claim uncapped under these clauses?", True),
    ("yn_free_of", "Is this claim free of the cap of clause {CAP_ID}?", True),
])
def test_wording_lint_cases(qform, text, ok):
    _obj, v = AI.check_wording_i1("x", text, {"qform": qform}, "t", "p", set())
    assert (not v) is ok, v


def test_the_briefs_drop_the_contraction_examples():
    assert "isn't" in HA.WORDING_BRIEF["yn_not_capped"][1]          # the frozen v1 brief (never edited: tasks are pinned)
    rule = AI.BRIEF["yn_not_capped"][1]
    assert "Never a contraction" in rule and "isn't ... capped" not in rule
    dn = AI.BRIEF["yn_double_neg"][1]
    assert "is it not the case that" in dn and "TWO" in dn
    items, plan = AI.wording_items()
    assert len(items) == len(plan) == (8 + 1) * AI.CANDIDATES_PER_MISSING
    assert {p["qform"] for p in plan.values()} == {"yn_double_neg", "yn_not_capped"}


def test_a_failing_wording_is_never_drawn_and_the_pipeline_would_say_so():
    ctx = FX.ctx(bad=True)
    plugin = P.T21Plugin(lexicon=ctx.lexicon)
    assert "W-NOT-BAD" in plugin.quarantined_wordings(ctx)
    used = collections.Counter()
    for smp in TRAIN:
        for s in range(0, 150):
            spec = plugin.sample(s, smp)
            u = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
            assert u.ok, u.problems[:2]
            used.update(r["meta"]["wording_id"] for r in u.rows)
    assert used["W-NOT-BAD"] == 0 and used["W-NOT-1"] > 0
    # G-LEX safety net: a row that did get the failing wording is reported
    spec = next(plugin.sample(s, "S1") for s in range(300) if plugin.sample(s, "S1").qform == "yn_not_capped")
    rr = plugin.render(spec, ctx, wording=ctx.skin("W-NOT-BAD"))
    assert any(g == "G-LEX" and "polarity" in d for g, d in POL.row_problems(plugin, spec, rr, ctx))


# ------------------------------------------------------------------------------------------------ FIX-2

def test_clause_ids_are_role_blind(specs):
    ch = _choice(specs)
    assert len(ch) > 1000
    minors = collections.defaultdict(list)
    first_listed = 0
    for s in ch:
        env = s.env()
        ids = {n: env[n] for n in s.structure["order"] if n != "DEF_ID"}
        majors = {v.split(".")[0] for v in ids.values()}
        assert len(majors) == 1 and 6 <= int(next(iter(majors))) <= 14                 # one section, no band to tell roles
        assert len({len(f"Clause {v}") for v in ids.values()}) == 1                    # every option the same length
        for n, v in ids.items():
            minors["CAP" if n == "CAP_ID" else "X" if n == "X_ID" else "Y" if n == "Y_ID" else "L"].append(int(v.split(".")[1]))
        order_ids = [env[n] for n in s.structure["order"] if n != "DEF_ID"]
        first_listed += order_ids[0] == env["CAP_ID"]
    for role, vals in minors.items():
        assert 3.9 <= sum(vals) / len(vals) <= 5.1, role                                # uniform 1-8: mean 4.5
        c = collections.Counter(vals)
        assert min(c.get(m, 0) for m in range(1, 9)) > 0.06 * len(vals), (role, c)     # every minor, every role
    assert first_listed / len(ch) < 0.45                                                # the cap clause is not listed first


# ------------------------------------------------------------------------------------------------ FIX-3 / FIX-8

def test_nothing_visible_predicts_capped(specs):
    yn = _yes_no(specs)
    cap = {id(s): P.capped(s) for s in yn}
    assert 0.47 <= sum(cap.values()) / len(yn) <= 0.53

    def rate(feature):
        by = collections.defaultdict(lambda: [0, 0])
        for s in yn:
            by[feature(s)][0] += 1
            by[feature(s)][1] += cap[id(s)]
        return {k: (n, c / n) for k, (n, c) in by.items() if n >= 200}
    feats = {
        "n_clauses": lambda s: len(s.structure["order"]),
        "n_links": lambda s: s.structure["plan"]["n_links"],
        "has_decoy": lambda s: "X_ID" in s.slots,
        "has_def": lambda s: s.structure["def"] is not None,
        "qualifier": lambda s: s.structure["clauses"][0]["cause"] is not None,
        "n_back": lambda s: sum(c["level"] == 2 and not c["decoy"] for c in s.structure["clauses"]),
        "sampler": lambda s: s.sampler,
        "polarity": lambda s: P.T21Plugin.QFORMS[s.qform].polarity,
    }
    for name, f in feats.items():
        r = rate(f)
        assert r, name
        for k, (n, p) in r.items():
            assert abs(p - 0.5) < 0.075, (name, k, n, round(p, 3))        # the pilot's n_numbers + qform baseline was 0.645


def test_no_card_has_a_single_clause_and_every_chain_has_a_link(specs):
    for v in specs.values():
        for s in v:
            assert len(s.structure["order"]) >= 2 and s.structure["plan"]["n_links"] >= 1


def test_yes_no_cells_are_stratified(plugin):
    cells = collections.Counter()
    for s in range(900_000, 900_000 + 640):
        spec = plugin.sample(s, "S1")
        if spec.qform != P.CHOICE_FORM:
            cells[(P.capped(spec), P.T21Plugin.QFORMS[spec.qform].polarity)] += 1
    assert len(cells) == 4 and max(cells.values()) - min(cells.values()) <= 8, cells


def test_yes_no_rows_are_never_deep_and_meta_depth_is_the_chain_length(units):
    rows = [r for u in units for r in u.rows]
    assert rows and not any(r["meta"]["deep"] for r in rows if r["qtype"] == "noul")
    by = collections.defaultdict(lambda: [0, 0])
    for u in units:
        for rr in u.rendered:
            if rr.row["qtype"] != "noul":
                continue
            d = rr.row["meta"]["depth"]
            assert d in (1, 2, 3)
    ys = [r for r in rows if r["qtype"] == "noul" and r["meta"]["qform"] == "yn_capped"]
    for r in ys:
        by[r["meta"]["depth"]][0] += 1
        by[r["meta"]["depth"]][1] += r["gold"]
    for d, (n, c) in by.items():
        if n >= 40:
            assert 0.3 <= c / n <= 0.7, (d, n, c)             # the deciding depth (R9 parity) is not what meta.depth says


def test_the_cap_clause_is_gold_one_in_k(plugin, specs):
    by = collections.defaultdict(lambda: [0, 0])
    for s in _choice(specs):
        k = len(plugin._options(s))
        by[k][0] += 1
        by[k][1] += P.deciding(s) == s.env()["CAP_ID"]
    assert set(by) == {3, 4, 5, 6}
    for k, (n, c) in by.items():
        assert n >= 300 and abs(c / n - 1 / k) < 0.03, (k, n, c / n)


def test_twin_rows_are_half_capped_and_keep_the_chain_shape(plugin, specs):
    yn = [s for s in _yes_no(specs)][:2400]
    twins = []
    for s in yn:
        for prop in plugin.relations(s):
            if prop.kind == "twin":
                twins.append((s, prop))
    assert len(twins) > 300
    capped = sum(P.capped(plugin.derive(p.spec)) for _s, p in twins) / len(twins)
    assert 0.40 <= capped <= 0.60, capped
    for s, p in twins:
        assert plugin._monotone(P.cover_vector(p.spec)) and not p.spec.deep
        assert P.capped(plugin.derive(p.spec)) != P.capped(s)
    ch = [s for s in _choice(specs)][:2400]
    n_tw = n_cap = 0
    for s in ch:
        for prop in plugin.relations(s):
            if prop.kind == "twin":
                n_tw += 1
                n_cap += P.deciding(plugin.derive(prop.spec)) == prop.spec.env()["CAP_ID"]
                assert plugin._monotone(P.cover_vector(prop.spec))
    assert n_tw > 150 and 0.12 <= n_cap / n_tw <= 0.36, (n_tw, n_cap)


def test_choice_rows_keep_the_plain_layout_and_equiv_changes_the_skin(plugin, ctx):
    n = 0
    for s in range(900_000, 900_000 + 300):
        spec = plugin.sample(s, "S5")
        assert spec.structure["layout"] == ("plain" if spec.qform == P.CHOICE_FORM else "schedule")
        u = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
        assert u.ok, u.problems[:2]
        for r in u.rows:
            if r["qtype"] == "choice":
                assert "Clauses of the " in r["state"] and "Schedule of clauses" not in r["state"]
                n += 1
    assert n > 50


# ------------------------------------------------------------------------------------------------ FIX-5

def test_sampler_schedule_gives_s4_85_percent():
    sched = P.sampler_schedule()
    c = collections.Counter(sched)
    assert c["S4"] / c["S1"] == pytest.approx(0.85) and c["S1"] == c["S2"] == c["S3"] == 20
    assert sched == P.sampler_schedule()                                    # deterministic, no hash
    assert set(sched) == {"S1", "S2", "S3", "S4"}
    assert P.sampler_schedule({"S1": 1, "S2": 1, "S3": 1, "S4": 1}).count("S4") == 20
    with pytest.raises(ValueError):
        P.sampler_schedule({"S1": 1, "S2": 1, "S3": 1, "S4": 0})


def test_the_pilot_wrapper_follows_the_weights_and_restores_the_plugin(plugin, ctx):
    kit = types.SimpleNamespace(family="T21", plugin=plugin, ctx=ctx)
    b = RUN.build_weighted(kit, 130, run_g15=False)
    per = b.stats["per_sampler"]
    assert per["S4"]["attempted"] < per["S1"]["attempted"] and per["S1"]["attempted"] == per["S2"]["attempted"]
    assert "sample" not in plugin.__dict__ and "SAMPLERS" not in plugin.__dict__
    assert b.stats["sampler_seed_weights"]["S4"] == 0.85 and b.stats["training_samplers"] == list(TRAIN)
    seeds_by = collections.defaultdict(list)
    for i in b.infos:
        if i.row["role"] == "base":
            seeds_by[i.row["meta"]["sampler"]].append(i.row["meta"]["seed"])
    for smp, ss in seeds_by.items():
        assert ss == list(range(900_000, 900_000 + len(ss))), smp           # consecutive per sampler from SEED_BASE


# ------------------------------------------------------------------------------------------------ FIX-6

def test_double_negation_is_drawn_only_once_a_clean_wording_exists(plugin):
    assert not any(s.qform == P.DOUBLE_NEG_FORM for s in (plugin.sample(i, "S1") for i in range(400)))
    assert plugin.double_neg_ok == {False: False, True: False}


def test_double_negation_rows_pass_every_gate_and_complement_with_not_capped():
    ctx = FX.ctx(double_neg=True)
    plugin = P.T21Plugin(lexicon=ctx.lexicon)
    assert plugin.double_neg_ok == {False: True, True: True}
    n_dn = n_yn = 0
    for smp in TRAIN:
        for s in range(0, 160):
            spec = plugin.sample(s, smp)
            n_yn += spec.qform != P.CHOICE_FORM
            if spec.qform != P.DOUBLE_NEG_FORM:
                continue
            n_dn += 1
            u = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
            assert u.ok, u.problems[:2]
            for r in u.rows:
                if r["meta"]["qform"] == P.DOUBLE_NEG_FORM:
                    c = negcount.count(ctx.skin(r["meta"]["wording_id"]).text.replace("{CAP_ID}", "9.1"))
                    assert (c.k_all, c.k_syn) == (2, 2)
                    if r["role"] == "base":
                        assert r["gold"] == int(P.capped(spec))           # positive polarity: yes iff capped
                elif r["role"] == "complement":
                    assert r["meta"]["qform"] == "yn_not_capped"
    assert n_dn > 15 and 0.02 <= n_dn / n_yn <= 0.12, (n_dn, n_yn)


# ------------------------------------------------------------------------------------------------ FIX-7

def test_the_card_styles_keep_every_rule():
    assert CARD_MOD.SPEC.problems() == []
    old = Path(FV.G0_AT_FREEZE).read_text(encoding="utf-8").split("### 1.2 The card")[1].split("```")[1].strip("\n")
    assert CARD_MOD.TEMPLATES["full"] == P.CARD == old                       # the frozen v1.2 card, verbatim
    full, short = CARD_MOD.TEMPLATES["full"], CARD_MOD.TEMPLATES["short"]
    assert len(short) < len(full) and short.endswith(P.CLOSED_WORLD) and full.endswith(P.CLOSED_WORLD)
    assert len(CARD_MOD.ITEMS) == 7 and all(it.short for it in CARD_MOD.ITEMS)
    for it in CARD_MOD.ITEMS:
        assert KC.variant_problems(it.full, it.short) == [], it.item_id
    assert set(CARD_MOD.SHARES["noul"]) == {"full", "short"} and CARD_MOD.SHARES["noul"]["short"] <= KC.SHORT_CAP


def test_rules_sit_where_the_prompt_prints_them_once(units):
    styles = collections.Counter()
    for u in units:
        assert u.ok, u.problems[:2]
        cards = {r["card"] for r in u.rows if r["qtype"] == "noul"}
        assert len(cards) <= 1                                                # every yes/no row of a unit prints one card
        for r in u.rows:
            ds = r["meta"]["defs_style"]
            styles[ds] += 1
            if r["qtype"] == "noul":
                assert ds.startswith("rules_in_card_") and r["card"].endswith(P.CLOSED_WORLD)
                assert "\n\n" not in r["instructions"] and "How to read" not in r["instructions"]
            else:
                assert ds.startswith("rules_in_state_") and r["card"] is None and "\n\n" not in r["instructions"]
                assert r["state"].rstrip().endswith(P.CLOSED_WORLD)
    assert {"rules_in_card_full", "rules_in_card_short", "rules_in_state_full", "rules_in_state_short"} <= set(styles)
    n = sum(styles.values())
    assert 0.08 <= (styles["rules_in_card_short"] + styles["rules_in_state_short"]) / n <= 0.25


def test_solver_b_reads_both_placements_and_refuses_a_misplaced_card(plugin, ctx, units):
    ch = next(r for u in units for r in u.rows if r["qtype"] == "choice")
    yn = next(r for u in units for r in u.rows if r["qtype"] == "noul")
    plugin.parse(ch, ctx)
    plugin.parse(yn, ctx)
    moved = dict(yn, card=None, instructions=yn["card"] + "\n\n" + yn["instructions"])
    with pytest.raises(B.ParseError):
        plugin.parse(moved, ctx)
    wrong = dict(ch, meta={**ch["meta"], "defs_style": "rules_in_state_short" if "full" in ch["meta"]["defs_style"]
                           else "rules_in_state_full"})
    with pytest.raises(B.ParseError):
        plugin.parse(wrong, ctx)


def test_the_real_pools_stay_under_800_tokens_on_average(pools):
    ctx = FV.make_ctx(pools)
    plugin = FV.make_plugin(pools)
    rows = []
    for smp in TRAIN:
        for s in range(900_000, 900_000 + 60):
            u = pipeline.build_unit(plugin, plugin.sample(s, smp), ctx, run_g15=False)
            assert u.ok, u.problems[:2]
            rows += u.rows
    rep = KC.token_report(rows)
    if "pinned" not in rep["counted_by"]:
        pytest.skip("pinned tokenizer unavailable")
    assert rep["mean"] <= 800 and rep["max"] <= 2000, rep
    assert 0.42 <= rep["yes_no_share"] <= 0.58


# ------------------------------------------------------------------------------------------------ determinism

_SCRIPT = (
    "import sys, hashlib, json; sys.path.insert(0, %r); sys.dont_write_bytecode = True\n"
    "from transfer.T21 import fixtures as FX, plugin as P\n"
    "from c2_kit import pipeline\n"
    "ctx = FX.ctx(double_neg=True); pl = P.T21Plugin(lexicon=ctx.lexicon); h = hashlib.sha256()\n"
    "for smp in ('S1','S2','S3','S4','S5'):\n"
    "    for s in range(900000, 900030):\n"
    "        u = pipeline.build_unit(pl, pl.sample(s, smp), ctx, run_g15=False)\n"
    "        assert u.ok, u.problems[:2]\n"
    "        h.update(json.dumps(u.rows, sort_keys=True).encode())\n"
    "print(h.hexdigest(), P.sampler_schedule())\n")


def test_generation_is_identical_under_two_hash_seeds():
    out = []
    for hs in ("1", "4242"):
        env = dict(os.environ, PYTHONHASHSEED=hs)
        r = subprocess.run([sys.executable, "-B", "-c", _SCRIPT % str(C2_BUILD)], capture_output=True, text=True, env=env,
                           cwd=str(C2_BUILD), timeout=600)
        assert r.returncode == 0, r.stderr[-800:]
        out.append(r.stdout.strip())
    assert out[0] == out[1] and len(out[0]) > 64
