"""G11 diversity (independent F2 checker). C_DATA_SPEC 2.1 / 8 G11 + F2 G0 7:
- counts: cards >= 80, packs >= 30 (one card per pack, XF09), training samplers >= 4 (S1-S4; S5 never in training),
  rows per training sampler <= 2,500 over both rounds (round-1 share checked here);
- surface template = (format style, instruction wording, question frame), question frame = the question sentence with
  numbers, dates, IDs, currency/unit tokens and the card's quantity noun phrase masked; max share <= 2% of F2 rows;
  shares of format style, wording, question frame alone and of the masked whole-text skeleton are reported;
- Claude seeds: pairwise ROUGE-L (LCS F, own implementation; rouge_score is not installed) < 0.7 among F2's
  instruction wordings (formats-2 family_pools, pool F2) and among the 'setting' seeds of F2's 80 domain packs;
- compression ratio (gzip), Self-BLEU-4 (200-row seeded sample) and Vendi score (MiniLM embeddings from the G8 cache)
  are computed; the comparison with F2's slice of golden_train is NOT run here (golden_train is outside this checker's
  allow-list) and is left to the orchestrator. Usage: g11.py <name>"""
import json, sys, re, gzip, math, random
from collections import Counter
import numpy as np
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
rows = L.load(NAME)
MASK = [(re.compile(r"\b\d{4}-\d{2}-\d{2}\b"), "<D>"), (re.compile(r"\b[A-Z]{1,4}-\d{2,6}\b"), "<ID>"),
        (re.compile(r"\d[\d,]*(?:\.\d+)?"), "<N>"),
        (re.compile(r"\b(EUR|USD|GBP|CHF|JPY|AUD|CAD|NZD|SEK|NOK|DKK|INR|ZAR|SGD|dollars?)\b"), "<CUR>")]


def mask(s):
    for rx, t in MASK:
        s = rx.sub(t, s)
    return s


def qframe(r):
    q = mask(L.views(r)["q"]).lower()
    q = re.sub(r"\bthe ([a-z -]+?) (for|of|on) <id>", r"the <QTY> \2 <ID>", q)
    return q


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
    a, b = a.lower().split(), b.lower().split(); l = lcs(a, b)
    if not l:
        return 0.0
    p, r = l / len(b), l / len(a)
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
    out = {"gate": "G11", "file": f"out/{NAME}.jsonl", "rows": len(rows)}
    n = len(rows); samp = Counter(r["meta"]["sampler"] for r in rows)
    cards = {r["meta"]["card_id"] for r in rows}; packs = {r["meta"]["domain_pack"] for r in rows}
    out["counts"] = {"cards": len(cards), "packs": len(packs), "samplers": dict(samp)}
    c_ok = len(cards) >= 80 and len(packs) >= 30 and len([s for s in samp if s != "S5"]) >= 4 and "S5" not in samp and max(samp.values()) <= 2500
    tpl = Counter((r["meta"]["format_style"], r["meta"]["wording_id"], qframe(r)) for r in rows)
    fs = Counter(r["meta"]["format_style"] for r in rows); wd = Counter(r["meta"]["wording_id"] for r in rows)
    qf = Counter(qframe(r) for r in rows)
    skel = Counter(mask(L.full_text(r)) for r in rows)
    top = tpl.most_common(1)[0]
    out["surface_template"] = {"definition": "(format_style, wording_id, question frame)", "n_templates": len(tpl),
                               "max_share_pct": round(100 * top[1] / n, 3), "max_count": top[1],
                               "info_max_share_pct": {"format_style": round(100 * fs.most_common(1)[0][1] / n, 2),
                                                      "wording_id": round(100 * wd.most_common(1)[0][1] / n, 2),
                                                      "question_frame": round(100 * qf.most_common(1)[0][1] / n, 2),
                                                      "masked_full_text": round(100 * skel.most_common(1)[0][1] / n, 2)}}
    t_ok = top[1] / n <= 0.02
    used_w = set(wd)
    wt = {}
    for l in open(L.LEAN / "c_src/formats/formats-2/wordings/family_pools.jsonl"):
        d = json.loads(l)
        if d.get("pool") == "F2" or d["id"] in used_w:
            wt[d["id"]] = d["text"]
    pk = {}
    for f in ("packs-1/packs.jsonl", "packs-2/packs.jsonl", "packs-3/packs-3.jsonl", "packs-4/packs.jsonl"):
        p = L.LEAN / "c_src/packs" / f
        if p.exists():
            for l in open(p):
                d = json.loads(l)
                if d.get("id") in packs:
                    pk[d["id"]] = d.get("setting") or ""
    mw = max_pair(wt); mp = max_pair(pk)
    out["claude_seeds_rouge_l"] = {"wordings": {"n": len(wt), "max": round(mw[0], 3), "pair": mw[1:]},
                                   "pack_settings": {"n": len(pk), "found_of": len(packs), "max": round(mp[0], 3), "pair": mp[1:]}}
    s_ok = mw[0] < 0.7 and mp[0] < 0.7 and len(pk) == len(packs)
    txt = "\n".join(L.full_text(r) for r in rows).encode()
    rng = random.Random(1111); sm = rng.sample(rows, 200)
    sb = self_bleu([L.views(r)["q"] + " " + r["state"] for r in sm])
    vendi = None
    cache = L.QC / f"tmp/g8_emb_{NAME}.npz"
    if cache.exists():
        Z = np.load(cache)["rowemb"].astype(np.float64)
        X = np.concatenate([Z[:, 0], Z[:, 2]], axis=1); X /= np.linalg.norm(X, axis=1, keepdims=True) + 1e-12
        ev = np.linalg.eigvalsh(X.T @ X / len(X)); ev = ev[ev > 1e-12]
        vendi = float(math.exp(-(ev * np.log(ev)).sum()))
    out["corpus_metrics"] = {"gzip_ratio": round(len(gzip.compress(txt)) / len(txt), 4), "self_bleu4_q+state_200": round(sb, 4),
                             "vendi_minilm_q+state": round(vendi, 2) if vendi else None,
                             "vs_golden_train_slice": "not run (golden_train outside the F2 checker allow-list; orchestrator item)"}
    out["pass_parts"] = {"counts": c_ok, "surface_template_le_2pct": t_ok, "seeds_rouge_l_lt_0.7": s_ok,
                         "golden_train_comparison": "pending (orchestrator)"}
    out["pass"] = c_ok and t_ok and s_ok
    (L.QC / f"g11_{NAME}.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps(out, default=str)[:1500])


if __name__ == "__main__":
    main()
