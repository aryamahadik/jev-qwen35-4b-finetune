"""REJECTED in review (29 Sep 2026): do not use. main() exits; raw/defs files and the MANIFEST record were deleted.
Reason: gold labels are not clearly right often enough for a golden set. The Social IQa TRAIN split has no human
validation pass (dev/test do; human accuracy ~87%). After this builder's filters, plus two stricter ones tried in review
(names in the question must occur in the context; no same-polarity one/two-word answer sets for feel/describe),
30 fresh gold-side items still held 3 wrong golds ('How would Remy feel?' -> 'a thief'; 'What will Robin want to do
next?' -> a restatement of the context; answers about a person absent from the context) and about 8 where another
answer is equally right (accomplished / successful / tenacious; 'watch tv' / 'enjoy watching the show'). This is
source noise, not a builder bug, and no rule-based filter removes it.

Build golden rows for social_i_qa (Social IQa: commonsense reasoning about social interactions; Sap et al., EMNLP
2019), TRAIN split only.

Source : the official AI2 release zip https://storage.googleapis.com/ai2-mosaic/public/socialiqa/socialiqa-train-dev.zip
         (the URL used by the loader script of HF allenai/social_i_qa @ 8835ceb9141d7896d9d968634a9b21ae440e3ec5),
         members socialiqa-train-dev/train.jsonl + train-labels.lst only (33,410 questions); dev never read.
Licence: CC BY 4.0 -- AI2's official record (allenai.org/data/socialiqa redirects to huggingface.co/datasets/allenai/
         social_i_qa), README.md at that revision, "Licensing Information": "CC-BY-4.0".
Texts  : crowd-written contexts (from ATOMIC event prompts, rewritten with names), questions and answers; wrong answers
         are either handwritten or "question-switching" answers (right for a different question about the same
         context). Human accuracy 86-88%, so the dataset is used at a moderate size and only in framings that show
         all three answers (the annotated decision is "best of three").
Tasks  : one question per context (a context text is used once).
         - yes/no (default defs): 'Is (X) "..." the best answer to the question?' 50% gold.
         - choice (defs qid "choice"): 'Which listed answer best answers the question?' A-C.
         Question types are balanced round-robin: before (what was needed before), next (wants / will do next),
         effect (what happens to someone), feel (reactions), describe (traits), why (motives), other.
Noise  : two record filters (never labels): (1) the gold answer's form cannot answer the question type (adjective
         for 'need to do before' / 'want to do next', bare action for a feeling or trait; spaCy en_core_web_sm 3.8.0
         POS of the first word); (2) the gold is near-identical to a wrong answer (word-Jaccard >= 0.75 or character
         ratio >= 0.85, e.g. "go out with Jordan" / "go out with Jorden"). Audit of 20 rows after filtering: 18
         clearly right, 2 debatable (~10%, as the published human agreement suggests), so the size is kept small
         (2,500 rows).
Dedupe : one row per distinct context; exact duplicate answer sets dropped; decontamination vs forbidden label-NLI
         (incl. defeasible-nli/atomic, which also derives from ATOMIC), local train/dev/eval files, JevBench public.
Edge   : double_negation / negation (context or question), temporal (before / next / after questions),
         implicit (motives, traits and reactions that the context does not state).
Deterministic (seed 20261119).
"""
import collections
import difflib
import io
import json
import random
import re
import sys
import zipfile
from pathlib import Path

import spacy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

KEY = "social_i_qa"
SEED = 20261119
N_YN = 2000
N_CHOICE = 500
HF_REV = "8835ceb9141d7896d9d968634a9b21ae440e3ec5"
SPACY_MODEL_VERSION = "3.8.0"   # en_core_web_sm, used only as a record filter (POS of the gold answer's first word)
ZIP_URL = "https://storage.googleapis.com/ai2-mosaic/public/socialiqa/socialiqa-train-dev.zip"
CACHE = C.HERE / "cache" / KEY
FILES = {
    "socialiqa-train-dev.zip": (ZIP_URL, "ee073914a0fc33265cfbcfc50ec20df9b2e07809c3f420f599138d1f394ef5c3"),
    "README.md": (f"https://huggingface.co/datasets/allenai/social_i_qa/resolve/{HF_REV}/README.md",
                  "8eeeb23c4d993e6a8a50a26677db033dd9977ac275f1cb40d2981b6c9d89b3d1"),
}
LICENCE = (f"CC BY 4.0 (AI2 official record huggingface.co/datasets/allenai/social_i_qa/blob/{HF_REV}/README.md, "
           "'Licensing Information: CC-BY-4.0'; allenai.org/data/socialiqa redirects to this card)")
LET = C.letters(3)
DEFS = {
    "yes": "The named answer is the most plausible of the listed answers to the question as asked: about the person "
           "the question names and the moment it asks about (what was needed before, what happens or is wanted next, "
           "why, how someone feels or would be described), given everyday social commonsense.",
    "no": "Another listed answer fits better: the named answer is unlikely, is about a different person than the one "
          "asked about, answers a different kind of question (for example a feeling when the question asks what "
          "happens next, or a later step when it asks what was needed before), or is less plausible.",
}
DEFS_CHOICE = {L: f"Answer ({L}) is the most plausible listed answer to the question as asked: about the person it "
                  f"names and the moment it asks about (before, next, why, feelings, traits), given everyday social "
                  f"commonsense." for L in LET}
QTYPES = [("feel", re.compile(r"\bfeel\b", re.I)),          # first: 'How would X feel afterwards?' is a feeling
          ("describe", re.compile(r"\bdescribe\b|\bkind of person\b", re.I)),
          ("before", re.compile(r"\bbefore\b|\bbeforehand\b", re.I)),
          ("next", re.compile(r"\bnext\b|\bafter\b|\bafterwards?\b|\bwant to do\b", re.I)),
          ("effect", re.compile(r"\bhappen to\b", re.I)),
          ("why", re.compile(r"^\s*why\b", re.I))]


def qtype(q):
    for name, pat in QTYPES:
        if pat.search(q):
            return name
    return "other"


def form_mismatch(qt, doc):
    """Gold answer whose form cannot answer the question type (a known Social IQa noise pattern): an adjective as
    what someone needs to do before / wants to do next ('smart', 'fully charged'), or a bare action as a feeling or
    trait ('stretch their body', 'get things done'). spaCy is used only to filter records, never to label."""
    toks = [t for t in doc if not t.is_punct]
    if toks and toks[0].lower_ == "to" and len(toks) > 1:
        toks = toks[1:]
    if not toks:
        return True
    ft = toks[0].tag_
    if qt in ("before", "next") and (ft == "JJ" or (len(toks) <= 2 and ft in ("VBN", "JJ", "RB"))):
        return True
    if qt in ("feel", "describe") and ft == "VB" and len(toks) >= 2 and toks[0].lower_ not in ("feel", "be", "like"):
        return True
    return False


def near_identical(a, b):
    wa, wb = set(C.words(a)), set(C.words(b))
    return (len(wa & wb) / max(1, len(wa | wb)) >= 0.75
            or difflib.SequenceMatcher(None, C.norm(a), C.norm(b)).ratio() >= 0.85)


def edge(r):
    t = r["ctx"] + " " + r["q"]
    if C.is_double_negation(t):
        return "double_negation"
    if C.neg_count(t):
        return "negation"
    if r["qt"] in ("before", "next", "effect"):
        return "temporal"
    if r["qt"] in ("why", "describe", "feel"):
        return "implicit"
    return None


def main():
    sys.exit("social_i_qa was REJECTED in review (29 Sep 2026): gold labels too noisy for a golden set (see docstring)")
    rng = random.Random(SEED)
    paths = {n: C.fetch(u, CACHE / n, s) for n, (u, s) in FILES.items()}
    assert "CC-BY-4.0" in paths["README.md"].read_text()
    z = zipfile.ZipFile(paths["socialiqa-train-dev.zip"])
    data = [json.loads(l) for l in io.TextIOWrapper(z.open("socialiqa-train-dev/train.jsonl"), encoding="utf-8")
            if l.strip()]
    labels = [l.strip() for l in io.TextIOWrapper(z.open("socialiqa-train-dev/train-labels.lst"), encoding="utf-8")
              if l.strip()]
    assert len(data) == len(labels) == 33410
    cnt_ctx = collections.Counter(C.norm(d["context"]) for d in data)
    recs, seen = [], set()
    for i, (d, lab) in enumerate(zip(data, labels)):
        ctx, q = C.clean(d["context"]), C.clean(d["question"])
        ans = [C.clean(d["answerA"]), C.clean(d["answerB"]), C.clean(d["answerC"])]
        gi = int(lab) - 1
        if not all(ans) or len({C.norm(a) for a in ans}) < 3 or len(C.words(ctx)) < 4:
            continue
        k = C.norm(ctx)
        if k in seen:          # one question per context
            continue
        seen.add(k)
        recs.append({"rid": f"train_{i:05d}", "ctx": ctx, "q": q, "ans": ans, "gi": gi, "qt": qtype(q)})
    print(f"records={len(data)} usable (one per context)={len(recs)}; contexts with >1 question: "
          f"{sum(v > 1 for v in cnt_ctx.values())}")
    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser", "lemmatizer"])
    assert nlp.meta["version"] == SPACY_MODEL_VERSION, nlp.meta["version"]
    docs = nlp.pipe([r["ans"][r["gi"]] for r in recs], batch_size=512)
    drop = collections.Counter()
    kept = []
    for r, doc in zip(recs, docs):
        if form_mismatch(r["qt"], doc):
            drop["gold form does not fit question type"] += 1
            continue
        g = r["ans"][r["gi"]]
        if any(near_identical(g, a) for j, a in enumerate(r["ans"]) if j != r["gi"]):
            drop["gold near-identical to a wrong answer"] += 1
            continue
        kept.append(r)
    recs = kept
    print("noise filters:", dict(drop), "kept", len(recs))
    hits = C.decon({r["rid"]: [r["ctx"], r["ctx"] + " " + r["q"]] for r in recs})
    print("decon drops:", dict(collections.Counter(hits.values())))
    recs = [r for r in recs if r["rid"] not in hits]

    rng.shuffle(recs)
    pools = collections.defaultdict(list)
    for r in recs:
        pools[r["qt"]].append(r)
    print("question types available:", {k: len(v) for k, v in sorted(pools.items())})
    order, sel, i = sorted(pools), [], 0
    while len(sel) < N_YN + N_CHOICE and any(pools.values()):
        k = order[i % len(order)]
        if pools[k]:
            sel.append(pools[k].pop())
        i += 1
    rng.shuffle(sel)

    meta0 = {"dataset": "Social IQa (allenai/social_i_qa; official zip socialiqa-train-dev.zip)",
             "config": "train.jsonl + train-labels.lst",
             "revision": f"hf:{HF_REV} loader URL; sha256:{FILES['socialiqa-train-dev.zip'][1]}",
             "licence": LICENCE, "split": "train", "family": C.FAMILY}

    def state(r):
        a = "\n".join(f"({L}) {t}" for L, t in zip(LET, r["ans"]))
        return f"Context: {r['ctx']}\nQuestion: {r['q']}\nAnswers:\n{a}"

    rows = []
    yn, ch = sel[:N_YN], sel[N_YN:]
    flags = [True] * (len(yn) // 2) + [False] * (len(yn) - len(yn) // 2)
    rng.shuffle(flags)
    for r, ask_gold in zip(yn, flags):
        ai = r["gi"] if ask_gold else rng.choice([j for j in range(3) if j != r["gi"]])
        rows.append({"key": KEY, "rid": r["rid"], "state": state(r),
                     "instructions": f'Is ({LET[ai]}) "{r["ans"][ai]}" the best answer to the question?',
                     "options": C.YN, "gold": "yes" if ask_gold else "no", "soft": None,
                     "meta": dict(meta0, orig_label={"label": r["gi"] + 1, "question_type": r["qt"],
                                                     "asked": LET[ai]}, edge=edge(r))})
    for r in ch:
        rows.append({"key": KEY, "rid": r["rid"], "state": state(r),
                     "instructions": "Which listed answer best answers the question?",
                     "options": LET, "gold": LET[r["gi"]], "soft": None,
                     "meta": dict(meta0, defs="choice", orig_label={"label": r["gi"] + 1, "question_type": r["qt"]},
                                  edge=edge(r))})
    rng.shuffle(rows)
    out = C.write_outputs(KEY, rows, {None: DEFS, "choice": DEFS_CHOICE})
    s = C.summary(KEY, rows)
    print("question types used:", dict(collections.Counter(r["meta"]["orig_label"]["question_type"] for r in rows)))
    print("wrote", len(rows), "->", out)
    C.show_samples(rows, 6, seed=SEED)
    C.append_manifest({
        "key": KEY, "family": C.FAMILY, "dataset": "Social IQa (AI2 official zip, train)", "licence": LICENCE,
        "rows": len(rows), "qtype": "yesno+choice", "yesno_share": s["yes_share"],
        "edge_tags": sorted(t for t in s["edges"] if t),
        "notes": (f"Social commonsense (motives, reactions, needs before, wants next). {s['n_yn']} yes/no 'is (X) the "
                  f"best of the three answers' + {s['n_ch']} 3-way letter choice (defs qid 'choice'); question types "
                  f"balanced round-robin; one question per context. Noise filters (answer form vs question type; near-"
                  f"identical answers). Noisiest set here (~10% debatable on a 20-row audit, human accuracy ~87%): "
                  f"kept small; consider down-weighting."),
    })


if __name__ == "__main__":
    main()
