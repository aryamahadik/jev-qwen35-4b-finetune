# T43 w9 (16 Oct, Sonnet 5.5): patch size label-blind by construction

Change (plugin.py `_patch`, `full_sig`, `cheap_sig`; G0_SPEC.md section 4, sha ccb153b0...; backups in _backup_w9/): per attempt a candidate pool is built
for EACH of A, B, C on the same program and bug (72 tries each, 0-2 rewrites drawn per candidate). Signature = (added, removed, hunks, patch lines, token
edit, token hunks, AST delta) = exactly what probes.size_features reads. Allowed set = signatures all three verdicts reach AND execution confirms for all three
(grid judge). The row's signature = first allowed one in hash order of (row key, salt, signature). No common signature fails the attempt for every label alike.
Only the chosen candidate of the row's label gets the seeded re-judge (0 disagreements seen). The w8 hunk-reference rule is gone. Nothing relabelled, no bar lowered.
Costs: ~0.8 s per pv row single process unloaded; the VM was at load 23-27 (other agents), so the 10,206-row gated build took 9,643 s.

Results (10,206 rows, seed bases of qc_build; 5,999-row prefix = the first 857 rows of each of 7 shards): see QC_METRICS_w9a_gated_10k.json (gated),
QC_METRICS_w9a_10k.json (quick, same rows). diff-size probe: 10,206 rows lr 0.3279 / gbt 0.3399 vs majority 0.334 (-0.6 / +0.6 pp); prefix 0.3411 / 0.3317 vs 0.3355.
Per-head G6: pass at 10,206 (ll gbt max +1.4). At the 5,999-row prefix ll gbt +2.44 (n = 1,498, a_question / b_options / c_card the same cell): FAIL at 6k, pass at
10k; the ll rows are identical to w8q (patch code does not touch ll). A48 (d): the largest >= 5,000-row superset build binds.
Tests: 16 passed (A == B on 2,000 specs, determinism, reseed, timeout, two new tests: signature equals probes.size_features; on one program A, B, C get the
identical signature).
