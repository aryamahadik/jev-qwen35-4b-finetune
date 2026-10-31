"""T59 ASK-OR-PROCEED unit tests: solver A rule + oracle truth table, scene edits, plan quotas, renderer, K-gates, the check-at-generation
pipeline, the W-REPO guard, levers and G9 (no rows, no model, nothing written to disk; every example is built in memory)."""
import collections
import copy
import functools
import itertools
import os
import re

import pytest

from LK_COMMON import klevers, knames, kpipeline, kspec
from tool_engine import row_pipeline as rp, util
from tool_engine.probe_stub import StubHarness
import t59_build as bld
import t59_checked as ck
import t59_g9 as g9
import t59_gates as gates
import t59_generator as gen
import t59_hash_export as hxp
import t59_levers as lev
import t59_oracle as orc
import t59_render as rd
import t59_repo as repo
import t59_scene as sc
import t59_solver_a as sa

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(HERE)
AL = knames.load_allowlist()


@functools.lru_cache(maxsize=None)
def sample(total, seed="t59-test"):
    ctx = gen.Ctx(seed=seed, standin=False)
    plan = gen.build_plan(total=total, seed=seed)
    recs = []
    for g in plan:
        recs.extend(gen.generate_group(ctx, g))
    return tuple(recs), tuple(plan), ctx


@pytest.fixture(scope="module")
def pilot():
    return list(sample(1000)[0])


@pytest.fixture(scope="module")
def full():
    return list(sample(2000, "t59-full")[0])


# ---- K3: the rule ---------------------------------------------------------------------------------------------------------------
def test_truth_table_rule_oracle_and_formula_agree_on_the_full_cross_product():
    r = gates.k3_truth_table()
    # 128 = 2^6 flags x 2 modes per T6 3.3.1 sub-case; 7 sub-cases (none, 2 forced-ASK cases, 4 PROCEED-side neighbours; Opus ruling Q2)
    assert r["ok"] and r["cases"] == 128 * 7 and r["cases_t6"] == 128 * 6, r


def test_d3_irrev_definition():
    ok = dict(kind="delete", backup=True, undo=None, external=False, magnitude=3, created_by_agent=False)
    assert sa.undoable(ok) and not sa.irrev(ok, 10)
    assert sa.irrev(ok, 3)                                        # magnitude >= H counts as non-reversible even with a backup (T59-B1)
    assert sa.irrev(dict(ok, backup=False), 10)                   # no backup, no undo tool
    assert not sa.irrev(dict(ok, backup=False, undo=dict(tool="restore", remaining=5)), 10)
    assert sa.irrev(dict(ok, backup=False, undo=dict(tool="restore", remaining=0)), 10)    # window expired
    assert sa.irrev(dict(ok, external=True), 10)                  # external: not undoable by an undo tool
    assert not sa.irrev(dict(kind="read", backup=False, undo=None, external=False, magnitude=99), 10)
    cr = dict(kind="create", backup=False, undo=None, external=False, magnitude=1, created_by_agent=True)
    assert sa.undoable(cr)                                        # T59-M2: a create of an agent-made object, not external
    assert not sa.undoable(dict(cr, external=True))               # an invite / published object reaches people outside the thread


def test_a_resolver_never_settles_an_intent_slot():
    case = orc.case_from_flags(False, False, False, False, False, True, "ON")
    case["slots"][0]["resolver"] = True                           # INTENT slot with a resolver flag
    case["read_first"] = True
    assert sa.gold_case(case) == "ASK" == orc.oracle_label(case)


def test_imported_card_kinds_are_off_mode():
    for cid in ("card.t54.strict_ask", "card.t54.defaults_ok", "card.t54.read_before_write", "card.t50.c04", "card.t51.c06"):
        assert sa.imported_params(cid)["mode"] == "OFF"
    with pytest.raises(sa.SpecError):
        sa.imported_params("card.t59.c01")


# ---- scene edits ------------------------------------------------------------------------------------------------------------------
def _group(trigger, edit, card, world="tool", k=0, view="primary", form="mid", levels=None):
    return dict(gid="u-%s-%s-%s-%d" % (trigger, edit, world, k), block="A", trigger=trigger, kind="pair", edit=edit, form=form,
                labels=("ASK", "PROCEED"), view="with_outputs" if trigger in ("T6", "T8") else view, world=world, card=card,
                levels=levels or dict(certainty=2, intent=1, slot=1, undo=1, stakes=1, resolver=1, length=1), alarm=False,
                pos=[0, 1], size=2, spec=dict(size=2))


def _first_ok(trigger, edit, world="tool"):
    ctx = gen.Ctx(seed="edit-test", standin=False)
    for card in sc.CARDS:
        for k in range(4):
            g = _group(trigger, edit, card, world, k)
            for att in range(4):
                try:
                    return ctx, g, bld.build_group(ctx, g, att)
                except (bld.SceneReject, sc.EditNotApplicable):
                    continue
    return None


@pytest.mark.parametrize("trigger,edit", [(t, e) for t in sc.TRIGGERS for e in sc.EDITS_BY_TRIGGER[t]])
def test_every_registered_edit_flips_the_gold_and_only_its_lines_change(trigger, edit):
    got = _first_ok(trigger, edit)
    assert got is not None, "no realisable pair for %s/%s" % (trigger, edit)
    ctx, g, scenes = got
    recs = [rd.finalize(ctx, g, s, g["pos"][i], i) for i, s in enumerate(scenes)]
    assert [r["gold"] for r in recs] == ["ASK", "PROCEED"]
    assert gen.pair_line_problems(recs[0], recs[1], g) == []
    assert recs[0]["edit"] == recs[1]["edit"] == edit


def test_on_only_edits_are_refused_on_off_cards():
    ctx = gen.Ctx(seed="x", standin=False)
    for e, t in (("e3", "T1"), ("e4", "T1"), ("e11", "T4")):
        with pytest.raises((bld.SceneReject, sc.EditNotApplicable)):
            bld.build_group(ctx, _group(t, e, "card.t59.c05"), 0)


def test_edit_applicability_guards():
    ctx = gen.Ctx(seed="x", standin=False)
    with pytest.raises((bld.SceneReject, sc.EditNotApplicable)):
        bld.build_group(ctx, _group("T1", "e2", "card.t59.c02"), 0)          # defaults_count off on c02
    with pytest.raises((bld.SceneReject, sc.EditNotApplicable)):
        bld.build_group(ctx, _group("T3", "e10", "card.t59.c01"), 0)         # c01 carries no precedence line
    with pytest.raises((bld.SceneReject, sc.EditNotApplicable)):
        bld.build_group(ctx, _group("T7", "e14", "card.t59.c01"), 0)         # c01 has read_first off


# ---- plan --------------------------------------------------------------------------------------------------------------------------
def test_plan_sizes_follow_the_g0_lite_section_4():
    plan = gen.build_plan(total=2000, seed="t59-plan")
    a12, _ = gen.n_levers(2000)
    assert sum(a12.values()) == 150
    rows = sum(g["size"] for g in plan)
    assert rows == 2000 - 150
    by = collections.Counter()
    for g in plan:
        by[g["block"]] += g["size"]
    # the 150 lever rows are added to A (90), B (30) and D (30) by the pipeline hook; block sizes are read as shares (K4: +-2 pp)
    final = {"A": by["A"] + 90, "B": by["B"] + 30, "C": by["C"], "D": by["D"] + 30}
    for b, want in gates.BLOCK_SHARES.items():
        assert abs(final[b] / 2000.0 - want) <= 0.02, (b, final[b])


def test_plan_asks_are_42_percent_per_trigger_and_label_balanced():
    plan = gen.build_plan(total=2000, seed="t59-plan")
    ask = collections.Counter()
    tot = collections.Counter()
    for g in plan:
        labs = [g["label"]] if g["kind"] == "single" else list(g["labels"])
        for l in labs:
            tot[g["trigger"]] += 1
            ask[g["trigger"]] += l == "ASK"
    for tr in sc.TRIGGERS:
        assert 0.39 <= ask[tr] / tot[tr] <= 0.45, (tr, ask[tr] / tot[tr])


def test_plan_edit_mix_k12():
    plan = gen.build_plan(total=2000, seed="t59-plan")
    for tr in sc.TRIGGERS:
        c = collections.Counter(g["edit"] for g in plan if g["trigger"] == tr and g["kind"] == "pair")
        n = sum(c.values())
        assert len(c) >= 3 and max(c.values()) / n <= 0.40 and min(c.values()) / n >= 0.02, (tr, c)


def test_plan_world_and_view_shares():
    plan = gen.build_plan(total=2000, seed="t59-plan")
    rows = sum(g["size"] for g in plan)
    repo_rows = sum(g["size"] for g in plan if g["world"] == "repo")
    w_rows = sum(g["size"] for g in plan if g["view"] == "with_outputs")
    assert 0.35 <= repo_rows / rows <= 0.45, repo_rows / rows
    assert 0.30 <= w_rows / rows <= 0.40, w_rows / rows
    assert all(g["world"] == "tool" for g in plan if g["trigger"] in ("T3", "T5", "T6", "T7"))
    assert all(g["view"] == "with_outputs" for g in plan if g["trigger"] in ("T6", "T8"))


def test_plan_is_deterministic():
    a = gen.build_plan(total=300, seed="d")
    b = gen.build_plan(total=300, seed="d")
    assert [(g["gid"], g.get("edit"), g["card"], g["world"], g["view"]) for g in a] == [(g["gid"], g.get("edit"), g["card"], g["world"], g["view"]) for g in b]


# ---- generation --------------------------------------------------------------------------------------------------------------------
def test_generation_has_no_unrealisable_group_and_solver_a_matches_the_plan(pilot):
    assert len(pilot) >= 900
    assert len({r["row_id"] for r in pilot}) == len(pilot)


def test_rows_are_deterministic():
    a = gen.generate_in_memory(total=60, seed="det", standin=False)
    b = gen.generate_in_memory(total=60, seed="det", standin=False)
    assert [r["rendered"]["text"] for r in a] == [r["rendered"]["text"] for r in b]


def test_gold_is_solver_a_and_the_oracle_agrees(pilot):
    for r in pilot:
        case = sc.derive_case(r["scene"])
        assert sa.gold_label(r) == r["gold"] == orc.oracle_label(case)


def test_options_are_two_lettered_with_one_gold_and_balanced_positions(pilot):
    for r in pilot:
        assert [o["letter"] for o in r["options"]] == ["A", "B"]
        assert sum(1 for o in r["options"] if o["label"] == r["gold"]) == 1
        assert r["rendered"]["text"] == r["rendered"]["context"] + "\n\n" + r["rendered"]["question"] + "\n" + r["rendered"]["options_text"]
    for lab in ("ASK", "PROCEED"):
        rows = [r for r in pilot if r["gold"] == lab]
        a = sum(1 for r in rows if r["gold_letter"] == "A") / len(rows)
        assert 0.45 <= a <= 0.55, (lab, a)


def test_tags_are_never_rendered_and_no_internal_ids_leak(pilot):
    for r in pilot:
        assert kspec.rendered_tag_leaks(r) == []
        for tok in ck.FORBIDDEN:
            assert not re.search(r"(?<![A-Za-z0-9_])" + re.escape(tok) + r"(?![A-Za-z0-9_])", r["rendered"]["text"]), (r["row_id"], tok)


def test_the_text_is_ascii_and_within_the_token_rule(pilot):
    toks = [util.approx_tokens(r["rendered"]["text"]) for r in pilot]
    assert all(ord(c) < 128 for r in pilot for c in r["rendered"]["text"])
    assert max(toks) <= 1536 and sum(toks) / len(toks) <= 800


def test_names_are_on_the_frozen_allow_list(pilot):
    for r in pilot:
        assert AL.check_names("T59", r["names"]) == [], (r["row_id"], AL.check_names("T59", r["names"]))
    assert gates.k17_names(pilot, AL)["ok"]


def test_namespace_is_production_ready_and_nouns_are_drawn_not_picked():
    _recs, _plan, ctx = sample(1000)
    assert ctx.names.is_production_ready and not ctx.names.standin
    assert ctx.names.bucket == "bucket.t59"


def test_every_decisive_fact_is_visible_k25(pilot):
    for r in pilot:
        assert ck.observability_problems(r) == [], (r["row_id"], ck.observability_problems(r))


def test_family_invariants_pass_on_every_generated_row(pilot):
    bad = [(r["row_id"], ck.family_invariants(r)) for r in pilot if ck.family_invariants(r)]
    assert bad == [], bad[:3]


def test_output_lint_is_clean(pilot):
    for r in pilot:
        assert ck.lint_outputs(r) == [], r["row_id"]


# ---- K24 (W-REPO) --------------------------------------------------------------------------------------------------------------------
def test_k24_passes_on_every_repo_row_and_discriminates(pilot):
    rows = [r for r in pilot if r["world_kind"] == "repo"]
    assert len(rows) > 100
    assert all(repo.k24(r) == [] for r in rows)
    r = rows[0]
    spec, label_spec = repo.build_t50_spec(r)
    for n in spec.state.fs.values():                           # make every file foreign + dirty: T50 must ASK (R04), so K24 would refuse
        if n.kind == "file":
            n.tracked, n.created_by_agent = False, False
    res = label_spec(spec)
    assert res.label == "ASK" and "R04" in res.rules


def test_k24_refuses_a_t50_r18_ask_under_a_proceed_label_on_an_off_card(pilot, monkeypatch):
    """Skeptic: the ON-card exception for T50 R18 mirrors the T51 one -- R18 ASK + T59 PROCEED is allowed only on an ON card."""
    import types
    rows = [r for r in pilot if r["world_kind"] == "repo" and r["gold"] == "PROCEED"]
    off = [r for r in rows if r["card_mode"] == "OFF"]
    on = [r for r in rows if r["card_mode"] == "ON"]
    assert off and on
    real = repo.build_t50_spec

    def fake(rec, tag="k24"):
        spec, _ls = real(rec, tag)
        mem = types.SimpleNamespace(label="ASK", rule="R18")
        return spec, (lambda _spec: types.SimpleNamespace(label="ASK", members=[mem], rules=["R18"]))

    monkeypatch.setattr(repo, "build_t50_spec", fake)
    assert "t50:R18_ASK_but_T59_PROCEED_on_OFF" in repo.k24(off[0])
    assert "t50:R18_ASK_but_T59_PROCEED_on_OFF" not in repo.k24(on[0])


# ---- gates -------------------------------------------------------------------------------------------------------------------------------
def test_pilot_gates_that_are_data_only(pilot):
    out = {g["id"]: g for g in gates.run_all(pilot, harness=None, allowlist=AL, code_files=[os.path.join(FAM, f) for f in os.listdir(FAM) if f.endswith(".py")])}
    for gid in ("K3", "K7", "K12", "K13", "K14", "K16", "K17", "K18", "K20", "K24", "K25", "K26", "K27"):
        assert out[gid]["ok"] is True, (gid, out[gid])
    assert out["K4"]["ok"], out["K4"]
    assert out["K5"]["ok"] is None                              # probes need the harness


def test_probe_wiring_runs_with_the_stub_harness(pilot):
    h = StubHarness(repeats=2)
    for fn in (gates.k5_trigger_only, gates.k6_request_only, gates.k8_structure, gates.k9_card, gates.k10_candidate_count, gates.k11_alarm):
        res = fn(pilot, h)
        assert res["ok"] in (True, False) and "auc" in res or res["ok"] is None, res
    # a planted label leak must be caught by the wiring
    leak = gates.gc.probe_binary_gate("leak", h, [{"x": int(r["gold"] == "ASK")} for r in pilot], [int(r["gold"] == "ASK") for r in pilot],
                                      [r["group_id"] for r in pilot])
    assert leak["ok"] is False


def test_k14_catches_a_pair_that_differs_outside_its_edit(pilot):
    recs = [r for r in pilot if r["block"] == "A" and r["edit"] == "e1"]
    a = [r for r in recs if r["pair_role"] == "a"][0]
    b = [r for r in recs if r["pair_role"] == "b" and r["group_id"] == a["group_id"]][0]
    bad = copy.deepcopy(b)
    bad["lines"] = bad["lines"] + [("tool_filler", "- extra")]
    assert gen.pair_line_problems(a, bad, dict(kind="pair", edit="e1")) == ["tool_filler"]


def test_k18_scanner_flags_exec_names(tmp_path):
    p = tmp_path / "x.py"
    p.write_text("import subprocess\nx = 'subprocess is only a word here'\n# eval in a comment\nsubprocess.run(['ls'])\n")
    r = gates.k18_no_exec([str(p)])
    assert not r["ok"] and all(v[1] == "subprocess" for v in r["violations"])


def test_family_code_has_no_exec_k18():
    files = [os.path.join(FAM, f) for f in os.listdir(FAM) if f.endswith(".py")] + \
        [os.path.join(os.path.dirname(FAM), "LK_COMMON", f) for f in os.listdir(os.path.join(os.path.dirname(FAM), "LK_COMMON")) if f.endswith(".py")]
    assert gates.k18_no_exec(files)["ok"]


def test_swap_pairs_differ_only_in_card_lines_and_in_label(full):
    swaps = [r for r in full if r["block"] == "C"]
    assert len(swaps) >= 100
    assert gates.k9_card(full, None)["swap_bad"] == []


def test_expanded_pool_file_is_current_and_covers_every_seed_form():
    import json
    import t59_wording as tw
    pool = json.load(open(os.path.join(FAM, "pools", "wording_pool_v1.json")))
    man = json.load(open(os.path.join(FAM, "pools", "pool_manifest.json")))
    from tool_engine import wording_expand
    assert wording_expand.pool_sha(pool) == man["pool_sha256"]
    for form, ws in tw.seed_pool().pools.items():
        assert form in pool and all(w in pool[form] for w in ws), form


def test_wording_pool_has_50_per_question_form():
    import json
    pool = json.load(open(os.path.join(FAM, "pools", "wording_pool_v1.json")))
    assert len(pool["q.mid"]) >= 50 and len(pool["q.early"]) >= 50


# ---- the pipeline ------------------------------------------------------------------------------------------------------------------------
def _run(total=150, seed="p", hook=None, flip=()):
    sb = kpipeline.TestDoubleSolverB(sa.gold_label, flip_ids=flip)
    return ck.run(total, seed, hook or rp.TestDoubleHook(), solver_b=sb, render_b=kpipeline.test_double_render_b, standin=True)


def test_adapter_refuses_without_solver_b():
    with pytest.raises(kpipeline.SolverBRequired):
        ck.adapter(None, None)
    with pytest.raises(kpipeline.SolverBRequired):
        ck.adapter(lambda r: None, None)


def test_pipeline_refuses_without_a_stamp_hook():
    with pytest.raises(rp.StampServiceRequired):
        _run(hook=rp.RefusingHook())


def test_pipeline_keeps_only_stamped_clean_rows():
    kept, summ, log, rep = _run()
    assert summ["kept"] == len(kept) > 100 and summ["dropped"] == {}
    assert all(r["stamp"]["verdict"] == "clean" for r in kept)
    assert rep["cues"]["ok"]


def test_a_solver_b_disagreement_drops_the_row_only():
    kept, summ, log, _ = _run(flip=("A-T1-00000-a", "A-T1-00001-a", "D-T3-sett-00000-s"))
    assert summ["dropped"].get("answer:A_B_label_differs", 0) >= 1


def test_g13_hit_retires_the_whole_group_and_never_rewords_it():
    kept, summ, log, _ = _run(hook=rp.TestDoubleHook(hit_ids={"A-T2-00000-a"}))
    assert summ["retired_groups"] >= 1
    assert not any(r["group_id"] == "A-T2-00000" for r in kept)
    assert any(e.get("stage") == "g13" and e["group_id"] == "A-T2-00000" for e in log)


def test_lever_rows_are_derived_stamped_and_keep_their_clean_twin():
    kept, summ, log, _ = _run(total=400, seed="lev")
    a12 = [r for r in kept if r.get("lever_tag") == "lever.a12" and not r.get("heldout_family")]
    dev = [r for r in kept if r.get("heldout_family")]
    ids = {r["row_id"] for r in kept}
    assert a12 and dev
    assert all(r["twin_of"] in ids and r["stamp"]["verdict"] == "clean" for r in a12 + dev)
    assert all(r["a12"]["transform"] in klevers.TRAINED for r in a12)
    assert all(r["a12"]["transform"] in klevers.HELD_OUT and r["split"] == "dev" and r["dev_only"] == "split.dev_only" for r in dev)
    assert gates.k27_perturbation(kept)["ok"] and gates.k20_split(kept)["ok"]


def test_perturbed_rows_restore_exactly_and_keep_decision_spans(pilot):
    n = 0
    for r in pilot[:300]:
        row = lev.perturbed_row(r, "pert.diacritics", util.rng_for("x", r["row_id"]), "t")
        if row is None:
            continue
        back = klevers.invert(row["rendered"]["context"], [tuple(o) for o in row["a12"]["ops"]])
        assert back == r["rendered"]["context"]
        n += 1
    assert n > 100


# ---- A10 ----------------------------------------------------------------------------------------------------------------------------------
def test_wrapper_seeds_pass_the_lint_and_the_lint_catches_violations():
    for fam, ss in klevers.SEED_SENTENCES.items():
        for s in ss:
            assert klevers.lint_wrapper(s, "T59") == [] and klevers.lint_wrapper(s, "T60") == [], (fam, s)
    for bad in ("Please delete record 5 now.", "You may delete the backups.", "Just do it, no need to check.", "Ask me before you stop.", 'Use "alpha" here.'):
        assert klevers.lint_wrapper(bad, "T59"), bad


def test_a10_rows_when_built_keep_the_request_verbatim_and_the_label():
    ctx = gen.Ctx(seed="w", standin=False)
    plan = gen.build_plan(total=300, seed="w", a10=True)
    recs = []
    for g in plan:
        recs.extend(gen.generate_group(ctx, g))
    rows = lev.make_extra_rows(ctx, recs, a10=True)
    wr = [r for r in rows if r.get("lever_tag") == "lever.a10"]
    assert wr
    clean = {r["row_id"]: r for r in recs}
    for r in wr:
        c = clean[r["twin_of"]]
        assert r["gold"] == c["gold"] and c["lines"][0] == r["lines"][0]
        assert r["wrapper"]["family"] in klevers.WRAPPERS_TRAINED or r.get("heldout_family")
        req = [t for k, t in c["lines"] if k == "user_req"][0][len("User: "):]
        assert req in r["rendered"]["text"]


# ---- G9 -----------------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("leg", ["leg_a", "leg_b", "leg_c", "leg_d"])
def test_g9_legs_agree_100_percent(leg):
    r = getattr(g9, leg)()
    assert r["pass"] and r["mismatches"] == 0 and r["cases"] > 50, r


def test_g9_leg_e_on_off_coherence(full):
    r = g9.leg_e(full)
    assert r["pass"] and r["cases"] >= 50, r


def test_mapping_tables_are_hashed():
    assert len(g9.mapping_sha()) == 64


# ---- hygiene -------------------------------------------------------------------------------------------------------------------------------
def test_no_barred_words_in_the_family_files():
    bad = []
    for root in (FAM, os.path.join(os.path.dirname(FAM), "LK_COMMON")):
        for dp, dn, fn in os.walk(root):
            if "__pycache__" in dp:
                continue
            for f in fn:
                if f.endswith((".py", ".json", ".md", ".ini")) and f not in ("HASH_EXPORT.json",):
                    low = open(os.path.join(dp, f), encoding="utf-8").read().lower()
                    barred = ("o" + "hs", "seal" + "ed")
                    if any(b in low for b in barred) or barred[0] in os.path.join(dp, f).lower():
                        bad.append(os.path.join(dp, f))
    assert bad == []


def test_hash_export_is_hashes_only():
    exp = hxp.build(created="2026-10-18T00:00:00Z")
    from tool_engine import hash_export as hx
    assert hx.assert_no_text(exp)
    assert exp["wording_pool"]["n_forms"] >= 30


def test_the_row_start_guard_accepts_the_job_manifest_of_generated_rows(tmp_path):
    """L-0's own manifest check (family on the v1.2 allow-list, every policy / tool / language / runner / carrier id on it) on real rows."""
    import json
    import sys
    infra = os.path.join(os.path.dirname(os.path.dirname(FAM)), "c21_infra")
    if infra not in sys.path:
        sys.path.insert(0, infra)
    import row_start_guard as rsg
    from LK_COMMON import MANIFEST_V12, MANIFEST_V12_SHA
    from tool_engine import names as tn
    allow, _sha, reasons, fams = rsg.load_allowlist_and_families(MANIFEST_V12, open(MANIFEST_V12_SHA).read().split()[0])
    assert reasons == []
    recs = gen.generate_in_memory(total=200, seed="guard", standin=False)
    jm = tn.job_manifest("T59", recs)
    jm["family"] = "T59"
    p = tmp_path / "job.json"
    p.write_text(json.dumps(jm))
    assert rsg.check_manifest(str(p), allow, fams) == []
    jm["names"]["tool"] = jm["names"]["tool"] + ["verb.not_on_the_list"]
    p.write_text(json.dumps(jm))
    assert rsg.check_manifest(str(p), allow, fams)


# ---- Opus ruling Q2 (18 Oct 2026, before any pool rows): G0-lite 3.3.1 binds for T6 on every card ---------------------------------------
def _q2_scene(cls, mode, undo, big, keyed=False, idem=False, read_get=False, read_first=False, in_ctx=False):
    """A T6 scene whose card, undo path and magnitude are set explicitly (H = 10; magnitude 12 when `big`, else 3)."""
    s = g9._t6_scene([], 3, cls, 1, "write", idem, keyed, False, read_get, in_ctx, read_first, mode=mode, undo=undo)
    s["card"]["H"] = 10
    s["t"]["size"] = 12 if big else 3
    return s


def _q2_expected(cls, keyed, idem, read_get, in_ctx):
    """G0-lite 3.3.1, written out by hand: ambiguous write: key offered -> PROCEED, a read path (R-RES) -> PROCEED, an idempotent write ->
    PROCEED, neither -> ASK; invalid_named_arg: corrected value in context -> PROCEED, not in context -> ASK."""
    if cls == "ambiguous":
        return "PROCEED" if (keyed or idem or read_get) else "ASK"
    return "PROCEED" if in_ctx else "ASK"


def test_q2_t6_ambiguous_write_truth_table_over_card_undo_magnitude_key_idempotent_read_path():
    n = 0
    for mode, undo, big, keyed, idem, read_get, read_first in itertools.product(("ON", "OFF"), (False, True), (False, True), (False, True),
                                                                               (False, True), (False, True), (False, True)):
        scene = _q2_scene("ambiguous", mode, undo, big, keyed=keyed, idem=idem, read_get=read_get, read_first=read_first)
        if read_get and not read_first:                   # the one case 3.3.1 does not cover cleanly: refused, never labelled
            with pytest.raises(sa.SpecError):
                sc.scene_gold(scene)
            continue
        want = _q2_expected("ambiguous", keyed, idem, read_get, False)
        case = sc.derive_case(scene)
        got, trace = sa.gold_case(case, with_trace=True)
        assert got == orc.oracle_label(case) == want, (mode, undo, big, keyed, idem, read_get, read_first, got, want)
        assert trace["rule"] == ("t6_331" if want == "ASK" else "robust")
        n += 1
    assert n == 96


def test_q2_t6_invalid_named_arg_truth_table_over_card_undo_magnitude_and_context():
    n = 0
    for mode, undo, big, in_ctx, read_first in itertools.product(("ON", "OFF"), (False, True), (False, True), (False, True), (False, True)):
        scene = _q2_scene("invalid_named", mode, undo, big, in_ctx=in_ctx, read_first=read_first)
        want = _q2_expected("invalid_named", False, False, False, in_ctx)
        case = sc.derive_case(scene)
        got, trace = sa.gold_case(case, with_trace=True)
        assert got == orc.oracle_label(case) == want, (mode, undo, big, in_ctx, read_first, got, want)
        assert trace["rule"] == ("robust" if in_ctx else "t6_331")
        n += 1
    assert n == 32


def test_q2_the_ruling_scenario_on_card_undo_path_magnitude_below_h_is_ask_for_both_cases():
    for scene in (_q2_scene("ambiguous", "ON", True, False), _q2_scene("invalid_named", "ON", True, False, in_ctx=False)):
        assert scene["card"]["mode"] == "ON" and scene["fx"]["undo"] and scene["t"]["size"] < scene["card"]["H"]
        case = sc.derive_case(scene)
        a = sa.analyse(case)
        assert not a["robust"] and a["forward"] and not a["any_irrev"]          # under 3.2 steps (3)-(4) this would be PROCEED
        assert sa.gold_case(case) == orc.oracle_label(case) == "ASK"
        assert sa.gold_case(dict(case, t6=None)) == "PROCEED"                      # i.e. the 3.2 order alone is what the ruling overrides


def test_q2_other_t6_classes_are_unchanged_by_the_override():
    """3.3.1's other sub-cases do not depend on the card mode or the undo path either (they agree with 3.2 steps (1)-(2))."""
    for mode, undo, big in itertools.product(("ON", "OFF"), (False, True), (False, True)):
        for cls, idem, keyed, equiv, attempt, want in (("transient", True, False, False, 1, "PROCEED"), ("transient", False, True, False, 1, "PROCEED"),
                                                       ("transient", False, False, False, 3, "ASK"), ("transient", False, False, True, 3, "PROCEED"),
                                                       ("invalid_unnamed", False, False, False, 1, "ASK"), ("invalid_unnamed", False, False, True, 1, "PROCEED"),
                                                       ("unsupported_op", False, False, False, 1, "ASK"), ("unsupported_op", False, False, True, 1, "PROCEED"),
                                                       ("auth_denied", False, False, True, 1, "ASK")):
            scene = g9._t6_scene([], 3, cls, attempt, "write", idem, keyed, equiv, False, False, False, mode=mode, undo=undo)
            scene["card"]["H"], scene["t"]["size"] = 10, (12 if big else 3)
            assert sc.scene_gold(scene) == want == orc.oracle_label(sc.derive_case(scene)), (cls, mode, undo, big)


def test_q2_k3_catches_a_solver_without_the_override_and_a_wrong_formula(monkeypatch):
    assert gates.k3_truth_table()["ok"]
    monkeypatch.setattr(sa, "t6_forced_ask", lambda case: False)               # a solver that applies the 3.2 order alone
    r = gates.k3_truth_table()
    assert not r["ok"] and r["mismatches"]
    monkeypatch.undo()
    assert sa.gold_formula(False, False, False, False, False, False, "ON", t6_ask=True) == "ASK"
    assert sa.gold_formula(False, False, False, False, False, False, "ON", t6_ask=False) == "PROCEED"
    assert sa.gold_formula(False, True, False, False, False, False, "ON", t6_ask=True) == "PROCEED"      # (2) ROBUST comes first
    assert sa.gold_formula(True, False, False, False, False, False, "ON", t6_ask=False) == "ASK"          # (1) E empty


def test_q2_read_path_listed_on_a_card_without_read_first_is_refused_and_never_generated(full):
    scene = _q2_scene("ambiguous", "ON", True, False, read_get=True, read_first=False)
    with pytest.raises(sa.SpecError):
        sc.derive_case(scene)
    rows = [r for r in full if r["sub_block"] == "T6" and r["scene"]["t"]["cls"] == "ambiguous"]
    assert len(rows) > 50
    for r in rows:
        kinds = {k for k, _ in r["lines"]}
        listed = bool(r["scene"]["tools"].get("read_get"))
        assert listed == ("tool_read_get" in kinds)
        assert not listed or r["scene"]["card"]["read_first"], r["row_id"]
    assert any(r["scene"]["tools"].get("read_get") for r in rows)               # the read-path PROCEED side is still built


def test_q2_generated_t6_rows_follow_3_3_1_on_every_card(full):
    t6 = [r for r in full if r["sub_block"] == "T6"]
    assert {r["trace"]["rule"] for r in t6} <= {"E_empty", "robust", "t6_331"}           # no card-mode or undo-path rule is ever the reason
    forced = [r for r in t6 if r["trace"]["rule"] == "t6_331"]
    assert len(forced) >= 15 and all(r["gold"] == "ASK" for r in forced)
    for r in t6:
        t = r["scene"]["t"]
        if t["cls"] == "ambiguous" and not (r["scene"]["fx"]["keyed"] or r["scene"]["fx"]["idempotent"]) and not r["scene"]["tools"].get("read_get"):
            assert r["gold"] == "ASK" and r["trace"]["rule"] == "t6_331", r["row_id"]
        if t["cls"] == "invalid_named" and not t["corrected_in_ctx"]:
            assert r["gold"] == "ASK" and r["trace"]["rule"] == "t6_331", r["row_id"]
    # the ruling's scenario occurs in the data: an ON card, an undo path, magnitude below H, forced ASK
    scen = [r for r in forced if r["card_mode"] == "ON" and r["scene"]["fx"]["undo"] and sc.max_magnitude(r["scene"]) < r["scene"]["card"]["H"]]
    assert len(scen) >= 3
    # and both modes carry forced ASK rows
    assert {r["card_mode"] for r in forced} == {"ON", "OFF"}
    # the answer-side rows are the D1 / D2 / paired kinds: key offered, read path, equivalent tool, corrected value in context
    for r in (x for x in t6 if x["gold"] == "PROCEED"):
        assert r["trace"]["rule"] == "robust"


def test_q2_t6_forced_ask_rows_pass_k25_and_k25_catches_a_visible_key_or_read_path(full):
    forced = [r for r in full if r["sub_block"] == "T6" and r["trace"]["rule"] == "t6_331"]
    assert forced and all(ck.observability_problems(r) == [] for r in forced)
    amb = next(r for r in forced if r["scene"]["t"]["cls"] == "ambiguous")
    bad = copy.deepcopy(amb)
    bad["lines"] = bad["lines"] + [("tool_read_get", "- get_x(x_id: str) [read] -- Reads one.")]
    assert "t6_key_or_read_path_visible_but_forced_ask" in ck.observability_problems(bad)
    inv = [r for r in forced if r["scene"]["t"]["cls"] == "invalid_named"]
    if inv:
        bad2 = copy.deepcopy(inv[0])
        bad2["lines"] = bad2["lines"] + [("user_value", "User: The status is alpha.")]
        assert "t6_corrected_value_visible_but_forced_ask" in ck.observability_problems(bad2)


def test_q2_t6_stakes_evidence_is_drawn_independently_of_card_mode_class_and_label():
    """pick_cause gives T6 one fixed distribution (undo present and small / no undo / magnitude >= H), whatever the card mode or edit."""
    for card in ("card.t59.c01", "card.t59.c05"):                               # an ON card and an OFF card
        for edit in (None, "e17", "e18", "e19", "e20"):
            cnt = collections.Counter(bld.pick_cause(util.rng_for("q2", card, str(edit), i), dict(card=card), edit, "T6", "tool") for i in range(600))
            assert set(cnt) == set(bld.T6_CAUSES), cnt
            assert all(0.25 <= v / 600.0 <= 0.42 for v in cnt.values()), (card, edit, cnt)
    # the scene follows its cause: 'None' keeps an undo path and a small magnitude, i.e. the ruling's ON-card scenario can be built
    ctx = gen.Ctx(seed="q2", standin=False)
    seen = set()
    for k in range(60):
        g = dict(_group("T6", "e17", "card.t59.c01", k=k))
        try:
            scenes = bld.build_group(ctx, g, 0)
        except (bld.SceneReject, sc.EditNotApplicable):
            continue
        base = scenes[0] if g["labels"][0] == "ASK" else scenes[1]
        assert sc.scene_gold(base) == "ASK"
        seen.add((bool(base["fx"]["undo"]), sc.max_magnitude(base) >= base["card"]["H"]))
    assert (True, False) in seen                                                  # undo path present, magnitude below H, ON card: still ASK


def test_q2_t6_has_no_d3_controls_and_no_swap_pairs_and_d3_is_120_over_the_other_triggers():
    assert gen.D3_BY_TRIGGER["T6"] == 0 and "T6" not in gen.D3_TRIGGERS
    assert sum(gen.D3_BY_TRIGGER.values()) == gen.D3_TOTAL == 120
    assert all(gen.D3_BY_TRIGGER[t] > 0 for t in sc.TRIGGERS if t != "T6")
    assert gen.D3_WEIGHT_BOOST == {"T4": 2.0, "T5": 2.0}                          # FU1: recorded design weights
    assert not any(k.startswith("D|T6|reversible") for k in gen.ENTRIES) and not any(k.startswith("C|T6") for k in gen.ENTRIES)
    t6_proc = {v["ctl"]: v["rows"] for k, v in gen.ENTRIES.items() if v["trigger"] == "T6" and v["block"] == "D" and v.get("label") == "PROCEED"}
    assert set(t6_proc) == {"ctl.t59.unambiguous", "ctl.t59.settled"} and sum(t6_proc.values()) == 42
    plan = gen.build_plan(total=2000, seed="t59-plan")
    assert not [g for g in plan if g["trigger"] == "T6" and (g.get("ctl") == "ctl.t59.reversible_ambiguity" or g["kind"] == "swap")]
    assert all(g["ctl_edit"] in ("e17", "e18", "e19", "e20") for g in plan if g["trigger"] == "T6" and g.get("ctl") in
               ("ctl.t59.unambiguous", "ctl.t59.settled"))


def test_fu2_d_controls_follow_g0_lite_section_4_240_140_120_180_and_80_q_early():
    """Opus ruling Q2 follow-up FU2: the G0-lite numbers bind (the earlier 174 / 226 / 100 and Q-EARLY 50 were a builder deviation)."""
    by_ctl, early = collections.Counter(), 0
    for k, v in gen.ENTRIES.items():
        if v["block"] == "D":
            by_ctl[v["ctl"]] += v["rows"]
            early += v["rows"] if v["form"] == "early" else 0
    assert (by_ctl["ctl.t59.unambiguous"], by_ctl["ctl.t59.settled"], by_ctl["ctl.t59.reversible_ambiguity"], by_ctl["ctl.t59.clear_ask"]) == \
        (240, 140, 120, 180)
    assert early == 80 and gen.D1_EARLY_TOTAL == 80
    for tr in sc.TRIGGERS:                                                       # the per-trigger table (section 4) still holds
        proc = sum(v["rows"] for v in gen.ENTRIES.values() if v["block"] == "D" and v["trigger"] == tr and v.get("label") == "PROCEED")
        ask = sum(v["rows"] for v in gen.ENTRIES.values() if v["block"] == "D" and v["trigger"] == tr and v.get("label") == "ASK")
        assert (proc, ask) == (gen.D_PROC[tr], gen.D_ASK[tr]), tr
    assert sum(gen.D_PROC.values()) == 500 and sum(gen.D_ASK.values()) == 180
    assert not any(v["form"] == "early" for v in gen.ENTRIES.values() if v["trigger"] in ("T6", "T8"))
    # D2 holds only mechanisms the K30 'settled' count recognises, plus the common-step cases
    assert set(e for t in sc.TRIGGERS for e in bld.SETTLED_EDITS[t] if gen.D2_BY_TRIGGER[t]) <= {"e2", "e10", "e14", "e18", "e8"}
    # about half of the D1 groups carry an alarming surface (G0-lite: 120 of 240)
    plan = gen.build_plan(total=2000, seed="t59-plan")
    d1 = [g for g in plan if g.get("ctl") == "ctl.t59.unambiguous"]
    assert abs(sum(1 for g in d1 if g["alarm"]) - len(d1) / 2.0) <= 8


def test_fu2_k30_k4_k12_on_the_built_rows(pilot, full):
    """K30 is judged on built rows: settled 15-25%, common step >= 8%, reversibility 25-40%; K4 per-card ASK share 36-48%; K12 edit coverage."""
    for rows in (pilot, full):
        k30 = gates.k30_resolver_default(rows)
        assert k30["ok"] and 0.15 <= k30["settled"] <= 0.25 and k30["common"] >= 0.08 and 0.25 <= k30["reversible"] <= 0.40, k30
        assert gates.k4_balance(rows)["ok"], gates.k4_balance(rows)
        assert gates.k12_edit_coverage(rows)["ok"]
    plan = gen.build_plan(total=2000, seed="t59-plan")
    for tr in sc.TRIGGERS:                                                       # K12 on the plan: >= 3 fields, none above 40%, each >= 2%
        c = collections.Counter(g["edit"] for g in plan if g["trigger"] == tr and g["kind"] == "pair")
        n = sum(c.values())
        assert len(c) >= 3 and max(c.values()) / n <= 0.40 and min(c.values()) / n >= 0.02, (tr, c)


def test_fu3_row_schema_carries_the_t6_pointer_line_and_is_in_the_hash_export():
    txt = open(os.path.join(FAM, "ROW_SCHEMA.md"), encoding="utf-8").read()
    assert "T6 error classes follow G0-lite 3.3.1, which overrides steps (3)/(4) for T6 (Opus ruling Q2, 18 Oct)" in txt
    exp = hxp.build(created="2026-10-18T00:00:00Z")
    assert "ROW_SCHEMA.md" in exp["extra"] and "NOTES.md" in exp["extra"]


def test_q2_t6_d3_and_swap_branches_are_hard_guarded():
    ctx = gen.Ctx(seed="q2g", standin=False)
    g = dict(_group("T6", None, "card.t59.c01"), kind="single", label="PROCEED", ctl="ctl.t59.reversible_ambiguity", block="D")
    with pytest.raises(AssertionError):
        bld.build_group(ctx, g, 0)
    with pytest.raises(AssertionError):
        bld._build_reversible(ctx, g, ctx.rng("x"))
    sw = dict(_group("T6", "swap", "card.t59.c01"), kind="swap", card_off="card.t59.c05", block="C")
    with pytest.raises(AssertionError):
        bld.build_group(ctx, sw, 0)
    with pytest.raises(AssertionError):
        bld._build_swap(ctx, sw, ctx.rng("y"))


def test_q2_g9_leg_d_runs_under_on_and_off_cards_and_catches_the_old_on_card_proceed(monkeypatch):
    r = g9.leg_d(n_per_seed=1200, seeds=("q2-d1",))
    assert r["pass"] and r["mismatches"] == 0
    assert set(r["variants"]) == {"OFF/no_undo", "OFF/undo", "ON/no_undo", "ON/undo"} and len(set(r["variants"].values())) == 1

    def old_gold(scene):                                                         # the 3.2 order alone (what solver A did before the ruling)
        return sa.gold_case(dict(sc.derive_case(scene), t6=None))
    monkeypatch.setattr(sc, "scene_gold", old_gold)
    bad = g9.leg_d(n_per_seed=1200, seeds=("q2-d1",))
    assert not bad["pass"] and bad["mismatches"] > 0
    assert set(bad["mismatches_by_variant"]) == {"ON/undo"}                      # exactly the ON-card + undo-path case the ruling names


# ---- Opus ruling Q2 follow-up FU5: a read path is ANY listed read-only call on the target's noun (list_ or get_) ----------------------------
def _t7_scene(read_first, read_get=False, read_auth=False, prec=None, mode="ON", undo=False):
    """A T7 scene with two disagreeing sources, no precedence line unless `prec`, explicit card flags and tools."""
    ent = dict(noun="ent", unit="unit", unit_pl="units", fa="fa", fb="fb", parent="par")
    op = dict(verb="rename", kind="update", undo_verb="restore" if undo else None, param=dict(role="name", type="str"), ext_fixed=False)
    return dict(trigger="T7", world="tool", spec_id="u-t7", card=dict(id="card.t59.c02", mode=mode, H=10, defaults_count=False,
                                                                      read_first=read_first, retry_cap=3, prec_ok=True),
                ent=ent, op=op, fx=dict(undo=dict(window=30, elapsed=0) if undo else None, external=False, backup=False, idempotent=False, keyed=False),
                tools=dict(read_get=read_get, read_list=False, read_auth=read_auth, equiv=None), cands=[], prec=prec,
                t=dict(fact="name", role="name", va="v1", vb="v2", plan_val="v1", src_a="user", src_b="notes", target="x-1", size=3))


def test_fu5_any_listed_read_only_call_is_a_read_path_in_solver_a_and_the_oracle_for_t6():
    """list_<noun> alone is a read path (not only get_); on a read_first card it settles the open WORLD slot, on a card without it the row is refused."""
    base = _q2_scene("ambiguous", "ON", True, False, read_first=True)
    assert sc.scene_gold(base) == "ASK" and not sc.read_path_listed(base)
    for flag in ("read_get", "read_list", "read_auth"):
        s2 = copy.deepcopy(base)
        s2["tools"][flag] = True
        assert sc.read_path_listed(s2)
        case = sc.derive_case(s2)
        assert case["t6"]["read_path"] and sa.gold_case(case) == orc.oracle_label(case) == "PROCEED", flag
        s3 = copy.deepcopy(s2)
        s3["card"]["read_first"] = False
        with pytest.raises(sa.SpecError):
            sc.derive_case(s3)


def test_fu5_t7_a_read_only_call_on_the_noun_settles_the_fact_on_read_first_cards_only_solver_a_and_oracle():
    for name, kw in (("plain get_", dict(read_get=True)), ("authoritative get_", dict(read_auth=True))):
        on_rf = _t7_scene(True, **kw)
        case = sc.derive_case(on_rf)
        assert sa.gold_case(case, True)[1]["r_res"] and sa.gold_case(case) == orc.oracle_label(case) == "PROCEED", name
        no_rf = _t7_scene(False, **kw)                                        # D5: R-RES needs read_first, so the same row without it is not settled
        case = sc.derive_case(no_rf)
        assert not sa.analyse(case)["r_res"] and sa.gold_case(case) == orc.oracle_label(case) == "ASK", name
    bare = _t7_scene(True)                                                    # no read-only call at all: a read_first T7 ASK row
    case = sc.derive_case(bare)
    assert sa.gold_case(case) == orc.oracle_label(case) == "ASK" and not sc.read_path_listed(bare)


def test_fu5_generated_rows_never_show_a_read_only_call_where_the_row_is_meant_to_have_none(full):
    bad = [(r["row_id"], rd.read_path_problems(r)) for r in full if rd.read_path_problems(r)]
    assert bad == [], bad[:3]
    t6 = [r for r in full if r["sub_block"] == "T6"]
    t7 = [r for r in full if r["sub_block"] == "T7"]
    assert len(t6) > 100 and len(t7) > 100
    assert all(not any(k == "tool_read_list" for k, _t in r["lines"]) for r in t6 + t7)           # list_<noun> is never listed in a T6 / T7 row
    for r in t6:
        if r["scene"]["t"]["cls"] == "ambiguous" and not r["scene"]["tools"].get("read_get"):
            assert rd.read_only_calls_on_noun(r) == [], r["row_id"]                                # a 'neither' row shows no read-only call on the noun
        if r["scene"]["t"]["cls"] == "ambiguous" and rd.read_only_calls_on_noun(r):
            assert r["scene"]["card"]["read_first"] and r["gold"] == "PROCEED"
    rf_ask = [r for r in t7 if r["scene"]["card"]["read_first"] and r["gold"] == "ASK"]
    assert len(rf_ask) >= 5 and all(rd.read_only_calls_on_noun(r) == [] for r in rf_ask)           # a read_first T7 ASK row has none
    # tool evidence (a get_ result in the row) appears only on cards without read_first; a read_first T7 row with a read-only call is PROCEED
    for r in t7:
        shown = rd.read_only_calls_on_noun(r)
        if r["scene"]["t"]["src_b"] == "tool":
            assert shown and not r["scene"]["card"]["read_first"]
        if shown and r["scene"]["card"]["read_first"]:
            assert r["gold"] == "PROCEED" and r["trace"]["r_res"]
    assert any(r["scene"]["tools"].get("read_auth") for r in t7)                                   # the e14 resolver rows are still built


def test_fu5_the_per_row_assert_catches_a_planted_read_only_call(full):
    t7 = next(r for r in full if r["sub_block"] == "T7" and r["scene"]["card"]["read_first"] and r["gold"] == "ASK")
    bad = copy.deepcopy(t7)
    noun = bad["scene"]["ent"]["noun"]
    bad["lines"] = bad["lines"] + [("tool_read_list", "- list_%s() [read] -- Lists %s records." % (noun, noun))]
    got = rd.read_path_problems(bad)
    assert "t7_ask_on_read_first_card_with_a_read_only_call" in got and "read_path_scene_vs_text" in got
    t6 = next(r for r in full if r["sub_block"] == "T6" and r["scene"]["t"]["cls"] == "ambiguous" and r["gold"] == "ASK")
    bad = copy.deepcopy(t6)
    noun = bad["scene"]["ent"]["noun"]
    bad["lines"] = bad["lines"] + [("tool_filler", "- get_%s(%s_id: str) [read] -- Gets one %s." % (noun, noun, noun))]
    got = rd.read_path_problems(bad)
    assert "t6_ambiguous_read_path_vs_text" in got and "open_world_slot_resolver_vs_text" in got


def test_fu5_note_t8_is_exempt_from_the_read_path_rule_but_every_t8_fork_is_an_intent_slot(full, monkeypatch):
    t8 = [r for r in full if r["sub_block"] == "T8"]
    assert len(t8) > 50
    for r in t8:
        assert rd.read_path_problems(r) == [], r["row_id"]
        case = sc.derive_case(r["scene"])
        assert all(s["kind"] == "INTENT" and not s.get("resolver") for s in case["slots"])
        assert any(k == "tool_read_find" for k, _t in r["lines"]) or r["scene"]["world"] == "repo"        # the find / list calls are the observation
    r = next(x for x in t8 if x["scene"]["world"] == "tool")
    real = sc.derive_case

    def world_fork(scene):                                                        # a T8 fork built as a WORLD slot must be refused
        c = real(scene)
        c["slots"][0] = dict(c["slots"][0], kind="WORLD")
        return c
    monkeypatch.setattr(sc, "derive_case", world_fork)
    assert rd.read_path_problems(r) == ["t8_fork_not_an_intent_slot"]
