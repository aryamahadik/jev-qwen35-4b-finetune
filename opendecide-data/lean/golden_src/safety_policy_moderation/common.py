"""Shared helpers for the golden v14 safety_policy_moderation builders (CPU only, deterministic).

Decontamination layers (drop, never edit):
  1. forbidden_hits(): exact normalised text or any shared 10-word run against texts we must never train on or
     that are dev/eval/held-out sources: the whole tasksource/zero-shot-label-nli (152 forbidden tasks incl. mbib-base,
     dynahate, ethos, hate_speech18, hate_speech_offensive, implicit-hate, tweet_eval/*), Social Bias Frames (all
     splits; BTZSC biasframes dev), BTZSC biasframes_* dev files, HateXplain (all splits; inside mbib-base),
     tweet_eval hate/offensive/irony/sentiment (all splits; dev/eval), GoEmotions (OHS-1, raw + simplified),
     HateCheck (OHS-1), DynaHate v0.2.3 (forbidden), and optionally Measuring Hate Speech (so the other sets never
     share a text with the MHS rows). All read from pinned local snapshots, only to drop overlaps.
  2. our_file_hits(): exact normalised text or any shared 13-word run against every non-held-out *.jsonl under lean/
     and opendecide-data/data/ (train, dev and eval files) plus JevBench public. Paths whose parts start with ohs,
     preds or results are never opened. data/v14_parts/ is skipped (other golden builders write there concurrently);
     overlap inside this family is handled by family_hits().
  3. family_hits(): exact normalised text or shared 12-word run against raw outputs of family keys built earlier
     (FAMILY_ORDER), so no text appears in two datasets of this family.
"""
import hashlib
import json
import os
import pickle
import re
import unicodedata
import urllib.request
from collections import defaultdict
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent            # lean/golden_src/safety_policy_moderation
GOLDEN = HERE.parent
LEAN = GOLDEN.parent
ROOT = LEAN.parent                                # opendecide-data
JEV = ROOT.parent
CACHE = HERE / "cache"
RAW_DIR = LEAN / "data" / "v14_parts" / "raw"
DEFS_DIR = LEAN / "data" / "v14_parts" / "defs"
MANIFEST = GOLDEN / "MANIFEST.jsonl"
FAMILY = "safety_policy_moderation"
SEED = 20261129

# build order inside this family: a builder drops texts already used by keys listed before it
FAMILY_ORDER = ["mhs_hate", "aegis_prompts", "edos_sexism", "ghc_hate", "hatemoji_build_v14", "slur_usage",
                "misogyny_reddit", "east_asian_prejudice"]

HF = Path.home() / ".cache" / "huggingface" / "hub"
BREADTH_CACHE = LEAN / "breadth_src" / "cache"

# (label, path or glob dir, reader) - pinned snapshots; every one must exist
FORBIDDEN_SOURCES = [
    ("tasksource/zero-shot-label-nli@ee693dba", HF / "datasets--tasksource--zero-shot-label-nli/snapshots/"
     "ee693dba923b5d5484aa9232b7357c5e45dd39b8/data", ("parquet", "premise")),
    ("allenai/social_bias_frames@453e07c6", HF / "datasets--allenai--social_bias_frames/snapshots/"
     "453e07c6887c7420e7c62e3bbc1c03ceb4ab0f68/default", ("parquet_rec", "post")),
    ("Hate-speech-CNERG/hatexplain@b0e5676a", HF / "datasets--Hate-speech-CNERG--hatexplain/snapshots/"
     "b0e5676acc1d0dcb31d6ce8e93e7e94109044ed6/plain_text", ("parquet_rec", "post_tokens")),
    ("btzsc/btzsc@fef2a2ac biasframes_*", HF / "datasets--btzsc--btzsc/snapshots/"
     "fef2a2ac62b69c58670047dddf045c53d7c3cb5e", ("parquet_glob", "biasframes_*/*.parquet", "text")),
    ("cardiffnlp/tweet_eval@b3a375ba hate/offensive/irony/sentiment", HF / "datasets--cardiffnlp--tweet_eval/snapshots/"
     "b3a375baf0f409c77e6bc7aa35102b7b3534f8be", ("parquet_glob", "*/*.parquet", "text")),
    ("google-research-datasets/go_emotions@add49224", HF / "datasets--google-research-datasets--go_emotions/snapshots/"
     "add492243ff905527e67aeb8b80c082af02207c3", ("parquet_glob", "*/*.parquet", "text")),
    ("Paul/hatecheck@9d2ac89d test.csv", HF / "datasets--Paul--hatecheck/snapshots/"
     "9d2ac89df04254e5c427bcc8d61b6d6c83a1f59b/test.csv", ("csv", "test_case")),
    ("DynaHate v0.2.3 (bvidgen@36f9dc84)", BREADTH_CACHE / "hatemoji_build/decontam/dynahate_v0.2.3.csv",
     ("csv", "text")),
]
MHS_SOURCE = ("ucberkeley-dlab/measuring-hate-speech@5468f6e1", HF / "datasets--ucberkeley-dlab--measuring-hate-speech/"
              "snapshots/5468f6e118396646b02a2f691e771f6b6d9502ea/data", ("parquet", "text"))

FORBIDDEN_RUN = 10
OUR_RUN = 13
FAMILY_RUN = 12

_W = re.compile(r"[\W_]+")


def words(t):
    return _W.sub(" ", unicodedata.normalize("NFKC", t).casefold()).split()


def norm(t):
    return " ".join(words(t))


def enorm(t):
    """Emoji-preserving normalisation (NFKC, casefold, collapsed whitespace)."""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", t).casefold()).strip()


def grams(w, n):
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def fetch(url, path, sha=None):
    """Download url to path once; verify sha256 when given; return the sha256."""
    path = Path(path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        import requests  # certifi-backed TLS (the framework Python's urllib lacks a CA bundle here)
        with requests.get(url, headers={"User-Agent": "Mozilla/5.0 (golden-v14 builder)"}, stream=True,
                          timeout=300) as r, open(str(path) + ".part", "wb") as f:
            r.raise_for_status()
            for b in r.iter_content(1 << 20):
                f.write(b)
        os.replace(str(path) + ".part", path)
    got = sha256(path)
    if sha is not None and got != sha:
        raise SystemExit(f"sha256 mismatch for {path}: {got} != {sha}")
    return got


def _read_source(path, how):
    kind = how[0]
    if kind == "parquet":
        for f in sorted(Path(path).glob("*.parquet")):
            yield from pd.read_parquet(f, columns=[how[1]])[how[1]].astype(str)
    elif kind == "parquet_rec":
        for f in sorted(Path(path).rglob("*.parquet")):
            col = pd.read_parquet(f, columns=[how[1]])[how[1]]
            for v in col:
                yield " ".join(v) if not isinstance(v, str) else v
    elif kind == "parquet_glob":
        fs = sorted(Path(path).glob(how[1]))
        assert fs, f"no files for {path}/{how[1]}"
        for f in fs:
            yield from pd.read_parquet(f, columns=[how[2]])[how[2]].astype(str)
    elif kind == "csv":
        yield from pd.read_csv(path, usecols=[how[1]], dtype=str, keep_default_na=False)[how[1]]
    else:
        raise ValueError(kind)


def _index(texts, run):
    exact, owner = defaultdict(set), defaultdict(set)
    for rid, t in texts.items():
        w = words(t)
        exact[" ".join(w)].add(rid)
        for g in grams(w, run):
            owner[g].add(rid)
    return exact, owner


def _match(t, exact, owner, run):
    w = words(t)
    hit = set(exact.get(" ".join(w), ()))
    if owner:
        for i in range(len(w) - run + 1):
            s = owner.get(" ".join(w[i:i + run]))
            if s:
                hit |= s
    return hit


def forbidden_hits(texts, include_mhs=True, run=FORBIDDEN_RUN):
    """texts: {rid: text}. Returns ({rid: source label}, [source labels read])."""
    exact, owner = _index(texts, run)
    srcs = list(FORBIDDEN_SOURCES) + ([MHS_SOURCE] if include_mhs else [])
    hit = {}
    for label, path, how in srcs:
        assert Path(path).exists(), f"missing pinned decontam snapshot {path}"
        seen = set()
        for t in _read_source(path, how):
            if t in seen:
                continue
            seen.add(t)
            for rid in _match(t, exact, owner, run):
                hit.setdefault(rid, label)
    return hit, [s[0] for s in srcs]


def _is_heldout(rel):
    return any(x.lower().startswith(("ohs", "preds", "results")) for x in Path(rel).parts)


def scan_files():
    fs = set()
    for base in (LEAN, ROOT / "data"):
        if not base.exists():
            continue
        for p in base.rglob("*.jsonl"):
            rel = p.relative_to(base)
            parts = rel.parts
            if _is_heldout(rel) or "cache" in parts or ".venv" in parts or "golden_src" in parts:
                continue
            if len(parts) >= 2 and parts[0] == "data" and parts[1] == "v14_parts":
                continue
            if base == LEAN and len(parts) >= 1 and parts[0] == "v14_parts":
                continue
            fs.add(p)
    fs |= set((JEV / "bench/jevbench/datasets/public").glob("*.jsonl"))
    return sorted(fs)


def _strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from _strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from _strings(v)


def our_file_hits(texts, run=OUR_RUN, tag="default"):
    """13-word runs / exact normalised text vs every non-held-out jsonl. Cached per (text, file-signature)."""
    files = scan_files()
    sig = hashlib.sha1("\n".join(f"{f}|{f.stat().st_size}|{int(f.stat().st_mtime)}" for f in files).encode()).hexdigest()
    cpath = CACHE / "_ourfile_scan" / f"{tag}.pkl"
    cache = {}
    if cpath.exists():
        try:
            c = pickle.loads(cpath.read_bytes())
            if c.get("sig") == sig and c.get("run") == run:
                cache = c["res"]
        except Exception:  # noqa: BLE001
            cache = {}
    key = {rid: hashlib.sha1(norm(t).encode()).hexdigest() for rid, t in texts.items()}
    todo = {rid: t for rid, t in texts.items() if key[rid] not in cache}
    if todo:
        exact, owner = _index(todo, run)
        found = {}
        seen = set()
        for f in files:
            with open(f, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    try:
                        x = json.loads(line)
                    except Exception:  # noqa: BLE001
                        continue
                    for s in _strings(x):
                        if len(s) < 12:
                            continue
                        h = hash(s)
                        if h in seen:
                            continue
                        seen.add(h)
                        for rid in _match(s, exact, owner, run):
                            found.setdefault(rid, str(f.relative_to(JEV)))
        for rid in todo:
            cache[key[rid]] = found.get(rid, "")
        cpath.parent.mkdir(parents=True, exist_ok=True)
        cpath.write_bytes(pickle.dumps({"sig": sig, "run": run, "res": cache}))
    hits = {rid: cache[key[rid]] for rid in texts if cache[key[rid]]}
    return hits, len(files)


def family_hits(texts, self_key, run=FAMILY_RUN):
    """Overlap with raw outputs of family keys built before self_key."""
    before = FAMILY_ORDER[:FAMILY_ORDER.index(self_key)]
    exact, owner = _index(texts, run)
    hit = {}
    for k in before:
        p = RAW_DIR / f"{k}.jsonl"
        if not p.exists():
            continue
        for line in open(p, encoding="utf-8"):
            r = json.loads(line)
            for rid in _match(r["state"], exact, owner, run):
                hit.setdefault(rid, k)
    return hit


def within_dedup(items, text_fn, run=FAMILY_RUN):
    """Keep the first item of each exact-normalised text / shared 12-word run (items already in priority order)."""
    kept, seen_exact, seen_runs = [], set(), set()
    for it in items:
        w = words(text_fn(it))
        n = " ".join(w)
        g = grams(w, run)
        if n in seen_exact or (g & seen_runs):
            continue
        seen_exact.add(n)
        seen_runs |= g
        kept.append(it)
    return kept


def write_outputs(key, rows, defs, norm_fn=None):
    """defs: {option: definition} or {qid: {option: definition}} when meta.defs names the qid.
    norm_fn: text normaliser for the duplicate-state check (default: word-level norm; emoji-bearing sets pass one
    that keeps emoji, since an emoji swap changes the meaning)."""
    norm_fn = norm_fn or norm
    assert key in FAMILY_ORDER, f"{key} is not a {FAMILY} key"
    raw = RAW_DIR / f"{key}.jsonl"
    if raw.exists():  # never overwrite (or delete defs of) a same-named key written by another family's builder
        with open(raw, encoding="utf-8") as fh:
            first = fh.readline()
        if first.strip():
            fam = json.loads(first).get("meta", {}).get("family")
            assert fam == FAMILY, f"{raw} belongs to family {fam!r}; refusing to overwrite"
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    DEFS_DIR.mkdir(parents=True, exist_ok=True)
    states = [r["state"] for r in rows]
    assert all(s.strip() for s in states), "empty state"
    assert len({(norm_fn(r["state"]), r["instructions"]) for r in rows}) == len(rows), "duplicate state"
    assert len({norm_fn(s) for s in states}) == len(states), "same text used twice"
    for r in rows:
        assert r["gold"] in r["options"], r
        if r["soft"] is not None:
            assert set(r["soft"]) <= set(r["options"]) and abs(sum(r["soft"].values()) - 1) < 1e-6, r["soft"]
        assert r["meta"]["split"] == "train" and r["meta"]["family"] == FAMILY
    with open(RAW_DIR / f"{key}.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    for old in list(DEFS_DIR.glob(f"{key}__*.json")) + [DEFS_DIR / f"{key}.json"]:  # stale defs of this key
        if old.exists():
            old.unlink()
    qids = {r["meta"].get("defs") for r in rows}
    if qids == {None}:
        (DEFS_DIR / f"{key}.json").write_text(json.dumps(defs, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        for q in qids:
            assert q is not None, "mixed defs/no-defs rows"
            used = {o for r in rows if r["meta"].get("defs") == q for o in r["options"]}
            assert used <= set(defs[q]), (q, used - set(defs[q]))
            (DEFS_DIR / f"{key}__{q}.json").write_text(json.dumps(defs[q], indent=1, ensure_ascii=False) + "\n",
                                                        encoding="utf-8")


def soft_from_counts(counts, options):
    tot = sum(counts.get(o, 0) for o in options)
    if tot <= 0:
        return None
    s = {o: round(counts.get(o, 0) / tot, 6) for o in options}
    # push rounding residue onto the largest share so the shares sum to exactly 1
    top = max(s, key=lambda o: s[o])
    s[top] = round(s[top] + 1 - sum(s.values()), 6)
    return s


def summary(key, rows):
    from collections import Counter
    import statistics
    print(f"[{key}] rows={len(rows)}")
    by_q = Counter(r["instructions"] for r in rows)
    for q, n in by_q.most_common():
        g = Counter(r["gold"] for r in rows if r["instructions"] == q)
        print(f"  {n:5d}  {q[:90]}")
        print(f"         gold: {dict(g.most_common(12))}")
    yn = [r for r in rows if r["options"] == ["yes", "no"]]
    if yn:
        print(f"  yes/no rows {len(yn)}; yes share {sum(r['gold'] == 'yes' for r in yn) / len(yn):.3f}")
    print(f"  edge tags: {dict(Counter(r['meta']['edge'] for r in rows))}")
    print(f"  soft coverage {sum(r['soft'] is not None for r in rows)}/{len(rows)}; "
          f"soft p(gold)<0.5: {sum(1 for r in rows if r['soft'] and r['soft'][r['gold']] < 0.5)}")
    L = [len(r["state"]) for r in rows]
    print(f"  state chars min {min(L)} median {statistics.median(L)} max {max(L)}")


def manifest_append(rec):
    """Append-only (other builders append to the same file concurrently); skip when the key is already recorded."""
    if MANIFEST.exists():
        for line in MANIFEST.read_text(encoding="utf-8").splitlines():
            try:
                if json.loads(line).get("key") == rec["key"]:
                    print(f"MANIFEST already has {rec['key']}; not appending")
                    return False
            except Exception:  # noqa: BLE001
                pass
    with open(MANIFEST, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return True
