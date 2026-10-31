"""Build raw rows for uds_ordinal: graded semantic judgements about one event in a real English web sentence, from
the Universal Decompositional Semantics (UDS 2.0) raw crowd annotations.

Two ordinal question types (one row per sentence, never both):
  duration  - "How long did the marked event/state last?" on UDS-Time's 11 ordered duration classes
              (instant < seconds < minutes < hours < days < weeks < months < years < decades < centuries < forever);
              3+ raters per predicate, soft = their shares, gold = the unique plurality class that also contains the
              median rating (ordinal) and holds >= 60% of the votes; rows whose gold would be 'instantaneous' are
              dropped (review: those votes were mostly given to states such as 'is necessary' / 'need to').
  likelihood - Semantic Proto-Role (SPR2) property questions ("How likely is it that <participant> was aware of /
              chose / caused / changed location in ... the marked event?") on a 5-point likelihood scale; 13 core
              properties; kept only when every rater judged the question applicable and all raters chose the SAME
              point (typically 2 raters), so soft = {that point: 1.0}.

Source : decompositional-semantics-initiative/decomp @ 973705b0c8f0c82701126ac4d8e1e2186bdcab21,
         decomp/data/2.0/raw/sentence/annotations/{time,protoroles}.zip (raw per-annotator values), and the
         sentences of UD English-EWT r1.2 (UniversalDependencies/UD_English-EWT @ 17a19823d04bf078e8a9be532118fe0ff1011934,
         en-ud-train.conllu; the UDS ids 'ewt-train-N' are the N-th sentence of that file). TRAIN split only.
Licence: CC BY-SA 4.0 for both: decomp README 'All contents of decomp/data are covered by the CC-BY-SA 4.0 license
         contained in that directory' (decomp/data/LICENSE); UD EWT README.txt 'License: CC BY-SA 4.0' + LICENSE.txt.
Texts  : EWT web sentences (blogs, newsgroups, reviews, answers; the Enron 'email' genre is dropped in review because
         SetFit/enron_spam, a dev/selection source, shares its texts), detokenised with SpaceAfter=No; the event
         head word is shown as [word] and the participant head as <word> (plus its dependency-subtree phrase).
Deterministic (seed 20261101); CPU only; no model calls.
"""
import collections
import json
import random
import statistics
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ord_common as C  # noqa: E402

KEY = "uds_ordinal"
SEED = C.SEED
CACHE = C.CACHE / KEY
DECOMP = "973705b0c8f0c82701126ac4d8e1e2186bdcab21"
EWT = "17a19823d04bf078e8a9be532118fe0ff1011934"
EWT22 = "6e064999a75b9c941c515ce1be98352e6f9831e0"  # UD_English-EWT tag r2.2 (genre ids only; text/labels from r1.2)
FILES = {
    (f"https://raw.githubusercontent.com/decompositional-semantics-initiative/decomp/{DECOMP}/decomp/data/2.0/raw/"
     "sentence/annotations/time.zip"): ("time.zip", "fa7df1bf42ee9dbfd3e51c514a4ce6b2da51f4d546e9b1188a05a94240fdfb38"),
    (f"https://raw.githubusercontent.com/decompositional-semantics-initiative/decomp/{DECOMP}/decomp/data/2.0/raw/"
     "sentence/annotations/protoroles.zip"): ("protoroles.zip",
                                             "023e3e73961a4015041aa653a78b8ae324f7e934d99b8247dcae9518ad1bd633"),
    f"https://raw.githubusercontent.com/decompositional-semantics-initiative/decomp/{DECOMP}/decomp/data/LICENSE":
        ("decomp_LICENSE", "b3d1b0f4c6ae151f7eb78738f46ebd5ee140f8a7f76501ba26af123140d35ae7"),
    f"https://raw.githubusercontent.com/UniversalDependencies/UD_English-EWT/{EWT}/en-ud-train.conllu":
        ("en-ud-train.conllu", "4199e447ec4902a26b3b1550375e359a3f9908fcb0bebe02ae2bc37997a9d3ab"),
    f"https://raw.githubusercontent.com/UniversalDependencies/UD_English-EWT/{EWT}/README.txt":
        ("ewt_README.txt", "ee4fad447d0c2b26df27b94d4289008c129bfde70b4d02c5d6b6d1e1fc315fc4"),
    # review fix: r2.2 train has the same 12,543 sentences in the same order plus sent_ids naming the genre
    f"https://raw.githubusercontent.com/UniversalDependencies/UD_English-EWT/{EWT22}/en_ewt-ud-train.conllu":
        ("en_ewt-ud-train_r2.2.conllu", "74001b5c55bc997fc63394c46ed36207f0107d83e0e57c89699733b5dc999eae"),
}
# Review fixes (29 Sep 2026):
# (1) EWT 'email' sentences are Enron e-mails; SetFit/enron_spam (a dev/selection source in ohs3/used_sources.json)
#     holds the same mailboxes: 41 rows of the first build shared a 10-word run with it (e.g. 'If the reader of this
#     message is not the intended recipient ...'). All email-genre sentences are dropped (genre from r2.2 sent_ids;
#     answers are 2009/2011 Yahoo! Answers ids, after the 2007 yahoo_answers_topics dump, so they are kept).
# (2) 'instantaneous' duration votes were mostly given to states and light verbs ('is necessary', 'need to',
#     'is unique', 'know'), contradicting the class definition; rows whose gold would be 'instantaneous' are dropped
#     (the option stays on the scale).
DROP_GENRES = {"email"}
ENRON_SPAM_URL = ("https://huggingface.co/datasets/SetFit/enron_spam/resolve/1916f66c89d52221ae33eb57d44498b4f3a5df22/"
                  "enron_spam_data.csv")
ENRON_SPAM_SHA = "009c86359b5bd6ec142a9b9ca85075ec864fd8c7c1c378c9a430e9427d0f7d57"
DROP_DUR_GOLD = {"instantaneous"}
LICENCE = (f"CC BY-SA 4.0 (UDS annotations: https://github.com/decompositional-semantics-initiative/decomp/blob/"
           f"{DECOMP}/decomp/data/LICENSE and README 'All contents of decomp/data are covered by the CC-BY-SA 4.0 "
           f"license'; EWT text: https://github.com/UniversalDependencies/UD_English-EWT/blob/{EWT}/README.txt "
           f"'License: CC BY-SA 4.0')")
DATASET = "Universal Decompositional Semantics 2.0 raw annotations (UDS-Time duration, SPR2 proto-roles) on UD EWT r1.2 train"

DUR = ["instant", "seconds", "minutes", "hours", "days", "weeks", "months", "years", "decades", "centuries", "forever"]
DUR_OPTS = ["instantaneous", "seconds", "minutes", "hours", "days", "weeks", "months", "years", "decades",
            "centuries", "forever"]
LIK = ["very unlikely", "unlikely", "neither likely nor unlikely", "likely", "very likely"]
DUR_CAP = 230
LIK_CAP = 320

DUR_Q = ("How long did the event or state marked [ ] in the sentence last? Choose the most likely duration class "
         "given the sentence.")
PROP_Q = {
    "awareness": "was aware of being involved in",
    "change_of_location": "changed location during",
    "change_of_possession": "changed possession (was given, taken, sold or otherwise transferred) during",
    "change_of_state": "was altered or somehow changed during or by the end of",
    "existed_after": "existed after",
    "existed_before": "existed before",
    "existed_during": "existed during",
    "instigation": "caused",
    "partitive": "was only partly (only some portion of it) involved in",
    "sentient": "was sentient (able to feel or perceive) at the time of",
    "volition": "chose to be involved in",
    "was_for_benefit": "was someone for whose benefit",
    "was_used": "was used in carrying out",
}
DEFS = {
    "duration": {
        "instantaneous": "Happens at a single moment with essentially no duration (arriving, noticing, winning, a "
                         "click or a shot).",
        "seconds": "Lasts from about a second up to under a minute (a sentence spoken, a glance, a quick reply).",
        "minutes": "Lasts from about one minute up to under an hour (a phone call, a meal, a short meeting).",
        "hours": "Lasts from about one hour up to under a day (a workday, a flight, a party).",
        "days": "Lasts from about one day up to under a week (a trip, an illness, a weekend event).",
        "weeks": "Lasts from about one week up to under a month (a vacation, a short course, a hospital stay).",
        "months": "Lasts from about one month up to under a year (a season, a project, a pregnancy).",
        "years": "Lasts from about one year up to under a decade (a job, schooling, living somewhere).",
        "decades": "Lasts from about ten years up to under a century (a career, a marriage, a person's adult life).",
        "centuries": "Lasts a hundred years or more but has a beginning or end (an institution, a tradition, an "
                     "empire).",
        "forever": "Has no bounded duration: permanent, timeless or generic states and truths (being a species, a "
                   "mathematical fact, a general rule).",
    },
    "likelihood": {
        "very unlikely": "Given the sentence, the property is clearly false for the participant in this event "
                         "(scale point 1 of 5).",
        "unlikely": "The property is probably false for the participant, though the sentence leaves some room for "
                    "it (point 2 of 5).",
        "neither likely nor unlikely": "The sentence gives no reason to think the property holds or fails; it is "
                                       "an even bet (point 3 of 5).",
        "likely": "The property probably holds for the participant, though the sentence does not state it outright "
                  "(point 4 of 5).",
        "very likely": "Given the sentence, the property clearly holds for the participant in this event (point 5 "
                       "of 5).",
    },
}


def read_conllu(path):
    sents, cur = [], []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line:
            if cur:
                sents.append(cur)
                cur = []
            continue
        if line.startswith("#"):
            continue
        p = line.split("\t")
        if "-" in p[0] or "." in p[0]:
            continue
        cur.append({"id": int(p[0]), "form": p[1], "head": int(p[6]) if p[6].isdigit() else 0,
                    "upos": p[3], "nospace": "SpaceAfter=No" in p[9]})
    if cur:
        sents.append(cur)
    return sents


def render(toks, marks):
    """Detokenise; marks = {token_id: (open, close)}."""
    out = []
    for t in toks:
        w = t["form"]
        if t["id"] in marks:
            o, c = marks[t["id"]]
            w = o + w + c
        out.append(w + ("" if t["nospace"] else " "))
    return "".join(out).strip()


def subtree_span(toks, hid, max_len=12):
    kids = collections.defaultdict(list)
    for t in toks:
        kids[t["head"]].append(t["id"])
    seen, stack = set(), [hid]
    while stack:
        x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        stack.extend(kids.get(x, []))
    ids = sorted(seen)
    if ids[-1] - ids[0] + 1 != len(ids) or len(ids) > max_len:
        return None
    sub = [t for t in toks if t["id"] in seen]
    while sub and sub[0]["upos"] == "PUNCT":
        sub = sub[1:]
    while sub and sub[-1]["upos"] == "PUNCT":
        sub = sub[:-1]
    return render([dict(t, nospace=(t["nospace"] if t is not sub[-1] else True)) for t in sub], {}) if sub else None


def main():
    paths = {}
    for url, (name, sha) in FILES.items():
        paths[name] = C.fetch(url, CACHE / name, sha)
    sents = read_conllu(paths["en-ud-train.conllu"])
    genre = []
    cur_id, ntok = None, 0
    for line in open(paths["en_ewt-ud-train_r2.2.conllu"], encoding="utf-8"):
        if line.startswith("# sent_id"):
            cur_id = line.split("=", 1)[1].strip()
        elif not line.strip():
            if ntok:
                genre.append(cur_id.split("-")[0])
            ntok = 0
        elif not line.startswith("#"):
            ntok += 1
    if ntok:
        genre.append(cur_id.split("-")[0])
    assert len(genre) == len(sents) == 12543, (len(genre), len(sents))
    with zipfile.ZipFile(paths["time.zip"]) as z:
        time_data = json.loads(z.read("time.json"))["data"]
    with zipfile.ZipFile(paths["protoroles.zip"]) as z:
        pr_data = json.loads(z.read("protoroles.json"))["data"]
    stats = collections.Counter()

    def sent_of(gid):
        if not gid.startswith("ewt-train-"):
            return None
        i = int(gid.rsplit("-", 1)[1]) - 1
        if not 0 <= i < len(sents):
            return None
        if genre[i] in DROP_GENRES:
            stats["drop_email_genre_sentence"] += 1
            return None
        return sents[i]

    dur_c, lik_c = [], []
    for gid, nodes in time_data.items():
        toks = sent_of(gid)
        if toks is None:
            continue
        for nid, d in nodes.items():
            vals = list(d["time"]["duration"]["value"].values())
            if len(vals) < 3:
                stats["dur_drop_few_raters"] += 1
                continue
            idx = [DUR.index(v) for v in vals]
            cnt = collections.Counter(idx)
            top, tc = cnt.most_common(1)[0]
            if sum(1 for v in cnt.values() if v == tc) > 1 or tc / len(idx) < 0.6:
                stats["dur_drop_no_majority"] += 1
                continue
            if statistics.median_low(idx) != top:
                stats["dur_drop_median"] += 1
                continue
            if DUR_OPTS[top] in DROP_DUR_GOLD:
                stats["dur_drop_instantaneous_gold"] += 1
                continue
            pid = int(nid.rsplit("-", 1)[1])
            soft = C.fix_soft({DUR_OPTS[i]: cnt.get(i, 0) / len(idx) for i in range(len(DUR))})
            dur_c.append({"gid": gid, "toks": toks, "pid": pid, "gold": DUR_OPTS[top], "soft": soft,
                          "orig": {"duration_votes": sorted(vals, key=DUR.index)}})
    for gid, edges in pr_data.items():
        toks = sent_of(gid)
        if toks is None:
            continue
        for eid, d in edges.items():
            a, b = eid.split("%%")
            pid, aid = int(a.rsplit("-", 1)[1]), int(b.rsplit("-", 1)[1])
            for prop, vd in d["protoroles"].items():
                if prop not in PROP_Q:
                    continue
                v, c = vd["value"], vd["confidence"]
                if len(v) < 2:
                    stats["lik_drop_one_rater"] += 1
                    continue
                if any(c[x] != 1 for x in v):
                    stats["lik_drop_not_applicable"] += 1
                    continue
                if len(set(v.values())) != 1:
                    stats["lik_drop_disagree"] += 1
                    continue
                val = next(iter(v.values()))
                lik_c.append({"gid": gid, "toks": toks, "pid": pid, "aid": aid, "prop": prop, "gold": LIK[val],
                              "soft": {o: (1.0 if o == LIK[val] else 0.0) for o in LIK},
                              "orig": {"property": prop, "votes": sorted(v.values()), "n_raters": len(v)}})
    stats["dur_candidates"] = len(dur_c)
    stats["lik_candidates"] = len(lik_c)

    rng = random.Random(SEED)
    for xs in (dur_c, lik_c):
        xs.sort(key=lambda x: (x["gid"], x["pid"], x.get("aid", 0), x.get("prop", "")))
        rng.shuffle(xs)

    # decontaminate sentences once
    sent_text = {}
    for x in dur_c + lik_c:
        sent_text.setdefault(x["gid"], render(x["toks"], {}))
    # review fix: also drop any sentence sharing an exact text or a 10-word run with SetFit/enron_spam (dev/selection
    # source; its spam half contains the same 419-letter templates as some EWT newsgroup/weblog sentences)
    ep = C.fetch(ENRON_SPAM_URL, CACHE / "enron_spam_data.csv", ENRON_SPAM_SHA)
    import pandas as pd
    edf = pd.read_csv(ep)
    enron_texts = list(edf["Subject"].astype(str)) + list(edf["Message"].astype(str))
    hits = C.decon({g: [t] for g, t in sent_text.items()}, KEY, extra_texts={"enron_spam": enron_texts})
    hits.update(C.cross_v14({g: [t] for g, t in sent_text.items()}, {KEY}))
    stats["sentences_decon_hits"] = len(hits)

    used = set()
    nd = C.NearDup(thr=0.7)
    rows = []

    def take(x, qtype):
        if x["gid"] in used or x["gid"] in hits:
            return False
        s = sent_text[x["gid"]]
        if len(C.words(s)) < 6 or len(s) > 600:
            return False
        if nd.seen(s):
            used.add(x["gid"])
            return False
        used.add(x["gid"])
        toks = x["toks"]
        pw = toks[x["pid"] - 1]["form"]
        if qtype == "duration":
            sent = render(toks, {x["pid"]: ("[", "]")})
            state = f"Sentence: {sent}\nMarked event or state: [{pw}]"
            q, opts, defs = DUR_Q, DUR_OPTS, "duration"
        else:
            aw = toks[x["aid"] - 1]["form"]
            sent = render(toks, {x["pid"]: ("[", "]"), x["aid"]: ("<", ">")})
            phrase = subtree_span(toks, x["aid"])
            part = f"<{aw}>" + (f' (the phrase "{phrase}")' if phrase and phrase != aw else "")
            state = f"Sentence: {sent}\nMarked event: [{pw}]\nMarked participant: {part}"
            if x["prop"] == "was_for_benefit":
                q = (f"In this sentence, how likely is it that the [{pw}] event happened for the benefit of the "
                     f"participant <{aw}>?")
            elif x["prop"] == "instigation":
                q = f"In this sentence, how likely is it that the participant <{aw}> caused the [{pw}] event to happen?"
            elif x["prop"] == "sentient":
                q = (f"In this sentence, how likely is it that the participant <{aw}> was sentient (able to feel or "
                     f"perceive) at the time of the [{pw}] event?")
            else:
                q = f"In this sentence, how likely is it that the participant <{aw}> {PROP_Q[x['prop']]} the [{pw}] event?"
            opts, defs = LIK, "likelihood"
        edge = []
        if qtype == "duration":
            edge.append("temporal")
        if C.neg_count(s):
            edge.append("negation")
        if C.HYPO.search(s):
            edge.append("hypothetical")
        if max(x["soft"].values()) < 0.6:
            edge.append("ambiguous")
        if qtype == "likelihood" and x["gold"] in ("unlikely", "likely", "neither likely nor unlikely"):
            edge.append("implicit")
        rid = f"uds-{x['gid']}-{qtype}-" + (f"p{x['pid']}" if qtype == "duration" else f"p{x['pid']}a{x['aid']}-{x['prop']}")
        rows.append({
            "key": KEY, "rid": rid, "state": state, "instructions": q, "options": opts, "gold": x["gold"],
            "soft": x["soft"],
            "meta": {"dataset": DATASET, "config": f"question={qtype}" + ("" if qtype == "duration" else f"; property={x['prop']}"),
                     "revision": f"decomp git:{DECOMP}; UD_English-EWT git:{EWT} (r1.2); sha256 pinned in builder",
                     "licence": LICENCE, "split": "train", "orig_label": x["orig"], "family": C.FAMILY,
                     "edge": C.edge_join(edge), "defs": defs, "seed": SEED},
        })
        return True

    # rarest classes first so their sentences are not consumed by the other question type
    dur_by = collections.defaultdict(list)
    for x in dur_c:
        dur_by[x["gold"]].append(x)
    lik_by = collections.defaultdict(list)
    for x in lik_c:
        lik_by[(x["gold"], x["prop"])].append(x)
    got = collections.Counter()
    for lev in sorted(DUR_OPTS, key=lambda o: len(dur_by[o])):
        for x in dur_by[lev]:
            if got[("d", lev)] >= DUR_CAP:
                break
            if take(x, "duration"):
                got[("d", lev)] += 1
    for lev in sorted(LIK, key=lambda o: sum(len(v) for k, v in lik_by.items() if k[0] == o)):
        props = sorted(p for (g, p) in lik_by if g == lev)
        i, idle = 0, 0
        while got[("l", lev)] < LIK_CAP and idle < len(props):
            p = props[i % len(props)]
            i += 1
            took = False
            while lik_by[(lev, p)]:
                if take(lik_by[(lev, p)].pop(), "likelihood"):
                    got[("l", lev)] += 1
                    took = True
                    break
            idle = 0 if took else idle + 1
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, DEFS)
    print(dict(stats))
    print("properties:", dict(collections.Counter(r["meta"]["config"].split("property=")[-1] for r in rows
                                                  if "property=" in r["meta"]["config"])))
    st = C.summary(KEY, rows)
    C.show_samples(rows, n=6, seed=4)
    rec = C.manifest_record(
        KEY, DATASET, LICENCE, rows,
        "choice (ordinal: event duration 11 classes / proto-role likelihood 5 points; soft labels)",
        "UD EWT train web sentences with one marked event: UDS-Time duration class (3+ raters, soft shares, gold = "
        "plurality holding the median and >= 60%) or an SPR2 proto-role likelihood question (13 properties; all "
        "raters applicable and in exact agreement); one row per sentence; rare classes filled first, capped per "
        "class; review fixes: EWT email (Enron) genre and any sentence sharing text with SetFit/enron_spam dropped, "
        "'instantaneous' gold rows dropped (votes mostly on states).", st)
    return rows, rec


if __name__ == "__main__":
    rows, rec = main()
    if "--manifest" in sys.argv:
        C.append_manifest(rec)
        print("manifest record appended")
