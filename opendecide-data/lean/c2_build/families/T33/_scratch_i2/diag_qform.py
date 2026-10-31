import sys, json
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import pilot, pilot_loaders as PL
with PL.open_family("T33") as kit:
    b = pilot.build_pilot(kit, 6000, run_g15=False)
ch = [i for i in b.infos if i.row["qtype"] == "choice"]
for q in ("ch_failed_check", "ch_claim_verdict", "ch_bad_claim"):
    sub = [i for i in ch if i.row["meta"].get("qform") == q]
    r = pilot.g6_choice(sub)
    print("QF", q, len(sub), {v: r[v] for v in r if isinstance(r[v], dict) and "lr" in r[v]}, r.get("chance"), flush=True)
