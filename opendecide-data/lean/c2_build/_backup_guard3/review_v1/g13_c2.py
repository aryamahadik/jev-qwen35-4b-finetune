"""g13_c2.py: the C2 G13 decontamination wrapper (C2_DATA_SPEC 6.1, 6.3 G13 / G-TPL, 6.4 steps 4, 8 and 10, 8.4;
PREREG A37 e, A38). CPU only, no network, $0. Counts and C2 ids only: no eval or OHS-4 text is ever printed or kept.

Runs (one process each, from lean/; several blocks of one run share one eval pass):
  ../.venv/bin/python c2_build/g13_c2.py seed [--block T28 ...]   G13-seed on the frozen Haiku pools, before any row
        (step 4). Every pool record (skin, wording, lexicon form, paraphrase, pack, document) is one TEMPLATE unit; any
        hit quarantines that template only. The A31 (b) "not rendered" exemption of decontam_g13 does not apply to a
        pool (at seed time no row exists, and the pool is exactly what rows are rendered from). The family's program
        literals (plugin / vocab / fixtures) also go through G-TPL (gtpl_check) as program templates.
  ../.venv/bin/python c2_build/g13_c2.py candidates [--block ...]  G13 on every block's candidates_c2.jsonl (step 8,
        one batch): every method drops the whole unit (call_id). The block's program literals are decontam_g13 seeds
        exactly as round 1's gen/** (A31 b render check against the block's candidates).
  ../.venv/bin/python c2_build/g13_c2.py carry [--block F5 ...]    carry-over pools (round-1 candidates_r1): the NEW
        targets only (they passed the old ones in round 1).
  ../.venv/bin/python c2_build/g13_c2.py final                      the final mix data/c2_parts/c2_train.jsonl (step
        10): the NEW targets only on every row (replay rows passed the old targets in round 1, new rows at step 8).
  ../.venv/bin/python c2_build/g13_c2.py targets                    which targets resolve (file counts only)
  ../.venv/bin/python c2_build/g13_c2.py status                     every written C2 log: complete, written by the
                                                                    guarded code (inputs_at_start), inputs unchanged
                                                                    since, no dev file added since, pinned exports (exit
                                                                    1 on a problem)
  options: --no-embed (method 5 off: the log stays incomplete), --no-side (A25 d child off: incomplete),
           --side-serial, --dry (build the training side only; nothing is read on the eval side or written)

Targets
  old  decontam_g13.targets(), through decontam_g13.run_sets (c_build/decontam_g13.py, imported read-only, never
       edited): the 9 dev splits, round-1 mixdev (A25 c) + its structure keys, JevBench item files, BTZSC, eval_opi /
       eval_jagged, OHS-1/2 and their cached sources, TabFact, HateXplain, SBF, ejs-5, DI test, the A25 (d) sealed-side
       child (OHS-3, its sources, LongBench v2: its own process, counts and unit indices only), method 8 (OPI / jagged
       templates, dev / eval instructions both ways) and the sealed_nd suite checker. Methods 1-9 as there.
  new  ohs4_hash   c2_build/sealed_hashes/ (FORMAT.md), applied here by program after its sha256s are checked against
                   MANIFEST.json, the pinned manifest sha and the A38 freeze sha. Binding: word 10- / 12-grams,
                   exact normalised text (>= 5 words), exact raw text (>= 5 words), sentences / lines (>= 5 words),
                   the keyword block-list (runs of 1-8 tokens, URL hosts), R / U structure (struct_g13 of state +
                   options, skeleton of the state, of each state line, of the instructions; state / instructions
                   >= 5 words). Report-only: exact matches of texts under 5 words (short labels and options; the
                   sealed child's exact_short decides those).
       ohs4_rows   ohs4_sealed/tools/g13_ohs4_check.py, RUN only (CHECKERS.md): exact / segment / short / substring /
                   10- and 12-gram / Tulu 8-gram / MinHash / structure vs the full suite; returns C2 ids only.
       ohs4_gtpl   ohs4_sealed/tools/gtpl_check.py, RUN only: G-TPL, 8-grams of C2 templates (pools and program
                   literals, cut at every placeholder) vs the suite's R / U wording; a hit quarantines the template.
       c2_mixdev       data/c2_mixdev.jsonl + data/c2_parts/*/out/mixdev_S5.jsonl, once they exist: instance content
                       only (eval state + options vs training state + options; the A25 (c) rule: the family's card
                       and question wording is shared on purpose) + method 6 keys (meta.structure_hash, struct_g13,
                       group_id).
       (c2_t37b_dev    removed 16 Oct 2026: T37b is in C3 (A52 a), so no T37b-dev set exists.)
       c2_transfer_dev data/c2_transfer_dev.jsonl: every field (never-trained families, like the 9 dev splits) +
                       method 6 keys.
       A missing C2 dev set keeps the log incomplete (spec 7.1: built before training); pools skip them (templates
       are shared with the dev rows by design; rows are checked at step 8).

Never opened by this program: any "ohs" path (the sealed checkers are only RUN, by path, with input files written to
the system temp folder and their result JSON read back), sealed_nd, sealed_brief, preread, quarantine, LongBench, Jev
files, ~/.claude/projects, the session temp folder (c2io.refusal on every input). Output (kit guarded writer, A38
first): logs/decontam_counts/c2_<run>_<block>.json = {"drop_ids" (rows of every hit unit; [] for pools),
"quarantine" (pool templates), "counts_by_target_and_method", "report_only", "engine" (the decontam_g13 record),
"ohs4" (export and checker records), "complete", "incomplete_why", "inputs_at_start", ...}. mix_c2 --decontam-drops and
c2_select --exclude-ids read "drop_ids".

Run-input guard (16 Oct 2026; found in candidates batch 3). Before the engine reads anything, run() records the sha256 of
every file the run reads or re-reads later: this program and decontam_g13.py (as they were when this process imported
them: a code fix made after the import is NOT in the running code), the C2 dev files (c2_mixdev files, c2_transfer_dev),
the run's training / pool / program-literal files and, for a final run, the family files A53 re-reads at the end. The
snapshot is stored in every result as "inputs_at_start" (file basename -> sha256; a lean/-relative path when two files
share a basename) with "inputs_at_start_paths" (the same names -> lean/-relative path, so `status` can find each file).
At the A53 step and again just before each result JSON is written, the hashes (and the set of dev files) are recomputed;
a file that differs, appeared or is gone makes that result complete=False with an "incomplete_why" entry "<file> changed
during the run: re-run", and A53 applies no waiver at all for a result with a changed input (more drops, never fewer).
Without this the engine could scan the old mixdev files while A53 read the rebuilt ones.
  * The training / candidates / pool / final-mix / program-literal files are read by build_sets BEFORE the guard exists.
    build_sets therefore hashes each of them before it reads anything, checks again after the read (a file that changed
    while it was being read refuses the run: ReadChanged), and the guard takes that build-time sha256 as the file's start
    value instead of hashing the file again (a change right after build_sets is seen).
  * A change that shows up only at the last check (after the A53 step already waived units) withdraws the waivers:
    drop_ids, drop_units, counts and quarantine are put back to what no waiver would have given (withdraw_waivers), so
    drop_ids never shrink because of a changed input. The record is complete=False either way.
  * `status` flags (a) a candidates / carry / final log with no inputs_at_start as "pre-guard log: re-run", (b) any
    inputs_at_start dev / training / pool / program-literal file whose sha256 now differs, or that is gone, as "changed
    after the run" (the two code files are not compared: a code edit mid-run is the guard's job), and (c) a dev file that
    exists now (the c2_mixdev target is a glob: data/c2_parts/*/out/mixdev_S5.jsonl) but is not in the log's
    inputs_at_start, as "changed after the run (appeared after the run ...)": the current resolved dev-file set is compared
    with the recorded one.
  * A path is checked against the never-open rule before it is stat-ed or hashed: RunGuard (_sha_now, _items), build_sets
    (_sha_map, pool_files, code_seed_units), A53Context / A53State.context, and the engine-inputs and inputs_at_start
    loops of `status` (log_problems). build_sets lists the pool files once and gives that one list to the sha map and to
    pool_units, so no file is read that the guard does not hold.
mix_c2 refuses a G13 log that is not complete or is stale (mix_c2.g13_log_problems = c2_select.g13_log_problems, the same
check c2_select --exclude-ids runs): a candidates / carry / final log whose recorded training sha256 or C2 dev-file shas
differ from the files now, or that misses a dev file that exists now, is refused with "stale G13 log (<file> changed after
the run): re-run G13 for <block>". --final stops, a dry run lists the problem.
"""
from __future__ import annotations

import argparse
import contextlib
import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
import uuid
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent            # lean/c2_build
sys.path.insert(0, str(HERE))
import c2io  # noqa: E402  (guard, layout; puts c_build on sys.path)
from c2_kit import paths as kp  # noqa: E402

import numpy as np  # noqa: E402
import decontam_g13 as g  # noqa: E402  (c_build: imported read-only, never edited)

LEAN = c2io.LEAN
OUT = LEAN / "logs" / "decontam_counts"
EXPORTS = HERE / "sealed_hashes"
SEALED_HASHES_MANIFEST_SHA256 = "3771b47ad06157a97973eaf3539c9bde0b87e97b5b4458148a51f2506025470b"
OHS4_FREEZE_SHA256 = "c0217e7739c570b9d22176b68e1c489623dcd5f7c551011606b6ff17e59c09c3"   # A38: OHS-4 MANIFEST.json
SEALED_TOOLS = LEAN / "ohs4_sealed" / "tools"     # RUN only: never opened, listed, hashed or copied
G13_OHS4_TOOL = SEALED_TOOLS / "g13_ohs4_check.py"
GTPL_TOOL = SEALED_TOOLS / "gtpl_check.py"
CHECKER_TIMEOUT = 6 * 3600
FAMILY_DIRS = {"T37b": HERE / "t37b", **{t: HERE / "transfer" / t for t in c2io.TRANSFER_DEV}}
CODE_FILES = ("plugin.py", "vocab.py", "fixtures.py", "builder.py", "sources.py", "polarity.py", "select.py")
RUNS = ("seed", "candidates", "carry", "final")

# ---- the C2 dev targets (spec 7.1; paths as mix_c2.DEV_SETS) ------------------------------------------------------
C2_DEV = {
    "c2_mixdev": {"paths": ["lean:data/c2_mixdev.jsonl", "lean:data/c2_parts/*/out/mixdev_S5.jsonl"],
                  "fields": g.MIXDEV_EVAL_FIELDS, "train_fields": g.MIXDEV_TRAIN_FIELDS,
                  "note": "C2 mixdev: instance content only (A25 c), every method; method 6 keys in c2_dev_structure"},
    # c2_t37b_dev is NOT a target: T37b moved to C3 (PREREG A52 a), so no T37b-dev set exists for C2 (spec 7.1's
    # "T37b-dev 300 pairs" is not built). Removed 16 Oct 2026; if T37b returns in C3, re-add it with its builder.
    "c2_transfer_dev": {"paths": ["lean:data/c2_transfer_dev.jsonl"], "fields": None, "train_fields": None,
                        "note": "transfer dev (T19, T21; never trained; T36 and T20 out by A45 c / A52): every field, every method"},
}
C2_STRUCT = "c2_dev_structure"


def c2_dev_targets() -> list[dict]:
    return [g.target(n, d["paths"], fields=d["fields"], train_fields=d["train_fields"], main_only=True,
                     note=d["note"]) for n, d in C2_DEV.items()]


def _glob_parts(base: Path, pat: str) -> list[Path]:
    """sorted(base.glob(pat)) for a pattern of '/'-separated parts with *, ? and [..] (no '**'), with the never-open rule
    applied to every path BEFORE it is listed or stat-ed: a folder is listed by name only (os.listdir) after the rule
    passed on it, and a child that is refused is dropped before its '<child>/out' is built (pathlib's glob would stat it
    first). A part with no wildcard is not looked up; the caller's is_file() decides whether the path exists."""
    cur = [base]
    for part in [x for x in pat.split("/") if x]:
        if "**" in part:
            raise ValueError(f"C2 dev pattern {pat!r}: '**' is not supported")
        nxt = []
        for d in cur:
            if any(c in part for c in "*?["):
                if not d.is_dir():
                    continue
                for nm in sorted(os.listdir(d)):
                    q = d / nm
                    if fnmatch.fnmatchcase(nm, part) and not c2io.refusal(q):
                        nxt.append(q)
            else:
                q = d / part
                if not c2io.refusal(q):
                    nxt.append(q)
        cur = nxt
    return cur                                                   # every level in name order: the order of sorted(glob)


def resolve_dev_spec(spec: str) -> list[Path]:
    """decontam_g13.resolve(spec) for the specs a C2 dev target uses (lean:, repo:, od:, abs:), same files, same order, same
    filters (a file; no README / LICENSE / .git / .md; one path per resolved file), but listed through _glob_parts so a
    refused folder or file is never stat-ed or scanned. Any other kind of spec is refused (ValueError)."""
    kind, _, rest = spec.partition(":")
    if kind == "lean":
        base, pat = g.LEAN, rest
    elif kind == "repo":
        base, pat = g.REPO, rest
    elif kind == "od":
        base, pat = g.LEAN.parent, rest
    elif kind == "abs":
        q = Path(rest)
        base, pat = q.parent, q.name
    else:
        raise ValueError(f"C2 dev spec {spec!r}: only lean:, repo:, od: and abs: specs are listed here")
    if c2io.refusal(base) or not base.exists():
        return []
    seen, out = set(), []
    for p in _glob_parts(base, pat):
        if not p.is_file() or p.name.lower().startswith(("readme", "license", ".git")) or p.suffix == ".md":
            continue
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            out.append(p)
    return out


def dev_files(name: str) -> list[Path]:
    """The existing files of one C2 dev target (main files only, never their companions). Listed through
    resolve_dev_spec: the never-open rule runs before any folder is scanned or path stat-ed."""
    out = []
    for spec in C2_DEV[name]["paths"]:
        out += [p for p in resolve_dev_spec(spec) if p.name.count(".") == 1 and not c2io.refusal(p)]
    return sorted(set(out))


# ================================================================================ FORMAT.md hashing (exactly)
_W = re.compile(r"[^\W_]+")
_SEG = re.compile(r"(?<=[.!?])\s+|\n+")
KW_STRIP = ".,;:!?\"'()[]{}<>"
URL_RE = re.compile(r"https?://[^\s\"'<>()\[\]{}]+", re.I)
SLOT_RE = re.compile(r"\{[^{}\s\"']*\}")          # kit placeholders and Python-format slots ({X}, {a|X}, {N|d|ds})
MIN_WORDS = 5


def words(t: str) -> list[str]:
    return _W.findall(unicodedata.normalize("NFKC", t).lower())


def norm(t: str) -> str:
    return " ".join(words(t))


def sha_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def skeleton(t: str) -> str:
    out = []
    for w in re.findall(r"[^\W_]+", unicodedata.normalize("NFKC", t)):
        if w.isdigit() or re.fullmatch(r"\d[\d]*", w):
            out.append("0")
        elif w[0].isupper():
            out.append("N")
        else:
            out.append(re.sub(r"\d+", "0", w.lower()))
    return " ".join(out)


struct_g13 = g.struct_g13                          # FORMAT.md: "= decontam_g13.struct_g13" (self-test below)


def gram_digests(ws: list[str], n: int) -> list[bytes]:
    return [hashlib.sha256(" ".join(ws[i:i + n]).encode()).digest() for i in range(len(ws) - n + 1)]


def keyword_hashes(text: str) -> set:
    """FORMAT.md keyword rule: runs of 1-8 whitespace tokens of the lower-cased, whitespace-collapsed text, stripped of
    punctuation at the run's two ends (the unstripped run is hashed too), >= 4 characters; plus URL hosts with and
    without a leading www."""
    toks = re.sub(r"\s+", " ", text.strip().lower()).split(" ") if text.strip() else []
    out = set()
    for i in range(len(toks)):
        for n in range(1, 9):
            if i + n > len(toks):
                break
            run = " ".join(toks[i:i + n])
            for r in {run, run.strip(KW_STRIP).strip()}:
                if len(r) >= 4:
                    out.add(sha_hex(r))
    for u in URL_RE.findall(text):
        host = urlsplit(u).netloc.lower()
        if host:
            out.add(sha_hex(host))
            out.add(sha_hex(host[4:] if host.startswith("www.") else "www." + host))
    return out


def template_pieces(text: str) -> list[str]:
    """A template cut at every placeholder and line break; a word glued to a placeholder ('{N}th') is dropped from its
    piece (it renders glued to a value). Pieces with >= 1 word."""
    out, at, glue_l = [], 0, False
    for m in [*re.finditer(SLOT_RE.pattern + r"|\n", text), None]:
        s, e = (m.start(), m.end()) if m else (len(text), len(text))
        glue_r = m is not None and m.group() != "\n"
        part = text[at:s]
        ws = part.split()
        if ws and glue_l and not part[:1].isspace():
            ws = ws[1:]
        if ws and glue_r and not part[-1:].isspace():
            ws = ws[:-1]
        if words(" ".join(ws)):
            out.append(" ".join(ws))
        at, glue_l = e, glue_r
    return out


# ================================================================================ the OHS-4 hash exports
class ExportError(RuntimeError):
    """The hash exports do not match their manifest, the pinned manifest sha or the A38 freeze."""


class Exports:
    """c2_build/sealed_hashes/, checked before use. Membership tests only; nothing here is ever printed."""

    TEXT_KINDS = ("full_text_norm", "full_text_norm_min5words", "full_text_raw", "sentence_norm_min5words")
    STRUCT_KINDS = ("structure_g13_R", "structure_g13_U", "skeleton_state_R", "skeleton_state_U", "skeleton_line_R",
                    "skeleton_line_U", "skeleton_instructions_R", "skeleton_instructions_U")

    def __init__(self, root: Path = EXPORTS, manifest_sha: str = SEALED_HASHES_MANIFEST_SHA256,
                 freeze_sha: str = OHS4_FREEZE_SHA256, prereg_text: str | None = None):
        ilog = c2io.C2InputLog()
        mp = root / "MANIFEST.json"
        got = g.sha256_file(ilog.record(mp))
        if manifest_sha and got != manifest_sha:
            raise ExportError(f"sealed_hashes/MANIFEST.json sha256 {got[:12]} is not the pinned {manifest_sha[:12]}")
        man = ilog.json(mp)
        if man.get("freeze_manifest_sha256") != freeze_sha:
            raise ExportError("sealed_hashes/MANIFEST.json does not name the A38 freeze manifest")
        a38 = _a38_block(c2io.PREREG.read_text(encoding="utf-8") if prereg_text is None else prereg_text)
        if freeze_sha not in a38:
            raise ExportError("the OHS-4 freeze sha is not in the 'Ruling A38' block of PREREG_FINAL.md")
        for name, d in man["files"].items():
            if g.sha256_file(ilog.record(root / name)) != d["sha256"]:
                raise ExportError(f"sealed_hashes/{name} differs from MANIFEST.json")
        self.shas = {"manifest": got, **{n: d["sha256"] for n, d in man["files"].items()}}
        self.records_by_kind = man.get("records_by_kind", {})
        self.ng = {n: self._grams(root / f"ngrams{n}_sha256.npy") for n in (10, 12)}
        self.sets = defaultdict(set)
        for f in ("text_hashes.jsonl", "structure_hashes.jsonl", "keyword_hashes.jsonl"):
            for line in (root / f).read_text(encoding="utf-8").splitlines():
                if line.strip():
                    r = json.loads(line)
                    self.sets[r["kind"]].add(r["hash"])
        for k, n in self.records_by_kind.items():
            if len(self.sets[k]) != n:
                raise ExportError(f"kind {k}: {len(self.sets[k])} hashes, manifest says {n}")
        self.struct = {k[:-2]: self.sets[k[:-2] + "_R"] | self.sets[k[:-2] + "_U"]
                       for k in self.STRUCT_KINDS if k.endswith("_R")}

    @staticmethod
    def _grams(p: Path):
        a = np.load(p)
        if a.ndim != 2 or a.shape[1] != 32 or a.dtype != np.uint8:
            raise ExportError(f"{p.name}: not a [n, 32] uint8 digest array")
        pre = a[:, :8].copy().view(">u8").ravel().astype(np.uint64)
        if len(pre) > 1 and not np.all(pre[1:] >= pre[:-1]):
            raise ExportError(f"{p.name}: digests are not sorted")
        return a, pre

    def has_grams(self, n: int, digests: list[bytes]) -> bool:
        if not digests:
            return False
        a, pre = self.ng[n]
        q = np.array([int.from_bytes(d[:8], "big") for d in digests], np.uint64)
        lo, hi = np.searchsorted(pre, q, "left"), np.searchsorted(pre, q, "right")
        for i in np.nonzero(hi > lo)[0].tolist():
            want = np.frombuffer(digests[i], np.uint8)
            if any(np.array_equal(a[j], want) for j in range(lo[i], hi[i])):
                return True
        return False


def _a38_block(text: str) -> str:
    m = kp.A38_RE.search(text)
    if not m:
        return ""
    out = []
    for line in text[m.start():].splitlines():
        if out and not line.startswith(">"):
            break
        out.append(line)
    return "\n".join(out)


def ohs4_hash_hits(units: list[dict], ex: Exports) -> tuple[dict, dict]:
    """The FORMAT.md compare of every unit: ({method: {unit key: fields}}, report-only counts). Row units carry their
    rows (state, instructions, card, options); template units their texts, cut at placeholders."""
    hits, rep = defaultdict(lambda: defaultdict(set)), defaultdict(int)
    cache: dict = {}

    def text_methods(t: str, cut: bool) -> tuple:
        k = (t, cut)
        if k in cache:
            return cache[k]
        got, short = set(), set()
        for piece in (template_pieces(t) if cut else [t]):
            ws = words(piece)
            if ex.has_grams(10, gram_digests(ws, 10)):
                got.add("ngram10")
            if ex.has_grams(12, gram_digests(ws, 12)):
                got.add("ngram12")
            if len(ws) >= MIN_WORDS:
                if sha_hex(" ".join(ws)) in ex.sets["full_text_norm_min5words"]:
                    got.add("exact_full")
                if not cut and sha_hex(piece) in ex.sets["full_text_raw"]:
                    got.add("exact_raw")
            elif ws:
                if sha_hex(" ".join(ws)) in ex.sets["full_text_norm"]:
                    short.add("exact_short_norm")
                if not cut and sha_hex(piece) in ex.sets["full_text_raw"]:
                    short.add("exact_short_raw")
            for s in _SEG.split(piece):
                sw = words(s)
                if len(sw) >= MIN_WORDS and sha_hex(" ".join(sw)) in ex.sets["sentence_norm_min5words"]:
                    got.add("exact_sentence")
            if keyword_hashes(piece) & ex.sets["keyword"]:
                got.add("keyword")
        if cut:
            for line in t.split("\n"):
                if not SLOT_RE.search(line) and _line_skel_hit(line, ex):
                    got.add("skeleton_line")
        cache[k] = (frozenset(got), frozenset(short))
        return cache[k]

    for u in units:
        key = u["key"]
        for field, t in u["texts"]:
            got, short = text_methods(t, u.get("template", False))
            for m in got:
                hits[m][key].add(field)
            for m in short:
                rep[m] += 1
        for r in u.get("rows_src", ()):
            st, opts, ins = r.get("state"), r.get("options"), r.get("instructions")
            if isinstance(st, str) and len(words(st)) >= MIN_WORDS:
                sg = struct_g13(st, opts if isinstance(opts, list) else None)
                if sg in ex.struct["structure_g13"]:
                    hits["structure_g13"][key].add("state+options")
                if sha_hex(skeleton(st)) in ex.struct["skeleton_state"]:
                    hits["skeleton_state"][key].add("state")
            if isinstance(st, str):
                for line in st.split("\n"):
                    if _line_skel_hit(line, ex):
                        hits["skeleton_line"][key].add("state")
            if isinstance(ins, str) and len(words(ins)) >= MIN_WORDS and \
                    sha_hex(skeleton(ins)) in ex.struct["skeleton_instructions"]:
                hits["skeleton_instructions"][key].add("instructions")
    return {m: dict(v) for m, v in hits.items()}, dict(rep)


def _line_skel_hit(line: str, ex: Exports) -> bool:
    sk = skeleton(line)
    toks = sk.split()
    return len(toks) >= 6 and sum(t not in ("0", "N") for t in toks) >= 3 and \
        sha_hex(sk) in ex.struct["skeleton_line"]


# ================================================================================ units
def row_fields(r: dict) -> list[tuple[str, str]]:
    """Model-visible texts of a row as the exports hash them: state, instructions, card (a string; a mapping or list as
    sorted-key JSON plus every string leaf), every option."""
    out = [(f, r.get(f)) for f in ("state", "instructions")]
    c = r.get("card")
    if isinstance(c, str):
        out.append(("card", c))
    elif isinstance(c, (dict, list)) and c:
        out.append(("card", json.dumps(c, ensure_ascii=False, sort_keys=True)))
        out += [("card", x) for x in g.leaves(c)]
    out += [("option", o) for o in (r.get("options") or []) if isinstance(o, str)]
    return [(f, t) for f, t in out if isinstance(t, str) and t.strip()]


def row_units(rows: list[dict]) -> list[dict]:
    """One unit per call_id (the mixer's unit; decontam_g13.train_units groups the same way): row ids, texts, the full
    rows (structure methods) and the method 6 keys."""
    units, at = [], {}
    for r in rows:
        k = str(r.get("call_id") or r["id"])
        if k not in at:
            at[k] = len(units)
            units.append({"key": k, "rows": [], "source": str(r.get("source") or "?"), "seed": False, "texts": [],
                          "rows_src": [], "struct": set(), "s_g13": set(), "groups": set()})
        u = units[at[k]]
        u["rows"].append(str(r["id"]))
        u["texts"] += row_fields(r)
        u["rows_src"].append(r)
        m = r.get("meta") if isinstance(r.get("meta"), dict) else {}
        if isinstance(m.get("structure_hash"), str) and m["structure_hash"]:
            u["struct"].add(m["structure_hash"])
        if r.get("group_id") not in (None, ""):
            u["groups"].add(str(r["group_id"]))
        sg = struct_g13(r.get("state"), r.get("options"))
        if sg:
            u["s_g13"].add(sg)
    return units


POOL_META = {"id", "skin_id", "template_id", "form_id", "pack_id", "doc_id", "wording_id", "family", "kind",
             "register", "escape", "author_mode", "qform", "sem", "sem_id", "haiku_task_id", "haiku_prompt_sha",
             "sha256", "status", "lexicon_ids", "held_out", "slots", "counts", "role", "source", "task_id",
             "answer_file", "created_utc", "admitted", "extractions", "reads", "votes"}
POOL_ID_KEYS = ("skin_id", "template_id", "form_id", "wording_id", "pack_id", "doc_id", "id")
POOL_EXT = (".jsonl", ".json", ".txt")


def pool_records(p: Path, ilog) -> list[tuple[int, object]]:
    """(line, record) of one pool file: JSONL lines, a JSON list / dict of record lists / single dict, TXT lines."""
    ilog.record(p)
    text = p.read_text(encoding="utf-8", errors="replace")
    if p.suffix == ".txt":
        return [(i, ln) for i, ln in enumerate(text.splitlines(), 1) if ln.strip()]
    if p.suffix == ".jsonl":
        out = []
        for i, ln in enumerate(text.splitlines(), 1):
            if ln.strip():
                out.append((i, json.loads(ln)))
        return out
    d = json.loads(text)
    if isinstance(d, list):
        return [(i, x) for i, x in enumerate(d)]
    if isinstance(d, dict):
        big = [v for v in d.values() if isinstance(v, list) and v and isinstance(v[0], dict)]
        if big:
            return [(i, x) for i, x in enumerate(r for v in big for r in v)]
        return [(0, d)]
    return []


def pool_texts(rec) -> list[str]:
    if isinstance(rec, str):
        return [rec]
    if isinstance(rec, dict):
        return [t for k, v in rec.items() if k not in POOL_META for t in g.leaves(v) if isinstance(t, str)]
    return [t for t in g.leaves(rec) if isinstance(t, str)]


def pool_files(root: Path) -> list[Path]:
    """The files pool_units reads under one pools folder (a never-open pool file raises C2Refused, before any stat)."""
    if c2io.refusal(root):
        raise c2io.C2Refused(f"pools folder refused: {root}")         # the never-open rule before the first stat
    if not root.is_dir():
        return []
    out, todo = [], [root]
    while todo:                                                    # the folders under root, listed one at a time (no rglob)
        with os.scandir(todo.pop()) as it:
            entries = sorted(it, key=lambda e: e.name)
        for e in entries:
            p = Path(e.path)
            if c2io.refusal(p):                                    # a refused file OR folder: before any stat or listing of it
                raise c2io.C2Refused(f"pool path refused: {p}")
            if e.is_dir(follow_symlinks=False):                    # (a symlinked folder is not entered: as rglob)
                if p.name != "__pycache__":
                    todo.append(p)
                continue
            if p.suffix not in POOL_EXT or g.SEED_SKIP.search(p.name) or "__pycache__" in p.parts:
                continue
            if p.is_file():
                out.append(p)
    return sorted(out)


def pool_units(block: str, root: Path, ilog, files: list[Path] | None = None) -> tuple[list[dict], dict]:
    """One TEMPLATE unit per pool record under <block dir>/pools/ (manifests, reports and checks skipped). `files` = the
    listing pool_files(root) gave (build_sets passes the one it hashed, so no file is read that the guard does not hold)."""
    units, shas = [], {}
    for p in (pool_files(root) if files is None else files):
        if c2io.refusal(p):
            raise c2io.C2Refused(f"pool file refused: {p}")          # also for a listing handed in
        rel = lean_rel(p)
        recs = pool_records(p, ilog)
        shas[rel] = g.sha256_file(p)
        for line, rec in recs:
            ts = [t for t in pool_texts(rec) if t.strip()]
            if not ts:
                continue
            tid = next((str(rec[k]) for k in POOL_ID_KEYS if isinstance(rec, dict) and rec.get(k) not in (None, "")),
                       f"{rel}#{line}")
            units.append({"key": f"pool:{rel}#{line}", "rows": [], "source": f"pool:{block}", "seed": True,
                          "public": False, "line": line, "template": True, "template_id": tid, "file": rel,
                          "texts": [("pool", t) for t in ts]})
    return units, shas


def code_seed_units(block: str, root: Path) -> tuple[list[dict], dict]:
    """The block's program literals (decontam_g13 seed units, the round-1 gen/** contract: A31 b render check)."""
    units, shas = [], {}
    for name in CODE_FILES:
        p = root / name
        if c2io.refusal(p) or not p.is_file():                     # the never-open rule first: nothing is stat-ed before it
            continue
        rel = lean_rel(p)
        texts = [x for x in g._seed_texts(p) if len(g.words(x[0])) >= 2]
        if not texts:
            continue
        shas[rel] = g.sha256_file(p)
        for i, (t, ln, rt) in enumerate(texts):
            u = {"key": f"seed:{rel}#{i}", "rows": [], "source": f"seed:{rel}", "seed": True, "public": False,
                 "line": ln, "texts": [("seed", t)], "template": True, "file": rel, "template_id": f"{rel}#{i}"}
            if rt != t:
                u["render_text"] = rt
            units.append(u)
    return units, shas


def lean_rel(p: Path) -> str:
    """lean/-relative posix path (absolute outside lean/, e.g. test folders)."""
    try:
        return Path(p).resolve().relative_to(LEAN.resolve()).as_posix()
    except ValueError:
        return Path(p).as_posix()


def block_dir(block: str) -> Path:
    return FAMILY_DIRS.get(block, HERE / "families" / block)


def engine_units(units: list[dict]) -> list[dict]:
    """The decontam_g13 view of our units (its keys; pool texts of >= 2 words, as its seed rule)."""
    out = []
    for u in units:
        e = {k: u[k] for k in ("key", "rows", "seed") if k in u}
        e["source"] = u.get("source", "?")
        e["public"] = u.get("public", False)
        e["line"] = u.get("line")
        e["texts"] = [(f if f != "pool" else "seed", t) for f, t in u["texts"]
                      if not u.get("seed") or len(g.words(t)) >= 2]
        for k in ("struct", "s_g13", "groups", "render_text"):
            if k in u:
                e[k] = u[k]
        out.append(e)
    return out


# ================================================================================ the sealed-side checkers (RUN only)
class CheckerError(RuntimeError):
    pass


@contextlib.contextmanager
def fresh_tempdir(prefix: str):
    """tempfile.TemporaryDirectory(prefix=prefix) with a name that cannot be on the never-open list. TemporaryDirectory adds
    8 random characters from a-z, 0-9 and '_': about one name in 2,700 holds 'ohs' or 'jev', and a run then died with "the
    temp folder is on the never-open list" at its checker step, after the engine's hours. Here the random part is 32 hex
    digits (no 'o', 'h', 's', 'j' or 'v'). A temp BASE folder that is itself refused still fails (CheckerError), before
    anything is created. Yields the folder's path (str); the folder is removed on exit."""
    td = Path(tempfile.gettempdir()) / (prefix + uuid.uuid4().hex)
    if c2io.refusal(td):                                           # the string rule first: nothing is created or stat-ed
        raise CheckerError("the temp folder is on the never-open list")
    td.mkdir(mode=0o700)
    try:
        yield str(td)
    finally:
        shutil.rmtree(td, ignore_errors=True)


def run_checker(tool: Path, flag: str, records: list[dict], extra: list | None = None, py: str = sys.executable,
                timeout: int = CHECKER_TIMEOUT) -> dict:
    """Run one sealed-side checker on `records` (written to the system temp folder, never inside the sealed folder);
    read back only its result JSON. The tool file itself is never opened, listed or hashed here."""
    with fresh_tempdir("c2g13_") as td:
        inp, outp = Path(td) / "in.jsonl", Path(td) / "result.json"
        with open(inp, "w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        t0 = time.time()
        p = subprocess.run([py, str(tool), flag, str(inp), "--out", str(outp)] + list(extra or []),
                           capture_output=True, text=True, cwd=str(LEAN), timeout=timeout)
        rec = {"tool": tool.name, "exit": p.returncode, "records_sent": len(records),
               "wall_s": round(time.time() - t0, 1)}
        if p.returncode in (0, 4) and outp.exists():
            d = json.loads(outp.read_text(encoding="utf-8"))
            rec.update({k: d.get(k) for k in ("version", "manifest_verified", "suite_sha256", "g13_sha256",
                                              "input_sha256", "counts", "complete", "methods", "scope_parts",
                                              "params", "ngram")})
            rec["hit_ids"] = [str(x) for x in d.get("hit_ids") or []]
            rec["hit_ids_by_method"] = {m: [str(x) for x in v] for m, v in (d.get("hit_ids_by_method") or {}).items()}
            rec["status"] = "scanned" if d.get("complete") and d.get("manifest_verified") else "incomplete"
            return rec
        if "can't open file" in (p.stderr or ""):
            rec["status"] = "missing"
        elif p.returncode == 3:
            rec["status"] = "suite changed since the freeze manifest"
        else:
            try:
                err = json.loads((p.stdout or "").strip().splitlines()[-1]).get("error")
            except (ValueError, IndexError, AttributeError):
                err = None
            rec["status"] = f"failed ({err or 'exit ' + str(p.returncode)})"
        return rec


def checker_rows(sets: dict) -> tuple[list[dict], dict]:
    """g13_ohs4_check input: one record per C2 row (template units: one per text, the unit as call_id). Ids carry
    their set so a hit maps back."""
    recs, back = [], {}
    for name, units in sets.items():
        for u in units:
            cid = f"{name}|{u['key']}"
            if u.get("template"):
                for j, (_f, t) in enumerate(u["texts"]):
                    rid = f"{cid}#{j}"
                    recs.append({"id": rid, "call_id": cid, "state": t})
                    back[rid] = (name, u["key"])
            else:
                for r in u["rows_src"]:
                    rid = f"{name}|{r['id']}"
                    recs.append({"id": rid, "call_id": cid, **{k: r.get(k) for k in ("state", "instructions", "card",
                                                                                     "options")}})
                    back[rid] = (name, u["key"])
    return recs, back


def gtpl_records(sets: dict) -> tuple[list[dict], dict]:
    recs, back = [], {}
    for name, units in sets.items():
        for u in units:
            if not u.get("template"):
                continue
            for j, (_f, t) in enumerate(u["texts"]):
                tid = f"{name}|{u['key']}#{j}"
                recs.append({"id": tid, "text": SLOT_RE.sub("{X}", t)})
                back[tid] = (name, u["key"])
    return recs, back


# ================================================================================ C2 method 6 (dev structure keys)
def dev_struct_keys(names, ilog) -> tuple[dict, dict]:
    keys, rec = {"structure": set(), "structure_g13": set(), "group_id": set()}, {}
    for n in names:
        files = dev_files(n)
        items = 0
        for f in files:
            for r in ilog.jsonl(f):
                items += 1
                m = r.get("meta") if isinstance(r.get("meta"), dict) else {}
                if isinstance(m.get("structure_hash"), str) and m["structure_hash"]:
                    keys["structure"].add(m["structure_hash"])
                sg = struct_g13(r.get("state"), r.get("options"))
                if sg:
                    keys["structure_g13"].add(sg)
                if r.get("group_id") not in (None, ""):
                    keys["group_id"].add(str(r["group_id"]))
        rec[n] = {"files": len(files), "items": items}
    return keys, rec


def dev_struct_hits(units: list[dict], keys: dict) -> dict:
    uk = {"structure": "struct", "structure_g13": "s_g13", "group_id": "groups"}
    return {m: {u["key"]: {m} for u in units if u.get(uk[m]) and u[uk[m]] & keys[m]} for m in keys}



# ================================================================================ A53: G13 vs the C2-side dev targets
# PREREG Ruling A53 (16 Oct 2026; rule text c2_build/zed_orch/G13_DEV_TARGET_DRAFT.md, sha256 9f3393df...). For the
# targets c2_mixdev and c2_transfer_dev ONLY, a shared item (word 10-gram, >= 5-word segment or >= 5-word option) between
# a training unit and a dev row is not a hit when it is a family frame item: (A) asset-independent (in the block's
# candidates it spans >= min(5, n) distinct values of each of skin_id / wording_id / card_id / domain_pack that has
# n >= 2 values) or (C) tiled by the family's frozen program literals (spans of >= 2 words inside one string literal of
# its code files cut at placeholders; a single word only at the item's two ends or as a whole literal). Precondition per
# (block, target): the dev rows share no skin_id, register, card_id, wording_id or domain_pack with the block's
# candidates (c2_mixdev: the block's own mixdev rows, meta.family == block), else no waiver. A unit with ANY non-waived
# shared item, or with no computable shared item, keeps every hit as before (whichever method found it). Nothing else
# (sealed, public, old dev, G-TPL, structure keys) is touched. Items here are a superset of the engine's (all texts for
# the transfer dev), so the waiver can only be rarer than the rule's text.
A53_TARGETS = ("c2_mixdev", "c2_transfer_dev")
A53_MIN_DISTINCT = 5
A53_DIMS = ("skin", "wording", "card", "pack")
A53_PLACEHOLDER = re.compile(r"\{[^{}]*\}|%\(\w+\)[sd]|%[sd]")
A53_SEG = re.compile(r"(?<=[.!?])\s+|\n+")
A53_RULING = "PREREG A53"


# PREREG A54 (1): the precondition compares the PACK ID, not a domain label. meta.domain_pack is a pack id when it names a
# pack (t06.act.brelmoria.S4.c03, t26-pack-cassillo, t31:appr:p31, t01-anchor-p3, t07-placeholder-34); it is a bare domain
# LABEL, shared with training by design, when it is "<family>:<domain>" with one colon and letters only (T23: t23:travel).
# A bare label carries no pack identity and is not compared.
A53_DOMAIN_LABEL = re.compile(r"^[a-z0-9]+:[a-z_]+$")
# A54 (a): T01's domain_pack is an in-code card-slot label t01-<kind>-p<card % 4>; T01 has no pack vocabulary (its plugin
# reads no pack file), so it carries no pack identity either. Cards are still compared (card_id).
A53_CARD_SLOT_LABEL = re.compile(r"^t01-[a-z]+-p[0-3]$")


def a53_pack_id(m: dict):
    v = m.get("domain_pack")
    if not isinstance(v, str) or A53_DOMAIN_LABEL.match(v) or A53_CARD_SLOT_LABEL.match(v):
        return None
    return v


def a53_assets(r: dict) -> dict:
    m = r.get("meta") if isinstance(r.get("meta"), dict) else {}
    c = m.get("c2") if isinstance(m.get("c2"), dict) else {}
    return {"skin": c.get("skin_id"), "wording": m.get("wording_id"), "card": m.get("card_id"),
            "pack": a53_pack_id(m), "register": c.get("register")}


def _a53_text_items(t: str, ng: bool, seg: bool, full: bool) -> set:
    w = words(t)
    out = set()
    if ng:
        out.update(("ng", " ".join(w[i:i + 10])) for i in range(len(w) - 9))
    if seg:
        for part in A53_SEG.split(t):
            sw = words(part)
            if len(sw) >= MIN_WORDS:
                out.add(("seg", " ".join(sw)))
    if full and len(w) >= MIN_WORDS:
        out.add(("opt", " ".join(w)))
    return out


def a53_row_items(r: dict, all_fields: bool) -> set:
    """Shared-item candidates of one row. c2_mixdev: state (10-grams, segments) + options (segments, whole option).
    c2_transfer_dev (every field): the same for every model-visible text of the row."""
    out = set()
    if all_fields:
        for f, t in row_fields(r):
            out |= _a53_text_items(t, True, True, f != "state")
    else:
        if isinstance(r.get("state"), str):
            out |= _a53_text_items(r["state"], True, True, False)
        for o in r.get("options") or []:
            if isinstance(o, str):
                out |= _a53_text_items(o, False, True, True)
    return out


class A53Context:
    """One block's A53 inventory: asset counts of its candidates and its program-literal spans."""

    def __init__(self, block: str, rows: list[dict], root: Path):
        self.block, self.root = block, root
        self.rows = rows
        self.ndist = {d: len({a53_assets(r)[d] for r in rows} - {None}) for d in A53_DIMS}
        self.has_assets = any(n >= 2 for n in self.ndist.values())    # (A) is vacuous without asset ids: then (C) only
        self.registers = {a53_assets(r)["register"] for r in rows} - {None}
        self.values = {d: {a53_assets(r)[d] for r in rows} - {None} for d in A53_DIMS}
        pieces = []
        for name in CODE_FILES:
            p = root / name
            if c2io.refusal(p) or not p.is_file():
                continue
            for t, _ln, _rt in g._seed_texts(p):
                for piece in A53_PLACEHOLDER.split(t):
                    w = words(piece)
                    if w:
                        pieces.append(tuple(w))
        self.n_pieces = len(pieces)
        self.whole = set(pieces)
        self.spans = set()
        for w in pieces:
            for L in range(2, min(len(w), 10) + 1):
                for i in range(len(w) - L + 1):
                    self.spans.add(w[i:i + L])
        self.big = " " + " | ".join(" ".join(w) for w in pieces) + " "
        self._memo: dict = {}

    def _span_ok(self, t: tuple, edge: bool) -> bool:
        n = len(t)
        if n == 1:
            return edge or t in self.whole
        if n <= 10:
            return t in self.spans
        return (" " + " ".join(t) + " ") in self.big

    def tiled(self, text: str) -> bool:
        key = tuple(text.split())
        if key not in self._memo:
            n = len(key)
            ok = [False] * (n + 1)
            ok[0] = True
            for j in range(1, n + 1):
                for i in range(j):
                    if ok[i] and self._span_ok(key[i:j], i == 0 or j == n):
                        ok[j] = True
                        break
            self._memo[key] = ok[n]
        return self._memo[key]

    def precondition(self, dev_rows: list[dict]) -> dict:
        dv = {d: {a53_assets(r)[d] for r in dev_rows} - {None} for d in A53_DIMS}
        shared = {d: len(dv[d] & self.values[d]) for d in A53_DIMS}
        shared["register"] = len(({a53_assets(r)["register"] for r in dev_rows} - {None}) & self.registers)
        return {"dev_rows": len(dev_rows), "shared_values": shared,
                "ok": bool(dev_rows) and self.n_pieces > 0 and not any(shared.values())}


class A53State:
    """Per-run cache: dev rows and their items per target, one context per block."""

    def __init__(self, ilog, dev_names=A53_TARGETS):
        self.ilog, self.ctx = ilog, {}
        self.dev = {n: [r for f in dev_files(n) for r in ilog.jsonl(f)] for n in dev_names}
        self.items = {n: set().union(*[a53_row_items(r, n == "c2_transfer_dev") for r in rows]) if rows else set()
                      for n, rows in self.dev.items()}

    def context(self, block: str, rows: list[dict] | None):
        if block not in self.ctx:
            root = block_dir(block)
            plugin = root / "plugin.py"
            if rows is None:
                f = c2io.fam_files(block)["cand"] if block in c2io.ALL_TARGETS else None
                # the never-open rule before the first stat (a family name comes from row metadata)
                rows = self.ilog.jsonl(f) if f is not None and not c2io.refusal(f) and f.exists() else []
            ok = bool(rows) and not c2io.refusal(root) and not c2io.refusal(plugin) and plugin.is_file()
            self.ctx[block] = A53Context(block, rows, root) if ok else None
        return self.ctx[block]


def a53_apply(run_name: str, s: dict, hits: dict, st: A53State | None, changed: list[str] | None = None) -> dict:
    """Apply A53 to `hits` (target -> method -> {unit key: fields}) in place; return the record for the log.
    `changed`: the run-input guard's messages (RunGuard.check) for this result; when there are any, an input the engine
    scanned is not the file A53 would read now, so no waiver is applied (every hit keeps binding)."""
    rec = {"ruling": A53_RULING, "applied_to": list(A53_TARGETS), "blocks": {}}
    if st is None or run_name not in ("candidates", "final"):
        rec["note"] = "not applied (no state or not a candidates / final run)"
        return rec
    if changed:
        rec["note"] = "not applied: an input changed during the run (re-run); no waiver from changed files"
        rec["changed_inputs"] = list(changed)
        return rec
    units = {u["key"]: u for u in s["units"]}

    def family(u):
        if run_name == "candidates":
            return s["block"]
        m = (u["rows_src"][0].get("meta") or {}) if u.get("rows_src") else {}
        return str(m.get("family") or "")

    for tg in A53_TARGETS:
        if tg not in hits:
            continue
        hit_units = {k for d in hits[tg].values() for k in d}
        by_fam = defaultdict(list)
        for k in sorted(hit_units):
            by_fam[family(units[k])].append(k)
        waived_all = set()
        for fam, keys in sorted(by_fam.items()):
            ctx = st.context(fam, [r for u in s["units"] for r in u["rows_src"]] if run_name == "candidates" else None)
            entry = {"units_hit": len(keys), "units_waived": 0, "eligible": False}
            rec["blocks"].setdefault(tg, {})[fam or "?"] = entry
            if ctx is None:
                entry["why"] = "no program inventory or candidates for this family (no waiver)"
                continue
            dev_rows = st.dev[tg]
            if tg == "c2_mixdev":
                dev_rows = [r for r in dev_rows if isinstance(r.get("meta"), dict) and r["meta"].get("family") == fam]
            pre = ctx.precondition(dev_rows)
            entry["precondition"] = pre
            if not pre["ok"]:
                entry["why"] = "precondition failed or no own dev rows / program literals (no waiver)"
                continue
            entry["eligible"] = True
            ev = st.items[tg]
            all_fields = tg == "c2_transfer_dev"
            iv = defaultdict(lambda: defaultdict(set))
            row_items = {}
            for r in ctx.rows:
                its = a53_row_items(r, all_fields) & ev
                row_items[r["id"]] = its
                a = a53_assets(r)
                for it in its:
                    for d in A53_DIMS:
                        iv[it][d].add(a[d])

            def ok_item(it):
                indep = ctx.has_assets and all(ctx.ndist[d] < 2 or len(iv[it][d] - {None}) >=
                                               min(A53_MIN_DISTINCT, ctx.ndist[d]) for d in A53_DIMS)
                return indep or ctx.tiled(it[1])

            verdict = {}
            for k in keys:
                its = set()
                for r in units[k]["rows_src"]:
                    its |= row_items.get(r["id"]) if r["id"] in row_items else (a53_row_items(r, all_fields) & ev)
                # in a final run a row may be absent from the candidates file: its items count, and an item the
                # asset counts never saw (iv empty) is not asset-independent, so it needs tiling.
                verdict[k] = bool(its) and all(ok_item(it) for it in its)
            wk = {k for k, v in verdict.items() if v}
            entry["units_waived"], entry["units_binding"] = len(wk), len(keys) - len(wk)
            waived_all |= wk
        if waived_all:
            rec.setdefault("waived_before_after", {})[tg] = {
                m: {"units_before": len(d), "units_after": len(set(d) - waived_all)} for m, d in sorted(hits[tg].items())}
            for m in list(hits[tg]):
                for k in waived_all:
                    hits[tg][m].pop(k, None)
                if not hits[tg][m]:
                    del hits[tg][m]
            if not hits[tg]:
                del hits[tg]
            rec.setdefault("waived_units", {})[tg] = len(waived_all)
            rec.setdefault("waived_units_sha256", {})[tg] = sha_hex("\n".join(sorted(waived_all)))
    return rec


# ================================================================================ the run-input guard
# Candidates batch 3 (16 Oct 2026): the engine scanned the OLD c2_mixdev files of T01 / T07 / T23 / T31 (read at run start),
# A53 re-read the dev files at the END of the run, after they were rebuilt, and the log's recorded input hashes (first read
# by ilog, after the engine) matched the NEW files, so nothing flagged it. The job had also imported this program before a
# code fix, so it ran older code than the file on disk at the end. RunGuard closes both holes (module docstring).
ALL = "*"                                           # scope of a file every result of the run depends on
CHANGED = "changed during the run: re-run"
CODE_GUARD = {"g13_c2.py": Path(__file__).resolve(), "decontam_g13.py": Path(g.__file__).resolve()}
# sha256 of the two code files as they were when this process imported them: the code the run actually executes.
_CODE_AT_IMPORT = {n: g.sha256_file(p) for n, p in CODE_GUARD.items()}


def _sha_now(p: Path) -> str | None:
    """sha256 of an existing file, else None. The never-open rule runs first: a refused path is not stat-ed or opened."""
    if c2io.refusal(p):
        return None
    try:
        return g.sha256_file(p) if p.is_file() else None
    except OSError:
        return None


class RunGuard:
    """sha256 snapshot of every input of one run (taken before the engine reads anything) and its re-checks.

    `collect()` -> [(path, scope, expected sha256 | None)], called at the start and again at every check, so a dev file
    that appears later is seen. scope = ALL or one set name (a result is judged by the ALL files and its own). The
    expected sha is used for the start snapshot only: the code files' import-time sha and the sha256 build_sets took of
    each training / pool / program-literal file BEFORE it read it (so a change after that read is a change, and a file
    gone since is listed as gone); None = hash the file now."""

    def __init__(self, collect):
        self._collect = collect
        self.start: dict[str, tuple[str | None, str]] = {}                 # resolved path -> (sha256, scope)
        for k, (sc, expect) in self._items().items():
            self.start[k] = (expect if expect is not None else _sha_now(Path(k)), sc)

    def _items(self) -> dict:
        out: dict = {}
        for p, sc, expect in self._collect():
            if c2io.refusal(p):
                continue                              # the never-open rule FIRST, on the path as given: no stat, no hash
            p = Path(p).resolve()
            if c2io.refusal(p):
                continue                              # ... and on where a symlink leads
            if expect is None and not p.is_file():
                continue                              # a file gone since the start is seen below (a file with an expected sha is kept: gone)
            k = str(p)
            if k in out:                                                    # listed twice: wider scope, keep the first expected sha
                sc, expect = (ALL if out[k][0] != sc else sc), (out[k][1] if out[k][1] is not None else expect)
            out[k] = (sc, expect)
        return out

    @staticmethod
    def _names(paths) -> dict:
        """file basename; the lean/-relative path when two guarded files share a basename (or a basename starts with '_':
        the guarded writer refuses private keys)."""
        by = defaultdict(list)
        for k in paths:
            by[Path(k).name].append(k)
        return {k: (Path(k).name if len(v) == 1 and not Path(k).name.startswith("_") else lean_rel(Path(k)))
                for v in by.values() for k in v}

    def inputs_at_start(self, name: str | None = None) -> dict:
        """{file basename: sha256} of the start snapshot (the ALL files and the set `name`'s own)."""
        names = self._names(self.start)
        return {names[k]: sha for k, (sha, sc) in sorted(self.start.items()) if name is None or sc in (ALL, name)}

    def paths_at_start(self, name: str | None = None) -> dict:
        """{file name as in inputs_at_start: lean/-relative path (absolute outside lean/)}: where `status` finds each file."""
        names = self._names(self.start)
        return {names[k]: lean_rel(Path(k)) for k, (_sha, sc) in sorted(self.start.items())
                if name is None or sc in (ALL, name)}

    def check(self, name: str | None = None) -> list[str]:
        """Recompute every hash (and the file set); one '<file> changed during the run: re-run (...)' message per file
        that differs, appeared or is gone. `name`: judge the ALL files and that set's own files only."""
        cur = {k: (_sha_now(Path(k)), sc) for k, (sc, _e) in self._items().items()}
        for k, (_sha, sc) in self.start.items():
            cur.setdefault(k, (_sha_now(Path(k)), sc))
        keys = sorted(set(self.start) | set(cur))
        names = self._names(keys)
        code = {str(Path(p).resolve()) for p in CODE_GUARD.values()}
        out = []
        for k in keys:
            was, sc = self.start[k] if k in self.start else (None, cur[k][1])
            now = cur[k][0]
            if name is not None and sc not in (ALL, name):
                continue
            if k not in self.start:
                out.append(f"{names[k]} {CHANGED} (appeared after the start)")
            elif now is None:
                out.append(f"{names[k]} {CHANGED} (gone)")
            elif now != was:
                when = "when the module was imported" if k in code else "at the start"
                out.append(f"{names[k]} {CHANGED} (sha256 {str(was)[:12]} {when}, {now[:12]} now)")
        return out

    def finalize(self, rec: dict, name: str) -> list[str]:
        """Re-check just before a result is written: a changed file not yet in rec['incomplete_why'] is added and the
        result is no longer complete. Returns the messages added."""
        have = {w.split(" (")[0] for w in rec["incomplete_why"]}
        new = [w for w in self.check(name) if w.split(" (")[0] not in have]
        if new:
            rec["incomplete_why"] = list(rec["incomplete_why"]) + new
            rec["complete"] = False
        return new


def a53_family_files() -> list[Path]:
    """What A53 re-reads for a family at the END of a final run (A53State.context): the family's candidates file and its
    program-literal files. Which families occur is not known at the start, so every target family is listed."""
    out = []
    for b in c2io.ALL_TARGETS:
        try:
            cand = c2io.fam_files(b)["cand"]
        except Exception:                                                   # noqa: BLE001  (layout not resolvable here)
            cand = None
        if cand is not None and not c2io.refusal(cand):
            out.append(Path(cand))
        out += [block_dir(b) / n for n in CODE_FILES]
    return out


def run_guard(run_name: str, sets: dict) -> RunGuard:
    """The guard of one run over `sets` (build_sets). Files: this program and decontam_g13.py (import-time sha), the C2 dev
    files (every run but a seed run, which does not read them), each set's training / pool / program-literal files, and for
    a final run the family files A53 re-reads."""
    static = []
    for n, s in sets.items():
        # start values = the sha256 build_sets took before it read each file (guard_shas; train_shas / seed_shas as a fallback)
        shas = s.get("guard_shas") or {**s["train_shas"], **s["seed_shas"]}
        for rel, sha in shas.items():
            static.append((Path(rel) if Path(rel).is_absolute() else LEAN / rel, n, sha))

    def collect():
        out = [(p, ALL, _CODE_AT_IMPORT.get(nm)) for nm, p in CODE_GUARD.items()]
        if run_name != "seed":
            out += [(p, ALL, None) for nm in C2_DEV for p in dev_files(nm)]
        out += [(p, n, sha) for p, n, sha in static]
        if run_name in ("seed", "candidates"):                              # A53Context reads these again at the end
            out += [(block_dir(s["block"]) / f, n, None) for n, s in sets.items() for f in CODE_FILES]
        if run_name == "final":
            out += [(p, ALL, None) for p in a53_family_files()]
        return out

    return RunGuard(collect)


# ================================================================================ the run
def load_rows(path: Path, ilog) -> list[dict]:
    return ilog.jsonl(path)


class ReadChanged(SystemExit):
    """An input changed while build_sets was reading it (run-input guard): nothing was written; run again."""


def _sha_map(paths) -> dict:
    """{path: sha256} of the existing files among `paths`, taken BEFORE they are read. The never-open rule is applied
    first: a refused path is never stat-ed or hashed here (its reader refuses it)."""
    out = {}
    for p in paths:
        p = Path(p)
        if not c2io.refusal(p) and p.is_file():
            out[p] = g.sha256_file(p)
    return out


def _unchanged_since_read(before: dict) -> None:
    """Raise ReadChanged unless every file in `before` ({path: sha256 before the read}) still has that sha256."""
    bad = sorted(p.name for p, sha in before.items() if _sha_now(p) != sha)
    if bad:
        raise ReadChanged(f"g13_c2: {bad} changed while the run's inputs were being read: re-run (nothing was written)")


def code_files(root: Path) -> list[Path]:
    return [root / n for n in CODE_FILES]


def build_sets(run: str, blocks: list[str], ilog) -> dict:
    """{set name: {"units" (pool templates or row units), "code" (program literal units), "train_shas", "seed_shas",
    "train_path", "block", "guard_shas"}}. Blocks without pools / candidates are skipped. "guard_shas" = {lean/-relative
    path: sha256 taken before the file was read} for every file read here (the run-input guard's start values; a file that
    changes while it is read raises ReadChanged)."""
    sets = {}
    for b in blocks:
        c2io.check_name(b, "block")
        if run == "seed":
            # the CURRENT frozen pool: pools_v2/ (freeze-v2 merge of v1 + redo rounds) when a family has one, else pools/
            pdir = block_dir(b) / "pools_v2" if (block_dir(b) / "pools_v2").is_dir() else block_dir(b) / "pools"
            pfiles = pool_files(pdir)                                  # listed ONCE: the sha map and pool_units get the same list
            before = _sha_map([*pfiles, *code_files(block_dir(b))])
            units, shas = pool_units(b, pdir, ilog, files=pfiles)
            if not units:
                continue
            code, cshas = code_seed_units(b, block_dir(b))
            _unchanged_since_read(before)
            sets[f"c2_seed_{b}"] = {"units": units, "code": code, "train_shas": {}, "seed_shas": {**shas, **cshas},
                                    "train_path": None, "block": b,
                                    "guard_shas": {lean_rel(p): sha for p, sha in before.items()}}
        elif run in ("candidates", "carry"):
            f = c2io.fam_files(b)["cand"]
            if not f.exists():
                continue
            before = _sha_map([f, *(code_files(block_dir(b)) if run == "candidates" else [])])
            units = row_units(load_rows(f, ilog))
            code, cshas = code_seed_units(b, block_dir(b)) if run == "candidates" else ([], {})
            _unchanged_since_read(before)
            sets[f"c2_{'cand' if run == 'candidates' else 'carry'}_{b}"] = {
                "units": units, "code": code, "train_shas": {lean_rel(f): before[f]},
                "seed_shas": cshas, "train_path": f, "block": b,
                "guard_shas": {lean_rel(p): sha for p, sha in before.items()}}
    if run == "final":
        f = c2io.C2_PARTS / "c2_train.jsonl"
        if f.exists():
            before = _sha_map([f])
            units = row_units(load_rows(f, ilog))
            _unchanged_since_read(before)
            sets["c2_final"] = {"units": units, "code": [], "train_shas": {lean_rel(f): before[f]},
                                "seed_shas": {}, "train_path": f, "block": "final",
                                "guard_shas": {lean_rel(p): sha for p, sha in before.items()}}
    return sets


def engine_targets(run: str) -> list[dict]:
    if run == "seed":
        return g.targets()
    if run == "candidates":
        return g.targets() + c2_dev_targets()
    return c2_dev_targets()                     # carry, final: the new targets only


def run(run_name: str, blocks: list[str], *, embed: bool = True, side: bool = True, side_parallel: bool = True,
        tgs: list[dict] | None = None, exports: Exports | None = None, write: bool = True,
        prereg_text: str | None = None) -> dict:
    """One G13 run over several blocks (one eval pass). Returns {set name: record}; writes each record (guarded)."""
    if run_name not in RUNS:
        raise ValueError(run_name)
    kp.require_a38(prereg_text)
    t0 = time.time()
    ilog = c2io.C2InputLog()
    sets = build_sets(run_name, blocks, ilog)
    if not sets:
        raise SystemExit(f"g13_c2 {run_name}: nothing to check (no pools / candidates / final mix on disk for "
                         f"{blocks or 'any block'})")
    guard = run_guard(run_name, sets)          # sha256 of every input (code included), BEFORE the engine reads anything
    tgs = engine_targets(run_name) if tgs is None else tgs
    why_all: list = []
    # ---- old targets + C2 dev targets: decontam_g13 (one eval pass for every set)
    eng_sets = {}
    for n, s in sets.items():
        eu = engine_units(s["units"]) + (engine_units(s["code"]) if run_name == "candidates" else [])
        eng_sets[n] = (eu, s["train_shas"], s["seed_shas"], s["train_path"] if run_name != "seed" else None)
    with fresh_tempdir("c2g13e_") as td:
        eng = g.run_sets(eng_sets, tgs, Path(td), cosine=g.COSINE if embed else None,
                         side=side and run_name in ("seed", "candidates"), side_parallel=side_parallel)
    # ---- OHS-4: hash exports (by program) and the two sealed-side checkers (RUN only)
    try:
        ex = exports or Exports(prereg_text=prereg_text)
        ex_rec = {"status": "verified", "sha256": ex.shas}
    except ExportError as e:
        ex, ex_rec = None, {"status": f"refused: {e}"}
        why_all.append(f"ohs4_hash: {e}")
    hash_hits, hash_rep = {}, {}
    if ex is not None:
        for n, s in sets.items():
            hash_hits[n], hash_rep[n] = ohs4_hash_hits(s["units"], ex)
    recs, back = checker_rows({n: s["units"] for n, s in sets.items()})
    rows_rec = run_checker(G13_OHS4_TOOL, "--rows", recs) if recs else {"status": "nothing to check"}
    if rows_rec["status"] not in ("scanned", "nothing to check"):
        why_all.append(f"ohs4_rows: g13_ohs4_check {rows_rec['status']}")
    tpl_sets = {n: s["units"] + s["code"] for n, s in sets.items()} if run_name == "seed" else \
        {n: s["code"] for n, s in sets.items()}
    trecs, tback = gtpl_records(tpl_sets)
    gtpl_rec = run_checker(GTPL_TOOL, "--templates", trecs) if trecs else {"status": "nothing to check"}
    if gtpl_rec["status"] not in ("scanned", "nothing to check"):
        why_all.append(f"ohs4_gtpl: gtpl_check {gtpl_rec['status']}")
    # ---- C2 method 6 (dev structure keys)
    dev_names = [] if run_name == "seed" else list(C2_DEV)
    skeys, srec = dev_struct_keys(dev_names, ilog)
    a53 = A53State(ilog) if run_name in ("candidates", "final") else None
    for n in dev_names:
        if not srec[n]["files"]:
            why_all.append(f"{n}: not built yet (no file; spec 7.1: frozen before training)")
    out, unwaived = {}, {}
    for name, s in sets.items():
        out[name] = _record(run_name, name, s, eng[name], hash_hits.get(name, {}), hash_rep.get(name, {}),
                            rows_rec, back, gtpl_rec, tback, skeys, srec, ex_rec, why_all, ilog, t0, embed, side, a53=a53,
                            guard=guard, unwaived=unwaived)
        late = guard.finalize(out[name], name)  # again just before the result is written (and returned)
        withdraw_waivers(out[name], unwaived.get(name), late)   # a change seen only now undoes the A53 waivers
        if write:
            kp.write_json(OUT / f"{name}.json", out[name], prereg_text=prereg_text)
    return out


def derive_hits(run_name: str, units: dict, hits: dict, eng: dict) -> dict:
    """What a result lists from its hits ({target: {method: {unit key: fields}}}): drop_ids (rows of every hit unit; []
    for a seed run), drop_units, quarantine (seed: the pool templates), counts_by_target_and_method. Called on the hits
    after A53 (the record) and on a copy before it (the same fields with no waiver: withdraw_waivers)."""
    hit_keys = {k for ms in hits.values() for d in ms.values() for k in d}
    counts = {tg: {m: {"units": len(d), "rows": sum(len(units[k]["rows"]) for k in d)} for m, d in sorted(ms.items())}
              for tg, ms in sorted(hits.items())}
    for lb, ms in (eng.get("counts_by_eval_and_method") or {}).items():
        for m, c in ms.items():
            if lb in counts and m in counts[lb]:
                counts[lb][m]["eval_items"] = c.get("eval_items")
    template = run_name == "seed"
    quarantine = []
    if template:
        for k in sorted(hit_keys):
            u = units[k]
            quarantine.append({"template": k, "template_id": u["template_id"], "file": u["file"], "line": u["line"],
                               "hits": {tg: sorted(m for m, d in ms.items() if k in d)
                                        for tg, ms in sorted(hits.items()) if any(k in d for d in ms.values())}})
    return {"drop_ids": [] if template else sorted({r for k in hit_keys for r in units[k]["rows"]}),
            "drop_units": 0 if template else len(hit_keys), "quarantine": quarantine,
            "counts_by_target_and_method": counts}


def withdraw_waivers(rec: dict, unwaived: dict | None, late: list[str]) -> bool:
    """An input turned out to have changed AFTER the A53 step had already waived units: put back drop_ids, drop_units,
    counts and quarantine as they are with no waiver (so drop_ids never shrink because of a changed input) and say so in
    rec["a53"]. `unwaived` = derive_hits of the hits before A53. True when a waiver was withdrawn."""
    a = rec.get("a53") or {}
    if not late or not a.get("waived_units"):
        return False
    if unwaived is None:                       # cannot happen from run(): _record always keeps it when A53 ran
        raise RuntimeError("g13_c2: waivers were applied but no unwaived record was kept")
    rec.update({k: unwaived[k] for k in ("drop_ids", "drop_units", "quarantine", "counts_by_target_and_method")})
    rec["quarantine_templates"] = len(unwaived["quarantine"])
    rec["a53"] = {"ruling": a.get("ruling", A53_RULING), "applied_to": list(a.get("applied_to") or A53_TARGETS), "blocks": {},
                  "note": "withdrawn: an input changed after the A53 step (re-run); drop_ids recomputed with no waiver",
                  "changed_inputs": list(late),
                  "withdrawn": {k: a[k] for k in ("waived_units", "waived_units_sha256", "waived_before_after") if k in a}}
    return True


def _record(run_name, name, s, eng, hh, hrep, rows_rec, back, gtpl_rec, tback, skeys, srec, ex_rec, why_all, ilog,
            t0, embed, side, a53=None, guard=None, unwaived=None) -> dict:
    units = {u["key"]: u for u in s["units"]}
    code = {u["key"]: u for u in s["code"]}
    hits = defaultdict(lambda: defaultdict(dict))          # target -> method -> {unit key: fields}

    def add(tg, m, key, fields):
        cur = hits[tg][m].setdefault(key, set())
        cur |= set(fields)

    code_hits = defaultdict(lambda: defaultdict(set))
    code_bind = set(eng.get("seed_hit_locs") or []) & set(code)          # A31 (b): rendered / unprovable literals
    code_rep = set(eng.get("seed_hit_locs_report_only") or []) & set(code)
    for lb, ms in (eng.get("hits_by_eval") or {}).items():
        for m, e in ms.items():
            for k, fs in e["u"].items():
                if k in units:
                    add(lb, m, k, fs)
            for k in e["s"]:
                if k in units:                             # a pool template: every hit binds (no A31 b exemption)
                    add(lb, m, k, ["pool"])
                elif k in code_bind:
                    code_hits[lb][m].add(k)
    for m, d in hh.items():
        for k, fs in d.items():
            add("ohs4_hash", m, k, fs)
    if rows_rec.get("status") == "scanned":
        by_m = rows_rec.get("hit_ids_by_method") or {}
        for rid in rows_rec.get("hit_ids") or []:
            if back.get(rid, (None,))[0] != name:
                continue
            ms = [m for m, ids in by_m.items() if rid in ids] or ["any"]
            for m in ms:
                add("ohs4_rows", m, back[rid][1], ["sealed"])
    if gtpl_rec.get("status") == "scanned":
        for tid in gtpl_rec.get("hit_ids") or []:
            nm, k = tback.get(tid, (None, None))
            if nm != name:
                continue
            if k in units:
                add("ohs4_gtpl", "gtpl8", k, ["template"])
            else:
                code_hits["ohs4_gtpl"]["gtpl8"].add(k)
    if skeys and any(skeys.values()):
        for m, d in dev_struct_hits(s["units"], skeys).items():
            for k, fs in d.items():
                add(C2_STRUCT, m, k, fs)
    changed = guard.check(name) if guard is not None else []         # run-input guard, at the A53 step
    if unwaived is not None and a53 is not None:                      # what no waiver would give, kept for withdraw_waivers
        unwaived[name] = derive_hits(run_name, units, {tg: {m: {k: set(v) for k, v in d.items()} for m, d in ms.items()}
                                                       for tg, ms in hits.items()}, eng)
    a53_rec = a53_apply(run_name, s, hits, a53, changed=changed)     # PREREG A53: c2_mixdev / c2_transfer_dev only
    derived = derive_hits(run_name, units, hits, eng)
    template = run_name == "seed"
    code_list = sorted({k for ms in code_hits.values() for v in ms.values() for k in v})
    why = list(eng.get("incomplete_why") or []) + list(why_all) + list(changed)
    if not embed:
        why.append("method 5 (embed) off in this run (--no-embed)")
    eng_keep = {k: v for k, v in eng.items() if k not in ("files_by_target", "drop_ids", "set", "batch")}
    rec = {
        "set": name, "run": run_name, "block": s["block"], "tool": "c2_build/g13_c2.py",
        "tool_sha256": g.sha256_file(Path(__file__)), "engine_sha256": g.sha256_file(Path(g.__file__)),
        "spec": "C2_DATA_SPEC 6.3 G13 / G-TPL, 6.4, 8.4; PREREG A37 e, A38, A53 (dev targets)",
        "unit": "template (pool record)" if template else "call_id (every row of a hit unit is listed)",
        "drop_ids": derived["drop_ids"], "drop_units": derived["drop_units"],
        "quarantine": derived["quarantine"], "quarantine_templates": len(derived["quarantine"]),
        "units": len(units), "rows": sum(len(u["rows"]) for u in units.values()),
        "code_seed_literals": len(code),
        "code_seed_hits": code_list,
        "code_seed_hits_report_only": sorted(code_rep),
        "code_seed_rule": "program literals: decontam_g13 A31 (b) for the old targets (binding only when rendered, "
                          "then the rows drop too); G-TPL hits bind: reword the literal and run again",
        "counts_by_target_and_method": derived["counts_by_target_and_method"],
        "a53": a53_rec,
        "report_only": {"ohs4_hash_short_exact": hrep,
                        "engine_seed_hits_report_only": eng.get("seed_hits_report_only"),
                        "code_seed_hits_by_target": {tg: {m: len(v) for m, v in ms.items()}
                                                     for tg, ms in code_hits.items()}},
        "ohs4": {"exports": ex_rec, "rows_checker": _strip_ids(rows_rec), "gtpl_checker": _strip_ids(gtpl_rec)},
        "c2_dev_targets": {"structure": srec, "engine": {n: (eng.get("targets") or {}).get(n) for n in C2_DEV}},
        "engine": eng_keep,
        "inputs": ilog.entries,
        "inputs_at_start": guard.inputs_at_start(name) if guard is not None else {},
        "inputs_at_start_paths": guard.paths_at_start(name) if guard is not None else {},
        "complete": not why, "incomplete_why": why,
        "wall_s": round(time.time() - t0, 1),
    }
    return rec


def _strip_ids(r: dict) -> dict:
    """A checker record without its id lists (they are folded into drop_ids / quarantine)."""
    return {k: v for k, v in r.items() if k not in ("hit_ids", "hit_ids_by_method")}


# ================================================================================ CLI
def default_blocks(run_name: str) -> list[str]:
    if run_name == "seed":
        fams = sorted(n for n in (os.listdir(HERE / "families") if (HERE / "families").is_dir() else [])
                      if not c2io.refusal(HERE / "families" / n)         # a refused family folder is never stat-ed
                      and any((HERE / "families" / n / sub).is_dir() for sub in ("pools", "pools_v2")))
        return fams + [b for b, d in FAMILY_DIRS.items() if (d / "pools").is_dir() or (d / "pools_v2").is_dir()]
    if run_name == "candidates":
        return [b for b in c2io.ALL_TARGETS if b not in c2io.CARRY]   # W6: + T40-T45, GB, GW, MD, RTW (a block with no candidates on disk is skipped)
    if run_name == "carry":
        return list(c2io.CARRY)
    return []


def targets_report() -> dict:
    out = {"old": {}, "new": {}}
    for tg in g.targets():
        fs = [p for s in tg["paths"] for p in g.resolve(s)]
        out["old"][tg["name"]] = tg["status"] or (f"{sum(map(g.allowed, fs))} files" if tg["kind"] not in
                                                  ("sealed_side", "sealed_check") else "child process")
    for n in C2_DEV:
        out["new"][n] = f"{len(dev_files(n))} files"
    out["new"]["ohs4_hash"] = "c2_build/sealed_hashes (verified at run time)"
    out["new"]["ohs4_rows"] = "g13_ohs4_check.py (run only)"
    out["new"]["ohs4_gtpl"] = "gtpl_check.py (run only; templates)"
    return out


PRE_GUARD = "pre-guard log: re-run"
_RUN_OF_PREFIX = (("c2_seed_", "seed"), ("c2_cand_", "candidates"), ("c2_carry_", "carry"), ("c2_final", "final"))


def log_run(d: dict, stem: str = "") -> str | None:
    """The run a log came from: its "run" key, else the set-name prefix (c2_cand_<block> ...)."""
    if d.get("run"):
        return str(d["run"])
    name = str(d.get("set") or stem)
    return next((r for pre, r in _RUN_OF_PREFIX if name.startswith(pre)), None)


def inputs_at_start_problems(d: dict, name: str, run: str | None) -> list[str]:
    """Log check (a) a candidates / carry / final log with no inputs_at_start is a pre-guard log; (b) every
    inputs_at_start dev / training / pool / program-literal file must still have its start sha256 ("changed after the
    run"; a file gone since is also a change); (c) the dev files that exist now (the c2_mixdev target is a glob) must all be
    in inputs_at_start: one that appeared after the run is "changed after the run (appeared after the run ...)", unless the
    log is a seed log (it never reads them). The two code files are not compared. A file is found through the log's
    inputs_at_start_paths; an older record (names only) through its path key, its engine input paths and the dev files
    that exist now. A name that cannot be located is a problem (gone / re-run), never skipped."""
    ias = d.get("inputs_at_start")
    if not isinstance(ias, dict) or not ias:
        # candidates / carry / final (or a run that cannot be told): the dev files are not pinned by anything else. A seed
        # log never reads them; its pool / literal files are pinned by engine.inputs_sha256 (log_problems below).
        return [f"{name}: {PRE_GUARD} (no inputs_at_start)"] if run != "seed" else []
    paths = d.get("inputs_at_start_paths") if isinstance(d.get("inputs_at_start_paths"), dict) else {}
    eng = (d.get("engine") or {}).get("inputs_sha256") or {}
    known: dict = defaultdict(set)                                    # basename -> lean-relative or absolute paths
    for rel in [*(eng.get("train") or {}), *(eng.get("seeds") or {})]:
        known[Path(rel).name].add(str(rel))
    for nm in C2_DEV:
        for q in dev_files(nm):
            known[q.name].add(lean_rel(q))
    out = []
    for key, sha in sorted(ias.items()):
        if key in CODE_GUARD:
            continue
        rel = paths.get(key) or (key if "/" in key else None)
        if rel is None:
            cands = known.get(key) or set()
            if not cands:
                out.append(f"{name}: input {key} changed after the run (gone: no such file now)")
                continue
            if len(cands) > 1:
                out.append(f"{name}: input {key} cannot be located ({len(cands)} files share the name): re-run")
                continue
            rel = next(iter(cands))
        q = Path(rel) if Path(rel).is_absolute() else LEAN / rel
        if c2io.refusal(q):
            out.append(f"{name}: input {key} is on the never-open list: re-run")
        elif not q.is_file():
            out.append(f"{name}: input {key} changed after the run (gone)")
        elif g.sha256_file(q) != sha:
            out.append(f"{name}: input {key} changed after the run")
    if run != "seed":                                                 # (c) a dev file that appeared after the run
        placed = {paths.get(k) or (k if "/" in k else None) for k in ias} - {None}
        loose = {k for k in ias if not (paths.get(k) or "/" in k)}    # names without a path (an ambiguous one is reported above)
        cur = sorted({q for nm in C2_DEV for q in dev_files(nm)})
        count = Counter(q.name for q in cur)
        for q in cur:
            if lean_rel(q) not in placed and q.name not in loose:
                out.append(f"{name}: input {lean_rel(q) if count[q.name] > 1 else q.name} changed after the run "
                           f"(appeared after the run: not in inputs_at_start)")
    return out


def log_problems(paths: list[Path] | None = None) -> list[str]:
    """Preflight on written logs: complete, a candidates / carry / final log written by the guarded code (inputs_at_start),
    every start input (dev, training, pool, program-literal files) unchanged since, the exports pinned."""
    out = []
    for f in paths if paths is not None else sorted(OUT.glob("c2_*.json")):
        if c2io.refusal(f):                                           # the never-open rule before the log is opened
            out.append(f"{Path(f).name}: log is on the never-open list: re-run")
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        name = d.get("set", f.stem)
        if not d.get("complete"):
            out.append(f"{name}: incomplete ({len(d.get('incomplete_why') or [])} reasons)")
        out += inputs_at_start_problems(d, name, log_run(d, f.stem))
        shas = {**(d.get("engine", {}).get("inputs_sha256", {}).get("train") or {}),
                **(d.get("engine", {}).get("inputs_sha256", {}).get("seeds") or {})}
        for rel, sha in shas.items():
            q = Path(rel) if Path(rel).is_absolute() else LEAN / rel
            if c2io.refusal(q):                                       # the never-open rule BEFORE any stat or hash
                out.append(f"{name}: input {rel} is on the never-open list: re-run")
            elif not q.exists():
                out.append(f"{name}: input {rel} is gone")
            elif g.sha256_file(q) != sha:
                out.append(f"{name}: input {rel} changed after the G13 run")
        if (d.get("ohs4", {}).get("exports", {}).get("sha256") or {}).get("manifest") != SEALED_HASHES_MANIFEST_SHA256:
            out.append(f"{name}: not run against the pinned OHS-4 hash exports")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="C2 G13 decontamination wrapper (counts and C2 ids only)")
    ap.add_argument("run", choices=RUNS + ("targets", "status"))
    ap.add_argument("--block", nargs="*", default=None)
    ap.add_argument("--no-embed", action="store_true")
    ap.add_argument("--no-side", action="store_true")
    ap.add_argument("--side-serial", action="store_true")
    ap.add_argument("--dry", action="store_true", help="build the training side only (nothing read or written)")
    a = ap.parse_args(argv)
    if a.run == "targets":
        print(json.dumps(targets_report(), indent=1))
        return 0
    if a.run == "status":
        p = log_problems()
        print("\n".join(p) or "C2 G13 logs OK")
        return 1 if p else 0
    blocks = a.block if a.block is not None else default_blocks(a.run)
    if a.dry:
        sets = build_sets(a.run, blocks, c2io.C2InputLog())
        if not sets:
            print(f"g13_c2 {a.run} --dry: nothing on disk yet for {blocks or 'any block'}")
        for n, s in sets.items():
            print(f"{n}: units {len(s['units'])} rows {sum(len(u['rows']) for u in s['units'])} "
                  f"texts {sum(len(u['texts']) for u in s['units'])} code literals {len(s['code'])}")
        return 0
    recs = run(a.run, blocks, embed=not a.no_embed, side=not a.no_side, side_parallel=not a.side_serial)
    for n, r in recs.items():
        what = f"quarantine {r['quarantine_templates']} templates" if r["run"] == "seed" else \
            f"drop units {r['drop_units']} rows {len(r['drop_ids'])}"
        print(f"G13-C2 {n}: units {r['units']} rows {r['rows']} | {what} | code literal hits "
              f"{len(r['code_seed_hits'])} | complete {r['complete']} ({len(r['incomplete_why'])} reasons)")
        for tg, ms in r["counts_by_target_and_method"].items():
            print(f"  {tg}: " + ", ".join(f"{m} {c['units']}u" for m, c in ms.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
