"""Build golden rows for winogrande (WinoGrande XL; Sakaguchi et al., AAAI 2020), TRAIN split only.

Source : HF allenai/winogrande (the AI2 release), config winogrande_xl, file winogrande_xl/train-00000-of-00001.parquet
         at revision 01e74176c63542e6b0bcb004dcdea22d94fb67b5 (40,398 sentences). validation/test never read.
Licence: CC-BY. Official repository README, section "License": "Winogrande (codebase) is licensed under the Apache
         License 2.0. The dataset is licensed under CC-BY." (github.com/allenai/winogrande @ 727e837, README.md).
Texts  : crowd-written twin sentences (AMT); each has a blank "_" and two candidate fillers; labels by construction of
         the twin (trigger word flips the answer), then validated by three crowd workers; AFLite removed easy items
         (model-based filtering of which items to keep, not labelling). No LLM text, no LLM labels.
Task   : yes/no only. "Does the blank (_) in the sentence stand for "X"?" where X is one of the two candidates.
         Twins (consecutive rows with the same candidates, flipped answer, word-Jaccard >= 0.5) are kept together and
         asked about the SAME candidate, so the gold flips with the one-word trigger change (meta.twin_of links them).
Balance: rows come in twin pairs -> exactly 50% yes. Half the pairs have person-name candidates, half object/concept
         candidates (social vs physical commonsense).
Dedupe : exact normalised sentences; near-duplicates (word-Jaccard >= 0.85 with an already chosen sentence of another
         pair that has the same candidate pair or the same first five words; the second block added in review 29 Sep
         2026 for items re-posted with one candidate reworded, e.g. 'wide sailor pants' / 'wide leg pants'); decontamination against forbidden label-NLI (winowhy etc.), local
         train/dev/eval files and JevBench public (see _common.decon).
Edge   : negation / double_negation / units / numeric / quantifier from surface cues of the sentence.
Deterministic (seed 20261114).
"""
import collections
import random
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

KEY = "winogrande"
SEED = 20261114
N_PAIRS = 3500
REV = "01e74176c63542e6b0bcb004dcdea22d94fb67b5"
GH_COMMIT = "727e837f77521ef38bcc56df3b275c8da43f45af"
CACHE = C.HERE / "cache" / KEY
FILES = {
    "train.parquet": (f"https://huggingface.co/datasets/allenai/winogrande/resolve/{REV}/winogrande_xl/"
                      "train-00000-of-00001.parquet",
                      "5d8c38ad12b9a6c88f79b6e00aaf0f40781f93d4f94816f6cff2b67625d67399"),
    "README.md": (f"https://raw.githubusercontent.com/allenai/winogrande/{GH_COMMIT}/README.md",
                  "6dc5ec952a9e5d6e553e2800c24b43b1fa8add70d998e60b76262e2195413efe"),
}
LICENCE = (f"CC-BY (github.com/allenai/winogrande/blob/{GH_COMMIT}/README.md, section 'License': 'The dataset is "
           "licensed under CC-BY.')")

DEFS = {
    "yes": "The named candidate is what the blank stands for: given the situation, everyday knowledge of people, "
           "objects and causes makes the clause containing the blank true of the named candidate rather than of the "
           "other candidate.",
    "no": "The blank stands for the other candidate: putting the named candidate in the blank makes the sentence "
          "illogical, self-contradictory or clearly less sensible than putting in the other candidate.",
}


def jacc(a, b):
    a, b = set(C.words(a)), set(C.words(b))
    return len(a & b) / max(1, len(a | b))


def is_person(o1, o2):
    return all(o[:1].isupper() and " " not in o.strip() for o in (o1, o2))


def main():
    rng = random.Random(SEED)
    paths = {n: C.fetch(u, CACHE / n, s) for n, (u, s) in FILES.items()}
    assert "The dataset is licensed under CC-BY." in paths["README.md"].read_text()
    df = pd.read_parquet(paths["train.parquet"])          # TRAIN ONLY
    assert len(df) == 40398
    recs = []
    for i, r in enumerate(df.itertuples(index=False)):
        s = C.clean(r.sentence)
        assert s.count("_") == 1, s
        recs.append({"rid": f"xl_train_{i:05d}", "i": i, "sentence": s, "o1": C.clean(r.option1),
                     "o2": C.clean(r.option2), "ans": int(r.answer)})

    # twin pairs: consecutive rows, same candidates, flipped answer, similar wording
    pairs, used = [], set()
    for a, b in zip(recs, recs[1:]):
        if a["i"] in used or b["i"] in used or a["i"] % 2 or (a["o1"], a["o2"]) != (b["o1"], b["o2"]):
            continue
        if a["ans"] == b["ans"] or jacc(a["sentence"], b["sentence"]) < 0.5:
            continue
        if C.norm(a["sentence"]) == C.norm(b["sentence"]):
            continue
        pairs.append((a, b))
        used |= {a["i"], b["i"]}
    print(f"records={len(recs)} twin pairs={len(pairs)} singles={len(recs) - 2 * len(pairs)}")

    # decontamination on every sentence of every candidate pair
    core = {x["rid"]: [x["sentence"]] for p in pairs for x in p}
    hits = C.decon(core)
    drop = collections.Counter(hits.values())
    pairs = [p for p in pairs if not any(x["rid"] in hits for x in p)]
    print(f"decon drops (records): {dict(drop)}; pairs left={len(pairs)}")

    # exact duplicates across the corpus (a sentence appearing twice anywhere drops its pair)
    cnt = collections.Counter(C.norm(x["sentence"]) for x in recs)
    pairs = [p for p in pairs if all(cnt[C.norm(x["sentence"])] == 1 for x in p)]

    pairs.sort(key=lambda p: p[0]["i"])
    rng.shuffle(pairs)
    people = [p for p in pairs if is_person(p[0]["o1"], p[0]["o2"])]
    things = [p for p in pairs if not is_person(p[0]["o1"], p[0]["o2"])]
    print(f"person-candidate pairs={len(people)} object/concept pairs={len(things)}")

    chosen, blocks = [], collections.defaultdict(list)

    def take(pool, n):
        got = 0
        for p in pool:
            if got >= n:
                break
            blk = tuple(sorted((p[0]["o1"].lower(), p[0]["o2"].lower())))
            blk2 = ("first5",) + tuple(C.words(p[0]["sentence"])[:5])   # same item, one candidate reworded
            ws = [set(C.words(x["sentence"])) for x in p]
            if any(len(w & o) / max(1, len(w | o)) >= 0.85 for w in ws for b in (blk, blk2) for o in blocks[b]):
                continue
            blocks[blk].extend(ws)
            blocks[blk2].extend(ws)
            chosen.append(p)
            got += 1
        return got

    half = N_PAIRS // 2
    g1 = take(people, half)
    g2 = take(things, N_PAIRS - g1)
    if g1 + g2 < N_PAIRS:
        take([p for p in people if p not in chosen], N_PAIRS - g1 - g2)
    print(f"chosen pairs={len(chosen)} (people {g1}, things {g2})")

    rows = []
    for a, b in chosen:
        asked = rng.choice([a["o1"], a["o2"]])
        for x, twin in ((a, b), (b, a)):
            gold_opt = x["o1"] if x["ans"] == 1 else x["o2"]
            state = f'{x["sentence"]}\n\nThe blank (_) stands for one of two candidates: "{x["o1"]}" or "{x["o2"]}".'
            rows.append({
                "key": KEY,
                "rid": x["rid"],
                "state": state,
                "instructions": f'Does the blank (_) in the sentence stand for "{asked}"?',
                "options": C.YN,
                "gold": "yes" if gold_opt == asked else "no",
                "soft": None,
                "meta": {"dataset": "allenai/winogrande", "config": "winogrande_xl",
                         "revision": f"hf:{REV}; sha256:{FILES['train.parquet'][1]}", "licence": LICENCE,
                         "split": "train",
                         "orig_label": {"option1": x["o1"], "option2": x["o2"], "answer": x["ans"]},
                         "family": C.FAMILY,
                         "edge": C.edge(x["sentence"], order=("double_negation", "negation", "units", "numeric",
                                                              "quantifier")),
                         "twin_of": twin["rid"]},
            })
    rng.shuffle(rows)
    out = C.write_outputs(KEY, rows, {None: DEFS})
    s = C.summary(KEY, rows)
    print("wrote", len(rows), "->", out)
    C.show_samples(rows, 5, seed=SEED)
    C.append_manifest({
        "key": KEY, "family": C.FAMILY, "dataset": "allenai/winogrande (winogrande_xl train)", "licence": LICENCE,
        "rows": len(rows), "qtype": "yesno", "yesno_share": s["yes_share"],
        "edge_tags": sorted(t for t in s["edges"] if t),
        "notes": ("Twin-sentence coreference (commonsense). Yes/no 'does the blank stand for X', both twins asked about "
                  "the same candidate so the one-word trigger flips the gold (meta.twin_of). Half person-name, half "
                  "object/concept candidates. Decon vs label-NLI (incl. winowhy), local files, JevBench."),
    })


if __name__ == "__main__":
    main()
