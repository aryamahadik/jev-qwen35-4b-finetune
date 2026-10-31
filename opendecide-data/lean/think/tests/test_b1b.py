"""A30 (B1b): engine configs (DFlash with capped requests, native MTP), the speculative-state budget, the gold-free
speculation pick, the step runner with fake engines (deadline cut), the S1 / DEER rules at their boundaries, the cost
caps and the local scoring decisions. CPU only."""
import json
import time

import pytest

import eval_think as E
import modal_think as MT
import think_engine as te
from common import sha256_file, write_jsonl
from conftest import mc_row


# ------------------------------------------------------------------------------------------------ engine configs
def test_engine_kwargs_b1b_and_b1a_unchanged():
    k = MT.engine_kwargs("bf16_mtp", 16, 0.8)
    assert (k["speculative_algorithm"], k["speculative_num_steps"], k["speculative_eagle_topk"],
            k["speculative_num_draft_tokens"], k["max_running_requests"]) == ("NEXTN", 3, 1, 4, 32)
    assert "speculative_draft_model_path" not in k and "quantization" not in k
    k = MT.engine_kwargs("fp8_dflash_m16", 16, 0.8)
    assert (k["speculative_algorithm"], k["speculative_dflash_block_size"], k["max_running_requests"],
            k["quantization"]) == ("DFLASH", 16, 16, "fp8")
    k = MT.engine_kwargs("bf16_dflash")  # B1a config: as it ran
    assert (k["speculative_algorithm"], k["max_running_requests"], k["mem_fraction_static"]) == ("DFLASH", 128, 0.55)
    assert "speculative_algorithm" not in MT.engine_kwargs("bf16_nospec")
    for c in MT.CONFIGS:
        assert set(MT.engine_kwargs(c)) <= MT.SGLANG_FIELDS


def test_spec_state_budget_explains_b1a_and_fits_b1b():
    assert MT.spec_state_gb("bf16_dflash") > MT.H100_GB  # 99 GB: why B1a's DFlash could not start
    assert MT.spec_state_gb("bf16_nospec") == 0.0
    for c in ("bf16_dflash_m16", "fp8_dflash_m16", "bf16_mtp", "fp8_mtp"):
        assert MT.spec_state_gb(c) <= 0.5 * MT.B1B_PLAN["mem_fraction"] * MT.H100_GB


# ------------------------------------------------------------------------------------------------ gold-free pick
def _role(cfg, rate, n=10, wall=0.5, tokens=300, partial=False, err=None):
    recs = [{"id": f"r{i}", "wall_s": wall, "think_tokens": tokens} for i in range(n)]
    return {"config": cfg, "errors": {"engine_start": err} if err else {},
            "steps": {"speed": {"1024": {"decode_tok_s_p50": rate}},
                      "math_short_bs1": {"records": recs, "n_rows": 10, "partial": partial}}}


def test_pick_spec_rules():
    ref = {"config": "bf16_nospec", "steps": {"speed": {"1024": {"decode_tok_s_p50": 250.0}}}}
    res = {"ref": ref, "spec_dflash": _role("bf16_dflash_m16", 800, wall=0.4), "spec_mtp": _role("bf16_mtp", 400)}
    pick, rep = MT.pick_spec(res)
    assert pick == "bf16_dflash_m16" and rep["arms"]["spec_mtp"]["eligible"]  # MTP 1.6x exactly = eligible
    assert MT.pick_spec(res, {"spec_dflash": False, "spec_mtp": True})[0] == "bf16_mtp"  # S1 accuracy filter
    res["spec_dflash"] = _role("bf16_dflash_m16", 620, wall=0.1)  # 2.48x < 2.5
    res["spec_mtp"] = _role("bf16_mtp", 399)  # 1.596x < 1.6
    assert MT.pick_spec(res)[0] is None
    for bad in (dict(err="ValueError: no KV"), dict(partial=True), dict(n=9), dict(tokens=301)):
        res["spec_dflash"] = _role("bf16_dflash_m16", 900, **bad)
        assert MT.pick_spec(res)[0] is None, bad
    assert MT.FP8_FOR[None] == "fp8_nospec" and MT.FP8_FOR["bf16_mtp"] == "fp8_mtp"


# ------------------------------------------------------------------------------------------------ step runner
def _items(tok, dio, n=6):
    tp = te.ThinkPath(te.FakeBackend(think_len=40), tok, dio)
    rows = [mc_row(f"q{i}", f"state {i}", ["1", "2", "3", "4"], "1") for i in range(n)]
    preps = tp.prepare([{"id": r["id"], "row": r} for r in rows])
    return tp, [{"id": r["id"], "row": r, "user": p["user"], "info": p["info"]} for r, p in zip(rows, preps)]


def test_run_steps_all_roles_fake(tok, dio):
    tp, items = _items(tok, dio)
    plan = {**MT.B1B_PLAN, "n_speed": 2, "chunk_bs1": 4, "chunk_bat": 4}
    steps = sorted({s for _, _, ss in MT.B1B_ROLES for s in ss})
    res = {"steps": {}, "skipped": [], "errors": {}}
    saves = []
    MT.run_steps(tp, MT.FakeEngine(rate=5000), items, steps, plan, time.time() + 3600, res, lambda: saves.append(1))
    assert not res["errors"] and not res["skipped"] and len(saves) == len(steps)
    for s in ("math_short_bs1", "math_short_bat", "math_full", "math_cap1024_bat", "math_deer1024_bat"):
        st = res["steps"][s]
        assert st["n"] == st["n_rows"] == 6 and not st["partial"]
        assert all("gold" not in r for r in st["records"])
    bs1 = res["steps"]["math_short_bs1"]["records"]
    assert all(r["group_size"] == 1 and r["policy"] == "short_cot" and r["think_tokens"] <= 300 for r in bs1)
    assert res["steps"]["math_cap1024_bat"]["kw"] == {"deer": {}}  # DEER off in the plain 1,024 arm
    assert all(r["policy"] == "full_think" for r in res["steps"]["math_full"]["records"])
    assert set(res["steps"]["speed"]) == {"300", "1024"}


def test_run_steps_deadline(tok, dio):
    tp, items = _items(tok, dio)
    plan = {**MT.B1B_PLAN, "n_speed": 2, "chunk_bat": 4}
    res = {"steps": {}, "skipped": [], "errors": {}}
    MT.run_steps(tp, MT.FakeEngine(), items, ["math_short_bat"], plan, time.time() + 90, res)  # step ok, chunk needs 120
    st = res["steps"]["math_short_bat"]
    assert st["partial"] and st["n"] == 0
    res = {"steps": {}, "skipped": [], "errors": {}}
    MT.run_steps(tp, MT.FakeEngine(), items, ["sanity", "math_full"], plan, time.time() + 30, res)
    assert res["skipped"] == ["sanity", "math_full"] and not res["steps"]


def test_fake_engine_rates_hold():
    def rate(r):
        e = MT.FakeEngine(rate=r)
        return MT._speed(e, ["p"] * 2, 1024, {}, time.time() + 60)["decode_tok_s_p50"]
    assert rate(800) / rate(250) > 2.5


# ------------------------------------------------------------------------------------------------ rules
def _rows(n):
    return {f"m{i}": {"id": f"m{i}", "qtype": "choice", "options": ["a", "b"], "gold": "a"} for i in range(n)}


def _recs(rows, n_right, **kw):
    return {i: {"id": i, "final_key": "a" if k < n_right else "b", **kw} for k, i in enumerate(sorted(rows))}


def test_rule_spec_acc_boundaries():
    rows = _rows(100)
    ref = _recs(rows, 80)
    assert E.rule_spec_acc(rows, _recs(rows, 82), ref)["pass"]  # +2.0 pts
    assert E.rule_spec_acc(rows, _recs(rows, 78), ref)["pass"]  # -2.0 pts
    assert not E.rule_spec_acc(rows, _recs(rows, 77), ref)["pass"]
    assert not E.rule_spec_acc(rows, _recs(rows, 83), ref)["pass"]
    part = _recs(rows, 80)
    part.pop("m0")
    assert E.rule_spec_acc(rows, part, ref)["status"] == "incomplete"


def test_rule_deer_boundaries():
    rows = _rows(100)
    ids = sorted(rows)
    plain = _recs(rows, 100, think_tokens=1000)

    def deer(n_exit, n_wrong_exited):
        d = _recs(rows, 100, think_tokens=400)
        for k, i in enumerate(ids[:n_exit]):
            d[i]["exit"] = "deer"
            if k < n_wrong_exited:
                d[i]["final_key"] = "b"
        return d
    r = E.rule_deer(rows, deer(50, 1), plain)  # 49/50 vs 50/50 = -2.0 pts: pass
    assert r["pass"] and r["early_exits"] == 50 and r["tokens_ratio"] == 0.4
    assert not E.rule_deer(rows, deer(50, 2), plain)["pass"]  # -4 pts
    r = E.rule_deer(rows, deer(19, 0), plain)
    assert r["status"] == "too_few_early_exits" and not r["pass"]


def test_estimate_and_caps():
    e = MT.estimate_b1b(MT.B1B_CAP_MIN)
    assert e["usd_worst_case"] <= MT.B1B_USD_CAP and e["usd_expected"] <= e["usd_pessimistic"] <= e["usd_worst_case"]
    assert not MT.check_caps(e, MT.B1B_USD_CAP)
    assert MT.check_caps(e, 5.0)  # refuses below the worst case
    assert MT.check_caps(MT.estimate_b1b(120), MT.B1B_USD_CAP)  # a longer window does not fit the per-launch cap


# ------------------------------------------------------------------------------------------------ local scoring
def _run_dir(tmp_path, dflash_right=30):
    n = 40
    clean = tmp_path / "clean"
    clean.mkdir()
    rows = [{"id": f"m{i}", "qtype": "choice", "state": "s", "instructions": "i", "options": ["a", "b"], "gold": "a",
             "set": "gsm8k_train500", "think_type": "math", "split": "dev_fit"} for i in range(n)]
    write_jsonl(clean / "gsm8k_train500.jsonl", rows)
    (clean / "manifest.json").write_text(json.dumps({"sets": {"gsm8k_train500": {
        "sha256": sha256_file(clean / "gsm8k_train500.jsonl")}}}))
    ids = [r["id"] for r in rows]

    def recs(right, policy, wall=0.5, gs=1, tokens=300, exit_=None):
        return [{"id": i, "final_key": "a" if k < right else "b", "policy": policy, "wall_s": wall, "group_size": gs,
                 "think_tokens": tokens, "exit": exit_ or "budget"} for k, i in enumerate(ids)]

    def step(rs):
        return {"records": rs, "n_rows": n, "n": len(rs), "partial": False}

    def speed(rate):
        return {"1024": {"decode_tok_s_p50": rate}}
    run = tmp_path / "b1b_test"
    run.mkdir()
    roles = {
        "ref": {"config": "bf16_nospec", "steps": {"speed": speed(250), "math_short_bat": step(recs(30, "short_cot", gs=40)),
                                                   "math_full": step(recs(32, "full_think", tokens=2000, gs=40))}},
        "spec_dflash": {"config": "bf16_dflash_m16", "steps": {"speed": speed(800),
                                                               "math_short_bs1": step(recs(dflash_right, "short_cot", 0.4))}},
        "spec_mtp": {"config": "bf16_mtp", "steps": {"speed": speed(450), "math_short_bs1": step(recs(30, "short_cot", 0.7))}},
        "fp8": {"config": "fp8_dflash_m16", "steps": {"speed": speed(900), "math_short_bs1": step(recs(30, "short_cot", 0.3))}},
        "deer": {"config": "bf16_nospec", "steps": {"math_cap1024_bat": step(recs(36, "capped_think", tokens=900)),
                                                    "math_deer1024_bat": step(recs(36, "capped_think", tokens=500,
                                                                                   exit_="deer"))}}}
    for k, v in roles.items():
        (run / f"{k}.json").write_text(json.dumps({**v, "errors": {}, "skipped": []}))
    return run, clean


def test_score_b1b_decisions(tmp_path, monkeypatch):
    monkeypatch.setattr(MT, "_b1a_fast_p50", lambda: (14.1, "test"))
    run, clean = _run_dir(tmp_path)
    s = MT.score_b1b(run, clean)
    assert s["decisions"] == {"speculation": "bf16_dflash_m16", "b1_pass": True, "ship_fp8": True,
                              "deer_on_in_capped_think": True}
    assert s["b1"]["math"]["keep_ratio"] == round(30 / 32, 4) and s["b1"]["math"]["median_wall_s"] == 0.4
    assert (run / "records" / "spec_dflash__math_short_bs1.jsonl").exists()
    # DFlash 26/40 vs no-spec 30/40 = -10 pts: fails S1 accuracy -> MTP ships; the FP8 arm ran with DFlash -> not shipped
    (tmp_path / "x").mkdir()
    run2, clean2 = _run_dir(tmp_path / "x", dflash_right=26)
    s = MT.score_b1b(run2, clean2)
    assert s["decisions"]["speculation"] == "bf16_mtp" and s["b1"]["pass"] and not s["ship_fp8"]
    assert s["fp8"]["same_spec_as_shipped"] is False


def test_score_b1b_no_spec_fails_b1(tmp_path, monkeypatch):
    monkeypatch.setattr(MT, "_b1a_fast_p50", lambda: (14.1, "test"))
    run, clean = _run_dir(tmp_path)
    for role in ("spec_dflash", "spec_mtp"):
        cfg = {r: c for r, c, _ in MT.B1B_ROLES}[role]
        (run / f"{role}.json").write_text(json.dumps({"config": cfg, "steps": {}, "errors": {"engine_start": "x"},
                                                      "skipped": []}))
    s = MT.score_b1b(run, clean)
    assert s["decisions"]["speculation"] == "none" and not s["b1"]["pass"] and not s["ship_fp8"]
    assert s["b1"]["math"]["status"] == "incomplete" and "note" in s["b1"]["math"]


# ------------------------------------------------------------------------------------------------ the frozen set
def test_b1b_sets_selection_and_inputs():
    import b1b_sets as B
    recs = [{"question": f"Tom has {i} apples and buys 3 more. How many now?", "answer": f"... #### {i + 3}"}
            for i in range(30)]
    rows = B.gsm8k_rows(recs)
    assert len(rows) == 30 and all(r["think_type"] == "math" and r["gold"] in r["options"] for r in rows)
    a = B.select(rows, set(), 10)
    b = B.select(rows, {a[0]["id"]}, 10)
    assert [r["id"] for r in a] == [r["id"] for r in B.select(list(reversed(rows)), set(), 10)]  # order-free
    assert a[0]["id"] not in {r["id"] for r in b} and [r["id"] for r in b][:9] == [r["id"] for r in a][1:]
    man = MT._check_b1b_inputs()  # the real frozen files: sha256 match, no gold in the Modal input
    assert man["n"] == 500 and man["gold_free"]
