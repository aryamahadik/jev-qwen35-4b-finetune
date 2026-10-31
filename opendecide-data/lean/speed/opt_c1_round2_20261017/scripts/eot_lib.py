"""End-of-turn detectors on a stream: (a) Silero VAD (silence trigger) + Smart Turn v3.2 confirm, (b) Parakeet Realtime EOU 120M.
All CPU. Times are stream times (seconds from the first sample) unless named *_cpu (include measured CPU compute)."""
import os, re, time, math
import numpy as np
import torch

SR = 16000
# ------------------------------------------------------------------ forced alignment (CTC Viterbi on wav2vec2-base-960h)
def load_w2v2(path):
    from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
    p = Wav2Vec2Processor.from_pretrained(path); m = Wav2Vec2ForCTC.from_pretrained(path).eval()
    return p, m

def _ctc_viterbi(logp, tok):
    T, V = logp.shape; L = len(tok); S = 2 * L + 1
    ext = np.zeros(S, int); ext[1::2] = tok
    NEG = -1e30
    dp = np.full((T, S), NEG); bp = np.zeros((T, S), np.int8)
    dp[0, 0] = logp[0, 0]
    if S > 1: dp[0, 1] = logp[0, ext[1]]
    can_skip = np.zeros(S, bool)
    for s in range(3, S, 2):
        can_skip[s] = ext[s] != ext[s - 2]
    for t in range(1, T):
        prev = dp[t - 1]
        c0 = prev
        c1 = np.concatenate([[NEG], prev[:-1]])
        c2 = np.concatenate([[NEG, NEG], prev[:-2]]); c2 = np.where(can_skip, c2, NEG)
        st = np.stack([c0, c1, c2]); k = st.argmax(0)
        dp[t] = st[k, np.arange(S)] + logp[t, ext]; bp[t] = k
    s = S - 1 if S == 1 or dp[T - 1, S - 1] >= dp[T - 1, S - 2] else S - 2
    path = np.zeros(T, int)
    for t in range(T - 1, -1, -1):
        path[t] = s; s = s - int(bp[t, s])
    return path, ext

@torch.inference_mode()
def align_words(proc, model, audio, text):
    """-> dict(first_word_start, last_word_start, last_word_end, n_words) in seconds, or None if infeasible."""
    vocab = proc.tokenizer.get_vocab()
    words = [re.sub(r"[^A-Z']", "", w.upper()) for w in text.split()]
    words = [w for w in words if w]
    if not words: return None
    chars = []; widx = []
    for i, w in enumerate(words):
        for ch in w: chars.append(vocab[ch]); widx.append(i)
        if i < len(words) - 1: chars.append(vocab["|"]); widx.append(-1)
    inp = proc(audio, sampling_rate=SR, return_tensors="pt")
    lg = model(inp.input_values).logits[0]
    logp = torch.log_softmax(lg, -1).numpy()
    T = len(logp)
    if T < len(chars) + 1: return None
    path, ext = _ctc_viterbi(logp, np.array(chars))
    # frames where the path is on a real char state (odd s) -> char index (s-1)//2
    cs = {}
    for t, s in enumerate(path):
        if s % 2 == 1:
            ci = (s - 1) // 2
            if widx[ci] >= 0: cs.setdefault(widx[ci], []).append(t)
    if len(cs) < len(words): return None
    fr = 0.02  # wav2vec2 stride 20 ms
    first = cs[0][0] * fr; ls = cs[len(words) - 1][0] * fr; le = (cs[len(words) - 1][-1] + 1) * fr
    return {"first_word_start": first, "last_word_start": ls, "last_word_end": min(le, len(audio) / SR), "n_words": len(words)}

# ------------------------------------------------------------------ stream builder
def room_tone_tail(audio, seconds, seed):
    """Gaussian noise at the clip's noise floor (10th percentile of 20 ms frame RMS, min 1e-4)."""
    fr = 320; n = len(audio) // fr
    rms = np.sqrt((audio[: n * fr].reshape(n, fr) ** 2).mean(1)) if n else np.array([1e-3])
    lvl = max(float(np.percentile(rms, 10)), 1e-4)
    rng = np.random.default_rng(seed)
    return (rng.standard_normal(int(seconds * SR)) * lvl).astype("float32")

# ------------------------------------------------------------------ (a) Silero VAD + Smart Turn v3.2
class SileroST:
    def __init__(self, silero_onnx, st_onnx, threads=1):
        import onnxruntime as ort
        from silero_vad.utils_vad import OnnxWrapper
        from transformers import WhisperFeatureExtractor
        torch.set_num_threads(threads)
        self.vad = OnnxWrapper(silero_onnx, force_onnx_cpu=True)
        so = ort.SessionOptions(); so.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
        so.inter_op_num_threads = 1; so.intra_op_num_threads = threads; so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.st = ort.InferenceSession(st_onnx, sess_options=so)
        self.fe = WhisperFeatureExtractor(chunk_length=8)

    def vad_probs(self, x):
        """Silero v5/6 speech probability per 512-sample window (32 ms). Returns (probs, ms per window list)."""
        self.vad.reset_states()
        n = len(x) // 512; probs = np.zeros(n); ms = []
        xt = torch.from_numpy(x[: n * 512]).view(n, 512)
        for i in range(n):
            t0 = time.perf_counter(); probs[i] = float(self.vad(xt[i:i + 1], SR)[0, 0]); ms.append((time.perf_counter() - t0) * 1000)
        return probs, ms

    def smart_turn(self, audio):
        from_end = audio[-8 * SR:]
        if len(from_end) < 8 * SR: from_end = np.pad(from_end, (8 * SR - len(from_end), 0))
        t0 = time.perf_counter()
        f = self.fe(from_end, sampling_rate=SR, return_tensors="np", padding="max_length", max_length=8 * SR, truncation=True, do_normalize=True)
        feat = f.input_features.astype(np.float32)
        t1 = time.perf_counter()
        p = float(self.st.run(None, {"input_features": feat})[0].reshape(-1)[0])
        t2 = time.perf_counter()
        return p, (t1 - t0) * 1000, (t2 - t1) * 1000

    def detect(self, x, probs, stop_secs=0.2, thr=0.5, start_secs=0.2, fallback_secs=3.0, use_st=True):
        """Pipecat-style: VAD state machine; at each VAD stop (stop_secs of silence) run Smart Turn on the audio since speech start;
        complete (p>0.5) -> end of turn; incomplete -> keep listening, fire anyway after fallback_secs of silence.
        use_st=False: VAD only (fires at every VAD stop). Returns dict with stream times (s)."""
        W = 512 / SR; sf = int(math.ceil(start_secs / W)); ef = int(math.ceil(stop_secs / W))
        spk = probs >= thr
        state = "quiet"; run_s = 0; run_q = 0; speech_start = None; last_speech_end = None
        st_calls = []; n = len(probs)
        for i in range(n):
            if spk[i]:
                run_s += 1; run_q = 0
                if state == "quiet" and run_s >= sf:
                    state = "speaking"
                    if speech_start is None: speech_start = (i - sf + 1) * W
                if state == "speaking": last_speech_end = (i + 1) * W
            else:
                run_q += 1; run_s = 0
                if state == "speaking":
                    sil = run_q * W
                    if not use_st:
                        if run_q >= ef: return {"t": (i + 1) * W, "mode": "vad", "n_st": 0, "st_calls": st_calls, "speech_start": speech_start}
                    else:
                        if run_q == ef:   # VAD stop event -> Smart Turn on audio since speech start
                            buf = x[int(speech_start * SR): int((i + 1) * W * SR)]
                            p, fe_ms, ort_ms = self.smart_turn(buf)
                            st_calls.append({"t": (i + 1) * W, "p": p, "fe_ms": fe_ms, "ort_ms": ort_ms})
                            if p > 0.5:
                                return {"t": (i + 1) * W, "mode": "smart_turn", "n_st": len(st_calls), "st_calls": st_calls, "speech_start": speech_start}
                        if sil >= fallback_secs:
                            return {"t": (i + 1) * W, "mode": "fallback", "n_st": len(st_calls), "st_calls": st_calls, "speech_start": speech_start}
                    # speech resumes -> state stays "speaking" (new run), handled above
                if state == "speaking" and run_q == 0: pass
        return {"t": None, "mode": "none", "n_st": len(st_calls), "st_calls": st_calls, "speech_start": speech_start}

# ------------------------------------------------------------------ (b) Parakeet Realtime EOU 120M (HF-converted)
class ParakeetEOU:
    def __init__(self, path, threads=1, eou_id=1024, lookahead=1):
        from transformers import AutoModelForRNNT
        from transformers.models.nemotron_asr_streaming.feature_extraction_nemotron_asr_streaming import NemotronAsrStreamingFeatureExtractor
        torch.set_num_threads(threads)
        self.fe = NemotronAsrStreamingFeatureExtractor.from_pretrained(path)
        self.model = AutoModelForRNNT.from_pretrained(path, dtype=torch.float32).eval()
        self.eou_id = eou_id; self.k = lookahead
        S = 8; self.nmel_first = 1 + S * self.k; self.nmel = S * (self.k + 1)
        hop, win = self.fe.hop_length, self.fe.win_length
        self.hop, self.nfft = hop, self.fe.n_fft
        self.nfirst = (self.nmel_first - 1) * hop + win // 2
        self.nchunk = self.nmel * hop + win
        self.adv = self.nmel * hop

    @torch.inference_mode()
    def run(self, x, stop_at_eou=True):
        """Stream x (float32 16k). Returns dict: tokens (ids), frames (encoder frame idx per token), eou_frame, chunk_end_s[], chunk_ms[]."""
        fe = self.fe
        xs = np.concatenate([x, np.zeros(self.nchunk, "float32")])
        first = fe(xs[: self.nfirst], sampling_rate=SR, return_tensors="pt", center=True)
        ends = [self.nfirst / SR]; marks = []
        def gen():
            marks.append(time.perf_counter())
            yield first.input_features[:, : self.nmel_first, :].to(self.model.dtype)
            idx = self.nmel_first; start = idx * self.hop - self.nfft // 2
            while start + self.nchunk <= len(xs) and start < len(x):
                f = fe(xs[start: start + self.nchunk], sampling_rate=SR, return_tensors="pt", center=False)
                marks.append(time.perf_counter()); ends.append((start + self.nchunk) / SR)
                yield f.input_features.to(self.model.dtype)
                idx += self.nmel; start = idx * self.hop - self.nfft // 2
        kw = {"input_features": gen(), "num_lookahead_tokens": self.k, "return_dict_in_generate": True}
        t0 = time.perf_counter()
        out = self.model.generate(**kw)
        t1 = time.perf_counter()
        seq = out.sequences[0].tolist(); dur = out.durations[0].tolist() if getattr(out, "durations", None) is not None else None
        m = marks + [t1]; chunk_ms = [(m[i + 1] - m[i]) * 1000 for i in range(len(marks))]
        return {"seq": seq, "dur": dur, "chunk_end_s": ends, "chunk_ms": chunk_ms, "total_ms": (t1 - t0) * 1000}
