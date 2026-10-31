#!/usr/bin/env python3
"""zed_orch/a57_hashcheck_ac.py: the C2-side hash compare against the OHS-AC hash export (Ruling A57 steps 2 and 6 (i); Ruling A64 (g)).

CPU only, no network, no Modal, $0. Reads ONLY c2_build/sealed_hashes_ac/ and c2_build/sealed_hashes_ac_union/ (hash files; FORMAT.md) and
the C2 texts it is given. Never opens any "ohs" path. Prints / writes counts and C2 ids only.

  ../../.venv/bin/python -B zed_orch/a57_hashcheck_ac.py selftest
  ../../.venv/bin/python -B zed_orch/a57_hashcheck_ac.py taskfiles <tasks dir> --out <result.json> [--pat '*.md']
  ../../.venv/bin/python -B zed_orch/a57_hashcheck_ac.py texts <jsonl of {"id","text"}> --out <result.json>

The compare is c2_build/g13_c2.AcSide.hash_compare (the FORMAT.md rules through ohs4_hash_hits). A64 (g) 3: ONE way to build units. Every text is
compared both uncut and as cut template pieces (so exact_raw and the full_text kinds always run), and passed as a state and as an instruction
(rows_src), so structure_g13, skeleton_state, skeleton_instructions and skeleton_line also run.

`complete` is COMPUTED (A64 g 1, g 2), true only if ALL of these hold; otherwise false and the exit code is 3:
  * the export's MANIFEST verifies (every file's sha256, the record counts, FORMAT.md, the A42-D block sha);
  * finality holds by the addendum shas read from PREREG_FINAL.md: the MANIFEST file sha (fadec66f...), final_suite_sha256 (c2dfefa6...),
    post_freeze_manifest_sha256 (305356b6...) and source_manifest_sha256 (fcf4b384...). The MANIFEST "stage" string is recorded and decides nothing;
  * the union record c2_build/sealed_hashes_ac_union/RECORD.json exists and is ok (status freeze_subset_of_final with every count 0, or union_built
    with verified union files; 'lost' or missing = not ok);
  * every required method ran on every unit (g13_c2.AC_REQUIRED_METHODS).
Exit 0 = 0 hits and complete; 4 = complete with hits; 3 = not complete (hits, if any, are in the file and still stand: a record can count as a
hit but never as a pass); 2 = usage / export error (the export did not verify; nothing was compared).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parent
sys.path.insert(0, str(C2_BUILD))
import g13_c2 as G  # noqa: E402  (c2_build wrapper: words / norm / hashes / the OHS-AC side; imported, not edited)

VEC = "The quick brown fox jumps over the lazy dog while seven bakers sing loudly near the old harbour wall."
VEC_EXPECT = {
    "norm": "the quick brown fox jumps over the lazy dog while seven bakers sing loudly near the old harbour wall",
    "ng10": "100f4b5d5ad9f8b1e0f70e122374bcb151ee5108e3323e981322588380a0121c",
    "ng12": "b3bf0c9691b60f8273f9f31cc8fabae58029194949363bacec931eabbd2b257d",
    "full_norm": "bcae36e66bee28e419f6c66999314f636d9af10f99a082aa60217adbc3705862",
    "full_raw": "8319bfde10020cf668ceab48284326ddb2c02440da8a2c0786c6b4722968bdfc",
    "skeleton": "5e56e8ce7b5c8a97db7b8e744678c637c541ec272e22eafaabb8e22e7da9cede",
    "keyword": "867c3db642f0e99f2aea32ff92be5c9a543dd1c028c4b12b24e76e589719f679",
    "struct": "207ab7b3aedb04d5ca8368c5d26f5bae079d7c553c1a79d652fe286da13d4d8f",
}


ExportsAC = G.ExportsAC       # kept for the A57 drivers (a57_t4x_*.py): HC.ExportsAC(), HC.selftest(ex), HC.run(units, ex). Their units are built their
                              # own way, so the computed `complete` of HC.run is false unless every required method ran on every unit (A64 g).


def _side(x) -> "G.AcSide":
    """An AcSide from an AcSide, or (legacy callers) from the ExportsAC they hold: the side is rebuilt from disk, so finality and the union
    record are always checked."""
    return x if isinstance(x, G.AcSide) else G.AcSide.load()


def selftest(side: "G.AcSide") -> dict:
    side = _side(side)
    ex = side.ex
    ws = G.words(VEC)
    got = {
        "norm": G.norm(VEC),
        "ng10": G.gram_digests(ws, 10)[0].hex(),
        "ng12": G.gram_digests(ws, 12)[0].hex(),
        "full_norm": G.sha_hex(G.norm(VEC)),
        "full_raw": G.sha_hex(VEC),
        "skeleton": G.sha_hex(G.skeleton(VEC)),
        "keyword": G.sha_hex("example keyword"),
        "struct": G.struct_g13("Alice pays Bob 12 dollars on Monday.", ["Alice", "Bob"]),
    }
    res = {k: got[k] == v for k, v in VEC_EXPECT.items()}
    # positive controls: a digest taken from the export itself is found; a fixed non-item text is not
    a, _pre = ex.ng[10]
    res["lookup_positive_ng10"] = ex.has_grams(10, [bytes(a[len(a) // 2])])
    a12, _ = ex.ng[12]
    res["lookup_positive_ng12"] = ex.has_grams(12, [bytes(a12[len(a12) // 3])])
    res["lookup_negative"] = not ex.has_grams(10, G.gram_digests(ws, 10)) and not ex.has_grams(12, G.gram_digests(ws, 12))
    res["keyword_set_nonempty"] = bool(next(iter(ex.sets["keyword"])))
    # A64 g 3 on a synthetic template unit: every required method's code runs on it (exact_raw included), and that is what `complete` counts
    unit = G.ac_unit_from_texts("selftest", [("text", "Dear {NAME}, " + VEC + "\nSecond line {N} of the synthetic unit goes here.")], True)
    cover: dict = {}
    G.ohs4_hash_hits([unit], ex, cover=cover)
    res["template_unit_runs_every_method"] = cover.get("selftest") == set(G.AC_REQUIRED_METHODS)
    return res


def units_from_taskfiles(d: Path, pat: str) -> list:
    units = []
    for p in sorted(d.glob(pat)):
        t = p.read_text(encoding="utf-8")
        texts = [("file", t)] + [("line", ln) for ln in t.split("\n") if ln.strip()]
        u = G.ac_unit_from_texts(p.stem, texts, True)
        if u is not None:
            units.append(u)
    return units


def units_from_jsonl(p: Path) -> list:
    units = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        if ln.strip():
            r = json.loads(ln)
            u = G.ac_unit_from_texts(str(r["id"]), [("text", r["text"])], True)
            if u is not None:
                units.append(u)
    return units


def _full_unit(u: dict) -> dict:
    """Legacy A57 drivers build units by hand ({"key","texts","template"}). Rebuild those through G.ac_unit_from_texts so every required method
    (uncut for templates, rows_src for structure_g13 / skeleton_*) is set up; a unit that already carries rows_src is left as it is."""
    if "rows_src" in u:
        return u
    v = G.ac_unit_from_texts(str(u["key"]), list(u["texts"]), bool(u.get("template", True)))
    if v is None:
        return u
    return {**u, **{k: v[k] for k in v if k not in ("key",)}}


def run(units: list, side: "G.AcSide") -> dict:
    side = _side(side)
    units = [_full_unit(u) for u in units]
    hits, rep, cover = side.hash_compare(units)
    complete, why = side.completeness(units, cover)
    by_method = {m: len(v) for m, v in sorted(hits.items())}
    hit_units = sorted({k for v in hits.values() for k in v})
    return {"tool": "a57_hashcheck_ac", "version": 2, "export": "c2_build/sealed_hashes_ac", **side.record(),
            # legacy key names read by the A57 drivers (a57_t40_stage4*.py, a57_t44_stage4.py, a57_t43_step6.py); export_final is the COMPUTED finality
            "export_stage": side.ex.stage if side.ex else None, "export_final": bool(side.ex and side.ex.is_final),
            "freeze_manifest_sha256": side.union.get("freeze_manifest_sha256"),
            "required_methods": list(G.AC_REQUIRED_METHODS),
            "counts": {"units": len(units), "texts": sum(len(u["texts"]) for u in units), "hit_units": len(hit_units),
                       "by_method": by_method, "report_only": rep,
                       "units_missing_methods": sum(1 for u in units if set(G.AC_REQUIRED_METHODS) - cover.get(u["key"], set()))},
            "hit_ids": hit_units, "complete": complete, "incomplete_why": why}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("selftest", "taskfiles", "texts"))
    ap.add_argument("path", nargs="?")
    ap.add_argument("--pat", default="*.md")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    side = G.AcSide.load()
    if side.ex is None:
        print(json.dumps({"error": "export", "detail": side.manifest_error}))
        return 2
    st = selftest(side)
    if a.cmd == "selftest":
        print(json.dumps({"selftest": st, "ok": all(st.values()), "stage_recorded_only": side.ex.stage, "final": side.ex.is_final,
                          "union_status": side.union["status"], "complete_possible": not side.problems,
                          "problems": side.problems}))
        return 0 if all(st.values()) else 2
    if not all(st.values()):
        print(json.dumps({"error": "selftest", "selftest": st}))
        return 2
    units = units_from_taskfiles(Path(a.path), a.pat) if a.cmd == "taskfiles" else units_from_jsonl(Path(a.path))
    res = run(units, side)
    res["selftest_ok"] = True
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"counts": res["counts"], "complete": res["complete"], "final": res["final"],
                      "union_status": res["union"]["status"], "incomplete_why": res["incomplete_why"]}))
    if not res["complete"]:
        return 3
    return 0 if res["counts"]["hit_units"] == 0 else 4


if __name__ == "__main__":
    sys.exit(main())
