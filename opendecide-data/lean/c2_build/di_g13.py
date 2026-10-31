"""di_g13.py: the A61 (e) leak-check targets of the Decision Index for g13_c2.py (draft ruling c2_build/zed_orch/di_train/A61_DRAFT.md).
CPU only, no network. Pure functions plus two file readers (the pins and the hashed exports under c2_build/g13_di/); it never opens,
lists or stats a bench/external_quarantine/ path (g13_c2's never-open rule), and no DI item text is ever printed, kept or logged.

Two engine targets (decontam_g13.target dicts, scanned by decontam_g13.run_sets with the same methods as di_test):
  di03_public    the DI 0.3 public suite (edition release-v3 of the kit github.com/apolinario/decision-index): selected-rows.jsonl.gz and
                 added-rows.jsonl.gz (release-v2 cut + the 7 added benchmarks, the 0.2 GSM8K rows and ForecastBench included: a superset of what
                 0.3 scores) and gsm8k-rows.jsonl.gz (the 0.3 GSM8K rows), rebuilt locally with the kit (the suite is not redistributed) in
                 bench/external_quarantine/decision_index_03/ and registered in the engine's QUARANTINE_OK (patch_engine). Fields read: state and
                 questions (every instruction, criterion and option string). `di_test` (the release-v1 rebuild) is a different, older target and
                 stays as it is.
  di_src_splits  the FULL DI-scored split of each benchmark that feeds a DI block (GSM8K test 1,319, HoVer dev 4,000, iSarcasmEval test, all
                 tracks), fetched upstream at the suite.md pins into bench/external_quarantine/decision_index_03/src_splits/.
Three program methods on top of the engine's (exact full / segment / short, substring, 10- and 12-gram, tulu8, minhash, embed), from hashed exports in
c2_build/g13_di/ made by g13_di/di_register.py (the only program that reads the DI files, outside this module):
  record_id  (di_src_splits)  a GSM8K question / HoVer claim / iSarcasm tweet text hash of a unit's text, a segment or a line of >= 5 words, or a HoVer
                              uid / hpqa_id (origin-claim group) in a row's meta.
  wording8   (di03_public)    an instruction / definition (card) / option text of a unit shares one word 8-gram with any DI request instruction or
                              criterion string (A61 c 5: "no DI wording").
  structure  (di03_public)    the unit's decontam_g13.struct_g13 key (state + options) is a DI request question's.
A hit drops the whole unit (call_id), exactly as every other method. No waiver applies (A53 is for the C2 dev targets only).

Readiness (A61 e 6). g13_c2 includes these targets in a run when the run holds a DI block, or a final run that has DI rows or whose targets are complete;
a core-only run without them still runs against every other target. A target with a coverage gap makes the log incomplete: the HLE gap ("HLE not
scanned (gated)", the 513 gated requests) is accepted only when PREREG_FINAL.md's 'Ruling A61' block carries the tag A61-HLE; any other gap, or a pin
record that is not complete, keeps the log incomplete, and mix_c2 then keeps every DI block out of the mix.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent                      # lean/c2_build
sys.path.insert(0, str(HERE))
import c2io  # noqa: E402  (puts c_build on sys.path)
import decontam_g13 as g  # noqa: E402  (c_build: imported read-only)

DI_DIR = HERE / "g13_di"                                    # pins and hashed exports: no item text, outside the quarantine
PINS = DI_DIR / "di_pins.json"
EXPORT_MANIFEST = DI_DIR / "MANIFEST.json"
NEVER_TRAIN = DI_DIR / "di_never_train.json"

QROOT = "bench/external_quarantine/decision_index_03"       # repo-relative; read by the engine only
_SUITE = QROOT + "/work/artifacts/benchmark-suite"
DI03_FILES = (_SUITE + "/release-v2-rebuilt/selected-rows.jsonl.gz", _SUITE + "/release-v2-rebuilt/added-rows.jsonl.gz",
              _SUITE + "/release-v3-rebuilt/gsm8k-rows.jsonl.gz")
_SRC = QROOT + "/src_splits"
SRC_FILES = (_SRC + "/gsm8k_test.jsonl", _SRC + "/hover_dev.jsonl", _SRC + "/isarcasmeval_test.jsonl")
QUARANTINE_OK = DI03_FILES + SRC_FILES                      # added to decontam_g13.QUARANTINE_OK by patch_engine
TARGETS = ("di03_public", "di_src_splits")
FILES = {"di03_public": DI03_FILES, "di_src_splits": SRC_FILES}
FIELDS = {"di03_public": ("state", "questions"), "di_src_splits": None}
PROGRAM_METHODS = {"di03_public": ("wording8", "structure"), "di_src_splits": ("record_id",)}
NOTES = {"di03_public": "A61 e 2: the DI 0.3 public suite (kit release-v3), rebuilt locally; state + questions (instructions, criteria, options)",
         "di_src_splits": "A61 e 3: the full DI-scored splits of GSM8K (test), HoVer (dev) and iSarcasmEval (test, all tracks), fetched at the suite.md pins"}
HLE_GAP = "HLE not scanned (gated)"
HLE_TAG = "A61-HLE"
WORDING_FIELDS = ("instructions", "card", "option")         # A61 c 5: instruction and definition text (and option text) of a training unit
MIN_WORDS = 5
GRAM = 8
ID_META_KEYS = ("uid", "hover_uid", "hpqa_id", "origin_claim", "origin_group", "origin_claim_group", "source_record_id", "record_id")
_SEG = re.compile(r"(?<=[.!?])\s+|\n+")


class DiError(RuntimeError):
    """The DI pins or exports are missing, inconsistent or not the files they were derived from."""


# ---- text helpers (the same normalisation as decontam_g13 / g13_c2) ---------------------------------------------------
def words(t: str) -> list[str]:
    return g.words(t)


def norm(t: str) -> str:
    return " ".join(words(t))


def sha_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def gram_u64(ws: list[str], n: int = GRAM) -> list[int]:
    """The first 8 bytes (big endian) of the sha256 of every word n-gram, as ints."""
    return [int.from_bytes(hashlib.sha256(" ".join(ws[i:i + n]).encode()).digest()[:8], "big") for i in range(len(ws) - n + 1)]


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


# ---- what a DI request contributes (used by the register program; here so the two sides agree) ------------------------
def request_wording(row: dict):
    """Every instruction and criterion string of one DI request (questions[*].instructions, questions[*].criteria values)."""
    for q in (row.get("questions") or {}).values():
        if isinstance(q, dict):
            yield from _strings(q.get("instructions"))
            yield from _strings(q.get("criteria"))


def request_structs(row: dict) -> set:
    """decontam_g13.struct_g13 keys of one DI request: its state (a JSON object as sorted-key JSON) with each question's criteria values as
    the options."""
    st = row.get("state")
    if isinstance(st, (dict, list)):
        st = json.dumps(st, ensure_ascii=False, sort_keys=True)
    out = set()
    for q in (row.get("questions") or {}).values():
        crit = q.get("criteria") if isinstance(q, dict) else None
        opts = [v for v in crit.values() if isinstance(v, str)] if isinstance(crit, dict) else None
        k = g.struct_g13(st, opts)
        if k:
            out.add(k)
    return out


# ---- pins ----------------------------------------------------------------------------------------------------------------
def load_pins(path: Path | None = None) -> dict:
    """c2_build/g13_di/di_pins.json ({} when it is not written yet). Written by g13_di/di_register.py finalize."""
    p = Path(path) if path else PINS
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def a61_block(prereg_text: str) -> str:
    """The text of the 'Ruling A61' block (its quoted lines) in PREREG_FINAL.md, or ''."""
    out, inside = [], False
    for ln in prereg_text.splitlines():
        if re.match(r"^>\s*\*\*Ruling A61\b", ln):
            inside = True
        elif inside and not ln.startswith(">"):
            break
        if inside:
            out.append(ln)
    return "\n".join(out)


def hle_accepted(prereg_text: str | None = None) -> bool:
    """The HLE coverage gap is accepted only under ruling tag A61-HLE: PREREG_FINAL.md must hold a 'Ruling A61' block that carries the tag."""
    if prereg_text is None:
        try:
            prereg_text = c2io.PREREG.read_text(encoding="utf-8")
        except OSError:
            return False
    return HLE_TAG in a61_block(prereg_text)


def gap_for(name: str, pins: dict | None = None, prereg_text: str | None = None) -> str | None:
    """Why target `name` is incomplete (None = complete). The pin record must exist, say complete true and carry no gap but HLE's; HLE's gap
    needs the ruling tag."""
    pins = load_pins() if pins is None else pins
    p = pins.get(name)
    if not isinstance(p, dict):
        return f"{name}: not built or fetched yet (no record in g13_di/di_pins.json): the target is incomplete (A61 e 6)"
    gaps = [str(x) for x in p.get("gaps") or []]
    other = [x for x in gaps if x != HLE_GAP]
    if p.get("complete") is not True or other:
        return f"{name}: incomplete ({'; '.join(other) or 'complete is not true'}) (A61 e 2, e 3)"
    if HLE_GAP in gaps and not hle_accepted(prereg_text):
        return f"{name}: {HLE_GAP}: accepted only under ruling tag {HLE_TAG} in PREREG_FINAL.md (A61 e 2), which is not there"
    return None


def complete(pins: dict | None = None, prereg_text: str | None = None) -> bool:
    pins = load_pins() if pins is None else pins
    return all(gap_for(n, pins, prereg_text) is None for n in TARGETS)


def pinned_files(pins: dict) -> dict:
    """{repo-relative DI file path: sha256} of every file the pin records list."""
    out = {}
    for n in TARGETS:
        for f, d in ((pins.get(n) or {}).get("files") or {}).items():
            out[f] = (d or {}).get("sha256")
    return out


# ---- the engine side ---------------------------------------------------------------------------------------------------
def patch_engine() -> None:
    """Add the DI files to decontam_g13.QUARANTINE_OK (the engine's allow-list reads the module global at call time). The engine file itself is
    not edited. Idempotent."""
    g.QUARANTINE_OK = tuple(g.QUARANTINE_OK) + tuple(p for p in QUARANTINE_OK if p not in g.QUARANTINE_OK)


def targets(pins: dict | None = None, prereg_text: str | None = None) -> list[dict]:
    """The two engine target dicts (blind: counts only). `gap` carries the coverage gap that keeps a log incomplete. Same dict as g.target."""
    pins = load_pins() if pins is None else pins
    return [g.target(n, ["repo:" + p for p in FILES[n]], kind="generic", fields=FIELDS[n], blind=True, note=NOTES[n],
                     gap=gap_for(n, pins, prereg_text)) for n in TARGETS]


def has_di_rows(units: list[dict]) -> bool:
    """True when a unit's row is a DI block's (meta.family)."""
    for u in units:
        for r in u.get("rows_src", ()) or ():
            m = r.get("meta") if isinstance(r.get("meta"), dict) else {}
            if m.get("family") in c2io.DI_BLOCKS:
                return True
    return False


def needs_di(run_name: str, sets: dict, pins: dict | None = None, prereg_text: str | None = None) -> bool:
    """A61 (e 5, e 6): the DI targets join a run when it holds a DI block (seed / candidates / final), or when it is a final run and the targets
    are complete (every block meets them) or the mix has DI rows (then an incomplete target keeps the log incomplete). A core-only run without a
    complete target runs against every other target as before."""
    if any(s.get("block") in c2io.DI_BLOCKS for s in sets.values()):
        return True
    if run_name != "final":
        return False
    pins = load_pins() if pins is None else pins
    if complete(pins, prereg_text):
        return True
    return any(has_di_rows(s["units"]) for s in sets.values())


def verify_scanned(eval_shas: dict, pins: dict, names=TARGETS, require: bool = False) -> list[str]:
    """Problems between what the engine scanned (its inputs_sha256.eval: repo-relative file -> sha256) and the pinned files of `names`: a scanned
    file that is not the pinned one; with require, also a pinned file the engine did not scan."""
    out = []
    pin = pinned_files({n: pins.get(n) for n in names} if pins else {})
    for n in names:
        for f in FILES[n]:
            want = pin.get(f)
            got = (eval_shas or {}).get(f)
            if want and got and want != got:
                out.append(f"{n}: the scanned file {Path(f).name} is not the pinned one (sha256 {str(got)[:12]} vs pinned {str(want)[:12]})")
            elif want and not got and require:
                out.append(f"{n}: the pinned file {Path(f).name} was not scanned")
    return out


# ---- the program side: hashed exports -----------------------------------------------------------------------------------
class DiExports:
    """c2_build/g13_di/ exports (MANIFEST.json, wording8_u64.npy, structure_g13.json, record_ids.json), checked against their manifest and against
    the DI files' pinned sha256 they were derived from. Membership tests only; nothing here is printed."""

    FILES = ("wording8_u64.npy", "structure_g13.json", "record_ids.json")

    def __init__(self, root: Path | None = None, pins: dict | None = None):
        root = Path(root) if root else DI_DIR
        try:
            man = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            raise DiError(f"g13_di/MANIFEST.json is not readable ({type(e).__name__}): run g13_di/di_register.py export") from None
        for name in self.FILES:
            d = (man.get("files") or {}).get(name)
            f = root / name
            if not isinstance(d, dict) or not f.is_file() or g.sha256_file(f) != d.get("sha256"):
                raise DiError(f"g13_di/{name} is missing or differs from MANIFEST.json")
        pins = load_pins() if pins is None else pins
        derived, pinned = man.get("derived_from") or {}, pinned_files(pins)
        if not derived or any(pinned.get(f) != s for f, s in derived.items()):
            raise DiError("the DI exports were derived from other DI files than the pinned ones (g13_di/di_pins.json): export again")
        self.shas = {"manifest": g.sha256_file(root / "MANIFEST.json"), **{n: d["sha256"] for n, d in man["files"].items()}}
        a = np.load(root / "wording8_u64.npy")
        if a.dtype != np.uint64 or a.ndim != 1 or (len(a) > 1 and not np.all(a[1:] > a[:-1])):
            raise DiError("wording8_u64.npy is not a sorted unique uint64 array")
        self.wording8 = a
        self.struct = set(json.loads((root / "structure_g13.json").read_text(encoding="utf-8")))
        ids = json.loads((root / "record_ids.json").read_text(encoding="utf-8"))
        self.ids = {k: set(map(str, v)) for k, v in ids.items()}
        for k in ("gsm8k_question_sha256", "hover_claim_sha256", "hover_uid", "hover_group", "isarcasm_text_sha256"):
            if k not in self.ids:
                raise DiError(f"record_ids.json has no {k}")
        for k, n in (man.get("counts") or {}).items():
            have = len(self.wording8) if k == "wording8" else len(self.struct) if k == "structure_g13" else len(self.ids.get(k, ()))
            if have != n:
                raise DiError(f"export {k}: {have} entries, MANIFEST.json says {n}")

    def has_grams(self, hashes) -> bool:
        if not len(hashes) or not len(self.wording8):
            return False
        q = np.array(sorted(set(hashes)), np.uint64)
        pos = np.searchsorted(self.wording8, q)
        pos[pos >= len(self.wording8)] = len(self.wording8) - 1
        return bool(np.any(self.wording8[pos] == q))


def _text_hash_hit(ex: DiExports, t: str) -> bool:
    """record_id: the normalised text, or one of its segments / lines of >= MIN_WORDS words, is a GSM8K question, HoVer claim or iSarcasm tweet."""
    pools = (ex.ids["gsm8k_question_sha256"], ex.ids["hover_claim_sha256"], ex.ids["isarcasm_text_sha256"])
    cands = [norm(t)] + [norm(s) for s in _SEG.split(t)]
    for c in cands:
        if len(c.split()) >= MIN_WORDS and any(sha_hex(c) in p for p in pools):
            return True
    return False


def di_hits(units: list[dict], ex: DiExports) -> tuple[dict, dict]:
    """({target: {method: {unit key: fields}}}, counts). Row units carry their rows (rows_src), the texts (state / instructions / card / option)
    and the method-6 keys (s_g13)."""
    hits = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
    cache_rid, cache_w8 = {}, {}
    rep = defaultdict(int)
    for u in units:
        key = u["key"]
        for field, t in u.get("texts", ()):
            if t not in cache_rid:
                cache_rid[t] = _text_hash_hit(ex, t)
            if cache_rid[t]:
                hits["di_src_splits"]["record_id"][key].add(field)
            if field in WORDING_FIELDS or u.get("template"):          # a pool template IS an instruction / definition wording
                if t not in cache_w8:
                    cache_w8[t] = ex.has_grams(gram_u64(words(t)))
                if cache_w8[t]:
                    hits["di03_public"]["wording8"][key].add(field)
        for r in u.get("rows_src", ()) or ():
            m = r.get("meta") if isinstance(r.get("meta"), dict) else {}
            for k in ID_META_KEYS:
                v = m.get(k, r.get(k))
                if v not in (None, "") and (str(v) in ex.ids["hover_uid"] or str(v) in ex.ids["hover_group"]):
                    hits["di_src_splits"]["record_id"][key].add("meta." + k)
        if u.get("s_g13") and set(u["s_g13"]) & ex.struct:
            hits["di03_public"]["structure"][key].add("state+options")
    for t, ms in hits.items():
        for m_, d in ms.items():
            rep[f"{t}.{m_}"] = len(d)
    return {t: {m_: {k: set(v) for k, v in d.items()} for m_, d in ms.items()} for t, ms in hits.items()}, dict(rep)
