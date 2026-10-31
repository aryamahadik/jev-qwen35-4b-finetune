"""Mac or VM: WER per set/mode from out/asr_*.jsonl + manifests. Prints a table, writes results/wer_summary.json"""
import sys, os, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r2common import *
root = sys.argv[1]; samples = sys.argv[2]; outp = sys.argv[3]
CARD = {  # model card (OpenASR, normalised): chunk 0.16 / 0.56 / 1.12 s
  "ls_clean": {"s160": 2.56, "s560": 2.46, "offline": 2.32}, "ls_other": {"s160": 5.57, "s560": 5.07, "offline": 4.84},
  "tedlium": {"s160": 3.77, "s560": 3.54, "offline": 3.50}, "ami": {"s160": 14.71, "s560": 11.88, "offline": 11.73},
  "earnings22": {"s160": 13.01, "s560": 12.82, "offline": 12.52}}
res = {}
for st in CARD:
    man = {m["uid"]: m for m in read_jsonl(f"{samples}/{st}/manifest.jsonl")}
    for mode in ("s160", "s560", "offline"):
        rows = []
        for f in glob.glob(f"{root}/out/asr_{st}_{mode}.shard*.jsonl"):
            rows += read_jsonl(f)
        if not rows: continue
        errs, nref, ms, dur, nsil = [], [], [], [], 0
        for r in rows:
            e, n = word_errors(man[r["uid"]]["ref_norm"], norm_text(r["hyp"]))
            errs.append(e); nref.append(n); ms.append(r["ms"]); dur.append(r["dur_s"])
        wer = sum(errs) / sum(nref); lo, hi = bootstrap_wer(errs, nref)
        c = CARD[st][mode]
        res[f"{st}/{mode}"] = {"n": len(rows), "words": int(sum(nref)), "wer_pct": round(wer * 100, 2), "ci95_pct": [round(lo * 100, 2), round(hi * 100, 2)],
            "card_pct": c, "delta_pt": round(wer * 100 - c, 2), "card_in_ci": bool(lo * 100 <= c <= hi * 100), "within_0.5pt": bool(abs(wer * 100 - c) <= 0.5),
            "audio_h": round(sum(dur) / 3600, 3), "rtf_cpu": round(sum(ms) / 1000 / sum(dur), 3)}
        print(st, mode, res[f"{st}/{mode}"])
json.dump(res, open(outp, "w"), indent=1)
