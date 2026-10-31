"""T55 RECOVER-ESCALATE unit tests: generator, SOLVER A (rule tables with the Opus C1-C3 orders), ledger simulation, renderer
and the PRE-FREEZE CPU gates. Everything is built in memory; no rows, no model calls, no files."""
import collections
import copy
import functools
import importlib.util
import itertools
import os

import pytest

import t55_dryrun
import t55_generator as gen
import t55_gates as gates
import t55_solver_a as sa
from tool_engine import invariants, names, perturb, state, util
from tool_engine.probe_stub import StubHarness

AL = names.AllowList.load()


@functools.lru_cache(maxsize=None)
def sample(total, seed="t55-test"):
    ctx = gen.Ctx(seed=seed, standin=True)
    return tuple(gen.generate_in_memory(total=total, seed=seed, ctx=ctx)), ctx


@pytest.fixture(scope="module")
def full():
    return list(sample(3000)[0])


# ---- plan --------------------------------------------------------------------------------------------------------
def test_sizes_and_label_mixes_equal_the_g0_lite_section_4(full):
    assert collections.Counter(r["sub_block"] for r in full) == collections.Counter(gen.SIZES)
    lab = {sb: collections.Counter(r["gold"] for r in full if r["sub_block"] == sb) for sb in gen.SIZES}
    assert lab["b1_classic"] == {"RETRY": 180, "FIX_ARGS": 180, "SWITCH_TOOL": 180, "ASK": 225, "STOP": 135}
    assert lab["b2_ambig_write"] == {"RETRY_KEYED": 150, "READ_BACK": 150, "ASK": 150, "NO_RETRY": 75, "RETRY_PLAIN": 75}
    assert lab["b3_implicit"] == {"ACCEPT": 160, "RETRY": 80, "FIX_ARGS": 90, "SWITCH_TOOL": 70, "ASK": 100}
    assert lab["b5_deny_escalate"] == {"CONTINUE_ALT": 120, "ESCALATE": 135, "STOP": 45}
    assert lab["b6_loop_poll"] == {"KEEP_POLLING": 120, "BREAK_LOOP_ALT": 75, "ESCALATE": 60, "STOP": 45}
    # B4: X = FIX_ARGS 80 / ASK 20; Y = SWITCH_TOOL 70 / ASK 30. The G0-lite's "Y STOP 10" cannot be produced by B1 rule 5
    # (invalid_unnamed -> SWITCH_TOOL or ASK): spec conflict reported to the orchestrator; STOP is folded into ASK.
    assert lab["b4_blind_retry"] == {"FIX_ARGS": 160, "SWITCH_TOOL": 140, "ASK": 100}


def test_pair_shares_meet_the_per_block_floors(full):
    assert gates.gc.pair_integrity(full)["ok"] and gates.gc.pair_share(full) >= 0.30
    by = collections.defaultdict(list)
    for r in full:
        by[r["sub_block"]].append(r)
    floors = {"b1_classic": 0.40, "b4_blind_retry": 1.0, "b2_ambig_write": 0.60, "b3_implicit": 0.50, "b5_deny_escalate": 0.50,
              "b6_loop_poll": 0.50}
    for sb, fl in floors.items():
        assert gates.gc.pair_share(by[sb]) >= fl - 1e-9, sb


def test_every_gold_is_reproduced_from_the_structured_record(full):
    assert all(sa.gold_label(r) == r["gold"] for r in full)
    for r in full:
        assert r["options"][ord(r["gold_letter"]) - 65]["label"] == r["gold"]


# ---- solver A: the C1 / C2 / C3 orders and the B1-B6 tables ---------------------------------------------------------
def test_truth_tables_rule_table_equals_evaluator_on_every_cell():
    for res in gates.p4_all():
        assert res["ok"], res
    assert gates.p4_b1_truth_table()["cells"] > 1000 and gates.p4_b2_truth_table()["cells"] == 32


def test_b1_cell_examples():
    S = gates.synth_b1
    assert sa.b1_label(S("transient_unavailable", 1, 3, "read", False, False, "ASK", "ASK")) == "RETRY"
    assert sa.b1_label(S("rate_limited", 3, 3, "idem", True, False, "ASK", "ASK")) == "SWITCH_TOOL"
    assert sa.b1_label(S("rate_limited", 3, 3, "key", False, False, "ASK", "ASK")) == "ASK"
    with pytest.raises(sa.OutOfBlock):                                     # B1 rule 3 belongs to B2
        sa.b1_label(S("transient_unavailable", 1, 3, "plain", False, False, "ASK", "ASK"))
    assert sa.b1_label(S("invalid_named_arg", 1, 2, "read", False, True, "ASK", "ASK")) == "FIX_ARGS"
    assert sa.b1_label(S("invalid_named_arg", 1, 2, "read", False, False, "ASK", "ASK")) == "ASK"
    assert sa.b1_label(S("unsupported_op", 1, 2, "read", False, False, "ASK", "STOP")) == "STOP"
    assert sa.b1_label(S("quota_exhausted", 1, 2, "read", False, False, "STOP", "ASK")) == "STOP"
    assert sa.b1_label(S("irrecoverable", 1, 2, "read", True, True, "ASK", "ASK")) == "STOP"


def test_c1_b3_order_arg_caused_beats_write_ask_beats_read_rules():
    rng = util.rng_for("c1")

    def row(vt, cause, rw, a, eq):
        base = invariants.make_base(vt, rng, "kol", "qty", cause)
        result, ctx = invariants.materialise(base, True)
        t0 = dict(tid="t0", rw=rw, idempotent=rw == "read", group="g", entity="e", verb="v", params=[])
        tools = [t0] + ([dict(t0, tid="te")] if eq else [])
        return dict(result=result, ctx=ctx, attempt=a, tools=tools, call=dict(tool_tid="t0", args=[]))
    assert sa.b3_label(row("id_not_in_prior_list", "arg", "write", 1, False)) == "FIX_ARGS"      # (2) before (3)
    assert sa.b3_label(row("negative_value", "data", "write", 1, True)) == "ASK"                  # (3)
    assert sa.b3_label(row("negative_value", "data", "read", 1, True)) == "RETRY"                 # (4)
    assert sa.b3_label(row("negative_value", "data", "read", 2, True)) == "SWITCH_TOOL"           # (5)
    assert sa.b3_label(row("negative_value", "data", "read", 2, False)) == "ASK"
    r = row("negative_value", "data", "read", 1, False)
    r["result"], r["ctx"] = invariants.materialise(invariants.make_base("negative_value", rng, "kol", "qty"), False)
    assert sa.b3_label(r) == "ACCEPT"                                                              # (1)


def test_b3_refuses_mixed_violations():
    rng = util.rng_for("mix")
    base = invariants.make_base("negative_value", rng, "kol", "qty")
    result, ctx = invariants.materialise(base, True)
    base2 = invariants.make_base("parts_total_mismatch", rng, "kol", "qty")
    r2, c2 = invariants.materialise(base2, True)
    result["items"], result["total"] = r2["items"], r2["total"]
    with pytest.raises(sa.SpecError):
        sa.b3_label(dict(result=result, ctx=ctx, attempt=1, tools=[], call=dict(tool_tid="t0")))


def test_c2_b6_order():
    def rec(adv_pattern, cu, pc=8, L=3, alt=False, nw=False):
        prog = [10]
        for x in adv_pattern:
            prog.append(prog[-1] + (4 if x else 0))
        return dict(poll=dict(obs=[{"progress": v} for v in prog], calls_used=cu, alt_exists=alt),
                    card_b6=dict(P_cap=pc, L=L, transitions=[], non_waitable=nw))
    assert sa.b6_label(rec([False, True], 3)) == "KEEP_POLLING"                      # (1) changed, under the budget
    assert sa.b6_label(rec([False, True], 8)) == "ESCALATE"                          # (2) changed, budget used up
    assert sa.b6_label(rec([True, False, False], 3)) == "KEEP_POLLING"               # (3) stale < L
    assert sa.b6_label(rec([True, False, False, False], 3, alt=True)) == "BREAK_LOOP_ALT"          # (4)
    assert sa.b6_label(rec([True, False, False, False], 3, alt=True, nw=True)) == "BREAK_LOOP_ALT"    # alt beats non-waitable
    assert sa.b6_label(rec([True, False, False, False], 3, nw=True)) == "STOP"       # (5)
    assert sa.b6_label(rec([True, False, False, False], 3)) == "ESCALATE"            # (6)


def test_b6_state_change_predicate_uses_declared_transitions_and_counters():
    r = dict(poll=dict(obs=[{"status": "queued", "counter": 1}, {"status": "running", "counter": 1}, {"status": "running", "counter": 2}],
                       calls_used=3, alt_exists=False), card_b6=dict(P_cap=8, L=3, transitions=[["queued", "running"]], non_waitable=False))
    assert sa.b6_changes(r) == [True, True]
    r["poll"]["obs"][1] = {"status": "done", "counter": 1}                       # an UNDECLARED transition is not an advance
    assert sa.b6_changes(r)[0] is False


def test_b5_thresholds():
    rec = lambda n_c, n_t, n_w, alt, hard, K=(3, 20, None, False): dict(                # noqa: E731
        denials=dict(n_c=n_c, n_t=n_t, n_w=n_w, alt_exists=alt, goal_blocked_hard=hard),
        card_b5=dict(K_c=K[0], K_t=K[1], K_w=K[2], W=50 if K[3] else None, window=K[3]))
    assert sa.b5_label(rec(2, 5, None, True, False)) == "CONTINUE_ALT" and sa.b5_label(rec(3, 5, None, True, False)) == "ESCALATE"
    assert sa.b5_label(rec(1, 20, None, True, False)) == "ESCALATE" and sa.b5_label(rec(1, 5, None, False, False)) == "ESCALATE"
    assert sa.b5_label(rec(1, 5, None, True, True)) == "STOP" and sa.b5_label(rec(3, 5, None, True, True)) == "ESCALATE"
    assert sa.b5_label(rec(1, 12, 10, True, False, (3, None, 10, True))) == "ESCALATE"


# ---- ledger ------------------------------------------------------------------------------------------------------
def test_b2_rule_table_equals_the_five_option_two_world_simulation_in_every_row(full):
    for r in [x for x in full if x["sub_block"] == "b2_ambig_write"]:
        f = sa.b2_facts(r)
        assert sa.b2_rule(**{"idem": f["idem"], "kf": f["kf"], "rp": f["rp"], "committed": f["committed"], "step": f["step"]}) \
            == state.ambiguous_write_simulated_gold(f["idem"], f["kf"], f["rp"], bool(f["committed"]), f["step"]) == r["gold"]


def test_b2_step_two_requires_a_conclusive_read_back(full):
    for r in [x for x in full if x["sub_block"] == "b2_ambig_write" and x["step"] == 2]:
        assert "committed: %s" % ("yes" if r["readback"]["committed"] else "no") in r["rendered"]["text"]
        assert any(t["tid"] == "tr" for t in r["tools"])


# ---- held-out violation types, cells, channels, B4, B5 ----------------------------------------------------------------
def test_heldout_types_never_appear_in_training_rows(full):
    seen = {r["b3"]["vtype"] for r in full if r["sub_block"] == "b3_implicit"}
    assert not (seen & set(perturb.HELDOUT_TYPES)) and seen == set(perturb.TRAIN_TYPES)


def test_cells_and_type_coverage(full):
    r = gates.p3_perturbation_coverage(full)
    assert r["ok"], r
    assert min(r["cells"].values()) >= 0.08


def test_b4_pairs_differ_only_in_the_detail_field(full):
    assert gates.p8_b4_pairs(full)["ok"]
    by = collections.defaultdict(dict)
    for r in full:
        if r["sub_block"] == "b4_blind_retry":
            by[r["group_id"]][r["pair_role"]] = r
    for d in list(by.values())[:100]:
        ea, eb = d["a"]["error"], d["b"]["error"]
        assert ea["class"] == "invalid_named_arg" and eb["class"] == "invalid_unnamed" and ea["code"] == eb["code"]
        ta, tb = d["a"]["rendered"]["text"], d["b"]["rendered"]["text"]
        outs_a, outs_b = d["a"]["parts"]["outputs"], d["b"]["parts"]["outputs"]
        assert len(outs_a) == len(outs_b) == 1
        la, lb = outs_a[0].splitlines(), outs_b[0].splitlines()
        assert [x for x in la if x not in lb] == ["field: %s" % ea["field"]] and [x for x in lb if x not in la] == []
        assert "field: %s" % ea["field"] in ta and "field:" not in tb


def test_channel_mixing_and_b5_threshold_diversity(full):
    assert gates.p9_channels(full)["ok"] and gates.p19_b5_thresholds(full)["ok"]
    kinds = {tuple(r["error"]["channels"]) for r in full if r["sub_block"] in ("b1_classic", "b4_blind_retry")}
    assert len(kinds) == 7


def _is_oddity(r):
    vt, res, ctx = r["b3"]["vtype"], r["result"], r["ctx"]
    if vt == "empty_when_count_stated":
        return res["items"] == [] and ctx["stated_count"] == 0
    if vt == "negative_value":
        return all(v == 0 for v in res["fields"].values())
    if vt == "parts_total_mismatch":
        return len(set(res["items"])) == 1 and res["total"] == sum(res["items"])
    if vt == "id_not_in_prior_list":
        return len(res["items"]) >= 2
    if vt == "scale_mismatch":
        return res["fields"][ctx["reference"]["field"]] != ctx["reference"]["value"]
    if vt == "stale_echo":
        return list(res["echo"]) != list(ctx["intended_args"])
    return False


def test_b3_valid_results_are_legitimate_surface_oddities(full):
    b3 = [r for r in full if r["sub_block"] == "b3_implicit"]
    valid = [r for r in b3 if r["gold"] == "ACCEPT"]
    assert all(_is_oddity(r) for r in valid)
    assert len(valid) / len(b3) >= 0.30                                         # G0-lite: >= 30% of B3 rows


def test_implicit_violations_are_never_named_by_the_card(full):
    for r in full:
        if r["sub_block"] == "b3_implicit":
            low = r["parts"]["card"].lower()
            assert not any(t.replace("_", " ") in low for t in perturb.VIOLATION_TYPES)
            assert "violat" not in low and "invariant" not in low


# ---- rendering, names, determinism, safety -----------------------------------------------------------------------------
def test_rendered_outputs_pass_the_lint_and_every_fact_is_visible(full):
    assert gates.p14_output_lint(full)["ok"]
    assert gates.p10_observability(full)["ok"]


def test_names_on_the_allow_list_and_accepted_by_the_row_start_guard(full):
    assert gates.gc.name_guard_gate("P-15", full, AL, "T55")["ok"]
    spec = importlib.util.spec_from_file_location("od_row_start_guard", os.path.join(names.INFRA_DIR, "row_start_guard.py"))
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)
    allow = {c: set(AL.union[c]) for c in names.CATEGORIES}
    assert guard.check_names(names.job_manifest("T55", full)["names"], allow, "job") == []


def test_generation_is_deterministic_and_production_is_refused_and_nothing_is_written(tmp_path, monkeypatch):
    sha = lambda rs: util.sha256_text(util.canon_json([(r["row_id"], r["gold"], r["rendered"]["text"]) for r in rs]))     # noqa: E731
    assert sha(gen.generate_in_memory(total=150, seed="d")) == sha(gen.generate_in_memory(total=150, seed="d"))
    with pytest.raises(names.NamespaceError):
        gen.generate_in_memory(total=20, seed="p", standin=False)
    monkeypatch.chdir(tmp_path)
    recs, summary = t55_dryrun.run(20)
    assert summary["written_to_disk"] is False and list(tmp_path.iterdir()) == []
    with pytest.raises(ValueError):
        t55_dryrun.run(t55_dryrun.MAX_DRY + 1)


def test_all_non_probe_gates_pass_except_the_seed_wording_pool(full):
    failing = [r["id"] for r in gates.run_all(full, allowlist=AL) if not r["ok"]]
    assert set(failing) <= {"P-13:wording"}, failing


def test_probe_wiring_and_power(full):
    h = StubHarness(repeats=3)
    res = gates.p5_structure(full, h)
    assert len(res) == 6 and all(r["bacc"] < 0.45 for r in res)
    leaked = copy.deepcopy(full)
    for r in leaked:
        if r["sub_block"] == "b3_implicit":
            r["parts"]["outputs"] = [o + ("\nitems: zzz" if r["gold"] != "ACCEPT" else "") for o in r["parts"]["outputs"]]
    assert not gates.p6_b3_shape(leaked, h)["ok"]


def test_seed_wording_pool_fails_the_wording_gate_as_it_should(full):
    assert gates.gc.wording_gate("w", full)["ok"] is False


def test_solver_b_hook(full):
    assert gates.gc.agreement_gate("P-1", full, lambda r: r["gold"])["ok"]
    assert not gates.gc.agreement_gate("P-1", full, lambda r: "X" if r["row_id"].endswith("-s") else r["gold"])["ok"]


def test_g10_decision_spans_cover_every_user_stated_value(full):
    from tool_engine import render
    for r in full[:800]:
        ds = r["decision_spans"]
        text = r["parts"]["request"]
        for sp in ds["spans"]:
            assert text[sp["start"]:sp["end"]] == sp["text"] and sp["role"] in render.ROLES_G10
        for _k, v in r.get("user_values", []):
            assert any(sp["role"] == "authority" and sp["text"] == v for sp in ds["spans"])
