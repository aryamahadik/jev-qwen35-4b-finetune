"""a57_hashcmp.py: C2-side hash compare of C2 texts against a sealed hash export (A57 steps 2 and 6(i); Ruling A64 (g)).
Counts and C2 ids only. Exports: sealed_hashes_ac (OHS-AC; MANIFEST layout 'sha256' map) or sealed_hashes (OHS-4).
Input: --units <jsonl> of {"id","text"} (each is a TEMPLATE unit: compared cut at placeholders and lines AND uncut, with rows_src, so exact_raw,
the full_text kinds, structure_g13 and the skeleton kinds always run; g13_c2.ac_unit_from_texts).
Usage (from c2_build): ../../.venv/bin/python -B zed_orch/a57_hashcmp.py --export ac --units u.jsonl --out r.json

`complete` is COMPUTED, not written by hand. For --export ac it is true only if the MANIFEST verifies, finality holds by the addendum shas of
PREREG_FINAL.md (MANIFEST fadec66f..., suite c2dfefa6..., post-freeze manifest 305356b6..., source manifest fcf4b384...; the MANIFEST stage string is
recorded and decides nothing), the union record sealed_hashes_ac_union/RECORD.json exists and is ok, and every required method ran on every unit.
For --export ohs4 (the single frozen OHS-4 export, pinned by its manifest sha at load) it is true if the export verified and every required method
ran on every unit. Exit 0 = 0 hits and complete; 4 = complete with hits; 3 = not complete (hits, if any, are in the file and still stand); 2 = the
export did not verify.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import g13_c2 as G  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", choices=["ac", "ohs4"], required=True)
    ap.add_argument("--units", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    units = []
    for line in Path(a.units).read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            u = G.ac_unit_from_texts(str(r["id"]), [("text", r["text"])], True)
            if u is not None:
                units.append(u)
    if a.export == "ac":
        side = G.AcSide.load()
        if side.ex is None:
            print(json.dumps({"error": "export", "detail": side.manifest_error}))
            return 2
        hits, rep, cover = side.hash_compare(units)
        complete, why = side.completeness(units, cover)
        ident = {"export": "ac", **side.record()}
    else:
        try:
            ex = G.Exports()
        except (G.ExportError, OSError, KeyError, ValueError) as e:
            print(json.dumps({"error": "export", "detail": str(e)[:300]}))
            return 2
        cover = {}
        hits, rep = G.ohs4_hash_hits(units, ex, cover=cover)
        short = sum(1 for u in units if set(G.AC_REQUIRED_METHODS) - cover.get(u["key"], set()))
        why = [f"{short} unit(s) did not get every required method"] if short else []
        complete = not why
        ident = {"export": "ohs4", "manifest_verified": True, "manifest_sha256": ex.shas.get("manifest"),
                 "finality": "n/a: the OHS-4 export is the single frozen export, pinned by its manifest sha at load",
                 "union": "n/a"}
    ids = sorted({k for m in hits.values() for k in m})
    res = {"tool": "a57_hashcmp", "version": 2, **ident,
           "units": len(units), "hit_units": len(ids), "hit_ids": ids,
           "by_method": {m: len(v) for m, v in sorted(hits.items())}, "report_only": rep,
           "required_methods": list(G.AC_REQUIRED_METHODS),
           "units_missing_methods": sum(1 for u in units if set(G.AC_REQUIRED_METHODS) - cover.get(u["key"], set())),
           "complete": complete, "incomplete_why": why}
    Path(a.out).write_text(json.dumps(res, indent=1))
    print(json.dumps({k: res[k] for k in ("export", "units", "hit_units", "by_method", "report_only", "complete")}))
    if not complete:
        return 3
    return 0 if not ids else 4


if __name__ == "__main__":
    sys.exit(main())
