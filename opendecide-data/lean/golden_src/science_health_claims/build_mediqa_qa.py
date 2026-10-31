"""Build raw rows for mediqa_qa (MEDIQA 2019 Task 3: medical Question Answering; Ben Abacha, Shivade &
Demner-Fushman, ACL-BioNLP 2019).

Source : GitHub abachaa/MEDIQA2019 pinned to commit 32311a139b583a9ccec133b3f8a21873d4ff3561, TRAINING file 2
         only: MEDIQA_Task3_QA/MEDIQA2019-Task3-QA-TrainingSet2-Alexa.xml (104 simple questions about frequent
         diseases). Training file 1 (LiveQA-Med; its questions are the TREC 2017 LiveQA medical TEST questions),
         the validation and the test files are never downloaded.
Licence: CC BY 4.0 (README.md 'License' section at the pinned commit: "This work is released under the Creative
         Commons Attribution 4.0 International License").
Texts  : real consumer health questions; candidate answers are passages from trusted health websites (MedlinePlus,
         GHR, GARD, NIDDK, Mayo Clinic, ...) retrieved by the NLM CHiQA system. Human-written.
Labels : manual expert ReferenceScore per answer: 4 Excellent, 3 Correct but incomplete, 2 Related, 1 Incorrect. The
         official answer-classification mapping (Task3_README.txt) is 3-4 = correct (yes), 1-2 = incorrect (no).
Question: "Does the passage correctly answer the consumer's health question?"
Filters: answers of 40-6,000 characters (longer pages are not truncated, because a cut could remove the answer);
         exact (question, answer) duplicates dropped; decontamination (label-NLI, local train/dev/eval, JevBench) and a
         cross-check against the other v14 golden parts (NIH passages also appear in MedQuAD-based parts) drop overlaps;
         to reach the yes band some score-1 (clearly off-topic) negatives are dropped first, score-2 'related but not
         answering' negatives are kept as hard cases (edge=missing_info).
Review fix (strict reviewer, 29 Sep): Training Set 1's questions ARE the TREC 2017 LiveQA medical TEST questions
         (Task3_README: "TREC-2017-LiveQA medical test questions"; the same 104 questions are the 'LiveQA' test set
         of MultiMedQA). Rule 4 (never test) and 'never share texts with a test set' therefore exclude it: only
         Training Set 2 (Alexa, 104 simple questions about frequent diseases written for MEDIQA) is used, and the
         LiveQA-Med file is no longer downloaded. A 15-row audit also found its score-3 labels the least reliable
         (generic pages scored 'correct but incomplete').
Deterministic (seed 20261116). CPU only.
"""
import collections
import random
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _shc_common as C  # noqa: E402

KEY = "mediqa_qa"
SEED = 20261116
COMMIT = "32311a139b583a9ccec133b3f8a21873d4ff3561"
BASE = f"https://raw.githubusercontent.com/abachaa/MEDIQA2019/{COMMIT}/"
# Training Set 1 (MEDIQA2019-Task3-QA-TrainingSet1-LiveQAMed.xml, sha256 351d60ad...) is NOT used: its questions are
# the TREC 2017 LiveQA medical test questions (see the review fix above).
FILES = {
    "MEDIQA_Task3_QA/MEDIQA2019-Task3-QA-TrainingSet2-Alexa.xml":
        "00bacd5a61cefa22dee872c8a1efb09407638cbc56833688b89388b620b81944",
    "README.md": "22a4342625442cd97be5de2d08e39aa538eb691c9cbdb38f7dc3ec0b0e95baeb",
    "MEDIQA_Task3_QA/Task3_README.txt": "fe91e5614b53a19affb6823a190589cef2757ccd9905ed0521447eceb1771a81",
}
LICENCE = (f"CC BY 4.0 (https://github.com/abachaa/MEDIQA2019/blob/{COMMIT}/README.md, 'License': 'This work is "
           "released under the Creative Commons Attribution 4.0 International License')")
DATASET = "MEDIQA 2019 Task 3 QA (github abachaa/MEDIQA2019)"
QUESTION = "Does the passage correctly answer the consumer's health question?"
DEFS = {
    "yes": "The passage gives a correct answer to what the consumer actually asked, either completely or correctly "
           "but incompletely (it covers part of the requested information, such as some of the treatments or "
           "symptoms asked about).",
    "no": "The passage does not answer the question: it is only related to the topic (right disease or drug but the "
          "wrong aspect, e.g. causes when treatment was asked, or page metadata), or it is about something else or "
          "gives incorrect information.",
}
MIN_LEN, MAX_LEN = 40, 6000


def main():
    rng = random.Random(SEED)
    cache = C.CACHE / KEY
    paths = {rel: C.fetch(BASE + rel, cache / Path(rel).name, sha) for rel, sha in FILES.items()}
    stats = collections.Counter()
    cands, seen = [], set()
    for rel in list(FILES)[:1]:  # Alexa only
        subset = "LiveQAMed" if "LiveQAMed" in rel else "Alexa"
        root = ET.parse(paths[rel]).getroot()
        for q in root.findall("Question"):
            qid = q.get("QID")
            qtext = C.clean(q.find("QuestionText").text or "")
            for a in q.find("AnswerList").findall("Answer"):
                stats["answers"] += 1
                atext = C.clean(a.find("AnswerText").text or "")
                score = int(a.get("ReferenceScore"))
                if not (MIN_LEN <= len(atext) <= MAX_LEN) or len(qtext) < 8:
                    stats["drop_len"] += 1
                    continue
                k = (C.norm(qtext), C.norm(atext))
                if k in seen:
                    stats["drop_dup"] += 1
                    continue
                seen.add(k)
                cands.append({"rid": f"{subset}-{a.get('AID')}", "q": qtext, "a": atext, "score": score,
                              "gold": "yes" if score >= 3 else "no", "subset": subset, "qid": qid,
                              "url": (a.find("AnswerURL").text or "").strip(),
                              "sys_rank": int(a.get("SystemRank")), "ref_rank": int(a.get("ReferenceRank"))})
    stats["cands"] = len(cands)
    core = {c["rid"]: [c["q"], c["a"]] for c in cands}
    hits = C.decon(core, cache_name=KEY)
    xhits = C.cross_v14({c["rid"]: [c["a"]] for c in cands}, own_keys={KEY})
    cands = [c for c in cands if c["rid"] not in hits and c["rid"] not in xhits]

    yes = [c for c in cands if c["gold"] == "yes"]
    no2 = [c for c in cands if c["score"] == 2]
    no1 = [c for c in cands if c["score"] == 1]
    max_no = int(len(yes) * 0.60 / 0.40)
    rng.shuffle(no1)
    no = no2 + no1
    if len(no) > max_no:
        no = no2 + no1[:max(0, max_no - len(no2))]
    rows = []
    for c in sorted(yes + no, key=lambda c: c["rid"]):
        state = f"Consumer health question:\n{c['q']}\n\nPassage:\n{c['a']}"
        if c["score"] == 2:
            e = "missing_info"
        elif len(state) > 2500:
            e = "long_context"
        else:
            e = None
        rows.append({
            "key": KEY, "rid": c["rid"], "state": state, "instructions": QUESTION, "options": C.YN,
            "gold": c["gold"], "soft": None,
            "meta": {"dataset": DATASET, "config": f"Task3 QA training set ({c['subset']})",
                     "revision": f"git:{COMMIT}; sha256:{FILES[list(FILES)[0]]}",
                     "licence": LICENCE, "split": "train",
                     "orig_label": {"ReferenceScore": c["score"], "ReferenceRank": c["ref_rank"],
                                    "SystemRank": c["sys_rank"], "QID": c["qid"], "AnswerURL": c["url"]},
                     "family": C.FAMILY, "edge": e},
        })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, {None: DEFS})
    st = C.summary(KEY, rows)
    print("stats:", dict(stats), "| decon:", len(hits), "| cross_v14:", len(xhits))
    print("scores:", dict(collections.Counter(r["meta"]["orig_label"]["ReferenceScore"] for r in rows)))
    C.show_samples(rows, n=5, seed=8)
    C.append_manifest(C.manifest_record(
        KEY, DATASET + ", training set 2 (Alexa) only", LICENCE, rows, "yesno",
        "Answer-adequacy judging for consumer health questions: expert ReferenceScore 3-4 = yes, 1-2 = no (official "
        "mapping); score-2 'related but not answering' passages kept as hard negatives; no truncation of long pages; "
        "training set 1 (LiveQA-Med) excluded because its questions are the TREC 2017 LiveQA medical test set.",
        st))


if __name__ == "__main__":
    main()
