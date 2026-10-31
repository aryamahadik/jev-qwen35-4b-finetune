"""build_ab_yn2b.py: S over make_units' merged units, arm files, counts, replay, F4(a) and family-balance asserts."""
from __future__ import annotations

import json

import pytest

import build_ab_yn2b as ab
import train_decoder as td
import yn2b_common as yc
from conftest import ch_row, write_jsonl, yn_row

CFG = {"seed": 20260925, "batch": 4, "style": "cygnet", "perm_twin": 0.3, "kd": 0.5, "kd_skip_src": ["blend50"],
       "kd_full_src": ["gd_gen2_probability"], "epochs": "FILL"}


def _kd_rows(n=400):
    rows = []
    for i in range(n):
        if i % 3 == 0:
            rows.append(ch_row(i, teacher={"A": 0.2, "B": 0.7, "C": 0.1} if i % 2 else None))  # gold A: wrong teacher
        else:
            rows.append(yn_row(i, gold=i % 2, teacher=0.9 if i % 4 else None))
    # an attacked twin with ANOTHER call_id: make_units must merge it with its clean partner
    rows.append(yn_row(9999, gold=rows[1]["gold"], call="other", role="attacked"))
    return rows


def _setup(tmp_path, yn2b=None, yn2b_rel=()):
    dd = tmp_path / "data"
    rows = _kd_rows()
    rels = [{"type": "inv", "a": "r1", "b": "r9999"}, {"type": "complement", "a": "r4", "b": "r5"}]
    write_jsonl(dd / "kd.jsonl", rows)
    write_jsonl(dd / "rel.jsonl", rels)
    (tmp_path / "cfg.json").write_text(json.dumps(CFG))
    if yn2b is not None:
        write_jsonl(dd / "yn.jsonl", yn2b)
        write_jsonl(dd / "yn_rel.jsonl", list(yn2b_rel))
    return dd, rows, rels


def _args(tmp_path, arms="A", extra=()):
    return ["--data-dir", str(tmp_path / "data"), "--arms", arms, "--kd-file", "kd.jsonl", "--rel", "rel.jsonl",
            "--yn2b", "yn.jsonl", "--yn2b-rel", "yn_rel.jsonl", "--out-dir", "ab", "--config", str(tmp_path / "cfg.json"),
            *extra]


def test_s_is_drawn_over_merged_units(tmp_path):
    dd, rows, rels = _setup(tmp_path)
    light = [{"id": r["id"], "call_id": r["call_id"], "group_id": r["group_id"]} for r in rows]
    s_ids, s_units, n_all, merged = ab.select_s(light, rels)
    assert merged == 1
    units, _ = td.make_units(rows, rels)
    want = set()
    for u in units:
        if int(yc.sha256_int("yn2b-ab:" + min(r["call_id"] for r in u))) % 8 == 0:
            want |= {r["id"] for r in u}
    assert s_ids == want and n_all == len(units)
    assert ("r1" in s_ids) == ("r9999" in s_ids), "an inv pair is never split"
    assert 0.03 < len(s_units) / n_all < 0.25


def test_arm_a_file_counts_and_replay(tmp_path):
    dd, rows, rels = _setup(tmp_path)
    ab.main(_args(tmp_path))
    out = dd / "ab"
    a_rows = [json.loads(l) for l in open(out / "yn2b_ab_A.jsonl")]
    a_rel = [json.loads(l) for l in open(out / "yn2b_ab_A_rel.jsonl")]
    counts = json.loads((out / "yn2b_ab_A_counts.json").read_text())
    ids = {r["id"] for r in a_rows}
    assert all(x["a"] in ids and x["b"] in ids for x in a_rel)
    # rows keep the KD file's order and bytes
    src = {json.loads(l)["id"]: l for l in open(dd / "kd.jsonl")}
    assert [l for l in open(out / "yn2b_ab_A.jsonl")] == [src[r["id"]] for r in a_rows]
    assert counts["rows"] == len(a_rows)
    assert (counts["kd_targets"], counts["kd_full"]) == yc.counts_kd(a_rows)
    # replay: the epochs value gives exactly one pass under train_decoder's step formula
    import replay_steps as rs
    units, _ = td.make_units(a_rows, a_rel)
    p = rs.first_pass(units, rs.stream_cfg({k: v for k, v in CFG.items() if k != "epochs"}))
    assert counts["replay"]["pass_batches"] == p["batches"]
    assert rs.n_steps(len(a_rows), CFG["batch"], counts["replay"]["epochs"]) == p["batches"]
    assert counts["config_patch"]["expect_kd_targets"] == counts["kd_targets"]
    assert (out / "yn2b_ab_S_units.jsonl").exists()
    # a second run refuses to overwrite
    with pytest.raises(SystemExit):
        ab.main(_args(tmp_path))


def _yn2b_rows(s_ids, n_lat=400, family="gd_gen3_tool_guard"):
    out = []
    for k in range(n_lat):
        for v in range(2):
            r = yn_row(f"y{k}_{v}", gold=(k + v) % 2, source=family, call=f"yl{k}")
            r["id"] = f"r_yn2b_{family}_{k}_{v}"
            r["meta"] = {"latent_id": f"L{k}", "dataset": "p", "licence": "CC0"}
            out.append(r)
    return out


def test_arms_b_and_c(tmp_path):
    dd, rows, rels = _setup(tmp_path)
    light = [{"id": r["id"], "call_id": r["call_id"], "group_id": r["group_id"]} for r in rows]
    s_ids = ab.select_s(light, rels)[0]
    yn = _yn2b_rows(s_ids)
    write_jsonl(dd / "yn.jsonl", yn)
    write_jsonl(dd / "yn_rel.jsonl", [{"type": "complement", "a": yn[0]["id"], "b": yn[1]["id"]}])
    ab.main(_args(tmp_path, "A,B,C"))
    out = dd / "ab"
    A = [json.loads(l) for l in open(out / "yn2b_ab_A.jsonl")]
    B = [json.loads(l) for l in open(out / "yn2b_ab_B.jsonl")]
    C = [json.loads(l) for l in open(out / "yn2b_ab_C.jsonl")]
    assert B[:len(A)] == A
    half = [r for r in B[len(A):]]
    assert half and all(ab.in_half(r["meta"]["latent_id"]) for r in half)
    assert [r["id"] for r in C] == [r["id"] for r in B]
    cc = json.loads((out / "yn2b_ab_C_counts.json").read_text())
    bc = json.loads((out / "yn2b_ab_B_counts.json").read_text())
    assert cc["kd_targets"] < bc["kd_targets"]  # the gate removed the wrong choice teachers in S
    assert cc["files"]["rel_file"].endswith("yn2b_ab_B_rel.jsonl")


def test_family_balance_and_f4a_asserts():
    rows = _yn2b_rows(set(), n_lat=40)
    skew = [r for r in rows if not ab.in_half(r["meta"]["latent_id"])]  # a family where no latent is selected
    with pytest.raises(AssertionError):
        ab.yn2b_half(skew, set())
    ok = _yn2b_rows(set(), n_lat=400)
    f4 = dict(ok[0], meta=dict(ok[0]["meta"], derived_from="r_not_in_S"))
    lid = next(r["meta"]["latent_id"] for r in ok if ab.in_half(r["meta"]["latent_id"]))
    f4["meta"]["latent_id"] = lid
    with pytest.raises(AssertionError):
        ab.yn2b_half(ok + [dict(f4, id="f4a_row")], set())


def test_yn2b_rows_with_teacher_are_refused(tmp_path):
    dd, rows, rels = _setup(tmp_path)
    yn = _yn2b_rows(set(), n_lat=200)
    yn[0]["meta"]["teacher"] = {"yes": 0.5}
    write_jsonl(dd / "yn.jsonl", yn)
    write_jsonl(dd / "yn_rel.jsonl", [])
    with pytest.raises(AssertionError):
        ab.main(_args(tmp_path, "B"))


def test_excluded_ids_leave_every_arm_with_their_relations(tmp_path):
    """--exclude-ids (draft A4): listed rows leave every arm file after S is chosen; S units do not move."""
    dd, rows, rels = _setup(tmp_path)
    light = [{"id": r["id"], "call_id": r["call_id"], "group_id": r["group_id"]} for r in rows]
    s_ids = ab.select_s(light, rels)[0]
    yn = _yn2b_rows(s_ids)
    write_jsonl(dd / "yn.jsonl", yn)
    write_jsonl(dd / "yn_rel.jsonl", [])
    ab.main(_args(tmp_path, "A"))
    s_units_before = (dd / "ab/yn2b_ab_S_units.jsonl").read_text()
    a_before = [json.loads(l) for l in open(dd / "ab/yn2b_ab_A.jsonl")]
    gone = sorted(s_ids)[:3]
    bad = {"about": "test", "groups": {"g1": {"ids": gone[:2]}, "g2": {"ids": gone[2:]}}, "all_ids": gone}
    (tmp_path / "bad.json").write_text(json.dumps(bad))
    ab.main(_args(tmp_path, "A,B,C", ["--exclude-ids", str(tmp_path / "bad.json"), "--exclude-groups", "g1",
                                      "--gate-exclude", str(tmp_path / "bad.json"), "--overwrite"]))
    assert (dd / "ab/yn2b_ab_S_units.jsonl").read_text() == s_units_before
    for arm in "ABC":
        ids = [json.loads(l)["id"] for l in open(dd / f"ab/yn2b_ab_{arm}.jsonl")]
        assert not set(gone[:2]) & set(ids) and gone[2] in ids
    A = [json.loads(l)["id"] for l in open(dd / "ab/yn2b_ab_A.jsonl")]
    assert A == [r["id"] for r in a_before if r["id"] not in gone[:2]]
    counts = json.loads((dd / "ab/yn2b_ab_A_counts.json").read_text())
    assert counts["excluded"]["rows_dropped_from_S"] == 2 and counts["rows"] == len(a_before) - 2
    a_rel = [json.loads(l) for l in open(dd / "ab/yn2b_ab_A_rel.jsonl")]
    assert all(x["a"] not in gone[:2] and x["b"] not in gone[:2] for x in a_rel)
    assert ab.load_excluded(str(tmp_path / "bad.json")) == frozenset(gone)
    with pytest.raises(SystemExit):
        ab.load_excluded(str(tmp_path / "bad.json"), "no_such_group")


def test_arm_c_refuses_a_teacher_source_absent_from_s(tmp_path):
    dd, rows, rels = _setup(tmp_path)
    write_jsonl(dd / "yn.jsonl", _yn2b_rows(set()))
    write_jsonl(dd / "yn_rel.jsonl", [])
    with pytest.raises(SystemExit):
        ab.main(_args(tmp_path, "B,C", ["--teacher-src", "q35_4b_E2v"]))


def test_kd_file_defaults_to_the_config_train_file(tmp_path):
    dd, rows, rels = _setup(tmp_path)
    cfg = dict(CFG, train_file="kd.jsonl")
    (tmp_path / "cfg.json").write_text(json.dumps(cfg))
    args = [x for x in _args(tmp_path) if x not in ("--kd-file",)]
    args.remove("kd.jsonl")
    ab.main(args)
    counts = json.loads((dd / "ab/yn2b_ab_A_counts.json").read_text())
    assert counts["kd_file"]["path"].endswith("kd.jsonl")
