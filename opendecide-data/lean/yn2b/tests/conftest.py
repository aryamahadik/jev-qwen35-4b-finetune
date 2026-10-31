"""Shared fixtures for the yn2b tool tests. CPU only; every test writes into pytest's tmp_path only, and the
MANIFEST_yn2b.jsonl path is redirected there (the real manifest and data/ are never written by a test).

Run:  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -m pytest -q yn2b/tests
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True  # never leave .pyc files next to frozen code (golden_src/gen, lean/)

YN2B = Path(__file__).resolve().parents[1]
LEAN = YN2B.parent
for p in (str(YN2B), str(LEAN)):
    if p not in sys.path:
        sys.path.insert(0, p)

import yn2b_common as yc  # noqa: E402


@pytest.fixture(autouse=True)
def _tmp_manifest(tmp_path, monkeypatch):
    """No test may append to the real golden_src/gen3/MANIFEST_yn2b.jsonl."""
    m = tmp_path / "MANIFEST_yn2b.jsonl"
    monkeypatch.setattr(yc, "MANIFEST", m)
    return m


def write_jsonl(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return path


def yn_row(i, gold=1, source="gd_gen_tables", teacher=None, teacher_src="q35_4b_E", call=None, role="aff", **kw):
    m = {"dataset": "x", "licence": "y"}
    if teacher is not None:
        m.update(teacher={"yes": teacher}, teacher_src=teacher_src, teacher4b={"yes": teacher})
    r = {"id": f"r{i}", "group_id": f"g{call or i}", "call_id": f"c{call or i}", "split": "train", "track": "GD",
         "source": source, "state": f"state {i}", "qtype": "noul", "instructions": f"q {i}?", "options": None,
         "gold": gold, "role": role, "card": "- yes: a\n- no: b", "meta": m}
    r.update(kw)
    return r


def ch_row(i, opts=("A", "B", "C"), gold="A", source="gd_gen_tables", teacher=None, teacher_src="q35_4b_E", call=None,
           role="choice", **kw):
    m = {"dataset": "x", "licence": "y"}
    if teacher is not None:
        m.update(teacher=dict(teacher), teacher_src=teacher_src, teacher4b=dict(teacher))
    r = {"id": f"r{i}", "group_id": f"g{call or i}", "call_id": f"c{call or i}", "split": "train", "track": "GD",
         "source": source, "state": f"state {i}", "qtype": "choice", "instructions": f"q {i}?", "options": list(opts),
         "gold": gold, "role": role, "card": None, "meta": m}
    r.update(kw)
    return r
