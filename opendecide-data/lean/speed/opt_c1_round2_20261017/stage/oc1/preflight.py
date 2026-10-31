"""oc1.preflight: what the CPU-only Modal preflight inspects inside the (pinned) SGLang image and on the Volumes.

Everything here is plain Python that runs in the container's image python (stdlib + whatever the SGLang image has);
every probe is wrapped so that one failure never hides the others. No GPU, no model load, no writes except /tmp.

  sglang_env()          sglang / torch / transformers versions, python
  launch_help()         `python -m sglang.launch_server --help` text and the parsed flag table (name -> choices/default)
  grep_source(...)      file:line matches of regexes in the installed sglang package (capability evidence)
  score_api_schema()    the /v1/score request/response classes and score_request code (first lines) as installed
  check_volume_c1(...)  adapter sha256 vs C1's pin, base snapshot files vs the pinned shas, merged checkpoint status
  hf_models(...)        Hub metadata (licence, size, files) of the TTS / ASR repos the voice phase wants
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


def _run(cmd, timeout=300, env=None):
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env)
        return {"rc": r.returncode, "out": r.stdout, "err": r.stderr[-3000:], "s": round(time.time() - t0, 1)}
    except Exception as e:  # noqa: BLE001
        return {"rc": -1, "out": "", "err": f"{type(e).__name__}: {e}", "s": round(time.time() - t0, 1)}


def sglang_env(python: str = sys.executable) -> dict:
    code = ("import json,sys,importlib\n"
            "o={'python':sys.version.split()[0]}\n"
            "for m in ('sglang','torch','transformers','tokenizers','flashinfer','sgl_kernel','triton','PIL','httpx','aiohttp',"
            "'huggingface_hub','numpy','safetensors','compressed_tensors','llmcompressor','modelopt'):\n"
            "    try:\n"
            "        mod=importlib.import_module(m); o[m]=getattr(mod,'__version__','?')\n"
            "    except Exception as e: o[m]='MISSING '+type(e).__name__\n"
            "try:\n"
            "    import sglang,os; o['sglang_dir']=os.path.dirname(sglang.__file__)\n"
            "except Exception: pass\n"
            "print(json.dumps(o))\n")
    r = _run([python, "-c", code], timeout=600)
    try:
        return json.loads(r["out"].strip().splitlines()[-1])
    except Exception:  # noqa: BLE001
        return {"error": r["err"] or r["out"][-500:]}


FLAG_RE = re.compile(r"^\s{0,4}(--[a-z0-9][a-z0-9\-]*)(?:[ ,]+(.*))?$")


def parse_help(text: str) -> dict:
    """argparse --help text -> {flag: {"meta": rest of the first line, "doc": following lines (<=400 chars)}}."""
    flags, cur = {}, None
    for line in text.splitlines():
        m = FLAG_RE.match(line)
        if m and line.lstrip().startswith("--"):
            cur = m.group(1)
            flags[cur] = {"meta": (m.group(2) or "").strip(), "doc": ""}
            continue
        # argparse prints "-h, --help" style and wraps help text on following lines
        if cur and line.startswith("   ") and len(flags[cur]["doc"]) < 400:
            flags[cur]["doc"] += " " + line.strip()
    for v in flags.values():
        v["doc"] = v["doc"].strip()[:400]
    return flags


def launch_help(python: str = sys.executable, timeout: int = 600) -> dict:
    r = _run([python, "-m", "sglang.launch_server", "--help"], timeout=timeout,
             env={**os.environ, "HF_HUB_OFFLINE": "1"})
    text = r["out"] or r["err"]
    flags = parse_help(text)
    return {"rc": r["rc"], "s": r["s"], "n_chars": len(text), "n_flags": len(flags), "flags": flags,
            "help_head": text[:600]}


def grep_source(root: str, patterns: dict, max_hits: int = 12, exts=(".py",), max_files: int = 4000) -> dict:
    """patterns {label: regex}: up to max_hits 'relpath:line: text' hits per label under root."""
    out = {k: [] for k in patterns}
    rx = {k: re.compile(v) for k, v in patterns.items()}
    n = 0
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ("__pycache__", "tests", "test", "benchmark", "benchmarks")]
        for f in fn:
            if not f.endswith(exts):
                continue
            n += 1
            if n > max_files:
                return {"truncated": True, "hits": out}
            p = os.path.join(dp, f)
            try:
                with open(p, errors="replace") as fh:
                    for i, line in enumerate(fh, 1):
                        for k, r in rx.items():
                            if len(out[k]) < max_hits and r.search(line):
                                out[k].append(f"{os.path.relpath(p, root)}:{i}: {line.strip()[:200]}")
            except OSError:
                pass
    return {"truncated": False, "hits": out}


SOURCE_PATTERNS = {
    "unified_radix": r"UNIFIED_RADIX|unified_radix|UnifiedRadix",
    "env_vit_graph": r"VIT_ENABLE_CUDA_GRAPH|ENCODER_EMBEDDING_CACHE|MM_.*CACHE",
    "piecewise_flag": r"piecewise[-_]cuda[-_]graph|breakable|cuda_graph_backend_prefill|disable_prefill_cuda_graph",
    "chunked_prefill_hybrid": r"chunked_prefill_size.*(mamba|hybrid|linear)|(mamba|hybrid|linear).*chunked_prefill_size",
    "mamba_strategy": r"mamba_radix_cache_strategy|mamba_scheduler_strategy",
    "score_label_ids": r"label_token_ids",
    "apply_softmax": r"apply_softmax",
    "quant_methods": r"BASE_QUANTIZATION_METHODS|QUANTIZATION_METHODS\s*=|\"w8a8_int8\"|\"compressed-tensors\"|\"modelopt",
    "fp8_ignored": r"ignored_layers|exclude_modules|ignore_list|modules_to_not_convert",
    "qwen35_linear_quant": r"in_proj_(a|b|qkv|z|ba)\b.*(quant|Linear)|(quant|Linear).*in_proj_(a|b|qkv|z|ba)\b",
    "return_prompt_ids": r"return_prompt_token_ids|prefill_only|is_prefill_only",
    "mm_process_config": r"mm_process_config|max_pixels|min_pixels",
    "enable_mis": r"enable_mis|MIS_DELIMITER",
}


def read_snippets(root: str, rels: dict) -> dict:
    """rels {label: (relpath, start_line, n_lines)} -> text slices (empty string when the file is absent)."""
    out = {}
    for label, (rel, start, n) in rels.items():
        p = Path(root) / rel
        try:
            lines = p.read_text(errors="replace").splitlines()
            out[label] = "\n".join(lines[start - 1:start - 1 + n])
        except OSError:
            out[label] = ""
    return out


def find_def(root: str, rel: str, names, max_lines: int = 140) -> dict:
    """First 'class X' / 'def X' block (indent-based) of each name in root/rel."""
    out = {}
    try:
        lines = (Path(root) / rel).read_text(errors="replace").splitlines()
    except OSError:
        return {n: "" for n in names}
    for name in names:
        rx = re.compile(rf"^(\s*)(class|def|async def)\s+{re.escape(name)}\b")
        for i, line in enumerate(lines):
            m = rx.match(line)
            if m:
                ind = len(m.group(1))
                j = i + 1
                while j < len(lines) and j - i < max_lines and (not lines[j].strip() or len(lines[j]) - len(lines[j].lstrip()) > ind):
                    j += 1
                out[name] = "\n".join(lines[i:j])
                break
        else:
            out[name] = ""
    return out


def sha256_file(p, chunk=1 << 22) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def check_volume_c1(old_root: str, new_root: str, base: str, revision: str, adapter_sha: str, base_pins: dict,
                    merged_name: str, hash_shards: bool = True) -> dict:
    """Read-only checks on the two Volumes (old = jaypatil-duke's `opendecide`, new = this task's Volume)."""
    res = {}
    ad = Path(old_root) / "models" / "q35_4b_main500k"
    res["adapter_dir_files"] = sorted(p.name for p in ad.iterdir()) if ad.exists() else None
    f = ad / "adapter_model.safetensors"
    if f.exists():
        got = sha256_file(f)
        res["adapter_sha256"] = {"got": got, "want": adapter_sha, "match": got == adapter_sha, "bytes": f.stat().st_size}
    else:
        res["adapter_sha256"] = {"missing": True}
    snap = Path(old_root) / "hf" / "hub" / ("models--" + base.replace("/", "--")) / "snapshots" / revision
    res["base_snapshot"] = {"dir_exists": snap.exists()}
    if snap.exists():
        names = sorted(p.name for p in snap.iterdir())
        res["base_snapshot"]["files"] = names
        miss = [n for n in base_pins if n not in names]
        res["base_snapshot"]["missing_pinned"] = miss
        sh = {}
        for name, (kind, want) in sorted(base_pins.items()):
            p = snap / name
            if not p.exists():
                continue
            if kind == "lfs_sha256":
                if hash_shards or p.stat().st_size < (1 << 28):
                    got = sha256_file(p)
                    sh[name] = {"got": got[:16], "want": want[:16], "match": got == want, "bytes": p.stat().st_size}
                else:
                    sh[name] = {"skipped": True, "bytes": p.stat().st_size}
            else:
                data = p.read_bytes()
                got = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
                sh[name] = {"got": got[:16], "want": want[:16], "match": got == want}
        res["base_snapshot"]["pins"] = sh
        res["base_snapshot"]["all_match"] = bool(sh) and all(v.get("match") for v in sh.values() if "match" in v)
    mg = Path(new_root) / "models" / merged_name
    res["merged"] = {"dir_exists": mg.exists()}
    if mg.exists() and (mg / "merge_manifest.json").exists():
        man = json.loads((mg / "merge_manifest.json").read_text())
        probs = []
        for rel, meta in sorted((man.get("files") or {}).items()):
            p = mg / rel
            if not p.exists():
                probs.append(f"{rel}: missing")
            elif p.stat().st_size != meta["bytes"] or (hash_shards and sha256_file(p) != meta["sha256"]):
                probs.append(f"{rel}: differs")
        res["merged"].update({"manifest_adapter_ok": man.get("adapter_sha256") == adapter_sha, "n_files": len(man.get("files") or {}),
                              "problems": probs[:10], "verified": not probs})
    return res


HF_REPOS = {
    "nemotron_speech": ["nvidia/nemotron-speech-streaming-en-0.6b"],
    "parakeet_v3": ["nvidia/parakeet-tdt-0.6b-v3"],
    "kokoro": ["hexgrad/Kokoro-82M"],
    "silero": [],
}


def hf_models(repos: dict = HF_REPOS, search_terms=("nemotron speech", "nemotron-speech", "cache-aware streaming")) -> dict:
    out = {}
    try:
        from huggingface_hub import HfApi
        api = HfApi()
    except Exception as e:  # noqa: BLE001
        return {"error": f"{type(e).__name__}: {e}"}
    for label, ids in repos.items():
        for rid in ids:
            try:
                mi = api.model_info(rid, files_metadata=True)
                sibs = [(s.rfilename, getattr(s, "size", None)) for s in (mi.siblings or [])]
                out[rid] = {"license": getattr(mi.card_data, "license", None) if mi.card_data else None,
                            "tags": (mi.tags or [])[:25], "sha": mi.sha, "downloads": getattr(mi, "downloads", None),
                            "files": sibs[:40], "total_bytes": sum(s or 0 for _, s in sibs),
                            "library": getattr(mi, "library_name", None), "gated": getattr(mi, "gated", None)}
            except Exception as e:  # noqa: BLE001
                out[rid] = {"error": f"{type(e).__name__}: {str(e)[:200]}"}
    found = {}
    for term in search_terms:
        try:
            found[term] = [m.id for m in api.list_models(search=term, limit=15)]
        except Exception as e:  # noqa: BLE001
            found[term] = [f"error {type(e).__name__}"]
    out["_search"] = found
    return out


def model_card_head(repo: str, n_chars: int = 6000) -> str:
    try:
        from huggingface_hub import hf_hub_download
        p = hf_hub_download(repo, "README.md")
        return Path(p).read_text(errors="replace")[:n_chars]
    except Exception as e:  # noqa: BLE001
        return f"error {type(e).__name__}: {str(e)[:200]}"


def inspect_sglang(root: str, spec: list, max_chars: int = 12000) -> dict:
    """spec items: {"label", "rel", "start", "n"} (a line slice), {"label", "ls": rel} (directory listing) or
    {"label", "grep": regex, "under": rel, "context": k} (matches with k lines of context, max 8 per file)."""
    out = {}
    for it in spec:
        lab = it["label"]
        try:
            if "ls" in it:
                p = Path(root) / it["ls"]
                out[lab] = sorted(x.name for x in p.iterdir())[:200]
            elif "grep" in it:
                rx, k, hits = re.compile(it["grep"]), int(it.get("context", 2)), []
                base = Path(root) / it.get("under", "")
                files = [base] if base.is_file() else [x for x in base.rglob("*.py")]
                for f in files:
                    try:
                        lines = f.read_text(errors="replace").splitlines()
                    except OSError:
                        continue
                    n = 0
                    for i, line in enumerate(lines):
                        if rx.search(line):
                            n += 1
                            if n > 8:
                                break
                            hits.append(f"--- {f.relative_to(root)}:{i + 1}\n" + "\n".join(lines[max(0, i - k):i + k + 1]))
                out[lab] = "\n".join(hits)[:max_chars]
            else:
                lines = (Path(root) / it["rel"]).read_text(errors="replace").splitlines()
                s = int(it.get("start", 1))
                out[lab] = "\n".join(f"{s + j}: {l}" for j, l in enumerate(lines[s - 1:s - 1 + int(it.get("n", 80))]))[:max_chars]
        except Exception as e:  # noqa: BLE001
            out[lab] = f"error {type(e).__name__}: {e}"
    return out
