"""PREREG A23: the FAM-1 step-0 record must exist and be reported; controls need not pass; no waiver is read."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import r1_check as rc  # noqa: E402


def write(tmp, **kw):
    p = tmp / "fam1_step0_c1.json"
    p.write_text(json.dumps(kw))
    return p


def test_missing_record_refuses(tmp_path):
    rep, e = rc.fam1_report(tmp_path / "fam1_step0_c1.json")
    assert rep == {"exists": False} and "missing" in e and "A23" in e


def test_failed_controls_and_flags_are_reported_not_refused(tmp_path):
    p = write(tmp_path, wall_min=63.71, controls_pass=False,
              flags=["F1: rho(X->T_old) = -0.548 < -0.2 (CI [-3.47, 2.38])", "F3: rho ...", "F5: x", "F11: y"])
    rep, e = rc.fam1_report(p)
    assert e is None
    assert rep["controls_pass"] is False and rep["valid_for_round1"] is False and rep["wall_min"] == 63.71
    assert rep["flags"] == 4 and rep["flag_families"] == ["F1", "F11", "F3", "F5"] and "invalid" in rep["a23"]


def test_passing_controls_valid(tmp_path):
    rep, e = rc.fam1_report(write(tmp_path, wall_min=10, controls_pass=True, flags=[]))
    assert e is None and rep["valid_for_round1"] is True and rep["flags"] == 0


def test_unreported_fields_refuse(tmp_path):
    rep, e = rc.fam1_report(write(tmp_path, controls_pass="?", flags=None))
    assert e and "wall_min" in e and "controls_pass" in e and "flags" in e


def test_v1_record_reported_too(tmp_path):
    p = write(tmp_path, wall_min=5, controls_pass=True, flags=[])
    (tmp_path / "fam1_step0_c1.v1_randlabel.json").write_text(json.dumps({"controls_pass": False, "wall_min": 63.7,
                                                                           "flags": ["a", "b"]}))
    rep, _ = rc.fam1_report(p)
    assert rep["v1_randlabel"] == {"controls_pass": False, "wall_min": 63.7, "flags": 2}


def test_no_fam1_waiver_keys_in_preflight_source():
    src = (HERE.parent / "r1_check.py").read_text()
    body = src.split("def extra_checks", 1)[1]
    assert '"fam1_step0" not in w' not in body and '"fam1_flags" not in w' not in body
