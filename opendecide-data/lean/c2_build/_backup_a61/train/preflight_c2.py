"""preflight_c2.py: everything that must be true before C2 training launches (c2_chain.sh start runs it). Free: the
only external calls are `modal ... billing/app/volume ls/profile list` (control plane, no compute). EXIT 0 only on GO;
1 = not GO; 2 = `--offline` (account checks skipped: never a GO).

Checks (each prints PASS/FAIL):
  config   runs/q35_4b_c2.json = runs/q35_4b_c_r1.json except name, train/rel file, the four mixer fills, seed, snapshots
           (A37 i: lr 5e-5, one pass, seed 20261013, C1 init, r16/alpha32, expect_trainable 32,464,896);
           6-10 checkpoints (A42-D 9.1: snap_fracs + the final adapter), 25/50/75% kept for the stop rule, one near 33%.
  mix      data/c2_parts/c2_train.jsonl + c2_rel.jsonl hash-match c2_mix_manifest.json and mix_c2/config_fill_c2.json;
           the config's epochs / expect_* / seed equal the fill; rows within 50,000..125,000 (A42-D 1.4, spec 5.5);
           manifest ohs4 sha = Ruling A38's; the mix's projected cost <= T_max; pending_after_mix acknowledged.
  prereg   the A42-D block sha256 (A45 e) still matches; A38's OHS-4 sha is in PREREG; OWNER_GO_C2.txt exists.
  mount    modal_od_c2.py is current (make_modal_od_c2.py --check); its data mount keeps c2_train/c2_rel and drops every
           sealed/eval name (ohs, sealed, quarantine, longbench, jevbench, decision_index, ejs, jev); no mount entry
           and neither training path matches that list.
  money    T_max (A42-D 2.3) from logs/c2_spend.jsonl; with --fix-tmax it is written once (logs/c2_tmax.json).
  accounts mahadikarya2 and mahadikarya3 exist (no card account), credit left, no app running, C1 init adapter on
           both Volumes, no models/q35_4b_c2 yet on either; billing baselines recorded (logs/c2_baseline.json).
  monitor  snap_monitor_c2.py CPU test record current; gate_c2.py present; no stale stop/segment records.
  cd lean && ../.venv/bin/python -B c2_build/train/preflight_c2.py [--fix-tmax] [--ack-pending] [--offline]
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
C2 = LEAN / "c2_build"
LOGS = HERE / "logs"
sys.path.insert(0, str(HERE))
import c2_check  # noqa: E402

MODAL = str(LEAN.parent / ".venv/bin/modal")
CONFIG, TEMPLATE = LEAN / "runs/q35_4b_c2.json", LEAN / "runs/q35_4b_c_r1.json"
MIX_DIR = LEAN / "data/c2_parts"
MANIFEST, FILL = MIX_DIR / "c2_mix_manifest.json", C2 / "mix_c2/config_fill_c2.json"
PREREG = LEAN / "PREREG_FINAL.md"
A38_OHS4_SHA = "c0217e7739c570b9d22176b68e1c489623dcd5f7c551011606b6ff17e59c09c3"
A42D_BLOCK_SHA = "cbdc29d950bba3bad3e1fa2559346eae9405522c30bb7a4ffe0aaf7873665d2f"
SEED, C1_INIT, C1_SHA = 20261013, "/vol/models/q35_4b_main500k_init", "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
FILL_KEYS = ("epochs", "expect_ord_rows", "expect_kd_targets", "expect_kd_full")
ALLOWED_DIFF = {"name", "train_file", "rel_file", "seed", "snap_every", "snap_fracs", *FILL_KEYS}
DENY = re.compile(r"ohs|sealed|quarantine|longbench|jevbench|decision_index|ejs|jev", re.I)
MIN_ROWS, MAX_ROWS = 50_000, 125_000


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


class Sh:
    """The only way this script reaches Modal (tests replace it)."""

    def modal(self, profile: str, args: list, timeout: int = 120) -> tuple:
        env = {**os.environ, "MODAL_PROFILE": profile}          # MODAL_PROFILE is always passed
        try:
            r = subprocess.run([MODAL, *args], capture_output=True, text=True, timeout=timeout, env=env)
            return r.returncode, (r.stdout or "") + (r.stderr or "")
        except subprocess.TimeoutExpired:
            return 124, "timeout"


def check_config(cfg: dict, tmpl: dict, fill: dict | None) -> list:
    p = []
    fills = [k for k, v in cfg.items() if isinstance(v, str) and v.startswith("FILL")]
    if fills:
        p.append(f"config still has FILL values {fills} (after mix_c2.py --final run: preflight_c2.py fill)")
    diff = sorted(k for k in set(cfg) | set(tmpl) if cfg.get(k) != tmpl.get(k))
    if set(diff) - ALLOWED_DIFF:
        p.append(f"config differs from the round-1 recipe in {sorted(set(diff) - ALLOWED_DIFF)} (A37 i: recipe unchanged)")
    exp = {"seed": SEED, "lr": 5e-5, "batch": 16, "r": 16, "alpha": 32, "init_adapter": C1_INIT, "expect_trainable": 32464896,
           "name": "q35_4b_c2", "lam_ord": 1.0, "perm_twin": 0.3, "kd": 0.5, "micro_tokens": 8192, "no_overwrite": True,
           "train_file": "c2_parts/c2_train.jsonl", "rel_file": "c2_parts/c2_rel.jsonl"}
    p += [f"config {k} = {cfg.get(k)!r}, expected {v!r}" for k, v in exp.items() if cfg.get(k) != v]
    if "snap_every" in cfg:
        p.append("snap_every must be absent (checkpoints are exactly snap_fracs + the final adapter)")
    fr = cfg.get("snap_fracs") or []
    if not (6 <= len(fr) + 1 <= 10) or sorted(set(fr)) != list(fr) or not all(0 < f < 1 for f in fr):
        p.append(f"snap_fracs {fr}: need 5-9 sorted fractions in (0,1) (+ the final adapter = 6-10 checkpoints, A42-D 9.1)")
    if not all(f in fr for f in (0.25, 0.5, 0.75)):
        p.append("snap_fracs must keep 0.25, 0.5 and 0.75 (the A37 k stop-rule monitor reads them)")
    if fr and min(abs(f - 1 / 3) for f in fr) > 0.04:
        p.append("no snapshot within 0.04 of 33% (the early checkpoint of the early+late base)")
    if len([f for f in fr if f > 0.6]) < 2:
        p.append("need at least 2 snapshots after 60% so the last-3 average has 3 distinct late checkpoints")
    if fill:
        p += [f"config {k} = {cfg.get(k)!r} != mixer fill {fill.get(k)!r}" for k in FILL_KEYS + ("seed",)
              if cfg.get(k) != fill.get(k)]
    return p


def check_mix(manifest: dict, fill: dict, files: dict) -> tuple:
    """files = {name: sha256 on disk}. Returns (problems, info)."""
    p, info = [], {}
    for name in ("c2_train.jsonl", "c2_rel.jsonl"):
        want = (manifest.get("files") or {}).get(name, {}).get("sha256")
        got = files.get(name)
        key = "train_file_sha256" if "train" in name else "rel_file_sha256"
        if not want or got != want:
            p.append(f"{name}: sha256 on disk {str(got)[:12]} != manifest {str(want)[:12]}")
        if fill.get(key) != want:
            p.append(f"{name}: mix_c2/config_fill_c2.json {key} {str(fill.get(key))[:12]} != manifest")
    rows = (manifest.get("files") or {}).get("c2_train.jsonl", {}).get("rows")
    info["rows"] = rows
    if not isinstance(rows, int) or not MIN_ROWS <= rows <= MAX_ROWS:
        p.append(f"rows {rows!r} outside {MIN_ROWS:,}..{MAX_ROWS:,} (spec 5.5 floor, A42-D 1.4 cap)")
    if manifest.get("ohs4_manifest_sha256") != A38_OHS4_SHA:
        p.append(f"manifest ohs4_manifest_sha256 {str(manifest.get('ohs4_manifest_sha256'))[:12]} != Ruling A38's")
    if fill.get("seed") != SEED:
        p.append(f"fill seed {fill.get('seed')!r} != {SEED}")
    info["by_block"] = (manifest.get("counts") or {}).get("by_block")
    info["pending_after_mix"] = manifest.get("pending_after_mix")
    info["mix_projection_usd"] = manifest.get("budget_final_usd")
    return p, info


def check_mount(ignore, train_path: str, rel_path: str, top_level: list) -> list:
    p = []
    for q in (train_path, rel_path):
        if ignore(Path(q)):
            p.append(f"{q} is dropped by the image's data mount")
        if DENY.search(q):
            p.append(f"{q} matches the sealed/eval deny list")
    probes = ["ohs3_x.jsonl", "ohs3_parts/x", "ohs4_sealed/x", "ohs_ac_sealed/x", "OHS4/x", "sealed_nd/x",
              "bench/external_quarantine/x", "longbench_v2/x", "jevbench/x", "decision_index/x", "ejs5/x",
              "c2_parts/T40/out/candidates_c2.jsonl", "c2_parts/c2_mix_manifest.json", "c_parts/ohs_x.jsonl"]
    p += [f"mount keeps {x}" for x in probes if not ignore(Path(x))]
    p += [f"mount uploads top-level data/{n}" for n in top_level if DENY.search(n) and not ignore(Path(n))]
    return p


def prereg_checks(text: str) -> list:
    p = []
    lines = text.splitlines(True)
    try:
        a = next(i for i, ln in enumerate(lines) if ln.startswith("> **Ruling A42-D"))
        b = next(i for i in range(a, len(lines)) if lines[i].rstrip().endswith("13.8)."))
        got = hashlib.sha256("".join(lines[a:b + 1]).encode()).hexdigest()
        if got != A42D_BLOCK_SHA:
            p.append(f"A42-D block sha256 {got[:12]} != A45 (e) {A42D_BLOCK_SHA[:12]} (PREREG changed?)")
    except StopIteration:
        p.append("A42-D block not found in PREREG_FINAL.md")
    if A38_OHS4_SHA not in text:
        p.append("Ruling A38's OHS-4 manifest sha256 is not in PREREG_FINAL.md")
    return p


def check_accounts(sh: Sh, bill, profiles=c2_check.PROFILES) -> tuple:
    p, info, base = [], {}, {}
    rc, out = sh.modal(profiles[0], ["profile", "list"])
    for pr in profiles:
        if rc != 0 or pr not in out:
            p.append(f"modal profile {pr} not found (modal profile list rc {rc})")
    for pr in profiles:
        try:
            b = bill(pr)
        except Exception as e:  # noqa: BLE001
            p.append(f"{pr}: billing call failed ({e!r})")
            continue
        info[pr] = {"credit_left": b["credit_left"], "metered": b["metered"]}
        base[pr] = b["metered"]
        rc, out = sh.modal(pr, ["app", "list", "--json"], 90)
        try:
            apps = [a for a in json.loads(out[out.index("["):]) if str(a.get("State") or a.get("state") or "").lower() != "stopped"
                    and (int(a.get("Tasks") or a.get("tasks") or 0) > 0 or "ephemeral" in str(a.get("State") or "").lower()
                         or "detached" in str(a.get("State") or "").lower())]
        except (ValueError, TypeError):
            apps, p = [], p + [f"{pr}: modal app list not readable (rc {rc})"]
        if apps:
            p.append(f"{pr}: {len(apps)} app(s) already running")
        rc, out = sh.modal(pr, ["volume", "ls", "opendecide", "models/q35_4b_main500k_init"])
        if rc != 0 or "adapter_model.safetensors" not in out:
            p.append(f"{pr}: C1 init adapter models/q35_4b_main500k_init missing on the Volume (rc {rc})")
        rc, out = sh.modal(pr, ["volume", "ls", "opendecide", "models/q35_4b_c2"])
        if rc == 0 and out.strip() and "no such" not in out.lower() and "not found" not in out.lower():
            p.append(f"{pr}: models/q35_4b_c2 already exists on the Volume (no_overwrite)")
    return p, info, base


def fill_config(dry: bool = False) -> int:
    """Writes the four mixer fills (and nothing else) into runs/q35_4b_c2.json from mix_c2/config_fill_c2.json, after the
    mix files' sha256 match the manifest (as c_build/endgame/fill_config.py did for round 1)."""
    if not (MANIFEST.exists() and FILL.exists()):
        print("refused: run mix_c2.py --final first")
        return 1
    man, fill, cfg = json.loads(MANIFEST.read_text()), json.loads(FILL.read_text()), json.loads(CONFIG.read_text())
    files = {n: sha_file(MIX_DIR / n) for n in ("c2_train.jsonl", "c2_rel.jsonl")}
    probs, _ = check_mix(man, fill, files)
    probs += [f"fill has no value for {k}" for k in FILL_KEYS if fill.get(k) is None]
    if not isinstance(fill.get("epochs"), (int, float)) or not 0 < fill["epochs"] <= 3:
        probs.append(f"epochs {fill.get('epochs')!r} out of range")
    if probs:
        print("refused:\n  " + "\n  ".join(probs))
        return 1
    new = {**cfg, **{k: fill[k] for k in FILL_KEYS}}
    print(json.dumps({k: [cfg[k], new[k]] for k in FILL_KEYS}))
    if not dry:
        CONFIG.write_text(json.dumps(new, indent=2) + "\n")
    return 0


def run(a: list, sh: Sh | None = None, bill=None) -> int:
    sh, bill = sh or Sh(), bill or c2_check.BILL
    offline, fix = "--offline" in a, "--fix-tmax" in a
    rep, probs = {}, []
    cfg, tmpl = json.loads(CONFIG.read_text()), json.loads(TEMPLATE.read_text())
    man = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else None
    fill = json.loads(FILL.read_text()) if FILL.exists() else None
    if man is None or fill is None:
        probs.append(f"mix not built: {MANIFEST.relative_to(LEAN)} / {FILL.relative_to(LEAN)} missing (mix_c2.py --final)")
    probs += check_config(cfg, tmpl, fill)
    if man and fill:
        files = {n: sha_file(MIX_DIR / n) for n in ("c2_train.jsonl", "c2_rel.jsonl") if (MIX_DIR / n).exists()}
        mp, rep["mix"] = check_mix(man, fill, files)
        probs += mp
        if "--ack-pending" not in a and rep["mix"].get("pending_after_mix"):
            probs.append(f"manifest pending_after_mix {rep['mix']['pending_after_mix']} not acknowledged (--ack-pending)")
    probs += prereg_checks(PREREG.read_text())
    if not (HERE / "OWNER_GO_C2.txt").exists() or not (HERE / "OWNER_GO_C2.txt").read_text().strip():
        probs.append("train/OWNER_GO_C2.txt missing or empty (the owner's GO before C2 training, A37 l)")
    if subprocess.run([sys.executable, "-B", str(HERE / "make_modal_od_c2.py"), "--check"], capture_output=True).returncode:
        probs.append("modal_od_c2.py is stale or missing (run make_modal_od_c2.py)")
    else:
        sys.path.insert(0, str(HERE))
        import modal_od_c2
        top = sorted(e.name for e in os.scandir(LEAN / "data"))      # names only; nothing is opened
        probs += check_mount(modal_od_c2._data_ignore, cfg["train_file"], cfg["rel_file"], top)
    try:
        t_max = c2_check.tmax(fix=fix and not offline)
    except c2_check.Verdict as v:
        probs.append(v.verdict)
        t_max = 0.0
    rep["money"] = {"t_max": t_max, "spent_other_usd": c2_check.spend_other(), "cap_total": c2_check.CAP_TOTAL,
                    "t_max_fixed": (LOGS / "c2_tmax.json").exists()}
    if not (LOGS / "c2_tmax.json").exists() and not offline:
        probs.append("T_max not fixed yet (run with --fix-tmax at the training GO)")
    proj = (rep.get("mix") or {}).get("mix_projection_usd")
    if isinstance(proj, (int, float)) and proj > t_max:
        probs.append(f"mix projection ${proj} > T_max ${t_max} (A42-D 2.3: trim with mix_c2.py first)")
    try:
        sys.path.insert(0, str(C2))
        import snap_monitor_c2
        why = snap_monitor_c2.cputest_ok()
        if why:
            probs.append(f"snap_monitor_c2 CPU test record: {why}")
    except Exception as e:  # noqa: BLE001
        probs.append(f"snap_monitor_c2 not importable ({e!r})")
    if not (C2 / "gate_c2.py").exists():
        probs.append("gate_c2.py missing")
    stale = [n for n in ("c2_segments.jsonl", "c2_stop_after_min.txt", "c2_baseline.json", "c2_check_proj.json")
             if (LOGS / n).exists()]
    stale += [str(q.name) for q in (LEAN / "logs").glob("relay_q35_4b_c2_*.json")]
    stale += [n for n in ("snap_monitor_c2_stop.json", "snap_monitor_c2_escalation.json", "snap_monitor_c2_state.json")
              if (C2 / "logs" / n).exists()]
    if stale:
        probs.append(f"stale records of an earlier attempt: {stale} (move them aside; the owner decides)")
    base = {}
    if not offline:
        ap, rep["accounts"], base = check_accounts(sh, bill)
        probs += ap
        cr = sum(float(v["credit_left"]) for v in rep["accounts"].values())
        rep["free_credit_total_usd"] = round(cr, 2)
        rep["free_credit_covers_t_max"] = cr - 2 * c2_check.CREDIT_RESERVE >= t_max
    rep["problems"] = probs
    verdict = "NOT GO" if probs else ("OFFLINE (accounts unchecked; never a GO)" if offline else "GO")
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / "c2_check_preflight.json").write_text(json.dumps({**rep, "decision": verdict, "utc": time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, indent=1, default=str))
    if verdict == "GO":
        (LOGS / "c2_baseline.json").write_text(json.dumps({"profiles": base, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                                                                  time.gmtime())}))
    for k, v in rep.items():
        print(f"{k}: {json.dumps(v, default=str)[:220]}")
    print(verdict)
    return 0 if verdict == "GO" else 2 if verdict.startswith("OFFLINE") and not probs else 1


if __name__ == "__main__":
    argv = sys.argv[1:]
    sys.exit(fill_config("--dry-run" in argv) if argv[:1] == ["fill"] else run(argv))
