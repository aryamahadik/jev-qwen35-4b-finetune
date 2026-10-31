import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import soundfile as sf, numpy as np, torch
from asr_lib import *
from r2common import *
root = os.path.expanduser("~/opt_r2/voice"); st = sys.argv[1]; dtype = sys.argv[2]; thr = int(sys.argv[3]); n = int(sys.argv[4])
proc, model = load_asr(f"{root}/models/nemotron", dtype, thr)
man = read_jsonl(f"{root}/samples/{st}/manifest.jsonl")[:n]
tot = {}; 
for m in man:
    x, sr = sf.read(f"{root}/samples/{st}/audio/{m['uid']}.flac", dtype="float32")
    res = {"off": asr_offline(proc, model, x), "s560f": asr_streaming(proc, model, x, 6, "flush"), "s560d": asr_streaming(proc, model, x, 6, "drop"), "s160f": asr_streaming(proc, model, x, 1, "flush")}
    for k, v in res.items():
        e, nw = word_errors(m["ref_norm"], norm_text(v["text"])); t = tot.setdefault(k, [0, 0, 0.0]); t[0] += e; t[1] += nw; t[2] += v["ms"]
    print(m["uid"], round(m["dur_s"], 1), {k: round(v["ms"] / 1000 / m["dur_s"], 2) for k, v in res.items()}, flush=True)
print({k: {"wer": round(v[0] / v[1] * 100, 1), "rtf": round(v[2] / 1000 / sum(m["dur_s"] for m in man[:n]), 3)} for k, v in tot.items()})
