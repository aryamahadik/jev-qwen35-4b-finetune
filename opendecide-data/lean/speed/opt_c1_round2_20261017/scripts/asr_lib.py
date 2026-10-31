"""Nemotron Speech Streaming EN 0.6B through HF transformers (>=5.13), CPU. Streaming loop = the model card's recipe
(oc1/voice.py asr_streaming of the 17 Oct harness), plus an explicit end-of-input flush (zero-pad the last real chunk, then ONE
silent chunk so the right-context frames of the last words are emitted). tail='drop' reproduces the card loop exactly (a final
partial chunk is dropped)."""
import time
import numpy as np
import torch

REPO = "nvidia/nemotron-speech-streaming-en-0.6b"
MODES = {"s160": 1, "s560": 6, "s1120": 13}
CHUNK_S = {"s160": 0.16, "s560": 0.56, "s1120": 1.12}

def load_asr(path, dtype="fp32", threads=None):
    from transformers import AutoModelForRNNT, AutoProcessor
    if threads:
        torch.set_num_threads(int(threads))
    proc = AutoProcessor.from_pretrained(path)
    model = AutoModelForRNNT.from_pretrained(path, dtype=torch.bfloat16 if dtype == "bf16" else torch.float32)
    model.eval()
    return proc, model

def _text(x):
    if isinstance(x, (list, tuple)):
        return " ".join(str(t) for t in x).strip()
    return str(x).strip()

@torch.inference_mode()
def asr_offline(proc, model, audio):
    sr = proc.feature_extractor.sampling_rate
    inputs = proc(audio, sampling_rate=sr)
    inputs.to(model.device, dtype=model.dtype)
    t0 = time.perf_counter()
    out = model.generate(**inputs, return_dict_in_generate=True)
    ms = (time.perf_counter() - t0) * 1000.0
    return {"text": _text(proc.decode(out.sequences, skip_special_tokens=True)), "ms": ms}

@torch.inference_mode()
def asr_streaming(proc, model, audio, lookahead, tail="flush", record_emit=False):
    """Returns text, wall ms, per-chunk compute ms, n_chunks. tail='flush' (default) or 'drop' (model-card loop)."""
    proc.set_num_lookahead_tokens(lookahead)
    sr = proc.feature_extractor.sampling_rate
    hop, n_fft = proc.feature_extractor.hop_length, proc.feature_extractor.n_fft
    nfirst, nchunk = proc.num_samples_first_audio_chunk, proc.num_samples_per_audio_chunk
    adv = proc.num_mel_frames_per_audio_chunk * hop              # new samples per chunk
    L = len(audio)
    if tail == "flush":
        audio = np.concatenate([audio, np.zeros(nchunk + 2 * adv + nfirst, dtype=audio.dtype)])
    if len(audio) < nfirst:
        audio = np.concatenate([audio, np.zeros(nfirst - len(audio), dtype=audio.dtype)])
    first = proc(audio[:nfirst], sampling_rate=sr, is_streaming=True, is_first_audio_chunk=True,
                 return_tensors="pt").to(model.device, dtype=model.dtype)
    marks = []
    def gen():
        marks.append(time.perf_counter())
        yield first.input_features[:, : proc.num_mel_frames_first_audio_chunk, :]
        idx = proc.num_mel_frames_first_audio_chunk
        start = idx * hop - n_fft // 2
        while True:
            end = start + nchunk
            if tail == "flush":
                if idx * hop >= L + adv or end > len(audio):
                    break
            elif not (end < len(audio)):
                break
            x = proc(audio[start:end], sampling_rate=sr, is_streaming=True, is_first_audio_chunk=False,
                     return_tensors="pt").to(model.device, dtype=model.dtype)
            marks.append(time.perf_counter())
            yield x.input_features
            idx += proc.num_mel_frames_per_audio_chunk
            start = idx * hop - n_fft // 2
    t0 = time.perf_counter()
    kwargs = {**first, "input_features": gen()}
    out = model.generate(**kwargs, return_dict_in_generate=True)
    t1 = time.perf_counter()
    text = _text(proc.decode(out.sequences, skip_special_tokens=True))
    m = marks + [t1]
    chunk_ms = [(m[i + 1] - m[i]) * 1000.0 for i in range(len(marks))]
    return {"text": text, "ms": (t1 - t0) * 1000.0, "chunk_ms": chunk_ms}


# ------------------------------------------------------------------ batched variants (throughput only; same model, same chunking)
@torch.inference_mode()
def asr_offline_batch(proc, model, audios):
    sr = proc.feature_extractor.sampling_rate
    inputs = proc(list(audios), sampling_rate=sr)
    inputs.to(model.device, dtype=model.dtype)
    t0 = time.perf_counter()
    out = model.generate(**inputs, return_dict_in_generate=True)
    ms = (time.perf_counter() - t0) * 1000.0
    return {"texts": [t.strip() for t in proc.batch_decode(out.sequences, skip_special_tokens=True)], "ms": ms}

@torch.inference_mode()
def asr_streaming_batch(proc, model, audios, lookahead):
    """B utterances (ideally of similar length) streamed together chunk by chunk with the flush of asr_streaming(); shorter ones are
    zero-padded to the longest (more silent chunks after their own end). Same chunk geometry per row as the batch-1 loop."""
    proc.set_num_lookahead_tokens(lookahead)
    sr = proc.feature_extractor.sampling_rate
    hop, n_fft = proc.feature_extractor.hop_length, proc.feature_extractor.n_fft
    nfirst, nchunk = proc.num_samples_first_audio_chunk, proc.num_samples_per_audio_chunk
    adv = proc.num_mel_frames_per_audio_chunk * hop
    Lmax = max(len(a) for a in audios)
    pad = nchunk + 2 * adv + nfirst
    X = [np.concatenate([a, np.zeros(Lmax - len(a) + pad, dtype=a.dtype)]) for a in audios]
    first = proc([x[:nfirst] for x in X], sampling_rate=sr, is_streaming=True, is_first_audio_chunk=True,
                 return_tensors="pt").to(model.device, dtype=model.dtype)
    def gen():
        yield first.input_features[:, : proc.num_mel_frames_first_audio_chunk, :]
        idx = proc.num_mel_frames_first_audio_chunk
        start = idx * hop - n_fft // 2
        while True:
            end = start + nchunk
            if idx * hop >= Lmax + adv or end > len(X[0]):
                break
            x = proc([xi[start:end] for xi in X], sampling_rate=sr, is_streaming=True, is_first_audio_chunk=False,
                     return_tensors="pt").to(model.device, dtype=model.dtype)
            yield x.input_features
            idx += proc.num_mel_frames_per_audio_chunk
            start = idx * hop - n_fft // 2
    t0 = time.perf_counter()
    out = model.generate(**{**first, "input_features": gen()}, return_dict_in_generate=True)
    ms = (time.perf_counter() - t0) * 1000.0
    return {"texts": [t.strip() for t in proc.batch_decode(out.sequences, skip_special_tokens=True)], "ms": ms}
