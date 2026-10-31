"""Build raw rows for crossner (CrossNER: cross-domain fine-grained NER; Liu et al., AAAI 2021).

Source : GitHub zliucr/CrossNER @2e7ba2a7, ner_data/{politics,science,music,literature,ai}/train.txt ONLY (dev/test and
         the bundled CoNLL-2003 copy are never read). sha256 pinned.
Licence: MIT (https://github.com/zliucr/CrossNER/blob/2e7ba2a7798c961e3f29fbc51252c5a8d40224bf/LICENSE, covering the
         repository including ner_data/).
Texts  : English Wikipedia sentences per domain; entities pre-tagged from DBpedia links and then corrected by two expert
         annotators per domain (paper, section 3), domain-specific fine-grained types.
Task   : fine-grained entity typing. State = one sentence with ONE entity mention wrapped in <e>...</e>; options = the
         full type set of that domain (9-17 types, e.g. politician vs person, band vs musical artist, enzyme vs protein,
         algorithm vs task vs field); definitions are per domain (defs/crossner__<domain>.json). Mentions typed "misc"
         are never the gold (the catch-all is vague) but "miscellaneous" stays an option.
Rows   : one row per sentence; the marked entity is chosen round-robin by (domain, type), rarest first.
Checks : sentences overlapping Few-NERD / FewRel (OHS-3, both Wikipedia), label-NLI, local files or other v14 parts
         (incl. redocred/webred) are dropped; exact/near duplicates dropped.
Deterministic (seed 20261129).
"""
import collections
import random

import _re_common as C

KEY = "crossner"
COMMIT = "2e7ba2a7798c961e3f29fbc51252c5a8d40224bf"
BASE = f"https://raw.githubusercontent.com/zliucr/CrossNER/{COMMIT}/ner_data/"
FILES = {"politics": "1d8be31abb58463349496fe21b13d70114cf015294a9ff9cce77af9b83e8aa84", "science": "8f6a26096cc7be6790b5790bf5f5b5c8928d8b73d4632e7d45dc8bffad0504ac", "music": "3774c38e0ebbeb4b98dbfae137071e4911e8764cdb7f247599009841f68d9fb5", "literature": "0647e403a85040742c2f4041cf002146a81aa2e13adda19d0e82a8bcd493c18b", "ai": "484217a660f52927bd5157507c22fc103b36306364329f62f80fc8acb897b187"}
LICENCE = f"MIT (https://github.com/zliucr/CrossNER/blob/{COMMIT}/LICENSE)"
DATASET = "CrossNER (zliucr/CrossNER), ner_data/<domain>/train.txt"

COMMON = {
    "person": ("person", "A named person who is not in one of the more specific person types listed (e.g. not a {spec})."),
    "organisation": ("organisation", "A named organisation, company, agency or institution that is not one of the more specific organisation types listed ({spec})."),
    "location": ("location", "A named place that is not a country: city, region, state, building, venue, river or other geographic feature."),
    "country": ("country", "A named sovereign country or nation state (e.g. 'France', 'United States'), including historical countries."),
    "event": ("event", "A named event such as a war, festival, conference, ceremony, competition or historical episode{spec}."),
    "misc": ("miscellaneous", "A named entity that fits none of the other listed types (e.g. a nationality, language, law or other named thing)."),
    "award": ("award", "A named prize, award or honour (e.g. 'Nobel Prize in Physics', 'Grammy Award', 'Hugo Award')."),
}
DOMAIN = {
    "politics": {
        "politician": ("politician", "A named person active in politics: head of state or government, minister, legislator, party leader, candidate or official."),
        "politicalparty": ("political party", "A named political party or party alliance (e.g. 'United Russia', 'Labour Party')."),
        "election": ("election", "A named election or referendum (e.g. '1934 Australian federal election')."),
        "_spec": {"person": "politician", "organisation": "political party", "event": "; elections have their own type"},
    },
    "science": {
        "scientist": ("scientist", "A named person known as a scientist, researcher, physician or scholar in the natural sciences."),
        "university": ("university", "A named university, college or research institute."),
        "discipline": ("discipline", "A named scientific field or discipline (e.g. 'astrophysics', 'organic chemistry')."),
        "theory": ("theory", "A named scientific theory, law, hypothesis or principle (e.g. 'general relativity')."),
        "protein": ("protein", "A named protein, receptor, hormone or gene product that is not specifically named as an enzyme."),
        "enzyme": ("enzyme", "A named enzyme, a protein that catalyses a reaction (names often end in '-ase', e.g. 'DNA polymerase')."),
        "chemicalelement": ("chemical element", "A named chemical element (e.g. 'oxygen', 'uranium')."),
        "chemicalcompound": ("chemical compound", "A named chemical compound, molecule or material made of several elements (e.g. 'benzene', 'sodium chloride')."),
        "astronomicalobject": ("astronomical object", "A named star, planet, moon, galaxy, comet, asteroid or other celestial object."),
        "academicjournal": ("academic journal", "A named scientific or academic journal (e.g. 'Nature', 'Physical Review Letters')."),
        "_spec": {"person": "scientist", "organisation": "university", "event": ""},
    },
    "music": {
        "musicalartist": ("musical artist", "A named individual musician, singer, composer, rapper or DJ."),
        "band": ("band", "A named band, music group, orchestra or choir (more than one performer)."),
        "song": ("song", "The title of a named song, single or other short musical piece."),
        "album": ("album", "The title of a named album, EP or record."),
        "musicgenre": ("music genre", "A named genre or style of music (e.g. 'synthpop', 'jazz', 'Sacred Harp singing')."),
        "musicalinstrument": ("musical instrument", "A named musical instrument (e.g. 'Hammond organ', 'theremin')."),
        "_spec": {"person": "musical artist", "organisation": "band", "event": ""},
    },
    "literature": {
        "writer": ("writer", "A named person known as a writer, novelist, poet, playwright or author."),
        "book": ("book", "The title of a named book, novel, story collection or play."),
        "poem": ("poem", "The title of a named poem."),
        "magazine": ("magazine", "A named magazine, newspaper or literary periodical."),
        "literarygenre": ("literary genre", "A named literary genre or form (e.g. 'science fiction', 'sonnet', 'fairy tale')."),
        "_spec": {"person": "writer", "organisation": "magazine", "event": ""},
    },
    "ai": {
        "researcher": ("researcher", "A named person known as a researcher or scientist in computing or artificial intelligence."),
        "university": ("university", "A named university, college or research institute."),
        "conference": ("conference", "A named academic conference or workshop (e.g. 'NeurIPS', 'AAAI')."),
        "field": ("field", "A named research field or sub-field (e.g. 'machine learning', 'computer vision')."),
        "task": ("task", "A named problem or task that methods are built to solve (e.g. 'speech recognition', 'image segmentation')."),
        "algorithm": ("algorithm", "A named algorithm, model, method or technique (e.g. 'backpropagation', 'support vector machine')."),
        "metrics": ("metric", "A named evaluation metric or measure (e.g. 'F1 score', 'BLEU', 'mean squared error')."),
        "programlang": ("programming language", "A named programming language (e.g. 'Python', 'MATLAB', 'Lisp')."),
        "product": ("product", "A named software product, system, device or tool (e.g. 'Octave', 'TensorFlow', 'Siri')."),
        "_spec": {"person": "researcher", "organisation": "university or conference", "event": "; conferences have their own type"},
    },
}
Q = 'In this {d} text, what type of entity is "{m}" (marked <e>)?'
DOMAIN_WORD = {"politics": "politics", "science": "science", "music": "music", "literature": "literature",
               "ai": "artificial-intelligence"}


def read_conll(path):
    sents, cur = [], []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip():
            if cur:
                sents.append(cur)
                cur = []
            continue
        tok, lab = line.rsplit("\t", 1)
        cur.append((tok, lab))
    if cur:
        sents.append(cur)
    return sents


def spans(sent):
    out, i = [], 0
    while i < len(sent):
        lab = sent[i][1]
        if lab.startswith("B-"):
            typ, j = lab[2:], i + 1
            while j < len(sent) and sent[j][1] == "I-" + typ:
                j += 1
            out.append((i, j, typ))
            i = j
        else:
            i += 1
    return out


def domain_defs(dom, types):
    spec = DOMAIN[dom]["_spec"]
    out = {}
    for t in types:
        if t in DOMAIN[dom] and t != "_spec":
            n, d = DOMAIN[dom][t]
        else:
            n, d = COMMON[t]
            d = d.format(spec=spec.get(t, ""))
        out[t] = (n, d)
    return out


def main():
    rng = random.Random(C.SEED)
    data = {}
    for dom, sha in FILES.items():
        p = C.fetch(BASE + f"{dom}/train.txt", C.CACHE / KEY / f"{dom}_train.txt", sha)
        data[dom] = read_conll(p)  # TRAIN ONLY
    types = {dom: sorted({sp[2] for s in ss for sp in spans(s)}) for dom, ss in data.items()}
    defs = {dom: domain_defs(dom, ts) for dom, ts in types.items()}
    recs = []
    for dom, ss in sorted(data.items()):
        for i, s in enumerate(ss):
            sp = spans(s)
            if not sp:
                continue
            recs.append({"dom": dom, "i": i, "toks": [t for t, _ in s], "spans": sp,
                         "text": C.detok([t for t, _ in s])})
    print("sentences with entities:", len(recs), {d: len(v) for d, v in data.items()})
    core = {f"{r['dom']}:{r['i']}": [r["text"]] for r in recs}
    hits = C.decon(core, KEY, extra_texts=C.ohs3_wiki_texts())
    hits.update(C.cross_v14(core, {KEY}))
    print("dropped:", len(hits), dict(collections.Counter(v.split(":")[0] for v in hits.values())))
    nd = C.NearDup(thr=0.7)
    ok = [r for r in recs if f"{r['dom']}:{r['i']}" not in hits and not nd.seen(r["text"])]
    pools = collections.defaultdict(list)
    for r in ok:
        for sp in r["spans"]:
            if sp[2] != "misc":
                pools[(r["dom"], sp[2])].append((r, sp))
    for k in pools:
        rng.shuffle(pools[k])
    order = sorted(pools, key=lambda k: (len(pools[k]), k))
    used, picked, ptr = set(), [], {k: 0 for k in order}
    while True:
        progressed = False
        for k in order:
            while ptr[k] < len(pools[k]):
                r, sp = pools[k][ptr[k]]
                ptr[k] += 1
                if (r["dom"], r["i"]) in used:
                    continue
                used.add((r["dom"], r["i"]))
                picked.append((r, sp))
                progressed = True
                break
        if not progressed:
            break
    rows = []
    for r, (a, b, typ) in picked:
        dom = r["dom"]
        toks = list(r["toks"])
        toks[a] = "<e>" + toks[a]
        toks[b - 1] = toks[b - 1] + "</e>"
        state = C.detok(toks)
        mention = C.detok(r["toks"][a:b])
        opts = [defs[dom][t][0] for t in types[dom]]
        rng.shuffle(opts)
        tags = []
        if C.NEG.search(C.strip_markers(state)):
            tags.append("negation")
        rows.append({
            "key": KEY,
            "rid": f"{dom}:train:{r['i']}:{a}-{b}",
            "state": state,
            "instructions": Q.format(d=DOMAIN_WORD[dom], m=mention),
            "options": opts,
            "gold": defs[dom][typ][0],
            "soft": None,
            "meta": {"dataset": DATASET, "config": f"domain={dom}; {len(types[dom])} types",
                     "revision": f"git:{COMMIT}; sha256:{FILES[dom]}",
                     "licence": LICENCE, "split": "train", "orig_label": typ, "family": C.FAMILY,
                     "edge": C.edge_join(tags), "defs": dom},
        })
    rng.shuffle(rows)
    defs_by_qid = {None: {}}
    for dom in defs:
        defs_by_qid[dom] = {n: d for n, d in defs[dom].values()}
    del defs_by_qid[None]
    C.write_outputs(KEY, rows, defs_by_qid)
    st = C.summary(KEY, rows)
    print("per domain:", collections.Counter(r["meta"]["defs"] for r in rows))
    C.show_samples(rows, 5)
    notes = ("CrossNER train (Wikipedia; DBpedia pre-tags corrected by expert annotators). Fine-grained entity "
             "typing, one marked mention per sentence, options = the domain's 9-17 types with per-domain defs "
             "(defs/crossner__<domain>.json); misc never gold. Mention chosen round-robin by (domain, type). "
             "Few-NERD/FewRel (OHS-3), label-NLI, local and v14 overlaps dropped.")
    C.append_manifest(C.manifest_record(KEY, DATASET, LICENCE, rows, "choice (9-17 fine-grained entity types)",
                                        notes, st))


if __name__ == "__main__":
    main()
