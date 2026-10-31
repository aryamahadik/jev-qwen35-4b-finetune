"""export_c1_merged: C1 (Qwen/Qwen3.5-4B @ 851bf6e8 + LoRA q35_4b_main500k, adapter sha256 507d1c29...) merged in BF16
exactly as hosting/modal_direct_host.boot_gpu merges it (decoder_io.load + merge_and_unload), written ONCE to the account
Volume as a plain checkpoint, /vol/models/q35_4b_main500k_merged, for the SGLang arms S1/S2 (hosting/sglang_host.py):
SGLang 0.5.20's Qwen3.5 LoRA path has no in_proj_a / in_proj_b, so C1 must be served pre-merged. NEW file; nothing
pinned is edited (decoder_io.py etc. come from core.image read-only).

Layouts (--layout):
  base (default)   the base snapshot's own layout, file for file: same config.json (Qwen3_5ForConditionalGeneration,
                   tie_word_embeddings, text_config.mamba_ssm_dtype float32), same shard names, keys, dtypes and
                   index, same tokenizer / processor files, vision tower and MTP layer copied byte for byte. Every
                   language-model tensor holds the merged in-memory model's value: the LoRA targets (q/k/v/o, gate/up/
                   down, out_proj, in_proj_qkv/z/a/b) are merged, and the 48 tensors the base stores in F32 (A_log,
                   linear_attn.norm.weight) keep the F32 dtype but hold the value HF's BF16 load gives them (the value
                   C1 has always been read with: the HF arms and the L4 reads cast them to BF16). This is the layout
                   SGLang 0.5.20 already served in B1a (Qwen/Qwen3.5-4B, 5 Oct).
  save_pretrained  model.save_pretrained + tokenizer.save_pretrained of the merged Qwen3_5ForCausalLM (text-only
                   qwen3_5_text config; transformers 5.17 writes the keys back as model.language_model.*; vision/MTP
                   dropped); mamba_ssm_dtype float32 is added to config.json if missing. Not yet proven on SGLang.
Both layouts also get c1_tokenizer/ = the adapter folder's tokenizer.json, tokenizer_config.json, chat_template.jinja,
train_meta.json and adapter_config.json (the HF path's own tokenizer and prompt layout, which the SGLang front end
loads), and merge_manifest.json (written last, only when every check passed).

Checks (in the container, before the folder gets its final name; any failure = no manifest, nothing published):
  adapter sha256 = C1's pin; layout/style from train_meta = (schema_branch_mark, cygnet); PRISM-X refused;
  base files = Qwen/Qwen3.5-4B @ 851bf6e8 (LFS sha256 of the shards and tokenizer.json, git blob sha1 of the rest);
  every in-memory tensor maps to exactly one checkpoint key (tied lm_head absent) and every key to one tensor;
  LoRA targets differ from the base; every other mapped tensor equals the base (or its BF16 rounding);
  re-read: every written tensor == the in-memory merged tensor, bitwise;
  a FRESH second decoder_io.load + merge_and_unload in the same container == the written tensors, bitwise (all of them);
  formula: --sample LoRA targets recomputed as W_base + (B @ A) * scaling (PEFT's merge, same device) == written;
  vision/MTP tensors == base bitwise (base layout); config fields (architecture, tie_word_embeddings, mamba_ssm_dtype,
  sizes = the in-memory model's); sha256 of every file in merge_manifest.json (sglang_host re-hashes them at boot).

Commands, run from lean/ and ONLY after the owner's GO (nothing in this file has run on Modal yet):
  0) free CPU tests:  ../.venv/bin/python -m pytest hosting/tests/test_sglang_host.py -q -k export
  1) once per account, C1's adapter on the Volume (SPEED1_DESIGN.md: mahadikarya3 has the base, not the adapter):
       bash hosting/upload_c1_adapter.sh mahadikarya3     (Volume operations only; sha256-checked; no compute bill)
  2) the export (CPU container, 4 cores / 48 GiB, ~15-25 min; ~$0.15-0.25 of free credit, worst case 40 min ~$0.4):
       MODAL_PROFILE=mahadikarya3 ../.venv/bin/modal run hosting/export_c1_merged.py
     --gpu H100! merges on an H100 instead (dev cuda, as boot_gpu does; ~$1, worst $3): the CPU merge computes the same
     fp32 delta but with a different GEMM, so a rare weight may differ by 1 BF16 ulp from the HF host's boot-time merge.
     --check-only re-verifies an existing export (sha256 of every file); --overwrite rebuilds it; --layout save_pretrained.
     Writes speed/export_c1_merged.json locally.
Cost guards: payer guard (sglang_host.payer_guard: MODAL_PROFILE = mahadikarya3 or mahadikarya2, set explicitly; only
`modal run`, never --detach), one container, 40 min hard timeout, no GPU unless --gpu, idempotent (an existing verified
export is re-checked and returned, never rebuilt without --overwrite), the Volume's HF cache is never written.
"""
from __future__ import annotations

import gc
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import time
from pathlib import Path

import modal

HERE = Path(__file__).resolve().parent  # lean/hosting locally; /root in the container
LEAN = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import modal_direct_host as core  # noqa: E402  (read-only: image, BASE, REVISION, lean_import, sha256_file, base_snapshot_complete)

APP_NAME = "od-c1-export"
BASE, REVISION = core.BASE, core.REVISION
C1_MODEL = "q35_4b_main500k"
C1_ADAPTER_SHA256 = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
MERGED_NAME = "q35_4b_main500k_merged"
MANIFEST = "merge_manifest.json"
C1_TOKENIZER_SUBDIR = "c1_tokenizer"
C1_TOKENIZER_FILES = ("tokenizer.json", "tokenizer_config.json", "train_meta.json", "chat_template.jinja",
                      "adapter_config.json")
C1_TOKENIZER_REQUIRED = ("tokenizer.json", "tokenizer_config.json", "train_meta.json")
EXPECT_LAYOUT = ("schema_branch_mark", "cygnet")
LAYOUTS = ("base", "save_pretrained")
EXPECT_ARCH = {"base": "Qwen3_5ForConditionalGeneration", "save_pretrained": "Qwen3_5ForCausalLM"}
SKIP_BASE_FILES = {"README.md", ".gitattributes"}
# Qwen/Qwen3.5-4B @ 851bf6e8 as the Hub lists it (the laptop's HF cache tree for that revision, 12 Oct): LFS sha256 for
# LFS files, git blob sha1 for the others. README.md and .gitattributes are not copied.
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
FUNCTION_TIMEOUT_S = 40 * 60
CPU_CORES, MEMORY_MB = 4.0, 49152
CPU_USD_CORE_H, MEM_USD_GIB_H, H100_USD_H = 0.0472, 0.0080, 3.95  # [E] Modal list rates
EXPECT_MIN = {"cpu": (15, 25), "gpu": (10, 15)}  # [E] minutes


class ExportFailed(SystemExit):
    """A check failed: nothing is published (the message is the checks report)."""


# ------------------------------------------------------------------ pure helpers (CPU-testable)

def ckpt_to_mem(key: str):
    """Checkpoint tensor name -> the in-memory Qwen3_5ForCausalLM state_dict name (None = not part of it: the vision
    tower and the MTP layer of the base checkpoint)."""
    if key.startswith("model.language_model."):
        return "model." + key[len("model.language_model."):]
    if key.startswith(("model.visual.", "mtp.", "visual.")):
        return None
    if key.startswith("model.") or key == "lm_head.weight":
        return key
    return None


def git_blob_sha1(path) -> str:
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def sha256_file(p) -> str:
    return core.sha256_file(p)


def check_pins(files: dict, pins: dict = BASE_PINS) -> list:
    """files {name: path}: every pinned name must be present and match its pin. Returns the problems."""
    problems = []
    for name, (kind, want) in sorted(pins.items()):
        p = files.get(name)
        if p is None or not Path(p).exists():
            problems.append(f"{name}: missing")
            continue
        got = sha256_file(p) if kind == "lfs_sha256" else git_blob_sha1(p)
        if got != want:
            problems.append(f"{name}: {kind} {got[:16]} != pinned {want[:16]}")
    return problems


def shard_names(d) -> list:
    d = Path(d)
    idx = d / "model.safetensors.index.json"
    if idx.exists():
        return sorted(set(json.loads(idx.read_text())["weight_map"].values()))
    return sorted(p.name for p in d.glob("*.safetensors"))


def lora_targets(peft_model) -> dict:
    """{in-memory weight name: LoRA scaling} of every LoRA-wrapped linear, read BEFORE merge_and_unload."""
    out = {}
    for name, mod in peft_model.named_modules():
        la = getattr(mod, "lora_A", None)
        if la is None or not hasattr(mod, "base_layer") or not len(la):
            continue
        if len(la) != 1:
            raise ExportFailed(f"{name}: {len(la)} adapters on one layer (C1 has one)")
        adapter = next(iter(la.keys()))
        n = name[len("base_model.model."):] if name.startswith("base_model.model.") else name
        out[n + ".weight"] = float(mod.scaling[adapter])
    return out


def merge_c1(base_ref, adapter_dir, dev: str = "cpu", revision=REVISION, expect_layout=EXPECT_LAYOUT, log=print):
    """modal_direct_host.boot_gpu's load + merge on `dev`: decoder_io.load (layout, style and revision from the
    adapter's train_meta.json), merge_and_unload in BF16, eval, use_cache. -> (model, tok, load_info, targets)."""
    dio = core.lean_import()
    model, tok, info = dio.load(str(base_ref), dev, adapter=str(adapter_dir), revision=revision, return_info=True)
    if info.get("prism_x"):
        raise ExportFailed("PRISM-X adapter: not a plain LoRA, refusing")
    if expect_layout is not None and (info.get("layout"), info.get("style")) != tuple(expect_layout):
        raise ExportFailed(f"adapter layout/style {(info.get('layout'), info.get('style'))} != C1's {tuple(expect_layout)}")
    targets = lora_targets(model)
    if not targets:
        raise ExportFailed("no LoRA layers found after decoder_io.load")
    model = model.merge_and_unload()
    model.eval()
    for c in (model.config, getattr(model.config, "text_config", None)):
        if c is not None:
            c.use_cache = True
    if getattr(model, "generation_config", None) is not None:
        model.generation_config.use_cache = True
    log(f"merged {len(targets)} LoRA linears on {dev} ({type(model).__name__})")
    return model, tok, info, targets


def _tied(model, sd) -> bool:
    if "lm_head.weight" not in sd or "model.embed_tokens.weight" not in sd:
        return False
    return bool(getattr(model.config, "tie_word_embeddings", False)) and \
        sd["lm_head.weight"].data_ptr() == sd["model.embed_tokens.weight"].data_ptr()


def write_base_layout(model, base_dir, out_dir, targets: dict, extra_files: dict | None = None, log=print) -> dict:
    """Rewrite the base checkpoint shard by shard: mapped keys take the merged in-memory value (in the base dtype; BF16
    -> F32 is exact), vision/MTP keys are copied, every non-weight file is copied (plus extra_files)."""
    import torch
    from safetensors import safe_open
    from safetensors.torch import save_file
    base_dir, out_dir = Path(base_dir), Path(out_dir)
    sd = model.state_dict()
    tied = _tied(model, sd)
    rep = {"shards": [], "merged": [], "rounded_like_hf": [], "copied_base": [], "same_as_base": 0, "problems": []}
    seen = set()
    for sh in shard_names(base_dir):
        tensors = {}
        with safe_open(str(base_dir / sh), "pt") as f:
            meta = f.metadata()
            for k in f.keys():
                b = f.get_tensor(k)
                m = ckpt_to_mem(k)
                if m is None:
                    tensors[k] = b
                    rep["copied_base"].append(k)
                    continue
                if m not in sd:
                    rep["problems"].append(f"{k}: no in-memory tensor {m}")
                    continue
                mem = sd[m].detach().to("cpu")
                if tuple(mem.shape) != tuple(b.shape):
                    rep["problems"].append(f"{k}: shape {tuple(mem.shape)} != base {tuple(b.shape)}")
                    continue
                t = mem.to(b.dtype).contiguous()
                same = torch.equal(t, b)
                if m in targets:
                    if same:
                        rep["problems"].append(f"{k}: LoRA target equals the base (adapter not applied?)")
                    rep["merged"].append(k)
                elif not same:
                    if b.dtype != mem.dtype and torch.equal(b.to(mem.dtype), mem):
                        rep["rounded_like_hf"].append(k)  # F32 in the base, BF16 in memory: HF's value is kept
                    else:
                        rep["problems"].append(f"{k}: not a LoRA target but differs from the base")
                else:
                    rep["same_as_base"] += 1
                tensors[k] = t
                seen.add(m)
        save_file(tensors, str(out_dir / sh), metadata=meta)
        rep["shards"].append(sh)
        del tensors
        gc.collect()
    skip = {"lm_head.weight"} if tied else set()
    unmapped = sorted(set(sd) - seen - skip)
    if unmapped:
        rep["problems"].append(f"{len(unmapped)} in-memory tensors absent from the checkpoint (e.g. {unmapped[:3]})")
    if "lm_head.weight" in sd and not tied:
        rep["problems"].append("lm_head is not tied to embed_tokens in memory (the base layout has no lm_head)")
    copied = []
    for p in sorted(base_dir.iterdir()):
        if p.is_file() and not p.name.endswith(".safetensors") and p.name not in SKIP_BASE_FILES:
            shutil.copyfile(p, out_dir / p.name)  # follows the HF cache's symlinks
            copied.append(p.name)
    for name, p in sorted((extra_files or {}).items()):
        if name not in copied:
            shutil.copyfile(p, out_dir / name)
            copied.append(name)
    rep["files_copied"] = copied
    rep["tied_lm_head"] = tied
    log(f"base layout: {len(rep['merged'])} merged, {len(rep['rounded_like_hf'])} F32 kept at HF's BF16 value, "
        f"{rep['same_as_base']} unchanged, {len(rep['copied_base'])} vision/MTP copied")
    return {**rep, "n_merged": len(rep["merged"]), "n_copied_base": len(rep["copied_base"])}


def write_save_pretrained(model, tok, out_dir, targets: dict, log=print) -> dict:
    out_dir = Path(out_dir)
    model.save_pretrained(str(out_dir), safe_serialization=True, max_shard_size="5GB")
    tok.save_pretrained(str(out_dir))
    cfg_p = out_dir / "config.json"
    c = json.loads(cfg_p.read_text())
    patched = []
    if c.get("mamba_ssm_dtype") != "float32":  # Qwen3.5 keeps the GDN state in fp32 (base text_config)
        c["mamba_ssm_dtype"] = "float32"
        patched.append("mamba_ssm_dtype")
        cfg_p.write_text(json.dumps(c, indent=2))
    log(f"save_pretrained: {len(shard_names(out_dir))} shard(s), config patched {patched}")
    return {"shards": shard_names(out_dir), "config_patched": patched, "n_merged": len(targets), "problems": []}


def copy_c1_tokenizer(adapter_dir, out_dir) -> dict:
    """c1_tokenizer/ = the adapter folder's tokenizer + prompt-layout files (what decoder_io.load reads)."""
    src, dst = Path(adapter_dir), Path(out_dir) / C1_TOKENIZER_SUBDIR
    dst.mkdir(parents=True, exist_ok=True)
    out = {}
    for n in C1_TOKENIZER_FILES:
        if (src / n).exists():
            shutil.copyfile(src / n, dst / n)
            out[n] = sha256_file(src / n)
        elif n in C1_TOKENIZER_REQUIRED:
            raise ExportFailed(f"{src / n} missing")
    return out


def verify_written(model, out_dir) -> dict:
    """Every written language-model tensor == the in-memory merged tensor, bitwise (a dtype kept from the base must
    round-trip exactly), every in-memory tensor written once (a tied lm_head excepted), and the index lists exactly the
    keys the shards hold."""
    import torch
    from safetensors import safe_open
    out_dir = Path(out_dir)
    sd = model.state_dict()
    seen, bad, n, keys = set(), [], 0, {}
    for sh in shard_names(out_dir):
        with safe_open(str(out_dir / sh), "pt") as f:
            for k in f.keys():
                keys[k] = sh
                m = ckpt_to_mem(k)
                if m is None:
                    continue
                if m not in sd:
                    bad.append(f"{k}: no in-memory tensor")
                    continue
                w, mem = f.get_tensor(k), sd[m].detach().to("cpu")
                ok = tuple(w.shape) == tuple(mem.shape) and torch.equal(w.to(mem.dtype), mem) and \
                    (w.dtype == mem.dtype or torch.equal(mem.to(w.dtype), w))
                if not ok:
                    bad.append(k)
                if m in seen:
                    bad.append(f"{k}: {m} written twice")
                seen.add(m)
                n += 1
    skip = {"lm_head.weight"} if _tied(model, sd) else set()
    missing = sorted(set(sd) - seen - skip)
    idx = out_dir / "model.safetensors.index.json"
    index_ok = True
    if idx.exists():
        index_ok = json.loads(idx.read_text())["weight_map"] == keys
    return {"tensors_checked": n, "n_mismatched": len(bad), "mismatched": bad[:20], "n_missing": len(missing),
            "missing": missing[:20], "index_matches_shards": index_ok, "ok": not bad and not missing and index_ok}


def verify_base_copies(out_dir, base_dir) -> dict:
    """Base layout: the tensors that are not C1's (vision tower, MTP) are the base's, bitwise; dtypes and shapes of
    every key equal the base's (so the copied index's total_size stays exact)."""
    import torch
    from safetensors import safe_open
    bad, n = [], 0
    for sh in shard_names(base_dir):
        with safe_open(str(Path(base_dir) / sh), "pt") as fb, safe_open(str(Path(out_dir) / sh), "pt") as fo:
            if set(fb.keys()) != set(fo.keys()):
                bad.append(f"{sh}: key sets differ")
                continue
            for k in fb.keys():
                sb, so = fb.get_slice(k), fo.get_slice(k)
                if sb.get_dtype() != so.get_dtype() or list(sb.get_shape()) != list(so.get_shape()):
                    bad.append(f"{k}: dtype/shape changed")
                if ckpt_to_mem(k) is None:
                    n += 1
                    if not torch.equal(fb.get_tensor(k), fo.get_tensor(k)):
                        bad.append(f"{k}: differs from the base")
    return {"copied_checked": n, "n_problems": len(bad), "problems": bad[:20], "ok": not bad}


def formula_check(out_dir, base_dir, adapter_dir, targets: dict, n: int = 32, seed: int = 0, dev: str = "cpu") -> dict:
    """Recompute `n` sampled LoRA targets the way PEFT merges them (W_bf16 += (B_fp32 @ A_fp32) * scaling, on `dev`)
    straight from the base and adapter files, and compare with the written tensors: bitwise, else max BF16 ulps."""
    import torch
    from safetensors import safe_open
    out_dir, base_dir = Path(out_dir), Path(base_dir)

    def keymap(d):
        km = {}
        for sh in shard_names(d):
            with safe_open(str(Path(d) / sh), "pt") as f:
                for k in f.keys():
                    m = ckpt_to_mem(k)
                    if m is not None:
                        km[m] = (sh, k)
        return km

    def get(d, sh, k):
        with safe_open(str(Path(d) / sh), "pt") as f:
            return f.get_tensor(k)

    norm = lambda k: k[len("base_model.model."):] if k.startswith("base_model.model.") else k  # noqa: E731
    with safe_open(str(Path(adapter_dir) / "adapter_model.safetensors"), "pt") as fa:
        ad = {norm(k).replace("model.language_model.", "model."): fa.get_tensor(k) for k in fa.keys()}
    wk, bk = keymap(out_dir), keymap(base_dir)
    pick = sorted(random.Random(seed).sample(sorted(targets), min(n, len(targets))))
    rows, worst = [], 0
    for m in pick:
        stem = m[: -len(".weight")]
        A, B = ad.get(stem + ".lora_A.weight"), ad.get(stem + ".lora_B.weight")
        if A is None or B is None or m not in wk or m not in bk:
            rows.append({"tensor": m, "error": "adapter or checkpoint key not found"})
            worst = max(worst, 1 << 15)
            continue
        W = get(base_dir, *bk[m]).to(torch.bfloat16).to(dev)
        exp = W.clone()
        exp += (B.to(dev).float() @ A.to(dev).float()) * targets[m]
        got = get(out_dir, *wk[m]).to(torch.bfloat16).to(dev)
        ulp = int((exp.view(torch.int16).int() - got.view(torch.int16).int()).abs().max())
        worst = max(worst, ulp)
        rows.append({"tensor": m, "bitwise": bool(torch.equal(exp, got)), "max_ulp": ulp,
                     "changed_vs_base": not torch.equal(got, W)})
    ok = bool(rows) and worst <= 1 and all(r.get("changed_vs_base") for r in rows)
    return {"n": len(rows), "bitwise_all": all(r.get("bitwise") for r in rows), "max_ulp": worst, "ok": ok,
            "rows": rows}


def check_config(out_dir, layout: str, model_cfg: dict) -> dict:
    """architectures, tie_word_embeddings, mamba_ssm_dtype float32 and the sizes of the written config.json."""
    c = json.loads((Path(out_dir) / "config.json").read_text())
    tc = c.get("text_config") or c
    got = {"architectures": c.get("architectures"), "model_type": c.get("model_type"),
           "tie_word_embeddings": c.get("tie_word_embeddings", tc.get("tie_word_embeddings")),
           "mamba_ssm_dtype": tc.get("mamba_ssm_dtype", c.get("mamba_ssm_dtype")),
           **{k: tc.get(k) for k in ("vocab_size", "hidden_size", "num_hidden_layers")}}
    problems = []
    if (got["architectures"] or [None])[0] != EXPECT_ARCH[layout]:
        problems.append(f"architectures {got['architectures']} != [{EXPECT_ARCH[layout]}]")
    if got["tie_word_embeddings"] is not True:
        problems.append(f"tie_word_embeddings {got['tie_word_embeddings']!r} (C1's lm_head is the embedding)")
    if got["mamba_ssm_dtype"] != "float32":
        problems.append(f"mamba_ssm_dtype {got['mamba_ssm_dtype']!r} != 'float32'")
    for k, v in model_cfg.items():
        if got.get(k) != v:
            problems.append(f"{k}: config {got.get(k)!r} != in-memory {v!r}")
    return {**got, "problems": problems, "ok": not problems}


def file_manifest(out_dir) -> dict:
    out_dir = Path(out_dir)
    return {str(p.relative_to(out_dir)): {"sha256": sha256_file(p), "bytes": p.stat().st_size}
            for p in sorted(out_dir.rglob("*")) if p.is_file() and p.name != MANIFEST}


def export_local(base_ref, base_dir, adapter_dir, out_dir, layout: str = "base", dev: str = "cpu", revision=REVISION,
                 fresh: bool = True, sample: int = 32, seed: int = 0, adapter_sha: str | None = C1_ADAPTER_SHA256,
                 expect_layout=EXPECT_LAYOUT, extra_files: dict | None = None, base_pins: dict | None = None,
                 log=print) -> dict:
    """The whole export into an EMPTY out_dir (the Modal function's body; CPU-testable on a tiny model). Raises
    ExportFailed (no manifest written) unless every check passes; returns the manifest."""
    import torch
    t0 = time.time()
    if layout not in LAYOUTS:
        raise ExportFailed(f"--layout must be one of {LAYOUTS}")
    out_dir, base_dir, adapter_dir = Path(out_dir), Path(base_dir), Path(adapter_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if any(out_dir.iterdir()):
        raise ExportFailed(f"{out_dir} is not empty")
    asha = sha256_file(adapter_dir / "adapter_model.safetensors")
    if adapter_sha is not None and asha != adapter_sha:
        raise ExportFailed(f"adapter sha256 {asha} != C1's pin {adapter_sha}")
    problems = []
    if base_pins:
        files = {p.name: p for p in base_dir.iterdir() if p.is_file()}
        files.update(extra_files or {})
        problems += [f"base: {x}" for x in check_pins(files, base_pins)]
        if problems:
            raise ExportFailed(json.dumps({"problems": problems}))
    model, tok, info, targets = merge_c1(base_ref, adapter_dir, dev, revision, expect_layout, log)
    sd = model.state_dict()
    model_cfg = {k: getattr(model.config, k, None) for k in ("vocab_size", "hidden_size", "num_hidden_layers")}
    mem = {"class": type(model).__name__, "dtype": str(next(model.parameters()).dtype),
           "tensors": len(sd), "params": sum(p.numel() for p in model.parameters()), "config": model_cfg}
    del sd
    if layout == "base":
        wr = write_base_layout(model, base_dir, out_dir, targets, extra_files, log)
    else:
        wr = write_save_pretrained(model, tok, out_dir, targets, log)
    problems += wr["problems"]
    tokfiles = copy_c1_tokenizer(adapter_dir, out_dir)
    v1 = verify_written(model, out_dir)
    log(f"verify vs in-memory merge: {json.dumps({k: v1[k] for k in ('tensors_checked', 'n_mismatched', 'n_missing')})}")
    del model, tok
    gc.collect()
    if dev == "cuda":
        torch.cuda.empty_cache()
    v2 = None
    if fresh:  # a second, independent load + merge must give the same bits
        m2, _, _, t2 = merge_c1(base_ref, adapter_dir, dev, revision, expect_layout, log)
        v2 = verify_written(m2, out_dir)
        v2["same_targets"] = sorted(t2) == sorted(targets)
        log(f"verify vs fresh merge: {json.dumps({k: v2[k] for k in ('tensors_checked', 'n_mismatched', 'n_missing')})}")
        del m2
        gc.collect()
        if dev == "cuda":
            torch.cuda.empty_cache()
    fc = formula_check(out_dir, base_dir, adapter_dir, targets, sample, seed, dev)
    bc = verify_base_copies(out_dir, base_dir) if layout == "base" else None
    cfg = check_config(out_dir, layout, model_cfg)
    if not v1["ok"]:
        problems.append(f"written != in-memory merge: {v1['n_mismatched']} mismatched, {v1['n_missing']} missing")
    if v2 is not None and not (v2["ok"] and v2["same_targets"]):
        problems.append(f"written != fresh merge: {v2['n_mismatched']} mismatched, {v2['n_missing']} missing")
    if not fc["ok"]:
        problems.append(f"formula check: max {fc['max_ulp']} BF16 ulp or an unchanged target")
    if bc is not None and not bc["ok"]:
        problems += [f"base copies: {x}" for x in bc["problems"]]
    problems += [f"config: {x}" for x in cfg["problems"]]
    checks = {"passed": not problems, "problems": problems, "write": {k: v for k, v in wr.items()
                                                                       if k not in ("merged", "copied_base")},
              "verify_in_memory": v1, "verify_fresh_merge": v2, "formula": fc, "base_copies": bc, "config": cfg}
    if problems:
        raise ExportFailed(json.dumps(checks, default=str)[:20000])
    import peft
    import transformers
    man = {"format": 1, "model": C1_MODEL, "base": BASE if revision else str(base_ref), "revision": revision,
           "adapter_sha256": asha, "layout": layout, "c1_tokenizer": tokfiles,
           "merge": {"device": dev, "method": "decoder_io.load + merge_and_unload (= modal_direct_host.boot_gpu)",
                     "torch": torch.__version__, "transformers": transformers.__version__, "peft": peft.__version__,
                     "lora_targets": len(targets), "load_info": {k: info.get(k) for k in
                                                                ("layout", "style", "revision", "prism_x",
                                                                 "chat_template_sha")}, "in_memory": mem},
           "config": {k: cfg[k] for k in ("architectures", "model_type", "tie_word_embeddings", "mamba_ssm_dtype",
                                          "vocab_size", "hidden_size", "num_hidden_layers")},
           "checks": checks, "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "export_s": round(time.time() - t0, 1)}
    man["files"] = file_manifest(out_dir)
    tmp = out_dir / (MANIFEST + ".tmp")
    tmp.write_text(json.dumps(man, indent=1, default=str))
    os.replace(tmp, out_dir / MANIFEST)
    log(f"export OK in {man['export_s']} s: {len(man['files'])} files")
    return man


def verify_manifest_files(d, man) -> list:
    problems = []
    for rel, meta in sorted((man.get("files") or {}).items()):
        p = Path(d) / rel
        if not p.exists():
            problems.append(f"{rel}: missing")
        elif sha256_file(p) != meta["sha256"]:
            problems.append(f"{rel}: sha256 differs")
    return problems


def cost_estimate(gpu: str = "") -> dict:
    rate = CPU_CORES * CPU_USD_CORE_H + MEMORY_MB / 1024 * MEM_USD_GIB_H + (H100_USD_H if gpu else 0.0)
    lo, hi = EXPECT_MIN["gpu" if gpu else "cpu"]
    return {"rate_usd_h": round(rate, 3), "expected_usd": [round(lo / 60 * rate, 2), round(hi / 60 * rate, 2)],
            "worst_usd": round(FUNCTION_TIMEOUT_S / 3600 * rate, 2), "note": "[E] Modal list rates, no region pin"}


# ------------------------------------------------------------------ Modal

if modal.is_local():
    from sglang_host import payer_guard  # noqa: E402  (the same guard as the SGLang host; checked on import there too)
    if MERGED_NAME != __import__("sglang_host").MERGED_NAME or C1_ADAPTER_SHA256 != __import__("sglang_host").C1_ADAPTER_SHA256:
        raise SystemExit("export_c1_merged and sglang_host disagree on the merged name or the adapter pin")

image = core.image.add_local_file(HERE / "modal_direct_host.py", "/root/modal_direct_host.py")  # imported as core
app = modal.App(APP_NAME)
vol = modal.Volume.from_name("opendecide")  # writes only /vol/models/q35_4b_main500k_merged(.partial)


def _base_sources(log=print):
    """The base snapshot the merge reads, as boot_gpu picks it (/vol/hf offline, else a download to /tmp/hf; the
    Volume's HF cache is never written), plus any pinned non-weight file it lacks (fetched in a subprocess so this
    process's huggingface_hub stays offline)."""
    snap_rel = Path("hub") / ("models--" + BASE.replace("/", "--")) / "snapshots" / REVISION
    if core.base_snapshot_complete("/vol/hf"):
        os.environ["HF_HUB_OFFLINE"] = "1"
        snap, source = Path("/vol/hf") / snap_rel, "/vol/hf snapshot (offline)"
    else:
        env = {**os.environ, "HF_HOME": "/tmp/hf", "HF_HUB_OFFLINE": "0"}
        subprocess.run([sys.executable, "-c", f"from huggingface_hub import snapshot_download; "
                        f"snapshot_download({BASE!r}, revision={REVISION!r})"], env=env, check=True)
        os.environ.update(HF_HOME="/tmp/hf", HF_HUB_OFFLINE="1")
        snap, source = Path("/tmp/hf") / snap_rel, "downloaded to /tmp/hf"
    have = {p.name for p in snap.iterdir() if p.is_file()}
    missing = [n for n in BASE_PINS if n not in have]
    extra = {}
    if missing:
        env = {**os.environ, "HF_HOME": "/tmp/hf_meta", "HF_HUB_OFFLINE": "0"}
        code = ("import json, sys; from huggingface_hub import hf_hub_download; "
                f"print(json.dumps({{n: hf_hub_download({BASE!r}, n, revision={REVISION!r}) for n in {missing!r}}}))")
        r = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, check=True)
        extra = {n: Path(p) for n, p in json.loads(r.stdout.strip().splitlines()[-1]).items()}
        log(f"fetched {sorted(extra)} (absent from the {source})")
    return snap, extra, source


@app.function(image=image, cpu=CPU_CORES, memory=MEMORY_MB, volumes={"/vol": vol}, timeout=FUNCTION_TIMEOUT_S,
              max_containers=1)
def export(layout: str = "base", overwrite: bool = False, dev: str = "cpu", fresh: bool = True, sample: int = 32,
           check_only: bool = False) -> dict:
    t0 = time.time()
    models = Path("/vol/models")
    final, partial = models / MERGED_NAME, models / (MERGED_NAME + ".partial")
    if final.exists() and (check_only or not overwrite):
        if not (final / MANIFEST).exists():
            raise SystemExit(f"{final} exists without {MANIFEST}: refusing (--overwrite rebuilds it)")
        man = json.loads((final / MANIFEST).read_text())
        probs = verify_manifest_files(final, man)
        return {"status": "exists", "verified": not probs, "problems": probs, "manifest": man,
                "wall_s": round(time.time() - t0, 1)}
    if check_only:
        return {"status": "absent", "wall_s": round(time.time() - t0, 1)}
    adapter = models / C1_MODEL
    if not (adapter / "adapter_model.safetensors").exists():
        raise SystemExit(f"{adapter} missing on this account's Volume: upload C1's adapter first (docstring step 1)")
    snap, extra, source = _base_sources()
    if partial.exists():
        shutil.rmtree(partial)
    try:
        man = export_local(BASE, snap, adapter, partial, layout=layout, dev=dev, revision=REVISION, fresh=fresh,
                           sample=sample, extra_files=extra, base_pins=BASE_PINS)
    except BaseException:
        shutil.rmtree(partial, ignore_errors=True)
        vol.commit()
        raise
    if final.exists():  # --overwrite
        shutil.rmtree(final)
    try:
        os.rename(partial, final)
    except OSError:  # a Volume that cannot rename directories: copy, then drop the partial folder
        shutil.copytree(partial, final)
        shutil.rmtree(partial)
        probs = verify_manifest_files(final, man)
        if probs:
            raise SystemExit(f"copy to {final} differs from the manifest: {probs}")
    vol.commit()
    return {"status": "exported", "base_source": source, "manifest": man, "wall_s": round(time.time() - t0, 1)}


@app.local_entrypoint()
def main(layout: str = "base", gpu: str = "", overwrite: bool = False, fresh: bool = True, sample: int = 32,
         check_only: bool = False):
    """Export C1 merged to this account's Volume (or --check-only an existing export); writes speed/export_c1_merged.json."""
    prof = payer_guard()
    if layout not in LAYOUTS:
        raise SystemExit(f"--layout must be one of {LAYOUTS}")
    if gpu and gpu != "H100!":
        raise SystemExit("--gpu: only H100! (the HF host's GPU; the merge must use its GEMM)")
    est = cost_estimate(gpu)
    print(f"payer {prof}; {'GPU ' + gpu if gpu else 'CPU'} export; cost estimate {json.dumps(est)}", flush=True)
    fn = export.with_options(gpu=gpu) if gpu else export
    t0 = time.time()
    res = fn.remote(layout=layout, overwrite=overwrite, dev="cuda" if gpu else "cpu", fresh=fresh, sample=sample,
                    check_only=check_only)
    out = LEAN / "speed" / "export_c1_merged.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"profile": prof, "result": res, "cost_estimate": est,
                               "wall_min": round((time.time() - t0) / 60, 1)}, indent=1, default=str))
    man = res.get("manifest") or {}
    print(json.dumps({"status": res.get("status"), "verified": res.get("verified"), "layout": man.get("layout"),
                      "files": len(man.get("files") or {}), "checks_passed": (man.get("checks") or {}).get("passed"),
                      "wall_s": res.get("wall_s")}, indent=1))
    print(f"wrote {out}")
