"""One small in-memory harness run (generator stand-in, two seeds), the pipeline wiring, and a mutation canary proving the harness would catch a broken B."""
import collections

import pytest

from T65 import checked, dryrun
from T65.solver_b import agree, hook
from T65.solver_b import rules as R


def test_small_harness_run_agrees_with_gold():
    stats, classes, reasons, total, rejects = agree.run(260, [31, 32])
    allg = stats["ALL"]
    assert allg["rows"] >= 400
    assert allg["disagree"] == 0 and allg["abstain"] == 0 and allg["error"] == 0 and allg["letter_mismatch"] == 0
    subs = {k for k in stats if k.startswith("sub:CWEC")}
    assert len(subs) == 9 and any(k.startswith("head:CWE") for k in stats)
    assert allg["agree"] == allg["rows"]


def test_pipeline_wiring_accepts_solver_b():
    ad = checked.adapter(solver_b=hook.solver_b)
    assert ad.solver_b is hook.solver_b
    rows, summary, log, report = dryrun.dry_rows(60, seed=3, solver_b=hook.solver_b)
    assert rows and not summary["dropped"] and "solver_b_absent" not in summary["notes"]


def test_mutation_canary_harness_detects_a_broken_neutraliser_table(monkeypatch):
    broken = dict(R.NEUTRALISER_CALLS)
    del broken["html.escape"]
    monkeypatch.setattr(R, "NEUTRALISER_CALLS", broken)
    stats, classes, reasons, total, rejects = agree.run(260, [31])
    assert stats["ALL"]["disagree"] + stats["ALL"]["abstain"] > 0


def test_mutation_canary_wrong_class_credit(monkeypatch):
    monkeypatch.setattr(R, "NEUTRALISER_CALLS", dict(R.NEUTRALISER_CALLS, **{"html.escape": "CWEC-22"}))
    stats, classes, reasons, total, rejects = agree.run(260, [31])
    assert stats["ALL"]["disagree"] > 0
