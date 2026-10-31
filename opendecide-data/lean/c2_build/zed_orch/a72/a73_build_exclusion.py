"""A73 exclusion list (drop-only; A34 b: units leave the pool BEFORE selection). CPU only; no Modal, no G13, no model call. Reads row METADATA
only (row source) and ids; no row text is printed or kept. Every MD candidate unit that holds a row whose source is c2_md_ror leaves the pool
(whole source, A73). Plain drop list in the same format as a72_excl_*.json (complete true, drop_ids). Run from lean/:
  ../.venv/bin/python -B c2_build/zed_orch/a72/a73_build_exclusion.py [--write]"""
import sys, json, hashlib, argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_exclusions as be  # noqa: E402

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true"); a = ap.parse_args()
    rows, rels = be.load("MD")
    ids, nu, nm = be.closure(rows, rels, lambda r: r.get("source") == "c2_md_ror")
    sha = be.sha_ids(ids)
    print("MD_ror_source ids", len(ids), "units", nu, "direct_rows", nm, "candidates", len(rows), "sha", sha[:16])
    if a.write:
        doc = {"set": "a73_excl_MD_ror_source", "tool": "a72/a73_build_exclusion.py", "complete": True, "incomplete_why": [], "drop_ids": ids,
               "drop_ids_sha256": sha, "counts": {"units": nu, "direct_rows": nm, "candidates": len(rows), "source": "c2_md_ror",
               "basis": "A73: c2_md_ror falls to 39 tasks (< 40, A42-D 8.2) after the A72 quarantine; ROR leaves MD whole (drop-only), MD re-selected from its other 10 sources"}}
        p = HERE / "a73_excl_MD_ror_source.json"
        p.write_text(json.dumps(doc, indent=1, sort_keys=True), encoding="utf-8")
        print("wrote", p, hashlib.sha256(p.read_bytes()).hexdigest()[:16])

if __name__ == "__main__":
    main()
