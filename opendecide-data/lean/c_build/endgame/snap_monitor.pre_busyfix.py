"""snap_monitor.py: the recipe 5 stop-rule driver for C round 1 (RUNBOOK D5, blocker B6). $0 Modal compute.

Pre-registered stop rule (C_TRAIN_RECIPE v4 section 5): stop the run if the old slice is below C1 - 1.5 pp at BOTH the
25% and 50% snapshots, or if mean P(yes) on old yes/no rows drifts by more than 0.02 (vs C1, either way, at any read
snapshot). A stopped run yields no candidate for that round; the owner reviews; a re-run needs an amendment.

  watch   (r1_chain.sh starts it beside segment 3, from lean/):
            snap_monitor.py watch --profile aryamhd --name q35_4b_c_r1
          Polls the aryamhd Volume (`modal volume ls`, free) for the 25 / 50 / 75% snapshots (int(f x n_steps), the
          trainer's snap_fracs; n_steps from the snapshot's own train_meta), downloads each one (`modal volume get`),
          reads it on a free Google L4 VM with the existing tool (od_gcp.py label --tta-choice: the A5 readout C1's
          old-slice read used, data/c_old_slice_shards/labels_q35_4b_main500k), fetches the labels and scores them on
          the Mac against C1's read of the same 2,000 rows (accuracy, 1->0 / 0->1 flips, mean P(yes), KL(C1 || C)).
          Logs to logs/snap_monitor.jsonl. When the rule fires: `MODAL_PROFILE=aryamhd modal app stop <relay app>`
          (the app id from logs/r1_seg3.log plus every running app on the card-only account), a ledger line, and
          logs/snap_monitor_stop.json (no candidate this round). RETRY CAP: a snapshot whose read fails 3 times
          (fetch, L4 read, refused settings or scoring; a stockout wait is not a failed read) ESCALATES: the relay
          app is stopped (the stop rule cannot be checked, so the run must not continue unwatched), a ledger line
          and logs/snap_monitor_escalation.json are written, and watch exits 4 (no candidate until the owner
          decides). Restartable: logs/snap_monitor_state.json keeps every
          finished read; the VM-side label job is resumable (od_gcp.py label skips a finished shard).
          L4: use a VM that is already RUNNING, else start od-l4b (us-east4-c), on STOCKOUT / quota od-l4
          (us-central1-a); if both fail, retry every 20 min. A VM this monitor started is stopped after each read
          (unless the next snapshot is due within 30 min or another od_gcp.py job runs on it) and at exit.
  status  print the state and the last log lines.
  cputest run tests/test_snap_monitor.py (fakes only) and write logs/snap_monitor_cputest.json (pass, sha256s).
  score <snapshot labels dir>   CPU: score one fetched snapshot read against C1 (no rule action).

Snapshots are read ONLY on the old slice (never the sealed suite, dev gate splits, OHS, ejs-5, JevBench, LongBench) and
are never candidates. Not covered here (report-only monitors of recipe 5, never part of the rule): the mix-tuning dev,
the B3 yes-share alarm at T = 1 and KL on 2,000 new rows have no shard sets yet; FAM-1 25/50/75% reads are separate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
LOGS = HERE / "logs"
PY = str(LEAN.parent / ".venv/bin/python")
MODAL = str(LEAN.parent / ".venv/bin/modal")
VOLUME = "opendecide"
FRACS = ("0.25", "0.5", "0.75")
OLD_DROP_PP, PYES_DRIFT = 1.5, 0.02
C1 = "q35_4b_main500k"
OLD_DIR = LEAN / "data/c_old_slice_shards"
OLD_SHARDS_SHA = "9118d6b58466d301da0bb2dd5a197d164dcc933154e16d2dfcc9e555e3fa63d8"   # shards.json (L4_REPLAY_READ.sh)
OLD_ROWS_SHA = "d2bd19c55625162b62988e21a519868c41c612972356dab5d3425874158458a6"     # shard_000.jsonl
BASE, REV, LAYOUT = "Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a", "schema_branch_mark"
PROJECT = "system-one-509903"
VMS = (("od-l4b", "us-east4-c"), ("od-l4", "us-central1-a"))
CODE = ("od_gcp.py", "decoder_io.py", "shard_golden.py", "train_decoder.py", "prism_x.py", "writeblock.py")
STOCKOUT = ("ZONE_RESOURCE_POOL_EXHAUSTED", "STOCKOUT", "does not have enough resources", "QUOTA_EXCEEDED",
            "GPUS_ALL_REGIONS", "Quota")
POLL_S, RETRY_S, READ_POLL_S, READ_MAX_S, PRESTART_MIN, KEEP_MIN = 300, 1200, 60, 75 * 60, 25, 30
READ_FAIL_CAP = 3               # failed reads of one snapshot before the monitor escalates (stops the relay app)
STATE, JSONL, STOPREC = LOGS / "snap_monitor_state.json", LOGS / "snap_monitor.jsonl", LOGS / "snap_monitor_stop.json"
ESCREC = LOGS / "snap_monitor_escalation.json"
CPUTEST = LOGS / "snap_monitor_cputest.json"
TEST = HERE / "tests/test_snap_monitor.py"


def sha_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read_jsonl(p) -> list[dict]:
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


# ---- scoring (CPU) --------------------------------------------------------------------------------------------------
def score_row(r: dict, pr: dict) -> float:
    """gate_dev.score: argmax correct, a tie for the top counts as wrong."""
    keys, g = (["yes", "no"], "yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else (r["options"], r["gold"])
    p = {k: float(pr.get(k, 0.0)) for k in keys}
    best = max(p.values())
    return float([k for k, v in p.items() if v == best] == [g])


def p_yes(pr: dict) -> float:
    y, n = float(pr.get("yes", 0.0)), float(pr.get("no", 0.0))
    return y / (y + n) if y + n > 0 else 0.5


def kl(r: dict, p: dict, q: dict) -> float:
    keys = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
    a = [max(float(p.get(k, 0.0)), 0.0) for k in keys]
    b = [max(float(q.get(k, 0.0)), 0.0) for k in keys]
    sa, sb = sum(a) or 1.0, sum(b) or 1.0
    return sum((x / sa) * math.log((x / sa + 1e-12) / (y / sb + 1e-12)) for x, y in zip(a, b) if x > 0)


def stats(rows: list[dict], ref: dict, snap: dict) -> dict:
    miss = [r["id"] for r in rows if r["id"] not in ref or r["id"] not in snap]
    if miss:
        raise ValueError(f"{len(miss)} old-slice rows without a prediction (first {miss[0]})")
    ok_r = [score_row(r, ref[r["id"]]) for r in rows]
    ok_s = [score_row(r, snap[r["id"]]) for r in rows]
    yn = [r for r in rows if r["qtype"] == "noul"]
    n = len(rows)
    py_r = sum(p_yes(ref[r["id"]]) for r in yn) / len(yn) if yn else float("nan")
    py_s = sum(p_yes(snap[r["id"]]) for r in yn) / len(yn) if yn else float("nan")
    return {"n": n, "n_yesno": len(yn), "acc_c1": 100 * sum(ok_r) / n, "acc_snap": 100 * sum(ok_s) / n,
            "acc_diff_pp": 100 * (sum(ok_s) - sum(ok_r)) / n,
            "flips_1to0": int(sum(a > b for a, b in zip(ok_r, ok_s))),
            "flips_0to1": int(sum(b > a for a, b in zip(ok_r, ok_s))),
            "pyes_c1": py_r, "pyes_snap": py_s, "pyes_drift": py_s - py_r,
            "kl_c1_snap": sum(kl(r, ref[r["id"]], snap[r["id"]]) for r in rows) / n}


def rule(reads: dict) -> tuple[bool, list[str]]:
    """The pre-registered stop rule on the finished snapshot reads {frac: stats}."""
    why = []
    low = {f: s["acc_diff_pp"] < -OLD_DROP_PP - 1e-9 for f, s in reads.items()}
    if low.get("0.25") and low.get("0.5"):
        why.append(f"old slice below C1 - {OLD_DROP_PP} pp at both 25% ({reads['0.25']['acc_diff_pp']:+.2f}) and 50% "
                   f"({reads['0.5']['acc_diff_pp']:+.2f})")
    for f, s in sorted(reads.items()):
        if abs(s["pyes_drift"]) > PYES_DRIFT + 1e-12:
            why.append(f"mean P(yes) on old yes/no rows drifted {s['pyes_drift']:+.4f} (> {PYES_DRIFT}) at "
                       f"{float(f):.0%}")
    return bool(why), why


def load_labels(d: Path, shard: Path) -> tuple[dict, dict]:
    lp, mp = d / shard.name, d / (shard.name[:-len(".jsonl")] + ".meta.json")
    if not (lp.exists() and mp.exists()):
        raise ValueError(f"{d.name}: label file or meta missing")
    meta = json.loads(mp.read_text())
    labs = read_jsonl(lp)
    if meta.get("shard_sha256") != sha_file(shard) or meta.get("rows") != len(labs):
        raise ValueError(f"{d.name}: labels are not of this old-slice shard (sha / rows)")
    return {x["id"]: x["probs"] for x in labs}, meta


def check_settings(meta: dict, ref_meta: dict, name: str) -> list[str]:
    """Same readout as C1's old-slice read (everything but the name); raises on a readout difference. Returns flags
    (report only): a different chat-template sha."""
    want = {**ref_meta["settings"], "name": name}
    if meta.get("settings") != want:
        raise ValueError(f"{name}: read with other settings {meta.get('settings')} (want {want})")
    flags = []
    t, tr = (meta.get("load") or {}).get("chat_template_sha"), (ref_meta.get("load") or {}).get("chat_template_sha")
    if t != tr:
        flags.append(f"chat_template_sha {str(t)[:12]} != C1's {str(tr)[:12]}")
    return flags


class OldSlice:
    def __init__(self, d: Path = OLD_DIR, shards_sha: str = OLD_SHARDS_SHA, rows_sha: str = OLD_ROWS_SHA):
        man = d / "shards.json"
        if sha_file(man) != shards_sha:
            raise SystemExit(f"{man}: sha256 is not the pinned old slice")
        m = json.loads(man.read_text())
        if len(m["shards"]) != 1:
            raise SystemExit("old slice: one shard expected")
        self.dir, self.shard = d, d / m["shards"][0]["file"]
        if sha_file(self.shard) != rows_sha:
            raise SystemExit(f"{self.shard}: sha256 is not the pinned old slice")
        self.rows = read_jsonl(self.shard)
        self.ref, self.ref_meta = load_labels(d / f"labels_{C1}", self.shard)
        if self.ref_meta["settings"].get("name") != C1 or not self.ref_meta["settings"].get("tta_choice"):
            raise SystemExit("C1's old-slice read is not the A5 readout of C1")


# ---- side effects (the CPU test replaces these) ---------------------------------------------------------------------
class Ops:
    def __init__(self, profile: str, seg3_log: Path = LOGS / "r1_seg3.log"):
        self.profile, self.seg3_log = profile, seg3_log

    def _run(self, argv: list[str], timeout: float, env: dict | None = None) -> tuple[int, str]:
        try:
            r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, env=env)
            return r.returncode, (r.stdout or "") + (r.stderr or "")
        except subprocess.TimeoutExpired:
            return 124, "timeout"

    def modal(self, args: list[str], timeout: float = 120) -> tuple[int, str]:
        return self._run([MODAL, *args], timeout, {**os.environ, "MODAL_PROFILE": self.profile})

    def gcloud(self, args: list[str], timeout: float = 300) -> tuple[int, str]:
        return self._run(["gcloud", *args], timeout)

    def sleep(self, s: float) -> None:
        time.sleep(s)

    def now(self) -> float:
        return time.time()

    # Modal (control plane / Volume only: no compute)
    def list_snaps(self, name: str) -> list[int]:
        rc, out = self.modal(["volume", "ls", VOLUME, f"models/{name}/snaps", "--json"])
        if rc != 0:
            return []
        steps = set()
        try:
            items = json.loads(out[out.index("["):]) if "[" in out else []
            texts = [v for it in items for v in (it.values() if isinstance(it, dict) else [it]) if isinstance(v, str)]
        except ValueError:
            texts = out.split()
        for t in texts:
            m = re.search(r"(?:^|/)s(\d{6})/?$", t.strip())
            if m:
                steps.add(int(m.group(1)))
        return sorted(steps)

    def get(self, remote: str, dest: Path) -> None:
        dest.mkdir(parents=True, exist_ok=True)
        rc, out = self.modal(["volume", "get", VOLUME, remote, str(dest) + "/"], timeout=900)
        if rc != 0:
            raise RuntimeError(f"modal volume get {remote}: rc {rc}: {out[-200:]}")

    def running_apps(self) -> list[str]:
        rc, out = self.modal(["app", "list", "--json"], timeout=90)
        ids = []
        try:
            for a in json.loads(out[out.index("["):]) if "[" in out else []:
                state = str(a.get("State") or a.get("state") or "").lower()
                if state != "stopped" and (int(a.get("Tasks") or a.get("tasks") or 0) > 0 or "ephemeral" in state
                                           or "detached" in state or "deployed" in state):
                    ids.append(a.get("App ID") or a.get("app_id"))
        except ValueError:
            pass
        return [i for i in ids if i]

    def stop_app(self, name: str) -> dict:
        """Stop the round-1 relay app on the card-only account: the id in r1_seg3.log plus every running app."""
        ids = []
        seg3 = self.seg3_log
        if seg3.exists():
            ids += re.findall(r"\bap-[A-Za-z0-9]{6,}\b", seg3.read_text(errors="replace"))[-1:]
        ids += self.running_apps()
        ids = list(dict.fromkeys(ids))
        calls, left = [], ids
        for attempt in range(3):
            for i in left:
                rc, out = self.modal(["app", "stop", "-y", i], timeout=90)
                calls.append({"app": i, "rc": rc, "out": out[-120:]})
            self.sleep(20)
            left = self.running_apps()
            if not left:
                break
        return {"app_ids": ids, "calls": calls, "still_running": left}

    def ledger(self, text: str) -> None:
        sys.path.insert(0, str(HERE))
        import spend_guard
        try:
            spend_guard.ledger(self.profile, text, "card")
        except Exception as e:  # noqa: BLE001 - the stop matters more than the ledger line
            with open(LEAN / "logs/budget_ledger.md", "a") as f:
                f.write(f"| {text} | {time.strftime('%d %b %H:%M', time.gmtime())} UTC, {self.profile} | billing "
                        f"call failed ({type(e).__name__}) | card |\n")


# ---- the L4 VM ----------------------------------------------------------------------------------------------------
class L4:
    def __init__(self, ops: Ops, state: dict):
        self.ops, self.state = ops, state
        self.vm: tuple[str, str] | None = tuple(state["vm"]) if state.get("vm") else None
        self.prepared = False

    def _g(self, args, timeout=300):
        return self.ops.gcloud([*args, "--project", PROJECT], timeout)

    def status(self, vm, zone) -> str:
        rc, out = self._g(["compute", "instances", "describe", vm, "--zone", zone, "--format=value(status)"], 120)
        return out.strip().splitlines()[-1] if rc == 0 and out.strip() else "UNKNOWN"

    def ssh(self, cmd: str, timeout=300) -> tuple[int, str]:
        vm, zone = self.vm
        return self._g(["compute", "ssh", vm, "--zone", zone, "--quiet", "--command", cmd], timeout)

    def scp(self, src: str, dst: str, timeout=1200) -> tuple[int, str]:
        return self._g(["compute", "scp", "--recurse", "--zone", self.vm[1], "--quiet", src, dst], timeout)

    def ensure_up(self, log) -> bool:
        """A RUNNING VM if there is one (global GPU quota 1), else start od-l4b, then od-l4 on STOCKOUT / quota."""
        if self.vm and self.status(*self.vm) == "RUNNING":
            return True
        bad = set(self.state.get("bad_vms") or [])
        for vm, zone in VMS:
            if vm not in bad and self.status(vm, zone) == "RUNNING":
                self.vm, self.prepared = (vm, zone), False
                self.state["vm"] = list(self.vm)
                log("vm", vm=vm, how="already running")
                return self._ready(log)
        for vm, zone in VMS:
            if vm in bad:
                continue
            rc, out = self._g(["compute", "instances", "start", vm, "--zone", zone], 400)
            if rc == 0:
                self.vm, self.prepared = (vm, zone), False
                self.state["vm"], self.state["vm_started_by_us"] = list(self.vm), vm
                log("vm", vm=vm, how="started")
                return self._ready(log)
            kind = "stockout" if any(s.lower() in out.lower() for s in STOCKOUT) else "error"
            log("vm_start_failed", vm=vm, zone=zone, kind=kind, out=out.strip()[-160:])
        self.vm = None
        self.state["vm"] = None
        return False

    def _ready(self, log) -> bool:
        for _ in range(10):
            if self.ssh("echo ok", 90)[0] == 0:
                return True
            self.ops.sleep(20)
        log("vm_ssh_failed", vm=self.vm[0])
        return False

    def busy_other(self, snap: str | None = None) -> bool:
        rc, out = self.ssh("pgrep -fa '[o]d_gcp.py' || true", 120)
        jobs = [l for l in out.splitlines() if "od_gcp.py" in l]
        return any(snap is None or f"--name {snap}" not in l for l in jobs)

    def prepare(self, old: OldSlice, log) -> None:
        if self.prepared:
            return
        files = [*CODE, f"data/{old.dir.name}/{old.shard.name}", f"data/{old.dir.name}/shards.json"]
        rc, out = self.ssh(
            f"mkdir -p ~/lean/data/{old.dir.name} ~/lean/models ~/lean/logs && cd ~/lean && "
            f"(ls -d ~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/{REV} >/dev/null 2>&1 && echo BASE_OK "
            f"|| echo BASE_MISSING) && (test -x ~/od/bin/python && echo PY_OK || echo PY_MISSING) && "
            f"(sha256sum {' '.join(files)} 2>/dev/null || true)", 180)
        if rc != 0 or "BASE_OK" not in out or "PY_OK" not in out:
            name = self.vm[0]
            if rc == 0:                                   # a VM without the pinned base or env: never use it again
                self.state["bad_vms"] = sorted(set(self.state.get("bad_vms") or []) | {self.vm[0]})
                self.stop_if_ours(log, "not usable for a read")
            raise RuntimeError(f"VM {name} not usable for a read (base snapshot / python): {out.strip()[-160:]}")
        have = {}
        for line in out.splitlines():
            parts = line.split()
            if len(parts) == 2 and re.fullmatch(r"[0-9a-f]{64}", parts[0]):
                have[parts[1]] = parts[0]
        local = {f: (LEAN / f if f in CODE else old.dir / Path(f).name) for f in files}
        push = [f for f in files if have.get(f) != sha_file(local[f])]
        for f in push:
            dst = "~/lean/" if f in CODE else f"~/lean/data/{old.dir.name}/"
            rc, o = self.scp(str(local[f]), f"{self.vm[0]}:{dst}", 600)
            if rc != 0:
                raise RuntimeError(f"push {f}: {o.strip()[-160:]}")
        log("vm_prepared", vm=self.vm[0], pushed=push)
        self.prepared = True

    def stop_if_ours(self, log, why: str) -> None:
        mine = self.state.get("vm_started_by_us")
        if not (self.vm and mine == self.vm[0]):
            return
        if self.status(*self.vm) == "RUNNING" and self.busy_other():
            log("vm_left_running", vm=self.vm[0], why="another od_gcp.py job runs on it")
            return
        rc, out = self._g(["compute", "instances", "stop", self.vm[0], "--zone", self.vm[1]], 400)
        log("vm_stop", vm=self.vm[0], rc=rc, why=why)
        if rc == 0:
            self.state["vm_started_by_us"], self.state["vm"], self.vm = None, None, None


# ---- the monitor ----------------------------------------------------------------------------------------------------
class Monitor:
    def __init__(self, ops: Ops, name: str, old: OldSlice, local: Path = HERE / "snaps", logs: Path = LOGS):
        self.ops, self.name, self.old, self.local, self.logs = ops, name, old, local, logs
        self.state_p, self.jsonl, self.stop_p = logs / STATE.name, logs / JSONL.name, logs / STOPREC.name
        self.esc_p = logs / ESCREC.name
        self.state = json.loads(self.state_p.read_text()) if self.state_p.exists() else {}
        self.state.setdefault("name", name)
        self.state.setdefault("reads", {})
        self.state.setdefault("attempts", {})
        self.state.setdefault("failures", {})
        if self.state["name"] != name:
            raise SystemExit(f"{self.state_p} belongs to {self.state['name']}, not {name}")
        self.l4 = L4(ops, self.state)

    def log(self, ev: str, **kw) -> None:
        self.logs.mkdir(parents=True, exist_ok=True)
        rec = {"t": round(self.ops.now()), "ev": ev, **kw}
        with open(self.jsonl, "a") as f:
            f.write(json.dumps(rec, default=str) + "\n")
        print(json.dumps(rec, default=str)[:300], flush=True)

    def save(self) -> None:
        self.state_p.write_text(json.dumps(self.state, indent=1, default=str))

    # n_steps and progress
    def n_steps(self, steps: list[int]) -> int | None:
        if self.state.get("n_steps"):
            return self.state["n_steps"]
        if not steps:
            return None
        s0 = min(steps)
        tmp = self.local / f".meta_s{s0:06d}"
        shutil.rmtree(tmp, ignore_errors=True)
        self.ops.get(f"models/{self.name}/snaps/s{s0:06d}/train_meta.json", tmp)
        m = json.loads(next(tmp.rglob("train_meta.json")).read_text())
        shutil.rmtree(tmp, ignore_errors=True)
        n = int(m["steps"])
        if int(m.get("snapshot_step", s0)) != s0:
            raise RuntimeError(f"s{s0:06d}/train_meta.json says snapshot_step {m.get('snapshot_step')}")
        self.state["n_steps"] = n
        self.log("n_steps", n_steps=n, targets={f: int(float(f) * n) for f in FRACS})
        return n

    def eta_min(self, step: int) -> float | None:
        """Minutes until the trainer reaches `step`, from the last two step records in logs/r1_seg3.log."""
        p = self.logs / "r1_seg3.log"
        if not p.exists():
            return None
        recs = []
        for line in p.read_text(errors="replace").splitlines()[-400:]:
            m = re.search(r'"step": (\d+).*?"min": ([0-9.]+)', line)
            if m:
                recs.append((int(m.group(1)), float(m.group(2))))
        if len(recs) < 2 or recs[-1][0] <= recs[-2][0] or recs[-1][1] <= recs[-2][1]:
            return None                                  # too few records, or the clock restarted (preemption)
        (s1, m1), (s2, m2) = recs[-2], recs[-1]
        return max(0.0, (step - s2) * (m2 - m1) / (s2 - s1))

    def final_exists(self) -> bool:
        return (LEAN / f"logs/relay_{self.name}_final.json").exists()

    # one snapshot read
    def snap_name(self, step: int) -> str:
        return f"snap_{self.name}_s{step:06d}"

    def fetch_snapshot(self, step: int) -> Path:
        snap = self.snap_name(step)
        dst = self.local / snap
        if (dst / "adapter_model.safetensors").exists() and (dst / ".complete").exists():
            return dst
        stage = self.local / f".stage_{snap}"
        shutil.rmtree(stage, ignore_errors=True)
        self.ops.get(f"models/{self.name}/snaps/s{step:06d}", stage)
        got = next((p.parent for p in stage.rglob("adapter_model.safetensors")), None)
        if got is None or not (got / "train_meta.json").exists():
            raise RuntimeError(f"s{step:06d}: no adapter_model.safetensors / train_meta.json on the Volume")
        m = json.loads((got / "train_meta.json").read_text())
        if int(m.get("snapshot_step", -1)) != step or not isinstance(m.get("cfg"), dict):
            raise RuntimeError(f"s{step:06d}: train_meta snapshot_step {m.get('snapshot_step')} / no cfg")
        shutil.rmtree(dst, ignore_errors=True)
        got.rename(dst)
        shutil.rmtree(stage, ignore_errors=True)
        (dst / ".complete").write_text(sha_file(dst / "adapter_model.safetensors") + "\n")
        return dst

    def read_on_l4(self, snap: str, local_dir: Path) -> Path:
        """od_gcp.py label of the old slice with the snapshot (resumable), then fetch the labels. Returns the dir."""
        l4, od = self.l4, self.old.dir.name
        self.l4.prepare(self.old, self.log)
        want = sha_file(local_dir / "adapter_model.safetensors")
        rc, out = l4.ssh(f"sha256sum ~/lean/models/{snap}/adapter_model.safetensors 2>/dev/null || echo NONE", 120)
        if want not in out:
            rc, o = l4.scp(str(local_dir), f"{l4.vm[0]}:~/lean/models/", 1200)
            if rc != 0:
                raise RuntimeError(f"push {snap}: {o.strip()[-160:]}")
        lab = f"data/{od}/labels_{snap}"
        cmd = (f"cd ~/lean && if test -f {lab}/{self.old.shard.name[:-6]}.meta.json; then echo DONE; "
               f"elif pgrep -f 'label --name [{snap[0]}]{snap[1:]} ' >/dev/null; then echo RUNNING; "
               f"elif pgrep -f '[o]d_gcp.py' >/dev/null; then echo BUSY; "
               f"else HF_HUB_OFFLINE=1 setsid nohup ~/od/bin/python od_gcp.py label --name {snap} --base {BASE} "
               f"--revision {REV} --layout {LAYOUT} --shards-dir data/{od} --tta-choice "
               f"> logs/snapmon_{snap}.log 2>&1 < /dev/null & echo LAUNCHED; fi")
        t0, launches = self.ops.now(), 0
        while True:
            rc, out = l4.ssh(cmd, 120)
            word = next((w for w in ("DONE", "RUNNING", "BUSY", "LAUNCHED") if w in out), "ERR")
            if word == "DONE":
                break
            if word == "LAUNCHED":
                launches += 1
                self.log("read_launched", snap=snap, vm=l4.vm[0], n=launches)
                if launches > 3:
                    _, tail = l4.ssh(f"tail -n 3 ~/lean/logs/snapmon_{snap}.log", 60)
                    raise RuntimeError(f"{snap}: label job failed 3 times: {tail.strip()[-200:]}")
            elif word == "BUSY":
                self.log("vm_busy", vm=l4.vm[0], why="another od_gcp.py job; waiting (one job at a time)")
            elif word == "ERR" and l4.status(*l4.vm) != "RUNNING":
                self.log("vm_lost", vm=l4.vm[0])
                if not l4.ensure_up(self.log):
                    raise RuntimeError("VM lost and no L4 available")
                l4.prepare(self.old, self.log)
                return self.read_on_l4(snap, local_dir)
            if self.ops.now() - t0 > READ_MAX_S:
                raise RuntimeError(f"{snap}: read not done after {READ_MAX_S // 60} min")
            self.ops.sleep(READ_POLL_S)
        out_dir = self.local / "labels"
        out_dir.mkdir(parents=True, exist_ok=True)
        shutil.rmtree(out_dir / f"labels_{snap}", ignore_errors=True)
        rc, o = l4.scp(f"{l4.vm[0]}:~/lean/{lab}", str(out_dir) + "/", 600)
        if rc != 0:
            raise RuntimeError(f"fetch labels of {snap}: {o.strip()[-160:]}")
        return out_dir / f"labels_{snap}"

    def process(self, frac: str, step: int) -> bool:
        snap = self.snap_name(step)
        self.state["attempts"][frac] = self.state["attempts"].get(frac, 0) + 1
        self.save()
        local_dir = self.fetch_snapshot(step)
        if not self.l4.ensure_up(self.log):
            self.log("no_l4", frac=frac, retry_min=RETRY_S // 60, why="both zones stocked out / quota / error")
            self.ops.sleep(RETRY_S)
            return False
        labels = self.read_on_l4(snap, local_dir)
        snap_p, meta = load_labels(labels, self.old.shard)
        flags = check_settings(meta, self.old.ref_meta, snap)
        s = stats(self.old.rows, self.old.ref, snap_p)
        s.update(step=step, snap=snap, vm=self.l4.vm[0], flags=flags, read_sec=meta.get("sec"),
                 adapter_sha256=sha_file(local_dir / "adapter_model.safetensors"))
        self.state["reads"][frac] = s
        self.save()
        self.log("read", frac=frac, **{k: (round(v, 4) if isinstance(v, float) else v) for k, v in s.items()})
        return True

    def act(self, why: list[str]) -> None:
        after_final = self.final_exists()
        rec = {"fired": True, "why": why, "reads": self.state["reads"], "unix": round(self.ops.now()),
               "after_final": after_final,
               "candidate": "none: recipe 5, a run the stop rule stops yields no candidate for this round; the owner "
                            "reviews; a re-run needs an amendment; keep the last good snapshot for diagnosis only"}
        if after_final:
            rec["app_stop"] = "not needed: the run had already ended (the reads came late); owner review before any gate"
        else:
            rec["app_stop"] = self.ops.stop_app(self.name)
        self.state["fired"] = True
        self.save()
        self.stop_p.write_text(json.dumps(rec, indent=1, default=str))
        self.log("STOP_RULE_FIRED", why=why, after_final=after_final,
                 app_stop=rec["app_stop"] if isinstance(rec["app_stop"], str) else rec["app_stop"]["app_ids"])
        self.ops.ledger(f"round 1 (C r1): recipe-5 STOP RULE fired ({'; '.join(why)[:160]}); "
                        f"{'run already ended' if after_final else 'relay app stopped'}; no candidate this round")

    def read_failed(self, frac: str, step: int, e: Exception) -> bool:
        """Count one failed read of a snapshot; at READ_FAIL_CAP escalate (stop the relay app). True if escalated."""
        n = self.state["failures"][frac] = self.state["failures"].get(frac, 0) + 1
        self.save()
        self.log("read_failed", frac=frac, step=step, n=n, cap=READ_FAIL_CAP, kind=type(e).__name__, msg=str(e)[:200])
        if n < READ_FAIL_CAP:
            return False
        after_final = self.final_exists()
        rec = {"escalated": True, "frac": frac, "step": step, "failures": n, "last_error": f"{type(e).__name__}: "
               f"{str(e)[:300]}", "unix": round(self.ops.now()), "after_final": after_final,
               "candidate": "none until the owner decides: the recipe-5 stop rule could not be checked on this "
                            "snapshot (gate_c refuses a run whose 25/50/75% reads are incomplete)"}
        rec["app_stop"] = ("not needed: the run had already ended" if after_final else self.ops.stop_app(self.name))
        self.state["escalated"] = {k: rec[k] for k in ("frac", "step", "failures", "unix")}
        self.save()
        self.esc_p.write_text(json.dumps(rec, indent=1, default=str))
        self.log("ESCALATED", frac=frac, step=step, failures=n, after_final=after_final,
                 app_stop=rec["app_stop"] if isinstance(rec["app_stop"], str) else rec["app_stop"].get("app_ids"))
        self.ops.ledger(f"round 1 (C r1): snap_monitor ESCALATED: the {frac} snapshot (s{step:06d}) failed {n} reads; "
                        f"{'run already ended' if after_final else 'relay app stopped'}; owner decides")
        return True

    def run(self, max_hours: float = 14.0) -> int:
        end = self.ops.now() + max_hours * 3600
        self.log("start", name=self.name, profile=self.ops.profile, done=sorted(self.state["reads"]),
                 fired=bool(self.state.get("fired")))
        rc = 0
        try:
            while self.ops.now() < end and not self.state.get("fired") and not self.state.get("escalated"):
                try:
                    steps = self.ops.list_snaps(self.name)
                    n = self.n_steps(steps)
                    if n:
                        todo = [(f, int(float(f) * n)) for f in FRACS if f not in self.state["reads"]]
                        if not todo:
                            self.log("done", why="25/50/75% read, rule did not fire")
                            break
                        for f, st in todo:
                            if st not in steps:
                                break
                            try:
                                ok = self.process(f, st)
                            except Exception as e:  # noqa: BLE001 - a failed read of this snapshot
                                if self.read_failed(f, st, e):
                                    break
                                raise
                            if not ok:
                                break
                            fired, why = rule(self.state["reads"])
                            if fired:
                                self.act(why)
                                break
                        if self.state.get("fired") or self.state.get("escalated"):
                            break
                        todo = [(f, st) for f, st in todo if f not in self.state["reads"]]
                        if todo and self.l4.vm is None:
                            eta = self.eta_min(todo[0][1])
                            if eta is not None and eta <= PRESTART_MIN:
                                self.l4.ensure_up(self.log)
                        if self.l4.vm and todo:
                            eta = self.eta_min(todo[0][1])
                            if eta is None or eta > KEEP_MIN:
                                self.l4.stop_if_ours(self.log, f"next snapshot not due within {KEEP_MIN} min")
                        missing = [f for f, st in todo if st not in steps]
                        if missing and self.final_exists():
                            self.log("ended", why="final written but a frac snapshot is missing on the Volume",
                                     missing=missing)
                            rc = 1
                            break
                    elif self.final_exists():
                        self.log("ended", why="final written and no snapshot found")
                        rc = 1
                        break
                except Exception as e:  # noqa: BLE001 - keep watching; every error is logged
                    self.log("error", kind=type(e).__name__, msg=str(e)[:300])
                    self.state["errors"] = self.state.get("errors", 0) + 1
                    self.save()
                    if self.l4.vm:
                        self.l4.prepared = False
                self.save()
                if not self.state.get("fired") and not self.state.get("escalated"):
                    self.ops.sleep(POLL_S)
            else:
                if not self.state.get("fired") and not self.state.get("escalated"):
                    self.log("timeout", max_hours=max_hours, reads=sorted(self.state["reads"]))
                    rc = 1
        finally:
            self.l4.stop_if_ours(self.log, "monitor exit")
            self.save()
        return 3 if self.state.get("fired") else 4 if self.state.get("escalated") else rc


# ---- CLI ------------------------------------------------------------------------------------------------------------
def lock(logs: Path) -> Path:
    p = logs / "snap_monitor.pid"
    if p.exists():
        try:
            pid = int(p.read_text().strip())
            os.kill(pid, 0)
            raise SystemExit(f"another snap_monitor runs (pid {pid})")
        except (ValueError, ProcessLookupError, PermissionError):
            pass
    logs.mkdir(parents=True, exist_ok=True)
    p.write_text(str(os.getpid()))
    return p


def cputest() -> int:
    r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(TEST)], cwd=str(LEAN),
                       capture_output=True, text=True, timeout=140)
    last = [l for l in (r.stdout or "").splitlines() if l.strip()][-1:] or [""]
    rec = {"pass": r.returncode == 0, "summary": last[0][-200:], "snap_monitor_sha256": sha_file(__file__),
           "test_sha256": sha_file(TEST), "unix": round(time.time())}
    LOGS.mkdir(parents=True, exist_ok=True)
    CPUTEST.write_text(json.dumps(rec, indent=1) + "\n")
    print(rec["summary"])
    print("PASS" if rec["pass"] else "FAIL")
    return 0 if rec["pass"] else 1


def cputest_ok(path: Path = CPUTEST) -> str | None:
    """None if the CPU test record passes AND vouches for the current snap_monitor.py and test file, else why not."""
    try:
        rec = json.loads(path.read_text())
    except Exception:  # noqa: BLE001
        return "no logs/snap_monitor_cputest.json"
    if rec.get("pass") is not True:
        return "snap_monitor CPU test did not pass"
    if rec.get("snap_monitor_sha256") != sha_file(HERE / "snap_monitor.py") or rec.get("test_sha256") != sha_file(TEST):
        return "snap_monitor.py or its test changed after the CPU test (run snap_monitor.py cputest)"
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="recipe 5 stop-rule driver (RUNBOOK D5)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("watch")
    w.add_argument("--profile", default="aryamhd")
    w.add_argument("--name", default="q35_4b_c_r1")
    w.add_argument("--max-hours", dest="max_hours", type=float, default=14.0)
    sub.add_parser("status")
    sub.add_parser("cputest")
    s = sub.add_parser("score")
    s.add_argument("labels_dir")
    a = ap.parse_args(argv)
    if a.cmd == "cputest":
        return cputest()
    if a.cmd == "status":
        st = json.loads(STATE.read_text()) if STATE.exists() else {}
        print(json.dumps({k: st.get(k) for k in ("name", "n_steps", "fired", "escalated", "failures", "vm", "errors")}))
        for f, r in sorted((st.get("reads") or {}).items()):
            print(f"{f}: acc {r['acc_diff_pp']:+.2f} pp, P(yes) drift {r['pyes_drift']:+.4f}, KL {r['kl_c1_snap']:.4f}")
        for line in (JSONL.read_text().splitlines()[-5:] if JSONL.exists() else []):
            print(line[:200])
        return 0
    if a.cmd == "watch" and a.profile != "aryamhd":
        raise SystemExit("round 1 runs on aryamhd only (owner rule)")
    old = OldSlice()
    if a.cmd == "score":
        d = Path(a.labels_dir)
        p, meta = load_labels(d, old.shard)
        flags = check_settings(meta, old.ref_meta, meta["settings"]["name"])
        print(json.dumps({**stats(old.rows, old.ref, p), "flags": flags}))
        return 0
    lk = lock(LOGS)
    try:
        return Monitor(Ops(a.profile), a.name, old).run(a.max_hours)
    finally:
        lk.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
