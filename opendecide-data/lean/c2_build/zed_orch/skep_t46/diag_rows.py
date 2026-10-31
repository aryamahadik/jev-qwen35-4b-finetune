"""Skeptic diagnostic for T46 (A59 review): a fresh 6,000-row QC-style build at a NON-registered seed base; writes ONLY label-side metadata
per yes/no row (qform, asked class, true class, answer, twin kind, sampler, seed pair) so the proposal-correctness balance by asked class
can be analysed offline. Diagnostic only. $PY zed_orch/skep_t46/diag_rows.py SEEDBASE OUT.json"""
import sys, json, time
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import gen_full_c2 as G
sb, out = int(sys.argv[1]), Path(sys.argv[2])
with G.loader_patch("T46"):
    with G.PL.open_family("T46") as kit0:
        kit, xrep = G.apply_exclusions(kit0, set())
        b = G.pilot.build_pilot(kit, 6000, seed_base=sb, run_g15=False)
rows = []
for i in b.infos:
    r = i.row; t = r["meta"]["t46"]
    rows.append([r["qtype"], r["meta"]["qform"], t["ask"], t["cls"], r["gold"] if r["qtype"] == "noul" else None,
                 r["meta"].get("twin_kind"), r["meta"]["sampler"], r["meta"]["seed"], r["meta"]["card_id"], t["arm"], t["wf"], t["typ"]])
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({"seed_base": sb, "cols": ["qtype", "qform", "ask", "cls", "gold", "twin_kind", "sampler", "seed", "card", "arm", "wf", "typ"], "rows": rows}))
print("ok", sb, len(rows))
