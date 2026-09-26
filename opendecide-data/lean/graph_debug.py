"""Debug GraphRunner with batch > 1 on a small model, with synchronous CUDA errors."""
import json
import os

import modal

from modal_od import SECRETS, image35, vol

app = modal.App("opendecide-graphdebug")


@app.function(image=image35.add_local_python_source("modal_od"), gpu="L4",
              volumes={"/vol": vol}, secrets=SECRETS, timeout=900)
def dbg():
    os.environ["CUDA_LAUNCH_BLOCKING"] = "1"  # before torch initialises CUDA
    import traceback
    import torch
    import decoder_io
    decoder_io.STYLE = "cygnet"
    model, tok = decoder_io.load("Qwen/Qwen3.5-0.8B", "cuda")
    model.eval()
    ro = decoder_io.Readout(tok)
    rows = [json.loads(l) for l in open("/root/data/devp_card.jsonl")][:6]
    out = {"pad_token": tok.pad_token, "pad_id": tok.pad_token_id}
    gr = decoder_io.GraphRunner(model, tok, batches=(1, 2, 4), max_graph_tokens=4096)
    decoder_io.GRAPHS = None
    e1 = [decoder_io.cand_logits(model, ro, [r], "cuda")[0] for r in rows]
    diff = lambda a, b: max(float((torch.softmax(x, -1) - torch.softmax(y, -1)).abs().max()) for x, y in zip(a, b))
    step = "start"
    try:
        step = "b1 graphs only"
        for L in (64, 128, 256, 512):
            gr._graph(1, L)
        decoder_io.GRAPHS = gr
        out["b1_alone"] = diff(e1, [decoder_io.cand_logits(model, ro, [r], "cuda")[0] for r in rows])
        step = "capture b4"
        for L in (64, 128, 256, 512):
            gr._graph(4, L)
        step = "b1 after b4 capture"
        out["b1_after_b4_capture"] = diff(e1, [decoder_io.cand_logits(model, ro, [r], "cuda")[0] for r in rows])
        step = "b3 replay"
        grp = decoder_io.cand_logits(model, ro, rows[:3], "cuda")
        out["b3"] = diff(e1[:3], grp)
        step = "b1 after b4 replay"
        out["b1_after_b4_replay"] = diff(e1, [decoder_io.cand_logits(model, ro, [r], "cuda")[0] for r in rows])
    except Exception:
        out["failed_at"] = step
        out["error"] = traceback.format_exc()[-1500:]
    return out


@app.local_entrypoint()
def main():
    r = dbg.remote()
    print(json.dumps({k: v for k, v in r.items() if k != "error"}, indent=1))
    print(r.get("error", "no error"))
