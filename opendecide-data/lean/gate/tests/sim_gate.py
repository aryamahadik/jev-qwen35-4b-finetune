"""End-to-end CPU simulation of gate/gate_4b_l4.sh vm-job1 / vm-job2 (no GPU, no network, nothing paid).

Each scenario builds a throw-away lean/ tree under OUT/<scenario>: data/ is a read-only symlink to the real data,
the code files and gate/ are copies (gate_dev.py possibly patched as an amendment variant), the stored 4B-E preds and
the 30 Sep q35_4b_pxE_parity / _tta reads are copied, models/ holds REAL adapters (main-run snapshots s002500 / s005000
stand in for the final adapter and the three late snapshots, so C2 / C3 are really materialized), and the od_gcp
predict calls are replaced by gate/tests/predict_stub.py (copies existing probabilities). The verdicts are meaningless;
the test is the plumbing: names, read order, manifests, preflight, the parity stop, the C3 branch, the choice, the
ship looks, FINAL vs NOT FINAL, the ledger and the once-only looks.
  ../.venv/bin/python gate/tests/sim_gate.py OUT_DIR [scenario ...]
Scenarios: frozen, B, A, A_rerun, A_ship, A_split, A_c3. The real lean/ tree is never written.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

LEAN = Path(__file__).resolve().parents[2]
PY = str(LEAN.parent / ".venv/bin/python")
SNAPS = LEAN / "handoff/main500k_snaps/snaps"
REF_BACKUP = Path("/Users/aryamahadik/Documents/jev/backups/gcp_models/q35_4b_pxE")
SPLITS9 = "dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev".split(",")
ATTACKS = ["eval_jagged", "eval_opi", "eval_redef"]
ADAPTER_FILES = ["adapter_config.json", "adapter_model.safetensors", "tokenizer.json", "tokenizer_config.json",
                 "chat_template.jinja", "train_meta.json"]

AMEND_A = ('STORED_REF = {"4b": "q35_4b_pxE", "2b": "q35_2b_v11r"}',
           'STORED_REF = {"4b": "q35_4b_pxE_parity", "2b": "q35_2b_v11r"}')
AMEND_B = ('        bases = {str(m.get("base") or "") for sp in a.splits.split(",") if (m := read_meta(f"preds_{sp}", n))}',
           '        bases = {str(((m.get("train") or {}).get("cfg") or {}).get("base") or m.get("base") or "") '
           'for sp in a.splits.split(",") if (m := read_meta(f"preds_{sp}", n))}')


def build(root: Path, variant: str):
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    (root / "data").symlink_to(LEAN / "data")
    for f in ("gate_dev.py", "od_gcp.py", "decoder_io.py", "prism_x.py", "writeblock.py", "ship_unseen_sources.json"):
        shutil.copy2(LEAN / f, root / f)
    (root / "runs").mkdir()
    shutil.copy2(LEAN / "runs/q35_4b_main.json", root / "runs")
    shutil.copytree(LEAN / "gate", root / "gate", ignore=shutil.ignore_patterns("__pycache__", "manifest_*"))
    g = (root / "gate_dev.py").read_text()
    for flag, (old, new) in (("A", AMEND_A), ("B", AMEND_B)):
        if flag in variant:
            assert g.count(old) == 1, old
            g = g.replace(old, new)
    (root / "gate_dev.py").write_text(g)
    for s in SPLITS9:
        (root / f"preds_{s}").mkdir()
        for n in ("q35_4b_pxE", "q35_4b_pxE_parity", "q35_4b_pxE_tta"):
            for ext in (".jsonl", ".meta.json"):
                shutil.copy2(LEAN / f"preds_{s}/{n}{ext}", root / f"preds_{s}")
    for s in ATTACKS:
        (root / f"preds_{s}").mkdir()
        for ext in (".jsonl", ".meta.json"):
            shutil.copy2(LEAN / f"preds_{s}/q35_4b_pxE{ext}", root / f"preds_{s}")
    m = root / "models"
    m.mkdir()
    (m / "q35_4b_pxE").symlink_to(REF_BACKUP)
    fin = m / "q35_4b_main500k"
    (fin / "snaps").mkdir(parents=True)
    for f in ADAPTER_FILES:  # stand-in for the final adapter
        (fin / f).symlink_to(SNAPS / "s005000" / f)
    for s, src in (("s025888", "s002500"), ("s027411", "s005000"), ("s028934", "s002500")):
        (fin / "snaps" / s).symlink_to(SNAPS / src)
    (root / "logs").mkdir()


def run(root: Path, phase: str, stub_map: dict | None = None, extra_env: dict | None = None, args=()):
    env = {**os.environ, "LEAN": str(root), "PY": PY, "GATE_SIM": "1", "NO_SHUTDOWN": "1",
           "PREDICT_CMD": f"{PY} gate/tests/predict_stub.py", "BACKUP": str(root / "models/q35_4b_main500k"),
           **(extra_env or {})}
    if stub_map is not None:
        (root / "stub_map.json").write_text(json.dumps(stub_map))
        env["GATE_STUB_MAP"] = str(root / "stub_map.json")
    p = subprocess.run(["bash", str(root / "gate/gate_4b_l4.sh"), phase, *args], env=env, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def ledger(root):
    p = root / "logs/ship_looks.jsonl"
    return [json.loads(l) for l in p.read_text().splitlines()] if p.exists() else []


def summary(root):
    p = root / "logs/gate4b/summary.json"
    return json.loads(p.read_text()) if p.exists() else None


def exists(root, name):
    return (root / f"preds_dev/{name}.jsonl").exists()


def check(cond, msg, results):
    results.append(("PASS" if cond else "FAIL", msg))


MAP_NORMAL = {"q35_4b_main500k": {"src": "q35_4b_pxE_tta"}, "q35_4b_main500k_perm": {"src": "q35_4b_pxE_parity"},
              "q35_4b_main500k_c2": {"src": "q35_4b_pxE"}}
MAP_C3 = {"q35_4b_main500k": {"degrade_noul": 0.06}, "q35_4b_main500k_j2": {"degrade_noul": 0.06},
          "q35_4b_main500k_c3w10": {"degrade_noul": 0.06},  # (1,0) reproduces the job-2 C1 read
          "q35_4b_main500k_c2": {"degrade_noul": 0.08}}     # C2 worse than C1: only C3 can qualify


def scenario(out: Path, name: str, results):
    root = out / name
    if name == "frozen":
        build(root, "")
        assert run(root, "manifest")[0] == 0
        rc, log = run(root, "vm-job1", MAP_NORMAL)
        check(rc == 2 and "cannot run --mode refparity against q35_4b_pxE" in log,
              "frozen gate_dev.py: preflight stops before any read (stored REF metas say Qwen3.5-2B)", results)
        check(not exists(root, "q35_4b_pxE_fresh") and not ledger(root), "frozen: no read made, no look logged", results)
    elif name == "B":
        build(root, "B")
        assert run(root, "manifest")[0] == 0
        rc, log = run(root, "vm-job1", MAP_NORMAL)
        lk = ledger(root)
        check(rc == 10 and "REF PARITY FAILED" in log, "B (size fix only, stored = in-process read): parity look FAILS, job stops (exit 10)", results)
        check(len(lk) == 1 and lk[0]["mode"] == "refparity" and lk[0]["pass"] is False and lk[0]["max_dp"] > 0.05,
              f"B: one failed refparity look logged (max |dp| {lk[0]['max_dp'] if lk else None})", results)
        check(not exists(root, "q35_4b_main500k"), "B: no candidate was read after the failed parity look", results)
    elif name in ("A", "A_rerun"):
        if name == "A_rerun":
            root = out / "A"
            n0 = len(ledger(root))
            rc, log = run(root, "vm-job1", MAP_NORMAL)
            check(rc == 0 and len(ledger(root)) == n0 and log.count("already complete, skipped") == 6
                  and "not repeated" in log, "A rerun: every read skipped, no look repeated, ledger unchanged", results)
            return
        build(root, "A")
        rc, log = run(root, "manifest")
        assert rc == 0, log
        rc, log = run(root, "vm-job1", MAP_NORMAL)
        lk, sm = ledger(root), summary(root)
        modes = [x["mode"] for x in lk]
        check(rc == 0 and modes[:2] == ["refparity", "c3trigger"] and "ship" in modes,
              f"A (stored = q35_4b_pxE_parity): job 1 runs to the end; looks {modes}", results)
        check(lk[0]["pass"] and lk[0]["counts"], "A: refparity passes and counts", results)
        ships = [x for x in lk if x["mode"] == "ship"]
        check(all(x["final"] for x in ships), f"A: every ship look is FINAL ({[(x['cand'], x['verdict'], x['not_final']) for x in ships]})", results)
        check(sm is not None and sm["decision"], f"A: summary decision = {sm and sm['decision']}", results)
        for n in ("q35_4b_pxE_fresh", "q35_4b_pxE_fresh_perm", "q35_4b_main500k", "q35_4b_main500k_perm",
                  "q35_4b_main500k_c2", "q35_4b_main500k_c2_perm"):
            check(exists(root, n), f"A: read {n} present", results)
        b = json.loads((root / "logs/gate4b/built_q35_4b_main500k_c2.json").read_text())
        check(b["modules"] == 248 and b["max_rel_err"] < 1e-12, f"A: C2 materialized from 4 real adapters, verify {b['max_rel_err']:.1e}", results)
    elif name == "A_ship":  # a clearly better C1 (stub gives it the gold side on 4% of yes/no rows): look 1 = SHIP
        build(root, "A")
        assert run(root, "manifest")[0] == 0
        rc, log = run(root, "vm-job1", {"q35_4b_main500k": {"improve_noul": 0.04},
                                        "q35_4b_main500k_c2": {"improve_noul": 0.02}})
        lk, sm = ledger(root), summary(root)
        ships = [x for x in lk if x["mode"] == "ship"]
        check(rc == 0 and len(ships) == 1 and ships[0]["verdict"] == "SHIP" and ships[0]["final"]
              and sm["decision"] == "SHIP q35_4b_main500k", f"A_ship: one ship look, SHIP and FINAL; decision {sm and sm['decision']}", results)
        check(sm is not None and "teacher_switch_c_dev_select_diff_pp" in sm,
              f"A_ship: summary reports the teacher-switch dev-select margin ({sm and sm.get('teacher_switch_c_dev_select_diff_pp')})", results)
    elif name == "A_split":  # STOP_BEFORE_SHIP on the VM, then the choice and the ship looks on the "Mac"
        build(root, "A")
        assert run(root, "manifest")[0] == 0
        rc, log = run(root, "vm-job1", MAP_NORMAL, {"STOP_BEFORE_SHIP": "1"})
        lk = ledger(root)
        check(rc == 0 and [x["mode"] for x in lk] == ["refparity", "c3trigger"] and "STOP_BEFORE_SHIP" in log,
              "A_split: the VM job stops after reads, parity look and C3 trigger (no ship look)", results)
        rc, log = run(root, "local-ship", None, args=["job1"])
        lk = ledger(root)
        ships = [x for x in lk if x["mode"] == "ship"]
        check(rc == 0 and ships and all(x["final"] for x in ships),
              f"A_split: local-ship makes the ship look(s), FINAL: {[(x['cand'], x['verdict'], x['final']) for x in ships]}", results)
    elif name == "A_c3":
        build(root, "A")
        assert run(root, "manifest")[0] == 0
        rc, log = run(root, "vm-job1", MAP_C3)
        lk = ledger(root)
        check(rc == 0 and [x["mode"] for x in lk] == ["refparity", "c3trigger"] and lk[1]["trigger"],
              f"A_c3: degraded C1 fires the C3 trigger ({lk[1]['failed'] if len(lk) > 1 else None}); job 1 makes no ship look", results)
        rc, log = run(root, "vm-job2", MAP_C3)
        lk, sm = ledger(root), summary(root)
        modes = [x["mode"] for x in lk]
        check(rc == 0 and modes[:3] == ["refparity", "c3trigger", "refparity"], f"A_c3: job 2 looks {modes}", results)
        check("MERGE CHECK q35_4b_main500k_c3w10 vs q35_4b_main500k_j2" in log and "FAIL" not in
              "".join(l for l in log.splitlines() if l.startswith("MERGE CHECK")), "A_c3: both merge checks run and pass", results)
        rep = json.loads((root / "logs/gate4b/replacement.json").read_text())
        check(rep["chosen"] == "q35_4b_main500k_c3", f"A_c3: replacement rule chooses {rep['chosen']}", results)
        ships = [x for x in lk if x["mode"] == "ship"]
        check(ships and ships[0]["cand"] == "q35_4b_main500k_c3" and ships[0]["ref"] == "q35_4b_pxE_fresh2",
              f"A_c3: ship look 1 is C3 vs the job-2 REF; looks {[(x['cand'], x['ref'], x['verdict'], x['final']) for x in ships]}", results)
        check(sm is not None, f"A_c3: summary decision = {sm and sm['decision']}", results)


def main():
    out = Path(sys.argv[1]).resolve()
    names = sys.argv[2:] or ["frozen", "B", "A", "A_rerun", "A_ship", "A_split", "A_c3"]
    results = []
    for n in names:
        scenario(out, n, results)
    for st, msg in results:
        print(f"[{st}] {msg}")
    sys.exit(0 if all(st == "PASS" for st, _ in results) else 1)


if __name__ == "__main__":
    main()
