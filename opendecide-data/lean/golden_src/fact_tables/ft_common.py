"""Shared helpers for the v14 golden family `fact_tables` (fact verification against tables + text evidence).

Only helpers live here; every dataset has its own build_<key>.py. Everything is CPU-only and deterministic.
"""
import fcntl
import hashlib
import json
import random
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent          # lean/golden_src/fact_tables
GOLDEN = HERE.parent                            # lean/golden_src
LEAN = GOLDEN.parent                            # lean
ROOT = LEAN.parent                              # opendecide-data
JEV = ROOT.parent
RAW_DIR = LEAN / "data" / "v14_parts" / "raw"
DEFS_DIR = LEAN / "data" / "v14_parts" / "defs"
MANIFEST = GOLDEN / "MANIFEST.jsonl"
CACHE = HERE / "cache"
FAMILY = "fact_tables"
SEED = 20261101
GRAM = 13

EDGE_TAGS = {"negation", "double_negation", "exception", "missing_info", "conflicting_evidence", "temporal", "numeric",
             "units", "quantifier", "hypothetical", "reported_speech", "sarcasm", "implicit", "long_context", "table",
             "multi_hop", "ambiguous"}

_W = re.compile(r"[\W_]+")


def words(t):
    return _W.sub(" ", t.casefold()).split()


def norm(t):
    return " ".join(words(t))


def grams(ws, n=GRAM):
    return {" ".join(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def fetch(url, dest, sha=None):
    """Download url to dest once (certifi TLS via requests); check sha256 when given."""
    dest = Path(dest)
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        r = requests.get(url, timeout=600)
        r.raise_for_status()
        tmp = dest.with_suffix(dest.suffix + ".part")
        tmp.write_bytes(r.content)
        tmp.rename(dest)
    if sha is not None:
        got = sha256_file(dest)
        if got != sha:
            raise SystemExit(f"sha256 mismatch for {dest}: {got}")
    return dest


# ----------------------------------------------------------------------------------------------- rendering
def clean_cell(v, max_chars=200):
    v = re.sub(r"\s+", " ", str(v)).strip()
    if len(v) > max_chars:
        v = v[:max_chars - 3].rstrip() + "..."
    return v


def render_table(rows, max_cell_chars=200):
    """Pipe table, one line per row, first row as given (callers say which row is the header)."""
    out = []
    for r in rows:
        cells = [clean_cell(c, max_cell_chars) for c in r]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


# ----------------------------------------------------------------------------------------------- numbers
NUM_RE = re.compile(r"(?<![\w.])[-−(]?\$?\s?\d[\d,]*(?:\.\d+)?\)?%?")


def parse_num(s):
    """Parse '1,234.5', '(1,234)', '-3.2%', '$ 45' -> float, else None."""
    if s is None:
        return None
    t = str(s).strip().replace("−", "-").replace("$", "").replace(",", "").replace("%", "").strip()
    neg = False
    if t.startswith("(") and t.endswith(")"):
        neg, t = True, t[1:-1].strip()
    try:
        v = float(t)
    except ValueError:
        return None
    return -v if neg else v


def decimals_of(s):
    t = str(s).replace(",", "").strip().rstrip("%")
    if "." in t:
        return len(t.split(".")[1].rstrip(")"))
    return 0


def fmt_num(v, dec, commas=True):
    if dec <= 0:
        s = f"{round(v):,}" if commas else f"{round(v)}"
    else:
        s = f"{v:,.{dec}f}" if commas else f"{v:.{dec}f}"
    if s in ("-0", "-0.0", "-0.00"):
        s = s[1:]
    return s


def clearly_different(d, g, dec, rel=0.02):
    """True when candidate d is a clearly different answer from gold g at gold's precision."""
    step = 10 ** (-dec) if dec > 0 else 1
    if round(d, max(dec, 0)) == round(g, max(dec, 0)):
        return False
    if abs(d - g) < 2 * step - 1e-12:
        return False
    return abs(d - g) >= rel * max(abs(g), 1e-9)


# ----------------------------------------------------------------------------------------------- decontamination
def is_heldout(rel_parts):
    parts = [x.lower() for x in rel_parts]
    return any(x.startswith(("ohs", "preds", "results")) for x in parts)


def scan_files():
    """Our non-held-out jsonl files (train, dev, eval, JevBench public). ohs*/preds*/results* are never opened.
    data/v14_parts and golden_src are skipped (other v14 builders write there concurrently; cross-family dedupe happens
    at merge)."""
    fs = set()
    for base in (LEAN, ROOT / "data"):
        for p in base.rglob("*.jsonl"):
            rel = p.relative_to(base)
            if is_heldout(rel.parts) or "cache" in rel.parts or ".venv" in rel.parts or "v14_parts" in rel.parts \
                    or "golden_src" in rel.parts:
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


def heldout_source_texts():
    """Wikipedia-text source split behind a held-out task (VitaminC test, OHS-1), reused read-only from the
    breadth decontamination cache; used only to drop rows."""
    p = LEAN / "breadth_src/cache/heldout_decon/tals__vitaminc/be6febb761b0/test.jsonl"
    if p.exists():
        with open(p, encoding="utf-8") as f:
            for line in f:
                yield from _strings(json.loads(line))


def local_decontam(docs, heldout=False, gram=GRAM):
    """docs: {doc_id: text}. Returns {doc_id: first source path hit} for docs sharing a word 13-gram with any string
    in our local non-held-out jsonl files (and, if heldout=True, with the VitaminC test source split)."""
    owner = defaultdict(set)
    for did, t in docs.items():
        for g in grams(words(t), gram):
            owner[hash(g)].add(did)
    hit = {}
    dgrams = {}

    def check(t, src):
        w = words(t)
        for i in range(len(w) - gram + 1):
            g = " ".join(w[i:i + gram])
            h = hash(g)
            if h in owner:
                for did in owner[h]:
                    if did in hit:
                        continue
                    if did not in dgrams:
                        dgrams[did] = grams(words(docs[did]), gram)
                    if g in dgrams[did]:
                        hit[did] = src

    if heldout:
        for t in heldout_source_texts():
            check(t, "HELDOUT_SOURCE:vitaminc_test")
    seen = set()
    files = scan_files()
    for p in files:
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    x = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                for t in _strings(x):
                    if len(t) < 40:
                        continue
                    h = hash(t)
                    if h in seen:
                        continue
                    seen.add(h)
                    check(t, str(p.relative_to(ROOT.parent)))
    print(f"local decontam: {len(docs)} docs, {len(files)} files scanned, {len(hit)} docs hit")
    return hit


def tabfact_index():
    """TabFact (OHS-2 held-out source) page titles, table captions and statement 8-grams, for dropping rows only.
    Downloaded from the public TabFact repo (github wenhuchen/Table-Fact-Checking, master)."""
    tf = CACHE / "tabfact_decon"
    base = "https://raw.githubusercontent.com/wenhuchen/Table-Fact-Checking/master/"
    t2p = json.load(open(fetch(base + "data/table_to_page.json", tf / "table_to_page.json")))
    titles = {norm(v[0]) for v in t2p.values()}
    urls = {v[1].rsplit("/", 1)[-1].lower() for v in t2p.values()}
    caps, g8, short = set(), set(), set()
    for f in ("r1_training_all.json", "r2_training_all.json"):
        for _tid, (stmts, _labels, cap) in json.load(open(fetch(base + "collected_data/" + f, tf / f))).items():
            caps.add(norm(cap))
            for s in stmts:
                ws = words(s)
                g8 |= grams(ws, 8)
                short.add(" ".join(ws))
    return {"titles": titles, "urls": urls, "captions": caps, "g8": g8, "short": short}


def tabfact_hit(tfi, title=None, url=None, text=None):
    if title and norm(title) in tfi["titles"] | tfi["captions"]:
        return "tabfact_title"
    if url and url.rsplit("/", 1)[-1].lower() in tfi["urls"]:
        return "tabfact_url"
    if text:
        ws = words(text)
        if len(ws) < 8:
            if " ".join(ws) in tfi["short"]:
                return "tabfact_statement"
        elif grams(ws, 8) & tfi["g8"]:
            return "tabfact_statement_8gram"
    return None


# ----------------------------------------------------------------------------------------------- output
def write_outputs(key, rows, defs):
    """rows: list of row dicts. defs: {qid_or_None: {option: definition}}; None -> defs/<key>.json."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    DEFS_DIR.mkdir(parents=True, exist_ok=True)
    out = RAW_DIR / f"{key}.jsonl"
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    for qid, d in defs.items():
        p = DEFS_DIR / (f"{key}.json" if qid is None else f"{key}__{qid}.json")
        p.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def check_rows(key, rows):
    """Hard checks + summary print. Returns summary dict."""
    assert rows, "no rows"
    rids = [r["rid"] for r in rows]
    assert len(set(rids)) == len(rids), "duplicate rid"
    states = [norm(r["state"]) for r in rows]
    assert len(set(states)) == len(states), "duplicate state"
    for r in rows:
        assert r["key"] == key and r["state"].strip() and r["instructions"].strip()
        assert r["gold"] in r["options"], r
        assert r["options"] == ["yes", "no"] or len(r["options"]) >= 2
        assert r["meta"]["split"] == "train"
        e = r["meta"].get("edge")
        assert e is None or e in EDGE_TAGS, e
        if r["soft"] is not None:
            assert abs(sum(r["soft"].values()) - 1) < 1e-6
    yn = [r for r in rows if r["options"] == ["yes", "no"]]
    share = sum(r["gold"] == "yes" for r in yn) / len(yn) if yn else None
    lens = [len(r["state"]) for r in rows]
    edges = Counter(r["meta"].get("edge") for r in rows)
    print(f"[{key}] rows={len(rows)} yes/no rows={len(yn)} yes share={share if share is None else round(share, 4)}")
    print(f"[{key}] instructions: {dict(Counter(r['instructions'] for r in rows))}")
    print(f"[{key}] gold by instruction: {dict(Counter((r['instructions'][:40], r['gold']) for r in rows))}")
    print(f"[{key}] edge: {dict(edges)}")
    print(f"[{key}] state chars min/median/mean/max: {min(lens)}/{int(statistics.median(lens))}/"
          f"{int(statistics.mean(lens))}/{max(lens)}")
    return {"rows": len(rows), "yesno_share": share, "edge_tags": sorted(k for k in edges if k)}


def append_manifest(rec):
    """Append once per key (skips if the key is already recorded). flock guards concurrent appends."""
    MANIFEST.touch(exist_ok=True)
    with open(MANIFEST, "r+", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        keys = set()
        for line in f:
            try:
                keys.add(json.loads(line).get("key"))
            except Exception:  # noqa: BLE001
                pass
        if rec["key"] in keys:
            print(f"manifest: {rec['key']} already recorded, not appended")
        else:
            f.seek(0, 2)
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(f"manifest: appended {rec['key']}")
        fcntl.flock(f, fcntl.LOCK_UN)


def balanced_pick(cands, strata_key, label_key, n, rng):
    """Round-robin over strata; inside each stratum alternate labels so yes/no stay balanced per stratum."""
    strata = defaultdict(lambda: defaultdict(list))
    for c in cands:
        strata[strata_key(c)][label_key(c)].append(c)
    for s in strata.values():
        for lst in s.values():
            rng.shuffle(lst)
    # per stratum, keep equal counts of each label (min over labels)
    queues = {}
    for sk, by in strata.items():
        labs = sorted(by)
        m = min(len(by[l]) for l in labs) if len(labs) > 1 else 0
        q = []
        for i in range(m):
            for l in labs:
                q.append(by[l][i])
        queues[sk] = q
    out, keys, i = [], sorted(queues, key=str), 0
    while len(out) < n and any(queues.values()):
        k = keys[i % len(keys)]
        if queues[k]:
            out.append(queues[k].pop(0))
            if queues[k] and len(out) < n:
                out.append(queues[k].pop(0))
        i += 1
    return out
