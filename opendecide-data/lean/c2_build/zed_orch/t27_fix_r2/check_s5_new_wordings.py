"""Is mixdev_S5.jsonl (base 68,000,000) unchanged when the overlay ADDS new training wordings (ch_next and yn_beyond)? Needs the
fabricated payload that `smoke_new_wordings.py make` writes (scratch/smoke_payload.json; never admitted_wordings.json). Builds the
150 S5 rows with overlay.patched(extra=payload) and compares their ids with the installed (or held-aside) mixdev_S5.jsonl, read
only. S5 draws held-out wordings (min-hash, unchanged) so the new training wordings must not move a row. Counts only.
  smoke_new_wordings.py make ; check_s5_new_wordings.py ; smoke_new_wordings.py run     (three processes, from lean/c2_build)"""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
for p in (str(C2), str(HERE)):
    sys.path.insert(0, p)
import gen_full_c2 as G
import overlay as O
pay = json.loads((HERE / "scratch" / "smoke_payload.json").read_text())
DST = C2.parent / "data" / "c2_parts" / "T27"
installed = next(p for p in (DST / "out" / "mixdev_S5.jsonl", DST / "_hold_batch4" / "mixdev_S5.jsonl") if p.is_file())
inst = [json.loads(l)["id"] for l in open(installed)]
src = G.quarantine_sources("T27")
banned = set().union(*map(set, src.values()))
with O.patched(extra=pay):
    with G.loader_patch("T27"):
        with G.PL.open_family("T27") as kit0:
            kit, _x = G.apply_exclusions(kit0, banned)
            rows, rep = G.build_mixdev(kit, G.MIXDEV_N, seed_base=68_000_000)
ids = [r["id"] for r in rows]
by_q = {}
for w in pay["wordings"]:
    by_q[w["qform"]] = by_q.get(w["qform"], 0) + 1
print(json.dumps({"new_wordings_in_overlay": by_q, "installed_rows": len(inst), "rows": len(ids), "ids_equal_installed": ids == inst,
                  "n_equal_positions": sum(a == b for a, b in zip(ids, inst))}))
