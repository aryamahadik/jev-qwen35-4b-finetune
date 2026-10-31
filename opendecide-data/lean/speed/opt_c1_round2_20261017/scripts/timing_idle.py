"""od-cpu1, run on an IDLE machine: CPU compute of the end-of-turn parts and of the ASR streaming chunk (c3-standard-8, Sapphire Rapids).
usage: timing_idle.py <threads>"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import soundfile as sf, numpy as np, torch
from eot_lib import *
from asr_lib import *
from r2common import *
thr = int(sys.argv[1]); root = os.path.expanduser("~/opt_r2/voice")
torch.set_num_threads(thr)
res = {"threads": thr}
man = read_jsonl(f"{root}/samples/slurp/manifest.jsonl")[:30]
aud = [sf.read(f"{root}/samples/slurp/audio/{m['uid']}.flac", dtype="float32")[0] for m in man]
sil = SileroST(f"{root}/models/st/silero_vad.onnx", f"{root}/models/st/smart-turn-v3.2-cpu.onnx", threads=thr)
x = np.concatenate([aud[0], aud[1], aud[2], aud[3]])
sil.smart_turn(x); sil.smart_turn(x)
fe, ort = [], []
for i in range(60):
    y = np.concatenate([aud[i % 30], aud[(i + 1) % 30]])
    p, a, b = sil.smart_turn(y); fe.append(a); ort.append(b)
res["smart_turn_ms"] = {"feature_p50": round(pct(fe, .5), 1), "onnx_p50": round(pct(ort, .5), 1), "total_p50": round(pct([a + b for a, b in zip(fe, ort)], .5), 1), "total_p95": round(pct([a + b for a, b in zip(fe, ort)], .95), 1)}
_, vms = sil.vad_probs(np.concatenate(aud[:10]))
res["silero_ms_per_32ms_window"] = {"p50": round(pct(vms, .5), 3), "p95": round(pct(vms, .95), 3)}
eou = ParakeetEOU(f"{root}/models/parakeet_eou_hf", threads=thr)
eou.run(np.concatenate([aud[0], np.zeros(8000, "float32")]))
cm = []
for a_ in aud[:15]:
    r = eou.run(np.concatenate([a_, np.zeros(40000, "float32")])); cm += r["chunk_ms"][1:]
res["eou_chunk_ms_160ms_chunks"] = {"p50": round(pct(cm, .5), 1), "p95": round(pct(cm, .95), 1), "max": round(max(cm), 1), "n_chunks": len(cm)}
del eou
for dtype in ("fp32", "bf16"):
    proc, model = load_asr(f"{root}/models/nemotron", dtype, thr)
    asr_streaming(proc, model, aud[0], 6, "flush")
    for name, k in (("s560", 6), ("s160", 1)):
        cms, lastc = [], []
        for a_ in aud[:12]:
            r = asr_streaming(proc, model, a_, k, "flush"); cms += r["chunk_ms"][1:-1]; lastc.append(r["chunk_ms"][-1])
        res[f"nemotron_{dtype}_{name}_chunk_ms"] = {"p50": round(pct(cms, .5), 1), "p95": round(pct(cms, .95), 1), "n": len(cms), "chunk_s": CHUNK_S[name], "last_flush_chunk_p50": round(pct(lastc, .5), 1)}
    off = [asr_offline(proc, model, a_)["ms"] for a_ in aud[:12]]
    res[f"nemotron_{dtype}_offline_ms_per_clip_p50"] = round(pct(off, .5), 1)
    res[f"nemotron_{dtype}_clip_s_p50"] = round(pct([len(a_) / 16000 for a_ in aud[:12]], .5), 2)
    del model
print(json.dumps(res, indent=1))
json.dump(res, open(f"{root}/out/timing_idle_{thr}t.json", "w"), indent=1)
