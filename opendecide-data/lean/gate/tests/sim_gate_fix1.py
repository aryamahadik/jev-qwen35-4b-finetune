"""End-to-end CPU simulation of gate/gate_4b_fix1_l4.sh vm-job3 (no GPU, no network, nothing paid).

Reuses gate/tests/sim_gate.build(): a throw-away lean/ tree with data/ as a read-only symlink to the real data, copies
of the code and gate/, the stored 4B-E preds, and od_gcp predict replaced by gate/tests/predict_stub.py (copies
existing probabilities, so every verdict is meaningless; the test is the plumbing). Adds: models/q35_4b_main500k_fix1
(a main-run snapshot stands in for the C4 adapter), runs/q35_4b_fix1.json, yn2b/check_unseen.py + yn2b_common.py, and a
PREREG_FINAL.md stand-in that holds the A8 header the preflight looks for.
  ../.venv/bin/python gate/tests/sim_gate_fix1.py OUT_DIR [scenario ...]
Scenarios: ok (job 3 end to end, then a rerun that repeats nothing), noA8 (preflight stops: no A8), parity_fail
(a fresh REF read that misses the parity bar: the job stops before any C4 read). The real lean/ tree is never written.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sim_gate as sg  # noqa: E402

LEAN, PY = sg.LEAN, sg.PY
C4 = "q35_4b_main500k_fix1"


def build(root: Path, with_a8=True):
    sg.build(root, "")  # the committed gate_dev.py (A7 already applied)
    fin = root / "models" / C4
    fin.mkdir(parents=True)
    for f in sg.ADAPTER_FILES:
        (fin / f).symlink_to(sg.SNAPS / "s002500" / f)
    (root / "yn2b").mkdir()
    for f in ("check_unseen.py", "yn2b_common.py"):
        shutil.copy2(LEAN / "yn2b" / f, root / "yn2b" / f)  # gate/check_unseen_fix1.py imports them
    shutil.copy2(LEAN / "runs/q35_4b_fix1.json", root / "runs")
    (root / "PREREG_FINAL.md").write_text("# stand-in\n" + ("> **Amendment A8 (simulation)**\n" if with_a8 else ""))


def run(root: Path, phase: str, stub_map=None, extra_env=None):
    env = {**os.environ, "LEAN": str(root), "PY": PY, "GATE_SIM": "1", "NO_SHUTDOWN": "1", "ALLOW_DIRTY": "1",
           "PREDICT_CMD": f"{PY} gate/tests/predict_stub.py", "BACKUP": str(root / "models" / C4), **(extra_env or {})}
    if stub_map is not None:
        (root / "stub_map.json").write_text(json.dumps(stub_map))
        env["GATE_STUB_MAP"] = str(root / "stub_map.json")
    p = subprocess.run(["bash", str(root / "gate/gate_4b_fix1_l4.sh"), phase], env=env, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def scenario(out: Path, name: str, results):
    root = out / name
    chk = lambda c, m: sg.check(c, m, results)  # noqa: E731
    if name == "ok":
        build(root)
        rc, log = run(root, "manifest")
        chk(rc == 0, f"ok: manifest written ({log.strip().splitlines()[-1] if log.strip() else ''})")
        rc, log = run(root, "vm-job3", {C4: {"improve_noul": 0.03}})
        lk = sg.ledger(root)
        modes = [x["mode"] for x in lk]
        chk(rc == 0 and modes == ["refparity", "ship"], f"ok: job 3 runs to the end, looks {modes} (rc {rc})")
        chk(bool(lk) and lk[0]["pass"] and lk[0]["counts"] and lk[0]["fresh"] == "q35_4b_pxE_fresh3",
            "ok: refparity3 passes and counts for q35_4b_pxE_fresh3")
        ship = [x for x in lk if x["mode"] == "ship"]
        chk(len(ship) == 1 and ship[0]["cand"] == C4 and ship[0]["ref"] == "q35_4b_pxE_fresh3" and ship[0]["final"],
            f"ok: one ship look, C4 vs fresh3, FINAL ({[(x['verdict'], x['final'], x['not_final']) for x in ship]})")
        sm = json.loads((root / "logs/gate4b_fix1/summary.json").read_text()) if (root / "logs/gate4b_fix1/summary.json").exists() else None
        chk(sm is not None, f"ok: summary decision = {sm and sm['decision']}")
        for n in ("q35_4b_pxE_fresh3", "q35_4b_pxE_fresh3_perm", C4, C4 + "_perm"):
            chk(sg.exists(root, n), f"ok: read {n} present")
        chk("check_unseen" not in log or "FAILED" not in log, "ok: the A8 check_unseen precondition passed in preflight")
        n0 = len(lk)
        rc, log = run(root, "vm-job3", {C4: {"improve_noul": 0.03}})
        chk(rc == 0 and len(sg.ledger(root)) == n0 and log.count("already complete, skipped") == 4 and "not repeated" in log,
            "ok rerun: every read skipped, no look repeated, ledger unchanged")
    elif name == "noA8":
        build(root, with_a8=False)
        assert run(root, "manifest")[0] == 0
        rc, log = run(root, "vm-job3")
        chk(rc == 2 and "no Amendment A8" in log and not sg.exists(root, "q35_4b_pxE_fresh3"),
            "noA8: preflight stops before any read when PREREG_FINAL.md has no A8")
    elif name == "parity_fail":
        build(root)
        assert run(root, "manifest")[0] == 0
        rc, log = run(root, "vm-job3", {"q35_4b_pxE_fresh3": {"degrade_noul": 0.05}})
        lk = sg.ledger(root)
        chk(rc == 10 and "REF PARITY FAILED" in log and len(lk) == 1 and lk[0]["pass"] is False,
            f"parity_fail: the parity look fails and the job stops (rc {rc})")
        chk(not sg.exists(root, C4), "parity_fail: C4 was never read")


def main():
    out = Path(sys.argv[1]).resolve()
    names = sys.argv[2:] or ["ok", "noA8", "parity_fail"]
    results = []
    for n in names:
        scenario(out, n, results)
    for s, m in results:
        print(f"[{s}] {m}")
    bad = [m for s, m in results if s != "PASS"]
    print(f"{len(results) - len(bad)}/{len(results)} checks pass")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
