"""Golden v14 / safety_policy_moderation: raw rows for "misogyny_reddit" (Guest, Vidgen, Mittos, Sastry, Tyson &
Margetts 2021, "An Expert Annotated Dataset for the Detection of Online Misogyny", EACL).

Source  : github.com/ellamguest/online-misogyny-eacl2021 at commit b3c04567452ed92b160c3692343a0f2d74a027b2:
          data/final_labels.csv (agreed labels after expert facilitation; column split = train/test),
          data/original_labels.csv (each annotator's labels before facilitation) and Annotator Codebook.pdf,
          sha256-pinned. Only split == "train" entries are used, as rows and as parent context.
Licence : MIT (repo LICENSE.md, "Copyright (c) 2023 Ella Guest").
Provenance: Reddit posts/comments (Feb-May 2020, 34 subreddits incl. men's-rights, incel and anti-misogyny
          communities) annotated by trained annotators (2-3 per entry, then expert-facilitated agreement) with the
          codebook's hierarchical taxonomy. No model-written text or labels.
Question: misogynistic yes/no ("Is the comment misogynistic?"), gold = level_1 after facilitation; soft = share of
          original (pre-facilitation) annotator level_1 votes. Reviewer fix: rows whose original annotators tied or
          whose majority was overruled in facilitation are dropped (2/15 reviewed rows of that kind contradicted the
          definitions). yes = all usable train entries labelled
          Misogynistic; no = the same number of Nonmisogynistic entries, first every non-misogynistic personal attack
          and counter-speech entry (hard negatives: abusive or about misogyny but not misogynistic), then others.
State   : the entry text; when its parent entry is a train entry in the dataset, the parent is shown first as
          "Replying to: ..." (<= 600 chars) because annotators labelled entries in thread context.
Edge tags: "implicit" when the codebook's strength field says "Nature of the abuse is Implicit"; else "ambiguous" when
          the original annotators split; else null.
Filters: image-based entries (image == "Yes") and rows whose image column holds stray text (CSV quoting damage) are
          dropped; 15-2,000 chars; within-set dedup; forbidden-source, our-file and family decontamination on the
          entry text.
Deterministic (seed 20261129).

  ../.venv/bin/python golden_src/safety_policy_moderation/build_misogyny_reddit.py
"""
import random
from collections import Counter

import pandas as pd

import common as C

KEY = "misogyny_reddit"
COMMIT = "b3c04567452ed92b160c3692343a0f2d74a027b2"
BASE = f"https://raw.githubusercontent.com/ellamguest/online-misogyny-eacl2021/{COMMIT}/"
FILES = {"final_labels.csv": "data/final_labels.csv", "original_labels.csv": "data/original_labels.csv",
         "LICENSE.md": "LICENSE.md", "Annotator_Codebook.pdf": "Annotator%20Codebook.pdf"}
PINNED = {"final_labels.csv": "2db36c213237214a8dcf15861c89dd2b9ff7add1e6ce307fbaa432b000e18251",
          "original_labels.csv": "9bf257057ff8824e4e0ba4a3318e1197d51d3d69bc53dd591e55a640f0ffffa2",
          "LICENSE.md": "50cedbffa0001f47904a35031550d12e3160142033bd17044e38d8629a54f8f6",
          "Annotator_Codebook.pdf": "7a14980218ad716142f47bf3452d510e72c9a4ba6b4a78088d973d1202a58f39"}
LICENCE = (f"MIT (https://github.com/ellamguest/online-misogyny-eacl2021/blob/{COMMIT}/LICENSE.md, "
           "'Copyright (c) 2023 Ella Guest')")
YN = ["yes", "no"]
Q = "Is the comment misogynistic?"
DEFS = {
    "yes": "Misogynistic: a misogynistic pejorative for a person (slut, whore, Stacy), misogynistic abuse at a "
           "named or present woman, or demeaning women as a group, deriding their character, intellect, morals or "
           "bodies or endorsing mistreating them, explicitly or implicitly.",
    "no": "Not misogynistic: unrelated content, discussion of gender or relationships without contempt for women, "
          "counter-speech against misogyny, abuse of a person that is not misogynistic in content, and reclaimed, "
          "neutral or quoted use of pejoratives.",
}


def main():
    shas = {f: C.fetch(BASE + p, C.CACHE / KEY / f, PINNED.get(f)) for f, p in FILES.items()}
    if not PINNED:
        print("PIN", shas)
    fin = pd.read_csv(C.CACHE / KEY / "final_labels.csv", dtype=str, keep_default_na=False)
    org = pd.read_csv(C.CACHE / KEY / "original_labels.csv", dtype=str, keep_default_na=False)
    drop = Counter()
    ok_rows = fin[fin["image"].isin(["", "Yes"]) & fin["level_1"].isin(["Misogynistic", "Nonmisogynistic"])]
    drop["malformed CSV row"] = len(fin) - len(ok_rows)
    train = ok_rows[ok_rows["split"] == "train"]
    by_id = {r.entry_id: r for r in train.itertuples(index=False)}
    votes = {}
    for eid, g in org.groupby("entry_id"):
        votes[eid] = Counter(v for v in g["level_1"] if v in ("Misogynistic", "Nonmisogynistic"))
    recs = []
    for r in train.itertuples(index=False):
        if r.image == "Yes":
            drop["image-based entry"] += 1
            continue
        body = r.body.strip()
        if not (15 <= len(body) <= 2000) or body in ("[deleted]", "[removed]"):
            drop["length/deleted"] += 1
            continue
        v = votes.get(r.entry_id, Counter())
        if sum(v.values()) < 2:
            drop["< 2 original annotations"] += 1
            continue
        pid = r.parent_id.split("_", 1)[1] if "_" in r.parent_id else ""
        parent = by_id.get(pid)
        state = body
        if parent is not None and parent.entry_id != r.entry_id and parent.body.strip() and parent.image != "Yes":
            pb = parent.body.strip()
            pb = pb if len(pb) <= 600 else pb[:600].rsplit(" ", 1)[0] + " ..."
            state = f"Replying to: {pb}\n\nComment: {body}"
        recs.append({"rid": r.entry_id, "text": body, "state": state, "gold": r.level_1, "l2": r.level_2,
                     "l3": r.level_3, "strength": r.strength, "subreddit": r.subreddit, "votes": v})
    rng = random.Random(C.SEED)
    recs.sort(key=lambda x: x["rid"])
    rng.shuffle(recs)
    n0 = len(recs)
    recs = C.within_dedup(recs, lambda x: x["text"])
    drop["within-set duplicate"] = n0 - len(recs)
    fh, srcs = C.forbidden_hits({x["rid"]: x["text"] for x in recs})
    oh, nfiles = C.our_file_hits({x["rid"]: x["text"] for x in recs if x["rid"] not in fh}, tag=KEY)
    fam = C.family_hits({x["rid"]: x["text"] for x in recs}, KEY)
    bad = set(fh) | set(oh) | set(fam)
    drop["forbidden overlap"] = len(fh)
    drop["our-file overlap"] = len(set(oh) - set(fh))
    drop["family overlap"] = len(set(fam) - set(fh) - set(oh))
    recs = [x for x in recs if x["rid"] not in bad]
    print(f"kept {len(recs)}; drops {dict(drop)}; forbidden {Counter(fh.values()).most_common()}; "
          f"family {Counter(fam.values()).most_common()}")

    def overruled(x):
        """Facilitated gold differs from the original annotators' majority (or they tied)."""
        v = x["votes"]
        maj = "Misogynistic" if v["Misogynistic"] > v["Nonmisogynistic"] else (
            "Nonmisogynistic" if v["Nonmisogynistic"] > v["Misogynistic"] else None)
        return maj != x["gold"]

    # reviewer fix: 2 of 15 reviewed rows contradicted the definitions, both tied (1-1) or overruled in facilitation
    # (e.g. a comment discussing the word 'bitch' labelled a misogynistic pejorative); keep only rows whose
    # facilitated label equals the strict majority of the original annotators
    n1 = len(recs)
    recs = [x for x in recs if not overruled(x)]
    drop["original annotators tied or overruled by facilitation"] = n1 - len(recs)
    print(f"after majority filter {len(recs)}; drops {dict(drop)}")
    yes = [x for x in recs if x["gold"] == "Misogynistic"]
    hard = [x for x in recs if x["gold"] == "Nonmisogynistic"
            and x["l2"] in ("Nonmisogynistic_personal_attack", "Counter_speech")]
    hs = {x["rid"] for x in hard}
    no = (hard + [x for x in recs if x["gold"] == "Nonmisogynistic" and x["rid"] not in hs])[:len(yes)]

    def edge(x):
        if "Implicit" in x["strength"]:
            return "implicit"
        v = x["votes"]
        if (v["Misogynistic"] and v["Nonmisogynistic"]) or overruled(x):
            return "ambiguous"
        return None

    rows = []
    for x, g in [(x, "yes") for x in yes] + [(x, "no") for x in no]:
        v = x["votes"]
        rows.append({"key": KEY, "rid": x["rid"], "state": x["state"], "instructions": Q, "options": list(YN),
                     "gold": g, "soft": None if overruled(x) else
                     C.soft_from_counts({"yes": v["Misogynistic"], "no": v["Nonmisogynistic"]}, YN),
                     "meta": {"dataset": "ellamguest/online-misogyny-eacl2021 (Guest et al., EACL 2021)",
                              "config": "data/final_labels.csv split=train (+ original_labels.csv votes)",
                              "revision": f"git:{COMMIT}; sha256 final:{shas['final_labels.csv']} "
                                          f"original:{shas['original_labels.csv']}",
                              "licence": LICENCE, "split": "train",
                              "orig_label": {"level_1": x["gold"], "level_2": x["l2"], "level_3": x["l3"],
                                             "strength": x["strength"], "subreddit": x["subreddit"],
                                             "original_votes": dict(v)},
                              "family": C.FAMILY, "edge": edge(x)}})
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, DEFS)
    print(f"forbidden sources {srcs}; our files {nfiles}")
    C.summary(KEY, rows)
    print("level_2 of rows:", Counter(r["meta"]["orig_label"]["level_2"] for r in rows))


if __name__ == "__main__":
    main()
