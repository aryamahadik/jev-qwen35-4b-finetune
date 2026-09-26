"""Latency probe on H100: where do the ~66 ms per decision go, and do CUDA graphs remove the overhead?
Compares (a) current path, (b) no attention mask (batch 1, right padding is causal-safe), (c) CUDA graph per length
bucket. Checks that (b)/(c) give the same candidate probabilities as (a). JevBench half-A prompts, no labels used."""
import json
import statistics
import time

import modal

from modal_od import SECRETS, image35, vol

app = modal.App("opendecide-graphprobe")


@app.function(image=image35.add_local_python_source("modal_od"), gpu="H100", volumes={"/vol": vol}, secrets=SECRETS, timeout=1800)
def probe(adapter: str = "/vol/models/q35_4b_v07", bucket: int = 64):
    import sys
    import torch
    import decoder_io
    decoder_io.STYLE = "cygnet"
    sys.path.insert(0, "/root/jevbench_pkg")
    from jevbench.tasks import load_jsonl
    import jevbench_od
    model, tok = decoder_io.load("Qwen/Qwen3.5-4B", "cuda", adapter=adapter)
    model = model.merge_and_unload()
    model.eval()
    ro = decoder_io.Readout(tok)
    body, head = decoder_io._parts(model)
    tasks = load_jsonl("/root/jb_split/jevbench_A.jsonl")
    rows = [jevbench_od.letter_row(t, tok, "cygnet")[0] for t in tasks]
    res = {}

    def timeit(fn, reps=1):
        torch.cuda.synchronize()
        t = time.perf_counter()
        out = fn()
        torch.cuda.synchronize()
        return out, (time.perf_counter() - t) * 1000

    decoder_io.warmup(model, ro, max_tokens=4096, batch_sizes=(1,))
    # (a) current path
    base, lat_a = [], []
    for r in rows:
        o, ms = timeit(lambda: decoder_io.cand_logits(model, ro, [r], "cuda")[0])
        base.append(torch.softmax(o, -1))
        lat_a.append(ms)
    # components
    t_tok, t_fwd, t_read = [], [], []
    with torch.no_grad():
        for r in rows[:40]:
            t = time.perf_counter()
            enc = tok([r["_prompt"]], add_special_tokens=False, return_tensors="pt").to("cuda")
            t_tok.append((time.perf_counter() - t) * 1000)
            hs, ms = timeit(lambda: body(input_ids=enc["input_ids"]).last_hidden_state)
            t_fwd.append(ms)
            t = time.perf_counter()
            groups = ro.cand(r)
            flat = [x for g in groups for x in g]
            lg = hs[0, -1].float() @ head.weight[flat].float().T
            torch.cuda.synchronize()
            t_read.append((time.perf_counter() - t) * 1000)
    res["components_ms_median"] = {"tokenize": statistics.median(t_tok), "forward_nomask_nopad": statistics.median(t_fwd),
                                   "readout": statistics.median(t_read)}

    # (c) CUDA graphs per bucket, batch 1, no mask, right-padded to the bucket (causal: pads never affect real tokens)
    graphs = {}

    def get_graph(L):
        if L in graphs:
            return graphs[L]
        ids = torch.full((1, L), tok.pad_token_id, dtype=torch.long, device="cuda")
        s = torch.cuda.Stream()
        s.wait_stream(torch.cuda.current_stream())
        with torch.cuda.stream(s), torch.no_grad():
            for _ in range(3):
                body(input_ids=ids, use_cache=False)
        torch.cuda.current_stream().wait_stream(s)
        g = torch.cuda.CUDAGraph()
        with torch.cuda.graph(g), torch.no_grad():
            out = body(input_ids=ids, use_cache=False).last_hidden_state
        graphs[L] = (g, ids, out)
        return graphs[L]

    err = None
    lat_c, maxdiff = [], 0.0
    try:
        t0 = time.time()
        lens = sorted({((len(tok(r["_prompt"], add_special_tokens=False)["input_ids"]) + bucket - 1) // bucket) * bucket for r in rows})
        for L in lens:
            get_graph(L)
        res["graph_capture_s"] = round(time.time() - t0, 1)
        res["graphs"] = len(lens)
        for r, b in zip(rows, base):
            def run():
                ids = tok(r["_prompt"], add_special_tokens=False, return_tensors="pt")["input_ids"][0].to("cuda", non_blocking=True)
                n = ids.shape[0]
                L = ((n + bucket - 1) // bucket) * bucket
                g, sid, out = get_graph(L)
                sid.fill_(tok.pad_token_id)
                sid[0, :n].copy_(ids)
                g.replay()
                groups = ro.cand(r)
                flat = [x for gg in groups for x in gg]
                lg = out[0, n - 1].float() @ head.weight[flat].float().T
                parts, k = [], 0
                for gg in groups:
                    parts.append(torch.logsumexp(lg[k:k + len(gg)], 0))
                    k += len(gg)
                return torch.softmax(torch.stack(parts), -1)
            p, ms = timeit(run)
            lat_c.append(ms)
            maxdiff = max(maxdiff, float((p - b).abs().max()))
    except Exception as e:
        err = repr(e)[:600]
    q = lambda xs: {"p50": round(statistics.median(xs), 1), "p95": round(sorted(xs)[int(0.95 * len(xs))], 1)} if xs else None
    res.update({"current_ms": q(lat_a), "graph_ms": q(lat_c), "graph_max_prob_diff": maxdiff, "graph_error": err})
    return res


@app.local_entrypoint()
def main(bucket: int = 64):
    print(json.dumps(probe.remote(bucket=bucket), indent=1))
