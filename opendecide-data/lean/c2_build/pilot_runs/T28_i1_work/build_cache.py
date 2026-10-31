"""T28 i1 diagnostic: build N rows in memory (no write) and pickle (infos, stats) for the analysis scripts."""
import pickle, sys
sys.dont_write_bytecode = True
sys.path.insert(0, ".")
import pilot, pilot_loaders as PL
n, out = int(sys.argv[1]), sys.argv[2]
with PL.open_family("T28") as kit:
    b = pilot.build_pilot(kit, n, log=lambda m: print(m, file=sys.stderr, flush=True), run_g15=False)
print(b.stats["units_attempted"], b.stats["drops_by_gate"], b.stats["drop_examples"])
try:
    with open(out, "wb") as f:
        pickle.dump((b.infos, b.stats), f)
    print("pickled infos")
except Exception as e:  # noqa: BLE001
    print("pickle of infos failed", repr(e)[:300])
    with open(out, "wb") as f:
        pickle.dump(([i.row for i in b.infos], b.stats), f)
