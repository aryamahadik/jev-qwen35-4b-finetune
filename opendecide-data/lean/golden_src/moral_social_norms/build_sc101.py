"""Build raw rows for sc101 (Social-Chem-101, Forbes et al., EMNLP 2020), TRAIN split only.

Source : https://storage.googleapis.com/ai2-mosaic-public/projects/social-chemistry/data/social-chem-101.zip
         (GCS object generation 1604370600946981, last-modified 2020-11-03; sha256 pinned below), file
         social-chem-101.v1.0.tsv. Repo README pinned at github mbforbes/social-chemistry-101 commit
         116ead94d7e25dd8c02302c0642de63e99d50477.
Licence: CC BY-SA 4.0, stated in that README.md ("The dataset is licensed under the CC BY-SA 4.0 license.").
Texts  : situations = r/confessions titles, ROCStories sentences, Dear Abby headlines; rules-of-thumb (RoTs), actions
         and all attributes written/labelled by crowd workers (human). No model-written text.
Rules  :
- split == 'train' only (dev/test/dev-extra/test-extra/analysis never read into rows); rot-bad == 0.
- area 'amitheasshole' is DROPPED: those situations are Scruples anecdote titles and `scruples` is a forbidden
  label-NLI task (derivation rule).
- Moral Stories (demelin/moral_stories, OHS-2) takes its norms from Social-Chem-101: every RoT whose normalised text
  matches a Moral Stories norm exactly or by token-set Jaccard >= 0.6, and every action that is a contiguous word run of
  a Moral Stories norm, is DROPPED (all 12k Moral Stories norms loaded only for this exclusion).
Tasks (each RoT record used at most once; each normalised action text used at most once):
- acceptability (yes/no): state = situation + the worker's action phrase; gold from `action-moral-judgment`
  (-2/-1 -> not acceptable; 0/1/2 -> acceptable). Only consensus items: action-agree >= 3 AND rot-agree >= 3
  (>= 75% of people estimated to agree), action-agency == 'agency', a character is doing / probably doing the action
  (action-hypothetical in {explicit, probable}), and the RoT is categorised as morality-ethics and/or social-norms
  (pure 'advice' and any 'description' RoTs dropped: they judge usefulness or describe habits, not social
  acceptability). 30% of rows ask the negated question ("... wrong ...?") with the answer flipped. At most 2 rows
  per situation (a second row only if it has the opposite answer). Actions that are feelings or mental states
  ('hating ...', 'being jealous ...', 'wanting ...') are dropped: the question is about conduct. Soft labels: none (train RoTs have one breakdown;
  the triple-annotated m == 3 subset is AITA-only and dropped).
- legality (yes/no): state = the action phrase; "Is this action against the law in most places?". yes = worker
  marked 'illegal' AND judged it bad AND the phrase names a clear crime (keyword list below) AND it is not on the
  reviewer false-positive list ILLEGAL_FP_RE (victims, idioms, acquittals, accidents, mental states); no = worker marked
  'legal' AND no crime/risky keyword; 60% of the 'no' rows are actions judged bad (wrong-but-legal contrast).
Deterministic (seed 20261101).
"""
import collections
import json
import random
import re
import zipfile

import pandas as pd

from common import (CACHE, FAMILY, EXC_RE, NEG_RE, NearDup, TokenSetIndex, append_manifest, edge_join, edge_tags,
                    fetch, norm, show, summary, toks, write_defs, write_rows, yesno_share)

KEY = "sc101"
SEED = 20261101
N_ACC = 7640
N_LEGAL = 1500
C = CACHE / "sc101"
ZIP_URL = "https://storage.googleapis.com/ai2-mosaic-public/projects/social-chemistry/data/social-chem-101.zip"
ZIP_SHA = "ebaa524280c53aa3dbfb2b73502b120eeb71d03523a557c659275aebb2afd95a"
TSV_SHA = "6a289ec5f814ec975deacc244ed7b5758911611847c0834bf6b2f32817722aea"
README_COMMIT = "116ead94d7e25dd8c02302c0642de63e99d50477"
README_URL = f"https://raw.githubusercontent.com/mbforbes/social-chemistry-101/{README_COMMIT}/README.md"
README_SHA = "54ce0b9d67afb2939b9f9a234fd2581a4e7b0fa752ebdb84030818dac407381f"
MS_URL = ("https://huggingface.co/datasets/demelin/moral_stories/resolve/b830cf56eb00bc4edd1860dd544a192216eb3587/"
          "data/moral_stories_full.jsonl")
MS_SHA = "98a62d4a083e02ba234ca3d4f2312df6c337ef10cd3f12dcf917a2957ba59c10"
LICENCE = (f"CC BY-SA 4.0 (https://github.com/mbforbes/social-chemistry-101/blob/{README_COMMIT}/README.md: "
           "'The dataset is licensed under the CC BY-SA 4.0 license.')")
REV = f"gcs-generation-1604370600946981 (zip sha256 {ZIP_SHA[:16]}...); README commit {README_COMMIT}"

Q_ACC = "Is the action being judged acceptable according to common social norms?"
Q_WRONG = "Is the action being judged wrong according to common social norms?"
Q_LEGAL = "Is this action against the law in most places?"

DEFS = {
    "acceptable": {
        "yes": "Most people would see the action being judged, as described, as okay, expected or good (annotators rated "
               "it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.",
        "no": "Most people would see the action being judged, as described, as bad or very bad: rude, unkind, "
              "dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.",
    },
    "wrong": {
        "yes": "Most people would see the action being judged, as described, as bad or very bad: rude, unkind, "
               "dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.",
        "no": "Most people would see the action being judged, as described, as okay, expected or good (annotators rated "
              "it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad.",
    },
    "legal": {
        "yes": "Doing the action is a crime or legal offence in most places (for example theft, assault, fraud, "
               "drunk driving, vandalism, hard-drug use), not merely rude or immoral.",
        "no": "The action is legal in most places, even if it is rude, unkind, dishonest or morally wrong (for "
              "example lying to a friend, cheating on a partner, breaking a promise).",
    },
}

ILLEGAL_RE = re.compile(
    r"\b(steal|steals|stealing|stole|stolen|shoplift\w*|rob|robs|robbing|robbed|robbery|burglar\w*|mugg\w*|"
    r"break(ing)? into|breaks into|murder\w*|assault\w*|rap(e|ing)|molest\w*|sexually (abus|exploit)\w*|child abuse|"
    r"drunk driving|driving (drunk|while drunk|under the influence|while intoxicated|while impaired|when you've been drinking|after drinking)|"
    r"drive drunk|drinking and (then )?driv\w*|hit and run|(driving away|leaving|fleeing) after hitting|hitting someone's car and leav\w*|"
    r"running red lights|running a red light|vandali\w*|arson|fraud\w*|defraud\w*|scam\w*|embezzl\w*|brib\w*|"
    r"blackmail\w*|extort\w*|kidnap\w*|trespass\w*|poach\w*|smuggl\w*|counterfeit\w*|identity theft|"
    r"forg(e|ing) (checks|documents|signatures|a signature|someone's signature)|tax evasion|evading taxes|"
    r"illegal\w*|underage drinking|sell(ing)? drugs|deal(ing)? drugs|drug dealing|(doing|taking) (illegal )?drugs|"
    r"(doing|using|taking|selling|buying|shooting) (heroin|cocaine|meth|crack)|heroin|cocaine|methamphetamine|"
    r"stalk\w*|animal cruelty|abusing animals|peeping into\w*|secretly film\w*|"
    r"abus\w* (your |a |their )?(child|children|kids|baby)|"
    r"(beat|beating|hit|hitting) (your |a |their )?(child|children|kids|baby|wife|husband|spouse|women|a woman|people|someone|others)|"
    r"stab\w*|strangl\w*|punch\w* (people|someone|others|a lot of people|strangers)|"
    r"shoot(ing)? (people|someone|police|up schools|up a school)|school shooter|"
    r"kill(ing)? (people|someone|a person|others|innocent\w*|another human being|another person)|"
    r"pirat(e|ing) (movies|software|music|games)|lying under oath|perjury|breaking the law|commit(ting)? (a )?crime\w*|"
    r"groom\w* children|sexual (acts|relations|relationships?) with (a )?(child|children|minor|minors)|"
    r"parking in a handicapped spot)\b", re.I)
# Reviewer fix: crime keywords that match but where the ACTION itself is not the crime (victim, idiom, bystander,
# acquittal, helping addicts, apologising, condoning, accidents, mental states, vague 'could hurt').
ILLEGAL_FP_RE = re.compile(
    r"\b(robbing the cradle|acquit\w*|being (mugged|robbed|stolen from|assaulted|molested|stalked|scammed|abused)|"
    r"helping (others|people|someone|addicts)|apologi\w*|condon\w*|could hurt or kill|"
    r"hitting someone with a car|hitting someone who is riding|feel you need to|being so desperate|"
    r"risk losing|living life like|children doing foolish|being considered|since that's illegal|"
    r"because it's illegal|wanting to have a clean record|so you aren't stopped|being involved with|"
    r"allowing your child|having to steal)\b", re.I)
RISKY_RE = re.compile(
    r"\b(drug\w*|weed|marijuana|pot|cannabis|alcohol\w*|drink\w*|drunk|beer|wine|gun\w*|weapon\w*|knife|knives|"
    r"driv\w*|speed\w*|car|cars|minor\w*|underage|teen\w*|sex\w*|porn\w*|hit|hitting|hurt\w*|harm\w*|fight\w*|punch\w*|"
    r"kill\w*|steal\w*|take|taking|took|tax\w*|police|cop|cops|law\w*|legal\w*|jail|prison|crime\w*|criminal\w*|"
    r"violen\w*|abus\w*|threat\w*|touch\w*|record\w*|film\w*|spy\w*|hack\w*|download\w*|money|pay\w*|work\w*|"
    r"job\w*|employ\w*|fire|firework\w*|smok\w*|vap\w*|pill\w*|medic\w*|animal\w*|dog\w*|cat|cats|pet|pets|hunt\w*|"
    r"fish\w*|trash|litter\w*|park\w*|trespass\w*|property|break\w*|damag\w*|destroy\w*|sell\w*|buy\w*)\b", re.I)


LEAD_SPLIT = re.compile(r"\b(if|when|whenever|unless|because|while|after|before|since|until|even|as long as|so that|just because)\b", re.I)


def neg_tag(action):
    """negation edge tag only when the main clause of the action is negated (e.g. 'not tipping ...',
    'never calling ...'), not for a negation inside a subordinate clause."""
    main = LEAD_SPLIT.split(action, maxsplit=1)[0]
    return bool(NEG_RE.search(main)) or bool(re.match(r"\s*(refus|fail|neglect)\w*", action, re.I))


# actions that are mental states / feelings rather than conduct (judged as 'acceptable conduct' they are ill-posed)
MENTAL_RE = re.compile(
    r"\s*((not|never|no longer)\s+)?(feel|feeling|want|wanting|like|liking|dislike|disliking|hate|hating|love|loving|"
    r"appreciat\w*|think|thinking|believ\w*|worry|worrying|care|caring about|know|knowing|fear|fearing|enjoy\w*|"
    r"wish\w*|hop(e|ing)|miss|missing|need|needing|prefer\w*|resent\w*|regret\w*|envy\w*|trust\w*|admir\w*|"
    r"being (upset|sad|happy|angry|mad|jealous|scared|afraid|nervous|excited|curious|proud|ashamed|embarrassed|lonely|"
    r"attracted|interested|worried|annoyed|frustrated|disappointed|hurt|bored|tired|confused|anxious|depressed))\b", re.I)


def clean_phrase(t):
    t = re.sub(r"\s+", " ", t).strip().rstrip(" .;,")
    return t[:1].upper() + t[1:] if t else t


def clean_sit(t):
    t = re.sub(r"\s+", " ", t).strip()
    return t


def ms_exclusion():
    path = fetch(MS_URL, CACHE / "_exclusion" / "moral_stories_full.jsonl", MS_SHA)
    norms = [json.loads(l)["norm"] for l in open(path)]
    idx = TokenSetIndex(norms)
    grams = set()
    for n_ in norms:
        w = toks(n_)
        for a in range(len(w)):
            for b in range(a + 3, min(len(w), a + 14) + 1):
                grams.add(" ".join(w[a:b]))
    return idx, grams


def main():
    rng = random.Random(SEED)
    zp = fetch(ZIP_URL, C / "social-chem-101.zip", ZIP_SHA)
    fetch(README_URL, C / "README_repo.md", README_SHA)
    tsv = C / "social-chem-101" / "social-chem-101.v1.0.tsv"
    if not tsv.exists():
        with zipfile.ZipFile(zp) as z:
            z.extract("social-chem-101/social-chem-101.v1.0.tsv", C)
    from common import sha256_file
    assert sha256_file(tsv) == TSV_SHA
    df = pd.read_csv(tsv, sep="\t", keep_default_na=False, dtype=str)

    tr = df[(df.split == "train") & (df.area != "amitheasshole") & (df["rot-bad"] == "0")].copy()
    ms_idx, ms_grams = ms_exclusion()
    stats = collections.Counter()
    keep = []
    for r in tr.to_dict("records"):
        rot, act = r["rot"], r["action"]
        if ms_idx.match(rot, thr=0.6):
            stats["drop_ms_rot"] += 1
            continue
        if act and " ".join(toks(act)) in ms_grams:
            stats["drop_ms_action"] += 1
            continue
        keep.append(r)
    print("train non-AITA:", len(tr), "after Moral Stories exclusion:", len(keep), dict(stats))

    used_rot, used_act = set(), set()

    # ---------------- legality (built first: it needs scarce 'illegal' items) ----------------
    ill, leg_bad, leg_ok = [], [], []
    for r in keep:
        a = r["action"]
        if not a or r["action-agency"] != "agency" or r["action-agree"] not in ("3", "4"):
            continue
        if len(toks(a)) < 2 or len(a) > 160:
            continue
        j = r["action-moral-judgment"]
        if r["action-legal"] == "illegal" and j in ("-1", "-2") and ILLEGAL_RE.search(a) and not ILLEGAL_FP_RE.search(a):
            ill.append(r)
        elif r["action-legal"] == "legal" and j != "" and not ILLEGAL_RE.search(a) and not RISKY_RE.search(a):
            (leg_bad if j in ("-1", "-2") else leg_ok).append(r)
    for pool in (ill, leg_bad, leg_ok):
        pool.sort(key=lambda r: r["rot-id"])
        rng.shuffle(pool)
    print("legality pools: illegal", len(ill), "legal&bad", len(leg_bad), "legal&ok", len(leg_ok))

    legal_rows = []
    nd_leg = NearDup(thr=0.6)

    def take(pool, n, gold, tag):
        got = 0
        for r in pool:
            if got >= n:
                break
            na = " ".join(toks(r["action"]))
            if r["rot-id"] in used_rot or na in used_act or nd_leg.seen(r["action"], add=False):
                continue
            nd_leg.seen(r["action"])
            used_rot.add(r["rot-id"])
            used_act.add(na)
            state = "Action: " + clean_phrase(r["action"]) + "."
            tags = []
            if neg_tag(r["action"]):
                tags.append("negation")
            if EXC_RE.search(r["action"]):
                tags.append("exception")
            legal_rows.append({
                "key": KEY, "rid": f"{r['rot-id']}::legal", "state": state, "instructions": Q_LEGAL,
                "options": ["yes", "no"], "gold": gold, "soft": None,
                "meta": {"dataset": "social-chem-101 (mbforbes/social-chemistry-101)", "config": "legality",
                         "revision": REV, "licence": LICENCE, "split": "train",
                         "orig_label": {"action-legal": r["action-legal"],
                                        "action-moral-judgment": int(r["action-moral-judgment"]),
                                        "action-agree": int(r["action-agree"]), "area": r["area"], "subset": tag},
                         "family": FAMILY, "edge": edge_join(tags), "defs": "legal"},
            })
            got += 1
        return got

    n_yes = take(ill, N_LEGAL // 2, "yes", "illegal")
    n_bad = take(leg_bad, round(n_yes * 0.6), "no", "legal_but_bad")
    take(leg_ok, n_yes - n_bad, "no", "legal_ok")

    # ---------------- acceptability ----------------
    cands = []
    for r in keep:
        a = r["action"]
        if (not a or r["action-agency"] != "agency" or r["action-moral-judgment"] == ""
                or r["action-agree"] not in ("3", "4") or r["rot-agree"] not in ("3", "4")
                or r["action-hypothetical"] not in ("explicit", "probable")
                or r["action-char-involved"] in ("", "char-none")):
            continue
        sit = clean_sit(r["situation"])
        if len(toks(a)) < 2 or len(a) > 200 or len(toks(sit)) < 3 or len(sit) > 1500:
            continue
        j = int(r["action-moral-judgment"])
        gold_acc = "yes" if j >= 0 else "no"
        if MENTAL_RE.match(a):
            continue
        cats = set(r["rot-categorization"].split("|")) - {""}
        if not (cats & {"morality-ethics", "social-norms"}) or "description" in cats:
            continue
        soft = None
        nuanced = bool(NEG_RE.search(a) or EXC_RE.search(a) or re.search(r"\b(if|when|while|before|after|instead|because|just|only|too)\b", a, re.I))
        cands.append((r, gold_acc, soft, nuanced))
    print("acceptability candidates:", len(cands), collections.Counter(c[1] for c in cands), dict(stats))

    cands.sort(key=lambda c: c[0]["rot-id"])
    rng.shuffle(cands)
    # nuanced first within each label, then the rest (each list keeps its shuffled order)
    by_gold = {g: [c for c in cands if c[1] == g and c[3]] + [c for c in cands if c[1] == g and not c[3]]
               for g in ("yes", "no")}
    per_sit = collections.Counter()
    sit_gold = collections.defaultdict(set)
    nd_acc = NearDup(thr=0.8)
    acc_rows = []
    ptr = {"yes": 0, "no": 0}
    target = {"yes": N_ACC // 2, "no": N_ACC - N_ACC // 2}
    got = {"yes": 0, "no": 0}
    while any(got[g] < target[g] and ptr[g] < len(by_gold[g]) for g in got):
        for g in ("no", "yes"):
            while got[g] < target[g] and ptr[g] < len(by_gold[g]):
                r, gold_acc, soft, nuanced = by_gold[g][ptr[g]]
                ptr[g] += 1
                sid = r["situation-short-id"]
                na = " ".join(toks(r["action"]))
                if r["rot-id"] in used_rot or na in used_act:
                    continue
                if per_sit[sid] >= 2 or (per_sit[sid] == 1 and gold_acc in sit_gold[sid]):
                    continue
                state = f"Situation: {clean_sit(r['situation'])}\nAction being judged: {clean_phrase(r['action'])}."
                if nd_acc.seen(state):
                    continue
                used_rot.add(r["rot-id"])
                used_act.add(na)
                per_sit[sid] += 1
                sit_gold[sid].add(gold_acc)
                negq = rng.random() < 0.30
                gold = gold_acc if not negq else ("no" if gold_acc == "yes" else "yes")
                s = None
                if soft is not None:
                    s = soft if not negq else {"yes": soft["no"], "no": soft["yes"]}
                tags = []
                if neg_tag(r["action"]):
                    tags.append("negation")
                if EXC_RE.search(r["action"]):
                    tags.append("exception")
                if len(state) > 600:
                    tags.append("long_context")
                acc_rows.append({
                    "key": KEY, "rid": f"{r['rot-id']}::{'wrong' if negq else 'acceptable'}", "state": state,
                    "instructions": Q_WRONG if negq else Q_ACC, "options": ["yes", "no"], "gold": gold, "soft": s,
                    "meta": {"dataset": "social-chem-101 (mbforbes/social-chemistry-101)", "config": "acceptability",
                             "revision": REV, "licence": LICENCE, "split": "train",
                             "orig_label": {"action-moral-judgment": int(r["action-moral-judgment"]),
                                            "action-agree": int(r["action-agree"]), "rot-agree": int(r["rot-agree"]),
                                            "action-hypothetical": r["action-hypothetical"], "area": r["area"],
                                            "rot": r["rot"]},
                             "family": FAMILY, "edge": edge_join(tags), "defs": "wrong" if negq else "acceptable"},
                })
                got[g] += 1
                break
    print("acceptability rows:", got, "situations with 2 rows:", sum(v == 2 for v in per_sit.values()))

    rows = acc_rows + legal_rows
    rng.shuffle(rows)
    write_rows(KEY, rows)
    for qid, d in DEFS.items():
        write_defs(f"{KEY}__{qid}", d)
    summary(rows)
    print("areas:", collections.Counter(r["meta"]["orig_label"]["area"] for r in rows))
    show(rows, 5, seed=SEED)
    append_manifest({
        "key": KEY, "family": FAMILY, "dataset": "Social-Chem-101 (mbforbes/social-chemistry-101)", "licence": LICENCE,
        "rows": len(rows), "qtype": "yesno", "yesno_share": yesno_share(rows), "edge_tags": edge_tags(rows),
        "notes": ("train split only; AITA area dropped (Scruples-derived); RoTs/actions matching Moral Stories norms "
                  "dropped; acceptability (consensus morality/social-norm RoTs, 30% negated question) + legality "
                  "(crime-keyword-verified illegal vs legal, 60% wrong-but-legal); no soft labels (single breakdown)."),
    })


if __name__ == "__main__":
    main()
