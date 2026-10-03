"""Check a downloaded q35_4b_main500k_fix2 adapter folder (candidate C4, draft amendment A8-prime) before it goes to the
L4. CPU only, read only.

Runs every check of gate/check_adapter.py against runs/q35_4b_fix2.json (files, LoRA config r16 / alpha 32 / QWEN35
targets, 496 finite fp32 rank-16 tensors, the chat template sha of every Qwen3.5-4B adapter, train_meta cfg on base /
revision / layout / style / r / alpha / lr / epochs / seed / train_file, no PRISM-X files, not a snapshot), with the
fix2 step count (one pass, train()'s own formula on fix2_counts.json rows), and adds:
  - train_meta steps = that count and no snapshot folder (A8-prime B: no snapshots, C4 = the last step);
  - train_meta cfg: init_adapter = the C1 copy (/vol/models/q35_4b_main500k_init), rel_file = fix2 relations,
    lr 2e-5, every key of runs/q35_4b_fix2.json that train() records equal to the config (RUN_KEYS excepted);
  - train_meta data = the sha256 of data/v14_parts/fix2_train.jsonl and fix2_relations.jsonl (fix2_counts.json);
  - train_meta code = the main run's code (frozen train_decoder / decoder_io / prism_x / writeblock) and the same peft;
  - the C1 init copy it started from is the gated C1 (507d1c29...: the local C1 backup is checked);
  - the adapter differs from C1 (training happened); how far it moved is reported (relative change of B @ A).
  python gate/check_adapter_fix2.py <folder> [--c1 <C1 folder>]          Exit 0 = OK, 1 = problems (listed).
"""
import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "gate"))
import check_adapter as ca  # noqa: E402
import check_adapter_fix1 as c1chk  # noqa: E402  (lora_delta)

FIX2_CFG = HERE / "runs/q35_4b_fix2.json"
COUNTS = HERE / "data/v14_parts/fix2_counts.json"
C1_DEFAULT = Path("/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k")
C1_ADAPTER_SHA = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
INIT_DIR = "/vol/models/q35_4b_main500k_init"
RUN_KEYS = {"resume", "ckpt_every_min", "log_every", "expect_resume", "stop_after_min", "stop_at_step",
            "allow_code_change", "allow_env_change", "fresh_start", "stop_at_unix", "snap_every", "snap_fracs",
            "expect_trainable", "expect_kd_targets", "expect_kd_full", "name", "no_overwrite"}


def fix2_steps(cfg) -> int:
    rows = json.loads(COUNTS.read_text())["rows"]
    return math.ceil(rows / cfg["batch"] * cfg["epochs"])


def check(folder, c1=C1_DEFAULT):
    cfg = json.loads(FIX2_CFG.read_text())
    ca.N_STEPS = fix2_steps(cfg)
    bad, sha = ca.check(folder, None, run_cfg=FIX2_CFG)
    d = Path(folder)
    if (d / "snaps").exists():
        bad.append("a snaps/ folder exists: A8-prime B allows no snapshot")
    if ca.sha256(Path(c1) / "adapter_model.safetensors") != C1_ADAPTER_SHA:
        bad.append("the C1 folder given is not the gated C1 (sha256)")
    if (d / "train_meta.json").exists():
        m = json.loads((d / "train_meta.json").read_text())
        mc = m.get("cfg") or {}
        if mc.get("init_adapter") != INIT_DIR:
            bad.append(f"train_meta cfg init_adapter = {mc.get('init_adapter')!r}, expected {INIT_DIR!r}")
        for k, v in cfg.items():
            if k in RUN_KEYS or k == "targets":
                continue
            if mc.get(k) != v:
                bad.append(f"train_meta cfg {k} = {mc.get(k)!r}, runs/q35_4b_fix2.json has {v!r}")
        files = json.loads(COUNTS.read_text())["files"]
        want = [files[cfg["train_file"]], files[cfg["rel_file"]]]
        if m.get("data") != want:
            bad.append(f"train_meta data {m.get('data')} is not the fix2 files' sha256 {want}")
        c1m = json.loads((Path(c1) / "train_meta.json").read_text())
        if m.get("code") != c1m.get("code"):
            bad.append(f"train_meta code differs from the main run's: {m.get('code')} vs {c1m.get('code')}")
        if m.get("env", {}).get("peft") != c1m.get("env", {}).get("peft"):
            bad.append(f"peft {m.get('env', {}).get('peft')} differs from the main run's {c1m.get('env', {}).get('peft')}")
    delta, err = c1chk.lora_delta(d, c1) if (d / "adapter_model.safetensors").exists() else (None, "no adapter")
    if err:
        bad.append(err)
    elif delta["identical_to_c1"]:
        bad.append("the adapter is identical to C1 (no training happened)")
    return bad, sha, delta, ca.N_STEPS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--c1", default=str(C1_DEFAULT))
    a = ap.parse_args()
    bad, sha, delta, n = check(a.folder, a.c1)
    print(json.dumps({"folder": a.folder, "steps_expected": n, "adapter_sha256": sha, "vs_c1": delta, "problems": bad},
                     indent=1))
    print("OK" if not bad else f"PROBLEMS: {len(bad)}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
