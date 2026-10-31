"""Shared helpers for the large_labelsets golden builders (round 2; CPU-only, deterministic).

Adapted from golden_src/domain_classification/common.py (fetch + sha256 pin, exact/near-exact dedup, row checks,
append-only MANIFEST writer) plus two helpers used by every builder in this family:
  * oof_filter   : out-of-fold TF-IDF + logistic-regression noise filter. It only DROPS rows whose human label is
                   confidently contradicted by the rest of the data (never relabels, never used to create labels).
  * option_subset: picks the 8-40 options shown in one row: the gold, the most confusable labels (hand-written
                   confusion groups), then a seeded random fill from the rest of the label set.
"""
import collections
import hashlib
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent.parent
RAW = LEAN / "data" / "v14_parts" / "raw"
DEFS = LEAN / "data" / "v14_parts" / "defs"
CACHE = HERE / "cache"
MANIFEST = LEAN / "golden_src" / "MANIFEST.jsonl"
FAMILY = "large_labelsets"
EDGE_TAGS = {"negation", "double_negation", "exception", "missing_info", "conflicting_evidence", "temporal",
             "numeric", "units", "quantifier", "hypothetical", "reported_speech", "sarcasm", "implicit",
             "long_context", "table", "multi_hop", "ambiguous"}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url, path, sha=None, headers=None):
    path = Path(path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".part")
        import requests
        h = {"User-Agent": "Mozilla/5.0 (golden-builder)"}
        h.update(headers or {})
        with requests.get(url, headers=h, stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(tmp, "wb") as f:
                for b in r.iter_content(1 << 20):
                    f.write(b)
        tmp.rename(path)
    got = sha256_file(path)
    if sha is not None and got != sha:
        sys.exit(f"sha256 mismatch for {path}: {got} != {sha}")
    return path, got


def norm(t):
    return re.sub(r"\W+", " ", t.lower()).strip()


def shingles(t, n=5):
    w = norm(t).split()
    if len(w) < n:
        return {" ".join(w)}
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


class NearDup:
    """Exact (normalised) + near-exact (MinHash LSH over word 5-gram shingles, Jaccard >= thr) detector."""

    def __init__(self, thr=0.7, k=32, bands=8, n=5):
        self.thr, self.k, self.bands, self.n = thr, k, bands, n
        self.r = k // bands
        self.exact = set()
        self.buckets = collections.defaultdict(list)
        self.sh = []
        self.seeds = [int(hashlib.md5(str(i).encode()).hexdigest()[:8], 16) for i in range(k)]

    def _sig(self, sh):
        hs = [int(hashlib.md5(s.encode()).hexdigest()[:12], 16) for s in sh]
        return [min((h ^ sd) for h in hs) for sd in self.seeds]

    def seen(self, text, add=True):
        n = norm(text)
        if n in self.exact:
            return True
        sh = shingles(text, self.n)
        sig = self._sig(sh)
        keys = [(b, tuple(sig[b * self.r:(b + 1) * self.r])) for b in range(self.bands)]
        cands = set()
        for key in keys:
            cands.update(self.buckets.get(key, ()))
        for c in cands:
            o = self.sh[c]
            if len(sh & o) / max(1, len(sh | o)) >= self.thr:
                return True
        if add:
            self.exact.add(n)
            idx = len(self.sh)
            self.sh.append(sh)
            for key in keys:
                self.buckets[key].append(idx)
        return False


def oof_filter(texts, labels, seed, folds=5, min_gold=0.12, max_other=0.75, word=True, char=True):
    """Out-of-fold TF-IDF + LR probabilities. Returns (keep_mask, p_gold list, top_other list).
    A row is dropped when the held-out model gives its human label p < min_gold AND some other label p > max_other.
    Pure CPU (scikit-learn); used only to drop likely label noise, never to assign labels."""
    import numpy as np
    from scipy.sparse import hstack
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold

    labs = sorted(set(labels))
    li = {l: i for i, l in enumerate(labs)}
    y = np.array([li[l] for l in labels])
    cnt = collections.Counter(y)
    n_splits = max(2, min(folds, min(cnt.values()))) if min(cnt.values()) >= 2 else 2
    P = np.zeros((len(texts), len(labs)))
    # classes with < n_splits members cannot be stratified; they get p_gold = 1 (never dropped)
    rare = {c for c, k in cnt.items() if k < n_splits}
    idx = np.array([i for i in range(len(texts)) if y[i] not in rare])
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    for tr, te in skf.split(idx, y[idx]):
        tr, te = idx[tr], idx[te]
        vecs = []
        if word:
            vecs.append(TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, max_features=200000))
        if char:
            vecs.append(TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=3, sublinear_tf=True,
                                        max_features=300000))
        Xtr = hstack([v.fit_transform([texts[i] for i in tr]) for v in vecs]).tocsr()
        Xte = hstack([v.transform([texts[i] for i in te]) for v in vecs]).tocsr()
        clf = LogisticRegression(C=4.0, max_iter=2000, class_weight="balanced")
        clf.fit(Xtr, y[tr])
        pr = clf.predict_proba(Xte)
        full = np.zeros((len(te), len(labs)))
        full[:, clf.classes_] = pr
        P[te] = full
    keep, pg, po = [], [], []
    for i in range(len(texts)):
        if y[i] in rare:
            keep.append(True), pg.append(1.0), po.append(0.0)
            continue
        g = P[i, y[i]]
        o = max(P[i, j] for j in range(len(labs)) if j != y[i])
        pg.append(float(g)), po.append(float(o))
        keep.append(not (g < min_gold and o > max_other))
    return keep, pg, po


def option_subset(gold, all_labels, confusers, rng, lo=8, hi=40):
    """gold + its hand-listed confusers (in order) + seeded random fill; size drawn uniformly in [lo, hi]
    (capped by the label-set size). The returned list is shuffled."""
    n = min(len(all_labels), rng.randint(lo, hi))
    opts = [gold]
    for c in confusers:
        if c != gold and c in all_labels and c not in opts and len(opts) < n:
            opts.append(c)
    rest = [l for l in all_labels if l not in opts]
    rng.shuffle(rest)
    opts += rest[:max(0, n - len(opts))]
    rng.shuffle(opts)
    return opts


def final_dedup(rows, thr=0.7, n=3):
    """Exact (non-LSH) near-duplicate pass over the finished rows: word n-gram Jaccard >= thr on the state with
    digits removed (ages, sizes, dates and codes do not make two templated texts different). Keeps the first row
    in list order, drops later near-copies. Deterministic, CPU only. Added by the round-2 reviewer because the
    MinHash LSH in NearDup (bands of 4) misses many pairs at Jaccard 0.5-0.7."""
    inv = collections.defaultdict(list)
    kept, sh = [], []
    dropped = 0
    for r in rows:
        s = shingles(re.sub(r"\d+", " ", r["state"]), n)
        cnt = collections.Counter(j for g in s for j in inv[g])
        if any(c / max(1, len(s | sh[j])) >= thr for j, c in cnt.items()):
            dropped += 1
            continue
        j = len(sh)
        sh.append(s)
        for g in s:
            inv[g].append(j)
        kept.append(r)
    print(f"final_dedup: dropped {dropped} near-duplicate rows (word {n}-gram Jaccard >= {thr})")
    return kept


def round_robin(pools, n, rng=None):
    labels = sorted(pools)
    out, i = [], 0
    while len(out) < n and any(pools[k] for k in labels):
        k = labels[i % len(labels)]
        if pools[k]:
            out.append(pools[k].pop())
        i += 1
    return out


def write_rows(key, rows):
    RAW.mkdir(parents=True, exist_ok=True)
    out = RAW / f"{key}.jsonl"
    for r in rows:
        assert r["gold"] in r["options"], r
        assert len(set(r["options"])) == len(r["options"]), r["options"]
        assert r["state"].strip() and r["instructions"].strip()
        assert r["meta"]["split"] == "train"
        e = r["meta"].get("edge")
        assert e is None or all(x in EDGE_TAGS for x in e.split(",")), e
        if r["soft"] is not None:
            assert abs(sum(r["soft"].values()) - 1) < 1e-6
    states = [norm(r["state"] + " || " + r["instructions"]) for r in rows]
    assert len(set(states)) == len(states), "duplicate state+instruction"
    assert len({norm(r["state"]) for r in rows}) == len(rows), "duplicate state"
    assert len({r["rid"] for r in rows}) == len(rows), "duplicate rid"
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return out


def write_defs(name, defs):
    DEFS.mkdir(parents=True, exist_ok=True)
    out = DEFS / f"{name}.json"
    for k, v in defs.items():
        assert v and len(v.split()) <= 60, (k, len(v.split()))
    with open(out, "w") as f:
        json.dump(defs, f, ensure_ascii=False, indent=1)
    return out


def summary(rows, by=lambda r: r["meta"].get("config", "")):
    print(f"rows={len(rows)}")
    groups = collections.defaultdict(list)
    for r in rows:
        groups[by(r)].append(r)
    for g, rs in sorted(groups.items()):
        c = collections.Counter(r["gold"] for r in rs)
        no = [len(r["options"]) for r in rs]
        print(f"[{g}] rows={len(rs)} labels={len(c)} max share={max(c.values()) / len(rs):.3f} "
              f"options min/med/max={min(no)}/{sorted(no)[len(no) // 2]}/{max(no)}")
    e = collections.Counter(r["meta"].get("edge") for r in rows)
    print("edge:", dict(e.most_common()))
    L = sorted(len(r["state"]) for r in rows)
    print("state len min/med/max:", L[0], L[len(L) // 2], L[-1])
    c = collections.Counter(r["gold"] for r in rows)
    print(f"overall max class share={max(c.values()) / len(rows):.3f}")


def append_manifest(rec):
    """Append-only (other families write to the same file concurrently): one O_APPEND write per record.
    Replaces nothing; skips if a record with this key is already present."""
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    if MANIFEST.exists():
        for ln in MANIFEST.read_text().splitlines():
            try:
                if ln.strip() and json.loads(ln).get("key") == rec["key"]:
                    print("manifest: key already present, not appended:", rec["key"])
                    return
            except Exception:
                pass
    with open(MANIFEST, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def show(rows, k=5, seed=0):
    rng = random.Random(seed)
    for r in rng.sample(rows, min(k, len(rows))):
        print("=" * 100)
        print("rid:", r["rid"], "| edge:", r["meta"].get("edge"))
        print("STATE:", r["state"])
        print("Q:", r["instructions"])
        print("OPTIONS:", r["options"])
        print("GOLD:", r["gold"], "| orig:", r["meta"]["orig_label"])
