"""CPU test of c_build/endgame/snap_monitor.py with fakes only (no Modal, no gcloud, no GPU, no real snapshot):
rule boundaries, scoring, the watch loop end to end (stockout fallback, the app-stop call mocked, ledger, VM stop),
resume, a refused read, the real Ops.stop_app command line with a fake runner.
Run: cd lean && ../.venv/bin/python -m pytest -q c_build/endgame/tests/test_snap_monitor.py
(`snap_monitor.py cputest` runs this and writes logs/snap_monitor_cputest.json)."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
EG = HERE.parent
sys.path.insert(0, str(EG))
import snap_monitor as sm  # noqa: E402

N_STEPS = 1000                      # targets 250 / 500 / 750
C1_SETTINGS = {"name": sm.C1, "base": sm.BASE, "revision": sm.REV, "layout": sm.LAYOUT, "perm_seed": None,
               "tta": False, "tta_choice": True, "tta_noul": False, "merged": True}
TPL = "a4aee8af"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


@pytest.fixture
def tmp():
    d = Path(tempfile.mkdtemp(prefix="snapmon_test_", dir=str(EG / "tmp")))
    yield d
    shutil.rmtree(d, ignore_errors=True)


# ---- a fake 200-row old slice with C1's read (100 yes/no, 100 choice; C1 right on every row) ----------------------------
def make_old(tmp: Path) -> sm.OldSlice:
    d = tmp / "c_old_slice_shards"
    (d / f"labels_{sm.C1}").mkdir(parents=True)
    rows = []
    for i in range(200):
        if i < 100:
            rows.append({"id": f"r{i}", "qtype": "noul", "gold": i % 2})
        else:
            rows.append({"id": f"r{i}", "qtype": "choice", "options": ["a", "b", "c"], "gold": "a"})
    shard = d / "shard_000.jsonl"
    shard.write_text("".join(json.dumps(r) + "\n" for r in rows))
    (d / "shards.json").write_text(json.dumps({"rows": 200, "shards": [{"file": "shard_000.jsonl", "rows": 200}]}))
    write_labels(d / f"labels_{sm.C1}", rows, ref_probs(rows), dict(C1_SETTINGS), shard)
    return sm.OldSlice(d, sha(d / "shards.json"), sha(shard))


def ref_probs(rows):
    out = {}
    for r in rows:
        if r["qtype"] == "noul":
            y = 0.8 if r["gold"] == 1 else 0.2
            out[r["id"]] = {"yes": y, "no": 1 - y}
        else:
            out[r["id"]] = {"a": 0.6, "b": 0.3, "c": 0.1}
    return out


def snap_probs(rows, drop: int, shift: float):
    """C1's read with `drop` choice rows turned wrong and P(yes) moved by `shift` on every yes/no row (argmax kept)."""
    p = ref_probs(rows)
    for r in [r for r in rows if r["qtype"] == "choice"][:drop]:
        p[r["id"]] = {"a": 0.1, "b": 0.8, "c": 0.1}
    for r in rows:
        if r["qtype"] == "noul":
            y = p[r["id"]]["yes"] + shift
            p[r["id"]] = {"yes": y, "no": 1 - y}
    return p


def write_labels(d: Path, rows, probs, settings, shard: Path):
    d.mkdir(parents=True, exist_ok=True)
    (d / "shard_000.jsonl").write_text("".join(json.dumps({"id": r["id"], "model": settings["name"],
                                                           "probs": probs[r["id"]]}) + "\n" for r in rows))
    (d / "shard_000.meta.json").write_text(json.dumps({"shard": "shard_000.jsonl", "rows": len(rows),
                                                       "shard_sha256": sha(shard), "settings": settings,
                                                       "load": {"chat_template_sha": TPL}, "sec": 900}))


# ---- rule boundaries ----------------------------------------------------------------------------------------------
def S(acc, drift=0.0):
    return {"acc_diff_pp": acc, "pyes_drift": drift}


@pytest.mark.parametrize("reads,fires", [
    ({"0.25": S(-1.5), "0.5": S(-1.5)}, False),            # exactly C1 - 1.5: not below
    ({"0.25": S(-1.51), "0.5": S(-1.51)}, True),
    ({"0.25": S(-2.0), "0.5": S(-1.4)}, False),            # 25% only
    ({"0.25": S(-1.0), "0.5": S(-3.0)}, False),            # 50% only
    ({"0.25": S(-2.0)}, False),                            # 50% not read yet
    ({"0.25": S(-2.0), "0.5": S(-2.0), "0.75": S(0.0)}, True),
    ({"0.25": S(0.0, 0.02)}, False),                       # drift exactly 0.02
    ({"0.25": S(0.0, 0.0201)}, True),
    ({"0.25": S(0.0, -0.0201)}, True),                     # either direction
    ({"0.25": S(0.0), "0.5": S(0.0), "0.75": S(0.0, 0.021)}, True),   # drift at 75%
    ({"0.25": S(+3.0), "0.5": S(+3.0), "0.75": S(+3.0, 0.019)}, False),
])
def test_rule_boundaries(reads, fires):
    assert sm.rule(reads)[0] is fires


def test_stats(tmp):
    old = make_old(tmp)
    s = sm.stats(old.rows, old.ref, old.ref)
    assert s["acc_diff_pp"] == 0 and s["flips_1to0"] == 0 and abs(s["kl_c1_snap"]) < 1e-9 and s["pyes_drift"] == 0
    s = sm.stats(old.rows, old.ref, snap_probs(old.rows, 3, 0.0))
    assert s["acc_diff_pp"] == -1.5 and s["flips_1to0"] == 3 and s["kl_c1_snap"] > 0
    tie = dict(old.ref, r150={"a": 0.45, "b": 0.45, "c": 0.1})                 # a tie for the top counts as wrong
    assert sm.stats(old.rows, old.ref, tie)["flips_1to0"] == 1
    s = sm.stats(old.rows, old.ref, snap_probs(old.rows, 0, 0.03))
    assert abs(s["pyes_drift"] - 0.03) < 1e-9 and s["acc_diff_pp"] == 0
    with pytest.raises(ValueError):
        sm.stats(old.rows, old.ref, {k: v for k, v in old.ref.items() if k != "r5"})


def test_settings_and_refs(tmp):
    old = make_old(tmp)
    meta = {"settings": {**C1_SETTINGS, "name": "snap_x"}, "load": {"chat_template_sha": "other"}}
    assert sm.check_settings(meta, old.ref_meta, "snap_x") == ["chat_template_sha other != C1's a4aee8af"]
    with pytest.raises(ValueError):
        sm.check_settings({"settings": {**C1_SETTINGS, "name": "snap_x", "tta_choice": False}}, old.ref_meta, "snap_x")
    with pytest.raises(SystemExit):
        sm.OldSlice(old.dir, "0" * 64, sha(old.shard))


# ---- fakes for the watch loop ------------------------------------------------------------------------------------------
class FakeOps(sm.Ops):
    def __init__(self, old: sm.OldSlice, plan: dict, timeline: list, starts=None, running=None, final=False):
        super().__init__("aryamhd")
        self.old, self.plan, self.timeline = old, plan, timeline       # plan: step -> (drop, shift, settings patch)
        self.t, self.polls, self.sleeps, self.calls = 1e9, 0, [], []
        self.status = {"od-l4b": "TERMINATED", "od-l4": "TERMINATED", **(running or {})}
        self.starts = {k: list(v) for k, v in (starts or {}).items()}
        self.jobs, self.app_stops, self.ledgers, self.gets = {}, [], [], []

    def now(self):
        return self.t

    def sleep(self, s):
        self.sleeps.append(s)
        self.t += s

    def list_snaps(self, name):
        self.polls += 1
        return self.timeline[min(self.polls - 1, len(self.timeline) - 1)]

    def get(self, remote, dest):
        self.gets.append(remote)
        dest.mkdir(parents=True, exist_ok=True)
        step = int(remote.split("/snaps/s")[1][:6])
        meta = {"cfg": {"layout": sm.LAYOUT}, "steps": N_STEPS, "snapshot_step": step}
        if remote.endswith("train_meta.json"):
            (dest / "train_meta.json").write_text(json.dumps(meta))
            return
        d = dest / f"s{step:06d}"
        d.mkdir()
        (d / "adapter_model.safetensors").write_bytes(f"adapter {step}".encode())
        (d / "train_meta.json").write_text(json.dumps(meta))

    def stop_app(self, name):
        self.app_stops.append(name)
        return {"app_ids": ["ap-fake123"], "calls": [], "still_running": []}

    def ledger(self, text):
        self.ledgers.append(text)

    def gcloud(self, args, timeout=300):
        i = args.index("--project")
        assert args[i + 1] == sm.PROJECT
        args = args[:i] + args[i + 2:]
        self.calls.append(args)
        if args[:3] == ["compute", "instances", "describe"]:
            return 0, self.status[args[3]] + "\n"
        if args[:3] == ["compute", "instances", "start"]:
            rc, out = (self.starts.get(args[3]) or [(0, "")]).pop(0) if self.starts.get(args[3]) else (0, "")
            if rc == 0:
                self.status[args[3]] = "RUNNING"
            return rc, out
        if args[:3] == ["compute", "instances", "stop"]:
            self.status[args[3]] = "TERMINATED"
            return 0, ""
        if args[:2] == ["compute", "ssh"]:
            assert self.status[args[2]] == "RUNNING", f"ssh to a stopped VM {args[2]}"
            cmd = args[args.index("--command") + 1]
            if cmd == "echo ok":
                return 0, "ok"
            if "BASE_OK" in cmd:
                return 0, "BASE_OK\nPY_OK\n"                         # no sha lines: every file gets pushed
            if "pgrep -fa" in cmd:
                return 0, ""
            if cmd.startswith("sha256sum ~/lean/models/"):
                return 0, "NONE"
            if "od_gcp.py label --name" in cmd:
                snap = cmd.split("od_gcp.py label --name ")[1].split()[0]
                assert "--tta-choice" in cmd and "[o]d_gcp.py" in cmd and f"[{snap[0]}]{snap[1:]}" in cmd
                n = self.jobs.get(snap, -1)
                self.jobs[snap] = n + 1
                return 0, "LAUNCHED" if n < 0 else ("DONE" if n >= 2 else "RUNNING")
            if cmd.startswith("tail"):
                return 0, ""
            raise AssertionError(f"unexpected ssh {cmd[:80]}")
        if args[:2] == ["compute", "scp"]:
            src, dst = args[-2], args[-1]
            if ":~/lean/data/" in src:                                # fetch the labels of a finished read
                snap = src.split("labels_")[1]
                step = int(snap[-6:])
                drop, shift, patch = self.plan[step]
                write_labels(Path(dst) / f"labels_{snap}", self.old.rows, snap_probs(self.old.rows, drop, shift),
                             {**C1_SETTINGS, "name": snap, **patch}, self.old.shard)
            return 0, ""
        raise AssertionError(f"unexpected gcloud {args[:3]}")


def monitor(tmp, ops, old):
    logs = tmp / "logs"
    logs.mkdir(exist_ok=True)
    return sm.Monitor(ops, "q35_4b_c_r1", old, local=tmp / "snaps", logs=logs)


def events(tmp):
    return [json.loads(l) for l in (tmp / "logs/snap_monitor.jsonl").read_text().splitlines()]


STOCK = (1, "ERROR: (gcloud.compute.instances.start) ZONE_RESOURCE_POOL_EXHAUSTED: a STOCKOUT in us-east4-c")


def test_watch_fires_at_50_stops_app_and_vm(tmp):
    old = make_old(tmp)
    plan = {250: (4, 0.0, {}), 500: (4, 0.0, {}), 750: (0, 0.0, {})}       # -2.0 pp at 25% and 50%
    ops = FakeOps(old, plan, [[], [], [250], [250, 500], [250, 500, 750]], starts={"od-l4b": [STOCK]})
    rc = monitor(tmp, ops, old).run(max_hours=12)
    assert rc == 3 and ops.app_stops == ["q35_4b_c_r1"] and len(ops.ledgers) == 1 and "STOP RULE" in ops.ledgers[0]
    rec = json.loads((tmp / "logs/snap_monitor_stop.json").read_text())
    assert rec["fired"] and "both 25%" in rec["why"][0] and rec["candidate"].startswith("none")
    st = json.loads((tmp / "logs/snap_monitor_state.json").read_text())
    assert sorted(st["reads"]) == ["0.25", "0.5"] and st["reads"]["0.5"]["acc_diff_pp"] == -2.0
    ev = events(tmp)
    assert any(e["ev"] == "vm_start_failed" and e["vm"] == "od-l4b" and e["kind"] == "stockout" for e in ev)
    assert ops.status == {"od-l4b": "TERMINATED", "od-l4": "TERMINATED"}            # the VM it started is stopped
    assert not any("s000750" in g for g in ops.gets)


def test_watch_no_fire_reads_all_three(tmp):
    old = make_old(tmp)
    plan = {250: (3, 0.02, {}), 500: (3, -0.02, {}), 750: (10, 0.0, {})}   # exactly -1.5 pp and exactly 0.02
    ops = FakeOps(old, plan, [[250, 500, 750]])
    rc = monitor(tmp, ops, old).run(max_hours=12)
    st = json.loads((tmp / "logs/snap_monitor_state.json").read_text())
    assert rc == 0 and sorted(st["reads"]) == ["0.25", "0.5", "0.75"] and not ops.app_stops and not ops.ledgers
    assert not (tmp / "logs/snap_monitor_stop.json").exists() and ops.status["od-l4b"] == "TERMINATED"
    assert any(e["ev"] == "done" for e in events(tmp))


def test_watch_pyes_drift_fires_at_25(tmp):
    old = make_old(tmp)
    ops = FakeOps(old, {250: (0, 0.03, {}), 500: (0, 0.0, {}), 750: (0, 0.0, {})}, [[250]])
    assert monitor(tmp, ops, old).run(max_hours=12) == 3 and ops.app_stops
    assert "P(yes)" in json.loads((tmp / "logs/snap_monitor_stop.json").read_text())["why"][0]


def test_both_zones_stockout_retry_20_min(tmp):
    old = make_old(tmp)
    ops = FakeOps(old, {s: (0, 0.0, {}) for s in (250, 500, 750)}, [[250, 500, 750]],
                  starts={"od-l4b": [STOCK, (0, "")], "od-l4": [(1, "Quota 'GPUS_ALL_REGIONS' exceeded")]})
    assert monitor(tmp, ops, old).run(max_hours=12) == 0
    assert sm.RETRY_S in ops.sleeps and any(e["ev"] == "no_l4" for e in events(tmp))


def test_resume_skips_finished_reads(tmp):
    old = make_old(tmp)
    (tmp / "logs").mkdir()
    (tmp / "logs/snap_monitor_state.json").write_text(json.dumps({
        "name": "q35_4b_c_r1", "n_steps": N_STEPS, "reads": {"0.25": {"acc_diff_pp": -2.0, "pyes_drift": 0.0}},
        "attempts": {"0.25": 1}}))
    ops = FakeOps(old, {500: (4, 0.0, {}), 750: (0, 0.0, {})}, [[250, 500]])
    assert monitor(tmp, ops, old).run(max_hours=12) == 3                     # 25% (stored) + 50% now -> fires
    assert not any("s000250" in g for g in ops.gets)


def test_refused_read_is_logged_not_scored(tmp):
    old = make_old(tmp)
    ops = FakeOps(old, {250: (10, 0.05, {"tta_choice": False}), 500: (0, 0, {}), 750: (0, 0, {})}, [[250]])
    rc = monitor(tmp, ops, old).run(max_hours=1)
    st = json.loads((tmp / "logs/snap_monitor_state.json").read_text())
    assert rc == 4 and st["reads"] == {} and st["errors"] >= 1        # refused 3 times -> escalation (retry cap)
    assert any(e["ev"] == "error" and "other settings" in e["msg"] for e in events(tmp))


def test_three_failed_reads_escalate_and_stop_app(tmp):
    old = make_old(tmp)
    ops = FakeOps(old, {250: (10, 0.05, {"tta_choice": False}), 500: (0, 0, {}), 750: (0, 0, {})}, [[250]])
    rc = monitor(tmp, ops, old).run(max_hours=12)
    st = json.loads((tmp / "logs/snap_monitor_state.json").read_text())
    assert rc == 4 and st["failures"]["0.25"] == sm.READ_FAIL_CAP == 3 and st["reads"] == {}
    assert ops.app_stops == ["q35_4b_c_r1"] and len(ops.ledgers) == 1 and "ESCALATED" in ops.ledgers[0]
    rec = json.loads((tmp / "logs/snap_monitor_escalation.json").read_text())
    assert rec["escalated"] and rec["frac"] == "0.25" and rec["failures"] == 3 and rec["candidate"].startswith("none")
    assert not (tmp / "logs/snap_monitor_stop.json").exists()
    assert ops.status == {"od-l4b": "TERMINATED", "od-l4": "TERMINATED"}
    assert [e["n"] for e in events(tmp) if e["ev"] == "read_failed"] == [1, 2, 3]
    assert monitor(tmp, ops, old).run(max_hours=1) == 4 and ops.app_stops == ["q35_4b_c_r1"]   # restart: no re-stop


def test_two_failed_reads_then_success_do_not_escalate(tmp):
    old = make_old(tmp)

    class Flaky(FakeOps):
        fails = 2

        def get(self, remote, dest):
            if not remote.endswith("train_meta.json") and self.fails:
                self.fails -= 1
                raise RuntimeError("volume get failed")
            return super().get(remote, dest)

    ops = Flaky(old, {250: (3, 0.0, {}), 500: (3, 0.0, {}), 750: (3, 0.0, {})}, [[250, 500, 750]])
    rc = monitor(tmp, ops, old).run(max_hours=12)
    st = json.loads((tmp / "logs/snap_monitor_state.json").read_text())
    assert rc == 0 and sorted(st["reads"]) == ["0.25", "0.5", "0.75"] and st["failures"] == {"0.25": 2}
    assert not ops.app_stops and not (tmp / "logs/snap_monitor_escalation.json").exists()


def test_uses_running_vm_and_leaves_it_running(tmp):
    old = make_old(tmp)
    ops = FakeOps(old, {s: (0, 0.0, {}) for s in (250, 500, 750)}, [[250, 500, 750]], running={"od-l4": "RUNNING"})
    assert monitor(tmp, ops, old).run(max_hours=12) == 0
    assert ops.status["od-l4"] == "RUNNING" and not any(a[:3] == ["compute", "instances", "start"] for a in ops.calls)


def test_fire_after_final_does_not_stop_app(tmp, monkeypatch):
    old = make_old(tmp)
    ops = FakeOps(old, {250: (0, 0.05, {}), 500: (0, 0, {}), 750: (0, 0, {})}, [[250, 500, 750]])
    m = monitor(tmp, ops, old)
    monkeypatch.setattr(m, "final_exists", lambda: True)
    assert m.run(max_hours=12) == 3 and not ops.app_stops and len(ops.ledgers) == 1
    assert json.loads((tmp / "logs/snap_monitor_stop.json").read_text())["after_final"] is True


# ---- the real Ops command lines with a fake runner -----------------------------------------------------------------------
def test_real_stop_app_command_line(tmp):
    seg3 = tmp / "r1_seg3.log"
    seg3.write_text("View run at https://modal.com/apps/x/main/ap-AbC123xyz\n")
    ran = []
    lists = [json.dumps([{"App ID": "ap-Other999", "State": "ephemeral (detached)", "Tasks": "1"}]), "[]"]

    class R(sm.Ops):
        def _run(self, argv, timeout, env=None):
            ran.append((argv, (env or {}).get("MODAL_PROFILE")))
            if argv[1:3] == ["app", "list"]:
                return 0, lists.pop(0) if lists else "[]"
            return 0, ""

        def sleep(self, s):
            pass

    res = R("aryamhd", seg3_log=seg3).stop_app("q35_4b_c_r1")
    stops = [a for a, prof in ran if a[1:3] == ["app", "stop"]]
    assert [a[-1] for a in stops] == ["ap-AbC123xyz", "ap-Other999"] and res["still_running"] == []
    assert all("-y" in a for a in stops)  # non-interactive `modal app stop` aborts without -y
    assert all(prof == "aryamhd" for _, prof in ran) and all(a[0] == sm.MODAL for a, _ in ran)


def test_real_list_snaps_parses_volume_json():
    class R(sm.Ops):
        def _run(self, argv, timeout, env=None):
            assert argv[1:5] == ["volume", "ls", "opendecide", "models/q35_4b_c_r1/snaps"]
            return 0, json.dumps([{"Filename": "models/q35_4b_c_r1/snaps/s002317", "Type": "dir"},
                                  {"Filename": "models/q35_4b_c_r1/snaps/.s004634.tmp", "Type": "dir"},
                                  {"Filename": "models/q35_4b_c_r1/snaps/s002500", "Type": "dir"}])
    assert R("aryamhd").list_snaps("q35_4b_c_r1") == [2317, 2500]


def test_lock_and_cputest_record(tmp):
    (tmp / "snap_monitor.pid").write_text(str(os.getpid()))
    with pytest.raises(SystemExit):
        sm.lock(tmp)
    (tmp / "snap_monitor.pid").write_text("999999")
    assert sm.lock(tmp).read_text() == str(os.getpid())
    rec = tmp / "rec.json"
    rec.write_text(json.dumps({"pass": True, "snap_monitor_sha256": "0" * 64, "test_sha256": sha(sm.TEST)}))
    assert "changed" in sm.cputest_ok(rec)
    rec.write_text(json.dumps({"pass": True, "snap_monitor_sha256": sha(EG / "snap_monitor.py"),
                               "test_sha256": sha(sm.TEST)}))
    assert sm.cputest_ok(rec) is None


def test_main_refuses_other_profile():
    with pytest.raises(SystemExit, match="aryamhd"):
        sm.main(["watch", "--profile", "atmosphor"])


def test_vm_without_base_is_dropped_for_the_other(tmp):
    old = make_old(tmp)

    class NoBase(FakeOps):
        def gcloud(self, args, timeout=300):
            if "--command" in args and "BASE_OK" in args[args.index("--command") + 1] and "od-l4b" in args:
                return 0, "BASE_MISSING\nPY_OK\n"
            return super().gcloud(args, timeout)

    ops = NoBase(old, {s: (0, 0.0, {}) for s in (250, 500, 750)}, [[250, 500, 750]])
    assert monitor(tmp, ops, old).run(max_hours=12) == 0
    st = json.loads((tmp / "logs/snap_monitor_state.json").read_text())
    assert st["bad_vms"] == ["od-l4b"] and {r["vm"] for r in st["reads"].values()} == {"od-l4"}
    assert ops.status == {"od-l4b": "TERMINATED", "od-l4": "TERMINATED"}
