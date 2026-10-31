"""G11 diversity (independent F10 checker, check:F10, c-lanes-v3; test adapted from the F11 checker's g11.py). C_DATA_SPEC
2.1 / 8 G11 + F10 G0 1, 8:
- counts: cards >= 80 (round 1), packs >= 30 (round 1) with one pack per card, training samplers S1-S4, S6, S7 (S5
  never in a training pool), rows per training sampler <= 2,500 over both rounds (round 1 rows reported), rows per
  card <= 128;
- 2.1 quotas: instruction wordings pool >= 30 and >= 5 per card; definition styles >= 3; short or no card on about 15%
  of rows (10-20); few-shot cards (worked items with answers in the card) 5-10% of cards; definition examples on about
  50% of cards (report); inverted cards 10-15% of cards (report); held-out format styles never in a training pool;
- surface template = (format style, wording id, question sentence with code names / quoted names / numbers masked):
  max share <= 2% of F10 rows;
- Claude seeds: pairwise ROUGE-L (LCS F) < 0.7 among F10 instruction wordings (formats-2 family_pools) and among the
  setting seeds of F10 packs (S7 codebooks have no pack);
- gzip ratio and Self-BLEU-4 (200-row seeded sample) reported; the golden_train slice comparison is outside the
  checker allow-list (orchestrator item). Usage: g11.py <name>"""
import json, sys, re, gzip, math, random
from collections import Counter, defaultdict
import numpy as np
import chk_lib as L
_load = L.load
L.load = lambda n: _load(n)[0]

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
rows = L.load(NAME)
_side = _load(NAME)[1]
WORKED_RX = re.compile(r"(?i)(answer key:|the answer is [A-Z0-9]|<answer>)")
EXAMPLE_RX = re.compile(r"Example of ")


def qframe(r):
    s = [x for x in L.views(r)["q"].split("\n") if "?" in x]; s = s[-1] if s else L.views(r)["q"]
    for t in sorted(L.card_terms(r) + list(r["options"] or []), key=len, reverse=True):
        if len(t) >= 2:
            s = s.replace(t, "<T>")
    s = re.sub(r"[«'\"\[][^»'\"\]]{1,60}[»'\"\]]", "<Q>", s)
    return re.sub(r"\d[\d,]*(?:\.\d+)?", "<N>", s)


def lcs(a, b):
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if x == y else max(prev[j], cur[-1]))
        prev = cur
    return prev[-1]


def rouge_l(a, b):
    a, b = a.lower().split(), b.lower().split(); l_ = lcs(a, b)
    if not l_:
        return 0.0
    p, r = l_ / len(b), l_ / len(a)
    return 2 * p * r / (p + r)


def max_pair(texts):
    best = (0.0, None, None); ids = list(texts)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            v = rouge_l(texts[ids[i]], texts[ids[j]])
            if v > best[0]:
                best = (v, ids[i], ids[j])
    return best


def self_bleu(texts, n=4):
    toks = [t.lower().split() for t in texts]; scores = []
    grams = [[Counter(tuple(t[i:i + k]) for i in range(len(t) - k + 1)) for k in range(1, n + 1)] for t in toks]
    for h in range(len(toks)):
        logp = 0.0
        for k in range(n):
            hc = grams[h][k]; tot = sum(hc.values())
            if not tot:
                logp += math.log(1e-9); continue
            mx = Counter()
            for o in range(len(toks)):
                if o != h:
                    mx |= grams[o][k]
            clip = sum(min(c, mx[g]) for g, c in hc.items())
            logp += math.log(max(clip, 1e-9) / tot)
        scores.append(math.exp(logp / n))
    return float(np.mean(scores))


def main():
    out = {"gate": "G11", "file": f"out/{NAME}.jsonl", "rows": len(rows)}; P = {}
    n = len(rows); samp = Counter(r["meta"]["sampler"] for r in rows)
    per = defaultdict(list)
    for r in rows:
        per[r["meta"]["card_id"]].append(r)
    packs = Counter(r["meta"]["domain_pack"] for r in rows); pc = defaultdict(set)
    for r in rows:
        pc[r["meta"]["domain_pack"]].add(r["meta"]["card_id"])  # S7: codebook id
    rpc = {c: len(v) for c, v in per.items()}
    out["counts"] = {"cards": len(per), "packs": len(packs), "packs_on_2plus_cards": sum(len(v) > 1 for v in pc.values()),
                     "samplers": dict(samp), "rows_per_card_max": max(rpc.values()),
                     "rows_per_card_median": sorted(rpc.values())[len(rpc) // 2]}
    train_s = {"S1", "S2", "S3", "S4", "S6", "S7"}
    if NAME == "mixdev_S5":
        P["counts"] = set(samp) == {"S5"}
    else:
        P["counts"] = (len(per) >= 80 and len(packs) >= 30 and all(len(v) == 1 for v in pc.values() if True)
                       and set(samp) <= train_s and len(samp) >= 4 and max(samp.values()) <= 2500
                       and max(rpc.values()) <= 128)
    wd = Counter(r["meta"]["wording_id"] for r in rows); wpc = {c: len({r["meta"]["wording_id"] for r in v}) for c, v in per.items()}
    out["wordings"] = {"pool_used": len(wd), "min_per_card": min(wpc.values()), "cards_below_5": sum(v < 5 for v in wpc.values())}
    P["wordings"] = len(wd) >= 30 and (min(wpc.values()) >= 5 or NAME == "mixdev_S5")
    ds = Counter(r["meta"]["defs_style"] for r in rows)
    sc = sum(not (r.get("card") or "").strip() and r["meta"]["defs_style"] is None for r in rows) or sum(bool(_side.get(r["id"], {}).get("short")) for r in rows)
    out["defs_styles"] = {"rows": dict(ds), "short_card_pct": round(100 * sc / n, 2)}
    P["defs_styles"] = len([d for d in ds if d not in ("short", "none", None)]) >= 3
    if NAME != "mixdev_S5":
        P["short_card_10_20"] = 10 <= 100 * sc / n <= 20
    nwk, nex, inv = {}, {}, {}
    for c, v in per.items():
        base = [r for r in v if not r["meta"].get("twin_kind")] or v
        nwk[c] = int(any(_side.get(r["id"], {}).get("fewshot_card") for r in v))
        nex[c] = int(any(r["meta"].get("defs_style", "").endswith("examples") for r in v))
        inv[c] = any(_side.get(r["id"], {}).get("inverted_card") for r in v)
    nC = len(per); few = sum(1 for x in nwk.values() if x >= 1); exa = sum(1 for x in nex.values() if x >= 1)
    out["cards"] = {"fewshot_cards_pct": round(100 * few / nC, 2), "example_cards_pct": round(100 * exa / nC, 2),
                    "inverted_cards_pct": round(100 * sum(inv.values()) / nC, 2),
                    "worked_items_per_card": dict(Counter(min(x, 4) for x in nwk.values()))}
    if NAME != "mixdev_S5":
        P["fewshot_cards_5_10"] = 5 <= 100 * few / nC <= 10
    held = {json.loads(l)["id"] for l in open(L.LEAN / "c_src/formats/formats-1/data/styles.jsonl") if json.loads(l)["held_out"]}
    fs = Counter(r["meta"]["format_style"] for r in rows); hs = sum(v for k, v in fs.items() if k in held)
    out["held_out_style_rows"] = hs; P["no_held_out_styles"] = hs == 0 or NAME == "mixdev_S5"
    tpl = Counter((r["meta"]["format_style"], r["meta"]["wording_id"], qframe(r)) for r in rows)
    qf = Counter(qframe(r) for r in rows); top = tpl.most_common(1)[0]
    out["surface_template"] = {"definition": "(format_style, wording_id, masked question sentence)", "n_templates": len(tpl),
                               "max_share_pct": round(100 * top[1] / n, 3),
                               "info_max_share_pct": {"format_style": round(100 * fs.most_common(1)[0][1] / n, 2),
                                                      "wording_id": round(100 * wd.most_common(1)[0][1] / n, 2),
                                                      "question_frame": round(100 * qf.most_common(1)[0][1] / n, 2)}}
    P["surface_template_le_2pct"] = top[1] / n <= 0.02
    wt = {}
    for l in open(L.LEAN / "c_src/formats/formats-2/wordings/family_pools.jsonl"):
        d = json.loads(l)
        if d.get("pool") == "F10" or d["id"] in wd:
            wt[d["id"]] = d["text"]
    pk = {}
    for f in ("packs-1/packs.jsonl", "packs-2/packs.jsonl", "packs-3/packs-3.jsonl", "packs-4/packs.jsonl", "packs-4/packs-4.jsonl"):
        p = L.LEAN / "c_src/packs" / f
        if p.exists():
            for l in open(p):
                d = json.loads(l)
                if d.get("id") in packs:
                    pk[d["id"]] = d.get("setting") or d.get("description") or ""
    mw = max_pair(wt); mp = max_pair(pk)
    out["claude_seeds_rouge_l"] = {"wordings": {"n": len(wt), "max": round(mw[0], 3), "pair": mw[1:]},
                                   "pack_settings": {"n": len(pk), "found_of": len(packs), "max": round(mp[0], 3), "pair": mp[1:]}}
    P["seeds_rouge_l_lt_0.7"] = mw[0] < 0.7 and mp[0] < 0.7
    txt = "\n".join(L.full_text(r) for r in rows).encode()
    sm = random.Random(1111).sample(rows, min(200, len(rows)))
    sb = self_bleu([L.views(r)["q"] + " " + r["state"] for r in sm])
    out["corpus_metrics"] = {"gzip_ratio": round(len(gzip.compress(txt)) / len(txt), 4), "self_bleu4_q+state_200": round(sb, 4),
                             "vs_golden_train_slice": "not run (golden_train outside the checker allow-list; orchestrator item)"}
    # recheck:F10 r1 fix (script gap vs spec 8 G11: Vendi score was not computed): Vendi (exp entropy of the normalised
    # cosine kernel eigenvalues) on TF-IDF word 1-2 grams of question + state, 1,000-row seeded sample; report only
    # (the golden_train comparison is outside the allow-list)
    from sklearn.feature_extraction.text import TfidfVectorizer
    vs = random.Random(1112).sample(rows, min(1000, len(rows)))
    X = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True).fit_transform([L.views(r)["q"] + " " + r["state"] for r in vs])
    K = (X @ X.T).toarray() / len(vs); ev = np.clip(np.linalg.eigvalsh(K), 0, None); ev = ev[ev > 1e-12]; ev = ev / ev.sum()
    out["corpus_metrics"]["vendi_tfidf_q+state_1000"] = round(float(np.exp(-(ev * np.log(ev)).sum())), 2)
    out["pass_parts"] = P
    out["pass"] = all(P.values())
    (L.QC / f"g11_{NAME}.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({"pass": out["pass"], "parts": P, "counts": out["counts"], "cards": out["cards"],
                      "template": out["surface_template"]["max_share_pct"], "seeds": out["claude_seeds_rouge_l"]}, default=str))


if __name__ == "__main__":
    main()
