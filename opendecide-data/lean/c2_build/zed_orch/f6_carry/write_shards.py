"""F6 carry: write the C1 crowd-read shards of the v2 candidates (same call as c2_select.cmd_tasks --write-shards, which skips
carry pools). Output data/c2_crowd_shards/F6 (new folder). Does NOT touch crowd_tasks_c2.json. Counts only."""
import sys
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
import c2io, c2_select as sel
sys.path.insert(0, str(c2io.LEAN))
import shard_golden as sg
ilog = sel.LinkGuardedInputLog()
rows, _, shas = sel.family_inputs(ilog, "F6")
bad = c2io.candidate_problems("F6", rows)
print("candidate_problems:", bad)
if bad: raise SystemExit("candidates refused")
sd = sel.SHARDS / "F6"
assert not sd.exists() or not any(sd.iterdir()), f"{sd} not empty"
man = sg.write_shards(rows, sd, sel.SHARD_ROWS, {"purpose": "C2 crowd read F6 (carry v2)", "seed": sel.SEED, "candidates_sha256": shas["candidates_sha256"]})
print("rows", len(rows), "shards", len(sg.shard_files(sd)), shas)
