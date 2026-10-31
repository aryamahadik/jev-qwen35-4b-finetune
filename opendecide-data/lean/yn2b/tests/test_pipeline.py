"""End to end on builder A's toy family: mv_core raw files -> assemble_yn2b -> build_ab_yn2b (arms A, B, C on a
synthetic KD file) -> merge_yn2b. Checks that the tools agree on ids, units, counts and the one-pass schedule."""
from __future__ import annotations

import json

import assemble_yn2b as asm
import build_ab_yn2b as ab
import merge_yn2b as mg
import yn2b_common as yc
from conftest import write_jsonl
from test_build_ab import CFG, _kd_rows


def test_toy_family_through_every_tool(tmp_path):
    import mv_core as mv
    import toy_family as toy
    d = tmp_path / "data"
    fb = mv.FamilyBuilder(toy.KEY, generator_file=toy.__file__, raw_dir=d / "raw", defs_dir=d / "defs",
                          manifest=tmp_path / "m.jsonl", tier_shares={"easy": 0.3, "standard": 0.4, "hard": 0.3})
    toy.build(fb, "train", 400)
    fb.write()
    res = asm.assemble(d / "raw", d / "defs")
    write_jsonl(d / "yn.jsonl", res["train"])
    write_jsonl(d / "yn_rel.jsonl", res["train_rel"])
    write_jsonl(d / "kd.jsonl", _kd_rows())
    write_jsonl(d / "rel.jsonl", [{"type": "inv", "a": "r1", "b": "r9999"}])
    (tmp_path / "cfg.json").write_text(json.dumps(CFG))
    ab.main(["--data-dir", str(d), "--arms", "A,B,C", "--kd-file", "kd.jsonl", "--rel", "rel.jsonl", "--yn2b", "yn.jsonl",
             "--yn2b-rel", "yn_rel.jsonl", "--out-dir", "ab", "--config", str(tmp_path / "cfg.json")])
    A = json.loads((d / "ab/yn2b_ab_A_counts.json").read_text())
    B = json.loads((d / "ab/yn2b_ab_B_counts.json").read_text())
    assert B["yn2b_rows"] > 0 and B["rows"] == A["rows"] + B["yn2b_rows"]
    assert B["kd_targets"] == A["kd_targets"]  # yn2b rows never carry a teacher
    assert B["replay"]["pass_batches"] > A["replay"]["pass_batches"]
    s = mg.merge(d / "kd.jsonl", d / "rel.jsonl", res["train"], res["train_rel"], d / "merged.jsonl", d / "merged_rel.jsonl",
                 expect_kd=yc.counts_kd(_kd_rows())[0])
    assert s["rows_out"] == len(_kd_rows()) + len(res["train"])
    assert s["relations_out"] == 1 + len(res["train_rel"])
