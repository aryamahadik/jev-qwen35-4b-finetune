"""router.py on CPU with a synthetic dev set: guards, features, strata, fit, threshold, invariance."""
import json
import random

import numpy as np
import pytest
from conftest import mc_row, yn_row

import router as R
from common import write_jsonl


def test_guard_refuses_held_out_paths():
    for bad in ("x/ohs2/rows.jsonl", "bench/nimble_suite/a.jsonl", "bench/external_quarantine/q.jsonl",
                "bench/ejs5/p.jsonl", "data/sealed_x.jsonl", "bench/jevbench_v154/a.jsonl"):
        with pytest.raises(SystemExit):
            R._guard_path(bad)
    assert R._guard_path("lean/data/dev.jsonl").name == "dev.jsonl"


def test_dev_splits_match_gate_dev():
    assert R.dev_splits() == "dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev".split(",")


def test_think_type_and_policy():
    assert R.think_type(mc_row("a", "Tom has 3 apples and buys 4 more.", ["7", "8", "9"], "7")) == "math"
    assert R.think_type(mc_row("b", "def f(x):\n    return x * 2\nprint(f(3))", ["six", "five"], "six")) == "code"
    assert R.think_type(mc_row("c", "The sky is blue.", ["true", "false"], "true")) == "other"
    assert R.policy_for(mc_row("a", "Compute 12 + 30 = ?", ["42", "41"], "42")) == "short_cot"


def test_features_ignore_dataset_fields():
    row = mc_row("a", "If it rains, the match is not played. It rained.", ["played", "not played"], "not played",
                 source="banking77", set="k_x", track="DEV", split="dev")
    probs = {"played": 0.4, "not played": 0.6}
    blank = {**row, "source": "", "set": "", "track": "", "split": ""}
    assert R.features(row, probs) == R.features(blank, probs)
    f = R.features(row, probs)
    assert list(f) == R.FEATURES and f["cue_causal"] == 1.0 and abs(f["margin"] - 0.2) < 1e-9


def test_pick_threshold_closest_share():
    t, sh = R.pick_threshold([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], [1] * 10, 0.1)
    assert t == 1.0 and abs(sh - 0.1) < 1e-12
    t, sh = R.pick_threshold([0.5] * 8 + [0.9, 0.9], [1] * 10, 0.1)  # ties: 20% is the closest share
    assert t == 0.9 and abs(sh - 0.2) < 1e-12


def test_fit_logistic_fractional_targets():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(2000, 2))
    p = 1 / (1 + np.exp(-(0.5 + 2.0 * X[:, 0])))
    y = (rng.random(2000) < p).astype(float) * 0.5 + 0.25  # fractional targets in {0.25, 0.75}
    b = R.fit_logistic(X, y, np.ones(2000), l2=0.0)
    assert b[1] > 0.3 and abs(b[2]) < 0.15


def _synthetic(tmp_path, monkeypatch, n=600):
    """Two fake dev splits. C1 is unsure on half; 'thinking helps' when the text has a sum and C1 is unsure."""
    rng = random.Random(0)
    data, preds = tmp_path / "data", tmp_path
    data.mkdir()
    think = []
    for sp in ("devA", "devB"):
        rows, pr = [], []
        for i in range(n):
            rid = f"{sp}_{i}"
            maths = i % 3 == 0
            st = f"Add {i} + {i + 1} to get the total." if maths else f"Plain sentence number {i}."
            gold = "x" if rng.random() < 0.5 else "y"
            unsure = i % 2 == 0
            top = rng.uniform(0.5, 0.75) if unsure else rng.uniform(0.9, 0.99)
            c1 = gold if (not unsure or rng.random() < 0.5) else ("y" if gold == "x" else "x")
            rows.append(mc_row(rid, st, ["x", "y"], gold, group_id=f"g{rid}"))
            pr.append({"id": rid, "probs": {c1: top, ("y" if c1 == "x" else "x"): 1 - top}})
            helps = maths and unsure
            th = gold if (helps or rng.random() < 0.5) else ("y" if gold == "x" else "x")
            if not maths:
                th = c1 if rng.random() < 0.8 else ("y" if c1 == "x" else "x")  # non-maths: think mostly copies
            think.append({"key": f"dev|{sp}|{rid}", "pred_key": th, "think_tokens": 100, "status": "ok"})
        write_jsonl(data / f"{sp}.jsonl", rows)
        write_jsonl(preds / f"preds_{sp}" / "q35_4b_main500k.jsonl", pr)
    monkeypatch.setattr(R, "LEAN", tmp_path)
    monkeypatch.setattr(R, "OUT", tmp_path / "out")
    monkeypatch.setattr(R, "dev_splits", lambda: ["devA", "devB"])
    write_jsonl(tmp_path / "think_out.jsonl", think)
    return tmp_path / "think_out.jsonl"


def test_tasks_strata_and_no_gold(tmp_path, monkeypatch):
    _synthetic(tmp_path, monkeypatch)
    R.main(["tasks", "--hi-share", "0.2"])
    tasks = [json.loads(l) for l in open(R.OUT / "think_tasks_dev.jsonl")]
    local = {json.loads(l)["key"]: json.loads(l) for l in open(R.OUT / "think_tasks_dev_local.jsonl")}
    assert all("gold" not in t["row"] for t in tasks)
    lo = [k for k, v in local.items() if v["stratum"] == "lo"]
    hi = [k for k, v in local.items() if v["stratum"] == "hi"]
    assert len(lo) == 600  # every unsure row (top 0.55 < 0.8) on both splits
    assert 0.1 < len(hi) / 600 < 0.3 and all(local[k]["weight"] == 5.0 for k in hi)
    man = json.loads((R.OUT / "tasks_manifest.json").read_text())
    assert man["tasks"] == len(tasks) and any("think_rows.py" in c and "--budget 1024" in c for c in man["commands"])


def test_fit_routes_about_ten_percent_and_finds_the_helpful_kind(tmp_path, monkeypatch):
    th = _synthetic(tmp_path, monkeypatch)
    R.main(["tasks", "--hi-share", "0.5"])
    R.main(["fit", "--think", str(th)])
    m = json.loads((R.OUT / "router.json").read_text())
    fit = m["report"]["dev_fit"]["router"]
    assert 0.05 <= fit["route_share"] <= 0.12
    assert fit["gain_pts"] > 0 and m["threshold"] > 0.5
    con = m["report"]["dev_confirm"]["router"]
    assert con["n"] > 0 and con["gain_pts"] >= 0
    rt = R.load_router(R.OUT / "router.json")
    helpful = mc_row("h", "Add 3 + 4 to get the total.", ["x", "y"], "x")
    plain = mc_row("p", "Plain sentence number 5.", ["x", "y"], "x")
    unsure, sure = {"x": 0.55, "y": 0.45}, {"x": 0.97, "y": 0.03}
    assert rt.score(helpful, unsure) > rt.score(plain, unsure) and rt.score(helpful, unsure) > rt.score(helpful, sure)
    d = rt.decide(helpful, unsure)
    assert d["route"] and d["policy"] == "short_cot"
    assert rt.decide(plain, sure) == {**rt.decide(plain, sure), "route": False, "policy": "fast"}


def test_fit_refuses_non_dev_keys(tmp_path, monkeypatch):
    th = _synthetic(tmp_path, monkeypatch)
    R.main(["tasks"])
    rows = [json.loads(l) for l in open(th)] + [{"key": "nimble|squad2|1", "pred_key": "x"}]
    write_jsonl(th, rows)
    with pytest.raises(SystemExit):
        R.main(["fit", "--think", str(th)])


def test_route_cli(tmp_path, monkeypatch):
    th = _synthetic(tmp_path, monkeypatch)
    R.main(["tasks", "--hi-share", "0.5"])
    R.main(["fit", "--think", str(th), "--route-share", "0.16"])
    rows = [mc_row("h", "Add 3 + 4 to get the total.", ["x", "y"], "x"), yn_row("n", "Plain.", 1)]
    write_jsonl(tmp_path / "r.jsonl", rows)
    write_jsonl(tmp_path / "p.jsonl", [{"id": "h", "probs": {"x": 0.5, "y": 0.5}},
                                       {"id": "n", "probs": {"yes": 0.99, "no": 0.01}}])
    R.main(["route", "--rows", str(tmp_path / "r.jsonl"), "--c1", str(tmp_path / "p.jsonl"),
            "--out", str(tmp_path / "d.jsonl"), "--model", str(R.OUT / "router.json")])
    d = {json.loads(l)["id"]: json.loads(l) for l in open(tmp_path / "d.jsonl")}
    assert d["h"]["route"] and not d["n"]["route"] and d["n"]["c1_key"] == "yes" and d["h"]["c1_key"] == "x"
