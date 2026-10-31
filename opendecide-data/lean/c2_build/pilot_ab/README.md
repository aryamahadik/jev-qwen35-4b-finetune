# A42-D item 4: single-family pilot harness (T40-T45)

Rules: PREREG_FINAL A42-D 4.1-4.4 and 12.6, A37 (i). Built 15 Oct. No GPU run, no Modal call, no network was used to build or test it.
Every family is piloted alone: one short LoRA pass from C1 (adapter sha256 507d1c29...) on its 1,500 new rows (no replay),
recipe of `runs/q35_4b_c_r1.json` (LR 5e-5, batch 16, r16/alpha 32, 5% warm-up + cosine, one real pass, seed 20261013,
lam_inv 1, sym_cons, perm_twin 0.3, kd guards measured on the rows, no snapshots). There is no re-pilot.

## Files
| File | Role |
|---|---|
| `common.py` | constants and the bars (never loosened); `refuse_path` (never-open paths) |
| `make_config.py` | stages the family's 1,500 rows, writes `configs/<FAM>.json`; `epochs` = exactly one pass (replay_steps); prints cost; `l4_train_argv` |
| `modal_pilot.py` | Modal launcher (own app; data mount = the two staged files only; C1 sha check in the container) |
| `l4_reads.sh` | od-l4 sequence: `fetch`, `push`, `read-c1`, `read`, `pull` (nothing runs by itself; `plan FAM` prints it) |
| `verdict.py` | the three rules -> `families/<FAM>/pilot_ab/PILOT_AB_VERDICT.json` |
| `tests/test_pilot_ab.py` | 31 CPU tests on fabricated predictions (about 2 min) |

## Commands (per family; run from `lean/c2_build`)
```
PY="../../.venv/bin/python -B"; M=../../.venv/bin/modal
export PILOT_FAMILY=T40 MODAL_PROFILE=mahadikarya2
# 0. CPU: stage + config (refuses != 1,500 rows, duplicate ids, a relation outside the rows, an id shared with a dev file)
$PY pilot_ab/make_config.py --family T40 --rows <T40 1500-row train jsonl> --rels <T40 relations jsonl> \
    --dev-files <own dev jsonl> <g-proxy jsonl>
# 1. free checks (config, staged sha, trainer code = C1's train_meta code hashes, C1 adapter on the volume, cost)
$M run pilot_ab/modal_pilot.py::pilot_check
$M run pilot_ab/modal_pilot.py::pilot_upload_init        # only if pilot_check says the init adapter is missing; once per account
# 2. THE PAID STEP (one H100, about 8 min, about 0.55 USD): needs the orchestrator's go
$M run --detach pilot_ab/modal_pilot.py::pilot_spawn
# 3. the free L4 (Google credit)
pilot_ab/l4_reads.sh fetch T40 ; pilot_ab/l4_reads.sh start
pilot_ab/l4_reads.sh push T40 <own dev> <g-proxy rows> <g-proxy relations>
pilot_ab/l4_reads.sh read-c1 T40        # once for all families: C1 reads the 9 dev splits, the G-proxy and each own dev
pilot_ab/l4_reads.sh read T40 ; pilot_ab/l4_reads.sh pull T40 ; pilot_ab/l4_reads.sh stop
# 4. verdict (CPU)
$PY pilot_ab/verdict.py --family T40 --reads-dir pilot_ab/reads/T40 --own-rows <own dev> \
    --gproxy-rows <g-proxy rows> --gproxy-rel <g-proxy relations> --gproxy-sha256 <hash recorded before C1's first read>
```
Own dev and G-proxy are pushed as splits `pab_own_<FAM>` and `pab_gproxy` (+ `pab_gproxy_relations`); nothing is written into `lean/data`.
Tests: `nice -n 10 $PY -m pytest -q -p no:cacheprovider pilot_ab/tests`.

## What is read, and the readout
C1 and the pilot are each read by `od_gcp.py predict` with C1's own prompt (layout `schema_branch_mark`, style from the adapter's
train_meta, pinned base revision 851bf6e8, no forced override: the A18.2 readout) and `--tta-choice`: choice rows are read twice
(given and reversed option order) and averaged, yes/no rows once. Splits: own dev (300), the 9 gate dev splits (8,143 rows;
`tb_mixtral`, 1,087 rows, is dropped from the pool, leaving the 7,056 retention rows as `gate_dev` D1 pools them) and the G-proxy.
`verdict.py` refuses unless both models come from one machine/software/revision/chat-template, with `tta_choice` only, no `perm_seed`,
C1's adapter sha256 = 507d1c29..., every row predicted by both, own n = 300, existing n = 7,056, G-proxy >= 2,000 rows and >= 150
complement pairs, and (when given) the G-proxy file hash equal to the recorded one. Refusal exits 2 and writes nothing.

## Verdict rules (A42-D 4.2, 4.3; all point values in percentage points of accuracy, pilot minus C1)
1. Own dev gain >= +2.0 (6 of 300 rows is exactly +2.0 and passes).
2. Existing dev (pooled micro accuracy, 7,056 rows) change >= -0.5 (a drop of up to 0.5 passes).
3. G-proxy: 95% paired bootstrap CI, 10,000 resamples, seed 0 (`gate_dev.group_boot`, the pre-gate's own), clusters = source
   documents with each complement pair merged into one cluster (union-find). Rejected iff the CI upper bound < -0.5. No point rule.
KEEP only if (1), (2) and not-rejected (3); otherwise MOVE_TO_C3. The JSON also holds per-split and per-type accuracies, report-only
CIs for own and existing dev, input sha256s and warnings.

## Expected wall time and cost per family
| Step | Where | Wall time | Cost |
|---|---|---|---|
| make_config, pilot_check, verdict | laptop CPU | about 1 min, 1 min, 1 min | 0 |
| Train, 1,500 rows = about 94 steps (H100, 2.9 s/step, +3.5 min start-up and save; +about 5 min once per account for the base download) | Modal mahadikarya2 | about 8 min | **about 0.55 USD** (0.30 compute only; 0.61 if rows average 900 tokens) |
| Reads of one adapter: model load 3 min, 9 splits about 40 min (choice rows doubled), G-proxy about 10 min, own dev about 2 min | od-l4 | about 55 min | 0 Modal |
| C1 reads, once for all families | od-l4 | about 55 min + 2 min per own dev | 0 Modal |

Six families: Modal about 3.3 USD (the A42-D 4.1 line says about 1.5 USD, 0.25 per pilot: the estimate here is higher because of
start-up and the model load; both are far inside the 40 USD cap), L4 about 6.6 h in total. Wave 1 (T40-T43) pilots can run back to
back: one L4 start serves all four reads.
Free alternative for training: `make_config.py` prints an `od_gcp.py train` command (micro_tokens 4096, about 30 min per pilot on the
L4, 0 Modal). Its memory fit is UNPROVEN (the H100 smoke at 8192 reserved 28.6 GB; the L4 has 23 GB): run `od_gcp.py smoke` first. The
Modal path is the proven one.

## Open items for the orchestrator
- Paths of the family row files, the 300-row own dev splits, the G-proxy rows/relations and its recorded hash are not known yet.
- The G-proxy rows should carry `meta.source_doc` (or `doc_id`); otherwise clustering falls back to `group_id` and `verdict.py` warns (a finer unit makes the CI too narrow).
- The pilot rows are trained as given; `make_config` reports ordinal rows (lam_ord 1.0 would act on them, A37 i) and kd targets.
- mahadikarya2 may lack the C1 init adapter and the base: `pilot_check` says; `pilot_upload_init` uploads C1 from the local backup.
