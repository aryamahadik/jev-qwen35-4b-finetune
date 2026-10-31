"""keyword_narrow.py: OPTION 2 (b), the narrowed OHS-AC keyword export (default OFF, NOT applied; the export does not exist yet).

Why. For GB, GW, MD, I10 and the F-blocks the only OHS-AC method that hits is `keyword`: logs/decontam_counts/acquick_c2_*.json show
ohsac_hash keyword as the sole method with hits (4,590 / 4,427 / 4,132 / 123 rows and the F-block rows), because the 956 keyword hashes are
"source identifiers plus every held-out registry/tool/carrier name of >= 4 characters" and ANY single token of a C2 text that equals one
drops its unit (STOP_REPORT_A62c). For the 15 program families keyword also hits every unit, next to the sentence / n-gram methods, so
option 2 (a) alone cannot free them.

What. A FRESH sealed agent (brief: OPT2_SEALED_BRIEF_KW.md) rebuilds the keyword hashes from the same plain-text names the freeze export used,
but keeps only names that pass keyword_rule.decide (multi-token names; identifier-like names; single rare words, Zipf < 3.0 and length >= 5).
It writes a hash-only folder c2_build/sealed_hashes_ac_kw2/ (keyword_hashes.jsonl + MANIFEST.json). The C2 side never sees a name.

The C2 side switches to it only under an owner ruling carrying OHSAC_KW_NARROW (ruling_gate.py). With the switch, in THIS process:
  * g13_c2.AcSide.load verifies the narrowed export (below) and replaces the `keyword` hash set of the OHS-AC export (and of any union files:
    intersected) by the narrowed set. Nothing else in the export changes; the other nine required methods compare as before.
  * the narrowed files join the run-input guard (sha256 at start and end), and the OHS-AC record gains ohsac.keyword_narrow = {ruling, counts,
    shas, rule sha}.
  * any verification problem is a SystemExit (the run stops; it never silently falls back to either set).
The OHS-4 keyword method (ohs4_hash keyword), A53, A31 (b), the dev targets and the 8.5 source gate are untouched.

Verification of the export (counts and shas only; no name, no token probe):
  1. MANIFEST.json parses: kind ac_keyword_narrow, version 1; keyword_hashes.jsonl matches its sha256 and record count;
  2. rule block == keyword_rule.py's constants and rule_sha256 == the sha256 of keyword_rule.py now (the rule was fixed before the run);
  3. parent_manifest_sha256 == the OHS-AC export's MANIFEST sha256 now (same freeze);
  4. every narrowed hash is IN the full export's keyword set (the agent cannot add a hash), 0 < narrowed < full;
  5. the manifest's per-reason counts add up to the record count and use only the rule's reasons.
C2 does NOT test which common words are in the export (that would be a probe); it relies on 2 + 4 and on the agent's counts, and the
orchestrator reports the counts to the owner.

CLI (counts only): ../.venv/bin/python -B c2_build/zed_orch/owner_options/keyword_narrow.py verify [--dir DIR]
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import keyword_rule as kr  # noqa: E402
import ruling_gate as rg  # noqa: E402

KW_DIR_NAME = "sealed_hashes_ac_kw2"
KIND, VERSION = "ac_keyword_narrow", 1


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def rule_sha256() -> str:
    return _sha(HERE / "keyword_rule.py")


class NarrowError(SystemExit):
    pass


def load_narrowed(root: Path, full_keywords: set, parent_manifest_sha256: str) -> tuple[dict, frozenset]:
    """(info, narrowed hash set) of the folder `root`, or NarrowError. `full_keywords` = the OHS-AC export's keyword hash set now."""
    root, why = Path(root), []
    mp, kp = root / "MANIFEST.json", root / "keyword_hashes.jsonl"
    if not mp.is_file() or not kp.is_file():
        raise NarrowError(f"keyword narrowing refused: {root.name}/MANIFEST.json or keyword_hashes.jsonl is missing (the export is not built)")
    try:
        man = json.loads(mp.read_text(encoding="utf-8"))
    except ValueError:
        raise NarrowError("keyword narrowing refused: MANIFEST.json is not JSON") from None
    if man.get("kind") != KIND or man.get("version") != VERSION:
        why.append("MANIFEST kind / version")
    ent = (man.get("files") or {}).get("keyword_hashes.jsonl") or {}
    got_sha = _sha(kp)
    if ent.get("sha256") != got_sha:
        why.append("keyword_hashes.jsonl differs from its recorded sha256")
    hashes, bad = [], 0
    for ln in kp.read_text(encoding="utf-8").splitlines():
        if ln.strip():
            r = json.loads(ln)
            if r.get("kind") != "keyword" or not isinstance(r.get("hash"), str) or len(r["hash"]) != 64:
                bad += 1
            else:
                hashes.append(r["hash"])
    hs = frozenset(hashes)
    if bad:
        why.append(f"{bad} line(s) that are not a keyword hash")
    if len(hashes) != len(hs) or ent.get("records") != len(hs):
        why.append("record count differs from the manifest (or duplicate hashes)")
    rule = man.get("rule") or {}
    want = {"version": kr.RULE_VERSION, "min_len_single": kr.SINGLE_MIN_LEN, "zipf_max": kr.ZIPF_MAX, "wordfreq_version": kr.WORDFREQ_VERSION,
            "export_min_len": kr.EXPORT_MIN_LEN}
    if any(rule.get(k) != v for k, v in want.items()):
        why.append("rule block differs from keyword_rule.py")
    if rule.get("rule_sha256") != rule_sha256():
        why.append("rule_sha256 is not the sha256 of keyword_rule.py now")
    if man.get("parent_manifest_sha256") != parent_manifest_sha256:
        why.append("parent_manifest_sha256 is not the OHS-AC export's MANIFEST sha256")
    if not hs <= set(full_keywords):
        why.append(f"{len(hs - set(full_keywords))} narrowed hash(es) are not in the full export's keyword set")
    if not 0 < len(hs) < len(full_keywords):
        why.append("the narrowed set must be non-empty and smaller than the full set")
    cnt = man.get("counts") or {}
    kept, dropped = cnt.get("kept_names_by_reason") or {}, cnt.get("dropped_names_by_reason") or {}
    if not set(kept) <= set(kr.REASONS_KEEP) or not set(dropped) <= set(kr.REASONS_DROP) or cnt.get("narrowed_hashes") != len(hs) \
            or cnt.get("full_keyword_hashes") != len(full_keywords):
        why.append("manifest counts do not match the export or use reasons outside the rule")
    if why:
        raise NarrowError("keyword narrowing refused: " + "; ".join(why))
    return ({"dir": root.name, "manifest_sha256": _sha(mp), "keyword_hashes_sha256": got_sha, "rule_sha256": rule["rule_sha256"],
             "narrowed_hashes": len(hs), "full_keyword_hashes": len(full_keywords),
             "kept_names_by_reason": dict(sorted(kept.items())), "dropped_names_by_reason": dict(sorted(dropped.items())),
             "parent_manifest_sha256": parent_manifest_sha256}, hs)


def install(G, ruling: dict, root: Path | None = None) -> None:
    """Wrap g13_c2.AcSide.load / .record and ac_guard_files in THIS process (idempotent). `ruling` = ruling_gate.require(...) info."""
    if getattr(G, "_opt2_kw", False):
        return
    root = Path(root) if root is not None else Path(G.HERE) / KW_DIR_NAME
    orig_load = G.AcSide.load.__func__
    orig_record = G.AcSide.record
    orig_guard = G.ac_guard_files

    def load(cls, root_=None, union_root=None, prereg_text=None):
        side = orig_load(cls, root_, union_root, prereg_text)
        if side.ex is None:                                   # the export did not verify: the run is incomplete anyway; nothing to narrow
            return side
        info, hs = load_narrowed(root, side.ex.sets["keyword"], side.ex.manifest_sha256)
        side.ex.sets["keyword"] = set(hs)
        for e in side.union.get("exports") or []:
            e.sets["keyword"] = set(e.sets.get("keyword") or ()) & hs
        side.keyword_narrow = {**info, "ruling": ruling}
        return side

    def record(self):
        r = orig_record(self)
        if getattr(self, "keyword_narrow", None):
            r["keyword_narrow"] = self.keyword_narrow
        return r

    G.AcSide.load, G.AcSide.record = classmethod(load), record
    G.ac_guard_files = lambda: [*orig_guard(), root / "MANIFEST.json", root / "keyword_hashes.jsonl"]
    G._opt2_kw = True


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("verify", help="verify the narrowed export against the OHS-AC export (counts only)")
    v.add_argument("--dir", default=None)
    a = ap.parse_args(argv)
    cb = rg.lean_on_path()
    import g13_c2 as G
    ex = G.ExportsAC()
    info, hs = load_narrowed(Path(a.dir) if a.dir else cb / KW_DIR_NAME, ex.sets["keyword"], ex.manifest_sha256)
    print(json.dumps({"ok": True, **info}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
