"""Build raw rows for ncbi_disease (NCBI Disease Corpus; Islamaj Dogan, Leaman & Lu, J Biomed Inform 2014).

Source : https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/NCBItrainset_corpus.zip (sha256 pinned), the TRAIN set
         only (593 PubMed abstracts; the development and test sets are never downloaded).
Licence: US Government Work, public domain: PUBLIC DOMAIN NOTICE at
         https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/disclaimer.html ("The data is freely available to the
         public for use. The National Library of Medicine and the U.S. Government have not placed any restriction on
         its use or reproduction.").
Labels : 14 annotators (two per abstract, disagreements resolved) marked every disease mention in PubMed titles and
         abstracts with one of 4 mention categories defined in the corpus guidelines
         (https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/Guidelines.html): SpecificDisease, DiseaseClass,
         Modifier, CompositeMention.
Task   : mention-category typing. State = one sentence (title or abstract sentence) with ONE disease mention wrapped in
         <e>...</e>; options = the 4 categories; the hard boundaries are specific disease vs disease class (one disease
         vs a family of diseases) and noun-phrase use vs modifier use of the same name.
Rows   : one row per sentence (a sentence is never shown twice); the mention is chosen round-robin by category
         (rarest first) so SpecificDisease stays below 50%.
Split  : review fix (2026-09-29): a '13. 8%'-style decimal point followed by a space in the source text is no
         longer treated as a sentence boundary (it produced fragments such as '8% of northern Chinese ... (2.').
Checks : sentences overlapping PubMed 20k RCT, Medical Abstracts TC, SciFact, PubMedQA, DDI 2013 (OHS-1/2), FewRel
         PubMed files (OHS-3), label-NLI, local files or other v14 parts (incl. biored, drugprot) are dropped.
Deterministic (seed 20261129).
"""
import collections
import random
import zipfile

import _re_common as C

KEY = "ncbi_disease"
URL = "https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/NCBItrainset_corpus.zip"
SHA = "26157233d70aeda0b2ac1dda4fc9369b0717bd888f5afe511d0c1c6a5ad307a0"
LICENCE = ("Public domain, US Government Work (NCBI PUBLIC DOMAIN NOTICE, "
           "https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/disclaimer.html)")
DATASET = "NCBI Disease Corpus (NCBI/NLM), NCBItrainset_corpus.zip (train set)"
CATS = {
    "SpecificDisease": ("specific disease", "The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC')."),
    "DiseaseClass": ("disease class", "The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders')."),
    "Modifier": ("modifier", "The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients')."),
    "CompositeMention": ("composite mention", "One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers')."),
}
Q = 'According to the NCBI disease-mention categories, what kind of disease mention is "{m}" (marked <e>) in this sentence?'


def parse(raw):
    docs = []
    for block in raw.replace("\r", "").strip().split("\n\n"):
        lines = [ln for ln in block.split("\n") if ln.strip()]
        pmid, _, title = lines[0].split("|", 2)
        _, _, abstract = lines[1].split("|", 2)
        ments = []
        for ln in lines[2:]:
            f = ln.split("\t")
            if len(f) == 6:
                ments.append({"s": int(f[1]), "e": int(f[2]), "text": f[3], "cat": f[4], "id": f[5]})
        docs.append({"pmid": pmid, "title": title, "abstract": abstract, "ments": ments})
    return docs


def main():
    rng = random.Random(C.SEED)
    zp = C.fetch(URL, C.CACHE / KEY / "NCBItrainset_corpus.zip", SHA)
    with zipfile.ZipFile(zp) as zf:
        docs = parse(zf.read("NCBItrainset_corpus.txt").decode("utf-8"))  # TRAIN ONLY
    assert len(docs) == 593, len(docs)
    sents = {}
    for d in docs:
        full = d["title"] + " " + d["abstract"]
        for m in d["ments"]:
            # one mention in the release replaces quote marks by spaces in its text column; the offsets are right
            assert full[m["s"]:m["e"]].replace('"', " ") == m["text"], (d["pmid"], m)
            m["text"] = full[m["s"]:m["e"]]
        off = len(d["title"]) + 1
        prot = [(m["s"] - off, m["e"] - off) for m in d["ments"]]
        sp = [(0, len(d["title"]))] + [(a + off, b + off) for a, b in C.split_sentences(d["abstract"], prot)]
        d["full"] = full
        sents[d["pmid"]] = sp
    recs = []
    for d in docs:
        for si, (a, b) in enumerate(sents[d["pmid"]]):
            ms = [m for m in d["ments"] if a <= m["s"] and m["e"] <= b]
            if ms:
                recs.append({"pmid": d["pmid"], "si": si, "a": a, "b": b, "text": d["full"][a:b], "ments": ms,
                             "full": d["full"]})
    print("sentences with mentions:", len(recs))
    core = {f"{r['pmid']}:{r['si']}": [r["text"]] for r in recs}
    extra = C.pubmed_ohs_texts()
    extra.update({k: v for k, v in C.ohs3_wiki_texts().items() if k == "fewrel"})
    hits = C.decon(core, KEY, extra_texts=extra)
    hits.update(C.cross_v14(core, {KEY}))
    print("dropped:", len(hits), dict(collections.Counter(v.split(":")[0] for v in hits.values())))
    nd = C.NearDup(thr=0.7)
    ok = [r for r in recs if f"{r['pmid']}:{r['si']}" not in hits and len(C.words(r["text"])) >= 5
          and not nd.seen(r["text"])]
    pools = collections.defaultdict(list)
    for r in ok:
        for m in r["ments"]:
            pools[m["cat"]].append((r, m))
    for k in pools:
        rng.shuffle(pools[k])
    order = sorted(pools, key=lambda k: (len(pools[k]), k))
    used, picked, ptr = set(), [], {k: 0 for k in order}
    while True:
        progressed = False
        for k in order:
            while ptr[k] < len(pools[k]):
                r, m = pools[k][ptr[k]]
                ptr[k] += 1
                key = (r["pmid"], r["si"])
                if key in used:
                    continue
                used.add(key)
                picked.append((r, m))
                progressed = True
                break
        if not progressed:
            break
    cnt = collections.Counter(m["cat"] for _, m in picked)
    while cnt["SpecificDisease"] > 0.48 * len(picked):
        for i in range(len(picked) - 1, -1, -1):
            if picked[i][1]["cat"] == "SpecificDisease":
                picked.pop(i)
                cnt["SpecificDisease"] -= 1
                break
    rows = []
    for r, m in picked:
        s = r["full"]
        state = C.clean(s[r["a"]:m["s"]] + "<e>" + s[m["s"]:m["e"]] + "</e>" + s[m["e"]:r["b"]])
        opts = [v[0] for v in CATS.values()]
        rng.shuffle(opts)
        tags = []
        if sum(1 for x in r["ments"] if x["text"].lower() == m["text"].lower() and x["cat"] != m["cat"]):
            tags.append("ambiguous")  # the same string carries another category elsewhere in the sentence
        if C.NEG.search(C.strip_markers(state)):
            tags.append("negation")
        rows.append({
            "key": KEY,
            "rid": f"{r['pmid']}:{r['si']}:{m['s']}-{m['e']}",
            "state": state,
            "instructions": Q.format(m=m["text"]),
            "options": opts,
            "gold": CATS[m["cat"]][0],
            "soft": None,
            "meta": {"dataset": DATASET, "config": f"PMID {r['pmid']}, sentence {r['si']}",
                     "revision": f"NCBItrainset_corpus.zip (2012-11-07); sha256:{SHA}", "licence": LICENCE,
                     "split": "train", "orig_label": {"category": m["cat"], "concept": m["id"]},
                     "family": C.FAMILY, "edge": C.edge_join(tags)},
        })
    rng.shuffle(rows)
    defs = {v[0]: v[1] for v in CATS.values()}
    C.write_outputs(KEY, rows, {None: defs})
    st = C.summary(KEY, rows)
    C.show_samples(rows, 5)
    notes = ("NCBI Disease Corpus train set (PubMed titles/abstracts, 14 expert annotators). Mention-category typing: one "
             "disease mention per sentence marked <e>; options = specific disease / disease class / modifier / "
             "composite mention (guideline definitions). Mention chosen round-robin by category, SpecificDisease "
             "<= 48%. PubMed OHS sources, FewRel PubMed, label-NLI, local and v14 overlaps (incl. biored) dropped."
             " Review fix: '13. 8'-style decimals no longer split sentences.")
    C.append_manifest(C.manifest_record(KEY, DATASET, LICENCE, rows, "choice (4 disease-mention categories)", notes, st))


if __name__ == "__main__":
    main()
