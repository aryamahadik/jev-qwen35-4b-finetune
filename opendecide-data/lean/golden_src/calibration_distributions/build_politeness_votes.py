"""Build raw rows for politeness_votes (Stanford Politeness Corpus, Wikipedia half; Danescu-Niculescu-Mizil et al.
ACL 2013), ConvoKit release.

Source : ConvoKit wikipedia-politeness-corpus.zip (sha256 pinned): utterances.jsonl + Annotations-bin.p (the five
         raw MTurk ratings of every request). The Stack Exchange half is never used (Stack Exchange is an OHS source).
Licence: CC BY 4.0 (ConvoKit docs https://convokit.cornell.edu/documentation/wiki_politeness.html, 'Data License':
         "ConvoKit's Stanford Politeness Corpus is governed by the CC BY license v4.0.").
Texts  : requests written by Wikipedia editors on user talk pages (human-written, pre-2013).
Labels : 5 Mechanical Turk annotators per request rated politeness on a 1-25 slider from "very impolite" to
         "very polite" with 13 as the neutral midpoint (the ratings cluster on 1, 5, 9, 13, 17, 21, 25).
Split  : no official split -> train; every request in Cleanlab's public stanford-politeness test.csv (a test set built
         from this corpus) is dropped.
Language: the corpus holds a few non-English requests (Polish, Serbo-Croatian, Dutch, Finnish, Tagalog ...; raters
         could not read them and mostly gave the neutral 13) and texts whose non-ASCII letters were flattened to
         backslash-less escapes ("Wacu0142awowo", "xe4"). Both are dropped: an escape remnant (u0XXX / x[b-f]digit), or
         >= 6 words with an English function-word share < 0.10 (review fix, 29 Sep).
Tasks  (each request used for one question; per-annotator binarisation around the neutral midpoint 13):
 - q_impolite "Is this request impolite?": yes-vote = rating 1-12, no-vote = 13-25.
 - q_polite   "Is this request clearly polite?": yes-vote = rating 14-25, no-vote = 1-13.
 Soft = share of the 5 annotators voting yes; gold yes if >= 4/5, no if <= 1/5; 2/5-3/5 requests are not used.
Overlap: requests sharing a 10-word run with any Kaggle Jigsaw (Wikipedia talk) comment are dropped (Jigsaw sits
         inside the forbidden label-NLI task mbib-base/hate-speech; thesofakillers mirror pinned by revision + sha256);
         standard decontamination (local data incl. the v13 politeness_wiki part, label-NLI, JevBench, other v14).
Balance: yes share per question 0.42-0.45. Deterministic (seed 20261101).
"""
import collections
import json
import pickle
import random
import re
import zipfile
from pathlib import Path

import pandas as pd

import _cal_common as C

KEY = "politeness_votes"
ZIP_URL = ("https://zissou.infosci.cornell.edu/convokit/datasets/wikipedia-politeness-corpus/"
           "wikipedia-politeness-corpus.zip")
ZIP_SHA = "90ec6c2c6e05d064a805d2e4be4a8d442f370b31f0025798e8eaf62d0014ba48"
CL_URL = "https://s.cleanlab.ai/stanford-politeness/fine-tuning/test.csv"
CL_SHA = "78b7f79887351aa4f5f089f1990b86c94343f1c170f0ed5652b825c5cc3b3306"
JIG_REPO = "thesofakillers/jigsaw-toxic-comment-classification-challenge"
JIG_REV = "50f3c926ec8c07b440cb17b55d8cd80e8484497e"
JIG_SHA = {"train.csv": "bd4084611bd27c939ba98e5e63bc3e5a2c1a4e99477dcba46c829e4c986c429d",
           "test.csv": "c2513ce4abb98c4d1d216e3ca0d4377d57589a0989aa8c06a840509a16c786e8"}
LICENCE = ("CC BY 4.0 (ConvoKit docs https://convokit.cornell.edu/documentation/wiki_politeness.html, 'Data License': "
           "\"ConvoKit's Stanford Politeness Corpus is governed by the CC BY license v4.0.\")")
DATASET = "Stanford Politeness Corpus, Wikipedia half (ConvoKit wikipedia-politeness-corpus.zip), raw 5-rater votes"
CACHE = C.CACHE / KEY

QS = {
    "q_impolite": (lambda s: s <= 12, "Is this request from a Wikipedia editor to another editor impolite?"),
    "q_polite": (lambda s: s >= 14, "Is this request from a Wikipedia editor to another editor clearly polite?"),
}
DEFS = {
    "q_impolite": {
        "yes": "At least 4 of 5 raters placed it on the impolite side of the scale: blunt or challenging questions "
               "('Why did you...?'), commands, accusations, impatience or sarcasm, with no greeting, thanks, "
               "apology or softening; insults are not required.",
        "no": "At most 1 of 5 raters placed it on the impolite side: the request is neutral and matter-of-fact or "
              "courteous (greeting, thanks, 'could you please', hedging), even if short or direct.",
    },
    "q_polite": {
        "yes": "At least 4 of 5 raters placed it on the polite side of the scale: courteous wording such as greeting, "
               "thanks, apology, praise, hedging ('I think', 'perhaps') or indirect asks ('would you mind', 'could "
               "you please').",
        "no": "At most 1 of 5 raters placed it on the polite side: the request is plain and neutral (bare questions "
              "or statements without courtesy markers) or blunt and impolite.",
    },
}


EN_SW = set("""a about above after again against all am an and any are as at be because been before being below between
both but by can could did do does doing down during each few for from further had has have having he her here hers him his
how i if in into is it its itself just me more most my no nor not now of off on once only or other our out over own same she
should so some such than that the their them then there these they this those through to too under until up very was we were
what when where which while who whom why will with would you your yours yourself anything else something please thanks thank
hi hello okay ok done yes also get got make""".split())
ESCAPED = re.compile(r"u0[0-9a-f]{3}|x(?:[c-f][0-9]|b[0-9])")


def not_english(t):
    """True for texts with flattened unicode escapes or (>= 6 words) almost no English function words."""
    if ESCAPED.search(t):
        return True
    w = [x.strip("'") for x in re.findall(r"[a-z']+", t.lower().replace("<url>", " ").replace("<person>", " "))]
    w = [x for x in w if x]
    return len(w) >= 6 and sum(x in EN_SW for x in w) / len(w) < 0.10


def jigsaw_texts():
    from huggingface_hub import hf_hub_download
    out = []
    for fn, sha in JIG_SHA.items():
        p = Path(hf_hub_download(JIG_REPO, fn, repo_type="dataset", revision=JIG_REV))
        assert C.sha256(p) == sha, fn
        out.extend(pd.read_csv(p)["comment_text"].astype(str).tolist())
    return out


def main():
    rng = random.Random(C.SEED)
    z = C.fetch(ZIP_URL, CACHE / "wikipedia-politeness-corpus.zip", ZIP_SHA)
    cl = C.fetch(CL_URL, CACHE / "cleanlab_test.csv", CL_SHA)
    with zipfile.ZipFile(z) as zf:
        utts = [json.loads(ln) for ln in zf.read("wikipedia-politeness-corpus/utterances.jsonl").decode().splitlines()
                if ln.strip()]
        ann = pickle.loads(zf.read("wikipedia-politeness-corpus/Annotations-bin.p"))
    cl_test = {C.norm(t) for t in pd.read_csv(cl)["prompt"].astype(str)}

    recs = []
    drop = collections.Counter()
    for u in utts:
        t = C.clean(u["text"])
        if not (15 <= len(t) <= 4000) or len(C.words(t)) < 4:
            drop["len"] += 1
            continue
        if C.norm(t) in cl_test:
            drop["cleanlab_test"] += 1
            continue
        if not_english(t):
            drop["non_english_or_escaped"] += 1
            continue
        d = ann[int(re.search(r"bin\{(\d+)\}", u["meta"]["Annotations"]).group(1))]
        scores = [int(s) for s in d.values()]
        if len(scores) != 5:
            drop["not5"] += 1
            continue
        recs.append((str(u["id"]), t, scores, u["meta"]))
    core = {rid: [t] for rid, t, _, _ in recs}
    hits = C.decon(core, KEY, extra_texts={"jigsaw": jigsaw_texts()})
    hits.update(C.cross_v14(core, {KEY}))
    print("records:", len(recs), "dropped:", dict(drop), "overlap hits:", len(hits),
          dict(collections.Counter(v.split(":")[0] for v in hits.values())))
    recs = [r for r in recs if r[0] not in hits]

    cands = collections.defaultdict(list)
    for rid, t, scores, meta in recs:
        for q, (fn, _) in QS.items():
            v = sum(fn(s) for s in scores)
            if v >= 4:
                cands[(q, "yes")].append((rid, t, scores, v, meta))
            elif v <= 1:
                cands[(q, "no")].append((rid, t, scores, v, meta))
    print("candidates:", {f"{q}/{g}": len(x) for (q, g), x in sorted(cands.items())})
    for k in sorted(cands):
        rng.shuffle(cands[k])
    # impolite-yes is the scarcest cell: fill q_impolite first, then q_polite from the unused requests.
    nd = C.NearDup(thr=0.7)
    used = set()
    out = {}

    def take(k, n):
        lst = []
        for c in cands[k]:
            if len(lst) >= n:
                break
            if c[0] in used or nd.seen(c[1]):
                continue
            used.add(c[0])
            lst.append(c)
        return lst

    out[("q_impolite", "yes")] = take(("q_impolite", "yes"), 10 ** 6)
    ny = len(out[("q_impolite", "yes")])
    out[("q_impolite", "no")] = take(("q_impolite", "no"), int(ny * 0.56 / 0.44))
    out[("q_polite", "yes")] = take(("q_polite", "yes"), 10 ** 6)
    ny2 = len(out[("q_polite", "yes")])
    out[("q_polite", "no")] = take(("q_polite", "no"), int(ny2 * 0.56 / 0.44))
    # if q_polite-no ran short, trim q_polite-yes to keep its share <= 0.55
    np_ = len(out[("q_polite", "no")])
    if ny2 > np_ * 0.55 / 0.45:
        out[("q_polite", "yes")] = out[("q_polite", "yes")][:int(np_ * 0.55 / 0.45)]
    print({f"{q}/{g}": len(x) for (q, g), x in out.items()})

    rows = []
    for (q, g), lst in out.items():
        for rid, t, scores, v, meta in lst:
            e = None
            if C.neg_count(t):
                e = "negation"
            rows.append({
                "key": KEY, "rid": f"spc-wiki-{rid}", "state": t, "instructions": QS[q][1], "options": C.YN,
                "gold": g, "soft": C.soft_yes(v, 5),
                "meta": {"dataset": DATASET, "config": q, "revision": f"zip sha256 {ZIP_SHA}", "licence": LICENCE,
                         "split": "train",
                         "orig_label": {"ratings_1to25": sorted(scores), "Binary": meta["Binary"],
                                        "Normalized Score": round(meta["Normalized Score"], 3)},
                         "family": C.FAMILY, "edge": e, "defs": q},
            })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, DEFS)
    st = C.summary(KEY, rows)
    C.show_samples(rows, 6)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Soft = share of the 5 MTurk raters on the impolite (1-12) or polite (14-25) side of the 1-25 slider (13 = "
        "neutral). Gold >= 4/5 yes, <= 1/5 no. Two defs files (__q_impolite, __q_polite). Stack Exchange half never "
        "used; Cleanlab public test texts and Jigsaw (label-NLI mbib) overlaps dropped; non-English / escape-mangled "
        "texts dropped; v13 rows removed by decon.",
        st))


if __name__ == "__main__":
    main()
