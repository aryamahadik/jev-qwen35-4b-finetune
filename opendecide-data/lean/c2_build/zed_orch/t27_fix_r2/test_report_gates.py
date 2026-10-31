"""report_gates.py: a gate the report does not hold is shown as 'not run' with null details, never as a passing zero (reviewer
finding: G11 `templates_over_bar` was 0 for a candidates-only run). Fabricated reports in a scratch folder; counts only.
Run from lean/c2_build: ../../.venv/bin/python -B -m pytest zed_orch/t27_fix_r2/test_report_gates.py -q -p no:cacheprovider"""
import json, shutil, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
for p in (str(C2), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)
import pytest  # noqa: E402
import report_gates as RG  # noqa: E402


def g11(over: dict, share=0.0408):
    return {"gate": "G11", "n_rows": 2401, "max_template_share": share, "templates_over_bar": over,
            "verdict": "pass" if not over else "fail", "report_3_0": {"skins_over_6_rows": 116}}


def report(gates):
    return {"gates": gates, "program_pass": False, "program_failing": ["G11"], "n_candidates": 2401, "seeds": {}}


@pytest.fixture()
def scratch():
    d = HERE / "scratch" / "t_report_gates"
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    yield d
    shutil.rmtree(d, ignore_errors=True)


def test_g11_not_evaluated_is_null_not_zero():
    rep = report({"G12": {"verdict": "pass"}})                       # a candidates-only run holds no G11 entry
    d = RG.detail(rep, "G11")
    assert d["evaluated"] is False and d["templates_over_bar"] is None and d["max_template_share"] is None
    assert d["skins_over_6_rows"] is None and "not run" in d["note"]
    assert RG.verdict(rep, "G11") is None and RG.show(RG.verdict(rep, "G11")) == "not run"


def test_g11_present_but_without_the_share_table_is_not_evaluated():
    for x in ({}, {"verdict": "skipped"}, {"templates_over_bar": None}, {"templates_over_bar": []}):
        assert RG.detail(report({"G11": x}), "G11")["templates_over_bar"] is None, x


def test_a_real_zero_stays_zero_and_a_failure_is_counted():
    d0 = RG.detail(report({"G11": g11({}, 0.0199)}), "G11")
    assert d0["evaluated"] is True and d0["templates_over_bar"] == 0 and d0["max_template_share"] == 0.0199
    d2 = RG.detail(report({"G11": g11({"a": 0.03, "b": 0.025})}), "G11")
    assert d2["evaluated"] is True and d2["templates_over_bar"] == 2 and d2["skins_over_6_rows"] == 116


def test_no_report_is_none():
    assert RG.detail(None, "G11") is None and RG.verdict(None, "G11") is None


def _cand(path, counts):
    with open(path, "w") as f:
        for (q, w), n in counts.items():
            for _ in range(n):
                f.write(json.dumps({"meta": {"qform": q, "wording_id": w}}) + "\n")


def test_candidates_file_wording_shares_are_reported_apart_from_the_gate(scratch):
    c = scratch / "cand.jsonl"
    _cand(c, {("ch_next", "w1"): 30, ("ch_next", "w2"): 30, ("yn_beyond", "w3"): 20, ("yn_beyond", "w4"): 20})
    st = RG.wording_stats([json.loads(l) for l in open(c)])
    assert st["n_rows"] == 100 and st["max_wording_share"] == 0.3 and st["wordings_over_2pct"] == 4
    old = scratch / "old.json"; new = scratch / "new.json"
    old.write_text(json.dumps(report({"G11": g11({"a": 0.03})})))
    new.write_text(json.dumps(report({"G12": {"verdict": "pass"}})))
    out = RG.build(old, new, c)
    row = out["table"]["G11"]
    assert row["before"] == "fail" and row["before_detail"]["templates_over_bar"] == 1
    assert row["after"] is None and row["after_detail"]["templates_over_bar"] is None
    assert row["after_detail"]["candidates_file_only"]["wordings_over_2pct"] == 4
    assert "not the G11 gate" in row["after_detail"]["candidates_file_only"]["note"]
    assert out["new_wordings_over_2pct_by_qform"] == {"ch_next": 2, "yn_beyond": 2}


def test_cli_prints_not_run_and_writes_json(scratch, capsys):
    old = scratch / "old.json"; new = scratch / "new.json"; o = scratch / "o.json"
    old.write_text(json.dumps(report({"G11": g11({"a": 0.03})})))
    new.write_text(json.dumps(report({"G12": {"verdict": "pass"}})))
    assert RG.main(["--old", str(old), "--new", str(new), "--cand", str(scratch / "none.jsonl"), "--out", str(o)]) == 0
    text = capsys.readouterr().out
    g11_line = next(l for l in text.splitlines() if l.startswith("G11"))
    assert "before fail" in g11_line and "after not run" in g11_line and "'templates_over_bar': None" in g11_line
    saved = json.loads(o.read_text())
    assert saved["table"]["G11"]["after"] is None and saved["table"]["G11"]["after_detail"]["templates_over_bar"] is None


def test_a_missing_new_report_leaves_every_after_empty(scratch):
    old = scratch / "old.json"
    old.write_text(json.dumps(report({"G11": g11({"a": 0.03})})))
    out = RG.build(old, scratch / "absent.json", scratch / "none.jsonl")
    assert out["new_report"] is None and all(v["after"] is None and v["after_detail"] is None for v in out["table"].values())
