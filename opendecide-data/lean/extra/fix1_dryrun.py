"""CPU dry run of the 4B top-up q35_4b_main500k_fix1: builds the exact config the launcher sends
(extra/fix1_spawn.build_cfg), checks the data files, the image data mount, the init adapter (the local C1 backup:
config, fp32, trainable count, sha256 = the gate's C1), the one-pass step count (replay_steps) and the learning-rate
schedule, then runs train_decoder.train() itself on CPU and stops it at the model load (train_decoder.load is replaced
by a function that raises). Everything train() does before the load runs for real: the unknown-key check, the style
and layout checks, reading the data, check_rows, make_units, the kd counts and expect_kd_targets / expect_kd_full.
No GPU, no Modal call, no network (the modal package is imported, nothing is sent).

  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python extra/fix1_dryrun.py [--out <json>]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import tempfile
from pathlib import Path

LEAN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LEAN))
sys.path.insert(0, str(LEAN / "extra"))
sys.dont_write_bytecode = True

import fix1_spawn as fs  # noqa: E402  (imports modal_od: defines the app and images, sends nothing)
import replay_steps as rs  # noqa: E402

BACKUP = Path("/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k")
MAIN_CFG = LEAN / "runs/q35_4b_main.json"
# keys that must equal the main run's (the top-up continues the same model with the same loss)
SAME_AS_MAIN = ("base", "base_revision", "recipe", "batch", "r", "alpha", "dropout", "lam", "beta", "kd", "kd_skip_src",
                "kd_full_src", "lam_inv", "sym_cons", "perm_twin", "lam_p", "aux_norm", "grad_ckpt", "style", "layout",
                "micro_tokens", "targets", "expect_trainable")


class StopBeforeModelLoad(Exception):
    pass


def init_adapter_checks(cfg) -> dict:
    import torch
    from safetensors import safe_open
    ac = json.loads((BACKUP / "adapter_config.json").read_text())
    bad = []
    for k, v in (("r", cfg["r"]), ("lora_alpha", cfg["alpha"]), ("lora_dropout", cfg["dropout"]),
                 ("target_modules", fs.QWEN35_TARGETS), ("use_dora", False), ("use_rslora", False),
                 ("peft_type", "LORA"), ("base_model_name_or_path", cfg["base"])):
        if ac.get(k) != v:
            bad.append(f"adapter_config {k} = {ac.get(k)!r}, expected {v!r}")
    n, dtypes, keys = 0, set(), 0
    with safe_open(str(BACKUP / "adapter_model.safetensors"), "pt") as f:
        for k in f.keys():
            t = f.get_tensor(k)
            n += t.numel()
            dtypes.add(str(t.dtype))
            keys += 1
            if not torch.isfinite(t).all():
                bad.append(f"{k} not finite")
    if n != cfg["expect_trainable"]:
        bad.append(f"adapter has {n} parameters, expect_trainable is {cfg['expect_trainable']}")
    if dtypes != {"torch.float32"}:
        bad.append(f"adapter dtypes {dtypes} (train() needs fp32 trainable parameters)")
    sha = {f: fs.sha256_file(BACKUP / f) for f in fs.INIT_FILES}
    if sha != fs.c1_sha():
        bad.append(f"backup sha256 {sha} differs from the gate's C1 {fs.c1_sha()}")
    meta = json.loads((BACKUP / "train_meta.json").read_text())
    code_now = {m: fs.sha256_file(LEAN / f"{m}.py") for m in ("train_decoder", "decoder_io", "prism_x", "writeblock")}
    if meta.get("code") != code_now:
        bad.append(f"frozen code differs from the main run's: {meta.get('code')} vs {code_now}")
    return {"tensors": keys, "parameters": n, "dtypes": sorted(dtypes), "sha256": sha,
            "main_run_steps": meta.get("steps"), "code_equals_main_run": meta.get("code") == code_now, "problems": bad}


def lr_points(lr, n_steps):
    """train_decoder's schedule: linear warm-up over int(0.05 n) steps, then cosine to 0 (LambdaLR, one sched.step()
    per step; the lr of step s is lr * f(s))."""
    warm = int(0.05 * n_steps)
    f = lambda s: (s + 1) / max(1, warm) if s < warm else 0.5 * (1 + math.cos(math.pi * (s - warm) / max(1, n_steps - warm)))  # noqa: E731
    pts = sorted({0, warm - 1, warm, n_steps // 4, n_steps // 2, (3 * n_steps) // 4, n_steps - 1})
    mean = sum(lr * f(s) for s in range(n_steps)) / n_steps
    return {"warmup_steps": warm, "lr_at_step": {str(s): float(f"{lr * f(s):.3e}") for s in pts if s >= 0},
            "mean_lr": float(f"{mean:.3e}"), "sum_lr": round(sum(lr * f(s) for s in range(n_steps)), 5)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="")
    a = ap.parse_args(argv)
    res = {}
    # 1. the exact cfg the launcher sends (fixed clock so the dry run is reproducible)
    name, cfg = fs.build_cfg(fs.CONFIG, expect_resume=False, stop_after_min=240, stop_at_step=0, log_every=0, now=0.0)
    res["name"], res["cfg_sent"] = name, cfg
    main_cfg = json.loads(MAIN_CFG.read_text())
    raw = json.loads((LEAN / fs.CONFIG).read_text())
    res["differs_from_main_run"] = {k: [main_cfg.get(k), raw.get(k)] for k in sorted(set(main_cfg) | set(raw))
                                    if main_cfg.get(k) != raw.get(k)}
    bad_same = [k for k in SAME_AS_MAIN if main_cfg.get(k) != raw.get(k)]
    if bad_same:
        raise SystemExit(f"keys that must equal the main run's differ: {bad_same}")
    # 2. data files and the image data mount
    res["data_sha256"] = fs.local_checks(cfg)
    import modal_od
    res["data_mount"] = {f: not modal_od._data_ignore(Path(f)) for f in (cfg["train_file"], cfg["rel_file"])}
    # what this launcher's image would upload from data/ (the same ignore rule Modal applies to every path)
    up, n_up = 0, 0
    for q in sorted((LEAN / "data").rglob("*")):
        rel = q.relative_to(LEAN / "data")
        if q.is_file() and not any(modal_od._data_ignore(Path(*rel.parts[:i])) for i in range(1, len(rel.parts) + 1)):
            up, n_up = up + q.stat().st_size, n_up + 1
    v14 = sorted(str(q.relative_to(LEAN / "data")) for q in (LEAN / "data/v14_parts").iterdir()
                 if q.is_file() and not modal_od._data_ignore(q.relative_to(LEAN / "data")))
    res["data_mount_upload"] = {"files": n_up, "gb": round(up / 1e9, 2), "v14_parts_files": v14}
    if v14 != sorted(f"v14_parts/{f}" for f in fs.FIX1_FILES):
        raise SystemExit(f"the image would carry other v14_parts files: {v14}")
    # 3. init adapter (local backup = what is uploaded)
    res["init_adapter"] = init_adapter_checks(cfg)
    if res["init_adapter"]["problems"]:
        raise SystemExit(f"init adapter problems: {res['init_adapter']['problems']}")
    # 4. one pass, as train() draws it
    with tempfile.TemporaryDirectory() as td_:
        rep = rs.main(["--config", fs.CONFIG, "--out", str(Path(td_) / "replay.json")])
    if not rep.get("config_is_one_pass"):
        raise SystemExit(f"epochs {cfg['epochs']} is not one pass: config gives {rep.get('config_n_steps')} steps, the "
                         f"pass is {rep['pass_batches']} batches (set epochs to {rep['epochs']!r})")
    res["replay"] = {k: rep[k] for k in ("rows", "relations", "units", "inv_merged", "pass_batches", "pass_rows",
                                         "mean_rows_per_batch", "dropped_units", "dropped_rows", "epochs",
                                         "epochs_check", "config_n_steps", "config_is_one_pass", "warmup_steps",
                                         "ramp_full_from_step")}
    res["lr_schedule"] = lr_points(cfg["lr"], rep["config_n_steps"])
    # 5. train() itself, stopped at the model load
    import decoder_io
    import train_decoder as td
    decoder_io.STYLE = cfg.get("style", "od")  # as modal_od.train_relay35 does
    seen = {}

    def stop_load(base, dev, **kw):
        seen.update({"base": base, "dev": dev, **kw})
        raise StopBeforeModelLoad()

    td.load = stop_load
    try:
        import peft  # noqa: F401
    except ModuleNotFoundError:  # the laptop venv has no peft; train() imports it just before the load. A stand-in
        import types            # that raises on any use (nothing uses it before the load); the image pins peft 0.21.0

        def _never(*a, **k):
            raise RuntimeError("peft stand-in used: the dry run went past the model load")
        sys.modules["peft"] = types.SimpleNamespace(LoraConfig=_never, get_peft_model=_never, PeftModel=_never)
        res["peft_stand_in"] = True
    with tempfile.TemporaryDirectory() as out:
        try:
            td.train(dict(cfg), LEAN / "data", Path(out) / name, dev="cpu")
            raise SystemExit("train() returned without loading a model (unexpected)")
        except StopBeforeModelLoad:
            res["train_reached_model_load"] = {"load_args": seen, "layout": decoder_io.LAYOUT,
                                               "style": decoder_io.STYLE}
    print(json.dumps({k: v for k, v in res.items() if k != "cfg_sent"}, indent=1))
    print("DRY RUN OK: config built, data verified, init adapter verified, train() stopped at the model load")
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=1) + "\n")


if __name__ == "__main__":
    main()
