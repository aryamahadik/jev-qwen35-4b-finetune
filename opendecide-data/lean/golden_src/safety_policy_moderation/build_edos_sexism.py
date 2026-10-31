"""Golden v14 / safety_policy_moderation: raw rows for "edos_sexism" (EDOS, SemEval-2023 Task 10: Explainable
Detection of Online Sexism; Kirk et al. 2023, arXiv:2303.04222).

Source  : github.com/rewire-online/edos at commit b1f1fbcca9d42de0395432ada8fcfb5c35f68c77 (sha256-pinned):
            data/edos_labelled_aggregated.csv              (gold label_sexist / label_category / label_vector, split)
            data/edos_labelled_individual_annotations.csv  (3 trained annotators per post)
          Rows with split == "train" only (dev/test rows are dropped on read).
Licence : CC0 1.0 Universal (LICENSE file at the repo root, same commit).
Provenance: human Gab and Reddit posts (2019-2021 samples); three trained annotators (women, self-identified) per
          post, disagreements adjudicated by experts. No model-written text or labels.
Questions (each post used once):
  sexist   yes/no  "Is this post sexist?" (Task A). Only posts whose gold equals the annotator majority (expert
                   overrides of a 2-1 or 3-0 majority are dropped); soft = annotator shares.
  vector   choice  11 fine-grained types (Task C) for sexist posts whose gold vector was chosen by >= 2 annotators;
                   soft = vector shares among annotators who said sexist.
  (Task B categories are not asked: they are a deterministic grouping of the Task C types.)
Allocation: vector rows first (round-robin over the 11 types, <= 700), then yes/no rows with every remaining sexist
  post and the same number of not-sexist posts (35% near misses where 1 of 3 annotators said sexist, 65% where none
  did).
Edge tags: "implicit" = gold type in the EDOS "animosity" category (casual gendered slurs, stereotypes, backhanded
  compliments, condescending advice: the paper's implicit/subtle sexism); else "ambiguous" when the annotators split
  (2-1); else null.
Filters: 15-4,000 chars, >= 3 words; within-set dedup; forbidden-source (incl. Social Bias Frames / BTZSC biasframes
  Gab+Reddit dev sets), our-file (drops the ~700 posts already in the v0.13 breadth "edos" rows) and family
  decontamination (common.py).
Deterministic (seed 20261129).

  ../.venv/bin/python golden_src/safety_policy_moderation/build_edos_sexism.py
"""
import random
from collections import Counter, defaultdict

import pandas as pd

import common as C

KEY = "edos_sexism"
REV = "b1f1fbcca9d42de0395432ada8fcfb5c35f68c77"
RAW = f"https://raw.githubusercontent.com/rewire-online/edos/{REV}/"
FILES = {"edos_labelled_aggregated.csv": ("data/edos_labelled_aggregated.csv",
                                          "607bdbb766e1803a28f0eb8fc21c14b6b9dfa20039f726ba6767438584b47f9b"),
         "edos_labelled_individual_annotations.csv": ("data/edos_labelled_individual_annotations.csv",
                                                      "15d430d6756f620b2e83dddd7a3a68dc3e939df3a4c417d184e3c431cc0e20b2"),
         "LICENSE": ("LICENSE", "a2010f343487d3f7618affe54f789f5487602331c0a8d03f49e9a7c547cf0499"),
         "README.md": ("README.md", "1c6135761e05cb841c220786cb2f6410bdd39bafe07a9a3ddcfe4dd93d028299")}
LICENCE = f"CC0 1.0 Universal (LICENSE file at the root of https://github.com/rewire-online/edos/blob/{REV}/LICENSE)"
N_VECTOR = 700

VECTOR = {
    "1.1 threats of harm": "threats of harm",
    "1.2 incitement and encouragement of harm": "incitement and encouragement of harm",
    "2.1 descriptive attacks": "descriptive attacks",
    "2.2 aggressive and emotive attacks": "aggressive and emotive attacks",
    "2.3 dehumanising attacks & overt sexual objectification": "dehumanising attacks and sexual objectification",
    "3.1 casual use of gendered slurs, profanities, and insults": "casual use of gendered slurs, profanities and insults",
    "3.2 immutable gender differences and gender stereotypes": "immutable gender differences and stereotypes",
    "3.3 backhanded gendered compliments": "backhanded gendered compliments",
    "3.4 condescending explanations or unwelcome advice": "condescending explanations or unwelcome advice",
    "4.1 supporting mistreatment of individual women": "supporting mistreatment of individual women",
    "4.2 supporting systemic discrimination against women as a group": "supporting systemic discrimination against women",
}
CATEGORY = {
    "1. threats, plans to harm and incitement": "threats and incitement to harm",
    "2. derogation": "derogation",
    "3. animosity": "animosity",
    "4. prejudiced discussions": "prejudiced discussion",
}
VOPTS, COPTS, YN = list(VECTOR.values()), list(CATEGORY.values()), ["yes", "no"]
Q = {"sexist": "Is this post sexist?",
     "vector": "Which specific type of sexism does this sexist post show?"}
DEFS = {
    "sexist": {
        "yes": "The post is sexist: it contains abuse or negative sentiment directed at women because of their "
               "gender, or their gender combined with another identity such as race, religion or being trans - "
               "including casual gendered slurs, stereotypes and backhanded compliments.",
        "no": "The post is not sexist: it may be rude, crude, about gender or relationships, or abusive toward men or "
              "other groups, but it expresses no abuse or prejudice against women because they are women.",
    },
    "vector": {
        "threats of harm": "The author states an intent, willingness or wish to harm a woman or women, physically, "
                           "sexually, emotionally or by violating their privacy.",
        "incitement and encouragement of harm": "The post urges or encourages others to harm women, or argues that "
                                                "harming women is justified, rather than only insulting them.",
        "descriptive attacks": "The post openly describes women in a derogatory way, such as negative "
                               "generalisations about their abilities, intellect, character, morals, appearance or "
                               "sexual behaviour.",
        "aggressive and emotive attacks": "The post expresses strong negative emotion such as hatred or disgust "
                                          "toward women, through stated feelings, baseless accusations or gendered "
                                          "slurs used to attack women.",
        "dehumanising attacks and sexual objectification": "The post compares women to animals, objects, vermin or "
                                                           "refuse, or reduces them to sexual objects valued only for "
                                                           "sex or their bodies.",
        "casual use of gendered slurs, profanities and insults": "The post uses a slur or insult that traditionally "
                                                                 "describes women, such as bitch or slut, casually "
                                                                 "rather than to deliberately attack women, often "
                                                                 "even aimed at a man.",
        "immutable gender differences and stereotypes": "The post asserts natural or unchangeable differences between "
                                                        "men and women or uses gender stereotypes, including using "
                                                        "women's traits to mock men; most sexist jokes fall here.",
        "backhanded gendered compliments": "The post seems to praise women but actually belittles them, implying "
                                           "they are weak, need protection or matter only for their looks.",
        "condescending explanations or unwelcome advice": "The post gives women patronising or unsolicited advice "
                                                          "or explanations, implying they cannot understand or judge "
                                                          "for themselves.",
        "supporting mistreatment of individual women": "The post denies, understates or justifies mistreatment of a "
                                                       "particular woman or women, such as blaming a victim of abuse "
                                                       "or harassment.",
        "supporting systemic discrimination against women": "The post denies, understates or justifies "
                                                            "discrimination against women as a group, such as denying "
                                                            "sexism exists or opposing women's rights.",
    },
}


def main():
    shas = {f: C.fetch(RAW + path, C.CACHE / KEY / f, sha) for f, (path, sha) in FILES.items()}
    agg = pd.read_csv(C.CACHE / KEY / "edos_labelled_aggregated.csv", dtype=str, keep_default_na=False)
    ind = pd.read_csv(C.CACHE / KEY / "edos_labelled_individual_annotations.csv", dtype=str, keep_default_na=False)
    agg = agg[agg["split"] == "train"]
    ind = ind[ind["split"] == "train"]
    ann = {rid: g for rid, g in ind.groupby("rewire_id")}
    drop = Counter()
    occ = Counter(C.norm(t) for t in agg["text"])
    recs = []
    for r in agg.itertuples(index=False):
        t = r.text.strip()
        if not (15 <= len(t) <= 4000) or len(C.words(t)) < 3:
            drop["length"] += 1
            continue
        if occ[C.norm(t)] > 1:
            drop["text repeated in train"] += 1
            continue
        g = ann[r.rewire_id]
        sv = int((g["label_sexist"] == "sexist").sum())
        n = len(g)
        vv = Counter(v for v in g["label_vector"] if v != "none")
        cv = Counter(v for v in g["label_category"] if v != "none")
        recs.append({"rid": r.rewire_id, "text": t, "gold": r.label_sexist, "vector": r.label_vector,
                     "category": r.label_category, "sv": sv, "n": n, "vv": dict(vv), "cv": dict(cv),
                     "ann": sorted(zip(g["label_sexist"], g["label_vector"]))})
    rng = random.Random(C.SEED)
    recs.sort(key=lambda r: int(r["rid"].rsplit("-", 1)[1]))
    rng.shuffle(recs)
    recs = C.within_dedup(recs, lambda r: r["text"])
    fh, srcs = C.forbidden_hits({r["rid"]: r["text"] for r in recs})
    oh, nfiles = C.our_file_hits({r["rid"]: r["text"] for r in recs if r["rid"] not in fh}, tag=KEY)
    fam = C.family_hits({r["rid"]: r["text"] for r in recs}, KEY)
    drop["forbidden/dev/held-out overlap"] = len(fh)
    drop["13-gram overlap with our files (incl. v0.13 breadth edos rows)"] = len(oh)
    drop["overlap with earlier family sets"] = len(set(fam) - set(fh) - set(oh))
    recs = [r for r in recs if r["rid"] not in fh and r["rid"] not in oh and r["rid"] not in fam]
    print(f"pool {len(recs)}; drops {dict(drop)}; forbidden {Counter(fh.values()).most_common()}; "
          f"our-file {Counter(oh.values()).most_common(3)}; family {Counter(fam.values()).most_common()}")

    majority_ok = [r for r in recs if (r["gold"] == "sexist") == (r["sv"] * 2 > r["n"])]
    drop["gold != annotator majority (expert override)"] = len(recs) - len(majority_ok)
    sexist = [r for r in majority_ok if r["gold"] == "sexist"]
    notsex = [r for r in majority_ok if r["gold"] == "not sexist"]

    def rr(pool, lab, n):
        by = defaultdict(list)
        for r in pool:
            by[lab(r)].append(r)
        out, i = [], 0
        labs = sorted(by)
        while len(out) < n and any(i < len(by[k]) for k in labs):
            for k in labs:
                if i < len(by[k]) and len(out) < n:
                    out.append(by[k][i])
            i += 1
        return out

    def edge(r, q):
        if r["vector"].startswith("3."):
            return "implicit"
        if q == "sexist" and min(r["sv"], r["n"] - r["sv"]) >= 1:
            return "ambiguous"
        if q != "sexist" and r["vv"] and max(r["vv"].values()) < sum(r["vv"].values()):
            return "ambiguous"
        return None

    def mk(r, q, opts, gold, soft):
        return {"key": KEY, "rid": r["rid"], "state": r["text"], "instructions": Q[q], "options": opts, "gold": gold,
                "soft": soft,
                "meta": {"dataset": "rewire-online/edos (EDOS, SemEval-2023 Task 10)",
                         "config": f"edos_labelled_aggregated.csv split=train; question={q}",
                         "revision": f"git:{REV}; sha256 aggregated:{shas['edos_labelled_aggregated.csv']} "
                                     f"individual:{shas['edos_labelled_individual_annotations.csv']}",
                         "licence": LICENCE, "split": "train",
                         "orig_label": {"label_sexist": r["gold"], "label_category": r["category"],
                                        "label_vector": r["vector"], "annotator_labels": r["ann"]},
                         "family": C.FAMILY, "edge": edge(r, q), "defs": q}}

    rows = []
    vpool = [r for r in sexist if r["vv"].get(r["vector"], 0) >= 2]
    vrows = rr(vpool, lambda r: r["vector"], N_VECTOR)
    for r in vrows:
        rows.append(mk(r, "vector", VOPTS, VECTOR[r["vector"]],
                       C.soft_from_counts({VECTOR[k]: v for k, v in r["vv"].items()}, VOPTS)))
    used = {r["rid"] for r in vrows}
    yes = [r for r in sexist if r["rid"] not in used]
    near = [r for r in notsex if r["sv"] == 1][:int(0.35 * len(yes))]   # 1 of 3 annotators said sexist
    no = near + [r for r in notsex if r["sv"] == 0][:len(yes) - len(near)]
    for r in yes + no:
        rows.append(mk(r, "sexist", YN, "yes" if r["gold"] == "sexist" else "no",
                       C.soft_from_counts({"yes": r["sv"], "no": r["n"] - r["sv"]}, YN)))
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, DEFS)
    print(f"forbidden sources {srcs}; our files {nfiles}; drops {dict(drop)}")
    C.summary(KEY, rows)


if __name__ == "__main__":
    main()
