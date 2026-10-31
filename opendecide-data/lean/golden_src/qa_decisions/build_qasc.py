"""Build golden rows for qasc (QASC: Question Answering via Sentence Composition; Khot et al., AAAI 2020), TRAIN only.

Source : HF allenai/qasc (AI2's official record: allenai.org/data/qasc redirects to it), data/train-00000-of-00001.parquet
         at revision a34ba204eb9a33b919c10cc08f4f1c8dae5ec070 (8,134 questions). validation/test never read.
Licence: CC BY 4.0 -- dataset card README.md at that revision, "Licensing Information": "The dataset is released
         under [CC BY 4.0] license." (also `license: cc-by-4.0` in the card metadata).
Texts  : grade-school science questions written by crowd workers who combined two facts (fact1 from a seed set of
         science facts, fact2 from a large web-sentence corpus) into a composed fact and a question with 8 choices.
         Labels: the worker's composed answer (human). No LLM text or labels.
Tasks  : every row shows Fact 1, Fact 2, the question and the 8 lettered choices (without the facts several
         questions are ambiguous, e.g. clouds -> 'beads' vs 'rain'; with them the chained answer is determinate).
         - yes/no (default defs): 'Do Fact 1 and Fact 2, taken together, lead to answer choice (X) "..."?'
           50% asked about the gold choice, 50% about one distractor. Distractors that could also be read as right
           are never asked about: a distractor is eligible only if it shares no content word with the facts, the
           composed fact or the gold answer, is not a generic category word (animals, organisms, people, ...),
           neither answer contains the other, and it is not a look-alike string of the gold (difflib ratio < 0.6).
           Residual risk (audited on 25 'no' rows): a distractor may be true in the world but not established by the
           two facts (e.g. 'ferns' when the facts establish 'humans'); the definition says such choices are 'no',
           and the yes/no share is kept at half of the rows for that reason (3,000 yes/no, 3,000 choice).
         - choice (defs qid "choice"): 'Which answer choice do Fact 1 and Fact 2, taken together, lead to?' A-H.
Dedupe : one row per distinct question text (561 repeated questions dropped); decontamination vs forbidden label-NLI,
         local train/dev/eval files and JevBench public.
Edge   : multi_hop (two-fact composition) unless the question carries negation.
Deterministic (seed 20261116).
"""
import collections
import difflib
import random
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

KEY = "qasc"
SEED = 20261116
N_YN = 3000
N_CHOICE = 3000
REV = "a34ba204eb9a33b919c10cc08f4f1c8dae5ec070"
CACHE = C.HERE / "cache" / KEY
FILES = {
    "train.parquet": (f"https://huggingface.co/datasets/allenai/qasc/resolve/{REV}/data/train-00000-of-00001.parquet",
                      "b9a297b5ab55f1605c7682ffbb7042c26d7ecb9ff1e1aa5a820d4e791c8302d1"),
    "README.md": (f"https://huggingface.co/datasets/allenai/qasc/resolve/{REV}/README.md",
                  "c90ae4776b98cd6fc0a22558784c43b07e1f0b00a090dda99797d6b6efab4a3e"),
}
LICENCE = (f"CC BY 4.0 (huggingface.co/datasets/allenai/qasc/blob/{REV}/README.md, 'Licensing Information': 'The "
           "dataset is released under CC BY 4.0 license.'; allenai.org/data/qasc redirects to this card)")
STOP = set("a an the of to in on at by for with from and or is are was were be been being it its this that these "
           "those as can could will would may might do does did has have had not no than then so such into onto "
           "over under up down out off their there they them he she his her we our you your i my me which what who "
           "whom whose when where why how all any some most more less many much one two".split())
GENERIC = {"animals", "animal", "organisms", "organism", "living things", "living thing", "things", "creatures",
           "people", "humans", "human", "person", "man", "men", "mammals", "vertebrates", "plants", "species", "life",
           "cells", "matter", "energy", "objects", "something", "it", "they", "nothing", "everything", "earth",
           "the earth", "water", "heat", "food", "nutrients", "an object", "most organisms", "all organisms"}

DEFS = {
    "yes": "Chaining Fact 1 and Fact 2 through the concept they share answers the question with the named choice: "
           "the conclusion the two facts establish together names that choice or an obvious paraphrase of it.",
    "no": "The two facts, chained together, lead to a different listed choice; the named choice is not what they "
          "establish, even if it might be true in general or from outside knowledge.",
}
LET = C.letters(8)
DEFS_CHOICE = {L: f"Choice ({L}) is the answer the question gets when Fact 1 and Fact 2 are chained through the "
                  f"concept they share (the conclusion the two facts establish together names it)." for L in LET}


def content(t):
    return {w for w in C.words(t) if w not in STOP and len(w) > 2} | {w[:-1] for w in C.words(t)
                                                                      if w.endswith("s") and len(w) > 4}


def eligible_distractor(d, gold, facts):
    dn, gn = C.norm(d), C.norm(gold)
    if not dn or dn in GENERIC or dn in gn or gn in dn:
        return False
    if difflib.SequenceMatcher(None, dn, gn).ratio() >= 0.6:   # look-alikes such as HPV/HIV, expode/explode
        return False
    cd = content(d)
    if not cd:
        return False
    return not (cd & content(facts)) and not (cd & content(gold))


def main():
    rng = random.Random(SEED)
    paths = {n: C.fetch(u, CACHE / n, s) for n, (u, s) in FILES.items()}
    assert "The dataset is released under [CC BY 4.0]" in paths["README.md"].read_text()
    df = pd.read_parquet(paths["train.parquet"])          # TRAIN ONLY
    assert len(df) == 8134
    recs, seen_q = [], set()
    for r in df.itertuples(index=False):
        labels, texts = list(r.choices["label"]), [C.clean(t) for t in r.choices["text"]]
        if labels != LET or r.answerKey not in LET or len(set(C.norm(t) for t in texts)) != 8:
            continue
        nq = C.norm(r.question)
        if nq in seen_q:
            continue
        seen_q.add(nq)
        recs.append({"rid": r.id, "q": C.clean(r.question), "ch": texts, "key": r.answerKey,
                     "f1": C.clean(r.fact1), "f2": C.clean(r.fact2), "cf": C.clean(r.combinedfact)})
    print(f"records={len(df)} usable (distinct questions, 8 distinct choices)={len(recs)}")

    hits = C.decon({r["rid"]: [r["q"], r["f1"], r["f2"], r["cf"]] for r in recs})
    print("decon drops:", dict(collections.Counter(hits.values())))
    recs = [r for r in recs if r["rid"] not in hits]

    rng.shuffle(recs)
    meta0 = {"dataset": "allenai/qasc", "config": "default", "revision": f"hf:{REV}; sha256:{FILES['train.parquet'][1]}",
             "licence": LICENCE, "split": "train", "family": C.FAMILY}

    def state(r):
        ch = "\n".join(f"({L}) {t}" for L, t in zip(LET, r["ch"]))
        return f"Fact 1: {r['f1']}\nFact 2: {r['f2']}\n\nQuestion: {r['q']}\nAnswer choices:\n{ch}"

    def edge(r):
        return "negation" if C.neg_count(r["q"]) else "multi_hop"

    rows, n_skip = [], 0
    ask_gold_flags = [True] * (N_YN // 2) + [False] * (N_YN - N_YN // 2)
    rng.shuffle(ask_gold_flags)
    it = iter(recs)
    yn_rows = []
    for ask_gold in ask_gold_flags:
        while True:
            r = next(it)
            gi = LET.index(r["key"])
            facts = " ".join([r["f1"], r["f2"], r["cf"], r["q"]])
            elig = [i for i in range(8) if i != gi and eligible_distractor(r["ch"][i], r["ch"][gi], facts)]
            if ask_gold:
                ai = gi
                break
            if elig:
                ai = rng.choice(elig)
                break
            n_skip += 1          # no safe distractor: this record stays in the pool for the choice question
        yn_rows.append({"key": KEY, "rid": r["rid"], "state": state(r),
                        "instructions": f'Do Fact 1 and Fact 2, taken together, lead to answer choice '
                                        f'({LET[ai]}) "{r["ch"][ai]}"?',
                        "options": C.YN, "gold": "yes" if ai == gi else "no", "soft": None,
                        "meta": dict(meta0, orig_label={"answerKey": r["key"], "combinedfact": r["cf"],
                                                         "asked": LET[ai]}, edge=edge(r))})
    used = {x["rid"] for x in yn_rows}
    rest = [r for r in recs if r["rid"] not in used]
    seen = set()
    ch_rows = []
    for r in rest:
        if len(ch_rows) >= N_CHOICE:
            break
        if r["rid"] in seen:
            continue
        seen.add(r["rid"])
        ch_rows.append({"key": KEY, "rid": r["rid"], "state": state(r),
                        "instructions": "Which answer choice do Fact 1 and Fact 2, taken together, lead to?",
                        "options": LET, "gold": r["key"], "soft": None,
                        "meta": dict(meta0, defs="choice", orig_label={"answerKey": r["key"], "combinedfact": r["cf"]},
                                     edge=edge(r))})
    rows = yn_rows + ch_rows
    rng.shuffle(rows)
    print(f"records without a safe distractor (moved to choice pool): {n_skip}")
    out = C.write_outputs(KEY, rows, {None: DEFS, "choice": DEFS_CHOICE})
    s = C.summary(KEY, rows)
    print("wrote", len(rows), "->", out)
    C.show_samples(rows, 6, seed=SEED)
    C.append_manifest({
        "key": KEY, "family": C.FAMILY, "dataset": "allenai/qasc (train)", "licence": LICENCE, "rows": len(rows),
        "qtype": "yesno+choice", "yesno_share": s["yes_share"], "edge_tags": sorted(t for t in s["edges"] if t),
        "notes": (f"Two-fact science composition with the facts shown (evidence-based, multi-hop). {len(yn_rows)} "
                  f"yes/no 'do the facts lead to choice X' (distractors asked only when they cannot also be read as "
                  f"right) + {len(ch_rows)} 8-way letter choice (defs qid 'choice'). One row per distinct question."),
    })


if __name__ == "__main__":
    main()
