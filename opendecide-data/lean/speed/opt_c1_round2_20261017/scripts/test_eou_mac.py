import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import soundfile as sf, numpy as np, torch
from eot_lib import *
from r2common import *
A = os.path.join(os.path.dirname(__file__), "..", "assets")
e = ParakeetEOU(f"{A}/models/parakeet_eou_hf", threads=4)
man = read_jsonl(f"{A}/samples/slurp/manifest.jsonl")[:3]
import sentencepiece as spm
sp = spm.SentencePieceProcessor(model_file=[os.path.join(A, "..", "work/eou_nemo", f) for f in os.listdir(os.path.join(A, "..", "work/eou_nemo")) if f.endswith("tokenizer.model")][0])
for m in man:
    x, sr = sf.read(f"{A}/samples/slurp/audio/{m['uid']}.flac", dtype="float32")
    x = np.concatenate([x, room_tone_tail(x, 2.0, 0)])
    r = e.run(x)
    print(m["ref"], "|", len(r["seq"]), r["seq"][:40], r["dur"] and r["dur"][:40])
    ids = [t for t in r["seq"] if t < 1024]
    print(sp.decode(ids), "| chunks", len(r["chunk_ms"]), "p50 ms", np.median(r["chunk_ms"]))
