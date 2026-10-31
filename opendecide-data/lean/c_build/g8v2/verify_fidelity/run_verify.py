"""Run g8_aflite.family_report end to end with every write redirected into verify_fidelity/ (OUTDIR, CACHE)."""
import hashlib, sys
from pathlib import Path
sys.dont_write_bytecode = True
V = Path(__file__).resolve().parent
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/common")
import g8_aflite as G  # noqa: E402
fam, want, jobs, spread = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
G.OUTDIR = V; G.CACHE = V / "cache"
pool = G.LEAN / f"c_src/{fam}/out/candidates_r1.jsonl"
sha = hashlib.sha256(pool.read_bytes()).hexdigest(); print("pool sha", sha, flush=True)
assert sha.startswith(want), "pool changed; abort"
G.family_report(fam, str(pool), V / f"{fam}_verify.json", jobs, n_spread=spread)
print("DONE", flush=True)
