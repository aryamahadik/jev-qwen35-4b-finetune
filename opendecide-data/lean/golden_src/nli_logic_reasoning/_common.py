"""Shared helpers for the golden v14 nli_logic_reasoning builders (CPU only, deterministic, no model calls).

Every builder in this folder writes
  data/v14_parts/raw/<key>.jsonl            (one row per line, GOLDEN_SPEC.md format)
  data/v14_parts/defs/<key>.json            (single option set)  or  defs/<key>__<qid>.json (several sets)
and appends one record to golden_src/MANIFEST.jsonl.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

FAMILY = "nli_logic_reasoning"
HERE = Path(__file__).resolve().parent
GOLDEN = HERE.parent
LEAN = GOLDEN.parent
CACHE_ROOT = HERE / "cache"
RAW_DIR = LEAN / "data" / "v14_parts" / "raw"
DEFS_DIR = LEAN / "data" / "v14_parts" / "defs"
MANIFEST = GOLDEN / "MANIFEST.jsonl"

EDGE_TAGS = {"negation", "double_negation", "exception", "missing_info", "conflicting_evidence", "temporal",
             "numeric", "units", "quantifier", "hypothetical", "reported_speech", "sarcasm", "implicit",
             "long_context", "table", "multi_hop", "ambiguous", None}

WORD = re.compile(r"[a-z0-9]+")


def words(s):
    return WORD.findall(s.lower())


def ngrams(ws, n):
    return {" ".join(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def norm(s):
    """Normalisation used for exact / near-exact duplicate detection of states."""
    return " ".join(words(s))


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url, dest):
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        tmp = dest.with_suffix(dest.suffix + ".part")
        subprocess.run(["curl", "-sfL", "--retry", "3", "-o", str(tmp), url], check=True)
        tmp.rename(dest)
    return dest


def clean(s):
    return re.sub(r"\s+", " ", str(s)).strip()


def check_defs(defs, max_words=45):
    for k, v in defs.items():
        n = len(v.split())
        assert 6 <= n <= max_words, (k, n, v)


def write_defs(key, defs, qid=None):
    check_defs(defs)
    DEFS_DIR.mkdir(parents=True, exist_ok=True)
    p = DEFS_DIR / (f"{key}__{qid}.json" if qid else f"{key}.json")
    p.write_text(json.dumps(defs, indent=1, ensure_ascii=False) + "\n")
    return p


def validate_rows(key, rows, defs_by_qid):
    """Hard checks before writing: format, options/gold, no empty or duplicate states, defs cover options."""
    seen_rid, seen_state = set(), set()
    for r in rows:
        assert r["key"] == key
        assert r["rid"] and r["rid"] not in seen_rid, r["rid"]
        seen_rid.add(r["rid"])
        assert r["state"].strip(), r["rid"]
        ns = norm(r["state"] + " || " + r["instructions"])
        assert ns not in seen_state, ("duplicate state+question", r["rid"])
        seen_state.add(ns)
        assert r["instructions"].strip()
        assert r["gold"] in r["options"], r["rid"]
        assert len(set(r["options"])) == len(r["options"])
        if set(r["options"]) == {"yes", "no"}:
            assert r["options"] == ["yes", "no"]
        if r["soft"] is not None:
            assert abs(sum(r["soft"].values()) - 1) < 1e-6
        m = r["meta"]
        for f in ("dataset", "config", "revision", "licence", "split", "orig_label", "family", "edge"):
            assert f in m, (f, r["rid"])
        assert m["split"] == "train" and m["family"] == FAMILY
        assert m["edge"] in EDGE_TAGS, m["edge"]
        qid = m.get("defs")
        d = defs_by_qid[qid]
        assert set(r["options"]) <= set(d), (qid, r["options"], list(d))


def write_rows(key, rows):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    p = RAW_DIR / f"{key}.jsonl"
    with open(p, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return p


def report(key, rows):
    n = len(rows)
    print(f"[{key}] rows: {n}")
    byq = Counter(r["meta"].get("defs") or "-" for r in rows)
    print(f"[{key}] option sets: {dict(byq)}")
    for q in byq:
        sub = [r for r in rows if (r["meta"].get("defs") or "-") == q]
        c = Counter(r["gold"] for r in sub)
        mx = max(c.values()) / len(sub)
        print(f"[{key}]   {q}: {dict(c)}  max share {mx:.1%}")
    e = Counter(r["meta"]["edge"] for r in rows)
    print(f"[{key}] edge tags: {dict(e)}")
    L = sorted(len(r["state"]) for r in rows)
    print(f"[{key}] state chars: min {L[0]} median {L[n // 2]} p95 {L[int(n * .95)]} max {L[-1]}")
    yn = [r for r in rows if r["options"] == ["yes", "no"]]
    share = (sum(r["gold"] == "yes" for r in yn) / len(yn)) if yn else None
    if yn:
        print(f"[{key}] yes/no rows {len(yn)}, yes share {share:.1%}")
    return share


def append_manifest(rec):
    """Upsert our record for rec['key'] in the shared MANIFEST (other families write to it concurrently).
    Everything happens under an exclusive flock on the file itself (the lock the other families' helpers take):
    a new key is one appended line; a re-run of our own builder rewrites the file IN PLACE (no rename, so other
    writers keep the same inode) with only our stale line removed."""
    import fcntl
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.touch(exist_ok=True)
    line = json.dumps(rec, ensure_ascii=False)
    with open(MANIFEST, "r+", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            lines = f.read().splitlines()
            keep, stale = [], False
            for ln in lines:
                try:
                    if ln.strip() and json.loads(ln).get("key") == rec["key"]:
                        stale = True
                        continue
                except Exception:
                    pass
                keep.append(ln)
            if stale:
                f.seek(0)
                f.truncate()
                f.write("\n".join([ln for ln in keep if ln.strip()] + [line]) + "\n")
            else:
                f.seek(0)
                text = f.read()
                f.seek(0, os.SEEK_END)
                if text and not text.endswith("\n"):
                    f.write("\n")
                f.write(line + "\n")
            f.flush()
            os.fsync(f.fileno())
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def iter_strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from iter_strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from iter_strings(v)


def local_eval_files():
    """Our own dev / eval / selection files (never the OHS held-out files, which we do not open)."""
    return sorted(p for p in (LEAN / "data").glob("*.jsonl")
                  if not p.name.startswith("ohs") and re.search(r"dev|eval", p.name))


def local_hits(patterns, files=None):
    """Return the subset of normalised word patterns that occur (space-bounded) in local dev/eval files."""
    files = files if files is not None else local_eval_files()
    if not patterns:
        return set()
    tmpdir = Path(tempfile.mkdtemp(prefix="nlr_decon_"))
    normf, patf = tmpdir / "norm.txt", tmpdir / "pat.txt"
    try:
        with open(normf, "w") as out:
            for f in files:
                with open(f, errors="replace") as fh:
                    for line in fh:
                        try:
                            o = json.loads(line)
                        except Exception:
                            o = line
                        for s in iter_strings(o):
                            ws = words(s)
                            if len(ws) >= 6:
                                out.write(" " + " ".join(ws) + " \n")
        patf.write_text("".join(f" {p} \n" for p in sorted(patterns)))
        tool = shutil.which("rg") or "grep"
        cmd = ([tool, "-F", "-o", "-N", "--no-filename", "-f", str(patf), str(normf)] if tool.endswith("rg")
               else [tool, "-F", "-o", "-h", "-f", str(patf), str(normf)])
        res = subprocess.run(cmd, capture_output=True, text=True)
        assert res.returncode in (0, 1), res.stderr
        hits = {h.strip() for h in res.stdout.splitlines() if h.strip()}
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    print(f"local dev/eval decontam: {len(files)} files, {len(patterns)} patterns, {len(hits)} hits")
    return hits


def balanced_pick(pools, quota, rng, key_fn=None, cap_fn=None):
    """Round-robin over label pools (each pre-shuffled) until each label reaches its quota.
    key_fn(row) -> group id for a per-group cap enforced by cap_fn(group_counts, row) -> bool (True = allowed)."""
    out, ptr = [], {k: 0 for k in pools}
    got = Counter()
    groups = Counter()
    active = [k for k in pools if quota.get(k, 0) > 0]
    while active:
        for lab in list(active):
            pool = pools[lab]
            placed = False
            while ptr[lab] < len(pool):
                r = pool[ptr[lab]]
                ptr[lab] += 1
                g = key_fn(r) if key_fn else None
                if cap_fn and not cap_fn(groups, r, g):
                    continue
                out.append(r)
                got[lab] += 1
                if g is not None:
                    groups[g] += 1
                placed = True
                break
            if not placed or got[lab] >= quota[lab]:
                active.remove(lab)
    return out


def show_samples(rows, k=5, seed=7):
    import random
    rng = random.Random(seed)
    for r in rng.sample(rows, min(k, len(rows))):
        print("=" * 100)
        print("RID:", r["rid"], "| EDGE:", r["meta"]["edge"], "| DEFS:", r["meta"].get("defs"))
        st = r["state"]
        print("STATE:\n" + (st if len(st) < 2500 else st[:1200] + "\n[...]\n" + st[-1000:]))
        print("Q:", r["instructions"])
        print("OPTIONS:", r["options"], "GOLD:", r["gold"], "ORIG:", r["meta"]["orig_label"])
