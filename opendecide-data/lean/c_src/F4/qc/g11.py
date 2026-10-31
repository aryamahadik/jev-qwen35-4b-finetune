"""G11 diversity (independent F4 checker). C_DATA_SPEC 2.1 / 8 G11 + F4 G0 11:
- counts: cards >= 80 (round 1), one pack per card (>= 30 packs), training samplers S1-S4 (S5 never in training),
  rows per training sampler <= 2,500 over both rounds (round-1 pool checked);
- surface template = (instruction wording, question-frame paraphrase) pair (F4 G0 11: wording_id + edge frame tag);
  max share <= 2% of F4 rows; shares of wording, frame and style alone reported;
- Claude seeds, pairwise word-level ROUGE-L F1 (LCS, own implementation, lowercased, punctuation removed, slots one
  token) < 0.7: (a) F4's instruction wordings (formats-2 family pool F4); (b) question-frame paraphrase skeletons
  read off the rows (claim, entity, predicate, type noun and the {OUT} slot masked; leading 'Q:' / 'Question:' labels
  of the format style stripped); (c) the canonical clause lines of F4 G0 section 9 (one seed per numbered line,
  placeholders as one slot token); (d) the 'setting' seeds of F4's domain packs. Pairs inside one seed (a frame paraphrase vs its own
  slot fills) do not occur after masking;
- corpus metrics: gzip compression ratio, Self-BLEU-4 (200-row seeded sample), Vendi score (MiniLM state embeddings
  from the G8 cache). The comparison with golden_train (fld / proofwriter slice) is outside this checker's allow-list
  and is left to the orchestrator. Usage: g11.py <name>"""
import gzip, json, math, random, re, sys
from collections import Counter
import numpy as np
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
rows = L.load(NAME)
side = {json.loads(l)["id"]: json.loads(l) for l in open(L.OUT / f"{NAME}.sidecar.jsonl")}
W = re.compile(r"<[a-z]+>|[a-z0-9]+")


def toks(s):
    return W.findall(s.lower())


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
    p, r = l / len(a), l / len(b)
    return 2 * p * r / (p + r)


def max_pair(seeds):
    items = [(k, toks(v)) for k, v in seeds.items()]
    best = (0.0, None)
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            s = rouge_l(items[i][1], items[j][1])
            if s > best[0]:
                best = (s, (items[i][0], items[j][0]))
    n_over = sum(1 for i in range(len(items)) for j in range(i + 1, len(items))
                 if rouge_l(items[i][1], items[j][1]) >= 0.7) if best[0] >= 0.7 else 0
    return {"n": len(items), "max": round(best[0], 3), "pair": best[1], "pairs_ge_0.7": n_over}


IDR = re.compile(r"\b[A-Z]{2}[-/][A-Z0-9]{4,6}\b")
OUT = re.compile(r"\b(does not |do not )?(establish(es)?|show(s)?|rule(s)? out|leave(s)? open|follows? from)\b( that| whether)?", re.I)
LISTM = re.compile(r"^\s*(>\s*)?([-*•+]|\d+(\.\d+)*[.)]?|Step \d+:|\(\d+\))\s+")
LABEL = re.compile(r"^\s*(\*\*)?[A-Z][A-Za-z ()0-9]{1,40}(\*\*)?\s*(=|:|\||::)\s+")


def frame_skeleton(r):
    q = L.views(r)["q"]
    sc = side[r["id"]]; c = sc.get("c") or []
    q = IDR.sub("<e>", q)
    if c and isinstance(c[0], str):
        q = re.sub(r"\b%s\b" % re.escape(c[0]), "<p>", q)
    q = re.sub(r"<e> is (not )?(<p>|[\w-]+)", "<c>", q)
    q = re.sub(r"^(Q|Question|The question to answer)\s*:\s*", "", q)
    q = OUT.sub("<out>", q)
    q = re.sub(r"these [\w -]+?s(?= does| the record| for which| is |\?|,)", "these <type>s", q)
    q = re.sub(r"it is \w+\?", "it is <h>?", q)
    return q.strip()


def clause_skeleton(line, noun, persona):
    l = LISTM.sub("", line).strip()
    if not l or l.lower().startswith(("for example", "illustration", "sample", "example", "(e.g.", "e.g.")) or "EX-0" in l:
        return None
    l = LABEL.sub("", l)
    if persona and persona in l:
        return None
    if noun:
        l = re.sub(r"\b%ss?\b" % re.escape(noun), "<entity>", l)
    l = re.sub(r"Every [a-z ]+ in the record is given in [^,]+, the unit", "Every <quantity> in the record is given in <unit>, the unit", l)
    l = re.sub(r"only those from .+ count as facts", "only those from <sources> count as facts", l)
    return l if len(toks(l)) >= 6 else None


def spec_clause_seeds():
    """canonical clause lines from F4 G0 section 9 (column 4 quoted strings; one seed per numbered line)."""
    txt = open(L.F4 / "G0_SPEC.md").read()
    sec = txt[txt.index("## 9. Semantics table"):txt.index("## 10. Meta")]
    seeds = {}
    for line in sec.split("\n"):
        if not line.startswith("| ") or line.startswith("| #") or line.startswith("|---"):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split(" | ")]
        if len(cols) < 4:
            continue
        cid = cols[0]
        for j, q in enumerate(re.findall(r'"([^"]{20,})"', cols[3])):
            q = re.sub(r"<[^>]+>", "<slot>", q)
            seeds[f"clause{cid}.{j + 1}"] = q
    return seeds


def seeds_from_rows():
    frames, clauses = {}, {}
    for r in rows:
        f = frame_skeleton(r)
        if f:
            frames.setdefault(f, f)
        text = (r.get("card") or "") if r["qtype"] == "noul" else r["instructions"]
        m = re.search(r"Each (.+?) has exactly one type", text)
        noun = m.group(1) if m else None
        pm = re.search(r"(?:You are the|Reader: the|Role:) ([^.\n]+)", text)
        persona = pm.group(1) if pm else None
        for line in text.split("\n"):
            s = clause_skeleton(line, noun, persona)
            if s and "?" not in s:
                clauses.setdefault(s, s)
    return frames, clauses


def bleu4(hyp, refs):
    from collections import Counter as C
    ps = []
    for n in range(1, 5):
        h = C(tuple(hyp[i:i + n]) for i in range(len(hyp) - n + 1))
        mx = C()
        for ref in refs:
            rc = C(tuple(ref[i:i + n]) for i in range(len(ref) - n + 1))
            for g in h:
                mx[g] = max(mx[g], rc[g])
        num = sum(min(c, mx[g]) for g, c in h.items()); den = max(1, sum(h.values()))
        ps.append((num + 1) / (den + 1))
    rl = min((abs(len(r) - len(hyp)), len(r)) for r in refs)[1]
    bp = 1.0 if len(hyp) > rl else math.exp(1 - rl / max(1, len(hyp)))
    return bp * math.exp(sum(math.log(p) for p in ps) / 4)


def self_bleu(texts):
    from collections import Counter as C
    tk = [toks(t) for t in texts]
    grams = [[C(tuple(t[i:i + n]) for i in range(len(t) - n + 1)) for n in range(1, 5)] for t in tk]
    scores = []
    for a in range(len(tk)):
        ps = []
        for n in range(4):
            h = grams[a][n]; mx = C()
            for b in range(len(tk)):
                if b != a:
                    mx |= grams[b][n]
            num = sum(min(c, mx[g]) for g, c in h.items()); den = max(1, sum(h.values()))
            ps.append((num + 1) / (den + 1))
        ln = [len(tk[b]) for b in range(len(tk)) if b != a]
        rl = min(ln, key=lambda x: (abs(x - len(tk[a])), x))
        bp = 1.0 if len(tk[a]) > rl else math.exp(1 - rl / max(1, len(tk[a])))
        scores.append(bp * math.exp(sum(math.log(p) for p in ps) / 4))
    return float(np.mean(scores))


def main():
    cards = {r["meta"]["card_id"] for r in rows}
    packs = {r["meta"]["domain_pack"] for r in rows}
    card_pack = {}
    for r in rows:
        card_pack.setdefault(r["meta"]["card_id"], set()).add(r["meta"]["domain_pack"])
    sm = Counter(r["meta"]["sampler"] for r in rows)
    counts = {"cards": len(cards), "packs": len(packs), "one_pack_per_card": all(len(v) == 1 for v in card_pack.values()),
              "samplers": dict(sorted(sm.items()))}
    counts_ok = (len(cards) >= 80 and len(packs) >= 30 and counts["one_pack_per_card"] and set(sm) <= {"S1", "S2", "S3", "S4"}
                 and len(sm) >= 4 and max(sm.values()) <= 2500)
    frame_tag = lambda r: next((e for e in r["meta"]["edge"] if e.startswith("frame:")), "frame:none")
    st = Counter((r["meta"]["wording_id"], frame_tag(r)) for r in rows); n = len(rows)
    surf = {"definition": "(wording_id, frame:<frame>/<paraphrase>) pair (F4 G0 11)", "n_templates": len(st),
            "max_share_pct": round(100 * max(st.values()) / n, 3), "max_count": max(st.values()),
            "info_max_share_pct": {"wording_id": round(100 * max(Counter(r["meta"]["wording_id"] for r in rows).values()) / n, 2),
                                   "frame_paraphrase": round(100 * max(Counter(frame_tag(r) for r in rows).values()) / n, 2),
                                   "format_style": round(100 * max(Counter(r["meta"]["format_style"] for r in rows).values()) / n, 2)}}
    wd = {}
    for l in open(L.LEAN / "c_src/formats/formats-2/wordings/family_pools.jsonl"):
        w = json.loads(l)
        if w.get("pool") == "F4":
            wd[w["id"]] = w["text"]
    used = {r["meta"]["wording_id"] for r in rows}
    ps = {}
    for f in sorted((L.LEAN / "c_src/packs").glob("packs-*/*.jsonl")):
        if "sealedqc" in f.name or "index" in f.name:
            continue
        for l in open(f):
            try:
                p = json.loads(l)
            except Exception:
                continue
            pid = p.get("pack_id") or p.get("id")
            if pid in packs and p.get("setting"):
                ps[pid] = p["setting"]
    frames, clauses = seeds_from_rows()
    seeds = {"wordings": max_pair(wd), "frame_skeletons": max_pair(frames), "clause_lines_spec9": max_pair(spec_clause_seeds()),
             "pack_settings": {**max_pair(ps), "found_of": len(packs)}}
    seeds["wordings"]["used_in_rows"] = len(used); seeds["wordings"]["pool_has_all_used"] = used <= set(wd)
    rng = random.Random(1111); samp = rng.sample(rows, 200)
    txt = "\n".join(r["state"] for r in rows).encode()
    metrics = {"gzip_ratio_state": round(len(gzip.compress(txt)) / len(txt), 4),
               "self_bleu4_state_200": round(self_bleu([r["state"] for r in samp]), 4)}
    cache = L.TMP / f"g8_emb_{NAME}.npz"
    if cache.exists():
        S = np.load(cache, allow_pickle=True)["S"].astype(np.float64)
        S = S / np.linalg.norm(S, axis=1, keepdims=True)
        ev = np.clip(np.linalg.eigvalsh(S.T @ S / len(S)), 1e-12, None)
        metrics["vendi_minilm_state"] = round(float(np.exp(-(ev * np.log(ev)).sum())), 2)
    metrics["vs_golden_train_fld_proofwriter"] = "not run (golden_train is outside this checker's allow-list; orchestrator item)"
    seeds_ok = all(v["max"] < 0.7 for v in seeds.values())
    res = {"gate": "G11", "file": f"out/{NAME}.jsonl", "rows": n, "counts": counts, "surface_template": surf,
           "claude_seeds_rouge_l": seeds, "corpus_metrics": metrics,
           "pass_parts": {"counts": counts_ok, "surface_template_le_2pct": surf["max_share_pct"] <= 2.0,
                          "seeds_rouge_l_lt_0.7": seeds_ok, "golden_train_comparison": "pending (orchestrator)"}}
    res["pass"] = counts_ok and surf["max_share_pct"] <= 2.0 and seeds_ok
    json.dump(res, open(L.QC / f"g11_{NAME}.json", "w"), indent=1)
    print(json.dumps({"pass": res["pass"], "pass_parts": res["pass_parts"], "seeds": {k: (v["n"], v["max"]) for k, v in seeds.items()},
                      "surface_max": surf["max_share_pct"], "metrics": metrics}))


if __name__ == "__main__":
    main()
