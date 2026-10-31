"""Shared helpers for the routing_dialogue golden builders (v14, round 2: multiple-choice routing / next-action rows).

Only paths, pinned downloads, text normalisation, row checks, writers and the report live here; every builder keeps its
own source-specific logic, questions and definitions. CPU only, no model calls.
"""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

FAMILY = "routing_dialogue"
HERE = Path(__file__).resolve().parent
LEAN = HERE.parent.parent
CACHE = HERE / "cache"
RAW = LEAN / "data" / "v14_parts" / "raw"
DEFS = LEAN / "data" / "v14_parts" / "defs"
UA = "OpenDecideGoldenBuilder/0.2 (dataset research; python-urllib)"

EDGE_TAGS = {"negation", "double_negation", "exception", "missing_info", "conflicting_evidence", "temporal", "numeric",
             "units", "quantifier", "hypothetical", "reported_speech", "sarcasm", "implicit", "long_context", "table",
             "multi_hop", "ambiguous", None}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url, path, sha=None):
    """Download url to path once; verify sha256 when given. Returns the sha256."""
    path = Path(path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".part")
        import requests  # certifi CA bundle (the framework python has no system CA store)
        with requests.get(url, headers={"User-Agent": UA}, stream=True, timeout=300) as r, open(tmp, "wb") as f:
            r.raise_for_status()
            for b in r.iter_content(1 << 20):
                f.write(b)
        tmp.rename(path)
    got = sha256_file(path)
    if sha is not None and got != sha:
        sys.exit(f"sha256 mismatch for {path}: {got} != {sha}")
    return got


def norm(t):
    """Normalisation used for exact / near-exact duplicate detection."""
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def stable_hash(s):
    return int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16)


def check_rows(rows, key):
    """Hard checks every builder runs before writing."""
    assert rows, "no rows"
    seen_rid, seen_state = set(), set()
    for r in rows:
        assert r["key"] == key
        assert r["state"].strip() and r["instructions"].strip()
        assert r["gold"] in r["options"], (r["rid"], r["gold"], r["options"])
        assert len(set(r["options"])) == len(r["options"])
        assert 3 <= len(r["options"]) <= 60, (r["rid"], len(r["options"]))
        if r["soft"] is not None:
            assert set(r["soft"]) <= set(r["options"]) and abs(sum(r["soft"].values()) - 1) < 1e-6
        m = r["meta"]
        assert m["split"] == "train" and m["family"] == FAMILY and m["edge"] in EDGE_TAGS, m
        assert r["rid"] not in seen_rid, ("duplicate rid", r["rid"])
        seen_rid.add(r["rid"])
        n = norm(r["state"])
        assert n not in seen_state, ("duplicate state", r["rid"])
        seen_state.add(n)


def decon_drop(rows, key):
    hits_file = HERE / "decon_hits.json"
    if hits_file.exists():
        bad = {rid for k, rid, _ in json.load(open(hits_file)) if k == key}
        if bad:
            before = len(rows)
            rows = [r for r in rows if r["rid"] not in bad]
            print(f"decon: dropped {before - len(rows)} listed rows")
    return rows


def write_rows(rows, key):
    """Drop rows listed in decon_hits.json (13-gram hits found by decon_rd.py), check, then write."""
    rows = decon_drop(rows, key)
    check_rows(rows, key)
    RAW.mkdir(parents=True, exist_ok=True)
    out = RAW / f"{key}.jsonl"
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return out, rows


def write_defs(defs, key, qid=None):
    DEFS.mkdir(parents=True, exist_ok=True)
    out = DEFS / (f"{key}__{qid}.json" if qid else f"{key}.json")
    for k, v in defs.items():
        assert v.strip() and len(v.split()) <= 60, (key, qid, k, len(v.split()))
    with open(out, "w") as f:
        json.dump(defs, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return out


def round_robin(pools, n):
    """Round-robin over label pools (each pool already in a seeded order; items are popped from the end) until n."""
    labels = sorted(pools)
    pools = {k: list(v) for k, v in pools.items()}
    out, i = [], 0
    while len(out) < n and any(pools[k] for k in labels):
        k = labels[i % len(labels)]
        i += 1
        if pools[k]:
            out.append(pools[k].pop())
    return out


def cap_label(rows, lab, share=0.5):
    """Drop rows of the largest labels until no label exceeds `share` of the rows (keeps order)."""
    rows = list(rows)
    while True:
        c = collections.Counter(lab(r) for r in rows)
        top, n = c.most_common(1)[0]
        if n <= share * len(rows) or len(c) < 2:
            return rows
        excess = n - int(share * (len(rows) - n) / (1 - share))
        drop, out = excess, []
        for r in reversed(rows):
            if drop > 0 and lab(r) == top:
                drop -= 1
                continue
            out.append(r)
        rows = list(reversed(out))


def report(rows, qkey=lambda r: r["meta"].get("defs") or r["instructions"][:60]):
    """Print counts, balance, edge tags and length stats per question type."""
    by = collections.defaultdict(list)
    for r in rows:
        by[qkey(r)].append(r)
    print(f"TOTAL rows={len(rows)}")
    for q, rs in sorted(by.items()):
        c = collections.Counter(r["gold"] for r in rs)
        top = max(c.values()) / len(rs)
        print(f"  [{q}] n={len(rs)} options={len(rs[0]['options'])} labels_used={len(c)} max_share={top:.1%}")
        print("     ", dict(c.most_common()))
    allc = collections.Counter(r["gold"] for r in rows)
    print(f"  overall max gold share={max(allc.values()) / len(rows):.1%}")
    print("  edge:", dict(collections.Counter(r["meta"]["edge"] for r in rows).most_common()))
    L = sorted(len(r["state"]) for r in rows)
    print(f"  state chars min={L[0]} median={L[len(L) // 2]} max={L[-1]}")


def near_dedupe(rows, text_fn=lambda r: r["state"], thr=0.8, n=5):
    """Drop rows whose word n-gram set has Jaccard >= thr with an earlier kept row (short texts: same word set)."""
    index = collections.defaultdict(list)
    kept_sets, kept, dropped = [], [], 0
    for r in rows:
        w = re.findall(r"[a-z0-9]+", text_fn(r).lower())
        if len(w) < n + 2:
            g = {" ".join(sorted(set(w)))}
        else:
            g = {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}
        cand = collections.Counter()
        for x in g:
            for j in index.get(x, ()):
                cand[j] += 1
        dup = False
        for j, inter in cand.items():
            if inter / (len(g) + len(kept_sets[j]) - inter) >= thr:
                dup = True
                break
        if dup:
            dropped += 1
            continue
        k = len(kept_sets)
        kept_sets.append(g)
        for x in g:
            index[x].append(k)
        kept.append(r)
    print(f"near-dedupe: dropped {dropped} of {len(rows)}")
    return kept
