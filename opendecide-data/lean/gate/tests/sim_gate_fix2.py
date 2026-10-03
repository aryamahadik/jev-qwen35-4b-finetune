"""End-to-end CPU simulation of gate/gate_4b_fix2_l4.sh (A8-prime job 3) and its step 0b: no GPU, no network, nothing
paid. Reuses gate/tests/sim_gate.build() (a throw-away lean/ tree: data/ a read-only symlink to the real data, copies of
the code and gate/, the stored 4B-E preds) and adds: the job-1 C1 reads (R needs them), models/<C1> and models/<C4>
(main-run snapshots stand in; the verdicts are meaningless), runs/q35_4b_fix2.json, yn2b/check_unseen.py +
yn2b_common.py + f7_fix2_drops.json (so step 0a reproduces the real frozen gate/fix2_pairs.json byte for byte), a PREREG_FINAL.md stand-in holding "Amendment A8-prime", gate/teacher_switch_l4.sh with
prereg_drafts/teacher_switch_l4_c4.patch applied, and od_gcp predict replaced by gate/tests/predict_stub_fix2.py.

  ../.venv/bin/python gate/tests/sim_gate_fix2.py OUT_DIR [scenario ...]
Scenarios:
  ok           pairs -> manifest -> vm-probe0 (GO) -> vm-job3 end to end (C4 present) -> a rerun repeats nothing
  ship         C4 without (e) flips: R, P, N pass, the look is SHIP + FINAL, then the _2v and 6 (d) memo reads
  nogo         the probe does not reproduce the failure: 0b NO GO, and vm-job3's preflight refuses to start
  noA8         no "Amendment A8-prime" in PREREG_FINAL.md: 0b and job 3 stop before any read
  parity_fail  the fresh REF read misses the parity bar: the job stops before any C1R or C4 read
  R_fail       the C1 re-read does not reproduce job 1: the job stops (exit 20) before any C4 read
  wait         C4 absent: part 1 runs (incl. the C1R report reads), then the wait times out (exit 12, no C4 read);
               C4 + manifest added: the relaunch skips every finished read and runs to the end
  P_fail       C4 keeps C1's probe flips: P fails, no ship look, outcome noship-P
  noverdict    C4's probe read has no load record (a pipeline problem): P gives NO VERDICT (exit 2), the job stops
               (exit 7) with no P record and no summary; after a clean re-read P is computed once, as usual
  reset        R fails (exit 20); 'vm-reset-pre-c4 NOTE' moves R / refparity3 and the REF fresh3 / C1R reads aside
               (refused without a NOTE, and refused once a C4 read exists); the relaunch recomputes R and finishes
  parser       the fixed PUSH_FIXES parser keeps only '<path>: FAILED' lines (job 1's parser took 'sha256sum')
The real lean/ tree is never written.
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sim_gate as sg  # noqa: E402

LEAN, PY = sg.LEAN, sg.PY
C1, C4, REFA = "q35_4b_main500k", "q35_4b_main500k_fix2", "q35_4b_pxE"
STD = sg.SPLITS9 + sg.ATTACKS
G = "logs/gate4b_fix2"
C1_BACKUP = Path("/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k")


def build(root: Path, with_a8=True, with_c4=True):
    sg.build(root, "")  # the committed gate_dev.py (A7 applied); models/q35_4b_main500k = a snapshot stand-in
    for s in STD:  # the job-1 C1 reads (A8' R compares the job-3 re-read with them)
        for n in (C1, C1 + "_perm") if s in sg.SPLITS9 else (C1,):
            for ext in (".jsonl", ".meta.json"):
                shutil.copy2(LEAN / f"preds_{s}/{n}{ext}", root / f"preds_{s}")
    shutil.rmtree(root / "models" / C1)
    (root / "models" / C1).symlink_to(C1_BACKUP)  # the real C1 (its sha256 is checked by 'manifest')
    if with_c4:
        add_c4(root)
    (root / "yn2b").mkdir()
    for f in ("check_unseen.py", "yn2b_common.py", "f7_fix2_drops.json"):  # the drops file: 0a's accuracy-exclusion list
        shutil.copy2(LEAN / "yn2b" / f, root / "yn2b" / f)
    shutil.copy2(LEAN / "runs/q35_4b_fix2.json", root / "runs")
    (root / "PREREG_FINAL.md").write_text("# stand-in\n" + ("> **Amendment A8-prime (A8′) (simulation)**\n" if with_a8 else ""))
    shutil.copy2(LEAN / "gate/tests/predict_stub_fix2.py", root / "gate/tests/predict_stub_fix2.py")
    p = subprocess.run(["patch", "-p3", "-d", str(root), "-i", str(LEAN / "prereg_drafts/teacher_switch_l4_c4.patch")],
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr


def add_c4(root: Path):
    fin = root / "models" / C4
    fin.mkdir(parents=True, exist_ok=True)
    for f in sg.ADAPTER_FILES:
        (fin / f).symlink_to(sg.SNAPS / "s002500" / f)


def write_c4_manifest(root: Path):
    out = subprocess.run(["shasum", "-a", "256"] + [f"models/{C4}/{f}" for f in sg.ADAPTER_FILES], cwd=root,
                         capture_output=True, text=True, check=True).stdout
    (root / "gate/manifest_c4_fix2.sha256").write_text(out)


def run(root: Path, phase: str, stub_map=None, extra_env=None):
    env = {**os.environ, "LEAN": str(root), "PY": PY, "GATE_SIM": "1", "NO_SHUTDOWN": "1", "ALLOW_DIRTY": "1",
           "PREDICT_CMD": f"{PY} gate/tests/predict_stub_fix2.py", "BACKUP": str(root / "models" / C4),
           "C1_BACKUP": str(C1_BACKUP), "WAIT_POLL_S": "1", **(extra_env or {})}
    if stub_map is not None:
        (root / "stub_map.json").write_text(json.dumps(stub_map))
        env["GATE_STUB_MAP"] = str(root / "stub_map.json")
    p = subprocess.run(["bash", str(root / "gate/gate_4b_fix2_l4.sh"), phase], env=env, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def has(root, split, name):
    return (root / f"preds_{split}/{name}.jsonl").exists()


def cond(root, cid):
    p = root / G / "conds" / f"{cid}.json"
    return json.loads(p.read_text()) if p.exists() else None


# stub settings: C1 re-read = C1's job-1 probabilities (R passes); C1 flips 40% of F7 even rungs, 4B-E 5% (0b GO);
# C4 = C1's 9-split probabilities and 5% F7 flips (P passes on the probe; N passes at identity)
MAP_OK = {f"{C1}_r3": {"src": C1, "src_attack": C1, "f7_flip": 0.40}, f"{C1}_r3_perm": {"src": C1 + "_perm"},
          f"{C1}_r3_tta": {"src": C1}, f"{C1}_r3_perm_tta": {"src": C1 + "_perm"},
          f"{C1}_p0": {"f7_flip": 0.40}, f"{REFA}_p0": {"f7_flip": 0.05},
          C4: {"src": C1, "src_attack": C1, "f7_flip": 0.05}, f"{C4}_perm": {"src": C1 + "_perm"},
          f"{C4}_tta": {"src": C1}, f"{C4}_perm_tta": {"src": C1 + "_perm"}, f"{C4}_2v": {"src": C1}}


def prep(root, with_a8=True, with_c4=True):
    build(root, with_a8=with_a8, with_c4=with_c4)
    rc, log = run(root, "pairs")
    assert rc == 0, log
    rc, log = run(root, "manifest")
    assert rc == 0, log
    if with_c4:
        write_c4_manifest(root)


def scenario(out: Path, name: str, results):
    root = out / name
    chk = lambda c, m: sg.check(c, m, results)  # noqa: E731
    if name == "ok":
        prep(root)
        rc, log = run(root, "vm-probe0", MAP_OK)
        go = cond(root, "probe_go")
        chk(rc == 0 and go and go["pass"] and "A8' 0b: GO" in log, f"ok: 0b GO ({go and (go['c1_flips'], go['ref_flips'], go['pairs'])})")
        rc, log = run(root, "vm-job3", MAP_OK)
        lk = sg.ledger(root)
        modes = [x["mode"] for x in lk]
        chk(rc == 0 and modes == ["refparity", "ship"], f"ok: job 3 runs to the end, looks {modes} (rc {rc})")
        chk(all(cond(root, c) and cond(root, c)["pass"] for c in ("R", "P", "N")),
            f"ok: R, P, N computed and pass ({[(c, (cond(root, c) or {}).get('pass')) for c in ('R', 'P', 'N')]})")
        ship = [x for x in lk if x["mode"] == "ship"]
        chk(len(ship) == 1 and ship[0]["cand"] == C4 and ship[0]["ref"] == "q35_4b_pxE_fresh3",
            f"ok: one ship look, C4 vs fresh3 ({[(x['verdict'], x['final']) for x in ship]})")
        for sp, n in [("dev", "q35_4b_pxE_fresh3"), ("dev", "q35_4b_pxE_fresh3_perm"), ("f7_probe", f"{C1}_r3"),
                      ("dev", f"{C1}_r3_perm"), ("dev", f"{C1}_r3_tta"), ("dev", f"{C1}_r3_perm_tta"), ("f7_devx", C4),
                      ("dev", f"{C4}_perm"), ("dev", f"{C4}_tta"), ("dev", f"{C4}_perm_tta")]:
            chk(has(root, sp, n), f"ok: read {sp}/{n} present")
        tv = root / G / "twoview.json"
        chk(tv.exists() and len(json.loads(tv.read_text())["models"]) == 2, "ok: the 2-view report ran on C1R and C4")
        sm = json.loads((root / G / "summary.json").read_text())
        chk(sm["outcome"].split(":")[0] in ("ship", "noship", "not-final"), f"ok: summary {sm['outcome']}")
        if sm["outcome"].startswith("ship:"):
            chk(has(root, "dev", f"{C4}_2v") and has(root, "memo4b_train_rows", C4),
                "ok: FINAL SHIP -> C4 _2v read and the 6 (d) memo read")
        else:
            chk(not has(root, "dev", f"{C4}_2v"), "ok: no FINAL SHIP -> no _2v / memo read")
        n0 = len(lk)
        rc, log = run(root, "vm-job3", MAP_OK)
        tail = log.split("PREFLIGHT OK")[-1]
        chk(rc == 0 and len(sg.ledger(root)) == n0 and "not repeated" in tail and "not recomputed" in tail
            and not re.search(r"READ \S+ START", tail),
            "ok rerun: every read skipped, no look or condition repeated, ledger unchanged")
    elif name == "ship":
        prep(root)
        run(root, "vm-probe0", MAP_OK)
        m = {**MAP_OK, C4: {**MAP_OK[C4], "fix_equiv": True}, f"{C4}_perm": {"src": C1 + "_perm", "fix_equiv": True}}
        rc, log = run(root, "vm-job3", m)
        sm = json.loads((root / G / "summary.json").read_text())
        chk(rc == 0 and sm["outcome"] == f"ship:{C4}", f"ship: R, P, N pass and the look gives SHIP + FINAL ({sm['outcome']})")
        chk(has(root, "dev", f"{C4}_2v") and has(root, "memo4b_train_rows", C4) and "MEMO meta vs preds_dev" in
            (root / G / "events.log").read_text(), "ship: the C4 _2v read and the 6 (d) memo read follow the FINAL SHIP")
        meta = json.loads((root / f"preds_dev/{C4}_2v.meta.json").read_text())
        chk(meta["tta_choice"] and not meta["tta_noul"], "ship: _2v is the served readout (--tta-choice only)")
    elif name == "nogo":
        prep(root)
        m = {**MAP_OK, f"{C1}_p0": {"f7_flip": 0.05}}
        rc, log = run(root, "vm-probe0", m)
        chk(rc == 0 and cond(root, "probe_go") and not cond(root, "probe_go")["pass"] and "NO GO" in log,
            "nogo: 0b NO GO recorded")
        rc, log = run(root, "vm-job3", m)
        chk(rc == 2 and "was NO GO" in log and not has(root, "dev", "q35_4b_pxE_fresh3"),
            "nogo: job 3's preflight refuses to start (no read)")
    elif name == "noA8":
        prep(root, with_a8=False)
        rc, log = run(root, "vm-probe0", MAP_OK)
        chk(rc == 2 and "no Amendment A8-prime" in log and not has(root, "f7_probe", f"{C1}_p0"),
            "noA8: 0b stops before any probe read")
    elif name == "parity_fail":
        prep(root)
        run(root, "vm-probe0", MAP_OK)
        rc, log = run(root, "vm-job3", {**MAP_OK, "q35_4b_pxE_fresh3": {"degrade_noul": 0.05}})
        chk(rc == 10 and "REF PARITY FAILED" in log and not has(root, "dev", f"{C1}_r3") and not has(root, "dev", C4),
            f"parity_fail: stops before any C1R / C4 read (rc {rc})")
    elif name == "R_fail":
        prep(root)
        run(root, "vm-probe0", MAP_OK)
        rc, log = run(root, "vm-job3", {**MAP_OK, f"{C1}_r3": {"src": C1, "src_attack": C1, "degrade_noul": 0.05}})
        chk(rc == 20 and "A8' R FAILED" in log and not has(root, "dev", C4) and len(sg.ledger(root)) == 1,
            f"R_fail: stops after R, no C4 read, only the parity look logged (rc {rc})")
    elif name == "wait":
        prep(root, with_c4=False)
        run(root, "vm-probe0", MAP_OK)
        rc, log = run(root, "vm-job3", MAP_OK, {"WAIT_C4_MAX_MIN": "0"})
        chk(rc == 12 and has(root, "dev", f"{C1}_r3_tta") and not has(root, "dev", C4),
            f"wait: part 1 + the idle-time C1R report reads ran, then the wait stopped before any C4 read (rc {rc})")
        add_c4(root)
        write_c4_manifest(root)
        rc, log = run(root, "vm-job3", MAP_OK)
        chk(rc == 0 and log.count("already complete, skipped") >= 6 and has(root, "dev", C4)
            and [x["mode"] for x in sg.ledger(root)] == ["refparity", "ship"],
            f"wait: relaunch keeps every finished read and runs to the end (rc {rc})")
    elif name == "P_fail":
        prep(root)
        run(root, "vm-probe0", MAP_OK)
        rc, log = run(root, "vm-job3", {**MAP_OK, C4: {**MAP_OK[C4], "f7_flip": 0.40}})
        sm = json.loads((root / G / "summary.json").read_text())
        chk(rc == 0 and sm["outcome"] == f"noship-P:{C4}" and [x["mode"] for x in sg.ledger(root)] == ["refparity"]
            and cond(root, "N") is None, f"P_fail: P fails, N not computed, no ship look ({sm['outcome']})")
    elif name == "noverdict":
        prep(root)
        run(root, "vm-probe0", MAP_OK)
        rc, log = run(root, "vm-job3", {**MAP_OK, C4: {**MAP_OK[C4], "no_load": True}})
        chk(rc == 7 and "no verdict" in log and cond(root, "P") is None and not (root / G / "summary.json").exists()
            and [x["mode"] for x in sg.ledger(root)] == ["refparity"],
            f"noverdict: a pipeline problem stops the job with no P record, no look, no summary (rc {rc})")
        for s_ in STD + ["f7_probe", "f7_devx"]:  # the repaired read: remove C4's bad reads, then relaunch
            for f in (root / f"preds_{s_}").glob(f"{C4}.*"):
                f.unlink()
        rc, log = run(root, "vm-job3", MAP_OK)
        chk(rc == 0 and cond(root, "P") and cond(root, "P")["pass"] and (root / G / "summary.json").exists(),
            f"noverdict: after a clean re-read, P is computed once and the job finishes (rc {rc})")
    elif name == "reset":
        prep(root)
        run(root, "vm-probe0", MAP_OK)
        rc, log = run(root, "vm-job3", {**MAP_OK, f"{C1}_r3": {"src": C1, "src_attack": C1, "degrade_noul": 0.05}})
        chk(rc == 20 and cond(root, "R") and not cond(root, "R")["pass"], f"reset: R fails first (rc {rc})")
        rc, log = run(root, "vm-reset-pre-c4")
        chk(rc != 0 and cond(root, "R") is not None, "reset: refused without a dated NOTE")
        rc, log = run(root, "vm-job3", MAP_OK)
        chk(rc == 20 and "not recomputed" in log, "reset: without a reset the failed R is never recomputed")
        env_note = "2 Oct 23:59 UTC: VM repaired (simulation)"
        p = subprocess.run(["bash", str(root / "gate/gate_4b_fix2_l4.sh"), "vm-reset-pre-c4", env_note],
                           env={**os.environ, "LEAN": str(root), "PY": PY, "GATE_SIM": "1", "NO_SHUTDOWN": "1"},
                           capture_output=True, text=True)
        moved = sorted((root / G).glob("reset_*"))
        chk(p.returncode == 0 and cond(root, "R") is None and moved and (moved[0] / "NOTE.txt").exists()
            and not has(root, "dev", f"{C1}_r3") and not has(root, "dev", "q35_4b_pxE_fresh3"),
            f"reset: records and the fresh3 / C1R reads moved to {moved[0].name if moved else None}")
        rc, log = run(root, "vm-job3", MAP_OK)
        chk(rc == 0 and cond(root, "R")["pass"] and cond(root, "P") is not None,
            f"reset: the relaunch recomputes R and runs to the end (rc {rc})")
        p = subprocess.run(["bash", str(root / "gate/gate_4b_fix2_l4.sh"), "vm-reset-pre-c4", env_note],
                           env={**os.environ, "LEAN": str(root), "PY": PY, "GATE_SIM": "1", "NO_SHUTDOWN": "1"},
                           capture_output=True, text=True)
        chk(p.returncode != 0 and "C4 read exists" in p.stdout + p.stderr, "reset: refused once any C4 read exists")
    elif name == "parser":
        sample = ("data/dev.jsonl: OK\ngate_dev.py: FAILED\nsha256sum: data/x.jsonl: No such file or directory\n"
                  "data/x.jsonl: FAILED open or read\nsha256sum: WARNING: 1 listed file could not be read\n"
                  "sha256sum: WARNING: 1 computed checksum did NOT match\n")
        p = subprocess.run(["bash", "-c", "eval \"$(sed -n '/^failed_paths()/p' gate/gate_4b_fix2_l4.sh)\"; failed_paths"],
                           input=sample, cwd=LEAN, capture_output=True, text=True)
        chk(p.stdout.split() == ["gate_dev.py", "data/x.jsonl"], f"parser: fixed parser keeps only real paths ({p.stdout.split()})")
        old = subprocess.run(["bash", "-c", "grep -E 'FAILED|No such' | sed 's/:.*//'"], input=sample, capture_output=True,
                             text=True).stdout.split()
        chk("sha256sum" in old, f"parser: job 1's parser yields the bogus path 'sha256sum' ({old})")


def main():
    out = Path(sys.argv[1]).resolve()
    names = sys.argv[2:] or ["parser", "ok", "ship", "nogo", "noA8", "parity_fail", "R_fail", "wait", "P_fail",
                             "noverdict", "reset"]
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
