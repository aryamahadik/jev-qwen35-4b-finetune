"""SB5 G6-style partial-input probe (A58 c 7): REPORT ONLY, never admits or drops a row. 5-fold CV (seed 20261013) on all
non-hold-out source train rows: majority share, length-only logistic, word-unigram lexicon logistic, and both."""
import json, sys
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from scipy.sparse import hstack, csr_matrix
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from sb5_lib import *
P = json.load(open(WORK / "pool.json", encoding="utf-8"))
dev = set(P["dev_ids"]); rows = [r for r in P["kept"] if r["rid"] not in dev]
y = np.array([r["label"] == "pos" for r in rows]); txt = [" ".join(norm_tokens(r["text"])) for r in rows]
def lenf(r):
    t = r["text"]; w = t.split()
    return [len(w), len(t), np.log1p(len(w)), t.count("!"), t.count("?"), t.count("#"), t.count("@"), int("http" in t)]
L = np.array([lenf(r) for r in rows], float); L = (L - L.mean(0)) / (L.std(0) + 1e-9)
cv = StratifiedKFold(5, shuffle=True, random_state=SEED % (2**31))
def score(X):
    return float(np.mean(cross_val_score(LogisticRegression(max_iter=2000, C=1.0), X, y, cv=cv)))
vec = TfidfVectorizer(token_pattern=r"\S+", min_df=2, sublinear_tf=True)
Xw = vec.fit_transform(txt)       # vocabulary fit on all rows: a mild optimism for the lexicon baseline, stated
out = {"rows": len(rows), "positive_share": round(float(y.mean()), 4), "majority": round(float(max(y.mean(), 1 - y.mean())), 4),
       "length_only_cv_acc": round(score(L), 4), "lexicon_unigram_cv_acc": round(score(Xw), 4),
       "length_plus_lexicon_cv_acc": round(score(hstack([Xw, csr_matrix(L)]).tocsr()), 4),
       "mean_words": {"positive": round(float(np.mean([len(r["text"].split()) for r, p in zip(rows, y) if p])), 2),
                      "negative": round(float(np.mean([len(r["text"].split()) for r, p in zip(rows, y) if not p])), 2)},
       "note": "report only (A58 c 7); the TF-IDF vocabulary is fit on all rows before the folds, so the lexicon score is a slight over-estimate; the length gap is the creators' known one"}
json.dump(out, open(WORK / "probe_report.json", "w"), indent=1); print(json.dumps(out, indent=1))
