"""sob_g13.py: the A58 leak-check target of the System One Bench text items for g13_c2.py (PREREG_FINAL.md Ruling A58: "G13 at the final all-block run with
the System One Bench text items as a target"). Modeled on di_g13.py. CPU only, no network, no bench text is ever printed, kept in a log or written to
an export; counts, ids, paths and sha256 only.

One engine target (decontam_g13.target dict, scanned by decontam_g13.run_sets with the same methods as di_test: exact full / segment / short, substring,
10- and 12-gram, tulu8, minhash, embed; blind, generic kind):
  sob_text   the 3,250 text cases of the bench (16 suites, 4,850 decisions) as ONE UNIT PER CASE (call_id = the bench case id), read by the engine from the
             derived file vision_bench/text_track/data/sob_g13_units.jsonl. The engine's generic reader takes the string values of a record and never reads
             dict keys, but the bench's choice options ARE dict keys and its states are JSON objects, so the file is not cases.jsonl itself: this module's
             builder writes one record per case with every text a training row could leak as a string value:
               state          the model-visible state text (json.dumps(state, indent=1) for the bench's dict states: tt_core.state_text)
               state_values   each string leaf of a dict / list state, on its own (a row may print the fields as lines rather than as JSON)
               instructions   {q<j>: the question's instruction string}
               criteria       {q<j>: {c<i>: a criteria description / definition / score level}}  (values; for choice questions these are the descriptions)
               options        {q<j>: {o<i>: an option string}}  choice: each criteria KEY; score: "<i>: <level>" (C1's option form)
               card           {q<j>: the "- key: description" / "- Yes: ... - No: ..." definitions card, rendered as tt_core.to_row renders it}
               workflow       typed-decisions' workflow name (not model-visible; kept so nothing text-like is left out)
             call_id, suite and the gold are NOT read by the engine (the target's fields filter) and the gold is never written.
The engine's own rule applies unchanged: a non-content text under 5 words (a one-word option, a class name) is not an item; the options are in the unit
for the 5+ word strings (cards, "i: level" forms) and for the context they give.
A hit drops the whole training unit (call_id), as every other method. No waiver applies (A53 is for the C2 dev targets only).

Source check. build() refuses unless cases.jsonl matches vision_bench/text_track/data/data.lock.cases.json (the bench's frozen per-suite hashes, the same
fingerprint as text_track/harness/lockcheck.py: SHA-256 of every case as canonical JSON, per suite, and one hash over all suites). The file is read ONCE
(its bytes are hashed and parsed from the same read) and only by build().

Outputs (g13_sob/ holds hashes, ids and counts only; the one file with bench text is the derived units file next to cases.jsonl):
  g13_sob/sob_pins.json     what sob_g13 reads: source sha256 + lock sha256, the units file's sha256 / rows, counts, complete, gaps
  g13_sob/unit_hashes.json  {call_id: sha256 of the unit's canonical JSON}
  g13_sob/MANIFEST.json     the sha256 of unit_hashes.json, derived_from (the units file's sha256), counts
Readiness. A target with no pin record, a pin record that is not complete or any gap keeps the log incomplete (gap_for): g13_c2 includes the target in a
final run whatever the pins say, so a final log is complete only after `sob_g13.py build`.

  cd lean && ../../.venv/bin/python -B c2_build/sob_g13.py build      # lock check, units file, pins, exports (prints counts and shas)
  cd lean && ../../.venv/bin/python -B c2_build/sob_g13.py verify     # the units file against the exports (no source read)
  cd lean && ../../.venv/bin/python -B c2_build/sob_g13.py status     # counts only

Second engine target (A58 step 4 / step 12: "the full scored splits named there"), sob_splits, built by build_splits() into its own files (the sob_text
files above are not touched): the FULL scored split of every bench source that has one, at the revision build_suites.py / build_arabic.py pin, ONE UNIT PER
ITEM, read by the engine from vision_bench/text_track/data/sob_g13_splits_units.jsonl (hashed exports g13_sob/splits_pins.json, SPLITS_MANIFEST.json,
splits_unit_hashes.json; no plain text). Splits: sst5 test (2,210), sst2 validation (872), boolq validation (3,270), xnli test ar / en / fr (5,010 each,
parallel items included: one unit per language and item), tweet_sentiment_multilingual arabic test, and for MIRACL-ar the dev queries (and, per query,
the full passages) that ar_miracl_rerank / ar_miracl_pair use. The engine's methods are those of sob_text (exact full / segment / short, substring,
10- and 12-gram, tulu8, minhash, embed: a superset of 13-gram + exact + near-exact). The build is REFUSED (nothing written) on any count that differs from
A58's, a revision that differs from the bench scripts', a source file that is not the blob its revision names, or a bench suite whose cases are not drawn
from the split (the bench's own seeded sample is replayed). The one A58 count the pinned data contradicts (tweet arabic test: 256 named, 870 rows)
needs the explicit `--accept-count tweet_ar_test=870` of whoever amends A58; it is then recorded in the pins (count_deviations).

  cd lean && ../../.venv/bin/python -B c2_build/sob_g13.py fetch-splits     # network: Hugging Face Hub dataset files at the pinned revisions only
  cd lean && ../../.venv/bin/python -B c2_build/sob_g13.py build-splits [--accept-count NAME=N]
  cd lean && ../../.venv/bin/python -B c2_build/sob_g13.py verify-splits     # the units file against its exports and pins (no source read)
"""
from __future__ import annotations

import argparse
import ast
import datetime
import gzip
import hashlib
import json
import os
import random
import re
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent                      # lean/c2_build
sys.path.insert(0, str(HERE))
import c2io  # noqa: E402  (puts c_build on sys.path)
import decontam_g13 as g  # noqa: E402  (c_build: imported read-only)

SRC_REL = "vision_bench/text_track/data/cases.jsonl"                  # repo-relative: read by build() only
LOCK_REL = "vision_bench/text_track/data/data.lock.cases.json"
UNITS_REL = "vision_bench/text_track/data/sob_g13_units.jsonl"        # derived (bench text): read by the engine only
SOB_DIR = HERE / "g13_sob"                                  # pins and hashed exports: no bench text
PINS = SOB_DIR / "sob_pins.json"
EXPORT_MANIFEST = SOB_DIR / "MANIFEST.json"
UNIT_HASHES = "unit_hashes.json"

TARGETS = ("sob_text",)
FILES = {"sob_text": (UNITS_REL,)}
FIELDS = ("state", "state_values", "instructions", "criteria", "options", "card", "workflow")
NOTES = {"sob_text": "A58: the System One Bench text items (16 suites, 3,250 cases = units): state, state values, instructions, criteria, options, "
                     "definitions card, workflow; derived from vision_bench/text_track/data/cases.jsonl at the frozen lock"}
QUARANTINE_OK: tuple = ()                                   # the units file is not under bench/external_quarantine/: the engine needs no allow entry
SOB_BLOCKS = ("SB5", *c2io.DI_BLOCKS)                       # a run that holds one of these blocks' rows scans the target (A58 SB5; the DI-train blocks)
EXPECTED_CASES = 3250
EXPECTED_SUITES = 16
ROW_FIELDS = ("state", "state_values", "instructions", "criteria", "options", "card", "workflow")

# ---- the second target: the full scored splits (A58 step 4 / step 12) --------------------------------------------------------
SPLITS_UNITS_REL = "vision_bench/text_track/data/sob_g13_splits_units.jsonl"   # derived (split text): read by the engine only
HUB_REL = "vision_bench/hf_cache/hub"                       # the bench's local Hugging Face hub cache (snapshots/<revision>/...)
SCRIPTS_REL = "vision_bench/src/system-one-bench"           # build_suites.py / build_arabic.py: their REVISIONS dicts are the pins
SPLITS_PINS = SOB_DIR / "splits_pins.json"
SPLITS_EXPORT_MANIFEST = SOB_DIR / "SPLITS_MANIFEST.json"
SPLITS_UNIT_HASHES = "splits_unit_hashes.json"
SPLIT_TARGETS = ("sob_splits",)
ALL_TARGETS = TARGETS + SPLIT_TARGETS
SPLIT_FILES = {"sob_splits": (SPLITS_UNITS_REL,)}
SPLIT_FIELDS = ("parts",)                                   # the engine reads the VALUES of the parts dict (premise, hypothesis, passage, ...), never its keys
SPLIT_NOTES = {"sob_splits": "A58 step 4 / 12: the full scored splits of the bench text sources (sst5 test, sst2 validation, boolq validation, xnli test "
                             "ar / en / fr, tweet_sentiment_multilingual arabic test, MIRACL-ar dev queries and passages used by ar_miracl_*), one unit "
                             "per item, at the revisions build_suites.py / build_arabic.py pin"}
SPLITS_RULING = {"ruling": "A58 step 4, step 12", "draft": "c2_build/zed_orch/sb_blocks/A58_DRAFT.md",
                 "draft_sha256": "254ea52d1ca59910e8fe95124b8cdd9f4751414fe14091321ba81b230a7bad82"}
BENCH_SEED = 0                                              # build_suites.py / build_arabic.py: random.Random(SEED).shuffle(range(len)) [:N]
# key -> source. `a58`: the item count A58 names (None = none named). `link`: bench state key -> (item column, suffix the bench appends); `parts`: the
# unit's parts name -> item column (the text a training row could leak, as the source has it).
_XNLI = {"repo": "facebook/xnli", "revision": "b8dd5d7af51114dbda02c0e3f6133f332186418e", "split": "test", "fmt": "parquet", "a58": 5010,
         "n_sample": 150, "parts": {"premise": "premise", "hypothesis": "hypothesis"},
         "link": {"premise": ("premise", ""), "hypothesis": ("hypothesis", "")}}
SPLIT_SOURCES = {
    "sst5_test": {"repo": "SetFit/sst5", "revision": "e51bdcd8cd3a30da231967c1a249ba59361279a3", "config": None, "split": "test", "fmt": "jsonl",
                  "files": ("test.jsonl",), "a58": 2210, "bench_suite": "sst5", "n_sample": 200, "parts": {"review": "text"},
                  "link": {"review": ("text", "")}, "script": "build_suites.py"},
    "sst2_validation": {"repo": "stanfordnlp/sst2", "revision": "8d51e7e4887a4caaa95b3fbebbf53c0490b58bbb", "config": None, "split": "validation",
                        "fmt": "parquet", "files": ("data/validation-00000-of-00001.parquet",), "a58": 872, "bench_suite": "sst2", "n_sample": 200,
                        "parts": {"review": "sentence"}, "link": {"review": ("sentence", "")}, "script": "build_suites.py"},
    "boolq_validation": {"repo": "google/boolq", "revision": "35b264d03638db9f4ce671b711558bf7ff0f80d5", "config": None, "split": "validation",
                         "fmt": "parquet", "files": ("data/validation-00000-of-00001.parquet",), "a58": 3270, "bench_suite": "boolq", "n_sample": 200,
                         "parts": {"question": "question", "passage": "passage"}, "link": {"passage": ("passage", ""), "question": ("question", "?")},
                         "script": "build_suites.py"},
    **{f"xnli_{lang}_test": {**_XNLI, "config": lang, "files": (f"{lang}/test-00000-of-00001.parquet",), "bench_suite": f"xnli_{lang}",
                             "script": "build_suites.py"} for lang in ("ar", "en", "fr")},
    "tweet_ar_test": {"repo": "mteb/tweet_sentiment_multilingual", "revision": "bceb37eb62681b42e4147d879384917969bb1674", "config": "arabic",
                      "split": "test", "fmt": "jsonl.gz", "files": ("test/arabic.jsonl.gz",), "a58": 256, "bench_suite": "ar_sentiment",
                      "n_sample": 200, "parts": {"tweet": "text"}, "link": {"tweet": ("text", "")}, "script": "build_arabic.py"},
    "miracl_ar_dev": {"repo": "mteb/MIRACLReranking", "revision": "ab6f54eff185a84bc1f6ab96b56bc7df87433228", "config": "ar-queries / ar-qrels / ar-corpus",
                      "split": "dev", "fmt": "miracl", "a58": None, "script": "build_arabic.py", "k": 8, "n_rerank": 200, "n_pair": 200, "clip": 320,
                      "files": ("ar-queries/dev-00000-of-00001.parquet", "ar-qrels/dev-00000-of-00001.parquet", "ar-corpus/dev-00000-of-00001.parquet"),
                      "hub_counts": {"queries": 2896, "qrels": 287181, "corpus": 287181}},
}


class SobError(RuntimeError):
    """The bench cases do not match their lock, or the SOB pins / exports are missing, inconsistent or not the files they were derived from."""


# ---- hashing and text helpers ------------------------------------------------------------------------------------------
def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canon(obj) -> str:
    """The canonical JSON of the bench lock (sorted keys, no spaces, utf-8 as is)."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _strings(x):
    """Every string leaf of a JSON value (keys are not read)."""
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from _strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from _strings(v)


def state_text(state) -> str:
    """text_track/harness/tt_core.state_text (= lean/jevbench_od.state_text): the model-visible state."""
    return state if isinstance(state, str) else json.dumps(state, ensure_ascii=False, indent=1)


def definitions_card(q: dict):
    """The definitions card tt_core.to_row builds for a question (None when it has none)."""
    qt, crit = q.get("type"), q.get("criteria")
    if qt == "noul":
        if isinstance(crit, dict) and (crit.get("true") or crit.get("false")):
            return f"- Yes: {crit.get('true') or 'the statement holds'}\n- No: {crit.get('false') or 'it does not hold'}"
        return None
    if qt == "choice" and isinstance(crit, dict):
        notes = [f"- {k}: {v}" for k, v in crit.items() if v and str(v).strip() and str(v).strip() != k]
        return "\n".join(notes) or None
    return None


# ---- the frozen lock -----------------------------------------------------------------------------------------------------
def total(suites: dict) -> str:
    """text_track/harness/lockcheck.total."""
    return hashlib.sha256("".join(f"{s} {v['sha256']}\n" for s, v in sorted(suites.items())).encode()).hexdigest()


def fingerprint(cases: list) -> dict:
    """text_track/harness/lockcheck.fingerprint over parsed cases: {"sha256", "suites": {suite: {"n", "sha256"}}}."""
    h, n = defaultdict(hashlib.sha256), defaultdict(int)
    for c in cases:
        h[c["suite"]].update(canon(c).encode() + b"\n")
        n[c["suite"]] += 1
    suites = {s: {"n": n[s], "sha256": h[s].hexdigest()} for s in sorted(h)}
    return {"sha256": total(suites), "suites": suites}


def lock_problems(cases: list, lock: dict) -> list[str]:
    """Problems between the parsed cases and the frozen lock entry (suite names, counts and 12-char hash prefixes only); empty when all match."""
    got = fingerprint(cases)
    want = lock.get("suites")
    if not isinstance(want, dict) or not want or not isinstance(lock.get("sha256"), str):
        return ["the lock file has no suites / sha256"]
    out = []
    for s in sorted(want):
        if s not in got["suites"]:
            out.append(f"{s}: missing")
        elif got["suites"][s] != want[s]:
            out.append(f"{s}: {got['suites'][s]['n']} cases, hash {got['suites'][s]['sha256'][:12]}; frozen: {want[s].get('n')} cases, "
                       f"hash {str(want[s].get('sha256'))[:12]}")
    out += [f"{s}: not a frozen suite" for s in sorted(set(got["suites"]) - set(want))]
    if got["sha256"] != lock["sha256"]:
        out.append("overall hash differs")
    return out


def load_verified_cases(cases_path: Path | str | None = None, lock_path: Path | str | None = None) -> tuple[list, dict]:
    """(cases, info). The cases file is read once; refused (SobError) unless it matches the lock: nothing is returned then."""
    cp = Path(cases_path) if cases_path else g.REPO / SRC_REL
    lp = Path(lock_path) if lock_path else g.REPO / LOCK_REL
    try:
        lock_bytes = lp.read_bytes()
        lock = json.loads(lock_bytes)
    except (OSError, ValueError) as e:
        raise SobError(f"the bench lock {lp.name} is not readable ({type(e).__name__})") from None
    try:
        raw = cp.read_bytes()
    except OSError as e:
        raise SobError(f"the bench cases file {cp.name} is not readable ({type(e).__name__})") from None
    try:
        cases = [json.loads(ln) for ln in raw.decode("utf-8").splitlines() if ln.strip()]
        for c in cases:
            c["suite"], c["id"], c["questions"], c["state"]
    except (ValueError, KeyError, TypeError) as e:
        raise SobError(f"the bench cases file {cp.name} is not a cases file ({type(e).__name__})") from None
    problems = lock_problems(cases, lock)
    if problems:
        raise SobError("the bench cases do not match their lock, refused: " + "; ".join(problems))
    ids = [c["id"] for c in cases]
    if len(set(ids)) != len(ids):
        raise SobError("the bench case ids are not unique, refused")
    return cases, {"file_sha256": sha_bytes(raw), "lock_sha256": sha_bytes(lock_bytes), "lock_total_sha256": lock["sha256"],
                   "suites": {s: v["n"] for s, v in sorted(lock["suites"].items())}}


# ---- the units -----------------------------------------------------------------------------------------------------------
def case_unit(c: dict) -> dict:
    """One unit per case: every text a training row could leak, as string values (see the module doc). The gold is never read."""
    st = c["state"]
    u = {"call_id": c["id"], "suite": c["suite"], "state": state_text(st)}
    if not isinstance(st, str):
        vals = [s for s in _strings(st) if s.strip()]
        if vals:
            u["state_values"] = {f"v{i}": s for i, s in enumerate(vals)}
    ins, crit, opts, cards = {}, {}, {}, {}
    for j, q in enumerate((c.get("questions") or {}).values()):
        k = f"q{j}"
        if isinstance(q.get("instructions"), str) and q["instructions"].strip():
            ins[k] = q["instructions"]
        cr = q.get("criteria")
        if isinstance(cr, dict):
            vs = [v for v in cr.values() if isinstance(v, str) and v.strip()]
            if vs:
                crit[k] = {f"c{i}": v for i, v in enumerate(vs)}
            if q.get("type") == "choice":
                opts[k] = {f"o{i}": str(o) for i, o in enumerate(cr.keys())}
        elif isinstance(cr, list):
            vs = [str(v) for v in cr if isinstance(v, (str, int, float))]
            if vs:
                crit[k] = {f"c{i}": v for i, v in enumerate(vs)}
            if q.get("type") == "score":
                opts[k] = {f"o{i}": f"{i}: {v}" for i, v in enumerate(vs)}
            elif q.get("type") == "choice":                      # (no such question in the bench today: the bench's own option order is the list)
                opts[k] = {f"o{i}": v for i, v in enumerate(vs)}
        cd = definitions_card(q)
        if cd:
            cards[k] = cd
    for name, val in (("instructions", ins), ("criteria", crit), ("options", opts), ("card", cards)):
        if val:
            u[name] = val
    if isinstance(c.get("workflow"), str) and c["workflow"].strip():
        u["workflow"] = c["workflow"]
    return u


def unit_sha(u: dict) -> str:
    return sha_bytes(canon(u).encode("utf-8"))


def unit_counts(units: list[dict]) -> dict:
    """Counts only: how many units / strings of every field type the units carry, and the unique strings."""
    c = Counter()
    uniq = set()
    for u in units:
        c["units"] += 1
        for f in ROW_FIELDS:
            v = u.get(f)
            if v is None:
                continue
            c[f"units_with_{f}"] += 1
            for s in _strings(v):
                c[f"strings_{f}"] += 1
                uniq.add(s)
    c["unique_strings"] = len(uniq)
    return dict(sorted(c.items()))


def coverage_problems(cases: list, units: list[dict]) -> list[str]:
    """What the units miss of the cases they were built from (counts only): one unit per case, every question's instruction, every criteria value,
    every choice key and score level, every string leaf of a dict state."""
    out = []
    if len(units) != len(cases) or [u["call_id"] for u in units] != [c["id"] for c in cases]:
        out.append(f"{len(units)} units for {len(cases)} cases (one unit per case, in file order, is required)")
        return out
    miss = Counter()
    for c, u in zip(cases, units):
        qs = list((c.get("questions") or {}).values())
        if len(u.get("instructions") or {}) != sum(1 for q in qs if isinstance(q.get("instructions"), str) and q["instructions"].strip()):
            miss["instructions"] += 1
        want_c = sum(len([v for v in q["criteria"].values() if isinstance(v, str) and v.strip()]) if isinstance(q.get("criteria"), dict)
                     else len(q["criteria"]) if isinstance(q.get("criteria"), list) else 0 for q in qs)
        if sum(len(d) for d in (u.get("criteria") or {}).values()) != want_c:
            miss["criteria"] += 1
        want_o = sum(len(q["criteria"]) for q in qs if q.get("type") in ("choice", "score") and isinstance(q.get("criteria"), (dict, list)))
        if sum(len(d) for d in (u.get("options") or {}).values()) != want_o:
            miss["options"] += 1
        want_v = 0 if isinstance(c["state"], str) else len([s for s in _strings(c["state"]) if s.strip()])
        if len(u.get("state_values") or {}) != want_v:
            miss["state_values"] += 1
        if u.get("state") != state_text(c["state"]):
            miss["state"] += 1
    return [f"{n} units miss part of their case's {f}" for f, n in sorted(miss.items())]


# ---- pins ----------------------------------------------------------------------------------------------------------------
def load_pins(path: Path | None = None) -> dict:
    """c2_build/g13_sob/sob_pins.json ({} when it is not written yet). Written by build()."""
    p = Path(path) if path else PINS
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def files_of(name: str) -> tuple:
    """The repo-relative units file(s) the engine scans for target `name`."""
    return FILES[name] if name in FILES else SPLIT_FILES[name]


def gap_for(name: str = "sob_text", pins: dict | None = None) -> str | None:
    """Why target `name` is incomplete (None = complete): the pin record must exist, say complete true, carry no gap, pin its units file and name its
    source."""
    pins = (load_pins(SPLITS_PINS) if name in SPLIT_TARGETS else load_pins()) if pins is None else pins
    p = pins.get(name)
    if not isinstance(p, dict):
        if name in SPLIT_TARGETS:
            return f"{name}: not built yet (no record in g13_sob/splits_pins.json): run c2_build/sob_g13.py fetch-splits, then build-splits (A58 step 12)"
        return f"{name}: not built yet (no record in g13_sob/sob_pins.json): run c2_build/sob_g13.py build (A58)"
    gaps = [str(x) for x in p.get("gaps") or []]
    files = p.get("files") or {}
    if p.get("complete") is not True or gaps:
        return f"{name}: incomplete ({'; '.join(gaps) or 'complete is not true'}) (A58)"
    if set(files) != set(files_of(name)) or any(not (d or {}).get("sha256") for d in files.values()):
        return f"{name}: the pin record does not pin the units file (A58)"
    if not (p.get("source") or {}).get("file_sha256"):
        return f"{name}: the pin record does not name the bench source sha256 (A58)"
    return None


def complete(pins: dict | None = None) -> bool:
    pins = load_pins() if pins is None else pins
    return all(gap_for(n, pins) is None for n in TARGETS)


def pinned_files(pins: dict) -> dict:
    """{repo-relative path: sha256} of every file the pin records list."""
    out = {}
    for n in ALL_TARGETS:
        for f, d in ((pins.get(n) or {}).get("files") or {}).items():
            out[f] = (d or {}).get("sha256")
    return out


def verify_scanned(eval_shas: dict, pins: dict, names=TARGETS, require: bool = False) -> list[str]:
    """Problems between what the engine scanned (its inputs_sha256.eval: repo-relative file -> sha256) and the pinned units file: a scanned file that
    is not the pinned one; with require, also a pinned file the engine did not scan."""
    out = []
    pin = pinned_files({n: pins.get(n) for n in names} if pins else {})
    for n in names:
        for f in files_of(n):
            want = pin.get(f)
            got = (eval_shas or {}).get(f)
            if want and got and want != got:
                out.append(f"{n}: the scanned file {Path(f).name} is not the pinned one (sha256 {str(got)[:12]} vs pinned {str(want)[:12]})")
            elif want and not got and require:
                out.append(f"{n}: the pinned file {Path(f).name} was not scanned")
    return out


# ---- the engine side -----------------------------------------------------------------------------------------------------
def engine_allows() -> bool:
    """True when decontam_g13.allowed() lets the engine read the units file (string logic only). It does, so no allow-list entry is needed."""
    return all(g.allowed(g.REPO / p) for ps in FILES.values() for p in ps)


def patch_engine() -> None:
    """Add QUARANTINE_OK (empty today: the units file is outside bench/external_quarantine/) to decontam_g13.QUARANTINE_OK. Idempotent; the engine file
    itself is not edited. g13_c2 does not need to call it."""
    g.QUARANTINE_OK = tuple(g.QUARANTINE_OK) + tuple(p for p in QUARANTINE_OK if p not in g.QUARANTINE_OK)


def targets(pins: dict | None = None) -> list[dict]:
    """The engine target dict (blind: counts only). `gap` carries the coverage gap that keeps a log incomplete. Same dict as g.target."""
    pins = load_pins() if pins is None else pins
    if not engine_allows():
        raise SobError("decontam_g13.allowed() refuses the units file path")
    return [g.target(n, ["repo:" + p for p in FILES[n]], kind="generic", fields=FIELDS, blind=True, note=NOTES[n], gap=gap_for(n, pins))
            for n in TARGETS]


def has_sob_rows(units: list[dict]) -> bool:
    """True when a unit's row is an SB5 or DI block's (meta.family)."""
    for u in units:
        for r in u.get("rows_src", ()) or ():
            m = r.get("meta") if isinstance(r.get("meta"), dict) else {}
            if m.get("family") in SOB_BLOCKS:
                return True
    return False


def needs_sob(run_name: str, sets: dict) -> bool:
    """A58: the target joins every final run (the final all-block mix), and any candidates / carry run that holds SB5 or DI rows (the block, or rows whose
    meta.family is one). Never a seed run (pool templates) and never a run of other blocks: pass tgs explicitly to ask for it."""
    if run_name == "final":
        return True
    if run_name == "seed":
        return False
    if any(s.get("block") in SOB_BLOCKS for s in sets.values()):
        return True
    return any(has_sob_rows(s["units"]) for s in sets.values())


# ---- the program side: hashed exports -----------------------------------------------------------------------------------
class SobExports:
    """c2_build/g13_sob/ exports (MANIFEST.json, unit_hashes.json), checked against their manifest and against the units file's pinned sha256 they were
    derived from. Membership tests only; nothing here is printed."""

    FILES = (UNIT_HASHES,)
    MANIFEST = "MANIFEST.json"
    HASHES = UNIT_HASHES
    HINT = "build"

    def _default_pins(self) -> dict:
        return load_pins()

    def __init__(self, root: Path | None = None, pins: dict | None = None):
        root = Path(root) if root else SOB_DIR
        try:
            man = json.loads((root / self.MANIFEST).read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            raise SobError(f"g13_sob/{self.MANIFEST} is not readable ({type(e).__name__}): run c2_build/sob_g13.py {self.HINT}") from None
        for name in self.FILES:
            d = (man.get("files") or {}).get(name)
            f = root / name
            if not isinstance(d, dict) or not f.is_file() or g.sha256_file(f) != d.get("sha256"):
                raise SobError(f"g13_sob/{name} is missing or differs from {self.MANIFEST}")
        pins = self._default_pins() if pins is None else pins
        derived, pinned = man.get("derived_from") or {}, pinned_files(pins)
        if not derived or any(pinned.get(f) != s for f, s in derived.items()):
            raise SobError("the SOB exports were derived from another units file than the pinned one (g13_sob/*pins.json): build again")
        self.shas = {"manifest": g.sha256_file(root / self.MANIFEST), **{n: d["sha256"] for n, d in man["files"].items()}}
        try:
            h = json.loads((root / self.HASHES).read_text(encoding="utf-8"))
        except ValueError:
            raise SobError(f"{self.HASHES} is not JSON") from None
        if not isinstance(h, dict) or not all(isinstance(k, str) and isinstance(v, str) and len(v) == 64 for k, v in h.items()):
            raise SobError(f"{self.HASHES} is not {{call_id: sha256}}")
        self.unit_hashes = h
        n = (man.get("counts") or {}).get("units")
        if n != len(h):
            raise SobError(f"export units: {len(h)} entries, {self.MANIFEST} says {n}")
        self.counts = dict(man.get("counts") or {})


class SplitExports(SobExports):
    """The same checks for the sob_splits exports (SPLITS_MANIFEST.json, splits_unit_hashes.json) against g13_sob/splits_pins.json."""

    FILES = (SPLITS_UNIT_HASHES,)
    MANIFEST = "SPLITS_MANIFEST.json"
    HASHES = SPLITS_UNIT_HASHES
    HINT = "fetch-splits, then build-splits"

    def _default_pins(self) -> dict:
        return load_pins(SPLITS_PINS)

    def __init__(self, root: Path | None = None, pins: dict | None = None):
        super().__init__(root, pins)
        n = (self.counts or {}).get("splits")
        if not n:
            raise SobError(f"{self.MANIFEST} names no split counts")


def units_file_problems(units_path: Path | str, ex: SobExports) -> list[str]:
    """The units file against the exports (no source read): one unit per exported call_id, each with its exported hash. Counts only."""
    try:
        lines = Path(units_path).read_text(encoding="utf-8").splitlines()
        units = [json.loads(x) for x in lines if x.strip()]
    except (OSError, ValueError) as e:
        return [f"the units file is not readable ({type(e).__name__})"]
    got = {u.get("call_id"): unit_sha(u) for u in units}
    out = []
    if len(got) != len(units):
        out.append("the units file has duplicate call_ids")
    if set(got) != set(ex.unit_hashes):
        out.append(f"the units file has {len(set(got) - set(ex.unit_hashes))} units the export lacks and lacks {len(set(ex.unit_hashes) - set(got))} of its units")
    bad = sum(1 for k, v in got.items() if k in ex.unit_hashes and ex.unit_hashes[k] != v)
    if bad:
        out.append(f"{bad} units differ from their exported hash")
    return out


# ---- the builder: the only reader of the bench cases ------------------------------------------------------------------------
def _atomic_write(p: Path, data: bytes) -> str:
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(p.parent), prefix=p.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.chmod(tmp, 0o644)
        os.replace(tmp, p)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return sha_bytes(data)


def _write_json(p: Path, obj) -> str:
    return _atomic_write(p, (json.dumps(obj, indent=1, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8"))


def build(cases_path=None, lock_path=None, units_path=None, out_dir=None) -> dict:
    """Lock check, then the units file, the pin record and the hashed exports. Returns the pin record (counts and shas only). SobError (nothing
    written) when the cases do not match their lock."""
    cases, info = load_verified_cases(cases_path, lock_path)
    units = [case_unit(c) for c in cases]
    up = Path(units_path) if units_path else g.REPO / UNITS_REL
    out = Path(out_dir) if out_dir else SOB_DIR
    gaps = coverage_problems(cases, units)
    if len(units) != EXPECTED_CASES:
        gaps.append(f"{len(units)} units, {EXPECTED_CASES} expected")
    if len(info["suites"]) != EXPECTED_SUITES:
        gaps.append(f"{len(info['suites'])} suites, {EXPECTED_SUITES} expected")
    counts = unit_counts(units)
    for f in ("state", "instructions", "criteria", "options", "card"):
        if not counts.get(f"units_with_{f}"):
            gaps.append(f"no unit carries a {f}")
    body = "".join(json.dumps(u, ensure_ascii=False) + "\n" for u in units).encode("utf-8")
    units_sha = _atomic_write(up, body)
    hashes = {u["call_id"]: unit_sha(u) for u in units}
    h_sha = _write_json(out / UNIT_HASHES, hashes)
    rows_by_suite = Counter(u["suite"] for u in units)
    questions = sum(len(c["questions"]) for c in cases)
    man = {"built_utc": _utc(), "files": {UNIT_HASHES: {"sha256": h_sha}}, "derived_from": {UNITS_REL: units_sha},
           "counts": {"units": len(hashes), "suites": len(rows_by_suite), "questions": questions}}
    _write_json(out / "MANIFEST.json", man)
    pins = {"built_utc": man["built_utc"],
            "sob_text": {"complete": not gaps, "gaps": gaps,
                         "files": {UNITS_REL: {"rows": len(units), "sha256": units_sha}},
                         "source": {"path": SRC_REL, "lock_path": LOCK_REL, **info, "cases": len(cases), "questions": questions},
                         "counts": {**counts, "units_by_suite": dict(sorted(rows_by_suite.items()))},
                         "note": NOTES["sob_text"]}}
    _write_json(out / "sob_pins.json", pins)
    return pins


def _utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ==== the second target: the full scored splits (A58 step 4 / step 12) ==================================================================
def load_all_pins() -> dict:
    """{"sob_text": ..., "sob_splits": ...}: the two pin files together (each target's record under its own name)."""
    return {**load_pins(), **load_pins(SPLITS_PINS)}


def split_targets(pins: dict | None = None) -> list[dict]:
    """The engine target dict of the full scored splits (blind, generic, every method; fields = the parts dict of a unit). `gap` is the coverage gap that
    keeps a log incomplete until build-splits has run."""
    pins = load_pins(SPLITS_PINS) if pins is None else pins
    if not all(g.allowed(g.REPO / p) for p in SPLIT_FILES["sob_splits"]):
        raise SobError("decontam_g13.allowed() refuses the splits units file path")
    return [g.target("sob_splits", ["repo:" + p for p in SPLIT_FILES["sob_splits"]], kind="generic", fields=SPLIT_FIELDS, blind=True,
                     note=SPLIT_NOTES["sob_splits"], gap=gap_for("sob_splits", pins))]


def all_targets(pins: dict | None = None) -> list[dict]:
    """sob_text + sob_splits: where g13_c2 adds one it adds both. `pins`: the merged dict of load_all_pins() (None: each target loads its own)."""
    return targets(pins) + split_targets(pins)


def guard_files(names=True) -> list:
    """The files a run holding the named SOB targets must hash at its start and re-check (RunGuard): this program, and per target its pins, export
    manifest, hashed exports and the units file the engine scans. names=True: every SOB target."""
    names = ALL_TARGETS if names is True else tuple(names)
    out = [Path(__file__).resolve()]
    if "sob_text" in names:
        out += [PINS, EXPORT_MANIFEST, *(SOB_DIR / n for n in SobExports.FILES), g.REPO / UNITS_REL]
    if "sob_splits" in names:
        out += [SPLITS_PINS, SPLITS_EXPORT_MANIFEST, *(SOB_DIR / n for n in SplitExports.FILES), g.REPO / SPLITS_UNITS_REL]
    return out


def export_record(name: str, pins: dict) -> tuple[dict, list[str]]:
    """(the run record of target `name`'s exports, why-incomplete strings): verified exports give counts and shas only; a refusal gives its reason."""
    cls, label = (SobExports, "sob_exports") if name == "sob_text" else (SplitExports, "sob_splits_exports")
    try:
        sx = cls(pins=pins)
    except SobError as e:
        return {"status": f"refused: {e}"}, [f"{label}: {e}"]
    p = pins.get(name) or {}
    rec = {"status": "verified", "sha256": sx.shas, "units": len(sx.unit_hashes),
           "source": {k: (p.get("source") or {}).get(k) for k in ("file_sha256", "lock_sha256", "lock_total_sha256", "cases")}}
    if name == "sob_splits":
        rec["splits"] = {k: {"units": v.get("units"), "count": v.get("count"), "revision": str(v.get("revision"))[:12]} for k, v in (p.get("splits") or {}).items()}
        rec["count_deviations"] = list(p.get("count_deviations") or [])
    return rec, []


# ---- the bench scripts' pins ---------------------------------------------------------------------------------------------------
def bench_script_facts(scripts_dir: Path | str | None = None) -> dict:
    """What build_suites.py / build_arabic.py say, read by ast only (nothing is run): {script: {"revisions": {repo: revision}, "loads": [(repo,
    positional args after the repo (constants, None for a name), split)]}}."""
    base = Path(scripts_dir) if scripts_dir else g.REPO / SCRIPTS_REL
    out = {}
    for name in ("build_suites.py", "build_arabic.py"):
        try:
            tree = ast.parse((base / name).read_text(encoding="utf-8"))
        except (OSError, SyntaxError, ValueError) as e:
            raise SobError(f"the bench script {name} is not readable ({type(e).__name__})") from None
        revs, loads = {}, []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "REVISIONS" for t in node.targets):
                try:
                    revs = dict(ast.literal_eval(node.value))
                except ValueError:
                    revs = {}
            if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "load" and node.args and isinstance(node.args[0], ast.Constant):
                split = next((k.value.value for k in node.keywords if k.arg == "split" and isinstance(k.value, ast.Constant)), None)
                loads.append((node.args[0].value, [a.value if isinstance(a, ast.Constant) else None for a in node.args[1:]], split))
        out[name] = {"revisions": revs, "loads": loads}
    return out


def revision_problems(sources: dict, scripts_dir: Path | str | None = None) -> list[str]:
    """Each source's repo, revision, config and split against what the bench scripts pin and load (counts / short hashes only)."""
    facts, out = bench_script_facts(scripts_dir), []
    for key, s in sources.items():
        f = facts.get(s["script"]) or {}
        got = (f.get("revisions") or {}).get(s["repo"])
        if got != s["revision"]:
            out.append(f"{key}: revision {s['revision'][:12]} is not the one {s['script']} pins ({str(got)[:12]})")
        mine = [(cfg, sp) for repo, cfg, sp in f.get("loads") or [] if repo == s["repo"]]
        if not any(sp == s["split"] and (s.get("config") is None or any(c is None or c == s["config"] or c in str(s["config"]) for c in cfg)) for cfg, sp in mine):
            out.append(f"{key}: {s['script']} does not load {s['repo']} split {s['split']}")
    return out


# ---- reading the pinned source files (local hub cache; the network only in fetch_splits) ------------------------------------------
def hub_dir(hub: Path | str | None = None) -> Path:
    return Path(hub) if hub else g.REPO / HUB_REL


def snapshot_file(repo: str, revision: str, rel: str, hub: Path | str | None = None) -> Path:
    p = hub_dir(hub) / ("datasets--" + repo.replace("/", "--")) / "snapshots" / revision / rel
    if not p.is_file():
        raise SobError(f"{repo}@{revision[:8]}/{rel} is not in the local hub cache: run c2_build/sob_g13.py fetch-splits")
    return p


def read_source_file(repo: str, revision: str, rel: str, hub: Path | str | None = None) -> tuple[bytes, dict]:
    """(bytes, {"sha256", "bytes", "blob_check"}). The hub's own blob id (the name the snapshot link points at: the sha256 of an LFS file, the git blob sha1
    of the others) must agree with the content; a file with another name is recorded as 'unchecked'. SobError on a disagreement."""
    p = snapshot_file(repo, revision, rel, hub)
    data = p.read_bytes()
    sha, name = sha_bytes(data), (Path(os.readlink(p)).name if p.is_symlink() else p.name)       # the snapshot link's own target name = the hub blob id
    if re.fullmatch(r"[0-9a-f]{64}", name):
        how, ok = "lfs_sha256", name == sha
    elif re.fullmatch(r"[0-9a-f]{40}", name):
        how, ok = "git_blob_sha1", hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest() == name
    else:
        how, ok = "unchecked", True
    if not ok:
        raise SobError(f"{repo}/{rel}: the cached content is not the hub blob {name[:12]} its name says")
    return data, {"sha256": sha, "bytes": len(data), "blob_check": how}


def parse_rows(data: bytes, fmt: str, columns=None) -> list[dict]:
    """The rows of one source file in file order (= the order datasets gives a single-shard split)."""
    if fmt in ("jsonl", "jsonl.gz"):
        txt = (gzip.decompress(data) if fmt == "jsonl.gz" else data).decode("utf-8")
        return [json.loads(x) for x in txt.split("\n") if x.strip()]
    if fmt == "parquet":
        import io
        import pyarrow.parquet as pq
        return pq.read_table(io.BytesIO(data), columns=list(columns) if columns else None).to_pylist()
    raise SobError(f"unknown source format {fmt}")


def fetch_splits(hub: Path | str | None = None, sources: dict | None = None) -> dict:
    """NETWORK: download the pinned data files of every source from the Hugging Face Hub (dataset repos, exact revisions) into the bench's hub cache,
    then check each against its blob id. Counts only."""
    from huggingface_hub import hf_hub_download
    sources, out = SPLIT_SOURCES if sources is None else sources, {}
    for key, s in sources.items():
        for rel in s["files"]:
            hf_hub_download(repo_id=s["repo"], filename=rel, repo_type="dataset", revision=s["revision"], cache_dir=str(hub_dir(hub)))
            _, rec = read_source_file(s["repo"], s["revision"], rel, hub)
            out[f"{key}:{rel}"] = {"bytes": rec["bytes"], "blob_check": rec["blob_check"]}
    return out


# ---- the replay of the bench's own sampling ---------------------------------------------------------------------------------------
def sample_indices(n: int, k: int, seed: int = BENCH_SEED) -> list[int]:
    """build_suites.py / build_arabic.py sample(): random.Random(seed).shuffle(range(n)), first k."""
    idx = list(range(n))
    random.Random(seed).shuffle(idx)
    return idx[:k]


def linked_cases(s: dict, rows: list[dict], cases: list[dict]) -> int:
    """How many of the bench's cases of this source's suite are exactly the split's item the bench's seeded sample draws for them (same id, same state)."""
    idx, ok = sample_indices(len(rows), s["n_sample"]), 0
    for i, c in enumerate(cases):
        if i >= len(idx):
            break
        r = rows[idx[i]]
        want = {k: f"{r[col]}{suf}" for k, (col, suf) in s["link"].items()}
        ok += c["id"] == f"{s['bench_suite']}-{i}" and c["state"] == want
    return ok


def clip(text: str, n: int) -> str:
    """build_arabic.py clip()."""
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + " …"


def miracl_replay(queries: dict, qrels: dict, k: int, n: int, seed: int = BENCH_SEED):
    """build_arabic.py's ar_miracl_* draws, replayed on the dev queries and qrels: (usable queries, [(qid, doc ids in option order)] for the rerank
    suite, [(qid, doc id)] for the pair suite). qrels: {query id: {doc id: score}} in file order."""
    usable = [q for q in queries if any(v > 0 for v in qrels.get(q, {}).values()) and sum(v == 0 for v in qrels.get(q, {}).values()) >= k - 1]
    rng = random.Random(seed + 2)
    rng.shuffle(usable)
    rerank = []
    for qid in usable[:n]:
        pos = rng.choice([d for d, v in qrels[qid].items() if v > 0])
        negs = rng.sample([d for d, v in qrels[qid].items() if v == 0], k - 1)
        docs = negs + [pos]
        rng.shuffle(docs)
        rerank.append((qid, docs))
    pair = []
    for i, qid in enumerate(usable[n:2 * n]):
        rel = i % 2 == 0
        pair.append((qid, rng.choice([d for d, v in qrels[qid].items() if (v > 0) == rel])))
    return usable, rerank, pair


def miracl_linked(s: dict, queries: dict, text: dict, rerank: list, pair: list, by_suite: dict) -> int:
    """How many of the bench's ar_miracl_rerank / ar_miracl_pair cases are exactly the replayed draws (query, and the clipped passages in option order)."""
    ok, c = 0, s["clip"]
    for i, (c_case, (qid, docs)) in enumerate(zip(by_suite.get("ar_miracl_rerank", []), rerank)):
        q = next(iter(c_case["questions"].values()))
        crit = q.get("criteria")
        ok += (c_case["id"] == f"ar_miracl_rerank-{i}" and c_case["state"] == {"query": queries[qid]} and isinstance(crit, dict)
               and list(crit.values()) == [clip(text[d], c) for d in docs])
    for i, (c_case, (qid, doc)) in enumerate(zip(by_suite.get("ar_miracl_pair", []), pair)):
        ok += c_case["id"] == f"ar_miracl_pair-{i}" and c_case["state"] == {"query": queries[qid], "passage": clip(text[doc], c)}
    return ok


# ---- the units ----------------------------------------------------------------------------------------------------------------
def split_unit(key: str, ident, parts: dict) -> dict:
    """One unit = one scored item: every text of it as a string value of `parts` (the dict keys are not read by the engine)."""
    return {"call_id": f"{key}:{ident}", "split": key, "parts": parts}


def parts_problem(parts: dict) -> str | None:
    if not parts or not all(isinstance(v, str) for v in parts.values()):
        return "an item has a part that is not text"
    return None


def items_sha(units: list[dict]) -> str:
    return sha_bytes(canon([u["parts"] for u in units]).encode("utf-8"))


def word_rule_effect(units: list[dict]) -> dict:
    """The engine's 5-word rule on these units (decontam_g13.Scan.add_item, kind generic: the longest string of an item is its content text, every other
    string is not): counts only. no_content_5w = the engine's 'short' items (no content text of >= 5 words: only the exact whole-text hash of the
    longest string runs); parts_below_5w = items with a non-content string under 5 words, which is not scanned at all; the length bands of the content
    text tell which methods can fire (5-9 words: no 10- / 12-gram; 10+ words: all)."""
    c = Counter({k: 0 for k in ("units", "no_content_5w", "no_text_5w", "parts_below_5w", "content_5_9", "content_ge10")})
    for u in units:
        lv = [x for x in g.leaves(u, SPLIT_FIELDS)]
        ws = [g.words(x) for x in lv]
        top = max(range(len(lv)), key=lambda i: len(lv[i]), default=-1)
        c["units"] += 1
        n_top = len(ws[top]) if top >= 0 else 0
        if n_top < g.MIN_WORDS:
            c["no_content_5w"] += 1
        if top >= 0 and not any(len(w) >= g.MIN_WORDS for w in ws):
            c["no_text_5w"] += 1
        if any(i != top and 0 < len(w) < g.MIN_WORDS for i, w in enumerate(ws)):
            c["parts_below_5w"] += 1
        c["content_5_9"] += g.MIN_WORDS <= n_top < g.NGRAM
        c["content_ge10"] += n_top >= g.NGRAM
    return dict(sorted(c.items()))


def count_check(key: str, got: int, want: int | None, accept: dict) -> tuple[str | None, dict | None]:
    """(problem, deviation): an item count against A58's; a mismatch passes only with an explicit accept_counts entry that equals the actual count."""
    if want is None or got == want:
        return (f"{key}: accepted count {accept[key]} but A58's {want} is right: remove the flag" if key in accept else None), None
    if accept.get(key) == got:
        return None, {"split": key, "a58": want, "actual": got}
    return f"{key}: {got} items, A58 names {want}" + (f" (accepted {accept[key]}, not {got})" if key in accept else ""), None


def _plain_units(key: str, s: dict, by_suite: dict, hub, accept: dict):
    data, frec = read_source_file(s["repo"], s["revision"], s["files"][0], hub)
    cols = sorted({*s["parts"].values(), *(c for c, _ in s["link"].values())})
    rows = parse_rows(data, s["fmt"], cols if s["fmt"] == "parquet" else None)
    probs, units = [], []
    for i, r in enumerate(rows):
        try:
            parts = {name: r[col] for name, col in s["parts"].items()}
        except KeyError:
            probs.append(f"{key}: a column of the parts map is missing")
            break
        if parts_problem(parts):
            probs.append(f"{key}: {parts_problem(parts)}")
            break
        units.append(split_unit(key, i, parts))
    p, dev = count_check(key, len(rows), s["a58"], accept)
    probs += [p] if p else []
    cases = by_suite.get(s["bench_suite"], [])
    linked = linked_cases(s, rows, cases) if not probs else 0
    if not probs and (linked != len(cases) or len(cases) != s["n_sample"]):
        probs.append(f"{key}: {linked} of the bench's {len(cases)} {s['bench_suite']} cases (expected {s['n_sample']}) are drawn from this split at this revision")
    rec = {"dataset": s["repo"], "config": s["config"], "revision": s["revision"], "split": s["split"], "files": {s["files"][0]: frecord(frec)},
           "a58_count": s["a58"], "count": len(rows), "units": len(units), "items_sha256": items_sha(units),
           "bench_suite": s["bench_suite"], "bench_cases": len(cases), "bench_cases_linked": linked, "bench_script": s["script"]}
    return units, rec, probs, dev


def frecord(f: dict) -> dict:
    return {"sha256": f["sha256"], "bytes": f["bytes"], "blob_check": f["blob_check"]}


def _miracl_units(key: str, s: dict, by_suite: dict, hub, accept: dict):
    recs, probs = {}, []
    tabs = {}
    for name, rel in zip(("queries", "qrels", "corpus"), s["files"]):
        data, recs[rel] = read_source_file(s["repo"], s["revision"], rel, hub)
        cols = {"queries": ("_id", "text"), "qrels": ("query-id", "corpus-id", "score"), "corpus": ("_id", "title", "text")}[name]
        tabs[name] = parse_rows(data, "parquet", cols)
    for name, want in s["hub_counts"].items():
        if len(tabs[name]) != want:
            probs.append(f"{key}: {name} has {len(tabs[name])} rows, the hub's dataset card says {want}")
    queries = {r["_id"]: r["text"] for r in tabs["queries"]}
    qrels: dict = {}
    for r in tabs["qrels"]:
        qrels.setdefault(r["query-id"], {})[r["corpus-id"]] = r["score"]
    usable, rerank, pair = miracl_replay(queries, qrels, s["k"], s["n_rerank"])
    need = {d for _, docs in rerank for d in docs} | {d for _, d in pair}
    text = {r["_id"]: (r["title"] + ": " if r["title"] else "") + r["text"] for r in tabs["corpus"] if r["_id"] in need}
    if len(rerank) != s["n_rerank"] or len(pair) != s["n_pair"] or need - set(text):
        probs.append(f"{key}: the replay gives {len(rerank)} rerank / {len(pair)} pair draws and {len(need - set(text))} passages missing from the corpus")
        return [], {"files": recs}, probs, None
    cases = len(by_suite.get("ar_miracl_rerank", [])) + len(by_suite.get("ar_miracl_pair", []))
    linked = miracl_linked(s, queries, text, rerank, pair, by_suite)
    if linked != cases or cases != s["n_rerank"] + s["n_pair"]:
        probs.append(f"{key}: {linked} of the bench's {cases} ar_miracl cases (expected {s['n_rerank'] + s['n_pair']}) are the replayed draws at this revision")
    p, _ = count_check(key, len(rerank) + len(pair), None, accept)
    probs += [p] if p else []
    units = []
    for qid, docs in rerank:
        units.append(split_unit(key, qid, {"query": queries[qid], **{f"p{j}": text[d] for j, d in enumerate(docs)}}))
    for qid, doc in pair:
        units.append(split_unit(key, qid, {"query": queries[qid], "p0": text[doc]}))
    rec = {"dataset": s["repo"], "config": s["config"], "revision": s["revision"], "split": s["split"], "files": {k: frecord(v) for k, v in recs.items()},
           "a58_count": None, "count": len(units), "units": len(units), "items_sha256": items_sha(units), "bench_suite": "ar_miracl_rerank + ar_miracl_pair",
           "bench_cases": cases, "bench_cases_linked": linked, "bench_script": s["script"],
           "dev_queries": len(queries), "dev_qrels_rows": len(tabs["qrels"]), "dev_corpus_rows": len(tabs["corpus"]), "usable_queries": len(usable),
           "queries_used": len(units), "passage_uses": sum(len(d) for _, d in rerank) + len(pair), "passages_used": len(need)}
    return units, rec, probs, None


def build_splits(cases_path=None, lock_path=None, units_path=None, out_dir=None, hub=None, scripts_dir=None, sources: dict | None = None,
                 accept_counts: dict | None = None, check_scripts: bool = True) -> dict:
    """Lock check of the bench cases, then the units of every full scored split, the pin record and the hashed exports. Returns the pin record (counts
    and shas only). SobError, NOTHING written, on: a count that differs from A58's (unless explicitly accepted, see count_check), a revision / split the
    bench scripts do not pin, a source file that is not its hub blob, an hub row count that differs from the dataset card, or a bench suite whose cases
    are not the seeded sample of the split (the replay)."""
    sources = SPLIT_SOURCES if sources is None else sources
    accept = dict(accept_counts or {})
    cases, info = load_verified_cases(cases_path, lock_path)
    by_suite = defaultdict(list)
    for c in cases:
        by_suite[c["suite"]].append(c)
    problems = [f"{k}: --accept-count names no such split" for k in sorted(set(accept) - set(sources))]
    problems += revision_problems(sources, scripts_dir) if check_scripts else []
    units, recs, deviations = [], {}, []
    for key, s in sources.items():
        try:
            u, rec, probs, dev = (_miracl_units if s["fmt"] == "miracl" else _plain_units)(key, s, by_suite, hub, accept)
        except SobError as e:
            problems.append(f"{key}: {e}")
            continue
        problems += probs
        deviations += [dev] if dev else []
        units += u
        recs[key] = rec
    ids = [u["call_id"] for u in units]
    if len(set(ids)) != len(ids):
        problems.append("the splits' call ids are not unique")
    if problems:
        raise SobError("the full-split build is refused, nothing written: " + "; ".join(problems))
    up = Path(units_path) if units_path else g.REPO / SPLITS_UNITS_REL
    out = Path(out_dir) if out_dir else SOB_DIR
    body = "".join(json.dumps(u, ensure_ascii=False) + "\n" for u in units).encode("utf-8")
    units_sha = _atomic_write(up, body)
    hashes = {u["call_id"]: unit_sha(u) for u in units}
    h_sha = _write_json(out / SPLITS_UNIT_HASHES, hashes)
    by_split = Counter(u["split"] for u in units)
    effect = {k: word_rule_effect([u for u in units if u["split"] == k]) for k in recs}
    for k in recs:
        recs[k]["word_rule_5"] = effect[k]
    man = {"built_utc": _utc(), "files": {SPLITS_UNIT_HASHES: {"sha256": h_sha}}, "derived_from": {SPLITS_UNITS_REL: units_sha},
           "counts": {"units": len(hashes), "splits": len(recs), "units_by_split": dict(sorted(by_split.items()))}}
    _write_json(out / SPLITS_EXPORT_MANIFEST.name, man)
    pins = {"built_utc": man["built_utc"],
            "sob_splits": {"complete": True, "gaps": [], "ruling": dict(SPLITS_RULING), "count_deviations": deviations,
                           "files": {SPLITS_UNITS_REL: {"rows": len(units), "sha256": units_sha}},
                           "source": {"path": SRC_REL, "lock_path": LOCK_REL, **{k: v for k, v in info.items() if k != "suites"}, "cases": len(cases)},
                           "splits": dict(sorted(recs.items())),
                           "counts": {"units": len(units), "splits": len(recs), "units_by_split": dict(sorted(by_split.items())),
                                      "word_rule_5": word_rule_effect(units)},
                           "note": SPLIT_NOTES["sob_splits"]}}
    _write_json(out / SPLITS_PINS.name, pins)
    return pins


def splits_pin_problems(units: list[dict], pins: dict) -> list[str]:
    """The units file against the pin record (no source read): per split the unit count and the items hash, and the rows total. Counts only."""
    p = (pins.get("sob_splits") or {})
    out = []
    by = defaultdict(list)
    for u in units:
        by[u.get("split")].append(u)
    spl = p.get("splits") or {}
    if set(by) != set(spl):
        out.append(f"{len(set(by) - set(spl))} splits in the units file are not pinned, {len(set(spl) - set(by))} pinned splits are not in it")
    for k, rec in spl.items():
        if len(by.get(k, [])) != rec.get("units"):
            out.append(f"{k}: {len(by.get(k, []))} units, the pins say {rec.get('units')}")
        elif items_sha(by[k]) != rec.get("items_sha256"):
            out.append(f"{k}: the units' items differ from the pinned items hash")
    rows = sum(len(v) for v in by.values())
    if rows != ((p.get("files") or {}).get(SPLITS_UNITS_REL) or {}).get("rows"):
        out.append(f"{rows} units in the file, the pins say {((p.get('files') or {}).get(SPLITS_UNITS_REL) or {}).get('rows')}")
    return out


def splits_status() -> dict:
    pins = load_pins(SPLITS_PINS)
    p = pins.get("sob_splits") or {}
    return {"pins": bool(pins), "complete": gap_for("sob_splits", pins) is None, "gap": gap_for("sob_splits", pins),
            "units": ((p.get("files") or {}).get(SPLITS_UNITS_REL) or {}).get("rows"), "units_file_exists": (g.REPO / SPLITS_UNITS_REL).is_file(),
            "export_manifest": SPLITS_EXPORT_MANIFEST.is_file(), "count_deviations": p.get("count_deviations")}


def status() -> dict:
    """Counts only: which pieces exist and whether the target is complete (the sob_text record; `splits`: the sob_splits record)."""
    pins = load_pins()
    p = pins.get("sob_text") or {}
    return {"pins": bool(pins), "complete": complete(pins), "gap": gap_for("sob_text", pins),
            "units": ((p.get("files") or {}).get(UNITS_REL) or {}).get("rows"), "units_file_exists": (g.REPO / UNITS_REL).is_file(),
            "export_manifest": EXPORT_MANIFEST.is_file(), "splits": splits_status()}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("build", "verify", "status", "fetch-splits", "build-splits", "verify-splits"))
    ap.add_argument("--accept-count", action="append", default=[], metavar="NAME=N",
                    help="build-splits: accept the actual item count N of split NAME although it differs from A58's (recorded in the pins)")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "build":
            p = build()["sob_text"]
            print(json.dumps({"complete": p["complete"], "gaps": p["gaps"], "units": p["files"][UNITS_REL],
                              "source_sha256": p["source"]["file_sha256"], "counts": p["counts"]}, indent=1, sort_keys=True))
            return 0 if p["complete"] else 1
        if a.cmd == "verify":
            ex = SobExports()
            probs = units_file_problems(g.REPO / UNITS_REL, ex)
            probs += verify_scanned({UNITS_REL: g.sha256_file(g.REPO / UNITS_REL)}, load_pins(), require=True)
            print(json.dumps({"units": len(ex.unit_hashes), "problems": probs}, indent=1))
            return 1 if probs else 0
        if a.cmd == "fetch-splits":
            print(json.dumps(fetch_splits(), indent=1, sort_keys=True))
            return 0
        if a.cmd == "build-splits":
            try:
                acc = {k: int(v) for k, _, v in (x.partition("=") for x in a.accept_count)}
            except ValueError:
                print("sob_g13 refused: --accept-count wants NAME=N")
                return 2
            p = build_splits(accept_counts=acc)["sob_splits"]
            print(json.dumps({"complete": p["complete"], "gaps": p["gaps"], "units": p["files"][SPLITS_UNITS_REL], "count_deviations": p["count_deviations"],
                              "source_sha256": p["source"]["file_sha256"], "counts": p["counts"],
                              "splits": {k: {x: v[x] for x in ("count", "units", "revision", "bench_cases_linked")} for k, v in p["splits"].items()}},
                             indent=1, sort_keys=True))
            return 0 if p["complete"] else 1
        if a.cmd == "verify-splits":
            pins = load_pins(SPLITS_PINS)
            ex = SplitExports()
            f = g.REPO / SPLITS_UNITS_REL
            units = [json.loads(x) for x in f.read_text(encoding="utf-8").splitlines() if x.strip()]
            probs = units_file_problems(f, ex) + splits_pin_problems(units, pins)
            probs += verify_scanned({SPLITS_UNITS_REL: g.sha256_file(f)}, pins, names=SPLIT_TARGETS, require=True)
            print(json.dumps({"units": len(ex.unit_hashes), "problems": probs}, indent=1))
            return 1 if probs else 0
        print(json.dumps(status(), indent=1, sort_keys=True))
        return 0
    except SobError as e:
        print(f"sob_g13 refused: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
