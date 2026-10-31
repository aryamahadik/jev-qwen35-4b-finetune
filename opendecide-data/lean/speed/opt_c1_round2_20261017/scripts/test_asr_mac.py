import sys, os, json, time
sys.path.insert(0, os.path.dirname(__file__))
import soundfile as sf, numpy as np, torch
from asr_lib import *
from r2common import *
A = os.path.join(os.path.dirname(__file__), "..", "assets")
proc, model = load_asr(f"{A}/models/nemotron", "fp32", 6)
man = read_jsonl(f"{A}/samples/tedlium/manifest.jsonl")[:6]
for m in man:
    x, sr = sf.read(f"{A}/samples/tedlium/audio/{m['uid']}.flac", dtype="float32")
    ref = m["ref_norm"]
    res = {}
    res["off"] = asr_offline(proc, model, x)
    for name, k, tail in [("s560f", 6, "flush"), ("s560d", 6, "drop"), ("s160f", 1, "flush")]:
        res[name] = asr_streaming(proc, model, x, k, tail)
    print(m["uid"], round(m["dur_s"], 1), "s", {k: (round(corpus_wer([(ref, norm_text(v["text"]))]) * 100, 1), round(v["ms"] / 1000 / m["dur_s"], 2)) for k, v in res.items()}, flush=True)
