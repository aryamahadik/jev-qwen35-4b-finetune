"""OpenDecide on Modal: every training run and every model evaluation happens here, not on the laptop.

  modal run modal_od.py::bakeoff --models qwen3-1.7b,gliclass-modern-large --splits dev,devzs
  modal run modal_od.py::train --name q17_A3 --base Qwen/Qwen3-1.7B --recipe A3 --splits dev,devzs
  modal run modal_od.py::latency --name q17_A3 --gpu L4

Predictions come back to the laptop as lean/preds_<split>/<name>.jsonl (preds/ for eval), ready for score.py.
Adapters live on the Modal volume "opendecide" under /vol/models/<name>.
"""
from __future__ import annotations

import json
from pathlib import Path

import modal

HERE = Path(__file__).resolve().parent
JB = HERE.parent.parent / "bench/jevbench"  # JevBench v1.4.2 @ 1bcc55eb (public items + official runner/scoring)
app = modal.App("opendecide")
vol = modal.Volume.from_name("opendecide", create_if_missing=True)
image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("torch==2.8.0", "transformers==4.57.6", "peft==0.17.1", "accelerate", "gliclass==0.1.17",
                 "datasets", "numpy", "sentencepiece", "protobuf", "hf_transfer", "sentence-transformers==5.1.1")
    .env({"HF_HOME": "/vol/hf", "HF_HUB_ENABLE_HF_TRANSFER": "1", "TOKENIZERS_PARALLELISM": "false"})
    .add_local_python_source("decoder_io", "gliclass_io", "train_decoder", "hc", "jevbench_od")
    .add_local_dir(JB / "jevbench", "/root/jevbench_pkg/jevbench")
    .add_local_dir(JB / "datasets/public", "/root/jb_public")
    .add_local_dir(JB.parent / "splits", "/root/jb_split")
    .add_local_file(HERE / "train.py", "/root/train.py")
    .add_local_dir(HERE / "data", "/root/data")
)
# Qwen3.5 (hybrid Gated-DeltaNet + attention) and Gemma 4 need transformers 5.x; fla's Triton kernels need
# triton >= 3.7.1 on Hopper (torch 2.14 ships triton 3.8)
image35 = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("torch==2.14.0", "transformers==5.17.0", "peft", "accelerate", "flash-linear-attention==0.5.2",
                 "datasets", "numpy", "sentencepiece", "protobuf", "hf_transfer", "sentence-transformers")
    .env({"HF_HOME": "/vol/hf", "HF_HUB_ENABLE_HF_TRANSFER": "1", "TOKENIZERS_PARALLELISM": "false"})
    .add_local_python_source("decoder_io", "train_decoder", "hc", "jevbench_od")
    .add_local_dir(JB / "jevbench", "/root/jevbench_pkg/jevbench")
    .add_local_dir(JB / "datasets/public", "/root/jb_public")
    .add_local_dir(JB.parent / "splits", "/root/jb_split")
    .add_local_dir(HERE / "data", "/root/data")
)
SECRETS = [modal.Secret.from_name("opendecide-keys")]
# LoRA on every decoder-layer projection (attention, Gated-DeltaNet in/out projections, MLP); vision blocks are not "layers.N"
GEMMA4_TARGETS = r"^(?!.*(vision|audio|visual)).*layers\.\d+\.(self_attn|mlp)\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj)"
QWEN35_TARGETS = r".*layers\.\d+\..*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj|out_proj|in_proj[a-z_]*)"


def is35(hf_id):  # needs the transformers-5 image
    return "Qwen3.5" in hf_id or "gemma-4" in hf_id

# short name -> (kind, HF id)
BACKBONES = {
    "qwen3-0.6b": ("decoder", "Qwen/Qwen3-0.6B"),
    "qwen3-1.7b": ("decoder", "Qwen/Qwen3-1.7B"),
    "qwen3-4b": ("decoder", "Qwen/Qwen3-4B-Instruct-2507"),
    "qwen3-8b": ("decoder", "Qwen/Qwen3-8B"),
    "qwen3-30b-a3b": ("decoder", "Qwen/Qwen3-30B-A3B-Instruct-2507"),
    "qwen3.5-4b": ("decoder", "Qwen/Qwen3.5-4B"),
    "qwen3.5-2b": ("decoder", "Qwen/Qwen3.5-2B"),
    "qwen3.5-9b": ("decoder", "Qwen/Qwen3.5-9B"),
    "gemma4-12b": ("decoder", "google/gemma-4-12B-it"),
    "gliclass-edge": ("gliclass", "knowledgator/gliclass-edge-v3.0"),
    "gliclass-modern-base": ("gliclass", "knowledgator/gliclass-modern-base-v3.0"),
    "gliclass-modern-large": ("gliclass", "knowledgator/gliclass-modern-large-v3.0"),
    "gliclass-large": ("gliclass", "knowledgator/gliclass-large-v3.0"),
}


def _rows(split):
    return [json.loads(l) for l in open(f"/root/data/{split}.jsonl")]


def _predict(kind, model, tok, rows, tta=False):
    import torch
    if kind == "decoder":
        import decoder_io
        return decoder_io.predict(model, tok, rows, dev="cuda", tta=tta)
    import gliclass_io
    return gliclass_io.predict(model, tok, rows, dev=torch.device("cuda"))


def _load(kind, hf_id, adapter=None):
    import torch
    if kind == "decoder":
        import decoder_io
        return decoder_io.load(hf_id, "cuda", adapter=adapter)
    import gliclass_io
    return gliclass_io.load(adapter or hf_id, torch.device("cuda"))


def _zeroshot_impl(short, splits, tta, system=None):
    import time
    if system:
        import decoder_io
        decoder_io.SYSTEM = system
    kind, hf_id = BACKBONES[short]
    t = time.time()
    model, tok = _load(kind, hf_id)
    out = {}
    for s in splits:
        rows = _rows(s)
        out[s] = _predict(kind, model, tok, rows, tta=tta)
    vol.commit()
    return {"preds": out, "seconds": round(time.time() - t, 1), "hf_id": hf_id}


@app.function(image=image, gpu="L40S", volumes={"/vol": vol}, secrets=SECRETS, timeout=3600)
def zeroshot(short: str, splits: list[str], tta: bool = False, system: str = "") -> dict:
    return _zeroshot_impl(short, splits, tta, system)


@app.function(image=image35, gpu="L40S", volumes={"/vol": vol}, secrets=SECRETS, timeout=3600)
def zeroshot35(short: str, splits: list[str], tta: bool = False, system: str = "") -> dict:
    return _zeroshot_impl(short, splits, tta, system)


def _train_impl(name, cfg, splits, tta):
    import decoder_io
    decoder_io.STYLE = cfg.get("style", "od")
    import train_decoder
    res = train_decoder.train(cfg, Path("/root/data"), Path(f"/vol/models/{name}"))
    vol.commit()
    model, tok = res["model"], res["tok"]
    preds = {s: _predict("decoder", model, tok, _rows(s), tta=tta) for s in splits}
    return {"preds": preds, "meta": res["meta"]}


@app.function(image=image, gpu="L40S", volumes={"/vol": vol}, secrets=SECRETS, timeout=4 * 3600)
def train_remote(name: str, cfg: dict, splits: list[str], tta: bool = False) -> dict:
    return _train_impl(name, cfg, splits, tta)


@app.function(image=image35, gpu="L40S", volumes={"/vol": vol}, secrets=SECRETS, timeout=4 * 3600)
def train_remote35(name: str, cfg: dict, splits: list[str], tta: bool = False) -> dict:
    return _train_impl(name, cfg, splits, tta)


@app.function(image=image, gpu="L40S", volumes={"/vol": vol}, secrets=SECRETS, timeout=4 * 3600)
def train_gliclass_remote(name: str, argv: list[str], splits: list[str]) -> dict:
    """Runs the original train.py (GLiClass recipes A0/A3) on a GPU instead of the laptop."""
    import runpy
    import sys
    import torch
    import gliclass_io
    gliclass_io.device = lambda: torch.device("cuda")
    sys.argv = ["train.py", "--out", name, "--models_dir", "/vol/models", *argv]
    runpy.run_path("/root/train.py", run_name="__main__")
    vol.commit()
    model, tok = gliclass_io.load(f"/vol/models/{name}", torch.device("cuda"))
    meta = json.loads(Path(f"/vol/models/{name}/train_meta.json").read_text())
    return {"preds": {s: _predict("gliclass", model, tok, _rows(s)) for s in splits}, "meta": meta}


def _eval_impl(name, base, splits, tta, alpha=1.0, style="od"):
    import decoder_io
    decoder_io.STYLE = style
    model, tok = _load("decoder", base, adapter=f"/vol/models/{name}")
    if alpha != 1.0:  # WiSE-FT style: interpolate between the base model (0) and the fine-tuned model (1)
        n = 0
        for m in model.modules():
            if hasattr(m, "scaling") and isinstance(m.scaling, dict) and "default" in m.scaling:
                m.scaling["default"] *= alpha
                n += 1
        assert n > 0, "no LoRA layers found to scale"
    return {"preds": {s: _predict("decoder", model, tok, _rows(s), tta=tta) for s in splits}}


@app.function(image=image, volumes={"/vol": vol}, secrets=SECRETS, timeout=3600, gpu="L40S")
def eval_remote(name: str, base: str, splits: list[str], tta: bool = False, alpha: float = 1.0) -> dict:
    return _eval_impl(name, base, splits, tta, alpha)


@app.function(image=image35, volumes={"/vol": vol}, secrets=SECRETS, timeout=3600, gpu="L40S")
def eval_remote35(name: str, base: str, splits: list[str], tta: bool = False, style: str = "od") -> dict:
    return _eval_impl(name, base, splits, tta, 1.0, style)


def _latency_impl(kind, hf_id, adapter, n):
    import torch
    rows = [r for r in _rows("eval") if r["track"] in ("ID", "ZS")]
    model, tok = _load(kind, hf_id, adapter)
    if adapter and kind == "decoder":
        model = model.merge_and_unload()  # serving form: LoRA folded into the weights
    if kind == "decoder":
        import decoder_io
        out = decoder_io.latency(model, tok, rows, "cuda", n=n)
        out.update(decoder_io.latency_state(model, tok, _rows("eval"), "cuda"))
        return out
    import gliclass_io
    import time
    model.eval()
    ts = []
    with torch.no_grad():
        for r in rows[: n + 10]:
            torch.cuda.synchronize(); t = time.perf_counter()
            gliclass_io.forward_logits(model, tok, [r], torch.device("cuda"))
            torch.cuda.synchronize(); ts.append((time.perf_counter() - t) * 1000)
    ts = sorted(ts[10:])
    return {"device": torch.cuda.get_device_name(), "median_ms": ts[len(ts) // 2], "p95_ms": ts[int(len(ts) * 0.95)], "n": len(ts)}


@app.function(image=image, gpu="L4", volumes={"/vol": vol}, secrets=SECRETS, timeout=1800)
def latency_l4(kind: str, hf_id: str, adapter: str | None = None, n: int = 200) -> dict:
    return _latency_impl(kind, hf_id, adapter, n)


@app.function(image=image35, gpu="L4", volumes={"/vol": vol}, secrets=SECRETS, timeout=1800)
def latency35(kind: str, hf_id: str, adapter: str | None = None, n: int = 200) -> dict:
    return _latency_impl(kind, hf_id, adapter, n)


@app.function(image=image, gpu="L4", volumes={"/vol": vol}, secrets=SECRETS, timeout=3600)
def hc_recall_remote(embedder: str, split: str) -> dict:
    import hc
    sl = hc.Shortlister(embedder)
    return hc.recall_at(sl, _rows(split))


@app.function(image=image, gpu="L4", volumes={"/vol": vol}, secrets=SECRETS, timeout=3600)
def hc_shortlist_remote(embedder: str, split: str, k: int) -> dict:
    import hc
    sl = hc.Shortlister(embedder)
    out = {}
    for r in _rows(split):
        pool = [o for o in r["options"] if not o.startswith("none of")]
        if len(r["options"]) > 255:
            out[r["id"]] = sl.topk(r["state"], pool, k)
    return out


def _hc_impl(name, base, split, embedder, k, chunk, keep):
    import hc
    model, tok = _load("decoder", base, adapter=f"/vol/models/{name}" if name else None)
    if name:
        model = model.merge_and_unload()
    sl = hc.Shortlister(embedder) if embedder else None
    rows = _rows(split)
    if sl:  # label embeddings are cached offline, as in serving; do not count them in per-question latency
        sl._labels(sorted({o for r in rows for o in r["options"]}))
    hc.predict_many(model, tok, rows[:5], shortlist=sl, k=k, chunk=chunk, keep=keep)  # warm-up
    preds, lat = hc.predict_many(model, tok, rows, shortlist=sl, k=k, chunk=chunk, keep=keep)
    import torch
    return {"preds": preds, "lat": lat, "gpu": torch.cuda.get_device_name()}


@app.function(image=image, gpu="L40S", volumes={"/vol": vol}, secrets=SECRETS, timeout=4 * 3600)
def hc_remote(name: str, base: str, split: str, embedder: str, k: int, chunk: int, keep: int) -> dict:
    return _hc_impl(name, base, split, embedder, k, chunk, keep)


@app.function(image=image35, gpu="L40S", volumes={"/vol": vol}, secrets=SECRETS, timeout=4 * 3600)
def hc_remote35(name: str, base: str, split: str, embedder: str, k: int, chunk: int, keep: int) -> dict:
    return _hc_impl(name, base, split, embedder, k, chunk, keep)


def _jevbench_impl(name, base, adapter, temps, tiers, think_below=None, fmt="od", style="od"):
    import sys
    import decoder_io
    decoder_io.STYLE = style
    import torch
    sys.path.insert(0, "/root/jevbench_pkg")
    from jevbench.budget import Ledger
    from jevbench.runner import Runner
    from jevbench.tasks import load_jsonl
    import jevbench_od
    model, tok = _load("decoder", base, adapter=adapter or None)
    if adapter:
        model = model.merge_and_unload()
    model.eval()
    model.config.use_cache = True  # training-time gradient checkpointing turns the KV cache off in saved configs
    if getattr(model.config, "text_config", None) is not None:
        model.config.text_config.use_cache = True
    model.generation_config.use_cache = True
    ad = jevbench_od.OpenDecideAdapter(model, tok, temps, label=name, think_below=think_below, fmt=fmt)
    tasks = [t for tier in tiers for t in load_jsonl(f"/root/jb_split/jevbench_{tier}.jsonl" if tier in ("A", "B")
                                                      else f"/root/jb_public/{tier}.jsonl")]
    for t in tasks[:3]:  # warm-up (CUDA init is not decision latency, like a server that is already up)
        ad.run(t)
    Path("/tmp/jb").mkdir(exist_ok=True)
    runner = Runner(ad, Ledger("/tmp/jb/ledger.jsonl", cap_usd=100), raw_dir="/tmp/jb/raw")
    recs = runner.run_all(tasks, results_path="/tmp/jb/results.jsonl")
    return {"records": recs, "gpu": torch.cuda.get_device_name()}


@app.function(image=image, gpu="L40S", volumes={"/vol": vol}, secrets=SECRETS, timeout=3600)
def jevbench_remote(name: str, base: str, adapter: str, temps: dict, tiers: list[str], think_below: float | None = None, fmt: str = "od",
                     style: str = "od") -> dict:
    return _jevbench_impl(name, base, adapter, temps, tiers, think_below, fmt, style)


@app.function(image=image35, gpu="L40S", volumes={"/vol": vol}, secrets=SECRETS, timeout=3600)
def jevbench_remote35(name: str, base: str, adapter: str, temps: dict, tiers: list[str], think_below: float | None = None, fmt: str = "od",
                     style: str = "od") -> dict:
    return _jevbench_impl(name, base, adapter, temps, tiers, think_below, fmt, style)


def _save(name, preds_by_split, extra=None):
    for s, preds in preds_by_split.items():
        rows = [json.loads(l) for l in open(HERE / f"data/{s}.jsonl")]
        pd = HERE / ("preds" if s == "eval" else f"preds_{s}")
        pd.mkdir(exist_ok=True)
        with open(pd / f"{name}.jsonl", "w") as f:
            for r, p in zip(rows, preds):
                f.write(json.dumps({"id": r["id"], "model": name, "probs": p}) + "\n")
        meta_p = pd / f"{name}.meta.json"
        meta = json.loads(meta_p.read_text()) if meta_p.exists() else {}
        meta.update({"name": name, "rows": len(rows), **(extra or {})})
        meta_p.write_text(json.dumps(meta, indent=2))
        print(f"wrote {pd.name}/{name}.jsonl ({len(preds)} rows)")


@app.local_entrypoint()
def bakeoff(models: str, splits: str = "dev,devzs", tta: bool = False, suffix: str = "_zs", system: str = "", gpu: str = "L40S"):
    sp = splits.split(",")
    names = models.split(",")
    fn = (zeroshot35 if any(is35(BACKBONES[n][1]) for n in names) else zeroshot).with_options(gpu=gpu)
    assert len({is35(BACKBONES[n][1]) for n in names}) == 1, "do not mix Qwen3.5 with other backbones in one call"
    for short, res in zip(names, fn.map(names, kwargs={"splits": sp, "tta": tta, "system": system}, return_exceptions=True)):
        if isinstance(res, Exception):
            print(f"FAILED {short}: {res!r}")
            continue
        _save(short + suffix + ("_tta" if tta else ""), res["preds"], {"hf_id": res["hf_id"], "seconds": res["seconds"]})


@app.local_entrypoint()
def train(name: str, base: str, recipe: str = "A3", splits: str = "dev,devzs", epochs: float = 1.0, lr: float = 1e-4,
          batch: int = 16, lam: float = 0.5, r: int = 16, train_file: str = "train.jsonl",
          rel_file: str = "train_relations.jsonl", tta: bool = False, gpu: str = "L40S", grad_ckpt: bool = True,
          beta: float = 0.0, targets: str = "", style: str = "od"):
    cfg = {"base": base, "recipe": recipe, "epochs": epochs, "lr": lr, "batch": batch, "lam": lam, "r": r, "alpha": 2 * r,
           "train_file": train_file, "rel_file": rel_file, "grad_ckpt": grad_ckpt, "beta": beta, "style": style}
    if is35(base):
        cfg["targets"] = GEMMA4_TARGETS if "gemma-4" in base else QWEN35_TARGETS
    if targets:
        cfg["targets"] = targets.split(",") if "," in targets else targets
    fn = train_remote35 if is35(base) else train_remote
    res = fn.with_options(gpu=gpu).remote(name, cfg, splits.split(","), tta)
    _save(name + ("_tta" if tta else ""), res["preds"], {"base": base, "train": {k: v for k, v in res["meta"].items() if k != "log"}})
    (HERE / "logs").mkdir(exist_ok=True)
    (HERE / f"logs/{name}.json").write_text(json.dumps(res["meta"], indent=2))


@app.local_entrypoint()
def train_gliclass(name: str, base: str, recipe: str = "A3", splits: str = "dev,devzs", epochs: float = 2.0, lr: float = 3e-5,
                   train_file: str = "train.jsonl", rel_file: str = "train_relations.jsonl", gpu: str = "H100"):
    argv = ["--base", base, "--recipe", recipe, "--epochs", str(epochs), "--lr", str(lr),
            "--train_file", train_file, "--rel_file", rel_file]
    res = train_gliclass_remote.with_options(gpu=gpu).remote(name, argv, splits.split(","))
    _save(name, res["preds"], {"base": base, "train": {k: v for k, v in res["meta"].items() if k != "log"}})
    (HERE / "logs").mkdir(exist_ok=True)
    (HERE / f"logs/{name}.json").write_text(json.dumps(res["meta"], indent=2))


@app.local_entrypoint()
def evaluate(name: str, base: str, splits: str = "eval", tta: bool = False, alphas: str = "1.0", gpu: str = "L40S",
             style: str = "od"):
    al = [float(x) for x in alphas.split(",")]
    if is35(base):
        res = [eval_remote35.with_options(gpu=gpu).remote(name, base, splits.split(","), tta, style)]
    else:
        res = list(eval_remote.starmap([(name, base, splits.split(","), tta, x) for x in al]))
    for x, r in zip(al, res):
        tag = ("_tta" if tta else "") + ("" if x == 1.0 else f"_a{x:g}")
        _save(name + tag, r["preds"], {"base": base, "alpha": x})


@app.local_entrypoint()
def latency(kind: str, hf_id: str, adapter: str = "", name: str = "", n: int = 200, gpu: str = "L4"):
    res = (latency35 if is35(hf_id) else latency_l4).with_options(gpu=gpu).remote(kind, hf_id, adapter or None, n)
    print(json.dumps(res, indent=2))
    if name:
        p = HERE / f"preds/{name}.meta.json"
        meta = json.loads(p.read_text()) if p.exists() else {"name": name}
        meta[f"latency_{gpu.lower()}"] = res
        p.write_text(json.dumps(meta, indent=2))


@app.local_entrypoint()
def hc_recall(embedders: str = "Alibaba-NLP/gte-modernbert-base,Qwen/Qwen3-Embedding-0.6B", split: str = "dev_hc"):
    names = embedders.split(",")
    for e, res in zip(names, hc_recall_remote.map(names, kwargs={"split": split}, return_exceptions=True)):
        print(e, json.dumps(res if isinstance(res, dict) else repr(res), indent=1))
        (HERE / "logs").mkdir(exist_ok=True)
        (HERE / f"logs/recall_{split}_{e.split('/')[-1]}.json").write_text(json.dumps(res if isinstance(res, dict) else repr(res), indent=1))


@app.local_entrypoint()
def hc_eval(name: str, base: str, split: str = "dev_hc", embedder: str = "", k: int = 64, chunk: int = 20, keep: int = 2,
            gpu: str = "L40S", tag: str = ""):
    fn = hc_remote35 if is35(base) else hc_remote
    res = fn.with_options(gpu=gpu).remote(name, base, split, embedder, k, chunk, keep)
    out = (name or base.split("/")[-1]) + (tag or "")
    _save(out, {split: res["preds"]}, {"base": base, "embedder": embedder, "k": k, "chunk": chunk, "keep": keep, "gpu": res["gpu"]})
    pd = HERE / f"preds_{split}"
    rows = [json.loads(l) for l in open(HERE / f"data/{split}.jsonl")]
    lines = [json.loads(l) for l in open(pd / f"{out}.jsonl")]
    with open(pd / f"{out}.jsonl", "w") as f:
        for r, p, l in zip(rows, lines, res["lat"]):
            f.write(json.dumps({**p, "latency_ms": l["ms"], "passes": l["passes"]}) + "\n")


@app.local_entrypoint()
def hc_shortlist(embedder: str, split: str = "eval_hc", k: int = 255):
    res = hc_shortlist_remote.remote(embedder, split, k)
    (HERE / f"data/{split}_shortlist_{k}.json").write_text(json.dumps(res))
    print(f"wrote data/{split}_shortlist_{k}.json ({len(res)} rows)")


@app.local_entrypoint()
def jevbench(name: str, base: str, adapter: str = "", temps: str = "1.0,1.0", tiers: str = "easy,original,hard",
             gpu: str = "L40S", think_below: float = -1.0, fmt: str = "od", style: str = "od"):
    tn, tc = (float(x) for x in temps.split(","))
    fn = jevbench_remote35 if is35(base) else jevbench_remote
    res = fn.with_options(gpu=gpu).remote(name, base, adapter, {"noul": tn, "choice": tc}, tiers.split(","),
                                          think_below if think_below > 0 else None, fmt, style)
    out = JB.parent / "runs" / name
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "results.jsonl", "w") as f:
        for r in res["records"]:
            f.write(json.dumps(r) + "\n")
    (out / "manifest.json").write_text(json.dumps({"name": name, "base": base, "adapter": adapter, "temps": [tn, tc],
                                                   "gpu": res["gpu"], "tiers": tiers, "think_below": think_below, "fmt": fmt}, indent=2))
    ok = sum(r["correct"] for r in res["records"])
    print(f"{name}: {ok}/{len(res['records'])} correct on {tiers} ({res['gpu']})")


@app.function(image=image35, gpu="H100", volumes={"/vol": vol}, secrets=SECRETS, timeout=1800)
def gen_diag_remote(base: str) -> dict:
    """Decode speed: generate() vs a manual KV-cache loop, 64 new tokens after a ~2.4k-token prompt."""
    import time
    import torch
    import decoder_io
    model, tok = decoder_io.load(base, "cuda")
    model.eval()
    prompt = tok.apply_chat_template([{"role": "user", "content": ("The policy text. " * 600) + "\nSummarize the rule."}],
                                     tokenize=False, add_generation_prompt=True)
    enc = tok(prompt, add_special_tokens=False, return_tensors="pt").to("cuda")
    out = {"prompt_tokens": int(enc["input_ids"].shape[1]), "attn_impl": str(getattr(model.config, "_attn_implementation", "?"))}
    with torch.no_grad():
        for label, kw in (("generate_default", {}), ("generate_dynamic", {"cache_implementation": "dynamic"})):
            try:
                torch.cuda.synchronize(); t = time.perf_counter()
                g = model.generate(**enc, max_new_tokens=64, do_sample=False, use_cache=True, **kw)
                torch.cuda.synchronize()
                out[label] = {"new": int(g.shape[1] - enc["input_ids"].shape[1]), "s": round(time.perf_counter() - t, 2)}
            except Exception as e:  # noqa: BLE001
                out[label] = repr(e)[:200]
        torch.cuda.synchronize(); t = time.perf_counter()
        o = model(**enc, use_cache=True, logits_to_keep=1)
        pkv = o.past_key_values
        out["pkv_type"] = type(pkv).__name__
        ids, mask = o.logits[:, -1].argmax(-1, keepdim=True), enc["attention_mask"]
        for _ in range(63):
            mask = torch.cat([mask, mask.new_ones((1, 1))], 1)
            o = model(input_ids=ids, attention_mask=mask, past_key_values=pkv, use_cache=True, logits_to_keep=1)
            pkv, ids = o.past_key_values, o.logits[:, -1].argmax(-1, keepdim=True)
        torch.cuda.synchronize()
        out["manual_loop_64_s"] = round(time.perf_counter() - t, 2)
    return out


@app.local_entrypoint()
def gen_diag(base: str = "google/gemma-4-12B-it"):
    print(json.dumps(gen_diag_remote.remote(base)))
