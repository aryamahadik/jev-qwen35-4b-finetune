#!/usr/bin/env python3
"""zed_orch/a57_hashcheck_ac.py: the C2-side hash compare against the OHS-AC hash export (Ruling A57 steps 2 and 6 (i)).

CPU only, no network, $0. Reads ONLY c2_build/sealed_hashes_ac/ (hash files; FORMAT.md) and the C2 texts it is given.
Never opens any "ohs" path. Prints / writes counts and C2 ids only.

  ../../.venv/bin/python -B zed_orch/a57_hashcheck_ac.py selftest
  ../../.venv/bin/python -B zed_orch/a57_hashcheck_ac.py taskfiles <tasks dir> --out <result.json> [--pat '*.md']
  ../../.venv/bin/python -B zed_orch/a57_hashcheck_ac.py texts <jsonl of {"id","text"}> --out <result.json>

Compare = c2_build/g13_c2.ohs4_hash_hits (the FORMAT.md rules: ngram10, ngram12, full_text_norm(_min5words), full_text_raw,
sentence_norm_min5words, keyword, structure / skeleton kinds). The export is verified first: every file's sha256 against
MANIFEST.json "sha256", record counts against "records", the freeze manifest sha (source_manifest_sha256) against the freeze
addendum of PREREG_FINAL.md and the A42-D block sha. The result records MANIFEST.json's stage, final_suite_sha256 and
whether the stage is final; an export that is not the final one is NOT valid for A57 step 6 (complete=false there).
Exit 0 = 0 hits and complete; 4 = hits; 2 = usage / export error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parent
sys.path.insert(0, str(C2_BUILD))
import g13_c2 as G  # noqa: E402  (c2_build wrapper: words / norm / hashes / ohs4_hash_hits; imported, not edited)

EXPORT = C2_BUILD / "sealed_hashes_ac"
FREEZE_SHA = "fcf4b384c7acae198dd597c8eb5b1b2f13ff5d6a2ad57ae878c88f23755320b6"
A42D_SHA = "cbdc29d950bba3bad3e1fa2559346eae9405522c30bb7a4ffe0aaf7873665d2f"
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


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


class ExportsAC(G.Exports):
    """sealed_hashes_ac/, checked before use (no OHS-4 pins). Membership tests only; nothing here is ever printed."""

    def __init__(self, root: Path = EXPORT):
        man = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
        self.manifest = man
        problems = []
        if man.get("source_manifest_sha256") != FREEZE_SHA:
            problems.append("source_manifest_sha256 is not the freeze manifest sha of the freeze addendum")
        if man.get("a42d_block_sha256") != A42D_SHA:
            problems.append("a42d_block_sha256 differs from the A42-D block sha")
        prereg = G.c2io.PREREG.read_text(encoding="utf-8")
        if FREEZE_SHA not in prereg or A42D_SHA not in prereg:
            problems.append("the freeze sha / A42-D sha are not in PREREG_FINAL.md")
        if man.get("format_md_sha256") != sha_file(root / "FORMAT.md"):
            problems.append("FORMAT.md differs from MANIFEST.json")
        for name, want in man["sha256"].items():
            if sha_file(root / name) != want:
                problems.append(f"{name} differs from MANIFEST.json")
        if problems:
            raise G.ExportError("; ".join(problems))
        self.shas = {"manifest": sha_file(root / "MANIFEST.json"), **man["sha256"]}
        self.ng = {n: self._grams(root / f"ngrams{n}_sha256.npy") for n in (10, 12)}
        for n in (10, 12):
            if len(self.ng[n][0]) != man["records"][f"ngrams{n}_sha256.npy"]:
                raise G.ExportError(f"ngrams{n}: record count differs from MANIFEST.json")
        self.sets = defaultdict(set)
        for f in ("text_hashes.jsonl", "structure_hashes.jsonl", "keyword_hashes.jsonl"):
            for line in (root / f).read_text(encoding="utf-8").splitlines():
                if line.strip():
                    r = json.loads(line)
                    self.sets[r["kind"]].add(r["hash"])
        for f in ("text_hashes.jsonl", "structure_hashes.jsonl", "keyword_hashes.jsonl"):
            for k, n in man["records"][f].items():
                if len(self.sets[k]) != n:
                    raise G.ExportError(f"kind {k}: {len(self.sets[k])} hashes, manifest says {n}")
        self.struct = {k[:-2]: self.sets[k[:-2] + "_R"] | self.sets[k[:-2] + "_U"]
                       for k in self.STRUCT_KINDS if k.endswith("_R")}
        self.stage = man.get("stage")
        self.final_suite_sha256 = man.get("final_suite_sha256")
        self.is_final = self.stage in ("final", "post_surface_final")


def selftest(ex: ExportsAC) -> dict:
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
    kw = next(iter(ex.sets["keyword"]))
    res["keyword_set_nonempty"] = bool(kw)
    return res


def units_from_taskfiles(d: Path, pat: str) -> list:
    units = []
    for p in sorted(d.glob(pat)):
        t = p.read_text(encoding="utf-8")
        texts = [("file", t)] + [("line", ln) for ln in t.split("\n") if ln.strip()]
        units.append({"key": p.stem, "texts": texts, "template": False})
    return units


def units_from_jsonl(p: Path) -> list:
    units = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        if ln.strip():
            r = json.loads(ln)
            units.append({"key": r["id"], "texts": [("text", r["text"])], "template": False})
    return units


def run(units: list, ex: ExportsAC) -> dict:
    hits, rep = G.ohs4_hash_hits(units, ex)
    by_method = {m: len(v) for m, v in sorted(hits.items())}
    hit_units = sorted({k for v in hits.values() for k in v})
    return {"tool": "a57_hashcheck_ac", "version": 1, "export": "c2_build/sealed_hashes_ac",
            "export_stage": ex.stage, "export_final": ex.is_final, "final_suite_sha256": ex.final_suite_sha256,
            "manifest_sha256": ex.shas["manifest"], "manifest_verified": True,
            "freeze_manifest_sha256": FREEZE_SHA,
            "counts": {"units": len(units), "texts": sum(len(u["texts"]) for u in units), "hit_units": len(hit_units),
                       "by_method": by_method, "report_only": rep},
            "hit_ids": hit_units, "complete": True}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("selftest", "taskfiles", "texts"))
    ap.add_argument("path", nargs="?")
    ap.add_argument("--pat", default="*.md")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    try:
        ex = ExportsAC()
    except (G.ExportError, OSError, KeyError, ValueError) as e:
        print(json.dumps({"error": "export", "detail": str(e)[:300]}))
        return 2
    st = selftest(ex)
    if a.cmd == "selftest":
        print(json.dumps({"selftest": st, "ok": all(st.values()), "stage": ex.stage, "final": ex.is_final}))
        return 0 if all(st.values()) else 2
    if not all(st.values()):
        print(json.dumps({"error": "selftest", "selftest": st}))
        return 2
    units = units_from_taskfiles(Path(a.path), a.pat) if a.cmd == "taskfiles" else units_from_jsonl(Path(a.path))
    res = run(units, ex)
    res["selftest_ok"] = True
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"counts": res["counts"], "complete": res["complete"], "export_stage": res["export_stage"]}))
    return 0 if res["counts"]["hit_units"] == 0 else 4


if __name__ == "__main__":
    sys.exit(main())
