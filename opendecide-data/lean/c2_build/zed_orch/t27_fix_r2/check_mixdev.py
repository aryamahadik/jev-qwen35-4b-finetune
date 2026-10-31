"""Is mixdev_S5.jsonl (base 68,000,000) unchanged by the fix? Builds it with and without overlay.patched() and compares the row ids
with data/c2_parts/T27/out/mixdev_S5.jsonl (read only). Prints counts and booleans only."""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
for p in (str(C2), str(HERE)):
    sys.path.insert(0, p)
import gen_full_c2 as G
import overlay as O
inst = [json.loads(l)["id"] for l in open(C2.parent / "data" / "c2_parts" / "T27" / "_hold_batch4" / "mixdev_S5.jsonl")]
src = G.quarantine_sources("T27")
banned = set().union(*map(set, src.values()))
res = {"installed_rows": len(inst)}
import contextlib
mode = sys.argv[1] if len(sys.argv) > 1 else "with_overlay"          # one family open per process (install_vocab runs once)
for name, ctxm in ((mode, (lambda: O.patched(wordings=False)) if mode == "with_overlay" else None),):
    cm = ctxm() if ctxm else contextlib.nullcontext()
    with cm:
        with G.loader_patch("T27"):
            with G.PL.open_family("T27") as kit0:
                kit, _x = G.apply_exclusions(kit0, banned)
                rows, rep = G.build_mixdev(kit, G.MIXDEV_N, seed_base=68_000_000)
    ids = [r["id"] for r in rows]
    res[name] = {"rows": len(ids), "ids_equal_installed": ids == inst, "n_equal_positions": sum(a == b for a, b in zip(ids, inst))}
print(json.dumps(res))
