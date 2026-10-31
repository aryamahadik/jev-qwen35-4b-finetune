"""od-cpu1: end-of-turn test. Per utterance: forced alignment (reference speech end), stream = clip + 2.5 s room-tone tail,
(a) Silero VAD + Smart Turn v3.2 (several stop_secs), (b) Parakeet Realtime EOU 120M. CPU only. Writes per-utterance numbers.
usage: eot_run.py --set slurp|ami [--shard i/k] [--n 500] [--threads 1]"""
import argparse, os, sys, json, time, zlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("--set", required=True); ap.add_argument("--shard", default="0/1"); ap.add_argument("--n", type=int, default=500)
ap.add_argument("--threads", type=int, default=1); ap.add_argument("--root", default=os.path.expanduser("~/opt_r2/voice"))
ap.add_argument("--tail", type=float, default=2.5)
a = ap.parse_args()
import soundfile as sf, numpy as np, torch
from eot_lib import *
from r2common import read_jsonl
si, sk = map(int, a.shard.split("/"))
man = read_jsonl(f"{a.root}/samples/{a.set}/manifest.jsonl")[: a.n]
man = [m for j, m in enumerate(man) if j % sk == si]
out = f"{a.root}/out/eot_{a.set}.shard{si}of{sk}.jsonl"
done = {json.loads(l)["uid"] for l in open(out)} if os.path.exists(out) else set()
torch.set_num_threads(a.threads)
fa_proc, fa_model = load_w2v2(f"{a.root}/models/w2v2")
sil = SileroST(f"{a.root}/models/st/silero_vad.onnx", f"{a.root}/models/st/smart-turn-v3.2-cpu.onnx", threads=a.threads)
eou = ParakeetEOU(f"{a.root}/models/parakeet_eou_hf", threads=a.threads)
CFG = [("st", 0.2), ("st", 0.3), ("st", 0.5), ("vad", 0.2), ("vad", 0.5), ("vad", 0.8)]
# warm up
w = np.random.default_rng(0).standard_normal(16000 * 3).astype("float32") * 0.01
sil.vad_probs(w); sil.smart_turn(w); eou.run(w)
f = open(out, "a"); t0 = time.time(); n = 0
for m in man:
    if m["uid"] in done: continue
    x, sr = sf.read(f"{a.root}/samples/{a.set}/audio/{m['uid']}.flac", dtype="float32")
    rec = {"uid": m["uid"], "dur_s": len(x) / SR}
    with torch.inference_mode():
        fa = align_words(fa_proc, fa_model, x, m["ref"])
    if fa is None:
        rec["fa_ok"] = False; f.write(json.dumps(rec) + "\n"); f.flush(); continue
    rec["fa_ok"] = True; rec.update(fa)
    for tk in ("noise", "zero"):
        tail = room_tone_tail(x, a.tail, zlib.crc32(m["uid"].encode())) if tk == "noise" else np.zeros(int(a.tail * SR), "float32")
        s = np.concatenate([x, tail]).astype("float32")
        R = {}
        probs, vms = sil.vad_probs(s)
        R["vad_ms_p50"] = float(np.median(vms)); R["vad_ms_mean"] = float(np.mean(vms))
        for kind, stop in CFG:
            d = sil.detect(s, probs, stop_secs=stop, use_st=(kind == "st"))
            R[f"{kind}_{stop}"] = {"t": d["t"], "mode": d["mode"], "n_st": d["n_st"], "st_p": [round(c["p"], 4) for c in d["st_calls"]],
                                   "st_fe_ms": [round(c["fe_ms"], 2) for c in d["st_calls"]], "st_ort_ms": [round(c["ort_ms"], 2) for c in d["st_calls"]],
                                   "speech_start": d["speech_start"]}
        r = eou.run(s)
        seq, dur = r["seq"], r["dur"]
        frames = np.cumsum(dur) - np.array(dur) if dur is not None else None
        eou_steps = [i for i, t in enumerate(seq) if t == eou.eou_id]
        ends, cms = r["chunk_end_s"], r["chunk_ms"]
        tdone = []; tp = 0.0
        for e, c in zip(ends, cms):
            tp = max(e, tp) + c / 1000.0; tdone.append(tp)
        def tof(step):
            j = min(int(frames[step]) // 2, len(ends) - 1)
            return ends[j], tdone[j], j
        R["eou"] = {"n_eou": len(eou_steps), "frames_total": int(sum(dur)) if dur else None, "n_chunks": len(ends)}
        if eou_steps:
            ta, tc, j = tof(eou_steps[0]); R["eou"].update({"t_alg": ta, "t_cpu": tc, "chunk": j})
            R["eou"]["all_t_alg"] = [tof(i)[0] for i in eou_steps[:5]]
        R["eou"]["chunk_ms_p50"] = float(np.median(cms)); R["eou"]["chunk_ms_p95"] = float(np.percentile(cms, 95)); R["eou"]["chunk_ms_max"] = float(np.max(cms))
        rec[tk] = R
    f.write(json.dumps(rec) + "\n"); f.flush(); n += 1
    if n % 20 == 0: print(f"{a.set} shard {si}: {n} done, {time.time()-t0:.0f}s", flush=True)
print("finished", n, round(time.time() - t0), "s", flush=True)
