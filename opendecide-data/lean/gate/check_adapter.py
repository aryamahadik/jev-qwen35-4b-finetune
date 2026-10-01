"""Check a downloaded q35_4b_main500k adapter folder (the final adapter or a snapshot) before it goes to the L4:
files present, LoRA config as the frozen run config says (r16 / alpha 32, QWEN35 targets, no DoRA / rsLoRA), 496 fp32
lora tensors of the right ranks, all finite and B not all zero, train_meta cfg equal to runs/q35_4b_main.json on the
keys that decide the read and the run (base, base_revision, layout, style, r, alpha, lr, epochs, seed, train_file),
steps 30,457, the snapshot step (snapshots), the chat template sha of every Qwen3.5-4B adapter, and no PRISM-X files.
Prints the sha256 of adapter_model.safetensors. CPU only, read only.
  python gate/check_adapter.py models/q35_4b_main500k [--snapshot 25888]
  python gate/check_adapter.py /Users/.../backups/modal_models/q35_4b_main500k/snaps/s025888 --snapshot 25888
Exit 0 = OK, 1 = problems (listed).
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import torch
from safetensors import safe_open

HERE = Path(__file__).resolve().parents[1]
RUN_CFG = HERE / "runs/q35_4b_main.json"
CHAT_TEMPLATE_SHA = "a4aee8afcf2e0711942cf848899be66016f8d14a889ff9ede07bca099c28f715"  # every Qwen3.5-4B adapter so far
QWEN35_TARGETS = r".*layers\.\d+\..*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj|out_proj|in_proj[a-z_]*)"
N_TENSORS, N_STEPS = 496, 30457
CFG_KEYS = ("base", "base_revision", "layout", "style", "r", "alpha", "lr", "epochs", "seed", "train_file")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def check(d, snapshot=None, run_cfg=RUN_CFG):
    d, bad = Path(d), []
    need = ["adapter_config.json", "adapter_model.safetensors", "train_meta.json", "tokenizer.json",
            "tokenizer_config.json", "chat_template.jinja"]
    miss = [f for f in need if not (d / f).exists()]
    if miss:
        return [f"missing files: {miss}"], None
    if any((d / f).exists() for f in ("prism_x.json", "prism_x.safetensors")):
        bad.append("PRISM-X files present (the 4B has no PRISM-X)")
    c = json.loads((d / "adapter_config.json").read_text())
    for k, v in (("r", 16), ("lora_alpha", 32), ("use_dora", False), ("use_rslora", False), ("peft_type", "LORA"),
                 ("target_modules", QWEN35_TARGETS)):
        if c.get(k) != v:
            bad.append(f"adapter_config {k} = {c.get(k)!r}, expected {v!r}")
    if sha256(d / "chat_template.jinja") != CHAT_TEMPLATE_SHA:
        bad.append("chat_template.jinja differs from every earlier Qwen3.5-4B adapter (pipeline check would split)")
    m = json.loads((d / "train_meta.json").read_text())
    cfg, want = m.get("cfg") or {}, json.loads(Path(run_cfg).read_text())
    for k in CFG_KEYS:
        if cfg.get(k) != want.get(k):
            bad.append(f"train_meta cfg {k} = {cfg.get(k)!r}, runs/q35_4b_main.json has {want.get(k)!r}")
    if m.get("steps") != N_STEPS:
        bad.append(f"train_meta steps = {m.get('steps')!r}, expected {N_STEPS}")
    if snapshot is None:
        if "snapshot_step" in m:
            bad.append(f"this is a snapshot (snapshot_step {m['snapshot_step']}), not the final adapter")
        for k in ("env", "code", "data"):
            if k not in m:
                bad.append(f"final train_meta has no {k!r} record (not a finished run?)")
    elif m.get("snapshot_step") != snapshot:
        bad.append(f"snapshot_step = {m.get('snapshot_step')!r}, expected {snapshot}")
    n = 0
    with safe_open(str(d / "adapter_model.safetensors"), "pt") as f:
        keys = list(f.keys())
        if len(keys) != N_TENSORS:
            bad.append(f"{len(keys)} tensors, expected {N_TENSORS}")
        zero_b = 0
        for k in keys:
            t = f.get_tensor(k)
            if t.dtype != torch.float32:
                bad.append(f"{k} is {t.dtype}")
                break
            if not torch.isfinite(t).all():
                bad.append(f"{k} has non-finite values")
                break
            if k.endswith("lora_A.weight") and t.shape[0] != 16 or k.endswith("lora_B.weight") and t.shape[1] != 16:
                bad.append(f"{k} shape {tuple(t.shape)} is not rank 16")
                break
            if k.endswith("lora_B.weight"):
                zero_b += int(t.abs().max().item() == 0.0)
            n += 1
        if zero_b == sum(k.endswith("lora_B.weight") for k in keys):
            bad.append("every lora_B is zero (an untrained adapter)")
    return bad, sha256(d / "adapter_model.safetensors")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("adapter")
    ap.add_argument("--snapshot", type=int, default=None, help="expected snapshot_step (omit for the final adapter)")
    a = ap.parse_args(argv)
    bad, sha = check(a.adapter, a.snapshot)
    print(json.dumps({"adapter": a.adapter, "ok": not bad, "problems": bad, "adapter_sha256": sha}))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
