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
  ../.venv/bin/python c2_build/g13_c2.py status                     every written C2 log: complete, inputs unchanged,
                                                                    pinned exports (exit 1 on a problem)
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
"ohs4" (export and checker records), "complete", "incomplete_why", ...}. mix_c2 --decontam-drops and c2_select
--exclude-ids read "drop_ids".
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
import unicodedata
from collections import defaultdict
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


def dev_files(name: str) -> list[Path]:
    """The existing files of one C2 dev target (main files only, never their companions)."""
    out = []
    for spec in C2_DEV[name]["paths"]:
        out += [p for p in g.resolve(spec) if p.name.count(".") == 1 and not c2io.refusal(p)]
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


def pool_units(block: str, root: Path, ilog) -> tuple[list[dict], dict]:
    """One TEMPLATE unit per pool record under <block dir>/pools/ (manifests, reports and checks skipped)."""
    units, shas = [], {}
    if not root.is_dir():
        return units, shas
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix not in POOL_EXT or g.SEED_SKIP.search(p.name) or "__pycache__" in p.parts:
            continue
        if c2io.refusal(p):
            raise c2io.C2Refused(f"pool file refused: {p}")
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
        if not p.is_file() or c2io.refusal(p):
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


def run_checker(tool: Path, flag: str, records: list[dict], extra: list | None = None, py: str = sys.executable,
                timeout: int = CHECKER_TIMEOUT) -> dict:
    """Run one sealed-side checker on `records` (written to the system temp folder, never inside the sealed folder);
    read back only its result JSON. The tool file itself is never opened, listed or hashed here."""
    with tempfile.TemporaryDirectory(prefix="c2g13_") as td:
        if c2io.refusal(Path(td)):
            raise CheckerError("the temp folder is on the never-open list")
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


def a53_pack_id(m: dict):
    v = m.get("domain_pack")
    return None if not isinstance(v, str) or A53_DOMAIN_LABEL.match(v) else v


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
            if not p.is_file() or c2io.refusal(p):
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
            if rows is None:
                f = c2io.fam_files(block)["cand"] if block in c2io.ALL_TARGETS else None
                rows = self.ilog.jsonl(f) if f is not None and f.exists() else []
            self.ctx[block] = A53Context(block, rows, root) if rows and (root / "plugin.py").is_file() else None
        return self.ctx[block]


def a53_apply(run_name: str, s: dict, hits: dict, st: A53State | None) -> dict:
    """Apply A53 to `hits` (target -> method -> {unit key: fields}) in place; return the record for the log."""
    rec = {"ruling": A53_RULING, "applied_to": list(A53_TARGETS), "blocks": {}}
    if st is None or run_name not in ("candidates", "final"):
        rec["note"] = "not applied (no state or not a candidates / final run)"
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


# ================================================================================ the run
def load_rows(path: Path, ilog) -> list[dict]:
    return ilog.jsonl(path)


def build_sets(run: str, blocks: list[str], ilog) -> dict:
    """{set name: {"units" (pool templates or row units), "code" (program literal units), "train_shas", "seed_shas",
    "train_path", "block"}}. Blocks without pools / candidates are skipped."""
    sets = {}
    for b in blocks:
        c2io.check_name(b, "block")
        if run == "seed":
            # the CURRENT frozen pool: pools_v2/ (freeze-v2 merge of v1 + redo rounds) when a family has one, else pools/
            pdir = block_dir(b) / "pools_v2" if (block_dir(b) / "pools_v2").is_dir() else block_dir(b) / "pools"
            units, shas = pool_units(b, pdir, ilog)
            if not units:
                continue
            code, cshas = code_seed_units(b, block_dir(b))
            sets[f"c2_seed_{b}"] = {"units": units, "code": code, "train_shas": {}, "seed_shas": {**shas, **cshas},
                                    "train_path": None, "block": b}
        elif run in ("candidates", "carry"):
            f = c2io.fam_files(b)["cand"]
            if not f.exists():
                continue
            units = row_units(load_rows(f, ilog))
            code, cshas = code_seed_units(b, block_dir(b)) if run == "candidates" else ([], {})
            sets[f"c2_{'cand' if run == 'candidates' else 'carry'}_{b}"] = {
                "units": units, "code": code, "train_shas": {lean_rel(f): g.sha256_file(f)},
                "seed_shas": cshas, "train_path": f, "block": b}
    if run == "final":
        f = c2io.C2_PARTS / "c2_train.jsonl"
        if f.exists():
            units = row_units(load_rows(f, ilog))
            sets["c2_final"] = {"units": units, "code": [], "train_shas": {lean_rel(f): g.sha256_file(f)},
                                "seed_shas": {}, "train_path": f, "block": "final"}
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
    tgs = engine_targets(run_name) if tgs is None else tgs
    why_all: list = []
    # ---- old targets + C2 dev targets: decontam_g13 (one eval pass for every set)
    eng_sets = {}
    for n, s in sets.items():
        eu = engine_units(s["units"]) + (engine_units(s["code"]) if run_name == "candidates" else [])
        eng_sets[n] = (eu, s["train_shas"], s["seed_shas"], s["train_path"] if run_name != "seed" else None)
    with tempfile.TemporaryDirectory(prefix="c2g13e_") as td:
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
    out = {}
    for name, s in sets.items():
        out[name] = _record(run_name, name, s, eng[name], hash_hits.get(name, {}), hash_rep.get(name, {}),
                            rows_rec, back, gtpl_rec, tback, skeys, srec, ex_rec, why_all, ilog, t0, embed, side, a53=a53)
        if write:
            kp.write_json(OUT / f"{name}.json", out[name], prereg_text=prereg_text)
    return out


def _record(run_name, name, s, eng, hh, hrep, rows_rec, back, gtpl_rec, tback, skeys, srec, ex_rec, why_all, ilog,
            t0, embed, side, a53=None) -> dict:
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
    a53_rec = a53_apply(run_name, s, hits, a53)                      # PREREG A53: c2_mixdev / c2_transfer_dev only
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
    drop_ids = [] if template else sorted({r for k in hit_keys for r in units[k]["rows"]})
    code_list = sorted({k for ms in code_hits.values() for v in ms.values() for k in v})
    why = list(eng.get("incomplete_why") or []) + list(why_all)
    if not embed:
        why.append("method 5 (embed) off in this run (--no-embed)")
    eng_keep = {k: v for k, v in eng.items() if k not in ("files_by_target", "drop_ids", "set", "batch")}
    rec = {
        "set": name, "run": run_name, "block": s["block"], "tool": "c2_build/g13_c2.py",
        "tool_sha256": g.sha256_file(Path(__file__)), "engine_sha256": g.sha256_file(Path(g.__file__)),
        "spec": "C2_DATA_SPEC 6.3 G13 / G-TPL, 6.4, 8.4; PREREG A37 e, A38, A53 (dev targets)",
        "unit": "template (pool record)" if template else "call_id (every row of a hit unit is listed)",
        "drop_ids": drop_ids, "drop_units": 0 if template else len(hit_keys),
        "quarantine": quarantine, "quarantine_templates": len(quarantine),
        "units": len(units), "rows": sum(len(u["rows"]) for u in units.values()),
        "code_seed_literals": len(code),
        "code_seed_hits": code_list,
        "code_seed_hits_report_only": sorted(code_rep),
        "code_seed_rule": "program literals: decontam_g13 A31 (b) for the old targets (binding only when rendered, "
                          "then the rows drop too); G-TPL hits bind: reword the literal and run again",
        "counts_by_target_and_method": counts,
        "a53": a53_rec,
        "report_only": {"ohs4_hash_short_exact": hrep,
                        "engine_seed_hits_report_only": eng.get("seed_hits_report_only"),
                        "code_seed_hits_by_target": {tg: {m: len(v) for m, v in ms.items()}
                                                     for tg, ms in code_hits.items()}},
        "ohs4": {"exports": ex_rec, "rows_checker": _strip_ids(rows_rec), "gtpl_checker": _strip_ids(gtpl_rec)},
        "c2_dev_targets": {"structure": srec, "engine": {n: (eng.get("targets") or {}).get(n) for n in C2_DEV}},
        "engine": eng_keep,
        "inputs": ilog.entries,
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
        fams = sorted({p.parent.name for g in ("*/pools", "*/pools_v2") for p in (HERE / "families").glob(g) if p.is_dir()})
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


def log_problems(paths: list[Path] | None = None) -> list[str]:
    """Preflight on written logs: complete, the training / pool files unchanged since, the exports pinned."""
    out = []
    for f in paths if paths is not None else sorted(OUT.glob("c2_*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        name = d.get("set", f.stem)
        if not d.get("complete"):
            out.append(f"{name}: incomplete ({len(d.get('incomplete_why') or [])} reasons)")
        shas = {**(d.get("engine", {}).get("inputs_sha256", {}).get("train") or {}),
                **(d.get("engine", {}).get("inputs_sha256", {}).get("seeds") or {})}
        for rel, sha in shas.items():
            q = Path(rel) if Path(rel).is_absolute() else LEAN / rel
            if not q.exists():
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
