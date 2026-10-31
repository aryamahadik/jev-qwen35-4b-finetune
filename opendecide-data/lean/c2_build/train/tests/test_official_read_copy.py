"""CPU tests for official_read_copy.py (PREREG A97 (2)): the chosen candidate's H100 grid reads copied byte for byte to the
q35_4b_c2 read names after CANDIDATE_C2.json. Tiny fake trees; no Modal, no network, no OHS path.
  cd lean/c2_build/train && ../../../.venv/bin/python -B -m pytest -q tests/test_official_read_copy.py"""
import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

TRAIN = Path(__file__).resolve().parents[1]
C2B = TRAIN.parent
sys.path.insert(0, str(TRAIN))
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(TRAIN / "tests"))
import gate_c2 as gc  # noqa: E402
import gate_dev as g  # noqa: E402
import grid_plan as gp  # noqa: E402
import official_read_copy as oc  # noqa: E402
from test_grid_tools import _cand_setup, real_grid, touch  # noqa: E402,F401

SRC = "q35_4b_c2grid_last3_a08"                           # _cand_setup chooses last3_a08
SPLITS = ("dev", "pg_dev", "c2_mixdev", "pab_gproxy", "eval_jagged")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


@pytest.fixture
def world(tmp_path, real_grid):
    """_cand_setup's tree (grid, record at 1000, CANDIDATE_C2 at 3000, CHOSEN) plus the chosen candidate's read files in lean/preds_*
    (mtime 2000, before the record) and the pulled run folder of the H100 job with DONE.json for them."""
    root, lean, gpath, rec, cand, ch, ad = _cand_setup(tmp_path, real_grid)
    for sp in SPLITS:
        for suf in ("", "_perm"):
            if sp in ("pab_gproxy", "eval_jagged", "c2_mixdev") and suf:
                continue
            touch(lean / f"preds_{sp}/{SRC}{suf}.jsonl", 2000.0, f'{{"id":"{sp}{suf}","probs":{{"yes":0.5,"no":0.5}}}}\n')
            touch(lean / f"preds_{sp}/{SRC}{suf}.meta.json", 2000.0, json.dumps({"name": SRC + suf, "host": "modal", "gpu": "H100"}))
    run = tmp_path / "run" / "grid_1018_1215"
    files = {str(f.relative_to(lean)): sha(f.read_bytes()) for d in sorted(lean.glob("preds_*")) for f in d.glob(f"{SRC}*") if f.is_file()}
    (run / "models" / SRC).mkdir(parents=True)
    cd = json.loads(cand.read_text())
    (run / "models" / SRC / "DONE.json").write_text(json.dumps({"read_name": SRC, "adapter_sha256": cd["adapter_sha256"],
                                                                "files": files, "done_utc": "2026-10-18T16:13:36Z"}))
    (run / "plan.json").write_text(json.dumps({"run_id": "grid_1018_1215"}))
    (run / "session_result.json").write_text(json.dumps({"complete": True, "errors": [], "models_done": [SRC]}))
    kw = dict(root=lean, candidate=cand, chosen=ch, grid=gpath, grid_record=rec, run_dir=run)
    return lean, kw, files, run, cand


def test_plan_and_copy_are_byte_for_byte_and_after_the_candidate(world):
    lean, kw, files, run, cand = world
    plan = oc.make_plan(**kw)
    assert plan["candidate"] == "last3_a08" and plan["src"] == SRC and len(plan["files"]) == len(files)
    assert plan["job"]["run_id"] == "grid_1018_1215" and plan["candidate_check"]["status"] == "OK_BEFORE_READS"
    assert not any((lean / f["dst_rel"]).exists() for f in plan["files"])             # the plan writes nothing
    rec_p = lean / "OFFICIAL_READ_COPY_A97.json"
    rec = oc.copy(plan, lean, cand, rec_p)
    assert rec["n_files"] == len(files) and rec["predictions_changed"] is False and rec["meta_fields_changed"] == []
    assert rec["copy_unix"] > rec["candidate_written_unix"] and rec["candidate_record_sha256"] == sha(cand.read_bytes())
    for f in rec["files"]:
        s, d = lean / f["src_rel"], lean / f["dst_rel"]
        assert d.read_bytes() == s.read_bytes() and f["src_sha256"] == f["dst_sha256"] == sha(d.read_bytes())
        assert Path(f["dst_rel"]).name.startswith("q35_4b_c2.") or Path(f["dst_rel"]).name.startswith("q35_4b_c2_perm.")
        assert d.stat().st_mtime > 3000.0                                              # newer than CANDIDATE_C2.json (3000)
    assert oc.verify(lean, rec_p) == []
    assert json.loads((lean / "preds_dev/q35_4b_c2.meta.json").read_text())["name"] == SRC   # meta untouched
    # the planner's own timing check now sees the official reads as coming after the record
    assert gp.candidate_check(cand, kw["grid"], kw["grid_record"], kw["chosen"], kw["grid"].parent / "last3_a08" / "adapter_model.safetensors",
                              lean)["status"] == "OK_READS_AFTER"
    # and gate_c2's own identity check accepts the candidate with the copied reads in place
    ad = kw["grid"].parent / "last3_a08" / "adapter_model.safetensors"
    assert gc.check_candidate(cand, ad, "q35_4b_c2", lean)["name"] == "q35_4b_c2"
    with pytest.raises(oc.Refused, match="exist"):                                    # copied once
        oc.copy(plan, lean, cand, rec_p)


def test_copy_twice_and_existing_destination_refuse(world):
    lean, kw, files, run, cand = world
    plan = oc.make_plan(**kw)
    first = lean / plan["files"][0]["dst_rel"]
    first.parent.mkdir(exist_ok=True)
    first.write_text("somebody else's read")
    with pytest.raises(oc.Refused, match="exist"):
        oc.make_plan(**kw)
    with pytest.raises(oc.Refused, match="exist"):                                    # stale plan, destination appeared since
        oc.copy(plan, lean, cand, lean / "R.json")
    assert not (lean / "R.json").exists()
    for f in plan["files"][1:]:
        assert not (lean / f["dst_rel"]).exists()                                      # nothing half-placed


def test_refuses_without_the_candidate_record_or_with_a_late_or_bad_one(world):
    lean, kw, files, run, cand = world
    d = json.loads(cand.read_text())
    cand.unlink()
    with pytest.raises(oc.Refused, match="does not exist"):
        oc.make_plan(**kw)
    cand.write_text(json.dumps(d | {"name": "q35_4b_main500k"}))
    with pytest.raises(oc.Refused, match="names"):
        oc.make_plan(**kw)
    cand.write_text(json.dumps(d | {"grid_candidate": "nonsense"}))
    with pytest.raises(oc.Refused):
        oc.make_plan(**kw)
    cand.write_text(json.dumps(d | {"adapter_sha256": "1" * 64}))
    with pytest.raises(oc.Refused, match="candidate_check"):
        oc.make_plan(**kw)
    cand.write_text(json.dumps(d | {"written_unix": 1500.0}))                          # before the last grid read (2000)
    with pytest.raises(oc.Refused, match="candidate_check"):
        oc.make_plan(**kw)


def test_refuses_when_an_official_read_already_exists(world):
    lean, kw, files, run, cand = world
    touch(lean / "preds_dev/q35_4b_c2.jsonl", 2500.0)                                  # before the candidate record
    with pytest.raises(oc.Refused, match="FAIL|first official read|candidate_check"):
        oc.make_plan(**kw)


@pytest.mark.parametrize("how", ["source_changed", "source_extra", "source_missing", "done_missing", "incomplete", "errors",
                                 "model_not_done", "wrong_adapter", "wrong_read_name"])
def test_refuses_when_the_sources_do_not_match_the_job_records(world, how):
    lean, kw, files, run, cand = world
    done_p = run / "models" / SRC / "DONE.json"
    done = json.loads(done_p.read_text())
    rel = sorted(files)[0]
    if how == "source_changed":
        (lean / rel).write_text("edited")
    elif how == "source_extra":
        touch(lean / f"preds_dev/{SRC}_extra.jsonl", 2000.0)
    elif how == "source_missing":
        (lean / rel).unlink()
    elif how == "done_missing":
        done_p.unlink()
    elif how == "incomplete":
        (run / "session_result.json").write_text(json.dumps({"complete": False, "errors": [], "models_done": [SRC]}))
    elif how == "errors":
        (run / "session_result.json").write_text(json.dumps({"complete": True, "errors": ["boom"], "models_done": [SRC]}))
    elif how == "model_not_done":
        (run / "session_result.json").write_text(json.dumps({"complete": True, "errors": [], "models_done": []}))
    elif how == "wrong_adapter":
        done_p.write_text(json.dumps(done | {"adapter_sha256": "2" * 64}))
    elif how == "wrong_read_name":
        done_p.write_text(json.dumps(done | {"read_name": "q35_4b_c2grid_final_a10"}))
    with pytest.raises(oc.Refused):
        oc.make_plan(**kw)
    assert not [f for d in lean.glob("preds_*") for f in d.glob("q35_4b_c2.*")]       # nothing was placed


def test_copy_refuses_a_time_before_the_candidate_and_leaves_nothing(world):
    lean, kw, files, run, cand = world
    plan = oc.make_plan(**kw)
    with pytest.raises(oc.Refused, match="not later"):
        oc.copy(plan, lean, cand, lean / "R.json", now=2999.0)
    assert not [f for d in lean.glob("preds_*") for f in d.glob("q35_4b_c2.*")] and not (lean / "R.json").exists()


def test_a_failed_copy_check_removes_what_it_placed(world, monkeypatch):
    lean, kw, files, run, cand = world
    plan = oc.make_plan(**kw)
    real = oc.gp.sha_file
    calls = {"n": 0}

    def flaky(p):
        calls["n"] += 1
        return "0" * 64 if calls["n"] == 3 else real(p)                               # the third destination hashes wrong
    monkeypatch.setattr(oc.gp, "sha_file", flaky)
    with pytest.raises(oc.Refused, match="differs from its source"):
        oc.copy(plan, lean, cand, lean / "R.json")
    assert not [f for d in lean.glob("preds_*") for f in d.glob("q35_4b_c2.*")] and not (lean / "R.json").exists()


def test_verify_finds_a_changed_destination_or_source(world):
    lean, kw, files, run, cand = world
    rec = oc.copy(oc.make_plan(**kw), lean, cand, lean / "R.json")
    assert oc.verify(lean, lean / "R.json") == []
    d = lean / rec["files"][0]["dst_rel"]
    d.write_bytes(d.read_bytes() + b" ")
    assert any("changed" in x for x in oc.verify(lean, lean / "R.json"))


def test_the_copy_is_what_the_gate_reads_as_the_candidate(world):
    """gate_dev.fresh_sha / gate_c2.pred_files see the copied names, and the byte-identical preds give identical shas."""
    lean, kw, files, run, cand = world
    oc.copy(oc.make_plan(**kw), lean, cand, lean / "R.json")
    with gc.at_root(lean):
        a, b = g.fresh_sha("q35_4b_c2"), g.fresh_sha(SRC)
    assert {k.replace("q35_4b_c2.", "X.").replace("q35_4b_c2_perm.", "X_perm.") for k in a} >= set() and len(a) == len(b) > 0
    assert sorted(a.values()) == sorted(b.values())
    names = {p.name for p in gc.pred_files(lean, "q35_4b_c2")}
    assert names and all(n.startswith("q35_4b_c2") for n in names)
