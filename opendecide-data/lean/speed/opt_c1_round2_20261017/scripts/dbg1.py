import sys, os, time
sys.path.insert(0, os.path.dirname(__file__))
import soundfile as sf
from asr_lib import *
from r2common import *
A = os.path.join(os.path.dirname(__file__), "..", "assets")
t=time.time(); proc, model = load_asr(f"{A}/models/nemotron", "fp32", 4); print("load", time.time()-t, flush=True)
man = read_jsonl(f"{A}/samples/tedlium/manifest.jsonl")
m=min(man,key=lambda m:m["dur_s"])
x, sr = sf.read(f"{A}/samples/tedlium/audio/{m['uid']}.flac", dtype="float32"); print(m["dur_s"], flush=True)
t=time.time(); r=asr_offline(proc, model, x); print("offline", r["text"], time.time()-t, flush=True)
t=time.time(); r=asr_streaming(proc, model, x, 6, "flush"); print("s560", r["text"], time.time()-t, len(r["chunk_ms"]), flush=True)
