"""G11 diversity (independent F3 checker). Spec 8 G11 + 2.1 counts + F3 G0 (card distinctness R1-11, definition
styles, XF09 one pack per card). Checks on out/candidates_r1.jsonl:
 (1) card / pack / sampler counts and per-card quotas (2.1 table; G0 section 1);
 (2) pairwise card distinctness: different pack AND (different stated toggle set OR different label schema);
 (3) no surface template above 2% of the family (template = question-stem skeleton: IDs, quoted values, numbers and
     month names masked); wording / style shares reported (pool sizes >= 30 make > 2% unavoidable for those);
 (4) ROUGE-L (LCS F1 on word tokens) < 0.7 between every two Claude seeds used by F3 (its domain packs; its wordings);
 (5) compression ratio, Self-BLEU-4 and Vendi score of F3 rows, reported; the golden_train comparison is not run here
     (golden_train is outside this checker's allow-list) and is left to the orchestrator.
Usage: g11.py  (writes qc/g11_candidates_r1.json)"""
import glob, gzip, json, math, random, re, statistics, time
from collections import Counter, defaultdict
import numpy as np
import qc_lib as L

T0 = time.time()
TRAIN_SAMPLERS = {"S1", "S2", "S3", "S4", "S6", "S7", "S8", "S9"}


def log(m):
    print(f"[{time.time() - T0:7.1f}s] {m}", flush=True)


def skel(q):
    q = re.sub(r"\b[A-Z0-9]{1,5}(-[A-Z0-9]{1,6})+\b", "<ID>", q)
    q = re.sub(r"'[^']*'", "<V>", q); q = re.sub(r'"[^"]*"', "<V>", q)
    q = re.sub(r"\d[\d,.:]*", "<N>", q)
    q = re.sub(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b", "<M>", q)
    return q


def toks(s):
    return re.findall(r"\w+|[^\w\s]", s.lower())


def lcs_len(a, b):
    """Bit-parallel LCS length (Hyyrö 2004) on token lists."""
    if not a or not b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    masks = defaultdict(int)
    for i, t in enumerate(a):
        masks[t] |= 1 << i
    full = (1 << len(a)) - 1; v = full
    for t in b:
        u = v & masks.get(t, 0)
        v = ((v + u) | (v - u)) & full
    return len(a) - bin(v).count("1")


def rouge_l(a, b):
    l = lcs_len(a, b)
    if l == 0:
        return 0.0
    p, r = l / len(b), l / len(a)
    return 2 * p * r / (p + r)


def pack_text(p):
    out = []
    def walk(x):
        if isinstance(x, str):
            out.append(x)
        elif isinstance(x, dict):
            for k, v in x.items():
                if k not in ("id", "pack_sha256", "pack_version", "persona_seed", "provenance"):
                    walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(p)
    return " ".join(out)


def max_pairwise(items):
    """items: list of (name, tokens); returns max ROUGE-L, the arg pair and the count of pairs >= 0.7."""
    best, arg, n_hi = 0.0, None, 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            s = rouge_l(items[i][1], items[j][1])
            if s >= 0.7:
                n_hi += 1
            if s > best:
                best, arg = s, [items[i][0], items[j][0]]
    return round(best, 4), arg, n_hi


def counts(rows, side):
    m = [r["meta"] for r in rows]; n = len(rows); res = {}
    cards = defaultdict(list)
    for r in rows:
        cards[r["meta"]["card_id"]].append(r)
    packs_by_card = {c: {x["meta"]["domain_pack"] for x in rs} for c, rs in cards.items()}
    pack_cards = defaultdict(set)
    for c, ps in packs_by_card.items():
        for p in ps:
            pack_cards[p].add(c)
    samp = Counter(x["sampler"] for x in m)
    per_card = [len(v) for v in cards.values()]
    wd_per_card = [len({x["meta"]["wording_id"] for x in v}) for v in cards.values()]
    card_defs = Counter()
    for v in cards.values():
        st = Counter(x["meta"]["defs_style"] for x in v if x["meta"]["defs_style"] != "none")
        card_defs[st.most_common(1)[0][0] if st else "none"] += 1
    styles = {json.loads(l)["id"]: json.loads(l)["held_out"] for l in open(L.LEAN / "c_src/formats/formats-1/data/styles.jsonl")}
    pool = {json.loads(l)["id"] for l in open(L.LEAN / "c_src/formats/formats-2/wordings/family_pools.jsonl")
            if json.loads(l).get("family") == "F3"}
    used_fs = Counter(x["format_style"] for x in m); used_wd = Counter(x["wording_id"] for x in m)
    fewshot = sum(any("fewshot" in str(x["meta"].get("edge")) or "few_shot" in str(x["meta"].get("edge"))
                      or "fewshot" in str(x["meta"]["defs_style"]) for x in v) for v in cards.values())
    inverted = sum(any(side[x["id"]].get("inverted_card") for x in v) for v in cards.values())
    nc = len(cards)
    res["cards"] = {"value": nc, "rule": ">= 80 (round 1)", "pass": nc >= 80}
    res["packs"] = {"value": len(pack_cards), "rule": ">= 30 per family (round 1); XF09 one pack per card",
                    "cards_with_gt1_pack": sum(len(p) > 1 for p in packs_by_card.values()),
                    "packs_shared_by_gt1_card": sum(len(c) > 1 for c in pack_cards.values())}
    res["packs"]["pass"] = (len(pack_cards) >= 30 and res["packs"]["cards_with_gt1_pack"] == 0
                            and res["packs"]["packs_shared_by_gt1_card"] == 0)
    tr = {s: c for s, c in samp.items() if s in TRAIN_SAMPLERS}
    res["samplers"] = {"counts": dict(sorted(samp.items())), "rule": ">= 4 training samplers; S5 never in training pool; "
                       "<= 2,500 rows per sampler over both rounds", "pass": len(tr) >= 4 and samp.get("S5", 0) == 0
                       and max(samp.values()) <= 2500}
    res["rows_per_card"] = {"max": max(per_card), "median": statistics.median(per_card), "min": min(per_card),
                            "rule": "max 128; median about 40-50 (median reported)", "pass": max(per_card) <= 128}
    res["wordings"] = {"pool_F3": len(pool), "used": len(used_wd), "not_in_F3_pool": sorted(set(used_wd) - pool),
                       "min_per_card": min(wd_per_card), "rule": "pool >= 30; each card >= 5"}
    res["wordings"]["pass"] = len(pool) >= 30 and min(wd_per_card) >= 5 and not res["wordings"]["not_in_F3_pool"]
    fs_unknown = sorted(s for s in used_fs if s not in styles); fs_held = sorted(s for s in used_fs if styles.get(s))
    res["format_styles"] = {"used": len(used_fs), "held_out_styles_used": fs_held, "unknown_styles": fs_unknown,
                            "rule": "no formats-1 held-out style in a training pool", "pass": not fs_held and not fs_unknown}
    defs_rows = Counter(x["defs_style"] for x in m)
    res["definition_styles"] = {"row_counts": dict(defs_rows), "card_main_style": dict(card_defs),
                                "n_styles_excl_none": len([k for k in defs_rows if k != "none"]),
                                "short_or_no_card_row_share": round(sum(r["meta"]["defs_style"] in ("none", "short")
                                                                        for r in rows) / n, 4),
                                "rule": ">= 3 styles (pass rule); about 50% of cards one-line + examples and about "
                                        "15% short/no-card rows are reported (approximate targets)"}
    res["definition_styles"]["pass"] = res["definition_styles"]["n_styles_excl_none"] >= 3
    res["few_shot_cards"] = {"value": fewshot, "share": round(fewshot / nc, 4), "rule": "5-10% of cards",
                             "pass": 0.05 <= fewshot / nc <= 0.10}
    res["inverted_cards"] = {"value": inverted, "share": round(inverted / nc, 4), "rule": "10-15% of cards",
                             "pass": 0.10 <= inverted / nc <= 0.15}
    return res, cards


def distinct(cards, side):
    """Pairwise: different pack AND (different stated toggle set OR different label schema). Per F3 G0 R1-11 the label
    schema is the status vocabulary kind (plain / masked / swapped, T36) plus the set of question types; the stated
    rule set is the sidecar's stated_toggles ('none' on no-card cards = no stated toggle)."""
    info = {}
    for c, v in cards.items():
        tog = set(); voc = set(); qts = set()
        for x in v:
            s = side[x["id"]]
            st = s.get("stated_toggles") or []
            if isinstance(st, str):  # 'none' (no card) or 'short:T1,T4,...' (short card)
                st = [] if st == "none" else st.split(":", 1)[-1].split(",")
            tog |= {t.strip() for t in st if t.strip()}; voc.add(str(s.get("vocab"))); qts.add(s.get("qt"))
        info[c] = (frozenset({x["meta"]["domain_pack"] for x in v}), frozenset(tog), (frozenset(voc), frozenset(qts)))
    ks = sorted(info); bad_pack, bad_rule = [], []
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            a, b = info[ks[i]], info[ks[j]]
            if a[0] & b[0]:
                bad_pack.append([ks[i], ks[j]])
            if a[1] == b[1] and a[2] == b[2]:
                bad_rule.append([ks[i], ks[j]])
    return {"pairs": len(ks) * (len(ks) - 1) // 2, "pairs_sharing_pack": len(bad_pack), "pairs_same_rules_and_schema": len(bad_rule),
            "examples": (bad_pack + bad_rule)[:10], "pass": not bad_pack and not bad_rule}


def templates(rows):
    n = len(rows)
    q = Counter(skel(L.views(r)["q"]) for r in rows)
    ins = Counter(skel(r["instructions"]) for r in rows)
    wd = Counter(r["meta"]["wording_id"] for r in rows); fs = Counter(r["meta"]["format_style"] for r in rows)
    top = q.most_common(1)[0][1] / n
    return {"definition": "question-stem skeleton (IDs, quoted values, numbers, month names masked)",
            "distinct_question_skeletons": len(q), "max_question_skeleton_share": round(top, 4),
            "distinct_instruction_skeletons": len(ins), "max_instruction_skeleton_share": round(ins.most_common(1)[0][1] / n, 4),
            "report_only_max_wording_share": round(wd.most_common(1)[0][1] / n, 4),
            "report_only_max_format_style_share": round(fs.most_common(1)[0][1] / n, 4),
            "note": "wording (36-pool) and format style are pool draws, not surface templates; a 30+ pool cannot keep each "
                    "under 2%", "rule": "no surface template > 2% of family", "pass": top <= 0.02}


def seeds(rows):
    packs = {}
    for p in glob.glob(str(L.LEAN / "c_src/packs/packs-*/packs*.jsonl")):
        if "sealedqc" in p or "index" in p:
            continue
        for l in open(p):
            d = json.loads(l)
            for k in ("id", "pack_id"):
                if isinstance(d.get(k), str):
                    packs[d[k]] = d
    used = sorted({r["meta"]["domain_pack"] for r in rows})
    missing = [u for u in used if u not in packs]
    P = [(u, toks(pack_text(packs[u]))) for u in used if u in packs]
    W = [(d["id"], toks(d["text"])) for d in map(json.loads, open(L.LEAN / "c_src/formats/formats-2/wordings/family_pools.jsonl"))
         if d.get("family") == "F3"]
    pb, pa, ph = max_pairwise(P); log(f"packs rouge max {pb}")
    wb, wa, wh = max_pairwise(W); log(f"wordings rouge max {wb}")
    return {"packs": {"n": len(P), "missing_pack_records": missing, "max_rouge_l": pb, "argmax": pa, "pairs_ge_0_7": ph},
            "wordings": {"n": len(W), "max_rouge_l": wb, "argmax": wa, "pairs_ge_0_7": wh},
            "rule": "every Claude seed ROUGE-L < 0.7 to all other seeds (F3's packs and wordings)",
            "pass": not missing and ph == 0 and wh == 0}


def self_bleu(texts, N=4):
    grams = []
    for t in texts:
        tk = toks(t); grams.append([Counter(tuple(tk[i:i + n]) for i in range(len(tk) - n + 1)) for n in range(1, N + 1)])
    top = [defaultdict(list) for _ in range(N)]  # gram -> top-2 (count, row)
    for ri, g in enumerate(grams):
        for n in range(N):
            for k, c in g[n].items():
                lst = top[n][k]; lst.append((c, ri)); lst.sort(reverse=True); del lst[2:]
    scores = []
    for ri, g in enumerate(grams):
        lp = 0.0
        for n in range(N):
            tot = sum(g[n].values()); clip = 0
            for k, c in g[n].items():
                ref = next((cc for cc, rr in top[n][k] if rr != ri), 0); clip += min(c, ref)
            lp += math.log(max(clip, 1e-9) / max(tot, 1)) / N
        scores.append(math.exp(lp))
    return float(np.mean(scores))


def vendi(X):
    X = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)
    ev = np.linalg.eigvalsh((X.T @ X) / len(X)); ev = ev[ev > 1e-12]
    return float(np.exp(-(ev * np.log(ev)).sum()))


def diversity(rows):
    texts = [L.views(r)["q"] + "\n" + r["state"] for r in rows]
    raw = "\n".join(texts).encode(); cr = len(raw) / len(gzip.compress(raw, 9))
    rng = random.Random(11); samp = rng.sample(range(len(rows)), 300)
    sb = self_bleu([texts[i] for i in samp]); log(f"self-bleu {sb:.4f}")
    out = {"compression_ratio_q_state": round(cr, 4), "self_bleu4_300_sample_seed11": round(sb, 4)}
    cache = L.QC / "tmp/g8_emb_candidates_r1.npz"
    if cache.exists():
        Z = np.load(cache)["rowemb"].astype(np.float32)
        out["vendi_minilm_state"] = round(vendi(Z[:, 2]), 3); out["vendi_minilm_question"] = round(vendi(Z[:, 0]), 3)
    out["golden_train_comparison"] = ("not run: data/v14_parts/golden_train.jsonl is outside this checker's allow-list; "
                                      "values are for the orchestrator's counts-only compare")
    out["pass"] = None
    return out


def main():
    rows, side = L.load("candidates_r1")
    out = {"gate": "G11", "file": "out/candidates_r1.jsonl", "rows": len(rows)}
    c, cards = counts(rows, side); out["counts"] = c; log("counts done")
    out["card_distinctness"] = distinct(cards, side); log("distinctness done")
    out["surface_templates"] = templates(rows); log("templates done")
    out["claude_seeds_rouge_l"] = seeds(rows)
    out["diversity_metrics"] = diversity(rows)
    checks = [v["pass"] for v in c.values()] + [out[k]["pass"] for k in ("card_distinctness", "surface_templates", "claude_seeds_rouge_l")]
    out["failed_checks"] = [k for k, v in c.items() if not v["pass"]] + [k for k in ("card_distinctness", "surface_templates",
                                                                                   "claude_seeds_rouge_l") if not out[k]["pass"]]
    out["pass_checkable_parts"] = all(checks)
    out["pass"] = out["pass_checkable_parts"]
    out["unrun"] = ["compression / Self-BLEU / Vendi vs golden_train family slice (outside allow-list)"]
    out["seconds"] = round(time.time() - T0, 1)
    (L.QC / "g11_candidates_r1.json").write_text(json.dumps(out, indent=1))
    log(f"done pass={out['pass']} failed={out['failed_checks']}")


if __name__ == "__main__":
    main()
