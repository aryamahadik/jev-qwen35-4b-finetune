"""T27 diagnostic (not a gate): pilot.g6_choice on a dump of ch_next rows (context = card + rules + state)."""
import json, sys
sys.dont_write_bytecode = True
sys.path.insert(0, ".")
import pilot
rows = [json.loads(l) for p in sys.argv[1:] for l in open(p)]
out = []
for r in rows:
    if r["qtype"] != "choice":
        continue
    rules, _, q = r["instructions"].rpartition("\n\n")
    ctx = "\n".join(x for x in (r.get("card") or "", rules, r["state"]) if x.strip())
    out.append(pilot.RowInfo(r, None, None, 0, q, ctx, None))
res = pilot.g6_choice(out)
print(json.dumps(res, indent=0))
