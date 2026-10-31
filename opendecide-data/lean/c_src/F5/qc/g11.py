"""G11 diversity (independent F5 checker). C_DATA_SPEC 8 G11 + 2.1 + F5 G0 3.3/9:
- counts (2.1, round 1): >= 4 training samplers (S1-S4; S6 if present), no S5 row, each sampler <= 2,500 rows; packs
  >= 30; cards (one per (sampler, pack)) with distinct packs per card (reported); no held-out formats-1 style.
- 2% rule (G0 3.3: question cue templates and text templates; SEM renderings and instruction wordings exempt):
  (a) question surface template = (truth frame id, question template id) from the polarity sidecar; (b) independent
  pack-free skeleton of the question sentence (tokens used by < 25% of cards -> <W>; IDs, numbers, dates masked).
  Gate: max share <= 2% on both. Text side (report): pack-free skeletons of record lines carrying a negation cue.
- Claude seeds (ROUGE-L < 0.7 pairwise): instruction wordings (non-question instruction text per wording id) and
  truth frames; SEM renderings reported only (paraphrases of one meaning by design).
- compression ratio (gzip), Self-BLEU-4 (300 rows), Vendi (2,000 rows, cached MiniLM embeddings): absolute values;
  the 'no worse than golden_train's family slice' comparison is n/a (no F5 slice exists in round 1 / not in allow-list).
Usage: g11.py <name>"""
import gzip, json, math, random, re, sys
from collections import Counter, defaultdict
import numpy as np
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
TOK = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")
IDRX = re.compile(r"\b[A-Z]{2,4}-\d{3,5}\b")
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
NUM = re.compile(r"\b\d+(?:\.\d+)?\b")
NEGW = re.compile(r"\b(not|no|never|none|nor|neither|lacks?|without|failed|fail|omitted|neglected|refused|declined|un\w+|in\w+able)\b", re.I)


def norm(s):
    s = IDRX.sub(" zid ", s); s = DATE.sub(" zdate ", s); s = NUM.sub(" znum ", s)
    return TOK.findall(s.lower())


def skeleton(s, keep):
    out = []
    for t in norm(s):
        w = t if (t in keep or t.startswith("z")) else "<W>"
        if not (w == "<W>" and out and out[-1] == "<W>"):
            out.append(w)
    return " ".join(out)


def lcs(a, b):
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            cur.append(prev[j] + 1 if x == y else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]


def rouge_l(a, b):
    l = lcs(a, b)
    if l == 0:
        return 0.0
    p, r = l / len(b), l / len(a)
    return 2 * p * r / (p + r)


def max_pair(texts):
    toks = {k: TOK.findall(v.lower()) for k, v in texts.items()}; ks = sorted(toks); best = (0.0, None)
    over = []
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            s = rouge_l(toks[ks[i]], toks[ks[j]])
            if s > best[0]:
                best = (s, [ks[i], ks[j]])
            if s >= 0.7:
                over.append([ks[i], ks[j], round(s, 3)])
    return {"n": len(ks), "max_rouge_l": round(best[0], 4), "max_pair": best[1], "pairs_ge_0.7": len(over),
            "examples_ge_0.7": over[:10]}


def ngr(t, n):
    return Counter(tuple(t[i:i + n]) for i in range(len(t) - n + 1))


def self_bleu(texts, n_max=4):
    """mean BLEU-4 of each text against all others as references (clipped by the max count over the other texts;
    computed from each n-gram's top-2 counts so the text itself is excluded); add-one smoothing; brevity penalty
    against the closest reference length."""
    toks = [TOK.findall(t.lower()) for t in texts]; grams = [[ngr(t, n) for n in range(1, n_max + 1)] for t in toks]
    top = []
    for n in range(n_max):
        t2 = defaultdict(lambda: [(0, -1), (0, -1)])
        for j, g in enumerate(grams):
            for k, v in g[n].items():
                a = t2[k]
                if v > a[0][0]:
                    a[1] = a[0]; a[0] = (v, j)
                elif v > a[1][0]:
                    a[1] = (v, j)
        top.append(t2)
    lens = sorted((len(t), j) for j, t in enumerate(toks))
    scores = []
    for i, t in enumerate(toks):
        logp = 0.0
        for n in range(n_max):
            c = grams[i][n]; tot = sum(c.values()); m = 0
            for g, v in c.items():
                a = top[n][g]; mx = a[1][0] if a[0][1] == i else a[0][0]
                m += min(v, mx)
            logp += math.log((m + 1) / (tot + 1)) / n_max
        rl = min(((abs(l - len(t)), l) for l, j in lens if j != i))[1]
        bp = 1.0 if len(t) > rl else math.exp(1 - rl / max(1, len(t)))
        scores.append(bp * math.exp(logp))
    return float(np.mean(scores))


def vendi(X):
    X = X / np.linalg.norm(X, axis=1, keepdims=True); K = X @ X.T / len(X)
    w = np.linalg.eigvalsh(K); w = w[w > 1e-12]
    return float(math.exp(-(w * np.log(w)).sum()))


def main():
    rows = L.load(NAME); side = L.load_side(NAME); n = len(rows); res = {"gate": "G11", "file": f"out/{NAME}.jsonl", "rows": n}
    sys.path.insert(0, str(L.LEAN / "c_src/formats/formats-1"))
    from fmt1 import pool
    held = {s["id"] if isinstance(s, dict) else s for s in pool.styles(held_out=True)}
    samp = Counter(r["meta"]["sampler"] for r in rows); packs = Counter(r["meta"]["domain_pack"] for r in rows)
    cards = defaultdict(set)
    for r in rows:
        cards[r["meta"]["card_id"]].add((r["meta"]["sampler"], r["meta"]["domain_pack"]))
    pack_cards = Counter(p for v in cards.values() for _, p in v)
    res["counts"] = {"by_sampler": dict(samp), "training_samplers": sorted(s for s in samp if s != "S5"),
                     "S5_rows": samp.get("S5", 0), "max_sampler_rows": max(samp.values()), "packs": len(packs),
                     "cards": len(cards), "cards_with_one_sampler_pack": sum(len(v) == 1 for v in cards.values()),
                     "max_cards_per_pack": max(pack_cards.values()), "max_pack_row_share": round(max(packs.values()) / n, 4),
                     "held_out_style_rows": sum(r["meta"].get("format_style") in held for r in rows),
                     "n_held_out_styles_known": len(held)}
    c = res["counts"]
    c["pass"] = (len(c["training_samplers"]) >= 4 and c["S5_rows"] == 0 and c["max_sampler_rows"] <= 2500
                 and c["packs"] >= 30 and c["held_out_style_rows"] == 0 and c["cards_with_one_sampler_pack"] == len(cards))
    # 2% rule
    fq = Counter((side[r["id"]].get("frame_id"), side[r["id"]].get("template")) for r in rows)
    qt = Counter(side[r["id"]].get("template") for r in rows)
    card_df = Counter()
    toks_by_card = defaultdict(set)
    for r in rows:
        q, _ = L.split_q(r["instructions"]); toks_by_card[r["meta"]["card_id"]] |= set(norm(q))
    for v in toks_by_card.values():
        card_df.update(v)
    keep = {t for t, k in card_df.items() if k >= 0.25 * len(cards)}
    sk = Counter(); tsk = Counter()
    for r in rows:
        q, _ = L.split_q(r["instructions"]); sk[skeleton(q, keep)] += 1
        seen = set()
        for line in re.split(r"[\n]|(?<=[.;])\s+|</?(?:li|td|tr|p)>", r["state"]):
            if line and NEGW.search(line):
                seen.add(skeleton(line, keep))
        tsk.update(seen)
    top = lambda C, k=5: [[str(a), b, round(b / n, 4)] for a, b in C.most_common(k)]
    res["two_pct"] = {"frame_x_template": {"n": len(fq), "max_share": round(fq.most_common(1)[0][1] / n, 4), "top": top(fq)},
                      "template_ignoring_frame_info": {"n": len(qt), "max_share": round(qt.most_common(1)[0][1] / n, 4), "top": top(qt)},
                      "question_skeleton": {"keep_vocab": len(keep), "n": len(sk), "max_share": round(sk.most_common(1)[0][1] / n, 4), "top": top(sk)},
                      "text_neg_line_skeleton_info": {"n": len(tsk), "max_row_share": round(tsk.most_common(1)[0][1] / n, 4), "top": top(tsk, 8)}}
    t2 = res["two_pct"]; t2["pass"] = t2["frame_x_template"]["max_share"] <= 0.02 and t2["question_skeleton"]["max_share"] <= 0.02
    # Claude seeds: instruction wordings (non-question text, most common per id) and truth frames (question skeleton
    # prefix before the first masked slot, most common per frame id)
    wtxt = defaultdict(Counter); ftxt = defaultdict(Counter)
    for r in rows:
        q, rest = L.split_q(r["instructions"])
        wtxt[r["meta"].get("wording_id")][IDRX.sub("ZID", rest)] += 1
        k = skeleton(q, keep).split(" <W> ")[0]
        ftxt[side[r["id"]].get("frame_id")][k] += 1
    res["seeds_rouge_l"] = {"wordings": max_pair({k: v.most_common(1)[0][0] for k, v in wtxt.items()}),
                            "wording_variants_per_id_max": max(len(v) for v in wtxt.values()),
                            "frames_info": max_pair({str(k): v.most_common(1)[0][0] for k, v in ftxt.items()}),
                            "sem_renderings": "not tested: renderings of one SEM meaning are paraphrases by design (G0 3.3)"}
    res["seeds_rouge_l"]["pass"] = res["seeds_rouge_l"]["wordings"]["pairs_ge_0.7"] == 0
    # compression / Self-BLEU / Vendi (absolute; comparison n/a)
    rng = random.Random(1111)
    qs = [L.split_q(r["instructions"])[0] + "\n" + r["state"] for r in rows]
    full = [L.full_text(r) for r in rows]
    cr = lambda T: round(len(gzip.compress("\n".join(T).encode())) / len("\n".join(T).encode()), 4)
    sb_ix = rng.sample(range(n), 300)
    X = np.load(L.TMP / f"g8/emb_{NAME}.npy") if (L.TMP / f"g8/emb_{NAME}.npy").exists() else None
    v_ix = rng.sample(range(n), min(2000, n))
    res["metrics"] = {"gzip_ratio_question_plus_record": cr(qs), "gzip_ratio_full_text": cr(full),
                      "self_bleu4_question_plus_record_300": round(self_bleu([qs[i] for i in sb_ix]), 4),
                      "vendi_minilm_2000": round(vendi(X[v_ix]), 2) if X is not None else None,
                      "comparison_vs_golden_train_family_slice": "n/a (no F5 slice in golden_train; not in allow-list)"}
    res["pass"] = c["pass"] and t2["pass"] and res["seeds_rouge_l"]["pass"]
    json.dump(res, open(L.QC / f"g11_{NAME}.json", "w"), indent=1)
    print(json.dumps({"counts": c["pass"], "two_pct": t2["pass"], "fxq": t2["frame_x_template"]["max_share"],
                      "skel": t2["question_skeleton"]["max_share"], "seeds": res["seeds_rouge_l"]["pass"],
                      "metrics": res["metrics"], "pass": res["pass"]}))


if __name__ == "__main__":
    main()
