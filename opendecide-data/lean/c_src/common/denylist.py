#!/usr/bin/env python3
"""Deny-list program for model C (C_DATA_SPEC.md v4, section 3.H; methods B1, rules B4 and S1). CPU only, stdlib only.

One program builds the deny-list (default `data/c_parts/denylist.json`) and checks dataset names against it.

Inputs (3.H.1):
  - every entry of every `golden_src/*/rejected.json`. Two formats: a top-level list of {dataset, reason}, or a dict
    whose `rejected` key holds that list. Any other format fails the run, so a new format cannot be skipped silently;
  - the "avoid" and OHS-3-source entries of `ohs3/used_sources.json`. Only this program reads that file, in its own
    process. Nothing from it is printed or stored in clear: its names are kept only as keyed hashes (key derived from
    the file bytes, so the hashes cannot be brute-forced without the file), and a match is reported as 'ohs3-avoid'
    with no further detail. The program prints only hit / no-hit per checked name and entry counts;
  - `golden_src/forbidden_label_nli.json` (152 tasks), the OHS-1/2/3 source list of `golden_src/GOLDEN_SPEC.md`;
  - the dev and eval source names: only the top-level `source` field of an explicit file list (gate_dev's 9 dev
    splits and the eval files). No other field is kept and no key starting with 'jev' is ever materialised (7.4);
  - the Decision Index benchmark names (`bench/decision_index/sample_manifest_sample10k.json`, `benchmarks[].dataset`;
    nothing else under bench/ is read);
  - the 3.G table of `c_spec/C_DATA_SPEC.md`;
  - `c_src/common/deny_aliases.json`: aliases and the reason class of every entry, written from the rejected.json and
    3.G texts only (3.H.1 Matching). Every rejected.json entry, 3.G row, forbidden task and OHS item must be covered
    there; an uncovered one gets auto-derived aliases and class `taint` (reason unclear) and a warning (--strict: fail);
  - the 7.4 Jev-output path globs and the never-open list, checked against input PATHS (`paths`, `check_path`).

Matching. Case, punctuation and version suffixes are normalised (identifier fields are also tried without a trailing
version). An alias hits when its compact form equals a contiguous token span of a checked string. Aliases marked
'name:' (and every alias of <= 4 characters or a generic word) are matched only in identifier fields (names, domains,
parents), never inside free-text dataset descriptions. Dev and eval source names use gate_dev.py's name rule (equal,
or one extends the other by a '_' part). Hashed parts (OHS-3, sealed): a checked string is tested against the hashed
keys directly, and every clear entry it hits also has ALL its curated aliases tested against the hashed keys, so two
spellings of one dataset (clinc150 / clinc_oos) cannot miss each other; such a hit is reported under the same label.

Platform words (PREREG_FINAL.md amendment A16, ruling a). A bare platform or text-source word (Wikipedia, Reddit,
GitHub, arXiv, Zenodo, PubMed, ...) never matches on its own: it is never a derived alias of a hashed entry (OHS-3,
sealed) or of an auto-derived fallback, and it is not matched in any other way. Real text overlap is caught by the
counts-only n-gram decontamination against OHS-1/2/3, the sealed exports, Decision Index test items and JevBench items,
run before every freeze (C_DATA_SPEC 7). Every build still counts the selected OHS-3 entries that had such a word left
out (count only, a disclosure) and writes that count into denylist.json, DENY_CLASSES.md and every verdict header.
Curated aliases are not derived: Stack Exchange stays an alias of its own OHS entry (its text is the denied source).

OHS-3 selection (A16 ruling c: 'locked' counts as 'avoid'): entries marked 'avoid' or 'locked' or marked as an OHS-3
source. It is a fixed choice (SELECTIONS: avoid_or_locked, avoid_only), never a free pattern, and it changes only
through a PREREG amendment (Python API `build(selection=...)`; there is no CLI flag).

Classes (one per entry, from its recorded reason; unclear -> taint). `taint`: denies the dataset as new data, denies
every dataset built on it (declared parents, checked recursively) and drops its replay rows. `no_new_rows`: denies new
rows from that dataset only; children pass and replay rows are kept. A16 ruling b: an entry rejected ONLY for label
quality (silver, distant or automatic labels, or noisy gold) is `no_new_rows`, category `label_quality` (T-REx, so
MuSiQue passes); the program checks the recorded reason of every `label_quality` entry and fails the build if it also
names a taint reason (licence, OHS, forbidden task, test/dev/eval split, DI, LLM or synthetic text, Jev, sealed).
Scope `split`: only the test/dev/eval items are tainted (replay rows from the train split are kept); scope `part`: one
subset, half or split, dropped by a program check. Replay exception (3.H.3): a replay source that dev uses as a seen
source by design (gate_dev name rule) is kept when that is its only taint reason; test-split, OHS, licence and Jev
reasons always drop.

Usage (from lean/):
  ../.venv/bin/python c_src/common/denylist.py build   [--denylist OUT]
  ../.venv/bin/python c_src/common/denylist.py replay  [--query c_build/replay_denylist_query.json]
                                                       [--out c_build/replay_denylist_verdicts.json]
  ../.venv/bin/python c_src/common/denylist.py check   --query QUERY.json --out OUT [--fail-on-taint]
                                     (exit 3: a taint verdict)
  ../.venv/bin/python c_src/common/denylist.py classes --out c_src/common/DENY_CLASSES.md
  ../.venv/bin/python c_src/common/denylist.py paths   PATH [PATH ...]
The replay defaults are the paths c_build/replay_sample.py reads (RUNBOOK_replay_reads.md 3.2). The CLI always reads
ohs3/used_sources.json with the fixed selection; tests use the Python API (`build(used_sources=fixture)`), and every
output header says whether it is `canonical` (consumers refuse a non-canonical verdict file).

Query files. Replay: {"sources": {src: {"names": [...], "datasets": [...], "domains": [...]}}} (written by
c_build/replay_sample.py). New data (public, commit, packs, builder manifests): {"datasets": {key: {"names": [...],
"datasets": [...], "domains": [...], "parents": [name | {"name"/"names", "datasets", "parents"}], "emits_rows": true}},
"parents_registry": {name: {"names": [...], "parents": [...]}}}. A dataset with no `parents` field fails (G1).
There is no override flag: a denied dataset comes back only through a PREREG amendment.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import hmac
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent            # lean/c_src/common
LEAN = HERE.parents[1]                            # opendecide-data/lean
ROOT = LEAN.parents[1]                            # jev/ (repo root of the 7.4 path list)
VERSION = "1.2"

GOLDEN_SRC = LEAN / "golden_src"
FORBIDDEN = GOLDEN_SRC / "forbidden_label_nli.json"
GOLDEN_SPEC = GOLDEN_SRC / "GOLDEN_SPEC.md"
C_SPEC = LEAN / "c_spec" / "C_DATA_SPEC.md"
USED_SOURCES = LEAN / "ohs3" / "used_sources.json"
ALIASES = HERE / "deny_aliases.json"
DI_MANIFEST = ROOT / "bench" / "decision_index" / "sample_manifest_sample10k.json"
DEV_SPLITS = ("dev_nc", "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims", "pg_dev", "devzs", "devp_card", "dev")
EVAL_FILES = ("eval", "eval_card", "eval_hc", "eval_long", "eval_multi", "eval_opi", "eval_redef", "eval_jagged")
DEFAULT_DENYLIST = LEAN / "data" / "c_parts" / "denylist.json"
REPLAY_QUERY = LEAN / "c_build" / "replay_denylist_query.json"        # written by c_build/replay_sample.py
REPLAY_VERDICTS = LEAN / "c_build" / "replay_denylist_verdicts.json"  # read by c_build/replay_sample.py
LOG = LEAN / "c_build" / "progress_tools.log"

TAINT_CATS = {"licence", "ohs_source", "ohs3_avoid", "forbidden_task", "di_test", "test_split", "dev_eval",
              "llm_written", "non_human_labels", "gold_noise", "derived", "sealed", "jev", "unclear"}
NNR_CATS = {"already_used", "extra_rows", "duplicate_taxonomy", "other_subset_used", "low_value", "too_few_options",
            "overlap_own_sets", "label_quality"}
# A16 ruling b: a label_quality entry's recorded reason may name no taint reason. Marker classes (names only are ever
# printed, never the reason text); a hit fails the build, so a mixed reason can never become no_new_rows silently.
LQ_TAINT_MARKERS = {
    "licence": r"licen[cs]|non-?commercial|\bNC\b|research[- ]only|\bterms\b|copyright|agreement|\bAFL\b",
    "ohs": r"\bOHS|used_sources|\bavoid|\blocked\b",
    "forbidden_task": r"forbidden|label[- ]nli",
    "test_eval_split": r"\btest\b|hidden|held[- ]out|\beval\b|evaluation|benchmark",
    "dev": r"\bdev\b",
    "decision_index": r"Decision Index|\bDI\b",
    "llm_text_or_labels": r"\bLLM|GPT|model[- ](?:written|generated|assisted)|machine[- ]generated|generated by",
    "synthetic_text": r"machine[- ]translat|\btranslated\b|simulat|synthetic|templat",
    "jev_sealed": r"\bJev|sealed",
}
CLS = {"t": "taint", "n": "no_new_rows"}
OHS3_LABEL = "ohs3-avoid"
SEALED_LABEL = "sealed-block"
SPLIT_VALUES = ["test", "validation", "valid", "dev", "eval"]
PLATFORM_RULE = ("RULED (PREREG_FINAL.md A16 a): a bare platform word (Wikipedia, Reddit, GitHub, arXiv, Zenodo, PubMed, "
                 "...) never matches on its own; real text overlap is caught by the counts-only n-gram decontamination "
                 "before every freeze")
SELECTION_RULE = "RULED (PREREG_FINAL.md A16 c): 'locked' counts as 'avoid'"
LABEL_QUALITY_RULE = ("RULED (PREREG_FINAL.md A16 b): an entry rejected only for label quality (silver or noisy labels) "
                      "is no_new_rows (category label_quality); contamination, licence, forbidden-task, dev and eval "
                      "entries stay taint")

# compact forms that are ordinary words: such aliases are matched only in identifier fields, never in descriptions
GENERIC = {
    "emotion", "hate", "irony", "climate", "spam", "star", "bright", "vast", "flute", "ethos", "ethics", "circa",
    "parade", "ambient", "discovery", "subjectivity", "fever", "copa", "race", "sick", "cola", "gum", "stac",
    "emergent", "verifiability", "oasis", "meld", "dream", "massive", "casino", "help", "control", "frames", "true",
    "quality", "drop", "beetle", "ellipse", "rebel", "acid", "nectar", "reveal", "frank", "mocha", "jester", "epic",
    "adept", "unfun", "complex", "offensive", "sentiment", "nursery", "zenodo", "github", "huggingface", "kaggle",
    "osf", "arxiv", "wikipedia", "wikidata", "reddit", "twitter", "gab", "news", "reviews", "dataset", "corpus",
    "data", "creak", "folio", "silicone", "hover", "swag", "imdb", "trec", "liar", "scone", "jigsaw", "yahoo", "yelp",
    "olid", "tasksource", "bless", "medical", "legal", "finance", "commits", "github repositories",
}
# platform / text-source words: never an alias on their own in derived (used_sources, sealed, fallback) aliases
PLATFORM = {"wikipedia", "wikidata", "wiki", "wikinews", "wikimedia", "reddit", "twitter", "tweets", "github", "gitlab",
            "gab", "arxiv", "zenodo", "huggingface", "hf", "kaggle", "osf", "pubmed", "pmc", "news", "web", "commoncrawl",
            "books", "movies", "reviews", "stackexchange"}
# never an alias (words that only describe a role or a split)
STOP = {"train", "test", "dev", "eval", "data", "dataset", "datasets", "default", "all", "main", "en", "english",
        "avoid", "locked", "ohs3", "ohs", "note", "notes", "yes", "no", "none", "true", "false", "other", "misc"}

NEVER_OPEN = [re.compile(p, re.I) for p in (
    r"(^|/)lean/ohs3(/|$)", r"(^|/)lean/data/[^/]*ohs3", r"(^|/)ohs3_parts(/|$)", r"(^|/)lean/prep89(/|$)",
    r"(^|/)lean/preds_ohs", r"(^|/)c_spec/sealed_brief(/|$)", r"(^|/)lean/sealed_nd(/|$)",
    r"(^|/)bench/external_quarantine(/|$)", r"(^|/)bench/longbench_v2(/|$)",
    r"(^|/)c_spec/RESEARCH_licensed-data\.md$", r"(^|/)c_spec/REVIEW_[^/]*\.md$",
    r"(^|/)c_spec/LICENCE_CHECK_[^/]*\.md$", r"(^|/)c_spec/ADDENDUM_research\.md$",
    r"(^|/)c_spec/RESEARCH_EXTRA_[^/]*\.md$", r"(^|/)\.claude/projects(/|$)", r"^/private/tmp/claude-501(/|$)",
    r"^/tmp/claude-501(/|$)")]
JEV_74 = [re.compile(p, re.I) for p in (                         # C_DATA_SPEC.md 7.4 table
    r"(^|/)lean/preds[^/]*/jev", r"(^|/)lean/preds_ohs3", r"(^|/)lean/logs/jev_[^/]*\.log$",
    r"(^|/)lean/prep89(/|$)", r"(^|/)bench/runs/jev_", r"(^|/)bench/jevbench(_v154)?/results(/|$)",
    r"(^|/)bench/jagged/data(/|$)", r"(^|/)bench/external_quarantine(/|$)", r"(^|/)bench/ejs5/runs(/|$)",
    r"(^|/)bench/ejs5/tests/_work(/|$)", r"(^|/)reports/pdf_build_30sep/v154_variants/jev_",
    r"(^|/)reports/OpenDecide_v05_vs_Jev\.md$", r"(^|/)lean/sealed_nd/jev_")]
JEV_NAME = re.compile(r"(^|[_/.-])jev", re.I)                   # 7.4 program rule (file or directory names)
JEVBENCH_ITEMS = re.compile(r"(^|/)bench/(splits/jevbench_[^/]*\.jsonl|v154/[^/]*\.jsonl)$", re.I)
# OHS-3 selection: a fixed choice, never a free pattern (3.H.2: no override flag). Changed only by a PREREG amendment.
SELECTIONS = {"avoid_or_locked": re.compile(r"\bavoid|\blocked\b", re.I),     # rejected.json: 'locked' = 'avoid'
              "avoid_only": re.compile(r"\bavoid", re.I)}
DEFAULT_SELECTION = "avoid_or_locked"
AVOID_RE = SELECTIONS[DEFAULT_SELECTION]
OHS3_RE = re.compile(r"\bohs[-_ ]?3\b", re.I)
NAME_KEYS = ("name", "names", "dataset", "datasets", "id", "ids", "hf_id", "hf", "hf_name", "hub_id", "repo", "repos",
             "source", "sources", "key", "keys", "alias", "aliases", "title", "url", "urls")
CANARIES = ("SNLI", "HANS", "NaN-NLI", "WANLI", "Measuring Hate Speech", "HWU64", "benayas/snips")  # rejected.json says 'avoid'


class DenyError(SystemExit):
    pass


def log(msg):
    line = f"{datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} [denylist] {msg}"
    print(line)
    try:
        with open(LOG, "a") as f:
            f.write(line + "\n")
    except OSError:
        pass


# ------------------------------------------------------------------ paths (7.4 and the never-open list)

def _rel(p):
    a = Path(p).resolve()
    try:
        r = a.relative_to(ROOT).as_posix()
    except ValueError:
        return a.as_posix()
    return re.sub(r"^opendecide-data/lean(/|$)", r"lean\1", r)


def check_path(p, allow_jevbench_items=False):
    """None when the path may be read; otherwise the reason (never-open list, 7.4 Jev outputs, /jev/ name rule)."""
    r = _rel(p)
    for rx in NEVER_OPEN:
        if rx.search(r) or rx.search(Path(p).resolve().as_posix()):
            return f"never-open list ({rx.pattern})"
    for rx in JEV_74:
        if rx.search(r):
            return f"7.4 Jev output ({rx.pattern})"
    if JEV_NAME.search(r) and not (allow_jevbench_items and JEVBENCH_ITEMS.search(r)):
        return "7.4 program rule: a file or directory name matches /(^|[_/.-])jev/i"
    return None


def safe_open(p, mode="r"):
    why = check_path(p)
    if why:
        raise DenyError(f"refused: {p}: {why}")
    return open(p, mode)


def strip_jev_keys(pairs):
    """json object_pairs_hook: no key starting with 'jev' is ever materialised (7.4 field rule)."""
    return {k: v for k, v in pairs if not str(k).lower().startswith("jev")}


def sha256_file(p):
    h = hashlib.sha256()
    with safe_open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ------------------------------------------------------------------ normaliser

_TOK = re.compile(r"[0-9]+(?:\.[0-9]+)+|[a-z0-9]+")     # dotted versions stay one token; letters+digits stay joined


def tokens(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    s = s.replace("++", "pp").replace("+", " plus ").replace("&", " and ")
    return _TOK.findall(s)


def _is_version(t):
    """A version token: v2, v1.2, 2.0, or a 1-2 digit number (years such as 2003 and ids such as 150 are kept)."""
    return bool(re.fullmatch(r"v[0-9]+(?:\.[0-9]+)*|[0-9]+\.[0-9]+(?:\.[0-9]+)*|[0-9]{1,2}", t))


def strip_version(toks):
    t = list(toks)
    while len(t) > 1 and _is_version(t[-1]):
        t.pop()
        if len(t) > 1 and t[-1] in ("v", "ver", "version", "release"):
            t.pop()
    return t


def compact(s):
    return "".join(tokens(s))


def norm_key(s):
    return "_".join(strip_version(tokens(s)))


def compile_alias(a):
    """'name:x' -> identifier-only; 'span:x' -> description matching forced; plain -> span unless short or generic."""
    mode = "span"
    if a.startswith("name:"):
        mode, a = "name", a[5:]
    elif a.startswith("span:"):
        mode, a = "span!", a[5:]
    t = tokens(a)
    if not t:
        return None
    c = "".join(t)
    if mode == "span" and (len(c) <= 4 or c in GENERIC):
        mode = "name"
    return ("span" if mode == "span!" else mode), c, a, len(t)


def spans(toks, maxlen):
    for i in range(len(toks)):
        acc = ""
        for j in range(i, min(i + maxlen, len(toks))):
            acc += toks[j]
            yield acc


def dev_rule(k, a):
    """gate_dev.source_seen: equal, or one extends the other by a '_' part."""
    return k == a or k.startswith(a + "_") or k.endswith("_" + a) or a.startswith(k + "_")


def _identifier_like(p):
    """A dataset-name-looking piece: an id or acronym (no spaces, with '/', '_', '-', a digit or an inner capital), or
    a multi-word name. Descriptive fragments inside parentheses are not aliases."""
    p = p.strip()
    if not p:
        return False
    if " " in p:
        return len(tokens(p)) >= 2
    return bool(re.search(r"[/_\-0-9]", p) or re.search(r".[A-Z]", p))


def derive_aliases(s, suppressed=None):
    """Generic alias derivation from a free-text name (auto-derived fallbacks, the used_sources part and the sealed
    block-list): the full name, the part before a parenthesis, identifier-like list items, the last segment of an id
    or URL. A bare platform or text-source word (Wikipedia, Reddit, GitHub, arXiv, Zenodo, PubMed, ...) is never an
    alias on its own: it names where text is hosted, not a dataset (A16 ruling a; the spec reads 'Zenodo' this way,
    decision 7). When `suppressed` is a list, every alias left out only because it is a platform word is appended to
    it (counted for disclosure; never matched)."""
    s = str(s).strip()
    out = {s}
    base = re.split(r"\s*[\(\[]", s)[0]
    out.add(base)
    for piece in re.split(r"\s+/\s+|,\s+|;\s+", base):
        if _identifier_like(piece):
            out.add(piece)
    for inner in re.findall(r"[\(\[]([^\)\]]*)[\)\]]", s):
        for piece in re.split(r"[,;]", inner):
            if _identifier_like(piece) and " " not in piece.strip():
                out.add(piece)
    for x in list(out):
        x = x.strip()
        if "://" in x:
            segs = [g for g in x.split("://", 1)[1].split("/") if g]
            if len(segs) >= 2:
                out.add("/".join(segs[-2:]))
                out.add(segs[-1])
        elif "/" in x and x.count("/") <= 2 and " " not in x:
            out.add(x.split("/")[-1])
    res = []
    for x in out:
        x = x.strip(" .:-")
        c = compact(x)
        if c and c not in STOP and len(c) >= 3:
            if c not in PLATFORM:
                res.append(x)
            elif suppressed is not None:
                suppressed.append(x)
    return sorted(set(res))


# ------------------------------------------------------------------ inputs

def load_rejected():
    """[(family, index, dataset, reason)] over every golden_src/*/rejected.json; fails on an unknown format."""
    out = []
    files = sorted(GOLDEN_SRC.glob("*/rejected.json"))
    if not files:
        raise DenyError("no golden_src/*/rejected.json found")
    for f in files:
        d = json.load(safe_open(f))
        if isinstance(d, list):
            items = d
        elif isinstance(d, dict) and isinstance(d.get("rejected"), list):
            items = d["rejected"]
        else:
            raise DenyError(f"{f}: neither a list of {{dataset, reason}} nor a dict with a 'rejected' list")
        for i, e in enumerate(items):
            if not isinstance(e, dict) or "dataset" not in e or "reason" not in e:
                raise DenyError(f"{f}: entry {i} is not a {{dataset, reason}} object")
            out.append((f.parent.name, i, str(e["dataset"]), str(e["reason"])))
    return out, files


def load_3g():
    t = safe_open(C_SPEC).read()
    s = t.index("### 3.G Excluded")
    e = t.index("### 3.H", s)
    rows = [l for l in t[s:e].splitlines() if l.startswith("|")][2:]
    out = []
    for l in rows:
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) < 2:
            raise DenyError(f"3.G row not understood: {l[:80]}")
        out.append((c[0], c[1]))
    if not out:
        raise DenyError("3.G table is empty")
    return out


def load_ohs_list():
    g = safe_open(GOLDEN_SPEC).read()
    m = re.search(r"\*\*OHS sources \(forbidden\):\*\*(.*?)\n\s*- ", g, re.S)
    if not m:
        raise DenyError("GOLDEN_SPEC.md: OHS source list not found")
    txt = " ".join(m.group(1).split()).rstrip(".")
    items, depth, cur = [], 0, ""
    for ch in txt:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            items.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        items.append(cur.strip())
    return items


def load_dev_eval():
    """{source: set(origins)} from the `source` field only of an explicit dev/eval file list."""
    dev, ev = defaultdict(set), defaultdict(set)
    files = []
    for group, names in (("dev", DEV_SPLITS), ("eval", EVAL_FILES)):
        for n in names:
            p = LEAN / "data" / f"{n}.jsonl"
            if not p.exists():
                log(f"WARNING: {group} file data/{n}.jsonl missing (skipped)")
                continue
            files.append(p)
            with safe_open(p) as f:
                for line in f:
                    if line.strip():
                        s = json.loads(line, object_pairs_hook=strip_jev_keys).get("source")
                        if s:
                            (dev if group == "dev" else ev)[str(s)].add(n)
    return dev, ev, files


def load_di():
    d = json.load(safe_open(DI_MANIFEST))
    names = [b["dataset"] for b in d.get("benchmarks", []) if isinstance(b, dict) and b.get("dataset")]
    if not names:
        raise DenyError("Decision Index manifest: no benchmarks[].dataset")
    return names


def _walk_pairs(x, key=None):
    if isinstance(x, dict):
        for k, v in x.items():
            yield k, v
            yield from _walk_pairs(v, k)
    elif isinstance(x, list):
        for v in x:
            yield from _walk_pairs(v, key)
    else:
        yield key, x


def _strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, list):
        for v in x:
            yield from _strings(v)
    elif isinstance(x, dict):
        for v in x.values():
            yield from _strings(v)


def _hkey(raw, salt):
    return hashlib.sha256(salt + raw).digest()


def _h(key, mode, c):
    return hmac.new(key, f"{mode}:{c}".encode(), hashlib.sha256).hexdigest()[:32]


def _hash_names(names, key, keys):
    """Adds the hashed aliases of one entry's names to keys. Returns (number of aliases, number of platform-word aliases
    left out: A16 a, counted only, never hashed or matched). Nothing in clear leaves this function."""
    sup = []
    al = [a for s in names for a in derive_aliases(s, sup)]
    for a in al:
        ca = compile_alias(a)
        if ca:
            keys[ca[0]].add(_h(key, ca[0], ca[1]))
    return len(al), len(sup)


def read_used_sources(path=USED_SOURCES, name_keys=NAME_KEYS, selection=DEFAULT_SELECTION):
    """In-process only. Returns (raw sha256, key, {'span': set, 'name': set}, counts). Never returns names.
    `selection` is one of the fixed SELECTIONS (no free pattern: 3.H.2)."""
    if selection not in SELECTIONS:
        raise DenyError(f"selection {selection!r}: not one of {sorted(SELECTIONS)} (3.H.2: no free pattern)")
    avoid_re = SELECTIONS[selection]
    p = Path(path)
    if not p.exists():
        raise DenyError(f"{_rel(p)} missing: the OHS-3 part of 3.H cannot be checked")
    raw = p.read_bytes()                       # the one sanctioned read of this file (3.H.1)
    doc = json.loads(raw)
    if not isinstance(doc, dict) or not isinstance(doc.get("datasets"), list):
        raise DenyError(f"{_rel(p)}: format not understood (no top-level 'datasets' list)")
    key = _hkey(raw, b"denylist-ohs3-v1:")
    keys = {"span": set(), "name": set()}
    n_sel = n_noname = n_bad = n_plat = n_plat_only = 0
    for e in doc["datasets"]:
        if isinstance(e, str):
            flags = [e]
            names = [avoid_re.sub(" ", OHS3_RE.sub(" ", e))]
        elif isinstance(e, dict):
            pairs = list(_walk_pairs(e))
            flags = [str(k) for k, v in pairs if k is not None and v] + [v for _, v in pairs if isinstance(v, str)]
            names = [s for k in name_keys if k in e for s in _strings(e[k])]
        else:
            n_bad += 1
            continue
        sel = any(avoid_re.search(s) or OHS3_RE.search(s) for s in flags)
        if not sel:
            continue
        n_sel += 1
        n_al, n_sup = _hash_names(names, key, keys)
        n_plat += bool(n_sup)
        if not n_al:
            n_noname += 1
            n_plat_only += bool(n_sup)
    counts = {"entries": len(doc["datasets"]), "selected": n_sel, "selected_without_name": n_noname,
              "selected_platform_alias_suppressed": n_plat, "selected_platform_alias_only": n_plat_only,
              "unparsed": n_bad, "alias_keys": len(keys["span"]) + len(keys["name"])}
    return hashlib.sha256(raw).hexdigest(), key, keys, counts


def read_blocklist(path):
    """Optional sealed block-list (a JSON list of names, or {'names': [...]}), hashed like the OHS-3 part (bare platform
    words are left out and counted: A16 a)."""
    p = Path(path)
    raw = p.read_bytes()
    doc = json.loads(raw)
    names = doc.get("names", []) if isinstance(doc, dict) else doc
    key = _hkey(raw, b"denylist-sealed-v1:")
    keys = {"span": set(), "name": set()}
    n_plat = 0
    for s in names:
        n_plat += bool(_hash_names([s], key, keys)[1])
    return hashlib.sha256(raw).hexdigest(), key, keys, {"entries": len(names), "platform_alias_suppressed": n_plat}


# ------------------------------------------------------------------ the deny-list

class DenyList:
    def __init__(self, entries, hashed, meta):
        self.entries = entries                  # list of dicts (clear entries only)
        self.hashed = hashed                    # {label: (key, {'span': set, 'name': set})}; every label denies
        self.meta = meta
        self.span, self.name, self.dev = defaultdict(list), defaultdict(list), []
        self.maxlen = 1
        for i, e in enumerate(entries):
            for mode, c, orig, n in e["_aliases"]:
                self.maxlen = max(self.maxlen, n)
                (self.span if mode == "span" else self.name)[c].append((i, orig))
            for k in e.get("_dev", ()):
                self.dev.append((k, i))
        self.maxlen = max(self.maxlen, 8)
        # clear entry -> hashed labels one of its curated aliases is in (alias equality, so both modes are tried).
        # Kept in memory only: never printed or stored (it would list which clear entries the hashed files hold).
        self.alias_hashed = defaultdict(list)
        for i, e in enumerate(entries):
            for label, (key, keys) in hashed.items():
                if any(_h(key, "span", c) in keys["span"] or _h(key, "name", c) in keys["name"]
                       for _, c, _, _ in e["_aliases"]):
                    self.alias_hashed[i].append(label)

    # --- matching
    def match(self, names=(), descs=(), domains=()):
        """[(entry index | label, field, alias, string)] for one item's own strings. A hashed label hits when a span
        of the string is one of its keys, or when the string hits a clear entry one of whose curated aliases is one
        of its keys (alias expansion: two spellings of one dataset never miss each other)."""
        hits = self._match(names, descs, domains)
        for i, field, _, s in [h for h in hits if not isinstance(h[0], str)]:
            for label in self.alias_hashed.get(i, ()):
                hits.append((label, field, None, s))
        return hits

    def _match(self, names=(), descs=(), domains=()):
        hits = []
        for field, strings, ident in (("name", names, True), ("dataset", descs, False), ("domain", domains, True)):
            for s in strings:
                if s is None or not str(s).strip():
                    continue
                t = tokens(s)
                variants = [t]
                if ident:
                    t2 = strip_version(t)
                    if t2 != t:
                        variants.append(t2)
                seen = set()
                for v in variants:
                    for c in spans(v, self.maxlen):
                        if c in seen:
                            continue
                        seen.add(c)
                        for i, a in self.span.get(c, ()):
                            hits.append((i, field, a, s))
                        if ident:
                            for i, a in self.name.get(c, ()):
                                hits.append((i, field, a, s))
                        for label, (key, keys) in self.hashed.items():
                            if _h(key, "span", c) in keys["span"] or (ident and _h(key, "name", c) in keys["name"]):
                                hits.append((label, field, None, s))
                    if field == "name":            # gate_dev's rule is a source-NAME rule (not domains)
                        k = "_".join(v)
                        for a, i in self.dev:
                            if dev_rule(k, a):
                                hits.append((i, field, "dev:" + a, s))
        return hits

    def resolve_hits(self, hits, via=()):
        out, seen = [], set()
        for i, field, alias, s in hits:
            if isinstance(i, str):
                k = (i, field, s, via)
                if k in seen:
                    continue
                seen.add(k)
                out.append({"label": i, "class": "taint", "field": field, "string": s, "via": via})
                continue
            e = self.entries[i]
            k = (e["id"], field, s, via)
            if k in seen:
                continue
            seen.add(k)
            out.append({"i": i, "id": e["id"], "entry": e["name"], "class": e["class"], "cat": e["cat"],
                        "scope": e["scope"], "origin": e["origin"], "field": field, "alias": alias, "string": s,
                        "via": via, "devname": bool(alias and alias.startswith("dev:"))})
        return out


def _entry(eid, name, cls, cat, aliases, origin, scope="dataset", note=None, dev=()):
    if cls not in ("taint", "no_new_rows"):
        raise DenyError(f"{eid}: class {cls!r}")
    if (cls == "taint") != (cat in TAINT_CATS) or (cls == "no_new_rows") != (cat in NNR_CATS):
        raise DenyError(f"{eid}: category {cat!r} does not belong to class {cls!r}")
    if scope not in ("dataset", "split", "part"):
        raise DenyError(f"{eid}: scope {scope!r}")
    comp = [x for x in (compile_alias(a) for a in aliases) if x]
    comp = sorted(set(comp))
    return {"id": eid, "name": name, "class": cls, "cat": cat, "scope": scope, "origin": origin,
            "aliases": [f"{m}:{orig}" for m, c, orig, n in comp] + [f"dev:{k}" for k in dev],
            "note": note, "_aliases": comp, "_dev": list(dev)}


def _sub(eid, sub, origin):
    name, cls, cat, aliases = sub[:4]
    opts = sub[4] if len(sub) > 4 else {}
    return _entry(eid, name, CLS[cls], cat, aliases, origin, opts.get("scope", "dataset"), opts.get("note"))


def lq_markers(reason):
    """A16 b guard: the taint-marker classes a recorded reason names (class names only; never the reason text)."""
    return sorted(k for k, rx in LQ_TAINT_MARKERS.items() if re.search(rx, reason, re.I))


def _check_label_quality(eid, cat, reason):
    if cat == "label_quality":
        m = lq_markers(reason)
        if m:
            raise DenyError(f"{eid}: curated label_quality (A16 b: no_new_rows), but its recorded reason also names "
                            f"taint marker(s) {m}; a mixed reason stays taint (fix deny_aliases.json)")


def build(used_sources=USED_SOURCES, with_ohs3=True, sealed=None, strict=False, selection=DEFAULT_SELECTION):
    """The deny-list. The CLI always calls this with the defaults (plus --sealed-blocklist / --strict); a build with
    another used_sources path or without the OHS-3 part (tests) is marked canonical: false in every output."""
    cur = json.load(safe_open(ALIASES))
    entries, warnings, inputs = [], [], {}
    # 1. rejected.json (both formats)
    rej, rej_files = load_rejected()
    for f in rej_files:
        inputs[_rel(f)] = sha256_file(f)
    for fam, i, ds, reason in rej:
        c = cur["rejected"].get(fam, {}).get(str(i))
        origin = f"rejected:{fam}#{i}"
        if c and " ".join(ds.split()).startswith(c["d"]):
            for j, sub in enumerate(c["e"]):
                _check_label_quality(f"rej:{fam}#{i}.{j}", sub[2], reason)
                entries.append(_sub(f"rej:{fam}#{i}.{j}", sub, origin))
        else:
            warnings.append(f"{origin}: not curated in deny_aliases.json (auto aliases, class taint: reason unclear)")
            entries.append(_entry(f"rej:{fam}#{i}.auto", ds[:120], "taint", "unclear", derive_aliases(ds), origin))
    # 2. 3.G table
    rows = load_3g()
    inputs[_rel(C_SPEC)] = sha256_file(C_SPEC)
    for r, (cell, reason) in enumerate(rows):
        c = cur["table_3G"].get(str(r))
        origin = f"3.G#{r}"
        if c and cell.startswith(c["d"]):
            for j, sub in enumerate(c["e"]):
                _check_label_quality(f"3G#{r}.{j}", sub[2], reason)
                entries.append(_sub(f"3G#{r}.{j}", sub, origin))
        else:
            warnings.append(f"{origin}: not curated (auto aliases, class taint)")
            entries.append(_entry(f"3G#{r}.auto", cell.replace("*", "")[:120], "taint", "unclear",
                                  derive_aliases(cell.replace("*", "")), origin))
    # 3. the 152 forbidden tasks (+ the aggregate itself)
    tasks = json.load(safe_open(FORBIDDEN))
    inputs[_rel(FORBIDDEN)] = sha256_file(FORBIDDEN)
    fb = cur["forbidden"]
    unknown = set(fb["extra"]) - set(tasks)
    if unknown:
        raise DenyError(f"deny_aliases.json forbidden.extra names unknown tasks: {sorted(unknown)}")
    for t in tasks:
        segs = t.split("/")
        al = [t] + list(fb["extra"].get(t, []))
        if len(segs) > 1:
            if segs[0] in fb["whole_prefix"]:
                al.append(segs[0])
            if segs[0] in fb["last_segment_ok"]:
                al.append("name:" + segs[-1])
        entries.append(_entry(f"forbidden:{t}", t, "taint", "forbidden_task", al, "forbidden_label_nli.json"))
    entries.append(_entry("forbidden:_aggregate", "tasksource/zero-shot-label-nli (aggregate)", "taint",
                          "forbidden_task", fb["aggregate"], "forbidden_label_nli.json"))
    # 4. OHS-1/2/3 source list
    ohs = load_ohs_list()
    inputs[_rel(GOLDEN_SPEC)] = sha256_file(GOLDEN_SPEC)
    for it in ohs:
        al = cur["ohs"].get(it)
        if al is None:
            warnings.append(f"OHS item {it!r}: not curated (auto aliases)")
            al = derive_aliases(it)
        entries.append(_entry(f"ohs:{it}", it, "taint", "ohs_source", al, "GOLDEN_SPEC.md OHS list"))
    # 5. dev and eval sources (names from the source field; gate_dev name rule) + curated aliases
    dev, ev, de_files = load_dev_eval()
    for f in de_files:
        inputs[_rel(f)] = sha256_file(f)
    dv = cur["dev_eval"]
    for s in sorted(dev):
        nm = re.sub(r"^redef:", "", s)
        entries.append(_entry(f"dev:{s}", f"dev source {s} ({', '.join(sorted(dev[s]))})", "taint", "dev_eval",
                              dv["dev"].get(nm, []), "dev splits", dev=[norm_key(nm)]))
    for s in sorted(ev):
        if s.startswith("redef:"):           # redefined dev sources: dev semantics (seen by design)
            nm = s[6:]
            entries.append(_entry(f"dev:{s}", f"dev source {nm} (eval_redef)", "taint", "dev_eval", [],
                                  "dev splits", dev=[norm_key(nm)]))
            continue
        files = sorted(ev[s])
        if files == ["eval_jagged"]:
            entries.append(_entry(f"eval:{s}", f"JevBench jagged source {s}", "taint", "jev",
                                  dv["eval"].get(s, []), "eval files", dev=[norm_key(s)]))
        else:
            entries.append(_entry(f"eval:{s}", f"eval source {s} ({', '.join(files)})", "taint", "dev_eval",
                                  dv["eval"].get(s, []), "eval files", scope="split", dev=[norm_key(s)]))
    for nm, kind in dv["also_forbidden_line"]:     # GOLDEN_SPEC rule 1 'Also forbidden' (dev / eval / JevBench)
        eid, name = f"golden_spec:{nm}", f"{nm} (GOLDEN_SPEC 'also forbidden')"
        if kind == "jev":
            entries.append(_entry(eid, name, "taint", "jev", ["jevbench", "jev bench"], "GOLDEN_SPEC.md"))
        elif kind == "eval":                       # CLINC150 and Banking77 TEST splits: split scope
            entries.append(_entry(eid, name, "taint", "dev_eval", ["clinc150", "clinc oos", "banking77"],
                                  "GOLDEN_SPEC.md", scope="split"))
        else:                                      # dev sources: the gate_dev name rule (seen-source exception)
            key = "btzsc" if nm.startswith("BTZSC") else norm_key(nm)
            entries.append(_entry(eid, name, "taint", "dev_eval", dv["dev"].get(nm, []), "dev splits", dev=[key]))
    # 6. Decision Index benchmarks
    di = load_di()
    inputs[_rel(DI_MANIFEST)] = sha256_file(DI_MANIFEST)
    for nm in di:
        c = cur["di"].get(nm)
        if c is None:
            warnings.append(f"DI benchmark {nm!r}: not curated (auto aliases, scope split)")
            c = {"a": derive_aliases(nm), "scope": "split"}
        entries.append(_entry(f"di:{nm}", f"Decision Index test: {nm}", "taint", "di_test", c["a"] + [nm],
                              "DI sample manifest", scope=c["scope"]))
    for nm, c in cur["di"].get("_extra", {}).items():
        entries.append(_entry(f"di:{nm}", f"Decision Index test: {nm}", "taint", "di_test", c["a"],
                              "LICENCE_REGISTER / 3.G", scope=c["scope"]))
    # 7. spec extras
    for j, sub in enumerate(cur["extra"]):
        if sub[2] == "label_quality":
            raise DenyError(f"extra:{j}: label_quality needs a recorded reason (rejected.json or 3.G)")
        entries.append(_sub(f"extra:{j}", sub, "C_DATA_SPEC (7.1, 7.4, 9)"))
    inputs[_rel(ALIASES)] = sha256_file(ALIASES)
    # 8. the hashed parts
    hashed, meta = {}, {"warnings": warnings, "inputs": inputs,
                        "rulings": {"platform_words": PLATFORM_RULE, "selection": SELECTION_RULE,
                                    "label_quality": LABEL_QUALITY_RULE}}
    canonical = bool(with_ohs3) and Path(used_sources).resolve() == USED_SOURCES.resolve() \
        and selection == DEFAULT_SELECTION
    meta["canonical"] = canonical
    if with_ohs3:
        sha, key, keys, cnt = read_used_sources(used_sources, selection=selection)
        hashed[OHS3_LABEL] = (key, keys)
        meta["ohs3"] = {"path": _rel(used_sources), "sha256": sha, **cnt, "selection": selection,
                        "selection_pattern": SELECTIONS[selection].pattern, "platform_rule": PLATFORM_RULE,
                        "keys": {m: sorted(v) for m, v in keys.items()}}
    else:
        meta["ohs3"] = None
    if sealed:
        sha, key, keys, cnt = read_blocklist(sealed)
        hashed[SEALED_LABEL] = (key, keys)
        meta["sealed"] = {"path": _rel(sealed), "sha256": sha, **cnt, "keys": {m: sorted(v) for m, v in keys.items()}}
    else:
        meta["sealed"] = None
    dl = DenyList(entries, hashed, meta)
    if with_ohs3:
        res = []
        for c in CANARIES:
            res.append((c, any(isinstance(i, str) and i == OHS3_LABEL for i, *_ in dl.match(names=[c]))))
        meta["ohs3"]["canaries"] = {c: ("hit" if h else "no-hit") for c, h in res}
        if meta["ohs3"]["selected_without_name"]:
            raise DenyError(f"used_sources: {meta['ohs3']['selected_without_name']} selected entries yield no name "
                            f"({meta['ohs3']['selected_platform_alias_only']} of them only a bare platform word; the "
                            "rest: entry name keys not understood); nothing printed")
        if not any(h for _, h in res):
            raise DenyError("used_sources: 0 of the rejected.json 'avoid' canaries hit; format not understood")
    if strict and warnings:
        raise DenyError("strict: " + "; ".join(warnings))
    return dl


def provisional(dl):
    """Why outputs of this build must not be relied on yet (empty list = none)."""
    out = []
    if not dl.meta["canonical"]:
        out.append("non-canonical build (tests or a fixture: OHS-3 part missing, another used_sources file or another "
                   "selection); consumers refuse it")
    return out


def notes(dl):
    """Disclosures that do not make the outputs provisional."""
    out = []
    if not dl.meta["sealed"]:
        out.append("sealed block-list not supplied (--sealed-blocklist): sealed-suite text overlap is caught by the "
                   "counts-only n-gram decontamination against the sealed exports before every freeze (A16 a)")
    return out


def denylist_doc(dl):
    ents = [{k: v for k, v in e.items() if not k.startswith("_")} for e in dl.entries]
    by = Counter((e["origin"].split(":")[0].split("#")[0], e["class"]) for e in dl.entries)
    return {"program": "c_src/common/denylist.py", "version": VERSION, "spec": "C_DATA_SPEC.md v4 3.H",
            "canonical": dl.meta["canonical"], "inputs": dl.meta["inputs"], "ohs3": dl.meta["ohs3"],
            "sealed": dl.meta["sealed"], "rulings": dl.meta["rulings"], "provisional": provisional(dl),
            "notes": notes(dl),
            "counts": {"entries": len(ents), "taint": sum(e["class"] == "taint" for e in ents),
                       "no_new_rows": sum(e["class"] == "no_new_rows" for e in ents),
                       "by_origin_class": {f"{o}|{c}": n for (o, c), n in sorted(by.items())}},
            "warnings": dl.meta["warnings"], "entries": ents}


def write_json(p, doc):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    s = json.dumps(doc, indent=1, sort_keys=False)
    p.write_text(s + "\n")
    return hashlib.sha256((s + "\n").encode()).hexdigest()


# ------------------------------------------------------------------ checks

def _item_strings(item):
    names = list(item.get("names") or [])
    if item.get("name"):
        names.insert(0, item["name"])
    return names, list(item.get("datasets") or []), list(item.get("domains") or [])


def check_item(dl, item, registry=None, via=(), seen=None, depth=0):
    """All hits of one item and, recursively, of its declared parents (each hit carries its parent chain)."""
    registry = registry or {}
    reg = {norm_key(k): v for k, v in registry.items()}
    seen = set() if seen is None else seen
    names, descs, doms = _item_strings(item)
    hits = dl.resolve_hits(dl.match(names, descs, doms), via)
    if depth > 12:
        return hits
    for p in item.get("parents") or []:
        pitem = {"names": [p]} if isinstance(p, str) else dict(p)
        pname = (_item_strings(pitem)[0] or ["?"])[0]
        k = norm_key(pname)
        if k in seen:
            continue
        if isinstance(p, str) and k in reg:
            pitem = {"names": [p] + list(reg[k].get("names", [])), **{x: y for x, y in reg[k].items() if x != "names"}}
        hits += check_item(dl, pitem, registry, via + (pname,), seen | {k}, depth + 1)
    return hits


def public_match(h):
    if "label" in h:
        return {"entry": h["label"], "class": h["class"]}
    m = {"entry": h["entry"], "id": h["id"], "class": h["class"], "cat": h["cat"], "scope": h["scope"],
         "field": h["field"], "alias": h["alias"]}
    if h["via"]:
        m["via"] = " > ".join(h["via"])
    return m


def _dedupe(ms):
    out, seen = [], set()
    for m in ms:
        k = json.dumps(m, sort_keys=True)
        if k not in seen:
            seen.add(k)
            out.append(m)
    return out


def verdict_new(dl, item, registry=None):
    """New data (public, commit, packs): taint anywhere in the item or its parents denies; a no_new_rows hit on the
    item itself denies new rows (only if it emits rows); no_new_rows on a parent passes."""
    hits = check_item(dl, item, registry)
    taint = [h for h in hits if h["class"] == "taint"]
    nnr_self = [h for h in hits if h["class"] == "no_new_rows" and not h["via"]]
    nnr_par = [h for h in hits if h["class"] == "no_new_rows" and h["via"]]
    emits = item.get("emits_rows", True)
    if taint:
        v, cls, dec = "deny", "taint", taint[0]
    elif nnr_self and emits:
        v, cls, dec = "no_new_rows", "no_new_rows", nnr_self[0]
    else:
        v, cls, dec = "pass", ("no_new_rows" if (nnr_self or nnr_par) else None), (nnr_self or nnr_par or [None])[0]
    return {"hit": bool(hits), "verdict": v, "class": cls,
            "entry": None if dec is None else dec.get("label", dec.get("entry")),
            "taint_hits": len({json.dumps(public_match(h), sort_keys=True) for h in taint}),
            "parent_no_new_rows_pass": sorted({" > ".join(h["via"]) for h in nnr_par}),
            "matches": _dedupe(public_match(h) for h in hits)}


def verdict_replay(dl, src, item):
    """3.H.3 replay verdict in the sampler's schema (hit, class, entry, part, parts, dev_seen_exception) + verdict and
    matches. `parts` lists EVERY part the sampler must drop (empty unless verdict is drop_part); `part`
    is its first element (kept for the schema)."""
    names, descs, doms = _item_strings(item)
    hits = dl.resolve_hits(dl.match(names, descs, doms))
    taint = [h for h in hits if h["class"] == "taint"]
    dev = [h for h in taint if h.get("devname") and h.get("origin") == "dev splits"]
    rest = [h for h in taint if h not in dev]
    whole, part_rows, split = [], defaultdict(set), []
    for h in rest:
        if h.get("scope") == "split":
            split.append(h)
            continue
        f = h["field"]
        pool = descs if f == "dataset" else doms if f == "domain" else None
        # an OHS-3 (hashed) hit never becomes a part: its values would say which string matched (no further detail)
        if pool is not None and len(set(pool)) > 1 and "label" not in h:
            part_rows[f].add(h["string"])
        else:
            whole.append(h)
    for f, vals in list(part_rows.items()):           # every value of the field tainted -> the whole source
        pool = descs if f == "dataset" else doms
        if vals >= set(pool):
            whole += [h for h in rest if h["field"] == f and h.get("scope") != "split"]
            del part_rows[f]
    parts_all = [{"field": f, "values": sorted(v)} for f, v in sorted(part_rows.items())]
    if split:
        parts_all.append({"field": "split", "values": SPLIT_VALUES, "rule": "train_provenance",
                          "note": "only test/dev/eval items are tainted. Fail closed: the sampler keeps a row only "
                                  "if it proves the row comes from a train split (a group_id split token, a train-"
                                  "split marker in meta.dataset, or a builder-declared split it re-checks in the "
                                  "builder source) and drops every other row (RUNBOOK_replay_reads.md 3.2)"})
    parts = [] if whole else parts_all
    part = parts[0] if parts else None
    nnr = [h for h in hits if h["class"] == "no_new_rows"]
    if whole:
        v, dec = "drop", next((h for h in whole if "label" not in h), whole[0])
    elif part:
        v, dec = "drop_part", (rest or split)[0]
    elif dev:
        v, dec = "keep_dev_seen", dev[0]
    elif nnr:
        v, dec = "keep_no_new_rows", nnr[0]
    else:
        v, dec = "keep", None
    return {"hit": bool(hits), "verdict": v,
            "class": "taint" if taint else ("no_new_rows" if nnr else None),
            "entry": None if dec is None else dec.get("label", dec.get("entry")),
            "part": part, "parts": parts,
            "dev_seen_exception": bool(dev) and not whole and not part,
            "matches": _dedupe(public_match(h) for h in hits)}


def _hdr(dl, dl_path, dl_sha, run, query, extra=None):
    prog = Path(__file__).resolve()
    o = dl.meta["ohs3"]
    return {"program": "c_src/common/denylist.py", "version": VERSION, "program_sha256": sha256_file(prog),
            "aliases_sha256": dl.meta["inputs"].get(_rel(ALIASES)), "denylist": _rel(dl_path),
            "denylist_sha256": dl_sha, "run": run, "query": _rel(query), "query_sha256": sha256_file(query),
            "created_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "canonical": dl.meta["canonical"],
            "ohs3_part": (f"checked in-process (selection {o['selection']}; matches shown only as '{OHS3_LABEL}')"
                          if o else "NOT checked"),
            "ohs3_platform_alias_suppressed_entries": o["selected_platform_alias_suppressed"] if o else None,
            "platform_rule": PLATFORM_RULE, "rulings": dl.meta["rulings"],
            "sealed_blocklist": "checked" if dl.meta["sealed"] else "not supplied",
            "provisional": provisional(dl), "notes": notes(dl),
            **(extra or {})}


def _run_counts(ver):
    return {"ohs3_hit": sum(any(m["entry"] == OHS3_LABEL for m in v["matches"]) for v in ver.values()),
            "sealed_hit": sum(any(m["entry"] == SEALED_LABEL for m in v["matches"]) for v in ver.values())}


def run_replay(dl, dl_path, dl_sha, query, out):
    q = json.load(safe_open(query))
    srcs = q.get("sources")
    if not isinstance(srcs, dict):
        raise DenyError(f"{query}: no 'sources' object")
    ver = {s: verdict_replay(dl, s, it) for s, it in sorted(srcs.items())}
    c = Counter(v["verdict"] for v in ver.values())
    counts = {"sources": len(ver), "hit": sum(v["hit"] for v in ver.values()),
              "taint_hit": sum(v["class"] == "taint" for v in ver.values()),
              "no_new_rows_only": c["keep_no_new_rows"], "drop_whole": c["drop"], "drop_part": c["drop_part"],
              "keep_dev_seen": c["keep_dev_seen"], "no_hit": c["keep"], **_run_counts(ver)}
    doc = _hdr(dl, dl_path, dl_sha, "replay", query, {
        "rules": "taint (scope dataset) -> drop the source; taint on one of several meta.dataset/domain values -> "
                 "part (drop only those rows); scope split -> part 'split' (the sampler keeps only rows it proves are "
                 "from a train split, fail closed); every element of `parts` applies; dev seen-source name hit only "
                 "-> keep (dev_seen_exception); no_new_rows (incl. label_quality, A16 b) -> keep (section 5 "
                 "licence rules still apply); a bare platform word never matches (A16 a)",
        "counts": counts, "verdicts": ver})
    write_json(out, doc)
    return counts, ver


def run_check(dl, dl_path, dl_sha, query, out, run="check"):
    q = json.load(safe_open(query))
    ds = q.get("datasets") or q.get("sources")
    if not isinstance(ds, dict):
        raise DenyError(f"{query}: no 'datasets' object")
    missing = [k for k, v in ds.items() if "parents" not in v]
    if missing:
        raise DenyError(f"G1: no 'parents' field for {missing}")
    reg = q.get("parents_registry", {})
    ver = {k: verdict_new(dl, v, reg) for k, v in ds.items()}
    c = Counter(v["verdict"] for v in ver.values())
    counts = {"datasets": len(ver), "hit": sum(v["hit"] for v in ver.values()), "deny_taint": c["deny"],
              "no_new_rows": c["no_new_rows"], "pass": c["pass"],
              "pass_with_parent_no_new_rows": sum(bool(v["parent_no_new_rows_pass"]) and v["verdict"] == "pass"
                                                  for v in ver.values()), **_run_counts(ver)}
    doc = _hdr(dl, dl_path, dl_sha, run, query, {
        "rules": "taint on the dataset or any declared parent (recursive) -> deny; no_new_rows on the dataset -> no "
                 "new rows (a builder emitting rows from it refuses); no_new_rows on a parent -> pass",
        "counts": counts, "verdicts": ver})
    write_json(out, doc)
    return counts, ver


# ------------------------------------------------------------------ DENY_CLASSES.md

CAT_TEXT = {
    "licence": "licence or terms (NC, ND, research-only, unknown, not on the allowed list, HF card or mirror only, "
               "unreachable record)",
    "ohs_source": "OHS-1/2/3 source, its sibling, or Stack Exchange text", "ohs3_avoid": "listed 'avoid' in "
    "ohs3/used_sources.json (as recorded in rejected.json)", "forbidden_task": "in or sharing texts with the 152 "
    "forbidden label-NLI tasks", "di_test": "Decision Index test benchmark", "test_split": "test-only, eval-only or "
    "hidden-label split", "dev_eval": "dev or eval source", "llm_written": "LLM-written or model-assisted text or "
    "labels", "non_human_labels": "automatic, distant, silver, simulated or machine-translated labels or text",
    "gold_noise": "gold labels wrong or not decidable above the bar", "derived": "built on or sharing texts with a "
    "tainted dataset", "sealed": "sealed-suite source", "jev": "Jev output or JevBench item source",
    "unclear": "reason unclear (default taint)", "already_used": "already used by C1 or round 1",
    "extra_rows": "extra rows of a used set", "duplicate_taxonomy": "duplicate taxonomy or framing",
    "other_subset_used": "a different subset or pool of it is used", "low_value": "low value", "too_few_options":
    "too few options", "overlap_own_sets": "overlaps C's own sets",
    "label_quality": "rejected only for label quality: silver, distant or automatic labels, or noisy gold, on usable "
                     "text (A16 b; the program checks the recorded reason names no taint reason)"}


def classes_md(dl, out):
    ents = dl.entries
    o = dl.meta["ohs3"]
    lines = [
        "# DENY_CLASSES: reason class of every 3.H deny entry (for the C PREREG amendment)", "",
        f"Generated by `c_src/common/denylist.py classes` (v{VERSION}) from `c_src/common/deny_aliases.json` "
        f"(sha256 `{dl.meta['inputs'].get(_rel(ALIASES), '')[:16]}...`) and the inputs listed in 3.H.1. "
        "Regenerate it; do not edit by hand.", "",
        "**Classes (C_DATA_SPEC.md 3.H.1).** `taint`: the text or labels are unusable for us; denies the dataset as "
        "new data, every dataset built on it (declared parents, recursive) and its replay rows. `no_new_rows`: no new "
        "rows from it; its text is not tainted, so children pass and replay rows are kept (section 5 licence rules "
        "still apply). When the recorded reason is unclear, or mixes a taint reason with a no_new_rows reason, the "
        "class is `taint`.", "",
        "**Label quality (PREREG_FINAL.md A16, ruling b).** An entry rejected only for label quality (silver, distant "
        "or automatic labels, or noisy gold) is `no_new_rows`, category `label_quality`: no new rows from it, but "
        "datasets built on its text pass (T-REx, so MuSiQue passes) and its replay rows are kept. Contamination, "
        "licence, forbidden-task, dev and eval entries stay `taint`. The program reads the recorded reason of every "
        "`label_quality` entry and fails the build if it also names a taint reason (licence or terms, OHS / "
        "used_sources / avoid / locked, a forbidden task, a test, dev or eval split, the Decision Index, LLM or "
        "machine-translated / simulated / synthetic text, Jev, sealed); such an entry keeps its taint category. "
        "LLM-written text or labels (`llm_written`) is not a label-quality-only reason and stays `taint`.", "",
        "**Scope.** `dataset`: the whole dataset. `split`: only its test, dev or eval items are tainted (a dev/eval "
        "source or a Decision Index benchmark that has a train split); replay rows from the train split are kept. "
        "`part`: one subset, half or per-item filter, applied by a program check (the dataset itself stays IN).", "",
        "**Replay exception (3.H.3).** A replay source that dev uses as a seen source by design (gate_dev name rule) "
        "is kept when that is its only taint reason. Test-split, OHS, licence and Jev reasons always drop.", "",
        "**Persona seeds (2.1).** O*NET's entry (large_labelsets #9) is `no_new_rows`, so a pack or commit row that "
        "declares O*NET as its persona-seed parent passes.", ""]
    if o:
        lines += [f"**OHS-3 part.** `ohs3/used_sources.json` is read only inside the program: {o['entries']} entries, "
                  f"{o['selected']} selected as 'avoid' (fixed selection `{o['selection']}`: rejected.json texts "
                  "equate 'locked' with 'avoid to be safe', and A16 ruling c confirms it; the only other choice, "
                  "`avoid_only`, needs a PREREG amendment) or as OHS-3 sources. All selected entries are class `taint`, category `ohs3_avoid`, "
                  f"scope `dataset`. Their names are withheld; a match prints only `{OHS3_LABEL}`. A checked name "
                  "is matched directly, and every clear entry it hits also has all its curated aliases checked "
                  "against the hashed names (so clinc150 and clinc_oos, say, cannot miss each other). Canary check "
                  "(names rejected.json records as 'avoid'): "
                  f"{sum(v == 'hit' for v in o['canaries'].values())}/{len(o['canaries'])} hit.", "",
                  "**Bare platform words (PREREG_FINAL.md A16, ruling a).** A bare platform or text-source word "
                  "(Wikipedia, Wikidata, Reddit, Twitter, GitHub, arXiv, Zenodo, Hugging Face, Kaggle, OSF, PubMed, "
                  "news, web, Common Crawl, books, movies, reviews, Stack Exchange) never matches on its own: it is "
                  "never a derived alias of a hashed entry, and it is not matched in any other way. Real text overlap "
                  "is caught by the counts-only n-gram decontamination against OHS-1/2/3, the sealed exports, "
                  "Decision Index test items and JevBench items, run before every freeze. In this build "
                  f"**{o['selected_platform_alias_suppressed']} of the {o['selected']} selected entries had such a "
                  "word left out** (count only, a disclosure). Curated aliases are not derived: Stack Exchange stays "
                  "an alias of its own OHS entry, because its text is the denied source.", ""]
    else:
        lines += ["**OHS-3 part.** Not read in this build (Python API, non-canonical; the CLI always reads it).", ""]
    lines += ["**Sealed-suite candidates.** Never listed here; checked only through `--sealed-blocklist` (read in the "
              "program's own process, matches print only `sealed-block`). The sealed suite is frozen (A15); with no "
              "block-list supplied, sealed text overlap is caught by the counts-only n-gram decontamination against "
              "the sealed exports before every freeze (A16 a).", ""]
    by = Counter((e["class"]) for e in ents)
    cat = Counter((e["class"], e["cat"]) for e in ents)
    lines += [f"**Totals.** {len(ents)} clear entries: {by['taint']} `taint`, {by['no_new_rows']} `no_new_rows`"
              + (f", plus {o['selected']} hashed OHS-3 entries (`taint`)." if o else "."), "",
              "| Class | Reason category | Meaning | Entries |", "|---|---|---|---|"]
    for (c, k), n in sorted(cat.items()):
        lines.append(f"| {c} | {k} | {CAT_TEXT.get(k, '')} | {n} |")
    groups = [("golden_src/*/rejected.json", lambda e: e["origin"].startswith("rejected:")),
              ("C_DATA_SPEC.md 3.G table", lambda e: e["origin"].startswith("3.G")),
              ("forbidden_label_nli.json (152 tasks + aggregate)", lambda e: e["origin"] == "forbidden_label_nli.json"),
              ("GOLDEN_SPEC.md OHS-1/2/3 source list", lambda e: e["origin"].startswith("GOLDEN_SPEC.md OHS")),
              ("Dev and eval sources", lambda e: e["origin"] in ("dev splits", "eval files", "GOLDEN_SPEC.md")),
              ("Decision Index test benchmarks", lambda e: e["id"].startswith("di:")),
              ("Spec extras (7.1, 7.4, 9)", lambda e: e["id"].startswith("extra:"))]
    for title, pred in groups:
        g = [e for e in ents if pred(e)]
        lines += ["", f"## {title} ({len(g)})", "", "| ID | Entry | Class | Reason category | Scope |",
                  "|---|---|---|---|---|"]
        for e in g:
            nm = e["name"].replace("|", "/")
            note = f" ({e['note']})" if e.get("note") else ""
            lines.append(f"| `{e['id']}` | {nm}{note} | {e['class']} | {e['cat']} | {e['scope']} |")
    Path(out).write_text("\n".join(lines) + "\n")


# ------------------------------------------------------------------ CLI

def _build_from_args(a):
    """The CLI build: always the canonical one (3.H.2: no override flag). Only the sealed block-list (an extra input,
    which can only add denials) and --strict (fail on any uncurated entry) are options."""
    dl = build(sealed=a.sealed_blocklist, strict=a.strict)
    if not dl.meta["canonical"]:
        raise DenyError("internal: the CLI build is not canonical")
    return dl


def _print_build(dl):
    d = denylist_doc(dl)
    log(f"deny-list: {d['counts']['entries']} clear entries ({d['counts']['taint']} taint, "
        f"{d['counts']['no_new_rows']} no_new_rows); warnings {len(d['warnings'])}")
    for w in d["warnings"]:
        log("WARNING " + w)
    o = dl.meta["ohs3"]
    if o:
        log(f"used_sources (in-process): {o['entries']} entries, {o['selected']} selected (selection "
            f"{o['selection']}: avoid, locked or OHS-3), {o['unparsed']} unparsed; "
            f"{o['selected_platform_alias_suppressed']} selected entries had a bare platform word left out (A16 a: "
            "never matched); canaries: " + ", ".join(f"{k} {v}" for k, v in o["canaries"].items()))
    return d


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["build", "replay", "check", "classes", "paths"])
    ap.add_argument("rest", nargs="*")
    ap.add_argument("--query", help="replay default: c_build/replay_denylist_query.json")
    ap.add_argument("--out", help="replay default: c_build/replay_denylist_verdicts.json (what the sampler reads)")
    ap.add_argument("--run", default="check", help="label of a check run (public, commit, ...)")
    ap.add_argument("--denylist", default=str(DEFAULT_DENYLIST))
    ap.add_argument("--sealed-blocklist", help="the sealed block-list (an extra input; matches print 'sealed-block')")
    ap.add_argument("--strict", action="store_true", help="fail on any uncurated entry")
    # no --used-sources, --no-ohs3 or selection flag: 3.H.2 'There is no override flag' (tests use the Python API)
    ap.add_argument("--fail-on-taint", action="store_true", help="builder start: exit 3 on any taint verdict")
    a = ap.parse_args(argv)
    if a.cmd == "paths":
        bad = 0
        for p in a.rest:
            why = check_path(p)
            print(f"{'REFUSED' if why else 'ok':8s} {p}" + (f"  ({why})" if why else ""))
            bad += bool(why)
        return 2 if bad else 0
    dl = _build_from_args(a)
    d = _print_build(dl)
    dl_sha = write_json(a.denylist, d)
    log(f"wrote {_rel(a.denylist)} sha256 {dl_sha[:16]}...")
    if a.cmd == "build":
        return 0
    if a.cmd == "classes":
        out = a.out or str(HERE / "DENY_CLASSES.md")
        classes_md(dl, out)
        log(f"wrote {_rel(out)}")
        return 0
    if a.cmd == "replay":
        a.query, a.out = a.query or str(REPLAY_QUERY), a.out or str(REPLAY_VERDICTS)
    if not a.query or not a.out:
        ap.error("--query and --out are required")
    if a.cmd == "replay":
        counts, ver = run_replay(dl, a.denylist, dl_sha, a.query, a.out)
    else:
        counts, ver = run_check(dl, a.denylist, dl_sha, a.query, a.out, a.run)
    log(f"{a.cmd} {a.run if a.cmd == 'check' else ''} {_rel(a.query)} -> {_rel(a.out)}: {json.dumps(counts)}")
    for k, v in sorted(ver.items()):
        print(f"  {'HIT ' if v['hit'] else 'no-hit'} {k}: {v['verdict']}" + (f" ({v['entry']})" if v["entry"] else ""))
    if a.cmd == "check" and a.fail_on_taint and counts.get("deny_taint"):
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
