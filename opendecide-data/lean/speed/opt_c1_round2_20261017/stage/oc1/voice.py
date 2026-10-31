"""oc1.voice: spoken decision prompts -> ASR transcript -> C1, with the latency breakdown.

Pipeline (the "voice attach test"):
  1. ~100 short DEV decision states (SPEED-2's parity set P, <= ~240 characters) are synthesised with Kokoro-82M
     (Apache-2.0, `kokoro` 0.9.4, voice af_heart, 24 kHz -> resampled to 16 kHz).
  2. NVIDIA Nemotron ASR Streaming 0.6B (nvidia/nemotron-speech-streaming-en-0.6b, NVIDIA Open Model License, cache-aware
     FastConformer-RNNT, runs in HF transformers >= 5.13 as AutoModelForRNNT) transcribes each utterance
        * streaming with 0.16 s chunks (processor.set_num_lookahead_tokens(1)) and 0.56 s chunks (lookahead 6),
        * offline (whole utterance) as the reference.
     Fallback if that model cannot load: Parakeet TDT 0.6B v3 offline (nvidia/parakeet-tdt-0.6b-v3, CC-BY-4.0).
  3. The transcript replaces the state in the SAME question (instructions / options / card unchanged); C1 reads both and
     the argmax agreement + mean |dp| vs the text prompt are reported (oc1.runner voice_c1). Gold labels are not used.

Latency model (stated, not hidden): audio reaches the recogniser in real time, chunk by chunk. For each streaming mode the
per-chunk compute time is MEASURED on the GPU (generator pulls timestamp the model's work); with a forced flush at the
end of speech the ASR-final latency is the compute of the last chunk plus the finaliser. Without a flush the tail waits
for up to one more chunk (reported as +chunk/2 on average). End-pointing (Silero VAD hold + Smart Turn) is NOT measured here.
Pure helpers (WER, prompt picking, latency algebra) are CPU-tested; the model code runs in the voice image only.
"""
from __future__ import annotations

import json
import math
import random
import re
import time
from pathlib import Path

from . import common as C

KOKORO_VOICE = "af_heart"
NEMOTRON = "nvidia/nemotron-speech-streaming-en-0.6b"
PARAKEET = "nvidia/parakeet-tdt-0.6b-v3"
MODES = {"stream160": 1, "stream560": 6}          # name -> processor.set_num_lookahead_tokens(k)
CHUNK_S = {"stream160": 0.16, "stream560": 0.56}
MAX_STATE_CHARS = 240
MIN_STATE_CHARS = 40


# ---------------------------------------------------------------- picking the prompts (laptop, CPU)
def clean_state(s: str) -> str:
    """What gets spoken: the state's text without header lines like 'Message:' and with whitespace collapsed."""
    t = re.sub(r"\s+", " ", s).strip()
    t = re.sub(r"^(Message|Text|Statement|Review|Post|Claim|Ticket|Email|Comment|Sentence):\s*", "", t, flags=re.I)
    return t


def speakable(s: str) -> bool:
    t = clean_state(s)
    if not (MIN_STATE_CHARS <= len(t) <= MAX_STATE_CHARS):
        return False
    if re.search(r"https?://|www\.|@\w+\.|[{}<>\\|#*_=~^`$%]", t):
        return False
    letters = sum(c.isalpha() or c == " " for c in t)
    return letters / len(t) >= 0.9 and bool(re.search(r"[A-Za-z]{3}", t))


def pick_prompts(items: list, n: int = 100, seed: int = 0) -> list:
    """items = workload P items. Half yes/no, half choice (up to 9 options), deterministic. Returns
    [{"id", "text" (spoken), "request" (the full API v1 request with the ORIGINAL state), "qtype"}]."""
    rng = random.Random(seed)
    ok = []
    for it in items:
        q = next(iter(it["request"]["questions"].values()))
        if not speakable(it["request"]["state"]):
            continue
        if q["type"] == "choice" and len(q.get("options") or []) > 9:
            continue
        ok.append(it)
    yn = [it for it in ok if it["qtype"] == "noul"]
    ch = [it for it in ok if it["qtype"] == "choice"]
    rng.shuffle(yn)
    rng.shuffle(ch)
    take = yn[: n // 2] + ch[: n - n // 2]
    rng.shuffle(take)
    return [{"id": it["id"], "qtype": it["qtype"], "text": clean_state(it["request"]["state"]), "request": it["request"]}
            for it in take[:n]]


def with_state(request: dict, state: str) -> dict:
    return {**request, "state": state}


# ---------------------------------------------------------------- scoring helpers (pure)
def norm_words(s: str) -> list:
    s = s.lower().replace("-", " ")
    s = re.sub(r"[^a-z0-9' ]", " ", s)
    return s.split()


def wer(ref: str, hyp: str) -> float:
    r, h = norm_words(ref), norm_words(hyp)
    if not r:
        return 0.0 if not h else 1.0
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            cur = d[j]
            d[j] = min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
            prev = cur
    return d[len(h)] / len(r)


def streaming_latency(chunk_ms: list, audio_s: float, chunk_s: float, flush_ms: float) -> dict:
    """Latency algebra for a real-time source. chunk_ms[i] = measured compute of chunk i (arrives at (i+1)*chunk_s).
    Returns the time from end of speech to the final transcript with a forced flush (final_flush_ms), and the extra
    wait when the tail must first fill a whole chunk (expected_unflushed_ms = final + chunk/2 on average)."""
    t_free, arrivals = 0.0, []
    for i, c in enumerate(chunk_ms):
        arr = (i + 1) * chunk_s
        start = max(arr, t_free)
        t_free = start + c / 1000.0
        arrivals.append(arr)
    end_of_speech = audio_s
    final = max(t_free, end_of_speech) + flush_ms / 1000.0
    return {"final_flush_ms": round((final - end_of_speech) * 1000.0, 1),
            "expected_unflushed_ms": round((final - end_of_speech) * 1000.0 + chunk_s * 500.0, 1),
            "backlog_ms": round(max(0.0, t_free - arrivals[-1]) * 1000.0, 1) if arrivals else 0.0,
            "n_chunks": len(chunk_ms)}


# ---------------------------------------------------------------- model code (voice image: torch, transformers>=5.13, kokoro)
def load_tts():
    from kokoro import KPipeline
    return KPipeline(lang_code="a")


def synth_one(pipe, text: str, voice: str = KOKORO_VOICE):
    """-> (float32 mono numpy at 16 kHz, seconds of audio, synthesis seconds)."""
    import numpy as np
    from scipy.signal import resample_poly
    t0 = time.perf_counter()
    chunks = [a.detach().cpu().numpy() if hasattr(a, "detach") else np.asarray(a) for _, _, a in pipe(text, voice=voice, speed=1.0)]
    x = np.concatenate(chunks).astype("float32") if chunks else np.zeros(1600, "float32")
    x16 = resample_poly(x, 2, 3).astype("float32")      # 24 kHz -> 16 kHz
    return x16, len(x16) / 16000.0, time.perf_counter() - t0


def load_asr(repo: str = NEMOTRON, device: str = "cuda"):
    import torch
    from transformers import AutoModelForRNNT, AutoProcessor
    proc = AutoProcessor.from_pretrained(repo)
    model = AutoModelForRNNT.from_pretrained(repo)      # no device_map: it needs `accelerate`, which the voice image does not carry
    model = model.to(device)
    model.eval()
    return proc, model


def _sync(device):
    if device != "cpu":
        import torch
        torch.cuda.synchronize()


def _text(x) -> str:
    """processor.decode of a [1, T] batch returns a list of strings (the model card prints it as is)."""
    if isinstance(x, (list, tuple)):
        return " ".join(str(t) for t in x).strip()
    return str(x).strip()


def asr_offline(proc, model, audio, device: str = "cuda") -> dict:
    sr = proc.feature_extractor.sampling_rate
    inputs = proc(audio, sampling_rate=sr)
    inputs.to(model.device, dtype=model.dtype)
    _sync(device)
    t0 = time.perf_counter()
    out = model.generate(**inputs, return_dict_in_generate=True)
    _sync(device)
    ms = (time.perf_counter() - t0) * 1000.0
    return {"text": _text(proc.decode(out.sequences, skip_special_tokens=True)), "ms": ms}


def asr_streaming(proc, model, audio, lookahead: int, device: str = "cuda") -> dict:
    """The model card's streaming recipe, with timestamps on every chunk the generator hands to the model."""
    proc.set_num_lookahead_tokens(lookahead)
    sr = proc.feature_extractor.sampling_rate
    first = proc(audio[: proc.num_samples_first_audio_chunk], sampling_rate=sr, is_streaming=True,
                 is_first_audio_chunk=True, return_tensors="pt").to(model.device, dtype=model.dtype)
    pulls = []

    def gen():
        pulls.append(time.perf_counter())
        yield first.input_features[:, : proc.num_mel_frames_first_audio_chunk, :]
        idx = proc.num_mel_frames_first_audio_chunk
        hop, n_fft = proc.feature_extractor.hop_length, proc.feature_extractor.n_fft
        start = idx * hop - n_fft // 2
        while (end := start + proc.num_samples_per_audio_chunk) < audio.shape[0]:
            x = proc(audio[start:end], sampling_rate=sr, is_streaming=True, is_first_audio_chunk=False,
                     return_tensors="pt").to(model.device, dtype=model.dtype)
            pulls.append(time.perf_counter())
            yield x.input_features
            idx += proc.num_mel_frames_per_audio_chunk
            start = idx * hop - n_fft // 2

    _sync(device)
    t0 = time.perf_counter()
    kwargs = {**first, "input_features": gen()}          # as the model card: the generator REPLACES the first chunk's features
    out = model.generate(**kwargs, return_dict_in_generate=True)
    _sync(device)
    t1 = time.perf_counter()
    text = _text(proc.decode(out.sequences, skip_special_tokens=True))
    # compute of chunk i = from its pull to the next pull (the last: to the end of generate)
    marks = pulls + [t1]
    chunk_ms = [(marks[i + 1] - marks[i]) * 1000.0 for i in range(len(pulls))]
    return {"text": text, "total_ms": (t1 - t0) * 1000.0, "chunk_ms": chunk_ms,
            "streaming_latency_ms": getattr(proc, "streaming_latency_ms", None)}


def run_voice(spec: dict, log=print) -> dict:
    """spec: prompts (list from pick_prompts), device, repo, out_dir. Returns transcripts + latency stats per mode."""
    device = spec.get("device", "cuda")
    prompts = spec["prompts"]
    t0 = time.time()
    tts = load_tts()
    audios, tts_s, aud_s = [], [], []
    for p in prompts:
        x, dur, ts = synth_one(tts, p["text"])
        audios.append(x)
        tts_s.append(ts)
        aud_s.append(dur)
    log(f"tts: {len(audios)} utterances, {sum(aud_s):.0f} s of audio in {sum(tts_s):.1f} s")
    del tts
    repo = spec.get("repo", NEMOTRON)
    proc, model = load_asr(repo, device)
    # warm the model (kernels, caches) on the first utterance
    for _ in range(2):
        asr_offline(proc, model, audios[0], device)
        for k in MODES.values():
            asr_streaming(proc, model, audios[0], k, device)
    res = {"repo": repo, "device": device, "n": len(prompts), "audio_s": C.summarize(aud_s), "tts_s": C.summarize(tts_s),
           "tts_rtf": round(sum(tts_s) / max(sum(aud_s), 1e-9), 4), "modes": {}, "items": []}
    per = [{"id": p["id"], "text": p["text"], "audio_s": a} for p, a in zip(prompts, aud_s)]
    modes = {"offline": None, **{m: k for m, k in MODES.items()}}
    for mode, k in modes.items():
        wers, finals, unfl, chunk_all, tot = [], [], [], [], []
        for i, (p, x) in enumerate(zip(prompts, audios)):
            if k is None:
                r = asr_offline(proc, model, x, device)
                per[i]["offline"] = {"text": r["text"], "ms": round(r["ms"], 1)}
                tot.append(r["ms"])
                hyp = r["text"]
            else:
                r = asr_streaming(proc, model, x, k, device)
                lat = streaming_latency(r["chunk_ms"][:-1] or r["chunk_ms"], aud_s[i], CHUNK_S[mode], r["chunk_ms"][-1])
                per[i][mode] = {"text": r["text"], "total_ms": round(r["total_ms"], 1), **lat,
                                "chunk_ms_p50": round(C.pct(r["chunk_ms"], 0.5), 2)}
                finals.append(lat["final_flush_ms"])
                unfl.append(lat["expected_unflushed_ms"])
                chunk_all += r["chunk_ms"]
                tot.append(r["total_ms"])
                hyp = r["text"]
            wers.append(wer(p["text"], hyp))
        res["modes"][mode] = {"wer_mean": round(sum(wers) / len(wers), 4), "wer_p90": round(C.pct(wers, 0.9), 4),
                              "exact_after_norm": round(sum(w == 0 for w in wers) / len(wers), 4),
                              "total_ms": C.summarize(tot)}
        if k is not None:
            res["modes"][mode].update({"chunk_ms": C.summarize(chunk_all), "final_flush_ms": C.summarize(finals),
                                       "expected_unflushed_ms": C.summarize(unfl), "chunk_s": CHUNK_S[mode],
                                       "streaming_latency_ms_model": r.get("streaming_latency_ms")})
        log(f"asr {mode}: WER {res['modes'][mode]['wer_mean']:.3f}")
    res["items"] = per
    res["wall_s"] = round(time.time() - t0, 1)
    return res
