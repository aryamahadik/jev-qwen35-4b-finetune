"""SCORE_ND_CLI commands that pipe into tee must run under `set -o pipefail` (else a refused look exits 0). CPU only;
never runs the sealed scorer and never reads sealed_nd data (a fake scorer file stands in for the sha check)."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import score_nd_cli  # noqa: E402


def test_generated_commands_carry_pipefail():
    cm = score_nd_cli.commands()
    tee = [k for k, v in cm.items() if "| tee" in v]
    assert tee, "the look commands should tee their stdout"
    assert all(cm[k].startswith("set -o pipefail; ") for k in tee)


def test_record_on_disk_carries_pipefail():
    rec = json.loads((HERE / "SCORE_ND_CLI.json").read_text())
    bad = [k for k, v in (rec.get("commands") or {}).items() if "| tee" in v and not v.startswith("set -o pipefail; ")]
    assert bad == []


def test_pipefail_makes_a_failed_look_fail(tmp_path):
    f = tmp_path / "o.txt"
    without = subprocess.run(["bash", "-c", f"false 2>&1 | tee {f}"]).returncode
    with_pf = subprocess.run(["bash", "-c", f"set -o pipefail; cd {tmp_path} && false 2>&1 | tee {f}"]).returncode
    assert without == 0 and with_pf != 0


def _rec(sha, cmds):
    return {"scorer_sha256": sha, "a15": {"scorer_sha256": sha}, "dry_run": {"pass": True}, "commands": cmds,
            "usage": {"look": "score_nd.py look --kind K"}, "status": "partial"}


def test_verify_refuses_a_tee_without_pipefail(tmp_path, monkeypatch):
    fake = tmp_path / "score_nd.py"
    fake.write_text("# stand-in\n")
    sha = hashlib.sha256(fake.read_bytes()).hexdigest()
    monkeypatch.setattr(score_nd_cli, "SCORER", fake)
    monkeypatch.setattr(score_nd_cli, "a15", lambda: {"scorer_sha256": sha, "suite_sha256": "0" * 64})
    good = {"S1": "set -o pipefail; cd x && py score_nd.py look --kind S1 2>&1 | tee a", "C": "set -o pipefail; c | tee b",
            "verdict": "cd x && py score_nd.py verdict", "status": "cd x && py score_nd.py status"}
    p = tmp_path / "cli.json"
    p.write_text(json.dumps(_rec(sha, {**good, "S1": "cd x && py score_nd.py look --kind S1 2>&1 | tee a"})))
    e = score_nd_cli.verify(p)
    assert e and "pipefail" in e and "S1" in e
    p.write_text(json.dumps(_rec(sha, good)))
    e = score_nd_cli.verify(p)
    assert e and "pipefail" not in e          # passes the pipefail rule; stops later at B5 PARTIAL (not confirmed)
