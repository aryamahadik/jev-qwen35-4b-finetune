"""Does padding / batching change Qwen3.5 candidate logits? (hybrid Gated-DeltaNet model; right padding)"""
import json

import modal

from modal_od import SECRETS, image35, vol

app = modal.App("opendecide-padprobe")


@app.function(image=image35.add_local_python_source("modal_od"), gpu="L4", volumes={"/vol": vol}, secrets=SECRETS, timeout=1200)
def probe(base: str = "Qwen/Qwen3.5-4B"):
    import sys
    import torch
    import decoder_io
    decoder_io.STYLE = "cygnet"
    sys.path.insert(0, "/root/jevbench_pkg")
    from jevbench.tasks import load_jsonl
    import jevbench_od
    model, tok = decoder_io.load(base, "cuda")
    model.eval()
    ro = decoder_io.Readout(tok)
    tasks = load_jsonl("/root/jb_split/jevbench_A.jsonl")[:12]
    rows = []
    for t in tasks:
        r, keys, yi = jevbench_od.letter_row(t, tok, "cygnet")
        rows.append({k: v for k, v in r.items() if k != "_prompt"})
    out = {}
    with torch.no_grad():
        for pm in (1, 256):
            decoder_io.PAD_MULTIPLE = pm
            single = [torch.softmax(decoder_io.cand_logits(model, ro, [r], "cuda")[0], -1).tolist() for r in rows]
            batch = [torch.softmax(l, -1).tolist() for l in decoder_io.cand_logits(model, ro, rows, "cuda")]
            out[pm] = {"single": single, "batch": batch}
    diff = lambda a, b: max(max(abs(x - y) for x, y in zip(p, q)) for p, q in zip(a, b))
    return {"single_pad1_vs_pad256": diff(out[1]["single"], out[256]["single"]),
            "single_vs_batch_pad1": diff(out[1]["single"], out[1]["batch"]),
            "single_vs_batch_pad256": diff(out[256]["single"], out[256]["batch"]),
            "example": [out[1]["single"][:3], out[256]["single"][:3], out[256]["batch"][:3]],
            "attn_impl": getattr(model.config, "_attn_implementation", None)}


@app.local_entrypoint()
def main():
    print(json.dumps(probe.remote(), indent=1))
