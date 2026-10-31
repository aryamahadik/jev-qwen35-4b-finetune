"""Shared helpers for the Round-2 real-audio voice tests (Mac prep + od-cpu1 runs). Counts/metrics only in outputs."""
import io, json, os, re, math, random
import numpy as np

SR = 16000

def decode_audio(a):
    """HF parquet audio struct {'bytes','path'} -> float32 mono 16 kHz."""
    import soundfile as sf
    x, sr = sf.read(io.BytesIO(a["bytes"]), dtype="float32", always_2d=False)
    if x.ndim > 1:
        x = x.mean(axis=1)
    if sr != SR:
        from scipy.signal import resample_poly
        g = math.gcd(sr, SR)
        x = resample_poly(x, SR // g, sr // g).astype("float32")
    return x

_norm = None
def normalizer():
    global _norm
    if _norm is None:
        from whisper_normalizer.english import EnglishTextNormalizer
        _norm = EnglishTextNormalizer()
    return _norm

def norm_text(s):
    return normalizer()(s)

def word_errors(ref_n, hyp_n):
    """(errors, ref_words) between two NORMALISED strings (word level Levenshtein, rapidfuzz)."""
    from rapidfuzz.distance import Levenshtein
    r, h = ref_n.split(), hyp_n.split()
    vocab = {}
    ri = [vocab.setdefault(w, len(vocab)) for w in r]
    hi = [vocab.setdefault(w, len(vocab)) for w in h]
    return Levenshtein.distance(ri, hi), len(r)

def corpus_wer(pairs):
    e = n = 0
    for ref_n, hyp_n in pairs:
        a, b = word_errors(ref_n, hyp_n)
        e += a; n += b
    return e / max(n, 1)

def bootstrap_wer(errs, nref, reps=2000, seed=0):
    errs = np.asarray(errs, float); nref = np.asarray(nref, float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(errs), size=(reps, len(errs)))
    w = errs[idx].sum(1) / nref[idx].sum(1)
    return float(np.percentile(w, 2.5)), float(np.percentile(w, 97.5))

def wilson(k, n, z=1.959964):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)

def read_jsonl(p):
    return [json.loads(l) for l in open(p) if l.strip()]

def pct(xs, q):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * q
    f, c = math.floor(k), math.ceil(k)
    return xs[f] + (xs[c] - xs[f]) * (k - f)
