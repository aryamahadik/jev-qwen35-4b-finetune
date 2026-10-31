"""Tests for families/T06/haiku/redo3/reads/build_reads.py (in memory; they read the written task files, write nothing).

  cd lean && ../.venv/bin/python -B -m pytest -q -p no:cacheprovider c2_build/families/T06/haiku/redo3/reads
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[4]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import paths  # noqa: E402

_spec = importlib.util.spec_from_file_location("t06_redo3_build_reads", HERE / "build_reads.py")
BR = importlib.util.module_from_spec(_spec)
sys.modules["t06_redo3_build_reads"] = BR
_spec.loader.exec_module(BR)

_BUILT = {}


def built() -> dict:
    if not _BUILT:
        _BUILT.update(BR.build())
    return _BUILT


def written() -> bool:
    return (HERE / "TASKS.json").is_file()


def test_every_redo3_answer_file_is_valid_and_none_is_edited():
    recs = built()["r3"]["files"]
    assert len(recs) == 5
    assert all(r["valid"] for r in recs), [r for r in recs if not r["valid"]]
    assert all(r["n_answered"] == r["n_items"] for r in recs)


def test_lint_counts_and_drops_carry_reasons():
    L = built()["lint"]["lint"]
    assert {k: len(v["kept"]) + len(v["drops"]) for k, v in L.items()} == {"packs": 10, "skins": 15, "attacks": 4,
                                                                             "wordings": 19}
    for k, v in L.items():
        assert all(d["reasons"] for d in v["drops"]), k
    assert all(d["item"] and d["task_id"] for k in L for d in L[k]["drops"])


def test_the_only_reads_are_two_independent_glex_reads_of_the_new_wordings():
    idx = built()["index"]
    assert idx["n_tasks"] == len(idx["tasks"]) == 2 <= BR.MAX_TASKS
    assert [t["read"] for t in idx["tasks"]] == ["glex-r1", "glex-r2"]
    assert all(t["kind"] == "question" for t in idx["tasks"])
    n_new = len(built()["lint"]["new_wording_forms"])
    assert n_new >= 1 and all(t["n_items"] == n_new for t in idx["tasks"])
    assert idx["counts"]["g3h_reads"] == 0


def test_reads_are_independent_own_qids_own_chunk_own_order():
    plan = built()["plan"]
    (l1, b1), (l2, b2) = plan["batches"]
    assert b1.batch_id != b2.batch_id and b1.prompt_sha != b2.prompt_sha and b1.seed != b2.seed
    assert not set(b1.key) & set(b2.key)                                    # no shared opaque id
    assert sorted(b1.key.values()) == sorted(b2.key.values())               # the same forms, read twice
    m1 = [x for x in b1.prompt.splitlines() if x.startswith("- ")]
    m2 = [x for x in b2.prompt.splitlines() if x.startswith("- ")]
    assert sorted(m1) == sorted(m2) and m1 != m2                            # the same closed list, another order
    tasks = built()["index"]["tasks"]
    assert len({t["answer_file"] for t in tasks}) == len({t["task_file"] for t in tasks}) == 2


def test_task_files_are_self_contained_and_answer_paths_are_under_reads_answers():
    for t in built()["index"]["tasks"]:
        text = built()["files"][f"tasks/{t['task_id']}.md"]
        assert t["answer_file"] in text and "/redo3/reads/answers/" in t["answer_file"]
        assert t["allowed_read"] == [t["task_file"]] and t["allowed_write"] == [t["answer_file"]]
        assert "ANSWER CONTRACT" in text and "Literal example" in text and "CLOSED LIST" in text
        chunk = json.loads(built()["files"][f"chunks/{t['task_id']}.json"])
        assert all(it["qid"] in text for it in chunk["items"])
        assert all(set(it) == {"qid", "text"} for it in chunk["items"])
        assert len(chunk["items"]) == t["n_items"]


def test_closed_list_parses_like_the_freeze_does_and_matches_the_prompt():
    from families.T06 import freeze_v2 as FZ
    for label, b in built()["plan"]["batches"]:
        t = next(x for x in built()["index"]["tasks"] if x["batch_id"] == b.batch_id)
        md = built()["files"][f"tasks/{t['task_id']}.md"]
        closed = FZ.closed_list(md)
        assert closed and all(c in b.prompt for c in closed)
        assert len(closed) == len(set(closed))
        assert FZ.answer_problems("extract_lex", [{"qid": it["qid"], "meaning": closed[0]}
                                                  for it in json.loads(built()["files"][
                                                      f"chunks/{t['task_id']}.json"])["items"]],
                                  [it["qid"] for it in json.loads(built()["files"][
                                      f"chunks/{t['task_id']}.json"])["items"]], set(closed)) == []


def test_no_internal_id_gold_or_never_open_path_reaches_a_task():
    plan = built()["plan"]
    internal = {fid for _l, b in plan["batches"] for fid in b.key.values()}
    for rel, text in built()["files"].items():
        if not rel.startswith(("tasks/", "chunks/", "prompts/")):
            continue
        assert not any(i in text for i in internal), rel
        for m in re.finditer(r"/[\w.@-]+(?:/[\w.@-]+)+", text):
            s = m.group()
            if "/redo3/reads/" in s:
                continue
            assert paths.never_open(s) is None, (rel, s)
        assert not re.search(r'"(?:gold|answer|label|key|expected)"\s*:', text), rel


def test_new_wordings_are_registered_and_unit_ok_and_the_frozen_forms_still_pass():
    reg = built()["plan"]["reg"]
    assert all(f.unit_ok for f in reg.forms.values())
    new = built()["plan"]["new"]
    assert all(reg.status(fid) == "untested" or reg.status(fid) == "pending" for fid in new)
    assert len(reg.forms) == built()["plan"]["n_frozen"] + len(new)


def test_gaps_are_closed_by_the_kept_pieces_before_glex():
    clos = built()["index"]["closing_arithmetic"]
    assert clos and all(r["closes_gap"] for r in clos), [r for r in clos if not r["closes_gap"]]


@pytest.mark.skipif(not written(), reason="read tasks not written yet")
def test_files_on_disk_equal_a_rebuild():
    assert BR.check_on_disk(HERE, built()["files"]) == []
