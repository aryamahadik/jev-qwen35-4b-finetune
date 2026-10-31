"""A74 SB5 exclusion list (drop-only; A34 b; A58 step 6 / A72): every unit holding an Opus-confirmed wrong-gold or ambiguous row of the A74 G9 read
(crowd_c2/g9_reread_a74/fam/SB5/G9_RESULT.json). Layered on a72_excl_SB5_g9.json (kept; both files are passed to --exclude-ids).
Reuses a72/build_exclusions.py load/closure/sha_ids unchanged. CPU only; ids/counts/sha only. Run from lean/: ../.venv/bin/python -B c2_build/zed_orch/a74/build_sb5_excl.py [--write]"""
import sys, json, hashlib
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "a72")); sys.dont_write_bytecode = True
import build_exclusions as B
CB = B.CB
r = json.load(open(CB / "crowd_c2" / "g9_reread_a74" / "fam" / "SB5" / "G9_RESULT.json"))
bad = set(r.get("confirmed_wrong_gold_ids") or []) | set(r.get("confirmed_ambiguous_ids") or [])
rows, rels = B.load("SB5")
ids, nu, nm = B.closure(rows, rels, lambda x: x["id"] in bad)
print("SB5_g9_a74 confirmed", len(bad), "direct_rows", nm, "units", nu, "ids", len(ids), "candidates", len(rows), "sha", B.sha_ids(ids)[:16])
if "--write" in sys.argv:
    doc = {"set": "a74_excl_SB5_g9", "tool": "a74/build_sb5_excl.py", "complete": True, "incomplete_why": [], "drop_ids": ids,
           "drop_ids_sha256": B.sha_ids(ids), "counts": {"confirmed_wrong_gold": len(r.get("confirmed_wrong_gold_ids") or []),
           "confirmed_ambiguous": len(r.get("confirmed_ambiguous_ids") or []), "units": nu, "direct_rows": nm, "candidates": len(rows)}}
    p = HERE / "a74_excl_SB5_g9.json"
    p.write_text(json.dumps(doc, indent=1, sort_keys=True), encoding="utf-8")
    print("wrote", hashlib.sha256(p.read_bytes()).hexdigest())
