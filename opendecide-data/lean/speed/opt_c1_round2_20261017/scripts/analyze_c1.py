import sys, os, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r2common import *
import numpy as np

def c1_summary(path, man_by_uid, asr_wer_by_uid=None):
    rows = read_jsonl(path)
    n = len(rows)
    if not n: return None
    ag = [r["pred_gold"] == r["pred_asr"] for r in rows]
    ok_g = [r["pred_gold"] == r["gold_label"] for r in rows]
    ok_a = [r["pred_asr"] == r["gold_label"] for r in rows]
    k = sum(ag); lo, hi = wilson(k, n)
    flips = [r for r in rows if r["pred_gold"] != r["pred_asr"]]
    dps = [r["max_abs_dp"] for r in rows]
    res = {"n": n, "agree": k, "agree_pct": round(100 * k / n, 2), "agree_wilson95_pct": [round(100 * lo, 2), round(100 * hi, 2)],
           "flips": n - k, "acc_gold_transcript_pct": round(100 * sum(ok_g) / n, 2), "acc_asr_transcript_pct": round(100 * sum(ok_a) / n, 2),
           "acc_diff_pt": round(100 * (sum(ok_a) - sum(ok_g)) / n, 2),
           "acc_gold_wilson95_pct": [round(100 * x, 2) for x in wilson(sum(ok_g), n)], "acc_asr_wilson95_pct": [round(100 * x, 2) for x in wilson(sum(ok_a), n)],
           "max_abs_dp": {"p50": round(pct(dps, .5), 4), "p95": round(pct(dps, .95), 4), "max": round(max(dps), 4)},
           "margin_gold_flipped_p50": round(pct([r["margin_gold"] for r in flips], .5), 3) if flips else None,
           "margin_gold_all_p50": round(pct([r["margin_gold"] for r in rows], .5), 3),
           "flips_where_gold_transcript_decision_correct": sum(r["pred_gold"] == r["gold_label"] for r in flips),
           "flips_where_asr_transcript_decision_correct": sum(r["pred_asr"] == r["gold_label"] for r in flips),
           "prompt_tokens_p50": int(pct([r["prompt_tokens"] for r in rows], .5)), "s_per_item_p50": round(pct([r["s"] for r in rows], .5), 1)}
    if asr_wer_by_uid:
        ex = [r for r in rows if asr_wer_by_uid.get(r["uid"]) == 0]; ne = [r for r in rows if asr_wer_by_uid.get(r["uid"], 0) > 0]
        res["by_transcript"] = {"exact_match_n": len(ex), "exact_agree_pct": round(100 * sum(r["pred_gold"] == r["pred_asr"] for r in ex) / max(len(ex), 1), 2),
                                "not_exact_n": len(ne), "not_exact_agree_pct": round(100 * sum(r["pred_gold"] == r["pred_asr"] for r in ne) / max(len(ne), 1), 2)}
    return res
