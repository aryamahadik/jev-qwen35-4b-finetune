import json

import pytest

import lr_common as lc
import lr_testlib as T
import datadog_malicious_packages as D


def records(n=20):
    out = []
    for i in range(n):
        eco = ["npm", "pypi"][i % 2]
        vers = None if i % 3 else ["1.0.%d" % i, "1.1.%d" % i]
        out.append({"ecosystem": eco, "name": "evil-pkg-%d" % i, "versions": vers, "_src_line": "%s:evil-pkg-%d" % (eco, i)})
    return out


def negs(n=20):
    return [{"id": "n%d" % i, "ecosystem": ["npm", "pypi"][i % 2], "name": "zq%dkx" % i, "versions": ["2.0.%d" % i]} for i in range(n)]


def test_blocked_until_t63_g0_lite_approved(tmp_path):
    assert D.t63_g0_lite_approved(str(tmp_path)) is False
    m = D.Mapper(T.pools_for(D.Mapper), seed=1, approved_fn=lambda: False)
    with pytest.raises(D.MapperBlocked):
        m.map_records(records())
    # an approval row in a G0_APPROVALS*.md file unblocks the check
    (tmp_path / "G0_APPROVALS_v33.md").write_text("| T63/G0_LITE.md (NEW) | L-P | APPROVE | 0 | T63-B1 |\n")
    assert D.t63_g0_lite_approved(str(tmp_path)) is True
    (tmp_path / "G0_APPROVALS_v33.md").write_text("| T63/G0_LITE.md (NEW) | L-P | REVISE | 3 | none |\n")
    assert D.t63_g0_lite_approved(str(tmp_path)) is False


def test_real_state_blocked_by_field_record_even_though_t63_is_approved():
    # Opus batch 1b approved the T63 G0-lite (REVISE -> APPROVED); T63-M3 still requires a label-bearing field outside the payloads
    assert isinstance(D.t63_g0_lite_approved(), bool)
    assert D.field_record_allows_mapping() is False
    m = D.Mapper(T.pools_for(D.Mapper), seed=1, approved_fn=lambda: True)
    with pytest.raises(D.MapperBlocked):
        m.map_records(records())


def test_field_record_measurement(tmp_path):
    (tmp_path / "npm.manifest.train.json").write_text(json.dumps({"zzpkgA": None, "zzpkgB": ["1.0.0", "1.0.1"], "zzpkgC": None}))
    (tmp_path / "pypi.manifest.train.json").write_text(json.dumps({"zzpkgX": None}))
    out = tmp_path / "rec.json"
    rec = D.measure_field_record(str(tmp_path), str(out))
    assert rec["ecosystems"]["npm"] == {"entries": 3, "null_all_versions": 2, "version_list": 1, "other_value_types": 0, "version_list_len_max": 2}
    assert rec["label_bearing_field_outside_payload"] is False and D.field_record_allows_mapping(str(out)) is False
    assert "zzpkg" not in json.dumps(rec)                      # no package name is written
    (tmp_path / "npm.manifest.train.json").write_text(json.dumps({"zzpkgA": {"description": "x"}}))
    assert D.measure_field_record(str(tmp_path), str(out))["label_bearing_field_outside_payload"] is True
    assert D.field_record_allows_mapping(str(out)) is True
    assert D.field_record_allows_mapping(str(tmp_path / "missing.json")) is False


def test_rows_with_t63_negatives_when_approved():
    m = D.Mapper(T.pools_for(D.Mapper), seed=1, approved_fn=lambda: True, record_fn=lambda: True)
    rows = m.map_records(records(), ctx={"t63_negatives": negs()})
    T.check_rows(rows, m, expect_kind=("yesno",), min_rows=40)
    yes = [r for r in rows if r["answer_text"] == "Yes"]
    assert len(yes) == 20 and all(r["extra"]["t63_gate_exception"] for r in yes)
    rep = T.check_set_report(rows, yes_no=True)
    assert rep["R7_pass"] and rep["yes_rate"] == 0.5
    assert all(r["family"] == "T63" and r["flags"]["p1_realism"] for r in rows)


def test_reader_reads_only_train_manifests(tmp_path):
    (tmp_path / "npm.manifest.train.json").write_text(json.dumps({"a": None, "b": ["1.0.0"]}))
    (tmp_path / "npm.manifest.holdout10.json").write_text(json.dumps({"HELD": None}))
    got = list(D.read_train(str(tmp_path)))
    assert sorted(g["name"] for g in got) == ["a", "b"]
    with pytest.raises(AssertionError):
        list(D.read_train("/x/bench/c21_eval_quarantine/lr_targets/datadog"))


def test_r4_and_empty_name():
    m = D.Mapper(T.pools_for(D.Mapper), seed=1, approved_fn=lambda: True, record_fn=lambda: True)
    recs = records(3) + [{"ecosystem": "npm", "name": "  ", "versions": None, "_src_line": "x"}]
    assert len(m.map_records(recs)) == 3 and m.drops.c["empty_name"] == 1
    m.independent_gold = lambda s, c: "No"
    assert m.map_records(records(2)) == []


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(D.Mapper)
