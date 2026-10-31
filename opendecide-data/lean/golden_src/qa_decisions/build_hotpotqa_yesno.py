"""Build golden rows for hotpotqa_yesno (HotpotQA yes/no comparison questions; Yang et al., EMNLP 2018), TRAIN only.

Source : HF hotpotqa/hotpot_qa, config distractor, train-0000{0,1}-of-00002.parquet at revision
         1908d6afbbead072334abe2965f91bd2709910ab (90,447 questions; a parquet copy of the official
         hotpot_train_v1.1.json). validation never read.
Licence: CC BY-SA 4.0 -- official site https://hotpotqa.github.io/ : "HotpotQA is distributed under a CC BY-SA 4.0
         License." (the HF card metadata also says cc-by-sa-4.0).
Texts  : crowd-written multi-hop questions over pairs of Wikipedia first paragraphs (human answers and human-marked
         supporting sentences). Only the native yes/no answers are used (5,481 comparison questions, ~50/50):
         "Are X and Y both ...?", "Were A and B from the same country?", "Do both ... have the same number of acts?".
         This is the implicit multi-hop yes/no slot (StrategyQA is in the forbidden label-NLI set).
Task   : yes/no, the instruction is the original question (whitespace/capitalisation tidy only). The state holds the two
         gold paragraphs (full, with titles); for 40% of rows two of the question's own TF-IDF distractor paragraphs are
         added and the order shuffled (tests picking the right evidence). States are capped at 3,600 characters
         (distractors dropped first; gold paragraphs trimmed after their last supporting sentence; else skipped).
Review : (29 Sep 2026) the 'no' definition now says what the question writers applied: 'no' also when a paragraph
         does not describe an entity as having the property (e.g. 'Have both X and Y been listed in Forbes?' with Forbes
         named for one only). Questions about the paragraphs themselves ('Is the Mental Floss paragraph related to the
         Dr. Dobb's Journal paragraph?') are dropped. orig_label.type is the source question type (was hard-coded).
Dedupe : one row per distinct question; decontamination per paragraph vs forbidden label-NLI (e.g. wiki_qa, FEVER-
         related), local train/dev/eval files and JevBench public: a contaminated distractor is simply left out, a
         contaminated question or gold paragraph drops the record. (Held-out OHS files are handled at compile time.)
Edge   : negation > numeric > temporal > quantifier (question cues) > long_context (distractors added) > multi_hop.
Deterministic (seed 20261120).
"""
import collections
import random
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

KEY = "hotpotqa_yesno"
SEED = 20261120
REV = "1908d6afbbead072334abe2965f91bd2709910ab"
CACHE = C.HERE / "cache" / KEY
FILES = {
    "train-00000.parquet": (f"https://huggingface.co/datasets/hotpotqa/hotpot_qa/resolve/{REV}/distractor/"
                            "train-00000-of-00002.parquet",
                            "76d3bb3048a7cc73c1958107c0c5872a00d7e7d00c105b81e92f6769e7822e68"),
    "train-00001.parquet": (f"https://huggingface.co/datasets/hotpotqa/hotpot_qa/resolve/{REV}/distractor/"
                            "train-00001-of-00002.parquet",
                            "713661628434fbb19fff7392e2e321e4ed107e3c7c7784d0690946e5f722763f"),
}
LICENCE = "CC BY-SA 4.0 (https://hotpotqa.github.io/ : 'HotpotQA is distributed under a CC BY-SA 4.0 License.')"
MAX_CHARS = 3600
P_DISTRACT = 0.40
DEFS = {
    "yes": "Read together, the paragraphs show the answer is yes: what the question asks holds for every entity it "
           "names (for 'both' questions both have the property, for 'same' questions the two values match, for a "
           "comparison the stated order is right).",
    "no": "The paragraphs do not bear out a yes: at least one named entity lacks the property or is not described "
          "as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about "
          "other topics are distractors and do not decide the answer.",
}
Q_NUM = re.compile(r"\d|\bnumber\b|\bhow many\b|\bpopulation\b|\bmore\b|\bless\b|\bfewer\b|\btaller\b|\bheight\b|"
                   r"\blarger\b|\bbigger\b|\bsmaller\b|\bhigher\b|\blower\b|\blonger\b|\bshorter\b", re.I)
Q_TEMP = re.compile(r"\byears?\b|\bborn\b|\bfounded\b|\bestablished\b|\bsame time\b|\bolder\b|\byounger\b|"
                    r"\bcentury\b|\bdecade\b|\bdate\b|\breleased\b|\bearlier\b|\blater\b|\bfirst\b|\bbefore\b|"
                    r"\bafter\b|\balive\b|\bdied\b|\bera\b|\bperiod\b", re.I)
META_Q = re.compile(r"\b(paragraphs?|passages?)\b", re.I)
Q_QUANT = re.compile(r"\bboth\b|\beither\b|\bneither\b|\ball\b|\beach\b|\bonly\b", re.I)


def tidy_q(q):
    q = C.clean(q)
    q = re.sub(r"\s+([?.,!])", r"\1", q)
    return q[:1].upper() + q[1:]


def para_text(title, sents):
    body = " ".join(C.clean(s) for s in sents if C.clean(s))
    return f"{C.clean(title)}\n{body}"


def edge(q, n_distract):
    if C.is_double_negation(q):
        return "double_negation"
    if C.neg_count(q):
        return "negation"
    if Q_NUM.search(q):
        return "numeric"
    if Q_TEMP.search(q):
        return "temporal"
    if Q_QUANT.search(q):
        return "quantifier"
    if n_distract:
        return "long_context"
    return "multi_hop"


def main():
    rng = random.Random(SEED)
    paths = {n: C.fetch(u, CACHE / n, s) for n, (u, s) in FILES.items()}
    df = pd.concat([pd.read_parquet(paths[n]) for n in sorted(paths)], ignore_index=True)   # TRAIN ONLY
    assert len(df) == 90447
    yn = df[df.answer.str.strip().str.lower().isin(["yes", "no"])]
    print(f"train questions={len(df)} yes/no={len(yn)} types={dict(yn.type.value_counts())}")
    recs, seen = [], set()
    for r in yn.itertuples(index=False):
        q = tidy_q(r.question)
        nq = C.norm(q)
        if nq in seen or len(C.words(q)) < 4:
            continue
        if META_Q.search(q):       # questions about the paragraphs themselves ('Is the X paragraph related to ...')
            continue
        seen.add(nq)
        ctx = {C.clean(t): list(s) for t, s in zip(r.context["title"], r.context["sentences"])}
        sup = collections.defaultdict(set)
        for t, i in zip(r.supporting_facts["title"], r.supporting_facts["sent_id"]):
            sup[C.clean(t)].add(int(i))
        gold_titles = sorted(sup)
        if len(gold_titles) != 2 or any(t not in ctx for t in gold_titles):
            continue
        if any(max(sup[t]) >= len(ctx[t]) for t in gold_titles):
            continue
        recs.append({"rid": r.id, "q": q, "ans": r.answer.strip().lower(), "level": r.level, "type": r.type, "ctx": ctx,
                     "sup": {t: sorted(v) for t, v in sup.items()}, "gold": gold_titles})
    print(f"usable (distinct questions, 2 gold paragraphs present)={len(recs)}")

    # per-paragraph decontamination
    core = {}
    for r in recs:
        core[f"{r['rid']}|Q"] = [r["q"]]
        for t, s in r["ctx"].items():
            core[f"{r['rid']}|{t}"] = [para_text(t, s)]
    hits = C.decon(core)
    bad = collections.defaultdict(set)
    for k in hits:
        rid, part = k.split("|", 1)
        bad[rid].add(part)
    drop = collections.Counter()
    kept = []
    for r in recs:
        b = bad.get(r["rid"], set())
        if "Q" in b or any(t in b for t in r["gold"]):
            drop["question or gold paragraph overlaps"] += 1
            continue
        r["distractors"] = sorted(t for t in r["ctx"] if t not in r["gold"] and t not in b)
        kept.append(r)
    recs = kept
    print("decon:", dict(drop), "| hit sources:", dict(collections.Counter(hits.values())))

    recs.sort(key=lambda r: r["rid"])
    rng.shuffle(recs)
    rows, skipped = [], collections.Counter()
    for r in recs:
        golds = {t: r["ctx"][t] for t in r["gold"]}
        paras = [para_text(t, s) for t, s in golds.items()]
        if sum(map(len, paras)) > MAX_CHARS:     # trim after the last supporting sentence
            paras = [para_text(t, s[:max(r["sup"][t]) + 1]) for t, s in golds.items()]
        if sum(map(len, paras)) + 2 * len(paras) > MAX_CHARS:
            skipped["too long"] += 1
            continue
        extra = []
        if rng.random() < P_DISTRACT and len(r["distractors"]) >= 2:
            for t in rng.sample(r["distractors"], 2):
                p = para_text(t, r["ctx"][t])
                if sum(map(len, paras + extra)) + len(p) + 2 * (len(paras) + len(extra) + 1) <= MAX_CHARS:
                    extra.append(p)
        allp = paras + extra
        rng.shuffle(allp)
        state = "\n\n".join(allp)
        rows.append({"key": KEY, "rid": r["rid"], "state": state, "instructions": r["q"], "options": C.YN,
                     "gold": r["ans"], "soft": None,
                     "meta": {"dataset": "hotpotqa/hotpot_qa (HotpotQA, distractor setting)", "config": "distractor",
                              "revision": f"hf:{REV}; sha256:{FILES['train-00000.parquet'][1]},"
                                          f"{FILES['train-00001.parquet'][1]}",
                              "licence": LICENCE, "split": "train",
                              "orig_label": {"answer": r["ans"], "type": r["type"], "level": r["level"],
                                             "supporting_titles": r["gold"], "n_distractor_paragraphs": len(extra)},
                              "family": C.FAMILY, "edge": edge(r["q"], len(extra))}})
    print("skipped:", dict(skipped))
    # dedupe states (paranoia) and keep yes share in range
    seen_s, out_rows = set(), []
    for x in rows:
        k = C.norm(x["state"])
        if k in seen_s:
            continue
        seen_s.add(k)
        out_rows.append(x)
    rows = out_rows
    out = C.write_outputs(KEY, rows, {None: DEFS})
    s = C.summary(KEY, rows)
    print("levels:", dict(collections.Counter(x["meta"]["orig_label"]["level"] for x in rows)))
    print("wrote", len(rows), "->", out)
    C.show_samples(rows, 5, seed=SEED)
    C.append_manifest({
        "key": KEY, "family": C.FAMILY, "dataset": "HotpotQA (hotpotqa/hotpot_qa distractor train), yes/no subset",
        "licence": LICENCE, "rows": len(rows), "qtype": "yesno", "yesno_share": s["yes_share"],
        "edge_tags": sorted(t for t in s["edges"] if t),
        "notes": ("Native human yes/no multi-hop comparison questions answered from two Wikipedia paragraphs (evidence "
                  "shown); 40% with two distractor paragraphs. Replaces StrategyQA (forbidden). Per-paragraph decon; "
                  "OHS decon (Wikipedia sentences shared with VitaminC/FEVER) must be applied at compile time."),
    })


if __name__ == "__main__":
    main()
