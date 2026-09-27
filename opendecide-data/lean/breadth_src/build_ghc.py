"""v0.13 breadth corpus: raw rows for "ghc" (Gab Hate Corpus, Kennedy et al., 2022, Language Resources & Evaluation).

Source : OSF project edua3 ("The Gab Hate Corpus"), Data folder:
           ghc_train.tsv                  (https://osf.io/download/x5pdg/, sha256 c82a2733...)  -> gold hd/cv/vo
           GabHateCorpus_annotations.tsv  (https://osf.io/download/wuecz/, sha256 70b1b065...)  -> per-annotator codes
         ghc_test.tsv is NEVER downloaded or read. The annotations file covers train + test posts; it is joined on the
         exact post text of ghc_train.tsv, so only train posts are used. A train text is dropped when it occurs more
         than once in ghc_train.tsv or maps to more than one annotation ID (a second ID could be a test copy).
Licence: CC BY 4.0, the OSF node licence of edua3 ("CC-By Attribution 4.0 International", OSF API
         /v2/nodes/edua3/ -> license 563c1cf88c5e4a3877f9e96a; shown on https://osf.io/edua3/).
Provenance: Gab posts (human-written, 2016-2018, Pushshift Gab dump); labels by trained human annotators
         (>= 3 per post) following the project's coding manual (GabHateCorpus_trainingmanual.pdf, kept in cache).
Labels : HD = assault on human dignity, CV = call for violence, VO = vulgarity/offensive language; train gold =
         annotator mean >= 0.5 (verified; the 2 rows that disagree with the annotations are dropped).
         Target types (REL, RAE, SXO, GEN, IDL, NAT, POL, MPH) are coded only by annotators who marked the post hateful.
Row types (each post used at most once):
  * yes/no HD, CV, VO questions; half of each "no" side is a near miss (VO-but-not-HD for HD; HD-but-not-CV for CV;
    HD-but-not-VO for VO), the other half any other post. Soft = annotator share {yes: p, no: 1-p}.
  * choice "which type of group is targeted" for posts whose gold is HD or CV; gold = the target type marked by the
    most hateful-coding annotators, only when that count is >= 2, >= half of those annotators and strictly highest.
    Soft = share of target marks per type (annotators may mark several types).
Decontamination (drop, never edit): exact normalised text and 12-word runs vs Social Bias Frames (all splits, contains
  Gab posts; used as dev via BTZSC biasframes), the BTZSC biasframes_* dev files and HateXplain (all splits; Gab posts;
  part of forbidden tasksource mbib-base) - these files are read only to drop overlaps; 13-word runs vs every
  non-held-out jsonl we have (as build_fm2.py); exact text and 10-word runs vs the whole forbidden
  tasksource/zero-shot-label-nli (all splits/tasks; its implicit-hate-stg1 holds Gab posts) and
  ucberkeley-dlab/measuring-hate-speech (both from the local HF cache, pinned revisions). Held-out item files (ohs*, preds_*, results_*) are never opened.
Deterministic (seed 20261101).

  ../.venv/bin/python breadth_src/build_ghc.py
"""
import hashlib
import json
import random
import re
import statistics
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent            # lean/breadth_src
LEAN = HERE.parent
ROOT = LEAN.parent                                # opendecide-data
JEV = ROOT.parent
CACHE = HERE / "cache" / "ghc"
OUT_RAW = LEAN / "data" / "v13_parts" / "raw" / "ghc.jsonl"
OUT_DEFS = LEAN / "data" / "v13_parts" / "defs" / "ghc.json"

KEY = "ghc"
SEED = 20261101
MAX_ROWS = 650
LEN_RANGE = (15, 4000)
GRAM = 13
DEDUP_RUN = 12

SRC = {  # file -> (url, sha256); train + annotations only
    "ghc_train.tsv": ("https://osf.io/download/x5pdg/",
                      "c82a27336560d3a6822a4cc3f92856481af5fd63aa2ce8d0ca644d440d351d43"),
    "GabHateCorpus_annotations.tsv": ("https://osf.io/download/wuecz/",
                                      "70b1b0657a1d715a06ff026395afee8e99f05c4ccc166ff577870260b07aa779"),
    "GabHateCorpus_trainingmanual.pdf": ("https://osf.io/download/nqt6h/",
                                         "af0ee38a2117c2fa51bcd283c647aaece2aa66678b94f2668e6e26aab33a2070"),
}
DEDUP = {  # read only to drop overlapping posts
    "sbic_train.parquet": "657502c7eae01ddc35ebce019cac5ce0f901ebc619e30041669548e39c14fcc6",
    "sbic_validation.parquet": "167b911b761af65dae4403527d08787145ced80bc40e4a009cc7fe14c8da55d5",
    "sbic_test.parquet": "86061dee400c129b75710d644923173524abc3f2314c1d77511b23d4c9a7a0bb",
    "hatexplain_train.parquet": "820abc7acd0019d2034056202b22a243a566b1645b71995ca5a8741cd8c148c1",
    "hatexplain_validation.parquet": "6ad2463d67207b98b3c9b23ee2199dfe5faeee350ae10a0ac00c8441b62cf2c8",
    "hatexplain_test.parquet": "de4071c91efcf3a5682fd79d796a2fa758723a37ecacd9c0d14172b793f41958",
    "btzsc_biasframes_intent.parquet": "82a6da7eff047ac43fde1fdcc1d9b1b986cde08718d324f04af901607f585941",
    "btzsc_biasframes_offensive.parquet": "5b4df757e7241d8fd5456fe04545eea2bfc171b9462069ea369991c9b4cef10e",
    "btzsc_biasframes_sex.parquet": "7cb2a305f07378708941d792d858577eb552faded64958d91b6da3d7360c5057",
}
DEDUP_ORIGIN = ("allenai/social_bias_frames@453e07c6887c7420e7c62e3bbc1c03ceb4ab0f68 (refs/convert/parquet); "
                "Hate-speech-CNERG/hatexplain@b0e5676acc1d0dcb31d6ce8e93e7e94109044ed6 (refs/convert/parquet); "
                "btzsc/btzsc@fef2a2ac62b69c58670047dddf045c53d7c3cb5e biasframes_*")

HF_HUB = Path.home() / ".cache" / "huggingface" / "hub"
BIG_DEDUP = [  # (snapshot dir, text column): forbidden aggregates read only to drop overlapping posts
    (HF_HUB / "datasets--tasksource--zero-shot-label-nli/snapshots/ee693dba923b5d5484aa9232b7357c5e45dd39b8/data",
     "premise"),   # all splits, all tasks (implicit-hate-stg1 contains Gab posts; mbib-base/*, dynahate, ...)
    (HF_HUB / "datasets--ucberkeley-dlab--measuring-hate-speech/snapshots/5468f6e118396646b02a2f691e771f6b6d9502ea/data",
     "text"),      # 'avoid to be safe' in used_sources.json
]
BIG_RUN = 10

DATASET = "Gab Hate Corpus (OSF edua3)"
REVISION = f"osf:edua3 ghc_train.tsv sha256:{SRC['ghc_train.tsv'][1]}; annotations sha256:" \
           f"{SRC['GabHateCorpus_annotations.tsv'][1]}"
LICENCE = ("CC BY 4.0 (OSF node licence of https://osf.io/edua3/ 'CC-By Attribution 4.0 International', "
           "OSF API license id 563c1cf88c5e4a3877f9e96a; Kennedy et al., The Gab Hate Corpus)")

YN = ["yes", "no"]
Q = {  # wording follows the coding manual (section 4): HD and CV need group identity; CV covers exclusion/segregation
    "hd": "Does this post assault the human dignity of people because of a group they belong to?",
    "cv": "Does this post call for or endorse violence, expulsion, exclusion or segregation against people because of a "
          "group they belong to?",
    "vo": "Does this post use vulgar, offensive or abusive language?",
    "target": "Which type of group does this post's hateful rhetoric mainly target?",
}
TARGETS = {  # code -> option name (coding manual, 'Targeted Populations')
    "RAE": "race or ethnicity",
    "NAT": "nationality or region",
    "GEN": "gender",
    "REL": "religion",
    "SXO": "sexual orientation",
    "IDL": "ideology",
    "POL": "political affiliation",
    "MPH": "health or disability",
}
TOPTS = list(TARGETS.values())
QUOTA = {"cv": 200, "target": 170, "hd": 150, "vo": 130}   # sums to 650; CV first (rarest)

DEFS = {  # from GabHateCorpus_trainingmanual.pdf, section 4 ("Coding Manual/Procedure", "Targeted Populations")
    "yes": "The post meets the category the question names, as the Gab Hate Corpus coding manual defines it. Assault on "
           "human dignity: it degrades a group, or a person because of their group, by asserting or implying "
           "inferiority, comparing them to animals or subhumans, using slurs meant to wound, spreading hateful "
           "stereotypes, or supporting hateful ideology such as white supremacy. Call for violence: it advocates or "
           "endorses violence, genocide, expulsion, exclusion or segregation against a group, or a person because of "
           "their group. Vulgar or offensive language: it uses vulgar, derogatory or abusive wording or personal "
           "insults, whether or not the post is hateful.",
    "no": "The post does not meet the category the question names under the coding manual. Insults or threats aimed "
          "at a person without invoking their group are neither an assault on dignity nor a call for violence; "
          "degrading a group without advocating aggression, expulsion or exclusion is not a call for violence; hateful "
          "or political views stated without vulgar, profane or abusive wording are not vulgar language; criticism of "
          "policies, parties or ideas that does not degrade people is none of these.",
    "race or ethnicity": "The hateful rhetoric mainly targets people for their race or ethnicity, for example "
                         "anti-Black, anti-Asian, anti-Latino, anti-Arab or antisemitic attacks on Jews as a people "
                         "(the manual codes antisemitism here).",
    "nationality or region": "The hateful rhetoric mainly targets people for their nationality, country or region of "
                             "origin, including general xenophobia, attacks on immigrants as foreigners, or on named "
                             "countries or regions.",
    "gender": "The hateful rhetoric mainly targets people for their gender or gender identity, for example anti-woman, "
              "anti-man or anti-trans attacks.",
    "religion": "The hateful rhetoric mainly targets people for their religion or spiritual beliefs, for example "
                "anti-Muslim or anti-Christian attacks on believers or the faith.",
    "sexual orientation": "The hateful rhetoric mainly targets people for their sexual orientation, for example gay, "
                          "lesbian or bisexual people.",
    "ideology": "The hateful rhetoric mainly targets people for their ideology or worldview, such as liberals, "
                "leftists, conservatives or the right wing as a camp of believers, not as members of a party.",
    "political affiliation": "The hateful rhetoric mainly targets people for membership of a political organisation "
                             "or party, such as Democrats or Republicans, or a named party's members or politicians.",
    "health or disability": "The hateful rhetoric mainly targets people for their mental or physical health status, "
                            "mental illness or a physical disability.",
}

words = lambda t: re.sub(r"[\W_]+", " ", t.casefold()).split()
norm = lambda t: " ".join(words(t))
URL = re.compile(r"https?://\S+|www\.\S+")
DANGLING = {"the", "of", "a", "an", "to", "and", "in", "for", "with", "their", "his", "her", "on", "at", "by", "from",
            "or", "your", "my", "our", "ur"}


def cut_off(t):
    """Post looks cut off by the source: ends on a dangling function word or a clipped @mention."""
    t = t.rstrip()
    if re.search(r"(^|\s)@\w{0,2}$", t):
        return True
    w = re.findall(r"[A-Za-z']+|\S", t)
    return bool(w) and w[-1].lower() in DANGLING


def grams(w, n):
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_src():
    CACHE.mkdir(parents=True, exist_ok=True)
    for f, (url, h) in SRC.items():
        p = CACHE / f
        if not p.exists():
            urllib.request.urlretrieve(url, p)
        assert sha(p) == h, f"sha256 mismatch {p}"
    for f, h in DEDUP.items():
        p = CACHE / "dedup" / f
        assert p.exists() and sha(p) == h, f"missing/changed dedup snapshot {p} (from {DEDUP_ORIGIN})"
    tr = pd.read_csv(CACHE / "ghc_train.tsv", sep="\t", dtype={"text": str}, keep_default_na=False)
    an = pd.read_csv(CACHE / "GabHateCorpus_annotations.tsv", sep="\t", dtype={"Text": str}, keep_default_na=False,
                     na_values={c: [""] for c in ["Hate", "HD", "CV", "VO", *TARGETS, "EX", "IM"]})
    return tr, an


def dedup_texts():
    out = []
    for f in DEDUP:
        d = pd.read_parquet(CACHE / "dedup" / f)
        if f.startswith("sbic"):
            out += d["post"].astype(str).tolist()
        elif f.startswith("hatexplain"):
            out += [" ".join(t) for t in d["post_tokens"]]
        else:
            out += d["text"].astype(str).tolist()
    return out


def big_dedup(posts):
    """Exact normalised text or any shared 10-word run vs BIG_DEDUP texts; returns rids to drop."""
    owner, exact = defaultdict(set), defaultdict(set)
    for p in posts:
        w = words(p["text"])
        exact[" ".join(w)].add(p["rid"])
        for g in grams(w, BIG_RUN):
            owner[g].add(p["rid"])
    hit = set()
    for d, col in BIG_DEDUP:
        fs = sorted(d.glob("*.parquet"))
        assert fs, f"missing dedup snapshot {d}"
        for f in fs:
            for t in set(pd.read_parquet(f, columns=[col])[col].astype(str)):
                w = words(t)
                hit |= exact.get(" ".join(w), set())
                for i in range(len(w) - BIG_RUN + 1):
                    hit |= owner.get(" ".join(w[i:i + BIG_RUN]), set())
    return hit


def is_heldout(p: Path) -> bool:
    parts = [x.lower() for x in p.parts]
    return any(x.startswith(("ohs", "preds", "results")) for x in parts)


def scan_files():
    fs = set()
    for base in (LEAN, ROOT / "data"):
        for p in base.rglob("*.jsonl"):
            rel = p.relative_to(base)
            if is_heldout(rel) or "cache" in rel.parts or ".venv" in rel.parts or p.resolve() == OUT_RAW.resolve():
                continue
            fs.add(p)
    fs |= set((JEV / "bench/jevbench/datasets/public").glob("*.jsonl"))
    return sorted(fs)


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


def decontaminate(posts):
    """13-word runs of our posts vs every non-held-out jsonl; returns {rid: first hit file}."""
    owner = defaultdict(set)
    exact = {}
    for p in posts:
        w = words(p["text"])
        exact.setdefault(" ".join(w), set()).add(p["rid"])
        for g in grams(w, GRAM):
            owner[g].add(p["rid"])
    hit, seen, nfiles = {}, set(), 0
    for f in scan_files():
        nfiles += 1
        with open(f, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    x = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                for t in strings(x):
                    if len(t) < 15:
                        continue
                    h = hash(t)
                    if h in seen:
                        continue
                    seen.add(h)
                    w = words(t)
                    for rid in exact.get(" ".join(w), ()):
                        hit.setdefault(rid, str(f))
                    for i in range(len(w) - GRAM + 1):
                        for rid in owner.get(" ".join(w[i:i + GRAM]), ()):
                            hit.setdefault(rid, str(f))
    return hit, nfiles


def build_posts(tr, an):
    drop = Counter()
    occ = Counter(tr["text"])
    ids_of = an.groupby("Text")["ID"].agg(lambda s: sorted(set(s))).to_dict()
    by_id = {i: g for i, g in an.groupby("ID")}
    posts, seen_norm = [], set()
    for r in tr.itertuples(index=False):
        text = r.text
        if occ[text] > 1:
            drop["text repeated in train"] += 1
            continue
        ids = ids_of.get(text, [])
        if len(ids) != 1:
            drop["text has 0 or >1 annotation IDs (possible test copy)"] += 1
            continue
        if not (LEN_RANGE[0] <= len(text.strip()) <= LEN_RANGE[1]):
            drop["length"] += 1
            continue
        if cut_off(text):
            drop["text cut off at the end"] += 1
            continue
        n = norm(text)
        if len(words(URL.sub(" ", text))) < 3 or n in seen_norm:
            drop["fewer than 3 non-URL words / duplicate normalised text"] += 1
            continue
        seen_norm.add(n)
        g = by_id[ids[0]]
        p = {"rid": str(ids[0]), "text": text, "n_ann": len(g)}
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
        posts.append(p)
    return posts, drop


def target_gold(p):
    if not (p["hd"] or p["cv"]):
        return None
    cnt = sorted(p["tcount"].items(), key=lambda kv: -kv[1])
    (k1, c1), (_, c2) = cnt[0], cnt[1]
    if c1 >= 2 and c1 >= p["n_hate"] / 2 and c1 > c2:
        return k1
    return None


def clarity(p, c):  # 0 = unanimous, larger = less clear; ties (0.5) last
    m = p[c + "_p"]
    return abs(m - (1.0 if p[c] else 0.0))


def main():
    tr, an = load_src()
    posts, drop = build_posts(tr, an)
    n0 = len(posts)

    # dedup vs SBIC / BTZSC biasframes / HateXplain: exact normalised text or any shared 12-word run
    ref = dedup_texts()
    ref_exact = {norm(t) for t in ref}
    ref_runs = set()
    for t in ref:
        ref_runs |= grams(words(t), DEDUP_RUN)
    keep = []
    for p in posts:
        w = words(p["text"])
        if " ".join(w) in ref_exact or any(g in ref_runs for g in grams(w, DEDUP_RUN)):
            drop["overlap SBIC/biasframes/HateXplain"] += 1
        else:
            keep.append(p)
    posts = keep

    big = big_dedup(posts)
    drop["overlap label-NLI (tasksource zero-shot-label-nli) / measuring-hate-speech"] = len(big)
    posts = [p for p in posts if p["rid"] not in big]

    hit, nfiles = decontaminate(posts)
    drop["13-gram/exact overlap with our files"] = sum(1 for p in posts if p["rid"] in hit)
    posts = [p for p in posts if p["rid"] not in hit]

    rng = random.Random(SEED)
    posts.sort(key=lambda p: int(p["rid"]))
    rng.shuffle(posts)
    order = {p["rid"]: i for i, p in enumerate(posts)}

    used, used_runs, rows = set(), set(), []

    def take(pool, n, key_fn=None):
        """Take up to n unused posts from pool (clearest first, then seeded order); no shared 12-word runs."""
        pool = sorted(pool, key=lambda p: ((key_fn(p) if key_fn else 0), order[p["rid"]]))
        got = []
        for p in pool:
            if len(got) >= n:
                break
            if p["rid"] in used:
                continue
            g = grams(words(p["text"]), DEDUP_RUN)
            if g & used_runs:
                continue
            used.add(p["rid"])
            used_runs.update(g)
            got.append(p)
        return got

    def yn_row(p, c):
        gold = "yes" if p[c] else "no"
        m = round(p[c + "_p"], 4)
        return mk(p, Q[c], list(YN), gold, {"yes": m, "no": round(1 - m, 4)}, c,
                  {c: p[c], "annotator_mean": m})

    def mk(p, q, opts, gold, soft, task, orig):
        orig = dict(orig, n_annotators=p["n_ann"])
        return {"key": KEY, "rid": p["rid"], "state": p["text"], "instructions": q, "options": opts, "gold": gold,
                "soft": soft,
                "meta": {"dataset": DATASET, "config": f"ghc_train.tsv+annotations:{task}", "revision": REVISION,
                         "licence": LICENCE, "split": "train", "orig_label": orig}}

    near = {"cv": lambda p: p["hd"] and not p["cv"], "hd": lambda p: p["vo"] and not p["hd"],
            "vo": lambda p: p["hd"] and not p["vo"]}
    for task in ("cv", "target", "hd", "vo"):
        n = QUOTA[task]
        if task == "target":
            pools = defaultdict(list)
            for p in posts:
                t = target_gold(p)
                if t:
                    pools[t].append(p)
            pools = {k: take(v, n, lambda p: -p["tcount"][target_gold(p)] / max(p["n_hate"], 1))
                     for k, v in pools.items()}
            got, i = [], 0
            codes = sorted(pools)
            while len(got) < n and any(i < len(pools[k]) for k in codes):
                for k in codes:
                    if i < len(pools[k]) and len(got) < n:
                        got.append(pools[k][i])
                i += 1
            for k in codes:  # release posts not used by the round-robin
                for p in pools[k]:
                    if p not in got:
                        used.discard(p["rid"])
                        used_runs.difference_update(grams(words(p["text"]), DEDUP_RUN))
            for p in got:
                k = target_gold(p)
                tot = sum(p["tcount"].values())
                soft = {TARGETS[c]: round(p["tcount"][c] / tot, 4) for c in TARGETS}
                soft[TARGETS[k]] = round(soft[TARGETS[k]] + 1 - sum(soft.values()), 4)  # rounding residue -> gold
                rows.append(mk(p, Q["target"], list(TOPTS), TARGETS[k], soft, "target",
                               {"target_code": k, "target_marks": p["tcount"], "n_hateful_coders": p["n_hate"],
                                "hd": p["hd"], "cv": p["cv"]}))
            continue
        pos = take([p for p in posts if p[task]], n // 2, lambda p: clarity(p, task))
        k_neg = n - len(pos)
        neg = take([p for p in posts if near[task](p)], k_neg // 2, lambda p: clarity(p, task))
        neg += take([p for p in posts if not p[task]], k_neg - len(neg), lambda p: clarity(p, task))
        rows += [yn_row(p, task) for p in pos + neg]

    rng.shuffle(rows)
    OUT_RAW.parent.mkdir(parents=True, exist_ok=True)
    OUT_DEFS.parent.mkdir(parents=True, exist_ok=True)
    OUT_RAW.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    OUT_DEFS.write_text(json.dumps(DEFS, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"train rows {len(tr)}; clean posts {n0}; after decontam {len(posts)}; drops {dict(drop)}")
    print(f"decontam: scanned {nfiles} files; hit files {Counter(hit.values()).most_common(5)}")
    print(f"wrote {len(rows)} rows -> {OUT_RAW}")
    print("by task", dict(Counter(r["meta"]["config"].split(":")[1] for r in rows)))
    print("gold overall", dict(Counter(r["gold"] for r in rows)))
    for t in ("hd", "cv", "vo", "target"):
        rs = [r for r in rows if r["meta"]["config"].endswith(":" + t)]
        print(f"  {t}: {dict(Counter(r['gold'] for r in rs))}")
    top = max(Counter(r["gold"] for r in rows).values()) / len(rows)
    print(f"max label share {top:.1%}; soft coverage {sum(r['soft'] is not None for r in rows)}/{len(rows)}; "
          f"soft p(gold)<0.5: {sum(r['soft'][r['gold']] < 0.5 for r in rows)}")
    L = [len(r["state"]) for r in rows]
    print(f"length chars min {min(L)} median {statistics.median(L)} mean {statistics.mean(L):.0f} max {max(L)}")
    assert len({r["rid"] for r in rows}) == len(rows)


if __name__ == "__main__":
    main()
