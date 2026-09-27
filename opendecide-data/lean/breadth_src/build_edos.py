"""Build raw rows for breadth set "edos" (EDOS, SemEval-2023 Task 10: Explainable Detection of Online Sexism).

Source : GitHub rewire-online/edos, pinned commit b1f1fbcc (raw snapshot saved in breadth_src/cache/edos/, sha256-checked):
           data/edos_labelled_aggregated.csv             (gold: label_sexist, label_category, label_vector, split)
           data/edos_labelled_individual_annotations.csv (3 trained annotators per post -> soft labels)
Licence: CC0 1.0 Universal (repo LICENSE file, cache/edos/LICENSE).
Texts  : human-written Gab and Reddit posts; labels by trained human annotators (disagreements adjudicated by experts).
Split  : split == 'train' only (dev and test rows are dropped). Never mft-moral / edos-sup derivatives.

Three label sets, one row per source post (no post used twice):
  - yesno  : "Is this post sexist?"                      yes / no           (Task A)
  - vector : fine-grained sexism type of a sexist post  11 options          (Task C)
  - category: broad sexism category of a sexist post     4 options           (Task B)
Soft labels: yesno = share of the 3 annotators who said sexist; vector/category = distribution over the annotators who
  said sexist (null when none of them did, i.e. the expert overruled all three).
Definitions follow Table 1 of Kirk et al. 2023 (arXiv 2303.04222); verifier tightened confusable pairs.
Filters: 15-4,000 chars; dedup on normalised text; exact and 12-word-run dedup against Social Bias Frames (all splits of
  allenai/social_bias_frames and BTZSC biasframes_* configs, i.e. the dev source); 13-gram + exact-state decontamination
  against our data/*.jsonl (never ohs*), other v13 raw parts and JevBench public. Deterministic, seed 20261101.

  python breadth_src/build_edos.py
"""
import collections
import glob
import hashlib
import html
import json
import random
import re
import statistics
import sys
import urllib.request
from pathlib import Path

import pandas as pd

SEED = 20261101
KEY = "edos"
REV = "b1f1fbcca9d42de0395432ada8fcfb5c35f68c77"
RAW = f"https://raw.githubusercontent.com/rewire-online/edos/{REV}/"
FILES = {"edos_labelled_aggregated.csv": "data/edos_labelled_aggregated.csv",
         "edos_labelled_individual_annotations.csv": "data/edos_labelled_individual_annotations.csv",
         "LICENSE": "LICENSE", "README.md": "README.md"}
SHA = {"edos_labelled_aggregated.csv": "607bdbb766e1803a28f0eb8fc21c14b6b9dfa20039f726ba6767438584b47f9b",
       "edos_labelled_individual_annotations.csv": "15d430d6756f620b2e83dddd7a3a68dc3e939df3a4c417d184e3c431cc0e20b2",
       "LICENSE": "a2010f343487d3f7618affe54f789f5487602331c0a8d03f49e9a7c547cf0499",
       "README.md": "1c6135761e05cb841c220786cb2f6410bdd39bafe07a9a3ddcfe4dd93d028299"}
LICENCE = "CC0 1.0 Universal (LICENSE file at the root of github.com/rewire-online/edos, commit b1f1fbcc)"
SBF = ("allenai/social_bias_frames", "453e07c6887c7420e7c62e3bbc1c03ceb4ab0f68",
       ["default/train/0000.parquet", "default/validation/0000.parquet", "default/test/0000.parquet"], "post")
BTZSC = ("btzsc/btzsc", "fef2a2ac62b69c58670047dddf045c53d7c3cb5e",
         [f"{c}/test-00000-of-00001.parquet" for c in ("biasframes_offensive", "biasframes_intent", "biasframes_sex")],
         "text")

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
CACHE = HERE / "cache" / KEY
OUT = LEAN / "data/v13_parts/raw" / f"{KEY}.jsonl"
DEFS = LEAN / "data/v13_parts/defs" / f"{KEY}.json"
JB = LEAN.parents[1] / "bench/jevbench/datasets/public"

MAX_ROWS = 700
N_VECTOR = 330
N_CATEGORY = 90
N_YESNO = MAX_ROWS - N_VECTOR - N_CATEGORY   # 280 (140 yes / 140 no)

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
V_OPTS = list(VECTOR.values())
C_OPTS = list(CATEGORY.values())
Q_YESNO = "Is this post sexist?"
Q_VECTOR = "This post is sexist. Which specific type of sexism does it show?"
Q_CATEGORY = "This post is sexist. Which broad category of sexism does it fall under?"

DEF = {
    "yes": "The post is sexist: it contains abuse or negative sentiment directed at women because of their gender, or their gender combined with another identity such as race, religion or being trans.",
    "no": "The post is not sexist: it may be rude, offensive, about gender, or abusive toward other groups or men, but it shows no abuse or prejudice against women because of their gender.",
    "threats of harm": "The author states an intent, willingness or wish to harm a woman or women, whether physically, sexually, emotionally or by violating their privacy.",
    "incitement and encouragement of harm": "The post urges or encourages others to harm a woman or women, or argues that harming women is justified; it calls for or endorses harm rather than only insulting women.",
    "descriptive attacks": "The post openly describes women in a derogatory way, for example negative generalisations about their abilities, intellect, character, morals, appearance or sexual behaviour.",
    "aggressive and emotive attacks": "The post expresses strong negative emotion such as hatred or disgust toward women, for example through the author's stated feelings, baseless accusations, or gendered slurs used to attack women.",
    "dehumanising attacks and sexual objectification": "The post compares women to animals, objects, vermin or refuse, or reduces them to sexual objects valued only for sex or their bodies.",
    "casual use of gendered slurs, profanities and insults": "The post uses a slur or insult that traditionally describes women, such as bitch or slut, casually and not to deliberately attack women, often even aimed at a man.",
    "immutable gender differences and stereotypes": "The post asserts natural, essential or unchangeable differences between men and women or uses gender stereotypes, including using women's traits to mock men; most sexist jokes fall here.",
    "backhanded gendered compliments": "The post seems to praise women but actually belittles them, for example implying they are weak, need protection or matter only for their looks.",
    "condescending explanations or unwelcome advice": "The post gives women patronising or unsolicited advice or explanations on matters they know more about ('mansplaining'), implying they cannot understand or judge for themselves.",
    "supporting mistreatment of individual women": "The post supports mistreatment of a particular woman or women by denying, understating or justifying it, for example blaming a victim of abuse or harassment.",
    "supporting systemic discrimination against women": "The post supports discrimination against women as a group by denying, understating or justifying it, for example denying that sexism exists or opposing women's rights.",
    "threats and incitement to harm": "The post threatens women or states plans to harm them, or incites and encourages others to inflict serious harm or violence on women.",
    "derogation": "The post explicitly demeans women: derogatory descriptions, aggressive or emotive attacks, dehumanising comparisons or overt sexual objectification.",
    "animosity": "The post shows implicit or subtle sexism: casual gendered slurs, stereotypes or claims of innate gender differences, backhanded compliments, or condescending advice.",
    "prejudiced discussion": "The post denies or justifies sexist treatment: supporting mistreatment of individual women, or denying or justifying discrimination against women as a group, including male-victimhood arguments.",
}


def fetch():
    CACHE.mkdir(parents=True, exist_ok=True)
    for name, path in FILES.items():
        p = CACHE / name
        if not p.exists():
            urllib.request.urlretrieve(RAW + path, p)
        got = hashlib.sha256(p.read_bytes()).hexdigest()
        if got != SHA[name]:
            sys.exit(f"sha256 mismatch for {p}: {got}")


def words(t):
    t = html.unescape(t).lower()
    t = re.sub(r"\[(user|url)\]|@\w+|https?://\S+|\brt\b", " ", t)
    return re.findall(r"[a-z0-9']+", t)


def norm(t):
    return " ".join(words(t))


def sbf_texts():
    from huggingface_hub import hf_hub_download
    out = []
    for repo, rev, paths, col in (SBF, BTZSC):
        for p in paths:
            f = hf_hub_download(repo, p, repo_type="dataset", revision=rev)
            out += pd.read_parquet(f, columns=[col])[col].astype(str).tolist()
    return set(out)


def overlap(recs, texts, n):
    """Norm keys of recs that equal, or share an n-word run with, any text in `texts`."""
    grams = collections.defaultdict(set)
    for k in recs:
        w = k.split()
        for i in range(len(w) - n + 1):
            grams[" ".join(w[i:i + n])].add(k)
    hit = set()
    for t in texts:
        ks = norm(t)
        if ks in recs:
            hit.add(ks)
        w = ks.split()
        for i in range(len(w) - n + 1):
            g = " ".join(w[i:i + n])
            if g in grams:
                hit |= grams[g]
    return hit


def our_texts():
    files = [f for f in glob.glob(str(LEAN / "data" / "*.jsonl")) if not Path(f).name.startswith("ohs")]
    files += [f for f in glob.glob(str(LEAN / "data/v13_parts/raw/*.jsonl")) if Path(f).stem != KEY]
    files += glob.glob(str(JB / "*.jsonl"))
    for f in files:
        for line in open(f, encoding="utf-8"):
            try:
                r = json.loads(line)
            except Exception:
                continue
            st = r.get("state") if isinstance(r, dict) else None
            yield st if isinstance(st, str) else line.replace("\\n", " ")


def dist(votes, opts):
    c = collections.Counter(v for v in votes if v in opts)
    n = sum(c.values())
    return {o: round(c[o] / n, 4) for o in opts} if n else None


def main():
    fetch()
    rng = random.Random(SEED)
    agg = pd.read_csv(CACHE / "edos_labelled_aggregated.csv", dtype=str, keep_default_na=False)
    ind = pd.read_csv(CACHE / "edos_labelled_individual_annotations.csv", dtype=str, keep_default_na=False)
    agg = agg[agg["split"] == "train"]
    ind = ind[ind["split"] == "train"]
    ann = {rid: g for rid, g in ind.groupby("rewire_id")}

    drop = collections.Counter()
    recs, dup = {}, set()
    for r in agg.itertuples(index=False):
        t = r.text
        if not (15 <= len(t.strip()) <= 4000) or len(words(t)) < 3:
            drop["length"] += 1
            continue
        k = norm(t)
        if k in recs or k in dup:
            dup.add(k)
            recs.pop(k, None)
            drop["duplicate text"] += 1
            continue
        recs[k] = r
    n_elig = len(recs)

    hit_sbf = overlap(recs, sbf_texts(), 12)
    for k in hit_sbf:
        recs.pop(k)
    hit_ours = overlap(recs, our_texts(), 13)
    for k in hit_ours:
        recs.pop(k)
    drop["social bias frames overlap"] = len(hit_sbf)
    drop["13-gram overlap with our files"] = len(hit_ours)

    def row(r, qtype, instr, opts, gold, soft):
        g = ann[r.rewire_id]
        return {"key": KEY, "rid": r.rewire_id, "state": r.text, "instructions": instr, "options": opts,
                "gold": gold, "soft": soft,
                "meta": {"dataset": "rewire-online/edos (SemEval-2023 Task 10)", "config": "edos_labelled_aggregated.csv",
                         "revision": REV, "licence": LICENCE, "split": "train", "qtype": qtype,
                         "orig_label": {"label_sexist": r.label_sexist, "label_category": r.label_category,
                                        "label_vector": r.label_vector},
                         "annotator_labels": sorted(zip(g["label_sexist"], g["label_vector"]))}}

    keys = sorted(recs)
    rng.shuffle(keys)
    sexist = [k for k in keys if recs[k].label_sexist == "sexist"]
    notsex = [k for k in keys if recs[k].label_sexist == "not sexist"]

    def round_robin(pool, lab, n):
        by = collections.defaultdict(list)
        for k in pool:
            by[lab(k)].append(k)
        labs = sorted(by)
        out, i = [], 0
        while len(out) < n and any(by[l] for l in labs):
            l = labs[i % len(labs)]
            if by[l]:
                out.append(by[l].pop(0))
            i += 1
        return out

    rows = []
    v_keys = round_robin(sexist, lambda k: recs[k].label_vector, N_VECTOR)
    for k in v_keys:
        r = recs[k]
        rows.append(row(r, "choice", Q_VECTOR, V_OPTS, VECTOR[r.label_vector],
                        dist([VECTOR.get(v) for v in ann[r.rewire_id]["label_vector"]], V_OPTS)))
    used = set(v_keys)
    c_keys = round_robin([k for k in sexist if k not in used], lambda k: recs[k].label_category, N_CATEGORY)
    for k in c_keys:
        r = recs[k]
        rows.append(row(r, "choice", Q_CATEGORY, C_OPTS, CATEGORY[r.label_category],
                        dist([CATEGORY.get(v) for v in ann[r.rewire_id]["label_category"]], C_OPTS)))
    used |= set(c_keys)
    y_keys = round_robin([k for k in sexist if k not in used] + notsex, lambda k: recs[k].label_sexist, N_YESNO)
    for k in y_keys:
        r = recs[k]
        votes = ["yes" if v == "sexist" else "no" for v in ann[r.rewire_id]["label_sexist"]]
        rows.append(row(r, "yesno", Q_YESNO, ["yes", "no"], "yes" if r.label_sexist == "sexist" else "no",
                        dist(votes, ["yes", "no"])))
    rng.shuffle(rows)
    assert len({r["rid"] for r in rows}) == len(rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    DEFS.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    used_opts = ["yes", "no"] + V_OPTS + C_OPTS
    assert set(DEF) == set(used_opts)
    for o, d in DEF.items():
        assert 8 <= len(d.split()) <= 35, (o, len(d.split()))
    with open(DEFS, "w", encoding="utf-8") as f:
        json.dump({o: DEF[o] for o in used_opts}, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"train posts {len(agg)}; eligible after length/dedup {n_elig}; drops {dict(drop)}; final pool {len(recs)}")
    print(f"wrote {len(rows)} rows -> {OUT}")
    for q in (Q_YESNO, Q_VECTOR, Q_CATEGORY):
        sub = [r for r in rows if r["instructions"] == q]
        cnt = collections.Counter(r["gold"] for r in sub)
        soft = [r for r in sub if r["soft"]]
        agree = sum(max(r["soft"], key=r["soft"].get) == r["gold"] for r in soft)
        print(f"\n[{q}] n={len(sub)} soft={len(soft)}/{len(sub)} soft-argmax==gold {agree}/{len(soft)}")
        for g, c in cnt.most_common():
            print(f"  {c:4d} ({c / len(sub):.1%})  {g}")
    lens = [len(r["state"]) for r in rows]
    print(f"\nlength chars: min={min(lens)} median={int(statistics.median(lens))} mean={statistics.mean(lens):.0f} "
          f"max={max(lens)}")


if __name__ == "__main__":
    main()
