"""Golden v14 / safety_policy_moderation: raw rows for "ghc_hate" (Gab Hate Corpus, Kennedy et al., 2022, Language
Resources & Evaluation).

Source : OSF project edua3 ("The Gab Hate Corpus"), Data folder (sha256-pinned):
           ghc_train.tsv                  (https://osf.io/download/x5pdg/)  -> gold hd / cv / vo
           GabHateCorpus_annotations.tsv  (https://osf.io/download/wuecz/)  -> per-annotator codes
           GabHateCorpus_trainingmanual.pdf (https://osf.io/download/nqt6h/) -> definitions
         ghc_test.tsv is NEVER downloaded or read. The annotations file covers train + test posts; it is joined on the
         exact post text of ghc_train.tsv; a train text is dropped when it occurs more than once in ghc_train.tsv or
         maps to more than one annotation ID (a second ID could be a test copy).
Licence: CC BY 4.0, the OSF node licence of edua3 ("CC-By Attribution 4.0 International", OSF API /v2/nodes/edua3/
         -> license 563c1cf88c5e4a3877f9e96a; shown on https://osf.io/edua3/).
Provenance: Gab posts (human-written, 2016-2018); labels by trained human annotators (>= 3 per post) following the
         project's coding manual. HD = assault on human dignity, CV = call for violence, VO = vulgarity/offensive
         language; train gold = annotator mean >= 0.5 (checked; disagreeing rows dropped). Target types and
         explicit/implicit (EX/IM) are coded only by annotators who marked the post hateful.
Questions (each post used at most once; allocation order cv -> target -> vo -> hd):
  cv     yes/no  every clean CV post; negatives = near misses (HD but not CV), same count.
  target choice  8 target types for HD/CV posts; gold = type marked by the most hateful-coding annotators when that
                 count is >= 2, >= half of them and strictly highest; round-robin, <= 300 rows (reviewer: was 450; the hd yes/no question gets the rest).
  vo     yes/no  yes = VO posts that are NOT hateful (vulgar/abusive but no group attack; the hard boundary); no = half
                 near misses (HD but not VO), half other posts; <= 600 per side.
  hd     yes/no  yes = all remaining HD posts; no = same count, 40% near misses (VO but not HD), 60% other posts.
  Soft labels = annotator share {yes: mean, no: 1 - mean}; target soft = share of target marks per type.
  Reviewer fix (3/15 labels wrong in review, all at the 2-of-3 or tie level): a post answers a question only when its
  annotators clearly agree - ties (mean 0.5, 3 of 5) are never used; a 2-of-3 hd/cv yes also needs >= 2 coders marking
  the same target type; vo yes needs mean >= 3/4 and vo no a zero mean; hd negatives need a zero hd mean.
Edge tags: "implicit" when most hateful-coding annotators coded the hate as implicit (IM) rather than explicit;
  "ambiguous" when the annotator mean is within (0.25, 0.75); else null.
Decontamination (drop, never edit): common.py forbidden sources (label-NLI incl. implicit-hate Gab posts, Social Bias
  Frames incl. Gab, BTZSC biasframes dev, HateXplain Gab, MHS, ...), 13-gram our-file scan (drops the ~650 posts
  already in the v0.13 breadth "ghc" rows) and earlier family sets.
Deterministic (seed 20261129).

  ../.venv/bin/python golden_src/safety_policy_moderation/build_ghc_hate.py
"""
import random
import re
from collections import Counter, defaultdict

import pandas as pd

import common as C

KEY = "ghc_hate"
SRC = {
    "ghc_train.tsv": ("https://osf.io/download/x5pdg/",
                      "c82a27336560d3a6822a4cc3f92856481af5fd63aa2ce8d0ca644d440d351d43"),
    "GabHateCorpus_annotations.tsv": ("https://osf.io/download/wuecz/",
                                      "70b1b0657a1d715a06ff026395afee8e99f05c4ccc166ff577870260b07aa779"),
    "GabHateCorpus_trainingmanual.pdf": ("https://osf.io/download/nqt6h/",
                                         "af0ee38a2117c2fa51bcd283c647aaece2aa66678b94f2668e6e26aab33a2070"),
}
DATASET = "Gab Hate Corpus (OSF edua3)"
REVISION = (f"osf:edua3 ghc_train.tsv sha256:{SRC['ghc_train.tsv'][1]}; annotations sha256:"
            f"{SRC['GabHateCorpus_annotations.tsv'][1]}")
LICENCE = ("CC BY 4.0 (OSF node licence of https://osf.io/edua3/ 'CC-By Attribution 4.0 International', "
           "OSF API license id 563c1cf88c5e4a3877f9e96a; Kennedy et al., The Gab Hate Corpus)")
YN = ["yes", "no"]
Q = {
    "hd": "Does this post assault the human dignity of people because of a group they belong to?",
    "cv": "Does this post call for or endorse violence, expulsion, exclusion or segregation against people because of "
          "a group they belong to?",
    "vo": "Does this post use vulgar, offensive or abusive language?",
    "target": "Which type of group does this post's hateful rhetoric mainly target?",
}
TARGETS = {
    "RAE": "race or ethnicity", "NAT": "nationality or region", "GEN": "gender", "REL": "religion",
    "SXO": "sexual orientation", "IDL": "ideology", "POL": "political affiliation", "MPH": "health or disability",
}
TOPTS = list(TARGETS.values())
DEFS = {  # from GabHateCorpus_trainingmanual.pdf, section 4 ("Coding Manual/Procedure", "Targeted Populations")
    "hd": {
        "yes": "The post degrades people because of their group (race, nationality, gender, religion, sexual "
               "orientation, ideology, politics, health): asserting inferiority, comparing them to animals or "
               "subhumans, slurs meant to wound, hateful stereotypes, or support for hateful ideology.",
        "no": "No: insults or vulgarity at a person without invoking their group, criticism of policies, parties or "
              "ideas that does not degrade people, and neutral mentions of groups do not assault anyone's dignity "
              "because of a group.",
    },
    "cv": {
        "yes": "The post advocates or endorses violence, genocide, expulsion, exclusion or segregation against a "
               "group, or against a person because of their group (for example deporting or banning all members).",
        "no": "The post calls for no violence, expulsion, exclusion or segregation of a group: degrading, insulting "
              "or stereotyping a group without advocating such action is no, as are threats at a person that do not "
              "invoke their group.",
    },
    "vo": {
        "yes": "The post uses vulgar, obscene, derogatory or abusive wording or personal insults (swearing, slurs, "
               "name-calling), whether or not it attacks any group.",
        "no": "The post has no vulgar, obscene or abusive wording: hateful or political views stated in clean, "
              "polite or neutral language are no, even when the view itself is offensive.",
    },
    "target": {
        "race or ethnicity": "The hateful rhetoric mainly targets people for their race or ethnicity, such as "
                             "anti-Black, anti-Asian, anti-Latino, anti-Arab, or antisemitic attacks on Jews as a people.",
        "nationality or region": "The hateful rhetoric mainly targets people for their nationality, country or region "
                                 "of origin, including general xenophobia and attacks on immigrants as foreigners.",
        "gender": "The hateful rhetoric mainly targets people for their gender or gender identity, such as "
                  "anti-woman, anti-man or anti-trans attacks.",
        "religion": "The hateful rhetoric mainly targets people for their religion or spiritual beliefs, such as "
                    "anti-Muslim or anti-Christian attacks on believers or the faith.",
        "sexual orientation": "The hateful rhetoric mainly targets people for their sexual orientation, such as "
                              "gay, lesbian or bisexual people.",
        "ideology": "The hateful rhetoric mainly targets people for their ideology or worldview, such as liberals, "
                    "leftists or conservatives as a camp of believers, not as members of a party.",
        "political affiliation": "The hateful rhetoric mainly targets members of a political organisation or party, "
                                 "such as Democrats or Republicans, or a named party's members or politicians.",
        "health or disability": "The hateful rhetoric mainly targets people for their mental or physical health "
                                "status, mental illness or a physical disability.",
    },
}
URL = re.compile(r"https?://\S+|www\.\S+")
DANGLING = {"the", "of", "a", "an", "to", "and", "in", "for", "with", "their", "his", "her", "on", "at", "by", "from",
            "or", "your", "my", "our", "ur"}


def cut_off(t):
    t = t.rstrip()
    if re.search(r"(^|\s)@\w{0,2}$", t):
        return True
    w = re.findall(r"[A-Za-z']+|\S", t)
    return bool(w) and w[-1].lower() in DANGLING


def main():
    shas = {f: C.fetch(u, C.CACHE / KEY / f, h) for f, (u, h) in SRC.items()}
    tr = pd.read_csv(C.CACHE / KEY / "ghc_train.tsv", sep="\t", dtype={"text": str}, keep_default_na=False)
    an = pd.read_csv(C.CACHE / KEY / "GabHateCorpus_annotations.tsv", sep="\t", dtype={"Text": str},
                     keep_default_na=False,
                     na_values={c: [""] for c in ["Hate", "HD", "CV", "VO", *TARGETS, "EX", "IM"]})
    drop = Counter()
    occ = Counter(tr["text"])
    ids_of = an.groupby("Text")["ID"].agg(lambda s: sorted(set(s))).to_dict()
    by_id = {i: g for i, g in an.groupby("ID")}
    posts, seen = [], set()
    for r in tr.itertuples(index=False):
        text = r.text
        if occ[text] > 1:
            drop["text repeated in train"] += 1
            continue
        ids = ids_of.get(text, [])
        if len(ids) != 1:
            drop["0 or >1 annotation IDs (possible test copy)"] += 1
            continue
        if not (15 <= len(text.strip()) <= 4000) or cut_off(text) or len(C.words(URL.sub(" ", text))) < 3:
            drop["length / cut off / < 3 words"] += 1
            continue
        n = C.norm(text)
        if n in seen:
            drop["duplicate normalised text"] += 1
            continue
        seen.add(n)
        g = by_id[ids[0]]
        p = {"rid": str(ids[0]), "text": text.strip(), "n_ann": len(g)}
        ok = True
        for c in ("hd", "cv", "vo"):
            m = float(g[c.upper()].mean())
            p[c] = int(getattr(r, c))
            p[c + "_p"] = m
            if (m >= 0.5) != bool(p[c]):
                ok = False
        if not ok:
            drop["train gold disagrees with annotations"] += 1
            continue
        hate = g[g["Hate"] == 1]
        p["n_hate"] = len(hate)
        p["tcount"] = {k: int(hate[k].fillna(0).sum()) for k in TARGETS}
        p["im"] = int(hate["IM"].fillna(0).sum())
        p["ex"] = int(hate["EX"].fillna(0).sum())
        posts.append(p)
    rng = random.Random(C.SEED)
    posts.sort(key=lambda p: int(p["rid"]))
    rng.shuffle(posts)
    posts = C.within_dedup(posts, lambda p: p["text"])
    fh, srcs = C.forbidden_hits({p["rid"]: p["text"] for p in posts})
    oh, nfiles = C.our_file_hits({p["rid"]: p["text"] for p in posts if p["rid"] not in fh}, tag=KEY)
    fam = C.family_hits({p["rid"]: p["text"] for p in posts}, KEY)
    drop["forbidden/dev/held-out overlap"] = len(fh)
    drop["13-gram overlap with our files"] = len(oh)
    drop["overlap with earlier family sets"] = len(set(fam) - set(fh) - set(oh))
    posts = [p for p in posts if p["rid"] not in fh and p["rid"] not in oh and p["rid"] not in fam]
    print(f"clean posts {len(posts)}; drops {dict(drop)}; forbidden {Counter(fh.values()).most_common()}; "
          f"our-file {Counter(oh.values()).most_common(4)}; family {Counter(fam.values()).most_common()}")
    order = {p["rid"]: i for i, p in enumerate(posts)}
    used, rows = set(), []

    def take(pool, n):
        got = []
        for p in sorted(pool, key=lambda p: order[p["rid"]]):
            if len(got) >= n:
                break
            if p["rid"] in used:
                continue
            used.add(p["rid"])
            got.append(p)
        return got

    def edge(p, c):
        if c in ("hd", "cv", "target") and (p["hd"] or p["cv"]) and p["im"] > p["ex"]:
            return "implicit"
        if c in ("hd", "cv", "vo") and 0.25 < p[c + "_p"] < 0.75:
            return "ambiguous"
        return None

    def mk(p, q, opts, gold, soft, orig):
        orig = dict(orig, n_annotators=p["n_ann"])
        return {"key": KEY, "rid": p["rid"], "state": p["text"], "instructions": Q[q], "options": opts, "gold": gold,
                "soft": soft, "meta": {"dataset": DATASET, "config": f"ghc_train.tsv+annotations; question={q}",
                                       "revision": REVISION, "licence": LICENCE, "split": "train", "orig_label": orig,
                                       "family": C.FAMILY, "edge": edge(p, q), "defs": q}}

    def yn(p, c):
        m = p[c + "_p"]
        return mk(p, c, list(YN), "yes" if p[c] else "no", C.soft_from_counts({"yes": m, "no": 1 - m}, YN),
                  {"hd": p["hd"], "cv": p["cv"], "vo": p["vo"], "annotator_mean_" + c: round(m, 4),
                   "implicit_marks": p["im"], "explicit_marks": p["ex"]})

    # reviewer fix (label reliability): a post answers a question only when its annotators clearly agree. Ties
    # (mean 0.5, 3 of 5) are never used; a 2-of-3 hate vote (hd/cv) also needs >= 2 coders marking the same target
    # group; vo (the noisiest code) needs >= 3/4 for yes and a zero mean for no; hd negatives need a zero hd mean.
    def Y(p, c, strict=False):
        m = p[c + "_p"]
        if not p[c] or m < (0.75 if strict else 2 / 3) - 1e-9:
            return False
        return m >= 0.75 - 1e-9 or c == "vo" or max(p["tcount"].values()) >= 2

    def N(p, c, strict=False):
        return not p[c] and p[c + "_p"] <= (0.0 if strict else 1 / 3) + 1e-9

    # cv
    cv_yes = take([p for p in posts if Y(p, "cv")], 10 ** 6)
    cv_no = take([p for p in posts if Y(p, "hd") and N(p, "cv")], len(cv_yes))
    rows += [yn(p, "cv") for p in cv_yes + cv_no]

    # target
    def tgold(p):
        if not (Y(p, "hd") or Y(p, "cv")):
            return None
        cnt = sorted(p["tcount"].items(), key=lambda kv: (-kv[1], kv[0]))
        (k1, c1), (_, c2) = cnt[0], cnt[1]
        return k1 if (c1 >= 2 and c1 >= p["n_hate"] / 2 and c1 > c2) else None
    pools = defaultdict(list)
    for p in posts:
        if p["rid"] not in used and tgold(p):
            pools[tgold(p)].append(p)
    got, i = [], 0
    while len(got) < 300 and any(i < len(v) for v in pools.values()):
        for k in sorted(pools):
            if i < len(pools[k]) and len(got) < 300 and sum(tgold(x) == k for x in got) < 100:
                got.append(pools[k][i])
        i += 1
    for p in got:
        used.add(p["rid"])
        k = tgold(p)
        rows.append(mk(p, "target", list(TOPTS), TARGETS[k],
                       C.soft_from_counts({TARGETS[c]: p["tcount"][c] for c in TARGETS}, TOPTS),
                       {"target_code": k, "target_marks": p["tcount"], "n_hateful_coders": p["n_hate"]}))
    # vo
    vo_yes = take([p for p in posts if Y(p, "vo", True) and N(p, "hd", True) and N(p, "cv", True)], 600)
    vo_no = take([p for p in posts if Y(p, "hd") and N(p, "vo", True)], len(vo_yes) // 2)
    vo_no += take([p for p in posts if N(p, "vo", True) and N(p, "hd", True)], len(vo_yes) - len(vo_no))
    rows += [yn(p, "vo") for p in vo_yes + vo_no]
    # hd
    hd_yes = take([p for p in posts if Y(p, "hd")], 10 ** 6)
    hd_no = take([p for p in posts if Y(p, "vo") and N(p, "hd", True)], int(0.4 * len(hd_yes)))
    hd_no += take([p for p in posts if N(p, "hd", True) and N(p, "vo", True)], len(hd_yes) - len(hd_no))
    rows += [yn(p, "hd") for p in hd_yes + hd_no]

    rng.shuffle(rows)
    C.write_outputs(KEY, rows, DEFS)
    print(f"forbidden sources {srcs}; our files {nfiles}; sha {shas}")
    C.summary(KEY, rows)


if __name__ == "__main__":
    main()
