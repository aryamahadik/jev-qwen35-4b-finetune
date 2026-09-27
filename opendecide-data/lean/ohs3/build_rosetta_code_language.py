"""OHS-3 part: rosetta_code_language (programming-language identification, 20-way choice, track U).

Source: Rosetta Code (https://rosettacode.org), crawled mid-2022 into the Hugging Face dataset christopher/rosetta-code
(train, the only split), pinned revision 11d8b38cbd90b0ae5bde304ae2d4ba5ace10af05 (parquet uploaded 2022-07-01).
Licence: GNU Free Documentation License 1.3 (Rosetta Code's own site licence; HF card `license: gfdl`). The full GFDL
1.3 text (gnu.org) is saved in the cache and shipped next to the output as rosetta_code_language_GFDL-1.3.txt.

Item = one Rosetta Code solution (the `code` field only: no task name, no task description, no language header).
Question: which programming language is the code written in? Label = the row's `language_name`.

Label set: the 20 `language_name` values with the most rows in the split (ties broken with a seeded shuffle; there is
no tie at rank 20 at this revision). Label definitions are author-written (one neutral sentence per language,
written once and frozen before sampling; loosely following the first sentence of each Rosetta Code language page).

Cleaning (the code is otherwise left verbatim):
  * layout only: CRLF -> LF, U+00A0 (no-break space, an HTML-scrape artefact of the crawl) -> space, leading and
    trailing blank lines dropped;
  * a shebang line (`#!...`) and Racket `#lang ...` lines (Racket's module-language line, the shebang equivalent)
    are removed;
  * every comment (Pygments comment token, preprocessor tokens excluded; small regex lexer for zkl, which Pygments
    lacks) that names one of the 20 languages, a related tool (e.g. tclsh, ghc, javac) or a source-file extension of
    them (e.g. .py, .exw, .ijs) is removed; a line left empty by that removal is dropped;
  * a sample in which a string literal names one of the languages / tools / extensions is DROPPED (not edited), so
    code is never changed; samples containing crawl artefacts ({{header|..}}, {{works with|..}}, {{out}} ...) are
    dropped; samples outside 20-6,000 chars after cleaning are dropped.
Identifiers and imports that are part of the code itself (e.g. `import java.util.*`, `(require racket/list)`) are kept;
their counts are reported in the summary.

Sampling: at most one sample per task over the WHOLE part (so also at most 1 per (task, language)); 142 items,
7 per language + 1 extra for 2 seeded languages; candidates per language shuffled with random.Random(SEED) in
row-index order, round-robin over languages (frequency order) taking the next clean candidate whose task is unused.
Rows shuffled; the 20 options shuffled per row with the same RNG.

Determinism: first run downloads the pinned parquet + README + dataset_infos.json into
ohs3/cache/rosetta_code_language/<rev>/ and the GFDL text into ohs3/cache/rosetta_code_language/fdl-1.3.txt;
later runs read only the cache (sha256 recorded). Pygments version is asserted. Seed 20261026.

No model predictions, results or LLM APIs are used.
  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python ohs3/build_rosetta_code_language.py
"""
import hashlib
import json
import random
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

import pyarrow.parquet as pq
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.token import Comment, String

LEAN = Path(__file__).resolve().parents[1]
REPO = "christopher/rosetta-code"
REV = "11d8b38cbd90b0ae5bde304ae2d4ba5ace10af05"
PARQUET_REL = "data/train-00000-of-00001-8b4da49264116bbf.parquet"
CACHE_ROOT = LEAN / "ohs3" / "cache" / "rosetta_code_language"
CACHE = CACHE_ROOT / REV
GFDL_CACHE = CACHE_ROOT / "fdl-1.3.txt"
GFDL_URL = "https://www.gnu.org/licenses/fdl-1.3.txt"
OUT = LEAN / "data" / "ohs3_parts" / "rosetta_code_language.jsonl"
SUMMARY = LEAN / "data" / "ohs3_parts" / "rosetta_code_language_summary.json"
GFDL_OUT = LEAN / "data" / "ohs3_parts" / "rosetta_code_language_GFDL-1.3.txt"

TASK = "rosetta_code_language"
SEED = 20261026
N_ITEMS = 142
N_LANGS = 20
MIN_LEN, MAX_LEN = 20, 6000
PYGMENTS_VERSION = "2.21.0"
LICENCE = "GFDL-1.3 (GNU Free Documentation License 1.3; Rosetta Code content)"
GFDL_NOTICE = ("Code from Rosetta Code (https://rosettacode.org), contributed by Rosetta Code users and available under "
               "the GNU Free Documentation License 1.3 (https://www.gnu.org/licenses/fdl-1.3.html); obtained via the "
               f"Hugging Face dataset {REPO} at revision {REV}. Modified for OHS-3: shebang/#lang lines and comments "
               "naming a programming language removed, whitespace normalised. The full licence text is shipped as "
               "rosetta_code_language_GFDL-1.3.txt.")
ATTRIBUTION = ("Rosetta Code, https://rosettacode.org (crawl of mid-2022, HF dataset christopher/rosetta-code by "
               "Christopher Akiki).")
LICENCE_EVIDENCE = ["https://rosettacode.org/wiki/Rosetta_Code:Copyrights (site licence: GFDL 1.3)",
                    f"https://huggingface.co/datasets/{REPO}/blob/{REV}/README.md (card metadata: license: gfdl)"]
INSTRUCTIONS = "Which programming language is this code written in?"

# Author-written definitions: one neutral sentence per language, written once and frozen before sampling.
DEFS = {
    "Phix": "An open-source, self-hosted hybrid interpreter/compiler programming language derived from Euphoria, developed by Pete Lomax.",
    "Julia": "A high-level, high-performance, dynamically typed programming language designed for technical and numerical computing.",
    "Wren": "A small, fast, class-based concurrent scripting language designed to be embedded in host applications.",
    "Go": "A statically typed, compiled, garbage-collected programming language with built-in concurrency, designed at Google.",
    "Raku": "A multi-paradigm, gradually typed programming language in the Perl family, formerly known as Perl 6.",
    "Perl": "A high-level, general-purpose, interpreted dynamic programming language originally developed for text processing.",
    "Python": "A high-level, general-purpose, interpreted programming language that emphasises code readability.",
    "Nim": "A statically typed, compiled, general-purpose systems programming language that compiles via C, C++ or JavaScript.",
    "J": "An array programming language in the APL family, written with the ASCII character set, developed by Kenneth Iverson and Roger Hui.",
    "C": "A general-purpose, procedural, statically typed systems programming language created by Dennis Ritchie at Bell Labs.",
    "Haskell": "A purely functional, statically typed programming language with lazy evaluation and type inference.",
    "Kotlin": "A statically typed, general-purpose programming language developed by JetBrains that runs mainly on the Java Virtual Machine.",
    "Java": "A class-based, object-oriented, statically typed programming language that compiles to bytecode for the Java Virtual Machine.",
    "Ruby": "A dynamic, interpreted, object-oriented general-purpose programming language created by Yukihiro Matsumoto.",
    "Racket": "A general-purpose, multi-paradigm programming language in the Lisp/Scheme family, designed as a platform for creating languages.",
    "C++": "A general-purpose, statically typed, compiled programming language created by Bjarne Stroustrup as an extension of C.",
    "REXX": "A structured, high-level, interpreted programming language (Restructured Extended Executor) developed at IBM by Mike Cowlishaw.",
    "zkl": "A small, general-purpose, object-oriented, dynamically typed programming language that borrows concepts from functional and prototype-based programming.",
    "D": "A general-purpose, statically typed, compiled systems programming language originally created by Walter Bright at Digital Mars.",
    "Tcl": "A high-level, general-purpose, interpreted dynamic scripting language (Tool Command Language) created by John Ousterhout.",
}

# Pygments lexer alias per language (zkl has none -> small regex lexer below).
LEXER = {"Phix": "phix", "Julia": "julia", "Wren": "wren", "Go": "go", "Raku": "raku", "Perl": "perl",
         "Python": "python", "Nim": "nim", "J": "j", "C": "c", "Haskell": "haskell", "Kotlin": "kotlin",
         "Java": "java", "Ruby": "ruby", "Racket": "racket", "C++": "cpp", "REXX": "rexx", "zkl": None, "D": "d",
         "Tcl": "tcl"}

# ---------------- mention patterns (frozen) ----------------
# multi-letter names and tools, case-insensitive, word-bounded
NAME_WORDS = [
    "phix", "julia", "wren", "golang", "raku", "rakudo", "perl", "perl5", "perl6", "python", "python2", "python3",
    "cpython", "pypy", "ipython", "nim", "nimble", "haskell", "ghc", "ghci", "runhaskell", "runghc", "hugs", "kotlin",
    "kotlinc", "java", "javac", "jdk", "jre", "ruby", "irb", "jruby", "racket", "raco", "drracket", "regina", "zkl",
    "tcl", "tclsh", "tcllib", "gcc", "clang", "dmd", "gdc", "ldc", "ldc2", "rdmd", "jconsole", "ijconsole",
    "jsoftware",
]
EXTS = ["py", "pyw", "pl", "pm", "p6", "pl6", "pm6", "raku", "rakumod", "rb", "java", "jar", "go", "jl", "nim",
        "nims", "hs", "lhs", "kt", "kts", "rkt", "cpp", "cxx", "cc", "hpp", "hxx", "h", "c", "d", "tcl", "rex",
        "rexx", "zkl", "exw", "ew", "e", "wren", "ijs"]
RE_WORDS = re.compile(r"(?<![\w])(?:" + "|".join(NAME_WORDS) + r")(?![\w])", re.I)
RE_REXX = re.compile(r"rexx", re.I)  # also ooRexx / NetRexx
RE_CPP = re.compile(r"(?<![\w])(?:c\+\+|cpp|g\+\+|cxx)(?![\w+])", re.I)
RE_EXT = re.compile(r"(?<![\w.])[A-Za-z_][\w\-/\\]*\.(?:" + "|".join(sorted(EXTS, key=len, reverse=True)) + r")(?![\w])", re.I)
RE_SHEBANG_LIKE = re.compile(r"#!\s*/")
# Go and single-letter names: in COMMENTS any case-sensitive standalone use counts (removing a comment is harmless);
# in STRINGS only a language-naming context counts (strings are dropped, not edited, so avoid dropping on "C"/"Go!").
RE_GO_COMMENT = re.compile(r"(?<![\w])go(?![\w])", re.I)
RE_LETTER_COMMENT = re.compile(r"(?<![\w'])[CDJ](?![\w'])")
_CTX_AFTER = (r"(?:language|lang|code|version|program|programs|compiler|implementation|library|libraries|standard|"
              r"style|function|functions|source|routine|solution|translation|port|runtime|entry|example|syntax|"
              r"interpreter|toolchain)")
_CTX_BEFORE = r"(?:in|ANSI|ISO|K&R|standard|using|native|pure|plain|written in|translated from|port of|the)"
RE_LETTER_STRING = re.compile(
    r"(?<![\w])(?:" + _CTX_BEFORE + r")\s+(?:C|D|J|Go)(?![\w'+#])"
    r"|(?<![\w'])(?:C|D|J|Go)[\s-]+" + _CTX_AFTER + r"(?![\w])"
    r"|(?<![\w])(?:C(?:89|90|99|11|17|18|23)|D[12])(?![\w])")
RE_GO_STRING = re.compile(r"(?<![\w])Go(?:lang)?(?![\w!?'])")


# (verifier fix) version-numbered language names in comments (e.g. "in j6", "c99", "go1.18", "tcl8.6") and comments that
# are only a version stamp (e.g. Rosetta Code Kotlin entries' "// version 1.1.2": a source-specific convention marker).
RE_VERSIONED_NAME = re.compile(r"(?<![\w])(?:j\d{1,3}|c\d\d|d[12]|go1(?:\.\d+)*|tcl\d(?:\.\d+)*|python\d(?:\.\d+)*|"
                               r"ruby\d(?:\.\d+)*|java\d+|jdk\d+|perl\d(?:\.\d+)*|julia\d(?:\.\d+)*|nim\d(?:\.\d+)*|"
                               r"kotlin\d(?:\.\d+)*)(?![\w])", re.I)
RE_VERSION_STAMP = re.compile(r"^[\W_]*(?:version|ver\.?|v)\s*\d[\w.\-]*[\W_]*$", re.I)


def mentions_comment(s):
    return (RE_WORDS.search(s) or RE_REXX.search(s) or RE_CPP.search(s) or RE_EXT.search(s)
            or RE_GO_COMMENT.search(s) or RE_LETTER_COMMENT.search(s) or RE_SHEBANG_LIKE.search(s)
            or RE_VERSIONED_NAME.search(s) or RE_VERSION_STAMP.match(s.strip()))


def mentions_string(s):
    return (RE_WORDS.search(s) or RE_REXX.search(s) or RE_CPP.search(s) or RE_EXT.search(s)
            or RE_LETTER_STRING.search(s) or RE_GO_STRING.search(s))


# residual (code-token) cue, for reporting only
RE_RESIDUAL = re.compile(r"(?<![\w])(?:" + "|".join(NAME_WORDS) + r"|c\+\+)(?![\w])", re.I)
# (verifier fix) a sample whose remaining code tokens name its OWN language or tool (e.g. `import java.util.*` in Java,
# `package require Tcl 8.5` in Tcl, `import kotlin.math.sqrt` in Kotlin, `(require racket/list)`) gives the answer
# away and is DROPPED (code is never edited). Names of OTHER languages in code (e.g. `import java.*` in Kotlin) are kept.
OWN_NAMES = {
    "Phix": ["phix"], "Julia": ["julia"], "Wren": ["wren"], "Go": ["golang"], "Raku": ["raku", "rakudo", "perl6"],
    "Perl": ["perl", "perl5"], "Python": ["python", "python2", "python3", "cpython", "pypy", "ipython"],
    "Nim": ["nim", "nimble"], "J": ["jconsole", "ijconsole", "jsoftware"], "C": ["gcc", "clang"],
    "Haskell": ["haskell", "ghc", "ghci", "runhaskell", "runghc", "hugs"], "Kotlin": ["kotlin", "kotlinc", "kotlinx"],
    "Java": ["java", "javax", "javac", "jdk", "jre"], "Ruby": ["ruby", "irb", "jruby"],
    "Racket": ["racket", "raco", "drracket"], "C++": [r"c\+\+", "cpp", r"g\+\+", "cxx"], "REXX": ["rexx", "regina"],
    "zkl": ["zkl"], "D": ["dmd", "gdc", "ldc", "ldc2", "rdmd"], "Tcl": ["tcl", "tclsh", "tcllib"],
}
RE_OWN = {k: re.compile(r"(?<![\w])(?:" + "|".join(v) + r")(?![\w+])", re.I) for k, v in OWN_NAMES.items()}
RE_OWN["REXX"] = re.compile(r"rexx|(?<![\w])regina(?![\w])", re.I)

ARTEFACT = re.compile(r"\{\{\s*(?:header|works with|libheader|trans|out|output|lang|improve|incorrect|omit from|"
                      r"draft|task|alertbox|example-needs-review)\b", re.I)

sha = lambda s: hashlib.sha256(s.encode()).hexdigest()


def ensure_snapshot():
    pq_path = CACHE / PARQUET_REL
    if not pq_path.exists():
        from huggingface_hub import hf_hub_download
        for f in (PARQUET_REL, "README.md", "dataset_infos.json"):
            hf_hub_download(REPO, f, repo_type="dataset", revision=REV, local_dir=str(CACHE))
        shutil.rmtree(CACHE / ".cache", ignore_errors=True)
    if not GFDL_CACHE.exists():
        import urllib.request
        GFDL_CACHE.write_bytes(urllib.request.urlopen(GFDL_URL, timeout=60).read())
    return pq_path


# ---------------- tokenising ----------------
_ZKL = re.compile(r'(?P<c>//[^\n]*|/\*[\s\S]*?\*/|(?m:^[ \t]*#(?!<<<|if|else|endif|include|fcn|text|tokenize)[^\n]*))'
                  r'|(?P<s>"(?:\\.|[^"\\\n])*"|0\'(.)[\s\S]*?\3)'
                  r'|(?P<h>#<<<[\s\S]*?#<<<)')


def segments(lang, text):
    """Yield (kind, start, end) for comment ('c') and string ('s') segments."""
    if LEXER[lang] is None:
        for m in _ZKL.finditer(text):
            if m.group("c"):
                yield "c", m.start(), m.end()
            elif m.group("s"):
                yield "s", m.start(), m.end()
            else:  # #<<< heredoc: text block (string)
                yield "s", m.start(), m.end()
        return
    lx = get_lexer_by_name(LEXER[lang], stripnl=False, stripall=False, ensurenl=False)
    toks = list(lx.get_tokens_unprocessed(text))
    assert "".join(v for _, _, v in toks) == text, lang
    cur = None  # (kind, start, end)
    for idx, tt, v in toks:
        if tt in Comment and not (tt in Comment.Preproc or tt in Comment.PreprocFile):
            kind = "c"
        elif tt in String:
            kind = "s"
        else:
            kind = None
        if cur and kind == cur[0] and idx == cur[2]:
            cur = (kind, cur[1], idx + len(v))
            continue
        if cur:
            yield cur
        cur = (kind, idx, idx + len(v)) if kind else None
    if cur:
        yield cur


def strip_blank_edges(lines):
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def clean(lang, code):
    """Return (state or None, info dict)."""
    info = {"shebang_removed": False, "lang_line_removed": False, "comments_removed": 0}
    text = code.replace("\r\n", "\n").replace("\r", "\n").replace(" ", " ")
    if ARTEFACT.search(text):
        return None, "crawl_artefact"
    lines = strip_blank_edges(text.split("\n"))
    if lines and lines[0].lstrip().startswith("#!"):
        lines.pop(0)
        info["shebang_removed"] = True
    kept = []
    for i, ln in enumerate(lines):
        if re.match(r"^\s*#lang\b", ln):
            info["lang_line_removed"] = True
            continue
        kept.append(ln)
    text = "\n".join(strip_blank_edges(kept))
    if not text.strip():
        return None, "empty"

    removed = []  # (start, end)
    for kind, s, e in segments(lang, text):
        seg = text[s:e]
        if kind == "s" and mentions_string(seg):
            return None, "string_names_language"
        if kind == "c" and mentions_comment(seg):
            # keep the trailing newline if the comment token included it
            if seg.endswith("\n"):
                e -= 1
            removed.append((s, e))
    info["comments_removed"] = len(removed)
    if removed:
        mask = bytearray(len(text))
        for s, e in removed:
            for k in range(s, e):
                mask[k] = 1
        out_lines, pos = [], 0
        for ln in text.split("\n"):
            a, b = pos, pos + len(ln)
            pos = b + 1
            touched = any(mask[a:b])
            if not touched:
                out_lines.append(ln)
                continue
            new = "".join(ch for k, ch in zip(range(a, b), ln) if not mask[k]).rstrip()
            if new.strip():
                out_lines.append(new)
        text = "\n".join(strip_blank_edges(out_lines))
    if not (MIN_LEN <= len(text) <= MAX_LEN):
        return None, "length_after_cleaning"
    # residual cues in the remaining comments/strings would be a bug: re-check
    for kind, s, e in segments(lang, text):
        seg = text[s:e]
        if (kind == "c" and mentions_comment(seg)) or (kind == "s" and mentions_string(seg)):
            return None, "residual_after_cleaning"
    if RE_OWN[lang].search(text):
        return None, "code_names_own_language"
    info["residual_code_mentions"] = sorted({m.group(0) for m in RE_RESIDUAL.finditer(text)})
    return text, info


def main():
    assert pygments.__version__ == PYGMENTS_VERSION, pygments.__version__
    pq_path = ensure_snapshot()
    pq_sha = hashlib.sha256(pq_path.read_bytes()).hexdigest()
    readme = CACHE / "README.md"
    readme_sha = hashlib.sha256(readme.read_bytes()).hexdigest()
    gfdl_bytes = GFDL_CACHE.read_bytes()
    assert b"Version 1.3, 3 November 2008" in gfdl_bytes
    tbl = pq.read_table(pq_path).to_pylist()

    # 1) top-20 languages by row count (seeded tie-break)
    freq = Counter(r["language_name"] for r in tbl)
    rng = random.Random(SEED)
    keys = sorted(freq)
    tb = {k: rng.random() for k in keys}
    ranked = sorted(keys, key=lambda k: (-freq[k], tb[k]))
    labels = ranked[:N_LANGS]
    boundary_tie = freq[ranked[N_LANGS - 1]] == freq[ranked[N_LANGS]]
    assert set(labels) == set(DEFS), set(labels) ^ set(DEFS)

    # 2) candidate pool: clean every row of the 20 languages; at most one row per (task, language)
    # code text (whitespace-normalised) that occurs under more than one language_name anywhere in the split has an
    # ambiguous attribution (crawl mis-assignment, e.g. a Java block filed under J): all such rows are dropped.
    wsnorm = lambda s: re.sub(r"\s+", " ", (s or "").replace("\u00a0", " ")).strip()
    code_langs = defaultdict(set)
    for r in tbl:
        code_langs[wsnorm(r["code"])].add(r["language_name"])
    drops = Counter()
    cands = defaultdict(list)
    seen_tl = set()
    stats = Counter()
    for idx, r in enumerate(tbl):
        lang = r["language_name"]
        if lang not in DEFS:
            continue
        tl = (r["task_name"], lang)
        if tl in seen_tl:
            drops["duplicate_task_language"] += 1
            continue
        seen_tl.add(tl)
        if not r["code"] or len(r["code"]) > 50_000:
            drops["raw_empty_or_huge"] += 1
            continue
        if len(code_langs[wsnorm(r["code"])]) > 1:
            drops["same_code_under_another_language"] += 1
            continue
        state, info = clean(lang, r["code"])
        if state is None:
            drops[info] += 1
            continue
        stats["shebang_removed"] += info["shebang_removed"]
        stats["lang_line_removed"] += info["lang_line_removed"]
        stats["samples_with_comment_removed"] += info["comments_removed"] > 0
        cands[lang].append({"idx": idx, "lang": lang, "task": r["task_name"], "task_url": r["task_url"],
                            "language_url": r["language_url"], "state": state, "info": info,
                            "raw_len": len(r["code"])})

    # 3) stratified sampling, one sample per task over the whole part
    base = N_ITEMS // N_LANGS
    extra = set(rng.sample(sorted(labels), N_ITEMS - base * N_LANGS))
    quota = {k: base + (1 if k in extra else 0) for k in labels}
    for k in labels:  # candidates already in row-index order
        rng.shuffle(cands[k])
    ptr = {k: 0 for k in labels}
    used_task = set()
    picked = {k: [] for k in labels}
    skip = Counter()
    while any(len(picked[k]) < quota[k] for k in labels):
        progressed = False
        for k in labels:
            if len(picked[k]) >= quota[k]:
                continue
            while ptr[k] < len(cands[k]):
                c = cands[k][ptr[k]]
                ptr[k] += 1
                if c["task"] in used_task:
                    skip["task_already_used"] += 1
                    continue
                used_task.add(c["task"])
                picked[k].append(c)
                progressed = True
                break
        if not progressed:
            raise SystemExit("ran out of candidates")
    chosen = [c for k in labels for c in picked[k]]
    rng.shuffle(chosen)

    card = "\n".join(f"- {l}: {DEFS[l]}" for l in labels)
    rows = []
    for c in chosen:
        opts = list(labels)
        rng.shuffle(opts)
        key = f"row{c['idx']}"
        rows.append({
            "id": "r_" + sha(f"ohs3:{TASK}:row:{key}")[:12],
            "group_id": f"g:ohs3:{TASK}:{key}",
            "call_id": "c_" + sha(f"ohs3:{TASK}:call:{key}")[:12],
            "split": "ohs3",
            "track": "U",
            "source": TASK,
            "state": c["state"],
            "qtype": "choice",
            "instructions": INSTRUCTIONS,
            "options": opts,
            "gold": c["lang"],
            "role": "choice",
            "card": card,
            "meta": {
                "task": TASK,
                "dataset": REPO,
                "split": "train",
                "revision": REV,
                "snapshot": "Rosetta Code crawl, parquet uploaded to HF 2022-07-01; pinned HF revision dated 2023-09-24",
                "row_index": c["idx"],
                "task_name": c["task"],
                "task_url": c["task_url"],
                "language": c["lang"],
                "language_url": c["language_url"],
                "original_label": c["lang"],
                "url": f"https://huggingface.co/datasets/{REPO}/blob/{REV}/{PARQUET_REL}",
                "record": f"{REPO}@{REV} train row {c['idx']}",
                "source_page": c["task_url"] + c["language_url"],
                "cleaning": {"shebang_removed": c["info"]["shebang_removed"],
                             "lang_line_removed": c["info"]["lang_line_removed"],
                             "comments_removed": c["info"]["comments_removed"],
                             "raw_chars": c["raw_len"]},
                "residual_code_mentions": c["info"]["residual_code_mentions"],
                "licence": LICENCE,
                "licence_notice": GFDL_NOTICE,
                "attribution": ATTRIBUTION,
            },
        })

    # checks
    assert len(rows) == N_ITEMS
    for f in ("id", "group_id", "call_id"):
        assert len({r[f] for r in rows}) == N_ITEMS
    assert len({r["meta"]["task_name"] for r in rows}) == N_ITEMS
    g = Counter(r["gold"] for r in rows)
    assert max(g.values()) / len(rows) <= 0.40 and set(g.values()) <= {base, base + 1}
    for r in rows:
        assert MIN_LEN <= len(r["state"]) <= MAX_LEN
        assert r["gold"] in r["options"] and sorted(r["options"]) == sorted(labels)
        assert " " not in r["state"]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    OUT.write_text(text)
    GFDL_OUT.write_bytes(gfdl_bytes)

    lens = sorted(len(r["state"]) for r in rows)
    resid = Counter()
    for r in rows:
        for m in r["meta"]["residual_code_mentions"]:
            resid[f"{r['gold']}: {m}"] += 1
    summary = {
        "task": TASK,
        "rows": len(rows),
        "qtype": "choice",
        "track": "U",
        "n_options": N_LANGS,
        "class_balance": dict(sorted(g.items(), key=lambda x: (-x[1], x[0]))),
        "max_class_share": round(max(g.values()) / len(rows), 4),
        "languages_with_8_items": sorted(extra),
        "label_set": [{"label": l, "rows_in_split": freq[l]} for l in labels],
        "next_excluded_languages": [{"label": l, "rows_in_split": freq[l]} for l in ranked[N_LANGS:N_LANGS + 3]],
        "boundary_tie_at_rank_20": boundary_tie,
        "instructions": INSTRUCTIONS,
        "card": card,
        "label_definitions_source": "author-written: one neutral sentence per language, written once and frozen before sampling (loosely following the first sentence of each Rosetta Code language page; no syntax hints)",
        "author_written_definitions": DEFS,
        "source": f"Rosetta Code via HF {REPO} (train, only split)",
        "revision": REV,
        "snapshot": {"cache_dir": str(CACHE.relative_to(LEAN)), "parquet": PARQUET_REL, "parquet_sha256": pq_sha,
                     "readme_sha256": readme_sha, "rows_in_split": len(tbl),
                     "gfdl_text": str(GFDL_CACHE.relative_to(LEAN)), "gfdl_sha256": hashlib.sha256(gfdl_bytes).hexdigest(),
                     "pygments_version": pygments.__version__},
        "licence": LICENCE,
        "licence_notice": GFDL_NOTICE,
        "licence_evidence": LICENCE_EVIDENCE,
        "licence_text_shipped": str(GFDL_OUT.relative_to(LEAN)),
        "attribution": ATTRIBUTION,
        "date_range": "Rosetta Code pages as crawled around June 2022 (parquet uploaded 2022-07-01; card cites access 2022-12-08); solutions written 2007-2022; no per-item dates; track U",
        "pool": {"candidates_per_language": {l: len(cands[l]) for l in labels}, "dropped": dict(drops),
                 "cleaning_counts_in_pool": dict(stats), "sampling_skips": dict(skip)},
        "sampled_cleaning": {"shebang_removed": sum(r["meta"]["cleaning"]["shebang_removed"] for r in rows),
                             "lang_line_removed": sum(r["meta"]["cleaning"]["lang_line_removed"] for r in rows),
                             "rows_with_comment_removed": sum(r["meta"]["cleaning"]["comments_removed"] > 0 for r in rows)},
        "residual_code_mentions_in_sampled_rows": dict(sorted(resid.items())),
        "sampling": (f"top {N_LANGS} language_name values by row count (seeded tie-break); every row of them cleaned; "
                     f"per language candidates in row order then random.Random({SEED}).shuffle; round-robin over "
                     "languages in frequency order taking the next clean candidate whose task_name is unused (one "
                     "sample per task in the whole part); quota 7 per language, +1 for 2 seeded languages; rows "
                     "shuffled; options shuffled per row with the same RNG"),
        "state_format": "the solution's code only (no task name/description, no language header); NBSP->space, CRLF->LF, blank edge lines trimmed; shebang and #lang lines removed; comments naming a language/tool/extension removed",
        "state_length": {"min": lens[0], "median": lens[len(lens) // 2], "max": lens[-1]},
        "row_indices": sorted(r["meta"]["row_index"] for r in rows),
        "output_sha256": sha(text),
        "uncertain": [
            "Code that names its OWN language/tool outside comments and strings (e.g. `import java.util.*` in Java, `package require Tcl`, `import kotlin.*`, `(require racket/...)`) is dropped (verifier fix); names of OTHER listed languages in code (e.g. `import java.*` in Kotlin) are kept; counts in residual_code_mentions_in_sampled_rows.",
            "Comments with a version-numbered language name (j6, c99, go1.x, tcl8.x ...) or consisting only of a version stamp (Rosetta Code Kotlin convention `// version 1.1.2`) are removed (verifier fix).",
            "Comment/string detection uses Pygments lexers (version pinned) and a small regex lexer for zkl; lexers can mis-tokenise unusual code, so a rare cue in an unrecognised comment may survive.",
            "Comment removal is deliberately broad (any standalone C/D/J/go word or file extension such as 'i.e' counts), so some harmless comments are also removed; code is never edited and samples whose strings name a language are dropped, which slightly shifts the pool away from programs that print language names.",
            "Racket '#lang' lines were removed as the shebang equivalent (judgement call beyond the literal spec); without them a Racket module would not run as-is.",
            "Crawl misattribution: rows whose code also appears under another language were dropped (label-agnostic rule), but a misattributed block that is unique in the split cannot be detected this way; no per-item manual relabelling was done.",
            "Rosetta Code language headers are sometimes wrong or the code belongs to a closely related dialect (e.g. Perl 6 era code under Raku, C code under C++); gold is kept as the source label.",
            "Some languages here are very close (C vs C++, Perl vs Raku, Java vs Kotlin), and short snippets can be valid in more than one; no manual filtering was done.",
            "Some sampled snippets are very short (min 20 chars, e.g. a one-line Perl swap) and may be valid in more than one listed language; kept because the spec only sets a 20-char floor.",
            "Blank lines in the crawl were U+00A0; after NBSP->space they appear as single-space lines (layout only).",
            "Rosetta Code is public since 2007 and widely crawled; contamination is very likely (track U).",
            "Licence: GFDL 1.3 is Rosetta Code's own site licence; the HF card only states 'gfdl'. GFDL requires the licence text and modification notice to travel with the data (shipped + meta.licence_notice).",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps({k: v for k, v in summary.items()
                      if k not in ("row_indices", "card", "author_written_definitions", "licence_notice")},
                     indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
