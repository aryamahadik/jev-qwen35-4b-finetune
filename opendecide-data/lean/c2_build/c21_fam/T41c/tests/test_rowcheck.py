"""Check-at-generation: every row is verified (schema/anchors, A vs B, invariants, guards, G13 hook, stamp) WHEN it is built."""
import json
from dataclasses import replace

import pytest

from t41c import build, export, planner, pools, rowcheck
from t41c.render import build_row, export_for_b
from t41c.spec import label_of


@pytest.fixture(scope="module")
def solve_b():
    return rowcheck.load_solver_b()


@pytest.fixture(scope="module")
def specs():
    s, _ = planner.plan_specs(400)
    return s


@pytest.fixture()
def checker(solve_b, pool, heldout):
    return rowcheck.RowChecker(solve_b, rowcheck.TestOnlyG13(), heldout=heldout, pool=pool)


def _first(specs, pred):
    return next(s for s in specs if pred(s))


def test_solver_b_is_required_and_production_needs_a_real_g13(solve_b, pool):
    with pytest.raises(rowcheck.RowCheckError):
        rowcheck.RowChecker(None)
    with pytest.raises(rowcheck.G13HookMissing):
        rowcheck.RowChecker(solve_b, None, production=True, pool=pool)
    with pytest.raises(rowcheck.G13HookMissing):
        rowcheck.RowChecker(solve_b, rowcheck.TestOnlyG13(), production=True, pool=pool)
    with pytest.raises(rowcheck.G13HookMissing):
        rowcheck.RowChecker(solve_b, rowcheck.MissingG13(), production=True, pool=pool)
    with pytest.raises(rowcheck.RowCheckError):                # a test-fixture pool is never a production pool
        rowcheck.RowChecker(solve_b, rowcheck.G13Hook(), production=True, pool=pool)
    with pytest.raises(rowcheck.G13HookMissing):
        rowcheck.MissingG13().stamp([{"row_id": "x", "text": "t"}])


def test_production_needs_the_row_start_guard_env(solve_b):
    class Real(rowcheck.G13Hook):
        kind = "stamp_service"

        def stamp(self, items):
            return [rowcheck.G13Result(True, False, (), "r" * 64, "m1") for _ in items]
    prod = pools.Pool({"kind": pools.KIND_PROD, "version": "x", "cells": {"x": [{"id": "1", "text": "t"}]}})
    with pytest.raises(rowcheck.RowCheckError):
        rowcheck.RowChecker(solve_b, Real(), production=True, pool=prod, guard_env={})
    env = {"OD_ROWGUARD_FREEZE_SHA": "a" * 64, "OD_ROWGUARD_REGISTRY_SHA": "b" * 64, "OD_ROWGUARD_ALLOWLIST_SHA": "c" * 64}
    chk = rowcheck.RowChecker(solve_b, Real(), production=True, pool=prod, guard_env=env)
    assert chk.registry_sha == "b" * 64


def test_a_clean_row_is_accepted_and_stamped(specs, pool, checker):
    s = specs[0]
    r = build_row(s, pool)
    v = checker.check_rendered(s, r)
    assert v.accepted and v.a_label == v.b_label == label_of(s)
    out = checker.stamp_batch([(s, r, v)])
    assert out[0].stamp["verdict"] == "clean" and out[0].stamp["row_id"] == s.row_id
    assert set(out[0].stamp) == {"row_id", "registry_sha", "method_set", "code_sha", "template_hash", "verdict", "g13_hook"}


def test_ab_disagreement_drops_the_row_and_logs_labels_not_text(specs, pool, solve_b, heldout):
    def liar(ex):
        out = dict(solve_b(ex))
        out["label"] = "ALLOW" if out["label"] != "ALLOW" else "BLOCK"
        return out
    chk = rowcheck.RowChecker(liar, rowcheck.TestOnlyG13(), heldout=heldout, pool=pool)
    s = specs[3]
    r = build_row(s, pool)
    v = chk.check_rendered(s, r)
    assert not v.accepted and v.stage == "answer_ab" and v.code == "AB_DISAGREE"
    blob = json.dumps(chk.log[0].__dict__, default=str)
    assert all(t not in blob for t in r.slot_texts)
    assert chk.first_pass_rates()["answer_ab"]["over"]                      # 100% disagreement is far over the 2% line


def test_b_crash_and_b_anomaly_are_drops(specs, pool, heldout, solve_b):
    def boom(ex):
        raise ValueError("x")
    s = specs[0]
    r = build_row(s, pool)
    v = rowcheck.RowChecker(boom, heldout=heldout).check_rendered(s, r)
    assert (v.stage, v.code) == ("answer_ab", "B_ERROR")
    absent = _first(specs, lambda x: not x.facts.present)
    ra = build_row(absent, pool)
    v = rowcheck.RowChecker(lambda ex: dict(solve_b(ex), anomalies=["index_without_package"]), heldout=heldout).check_rendered(absent, ra)
    assert v.code == "FACTS_ABSENT_UNDECIDABLE"


def test_heldout_values_are_refused_outside_the_ho_block(specs, pool, checker, heldout):
    s = _first(specs, lambda x: x.directives)
    d = s.directives[0]
    bad = replace(s, directives=(replace(d, wrapper=heldout["wrappers"][0], hidden=None),) + s.directives[1:])
    v = checker.check_rendered(bad, build_row(bad, pool))
    assert not v.accepted and v.code.startswith("HELDOUT_VALUE_IN_TRAIN")


def test_ho_rows_carry_exactly_one_heldout_value(pool, solve_b, heldout):
    ho, _ = planner.plan_heldout(per_value=10, heldout=heldout)
    chk = rowcheck.RowChecker(solve_b, rowcheck.TestOnlyG13(), heldout=heldout, pool=pool)
    acc, rep = build.build_rows_checked(ho, pool, chk)
    assert len(acc) > 0.9 * len(ho) and not rep["combined_fix_triggered"]


def test_skeleton_must_be_neutral(specs, pool, checker):
    s = _first(specs, lambda x: x.directives)
    r = build_row(s, pool)
    assert rowcheck.skeleton_problems(r) == []
    r.spans[0].text += "\nthe credential store holds a secret token"
    assert any("ATTACK_VOCAB" in p for p in rowcheck.skeleton_problems(r))
    v = checker.check_rendered(s, r)
    assert not v.accepted and v.code == "SKELETON_NOT_NEUTRAL"


def test_pii_scrub_codes():
    ok = "mail ops@build.example from 192.0.2.7 and 10.3.4.5, see https://a-1.liri.invalid/x, version 1.2.3.4.5"
    assert rowcheck.pii_problems(ok) == []
    assert "PII_EMAIL" in rowcheck.pii_problems("write to jo@real-corp.com")
    assert "PII_REAL_IP" in rowcheck.pii_problems("host 8.8.4.4 listens")
    assert "REAL_DOMAIN" in rowcheck.pii_problems("fetch https://files.somewhere.io/a")
    assert "PII_SSN" in rowcheck.pii_problems("id 123-45-6789")
    assert "PII_CARD" in rowcheck.pii_problems("card 4111 1111 1111 1111")
    assert "PII_CARD" not in rowcheck.pii_problems("number 1234 5678 9012 3456")      # fails Luhn


def test_token_cap_g6_drops_a_long_row(specs, pool, solve_b, heldout):
    chk = rowcheck.RowChecker(solve_b, heldout=heldout, token_fn=lambda t: 1537)
    s = specs[0]
    v = chk.check_rendered(s, build_row(s, pool))
    assert v.code == "TOKEN_CAP_G6"


def test_g13_hit_retires_the_whole_group_and_is_never_reworded(specs, pool, solve_b, heldout):
    plain, _ = build.build_rows(specs, pool)
    built = {s.group_id for s, _ in plain}
    grp = next(s.group_id for s in specs if s.pair_kind != "single" and s.group_id in built)
    victim = _first(specs, lambda x: x.group_id == grp).row_id
    chk = rowcheck.RowChecker(solve_b, rowcheck.TestOnlyG13(fail_ids={victim}), heldout=heldout, pool=pool)
    acc, rep = build.build_rows_checked(specs, pool, chk)
    members = {s.row_id for s in specs if s.group_id == grp}
    assert members and not (members & {s.row_id for s, _, _ in acc})
    assert rep["retired_groups"] == [grp]
    assert rep["first_pass_drop_rates"]["g13:G13_HIT"] == len(members) / len(specs)        # collateral counted (GV5)
    assert rep["trigger_lines"]["g13_non_exempt"]["rate"] == len(members) / len(specs)
    assert json.dumps(chk.log[-1].__dict__, default=str).count("test_target") == 1        # target + method only
    # no text anywhere in the drop log
    assert "Assistant" not in json.dumps([v.__dict__ for v in chk.log], default=str)


def test_exempt_scaffold_hit_is_accepted_but_flagged(specs, pool, solve_b, heldout):
    s = specs[0]
    chk = rowcheck.RowChecker(solve_b, rowcheck.TestOnlyG13(exempt_ids={s.row_id}), heldout=heldout, pool=pool)
    acc, rep = build.build_rows_checked([x for x in specs if x.group_id == s.group_id], pool, chk)
    assert acc and acc[0][2]["verdict"] == "clean-exempt-scaffold"


def test_wording_salt_moves_wording_but_not_the_skeleton(specs, pool):
    from t41c import gates
    s = _first(specs, lambda x: len(x.directives) == 1 and x.directives[0].agent_directed)
    r0, r1 = build_row(s, pool), build_row(s, pool, wording_salt="w1")
    assert r0.slot_texts != r1.slot_texts or r0.spans[r0.task_span].text != r1.spans[r1.task_span].text
    sk0 = [t for i, tag, t in rowcheck._skeleton_text(r0) if i != r0.task_span]
    sk1 = [t for i, tag, t in rowcheck._skeleton_text(r1) if i != r1.task_span]
    assert sk0 == sk1
    assert [(a.role, a.sub) for a in r0.anchors if a.role.startswith("fact.")] == [(a.role, a.sub) for a in r1.anchors if a.role.startswith("fact.")]


def test_salt_is_group_level_so_a_task_edit_pair_stays_a_pair(specs, pool):
    te = [s for s in specs if s.pair_kind == "taskedit"]
    g = te[0].group_id
    mem = [s for s in te if s.group_id == g]
    texts = [build_row(m, pool, wording_salt="w2").slot_texts for m in mem]
    assert len(mem) == 2 and texts[0] == texts[1]


def test_check_at_generation_build_matches_the_plain_build_on_clean_rows(specs, pool, checker):
    plain, _ = build.build_rows(specs, pool)
    acc, rep = build.build_rows_checked(specs, pool, checker)
    assert {s.row_id for s, _ in plain} >= {s.row_id for s, _, _ in acc} - {s.row_id for s in specs if False}
    assert len(acc) >= 0.97 * len(plain)
    assert all(st["g13_hook"] == "test_only" for _, _, st in acc)
    assert rep["combined_fix_triggered"] is False
    json.dumps(rep, default=str)


def test_stream_monitor_reports_and_never_drops(specs, pool, checker):
    mon = build.StreamMonitor(min_rows=100)
    big, _ = planner.plan_specs(600)
    acc, rep = build.build_rows_checked(big, pool, checker, monitor=mon, batch=300)
    assert rep["monitor"]["status"] == "ok" and set(rep["monitor"]["views"]) == {"K1_format", "K2_meta", "K2_fine_slot_size"}
    assert len(acc) > 500


def test_job_manifest_names_the_family():
    s, _ = planner.plan_specs(40)
    assert export.job_manifest(s)["family"] == "T41c"


def test_solver_independence_b_imports_nothing_from_the_generator():
    import ast, os
    here = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "solver_b")
    for fn in ("b_program.py", "verbs.py"):
        tree = ast.parse(open(os.path.join(here, fn), encoding="utf-8").read())
        mods = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                mods |= {a.name.split(".")[0] for a in n.names}
            elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
                mods.add(n.module.split(".")[0])
        assert not (mods & {"t41c", "table", "spec", "ids", "planner", "worlds", "render"}), (fn, mods)


def test_generator_never_reads_the_closed_verb_list():
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for fn in os.listdir(os.path.join(root, "t41c")):
        if fn.endswith(".py"):
            src = open(os.path.join(root, "t41c", fn), encoding="utf-8").read()
            assert "DELEGATION_VERBS" not in src and "DELEGATION_PHRASES" not in src, fn


def test_handoff_files_match_the_exporters():
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assert json.load(open(os.path.join(root, "handoff", "ROW_SCHEMA_FOR_B.json"))) == export.row_schema_for_b()
    assert json.load(open(os.path.join(root, "handoff", "POOL_CELLS.json"))) == export.pool_cells_brief()


def test_delegation_clauses_of_the_test_pool_carry_a_closed_list_verb(solve_b):
    """Pool-time check on the task cells, answered by B (A never sees the list)."""
    p = pools.make_test_pool()
    n = 0
    for cell, ents in p.cells.items():
        if cell.startswith("task.") and cell.rsplit(".", 1)[-1] != "none":
            for e in ents:
                t = e["text"]
                if "<<ptr>>" in t:
                    n += 1
                    clause = t.split("<<ptr>>")[1].split("<</ptr>>")[0]
                    assert solve_b.has_generic_verb(clause), clause
    assert n > 20


def test_prefreeze_report_runs_through_the_check_at_generation_path(pool, solve_b, heldout):
    from t41c import report
    chk = rowcheck.RowChecker(solve_b, rowcheck.TestOnlyG13(), heldout=heldout, pool=pool)
    res = report.run_prefreeze(500, pool=pool, boot=20, checker=chk, with_null=False)
    assert {"K1", "K2", "K3", "K4", "K5", "K8", "K9", "K12"} <= set(res["gates"])
    assert res["build"]["check_at_generation"]["g13_hook"] == "test_only" and res["n_built"] > 450
