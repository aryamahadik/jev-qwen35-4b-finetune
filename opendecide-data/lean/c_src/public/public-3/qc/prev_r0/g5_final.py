#!/usr/bin/env python3
"""G5 result for public-3 (prep5/B4): the flag-only reader's final verdicts on the seeded sample (qc/g5_sample_ids.json,
read through qc/g5_show.py: decoder_io.user_msg in the C round-1 style). Indices are positions in each dataset's
sample order; ids are written out, never text. The reader never set or edited a label.
Spec 8 G5, public rows: dataset-level decision only: a dataset with > 8% clearly wrong golds (> 8 of 100) is dropped.
"Clearly wrong" = a careful reader applying the row's own card would answer differently with high confidence and the
gold is not a defensible reading; anything weaker is "ambiguous" (reported; the <= 1% ambiguous bar is for families).
Writes qc/g5.json."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WRONG = {"c_pub_edos": [25],
         "c_pub_ghc": [6, 20, 32, 38, 50, 65, 69, 75, 96, 97],
         "c_pub_mams": [15, 23, 35, 40, 72, 73, 77, 84],
         "c_pub_sarcasm": [],
         "c_pub_xed": []}
AMBIG = {"c_pub_edos": [5, 14, 20, 32, 43, 49, 59, 86, 89, 95, 98],
         "c_pub_ghc": [0, 4, 18, 26, 36, 44, 63, 67, 68, 72, 76, 80, 83, 84, 93, 98],
         "c_pub_mams": [1, 6, 11, 22, 27, 34, 42, 55, 60, 61, 66, 68, 69, 71, 80, 92, 94],
         "c_pub_sarcasm": [],
         "c_pub_xed": [7, 8, 12, 14, 21, 37, 44, 50, 60, 62, 67, 78, 80, 89]}
NOTES = {"c_pub_ghc": "every flagged gold equals the GHC hd/cv/vo majority labels as parsed by both public-3 and "
                      "formats-2 (dataset label noise, not a parse bug); typical: no profanity labelled vulgar, "
                      "political or news posts labelled attack / call for violence, a group attack labelled vulgar only",
         "c_pub_mams": "at the bar (8 = 8%, not > 8%); every flagged gold equals the MAMS term / category polarity as "
                       "parsed by both public-3 and formats-2 (dataset label noise); 1 more (80) judged ambiguous",
         "c_pub_edos": "category labels of EDOS are noisy (11 ambiguous), 1 clearly wrong",
         "c_pub_xed": "subjective emotion tags: 14 ambiguous, none clearly wrong"}


def main():
    s = json.load(open(HERE / "g5_sample_ids.json"))
    out, prob = {}, []
    for ds, ids in s["ids"].items():
        w, a = WRONG[ds], AMBIG[ds]
        assert not set(w) & set(a) and len(ids) == 100
        fail = len(w) > 8
        out[ds] = {"read": len(ids), "clearly_wrong": len(w), "ambiguous": len(a), "bar": "> 8 of 100 clearly wrong drops the dataset",
                   "pass": not fail, "clearly_wrong_ids": [ids[i] for i in w], "ambiguous_ids": [ids[i] for i in a],
                   "note": NOTES.get(ds, "")}
        if fail:
            prob.append(f"{ds}: {len(w)}/100 clearly wrong > 8% -> spec G5: drop the dataset")
    res = {"gate": "G5", "pass": not prob, "problems": prob, "seed": s["seed"], "per_dataset": out,
           "reader": "independent Claude session (prep5 checker; not a public-3 author), flag-only",
           "render": "decoder_io.user_msg, STYLE/LAYOUT of runs/q35_4b_c_r1.json (cygnet, schema_branch_mark), seeded "
                     "random option order; reader saw the prompt and the displayed gold only",
           "builder_sample_check": "out/public3_g5_sample_ids.json: 500 ids, 100 per dataset, all in the current mixed "
                                   "files (88 shared with this draw); used as a check only"}
    (HERE / "g5.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k: (v["clearly_wrong"], v["ambiguous"], v["pass"]) for k, v in out.items()}), prob)


if __name__ == "__main__":
    main()
