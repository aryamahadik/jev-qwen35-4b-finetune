"""C1 fast-path timing on the think server's H100 (A17 B1 rule: fast-path p50 <= 50 ms compute).

C1 = q35_4b_main500k, LoRA merged into the weights, one-pass candidate-token readout through decoder_io's CUDA-graph
GraphRunner (the serving form, as di_engine.py builds it). Runs in the container's /opt/fastpath venv (the PINNED35
stack of modal_od.image35, the one C1 was trained and evaluated with), as its own process next to the SGLang think
engine: R_serving.md 5 "two processes on one GPU".

  /opt/fastpath/bin/python fast_timing.py --adapter /vol/models/q35_4b_main500k --rows a.jsonl,b.jsonl --out t.json

Reported, device-synchronised wall ms (prompt building + tokenisation included, as decoder_io.latency does):
  batch 1: one decision per call, p50 / p95 over n rows after 10 warm calls;
  batched: B rows per call (B = 4, 8, 16): ms per call and ms per decision;
  per state: every question of one call_id in one call (dev rows), as decoder_io.latency_state;
  graph check: max |p_graph - p_eager| on 16 rows (must be ~0) and the share of calls that ran on a CUDA graph.
No labels are read. The adapter's sha256 is checked before load.
"""
import argparse
import hashlib
import json
import statistics
import sys
import time

ap = argparse.ArgumentParser()
ap.add_argument("--adapter", required=True)
ap.add_argument("--sha256", default="")
ap.add_argument("--base", default="Qwen/Qwen3.5-4B")
ap.add_argument("--rows", required=True, help="comma-separated jsonl files of our rows")
ap.add_argument("--out", required=True)
ap.add_argument("--n", type=int, default=200)
ap.add_argument("--batches", default="4,8,16")
ap.add_argument("--max-tokens", type=int, default=4096)
ap.add_argument("--lean", default="/root/lean")
a = ap.parse_args()
sys.path.insert(0, a.lean)

import torch  # noqa: E402

import decoder_io as dio  # noqa: E402


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def pct(ts, q):
    ts = sorted(ts)
    return round(ts[min(len(ts) - 1, int(len(ts) * q))], 2)


def timed(fn):
    torch.cuda.synchronize()
    t = time.perf_counter()
    out = fn()
    torch.cuda.synchronize()
    return out, (time.perf_counter() - t) * 1000


def main():
    res = {"adapter": a.adapter, "device": torch.cuda.get_device_name(), "torch": torch.__version__}
    got = sha_file(f"{a.adapter}/adapter_model.safetensors")
    res["adapter_sha256"] = got
    if a.sha256 and got != a.sha256:
        raise SystemExit(f"adapter sha256 {got[:16]} != expected {a.sha256[:16]}")
    rows = []
    for f in a.rows.split(","):
        rows += [json.loads(x) for x in open(f) if x.strip()]
    rows = [r.get("row", r) for r in rows]  # parity items carry the row under "row"
    t0 = time.perf_counter()
    model, tok, info = dio.load(a.base, "cuda", adapter=a.adapter, return_info=True)  # layout/style/revision from C1
    model = model.merge_and_unload()  # serving form: LoRA folded into the weights
    model.eval()
    ro = dio.Readout(tok)
    res["load"] = {k: info.get(k) for k in ("layout", "style", "revision", "prism_x")}
    res["load_s"] = round(time.perf_counter() - t0, 1)
    import transformers
    res["transformers"] = transformers.__version__
    with torch.no_grad():
        eager = [dio.cand_logits(model, ro, [r], "cuda")[0].float().softmax(-1) for r in rows[:16]]
        t1 = time.perf_counter()
        dio.warmup(model, ro, max_tokens=a.max_tokens, batch_sizes=(1, 4, 8, 16))
        dio.GRAPHS = dio.GraphRunner(model, tok, batches=(1, 2, 4, 8, 16), max_len=a.max_tokens)
        dio.GRAPHS.capture_all(max_tokens=2048)
        res["warmup_capture_s"] = round(time.perf_counter() - t1, 1)
        graph = [dio.cand_logits(model, ro, [r], "cuda")[0].float().softmax(-1) for r in rows[:16]]
        res["graph_vs_eager_max_abs_dprob"] = max(float((g - e).abs().max()) for g, e in zip(graph, eager))
        ntok = [len(tok(dio.prompt_texts(ro, [r])[0], add_special_tokens=False)["input_ids"]) for r in rows]
        res["prompt_tokens"] = {"p50": statistics.median(ntok), "max": max(ntok), "n_rows": len(rows),
                                "share_in_graph_len": round(sum(n <= a.max_tokens for n in ntok) / len(ntok), 3)}
        ts = []
        for r in (rows * 3)[: a.n + 10]:
            ts.append(timed(lambda: dio.cand_logits(model, ro, [r], "cuda"))[1])
        ts = ts[10:]
        res["batch1"] = {"p50_ms": pct(ts, 0.5), "p95_ms": pct(ts, 0.95), "mean_ms": round(statistics.mean(ts), 2),
                         "n": len(ts)}
        res["batched"] = {}
        for B in [int(x) for x in a.batches.split(",")]:
            calls = [rows[i:i + B] for i in range(0, len(rows) - B + 1, B)]
            for g in calls[:3]:
                dio.cand_logits(model, ro, g, "cuda")
            tc = [timed(lambda g=g: dio.cand_logits(model, ro, g, "cuda"))[1] for g in calls]
            res["batched"][str(B)] = {"call_p50_ms": pct(tc, 0.5), "call_p95_ms": pct(tc, 0.95),
                                      "per_decision_p50_ms": round(pct(tc, 0.5) / B, 2), "calls": len(tc)}
        by = {}
        for r in rows:
            if r.get("call_id") is not None:
                by.setdefault(r["call_id"], []).append(r)
        if by:
            tg = [timed(lambda g=g: dio.cand_logits(model, ro, g, "cuda"))[1] for g in list(by.values())[:150]]
            res["per_state"] = {"p50_ms": pct(tg, 0.5), "p95_ms": pct(tg, 0.95), "n_states": len(tg),
                                "questions_mean": round(statistics.mean(len(g) for g in by.values()), 2)}
    res["gpu_mem_gb"] = round(torch.cuda.max_memory_allocated() / 2**30, 2)
    res["b1_rule_fast_p50_le_50ms"] = res["batch1"]["p50_ms"] <= 50.0
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps({k: res[k] for k in ("batch1", "graph_vs_eager_max_abs_dprob", "b1_rule_fast_p50_le_50ms")}))


if __name__ == "__main__":
    main()
