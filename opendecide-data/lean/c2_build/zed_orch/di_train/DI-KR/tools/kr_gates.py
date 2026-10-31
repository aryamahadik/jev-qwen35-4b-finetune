"""DI-KR format gates at 100% (A61 c 5/7): schema, options exactly the block's label set (4 distinct integers, one number format, gold one of them),
G12 (exact dup 0, one row per source record, near-dup), G15 loader round trip, tokens (<= 2,000 per row, mean <= 800, instructions twice), >= 4 wordings
none above 35%, gold position, G10 class balance (no class above 40%), and the GSM8K gold check re-run on the source answer of every row (AST).
Usage: python -I -B kr_gates.py <rows.jsonl> [...]  -> work/gates_<stem>.json (counts only)"""
import json, re, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kr_lib import *
from c2_kit import rows as R, cards
from scipy.stats import chisquare

SRCROWS = [json.loads(l) for l in open(SRC / "train.jsonl", encoding="utf-8")]


def run(path):
    rows = [json.loads(l) for l in open(path, encoding="utf-8")]
    res = {"file": Path(path).name, "rows": len(rows)}
    bad = {}
    bad["schema"] = sum(bool([p for p in R.validate_row(r) if p != "meta.licence"]) for r in rows)
    def fmt_ok(r):
        o = r["options"]
        return (r["qtype"] == "choice" and len(o) == 4 and len(set(o)) == 4 and all(re.fullmatch(r"[1-9][0-9]*", x) for x in o) and r["gold"] in o
                and len({int(x) for x in o}) == 4)
    bad["options_gold_format"] = sum(not fmt_ok(r) for r in rows)
    ids = Counter(r["id"] for r in rows); st = Counter(" ".join(norm_tokens(r["state"])) for r in rows)
    pids = Counter(r["meta"]["di_kr"]["pid"] for r in rows)
    bad["g12_dup_id"] = sum(v > 1 for v in ids.values()); bad["g12_exact_dup_state"] = sum(v - 1 for v in st.values() if v > 1)
    bad["g12_one_row_per_source_record"] = sum(v > 1 for v in pids.values())
    # near-duplicate (5-gram Jaccard >= 0.8) among the rows, inverted index
    inv, segs, nd = {}, [], 0
    for r in rows:
        g = grams(norm_tokens(r["state"])); cand = set()
        for x in g: cand |= inv.get(x, set())
        if any(len(g & segs[j]) / max(1, len(g | segs[j])) >= 0.8 for j in cand): nd += 1
        segs.append(g)
        for x in g: inv.setdefault(x, set()).add(len(segs) - 1)
    bad["g12_near_dup"] = nd
    g15 = 0; err = []
    for r in rows:
        try:
            x = R.g15_check(r); ok = (x.get("ok", True) if isinstance(x, dict) else bool(x))
            if not ok: g15 += 1; err.append(str(x)[:100])
        except Exception as e:
            g15 += 1; err.append(type(e).__name__ + str(e)[:100])
    bad["g15_loader_round_trip"] = g15
    mx, tok = cards._tokenizer()
    class L:
        def record(self, *a, **k): pass
    tt = mx.token_counts(L(), rows) if tok is not None else [R.approx_tokens(r) for r in rows]
    res["tokens"] = {"counted_by": "pinned Qwen3.5-4B tokenizer" if tok is not None else "approx", "mean": round(sum(tt) / len(tt), 1), "max": max(tt)}
    bad["tokens_gt_2000"] = sum(t > 2000 for t in tt); bad["token_mean_gt_800"] = int(sum(tt) / len(tt) > 800)
    wc = Counter(r["meta"]["wording_id"] for r in rows)
    res["wordings"] = len(wc); res["wording_max_share"] = round(max(wc.values()) / len(rows), 4)
    bad["wording_lt4_or_gt35"] = int(len(wc) < 4 or max(wc.values()) / len(rows) > 0.35)
    pos = Counter(r["options"].index(r["gold"]) for r in rows)
    res["gold_position"] = {str(k): pos[k] for k in range(4)}
    res["gold_position_chi2_p"] = round(float(chisquare([pos[k] for k in range(4)]).pvalue), 4)
    bad["class_above_40"] = int(max(pos.values()) / len(rows) > 0.40)
    rk = Counter(r["meta"]["di_kr"]["gold_rank"] for r in rows); res["gold_numeric_rank"] = {str(k): rk[k] for k in range(4)}
    bad["rank_class_above_40"] = int(max(rk.values()) / len(rows) > 0.40)
    # gold check re-run on the source answer (AST evaluator)
    gc = 0
    for r in rows:
        d = r["meta"]["di_kr"]; o = SRCROWS[d["train_idx"]]
        ok, why, info = check_problem(o["answer"])
        if not (ok and str(int(parse_num(info["gold"]))) == r["gold"] and " ".join(o["question"].split()) == r["state"]): gc += 1
    bad["gold_check_ast_rerun"] = gc
    res["distractor_sources"] = {"hard": sum(r["meta"]["di_kr"]["n_hard"] for r in rows), "style": sum(r["meta"]["di_kr"]["n_style"] for r in rows)}
    res["failures"] = bad; res["g15_errors_sample"] = err[:3]; res["pass"] = all(v == 0 for v in bad.values())
    return res


if __name__ == "__main__":
    for p in sys.argv[1:]:
        r = run(p); json.dump(r, open(WORK / f"gates_{Path(p).stem}.json", "w"), indent=1); print(json.dumps(r, indent=1))
