"""Shared helpers for the domain_classification golden builders (CPU-only, deterministic)."""
import collections
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent.parent
RAW = LEAN / "data" / "v14_parts" / "raw"
DEFS = LEAN / "data" / "v14_parts" / "defs"
CACHE = HERE / "cache"
MANIFEST = LEAN / "golden_src" / "MANIFEST.jsonl"
FAMILY = "domain_classification"
EDGE_TAGS = {"negation", "double_negation", "exception", "missing_info", "conflicting_evidence", "temporal",
             "numeric", "units", "quantifier", "hypothetical", "reported_speech", "sarcasm", "implicit",
             "long_context", "table", "multi_hop", "ambiguous"}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url, path, sha=None):
    path = Path(path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".part")
        import requests
        with requests.get(url, headers={"User-Agent": "Mozilla/5.0 (golden-builder)"}, stream=True, timeout=120) as r:
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


def ngrams(t, n=12):
    w = norm(t).split()
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}


class NearDup:
    """Exact (normalised) + near-exact (MinHash LSH over word 5-gram shingles, Jaccard >= thr) detector."""

    def __init__(self, thr=0.7, k=32, bands=8):
        self.thr, self.k, self.bands = thr, k, bands
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
        sh = shingles(text)
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


def write_rows(key, rows):
    RAW.mkdir(parents=True, exist_ok=True)
    out = RAW / f"{key}.jsonl"
    for r in rows:
        assert r["gold"] in r["options"], r
        assert r["state"].strip() and r["instructions"].strip()
        e = r["meta"].get("edge")
        assert e is None or all(x in EDGE_TAGS for x in e.split(",")), e
        if r["soft"] is not None:
            assert abs(sum(r["soft"].values()) - 1) < 1e-6
    states = [norm(r["state"] + " || " + r["instructions"]) for r in rows]
    assert len(set(states)) == len(states), "duplicate state+instruction"
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return out


def write_defs(name, defs):
    DEFS.mkdir(parents=True, exist_ok=True)
    out = DEFS / f"{name}.json"
    with open(out, "w") as f:
        json.dump(defs, f, ensure_ascii=False, indent=1)
    return out


def summary(rows):
    by_q = collections.defaultdict(list)
    for r in rows:
        by_q[r["instructions"] if len(r["options"]) == 2 else "choice:" + r["meta"].get("config", "")].append(r)
    print(f"rows={len(rows)}")
    yn = [r for r in rows if r["options"] == ["yes", "no"]]
    if yn:
        print(f"yes/no rows={len(yn)} yes share={sum(r['gold'] == 'yes' for r in yn) / len(yn):.3f}")
    ch = [r for r in rows if r["options"] != ["yes", "no"]]
    if ch:
        c = collections.Counter(r["gold"] for r in ch)
        print(f"choice rows={len(ch)} labels={len(c)} max share={max(c.values()) / len(ch):.3f}")
    e = collections.Counter(r["meta"].get("edge") for r in rows)
    print("edge:", dict(e.most_common()))
    L = sorted(len(r["state"]) for r in rows)
    print("state len min/med/max:", L[0], L[len(L) // 2], L[-1])


LEXGLUE_REV = "c23fdff1a6bf74e0e1a71cb86f1e781d37da888c"   # coastalcph/lex_glue (OHS-1 LEDGAR; SCOTUS is a forbidden label-NLI task)
LEGALBENCH_REV = "daec8237410aa23e3faf4bc41ad8b3a7e1696826"  # nguha/legalbench (every task forbidden)
FORBIDDEN_LEGAL = {
    "lexglue_scotus": [f"scotus/{s}-00000-of-00001.parquet" for s in ("train", "validation", "test")],
    "lexglue_ledgar": [f"ledgar/{s}-00000-of-00001.parquet" for s in ("train", "validation", "test")],
    "lexglue_casehold_evaltest": [f"case_hold/{s}-00000-of-00001.parquet" for s in ("validation", "test")],
}


def _stable(g):
    return int.from_bytes(hashlib.blake2b(g.encode(), digest_size=8).digest(), "little")


def stable_ngrams(t, n=12):
    w = norm(t).split()
    return {_stable(" ".join(w[i:i + n])) for i in range(max(0, len(w) - n + 1))}


def _forbidden_legal_texts(groups):
    """Yield every text of the forbidden legal sources (decontamination only; nothing is used as data).
    lex_glue parquet files at LEXGLUE_REV; LegalBench: every data/*/*.tsv at LEGALBENCH_REV (all string columns)."""
    import pandas as pd
    import requests
    d = CACHE / "forbidden_legal"
    shas = {}
    for grp in groups:
        if grp == "legalbench_all":
            listing = requests.get(f"https://huggingface.co/api/datasets/nguha/legalbench/tree/{LEGALBENCH_REV}/data"
                                   "?recursive=true", timeout=120).json()
            files = sorted(x["path"] for x in listing if x["type"] == "file" and x["path"].endswith(".tsv"))
            for fp in files:
                p, sha = fetch(f"https://huggingface.co/datasets/nguha/legalbench/resolve/{LEGALBENCH_REV}/{fp}",
                               d / "legalbench" / fp.replace("/", "__"))
                shas[fp] = sha
                df = pd.read_csv(p, sep="\t", dtype=str, keep_default_na=False, quoting=3, on_bad_lines="skip")
                for col in df.columns:
                    for t in df[col]:
                        if len(t) > 60:
                            yield t
            continue
        for fp in FORBIDDEN_LEGAL[grp]:
            p, sha = fetch(f"https://huggingface.co/datasets/coastalcph/lex_glue/resolve/{LEXGLUE_REV}/{fp}",
                           d / "lex_glue" / fp.replace("/", "__"))
            shas[fp] = sha
            df = pd.read_parquet(p)
            for col in ("text", "context", "endings"):
                if col in df.columns:
                    for t in df[col]:
                        if isinstance(t, str):
                            yield t
                        else:
                            yield from (x for x in t)
    (d / "shas.json").write_text(json.dumps(shas, indent=1, sort_keys=True))


def forbidden_legal_hits(id2texts, groups, n=12):
    """Return the ids whose texts share any word n-gram (normalised) with a forbidden legal source.
    Memory-lean: only the n-grams of our candidate texts are held; forbidden texts are streamed."""
    mine = {}
    allg = set()
    for i, texts in id2texts.items():
        g = set()
        for t in texts:
            g |= stable_ngrams(t, n)
        mine[i] = g
        allg |= g
    hit = set()
    for t in _forbidden_legal_texts(groups):
        w = norm(t).split()
        for k in range(max(0, len(w) - n + 1)):
            h = _stable(" ".join(w[k:k + n]))
            if h in allg:
                hit.add(h)
    return {i for i, g in mine.items() if g & hit}


def append_manifest(rec):
    """Append-only (other families write to the same file concurrently): one O_APPEND write per record.
    Skips if a record with this key is already present."""
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
