"""check_unseen.py (SPEC 7.4) on a fixture tree with gate_dev's layout."""
from __future__ import annotations

import pytest

import check_unseen as cu
import gate_dev as gd
from conftest import write_jsonl

UNSEEN = {"ag_news": 2, "spam": 1}


def _tree(tmp_path, yn2b_rows):
    d = tmp_path / "data"
    splits = gd.SPLITS.split(",")
    for i, sp in enumerate(splits):
        rows = [{"id": f"{sp}_c", "group_id": f"g_{sp}", "source": "clinc150", "state": f"book a table for {i} people"}]
        if sp == "dev":
            rows += [{"id": "a1", "group_id": "ga1", "source": "ag_news",
                      "state": "the central bank raised rates by half a point on thursday in a surprise move"},
                     {"id": "a2", "group_id": "ga2", "source": "ag_news", "state": "the striker scored twice in the final"},
                     {"id": "s1", "group_id": "gs1", "source": "spam", "state": "win a free cruise now by replying yes"}]
        write_jsonl(d / f"{sp}.jsonl", rows)
    for f in gd.TRAIN_FILES:
        write_jsonl(d / f"{f}.jsonl", [{"id": "t", "source": "clinc150", "state": "reserve a table"}] if "golden" in f else [])
    write_jsonl(d / "v14_parts/yn2b_train.jsonl", yn2b_rows)
    return tmp_path


@pytest.fixture()
def patched(monkeypatch):
    monkeypatch.setattr(gd, "UNSEEN_FROZEN_ROWS", dict(UNSEEN))
    monkeypatch.setattr(cu, "N_SOURCES", 2)
    monkeypatch.setattr(cu, "N_ROWS", 3)
    monkeypatch.setattr(gd, "ROOT", gd.ROOT)  # restored after the test (check() may set it)


def _files(root):
    return sorted(p for p in root.rglob("*") if p.is_file())


def test_pass_and_writes_nothing(tmp_path, patched):
    root = _tree(tmp_path, [{"id": "y1", "source": "gd_gen3_tool_guard", "state": "may the transfer run"}])
    before = _files(root)
    res = cu.check("v14_parts/yn2b_train", root)
    assert res["problems"] == [] and res["unseen_rows"] == 3
    assert _files(root) == before
    assert not (root / gd.UNSEEN_FROZEN).exists()


def test_text_overlap_and_name_clash_fail(tmp_path, patched):
    root = _tree(tmp_path, [{"id": "y1", "source": "gd_gen3_tool_guard",
                             "state": "note: the central bank raised rates by half a point on thursday in a surprise move"}])
    res = cu.check("v14_parts/yn2b_train", root)
    assert any("text guard" in p for p in res["problems"])
    root = _tree(tmp_path, [{"id": "y1", "source": "gd_gen3_spam", "state": "fine"}])
    res = cu.check("v14_parts/yn2b_train", root)
    assert any("differs from UNSEEN_FROZEN_ROWS" in p for p in res["problems"])


def test_missing_file_is_a_failure(tmp_path, patched):
    root = _tree(tmp_path, [])
    res = cu.check("v14_parts/does_not_exist", root)
    assert res["problems"] and "missing" in res["problems"][0]
