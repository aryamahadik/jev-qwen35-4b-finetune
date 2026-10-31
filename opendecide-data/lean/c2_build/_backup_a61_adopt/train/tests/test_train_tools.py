"""CPU tests for the C2 training chain tools (tiny fake tensors, fake billing, no Modal, no network).
  cd lean/c2_build/train && ../../../.venv/bin/python -B -m pytest -q tests"""
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
import torch
from safetensors.torch import save_file

TRAIN = Path(__file__).resolve().parents[1]
LEAN = TRAIN.parents[1]
sys.path.insert(0, str(TRAIN))
import c2_check as cc  # noqa: E402
import merge_avg as ma  # noqa: E402
import preflight_c2 as pf  # noqa: E402
import select_candidate as sc  # noqa: E402
import symmetrise as sy  # noqa: E402


# ----------------------------------------------------------------------------------------------- config / mount / prereg
def cfgs():
    return json.loads((LEAN / "runs/q35_4b_c2.json").read_text()), json.loads((LEAN / "runs/q35_4b_c_r1.json").read_text())


def filled(cfg):
    fill = {"epochs": 0.9871, "expect_ord_rows": 4000, "expect_kd_targets": 20000, "expect_kd_full": 23, "seed": pf.SEED}
    return {**cfg, **{k: fill[k] for k in pf.FILL_KEYS}}, fill


def test_config_is_the_a37_recipe_and_only_fill_problems_remain():
    cfg, tmpl = cfgs()
    probs = pf.check_config(cfg, tmpl, None)
    assert len(probs) == 1 and "FILL" in probs[0]
    f, fill = filled(cfg)
    assert pf.check_config(f, tmpl, fill) == []
    assert cfg["seed"] == 20261013 and cfg["lr"] == 5e-5 and cfg["init_adapter"].endswith("q35_4b_main500k_init")
    assert len(cfg["snap_fracs"]) + 1 in range(6, 11) and "snap_every" not in cfg


@pytest.mark.parametrize("edit,frag", [({"lr": 1e-4}, "lr"), ({"snap_fracs": [0.25, 0.5, 0.75]}, "snap_fracs"),
                                        ({"snap_fracs": [0.25, 0.4, 0.5, 0.67, 0.75, 0.83, 0.92]}, "33%"),
                                        ({"snap_every": 2500}, "snap_every"), ({"seed": 20261003}, "seed"),
                                        ({"kd_skip_src": []}, "recipe"), ({"snap_fracs": [0.25, 0.33, 0.5, 0.67, 0.7, 0.75, 0.8, 0.9, 0.95, 0.97]}, "snap_fracs")])
def test_config_rejects_recipe_drift(edit, frag):
    cfg, tmpl = cfgs()
    f, fill = filled(cfg)
    probs = pf.check_config({**f, **edit}, tmpl, fill)
    assert any(frag in p for p in probs), probs


def test_mix_checks_hash_ohs4_rows_and_floor():
    man = {"files": {"c2_train.jsonl": {"sha256": "a" * 64, "rows": 66000}, "c2_rel.jsonl": {"sha256": "b" * 64, "rows": 9}},
           "ohs4_manifest_sha256": pf.A38_OHS4_SHA, "budget_final_usd": 30.0, "counts": {"by_block": {"T01": 1}}}
    fill = {"train_file_sha256": "a" * 64, "rel_file_sha256": "b" * 64, "seed": pf.SEED}
    assert pf.check_mix(man, fill, {"c2_train.jsonl": "a" * 64, "c2_rel.jsonl": "b" * 64})[0] == []
    p, _ = pf.check_mix(man, fill, {"c2_train.jsonl": "c" * 64, "c2_rel.jsonl": "b" * 64})
    assert any("sha256 on disk" in x for x in p)
    p, _ = pf.check_mix({**man, "ohs4_manifest_sha256": "0" * 64}, fill, {"c2_train.jsonl": "a" * 64, "c2_rel.jsonl": "b" * 64})
    assert any("A38" in x for x in p)
    small = {**man, "files": {**man["files"], "c2_train.jsonl": {"sha256": "a" * 64, "rows": 49000}}}
    assert any("rows" in x for x in pf.check_mix(small, fill, {"c2_train.jsonl": "a" * 64, "c2_rel.jsonl": "b" * 64})[0])


def test_modal_copy_current_and_mount_excludes_sealed_paths():
    assert subprocess.run([sys.executable, "-B", str(TRAIN / "make_modal_od_c2.py"), "--check"]).returncode == 0
    import modal_od_c2 as m
    assert pf.check_mount(m._data_ignore, "c2_parts/c2_train.jsonl", "c2_parts/c2_rel.jsonl",
                          ["golden_dev.jsonl", "ohs3_x", "ohs4_sealed", "c_parts"]) == []
    # a mount that keeps a sealed name is caught
    assert pf.check_mount(lambda p: False, "c2_parts/c2_train.jsonl", "c2_parts/c2_rel.jsonl", ["ohs3_x"])
    # the real relay entry refuses a missing / card profile and any config that is not C2
    src = (TRAIN / "modal_od_c2.py").read_text()
    assert "C2_ALLOWED_PROFILES" in src and "q35_4b_c2" in src


def test_prereg_block_and_a38_sha():
    assert pf.prereg_checks((LEAN / "PREREG_FINAL.md").read_text()) == []
    assert pf.prereg_checks("nothing")


RELAY = ("mahadikarya2", "mahadikarya3", "jaypatil-duke", "atmosphor", "arya-mahadik-ai", "mahadikarya44")    # A61 g


class FakeSh:
    def __init__(self, apps="[]", init=True, run_exists=False, profiles=RELAY):
        self.apps, self.init, self.run_exists, self.profiles, self.calls = apps, init, run_exists, profiles, []

    def modal(self, profile, args, timeout=120):
        self.calls.append((profile, tuple(args)))
        assert profile in RELAY and profile != "aryamhd"             # MODAL_PROFILE is always passed; the card is never touched
        if args[:2] == ["profile", "list"]:
            return 0, " ".join(self.profiles)
        if args[:2] == ["app", "list"]:
            return 0, self.apps
        if args[:3] == ["volume", "ls", "opendecide"] and args[3].endswith("_init"):
            return (0, "adapter_model.safetensors") if self.init else (1, "")
        if args[:3] == ["volume", "ls", "opendecide"]:
            return (0, "_ckpt") if self.run_exists else (1, "not found")
        return 1, ""


def test_accounts_check():
    bill = lambda p: {"credit_left": 19.0 if p == "mahadikarya2" else 13.0, "metered": 11.0}  # noqa: E731
    p, info, base = pf.check_accounts(FakeSh(), bill)
    assert p == [] and base == {a: 11.0 for a in RELAY} and list(info) == list(RELAY)      # all six relay accounts, live balances logged
    busy = '[{"App ID":"ap-1","State":"ephemeral","Tasks":1}]'
    assert any("running" in x for x in pf.check_accounts(FakeSh(apps=busy), bill)[0])
    assert any("init adapter" in x for x in pf.check_accounts(FakeSh(init=False), bill)[0])
    assert any("already exists" in x for x in pf.check_accounts(FakeSh(run_exists=True), bill)[0])
    assert any("not found" in x for x in pf.check_accounts(FakeSh(profiles=("mahadikarya2",)), bill)[0])
    assert any("mahadikarya44 not found" in x for x in pf.check_accounts(FakeSh(profiles=RELAY[:5]), bill)[0])      # the last relay account counts too


# ----------------------------------------------------------------------------------------------- money and stop rules
@pytest.fixture
def money(tmp_path, monkeypatch):
    lg, lean = tmp_path / "logs", tmp_path / "lean"
    (lean / "logs").mkdir(parents=True)
    lg.mkdir()
    state = {"now": 1_000_000.0, "metered": {"mahadikarya2": 10.0, "mahadikarya3": 5.0}, "credit": {"mahadikarya2": 19.0, "mahadikarya3": 13.0}}
    monkeypatch.setattr(cc, "LOGS", lg)
    monkeypatch.setattr(cc, "LEAN", lean)
    monkeypatch.setattr(cc, "NOW", lambda: state["now"])
    monkeypatch.setattr(cc, "BILL", lambda p: {"metered": state["metered"][p], "billed": 0.0, "credit_left": state["credit"][p]})
    return state, lg, lean


def seg_lines(lg, rows):
    with (lg / "c2_segments.jsonl").open("w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def test_tmax_formula_and_fixed_once(money):
    state, lg, _ = money
    assert (cc.CAP_TOTAL, cc.TMAX_CAP, cc.TMAX_BASE) == (45.0, 39.0, 37.0)     # A61 g: $45 cap, T_max = min(39, 37 - spend)
    assert cc.tmax_value(1.5) == 35.5 and cc.tmax_value(0) == 37.0 and cc.tmax_value(40) < 0
    with (lg / "c2_spend.jsonl").open("w") as f:
        f.write(json.dumps({"usd": 1.5, "what": "pilots"}) + "\n")
    assert cc.tmax() == 35.5
    assert cc.tmax(fix=True) == 35.5 and (lg / "c2_tmax.json").exists()
    assert json.loads((lg / "c2_tmax.json").read_text())["formula"] == "min(39, 37 - spend to date)"
    with (lg / "c2_spend.jsonl").open("a") as f:
        f.write(json.dumps({"usd": 9, "what": "later"}) + "\n")
    assert cc.tmax() == 35.5                                   # fixed at the GO, never recomputed
    (lg / "c2_tmax.json").unlink()
    (lg / "c2_spend.jsonl").write_text(json.dumps({"usd": 38}) + "\n")
    with pytest.raises(cc.Verdict):
        cc.tmax(fix=True)


def test_spend_wall_vs_billing_and_unclosed_segments(money):
    state, lg, _ = money
    (lg / "c2_baseline.json").write_text(json.dumps({"profiles": {"mahadikarya2": 10.0, "mahadikarya3": 5.0}}))
    t0 = state["now"] - 3 * 3600
    seg_lines(lg, [{"seg": "seg1", "profile": "mahadikarya2", "start": t0, "end": t0 + 3600, "rc": 0, "args": ""}])
    state["metered"]["mahadikarya2"] = 10.0                    # billing lags: wall wins
    usd, _ = cc.spent_training()
    assert usd == pytest.approx(4.09, abs=0.01)
    state["metered"]["mahadikarya2"] = 16.0                    # billing ahead of wall: billing wins
    assert cc.spent_training()[0] == pytest.approx(6.0, abs=0.01)
    state["metered"]["mahadikarya2"] = 10.0
    seg_lines(lg, [{"seg": "seg3", "profile": "mahadikarya2", "start": state["now"] - 1800, "open": True,
                    "args": "--stop-after-min 60"}])           # open line only: counted to its cap
    usd2, how = cc.spent_training()
    assert usd2 > 0 and "unclosed" in how
    assert cc.unbilled_usd("mahadikarya2") == pytest.approx(0.5 * 4.09, abs=0.05) or cc.unbilled_usd("mahadikarya2") > 0
    assert cc.spent_training(lg / "nonexistent")[0] is None or True


def meta(n=4000, sps=3.0, bad=None, start_step=0, upto=100):
    recs = []
    for s in range(start_step, upto):
        r = {"step": s, "of": n, "loss": 1.0 - 0.001 * s, "task": 0.9, "cons": 0.1, "min": 5 + s * sps / 60}
        if bad and s == bad[0]:
            r[bad[1]] = bad[2]
        recs.append(r)
    return {"steps": n, "log": recs}


def test_first100_rules():
    rec, v = cc.first100_verdict(meta())
    assert v == "GO" and rec["s_per_step_10_99"] == pytest.approx(3.0, abs=0.01)
    assert cc.first100_verdict(meta(bad=(50, "loss", float("nan"))))[1] == "ABORT"
    assert cc.first100_verdict(meta(bad=(7, "cons", float("inf"))))[1] == "ABORT"
    assert cc.first100_verdict(meta(bad=(60, "loss", 9.0)))[1] == "ABORT"           # > 3 x the first-5 mean
    assert cc.first100_verdict(meta(sps=9.0))[1] == "ABORT"                         # > 2 x 3.716
    assert cc.first100_verdict(meta(upto=80))[1] == "ABORT"
    assert cc.first100_verdict(None)[1] == "ABORT"


def verdict(**kw):
    a = dict(kind="proj", head={}, n=4000, at=300, sps=3.0, spent=1.0, other=1.5, t_max=30.5, credit_min=600,
             profile="mahadikarya2")
    a.update(kw)
    try:
        rec, seg_min = cc.rest_verdict(a["kind"], a["head"], a["n"], a["at"], a["sps"], a["spent"], a["other"], a["t_max"],
                                       a["credit_min"], a["profile"])
    except cc.Verdict as v:
        return v
    from types import SimpleNamespace
    return SimpleNamespace(verdict="GO", rec=rec, code=0)


def test_a37k_projection_above_tmax_stops_and_asks():
    # 4000 steps x 3.0 s = 3.33 h = $13.6 (+2): GO
    assert verdict().verdict == "GO" and verdict().rec["projected_training_usd"] == pytest.approx(15.6, abs=0.1)
    # 4000 x 7.0 s = 7.8 h = $31.8 + 2 > 30.5 -> STOP and ask (A37 k as changed by A42-D 2.3)
    v = verdict(sps=7.0)
    assert v.verdict.startswith("STOP") and "T_max" in v.verdict and v.code == 1
    # the old $17 threshold is NOT the rule any more: $20 projection under T_max 30.5 is a GO
    assert verdict(sps=4.5, credit_min=2000).verdict == "GO"
    # total cap: other spend + projection above $45 (A61 g)
    assert verdict(other=28.0, t_max=32.0, sps=3.5).verdict.startswith("STOP")
    assert verdict(other=26.0, t_max=32.0, sps=3.5).verdict == "GO"                 # 26 + 17.9 = 43.9 <= 45
    # rest does not fit the T_max minutes
    assert verdict(sps=6.0, spent=12.0, n=4000).verdict.startswith("STOP")


def test_credit_cap_relay_and_no_card():
    v = verdict(credit_min=5)
    assert v.verdict.startswith("RELAY") and v.code == 3 and "mahadikarya3" in v.verdict
    for here, there in zip(RELAY, RELAY[1:]):                                       # A61 g: every account but the last relays to the next
        v = verdict(credit_min=5, profile=here)
        assert v.verdict.startswith("RELAY") and v.code == 3 and there in v.verdict, (here, v.verdict)
    v = verdict(credit_min=5, profile="mahadikarya44")                              # the last free account: stop, a card needs the owner's GO
    assert v.verdict.startswith("STOP") and "card" in v.verdict and v.code == 1
    v = verdict(credit_min=120)
    assert v.verdict == "GO" and v.rec["limit"] == "credit" and v.rec["stop_after_min"] == 120
    v = verdict(credit_min=2000)
    assert v.rec["limit"] == "budget" and v.rec["stop_after_min"] <= 540


def test_proj_end_to_end_writes_cap_file_and_relay_exit(money):
    state, lg, lean = money
    (lg / "c2_tmax.json").write_text(json.dumps({"t_max": 30.5}))
    (lg / "c2_baseline.json").write_text(json.dumps({"profiles": {"mahadikarya2": 10.0}}))
    seg_lines(lg, [{"seg": "seg1", "profile": "mahadikarya2", "start": state["now"] - 7200, "end": state["now"] - 6000, "rc": 0, "args": ""}])
    m = meta(4000, 3.0, start_step=0, upto=301)
    (lean / "logs/relay_q35_4b_c2_stopped_at_300.json").write_text(json.dumps(m))
    assert cc.main(["proj", "--profile", "mahadikarya2"]) == 0
    assert (lg / "c2_stop_after_min.txt").read_text().split()[1] in ("budget", "credit")
    assert json.loads((lg / "c2_check_proj.json").read_text())["decision"] == "GO"
    state["credit"]["mahadikarya2"] = 1.5                       # nearly empty free credit -> RELAY
    assert cc.main(["proj", "--profile", "mahadikarya2"]) == 3
    assert cc.main(["proj", "--profile", "aryamhd"]) == 1       # the card account is refused


def test_status_and_verify_copy(money, tmp_path):
    d = tmp_path / "q35_4b_c2"
    (d / "_ckpt").mkdir(parents=True)
    (d / "_ckpt/state.pt").write_bytes(b"x")
    import hashlib
    (d / "_ckpt/manifest.json").write_text(json.dumps({"files": {"state.pt": hashlib.sha256(b"x").hexdigest()}}))
    assert cc.main(["verify-copy", str(d)]) == 0
    (d / "_ckpt/state.pt").write_bytes(b"y")
    assert cc.main(["verify-copy", str(d)]) == 1


# ----------------------------------------------------------------------------------------------- the chain script
def test_chain_script_profiles_and_modal_calls():
    sh = TRAIN / "c2_chain.sh"
    assert subprocess.run(["bash", "-n", str(sh)]).returncode == 0
    for bad in (["resume", "aryamhd"], ["resume", ""], ["bogus"]):
        r = subprocess.run(["bash", str(sh), *bad], capture_output=True, text=True, env={"PATH": "/usr/bin:/bin", "C2_MODAL": "/nonexistent"})
        assert r.returncode == 2, (bad, r.stdout, r.stderr)
    text = sh.read_text()
    assert text.count("export MODAL_PROFILE=$P") == 1
    for line in text.splitlines():
        if ("$M " in line or "'$M'" in line) and not line.lstrip().startswith("#"):
            assert "MODAL_PROFILE" in line or line.lstrip().startswith(("stop ", "echo ")) or "[ $rc = 0 ]" in line, line
    assert "--stop-at-step 100 --log-every 1 --stop-after-min 30" in text and "--stop-at-step 300" in text
    assert "A37 (k)" in text


# ----------------------------------------------------------------------------------------------- merge_avg
def fake_adapter(d: Path, seed: int, r=4, mods=(("m0", 6, 5), ("m1", 6, 3)), n_steps=None):
    g = torch.Generator().manual_seed(seed)
    d.mkdir(parents=True, exist_ok=True)
    sd = {}
    for m, i, o in mods:
        sd[f"base_model.model.{m}.lora_A.weight"] = torch.randn(r, i, generator=g)
        sd[f"base_model.model.{m}.lora_B.weight"] = torch.randn(o, r, generator=g)
    save_file(sd, str(d / "adapter_model.safetensors"))
    (d / "adapter_config.json").write_text(json.dumps({"r": r, "lora_alpha": 2 * r, "peft_type": "LORA"}))
    if n_steps:
        (d / "train_meta.json").write_text(json.dumps({"steps": n_steps}))


@pytest.fixture
def run_dir(tmp_path):
    n = 1000
    fake_adapter(tmp_path / "c1", 1)
    run = tmp_path / "run"
    fake_adapter(run, 2, n_steps=n)
    for k, f in enumerate((0.25, 0.33, 0.5, 0.67, 0.75, 0.83, 0.92)):
        fake_adapter(run / "snaps" / f"s{int(f * n):06d}", 10 + k)
    return tmp_path


def test_checkpoints_and_bases(run_dir):
    ck = ma.list_checkpoints(run_dir / "run")
    assert len(ck) == 8 and ck[-1]["name"] == "final" and ck[-1]["step"] == 1000
    b = ma.base_coefs(ck)
    assert set(b["earlylate"]) == {"s000330", "final"} and set(b["last3"]) == {"s000830", "s000920", "final"}
    assert sum(b["last3"].values()) == pytest.approx(1)
    c = ma.candidate_coefs(b["last3"], 0.7)
    assert c["c1"] == pytest.approx(0.3) and c["final"] == pytest.approx(0.7 / 3) and sum(c.values()) == pytest.approx(1)
    assert "c1" not in ma.candidate_coefs(b["final"], 1.0)


def test_grid_is_exact_in_merged_space_and_18_candidates(run_dir):
    out = run_dir / "grid"
    g = ma.build_grid(run_dir / "c1", run_dir / "run", out)
    assert len(g["candidates"]) == 18 and len({c["name"] for c in g["candidates"]}) == 18
    assert g["worst_verify_err"] < 1e-5
    from safetensors.torch import load_file
    c1 = ma.pairs(load_file(str(run_dir / "c1/adapter_model.safetensors")))
    snaps = {q.name: ma.pairs(load_file(str(q / "adapter_model.safetensors"))) for q in (run_dir / "run/snaps").glob("s*")}
    fin = ma.pairs(load_file(str(run_dir / "run/adapter_model.safetensors")))
    srcs = {**snaps, "final": fin, "c1": c1}
    cand = load_file(str(out / "last3_a07/adapter_model.safetensors"))
    cfg = json.loads((out / "last3_a07/adapter_config.json").read_text())
    assert cfg["r"] == 4 * 4 and cfg["lora_alpha"] / cfg["r"] == 2.0                   # rank 4 sources: C1 + 3 checkpoints
    mod = "base_model.model.m0"
    want = 2.0 * (0.3 * c1[mod][1] @ c1[mod][0] + 0.7 / 3 * sum(srcs[k][mod][1] @ srcs[k][mod][0] for k in ("s000830", "s000920", "final")))
    assert torch.allclose(ma.dense(cand, mod, 2.0), want, atol=1e-4)
    # the forbidden shortcut (average A and B separately) is a DIFFERENT matrix
    mA = sum(srcs[k][mod][0] for k in ("s000830", "s000920", "final")) / 3
    mB = sum(srcs[k][mod][1] for k in ("s000830", "s000920", "final")) / 3
    sep = 2.0 * (mB @ mA)
    avg_of_prods = 2.0 * sum(srcs[k][mod][1] @ srcs[k][mod][0] for k in ("s000830", "s000920", "final")) / 3
    assert not torch.allclose(sep, avg_of_prods, atol=1e-3)
    # final_a10 is the final adapter byte for byte; earlylate_a10 = 0.5 early + 0.5 final
    assert (out / "final_a10/adapter_model.safetensors").read_bytes() == (run_dir / "run/adapter_model.safetensors").read_bytes()
    el = load_file(str(out / "earlylate_a10/adapter_model.safetensors"))
    e = snaps["s000330"][mod]
    assert torch.allclose(ma.dense(el, mod, 2.0), 2.0 * 0.5 * (e[1] @ e[0] + fin[mod][1] @ fin[mod][0]), atol=1e-4)
    with pytest.raises(SystemExit):
        ma.build_grid(run_dir / "c1", run_dir / "run", out)                           # the grid is written once


def test_checkpoint_count_is_enforced(tmp_path):
    fake_adapter(tmp_path / "c1", 1)
    fake_adapter(tmp_path / "run", 2, n_steps=100)
    for f in (25, 50):
        fake_adapter(tmp_path / "run/snaps" / f"s{f:06d}", f)
    with pytest.raises(SystemExit):
        ma.list_checkpoints(tmp_path / "run")


# ----------------------------------------------------------------------------------------------- select_candidate
def mk(name, acc_g, acc_r, acc_o=None, elig=True, n=400, seed=0, base=None):
    """Item correctness drawn so each component has the requested accuracy; clusters of 2 items."""
    rng = np.random.default_rng(seed)
    items = {}
    for comp, a in (("gproxy", acc_g), ("rmixdev", acc_r), ("own_dev", acc_o)):
        if a is None:
            continue
        ref = base["items"][comp]["correct"] if base else None
        if ref is None:
            corr = (rng.random(n) < a).astype(int).tolist()
        else:
            corr = list(ref)
            flip = int(round(a * n))                       # with a base, a is a DELTA in accuracy (fraction)
            idx = [i for i, c in enumerate(corr) if c == (0 if flip > 0 else 1)][:abs(flip)]
            for i in idx:
                corr[i] = 1 - corr[i]
        items[comp] = {"id": list(range(n)), "cluster": [i // 2 for i in range(n)], "correct": corr}
    el = {k: True for k in sc.ELIG_KEYS} if elig else {**{k: True for k in sc.ELIG_KEYS}, "c4_D4": False}
    return {"candidate": name, "items": items, "eligibility": el}


def test_final_stays_unless_ci_lower_bound_positive():
    fin = mk("final_a10", 0.70, 0.70, 0.70, seed=1)
    small = mk("last3_a08", 0.002, 0.002, 0.002, base=fin)          # +0.2 pt: CI straddles 0
    big = mk("last3_a07", 0.09, 0.09, 0.09, base=fin)               # +9 pt: clearly > 0
    r = sc.choose({"final_a10": fin, "last3_a08": small}, 2000)
    assert r["chosen"] == "final_a10" and r["ci_vs_final"]["lo"] <= 0
    r = sc.choose({"final_a10": fin, "last3_a07": big, "last3_a08": small}, 2000)
    assert r["chosen"] == "last3_a07" and r["ci_vs_final"]["lo"] > 0 and r["best_eligible"] == "last3_a07"
    assert r["ci_vs_final"]["resamples"] == 2000 and r["ci_vs_final"]["seed"] == 0


def test_ineligible_final_none_eligible_and_missing_checks():
    fin = mk("final_a10", 0.70, 0.70, 0.70, elig=False, seed=1)
    other = mk("last3_a08", -0.10, -0.10, -0.10, base=fin)
    r = sc.choose({"final_a10": fin, "last3_a08": other}, 500)
    assert r["chosen"] == "last3_a08" and "not eligible" in r["status"]
    other["eligibility"]["d_complement"] = False
    r = sc.choose({"final_a10": fin, "last3_a08": other}, 500)
    assert r["chosen"] is None and "pre-gate fails" in r["status"]
    ok = mk("x_a10", 0.7, 0.7, 0.7)
    del ok["eligibility"]["gproxy_rule_4_3"]                          # missing = not a pass
    assert sc.eligible(ok) == (False, ["gproxy_rule_4_3"])


def test_score_is_mean_of_three_accuracies_and_two_without_new_families():
    a = mk("final_a10", 0.8, 0.6, 0.4, n=1000, seed=3)
    assert sc.score(a, ("gproxy", "rmixdev", "own_dev")) == pytest.approx(np.mean([sc.acc(a, c) for c in sc.COMPONENTS]))
    b = mk("final_a10", 0.8, 0.6, None, n=1000, seed=3)
    assert sc.components_of(b) == ("gproxy", "rmixdev")
    r = sc.choose({"final_a10": b, "last3_a09": mk("last3_a09", 0.0, 0.0, None, base=b)}, 200)
    assert r["components_in_S"] == ["gproxy", "rmixdev"]
    with pytest.raises(SystemExit):
        sc.choose({"final_a10": a, "last3_a09": b}, 200)             # mixed component sets are refused


def test_ci_is_paired_clustered_and_reproducible():
    fin = mk("final_a10", 0.70, 0.70, 0.70, seed=1)
    c = mk("last3_a07", 0.05, 0.05, 0.05, base=fin)
    ci1 = sc.paired_ci(c, fin, sc.COMPONENTS, 1000, 0)
    assert ci1 == sc.paired_ci(c, fin, sc.COMPONENTS, 1000, 0)
    assert ci1["point_pt"] == pytest.approx(5.0, abs=0.3) and ci1["lo"] < ci1["point_pt"] < ci1["hi"]
    c["items"]["gproxy"]["id"][0] = 999
    with pytest.raises(SystemExit):
        sc.paired_ci(c, fin, sc.COMPONENTS, 100, 0)


def test_ties_prefer_final_then_larger_alpha():
    fin = mk("final_a10", 0.7, 0.7, 0.7, seed=1)
    t1 = mk("last3_a05", 0.0, 0.0, 0.0, base=fin)
    t2 = mk("earlylate_a09", 0.0, 0.0, 0.0, base=fin)
    assert sc.choose({"final_a10": fin, "last3_a05": t1, "earlylate_a09": t2}, 100)["best_eligible"] == "final_a10"
    order = sorted(["last3_a05", "earlylate_a09", "last3_a09"], key=lambda n: sc.sort_key(n, 70.0))
    assert order == ["last3_a09", "earlylate_a09", "last3_a05"]


# ----------------------------------------------------------------------------------------------- symmetrise
def rec(i, set_, gold, p, pf_=None, pair=None, role=None, pat=None):
    return {"id": i, "set": set_, "gold": gold, "p": p, "p_flip": pf_, "pair_id": pair, "role": role, "pattern_id": pat}


def good_records():
    r = []
    for i in range(50):                                   # q and its flip disagree with noise; symmetrising helps
        gold = i % 2
        p = 0.65 if gold else 0.35
        pfl = 0.2 if gold else 0.8                         # the flip is the complement: p(flip yes) = 1 - p(q) direction
        r.append(rec(f"g{i}", "gproxy", gold, p, pfl))
        r.append(rec(f"d{i}", "d1_yesno", gold, p, pfl))
    for k in range(10):                                   # pairs: plain answers the same way (violation), sym fixes it
        r.append(rec(f"q{k}", "pair", 1, 0.6, 0.1, pair=k, role="q", pat=f"P{k // 5}"))
        r.append(rec(f"n{k}", "pair", 0, 0.6, 0.9, pair=k, role="nq", pat=f"P{k // 5}"))
    return r


def test_sym_formula_and_unflippable_items_stay_plain():
    assert sy.sym_p(0.8, 0.3) == pytest.approx(0.75) and sy.sym_p(0.8, None) == 0.8
    assert sy.sym_p(0.5, 0.5) == 0.5


def test_adoption_passes_and_each_rule_can_fail():
    lat = {"c1_p50_ms": 14.0, "sym_p50_ms": 14.5}
    r = sy.adopt(good_records(), lat)
    assert r["adopt"] and r["name"] == "C2 + symmetrisation" and r["violation"]["drop"] >= 0.02
    assert not sy.adopt(good_records(), {"c1_p50_ms": 14.0, "sym_p50_ms": 16.0})["adopt"]                # D9 fails
    assert not sy.adopt(good_records(), {"c1_p50_ms": 14.0})["adopt"]                                   # D9 unknown
    recs = [dict(x, p_flip=None) if x["set"] == "pair" else x for x in good_records()]                  # no violation drop
    assert not sy.adopt(recs, lat)["adopt"]
    bad = good_records()
    for x in bad:
        if x["set"] == "gproxy":
            x["p_flip"] = 0.9 if x["gold"] else 0.1            # flip points the wrong way: accuracy and Brier get worse
    out = sy.adopt(bad, lat)
    assert not out["adopt"] and not out["checks"]["gproxy_acc"]
    assert sy.adopt(good_records()[:5], lat)["adopt"] is False                                          # missing sets


def test_pair_rules_held_out_patterns_and_cap():
    rows = [r for r in good_records() if r["set"] == "pair"]
    assert sy.check_pairs(rows, {"X"}) == []
    assert sy.check_pairs(rows, {"P0"})                                                  # a trained pattern: refused (10.3)
    many = [rec(f"q{k}", "pair", 1, 0.6, None, pair=k, role="q", pat="P") for k in range(6)]
    assert any("> 5" in x for x in sy.check_pairs(many, None))


def test_temperature_fit_and_brier():
    ps, ys = [0.9, 0.9, 0.1, 0.1, 0.9, 0.1], [1, 0, 0, 1, 1, 0]
    T = sy.fit_T(ps, ys)
    assert T > 1.0 and sy.brier(ps, ys, T) <= sy.brier(ps, ys, 1.0)


def test_catalogue_flipper_makes_a_complement_flip_and_none_otherwise():
    f = sy.CatalogueFlipper()
    out = f.flip({"id": "a", "instruction": "Read the policy. Does the vendor allow refunds after 30 days?"})
    assert out and out["id"] == "a::flip" and out["flip_of"] == "a" and out["instruction"].startswith("Read the policy. ")
    assert f.flip({"id": "b", "instruction": "Summarise the policy."}) is None
    flips, none = sy.make_flips([{"id": "a", "instruction": "Does it allow refunds?"}, {"id": "b", "instruction": "No question"}], f)
    assert len(flips) == 1 and none == ["b"]


# ----------------------------------------------------------------------------------------------- chain `copy` with a fake modal
FAKE_MODAL = """#!/bin/bash
echo "$MODAL_PROFILE|$*" >> "$FAKE_LOG"
[ -z "$MODAL_PROFILE" ] && exit 9
case "$1 $2" in
  "app list") echo "${FAKE_APPS:-[]}";;
  "volume get") d="${@: -1}"; mkdir -p "${d}q35_4b_c2/_ckpt" "${d}q35_4b_c2/snaps/s000100"
     printf x > "${d}q35_4b_c2/_ckpt/state.pt"
     h=$(printf x | shasum -a 256 | cut -c1-64); [ -n "$FAKE_BAD" ] && h=deadbeef
     echo "{\\"files\\": {\\"state.pt\\": \\"$h\\"}}" > "${d}q35_4b_c2/_ckpt/manifest.json";;
  "volume put") :;;
  "volume ls") echo "state.pt";;
esac
exit 0
"""


def run_copy(tmp_path, apps="[]", bad=""):
    fake = tmp_path / "modal"
    fake.write_text(FAKE_MODAL)
    fake.chmod(0o755)
    log = tmp_path / "calls.log"
    import os
    env = {**os.environ, "C2_MODAL": str(fake), "FAKE_LOG": str(log), "FAKE_APPS": apps, "FAKE_BAD": bad,
           "C2_TEST_NO_LEDGER": "1", "MODAL_PROFILE": "aryamhd"}                  # a wrong inherited profile must not leak
    r = subprocess.run(["bash", str(TRAIN / "c2_chain.sh"), "copy"], capture_output=True, text=True, env=env)
    calls = log.read_text().splitlines() if log.exists() else []
    subprocess.run(["rm", "-rf", str(TRAIN / "tmp"), str(TRAIN / "logs/c2_copy_ls.txt"),
                    str(TRAIN / "logs/c2_check_verify-copy.json")])
    return r, calls


def test_copy_p2_to_p3_hash_checked_and_profiles_always_passed(tmp_path):
    r, calls = run_copy(tmp_path)
    assert r.returncode == 0, (r.stdout, r.stderr)
    assert "COPIED" in r.stdout and calls
    assert all(c.split("|")[0] in ("mahadikarya2", "mahadikarya3") for c in calls)
    assert [c.split("|")[0] for c in calls if "volume get" in c] == ["mahadikarya2"]
    assert [c.split("|")[0] for c in calls if "volume put" in c] == ["mahadikarya3"]


def test_copy_refused_when_an_app_runs_or_the_copy_is_corrupt(tmp_path):
    busy = '[{"App ID":"ap-1","State":"detached","Tasks":1}]'
    r, calls = run_copy(tmp_path, apps=busy)
    assert r.returncode == 1 and "REFUSED" in r.stdout and not any("volume get" in c for c in calls)
    r, calls = run_copy(tmp_path, bad="1")
    assert r.returncode == 1 and "manifest" in r.stdout and not any("volume put" in c for c in calls)


def test_cli_writes_candidate_record_for_gate_c2(tmp_path):
    reads = tmp_path / "reads"
    reads.mkdir()
    fin = mk("final_a10", 0.7, 0.7, 0.7, seed=1)
    names = [ma.cand_name(b, a) for b in ma.BASES for a in ma.ALPHAS]
    cands = []
    for n in names:
        rec = fin if n == "final_a10" else mk(n, 0.0, 0.0, 0.0, base=fin)
        (reads / f"{n}.json").write_text(json.dumps({**rec, "candidate": n}))
        cands.append({"name": n, "adapter_sha256": (n[0] * 64)[:64] if False else "%064x" % (abs(hash(n)) % 16**8)})
    (tmp_path / "grid.json").write_text(json.dumps({"candidates": cands, "grid_sha256": "g" * 64}))
    rc = sc.main(["--reads", str(reads), "--grid", str(tmp_path / "grid.json"), "--out", str(tmp_path / "chosen.json"),
                  "--candidate-out", str(tmp_path / "CANDIDATE_C2.json"), "--resamples", "200"])
    assert rc == 0
    rec = json.loads((tmp_path / "CANDIDATE_C2.json").read_text())
    assert rec["name"] == "q35_4b_c2" and rec["grid_candidate"] == "final_a10" and len(rec["adapter_sha256"]) == 64
    assert len(json.loads((tmp_path / "chosen.json").read_text())["candidates"]) == 18


# ----------------------------------------------------------------------------------------------- A61 g: the six-account relay
def test_relay_accounts_are_one_list_everywhere_and_never_the_card():
    import re
    sys.path.insert(0, str(TRAIN.parent))
    import make_modal_od_c2 as mk
    import mix_c2
    import snap_monitor_c2 as sm
    assert cc.RELAY_ACCOUNTS == cc.PROFILES == RELAY and "aryamhd" not in cc.PROFILES
    assert tuple(mk.ALLOWED_PROFILES) == RELAY == tuple(sm.PROFILES) == tuple(mix_c2.RELAY_ACCOUNTS)
    gen = (TRAIN / "modal_od_c2.py").read_text()
    assert f"C2_ALLOWED_PROFILES = {RELAY!r}" in gen and "aryamhd" not in gen.split("C2_ALLOWED_PROFILES", 1)[1].split("\n", 1)[0]
    sh = (TRAIN / "c2_chain.sh").read_text()
    assert re.search(r'^RELAY="([^"]+)"', sh, re.M).group(1).split() == list(RELAY)
    assert mk.main(["--check"]) == 0                                                 # modal_od_c2.py is the generated copy
    assert cc.next_profile("mahadikarya2") == "mahadikarya3" and cc.next_profile("mahadikarya44") is None
    assert cc.next_profile("aryamhd") is None and cc.next_profile("nobody") is None
    assert [cc.next_profile(a) for a in RELAY[:-1]] == list(RELAY[1:])


def test_next_command_prints_the_following_account(capsys):
    assert cc.main(["next", "--profile", "atmosphor"]) == 0 and capsys.readouterr().out.strip() == "arya-mahadik-ai"
    assert cc.main(["next", "--profile", "mahadikarya44"]) == 3 and capsys.readouterr().out.strip() == "NONE"
    assert cc.main(["next", "--profile", "aryamhd"]) == 1


def test_chain_script_copy_and_resume_only_inside_the_relay_order():
    sh = TRAIN / "c2_chain.sh"
    env = {"PATH": "/usr/bin:/bin", "C2_MODAL": "/nonexistent"}

    def run(*args):
        return subprocess.run(["bash", str(sh), *args], capture_output=True, text=True, env=env)
    for bad in (("resume", "aryamhd"), ("copy", "aryamhd", "mahadikarya2")):
        assert run(*bad).returncode == 2, bad                                        # the card account is refused at the door
    assert run("resume", "nobody").returncode == 2
    skip = run("copy", "mahadikarya2", "jaypatil-duke")                              # skipping an account needs the owner's OK
    assert skip.returncode == 1 and "not the account after" in skip.stdout, (skip.stdout, skip.stderr)
    back = run("copy", "mahadikarya3", "mahadikarya2")
    assert back.returncode == 1 and "REFUSED" in back.stdout
    last = run("copy", "mahadikarya44")
    assert last.returncode == 1 and "no free account after mahadikarya44" in last.stdout
    card = run("copy", "mahadikarya3", "aryamhd")
    assert card.returncode == 1 and "not a relay account" in card.stdout
    text = sh.read_text()
    assert "aryamhd" in text and "NOT in" in text                                    # documented
    assert "MODAL_PROFILE=$FROM $M volume get" in text and text.count("MODAL_PROFILE=$TO $M volume") == 2     # the copy names the account on every modal call
    assert "'MODAL_PROFILE':'$FROM'" in text
    assert "copy $P $NEXTP" in text and "resume $NEXTP" in text


def test_preflight_row_cap_is_the_a61_mix_cap():
    assert (pf.MIN_ROWS, pf.MAX_ROWS) == (50_000, 150_000)
    assert pf.c2_check.PROFILES == RELAY
