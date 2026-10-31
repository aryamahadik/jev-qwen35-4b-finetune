"""Shared helpers for the calibration_distributions golden builders (v14). CPU-only, deterministic, no model calls.

Every key in this family carries REAL annotator vote shares in `soft` (per-annotator judgements, binarised per
annotator where the scale is ordinal, exactly as documented in each builder).

- fetch(): pinned URL download into golden_src/calibration_distributions/cache/<key>/ with a sha256 check.
- decon(): drops candidate records whose texts share an exact normalised text (>= 6 words) or a 10-word run with
  (a) every premise of tasksource/zero-shot-label-nli (forbidden: all 152 tasks, all splits; read only to drop
  overlaps), (b) every local *.jsonl under lean/ and ../data except held-out/eval files (ohs*, preds*, results*),
  caches and data/v14_parts (other golden parts are checked by cross_v14() and cross-deduped at compile time),
  including our own v13 breadth parts, and (c) the JevBench public splits. OHS files are never opened.
  Verdicts are cached per text hash in cache/_decon/<key>.json (keyed on the scanned file list + sizes).
- cross_v14(): overlap check against the OTHER golden v14 raw parts already written.
- NearDup: exact + near-exact (word 5-gram MinHash, Jaccard >= thr) duplicate detector.
- write_outputs() / manifest_record() / append_manifest(): raw rows, defs and the MANIFEST record (file-locked,
  replaces an older record of the same key so reruns do not duplicate it).
"""
import collections
import fcntl
import hashlib
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent            # golden_src/calibration_distributions
GOLDEN = HERE.parent                               # golden_src
LEAN = GOLDEN.parent                               # lean
ROOT = LEAN.parent                                 # opendecide-data
JEV = ROOT.parent                                  # jev
CACHE = HERE / "cache"
RAW_DIR = LEAN / "data" / "v14_parts" / "raw"
DEFS_DIR = LEAN / "data" / "v14_parts" / "defs"
MANIFEST = GOLDEN / "MANIFEST.jsonl"
FAMILY = "calibration_distributions"
YN = ["yes", "no"]
SEED = 20261101
EDGE_TAGS = {"negation", "double_negation", "exception", "missing_info", "conflicting_evidence", "temporal",
             "numeric", "units", "quantifier", "hypothetical", "reported_speech", "sarcasm", "implicit",
             "long_context", "table", "multi_hop", "ambiguous"}

HF_HUB = Path.home() / ".cache" / "huggingface" / "hub"
LABEL_NLI_REV = "ee693dba923b5d5484aa9232b7357c5e45dd39b8"
LABEL_NLI_DIR = HF_HUB / f"datasets--tasksource--zero-shot-label-nli/snapshots/{LABEL_NLI_REV}/data"
LABEL_NLI_URL = "https://huggingface.co/datasets/tasksource/zero-shot-label-nli/resolve/{rev}/data/{name}"
LABEL_NLI_FILES = {  # name -> sha256 (LFS oid)
    "test-00000-of-00001-c260d1ee78ad6397.parquet": "a7bc5319f8af2704adaba91a3aef8290913e2e3651f46225130e4bfd1cc0864d",
    "train-00000-of-00002-970172c89e89b5df.parquet": "aa0fe36796bc0ac46755738128dc101918303fed9c9a5c48aeced4d6060745b5",
    "train-00001-of-00002-509e762f01abeb95.parquet": "2d4ee59ed8c9d9e0e4cdd4b89aad0e8b4d00c68e7ef1c326f97bd2e55e1eb556",
    "validation-00000-of-00001-79d9ba1d8f02bef0.parquet": "f45c234013c9d994c39f9907403056564e120ef67b6492cc20faf5fac826e5ca",
}
JEVBENCH_PUBLIC = JEV / "bench" / "jevbench" / "datasets" / "public"
RUN = 10          # word-run length for overlap
MIN_EXACT = 6     # exact-match only for texts of at least this many words


# ----------------------------------------------------------------------------------------------- download
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url, path, sha):
    """Download once into cache/ and verify the pinned sha256 (sha=None only while pinning a new file)."""
    path = Path(path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        import requests
        tmp = path.with_suffix(path.suffix + ".part")
        with requests.get(url, headers={"User-Agent": "opendecide-golden-builder"}, stream=True, timeout=600) as r:
            r.raise_for_status()
            with open(tmp, "wb") as f:
                for b in r.iter_content(1 << 20):
                    f.write(b)
        tmp.rename(path)
    got = sha256(path)
    if sha is None:
        print(f"PIN {path.name}: {got}")
    elif got != sha:
        sys.exit(f"sha256 mismatch for {path}: {got} != {sha}")
    return path


# ----------------------------------------------------------------------------------------------- text utils
def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", str(t).lower()).strip()


def words(t):
    return re.findall(r"[a-z0-9]+", str(t).lower())


def clean(t):
    """Whitespace tidy only (no rewording)."""
    t = str(t).replace(" ", " ").replace("​", "").replace("\r", "")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


NEG = re.compile(r"\b(not|no|never|none|nobody|nothing|neither|nor|without|cannot)\b|n't\b|n’t\b", re.I)
QUANT = re.compile(r"\b(all|every|each|only|most|none of|at least|at most|exactly|more than|less than|fewer than|"
                   r"always|any)\b", re.I)
NUM = re.compile(r"(?<![\w-])\d+(?:[.,]\d+)*(?:%|(?![\w-]))")
TEMP = re.compile(r"\b(yesterday|tomorrow|tonight|last (week|month|year|night)|next (week|month|year)|ago|until|"
                  r"since|(19|20)\d\d)\b", re.I)
HYPO = re.compile(r"\b(if|would|could|might|unless|suppose|imagine|what if)\b", re.I)
REPORTED = re.compile(r"\b(said|says|according to|claims?|claimed|told|reported|announced)\b", re.I)


def neg_count(t):
    return len(NEG.findall(t))


def edge_join(tags):
    tags = [t for t in dict.fromkeys(tags) if t]
    for t in tags:
        assert t in EDGE_TAGS, t
    return ",".join(tags) if tags else None


# ----------------------------------------------------------------------------------------------- near-dup
def shingles(t, n=5):
    w = words(t)
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
        for c in sorted(cands):
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


# ----------------------------------------------------------------------------------------------- decontamination
def _is_skipped(rel_parts):
    parts = [x.lower() for x in rel_parts]
    if any(x.startswith(("ohs", "preds", "results")) for x in parts):
        return True
    if "cache" in parts or ".venv" in parts or "v14_parts" in parts or "node_modules" in parts:
        return True
    if parts and parts[-1] == "manifest.jsonl":  # golden MANIFEST (metadata only; changes on every family append)
        return True
    return False


def scan_files():
    fs = set()
    for base in (LEAN, ROOT / "data"):
        if not base.exists():
            continue
        for p in base.rglob("*.jsonl"):
            rel = p.relative_to(base)
            if _is_skipped(rel.parts):
                continue
            fs.add(p)
    if JEVBENCH_PUBLIC.exists():
        fs |= set(JEVBENCH_PUBLIC.glob("*.jsonl"))
    return sorted(fs)


def label_nli_files():
    out = []
    for name, sha in LABEL_NLI_FILES.items():
        p = LABEL_NLI_DIR / name
        if not p.exists():
            p = fetch(LABEL_NLI_URL.format(rev=LABEL_NLI_REV, name=name), CACHE / "_label_nli" / name, sha)
        out.append(p)
    return out


def _thash(t):
    return hashlib.sha1(" ".join(words(t)).encode()).hexdigest()


def decon(core, cache_name, verbose=True, extra_texts=None):
    """core: {rid: [text, ...]} -> {rid: reason} for records that overlap a forbidden / used / eval text.
    extra_texts: optional {reason: iterable of texts} also treated as forbidden (e.g. a benchmark test split)."""
    import pandas as pd
    files = scan_files()
    sig = hashlib.sha1(json.dumps([[str(p), p.stat().st_size] for p in files] + [LABEL_NLI_REV]).encode()).hexdigest()
    cpath = CACHE / "_decon" / f"{cache_name}.json"
    cached = {}
    if cpath.exists():
        blob = json.loads(cpath.read_text())
        if blob.get("sig") == sig:
            cached = blob["verdicts"]
    text_by_h = {}
    for rid, texts in core.items():
        for t in texts:
            text_by_h[_thash(t)] = t
    todo = {h: t for h, t in text_by_h.items() if h not in cached}
    if todo:
        exact = collections.defaultdict(set)
        owner = collections.defaultdict(set)
        for h, t in todo.items():
            w = words(t)
            if len(w) >= MIN_EXACT:
                exact[" ".join(w)].add(h)
            for i in range(len(w) - RUN + 1):
                owner[hash(tuple(w[i:i + RUN]))].add(h)
        found = {}

        def check_words(w, reason):
            if not w:
                return
            for h in exact.get(" ".join(w), ()):
                found.setdefault(h, reason)
            for i in range(len(w) - RUN + 1):
                k = hash(tuple(w[i:i + RUN]))
                if k in owner:
                    for h in owner[k]:
                        found.setdefault(h, reason)

        for p in label_nli_files():
            df = pd.read_parquet(p, columns=["premise"])
            for t in set(df["premise"].astype(str)):
                check_words(words(t), "label_nli")
        for p in files:
            reason = "jevbench" if JEVBENCH_PUBLIC in p.parents else f"local:{p.name}"
            with open(p, encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        check_words(words(line), reason)
                        continue
                    for s in _strings(obj):
                        if len(s) >= 20:
                            check_words(words(s), reason)
        for h in todo:
            cached[h] = found.get(h)
        cpath.parent.mkdir(parents=True, exist_ok=True)
        cpath.write_text(json.dumps({"sig": sig, "verdicts": cached}))
    hits = {}
    for rid, texts in core.items():
        for t in texts:
            v = cached.get(_thash(t))
            if v:
                hits.setdefault(rid, v)
                break
    if extra_texts:
        exact = collections.defaultdict(set)
        owner = collections.defaultdict(set)
        for rid, texts in core.items():
            for t in texts:
                w = words(t)
                if len(w) >= MIN_EXACT:
                    exact[" ".join(w)].add(rid)
                for i in range(len(w) - RUN + 1):
                    owner[hash(tuple(w[i:i + RUN]))].add(rid)
        for reason, texts in extra_texts.items():
            for t in texts:
                w = words(t)
                for rid in exact.get(" ".join(w), ()):
                    hits.setdefault(rid, reason)
                for i in range(len(w) - RUN + 1):
                    for rid in owner.get(hash(tuple(w[i:i + RUN])), ()):
                        hits.setdefault(rid, reason)
    if verbose:
        print(f"decon: {len(core)} records ({len(todo)} new texts scanned over {len(files)} files + label-NLI), "
              f"hits={len(hits)} {dict(collections.Counter(v.split(':')[0] for v in hits.values()))}")
    return hits


def _strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from _strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from _strings(v)


# Build order inside this family: a key is checked against every other family's parts and against the family keys
# EARLIER in this list (so the result does not depend on the order in which the builders happen to be re-run).
FAMILY_ORDER = ["megaveridicality", "meganegraising", "megaacceptability", "clickbait16", "clickbait17",
                "csc_sarcasm", "politeness_votes", "crowdtruth_mre"]


def cross_v14(core, own_keys, verbose=True, exact_min=MIN_EXACT):
    """{rid: [text, ...]} -> {rid: 'v14:<key>'} for records sharing an exact normalised text (>= 6 words) or a
    10-word run with a state in another golden v14 raw part (data/v14_parts/raw/*.jsonl, not our own keys, and not
    this family's keys that come later in FAMILY_ORDER)."""
    own_keys = set(own_keys)
    for k in own_keys & set(FAMILY_ORDER):
        own_keys |= set(FAMILY_ORDER[FAMILY_ORDER.index(k) + 1:])
    exact = collections.defaultdict(set)
    owner = collections.defaultdict(set)
    for rid, texts in core.items():
        for t in texts:
            w = words(t)
            if len(w) >= exact_min:
                exact[" ".join(w)].add(rid)
            for i in range(len(w) - RUN + 1):
                owner[hash(tuple(w[i:i + RUN]))].add(rid)
    hits = {}
    for p in sorted(RAW_DIR.glob("*.jsonl")):
        k = p.stem
        if k in own_keys:
            continue
        with open(p) as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                w = words(obj.get("state", ""))
                for rid in exact.get(" ".join(w), ()):
                    hits.setdefault(rid, f"v14:{k}")
                for i in range(len(w) - RUN + 1):
                    h = hash(tuple(w[i:i + RUN]))
                    if h in owner:
                        for rid in owner[h]:
                            hits.setdefault(rid, f"v14:{k}")
    if verbose:
        print(f"cross_v14: {len(core)} records, hits={len(hits)} {dict(collections.Counter(hits.values()))}")
    return hits


# ----------------------------------------------------------------------------------------------- soft labels
def soft_yes(n_yes, n_total, n_half=0):
    """Vote share for 'yes' from per-annotator judgements (a half vote counts 0.5, e.g. a scale midpoint)."""
    p = (n_yes + 0.5 * n_half) / n_total
    return {"yes": round(p, 4), "no": round(1 - p, 4)}


def fix_soft(soft):
    """Round and make the shares sum exactly to 1 (the rounding residue goes to the largest share)."""
    s = {k: round(v, 4) for k, v in soft.items()}
    top = max(s, key=lambda k: (s[k], k))
    s[top] = round(s[top] + (1 - sum(s.values())), 4)
    return s


# ----------------------------------------------------------------------------------------------- output
def check_rows(key, rows, defs_by_qid):
    assert rows, "no rows"
    rids = [r["rid"] for r in rows]
    assert len(set(rids)) == len(rids), "duplicate rid"
    states = [norm(r["state"]) for r in rows]
    assert all(states), "empty state"
    assert len(set(states)) == len(states), "duplicate state"
    for r in rows:
        assert set(r) == {"key", "rid", "state", "instructions", "options", "gold", "soft", "meta"}, r.keys()
        assert r["key"] == key
        assert r["instructions"].strip() and r["gold"] in r["options"], r
        assert r["meta"]["split"] == "train"
        assert r["meta"]["family"] == FAMILY
        e = r["meta"].get("edge")
        assert e is None or all(x in EDGE_TAGS for x in e.split(",")), e
        qid = r["meta"].get("defs")
        d = defs_by_qid[qid] if qid else defs_by_qid[None]
        assert all(o in d for o in r["options"]), (qid, r["options"])
        assert r["soft"] is not None, "calibration family: every row carries annotator vote shares"
        assert set(r["soft"]) == set(r["options"]), (r["soft"], r["options"])
        assert abs(sum(r["soft"].values()) - 1) < 1e-6, r["soft"]
        assert all(0 <= v <= 1 for v in r["soft"].values())
        # gold is the plurality of the vote shares
        assert r["soft"][r["gold"]] >= max(r["soft"].values()) - 1e-9, (r["gold"], r["soft"])
    yn = [r for r in rows if r["options"] == YN]
    if yn:
        share = sum(r["gold"] == "yes" for r in yn) / len(yn)
        assert 0.35 <= share <= 0.65, f"yes share {share:.3f}"
    ch = [r for r in rows if r["options"] != YN]
    if ch:
        top = max(collections.Counter(r["gold"] for r in ch).values()) / len(ch)
        assert top <= 0.5 + 1e-9, f"choice class share {top:.3f}"
    for qid, d in defs_by_qid.items():
        for k, v in d.items():
            assert len(v.split()) <= 48, (qid, k, len(v.split()))
    return True


def write_outputs(key, rows, defs_by_qid):
    """defs_by_qid: {None: {...default...}, "<qid>": {...}}"""
    check_rows(key, rows, defs_by_qid)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    DEFS_DIR.mkdir(parents=True, exist_ok=True)
    out = RAW_DIR / f"{key}.jsonl"
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    for qid, d in defs_by_qid.items():
        name = f"{key}.json" if qid is None else f"{key}__{qid}.json"
        with open(DEFS_DIR / name, "w") as f:
            json.dump(d, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return out


def summary(key, rows):
    yn = [r for r in rows if r["options"] == YN]
    ch = [r for r in rows if r["options"] != YN]
    edges = collections.Counter(t for r in rows for t in (r["meta"].get("edge") or "").split(",") if t)
    ys = (sum(r["gold"] == "yes" for r in yn) / len(yn)) if yn else None
    gold_ch = collections.Counter(r["gold"] for r in ch)
    lens = sorted(len(r["state"]) for r in rows)
    print(f"[{key}] rows={len(rows)} yesno={len(yn)} choice={len(ch)} yes_share={ys}")
    by_q = collections.defaultdict(collections.Counter)
    for r in rows:
        by_q[r["meta"].get("defs") or "default"][r["gold"]] += 1
    for q, c in sorted(by_q.items()):
        print(f"  q={q}: {dict(c)}")
    if ch:
        print(f"  choice gold dist: {dict(sorted(gold_ch.items()))}")
    print(f"  edge tags: {dict(edges.most_common())} (untagged {sum(not r['meta'].get('edge') for r in rows)})")
    print(f"  state chars: min={lens[0]} median={lens[len(lens) // 2]} max={lens[-1]}")
    pg = [r["soft"][r["gold"]] for r in rows]
    bins = collections.Counter(min(9, int(p * 10)) for p in pg)
    print(f"  mean soft prob of gold={sum(pg) / len(pg):.3f}; gold-share deciles: {dict(sorted(bins.items()))}")
    return {"yes_share": round(ys, 4) if ys is not None else None, "edges": edges, "n_yn": len(yn), "n_ch": len(ch)}


def show_samples(rows, n=5, seed=7):
    rng = random.Random(seed)
    for r in rng.sample(rows, min(n, len(rows))):
        print("-" * 100)
        print("RID:", r["rid"], "| edge:", r["meta"].get("edge"), "| defs:", r["meta"].get("defs"),
              "| orig:", json.dumps(r["meta"].get("orig_label"), ensure_ascii=False)[:300])
        print("STATE:\n" + r["state"][:2000])
        print("Q:", r["instructions"])
        print("OPTIONS:", r["options"], "| GOLD:", r["gold"], "| SOFT:", r["soft"])


def append_manifest(rec):
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.touch(exist_ok=True)
    with open(MANIFEST, "r+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            lines = [ln for ln in f.read().splitlines() if ln.strip()]
            keep = []
            for ln in lines:
                try:
                    o = json.loads(ln)
                    if o.get("key") == rec["key"]:
                        assert o.get("family") == FAMILY, "refusing to replace another family's record"
                        continue
                except json.JSONDecodeError:
                    pass
                keep.append(ln)
            keep.append(json.dumps(rec, ensure_ascii=False))
            f.seek(0)
            f.truncate()
            f.write("\n".join(keep) + "\n")
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def manifest_record(key, dataset, licence, rows, qtype, notes, stats):
    return {"key": key, "family": FAMILY, "dataset": dataset, "licence": licence, "rows": len(rows), "qtype": qtype,
            "yesno_share": stats["yes_share"], "edge_tags": sorted(stats["edges"]), "notes": notes}
