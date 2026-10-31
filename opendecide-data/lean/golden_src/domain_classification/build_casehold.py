"""Build raw rows for casehold_yn (CaseHOLD, Zheng, Guha et al., ICAIL 2021) as a yes/no holding-verification task.

Source : HF casehold/casehold (the authors' org), data/all/train.csv ONLY (val/test never read).
         Pinned to revision acc4532a67e0966e9ed7ec4ca543e8532f983b0c; sha256 of train.csv checked.
Licence: Apache-2.0, LICENSE file of the authors' repository reglab/casehold (commit daea97cc...), whose README
         states "It includes models, datasets, and code"; texts are US judicial opinions (Harvard Caselaw Access
         Project, public-domain government edicts).
Texts  : human-written: the citing passage of a US court opinion with the cited case's parenthetical replaced by
         <HOLDING>, and holding statements written by judges in citation parentheticals.
Labels : by construction of the source: exactly one of the 5 candidates is the parenthetical that actually followed
         the citation; the other 4 are holdings of other cases retrieved for topical similarity. No model labels.
Task   : one row per source record. yes-row = the true holding; no-row = the wrong candidate that is least similar
         (content-word Jaccard) to the true holding, only if that Jaccard <= 0.35 and neither text contains the
         other (so a "no" is never a paraphrase of the correct holding).
Decontamination: 12-gram overlap against LegalBench overruling + function_of_decision_section (Casetext / case-law
         sentences, an OHS-1 source family) -> dropped; then (reviewer fix) any 12-gram shared by the passage or any of
         the 5 candidates with lex_glue SCOTUS / LEDGAR or any LegalBench task, or by the passage with lex_glue case_hold
         validation+test passages -> dropped. Near-duplicate passages (5-gram MinHash Jaccard >= 0.7) dropped.
Deterministic (seed 20260929). CPU only.
"""
import collections
import random
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

KEY = "casehold_yn"
SEED = 20260929
MAX_ROWS = 6000
REV = "acc4532a67e0966e9ed7ec4ca543e8532f983b0c"
TRAIN_SHA = "515aa9c21911d644caeef4a7b962fe079c476e693a2901a43fc09b9a998fbbd5"
LIC_COMMIT = "daea97cca16a4d203380f2cebed1a10ed8d42b87"
LIC_SHA = "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4"
LB_REV = "daec8237410aa23e3faf4bc41ad8b3a7e1696826"
LICENCE = (f"Apache-2.0 (https://github.com/reglab/casehold/blob/{LIC_COMMIT}/LICENSE; README of the same repo: "
           "'It includes models, datasets, and code'); texts are US court opinions (Caselaw Access Project, public domain)")
CACHE = C.CACHE / "casehold"
QUESTION = ("Does the candidate statement correctly give the holding of the case that this court opinion cites "
            "at the <HOLDING> marker?")
DEFS = {
    "yes": ("The candidate is the holding the citing court attributes to the case cited at <HOLDING>: it states the "
            "legal rule or outcome of that cited case and supports the exact proposition the passage uses it for."),
    "no": ("The candidate is a holding from a different case: its rule, statute, jurisdiction, party situation or "
           "outcome does not match the proposition the passage cites that case for, even if it shares topic words."),
}
STOP = set("a an the of to in on for and or that is was be by as at it its with from this which under not no "
           "holding held recognizing finding noting stating explaining concluding".split())
NEG = re.compile(r"\b(not|no|never|neither|nor|cannot)\b|n't\b")
EXC = re.compile(r"\b(unless|except|excepting|exception|notwithstanding|absent)\b")


def cw(t):
    return {w for w in C.norm(t).split() if w not in STOP and len(w) > 1}


def jacc(a, b):
    a, b = cw(a), cw(b)
    return len(a & b) / max(1, len(a | b))


def clean_context(t):
    t = re.sub(r"\s+", " ", t).strip()
    if t and not t[0].isupper():
        m = re.search(r"[.!?][\"”’)]?\s+(?=[A-Z])", t[:300])
        if m:
            t = t[m.end():]
    return t


def main():
    train, _ = C.fetch(f"https://huggingface.co/datasets/casehold/casehold/resolve/{REV}/data/all/train.csv",
                       CACHE / "train.csv", TRAIN_SHA)
    C.fetch(f"https://raw.githubusercontent.com/reglab/casehold/{LIC_COMMIT}/LICENSE", CACHE / "LICENSE", LIC_SHA)
    lb = set()
    for task in ("overruling", "function_of_decision_section"):
        for sp in ("train", "test"):
            p, _ = C.fetch(f"https://huggingface.co/datasets/nguha/legalbench/resolve/{LB_REV}/data/{task}/{sp}.tsv",
                           CACHE / f"lb_{task}_{sp}.tsv")
            df = pd.read_csv(p, sep="\t", dtype=str, keep_default_na=False)
            for t in df["text" if "text" in df.columns else "Paragraph"]:
                lb |= C.ngrams(t, 12)
    print("legalbench decontam 12-grams:", len(lb))

    d = pd.read_csv(train, dtype=str, keep_default_na=False)  # TRAIN ONLY
    stats = collections.Counter()
    nd = C.NearDup(0.7)
    recs = []
    for r in d.itertuples(index=False):
        rid, ctx = r[0], r[1]
        hold = [re.sub(r"\s+", " ", h).strip() for h in r[2:7]]
        lab = int(r[12])
        if ctx.count("<HOLDING>") != 1:
            stats["no_marker"] += 1
            continue
        ctx = clean_context(ctx)
        if len(ctx) < 400 or ctx.index("<HOLDING>") < 150:
            stats["short"] += 1
            continue
        if len({C.norm(h) for h in hold}) < 5 or min(len(h.split()) for h in hold) < 4 or max(map(len, hold)) > 400:
            stats["bad_cands"] += 1
            continue
        if C.ngrams(ctx, 12) & lb:
            stats["legalbench_overlap"] += 1
            continue
        if nd.seen(ctx):
            stats["near_dup"] += 1
            continue
        correct = hold[lab]
        wrong = sorted(((jacc(correct, hold[k]), k) for k in range(5) if k != lab))
        jw, kw = wrong[0]
        ok_no = (jw <= 0.35 and C.norm(hold[kw]) not in C.norm(correct) and C.norm(correct) not in C.norm(hold[kw])
                 and len(hold[kw].split()) >= 6)
        recs.append({"rid": rid, "ctx": ctx, "hold": hold, "lab": lab, "kw": kw if ok_no else None, "jw": jw})
    print("usable:", len(recs), dict(stats))
    # Reviewer fix (2026-09-29): 12-gram decontamination of the passage AND all 5 candidate holdings against the
    # forbidden legal sources: lex_glue SCOTUS (a forbidden label-NLI task; lower courts quote SCOTUS opinions and a
    # few CaseHOLD passages are SCOTUS opinions), lex_glue LEDGAR (OHS-1) and all of LegalBench. Passages only (the
    # holdings pool is shared by design) against lex_glue case_hold validation/test (the LexGLUE re-split's eval
    # parts). Any shared 12-gram drops the record.
    bad = C.forbidden_legal_hits({r["rid"]: [r["ctx"]] + r["hold"] for r in recs},
                                 ["lexglue_scotus", "lexglue_ledgar", "legalbench_all"])
    bad |= C.forbidden_legal_hits({r["rid"]: [r["ctx"]] for r in recs}, ["lexglue_casehold_evaltest"])
    recs = [r for r in recs if r["rid"] not in bad]
    print("forbidden-legal 12-gram overlap dropped:", len(bad), "usable now:", len(recs))

    rng = random.Random(SEED)
    recs.sort(key=lambda x: int(x["rid"]))
    rng.shuffle(recs)
    n_half = MAX_ROWS // 2
    used_cand = collections.Counter()
    rows = []
    n_yes = n_no = 0
    for rec in recs:
        if n_yes >= n_half and n_no >= n_half:
            break
        want_no = rec["kw"] is not None and n_no < n_half and (n_no <= n_yes or n_yes >= n_half)
        if not want_no and n_yes >= n_half:
            continue
        k = rec["kw"] if want_no else rec["lab"]
        cand = rec["hold"][k]
        if used_cand[C.norm(cand)] >= 2:  # keep candidate holdings diverse
            continue
        used_cand[C.norm(cand)] += 1
        gold = "no" if want_no else "yes"
        n_no += want_no
        n_yes += not want_no
        edge = "exception" if EXC.search(cand) else "negation" if NEG.search(cand) else None
        state = ("Court opinion passage (the parenthetical after one citation is replaced by <HOLDING>):\n"
                 f"{rec['ctx']}\n\nCandidate holding for <HOLDING>: {cand}")
        rows.append({
            "key": KEY, "rid": f"casehold-train-{rec['rid']}", "state": state, "instructions": QUESTION,
            "options": ["yes", "no"], "gold": gold, "soft": None,
            "meta": {"dataset": "casehold/casehold (CaseHOLD)", "config": "data/all/train.csv; yes/no holding verification",
                     "revision": f"hf:{REV}; sha256:{TRAIN_SHA}", "licence": LICENCE, "split": "train",
                     "orig_label": {"correct_index": rec["lab"], "candidate_index": k,
                                    "candidate_jaccard_to_correct": round(rec["jw"], 3) if want_no else 1.0},
                     "family": C.FAMILY, "edge": edge, "seed": SEED},
        })
    rng.shuffle(rows)
    C.write_rows(KEY, rows)
    C.write_defs(KEY, DEFS)
    C.summary(rows)


if __name__ == "__main__":
    main()
