"""Build raw rows for answer_equiv: can a candidate answer replace the reference answer? (Answer Equivalence dataset;
Bulian et al. 2022, "Tomayto, Tomahto. Beyond Token-level Answer Equivalence for Question Answering Evaluation").

Source : GitHub google-research-datasets/answer-equivalence-dataset pinned to commit
         5032298f3fe69bebab4a013de5606231a948cebc, v1/train.jsonl ONLY (ae_dev / ae_test / dev_by_system never read).
Licence: Apache-2.0 (repo LICENSE at the pinned commit). Passages and questions are SQuAD 1.1 (Wikipedia, CC BY-SA 4.0).
Texts  : SQuAD train questions + Wikipedia passages; the candidate answers are spans predicted by ALBERT models trained
         on the other 80% of SQuAD train (non-exact-match predictions only) - the objects being judged.
Labels : HUMAN rating (one rater per train example) with the paper's sequential questions: Q1 "Is the second answer a
         completely different answer?"; Q2 "Would using the second answer in place of the first answer convey at
         least the same information to someone asking this question, without leaving out any important information
         nor adding any misleading or superfluous information?" Equivalent = Q1 no and Q2 yes; otherwise not equivalent
         (completely different, or information removed / misleading or superfluous information added).
Rows   : two framings (qids): 'equiv' (Q2 as asked) and 'notequiv' (negated: unacceptable substitute?). Each passage
         is used for at most one row (SQuAD passages carry several questions), so states never repeat a passage.
Filters: decontamination (question + passage) against label-NLI, all local train/dev/eval files (drops passages that
         reach our data through QNLI, which is built from SQuAD) and JevBench; cross-check with other v14 parts;
         yes share kept in 45-55% per framing.
Deterministic (seed 20261206). CPU only.
"""
import collections
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _jv_common as C  # noqa: E402

KEY = "answer_equiv"
SEED = 20261206
COMMIT = "5032298f3fe69bebab4a013de5606231a948cebc"
BASE = f"https://raw.githubusercontent.com/google-research-datasets/answer-equivalence-dataset/{COMMIT}/"
FILES = {"v1/train.jsonl": "431c524a00800da114685b89b0066969284f6b947383e42bde9fd724ba57f9e3", "LICENSE": "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30", "README.md": "b855d8204af8e681ae366c326f94400722839ebcf0c81f2c18ab59cc8b5a4a7c"}
LICENCE = (f"Apache-2.0 (https://github.com/google-research-datasets/answer-equivalence-dataset/blob/{COMMIT}/LICENSE); "
           "passages/questions from SQuAD 1.1 (CC BY-SA 4.0)")
DATASET = "google-research-datasets/answer-equivalence-dataset (AE v1 train)"
TARGET = 6000

Q = {
    "equiv": "Can the candidate answer be used in place of the reference answer, conveying at least the same information "
             "for this question without leaving out anything important or adding misleading or superfluous information?",
    "notequiv": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different "
                "answer, leaves out important information, or adds misleading or superfluous information?",
}
_EQ = ("Acceptable substitute: given the question and passage, the candidate conveys at least the same information as "
       "the reference (differences in wording, extra relevant detail, or dropping irrelevant or misleading parts are "
       "fine) and adds nothing misleading or superfluous.")
_NE = ("Not an acceptable substitute: the candidate is a different answer, or it leaves out important information from "
       "the reference (e.g. 'June' for 'every June', a partial name or number), or adds misleading or superfluous "
       "information.")
DEFS = {"equiv": {"yes": _EQ, "no": _NE}, "notequiv": {"yes": _NE, "no": _EQ}}


def main():
    rng = random.Random(SEED)
    cache = C.CACHE / "answer_equiv"
    paths = {rel: C.fetch(BASE + rel, cache / Path(rel).name, sha) for rel, sha in FILES.items()}
    stats = collections.Counter()
    recs = []
    for i, l in enumerate(open(paths["v1/train.jsonl"])):
        o = json.loads(l)
        rr = o["raw_rating"]
        lab = o["label"]
        # decode the sequential rating: Q1 yes -> different; Q1 no & Q2 yes -> equivalent; else info removed/added
        if rr[0] == "yes":
            kind = "different"
        elif rr[1] == "yes":
            kind = "equivalent"
        else:
            kind = "info_changed"
        if (kind == "equivalent") != (lab == "equivalent"):
            stats["label_rating_mismatch"] += 1
            continue
        ctx, q, ref, cand = C.clean(o["context"]), C.clean(o["question"]), C.clean(o["reference"]), C.clean(o["candidate"])
        if not (ctx and q and ref and cand) or C.norm(ref) == C.norm(cand):
            stats["drop_empty_or_same"] += 1
            continue
        recs.append({"rid": f"ae-train-{i}-{o['qid']}", "qid": o["qid"], "ctx": ctx, "q": q, "ref": ref, "cand": cand,
                     "kind": kind, "raw": rr})
    stats["recs"] = len(recs)
    hits = C.decon({r["rid"]: [r["q"], r["ctx"]] for r in recs}, cache_name=KEY)
    xhits = C.cross_v14({r["rid"]: [r["ctx"]] for r in recs}, own_keys={KEY})
    recs = [r for r in recs if r["rid"] not in hits and r["rid"] not in xhits]
    stats["after_decon"] = len(recs)

    recs.sort(key=lambda r: r["rid"])
    rng.shuffle(recs)
    # negatives first (scarcer), then equivalents; one row per passage
    used_ctx = set()
    neg, pos = [], []
    for r in sorted(recs, key=lambda r: r["kind"] == "equivalent"):
        k = C.norm(r["ctx"])
        if k in used_ctx:
            continue
        if r["kind"] == "equivalent":
            if len(pos) >= TARGET // 2:
                continue
            pos.append(r)
        else:
            if len(neg) >= TARGET // 2:
                continue
            neg.append(r)
        used_ctx.add(k)
    n = min(len(neg), len(pos))
    pos = pos[:int(n * 1.1)]
    stats.update({"neg": len(neg), "pos": len(pos)})
    rows = []
    sel = neg + pos
    rng.shuffle(sel)
    for i, r in enumerate(sel):
        qid = "equiv" if i % 2 == 0 else "notequiv"
        eq = r["kind"] == "equivalent"
        gold = ("yes" if eq else "no") if qid == "equiv" else ("no" if eq else "yes")
        ab = r["ref"] + " " + r["cand"]
        if re.search(r"\b(1[0-9]{3}|20[0-9]{2})\b|\b(january|february|march|april|may|june|july|august|september|"
                     r"october|november|december|century)\b", ab, re.I):
            e = "temporal"
        elif re.search(r"\d", ab):
            e = "numeric"
        elif C.QUANT.search(ab):
            e = "quantifier"
        elif C.neg_count(ab):
            e = "negation"
        else:
            e = None
        state = (f"Passage:\n{r['ctx']}\n\nQuestion: {r['q']}\nReference answer: {r['ref']}\n"
                 f"Candidate answer: {r['cand']}")
        rows.append({
            "key": KEY, "rid": r["rid"], "state": state, "instructions": Q[qid], "options": C.YN, "gold": gold,
            "soft": None,
            "meta": {"dataset": DATASET, "config": "v1/train.jsonl", "revision": f"git:{COMMIT}; sha256:{FILES['v1/train.jsonl']}",
                     "licence": LICENCE, "split": "train",
                     "orig_label": {"label": "equivalent" if eq else "not equivalent", "kind": r["kind"],
                                    "raw_rating": r["raw"]},
                     "family": C.FAMILY, "edge": e, "defs": qid},
        })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, DEFS)
    st = C.summary(KEY, rows)
    print("stats:", dict(stats), "| decon:", len(hits), "| cross_v14:", len(xhits))
    print("kinds:", dict(collections.Counter(r["meta"]["orig_label"]["kind"] for r in rows)))
    C.show_samples(rows, n=6, seed=16)
    C.append_manifest(C.manifest_record(
        KEY, DATASET, LICENCE, rows, "yesno",
        "Answer-equivalence judging with HUMAN ratings: can a model-predicted SQuAD answer replace the reference "
        "(asymmetric, conditioned on question and passage; 'June' vs 'every June' is not equivalent, extra relevant "
        "detail is fine). Negatives = completely different or info removed/misleading added. Two framings "
        "(equivalent? / unacceptable substitute?); one row per passage; decon drops passages reachable via QNLI.", st))


if __name__ == "__main__":
    main()
