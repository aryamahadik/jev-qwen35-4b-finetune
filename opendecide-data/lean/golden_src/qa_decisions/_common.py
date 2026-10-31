"""Shared helpers for the qa_decisions golden builders (v14). CPU-only, deterministic, no model calls.

- fetch(): pinned URL download into golden_src/qa_decisions/cache/<key>/ with a sha256 check.
- decon(): drops candidate records whose core texts share an exact normalised text (>= 6 words) or a 10-word run
  with (a) every premise of tasksource/zero-shot-label-nli (forbidden, all 152 tasks, all splits; read only to drop
  overlaps, as breadth_src/build_ghc.py does), (b) every local *.jsonl under lean/ and ../data except held-out files
  (ohs*, preds*, results*), caches and data/v14_parts (other golden parts are cross-deduped at compile time), and
  (c) the JevBench public splits. Held-out (OHS) files are never opened here; the compile step decontaminates
  against them.
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
import urllib.request
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent            # golden_src/qa_decisions
GOLDEN = HERE.parent                               # golden_src
LEAN = GOLDEN.parent                               # lean
ROOT = LEAN.parent                                 # opendecide-data
JEV = ROOT.parent                                  # jev
RAW_DIR = LEAN / "data" / "v14_parts" / "raw"
DEFS_DIR = LEAN / "data" / "v14_parts" / "defs"
MANIFEST = GOLDEN / "MANIFEST.jsonl"
FAMILY = "qa_decisions"
YN = ["yes", "no"]

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
        req = urllib.request.Request(url, headers={"User-Agent": "opendecide-golden-builder"})
        with urllib.request.urlopen(req, timeout=600) as r, open(path, "wb") as f:
            while True:
                b = r.read(1 << 20)
                if not b:
                    break
                f.write(b)
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
    t = str(t).replace("\u00a0", " ")
    t = re.sub(r"[ \t]+", " ", t)
    return t.strip()


NEG = re.compile(r"\b(not|no|never|none|nobody|nothing|nowhere|neither|nor|without|cannot|n't|isn't|aren't|wasn't|"
                 r"weren't|don't|doesn't|didn't|won't|wouldn't|can't|couldn't|shouldn't|hasn't|haven't|hadn't|"
                 r"unable|lack|lacks|lacked|refuse[sd]?|fail(?:s|ed)?)\b", re.I)
NEG_STRICT = re.compile(r"\b(not|no|never|none|nobody|nothing|neither|nor|without|cannot)\b|n't\b", re.I)
QUANT = re.compile(r"\b(all|every|each|some|any|most|few|both|either|neither|only|at least|at most|exactly|none of|"
                   r"more than|less than|fewer than)\b", re.I)
NUM = re.compile(r"\d|\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|"
                 r"hundred|thousand|million|billion|dozen|half|twice|double|triple|percent)\b", re.I)
UNITS = re.compile(r"\b\d[\d,.]*\s?(km|kg|g|mg|lb|lbs|pounds?|miles?|feet|foot|inch(?:es)?|meters?|metres?|cm|mm|"
                   r"liters?|litres?|gallons?|ounces?|oz|degrees?|°[cf]?|mph|kph|hours?|minutes?|seconds?|"
                   r"calories|watts?|volts?)\b", re.I)
TEMP = re.compile(r"\b(before|after|afterwards?|then|while|during|until|since|yesterday|tomorrow|tonight|ago|later|"
                  r"earlier|soon|next|previous(?:ly)?|already|still|year|years|month|months|week|weeks|day|days|"
                  r"hour|hours|minute|minutes|morning|evening|night|century|decade|born|died|founded|older|younger|"
                  r"oldest|youngest|first|last|once|when|finally|eventually|season|winter|summer|spring|autumn)\b",
                  re.I)
HYPO = re.compile(r"\b(if|would|could|might|unless|suppose|imagine|pretend)\b", re.I)


def neg_count(t):
    return len(NEG_STRICT.findall(t))


_NEG_TOK = {"not", "no", "never", "none", "nobody", "nothing", "neither", "nor", "without", "cannot"}
_NEG_PREFIX = re.compile(r"^(un|in|im|il|ir|dis|non)[a-z]{3,}$")
_NOT_PREFIXED = {"under", "understand", "understood", "until", "unit", "united", "universe", "university", "into",
                 "inside", "interest", "interested", "instead", "information", "include", "important", "impact",
                 "increase", "income", "indeed", "individual", "inform", "industry", "image", "imagine", "island",
                 "illness", "issue", "discuss", "dish", "disk", "distance", "district", "display", "discover",
                 "dinner", "direct", "direction", "iron", "irish", "irritate", "irritated", "invite", "invited",
                 "invest", "insect", "instrument", "internet", "interview", "introduce", "invent", "invented",
                 "influence", "injury", "injured", "ink", "inch", "inches", "income", "input", "insurance"}


def is_double_negation(t):
    """Two negations that act on each other: two negation cues within 2 tokens ('not ... no', 'never not'), or a
    negation cue directly before a negatively prefixed word ('not unlike', 'not impossible', "isn't uncommon")."""
    toks = re.findall(r"[a-z]+'?[a-z]*", t.lower())
    toks = ["not" if x.endswith("n't") else x for x in toks]
    pos = [i for i, x in enumerate(toks) if x in _NEG_TOK]
    if any(b - a <= 2 for a, b in zip(pos, pos[1:])):
        return True
    for i in pos:
        for j in (i + 1, i + 2):
            if j < len(toks) and _NEG_PREFIX.match(toks[j]) and toks[j] not in _NOT_PREFIXED:
                return True
    return False


def edge(text, order=("double_negation", "negation", "units", "numeric", "quantifier", "temporal"), default=None):
    """First matching tag in `order` (surface cues on the text the decision depends on)."""
    for tag in order:
        if tag == "double_negation" and is_double_negation(text):
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
            p = fetch(LABEL_NLI_URL.format(rev=LABEL_NLI_REV, name=name), HERE / "cache" / "_label_nli" / name, sha)
        out.append(p)
    return out


def decon(core, verbose=True):
    """core: {rid: [text, ...]} -> {rid: reason} for records that overlap a forbidden / used / eval text."""
    exact = collections.defaultdict(set)
    owner = collections.defaultdict(set)
    for rid, texts in core.items():
        for t in texts:
            w = words(t)
            if len(w) >= MIN_EXACT:
                exact[" ".join(w)].add(rid)
            for i in range(len(w) - RUN + 1):
                owner[hash(tuple(w[i:i + RUN]))].add(rid)
    hits = {}

    def check(text, reason):
        w = words(text)
        if not w:
            return
        for rid in exact.get(" ".join(w), ()):
            hits.setdefault(rid, reason)
        for i in range(len(w) - RUN + 1):
            h = hash(tuple(w[i:i + RUN]))
            if h in owner:
                for rid in owner[h]:
                    hits.setdefault(rid, reason)

    # (a) forbidden label-NLI (all tasks, all splits), premise column only (hypotheses are label verbalisations)
    for p in label_nli_files():
        df = pd.read_parquet(p, columns=["premise"])
        for t in set(df["premise"].astype(str)):
            check(t, "label_nli")
    n_a = len(hits)
    # (b) local jsonl (train/dev/eval, no held-out) + (c) JevBench public
    files = scan_files()
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
    if verbose:
        print(f"decon: {len(core)} records, label-NLI hits={n_a}, local/jevbench hits={len(hits) - n_a} "
              f"({len(files)} files scanned)")
    return hits


# ----------------------------------------------------------------------------------------------- near-dup
def near_dup_filter(items, text_of, thresh=0.85, block_of=None):
    """Greedy near-duplicate removal (word-set Jaccard >= thresh within a block). Keeps order; returns kept list."""
    kept, seen_exact = [], set()
    blocks = collections.defaultdict(list)
    for it in items:
        t = text_of(it)
        n = norm(t)
        if n in seen_exact:
            continue
        ws = set(n.split())
        b = block_of(it) if block_of else tuple(sorted(ws))[:1]
        if any(len(ws & o) / max(1, len(ws | o)) >= thresh for o in blocks[b]):
            continue
        seen_exact.add(n)
        blocks[b].append(ws)
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
        qid = r["meta"].get("defs")
        d = defs_by_qid[qid] if qid else defs_by_qid[None]
        assert all(o in d for o in r["options"]), (qid, r["options"])
        if r["soft"] is not None:
            assert abs(sum(r["soft"].values()) - 1) < 1e-6
    yn = [r for r in rows if r["options"] == YN]
    if yn:
        share = sum(r["gold"] == "yes" for r in yn) / len(yn)
        assert 0.35 <= share <= 0.65, f"yes share {share:.3f}"
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
    print(f"  question sets: {dict(qids)}")
    print(f"  choice gold dist: {dict(sorted(gold_ch.items()))}")
    print(f"  edge tags: {dict(edges.most_common())}")
    print(f"  state chars: min={lens[0]} median={lens[len(lens) // 2]} max={lens[-1]}")
    return {"yes_share": round(ys, 4) if ys is not None else None, "edges": edges, "n_yn": len(yn), "n_ch": len(ch)}


def show_samples(rows, n=5, seed=7):
    rng = random.Random(seed)
    for r in rng.sample(rows, min(n, len(rows))):
        print("-" * 100)
        print("RID:", r["rid"], "| edge:", r["meta"].get("edge"), "| defs:", r["meta"].get("defs"))
        print("STATE:\n" + r["state"])
        print("Q:", r["instructions"])
        print("OPTIONS:", r["options"], "| GOLD:", r["gold"])


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


def letters(n):
    return [chr(ord("A") + i) for i in range(n)]
