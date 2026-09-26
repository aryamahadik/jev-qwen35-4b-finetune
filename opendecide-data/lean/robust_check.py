"""Check: batched predict_robust == per-row robust_probs; two_stage decisions == full-variant decisions (small model)."""
import json

import modal

from modal_od import SECRETS, image35, vol

app = modal.App("opendecide-robustcheck")


@app.function(image=image35.add_local_python_source("modal_od"), gpu="L4", volumes={"/vol": vol}, secrets=SECRETS, timeout=1200)
def check(base: str = "Qwen/Qwen3.5-0.8B"):
    import time
    import decoder_io
    decoder_io.STYLE = "cygnet"
    model, tok = decoder_io.load(base, "cuda")
    model.eval()
    ro = decoder_io.Readout(tok)
    rows = [json.loads(l) for l in open("/root/data/devp_card.jsonl")][::60][:29] + \
           [json.loads(l) for l in open("/root/data/dev.jsonl")][:15]
    t = time.time()
    decoder_io.warmup(model, ro, max_tokens=1024, batch_sizes=(1, 2))
    tw = time.time() - t
    batched, infos = decoder_io.predict_robust(model, tok, rows, "cuda", meta_min=0.0)
    per = [decoder_io.robust_probs(model, ro, r, "cuda", meta_min=0.0, two_stage=False) for r in rows]
    diff = max(abs(batched[i][k] - per[i][0][k]) for i in range(len(rows)) for k in batched[i])
    same2 = sum(max(decoder_io.robust_probs(model, ro, r, "cuda", meta_min=0.6, two_stage=True)[0].items(), key=lambda x: x[1])[0]
                == max(decoder_io.robust_probs(model, ro, r, "cuda", meta_min=0.6, two_stage=False)[0].items(), key=lambda x: x[1])[0]
                for r in rows)
    return {"rows": len(rows), "simple_rows": sum(i["kind"] == "none" for i in infos), "max_diff": diff,
            "two_stage_same_decision": f"{same2}/{len(rows)}", "warmup_s": round(tw, 1)}


@app.local_entrypoint()
def main():
    print(json.dumps(check.remote(), indent=1))
