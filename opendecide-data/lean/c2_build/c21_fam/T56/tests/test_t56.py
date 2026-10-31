"""T56 DONE-CLAIM (done-claim half) unit tests: environment, SOLVER A (hidden truth), renderer, pairs and the PRE-FREEZE CPU
gates. Everything is built in memory; no rows, no model, no execution of generated code, no files."""
import collections
import copy
import functools
import importlib.util
import os
import random
import re

import pytest

import t56_dryrun
import t56_env as E
import t56_generator as gen
import t56_gates as gates
import t56_render as rd
import t56_solver_a as sa
import t56_wording as tw
from tool_engine import names, perturb, render, util
from tool_engine.probe_stub import StubHarness

AL = names.AllowList.load()


@functools.lru_cache(maxsize=None)
def sample(total, seed="t56-test"):
    ctx = gen.Ctx(seed=seed, standin=True)
    return tuple(gen.generate_in_memory(total=total, seed=seed, ctx=ctx)), ctx


@pytest.fixture(scope="module")
def full():
    return list(sample(2000)[0])


# ---- plan / sizes ------------------------------------------------------------------------------------------------------
def test_sizes_labels_reasons_equal_the_g0_lite_section_4(full):
    assert len(full) == 2000 and collections.Counter(r["sub_block"] for r in full) == collections.Counter(gen.SIZES)
    for sb in gen.SUB_BLOCKS:
        rs = [r for r in full if r["sub_block"] == sb]
        pos = sum(r["gold"] in ("DONE", "READY") for r in rs)
        assert pos == len(rs) - pos
    d1 = collections.Counter(r["gold_reason"] for r in full if r["sub_block"] == "d1_evidence" and r["gold"] == "CONTINUE")
    assert d1 == {"unmet_criterion": 120, "short_coverage": 165, "stale_evidence": 90, "wrong_target": 75}
    d4 = collections.Counter(r["gold_reason"] for r in full if r["sub_block"] == "d4_ready" and r["gold"] == "NOT_READY")
    assert d4 == {"stray_change": 75, "stale_evidence": 35, "unmet_criterion": 40}
    d2 = collections.Counter(r["fault"] for r in full if r["sub_block"] == "d2_ledger" and r["gold"] == "CONTINUE")
    assert d2 == {"f_ledger_dup": 90, "f_ledger_missing": 85}
    d3 = collections.Counter(r["hidden"]["final"]["graph"] and r["entry"] for r in full if r["sub_block"] == "d3_demo_only" and r["gold"] == "CONTINUE")
    assert sorted(d3.values()) == [31, 31, 31, 32]
    assert sum(1 for r in full if r["sub_block"] == "d5_unverified" and r["gold_reason"] == "unverified") == 100


def test_pair_share_languages_and_stages(full):
    assert gates.gc.pair_share(full) >= 0.80 and gates.gc.pair_integrity(full)["ok"]
    assert gates.p10_stages(full)["ok"]
    langs = collections.Counter(r["lang"] for r in full)
    assert 0.35 <= langs["python"] / len(full) <= 0.45 and all(langs[l] / len(full) > 0.15 for l in ("javascript", "go", "bash"))


def test_every_gold_and_reason_is_reproduced_from_the_hidden_state(full):
    for r in full:
        assert sa.gold(r) == (r["gold"], r["gold_reason"])
        assert (r["gold_reason"] == "none") == (r["gold"] in ("DONE", "READY"))
        assert perturb.FAULT_REASON[r["fault"]] == r["gold_reason"] or r["fault"] == "f_none"
        assert r["options"][ord(r["gold_letter"]) - 65]["label"] == r["gold"]


def test_hard_bin_and_fault_coverage(full):
    assert gates.p12_fault_coverage(full)["ok"]
    neg = [r for r in full if r["gold"] in ("CONTINUE", "NOT_READY")]
    assert sum(r["bin"] == "hard" for r in neg) / len(neg) >= 0.40


# ---- the matched-pair design ---------------------------------------------------------------------------------------------
def test_claim_task_and_call_skeleton_are_byte_identical_in_every_pair_and_only_outputs_differ(full):
    assert gates.p3_pair_identity(full)["ok"]
    by = collections.defaultdict(dict)
    for r in full:
        if r["pair_role"]:
            by[r["group_id"]][r["pair_role"]] = r
    differs = 0
    for d in by.values():
        a, b = d["a"], d["b"]
        assert a["claim"] == b["claim"] and a["task_text"] == b["task_text"]
        if a["sub_block"] != "d5_unverified":
            assert a["skeleton"] == b["skeleton"]
            differs += a["parts"]["outputs"] != b["parts"]["outputs"]
        else:                                                              # the declared exception: one verification call
            assert len(a["skeleton"]) > len(b["skeleton"])
    assert differs > 0.9 * sum(1 for d in by.values() if d["a"]["sub_block"] != "d5_unverified")


def test_every_claim_wording_is_used_with_both_labels_at_equal_rates(full):
    assert gates.p9_claims(full)["ok"]
    by = collections.defaultdict(list)
    for r in full:
        by[r["claim_wording"]].append(r["gold"] in ("DONE", "READY"))
    shares = [sum(v) / len(v) for v in by.values() if len(v) >= 20]
    assert shares and all(0.4 <= s <= 0.6 for s in shares)


# ---- solver A: precedence, single faults, evidence quality -------------------------------------------------------------------
def _first(full, fault, sb=None):
    return next(r for r in full if r["fault"] == fault and (sb is None or r["sub_block"] == sb))


def test_a_done_row_has_no_failing_condition(full):
    for r in [x for x in full if x["fault"] == "f_none"][:200]:
        assert sa.failing_conditions(r["hidden"]) == set()


@pytest.mark.parametrize("fault", sorted(set(perturb.FAULT_REASON) - {"f_none"} - {"f_demo_only"}))
def test_each_fault_yields_exactly_its_reason(full, fault):
    rows = [r for r in full if r["fault"] == fault]
    assert rows
    for r in rows[:25]:
        assert sa.failing_conditions(r["hidden"]) == {perturb.FAULT_REASON[fault]}


def test_demo_only_variants_each_yield_dead_or_demo_only_and_bfs_equals_dfs(full):
    assert gates.p20_reachability(full)["ok"]
    variants = set()
    for r in [x for x in full if x["fault"] == "f_demo_only"]:
        assert sa.failing_conditions(r["hidden"]) == {"dead_or_demo_only"}
        variants.add(r["entry"])
    assert len(variants) == 4


def test_mixed_faults_are_refused_and_precedence_orders_the_reasons(full):
    r = copy.deepcopy(_first(full, "f_unmet", "d1_evidence"))
    ch = next(c for c in r["hidden"]["checks"] if c["full"])
    ch["snapshot_rev"] = 0                                                  # now ALSO stale
    reasons = sa.failing_conditions(r["hidden"])
    assert {"unmet_criterion", "stale_evidence"} <= reasons
    with pytest.raises(sa.SpecError):
        sa.gold(r)
    assert sa.precedence_first(r, reasons) == "unmet_criterion"
    assert sa.precedence_first(r, {"short_coverage", "wrong_target", "ledger_mismatch"}) == "wrong_target"
    assert sa.precedence_first(r, {"dead_or_demo_only", "unverified", "stale_evidence"}) == "unverified"
    d4 = _first(full, "f_stray", "d4_ready")
    assert sa.precedence_first(d4, {"short_coverage", "stray_change", "stale_evidence"}) == "stale_evidence"
    assert sa.precedence_first(d4, {"short_coverage", "stray_change"}) == "stray_change"      # D4: stray before short coverage
    assert sa.precedence_first(r, {"short_coverage", "ledger_mismatch"}) == "short_coverage"


def test_unverified_means_no_verification_call_at_all(full):
    r = _first(full, "f_no_check")
    assert not (r["hidden"]["checks"] or r["hidden"]["ledger_reads"] or r["hidden"]["graph_reads"])
    r2 = copy.deepcopy(_first(full, "f_none", "d1_evidence"))
    r2["hidden"]["checks"] = [c for c in r2["hidden"]["checks"] if c["target"] != r2["hidden"]["deliverables"]["store"]]
    assert "short_coverage" in sa.failing_conditions(r2["hidden"])          # evidence for some criteria missing != unverified
    r2["hidden"]["checks"], r2["hidden"]["ledger_reads"], r2["hidden"]["graph_reads"] = [], [], []
    assert sa.failing_conditions(r2["hidden"]) == {"unverified"}


def test_stale_evidence_is_the_relation_between_two_stamps(full):
    r = _first(full, "f_stale_run", "d1_evidence")
    t = r["rendered"]["text"]
    snap = int(re.search(r"snapshot_rev: (\d+)", t).group(1))
    revs = [int(x) for x in re.findall(r"rev: (\d+)", t)]
    assert snap < max(c["rev"] for c in r["calls"] if c["kind"] == "mutate")
    d = _first(full, "f_none", "d1_evidence")
    assert int(re.search(r"snapshot_rev: (\d+)", d["rendered"]["text"]).group(1)) > max(
        c["rev"] for c in d["calls"] if c["kind"] == "mutate")


def test_count_short_and_wrong_target_are_visible_only_as_relations(full):
    r = _first(full, "f_count_short", "d1_evidence")
    n_items = len(re.findall(r"item\[\d+\]", r["rendered"]["text"]))
    declared = len(next(c for c in r["hidden"]["checks"] if c["full"])["declared"])
    assert n_items == declared - 1
    w = _first(full, "f_wrong_target", "d1_evidence")
    assert re.search(r"target: (\S+)", w["rendered"]["text"]).group(1) != w["hidden"]["deliverables"]["store"]


def test_ledger_faults_change_the_entry_count_not_a_keyword(full):
    d = _first(full, "f_ledger_dup", "d1_evidence") if False else _first(full, "f_ledger_dup")
    m = _first(full, "f_ledger_missing")
    for r, delta in ((d, +1), (m, -1)):
        entries = int(re.search(r"entries: (\d+)", r["rendered"]["text"]).group(1))
        sent = len([c for c in r["calls"] if c["tool"].startswith("send_")])
        extras = len([e for e in r["hidden"]["final"]["ledger"] if e["rev"] == 0])
        assert entries == sent + extras + delta


def test_evidence_sufficiency_structure(full):
    assert gates.p11_sufficiency(full)["ok"]
    r = copy.deepcopy(_first(full, "f_none", "d1_evidence"))
    for c in r["hidden"]["checks"]:
        c["declared"] = c["declared"][:-1]
    assert sa.evidence_sufficiency(r)


# ---- environment -----------------------------------------------------------------------------------------------------------
def test_graph_variants_and_independent_searches_agree_on_random_graphs():
    rng = random.Random(4)
    for v in (None, "import_not_wired", "flag_default_off", "unreachable_branch", "helper_never_called"):
        for _ in range(40):
            g = E.build_graph(rng, "mm", "ff", "ss", ["u1", "u2"][: rng.randint(1, 2)], v)
            assert E.reachable(g, g["target"]) == E.reachable_dfs(g, g["target"]) == (v is None)
            for sym in g["module_of"]:
                assert E.reachable(g, sym) == E.reachable_dfs(g, sym)


def test_env_revision_clock_and_dropped_effects():
    env = E.Env(["a", "b"], "x0", "f")
    r1 = env.set_status("a", "closed")
    r2 = env.set_status("b", "closed", drop=True)
    assert (r1, r2) == (1, 2) and env.store["a"]["status"] == "closed" and env.store["b"]["status"] == "open"
    assert env.last_mut == {"a": 1, "b": 2}
    env.send("u", "k", "dup")
    env.send("v", "k", "drop")
    assert [e["recipient"] for e in env.ledger] == ["u", "u"]
    assert env.eval_pred(dict(pred="status_is", item="a", value="closed")) and not env.eval_pred(dict(pred="status_is", item="b", value="closed"))
    assert not env.eval_pred(dict(pred="exactly_once", item="u")) and not env.eval_pred(dict(pred="exactly_once", item="v"))
    assert env.eval_pred(dict(pred="unchanged", item="a")) is False and set(E.PREDICATES) == {
        "exists", "absent", "equals", "count_eq", "exactly_once", "status_is", "unchanged", "reachable"}


# ---- reason head rows (G7) ---------------------------------------------------------------------------------------------------
def test_head_rows_are_extra_copies_from_at_most_a_quarter_of_the_specs(full):
    ctx = sample(2000)[1]
    heads = gen.head_rows(ctx, full)
    assert heads and gates.head_share(full, heads)["ok"]
    for h in heads[:50]:
        assert len(h["options"]) == 9 and h["gold"] == h["gold_reason"]
        assert h["rendered"]["context"] == next(r for r in full if r["row_id"] == h["row_id"][:-5])["rendered"]["context"]
        assert "none" in [o["label"] for o in h["options"]]


# ---- text / names / safety ------------------------------------------------------------------------------------------------------
def test_task_and_claim_text_do_not_name_the_fault_family(full):
    for r in full:
        low = (r["task_text"] + " " + r["claim"]).lower()
        for w in ("ledger", "stray", "stale", "unverified", "demo", "dead code", "wrong target"):
            assert re.search(r"\b%s\b" % re.escape(w), low) is None


def test_outputs_pass_the_lint_and_names_are_on_the_allow_list(full):
    assert gates.p13_output_lint(full)["ok"]
    assert gates.gc.name_guard_gate("P-16", full, AL, "T56")["ok"]
    assert all(not any(i.startswith("param.") for i in r["names"]["tool"]) for r in full)          # T56 lists no param roles
    spec = importlib.util.spec_from_file_location("od_row_start_guard", os.path.join(names.INFRA_DIR, "row_start_guard.py"))
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)
    allow = {c: set(AL.union[c]) for c in names.CATEGORIES}
    assert guard.check_names(names.job_manifest("T56", full)["names"], allow, "job") == []


def test_token_budget_and_letter_share(full):
    assert gates.gc.token_gate("t", full)["ok"]
    assert all(r["ok"] for r in gates.p19_letters(full))


def test_generation_is_deterministic_production_refused_nothing_written(tmp_path, monkeypatch):
    sha = lambda rs: util.sha256_text(util.canon_json([(r["row_id"], r["gold"], r["rendered"]["text"]) for r in rs]))     # noqa: E731
    assert sha(gen.generate_in_memory(total=120, seed="d")) == sha(gen.generate_in_memory(total=120, seed="d"))
    with pytest.raises(names.NamespaceError):
        gen.generate_in_memory(total=20, seed="p", standin=False)
    monkeypatch.chdir(tmp_path)
    recs, summary = t56_dryrun.run(20)
    assert summary["written_to_disk"] is False and list(tmp_path.iterdir()) == []
    with pytest.raises(ValueError):
        t56_dryrun.run(t56_dryrun.MAX_DRY + 1)


def test_no_generated_code_is_executed_and_no_file_reads():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for fn in os.listdir(here):
        if fn.endswith(".py") and fn.startswith("t56_"):
            src = open(os.path.join(here, fn)).read()
            for bad in ("exec(", "eval(", "subprocess", "os.system", "open(", "compile("):
                assert bad not in src, (fn, bad)


# ---- gates -------------------------------------------------------------------------------------------------------------------------
def test_non_probe_gates_pass_except_the_seed_wording_pool(full):
    failing = [r["id"] for r in gates.run_all(full, allowlist=AL) if not r["ok"]]
    assert set(failing) <= {"P-9:wording"}, failing


def test_probe_gates_on_a_clean_sample(full):
    h = StubHarness(repeats=3)
    assert gates.p5_task_only(full, h)["auc"] < 0.60 and gates.p7_reason_head(full, h)["bacc"] < 0.25
    assert gates.p6_structure(full, h)["auc"] < 0.60
    assert gates.p8_hard_bin_outputs(full, h)["ok"]
    for r in gates.p4_claim_only(full, h):
        assert r["auc"] < 0.60


def test_probe_power_planted_claim_leak_and_reason_leak_are_caught(full):
    leaked = copy.deepcopy(full)
    for r in leaked:
        r["claim"] += " zzq" if r["gold"] in ("DONE", "READY") else " ppk"
    assert not gates.p4_claim_only(leaked, StubHarness(repeats=3))[0]["ok"]
    leaked = copy.deepcopy(full)
    for r in leaked:
        r["task_text"] += " tag%s" % r["gold_reason"]
    assert not gates.p7_reason_head(leaked, StubHarness(repeats=3))["ok"]


def test_solver_b_agreement_hook(full):
    assert gates.gc.agreement_gate("P-1", full, lambda r: r["gold"])["ok"]
    res = gates.gc.agreement_gate("P-1", full, lambda r: "CONTINUE" if r["row_id"].endswith("-s") else r["gold"])
    assert not res["ok"] and res["dropped_ids"]


def test_seed_wording_pool_is_flagged_by_the_wording_gate(full):
    assert gates.gc.wording_gate("w", full)["ok"] is False


def test_g10_scope_declaration_is_an_authority_span(full):
    for r in full[:500]:
        ds = r["decision_spans"]
        assert any(sp["role"] == "authority" and sp["text"] == r["hidden"]["scope"] for sp in ds["spans"])
        for sp in ds["spans"]:
            assert r["task_text"][sp["start"]:sp["end"]] == sp["text"] and sp["role"] in render.ROLES_G10
