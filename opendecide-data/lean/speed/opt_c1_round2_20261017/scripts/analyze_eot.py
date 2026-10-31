import sys, os, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r2common import *
import numpy as np

METHODS = ["st_0.2", "st_0.3", "st_0.5", "vad_0.2", "vad_0.5", "vad_0.8", "eou"]

def det_time(R, meth, cpu):
    """-> stream time (s) of the end-of-turn decision, or None. cpu=True adds measured CPU compute."""
    if meth == "eou":
        e = R["eou"]
        return e.get("t_cpu" if cpu else "t_alg")
    d = R[meth]
    if d["t"] is None: return None
    t = d["t"]
    if cpu:
        if meth.startswith("st") and d["mode"] == "smart_turn" and d["st_fe_ms"]:
            t += (d["st_fe_ms"][-1] + d["st_ort_ms"][-1]) / 1000.0
        t += R["vad_ms_mean"] / 1000.0
    return t

def eot_summary(rows, tk, ref_kind="fa", add_ms=None):
    add_ms = add_ms or {}   # idle-CPU compute to add to the algorithmic latency, e.g. {"st": 60.0, "eou": 30.0, "vad": 0.5}
    out = {}
    ok = [r for r in rows if r.get("fa_ok")]
    for meth in METHODS:
        lat_a, lat_c, hard, anyc, miss, fb, good = [], [], 0, 0, 0, 0, 0
        n = len(ok)
        for r in ok:
            R = r[tk]
            ref_end = r["last_word_end"] if ref_kind == "fa" else r["dur_s"]
            ta = det_time(R, meth, False)
            tc = None if ta is None else ta + add_ms.get("eou" if meth == "eou" else ("st" if (meth.startswith("st") and R[meth]["mode"] == "smart_turn") else "vad"), 0.0) / 1000.0
            if ta is None: miss += 1; continue
            if ta < r["last_word_start"]: hard += 1
            if ta < ref_end: anyc += 1
            lat_a.append(ta - ref_end); lat_c.append(tc - ref_end)
            if 0 <= tc - ref_end <= 1.0: good += 1
            if meth.startswith("st") and R[meth]["mode"] == "fallback": fb += 1
        det = len(lat_a)
        pos = [x for x in lat_a if x >= 0]
        o = {"n": n, "detected": det, "miss_pct": round(100 * miss / n, 2) if n else None,
             "false_cut_before_last_word_pct": round(100 * hard / n, 2), "false_cut_before_last_word_wilson95": [round(100 * x, 2) for x in wilson(hard, n)],
             "cut_before_speech_end_pct": round(100 * anyc / n, 2), "decided_within_1s_after_end_no_cut_pct": round(100 * good / n, 2),
             "lat_alg_ms": {q: round(1000 * pct(lat_a, p), 0) for q, p in (("p50", .5), ("p90", .9), ("p95", .95))} if lat_a else None,
             "lat_incl_idle_cpu_ms": {q: round(1000 * pct(lat_c, p), 0) for q, p in (("p50", .5), ("p90", .9), ("p95", .95))} if lat_c else None,
             "lat_alg_ms_nonneg_p50": round(1000 * pct(pos, .5), 0) if pos else None}
        if meth.startswith("st"): o["fallback_pct"] = round(100 * fb / n, 2)
        out[meth] = o
    # CPU compute facts
    st_ms = [(f + o) for r in ok for f, o in zip(r[tk]["st_0.2"]["st_fe_ms"], r[tk]["st_0.2"]["st_ort_ms"])]
    out["_compute"] = {"smart_turn_call_ms": {"p50": round(pct(st_ms, .5), 1), "p95": round(pct(st_ms, .95), 1), "n_calls": len(st_ms)} if st_ms else None,
                       "silero_ms_per_32ms_window_mean": round(float(np.mean([r[tk]["vad_ms_mean"] for r in ok])), 3),
                       "eou_chunk_ms_p50": round(float(np.median([r[tk]["eou"]["chunk_ms_p50"] for r in ok])), 1),
                       "eou_chunk_ms_p95_of_p95": round(float(np.percentile([r[tk]["eou"]["chunk_ms_p95"] for r in ok], 95)), 1)}
    return out

def load_eot(root, st):
    rows = []
    for f in glob.glob(f"{root}/eot_{st}.shard*.jsonl"): rows += read_jsonl(f)
    return rows
