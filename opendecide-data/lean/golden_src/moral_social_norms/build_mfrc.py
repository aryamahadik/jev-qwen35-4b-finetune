"""Build raw rows for mfrc (Moral Foundations Reddit Corpus; Trager et al., LREC 2026 / arXiv 2208.05545).

Source : HF USC-MOLA-Lab/MFRC (the authors' lab; the paper links this repo), revision
         ddc21d2f03e156732fd1ba95a51c4c29f07975be, file final_mfrc_data.csv (one row per comment x annotator).
Licence: CC BY 4.0, stated in the dataset card README.md "### Licensing Information: cc-by-4.0" (same revision).
Texts  : English Reddit comments (12 subreddits; comments, not posts), annotated by >= 3 trained undergraduate
         annotators with the MFT coding manual (paper Appendix A). No model-written text or labels. No splits -> train.
Labels : per comment, the share of annotators marking each foundation (Care, Equality, Proportionality, Loyalty,
         Authority, Purity) and the share marking anything other than Non-Moral. These shares are the soft labels.
Tasks  (each comment used once):
- foundation (yes/no, one of 6 questions): yes = share >= 2/3 (at least 2 annotators); no = share == 0, taken 70% from
  comments that ARE moral (>= 2/3) but about another foundation or thin morality (hard negatives) and 30% from
  unanimously non-moral comments. Per foundation: yes rows <= 700, same number of no rows.
- moral presence (yes/no): yes = moral share >= 2/3; no = unanimously Non-Moral; fills the rest up to MAX_ROWS.
Cleaning: exact duplicate file rows collapsed; comments where one annotator has two different annotations dropped;
HTML entities unescaped; [deleted]/[removed], < 8 words or > 2,000 chars dropped; exact + near-duplicate
(word 5-gram Jaccard >= 0.8) comments dropped; ambiguous middle shares (0 < share < 2/3) never used.
Deterministic (seed 20261101).
"""
import collections
import html
import random
import re

import pandas as pd

from common import (CACHE, FAMILY, NearDup, append_manifest, edge_join, edge_tags, fetch, show, summary, toks,
                    write_defs, write_rows, yesno_share)

KEY = "mfrc"
SEED = 20261101
MAX_ROWS = 8000
PER_F_YES = 700
REV = "ddc21d2f03e156732fd1ba95a51c4c29f07975be"
BASE = f"https://huggingface.co/datasets/USC-MOLA-Lab/MFRC/resolve/{REV}/"
FILES = {"final_mfrc_data.csv": "f7ad7a41d65d4932e11054065cccfadacecbc84628527aa89bcc14601da7feff",
         "README.md": "992edde48e9484e60917b3285c6a0661cea184ae81020d2b7c6792df4013e275"}
LICENCE = (f"CC BY 4.0 (https://huggingface.co/datasets/USC-MOLA-Lab/MFRC/blob/{REV}/README.md, "
           "'Licensing Information: cc-by-4.0'; authors' lab repo linked from the paper)")
FOUND = {
    "Care": ("Care (protecting people, animals or other living things from harm; kindness versus cruelty)",
             "caring for, protecting or harming people, animals or other living things (kindness, compassion versus cruelty, abuse, suffering)"),
    "Equality": ("Equality (equal treatment and equal outcomes for all people and groups)",
                 "equal treatment and equal outcomes for all individuals and groups (social justice, equal rights versus discrimination, prejudice, inequality)"),
    "Proportionality": ("Proportionality (people getting what they deserve in proportion to their effort, merit or deeds)",
                        "people being rewarded or punished in proportion to their effort, merit or deeds (deservingness versus freeloading, corruption, nepotism)"),
    "Loyalty": ("Loyalty (standing by one's group, family, community or nation versus betraying it)",
                "loyalty to, cooperation with or betrayal of one's in-group, family, community, region or nation (solidarity, patriotism versus treason, abandonment)"),
    "Authority": ("Authority (respecting legitimate authority, tradition and social order versus subverting it)",
                  "respect for or subversion of legitimate authorities, traditions, laws, social roles and institutions (obedience, duty, order versus disorder, rebellion)"),
    "Purity": ("Purity (sanctity, cleanliness or holiness versus degradation, contamination or sin)",
               "purity, sanctity or degradation of bodies, people, objects or the sacred (cleanliness, holiness, chastity versus disgust, contamination, sin)"),
}
Q_F = "Does this Reddit comment express a moral concern about {}?"
Q_MORAL = "Does this Reddit comment express a moral judgement or moral concern (as opposed to being non-moral)?"


def defs_for(f):
    gloss = FOUND[f][1]
    return {
        "yes": f"At least two-thirds of the trained annotators judged that the comment voices a concern, belief, attitude "
               f"or emotion about {gloss}, praising the virtue or condemning the vice, explicitly or implicitly.",
        "no": f"No annotator found a {f} concern: the comment is non-moral, or its moral content is about another "
              f"foundation or a plain good/bad judgement; merely mentioning a related topic without a moral stance does not count.",
    }


DEFS_MORAL = {
    "yes": "At least two-thirds of the trained annotators judged that the comment evaluates something as morally right or "
           "wrong, good or bad, or voices concern about care, fairness, loyalty, authority or purity.",
    "no": "Every annotator judged the comment non-moral: it states facts, preferences, jokes, questions or opinions on "
          "non-moral matters (for example strategy or taste) without evaluating anyone as morally right or wrong.",
}

JUNK = re.compile(r"^\s*\[(deleted|removed)\]\s*$", re.I)


def clean(t):
    t = html.unescape(t).replace("\r", "")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return t


def main():
    rng = random.Random(SEED)
    paths = {f: fetch(BASE + f, CACHE / "mfrc" / f, sha) for f, sha in FILES.items()}
    df = pd.read_csv(paths["final_mfrc_data.csv"], keep_default_na=False, dtype=str)
    stats = collections.Counter()
    per = collections.defaultdict(dict)  # text -> annotator -> set(labels)
    meta = {}
    conflicted = set()
    for r in df.itertuples(index=False):
        labs = {x.strip() for x in r.annotation.split(",") if x.strip()}
        if not labs:
            stats["empty_annotation"] += 1
            continue
        if r.annotator in per[r.text]:
            if per[r.text][r.annotator] != labs:
                conflicted.add(r.text)  # same annotator, two different annotations -> drop the comment
            stats["dup_row"] += 1
            continue
        per[r.text][r.annotator] = labs
        meta.setdefault(r.text, (r.subreddit, r.bucket))
    recs = []
    nd = NearDup(thr=0.8)
    for text in sorted(per):
        anns = per[text]
        n = len(anns)
        t = clean(text)
        if text in conflicted:
            stats["drop_conflicting_annotations"] += 1
            continue
        if n < 3 or JUNK.match(t) or len(toks(t)) < 8 or len(t) > 2000:
            stats["drop_filter"] += 1
            continue
        if nd.seen(t):
            stats["drop_dup"] += 1
            continue
        moral = sum(1 for s in anns.values() if s - {"Non-Moral"}) / n
        shares = {f: sum(1 for s in anns.values() if f in s) / n for f in FOUND}
        recs.append({"text": t, "n": n, "moral": moral, "shares": shares, "sub": meta[text][0],
                     "bucket": meta[text][1], "rid": f"mfrc-{abs(hash(t)) % 10**12}"})
    # stable rid independent of PYTHONHASHSEED
    import hashlib
    for r in recs:
        r["rid"] = "mfrc-" + hashlib.sha1(r["text"].encode()).hexdigest()[:16]
    print("comments:", len(recs), dict(stats))
    recs.sort(key=lambda r: r["rid"])
    rng.shuffle(recs)

    used = set()
    rows = []
    TH = 2 / 3 - 1e-9

    def add(r, qid, gold, soft):
        used.add(r["rid"])
        tags = []
        if len(r["text"]) > 1000:
            tags.append("long_context")
        if re.search(r"(^|\n)\s*>", r["text"]):
            tags.append("reported_speech")
        q = Q_MORAL if qid == "moral" else Q_F.format(FOUND[qid][0])
        rows.append({
            "key": KEY, "rid": f"{r['rid']}::{qid}", "state": r["text"], "instructions": q,
            "options": ["yes", "no"], "gold": gold, "soft": soft,
            "meta": {"dataset": "USC-MOLA-Lab/MFRC", "config": f"final_mfrc_data.csv:{qid}", "revision": REV,
                     "licence": LICENCE, "split": "train",
                     "orig_label": {"n_annotators": r["n"], "moral_share": round(r["moral"], 4),
                                    "shares": {k: round(v, 4) for k, v in r["shares"].items() if v > 0},
                                    "subreddit": r["sub"], "bucket": r["bucket"]},
                     "family": FAMILY, "edge": edge_join(tags), "defs": qid},
        })

    # 1) foundation yes rows, scarcest foundation first; a comment goes to its scarcest qualifying foundation
    cnt = {f: sum(r["shares"][f] >= TH for r in recs) for f in FOUND}
    order = sorted(FOUND, key=lambda f: (cnt[f], f))
    print("foundation yes candidates:", cnt)
    yes_n = {}
    for f in order:
        got = 0
        for r in recs:
            if got >= PER_F_YES:
                break
            if r["rid"] in used or r["shares"][f] < TH:
                continue
            p = r["shares"][f]
            add(r, f, "yes", {"yes": round(p, 4), "no": round(1 - p, 4)})
            got += 1
        yes_n[f] = got
    # 2) foundation no rows: 70% moral-but-other-foundation, 30% unanimously non-moral
    for f in order:
        need = yes_n[f]
        hard = round(need * 0.7)
        got_h = got_e = 0
        for r in recs:
            if got_h >= hard:
                break
            if r["rid"] in used or r["shares"][f] > 0 or r["moral"] < TH:
                continue
            add(r, f, "no", {"yes": 0.0, "no": 1.0})
            got_h += 1
        for r in recs:
            if got_e >= need - got_h:
                break
            if r["rid"] in used or r["moral"] > 0:
                continue
            add(r, f, "no", {"yes": 0.0, "no": 1.0})
            got_e += 1
    # 3) moral presence rows, balanced, to fill up to MAX_ROWS
    rest = MAX_ROWS - len(rows)
    ym = [r for r in recs if r["rid"] not in used and r["moral"] >= TH]
    nm = [r for r in recs if r["rid"] not in used and r["moral"] == 0]
    k = min(rest // 2, len(ym), len(nm))
    for r in ym[:k]:
        add(r, "moral", "yes", {"yes": round(r["moral"], 4), "no": round(1 - r["moral"], 4)})
    for r in nm[:rest - k]:
        add(r, "moral", "no", {"yes": 0.0, "no": 1.0})

    rng.shuffle(rows)
    write_rows(KEY, rows)
    for f in FOUND:
        write_defs(f"{KEY}__{f}", defs_for(f))
    write_defs(f"{KEY}__moral", DEFS_MORAL)
    summary(rows)
    print("subreddits:", collections.Counter(r["meta"]["orig_label"]["subreddit"] for r in rows).most_common())
    show(rows, 5, seed=SEED)
    append_manifest({
        "key": KEY, "family": FAMILY, "dataset": "USC-MOLA-Lab/MFRC (Moral Foundations Reddit Corpus)",
        "licence": LICENCE, "rows": len(rows), "qtype": "yesno", "yesno_share": yesno_share(rows),
        "edge_tags": edge_tags(rows),
        "notes": ("no official splits (counts as train); 6 foundation questions (yes >= 2/3 of >= 3 trained annotators, "
                  "no = 0 votes, 70% hard negatives from moral comments about other foundations) + moral-vs-non-moral; "
                  "soft = real annotator vote shares; each comment used once; near-duplicates removed."),
    })


if __name__ == "__main__":
    main()
