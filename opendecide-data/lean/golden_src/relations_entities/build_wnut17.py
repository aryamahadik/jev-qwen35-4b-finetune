"""Build raw rows for wnut17 (WNUT 2017 Emerging and Rare Entities; Derczynski et al., W-NUT 2017).

Source : GitHub leondz/emerging_entities_17 @e52a2d2a, wnut17train.conll ONLY (the dev/test files, which hold the
         YouTube, Reddit and Stack Overflow text, are never used as rows). sha256 pinned. The two Stack Overflow source
         files (source/stacko.dev, source/stacko.test) are downloaded only as an exclusion list (no Stack Exchange text).
Licence: CC BY 4.0 (README.md of the repo: "This data is distributed under the CC-BY 4.0 license").
Texts  : English tweets (the training part comes from the WNUT 2016 Twitter NER data), annotated by CrowdFlower workers
         and adjudicated by NLP researchers for 6 entity types: person, location, group, creative work, corporation,
         product.
Task   : entity typing. State = the tweet with ONE entity mention wrapped in <e>...</e>; options = the 6 WNUT17 types;
         gold = the adjudicated type. One row per tweet (a tweet is never shown twice); the marked entity is chosen
         round-robin by type (rarest first) so person/location do not dominate.
Defs   : follow the WNUT17 guideline conventions as the annotators applied them (review fix 2026-09-29): websites,
         social networks and online services (Twitter 37x, Facebook 14x, YouTube 13x in train) are corporation, not
         product; video games are product, not creative work; TV channels are corporation.
Checks : tweets overlapping the Stack Overflow files, label-NLI (e.g. tweet_eval), local train/dev/eval files or other
         v14 parts are dropped; exact/near-duplicate tweets dropped.
Deterministic (seed 20261129).
"""
import collections
import html
import random

import _re_common as C

KEY = "wnut17"
COMMIT = "e52a2d2a71ac1a051ca2d532eef28653c5c02603"
BASE = f"https://raw.githubusercontent.com/leondz/emerging_entities_17/{COMMIT}/"
FILES = {"wnut17train.conll": "731820e13f71af324c6b55a1575ec2ce59fbaa2a0806f8f0400b98d56cd6a7a5",
         "source/stacko.dev": "42e76c2b85e416c93c1b92056aa448a198e3b39cc81783a218cfc8103980512a",
         "source/stacko.test": "e41280b6806eef6e8bdb3b18de353dd09adaa56479228141b680382099c9208f"}
LICENCE = (f"CC BY 4.0 (https://github.com/leondz/emerging_entities_17/blob/{COMMIT}/README.md, 'This data is "
           "distributed under the CC-BY 4.0 license')")
DATASET = "WNUT 2017 Emerging Entities (leondz/emerging_entities_17), wnut17train.conll"
TYPES = {
    "person": ("person", "A named individual person, real or fictional, including first names, nicknames and stage names (e.g. 'Rashad', 'Kanye', 'Harry Potter'); not a band or team."),
    "location": ("location", "A named place: country, city, region, street, venue, building, landmark or geographic feature (e.g. 'London', 'Empire State Building')."),
    "group": ("group", "A named group of people that is not a company: band, sports team, political party, government agency, club, charity or other organisation (e.g. 'Nirvana', 'San Diego Padres', 'FDA')."),
    "corporation": ("corporation", "A named company or business, including websites, social networks and online services (e.g. 'Google', 'Twitter', 'Facebook', 'YouTube', 'Walmart') and TV channels (e.g. 'MTV'), even when the site or app is meant."),
    "product": ("product", "A named product sold or used as a thing: device, gadget, food or drink brand, clothing, video game or software package (e.g. 'iPhone', 'Xbox', 'Pringles', 'Halo Reach', 'iOS'); websites and social networks are corporation."),
    "creative-work": ("creative work", "The title of a creative work: song, album, film, TV show, book, artwork or play (e.g. 'Game of Thrones', 'Thriller'); video games count as product."),
}
Q = 'What type of named entity is "{m}" (marked <e>) in this post?'


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


def main():
    rng = random.Random(C.SEED)
    paths = {}
    for rel, sha in FILES.items():
        paths[rel] = C.fetch(BASE + rel, C.CACHE / KEY / rel.replace("/", "_"), sha)
    sents = read_conll(paths["wnut17train.conll"])  # TRAIN ONLY
    stacko = [ln.strip() for rel in ("source/stacko.dev", "source/stacko.test")
              for ln in open(paths[rel], encoding="utf-8", errors="replace") if ln.strip()]
    recs = []
    for i, s in enumerate(sents):
        sp = [x for x in spans(s) if x[2] in TYPES]
        if not sp:
            continue
        toks = [html.unescape(t) for t, _ in s]
        recs.append({"i": i, "toks": toks, "spans": sp, "text": C.detok(toks)})
    print("tweets:", len(sents), "with entities:", len(recs))
    core = {str(r["i"]): [r["text"]] for r in recs}
    hits = C.decon(core, KEY, extra_texts={"stackoverflow": stacko})
    hits.update(C.cross_v14(core, {KEY}))
    nd = C.NearDup(thr=0.7)
    ok = []
    for r in recs:
        if str(r["i"]) in hits or len(C.words(r["text"])) < 4 or nd.seen(r["text"]):
            continue
        ok.append(r)
    print("after decon/dedupe:", len(ok), dict(collections.Counter(v.split(":")[0] for v in hits.values())))
    pools = collections.defaultdict(list)
    for r in ok:
        for sp in r["spans"]:
            pools[sp[2]].append((r, sp))
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
                if r["i"] in used:
                    continue
                used.add(r["i"])
                picked.append((r, sp))
                progressed = True
                break
        if not progressed:
            break
    rows = []
    for r, (a, b, typ) in picked:
        toks = list(r["toks"])
        toks[a] = "<e>" + toks[a]
        toks[b - 1] = toks[b - 1] + "</e>"
        state = C.detok(toks)
        mention = C.detok(r["toks"][a:b])
        opts = [v[0] for v in TYPES.values()]
        rng.shuffle(opts)
        tags = []
        plain = C.strip_markers(state)
        if C.NEG.search(plain):
            tags.append("negation")
        if mention.startswith(("@", "#")) or mention.islower():
            tags.append("implicit")  # handle, hashtag or lower-case mention: no capitalisation cue
        rows.append({
            "key": KEY,
            "rid": f"wnut17train:{r['i']}:{a}-{b}",
            "state": state,
            "instructions": Q.format(m=mention),
            "options": opts,
            "gold": TYPES[typ][0],
            "soft": None,
            "meta": {"dataset": DATASET, "config": "entity typing, 6 WNUT17 types",
                     "revision": f"git:{COMMIT}; sha256:{FILES['wnut17train.conll']}", "licence": LICENCE,
                     "split": "train", "orig_label": typ, "family": C.FAMILY, "edge": C.edge_join(tags)},
        })
    rng.shuffle(rows)
    defs = {v[0]: v[1] for v in TYPES.values()}
    C.write_outputs(KEY, rows, {None: defs})
    st = C.summary(KEY, rows)
    C.show_samples(rows, 5)
    notes = ("WNUT17 train tweets (crowd annotation + expert adjudication). Entity typing: one mention per tweet "
             "marked <e>, 6 types (person, location, group, corporation, product, creative work; group vs "
             "corporation and corporation vs product are the near-misses). Mention chosen round-robin by type. Stack "
             "Overflow dev/test sources used only as an exclusion list; label-NLI/local/v14 overlaps dropped."
             " Review fix: defs follow the WNUT17 conventions (websites/social networks = corporation; video games = product).")
    C.append_manifest(C.manifest_record(KEY, DATASET, LICENCE, rows, "choice (6 entity types)", notes, st))


if __name__ == "__main__":
    main()
