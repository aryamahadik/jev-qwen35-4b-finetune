"""Time cap per crowd container (RUNBOOK A, crowd_launch.sh), from the tasks estimate and the profile's credit left.
Read-only (billing and app-list calls only).

Prints CAP_MIN (minutes per container: 1.5 x the estimated read time, never above what
  credit_left - MARGIN - unbilled launches (spend_guard: logged launches whose capped window reaches into the last
  75 min, i.e. not yet billed or still running)
pays for 3 H100s at $4.09/h), or exits 1 with REFUSED when the credit cannot pay for the estimated read, or when an
app the launch log does not explain is running on the profile (its spend is unknown). CAP_MIN is passed to
modal_crowd.py --max-min, which enforces it ON THE SERVER (function timeout + an absolute deadline that survives a
preemption restart), so a sleeping Mac cannot let the read run on.
A measured rate in c_build/endgame/logs/crowd_rate.json ({"reads_per_s": x}) replaces the assumed 10.4 reads/s.

  CAP_MIN=$(../.venv/bin/python c_build/endgame/crowd_cap.py atmosphor) || exit 1
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
sys.path.insert(0, str(HERE))
import spend_guard as g  # noqa: E402

ASSUMED = 10.4          # crowd_select: L4 3.47 reads/s x 3.0
USD_H, MARGIN, N_CONT = g.USD_H, 1.0, 3
LOAD_MIN = 3.0          # image pull + 4B load per container


def main():
    prof = sys.argv[1] if len(sys.argv) > 1 else "atmosphor"
    e = json.loads((LEAN / "c_build/crowd_r1/crowd_tasks_r1.json").read_text())["estimate"]
    rate = ASSUMED
    rf = HERE / "logs/crowd_rate.json"
    if rf.exists():
        rate = float(json.loads(rf.read_text())["reads_per_s"])
    need_min = e["reads"] / N_CONT / rate / 60 + LOAD_MIN           # per container
    b = g.bill(prof)
    unb = g.unbilled_usd(prof)
    unk = g.unexplained_apps(prof)
    afford_min = (b["credit_left"] - MARGIN - unb) / N_CONT / USD_H * 60
    print(json.dumps({"profile": prof, "reads": e["reads"], "rate": rate, "need_min": round(need_min, 1),
                      "credit_left": b["credit_left"], "unbilled_usd": unb, "usd_h": USD_H,
                      "afford_min": round(afford_min, 1), "unexplained_running_apps": len(unk)}), file=sys.stderr)
    if unk:
        print("REFUSED: an app the launch log does not explain is running on the profile", file=sys.stderr)
        sys.exit(1)
    if afford_min < need_min:
        print("REFUSED: the credit left cannot pay for the estimated read", file=sys.stderr)
        sys.exit(1)
    print(int(min(1.5 * need_min, afford_min)))


if __name__ == "__main__":
    main()
