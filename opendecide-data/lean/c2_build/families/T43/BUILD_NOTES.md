# T43 PATCH-VERDICT: build notes (15 Oct 2026, Sonnet 5.5 agent; nothing on disk but code, G0 and a numbers-only QC_METRICS.json)

## What exists (families/T43/)
`G0_SPEC.md` (G0-lite, sha256 daaa...75e8dffe, frozen in `plugin.G0_SHA256`), `plugin.py` (kit Plugin, samplers S1-S5, `sealed_rows`), `templates.py`
(14 six-line templates + 4 module reducers x 9 stages; S5-only: `digit_total`, `lead_trim`, `tail_top`), `executor.py` + `exec_child.py` (solver A,
hermetic CPython 3.12, two runs), `patching.py` (strict unified-diff applier), `repairs.py` (repair family R*, A side), `solver_b.py` + `interp_b.py`
(solver B: own parser, diff applier, AST interpreter, docstring-expression oracle, own R*), `probes.py`, `qc_build.py` (parallel in-memory QC),
`run_pilot_i1.py` (`--dry-run`, `--n`, `--no-g15`; refuses to write rows without `--after-freeze`), `test_t43.py` (9 tests), `QC_METRICS.json`.
Heads: ll (6 numbered lines, none 5.3%), lf (5-8 functions, none), pv (A/B/C, D 4.1% of pv rows). Mix: pv 50% (S1 lines, S4 modules), ll 25%, lf 25%.
Bugs: AST mutants (T42 `mutate.py`, imported; HELD_OUT_OPS = swap_args, wrong_slice_bound, the same two as T42). Gold: execution (tests, G0 grid, 240 seeded cases
per function vs the original; strict applier for D). Solver B never sees the original: the docstring `Equals <expr>.` is its oracle.

## A45 pre-freeze check (in memory; 5,202 QC rows in 9 parallel shards of `qc_build.py`; no row file)
| Gate | Value | Bar | Pass |
|---|---|---|---|
| G0-lite + exemptions listed (G0 section 6) | written | exists | yes (orchestrator must confirm exemptions) |
| HELD_OUT_SAMPLERS (S5: ops, layouts boxed/tabs) unreachable from S1-S4 | test_held_out_unreachable | pass | yes |
| solver A == B on 2,000 specs (S1-S5, 3 heads) | 0 mismatches; appliers agree | 100% | yes |
| two execution runs agree | `confirm=True` on every shown program/patch | all rows | yes |
| G6 pooled (4 views x LR/GBT) | max a_q gbt .232, b_opt gbt .2364, c lr .2388, d_meta gbt .2538 vs chance .2392 | <= chance + 2 pp | yes |
| G6 per head (n >= 1,000): lf, pv | pass | same | yes |
| G6 per head: ll (n = 1,305) | gbt .1816 (a, b, c), d_meta gbt .1962 vs .1583 | same | **NO** (+2.3 / +3.8 pp) |
| G7 | 299 tests, 0 fails | 0 | yes |
| G10 | pass (gold position, rank, abstain, longest) | pass | yes |
| options-only probe | ll lr -4.07 (inverse; fails), ll gbt +1.91, lf pass, pv pass (-1.3/+0.8) | +-3 pp | **NO** (ll lr) |
| formatting-only probe | ll gbt +7.2, lf gbt +3.14, pv gbt +4.38 (lr all within +-1) | +-3 pp | **NO** |
| diff-size probe (added/removed, hunks, token edit, AST delta) | cv acc lr .3468 / gbt .3476 vs majority .3348; AUCs .47-.53 | <= maj + 3 pp | yes |
| reseed audit (3%, independent random stream + other hash seed/seeded cases) | 0 flips of 64 (re-exec); regeneration compares line/position/label | <= 1% | yes |
| determinism, PYTHONHASHSEED 1 vs 2 | identical row hashes (20 rows) | equal | yes |
| prompt tokens (Qwen tokenizer, instructions x2) | mean 780.1, max 1,198 | <= 800 / 2,000 | yes |
| rows per card | 468 cards, max 28 | <= 64, >= 28 specs | yes |
| D share / none share | 4.11% of pv rows / 5.31% of ll+lf rows | <= 5% / ~5% | yes |
| G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options (200-row dry run with G15) | 0 failures | 100% | yes |
G4 relations (never emitted): reorder test listing, add 1 passing test, add 2 passing tests, pv: append unused function. The dry run's G6 (n = 200) and overlay
(twin/equiv share 0: choice-only family, as T42) fail by construction; the 5,000-row G6 binds.

## Open items (fix iteration 1 candidates; generator and sampler only)
1. **Formatting-only GBT and ll per-head G6 are a template/label prior, not a text artefact.** P(bug line | template) and P(label | template) are
   still not flat: the ambiguity guard and observability rules make some (template, line) pairs rare (feasibility runs: `scaled_cap` line 4 .38,
   `alt_sum` line 4 ~.7, `band_count` line 5 .83) and C patches fail more often (224 attempts). Fix: draw the ll template with weight 1/feas(T, j) from the measured table, and
   widen the C core edits; then re-run `qc_build.py`. 2. ll options-only LR -4.07 is a CV artefact of balanced classes (it flips sign with n); re-test after 1.
3. Haiku surface text: none (program text only); wordings are admitted by program stand-ins. 4. G5-H/G3-H pending (orchestrator). 5. `families/T42/mutate.py`
   is imported (not copied): a T42 operator change moves T43 rows; `interp_b.py` is a vendored copy. 6. Kit candidates: CHOICE_ONLY flag for overlay twin/equiv share;
   runtime FAMILIES registration (done in plugin). 7. Cost: ~3 s per row single process; 5,200 rows take 18 min on 9 workers.
8. Twins, equiv partners, complements, attack lines undefined for T43 (choice rows, no slots).

## Commands (from lean/c2_build, venv python -B)
- Tests: `T43_N_AB=2000 T43_WORKERS=9 .venv python -m pytest -q -p no:cacheprovider families/T43/test_t43.py` (A==B parallel; ~12 min).
- QC / probes: `python -B families/T43/qc_build.py --rows 5200 --workers 9 --no-g15 --out families/T43/QC_METRICS.json` (`--quick` skips gates).
- Dry run: `python -B families/T43/run_pilot_i1.py --dry-run --n 200` (add `--no-g15` to skip G15). No rows are written without `--after-freeze`.
- **Sealed entry point:** `from families.T43.plugin import sealed_rows; sealed_rows(n, start_seed)` returns n (Spec, RenderedRow) from S5 only (held-out ops swap_args /
  wrong_slice_bound, layouts boxed/tabs, heads ll/lf/pv-line/pv-module equally, D and none shown as in training). The sealed agent writes under `lean/ohs_ac_sealed/`;
  this build never does. Rows with a failing `solve_a` raise ContractError: drop the seed (never relabel).
