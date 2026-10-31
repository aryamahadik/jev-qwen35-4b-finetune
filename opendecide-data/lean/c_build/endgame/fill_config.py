"""Fill the 5 FILL keys of runs/q35_4b_c_r1.json from mixer --final's config fill (RUNBOOK C3). CPU, no Modal.

Refuses unless: c_build/mix_r1/config_fill_r1.json and data/c_parts/c_mix_r1_manifest.json exist; the training and
relation files on disk have the sha256 both record; every FILL key gets a value (epochs, expect_ord_rows,
expect_kd_targets, expect_kd_full, seed); the seed is not C1's (20260925); no other key changes. The untouched template
is kept once as c_build/endgame/q35_4b_c_r1.template.json (r1_preflight.py compares against it).

  cd lean && ../.venv/bin/python c_build/endgame/fill_config.py [--dry-run]
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
CONFIG = LEAN / "runs/q35_4b_c_r1.json"
TEMPLATE = HERE / "q35_4b_c_r1.template.json"
FILL = LEAN / "c_build/mix_r1/config_fill_r1.json"
MANIFEST = LEAN / "data/c_parts/c_mix_r1_manifest.json"
KEYS = ("epochs", "expect_ord_rows", "expect_kd_targets", "expect_kd_full", "seed")
C1_SEED = 20260925


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    dry = "--dry-run" in sys.argv
    for p in (FILL, MANIFEST):
        if not p.exists():
            raise SystemExit(f"refused: {p.relative_to(LEAN)} missing (run mixer.py --final first)")
    fill, man = json.loads(FILL.read_text()), json.loads(MANIFEST.read_text())
    cfg = json.loads(CONFIG.read_text())
    if not TEMPLATE.exists():
        if any(not (isinstance(cfg.get(k), str) and cfg[k].startswith("FILL")) for k in KEYS):
            raise SystemExit("refused: no template saved and the config is not the FILL draft")
        if not dry:
            TEMPLATE.write_text(json.dumps(cfg, indent=2) + "\n")
    tmpl = json.loads(TEMPLATE.read_text()) if TEMPLATE.exists() else cfg
    probs = []
    for name, key in (("c_train_r1.jsonl", "train_file_sha256"), ("c_rel_r1.jsonl", "rel_file_sha256")):
        disk = sha(LEAN / "data/c_parts" / name)
        if disk != man["files"][name]["sha256"] or disk != fill.get(key):
            probs.append(f"{name}: sha256 on disk {disk[:12]} != manifest/config fill")
    vals = {k: fill.get(k) for k in KEYS}
    probs += [f"config fill has no value for {k}" for k, v in vals.items() if v is None]
    if vals["seed"] == C1_SEED:
        probs.append("seed equals C1's seed (recipe: a new seed)")
    if not isinstance(vals["epochs"], (int, float)) or not 0 < vals["epochs"] <= 3:
        probs.append(f"epochs {vals['epochs']!r} out of range")
    new = {**tmpl, **vals}
    changed = sorted(k for k in new if new[k] != tmpl.get(k))
    if set(changed) - set(KEYS):
        probs.append(f"keys other than the FILL keys would change: {sorted(set(changed) - set(KEYS))}")
    left = sorted(k for k, v in new.items() if isinstance(v, str) and v.startswith("FILL"))
    if left:
        probs.append(f"still FILL: {left}")
    if probs:
        raise SystemExit("refused:\n  " + "\n  ".join(probs))
    print(json.dumps({"fill": vals, "dry_run_steps": fill.get("dry_run_steps"),
                      "train_sha256": man["files"]["c_train_r1.jsonl"]["sha256"][:16]}))
    if not dry:
        CONFIG.write_text(json.dumps(new, indent=2) + "\n")
        print(f"written {CONFIG.relative_to(LEAN)}")


if __name__ == "__main__":
    main()
