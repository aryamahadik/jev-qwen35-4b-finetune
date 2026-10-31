"""Build raw rows for cards (CARDS: Computer-Assisted Recognition of (climate change) Denial and Skepticism;
Coan, Boussalis, Cook & Nanko, "Computer-assisted classification of contrarian claims about climate change",
Scientific Reports 11:22320, 2021).

Source : github traviscoan/cards pinned to commit 51a824c96b9ac5beb9efd6481567bc3a1e74d53a; its README links the
         released data zip (Google Drive id 14exmlYCT3-K2byYHFFrShAIYiemJQroi, 'data_clean'), pinned here by sha256.
         Only data/training/training.csv is read (validation.csv, test.csv and the model-labelled
         analysis/cards_for_analysis.csv are never read).
Licence: Apache-2.0 (LICENSE file of the repository, whose README states "This repository makes available the
         training data and main code").
Texts  : paragraphs from conservative think-tank websites and contrarian blogs (1998-2020). Human-written.
Labels : human coding by 30 climate-literate volunteers (Skeptical Science team), each paragraph coded by >= 3 coders,
         majority rule; sub-claim codes 'super_sub' (0_0 = no contrarian claim). Paragraphs the coders flagged as
         containing multiple claims were removed by the authors. The authors call the training labels noisy (their
         test set was re-annotated); we therefore use the more reliable SUPER-claim level (coder accuracy 0.86-0.97
         on the five claim classes, Table 1) and keep each question's negatives mostly to majority-'no claim' paragraphs.
Questions (one per paragraph, yes/no): "Does this paragraph make the contrarian climate claim that ...?"
         q1 global warming is not happening; q2 human greenhouse gases are not causing climate change; q3 climate
         impacts / global warming are beneficial or not bad; q4 climate solutions won't work; q5 climate science or
         the climate movement is unreliable.
         yes = paragraph coded with a sub-claim of that super-claim; no = paragraph coded 0_0 (~55%) or, for q1-q4
         only, coded with a sub-claim of a clearly different super-claim (~45%, harder negatives: q1/q2/q3 <- policy
         claims 4_x; q4 <- science claims 1_x/2_x/3_x). q5 never gets cross-claim negatives because attacks on
         science/movement co-occur with every other category. An audit of the first build found unflagged claims
         inside 0_0 paragraphs, so EVERY negative for question q must also pass q's topic screen (no cue word of q's
         topic, e.g. no 'tax/policy/energy/cost' for q4, no 'warm/ice/temperature/record' for q1): a 'no' is then
         clearly right even where the 0_0 majority label missed a claim of another kind.
Filters: >= 10 words, complete paragraphs only (sentence start and end, no e-mail '>' quoting); paragraphs with
         '??' or letter?letter mojibake (lost curly quotes/apostrophes) dropped rather than guessed; exact and
         near-duplicate removal; decontamination (label-NLI incl. tweet_eval/stance_climate and
         crowdflower/tweet_global_warming, local train/dev/eval, JevBench public).
Review fix (strict reviewer, 29 Sep): 14 pairs of paragraphs where one is (almost) contained in the other (quoted
         or re-posted text with a different lead-in; word Jaccard < 0.85, so the near-dup filter missed them) were in
         the part; a paragraph sharing >= 50% of its 8-word shingles with an earlier kept paragraph is now dropped,
         and both are dropped when their claim codes differ (conflicting codes for the same text).
Deterministic (seed 20261117). CPU only.
"""
import collections
import hashlib
import io
import random
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _shc_common as C  # noqa: E402

KEY = "cards"
SEED = 20261117
COMMIT = "51a824c96b9ac5beb9efd6481567bc3a1e74d53a"
ZIP_URL = "https://drive.usercontent.google.com/download?id=14exmlYCT3-K2byYHFFrShAIYiemJQroi&export=download&confirm=t"
ZIP_SHA = "572b91d5742294398120305dc2562f8178690acc7898055d3871fda51ee744ae"
TRAIN_SHA = "2fd2019a593ae58ce36d60f2a06545fe8edcbd914386ab4ef2716ec4c0be4866"
LICENSE_URL = f"https://raw.githubusercontent.com/traviscoan/cards/{COMMIT}/LICENSE"
LICENSE_SHA = "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4"
README_URL = f"https://raw.githubusercontent.com/traviscoan/cards/{COMMIT}/README.md"
README_SHA = "2d9b2e307fade7bc530897fd8c962080d40d879fac7a7431876de5a2ae6a140f"
LICENCE = (f"Apache-2.0 (https://github.com/traviscoan/cards/blob/{COMMIT}/LICENSE; README: 'This repository makes "
           "available the training data', data zip linked from the README)")
DATASET = "CARDS contrarian climate claims (github traviscoan/cards, data_clean zip)"
POS_PER_Q = 800
HARD_SHARE = 0.45
# Topic screens: a NEGATIVE for question q must not mention any of q's topic cues. The 0_0 ('no claim') majority
# labels are noisy (audit: unflagged policy or science claims inside 0_0 paragraphs), so a 0_0 or other-claim
# paragraph is only used as a 'no' for q when it does not even touch q's topic; this keeps every 'no' clearly right.
SCREEN = {
    "1": ["cool", "cold", "snow", "ice", "arctic", "antarctic", "glacier", "sea level", "sea-level", "warm",
          "temperature", "hurricane", "storm", "drought", "flood", "extreme", "record", "pause", "hiatus", "heat",
          "climate change", "melt", "weather"],
    "2": ["natural", "cycle", "sun", "solar", "cosmic", "ocean", "nino", "nina", "pdo", "amo", "co2", "co 2",
          "carbon dioxide", "greenhouse", "forcing", "anthropogenic", "man-made", "manmade", "human", "warm",
          "climate change", "cause"],
    "3": ["benefi", "co2", "co 2", "carbon dioxide", "plant", "crop", "fertili", "greening", "sensitivity",
          "feedback", "polar bear", "coral", "reef", "species", "pollutant", "harmless", "degree", "warm", "impact",
          "good for", "not bad", "health"],
    "4": ["tax", "cap and trade", "cap-and-trade", "kyoto", "paris", "regulat", "epa", "polic", "renewable", "wind",
          "solar", "biofuel", "ethanol", "energy", "fossil", "coal", "oil", "gas", "nuclear", "emission",
          "mitigat", "cost", "econom", "jobs", "subsid", "carbon", "treaty", "legislation", "bill", "price"],
    "5": ["model", "data", "scien", "ipcc", "consensus", "alarm", "hoax", "fraud", "climategate", "hansen", "mann",
          "gore", "activist", "media", "study", "studies", "peer", "adjust", "record", "uncertain", "research",
          "professor", "expert", "warmist", "believ", "conspira", "scam", "agenda", "propaganda", "lie"],
}

SUPER = {
    "1": ("q1", "global warming is not happening",
          "denies that warming or its physical signs are happening: ice, permafrost or snow cover is not melting; "
          "we are heading into an ice age or global cooling; cold or snowy weather disproves warming; the climate "
          "has not warmed over recent decades; oceans are not warming; sea-level rise is exaggerated or not "
          "accelerating; extreme weather is not increasing, happened before or is not linked to climate change"),
    "2": ("q2", "human greenhouse gases are not causing climate change",
          "denies that human greenhouse-gas emissions drive climate change: it is natural cycles or variation "
          "(sun, oceans, orbital cycles); non-greenhouse human forcings are responsible; there is no evidence that "
          "the greenhouse effect or carbon dioxide drives warming; CO2 is not rising or human emissions are "
          "negligible"),
    "3": ("q3", "climate impacts are not bad or are beneficial",
          "argues that warming or its impacts are harmless or good: climate sensitivity is low or negative "
          "feedbacks limit warming; species, plants or reefs are not harmed or even benefit; carbon dioxide is "
          "beneficial (plant food) or not a pollutant; the warming is only a few degrees"),
    "4": ("q4", "climate solutions won't work",
          "argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto "
          "or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean "
          "energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy"),
    "5": ("q5", "climate science or the climate movement is unreliable",
          "attacks the reliability of climate science or its proponents: the data, models, methods or consensus "
          "are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are "
          "alarmist, biased, hypocritical, corrupt or part of a conspiracy"),
}
HARD_FROM = {"1": {"4"}, "2": {"4"}, "3": {"4"}, "4": {"1", "2", "3"}, "5": set()}


def containment_filter(recs, stats):
    """Drop a paragraph sharing >= 50% of its 8-word shingles with an earlier kept one; drop both when their claim
    codes differ."""
    def sh(t):
        w = C.words(t)
        return {hash(tuple(w[i:i + 8])) for i in range(len(w) - 7)}
    shs = [sh(r["text"]) for r in recs]
    owner, drop = {}, set()
    for i, s in enumerate(shs):
        cnt = collections.Counter(owner[h] for h in s if h in owner)
        for j, n in cnt.items():
            if n / (min(len(s), len(shs[j])) or 1) >= 0.5:
                drop.add(i)
                if recs[i]["claim"] != recs[j]["claim"]:
                    drop.add(j)
                    stats["drop_overlap_conflicting_codes"] += 1
        if i not in drop:
            for h in s:
                owner.setdefault(h, i)
    stats["drop_overlapping_paragraph"] += len(drop)
    return [r for i, r in enumerate(recs) if i not in drop]


def well_formed(t):
    """A complete paragraph: starts like a sentence and ends with sentence punctuation (drops cut fragments,
    headings and e-mail quoting)."""
    t = t.strip()
    return (len(t.split()) >= 12 and (t[0].isupper() or t[0] in "\"'“(") and t[-1] in ".!?\"'”)"
            and ">" not in t)


def off_topic(t, sup):
    low = t.lower()
    return not any(k in low for k in SCREEN[sup])


def defs_for(sup):
    qid, short, desc = SUPER[sup]
    return {
        "yes": f"The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the "
               f"contrarian claim that {short}: it {desc}.",
        "no": f"The paragraph does not make this contrarian claim: it gives background, neutral description or "
              f"mainstream statements, or it makes a different kind of argument (for example about policy costs "
              f"rather than the science, or vice versa) without claiming that {short}.",
    }


def main():
    rng = random.Random(SEED)
    cache = C.CACHE / KEY
    zpath = C.fetch(ZIP_URL, cache / "cards_data.zip", ZIP_SHA)
    C.fetch(LICENSE_URL, cache / "LICENSE", LICENSE_SHA)
    C.fetch(README_URL, cache / "README.md", README_SHA)
    with zipfile.ZipFile(zpath) as z:
        raw = z.read("data/training/training.csv")  # TRAINING SPLIT ONLY
    assert hashlib.sha256(raw).hexdigest() == TRAIN_SHA
    df = pd.read_csv(io.BytesIO(raw), keep_default_na=False)
    stats = collections.Counter()
    recs = []
    for i, (text, claim) in enumerate(zip(df["text"], df["claim"])):
        t = C.clean(text)
        if "??" in t or re.search(r"[A-Za-z]\?[A-Za-z]", t):
            stats["drop_mojibake"] += 1
            continue
        if len(t.split()) < 10:
            stats["drop_short"] += 1
            continue
        if not well_formed(t):
            stats["drop_fragment"] += 1
            continue
        recs.append({"rid": f"cards-train-{i:05d}", "text": t, "claim": claim, "super": claim.split("_")[0]})
    stats["usable"] = len(recs)

    hits = C.decon({r["rid"]: [r["text"]] for r in recs}, cache_name=KEY)
    recs = [r for r in recs if r["rid"] not in hits]
    recs.sort(key=lambda r: r["rid"])
    rng.shuffle(recs)
    recs = C.near_dup_filter(recs, lambda r: r["text"], thresh=0.85)
    recs = containment_filter(recs, stats)
    stats["after_decon_dedupe"] = len(recs)

    by_super = collections.defaultdict(list)
    for r in recs:
        by_super[r["super"]].append(r)
    by_code = collections.defaultdict(list)
    for r in recs:
        by_code[r["claim"]].append(r)
    used = set()
    rows = []

    def take(pool, n):
        out = []
        for r in pool:
            if len(out) >= n:
                break
            if r["rid"] in used:
                continue
            used.add(r["rid"])
            out.append(r)
        return out

    none_pool = list(by_super["0"])
    for sup in ["3", "4", "2", "1", "5"]:  # scarcest positive pools first
        qid, short, _ = SUPER[sup]
        # positives: round-robin over sub-claims so rare sub-claims are represented
        subs = sorted(c for c in by_code if c.startswith(sup + "_"))
        queues = {c: [r for r in by_code[c] if r["rid"] not in used] for c in subs}
        pos = []
        while len(pos) < POS_PER_Q and any(queues.values()):
            for c in subs:
                if queues[c] and len(pos) < POS_PER_Q:
                    r = queues[c].pop(0)
                    if r["rid"] not in used:
                        used.add(r["rid"])
                        pos.append(r)
        n_hard = int(round(len(pos) * HARD_SHARE)) if HARD_FROM[sup] else 0
        hard_pool = [r for r in recs if r["super"] != "0" and r["rid"] not in used and
                     (r["super"] in HARD_FROM[sup] or r["claim"] in HARD_FROM[sup]) and off_topic(r["text"], sup)]
        hard = take(hard_pool, n_hard)
        neg = take([r for r in none_pool if off_topic(r["text"], sup)], len(pos) - len(hard))
        for r, gold, kind in [(x, "yes", "positive") for x in pos] + [(x, "no", "cross-claim") for x in hard] + \
                             [(x, "no", "no-claim") for x in neg]:
            e = C.edge(r["text"], order=("double_negation", "negation", "units", "numeric", "quantifier"))
            if len(r["text"]) > 900:
                e = e or "long_context"
            rows.append({
                "key": KEY, "rid": r["rid"], "state": r["text"],
                "instructions": f"Does this paragraph make the contrarian climate claim that {short}?",
                "options": C.YN, "gold": gold, "soft": None,
                "meta": {"dataset": DATASET, "config": f"data/training/training.csv; super-claim {sup} ({qid})",
                         "revision": f"git:{COMMIT}; zip sha256:{ZIP_SHA}; training.csv sha256:{TRAIN_SHA}",
                         "licence": LICENCE, "split": "train",
                         "orig_label": {"claim": r["claim"], "negative_kind": None if gold == "yes" else kind},
                         "family": C.FAMILY, "edge": e, "defs": qid},
            })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, {SUPER[s][0]: defs_for(s) for s in SUPER})
    st = C.summary(KEY, rows)
    print("stats:", dict(stats), "| decon hits:", len(hits))
    print("positive sub-claims:", dict(sorted(collections.Counter(r["meta"]["orig_label"]["claim"] for r in rows
                                                               if r["gold"] == "yes").items())))
    print("negative kinds:", dict(collections.Counter(r["meta"]["orig_label"]["negative_kind"] for r in rows
                                                      if r["gold"] == "no")))
    C.show_samples(rows, n=5, seed=4)
    C.append_manifest(C.manifest_record(
        KEY, DATASET + ", training.csv only", LICENCE, rows, "yesno",
        "Climate contrarian-claim detection at the super-claim level (5 yes/no questions with per-question "
        "definitions listing the sub-claims); majority-of->=3 expert-volunteer codes; negatives ~55% majority "
        "no-claim paragraphs and ~45% clearly different claim categories (not for q5), every negative passing a topic "
        "screen for the asked claim; fragments and mojibake paragraphs dropped; overlapping (contained) paragraphs "
        "dropped, both when their codes conflict.",
        st))


if __name__ == "__main__":
    main()
