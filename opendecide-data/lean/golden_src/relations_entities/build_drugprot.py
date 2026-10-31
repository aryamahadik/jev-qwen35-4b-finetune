"""Build raw rows for drugprot (DrugProt, BioCreative VII Track 1: chemical-protein relations in PubMed abstracts).

Source : Zenodo record 5119892 (official DrugProt release by the organisers), file
         drugprot-training-development-test-background.zip (sha256 pinned), version 1.2 (21 Jul 2021). Used: the
         training/ folder ONLY (drugprot_training_{abstracs,entities,relations}.tsv); development and test+background
         files are never read.
Licence: CC BY 4.0 (Zenodo record https://zenodo.org/records/5119892 metadata 'license: cc-by-4.0').
Texts  : 3,500 PubMed titles+abstracts. Labels: manual expert annotation of chemical and gene/protein mentions and of
         13 chemical-protein relation types (ChemProt guidelines revised for DrugProt; relation guidelines: Zenodo
         4957138, CC BY 4.0).
Task   : relation classification. State = the one sentence that contains both arguments, with the chemical mention
         wrapped in <e1>...</e1> and the gene/protein mention in <e2>...</e2>. Options = the 13 DrugProt relation types
         (fine-grained near-misses: direct inhibitor vs indirect downregulator vs antagonist, agonist vs
         agonist-activator, substrate vs product), minus any OTHER type annotated for the same mention pair (about 1%
         of pairs carry two labels, e.g. ACTIVATOR + INDIRECT-UPREGULATOR), so exactly one listed option is correct.
         No "no relation" option: unannotated pairs are not reliable negatives (the guidelines leave some regulation
         statements unlabelled), so only annotated pairs are asked.
Rows   : one row per sentence (a sentence is never shown twice); the pair is chosen round-robin by relation type
         (rarest first) so the frequent INHIBITOR class stays below 30%.
Split  : review fix (2026-09-29): a '13. 8%'-style decimal point followed by a space in the source text is no
         longer treated as a sentence boundary (it produced fragments such as '8% of northern Chinese ... (2.').
Checks : sentences overlapping PubMed 20k RCT, Medical Abstracts TC, SciFact, PubMedQA, DDI 2013 (OHS-1/2), FewRel
         (incl. its PubMed files; OHS-3), label-NLI, local files or other v14 parts are dropped. Exact and near
         duplicate sentences dropped.
Deterministic (seed 20261129).
"""
import collections
import csv
import io
import random
import re
import zipfile

import _re_common as C

KEY = "drugprot"
URL = "https://zenodo.org/api/records/5119892/files/drugprot-training-development-test-background.zip/content"
SHA = "679ca89698ca471a7fedc9af95acc8722c127c04eba19660fead406b5b9b52c9"
LICENCE = "CC BY 4.0 (Zenodo record https://zenodo.org/records/5119892 metadata 'license: cc-by-4.0'; DrugProt corpus v1.2)"
DATASET = "DrugProt (BioCreative VII Track 1), Zenodo 5119892, training set only"
TRAIN = "drugprot-gs-training-development/training/"
TARGET = 7000
CAP = {"INHIBITOR": 1450}

LABELS = {
    "INHIBITOR": ("inhibitor", "The chemical lowers the activity or function of the gene product, by binding it or with no mechanism stated ('X inhibits Y', 'Y inhibitor X'); lower amounts or expression of Y are indirect downregulation instead."),
    "ACTIVATOR": ("activator", "The chemical raises the activity or function of the gene product, by binding it or with no mechanism stated ('X activates Y', 'X enhanced Y activity'); higher amounts or expression of Y are indirect upregulation instead."),
    "INDIRECT-DOWNREGULATOR": ("indirect downregulator", "The chemical lowers the amount, expression, release or activity of the gene product through other targets: e.g. reduced Y mRNA or protein levels, decreased Y secretion or phosphorylation after X treatment."),
    "INDIRECT-UPREGULATOR": ("indirect upregulator", "The chemical raises the amount, expression, release or activity of the gene product through other targets: e.g. X induced Y expression, increased Y levels, secretion or phosphorylation after X treatment."),
    "DIRECT-REGULATOR": ("direct regulator (binder)", "The chemical binds or physically interacts with the gene product (binder, ligand, affinity, modulator) but the text does not say whether it activates, inhibits, agonises or antagonises it."),
    "AGONIST": ("agonist", "The chemical is an agonist of the gene product (usually a receptor) that binds and triggers its response, with no statement of whether the response is increased or decreased."),
    "AGONIST-ACTIVATOR": ("agonist-activator", "The chemical is an agonist stated to increase the receptor's response when it binds, typically called a full or partial agonist that activates the receptor."),
    "AGONIST-INHIBITOR": ("agonist-inhibitor", "The chemical is an agonist that binds the receptor and decreases its response, typically an inverse agonist."),
    "ANTAGONIST": ("antagonist", "The chemical is an antagonist or blocker of the gene product (usually a receptor): it binds and prevents or reduces the receptor's response to an agonist."),
    "SUBSTRATE": ("substrate", "The gene product (an enzyme or transporter) acts on the chemical: the chemical is metabolised, converted, modified or transported by it."),
    "PRODUCT-OF": ("product of", "The chemical is produced by the gene product: it is the product of the enzyme's reaction or is released or exported by the transporter."),
    "SUBSTRATE_PRODUCT-OF": ("substrate and product of", "The chemical is both a substrate and a product of the gene product's reaction, e.g. an enzyme that interconverts or exchanges that chemical."),
    "PART-OF": ("part of", "The chemical is a structural part of the gene product, e.g. an amino-acid residue (Ser-15, cysteine residues), a sugar chain or another chemical group within the protein."),
}
Q = ('Which chemical-protein relation does the sentence state between the chemical "{c}" (marked <e1>) and the gene or '
     'protein "{g}" (marked <e2>)?')
UNITS = re.compile(r"\d\s?(nM|µM|μM|uM|mM|pM|M|mg|µg|μg|ng|kg|%|mmol|µmol|μmol)\b")


def read_tsv(zf, name):
    return list(csv.reader(io.TextIOWrapper(zf.open(TRAIN + name), encoding="utf-8"), delimiter="\t",
                           quoting=csv.QUOTE_NONE))


def main():
    rng = random.Random(C.SEED)
    zp = C.fetch(URL, C.CACHE / KEY / "drugprot.zip", SHA)
    with zipfile.ZipFile(zp) as zf:
        abstracts = read_tsv(zf, "drugprot_training_abstracs.tsv")
        entities = read_tsv(zf, "drugprot_training_entities.tsv")
        relations = read_tsv(zf, "drugprot_training_relations.tsv")
    assert len(abstracts) == 3500
    txt, tl = {}, {}
    for pmid, title, abstract in abstracts:
        txt[pmid] = title + " " + abstract
        tl[pmid] = len(title)
    ents = collections.defaultdict(dict)
    for pmid, tid, typ, s, e, m in entities:
        ents[pmid][tid] = (typ, int(s), int(e), m)
        assert txt[pmid][int(s):int(e)] == m
    # sentence spans: title + split abstract (entity mentions are never split)
    sents = {}
    for pmid, t in txt.items():
        off = tl[pmid] + 1
        prot = [(e[1] - off, e[2] - off) for e in ents[pmid].values()]
        sents[pmid] = [(0, tl[pmid])] + [(a + off, b + off) for a, b in C.split_sentences(t[off:], prot)]

    def sid_of(pmid, s, e):
        for i, (a, b) in enumerate(sents[pmid]):
            if a <= s and e <= b:
                return i
        return None

    pair_labels = collections.defaultdict(set)
    for pmid, lab, a1, a2 in relations:
        pair_labels[(pmid, a1.split(":")[1], a2.split(":")[1])].add(lab)
    by_sent = collections.defaultdict(list)
    stats = collections.Counter()
    for (pmid, a1, a2), labs in sorted(pair_labels.items()):
        e1, e2 = ents[pmid][a1], ents[pmid][a2]
        assert e1[0] == "CHEMICAL" and e2[0].startswith("GENE")
        s1, s2 = sid_of(pmid, e1[1], e1[2]), sid_of(pmid, e2[1], e2[2])
        if s1 is None or s1 != s2:
            stats["cross_sentence"] += 1
            continue
        # crossing (non-nested) mention overlap cannot be marked
        (x1, y1), (x2, y2) = (e1[1], e1[2]), (e2[1], e2[2])
        if x1 < y2 and x2 < y1 and not ((x1 <= x2 and y2 <= y1) or (x2 <= x1 and y1 <= y2)):
            stats["crossing"] += 1
            continue
        if (x1, y1) == (x2, y2):
            stats["same_span"] += 1
            continue
        for lab in sorted(labs):
            by_sent[(pmid, s1)].append((lab, a1, a2, sorted(labs)))
    print("sentences with relations:", len(by_sent), dict(stats))

    # decontamination at sentence level
    core = {f"{p}:{s}": [txt[p][sents[p][s][0]:sents[p][s][1]]] for p, s in by_sent}
    extra = C.pubmed_ohs_texts()
    extra.update({k: v for k, v in C.ohs3_wiki_texts().items() if k == "fewrel"})
    hits = C.decon(core, KEY, extra_texts=extra)
    hits.update(C.cross_v14(core, {KEY}))
    print("dropped sentences:", len(hits), dict(collections.Counter(v.split(":")[0] for v in hits.values())))

    nd = C.NearDup(thr=0.7)
    keys = sorted(by_sent)
    rng.shuffle(keys)
    ok = []
    for k in keys:
        a, b = sents[k[0]][k[1]]
        s = txt[k[0]][a:b]
        if f"{k[0]}:{k[1]}" in hits or len(C.words(s)) < 5 or nd.seen(s):
            continue
        ok.append(k)
    pools = collections.defaultdict(list)
    for k in ok:
        for item in by_sent[k]:
            pools[item[0]].append((k, item))
    for lab in pools:
        rng.shuffle(pools[lab])
    order = sorted(pools, key=lambda l: (len(pools[l]), l))
    used, picked, cnt = set(), [], collections.Counter()
    ptr = {l: 0 for l in order}
    while len(picked) < TARGET:
        progressed = False
        for lab in order:
            if len(picked) >= TARGET or cnt[lab] >= CAP.get(lab, 10 ** 9):
                continue
            while ptr[lab] < len(pools[lab]):
                k, item = pools[lab][ptr[lab]]
                ptr[lab] += 1
                if k in used:
                    continue
                used.add(k)
                picked.append((k, item))
                cnt[lab] += 1
                progressed = True
                break
        if not progressed:
            break
    print("picked:", len(picked), dict(cnt))

    rows = []
    for (pmid, si), (lab, a1, a2, labs) in picked:
        a, b = sents[pmid][si]
        e1, e2 = ents[pmid][a1], ents[pmid][a2]
        ins = [(e1[1], 1, "<e1>"), (e1[2], 0, "</e1>"), (e2[1], 1, "<e2>"), (e2[2], 0, "</e2>")]
        # at equal offsets: closing tags first; for nested spans the outer opening tag comes first
        outer = "e1" if (e1[1] <= e2[1] and e2[2] <= e1[2]) else "e2"

        def okey(x):
            pos, is_open, tag = x
            if is_open:
                return (pos, 1, 0 if tag[1:3] == outer else 1)
            return (pos, 0, 0 if tag[2:4] != outer else 1)
        s = txt[pmid]
        out, prev = [], a
        for pos, is_open, tag in sorted(ins, key=okey):
            out.append(s[prev:pos])
            out.append(tag)
            prev = pos
        out.append(s[prev:b])
        state = C.clean("".join(out))
        other = [l for l in labs if l != lab]
        opts = [LABELS[l][0] for l in sorted(LABELS) if l not in other]
        rng.shuffle(opts)
        plain = C.strip_markers(state)
        tags = []
        if C.NEG.search(plain):
            tags.append("negation")
        if C.HEDGE.search(plain):
            tags.append("hypothetical")
        if UNITS.search(plain):
            tags.append("units")
        if len(C.words(plain)) > 60:
            tags.append("long_context")
        rows.append({
            "key": KEY,
            "rid": f"{pmid}:{si}:{a1}-{a2}",
            "state": state,
            "instructions": Q.format(c=e1[3], g=e2[3]),
            "options": opts,
            "gold": LABELS[lab][0],
            "soft": None,
            "meta": {"dataset": DATASET, "config": f"PMID {pmid}, sentence {si}"
                     + (f"; co-annotated {other} removed from options" if other else ""),
                     "revision": f"zenodo:5119892 v1.2; sha256:{SHA}", "licence": LICENCE, "split": "train",
                     "orig_label": {"relation": lab, "pair_labels": labs, "arg1": a1, "arg2": a2,
                                    "gene_type": e2[0]},
                     "family": C.FAMILY, "edge": C.edge_join(tags)},
        })
    rng.shuffle(rows)
    defs = {v[0]: v[1] for v in LABELS.values()}
    C.write_outputs(KEY, rows, {None: defs})
    st = C.summary(KEY, rows)
    C.show_samples(rows, 5)
    notes = ("DrugProt training set (PubMed abstracts, expert chemical/gene mentions and relations). One row per "
             "sentence: chemical <e1>, gene/protein <e2>; options = the 13 DrugProt relation types minus any other "
             "type co-annotated for the same mention pair. No 'no relation' option (unannotated pairs are not safe "
             "negatives). Pair chosen round-robin by type (rarest first, INHIBITOR capped). Sentences overlapping "
             "PubMed RCT / Medical Abstracts / SciFact / PubMedQA / DDI 2013 / FewRel, label-NLI, local files or other "
             "v14 parts dropped."
             " Review fix: '13. 8'-style decimals no longer split sentences.")
    C.append_manifest(C.manifest_record(KEY, DATASET, LICENCE, rows, "choice (13 chemical-protein relation types)",
                                        notes, st))


if __name__ == "__main__":
    main()
