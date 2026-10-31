"""T46 G-TPL (A59 e): the family's templates (pool records + program literals of its code files) against the OHS-4 and OHS-AC
template hashes, by RUNNING the C2-side checkers (gtpl_check.py, gtpl_check_ac.py). Prints counts and C2 ids only."""
import sys, json
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2))
import g13_c2 as G  # noqa: E402
root = C2 / "families" / "T46"
ilog = G.LinkGuardedInputLog()
pu, _ = G.pool_units("T46", root / "pools", ilog)
G.CODE_FILES = G.CODE_FILES + ("tables.py", "policy.py", "audits.py", "probes.py")
cu, _ = G.code_seed_units("T46", root)
recs, back = G.gtpl_records({"T46": pu + cu})
a = G.run_checker(G.GTPL_TOOL, "--templates", recs)
b = G.run_checker(G.LEAN / "ohs_ac_sealed" / "tools" / "gtpl_check_ac.py", "--templates", recs, extra=["--min-shared", "1", "--parts", "all"])
def pack(x):
    return {k: x.get(k) for k in ("status", "exit", "manifest_verified", "complete", "counts", "hit_ids")}
print(json.dumps({"pool_units": len(pu), "code_units": len(cu), "templates": len(recs), "ohs4": pack(a), "ohsac": pack(b)}, indent=1))
