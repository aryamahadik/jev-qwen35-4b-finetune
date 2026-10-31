"""F3 decide2 (golden_src/gen3/v3_state_track.py) on the WRITTEN F3 rows (read only; skipped when absent).

- every train and dev row parses (renderer detected from the text alone), names the right machine, and shows as many
  events as meta.n_events says (meta is read here, in the test, never by the solver);
- decide2 never reads meta (answers are unchanged with meta removed);
- agreement with the program gold: on the build these tests were written against (pinned sha256), the mismatches are
  exactly the traced rows in v3.DIAGNOSIS; on any other build, agreement must stay >= 99% per part;
- the alternative readings (v3.READINGS) change only the rows the report lists.

Run:  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider yn2b/tests/test_v3_state_track_written.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
GEN3 = Path(__file__).resolve().parents[2] / "golden_src" / "gen3"
if str(GEN3) not in sys.path:
    sys.path.insert(0, str(GEN3))

import v3_state_track as v3  # noqa: E402

PINNED = {"train": "94a9c23d2103614b6ed790f391b991bf271f6d2bc377d1652197eb2b766f458a",
          "dev": "cd133970f9d82b46d92c59afb81d0caf95889d10671e738c9230471b4dc38d78"}
PATHS = {"train": v3.TRAIN_PATH, "dev": v3.DEV_PATH}
PACK = {"orders": "orders", "tickets": "tickets", "access": "access", "inventory": "inventory",
        "bookings": "bookings", "ledger": "ledger", "dialogue": "dialogue", "agent": "agent", "flags": "flags",
        "docs": "docs"}

pytestmark = pytest.mark.skipif(not all(p.exists() for p in PATHS.values()), reason="F3 rows not written")


def _rows(part):
    return [json.loads(line) for line in PATHS[part].open()]


def _pinned(part):
    return hashlib.sha256(PATHS[part].read_bytes()).hexdigest() == PINNED[part]


@pytest.fixture(scope="module")
def answers():
    out = {}
    for part in PATHS:
        for r in _rows(part):
            out[r["rid"]] = (part, r, v3.explain_row(r))
    return out


@pytest.mark.parametrize("part", ["train", "dev"])
def test_every_row_parses_and_counts_events(part):
    for r in _rows(part):
        s = v3.Solver(r)
        assert s.mach == PACK[r["meta"]["pack"]], r["rid"]
        assert len(s.doc.events) == r["meta"]["n_events"], r["rid"]


def test_no_meta_needed(answers):
    for rid, (_, r, ex) in list(answers.items())[::7]:
        bare = {"state": r["state"], "instructions": r["instructions"], "options": r["options"]}
        assert v3.explain_row(bare)["answer"] == ex["answer"], rid


@pytest.mark.parametrize("part", ["train", "dev"])
def test_agreement(answers, part):
    mism = sorted(rid for rid, (p, r, ex) in answers.items() if p == part and ex["answer"] != r["gold"])
    n = sum(1 for p, _, _ in answers.values() if p == part)
    if _pinned(part):
        known = sorted(rid for rid in v3.DIAGNOSIS if rid in {k for k, (p, _, _) in answers.items() if p == part})
        assert mism == known
    assert 1 - len(mism) / n >= 0.99, mism


def test_no_undefined(answers):
    und = [rid for rid, (_, _, ex) in answers.items() if ex["answer"] is v3.UNDEFINED]
    assert und == []


def test_mv_core_verify_labels_view():
    mv = pytest.importorskip("mv_core")
    rows = _rows("train")
    rep = mv.verify_labels(rows, v3.decide2_row)
    assert rep["undefined"] == 0
    if _pinned("train"):
        assert rep["disagree"] == len([k for k in v3.DIAGNOSIS if k.startswith("f3-tr-")])


def test_alternative_readings_are_listed():
    if not all(_pinned(p) for p in PATHS):
        pytest.skip("not the pinned build")
    sens = v3.readings_sensitivity(PATHS)
    want = {"clear_over_quarantine": (31, "primary"), "restore_not_in_trash": (1, "alt"),
            "other_booking_self": (5, "primary"), "assistant_request": (3, "alt"), "customer_proposal": (24, "primary"),
            "rehold_same_person": (26, "primary"), "revert_of_resolve": (4, "primary"),
            "same_as_before_excluded": (8, "primary"), "override_overlap": (3, "alt")}
    assert {k: (v["rows_changed"], v["gold_follows"]) for k, v in sens.items()} == want
    # every disagreement that a reading explains is in DIAGNOSIS
    for k in ("restore_not_in_trash", "assistant_request", "override_overlap"):
        assert {c["rid"] for c in sens[k]["rows"]} <= set(v3.DIAGNOSIS)
