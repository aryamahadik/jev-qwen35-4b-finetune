"""Shared helpers for the moral_social_norms golden builders (CPU-only, deterministic).

Output format follows golden_src/GOLDEN_SPEC.md: data/v14_parts/raw/<key>.jsonl + data/v14_parts/defs/<key>[__qid].json,
and one MANIFEST record per key (append-only; other families write the same file concurrently).
"""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent.parent
RAW = LEAN / "data" / "v14_parts" / "raw"
DEFS = LEAN / "data" / "v14_parts" / "defs"
CACHE = HERE / "cache"
MANIFEST = LEAN / "golden_src" / "MANIFEST.jsonl"
FAMILY = "moral_social_norms"
EDGE_TAGS = {"negation", "double_negation", "exception", "missing_info", "conflicting_evidence", "temporal",
             "numeric", "units", "quantifier", "hypothetical", "reported_speech", "sarcasm", "implicit",
             "long_context", "table", "multi_hop", "ambiguous"}

NEG_RE = re.compile(r"\b(not|no|never|nobody|nothing|none|neither|nor|without|n't)\b|n't\b", re.I)
EXC_RE = re.compile(r"\b(unless|except|excepting|even if|even when|even though|as long as|only if|only when|"
                    r"provided that|so long as)\b", re.I)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url, path, sha=None):
    """Download once into cache/ and verify the pinned sha256."""
    path = Path(path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".part")
        import requests
        with requests.get(url, headers={"User-Agent": "Mozilla/5.0 (golden-builder)"}, stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(tmp, "wb") as f:
                for b in r.iter_content(1 << 20):
                    f.write(b)
        tmp.rename(path)
    got = sha256_file(path)
    if sha is not None and got != sha:
        sys.exit(f"sha256 mismatch for {path}: {got} != {sha}")
    return path


def norm(t):
    return re.sub(r"\W+", " ", t.lower()).strip()


def toks(t):
    return norm(t).split()


def shingles(t, n=5):
    w = toks(t)
    if len(w) < n:
        return {" ".join(w)}
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


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


class TokenSetIndex:
    """Near-match of short texts (norms / rules of thumb) by token-set Jaccard via an inverted index."""

    STOP = set("a an the to of and or is it its it's be are for in on at your you their they them with as that "
               "this if when".split())

    def __init__(self, texts):
        self.sets = []
        self.inv = collections.defaultdict(list)
        self.exact = set()
        for t in texts:
            s = frozenset(toks(t))
            if not s:
                continue
            self.exact.add(" ".join(toks(t)))
            i = len(self.sets)
            self.sets.append(s)
            for w in s - self.STOP:
                self.inv[w].append(i)

    def match(self, text, thr=0.7):
        if " ".join(toks(text)) in self.exact:
            return True
        s = frozenset(toks(text))
        content = s - self.STOP
        if not content:
            return False
        # candidates share one of the two rarest content words (deterministic tie-break by the word itself)
        rare = sorted(content, key=lambda w: (len(self.inv.get(w, ())), w))[:2]
        cands = sorted({i for w in rare for i in self.inv.get(w, ())})
        for i in cands:
            o = self.sets[i]
            if len(s & o) / len(s | o) >= thr:
                return True
        return False


def edge_join(tags):
    tags = [t for t in dict.fromkeys(tags) if t]
    for t in tags:
        assert t in EDGE_TAGS, t
    return ",".join(tags) if tags else None


def check_rows(rows):
    for r in rows:
        assert set(r) == {"key", "rid", "state", "instructions", "options", "gold", "soft", "meta"}, r.keys()
        assert r["gold"] in r["options"], r
        assert r["state"].strip() and r["instructions"].strip()
        assert r["meta"]["split"] == "train"
        e = r["meta"].get("edge")
        assert e is None or all(x in EDGE_TAGS for x in e.split(",")), e
        if r["soft"] is not None:
            assert set(r["soft"]) == set(r["options"]), r["soft"]
            assert abs(sum(r["soft"].values()) - 1) < 1e-6, r["soft"]
    keys = [norm(r["state"]) + " || " + norm(r["instructions"]) for r in rows]
    assert len(set(keys)) == len(keys), "duplicate state+instruction"
    rids = [r["rid"] for r in rows]
    assert len(set(rids)) == len(rids), "duplicate rid"


def write_rows(key, rows):
    check_rows(rows)
    RAW.mkdir(parents=True, exist_ok=True)
    out = RAW / f"{key}.jsonl"
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return out


def write_defs(name, defs):
    DEFS.mkdir(parents=True, exist_ok=True)
    for k, v in defs.items():
        assert len(v.split()) <= 48, (name, k, len(v.split()))
    out = DEFS / f"{name}.json"
    with open(out, "w") as f:
        json.dump(defs, f, ensure_ascii=False, indent=1)
    return out


def summary(rows):
    print(f"rows={len(rows)}")
    yn = [r for r in rows if r["options"] == ["yes", "no"]]
    if yn:
        print(f"yes/no rows={len(yn)} yes share={sum(r['gold'] == 'yes' for r in yn) / len(yn):.3f}")
    ch = [r for r in rows if r["options"] != ["yes", "no"]]
    if ch:
        c = collections.Counter(r["gold"] for r in ch)
        print(f"choice rows={len(ch)} labels={len(c)} max share={max(c.values()) / len(ch):.3f}")
    q = collections.Counter((r["meta"].get("defs") or r["meta"].get("config"), r["gold"]) for r in rows)
    print("by question/gold:", dict(sorted(q.items())))
    e = collections.Counter(t for r in rows for t in (r["meta"].get("edge") or "none").split(","))
    print("edge:", dict(e.most_common()))
    print("soft coverage:", sum(r["soft"] is not None for r in rows), "/", len(rows))
    L = sorted(len(r["state"]) for r in rows)
    print("state len min/med/max:", L[0], L[len(L) // 2], L[-1])


def yesno_share(rows):
    yn = [r for r in rows if r["options"] == ["yes", "no"]]
    return round(sum(r["gold"] == "yes" for r in yn) / len(yn), 4) if yn else None


def edge_tags(rows):
    return sorted({t for r in rows for t in (r["meta"].get("edge") or "").split(",") if t})


def append_manifest(rec):
    """Upsert this family's record for rec['key'].
    New key -> one O_APPEND write (other families append to the same file concurrently).
    Existing key with a stale record (a re-run of our own builder) -> the file is rewritten without that one line
    and with the new record; the snapshot is re-checked right before the atomic replace so that a concurrent
    append by another family is never lost (retry on change)."""
    import os
    import time
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(rec, ensure_ascii=False)
    for _ in range(20):
        text = MANIFEST.read_text() if MANIFEST.exists() else ""
        lines = text.splitlines()
        mine = []
        for i, ln in enumerate(lines):
            try:
                if ln.strip() and json.loads(ln).get("key") == rec["key"]:
                    mine.append(i)
            except Exception:
                pass
        if not mine:
            with open(MANIFEST, "a") as f:
                f.write(line + "\n")
            return
        if len(mine) == 1 and lines[mine[0]] == line:
            return
        for i in mine:
            assert json.loads(lines[i]).get("family") == FAMILY, "refusing to replace another family's record"
        new = [ln for i, ln in enumerate(lines) if i not in set(mine)] + [line]
        tmp = MANIFEST.with_suffix(".jsonl.tmp_msn")
        tmp.write_text("\n".join(new) + "\n")
        if (MANIFEST.read_text() if MANIFEST.exists() else "") == text:
            os.replace(tmp, MANIFEST)
            return
        tmp.unlink()
        time.sleep(0.2)
    raise RuntimeError("manifest kept changing; not updated")


def show(rows, n=5, seed=0):
    import random
    rng = random.Random(seed)
    for r in rng.sample(rows, min(n, len(rows))):
        print("-" * 100)
        print("RID:", r["rid"], "| Q:", r["instructions"])
        print("STATE:", r["state"][:900])
        print("GOLD:", r["gold"], "| soft:", r["soft"], "| edge:", r["meta"].get("edge"),
              "| orig:", json.dumps(r["meta"].get("orig_label"))[:200])
