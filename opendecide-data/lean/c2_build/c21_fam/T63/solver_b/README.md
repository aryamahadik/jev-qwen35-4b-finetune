# T63 solver B (independent program, G1)

Written from `G0_LITE.md` (incl. the Opus batch-1b block), `G0_APPROVALS_v32.md` and `ROW_SCHEMA.md` only. It never sees solver A, the spec, the gold or the
generator's meta. Stdlib only, reads no file at run time.

## Method (how it differs from A)
A is a forward function over the generator spec. B PARSES THE RENDERED ROW and re-derives the label with its own code:
* NEAR: reads the definitions block (and abstains if its clauses differ from the rule B implements), the registry legend, the project card, the snapshot in any of the
  five formats (csv / tsv / pipe / json / kv, picked from the `Snapshot (...)` line) and the proposed command. Near-name relations NM-T1..T7 are PAIRWISE
  PREDICATES on two strings (`rel.py`, ROW_SCHEMA 2a pins); B never generates candidate edits. T8 is its own first-match clause (T63-M1): a name on the card's
  reserved list is decided by the four conditions alone (no fall-through to T1..T7); otherwise established / publisher / fork-edge / strictly-younger-class rules
  over entries of the QUERY's registry.
* EX-A1 / EX-A2 / EX-B1: membership in the RENDERED complete listing. Absence is a NO only inside the stated range; a name outside it (cannot be proved) -> abstain.
  The asked registry / module.symbol is read from the question. EX-B1 and EX-B2 take lang / module / name from `witness_inputs`.
* EX-B2: membership of the witness name in the sha-bound stdlib export (the L-0 image record), passed in as plain data `{lang: {module: [names]}}` + its sha.
* EX-B1 additionally REQUIRES that export and sha (Opus ruling Q3a, 18 Oct): the label read off the shown list must equal the export's membership
  (`b1_export_mismatch`), and the module must be in the export (`b1_export_module_unknown`), else abstain.
* LIC: reads the four axes from the rendered card and looks the cell up in the hashed table, passed in as plain data `{(dep, project, "LC-USE-n", "LC-DIST-n"): label}`
  (phrase->id order = G0-lite 2.3 order) + its sha. No source configured -> abstain; B never guesses.
* The sha check is MANDATORY (Opus ruling Q3a, 18 Oct; before, it ran only "if the sha is not None"). For EX-B1, EX-B2 and LIC, B abstains (the pipeline then
  drops the row as `B_abstain`, counted) when: the source is missing (`no_export_source` / `no_table_source`); no sha is configured (`no_export_sha` /
  `no_table_sha`); the row's witness carries no sha (`witness_export_sha_missing` / `witness_table_sha_missing`); the witness sha differs from the configured
  one, i.e. the sha recorded by the L-0 image record / the Opus table record (`export_sha_mismatch` / `table_sha_mismatch`); or the source or its sha is a
  FIXTURE (`fixture_export_source` / `fixture_table_source`): declared with `fixture=True`, or a sha string that names itself fixture / standin / stand-in /
  placeholder / dummy / test. Only an explicit `allow_fixture=True` (the build-stage CPU harness, `agree.py`) lets a fixture through, the result then carries
  `"fixture": True`, and that run is build-stage evidence only (G0-lite :172), never production K1. A real sha256 hex string is never mistaken for a fixture.
* The option letter is recovered from the rendered options text and cross-checked with the b-view `options`.

## Files
`rel.py` relation predicates; `near_b.py`, `exists_b.py`, `lic_b.py` per head; `common.py` options / helpers; `hook.py` plug points; `agree.py` in-memory harness
(the only file that imports the generator side); `tests/` (pytest, CPU); `agreement_log.json` counts only; `SHAS.json`.

## Use
```
hook.solver_b(bview)                                    # module level; sources via hook.configure(exports=, export_sha=, table=, table_sha=)
hook.make_solver_b(exports=..., export_sha=..., table=..., table_sha=...)   # closure, e.g. checked.run(..., solver_b=that)
# every source needs its sha; fixture sources need  fixture=True, allow_fixture=True  (build-stage harness only)
```
Returns `{"status": "ok"|"abstain"|"error", "label": ..., "letter": ..., "reason": ...}`; abstain / error carry `label=None`.
Without `exports` / `table` and their shas, EX-B1 / EX-B2 / LIC rows abstain (the pipeline then drops them as `B_abstain`).
`hook.table_from_label_fn(fn, deps, projects)` builds the plain table from any `fn(dep, project, use_id, dist_id)`.

## Run
```
cd c21_fam/T63/solver_b
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest tests -q
PYTHONDONTWRITEBYTECODE=1 python3 -B agree.py --rows 6000 --seeds 101,102,103 --out SCRATCH/report.json --log agreement_log.json [--pool real|test]
python3 -B agree.py --shas                               # rewrites SHAS.json
```
`--rows` is per seed (the generator oversamples by 15%). The harness uses the family's own FIXTURE stdlib export (non-production; the L-0 image-record export does not exist yet), so EX-B1 / EX-B2 run with
`fixture=True, allow_fixture=True` (build-stage evidence only). LIC rows come from the REAL hashed T63-LIC-TABLE (`zed_orch/c21/l0/T63_LIC_TABLE.json`) and B
runs on them with `fixture=False`: B's plain table is read straight from that file (not from the generator's table object) and B's sha is the content sha
the L-0 record `T63_LIC_TABLE_RECORD.json` states (`--lic-fixture` restores the old fixture table). Production K1 is the per-row read at creation on the real sources (the L-0 image-record export, the hashed Opus table).
