"""od-cpu1: Nemotron ASR over a sample set in one mode. Resumable (appends to out jsonl). Writes hypotheses (raw) + timing only.
usage: asr_run.py --set ls_clean --mode s560|s160|offline [--shard i/k] [--threads 2] [--dtype fp32|bf16] [--tail flush|drop] [--limit N]
"""
import argparse, os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("--set", required=True); ap.add_argument("--mode", required=True)
ap.add_argument("--root", default=os.path.expanduser("~/opt_r2/voice"))
ap.add_argument("--shard", default="0/1"); ap.add_argument("--threads", type=int, default=2)
ap.add_argument("--dtype", default="fp32"); ap.add_argument("--tail", default="flush"); ap.add_argument("--limit", type=int, default=0)
ap.add_argument("--tag", default="")
a = ap.parse_args()
import soundfile as sf, numpy as np, torch
from asr_lib import *
from r2common import read_jsonl
si, sk = map(int, a.shard.split("/"))
man = read_jsonl(f"{a.root}/samples/{a.set}/manifest.jsonl")
import zlib
man = sorted(man, key=lambda m: zlib.crc32(("asr:" + m["uid"]).encode()))   # seeded shuffle: any prefix is a random subsample
if a.limit: man = man[: a.limit]
man = [m for j, m in enumerate(man) if j % sk == si]
out = f"{a.root}/out/asr_{a.set}_{a.mode}{a.tag}.shard{si}of{sk}.jsonl"
done = {json.loads(l)["uid"] for l in open(out)} if os.path.exists(out) else set()
proc, model = load_asr(f"{a.root}/models/nemotron", a.dtype, a.threads)
print(f"{a.set} {a.mode} shard {si}/{sk}: {len(man)} utts, {len(done)} done, threads {a.threads}, {a.dtype}, tail {a.tail}", flush=True)
f = open(out, "a"); t0 = time.time(); n = 0
for m in man:
    if m["uid"] in done: continue
    x, sr = sf.read(f"{a.root}/samples/{a.set}/audio/{m['uid']}.flac", dtype="float32")
    if a.mode == "offline":
        r = asr_offline(proc, model, x); extra = {}
    else:
        r = asr_streaming(proc, model, x, MODES[a.mode], a.tail)
        extra = {"n_chunks": len(r["chunk_ms"]), "chunk_ms_p50": float(np.median(r["chunk_ms"])), "chunk_ms_max": float(np.max(r["chunk_ms"])), "last_chunk_ms": r["chunk_ms"][-1]}
    f.write(json.dumps({"uid": m["uid"], "mode": a.mode, "hyp": r["text"], "ms": round(r["ms"], 1), "dur_s": m["dur_s"], **extra}) + "\n"); f.flush()
    n += 1
    if n % 25 == 0: print(f"  {n} done, {time.time()-t0:.0f}s", flush=True)
print("finished", n, "in", round(time.time() - t0), "s", flush=True)
