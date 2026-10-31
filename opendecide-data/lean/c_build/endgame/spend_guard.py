"""Spend guards for every paid Modal launch in RUNBOOK.md (free to run: billing and app-list calls only).

Modal billing lags by up to about 1 h, so a billing poll alone is not a cap. This file keeps a local LAUNCH LOG
(logs/launches.jsonl: profile, what, start unix, cap minutes, GPUs) and counts, for every logged launch, the part of its
capped window that falls after (now - LAG) as NOT YET BILLED (it may have run but not be billed yet, or may still run).

  check  <profile> --cap-usd X [--reserve R]   GO (exit 0) only if credit_left - unbilled - X >= R, and no app runs on
                                               the profile that the launch log does not explain. Else REFUSED (exit 1).
  record <profile> <what> <cap_min> <n_gpu>     append a launch to the log (call right before the launch).
  run    --profile P --what W --cap-min N -- <cmd ...>
                                               a NON-detached `modal run` with a hard wall cap: records the launch, runs
                                               the command, at N minutes sends SIGINT (Modal stops an ephemeral app when
                                               its client stops), then `modal app stop <app id>`; exit code = the
                                               command's (124 when the cap fired). If the Mac sleeps or the client dies,
                                               Modal stops the ephemeral app itself.
  ledger <profile> <text> [--payer credit|card] one line in logs/budget_ledger.md with the billing numbers right now.
  bill   <profile>                              print metered / billed / credit_left.

  cd lean && ../.venv/bin/python c_build/endgame/spend_guard.py check jaypatil-duke --cap-usd 1 --reserve 12
"""
from __future__ import annotations

import json
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
LOGS = HERE / "logs"
LAUNCHES = LOGS / "launches.jsonl"
LEDGER = LEAN / "logs/budget_ledger.md"
MODAL = str(LEAN.parent / ".venv/bin/modal")
USD_H = 4.09          # H100 $/h used everywhere (recipe 4; Modal lists $3.95/h, the higher one is used)
LAG_S = 75 * 60       # billing lag allowance (Modal: up to about 1 h)
MONTHLY_CREDIT = 30.0


def bill(profile: str) -> dict:
    r = subprocess.run([MODAL, "billing", "summary", "--for", "this month", "--json", "--profile", profile],
                       capture_output=True, text=True, timeout=90)
    d = json.loads(r.stdout)
    credits = float((d.get("adjustments") or {}).get("credits", "0") or 0)
    return {"profile": profile, "metered": float(d["metered_cost"]), "billed": float(d["billed_cost"]),
            "credit_left": round(MONTHLY_CREDIT + credits, 2)}


def launches(profile: str) -> list[dict]:
    if not LAUNCHES.exists():
        return []
    out = []
    for line in LAUNCHES.read_text().splitlines():
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r.get("profile") == profile:
            out.append(r)
    return out


def unbilled_usd(profile: str, now: float | None = None) -> float:
    """Upper bound of spend not yet in billing (or still to come) from logged launches on this profile."""
    now = now or time.time()
    tot = 0.0
    for r in launches(profile):
        start, end = float(r["start"]), float(r["start"]) + 60 * float(r["cap_min"])
        lo = max(start, now - LAG_S)
        if end > lo:
            tot += (end - lo) / 3600 * USD_H * int(r.get("n_gpu", 1))
    return round(tot, 2)


def running_apps(profile: str) -> list[dict]:
    r = subprocess.run([MODAL, "app", "list", "--json"], capture_output=True, text=True, timeout=90,
                       env={**os.environ, "MODAL_PROFILE": profile})
    apps = []
    for a in json.loads(r.stdout or "[]"):
        state = str(a.get("State") or a.get("state") or "").lower()
        tasks = int(a.get("Tasks") or a.get("tasks") or 0)
        if state != "stopped" and (tasks > 0 or "ephemeral" in state or "detached" in state):
            apps.append({"id": a.get("App ID") or a.get("app_id"), "desc": a.get("Description") or a.get("description"),
                         "state": state, "tasks": tasks})
    return apps


def unexplained_apps(profile: str, now: float | None = None) -> list[dict]:
    """Running apps on the profile beyond what the open logged launches explain (one app per logged GPU)."""
    now = now or time.time()
    expected = sum(int(r.get("n_gpu", 1)) for r in launches(profile)
                   if float(r["start"]) + 60 * float(r["cap_min"]) + 300 > now)
    apps = running_apps(profile)
    return apps[expected:] if len(apps) > expected else []


def check(profile: str, cap_usd: float, reserve: float) -> int:
    b = bill(profile)
    unb = unbilled_usd(profile)
    unk = unexplained_apps(profile)
    afford = round(b["credit_left"] - unb - reserve, 2)
    print(json.dumps({**b, "unbilled_usd": unb, "reserve": reserve, "cap_usd": cap_usd, "afford_usd": afford,
                      "unexplained_running_apps": unk}))
    if unk:
        print(f"REFUSED: {len(unk)} app(s) running on {profile} that the launch log does not explain "
              "(their unbilled spend is unknown); wait for them to stop")
        return 1
    if afford < cap_usd:
        print(f"REFUSED: credit_left {b['credit_left']} - unbilled {unb} - reserve {reserve} = {afford} < cap {cap_usd}")
        return 1
    print("GO")
    return 0


def record(profile: str, what: str, cap_min: float, n_gpu: int) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    with LAUNCHES.open("a") as f:
        f.write(json.dumps({"profile": profile, "what": what, "start": round(time.time()), "cap_min": float(cap_min),
                            "n_gpu": int(n_gpu), "usd_cap": round(float(cap_min) / 60 * USD_H * int(n_gpu), 2),
                            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}) + "\n")


def capped_run(profile: str, what: str, cap_min: float, cmd: list[str]) -> int:
    import os
    import threading
    record(profile, what, cap_min, 1)
    env = {**os.environ, "MODAL_PROFILE": profile}
    p = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                         start_new_session=True)
    seen = {"app": None}

    def pump():  # copy the client's output and catch its app id (ap-...)
        for line in p.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
            m = re.search(r"\b(ap-[A-Za-z0-9]{10,})\b", line)
            if m and not seen["app"]:
                seen["app"] = m.group(1)
    t = threading.Thread(target=pump, daemon=True)
    t.start()
    deadline = time.time() + 60 * cap_min
    while p.poll() is None and time.time() < deadline:
        time.sleep(2)
    if p.poll() is None:
        print(f"[spend_guard] cap {cap_min} min reached: SIGINT, then app stop {seen['app']}", flush=True)
        os.killpg(p.pid, signal.SIGINT)          # the whole client group (Modal stops an ephemeral app on SIGINT)
        if seen["app"]:
            subprocess.run([MODAL, "app", "stop", "-y", seen["app"]], env=env, capture_output=True, timeout=90)
        for sig, wait in ((None, 60), (signal.SIGTERM, 20), (signal.SIGKILL, 10)):
            if sig is not None and p.poll() is None:
                os.killpg(p.pid, sig)
            try:
                p.wait(timeout=wait)
                break
            except subprocess.TimeoutExpired:
                continue
        t.join(timeout=5)
        return 124
    t.join(timeout=5)
    return p.returncode or 0


def ledger(profile: str, text: str, payer: str) -> None:
    b = bill(profile)
    line = (f"| {text} | {time.strftime('%d %b %H:%M', time.gmtime())} UTC, {profile} | metered ${b['metered']:.2f}, "
            f"billed ${b['billed']:.2f}, credit left ${b['credit_left']:.2f} | {payer} |")
    with LEDGER.open("a") as f:
        f.write(line + "\n")
    print(line)


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    cmd, a = argv[0], argv[1:]

    def opt(name, default=None):
        return a[a.index(name) + 1] if name in a else default
    if cmd == "bill":
        print(json.dumps(bill(a[0])))
        return 0
    if cmd == "check":
        return check(a[0], float(opt("--cap-usd")), float(opt("--reserve", "0")))
    if cmd == "record":
        record(a[0], a[1], float(a[2]), int(a[3]))
        return 0
    if cmd == "run":
        if "--" not in a:
            print("usage: run --profile P --what W --cap-min N -- <cmd ...>")
            return 2
        i = a.index("--")
        if "--detach" in a[i + 1:]:
            print("REFUSED: `run` caps a NON-detached client; a detached app outlives it (use a server-side cap)")
            return 2
        return capped_run(opt("--profile"), opt("--what"), float(opt("--cap-min")), a[i + 1:])
    if cmd == "ledger":
        ledger(a[0], a[1], opt("--payer", "credit"))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
