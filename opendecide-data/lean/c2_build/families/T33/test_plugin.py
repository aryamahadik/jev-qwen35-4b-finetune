"""families/T33/test_plugin.py: in-memory tests for T33 (A37 f: nothing is written; no Haiku, no network).

Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T33
  contract     validate_plugin(strict) == [], solver-B independence, G0-lite frozen and <= 200 lines
  G2 / G3      solver A == solver B and parse == canonical on 5,000 sampled specs (1,000 per sampler)
  pipeline     whole relation units through G2, G3, G4, G-SL, G-LEX, G-TW (G15 on a sample); overlay shares
  relations    twins change exactly one input slot and the answer moves to the construction's prediction;
               complements are opposite; G4 metamorphic proposals keep the answer
  balance      2,000 specs: yes/no gold 50/50, choice gold shares, None wrong on >= 50% of the rows showing it,
               yes = bad outcome, gold positions, label-free metadata (log length, claim count), registers
  G-SL         every built-in placeholder skin / wording / attack lints clean; no gold-label word and no slot value
               outside slot spans in the state; injected leaks are caught
  determinism  same seed, same spec and rows
  bugs         injected solver-B, solver-A, renderer and twin bugs are caught by G2 / G3 / G-TW / the construction check
"""
from __future__ import annotations

import collections
import dataclasses
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
from c2_kit import plugin as P  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.distractors import abstain_report, position_counts  # noqa: E402
from c2_kit.relations import RelationEmitter, masked, slot_diff  # noqa: E402
from families.T33 import cardtext as CT  # noqa: E402
from families.T33 import fixtures as FX  # noqa: E402
from families.T33 import plugin as T  # noqa: E402
from families.T33 import solver_b as B  # noqa: E402


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return T.T33Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def specs2000(plugin):
    return [plugin.sample(seed, smp) for smp in plugin.SAMPLERS for seed in range(400)]


# ------------------------------------------------------------------------------------------------ contract

def test_plugin_meets_the_contract_strictly(plugin):
    assert P.validate_plugin(plugin, strict=True) == []
    assert P.check_independence(plugin) == []
    assert len(plugin.G0_LITE.read_text(encoding="utf-8").splitlines()) <= 200
    assert plugin.PARADIGM_A == "simulator" and plugin.PARADIGM_B == "sql_sqlite"


def test_lexicon_forms_pass_their_unit_tests_and_are_admitted(ctx):
    reg = ctx.lexicon
    assert all(f.unit_ok for f in reg.forms.values()), {f.text: f.unit_problems for f in reg.forms.values()
                                                         if not f.unit_ok}
    assert reg.gate()["pass"]


def test_no_admitted_form_means_no_sample():
    ctx0 = FX.ctx(admit=False)
    with pytest.raises(P.ContractError):
        for seed in range(20):
            T.T33Plugin(lexicon=ctx0.lexicon).sample(seed, "S1")


# ------------------------------------------------------------------------------------------------ G2 / G3

def test_solver_a_equals_solver_b_and_g3_on_5000_specs(plugin, ctx):
    n, problems = 0, []
    for smp in plugin.SAMPLERS:
        for seed in range(1000):
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            view = plugin.parse(rr.row, ctx)
            a, b = plugin.solve_a(spec), plugin.solve_b(view)
            facts = {k: v for k, v in view.items() if k != "options"}
            if a != b or rr.answer != a:
                problems.append(("G2", smp, seed, spec.qform, a, b))
            if facts != plugin.canonical_for(spec, "T"):
                problems.append(("G3", smp, seed))
            if rr.row["qtype"] == "choice":
                keys = view["options"]
                if keys[rr.row["options"].index(rr.row["gold"])] != b or len(set(map(repr, keys))) != len(keys):
                    problems.append(("options", smp, seed))
            if R.validate_row(rr.row):
                problems.append(("schema", smp, seed, R.validate_row(rr.row)))
            n += 1
    assert n == 5000
    assert problems == [], problems[:10]


def test_every_sampler_passes_every_program_gate(plugin, ctx):
    units, stats = [], collections.Counter()
    for seed in range(120):
        for smp in plugin.SAMPLERS:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=(seed < 8))
            assert res.ok, (seed, smp, res.problems)
            units.append(res)
            for r in res.rows:
                stats[r["role"]] += 1
                assert r["meta"]["dev_only"] == (smp == "S5" or r["meta"]["c2"]["register"] in
                                                 plugin.HELD_OUT_REGISTERS)
    rep = pipeline.overlay_report(units, plugin)
    assert rep["complement_share_of_yes_no"] >= 0.20
    assert rep["non_syntactic_share_of_pairs"] >= 0.30
    assert 0.15 <= rep["twin_share"] <= 0.30, rep["twin_share"]
    assert 0.03 <= rep["equiv_share"] <= 0.10, rep["equiv_share"]
    assert 0.02 <= rep["attack_share"] <= 0.08, rep["attack_share"]
    assert 0.45 <= rep["yes_rate"] <= 0.55
    assert rep["abstain"]["pass"]
    assert all(stats[k] for k in ("base", "complement", "twin", "equiv", "attack"))


# ------------------------------------------------------------------------------------------------ relations

def test_twins_change_one_slot_and_move_the_answer_as_constructed(plugin, specs2000):
    kinds, n = collections.Counter(), 0
    for spec in specs2000:
        for prop in plugin.relations(spec):
            if prop.kind != "twin":
                continue
            twin = plugin.derive(prop.spec)
            assert slot_diff(spec, twin) == {prop.changed_slot}
            assert plugin.solve_a(twin) == prop.expect != plugin.solve_a(spec), (spec.sampler, spec.seed)
            kinds[re.sub(r"\d+", "", prop.changed_slot)] += 1
            n += 1
    assert n >= 600
    assert {"L_STATE", "L_CODE", "L_VAL", "R_MAX", "D_MAX", "K_VAL", "K_ENT"} <= set(kinds), kinds


def test_twins_render_identically_outside_the_changed_slot(plugin, ctx, specs2000):
    checked = 0
    for spec in specs2000[:600]:
        for prop in plugin.relations(spec):
            if prop.kind != "twin":
                continue
            rr = plugin.render(spec, ctx)
            twin = plugin.derive(prop.spec)
            rt = plugin.render(twin, ctx, skin=ctx.skin(rr.skin_id), wording=ctx.skin(rr.wording_id),
                               forms=pipeline._forms_for(twin, rr.forms, "k", {prop.changed_slot}))
            em = RelationEmitter(plugin)
            em.base(rr)
            em.twin(rr, rt, spec, twin, prop.changed_slot, prop.expect)       # raises GTWError on any breach
            checked += 1
    assert checked >= 150


def test_complements_are_opposite_and_metamorphic_relations_keep_the_answer(plugin, specs2000):
    pairs = 0
    for spec in specs2000:
        a = plugin.solve_a(spec)
        for q2, _share in T.PARTNERS.get(spec.qform, ()):
            q, p2 = plugin.QFORMS[spec.qform], plugin.QFORMS[q2]
            assert q.predicate == p2.predicate and q.polarity == -p2.polarity
            assert a + plugin.solve_a(spec.replace(qform=q2)) == 1
            pairs += 1
        for prop in plugin.relations(spec):
            if prop.kind == "metamorphic":
                assert plugin.solve_a(plugin.derive(prop.spec)) == a, prop.note
    assert pairs >= 900


# ------------------------------------------------------------------------------------------------ balance

def test_gold_balance_on_2000_specs(plugin, ctx, specs2000):
    yes, n = collections.Counter(), collections.Counter()
    gold = collections.defaultdict(collections.Counter)
    lines, claims, sets, regs = collections.defaultdict(list), collections.defaultdict(list), [], collections.Counter()
    yes_is_bad = 0
    for spec in specs2000:
        q = plugin.QFORMS[spec.qform]
        a = plugin.solve_a(spec)
        if q.qtype == "noul":
            yes[spec.qform] += a
            n[spec.qform] += 1
            yes_is_bad += bool(q.yes_is_bad)
            lines[a].append(len(spec.structure["lines"]))
            if spec.structure["sub"] == "b":
                claims[a].append(len(spec.structure["claims"]))
        else:
            gold[spec.qform]["none" if a == "none" else (a if spec.qform == "ch_claim_verdict" else "item")] += 1
            rr = plugin.render(spec, ctx)
            sets.append(rr.option_set)
            regs[rr.register] += 1
    n_yn = sum(n.values())
    assert sum(yes.values()) / n_yn == 0.5                          # antithetic pairs: exact by construction
    for qf in n:
        assert yes[qf] / n[qf] == 0.5, qf                         # per question form and sampler stream too
    assert 0.45 <= yes_is_bad / n_yn <= 0.55
    assert 0.40 <= n_yn / len(specs2000) <= 0.50                    # yes/no base rows (complements add more)
    subs = collections.Counter(s.structure["sub"] for s in specs2000)
    assert abs(subs["a"] / len(specs2000) - 0.464) <= 0.04        # base 46.4 / 53.6: the overlay is (a)-heavy, so ROWS are 50 / 50
    for qf in ("ch_failed_check", "ch_bad_claim"):
        share = gold[qf]["none"] / sum(gold[qf].values())
        assert 0.22 <= share <= 0.38, (qf, share)
    v = gold["ch_claim_verdict"]
    assert all(0.26 <= v[k] / sum(v.values()) <= 0.41 for k in T.VERDICTS), v
    assert abstain_report(sets)["pass"]
    for k, counts in position_counts(sets).items():
        if sum(counts) >= 150:               # k = 5 has about 60 rows in 2,000 specs: too few for a +-12 pp bar
            assert max(counts) / sum(counts) - 1 / k <= 0.12, (k, counts)
    assert abs(statistics.mean(lines[1]) - statistics.mean(lines[0])) <= 0.5      # G6 metadata: log length
    assert abs(statistics.mean(claims[1]) - statistics.mean(claims[0])) <= 0.25   # claim count
    assert max(regs.values()) / sum(regs.values()) <= 0.15


def test_trap_shares_and_depth(specs2000):
    tags = collections.Counter(t for s in specs2000 for t in s.tags)
    n = len(specs2000)
    targets = {"status_2xx_unfinished": 0.25, "retry_then_success": 0.15, "cents_trap": 0.15, "claim_no_call": 0.15,
               "value_other_entity": 0.10, "silent_success": 0.10}
    for t, share in targets.items():
        assert 0.5 * share <= tags[t] / n <= 2 * share, (t, tags[t] / n)
    assert tags["partial_write"] and tags["boundary"] and tags["ms_vs_seconds"]
    assert sum(s.deep for s in specs2000) / n <= 0.10
    assert max(len(s.structure["lines"]) for s in specs2000) <= T.MAX_LINES


def test_rows_stay_under_the_length_cap(plugin, ctx, specs2000):
    toks = [R.approx_tokens(plugin.render(s, ctx).row) for s in specs2000[::4]]
    assert max(toks) <= R.MAX_TOKENS
    assert statistics.mean(toks) <= 1000          # measured ~890 real Qwen tokens; spec family mean 800 is open


# ------------------------------------------------------------------------------------------------ G-SL

def test_builtin_skins_wordings_and_attacks_lint_clean(plugin, ctx):
    for sk in ctx.skins.values():
        v = gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                              name_allow=plugin.NAME_ALLOW)
        assert v == [], (sk.skin_id, v)


def test_no_gold_label_word_or_slot_value_outside_slot_spans(plugin, ctx, specs2000):
    label_re = re.compile(r"(?<![a-z])(?:" + "|".join(sorted(gsl._label_forms(plugin.LABEL_WORDS) | {"not shown"},
                                                             key=len, reverse=True)) + r")(?![a-z])", re.I)
    for spec in specs2000[::5]:
        rr = plugin.render(spec, ctx)
        outside = masked(rr, "state", set(spec.all_slots())).replace("\x00", " ")
        assert not label_re.search(outside), (spec.sampler, spec.seed, label_re.search(outside))
        for name, slot in spec.all_slots().items():
            if slot.kind in ("id", "name") or (slot.kind in ("cents", "count") and slot.value >= 1000):
                for form in S.forms(slot):
                    text = S.render(slot, form)
                    assert not re.search(r"(?<![\w.$,])" + re.escape(text) + r"(?![\w,])", outside), (name, text)
        for v in gsl.check_row(rr, ctx, plugin, spec):
            pytest.fail(f"G-SL {v}")


def test_gsl_catches_leaky_skins(plugin, ctx):
    spec = next(s for s in (plugin.sample(i, "S1") for i in range(40)) if s.structure["sub"] == "b")
    base = next(sk for sk in ctx.skins.values() if plugin._skin_fits(sk, spec) and not sk.held_out)
    for leak in (" The refund failed.", " Every claim here is supported.", " It will settle tomorrow.",
                 " Order 4471 is fine."):
        bad = dataclasses.replace(base, skin_id="LEAK", text=base.text + leak)
        c2 = dataclasses.replace(ctx, skins={**ctx.skins, "LEAK": bad})
        rr = plugin.render(spec, c2, skin=bad)
        assert any(g == "G-SL" for g, _ in pipeline.check_rendered(plugin, spec, rr, c2, run_g15=False)), leak


# ------------------------------------------------------------------------------------------------ determinism

def test_generation_is_deterministic_by_seed(plugin, ctx):
    for smp in plugin.SAMPLERS:
        a, b = plugin.sample(11, smp), plugin.sample(11, smp)
        assert a.structure_hash() == b.structure_hash() and a.facts() == b.facts()
        assert plugin.render(a, ctx).row == plugin.render(b, ctx).row
        assert (pipeline.build_unit(plugin, a, ctx, run_g15=False).rows
                == pipeline.build_unit(plugin, b, ctx, run_g15=False).rows)
    hashes = {plugin.sample(seed, "S1").structure_hash() for seed in range(200)}
    assert len(hashes) == 200


def test_wrong_options_are_error_model_outputs(plugin, ctx, specs2000):
    models = plugin.error_models()
    seen = 0
    for spec in specs2000:
        if plugin.QFORMS[spec.qform].qtype != "choice":
            continue
        rr = plugin.render(spec, ctx)
        for o in rr.option_set.options:
            for name in o.err:
                assert models[name].fn(spec) == o.key, (name, o.key)
                seen += 1
    assert seen >= 300


# ------------------------------------------------------------------------------------------------ injected bugs

def _gate_failures(plugin, ctx, n=40):
    out = collections.Counter()
    for seed in range(n):
        for smp in ("S1", "S2", "S3"):
            try:
                spec = plugin.sample(seed, smp)
            except P.ContractError:
                out["construction"] += 1
                continue
            for g, _ in pipeline.build_unit(plugin, spec, ctx, run_g15=False).problems:
                out[g] += 1
    return out


def test_g2_catches_a_solver_b_that_trusts_202(plugin, ctx, monkeypatch):
    monkeypatch.setattr(B, "FACTS_SQL", B.FACTS_SQL.replace("t.status IN (200, 201, 204)",
                                                            "t.status IN (200, 201, 202, 204)"))
    assert _gate_failures(plugin, ctx)["G2"] > 0


def test_construction_check_catches_a_solver_a_that_ignores_409(plugin, ctx, monkeypatch):
    real = T.T33Plugin._replay
    monkeypatch.setattr(T.T33Plugin, "_replay", lambda self, spec, env, flaws: real(
        self, spec, env, frozenset(flaws) | {"conflict_as_failure"}))
    f = _gate_failures(plugin, ctx)
    assert f["construction"] + f["G2"] > 0


def test_g2_catches_mislabelled_verdict_options(plugin, ctx, monkeypatch):
    monkeypatch.setitem(T.VERDICT_TEXT, "supported", "Contradicted by the log")
    monkeypatch.setitem(T.VERDICT_TEXT, "contradicted", "Supported by the log")
    assert _gate_failures(plugin, ctx)["G2"] > 0


def test_g3_catches_a_renderer_that_prints_the_wrong_fact(plugin, ctx, monkeypatch):
    real = T.T33Plugin._line_tpl
    monkeypatch.setattr(T.T33Plugin, "_line_tpl", staticmethod(
        lambda fmt, ln, i, arch: real(fmt, ln, i, arch).replace("{S" + str(ln["step"]) + "_KEY}",
                                                               "{S" + str(ln["step"]) + "_TOOL}")))
    assert _gate_failures(plugin, ctx)["G3"] > 0


def test_gtw_catches_a_wrong_twin_prediction(plugin, ctx, monkeypatch):
    real = T.T33Plugin._twin

    def wrong(self, spec):
        prop = real(self, spec)
        if prop is not None:
            prop.expect = (1 - prop.expect) if prop.expect in (0, 1) else ("none" if prop.expect != "none" else "x")
        return prop
    monkeypatch.setattr(T.T33Plugin, "_twin", wrong)
    assert _gate_failures(plugin, ctx, n=80)["G-TW"] > 0


def test_gtw_catches_a_twin_that_changes_two_slots(plugin, ctx, monkeypatch):
    real = T.T33Plugin._twin

    def two(self, spec):
        prop = real(self, spec)
        if prop is not None:
            prop.spec = prop.spec.with_slot("USER", S.name_slot("Zora Quill"))
        return prop
    monkeypatch.setattr(T.T33Plugin, "_twin", two)
    assert _gate_failures(plugin, ctx, n=80)["G-TW"] > 0


def test_solver_b_drops_a_claim_that_binds_to_two_steps(plugin, ctx):
    spec = next(s for s in (plugin.sample(i, "S1") for i in range(60))
                if s.structure["sub"] == "b" and len(s.structure["steps"]) >= 2)
    view = plugin.parse(plugin.render(spec, ctx).row, ctx)
    view["steps"][1][2] = view["steps"][0][2]                      # two steps now share one target
    view["claims"][0][1] = view["steps"][0][2]
    with pytest.raises(B.BindError):
        B.solve_b(view)


# ------------------------------------------------------------------------------------------------ review fixes

def test_failed_check_rows_list_finished_first_and_balance_check_types(plugin, ctx):
    """Two review fixes on ch_failed_check. (1) A failed or running money job prints its amount on every poll and a
    running bulk job may print every row, so a value check can hold (S7) on a step that is not done; listed before
    "finished", the card's first failing check was "finished" while a natural reader answers the value check. Now
    crit.finished is listed first on every ch_failed_check row (base and twins). (2) The check TYPE predicted the gold
    (max_tries gold on 13% of its showings, max_duration 41%): the first failing check is drawn uniformly over the
    listed checks + None from the seed and the checks stay fixed while plans are drawn; twins onto "finished" or a
    value check are thinned. Over all emitted rows every type is gold within 5 pp of 1 / k."""
    shown, gold, chance = collections.Counter(), collections.Counter(), collections.Counter()
    for seed in range(2400):
        for smp in ("S1", "S2", "S3", "S4"):
            spec = plugin.sample(seed, smp)
            if spec.qform != "ch_failed_check":
                continue
            res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
            assert res.ok, res.problems[:3]
            for rr in res.rendered:
                if rr.row["qtype"] != "choice":
                    continue
                assert spec.structure["checks"][0] == "crit.finished"
                for o in rr.option_set.options:
                    shown[o.key] += 1
                    gold[o.key] += o.role == "gold"
                    chance[o.key] += 1 / len(rr.option_set.options)
    assert set(shown) >= {"none", "crit.finished", "crit.max_tries", "crit.max_duration", "crit.amount_match",
                          "crit.all_written"}
    for key, n in shown.items():           # a 2,400-seed sample: sd about 2 pp at n = 500; the scale run checks 1.5 pp
        assert n >= 200 and abs(gold[key] / n - chance[key] / n) <= 0.07, (key, gold[key] / n, chance[key] / n)


def test_choice_logs_hold_a_seed_drawn_unfinished_count_and_every_verdict_once(specs2000):
    """G0 section 12 (amendment w9, A52 d fix round). The card view (G6 c, no question) found that a failed / running /
    queued step or a 4xx status in a choice log predicted the gold: the decisive step was the only unfinished one. The number
    of UNFINISHED steps of a ch_failed_check / ch_bad_claim log is now drawn from the row seed alone (never from the label or
    the rng stream), so the bag of failure cues is the same for every gold; a ch_claim_verdict log always holds three claims,
    one supported, one contradicted, one not shown (the question picks which)."""
    seen = collections.Counter()
    for spec in specs2000:
        st = spec.structure
        if spec.qform not in ("ch_failed_check", "ch_bad_claim", "ch_claim_verdict"):
            continue
        steps = st["intent"]["steps"]
        unf = sum(not v["done"] for v in steps.values())
        if spec.qform == "ch_failed_check":
            assert unf == T._unf_target(spec.sampler, spec.seed, len(steps) - 1, "fcc"), (spec.sampler, spec.seed)
        elif spec.qform == "ch_bad_claim":
            assert unf == T._unf_target(spec.sampler, spec.seed, len(steps) - len(st["claims"]), "bad"), (spec.sampler, spec.seed)
        else:
            assert len(st["claims"]) == 3 and sorted(st["intent"]["verdicts"]) == sorted(T.VERDICTS), (spec.sampler, spec.seed)
        assert 1 <= unf <= 3 or spec.qform == "ch_claim_verdict"
        seen[spec.qform] += 1
    assert min(seen.values()) >= 100 and len(seen) == 3, seen


# ------------------------------------------------------------------------------------------------ amb:T33 resolutions

def test_many_packs_one_pack_per_card_and_stream_subsets(ctx):
    """G0 S1 (amb:T33 R-S1): with the Haiku pack pool (>= 25 packs) each (sampler, sub-form) stream draws from a fixed
    seeded subset of PACKS_PER_STREAM packs, one pack per card, so cards stay near 30-45 rows; packs need a money, a
    bulk and an action tool; pack voices are a label-blind preference only."""
    base = list(T.PACKS.values())
    packs = {f"pk{i:02d}": tuple((f"ns{i}.{t.split('.')[1]}", v, k) for t, v, k in base[i % len(base)])
             for i in range(30)}
    voices = {n: ("ops_bot",) for n in packs}
    p = T.T33Plugin(lexicon=ctx.lexicon, packs=packs, voices=voices)
    cards, used = collections.defaultdict(set), set()
    for smp in ("S1", "S2", "S3", "S4"):
        for seed in range(240):
            spec = p.sample(seed, smp)
            sub = spec.structure["sub"]
            assert spec.pack in p.stream_packs(smp, sub) and spec.card_id == f"T33:{smp}:{sub}:{spec.pack}"
            cards[(smp, sub)].add(spec.pack)
            used.add(spec.pack)
            env = spec.env()
            assert all(env[f"S{s['n']}_TOOL"].startswith(f"ns{int(spec.pack[2:])}.") for s in spec.structure["steps"])
            assert plugin_rows_ok(p, spec, ctx)
    assert all(len(v) <= T.PACKS_PER_STREAM for v in cards.values())
    assert len(used) >= 25
    with pytest.raises(P.ContractError):
        T.T33Plugin(lexicon=ctx.lexicon, packs={"bad": (("x.send_note", "send", "contact"),)})


def plugin_rows_ok(p, spec, ctx) -> bool:
    rr = p.render(spec, ctx)
    view = p.parse(rr.row, ctx)
    return p.solve_b(view) == p.solve_a(spec) == rr.answer


def test_card_states_the_resolved_rules(plugin, ctx):
    """amb:T33: the card names poll status 200 as meaningless, lines as time-ordered, 409 as done, the result field,
    the lowest-numbered failing check, the per-step not-shown test and the attack-line rule (only the log is
    evidence); no option_framing wording uses "leaves out". The block is need-to-know and has two drawn styles (compact, short; full is the reference)
    since G0 section 8; every fragment below is in both styles."""
    spec = next(s for s in (plugin.sample(i, "S1") for i in range(80)) if s.qform == "ch_failed_check")
    ins = plugin.render(spec, ctx).row["instructions"]
    for frag in ("lines in time order", "a poll's 200 means nothing", "same ", " 409", "lowest-numbered",
                 "the only evidence"):
        assert frag in ins, frag
    assert "No step in the log has that target" in CT.claim_rules("full", CT.Needs())
    assert "No such step: not shown in the log" in CT.claim_rules("short", CT.Needs())
    assert "No step has that target: not shown in the log" in CT.claim_rules("compact", CT.Needs())
    assert all("leaves out" not in sk.text for sk in ctx.skins.values())


def test_g0_is_frozen_after_the_haiku_ambiguity_pass(plugin):
    """amb:T33: the points of the Haiku ambiguity pass are on file with the sha the plugin records, and the G0-lite
    spec answers every point (R1..R37 in its section 6)."""
    import hashlib
    import json
    rec = T.T33Plugin.AMB_PASS
    obj = json.loads((T.HERE / rec["points_file"]).read_text(encoding="utf-8"))
    canon = json.dumps(obj["points"], sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    assert hashlib.sha256(canon.encode()).hexdigest() == rec["points_sha256"] == obj["points_sha256"]
    assert len(obj["points"]) == rec["n_points"] == 37
    g0 = plugin.G0_LITE.read_text(encoding="utf-8")
    assert hashlib.sha256(plugin.G0_LITE.read_bytes()).hexdigest() == plugin.G0_SHA256 != rec["g0_before"]
    assert all(re.search(rf"^R{i} ", g0, re.M) for i in range(1, 38))
