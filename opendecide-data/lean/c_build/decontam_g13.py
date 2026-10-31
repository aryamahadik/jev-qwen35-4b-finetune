"""decontam_g13.py: G13 counts-only decontamination (C_DATA_SPEC section 7; RUNBOOK B, blocker B1). CPU only, $0.

Run by the orchestrator, one process per run, from lean/ (each run prints COUNTS ONLY; no eval text is ever printed,
logged or kept on disk):
  ../.venv/bin/python c_build/decontam_g13.py --fam F3        c_src/F3/out/candidates_r1.jsonl (every candidate: the
                                                               selection and the refill pool) + the family's
                                                               Claude-written seeds / templates (c_src/F3/gen/**)
  ../.venv/bin/python c_build/decontam_g13.py --final         data/c_parts/c_train_r1.jsonl -> final_mix_r1.json
  ../.venv/bin/python c_build/decontam_g13.py --set packs     shared Claude-written domain packs (c_src/packs)
  ../.venv/bin/python c_build/decontam_g13.py --set formats   format codebooks / styles (c_src/formats)
  ../.venv/bin/python c_build/decontam_g13.py status [names]  log check (r1_check.py preflight / autopilot_check.py)
  ../.venv/bin/python c_build/decontam_g13.py targets         which eval targets resolve (file counts only)
  ../.venv/bin/python c_build/decontam_g13.py calib --fams F3 F6 F9 --out <jsonl>   method 5 hand-check pairs, exactly as
                                                               c_build/g13_cosine_calib_plan.json fixes them (open C
                                                               rows only, never an eval set)
  ../.venv/bin/python c_build/decontam_g13.py fetch           big_patent column-projected into the cache (A25 e)
  ../.venv/bin/python c_build/decontam_g13.py embed-cache     encode every eval text method 5 sees, once (vectors only)
  ../.venv/bin/python c_build/decontam_g13.py census          sealed-side file / item counts (via the child)
  ../.venv/bin/python c_build/decontam_g13.py side-embed-cache  prebuild the sealed-side child's OWN vector cache
                                                               (SideCache, A25 d; vectors + text hashes only; resumable;
                                                               progress counts in logs/decontam_counts/run/)
  ../.venv/bin/python c_build/decontam_g13.py freeze-mixdev   record the mixdev files' shas (MIXDEV_FREEZE.json);
                                                               `status` then names every mixdev file changed since
  ../.venv/bin/python c_build/decontam_g13.py refresh F3 F6 [--targets T ...]   re-scan ONLY targets T (default mixdev +
                                                               mixdev_structure) for logs fresh outside T, merged as a
                                                               full run computes them (hits_by_eval); e.g. after a lane
                                                               rewrites its mixdev, after a failed sealed-side child
                                                               (--targets ohs3 ohs3_src longbench_v2), or big_patent
                                                               with G13_BIGPAT_STREAM=1
  several sets in one eval pass: c_build/decontam_g13_batch.py --sets F3 F6 F9 (same engine, run_sets)

Output: logs/decontam_counts/<set>.json = {"set", "drop_ids" (training row ids; every row of a hit unit = call_id),
"counts_by_eval_and_method", "counts_by_training_source", "short_items", "inputs_sha256", "complete", ...}. The
`drop_ids` key is what mixer.decontam_drop_ids reads. Seed / template / pack hits have no training ids: they are
counted in `seed_hits` (file#literal locators only) and make `seeds_clean` false (the builder must change the seed).

Eval side (spec 7.1; registry in targets()): the 9 dev gate splits, every mix-tuning dev file (A25 c: instance content
only, state + options against training state + options), JevBench public (231) and v1.5.4 item files (item text only;
the one /jev/ path exception of spec 7.4), BTZSC, eval_opi / eval_jagged (state, instructions, options only), the 152
forbidden label-NLI tasks, the OHS-1/2 items and every locally cached split of their source datasets (big_patent:
abstracts of every split + test descriptions, column-projected; dstc8 parquet), TabFact tables (table hashes),
HateXplain and SBF posts (exact text + substring), ejs-5 and the Decision Index test sets. OHS-3 (+ its cached source
datasets) and LongBench v2 are read ONLY by the sealed-side child (A25 d; counts, unit indices and sha digests only).
The sealed suite: sealed_nd/qc/sealed_check.py, run only.

Methods (spec 7.2 1-8 / RUNBOOK B; any hit drops the whole training unit):
  exact_full / exact_seg   normalized full text; every sentence or line of >= 5 words
  exact_short              an eval item under 5 words: exact full-text hash only (never against a training OPTION)
  substring                every eval text of >= 5 words inside a training text (word boundaries)
  ngram10                  any shared word 10-gram (lower case)
  tulu8                    > 50% of an eval text's tokens fall in 8-grams shared with ONE training text
  minhash                  word 5-gram MinHash (100 perms, 20 x 5 bands), confirmed by exact Jaccard >= 0.8 AND
                           word-level edit similarity >= 0.8
  embed      (method 5)    top-5 nearest training texts OF THE SAME SET with cosine >= the hand-fixed threshold
                           (c_build/g13_cosine_threshold.json; eval vectors from the EmbCache, misses encoded live)
  table      (method 9)    normalized header + cell-set hash of every table, where the eval has tables, in every
                           container public-2 renders (markdown, pipe_plain incl. 2 columns, csv, json_records,
                           key_value, html); TabFact's '#'-delimited all_csv files become pipe-table text (same hash)
  structure / structure_g13 / group_id  (method 6 vs mixdev)  the generator's meta.structure_hash, G13's own hash of
                           state + options (names abstracted, options as a set), shared group_id
  template   (method 8)    OPI's strategy strings and jagged's injected line anywhere in a unit's texts; every dev /
                           eval instruction (whole and per sentence / line, >= 5 words) as a substring (templates_instr)
  template_rev (method 8, other direction)  a Claude-written seed piece of >= 3 words EQUAL to a dev / eval instruction
                           sentence / line or OPI / jagged wording, or of 5-9 words CONTAINED in one (seeds_clean
                           false); 2-word equalities and 3-4-word containments are counted report-only. A31 (c):
                           Claude-written seeds / templates only; public-data records (formats-2 records/*.jsonl,
                           PUBLIC_RECORDS) are instance text, checked by methods 1-7 and always binding
  A31 (b) render check     every hit Claude-written seed literal is searched (program, the methods' normalization,
                           split at placeholders / lines, >= 2-word pieces) in its set's training rows (a family: its
                           candidates_r1; packs / formats: every family's candidates_r1 + the public training rows /
                           reserves + the final mix when present); proven absent -> report-only ('A31b: not
                           rendered': seed_hit_locs_report_only, seed_render); rendered -> binding as before.
                           A32 (c): a piece's edge word touching a placeholder, f-string value, `+` operand or
                           %-format match with no space between is dropped ('{n}th' -> '5th'); the bare %-spec has no
                           space flag ('50% sure' is prose); no piece with >= 2 words left -> unprovable (binds)
  sealed_*   (6 P, 7)      sealed_nd/qc/sealed_check.py RUN only, own process, --structure-fields
                           state,card,instructions,options: p_struct / p_template (part P), keyword_hard (sealed
                           domain keywords), and its gram / line / sentence / context kinds; ids + hit kinds only
  big_patent train / validation descriptions (16.2 GB) are scanned only with G13_BIGPAT_STREAM=1 (hfstream: one parquet
  at a time, fetched, scanned, its eval vectors cached, deleted); otherwise the log names that gap and stays incomplete,
  unless G13_BIGPAT_RULING=<tag> names a written ruling whose line 'G13-BIGPAT-RULING <tag>' is in PREREG_FINAL.md
  (this tool never writes it).
Speed switch G13_STREAM_WORKERS=N (default 1 = the serial scan, no process is started): a target with >= 4 parquet files
(>= G13_STREAM_MIN_MB = 32 MB of them, or any hfstream file) is scanned by N worker processes and merged in file order; the
result is the serial scan's (see the G13_STREAM_WORKERS block after stream()). About 2 GB of RAM per worker: N <= 4 on the
16 GB Mac. Not used by the sealed-side child.
"""
from __future__ import annotations

import argparse
import array
import ast
import csv
import difflib
import gzip
import hashlib
import io
import json
import os
import pickle
import re
import shutil
import subprocess
import sys
import tempfile
import tarfile
import time
import traceback
import unicodedata
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

for _k, _v in (("TOKENIZERS_PARALLELISM", "false"), ("OMP_NUM_THREADS", "2"), ("VECLIB_MAXIMUM_THREADS", "2"),
               ("OPENBLAS_NUM_THREADS", "2"), ("MKL_NUM_THREADS", "2"), ("RAYON_NUM_THREADS", "2")):
    os.environ.setdefault(_k, _v)                # the Mac stays light: at most ~2 cores per G13 process
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent          # lean/c_build
LEAN = HERE.parent
REPO = LEAN.parents[1]                          # jev/
HF = Path.home() / ".cache/huggingface/hub"
GH = Path.home() / ".cache/opendecide_ext/gh"    # gh:<owner>/<repo> sparse clones (fetched by program, never opened)
GH_PAT = {"wenhuchen/Table-Fact-Checking": "data/all_csv/*.csv"}
# HF sources too big for the local disk (big_patent: 189 files, 34 GB; 19 GB free on 6 Oct): one parquet at a time is
# downloaded to a temp folder, scanned and deleted (hfstream:), unless a full local snapshot exists (then hf: is used)
HF_STREAM = ("NortheasternUniversity/big_patent",)
STREAM_ROOT = Path("/hfstream")
# big_patent (34 GB on the hub; 'all' = the union of the a..y configs, 17 GB) is fetched column-projected into PROJ by
# `decontam_g13.py fetch` (A25 e; free download cap ~2 GB): the abstract of every split ('all' train / validation /
# test; OHS-2 shows test abstracts, ohs2/build_misc.py) and the test descriptions. The train / validation descriptions
# (16.2 GB) are scanned only with G13_BIGPAT_STREAM=1 (hfstream: one parquet at a time, description column, deleted).
PROJ = Path.home() / ".cache/opendecide_ext/hf_proj"
BIGPAT, BIGPAT_REV = "NortheasternUniversity/big_patent", "2a5336492ddc4e21cebd3865fd2a7e8b070bfede"  # = ohs2 REV
BIGPAT_COLS = {"train": ("abstract",), "validation": ("abstract",), "test": ("abstract", "description")}
BIGPAT_REST = r"^all/(train|validation)-"         # the description column of these files: stream mode only
HF_PARQUET = {"google-research-datasets/schema_guided_dstc8": "refs/convert/parquet"}   # script datasets: parquet copy
# A25 (d): OHS-3 and LongBench v2 are read ONLY by the sealed-side child (`decontam_g13.py sealedside`, its own process;
# counts and training-unit ids only). The parent never resolves, opens or lists these paths.
SEALED_SIDE = {"ohs3": ["lean:data/*ohs3*", "lean:data/ohs3_parts/**/*", "od:data/*ohs3*"],
               "ohs3_src": ["lean:ohs3/**/*", "ohs3hf:"],
               "longbench_v2": ["repo:bench/longbench_v2/**/*"]}
SIDE_NEVER = re.compile(r"(^|/)(sealed_nd|sealed_brief|prep89|_work|runs|results)(/|$)|(^|/)preds[^/]*(/|$)", re.I)
# A25 (c): against mixdev only the instance content is compared (state, options, group_id, structure hash of
# state + options); its instruction / card text is shared with training on purpose (same family templates).
MIXDEV_EVAL_FIELDS, MIXDEV_TRAIN_FIELDS = ("state", "options"), ("state", "option")
OUT = LEAN / "logs/decontam_counts"
COSINE = HERE / "g13_cosine_threshold.json"
EMB_DIR = Path.home() / ".cache/opendecide_ext/g13_emb"    # eval-side vectors only (EmbCache), never text
SIDE_EMB_DIR = Path.home() / ".cache/opendecide_ext/g13_emb_sealedside"   # A25 (d): the child's own vectors (SideCache)
FAMS = [f"F{i}" for i in range(1, 14)] + ["COMMIT"]
SEED_SETS = {"packs": "c_src/packs", "formats": "c_src/formats"}
FINAL_TRAIN = "data/c_parts/c_train_r1.jsonl"
SEALED_CHECK = LEAN / "sealed_nd/qc/sealed_check.py"     # RUN only, never opened (spec 7.1 v3, methods 6 P / 7)
SEALED_STRUCT_FIELDS = "state,card,instructions,options"  # the part-P structure check's fields (its --help example)
SEALED_KIND = {"keyword_hard": "sealed_keyword", "p_struct": "sealed_p_structure", "p_template": "sealed_p_structure"}
MIXDEV_GLOB = "c_src/*/out/mixdev_*.jsonl"
OPI_BUILDER = "build_opi.py"                               # OPI's five strategy strings (STRATS), read by ast only
TEMPLATE_SETS = ("dev_nc", "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims", "pg_dev", "devzs", "devp_card",
                 "dev", "eval_opi", "eval_jagged", "ohs", "ohs2")   # method 8 instruction sources (field read: instructions)
MIN_WORDS, NGRAM, TULU_N, TULU_FRAC = 5, 10, 8, 0.5
MH_N, MH_J, MH_EDIT, MH_PERM, MH_BANDS = 5, 0.8, 0.8, 100, 20
BATCH_WORDS = 400_000
DEV9 = ("dev_nc", "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims", "pg_dev", "devzs", "devp_card", "dev")
OHS_SRC_HF = ("HiTZ/This-is-not-a-dataset", "NortheasternUniversity/big_patent", "Paul/hatecheck",
              "TimSchopf/medical_abstracts", "coastalcph/lex_glue", "demelin/moral_stories",
              "google-research-datasets/go_emotions", "google-research-datasets/schema_guided_dstc8",
              "ibm-research/argument_quality_ranking_30k", "knowledgator/GLIClass-v1.0", "knowledgator/gliclass-v2.0",
              "knowledgator/gliclass-v3-logic-dataset", "nguha/legalbench", "qiaojin/PubMedQA",
              "tals/vitaminc", "tasksource/scone", "tasksource/zero-shot-label-nli")
OHS_SRC_LOCAL = ("ohs/_cache", "ohs/cache", "ohs2/arxiv_fresh_cache", "ohs2/science_cache")
DATA_EXT = {".jsonl", ".json", ".parquet", ".csv", ".tsv", ".txt", ".abst", ".xml", ".html", ".gz", ".zip", ".tgz"}
SEED_SKIP = re.compile(r"sealedqc|denylist|lint|manifest|report|check|verdict|summary|draw|gates|sidecar|qc_side", re.I)

# ---- input guard (spec 7.4 and the builder's never-open list) --------------------------------------------------------
NEVER = re.compile(r"ohs3|g13_emb_sealedside|(^|/)(prep89|sealed_nd|sealed_brief|longbench_v2|_work|runs|results)(/|$)|"
                   r"(^|/)preds[^/]*(/|$)", re.I)
JEV = re.compile(r"(^|[_/.-])jev", re.I)
JEV_ITEMS = ("bench/splits/", "bench/jevbench/datasets/public/", "bench/jevbench_v154/datasets/public/")
QUARANTINE_OK = ("bench/external_quarantine/ejs5/ejs5_rows.jsonl",
                 "bench/external_quarantine/decision_index/work/artifacts/benchmark-suite/release-v1-rebuilt/"
                 "selected-rows.jsonl")


def rel_of(p: Path) -> str:
    p = Path(p).absolute()
    for root in (REPO, HF, GH.parent):
        try:
            return p.relative_to(root).as_posix()
        except ValueError:
            continue
    return p.as_posix()


def allowed(p: Path) -> bool:
    """False for every path this program must never read (OHS-3, LongBench v2, sealed, preds, Jev outputs...)."""
    r = rel_of(p)
    if NEVER.search(r):
        return False
    if "external_quarantine/" in r and r not in QUARANTINE_OK:
        return False
    if JEV.search(r):
        return r.startswith(JEV_ITEMS) and r.endswith(".jsonl") and "/results/" not in r
    return True


# ---- text normalization and hashing ----------------------------------------------------------------------------------
_W = re.compile(r"[^\W_]+")
_SEG = re.compile(r"(?<=[.!?])\s+|\n+")
_VOC: dict = {}
M64 = np.uint64(0x100000001B3)


def words(t: str) -> list[str]:
    return _W.findall(unicodedata.normalize("NFKC", t).lower())


def hseq(ws) -> int:
    return int.from_bytes(hashlib.blake2b(" ".join(ws).encode(), digest_size=8).digest(), "little")


def wids(ws) -> np.ndarray:
    if len(_VOC) > 6_000_000:
        _VOC.clear()
    out = np.empty(len(ws), np.uint64)
    for i, w in enumerate(ws):
        v = _VOC.get(w)
        if v is None:
            v = _VOC[w] = int.from_bytes(hashlib.blake2b(w.encode(), digest_size=8).digest(), "little")
        out[i] = v
    return out


def _mix(h: np.ndarray) -> np.ndarray:
    with np.errstate(over="ignore"):
        h = h ^ (h >> np.uint64(30))
        h = h * np.uint64(0xBF58476D1CE4E5B9)
        h = h ^ (h >> np.uint64(27))
        h = h * np.uint64(0x94D049BB133111EB)
        return h ^ (h >> np.uint64(31))


def grams(cat: np.ndarray, lens: np.ndarray, n: int):
    """(hash, text index, position) of every word n-gram lying inside one text of the concatenation `cat`."""
    m = len(cat) - n + 1
    if m <= 0:
        return np.empty(0, np.uint64), np.empty(0, np.int64), np.empty(0, np.int64)
    h = np.zeros(m, np.uint64)
    with np.errstate(over="ignore"):
        for i in range(n):
            h = h * M64 + cat[i:i + m]
    starts = np.concatenate([[0], np.cumsum(lens)[:-1]]).astype(np.int64)
    tix = np.repeat(np.arange(len(lens)), lens)[:m]
    pos = np.arange(m) - starts[tix]
    ok = pos + n <= lens[tix]
    return _mix(h[ok]), tix[ok], pos[ok]


_RNG = np.random.default_rng(13)
PA = _RNG.integers(1, 2 ** 63, MH_PERM, dtype=np.uint64) | np.uint64(1)
PB = _RNG.integers(0, 2 ** 63, MH_PERM, dtype=np.uint64)
BC = _RNG.integers(1, 2 ** 63, MH_PERM // MH_BANDS, dtype=np.uint64) | np.uint64(1)


def minhash(h5: np.ndarray, t5: np.ndarray, n_texts: int) -> np.ndarray:
    sig = np.full((n_texts, MH_PERM), np.iinfo(np.uint64).max, np.uint64)
    if len(h5) == 0:
        return sig
    order = np.argsort(t5, kind="stable")
    h5, t5 = h5[order], t5[order]
    ut, first = np.unique(t5, return_index=True)
    step = max(1, min(MH_PERM, 4_000_000 // max(1, len(h5))))
    with np.errstate(over="ignore"):
        for c in range(0, MH_PERM, step):
            v = _mix(h5[:, None] * PA[None, c:c + step] + PB[None, c:c + step])
            sig[ut, c:c + step] = np.minimum.reduceat(v, first, axis=0)
    return sig


def band_keys(sig: np.ndarray) -> np.ndarray:
    r = MH_PERM // MH_BANDS
    out = np.zeros((len(sig), MH_BANDS), np.uint64)
    with np.errstate(over="ignore"):
        for b in range(MH_BANDS):
            k = np.full(len(sig), np.uint64(b + 1))
            for i in range(r):
                k = k * BC[i] + sig[:, b * r + i]
            out[:, b] = _mix(k)
    return out


def segments(raw: str) -> list[list[str]]:
    return [ws for ws in (words(s) for s in _SEG.split(raw)) if len(ws) >= MIN_WORDS]


def _thash(rows: list[list[str]]) -> int | None:
    """Method 9's one hash: normalized header (first row) + the set of every normalized cell (header included)."""
    rows = [[" ".join(words(str(c))) for c in r] for r in rows]
    if len(rows) < 2:
        return None
    cellset = sorted({c for r in rows for c in r if c})
    return hseq([json.dumps(rows[0]), json.dumps(cellset)])


def _pipe_cells(s: str) -> list[str]:
    # markdown '| a | b |' (one outer pipe off each end); pipe_plain 'a | b' (and '| b' = an empty first cell)
    return (s[1:-1] if len(s) >= 2 and s[0] == "|" and s[-1] == "|" else s).split("|")


def _pipe_tables(lines: list[str]) -> list[list[list[str]]]:
    """Runs of >= 2 consecutive lines with >= 1 '|' (markdown, and pipe_plain incl. 2 columns); separator rows off."""
    out, rows = [], []
    for line in lines + [""]:
        s = line.strip()
        if "|" in s:
            cells = _pipe_cells(s)
            if not all(set(c) <= set("-: ") for c in cells):
                rows.append(cells)
            continue
        if len(rows) >= 2:
            out.append(rows)
        rows = []
    return out


def _csv_tables(lines: list[str]) -> list[list[list[str]]]:
    """Runs of >= 2 consecutive comma lines with the same field count (>= 2), csv-quoted cells; the header is tried at
    the first 3 lines of a run (a title / caption line with a comma can join the run)."""
    out, run = [], []
    for line in lines + [""]:
        rec = None
        if "," in line:
            try:
                rec = next(csv.reader([line]))
            except (csv.Error, StopIteration):
                rec = None
        if rec is not None and len(rec) >= 2 and (not run or len(rec) == len(run[0])):
            run.append(rec)
            continue
        if len(run) >= 2:
            out += [run[k:] for k in range(min(3, len(run) - 1))]
        run = [rec] if rec is not None and len(rec) >= 2 else []
    return out


def _num_forms(v) -> list[str]:
    """A JSON scalar as cell text: as printed, and as public-2's fmt_num prints it (integer floats without '.0', at
    most 4 decimals), so a typed number matches either way."""
    if isinstance(v, bool) or v is None:
        return [str(v)]
    if isinstance(v, int):
        return [str(v)]
    if isinstance(v, float):
        a = repr(v)
        b = str(int(v)) if v.is_integer() else f"{v:.4f}".rstrip("0").rstrip(".")
        return [a] if a == b else [a, b]
    return [v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)]


def _json_tables(raw: str) -> list[list[list[str]]]:
    """JSON arrays of >= 1 record (objects with >= 2 keys; json_records): header = the first record's keys."""
    out, dec, pos = [], json.JSONDecoder(), 0
    for m in re.finditer(r"(?m)^[ \t]*\[", raw):
        if m.start() < pos:
            continue
        try:
            obj, end = dec.raw_decode(raw, m.end() - 1)
        except ValueError:
            continue
        pos = end
        if not (isinstance(obj, list) and obj and all(isinstance(r, dict) for r in obj) and len(obj[0]) >= 2):
            continue
        head = list(obj[0])
        for variant in (0, 1):
            rows = [head]
            for r in obj:
                rows.append([(lambda f: f[min(variant, len(f) - 1)])(_num_forms(r.get(h))) for h in head])
            out.append(rows)
    return out


_KV_LINE = re.compile(r"^([ \t]*)([^:\n]{1,200}?):(?:[ \t]+(.*?))?[ \t]*$")


def _kv_tables(lines: list[str]) -> list[list[list[str]]]:
    """key_value: runs of >= 2 consecutive 'key: value' lines at one indent = one record; records with the same keys
    (in order) form one table (header = the keys)."""
    recs, run, ind = [], [], None
    for line in lines + [""]:
        m = _KV_LINE.match(line) if line.strip() else None
        if m and (ind is None or m.group(1) == ind):
            run.append((m.group(2).strip(), m.group(3) or ""))
            ind = m.group(1)
            continue
        if len(run) >= 2:
            recs.append(run)
        run, ind = ([(m.group(2).strip(), m.group(3) or "")], m.group(1)) if m else ([], None)
    by: dict = {}
    for r in recs:
        by.setdefault(tuple(k for k, _ in r), []).append([v for _, v in r])
    return [[list(k)] + vs for k, vs in by.items()]


_HTML_TABLE = re.compile(r"<table\b[^>]*>(.*?)</table\s*>", re.I | re.S)
_HTML_TR = re.compile(r"<tr\b[^>]*>(.*?)</tr\s*>", re.I | re.S)
_HTML_CELL = re.compile(r"<t[hd]\b[^>]*>(.*?)</t[hd]\s*>", re.I | re.S)
_HTML_TAG = re.compile(r"<[^>]+>")


def _html_tables(raw: str) -> list[list[list[str]]]:
    import html as _html
    out = []
    for t in _HTML_TABLE.findall(raw):
        rows = [[_html.unescape(_HTML_TAG.sub(" ", c)) for c in _HTML_CELL.findall(tr)] for tr in _HTML_TR.findall(t)]
        rows = [r for r in rows if r]
        if len(rows) >= 2:
            out.append(rows)
    return out


def tables(raw: str) -> list[int]:
    """Method 9 (spec 7.2 9): normalized header + cell-set hash of every table in a text, in each container public-2
    renders (render.CONTAINERS: markdown, pipe_plain incl. 2 columns, csv, json_records, key_value, html); TabFact's
    '#' files come in as pipe text (csv_table_text). Titles: rows carry none. Extra candidate tables (a header tried
    at several lines, two number forms) only add hashes, so a real shared table is never missed."""
    if not raw:
        return []
    lines = raw.splitlines()
    found = _pipe_tables(lines)
    if "," in raw:
        found += _csv_tables(lines)
    if "[" in raw and "{" in raw:
        found += _json_tables(raw)
    if ":" in raw:
        found += _kv_tables(lines)
    if "<t" in raw.lower():
        found += _html_tables(raw)
    out, seen = [], set()
    for rows in found:
        h = _thash(rows)
        if h is not None and h not in seen:
            seen.add(h)
            out.append(h)
    return out


def csv_table_text(text: str, sep: str = "#") -> str:
    """A `sep`-delimited table file (TabFact all_csv: '#', header first) as pipe-table text, so tables() gives it the
    SAME header + cell-set hash as a pipe table with those cells (one table per file; no title, as training rows)."""
    out = []
    for line in text.splitlines():
        if line.strip():
            out.append("| " + " | ".join(c.replace("|", " ") for c in line.split(sep)) + " |")
    return "\n".join(out)


def member(sorted_arr: np.ndarray, x: np.ndarray) -> np.ndarray:
    """np.isin(x, sorted_arr) without re-sorting the (large, already sorted) training array on every call."""
    if len(sorted_arr) == 0 or len(x) == 0:
        return np.zeros(len(x), bool)
    i = np.minimum(np.searchsorted(sorted_arr, x), len(sorted_arr) - 1)
    return sorted_arr[i] == x


def edit_sim(a: np.ndarray, b: np.ndarray) -> float:
    return difflib.SequenceMatcher(None, a.tolist(), b.tolist(), autojunk=False).ratio()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 22), b""):
            h.update(blk)
    return h.hexdigest()


def jload(p: Path):
    try:
        return json.loads(Path(p).read_text())
    except Exception:  # noqa: BLE001
        return None


# ---- training side ---------------------------------------------------------------------------------------------------
def row_texts(r: dict) -> list[tuple[str, str]]:
    out = [("state", r.get("state")), ("instructions", r.get("instructions")), ("card", r.get("card"))]
    out += [("option", o) for o in (r.get("options") or [])]
    return [(f, t) for f, t in out if isinstance(t, str) and t.strip()]


_NAME = re.compile(r"[^\W\d_][^\W_]*|\d+")


def struct_g13(state, options) -> str | None:
    """Method 6, G13's own structure hash of the instance content (A25 c): state + options, NFKC, capitalised tokens
    (names) renamed N1, N2 ... in order of first use (state first, then options), lower case, options as a set."""
    if not isinstance(state, str) or not state.strip():
        return None
    names: dict = {}

    def norm(t: str) -> str:
        return " ".join(names.setdefault(w, f"N{len(names) + 1}") if w[0].isupper() else w.lower()
                        for w in _NAME.findall(unicodedata.normalize("NFKC", t)))

    s = norm(state)
    opts = sorted(norm(o) for o in (options or []) if isinstance(o, str))
    return hashlib.sha256(json.dumps([s, opts]).encode()).hexdigest()


def train_units(path: Path) -> list[dict]:
    """One unit per call_id (the mixer's training unit): every row id, the source, every model-visible text, and the
    instance keys method 6 compares (group_id, meta.structure_hash, G13's own state + options structure hash)."""
    units, at = [], {}
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            k = str(r.get("call_id") or r["id"])
            if k not in at:
                at[k] = len(units)
                units.append({"key": k, "rows": [], "source": str(r.get("source") or "?"), "seed": False,
                              "texts": [], "struct": set(), "groups": set(), "s_g13": set()})
            u = units[at[k]]
            u["rows"].append(str(r["id"]))
            u["texts"] += row_texts(r)
            sh = (r.get("meta") or {}).get("structure_hash") if isinstance(r.get("meta"), dict) else None
            if isinstance(sh, str) and sh:
                u["struct"].add(sh)
            if r.get("group_id") not in (None, ""):
                u["groups"].add(str(r["group_id"]))
            sg = struct_g13(r.get("state"), r.get("options"))
            if sg:
                u["s_g13"].add(sg)
    return units


def _edge_leaf(n, right: bool):
    """The node whose text ends (right) / starts (left) an expression joined by `+` (through `+` chains and f-strings)."""
    while True:
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):
            n = n.right if right else n.left
        elif isinstance(n, ast.JoinedStr) and n.values:
            n = n.values[-1] if right else n.values[0]
        else:
            return n


def py_literals_at(src: str, marked: bool = False) -> list[tuple]:
    """(literal, line) of every string literal of a generator file (f-string parts included), docstrings excluded.
    marked=True: (literal, line, render_text), where render_text is the literal with "{}" put at each edge that a
    runtime value joins with no gap in the code (an f-string value next to an f-string part; a `+` / `+=` operand), so
    the A31 (b) render check (seed_pieces) drops the edge word that touches it (A32 c)."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []
    docs, edge = set(), {}
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.body:
            b = n.body[0]
            if isinstance(b, ast.Expr) and isinstance(getattr(b, "value", None), ast.Constant):
                docs.add(id(b.value))
        if marked:
            if isinstance(n, ast.JoinedStr):
                vs = n.values
                for i, v in enumerate(vs):
                    if isinstance(v, ast.Constant):
                        lr = edge.setdefault(id(v), [False, False])
                        lr[0] |= i > 0 and not isinstance(vs[i - 1], ast.Constant)
                        lr[1] |= i + 1 < len(vs) and not isinstance(vs[i + 1], ast.Constant)
            elif isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):
                edge.setdefault(id(_edge_leaf(n.left, True)), [False, False])[1] = True
                edge.setdefault(id(_edge_leaf(n.right, False)), [False, False])[0] = True
            elif isinstance(n, ast.AugAssign) and isinstance(n.op, ast.Add):
                edge.setdefault(id(_edge_leaf(n.value, False)), [False, False])[0] = True
    out = [(n, getattr(n, "lineno", 0)) for n in ast.walk(tree)
           if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs]
    if not marked:
        return [(n.value, ln) for n, ln in out]
    return [(n.value, ln, "{}" * edge.get(id(n), (0, 0))[0] + n.value + "{}" * edge.get(id(n), (0, 0))[1])
            for n, ln in out]


def py_literals(src: str) -> list[str]:
    """String literals of a generator file (f-string parts included), docstrings excluded."""
    return [t for t, _ in py_literals_at(src)]


# A31 (c): public-data records (formats-2 XED / MAMS / GHC / EDOS records) are INSTANCE text: methods 1-7 check them
# as rows (their hits bind; they never get the A31 (b) render exemption) and the template -> eval direction
# (templates_rev, Claude-written seeds and templates only) skips them.
PUBLIC_RECORDS = re.compile(r"^c_src/formats/formats-2/records/[^/]+\.jsonl$")


def _seed_texts(p: Path) -> list[tuple[str, int, str]]:
    """(text, line, render_text) of a seed file, in the order seed_units always used (line = the file line of the
    literal / record; 0 for a .json file; render_text: see py_literals_at(marked=True), the text itself for records)."""
    if p.suffix == ".py":
        return py_literals_at(p.read_text(errors="replace"), marked=True)
    if p.suffix in (".jsonl", ".txt"):
        out = []
        for ln, line in enumerate(p.read_bytes().decode("utf-8", errors="replace").splitlines(), 1):
            if not line.strip():
                continue
            if p.suffix == ".txt":
                out.append((line, ln, line))
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            out += [(t, ln, t) for t in leaves(rec)]
        return out
    return [(t, 0, t) for rec in read_records(p, p.suffix, p.read_bytes()) for t in leaves(rec)]


def seed_units(root: Path, base: Path) -> tuple[list[dict], dict]:
    """Claude-written seeds, templates, packs and codebooks under `root` (spec 7.2): one unit per literal / record
    leaf. A31 (c): public-data records (PUBLIC_RECORDS) carry "public": True (instance text, see above)."""
    units, shas = [], {}
    if not root.exists():
        return units, shas
    for p in sorted(root.rglob("*")):
        parts = set(p.relative_to(root).parts[:-1])
        if not p.is_file() or parts & {"__pycache__", "tmp", "qc", "src", "out"} or SEED_SKIP.search(p.name):
            continue
        if p.suffix not in {".py", ".json", ".jsonl", ".txt"} or not allowed(p):
            continue
        rel = p.relative_to(base).as_posix()
        texts = [x for x in _seed_texts(p) if len(words(x[0])) >= 2]   # a single word is vocabulary
        if not texts:
            continue
        shas[rel] = sha256_file(p)
        pub = bool(PUBLIC_RECORDS.match(rel))
        for i, (t, ln, rt) in enumerate(texts):
            units.append({"key": f"seed:{rel}#{i}", "rows": [], "source": f"seed:{rel}", "seed": True,
                          "public": pub, "line": ln, "texts": [("seed", t)]})
            if rt != t:
                units[-1]["render_text"] = rt               # A32 (c): edges joined to a runtime value (seed_pieces)
    return units, shas


class TrainIndex:
    def __init__(self, units: list[dict]):
        self.units = units
        self.ids, self.occ, self.full, self.seg, self.tab = [], [], {}, defaultdict(set), defaultdict(set)
        self.raw, self.key = [], []        # first raw text and the text key (hseq) of every training text
        for ui, un in enumerate(units):
            for field, raw in un["texts"]:
                ws = words(raw)
                if not ws:
                    continue
                fh = hseq(ws)
                u = self.full.get(fh)
                if u is None:
                    u = self.full[fh] = len(self.ids)
                    self.ids.append(wids(ws))
                    self.occ.append([])
                    self.raw.append(raw)
                    self.key.append(fh)
                    for sw in segments(raw):
                        self.seg[hseq(sw)].add(u)
                for th in tables(raw):
                    self.tab[th].add(u)
                self.occ[u].append((ui, field))
        lens = np.array([len(x) for x in self.ids], np.int64)
        cat = np.concatenate(self.ids) if self.ids else np.empty(0, np.uint64)
        self.g = {}
        for n in (MH_N, TULU_N, NGRAM):
            h, t, p = grams(cat, lens, n)
            o = np.argsort(h, kind="stable")
            self.g[n] = (h[o], t[o], p[o], np.unique(h))
        h5, t5, _ = grams(cat, lens, MH_N)
        keys = band_keys(minhash(h5, t5, len(self.ids)))
        has = lens >= MH_N
        bk = keys[has].ravel()
        bt = np.repeat(np.nonzero(has)[0], MH_BANDS)
        o = np.argsort(bk, kind="stable")
        self.bk, self.bt = bk[o], bt[o]
        self._g5 = {}

    def g5set(self, u: int) -> np.ndarray:
        s = self._g5.get(u)
        if s is None:
            ids = self.ids[u]
            s = np.unique(grams(ids, np.array([len(ids)]), MH_N)[0])
            if len(self._g5) > 50_000:
                self._g5.clear()
            self._g5[u] = s
        return s

    def lookup(self, n: int, h: np.ndarray):
        """For gram hashes h: (index into h, training text) for every occurrence (+ position)."""
        H, T, P, _ = self.g[n]
        lo, hi = np.searchsorted(H, h, "left"), np.searchsorted(H, h, "right")
        cnt = hi - lo
        qi = np.repeat(np.arange(len(h)), cnt)
        idx = np.repeat(lo, cnt) + (np.arange(cnt.sum()) - np.repeat(np.cumsum(cnt) - cnt, cnt))
        return qi, T[idx], P[idx]


# ---- eval side -------------------------------------------------------------------------------------------------------
def leaves(x, fields=None):
    """Model-visible string leaves of an eval record; keys starting with 'jev' are never read (spec 7.4)."""
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for k, v in x.items():
            if str(k).lower().startswith("jev") or (fields is not None and k not in fields):
                continue
            yield from leaves(v)
    elif isinstance(x, list):
        if x and all(isinstance(v, str) for v in x) and sum(len(v.split()) for v in x) <= 2 * len(x) and len(x) > 2:
            yield " ".join(x)                 # a token list (HateXplain post_tokens)
        else:
            for v in x:
                yield from leaves(v)


def read_records(p: Path, ext: str, data: bytes):
    """Records of one data file (or archive member). xml/html: tags stripped, one text per file."""
    name = p.name.lower()
    if ext == ".gz" or name.endswith((".tar.gz", ".tgz")):
        if name.endswith((".tar.gz", ".tgz")):
            with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
                for m in tf.getmembers():
                    if m.isfile():
                        sub = Path(m.name)
                        if sub.suffix in DATA_EXT and sub.suffix not in {".gz", ".zip"}:
                            yield from read_records(sub, sub.suffix, tf.extractfile(m).read())
            return
        inner = Path(name[:-3])
        yield from read_records(inner, inner.suffix, gzip.decompress(data))
        return
    if ext == ".zip":
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            for m in zf.namelist():
                sub = Path(m)
                if sub.suffix in DATA_EXT and sub.suffix not in {".zip"} and not m.endswith("/"):
                    yield from read_records(sub, sub.suffix, zf.read(m))
        return
    text = data.decode("utf-8", errors="replace")
    if ext == ".jsonl":
        for line in text.splitlines():
            if line.strip():
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
    elif ext == ".json":
        try:
            d = json.loads(text)
        except json.JSONDecodeError:
            return
        if isinstance(d, list):
            yield from d
        elif isinstance(d, dict):
            big = [v for v in d.values() if isinstance(v, list) and v and isinstance(v[0], dict)]
            if big:
                for v in big:
                    yield from v
            else:
                yield d
    elif ext in (".csv", ".tsv"):
        csv.field_size_limit(sys.maxsize)
        yield from csv.DictReader(io.StringIO(text), delimiter="\t" if ext == ".tsv" else ",")
    elif ext in (".xml", ".html"):
        yield re.sub(r"<[^>]+>", "\n", text)
    elif ext == ".abst":
        yield text
    elif ext == ".txt":
        for line in text.splitlines():
            if line.strip():
                yield line


def parquet_records(p: Path, fields=None):
    import pyarrow as pa
    import pyarrow.parquet as pq
    pa.set_cpu_count(2)
    pa.set_io_thread_count(2)
    pf = pq.ParquetFile(p)
    cols = [c for c in pf.schema_arrow.names if fields is None or c in fields]
    for b in pf.iter_batches(batch_size=2048, columns=cols or None):
        yield from b.to_pylist()


def target(name, paths, kind="rows", fields=None, methods="all", blind=False, tables=False, sublabel=None,
           status=None, note="", csv_sep=None, train_fields=None, gap=None, main_only=False):
    """train_fields: the training-text fields a hit may come from (A25 c, mixdev); None = every field.
    gap: a coverage gap that keeps the log incomplete (stated in incomplete_why)."""
    return {"name": name, "paths": list(paths), "kind": kind, "fields": fields, "methods": methods, "blind": blind,
            "tables": tables, "sublabel": sublabel, "status": status, "note": note, "csv_sep": csv_sep,
            "train_fields": tuple(train_fields) if train_fields else None, "gap": gap, "main_only": main_only}


BIGPAT_RULING_MARK = "G13-BIGPAT-RULING"


def bigpat_ruling() -> str | None:
    """The orchestrator's written big_patent ruling, if any: env G13_BIGPAT_RULING=<tag> counts only when
    PREREG_FINAL.md holds a line with 'G13-BIGPAT-RULING <tag>' (an amendment written before the run). This tool never
    writes that line; without it the gap stays and the log stays incomplete."""
    tag = (os.environ.get("G13_BIGPAT_RULING") or "").strip()
    if not tag or not re.fullmatch(r"[A-Za-z0-9._-]{1,40}", tag):
        return None
    try:
        txt = (LEAN / "PREREG_FINAL.md").read_text(errors="replace")
    except OSError:
        return None
    return tag if re.search(rf"(?m){re.escape(BIGPAT_RULING_MARK)}\s+{re.escape(tag)}\b", txt) else None


def targets() -> list[dict]:
    """Spec 7.1, in order. `status` set here = not read by this program (the reason is in `note`)."""
    t = [target(f"dev:{s}", [f"lean:data/{s}.jsonl"]) for s in DEV9]
    t.append(target("mixdev", ["lean:" + MIXDEV_GLOB], fields=MIXDEV_EVAL_FIELDS, train_fields=MIXDEV_TRAIN_FIELDS,
                    main_only=True,
                    note="A25 (c): instance content only, both sides (eval state + options vs training state + "
                         "options; group_id and the state + options structure hash in mixdev_structure); every "
                         "method"))
    t.append(target("jevbench_public", ["repo:bench/splits/jevbench_*.jsonl", "repo:bench/jevbench/datasets/public/*.jsonl"],
                    kind="generic", note="item files only (spec 7.4 exception)"))
    t.append(target("jevbench_v154", ["repo:bench/jevbench_v154/datasets/public/*.jsonl"], kind="generic",
                    note="item files only"))
    t.append(target("btzsc", ["hf:btzsc/btzsc"]))
    for s in ("eval_opi", "eval_jagged"):
        t.append(target(s, [f"lean:data/{s}.jsonl"], fields=("state", "instructions", "options")))
    t.append(target("ohs1", ["lean:data/ohs.jsonl"], blind=True))
    t.append(target("ohs2", ["lean:data/ohs2.jsonl"], blind=True, tables=True))
    for r in OHS_SRC_HF:
        sub = {"names": "lean:golden_src/forbidden_label_nli.json", "label": "forbidden152"} \
            if r == "tasksource/zero-shot-label-nli" else None
        if r == BIGPAT:
            stream_on = os.environ.get("G13_BIGPAT_STREAM") == "1"
            ruled = None if stream_on else bigpat_ruling()
            t.append(target(f"ohs_src:{r}", [f"proj:{r}"] + ([f"hfstream:{r}|{BIGPAT_REST}"] if stream_on else []),
                            blind=True, fields=("abstract", "description"),
                            note="'all' config (= union of a..y): abstract of every split + test descriptions "
                                 "(fetched column-projected by `decontam_g13.py fetch`)"
                                 + ("; train / validation descriptions streamed" if stream_on else "")
                                 + (f"; train / validation descriptions NOT scanned under the written ruling "
                                    f"'{BIGPAT_RULING_MARK} {ruled}' in PREREG_FINAL.md" if ruled else ""),
                            gap=None if (stream_on or ruled) else
                            f"ohs_src:{r}: train / validation descriptions (16.2 GB) not scanned (over the ~2 GB "
                            "free-download cap; abstracts of every split and the test descriptions were scanned); "
                            "re-run with G13_BIGPAT_STREAM=1 or rule (G13_BIGPAT_RULING=<tag>, with the line "
                            f"'{BIGPAT_RULING_MARK} <tag>' in PREREG_FINAL.md)"))
            continue
        t.append(target(f"ohs_src:{r}", [f"hf:{r}"], blind=True, sublabel=sub))
    for d in OHS_SRC_LOCAL:
        t.append(target(f"ohs_src:{d}", [f"lean:{d}/**/*"], blind=True))
    t.append(target("tabfact_tables", ["gh:wenhuchen/Table-Fact-Checking"], blind=True, tables=True, csv_sep="#",
                    methods=("table",), kind="tables",
                    note="all TabFact tables (data/all_csv, '#'-delimited; header + cell-set hash = the pipe-table hash; "
                         "exact / segment / substring also run on the table text)"))
    t.append(target("hatexplain", ["hf:Hate-speech-CNERG/hatexplain"], fields=("post_tokens",),
                    methods=("exact", "substring")))
    t.append(target("sbf", ["hf:allenai/social_bias_frames"], fields=("post",), methods=("exact", "substring")))
    t.append(target("ejs5", ["repo:" + QUARANTINE_OK[0]], blind=True))
    t.append(target("di_test", ["repo:" + QUARANTINE_OK[1]], blind=True))
    for lb in SEALED_SIDE:
        t.append(target(lb, [], kind="sealed_side", blind=True, tables=True,
                        note="A25 (d): read only by the sealed-side child process (`decontam_g13.py sealedside`; "
                             "counts and training-unit ids only; methods 1-5 + tables); the parent never opens or "
                             "lists these files"))
    t.append(target("mixdev_structure", ["lean:" + MIXDEV_GLOB], kind="structure",
                    note="method 6 vs the mix-tuning dev (A25 c): structure_g13 = G13's own hash of state + options "
                         "with names abstracted (capitalised tokens renamed in order of first use, options as a set); "
                         "structure = the generator's meta.structure_hash (canonical problem); group_id = shared "
                         "group_id"))
    t.append(target("templates_m8", ["lean:" + OPI_BUILDER, "lean:data/eval_jagged.jsonl"], kind="templates",
                    note="method 8 (A25 e): OPI's strategy strings (build_opi.STRATS, placeholders removed, per line) "
                         "and jagged's injected line (state.editor_note), >= 2 words, each as a normalized word "
                         "sequence anywhere in a unit's texts (word boundaries)"))
    t.append(target("templates_instr", [f"lean:data/{s}.jsonl" for s in TEMPLATE_SETS], kind="instr",
                    fields=("instructions",), methods=("exact", "substring"), blind=True,
                    note="method 8 (A25 e): every dev / eval instruction template (the 9 dev splits, eval_opi, "
                         "eval_jagged, OHS-1/2; field read: instructions only), whole and each sentence / line, "
                         ">= 5 words, as a substring of any unit text (plus exact full / sentence matches)"))
    t.append(target("templates_rev", [f"lean:data/{s}.jsonl" for s in TEMPLATE_SETS] +
                    ["lean:" + OPI_BUILDER, "lean:data/eval_jagged.jsonl"], kind="templates_rev", blind=True,
                    note="method 8, other direction (spec 7.2 8): a Claude-written template piece (seed literal "
                         "split at placeholders / lines, whole and per sentence) must not EQUAL a dev / eval "
                         "instruction sentence / line or an OPI / jagged wording (>= 3 words) nor be CONTAINED in one "
                         "(5-9 words); seeds only (hits make seeds_clean false); 2-word equalities and 3-4-word "
                         "containments are counted report-only"))
    t.append(target("sealed_suite", [], kind="sealed_check", blind=True,
                    note="sealed_nd/qc/sealed_check.py RUN only (its own process): method 6 vs part P (p_struct, "
                         "p_template; --structure-fields " + SEALED_STRUCT_FIELDS + "), method 7 (keyword_hard) and "
                         "its 12/10-gram, line, sentence and context checks; ids and hit kinds only"))
    return t


def resolve(spec: str) -> list[Path]:
    kind, _, rest = spec.partition(":")
    if kind == "lean":
        base, pat = LEAN, rest
    elif kind == "repo":
        base, pat = REPO, rest
    elif kind == "od":                       # opendecide-data/
        base, pat = LEAN.parent, rest
    elif kind == "hf":
        snaps = HF / ("datasets--" + rest.replace("/", "--")) / "snapshots"
        base, pat = snaps, "*/**/*"
    elif kind == "proj":                     # column-projected copies written by `fetch` (complete files only)
        base, pat = PROJ / rest.replace("/", "--"), "**/*.parquet"
    elif kind == "hfstream":                 # remote parquet list only; stream() fetches one file at a time
        repo, _, rx = rest.partition("|")
        try:
            from huggingface_hub import HfApi
            fs = HfApi().list_repo_files(repo, repo_type="dataset")
        except Exception:  # noqa: BLE001
            return []
        return [STREAM_ROOT / repo / f for f in sorted(fs) if f.endswith(".parquet") and (not rx or re.search(rx, f))]
    elif kind == "gh":
        base, pat = GH / rest.replace("/", "--"), GH_PAT.get(rest, "**/*")
    elif kind == "abs":
        p = Path(rest)
        base, pat = p.parent, p.name
    else:
        return []
    if not base.exists():
        return []
    seen, out = set(), []
    for p in sorted(base.glob(pat)):
        if not p.is_file() or p.name.lower().startswith(("readme", "license", ".git")) or p.suffix == ".md":
            continue
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            out.append(p)
    return out


# ---- methods 6 (structure hash), 7 (sealed keywords), 8 (templates) ---------------------------------------------------
def note_sha(shas: dict, f: Path) -> None:
    """Record an eval input's sha; a file read twice in one run with different contents (another lane rewrote it
    mid-run) is recorded as changed, so the stale check flags the log."""
    k, h = rel_of(f), sha256_file(f)
    if k in shas and shas[k] != h:
        h = "changed-during-run"
    shas[k] = h


def mixdev_files() -> list[Path]:
    """The main mixdev files (mixdev_S5.jsonl), not their .sidecar / .sealedqc / .relations / .gates companions."""
    return [f for f in sorted(LEAN.glob(MIXDEV_GLOB)) if allowed(f) and f.name.count(".") == 1]


def mixdev_structs(shas: dict | None = None) -> tuple[dict, int, int]:
    """Method 6 keys of every mix-tuning-dev item (A25 c, instance content only): {"structure": meta.structure_hash,
    "structure_g13": struct_g13(state, options), "group_id": group_id} as sets; plus item and file counts."""
    ks, items, files = {"structure": set(), "structure_g13": set(), "group_id": set()}, 0, 0
    for f in mixdev_files():
        files += 1
        if shas is not None:
            note_sha(shas, f)
        with open(f) as fh:
            for line in fh:
                if not line.strip():
                    continue
                r = json.loads(line)
                items += 1
                m = r.get("meta") if isinstance(r.get("meta"), dict) else {}
                if isinstance(m.get("structure_hash"), str) and m["structure_hash"]:
                    ks["structure"].add(m["structure_hash"])
                sg = struct_g13(r.get("state"), r.get("options"))
                if sg:
                    ks["structure_g13"].add(sg)
                if r.get("group_id") not in (None, ""):
                    ks["group_id"].add(str(r["group_id"]))
    return ks, items, files


def template_strings(shas: dict | None = None) -> list[tuple[str, ...]]:
    """Method 8 eval wordings: OPI's strategy strings (build_opi.STRATS literal text, placeholders removed, one per
    line) and jagged's injected line(s) (the editor_note of eval_jagged's state; state is the only field read)."""
    out = set()
    if shas is not None:
        for f in (LEAN / OPI_BUILDER, LEAN / "data/eval_jagged.jsonl"):
            if f.exists():
                note_sha(shas, f)
    try:
        tree = ast.parse((LEAN / OPI_BUILDER).read_text())
        for n in ast.walk(tree):
            if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "STRATS" for t in n.targets):
                for v in ast.literal_eval(n.value).values():
                    for part in re.split(r"\{[a-z]\}|\n", v):
                        ws = tuple(words(part))
                        if len(ws) >= 2:
                            out.add(ws)
    except (OSError, SyntaxError, ValueError):
        pass
    jf = LEAN / "data/eval_jagged.jsonl"
    if jf.exists():
        with open(jf) as fh:
            for line in fh:
                st = json.loads(line).get("state") if line.strip() else None
                try:
                    d = json.loads(st) if isinstance(st, str) else st
                except json.JSONDecodeError:
                    d = None
                if isinstance(d, dict) and isinstance(d.get("editor_note"), str):
                    ws = tuple(words(d["editor_note"]))
                    if len(ws) >= 2:
                        out.add(ws)
    return sorted(out)


def instr_wordings(shas: dict | None = None) -> set:
    """Method 8, other direction (eval side): every dev / eval instruction (TEMPLATE_SETS, field `instructions` only,
    read by program) whole and per sentence / line, plus OPI's strategy strings and jagged's injected line, as
    normalized word tuples of >= 2 words. Never printed."""
    W = set()
    for s_ in TEMPLATE_SETS:
        f = LEAN / f"data/{s_}.jsonl"
        if not f.exists() or not allowed(f):
            continue
        if shas is not None:
            note_sha(shas, f)
        with open(f) as fh:
            for line in fh:
                ins = json.loads(line).get("instructions") if line.strip() else None
                if not isinstance(ins, str) or not ins.strip():
                    continue
                for t in [ins] + [x for x in _SEG.split(ins) if x.strip()]:
                    ws = tuple(words(t))
                    if len(ws) >= 2:
                        W.add(ws)
    W.update(template_strings(shas))
    return W


_PLACEHOLDER = re.compile(r"\{[^{}]*\}|\n")


def template_rev_hits(units: list[dict], W: set) -> tuple[dict, dict]:
    """Method 8, other direction, on seed units (Claude-written templates), each literal split at placeholders / lines,
    whole and per sentence. BINDING ({ui: fields}): a piece of >= 3 words EQUAL to a dev / eval wording in W, or a
    piece of 5-9 words CONTAINED in one (word boundaries). Report-only counts (a ruling may make them bind): 2-word
    equalities and 3-4-word containments (generic phrases such as 'is it true that'). A31 (c): these thresholds bind;
    Claude-written seeds / templates only (public-data records, u["public"], are instance text: methods 1-7)."""
    grams = {ws[i:i + n] for ws in W for n in range(3, 10) for i in range(len(ws) - n + 1)}
    hit, rep = defaultdict(set), Counter()
    for ui, u in enumerate(units):
        if not u["seed"] or u.get("public"):
            continue
        for f, raw in u["texts"]:
            pieces = {tuple(words(x)) for part in _PLACEHOLDER.split(raw)
                      for x in [part] + [y for y in _SEG.split(part) if y.strip()]}
            for ws in pieces:
                n = len(ws)
                if n < 2:
                    continue
                if ws in W:
                    if n >= 3:
                        hit[ui].add(f)
                    else:
                        rep["exact_2w_report_only"] += 1
                elif 3 <= n <= 9 and ws in grams:
                    if n >= 5:
                        hit[ui].add(f)
                    else:
                        rep["contained_3_4w_report_only"] += 1
    return hit, {k: rep.get(k, 0) for k in ("exact_2w_report_only", "contained_3_4w_report_only")}


def template_hits(units: list[dict], tmpls: list[tuple[str, ...]]) -> dict:
    """ui -> fields where a template's normalized word sequence occurs (word boundaries, any length >= 2 words)."""
    pats = [" " + " ".join(t) + " " for t in tmpls]
    hit = defaultdict(set)
    for ui, u in enumerate(units):
        for f, raw in u["texts"]:
            j = " " + " ".join(words(raw)) + " "
            if any(pt in j for pt in pats):
                hit[ui].add(f)
    return hit


def sealed_hits(units: list[dict], train_path: Path | None, py: str = sys.executable,
                checker: Path = SEALED_CHECK) -> tuple[dict, dict]:
    """RUN (never open) the sealed checker in its own process on the training rows (or the seed literals) with the
    part-P structure fields; read only its id / hit-kind output. Returns ({method: {ui}}, record)."""
    rec = {"checker": "sealed_nd/qc/sealed_check.py (run only)", "structure_fields": SEALED_STRUCT_FIELDS}
    if not checker.exists():
        rec["status"] = "missing"
        return {}, rec
    row_ui = {r: ui for ui, u in enumerate(units) for r in (u["rows"] if not u["seed"] else [f"seed:{ui}"])}
    with tempfile.TemporaryDirectory(dir=str(HERE / "tmp") if (HERE / "tmp").is_dir() else None) as td:
        src = train_path
        if any(u["seed"] for u in units):       # seed literals as rows; the training file's rows appended as they are
            src = Path(td) / "units.jsonl"
            with open(src, "w") as f:
                for ui, u in enumerate(units):
                    if u["seed"]:
                        f.write(json.dumps({"id": f"seed:{ui}", "state": "\n".join(t for _, t in u["texts"])}) + "\n")
                if train_path is not None:
                    with open(train_path) as g:
                        for line in g:
                            if line.strip():
                                f.write(line if line.endswith("\n") else line + "\n")
        if src is None:
            rec["status"] = "nothing to check"
            return {}, rec
        out, summ = Path(td) / "o.jsonl", Path(td) / "s.json"
        p = subprocess.run([py, str(checker), str(src), "--id-field", "id", "--structure-fields",
                            SEALED_STRUCT_FIELDS, "--out", str(out), "--summary", str(summ)],
                           capture_output=True, text=True, cwd=str(LEAN), timeout=7200)
        sm = jload(summ) or {}
        rec.update(exit=p.returncode, rows=sm.get("rows"), rows_hit=sm.get("rows_hit"),
                   suite_sha256=sm.get("suite_sha256"), checker_sha256=sm.get("checker_sha256"))
        hits = defaultdict(set)
        if p.returncode == 0 and out.exists():
            with open(out) as fh:
                for line in fh:
                    r = json.loads(line)
                    if not r.get("hit"):
                        continue
                    ui = row_ui.get(str(r.get("id")))
                    kinds = [k.get("kind") if isinstance(k, dict) else k for k in (r.get("hit_kinds") or [])]
                    for k in kinds or ["?"]:
                        hits[SEALED_KIND.get(k, "sealed_text")].add(ui)
        rec["status"] = "scanned" if p.returncode == 0 and sm else "failed"
    return {m: {u for u in us if u is not None} for m, us in hits.items()}, rec


# ---- the scan --------------------------------------------------------------------------------------------------------
class Scan:
    """The text scan of one training index. `owner[ui]` names the set of each unit (several sets in one eval pass;
    an eval item counts for a set when one of its hit training texts occurs in a unit of that set, as in a lone run).
    The embedding method's top-5 is per set: its hits come back as method "embed@<set>"."""

    def __init__(self, idx: TrainIndex, embed=None, owner: list | None = None, defer: bool = False):
        self.idx, self.embed = idx, embed
        # defer=True (the parent): method 5 runs after the scan from the EmbCache (embed_pass); the scan only notes the
        # key and item of every text the method sees. embed=Embed (the sealed-side child): live, inside flush().
        self.defer = defer
        self.ek = defaultdict(lambda: array.array("Q"))    # label -> text keys
        self.ei = defaultdict(lambda: array.array("q"))    # label -> eval item number of each key
        self.owner = owner if owner is not None else [""] * len(idx.units)
        self.hits = defaultdict(lambda: defaultdict(set))      # label -> method -> training texts
        self.items_hit = defaultdict(lambda: defaultdict(set))  # label -> method -> eval item numbers
        self.items_by = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))   # set -> label -> method -> items
        self._own: dict = {}
        self.items, self.short, self.sub_rows = Counter(), Counter(), Counter()
        self.cache: dict = {}
        self.q: list = []          # (cache key, ws, raw, methods, tables)
        self.q_words = 0
        self.waiting = defaultdict(list)   # cache key -> [(labels, item)]

    def add_item(self, labels: tuple, texts: list[tuple[str, bool]], methods, want_tables: bool) -> None:
        """texts: (raw, is_content). Texts of >= 5 words get every method of the target; a CONTENT text under 5 words
        gets the exact full-text hash only (exact_short); other short texts (labels, options) are not items."""
        item = self.items[labels[0]]
        for lb in labels:
            self.items[lb] += 1
        tw = [(raw, ws, c) for raw, c in texts for ws in [words(raw)] if ws]
        if not any(c and len(ws) >= MIN_WORDS for _, ws, c in tw):
            for lb in labels:
                self.short[lb] += 1
        mkey = methods if isinstance(methods, str) else ",".join(methods)
        for raw, ws, c in tw:
            short = len(ws) < MIN_WORDS
            if short and not c:
                continue
            key = (hseq(ws), mkey, short, want_tables)
            if self.defer and not short and methods == "all":
                for lb in labels:
                    self.ek[lb].append(key[0])
                    self.ei[lb].append(item)
            if key in self.cache:
                self._credit(labels, item, self.cache[key])
                continue
            if key not in self.waiting:
                self.q.append((key, ws, raw, methods, want_tables, short))
                self.q_words += len(ws)
            self.waiting[key].append((labels, item))
        if self.q_words >= BATCH_WORDS:
            self.flush()

    def owners(self, u: int) -> frozenset:
        o = self._own.get(u)
        if o is None:
            o = self._own[u] = frozenset(self.owner[ui] for ui, _ in self.idx.occ[u])
        return o

    def _credit(self, labels, item, res) -> None:
        if not res:
            return
        for m, us in res.items():
            for lb in labels:
                self.hits[lb][m] |= us
                self.items_hit[lb][m].add(item)
            sets = {m[6:]} if m.startswith("embed@") else frozenset().union(*(self.owners(u) for u in us))
            for st in sets:
                for lb in labels:
                    self.items_by[st][lb][m].add(item)

    def flush(self) -> None:
        if not self.q:
            return
        idx, q = self.idx, self.q
        res = [defaultdict(set) for _ in q]
        for i, (key, ws, raw, methods, want_tables, short) in enumerate(q):
            u = idx.full.get(key[0])
            if short:
                if u is not None:
                    res[i]["exact_short"].add(u)
                continue
            if u is not None:
                res[i]["exact_full"].add(u)
            for sw in segments(raw):
                us = idx.seg.get(hseq(sw))
                if us:
                    res[i]["exact_seg"] |= us
            if want_tables:
                for th in tables(raw):
                    res[i]["table"] |= idx.tab.get(th, set())
        full = [i for i, x in enumerate(q) if not x[5]]
        allm = [i for i in full if q[i][3] == "all"]
        self.arrs = {i: wids(q[i][1]) for i in full}
        if full:
            self._substring(full, res)
        if allm:
            self._ngrams(allm, res)
            if self.embed is not None:
                self.embed.scan([q[i][0][0] for i in allm], [q[i][2] for i in allm], [res[i] for i in allm])
        for i, (key, *_r) in enumerate(q):
            r = {m: frozenset(v) for m, v in res[i].items() if v}
            if len(self.cache) > 2_000_000:
                self.cache.clear()
            self.cache[key] = r
            for labels, item in self.waiting.pop(key, []):
                self._credit(labels, item, r)
        self.q, self.q_words = [], 0

    def _cat(self, sel):
        arrs = [self.arrs[i] for i in sel]
        lens = np.array([len(a) for a in arrs], np.int64)
        return arrs, lens, np.concatenate(arrs)

    def _substring(self, sel, res) -> None:
        idx = self.idx
        arrs, lens, cat = self._cat(sel)
        h5, t5, p5 = grams(cat, lens, MH_N)
        present = member(idx.g[MH_N][3], h5)
        n_all = np.bincount(t5, minlength=len(sel))
        n_ok = np.bincount(t5[present], minlength=len(sel))
        H = idx.g[MH_N][0]
        for k in np.nonzero((n_all > 0) & (n_all == n_ok))[0].tolist():
            lo, hi = np.searchsorted(t5, k, "left"), np.searchsorted(t5, k, "right")
            hk, pk = h5[lo:hi], p5[lo:hi]
            cnt = np.searchsorted(H, hk, "right") - np.searchsorted(H, hk, "left")
            j = int(np.argmin(cnt))
            qi, tt, pp = idx.lookup(MH_N, hk[j:j + 1])
            e = arrs[k]
            for t, p in zip(tt.tolist(), pp.tolist()):
                s = p - int(pk[j])
                ids = idx.ids[t]
                if s >= 0 and s + len(e) <= len(ids) and np.array_equal(ids[s:s + len(e)], e):
                    res[sel[k]]["substring"].add(t)

    def _ngrams(self, sel, res) -> None:
        idx = self.idx
        arrs, lens, cat = self._cat(sel)
        # ngram10
        h, t, _ = grams(cat, lens, NGRAM)
        m = member(idx.g[NGRAM][3], h)
        if m.any():
            qi, tt, _ = idx.lookup(NGRAM, h[m])
            for k, u in set(zip(t[m][qi].tolist(), tt.tolist())):
                res[sel[k]]["ngram10"].add(u)
        # tulu8: > 50% of the eval text's tokens inside 8-grams shared with one training text
        h, t, p = grams(cat, lens, TULU_N)
        m = member(idx.g[TULU_N][3], h)
        if m.any():
            for k in np.unique(t[m]).tolist():
                lo, hi = np.searchsorted(t, k, "left"), np.searchsorted(t, k, "right")
                mk = np.zeros(len(t), bool)
                mk[lo:hi] = m[lo:hi]
                pos = p[mk]
                cov = np.zeros(lens[k], bool)
                for j in pos.tolist():
                    cov[j:j + TULU_N] = True
                if cov.sum() <= TULU_FRAC * lens[k]:
                    continue                    # even the union of every shared 8-gram is not enough
                qi, tt, _ = idx.lookup(TULU_N, h[mk])
                by = defaultdict(set)
                for a, u in zip(qi.tolist(), tt.tolist()):
                    by[u].add(int(pos[a]))
                for u, js in by.items():
                    c = np.zeros(lens[k], bool)
                    for j in js:
                        c[j:j + TULU_N] = True
                    if c.sum() > TULU_FRAC * lens[k]:
                        res[sel[k]]["tulu8"].add(u)
        # minhash on word 5-grams, confirmed by exact Jaccard and edit similarity
        h5, t5, _ = grams(cat, lens, MH_N)
        keys = band_keys(minhash(h5, t5, len(sel)))
        has = lens >= MH_N
        flat = keys.ravel()
        hit = member(idx.bk, flat) & np.repeat(has, MH_BANDS)
        if hit.any():
            cand = set()
            for f in np.nonzero(hit)[0].tolist():
                k = f // MH_BANDS
                lo, hi = np.searchsorted(idx.bk, flat[f], "left"), np.searchsorted(idx.bk, flat[f], "right")
                cand |= {(k, int(u)) for u in idx.bt[lo:hi]}
            for k, u in cand:
                if u in res[sel[k]]["minhash"]:
                    continue
                lo, hi = np.searchsorted(t5, k, "left"), np.searchsorted(t5, k, "right")
                a = np.unique(h5[lo:hi])
                b = idx.g5set(u)
                inter = len(np.intersect1d(a, b, assume_unique=True))
                if inter / (len(a) + len(b) - inter) >= MH_J and edit_sim(arrs[k], idx.ids[u]) >= MH_EDIT:
                    res[sel[k]]["minhash"].add(u)


class Encoder:
    """The method-5 embedder exactly as g13_cosine_threshold.json fixes it: model, max_seq_length, dtype (fp16 on the
    GPU), L2-normalised. Vectors are returned as float16 (the cache's storage type) and compared in float32."""

    def __init__(self, cfg: dict):
        import torch
        from sentence_transformers import SentenceTransformer
        torch.set_num_threads(2)
        self.dev = "mps" if torch.backends.mps.is_available() else "cpu"
        self.m = SentenceTransformer(cfg["model"], device=self.dev)
        if cfg.get("max_seq_length"):
            self.m.max_seq_length = int(cfg["max_seq_length"])
        if cfg.get("dtype") == "float16" and self.dev != "cpu":
            self.m.half()
        self.dim = int(self.m.get_sentence_embedding_dimension())
        # the model reads only the first max_seq_length tokens; a text is cut to 32 chars per token first so a long
        # document (a patent description, a LongBench context) is not tokenized whole (same vector for natural text)
        self.cap = 32 * int(self.m.max_seq_length or 512)

    def __call__(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, self.dim), np.float16)
        return self.m.encode([t[:self.cap] for t in texts], batch_size=256, normalize_embeddings=True,
                             convert_to_numpy=True).astype(np.float16)


def emb_dir(cfg: dict) -> Path:
    tag = f"{cfg['model']}-L{cfg.get('max_seq_length')}-{cfg.get('dtype', 'float32')}"
    return EMB_DIR / re.sub(r"[^A-Za-z0-9.]+", "-", tag)


class EmbCache:
    """Eval-side embeddings keyed by the text key (hseq of the normalized words; the Scan's key), so the ~6M eval texts
    are encoded once (`decontam_g13.py embed-cache`), not once per run. Vectors only (no text). Shards are written
    whole (tmp + rename). A key that is missing is encoded live by Embed, so the cache never changes a result."""

    def __init__(self, d: Path):
        self.d = Path(d)
        self.vecs, keys, sh, row = [], [], [], []
        for kf in sorted(self.d.glob("s*.keys.npy")) if self.d.exists() else []:
            vf = kf.with_name(kf.name.replace(".keys.npy", ".vec.npy"))
            if not vf.exists():
                continue
            k = np.load(kf)
            self.vecs.append(np.load(vf, mmap_mode="r"))
            keys.append(k)
            sh.append(np.full(len(k), len(self.vecs) - 1, np.int32))
            row.append(np.arange(len(k), dtype=np.int64))
        k = np.concatenate(keys) if keys else np.empty(0, np.uint64)
        o = np.argsort(k, kind="stable")
        self.keys = k[o]
        self.sh = np.concatenate(sh)[o] if sh else np.empty(0, np.int32)
        self.row = np.concatenate(row)[o] if row else np.empty(0, np.int64)

    def __len__(self) -> int:
        return len(self.keys)

    def has(self, keys: np.ndarray) -> np.ndarray:
        return member(self.keys, np.asarray(keys, np.uint64))

    def get(self, keys: np.ndarray, dim: int) -> tuple[np.ndarray, np.ndarray]:
        keys = np.asarray(keys, np.uint64)
        out = np.zeros((len(keys), dim), np.float16)
        if not len(self.keys):
            return out, np.zeros(len(keys), bool)
        i = np.minimum(np.searchsorted(self.keys, keys), len(self.keys) - 1)
        ok = self.keys[i] == keys
        for s in np.unique(self.sh[i[ok]]).tolist():
            sel = np.nonzero(ok & (self.sh[i] == s))[0]
            out[sel] = self.vecs[s][self.row[i[sel]]]
        return out, ok

    def add(self, keys: list[int], vecs: np.ndarray) -> None:
        self.d.mkdir(parents=True, exist_ok=True)
        base = self.d / f"s{time.time_ns()}_{os.getpid()}"      # unique: two writers never share a shard name
        for suf, arr in ((".vec.npy", vecs.astype(np.float16)), (".keys.npy", np.asarray(keys, np.uint64))):
            tmp = Path(str(base) + suf + ".tmp")
            with open(tmp, "wb") as f:
                np.save(f, arr)
            tmp.rename(Path(str(base) + suf))       # keys last: a shard counts only once both files exist


class SideCache:
    """A25 (d), the sealed-side CHILD only: its own vector-only cache (keys = the Scan's text hash, values = float16
    vectors; never text) in its own folder (SIDE_EMB_DIR, apart from the parent's EmbCache), so OHS-3 + its sources +
    LongBench v2 are encoded once, not on every run. Only the child reads or writes it; the parent's guard refuses the
    folder (NEVER). A missing key is encoded live and added, so the cache never changes a result. G13_SIDE_CACHE=0
    turns it off (then nothing is written)."""

    def __init__(self, d: Path, shard: int = 50_000):
        self.d, self.shard = Path(d), shard
        self.c = EmbCache(self.d)
        self.bk, self.bv, self.added = [], [], 0

    def __len__(self) -> int:
        return len(self.c)

    def get(self, keys: np.ndarray, dim: int):
        return self.c.get(keys, dim)

    def has(self, keys: np.ndarray) -> np.ndarray:
        return self.c.has(keys)

    def put(self, keys: np.ndarray, vecs: np.ndarray) -> None:
        self.bk.append(np.asarray(keys, np.uint64))
        self.bv.append(np.asarray(vecs, np.float16))
        if sum(len(k) for k in self.bk) >= self.shard:
            self.flush()

    def flush(self) -> None:
        if not self.bk:
            return
        k, v = np.concatenate(self.bk), np.concatenate(self.bv)
        k, i = np.unique(k, return_index=True)
        self.c.add(k.tolist(), v[i])
        self.added += len(k)
        self.bk, self.bv = [], []


def side_emb_dir(cfg: dict) -> Path:
    return SIDE_EMB_DIR / emb_dir(cfg).name


class Embed:
    """Method 5 (spec 7.2; RUNBOOK B 6): an eval text hits a training text when that text is among its top-5 nearest
    training texts OF THE SAME SET and the cosine is >= the hand-fixed threshold (c_build/g13_cosine_threshold.json).
    Eval vectors come from the EmbCache, or are encoded live. One Embed per training index (bind)."""

    def __init__(self, cfg: dict, enc: "Encoder | None" = None, cache: "EmbCache | None" = None):
        self.cfg, self.thr = cfg, float(cfg["threshold"])
        self.enc = enc or Encoder(cfg)
        self.cache = cache
        self.vec_of: dict = {}                  # training text key -> vector (shared by every bound index)
        self.stats = Counter()
        self.T = None
        self.side = None                        # the sealed-side child's own cache (SideCache), never the parent's

    def bind(self, idx: TrainIndex, owner: list) -> "Embed":
        b = Embed.__new__(Embed)
        b.cfg, b.thr, b.enc, b.cache, b.vec_of, b.stats = self.cfg, self.thr, self.enc, self.cache, self.vec_of, \
            self.stats
        b.side = getattr(self, "side", None)
        b.us = [u for u, ids in enumerate(idx.ids) if len(ids) >= MIN_WORDS]
        need = [u for u in b.us if idx.key[u] not in self.vec_of]
        if need:
            V = self.enc([idx.raw[u] for u in need])
            for u, v in zip(need, V):
                self.vec_of[idx.key[u]] = v
        T = np.stack([self.vec_of[idx.key[u]] for u in b.us]).astype(np.float32) if b.us else \
            np.zeros((0, self.enc.dim), np.float32)
        cols = defaultdict(list)
        for j, u in enumerate(b.us):
            for st in {owner[ui] for ui, _ in idx.occ[u]}:
                cols[st].append(j)
        b.cols = {st: np.array(js, np.int64) for st, js in cols.items()}
        import torch
        b.torch = torch
        b.T = torch.from_numpy(T).to(self.enc.dev)
        return b

    def vectors(self, keys: list[int], raws: list[str]) -> np.ndarray:
        dim = self.enc.dim
        if self.cache is not None and len(self.cache):
            E, ok = self.cache.get(np.array(keys, np.uint64), dim)
        else:
            E, ok = np.zeros((len(keys), dim), np.float16), np.zeros(len(keys), bool)
        side = getattr(self, "side", None)
        if side is not None and (~ok).any():
            m = np.nonzero(~ok)[0]
            E2, ok2 = side.get(np.array(keys, np.uint64)[m], dim)
            E[m[ok2]] = E2[ok2]
            ok[m[ok2]] = True
            self.stats["side_cache_hit"] += int(ok2.sum())
        miss = np.nonzero(~ok)[0]
        if len(miss):
            E[miss] = self.enc([raws[i] for i in miss.tolist()])
            if side is not None:
                side.put(np.array(keys, np.uint64)[miss], E[miss])
        self.stats["cache_hit"] += int(ok.sum())
        self.stats["encoded_live"] += len(miss)
        return E

    def scan(self, keys, raws, ress, chunk: int = 2048) -> None:
        """Live (the sealed-side child): vectors from the cache or encoded now; hits into the flush results."""
        if not len(self.us) or not keys:
            return
        for r, got in self.hits(self.vectors(keys, raws), chunk):
            for m, us in got.items():
                ress[r][m] |= us

    def hits(self, V: np.ndarray, chunk: int = 2048) -> list:
        """Rows of V (float16 eval vectors) -> [(row, {"embed@<set>": {training text}})] for rows with a hit."""
        torch, out = self.torch, []
        if not len(self.us) or not len(V):
            return out
        for a in range(0, len(V), chunk):
            Ec = torch.from_numpy(np.ascontiguousarray(V[a:a + chunk]).astype(np.float32)).to(self.enc.dev)
            S = Ec @ self.T.T
            rows = torch.nonzero(S.max(dim=1).values >= self.thr).flatten().cpu().numpy()
            if not len(rows):
                continue
            Sr = S[torch.from_numpy(rows).to(self.enc.dev)].cpu().numpy()
            for r, srow in zip(rows.tolist(), Sr):
                got = {}
                for st, cs in self.cols.items():
                    v = srow[cs]
                    top = np.argpartition(-v, min(5, len(v)) - 1)[:5] if len(v) > 5 else np.arange(len(v))
                    us = {self.us[int(cs[j])] for j in top.tolist() if v[j] >= self.thr}
                    if us:
                        got[f"embed@{st}"] = us
                if got:
                    out.append((a + r, got))
        return out



def instr_pieces(instr) -> list[str]:
    """Method 8 (A25 e): a dev / eval instruction whole and each of its sentences / lines, >= 5 words each."""
    if not isinstance(instr, str) or not instr.strip():
        return []
    out = [instr] + [s for s in _SEG.split(instr) if s.strip()]
    seen, keep = set(), []
    for t in out:
        ws = words(t)
        if len(ws) >= MIN_WORDS and hseq(ws) not in seen:
            seen.add(hseq(ws))
            keep.append(t)
    return keep




def _alive(lock: Path) -> bool:
    """True while the embed-cache builder named in `lock` (its pid) is running."""
    try:
        os.kill(int(lock.read_text().strip()), 0)
        return True
    except (OSError, ValueError):
        return False


def embed_pass(sc: Scan, emb: "Embed", why: list, tgs: list, wait_s: int = 6 * 3600) -> dict:
    """Method 5 for a deferred scan (the parent): every noted eval text key is looked up in the EmbCache (no eval text
    is re-read or kept) and compared with this index's training texts, top-5 per set. While `embed-cache` is still
    building (its BUILDING file exists) missing keys are waited for; keys still missing make the log incomplete."""
    labels = [lb for lb in sc.ek if len(sc.ek[lb])]
    if not labels:
        return {"texts": 0}
    allk = np.unique(np.concatenate([np.frombuffer(sc.ek[lb], np.uint64) for lb in labels]))
    cache, t0 = emb.cache, time.time()
    if cache is not None and cache.d.exists():      # shards written during this run (hfstream targets) count too
        cache = emb.cache = EmbCache(cache.d)
    while True:
        miss = int((~cache.has(allk)).sum())
        building = any(_alive(f) for f in cache.d.glob("BUILDING*"))
        if not miss or not building or time.time() - t0 > wait_s:
            break
        print(f"  .. embed: {miss} of {len(allk)} eval texts not cached yet; waiting for embed-cache", flush=True)
        time.sleep(120)
        cache = emb.cache = EmbCache(cache.d)
    if miss and not any(_alive(f) for f in cache.d.glob("BUILDING*")):   # fill the missing keys' targets now
        need = {lb for lb in labels if (~cache.has(np.frombuffer(sc.ek[lb], np.uint64))).any()}
        names = sorted({t["name"] for t in tgs if t["name"] in need or (t["sublabel"] and t["sublabel"]["label"] in need)})
        print(f"  .. embed: {miss} eval texts not cached; encoding them now ({len(names)} targets)", flush=True)
        _build(emb.cfg, cache, names, tgs, emb.enc)
        cache = emb.cache = EmbCache(cache.d)
    ok = cache.has(allk)
    keys = allk[ok]
    res: dict = {}
    for a in range(0, len(keys), 200_000):
        kk = keys[a:a + 200_000]
        V, _ = cache.get(kk, emb.enc.dim)
        for r, got in emb.hits(V):
            res[int(kk[r])] = got
    emb.stats["cache_hit"] += int(ok.sum())
    if (~ok).any():
        miss_k = allk[~ok]
        for lb in labels:                           # one reason per eval label (refresh replaces a label's reasons)
            n = int(member(miss_k, np.unique(np.frombuffer(sc.ek[lb], np.uint64))).sum())
            if n:
                _tag(why, lb)
                why.append(f"embed (method 5): {n} eval texts not in the embedding cache [{lb}] (run "
                           "`decontam_g13.py embed-cache`, then re-run)")
        _tag(why, None)
    hk = np.array(sorted(res), np.uint64)
    for lb in labels:
        K, It = np.frombuffer(sc.ek[lb], np.uint64), np.frombuffer(sc.ei[lb], np.int64)
        m = member(hk, K)
        for k, it in zip(K[m].tolist(), It[m].tolist()):
            for meth, us in res[k].items():
                sc.hits[lb][meth] |= us
                sc.items_hit[lb][meth].add(it)
                sc.items_by[meth[6:]][lb][meth].add(it)
    return {"texts": len(allk), "cached": int(ok.sum()), "hit_texts": len(res), "s": round(time.time() - t0)}


def stream(scan: Scan, tg: dict, rec: dict, shas: dict, files: list | None = None, ok=None) -> None:
    """Feed every item of target `tg` to the scan. `files` / `ok`: the sealed-side child passes its own file list and
    guard (A25 d); the parent always uses resolve() + allowed()."""
    par_ok = files is None and ok is None          # G13_STREAM_WORKERS: only the parent's own call may use the pool
    ok = ok or allowed
    files = [p for spec in tg["paths"] for p in resolve(spec)] if files is None else files
    if tg.get("main_only"):                         # mixdev_S5.jsonl, not its .sidecar / .sealedqc / ... companions
        files = [p for p in files if p.name.count(".") == 1]
    refused = [p for p in files if not ok(p)]
    files = [p for p in files if ok(p)]
    rec["files"], rec["refused_paths"] = len(files), len(refused)
    names = set()
    if tg["sublabel"]:
        nf = resolve(tg["sublabel"]["names"])
        names = {str(x) for x in (jload(nf[0]) or [])} if nf else set()
        rec["sublabel_names"] = len(names)
    unsupported = Counter()
    on_file = getattr(scan, "on_file", None)       # the sealed-side child: counts-only progress per file
    nw = _par_workers(scan, files, par_ok, on_file)
    if nw:                                          # G13_STREAM_WORKERS=N > 1 and a big parquet target: process pool
        _stream_parallel(scan, tg, shas, files, unsupported, nw)
        if unsupported:
            rec["unsupported_files"] = dict(unsupported)
        return
    for fi, p in enumerate(files):
        if on_file is not None:
            on_file(fi, len(files))
        ext = p.suffix.lower()
        if ext not in DATA_EXT:
            unsupported[ext or "(none)"] += 1
            continue
        if p.is_relative_to(STREAM_ROOT):       # hfstream: fetch, scan, delete (never kept)
            repo, fn = "/".join(p.relative_to(STREAM_ROOT).parts[:2]), "/".join(p.relative_to(STREAM_ROOT).parts[2:])
            with tempfile.TemporaryDirectory(dir=str(HERE / "tmp") if (HERE / "tmp").is_dir() else None) as td:
                from huggingface_hub import hf_hub_download
                _lr = os.environ.get("G13_BIGPAT_LOCAL")   # owner OK 8 Oct: same parquet pre-downloaded with retries (flaky network)
                _loc = (Path(_lr) / fn) if _lr else None
                lp = _loc if (_loc is not None and _loc.is_file()) else Path(hf_hub_download(repo, fn, repo_type="dataset", local_dir=td))
                shas[f"hfstream:{repo}/{fn}"] = sha256_file(lp)
                co = getattr(scan, "co", None)      # the parent fills the EmbCache now: the file is gone afterwards
                for r in parquet_records(lp, tg["fields"]):
                    lv = list(leaves(r, tg["fields"]))
                    top = max(range(len(lv)), key=lambda i: len(lv[i]), default=-1)
                    its = [(x, i == top) for i, x in enumerate(lv)]
                    scan.add_item((tg["name"],), its, tg["methods"], tg["tables"])
                    if co is not None:
                        co.add_item((tg["name"],), its, tg["methods"], tg["tables"])
                scan.flush()
                if co is not None:
                    co.flush(force=True)
            continue
        note_sha(shas, p)
        if tg.get("csv_sep") and ext == ".csv":     # one table per file (TabFact all_csv)
            scan.add_item((tg["name"],), [(csv_table_text(p.read_text(errors="replace"), tg["csv_sep"]), True)],
                          tg["methods"], True)
            continue
        recs = parquet_records(p, tg["fields"]) if ext == ".parquet" else read_records(p, ext, p.read_bytes())
        if tg["kind"] == "instr":                   # method 8: instruction templates, pieces as content texts
            for r in recs:
                if isinstance(r, dict):
                    ps = instr_pieces(r.get("instructions"))
                    if ps:
                        scan.add_item((tg["name"],), [(x, True) for x in ps], tg["methods"], False)
            continue
        for r in recs:
            labels = (tg["name"],)
            if names and isinstance(r, dict) and any(isinstance(v, str) and v in names for v in r.values()):
                labels = (tg["name"], tg["sublabel"]["label"])
                scan.sub_rows[tg["sublabel"]["label"]] += 1
            if isinstance(r, dict) and "state" in r and tg["kind"] == "rows":   # the C / OpenDecide row format
                f = tg["fields"] or ("state", "instructions", "options", "card")
                texts = [(r["state"], True)] if "state" in f and isinstance(r.get("state"), str) else []
                for k in f:
                    if k == "state":
                        continue
                    v = r.get(k)
                    vs = v if isinstance(v, list) else [v]
                    texts += [(x, False) for x in vs if isinstance(x, str)]
            else:
                lv = list(leaves(r, tg["fields"] if isinstance(r, dict) else None))
                top = max(range(len(lv)), key=lambda i: len(lv[i]), default=-1)
                texts = [(x, i == top) for i, x in enumerate(lv)]
            scan.add_item(labels, texts, tg["methods"], tg["tables"])
    scan.flush()
    if unsupported:
        rec["unsupported_files"] = dict(unsupported)


# ---- G13_STREAM_WORKERS=N: the files of a big multi-file parquet target are scanned by N worker processes ------------
# Speed only; the result is the serial scan's. What a worker computes is the PURE part of Scan.flush(): the per-text
# result (training texts hit, per method), keyed by the exact text (normalized-words hash + a digest of the raw text, see
# _rawdig). Everything ORDER-dependent stays in the parent: the parent REPLAYS the serial Scan.add_item / Scan.flush
# sequence (item numbers, the dedup cache with its 2M clear rule, the BATCH_WORDS batches, the hfstream end-of-file flush,
# deferred ek / ei, credits, short / sub_rows / sha bookkeeping) on the real Scan, file by file in FILE ORDER, from the
# compact event streams the workers return. The Scan therefore goes through the same operations in the same order as in
# the serial run, whatever the number of workers (no offsetting or set merging). The workers' own dedup cache is a plain
# memo of that pure function (identical key = identical result), so it cannot change a result. Workers are fresh
# interpreters (subprocess + pipe, no fork, no __main__ re-import) that load this file and the training index once.
_REPLAY_SRC_SHA = "7e9c1f25d8051bb06681efc61d5fa119970389252fa35020bd6fe9c7c45437c1"          # sha256 of the Scan.add_item / flush / _credit / owners source the replay mirrors


def _replay_src_sha() -> str:
    import inspect
    src = "".join(inspect.getsource(f) for f in (Scan.add_item, Scan.flush, Scan._credit, Scan.owners))
    return hashlib.sha256(src.encode()).hexdigest()


def _env_num(name: str, default, cast):
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        return cast(raw.strip())
    except ValueError:
        raise ValueError(f"{name} must be a number, got {raw!r}") from None


def _par_workers(scan, files: list, par_ok: bool, on_file) -> int:
    """N > 1 when stream() should scan `files` with the process pool, else 0 (the exact serial path). Needs
    G13_STREAM_WORKERS=N >= 2, the parent's own Scan (not a subclass, not the sealed-side child's, no live embedding),
    >= G13_STREAM_MIN_FILES (4) parquet files and >= G13_STREAM_MIN_MB (32) of them (hfstream files count as big)."""
    n = _env_num("G13_STREAM_WORKERS", 1, int)
    if n < 1:
        raise ValueError("G13_STREAM_WORKERS must be >= 1")
    if n == 1:
        return 0
    if not (par_ok and type(scan) is Scan and scan.embed is None and on_file is None and not scan.q
            and not scan.waiting):
        return 0
    pq = [p for p in files if p.suffix.lower() == ".parquet"]
    if len(pq) < _env_num("G13_STREAM_MIN_FILES", 4, int):
        return 0
    mb = 0.0
    for p in pq:
        if p.is_relative_to(STREAM_ROOT):
            mb = float("inf")
            break
        try:
            mb += p.stat().st_size / 1e6
        except OSError:
            pass
    return min(n, len(files)) if mb >= _env_num("G13_STREAM_MIN_MB", 32.0, float) else 0


def _rawdig(raw: str) -> int:
    """64-bit digest of the raw text. Scan's dedup key is the normalized words, but exact_seg / table read the RAW text
    (sentence and line cuts), so two raw texts with equal words can in principle differ; the workers key their results
    by (words, raw digest) and the replay picks the digest of the text the serial scan would have computed."""
    return int.from_bytes(hashlib.blake2b(raw.encode("utf-8", "surrogatepass"), digest_size=8).digest(), "little")


class _Harvest(dict):
    """A worker's dedup cache: keeps every result of its file (the parent applies Scan's own clear rule)."""

    def clear(self) -> None:
        pass


class _PScan(Scan):
    """WORKER ONLY. Scans one file on a fresh state: add_item mirrors Scan.add_item's text selection, queues each
    distinct (words, raw digest) text for the stock Scan.flush (which computes the per-text results), credits nothing,
    and records the compact event stream the parent replays (see _Replay). partial() is what goes back to the parent."""

    def __init__(self, idx: TrainIndex, defer: bool):
        super().__init__(idx, None, [], defer)
        self.cache = _Harvest()
        self._lab, self._mt = {}, {}
        self.e_lab, self.e_mt, self.e_sh, self.e_n = (array.array(c) for c in "HHBI")
        self.t_key, self.t_nw, self.t_dig = array.array("Q"), array.array("I"), array.array("Q")
        self.co_seen, self.co_keys = set(), array.array("Q")      # the embedding collector's keys (_Collect.add_item)

    def add_item(self, labels: tuple, texts: list[tuple[str, bool]], methods, want_tables: bool) -> None:
        mkey = methods if isinstance(methods, str) else ",".join(methods)
        lc = self._lab.setdefault(labels, len(self._lab))
        mc = self._mt.setdefault((methods if isinstance(methods, str) else tuple(methods), want_tables), len(self._mt))
        for lb in labels:
            self.items[lb] += 1
        tw = [(raw, ws, c) for raw, c in texts for ws in [words(raw)] if ws]
        sh = not any(c and len(ws) >= MIN_WORDS for _, ws, c in tw)
        if sh:
            for lb in labels:
                self.short[lb] += 1
        n = 0
        for raw, ws, c in tw:
            short = len(ws) < MIN_WORDS
            if short and not c:
                continue
            h = hseq(ws)
            dig = 0 if short else _rawdig(raw)
            n += 1
            self.t_key.append(h)
            self.t_nw.append(len(ws))
            self.t_dig.append(dig)
            if not short and methods == "all" and h not in self.co_seen:
                self.co_seen.add(h)
                self.co_keys.append(h)
            key = (h, mkey, short, want_tables, dig)
            if key in self.cache or key in self.waiting:
                continue
            self.q.append((key, ws, raw, methods, want_tables, short))
            self.q_words += len(ws)
            self.waiting[key] = []
        self.e_lab.append(lc)
        self.e_mt.append(mc)
        self.e_sh.append(sh)
        self.e_n.append(n)
        if self.q_words >= BATCH_WORDS:
            self.flush()

    def partial(self, shas: dict) -> dict:
        self.flush()
        return {"lab": list(self._lab), "mt": list(self._mt),
                "e_lab": self.e_lab.tobytes(), "e_mt": self.e_mt.tobytes(), "e_sh": self.e_sh.tobytes(),
                "e_n": self.e_n.tobytes(), "t_key": self.t_key.tobytes(), "t_nw": self.t_nw.tobytes(),
                "t_dig": self.t_dig.tobytes(),
                "res": {k: {m: tuple(v) for m, v in r.items()} for k, r in self.cache.items() if r},
                "sub_rows": list(self.sub_rows.items()), "shas": list(shas.items()), "co": self.co_keys.tobytes(),
                "items": dict(self.items), "short": dict(self.short)}


def _idx_state(idx: TrainIndex) -> dict:
    """What Scan.flush reads of a TrainIndex (not units / raw / key / occ), with the word-id arrays as one block."""
    cat = np.concatenate(idx.ids) if idx.ids else np.empty(0, np.uint64)
    return {"full": idx.full, "seg": idx.seg, "tab": idx.tab, "g": idx.g, "bk": idx.bk, "bt": idx.bt, "ids_cat": cat,
            "ids_len": np.array([len(x) for x in idx.ids], np.int64)}


def _idx_from_state(st: dict) -> TrainIndex:
    idx = TrainIndex.__new__(TrainIndex)
    idx.full, idx.seg, idx.tab, idx.g, idx.bk, idx.bt = (st[k] for k in ("full", "seg", "tab", "g", "bk", "bt"))
    lens = st["ids_len"]
    idx.ids = np.split(st["ids_cat"], np.cumsum(lens)[:-1]) if len(lens) else []
    idx._g5 = {}
    return idx


MH_BLOCK_ROWS, MH_BLOCK_ELEMS = 2048, 200_000


def _minhash_blocked(h5: np.ndarray, t5: np.ndarray, n_texts: int) -> np.ndarray:
    """WORKER ONLY: minhash() with cache-sized temporaries, bit for bit the same signatures. minhash() builds
    (all 5-grams of the batch x a few permutations) arrays of ~4M words and every step of _mix() passes through them
    in DRAM, which is what makes N processes share one memory bus. Here whole texts are taken in blocks of about
    MH_BLOCK_ROWS 5-grams (a longer text alone, its permutations in chunks of MH_BLOCK_ELEMS words), so the
    temporaries stay in the cache. A text's signature is still the minimum, over its own 5-grams, of the same
    _mix(h5 * PA + PB) values (tests/test_g13_parallel.py compares both on random batches)."""
    sig = np.full((n_texts, MH_PERM), np.iinfo(np.uint64).max, np.uint64)
    if len(h5) == 0:
        return sig
    order = np.argsort(t5, kind="stable")
    h5, t5 = h5[order], t5[order]
    ut, first = np.unique(t5, return_index=True)
    ends = np.append(first[1:], len(h5))
    a = 0
    with np.errstate(over="ignore"):
        while a < len(ut):
            b = max(a + 1, int(np.searchsorted(ends, first[a] + MH_BLOCK_ROWS, "right")))
            lo, hi = int(first[a]), int(ends[b - 1])
            step = max(1, min(MH_PERM, MH_BLOCK_ELEMS // (hi - lo)))
            for c in range(0, MH_PERM, step):
                v = _mix(h5[lo:hi, None] * PA[None, c:c + step] + PB[None, c:c + step])
                sig[ut[a:b], c:c + step] = np.minimum.reduceat(v, first[a:b] - lo, axis=0)
            a = b
    return sig


def _safe_err(e: BaseException) -> str:
    """Exception type and code locations only: never the message (it may quote an eval record)."""
    fr = traceback.extract_tb(e.__traceback__)[-4:]
    return type(e).__name__ + " at " + " < ".join(f"{Path(f.filename).name}:{f.lineno}:{f.name}" for f in reversed(fr))


def _pw_scan_file(st: dict, p: Path) -> dict:
    t0, c0 = time.time(), time.process_time()
    sc = _PScan(st["idx"], st["defer"])
    rec, shas = {}, {}
    stream(sc, st["tg"], rec, shas, files=[p])
    if rec.get("files") != 1 or rec.get("refused_paths"):
        raise RuntimeError("worker file refused or filtered")
    part = sc.partial(shas)
    part["wall_s"], part["cpu_s"] = round(time.time() - t0, 1), round(time.process_time() - c0, 1)
    if len(_VOC) > 1_000_000:                       # word-id memo (wids): a cache only; keeps a long-lived worker small
        _VOC.clear()
    return part


_PW_BOOT = ("import importlib.util, sys\n"
            "s = importlib.util.spec_from_file_location('g13_engine', sys.argv[1])\n"
            "m = importlib.util.module_from_spec(s)\n"
            "sys.modules['g13_engine'] = m\n"
            "s.loader.exec_module(m)\n"
            "m._pw_main(int(sys.argv[2]), sys.argv[3])\n")


def _pw_main(fd: int, init_path: str) -> None:
    """WORKER ENTRY (python -c _PW_BOOT): load the training index once, then scan the files the parent sends."""
    import threading
    from multiprocessing.connection import Connection
    conn, ppid = Connection(fd), os.getppid()
    globals()["minhash"] = _minhash_blocked         # this worker process only (Scan._ngrams looks minhash up here)

    def watch() -> None:                            # the parent is gone (killed): do not keep scanning
        while True:
            time.sleep(5)
            if os.getppid() != ppid:
                os._exit(3)

    threading.Thread(target=watch, daemon=True).start()
    try:
        with open(init_path, "rb") as f:
            st = pickle.load(f)
        if st["sha"] != sha256_file(Path(__file__)):
            raise RuntimeError("engine file changed since the parent started")
        st["idx"] = _idx_from_state(st["idx"])
        conn.send(("ready", os.getpid()))
    except BaseException as e:  # noqa: BLE001
        conn.send(("err", -1, _safe_err(e)))
        sys.exit(1)
    while True:
        try:
            msg = conn.recv()
        except EOFError:
            return
        if msg is None:
            return
        i, p = msg
        try:
            part = _pw_scan_file(st, Path(p))
        except BaseException as e:  # noqa: BLE001
            conn.send(("err", i, _safe_err(e)))
            sys.exit(1)
        conn.send(("ok", i, part))


class _StreamPool:
    """PARENT: N worker processes, each loads the slim training index from one temp file. run(files) yields
    (file, partial) in FILE ORDER; at most N files are being scanned and at most N more finished partials wait their
    turn (window 2N), so memory is bounded by N files plus N small partials."""

    def __init__(self, scan: Scan, tg: dict, n: int):
        from multiprocessing import Pipe
        self.td, self.workers = tempfile.mkdtemp(prefix="g13pw_"), []
        try:
            init = Path(self.td) / "init.pkl"
            with open(init, "wb") as f:
                pickle.dump({"sha": sha256_file(Path(__file__)), "idx": _idx_state(scan.idx), "defer": scan.defer,
                             "tg": tg}, f, protocol=pickle.HIGHEST_PROTOCOL)
            env = {**os.environ, "G13_STREAM_WORKERS": "1"}
            for _ in range(n):
                pc, cc = Pipe(duplex=True)
                proc = subprocess.Popen([sys.executable, "-B", "-c", _PW_BOOT, str(Path(__file__).resolve()),
                                         str(cc.fileno()), str(init)], pass_fds=[cc.fileno()],
                                        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, env=env, cwd=str(LEAN))
                cc.close()
                self.workers.append((proc, pc))
            for proc, pc in self.workers:
                while not pc.poll(1.0):
                    if proc.poll() is not None:
                        raise RuntimeError(f"G13 stream worker exited at start (exit {proc.poll()})")
                try:
                    msg = pc.recv()
                except EOFError:
                    raise RuntimeError(f"G13 stream worker died at start (exit {proc.wait()})") from None
                if msg[0] != "ready":
                    raise RuntimeError(f"G13 stream worker failed at start: {msg[2]}")
        except BaseException:
            self.close(abort=True)
            raise

    def run(self, files: list):
        from multiprocessing.connection import wait
        n, nxt, merged, done, busy = len(files), 0, 0, {}, {}
        idle, win = list(self.workers), 2 * len(self.workers)
        while merged < n:
            while idle and nxt < n and nxt < merged + win:
                w = idle.pop()
                try:
                    w[1].send((nxt, str(files[nxt])))
                except OSError:
                    raise RuntimeError(f"G13 stream worker died before file #{nxt} of {n} (exit {w[0].wait()})") from None
                busy[w[1]] = (w, nxt)
                nxt += 1
            for c in (wait(list(busy), timeout=5) if busy else []):
                w, i = busy.pop(c)
                try:
                    msg = c.recv()
                except EOFError:
                    raise RuntimeError(f"G13 stream worker died on file #{i} of {n} (exit {w[0].wait()})") from None
                if msg[0] != "ok":
                    raise RuntimeError(f"G13 stream worker failed on file #{msg[1]} of {n}: {msg[2]}")
                done[msg[1]] = msg[2]
                idle.append(w)
            while merged in done:
                part = done.pop(merged)
                yield files[merged], part
                del part
                merged += 1

    def close(self, abort: bool = False) -> None:
        for proc, conn in self.workers:
            try:
                if abort:
                    proc.terminate()
                else:
                    conn.send(None)
            except (OSError, ValueError):
                pass
        for proc, conn in self.workers:
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
            try:
                conn.close()
            except OSError:
                pass
        shutil.rmtree(self.td, ignore_errors=True)


def _arr(code: str, b: bytes) -> array.array:
    a = array.array(code)
    a.frombytes(b)
    return a


def _fset(t: tuple) -> frozenset:
    """The frozenset of a worker's result tuple. Same elements as the serial scan's; the iteration order of a set of
    several training texts depends on how it was built (even the serial result's depends on the batch it was computed
    in: ngram10 / minhash iterate sets of (batch index, text) pairs), and run_sets writes only sorted or counted
    fields except the key order of hits_by_eval[..]['u'], so that order is not a result."""
    return frozenset(set(t))


class _CoSink:
    """Stand-in Scan for stream(): feeds only the embedding collector, as stream() does for an hfstream file."""

    def __init__(self, co):
        self.co, self.sub_rows = co, Counter()

    def add_item(self, *a, **k) -> None:
        pass

    def flush(self) -> None:
        pass


class _Replay:
    """PARENT: Scan.add_item / Scan.flush replayed on the real Scan from the workers' event streams (file order). Mirrors
    the source whose sha256 is _REPLAY_SRC_SHA (checked before a pool is started)."""

    def __init__(self, scan: Scan):
        self.sc, self.rq, self.qw = scan, [], 0          # rq: (cache key, result) in queue order; qw: Scan.q_words

    def file(self, p: Path, part: dict, shas: dict, co, tg: dict) -> None:
        sc, hf = self.sc, p.is_relative_to(STREAM_ROOT)
        for k, h in part["shas"]:
            if not hf and k in shas and shas[k] != h:                 # note_sha: a file read twice with other contents
                h = "changed-during-run"
            shas[k] = h
        for lb, c in part["sub_rows"]:
            sc.sub_rows[lb] += c
        n0 = self.events(part)
        if hf:
            self.flush()                                            # stream(): scan.flush() after every hfstream file
            if co is not None:
                self.collect(p, part, n0, co, tg)

    def events(self, part: dict) -> Counter:
        sc, res, lab, mt = self.sc, part["res"], part["lab"], part["mt"]
        mk = [m if isinstance(m, str) else ",".join(m) for m, _ in mt]
        e_lab, e_mt, e_sh, e_n = (_arr(c, part[k]) for c, k in (("H", "e_lab"), ("H", "e_mt"), ("B", "e_sh"),
                                                                  ("I", "e_n")))
        t_key, t_nw, t_dig = _arr("Q", part["t_key"]), _arr("I", part["t_nw"]), _arr("Q", part["t_dig"])
        if sum(e_n) != len(t_key) or not (len(e_lab) == len(e_mt) == len(e_sh) == len(e_n)):
            raise RuntimeError("G13 stream worker returned an inconsistent event stream")
        items, short, cache, waiting, defer = sc.items, sc.short, sc.cache, sc.waiting, sc.defer
        base_i, base_s = Counter({lb: items[lb] for lb in part["items"]}), Counter({lb: short[lb] for lb in part["short"]})
        n0, tk, tn, td = Counter(), iter(t_key), iter(t_nw), iter(t_dig)
        for lc, mc, shi, n in zip(e_lab, e_mt, e_sh, e_n):
            labels, (methods, wt), mkey = lab[lc], mt[mc], mk[mc]
            item = items[labels[0]]
            for lb in labels:
                items[lb] += 1
            n0[labels[0]] += 1
            if shi:
                for lb in labels:
                    short[lb] += 1
            for _ in range(n):
                h, nw, dg = next(tk), next(tn), next(td)
                shrt = nw < MIN_WORDS
                key = (h, mkey, shrt, wt)
                if defer and not shrt and methods == "all":
                    for lb in labels:
                        sc.ek[lb].append(h)
                        sc.ei[lb].append(item)
                if key in cache:
                    sc._credit(labels, item, cache[key])
                    continue
                if key not in waiting:
                    r = res.get((h, mkey, shrt, wt, dg))
                    self.rq.append((key, {m: _fset(t) for m, t in r.items()} if r else {}))
                    self.qw += nw
                waiting[key].append((labels, item))
            if self.qw >= BATCH_WORDS:
                self.flush()
        if any(items[lb] - base_i[lb] != c for lb, c in part["items"].items()) or any(
                short[lb] - base_s[lb] != c for lb, c in part["short"].items()):
            raise RuntimeError("G13 stream worker counts differ from the replayed counts")
        return n0

    def flush(self) -> None:
        sc = self.sc
        for key, r in self.rq:
            if len(sc.cache) > 2_000_000:
                sc.cache.clear()
            sc.cache[key] = r
            for labels, item in sc.waiting.pop(key, []):
                sc._credit(labels, item, r)
        self.rq, self.qw = [], 0

    def collect(self, p: Path, part: dict, n0: Counter, co, tg: dict) -> None:
        """The embedding collector (hfstream files, run_sets with a cosine config) for the file just replayed. Keys all in
        the EmbCache: nothing to encode, only the collector's bookkeeping. Some missing: the parent re-reads the file
        through the collector and encodes serially, exactly as the serial path does."""
        new = [k for k in _arr("Q", part["co"]).tolist() if k not in co.seen]
        if new and (~co.cache.has(np.array(new, np.uint64))).any():
            stream(_CoSink(co), tg, {}, {}, files=[p])
            return
        for lb, c in n0.items():
            co.items[lb] += c
        co.seen.update(new)
        co.skipped += len(new)


def _stream_parallel(scan: Scan, tg: dict, shas: dict, files: list, unsupported: Counter, nw: int) -> None:
    """stream() with G13_STREAM_WORKERS: the serial file loop, files scanned by nw workers, merged by replay in file order."""
    if _replay_src_sha() != _REPLAY_SRC_SHA:
        raise RuntimeError("Scan.add_item / flush / _credit / owners changed: review _PScan / _Replay, then update "
                           "_REPLAY_SRC_SHA (or run with G13_STREAM_WORKERS=1)")
    todo = []
    for p in files:
        ext = p.suffix.lower()
        if ext not in DATA_EXT:
            unsupported[ext or "(none)"] += 1
        else:
            todo.append(p)
    co, rp, t0 = getattr(scan, "co", None), _Replay(scan), time.time()
    last, tr, wall, cpu = t0, 0.0, [], 0.0
    pool, ok = _StreamPool(scan, tg, min(nw, len(todo))), False
    try:
        for k, (p, part) in enumerate(pool.run(todo)):
            wall.append(part["wall_s"])
            cpu += part["cpu_s"]
            t1 = time.time()
            rp.file(p, part, shas, co, tg)
            tr += time.time() - t1
            if time.time() - last >= 300:
                last = time.time()
                print(f"  .. {tg['name']}: {k + 1}/{len(todo)} files merged, {last - t0:.0f} s ({len(pool.workers)} "
                      f"workers)", flush=True)
        rp.flush()                                  # stream(): the final scan.flush()
        ok = True
    finally:
        pool.close(abort=not ok)
    wall.sort()
    print(f"  .. {tg['name']}: parallel scan, {len(pool.workers)} workers, {len(todo)} files, {time.time() - t0:.0f} s "
          f"(workers: {sum(wall):.0f} s wall / {cpu:.0f} s cpu in total, per file min {wall[0]:.0f} / median "
          f"{wall[len(wall) // 2]:.0f} / max {wall[-1]:.0f} s; replay in the parent {tr:.0f} s)", flush=True)


EXTRA_KINDS = ("structure", "templates", "templates_rev", "sealed_check")
REFRESHABLE = ("mixdev", "mixdev_structure")      # `refresh`'s default targets (cheap; lanes rewrite mixdev)
FBT_MAX = 2000                                     # files_by_target is kept for targets reading <= this many files
UNIT_KEYS = {"structure": "struct", "structure_g13": "s_g13", "group_id": "groups"}


def extra_methods(units: list[dict], tgs: list[dict], trec: dict, why: list, train_path: Path | None = None,
                  eshas: dict | None = None) -> list:
    """Methods 6 (mixdev: generator structure hash, G13 state + options structure hash, group_id), 8 (OPI / jagged
    templates) and the sealed checker (6 part P, 7 keywords) for the targets of EXTRA_KINDS in `tgs`:
    [(target, method, {ui: fields}, eval items or None)]. Fills trec / why (and eshas with the inputs read)."""
    res = []
    for tg in tgs:
        if tg["status"] or tg["kind"] not in EXTRA_KINDS:
            continue
        r, t1, got_m = trec[tg["name"]], time.time(), {}
        _tag(why, tg["name"])
        ts: dict = {}
        if tg["kind"] == "structure":
            ks, n_items, n_files = mixdev_structs(ts)
            r.update(files=n_files, items=n_items, **{f"{m}_keys": len(v) for m, v in ks.items()},
                     units_without_structure_hash=sum(1 for u in units if not u["seed"] and not u.get("struct")))
            if not n_files:
                why.append(f"{tg['name']}: no mixdev file found")
            for m, v in ks.items():
                uk = UNIT_KEYS[m]
                got_m[m] = ({ui: {m} for ui, u in enumerate(units) if u.get(uk) and u[uk] & v},
                            len({h for u in units if u.get(uk) for h in u[uk] & v}))
        elif tg["kind"] == "templates_rev":
            W = instr_wordings(ts)
            hits, rep = template_rev_hits(units, W)
            r.update(wordings=len(W), **rep)
            if not W:
                why.append(f"{tg['name']}: no dev / eval instruction wording found (method 8 reverse not run)")
            got_m["template_rev"] = (hits, len(W))
        elif tg["kind"] == "templates":
            tm = template_strings(ts)
            r.update(templates=len(tm))
            if not tm:
                why.append(f"{tg['name']}: no OPI / jagged template string found (method 8 not run)")
            got_m["template"] = (template_hits(units, tm), len(tm))
        else:
            sh, srec = sealed_hits(units, train_path)
            r.update(srec)
            if srec.get("status") not in ("scanned", "nothing to check"):
                why.append(f"{tg['name']}: sealed_check {srec.get('status')} (exit {srec.get('exit')})")
            for m, us in sh.items():
                got_m[m] = ({ui: {"sealed"} for ui in us}, None)
        print(f"  .. {tg['name']}: {time.time() - t1:.0f} s", flush=True)
        if eshas is not None:
            eshas.update(ts)
        if isinstance(r, dict):
            r["eval_files"] = sorted(ts)
        res += [(tg["name"], m, got, n_ev) for m, (got, n_ev) in got_m.items()]
    _tag(why, None)
    return res


class _Why(list):
    """incomplete_why, with the eval target label(s) each reason belongs to ("_run" = the whole run), so `refresh` can
    replace exactly the reasons of the targets it re-scans."""

    def __init__(self, items=(), tags=None):
        super().__init__(items)
        if tags is None:
            tags = items.tags if isinstance(items, _Why) else [["_run"]] * len(self)
        self.tags = [list(t) for t in tags]
        self.cur = None

    def append(self, x) -> None:
        super().append(x)
        self.tags.append(list(self.cur) if isinstance(self.cur, (list, tuple)) else [self.cur or "_run"])

    def pairs(self) -> list:
        return [[t, w] for t, w in zip(self.tags, self)]


def _tag(why, label) -> None:
    if isinstance(why, _Why):
        why.cur = label


def methods_desc(tgs: list[dict], embed_on: bool, cfg: dict | None = None) -> dict:
    k = {t["kind"] for t in tgs if not t["status"]}
    return {"exact_full": "run", "exact_seg": "run", "exact_short": "run (never vs a training option)",
            "substring": "run", "ngram10": "run", "tulu8": "run", "minhash": "run",
            "embed": (f"run: top-5 per set, cosine >= {cfg['threshold']} ({cfg['model']}, max_seq_length "
                      f"{cfg.get('max_seq_length')}, {cfg.get('dtype', 'float32')})") if embed_on and cfg
            else "not_run: threshold not fixed",
            "table": "run where the eval has tables",
            "structure": "method 6 vs mixdev (meta.structure_hash, structure_g13 = state + options, group_id)"
            if "structure" in k else "not_run",
            "template": "method 8 (OPI strategy strings, jagged injected line; dev / eval instruction templates as "
                        "substrings under templates_instr)" if "templates" in k and "instr" in k else "not_run",
            "template_rev": "method 8, other direction (seeds_clean false): a Claude-written template piece of >= 3 "
                            "words EQUAL to a dev / eval instruction sentence / line or an OPI / jagged wording, or "
                            "of 5-9 words CONTAINED in one; 2-word equalities and 3-4-word containments counted "
                            "report-only" if "templates_rev" in k else "not_run",
            "sealed": "methods 6 (part P) / 7 via sealed_check.py (run only)" if "sealed_check" in k else "not_run",
            "sealed_side": "A25 (d): OHS-3 / LongBench v2 counts-only child, methods 1-5 + tables"
            if "sealed_side" in k else "not_run"}


def load_cosine(cosine: Path | None) -> dict | None:
    cfg = jload(cosine) if cosine and Path(cosine).exists() else None
    if cfg and isinstance(cfg.get("threshold"), (int, float)) and cfg.get("model"):
        return cfg
    return None


def sub_units(units: list[dict], fields: tuple) -> list[dict]:
    """A25 (c): the same units (same order) with only the instance-content texts (state, option)."""
    return [{**u, "texts": [(f, t) for f, t in u["texts"] if f in fields]} for u in units]


def _aggregate(hb: dict, unit_of: dict) -> dict:
    """The derived fields of a set's record from its per-label hits (hits_by_eval) and its units by key: drop ids /
    units, counts per eval label and method, counts per training source and field, seed hits. run_sets and refresh
    both use this, so a refreshed log is computed exactly as a full one."""
    counts, drop, seed_hit, seed_locs, unit_f = {}, set(), defaultdict(Counter), set(), defaultdict(set)
    seed_rep, rep_locs = defaultdict(Counter), set()
    for lb in sorted(hb):
        for m in sorted(hb[lb]):
            e = hb[lb][m]
            c = counts.setdefault(lb, {}).setdefault(m, {"units": len(e["u"]), "eval_items": e["n"]})
            if e["s"]:
                bind = [k for k in e["s"] if seed_status(unit_of.get(k)) != "not_rendered"]
                rep = [k for k in e["s"] if seed_status(unit_of.get(k)) == "not_rendered"]
                if bind:
                    c["seed_literals"] = len(bind)
                    seed_hit[lb][m] += len(bind)
                    seed_locs.update(bind)
                if rep:                             # A31 (b): proven absent from every training row: report only
                    c["seed_literals_report_only"] = len(rep)
                    seed_rep[lb][m] += len(rep)
                    rep_locs.update(rep)
            drop.update(e["u"])
            for k, fs in e["u"].items():
                unit_f[k].update(fs)
    by_src, by_field = Counter(), Counter()
    for k in drop:
        by_src[unit_of[k]["source"]] += 1
        for f in unit_f[k]:
            by_field[f] += 1
    return {"drop_ids": sorted(r for k in drop for r in unit_of[k]["rows"]), "drop_units": len(drop),
            "counts_by_eval_and_method": counts, "counts_by_training_source": dict(by_src),
            "counts_by_training_field": dict(by_field),
            "seed_hits": {k: dict(v) for k, v in seed_hit.items()}, "seed_hit_locs": sorted(seed_locs),
            "seeds_clean": not seed_locs,
            "seed_hits_report_only": {k: dict(v) for k, v in seed_rep.items()},
            "seed_hit_locs_report_only": sorted(rep_locs),
            "seed_render": {"rule": SEED_RENDER_RULE,
                            "binding": dict(Counter(seed_status(unit_of.get(k)) for k in seed_locs)),
                            "report_only_not_rendered": len(rep_locs)},
            "seed_hit_lines": {k: (unit_of.get(k) or {}).get("line") for k in sorted(seed_locs | rep_locs)[:1000]}}


# ---- A31 (b): does a hit seed literal render into a training row? (program check, counts only) ----------------------
SEED_RENDER_RULE = ("A31 (b): a Claude-written seed literal whose every piece (split at {...} / %-format / $-template "
                    "placeholders and line breaks; A32 (c): an edge word touching a placeholder, an f-string value, a "
                    "`+` operand or a %-format match with no space between is dropped; >= 2 words left, the methods' "
                    "normalization) is absent from every "
                    "training row of its set is code, not training content: its hits are report-only "
                    "('A31b: not rendered'). Rendered literals, literals with no >= 2-word piece (absence not "
                    "shown) and public-data records (A31 c) bind. Training rows: a family's candidates_r1 (selection "
                    "+ refill pool); packs / formats: every family's candidates_r1, the public training rows and "
                    "reserves, and the final mix when present")
_RENDER_SPLIT = re.compile(r"\{[^{}]*\}|%\(\w+\)[#0 +-]*\d*(?:\.\d+)?[A-Za-z]|%[#0+-]*\d*(?:\.\d+)?[sdifrxXeEgGc]"
                           r"|\$\{?\w+\}?|\n")   # A32 (c): no space flag in the bare %-spec ('50% sure' is prose)
RENDER_SHARED = tuple(f"c_src/{f}/out/candidates_r1.jsonl" for f in FAMS) + tuple(
    f"c_src/public/{x}" for x in ("public-1/out/public1_rows_r1.jsonl", "public-2/out/rows_r1.jsonl",
                                  "public-3/out/public3_rows_r1.jsonl", "public-1/out/public1_reserve.jsonl",
                                  "public-2/out/reserve_r1.jsonl", "public-3/out/public3_reserve.jsonl"))
# A34 (g): the final mix (FINAL_TRAIN) is no longer a render source: its only extra rows are replay rows, which are
# never generated from packs/formats and are checked as instance text by the final-mix G13.
RENDER_CHUNK = 32 << 20


def seed_status(u: dict | None) -> str:
    """A seed unit's A31 status: 'public_record' (A31 c, binds), 'rendered' / 'unprovable' / 'unchecked' (bind) or
    'not_rendered' (report-only)."""
    if not u:
        return "unchecked"
    if u.get("public"):
        return "public_record"
    return u.get("render") or "unchecked"


def seed_pieces(raw: str) -> list[str] | None:
    """A31 (b): the normalized pieces (' w1 w2 ... ', the methods' normalization) whose presence in a training row
    shows a seed literal renders. The literal is split at {...} / %-format / $-template placeholders and line breaks
    (a seed unit's render_text marks f-string values and `+` operands as "{}"). A32 (c): a piece's edge word that
    touches a placeholder / %-format match with no space between is dropped (the value glues onto it in the rendered
    text: '{n}th place' renders '5th place'). Every piece with >= 2 words left is kept. None: no piece has >= 2 words
    left, absence cannot be shown, the literal is 'unprovable' (binding)."""
    ps, at, glue_l = set(), 0, False
    for m in [*_RENDER_SPLIT.finditer(raw), None]:
        s, e, glue_r = (m.start(), m.end(), m.group() != "\n") if m else (len(raw), len(raw), False)
        part, ws = raw[at:s], words(raw[at:s])
        if ws and glue_l and not part[:1].isspace():
            ws = ws[1:]
        if ws and glue_r and not part[-1:].isspace():
            ws = ws[:-1]
        if len(ws) >= 2:
            ps.add(" " + " ".join(ws) + " ")
        at, glue_l = e, glue_r
    return sorted(ps) or None


class _RenderScan:
    """Normalized training texts, in ~32 MB chunks, searched for the pieces still not found (word boundaries; a
    separator no piece contains keeps texts apart). Repeated instructions / cards / options are normalized once."""

    def __init__(self, pieces):
        self.todo, self.found, self.seen, self.buf, self.n = set(pieces), set(), set(), [], 0

    def add(self, field: str, raw) -> None:
        if not self.todo or not isinstance(raw, str):
            return
        if field != "state":
            if raw in self.seen:
                return
            self.seen.add(raw)
        j = " ".join(words(raw))
        self.buf.append(j)
        self.n += len(j) + 3
        if self.n >= RENDER_CHUNK:
            self.flush()

    def flush(self) -> None:
        if self.buf and self.todo:
            big = " " + " \x01 ".join(self.buf) + " "
            hit = {p for p in self.todo if p in big}
            self.found |= hit
            self.todo -= hit
        self.buf, self.n = [], 0

    def done(self) -> set:
        self.flush()
        return self.found


def seed_render(need: dict, set_units: dict, shared_files=RENDER_SHARED) -> tuple[dict, dict]:
    """A31 (b) program check. need: set -> {seed key: literal} (hit Claude-written seed literals); set_units: set ->
    its units. A family's (any set but packs / formats) training rows are its own training units (candidates_r1:
    selection + refill pool); a shared seed set's (packs, formats) are every row of `shared_files` (one pass for both). Returns ({set: {key: status}},
    {set: {file: sha256}} of the shared row files read)."""
    pieces = {n: {k: seed_pieces(t) for k, t in ks.items()} for n, ks in need.items()}
    found, shared_want, shas = {}, set(), {}
    for n, pk in pieces.items():
        want = {p for ps in pk.values() if ps for p in ps}
        if n not in SEED_SETS:
            rs = _RenderScan(want)
            for u in set_units.get(n) or []:
                if not rs.todo:
                    break
                if not u["seed"]:
                    for f, t in u["texts"]:
                        rs.add(f, t)
            found[n] = rs.done()
        else:
            shared_want |= want
    shared_n = [n for n in pieces if n in SEED_SETS]
    if shared_n and shared_want:
        rs = _RenderScan(shared_want)
        for rel in shared_files:
            f = LEAN / rel
            if not rs.todo:
                break
            if not f.exists() or not allowed(f):
                continue
            shas[rel] = sha256_file(f)
            with open(f) as fh:
                for line in fh:
                    if not rs.todo:
                        break
                    if line.strip():
                        try:
                            r = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        for fld, t in row_texts(r):
                            rs.add(fld, t)
        got = rs.done()
        for n in shared_n:
            found[n] = got
    st = {n: {k: ("unprovable" if ps is None else "rendered" if any(p in found.get(n, ()) for p in ps)
                  else "not_rendered") for k, ps in pk.items()} for n, pk in pieces.items()}
    return st, {n: dict(shas) for n in shared_n}


def seed_render_annotate(hbs: dict, by_key: dict) -> dict:
    """Run seed_render for every hit Claude-written seed literal of each set (hbs: set -> hits_by_eval; by_key: set ->
    {unit key: unit}) and store each status on its unit ("render"), which _aggregate reads. Returns the shared row
    files' sha256 per set (inputs_sha256.render_rows)."""
    need = {}
    for n, hb in hbs.items():
        ks = {k for ms in hb.values() for e in ms.values() for k in e["s"]}
        us = by_key.get(n) or {}
        need[n] = {k: us[k].get("render_text") or us[k]["texts"][0][1] for k in sorted(ks)
                   if k in us and not us[k].get("public")}
    if not any(need.values()):
        return {}
    t1 = time.time()
    st, shas = seed_render({n: v for n, v in need.items() if v},
                           {n: list(by_key[n].values()) for n in need if need[n]})
    for n, d in st.items():
        for k, s in d.items():
            by_key[n][k]["render"] = s
    print(f"  .. A31 (b) render check: {sum(map(len, st.values()))} hit seed literals, "
          f"{sum(s == 'not_rendered' for d in st.values() for s in d.values())} not rendered, "
          f"{time.time() - t1:.0f} s", flush=True)
    return shas


def run_sets(sets: dict, tgs: list[dict], out_dir: Path, cosine: Path | None = COSINE, side: bool = True,
             side_parallel: bool = True) -> dict:
    """sets: name -> (units, train_shas, seed_shas, train_path). ONE pass over the eval side for every set; each set's
    record is what a lone run of that set gives (exact / segment / table / substring / n-gram / MinHash hits are per
    training text; the embedding top-5 is per set). Writes <out_dir>/<name>.json per set; returns {name: rec}."""
    t0 = time.time()
    units, owner = [], []
    for name, (us, *_r) in sets.items():
        units += us
        owner += [name] * len(us)
    idx = TrainIndex(units)
    cfg = load_cosine(cosine)
    emb = Embed(cfg, cache=EmbCache(emb_dir(cfg))) if cfg else None
    scans = {None: Scan(idx, None, owner, defer=emb is not None)}
    for tg in tgs:                                  # A25 (c): mixdev sees the instance content only
        tf = tg.get("train_fields")
        if tf and not tg["status"] and tf not in scans:
            scans[tf] = Scan(TrainIndex(sub_units(units, tf)), None, owner, defer=emb is not None)
    side_tgs = [tg for tg in tgs if tg["kind"] == "sealed_side" and not tg["status"]]
    side_names = [tg["name"] for tg in side_tgs]
    side_h = sealed_side_start(units, owner, side_names, cosine) if side_tgs and side and side_parallel else None
    trec, eshas, why = {}, {}, _Why()
    for tg in tgs:
        r = trec[tg["name"]] = {"status": tg["status"] or "scanned", "blind": tg["blind"]}
        _tag(why, tg["name"])
        if tg["note"]:
            r["note"] = tg["note"]
        if tg.get("gap"):
            why.append(tg["gap"])
        if tg["status"]:
            if tg["status"] == "pending_owner":
                why.append(f"{tg['name']}: not scanned, owner decision pending")
            continue
        if tg["kind"] in EXTRA_KINDS or tg["kind"] == "sealed_side":      # unit-level / child process, below
            continue
        t1 = time.time()
        sc = scans[tg.get("train_fields")]
        ts: dict = {}
        sc.co = _Collect(emb.cache, emb.enc, quiet=True) if emb is not None and any(
            sp.startswith("hfstream:") for sp in tg["paths"]) else None
        stream(sc, tg, r, ts)
        sc.co = None
        eshas.update(ts)
        r["eval_files"] = sorted(ts)
        print(f"  .. {tg['name']}: {r['files']} files, {sc.items[tg['name']]} items, {time.time() - t1:.0f} s",
              flush=True)
        if r["files"] == 0:
            r["status"] = "missing"
            why.append(f"{tg['name']}: no input file found ({', '.join(tg['paths'])[:120]})")
        elif tg["sublabel"] and not sc.sub_rows.get(tg["sublabel"]["label"]):
            why.append(f"{tg['sublabel']['label']}: 0 rows matched the {r.get('sublabel_names', 0)} task names")
    _tag(why, None)
    if emb is None:
        why.append("embed (method 5): not run, the cosine threshold is not fixed yet (hand-check 100 open-set pairs "
                   "at 0.85 / 0.90 / 0.95, then write c_build/g13_cosine_threshold.json)")
    else:
        for k, sc in scans.items():
            if not any(len(v) for v in sc.ek.values()):     # no eval text noted (e.g. a mixdev-only refresh)
                continue
            t1 = time.time()
            er = embed_pass(sc, emb.bind(sc.idx, owner), why, tgs)
            print(f"  .. embed pass ({'main' if k is None else 'instance-only'}): {er} {time.time() - t1:.0f} s",
                  flush=True)
    side_res = {}
    if side_tgs and side and side_h is None:          # serial mode: one G13 process at a time
        side_h = sealed_side_start(units, owner, side_names, cosine)
    if side_h is not None:
        t1 = time.time()
        side_res = sealed_side_finish(side_h)
        for tg in side_tgs:
            sr = side_res.get(tg["name"]) or {}
            _tag(why, tg["name"])
            trec[tg["name"]].update({k: sr[k] for k in ("status", "files", "items", "short", "digest", "detail")
                                     if k in sr})
            if sr.get("status") != "scanned":
                trec[tg["name"]]["status"] = sr.get("status") or "failed"
                why.append(f"{tg['name']}: sealed-side child {sr.get('status', 'failed')}")
            elif not sr.get("files"):
                trec[tg["name"]]["status"] = "missing"
                why.append(f"{tg['name']}: sealed-side child found no input file")
            for g in sr.get("gaps") or []:
                why.append(f"{tg['name']}: {g}")
        _tag(why, None)
        print(f"  .. sealed side ({', '.join(t['name'] for t in side_tgs)}): waited {time.time() - t1:.0f} s",
              flush=True)
    elif side_tgs:
        _tag(why, [t["name"] for t in side_tgs])
        why.append("sealed side (OHS-3 / LongBench v2): not run in this call")
        _tag(why, None)
    out, pre = {}, {}
    tool_sha = sha256_file(Path(__file__))
    for name, (_, train_shas, seed_shas, train_path) in sets.items():
        mine = [ui for ui, o in enumerate(owner) if o == name]
        hb: dict = {}                               # label -> method -> {"u": {unit key: fields}, "s": [seed keys], "n"}

        def take(lb, m, got, n_ev):
            e = hb.setdefault(lb, {}).setdefault(m, {"u": {}, "s": [], "n": 0})
            for ui, fs in got.items():
                if units[ui]["seed"]:
                    e["s"].append(units[ui]["key"])
                else:
                    e["u"][units[ui]["key"]] = sorted(set(e["u"].get(units[ui]["key"], ())) | set(fs))
            e["n"] = None if n_ev is None or e["n"] is None else e["n"] + n_ev

        for sc in scans.values():
            ih = sc.items_by.get(name, {})
            for lb in sorted(ih):
                for m in sorted(ih[lb]):
                    if m.startswith("embed@") and m != f"embed@{name}":
                        continue
                    got = defaultdict(set)
                    for u in sc.hits[lb][m]:
                        for ui, f in sc.idx.occ[u]:
                            if owner[ui] == name and (m != "exact_short" or f != "option"):
                                got[ui].add(f)
                    take(lb, "embed" if m.startswith("embed@") else m, got, len(ih[lb][m]))
        for lb, res in side_res.items():
            for m, v in ((res.get("by_set") or {}).get(name) or {}).items():
                take(lb, m, {ui: {"sealed_side"} for ui in v["units"]}, v["eval_items"])
        trec_s, why_s = json.loads(json.dumps(trec)), _Why(why)
        su = [units[ui] for ui in mine]
        for lb, m, got, n_ev in extra_methods(su, tgs, trec_s, why_s, train_path, eshas):
            take(lb, m, {mine[i]: f for i, f in got.items()}, n_ev)
        for e in (e for ms in hb.values() for e in ms.values()):
            e["s"] = sorted(set(e["s"]))
        pre[name] = (mine, hb, trec_s, why_s)
    by_key = {n: {units[ui]["key"]: units[ui] for ui in pre[n][0]} for n in sets}
    render_rows = seed_render_annotate({n: pre[n][1] for n in sets}, by_key)     # A31 (b), one pass per row file
    for name, (_, train_shas, seed_shas, train_path) in sets.items():
        mine, hb, trec_s, why_s = pre[name]
        items, short, subr = Counter(), Counter(), Counter()
        for sc in scans.values():
            items.update(sc.items)
            short.update(sc.short)
            subr.update(sc.sub_rows)
        for lb, res in side_res.items():
            items[lb] += res.get("items") or 0
            short[lb] += res.get("short") or 0
        su_by_key = {units[ui]["key"]: units[ui] for ui in mine}
        fbt = {k: v["eval_files"] for k, v in trec_s.items() if len(v.get("eval_files", [None] * (FBT_MAX + 1)))
               <= FBT_MAX}
        for v in trec_s.values():
            v.pop("eval_files", None)
        rec = {
            "set": name, "tool": "c_build/decontam_g13.py", "tool_sha256": tool_sha,
            "spec": "C_DATA_SPEC 7.1 / 7.2 (blind counts-only mode); RUNBOOK B; PREREG A25 (c)-(e)",
            **_aggregate(hb, su_by_key),
            "train_units": sum(1 for ui in mine if not units[ui]["seed"]),
            "train_rows": sum(len(units[ui]["rows"]) for ui in mine),
            "seed_literals": sum(1 for ui in mine if units[ui]["seed"]),
            "eval_items": dict(items), "short_items": dict(short), "sublabel_rows": dict(subr),
            "targets": trec_s,
            "methods": methods_desc(tgs, emb is not None, cfg),
            "embed_stats": dict(emb.stats) if emb else None,
            "rules": {"unit": "call_id (every row of a hit unit is listed)", "min_words": MIN_WORDS, "ngram": NGRAM,
                      "tulu": [TULU_N, TULU_FRAC], "minhash": {"n": MH_N, "jaccard": MH_J, "edit": MH_EDIT,
                                                               "perms": MH_PERM, "bands": MH_BANDS},
                      "embed": {"top_k": 5, "per_set": True, **({k: cfg.get(k) for k in
                                ("threshold", "model", "max_seq_length", "dtype")} if cfg else {})},
                      "mixdev": "A25 (c): eval state + options vs training state + options only",
                      "table_hash": "header + cell set (training rows carry no table title); every public-2 "
                                    "container (markdown, pipe_plain, csv, json_records, key_value, html)",
                      "normalize": "NFKC, lower case, alphanumeric word runs"},
            "complete": not why_s, "incomplete_why": list(why_s), "why_by_target": why_s.pairs(),
            "hits_by_eval": hb,
            "files_by_target": fbt,
            "inputs_sha256": {"train": train_shas, "seeds": seed_shas, "eval": dict(eshas),
                              "render_rows": render_rows.get(name) or {},
                              "cosine": sha256_file(Path(cosine)) if cfg else None,
                              "sealed_side": {lb: res.get("digest") for lb, res in side_res.items()}},
            "wall_s": round(time.time() - t0, 1), "unix": round(time.time()),
        }
        if len(sets) > 1:
            rec["batch"] = {"sets": list(sets)}
        out_dir.mkdir(parents=True, exist_ok=True)
        tmp = out_dir / f".{name}.json.tmp"
        tmp.write_text(json.dumps(rec, indent=1))
        tmp.rename(out_dir / f"{name}.json")
        out[name] = rec
    return out


def run(set_name: str, units: list[dict], train_shas: dict, seed_shas: dict, tgs: list[dict], out_dir: Path,
        cosine: Path | None = COSINE, train_path: Path | None = None, side: bool = True) -> dict:
    """One set (a lone run) = run_sets with that one set."""
    return run_sets({set_name: (units, train_shas, seed_shas, train_path)}, tgs, out_dir, cosine, side)[set_name]


# ---- A25 (d): OHS-3 and LongBench v2, read ONLY in the sealed-side child process ------------------------------------
_HF_CALL = re.compile(r"(?:load_dataset|snapshot_download|hf_hub_download|list_repo_files|repo_id\s*=)\s*\(?\s*"
                      r"[\"']([A-Za-z0-9][\w.-]*/[\w.-]+)[\"']")
_HF_ANY = re.compile(r"(?<![\w./-])([A-Za-z0-9][\w.-]{0,95}/[\w.-]{1,95})(?![\w/-])")


def side_ok(p: Path) -> bool:
    """The child's guard: the sealed-side sets themselves, never sealed_nd / sealed_brief / runs / results / preds /
    Jev outputs."""
    r = rel_of(p)
    return not SIDE_NEVER.search(r) and not JEV.search(r)


def _ohs3_hf(gaps: list) -> list[Path]:
    """CHILD ONLY. OHS-3's source datasets: HF ids named in lean/ohs3/** (code / config), read in this process only;
    every id with a local HF snapshot is scanned (all splits). Ids named in a dataset call but not cached are a gap
    (counted, never named)."""
    root, strict, loose = LEAN / "ohs3", set(), set()
    for p in sorted(root.rglob("*")) if root.exists() else []:
        if not p.is_file() or p.suffix not in {".py", ".json", ".yaml", ".yml", ".sh", ".txt", ".md"} or \
                not side_ok(p) or p.stat().st_size > 5_000_000:
            continue
        t = p.read_text(errors="replace")
        strict |= set(_HF_CALL.findall(t))
        loose |= set(_HF_ANY.findall(t))
    cached = {r for r in strict | loose if (HF / ("datasets--" + r.replace("/", "--")) / "snapshots").is_dir()}
    if strict - cached:
        gaps.append(f"{len(strict - cached)} OHS-3 source dataset(s) named in a dataset call are not in the local HF "
                    "cache (not scanned)")
    return [p for r in sorted(cached) for p in resolve("hf:" + r)]


def side_files(name: str, gaps: list) -> list[Path]:
    """CHILD ONLY: the files of one sealed-side target."""
    out = []
    for spec in SEALED_SIDE[name]:
        out += _ohs3_hf(gaps) if spec == "ohs3hf:" else resolve(spec)
    seen, keep = set(), []
    for p in out:
        if p.resolve() not in seen and side_ok(p):
            seen.add(p.resolve())
            keep.append(p)
    return keep


def _digest(shas: dict) -> str:
    return hashlib.sha256("\n".join(sorted(shas.values())).encode()).hexdigest()


def sealed_side_child(units_path: Path, names: list[str], cosine: Path | None, out_path: Path,
                      mode: str = "scan") -> int:
    """CHILD ONLY (`decontam_g13.py sealedside`). Reads the training units the parent wrote, scans the sealed-side
    targets with methods 1-5 + tables, and writes ONLY integers, unit indices and sha digests to `out_path`.
    mode "digest": input digests only (the stale check); "census": file / item counts only."""
    units, owner = [], []
    if mode == "scan":
        with open(units_path) as f:
            for line in f:
                d = json.loads(line)
                units.append({"key": str(len(units)), "rows": [], "source": "", "seed": bool(d["s"]),
                              "texts": [tuple(x) for x in d["t"]]})
                owner.append(d["o"])
    idx = TrainIndex(units) if mode == "scan" else None
    cfg = load_cosine(cosine) if mode in ("scan", "embed") else None
    emb = Embed(cfg, cache=EmbCache(emb_dir(cfg))) if cfg else None
    if emb is not None and os.environ.get("G13_SIDE_CACHE", "1") != "0":
        emb.side = SideCache(side_emb_dir(cfg))
    if mode == "embed" and (emb is None or emb.side is None):
        raise RuntimeError("embed mode needs the cosine file and G13_SIDE_CACHE on")
    res, t00 = {}, time.time()
    try:
        for name in names:
            res[name] = _side_one(name, mode, idx, units, owner, emb, t00, res)
    finally:
        if emb is not None and emb.side is not None:
            emb.side.flush()
    out_path.write_text(json.dumps(res))
    return 0


def _side_progress(res: dict, name: str, t00: float, **kw) -> None:
    """CHILD ONLY: counts / seconds per sealed-side target (no text, no file or source name) for the orchestrator."""
    dest = os.environ.get("G13_SIDE_PROGRESS")      # set by sealed_side_start; unset (tests, digest checks): no file
    if not dest:
        return
    try:
        cur = {**{k: {kk: v.get(kk) for kk in ("status", "files", "items", "s")} for k, v in res.items()},
               name: kw, "unix": round(time.time()), "since_start_s": round(time.time() - t00)}
        Path(dest).parent.mkdir(parents=True, exist_ok=True)
        tmp = Path(dest).with_name("." + Path(dest).name + ".tmp")
        tmp.write_text(json.dumps(cur))
        tmp.rename(dest)
    except OSError:
        pass


def _side_one(name: str, mode: str, idx, units: list, owner: list, emb, t00: float, res: dict) -> dict:
    """CHILD ONLY: one sealed-side target (scan / digest / census / embed). Integers, unit indices, digests only."""
    gaps: list = []
    files = side_files(name, gaps)
    shas: dict = {}
    t1 = time.time()
    _side_progress(res, name, t00, status="running", files=len(files))
    if mode == "digest":
        for p in files:
            if p.suffix.lower() in DATA_EXT:
                shas[str(p)] = sha256_file(p)
        return {"status": "scanned", "files": len(shas), "digest": _digest(shas)}
    last = [0.0]

    def on_file(i, n, sc=None):
        if time.time() - last[0] >= 60:
            last[0] = time.time()
            _side_progress(res, name, t00, status="running", files=n, files_done=i,
                           items=(sc.items[name] if sc is not None else None), s=round(time.time() - t1),
                           **({"added": sc.added} if hasattr(sc, "added") else {}))
    if mode == "embed":                             # prebuild the child's own vector cache (SideCache), counts only
        col = _Collect(_SideHas(emb), emb.enc, quiet=True)
        col.on_file = lambda i, n: on_file(i, n, col)
        tg = target(name, [], kind="rows", blind=True, tables=True)
        rec: dict = {}
        stream(col, tg, rec, shas, files=files, ok=side_ok)
        col.flush(force=True)
        emb.side.flush()
        r = {"status": "scanned", "files": rec.get("files", 0), "items": col.items[name], "added": col.added,
             "skipped": col.skipped, "digest": _digest(shas), "gaps": len(gaps), "s": round(time.time() - t1)}
        _side_progress(res, name, t00, **{k: r[k] for k in ("status", "files", "items", "added", "s")})
        return r
    tg = target(name, [], kind="rows", blind=True, tables=True)
    sc = Scan(idx if idx is not None else TrainIndex([]),
              emb.bind(idx, owner) if (emb and mode == "scan") else None, owner)
    sc.on_file = lambda i, n: on_file(i, n, sc)
    rec: dict = {}
    stream(sc, tg, rec, shas, files=files, ok=side_ok)
    r = {"status": "scanned", "files": rec.get("files", 0), "items": sc.items[name], "short": sc.short[name],
         "digest": _digest(shas), "gaps": gaps,
         "detail": {"unsupported_files": sum((rec.get("unsupported_files") or {}).values())}}
    if mode == "scan":
        by: dict = {}
        for st, lbs in sc.items_by.items():
            for m, its in (lbs.get(name) or {}).items():
                if m.startswith("embed@") and m != f"embed@{st}":
                    continue
                us = sorted({ui for u in sc.hits[name][m] for ui, f in idx.occ[u]
                             if owner[ui] == st and not units[ui]["seed"] and (m != "exact_short" or f != "option")})
                by.setdefault(st, {})["embed" if m.startswith("embed@") else m] = {"units": us,
                                                                                     "eval_items": len(its)}
        r["by_set"] = by
        r["detail"]["embed"] = dict(emb.stats) if emb else None
    r["s"] = round(time.time() - t1)
    _side_progress(res, name, t00, status=r["status"], files=r["files"], items=r["items"], s=r["s"],
                   embed=(dict(emb.stats) if emb else None))
    return r


class _SideHas:
    """CHILD ONLY: the cache view `embed` mode fills: a key counts as cached when the parent's EmbCache (open sets) or
    the child's SideCache has it; new vectors go to the SideCache only."""

    def __init__(self, emb):
        self.emb = emb

    def has(self, keys: np.ndarray) -> np.ndarray:
        h = self.emb.cache.has(keys) if self.emb.cache is not None and len(self.emb.cache) else \
            np.zeros(len(keys), bool)
        return h | self.emb.side.has(keys) | member(np.unique(np.concatenate(self.emb.side.bk))
                                                     if self.emb.side.bk else np.empty(0, np.uint64), keys)

    def add(self, keys, vecs) -> None:
        self.emb.side.put(np.asarray(keys, np.uint64), vecs)


def _side_busy() -> bool:
    """True while another sealed-side child process (`decontam_g13.py sealedside`, any mode) is alive."""
    try:
        out = subprocess.run(["pgrep", "-f", "decontam_g13.py sealedside"], capture_output=True, text=True,
                             timeout=30).stdout
    except (OSError, subprocess.SubprocessError):
        return False
    return any(x.strip().isdigit() and int(x) != os.getpid() for x in out.split())


def sealed_side_start(units: list[dict], owner: list, names: list[str], cosine: Path | None, mode: str = "scan",
                      py: str = sys.executable) -> dict:
    """PARENT: start the sealed-side child in its own process (it runs while the parent scans the open eval side).
    Scan / embed children never run two at once: while another sealed-side child is alive (e.g. a `side-embed-cache`
    prebuild filling the same SideCache) this waits (G13_SIDE_WAIT s, default 12 h; polls every 60 s), then gives up
    with status 'busy' (the log stays incomplete; `refresh --targets ohs3 ohs3_src longbench_v2` later)."""
    if mode in ("scan", "embed"):
        t_end = time.time() + int(os.environ.get("G13_SIDE_WAIT", 12 * 3600))
        while _side_busy() and time.time() < t_end:
            time.sleep(60)
        if _side_busy():
            return {"proc": None, "td": None, "out": None, "names": names}
    td = tempfile.mkdtemp(dir=str(HERE / "tmp") if (HERE / "tmp").is_dir() else None)
    up, op = Path(td) / "units.jsonl", Path(td) / "side.json"
    with open(up, "w") as f:
        for u, o in zip(units, owner):
            f.write(json.dumps({"o": o, "s": u["seed"], "t": u["texts"]}) + "\n")
    cmd = [py, str(Path(__file__).resolve()), "sealedside", "--units", str(up), "--out", str(op),
           "--side-mode", mode, "--side-names", *names] + (["--cosine", str(cosine)] if cosine else [])
    ef = open(Path(td) / "err.txt", "w")            # a file, not a pipe: the child never blocks on a full pipe
    env = {**os.environ}
    if mode in ("scan", "embed"):
        env["G13_SIDE_PROGRESS"] = str(OUT / "run" / f"side_progress_{mode}.json")
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=ef, cwd=str(LEAN), env=env)
    ef.close()
    return {"proc": proc, "td": td, "out": op, "names": names}


def sealed_side_finish(h: dict, timeout: int | None = None) -> dict:
    """PARENT: wait for the child (G13_SIDE_TIMEOUT seconds, default 24 h: on a busy Mac at nice 10 the live
    embedding of OHS-3 + its sources + LongBench took > 6 h on 6 Oct); read back counts, unit indices and digests only
    (never its inputs)."""
    timeout = timeout or int(os.environ.get("G13_SIDE_TIMEOUT", 24 * 3600))
    import shutil
    if h["proc"] is None:
        return {n: {"status": "failed (busy: another sealed-side child was running)"} for n in h["names"]}
    try:
        h["proc"].wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        h["proc"].kill()
        h["proc"].wait()
    ep = Path(h["td"]) / "err.txt"
    err = ep.read_text(errors="replace") if ep.exists() else ""
    d = jload(h["out"]) if Path(h["out"]).exists() else None
    shutil.rmtree(h["td"], ignore_errors=True)
    if h["proc"].returncode != 0 or not isinstance(d, dict):
        last = [x for x in (err or "").splitlines() if x.startswith("sealedside error:")]
        return {n: {"status": f"failed (exit {h['proc'].returncode}; {(last or ['?'])[-1][:60]})"} for n in h["names"]}
    return d


def sealed_side_run(units: list[dict], owner: list, names: list[str], cosine: Path | None,
                    mode: str = "scan", py: str = sys.executable) -> dict:
    """PARENT: run the sealed-side child to the end (digest / census modes, and tests)."""
    return sealed_side_finish(sealed_side_start(units, owner, names, cosine, mode, py))


# ---- log checks (r1_check.py preflight, autopilot_check.py) -----------------------------------------------------------
_SHA: dict = {}
_SIDE_DIGEST: dict = {}


def _sha_memo(f: Path) -> str:
    """sha256 of a file, re-hashed whenever its size or mtime changes (several logs share most eval files)."""
    st = Path(f).stat()
    k = (str(Path(f).resolve()), st.st_size, st.st_mtime_ns)
    if k not in _SHA:
        _SHA[k] = sha256_file(f)
    return _SHA[k]


def eval_path(k: str) -> Path | None:
    """A recorded eval key (rel_of: relative to the repo, the HF hub cache or ~/.cache/opendecide_ext) as a path."""
    for root in (REPO, HF, GH.parent):
        f = root / k
        if f.exists():
            return f
    return None


def eval_files_now() -> set[str]:
    """The eval files a run would read now (the keys rel_of gives), for the targets read by this process."""
    now = set()
    for tg in targets():
        now |= target_files_now(tg)
    return now


def eval_stale(d: dict) -> str | None:
    """A25 (e) eval-side stale check: every eval input the run read still has its sha256, no new eval file has appeared
    (a new mixdev, a new projected parquet ...), the cosine file is unchanged, and the sealed side's input digests
    (re-hashed by the child, counts only) are unchanged."""
    ins = d.get("inputs_sha256") or {}
    ev = ins.get("eval") or {}
    if not ev:
        return "no eval input hashes in the log (older tool)"
    for k, sha in ev.items():
        if k.startswith("hfstream:"):
            continue
        f = eval_path(k)
        if f is None or _sha_memo(f) != sha:
            return f"{k[:70]} changed or gone"
    new = eval_files_now() - set(ev)
    if new:
        return f"{len(new)} eval file(s) not in the run, e.g. {sorted(new)[0][:70]}"
    cfg = load_cosine(COSINE)
    if (ins.get("cosine") or None) != (_sha_memo(COSINE) if cfg else None):
        return "g13_cosine_threshold.json changed"
    side = {k: v for k, v in (ins.get("sealed_side") or {}).items() if v}   # a failed child has no digest
    if side:
        key = tuple(sorted(side))
        if key not in _SIDE_DIGEST:
            r = sealed_side_run([], [], list(key), None, mode="digest")
            _SIDE_DIGEST[key] = {n: (r.get(n) or {}).get("digest") for n in key}
        if any(_SIDE_DIGEST[key].get(n) != side[n] for n in key):
            return "a sealed-side input digest changed"
    return None


def log_problems(names, out_dir: Path = OUT) -> list[str]:
    p = []
    for n in names:
        d = jload(out_dir / f"{n}.json")
        if d is None:
            p.append(f"G13 {n}: no logs/decontam_counts/{n}.json (RUNBOOK B)")
            continue
        if not isinstance(d.get("drop_ids"), list):
            p.append(f"G13 {n}: no drop_ids list")
        if not d.get("complete"):
            p.append(f"G13 {n}: incomplete ({len(d.get('incomplete_why') or [])} reasons; first: "
                     f"{(d.get('incomplete_why') or ['?'])[0][:90]})")
        for path, sha in {**(d.get("inputs_sha256") or {}).get("train", {}),
                          **(d.get("inputs_sha256") or {}).get("seeds", {})}.items():
            f = LEAN / path
            if not f.exists() or _sha_memo(f) != sha:
                p.append(f"G13 {n}: stale ({path} changed after the run; re-run)")
                break
        if (d.get("seed_render") or {}).get("report_only_not_rendered"):
            rr = (d.get("inputs_sha256") or {}).get("render_rows") or {}
            now = [x for x in RENDER_SHARED if (LEAN / x).exists()] if n in SEED_SETS else []
            for path in list(rr) + [x for x in now if x not in rr]:
                f = LEAN / path
                if not f.exists() or _sha_memo(f) != rr.get(path):
                    p.append(f"G13 {n}: A31 (b) render check stale ({path} changed or new after the run; "
                             "`refresh`)")
                    break
        st = eval_stale(d)
        if st:
            hint = "`refresh` (mixdev only)" if refresh_problem(d) is None else "re-run"
            p.append(f"G13 {n}: stale eval side ({st}; {hint})")
        ms = d.get("methods") or {}
        old = [k for k in ("structure", "template", "sealed", "sealed_side", "embed", "template_rev")
               if str(ms.get(k, "not_run")).startswith("not_run")]
        if "container" not in str(((d.get("rules") or {}).get("table_hash")) or ""):
            old.append("table (all public-2 containers)")
        if old:
            p.append(f"G13 {n}: methods {old} (spec 7.2 5-9, A25) not run in this log (older tool; re-run)")
        if d.get("seeds_clean") is False:
            p.append(f"G13 {n}: {len(d.get('seed_hit_locs') or [])} Claude-written seed literal(s) hit an eval set "
                     "(builder fixes the seed, then re-run)")
        if n == "final_mix_r1" and d.get("drop_ids"):
            p.append(f"G13 on the final mix still has {len(d['drop_ids'])} hits (drop and re-run mixer --final)")
    return p


MIXDEV_FREEZE = OUT / "MIXDEV_FREEZE.json"


def mixdev_now() -> dict:
    """{repo-relative key: sha256} of every main mixdev file now (the files `mixdev` / `mixdev_structure` read)."""
    return {rel_of(f): _sha_memo(f) for f in mixdev_files()}


def freeze_mixdev() -> int:
    """Record the mixdev files as they are now (MIXDEV_FREEZE.json). The orchestrator freezes before a batch and tells
    the lanes; `status` then names every mixdev file that changed after the freeze. Counts and shas only."""
    now = mixdev_now()
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / ".MIXDEV_FREEZE.json.tmp"
    tmp.write_text(json.dumps({"unix": round(time.time()), "files": now}, indent=1))
    tmp.rename(MIXDEV_FREEZE)
    print(f"mixdev frozen: {len(now)} files")
    return 0


def mixdev_freeze_drift() -> list[str]:
    """Mixdev files changed, added or gone since MIXDEV_FREEZE.json ([] when no freeze is recorded)."""
    fr = (jload(MIXDEV_FREEZE) or {}).get("files")
    if not isinstance(fr, dict):
        return []
    now = mixdev_now()
    return sorted(k for k in set(fr) | set(now) if fr.get(k) != now.get(k))


def target_files_now(tg: dict) -> set[str]:
    """The eval file keys one target would read now (as eval_files_now; sealed-side / sealed-check: none here)."""
    if tg["status"] or tg["kind"] in ("sealed_side", "sealed_check"):
        return set()
    if tg["kind"] == "structure":
        fs = mixdev_files()
    elif tg["kind"] == "templates":
        fs = [f for f in (LEAN / OPI_BUILDER, LEAN / "data/eval_jagged.jsonl") if f.exists()]
    else:
        fs = [f for spec in tg["paths"] if not spec.startswith("hfstream:") for f in resolve(spec)
              if allowed(f) and f.suffix.lower() in DATA_EXT and (not tg.get("main_only") or f.name.count(".") == 1)]
    return {rel_of(f) for f in fs}


def refresh_labels(tgs: list[dict]) -> set:
    """The eval labels a set of targets owns: the target names and their sublabels (e.g. forbidden152)."""
    return {t["name"] for t in tgs} | {t["sublabel"]["label"] for t in tgs if t.get("sublabel")}


def refresh_problem(d: dict, tnames=REFRESHABLE) -> str | None:
    """None when a log may be refreshed on targets `tnames`: written by this tool version, training side unchanged,
    every eval input OUTSIDE those targets unchanged (no new eval file outside them), cosine unchanged, and the old
    log recorded those targets' files. Else why a full run is needed. The sealed-side digests of targets not
    refreshed are re-checked by log_problems afterwards, as for any log."""
    if not isinstance(d, dict) or not isinstance(d.get("hits_by_eval"), dict) or "why_by_target" not in d:
        return "the log predates refresh (no hits_by_eval / why_by_target): one full run first"
    if d.get("tool_sha256") != sha256_file(Path(__file__)):
        return "the tool changed after this log was written: full run"
    ins = d.get("inputs_sha256") or {}
    for path, sha in {**(ins.get("train") or {}), **(ins.get("seeds") or {})}.items():
        f = LEAN / path
        if not f.exists() or _sha_memo(f) != sha:
            return f"training side changed ({path}): full run"
    tgs = [t for t in targets() if t["name"] in tnames]
    if len(tgs) != len(set(tnames)):
        return f"unknown target in {sorted(tnames)}"
    fbt = d.get("files_by_target") or {}
    for t in tgs:
        if t["kind"] not in ("sealed_side", "sealed_check") and not t["status"] and t["name"] not in fbt:
            return f"{t['name']}: the log did not record this target's files (> {FBT_MAX} files?): full run"
    old_mine = {k for t in tgs for k in (fbt.get(t["name"]) or [])}
    ev = ins.get("eval") or {}
    for k, sha in ev.items():
        if k in old_mine or k.startswith("hfstream:"):
            continue
        f = eval_path(k)
        if f is None or _sha_memo(f) != sha:
            return f"{k[:70]} changed or gone (outside {sorted(tnames)}): full run"
    now_mine = set().union(*(target_files_now(t) for t in tgs)) if tgs else set()
    new = eval_files_now() - set(ev) - now_mine
    if new:
        return f"{len(new)} new eval file(s) outside {sorted(tnames)}, e.g. {sorted(new)[0][:70]}: full run"
    cfg = load_cosine(COSINE)
    if (ins.get("cosine") or None) != (_sha_memo(COSINE) if cfg else None):
        return "g13_cosine_threshold.json changed: full run"
    return None


def refresh(names: list[str], tnames=REFRESHABLE, out_dir: Path = OUT, cosine: Path | None = COSINE) -> int:
    """Re-scan ONLY the eval targets `tnames` (default: mixdev + mixdev_structure, which lanes rewrite; also e.g. the
    sealed-side targets after a failed child, or big_patent with G13_BIGPAT_STREAM=1) for every named set in one pass,
    and merge into each log exactly as a full run computes it (_aggregate over hits_by_eval): the other targets'
    hits, reasons and input shas are kept. Counts only. Refuses (exit 1) when a full run is needed."""
    tnames = tuple(dict.fromkeys(tnames))
    logs, refuse = {}, []
    for n in names:
        d = jload(out_dir / f"{n}.json")
        why = refresh_problem(d, tnames) if d else "no log: full run"
        if why:
            refuse.append(f"G13 {n}: refresh refused ({why})")
        else:
            logs[n] = d
    if refuse:
        print("\n".join(refuse))
        return 1
    tgs = [t for t in targets() if t["name"] in tnames]
    labels = refresh_labels(tgs)
    sets = {n: build_set(n) for n in names}
    side_on = any(t["kind"] == "sealed_side" for t in tgs)
    with tempfile.TemporaryDirectory(dir=str(HERE / "tmp") if (HERE / "tmp").is_dir() else None) as td:
        new = run_sets(sets, tgs, Path(td), cosine=cosine, side=side_on)
    hbs, ukeys = {}, {}
    for n, d in logs.items():
        r = new[n]
        hb = hbs[n] = {lb: v for lb, v in d["hits_by_eval"].items() if lb not in labels}
        hb.update({lb: v for lb, v in r["hits_by_eval"].items() if lb in labels})
        ukeys[n] = {u["key"]: u for u in sets[n][0]}
    render_rows = seed_render_annotate(hbs, ukeys)     # A31 (b) on the merged hits, with today's training rows
    for n, d in logs.items():
        r, hb, units = new[n], hbs[n], ukeys[n]
        wbt = [[t, w] for t, w in d["why_by_target"] if not set(t) <= labels]
        wbt += [[t, w] for t, w in r["why_by_target"] if set(t) <= labels]
        fbt_old = d.get("files_by_target") or {}
        old_mine = {k for t in tnames for k in (fbt_old.get(t) or [])}
        ev = {k: v for k, v in d["inputs_sha256"]["eval"].items()
              if k not in old_mine and not (k.startswith("hfstream:") and any(
                  k.startswith("hfstream:" + sp.split(":", 1)[1].split("|")[0])
                  for t in tgs for sp in t["paths"] if sp.startswith("hfstream:")))}
        ev.update(r["inputs_sha256"]["eval"])
        side = {**(d["inputs_sha256"].get("sealed_side") or {}),
                **{k: v for k, v in (r["inputs_sha256"].get("sealed_side") or {}).items() if k in labels}}
        rec = dict(d)
        rec.update(_aggregate(hb, units))
        rec["hits_by_eval"] = hb
        rec["why_by_target"] = wbt
        rec["incomplete_why"] = [w for _, w in wbt]
        rec["complete"] = not wbt
        rec["inputs_sha256"] = {**d["inputs_sha256"], "eval": ev, "sealed_side": side,
                                "render_rows": render_rows.get(n) or {}}
        rec["files_by_target"] = {**{k: v for k, v in fbt_old.items() if k not in tnames}, **r["files_by_target"]}
        rec["targets"] = {**d["targets"], **{t: r["targets"][t] for t in tnames if t in r["targets"]}}
        for key in ("eval_items", "short_items", "sublabel_rows"):
            rec[key] = {**{k: v for k, v in (d.get(key) or {}).items() if k not in labels},
                        **{k: v for k, v in (r.get(key) or {}).items() if k in labels}}
        rec["refreshed"] = (d.get("refreshed") or []) + [{
            "unix": round(time.time()), "targets": list(tnames), "wall_s": r["wall_s"],
            "files_before": len(old_mine), "files_now": sum(len(v) for k, v in r["files_by_target"].items()
                                                           if k in tnames),
            "embed_stats": r.get("embed_stats")}]
        rec["unix"] = round(time.time())
        tmp = out_dir / f".{n}.json.tmp"
        tmp.write_text(json.dumps(rec, indent=1))
        tmp.rename(out_dir / f"{n}.json")
        print(f"G13 {n} refreshed ({', '.join(tnames)}): drop units {rec['drop_units']} rows {len(rec['drop_ids'])} | "
              f"seeds_clean {rec['seeds_clean']} | complete {rec['complete']} ({len(rec['incomplete_why'])} reasons)")
    return 0


def fetch_bigpat(cap_bytes: int = 2_100_000_000) -> int:
    """A25 (e): big_patent ('all' config, pinned revision = ohs2's) column-projected into PROJ: the abstract of every
    split and the test descriptions (BIGPAT_COLS). Only those column chunks are downloaded (HTTP range reads). Resumable:
    a finished file is skipped; a file is written to .tmp and renamed only when complete. Prints counts only."""
    import pyarrow.parquet as pq
    from huggingface_hub import HfApi, HfFileSystem
    dst = PROJ / BIGPAT.replace("/", "--")
    dst.mkdir(parents=True, exist_ok=True)
    manp = dst / "fetch_manifest.json"
    man = jload(manp) or {"repo": BIGPAT, "revision": BIGPAT_REV, "columns": BIGPAT_COLS, "files": {}}
    files = sorted(f for f in HfApi().list_repo_files(BIGPAT, repo_type="dataset", revision=BIGPAT_REV)
                   if f.startswith("all/") and f.endswith(".parquet"))
    fs, got = HfFileSystem(), sum(v.get("column_bytes", 0) for v in man["files"].values())
    for i, f in enumerate(files):
        out = dst / f
        if out.exists() and f in man["files"]:
            continue
        cols = BIGPAT_COLS[f.split("/")[1].split("-")[0]]
        with fs.open(f"datasets/{BIGPAT}@{BIGPAT_REV}/{f}", "rb", block_size=1 << 20) as fh:
            pf = pq.ParquetFile(fh)
            md, names = pf.metadata, pf.schema_arrow.names
            nb = sum(md.row_group(g).column(j).total_compressed_size for g in range(md.num_row_groups)
                     for j in range(md.num_columns) if names[j] in cols)
            if got + nb > cap_bytes:
                print(f"fetch: stop before {f} (cap {cap_bytes / 1e9:.1f} GB; {got / 1e9:.2f} GB fetched)", flush=True)
                break
            tbl = pf.read(columns=list(cols))
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_name(out.name + ".tmp")
        pq.write_table(tbl, tmp, compression="zstd")
        tmp.rename(out)
        got += nb
        man["files"][f] = {"rows": tbl.num_rows, "columns": list(cols), "column_bytes": nb, "sha256": sha256_file(out)}
        manp.write_text(json.dumps(man, indent=1))
        print(f"fetch {i + 1}/{len(files)}: {tbl.num_rows} rows, {nb / 1e6:.0f} MB (total {got / 1e9:.2f} GB)",
              flush=True)
    done = all(f in man["files"] and (dst / f).exists() for f in files)
    man["complete"] = done
    manp.write_text(json.dumps(man, indent=1))
    print(f"fetch: {sum(f in man['files'] for f in files)}/{len(files)} files, {got / 1e9:.2f} GB, complete {done}")
    return 0 if done else 1


CALIB_PLAN = HERE / "g13_cosine_calib_plan.json"


def calib(fams, out: Path, plan_path: Path = CALIB_PLAN) -> int:
    """Method 5 calibration pairs (spec 7.2 5; A25 e), exactly as g13_cosine_calib_plan.json fixes it before any pair
    exists: open C rows only (never an eval set), one state text per unit, n texts drawn with a fixed seed, every pair
    of units that share no group_id with cosine >= 0.85, `per_band` pairs drawn per band with the same seed."""
    plan = jload(plan_path)
    if not plan:
        raise SystemExit(f"{plan_path.name} missing: write the calibration plan first")
    texts, meta = [], []
    for f in fams:
        for un in train_units(LEAN / f"c_src/{f}/out/candidates_r1.jsonl"):
            st = next((t for fld, t in un["texts"] if fld == "state"), None)
            if st and len(words(st)) >= MIN_WORDS:
                texts.append(st)
                meta.append({"fam": f, "unit": un["key"], "groups": sorted(un["groups"]), "struct": sorted(un["struct"])})
    rng = np.random.default_rng(int(plan["seed"]))
    pick = rng.permutation(len(texts))[:int(plan["n_texts"])]
    texts, meta = [texts[i] for i in pick], [meta[i] for i in pick]
    E = Encoder(plan)(texts).astype(np.float32)
    S = E @ E.T
    iu, ju = np.triu_indices(len(texts), 1)
    s = S[iu, ju]
    keep = s >= min(plan["bands"])
    iu, ju, s = iu[keep], ju[keep], s[keep]
    ok = np.array([not (set(meta[i]["groups"]) & set(meta[j]["groups"])) for i, j in zip(iu.tolist(), ju.tolist())],
                  bool)
    iu, ju, s = iu[ok], ju[ok], s[ok]
    bands = sorted(plan["bands"])
    pairs, pool = [], {}
    for k, b in enumerate(bands):
        hi = bands[k + 1] if k + 1 < len(bands) else 9.0
        sel = np.nonzero((s >= b) & (s < hi))[0]
        pool[str(b)] = int(len(sel))
        take = rng.permutation(sel)[:int(plan["per_band"])]
        for t in sorted(take.tolist(), key=lambda t: -s[t]):
            i, j = int(iu[t]), int(ju[t])
            pairs.append({"pair": len(pairs), "band": b, "cos": round(float(s[t]), 4),
                          "same_family": meta[i]["fam"] == meta[j]["fam"],
                          "same_structure_hash": bool(set(meta[i]["struct"]) & set(meta[j]["struct"])),
                          "a_fam": meta[i]["fam"], "b_fam": meta[j]["fam"], "a_unit": meta[i]["unit"],
                          "b_unit": meta[j]["unit"], "a": texts[i], "b": texts[j]})
    out.write_text("".join(json.dumps(x) + "\n" for x in pairs))
    print(json.dumps({"texts": len(texts), "pool_by_band": pool, "pairs": len(pairs),
                      "same_family": sum(p["same_family"] for p in pairs)}))
    return 0


class _Collect:
    """`embed-cache`: a Scan stand-in that gathers the texts the embedding method sees (targets with methods 'all',
    texts of >= 5 words), encodes the ones the cache lacks and writes them as shards. Resumable (keys already cached
    are skipped)."""

    def __init__(self, cache: EmbCache, enc: Encoder, shard: int = 50_000, quiet: bool = False):
        self.items, self.short, self.sub_rows = Counter(), Counter(), Counter()
        self.cache, self.enc, self.shard, self.quiet = cache, enc, shard, quiet
        self.pk, self.pr, self.seen = [], [], set()
        self.added = self.skipped = 0

    def add_item(self, labels, texts, methods, want_tables) -> None:
        self.items[labels[0]] += 1
        if methods != "all":
            return
        for raw, _c in texts:
            ws = words(raw)
            if len(ws) < MIN_WORDS:
                continue
            k = hseq(ws)
            if k not in self.seen:
                self.seen.add(k)
                self.pk.append(k)
                self.pr.append(raw)
        if len(self.pk) >= self.shard:
            self.flush(force=True)

    def flush(self, force: bool = False) -> None:
        if not self.pk or (not force and len(self.pk) < self.shard):
            return
        keys = np.array(self.pk, np.uint64)
        new = np.nonzero(~self.cache.has(keys))[0]
        self.skipped += len(keys) - len(new)
        if len(new):
            V = self.enc([self.pr[i] for i in new.tolist()])
            self.cache.add(keys[new].tolist(), V)
            self.added += len(new)
            if not self.quiet:
                print(f"  embed-cache: +{len(new)} (total added {self.added}, skipped {self.skipped})", flush=True)
        self.pk, self.pr = [], []


def build_emb_cache(plan_path: Path = CALIB_PLAN, only: list | None = None) -> int:
    """Encode every eval text the embedding method will see, once, into EmbCache (vectors only). Counts only."""
    plan = jload(COSINE) or jload(plan_path)
    if not plan or not plan.get("model"):
        raise SystemExit("no model fixed (g13_cosine_calib_plan.json / g13_cosine_threshold.json)")
    cache = EmbCache(emb_dir(plan))
    cache.d.mkdir(parents=True, exist_ok=True)
    lock = cache.d / f"BUILDING.{os.getpid()}"         # one lock per builder; a run waits while any is alive
    lock.write_text(str(os.getpid()))
    try:
        return _build(plan, cache, only)
    finally:
        lock.unlink(missing_ok=True)


def _build(plan: dict, cache: EmbCache, only=None, tgs: list | None = None, enc=None) -> int:
    col = _Collect(cache, enc or Encoder(plan))
    t0 = time.time()
    for tg in (tgs if tgs is not None else targets()):
        if tg["status"] or tg["kind"] in EXTRA_KINDS + ("sealed_side", "instr") or tg["methods"] != "all":
            continue
        if only and tg["name"] not in only:
            continue
        r: dict = {}
        stream(col, tg, r, {})
        col.flush(force=True)
        print(f"  .. {tg['name']}: {r.get('files')} files, {col.items[tg['name']]} items, {col.added} new vectors so "
              f"far, {time.time() - t0:.0f} s", flush=True)
        cache = col.cache = EmbCache(emb_dir(plan))
    print(f"embed-cache done: {len(cache)} vectors, {col.added} added this run, {time.time() - t0:.0f} s")
    return 0


SETS = FAMS + sorted(SEED_SETS) + ["final_mix_r1"]


def build_set(name: str) -> tuple:
    """(units, train_shas, seed_shas, train_path) of one set: a family's candidates (selection + refill pool) and its
    Claude-written seeds; the final mix; or a shared seed set (packs / formats)."""
    if name in FAMS:
        cand = LEAN / f"c_src/{name}/out/candidates_r1.jsonl"
        if not cand.exists():
            raise SystemExit(f"{cand.relative_to(LEAN)} missing: nothing to decontaminate")
        seeds, seed_shas = seed_units(LEAN / f"c_src/{name}/gen", LEAN)
        return train_units(cand) + seeds, {cand.relative_to(LEAN).as_posix(): sha256_file(cand)}, seed_shas, cand
    if name == "final_mix_r1":
        cand = LEAN / FINAL_TRAIN
        if not cand.exists():
            raise SystemExit(f"{FINAL_TRAIN} missing: run mixer.py --final first (RUNBOOK C2)")
        return train_units(cand), {FINAL_TRAIN: sha256_file(cand)}, {}, cand
    if name in SEED_SETS:
        seeds, seed_shas = seed_units(LEAN / SEED_SETS[name], LEAN)
        return seeds, {}, seed_shas, None
    raise SystemExit(f"unknown set {name!r} (one of {SETS})")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="G13 counts-only decontamination (spec 7; RUNBOOK B)")
    ap.add_argument("cmd", nargs="?", default="run",
                    choices=("run", "status", "targets", "calib", "fetch", "embed-cache", "sealedside", "census",
                             "side-embed-cache", "freeze-mixdev", "refresh"))
    ap.add_argument("names", nargs="*")
    ap.add_argument("--fam")
    ap.add_argument("--final", action="store_true")
    ap.add_argument("--set", dest="seedset", choices=sorted(SEED_SETS))
    ap.add_argument("--fams", nargs="*", default=[])
    ap.add_argument("--out")
    ap.add_argument("--units")
    ap.add_argument("--cosine")
    ap.add_argument("--side-mode", default="scan", choices=("scan", "digest", "census", "embed"))
    ap.add_argument("--side-names", nargs="*", default=list(SEALED_SIDE))
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--targets", nargs="*", help="refresh: the eval targets to re-scan (default mixdev, mixdev_structure)")
    a = ap.parse_args(argv)
    if a.cmd == "sealedside":                       # the A25 (d) child: never prints anything but an error type
        try:
            return sealed_side_child(Path(a.units) if a.units else None, a.side_names,
                                     Path(a.cosine) if a.cosine else None, Path(a.out), a.side_mode)
        except Exception as e:  # noqa: BLE001
            print(f"sealedside error: {type(e).__name__}", file=sys.stderr)
            return 2
    if a.cmd == "census":                           # sealed-side file / item counts only (via the child)
        r = sealed_side_run([], [], a.side_names, None, mode="census")
        for n, v in r.items():
            print(f"{n}: status {v.get('status')} files {v.get('files')} items {v.get('items')} short "
                  f"{v.get('short')} gaps {len(v.get('gaps') or [])}" + (f" ({v['gaps'][0][:90]})" if v.get('gaps') else ""))
        return 0
    if a.cmd == "embed-cache":
        return build_emb_cache(only=a.only)
    if a.cmd == "freeze-mixdev":
        return freeze_mixdev()
    if a.cmd == "refresh":                          # mixdev-only staleness: re-scan mixdev alone, merge (counts only)
        if not a.names:
            ap.error("refresh needs set names (e.g. refresh F3 F6 F9 [--targets mixdev mixdev_structure])")
        return refresh(a.names, tuple(a.targets or REFRESHABLE))
    if a.cmd == "side-embed-cache":                 # A25 (d): prebuild the child's own vector cache; counts only
        h = sealed_side_start([], [], a.side_names, COSINE, mode="embed")
        r = sealed_side_finish(h)
        for n, v in r.items():
            print(f"{n}: status {v.get('status')} files {v.get('files')} items {v.get('items')} new vectors "
                  f"{v.get('added')} already cached {v.get('skipped')} gaps {v.get('gaps')} {v.get('s')} s")
        return 0 if all(v.get("status") == "scanned" for v in r.values()) else 1
    if a.cmd == "status":
        names = a.names or [f for f in FAMS if (OUT / f"{f}.json").exists()] + ["final_mix_r1"]
        p = log_problems(names)
        drift = mixdev_freeze_drift()
        if drift:
            print(f"note: {len(drift)} mixdev file(s) changed after MIXDEV_FREEZE.json, e.g. {drift[0][:70]}")
        print("\n".join(p) or "G13 logs OK: " + ", ".join(names))
        return 1 if p else 0
    if a.cmd == "targets":
        for tg in targets():
            fs = [p for s in tg["paths"] for p in resolve(s)]
            print(f"{tg['name']}: {tg['status'] or ('files ' + str(sum(map(allowed, fs))))}")
        return 0
    if a.cmd == "calib":
        return calib(a.fams, Path(a.out))
    if a.cmd == "fetch":
        return fetch_bigpat()
    if sum(map(bool, (a.fam, a.final, a.seedset))) != 1:
        ap.error("exactly one of --fam F, --final, --set packs|formats")
    if a.fam and a.fam not in FAMS:
        ap.error(f"--fam must be one of {FAMS}")
    name = a.fam or ("final_mix_r1" if a.final else a.seedset)
    rec = run_sets({name: build_set(name)}, targets(), OUT)[name]
    print(f"G13 {name}: train units {rec['train_units']} rows {rec['train_rows']} seed literals {rec['seed_literals']}"
          f" | drop units {rec['drop_units']} rows {len(rec['drop_ids'])} | seeds_clean {rec['seeds_clean']}")
    for lb, ms in rec["counts_by_eval_and_method"].items():
        print(f"  {lb}: " + ", ".join(f"{m} {v['units']}u/{v['eval_items']}i" + (f"/{v['seed_literals']}s"
                                                                             if v.get("seed_literals") else "")
                                      for m, v in ms.items()))
    print(f"  by training source: {rec['counts_by_training_source']}")
    print(f"  short items: {sum(rec['short_items'].values())} over {len(rec['short_items'])} sets; "
          f"targets missing: {[k for k, v in rec['targets'].items() if v['status'] == 'missing']}")
    print(f"  complete: {rec['complete']} ({len(rec['incomplete_why'])} reasons); wall {rec['wall_s']} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
