"""Run an OpenDecide adapter on the JevBench v1.5.4 PUBLIC items through the official harness Runner (unofficial run).

  # on the L4 VM (see README.md): one model per call, serial, one decision per request
  ~/od/bin/python run_v154.py --model ~/lean/models/q35_4b_pxE --base Qwen/Qwen3.5-4B \
      --revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
  # CPU smoke tests (no GPU, no weights)
  python3 run_v154.py --model <adapter dir> --base Qwen/Qwen3.5-4B --dry-run --limit 5     # prompts + checks only
  python3 run_v154.py --model <adapter dir> --base Qwen/Qwen3.5-4B --fake-model --limit 5  # tiny random model on CPU

The model is loaded with decoder_io.load(base, adapter=..., revision=...), so the prompt layout, style and PRISM-X
control plane come from the adapter's train_meta.json / prism_x.json. The adapter code is jevbench_od.OpenDecideAdapter
(fmt follows decoder_io.STYLE); the JevBench harness (Runner, Ledger, DecisionResult, tasks) is the one in the v1.5.4
checkout, which is byte-identical to v1.4.2. Writes <out>/results.jsonl, manifest.json, ledger.jsonl and raw/.
Nothing under the lean folder is written. By default it refuses to start when another process is using the GPU
(a training run): pass --allow-shared-gpu only when you know it is safe.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
BENCH = HERE.parent


def sha256(path):
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except OSError:
        return None


def default_lean():
    env = os.environ.get("V154_LEAN")
    if env:
        return env
    home = Path.home() / "lean"
    return str(home if (home / "decoder_io.py").exists() else BENCH.parent / "opendecide-data/lean")


def gpu_users():
    try:
        out = subprocess.run(["nvidia-smi", "--query-compute-apps=pid,process_name,used_memory", "--format=csv,noheader"],
                             capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:
        return None
    return out or ""


def git_head(path):
    try:
        return subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True,
                              timeout=10).stdout.strip() or None
    except Exception:
        return None


def pick_spread(tasks, n):
    """n tasks for a smoke run: the first task of each question type, then evenly spaced ones."""
    if n >= len(tasks):
        return tasks
    chosen, seen = [], set()
    for t in tasks:
        if t.question["type"] not in seen:
            seen.add(t.question["type"])
            chosen.append(t)
    ids = {t.id for t in chosen}
    rest = [t for t in tasks if t.id not in ids]
    k = max(0, n - len(chosen))
    ids |= {rest[int(i * len(rest) / k)].id for i in range(k)}
    return [t for t in tasks if t.id in ids][:n]


def build_row(jo, decoder_io, task, tok, fmt):
    if fmt == "od":
        row, _ = jo.to_row(task)
        return row
    return jo.letter_row(task, tok, fmt)[0]


def check_prompts(jo, decoder_io, tasks, tok, fmt, prism_x_on):
    """Pre-flight on every task, before any GPU time: the message follows decoder_io.LAYOUT (an old jevbench_od.py
    hard-codes text_first) and, for PRISM-X, the token-role spans can be found in the exact chat text."""
    if prism_x_on:
        import prism_x
    stats = []
    for t in tasks:
        row = build_row(jo, decoder_io, t, tok, fmt)
        text = row.get("_prompt")
        if fmt == "cygnet":
            body = {k: v for k, v in row.items() if k != "_prompt"}
            if decoder_io.cygnet_msg(body) not in text:
                raise SystemExit(f"{t.id}: the adapter's prompt does not follow decoder_io.LAYOUT={decoder_io.LAYOUT!r}; "
                                 "jevbench_od.py is an old copy (use --adapter-code with the current one)")
            if prism_x_on:
                prism_x.row_char_spans(body, None, text)  # raises if PRISM-X could not place the token roles
        n = len(tok(text if text is not None else "", add_special_tokens=False)["input_ids"]) if text else None
        stats.append({"task_id": t.id, "type": t.question["type"], "n_options": len(t.labels), "n_tokens": n,
                      "prompt_sha256": hashlib.sha256(text.encode()).hexdigest() if text else None})
    return stats


def tiny_model(tok):
    """A random 1-layer Qwen3 with the real vocabulary: exercises the full readout path on CPU, answers are noise."""
    import torch
    from transformers import Qwen3Config, Qwen3ForCausalLM
    torch.manual_seed(0)
    cfg = Qwen3Config(vocab_size=len(tok), hidden_size=32, intermediate_size=64, num_hidden_layers=1,
                      num_attention_heads=2, num_key_value_heads=1, head_dim=16, max_position_embeddings=32768,
                      tie_word_embeddings=False)
    return Qwen3ForCausalLM(cfg).eval()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True, help="adapter dir (train_meta.json, adapter weights, prism_x.* if any)")
    ap.add_argument("--base", required=True, help="base model id, e.g. Qwen/Qwen3.5-4B")
    ap.add_argument("--revision", default=None, help="exact Hugging Face commit of the base")
    ap.add_argument("--name", default=None, help="run name (default: adapter dir name); output runs/v154_<name>")
    ap.add_argument("--lean", default=default_lean(), help="lean code dir (decoder_io.py, prism_x.py)")
    ap.add_argument("--adapter-code", default=str(HERE / "lean_snapshot"),
                    help="dir holding the jevbench_od.py to use (default: the snapshot next to this script)")
    ap.add_argument("--jevbench", default=str(BENCH / "jevbench_v154"), help="JevBench checkout (harness + public items)")
    ap.add_argument("--out", default=None, help="output dir (default: <bench>/runs/v154_<name>)")
    ap.add_argument("--tiers", default="easy,original,hard", help="public item files to run")
    ap.add_argument("--extra-items", default=None, help="extra canonical jsonl (e.g. v1.5 items if they are published)")
    ap.add_argument("--limit", type=int, default=0, help="run only N tasks spread over types (smoke tests)")
    ap.add_argument("--temps", default="1.0,1.0", help="noul,choice readout temperatures (1.0 = as trained)")
    ap.add_argument("--graphs", action="store_true", help="CUDA graphs (not for PRISM-X; memory-heavy on a 23 GB L4)")
    ap.add_argument("--warmup-tokens", type=int, default=8192)
    ap.add_argument("--dry-run", action="store_true", help="CPU: build and check every prompt, count tokens; no model")
    ap.add_argument("--fake-model", action="store_true", help="CPU: tiny random model through the real adapter+Runner")
    ap.add_argument("--allow-shared-gpu", action="store_true", help="start even if another process uses the GPU")
    ap.add_argument("--overwrite", action="store_true", help="move an existing output dir aside instead of stopping")
    a = ap.parse_args()

    model_dir = Path(a.model).expanduser().resolve()
    name = a.name or model_dir.name
    lean, jb, code = (Path(p).expanduser().resolve() for p in (a.lean, a.jevbench, a.adapter_code))
    out = Path(a.out).expanduser().resolve() if a.out else BENCH / "runs" / f"v154_{name}{'_dry' if a.dry_run else ''}" \
        f"{'_fake' if a.fake_model else ''}"
    if out.is_relative_to(lean) or out.is_relative_to(jb):
        raise SystemExit(f"output {out} must be outside the lean folder and the JevBench checkout")
    if not (jb / "jevbench/runner.py").exists():
        raise SystemExit(f"{jb}: not a JevBench checkout (git clone https://github.com/fstandhartinger/jevbench.git)")
    if out.exists():
        if not a.overwrite:
            raise SystemExit(f"{out} exists; pass --overwrite to move it aside")
        out.rename(out.with_name(out.name + time.strftime(".bak-%Y%m%d-%H%M%S")))
    mode = "dry-run" if a.dry_run else "fake-model" if a.fake_model else "gpu"
    users = None
    if mode == "gpu":
        users = gpu_users()
        if users is None:
            raise SystemExit("nvidia-smi not found: no GPU here (use --dry-run or --fake-model for CPU checks)")
        if users and not a.allow_shared_gpu:
            raise SystemExit("the GPU is in use (a training run?), refusing to start so it is not disturbed:\n" + users)

    # code paths: jevbench_od from --adapter-code (if it has one), decoder_io/prism_x from lean, jevbench from the checkout
    for p in (lean, code) if (code / "jevbench_od.py").exists() else (lean,):
        sys.path.insert(0, str(p))
    sys.path.insert(0, str(jb))
    import torch
    import decoder_io
    import jevbench_od as jo
    from jevbench.budget import Ledger
    from jevbench.runner import Runner
    from jevbench.tasks import dataset_hash, load_jsonl

    tasks = [t for tier in a.tiers.split(",") for t in load_jsonl(str(jb / "datasets/public" / f"{tier}.jsonl"))]
    if a.extra_items:
        tasks += load_jsonl(a.extra_items)
    all_hash = dataset_hash(tasks)
    if a.limit:
        tasks = pick_spread(tasks, a.limit)
    tn, tc = (float(x) for x in a.temps.split(","))
    temps = {"noul": tn, "choice": tc}
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    t0 = time.time()
    prism_json = (model_dir / "prism_x.json").exists()

    if mode == "gpu":
        model, tok, info = decoder_io.load(a.base, "cuda", adapter=str(model_dir), revision=a.revision, return_info=True)
        model = model.merge_and_unload()  # as od_gcp predict and the Modal JevBench runner; PRISM-X hooks survive it
        model.eval()
        for cfg in (model.config, getattr(model.config, "text_config", None)):
            if cfg is not None:
                cfg.use_cache = True
        model.generation_config.use_cache = True
        dev = "cuda"
    else:
        from transformers import AutoTokenizer
        info = decoder_io.resolve_prompt([str(model_dir)], a.base, None, None, a.revision)
        decoder_io.LAYOUT = info["layout"] or decoder_io.LAYOUT
        decoder_io.STYLE = info["style"] or decoder_io.STYLE
        if prism_json:
            px = json.loads((model_dir / "prism_x.json").read_text())
            if (px["layout"], px["style"]) != (decoder_io.LAYOUT, decoder_io.STYLE):
                raise SystemExit(f"prism_x.json layout/style {(px['layout'], px['style'])} != train_meta "
                                 f"{(decoder_io.LAYOUT, decoder_io.STYLE)}")
        info = {**info, "layout": decoder_io.LAYOUT, "style": decoder_io.STYLE, "prism_x": prism_json,
                "note": f"{mode}: layout/style resolved from train_meta, no weights loaded"}
        tok = AutoTokenizer.from_pretrained(str(model_dir))
        tok.padding_side = "right"
        if tok.pad_token is None:
            tok.pad_token = tok.eos_token
        dev = "cpu"
    fmt = "cygnet" if decoder_io.STYLE == "cygnet" else "od"
    px_on = bool(info.get("prism_x"))
    if px_on and a.graphs:
        raise SystemExit("--graphs is not supported with PRISM-X (it runs eagerly)")
    print(json.dumps({"run_v154": {"name": name, "mode": mode, "n_tasks": len(tasks), "layout": decoder_io.LAYOUT,
                                   "style": decoder_io.STYLE, "fmt": fmt, "prism_x": px_on}}), flush=True)
    stats = check_prompts(jo, decoder_io, tasks, tok, fmt, px_on)
    ntok = [s["n_tokens"] for s in stats if s["n_tokens"]]
    print(f"pre-flight OK on {len(stats)} prompts (layout followed{', PRISM-X spans found' if px_on else ''}); "
          f"tokens mean {sum(ntok) / max(1, len(ntok)):.0f}, max {max(ntok) if ntok else '-'}", flush=True)
    out.mkdir(parents=True)

    manifest = {
        "name": name, "mode": mode, "base": a.base, "revision": a.revision, "adapter": str(model_dir),
        "temps": [tn, tc], "fmt": fmt, "graphs": a.graphs, "load": info,
        "protocol": "UNOFFICIAL: JevBench v1.5.4 public items (the 231 published v1.2 items in the repository), "
                    "official harness Runner; score with score_v154.py (v1.5 formulas, public-only)",
        "jevbench_dir": str(jb), "jevbench_commit": git_head(jb), "dataset_hash_all": all_hash,
        "dataset_hash_run": dataset_hash(tasks), "tiers": a.tiers, "n_tasks": len(tasks),
        "method_v15_sha256": sha256(jb / "docs/METHOD-v1.5.md"),
        "code_sha256": {"jevbench_od.py": sha256(jo.__file__), "decoder_io.py": sha256(decoder_io.__file__),
                        "prism_x.py": sha256(lean / "prism_x.py"), "run_v154.py": sha256(__file__)},
        "code_paths": {"jevbench_od": jo.__file__, "decoder_io": decoder_io.__file__},
        "host": platform.node(), "python": sys.version.split()[0], "torch": torch.__version__,
        "cost_basis": "self_hosted_gpu", "started_utc": started,
    }
    try:
        import transformers
        manifest["transformers"] = transformers.__version__
    except Exception:
        pass
    if mode == "dry-run":
        with open(out / "prompts.jsonl", "w") as f:
            for s in stats:
                f.write(json.dumps(s) + "\n")
        manifest["finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
        (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
        usd = sum(ntok) / max(1, len(ntok)) * 0.03 / 1e6 * 1000
        print(f"dry-run: wrote {out}/prompts.jsonl; est. cost at the frozen Qwen3.5-4B reference ($0.03/M input): "
              f"${usd:.4f} per 1,000 decisions")
        return

    if mode == "fake-model":
        model = tiny_model(tok)
        # the adapter hard-codes "cuda": route its forward to the CPU for this smoke test only
        jo.cand_logits = lambda m, ro, rows, _dev, **k: decoder_io.cand_logits(m, ro, rows, "cpu", **k)
        torch.cuda.synchronize = lambda *x, **k: None
    ad = jo.OpenDecideAdapter(model, tok, temps, label=name, fmt=fmt)
    tw = time.time()
    if mode == "gpu":  # server start-up: compile/autotune every length bucket with filler text (no task data)
        decoder_io.warmup(model, ad.ro, max_tokens=a.warmup_tokens, batch_sizes=(1,))
        if a.graphs:
            decoder_io.GRAPHS = decoder_io.GraphRunner(model, tok, batches=(1,))
            decoder_io.GRAPHS.capture_all(max_tokens=4096)
            chk = [{k: v for k, v in build_row(jo, decoder_io, t, tok, fmt).items() if k != "_prompt"} for t in tasks[:6]]
            g_, decoder_io.GRAPHS = decoder_io.GRAPHS, None
            eag = [decoder_io.cand_logits(model, ad.ro, [r], dev)[0] for r in chk]
            decoder_io.GRAPHS = g_
            grp = [decoder_io.cand_logits(model, ad.ro, [r], dev)[0] for r in chk]
            diff = max(float((torch.softmax(x, -1) - torch.softmax(y, -1)).abs().max()) for x, y in zip(eag, grp))
            print(f"graph self-check: max prob diff vs eager {diff:.2e}", flush=True)
            manifest["graph_selfcheck_max_prob_diff"] = diff
        for t in tasks[:3]:  # warm-up calls, not recorded (CUDA init is not decision latency)
            ad.run(t)
    manifest["warmup_s"] = round(time.time() - tw, 1)
    manifest["load_and_warmup_s"] = round(time.time() - t0, 1)
    if mode == "gpu":
        manifest["gpu"] = torch.cuda.get_device_name(0)
        manifest["gpu_users_before_load"] = users
    print(f"warm-up {manifest['warmup_s']}s; running {len(tasks)} tasks serially", flush=True)
    runner = Runner(ad, Ledger(str(out / "ledger.jsonl"), cap_usd=100), raw_dir=str(out / "raw"))
    tr = time.time()
    recs = runner.run_all(tasks, results_path=str(out / "results.jsonl"))
    manifest.update({"run_s": round(time.time() - tr, 1), "n_records": len(recs),
                     "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat()})
    if mode == "gpu":
        manifest["max_memory_gb"] = round(torch.cuda.max_memory_allocated() / 2 ** 30, 2)
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    ok = sum(bool(r["correct"]) for r in recs)
    lat = sorted(r["latency_s"] for r in recs)
    print(f"{name}: {len(recs)} records, argmax-correct {ok} (v1.4 rule), raw latency p50 "
          f"{lat[len(lat) // 2] * 1000:.0f} ms; wrote {out}\nscore: python3 {HERE / 'score_v154.py'} {out.name} jev_p1")


if __name__ == "__main__":
    main()
