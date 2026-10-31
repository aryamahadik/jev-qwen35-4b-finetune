"""Compare batched vs batch-1 hypotheses (the batch path is only a throughput device; this checks it does not change the text)."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import soundfile as sf, numpy as np, torch
from asr_lib import *
from r2common import *
root = os.path.expanduser("~/opt_r2/voice"); st = sys.argv[1]; n = int(sys.argv[2]); B = int(sys.argv[3]); thr = int(sys.argv[4]); dtype = sys.argv[5] if len(sys.argv) > 5 else "fp32"
proc, model = load_asr(f"{root}/models/nemotron", dtype, thr)
man = sorted(read_jsonl(f"{root}/samples/{st}/manifest.jsonl")[:n], key=lambda m: m["dur_s"])
aud = {m["uid"]: sf.read(f"{root}/samples/{st}/audio/{m['uid']}.flac", dtype="float32")[0] for m in man}
res = {}
MODES_ = sys.argv[6].split(",") if len(sys.argv) > 6 else ["s560", "s160", "offline"]
for mode, k in [(m_, {"s560": 6, "s160": 1, "offline": None}[m_]) for m_ in MODES_]:
    t1 = time.time(); single = {}
    for m in man:
        single[m["uid"]] = (asr_offline(proc, model, aud[m["uid"]]) if k is None else asr_streaming(proc, model, aud[m["uid"]], k, "flush"))["text"]
    t1 = time.time() - t1; t2 = time.time(); batch = {}
    for i in range(0, len(man), B):
        ms = man[i:i + B]
        r = asr_offline_batch(proc, model, [aud[m["uid"]] for m in ms]) if k is None else asr_streaming_batch(proc, model, [aud[m["uid"]] for m in ms], k)
        for m, t in zip(ms, r["texts"]): batch[m["uid"]] = t
    t2 = time.time() - t2
    same = sum(norm_text(single[u]) == norm_text(batch[u]) for u in single)
    e1 = sum(word_errors(m["ref_norm"], norm_text(single[m["uid"]]))[0] for m in man); e2 = sum(word_errors(m["ref_norm"], norm_text(batch[m["uid"]]))[0] for m in man)
    nw = sum(word_errors(m["ref_norm"], "")[1] for m in man)
    res[mode] = {"n": len(man), "identical_after_norm": same, "wer_single": round(100 * e1 / nw, 2), "wer_batch": round(100 * e2 / nw, 2), "sec_single": round(t1, 1), "sec_batch": round(t2, 1)}
    print(mode, res[mode], flush=True)
