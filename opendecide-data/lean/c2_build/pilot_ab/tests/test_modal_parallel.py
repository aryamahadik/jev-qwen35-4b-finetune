"""CPU tests for modal_parallel.py (no GPU, no Modal call, no network, no sealed path).
Run from lean/c2_build:  nice -n 10 ../../.venv/bin/python -B -m pytest -q -p no:cacheprovider pilot_ab/tests/test_modal_parallel.py
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
PAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PAB))
import common as C  # noqa: E402
import modal_parallel as MP  # noqa: E402

FAM = "T40"
NOW = 1_800_000_000.0


# ------------------------------------------------------------------------------------------------------------ helpers
def pilot(state="done", usd=None, est=0.55, pess=0.79, start=None, spawn=NOW - 60, smoke=False):
    p = {"state": state, "name": "x", "call_id": "fc-1", "run_id": "r", "spawn_unix": spawn, "est_usd": est, "pess_usd": pess,
         "smoke": smoke, "files": [], "timeout_s": MP.TIMEOUT_S}
    if usd is not None:
        p["usd"] = usd
    if start is not None:
        p["hb_start_unix"] = start
    return p


def ledger(pilots=None, other=0.0):
    led = MP.new_ledger()
    led["other_spend"] = [{"what": "x", "usd": other}] if other else []
    led["pilots"] = pilots or {}
    return led


# ------------------------------------------------------------------------------------------------------------ account
@pytest.mark.parametrize("prof", ["", "mahadikarya2", "mahadikarya3", "aryamhd", "atmosphor", "mahadikarya4"])
def test_only_mahadikarya44_is_accepted(monkeypatch, prof):
    monkeypatch.setenv("MODAL_PROFILE", prof)
    with pytest.raises(MP.Refuse) as e:
        MP.check_profile()
    assert "mahadikarya44" in str(e.value)


def test_token_env_override_is_refused(monkeypatch):
    monkeypatch.setenv("MODAL_PROFILE", "mahadikarya44")
    monkeypatch.setenv("MODAL_TOKEN_ID", "ak-x")
    with pytest.raises(MP.Refuse) as e:
        MP.check_profile()
    assert "MODAL_TOKEN_ID" in str(e.value)


def test_constants_match_the_harness_and_the_cap():
    assert MP.PROFILE == "mahadikarya44" and MP.CAP_USD == 3.50 and MP.GPU == "H100!" and MP.MAX_PARALLEL == 6
    assert MP.FAMILIES == C.FAMILIES and MP.C1_ADAPTER_SHA == C.C1_ADAPTER_SHA and MP.SEED == C.SEED == 20261013
    assert MP.RATE_H >= MP.LIST_H100_H and MP.TIMEOUT_S <= 30 * 60
    src = (PAB / "modal_parallel.py").read_text()
    decos = [l for l in src.splitlines() if l.startswith("@app.function(")]
    assert len(decos) == 3 and any("gpu=GPU" in l for l in decos) and not any("retries" in l for l in decos)
    vline = [l for l in src.splitlines() if l.startswith("vol = modal.Volume.from_name(")]
    assert len(vline) == 1 and "create_if_missing=" not in vline[0].split("#")[0]                   # never creates an empty volume
    assert "FN = dict(" in src and "scaledown_window=SCALEDOWN_S" in src


def test_never_open_paths_are_refused(tmp_path):
    for bad in ("/x/ohs3/y", "/x/OHS_ac_sealed", "/x/c_spec/sealed_brief", "/x/c_build/preread", "/a/bench/longbench_v2/b",
                "/home/u/.claude/z", "/private/tmp/claude/x", "/x/bench/external_quarantine/a"):
        with pytest.raises(MP.Refuse):
            MP.refuse_path(bad)
    assert MP.refuse_path(tmp_path) == str(tmp_path)
    with pytest.raises(MP.Refuse):
        MP.main(["--root", "/x/ohs/y", "status"])


# ------------------------------------------------------------------------------------------------------------ the guard
def test_guard_launches_what_fits_and_defers_the_rest():
    led = ledger(other=0.0088)
    cands = [(f, 0.79) for f in MP.FAMILIES]
    plan = MP.plan_launch(led, cands, now=NOW)
    assert [f for f, _ in plan["launch"]] == ["T40", "T41", "T42", "T43"]        # 4 x 0.79 + 0.0088 = 3.17; the 5th would be 3.96
    assert [f for f, _ in plan["deferred"]] == ["T44", "T45"] and plan["committed_after"] <= MP.CAP_USD
    assert "cap" in plan["deferred"][0][1]


def test_guard_boundary_is_inclusive_and_never_exceeds_the_cap():
    plan = MP.plan_launch(ledger(), [("T40", 1.75), ("T41", 1.75), ("T42", 0.01)], now=NOW)
    assert [f for f, _ in plan["launch"]] == ["T40", "T41"] and plan["committed_after"] == 3.5
    assert [f for f, _ in plan["deferred"]] == ["T42"]
    for pess in (0.3, 0.55, 0.79, 1.1):
        pl = MP.plan_launch(ledger(other=0.2), [(f, pess) for f in MP.FAMILIES], now=NOW)
        assert pl["committed_after"] <= MP.CAP_USD + 1e-9


def test_running_pilots_are_reserved_at_their_pessimistic_cost_and_finished_ones_at_actual():
    led = ledger({"T40": pilot("done", usd=0.50), "T41": pilot("running", start=NOW - 120),
                  "T42": pilot("spawned", spawn=NOW - 10)}, other=0.01)
    assert MP.committed_usd(led, NOW) == pytest.approx(0.01 + 0.50 + 0.79 + 0.79)
    # a running pilot that already cost more than its reservation is held at the observed cost
    led["pilots"]["T41"]["hb_start_unix"] = NOW - 1500
    assert MP.pilot_reserved_usd(led["pilots"]["T41"], NOW) == pytest.approx(MP.usd(1500 + MP.BOOT_S + MP.SCALEDOWN_S))
    # a finished-pilot record with no usd (should not happen) is still charged for its elapsed time, never for nothing
    p = pilot("failed", start=NOW - 300)
    p["end_unix"] = NOW - 100
    assert MP.pilot_observed_usd(p, NOW) == pytest.approx(MP.usd(200 + MP.BOOT_S + MP.SCALEDOWN_S))


def test_parallel_limit_and_waves():
    led = ledger({f"T4{i}": pilot("running", start=NOW - 5, pess=0.2) for i in range(5)})
    plan = MP.plan_launch(led, [("T45", 0.2), ("T40", 0.2)], now=NOW)
    assert [f for f, _ in plan["launch"]] == ["T45"] and "parallel" in plan["deferred"][0][1]


def test_calibration_uses_real_evidence_only_downwards_bounded():
    est = {"usd": 0.55, "pess_usd": 0.79}
    assert MP.calibrate_pess(ledger(), est) == 0.79                                # no evidence: a-priori pessimism
    led = ledger({"T40": pilot("done", usd=0.50), "T41": pilot("done", usd=0.52)})
    c = MP.calibrate_pess(led, est)
    assert 0.55 * 1.05 <= c < 0.79 and c == pytest.approx(0.55 * 0.9 * 1.15 if 0.51 / 0.55 < 0.9 else 0.55 * (1.02 / 1.10) * 1.15, abs=0.01)
    led = ledger({"T40": pilot("done", usd=0.90)})                                  # dearer than estimated: capped at the a-priori value
    assert MP.calibrate_pess(led, est) == 0.79
    led = ledger({"T40": pilot("done", usd=0.01, smoke=True)})                      # smoke records never count as evidence
    assert MP.calibrate_pess(led, est) == 0.79


def test_hard_stop_threshold_leaves_room_for_one_poll():
    assert MP.hard_stop_at(0, 10) == pytest.approx(3.40)
    assert MP.hard_stop_at(6, 10) == pytest.approx(3.40 - 6 * MP.usd(10)) and MP.hard_stop_at(6, 10) < 3.40


def test_observed_cost_counts_from_the_container_start_not_the_queue():
    q = pilot("spawned", spawn=NOW - 100)                       # queued 100 s: not billed
    assert MP.pilot_observed_usd(q, NOW) == 0.0
    q = pilot("spawned", spawn=NOW - 400)                       # no heartbeat for 400 s: assume billed since the spawn
    assert MP.pilot_observed_usd(q, NOW) == pytest.approx(MP.usd(400 + MP.BOOT_S + MP.SCALEDOWN_S))
    r = pilot("running", start=NOW - 480, spawn=NOW - 900)
    assert MP.pilot_observed_usd(r, NOW) == pytest.approx(MP.usd(480 + MP.BOOT_S + MP.SCALEDOWN_S))


def _watch_args(tmp_path, **kw):
    return argparse.Namespace(root=str(tmp_path), smoke=False, poll=0.01, no_pull=True, no_stop=True, backups=str(tmp_path / "bk"), **kw)


def test_watch_hard_stop_cancels_everything_at_the_cap(tmp_path, monkeypatch):
    now = time.time()
    led = ledger({f: pilot("running", start=now - 600, spawn=now - 700) for f in MP.FAMILIES})    # 6 x 10.5 min = 4.3 USD
    p = MP.ledger_path(tmp_path)
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps(led))
    called = []
    monkeypatch.setattr(MP, "check_profile", lambda: None)
    monkeypatch.setattr(MP, "poll_pilot", lambda *a, **k: None)
    monkeypatch.setattr(MP.modal.Dict, "from_name", lambda *a, **k: None)
    monkeypatch.setattr(MP, "abort_all", lambda root, smoke, why: called.append(why))
    assert MP.cmd_watch(_watch_args(tmp_path)) == 3 and called and "hard stop" in called[0]


def test_watch_runs_to_the_end_under_the_cap_and_stops_nothing_early(tmp_path, monkeypatch):
    now = time.time()
    led = ledger({"T40": pilot("done", usd=0.5), "T41": pilot("running", start=now - 30, spawn=now - 60)})
    p = MP.ledger_path(tmp_path)
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps(led))
    calls = []

    def fake_poll(f, pl, hb, n, rate, smoke):
        calls.append(f)
        if len(calls) >= 2:
            pl.update(state="done", usd=0.52, wall_s=480.0)
    monkeypatch.setattr(MP, "check_profile", lambda: None)
    monkeypatch.setattr(MP, "poll_pilot", fake_poll)
    monkeypatch.setattr(MP.modal.Dict, "from_name", lambda *a, **k: None)
    monkeypatch.setattr(MP, "abort_all", lambda *a: pytest.fail("must not abort"))
    assert MP.cmd_watch(_watch_args(tmp_path)) == 0
    led2 = json.loads(p.read_text())
    assert led2["pilots"]["T41"]["state"] == "done" and led2["summary"]["observed_usd"] == pytest.approx(1.02)


def test_ledger_is_written_even_when_the_body_raises(tmp_path):
    with pytest.raises(RuntimeError):
        with MP.locked_ledger(tmp_path) as led:
            led["pilots"]["T40"] = pilot("spawned")
            raise RuntimeError("spawn of the next pilot failed")
    assert json.loads(MP.ledger_path(tmp_path).read_text())["pilots"]["T40"]["state"] == "spawned"


# ------------------------------------------------------------------------------------------------------------ polling errors
class _Hb:
    def __init__(self, state):
        self.state = state

    def get(self, k):
        return None


def test_poll_error_classification():
    he_failed = {"state": "failed", "t": 1.0, "wall_s": 12.0}
    assert MP.classify_poll_error(TimeoutError(), None, None)[0] == "pending"                       # get(timeout=) not ready
    assert MP.classify_poll_error(MP.modal.exception.FunctionTimeoutError("x"), None, None)[0] == "terminal"
    assert MP.classify_poll_error(RuntimeError("remote"), he_failed, None)[0] == "terminal"          # container wrote 'failed'
    k, st = MP.classify_poll_error(ConnectionError("blip"), None, None)
    assert k == "transient"
    k, st = MP.classify_poll_error(ConnectionError("blip"), None, st)
    assert k == "transient"
    k, st = MP.classify_poll_error(ConnectionError("blip"), None, st)
    assert k == "terminal"                                                                           # same error 3 polls in a row
    assert MP.classify_poll_error(ValueError("a"), None, (("ValueError", "b"), 5))[0] == "transient"  # a different error resets
    assert MP.classify_poll_error(MP.modal.exception.InputCancellation(), None, None)[0] == "terminal"


# ------------------------------------------------------------------------------------------------------------ estimate
def test_cost_model_matches_the_harness_and_the_cap_story():
    c = MP.cost_from(740 * MP.PADDED_PER_MEAN_TOKEN)
    assert c["steps"] == 94 and 7.5 < c["minutes"] < 8.6 and 0.50 < c["usd"] < 0.60 and c["pess_usd"] > c["usd"] * 1.3
    sc = {r["mean_row_tokens"]: r for r in MP.scenario_table()}
    assert sc[800]["six_pilots_usd"] <= 3.5 < sc[917]["six_pilots_usd"] + 0.3                         # the cap is tight at the 800 bar
    assert sc[500]["usd"] < sc[740]["usd"] < sc[917]["usd"]
    # calibration run of 16 Oct: 0.163 ms/padded token predicted 110.5 min for the 106.92-min round-1 run
    assert 0.95 < 106.92 / 110.5 < 1.0


def test_padded_projection_is_a_multiple_of_the_pad_and_covers_the_twins():
    import json as _j
    rows = []
    with open(C.LEAN / "data/c_parts/c_train_r1.jsonl") as f:
        for i, l in enumerate(f):
            if i >= 400:
                break
            rows.append(_j.loads(l))
    ids = {r["id"] for r in rows}
    rels = [x for x in C.read_jsonl(C.LEAN / "data/c_parts/c_rel_r1.jsonl") if x["a"] in ids and x["b"] in ids]
    ntok = {r["id"]: 500 for r in rows}
    pr = MP.padded_projection(rows, rels, ntok, 10)
    assert round(pr["padded_per_step"] * 10) % pr["pad_multiple"] == 0 and pr["padded_per_step"] >= 16 * 512
    assert round(pr["real_per_step"] * 10) % 500 == 0 and pr["real_per_step"] >= 500 * 16 and pr["twins_per_step"] > 0   # twins are counted


# ------------------------------------------------------------------------------------------------------------ staging
def fake_stage(root: Path, fam=FAM, n=1500, start=0):
    import make_config as M
    rows = []
    with open(C.LEAN / "data/c_parts/c_train_r1.jsonl") as f:
        for i, l in enumerate(f):
            if i >= start + n:
                break
            if i >= start:
                rows.append(json.loads(l))
    ids = {r["id"] for r in rows}
    rels = [x for x in C.read_jsonl(C.LEAN / "data/c_parts/c_rel_r1.jsonl") if x["a"] in ids and x["b"] in ids]
    (root / "r.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (root / "l.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    return M.stage(fam, root / "r.jsonl", root / "l.jsonl", out_root=root, quiet=True)


def test_load_family_checks_config_files_and_hashes(tmp_path):
    import train_decoder as td
    info = fake_stage(tmp_path)
    fi = MP.load_family(tmp_path, FAM)
    assert fi["name"] == "q35_4b_pab_T40" and fi["cfg"]["seed"] == 20261013 and fi["steps"] == info["steps"]
    assert fi["cfg"]["no_overwrite"] is True and fi["cfg"]["expect_resume"] is False and fi["cfg"]["stop_at_step"] == 0
    assert fi["cfg"]["targets"] == MP.modal_od.QWEN35_TARGETS and not (set(fi["cfg"]) - td.KNOWN_KEYS)
    import zlib
    assert zlib.decompress(fi["blob"]["train"]) == (tmp_path / "stage" / FAM / C.TRAIN_FILE).read_bytes()
    assert fi["blob"]["train_sha"] == info["train_sha256"]
    # a staged file changed after make_config
    with open(tmp_path / "stage" / FAM / C.TRAIN_FILE, "a") as f:
        f.write("\n")
    with pytest.raises(MP.Refuse):
        MP.load_family(tmp_path, FAM)


def test_load_family_refuses_other_content_wrong_config_and_missing(tmp_path):
    fake_stage(tmp_path)
    (tmp_path / "stage" / FAM / "dev.jsonl").write_text("x")
    with pytest.raises(MP.Refuse):
        MP.load_family(tmp_path, FAM)
    (tmp_path / "stage" / FAM / "dev.jsonl").unlink()
    cfgp = tmp_path / "configs" / f"{FAM}.json"
    cfg = json.loads(cfgp.read_text())
    for k, v in (("seed", 1), ("init_adapter", "/vol/models/q35_4b_main500k"), ("name", "q35_4b_pab_T41")):
        bad = dict(cfg, **{k: v})
        cfgp.write_text(json.dumps(bad))
        with pytest.raises(MP.Refuse):
            MP.load_family(tmp_path, FAM)
    cfgp.write_text(json.dumps({kk: vv for kk, vv in cfg.items() if kk != "lr"}))
    with pytest.raises(MP.Refuse):
        MP.load_family(tmp_path, FAM)
    with pytest.raises(MP.Refuse):
        MP.load_family(tmp_path, "T41")                                                              # not staged


def _patch_world(monkeypatch, on_vol=(), credit=4.69, orphan=(), est_pess=0.79):
    monkeypatch.setattr(MP, "check_profile", lambda: None)
    monkeypatch.setattr(MP, "volume_names", lambda: set(on_vol))
    monkeypatch.setattr(MP, "billing_state", lambda: {"credit_left_usd": credit, "credits_used_usd": 30 - credit, "billed_cost_usd": 0.0,
                                                       "metered_cost_usd": 1.0, "today_by_app": []})
    monkeypatch.setattr(MP, "orphans", lambda led: list(orphan))
    monkeypatch.setattr(MP, "estimate_family", lambda root, f: {"fam": f, "staged": True, "usd": round(est_pess / 1.44, 3),
                                                                 "pess_usd": est_pess, "minutes": 8.0, "minutes_pess": 11.0})


def _decide_args(tmp_path, fams=",".join(MP.FAMILIES), **kw):
    return argparse.Namespace(root=str(tmp_path), families=fams, retry_failed=False, smoke=False, go=False, strict=False,
                              smoke_sleep=1.0, **kw)


def test_decide_refuses_repilot_overwrite_verdict_and_orphans(tmp_path, monkeypatch):
    for f in ("T40", "T41", "T42"):
        fake_stage(tmp_path, f, start=0)
    _patch_world(monkeypatch, on_vol={"q35_4b_pab_T41"})
    led = MP.new_ledger()
    led["pilots"]["T40"] = pilot("done", usd=0.5)
    MP.ledger_path(tmp_path).parent.mkdir(parents=True)
    MP.ledger_path(tmp_path).write_text(json.dumps(led))
    d = MP.decide(_decide_args(tmp_path, "T40,T41,T42"))
    why = dict(d["notes"])
    assert "no re-pilot" in why["T40"] and "already on the volume" in why["T41"] and [f for f, _ in d["plan"]["launch"]] == ["T42"]
    # a family that was cancelled can be retried only with --retry-failed
    led["pilots"]["T42"] = pilot("cancelled", usd=0.1)
    MP.ledger_path(tmp_path).write_text(json.dumps(led))
    assert "T42" in dict(MP.decide(_decide_args(tmp_path, "T42"))["notes"])
    a = _decide_args(tmp_path, "T42")
    a.retry_failed = True
    assert [f for f, _ in MP.decide(a)["plan"]["launch"]] == ["T42"]


def test_launch_is_a_dry_run_without_go_and_refuses_on_credit_orphans_and_strict(tmp_path, monkeypatch, capsys):
    for i, f in enumerate(MP.FAMILIES):
        fake_stage(tmp_path, f, start=0)
    _patch_world(monkeypatch)
    spawned = []
    monkeypatch.setattr(MP.train_pilot, "spawn", lambda *a, **k: spawned.append(a), raising=False)
    a = _decide_args(tmp_path)
    assert MP.cmd_launch(a) == 0 and not spawned and "dry run" in capsys.readouterr().out          # no --go: nothing spawned
    a.strict = True
    assert MP.cmd_launch(a) == 2                                                                      # 6 x 0.79 > 3.5: strict refuses
    a.strict = False
    _patch_world(monkeypatch, credit=1.0)
    assert MP.cmd_launch(a) == 2 and not spawned                                                      # free credit does not cover 3.2
    _patch_world(monkeypatch, orphan=["ap-zzz"])
    assert MP.cmd_launch(a) == 2 and not spawned
    capsys.readouterr()


def test_decide_plan_defers_the_last_pilots_at_a_priori_pessimism(tmp_path, monkeypatch):
    for f in MP.FAMILIES:
        fake_stage(tmp_path, f, start=0)
    _patch_world(monkeypatch)
    d = MP.decide(_decide_args(tmp_path))
    assert [f for f, _ in d["plan"]["launch"]] == ["T40", "T41", "T42", "T43"] and d["credit_ok"] and not d["notes"]
    assert [f for f, _ in d["plan"]["deferred"]] == ["T44", "T45"]
    # cheaper pilots (short rows): all six fit at once
    _patch_world(monkeypatch, est_pess=0.55)
    d = MP.decide(_decide_args(tmp_path))
    assert len(d["plan"]["launch"]) == 6 and d["plan"]["committed_after"] == pytest.approx(3.3)


def test_pull_paths_are_the_harness_paths():
    # l4_reads.sh fetch: BK/q35_4b_pab_<FAM>/<FILES>
    fetch = [l for l in (PAB / "l4_reads.sh").read_text().splitlines() if l.startswith('FILES="')][0]
    files = fetch.split('"')[1].split()
    assert tuple(files) == MP.RESULT_FILES
    assert str(MP.BACKUPS).endswith("backups/modal_models") and C.pilot_name("T40") == "q35_4b_pab_T40"

def test_paid_launch_needs_a_recent_passing_preflight(tmp_path, monkeypatch, capsys):
    for f in ("T40", "T41"):
        fake_stage(tmp_path, f)
    _patch_world(monkeypatch)
    spawned = []
    monkeypatch.setattr(MP.train_pilot, "spawn", lambda *a, **k: spawned.append(a), raising=False)
    a = _decide_args(tmp_path, "T40,T41")
    a.go = True
    assert MP.cmd_launch(a) == 2 and not spawned and "preflight" in capsys.readouterr().out          # none on record
    led = MP.new_ledger()
    led["preflight"] = {"ok": True, "unix": time.time() - 80 * 3600}
    MP.ledger_path(tmp_path).parent.mkdir(parents=True, exist_ok=True)
    MP.ledger_path(tmp_path).write_text(json.dumps(led))
    assert MP.cmd_launch(a) == 2 and not spawned                                                      # too old
    assert MP.preflight_ok({"preflight": {"ok": True, "unix": time.time() - 3600}})
    assert not MP.preflight_ok({"preflight": {"ok": False, "unix": time.time()}})
