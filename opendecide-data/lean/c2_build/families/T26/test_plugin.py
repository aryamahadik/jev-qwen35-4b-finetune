"""c2_build/families/T26/test_plugin.py: in-memory tests for the T26 plugin (no file is written: A37 f).

Covers: the plugin contract (strict); solver A = solver B and parse = canonical on >= 5,000 sampled specs; every
relation unit through the kit gates; twins that differ in exactly one provenance field and flip as constructed
(re-checked by solver B's pair checker); complements with opposite gold; balance by construction on 2,000 specs; trap,
overlay and length targets of G0 section 2; G-SL on the built-in placeholder skins; determinism by seed; look-alike and
near-miss construction; and injected bugs that G2 / G3 / G-TW must catch.

Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T26
"""
from __future__ import annotations

import collections
import dataclasses
import random
import re
import statistics
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import gsl, pipeline  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.paths import never_open  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from families.T26 import fixtures as FX  # noqa: E402
from families.T26 import plugin as P  # noqa: E402
from families.T26 import solver_b as B  # noqa: E402

import negcount  # noqa: E402  (c_src/common, on sys.path through c2_kit.paths)

TRAIN = ("S1", "S2", "S3", "S4")


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T26Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def base_specs(plugin):
    """2,000 base specs: seeds 0-499 of each training sampler."""
    return [plugin.sample(seed, smp) for smp in TRAIN for seed in range(500)]


@pytest.fixture(scope="module")
def units(plugin, ctx, base_specs):
    """Every base spec (+ 200 S5 specs) through pipeline.build_unit (G2, G3, G4, G-SL, G-LEX, G-TW, schema)."""
    out = [pipeline.build_unit(plugin, s, ctx, run_g15=False) for s in base_specs]
    return out + [pipeline.build_unit(plugin, plugin.sample(seed, "S5"), ctx, run_g15=False) for seed in range(200)]


# ------------------------------------------------------------------------------------------------ contract

def test_plugin_meets_the_strict_contract(plugin):
    assert KP.validate_plugin(plugin, strict=True) == []
    assert KP.check_independence(plugin) == []
    assert plugin.PARADIGM_A != plugin.PARADIGM_B
    assert len(P.HERE.joinpath("G0_SPEC.md").read_text(encoding="utf-8").splitlines()) <= 200


def test_fixture_lexicon_is_admitted_and_unambiguous(ctx):
    reg = ctx.lexicon
    assert reg.gate()["pass"], reg.gate()
    assert all(f.unit_ok for f in reg.forms.values())
    assert sum(1 for f in reg.forms.values() if f.sem_id == P.PREC_SEM) >= 2      # G4 needs a second paraphrase
    for qf in P.T26Plugin.QFORMS:
        assert any(s.kind == "wording" and s.qform == qf for s in ctx.skins.values()), qf


def test_this_package_opens_no_never_open_path():
    for f in P.HERE.iterdir():
        assert never_open(f) is None, f


# ------------------------------------------------------------------------------------------------ G2 / G3

def test_solver_a_equals_solver_b_on_5000_specs(plugin, ctx):
    n, golds = 0, collections.Counter()
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
            golds[(spec.qform, a)] += 1
            n += 1
    assert n >= 5000
    assert {a for (q, a) in golds if q == "ch_verdict"} == {"apply", "reject", "escalate"}
    assert {a for (q, a) in golds if q == "ch_failing"} == set(P.CHECKS) | {"none"}


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
    assert 0.03 <= rep["attack_share"] <= 0.08, rep["attack_share"]
    assert rep["abstain"]["pass"] and rep["abstain"]["wrong_share"] >= 0.5
    chi2_01 = {1: 6.63, 2: 9.21, 3: 11.34, 4: 13.28, 5: 15.09, 6: 16.81, 7: 18.48, 8: 20.09}
    for k, counts in rep["gold_positions"].items():          # G10: gold position uniform per bucket (p > 0.01)
        mean = sum(counts) / k
        assert sum((c - mean) ** 2 / mean for c in counts) < chi2_01[k - 1], (k, counts)
    rows = [r for u in units for r in u.rows]
    assert max(collections.Counter(r["call_id"] for r in rows).values()) <= 3


def test_twins_differ_in_one_provenance_field_and_flip_as_constructed(plugin, ctx, base_specs):
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
            rt = plugin.render(twin, ctx, skin=ctx.skin(rr.skin_id), wording=ctx.skin(rr.wording_id), forms=rr.forms)
            va, vb = B.parse(rr.row, ctx), B.parse(rt.row, ctx)
            assert B.pair_diff(va, vb) == {"facts." + prop.changed_slot}           # solver B's pair checker
            assert (B.solve_b(va), B.solve_b(vb)) == (a, b)
            seen[prop.note.split(":")[0]] += 1
    assert set(seen) == set(P.CHECKS), seen                  # every check kind is twinned somewhere
    assert sum(seen.values()) >= 600


def test_complements_have_opposite_gold_and_one_predicate(plugin, units):
    pairs = 0
    for u in units:
        by_id = {r["id"]: r for r in u.rows}
        for rel in u.rels:
            if rel["type"] != "complement":
                continue
            a, b = by_id[rel["a"]], by_id[rel["b"]]
            qa, qb = plugin.QFORMS[a["meta"]["qform"]], plugin.QFORMS[b["meta"]["qform"]]
            assert a["gold"] + b["gold"] == 1 and qa.predicate == qb.predicate and qa.polarity != qb.polarity
            assert a["state"] == b["state"] and a["card"] == b["card"]
            for r in (a, b):                                                  # v1.2: the rules sit in row.card
                assert P.CLOSED_WORLD in (r["card"] or "") + r["instructions"]
            pairs += 1
    assert pairs >= 300


def test_metamorphic_relations_hold(plugin, base_specs):
    notes = collections.Counter()
    for spec in base_specs[:800]:
        for prop in plugin.relations(spec):
            if prop.kind == "metamorphic":
                assert plugin.solve_a(plugin.derive(prop.spec)) == plugin.solve_a(spec), prop.note
                notes[prop.note.split(" register")[0]] += 1
    assert len(notes) >= 4, notes


# ------------------------------------------------------------------------------------------------ balance and traps

def _verdict(plugin, spec):
    return P._decide(plugin._statuses(spec))


def test_gold_balance_on_2000_specs(plugin, base_specs):
    yn = [s for s in base_specs if plugin.QFORMS[s.qform].qtype == "noul"]
    assert 0.45 <= len(yn) / len(base_specs) <= 0.55
    for qf in {s.qform for s in yn}:
        xs = [plugin.solve_a(s) for s in yn if s.qform == qf]
        assert abs(sum(xs) / len(xs) - 0.5) <= 0.02, qf
    assert abs(sum(plugin.solve_a(s) for s in yn) / len(yn) - 0.5) <= 0.02
    bad = sum(1 for s in yn if plugin.QFORMS[s.qform].yes_is_bad) / len(yn)
    assert 0.45 <= bad <= 0.55
    cv = collections.Counter(plugin.solve_a(s) for s in base_specs if s.qform == "ch_verdict")
    n = sum(cv.values())
    assert all(abs(cv[v] / n - 1 / 3) <= 0.01 for v in P.VERDICTS), cv          # v1.2 (S18): the abstain gold is 1 / k
    cf = [plugin.solve_a(s) for s in base_specs if s.qform == "ch_failing"]
    assert 0.20 <= cf.count("none") / len(cf) <= 0.35


def test_pairs_are_antithetic_and_cards_mirrored(plugin):
    for smp in TRAIN:
        for k in range(300):
            a, b = plugin.sample(2 * k, smp), plugin.sample(2 * k + 1, smp)
            assert a.qform == b.qform
            ca, cb = int(a.card_id[-2:]), int(b.card_id[-2:])
            assert ca + cb == P.N_CARDS[smp] - 1                                   # mirrored cards
            assert a.structure["checks"] == b.structure["checks"] and a.structure["defs"] == b.structure["defs"]
            piv = P.PIVOT[a.qform]                    # None: choice rows follow the slot schedule (v1.2)
            if piv == "apply":
                assert (_verdict(plugin, a) == "apply") + (_verdict(plugin, b) == "apply") == 1
            elif piv == "fail":
                assert ("fail" in plugin._statuses(a).values()) + ("fail" in plugin._statuses(b).values()) == 1
    rates = [P.card_rate(c, 16) for c in range(16)]
    assert min(rates) >= 0.2 and max(rates) <= 0.8 and abs(statistics.mean(rates) - 0.5) < 1e-9


def test_trap_shares_meet_spec_3_7(plugin, ctx, units, base_specs):
    rows = [r for u in units[:2000] for r in u.rows]
    edge = collections.Counter(e for r in rows for e in r["meta"]["edge"])
    assert 0.20 <= edge["lookalike_domain"] / len(rows) <= 0.25, edge["lookalike_domain"] / len(rows)
    assert 0.15 <= edge["right_domain_missing_addendum"] / len(rows) <= 0.20
    legit_alarming = sum(1 for s in base_specs
                         if _verdict(plugin, s) == "apply" and "-URG-" in plugin.render(s, ctx).skin_id)
    apply_share = sum(1 for s in base_specs if _verdict(plugin, s) == "apply") / len(base_specs)
    # v1.2: the verdict thirds put apply on 1 / 3 of the choice rows, so the apply share is about 0.38 of the base rows;
    # the fixture pool is half alarming, so about 19% here; the frozen Haiku pool is 55% alarming (20-25%, measured at
    # the pilot on real rows: pilot_i1 / PILOT_REPORT.json)
    assert 0.34 <= apply_share <= 0.42, apply_share
    assert abs(legit_alarming / len(base_specs) - apply_share / 2) <= 0.03
    assert sum(s.deep for s in base_specs) / len(base_specs) <= 0.10


def test_negation_quotas_on_yes_no_rows(units):
    yn = [r for u in units[:2000] for r in u.rows if r["qtype"] == "noul"]
    k = [negcount.count(r["instructions"].split("\n\n")[-1]).k_syn for r in yn]
    assert sum(1 for x in k if x >= 1) / len(yn) >= 0.10
    assert sum(1 for x in k if x >= 2) / len(yn) >= 0.02


def test_construction_invariants(plugin, base_specs):
    for s in base_specs:
        stc = s.structure
        full = plugin._statuses(s, pool=stc["shown"])
        assert all(full[c] != "fail" for c in stc["shown"] if c not in stc["checks"])   # inert records never fail
        assert 2 <= len(stc["checks"]) <= 4 and set(stc["checks"]) <= set(stc["shown"])
        if s.qform == "ch_failing":
            st = plugin._statuses(s)
            assert "unver" not in st.values() and list(st.values()).count("fail") <= 1
        assert (stc["labels"] is not None) <= (s.qform == "ch_verdict")
        if "domain" in stc["shown"] and "REG_DOMAIN" in s.slots and s.slots["SENDER_DOMAIN"] != s.slots["REG_DOMAIN"]:
            assert s.slots["SENDER_DOMAIN"].value.isascii()


def test_lengths(units):
    rows = [r for u in units for r in u.rows]
    toks = [R.approx_tokens(r) for r in rows]
    assert max(toks) <= R.MAX_TOKENS
    chars4 = [t * R.CHARS_PER_TOKEN / 4 for t in toks]        # ~4 characters per real token (mixer re-checks)
    assert statistics.mean(chars4) <= 800


# ------------------------------------------------------------------------------------------------ G-SL on fixtures

def test_builtin_placeholder_skins_pass_gsl(plugin, ctx):
    for sk in ctx.skins.values():
        if sk.author_mode == "T":
            v = gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                                  name_allow=plugin.NAME_ALLOW)
            assert v == [], (sk.skin_id, v)
        if sk.kind == "skin":
            assert set(sk.decl) <= set(P.T26Plugin.NARRATIVE), sk.skin_id              # G0 section 4 slot list
            lit = re.sub(r"\{[^{}]*\}", " ", sk.text) if sk.author_mode == "T" else sk.text
            for v in sk.brief:
                lit = lit.replace(v[1], " ")
            assert not re.search(r"\d|@|\$|%|\b[a-z0-9-]+\.(?:example|test|com|net|org)\b", lit), sk.skin_id
            words = set(re.findall(r"[a-z]+", lit.lower()))
            assert not words & {"apply", "applied", "reject", "rejected", "escalate", "escalated", "legitimate", "fake",
                                "genuine", "verify", "verified", "pass", "passed", "fail", "failed"}, sk.skin_id
    tones = collections.Counter("URG" if "-URG-" in s.skin_id else "CALM" for s in ctx.skins.values()
                                if s.kind == "skin" and not s.held_out)
    assert tones["URG"] == tones["CALM"]


def test_mode_f_rows_pass_the_fact_lock(plugin, ctx):
    spec = plugin.sample(3, "S1")
    rr = plugin.render(spec, ctx, skin=ctx.skin("SK-FREE-CALM-1"))
    assert pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False) == []
    assert plugin.extract_view(spec)["req_id"] == spec.slots["REQ_ID"].value
    assert [f.name for f in plugin.extract_fields(spec)] == ["requester", "counterparty", "change", "req_id"]


def test_gsl_catches_a_leaky_skin(plugin, ctx):
    base = ctx.skin("SK-SMS-CALM-1")
    for extra in (" It is verified.", " Call 555-0100.", " Reply to ops@brightwell.example now."):
        leaky = dataclasses.replace(base, skin_id="SK-LEAK", text=base.text + extra)
        c2 = dataclasses.replace(ctx, skins={**ctx.skins, "SK-LEAK": leaky})
        spec = plugin.sample(5, "S1")
        probs = pipeline.check_rendered(plugin, spec, plugin.render(spec, c2, skin=leaky), c2, run_g15=False)
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


def test_s5_rows_are_dev_only(units):
    s5 = [r for u in units[2000:] for r in u.rows]
    assert s5 and all(r["meta"]["dev_only"] for r in s5)
    assert all(R.validate_row(r, training=True) for r in s5)
    assert all(not r["meta"]["dev_only"] for u in units[:200] for r in u.rows)


# ------------------------------------------------------------------------------------------------ helpers

def test_lookalikes_and_near_misses():
    rng = random.Random(7)
    kinds = collections.Counter()
    for _, label in P.PACKS:
        for tld in P.TLDS:
            d = f"{label}.{tld}"
            for _ in range(20):
                x = P.lookalike(d, rng)
                assert x != d and x.isascii() and x == x.lower() and P._norm(x) != P._norm(d)
                S.id_slot(x)
                kinds["suffix" if x.split(".", 1)[1] != tld else "label"] += 1
    assert kinds["suffix"] and kinds["label"]
    for v in ("ADD-0417", "FV-204C", "BK-48213", "555-0142"):
        for _ in range(50):
            x = P.near_miss(v, rng, tail=2 if v.startswith("555") else None)
            assert x != v and P.is_near(x, v) and len(x) == len(v)
    with pytest.raises(B.ParseError):
        B._same("brightwell.example", "Brightwell.example")             # normaliser guard: case-only pair refused
    assert B._same("brightwell.example", "brightwell.example")
    assert not B._same("brightwell.example", "brightwe1l.example")


def test_wrong_options_come_from_named_error_models(plugin, ctx, base_specs):
    produced, named, wrong = collections.Counter(), collections.Counter(), collections.Counter()
    for spec in base_specs:
        if spec.qform not in ("ch_verdict", "ch_failing"):
            continue
        rr = plugin.render(spec, ctx)
        for o in rr.option_set.options:
            if o.role == "gold":
                continue
            kind = "verdict" if spec.qform == "ch_verdict" else ("none" if o.key == "none" else "check")
            wrong[kind] += 1
            named[kind] += bool(o.err)
            produced.update(o.err)
        assert set(rr.row["meta"]["opt_err"]) == set(rr.row["options"]) - {rr.row["gold"]}
    assert set(produced) == set(P.EM_VARIANTS), set(P.EM_VARIANTS) - set(produced)   # every model is exercised
    assert named["verdict"] == wrong["verdict"] and named["none"] == wrong["none"]      # always named
    assert named["check"] / wrong["check"] >= 0.5, named["check"] / wrong["check"]     # closed-set names (open issue)


# ------------------------------------------------------------------------------------------------ injected bugs

def _gate_failures(plugin, ctx, n=120, units_too=False):
    out = collections.Counter()
    for smp in ("S1", "S2", "S3", "S4"):
        for seed in range(n // 4):
            try:
                spec = plugin.sample(seed, smp)
            except KP.ContractError:          # v1.2: sample() checks solver A against the planned outcome (label-first)
                out["sample"] += 1
                continue
            if units_too:
                probs = pipeline.build_unit(plugin, spec, ctx, run_g15=False).problems
            else:
                probs = pipeline.check_rendered(plugin, spec, plugin.render(spec, ctx), ctx, run_g15=False)
            for g, _ in probs:
                out[g] += 1
    return out


def test_g2_catches_a_solver_b_precedence_bug(plugin, ctx, monkeypatch):
    monkeypatch.setitem(B.OUTCOME, (True, True), "escalate")            # "escalate beats reject" in solver B
    assert _gate_failures(plugin, ctx, 400)["G2"] > 0


def test_g2_catches_a_solver_a_precedence_bug(plugin, ctx, monkeypatch):
    rules = P.OUTCOME_RULES
    monkeypatch.setattr(P, "OUTCOME_RULES", (rules[1], rules[0], rules[2]))
    f = _gate_failures(plugin, ctx, 400)
    assert f["G2"] + f["sample"] > 0           # caught by G2 or, earlier, by sample()'s plan-vs-solver-A check


def test_g2_catches_a_solver_b_lookalike_bug(plugin, ctx, monkeypatch):
    real = B._matches
    monkeypatch.setattr(B, "_matches", lambda f, c: True if c == "domain" else real(f, c))
    assert _gate_failures(plugin, ctx, 200)["G2"] > 0


def test_g3_catches_a_card_that_misstates_a_rule(plugin, ctx, monkeypatch):
    monkeypatch.setitem(P.CHECK_RULE, "callback", "the logged call-back dialled any number about this request's id")
    assert _gate_failures(plugin, ctx, 200)["G3"] > 0


def test_g3_catches_a_packet_that_prints_the_wrong_fact(plugin, ctx, monkeypatch):
    real = P.T26Plugin._record_value

    def swapped(self, spec, c):                              # the call-back record prints its two numbers swapped
        v = real(self, spec, c)
        return v.replace("{PHONE_ON_FILE}", "{@}").replace("{CB_NUM}", "{PHONE_ON_FILE}").replace("{@}", "{CB_NUM}")

    monkeypatch.setattr(P.T26Plugin, "_record_value", swapped)
    assert _gate_failures(plugin, ctx, 200)["G3"] > 0


def test_gtw_catches_a_wrong_twin_prediction(plugin, ctx, monkeypatch):
    real = P.T26Plugin._twin

    def wrong(self, spec):                                   # predicts "no flip" on yes/no twins: G-TW must refuse
        t = real(self, spec)
        return t if t is None or not isinstance(t.expect, int) else dataclasses.replace(t, expect=1 - t.expect)

    monkeypatch.setattr(P.T26Plugin, "_twin", wrong)
    f = _gate_failures(plugin, ctx, 200, units_too=True)
    assert f["G-TW"] > 0 and f["G2"] == 0 and f["G3"] == 0


# ------------------------------------------------------------------------------------------------ review fix: twin mix

def test_abstain_share_holds_on_every_emitted_row(plugin, ctx):
    """Minimal-edit twins mirror their base: fixing the one failing item of a base lands on the abstain key, so
    unthinned twins piled up there (42% of all emitted ch_failing rows against a G0 target of 1 / (n + 1), about 25%).
    Twins onto the key are thinned (kit relations.abstain_twin_kept); P(gold | key shown) over ALL emitted rows (base,
    twin, equiv, inv) is now within 5 pp of the target."""
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
    target = chance / shown
    assert shown >= 300 and roles["twin"] >= 30, (shown, roles)
    assert abs(gold / shown - target) <= 0.05, (gold / shown, target, roles)


# ------------------------------------------------------------------------------------------------ G0 resolution (H1-H49)

def test_g0_is_frozen_after_the_haiku_pass(plugin):
    assert plugin.G0_SHA256 and "amb:T26" in plugin.G0_HAIKU_PASS
    text = P.HERE.joinpath("G0_SPEC.md").read_text(encoding="utf-8")
    assert "FROZEN" in text and all(f"H{i} " in text for i in range(1, 50))


def test_yes_no_forms_on_escalate_rows_follow_s17(plugin, base_specs):
    """H1, H15: on escalate rows yn_clears is yes, yn_fails no, yn_hold and yn_not_apply yes (S17, literal)."""
    seen = 0
    for s in base_specs:
        st = plugin._statuses(s)
        if P._decide(st) != "escalate":
            continue
        seen += 1
        assert P._answer("yn_clears", st) == 1 and P._answer("yn_fails", st) == 0
        assert P._answer("yn_hold", st) == 1 and P._answer("yn_not_apply", st) == 1 and P._answer("yn_apply", st) == 0
    assert seen >= 100


def test_requester_is_never_the_approver_or_in_the_table(base_specs):
    """H3: the role check never meets self-approval; t26_requester_as_approver always reads the role check as failed."""
    for s in base_specs:
        v, n = s.env(), s.structure["n_dt"]
        names = {v[f"DT_NAME_{i}"] for i in range(n)}
        assert v["REQUESTER"] not in names and v.get("APPROVER") != v["REQUESTER"]
        assert v["CONTACT"] not in names | {v["REQUESTER"], v.get("APPROVER")}


def test_masked_codes_name_all_three_outcomes(plugin, ctx):
    """H4: three distinct codes, every outcome named, mapping seeded per row (no code fixed to an outcome)."""
    by_outcome = collections.defaultdict(set)
    n = 0
    for seed in range(1500):
        spec = plugin.sample(seed, "S1")
        lab = spec.structure["labels"]
        if lab is None:
            continue
        n += 1
        assert len({lab["apply"], lab["reject"], lab["escalate"]}) == 3 and sorted(lab["order"]) == sorted(P.VERDICTS)
        text = P._mask_template(lab)
        for k in P.VERDICTS:
            by_outcome[k].add(lab[k])
            assert f'"{lab[k]}" means' in text
    assert n >= 30 and all(len(c) >= 4 for c in by_outcome.values())


def test_extraction_offers_the_decoy_readings(ctx):
    """H1, H15, H28: G-LEX extractors see the decoy meanings, so a narrower or unqualified wording can be rejected."""
    reg = ctx.lexicon
    wid = next(f for f, x in reg.forms.items() if x.sem_id == "q.t26.yn_clears")
    pid = next(f for f, x in reg.forms.items() if x.sem_id == P.PREC_SEM)
    items = dict(reg.lexicon_items([wid, pid]))
    assert set(P.DECOY_QUESTION_MEANINGS.values()) <= set(items[wid]["choices"])
    assert set(P.PREC_DECOYS.values()) <= set(items[pid]["choices"]) and len(items[pid]["choices"]) == 4
    for meaning in P.DECOY_QUESTION_MEANINGS.values():
        assert reg.meaning_to_sem("question", meaning).startswith("q.t26.decoy_")


def test_none_share_on_base_rows_tracks_the_uniform_target(plugin, base_specs):
    """H32 (S19): P(none) = 1 / (n + 1) per row; the base-row share is within 5 pp of its mean."""
    cf = [s for s in base_specs if s.qform == "ch_failing"]
    share = sum(plugin.solve_a(s) == "none" for s in cf) / len(cf)
    target = statistics.mean(1 / (len(s.structure["checks"]) + 1) for s in cf)
    assert abs(share - target) <= 0.05, (share, target)


# ------------------------------------------------------------------------------------------------ v1.2: number budget, slot positions, depth (G0 S28-S30)

def test_packet_number_budget_is_independent_of_the_outcome(plugin, ctx, base_specs):
    """G0 S29: the packet prints the same number of numbers whatever the outcome (G6 d_meta read the gold off the count);
    the pad line exists on every row and holds at least one number."""
    by = collections.defaultdict(list)
    for sp in base_specs:
        assert "PAD" in sp.derived and sp.derived["PAD"].value.count("-") >= 1
        if sp.qform != "ch_verdict" or sp.sampler not in ("S1", "S2"):
            continue
        state = plugin.render(sp, ctx).row["state"]
        by[plugin.solve_a(sp)].append(len(P.NUM_RE.findall(state[state.index("\n\nRequest "):])))
    means = {k: statistics.mean(v) for k, v in by.items()}
    assert len(means) == 3 and max(means.values()) - min(means.values()) < 1.0, means


def test_choice_rows_are_never_deep(base_specs):
    assert not any(sp.deep for sp in base_specs if sp.qform in ("ch_verdict", "ch_failing"))


def test_gold_position_is_exactly_balanced_inside_a_slot_group(plugin, ctx):
    """G0 S28: the scheduled gold positions of the three rows of a verdict triple are 0, 1, 2 once each."""
    seen = collections.defaultdict(list)
    for smp in ("S1", "S3"):
        for seed in range(0, 2 * P.BLOCK_PAIRS):
            sl = P.slot_info(smp, seed)
            if sl["qform"] == "ch_verdict":
                seen[sl["group"]].append(sl["pos"])
    full = [v for v in seen.values() if len(v) == 3]
    assert full and all(sorted(v) == [0, 1, 2] for v in full)
