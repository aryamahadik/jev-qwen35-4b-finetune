"""Build golden rows for comve (SemEval-2020 Task 4 ComVE, Commonsense Validation; Wang et al. 2020), TRAIN only.

Source : github.com/wangcunxiang/SemEval2020-Task4-Commonsense-Validation-and-Explanation @ c55b1a9e,
         "ALL data/train.csv" (10,000 training pairs; the dev and test files are never read).
Licence: CC BY-SA 4.0 -- repository README.md, section "License": "The dataset is distributed under the
         [CC BY-SA 4.0] license."
Texts  : human-written minimal pairs: a sensible statement and a nonsensical twin that differs in a few words
         (Wang et al., ACL 2019 "Does It Make Sense? And Why?"; SemEval-2020 Task 4). Subtask A human accuracy 99.1%.
Tasks  : subtask A only (the cleanest part), in the annotated comparative framing only: both statements of a pair,
         random order; "Of these two statements, does Statement N go against common sense?" (exactly the decision the
         annotators made; human accuracy 99.1%). Each source record is used once.
         Single-statement framing ("Does this statement make sense?") was built first and REMOVED in review (29 Sep
         2026): shown alone, about 6% of nonsense statements are plainly sensible ('Lip gloss can make lips red.',
         'I bought a ring with stones.', 'He devoted his life to the study of courage.') and about 10% more are only
         unusual ('alex drove the van into the lake', 'He is drinking a bottle of bleach.'). They are nonsense only
         relative to their twin, so a single-statement 'no' is not a gold label.
         Subtask B reasons were inspected and NOT used: several 'confusing' reasons also explain the nonsense
         (e.g. '200 is one hundred' / confusing reason '200 is bigger than one hundred'), too noisy for gold rows.
Dedupe : exact normalised statements across the whole file (a statement text is used at most once in any state);
         decontamination vs forbidden label-NLI, local train/dev/eval files and JevBench public.
Edge   : double_negation / negation / units / numeric / quantifier / temporal cues of the decisive statement(s).
Deterministic (seed 20261115).
"""
import collections
import random
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

KEY = "comve"
SEED = 20261115
N_PAIR = 8000
COMMIT = "c55b1a9e6cb66997675f85073e17a9522cf38c2c"
BASE = f"https://raw.githubusercontent.com/wangcunxiang/SemEval2020-Task4-Commonsense-Validation-and-Explanation/{COMMIT}/"
CACHE = C.HERE / "cache" / KEY
FILES = {
    "train.csv": (BASE + "ALL%20data/train.csv", "a850e53f066697943220a5e2a01c732f929833717f7af9982b0ec81835ed19f8"),
    "README.md": (BASE + "README.md", "5893be805d3add4cea68250716dda05d010c41fc57c581455ba265a33d8469de"),
}
LICENCE = (f"CC BY-SA 4.0 (github.com/wangcunxiang/SemEval2020-Task4-Commonsense-Validation-and-Explanation/blob/"
           f"{COMMIT}/README.md, section 'License': 'The dataset is distributed under the CC BY-SA 4.0 license.')")
ORDER = ("double_negation", "negation", "units", "numeric", "quantifier", "temporal")

DEFS = {
    "yes": "The asked-about statement is the one of the two that goes against common sense: some part of it makes it "
           "impossible, absurd or clearly contrary to how the world works, while the other statement is normal.",
    "no": "The asked-about statement is the sensible one of the two; it is the other statement that goes against "
          "common sense.",
}


def main():
    rng = random.Random(SEED)
    paths = {n: C.fetch(u, CACHE / n, s) for n, (u, s) in FILES.items()}
    assert "The dataset is distributed under the [CC BY-SA 4.0]" in paths["README.md"].read_text()
    df = pd.read_csv(paths["train.csv"], keep_default_na=False, dtype=str)     # TRAIN ONLY
    assert len(df) == 10000
    recs = []
    for i, r in enumerate(df.itertuples(index=False)):
        good, bad = C.clean(r[0]), C.clean(r[1])
        if len(C.words(good)) < 3 or len(C.words(bad)) < 3 or C.norm(good) == C.norm(bad):
            continue
        recs.append({"rid": f"train_{i:05d}", "good": good, "bad": bad})

    # a statement text may appear in several records (e.g. 'He drinks milk.'): drop every record with a repeated text
    cnt = collections.Counter()
    for r in recs:
        cnt[C.norm(r["good"])] += 1
        cnt[C.norm(r["bad"])] += 1
    n0 = len(recs)
    recs = [r for r in recs if cnt[C.norm(r["good"])] == 1 and cnt[C.norm(r["bad"])] == 1]
    print(f"records={len(df)} usable={n0} after repeated-text drop={len(recs)}")

    hits = C.decon({r["rid"]: [r["good"], r["bad"]] for r in recs})
    print("decon drops:", dict(collections.Counter(hits.values())))
    recs = [r for r in recs if r["rid"] not in hits]

    rng.shuffle(recs)
    pair = recs[:N_PAIR]
    assert len(pair) == N_PAIR, len(pair)
    meta0 = {"dataset": "SemEval-2020 Task 4 ComVE (wangcunxiang/SemEval2020-Task4-Commonsense-Validation-and-"
                        "Explanation)",
             "revision": f"git:{COMMIT}; sha256:{FILES['train.csv'][1]}", "licence": LICENCE, "split": "train",
             "family": C.FAMILY}
    rows = []
    # pairs: random order, asked statement random, exactly half yes
    asks_bad = [True] * (len(pair) // 2) + [False] * (len(pair) - len(pair) // 2)
    rng.shuffle(asks_bad)
    for r, ask_bad in zip(pair, asks_bad):
        bad_first = rng.random() < 0.5
        s1, s2 = (r["bad"], r["good"]) if bad_first else (r["good"], r["bad"])
        bad_n = 1 if bad_first else 2
        n = bad_n if ask_bad else 3 - bad_n
        rows.append({"key": KEY, "rid": r["rid"], "state": f"Statement 1: {s1}\nStatement 2: {s2}",
                     "instructions": f"Of these two statements, does Statement {n} go against common sense?",
                     "options": C.YN, "gold": "yes" if ask_bad else "no", "soft": None,
                     "meta": dict(meta0, config="ALL data/train.csv; subtask A, statement pair",
                                  orig_label={"correct_statement": r["good"], "incorrect_statement": r["bad"],
                                              "incorrect_is_statement": bad_n, "asked_statement": n},
                                  edge=C.edge(r["bad"] + " " + r["good"], ORDER))})
    rng.shuffle(rows)
    out = C.write_outputs(KEY, rows, {None: DEFS})
    s = C.summary(KEY, rows)
    print("wrote", len(rows), "->", out)
    C.show_samples(rows, 6, seed=SEED)
    C.append_manifest({
        "key": KEY, "family": C.FAMILY, "dataset": "SemEval-2020 Task 4 ComVE subtask A (train.csv)",
        "licence": LICENCE, "rows": len(rows), "qtype": "yesno", "yesno_share": s["yes_share"],
        "edge_tags": sorted(t for t in s["edges"] if t),
        "notes": (f"Sense-making: {N_PAIR} ComVE minimal pairs ('of these two statements, does Statement N go against "
                  "common sense?', 50/50). Single-statement framing removed in review (nonsense is only relative to "
                  "the twin: ~6% of lone 'nonsense' statements are sensible). Subtask B reasons rejected as noisy. "
                  "Records with a repeated statement text dropped; decon applied."),
    })


if __name__ == "__main__":
    main()
