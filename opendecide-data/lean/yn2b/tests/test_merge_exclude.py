"""merge_yn2b.py for the 2B main file: --exclude-ids (amendment A4), the required --expect-kd (the count AFTER the
exclusion), --expect-kd-full, the assembled-file defaults, --yn2b '' (the A/B FAIL path) and --no-manifest.
CPU only; every file is in tmp_path (the real known-bad list is only read, ids only)."""
from __future__ import annotations

import json

import pytest

import merge_yn2b as mg
import yn2b_common as yc
from conftest import write_jsonl, yn_row


def _kd():
    """10 yes/no rows in 5 complement pairs (calls k0..k4), all with a teacher, plus one kd_full row: 11 kd, 1 full."""
    kd = [yn_row(i, gold=i % 2, teacher=0.8 if i % 2 else 0.2, call=f"k{i // 2}") for i in range(10)]
    kd.append(yn_row(99, gold=1, source="gd_gen2_probability", teacher=0.7, teacher_src="exact"))
    return kd


def _setup(d, kd=None, rel=None, yn=None, yrel=None, bad=None, kd_name="kd.jsonl", yn_name="yn.jsonl",
           yrel_name="yrel.jsonl"):
    kd = _kd() if kd is None else kd
    rel = [{"type": "complement", "a": f"r{2 * k}", "b": f"r{2 * k + 1}"} for k in range(5)] if rel is None else rel
    yn = [dict(yn_row(f"y{i}", gold=i % 2, source="gd_gen3_x", call=f"y{i // 2}"), meta={"latent_id": f"L{i // 2}"})
          for i in range(4)] if yn is None else yn
    yrel = [{"type": "complement", "a": "ry0", "b": "ry1"}] if yrel is None else yrel
    write_jsonl(d / kd_name, kd)
    write_jsonl(d / "rel.jsonl", rel)
    write_jsonl(d / yn_name, yn)
    write_jsonl(d / yrel_name, yrel)
    bad = {"about": "toy", "groups": {"bug": {"reason": "x", "raw_rows": 2, "ids": ["r2", "r3"]},
                                      "amb": {"reason": "y", "raw_rows": 1, "ids": ["r4"]}},
           "all_ids": ["r2", "r3", "r4"]} if bad is None else bad
    (d / "bad.json").write_text(json.dumps(bad))
    return kd, rel, yn, yrel


def _args(d, *extra):
    return ["--data-dir", str(d), "--kd-file", "kd.jsonl", "--rel", "rel.jsonl", "--yn2b", "yn.jsonl",
            "--yn2b-rel", "yrel.jsonl", "--out", "out.jsonl", "--out-rel", "out_rel.jsonl", *extra]


def _ids(path):
    return [json.loads(line)["id"] for line in open(path)]


def test_exclude_group_drops_rows_and_their_relations(tmp_path, _tmp_manifest):
    kd, rel, yn, yrel = _setup(tmp_path)
    s = mg.main(_args(tmp_path, "--exclude-ids", str(tmp_path / "bad.json"), "--exclude-groups", "bug",
                      "--expect-kd", "9", "--expect-kd-full", "1"))
    gone = {"r2", "r3"}
    assert _ids(tmp_path / "out.jsonl") == [r["id"] for r in kd if r["id"] not in gone] + [r["id"] for r in yn]
    kd_lines = [line for line in open(tmp_path / "kd.jsonl") if json.loads(line)["id"] not in gone]
    assert open(tmp_path / "out.jsonl").readlines()[:len(kd_lines)] == kd_lines  # kept rows: bytes and order unchanged
    rels = [json.loads(line) for line in open(tmp_path / "out_rel.jsonl")]
    assert {(x["a"], x["b"]) for x in rels} == {("r0", "r1"), ("r4", "r5"), ("r6", "r7"), ("r8", "r9"), ("ry0", "ry1")}
    assert s["rows_in"] == 11 and s["rows_excluded"] == 2 and s["rows_out"] == 11 - 2 + 4
    assert s["kd_targets_in"] == 11 and s["kd_targets_excluded"] == 2 and s["kd_targets"] == 9 and s["kd_full"] == 1
    assert s["relations_in"] == 5 and s["relations_dropped"] == 1 and s["relations_out"] == 5
    assert s["excluded"]["relations_dropped"] == {"complement": 1}
    assert s["excluded"]["partners_kept_without_their_relation"] == 0
    assert s["excluded"]["groups"] == "bug" and s["excluded"]["file_sha256"] == yc.sha256_file(tmp_path / "bad.json")
    rec = [json.loads(line) for line in open(_tmp_manifest)]
    assert len(rec) == 2 and all(r["rows_excluded"] == 2 and r["exclude_groups"] == "bug" for r in rec)


def test_exclude_all_ids_and_a_plain_list(tmp_path):
    _setup(tmp_path)
    s = mg.main(_args(tmp_path, "--exclude-ids", str(tmp_path / "bad.json"), "--expect-kd", "8", "--validate-only"))
    assert s["rows_excluded"] == 3 and s["kd_targets"] == 8 and s["excluded"]["groups"] == "all_ids"
    # r4 leaves; its partner r5 stays without the relation, and that is reported
    assert s["excluded"]["partners_kept_without_their_relation"] == 1 and s["relations_dropped"] == 2
    assert not (tmp_path / "out.jsonl").exists()
    (tmp_path / "list.json").write_text(json.dumps(["r9"]))
    s = mg.main(_args(tmp_path, "--exclude-ids", str(tmp_path / "list.json"), "--expect-kd", "10", "--validate-only"))
    assert s["rows_excluded"] == 1 and s["excluded"]["partners_kept_without_their_relation"] == 1
    with pytest.raises(SystemExit):  # a plain list has no groups
        mg.main(_args(tmp_path, "--exclude-ids", str(tmp_path / "list.json"), "--exclude-groups", "bug",
                      "--expect-kd", "10", "--validate-only"))


def test_expect_kd_is_required_and_is_the_count_after_the_exclusion(tmp_path):
    _setup(tmp_path)
    with pytest.raises(SystemExit):  # argparse: --expect-kd is required
        mg.main(_args(tmp_path, "--exclude-ids", str(tmp_path / "bad.json"), "--exclude-groups", "bug"))
    with pytest.raises(AssertionError, match="expect-kd 11"):  # the input file's count is wrong once rows leave
        mg.main(_args(tmp_path, "--exclude-ids", str(tmp_path / "bad.json"), "--exclude-groups", "bug",
                      "--expect-kd", "11"))
    assert not (tmp_path / "out.jsonl").exists() and not (tmp_path / "out.jsonl.tmp").exists()
    assert not (tmp_path / "out_rel.jsonl").exists()
    with pytest.raises(AssertionError, match="expect-kd-full"):
        mg.main(_args(tmp_path, "--exclude-ids", str(tmp_path / "bad.json"), "--exclude-groups", "bug",
                      "--expect-kd", "9", "--expect-kd-full", "238"))
    assert not (tmp_path / "out.jsonl").exists()
    # no exclusion: the input's count passes (the old behaviour)
    s = mg.main(_args(tmp_path, "--expect-kd", "11", "--validate-only"))
    assert s["rows_excluded"] == 0 and s["excluded"]["file"] is None


def test_exclude_refusals(tmp_path):
    _setup(tmp_path, bad={"groups": {"bug": {"ids": ["r2", "r_not_in_kd"]}}, "all_ids": ["r2", "r_not_in_kd"]})
    with pytest.raises(AssertionError, match="not in the KD file"):  # a list that does not belong to this KD file
        mg.main(_args(tmp_path, "--exclude-ids", str(tmp_path / "bad.json"), "--expect-kd", "10"))
    assert not (tmp_path / "out.jsonl").exists()
    with pytest.raises(SystemExit, match="no group"):
        mg.main(_args(tmp_path, "--exclude-ids", str(tmp_path / "bad.json"), "--exclude-groups", "nope",
                      "--expect-kd", "10"))
    with pytest.raises(SystemExit, match="needs --exclude-ids"):
        mg.main(_args(tmp_path, "--exclude-groups", "bug", "--expect-kd", "10"))
    # an excluded KD row still collides with a yn2b row of the same id
    _setup(tmp_path, yn=[dict(yn_row(2, gold=0, source="gd_gen3_x", call="y0"), meta={"latent_id": "L0"})], yrel=[])
    with pytest.raises(AssertionError, match="collision"):
        mg.main(_args(tmp_path, "--exclude-ids", str(tmp_path / "bad.json"), "--exclude-groups", "bug",
                      "--expect-kd", "9"))


def test_f4a_row_whose_base_row_is_excluded_is_refused(tmp_path):
    f4 = [dict(yn_row(f"f{i}", gold=i % 2, source="gd_gen3_polarity_ladder", call="k1"),
               meta={"latent_id": "Q0", "derived_from": "r2"}) for i in range(2)]
    _setup(tmp_path, yn=f4, yrel=[{"type": "complement", "a": "rf0", "b": "rf1"}])
    mg.main(_args(tmp_path, "--expect-kd", "11", "--validate-only"))  # base row present: fine
    with pytest.raises(AssertionError, match="base row"):
        mg.main(_args(tmp_path, "--exclude-ids", str(tmp_path / "bad.json"), "--exclude-groups", "bug",
                      "--expect-kd", "9", "--validate-only"))


def test_no_yn2b_is_the_fail_path(tmp_path):
    """--yn2b '': the plan-of-record KD file minus the A4 rows (WAVE1B 8.14 FAIL path), relations filtered the same."""
    kd, *_ = _setup(tmp_path)
    s = mg.main(["--data-dir", str(tmp_path), "--kd-file", "kd.jsonl", "--rel", "rel.jsonl", "--yn2b", "",
                 "--out", "out.jsonl", "--out-rel", "out_rel.jsonl", "--exclude-ids", str(tmp_path / "bad.json"),
                 "--exclude-groups", "bug", "--expect-kd", "9", "--no-manifest"])
    assert s["yn2b_rows"] == 0 and s["rows_out"] == 9 and s["relations_out"] == 4
    keep = [line for line in open(tmp_path / "kd.jsonl") if json.loads(line)["id"] not in {"r2", "r3"}]
    assert open(tmp_path / "out.jsonl").read() == "".join(keep)


def test_defaults_are_the_2view_file_and_the_assembled_yn2b_files(tmp_path, _tmp_manifest):
    """No --kd-file / --yn2b / --yn2b-rel: the A3 2-view file and v14_parts/yn2b_ab/ (WAVE1B 7.6)."""
    d = tmp_path / "data"
    (d / "v14_parts/yn2b_ab").mkdir(parents=True)
    _setup(d, kd_name="v14_parts/train_2b_golden_kd_2view.jsonl", yn_name="v14_parts/yn2b_ab/yn2b_train.jsonl",
           yrel_name="v14_parts/yn2b_ab/yn2b_relations.jsonl")
    (d / "rel.jsonl").rename(d / "v14_parts/golden_relations.jsonl")
    s = mg.main(["--data-dir", str(d), "--expect-kd", "11", "--no-manifest"])
    assert s["rows_out"] == 15 and s["kd_file"]["path"].endswith("v14_parts/train_2b_golden_kd_2view.jsonl")
    assert (d / "v14_parts/train_2b_golden_kd_yn2b.jsonl").exists()
    assert (d / "v14_parts/golden_relations_yn2b.jsonl").exists()
    assert not _tmp_manifest.exists()  # --no-manifest


def test_real_known_bad_list_resolves_from_lean(tmp_path, monkeypatch):
    """The documented command passes yn2b/label_audit_known_bad_ids.json relative to lean/: it resolves from any cwd.
    A4's group holds 73 ids, the whole list 85 (ids only are read)."""
    monkeypatch.chdir(tmp_path)
    p = "yn2b/label_audit_known_bad_ids.json"
    if not (yc.LEAN / p).exists():
        pytest.skip("no label_audit_known_bad_ids.json")
    assert len(mg.load_excluded(p, "gen_numeric_dates_letter_twin_question")) == 73
    assert len(mg.load_excluded(p)) == 85
    assert mg.load_excluded("") == frozenset()
