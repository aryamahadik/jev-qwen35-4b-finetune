"""oc1.common (round 2, H100 window of 17 Oct 2026): constants, payer guard, path guard, money (rates + budget governor), stats helpers.

Copied from lean/speed/opt_c1_20261017/oc1/common.py (read-only original); only the paths, the app name and the ledger moved:
ledger = h100/ledger.json (FRESH: cap USD 5.00, stop-launch 4.50, hard cancel 4.80; the 17 Oct ledger does not count).

Standard library only (this module is imported on the laptop, in the Modal function process and in the runner process).

HARD RULES encoded here:
  * Modal profile: jaypatil-duke ONLY (payer_guard). Never mahadikarya2/3/44, never aryamhd.
  * Money: hard cap USD 5.00 for everything (GPU + CPU + memory). Budget: stop launching at 4.50, cancel and stop all
    apps at 4.80. The estimate is container seconds x rate (rates from `modal billing rates`, 17 Oct), conservative.
  * Data: dev data only. safe_path() refuses any path that contains "ohs" (any case), "sealed", "c_spec/sealed_brief",
    "c_build/preread", "bench/external_quarantine", "bench/longbench_v2" or ".claude".
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import statistics
import sys
import time
from pathlib import Path

def _up(p: Path, n: int, default: str) -> Path:
    try:
        return p.parents[n]
    except IndexError:  # in a container the package sits at /root/oc1: there is no lean/ tree
        return Path(default)


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # .../lean/speed/opt_c1_round2_20261017/h100   (container: /root)
LEAN = _up(ROOT, 2, "/nonexistent-lean")        # .../lean
JEV_ROOT = _up(LEAN, 1, "/nonexistent-jev")     # .../jev   (LEAN.parents[1] = opendecide-data's parent)
OLD_ROOT = LEAN / "speed" / "opt_c1_20261017"   # the 17 Oct harness: data/, read-only
OLD_DATA = OLD_ROOT / "data"                    # P S N R workloads, vision_pack, SPEED-2 reference answers
RESULTS = ROOT / "results"
LEDGER = ROOT / "ledger.json"

# ------------------------------------------------------------------ identities
PROFILE = "jaypatil-duke"
FORBIDDEN_PROFILES = ("mahadikarya2", "mahadikarya3", "mahadikarya44", "aryamhd", "atmosphor", "arya-mahadik-ai")
BASE = "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
C1_MODEL = "q35_4b_main500k"
C1_ADAPTER_SHA256 = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
MERGED_NAME = "q35_4b_main500k_merged"
SGLANG_IMAGE = "lmsysorg/sglang:v0.5.20-cu130"   # S1's image (think/modal_think.py B1a, hosting/sglang_host.py)
SGLANG_VERSION = "0.5.20"
UV_PIN = "uv==0.12.23"
FASTPATH_PY = "/opt/fastpath/bin/python"
OLD_VOLUME = "opendecide"        # jaypatil-duke's existing Volume: adapter + HF cache, mounted READ-ONLY
NEW_VOLUME = "oc1-opt-20261017"  # jaypatil-duke Volume of the 17 Oct task: the merged C1 checkpoint; the block-FP8 checkpoint + this window's results go here
APP_NAME = "oc1-r2-h100-20261017"

# ------------------------------------------------------------------ money
CAP_USD = 5.00
STOP_LAUNCH_USD = 4.50
HARD_STOP_USD = 4.80
# `modal billing rates` 17 Oct 2026 (jaypatil-duke): CPU 0.0473/core/h, memory 0.008/GiB/h, GPUs per hour.
RATES = {
    "cpu_core_h": 0.0473,
    "mem_gib_h": 0.008,
    "gpu_h": {"H100": 3.95, "H200": 4.54, "A100-80GB": 2.50, "A100-40GB": 2.10, "L40S": 1.95, "A10G": 1.10, "L4": 0.80,
              "T4": 0.59, "B200": 6.25},
}
# modal_direct_host.REGION_MULT: any 1.0, broad (us/eu/ap) 1.15, narrow (us-east ...) 1.75, "to be confirmed". The
# governor uses the conservative values (broad 1.25) so that an under-estimate cannot let the cap be crossed.
REGION_MULT_CONSERVATIVE = {"any": 1.0, "us": 1.25, "eu": 1.25, "ap": 1.25, "narrow": 1.75}
CONTAINER_OVERHEAD_S = 45.0   # per container: start + volume mounts are billed, image pull is not (conservative)


def region_mult(region: str | None) -> float:
    if not region or region == "any":
        return REGION_MULT_CONSERVATIVE["any"]
    return REGION_MULT_CONSERVATIVE.get(region, REGION_MULT_CONSERVATIVE["narrow"])


def container_rate_usd_h(gpu: str | None, cpu: float, mem_gib: float, region: str | None = None) -> float:
    """USD per hour of one container: (gpu + cpu cores + memory GiB) x region multiplier."""
    g = 0.0
    if gpu:
        key = gpu.rstrip("!").split(":")[0].upper()
        key = {"A100": "A100-80GB", "A100-80G": "A100-80GB"}.get(key, key)
        if key not in RATES["gpu_h"]:
            raise ValueError(f"no rate for GPU {gpu!r}")
        g = RATES["gpu_h"][key]
    return (g + cpu * RATES["cpu_core_h"] + mem_gib * RATES["mem_gib_h"]) * region_mult(region)


def container_cost_usd(seconds: float, rate_h: float, overhead_s: float = CONTAINER_OVERHEAD_S) -> float:
    return (max(0.0, seconds) + overhead_s) / 3600.0 * rate_h


class BudgetExceeded(RuntimeError):
    pass


class Budget:
    """Running spend estimate = closed segments (ledger) + open segments (elapsed x rate). Persisted to LEDGER so that
    every `modal run` of this task counts toward the SAME USD 5.00 cap.

      open(name, rate_h)   a container started (call at spawn: the overhead is charged at once)
      close(name, seconds) it ended; `seconds` = the container's own measured wall seconds if known, else elapsed
      can_launch(est_usd)  False when spent + est_usd would pass STOP_LAUNCH_USD
      must_cancel()        True from HARD_STOP_USD on: the caller cancels every running call and stops
    """

    def __init__(self, path=LEDGER, cap=CAP_USD, stop_launch=STOP_LAUNCH_USD, hard_stop=HARD_STOP_USD,
                 clock=time.time, overhead_s=CONTAINER_OVERHEAD_S, persist=True):
        self.path, self.cap, self.stop_launch, self.hard_stop = Path(path), cap, stop_launch, hard_stop
        self.clock, self.overhead_s, self.persist = clock, overhead_s, persist
        self.closed = []   # [{name, usd, seconds, rate_h, utc}]
        self.open_ = {}    # name -> (t0, rate_h)
        self.extra = []    # [{name, usd}] non-container items (OpenRouter, storage)
        if persist and self.path.exists():
            d = json.loads(self.path.read_text())
            self.closed, self.extra = d.get("closed", []), d.get("extra", [])

    # -- state
    def spent_closed(self) -> float:
        return sum(c["usd"] for c in self.closed) + sum(e["usd"] for e in self.extra)

    def spent_open(self) -> float:
        now = self.clock()
        return sum(container_cost_usd(now - t0, r, self.overhead_s) for t0, r in self.open_.values())

    def spent(self) -> float:
        return self.spent_closed() + self.spent_open()

    def remaining(self) -> float:
        return self.cap - self.spent()

    # -- actions
    def open(self, name: str, rate_h: float):
        if name in self.open_:
            raise ValueError(f"{name} already open")
        self.open_[name] = (self.clock(), rate_h)
        self.save()

    def close(self, name: str, seconds: float | None = None):
        t0, rate = self.open_.pop(name)
        elapsed = self.clock() - t0
        secs = elapsed if seconds is None else max(float(seconds), 0.0)
        usd = container_cost_usd(secs, rate, self.overhead_s)
        self.closed.append({"name": name, "usd": round(usd, 4), "seconds": round(secs, 1), "elapsed_s": round(elapsed, 1),
                            "rate_h": round(rate, 4), "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
        self.save()
        return usd

    def add_extra(self, name: str, usd: float):
        self.extra.append({"name": name, "usd": round(float(usd), 4)})
        self.save()

    def can_launch(self, est_usd: float) -> bool:
        return self.spent() + est_usd <= self.stop_launch

    def must_cancel(self) -> bool:
        return self.spent() >= self.hard_stop

    def check_launch(self, name: str, est_usd: float):
        if not self.can_launch(est_usd):
            raise BudgetExceeded(f"{name}: spent ${self.spent():.2f} + estimate ${est_usd:.2f} > stop-launch "
                                 f"${self.stop_launch:.2f} (cap ${self.cap:.2f})")

    def save(self):
        if not self.persist:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"cap_usd": self.cap, "stop_launch_usd": self.stop_launch,
                                   "hard_stop_usd": self.hard_stop, "closed": self.closed, "extra": self.extra,
                                   "open": {k: {"t0": v[0], "rate_h": v[1]} for k, v in self.open_.items()},
                                   "spent_closed_usd": round(self.spent_closed(), 4)}, indent=1))
        os.replace(tmp, self.path)

    def summary(self) -> dict:
        return {"spent_usd": round(self.spent(), 4), "closed_usd": round(self.spent_closed(), 4),
                "open_usd": round(self.spent_open(), 4), "cap_usd": self.cap, "stop_launch_usd": self.stop_launch,
                "hard_stop_usd": self.hard_stop, "n_closed": len(self.closed)}


# ------------------------------------------------------------------ guards
def payer_guard(env=None, argv=None, active=None) -> str:
    """Refuse unless the Modal payer is jaypatil-duke: MODAL_PROFILE set explicitly to it, no MODAL_TOKEN_* override,
    the modal client's active profile is the same, `modal run` only (never deploy/serve/shell), never --detach."""
    env = os.environ if env is None else env
    argv = sys.argv if argv is None else argv
    prof = env.get("MODAL_PROFILE")
    if not prof:
        raise SystemExit(f"payer guard: set MODAL_PROFILE={PROFILE} explicitly (the default profile is never used)")
    if prof in FORBIDDEN_PROFILES or prof != PROFILE:
        raise SystemExit(f"payer guard: MODAL_PROFILE={prof!r} refused: only {PROFILE!r} may pay for this task")
    bad = [k for k in ("MODAL_TOKEN_ID", "MODAL_TOKEN_SECRET") if env.get(k)]
    if bad:
        raise SystemExit(f"payer guard: {bad} set in the environment would override the profile token: unset them")
    if active is None:
        try:
            import modal.config as _mc
            active = getattr(_mc, "_profile", prof)
        except Exception:  # noqa: BLE001
            active = prof
    if active != prof:
        raise SystemExit(f"payer guard: the modal client's active profile is {active!r}, not {prof!r}")
    a0 = Path(argv[0]) if argv else Path("")
    if a0.name == "modal" or (a0.name == "__main__.py" and a0.parent.name == "modal"):
        cmd = next((a for a in argv[1:] if not a.startswith("-")), None)
        if cmd not in (None, "run"):
            raise SystemExit(f"payer guard: only `modal run` is allowed here (got `modal {cmd}`)")
    if any(a in ("--detach", "-d") for a in argv[1:]):
        raise SystemExit("payer guard: --detach is refused (Ctrl-C on the laptop must stop the GPU)")
    return prof


FORBIDDEN_SUBSTRINGS = ("ohs", "sealed", "c_spec/sealed_brief", "c_build/preread", "bench/external_quarantine",
                        "bench/longbench_v2", ".claude")


def path_problem(p) -> str | None:
    s = str(p).replace("\\", "/").lower()
    for w in FORBIDDEN_SUBSTRINGS:
        if w in s:
            return f"path {p!r} contains {w!r}"
    return None


def safe_path(p) -> Path:
    """Return Path(p) or raise SystemExit when it names protected data. Use before every open of data."""
    bad = path_problem(p)
    if bad:
        raise SystemExit(f"refused: {bad} (OHS / sealed / quarantine data is never opened)")
    return Path(p)


def split_ok(name: str) -> bool:
    n = str(name).lower()
    return not any(w in n for w in ("ohs", "sealed", "jev"))


# ------------------------------------------------------------------ io + stats
def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256_file(p, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_jsonl(p) -> list:
    out = []
    with open(safe_path(p)) as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out


def write_jsonl(p, rows):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with open(tmp, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    os.replace(tmp, p)


def write_json(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1, default=str))
    os.replace(tmp, p)


def pct(xs, q: float):
    """Nearest rank, as client_bench.pct: s[min(n-1, int(q*n))]."""
    s = sorted(xs)
    return s[min(len(s) - 1, int(q * len(s)))] if s else None


def summarize(xs, nd: int = 2) -> dict:
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    if not xs:
        return {"n": 0}
    r = lambda v: round(v, nd)  # noqa: E731
    return {"n": len(xs), "p50": r(pct(xs, 0.5)), "p90": r(pct(xs, 0.9)), "p95": r(pct(xs, 0.95)),
            "p99": r(pct(xs, 0.99)), "mean": r(statistics.fmean(xs)), "min": r(min(xs)), "max": r(max(xs))}
