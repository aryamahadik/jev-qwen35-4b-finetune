"""Stage one family's 1,500 new rows and write its frozen pilot config (A42-D 4.1, A37 (i); CPU only, no Modal call).

  cd lean/c2_build && ../../.venv/bin/python -B pilot_ab/make_config.py --family T40 --rows <1500-row train jsonl> \
      [--rels <relations jsonl>] [--dev-files <own dev jsonl> <gproxy jsonl> ...]

Writes pilot_ab/stage/<FAM>/{pilot_ab_train.jsonl, pilot_ab_rel.jsonl} (the ONLY files the Modal image mounts) and
pilot_ab/configs/<FAM>.json (every key written out). Checks: exactly 1,500 rows, unique ids, relation endpoints inside the
rows, no id shared with any given dev file, no never-open path, kd/ordinal counts measured on the rows, `epochs` = exactly
one real pass (replay_steps), seed 20261013. The staged rows are the family's rows UNCHANGED (never relabelled).
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common as C  # noqa: E402

sys.path.insert(0, str(C.LEAN))
QWEN35 = r".*layers\.\d+\..*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj|out_proj|in_proj[a-z_]*)"
H100_USD_H = 4.09          # measured all-in rate (logs/budget_ledger.md; extra/fix2_spawn.py RATE_PER_H)
STEP_S = 2.72              # C1's measured s/step on the H100 (logs/main4b_seg1-5.log); a pilot row is longer: see est()


def base_config(fam: str, epochs: float, n_ord: int, n_kd: int, n_kd_full: int) -> dict:
    """The C1 round-1 config (runs/q35_4b_c_r1.json) with the pilot's data, one pass, seed and no snapshots."""
    return {
        "name": C.pilot_name(fam), "base": C.BASE, "base_revision": C.BASE_REV, "recipe": "A3",
        "init_adapter": C.C1_INIT_VOL, "train_file": C.TRAIN_FILE, "rel_file": C.REL_FILE,
        "epochs": epochs, "lr": 5e-05, "batch": 16, "r": 16, "alpha": 32, "dropout": 0.05, "lam": 1.0, "beta": 0.0,
        "kd": 0.5, "kd_skip_src": ["blend50"], "kd_full_src": ["gd_gen2_probability"],
        "lam_inv": 1.0, "sym_cons": True, "perm_twin": 0.3, "lam_p": 0.5,
        "lam_ord": 1.0, "expect_ord_rows": n_ord, "aux_norm": "batch", "seed": C.SEED, "grad_ckpt": True,
        "style": C.STYLE, "layout": C.LAYOUT, "micro_tokens": 8192, "targets": "QWEN35",
        "snap_every": 0, "snap_fracs": [], "expect_trainable": C.EXPECT_TRAINABLE,
        "expect_kd_targets": n_kd, "expect_kd_full": n_kd_full, "ckpt_every_min": 10, "log_every": 10,
        "no_overwrite": True,
    }


def est(n_steps: int, mean_tokens: float = 740.0, batch: int = 16) -> dict:
    """Wall time and cost of the H100 training job. Step time scales C1's 2.72 s/step (mean ~600-740 padded tokens/step
    row in the main run) by tokens per step; start-up (image, base from the volume, adapter load) ~3 min; save ~0.5 min."""
    step = STEP_S * (mean_tokens / 700.0)
    minutes = n_steps * step / 60 + 3.0 + 0.5
    return {"steps": n_steps, "s_per_step": round(step, 2), "minutes": round(minutes, 1),
            "usd": round(minutes / 60 * H100_USD_H, 2), "rate_per_h": H100_USD_H}


def stage(fam, rows_path, rels_path=None, dev_files=(), out_root=None, quiet=False) -> dict:
    import train_decoder as td
    import replay_steps as rs
    if fam not in C.FAMILIES:
        raise SystemExit(f"unknown family {fam!r} (pilots: {C.FAMILIES})")
    rows = C.read_jsonl(rows_path)
    rels = C.read_jsonl(rels_path) if rels_path else []
    if len(rows) != C.ROWS_PER_PILOT:
        raise SystemExit(f"{rows_path}: {len(rows)} rows, A42-D 4.1 needs exactly {C.ROWS_PER_PILOT}")
    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids):
        raise SystemExit("duplicate row ids in the pilot rows")
    idset = set(ids)
    bad = [x for x in rels if x["a"] not in idset or x["b"] not in idset]
    if bad:
        raise SystemExit(f"{len(bad)} relation(s) point outside the 1,500 rows (first: {bad[0]})")
    for df in dev_files:
        dids = {r["id"] for r in C.read_jsonl(df)}
        both = idset & dids
        if both:
            raise SystemExit(f"{len(both)} pilot row id(s) are also in {df} (dev rows are never trained)")
    td.check_rows(rows, 0.5)
    n_ord = sum(1 for r in rows if td.is_ordinal(r))
    kd_rows = [r for r in rows if td.kd_target(r) is not None]
    n_kd = len(kd_rows)
    n_kd_full = sum(1 for r in kd_rows if r["source"] == "gd_gen2_probability" and r["qtype"] == "noul")
    out_root = Path(out_root) if out_root else HERE
    sd = out_root / "stage" / fam
    if sd.exists():
        shutil.rmtree(sd)
    sd.mkdir(parents=True)
    with open(sd / C.TRAIN_FILE, "w") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    with open(sd / C.REL_FILE, "w") as f:
        f.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in rels)
    # one real pass: replay train()'s data stream on the staged files (seed, batch, style, perm_twin as in the config)
    rep = rs.main(["--config", "", "--data-dir", str(sd), "--train-file", C.TRAIN_FILE, "--rel-file", C.REL_FILE,
                   "--seed", str(C.SEED), "--batch", "16", "--style", C.STYLE, "--perm-twin", "0.3"])
    cfg = base_config(fam, rep["epochs"], n_ord, n_kd, n_kd_full)
    k = math.ceil(len(rows) / 16 * cfg["epochs"])
    if k != rep["pass_batches"]:
        raise SystemExit(f"epochs {cfg['epochs']} gives {k} steps, one pass is {rep['pass_batches']}")
    (out_root / "configs").mkdir(exist_ok=True)
    (out_root / "configs" / f"{fam}.json").write_text(json.dumps(cfg, indent=2) + "\n")
    info = {"family": fam, "rows": len(rows), "relations": len(rels), "steps": k, "warmup_steps": rep["warmup_steps"],
            "ordinal_rows": n_ord, "kd_targets": n_kd, "dropped_rows": rep["dropped_rows"],
            "train_sha256": C.sha256_file(sd / C.TRAIN_FILE), "rel_sha256": C.sha256_file(sd / C.REL_FILE),
            "est_h100": est(k)}
    (out_root / "configs" / f"{fam}.stage.json").write_text(json.dumps(info, indent=2) + "\n")
    if not quiet:
        print(json.dumps(info, indent=1))
        if n_ord:
            print(f"NOTE: {n_ord} ordinal row(s) in the pilot rows: lam_ord 1.0 applies to them (A37 i: lam_ord is for "
                  "replay ordinal rows; no replay here). Tell the orchestrator if this is not intended.")
    return info


L4_MICRO_TOKENS = 4096     # UNPROVEN on the 24 GB L4 (the H100 smoke at 8192 reserved 28.6 GB); run `od_gcp.py smoke` first.
# micro_tokens is not part of the run identity under aux_norm "batch" (runs/README.md), so the loss is unchanged.


def l4_train_argv(cfg: dict, init_name: str = C.C1_NAME) -> list:
    """`od_gcp.py train ...` arguments that rebuild this config on the od-l4 VM (adapter folders under ~/lean/models,
    the two staged files copied to ~/lean/data). Every key not a CLI option goes through --extra."""
    cli = {"base", "recipe", "epochs", "lr", "batch", "lam", "r", "alpha", "train_file", "rel_file", "grad_ckpt", "beta",
           "style", "log_every", "kd", "init_adapter", "name", "targets"}
    extra = {k: v for k, v in cfg.items() if k not in cli}
    extra["micro_tokens"] = L4_MICRO_TOKENS
    return ["train", "--name", cfg["name"], "--base", cfg["base"], "--recipe", cfg["recipe"], "--epochs", repr(cfg["epochs"]),
            "--lr", repr(cfg["lr"]), "--batch", str(cfg["batch"]), "--lam", repr(cfg["lam"]), "--r", str(cfg["r"]),
            "--beta", repr(cfg["beta"]), "--kd", repr(cfg["kd"]), "--style", cfg["style"], "--train-file", cfg["train_file"],
            "--rel-file", cfg["rel_file"], "--init", init_name, "--log-every", str(cfg["log_every"]), "--splits", "",
            "--extra", json.dumps(extra, sort_keys=True)]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--family", required=True)
    ap.add_argument("--rows", required=True, help="the family's 1,500 new training rows (jsonl, train row format)")
    ap.add_argument("--rels", default="", help="the family's relations jsonl for those rows (complement/equiv/twin/inv)")
    ap.add_argument("--dev-files", nargs="*", default=[], help="dev jsonl files whose ids must not be in the rows")
    a = ap.parse_args(argv)
    info = stage(a.family, a.rows, a.rels or None, a.dev_files)
    cfg = json.loads((HERE / "configs" / f"{a.family}.json").read_text())
    print("L4 alternative (UNPROVEN memory; smoke first): python od_gcp.py " + " ".join(
        repr(x) if " " in x or x == "" or "{" in x else x for x in l4_train_argv(cfg)))
    return info


if __name__ == "__main__":
    main()
