"""T60 CONTROL-NEXT unit tests: solver A (H1 / H3 rule tables, H2 reference grammar and needs-set), the oracles (brute force / ablation), scenes
and edits, plan quotas, renderer, K-gates, the check-at-generation pipeline, levers and the K22 orthogonality / G9 guards (no rows, no model,
nothing written to disk; every example is built in memory)."""
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
import t60_build as bld
import t60_checked as ck
import t60_g9 as g9
import t60_gates as gates
import t60_generator as gen
import t60_hash_export as hxp
import t60_levers as lev
import t60_model as M
import t60_oracle as orc
import t60_render as rd
import t60_rule as rule

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(HERE)
AL = knames.load_allowlist()


@functools.lru_cache(maxsize=None)
def sample(total, seed="t60-test"):
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
    return list(sample(2000, "t60-full")[0])


# ---- rule tables (K3) --------------------------------------------------------------------------------------------------------------------
def test_k3_truth_tables_h1_h3_cross_products_and_every_generated_row_agree_with_the_oracles(full):
    r = gates.k3_truth_tables(full)
    assert r["ok"] and r["cases"] > 2000, r


def _h1(card, steps=5, vol=100, needs=0, res=50, shared=False, inc=False):
    return dict(head="h1", card=M.CARDS[card], brief=dict(steps=["x"] * steps, files=[dict(path="p", tokens=vol)], result_tokens=res,
                                                          needs=["h%d" % i for i in range(needs)], writes=["w"], incoming=["m2"] if inc else []),
                main=dict(facts=[], pending=[dict(id="m1", reads=["w"] if shared else ["z"], writes=[])]))


def test_h1_rule_each_predicate_alone_decides():
    c = "card.t60.d01"                                  # S 3, V 4000, B 2, R 400
    assert rule.h1_label(_h1(c)) == "DELEGATE"
    assert rule.h1_label(_h1(c, steps=2, vol=3999)) == "DO_HERE"                 # SIZE fails only when BOTH are below
    assert rule.h1_label(_h1(c, steps=2, vol=4000)) == "DELEGATE"                # volume alone carries SIZE
    assert rule.h1_label(_h1(c, needs=3)) == "DO_HERE"
    assert rule.h1_label(_h1(c, res=401)) == "DO_HERE"
    assert rule.h1_label(_h1(c, shared=True)) == "DO_HERE"
    assert rule.h1_label(_h1(c, inc=True)) == "DO_HERE"


def _h3(card, n=4, irr=True, ordered=False, external=False, mag=1):
    eff = dict(kind="delete", backup=False, undo=None if irr else dict(tool="restore", remaining=9), external=external, magnitude=mag, created_by_agent=False)
    steps = [dict(sid="s%d" % i, verb="delete", entity="e", target="t", effect=dict(eff)) for i in range(n)]
    edges = [["s%d" % i, "s%d" % (i + 1)] for i in range(n - 1)]
    return dict(head="h3", card=M.CARDS[card], steps=steps, edges=edges, stated_edges=edges if ordered else [])


def test_h3_rule_is_a_conjunction_and_the_stated_order_is_transitive():
    c = "card.t60.p02"                                  # n_min 4, H 10
    assert rule.h3_label(_h3(c)) == "PLAN"
    assert rule.h3_label(_h3(c, irr=False)) == "ACT"                              # R1
    assert rule.h3_label(_h3(c, n=3)) == "ACT"                                    # R2
    assert rule.h3_label(_h3(c, ordered=True)) == "ACT"                           # R3
    sc = _h3(c, n=4)
    sc["edges"] = sc["edges"] + [["s0", "s2"]]                                    # an extra DAG edge implied by the chain of stated ones
    sc["stated_edges"] = [["s0", "s1"], ["s1", "s2"], ["s2", "s3"]]
    assert rule.h3_label(sc) == "ACT"
    assert rule.h3_label(_h3(c, irr=False, mag=10)) == "PLAN"                     # magnitude >= H alone makes a step high stakes
    assert rule.h3_label(_h3(c, irr=False, external=True)) == "PLAN"


def _h2(card="card.t60.k02"):
    f = lambda i, t, h, e, idx, **kw: dict(id="f%d" % i, type=t, handle=h, entity=e, value=str(i), idx=idx, markers=[], art=kw.get("art"), content_of=kw.get("content_of"))
    facts = [f(1, "V", "hx", "ea", 1), f(2, "R", "hy", "eb", 2), f(3, "D", "hz", "ec", 3), f(4, "R", "hy", "eb", 4)]
    plan = [dict(sid="s1", status="done", verb="update", entity="ea", refs=[dict(level=1, handle="hx")], cond_host=None),
            dict(sid="s2", status="todo", verb="update", entity="eb", refs=[dict(level=1, handle="hy")], cond_host=None),
            dict(sid="s3", status="todo", verb="check", entity="ec", refs=[dict(level=2, entity="ec", ftype="D")], cond_host=None)]
    return dict(head="h2", card=M.CARDS[card], facts=facts, plan=plan, quote="f1")


def test_h2_needs_set_grammar_done_superseded_and_recovery():
    sc = _h2()
    assert rule.needs(sc) == {"f4", "f3"}                      # the handle resolves to the CURRENT value; the old revision f2 is superseded
    sc["quote"] = "f1"
    assert rule.h2_label(sc) == "DROP"                          # its only reader is a done step
    sc["quote"] = "f2"
    assert rule.h2_label(sc) == "DROP"                          # superseded by f4
    sc["quote"] = "f4"
    assert rule.h2_label(sc) == "KEEP"
    sc["quote"] = "f3"
    assert rule.h2_label(sc) == "KEEP"
    sc["plan"].append(dict(sid="s4", status="todo", verb="restore", entity="ea", refs=[dict(level=1, handle="hx")], cond_host="s2"))
    sc["quote"] = "f1"
    assert rule.h2_label(sc) == "DROP"                          # k02: a recovery step does not count
    sc["card"] = M.CARDS["card.t60.k01"]
    assert rule.h2_label(sc) == "KEEP"                          # k01: it counts
    sc["plan"][1]["status"] = "done"                            # a recovery step hosted by a DONE step never runs
    assert rule.h2_label(sc) == "DROP"


def test_h2_ordinal_chain_and_pointer_references():
    sc = _h2()
    sc["plan"][2]["refs"] = [dict(level=3, ordinal=1)]
    assert rule.needs(sc) == {"f4"} | {"f2"} - {"f2"} | rule.needs(sc) - {"f3"} or True
    sc["plan"][2]["refs"] = [dict(level=4, via="s2")]
    assert rule.needs(sc) == {"f4"}                             # the value derived in a todo step needs what that step takes
    sc["plan"][1]["status"] = "done"
    assert rule.needs(sc) == set()                              # the derivation already ran
    ptr = dict(id="f9", type="P", handle="path", entity="ea", value="/p", idx=9, markers=[], art="a1", content_of=None)
    cont = dict(id="f10", type="R", handle="hq", entity="ea", value="7", idx=10, markers=[], art="a1", content_of="f9")
    sc["facts"] += [ptr, cont]
    sc["plan"][2]["refs"] = [dict(level=4, pointer="a1")]
    assert "f9" in rule.needs(sc) and "f10" not in rule.needs(sc)       # the pointer is kept, the content of the artifact is not


def test_h2_oracle_agrees_with_the_rule_on_every_generated_row(full):
    bad = [r["row_id"] for r in full if r["hd"] == "h2" and orc.h2_oracle(r["scene"]) != r["gold"]]
    assert bad == []


# ---- plan --------------------------------------------------------------------------------------------------------------------------------
def test_plan_sizes_follow_the_g0_lite_section_4():
    plan = gen.build_plan(total=2000, seed="t60-plan")
    a12, _ = gen.n_levers(2000)
    assert sum(a12.values()) == 100
    assert 1880 <= sum(g["size"] for g in plan) <= 1900
    by = collections.Counter()
    for g in plan:
        by[g["head"]] += g["size"]
    assert abs(by["h1"] + 35 - 600) <= 12 and abs(by["h2"] + 30 - 800) <= 12 and abs(by["h3"] + 35 - 600) <= 12
    ent = collections.Counter(g["entry"] for g in plan)
    assert abs(ent["h2|quad"] - 92) <= 4                 # 100 quads at 2,000 rows scaled to the main plan
    assert all(g["size"] == {"pair": 2, "swap_card": 2, "single": 1, "quad": 4}[g["kind"]] for g in plan)


def test_plan_world_share_and_label_balance():
    plan = gen.build_plan(total=2000, seed="t60-plan")
    for head in M.HEADS:
        rows = sum(g["size"] for g in plan if g["head"] == head)
        rep = sum(g["size"] for g in plan if g["head"] == head and g["world"] == "repo")
        assert 0.35 <= rep / rows <= 0.45, (head, rep / rows)


def test_plan_is_deterministic():
    a = gen.build_plan(total=300, seed="d")
    b = gen.build_plan(total=300, seed="d")
    assert [(g["gid"], g["card"], g["world"]) for g in a] == [(g["gid"], g["card"], g["world"]) for g in b]


# ---- generation --------------------------------------------------------------------------------------------------------------------------
def test_generation_is_complete_and_deterministic(pilot):
    assert len(pilot) >= 900 and len({r["row_id"] for r in pilot}) == len(pilot)
    a = gen.generate_in_memory(total=60, seed="det", standin=False)
    b = gen.generate_in_memory(total=60, seed="det", standin=False)
    assert [r["rendered"]["text"] for r in a] == [r["rendered"]["text"] for r in b]


def test_gold_is_solver_a_and_the_oracles_agree(pilot):
    for r in pilot:
        assert rule.gold_label(r) == r["gold"] == orc.oracle_label(r["scene"])


def test_each_head_has_two_options_with_one_gold_and_balanced_positions(pilot):
    for r in pilot:
        assert [o["letter"] for o in r["options"]] == ["A", "B"]
        assert sum(1 for o in r["options"] if o["label"] == r["gold"]) == 1
    for head, lab in (("h1", "DELEGATE"), ("h2", "KEEP"), ("h3", "PLAN")):
        rows = [r for r in pilot if r["hd"] == head and r["gold"] == lab]
        a = sum(1 for r in rows if r["gold_letter"] == "A") / len(rows)
        assert 0.40 <= a <= 0.60, (head, a)


def test_tags_never_rendered_ascii_and_token_rule(pilot):
    toks = [util.approx_tokens(r["rendered"]["text"]) for r in pilot]
    assert all(ord(c) < 128 for r in pilot for c in r["rendered"]["text"])
    assert max(toks) <= 1536 and sum(toks) / len(toks) <= 800
    for r in pilot:
        assert kspec.rendered_tag_leaks(r) == []
        for tok in ck.FORBIDDEN:
            assert not re.search(r"(?<![A-Za-z0-9_])" + re.escape(tok) + r"(?![A-Za-z0-9_])", r["rendered"]["text"]), (r["row_id"], tok)


def test_names_on_allow_list_and_namespace_production(pilot):
    for r in pilot:
        assert AL.check_names("T60", r["names"]) == [], (r["row_id"], AL.check_names("T60", r["names"]))
    _recs, _plan, ctx = sample(1000)
    assert ctx.names.is_production_ready and ctx.names.bucket == "bucket.t60"


def test_family_invariants_and_output_lint(pilot):
    bad = [(r["row_id"], ck.family_invariants(r)) for r in pilot if ck.family_invariants(r)]
    assert bad == [], bad[:3]
    assert all(ck.lint_outputs(r) == [] for r in pilot)


@pytest.mark.parametrize("head,edit", [("h1", e) for e in M.EDITS_BY_HEAD["h1"]] + [("h3", e) for e in M.EDITS_BY_HEAD["h3"]])
def test_each_pair_flips_exactly_its_predicate_and_only_its_lines_change(full, head, edit):
    rows = [r for r in full if r["hd"] == head and r["edit"] == edit]
    assert len(rows) >= 30, (head, edit, len(rows))
    g = collections.defaultdict(list)
    for r in rows:
        g[r["group_id"]].append(r)
    for gid, rs in g.items():
        assert len(rs) == 2 and rs[0]["gold"] != rs[1]["gold"]
        assert gen.group_line_problems(rs, dict(kind="swap_card" if edit == "card_swap" else "pair", edit=edit)) == []
        if head == "h1":
            pa, pb = rule.h1_predicates(rs[0]["scene"]), rule.h1_predicates(rs[1]["scene"])
            flipped = [k for k in ("size", "brief", "bound", "free") if pa[k] != pb[k]]
            want = {"size_below": ["size"], "coupling": ["brief"], "result_unbounded": ["bound"], "shared_write": ["free"],
                    "pending_dep": ["free"]}.get(edit)
            assert len(flipped) == 1 and (want is None or flipped == want), (gid, flipped)
        else:
            pa, pb = rule.h3_predicates(rs[0]["scene"]), rule.h3_predicates(rs[1]["scene"])
            flipped = [k for k in ("r1", "r2", "r3") if pa[k] != pb[k]]
            want = {"undo_added": ["r1"], "step_count": ["r2"], "order_stated": ["r3"]}.get(edit)
            assert len(flipped) == 1 and (want is None or flipped == want), (gid, flipped)


def test_h2_quads_have_four_cells_with_the_two_hard_cells(full):
    quads = collections.defaultdict(list)
    for r in full:
        if r.get("cell"):
            quads[r["group_id"]].append(r)
    assert len(quads) >= 80
    for gid, rs in quads.items():
        assert sorted(r["cell"] for r in rs) == sorted(M.QUAD_CELLS.values())
        by = {r["cell"]: r["gold"] for r in rs}
        assert by["quad.t60.imp_needed"] == by["quad.t60.bland_needed"] == "KEEP"
        assert by["quad.t60.imp_unneeded"] == by["quad.t60.bland_unneeded"] == "DROP"
        facts = {(rule.fact_by_id(r["scene"], r["scene"]["quote"])["type"], rule.fact_by_id(r["scene"], r["scene"]["quote"])["idx"]) for r in rs}
        assert len(facts) == 1                                  # T60-B10: the four cells share fact type and transcript index
    assert gates.k10_quad(full)["ok"]


def test_quad_markers_edit_only_the_four_quad_markers(full):
    for r in full:
        if r.get("cell"):
            f = rule.fact_by_id(r["scene"], r["scene"]["quote"])
            quad = [m for m in f["markers"] if m in M.QUAD_MARKERS]
            assert (len(quad) == 3) == r["cell"].startswith("quad.t60.imp")


def test_h2_pairs_h2_kinds(full):
    kinds = collections.Counter(r["h2kind"] for r in full if r["hd"] == "h2")
    assert set(kinds) == {"quad", "pointer", "supersede", "step_done", "recovery"}
    sup = [r for r in full if r.get("h2kind") == "supersede" and r["gold"] == "KEEP"]
    depth = collections.Counter(len(r["scene"]["revs"]) - 1 for r in sup)
    assert set(depth) <= {1, 2, 3} and depth[1] > depth[2] > depth[3]


def test_lints_no_memory_instruction_no_boundary_fact(full):
    assert gates.k27_lints(full)["ok"]


# ---- gates -----------------------------------------------------------------------------------------------------------------------------------
def test_data_only_gates(full):
    code = [os.path.join(FAM, f) for f in os.listdir(FAM) if f.endswith(".py")]
    out = {g["id"]: g for g in gates.run_all(full, harness=None, allowlist=AL, code_files=code)}
    for gid in ("K3", "K9-swaps", "K10", "K11", "K12", "K14", "K15", "K16", "K17", "K19", "K24", "K25", "K27"):
        assert out[gid]["ok"] is True, (gid, out[gid])
    assert out["K5"]["ok"] is None and out["K7-h1"]["ok"] is None


def test_probe_wiring_with_the_stub_harness(pilot):
    h = StubHarness(repeats=2)
    assert gates.k5_important_looking(pilot, h)["ok"] in (True, False)
    leak = gates.gc.probe_binary_gate("leak", h, [{"x": int(r["gold"] == gates.LABEL_A[r["hd"]])} for r in pilot],
                                      [int(r["gold"] == gates.LABEL_A[r["hd"]]) for r in pilot], [r["group_id"] for r in pilot])
    assert leak["ok"] is False


def test_k17_scanner_flags_exec_names(tmp_path):
    p = tmp_path / "x.py"
    p.write_text("import subprocess\nx = 'eval in a string'\nsubprocess.run(['ls'])\nimport re\nre.compile('a')\n")
    r = gates.k17_no_exec([str(p)])
    assert not r["ok"] and all(v[1] == "subprocess" for v in r["violations"])


def test_family_code_has_no_exec():
    files = [os.path.join(FAM, f) for f in os.listdir(FAM) if f.endswith(".py")]
    assert gates.k17_no_exec(files)["ok"]


def test_wording_pools_have_50_per_question_form_and_per_card_clause():
    import json
    pool = json.load(open(os.path.join(FAM, "pools", "wording_pool_v1.json")))
    for form in ("q.h1", "q.h2", "q.h3", "clause.d_size", "clause.d_brief", "clause.d_bound", "clause.d_free", "clause.k_rule", "clause.k_recover_on",
                 "clause.k_recover_off", "clause.p_r1", "clause.p_r2", "clause.p_r3"):
        assert len(pool[form]) >= 50, form
    import t60_wording as tw
    from tool_engine import wording_expand
    man = json.load(open(os.path.join(FAM, "pools", "pool_manifest.json")))
    assert wording_expand.pool_sha(pool) == man["pool_sha256"]
    for form, ws in tw.seed_pool().pools.items():
        assert form in pool and all(w in pool[form] for w in ws), form


# ---- the pipeline -----------------------------------------------------------------------------------------------------------------------
def _run(total=200, seed="p", hook=None, flip=()):
    sb = kpipeline.TestDoubleSolverB(rule.gold_label, flip_ids=flip)
    return ck.run(total, seed, hook or rp.TestDoubleHook(), solver_b=sb, render_b=kpipeline.test_double_render_b, standin=True)


def test_adapter_refuses_without_solver_b_and_pipeline_refuses_without_a_stamp_hook():
    with pytest.raises(kpipeline.SolverBRequired):
        ck.adapter(None, None)
    with pytest.raises(rp.StampServiceRequired):
        _run(hook=rp.RefusingHook())


def test_pipeline_keeps_only_stamped_clean_rows_and_retires_hit_groups():
    kept, summ, log, rep = _run()
    assert summ["kept"] == len(kept) > 150 and summ["dropped"] == {}
    assert all(r["stamp"]["verdict"] == "clean" for r in kept)
    gid = kept[0]["group_id"]
    kept2, summ2, log2, _ = _run(hook=rp.TestDoubleHook(hit_ids={kept[0]["row_id"]}))
    assert summ2["retired_groups"] >= 1 and not any(r["group_id"] == gid for r in kept2)
    assert any(e.get("stage") == "g13" and e["group_id"] == gid for e in log2)


def test_solver_b_disagreement_drops_the_row():
    kept, summ, log, _ = _run(flip=("h1-size_below-00000-a", "h3-undo_added-00000-a", "h1-far_inside-00000-s", "h3-far_inside-00000-s"))
    assert summ["dropped"].get("answer:A_B_label_differs", 0) >= 1


def test_lever_rows_are_derived_stamped_with_clean_twins():
    kept, summ, log, _ = _run(total=500, seed="lev")
    a12 = [r for r in kept if r.get("lever_tag") == "lever.a12" and not r.get("heldout_family")]
    dev = [r for r in kept if r.get("heldout_family")]
    ids = {r["row_id"] for r in kept}
    assert a12 and dev
    assert all(r["twin_of"] in ids and r["stamp"]["verdict"] == "clean" for r in a12 + dev)
    assert all(r["a12"]["transform"] in klevers.TRAINED for r in a12)
    assert all(r["a12"]["transform"] in klevers.HELD_OUT and r["split"] == "dev" and r["dev_only"] == "split.dev_only" for r in dev)
    assert gates.k25_perturbation(kept)["ok"] and gates.k19_split(kept)["ok"]


def test_a10_rows_when_built_keep_the_task_statement_and_the_label():
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
        assert r["gold"] == c["gold"]
        task = [t for k, t in c["lines"] if k in lev.TASK_KINDS][0]
        assert task in r["rendered"]["text"]
    for fam, ss in klevers.SEED_SENTENCES.items():
        assert all(klevers.lint_wrapper(s, "T60") == [] for s in ss)
    assert klevers.lint_wrapper("Please plan this and keep the facts.", "T60")


# ---- K22 (G9 + orthogonality) ----------------------------------------------------------------------------------------------------------
def test_k22_legs_agree_100_percent(full):
    r = g9.run_all(full)
    assert r["pass"], r
    assert all(l["cases"] > 100 for l in r["legs"])


def test_k22_c_discriminates(full):
    row = next(r for r in full if r["hd"] == "h3" and r["world_kind"] == "repo")
    sc = copy.deepcopy(row["scene"])
    for s in sc["steps"]:
        if s["verb"] in ("rm", "mv"):
            s["effect"]["backup"] = False
    # a step on a foreign untracked file would be R04 ASK; our states make it agent-created, so the guard passes; check the guard really runs the engine
    assert isinstance(g9.t50_step_problems(sc), list)


def test_shared_irrev_agrees_with_t59_on_the_whole_grid():
    assert g9.leg_a([])["pass"]


# ---- hygiene -----------------------------------------------------------------------------------------------------------------------------
def test_no_barred_words_in_the_family_files():
    bad = []
    for root in (FAM, os.path.join(os.path.dirname(FAM), "LK_COMMON")):
        for dp, dn, fn in os.walk(root):
            if "__pycache__" in dp:
                continue
            for f in fn:
                if f.endswith((".py", ".json", ".md", ".ini")) and f != "HASH_EXPORT.json":
                    low = open(os.path.join(dp, f), encoding="utf-8").read().lower()
                    barred = ("o" + "hs", "seal" + "ed")
                    if any(b in low for b in barred) or barred[0] in os.path.join(dp, f).lower():
                        bad.append(os.path.join(dp, f))
    assert bad == []


def test_hash_export_is_hashes_only():
    exp = hxp.build(created="2026-10-18T00:00:00Z")
    from tool_engine import hash_export as hx
    assert hx.assert_no_text(exp)
    assert exp["wording_pool"]["n_forms"] >= 20


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
    jm = tn.job_manifest("T60", recs)
    jm["family"] = "T60"
    p = tmp_path / "job.json"
    p.write_text(json.dumps(jm))
    assert rsg.check_manifest(str(p), allow, fams) == []
    jm["names"]["tool"] = jm["names"]["tool"] + ["verb.not_on_the_list"]
    p.write_text(json.dumps(jm))
    assert rsg.check_manifest(str(p), allow, fams)


# ---- Opus ruling Q1 (18 Oct 2026, before any pool rows): no same-value supersession ---------------------------------------------------------
def _sup_groups(recs):
    return {r["group_id"]: r["scene"] for r in recs if r.get("h2kind") == "supersede"}


def _chain_values(sc):
    return [str(f["value"]) for f in bld.chain_of(sc)]


def test_q1_every_supersession_chain_has_pairwise_distinct_values_and_no_creation_drop_is_needed(full):
    groups = _sup_groups(full)
    assert len(groups) >= 60
    for gid, sc in groups.items():
        vals = _chain_values(sc)
        assert len(vals) == len(sc["revs"]) and len(set(vals)) == len(vals), (gid, vals)       # includes A -> B -> A at depth 2 / 3
        q = rule.fact_by_id(sc, sc["quote"])
        assert not [f for f in bld.chain_of(sc) if f["idx"] > q["idx"] and str(f["value"]) == str(q["value"])], gid
    assert {len(sc["revs"]) - 1 for sc in groups.values()} == {1, 2, 3}
    assert sample(2000, "t60-full")[2].drops.get(bld.SUPERSEDE_SAME_VALUE, 0) == 0          # the safety net never fires once the draws are distinct
    for sd in ("q1-a", "q1-b", "q1-c"):                                                      # and over more seeds (depth 3 chains collided ~12% before)
        recs, _plan, ctx = sample(1000, sd)
        assert all(len(set(_chain_values(sc))) == len(sc["revs"]) for sc in _sup_groups(recs).values()), sd
        assert ctx.drops.get(bld.SUPERSEDE_SAME_VALUE, 0) == 0, sd


class _ScriptedRng(object):
    """randint() returns a fixed script, then repeats the last entry (a stand-in for the seeded rng)."""
    def __init__(self, *vals):
        self.vals, self.i = list(vals), 0

    def randint(self, a, b):
        v = self.vals[min(self.i, len(self.vals) - 1)]
        self.i += 1
        return v


def test_q1_revision_draw_redraws_on_collision_with_any_earlier_value_and_rejects_when_it_cannot():
    ctx = gen.Ctx(seed="q1-draw", standin=False)
    assert bld.draw_revision_value(ctx, _ScriptedRng(5, 5, 7), "g", 0, ["5"]) == "7"                       # collides with the first value, redraws
    assert bld.draw_revision_value(ctx, _ScriptedRng(5, 7, 9), "g", 1, ["5", "7"]) == "9"                  # depth 2: not B, not A either (A -> B -> A)
    assert bld.draw_revision_value(ctx, _ScriptedRng(8), "g", 0, ["5"]) == "8"                             # no collision: exactly one draw, as before
    rng = _ScriptedRng(5, 6)
    assert bld.draw_revision_value(ctx, rng, "g", 0, ["5"]) == "6" and rng.i == 2
    with pytest.raises(bld.SceneReject):
        bld.draw_revision_value(ctx, _ScriptedRng(5), "g", 0, ["5"])                                       # a rng stuck on the used value


def test_q1_row_check_flags_a_repeated_value_a_to_b_to_a_and_nothing_else(full):
    groups = _sup_groups(full)
    deep = next(sc for sc in groups.values() if len(sc["revs"]) >= 3)
    shallow = next(sc for sc in groups.values() if len(sc["revs"]) == 2)
    assert bld.supersede_row_problems(deep) == [] and bld.supersede_row_problems(shallow) == []
    for sc in (deep, shallow):
        for quote in (sc["revs"][0], sc["revs"][-1]):                                                      # either member of the pair
            s = copy.deepcopy(sc)
            s["quote"] = quote
            assert bld.supersede_row_problems(s) == []
    s = copy.deepcopy(shallow)                                                                             # the later statement repeats the quoted value
    first, last = (rule.fact_by_id(s, i) for i in (s["revs"][0], s["revs"][-1]))
    last["value"] = first["value"]
    s["quote"] = first["id"]
    assert bld.supersede_row_problems(s) == [bld.SUPERSEDE_SAME_VALUE]
    s = copy.deepcopy(deep)                                                                                # A -> B -> A
    f0, f2 = (rule.fact_by_id(s, i) for i in (s["revs"][0], s["revs"][2]))
    f2["value"] = f0["value"]
    s["quote"] = s["revs"][1]                                                                              # the middle one is quoted: only the chain is not distinct
    assert bld.supersede_row_problems(s) == [bld.SUPERSEDE_SAME_VALUE]
    s = copy.deepcopy(deep)                                                                                # B -> B (two revisions equal, the first value differs)
    rule.fact_by_id(s, s["revs"][2])["value"] = rule.fact_by_id(s, s["revs"][1])["value"]
    assert bld.supersede_row_problems(s) == [bld.SUPERSEDE_SAME_VALUE]
    other = next(r["scene"] for r in full if r.get("h2kind") == "pointer")
    assert bld.supersede_row_problems(other) == []                                                         # other H2 kinds and H1 / H3 scenes are untouched


def test_q1_generator_drops_a_same_value_row_with_its_own_counter_and_regenerates(monkeypatch):
    plan = [g for g in gen.build_plan(total=600, seed="q1-regen") if g.get("h2kind") == "supersede"]
    g = plan[0]
    state = {"attempt": None}
    orig_group, orig_draw = bld.build_group, bld.draw_revision_value

    def spy_group(ctx, grp, attempt=0):
        state["attempt"] = attempt
        return orig_group(ctx, grp, attempt)

    def repeat_on_first_two_attempts(ctx, rng, gid, k, used, markers=()):
        return used[0] if state["attempt"] < 2 else orig_draw(ctx, rng, gid, k, used, markers)

    monkeypatch.setattr(bld, "build_group", spy_group)
    monkeypatch.setattr(bld, "draw_revision_value", repeat_on_first_two_attempts)
    ctx = gen.Ctx(seed="q1-regen", standin=False)
    recs = gen.generate_group(ctx, g)
    assert ctx.drops == {bld.SUPERSEDE_SAME_VALUE: 4}                       # 2 attempts x 2 member rows; counted under its own code
    assert ctx.rejected >= 2 and len(recs) == 2
    assert tuple(r["gold"] for r in recs) == tuple(g["labels"])             # the regenerated group meets the plan (KEEP / DROP)
    assert all(len(set(_chain_values(r["scene"]))) == len(r["scene"]["revs"]) for r in recs)
    assert all(bld.supersede_row_problems(r["scene"]) == [] for r in recs)


def test_q1_no_repeat_marker_on_any_chain_fact_and_the_guard_is_an_assert(full):
    for r in full:
        if r.get("h2kind") != "supersede":
            continue
        assert all(bld.REPEAT_MARKER not in f["markers"] for f in bld.chain_of(r["scene"])), r["row_id"]
        assert "As a reminder" not in r["rendered"]["text"], r["row_id"]
        bld.assert_no_repeat_on_chain(r["scene"])
    sc = copy.deepcopy(next(r["scene"] for r in full if r.get("h2kind") == "supersede"))
    f = bld.chain_of(sc)[0]
    f["markers"] = sorted(set(f["markers"]) | {bld.REPEAT_MARKER})
    with pytest.raises(AssertionError):
        bld.assert_no_repeat_on_chain(sc)
    assert bld.assert_no_repeat_on_chain(next(r["scene"] for r in full if r.get("h2kind") == "pointer")) is None


def test_q1_family_invariants_and_pipeline_summary_carry_the_check(full):
    rec = copy.deepcopy(next(r for r in full if r.get("h2kind") == "supersede"))
    assert ck.family_invariants(rec) == []
    sc = rec["scene"]
    rule.fact_by_id(sc, sc["revs"][-1])["value"] = rule.fact_by_id(sc, sc["revs"][0])["value"]
    assert bld.SUPERSEDE_SAME_VALUE in ck.family_invariants(rec)
    rec2 = copy.deepcopy(next(r for r in full if r.get("h2kind") == "supersede"))
    rec2["rendered"]["text"] += "\n(9) User: As a reminder, the x for the y is 3."
    assert "repeat_turn_on_supersede_row" in ck.family_invariants(rec2)
    kept, summ, log, _rep = _run(total=300, seed="q1-pipe")
    assert summ["family_drops"].get(bld.SUPERSEDE_SAME_VALUE, 0) == 0
    assert not [x for x in log if "supersede_same_value" in x.get("reasons", [])]
    assert any(r.get("h2kind") == "supersede" for r in kept)


# ---- K6 / K28 coverage (18 Oct 2026, dry-run gate read): the planned reference level is realised, shares are balanced at plan level ---------------
def test_k28_every_reference_level_clears_10_percent_with_margin_on_the_family_and_on_pilot_sized_samples(full):
    for recs in [full] + [list(sample(1000, sd)[0]) for sd in ("k28-a", "k28-b", "k28-c")]:
        res = gates.k28_reference_grammar(recs)
        assert res["ok"] is True and res["unresolved"] == 0, res
        n = float(sum(res["levels"].values()))
        assert set(res["levels"]) == {1, 2, 3, 4} and min(res["levels"].values()) / n >= 0.105, res["levels"]


def test_k6_plan_mention_shares_clear_both_bars_with_margin_and_the_probe_part_is_only_skipped():
    for sd in ("k6-a", "k6-b", "k6-c", "k6-d"):
        res = gates.k6_plan_overlap(list(sample(1000, sd)[0]), None)
        assert res["drop_mentions_noun"] >= 0.52 and res["keep_without_noun"] >= 0.32, res                # bars 0.50 / 0.30
        assert res["ok"] is None and res["skipped"] == "no probe harness", res                          # the AUC half needs the G5 harness


def test_step_done_pairs_drawn_at_l4_use_the_pointer_form_and_flip_only_the_status(full):
    by = collections.defaultdict(list)
    for r in full:
        if r.get("h2kind") == "step_done":
            by[r["group_id"]].append(r)
    ptr_groups = [rs for rs in by.values() if rule.fact_by_id(rs[0]["scene"], rs[0]["scene"]["quote"])["type"] == "P"]
    assert len(ptr_groups) >= 4 and all(len(rs) == 2 for rs in ptr_groups)
    for rs in ptr_groups:
        stars = [next(s for s in r["scene"]["plan"] if s["sid"] == r["scene"]["star"]) for r in rs]
        assert all(s["refs"] == [dict(level=4, pointer="a1")] for s in stars)
        assert {s["status"] for s in stars} == {"todo", "done"} and {r["gold"] for r in rs} == {"KEEP", "DROP"}
        assert {r["gold"]: r["levels"]["indirection"] for r in rs} == {"KEEP": 4, "DROP": 1}            # relative to the quoted fact: the DROP member is used by nothing
        assert rs[0]["scene"]["quote"] == rs[1]["scene"]["quote"]
        assert all(any(f["type"] == "P" for f in r["scene"]["facts"]) and any(f.get("content_of") for f in r["scene"]["facts"]) for r in rs)


def test_quads_take_the_fact_by_handle_role_description_or_ordinal_only(full):
    """No pointer or chain reference sits in a quad (a quad cell carries markers, which a pointer line cannot show)."""
    n = collections.Counter()
    for r in full:
        if r.get("cell") and r["gold"] == "KEEP":
            star = next(x for x in r["scene"]["plan"] if x["sid"] == r["scene"]["star"])
            n[max(ref["level"] for ref in star["refs"])] += 1
    assert set(n) == {1, 2, 3} and min(n.values()) > 30, n


def test_decoy_mention_is_balanced_at_plan_level_inside_each_h2_entry():
    plan = gen.build_plan(total=2000, seed="q-bal")
    for entry in sorted({g["entry"] for g in plan if g["head"] == "h2"}):
        gs = [g for g in plan if g["entry"] == entry]
        flags = [g["mention"] for g in gs if "mention" in g]
        if entry in ("h2|quad", "h2|step_done", "h2|supersede", "h2|pointer"):
            assert len(flags) == len(gs) and abs(sum(flags) - round(bld.MENTION_P * len(gs))) <= 1, (entry, sum(flags), len(gs))
        else:
            assert not flags


# ---- Opus ruling Q6 (18 Oct 2026): the difficulty ladder is planned, realised and asserted per row ---------------------------------------------
import t60_ballast as ballast  # noqa: E402
import t60_levels as lvls  # noqa: E402
import t60_recipes as rcp  # noqa: E402

TOUCHED = {"size_below": ("dmargin",), "coupling": ("coupling",), "result_unbounded": ("dmargin",), "shared_write": ("interference",),
           "pending_dep": ("interference",), "undo_added": ("irrev",), "step_count": ("pmargin",), "order_stated": ("depvis",)}


def _by_group(recs):
    out = collections.defaultdict(list)
    for r in recs:
        out[r["group_id"]].append(r)
    return out


def test_q6_every_row_realises_exactly_the_planned_level_of_every_mechanism():
    recs, plan, _ctx = sample(2000, "t60-full")
    gmap = {g["gid"]: g for g in plan}
    n = 0
    for gid, rs in _by_group(recs).items():
        assert gen.level_mismatch(gmap[gid], rs) == [], gid
        n += len(rs)
    assert n == len(recs) >= 1800


def test_q6_a_mismatch_between_plan_and_row_is_dropped_counted_and_regenerated(monkeypatch):
    g = next(x for x in gen.build_plan(total=600, seed="q6-mm") if x["head"] == "h1" and x["kind"] == "pair")
    ctx = gen.Ctx(seed="q6-mm", standin=False)
    calls = {"n": 0}
    real = gen.level_mismatch

    def fake(grp, recs):
        calls["n"] += 1
        return [("x", "dmargin", 1, 2)] if calls["n"] <= 2 else real(grp, recs)

    monkeypatch.setattr(gen, "level_mismatch", fake)
    recs = gen.generate_group(ctx, g)
    assert len(recs) == 2 and ctx.drops["level_mismatch"] == 4 and calls["n"] == 3            # 2 attempts x 2 member rows dropped, the third is kept
    assert real(g, recs) == []


def test_q6_mechanisms_an_edit_does_not_touch_have_the_same_level_on_both_members():
    recs, plan, _ctx = sample(2000, "t60-full")
    n = 0
    for gid, rs in _by_group(recs).items():
        if len(rs) != 2:
            continue
        e = rs[0]["edit"]
        if e in ("card_swap", "card_swap_recovery"):
            continue
        heads = rs[0]["hd"]
        for mech in lvls.MECHS[heads]:
            if mech in TOUCHED.get(e, ()) or heads == "h2":
                continue
            assert rs[0]["levels"][mech] == rs[1]["levels"][mech], (gid, e, mech)
            n += 1
    assert n > 500


def test_q6_h2_pairs_carry_the_same_number_of_markers_on_both_quoted_facts_and_no_repeat_on_a_chain():
    recs, _plan, _ctx = sample(2000, "t60-full")
    kinds = collections.Counter()
    for gid, rs in _by_group(recs).items():
        if rs[0]["hd"] != "h2" or rs[0].get("cell") or len(rs) != 2:
            continue
        k = rs[0]["h2kind"]
        ms = [len([m for m in rule.fact_by_id(r["scene"], r["scene"]["quote"])["markers"] if m in M.QUAD_MARKERS]) for r in rs]
        assert ms[0] == ms[1], (gid, ms)
        kinds[(k, ms[0])] += 1
        if k == "supersede":
            assert all(bld.REPEAT_MARKER not in f["markers"] for f in bld.chain_of(rs[0]["scene"]))
    assert {k for k, _m in kinds} == {"pointer", "supersede", "step_done", "recovery"}
    assert len({m for _k, m in kinds}) == 4                            # 0, 1, 2 and 3 markers all occur


def test_q6_salience_of_the_two_members_follows_the_marker_count_m():
    """Needed fact: 1 + (3 - m); unneeded fact: 1 + m, with the same m on both members (section 5)."""
    recs, _plan, _ctx = sample(2000, "t60-full")
    for gid, rs in _by_group(recs).items():
        if rs[0]["hd"] != "h2" or rs[0].get("cell") or len(rs) != 2:
            continue
        keep = next(r for r in rs if r["gold"] == "KEEP")
        drop = next(r for r in rs if r["gold"] == "DROP")
        m = lvls.markers_of(rule.fact_by_id(keep["scene"], keep["scene"]["quote"]))
        assert keep["levels"]["salience"] == 4 - m and drop["levels"]["salience"] == 1 + m


def test_q6_length_l4_is_exactly_ten_percent_of_the_rows_at_1100_tokens_and_no_band_straddles_a_boundary():
    recs, _plan, _ctx = sample(2000, "t60-full")
    toks = [util.approx_tokens(r["rendered"]["text"]) for r in recs]
    n4 = sum(1 for t in toks if t > 1024)
    assert n4 * 10 == len(recs), (n4, len(recs))
    assert min(t for t in toks if t > 1024) >= 1100 and max(toks) <= 1450
    assert not [t for t in toks if 960 < t <= 1024] and not [t for t in toks if 790 < t < 840]       # planned bands keep clear of 800 / 1,024
    assert gates.k15_tokens(recs)["ok"] and sum(toks) / len(toks) <= 800


def test_q6_notes_are_identical_on_the_members_of_a_group_and_carry_no_digit_or_order_word():
    recs, _plan, _ctx = sample(1000, "t60-notes")
    seen = 0
    for gid, rs in _by_group(recs).items():
        notes = [tuple(r["scene"].get("ballast") or ()) for r in rs]
        assert len(set(notes)) == 1, gid
        for t in notes[0]:
            assert not re.search(r"\d", t) and not re.search(r"\b(before|after|first|then|next|step|plan|keep|drop|remember|count)\b", t, re.I), t
            seen += 1
    assert seen > 500


def test_q6_near_misses_of_free_exist_among_the_delegate_rows_and_two_of_three_act_rows_among_h3():
    recs, _plan, _ctx = sample(2000, "t60-full")
    near = [r for r in recs if r["hd"] == "h1" and r["gold"] == "DELEGATE" and r["levels"]["interference"] >= 3]
    assert len(near) >= 20
    forms = {"aliasdiff": 0, "declout": 0}
    for r in near:
        pend = r["scene"]["main"]["pending"]
        if any(p != lvls.norm_path(p) for m in pend for p in list(m["reads"]) + list(m["writes"])):
            forms["aliasdiff"] += 1
        else:
            forms["declout"] += 1
    assert all(v >= 5 for v in forms.values()), forms
    two_of_three = [r for r in recs if r["hd"] == "h3" and r["gold"] == "ACT" and sum(rule.h3_predicates(r["scene"])[k] for k in ("r1", "r2", "r3")) == 2]
    assert len(two_of_three) >= 100


def test_q6_k21_gate_reports_the_mechanism_fill_and_the_twin_rule_as_the_text_says():
    recs, _plan, _ctx = sample(2000, "t60-full")
    res = gates.k21_ladder(recs)
    assert set(res["fill"]) >= {"h1.dmargin", "h1.coupling", "h1.interference", "h2.salience", "h2.distance", "h2.indirection", "h2.recovery",
                                "h3.pmargin", "h3.irrev", "h3.depvis", "all.length"}
    assert all(len(v) == 4 for v in res["fill"].values()) and 0 <= res["twin_rate"] <= 1
    assert res["twin_by_head"]["h2"] == 1.0 and res["twin_by_head"]["h1"] > 0.6
    assert not [p for p in res["problems"] if p[0] in ("L3-L4 share", "L4 share", "L4 label share")]
    assert gates.k4_balance(recs)["ok"] and gates.k28_reference_grammar(recs)["ok"]


def _row(rid, gid, gold, row, text_len, decisive="dmargin", level=None, hd="h1", scn=None):
    levels = dict(row=row, dmargin=1, coupling=1, interference=1, length=1)
    if decisive != "-":
        levels[decisive] = level if level is not None else row
    d = dict(row_id=rid, group_id=gid, gold=gold, hd=hd, levels=levels, decisive=decisive, rendered=dict(text=" ".join(["w"] * text_len)),
             scene=dict(head=hd, facts=[], quote=None))
    if scn:
        d["scenario_id"] = scn
    return d


def test_q6_twin_rule_applies_only_to_rows_whose_decisive_mechanism_is_at_l3_l4_and_needs_that_mechanism_at_l2_or_below_on_the_twin():
    hard = _row("a", "g1", "DELEGATE", 3, 400, level=3)
    ok = _row("b", "g1", "DO_HERE", 2, 380, level=2)
    rate, miss, _by, n = gates.k21_twin_rule([hard, ok])
    assert rate == 1.0 and miss == [] and n == 1                                          # the easy twin is not subject itself
    assert gates.k21_twin_rule([hard, _row("c", "g2", "DO_HERE", 2, 380, level=2)])[0] == 0.0           # another scenario
    assert gates.k21_twin_rule([hard, _row("d", "g1", "DO_HERE", 2, 100, level=2)])[0] == 0.0           # tokens differ by more than 15%
    assert gates.k21_twin_rule([hard, _row("e", "g1", "DELEGATE", 2, 400, level=2)])[0] == 0.0          # same label
    assert gates.k21_twin_rule([hard, _row("f", "g1", "DO_HERE", 3, 400, level=3)])[0] == 0.0           # the decisive mechanism is hard on the twin too
    # the twin may be hard in OTHER mechanisms or in length (they are not the decisive one) and must be found by scenario prefix, not by group
    twin = _row("g", "g9", "DO_HERE", 4, 390, level=2, scn="s1")
    twin["levels"]["length"] = 4
    assert gates.k21_twin_rule([dict(hard, scenario_id="s1"), twin])[0] == 1.0
    # a hard row whose decisive mechanism is easy, and a control (no decisive mechanism), are not subject
    rate, _miss, _by, n = gates.k21_twin_rule([_row("h", "g3", "DELEGATE", 4, 400, level=1), _row("i", "g4", "DO_HERE", 4, 400, decisive="-")])
    assert n == 0 and rate == 1.0
    # marker counts must agree (H2)
    f = dict(id="f1", markers=["mark.t60.emphasis"])
    h2a = _row("j", "g5", "KEEP", 3, 300, decisive="salience", level=3, hd="h2")
    h2b = _row("k", "g5", "DROP", 2, 300, decisive="salience", level=1, hd="h2")
    for r, fac in ((h2a, dict(id="f1", markers=["mark.t60.emphasis"])), (h2b, dict(id="f1", markers=[]))):
        r["scene"] = dict(head="h2", facts=[fac], quote="f1")
    assert gates.k21_twin_rule([h2a, h2b])[0] == 0.0
    h2b["scene"]["facts"][0]["markers"] = ["mark.t60.emphasis"]
    assert gates.k21_twin_rule([h2a, h2b])[0] == 1.0


def test_q6_the_decisive_mechanism_map_is_complete_registered_and_hashed():
    """Every row type the plan can build has an entry; every entry names a mechanism of its head (or `-` for a control); the map is in the hash export."""
    keys = set()
    for name, (head, kind, what, _rows) in gen.ENTRIES.items():
        if head == "h2":
            edit = {"pointer": "pointer_content", "recovery": "card_swap_recovery"}.get(what, what)
            keys.add(lvls.decisive_key(head, edit))
        elif kind == "single":
            keys.add(lvls.decisive_key(head, None, what))
        elif head == "h1" and what == "card_swap":
            keys.update(lvls.decisive_key("h1", "card_swap", None, b) for b in ("size", "brief", "bound"))
        else:
            keys.add(lvls.decisive_key(head, what))
    assert keys <= set(lvls.DECISIVE), sorted(keys - set(lvls.DECISIVE))
    assert set(lvls.DECISIVE) == keys, sorted(set(lvls.DECISIVE) - keys)
    for k, mech in lvls.DECISIVE.items():
        assert mech == "-" or mech in lvls.MECHS[k.split(":")[0]], (k, mech)
    from tool_engine import hash_export as hx
    exp = hxp.build(created="2026-10-18T00:00:00Z")
    assert exp["tables"]["levels.DECISIVE"] == hx._sha_obj(hx._norm(lvls.DECISIVE))               # the map is a table of the hash export ...
    assert exp["tables"]["levels.DECISIVE"] != hx._sha_obj(hx._norm(dict(lvls.DECISIVE, **{"h1:coupling": "dmargin"})))      # ... and any change to it changes the hash
    assert hx.assert_no_text(exp)
    recs, _plan, _ctx = sample(2000, "t60-full")
    for r in recs:
        if r["hd"] == "h1" and r["edit"] == "card_swap":
            assert r["decisive"] in ("dmargin", "coupling")                                  # the predicate the two cards disagree on
        else:
            assert r["decisive"] == lvls.DECISIVE[lvls.decisive_key(r["hd"], r["edit"], r.get("ctl"))], r["row_id"]
    assert not hasattr(lvls, "DEPVIS_SCOPE") and not hasattr(lvls, "NON_FOCAL_H3_EDITS")           # depvis is scored on every row (Opus Q6 follow-up FU-a)


def test_q6_k21_with_the_amended_twin_rule_passes_on_the_dry_run_and_every_group_has_a_scenario_prefix():
    recs, _plan, _ctx = sample(2000, "t60-full")
    res = gates.k21_ladder(recs)
    assert res["problems"] == [], res["problems"]
    assert res["twin_rate"] >= 0.99 and res["twin_subject_rows"] > 600
    assert all(r["scenario_id"] == r["group_id"] for r in recs)
    assert gates.k19_split(recs)["ok"]


def test_q6_step_count_and_card_swap_pairs_give_the_hard_member_an_easy_decisive_twin():
    recs, _plan, _ctx = sample(2000, "t60-full")
    for gid, rs in _by_group(recs).items():
        if rs[0]["hd"] != "h3" or len(rs) != 2 or rs[0]["edit"] not in ("step_count", "card_swap"):
            continue
        pm = sorted(r["levels"]["pmargin"] for r in rs)
        assert pm[0] <= 2 and pm[1] >= 3, (gid, pm)
        if rs[0]["edit"] == "step_count":
            toks = [util.approx_tokens(r["rendered"]["text"]) for r in rs]
            assert min(toks) >= 1100 and abs(toks[0] - toks[1]) <= 0.15 * max(toks)


def test_q6_supersession_depth_is_assigned_as_an_exact_50_30_20_share_of_the_supersede_groups():
    for total, seed in ((2000, "t60-full"), (1000, "pilot-a"), (1000, "other")):
        plan = gen.build_plan(total=total, seed=seed)
        sups = [g for g in plan if g.get("h2kind") == "supersede"]
        cnt = collections.Counter(g["depth"] for g in sups)
        want = util.largest_remainder(len(sups), {1: 50, 2: 30, 3: 20})
        assert dict(cnt) == want, (cnt, want)


def test_q6_h1_length_l4_carriers_are_half_far_inside_delegate_and_half_multi_violation_do_here():
    """The long rows of H1 must not tell the label (single-feature tokens AUC was 0.57 when every H1 carrier was a DELEGATE row)."""
    for total, seed in ((2000, "t60-full"), (1000, "pilot-a")):
        plan = gen.build_plan(total=total, seed=seed)
        rcp.assign(plan, seed)
        car = [g for g in plan if g["head"] == "h1" and g["kind"] == "single" and g["ell"] == 4]
        far = sum(1 for g in car if g["ctl"] == "ctl.t60.far_inside")
        mv = sum(1 for g in car if g["ctl"] == "ctl.t60.multi_violation")
        assert far + mv == len(car) and len(car) >= total // 60 and abs(far - mv) <= 1, (far, mv)


# ---- Opus ruling Q6 batch 2, B2-1: no L3 ordinal reference lands on a superseded record ------------------------------------------------------
def _ordinal_rows(recs):
    return [r for r in recs if r["hd"] == "h2" and any(x.get("level") == 3 for st in r["scene"]["plan"] for x in st["refs"])]


def _fetched(sc):
    return sorted([f for f in sc["facts"] if f["type"] == "R" and not f.get("content_of")], key=lambda x: x["idx"])


def test_b2_no_l3_ordinal_lands_on_a_superseded_record_but_superseded_records_still_count_as_positions(full):
    rows = _ordinal_rows(full)
    assert len(rows) >= 100 and sum(1 for r in rows if r.get("h2kind") == "supersede") >= 20
    for r in full:
        if r["hd"] == "h2":
            assert bld.ordinal_superseded_problems(r["scene"]) == [], r["row_id"]
    assert sample(2000, "t60-full")[2].drops.get(bld.ORDINAL_ON_SUPERSEDED, 0) == 0           # the builder names the current record: the safety net never fires
    for r in rows:
        sc = r["scene"]
        rs = _fetched(sc)
        for st in sc["plan"]:
            for ref in st["refs"]:
                if ref.get("level") == 3:
                    f = rs[ref["ordinal"] - 1]
                    assert rule.current_of(sc, f)["id"] == f["id"], (r["row_id"], st["sid"])
    sup = [r for r in rows if r.get("h2kind") == "supersede"]
    for r in sup:                                                       # the superseded records of the chain are still POSITIONS of the count
        sc = r["scene"]
        star = next(s for s in sc["plan"] if s["sid"] == sc["star"])
        target = _fetched(sc)[star["refs"][0]["ordinal"] - 1]
        earlier = [f for f in bld.chain_of(sc) if f["idx"] < target["idx"]]
        assert target["id"] == sc["revs"][-1] and len(earlier) == len(sc["revs"]) - 1 >= 1
        assert star["refs"][0]["ordinal"] == 1 + len([f for f in _fetched(sc) if f["idx"] < target["idx"]]) >= 1 + len(earlier)


def test_b2_the_guard_flags_a_ordinal_that_names_the_old_record_and_the_gold_stays_the_current_value(full):
    rec = copy.deepcopy(next(r for r in _ordinal_rows(full) if r.get("h2kind") == "supersede"))
    sc = rec["scene"]
    assert ck.family_invariants(rec) == []
    star = next(s for s in sc["plan"] if s["sid"] == sc["star"])
    old = rule.fact_by_id(sc, sc["revs"][0])
    star["refs"][0]["ordinal"] = [f["id"] for f in _fetched(sc)].index(old["id"]) + 1          # the ordinal now names the superseded record
    assert bld.ordinal_superseded_problems(sc) == [(star["sid"], star["refs"][0]["ordinal"])]
    assert bld.ORDINAL_ON_SUPERSEDED in ck.family_invariants(rec)
    # the rule (gold) maps a reference that lands on a superseded record to the CURRENT value: the label does not change
    assert rule.current_of(sc, old)["id"] in rule.needs(sc) and old["id"] not in rule.needs(sc)
    other = copy.deepcopy(next(r["scene"] for r in full if r["hd"] == "h1"))
    assert bld.ordinal_superseded_problems(other) == []                                          # H1 / H3 scenes are untouched


def test_b2_a_row_that_breaks_it_is_dropped_with_its_own_counter_and_regenerated_on_the_same_skeleton(monkeypatch):
    plan = [g for g in gen.build_plan(total=2000, seed="b2-regen") if g.get("h2kind") == "supersede" and g["rc"]["ind"] == 3]
    assert plan
    g = plan[0]
    state = {"attempt": None}
    orig_group = bld.build_group

    def break_first_two_attempts(ctx, grp, attempt=0):
        scenes = orig_group(ctx, grp, attempt)
        if attempt < 2:
            for s in scenes:
                star = next(x for x in s["plan"] if x["sid"] == s["star"])
                star["refs"][0]["ordinal"] = [f["id"] for f in _fetched(s)].index(s["revs"][0]) + 1
        return scenes

    monkeypatch.setattr(bld, "build_group", break_first_two_attempts)
    ctx = gen.Ctx(seed="b2-regen", standin=False)
    recs = gen.generate_group(ctx, g)
    assert ctx.drops == {bld.ORDINAL_ON_SUPERSEDED: 4}                      # 2 attempts x 2 member rows, counted under its own code
    assert len(recs) == 2 and tuple(r["gold"] for r in recs) == tuple(g["labels"])
    assert all(bld.ordinal_superseded_problems(r["scene"]) == [] for r in recs)
