"""Build raw rows for spiced (SPICED: Scientific Paraphrase and Information ChangE Dataset; Wright, Pei, Jurgens &
Augenstein, EMNLP 2022, arXiv:2210.13001).

Source : HF copenlu/spiced pinned to revision 832c456f4ce1012b301a458b7e468f096ec76e88, file train.csv ONLY
         (dev.csv / test.csv never downloaded).
Licence: MIT (dataset card of copenlu/spiced, the authors' own org, 'license: mit'; the code repo
         github.com/copenlu/scientific-information-change is also MIT).
Texts  : a finding sentence from a scientific paper (S2ORC full text; CS, medicine, biology, psychology) paired with a
         finding sentence from a news article or a tweet that cites the paper (via Altmetric). Human-written.
Labels : Information Matching Score (IMS), 1-5 Likert, "The information in the findings is (1) completely different,
         (2) mostly different, (3) somewhat similar, (4) mostly the same, (5) completely the same"; expert Prolific
         annotators (3-5 per pair, low-competence annotators removed); final_score = mean.
         Rows whose instance_id contains 'easy' were labelled AUTOMATICALLY by SBERT similarity thresholds -> DROPPED.
Question: "Do the two passages report the same scientific finding?"  yes = IMS mostly/completely the same,
         no = mostly/completely different. The ambiguous middle ('somewhat similar') is dropped.
Keep rule: yes if final_score >= 3.75 and P(yes) >= 0.7; no if final_score <= 2.0 and P(no) >= 0.7, where over the
         individual ratings P(yes) = (#ratings>=4 + 0.5*#ratings==3)/n and P(no) = 1 - P(yes). soft = {yes, no} from
         these real annotator shares.
Dedupe : exact paper+news pair, near-duplicate states (word Jaccard >= 0.85); decontamination against label-NLI
         (incl. scientific-exaggeration-detection), local train/dev/eval files and JevBench public.
Review fix (strict reviewer, 29 Sep): findings that are extraction debris rather than a sentence (fewer than 4
         word tokens, or under 35% word tokens, e.g. '***p < 0.0001; **p < 0.01', '22.97, all p , 0.001), rare
         clean-shaven (all t 548 !', hashtag-only tweets) are dropped.
Deterministic (seed 20261115). CPU only.
"""
import ast
import collections
import random
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _shc_common as C  # noqa: E402

KEY = "spiced"
SEED = 20261115
REV = "832c456f4ce1012b301a458b7e468f096ec76e88"
URL = f"https://huggingface.co/datasets/copenlu/spiced/resolve/{REV}/"
FILES = {"train.csv": "383c61973d66100e5b1e501535c8afaf6f3d64f044fd3280d808c6c46d5b774c",
         "README.md": "faeffc5fed34f6ce165dafed110fe6ac3f41e3a1d2217489e86a946f6b782d96"}
LICENCE = f"MIT (dataset card https://huggingface.co/datasets/copenlu/spiced/blob/{REV}/README.md 'license: mit')"
DATASET = "copenlu/spiced (SPICED)"
QUESTION = "Do the two passages report the same scientific finding?"
DEFS = {
    "yes": "The information in the two findings is mostly or completely the same: the same result, relationship "
           "(direction, variables, population) and conclusion, even if the news or tweet uses plainer words, drops "
           "technical detail or adds framing such as 'researchers found'.",
    "no": "The information in the two findings is mostly or completely different: they report different results, "
          "variables or conclusions, or one passage only touches the same topic or study without stating the other "
          "passage's finding.",
}
YES_MIN, NO_MAX, AGREE = 3.75, 2.0, 0.7


def sentence_like(t):
    toks = t.split()
    wordy = sum(bool(re.fullmatch(r"[A-Za-z][A-Za-z'-]*[.,;:!?\"')]*", x)) for x in toks)
    return wordy >= 4 and wordy / max(1, len(toks)) >= 0.35


def main():
    rng = random.Random(SEED)
    cache = C.CACHE / KEY
    paths = {f: C.fetch(URL + f, cache / f, sha) for f, sha in FILES.items()}
    df = pd.read_csv(paths["train.csv"], keep_default_na=False)
    assert set(df["split"]) == {"train"}
    stats = collections.Counter()
    stats["all"] = len(df)
    df = df[~df["instance_id"].str.contains("easy")]
    stats["manual"] = len(df)

    cands = []
    for rec in df.to_dict("records"):
        scores = [float(x) for x in ast.literal_eval(rec["scores"])]
        n = len(scores)
        if n < 3:
            stats["drop_few_raters"] += 1
            continue
        p_yes = (sum(s >= 4 for s in scores) + 0.5 * sum(s == 3 for s in scores)) / n
        fs = float(rec["final_score"])
        if fs >= YES_MIN and p_yes >= AGREE:
            gold = "yes"
        elif fs <= NO_MAX and 1 - p_yes >= AGREE:
            gold = "no"
        else:
            stats["drop_middle_or_disagree"] += 1
            continue
        paper = C.clean(rec["Paper Finding"])
        news = C.clean(rec["News Finding"])
        if len(paper) < 30 or len(news) < 20:
            stats["drop_short"] += 1
            continue
        if not (sentence_like(paper) and sentence_like(news)):
            stats["drop_debris"] += 1
            continue
        src = rec["source"]
        label2 = "a news article" if src == "news" else "a tweet"
        state = (f"Finding in the scientific paper:\n{paper}\n\n"
                 f"Finding as reported in {label2}:\n{news}")
        cands.append({"rid": rec["instance_id"], "state": state, "paper": paper, "news": news, "gold": gold,
                      "soft": {"yes": round(p_yes, 4), "no": round(1 - p_yes, 4)}, "scores": scores, "fs": fs,
                      "field": rec["field"], "source": src, "doi": rec["DOI"]})
    stats["kept_clear"] = len(cands)

    hits = C.decon({c["rid"]: [c["paper"], c["news"]] for c in cands}, cache_name=KEY)
    cands = [c for c in cands if c["rid"] not in hits]
    cands.sort(key=lambda c: c["rid"])
    rng.shuffle(cands)
    cands = C.near_dup_filter(cands, lambda c: c["state"], thresh=0.85)

    yes = [c for c in cands if c["gold"] == "yes"]
    no = [c for c in cands if c["gold"] == "no"]
    yes, no = C.balance_yes(yes, no, rng, lo=0.42, hi=0.58)
    rows = []
    for c in yes + no:
        e = C.edge(c["news"] + " " + c["paper"], order=("negation", "units", "numeric", "quantifier"))
        if c["source"] == "tweet" and e is None:
            e = "implicit"
        rows.append({
            "key": KEY, "rid": c["rid"], "state": c["state"], "instructions": QUESTION, "options": C.YN,
            "gold": c["gold"], "soft": c["soft"],
            "meta": {"dataset": DATASET, "config": "train.csv (manually annotated pairs only)",
                     "revision": f"hf:{REV}; sha256:{FILES['train.csv']}", "licence": LICENCE, "split": "train",
                     "orig_label": {"final_score": c["fs"], "scores": c["scores"], "field": c["field"],
                                    "source": c["source"], "doi": c["doi"]},
                     "family": C.FAMILY, "edge": e},
        })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, {None: DEFS})
    st = C.summary(KEY, rows)
    print("stats:", dict(stats), "| decon hits:", len(hits))
    print("fields:", dict(collections.Counter(r["meta"]["orig_label"]["field"] for r in rows)),
          "sources:", dict(collections.Counter(r["meta"]["orig_label"]["source"] for r in rows)))
    print("mean soft of gold: %.3f" % (sum(r["soft"][r["gold"]] for r in rows) / len(rows)))
    C.show_samples(rows, n=5, seed=5)
    C.append_manifest(C.manifest_record(
        KEY, DATASET + ", train split, manually annotated pairs only", LICENCE, rows, "yesno",
        "Paper finding vs news/tweet finding: same scientific finding? Expert IMS ratings (1-5); only clear pairs "
        "(mean >= 3.75 or <= 2.0 with >= 70% rater agreement); SBERT-auto-labelled 'easy' pairs dropped; soft = real "
        "rater shares; extraction-debris findings dropped.", st))


if __name__ == "__main__":
    main()
