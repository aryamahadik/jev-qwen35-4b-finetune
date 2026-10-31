"""T28 iteration-1 determinism probe: build the first N rows in memory and print one sha256 (run under two PYTHONHASHSEEDs)."""
import hashlib, json, sys
sys.dont_write_bytecode = True
sys.path.insert(0, ".")
import pilot, pilot_loaders as PL
n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
with PL.open_family("T28") as kit:
    b = pilot.build_pilot(kit, n, log=None, run_g15=False)
rows = [i.row for i in b.infos]
h = hashlib.sha256("".join(json.dumps(r, ensure_ascii=False, sort_keys=False) + "\n" for r in rows).encode()).hexdigest()
print(len(rows), h)
