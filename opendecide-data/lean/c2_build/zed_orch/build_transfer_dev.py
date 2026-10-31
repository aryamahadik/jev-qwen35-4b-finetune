"""Build lean/data/c2_transfer_dev.jsonl (C2_DATA_SPEC 7.1 transfer dev; PREREG A52/A45 c, A48 a).
Sources: transfer/T19/pilot_i2 and transfer/T21/pilot_i1 (both PASS). T20 and T36 are out (A45 c / A52). Never trained.
Rows are taken as generated (no relabel, no edit). Excluded first: rows G5-H dropped (G5H_FINAL drop_rows) and rows whose
meta names a G5-H-quarantined template. Then 300 rows per family: whole units (call_id), seeded shuffle (seed 20261013),
a unit that would overshoot 300 is skipped. Output order: family, then selection order. Prints counts and sha256 only."""
import hashlib, json, random, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]                 # lean/c2_build
OUT = HERE.parent / "data" / "c2_transfer_dev.jsonl"
SRC = (("T19", "pilot_i2"), ("T21", "pilot_i1"))
N, SEED = 300, 20261013

def jl(p): return [json.loads(l) for l in open(p) if l.strip()]

out, rep = [], {}
for fam, pil in SRC:
    d = HERE / "transfer" / fam / pil
    rows = jl(d / "rows.jsonl")
    fin = json.load(open(d / "g5h" / "G5H_FINAL.json"))
    quar = set(fin.get("quarantined_templates") or [])
    dr = fin.get("drop_rows") or []
    drop_ids = set(dr.keys()) if isinstance(dr, dict) else {x if isinstance(x, str) else x.get("id") for x in dr}
    def uses_quar(r):
        s = json.dumps(r["meta"], sort_keys=True)
        return any(q in s for q in quar)
    keep = [r for r in rows if r["id"] not in drop_ids and not uses_quar(r)]
    assert all((r.get("meta") or {}).get("dev_only") and r["meta"].get("family") == fam for r in keep), fam
    units = {}
    for r in keep: units.setdefault(r["call_id"], []).append(r)
    keys = sorted(units); random.Random(SEED).shuffle(keys)
    sel = []
    for k in keys:
        if len(sel) + len(units[k]) <= N: sel += units[k]
        if len(sel) == N: break
    assert len(sel) == N, (fam, len(sel))
    out += sel
    rep[fam] = {"src": f"transfer/{fam}/{pil}/rows.jsonl", "rows_in": len(rows), "g5h_dropped": len(drop_ids & {r['id'] for r in rows}),
                "quarantined_templates": sorted(quar), "rows_after_exclusion": len(keep), "rows_selected": len(sel),
                "units_selected": len({r['call_id'] for r in sel}), "qtype": dict(Counter(r["qtype"] for r in sel)),
                "role": dict(Counter(r["role"] for r in sel)), "gold_top": Counter(r["gold"] for r in sel).most_common(3)}
ids = [r["id"] for r in out]; assert len(ids) == len(set(ids))
OUT.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=False) + "\n" for r in out), encoding="utf-8")
sha = hashlib.sha256(OUT.read_bytes()).hexdigest()
print(json.dumps({"file": str(OUT), "rows": len(out), "sha256": sha, "seed": SEED, "families": rep}, indent=1))
