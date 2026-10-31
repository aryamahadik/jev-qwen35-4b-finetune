"""families/T33/test_i1_fixes.py: fix iteration 1 after the pilot (PILOT_VERDICT F1-F7 and the Stage B kit changes).
In memory only (A37 f). Statistical checks here are small samples with wide bars; the 5,000-row gates run in
pilot_i1_work/scale.py and the pilot itself.

Run (from lean/c2_build):  ../../.venv/bin/python -m pytest -q families/T33/test_i1_fixes.py
  F1   a claim clause with an internal "and" never meets a skin that joins claims with "{Kj} and {Kj+1}"
  F2   R_MAX is drawn first from {1, 2}: the bound does not predict the gold on ch_failed_check
  F3   minimal-edit twins are balanced per question form (yes/no 50/50, ch_claim_verdict 1/3 each)
  F4   double-negation forms: drawn only with a clean wording; polarity rule on the pool; complements pass G-TW
  F6   register first, then the least-loaded skin (a skin feeds at most SKIN_CAP rows); equiv in another register
  F7   both seeds of an antithetic pair carry the same wording
  kit  choice plan: the abstain gold agrees with plan_choice(); no empty JSON result objects; deterministic by seed
"""
from __future__ import annotations

import collections
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot_loaders as PL  # noqa: E402
from c2_kit import pipeline, polarity  # noqa: E402
from c2_kit import plugin as P  # noqa: E402
from c2_kit.choiceplan import plan_choice  # noqa: E402
from c2_kit.lexicon import question_sem  # noqa: E402
from c2_kit.skin import make_skin  # noqa: E402
from families.T33 import fixtures as FX  # noqa: E402
from families.T33 import haiku_author as H  # noqa: E402
from families.T33 import plugin as T  # noqa: E402

TRAIN = ("S1", "S2", "S3", "S4")


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return T.T33Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def specs(plugin):
    return [plugin.sample(seed, smp) for smp in TRAIN for seed in range(1500)]


@pytest.fixture(scope="module")
def frozen():
    with PL.open_family("T33") as kit:
        yield kit


# ------------------------------------------------------------------------------------------------ F1

def test_f1_a_claim_clause_with_and_never_meets_an_and_joined_skin():
    reg = FX.lexicon()
    f = reg.add("I sent the receipt to {T} and logged it", "claim.send", slots={"T": "id"}, family="T33")
    assert reg.unit_test(f.form_id)
    for e in range(f.required):
        reg.record_extraction(f.form_id, f"fixture:and-{e}", f.sem_id)
    plugin = T.T33Plugin(lexicon=reg)
    spec = next(s for s in (plugin.sample(i, "S1") for i in range(200)) if s.structure["sub"] == "b"
                and s.structure["claims"][0]["verb"] == "send" and len(s.structure["claims"]) == 2)
    spec = spec.with_slot("K1", reg.clause(f.form_id, bind={"T": "K1_ENT"}))
    decl = {"K1": "clause", "K2": "clause", "USER": "name"}
    bad = make_skin("S-AND", "T33", "Hi {USER}: {K1} and {K2}.", decl, register="ops_bot")
    ok_comma = make_skin("S-COMMA", "T33", "Hi {USER}: {K1}, and {K2}.", decl, register="ops_bot")
    ok_semi = make_skin("S-SEMI", "T33", "Hi {USER}: {K1}; {K2}.", decl, register="ops_bot")
    assert not plugin._skin_fits(bad, spec)
    assert plugin._skin_fits(ok_comma, spec) and plugin._skin_fits(ok_semi, spec)
    ctx = FX.ctx()
    with pytest.raises(P.ContractError):
        plugin.render(spec, ctx, skin=bad)
    # a clause without "and" is fine next to the and-joined skin
    plain = spec.with_slot("K1", reg.clause(next(fid for fid, x in reg.forms.items() if x.sem_id == "claim.send"
                                                 and " and " not in x.text), bind={"T": "K1_ENT"}))
    assert plugin._skin_fits(bad, plain)


def test_f1_no_and_clause_form_of_the_frozen_pool_is_left_unguarded(frozen):
    plugin, ctx = frozen.plugin, frozen.ctx
    risky = [fid for fid, x in ctx.lexicon.forms.items() if x.sem_id.startswith("claim.") and " and " in x.text
             and ctx.lexicon.status(fid) == "admitted"]
    assert len(risky) >= 8                          # the 8 forms of the verdict (and the latent ones) are in the pool
    joined = [s for s in ctx.skins.values() if s.kind == "skin" and "} and {K" in s.text]
    assert joined
    n = 0
    for seed in range(400):
        spec = plugin.sample(seed, "S1")
        if spec.structure["sub"] != "b":
            continue
        res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
        assert not [p for g, p in res.problems if g == "G3"], res.problems[:2]
        n += 1
    assert n > 100


# ------------------------------------------------------------------------------------------------ F2

def test_f2_the_tries_bound_does_not_predict_the_gold(plugin, specs):
    seen = {1: [0, 0], 2: [0, 0]}
    three_try = 0
    for spec in specs:
        env = spec.env()
        if "R_MAX" in env:
            assert env["R_MAX"] in T.R_MAX_CHOICES
        if spec.qform != "ch_failed_check" or "crit.max_tries" not in spec.structure["checks"]:
            continue
        gold = plugin.solve_a(spec) == "crit.max_tries"
        seen[env["R_MAX"]][0] += 1
        seen[env["R_MAX"]][1] += gold
        it = spec.structure["intent"]["steps"][str(spec.structure["asked"])]
        if gold and env["R_MAX"] == 2:
            assert it["tries"] == 3                   # R_MAX = 2 fails with 3 tries: the episode is built to the need
            three_try += 1
        if gold and env["R_MAX"] == 1:
            assert it["tries"] >= 2
    r = {b: v[1] / v[0] for b, v in seen.items()}
    assert min(v[0] for v in seen.values()) > 200 and three_try > 20, (seen, three_try)
    assert abs(r[1] - r[2]) <= 0.10, r               # 3 sd of this sample; the 5,000-row G7 bar is 3 pp
    assert all(0.15 <= x <= 0.45 for x in r.values()), r


def test_f2_three_try_failures_exist_for_sync_and_async_steps(plugin, specs):
    shapes = collections.Counter()
    for spec in specs:
        for k, it in spec.structure["intent"]["steps"].items():
            if it["tries"] == 3:
                step = next(s for s in spec.structure["steps"] if s["n"] == int(k))
                shapes[("async" if step["async"] else "sync", it["done"])] += 1
    assert {("sync", True), ("sync", False), ("async", True), ("async", False)} <= set(shapes), shapes


# ------------------------------------------------------------------------------------------------ F3

def test_f3_twin_golds_are_balanced_per_form(plugin, specs):
    twins = collections.defaultdict(collections.Counter)
    for spec in specs:
        for prop in plugin.relations(spec):
            if prop.kind == "twin":
                twins[spec.qform][prop.expect if spec.qform != "ch_bad_claim"
                                  else ("none" if prop.expect == "none" else "item")] += 1
    for qf in ("yn_step_ok", "yn_step_failed", "yn_step_not_ok", "yn_all_supported", "yn_any_bad"):
        c = twins[qf]
        n = c[0] + c[1]
        assert n >= 100 and abs(c[1] / n - 0.5) <= 0.10, (qf, dict(c))
    v = twins["ch_claim_verdict"]
    assert sum(v.values()) >= 300 and all(abs(v[k] / sum(v.values()) - 1 / 3) <= 0.07 for k in T.VERDICTS), dict(v)


def test_f3_twins_are_a_fifth_of_the_rows(plugin, ctx):
    rows = collections.Counter()
    for seed in range(250):
        for smp in TRAIN:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            assert res.ok, res.problems[:2]
            rows.update(r["role"] for r in res.rows)
    n = sum(rows.values())
    assert 0.17 <= rows["twin"] / n <= 0.27, rows
    assert 0.04 <= rows["equiv"] / n <= 0.10, rows


# ------------------------------------------------------------------------------------------------ F4

def test_f4_double_negation_forms_have_the_declared_shape(plugin):
    for qf, pos in (("yn_dneg_step_ok", "yn_step_ok"), ("yn_dneg_all_supported", "yn_all_supported")):
        q, p = plugin.QFORMS[qf], plugin.QFORMS[pos]
        assert q.qtype == "noul" and q.polarity == 1 and q.predicate == p.predicate and q.yes_is_bad is False
        assert T.DNEG_FALLBACK[qf] == pos
    sums = collections.Counter()
    for q, share in T.QFORM_SHARES:
        sums[T.SUB_OF[q]] += share
    assert abs(sum(sums.values()) - 1.0) < 1e-9
    shares = dict(T.QFORM_SHARES)
    yn = sum(v for q, v in shares.items() if plugin.QFORMS[q].qtype == "noul")
    assert (shares["yn_dneg_step_ok"] + shares["yn_dneg_all_supported"]) / yn >= 0.05
    for a, partners in T.PARTNERS.items():
        assert abs(sum(s for _q, s in partners) - 1.0) < 1e-9
        for b, _s in partners:
            assert plugin.QFORMS[a].predicate == plugin.QFORMS[b].predicate
            assert plugin.QFORMS[a].polarity == -plugin.QFORMS[b].polarity


def test_f4_dneg_rows_pass_every_gate_and_gold_means_the_step_meets_it(plugin, ctx):
    n = collections.Counter()
    for seed in range(400):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            if spec.qform not in T.DNEG_FALLBACK:
                continue
            res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
            assert res.ok, res.problems[:2]
            twin_pos = spec.replace(qform=T.DNEG_FALLBACK[spec.qform])
            assert plugin.solve_a(spec) == plugin.solve_a(twin_pos)               # yes iff the positive form says yes
            n[spec.qform] += 1
            n["pairs"] += sum(r["role"] == "complement" for r in res.rows)
    assert n["yn_dneg_step_ok"] > 15 and n["yn_dneg_all_supported"] > 15 and n["pairs"] > 5


def test_f4_without_a_clean_wording_the_positive_form_is_drawn():
    ctx0 = FX.ctx(dneg=False)
    p0 = T.T33Plugin(lexicon=ctx0.lexicon)
    assert p0.dneg_ok == {"yn_dneg_step_ok": False, "yn_dneg_all_supported": False}
    seen = collections.Counter()
    for seed in range(300):
        for smp in TRAIN:
            spec = p0.sample(seed, smp)
            seen[spec.qform] += 1
            for prop in p0.relations(spec):
                assert prop.qform not in T.DNEG_FALLBACK
            if seed < 40:
                assert pipeline.build_unit(p0, spec, ctx0, run_g15=False).ok
    assert not set(seen) & set(T.DNEG_FALLBACK) and seen["yn_step_ok"] > 100 and seen["yn_all_supported"] > 100


def test_f4_the_polarity_rule_screens_the_pool_and_the_pipeline(plugin, ctx):
    texts = {"W-CONTR": ("yn_step_not_ok", "Doesn't step {STEP} on the log meet its success criterion?"),
             "W-MIXED": ("yn_dneg_step_ok", "Is it not true that step {STEP} of the log does not break its criterion?"),
             "W-FINE": ("yn_step_not_ok", "Does step {STEP} of the log not meet its success criterion?")}
    skins = dict(ctx.skins)
    reg = ctx.lexicon
    for wid, (qf, text) in texts.items():
        f = reg.add(text, question_sem("T33", qf), slots={"STEP": "count"}, family="T33")
        reg.unit_test(f.form_id)
        for e in range(f.required):
            reg.record_extraction(f.form_id, f"fixture:pol-{wid}-{e}", f.sem_id)
        skins[wid] = make_skin(wid, "T33", text, {"STEP": "count"}, kind="wording", register="question", qform=qf,
                               lexicon_ids=(f.form_id,))
    c2 = P.KitCtx(skins=skins, lexicon=reg)
    p2 = T.T33Plugin(lexicon=reg)
    bad = p2.quarantined_wordings(c2)
    assert set(bad) == {"W-CONTR", "W-MIXED"}
    assert any(x.startswith("P3") for x in bad["W-CONTR"]) and any(x.startswith("P1") for x in bad["W-MIXED"])
    assert polarity.form_problems(T.T33Plugin, "yn_step_not_ok", texts["W-FINE"][1]) == []
    # a quarantined wording that reaches a row fails G-LEX
    spec = next(s for s in (p2.sample(i, "S1") for i in range(300)) if s.qform == "yn_step_not_ok")
    rr = p2.render(spec, c2, wording=c2.skin("W-CONTR"))
    probs = pipeline.check_rendered(p2, spec, rr, c2, run_g15=False)
    assert any(g == "G-LEX" and "W-CONTR" in d and "polarity" in d for g, d in probs)
    # and render never picks one
    for i in range(200):
        sp = p2.sample(i, "S1")
        if sp.qform in ("yn_step_not_ok", "yn_dneg_step_ok"):
            assert p2.render(sp, c2).wording_id not in bad


def test_f4_the_frozen_pool_loses_only_the_contracted_wording(frozen):
    plugin, ctx = frozen.plugin, frozen.ctx
    bad = plugin.quarantined_wordings(ctx)
    assert set(bad) == {"T33-wor-4c252dcc00"}                   # W1 of the verdict: "Doesn't step N ... meet ...?"
    assert any(p.startswith("P3") for p in bad["T33-wor-4c252dcc00"])
    # nothing else changes: every other yes/no wording of the pool passes the rule
    assert plugin.dneg_ok == {"yn_dneg_step_ok": False, "yn_dneg_all_supported": False}
    for sid, sk in ctx.skins.items():
        if sk.kind == "wording" and sid not in bad:
            assert polarity.form_problems(plugin, sk.qform, sk.text) == [], sid
    for seed in range(60):
        assert plugin.sample(seed, "S1").qform not in T.DNEG_FALLBACK


def test_f4_the_authoring_brief_asks_for_the_safe_shape_only():
    for qf in T.DNEG_FALLBACK:
        text, sub = H.WORDING_BRIEFS[qf]
        assert "is it not true that" in text and "is it not the case that" in text and "contracted" in text
        assert "exactly two" in text and "negative meaning of its own" in text
        for f in H.FORBID:                                       # label-blind briefs (the chunker enforces it too)
            assert not re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", text.lower()), f
    assert H.NEG_COUNTS["yn_dneg_step_ok"] == H.NEG_COUNTS["yn_dneg_all_supported"] == (2, 2)
    assert H.TARGETS["wording"]["yn_dneg_step_ok"] >= 8 and H.TARGETS["wording"]["yn_dneg_all_supported"] >= 8
    assert H.WORDING_ITEMS["yn_dneg_step_ok"] * H.FORMS_PER_ITEM >= 16
    assert len(H.task_list(H.build_batches())) <= H.MAX_TASKS
    dn = H.build_dneg_batches()                                  # the iteration-1 chunks: the two forms only
    assert len(H.task_list(dn)) == 1 and {b.key[q].split("|")[2] for _n, b in dn for q in b.key} == set(T.DNEG_FALLBACK)
    assert all(c["answer_file"].startswith(str(H.AUTHOR_I1)) for _n, b in dn for c in b.chunks)
    # the loader refuses the three failure modes of the T35 pilot (contracted frame, negation over a negative word,
    # a lone negation) and keeps the explicit frame
    reg = H.registry()
    for text, ok in (("Is it not true that step {STEP} of the log does not meet its success criterion?", True),
                     ("Isn't it true that step {STEP} does not meet its criterion?", False),
                     ("Is it not true that step {STEP} of the log does not meet its criterion, or breaks it?", False),
                     ("Does step {STEP} of the log not meet its success criterion?", False)):
        got = H._load_one("wordings", ["t33", "wording", "yn_dneg_step_ok", "0"], text, "t33|wording|yn_dneg_step_ok|0",
                          "tid", "psha", reg)
        assert (got is not None and not isinstance(got, str)) == ok, (text, got)


# ------------------------------------------------------------------------------------------------ F6 / F7

def test_f7_both_seeds_of_a_pair_carry_the_same_wording(plugin, ctx):
    n = 0
    for smp in TRAIN:
        for m in range(60):
            a, b = plugin.sample(2 * m, smp), plugin.sample(2 * m + 1, smp)
            assert a.qform == b.qform
            ra, rb = plugin.render(a, ctx), plugin.render(b, ctx)
            assert ra.wording_id == rb.wording_id
            if a.qform != "ch_failed_check" and plugin.QFORMS[a.qform].qtype == "noul":
                assert ra.row["gold"] + rb.row["gold"] == 1          # opposite golds under one wording
            n += 1
    assert n == 240


def test_f7_wordings_are_used_evenly_and_partners_share_the_pair_wording(plugin, ctx):
    plugin.reset_balance()
    for smp in TRAIN:
        for m in range(150):
            plugin.render(plugin.sample(2 * m, smp), ctx)
    by_form = collections.defaultdict(list)
    for sid, n in plugin._wording_load.items():
        by_form[ctx.skin(sid).qform].append(n)
    assert len(by_form) == len(T.SUB_OF)
    for qf, uses in by_form.items():
        assert max(uses) - min(uses) <= 1, (qf, uses)          # the least-used wording is drawn: counts never drift apart
    c2 = plugin.ctx_for(None, ctx)
    a = c2.pick(T.FAMILY, "wording", "T33|10|S1|yn_step_ok", qform="yn_step_failed")
    b = c2.pick(T.FAMILY, "wording", "T33|11|S1|yn_step_ok", qform="yn_step_failed")
    assert a.skin_id == b.skin_id                              # a complement partner reads one wording in both seeds
    assert c2.pick(T.FAMILY, "wording", "some other key", qform="yn_step_failed").qform == "yn_step_failed"
    plugin.reset_balance()


def test_f6_registers_and_skins_are_balanced_on_the_frozen_pool(frozen):
    plugin, ctx = frozen.plugin, frozen.ctx
    plugin.reset_balance()
    regs, skins = collections.defaultdict(collections.Counter), collections.Counter()
    n = 0
    for seed in range(450):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            regs[spec.structure["sub"]][rr.register] += 1
            skins[rr.skin_id] += 1
            n += 1
    assert plugin.SKIN_CAP == 6.0 and max(plugin._skin_load.values()) <= plugin.SKIN_CAP + 1e-9
    for sub, c in regs.items():
        tot = sum(c.values())
        assert len(c) == (4 if sub == "a" else 6)
        # shares follow the skin counts (the skin cap needs it): a: 126 / 131 / 126 / 71 skins, b: 108-120 each
        assert max(c.values()) / tot <= (0.32 if sub == "a" else 0.20), (sub, dict(c))   # of the sub-form's units
        assert min(c.values()) / tot >= (0.12 if sub == "a" else 0.12), (sub, dict(c))
    assert max(skins.values()) <= 3, skins.most_common(3)         # 1,800 units over 1,131 skins: the walk spreads them
    plugin.reset_balance()


def test_f6_one_key_one_skin_and_equiv_changes_register(frozen):
    plugin, ctx = frozen.plugin, frozen.ctx
    plugin.reset_balance()
    n = 0
    for seed in range(300):
        spec = plugin.sample(seed, "S1")
        if spec.structure["sub"] != "a":
            continue
        r1 = plugin.render(spec, ctx)
        assert plugin.render(spec, ctx).skin_id == r1.skin_id               # the same key renders with the same skin
        for prop in plugin.relations(spec):
            if prop.kind == "equiv":
                assert prop.register != r1.register and prop.register in T.EQUIV_REGISTERS
                n += 1
    assert n > 8
    plugin.reset_balance()


# ------------------------------------------------------------------------------------------------ kit adoption

def test_choice_rows_follow_the_plan_drawn_before_the_structure(plugin, specs):
    seen = collections.Counter()
    for spec in specs:
        if spec.qform == "ch_failed_check":
            plan = plan_choice(plugin._okey(spec.sampler, spec.seed, spec.qform), closed=len(spec.structure["checks"]),
                               abstain=True)
        elif spec.qform == "ch_bad_claim":
            plan = plan_choice(plugin._okey(spec.sampler, spec.seed, spec.qform),
                               closed=len(spec.structure["claims"]), abstain=True)
        else:
            continue
        assert (plugin.solve_a(spec) == "none") == plan.gold_abstain, (spec.sampler, spec.seed)
        seen[(spec.qform, plan.k)] += 1
    assert len(seen) >= 4 and min(seen.values()) > 20, seen


def test_the_none_gold_share_is_one_over_k_on_base_rows(plugin, specs):
    cell = collections.defaultdict(lambda: [0, 0.0])
    for spec in specs:
        if spec.qform in ("ch_failed_check", "ch_bad_claim"):
            k = (len(spec.structure["checks"]) if spec.qform == "ch_failed_check" else len(spec.structure["claims"])) + 1
            c = cell[(spec.qform, k)]
            c[0] += plugin.solve_a(spec) == "none"
            c[1] += 1
    for (qf, k), (hit, n) in cell.items():
        if n >= 150:
            assert abs(hit / n - 1 / k) <= 0.07, (qf, k, hit, n)


def test_log_lines_print_no_empty_result_object(plugin, ctx, specs):
    n = 0
    for spec in [s for s in specs if s.structure["fmt"] == "jsonl"][:300]:
        text = plugin.render(spec, ctx).row["state"]
        assert '"result":{}' not in text
        for line in text.split("\n")[1:]:
            if line.startswith("{"):
                json.loads(line)
                n += 1
    assert n > 500


def test_generation_is_identical_under_two_hash_seeds():
    script = (
        "import sys, json, hashlib\n"
        f"sys.path.insert(0, {str(C2_BUILD)!r})\n"
        "sys.dont_write_bytecode = True\n"
        "from c2_kit import pipeline\n"
        "from families.T33 import fixtures as FX, plugin as T\n"
        "ctx = FX.ctx(); p = T.T33Plugin(lexicon=ctx.lexicon)\n"
        "rows = []\n"
        "for seed in range(24):\n"
        "    for smp in ('S1', 'S2', 'S3', 'S4'):\n"
        "        res = pipeline.build_unit(p, p.sample(seed, smp), ctx, run_g15=False)\n"
        "        rows += res.rows\n"
        "print(hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest(), len(rows))\n")
    outs = []
    for hs in ("1", "4242"):
        r = subprocess.run([sys.executable, "-B", "-c", script], capture_output=True, text=True,
                           env={"PYTHONHASHSEED": hs, "PATH": "/usr/bin:/bin"}, timeout=600)
        assert r.returncode == 0, r.stderr[-800:]
        outs.append(r.stdout.strip())
    assert outs[0] == outs[1] and int(outs[0].split()[1]) > 100, outs
