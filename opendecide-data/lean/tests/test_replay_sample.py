"""c_build/replay_sample.py: the E2 re-stratification (C_DATA_SPEC.md v4 section 5) and the second pass's p_g rule.
CPU, synthetic rows only (the real pool is never read here).

Run:  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -m pytest -q tests/test_replay_sample.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LEAN / "c_build"))
sys.path.insert(0, str(LEAN))
import replay_sample as rsm  # noqa: E402


def _pool(spec):
    """spec: [(unit_name, source, wording, family, [golds])] -> rows, units (yes/no hard-label rows)."""
    rows, units = [], []
    for name, src, w, f, golds in spec:
        idx = []
        for g in golds:
            idx.append(len(rows))
            rows.append({"id": f"{name}_{len(idx)}", "source": src, "qtype": "noul", "soft": False, "gold_probs": False,
                         "gold": g, "w": w, "wf": f, "role": "orig"})
        units.append({"rows": idx, "source": src, "id": name, "types": []})
    return rows, units


def _rate(rows, units, sel, w):
    n = y = 0
    for ui in sel:
        for i in units[ui]["rows"]:
            if rows[i]["w"] == w:
                n, y = n + 1, y + rows[i]["gold"]
    return n, y


def test_shrinking_a_cell_under_50_does_not_fix_it():
    """Review case: a 50-row wording cell at 60% yes. Swapping one unit for another wording's unit takes it to 45 rows,
    which the old score counted as fixed (a cell under 50 scored 0). The cell stays scored on its own rate, so the
    swap that fixes the rate is taken."""
    spec = [(f"a{k}", "s", "w_a", "f_a", [1, 1, 1, 0, 0]) for k in range(10)]           # 50 rows, 30 yes
    spec += [(f"pb{k}", "s", "w_b", "f_b", [1, 0, 1, 0, 1]) for k in range(3)]          # other wording, same size
    spec += [("pa_no", "s", "w_a", "f_a", [0, 0, 0, 0, 0])]                              # same wording, gold no
    rows, units = _pool(spec)
    sel, pool = set(range(10)), set(range(10, 14))
    new, _, swaps, stuck, sticky = rsm.restratify(rows, units, sel, pool)
    n, y = _rate(rows, units, new, "w_a")
    assert sticky == {"w_a"} and swaps >= 1 and not stuck
    assert rsm.BAND[0] <= y / n <= rsm.BAND[1], (n, y)
    rep = rsm.e2_report(rows, units, new, sticky=sticky)
    assert rep["cells_out_of_band"] == 0 and rep["start_cells"]["out_of_band_own_rate"] == 0


def test_sticky_cell_with_no_fix_is_reported_not_hidden():
    """No same-wording unit can fix the cell; the only swaps would shrink it at the same rate. That is no gain (a cell
    under 50 rows keeps the weight of 50), so nothing moves, the cell is stuck, and the after-report shows it."""
    spec = [(f"a{k}", "s", "w_a", "f_a", [1, 1, 1, 1, 0]) for k in range(10)]           # 50 rows, 80% yes
    spec += [(f"pb{k}", "s", "w_b", "f_b", [1, 0, 1, 0, 0]) for k in range(2)]
    rows, units = _pool(spec)
    new, _, swaps, stuck, sticky = rsm.restratify(rows, units, set(range(10)), set(range(10, 12)))
    rep = rsm.e2_report(rows, units, new, sticky=sticky)
    assert swaps == 0 and stuck == ["w:w_a"] and new == set(range(10))
    assert rep["cells_out_of_band"] == 1 and rep["start_cells"]["out_of_band_own_rate"] == 1
    assert rep["start_cells"]["worst"][0] == {"cell": "w:w_a", "n": 50, "yes_rate": 0.8}


def test_pen_any_gives_no_gain_for_shrinking_under_50():
    assert rsm._pen_any(45, 27) == pytest.approx(rsm._pen_any(50, 30)) == pytest.approx(2.5)
    assert rsm._pen(49, 40) == 0 and rsm._pen_any(0, 0) == 0 and rsm._pen_any(50, 25) == 0


def test_shrunk_cell_pools_into_its_family_and_is_scored_there():
    """Cells are re-derived after every swap: a wording that falls under 50 rows pools into its family. Here the family
    already holds 40 rows at 25% yes from small wordings (unchecked, < 50 rows). Moving w_a (50 rows) into it would make
    an out-of-band family cell of 85 rows, so that swap is refused; the in-wording fix is taken instead."""
    spec = [(f"a{k}", "s", "w_a", "fam", [1, 1, 1, 0, 0]) for k in range(10)]           # 50 rows, 60% yes
    spec += [(f"c{k}", "t", f"w_c{k}", "fam", [1, 0, 0, 0, 0]) for k in range(8)]      # 40 rows, 20% yes, small wordings
    spec += [("pb", "s", "w_b", "f_b", [1, 0, 1, 0, 1]), ("pa_no", "s", "w_a", "fam", [0, 0, 0, 0, 0])]
    rows, units = _pool(spec)
    new, _, _, stuck, sticky = rsm.restratify(rows, units, set(range(18)), {18, 19})
    rep = rsm.e2_report(rows, units, new, sticky=sticky)
    n, y = _rate(rows, units, new, "w_a")
    assert n == 50 and rsm.BAND[0] <= y / n <= rsm.BAND[1]
    assert rep["cells_out_of_band"] == 0 and rep["start_cells"]["out_of_band_own_rate"] == 0
    assert 18 in set(range(20)) - new  # the other-wording unit stayed in the pool


def test_family_cell_out_of_band_is_restratified():
    spec = [(f"c{k}", "s", f"w_c{k}", "fam", [1, 1, 1, 1, 0]) for k in range(12)]     # 60 rows in small wordings, 80%
    spec += [(f"p{k}", "s", f"w_p{k}", "fam", [0, 0, 0, 0, 1]) for k in range(12)]
    rows, units = _pool(spec)
    new, _, swaps, stuck, _ = rsm.restratify(rows, units, set(range(12)), set(range(12, 24)))
    rep = rsm.e2_report(rows, units, new)
    assert swaps > 0 and not stuck and rep["cells_out_of_band"] == 0 and rep["family_cells_checked"] == 1


def test_fixed_units_count_but_never_move():
    spec = [(f"a{k}", "s", "w_a", "f_a", [1, 1, 1, 0, 0]) for k in range(10)]
    spec += [("pa_no", "s", "w_a", "f_a", [0, 0, 0, 0, 0])]
    rows, units = _pool(spec)
    fixed = set(range(5))
    new, _, _, _, _ = rsm.restratify(rows, units, set(range(5, 10)), {10}, fixed=fixed)
    assert not (new & fixed) and 10 in new


# ---------------------------------------------------------------- second pass: the p_g rule for attacked rows

def test_pg_rule_flag_defaults_to_clean_partner_and_needs_an_amendment(tmp_path, monkeypatch):
    """Orchestrator decision (disclosed in the C PREREG amendment): an attacked row with p_g < 0.2 is counted, not
    dropped, and its unit is judged by the clean partner. The default refuses until the amendment is named and found."""
    ap = rsm.parser()
    a = ap.parse_args(["--second-pass", "x"])
    assert a.attacked_pg_rule == "clean_partner"
    with pytest.raises(SystemExit, match="amendment"):
        rsm.pg_rule(a)
    a = ap.parse_args(["--second-pass", "x", "--attacked-pg-rule", "spec"])
    assert rsm.pg_rule(a) == {"attacked_rows": "spec", "amendment": None}
    prereg = tmp_path / "PREREG_FINAL.md"
    prereg.write_text("## Amendment A15: attacked replay rows are judged through their clean partner\n")
    monkeypatch.setattr(rsm, "PREREG", prereg)
    a = ap.parse_args(["--second-pass", "x", "--pg-rule-amendment", "A16"])
    with pytest.raises(SystemExit, match="A16"):
        rsm.pg_rule(a)
    a = ap.parse_args(["--second-pass", "x", "--pg-rule-amendment", "A15"])
    assert rsm.pg_rule(a) == {"attacked_rows": "clean_partner", "amendment": "A15"}


def test_ohs3_hit_sources_match_build_fix2_and_no_a10_id_input():
    """A8-prime whole-source rule: the same two sources as extra/build_fix2.py; the A10 7-unit id file is gone."""
    import ast
    tree = ast.parse((LEAN / "extra/build_fix2.py").read_text())
    fix2 = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                and getattr(n.targets[0], "id", "") == "OHS3_HIT_SOURCES")
    assert rsm.OHS3_HIT_SOURCES == fix2 == ("gd_redocred", "gd_helpsteer3_pref")
    opts = {s for act in rsm.parser()._actions for s in act.option_strings}
    assert "--ohs3-overlap-ids" not in opts


@pytest.mark.parametrize("rule,dropped", [("spec", {"u_att"}), ("clean_partner", set())])
def test_pg_drop_units(rule, dropped):
    """Spec rule: every human-labelled hard-label row with p_g < 0.2 drops its unit, attacked rows included. The
    clean_partner rule (only by amendment) counts a low attacked row instead and judges the unit by its clean row."""
    rows = [{"id": "c", "source": "gd_x", "unit": "u_att", "attacked": False, "own_target": False, "p_g": 0.9},
            {"id": "a", "source": "gd_x", "unit": "u_att", "attacked": True, "own_target": False, "p_g": 0.05},
            {"id": "p", "source": "gd_gen2_x", "unit": "u_prog", "attacked": False, "own_target": False, "p_g": 0.01},
            {"id": "s", "source": "gd_x", "unit": "u_soft", "attacked": False, "own_target": True, "p_g": 0.01}]
    drop, att_low = rsm.pg_drop_units(rows, rule)
    assert drop == dropped and att_low == 1


# ---------------------------------------------------------------- 3.H.3 deny-list parts (split scope: train provenance)

def _row(source, group, dataset="", domain=""):
    return {"source": source, "group": group, "dataset": dataset, "domain": domain}


SPLIT_PART = {"field": "split", "values": ["test", "validation", "valid", "dev", "eval"], "rule": "train_provenance"}


def test_split_part_keeps_only_proven_train_rows():
    """Fail closed: a split-scope taint keeps a row only when the row is proven to come from a train split."""
    ok = {"arc": "build_train_v06.py:55"}
    keep = [_row("clinc150", "g:clinc150:train:12474"),
            _row("gd_winogrande", "g:gd:winogrande:xl_train_17826", "allenai/winogrande"),
            _row("gd_ragtruth_summary", "g:gd:ragtruth_summary:rt-1608",
                 "ParticleMedia/RAGTruth (Summary task, train split)"),
            _row("arc", "g:arc:Mercury_409819")]
    for r in keep:
        assert rsm.part_drop(r, [SPLIT_PART], ok) is None, r
    drop = [_row("clinc150", "g:clinc150:validation:77"),                       # the fake validation-split row
            _row("clinc150", "g:clinc150:test:5"),
            _row("gd_winogrande", "g:gd:winogrande:xl_dev_00012", "allenai/winogrande"),
            _row("gd_ragtruth_summary", "g:gd:ragtruth_summary:rt-9", "ParticleMedia/RAGTruth (Summary task, test split)"),
            _row("gd_ragtruth_summary", "g:gd:ragtruth_summary:rt-9", "ParticleMedia/RAGTruth (Summary task)"),
            _row("arc", "g:arc:Mercury_409819_x") | {"source": "arc_other"},     # no declaration for this source
            _row("binj_offensive", "g:binj_offensive:ap_ginger_train"),            # 'train' as a word is no proof
            _row("clinc150", "g:clinc150:train:1", "x (validation split)")]       # contradiction refutes
    for r in drop:
        assert rsm.part_drop(r, [SPLIT_PART], ok), r
    assert rsm.part_drop(_row("arc", "g:arc:Mercury_409819"), [SPLIT_PART], {"arc": None})   # declaration not found


def test_every_part_applies_and_unknown_fields_fail():
    parts = [{"field": "dataset", "values": ["Foo (Anthropic/hh-rlhf)"]}, SPLIT_PART]
    assert rsm.part_drop(_row("gd_x", "g:gd:x:train_1", "Foo (Anthropic/hh-rlhf)"), parts, {}) == "3.H taint part (dataset)"
    assert rsm.part_drop(_row("gd_x", "g:gd:x:test_1", "Bar"), parts, {}).startswith("3.H taint part (split)")
    assert rsm.part_drop(_row("gd_x", "g:gd:x:train_1", "Bar"), parts, {}) is None
    with pytest.raises(SystemExit):
        rsm.part_drop(_row("gd_x", "g:gd:x:train_1"), [{"field": "language", "values": ["en"]}], {})
    old = {"part": {"field": "dataset", "values": ["a"]}, "parts_all": [{"field": "dataset", "values": ["a"]},
                                                                         SPLIT_PART]}
    assert rsm.verdict_parts(old) == [{"field": "dataset", "values": ["a"]}, SPLIT_PART]
    assert rsm.verdict_parts({"parts": [], "part": None}) == []


def test_declared_split_is_rechecked_in_the_builder(tmp_path):
    assert rsm.check_declared_splits()["arc"] == "build_train_v06.py:55"
    b = tmp_path / "b.py"
    b.write_text('x = 1\nds = load_dataset("allenai/ai2_arc", "ARC-Challenge", split="validation")\ng = f"g:arc:{x[\'id\']}"\n')
    decl = {"arc": dict(rsm.TRAIN_SPLIT_DECLARED["arc"], builder=str(b))}
    assert rsm.check_declared_splits(decl) == {"arc": None}


def _good_verdicts(tmp_path):
    dl = tmp_path / "denylist.json"
    dl.write_text("{}\n")
    return {"program": "c_src/common/denylist.py", "run": "replay", "canonical": True, "provisional": [],
            "query_sha256": "q", "program_sha256": rsm.sha256_path(rsm.DENYLIST_PY),
            "aliases_sha256": rsm.sha256_path(rsm.DENY_ALIASES), "denylist": str(dl),
            "denylist_sha256": rsm.sha256_path(dl),
            "platform_rule": "RULED (PREREG_FINAL.md A16 a): a bare platform word never matches on its own",
            "verdicts": {"a": {}, "b": {}}}


def test_denylist_verdict_blockers(tmp_path):
    good = _good_verdicts(tmp_path)
    assert rsm.denylist_blockers(good, "q", ["a", "b"]) == []
    assert any("stale" in x for x in rsm.denylist_blockers(good, "other", ["a", "b"]))
    assert any("no verdict" in x for x in rsm.denylist_blockers(good, "q", ["a", "b", "c"]))
    assert any("non-canonical" in x for x in rsm.denylist_blockers(dict(good, canonical=False), "q", ["a"]))
    assert any("provisional" in x for x in rsm.denylist_blockers(dict(good, provisional=["x"]), "q", ["a"]))
    # pre-A16 verdicts (no RULED platform rule in the header) are refused
    assert any("A16" in x for x in rsm.denylist_blockers({k: v for k, v in good.items() if k != "platform_rule"},
                                                         "q", ["a"]))


def test_denylist_verdicts_must_match_the_current_program_aliases_and_denylist(tmp_path):
    """Staleness: verdicts built by another denylist.py, from other aliases, or naming a deny-list file that changed
    are refused for writing."""
    good = _good_verdicts(tmp_path)
    b = rsm.denylist_blockers(dict(good, program_sha256="0" * 64), "q", ["a", "b"])
    assert len(b) == 1 and "another denylist.py" in b[0]
    b = rsm.denylist_blockers(dict(good, aliases_sha256="0" * 64), "q", ["a", "b"])
    assert len(b) == 1 and "another deny_aliases.json" in b[0]
    Path(good["denylist"]).write_text('{"changed": 1}\n')
    b = rsm.denylist_blockers(good, "q", ["a", "b"])
    assert len(b) == 1 and "deny-list file" in b[0]
    b = rsm.denylist_blockers(dict(good, denylist=str(tmp_path / "missing.json")), "q", ["a", "b"])
    assert len(b) == 1 and "deny-list file" in b[0]
    assert rsm._lean_path("lean/c_build/denylist.json") == rsm.LEAN / "c_build" / "denylist.json"


def test_write_path_refuses_allow_pending():
    with pytest.raises(SystemExit, match="allow-pending"):
        rsm.main(["--write-shards", "--allow-pending", "--sealed-sha", "f" * 64])


def test_meta_split_is_a_train_proof_and_a_refutation():
    r = lambda split, group="g:x:abc", ds="": dict(_row("x", group, ds), split=split)
    assert rsm.part_drop(r("train"), [SPLIT_PART], {}) is None
    assert rsm.train_provenance(r("train"), {}) == (True, "meta.split train")
    for s in ("validation", "test", "dev", "eval"):
        assert rsm.part_drop(r(s), [SPLIT_PART], {}), s
        assert rsm.part_drop(r(s, "g:x:train"), [SPLIT_PART], {}), s       # a non-train meta.split refutes
    assert rsm.part_drop(r("train", "g:x:test_1"), [SPLIT_PART], {})       # a test token in group_id still refutes
    assert rsm.part_drop(r("other"), [SPLIT_PART], {})                     # no proof -> dropped (fail closed)
    assert rsm.part_drop(r(""), [SPLIT_PART], {})


def test_sealed_sha_must_be_the_a15_suite_sha(tmp_path):
    sha = "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68"
    assert rsm.sealed_sha_problem(sha) is None                                 # the real PREREG_FINAL.md
    txt = ("> **Amendment A14 (x): rules.** suite `suite_v2.jsonl`, sha256 `" + "a" * 64 + "`\n"
           "> **Amendment A15 (x): frozen.**\n>   - suite `suite_v2.jsonl`, sha256 `" + sha + "`;\n"
           ">   - scorer `score_nd.py`, sha256 `" + "b" * 64 + "`.\n> **Amendment A16 (x): plan.** " + "c" * 64 + "\n")
    assert rsm.sealed_sha_problem(sha, txt) is None
    assert "not in the A15 block" in rsm.sealed_sha_problem("a" * 64, txt)
    assert "not in the A15 block" in rsm.sealed_sha_problem("c" * 64, txt)
    assert "not as the suite" in rsm.sealed_sha_problem("b" * 64, txt)
    assert "64-hex" in rsm.sealed_sha_problem("f4ae", txt)
    assert "no 'Amendment A15'" in rsm.sealed_sha_problem(sha, "nothing here " + sha)


def test_sampler_default_reads_the_path_denylist_writes():
    sys.path.insert(0, str(LEAN / "c_src" / "common"))
    import denylist as D
    assert Path(rsm.parser().parse_args(["--dry-run"]).denylist_verdicts) == D.REPLAY_VERDICTS
    assert D.REPLAY_QUERY == rsm.HERE / "replay_denylist_query.json"
