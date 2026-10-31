"""Tests for gate_c2.py (the C2 dev pre-gate, spec 7.2). In memory: synthetic prediction rows and records; the only
files written are small JSON records (monitor state, look log) in a temp folder. No OHS path is ever opened: the
refusal tests check that nothing is read. Run from lean/:
  ../.venv/bin/python -m pytest -q c2_build/tests/test_gate_c2.py
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
import gate_c2 as gc  # noqa: E402
import gate_dev as g  # noqa: E402
from c2_kit import paths as kp  # noqa: E402


@pytest.fixture
def tmp(tmp_path):
    assert gc.c2io.refusal(tmp_path) is None             # never a session / never-open folder
    return tmp_path


def rows_with(n, acc_c, acc_r, seed=0, qtype="choice", family="T28", groups=None):
    """n prediction rows (gate_dev form) with the given accuracies (fractions), one group per row unless `groups`."""
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        oc, orr = float(rnd.random() < acc_c), float(rnd.random() < acc_r)
        out.append({"split": "s", "id": f"r{i}", "group_id": f"g{i if groups is None else i % groups}",
                    "source": "x", "qtype": qtype, "gold": "a", "options": ["a", "b"], "family": family,
                    "ok_c": oc, "ok_r": orr, "p_c": {"a": 0.9 if oc else 0.1, "b": 0.1 if oc else 0.9},
                    "p_r": {"a": 0.9 if orr else 0.1, "b": 0.1 if orr else 0.9}})
    return out


def dev_json(**over):
    d = {"mode": "ship", "cand": gc.CAND, "ref": gc.REF, "splits": gc.SPLITS9, "size": "4b",
         "full": {"n": 7056, "diff": -0.3, "lo": -1.0, "hi": 0.4},
         "types": {"noul": {"cand": 80.0, "ref": 80.5, "diff": -0.5, "n": 3000},
                   "choice": {"cand": 75.0, "ref": 75.2, "diff": -0.2, "n": 4000}},
         "calibration": {"cand": {"noul": {"brier_cal": 0.110}}, "ref": {"noul": {"brier_cal": 0.108}}},
         "equiv_flip": {"cand": 6.0, "ref": 5.0, "n": 722}, "perm_flip": {"cand": 3.0, "ref": 2.5, "n": 7056},
         "asr": {"jagged": {"cand": 0.01, "ref": 0.0, "lo": -0.01, "veto": False},
                 "opi": {"cand": 0.02, "ref": 0.013, "lo": -0.01, "veto": False}},
         "unmeasured": [], "pipeline_issues": [], "not_final": [],
         "report": {"per_split": {"hard_dev": {"n": 72, "diff": 5.0}, "pg_dev": {"n": 206, "diff": 7.0}}}}
    d.update(over)
    return d


D2 = {"n": 3847, "groups": 3000, "cand": 80.0, "ref": 80.4, "diff": -0.4, "lo": -1.2, "hi": 0.4}
LAT = {"cand_p50_ms": 99.0, "ref_p50_ms": 98.0, "served_path": "sglang_s1"}


def by_id(r):
    return r["id"]


def write_mix_manifest(root, by_block):
    """A written mix manifest (mix_c2.write_outputs: counts.by_block) under <root>/data/c2_parts/."""
    d = Path(root) / "data" / "c2_parts"
    d.mkdir(parents=True, exist_ok=True)
    (d / "c2_mix_manifest.json").write_text(json.dumps({"counts": {"by_block": by_block}}))
    return d / "c2_mix_manifest.json"


def t37(n=200, viol_c=0.05, viol_r=0.15):
    rows, rels = [], []
    for i in range(n):
        a, b = f"a{i}", f"b{i}"
        pa = 0.8
        rows.append({"id": a, "group_id": f"g{i}", "qtype": "noul", "p_c": {"yes": pa}, "p_r": {"yes": pa}})
        rows.append({"id": b, "group_id": f"g{i}", "qtype": "noul", "p_c": {"yes": 1 - pa + viol_c},
                     "p_r": {"yes": 1 - pa + viol_r}})
        rels.append({"a": a, "b": b, "type": "complement"})
    return rows, rels


# ---- refusals ---------------------------------------------------------------------------------------------------------
def test_refuses_ohs_paths_and_names_before_reading():
    sealed = kp.LEAN / "ohs4_sealed" / "suite.json"
    for p in (sealed, kp.LEAN / "data/ohs3_parts/x.jsonl", kp.LEAN / "sealed_nd/score_nd.py"):
        with pytest.raises(gc.Refused):
            gc.refuse_inputs([p])
    for n in ("ohs4_r", "OHS4", "preds_jev"):
        with pytest.raises(gc.Refused):
            gc.refuse_inputs(names=[n])
    gc.refuse_inputs([kp.LEAN / "logs/ship_c2.json"], ["c2_mixdev", gc.CAND])
    with pytest.raises(gc.Refused):
        gc.jload(sealed, "x")
    with pytest.raises(gc.Refused):
        gc.split_rows("ohs4_r", gc.CAND, gc.REF, kp.LEAN)


def test_main_refuses_an_ohs4_input_with_exit_2(capsys):
    rc = gc.main(["pregate", "--dev", str(kp.LEAN / "ohs4_sealed" / "look.json"), "--no-log"])
    out = capsys.readouterr().out
    assert rc == 2 and out.startswith("REFUSED") and "never reads OHS-4" in out
    rc = gc.main(["pregate", "--cand", "ohs4_model", "--no-log"])
    assert rc == 2


# ---- the bootstrap ----------------------------------------------------------------------------------------------------
def test_bootstrap_is_gate_dev_group_boot_10000_seed0(monkeypatch):
    seen = {}

    def spy(rows, boots=None, seed=None):
        seen.update(boots=boots, seed=seed)
        return {"n": len(rows)}
    monkeypatch.setattr(g, "group_boot", spy)
    gc.boot([{"x": 1}])
    assert seen == {"boots": 10000, "seed": 0} and gc.DEV_BOOT == {"resamples": 10000, "seed": 0}


def test_paired_mean_boot_matches_group_boot_on_accuracy():
    rows = rows_with(400, 0.8, 0.7, seed=3, groups=150)
    a = g.group_boot(rows, boots=2000, seed=0)
    b = gc.paired_mean_boot([(x["group_id"], x["ok_c"], x["ok_r"]) for x in rows], boots=2000, seed=0)
    for k in ("diff", "lo", "hi"):
        assert abs(a[k] - 100 * b[k]) < 1e-9
    assert b["n"] == 400 and b["groups"] == 150 and gc.paired_mean_boot([])["n"] == 0


# ---- the rules --------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("diff,lo,ok", [(8.0, 0.1, True), (7.99, 1.0, False), (12.0, 0.0, False), (12.0, -0.5, False)])
def test_learning_rule(diff, lo, ok):
    r = gc.gain_rule("a", "learning", {"n": 2550, "groups": 2000, "cand": 80, "ref": 80 - diff, "diff": diff, "lo": lo,
                                       "hi": diff + 2}, gc.A_MIN, gc.A_LB)
    assert (r["status"] == "PASS") is ok
    assert gc.gain_rule("b", "t", {"n": 0}, 3.0, 0.0)["status"] == "UNMEASURED"


@pytest.mark.parametrize("diff,lo,ok", [(3.0, 0.01, True), (2.99, 1.0, False), (5.0, 0.0, False)])
def test_transfer_rule(diff, lo, ok):
    r = gc.gain_rule("b", "transfer", {"n": 1200, "groups": 1200, "cand": 70, "ref": 70 - diff, "diff": diff, "lo": lo,
                                       "hi": diff + 3}, gc.B_MIN, gc.B_LB)
    assert (r["status"] == "PASS") is ok


def status(rules, rid):
    return next(r["status"] for r in rules if r["id"] == rid)


def test_dev_guards_pass_and_each_boundary():
    rules = gc.dev_guards(dev_json(), D2)
    assert all(r["status"] == "PASS" for r in rules) and len(rules) == 9
    assert status(gc.dev_guards(dev_json(full={"n": 1, "diff": 0, "lo": -1.5, "hi": 1}), D2), "c1") == "FAIL"
    assert status(gc.dev_guards(dev_json(full={"n": 1, "diff": 0, "lo": -1.49, "hi": 1}), D2), "c1") == "PASS"
    assert status(gc.dev_guards(dev_json(), D2 | {"diff": -1.01, "hi": -0.01}), "c2") == "FAIL"
    assert status(gc.dev_guards(dev_json(), D2 | {"diff": -1.01, "hi": 0.0}), "c2") == "PASS"     # UB not < 0
    assert status(gc.dev_guards(dev_json(), D2 | {"diff": -0.99, "hi": -0.1}), "c2") == "PASS"    # point >= -1
    t = dev_json()["types"]
    assert status(gc.dev_guards(dev_json(types=t | {"noul": t["noul"] | {"diff": -1.01}}), D2), "c3.yes/no") == "FAIL"
    assert status(gc.dev_guards(dev_json(types=t | {"choice": t["choice"] | {"diff": -1.0}}), D2), "c3.choice") == "PASS"
    cal = {"cand": {"noul": {"brier_cal": 0.1131}}, "ref": {"noul": {"brier_cal": 0.108}}}
    assert status(gc.dev_guards(dev_json(calibration=cal), D2), "c4") == "FAIL"
    cal["cand"]["noul"]["brier_cal"] = 0.113
    assert status(gc.dev_guards(dev_json(calibration=cal), D2), "c4") == "PASS"
    assert status(gc.dev_guards(dev_json(equiv_flip={"cand": 7.01, "ref": 5.0, "n": 9}), D2), "c5.equiv") == "FAIL"
    assert status(gc.dev_guards(dev_json(perm_flip={"cand": 4.5, "ref": 2.5, "n": 9}), D2), "c5.perm") == "PASS"
    assert status(gc.dev_guards(dev_json(perm_flip=None), D2), "c5.perm") == "UNMEASURED"
    asr = dev_json()["asr"]
    veto = asr | {"jagged": {"cand": 0.031, "ref": 0.0, "lo": 0.001, "veto": True}}
    assert status(gc.dev_guards(dev_json(asr=veto), D2), "c6.jagged") == "FAIL"
    noveto = asr | {"jagged": {"cand": 0.031, "ref": 0.0, "lo": 0.0, "veto": False}}             # LB not > 0
    assert status(gc.dev_guards(dev_json(asr=noveto), D2), "c6.jagged") == "PASS"
    cap = asr | {"opi": {"cand": 0.033, "ref": 0.013, "lo": 0.01, "veto": False}}                 # = C1 + 2 pp
    assert status(gc.dev_guards(dev_json(asr=cap), D2), "c6.opi") == "PASS"
    with pytest.raises(gc.Refused, match="disagrees"):
        gc.dev_guards(dev_json(asr=asr | {"opi": {"cand": 0.2, "ref": 0.0, "lo": 0.1, "veto": False}}), D2)


def test_latency_rule():
    assert gc.latency_rule({"cand_p50_ms": 105.0, "ref_p50_ms": 100.0, "served_path": "s1"})["status"] == "PASS"
    assert gc.latency_rule({"cand_p50_ms": 105.1, "ref_p50_ms": 100.0, "served_path": "s1"})["status"] == "FAIL"
    with pytest.raises(gc.Refused, match="one served path"):
        gc.latency_rule({"cand_p50_ms": 1.0, "ref_p50_ms": 1.0, "cand_path": "s1", "ref_path": "hf"})
    with pytest.raises(gc.Refused, match="missing"):
        gc.latency_rule({"cand_p50_ms": 1.0, "served_path": "s1"})


def test_complement_violation_rule_and_paired_ci():
    rows, rels = t37()
    s = gc.complement_stats(rows, rels)
    assert s["n"] == 200 and abs(s["cand"] - 0.05) < 1e-9 and abs(s["ref"] - 0.15) < 1e-9
    assert abs(s["diff"] + 0.1) < 1e-9 and s["lo"] <= s["diff"] <= s["hi"]
    assert gc.complement_rule(s)["status"] == "PASS"
    same = gc.complement_stats(*t37(viol_c=0.15))
    assert gc.complement_rule(same)["status"] == "FAIL"                          # equal is not better: C2 < C1
    rels.append({"a": "a0", "b": "b1", "type": "equiv"})                         # other relation types are ignored
    assert gc.complement_stats(rows, rels)["n"] == 200
    assert gc.complement_rule(gc.complement_stats([], []))["status"] == "UNMEASURED"


def test_report_only_helpers():
    rows = rows_with(100, 0.9, 0.5, seed=1)
    for x in rows[:40]:
        x["options"] = ["a", "ask the user first"]
        x["p_c"] = {"a": 0.8, "ask the user first": 0.2}
        x["p_r"] = {"a": 0.3, "ask the user first": 0.7}
    oa = gc.over_ask(rows)
    assert oa["rows"] == 40 and oa["cand"] == 0.0 and oa["ref"] == 1.0
    yn = [{"qtype": "noul", "p_c": {"yes": 0.95}, "p_r": {"yes": 0.6}, "ok_c": 1.0, "ok_r": 0.0} for _ in range(10)]
    assert abs(gc.ece(yn, "c") - 0.05) < 1e-9 and abs(gc.ece(yn, "r") - 0.6) < 1e-9 and gc.ece(rows, "c") is None
    fam = gc.per_family(rows_with(50, 0.9, 0.5, family="T36") + rows_with(50, 0.6, 0.6, family="T19"))
    assert set(fam) == {"T19", "T36"}


def test_evaluate_pass_and_fail_decisions():
    mix = rows_with(2550, 0.85, 0.70, seed=1)
    tr = rows_with(1200, 0.70, 0.60, seed=2, family="T36")
    rows, rels = t37()
    res = gc.evaluate(dev_json(), D2, mix, tr, rows, rels, LAT)
    assert res["pass"] and res["decision"].startswith("PRE-GATE PASS") and res["bootstrap"] == gc.DEV_BOOT
    assert [r["id"] for r in res["rules"]][:2] == ["a", "b"] and res["rules"][-1]["id"] == "d"
    assert res["report_only"]["hard_dev_pg_dev"]["pg_dev"]["diff"] == 7.0
    weak = gc.evaluate(dev_json(), D2, rows_with(2550, 0.75, 0.70, seed=1), tr, rows, rels, LAT)
    assert not weak["pass"] and weak["decision"].startswith("PRE-GATE FAIL (a)")       # +5 pp < +8: learning fails
    assert "no C2 look on OHS-4" in weak["decision"] and "C1 vs Jev only" in weak["decision"]
    slow = gc.evaluate(dev_json(), D2, mix, tr, rows, rels, LAT | {"cand_p50_ms": 120.0})
    assert not slow["pass"] and "c7" in slow["decision"]


# ---- identity / run checks -----------------------------------------------------------------------------------------
def test_check_dev_accepts_only_the_refparity_note():
    note = (f"the last refparity look of {gc.REF} was against {gc.STORED_C1} (4b), not the 4B stored REF "
            "q35_4b_pxE_parity")
    gc.check_dev(dev_json(not_final=[note]), gc.CAND, gc.REF)
    gc.check_dev(dev_json(not_final=[f"no refparity look logged for REF {gc.REF} (python ...)"]), gc.CAND, gc.REF)
    other = note.replace(gc.STORED_C1, "q35_4b_main500k_pre")
    with pytest.raises(gc.Refused, match="NOT FINAL"):
        gc.check_dev(dev_json(not_final=[other]), gc.CAND, gc.REF)
    with pytest.raises(gc.Refused, match="missing reads"):
        gc.check_dev(dev_json(perm_flip=None), gc.CAND, gc.REF)
    with pytest.raises(gc.Refused, match="compares"):
        gc.check_dev(dev_json(cand="q35_4b_c_r1"), gc.CAND, gc.REF)
    with pytest.raises(gc.Refused, match="9 pre-registered"):
        gc.check_dev(dev_json(splits=gc.SPLITS9 + ["ohs4_r"]), gc.CAND, gc.REF)
    with pytest.raises(gc.Refused, match="pipeline"):
        gc.check_dev(dev_json(pipeline_issues=["two jobs"]), gc.CAND, gc.REF)


def test_stop_rule_and_monitor_state(tmp):
    st, stop, esc = tmp / "state.json", tmp / "stop.json", tmp / "esc.json"
    with pytest.raises(gc.Refused, match="never checked"):
        gc.check_stop_rule(st, stop, esc, gc.CAND)
    ok = {"acc_diff_pp": -0.5, "pyes_drift": 0.0}
    st.write_text(json.dumps({"name": gc.CAND, "reads": {"0.25": ok, "0.5": ok}}))
    with pytest.raises(gc.Refused, match="missing"):
        gc.check_stop_rule(st, stop, esc, gc.CAND)
    st.write_text(json.dumps({"name": gc.CAND, "reads": {f: ok for f in ("0.25", "0.5", "0.75")}}))
    assert gc.check_stop_rule(st, stop, esc, gc.CAND)["reads"] == ["0.25", "0.5", "0.75"]
    low = {"acc_diff_pp": -1.6, "pyes_drift": 0.0}
    st.write_text(json.dumps({"name": gc.CAND, "reads": {"0.25": low, "0.5": low, "0.75": ok}}))
    with pytest.raises(gc.Refused, match="fired"):
        gc.check_stop_rule(st, stop, esc, gc.CAND)
    st.write_text(json.dumps({"name": "q35_4b_c_r1", "reads": {}}))
    with pytest.raises(gc.Refused, match="belongs"):
        gc.check_stop_rule(st, stop, esc, gc.CAND)
    stop.write_text("{}")
    with pytest.raises(gc.Refused, match="stopped run"):
        gc.check_stop_rule(st, stop, esc, gc.CAND)


def test_one_pregate_per_candidate(tmp):
    looks = tmp / "looks.jsonl"
    assert gc.guard_repeat(looks, "a" * 64, "x") is None
    looks.write_text(json.dumps({"cand_sha256": "a" * 64, "inputs_sha256": "x", "decision": "PRE-GATE FAIL"}) + "\n")
    assert gc.guard_repeat(looks, "a" * 64, "x")["decision"] == "PRE-GATE FAIL"
    with pytest.raises(gc.Refused, match="other inputs"):
        gc.guard_repeat(looks, "a" * 64, "y")
    assert gc.guard_repeat(looks, "b" * 64, "y") is None


def test_d2_rows_and_d2_set_refusals(tmp):
    rows = [{"source": "ag_news"}] * 3 + [{"source": "spam"}] * 2 + [{"source": "seen"}]
    assert len(gc.d2_rows(rows, {"ag_news": 3, "spam": 2})) == 5
    with pytest.raises(gc.Refused, match="changed"):
        gc.d2_rows(rows, {"ag_news": 4, "spam": 2})
    with pytest.raises(gc.Refused, match="c2_parts/c2_train"):
        gc.d2_set(list(g.TRAIN_FILES), tmp / "d2.json")
    with pytest.raises(gc.Refused):
        gc.d2_set(list(g.TRAIN_FILES) + [gc.C2_TRAIN], kp.LEAN / "ohs4_sealed" / "d2.json")
    assert not (tmp / "d2.json").exists()


def test_null_numbers_from_gate_dev_json_are_unmeasured_never_pass():
    # gate_dev's --json writes NaN as null: such a check is UNMEASURED (pregate then refuses), never a pass or a crash
    asr = dev_json()["asr"] | {"opi": {"cand": None, "ref": 0.01, "lo": None, "veto": False}}
    t = dev_json()["types"]
    rules = gc.dev_guards(dev_json(asr=asr, types=t | {"choice": t["choice"] | {"diff": None}},
                                   full={"n": 0, "diff": None, "lo": None, "hi": None},
                                   calibration={"cand": {}, "ref": {}}), D2 | {"diff": None})
    for rid in ("c1", "c2", "c3.choice", "c4", "c6.opi"):
        assert status(rules, rid) == "UNMEASURED", rid
    assert status(rules, "c3.yes/no") == "PASS" and status(rules, "c6.jagged") == "PASS"


def test_pregate_cli_flow_logs_once_and_repeats(tmp, monkeypatch, capsys):
    """pregate end to end with the reads faked in memory: decision printed, result + look written once, a repeat with
    the same inputs is not logged again, other inputs are refused."""
    mix = rows_with(2550, 0.85, 0.70, seed=1)
    tr = rows_with(1200, 0.70, 0.60, seed=2, family="T36")
    t37_rows, t37_rels = t37()
    dev_rows = rows_with(400, 0.8, 0.8, seed=4)
    for i, x in enumerate(dev_rows):
        x["source"] = "ag_news" if i < 100 else "seen"
    monkeypatch.setattr(gc, "check_candidate", lambda rec, ad, name, root: {"adapter_sha256": "c" * 64})
    monkeypatch.setattr(gc, "check_stop_rule", lambda *a: {"reads": ["0.25", "0.5", "0.75"]})
    monkeypatch.setattr(gc, "check_refparity", lambda root, ref, stored=gc.STORED_C1: {"agree": 99.9})
    monkeypatch.setattr(gc, "load_d2_set", lambda p, root, cand: {"sources": {"ag_news": 100}, "sources_sha256": "d"})
    monkeypatch.setattr(g, "complete_rows", lambda splits, cand, ref: dev_rows)
    monkeypatch.setattr(gc, "split_rows", lambda split, cand, ref, root: {gc.MIXDEV: mix, gc.TRANSFER: tr,
                                                                           gc.T37B_DEV: t37_rows}[split])
    monkeypatch.setattr(gc, "relations", lambda split, root: t37_rels)
    (tmp / "dev.json").write_text(json.dumps(dev_json()))
    (tmp / "lat.json").write_text(json.dumps(LAT))
    write_mix_manifest(tmp, {"T28": 100, "T01": 50, "replay": 150})                 # A80 (c): the trained families come from the written mix manifest
    argv = ["pregate", "--dev", str(tmp / "dev.json"), "--latency", str(tmp / "lat.json"), "--looks",
            str(tmp / "looks.jsonl"), "--out-dir", str(tmp), "--root", str(tmp)]
    assert gc.main(argv) == 0
    out = capsys.readouterr().out
    assert "PRE-GATE PASS" in out and "c6.opi" in out
    res = json.loads((tmp / f"gate_c2_pregate_{gc.CAND}.json").read_text())
    assert res["pass"] and res["report_only"]["ece_dev_yes_no"]["cand"] is None and res["bootstrap"] == gc.DEV_BOOT
    assert len((tmp / "looks.jsonl").read_text().splitlines()) == 1
    assert gc.main(argv) == 0 and len((tmp / "looks.jsonl").read_text().splitlines()) == 1     # same inputs: no new look
    (tmp / "lat.json").write_text(json.dumps(LAT | {"cand_p50_ms": 97.0}))
    assert gc.main(argv) == 2 and "other inputs" in capsys.readouterr().out


def test_pregate_refuses_reads_from_another_job(tmp, monkeypatch, capsys):
    seen = {}

    def pc(names, reads):
        seen["labels"] = [r[0] for r in reads]
        return ["gpu is not one value over the reads: H100 in q35_4b_c2 [c2_mixdev]; L4 in ..."], {}
    monkeypatch.setattr(gc, "check_candidate", lambda rec, ad, name, root: {"adapter_sha256": "c" * 64})
    monkeypatch.setattr(gc, "check_stop_rule", lambda *a: {})
    monkeypatch.setattr(gc, "check_refparity", lambda root, ref, stored=gc.STORED_C1: {})
    monkeypatch.setattr(gc, "load_d2_set", lambda p, root, cand: {"sources": {}, "sources_sha256": "d"})
    monkeypatch.setattr(g, "complete_rows", lambda splits, cand, ref: [])
    monkeypatch.setattr(g, "pipeline_check", pc)
    (tmp / "dev.json").write_text(json.dumps(dev_json()))
    rc = gc.main(["pregate", "--dev", str(tmp / "dev.json"), "--root", str(tmp), "--no-log"])
    assert rc == 2 and "one clean predict job" in capsys.readouterr().out
    assert {"c2_mixdev", "c2_transfer_dev", "c2_t37b_dev", "eval_jagged", "dev"} <= set(seen["labels"])


# ---- A80 (c): the pre-gate (a) reads only the families the final mix trained on ---------------------------------------------
def mixdev_with_untrained(n_trained=600, n_off=150):
    """Mixdev rows: T28 learns strongly (+20 pp); T33 / T12 / T24 are not trained and C2 is worse than C1 on them."""
    good = rows_with(n_trained, 0.90, 0.70, seed=1, family="T28")
    off = []
    for k, fam in enumerate(("T33", "T12", "T24")):
        rr = rows_with(n_off, 0.40, 0.75, seed=10 + k, family=fam)
        for x in rr:
            x["id"] = f"{fam}_{x['id']}"
            x["group_id"] = f"{fam}_{x['group_id']}"
        off += rr
    return good, off


def test_trained_families_come_from_the_mix_manifest_and_replay_is_not_one(tmp):
    p = write_mix_manifest(tmp, {"T28": 2247, "T01": 1600, "replay": 9000, "RTW": 5, "T33": 0})
    tf = gc.trained_families(p)
    assert tf["trained"] == ["RTW", "T01", "T28"] and len(tf["manifest_sha256"]) == 64          # a block with 0 rows and 'replay' are not trained families
    with pytest.raises(gc.Refused, match="missing or not JSON"):
        gc.trained_families(tmp / "nope.json")
    (tmp / "empty.json").write_text(json.dumps({"counts": {}}))
    with pytest.raises(gc.Refused, match="no counts.by_block"):
        gc.trained_families(tmp / "empty.json")
    (tmp / "norows.json").write_text(json.dumps({"counts": {"by_block": {"replay": 10, "T28": 0}}}))
    with pytest.raises(gc.Refused, match="no block with rows"):
        gc.trained_families(tmp / "norows.json")


def test_split_trained_is_in_memory_and_keeps_every_row():
    good, off = mixdev_with_untrained()
    allrows = good + off
    snap = json.dumps(allrows, sort_keys=True)
    a, b = gc.split_trained(allrows, {"T28"})
    assert len(a) == len(good) and len(b) == len(off) and {x["family"] for x in b} == {"T33", "T12", "T24"}
    assert json.dumps(allrows, sort_keys=True) == snap                                      # nothing edited
    nofam = [dict(good[0], family=None)]
    assert gc.split_trained(nofam, {"T28"}) == ([], nofam)                                 # a row without a family is never a gate row


def test_evaluate_scores_untrained_families_report_only_and_the_gate_reads_trained_rows():
    good, off = mixdev_with_untrained()
    mix = good + off
    tr = rows_with(1200, 0.70, 0.60, seed=2, family="T36")
    rows, rels = t37()
    old = gc.evaluate(dev_json(), D2, mix, tr, rows, rels, LAT)                              # the pre-A80 reading: every family counts
    assert not old["pass"] and old["decision"].startswith("PRE-GATE FAIL (a)")
    new = gc.evaluate(dev_json(), D2, mix, tr, rows, rels, LAT, trained={"T28"})
    assert new["pass"] and new["mixdev"]["n"] == len(good)                                    # (a) = the T28 rows only
    fam = new["report_only"]["held_out_families"]["mixdev"]
    assert fam["T28"]["trained_in_c2"] is True and fam["T28"]["role"] == "pre-gate (a) input"
    for f in ("T33", "T12", "T24"):
        assert fam[f]["trained_in_c2"] is False and fam[f]["role"] == "report-only: family not trained in C2"
        assert fam[f]["diff"] < 0                                                            # still scored (report-only)
    a80 = new["report_only"]["mixdev_trained_families"]
    assert a80["trained"] == ["T28"] and a80["gate_rows"] == len(good) and a80["report_only_rows"] == len(off)
    assert a80["report_only_families"] == ["T12", "T24", "T33"] and a80["label"] == "family not trained in C2"
    assert a80["all_families_mixdev_report_only"]["n"] == len(good) + len(off)               # the whole-file number is reported, never gated
    assert len(mix) == len(good) + len(off)                                                  # no row removed from the input list


def test_all_mixdev_families_trained_equals_the_old_reading():
    good, off = mixdev_with_untrained()
    mix = good + off
    tr = rows_with(1200, 0.70, 0.60, seed=2, family="T36")
    rows, rels = t37()
    old = gc.evaluate(dev_json(), D2, mix, tr, rows, rels, LAT)
    same = gc.evaluate(dev_json(), D2, mix, tr, rows, rels, LAT, trained={"T28", "T33", "T12", "T24"})
    assert same["mixdev"] == old["mixdev"] and same["pass"] == old["pass"]
    assert same["report_only"]["mixdev_trained_families"]["report_only_rows"] == 0
    assert same["report_only"]["mixdev_trained_families"]["all_families_mixdev_report_only"] is None


def test_pregate_cli_uses_the_manifest_trained_set_and_refuses_without_one(tmp, monkeypatch, capsys):
    good, off = mixdev_with_untrained()
    tr = rows_with(1200, 0.70, 0.60, seed=2, family="T36")
    t37_rows, t37_rels = t37()
    dev_rows = rows_with(400, 0.8, 0.8, seed=4)
    for i, x in enumerate(dev_rows):
        x["source"] = "ag_news" if i < 100 else "seen"
    monkeypatch.setattr(gc, "check_candidate", lambda rec, ad, name, root: {"adapter_sha256": "c" * 64})
    monkeypatch.setattr(gc, "check_stop_rule", lambda *a: {})
    monkeypatch.setattr(gc, "check_refparity", lambda root, ref, stored=gc.STORED_C1: {})
    monkeypatch.setattr(gc, "load_d2_set", lambda p, root, cand: {"sources": {"ag_news": 100}, "sources_sha256": "d"})
    monkeypatch.setattr(g, "complete_rows", lambda splits, cand, ref: dev_rows)
    monkeypatch.setattr(g, "pipeline_check", lambda names, reads: ([], {}))
    monkeypatch.setattr(gc, "split_rows", lambda split, cand, ref, root: {gc.MIXDEV: good + off, gc.TRANSFER: tr, gc.T37B_DEV: t37_rows}[split])
    monkeypatch.setattr(gc, "relations", lambda split, root: t37_rels)
    (tmp / "dev.json").write_text(json.dumps(dev_json()))
    (tmp / "lat.json").write_text(json.dumps(LAT))
    argv = ["pregate", "--dev", str(tmp / "dev.json"), "--latency", str(tmp / "lat.json"), "--looks", str(tmp / "looks.jsonl"),
            "--out-dir", str(tmp), "--root", str(tmp)]
    assert gc.main(argv) == 2 and "C2 mix manifest" in capsys.readouterr().out               # no manifest: cannot tell which families were trained
    write_mix_manifest(tmp, {"T28": 2247, "replay": 3370})
    assert gc.main(argv) == 0
    res = json.loads((tmp / f"gate_c2_pregate_{gc.CAND}.json").read_text())
    assert res["pass"] and res["checks"]["trained_families"]["trained"] == ["T28"]
    assert res["report_only"]["mixdev_trained_families"]["report_only_families"] == ["T12", "T24", "T33"]
    write_mix_manifest(tmp, {"T28": 2247, "T33": 88, "T12": 700, "T24": 599, "replay": 3370})     # another trained set = other inputs: one pre-gate per candidate
    assert gc.main(argv) == 2 and "other inputs" in capsys.readouterr().out


def test_pregate_never_names_a_dev_file_it_could_write():
    src = (C2B / "gate_c2.py").read_text()
    for call in ("write_text(", "write_jsonl(", ".write("):
        for ln in src.splitlines():
            if call in ln and ("mixdev" in ln.lower() or "c2_mixdev" in ln or "MIXDEV" in ln):
                raise AssertionError(f"gate_c2 writes near a mixdev file: {ln.strip()}")


# ---- PREREG A95 / A96: the owner's acceptance of ONE failed refparity look -------------------------------------------
A95_QUOTE = ("Option A: I accept the refparity miss (max dp 0.10 on 1 of 8,143 rows, all other checks pass) as serving-path "
             "noise, since all 19 models were read on the same H100 path. Continue C2 with the H100 reads and bring me any "
             "further blocker.")
STORED_NOTE = f"stored {gc.STORED_C1} is not the pre-registered q35_4b_pxE_parity"


def _look(tmp, **over):
    """The look exactly as gate_dev logs it for the C2 REF (failed on max |dp| only), over the files now in `tmp`."""
    with gc.at_root(tmp):
        fresh = g.fresh_sha(gc.REF)
    look = {"time": "2026-10-18T17:49:37+00:00", "mode": "refparity", "fresh": gc.REF, "stored": gc.STORED_C1, "size": "4b",
            "pass": False, "counts": False, "why_not": [STORED_NOTE], "n": 8143, "agree": 99.75, "mean_dp": 0.00198,
            "max_dp": 0.1013, "acc_diff": 0.0368, "fresh_sha": fresh}
    look.update(over)
    return look


def _write_record(tmp, look, **over):
    with gc.at_root(tmp):
        stored = g.fresh_sha(gc.STORED_C1)
    rec = {"record": "A95", "a95_quote": A95_QUOTE, "look_time": look["time"], "look_sha256": g.look_sha256(look),
           "fresh": look["fresh"], "stored": look["stored"], "size": look["size"], "n": look["n"], "max_dp": look["max_dp"],
           "fresh_sha": look["fresh_sha"], "stored_sha": stored}
    rec.update(over)
    (tmp / g.ACCEPT_A95).write_text(json.dumps(rec))
    return rec


def _write_looks(tmp, looks):
    (tmp / "logs").mkdir(exist_ok=True)
    (tmp / "logs/ship_looks.jsonl").write_text("".join(json.dumps(x) + "\n" for x in looks))


def _prereg_text(quote=A95_QUOTE, head="**Record A95 (18 Oct 2026 ~18:15 UTC, OWNER words, verbatim): "):
    """PREREG_FINAL.md as the real file has it: '> ' quoted and wrapped at about 120 columns."""
    import textwrap
    body = textwrap.fill(f'{head}"{quote}"** answering A94.', 118)
    return "> **Record A94 (orchestrator).** a failed look.\n\n" + "".join(f"> {ln}\n" for ln in body.splitlines())


@pytest.fixture
def a95(tmp, monkeypatch):
    """tmp lean root: a fresh and a stored read, the owner's words (OWNER_GO_C2.txt and PREREG_FINAL.md), one failed look
    (max |dp| only) and the A95 record for it. The code pin (gate_dev.ACCEPT_A95_LOOK_SHA256) is set to this look."""
    for name, body in ((gc.REF, "fresh read\n"), (gc.STORED_C1, "stored read\n")):
        (tmp / "preds_dev_nc").mkdir(exist_ok=True)
        (tmp / f"preds_dev_nc/{name}.jsonl").write_text(body)
    (tmp / "c2_build/train").mkdir(parents=True)
    (tmp / g.OWNER_GO_C2).write_text(f'- 18 Oct 2026, Record A95 (answer to A94 refparity): "{A95_QUOTE}"\n')
    (tmp / g.PREREG_FINAL_MD).write_text(_prereg_text())
    look = _look(tmp)
    monkeypatch.setattr(g, "ACCEPT_A95_LOOK_SHA256", g.look_sha256(look))
    _write_looks(tmp, [look])
    _write_record(tmp, look)
    return tmp, look


def test_a95_accepts_exactly_the_named_failed_look(a95, capsys):
    tmp, look = a95
    before = (tmp / "logs/ship_looks.jsonl").read_bytes()
    out = gc.check_refparity(tmp, gc.REF)
    assert "accepted by owner, PREREG A95" in capsys.readouterr().out
    assert out["accepted_by"] == "owner, PREREG A95" and out["look_pass"] is False and out["max_dp"] == 0.1013
    assert out["look_sha256"] == g.look_sha256(look)
    assert (tmp / "logs/ship_looks.jsonl").read_bytes() == before                  # the look stays logged pass false


def test_a95_without_a_record_keeps_the_original_refusal(a95):
    tmp, _ = a95
    (tmp / g.ACCEPT_A95).unlink()
    with pytest.raises(gc.Refused) as e:
        gc.check_refparity(tmp, gc.REF)
    assert str(e.value) == f"the last refparity look of {gc.REF} FAILED: stop and ask the owner (PREREG 4)"


@pytest.mark.parametrize("over", [{"time": "2026-10-18T17:49:38+00:00"}, {"max_dp": 0.1014}, {"n": 8142}, {"agree": 99.76},
                                  {"acc_diff": 0.0369}, {"counts": True}, {"fresh_sha": {"preds_dev_nc/x.jsonl": "0" * 64}},
                                  {"why_not": [STORED_NOTE, "x"]}])
def test_a95_another_look_than_the_named_one_refuses(a95, over):
    tmp, look = a95
    _write_looks(tmp, [look | over])               # the log holds a look the record does not name
    with pytest.raises(gc.Refused, match="FAILED: stop and ask the owner .*does not apply"):
        gc.check_refparity(tmp, gc.REF)


@pytest.mark.parametrize("over,why", [({"agree": 98.9}, "argmax agreement"), ({"mean_dp": 0.0051}, "mean .dp."),
                                      ({"acc_diff": 0.31}, "accuracy difference"), ({"acc_diff": -0.31}, "accuracy difference"),
                                      ({"max_dp": 0.05}, "max .dp. did not fail"), ({"max_dp": 0.04}, "max .dp. did not fail"),
                                      ({"agree": None}, "no finite"), ({"mean_dp": float("inf")}, "no finite"),
                                      ({"why_not": [STORED_NOTE, "not the pre-registered 9 splits"]}, "other reasons"),
                                      ({"why_not": ["the fresh read is not a clean od_gcp predict read"]}, "other reasons"),
                                      ({"pass": None}, "did not fail"), ({"mode": "ship"}, "did not fail")])
def test_a95_a_look_failing_any_other_bar_refuses_even_if_named(a95, over, why, monkeypatch):
    tmp, look = a95
    bad = look | over                              # the record is rebuilt for THIS look, so only the bars can refuse it
    monkeypatch.setattr(g, "ACCEPT_A95_LOOK_SHA256", g.look_sha256(bad))          # ... and the code pin follows it
    _write_looks(tmp, [bad])
    _write_record(tmp, bad)
    with pytest.raises(gc.Refused):
        gc.check_refparity(tmp, gc.REF)
    with gc.at_root(tmp):
        ok, reason = g.refparity_owner_accepted(bad, say=lambda *a: None)
    assert not ok and __import__("re").search(why, reason)


@pytest.mark.parametrize("name", ["fresh", "stored"])
def test_a95_a_changed_or_missing_read_file_refuses(a95, name):
    tmp, _ = a95
    f = tmp / "preds_dev_nc" / f"{gc.REF if name == 'fresh' else gc.STORED_C1}.jsonl"
    f.write_text("edited\n")
    with pytest.raises(gc.Refused, match="does not apply.*changed since the accepted look"):
        gc.check_refparity(tmp, gc.REF)
    f.unlink()
    with pytest.raises(gc.Refused, match="does not apply"):
        gc.check_refparity(tmp, gc.REF)


def test_a95_a_new_read_file_of_either_name_refuses(a95):
    tmp, _ = a95
    (tmp / "preds_hard_dev").mkdir()
    (tmp / f"preds_hard_dev/{gc.STORED_C1}.jsonl").write_text("one more stored split\n")
    with pytest.raises(gc.Refused, match="stored read files .* changed"):
        gc.check_refparity(tmp, gc.REF)


def test_a95_a_later_failed_look_refuses_and_a_later_pass_works_as_before(a95, capsys):
    tmp, look = a95
    later_fail = look | {"time": "2026-10-18T19:00:00+00:00"}                      # same numbers, another look
    _write_looks(tmp, [look, later_fail])
    with pytest.raises(gc.Refused, match="FAILED: stop and ask the owner .*does not apply"):
        gc.check_refparity(tmp, gc.REF)
    later_pass = look | {"time": "2026-10-18T19:30:00+00:00", "pass": True, "max_dp": 0.04}
    _write_looks(tmp, [look, later_fail, later_pass])
    capsys.readouterr()
    out = gc.check_refparity(tmp, gc.REF)
    assert "accepted_by" not in out and "accepted by owner" not in capsys.readouterr().out
    _write_looks(tmp, [look, later_pass, later_fail])                              # the failure is the last look again
    with pytest.raises(gc.Refused, match="FAILED"):
        gc.check_refparity(tmp, gc.REF)


def test_a95_a_look_against_another_stored_read_or_size_keeps_its_refusal(a95):
    tmp, look = a95
    _write_looks(tmp, [look | {"stored": "q35_4b_pxE_parity"}])
    with pytest.raises(gc.Refused, match="is against q35_4b_pxE_parity"):
        gc.check_refparity(tmp, gc.REF)
    _write_looks(tmp, [look | {"size": "2b"}])
    with pytest.raises(gc.Refused, match="is against"):
        gc.check_refparity(tmp, gc.REF)
    with pytest.raises(gc.Refused, match="no refparity look for q35_4b_c2"):
        _write_looks(tmp, [look])
        gc.check_refparity(tmp, gc.CAND)


@pytest.mark.parametrize("how", ["bad_json", "other_record", "no_quote", "quote_not_in_owner_file", "quote_edited", "missing_key",
                                 "wrong_look_sha", "wrong_stored_sha", "quote_not_option_a", "quote_only_option_a",
                                 "quote_truncated_prefix", "quote_truncated_suffix", "quote_with_extra_text",
                                 "owner_file_has_only_a_prefix", "prereg_lacks_the_quote", "prereg_quote_outside_record_a95",
                                 "prereg_missing", "prereg_quote_edited"])
def test_a95_a_bad_record_refuses(a95, how):
    tmp, look = a95
    p = tmp / g.ACCEPT_A95
    rec = json.loads(p.read_text())
    if how == "bad_json":
        p.write_text("{not json")
    elif how == "other_record":
        p.write_text(json.dumps(rec | {"record": "A94"}))
    elif how == "no_quote":
        p.write_text(json.dumps(rec | {"a95_quote": ""}))
    elif how == "quote_not_in_owner_file":
        (tmp / g.OWNER_GO_C2).write_text("- nothing about A95\n")
    elif how == "quote_edited":
        p.write_text(json.dumps(rec | {"a95_quote": A95_QUOTE.replace("accept", "reject")}))
    elif how == "missing_key":
        rec.pop("stored_sha")
        p.write_text(json.dumps(rec))
    elif how == "wrong_look_sha":
        p.write_text(json.dumps(rec | {"look_sha256": "0" * 64}))
    elif how == "wrong_stored_sha":
        p.write_text(json.dumps(rec | {"stored_sha": {k: "0" * 64 for k in rec["stored_sha"]}}))
    elif how == "quote_not_option_a":
        q = "Continue C2 with the H100 reads and bring me any further blocker."       # a true substring, but not the A95 answer
        p.write_text(json.dumps(rec | {"a95_quote": q}))
    elif how in ("quote_only_option_a", "quote_truncated_prefix", "quote_truncated_suffix", "quote_with_extra_text"):
        q = {"quote_only_option_a": "Option A", "quote_truncated_prefix": A95_QUOTE[:-20],
             "quote_truncated_suffix": A95_QUOTE[20:], "quote_with_extra_text": A95_QUOTE + " Yes."}[how]
        p.write_text(json.dumps(rec | {"a95_quote": q}))                               # in the file as a substring (or not)
        (tmp / g.OWNER_GO_C2).write_text((tmp / g.OWNER_GO_C2).read_text() + q + "\n")
    elif how == "owner_file_has_only_a_prefix":
        (tmp / g.OWNER_GO_C2).write_text(f'- Record A95: "{A95_QUOTE[:-20]}"\n')
    elif how == "prereg_lacks_the_quote":
        (tmp / g.PREREG_FINAL_MD).write_text(_prereg_text(quote=A95_QUOTE[:-20]))
    elif how == "prereg_quote_outside_record_a95":
        (tmp / g.PREREG_FINAL_MD).write_text(_prereg_text(head="**Record A93 (orchestrator): "))
    elif how == "prereg_missing":
        (tmp / g.PREREG_FINAL_MD).unlink()
    elif how == "prereg_quote_edited":
        (tmp / g.PREREG_FINAL_MD).write_text(_prereg_text(quote=A95_QUOTE.replace("accept", "reject")))
    with pytest.raises(gc.Refused, match="FAILED: stop and ask the owner"):
        gc.check_refparity(tmp, gc.REF)


def test_a95_a_record_for_one_look_cannot_accept_a_passing_or_other_ref(a95, capsys):
    tmp, look = a95
    passing = look | {"pass": True, "max_dp": 0.04, "counts": False}
    _write_looks(tmp, [passing])                                                  # pass: the ordinary path, no banner
    capsys.readouterr()
    assert "accepted_by" not in gc.check_refparity(tmp, gc.REF)
    assert "accepted by owner" not in capsys.readouterr().out
    (tmp / "preds_dev_nc/other_ref.jsonl").write_text("x\n")
    other = look | {"fresh": "other_ref", "fresh_sha": {"preds_dev_nc/other_ref.jsonl": g.hashlib.sha256(b"x\n").hexdigest()}}
    _write_looks(tmp, [other])                                                    # same numbers, another REF name
    with pytest.raises(gc.Refused, match="does not apply"):
        gc.check_refparity(tmp, "other_ref")


def test_a95_the_code_pins_the_one_look_the_record_cannot_move(a95):
    """The pin lives in gate_dev.py: a record naming another look sha, with the log edited to match, is refused; n and max |dp|
    are bounded in code too."""
    tmp, look = a95
    edited = look | {"agree": 99.76}                                  # an edited look, the log AND the record agree on it
    _write_looks(tmp, [edited])
    _write_record(tmp, edited)
    assert g.look_sha256(edited) != g.ACCEPT_A95_LOOK_SHA256           # the fixture pin is still the original look
    with pytest.raises(gc.Refused, match="not the one look the owner accepted"):
        gc.check_refparity(tmp, gc.REF)
    _write_looks(tmp, [look])                                         # the original log with a record that names the edited sha
    _write_record(tmp, look, look_sha256=g.look_sha256(edited))
    with pytest.raises(gc.Refused, match="does not apply"):
        gc.check_refparity(tmp, gc.REF)


@pytest.mark.parametrize("over,why", [({"n": 8142}, "n is not the accepted 8143"), ({"n": 8144}, "n is not the accepted 8143"),
                                      ({"max_dp": 0.10141}, "max .dp. is above the accepted 0.1014"),
                                      ({"max_dp": 0.2}, "max .dp. is above the accepted 0.1014")])
def test_a95_n_or_max_dp_off_refuses_even_with_a_matching_record_and_pin(a95, over, why, monkeypatch):
    tmp, look = a95
    bad = look | over
    monkeypatch.setattr(g, "ACCEPT_A95_LOOK_SHA256", g.look_sha256(bad))
    _write_looks(tmp, [bad])
    _write_record(tmp, bad)
    with pytest.raises(gc.Refused, match="does not apply"):
        gc.check_refparity(tmp, gc.REF)
    with gc.at_root(tmp):
        ok, reason = g.refparity_owner_accepted(bad, say=lambda *a: None)
    assert not ok and __import__("re").search(why, reason)


def test_a95_max_dp_at_the_accepted_bound_is_still_accepted(a95, monkeypatch):
    tmp, look = a95
    edge = look | {"max_dp": 0.1014}
    monkeypatch.setattr(g, "ACCEPT_A95_LOOK_SHA256", g.look_sha256(edge))
    _write_looks(tmp, [edge])
    _write_record(tmp, edge)
    assert gc.check_refparity(tmp, gc.REF)["accepted_by"] == "owner, PREREG A95"


def test_a95_the_pinned_sentence_is_the_real_one_and_the_real_look_is_the_pinned_one():
    """Against the real files (skipped where they are absent): the constant equals the owner's words in OWNER_GO_C2.txt and in
    PREREG_FINAL.md Record A95, the shipped record carries the same sentence, and the logged look hashes to the pin."""
    lean = C2B.parent
    assert g.A95_QUOTE == A95_QUOTE
    go, rec = lean / g.OWNER_GO_C2, lean / g.ACCEPT_A95
    if not (go.exists() and (lean / g.PREREG_FINAL_MD).exists() and rec.exists()):
        pytest.skip("real OWNER_GO_C2.txt / PREREG_FINAL.md / record not present")
    old = g.ROOT
    g.ROOT = lean
    try:
        assert A95_QUOTE in go.read_text() and g._prereg_has_a95_quote()
        assert json.loads(rec.read_text())["a95_quote"] == A95_QUOTE
        assert json.loads(rec.read_text())["look_sha256"] == g.ACCEPT_A95_LOOK_SHA256
        looks = [json.loads(x) for x in (lean / "logs/ship_looks.jsonl").read_text().splitlines() if x.strip()]
        mine = [x for x in looks if x.get("mode") == "refparity" and x.get("time") == "2026-10-18T17:49:37+00:00"]
        assert len(mine) == 1 and g.look_sha256(mine[0]) == g.ACCEPT_A95_LOOK_SHA256 and mine[0]["pass"] is False
    finally:
        g.ROOT = old
