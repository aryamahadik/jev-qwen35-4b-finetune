"""Shared helpers for the science_health_claims golden builders (v14). CPU-only, deterministic, no model calls.

- fetch(): pinned URL download into golden_src/science_health_claims/cache/<key>/ with a sha256 check.
- decon(): drops candidate records whose core texts share an exact normalised text (>= 6 words) or a 10-word run
  with (a) every premise of tasksource/zero-shot-label-nli (forbidden: all 152 tasks, all splits, e.g. health_fact,
  scientific-exaggeration-detection, scicite, tweet_eval/stance_climate; read only to drop overlaps), (b) every local
  *.jsonl under lean/ and ../data except held-out files (ohs*, preds*, results*), caches and data/v14_parts (other
  golden parts are cross-deduped at compile time), and (c) the JevBench public splits. Held-out (OHS) files are never
  opened here. Results are cached per text hash in cache/_decon/ so the 1.6 GB scan runs once per new text.
- near_dup_filter(): greedy exact + word-set-Jaccard near-duplicate removal.
- edge(): one edge-case tag per row from surface cues, in a fixed priority order.
- write_outputs() / append_manifest(): raw rows, defs and the MANIFEST record (file-locked, replaces an older record
  of the same key so reruns do not duplicate it).
"""
import collections
import fcntl
import hashlib
import json
import random
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent            # golden_src/science_health_claims
GOLDEN = HERE.parent                               # golden_src
LEAN = GOLDEN.parent                               # lean
ROOT = LEAN.parent                                 # opendecide-data
JEV = ROOT.parent                                  # jev
CACHE = HERE / "cache"
RAW_DIR = LEAN / "data" / "v14_parts" / "raw"
DEFS_DIR = LEAN / "data" / "v14_parts" / "defs"
MANIFEST = GOLDEN / "MANIFEST.jsonl"
FAMILY = "science_health_claims"
YN = ["yes", "no"]
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
    path = Path(path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        import requests  # certifi CA bundle (the framework python's urllib has no system CA store here)
        tmp = path.with_suffix(path.suffix + ".part")
        with requests.get(url, headers={"User-Agent": "opendecide-golden-builder"}, stream=True, timeout=600) as r:
            r.raise_for_status()
            with open(tmp, "wb") as f:
                for b in r.iter_content(1 << 20):
                    f.write(b)
        tmp.rename(path)
    got = sha256(path)
    if got != sha:
        sys.exit(f"sha256 mismatch for {path}: {got} != {sha}")
    return path


# ----------------------------------------------------------------------------------------------- text utils
def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", str(t).lower()).strip()


def words(t):
    return re.findall(r"[a-z0-9]+", str(t).lower())


def clean(t):
    """Whitespace tidy only (no rewording): non-breaking spaces to spaces, runs of spaces/tabs collapsed."""
    t = str(t).replace(" ", " ").replace("​", "")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


NEG_STRICT = re.compile(r"\b(not|no|never|none|nobody|nothing|neither|nor|without|cannot)\b|n't\b", re.I)
QUANT = re.compile(r"\b(all|every|each|only|most|majority|minority|none of|at least|at most|exactly|more than|less than|"
                   r"fewer than|always|any)\b", re.I)
NUM = re.compile(r"(?<![\w-])\d+(?:[.,]\d+)*(?:%|(?![\w-]))")
ALNUM_ID = re.compile(r"\b[A-Za-z]+[A-Za-z-]*-?\d+[A-Za-z0-9-]*\b")  # COVID-19, SARS-CoV-2, H1N1, CO2
UNITS = re.compile(r"\b\d[\d,.]*\s?(%|percent|km|kg|g|mg|mcg|µg|ml|mL|l|lb|lbs|pounds?|miles?|feet|meters?|metres?|cm|mm|"
                   r"nm|liters?|litres?|ppm|ppb|gt|mt|degrees?|°c|°f|°|mph|hours?|minutes?|days?|weeks?|months?|"
                   r"years?|mmhg|iu|units?)\b", re.I)
TEMP = re.compile(r"\b(before|after|until|since|by (19|20)\d\d|in (19|20)\d\d|(19|20)\d\d|decades?|century|years? ago|"
                  r"pre-industrial|preindustrial|baseline|projected|trend)\b", re.I)
HYPO = re.compile(r"\b(if|would|could|might|may|unless|suppose|assuming|possibly|likely|suggests?)\b", re.I)
REPORTED = re.compile(r"\b(said|says|according to|claims?|claimed|told|reported|announced|argues?|argued|believes?)\b",
                      re.I)


def neg_count(t):
    return len(NEG_STRICT.findall(t))


def edge(text, order=("double_negation", "negation", "units", "numeric", "quantifier", "temporal"), default=None):
    """First matching tag in `order` (surface cues on the text the decision depends on). Alphanumeric identifiers
    such as COVID-19, SARS-CoV-2, H1N1 or CO2 are not counted as numbers."""
    text = ALNUM_ID.sub(" ", text)
    for tag in order:
        if tag == "double_negation" and neg_count(text) >= 2:
            return tag
        if tag == "negation" and neg_count(text) >= 1:
            return tag
        if tag == "units" and UNITS.search(text):
            return tag
        if tag == "numeric" and NUM.search(text):
            return tag
        if tag == "quantifier" and QUANT.search(text):
            return tag
        if tag == "temporal" and TEMP.search(text):
            return tag
        if tag == "hypothetical" and HYPO.search(text):
            return tag
        if tag == "reported_speech" and REPORTED.search(text):
            return tag
    return default


# ----------------------------------------------------------------------------------------------- decontamination
def _is_skipped(rel_parts):
    parts = [x.lower() for x in rel_parts]
    if any(x.startswith(("ohs", "preds", "results")) for x in parts):
        return True
    if "cache" in parts or ".venv" in parts or "v14_parts" in parts or "node_modules" in parts:
        return True
    return False


def _strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from _strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from _strings(v)


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
    """The pinned snapshot from the local HF cache, or re-downloaded (same revision, sha256-checked) if cleared."""
    out = []
    for name, sha in LABEL_NLI_FILES.items():
        p = LABEL_NLI_DIR / name
        if not p.exists():
            p = fetch(LABEL_NLI_URL.format(rev=LABEL_NLI_REV, name=name), CACHE / "_label_nli" / name, sha)
        out.append(p)
    return out


def _thash(t):
    return hashlib.sha1(" ".join(words(t)).encode()).hexdigest()


def decon(core, verbose=True, cache_name=None):
    """core: {rid: [text, ...]} -> {rid: reason} for records that overlap a forbidden / used / eval text.

    Texts are checked once; per-text verdicts are cached (by sha1 of the normalised text) in cache/_decon/<cache_name>.json
    together with the list of scanned files and their sizes, and the cache is ignored if that list changes."""
    files = scan_files()
    sig = hashlib.sha1(json.dumps([[str(p), p.stat().st_size] for p in files] + [LABEL_NLI_REV]).encode()).hexdigest()
    cpath = CACHE / "_decon" / f"{cache_name}.json" if cache_name else None
    cached = {}
    if cpath and cpath.exists():
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

        def check(text, reason):
            w = words(text)
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
                check(t, "label_nli")
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
                        check(line, reason)
                        continue
                    for s in _strings(obj):
                        if len(s) >= 20:
                            check(s, reason)
        for h in todo:
            cached[h] = found.get(h)
        if cpath:
            cpath.parent.mkdir(parents=True, exist_ok=True)
            cpath.write_text(json.dumps({"sig": sig, "verdicts": cached}))
    hits = {}
    for rid, texts in core.items():
        for t in texts:
            v = cached.get(_thash(t))
            if v:
                hits.setdefault(rid, v)
                break
    if verbose:
        print(f"decon: {len(core)} records ({len(todo)} new texts scanned over {len(files)} files + label-NLI), "
              f"hits={len(hits)} {dict(collections.Counter(v.split(':')[0] for v in hits.values()))}")
    return hits


def cross_v14(core, own_keys, verbose=True, stock_min=3):
    """Overlap check against the OTHER golden v14 raw parts already written (data/v14_parts/raw/*.jsonl, states):
    {rid: [text, ...]} -> {rid: 'v14:<key>'} for records sharing an exact normalised text (>= 6 words) or a 10-word
    run. 10-word runs that occur in >= stock_min of our own DISTINCT texts are stock phrasing ('which of the following is
    the most appropriate next step in management') and are ignored. Keeps this family's rows text-disjoint from other
    families (compile also cross-dedupes)."""
    exact = collections.defaultdict(set)
    owner = collections.defaultdict(set)
    text_freq = collections.Counter()   # in how many DISTINCT own texts a run occurs (a passage reused by several
    seen_texts = set()                  # records counts once, so a reused passage is never mistaken for stock text)
    for rid, texts in core.items():
        for t in texts:
            w = words(t)
            if len(w) >= MIN_EXACT:
                exact[" ".join(w)].add(rid)
            runs = {hash(tuple(w[i:i + RUN])) for i in range(len(w) - RUN + 1)}
            for h in runs:
                owner[h].add(rid)
            key = " ".join(w)
            if key not in seen_texts:
                seen_texts.add(key)
                text_freq.update(runs)
    owner = {h: rids for h, rids in owner.items() if text_freq[h] < stock_min}
    hits = {}
    for p in sorted(RAW_DIR.glob("*.jsonl")):
        k = p.stem
        if k in own_keys:
            continue
        try:
            f = open(p)
        except FileNotFoundError:  # another family's part removed between glob and open
            continue
        with f:
            for line in f:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                for s in (obj.get("state", ""),):
                    w = words(s)
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


# ----------------------------------------------------------------------------------------------- near-dup
def near_dup_filter(items, text_of, thresh=0.85, block_of=None):
    """Greedy near-duplicate removal (word-set Jaccard >= thresh within a block). Keeps order; returns kept list.

    Default block: the 3 rarest-looking (longest) words are not stable, so we block on each of the first 2 sorted
    words of length >= 5; an item is compared with every earlier item sharing any block key."""
    kept, seen_exact = [], set()
    index = collections.defaultdict(list)
    for it in items:
        t = text_of(it)
        n = norm(t)
        if not n or n in seen_exact:
            continue
        ws = set(n.split())
        keys = block_of(it) if block_of else sorted(w for w in ws if len(w) >= 5)[:2] or ["_"]
        dup = False
        for k in keys:
            for o in index[k]:
                if len(ws & o) / max(1, len(ws | o)) >= thresh:
                    dup = True
                    break
            if dup:
                break
        if dup:
            continue
        seen_exact.add(n)
        for k in keys:
            index[k].append(ws)
        kept.append(it)
    return kept


# ----------------------------------------------------------------------------------------------- output
def check_rows(key, rows, defs_by_qid):
    assert rows, "no rows"
    rids = [r["rid"] for r in rows]
    assert len(set(rids)) == len(rids), "duplicate rid"
    states = [norm(r["state"]) for r in rows]
    assert all(states), "empty state"
    assert len(set(states)) == len(states), "duplicate state"
    for r in rows:
        assert r["key"] == key
        assert r["instructions"].strip() and r["gold"] in r["options"], r
        assert r["meta"]["split"] == "train"
        assert r["meta"]["family"] == FAMILY
        e = r["meta"].get("edge")
        assert e is None or e in EDGE_TAGS, e
        qid = r["meta"].get("defs")
        d = defs_by_qid[qid] if qid else defs_by_qid[None]
        assert all(o in d for o in r["options"]), (qid, r["options"])
        if r["soft"] is not None:
            assert abs(sum(r["soft"].values()) - 1) < 1e-6
            assert set(r["soft"]) <= set(r["options"])
    yn = [r for r in rows if r["options"] == YN]
    if yn:
        share = sum(r["gold"] == "yes" for r in yn) / len(yn)
        assert 0.35 <= share <= 0.65, f"yes share {share:.3f}"
    ch = [r for r in rows if r["options"] != YN]
    if ch:
        top = max(collections.Counter(r["gold"] for r in ch).values()) / len(ch)
        assert top <= 0.5 + 1e-9, f"choice class share {top:.3f}"
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
    edges = collections.Counter(r["meta"].get("edge") for r in rows)
    qids = collections.Counter(r["meta"].get("defs") or "default" for r in rows)
    ys = (sum(r["gold"] == "yes" for r in yn) / len(yn)) if yn else None
    gold_ch = collections.Counter(r["gold"] for r in ch)
    lens = sorted(len(r["state"]) for r in rows)
    print(f"[{key}] rows={len(rows)} yesno={len(yn)} choice={len(ch)} yes_share={ys}")
    by_q = collections.defaultdict(collections.Counter)
    for r in rows:
        by_q[r["meta"].get("defs") or "default"][r["gold"]] += 1
    for q, c in sorted(by_q.items()):
        print(f"  q={q}: {dict(c)}")
    print(f"  choice gold dist: {dict(sorted(gold_ch.items()))}")
    print(f"  edge tags: {dict(edges.most_common())}")
    print(f"  state chars: min={lens[0]} median={lens[len(lens) // 2]} max={lens[-1]}")
    print(f"  soft coverage: {sum(r['soft'] is not None for r in rows)}/{len(rows)}")
    return {"yes_share": round(ys, 4) if ys is not None else None, "edges": edges, "n_yn": len(yn), "n_ch": len(ch)}


def show_samples(rows, n=5, seed=7):
    rng = random.Random(seed)
    for r in rng.sample(rows, min(n, len(rows))):
        print("-" * 100)
        print("RID:", r["rid"], "| edge:", r["meta"].get("edge"), "| defs:", r["meta"].get("defs"),
              "| orig:", json.dumps(r["meta"].get("orig_label"), ensure_ascii=False)[:200])
        print("STATE:\n" + r["state"][:2500])
        print("Q:", r["instructions"])
        print("OPTIONS:", r["options"], "| GOLD:", r["gold"], "| SOFT:", r["soft"])


def append_manifest(rec):
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.touch(exist_ok=True)
    with open(MANIFEST, "r+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            lines = [l for l in f.read().splitlines() if l.strip()]
            keep = []
            for l in lines:
                try:
                    if json.loads(l).get("key") == rec["key"]:
                        continue
                except json.JSONDecodeError:
                    pass
                keep.append(l)
            keep.append(json.dumps(rec, ensure_ascii=False))
            f.seek(0)
            f.truncate()
            f.write("\n".join(keep) + "\n")
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def manifest_record(key, dataset, licence, rows, qtype, notes, stats):
    edges = sorted(t for t in stats["edges"] if t)
    return {"key": key, "family": FAMILY, "dataset": dataset, "licence": licence, "rows": len(rows), "qtype": qtype,
            "yesno_share": stats["yes_share"], "edge_tags": edges, "notes": notes}


def balance_yes(rows_yes, rows_no, rng, lo=0.40, hi=0.60):
    """Down-sample the larger side so the yes share lands in [lo, hi] (keeps as many rows as possible)."""
    ny, nn = len(rows_yes), len(rows_no)
    if ny + nn == 0:
        return rows_yes, rows_no
    if ny / (ny + nn) > hi:
        ny = int(hi / (1 - hi) * nn)
    elif ny / (ny + nn) < lo:
        nn = int((1 - lo) / lo * ny)
    ry, rn = list(rows_yes), list(rows_no)
    rng.shuffle(ry)
    rng.shuffle(rn)
    return ry[:ny], rn[:nn]
