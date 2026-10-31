"""Build raw rows for medqa_yn (MedQA-USMLE; Jin, Pan, Oufattole, Weng, Fang & Szolovits, "What Disease does this
Patient Have? A Large-scale Open Domain Question Answering Dataset from Medical Exams", Applied Sciences 2021,
arXiv:2009.13081) as yes/no answer verification on clinical vignettes.

Source : the data zip 'data_clean.zip' linked from the README of github jind11/MedQA (commit
         27b02f66aac217933c9648a06f82e9f720377925; Google Drive id 1ImYUSLk9JbgHXOemfvyiDiirluZHPeQw), pinned by
         sha256. Only data_clean/questions/US/train.jsonl is read (the official random split; dev.jsonl, test.jsonl,
         the Chinese/Taiwanese sets and the textbooks are never read).
Licence: MIT (LICENSE of github jind11/MedQA, "Copyright (c) 2022 Di Jin"; the repository is "Code and data for
         MedQA" and its README distributes the data through the linked zip).
Texts  : USMLE-style (Step 1, Step 2&3) multiple-choice questions written by medical experts for board-exam
         preparation: a clinical vignette (history, vitals, labs, exam) and a question stem; 5 options, one keyed
         single best answer. Human-written, human-keyed.
Framing: one row per question. State = the vignette and question, the five lettered answer choices, then
         "Proposed answer: <letter>. <option>". The proposed
         option is the keyed answer (yes) or one other option drawn uniformly at random (no), with a seeded 50/50
         choice, so labels follow exactly from the answer key (single-best-answer format).
Question: "Is the proposed answer the single best answer to this medical exam question?"
Filters: questions that refer to an image, radiograph, smear or ECG that is not in the text ('as shown', 'shown
         below', 'image', 'photograph', ...) are dropped (1,086 of 10,178); exact-duplicate questions dropped; decontamination (label-NLI incl. medical_questions_pairs, local
         train/dev/eval, JevBench public) and a cross-check against the other v14 golden parts; at most MAX_ROWS rows.
Edge   : negation for EXCEPT/NOT/LEAST stems (the answer is the exception), long_context for long vignettes, units
         for vignettes with lab values.
Review fix (strict reviewer, 29 Sep): the first build showed only the vignette and the proposed option, while the
         definitions (and the exam key) refer to the LISTED choices; 'single best answer' is relative to the option
         set (a keyed answer is sometimes only the best of the five listed). The state now lists all five answer
         choices before the proposed one, so the label follows exactly from the key. Near-duplicate questions in the
         source (the same vignette re-posted with small edits; >= 80% of 8-word shingles shared) are dropped.
Deterministic (seed 20261120). CPU only.
"""
import collections
import json
import random
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _shc_common as C  # noqa: E402

KEY = "medqa_yn"
SEED = 20261120
COMMIT = "27b02f66aac217933c9648a06f82e9f720377925"
ZIP_URL = "https://drive.usercontent.google.com/download?id=1ImYUSLk9JbgHXOemfvyiDiirluZHPeQw&export=download&confirm=t"
ZIP_SHA = "1c2ca8130b3d86d9a99a432ab9bef14f3bb9807bef20facd9ac86ba36960f629"
LICENSE_URL = f"https://raw.githubusercontent.com/jind11/MedQA/{COMMIT}/LICENSE"
LICENCE = (f"MIT (https://github.com/jind11/MedQA/blob/{COMMIT}/LICENSE, 'Copyright (c) 2022 Di Jin'; repository "
           "'Code and data for MedQA', data zip linked from its README)")
DATASET = "MedQA-USMLE (github jind11/MedQA, data_clean.zip, US 5-option)"
QUESTION = "Is the proposed answer the single best answer to this medical exam question?"
DEFS = {
    "yes": "Among the listed answer choices, the proposed option is the single best answer to the question exactly as "
           "asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, "
           "it is the one option that is the exception).",
    "no": "The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate "
          "in a different situation, but it is not the best answer to the question as asked.",
}
MAX_ROWS = 8000
NEG_STEM = re.compile(r"\b(EXCEPT|NOT|LEAST|FALSE|INCORRECT)\b")
# questions that depend on a picture, radiograph, smear, ECG or table that is not in the text are dropped
IMAGE_REF = re.compile(r"(\bas shown\b|\bis shown\b|\bare shown\b|\bshown below\b|\bshown in\b|\bpicture\b|"
                       r"\bphotograph|\bimage\b|\bfigure\b|\bexhibit\b|\bthe following (ECG|EKG|x-ray|radiograph|"
                       r"smear|slide|biopsy)|\bseen below\b|\billustrated\b)", re.I)
LAB = re.compile(r"\b\d[\d,.]*\s?(mg/dL|mEq/L|mmol/L|g/dL|U/L|/mm3|/mm\^3|mm Hg|mmHg|%|µg|ng/mL|pg/mL|IU/L)", re.I)


def main():
    rng = random.Random(SEED)
    cache = C.CACHE / KEY
    zpath = C.fetch(ZIP_URL, C.CACHE / "medqa" / "data_clean.zip", ZIP_SHA)
    with zipfile.ZipFile(zpath) as z:
        lines = z.read("data_clean/questions/US/train.jsonl").decode("utf-8").splitlines()  # TRAIN ONLY
    lic = cache / "LICENSE"
    if not lic.exists():
        import requests
        lic.parent.mkdir(parents=True, exist_ok=True)
        lic.write_bytes(requests.get(LICENSE_URL, timeout=60).content)
    assert "MIT License" in lic.read_text()
    stats = collections.Counter()
    recs, seen = [], set()
    for i, line in enumerate(lines):
        d = json.loads(line)
        q = C.clean(d["question"])
        opts = {k: C.clean(v) for k, v in d["options"].items()}
        key = d["answer_idx"]
        assert opts[key] == C.clean(d["answer"]), (i, key)
        if IMAGE_REF.search(q):
            stats["drop_needs_image"] += 1
            continue
        n = C.norm(q)
        if n in seen or len(q) < 40:
            stats["drop_dup_or_short"] += 1
            continue
        if len({C.norm(v) for v in opts.values()}) < len(opts):
            stats["drop_duplicate_options"] += 1
            continue
        seen.add(n)
        recs.append({"rid": f"medqa-us-train-{i:05d}", "q": q, "opts": opts, "key": key, "step": d["meta_info"]})
    # near-duplicate questions (same vignette re-posted with small edits): keep the first
    def sh(t):
        w = C.words(t)
        return {hash(tuple(w[i:i + 8])) for i in range(len(w) - 7)}
    owner, kept = {}, []
    for r in recs:
        s = sh(r["q"])
        cnt = collections.Counter(owner[h] for h in s if h in owner)
        if any(n / (min(len(s), olen) or 1) >= 0.8 for (j, olen), n in cnt.items()):
            stats["drop_near_dup_question"] += 1
            continue
        for h in s:
            owner.setdefault(h, (len(kept), len(s)))
        kept.append(r)
    recs = kept
    stats["usable"] = len(recs)
    hits = C.decon({r["rid"]: [r["q"]] for r in recs}, cache_name=KEY)
    xhits = C.cross_v14({r["rid"]: [r["q"]] for r in recs}, own_keys={KEY})
    recs = [r for r in recs if r["rid"] not in hits and r["rid"] not in xhits]
    rng.shuffle(recs)
    recs = recs[:MAX_ROWS]
    rows = []
    for j, r in enumerate(recs):
        is_yes = j % 2 == 0
        if is_yes:
            letter = r["key"]
        else:
            letter = rng.choice(sorted(k for k in r["opts"] if k != r["key"]))
        prop = r["opts"][letter]
        choices = "\n".join(f"{k}. {v}" for k, v in sorted(r["opts"].items()))
        state = f"{r['q']}\n\nAnswer choices:\n{choices}\n\nProposed answer: {letter}. {prop}"
        stem = re.split(r"(?<=[.?!])\s+", r["q"])[-1]
        if NEG_STEM.search(stem):
            e = "negation"
        elif len(r["q"]) > 1500:
            e = "long_context"
        elif LAB.search(r["q"]):
            e = "units"
        else:
            e = None
        rows.append({
            "key": KEY, "rid": r["rid"], "state": state, "instructions": QUESTION, "options": C.YN,
            "gold": "yes" if is_yes else "no", "soft": None,
            "meta": {"dataset": DATASET, "config": "data_clean/questions/US/train.jsonl",
                     "revision": f"git:{COMMIT}; zip sha256:{ZIP_SHA}", "licence": LICENCE, "split": "train",
                     "orig_label": {"answer_idx": r["key"], "proposed_idx": letter, "exam": r["step"],
                                    "options": r["opts"]},
                     "family": C.FAMILY, "edge": e},
        })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, {None: DEFS})
    st = C.summary(KEY, rows)
    print("stats:", dict(stats), "| decon:", len(hits), "| cross_v14:", len(xhits))
    print("exam:", dict(collections.Counter(x["meta"]["orig_label"]["exam"] for x in rows)))
    C.show_samples(rows, n=5, seed=10)
    C.append_manifest(C.manifest_record(
        KEY, DATASET + ", train split", LICENCE, rows, "yesno",
        "Clinical-vignette answer verification: vignette + all five lettered choices + a proposed choice; keyed single "
        "best answer (yes) vs one random other option (no), one row per question; labels exact from the exam key; "
        "near-duplicate questions dropped; EXCEPT/NOT stems tagged negation.", st))


if __name__ == "__main__":
    main()
