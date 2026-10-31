# C2 training chain and checkpoint-grid tooling (A37 i/k, A42-D 2, 9, 10; A45)

Everything here is CPU-tested (`tests/test_train_tools.py`, 45 tests, and `tests/test_preflight_a61.py`, 55 tests for the A61 `a61_85` gate, the `c2_tmax.json` guard and the credit coverage; tiny fake tensors, fake billing, fake `modal`);
nothing has launched a Modal run. All commands run from `jev/opendecide-data/lean`; `PY=../.venv/bin/python -B`.
The owner's GO (A37 l) comes first: write his words into `c2_build/train/OWNER_GO_C2.txt`; preflight refuses without it.

## Files
| File | What |
|---|---|
| `runs/q35_4b_c2.json` | Frozen config: C1 init `/vol/models/q35_4b_main500k_init` (507d1c29), recipe of `q35_4b_c_r1.json` unchanged (lr 5e-5, one pass, r16/a32, batch 16, lam_ord 1.0 on replay ordinals only), seed 20261013 (A37 i), `snap_fracs` 0.25/0.33/0.5/0.67/0.75/0.83/0.92 (+ the final adapter = 8 checkpoints, A42-D 9.1). 4 values are `FILL` until the mix exists (`modal_od` refuses a FILL config). |
| `modal_od_c2.py` (+ `MODAL_OD_C2.diff`, `make_modal_od_c2.py`) | Generated C2 copy of the pinned `modal_od.py`. **Checkpoint saving needs no edit** (`train_decoder` snapshots from `snap_fracs`). The 3 changes: data mount keeps `c2_parts/c2_train.jsonl` + `c2_rel.jsonl` (otherwise `_launch_checks` refuses); mount drops any path part matching `ohs|sealed|quarantine|longbench|jevbench|decision_index|ejs|jev`; `relay` refuses unless `MODAL_PROFILE` is exported and is mahadikarya2/3, and the config is `q35_4b_c2`. |
| `preflight_c2.py` | Config = round-1 recipe + allowed diffs; 6-10 checkpoints; mix files hash-match manifest + `config_fill_c2.json`; rows 50,000..125,000 (A40 d / A42-D 1.4); OHS-4 sha = A38; A42-D block sha (A45 e); mount probes; T_max (a `logs/c2_tmax.json` with another cap_total or formula FAILS); accounts (the two relay profiles, credit, no running app, C1 init on both Volumes, no `models/q35_4b_c2`; a free credit that does not cover T_max + the later lines FAILS); **`a61_85` (A61 f, fix 6): the 8.5-gated sources of the mix (`c2_md_<x>` -> `md_<x>`, `c2_sb5` -> `SB5_uci293`) each need exactly one `PASS` line in the one logged final-mix 8.5 run (`zed_orch/di_train/A61_FINAL_85_{INPUT.json,RESULT.txt,EXIT.txt}`, shas logged in `A61_EDIT_RECORD.json`, exit 0), none a `HIT`; no flag clears it**; snap-monitor CPU record; stale records. `fill` writes the 4 mixer values into the config. |
| `c2_check.py` | Money and stop rules (see below). |
| `c2_chain.sh` | `start`, `copy`, `resume <profile>`. |
| `merge_avg.py` | 18-candidate grid in merged-weight space (exact stacked-LoRA form). |
| `select_candidate.py` | A42-D 9.3-9.6. |
| `symmetrise.py` | A42-D 10: flips, adoption checks. |

## Money (A42-D 2)
* Cap $40 on every C2 Modal line, any account (A42-D 2.1; only a new owner ruling changes it). Non-training spend (pilots, reads, OHS-AC, ...) is added by hand:
  `$PY c2_build/train/c2_check.py spend --usd 1.2 --what "T40 pilot" --profile mahadikarya2`  (logs/c2_spend.jsonl).
* **T_max = T_core = min(34, 32 - that sum, C - 8)** (A42-D 2.3, A61 e), written once by `preflight_c2.py --fix-tmax` (the chain's `start` does it)
  to `logs/c2_tmax.json`, with C. C = the live free credit on mahadikarya2 + mahadikarya3, each less the $1 reserve (read through the billing
  call, logged; `c2_check.py status` prints it); the credit fit only lowers T_max ($8 = evaluation $4 + SPEED-3 $2 + the $2 reserve).
  `mix_c2.py` takes the same numbers: `--spend-to-date $($PY c2_build/train/c2_check.py other) --credit-usd <C>` (`--credit-usd` is required with `--final`).
* Training spend = per account max(wall of closed segments x $4.09/h, billing delta since the preflight baseline); an unclosed
  segment counts to its cap but never above billing + the last 75 min. Ledger lines: `lean/logs/budget_ledger.md` and `logs/c2_ledger.md`.
* **A37 (k) stop-and-ask:** `proj` (after steps 100-300) is STOP when the projection (training + $2) is above T_max, or when
  other spend + projection is above $40, or the rest does not fit the T_max minutes. The old $17 is gone.
* Each segment cap = min(T_max minutes left, free credit left on the account - $1, 540). When credit binds and the account has
  < 10 min, the verdict is RELAY (exit 3). Payers: the mahadikarya2 -> mahadikarya3 relay ONLY (A42-D 2.4, A61 e): no other account, and the card
  account (aryamhd) is never launched from here (an explicit owner GO that names the amount, by a new owner ruling).

## Launch (the orchestrator)
```
# 0. after the mix: fill the config, record GO, preflight (dry)
$PY c2_build/train/preflight_c2.py fill --dry-run && $PY c2_build/train/preflight_c2.py fill
$PY c2_build/train/preflight_c2.py --offline            # CPU checks only; never a GO
# 1. training, free credit, mahadikarya2 (preflight with --fix-tmax runs inside; --ack-pending = the manifest's
#    pending_after_mix list has been cleared by the orchestrator: G13 on the final mix, OHS-4 sealed-side count)
nohup bash c2_build/train/c2_chain.sh start --ack-pending > c2_build/train/logs/c2_chain.log 2>&1 &
# 2. exit 3 / "RELAY": the free credit of the running account is used up. Free copy of the run folder (hash-checked) to the next
#    account of the relay (A42-D 2.4, A61 e: mahadikarya2 -> mahadikarya3 only; never aryamhd),
#    then resume there (the chain prints both commands, e.g. for mahadikarya2 -> mahadikarya3):
bash c2_build/train/c2_chain.sh copy                    # from the account of the last segment to the next one (or: copy <from> <to>)
nohup bash c2_build/train/c2_chain.sh resume mahadikarya3 > c2_build/train/logs/c2_chain_mahadikarya3.log 2>&1 &
# 3. crash relaunch (only with the owner's OK): c2_chain.sh resume <profile of the crashed segment>
# 4. watching: tail c2_build/train/logs/c2_chain.log ; $PY c2_build/train/c2_check.py status ; $PY c2_build/snap_monitor_c2.py status
# 5. after "C2 TRAINING FINAL" (logs/relay_q35_4b_c2_final.json): ONE local copy (memory rule), on the profile that ran last:
MODAL_PROFILE=<last profile> ../.venv/bin/modal volume get opendecide models/q35_4b_c2 models/    # adapter, snaps/, train_meta.json
# 6. grid (18 candidates, ~6 GB fp32 on disk; record grid.json's sha256 before any look), then reads of all 18 on dev (od-l4, free)
$PY c2_build/train/merge_avg.py show --run models/q35_4b_c2
$PY c2_build/train/merge_avg.py grid --c1 <C1 adapter dir, sha 507d1c29> --run models/q35_4b_c2 --out models/q35_4b_c2_grid
# 7. selection (reads/<candidate>.json per select_candidate.py's docstring), then the freeze record gate_c2.py reads
$PY c2_build/train/select_candidate.py --reads <dir> --grid models/q35_4b_c2_grid/grid.json --out c2_build/train/CHOSEN.json \
    --candidate-out c2_build/CANDIDATE_C2.json
# 8. symmetrisation (after the candidate is frozen; item 10)
$PY c2_build/train/symmetrise.py make-flips --items <yes/no dev items.jsonl> --out flips.jsonl
$PY c2_build/train/symmetrise.py adopt --records recs.jsonl --latency lat.json --out c2_build/train/ADOPT.json
# tests
cd c2_build/train && ../../../.venv/bin/python -B -m pytest -q tests
```
Chain order (all inside `start`): preflight -> `cap` check -> seg1 (steps 0-100, `--log-every 1`, 30 min) -> `first100` (non-finite loss
term = ABORT at once, plus guards: loss > 3x first-5 mean, < 95 records, s/step > 2 x 3.716) -> seg2 (100-300, `--log-every 10`, 35 min)
-> `proj` (A37 k) -> snap monitor started and confirmed alive -> seg3.. (`--expect-resume`, server-side `--stop-after-min`) until `final`.
A fired stop rule, an escalation or a dead monitor ends the chain with no candidate; every modal call carries `MODAL_PROFILE`.

## Checkpoints, grid, selection
* Checkpoints: `snaps/s<step>` (7) + the final adapter. Early = nearest 33%; last-3 = the three latest incl. the final.
* `merge_avg.py` never averages A and B separately: candidate dW = sum c_k dW_k as one stacked LoRA (rank 16 K, same alpha/r),
  verified against the dense sum on sampled modules (< 1e-5, enforced). `final_a10` is the final adapter byte for byte.
* `select_candidate.py`: S = mean(G-proxy, R mixdev, pooled own dev) in pt; eligibility = 11 booleans (spec 7.2 a-d incl. D1-D6, D9,
  complement, plus the 4.3 G-proxy rule); paired 95% CI clustered, 10,000 resamples, seed 0, only for the best eligible
  candidate; final step unless that CI's lower bound > 0.

## Open items for the orchestrator (nothing below was edited; files belong to others)
1. ~~`snap_monitor_c2.py` accepts only `--profile mahadikarya2`~~ (A42-D 2.4): its `PROFILES` is the two relay accounts
   (= `c2_check.RELAY_ACCOUNTS`; a test keeps the lists equal). Its state file keeps the reads already done across a relay.
2. **`gate_c2.py` runs one pre-gate per candidate adapter (CANDIDATE_C2.json) and has no per-candidate eligibility mode.** A42-D 9.4 needs
   the 11 eligibility booleans for each of the 18 candidates before `CANDIDATE_C2.json` exists; the reads and a per-candidate gate wrapper
   (or gate_dev outputs mapped to the 11 keys) are not written.
3. `symmetrise.py`: which catalogue pattern is the serving flip (default order FAIL_TO, LACK, FRAME_NOT, NEG_FRAME, LEX_PAIR, frameless first)
   is a serving choice; the 150 held-out-pattern pairs (item 7.4) and the G-proxy do not exist yet. Reads of q and flip q (cached prefix)
   and the sym-path latency run are not scripted.
4. The training-GO request must state item 7's realised rows and pattern count (A45 a); `preflight_c2.py` prints `counts.by_block`.
5. Not run: online preflight (needs Modal control-plane calls), any Modal run, an end-to-end `start`.

## P6 grid tooling (17 Oct; CPU-tested in `tests/test_grid_tools.py`, 28 tests; nothing run on a VM, no G13)
| File | What |
|---|---|
| `grid_plan.py` | `record` (grid.json sha256 before any look, A42-D 9.6; refuses if any grid read exists), `verify`, `plan` (read plan for the 18 + the C1 reference, `--expected` before grid.json exists; writes `READ_PLAN.json` + `GRID_CFG.json`), `candidate-check` (CANDIDATE_C2.json timing and identity: after the grid reads and record, before the first official read of q35_4b_c2, adapter at the gate path = the chosen one). |
| `grid_elig.py` | Per-candidate eligibility: gate_c2's own rules on each candidate's reads mapped to the 11 booleans + item 4.3 G-proxy rule; writes `reads/<cand>.json` for select_candidate.py. A missing or unmeasured input is a refusal, never a pass. |
| `sym_reads.py` | A42-D 10: `items` (flip rows of D1 yes/no, G-proxy and the 150 pairs, staged outside data/), `records` (q + flip-q join for `symmetrise.py adopt`), `latency` (plain vs q+flip-q in one call, batch 1) and `latency-join`. |
| `symmetrise.py` | Fixed: `CatalogueFlipper` read only `instruction`; real rows use `instructions`, and rows with a card now get the exchanged card. |
Staged outputs: `c2_build/staged/P6-grid/` (READ_PLAN.json, GRID_CFG.json, sym/). Open questions Q1-Q7 are in READ_PLAN.json.
