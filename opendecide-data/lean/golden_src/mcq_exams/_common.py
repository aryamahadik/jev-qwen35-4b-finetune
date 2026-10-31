"""Shared helpers for the mcq_exams golden builders (v14, round 2). CPU-only, deterministic, no model calls.

Multiple-choice exam rows keep the exam's own answer choices as the options (qtype choice, 3-60 options). Because every
question has its own answer choices, every row gets its own definitions file: defs/<key>__<qid>.json with
meta.defs = qid (the GOLDEN_SPEC per-question option-set mechanism). Each definition restates its option in full (so it
still carries the meaning when the compile step swaps option names for opaque codes) and states the exam's decision
rule for that option type (normal answer, exception/NOT question, fill-in-the-blank, 'all/none of these', combined
choices, numeric value).

- fetch(): pinned URL download with a sha256 check (certifi CA bundle: the framework Python has none here).
- decon(): drops candidate records whose core texts share an exact normalised text (>= 6 words) or a 10-word run with
  (a) every premise of tasksource/zero-shot-label-nli (forbidden, all 152 tasks, all splits; read only to drop
  overlaps), (b) every local *.jsonl under lean/ and ../data except held-out files (ohs*, preds*, results*) and caches,
  including the round-1 golden raw parts (data/v14_parts/raw, except this family's own keys), and (c) the JevBench
  public splits. Held-out (OHS) files are never opened here; the compile step decontaminates against them.
- option_defs(): the per-row option definitions.
- write_outputs() / append_manifest(): raw rows, per-row defs and the MANIFEST record (file-locked, replaces an older
  record of the same key so reruns do not duplicate it).
"""
import collections
import fcntl
import hashlib
import json
import random
import re
import ssl
import sys
import urllib.request
from pathlib import Path

import certifi
import pandas as pd

HERE = Path(__file__).resolve().parent            # golden_src/mcq_exams
GOLDEN = HERE.parent                               # golden_src
LEAN = GOLDEN.parent                               # lean
ROOT = LEAN.parent                                 # opendecide-data
JEV = ROOT.parent                                  # jev
RAW_DIR = LEAN / "data" / "v14_parts" / "raw"
DEFS_DIR = LEAN / "data" / "v14_parts" / "defs"
MANIFEST = GOLDEN / "MANIFEST.jsonl"
FAMILY = "mcq_exams"
OWN_KEYS = {"aqua_rat", "uscg_mariner", "ncvec_ham", "nrc_gfe", "opentdb"}

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
MAX_OPT_WORDS = 40  # rows with a longer answer choice are dropped (its definition could not stay near 40 words)
MIN_EXACT = 6     # exact-match only for texts of at least this many words
CTX = ssl.create_default_context(cafile=certifi.where())


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
        with urllib.request.urlopen(req, timeout=600, context=CTX) as r, open(path, "wb") as f:
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
    """Whitespace tidy only (no rewording)."""
    t = str(t).replace(" ", " ").replace("​", "")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    return t.strip()


NEG_Q = re.compile(r"\b(NOT|EXCEPT|FALSE|INCORRECT|LEAST|NEVER|UNTRUE|NO LONGER)\b|\bnot\b|\bexcept\b|\bincorrect\b|"
                   r"\bfalse\b|\bleast\b|\bnever\b", re.S)
UNITS = re.compile(r"\b\d[\d,.]*\s?(km|kg|g|mg|lb|lbs|pounds?|miles?|feet|foot|ft|inch(?:es)?|in\.|meters?|metres?|m|cm|"
                   r"mm|liters?|litres?|gallons?|gal|ounces?|oz|degrees?|°[CF]?|mph|kph|km/h|kmph|knots?|kts|hours?|hrs?|"
                   r"minutes?|min|seconds?|sec|s|watts?|W|kW|volts?|V|amps?|A|ohms?|Ω|psi|psig|bar|Hz|kHz|MHz|GHz|dB|"
                   r"tons?|tonnes?|long tons|LT|rpm|BTU|°F|°C)(?![A-Za-z])", re.I)
NUMERIC = re.compile(r"\d")
BLANK = re.compile(r"_{3,}")
ALL_RE = re.compile(r"^(all (of )?(these|the above|of the above|of these|the choices|the answers|these choices|"
                    r"the above answers)( choices| answers)?( are correct| are true| is correct)?|all are correct|"
                    r"all of them|each of the above)\.?$", re.I)
NONE_RE = re.compile(r"^(none of (these|the above|them|these choices|the above answers|the choices|the above choices)"
                     r"( is correct| are correct)?|none|none of these answers|neither)\.?$", re.I)
LETTER_REF = re.compile(r"^(?:(both|only|either)\s+)?\(?([A-E])\)?\s*(,|and|&|or)\s*\(?([A-E])\)?(?:\s*(?:,|and|&|or)\s*"
                        r"\(?([A-E])\)?)?\s*(only|are correct|are true|but not [A-E])?\.?$", re.I)


def is_all(opt):
    return bool(ALL_RE.match(opt.strip()))


def is_none(opt):
    return bool(NONE_RE.match(opt.strip()))


def letter_refs(opt, n_opts):
    """'Both A and B' / 'A and C' / 'A, B, and C' -> [0, 1] etc.; None if the option is not a letter combination."""
    m = LETTER_REF.match(opt.strip())
    if not m:
        return None
    idx = [ord(x.upper()) - 65 for x in (m.group(2), m.group(4), m.group(5)) if x]
    if any(i >= n_opts for i in idx):
        return None
    return idx


def negative_question(stem):
    """An explicit exception question, where the keyed choice is the one that fails the stated condition while the
    others meet it: 'all of the following ... EXCEPT', 'Which statement is FALSE / INCORRECT'. (Questions with NOT are
    too varied to classify by rule -- 'Which vessel is NOT required ...' vs 'a position that is NOT based on ...' --
    so they get the negation-aware definition instead, see option_defs.)"""
    s = stem.strip()
    if re.search(r"\bEXCEPT\b", s) or re.search(r"\ball of the following\b[^?]*\bexcept\b|\ball except\b", s, re.I):
        return True
    return bool(re.search(r"\b(which|what)\b( of the following| one)?( statement| answer| choice)?[^?.,]{0,40}\b"
                          r"(is|are)\s+(FALSE|false|INCORRECT|incorrect|UNTRUE|untrue)\b", s))


def not_question(stem):
    """The question contains an upper-case NOT (exam emphasis) -- the keyed choice must respect it."""
    return bool(re.search(r"\bNOT\b", stem))


def has_negation(text):
    return bool(re.search(r"\b(not|never|no|none|except|cannot|without|neither|nor|unless)\b|n't\b", text, re.I))


# ----------------------------------------------------------------------------------------------- definitions
def _q(t, n=160):
    t = re.sub(r"\s+", " ", t).strip()
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + " ..."


def option_defs(stem, options, kind="exam", numeric=False):
    """One definition per option (restating the option in full and the exam's decision rule for it).

    kind: 'exam' (single best answer to an exam question) or 'math' (the value the word problem asks for).
    """
    neg = negative_question(stem)
    notq = not_question(stem)
    blank = bool(BLANK.search(stem))
    out = {}
    n = len(options)
    for i, o in enumerate(options):
        oq = o.strip()
        refs = letter_refs(oq, n)
        if len(oq.split()) > 18 and not refs and kind != "math":  # long choice: restate it with the short rule
            out[o] = (f'Answer "{oq}": correct only if it is the '
                      + ("one listed choice that fails the stated condition (the exception asked for)." if neg
                         else "best answer to the question exactly as asked" + (", respecting its NOT." if notq else ".")))
            continue
        if is_all(oq):
            d = (f'Answer "{oq}": correct only if every other listed choice is a right answer to the question; '
                 f'wrong if even one other choice is wrong.')
        elif is_none(oq):
            d = (f'Answer "{oq}": correct only if none of the other listed choices is a right answer to the question; '
                 f'wrong if any other choice is right.')
        elif refs:
            names = [f'"{options[j].strip()}"' for j in refs]
            joined = ", ".join(names[:-1]) + " and " + names[-1]
            d = (f'Answer "{oq}" (the listed choices {joined}): correct only if exactly those choices are all right '
                 f'and together form the best answer.')
        elif kind == "math":
            d = (f'Answer {oq}: correct only if solving the problem exactly as stated gives {oq} (up to the rounding '
                 f'the choices themselves use); any other result makes it wrong.')
        elif neg:
            d = (f'Answer "{oq}": the question asks for the exception (EXCEPT / false), so this is correct only if it '
                 f'is the one listed choice that fails the stated condition while the other choices meet it.')
        elif notq:
            d = (f'Answer "{oq}": correct only if it is the best answer to the question exactly as asked, respecting '
                 f'its NOT (for "which ... is NOT ..." wording, the one choice that fails the condition).')
        elif blank and len(BLANK.findall(stem)) >= 2 and ";" in oq:
            d = (f'Answer "{oq}": correct only if filling the blanks in order with its parts (separated by ";") makes '
                 f'the statement true; if either part is wrong, the choice is wrong.')
        elif blank:
            d = (f'Answer "{oq}": correct only if filling the blank with it makes the statement true and it is the '
                 f'best completion among the listed choices.')
        else:
            d = (f'Answer "{oq}": correct only if it is the best answer to the question as asked; a choice that is only '
                 f'partly true, true only in other conditions, or less complete than another is wrong.')
        out[o] = d
    return out


# ----------------------------------------------------------------------------------------------- decontamination
def _is_skipped(rel_parts):
    parts = [x.lower() for x in rel_parts]
    if any(x.startswith(("ohs", "preds", "results")) for x in parts):
        return True
    if "cache" in parts or ".venv" in parts or "node_modules" in parts:
        return True
    if "v14_parts" in parts:  # only the round-1/2 raw parts of OTHER keys are scanned (below)
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
    for p in RAW_DIR.glob("*.jsonl"):
        if p.stem not in OWN_KEYS:
            fs.add(p)
    if JEVBENCH_PUBLIC.exists():
        fs |= set(JEVBENCH_PUBLIC.glob("*.jsonl"))
    return sorted(fs)


def label_nli_files():
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

    for p in label_nli_files():
        df = pd.read_parquet(p, columns=["premise"])
        for t in set(df["premise"].astype(str)):
            check(t, "label_nli")
    n_a = len(hits)
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
        by = collections.Counter(v for v in hits.values())
        print(f"decon: {len(core)} records, label-NLI hits={n_a}, local/jevbench hits={len(hits) - n_a} "
              f"({len(files)} files scanned); top reasons {by.most_common(6)}")
    return hits


# ----------------------------------------------------------------------------------------------- near-dup
def shingles(t, k=3):
    w = words(t)
    return {tuple(w[i:i + k]) for i in range(max(1, len(w) - k + 1))}


def _stable_hash(shingle):
    return hashlib.blake2b(" ".join(shingle).encode("utf-8"), digest_size=8).digest()


def near_dup_filter(items, text_of, thresh=0.8, strip_numbers=True):
    """Greedy near-duplicate removal: word-3-gram Jaccard >= thresh (numbers masked when strip_numbers, so variants of
    one problem that only change the numbers count as near-duplicates). Blocked by an LSH-lite key (rare shingles)."""
    kept, seen_exact = [], set()
    index = collections.defaultdict(list)
    sigs = []
    for it in items:
        t = text_of(it)
        if strip_numbers:
            t = re.sub(r"\d+(?:[.,]\d+)*", "0", t)
        n = norm(t)
        if n in seen_exact:
            continue
        sh = shingles(n)
        # min-hash style keys; a stable hash (built-in hash() of str is salted per process, which made the kept set
        # vary between runs -- reviewer fix for GOLDEN_SPEC rule 6, determinism)
        keys = sorted(sh, key=_stable_hash)[:4]
        cand = set()
        for k in keys:
            cand.update(index[k])
        if any(len(sh & sigs[j]) / max(1, len(sh | sigs[j])) >= thresh for j in cand):
            continue
        seen_exact.add(n)
        j = len(sigs)
        sigs.append(sh)
        for k in keys:
            index[k].append(j)
        kept.append(it)
    return kept


# ----------------------------------------------------------------------------------------------- output
def qid_of(rid):
    return re.sub(r"[^A-Za-z0-9_-]+", "_", rid)


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
        assert 3 <= len(r["options"]) <= 60, r["options"]
        assert len(set(r["options"])) == len(r["options"]), r["options"]
        assert all(o.strip() for o in r["options"])
        assert r["meta"]["split"] == "train"
        d = defs_by_qid[r["meta"]["defs"]]
        assert set(d) == set(r["options"]), (r["meta"]["defs"], r["options"])
        assert all(len(v.split()) <= 75 for v in d.values()), d
    gold_pos = collections.Counter(r["options"].index(r["gold"]) for r in rows)
    assert max(gold_pos.values()) / len(rows) <= 0.5, gold_pos
    gold_txt = collections.Counter(r["gold"] for r in rows)
    assert max(gold_txt.values()) / len(rows) <= 0.5, gold_txt.most_common(3)
    return True


def write_outputs(key, rows, defs_by_qid):
    """defs_by_qid: {qid: {option: definition}} (one per row)."""
    check_rows(key, rows, defs_by_qid)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    DEFS_DIR.mkdir(parents=True, exist_ok=True)
    for old in DEFS_DIR.glob(f"{key}__*.json"):  # stale per-row defs from an earlier run
        old.unlink()
    out = RAW_DIR / f"{key}.jsonl"
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    used = {r["meta"]["defs"] for r in rows}
    for qid, d in defs_by_qid.items():
        if qid not in used:
            continue
        with open(DEFS_DIR / f"{key}__{qid}.json", "w") as f:
            json.dump(d, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return out


def summary(key, rows):
    edges = collections.Counter(r["meta"].get("edge") for r in rows)
    nopt = collections.Counter(len(r["options"]) for r in rows)
    pos = collections.Counter("ABCDEFGH"[r["options"].index(r["gold"])] for r in rows)
    lens = sorted(len(r["state"]) for r in rows)
    top = collections.Counter(r["gold"] for r in rows).most_common(3)
    print(f"[{key}] rows={len(rows)} options per row={dict(sorted(nopt.items()))}")
    print(f"  gold position: {dict(sorted(pos.items()))}  most common gold texts: {top}")
    print(f"  edge tags: {dict(edges.most_common())}")
    print(f"  state chars: min={lens[0]} median={lens[len(lens) // 2]} max={lens[-1]}")
    return {"edges": edges, "pos": pos}


def show_samples(rows, defs_by_qid, n=5, seed=7):
    rng = random.Random(seed)
    for r in rng.sample(rows, min(n, len(rows))):
        print("-" * 100)
        print("RID:", r["rid"], "| edge:", r["meta"].get("edge"), "| orig:", r["meta"].get("orig_label"))
        print("STATE:\n" + r["state"])
        print("Q:", r["instructions"])
        for o in r["options"]:
            print(("  * " if o == r["gold"] else "    ") + o + "  ||  " + defs_by_qid[r["meta"]["defs"]][o])


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
