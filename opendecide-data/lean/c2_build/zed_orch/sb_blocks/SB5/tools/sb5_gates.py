"""SB5 format gates at 100% (A58 c 5): schema, options/gold, G12, G15 loader round trip, tokens (<= 2,000 per row, mean <= 800,
instructions counted twice), no bench wording (no 8-gram shared with a bench instruction or criteria string), G10 balance.
Usage: python -B sb5_gates.py <rows.jsonl> [<rows.jsonl> ...] -> work/gates_<stem>.json (counts only)"""
import ast, json, re, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sb5_lib import *
from c2_kit import rows as R, cards

def wtok(s): return re.findall(r"[a-z0-9']+", s.lower())
def g8(s):
    w = wtok(s); return {" ".join(w[i:i + 8]) for i in range(len(w) - 7)}

def bench_strings():
    out = []
    for p in [BENCH / "text_track/data/cases.jsonl"] + sorted((BENCH / "data").glob("*/cases.jsonl")):
        for l in open(p, encoding="utf-8"):
            o = json.loads(l); strings_of(o.get("questions"), out)
    for p in (BENCH / "src/system-one-bench").glob("*.py"):
        try: tree = ast.parse(p.read_text())
        except Exception: continue
        for n in ast.walk(tree):
            if isinstance(n, ast.Constant) and isinstance(n.value, str) and len(n.value) > 30: out.append(n.value)
    return out

def run(path):
    rows = [json.loads(l) for l in open(path, encoding="utf-8")]
    res = {"file": str(Path(path).name), "rows": len(rows)}
    bad = {}
    sch = [(r["id"], [p for p in R.validate_row(r) if p != "meta.licence"]) for r in rows]
    bad["schema"] = sum(bool(p) for _, p in sch)
    bad["options_gold"] = sum(not (r["qtype"] == "noul" and r["options"] is None and r["gold"] in (0, 1)) for r in rows)
    ids = Counter(r["id"] for r in rows); nk = Counter(" ".join(norm_tokens(r["state"])) + "||" + r["instructions"] for r in rows)
    rids = Counter(r["meta"]["sb5"]["uci_rid"] for r in rows)
    bad["g12_dup_id"] = sum(v > 1 for v in ids.values()); bad["g12_dup_state_question"] = sum(v > 1 for v in nk.values())
    bad["g12_one_row_per_source_record"] = sum(v > 1 for v in rids.values())
    texts = [" ".join(norm_tokens(r["state"])) for r in rows]
    bad["g12_exact_dup_state"] = len(texts) - len(set(texts))
    g15 = 0; g15err = []
    for r in rows:
        try:
            x = R.g15_check(r); ok = (x.get("ok", True) if isinstance(x, dict) else bool(x))
            if not ok: g15 += 1; g15err.append(str(x)[:100])
        except Exception as e:
            g15 += 1; g15err.append(type(e).__name__ + str(e)[:100])
    bad["g15_loader_round_trip"] = g15
    mx, tok = cards._tokenizer()
    class L:
        def record(self, *a, **k): pass
    tt = mx.token_counts(L(), rows) if tok is not None else [R.approx_tokens(r) for r in rows]
    res["tokens"] = {"counted_by": "pinned Qwen3.5-4B tokenizer" if tok is not None else "approx", "mean": round(sum(tt) / len(tt), 1), "max": max(tt)}
    bad["tokens_gt_2000"] = sum(t > 2000 for t in tt); bad["token_mean_gt_800"] = int(sum(tt) / len(tt) > 800)
    bs = set()
    for s in bench_strings(): bs |= g8(s)
    mine = set()
    for r in rows: mine |= g8(r["instructions"]) | g8(r["card"])
    bad["bench_wording_8gram_shared"] = len(mine & bs)
    res["bench_strings_8grams"] = len(bs)
    yes = sum(r["gold"] for r in rows) / len(rows)
    res["yes_share"] = round(yes, 4); bad["g10_yes_share_outside_45_55"] = int(not 0.45 <= yes <= 0.55)
    wc = Counter(r["meta"]["wording_id"] for r in rows)
    res["wordings"] = len(wc); res["wording_max_share"] = round(max(wc.values()) / len(rows), 4)
    bad["wording_lt4_or_gt35"] = int(len(wc) < 4 or max(wc.values()) / len(rows) > 0.35)
    qs = Counter(r["meta"]["sb5"]["question_polarity"] for r in rows); res["question_polarity"] = dict(qs)
    res["labels"] = dict(Counter(r["meta"]["sb5"]["orig_label"] for r in rows))
    res["failures"] = bad; res["g15_errors_sample"] = g15err[:3]; res["pass"] = all(v == 0 for v in bad.values())
    return res

if __name__ == "__main__":
    for p in sys.argv[1:]:
        r = run(p); json.dump(r, open(WORK / f"gates_{Path(p).stem}.json", "w"), indent=1); print(json.dumps(r, indent=1))
