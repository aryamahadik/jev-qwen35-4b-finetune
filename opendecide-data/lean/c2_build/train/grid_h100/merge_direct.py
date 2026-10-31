"""grid_h100.merge_direct: a LoRA adapter (C1, or one stacked-LoRA grid candidate) merged into the Qwen3.5-4B base in BF16, written in the
BASE LAYOUT of hosting/export_c1_merged.py (same shard names, keys, dtypes, index, config, tokenizer and processor files, vision / MTP
tensors copied byte for byte), plus c1_tokenizer/ and merge_manifest.json. This is the fast sibling of export_c1_merged.export_local:
export_local runs decoder_io.load + PEFT merge_and_unload and a long list of re-reads (10-25 min per model), far too slow for 19 models.

The arithmetic is PEFT's own merge, written out: for every LoRA target   W' = bf16( float32(W) + (B_fp32 @ A_fp32) * (alpha / r) )
(export_c1_merged.formula_check recomputes the same formula; torch TF32 is switched off). The 48 tensors the base stores in F32
in the base: the 24 `linear_attn.norm.weight` keep the F32 dtype with the value HF's BF16 load gives them (rounded through BF16), the 24
`linear_attn.A_log` stay F32 bitwise (HF keeps them in F32), exactly as the production export's `rounded_like_hf` / `same_as_base` lists show;
any other F32 base tensor is refused (fail closed). Everything else is the base's tensor, bitwise. Checks (any failure = no manifest): every adapter module is a base tensor and every
target changed; shapes / dtypes of all keys equal the base's; a sample of written targets recomputed from the written file;
vision / MTP bytes equal the base's; the base's 12 pinned files match. `cross_check_export` compares a merge with an existing
export (C1: the production merged checkpoint) tensor by tensor.

CPU is the default device so that the merge of the next model can run while the current one is being read on the GPU; the same
function on the same device gives the same bits on any machine. The chosen candidate's merge is held to the HF-adapter read by the
>= 99.5% parity check (parity.py), which is what binds this implementation to the production merge.
"""
from __future__ import annotations

import gc
import hashlib
import json
import os
import random
import re
import shutil
import time
from pathlib import Path

import torch
from safetensors import safe_open
from safetensors.torch import load_file, save_file

from . import common as C

MANIFEST = "merge_manifest.json"
C1_TOKENIZER_SUBDIR = "c1_tokenizer"
SKIP_BASE_FILES = {"README.md", ".gitattributes"}
# Qwen/Qwen3.5-4B @ 851bf6e8 as export_c1_merged.BASE_PINS lists it (a test compares the two): LFS sha256 for LFS files, git blob sha1
# for the others.
BASE_PINS = {
    "LICENSE": ("git_sha1", "f938136e3adacfd92be087f6e113b5d6d97f678f"),
    "chat_template.jinja": ("git_sha1", "a585dec894e63da457d9440ec6aa7caa16d20860"),
    "config.json": ("git_sha1", "557d961b205319c6a7da5f757f565b69b3967b7d"),
    "merges.txt": ("git_sha1", "a494e019ca1502219fd0128658b979e5f05ae8e8"),
    "model.safetensors-00001-of-00002.safetensors":
        ("lfs_sha256", "26a93f066e1916adb13453dae5a0c707c0fbc71299ed98779571a907b8e74c61"),
    "model.safetensors-00002-of-00002.safetensors":
        ("lfs_sha256", "cb544bd9bfae93dc59b0f22b292f5933573854a7f9b97835c67060d7d910e188"),
    "model.safetensors.index.json": ("git_sha1", "fddda6039f7c1d17260c9e923b8a72fd025d9a86"),
    "preprocessor_config.json": ("git_sha1", "2ea84a437d448ff71b08df68fdd949d5cc4ebb64"),
    "tokenizer.json": ("lfs_sha256", "5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42"),
    "tokenizer_config.json": ("git_sha1", "eda48d3e75a8e59a8479ee4ec8b37f76e711d9c1"),
    "video_preprocessor_config.json": ("git_sha1", "3ba673a5ad7d4d13f54155ecd38b2a94a6dac8fe"),
    "vocab.json": ("git_sha1", "0aa0ce0658d60ac4a5d609f4eadb0e8e43514176"),
}


F32_ROUNDED = ("linear_attn.norm.weight",)     # F32 in the base, BF16 in HF's load: written as the BF16 value in F32 (export: rounded_like_hf)
F32_KEPT = ("linear_attn.A_log",)               # F32 in the base and in HF's load: written bitwise (export: same_as_base)


class MergeFailed(SystemExit):
    pass


# ------------------------------------------------------------------ names
def ckpt_to_mem(key: str):
    """Checkpoint tensor name -> the in-memory Qwen3_5ForCausalLM name (None = vision tower / MTP: copied, never merged)."""
    if key.startswith("model.language_model."):
        return "model." + key[len("model.language_model."):]
    if key.startswith(("model.visual.", "mtp.", "visual.")):
        return None
    if key.startswith("model.") or key == "lm_head.weight":
        return key
    return None


def shard_names(d) -> list:
    d = Path(d)
    idx = d / "model.safetensors.index.json"
    if idx.exists():
        return sorted(set(json.loads(idx.read_text())["weight_map"].values()))
    return sorted(p.name for p in d.glob("*.safetensors"))


def norm_module(k: str) -> str:
    """Adapter tensor name -> in-memory module stem (export_c1_merged.formula_check's normalisation)."""
    k = k[len("base_model.model."):] if k.startswith("base_model.model.") else k
    return k.replace("model.language_model.", "model.")


def adapter_pairs(sd: dict) -> dict:
    """{weight name in memory: (A fp32, B fp32)}; any tensor that is not lora_A / lora_B (prism_x, bias, dora) is refused."""
    mods = {}
    for k, t in sd.items():
        m = re.fullmatch(r"(.*)\.lora_([AB])\.weight", norm_module(k))
        if not m:
            raise MergeFailed(f"merge: unexpected adapter tensor {k!r} (only lora_A / lora_B weights are merged)")
        mods.setdefault(m.group(1) + ".weight", {})[m.group(2)] = t.float()
    bad = [m for m, v in mods.items() if set(v) != {"A", "B"}]
    if bad:
        raise MergeFailed(f"merge: modules without both A and B: {bad[:3]}")
    return {m: (v["A"], v["B"]) for m, v in mods.items()}


def adapter_scaling(adapter_dir: Path) -> tuple:
    cfg = json.loads((Path(adapter_dir) / "adapter_config.json").read_text())
    if cfg.get("use_rslora") or cfg.get("use_dora") or cfg.get("fan_in_fan_out"):
        raise MergeFailed("merge: rslora / dora / fan_in_fan_out adapters are not C1's kind")
    if cfg.get("peft_type") not in (None, "LORA"):
        raise MergeFailed(f"merge: peft_type {cfg.get('peft_type')!r}")
    r, a = int(cfg["r"]), float(cfg["lora_alpha"])
    return a / r, r


def merged_weight(w: torch.Tensor, A: torch.Tensor, B: torch.Tensor, scale: float, dev: str = "cpu") -> torch.Tensor:
    """PEFT's merge of one linear: bf16 weight + (B @ A) * scale in fp32, rounded back to bf16."""
    delta = (B.to(dev).float() @ A.to(dev).float()) * scale
    return (w.to(dev).float() + delta).to(torch.bfloat16).cpu()


def hf_rounded(b: torch.Tensor) -> torch.Tensor:
    """A tensor the base stores in F32 but HF loads as BF16: the BF16 value, stored back as F32."""
    return b.to(torch.bfloat16).to(b.dtype)


# ------------------------------------------------------------------ base checks
def git_blob_sha1(path) -> str:
    h = hashlib.sha1()
    p = Path(path)
    h.update(b"blob %d\0" % p.stat().st_size)
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def check_base_pins(base_dir, extra_dirs=(), pins: dict = BASE_PINS) -> list:
    """Problems with the 12 pinned base files (a pinned file may live in one of extra_dirs instead of base_dir)."""
    probs = []
    for name, (kind, want) in sorted(pins.items()):
        cand = [Path(d) / name for d in (base_dir, *extra_dirs)]
        p = next((x for x in cand if x.exists()), None)
        if p is None:
            probs.append(f"{name}: missing")
            continue
        got = C.sha256_file(p) if kind == "lfs_sha256" else git_blob_sha1(p)
        if got != want:
            probs.append(f"{name}: {kind} {got[:16]} != pinned {want[:16]}")
    return probs


# ------------------------------------------------------------------ the merge
def merge_adapter(base_dir, adapter_dir, out_dir, c1_tok_dir, label: str = "", dev: str = "cpu", threads: int | None = None,
                  extra_files: dict | None = None, sample: int = 16, seed: int = 0, expect_adapter_sha: str | None = None,
                  log=print) -> dict:
    """Merge into an EMPTY out_dir; returns the manifest (also written, last). Raises MergeFailed on any failed check."""
    t0 = time.time()
    base_dir, adapter_dir, out_dir, c1_tok_dir = Path(base_dir), Path(adapter_dir), Path(out_dir), Path(c1_tok_dir)
    for p in (base_dir, adapter_dir, out_dir, c1_tok_dir):
        C.safe_path(p)
    out_dir.mkdir(parents=True, exist_ok=True)
    if any(out_dir.iterdir()):
        raise MergeFailed(f"merge: {out_dir} is not empty")
    asha = C.sha256_file(adapter_dir / "adapter_model.safetensors")
    if expect_adapter_sha and asha != expect_adapter_sha:
        raise MergeFailed(f"merge: adapter sha256 {asha[:16]} != expected {expect_adapter_sha[:16]}")
    if threads:
        torch.set_num_threads(threads)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    scale, rank = adapter_scaling(adapter_dir)
    pairs = adapter_pairs(load_file(str(adapter_dir / "adapter_model.safetensors")))
    ranks = {A.shape[0] for A, _ in pairs.values()}
    if ranks != {rank}:
        raise MergeFailed(f"merge: adapter_config r={rank} but the tensors have ranks {sorted(ranks)}")
    problems, merged_keys, rounded, copied, same = [], [], [], [], 0
    files, used, probe = {}, set(), []
    for sh in shard_names(base_dir):
        tensors = {}
        with safe_open(str(base_dir / sh), "pt") as f:
            meta = f.metadata()
            for k in f.keys():
                b = f.get_tensor(k)
                m = ckpt_to_mem(k)
                if m is None:
                    tensors[k] = b
                    copied.append(k)
                elif m in pairs:
                    if b.dtype != torch.bfloat16:
                        problems.append(f"{k}: LoRA target is {b.dtype} in the base (expected bfloat16)")
                    w = merged_weight(b, *pairs[m], scale, dev)
                    if tuple(w.shape) != tuple(b.shape):
                        problems.append(f"{k}: merged shape {tuple(w.shape)} != base {tuple(b.shape)}")
                    elif torch.equal(w, b):
                        problems.append(f"{k}: LoRA target equals the base after the merge (adapter not applied?)")
                    tensors[k] = w
                    merged_keys.append(k)
                    used.add(m)
                    probe.append((sh, k, m))
                elif b.dtype == torch.float32:
                    if k.endswith(F32_ROUNDED):
                        tensors[k] = hf_rounded(b)
                        rounded.append(k)
                    elif k.endswith(F32_KEPT):
                        tensors[k] = b
                        same += 1
                    else:
                        problems.append(f"{k}: an F32 base tensor of an unknown kind (neither rounded like HF nor kept)")
                        tensors[k] = b
                else:
                    tensors[k] = b
                    same += 1
        save_file(tensors, str(out_dir / sh), metadata=meta)
        files[sh] = {"sha256": C.sha256_file(out_dir / sh), "bytes": (out_dir / sh).stat().st_size}
        del tensors
        gc.collect()
    unused = sorted(set(pairs) - used)
    if unused:
        problems.append(f"{len(unused)} adapter modules are not base tensors (e.g. {unused[:3]})")
    # non-weight base files, extra files, c1_tokenizer
    for p in sorted(base_dir.iterdir()):
        if p.is_file() and not p.name.endswith(".safetensors") and p.name not in SKIP_BASE_FILES:
            shutil.copyfile(p, out_dir / p.name)
    for name, p in sorted((extra_files or {}).items()):
        if not (out_dir / name).exists():
            shutil.copyfile(p, out_dir / name)
    tok_files = {}
    (out_dir / C1_TOKENIZER_SUBDIR).mkdir()
    for n in C.C1_PIN_TOKENIZER:
        if (c1_tok_dir / n).exists():
            shutil.copyfile(c1_tok_dir / n, out_dir / C1_TOKENIZER_SUBDIR / n)
            tok_files[n] = C.sha256_file(c1_tok_dir / n)
    for need in ("tokenizer.json", "tokenizer_config.json", "train_meta.json"):
        if need not in tok_files:
            problems.append(f"c1_tokenizer: {need} missing")
    # re-read checks on the written files
    shapes_bad = verify_layout(out_dir, base_dir)
    problems += shapes_bad
    rng = random.Random(seed)
    sampled = rng.sample(probe, min(sample, len(probe)))
    resample_bad = 0
    for sh, k, m in sampled:
        with safe_open(str(base_dir / sh), "pt") as fb, safe_open(str(out_dir / sh), "pt") as fo:
            exp = merged_weight(fb.get_tensor(k), *pairs[m], scale, dev)
            if not torch.equal(exp, fo.get_tensor(k)):
                resample_bad += 1
                problems.append(f"{k}: the written tensor differs from a recompute of the merge")
    vis_bad = []
    for sh in shard_names(base_dir):
        with safe_open(str(base_dir / sh), "pt") as fb, safe_open(str(out_dir / sh), "pt") as fo:
            for k in fb.keys():
                if ckpt_to_mem(k) is None and not torch.equal(fb.get_tensor(k), fo.get_tensor(k)):
                    vis_bad.append(k)
    problems += [f"{k}: vision / MTP tensor differs from the base" for k in vis_bad[:5]]
    if problems:
        raise MergeFailed("merge failed: " + json.dumps(problems[:12]))
    for p in sorted(out_dir.rglob("*")):
        if p.is_file() and p.name != MANIFEST:
            rel = str(p.relative_to(out_dir))
            files.setdefault(rel, {"sha256": C.sha256_file(p), "bytes": p.stat().st_size})
    man = {"format": 1, "tool": "grid_h100.merge_direct", "label": label, "model": label or None, "base": C.BASE, "revision": C.REVISION,
           "adapter_sha256": asha, "layout": "base", "c1_tokenizer": tok_files,
           "merge": {"device": dev, "method": "W' = bf16(fp32(W) + (B_fp32 @ A_fp32) * alpha/r) per LoRA target (PEFT's merge, no PEFT)",
                     "torch": torch.__version__, "allow_tf32": False, "scaling": scale, "rank": rank, "lora_targets": len(merged_keys),
                     "f32_rounded_like_hf": len(rounded), "unchanged": same, "vision_mtp_copied": len(copied)},
           "config": json.loads((out_dir / "config.json").read_text()).get("architectures"),
           "checks": {"passed": True, "problems": [], "targets_changed": len(merged_keys), "sampled_recompute": len(sampled),
                      "sampled_mismatch": resample_bad, "vision_mtp_bitwise": len(copied)},
           "created_utc": C.utc(), "merge_s": round(time.time() - t0, 1), "files": files}
    tmp = out_dir / (MANIFEST + ".tmp")
    tmp.write_text(json.dumps(man, indent=1, default=str))
    os.replace(tmp, out_dir / MANIFEST)
    log(f"merged {label or adapter_dir.name}: {len(merged_keys)} targets, {len(rounded)} F32 rounded, {len(copied)} copied, "
        f"{man['merge_s']} s on {dev}")
    return man


def verify_layout(out_dir, base_dir) -> list:
    """Every key of every base shard is in the written shard with the base's dtype and shape (the index stays exact)."""
    bad = []
    for sh in shard_names(base_dir):
        with safe_open(str(Path(base_dir) / sh), "pt") as fb, safe_open(str(Path(out_dir) / sh), "pt") as fo:
            if set(fb.keys()) != set(fo.keys()):
                bad.append(f"{sh}: key sets differ")
                continue
            for k in fb.keys():
                a, b = fb.get_slice(k), fo.get_slice(k)
                if a.get_dtype() != b.get_dtype() or list(a.get_shape()) != list(b.get_shape()):
                    bad.append(f"{k}: dtype / shape changed")
    return bad


def check_merged_dir(mdir, adapter_sha: str) -> tuple:
    """(manifest, problems) of a merged folder written here (sglang_host.check_manifest's rules, with this adapter's sha)."""
    mdir = Path(mdir)
    p = mdir / MANIFEST
    if not p.exists():
        return None, [f"{p} missing"]
    man = json.loads(p.read_text())
    probs = []
    if man.get("adapter_sha256") != adapter_sha:
        probs.append(f"manifest adapter_sha256 {str(man.get('adapter_sha256'))[:16]} != {adapter_sha[:16]}")
    files = man.get("files") or {}
    if not any(f.endswith(".safetensors") for f in files):
        probs.append("manifest lists no .safetensors file")
    for need in (f"{C1_TOKENIZER_SUBDIR}/train_meta.json", f"{C1_TOKENIZER_SUBDIR}/tokenizer.json", "config.json"):
        if need not in files:
            probs.append(f"manifest lists no {need}")
    if not (man.get("checks") or {}).get("passed"):
        probs.append("manifest checks did not pass")
    return man, probs


def verify_files(mdir, man) -> list:
    probs = []
    for rel, meta in sorted((man.get("files") or {}).items()):
        p = Path(mdir) / rel
        if not p.exists():
            probs.append(f"{rel}: missing")
        elif C.sha256_file(p) != meta["sha256"]:
            probs.append(f"{rel}: sha256 differs from the manifest")
    return probs


def cross_check_export(mdir, export_dir, max_report: int = 5) -> dict:
    """Tensor-by-tensor comparison of a merge with another merged checkpoint of the same adapter (for C1: the production export on the
    Volume). Report only: bitwise-equal count, tensors that differ and the largest BF16 distance in ulps."""
    n = eq = 0
    diff, worst = [], 0
    for sh in shard_names(mdir):
        with safe_open(str(Path(mdir) / sh), "pt") as fa, safe_open(str(Path(export_dir) / sh), "pt") as fb:
            if set(fa.keys()) != set(fb.keys()):
                return {"compared": 0, "error": f"{sh}: key sets differ"}
            for k in fa.keys():
                a, b = fa.get_tensor(k), fb.get_tensor(k)
                n += 1
                if a.dtype == b.dtype and a.shape == b.shape and torch.equal(a, b):
                    eq += 1
                    continue
                ulp = None
                if a.dtype == b.dtype == torch.bfloat16 and a.shape == b.shape:
                    ulp = int((a.view(torch.int16).int() - b.view(torch.int16).int()).abs().max())
                    worst = max(worst, ulp)
                diff.append({"tensor": k, "dtype": [str(a.dtype), str(b.dtype)], "max_ulp": ulp})
    return {"compared": n, "bitwise_equal": eq, "n_different": len(diff), "max_ulp_bf16": worst, "different": diff[:max_report]}
