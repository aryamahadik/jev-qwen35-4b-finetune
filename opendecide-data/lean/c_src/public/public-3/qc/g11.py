#!/usr/bin/env python3
"""Recheck r1 (independent): spec 8 G11 diversity for public-3, the parts that apply to public rows. Counts only.
  template : "no surface template above 2% of a family" with the dataset as the family: a row's surface template is
             everything the model sees except the human record (qtype, card, instructions, the state with each record
             text replaced by a slot, the options unless they are records). Max template share per dataset <= 2%.
  vs golden: "compression ratio, Self-BLEU and Vendi score no worse than the same family's slice of golden_train":
             each dataset vs C1's golden_train rows of the same dataset (equal-size seeded samples, n = min(both, 600);
             text = instructions + state + options). Compression ratio = raw / zlib bytes (lower = more diverse);
             Self-BLEU-4 against all other sample texts (lower = more diverse); Vendi on TF-IDF 1-2 gram cosine
             (higher = more diverse). Pass when ours is no worse on all three.
  n/a      : card / pack / sampler counts of 2.1 (own families only; spec 6: >= 3 wordings per public dataset, in
             qc/g1.json shape) and Claude-seed ROUGE-L (public rows carry no Claude seed text).
Writes qc/g11.json."""
import hashlib, json, math, random, re, zlib
from collections import Counter, defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import qclib as Q

GT = Q.P3.parents[2] / "data/v14_parts/golden_train.jsonl"
SLICE = {"c_pub_xed": {"br_xed_en"}, "c_pub_mams": {"br_mams_acsa"}, "c_pub_sarcasm": {"br_sarcasm_headlines"},
         "c_pub_edos": {"br_edos", "gd_edos_sexism"}}
W = re.compile(r"\w+")


def template(r):
    texts, _ = Q.record_texts(r)
    st = r["state"] or ""
    for t in sorted(texts, key=len, reverse=True):
        st = st.replace(t, "⟨REC⟩")
    rec_opts = isinstance(r["meta"].get("record_uid"), list) and len(r["meta"]["record_uid"]) > 1
    return json.dumps([r["qtype"], r["card"], r["instructions"], st, None if rec_opts else r["options"]])


def text(r):
    return "\n".join([r.get("instructions") or "", r.get("state") or ""] + [str(o) for o in (r.get("options") or [])])


def self_bleu(docs):
    toks = [W.findall(d.lower()) for d in docs]
    grams = [[Counter(tuple(t[i:i + n]) for i in range(len(t) - n + 1)) for n in range(1, 5)] for t in toks]
    df = [defaultdict(list) for _ in range(4)]
    for j, g in enumerate(grams):
        for n in range(4):
            for k, c in g[n].items():
                df[n][k].append((c, j))
    scores = []
    for j, g in enumerate(grams):
        logp, ok = 0.0, True
        for n in range(4):
            tot = sum(g[n].values())
            if tot == 0:
                ok = False
                break
            m = 0
            for k, c in g[n].items():
                ref = max((cc for cc, jj in df[n][k] if jj != j), default=0)
                m += min(c, ref)
            logp += math.log((m + 1) / (tot + 1)) / 4          # add-one smoothing (both sides alike)
        if ok:
            scores.append(math.exp(logp))
    return float(np.mean(scores))


def vendi(docs):
    X = TfidfVectorizer(ngram_range=(1, 2), token_pattern=r"\w+").fit_transform(docs)
    K = (X @ X.T).toarray() / len(docs)
    ev = np.linalg.eigvalsh(K)
    ev = ev[ev > 1e-12]
    return float(math.exp(-(ev * np.log(ev)).sum()))


def cr(docs):
    raw = "\n".join(docs).encode()
    return len(raw) / len(zlib.compress(raw, 9))


def metrics(docs):
    return {"n": len(docs), "compression_ratio": round(cr(docs), 4), "self_bleu4": round(self_bleu(docs), 4),
            "vendi": round(vendi(docs), 2)}


def main():
    rows = [r for n in Q.MIXED for r in Q.load(n)]
    by = defaultdict(list)
    for r in rows:
        by[r["source"]].append(r)
    res, prob = {"template": {}, "vs_golden": {}}, []
    for ds, rs in sorted(by.items()):
        c = Counter(template(r) for r in rs)
        top = c.most_common(1)[0][1]
        matched = sum(Q.record_texts(r)[1] for r in rs)
        res["template"][ds] = {"rows": len(rs), "templates": len(c), "max_template_rows": top,
                               "max_share": round(top / len(rs), 4), "record_wrap_matched": matched}
        if top / len(rs) > 0.02:
            prob.append(f"template share {ds}")
    want = set().union(*SLICE.values())
    gt = defaultdict(list)
    with open(GT, encoding="utf-8") as f:
        for line in f:
            if '"source"' in line and any(s in line for s in want):
                r = json.loads(line)
                if r.get("source") in want:
                    gt[r["source"]].append(text(r))
    for ds, rs in sorted(by.items()):
        g = [t for s in SLICE[ds] for t in gt[s]]
        n = min(len(rs), len(g), 600)
        key = lambda t: hashlib.sha256(("g11|" + t).encode()).hexdigest()
        ours = sorted((text(r) for r in rs), key=key)[:n]
        theirs = sorted(g, key=key)[:n]
        a, b = metrics(ours), metrics(theirs)
        ok = a["compression_ratio"] <= b["compression_ratio"] and a["self_bleu4"] <= b["self_bleu4"] and a["vendi"] >= b["vendi"]
        res["vs_golden"][ds] = {"golden_slice": sorted(SLICE[ds]), "golden_rows": len(g), "ours": a, "golden": b, "no_worse": ok}
        if not ok:
            prob.append(f"diversity vs golden_train {ds}")
    out = {"gate": "G11", "pass": not prob, "problems": prob, **res,
           "n_a": ["2.1 card / pack / sampler counts (own families)", "Claude-seed ROUGE-L (no Claude seeds)"]}
    (Q.HERE / "g11.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out)[:2500])


if __name__ == "__main__":
    main()
