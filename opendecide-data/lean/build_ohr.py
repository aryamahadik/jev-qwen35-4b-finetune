"""Open hard-reasoning rows (OHR) from public multi-step reasoning datasets, for the single decision model:
  ProofWriter (OWA, proof depth >= 2; true / false / unknown)   CC BY 4.0
  FLD v2 (formal-logic deduction with distractors; proved / disproved / unknown)
  LogiQA 2.0 (4-option logical reading)                          research licence (noted in HANDOFF)
  MuSR (long narratives: murder mysteries, object placement, team allocation)
None of these sources appear in our eval / dev splits; JevBench overlap is removed afterwards by decontam.py.
Writes data/ohr_train.jsonl.
"""
import ast
import json
import random
from collections import Counter
from pathlib import Path

from datasets import load_dataset

HERE = Path(__file__).resolve().parent
rng = random.Random(20260926)
rows = []


def add(src, i, state, instr, options, gold, card=None):
    assert gold in options and len(set(options)) == len(options)
    rows.append({"id": f"r_ohr_{src}_{i}", "group_id": f"g:ohr:{src}:{i}", "call_id": f"c_ohr_{src}_{i}", "split": "train",
                 "track": "OHR", "source": src, "state": state, "qtype": "choice", "instructions": instr, "options": options,
                 "gold": gold, "role": "choice", **({"card": card} if card else {}), "meta": {"anchor": False}})


def balanced(items, key, n):
    by = {}
    for x in items:
        by.setdefault(key(x), []).append(x)
    for v in by.values():
        rng.shuffle(v)
    per = n // len(by)
    return [x for v in by.values() for x in v[:per]]


# ProofWriter: open-world, multi-hop (QDep >= 2), balanced over true / false / unknown
pw = load_dataset("tasksource/proofwriter", split="train")
pw = pw.filter(lambda x: "OWA" in x["id"] and int(x["QDep"]) >= 2)
PW_CARD = ("- true: the statement follows from the facts and rules\n- false: the opposite of the statement follows from the "
           "facts and rules\n- unknown: neither the statement nor its opposite can be derived from the facts and rules")
for i, x in enumerate(balanced(list(pw.select(range(min(len(pw), 60000)))), lambda x: x["answer"], 1800)):
    add("proofwriter", i, x["theory"].replace(". ", ".\n"),
        f"Using only the facts and rules above (anything not stated or derivable is unknown), is this statement true, false, "
        f"or unknown?\nStatement: {x['question']}", ["true", "false", "unknown"], x["answer"].lower(), PW_CARD)

# FLD v2: deduction over many sentences with distractors
fld = load_dataset("hitachi-nlp/FLD.v2", "default", split="train")
FLD_CARD = ("- proved: the facts prove the hypothesis\n- disproved: the facts prove the hypothesis is false\n"
            "- unknown: the facts neither prove nor disprove the hypothesis")
lab = {"PROVED": "proved", "DISPROVED": "disproved", "UNKNOWN": "unknown"}
fl = [x for x in fld.select(range(20000)) if x["world_assump_label"] in lab]
for i, x in enumerate(balanced(fl, lambda x: x["world_assump_label"], 1500)):
    ctx = "\n".join("sent" + s.strip() for s in x["context"].split("sent") if s.strip())
    add("fld", i, ctx, f"Hypothesis: {x['hypothesis']}\nGiven only the sentences above, is the hypothesis proved, disproved, "
        f"or unknown?", ["proved", "disproved", "unknown"], lab[x["world_assump_label"]], FLD_CARD)

# LogiQA 2.0
lq = load_dataset("datatune/LogiQA2.0", split="train")
idx = rng.sample(range(len(lq)), 6000)
for i, j in enumerate(idx):
    d = json.loads(lq[j]["text"])
    if "options" not in d or sum(r["source"] == "logiqa2" for r in rows) >= 1500:  # the MRC rows (the NLI rows lack options)
        continue
    if sum(ord(ch) > 127 for ch in d["text"]) > 0.05 * len(d["text"]):  # English split only (the set also has Chinese)
        continue
    o = d["options"]
    opts = [str(x).strip() for x in (ast.literal_eval(o) if isinstance(o, str) else o)]
    if len(set(opts)) != len(opts) or not d["text"].strip():
        continue
    add("logiqa2", i, d["text"].strip(), d["question"].strip(), opts, opts[int(d["answer"])])

# MuSR: long narratives with multi-step commonsense reasoning
for sp in ("murder_mysteries", "object_placements", "team_allocation"):
    mu = load_dataset("TAUR-Lab/MuSR", split=sp)
    for i, x in enumerate(mu):
        ch = x["choices"] if isinstance(x["choices"], list) else ast.literal_eval(x["choices"])  # stored as a Python list string
        ch = [str(c).strip() for c in ch]
        if len(set(ch)) != len(ch):
            continue
        add(f"musr_{sp}", i, x["narrative"].strip(), x["question"].strip(), ch, ch[int(x["answer_index"])])

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
(HERE / "data/ohr_train.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
print(len(rows), Counter(r["source"] for r in rows), Counter(r["gold"] for r in rows if r["source"] in ("proofwriter", "fld")))
