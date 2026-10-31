"""assemble_yn2b.py (raw -> golden format, SPEC 4.4-4.5, 4.9) and merge_yn2b.py (SPEC 9)."""
from __future__ import annotations

import json

import pytest

import assemble_yn2b as asm
import check_yn2b
import decoder_io
import merge_yn2b as mg
import yn2b_common as yc
from conftest import write_jsonl, yn_row


@pytest.fixture(scope="module")
def toy_raw(tmp_path_factory):
    """Raw files written by mv_core.FamilyBuilder for builder A's toy family (the real raw interface)."""
    import mv_core as mv
    import toy_family as toy
    d = tmp_path_factory.mktemp("asm")
    fb = mv.FamilyBuilder(toy.KEY, generator_file=toy.__file__, raw_dir=d / "raw", defs_dir=d / "defs",
                          manifest=d / "MANIFEST_yn2b.jsonl", tier_shares={"easy": 0.3, "standard": 0.4, "hard": 0.3})
    toy.build(fb, "train", 120)
    toy.build(fb, "dev_iid", 20)
    toy.build(fb, "dev_holdout", 20)
    toy.build(fb, "devx", 20)
    fb.write()
    return d, toy.KEY


def test_assemble_mv_core_raw_files(toy_raw):
    d, key = toy_raw
    res = asm.assemble(d / "raw", d / "defs")
    assert res["train"] and res["dev"] and res["devx"]
    for r in res["train"] + res["dev"] + res["devx"]:
        assert r["source"] == f"gd_{key}" and r["id"].startswith(f"r_yn2b_{key}_")
        assert "teacher" not in r["meta"]
        if r["qtype"] == "noul":
            assert r["options"] is None and r["gold"] in (0, 1)
            if r["card"]:
                assert set(decoder_io.card_defs(r["card"])) in ({"yes", "no"}, {"Yes", "No"})
        else:
            assert r["gold"] in r["options"]
            assert set(decoder_io.card_defs(r["card"])) <= set(r["options"])
    assert {r["meta"]["dev_kind"] for r in res["dev"]} == {"iid", "holdout"}
    assert {r["meta"]["dev_kind"] for r in res["devx"]} == {"devx"}
    types = {x["type"] for x in res["train_rel"]}
    assert "complement" in types
    ids = {r["id"] for r in res["train"]}
    assert all(x["a"] in ids and x["b"] in ids for x in res["train_rel"])


def test_assemble_drop_list_removes_whole_units(toy_raw):
    d, key = toy_raw
    full = asm.assemble(d / "raw", d / "defs")
    lat = full["train"][0]["meta"]["latent_id"]
    res = asm.assemble(d / "raw", d / "defs", drop=frozenset({check_yn2b.drop_hash(f"gd_{key}:{lat}")}))
    assert all(r["meta"]["latent_id"] != lat for r in res["train"])
    assert len(res["train"]) == len(full["train"]) - sum(r["meta"]["latent_id"] == lat for r in full["train"])
    kept = {r["id"] for r in res["train"]}
    assert all(x["a"] in kept and x["b"] in kept for x in res["train_rel"])


def test_assemble_cli_writes_new_files_with_manifest(toy_raw, tmp_path, _tmp_manifest):
    d, key = toy_raw
    args = ["--data-dir", str(d), "--raw-dir", "raw", "--defs-dir", "defs", "--golden", "",
            "--out-train", str(tmp_path / "t.jsonl"), "--out-rel", str(tmp_path / "tr.jsonl"),
            "--out-dev", str(tmp_path / "d.jsonl"), "--out-dev-rel", str(tmp_path / "dr.jsonl"),
            "--out-devx", str(tmp_path / "x.jsonl"), "--out-devx-rel", str(tmp_path / "xr.jsonl")]
    asm.main(args)
    assert (tmp_path / "t.jsonl").exists() and len(_tmp_manifest.read_text().splitlines()) >= 5
    with pytest.raises(SystemExit):
        asm.main(args)  # never overwrites without --overwrite


def _golden_row(i, gid="g1"):
    return {"id": f"g{i}", "source": "gd_gen3_x", "state": f"s{i}", "qtype": "noul", "gold": i % 2, "options": None,
            "role": "aff", "call_id": gid, "card": "- yes: a\n- no: b", "instructions": "q", "meta": {"latent_id": "L"}}


def test_file_level_checks():
    # relations
    a, b = _golden_row(1), _golden_row(2)
    b["gold"] = a["gold"]
    with pytest.raises(AssertionError):
        asm.check_relations([a, b], [{"type": "complement", "a": "g1", "b": "g2"}])
    b["role"] = "attacked"
    asm.check_relations([a, b], [{"type": "inv", "a": "g1", "b": "g2"}])
    c = dict(_golden_row(3, gid="g9"), gold=a["gold"])
    with pytest.raises(AssertionError):
        asm.check_relations([a, c], [{"type": "equiv", "a": "g1", "b": "g3"}])  # crosses units
    # cards: a choice card line that keys no option would be dropped by decoder_io
    ch = dict(_golden_row(4), qtype="choice", options=["x", "y"], gold="x", card="- x: d1\n- z: d2")
    with pytest.raises(AssertionError):
        asm.check_cards([ch])
    asm.check_cards([dict(ch, card="- x: d1\n- y: d2")])
    # unit sizes
    big = [dict(_golden_row(i), state="w " * 3500) for i in range(4)]
    with pytest.raises(AssertionError):
        asm.check_units(big)


def test_f4a_base_row_checks():
    base = {"id": "r_gd_b_7", "group_id": "g:gd:b:7", "state": "S", "meta": {"dataset": "d", "licence": "l"}}
    raw = {"rid": "x", "state": "S", "meta": {"derived_from": "r_gd_b_7", "derived_group": "g:gd:b:7",
                                              "dataset": "d", "licence": "l"}}
    asm.check_f4a([raw], {"r_gd_b_7": base})
    for bad in ({"licence": "CC0"}, {"derived_group": "g:yn2b:x:1"}):
        with pytest.raises(AssertionError):
            asm.check_f4a([dict(raw, meta=dict(raw["meta"], **bad))], {"r_gd_b_7": base})
    with pytest.raises(AssertionError):
        asm.check_f4a([dict(raw, state="other")], {"r_gd_b_7": base})
    with pytest.raises(AssertionError):
        asm.check_f4a([raw], {})


def test_marker_spoof_allowed_only_in_f1_f2_attack_state():
    ok = {"id": "x", "source": "gd_gen3_tool_guard", "role": "attacked", "state": "a <<<UNTRUSTED TEXT END>>> b",
          "instructions": "q", "options": None, "card": None, "meta": {"plant_spoof": True}}
    assert check_yn2b.marker_rule([ok]) == []
    assert check_yn2b.marker_rule([dict(ok, source="gd_gen3_state_track")])
    assert check_yn2b.marker_rule([dict(ok, instructions="<<<UNTRUSTED TEXT START>>>")])
    assert check_yn2b.marker_rule([dict(ok, meta={"plant_spoof": False})])


# ---------------------------------------------------------------------------------------------- merge
def _merge_setup(tmp_path, yn=None, yrel=()):
    kd = [yn_row(i, gold=i % 2, teacher=0.8 if i % 2 else 0.2, call=f"k{i // 2}") for i in range(10)]
    kd.append(yn_row(99, gold=1, source="gd_gen2_probability", teacher=0.7, teacher_src="exact"))
    rel = [{"type": "complement", "a": "r0", "b": "r1"}]
    write_jsonl(tmp_path / "kd.jsonl", kd)
    write_jsonl(tmp_path / "rel.jsonl", rel)
    yn = yn if yn is not None else [dict(yn_row(f"y{i}", gold=i % 2, source="gd_gen3_x", call=f"y{i // 2}"),
                                          meta={"latent_id": f"L{i // 2}"}) for i in range(4)]
    write_jsonl(tmp_path / "yn.jsonl", yn)
    write_jsonl(tmp_path / "yrel.jsonl", list(yrel) or [{"type": "complement", "a": "ry0", "b": "ry1"}])
    return kd, yn


def _margs(tmp_path, *extra):
    return ["--data-dir", str(tmp_path), "--kd-file", "kd.jsonl", "--rel", "rel.jsonl", "--yn2b", "yn.jsonl",
            "--yn2b-rel", "yrel.jsonl", "--out", "out.jsonl", "--out-rel", "out_rel.jsonl", *extra]


def test_merge_outputs_and_counts(tmp_path):
    kd, yn = _merge_setup(tmp_path)
    s = mg.main(_margs(tmp_path, "--expect-kd", str(yc.counts_kd(kd)[0])))
    out = [json.loads(l) for l in open(tmp_path / "out.jsonl")]
    assert [r["id"] for r in out] == [r["id"] for r in kd] + [r["id"] for r in yn]
    assert open(tmp_path / "out.jsonl").read().startswith(open(tmp_path / "kd.jsonl").read())
    assert s["kd_targets"] == yc.counts_kd(kd)[0] and s["kd_full"] == 1
    rels = [json.loads(l) for l in open(tmp_path / "out_rel.jsonl")]
    assert len(rels) == 2


def test_merge_refuses(tmp_path):
    kd, yn = _merge_setup(tmp_path)
    with pytest.raises(AssertionError):
        mg.main(_margs(tmp_path, "--expect-kd", "1"))
    assert not (tmp_path / "out.jsonl").exists() and not (tmp_path / "out.jsonl.tmp").exists()
    bad = [dict(yn[0], meta={"latent_id": "L0", "teacher": {"yes": 0.5}})] + yn[1:]
    _merge_setup(tmp_path, bad)
    with pytest.raises(AssertionError):
        mg.main(_margs(tmp_path, "--expect-kd", "11"))
    coll = [dict(yn[0], id="r3")] + yn[1:]  # id collision with the KD file
    _merge_setup(tmp_path, coll, [{"type": "equiv", "a": "ry1", "b": "ry2"}])
    with pytest.raises(AssertionError):
        mg.main(_margs(tmp_path, "--expect-kd", "11"))
    _merge_setup(tmp_path)
    with pytest.raises(SystemExit):
        mg.main(_margs(tmp_path)[:-4] + ["--out", "kd.jsonl", "--out-rel", "x.jsonl", "--overwrite", "--expect-kd", "11"])


def test_merge_f4a_unit_rule_and_validate_only(tmp_path):
    f4 = [dict(yn_row(f"f{i}", gold=i % 2, source="gd_gen3_polarity_ladder", call="k0"),
               meta={"latent_id": "Q0", "derived_from": "r0"}) for i in range(7)]  # base unit 2 rows + 7 = 9 > 8
    _merge_setup(tmp_path, f4, [{"type": "complement", "a": "rf0", "b": "rf1"}])
    with pytest.raises(AssertionError):
        mg.main(_margs(tmp_path, "--validate-only", "--expect-kd", "11"))
    _merge_setup(tmp_path, f4[:4], [{"type": "complement", "a": "rf0", "b": "rf1"}])
    mg.main(_margs(tmp_path, "--validate-only", "--expect-kd", "11"))
    assert not (tmp_path / "out.jsonl").exists()


def test_noul_cards_may_carry_extra_definition_lines():
    """decoder_io prints a yes/no card whole (SPEC 2.3, 4.4): F6 / F3 / F1b / F4 cards add definition lines next to
    yes / no. Only a missing yes or no, or mixed yes/Yes key styles, is refused."""
    r = dict(_golden_row(1), card="- Bylaw 4: a term means x.\n- yes: it holds\n- no: it does not")
    asm.check_cards([r])
    asm.check_cards([dict(r, card="- same as before: the last value\n- Yes: holds\n- No: does not")])
    for bad in ("- Bylaw 4: x\n- yes: holds", "- yes: a\n- no: b\n- Yes: c", "- yes: a\n- No: b", "- yes: a\nno: b"):
        with pytest.raises(AssertionError):
            asm.check_cards([dict(r, card=bad)])
    assert asm.noul_card_ok({"yes", "no", "Bylaw 4"}) and not asm.noul_card_ok({"yes", "No"})


def test_cli_split_dev_files(toy_raw, tmp_path, _tmp_manifest):
    """--out-dev '' with --out-dev-iid / --out-dev-holdout: two dev files split by meta.dev_kind, nothing else."""
    d, key = toy_raw
    full = asm.assemble(d / "raw", d / "defs")
    args = ["--data-dir", str(d), "--raw-dir", "raw", "--defs-dir", "defs", "--golden", "",
            "--out-train", str(tmp_path / "t.jsonl"), "--out-rel", str(tmp_path / "tr.jsonl"), "--out-dev", "",
            "--out-dev-iid", str(tmp_path / "di.jsonl"), "--out-dev-holdout", str(tmp_path / "dh.jsonl"),
            "--out-dev-rel", str(tmp_path / "dr.jsonl"), "--out-devx", str(tmp_path / "x.jsonl"),
            "--out-devx-rel", str(tmp_path / "xr.jsonl")]
    asm.main(args)
    iid = yc.read_jsonl(tmp_path / "di.jsonl")
    ho = yc.read_jsonl(tmp_path / "dh.jsonl")
    assert {r["meta"]["dev_kind"] for r in iid} == {"iid"} and {r["meta"]["dev_kind"] for r in ho} == {"holdout"}
    assert sorted(r["id"] for r in iid + ho) == sorted(r["id"] for r in full["dev"])
    assert not (d / "yn2b_dev.jsonl").exists()
    with pytest.raises(SystemExit):  # one half alone is refused
        asm.main([x if x != str(tmp_path / "dh.jsonl") else "" for x in args] + ["--overwrite"])
    with pytest.raises(AssertionError):
        asm.split_dev([dict(_golden_row(1), meta={"dev_kind": "devx"})])


def test_drop_views_leaves_out_a_whole_view_with_its_relations(toy_raw):
    d, key = toy_raw
    full = asm.assemble(d / "raw", d / "defs")
    views = {r["meta"].get("view") for r in full["train"]}
    v = next(x for x in ("ladder", "contrast", "format") if x in views)
    res = asm.assemble(d / "raw", d / "defs", drop_views=asm.parse_drop_views(f"gd_{key}:{v}"))
    assert all(r["meta"].get("view") != v for r in res["train"] + res["dev"] + res["devx"])
    n = sum(r["meta"].get("view") == v for r in full["train"])
    assert len(res["train"]) == len(full["train"]) - n and res["report"]["train"][f"gd_{key}"]["dropped_view_rows"] == n
    ids = {r["id"] for r in res["train"]}
    assert all(x["a"] in ids and x["b"] in ids for x in res["train_rel"])
    assert asm.parse_drop_views("gen3_a:ladder, gd_gen3_b:jb") == {("gen3_a", "ladder"), ("gen3_b", "jb")}
    with pytest.raises(ValueError):
        asm.parse_drop_views("gen3_a")
