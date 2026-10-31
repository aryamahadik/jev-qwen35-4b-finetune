#!/usr/bin/env python3
"""G1/feasibility helper: headline overlap between ANS stance train and dev (counts only; python -I)."""
import csv, json, re, unicodedata
from collections import Counter
from pathlib import Path
SB4 = Path(__file__).resolve().parent.parent
DIAC = re.compile("[ً-ٰٟـ]"); PUNCT = re.compile(r"[^\w\s]", re.U)
def norm(t):
    t = unicodedata.normalize("NFKC", t); t = DIAC.sub("", t)
    t = t.replace("أ","ا").replace("إ","ا").replace("آ","ا").replace("ى","ي").replace("ة","ه")
    return " ".join(PUNCT.sub(" ", t.lower()).split())
def load(sp):
    with open(SB4/f"src/data/stance/{sp}.csv", encoding="utf-8", newline="") as f:
        r = csv.reader(f); h = next(r); return [(norm(x[h.index("s1")]), norm(x[h.index("s2")]), x[h.index("stance")]) for x in r]
tr, dv = load("train"), load("dev")
trv = {a for a, b, _ in tr} | {b for a, b, _ in tr}
dv_clean = [(a, b, c) for a, b, c in dv if a not in trv and b not in trv]
tr_pairs = {(a, b) for a, b, _ in tr}
out = {"train_rows": len(tr), "dev_rows": len(dv),
       "dev_rows_with_a_side_equal_to_a_train_value": len(dv) - len(dv_clean),
       "dev_rows_with_no_shared_value": len(dv_clean), "dev_clean_stance": dict(Counter(c for _, _, c in dv_clean)),
       "dev_pairs_equal_to_train_pair": sum(1 for a, b, _ in dv if (a, b) in tr_pairs or (b, a) in tr_pairs),
       "train_exact_pair_dups": len(tr) - len(tr_pairs),
       "train_pairs_with_same_unordered_pair": len(tr) - len({frozenset((a, b)) for a, b, _ in tr}),
       "train_rows_s1_equals_s2": sum(1 for a, b, _ in tr if a == b),
       "train_stance_conflicts_same_unordered_pair": 0}
d = {}
for a, b, c in tr: d.setdefault(frozenset((a, b)), set()).add(c)
out["train_stance_conflicts_same_unordered_pair"] = sum(1 for v in d.values() if len(v) > 1)
(SB4/"checks/g1_split_overlap.json").write_text(json.dumps(out, indent=1)+"\n"); print(json.dumps(out, indent=1))
