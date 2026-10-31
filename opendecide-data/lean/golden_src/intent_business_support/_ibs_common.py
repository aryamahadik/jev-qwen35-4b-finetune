"""Shared helpers for the intent_business_support golden builders (v14).

Only paths, pinned downloads, text normalisation, row checks and writers live here; every builder keeps its own
source-specific logic, questions and definitions. CPU only, no model calls.
"""
import collections
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

FAMILY = "intent_business_support"
HERE = Path(__file__).resolve().parent
LEAN = HERE.parent.parent
CACHE = HERE / "cache"
RAW = LEAN / "data" / "v14_parts" / "raw"
DEFS = LEAN / "data" / "v14_parts" / "defs"

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
        urllib.request.urlretrieve(url, tmp)
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


def mwz_partition(dialogue_id):
    """MultiWOZ dialogue partition shared by the dstc9 and multiwoz builders (0 = dstc9 context rows, 1 = multiwoz)."""
    return stable_hash("mwz-partition:" + dialogue_id.replace(".json", "")) % 2


def check_rows(rows, key):
    """Hard checks every builder runs before writing."""
    assert rows, "no rows"
    seen_rid, seen_state = set(), set()
    for r in rows:
        assert r["key"] == key
        assert r["state"].strip() and r["instructions"].strip()
        assert r["gold"] in r["options"], (r["rid"], r["gold"], r["options"])
        assert len(set(r["options"])) == len(r["options"])
        if r["soft"] is not None:
            assert set(r["soft"]) <= set(r["options"]) and abs(sum(r["soft"].values()) - 1) < 1e-6
        m = r["meta"]
        assert m["split"] == "train" and m["family"] == FAMILY and m["edge"] in EDGE_TAGS, m
        assert r["rid"] not in seen_rid, ("duplicate rid", r["rid"])
        seen_rid.add(r["rid"])
        n = norm(r["state"])
        assert n not in seen_state, ("duplicate state", r["rid"])
        seen_state.add(n)


def write_rows(rows, key):
    """Drop rows listed in decon_hits.json (13-gram hits found by decon_ibs.py), check, then write."""
    hits_file = HERE / "decon_hits.json"
    if hits_file.exists():
        bad = {rid for k, rid, _ in json.load(open(hits_file)) if k == key}
        if bad:
            rows = [r for r in rows if r["rid"] not in bad]
            print(f"decon: dropped {len(bad)} listed rows")
    check_rows(rows, key)
    RAW.mkdir(parents=True, exist_ok=True)
    out = RAW / f"{key}.jsonl"
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return out


def write_defs(defs, key, qid=None):
    DEFS.mkdir(parents=True, exist_ok=True)
    out = DEFS / (f"{key}__{qid}.json" if qid else f"{key}.json")
    with open(out, "w") as f:
        json.dump(defs, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return out


def report(rows, qkey=lambda r: r["meta"].get("defs") or r["instructions"][:60]):
    """Print counts, balance, edge tags and length stats per question type."""
    by = collections.defaultdict(list)
    for r in rows:
        by[qkey(r)].append(r)
    print(f"TOTAL rows={len(rows)}")
    for q, rs in sorted(by.items()):
        c = collections.Counter(r["gold"] for r in rs)
        top = max(c.values()) / len(rs)
        print(f"  [{q}] n={len(rs)} max_share={top:.1%} labels={dict(sorted(c.items()))}")
    yn = [r for r in rows if r["options"] == ["yes", "no"]]
    if yn:
        print(f"  yes/no rows={len(yn)} yes share={sum(r['gold'] == 'yes' for r in yn) / len(yn):.1%}")
    print("  edge:", dict(collections.Counter(r["meta"]["edge"] for r in rows).most_common()))
    L = sorted(len(r["state"]) for r in rows)
    print(f"  state chars min={L[0]} median={L[len(L) // 2]} max={L[-1]}")
