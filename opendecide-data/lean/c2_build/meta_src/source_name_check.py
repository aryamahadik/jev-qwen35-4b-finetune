#!/usr/bin/env python3
"""A42-D 8.5 / 12.2 sealed-side source-name check, C2 side. Prints ONLY "<id> PASS" or "<id> HIT" per source (A61 f).
Never prints which keyword or which hash matched. CPU only, no network.

A61 (f) fixes (PREREG_FINAL.md, Ruling A61; the pre-fix tool is c2_build/_backup_a61_adopt/meta_src/source_name_check.py, sha256 72fe203a...):
  FOLD. Entries with id <id> or <id>#... (and duplicate ids) fold into the source <id>; the source is a HIT if any of its entries hits; one
        output line per source ("PASS or HIT per source only", A42-D 8.5). The fold can turn a PASS into a HIT, never the reverse.
  EXPORT INTEGRITY under --exports all (default). The tool requires and verifies, before it reads the input file or prints any verdict:
        OHS-4            sealed_hashes/MANIFEST.json sha256 = OHS4_MANIFEST_SHA256 (g13_c2's SEALED_HASHES_MANIFEST_SHA256), naming the
                         A38 freeze OHS4_FREEZE_SHA256; the keyword file against the MANIFEST;
        OHS-AC final     sealed_hashes_ac/MANIFEST.json sha256 = OHSAC_FINAL_MANIFEST_SHA256 (fadec66f...); the keyword file against it;
        OHS-AC freeze    sealed_hashes_ac_union/RECORD.json (A64 h union record) names the freeze export MANIFEST OHSAC_FREEZE_MANIFEST_SHA256
                         (27808b0c...) exactly; status union_built (the union keyword file, verified against the record's sha256) or
                         freeze_subset_of_final with every count 0 (then the freeze keyword hashes are those of the final export itself).
        A missing or mismatching export prints only "<export> missing" or "<export> MISMATCH" (export = "OHS-4 export", "OHS-AC final
        export", "OHS-AC freeze export"), no verdict, exit 2. Every other exception is caught: nothing is printed, exit 2.
  COMPARE SET (stricter only). Built ONLY with the unchanged load_hashes and HEX64 over every file the pre-fix tool read, plus the freeze
        export's keyword hashes:   ../sealed_hashes/keyword_hashes.jsonl, ../sealed_hashes_ac/keyword_hashes.jsonl,
        ../sealed_hashes_ac/source_keywords_prelim.jsonl (still read when present; any 64-hex string value in a line is a keyword hash),
        and the freeze export's keyword hashes. identifier_texts and source_hashes are unchanged; g13_c2's export classes are not used.
  --exports ohs4 is never binding: only the OHS-4 export is checked and read; its lines are "<id> HIT" or "<id> PASS-NONBINDING".

For every source in the input file it hashes these identifiers with the keyword rule of g13_c2.keyword_hashes
(runs of 1-8 tokens, punctuation-stripped variants, URL hosts with and without a leading www.):
  name, publisher, host, every other host (each as bare text and as https://<host>/ and https://www.<host>/),
  upstream id, licence page URL (as text), dataset URL (as text; extra, not required by 8.5).
Usage (from lean/c2_build):  ../../.venv/bin/python -B meta_src/source_name_check.py [--file F] [--role g_proxy|metadata] [--exports all|ohs4]
Exit code 0 when the integrity check passes and the verdict lines are printed; 2 on a missing / mismatching export or any error.
A61 (a): only the orchestrator runs this on real inputs, once per stage, on a whole fixed input file.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
sys.path.insert(0, str(BUILD))
import g13_c2  # noqa: E402  (read-only import: keyword_hashes, sha_hex)

HEX64 = re.compile(r"^[0-9a-f]{64}$")


def load_hashes(path: Path) -> set:
    out = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        vals = obj.values() if isinstance(obj, dict) else [obj]
        for v in vals:
            if isinstance(v, str) and HEX64.match(v):
                out.add(v)
    return out


def identifier_texts(src: dict) -> list:
    hosts = [src.get("host") or ""] + list(src.get("other_hosts") or [])
    texts = [src.get("name") or "", src.get("publisher") or "", src.get("upstream_id") or "",
             src.get("licence_url") or "", src.get("dataset_url") or ""]
    for h in hosts:
        if not h:
            continue
        bare = h[4:] if h.startswith("www.") else h
        texts += [h, bare, "www." + bare, f"https://{bare}/", f"https://www.{bare}/"]
    return [t for t in texts if t.strip()]


def source_hashes(src: dict) -> set:
    hs = set()
    for t in identifier_texts(src):
        hs |= g13_c2.keyword_hashes(t)
        hs.add(g13_c2.sha_hex(re.sub(r"\s+", " ", t.strip().lower())))     # whole identifier, any length
    return hs


# ---------------------------------------------------------------------------------------------------- A61 (f): the pins
OHS4_MANIFEST_SHA256 = "3771b47ad06157a97973eaf3539c9bde0b87e97b5b4458148a51f2506025470b"       # = g13_c2.SEALED_HASHES_MANIFEST_SHA256
OHS4_FREEZE_SHA256 = "c0217e7739c570b9d22176b68e1c489623dcd5f7c551011606b6ff17e59c09c3"          # the A38 freeze (= g13_c2.OHS4_FREEZE_SHA256)
OHSAC_FINAL_MANIFEST_SHA256 = "fadec66fdb3824ca3e81096c65b15d5e8cac7998a05fc964d0ce1b4fdb36cd9b"   # the OHS-AC final export's MANIFEST
OHSAC_FREEZE_MANIFEST_SHA256 = "27808b0ccbaf69aae058745ef0e80db6f5b692648198f26161bf749c3f1c3f6e"  # the freeze export (A64 h union record)
KW = "keyword_hashes.jsonl"
PRELIM = "source_keywords_prelim.jsonl"
UNION_STATUSES = ("union_built", "freeze_subset_of_final")
N_OHS4, N_FINAL, N_FREEZE = "OHS-4 export", "OHS-AC final export", "OHS-AC freeze export"


class ExportProblem(Exception):
    """An export that is missing or does not match: .name is the export, .kind is 'missing' or 'MISMATCH'."""

    def __init__(self, name: str, kind: str):
        super().__init__(f"{name} {kind}")
        self.name, self.kind = name, kind


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _json_dict(p: Path, name: str) -> dict:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, UnicodeDecodeError):
        raise ExportProblem(name, "MISMATCH") from None
    if not isinstance(d, dict):
        raise ExportProblem(name, "MISMATCH")
    return d


def verify_ohs4(root: Path) -> Path:
    """OHS-4: MANIFEST sha = the pin, it names the A38 freeze, and the keyword file matches the MANIFEST. Returns the keyword file."""
    mp, kp = root / "MANIFEST.json", root / KW
    if not mp.is_file() or not kp.is_file():
        raise ExportProblem(N_OHS4, "missing")
    if sha_file(mp) != OHS4_MANIFEST_SHA256:
        raise ExportProblem(N_OHS4, "MISMATCH")
    man = _json_dict(mp, N_OHS4)
    want = ((man.get("files") or {}).get(KW) or {}).get("sha256") if isinstance(man.get("files"), dict) else None
    if man.get("freeze_manifest_sha256") != OHS4_FREEZE_SHA256 or not isinstance(want, str) or sha_file(kp) != want:
        raise ExportProblem(N_OHS4, "MISMATCH")
    return kp


def verify_final(root: Path) -> Path:
    """OHS-AC final export: MANIFEST sha = the pin and the keyword file matches the MANIFEST's sha256 map. Returns the keyword file."""
    mp, kp = root / "MANIFEST.json", root / KW
    if not mp.is_file() or not kp.is_file():
        raise ExportProblem(N_FINAL, "missing")
    if sha_file(mp) != OHSAC_FINAL_MANIFEST_SHA256:
        raise ExportProblem(N_FINAL, "MISMATCH")
    man = _json_dict(mp, N_FINAL)
    want = man["sha256"].get(KW) if isinstance(man.get("sha256"), dict) else None
    if not isinstance(want, str) or sha_file(kp) != want:
        raise ExportProblem(N_FINAL, "MISMATCH")
    return kp


def verify_freeze(root: Path) -> Path | None:
    """OHS-AC freeze export through A64 (h)'s union record. Returns the union keyword file (status union_built), or None
    (freeze_subset_of_final with every count 0: the freeze keyword hashes are the final export's, already in the compare set)."""
    rp = root / "RECORD.json"
    if not rp.is_file():
        raise ExportProblem(N_FREEZE, "missing")
    rec = _json_dict(rp, N_FREEZE)
    status = rec.get("status")
    if status == "lost":
        raise ExportProblem(N_FREEZE, "missing")
    if status not in UNION_STATUSES or rec.get("freeze_manifest_sha256") != OHSAC_FREEZE_MANIFEST_SHA256:
        raise ExportProblem(N_FREEZE, "MISMATCH")
    fin = rec.get("final_manifest_sha256")
    if fin not in (None, OHSAC_FINAL_MANIFEST_SHA256):
        raise ExportProblem(N_FREEZE, "MISMATCH")
    counts = rec.get("counts") if rec.get("counts") is not None else rec.get("counts_per_kind_freeze_minus_final")
    leaves, stack = [], [counts]
    while stack:
        x = stack.pop()
        if isinstance(x, dict):
            stack += list(x.values())
        elif isinstance(x, (list, tuple)):
            stack += list(x)
        else:
            leaves.append(x)
    if counts is None or not leaves or any(isinstance(x, bool) or not isinstance(x, int) or x < 0 for x in leaves):
        raise ExportProblem(N_FREEZE, "MISMATCH")
    if status == "freeze_subset_of_final":
        if any(leaves):
            raise ExportProblem(N_FREEZE, "MISMATCH")
        return None
    sha = rec.get("sha256")
    if not isinstance(sha, dict) or not isinstance(sha.get(KW), str):
        raise ExportProblem(N_FREEZE, "MISMATCH")
    kp = root / KW
    if not kp.is_file():
        raise ExportProblem(N_FREEZE, "missing")
    if sha_file(kp) != sha[KW]:
        raise ExportProblem(N_FREEZE, "MISMATCH")
    return kp


def fold_id(i) -> str:
    """<id> and <id>#... are the source <id> (A42-D 8.5: PASS or HIT per source only)."""
    if not isinstance(i, str) or not i.split("#", 1)[0]:
        raise ValueError("entry without a usable id")
    return i.split("#", 1)[0]


def fold_verdicts(srcs: list, bad: set, role: str | None = None) -> list:
    """[(source id, 'PASS'|'HIT')] in first-appearance order: a source is a HIT if any of its entries hits (duplicate ids fold too)."""
    out = {}
    for s in srcs:
        if role and s["role"] != role:
            continue
        sid = fold_id(s.get("id"))
        out[sid] = out.get(sid, False) or bool(source_hashes(s) & bad)
    return [(sid, "HIT" if hit else "PASS") for sid, hit in out.items()]


def compare_set(build: Path = BUILD, exports: str = "all") -> tuple:
    """(problems, bad): the export problems ("<export> missing|MISMATCH" strings; then `bad` is empty) or the compare set, built ONLY with
    the unchanged load_hashes/HEX64 over the verified keyword files (+ the AC preliminary file when present, --exports all)."""
    ohs4, ac, union = Path(build) / "sealed_hashes", Path(build) / "sealed_hashes_ac", Path(build) / "sealed_hashes_ac_union"
    problems, files = [], []
    for name, fn, root in (((N_OHS4, verify_ohs4, ohs4),) if exports == "ohs4" else
                           ((N_OHS4, verify_ohs4, ohs4), (N_FINAL, verify_final, ac), (N_FREEZE, verify_freeze, union))):
        try:
            files.append(fn(root))
        except ExportProblem as e:
            problems.append(f"{e.name} {e.kind}")
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            problems.append(f"{name} MISMATCH")
    if problems:
        return problems, set()
    bad = set()
    for p in files:                                   # the OHS-4 and OHS-AC keyword files, then the union keyword file when there is one
        if p is not None:
            bad |= load_hashes(p)
    prelim = ac / PRELIM
    if exports == "all" and prelim.exists():          # the AC preliminary file: still read when present
        bad |= load_hashes(prelim)
    return [], bad


def run(argv=None, build: Path = BUILD) -> tuple:
    """(exit code, stdout lines). Integrity first; no verdict unless every required export verified."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=str(HERE / "SOURCES_CANDIDATES.json"))
    ap.add_argument("--role", default=None)
    ap.add_argument("--exports", default="all", choices=["ohs4", "all"],
                    help="ohs4 = only the OHS-4 export (never binding); all = OHS-4 + OHS-AC final + the freeze export, each verified")
    a = ap.parse_args(argv)
    try:
        problems, bad = compare_set(build, a.exports)
        if problems:
            return 2, problems
        srcs = json.loads(Path(a.file).read_text(encoding="utf-8"))["sources"]
        verdicts = fold_verdicts(srcs, bad, a.role)
        if a.exports == "ohs4":
            return 0, [f"{sid} {'HIT' if v == 'HIT' else 'PASS-NONBINDING'}" for sid, v in verdicts]
        return 0, [f"{sid} {v}" for sid, v in verdicts]
    except Exception:  # noqa: BLE001 - nothing else is ever printed
        return 2, []


def main():
    code, lines = run()
    for ln in lines:
        print(ln)
    sys.exit(code)


if __name__ == "__main__":
    main()
