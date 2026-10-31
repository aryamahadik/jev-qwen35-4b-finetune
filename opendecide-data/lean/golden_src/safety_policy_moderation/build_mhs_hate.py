"""REJECTED BY THE STRICT REVIEWER (2026-09-29) - do not run; its raw/defs files were deleted.
Reason: ucberkeley-dlab/measuring-hate-speech is listed in ohs3/used_sources.json ("locked in original v0 design
(build/config.yaml, sources.lock.json) ... avoid to be safe"), and ../build/config.yaml gives it roles: [eval_zs],
i.e. it was designated as a zero-shot EVAL set. GOLDEN_SPEC hard rule 1 (never a dataset listed there for eval use;
when unsure, reject) therefore excludes it. It stays a read-only decontamination list (common.MHS_SOURCE).

Golden v14 / safety_policy_moderation: raw rows for "mhs_hate" (Measuring Hate Speech corpus, UC Berkeley D-Lab;
Kennedy et al. 2020 arXiv:2009.10277; Sachdeva et al. 2022, NLPerspectives@LREC).

Source  : HF ucberkeley-dlab/measuring-hate-speech, revision 5468f6e118396646b02a2f691e771f6b6d9502ea,
          data/train-00000-of-00001.parquet (sha256 pinned below). The release has only a train split (135,556
          annotation rows = 39,565 comments x 7,912 annotators).
Licence : CC BY 4.0 - dataset card YAML of the first-party repo (https://huggingface.co/datasets/ucberkeley-dlab/
          measuring-hate-speech/blob/5468f6e118396646b02a2f691e771f6b6d9502ea/README.md, "license: cc-by-4.0").
Provenance: human comments from Reddit /r/all, the Twitter random stream and YouTube (Mar-Aug 2019; URLs replaced
          by "URL"); labels by US MTurk annotators (poor-fit raters removed by the authors via Rasch fit statistics).
          hate_speech_score = the authors' many-facet Rasch (IRT) score over all 10 human items, adjusted for rater
          severity (> 0.5 ~ hate speech, < -1 counter/supportive speech, per the card). No model labels are used
          (the corpus's bin-sampling used classifiers only to choose which comments to annotate).
Exclusion check: listed in ohs3/used_sources.json only as "locked in original v0 design ... not in any row file;
          avoid to be safe" (never an eval, dev or held-out set, so training use is allowed by GOLDEN_SPEC rule 1).
          Not part of mbib-base (its hate-speech task = Kaggle Jigsaw, HateXplain, RedditBias, Online Harassment
          Corpus) nor of any other forbidden label-NLI task; the text-level check below confirms no shared texts.

Question types (each comment used at most once; allocation order: support, target, hs). Every question needs >= 3
raters (2-rater items were visibly noisier on inspection). Likert items use the 5-point scale, higher = more hateful:
>= 3 = agree, <= 1 = disagree, 2 = neither.
  (the Likert items violence / genocide / dehumanize are not used: even unanimous ratings were read far more
   loosely than the item wording - threats at one person, findom spam, "euthanize" remarks - see main())
  support   yes/no  "defends or supports the group": yes = >= 2/3 of raters say defending (attack_defend <= 1) and
                    IRT < -1.5; no = >= 2/3 say attacking (>= 3) and IRT > 0, or >= 2/3 say neither (= 2) with IRT in
                    [-1, 0.5]. A target group must be marked by >= 2/3 of raters.
  target    choice  8 identity-group types; gold = category marked by >= 2/3 of raters, every other category by
                    <= 1/3, and >= half of all marks; soft = share of marks per category.
  hs        yes/no  benchmark item "hatespeech" (0 no / 1 unclear / 2 yes): yes = >= 3 decisive votes, >= 2/3 yes and
                    IRT > 0.5; no = >= 3 decisive votes, <= 1/3 yes and IRT < -0.5 ("unclear" votes not counted).
  Soft labels (yes/no) = share of raters on each side among raters who took a side (Likert midpoint 2 / "unclear"
  not counted); rounded shares sum to 1.
Edge tags: "ambiguous" when the minority side holds >= 25% of the counted votes; otherwise null.
Filters: 20-1,500 chars, >= 4 words, not mostly URL/mentions; within-set exact and 12-word-run dedup; forbidden-source
  and our-file decontamination (common.py).
Deterministic (seed 20261129).

  ../.venv/bin/python golden_src/safety_policy_moderation/build_mhs_hate.py
"""
import random
import re
from collections import Counter

import numpy as np
import pandas as pd

import common as C

KEY = "mhs_hate"
REPO = "ucberkeley-dlab/measuring-hate-speech"
REV = "5468f6e118396646b02a2f691e771f6b6d9502ea"
FILE = "data/train-00000-of-00001.parquet"
SHA = "0d65ce8cfb857f5db90e74ce295067bba7473fe12115715f9dd18d2a5f87e976"  # = HF x-linked-etag
URL = f"https://huggingface.co/datasets/{REPO}/resolve/{REV}/{FILE}"
LICENCE = (f"CC BY 4.0 (first-party HF dataset card YAML 'license: cc-by-4.0', https://huggingface.co/datasets/{REPO}/"
           f"blob/{REV}/README.md)")
MAX_ROWS = 7700
MIN_RATERS = 3   # every question needs >= 3 raters (2-rater items were too noisy on inspection)

TGT = {  # MHS column -> option name
    "target_race": "race or ethnicity",
    "target_religion": "religion",
    "target_origin": "national origin or citizenship",
    "target_gender": "gender or gender identity",
    "target_sexuality": "sexual orientation",
    "target_age": "age",
    "target_disability": "disability",
    "target_politics": "political ideology",
}
TOPTS = list(TGT.values())
YN = ["yes", "no"]

Q = {
    "hs": "Is this comment hate speech against a protected identity group?",
    "support": "Does this comment defend or express support for the identity group it refers to?",
    "target": "Which kind of identity group does this comment mainly refer to or target?",
}
DEFS = {
    "hs": {
        "yes": "Hate speech: it attacks people for a protected identity (race, religion, national origin, gender, "
               "sexual orientation, age, disability) with identity slurs or insults, even aimed at one person, "
               "dehumanizing comparisons, threats, or calls for violence or killing.",
        "no": "Not hate speech: neutral or descriptive mentions, supportive messages, counter-speech against hate, or "
              "mild criticism without hostility; insults or profanity that do not invoke identity, and friendly "
              "in-group use of reclaimed words, are also no.",
    },
    "support": {
        "yes": "The comment defends or supports the identity group it refers to: counter-speech that rebuts hateful "
               "claims about the group, or respectful, proud or solidarity-based messages about it.",
        "no": "The comment does not defend or support the group: it attacks, insults or demeans the group, or it "
              "only mentions or describes the group neutrally without taking its side.",
    },
    "target": {
        "race or ethnicity": "The comment mainly refers to or targets people by race or ethnicity (for example Black, "
                             "white, Asian, Latinx, Arab, Native American, Jewish people as an ethnic group).",
        "religion": "The comment mainly refers to or targets people by religion or non-belief (for example Muslims, "
                    "Christians, Jews as a faith, Hindus, atheists).",
        "national origin or citizenship": "The comment mainly refers to or targets people by national origin or "
                                          "citizenship status (immigrants, migrant workers, undocumented people, "
                                          "people from a named country).",
        "gender or gender identity": "The comment mainly refers to or targets people by gender or gender identity "
                                     "(women, men, non-binary or transgender people).",
        "sexual orientation": "The comment mainly refers to or targets people by sexual orientation (gay, lesbian, "
                              "bisexual or straight people).",
        "age": "The comment mainly refers to or targets people by age group (children, teenagers, young adults, "
               "middle-aged people, seniors).",
        "disability": "The comment mainly refers to or targets people with a physical, cognitive, neurological, "
                      "visual or hearing disability.",
        "political ideology": "The comment mainly refers to or targets people by political ideology or party "
                              "(liberals, conservatives, leftists, Democrats, Republicans, the alt-right).",
    },
}
URL_RE = re.compile(r"\bURL\b|@\w+|#\w+")


def load():
    p = C.CACHE / KEY / "train-00000-of-00001.parquet"
    hf = C.HF / f"datasets--ucberkeley-dlab--measuring-hate-speech/snapshots/{REV}/{FILE}"
    if not p.exists() and hf.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(hf.read_bytes())
    got = C.fetch(URL, p)
    assert got == SHA, f"sha256 mismatch {got}"
    return pd.read_parquet(p), got


def aggregate(d):
    g = d.groupby("comment_id")
    first = g.first()
    rec = pd.DataFrame({
        "text": first["text"], "score": first["hate_speech_score"], "std_err": first["std_err"],
        "platform": first["platform"], "n": g.size(),
        "hs_yes": g["hatespeech"].apply(lambda s: int((s == 2).sum())),
        "hs_no": g["hatespeech"].apply(lambda s: int((s == 0).sum())),
        "hs_unc": g["hatespeech"].apply(lambda s: int((s == 1).sum())),
    })
    assert (g["text"].nunique() == 1).all() and (g["hate_speech_score"].nunique() == 1).all()
    for item in ("violence", "dehumanize", "genocide"):
        rec[item + "_agree"] = g[item].apply(lambda s: int((s >= 3).sum()))
        rec[item + "_dis"] = g[item].apply(lambda s: int((s <= 1).sum()))
    rec["ad_def"] = g["attack_defend"].apply(lambda s: int((s <= 1).sum()))
    rec["ad_att"] = g["attack_defend"].apply(lambda s: int((s >= 3).sum()))
    rec["ad_neu"] = g["attack_defend"].apply(lambda s: int((s == 2).sum()))
    for col in TGT:
        rec[col] = g[col].apply(lambda s: int(s.fillna(False).astype(bool).sum()))
    rec = rec.reset_index()
    return rec


def ok_text(t):
    t = t.strip()
    if not (20 <= len(t) <= 1500):
        return False
    rest = URL_RE.sub(" ", t)
    return len(C.words(rest)) >= 4


def main():
    d, file_sha = load()
    rec = aggregate(d)
    drop = Counter()
    rec = rec[rec["n"] >= MIN_RATERS]
    keep = rec["text"].map(ok_text)
    drop["length/<4 words/only mentions"] = int((~keep).sum())
    rec = rec[keep].copy()
    rec["rid"] = rec["comment_id"].astype(str)
    rng = random.Random(C.SEED)
    order = list(rec["rid"])
    order.sort(key=int)
    rng.shuffle(order)
    pos = {r: i for i, r in enumerate(order)}
    rec["ord"] = rec["rid"].map(pos)
    # reference-set comments (many raters) first, then seeded order
    rec = rec.sort_values(["n", "ord"], ascending=[False, True], key=lambda s: s.clip(upper=10) if s.name == "n" else s)
    items = C.within_dedup(rec.to_dict("records"), lambda r: r["text"])
    drop["within-set duplicate / shared 12-word run"] = len(rec) - len(items)

    texts = {r["rid"]: r["text"] for r in items}
    fh, srcs = C.forbidden_hits(texts, include_mhs=False)
    drop["overlap with forbidden/dev/held-out sources"] = len(fh)
    items = [r for r in items if r["rid"] not in fh]
    oh, nfiles = C.our_file_hits({r["rid"]: r["text"] for r in items}, tag=KEY)
    drop["13-gram overlap with our files"] = len(oh)
    items = [r for r in items if r["rid"] not in oh]
    print(f"pool after filters: {len(items)} comments; drops {dict(drop)}; forbidden hits by source "
          f"{Counter(fh.values()).most_common()}; our-file hits {Counter(oh.values()).most_common(5)}")

    def share(a, b):
        return a / (a + b) if a + b else float("nan")

    for r in items:
        dec = r["hs_yes"] + r["hs_no"]
        hs = share(r["hs_yes"], r["hs_no"])
        r["hs_yes_clear"] = dec >= 3 and hs >= 2 / 3 and r["score"] > 0.5
        r["hs_no_clear"] = dec >= 3 and hs <= 1 / 3 and r["score"] < -0.5
        for item in ("violence", "dehumanize", "genocide"):
            r[item + "_y"] = r[item + "_agree"] == r["n"]   # unanimous agree (4/5 or 5/5 on the item)
            r[item + "_n"] = r[item + "_dis"] == r["n"]     # unanimous disagree (1/5 or 2/5)
        marks = {c: r[c] for c in TGT}
        top = max(marks, key=lambda c: (marks[c], c))
        others = [marks[c] for c in TGT if c != top]
        tot = sum(marks.values())
        r["target_gold"] = top if (marks[top] >= 2 / 3 * r["n"] and max(others) <= r["n"] / 3
                                   and marks[top] >= 0.5 * tot) else None
        r["has_target"] = any(marks[c] >= 2 / 3 * r["n"] for c in TGT)

    used = set()

    def take(pool, n):
        got = []
        for r in pool:
            if len(got) >= n:
                break
            if r["rid"] in used:
                continue
            used.add(r["rid"])
            got.append(r)
        return got

    rows = []

    def yn(r, q, gold, yes_votes, no_votes, orig):
        soft = C.soft_from_counts({"yes": yes_votes, "no": no_votes}, YN)
        minority = min(yes_votes, no_votes) / max(1, yes_votes + no_votes)
        rows.append(mk(r, q, list(YN), gold, soft, "ambiguous" if minority >= 0.25 else None, orig))

    def mk(r, q, opts, gold, soft, edge, orig):
        o = {"n_raters": int(r["n"]), "hate_speech_score": float(r["score"]), "irt_std_err": float(r["std_err"]),
             "platform_code": int(r["platform"])}
        o.update(orig)
        return {"key": KEY, "rid": r["rid"], "state": r["text"].strip(), "instructions": Q[q], "options": opts,
                "gold": gold, "soft": soft,
                "meta": {"dataset": f"{REPO} (Measuring Hate Speech corpus)", "config": f"default/train; question={q}",
                         "revision": f"hf:{REV}; {FILE} sha256:{file_sha}", "licence": LICENCE, "split": "train",
                         "orig_label": o, "family": C.FAMILY, "edge": edge, "defs": q}}

    # The Likert items "violence", "genocide" and "dehumanize" are NOT used as questions: on inspection even
    # unanimous ratings included threats to one person, killing a wife, "euthanize" remarks about non-identity groups
    # and findom spam, i.e. the items were read far more loosely than their wording. The hs benchmark item (highest
    # agreement in Sachdeva et al. 2022), the IRT score and the target marks are used instead.
    # 4) support / counter-speech
    s_yes = take([r for r in items if r["has_target"] and r["ad_def"] >= 2 / 3 * r["n"] and r["score"] < -1.5], 500)
    s_no = take([r for r in items if r["has_target"] and r["ad_att"] >= 2 / 3 * r["n"] and r["score"] > 0], 280)
    s_no += take([r for r in items if r["has_target"] and r["ad_neu"] >= 2 / 3 * r["n"]
                  and -1 <= r["score"] <= 0.5], 500 - len(s_no))
    for r, gold in [(r, "yes") for r in s_yes] + [(r, "no") for r in s_no]:
        yn(r, "support", gold, r["ad_def"], r["ad_att"] + r["ad_neu"],
           {"attack_defend_votes": {"defend": r["ad_def"], "neither": r["ad_neu"], "attack": r["ad_att"]}})
    # 5) target (round-robin over categories)
    pools = {c: [r for r in items if r["target_gold"] == c and r["rid"] not in used] for c in TGT}
    got, i = [], 0
    per = {c: 0 for c in TGT}
    while len(got) < 900 and any(i < len(pools[c]) for c in TGT):
        for c in sorted(TGT):
            if i < len(pools[c]) and len(got) < 900 and per[c] < 225:
                r = pools[c][i]
                if r["rid"] not in used:
                    used.add(r["rid"])
                    got.append(r)
                    per[c] += 1
        i += 1
    for r in got:
        c = r["target_gold"]
        soft = C.soft_from_counts({TGT[k]: r[k] for k in TGT}, TOPTS)
        rows.append(mk(r, "target", list(TOPTS), TGT[c], soft, None,
                       {"target_marks": {TGT[k]: r[k] for k in TGT}}))
    # 6) hate speech benchmark item
    h_yes = take([r for r in items if r["hs_yes_clear"]], 1800)
    # hard negatives first: comments that name a group (target marked) or were rated insulting-ish (IRT >= -1.5)
    h_no = take([r for r in items if r["hs_no_clear"] and r["has_target"] and r["score"] >= -1.5], len(h_yes) // 2)
    h_no += take([r for r in items if r["hs_no_clear"]], len(h_yes) - len(h_no))
    for r, gold in [(r, "yes") for r in h_yes] + [(r, "no") for r in h_no]:
        yn(r, "hs", gold, r["hs_yes"], r["hs_no"], {"hatespeech_votes": {"no": r["hs_no"], "unclear": r["hs_unc"],
                                                                         "yes": r["hs_yes"]}})

    rows = rows[:MAX_ROWS]
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, DEFS)
    print(f"forbidden sources read: {srcs}; our files scanned: {nfiles}")
    C.summary(KEY, rows)
    for q in Q:
        rs = [r for r in rows if r["meta"]["defs"] == q]
        print(q, len(rs), Counter(r["gold"] for r in rs).most_common())


if __name__ == "__main__":
    raise SystemExit("mhs_hate was REJECTED in review (listed in ohs3/used_sources.json as 'avoid'; v0 eval_zs "
                     "role); see the module docstring")
