"""G11 diversity (independent F7 checker). C_DATA_SPEC 8 G11 + 2.1 quotas + F7 G0 4.6 (R19, Z01, T27) and 7:
- counts: >= 80 cards (r1), every F7 card has its own pack (no two cards share a pack), >= 30 packs, >= 4 training
  samplers (S1-S4, S6), each <= 2,500 rows, 0 S5 rows, 0 held-out formats-1 styles, rows per card <= 128 (median
  reported), wordings pool >= 30 and >= 5 per card (all from one wording family), definition styles >= 3;
- surface template = case-render template (sampler x container x frame set); frame set is approximated by the case
  skeleton (state with numbers, IDs, quoted values and pack nouns masked to the sampler's line shapes); no template > 2%
  of rows (gated on sampler x container x skeleton-of-line-kinds); max shares reported;
- Claude seeds ROUGE-L < 0.7 pairwise: instruction wordings (row-level wording + question with entity masked; most
  common text per wording_id) and C-line paraphrases (card-content paragraphs with numbers / names masked; distinct
  texts per C-line opener) - pairs >= 0.7 between different wording ids are fails; C-line pairs are reported;
- compression ratio (gzip), Self-BLEU-4 (300 rows), Vendi (2,000 rows, MiniLM): absolute values. The T27 comparison
  slice (golden_train) is outside the checker allow-list: reported n/a.
Usage: g11.py <name>"""
import gzip, json, math, random, re, sys
import numpy as np
from collections import Counter, defaultdict
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
IDRX = re.compile(r"\b[A-Z]{1,4}-?\d{2,6}\b")
NUMRX = re.compile(r"\d+(?:[.,]\d+)*")


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
    if not l:
        return 0.0
    p, r = l / len(b), l / len(a)
    return 2 * p * r / (p + r)


def max_pair(texts, cross=None):
    ks = sorted(texts); toks = {k: L.toks(texts[k]) for k in ks}; best = (0.0, None); over = []
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            if cross and cross(ks[i]) == cross(ks[j]):
                continue
            s = rouge_l(toks[ks[i]], toks[ks[j]])
            if s > best[0]:
                best = (s, [ks[i], ks[j]])
            if s >= 0.7:
                over.append([ks[i], ks[j], round(s, 3)])
    return {"n": len(ks), "max_rouge_l": round(best[0], 4), "max_pair": best[1], "pairs_ge_0.7": len(over), "examples": over[:10]}


def ngr(t, n):
    return Counter(tuple(t[i:i + n]) for i in range(len(t) - n + 1))


def self_bleu(texts, n_max=4):
    T = [L.toks(t) for t in texts]; scores = []
    for i, h in enumerate(T):
        refs = [T[j] for j in range(len(T)) if j != i]
        logs = 0.0
        for n in range(1, n_max + 1):
            hc = ngr(h, n); mx = Counter()
            for r in refs:
                for g, c in ngr(r, n).items():
                    if c > mx[g]:
                        mx[g] = c
            clip = sum(min(c, mx[g]) for g, c in hc.items()); tot = max(1, sum(hc.values()))
            logs += math.log(max(clip, 1e-9) / tot) / n_max
        scores.append(math.exp(logs))
    return float(np.mean(scores))


def skeleton(st):
    out = []
    for line in st.splitlines():
        s = IDRX.sub("<ID>", line); s = NUMRX.sub("<N>", s)
        s = re.sub(r"(?<=[:=|,]\s)[^:=|,<]+", "<V>", s)
        s = re.sub(r"\b[a-z]+(?:\s[a-z]+)*\b", "w", s)
        out.append(re.sub(r"\s+", " ", s).strip())
    return "\n".join(sorted(set(out)))[:400]


def main():
    rows = L.load(NAME); n = len(rows); res = {"gate": "G11", "file": f"out/{NAME}.jsonl", "rows": n}
    sys.path.insert(0, str(L.LEAN / "c_src/formats/formats-1"))
    from fmt1 import pool
    held = {s["id"] if isinstance(s, dict) else s for s in pool.styles(held_out=True)}
    samp = Counter(r["meta"]["sampler"] for r in rows); packs = Counter(r["meta"]["domain_pack"] for r in rows)
    cards = defaultdict(list)
    for r in rows:
        cards[r["meta"]["card_id"]].append(r)
    pack_cards = Counter(rs[0]["meta"]["domain_pack"] for rs in cards.values())
    wd = {c: {r["meta"]["wording_id"] for r in rs} for c, rs in cards.items()}
    wfam = {c: {w.rsplit(".", 1)[0] for w in v} for c, v in wd.items()}
    allw = Counter(r["meta"]["wording_id"] for r in rows)
    rpc = sorted(len(v) for v in cards.values())
    c = {"by_sampler": dict(samp), "training_samplers": sorted(s for s in samp if s != "S5"), "S5_rows": samp.get("S5", 0),
         "max_sampler_rows": max(samp.values()), "packs": len(packs), "cards": len(cards),
         "max_cards_per_pack": max(pack_cards.values()), "max_pack_row_share": round(max(packs.values()) / n, 4),
         "held_out_style_rows": sum(r["meta"].get("format_style") in held for r in rows), "n_held_out_styles_known": len(held),
         "rows_per_card_min_median_max": [rpc[0], rpc[len(rpc) // 2], rpc[-1]],
         "wordings_pool": len(allw), "min_wordings_per_card": min(len(v) for v in wd.values()),
         "max_wording_families_per_card": max(len(v) for v in wfam.values()),
         "wording_families": len({x for v in wfam.values() for x in v}),
         "defs_styles": dict(Counter(r["meta"].get("defs_style") for r in rows)),
         "format_styles": len({r["meta"].get("format_style") for r in rows})}
    c["pass"] = (c["cards"] >= 80 and c["max_cards_per_pack"] == 1 and c["packs"] >= 30 and len(c["training_samplers"]) >= 4
                 and c["S5_rows"] == 0 and c["max_sampler_rows"] <= 2500 and c["held_out_style_rows"] == 0 and rpc[-1] <= 128
                 and c["wordings_pool"] >= 30 and c["min_wordings_per_card"] >= 5 and c["max_wording_families_per_card"] == 1
                 and len(c["defs_styles"]) >= 3)
    res["counts"] = c
    tpl = Counter((r["meta"]["sampler"], r["meta"].get("container"), skeleton(r["state"])) for r in rows)
    sc = Counter((r["meta"]["sampler"], r["meta"].get("container")) for r in rows)
    res["two_pct"] = {"sampler_x_container_x_skeleton": {"n": len(tpl), "max_share": round(tpl.most_common(1)[0][1] / n, 4)},
                      "sampler_x_container_info": {"n": len(sc), "max_share": round(sc.most_common(1)[0][1] / n, 4)}}
    res["two_pct"]["pass"] = res["two_pct"]["sampler_x_container_x_skeleton"]["max_share"] <= 0.02
    cp = L.card_paras(rows); wtxt = defaultdict(Counter); ctxt = defaultdict(set)
    for r in rows:
        cc, rw = L.split_ins(r, cp)
        wtxt[r["meta"]["wording_id"]][IDRX.sub("<ID>", rw)] += 1
        for p in L.paras(cc):
            if p.startswith("<") or "\n" in p:
                continue
            m = NUMRX.sub("<N>", p)
            ctxt[" ".join(L.toks(m)[:3])].add(m)
    # Claude seeds as authored: the F7 wording pool (formats-2 family_pools, pool F7: text and text_gb) and the
    # generator lexicon's prose seeds (QUESTIONS, TASK_LINES, INJECT, canonical C-lines C). Data tables only; the
    # lexicon module has no imports. Closed 3.1 frames (F_*) and comparator words are spec vocabulary, reported apart.
    import runpy
    wp = [json.loads(l) for l in open(L.LEAN / "c_src/formats/formats-2/wordings/family_pools.jsonl")]
    wp = [w for w in wp if w.get("pool") == "F7"]
    lx = runpy.run_path(str(L.F7 / "gen/f7lex.py"))
    seeds = {}
    for w in wp:
        seeds["wd:" + w["id"]] = w["text"]
        if w.get("text_gb") and w["text_gb"] != w["text"]:
            seeds["wd:" + w["id"] + ":gb"] = w["text_gb"]
    for nm in ("QUESTIONS", "TASK_LINES", "INJECT"):
        for i, t in enumerate(lx.get(nm, [])):
            seeds[f"{nm}:{i}"] = t
    for k, v in lx["C"].items():
        seeds["C:" + k] = v if isinstance(v, str) else " ".join(v)
    same = lambda k: k.rsplit(":gb", 1)[0]
    res["seeds_rouge_l"] = {"seed_pool": {"n": len(seeds), "wordings": len(wp)}, "wordings": max_pair(seeds, cross=same),
                            "wordings_only": max_pair({k: v for k, v in seeds.items() if k.startswith("wd:")}, cross=same)}
    fr = {}
    for nm in [k for k in lx if k.startswith("F_")]:
        for i, t in enumerate(lx[nm] if isinstance(lx[nm], list) else [lx[nm]]):
            fr[f"{nm}:{i}"] = t
    res["seeds_rouge_l"]["closed_frames_info"] = max_pair(fr)
    wseeds = {k: v.most_common(1)[0][0] for k, v in wtxt.items()}
    res["seeds_rouge_l"]["row_extracted_info"] = {"n": len(wseeds), "note": "row-level text per wording_id; mixes card "
                                                  "renderings, report only"}
    cl = {}
    for k, v in ctxt.items():
        for i, t in enumerate(sorted(v)[:12]):
            cl[f"{k}#{i}"] = t
    res["seeds_rouge_l"]["c_line_paragraph_variants_info"] = {"n_texts": len(cl)}
    res["seeds_rouge_l"]["pass"] = res["seeds_rouge_l"]["wordings"]["pairs_ge_0.7"] == 0
    rng = random.Random(1111)
    qs = [L.split_ins(r, cp)[1] + "\n" + r["state"] for r in rows]
    full = [L.full_text(r) for r in rows]
    cr = lambda T: round(len(gzip.compress("\n".join(T).encode())) / len("\n".join(T).encode()), 4)
    sb = rng.sample(range(n), min(300, n))
    vendi = None
    try:
        from sentence_transformers import SentenceTransformer
        mdl = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
        vi = rng.sample(range(n), min(2000, n))
        X = mdl.encode([full[i][:2000] for i in vi], batch_size=64, normalize_embeddings=True)
        Kx = X @ X.T / len(X); w = np.linalg.eigvalsh(Kx); w = w[w > 1e-12]; vendi = round(float(math.exp(-(w * np.log(w)).sum())), 2)
    except Exception as e:  # noqa: BLE001
        vendi = f"n/a: {str(e)[:80]}"
    res["metrics"] = {"gzip_ratio_question_plus_record": cr(qs), "gzip_ratio_full_text": cr(full),
                      "self_bleu4_question_plus_record_300": round(self_bleu([qs[i] for i in sb]), 4),
                      "vendi_minilm_2000": vendi,
                      "comparison_vs_golden_train_slice": "n/a (golden_train is not in the checker allow-list; T27 slice is the mixer's)"}
    res["pass"] = c["pass"] and res["two_pct"]["pass"] and res["seeds_rouge_l"]["pass"]
    json.dump(res, open(L.QC / f"g11_{NAME}.json", "w"), indent=1)
    print(json.dumps({"pass": res["pass"], "counts_pass": c["pass"], "two_pct": res["two_pct"], "rouge": res["seeds_rouge_l"]["wordings"]["max_rouge_l"]}))


if __name__ == "__main__":
    main()
