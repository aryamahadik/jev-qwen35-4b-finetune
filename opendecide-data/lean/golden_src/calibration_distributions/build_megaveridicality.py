"""Build raw rows for megaveridicality (MegaVeridicality v2.1; White & Rawlins 2018, White et al. EMNLP 2018).

Source : http://megaattitude.io/projects/mega-veridicality/mega-veridicality-v2.1.zip (official release 2.1,
         2020-07-29; sha256 pinned), file mega-veridicality-v2.1.tsv (one row per participant response).
Licence: CC BY-SA 4.0 (LICENSE file inside the official zip: "Attribution-ShareAlike 4.0 International").
Texts  : researcher-built, semantically bleached sentences, one per clause-embedding verb x syntactic frame x matrix
         polarity ("Someone didn't know that a particular thing happened.", "A particular person didn't manage to do
         a particular thing."). No model-written text.
Labels : 10 Mechanical Turk annotators per sentence answered "Did that thing happen?" (or "Did that person do/have
         that thing?") with yes / maybe or maybe not / no, plus a 1-7 acceptability rating. No split -> train.
Filter : responses from participants who did not report American English as their native language are dropped
         (README 'exclude' rule); the 1,088 Task-2 items embedded in a conditional antecedent are not used (their
         displayed question is not in the release); sentences with mean acceptability < 4 of 7 are dropped
         (odd sentences such as "Someone updated that a particular thing happened" give unreliable judgements).
Tasks  (one question per sentence; faithful binary readings of the 3-way answer):
 - q_pos "Does this sentence imply that <P>?": yes-share = share of 'yes' answers; no = 'maybe or maybe not' + 'no'.
   gold yes if yes-share >= 0.7, gold no if yes-share <= 0.3.
 - q_neg "Does this sentence imply that <not P>?": yes-share = share of 'no' answers; gold yes if >= 0.6 of the
   annotators answered 'no' and at most 0.1 answered 'yes'; gold no if at most 0.1 answered 'no'.
   All q_neg-yes sentences are used, matched by as many q_neg-no sentences (half 'yes'-dominant, half
   'maybe'-dominant); every other clear sentence goes to q_pos.
Edge   : negation (negated matrix verb or negated question), double_negation (both).
Deterministic (seed 20261101).
"""
import collections
import random
import zipfile

import pandas as pd

import _cal_common as C

KEY = "megaveridicality"
URL = "http://megaattitude.io/projects/mega-veridicality/mega-veridicality-v2.1.zip"
ZIP_SHA = "1442ef1f0da66b4965f6d289966bd6240082ce0959c56584b4224ec00eb82219"
LICENCE = ("CC BY-SA 4.0 (LICENSE file in the official release zip http://megaattitude.io/projects/mega-veridicality/"
           "mega-veridicality-v2.1.zip: 'Attribution-ShareAlike 4.0 International')")
DATASET = "MegaVeridicality v2.1 (megaattitude.io, White & Rawlins 2018; White et al. 2018), Task-1 items"
CACHE = C.CACHE / KEY
YES_SHARE_POS = 0.42

PROP = {  # frame -> (positive proposition, negated proposition)
    "that": ("the particular thing happened", "the particular thing did not happen"),
    "do": ("the particular person did the particular thing", "the particular person did not do the particular thing"),
    "have": ("the particular person had the particular thing",
             "the particular person did not have the particular thing"),
}
FRAME_KIND = {
    "NP Ved that S": "that", "NP was Ved that S": "that", "NP Ved for NP to VP": "that",
    "NP Ved to VP[+eventive]": "do", "NP was Ved to VP[+eventive]": "do", "NP Ved NP to VP[+eventive]": "do",
    "NP Ved to VP[-eventive]": "have", "NP was Ved to VP[-eventive]": "have", "NP Ved NP to VP[-eventive]": "have",
}
Q = "Does this sentence imply that {}?"
DEFS = {
    "q_pos": {
        "yes": "At least 7 of 10 annotators, reading only this sentence, answered that it did happen (the person did or "
               "had it): the verb with its polarity commits the speaker to it, as with 'knew that', 'managed to' or "
               "'didn't forget to'.",
        "no": "At most 3 of 10 answered that it happened; the rest judged it merely possible ('maybe or maybe not', as "
              "after 'wanted', 'hoped', 'was asked to') or judged that it did not happen (as after 'didn't manage to', "
              "'pretended that').",
    },
    "q_neg": {
        "yes": "At least 6 of 10 annotators (and at most 1 saying the opposite) answered that it did NOT happen (the "
               "person did not do or have it): the sentence commits the speaker to non-occurrence, as with "
               "'neglected to', 'refused to' or 'didn't manage to'.",
        "no": "At most 1 of 10 annotators answered that it did not happen; the others judged that it did happen (as "
              "after 'didn't forget to', 'was glad that') or that it might or might not have (as after 'wanted', "
              "'wasn't told to').",
    },
}


def main():
    rng = random.Random(C.SEED)
    z = C.fetch(URL, CACHE / "mega-veridicality-v2.1.zip", ZIP_SHA)
    with zipfile.ZipFile(z) as zf:
        with zf.open("mega-veridicality-v2.1/mega-veridicality-v2.1.tsv") as f:
            d = pd.read_csv(f, sep="\t")
    d = d[(d.nativeenglish == True) & (d.conditional == False) & d.veridicality.notna()]  # noqa: E712
    items = []
    for sent, g in d.groupby("sentence", sort=True):
        v = g.veridicality.tolist()
        n = len(v)
        if n < 9 or g.frame.nunique() != 1:
            continue
        acc = g.acceptability.mean()
        if acc < 4:
            continue
        s = sent.replace("\\'", "'").strip()
        if not s.endswith("."):
            s += "."
        items.append({"sent": s, "frame": g.frame.iloc[0], "pol": g.polarity.iloc[0], "verb": g.verb.iloc[0], "n": n,
                      "py": v.count("yes") / n, "pm": v.count("maybe") / n, "pn": v.count("no") / n,
                      "counts": {k: v.count(k) for k in ("yes", "maybe", "no")}, "acc": round(acc, 2)})
    print("items (acceptability >= 4):", len(items))
    core = {it["sent"]: [it["sent"]] for it in items}
    hits = C.decon(core, KEY)
    hits.update(C.cross_v14(core, {KEY}))
    items = [it for it in items if it["sent"] not in hits]

    rng.shuffle(items)
    neg_yes = [it for it in items if it["pn"] >= 0.6 and it["py"] <= 0.1]
    pool_no_yesdom = [it for it in items if it["pn"] <= 0.1 and it["py"] >= 0.7]
    pool_no_maydom = [it for it in items if it["pn"] <= 0.1 and it["pm"] >= 0.7]
    k = len(neg_yes)
    neg_no = pool_no_yesdom[:k // 2] + pool_no_maydom[:k - k // 2]
    used = {it["sent"] for it in neg_yes + neg_no}
    rest = [it for it in items if it["sent"] not in used]
    pos_yes = [it for it in rest if it["py"] >= 0.7]
    pos_no = [it for it in rest if it["py"] <= 0.3]
    nn = min(len(pos_no), int(len(pos_yes) * (1 - YES_SHARE_POS) / YES_SHARE_POS))
    pos_no.sort(key=lambda it: (it["py"], it["sent"]))  # clearest 'not implied' first
    pos_no = pos_no[:nn]
    print({"neg_yes": len(neg_yes), "neg_no": len(neg_no), "pos_yes": len(pos_yes), "pos_no": len(pos_no)})

    rows = []
    for qid, gold, group in (("q_neg", "yes", neg_yes), ("q_neg", "no", neg_no),
                             ("q_pos", "yes", pos_yes), ("q_pos", "no", pos_no)):
        for it in group:
            pos, negp = PROP[FRAME_KIND[it["frame"]]]
            p_yes = it["pn"] if qid == "q_neg" else it["py"]
            negated_sent = it["pol"] == "negative"
            if qid == "q_neg":
                e = "double_negation" if negated_sent else "negation"
            else:
                e = "negation" if negated_sent else None
            rows.append({
                "key": KEY, "rid": f"mv2-{qid}-{it['verb']}-{it['frame']}-{it['pol']}".replace(" ", "_"),
                "state": it["sent"], "instructions": Q.format(negp if qid == "q_neg" else pos),
                "options": C.YN, "gold": gold, "soft": {"yes": round(p_yes, 4), "no": round(1 - p_yes, 4)},
                "meta": {"dataset": DATASET, "config": f"{it['frame']} / {it['pol']}", "revision":
                         f"release 2.1 (2020-07-29), zip sha256 {ZIP_SHA}", "licence": LICENCE, "split": "train",
                         "orig_label": {"answers": it["counts"], "mean_acceptability_1to7": it["acc"],
                                        "verb": it["verb"]},
                         "family": C.FAMILY, "edge": e, "defs": qid},
            })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, {"q_pos": DEFS["q_pos"], "q_neg": DEFS["q_neg"]})
    st = C.summary(KEY, rows)
    C.show_samples(rows, 6)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Veridicality/factivity under negation with 10 native-speaker votes per sentence (yes / maybe or maybe not / "
        "no). q_pos: implies it happened (yes-share = 'yes' answers); q_neg: implies it did not happen (yes-share = "
        "'no' answers). Two defs files (__q_pos, __q_neg). Non-native raters, conditional Task-2 items and "
        "sentences with mean acceptability < 4/7 dropped.", st))


if __name__ == "__main__":
    main()
