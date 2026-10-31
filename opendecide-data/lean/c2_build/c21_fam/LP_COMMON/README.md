# LP_COMMON and the L-P lane (code only, no rows)

Shared library for the lane L-P families: names (namespace.py manifest v1.2 via `ns.py`, TRAINING salt), names guard, wording pool check, plan helpers (15% oversampling, ladder level),
set-level gate helpers, the check-at-generation pipeline (`pipeline.py`: answer checks, solver B plug point `solver_b(b_view)`, render round trip, token cap 1,536, PII scrub, G13 stamp
in batches <= 500, GV5 whole-group retirement, 1% fix trigger), a safe interpreter for the sandbox DRY RUN (`pyeval.py`, `pyshim.py`: an AST walker, no exec of generated text), and the
executor interface (`sandbox_iface.py`: SimExecutor for tests, JobFileExecutor for the od-sbx1 two-phase flow).

Families built: T63 (NEAR, EXISTS, LIC), T66 (MERGE, SEMVER, MSG; Python), T67 (GATE, REASON, TIER), T65 (VULN generated half; Python). T62 is held (see T62/NOT_BUILT.md).
Each has: generator, Solver A, round trip, schema (`b_view`), checked.py (`run(...)` with a stamp hook), gates.py, dryrun.py, tests, ROW_SCHEMA.md, SHAS.json.

## Hard facts

* A production run needs: the real wording pool (the test pool is refused), the real Solver B (SolverBRequired otherwise), the real G13 stamp hook (RefusingHook is the default), the
  od-sbx1 executor (SimExecutor is refused), and the real fixtures (stdlib export, licence table, T67 lock table; the fixtures here are flagged and refused for production).
* `python3 -m pytest <FAM>` from this directory runs each family's CPU tests. Nothing writes rows; the dry runs are in memory.

## Open items (for the orchestrator)

1. Solver B for T63, T65, T66, T67 (separate sessions; see each ROW_SCHEMA.md).
2. Opus items: T63 licence table; T67 lock table (draft flagged), X08 pin_policy follows the digest lever (flagged), X08 reason difference, REVIEW share edge, CF-7 deviation (T66),
   CH-4 and CH-7 never realised (T66), T66 K5 stratum design conflict.
3. Not built: MAL (T63), MSG-REAL (T66), the Juliet slice (T65, L-R), T62, JS / Go slices.
4. Gate shortfalls on the dry-run fixtures (documented, not tuned): ladder composition (T63, T65, T66), probe power at small n, T63 K8, T66 K4/K5/K6/K19, K11 language quotas,
   T65 lexical probe (plain pairs separable by sanitiser keywords; decoy and no-hard kinds dilute it).
5. PyEval/pyshim fidelity against the real image: needs a smoke run in od-sbx1 before the first dynamic row (the stand-in modules are my model of the stdlib behaviour).
6. The L-0 slot mapping (`ns.LOCAL_SLOT_TO_KIND`) is local: confirm against the L-0 manifest owner.

## Build-skeptic changes (fresh Sonnet 5.5 high, Sun 18 Oct; no rows built, no model called, nothing executed)

Fixed (each has a CPU test in `tests/test_skeptic_*.py`; the original tests are unchanged):
1. `pipeline.verdict_class`: stamp verdicts FAIL CLOSED. An unknown verdict word, a `hit` that lists no hit entry, a malformed hit entry or an unknown `exempt` value was a pass; now an error.
2. Head rows (T65 CWE, T67 REASON / TIER) get the full `check_row` (solver A, solver B, round trip, names, token cap, PII, leak scan, spans ...) not only the options check.
3. `pipeline.stamp_in_batches`: the stamp service gets <= 500 rows per call (a batch could overshoot); `DenyListRequired`: a production run needs the shared deny-list program;
   `production_pins_pending`: a production row with no toolchain provenance (PENDING, the stand-in "sim" image) is refused; rows now record `manifest.pins` (T63 EX-B image + export sha,
   T65 / T66 the executor image of the witness, "n/a:..." where no toolchain is involved).
4. Solver B's view: `row_id` is opaque (`util.opaque_id`; the member letter `-a` was the YES / BREAKING member of every pair in T63, T65, T66); T67 `sub_block` is the carrier (the block
   ids P-d, P-e, K-d, C-d are all-ALLOW / all-BLOCK); T65 CWE head rows show `sub_block = "CWE"` (it was the gold class).
5. T65: NS-1 pairs of the three static classes rendered IDENTICAL code under opposite labels (33 of 342 pairs); fixed (identity helper) and the builder now rejects identical twins; gates K2
   (twin integrity) and K15 (lint) added. CWEC-89 functions create their own two-row table (the real sqlite3 has none in a fresh in-memory database); the CWEC-22 job ships its served
   files (`config.FIXTURES`), the runner changes into the job directory.
6. T63: EX-A1 query strictly inside the shown range for both labels and a one-edit neighbour listed on every single row (K8 AUC 0.61 -> 0.58); a real export / licence table must declare its
   sha256; K2 provenance and the K10 mixed-pair share are now computed.
7. T66: an unsound MERGE witness (not 3 identical runs, crash exit code) is no label (it read as NO). T67: head rows count tokens with the family counter; the P-d decorations no longer put
   firewall_rule / iam_policy items only into ALLOW rows.
8. Wording pools: T63-Q-NEAR (asked "is a near name present?", the gold is lookalike-or-confusion), T65-Q-VULN (7 frames asked the converse of YES = flawed) and T66-Q-SEMVER (10 yes/no
   frames for BREAKING / SAFE options) were repaired; pool guards (`pool_problems`) now refuse such pools in a production context. The 19 T66 MSG change-form wordings are the shared
   QUESTION frames, not commit messages: the guard refuses the pool until real message wordings exist (the MSG label is unlearnable with them).

Still open (builder / Opus / orchestrator): see the build-skeptic report to the orchestrator (solver B absent for all four; MSG message wordings; K4 / K6 length probes on T66 by design;
PLAN_JSON has no X05 / X06 rows; PyEval fidelity smoke run; T67 K5 design conflict; real stdlib export for the EX-B probes).
