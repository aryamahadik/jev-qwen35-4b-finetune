"""CPU test of c2_build/snap_monitor_c2.py with fakes only (no Modal, no gcloud, no GPU, no real snapshot): rule
boundaries, scoring, the watch loop end to end (stockout fallback, the app-stop call mocked, ledger, VM stop), resume,
refused reads, escalation, the 13 Oct pgrep fix, the real Ops command lines with a fake runner, the C2 parameters
(run name, old slice, account) and a final-record path that never reads a real run's state. The old slice and the
snapshot labels are built in memory (no row file); the fakes write only fake adapter bytes and the monitor's own
state / log records into a temp folder.
Run: cd lean && ../.venv/bin/python -m pytest -q c2_build/tests/test_snap_monitor_c2.py
(`snap_monitor_c2.py cputest` runs this and writes c2_build/logs/snap_monitor_c2_cputest.json)."""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
import snap_monitor_c2 as sm  # noqa: E402
from c2_kit import paths as kp  # noqa: E402

N_STEPS = 1000                      # targets 250 / 500 / 750
NAME = sm.NAME
C1_SETTINGS = {"name": sm.C1, "base": sm.BASE, "revision": sm.REV, "layout": sm.LAYOUT, "perm_seed": None,
               "tta": False, "tta_choice": True, "tta_noul": False, "merged": True}
TPL = "a4aee8af"
SHARD_SHA = "5" * 64


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


@pytest.fixture
def tmp(tmp_path):
    assert kp.never_open(tmp_path) is None                 # never a session / never-open folder
    return tmp_path


# ---- a 200-row old slice in memory with C1's read (100 yes/no, 100 choice; C1 right on every row) --------------------
def old_rows():
    rows = []
    for i in range(200):
        if i < 100:
            rows.append({"id": f"r{i}", "qtype": "noul", "gold": i % 2})
        else:
            rows.append({"id": f"r{i}", "qtype": "choice", "options": ["a", "b", "c"], "gold": "a"})
    return rows


def ref_probs(rows):
    out = {}
    for r in rows:
        if r["qtype"] == "noul":
            y = 0.8 if r["gold"] == 1 else 0.2
            out[r["id"]] = {"yes": y, "no": 1 - y}
        else:
            out[r["id"]] = {"a": 0.6, "b": 0.3, "c": 0.1}
    return out


def make_old(tmp: Path | None = None) -> sm.OldSlice:
    """The slice in memory. With `tmp`: its folder holds two EMPTY placeholder files (no row), which the L4 copy
    step hashes and pushes."""
    rows = old_rows()
    meta = {"shard": "shard_000.jsonl", "rows": 200, "shard_sha256": SHARD_SHA, "settings": dict(C1_SETTINGS),
            "load": {"chat_template_sha": TPL}}
    d = (tmp or Path("/nonexistent")) / "c_old_slice_shards"
    if tmp is not None:
        d.mkdir(exist_ok=True)
        (d / "shard_000.jsonl").write_text("")
        (d / "shards.json").write_text("")
    return sm.OldSlice.from_memory(rows, ref_probs(rows), meta, d, shard_sha=SHARD_SHA)


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


def test_stats():
    old = make_old()
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


def test_settings_and_refs():
    old = make_old()
    meta = {"settings": {**C1_SETTINGS, "name": "snap_x"}, "load": {"chat_template_sha": "other"}}
    assert sm.check_settings(meta, old.ref_meta, "snap_x") == ["chat_template_sha other != C1's a4aee8af"]
    with pytest.raises(ValueError):
        sm.check_settings({"settings": {**C1_SETTINGS, "name": "snap_x", "tta_choice": False}}, old.ref_meta, "snap_x")
    with pytest.raises(SystemExit, match="A5 readout"):
        sm.OldSlice.from_memory(old.rows, old.ref, {"settings": {**C1_SETTINGS, "name": "q35_4b_pxE"}})


def test_label_files_must_be_of_the_pinned_shard(tmp):
    old = make_old()
    d = tmp / "labels_snap"
    d.mkdir()
    (d / "shard_000.jsonl").write_text(json.dumps({"id": "r0", "probs": {"yes": 0.2, "no": 0.8}}) + "\n")
    (d / "shard_000.meta.json").write_text(json.dumps({"rows": 1, "shard_sha256": SHARD_SHA}))
    probs, meta = sm.load_labels(d, old)
    assert probs == {"r0": {"yes": 0.2, "no": 0.8}}
    (d / "shard_000.meta.json").write_text(json.dumps({"rows": 1, "shard_sha256": "0" * 64}))
    with pytest.raises(ValueError, match="not of this old-slice shard"):
        sm.load_labels(d, old)


def test_missing_old_slice_is_a_clear_refusal(tmp):
    with pytest.raises(SystemExit, match="old slice missing"):
        sm.OldSlice(tmp / "c_old_slice_shards")


def test_default_old_slice_is_the_round1_slice():
    if not (sm.OLD_DIR / "shards.json").exists():
        pytest.skip("round-1 old slice (data/c_old_slice_shards) is not on this machine")
    old = sm.OldSlice()                                     # sha256-pinned, as spec 5.4 asks (same rows as round 1)
    assert len(old.rows) == 2000 and set(old.ref) >= {r["id"] for r in old.rows}
    assert sm.OLD_SHARDS_SHA == "9118d6b58466d301da0bb2dd5a197d164dcc933154e16d2dfcc9e555e3fa63d8"


# ---- the 13 Oct pgrep fix -------------------------------------------------------------------------------------------
def test_label_cmd_pgrep_never_matches_its_own_shell():
    old = make_old()
    mon = sm.Monitor.__new__(sm.Monitor)
    mon.old = old
    snap = "snap_q35_4b_c2_s000250"
    cmd = mon.label_cmd(snap)
    pats = re.findall(r"pgrep -f '([^']+)'", cmd)
    assert len(pats) == 2 and all(p.startswith(sm.PY_OD) for p in pats)
    shell = f"bash -c {cmd}"                                # the remote shell's own command line
    job = f"/home/u/od/bin/python od_gcp.py label --name {snap} --base {sm.BASE} --revision {sm.REV}"
    other = "/home/u/od/bin/python3 od_gcp.py predict --name q35_4b_main500k"
    running, busy = (re.compile(p) for p in pats)          # pgrep -f: an ERE searched in the full command line
    assert not running.search(shell) and not busy.search(shell)
    assert running.search(job) and busy.search(job) and busy.search(other) and not running.search(other)
    assert "--tta-choice" in cmd and f"data/{old.dir_name}" in cmd


# ---- fakes for the watch loop ------------------------------------------------------------------------------------------
class FakeOps(sm.Ops):
    def __init__(self, old: sm.OldSlice, plan: dict, timeline: list, tmp: Path, starts=None, running=None):
        super().__init__("mahadikarya2", seg_log=tmp / "c2_seg.log")
        self.old, self.plan, self.timeline = old, plan, timeline       # plan: step -> (drop, shift, settings patch)
        self.t, self.polls, self.sleeps, self.calls = 1e9, 0, [], []
        self.status = {"od-l4b": "TERMINATED", "od-l4": "TERMINATED", **(running or {})}
        self.starts = {k: list(v) for k, v in (starts or {}).items()}
        self.jobs, self.app_stops, self.ledgers, self.gets, self.labels = {}, [], [], [], {}

    def now(self):
        return self.t

    def sleep(self, s):
        self.sleeps.append(s)
        self.t += s

    def list_snaps(self, name):
        assert name == NAME
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
                assert f"data/{self.old.dir_name}/{self.old.shard_name}" in cmd
                return 0, "BASE_OK\nPY_OK\n" + "".join(f"{'0' * 64}  x{n}\n" for n in range(2))
            if "pgrep -fa" in cmd:
                assert sm.PY_OD in cmd
                return 0, ""
            if cmd.startswith("sha256sum ~/lean/models/"):
                return 0, "NONE"
            if "od_gcp.py label --name" in cmd:
                snap = cmd.split("od_gcp.py label --name ")[1].split()[0]
                assert "--tta-choice" in cmd and sm.PY_OD in cmd and f"od_gcp[.]py label --name {snap} " in cmd
                n = self.jobs.get(snap, -1)
                self.jobs[snap] = n + 1
                return 0, "LAUNCHED" if n < 0 else ("DONE" if n >= 2 else "RUNNING")
            if cmd.startswith("tail"):
                return 0, ""
            raise AssertionError(f"unexpected ssh {cmd[:80]}")
        if args[:2] == ["compute", "scp"]:
            src = args[-2]
            if ":~/lean/data/" in src:                                # fetch the labels of a finished read
                snap = src.split("labels_")[1]
                step = int(snap[-6:])
                drop, shift, patch = self.plan[step]
                self.labels[f"labels_{snap}"] = (snap_probs(self.old.rows, drop, shift),
                                                 {"rows": len(self.old.rows), "shard_sha256": self.old.shard_sha,
                                                  "settings": {**C1_SETTINGS, "name": snap, **patch},
                                                  "load": {"chat_template_sha": TPL}, "sec": 900})
            return 0, ""
        raise AssertionError(f"unexpected gcloud {args[:3]}")


@pytest.fixture
def mem_labels(monkeypatch):
    """Snapshot labels come from the fake's memory (no label file is written)."""
    box = {}

    def load(d, old):
        probs, meta = box["ops"].labels[Path(d).name]
        if meta["shard_sha256"] != old.shard_sha or meta["rows"] != len(probs):
            raise ValueError("labels are not of this old-slice shard")
        return probs, meta
    monkeypatch.setattr(sm, "load_labels", load)
    return box


def monitor(tmp, ops, old, final_rec=None, box=None):
    logs = tmp / "logs"
    logs.mkdir(exist_ok=True)
    if box is not None:
        box["ops"] = ops
    return sm.Monitor(ops, NAME, old, local=tmp / "snaps", logs=logs, final_rec=final_rec or tmp / "relay_final.json")


def events(tmp):
    return [json.loads(l) for l in (tmp / "logs/snap_monitor_c2.jsonl").read_text().splitlines()]


STOCK = (1, "ERROR: (gcloud.compute.instances.start) ZONE_RESOURCE_POOL_EXHAUSTED: a STOCKOUT in us-east4-c")


def test_watch_fires_at_50_stops_app_and_vm(tmp, mem_labels):
    old = make_old(tmp)
    plan = {250: (4, 0.0, {}), 500: (4, 0.0, {}), 750: (0, 0.0, {})}       # -2.0 pp at 25% and 50%
    ops = FakeOps(old, plan, [[], [], [250], [250, 500], [250, 500, 750]], tmp, starts={"od-l4b": [STOCK]})
    rc = monitor(tmp, ops, old, box=mem_labels).run(max_hours=12)
    assert rc == 3 and ops.app_stops == [NAME] and len(ops.ledgers) == 1 and "STOP RULE" in ops.ledgers[0]
    assert ops.ledgers[0].startswith(f"C2 ({NAME})")
    rec = json.loads((tmp / "logs/snap_monitor_c2_stop.json").read_text())
    assert rec["fired"] and "both 25%" in rec["why"][0] and rec["candidate"].startswith("none") and rec["run"] == NAME
    st = json.loads((tmp / "logs/snap_monitor_c2_state.json").read_text())
    assert sorted(st["reads"]) == ["0.25", "0.5"] and st["reads"]["0.5"]["acc_diff_pp"] == -2.0
    ev = events(tmp)
    assert any(e["ev"] == "vm_start_failed" and e["vm"] == "od-l4b" and e["kind"] == "stockout" for e in ev)
    assert ops.status == {"od-l4b": "TERMINATED", "od-l4": "TERMINATED"}            # the VM it started is stopped
    assert not any("s000750" in g for g in ops.gets) and all(f"models/{NAME}/snaps/" in g for g in ops.gets)


def test_watch_no_fire_reads_all_three(tmp, mem_labels):
    old = make_old(tmp)
    plan = {250: (3, 0.02, {}), 500: (3, -0.02, {}), 750: (10, 0.0, {})}   # exactly -1.5 pp and exactly 0.02
    ops = FakeOps(old, plan, [[250, 500, 750]], tmp)
    rc = monitor(tmp, ops, old, box=mem_labels).run(max_hours=12)
    st = json.loads((tmp / "logs/snap_monitor_c2_state.json").read_text())
    assert rc == 0 and sorted(st["reads"]) == ["0.25", "0.5", "0.75"] and not ops.app_stops and not ops.ledgers
    assert not (tmp / "logs/snap_monitor_c2_stop.json").exists() and ops.status["od-l4b"] == "TERMINATED"
    assert any(e["ev"] == "done" for e in events(tmp))


def test_watch_pyes_drift_fires_at_25(tmp, mem_labels):
    old = make_old(tmp)
    ops = FakeOps(old, {250: (0, 0.03, {}), 500: (0, 0.0, {}), 750: (0, 0.0, {})}, [[250]], tmp)
    assert monitor(tmp, ops, old, box=mem_labels).run(max_hours=12) == 3 and ops.app_stops
    assert "P(yes)" in json.loads((tmp / "logs/snap_monitor_c2_stop.json").read_text())["why"][0]


def test_both_zones_stockout_retry_20_min(tmp, mem_labels):
    old = make_old(tmp)
    ops = FakeOps(old, {s: (0, 0.0, {}) for s in (250, 500, 750)}, [[250, 500, 750]], tmp,
                  starts={"od-l4b": [STOCK, (0, "")], "od-l4": [(1, "Quota 'GPUS_ALL_REGIONS' exceeded")]})
    assert monitor(tmp, ops, old, box=mem_labels).run(max_hours=12) == 0
    assert sm.RETRY_S in ops.sleeps and any(e["ev"] == "no_l4" for e in events(tmp))


def test_resume_skips_finished_reads(tmp, mem_labels):
    old = make_old(tmp)
    (tmp / "logs").mkdir()
    (tmp / "logs/snap_monitor_c2_state.json").write_text(json.dumps({
        "name": NAME, "n_steps": N_STEPS, "reads": {"0.25": {"acc_diff_pp": -2.0, "pyes_drift": 0.0}},
        "attempts": {"0.25": 1}}))
    ops = FakeOps(old, {500: (4, 0.0, {}), 750: (0, 0.0, {})}, [[250, 500]], tmp)
    assert monitor(tmp, ops, old, box=mem_labels).run(max_hours=12) == 3     # 25% (stored) + 50% now -> fires
    assert not any("s000250" in g for g in ops.gets)


def test_state_of_another_run_is_refused(tmp):
    (tmp / "logs").mkdir()
    (tmp / "logs/snap_monitor_c2_state.json").write_text(json.dumps({"name": "q35_4b_c_r1", "reads": {}}))
    with pytest.raises(SystemExit, match="belongs to q35_4b_c_r1"):
        monitor(tmp, FakeOps(make_old(), {}, [[]], tmp), make_old())


def test_three_failed_reads_escalate_and_stop_app(tmp, mem_labels):
    old = make_old(tmp)
    ops = FakeOps(old, {250: (10, 0.05, {"tta_choice": False}), 500: (0, 0, {}), 750: (0, 0, {})}, [[250]], tmp)
    rc = monitor(tmp, ops, old, box=mem_labels).run(max_hours=12)
    st = json.loads((tmp / "logs/snap_monitor_c2_state.json").read_text())
    assert rc == 4 and st["failures"]["0.25"] == sm.READ_FAIL_CAP == 3 and st["reads"] == {}
    assert ops.app_stops == [NAME] and len(ops.ledgers) == 1 and "ESCALATED" in ops.ledgers[0]
    rec = json.loads((tmp / "logs/snap_monitor_c2_escalation.json").read_text())
    assert rec["escalated"] and rec["frac"] == "0.25" and rec["failures"] == 3 and rec["candidate"].startswith("none")
    assert not (tmp / "logs/snap_monitor_c2_stop.json").exists()
    assert ops.status == {"od-l4b": "TERMINATED", "od-l4": "TERMINATED"}
    assert [e["n"] for e in events(tmp) if e["ev"] == "read_failed"] == [1, 2, 3]
    assert any(e["ev"] == "error" and "other settings" in e["msg"] for e in events(tmp))
    assert monitor(tmp, ops, old, box=mem_labels).run(max_hours=1) == 4 and ops.app_stops == [NAME]   # no re-stop


def test_two_failed_reads_then_success_do_not_escalate(tmp, mem_labels):
    old = make_old(tmp)

    class Flaky(FakeOps):
        fails = 2

        def get(self, remote, dest):
            if not remote.endswith("train_meta.json") and self.fails:
                self.fails -= 1
                raise RuntimeError("volume get failed")
            return super().get(remote, dest)

    ops = Flaky(old, {250: (3, 0.0, {}), 500: (3, 0.0, {}), 750: (3, 0.0, {})}, [[250, 500, 750]], tmp)
    rc = monitor(tmp, ops, old, box=mem_labels).run(max_hours=12)
    st = json.loads((tmp / "logs/snap_monitor_c2_state.json").read_text())
    assert rc == 0 and sorted(st["reads"]) == ["0.25", "0.5", "0.75"] and st["failures"] == {"0.25": 2}
    assert not ops.app_stops and not (tmp / "logs/snap_monitor_c2_escalation.json").exists()


def test_uses_running_vm_and_leaves_it_running(tmp, mem_labels):
    old = make_old(tmp)
    ops = FakeOps(old, {s: (0, 0.0, {}) for s in (250, 500, 750)}, [[250, 500, 750]], tmp,
                  running={"od-l4": "RUNNING"})
    assert monitor(tmp, ops, old, box=mem_labels).run(max_hours=12) == 0
    assert ops.status["od-l4"] == "RUNNING" and not any(a[:3] == ["compute", "instances", "start"] for a in ops.calls)


def test_fire_after_final_does_not_stop_app(tmp, mem_labels):
    old = make_old(tmp)
    final = tmp / "relay_q35_4b_c2_final.json"
    final.write_text("{}")
    ops = FakeOps(old, {250: (0, 0.05, {}), 500: (0, 0, {}), 750: (0, 0, {})}, [[250, 500, 750]], tmp)
    assert monitor(tmp, ops, old, final_rec=final, box=mem_labels).run(max_hours=12) == 3
    assert not ops.app_stops and len(ops.ledgers) == 1
    assert json.loads((tmp / "logs/snap_monitor_c2_stop.json").read_text())["after_final"] is True


def test_final_record_is_the_runs_own_and_hermetic(tmp):
    assert sm.final_record(NAME) == sm.LEAN / "logs/relay_q35_4b_c2_final.json"
    mon = monitor(tmp, FakeOps(make_old(), {}, [[]], tmp), make_old())
    assert mon.final_rec == tmp / "relay_final.json" and not mon.final_exists()      # a real run's file is never read


def test_vm_without_base_is_dropped_for_the_other(tmp, mem_labels):
    old = make_old(tmp)

    class NoBase(FakeOps):
        def gcloud(self, args, timeout=300):
            if "--command" in args and "BASE_OK" in args[args.index("--command") + 1] and "od-l4b" in args:
                return 0, "BASE_MISSING\nPY_OK\n"
            return super().gcloud(args, timeout)

    ops = NoBase(old, {s: (0, 0.0, {}) for s in (250, 500, 750)}, [[250, 500, 750]], tmp)
    assert monitor(tmp, ops, old, box=mem_labels).run(max_hours=12) == 0
    st = json.loads((tmp / "logs/snap_monitor_c2_state.json").read_text())
    assert st["bad_vms"] == ["od-l4b"] and {r["vm"] for r in st["reads"].values()} == {"od-l4"}
    assert ops.status == {"od-l4b": "TERMINATED", "od-l4": "TERMINATED"}


# ---- the real Ops command lines with a fake runner -----------------------------------------------------------------------
def test_real_stop_app_command_line(tmp):
    seg = tmp / "c2_seg.log"
    seg.write_text("View run at https://modal.com/apps/x/main/ap-AbC123xyz\n")
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

    res = R("mahadikarya2", seg_log=seg).stop_app(NAME)
    stops = [a for a, prof in ran if a[1:3] == ["app", "stop"]]
    assert [a[-1] for a in stops] == ["ap-AbC123xyz", "ap-Other999"] and res["still_running"] == []
    assert all("-y" in a for a in stops)  # non-interactive `modal app stop` aborts without -y
    assert all(prof == "mahadikarya2" for _, prof in ran) and all(a[0] == sm.MODAL for a, _ in ran)


def test_real_list_snaps_parses_volume_json():
    class R(sm.Ops):
        def _run(self, argv, timeout, env=None):
            assert argv[1:5] == ["volume", "ls", "opendecide", f"models/{NAME}/snaps"]
            return 0, json.dumps([{"Filename": f"models/{NAME}/snaps/s002317", "Type": "dir"},
                                  {"Filename": f"models/{NAME}/snaps/.s004634.tmp", "Type": "dir"},
                                  {"Filename": f"models/{NAME}/snaps/s002500", "Type": "dir"}])
    assert R("mahadikarya2").list_snaps(NAME) == [2317, 2500]


def test_lock_and_cputest_record(tmp):
    (tmp / "snap_monitor_c2.pid").write_text(str(os.getpid()))
    with pytest.raises(SystemExit):
        sm.lock(tmp)
    (tmp / "snap_monitor_c2.pid").write_text("999999")
    assert sm.lock(tmp).read_text() == str(os.getpid())
    rec = tmp / "rec.json"
    rec.write_text(json.dumps({"pass": True, "snap_monitor_c2_sha256": "0" * 64, "test_sha256": sha(sm.TEST)}))
    assert "changed" in sm.cputest_ok(rec)
    rec.write_text(json.dumps({"pass": True, "snap_monitor_c2_sha256": sha(C2B / "snap_monitor_c2.py"),
                               "test_sha256": sha(sm.TEST)}))
    assert sm.cputest_ok(rec) is None
    assert sm.TEST == Path(__file__).resolve()


def test_c2_parameters_and_main_refusals():
    assert sm.NAME == "q35_4b_c2" and sm.PROFILES == ("mahadikarya2", "mahadikarya3", "jaypatil-duke", "atmosphor", "arya-mahadik-ai", "mahadikarya44") and sm.LOGS == C2B / "logs"
    assert sm.OLD_DIR == sm.LEAN / "data/c_old_slice_shards" and sm.OLD_ROWS_SHA.startswith("d2bd19c5")
    assert "c_build" not in str(sm.STATE) and sm.STATE.name == "snap_monitor_c2_state.json"
    with pytest.raises(SystemExit, match="no card"):
        sm.main(["watch", "--profile", "aryamhd"])
    with pytest.raises(SystemExit, match="refused"):
        sm.main(["watch", "--name", "ohs4_probe"])
