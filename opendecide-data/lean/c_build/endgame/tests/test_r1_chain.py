"""CPU test of r1_chain.sh's snap-monitor liveness rules, with fake python / modal binaries (nothing is launched).

The chain is copied into a sandbox lean/ tree; ../.venv/bin/python and ../.venv/bin/modal are shell fakes: r1_check.py
says GO (proj writes a 30-minute cap), spend_guard.py appends ledger lines, `modal run` sleeps FAKE_SEG_S, and
snap_monitor.py behaves as FAKE_MON says."""
import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
CHAIN = HERE.parent / "r1_chain.sh"

FAKE_PY = r"""#!/bin/bash
case "$1" in
  */r1_check.py) [ "$2" = proj ] && echo 30 > c_build/endgame/logs/r1_stop_after_min.txt; echo GO; exit 0;;
  */spend_guard.py) shift; echo "$*" >> c_build/endgame/logs/ledger.txt; exit 0;;
  */snap_monitor.py)
    echo '{"ev": "start"}'
    case "$FAKE_MON" in
      die_now) exit 1;;
      die_mid) sleep 2; exit 1;;
      escalate) sleep 2; echo '{"escalated": true}' > c_build/endgame/logs/snap_monitor_escalation.json; exit 4;;
      ok) sleep 3; exit 0;;
    esac;;
esac
exit 0
"""
FAKE_MODAL = """#!/bin/bash
echo "$*" >> c_build/endgame/logs/modal_calls.txt
sleep "${FAKE_SEG_S:-0.2}"
exit 0
"""


def chain(tmp: Path, mon: str, seg3_s: float = 0.2, final: bool = True):
    lean = tmp / "lean"
    e = lean / "c_build/endgame"
    (e / "logs").mkdir(parents=True)
    (lean / "logs").mkdir()
    shutil.copy(CHAIN, e / "r1_chain.sh")
    (e / "snap_monitor.py").write_text("# fake\n")
    (lean / "PREREG_FINAL.md").write_text("")
    if final:
        (lean / "logs/relay_q35_4b_c_r1_final.json").write_text("{}")
    vb = tmp / ".venv/bin"
    vb.mkdir(parents=True)
    for name, body in (("python", FAKE_PY), ("modal", FAKE_MODAL)):
        (vb / name).write_text(body)
        (vb / name).chmod((vb / name).stat().st_mode | stat.S_IEXEC)
    env = {**os.environ, "FAKE_MON": mon, "R1_MON_START_S": "1", "R1_MON_POLL_S": "0.5"}

    def run_seg3_slow():
        return subprocess.run(["bash", str(e / "r1_chain.sh")], cwd=str(lean), capture_output=True, text=True,
                              timeout=60, env={**env, "FAKE_SEG_S": str(seg3_s)})
    r = run_seg3_slow()
    calls = (e / "logs/modal_calls.txt").read_text().splitlines() if (e / "logs/modal_calls.txt").exists() else []
    ledger = (e / "logs/ledger.txt").read_text() if (e / "logs/ledger.txt").exists() else ""
    return r, calls, ledger, e


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_monitor_dead_at_start_no_seg3(tmp_path):
    r, calls, ledger, e = chain(tmp_path, "die_now")
    assert r.returncode == 1 and "seg3 NOT launched" in r.stdout
    assert len(calls) == 2 and all("--stop-at-step" in c for c in calls)   # seg1 + seg2 only, never seg3
    assert "snap monitor not running" in ledger and (e / "logs/r1_monitor_dead.json").exists()


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_monitor_dies_during_seg3_stops_chain(tmp_path):
    r, calls, ledger, e = chain(tmp_path, "die_mid", seg3_s=4)
    assert r.returncode == 1 and "died during seg3" in r.stdout and "ROUND 1 FINAL" not in r.stdout
    assert r.stdout.count("SNAP MONITOR NOT RUNNING") == 1 and "during seg3" in ledger
    assert len(calls) == 3


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_monitor_escalation_stops_chain(tmp_path):
    r, calls, ledger, e = chain(tmp_path, "escalate", seg3_s=4)
    assert r.returncode == 1 and "ESCALATED" in r.stdout and "SNAP MONITOR NOT RUNNING" not in r.stdout


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_monitor_ok_reaches_final(tmp_path):
    r, calls, ledger, e = chain(tmp_path, "ok", seg3_s=1)
    assert r.returncode == 0, r.stdout[-400:]
    assert "ROUND 1 FINAL" in r.stdout and "alive before seg3" in r.stdout and len(calls) == 3
    assert not (e / "logs/r1_monitor_dead.json").exists()
