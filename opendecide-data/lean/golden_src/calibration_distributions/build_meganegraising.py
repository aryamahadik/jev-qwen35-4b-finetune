"""Build raw rows for meganegraising (MegaNegRaising v1; An & White, SCiL 2020, arXiv 1908.05253).

Source : http://megaattitude.io/projects/mega-negraising/mega-negraising-v1.zip (official release, sha256 pinned),
         file mega-negraising-v1.tsv (one row per participant response).
Licence: CC BY-SA 4.0 (LICENSE file inside the official zip: "Attribution-ShareAlike 4.0 International").
Texts  : researcher-built, semantically bleached sentence pairs for ~925 clause-embedding verbs x 6 frames x
         tense x subject person: sentence1 has matrix negation ("I don't think that a particular thing happened."),
         sentence2 has embedded negation ("I think that that thing didn't happen."). No model-written text.
Labels : ~10 Mechanical Turk annotators per pair answered "If I were to say <sentence1>, how likely is it that I
         mean <sentence2>?" on a 0-1 slider (left = extremely unlikely, middle = maybe or maybe not, right =
         extremely likely), and rated how easy it is to imagine someone saying sentence1 (0-1). No split -> train.
Soft   : per-annotator binarisation at the slider midpoint: > 0.5 = "likely" vote, < 0.5 = "unlikely", exactly 0.5 =
         half a vote each; soft = {"yes": likely share, "no": 1 - likely share}.
Gold   : yes if the likely share >= 0.7 AND the mean slider >= 0.7; no if the likely share <= 0.3 AND the mean slider
         <= 0.3; the middle and vote/mean disagreements are dropped (review 29 Sep: with the share rule alone, sliders
         just above 0.5 made items such as "doesn't murmur that" / "isn't agitated that" gold yes, contradicting the
         definition; the mean check keeps only clear neg-raisers: think, want, seem, suppose, intend, expect ...).
         The release's automatically built sentence2 writes particle verbs with an underscore ("I set_out not to
         ..."); the underscore is replaced by a space. Pairs whose sentence1 has mean
         imaginability < 0.6 are dropped (odd sentences such as "I wasn't thanked to do a particular thing").
         Non-native participants (README) are dropped.
Balance: yes share 0.40 (yes is the scarce side; ~90 clear yes pairs, so the key is small). Deterministic (seed 20261101).
"""
import random
import zipfile

import pandas as pd

import _cal_common as C

KEY = "meganegraising"
URL = "http://megaattitude.io/projects/mega-negraising/mega-negraising-v1.zip"
ZIP_SHA = "6121ed8da217e1e66c20e115fe90848a2d0c3a61e896ebfaaa388a966106ef23"
LICENCE = ("CC BY-SA 4.0 (LICENSE file in the official release zip http://megaattitude.io/projects/mega-negraising/"
           "mega-negraising-v1.zip: 'Attribution-ShareAlike 4.0 International')")
DATASET = "MegaNegRaising v1 (megaattitude.io; An & White 2020)"
CACHE = C.CACHE / KEY
YES_SHARE = 0.40
MIN_ACC = 0.6

Q = 'If someone says this sentence, is it likely that they mean "{}"?'
DEFS = {
    "yes": "At least 7 of 10 annotators, and the average rating, judged it likely that a speaker of the negated "
           "sentence means the version with the negation moved into the embedded clause (a neg-raising reading, as "
           "'I don't think it happened' usually means 'I think it didn't happen').",
    "no": "At most 3 of 10 annotators, and the average rating, judged it likely: the sentence only denies the "
          "attitude or report itself (as 'I didn't say it happened' does not mean 'I said it didn't happen').",
}


def main():
    rng = random.Random(C.SEED)
    z = C.fetch(URL, CACHE / "mega-negraising-v1.zip", ZIP_SHA)
    with zipfile.ZipFile(z) as zf:
        with zf.open("mega-negraising-v1/mega-negraising-v1.tsv") as f:
            d = pd.read_csv(f, sep="\t")
    d = d[(d.nativeenglish == True) & d.negraising.notna()]  # noqa: E712
    items = []
    for (s1, s2), g in d.groupby(["sentence1", "sentence2"], sort=True):
        v = g.negraising.tolist()
        n = len(v)
        if n < 8:
            continue
        acc = g.acceptability.mean()
        if acc < MIN_ACC:
            continue
        likely = sum(x > 0.5 for x in v)
        half = sum(x == 0.5 for x in v)
        p = (likely + 0.5 * half) / n
        mean = sum(v) / n
        if not ((p >= 0.7 and mean >= 0.7) or (p <= 0.3 and mean <= 0.3)):
            continue
        s1c = s1.replace("\\'", "'").replace("_", " ").strip()
        s2c = s2.replace("\\'", "'").replace("_", " ").strip()
        items.append({"s1": s1c, "s2": s2c, "p": p, "n": n, "likely": likely, "half": half,
                      "verb": g.verb.iloc[0], "frame": g.frame.iloc[0], "tense": g.tense.iloc[0],
                      "subject": g.subject.iloc[0], "acc": round(acc, 3),
                      "sliders": [round(x, 2) for x in v]})
    print("clear pairs:", len(items))
    core = {it["s1"]: [it["s1"]] for it in items}
    hits = C.decon(core, KEY)
    hits.update(C.cross_v14(core, {KEY}))
    items = [it for it in items if it["s1"] not in hits]
    rng.shuffle(items)
    yes = [it for it in items if it["p"] >= 0.7]
    no = sorted([it for it in items if it["p"] <= 0.3], key=lambda it: it["p"])
    # keep the no side diverse: at most 2 pairs per verb (the clearest first), then fill
    per_verb, no_pick, rest = {}, [], []
    for it in no:
        if per_verb.get(it["verb"], 0) < 2:
            no_pick.append(it)
            per_verb[it["verb"]] = per_verb.get(it["verb"], 0) + 1
        else:
            rest.append(it)
    nn = int(len(yes) * (1 - YES_SHARE) / YES_SHARE)
    no = (no_pick + rest)[:nn]
    print({"yes": len(yes), "no": len(no)})
    rows = []
    for gold, group in (("yes", yes), ("no", no)):
        for it in group:
            rows.append({
                "key": KEY, "rid": f"mnr-{it['verb']}-{it['frame']}-{it['tense']}-{it['subject']}".replace(" ", "_"),
                "state": it["s1"], "instructions": Q.format(it["s2"]), "options": C.YN, "gold": gold,
                "soft": C.soft_yes(it["likely"], it["n"], it["half"]),
                "meta": {"dataset": DATASET, "config": f"{it['frame']} / {it['tense']} / {it['subject']} person",
                         "revision": f"v1, zip sha256 {ZIP_SHA}", "licence": LICENCE, "split": "train",
                         "orig_label": {"sliders_0to1": it["sliders"], "imaginability_mean": it["acc"],
                                        "verb": it["verb"]},
                         "family": C.FAMILY, "edge": "negation"},
            })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, {None: DEFS})
    st = C.summary(KEY, rows)
    C.show_samples(rows, 6)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Neg-raising (negation scope) judgements: 'If someone says <not V that S>, do they mean <V that not S>?'. "
        "Soft = share of ~10 annotators whose 0-1 likelihood slider is above the midpoint (0.5 = half vote). "
        "Gold: share >= 0.7 and mean slider >= 0.7 / share <= 0.3 and mean <= 0.3; sentences with imaginability < 0.6 "
        "dropped; non-native raters dropped; particle-verb underscores in sentence2 replaced by spaces.", st))


if __name__ == "__main__":
    main()
