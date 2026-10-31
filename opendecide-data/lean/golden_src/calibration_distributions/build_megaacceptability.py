"""REJECTED in review (29 Sep 2026); main() refuses to run and no raw/defs files exist for this key.
Reason: the raw MTurk ratings of these bleached sentences are too lenient for a gold "acceptable" label. In a review
sample 3 of 15 gold-yes rows were plainly ungrammatical ("Someone questions someone that something happened.",
"Someone was being excited whether to do something."), and even the strictest fix tried (all raters 5-7 AND
participant-z-normalised mean >= 1.0) still gave ~6/30 bad yes items ("Someone revealed that something happen.",
"Someone vowed whether to do something."). The 'no' side is reliable, but yes/no balance cannot be kept without the
noisy side. Labelling by hand would be model labelling (hard rule 5).

Build raw rows for megaacceptability (MegaAcceptability v2; White & Rawlins 2016, 2020; An & White 2020).

Source : http://megaattitude.io/projects/mega-acceptability/mega-acceptability-v2.zip (official release, sha256
         pinned), file mega-acceptability-v2.tsv (one row per participant response).
Licence: CC BY-SA 4.0 (LICENSE file inside the official zip: "Attribution-ShareAlike 4.0 International").
Texts  : researcher-built, semantically bleached sentences: 1,007 clause-embedding verbs x 50 syntactic frames x
         3 tenses ("Someone wondered whether something happened.", "Someone was bitched that something happen.").
Labels : 5 Mechanical Turk annotators per sentence rated acceptability on a 1-7 scale (1 = awful, 7 = perfectly fine).
         Non-native participants (README) are dropped. No split -> train.
Soft   : per-rater binarisation around the scale midpoint: 5-7 = acceptable vote, 1-3 = unacceptable, 4 = half a vote
         each; soft = {"yes": acceptable share, "no": 1 - share}.
Gold   : yes if the acceptable share >= 0.8, no if <= 0.2; the middle is dropped.
Sampling: stratified over the 50 frames (equal yes/no per frame where possible), at most 3 sentences per verb,
         sentences also used in the MegaVeridicality / MegaNegRaising parts removed (cross-v14 check).
Deterministic (seed 20261101).
"""
import collections
import random
import zipfile

import pandas as pd

import _cal_common as C

KEY = "megaacceptability"
URL = "http://megaattitude.io/projects/mega-acceptability/mega-acceptability-v2.zip"
ZIP_SHA = "17acd493a44834cded470ccb66b3aace538432cce297b3c5bb78b5aca9a5b7a4"
LICENCE = ("CC BY-SA 4.0 (LICENSE file in the official release zip http://megaattitude.io/projects/mega-acceptability/"
           "mega-acceptability-v2.zip: 'Attribution-ShareAlike 4.0 International')")
DATASET = "MegaAcceptability v2 (megaattitude.io; White & Rawlins 2016/2020)"
CACHE = C.CACHE / KEY
MAX_ROWS = 2500
PER_VERB = 3

Q = "Is this sentence acceptable, natural-sounding English?"
DEFS = {
    "yes": "Most of the 5 native-speaker raters (at least 80%, a rating of 4 counting half) rated it 5-7 on a 1-7 "
           "scale: the verb fits this frame, so a native speaker could say it, even though 'someone' and "
           "'something' leave the content vague.",
    "no": "At most 20% of the rating weight is on 5-7: most raters gave 1-3 because the verb does not fit this frame "
          "(wrong complement, preposition, voice or verb form), so a native speaker would not say it; vagueness "
          "alone does not make it unacceptable.",
}


def main():
    raise SystemExit("megaacceptability was REJECTED in review (noisy gold-yes labels); see the module docstring")
    rng = random.Random(C.SEED)
    z = C.fetch(URL, CACHE / "mega-acceptability-v2.zip", ZIP_SHA)
    with zipfile.ZipFile(z) as zf:
        with zf.open("mega-acceptability-v2/mega-acceptability-v2.tsv") as f:
            d = pd.read_csv(f, sep="\t")
    d = d[(d.nativeenglish == True) & d.response.notna()]  # noqa: E712
    items = []
    for sent, g in d.groupby("sentence", sort=True):
        v = [int(x) for x in g.response]
        n = len(v)
        if n < 4 or g.frame.nunique() != 1:
            continue
        yes, half = sum(x >= 5 for x in v), sum(x == 4 for x in v)
        p = (yes + 0.5 * half) / n
        if 0.2 < p < 0.8:
            continue
        s = sent.replace("\\'", "'").strip()
        items.append({"sent": s, "p": p, "yes": yes, "half": half, "n": n, "frame": g.frame.iloc[0],
                      "verb": g.verb.iloc[0], "tense": g.tense.iloc[0], "ratings": v})
    print("clear sentences:", len(items))
    core = {it["sent"]: [it["sent"]] for it in items}
    hits = C.cross_v14(core, {KEY})
    items = [it for it in items if it["sent"] not in hits]
    # decontaminate only the sampled pool below (the full pool is ~48k bleached sentences)
    rng.shuffle(items)
    by = collections.defaultdict(list)
    for it in items:
        by[(it["frame"], "yes" if it["p"] >= 0.8 else "no")].append(it)
    frames = sorted({f for f, _ in by})
    per_verb = collections.Counter()
    picked = []
    pool_order = [(f, g) for f in frames for g in ("yes", "no")]
    idx = {k: 0 for k in pool_order}
    target = int(MAX_ROWS * 1.1)
    while len(picked) < target and any(idx[k] < len(by[k]) for k in pool_order):
        for k in pool_order:
            while idx[k] < len(by[k]):
                it = by[k][idx[k]]
                idx[k] += 1
                if per_verb[it["verb"]] < PER_VERB:
                    per_verb[it["verb"]] += 1
                    picked.append(it)
                    break
    hits = C.decon({it["sent"]: [it["sent"]] for it in picked}, KEY)
    picked = [it for it in picked if it["sent"] not in hits]
    ys = [it for it in picked if it["p"] >= 0.8]
    ns = [it for it in picked if it["p"] <= 0.2]
    ny = min(len(ys), MAX_ROWS // 2)
    ys, ns = ys[:ny], ns[:MAX_ROWS - ny]
    rows = []
    for it in ys + ns:
        gold = "yes" if it["p"] >= 0.8 else "no"
        rows.append({
            "key": KEY, "rid": f"macc-{it['verb']}-{it['frame']}-{it['tense']}".replace(" ", "_"),
            "state": it["sent"], "instructions": Q, "options": C.YN, "gold": gold,
            "soft": C.soft_yes(it["yes"], it["n"], it["half"]),
            "meta": {"dataset": DATASET, "config": f"{it['frame']} / {it['tense']}",
                     "revision": f"v2, zip sha256 {ZIP_SHA}", "licence": LICENCE, "split": "train",
                     "orig_label": {"ratings_1to7": it["ratings"], "verb": it["verb"]},
                     "family": C.FAMILY, "edge": None},
        })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, {None: DEFS})
    st = C.summary(KEY, rows)
    print("frames:", len({r["meta"]["config"].split(" / ")[0] for r in rows}),
          "verbs:", len({r["meta"]["orig_label"]["verb"] for r in rows}))
    C.show_samples(rows, 6)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Acceptability of bleached verb-frame sentences with 5 native-speaker 1-7 ratings; soft = share rating 5-7 "
        "(4 = half). Gold >= 0.8 / <= 0.2. Stratified over 50 frames, <= 3 sentences per verb.", st))


if __name__ == "__main__":
    main()
