"""Check a downloaded q35_4b_main500k_fix1 adapter folder (candidate C4, draft amendment A8) before it goes to the L4.

Runs every check of gate/check_adapter.py against runs/q35_4b_fix1.json (files, LoRA config r16 / alpha 32 / QWEN35
targets, 496 finite fp32 tensors, chat template sha, train_meta cfg on base / revision / layout / style / r / alpha /
lr / epochs / seed / train_file, no PRISM-X files), with the fix1 step count, and adds:
  - train_meta cfg init_adapter is the C1 copy (/vol/models/q35_4b_main500k_init), rel_file is the fix1 relations;
  - train_meta data = the sha256 of data/v14_parts/fix1_train.jsonl and fix1_relations.jsonl (fix1_counts.json);
  - train_meta code = the main run's code (the frozen train_decoder / decoder_io / prism_x / writeblock);
  - the adapter differs from C1 (training happened) and how far it moved (report: relative change of the LoRA
    product B @ A per module, median and max; for orientation only).
CPU only, read only.  python gate/check_adapter_fix1.py <folder> [--c1 <C1 folder>]
Exit 0 = OK, 1 = problems (listed).
"""
import argparse
import json
import math
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "gate"))
import check_adapter as ca  # noqa: E402

FIX1_CFG = HERE / "runs/q35_4b_fix1.json"
COUNTS = HERE / "data/v14_parts/fix1_counts.json"
C1_DEFAULT = Path("/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k")
INIT_DIR = "/vol/models/q35_4b_main500k_init"


def fix1_steps(cfg) -> int:
    rows = json.loads(COUNTS.read_text())["rows"]
    return math.ceil(rows / cfg["batch"] * cfg["epochs"])


def lora_delta(d, c1):
    """Relative Frobenius change of B @ A per LoRA module, fix1 vs C1."""
    import torch
    from safetensors.torch import load_file
    a, b = load_file(str(Path(d) / "adapter_model.safetensors")), load_file(str(Path(c1) / "adapter_model.safetensors"))
    if set(a) != set(b):
        return None, "tensor names differ from C1"
    rel, same = [], True
    for k in sorted(a):
        if not k.endswith("lora_A.weight"):
            continue
        kb = k.replace("lora_A", "lora_B")
        w_new, w_old = a[kb].double() @ a[k].double(), b[kb].double() @ b[k].double()
        same &= torch.equal(a[k], b[k]) and torch.equal(a[kb], b[kb])
        rel.append(float((w_new - w_old).norm() / max(float(w_old.norm()), 1e-12)))
    return {"modules": len(rel), "median_rel_change": statistics.median(rel), "max_rel_change": max(rel),
            "identical_to_c1": same}, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--c1", default=str(C1_DEFAULT))
    a = ap.parse_args()
    cfg = json.loads(FIX1_CFG.read_text())
    ca.N_STEPS = fix1_steps(cfg)
    bad, sha = ca.check(a.folder, None, run_cfg=FIX1_CFG)
    d = Path(a.folder)
    if (d / "train_meta.json").exists():
        m = json.loads((d / "train_meta.json").read_text())
        mc = m.get("cfg") or {}
        if mc.get("init_adapter") != INIT_DIR:
            bad.append(f"train_meta cfg init_adapter = {mc.get('init_adapter')!r}, expected {INIT_DIR!r}")
        if mc.get("rel_file") != cfg["rel_file"]:
            bad.append(f"train_meta cfg rel_file = {mc.get('rel_file')!r}, expected {cfg['rel_file']!r}")
        files = json.loads(COUNTS.read_text())["files"]
        want = [files[cfg["train_file"]], files[cfg["rel_file"]]]
        if m.get("data") != want:
            bad.append(f"train_meta data {m.get('data')} is not the fix1 files' sha256 {want}")
        c1m = json.loads((Path(a.c1) / "train_meta.json").read_text())
        if m.get("code") != c1m.get("code"):
            bad.append(f"train_meta code differs from the main run's: {m.get('code')} vs {c1m.get('code')}")
        if m.get("env", {}).get("peft") != c1m.get("env", {}).get("peft"):
            bad.append(f"peft {m.get('env', {}).get('peft')} differs from the main run's {c1m.get('env', {}).get('peft')}")
    delta, err = lora_delta(d, a.c1) if (d / "adapter_model.safetensors").exists() else (None, "no adapter")
    if err:
        bad.append(err)
    elif delta["identical_to_c1"]:
        bad.append("the adapter is identical to C1 (no training happened)")
    print(json.dumps({"folder": str(d), "steps_expected": ca.N_STEPS, "adapter_sha256": sha, "vs_c1": delta,
                      "problems": bad}, indent=1))
    print("OK" if not bad else f"PROBLEMS: {len(bad)}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
