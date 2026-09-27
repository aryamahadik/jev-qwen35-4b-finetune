"""Run OpenDecide jobs on a plain GPU machine (the Google Cloud L4 VM) with the same code paths as modal_od.py:
train_decoder.train for training and decoder_io.predict for predictions, the same config keys, the same LoRA targets,
and the same prediction file format (preds_<split>/<name>.jsonl plus a .meta.json). Paths are relative to this
directory: data/ holds the splits, models/<name>/ holds adapters.
  python od_gcp.py predict --name q35_2b_v11r --base Qwen/Qwen3.5-2B --splits dev,hard_dev [--tag suffix]
  python od_gcp.py train --name X --base Qwen/Qwen3.5-2B [same options as modal_od.py::train]
  python od_gcp.py smoke --base Qwen/Qwen3.5-2B --train-file train_2b_rest.jsonl --steps 20 [--batch 16]
  python od_gcp.py latency --name q35_2b_v11r --base Qwen/Qwen3.5-2B --split dev
"""
import argparse
import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA, MODELS = HERE / "data", HERE / "models"
QWEN35_TARGETS = r".*layers\.\d+\..*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj|out_proj|in_proj[a-z_]*)"


def rows(split):
    return [json.loads(l) for l in open(DATA / f"{split}.jsonl")]


def save(name, preds_by_split, extra=None):
    for s, preds in preds_by_split.items():
        rs = rows(s)
        pd = HERE / ("preds" if s == "eval" else f"preds_{s}")
        pd.mkdir(exist_ok=True)
        with open(pd / f"{name}.jsonl", "w") as f:
            for r, p in zip(rs, preds):
                f.write(json.dumps({"id": r["id"], "model": name, "probs": p}) + "\n")
        (pd / f"{name}.meta.json").write_text(json.dumps({"name": name, "rows": len(rs), **(extra or {})}, indent=2))
        print(f"wrote {pd.name}/{name}.jsonl ({len(preds)} rows)", flush=True)


def gpu_info():
    import torch
    return {"gpu": torch.cuda.get_device_name(0), "torch": torch.__version__, "cuda": torch.version.cuda}


def cmd_predict(a):
    import decoder_io
    decoder_io.STYLE = a.style
    adapter = str(MODELS / a.name) if a.adapter else None
    t0 = time.time()
    model, tok = decoder_io.load(a.base, "cuda", adapter=adapter)
    if adapter:
        model = model.merge_and_unload()
    model.eval()
    out = {}
    for s in a.splits.split(","):
        t = time.time()
        out[s] = decoder_io.predict(model, tok, rows(s), dev="cuda")
        print(f"{s}: {len(out[s])} rows in {time.time() - t:.0f}s", flush=True)
    save(a.name + a.tag, out, {"base": a.base, "host": "gcp", **gpu_info(), "sec": round(time.time() - t0)})


def build_cfg(a):
    cfg = {"base": a.base, "recipe": a.recipe, "epochs": a.epochs, "lr": a.lr, "batch": a.batch, "lam": a.lam, "r": a.r,
           "alpha": 2 * a.r, "train_file": a.train_file, "rel_file": a.rel_file, "grad_ckpt": True, "beta": a.beta,
           "style": a.style, "log_every": a.log_every, "kd": a.kd,
           **({"init_adapter": str(MODELS / a.init)} if a.init else {}), **(json.loads(a.extra) if a.extra else {})}
    if "Qwen3.5" in a.base:
        cfg["targets"] = QWEN35_TARGETS
    return cfg


def cmd_train(a):
    import decoder_io
    import train_decoder
    decoder_io.STYLE = a.style
    cfg = build_cfg(a)
    res = train_decoder.train(cfg, DATA, MODELS / a.name)
    model, tok = res["model"], res["tok"]
    preds = {s: decoder_io.predict(model, tok, rows(s), dev="cuda") for s in a.splits.split(",") if s}
    save(a.name, preds, {"base": a.base, "host": "gcp", **gpu_info(), "train": {k: v for k, v in res["meta"].items() if k != "log"}})
    (HERE / "logs").mkdir(exist_ok=True)
    (HERE / f"logs/{a.name}.json").write_text(json.dumps(res["meta"], indent=2))


def cmd_smoke(a):
    """A few training steps on the first rows of a train file: loss finite, seconds per step, peak GPU memory."""
    import torch
    import decoder_io
    import train_decoder
    decoder_io.STYLE = a.style
    src = [json.loads(l) for l in open(DATA / a.train_file)]
    n = a.steps * a.batch + 64
    tmp = DATA / "_smoke_train.jsonl"
    tmp.write_text("".join(json.dumps(r) + "\n" for r in src[:n]))
    a.train_file, a.rel_file, a.epochs, a.log_every = tmp.name, "_none_relations.jsonl", a.steps * a.batch / n, 5
    (DATA / a.rel_file).write_text("")
    torch.cuda.reset_peak_memory_stats()
    t0 = time.time()
    res = train_decoder.train(build_cfg(a), DATA, HERE / "models/_smoke")
    log = res["meta"].get("log", [])
    print(json.dumps({"steps": a.steps, "batch": a.batch, "sec_total": round(time.time() - t0),
                      "min_per_step_logged": [x.get("min") for x in log][-3:], "last_losses": [x.get("loss") for x in log][-3:],
                      "peak_mem_gb": round(torch.cuda.max_memory_allocated() / 2**30, 2), **gpu_info()}), flush=True)


def cmd_latency(a):
    import decoder_io
    decoder_io.STYLE = a.style
    model, tok = decoder_io.load(a.base, "cuda", adapter=str(MODELS / a.name))
    model = model.merge_and_unload()
    model.eval()
    print(json.dumps({"latency": decoder_io.latency(model, tok, rows(a.split), dev="cuda"), **gpu_info()}), flush=True)


ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
p = sub.add_parser("predict")
p.add_argument("--name", required=True)
p.add_argument("--base", required=True)
p.add_argument("--splits", required=True)
p.add_argument("--style", default="cygnet")
p.add_argument("--tag", default="")
p.add_argument("--no-adapter", dest="adapter", action="store_false")
for nm in ("train", "smoke"):
    t = sub.add_parser(nm)
    t.add_argument("--name", default="_smoke")
    t.add_argument("--base", required=True)
    t.add_argument("--recipe", default="A3")
    t.add_argument("--splits", default="")
    t.add_argument("--epochs", type=float, default=1.0)
    t.add_argument("--lr", type=float, default=1e-4)
    t.add_argument("--batch", type=int, default=16)
    t.add_argument("--lam", type=float, default=1.0)
    t.add_argument("--r", type=int, default=16)
    t.add_argument("--beta", type=float, default=1.0)
    t.add_argument("--kd", type=float, default=0.0)
    t.add_argument("--style", default="cygnet")
    t.add_argument("--train-file", dest="train_file", default="train.jsonl")
    t.add_argument("--rel-file", dest="rel_file", default="train_relations.jsonl")
    t.add_argument("--init", default="")
    t.add_argument("--extra", default='{"lam_inv": 1.0, "sym_cons": true, "perm_twin": 0.3, "lam_p": 0.5}')
    t.add_argument("--log-every", dest="log_every", type=int, default=50)
    t.add_argument("--steps", type=int, default=20)
l = sub.add_parser("latency")
l.add_argument("--name", required=True)
l.add_argument("--base", required=True)
l.add_argument("--split", default="dev")
l.add_argument("--style", default="cygnet")
a = ap.parse_args()
{"predict": cmd_predict, "train": cmd_train, "smoke": cmd_smoke, "latency": cmd_latency}[a.cmd](a)
