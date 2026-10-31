"""Shared pieces of the C2.1 Tier-1 eval harnesses (L-E; eval only, never a training input).

Protocol shared by every harness
--------------------------------
* One-token readout: every row is {id, state, instructions, options, qtype="choice", gold, card=None, meta}; the model
  answers with the LETTER of one option (decoder_io.predict reads the logits of the option-letter tokens). A harness
  therefore only BUILDS rows (CPU) and SCORES prediction files (CPU); reading the model is run_readout.py (GPU).
* Both option orders: every row gets a seeded displayed order ("fwd", seed rule = decoder_io.view_perms) and its exact
  reverse ("rev"). Two prediction files are written, one per order; the headline probability of an option is the mean of
  the two (the same average decoder_io.predict(tta=True) takes). Per-order accuracy is reported as a position-bias check.
* Predictions are {"id", "model", "probs": {option_text: p}} per line, probabilities keyed by the ORIGINAL option text.
* Row ids and ids inside views never contain eval text; views are plain index permutations.
* Nothing here calls a model API or a competitor. Quarantine directory: lean/bench/c21_eval_quarantine/<set>/.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent.parent
QUARANTINE = LEAN / "bench" / "c21_eval_quarantine"
SEED = "c21-eval-v1"  # view seed; part of the pre-registration (changing it changes every displayed order)


# ------------------------------------------------------------------ hashing and io
def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha256_obj(obj) -> str:
    return sha256_bytes(canon(obj).encode("utf-8"))


def read_jsonl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(p, rows):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return sha256_file(p)


def write_json(p, obj):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False, sort_keys=True)
    return sha256_file(p)


# ------------------------------------------------------------------ rows and views
def make_row(rid, state, instructions, options, gold=None, meta=None):
    if len(set(options)) != len(options):
        raise ValueError(f"row {rid}: duplicate option text")
    if gold is not None and gold not in options:
        raise ValueError(f"row {rid}: gold not among options")
    return {"id": rid, "state": state, "instructions": instructions, "options": list(options), "qtype": "choice",
            "gold": gold, "card": None, "meta": meta or {}}


def seeded_perm(rid: str, n: int, seed: str = SEED):
    """Displayed order for one row: same rule as decoder_io.view_perms (sha256 of seed:id, random.shuffle)."""
    rng = random.Random(int.from_bytes(hashlib.sha256(f"{seed}:{rid}".encode()).digest()[:8], "big"))
    p = list(range(n))
    rng.shuffle(p)
    return p


def make_views(rows, seed: str = SEED):
    """{id: {"fwd": perm, "rev": reversed perm}}; perm[k] = original index of the option shown at position k."""
    out = {}
    for r in rows:
        p = seeded_perm(r["id"], len(r["options"]), seed)
        out[r["id"]] = {"fwd": p, "rev": p[::-1]}
    return out


def shown_options(row, perm):
    return [row["options"][i] for i in perm]


def combine_orders(fwd: dict, rev: dict):
    """Mean of the two displayed-order readings, per row id. Inputs: {id: {option: p}} (original option keys)."""
    if set(fwd) != set(rev):
        raise ValueError("fwd and rev prediction files cover different row ids")
    out = {}
    for rid, pf in fwd.items():
        pr = rev[rid]
        keys = [k for k in pf if not k.startswith("_")]
        if set(keys) != {k for k in pr if not k.startswith("_")}:
            raise ValueError(f"row {rid}: option keys differ between orders")
        out[rid] = {k: (pf[k] + pr[k]) / 2 for k in keys}
    return out


def load_probs(path):
    """Prediction jsonl -> {id: {option: p}} (private '_' keys dropped, rows renormalised to sum 1)."""
    out = {}
    for r in read_jsonl(path):
        p = {k: float(v) for k, v in r["probs"].items() if not k.startswith("_")}
        s = sum(p.values())
        if s <= 0:
            raise ValueError(f"row {r['id']}: probabilities sum to {s}")
        out[r["id"]] = {k: v / s for k, v in p.items()}
    return out


def load_both_orders(fwd_path, rev_path):
    f, r = load_probs(fwd_path), load_probs(rev_path)
    return f, r, combine_orders(f, r)


def argmax_option(probs: dict):
    """Argmax with a fixed tie rule: highest p, ties broken by the option text (lexicographic) so it is order-free."""
    return sorted(probs.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


# ------------------------------------------------------------------ statistics
def wilson(k: int, n: int, z: float = 1.959964):
    """Wilson score interval for k successes in n."""
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def max_k_with_wilson_upper_below(n: int, bound: float):
    """Largest k such that the Wilson 95% upper bound of k/n is strictly below `bound` (None if none)."""
    best = None
    for k in range(n + 1):
        if wilson(k, n)[1] < bound:
            best = k
        else:
            break
    return best


def auroc(y, s):
    """Rank AUROC with mid-ranks for ties (equals sklearn.roc_auc_score)."""
    y = np.asarray(y)
    s = np.asarray(s, float)
    npos, nneg = int((y == 1).sum()), int((y == 0).sum())
    if npos == 0 or nneg == 0:
        return float("nan")
    order = np.argsort(s, kind="mergesort")
    ranks = np.empty(len(s))
    ss = s[order]
    i = 0
    while i < len(ss):
        j = i
        while j + 1 < len(ss) and ss[j + 1] == ss[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    return float((ranks[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg))


def tpr_at_fpr_sameset(y, s, target):
    """Liu's number (analysis/compute_all.py tpr_at): the best TPR on the ROC curve with FPR <= target, the threshold
    chosen on the SAME set. Ties are moved together (flag when score >= threshold). Labelled FAVOURABLE in our reports."""
    y = np.asarray(y)
    s = np.asarray(s, float)
    npos, nneg = int((y == 1).sum()), int((y == 0).sum())
    best = 0.0
    for t in sorted(set(s.tolist()), reverse=True):
        flag = s >= t
        fpr = (flag & (y == 0)).sum() / nneg
        if fpr <= target:
            best = max(best, (flag & (y == 1)).sum() / npos)
    return float(best)


def strict_threshold_for_fpr(benign_scores, target=0.01):
    """PRE-REGISTERED threshold rule (v3.1 skeptic 16). With n benign scores sorted descending and k = floor(target*n),
    the threshold is the (k+1)-th largest benign score and an item is flagged only if score > threshold (STRICT), so
    ties at the threshold are NOT flagged and the benign FPR on the fit set is <= k/n <= target. If n*target < 1
    (k = 0) the threshold is the largest benign score."""
    b = np.sort(np.asarray(benign_scores, float))[::-1]
    if len(b) == 0:
        raise ValueError("no benign scores to fit a threshold")
    k = int(math.floor(target * len(b) + 1e-12))
    return float(b[min(k, len(b) - 1)])


def tpr_fpr_at(y, s, thr):
    y = np.asarray(y)
    flag = np.asarray(s, float) > thr
    return float(flag[y == 1].mean()), float(flag[y == 0].mean())


def cluster_bootstrap(stat_fn, cluster_ids, n_boot=2000, seed=0):
    """Percentile 95% CI of stat_fn(index_array) resampling whole clusters (e.g. tasks) with replacement."""
    cluster_ids = np.asarray(cluster_ids)
    uniq = sorted(set(cluster_ids.tolist()))
    where = {c: np.where(cluster_ids == c)[0] for c in uniq}
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_boot):
        pick = rng.integers(0, len(uniq), len(uniq))
        idx = np.concatenate([where[uniq[i]] for i in pick])
        v = stat_fn(idx)
        if v == v:
            vals.append(v)
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


def paired_diff_ci(correct_a, correct_b, n_boot=10000, seed=0):
    """Paired bootstrap of mean(a) - mean(b) over items (a, b = 0/1 arrays on the same items). Returns point, lo, hi."""
    a, b = np.asarray(correct_a, float), np.asarray(correct_b, float)
    if a.shape != b.shape:
        raise ValueError("paired arrays differ in length")
    d = a - b
    rng = np.random.default_rng(seed)
    n = len(d)
    means = np.array([d[rng.integers(0, n, n)].mean() for _ in range(n_boot)])
    return float(d.mean()), float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


# ------------------------------------------------------------------ token counting
class TokenCounter:
    """Token counter for the pre-registered compaction budgets. With a tokenizer directory (env C21_TOKENIZER, the
    Qwen3.5 tokenizer) counts are exact; otherwise len(text)/3.2 rounded up (the repo's own rough rule, decoder_io.predict)
    and `exact` is False so the run record says so."""

    def __init__(self, tokenizer_dir=None):
        tokenizer_dir = tokenizer_dir or os.environ.get("C21_TOKENIZER")
        self.tok = None
        self.exact = False
        self.source = "chars/3.2 estimate"
        if tokenizer_dir:
            try:
                from transformers import AutoTokenizer
                self.tok = AutoTokenizer.from_pretrained(tokenizer_dir)
                self.exact = True
                self.source = f"tokenizer:{tokenizer_dir}"
            except Exception:
                self.tok = None

    def __call__(self, text: str) -> int:
        if self.tok is not None:
            return len(self.tok(text, add_special_tokens=False)["input_ids"])
        return int(math.ceil(len(text) / 3.2))


def fmt_pct(x, nd=1):
    return f"{100 * x:.{nd}f}"
