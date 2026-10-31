"""A57 step 6 for T43 program text (no Haiku pool): (i) C2-side hash compare vs sealed_hashes_ac (final export), (ii) g13_ohsac_check --rows,
(iii) gtpl_check_ac --templates --min-shared 1 --parts all. Run only; counts and ids. Mac, from c2_build:
  HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 ../../.venv/bin/python -B zed_orch/a57_t43_step6.py
"""
import json, sys, time, hashlib
from pathlib import Path
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2)); sys.path.insert(0, str(Path(__file__).parent))
from families.T43 import texts as TX
import a57_hashcheck_ac as HC
import g13_c2 as G
LEAN = G.LEAN
items = {}
for k, v in TX.RULES.items(): items[f"rule:{k}"] = v
for qf, ws in TX.WORDINGS.items():
    for i, w in enumerate(ws): items[f"wording:{qf}:{i}"] = w
for k, v in TX.OPT.items(): items[f"opt:{k}"] = v
for k, v in TX.NONE_TEXT.items(): items[f"none:{k}"] = v
for k, v in TX.TITLES.items(): items[f"title:{k}"] = v
ex = HC.ExportsAC(); st = HC.selftest(ex); assert all(st.values()), st
units = [{"key": i, "texts": [("text", t)], "template": False} for i, t in items.items()]
r = HC.run(units, ex)
hits_by = {}
ghits, rep = G.ohs4_hash_hits(units, ex)
for m, ids in ghits.items():
    for i in ids: hits_by.setdefault(i, []).append(m)
rows = [{"id": i, "call_id": i, "state": t} for i, t in items.items()]
ac_rows = G.run_checker(LEAN / "ohs_ac_sealed" / "tools" / "g13_ohsac_check.py", "--rows", rows)
trecs = [{"id": i, "text": G.SLOT_RE.sub("{X}", t)} for i, t in items.items()]
ac_tpl = G.run_checker(LEAN / "ohs_ac_sealed" / "tools" / "gtpl_check_ac.py", "--templates", trecs, extra=["--min-shared", "1", "--parts", "all"])
out = {"time_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), "texts_py_sha256": hashlib.sha256(Path(TX.__file__).read_bytes()).hexdigest(),
       "n_items": len(items),
       "hashcmp": {k: r[k] for k in ("export_stage", "export_final", "final_suite_sha256", "manifest_sha256", "manifest_verified", "complete", "counts")},
       "hashcmp_hit_ids_by_method": hits_by,
       "ohsac_rows": {k: ac_rows.get(k) for k in ("status", "exit", "manifest_verified", "suite_sha256", "complete", "counts", "hit_ids", "hit_ids_by_method")},
       "ohsac_templates": {k: ac_tpl.get(k) for k in ("status", "exit", "manifest_verified", "suite_sha256", "complete", "counts", "hit_ids", "hit_ids_by_method")}}
out["union_dropped_would_be"] = sorted(set(r["hit_ids"]) | set(ac_rows.get("hit_ids") or []) | set(ac_tpl.get("hit_ids") or []))
(C2 / "logs" / "a57" / "T43_step6.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
print(json.dumps({k: v for k, v in out.items() if k != "hashcmp_hit_ids_by_method"}, default=str)[:4000])
