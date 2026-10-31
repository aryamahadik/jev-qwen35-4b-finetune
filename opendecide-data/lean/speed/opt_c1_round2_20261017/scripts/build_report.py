"""Mac: builds VOICE_REAL.json from results/pulled/*.jsonl (pulled from od-cpu1 ~/opt_r2/voice/out). Numbers only."""
import sys, os, glob, json, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from r2common import *
from analyze_c1 import c1_summary
from analyze_eot import eot_summary, load_eot
import numpy as np
R = os.path.abspath(os.path.join(HERE, ".."))
P = f"{R}/results/pulled"; A = f"{R}/assets"
CARD = {"ls_clean": {"s160": 2.56, "s560": 2.46, "offline": 2.32}, "ls_other": {"s160": 5.57, "s560": 5.07, "offline": 4.84},
        "tedlium": {"s160": 3.77, "s560": 3.54, "offline": 3.50}, "ami": {"s160": 14.71, "s560": 11.88, "offline": 11.73},
        "earnings22": {"s160": 13.01, "s560": 12.82, "offline": 12.52}}
NAMES = {"ls_clean": "LibriSpeech test-clean", "ls_other": "LibriSpeech test-other", "tedlium": "TED-LIUM 3 test", "ami": "AMI IHM test", "earnings22": "Earnings-22 test"}

def load_asr(st, mode, tag=""):
    rows = {}
    for f in glob.glob(f"{P}/asr_{st}_{mode}{tag}.shard*.jsonl"):
        for r in read_jsonl(f): rows[r["uid"]] = r
    return rows

def wer_block():
    out = {}
    for st in CARD:
        man = {m["uid"]: m for m in read_jsonl(f"{A}/samples/{st}/manifest.jsonl")}
        for mode in ("s160", "s560", "offline"):
            rows = load_asr(st, mode)
            if not rows: continue
            errs, nref, ms, dur, ex = [], [], [], [], 0
            for u, r in rows.items():
                e, n = word_errors(man[u]["ref_norm"], norm_text(r["hyp"])); errs.append(e); nref.append(n); ms.append(r["ms"]); dur.append(r["dur_s"]); ex += (e == 0)
            w = 100 * sum(errs) / sum(nref); lo, hi = bootstrap_wer(errs, nref); c = CARD[st][mode]
            out[f"{st}/{mode}"] = {"set": NAMES[st], "mode": mode, "n_utts": len(rows), "n_ref_words": int(sum(nref)), "wer_pct": round(w, 2), "ci95_pct": [round(100 * lo, 2), round(100 * hi, 2)],
                "card_pct": c, "delta_pt": round(w - c, 2), "within_0.5pt": abs(w - c) <= 0.5, "card_inside_ci95": 100 * lo <= c <= 100 * hi,
                "utt_exact_pct": round(100 * ex / len(rows), 1), "audio_h": round(sum(dur) / 3600, 3), "cpu_rtf_1thread": round(sum(ms) / 1000 / sum(dur), 3)}
    return out

def slurp_block():
    man = {m["uid"]: m for m in read_jsonl(f"{A}/samples/slurp/manifest.jsonl")}
    asr = load_asr("slurp", "s560")
    e = n = 0; wer_by = {}
    for u, r in asr.items():
        a, b = word_errors(norm_text(man[u]["ref"]), norm_text(r["hyp"])); e += a; n += b; wer_by[u] = a
    res = {"asr_s560": {"n": len(asr), "wer_pct_vs_gold": round(100 * e / max(n, 1), 2), "utt_exact_pct": round(100 * sum(v == 0 for v in wer_by.values()) / max(len(wer_by), 1), 1)}}
    for lvl in ("scen", "intent"):
        p = f"{P}/c1_slurp_{lvl}_s560.jsonl"
        if os.path.exists(p): res[f"c1_{lvl}"] = c1_summary(p, man, wer_by)
    return res

def eot_block():
    out = {}
    for st in ("slurp", "ami", "ls_clean"):
        rows = load_eot(P, st)
        if not rows: continue
        ok = [r for r in rows if r.get("fa_ok")]
        o = {"n_utts": len(rows), "n_alignable": len(ok), "ref_speech_end_after_clip_start_s_p50": round(pct([r["last_word_end"] for r in ok], .5), 2) if ok else None}
        for tk in ("noise", "zero"):
            o[tk] = eot_summary(rows, tk)
        if st == "ami":
            o["noise_vs_clip_end"] = eot_summary(rows, "noise", ref_kind="clip")
        out[st] = o
    return out

if __name__ == "__main__":
    rev = json.load(open(f"{A}/REVISIONS.json"))
    res = {"generated_utc": datetime.datetime.utcnow().isoformat() + "Z", "wer": wer_block(), "slurp": slurp_block(), "eot": eot_block(), "revisions": rev}
    json.dump(res, open(f"{R}/results/report_raw.json", "w"), indent=1)
    print("wrote", f"{R}/results/report_raw.json")
