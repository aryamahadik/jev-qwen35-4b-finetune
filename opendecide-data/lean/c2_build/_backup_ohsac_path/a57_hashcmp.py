"""a57_hashcmp.py: C2-side hash compare of C2 texts against a sealed hash export (A57 steps 2 and 6(i)).
Counts and C2 ids only. Exports: sealed_hashes_ac (OHS-AC; MANIFEST layout 'sha256' map) or sealed_hashes (OHS-4).
Input: --units <jsonl> of {"id","text"} (each is a TEMPLATE unit: cut at placeholders and lines, FORMAT.md compare).
Usage (from c2_build): ../../.venv/bin/python -B zed_orch/a57_hashcmp.py --export ac --units u.jsonl --out r.json
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from collections import defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import g13_c2 as G  # noqa: E402


class ACExports(G.Exports):
    def __init__(self, root: Path):
        man = json.loads((root / "MANIFEST.json").read_text())
        for name, sha in man["sha256"].items():
            got = hashlib.sha256((root / name).read_bytes()).hexdigest()
            if got != sha:
                raise G.ExportError(f"{name} differs from MANIFEST.json")
        fm = hashlib.sha256((root / "FORMAT.md").read_bytes()).hexdigest()
        self.format_ok = fm == man.get("format_md_sha256")
        self.manifest_sha = hashlib.sha256((root / "MANIFEST.json").read_bytes()).hexdigest()
        self.man = man
        self.ng = {n: self._grams(root / f"ngrams{n}_sha256.npy") for n in (10, 12)}
        self.sets = defaultdict(set)
        for f in ("text_hashes.jsonl", "structure_hashes.jsonl", "keyword_hashes.jsonl"):
            for line in (root / f).read_text(encoding="utf-8").splitlines():
                if line.strip():
                    r = json.loads(line)
                    self.sets[r["kind"]].add(r["hash"])
        rec = man["records"]
        for f in ("text_hashes.jsonl", "structure_hashes.jsonl", "keyword_hashes.jsonl"):
            for k, n in rec[f].items():
                if len(self.sets[k]) != n:
                    raise G.ExportError(f"kind {k}: {len(self.sets[k])} vs manifest {n}")
        self.struct = {k[:-2]: self.sets[k[:-2] + "_R"] | self.sets[k[:-2] + "_U"]
                       for k in self.STRUCT_KINDS if k.endswith("_R")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", choices=["ac", "ohs4"], required=True)
    ap.add_argument("--units", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    ex = ACExports(HERE / "sealed_hashes_ac") if a.export == "ac" else G.Exports()
    units = []
    for line in Path(a.units).read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            units.append({"key": r["id"], "texts": [("text", r["text"])], "template": True})
    hits, rep = G.ohs4_hash_hits(units, ex)
    ids = sorted({k for m in hits.values() for k in m})
    res = {"tool": "a57_hashcmp", "export": a.export, "manifest_sha256": getattr(ex, "manifest_sha", None) or ex.shas.get("manifest"),
           "final_suite_sha256": getattr(ex, "man", {}).get("final_suite_sha256"),
           "stage": getattr(ex, "man", {}).get("stage"), "format_md_ok": getattr(ex, "format_ok", None),
           "units": len(units), "hit_units": len(ids), "hit_ids": ids,
           "by_method": {m: len(v) for m, v in hits.items()}, "report_only": rep,
           "complete": True}
    Path(a.out).write_text(json.dumps(res, indent=1))
    print(json.dumps({k: res[k] for k in ("export", "units", "hit_units", "by_method", "report_only")}))
    sys.exit(0 if not ids else 4)


if __name__ == "__main__":
    main()
