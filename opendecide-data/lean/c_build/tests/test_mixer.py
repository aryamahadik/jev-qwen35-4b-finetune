"""Synthetic-fixture tests for mixer.py and mixio.py (guards, anchor merge, option_level, G18, units, token cap,
config fill, deny-list query, decontam hook). CPU only; no real data is read."""
import json
import sys
from collections import Counter
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import mixer as mx  # noqa: E402
import mixio  # noqa: E402


def ordinal_row(gold="0: low", teacher=None, src="pg_routing", gp=None):
    o = ["0: low", "1: mid", "2: high"]
    m = {"option_level": {x: i for i, x in enumerate(o)}}
    if teacher is not None:
        m |= {"teacher": teacher, "teacher_src": "human_votes"}
    if gp is not None:
        m["gold_probs"] = gp
    return {"id": "o1", "source": src, "qtype": "choice", "options": o, "gold": gold, "meta": m, "call_id": "c"}


def test_guard_refuses_never_open_and_jev_paths(tmp_path):
    lean = mixio.LEAN
    for p in ("sealed_nd/suite_v2.jsonl", "c_spec/sealed_brief/x", "c_spec/RESEARCH_a.md", "c_spec/REVIEW_rules.md",
              "c_spec/LICENCE_CHECK_1.md", "c_spec/ADDENDUM_research.md", "ohs3/used_sources.json",
              "data/ohs3_test.jsonl", "data/x_ohs3.jsonl", "prep89/a", "preds_ohs2/a.jsonl", "preds/jev_dev.jsonl",
              "logs/jev_ohs.log", "../../bench/ejs5/runs/a", "../../reports/OpenDecide_v05_vs_Jev.md",
              "run_jevbench.py"):
        assert mixio.refusal(lean / p), p
    assert mixio.refusal(Path.home() / ".claude/projects/x/y")
    assert mixio.refusal(lean / "c_src/F1/out/candidates_r1.jsonl") is None
    assert mixio.refusal(lean / "data/c_replay_r1_shards/shard_000.jsonl") is None
    with pytest.raises(mixio.GuardError):
        mixio.InputLog().open(lean / "preds_ohs/x.jsonl")


def test_row_key_jev_refused():
    with pytest.raises(mixio.GuardError):
        mixio.check_row_keys({"id": "a", "meta": {"jev_recorded_p_yes": 0.4}})
    assert mixio.check_row_keys({"id": "a", "meta": {"x": 1}})


def test_input_log_records_sha(tmp_path):
    f = mixio.LEAN / "c_build" / "tests" / "test_mixer.py"
    lg = mixio.InputLog()
    lg.record(f)
    (k, v), = lg.entries.items()
    assert k.endswith("test_mixer.py") and len(v["sha256"]) == 64


def test_detect_option_level():
    r = {"qtype": "choice", "options": ["1: a", "3: c", "2: b"], "gold": "2: b"}
    assert mx.detect_option_level(r) == {"1: a": 0, "3: c": 2, "2: b": 1}
    assert mx.detect_option_level({"qtype": "choice", "options": ["22", "23", "24"], "gold": "22"}) is None
    assert mx.detect_option_level({"qtype": "choice", "options": ["1 liter", "2 liters"], "gold": "1 liter"}) is None
    assert mx.detect_option_level({"qtype": "choice", "options": ["0: a", "2: b"], "gold": "0: a"}) is None


def test_g18_spec_examples_and_fallback():
    r = ordinal_row(teacher={"0: low": 0.55, "1: mid": 0.35, "2: high": 0.10})
    # 0.5 x smoothed gold + 0.5 x votes: E = 0.5*(0.0333*1+0.0167*... ) -> check by the program
    rows, dropped = mx.g18_lint([r], "replay", cnt := {})
    assert not dropped and mx.g18_ok(rows[0])
    bad = ordinal_row(gold="0: low", gp={"0: low": 0.4, "1: mid": 0.1, "2: high": 0.5})
    assert not mx.g18_ok(bad)
    rows, dropped = mx.g18_lint([bad], "F7", cnt2 := {})
    assert not dropped and rows[0]["meta"].get("g18_fallback") == "smoothed_gold" and cnt2["F7"]["pg_routing"] == [1, 1, 0]
    assert mx.g18_ok(ordinal_row(gold="2: high"))


def test_train_target_matches_trainer_formula():
    r = ordinal_row(teacher={"0: low": 1.0, "1: mid": 0.0, "2: high": 0.0})
    q = mx.train_target(r)
    assert abs(sum(q) - 1) < 1e-9 and abs(q[0] - (0.5 * (0.05 / 3 + 0.95) + 0.5)) < 1e-9


def test_merge_replay_targets_anchor_blend50_licence():
    cnt = Counter()
    r = {"id": "r1", "source": "pg_policy", "qtype": "noul", "gold": 1, "meta": {}}
    out = mx.merge_replay_targets(r, {"anchor": "c1_anchor"}, {"r1": {"yes": 0.9, "no": 0.1}}, cnt)
    assert out["meta"]["teacher"] == {"yes": 0.9, "no": 0.1} and out["meta"]["teacher_src"] == "c1_anchor"
    assert out["meta"]["licence"].startswith("CC0")
    b = {"id": "r2", "source": "x", "qtype": "noul", "gold": 0, "meta": {"teacher": {"yes": 0.3},
                                                                          "teacher_src": "blend50", "licence": "MIT"}}
    out = mx.merge_replay_targets(b, {"anchor": None}, {}, cnt)
    assert "teacher" not in out["meta"] and cnt["blend50_stripped"] == 1
    v = {"id": "r3", "source": "x", "qtype": "choice", "options": ["a", "b"], "gold": "a",
         "meta": {"teacher": {"a": 0.6, "b": 0.4}, "teacher_src": "human_votes", "licence": "CC BY 4.0"}}
    out = mx.merge_replay_targets(v, {"anchor": "c1_anchor"}, {"r3": {"a": 0.99, "b": 0.01}}, cnt)
    assert out["meta"]["teacher_src"] == "human_votes"      # own target kept, never anchored
    c = {"id": "r4", "source": "x", "qtype": "choice", "options": ["a", "b"], "gold": "a", "meta": {"licence": "MIT"}}
    out = mx.merge_replay_targets(c, {"anchor": "c1_anchor_protected"}, {"r4": {"a": 0.6, "b": 0.4}}, cnt)
    assert set(out["meta"]["teacher"]) == {"a", "b"} and cnt["c1_anchor_protected"] == 1


def mk(i, cid, block="F1", tok=100, **kw):
    return {"id": i, "call_id": cid, "_block": block, "source": "c_own_F1", "qtype": "noul", "gold": 1,
            "role": "base", "meta": {"licence": "CC0"}, **kw}


def test_unit_check_flags_big_long_split_and_span():
    rows = [mk("a", "u1"), mk("b", "u1"), mk("c", "u1"), mk("d", "u1"),        # 4-row unit
            mk("e", "u2"), mk("f", "u2"), mk("g", "u2"),                       # long 3-row unit
            mk("h", "u3"), mk("i", "u4"),                                      # relation split across call_ids
            mk("j", "u5"), mk("k", "u5", block="public")]                      # call_id spans blocks
    ntok = {r["id"]: 100 for r in rows} | {"e": 2500}
    rels = [{"a": "h", "b": "i", "type": "complement"}]
    rep = {}
    probs = mx.unit_check(rows, rels, ntok, rep)
    u = rep["g15_units"]
    assert u["units_over_3"] == 1 and u["long_units_over_2"] == 1 and u["relation_pairs_split_call_id"] == 1
    assert u["call_id_spans_blocks"] == 1 and len(probs) == 4


def test_token_cap_drops_long_f13_first():
    rows = [mk(f"r{i}", f"c{i}", block="replay") for i in range(10)]
    rows += [mk(f"n{i}", f"d{i}") for i in range(80)]
    rows += [mk(f"L{i}", f"e{i}", block="F13") for i in range(20)]
    ntok = {r["id"]: 500 for r in rows} | {f"L{i}": 6500 for i in range(20)}
    rep = {}
    drop, probs = mx.token_cap(rows, ntok, rep)
    assert drop and all(d.startswith("L") for d in drop)
    assert rep["token_cap"]["long_token_share"] <= 0.30
    assert len(drop) == 18 and not probs


def test_drop_units_and_rows():
    rows = [mk("a", "u1"), mk("b", "u1"), mk("c", "u2")]
    rels = [{"a": "a", "b": "b", "type": "equiv"}]
    keep, krels, n = mx.drop_units(rows, rels, {"a"})
    assert [r["id"] for r in keep] == ["c"] and not krels and n == 2
    keep, krels = mx.drop_rows(rows, rels, {"b"})
    assert [r["id"] for r in keep] == ["a", "c"] and not krels


def test_largest_remainder_and_exact_total():
    assert sum(mx.largest_remainder({"a": 1, "b": 2, "c": 3}, 10).values()) == 10
    units = {0: {"rows": [0]}, 1: {"rows": [1, 2]}, 2: {"rows": [3]}, 3: {"rows": [4]}}
    take = {"s": [0, 1, 2, 3]}
    out = mx.exact_total(take, {"s": 3}, units, 3)
    assert sum(len(units[u]["rows"]) for u in out["s"]) == 3


def test_config_fill_epochs_rule():
    rows = [mk(f"a{i}", f"u{i // 2}") for i in range(400)]                  # 2-row units
    fill = mx.config_fill(rows, [])
    assert 16 <= fill["measured_rows_per_step"] <= 17.1
    assert abs(fill["epochs"] - 16 / fill["measured_rows_per_step"]) < 1e-3
    assert fill["expect_ord_rows"] == 0 and fill["expect_kd_targets"] == 0 and fill["seed"] == 20261003


def test_config_fill_counts_kd_and_ordinal():
    o = ordinal_row()
    rows = [o | {"_block": "F7"},
            mk("k1", "u1", meta={"teacher": {"yes": 0.7}, "teacher_src": "c1_anchor"}),
            mk("k2", "u2", meta={"teacher": {"yes": 0.7}, "teacher_src": "blend50"}),
            mk("k3", "u3", meta={"teacher": {"yes": 0.7}, "teacher_src": "c1_anchor"}) | {"source": "gd_gen2_probability"}]
    rows += [mk(f"f{i}", f"v{i}") for i in range(60)]
    fill = mx.config_fill(rows, [])
    with pytest.raises(ValueError):
        mx.config_fill(rows[:5], [])
    assert fill["expect_ord_rows"] == 1 and fill["expect_kd_targets"] == 2 and fill["expect_kd_full"] == 1


def test_denylist_query_entries():
    rows = [{"id": "1", "source": "c_pub_x", "meta": {"dataset": "X set"}},
            {"id": "2", "source": "c_own_F10", "meta": {"persona_seed": "11-1011.00",
                                                        "text_source": {"dataset": "EDOS", "split": "train"}}}]
    q = mx.denylist_query(rows, {"c_pub_x": ["Wikipedia"]})
    assert q["c_pub_x"]["names"] == ["X set", "c_pub_x"] and q["c_pub_x"]["parents"] == ["Wikipedia"]
    assert "parents" not in q["c_own_F10"] and "text:EDOS" in q     # undeclared: denylist.py's own G1 refusal applies
    q = mx.denylist_query(rows, {"c_pub_x": ["Wikipedia"], "c_own_F10": []})
    assert q["c_own_F10"]["parents"] == [mx.ONET_PARENT] and q["text:EDOS"]["parents"] == []


def test_decontam_hook(tmp_path):
    f = mixio.LEAN / "c_build" / "tests" / "_tmp_decontam.json"
    f.write_text(json.dumps({"drop_ids": ["a", "b"]}))
    try:
        ids, used = mx.decontam_drop_ids(mixio.InputLog(), [f])
        assert ids == {"a", "b"} and used[0]["ids"] == 2
        f.write_text(json.dumps({"counts": 3}))
        with pytest.raises(SystemExit):
            mx.decontam_drop_ids(mixio.InputLog(), [f])
    finally:
        f.unlink()


def test_final_requires_decontam_and_sealed_sha():
    with pytest.raises(SystemExit):
        mx.main(["--final"])                                   # no --decontam-drops
    with pytest.raises(SystemExit):
        mx.build(type("A", (), {"final": True, "sealed_sha": "0" * 64, "decontam_drops": []})())


def test_split_replay_call_ids_keeps_relation_pairs():
    rows = [mk(i, "C", block="replay") for i in ("a", "b", "c", "d", "e")] + [mk("x", "D", block="F1"),
                                                                              mk("y", "D", block="F1"),
                                                                              mk("z", "D", block="F1"),
                                                                              mk("w", "D", block="F1")]
    rels = [{"a": "a", "b": "b", "type": "complement"}, {"a": "c", "b": "d", "type": "inv"}]
    ntok = {r["id"]: 100 for r in rows}
    rep = {}
    rels = mx.split_replay_call_ids(rows, rels, ntok, rep)
    cid = {r["id"]: r["call_id"] for r in rows}
    assert cid["a"] == cid["b"] != cid["c"] == cid["d"] != cid["e"]
    assert cid["x"] == "D" and rep["replay_call_id_split"]["groups_split"] == 1
    assert rep["replay_call_id_split"]["units_after"] == 3
    probs = mx.unit_check(rows, rels, ntok, {})
    assert probs == ["G15 units_over_3 1"]                    # the new-row unit is reported, never split


def test_g10_longest_tie_credit_and_positions():
    rows = []
    for i in range(400):
        o = ["aa", "bb", "cc", "dd"]                           # all tie for longest: credit 1/4 = 1/k
        rows.append({"id": f"q{i}", "_block": "F9", "qtype": "choice", "options": o, "gold": o[i % 4],
                     "role": "base", "source": "c_own_F9", "instructions": "Which?", "meta": {}})
    rep = {}
    probs = mx.g10_checks(rows, rep, False)
    assert rep["g10"]["longest_by_block_pp"]["F9"] == 0.0 and not rep["g10"]["gold_position_fail"], probs


def test_long_replay_triple_split_keeps_inv_pair():
    rows = [mk(i, "T", block="replay") for i in ("a", "b", "c")]
    rels = [{"a": "a", "b": "b", "type": "equiv"}, {"a": "a", "b": "c", "type": "inv"}]
    ntok = {"a": 2500, "b": 100, "c": 100}
    rep = {}
    rels2 = mx.split_replay_call_ids(rows, rels, ntok, rep)
    cid = {r["id"]: r["call_id"] for r in rows}
    assert cid["a"] == cid["c"] != cid["b"] and rels2 == [rels[1]]
    assert mx.unit_check(rows, rels2, ntok, {}) == []
