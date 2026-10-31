"""Build golden rows for quartz (QuaRTz: open-domain qualitative relationships; Tafjord et al., EMNLP 2019), TRAIN only.

Source : HF allenai/quartz (AI2's official record: allenai.org/data/quartz redirects to it),
         data/train-00000-of-00001.parquet at revision 28c1dbb56caf81799296cb17892fa73402e23464 (2,696 questions).
         validation/test never read.
Licence: CC BY 4.0 -- dataset card README.md at that revision, "Licensing Information": "The dataset is licensed under
         Creative Commons Attribution 4.0 International (CC BY 4.0)." (and `license: cc-by-4.0` in the metadata).
Texts  : 400 single qualitative science sentences extracted by the authors ("para") + crowd-written situated 2-way
         questions, each validated by a second worker; poor ones reviewed by the authors (human accuracy 95%).
Task   : yes/no only. The background sentence, the question and its two choices are shown; "According to the
         background statement, is (X) "..." the correct answer?" 50% asked about the gold choice, 50% about the other.
         Many paras carry twin questions whose answer flips with the direction of the comparison (kept; the state
         differs; meta.twin_of links an original and its '-flip' question, added in review 29 Sep 2026). Trailing residue on a choice text ('?', ',', ' or') is stripped (formatting only).
Dedupe : exact normalised question+choices; decontamination vs forbidden label-NLI (quarel is a different dataset and
         its texts are checked here too), local train/dev/eval files and JevBench public.
Edge   : double_negation / negation / units / numeric / quantifier cues of the question.
Deterministic (seed 20261117).
"""
import collections
import random
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

KEY = "quartz"
SEED = 20261117
REV = "28c1dbb56caf81799296cb17892fa73402e23464"
CACHE = C.HERE / "cache" / KEY
FILES = {
    "train.parquet": (f"https://huggingface.co/datasets/allenai/quartz/resolve/{REV}/data/train-00000-of-00001.parquet",
                      "edeb1fa716d945ee198c9f5ce5ab6cad4d847e714ff7463834dee422c8450035"),
    "README.md": (f"https://huggingface.co/datasets/allenai/quartz/resolve/{REV}/README.md",
                  "0a7279210dc1c2310f5f0972d09058423c81a051a4fab8fbf8255e3be66ebb67"),
}
LICENCE = (f"CC BY 4.0 (huggingface.co/datasets/allenai/quartz/blob/{REV}/README.md, 'Licensing Information': 'The "
           "dataset is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).'; "
           "allenai.org/data/quartz redirects to this card)")
DEFS = {
    "yes": "Applying the qualitative relationship stated in the background (as one property goes up or down, another "
           "goes up or down) to the situations compared in the question gives the named choice.",
    "no": "Applying the background relationship gives the other choice: the named choice gets the direction of the "
          "effect backwards (for example more instead of less, or higher instead of lower).",
}


def main():
    rng = random.Random(SEED)
    paths = {n: C.fetch(u, CACHE / n, s) for n, (u, s) in FILES.items()}
    assert "Creative Commons [Attribution 4.0 International (CC BY 4.0)]" in paths["README.md"].read_text()
    df = pd.read_parquet(paths["train.parquet"])          # TRAIN ONLY
    assert len(df) == 2696
    recs, seen = [], set()
    for r in df.itertuples(index=False):
        ch = [re.sub(r"(\s+or|[?,;])+$", "", C.clean(t)).strip() for t in r.choices["text"]]
        labs = list(r.choices["label"])
        if labs != ["A", "B"] or r.answerKey not in labs or C.norm(ch[0]) == C.norm(ch[1]) or not all(ch):
            continue
        k = C.norm(r.question + " " + " ".join(ch))
        if k in seen:
            continue
        seen.add(k)
        recs.append({"rid": r.id, "para": C.clean(r.para), "q": C.clean(r.question), "ch": ch,
                     "gi": labs.index(r.answerKey)})
    print(f"records={len(df)} usable={len(recs)}")
    hits = C.decon({r["rid"]: [r["para"] + " " + r["q"], r["q"]] for r in recs})
    print("decon drops:", dict(collections.Counter(hits.values())))
    recs = [r for r in recs if r["rid"] not in hits]

    recs.sort(key=lambda r: r["rid"])
    rng.shuffle(recs)
    flags = [True] * (len(recs) // 2) + [False] * (len(recs) - len(recs) // 2)
    rng.shuffle(flags)
    rids = {r["rid"] for r in recs}

    def twin(rid):   # QuaRTz 'flip' questions invert the comparison of the original question (answer flips)
        t = rid[:-5] if rid.endswith("-flip") else rid + "-flip"
        return t if t in rids else None

    rows = []
    for r, ask_gold in zip(recs, flags):
        ai = r["gi"] if ask_gold else 1 - r["gi"]
        L = "AB"[ai]
        state = (f"Background: {r['para']}\n\nQuestion: {r['q']}\nChoices: (A) {r['ch'][0]}  (B) {r['ch'][1]}")
        rows.append({"key": KEY, "rid": r["rid"], "state": state,
                     "instructions": f'According to the background statement, is ({L}) "{r["ch"][ai]}" the correct '
                                     f'answer to the question?',
                     "options": C.YN, "gold": "yes" if ask_gold else "no", "soft": None,
                     "meta": {"dataset": "allenai/quartz", "config": "default",
                              "revision": f"hf:{REV}; sha256:{FILES['train.parquet'][1]}", "licence": LICENCE,
                              "split": "train",
                              "orig_label": {"answerKey": "AB"[r["gi"]], "asked": L},
                              "family": C.FAMILY, "twin_of": twin(r["rid"]),
                              "edge": C.edge(r["q"] + " " + " ".join(r["ch"]),
                                             ("double_negation", "negation", "units", "numeric", "quantifier"))}})
    rng.shuffle(rows)
    out = C.write_outputs(KEY, rows, {None: DEFS})
    s = C.summary(KEY, rows)
    print("wrote", len(rows), "->", out)
    C.show_samples(rows, 5, seed=SEED)
    C.append_manifest({
        "key": KEY, "family": C.FAMILY, "dataset": "allenai/quartz (train)", "licence": LICENCE, "rows": len(rows),
        "qtype": "yesno", "yesno_share": s["yes_share"], "edge_tags": sorted(t for t in s["edges"] if t),
        "notes": ("Qualitative science relationships applied to situations (direction of effect, comparisons), with "
                  "the background sentence shown as evidence. Yes/no 'is (X) the correct answer', 50/50. Twin "
                  "questions with flipped comparisons kept."),
    })


if __name__ == "__main__":
    main()
