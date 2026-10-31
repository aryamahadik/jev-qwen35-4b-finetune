"""Checks on the written F11 carry record (data/c2_parts/F11/qc/QC_REPORT.json): the mixer's admission + binding accept it, a
stale candidates sha is refused, the cutoff is enforced. Read-only; run from lean/c2_build:
  ../../.venv/bin/python -B -m pytest -q zed_orch/carry_f11/tests"""
import copy, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / "c_build"))
import c2io, mix_c2, mixer as mx  # noqa: E402

CUT = "2026-10-20T23:59:00+00:00"
F = c2io.fam_files("F11")
FILES = {F["cand"].name: F["cand"], F["rel"].name: F["rel"]}
QC = json.loads(c2io.fam_files("F11")["qc"].read_text())


def test_admitted():
    assert QC["pass"] is True and QC["fix_iterations"] == 0
    assert mx.qc_binding(QC, FILES) == []
    assert mix_c2.admission("F11", QC, [], cutoff=CUT) == []


def test_stale_sha_refused():
    bad = copy.deepcopy(QC)
    bad["files"]["candidates_r1.jsonl"]["sha256"] = "0" * 64
    assert mx.qc_binding(bad, FILES)


def test_late_pass_refused():
    late = copy.deepcopy(QC)
    late["passed_utc"] = "2026-10-21T00:00:00+00:00"
    assert mix_c2.admission("F11", late, [], cutoff=CUT)


def test_old_wording_rows_all_dropped():
    r = QC["wording_fix_8oct"]
    assert r["old_wording_rows_NOT_dropped"] == 0 and r["rows_with_old_sem15_wording"] == r["of_which_in_round1_g13_drops"]
