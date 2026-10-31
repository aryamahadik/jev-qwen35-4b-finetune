"""Build raw rows for biored (BioRED: document-level biomedical relation extraction, NCBI/NLM; Luo et al. 2022).

Source : https://ftp.ncbi.nlm.nih.gov/pub/lu/BioRED/BIORED.zip (sha256 pinned), BioRED/Train.PubTator ONLY (Dev and
         Test never read). Annotation guideline: BioRED_Annotation_Guideline.pdf in the same FTP folder.
Licence: US Government Work, public domain: https://ftp.ncbi.nlm.nih.gov/pub/lu/BioRED/README.txt ("PUBLIC DOMAIN
         NOTICE ... This software/database is a 'United States Government Work' ... freely available to the public for
         use. The National Library of Medicine and the U.S. Government have not placed any restriction on its use or
         reproduction.").
Texts  : 400 PubMed titles+abstracts; human curators annotated genes, chemicals, diseases, variants, species and cell
         lines (normalised to database ids) and document-level relations between concept pairs, 8 relation types.
Task   : relation classification over a whole abstract (long context). State = title + abstract with EVERY mention of
         concept 1 wrapped in <e1>...</e1> and every mention of concept 2 in <e2>...</e2> (a mention counts when its
         identifier list contains the concept id). Options = the 8 BioRED relation types. BioRED relations are
         non-directional; entity 1/2 follow the order of the annotation line.
Rows   : ONE row per abstract (an abstract is never shown twice): the pair is chosen round-robin by relation type
         (rarest first) so Association stays below 50%. Pairs whose e1/e2 mentions overlap are skipped.
Checks : abstracts sharing a 10-word run with PubMed 20k RCT, Medical Abstracts TC, SciFact, PubMedQA, DDI 2013
         (OHS-1/2), FewRel PubMed files (OHS-3), label-NLI, local files or other v14 parts (incl. drugprot) are
         dropped whole.
Deterministic (seed 20261129).
"""
import collections
import random
import re
import zipfile

import _re_common as C

KEY = "biored"
URL = "https://ftp.ncbi.nlm.nih.gov/pub/lu/BioRED/BIORED.zip"
SHA = "c3032230bd89d22a0923d0df6ae943bc8ea37fba7e42dafa7a8dec21bac02d47"
LICENCE = ("Public domain, US Government Work (NCBI/NLM PUBLIC DOMAIN NOTICE in "
           "https://ftp.ncbi.nlm.nih.gov/pub/lu/BioRED/README.txt)")
DATASET = "BioRED (NCBI, ftp.ncbi.nlm.nih.gov/pub/lu/BioRED/BIORED.zip), Train.PubTator"
LABELS = {
    "Association": ("association", "The abstract links the two concepts without a stated direction: a genetic association, a regulation or modification whose effect is not called increasing or decreasing, or any link fitting no other type."),
    "Positive_Correlation": ("positive correlation", "One concept raises the other or its risk, level or activity: a chemical induces a disease, a gene or variant increases disease risk, upregulation, or drug response/sensitivity."),
    "Negative_Correlation": ("negative correlation", "One concept lowers the other or its risk, level or activity: a drug treats or prevents a disease, a protective gene or variant, downregulation, inhibition, or drug resistance."),
    "Bind": ("bind", "The two concepts physically bind: protein-protein binding, or a chemical binding a protein as its ligand or receptor."),
    "Cotreatment": ("cotreatment", "The two chemicals are given together as a combined treatment."),
    "Drug_Interaction": ("drug interaction", "The two drugs interact: taking them together changes their effect or toxicity (a pharmacodynamic or pharmacokinetic drug-drug interaction)."),
    "Comparison": ("comparison", "The two chemicals are compared with each other, e.g. their efficacy, potency or side effects are evaluated side by side."),
    "Conversion": ("conversion", "One chemical is converted into the other (a metabolic or chemical transformation)."),
}
TYPES = {"GeneOrGeneProduct": "gene/protein", "ChemicalEntity": "chemical", "DiseaseOrPhenotypicFeature": "disease",
         "SequenceVariant": "variant", "OrganismTaxon": "species", "CellLine": "cell line"}
Q = ('Which relation does the abstract state between the {t1} "{n1}" (marked <e1>) and the {t2} "{n2}" (marked <e2>)?')


def parse(raw):
    docs = []
    for block in raw.replace("\r", "").strip().split("\n\n"):
        lines = block.split("\n")
        pmid, _, title = lines[0].split("|", 2)
        _, _, abstract = lines[1].split("|", 2)
        ments, rels = [], []
        for ln in lines[2:]:
            f = ln.split("\t")
            if len(f) == 6:
                ments.append({"s": int(f[1]), "e": int(f[2]), "text": f[3], "type": f[4], "ids": f[5].split(",")})
            elif len(f) == 5:
                rels.append({"type": f[1], "a": f[2], "b": f[3], "novel": f[4]})
        docs.append({"pmid": pmid, "title": title, "abstract": abstract, "ments": ments, "rels": rels})
    return docs


def mark(text, spans, lo):
    """Insert tags for spans [(s, e, tag)] (absolute offsets) that fall in text starting at offset lo."""
    out, prev = [], 0
    for s, e, tag in sorted(spans):
        s, e = s - lo, e - lo
        if s < 0 or e > len(text):
            continue
        out.append(text[prev:s])
        out.append(f"<{tag}>{text[s:e]}</{tag}>")
        prev = e
    out.append(text[prev:])
    return "".join(out)


def main():
    rng = random.Random(C.SEED)
    zp = C.fetch(URL, C.CACHE / KEY / "BIORED.zip", SHA)
    with zipfile.ZipFile(zp) as zf:
        docs = parse(zf.read("BioRED/Train.PubTator").decode("utf-8"))  # TRAIN ONLY
    assert len(docs) == 400, len(docs)
    for d in docs:
        full = d["title"] + " " + d["abstract"]
        for m in d["ments"]:
            assert full[m["s"]:m["e"]] == m["text"], (d["pmid"], m)

    core = {d["pmid"]: [d["title"] + " " + d["abstract"]] for d in docs}
    extra = C.pubmed_ohs_texts()
    extra.update({k: v for k, v in C.ohs3_wiki_texts().items() if k == "fewrel"})
    hits = C.decon(core, KEY, extra_texts=extra)
    hits.update(C.cross_v14(core, {KEY}))
    print("dropped abstracts:", len(hits), dict(collections.Counter(v.split(":")[0] for v in hits.values())))

    pools = collections.defaultdict(list)
    stats = collections.Counter()
    for d in docs:
        if d["pmid"] in hits:
            continue
        for r in d["rels"]:
            m1 = [m for m in d["ments"] if r["a"] in m["ids"]]
            m2 = [m for m in d["ments"] if r["b"] in m["ids"]]
            if not m1 or not m2:
                stats["no_mention"] += 1
                continue
            if any(x["s"] < y["e"] and y["s"] < x["e"] for x in m1 for y in m2):
                stats["overlap"] += 1
                continue
            pools[r["type"]].append((d, r, m1, m2))
    for k in pools:
        rng.shuffle(pools[k])
    print("pairs:", {k: len(v) for k, v in pools.items()}, dict(stats))
    order = sorted(pools, key=lambda k: (len(pools[k]), k))
    used, picked = set(), []
    ptr = {k: 0 for k in order}
    while True:
        progressed = False
        for k in order:
            while ptr[k] < len(pools[k]):
                d, r, m1, m2 = pools[k][ptr[k]]
                ptr[k] += 1
                if d["pmid"] in used:
                    continue
                used.add(d["pmid"])
                picked.append((d, r, m1, m2))
                progressed = True
                break
        if not progressed:
            break
    # Association cap (<= 48%)
    cnt = collections.Counter(r["type"] for _, r, _, _ in picked)
    while cnt["Association"] > 0.48 * len(picked):
        for i in range(len(picked) - 1, -1, -1):
            if picked[i][1]["type"] == "Association":
                picked.pop(i)
                cnt["Association"] -= 1
                break
    print("picked:", len(picked), dict(collections.Counter(r["type"] for _, r, _, _ in picked)))

    rows = []
    for d, r, m1, m2 in picked:
        spans = [(m["s"], m["e"], "e1") for m in m1] + [(m["s"], m["e"], "e2") for m in m2]
        tl = len(d["title"])
        title = mark(d["title"], [s for s in spans if s[1] <= tl], 0)
        abstract = mark(d["abstract"], [s for s in spans if s[0] > tl], tl + 1)
        state = C.clean(title + "\n" + abstract)
        n1, n2 = m1[0]["text"], m2[0]["text"]
        opts = [v[0] for v in LABELS.values()]
        rng.shuffle(opts)
        # negation / hedge tags only when the cue sits in a sentence that mentions one of the two concepts
        marked = [x for x in re.split(r"(?<=[.!?])\s+", state) if "<e1>" in x or "<e2>" in x]
        marked = " ".join(C.strip_markers(x) for x in marked)
        tags = ["long_context"]
        if C.NEG.search(marked):
            tags.append("negation")
        if C.HEDGE.search(marked):
            tags.append("hypothetical")
        rows.append({
            "key": KEY,
            "rid": f"{d['pmid']}:{r['a']}|{r['b']}",
            "state": state,
            "instructions": Q.format(t1=TYPES[m1[0]["type"]], n1=n1, t2=TYPES[m2[0]["type"]], n2=n2),
            "options": opts,
            "gold": LABELS[r["type"]][0],
            "soft": None,
            "meta": {"dataset": DATASET, "config": f"PMID {d['pmid']}; concept ids {r['a']} / {r['b']}",
                     "revision": f"ftp BIORED.zip (2022-04-07); sha256:{SHA}", "licence": LICENCE, "split": "train",
                     "orig_label": {"relation": r["type"], "novelty": r["novel"], "type1": m1[0]["type"],
                                    "type2": m2[0]["type"]},
                     "family": C.FAMILY, "edge": C.edge_join(tags)},
        })
    rng.shuffle(rows)
    defs = {v[0]: v[1] for v in LABELS.values()}
    C.write_outputs(KEY, rows, {None: defs})
    st = C.summary(KEY, rows)
    C.show_samples(rows, 5)
    notes = ("BioRED train (400 PubMed abstracts, NCBI curators). One row per abstract: all mentions of the two "
             "concepts marked <e1>/<e2> in title+abstract; options = the 8 BioRED relation types (association vs "
             "positive vs negative correlation are the hard near-misses); pair chosen round-robin by type, "
             "Association <= 48%. Abstracts overlapping PubMed OHS sources, FewRel PubMed, label-NLI, local files or "
             "other v14 parts dropped whole.")
    C.append_manifest(C.manifest_record(KEY, DATASET, LICENCE, rows, "choice (8 biomedical relation types)", notes, st))


if __name__ == "__main__":
    main()
