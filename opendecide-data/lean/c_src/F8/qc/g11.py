"""G11 diversity (independent F8 checker). C_DATA_SPEC 2.1 / 6 / 8 G11 + F8 G0 0 and 10.1 (Diversity row):
- counts: cards >= 80, packs >= 30 with one distinct pack per card (XF09), training samplers S1-S4 (S5 never in a
  training pool), rows per training sampler <= 2,500 over both rounds;
- 2.1 card-level quotas: instruction wordings pool >= 30 and >= 5 per card; definition styles >= 3 (one-line; one-line +
  examples; rubric / decision list); short or no card on about 15% of rows (10-20); few-shot cards (2-3 worked examples
  in the card) 5-10% of cards; one-line + 1-2 worked examples on about 50% of cards (report: worked examples counted in
  the rendered card text); held-out format styles (formats-1 held_out) never in a training pool;
- surface template = (format style, wording id, question frame with numbers / IDs / quoted names masked): max share
  <= 2% of F8 rows;
- Claude seeds: pairwise ROUGE-L (LCS F) < 0.7 among F8's instruction wordings (formats-2 family_pools) and among the
  'setting' seeds of F8's packs;
- gzip ratio, Self-BLEU-4 (200-row seeded sample) and Vendi (MiniLM from the G8 cache) reported; the golden_train slice
  comparison is outside this checker's allow-list (orchestrator item). Usage: g11.py <name>"""
import json, sys, re, gzip, math, random
from collections import Counter, defaultdict
import numpy as np
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
rows = L.load(NAME); side = L.load_side(NAME)
MASK = [(re.compile(r"\b\d{4}-\d{2}-\d{2}\b"), "<D>"), (re.compile(r"\b[A-Z]{1,5}-\d{2,6}\b"), "<ID>"),
        (re.compile(r"'[^']{1,60}'"), "<Q>"), (re.compile(r"\d[\d,]*(?:\.\d+)?%?"), "<N>")]
EX_RX = re.compile(r"(?im)(<answer>|^\W*(?:answer|output|outcome|correct choice|correct answer|expected answer|expected output|a)\s*:)")


def mask(s):
    for rx, t in MASK:
        s = rx.sub(t, s)
    return s


def qframe(r):
    return mask(L.views(r)["q"]).lower()


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
        pc[r["meta"]["domain_pack"]].add(r["meta"]["card_id"])
    out["counts"] = {"cards": len(per), "packs": len(packs), "packs_on_2plus_cards": sum(len(v) > 1 for v in pc.values()),
                     "samplers": dict(samp)}
    P["counts"] = (len(per) >= 80 and len(packs) >= 30 and all(len(v) == 1 for v in pc.values())
                   and {s for s in samp} <= {"S1", "S2", "S3", "S4"} and len(samp) >= 4 and max(samp.values()) <= 2500)
    wd = Counter(r["meta"]["wording_id"] for r in rows); wpc = {c: len({r["meta"]["wording_id"] for r in v}) for c, v in per.items()}
    out["wordings"] = {"pool_used": len(wd), "min_per_card": min(wpc.values()), "cards_below_5": sum(v < 5 for v in wpc.values())}
    P["wordings"] = len(wd) >= 30 and min(wpc.values()) >= 5
    ds = Counter(r["meta"]["defs_style"] for r in rows)
    sc = sum(side[r["id"]]["card_version"] in ("short", "none") for r in rows)
    out["defs_styles"] = {"rows": dict(ds), "short_or_no_card_pct": round(100 * sc / n, 2)}
    P["defs_styles"] = len([d for d in ds if d not in ("short", "none")]) >= 3
    P["short_or_no_card_10_20"] = 10 <= 100 * sc / n <= 20
    nex = {}
    for c, v in per.items():
        nex[c] = max(len(EX_RX.findall((r.get("card") or "") + "\n" + L.split_q(r["instructions"])[1])) for r in v)
    exc = Counter(min(x, 3) for x in nex.values()); nC = len(per)
    few = sum(1 for x in nex.values() if x >= 2); one = sum(1 for x in nex.values() if x == 1)
    cds = Counter(Counter(r["meta"]["defs_style"] for r in v).most_common(1)[0][0] for v in per.values())
    out["worked_examples"] = {"cards_by_example_count": {str(k): v for k, v in sorted(exc.items())},
                              "fewshot_cards_2to3_pct": round(100 * few / nC, 2), "one_example_cards_pct": round(100 * one / nC, 2),
                              "cards_by_majority_defs_style": dict(cds)}
    P["fewshot_cards_5_10"] = 5 <= 100 * few / nC <= 10
    out["worked_examples"]["cards_with_1plus_examples_pct"] = round(100 * (few + one) / nC, 2)
    out["worked_examples"]["note"] = ("2.1 'few-shot cards (1-3 worked examples) 5-10% of cards' read here as cards with 2-3 worked "
                                      "examples (F8 keeps 1-example cards as the 'one-line + 1-2 examples' definition style, about 50% "
                                      "of cards); with either reading the quota is missed (1+ examples on cards_with_1plus_examples_pct)")
    held = {json.loads(l)["id"] for l in open(L.LEAN / "c_src/formats/formats-1/data/styles.jsonl") if json.loads(l)["held_out"]}
    fs = Counter(r["meta"]["format_style"] for r in rows); hs = sum(v for k, v in fs.items() if k in held)
    out["held_out_style_rows"] = hs; P["no_held_out_styles"] = hs == 0 or NAME == "mixdev_S5"
    tpl = Counter((r["meta"]["format_style"], r["meta"]["wording_id"], qframe(r)) for r in rows)
    qf = Counter(qframe(r) for r in rows); top = tpl.most_common(1)[0]
    out["surface_template"] = {"definition": "(format_style, wording_id, masked question)", "n_templates": len(tpl),
                               "max_share_pct": round(100 * top[1] / n, 3),
                               "info_max_share_pct": {"format_style": round(100 * fs.most_common(1)[0][1] / n, 2),
                                                      "wording_id": round(100 * wd.most_common(1)[0][1] / n, 2),
                                                      "question_frame": round(100 * qf.most_common(1)[0][1] / n, 2)}}
    P["surface_template_le_2pct"] = top[1] / n <= 0.02
    wt = {}
    for l in open(L.LEAN / "c_src/formats/formats-2/wordings/family_pools.jsonl"):
        d = json.loads(l)
        if d.get("pool") == "F8" or d["id"] in wd:
            wt[d["id"]] = d["text"]
    pk = {}
    for f in ("packs-1/packs.jsonl", "packs-2/packs.jsonl", "packs-3/packs-3.jsonl", "packs-4/packs.jsonl", "packs-4/packs-4.jsonl"):
        p = L.LEAN / "c_src/packs" / f
        if p.exists():
            for l in open(p):
                d = json.loads(l)
                if d.get("id") in packs:
                    pk[d["id"]] = d.get("setting") or ""
    mw = max_pair(wt); mp = max_pair(pk)
    out["claude_seeds_rouge_l"] = {"wordings": {"n": len(wt), "max": round(mw[0], 3), "pair": mw[1:]},
                                   "pack_settings": {"n": len(pk), "found_of": len(packs), "max": round(mp[0], 3), "pair": mp[1:]}}
    P["seeds_rouge_l_lt_0.7"] = mw[0] < 0.7 and mp[0] < 0.7
    txt = "\n".join(L.full_text(r) for r in rows).encode()
    sm = random.Random(1111).sample(rows, min(200, len(rows)))
    sb = self_bleu([L.views(r)["q"] + " " + r["state"] for r in sm])
    vendi = None; cache = L.TMP / f"g8_emb_{NAME}.npz"
    if cache.exists():
        Z = np.load(cache)["rowemb"].astype(np.float64)
        X = np.concatenate([Z[:, 0], Z[:, 2]], axis=1); X /= np.linalg.norm(X, axis=1, keepdims=True) + 1e-12
        ev = np.linalg.eigvalsh(X.T @ X / len(X)); ev = ev[ev > 1e-12]
        vendi = float(math.exp(-(ev * np.log(ev)).sum()))
    out["corpus_metrics"] = {"gzip_ratio": round(len(gzip.compress(txt)) / len(txt), 4), "self_bleu4_q+state_200": round(sb, 4),
                             "vendi_minilm_q+state": round(vendi, 2) if vendi else None,
                             "vs_golden_train_slice": "not run (golden_train outside the checker allow-list; orchestrator item)"}
    out["pass_parts"] = P
    out["pass"] = all(P.values())
    (L.QC / f"g11_{NAME}.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({"pass": out["pass"], "parts": P, "counts": out["counts"], "examples": out["worked_examples"],
                      "template": out["surface_template"], "seeds": out["claude_seeds_rouge_l"]}, default=str))


if __name__ == "__main__":
    main()
