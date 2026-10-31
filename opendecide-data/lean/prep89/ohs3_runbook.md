# OHS-3 runbook (goal steps 8-9): one run, compared with Jev

Written 1 Oct 2026; §0 item 1 updated 2 Oct (the shipped 4B is TBD by gate job 3, `prereg_drafts/A8prime.md`);
dev-only fit logs, PRISM-X weights sha256, load-test `--plan` and §5/§6 updated 2 Oct UTC.
**Nothing here has run on real OHS-3.** Everything was built and tested on the Mac CPU only. No
Modal, gcloud, ssh or paid call was made. No OHS-3 item text was opened: the scripts touched OHS-3 only through row
counts, field names and the frozen sha256 values. All new files are in `lean/prep89/`. No PREREG file, `gate_dev.py`,
`score_ohs3.py`, `run_jev.py` or other frozen file was edited.

## 0. Read this first

1. **The shipped 4B is TBD by gate job 3** (`prereg_drafts/A8prime.md`). It is fixed only by that job's outcome
   (`logs/gate4b_fix2/summary.json`) or by a dated owner-override amendment, never by anything on OHS-3. All three
   candidates share base `Qwen/Qwen3.5-4B` at revision `851bf6e8…`, layout `schema_branch_mark` and style cygnet.

   | Candidate | Name | `adapter_model.safetensors` sha256 | The one local copy | When it ships |
   |---|---|---|---|---|
   | 4B-E (REF) | `q35_4b_pxE` | `1bbd8a79143f7ab5d6fd538c870ded0605120ab777c97d38ca3384b26c31a3f9` | `backups/gcp_models/q35_4b_pxE` | the PREREG 5.7 fallback: C4 fails any A8′ condition, or C4 is never trained |
   | C1 (main run) | `q35_4b_main500k` | `507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078` | `backups/modal_models/q35_4b_main500k` | only by a dated owner-override amendment (job 1: DO NOT SHIP, constraint (e) 8.86% vs 5.68%) |
   | C4 (top-up) | `q35_4b_main500k_fix2` | fill in after training, from the copy gate job 3 reads | `backups/modal_models/q35_4b_main500k_fix2` | A8′ steps R, P and N pass and its one ship look gives a FINAL SHIP |

   - The config template leaves `models.4b.name` and `adapter_sha256` as `<OWNER …>` placeholders, so no script runs
     until the shipped model is filled in from `models.4b._candidates`. `ohs3_preflight.py` checks the sha256 against
     the local copy in `backups/gcp_models/` or `backups/modal_models/`.
   - The A5 temperatures of whichever model ships come from one rule: `prep89/t_rule_check.py` (it reproduces
     READOUT_DEV.md's 1.00 / 1.00 for 4B-E and C1). C4 needs its job-3 standard read and a `--tta-choice` read
     (`q35_4b_main500k_fix2_2v`, A8′ step 7) first.
   - The readout amendment to PREREG_OHS3 rule 4 is drafted in `prereg_drafts/AMENDMENT_OHS3_rule4_readout.md`.
2. **Step 8 (dev only) suggests the A5 values** (`prep89/READOUT_DEV.md`). The template still leaves them to the
   owner:
   - choice rows: 2-view (given order + exact reversal, averaged), yes/no rows: single read;
   - T = 1.00 for yes/no and 1.00 for choice, for both readouts (the dev-select fits failed A5 item 4's bar);
   - band edge: JevBench only, never OHS-3;
   - 2-view does not fix the main run's (e) failure.
3. **The existing direct host cannot serve OHS-3 as it is.**
   - `hosting/modal_direct_host.parse_request` allows at most 26 options. OHS-3 has 284 base rows with 40 options
     (`se_site`, `fr_agency`), plus their option-order twins.
   - It rejects definition cards on yes/no rows (every OHS-3 row has a card), has no 2-view, no T, and returns only
     the final answer.
   - `prep89/ohs3_lib.A5Decider` fixes all of this. `prep89/modal_ohs3_host.py` puts it on the same H100 core (same
     image, boot, CUDA graphs and HTTP server, imported, not copied).
4. **Rule 4 vs "score on the L4, time on the H100".** PREREG_OHS3 rule 4: OpenDecide runs exactly once per model, in
   its serving configuration. Scoring on the L4 and then replaying the same inputs on the H100 for timing is a second
   OHS-3 pass. The speed draft says this breaks rule 4 unless an amendment allows it. See decision **D1**.
5. **The L4 may be busy.** The yn2b A/B arms are planned on the same VM. Run OHS-3 there only when `nvidia-smi` shows
   no job, and run the `--check-only` step first.
6. **Files to commit before the run** (the preflight lists them): `score_ohs3.py` and `hosting/` are **untracked**
   today; all of `prep89/ohs3_*.py` and `prep89/modal_ohs3_host.py`; the filled `prep89/ohs3_config.json`.
7. **Jev cost** (OpenRouter):
   - OHS-3 has 2,456 calls per run.
   - **At the rates billed so far** (OHS-1 $0.032 per 1K calls, OHS-2 about $0.038 per 1K): 2 runs **$0.16-0.19**;
     3 runs (with the timing pass) **$0.24-0.28**.
   - **List-price ceiling** (every call 6,000 characters of state + 40 option definitions, about 3,400 tokens, at
     $0.042 per million): **$0.70** for 2 runs, **$1.05** for 3.
   - OHS-3 calls are longer than OHS-1/2 calls (wide cards), so expect more than the billed-rate figure, but under
     the ceiling. The brief's **$1.2-2.7** is above both, so it is a safe budget. The collector stops at
     `--cost-cap 3.0`.

## 1. Files (all new, in `lean/prep89/`)

| File | Role |
|---|---|
| `ohs3_runbook.md` | this runbook |
| `ohs3_config.template.json` | **every setting to pre-register**: model and sha256, A5 readout, T values, cascade, D1/D2, hosting, speed rule, cost inputs. `<OWNER …>` marks the open choices (with the step-8 suggestion); the scripts refuse to run while any are left |
| `ohs3_lib.py` | shared code. Takes run_jev.py's own `card_defs`, `question` and GUARD, and calibrate.py's `scaled`, **by AST**, so they cannot drift. Also: `a5_read` (decoder_io.predict's batching and 2-view, keeping the identity view; optional per-row **token counts** read from the encodes cand_logits makes anyway, results bit-identical), `A5Decider` (returns `usage`: input tokens of every read, identity-read tokens, output 0), `CascadeDecider` + `cascade_answer` (the one 2B→4B rule, offline and served), `check_prism_x` (the 2B's control plane must be active with the config's parts), `region_multiplier` (C1/C2 rate), config checks, the rule-4 ledger, frozen-hash checks, the speed bootstrap, a blind print guard |
| `ohs3_jev_collect.py` | **(a)** runs the unchanged `run_jev.py` twice (`jev_guard`, then `jev_r2_guard`), with resume passes, preflight checks, a cost guard and per-run summaries |
| `ohs3_od_run.py` | **(b)** one blind OpenDecide run on the L4 with the A5 readout. Writes `<name>`, `<name>_cal` (primary), `<name>_cal_bc` (secondary, unchanged batchcal.py), `<name>_1v` and `<name>_1v_cal` (single read, same pass). Resumes after preemption; refuses a second run; `--check-only` pre-GO check; refuses code that differs from the Mac's manifest |
| `ohs3_backends.py` | `real` (GPU; sha256, layout and PRISM-X checked; the od_gcp load path), `tiny` (CPU dry run), `tiny_px` (CPU dry run of the 2B path: real 2B tokenizer + an active PRISM-X control plane, eager) and `oracle` (synthetic only) |
| `ohs3_serve.py` | our endpoint = A5Decider (4B, 2B) or CascadeDecider (2B→4B, big model loaded first) behind hosting's HTTP server (local or dry run) |
| `modal_ohs3_host.py` | the same on one Modal H100 through a direct tunnel: the 4B with CUDA graphs, the PRISM-X 2B **eagerly** (`boot_eager`), or the **cascade** (4B graphs + 2B eager on one GPU, `boot_cascade`); runs `ohs3_timing.py` in-process; optional DEV-only GPU smoke; the C1 **load test** (`--load-test`, or `--then-load-test` right after the timing pass). Region = the config's `hosting.region`. **Never run on Modal yet** |
| `ohs3_timing.py` | **(c)** the timing harness of the speed definition: interleaved, concurrency 1, seeded order, 20 dev warm-up calls, retries timed from the first attempt, failures recorded at 30 s, paired stratified bootstrap. `--model-key 4b / 2b / cascade` (one pass per system; the endpoint's /health must name the system and config). Every record logs **input and output tokens** (Jev: API usage; ours: the server's count) and per question [type, options, tokens]; the summary adds token totals, the 2-view token multiplier, the cascade's routed share and latency by route. Can write the scored files for D1 = served_h100 (models and the cascade) or D2 = run1_via_harness; then a refill pass re-sends failed calls (untimed) so every row has an answer |
| `ohs3_cascade.py` | optional 2B→4B cascade, offline from both models' primary predictions (same rule function as the served cascade; `route_on` primary or raw) |
| `load_test_c1.py` | **C1** dev-only load test: sustained decisions per hour under concurrency (levels 1-16), dev rows length-matched to the timing pass's logged token counts (KS ≤ 0.05, mean within 2%), server token count = local count checked, C1 at the region rate. `--plan` prints the exact commands and the cost estimate from the config (no endpoint) |
| `ohs3_final_table.py` | **(d)** runs `score_ohs3.py` (unchanged) on every configuration, then writes `results_ohs3/final_table.{md,json}` with every win condition |
| `ohs3_preflight.py` | pre-GO checklist (hashes, git state, config, sha256 values, rule 4, key present, cost); writes `ohs3_code_manifest.json` for the L4 |
| `make_synthetic_ohs3.py`, `fake_jev_server.py`, `dryrun_ohs3.py`, `test_ohs3_prep.py` | CPU dry run on a synthetic stand-in built from dev rows, and 97 unit checks |
| `t_rule_check.py` | the A5 item-4 temperature rule for any one model and its exact primary readout (`--json` = the `T_fit_log`). `--model` names the model (a read whose meta names another adapter stops it), `--choice-single` also fits `T_single.choice`, `--choice-lt10` builds the 2view_ge10 readout; the JSON records each dev read's sha256, adapter and view flags |
| `cascade_rule_fit.py` | the 2B → 4B cascade rule from DEV reads only (FINETUNE_PLAN 5.3): tau per budget 30-80% on dev-select, the smallest budget whose one-sided 95% lower bound vs the 4B is > −0.5 pp, dev-confirm once, and 5.3's use rule (cost ratio from two dev load tests + routed share < 0.85). Its `--json` = `cascade.tau_fit_log` |
| `t_fit_q35_4b_pxE.json`, `t_fit_q35_2b_armI_1600.json`, `cascade_fit_dev_armI1600_to_pxE.json` | dev-only logs of today's models (2 Oct): 4B-E's T log (ready as its `T_fit_log` if 4B-E ships), the 2B I_1600's (view flags missing in its old metas: TODO) and the cascade rule on them (70% routing chosen; use rule not measured). Evidence only, not config values |

## 2. Owner decisions (write them into the PREREG_OHS3 model amendment before any OHS-3 call)

Copy the template to `prep89/ohs3_config.json` and fill every `<OWNER …>`. Everything is chosen on dev only.

| Key | Choice | Source |
|---|---|---|
| `models.4b.readout_choice` | `2view` (step 8 suggests) / `single` / `2view_ge10` | A5 item 1; READOUT_DEV.md |
| `models.4b.T_primary`, `T_single`, `T_fit_log` | T per question type (step 8: 1.00 / 1.00 for both), copied from `prep89/t_rule_check.py --json` (the `T_fit_log`); every real run stops unless they equal its ship values | A5 item 4; READOUT_DEV.md |
| `models.2b.*`, `cascade.*` | run or not; 2B adapter sha256, **`prism_x_sha256`** (sha256 of `prism_x.safetensors`: the PRISM-X weights are part of the served 2B; the loaders and the preflight check it) and readout; cascade tau set on dev-select | A5 item 5, FINETUNE_PLAN 5.3 |
| `decisions.od_scored_run` (**D1**) | see below | rule 4 |
| `decisions.jev_timing` (**D2**) | see below | rules 2-3, speed draft decision 3 |
| `hosting.endpoint`, `customer_usable` | `modal_forward_tunnel` (what `modal_ohs3_host.py` does) / web endpoint | speed draft decision 2 |
| `speed.rule_S1` | default "p50 CI (Jev − OD) entirely above 0 AND p95 point estimate lower" | speed draft decision 1 |
| `cost.utilisation_for_claim`, `od_decisions_per_hour_sustained`, `l4_usd_per_hour`, `c3_od_usd_per_1k` | 0.4 (proposed) or 1.0; throughput `load_test` (recommended: `load_test_c1.py`, settings in `cost.load_test`) or a number from an earlier dev load test | speed draft decision 4 |
| `models.2b.prism_x`, `models.2b.cuda_graphs` | `"I"`, `false` (PRISM-X runs eagerly; the scripts refuse graphs for it) | 2B arm I |
| `cascade.tau`, `w_big`, `route_on`, `tau_fit_log` | `config_values` of `prep89/cascade_rule_fit.py --json` (dev-select, FINETUNE_PLAN 5.3 budget rule; copy the full tau float); `route_on`: `primary` (A5 item 5) or `raw` (5.3); identical at T = 1.00. Only if its 5.3 use rule passes (needs the 2B and 4B dev load tests) | A5 item 5 |
| `speed.headline_system` | `4b` (default) / `2b` / `cascade`: whose pass is the S1 claim; only that pass may collect a scored Jev run | speed draft |
| "accuracy ≥ Jev" rule (in `ohs3_final_table.py`) | won = PREREG "beats", or "matches" (CI lower bound > −2 pp) with a point estimate ≥ 0. Quote it in the amendment | final goal |

**D1: where OpenDecide's one scored run happens.**
- **`served_h100`** (recommended):
  - The only OpenDecide OHS-3 pass is the timed pass on the H100 direct host.
  - `--od-preds-name <name>` writes the five prediction files from the served answers (each response carries the
    pre-T readout, the identity view and the final answer).
  - Rule 4 holds as written: accuracy and speed come from the same answers, "in its serving configuration".
  - Risk: the scored run depends on one Modal session. The harness resumes, and a refill pass answers failed calls.
- **`L4_batch`** (the brief's default):
  - `ohs3_od_run.py` on the L4 is the scored run. The H100 timing pass replays the same inputs.
  - Needs one amendment sentence: *"The H100 timing replay's probabilities are never scored; they are used only for
    the parity check against the scored L4 run (argmax agreement ≥ 0.99, mean max |Δp| ≤ 0.005, max |Δp| ≤ 0.05)."*
    Without it, the replay breaks rule 4.

**D2: how Jev is timed.**
- **`extra_pass`** (recommended):
  - Both scored Jev runs use run_jev.py **exactly as for OHS-2** (concurrency 8).
  - Timing uses a third, unscored pass (`jev_timing_guard`), interleaved with ours at concurrency 1, with the same
    request objects (run_jev.py's own code). Disclose it as a third Jev pass (about +$0.1-0.4).
- **`run1_via_harness`** (the speed draft taken literally):
  - `--jev-preds-tag jev_guard` collects Jev run 1 interleaved with ours, in run_jev.py's exact raw and preds format
    (the dry run proves the converter is byte-identical). Run E **before** C, then C with `--tags jev_r2_guard`.
  - Disclose: run 1 at concurrency 1; its `latency_ms` is first attempt to success; failed calls were re-sent in a
    refill pass (as run_jev.py's resume passes do).

## 3. Exact commands

Run from `~/Documents/jev/opendecide-data/lean` unless marked VM. Python: `../.venv/bin/python`.

**A. Free, CPU, any time (all pass today):**
```
../.venv/bin/python prep89/test_ohs3_prep.py          # 97 checks, about 35 s
../.venv/bin/python prep89/dryrun_ohs3.py             # end to end on the synthetic stand-in (about 12 min)
../.venv/bin/python prep89/ohs3_preflight.py --config prep89/ohs3_config.template.json --template
```

**B. Owner: pre-register (no OHS-3 call):**
```
cp prep89/ohs3_config.template.json prep89/ohs3_config.json   # fill every <OWNER ...> (dev only)
# first: the shipped 4B from gate job 3 (A8'); fill models.4b.name + adapter_sha256 from models.4b._candidates, then its T:
../.venv/bin/python prep89/t_rule_check.py --model <SHIPPED_4B> --noul <its single read> --choice <its 2-view read> \
    --choice-single <its single read> --json prep89/t_fit_<SHIPPED_4B>.json
#   4B-E: --model q35_4b_pxE --noul q35_4b_pxE_fresh --choice q35_4b_pxE_tta --choice-single q35_4b_pxE_fresh
#   C4:   --model q35_4b_main500k_fix2 --noul q35_4b_main500k_fix2 --choice q35_4b_main500k_fix2_2v
#         --choice-single q35_4b_main500k_fix2
#   copy its "ship" values into T_primary (noul, choice) and T_single (noul = T_noul, choice = T_choice_single)
# only if the 2B / the cascade are pre-registered (dev only):
#   the 2B's T: the same command with --model <2B> and its reads -> prep89/t_fit_<2B>.json; prism_x_sha256 = sha256 of
#   its prism_x.safetensors (shasum -a 256 backups/<dir>/<2B>/prism_x.safetensors)
#   the cost ratio for 5.3's use rule: two DEV load tests on one H100 (E's load-test commands with --model-key 2b and
#   --model-key 4b, no --load-match: dev rows, PREREG type mix; about $0.9-2.0 each, `load_test_c1.py --plan`)
#   ../.venv/bin/python prep89/cascade_rule_fit.py --small-t-log prep89/t_fit_<2B>.json \
#       --big-t-log prep89/t_fit_<SHIPPED_4B>.json --route-on <raw|primary> --w-big 1.0 \
#       --load-tests logs/ohs3/load_test/<2b dev>/summary.json,logs/ohs3/load_test/<4b dev>/summary.json \
#       --json prep89/cascade_fit_<name>.json
#   copy its config_values into cascade.tau / w_big / route_on; set cascade.run true only if it chose a budget AND
#   its use rule passed (the preflight and every real cascade run check this)
git add score_ohs3.py hosting/ prep89/*.py prep89/ohs3_config.json prep89/ohs3_runbook.md \
    prep89/READOUT_DEV.md prep89/readout_dev.json prep89/readout_dev.txt prep89/t_fit_*.json \
    prep89/cascade_fit_*.json   # the dev-only evidence (T_fit_log, tau_fit_log)
git commit -m "OHS-3 harness + run config (before any OHS-3 run)"
../.venv/bin/python prep89/ohs3_preflight.py --config prep89/ohs3_config.json
#   must end "READY for GO"; prints the config sha256 and writes prep89/ohs3_code_manifest.json
# Commit the rule-4 readout amendment (prereg_drafts/AMENDMENT_OHS3_rule4_readout.md) and
# write the PREREG_OHS3 model amendment quoting: config sha256, adapter sha256, readout, T, D1, D2, endpoint,
# S1 rule, C1 utilisation, the accuracy-won rule, and the sha256 of score_ohs3.py / ohs3_*.py; adopt or change the
# scorer's INTERPRETATION points (prereg_drafts/score_ohs3_interpretations.md). Commit it.
# NOTE lines (D1 = L4_batch / D2 = run1_via_harness) are reminders of amendment text; they do not block READY.
```

**C. GO 1: Jev (paid OpenRouter; about $0.2-0.7, capped at $3):**
```
../.venv/bin/python prep89/ohs3_jev_collect.py --go --usage-check --cost-cap 3.0
# -> preds_ohs3/jev_guard{,_raw}.jsonl, jev_r2_guard{,_raw}.jsonl; logs/ohs3/jev_collect_<tag>.json
# Re-run the same command to resume. It stops if run_jev.py differs from HEAD, an override env var is set, or
# TYPESAFE_API_KEY is set (OHS-2 used the OpenRouter route).
# D2 = run1_via_harness: do E first, then:  ... ohs3_jev_collect.py --go --usage-check --tags jev_r2_guard
```

**D. OpenDecide scored run on the L4** (only if D1 = `L4_batch`; VM `od-l4`, zone `us-central1-a`, project
`system-one-509903`, VM python `~/od/bin/python`):
```
G="--zone us-central1-a --project system-one-509903"
gcloud compute instances start od-l4 $G
gcloud compute ssh od-l4 $G --command "nvidia-smi --query-gpu=memory.used --format=csv; mkdir -p ~/lean/prep89 ~/lean/logs"
gcloud compute scp $G data/ohs3.jsonl data/ohs3_relations.jsonl data/ohs3_calls.jsonl data/ohs3_summary.json od-l4:~/lean/data/
gcloud compute scp $G prep89/ohs3_lib.py prep89/ohs3_backends.py prep89/ohs3_od_run.py prep89/ohs3_config.json \
    prep89/ohs3_code_manifest.json prep89/t_fit_<SHIPPED_4B>.json od-l4:~/lean/prep89/
# (the manifest lists the T fit log too: the VM run stops unless the config's T equal its ship values)
# VM pre-GO check (no model load, no row read): config sha, frozen files, code manifest, adapter sha, rule 4
gcloud compute ssh od-l4 $G --command "cd ~/lean && ~/od/bin/python prep89/ohs3_od_run.py --config prep89/ohs3_config.json \
    --model-key 4b --config-sha256 <CONFIG_SHA256> --code-manifest prep89/ohs3_code_manifest.json --check-only"
#   if it names differing code files: copy the Mac's committed versions (decoder_io.py, prism_x.py, writeblock.py,
#   calibrate.py, batchcal.py) to ~/lean/ only when no VM job is using them, then re-check
# the run (blind: the log has counts and timings only)
gcloud compute ssh od-l4 $G --command "cd ~/lean && nohup ~/od/bin/python prep89/ohs3_od_run.py --config prep89/ohs3_config.json \
    --model-key 4b --config-sha256 <CONFIG_SHA256> --code-manifest prep89/ohs3_code_manifest.json --go \
    > logs/ohs3_od_4b.log 2>&1 &"
gcloud compute ssh od-l4 $G --command "tail -3 ~/lean/logs/ohs3_od_4b.log"     # poll until "wrote ..."
#   (only if pre-registered) the same two commands with --model-key 2b
mkdir -p preds_ohs3
gcloud compute scp $G "od-l4:~/lean/preds_ohs3/<SHIPPED_4B>*" preds_ohs3/
gcloud compute scp $G od-l4:~/lean/logs/ohs3_runs.jsonl logs/ohs3_runs_l4.jsonl && cat logs/ohs3_runs_l4.jsonl >> logs/ohs3_runs.jsonl
gcloud compute instances stop od-l4 $G
../.venv/bin/python prep89/ohs3_cascade.py --config prep89/ohs3_config.json      # only if cascade.run
```
- After a preemption, start the VM and run the same `--go` command again. It resumes from
  `preds_ohs3/<name>.partial.jsonl` (same run id only).

**E. GO 2: timing on the H100 direct host (Modal; about $4-8; boot about 8 min):**
```
# optional first, DEV rows only (no OHS-3, no Jev; about $1-2): the served path on a GPU vs the stored L4 reads
MODAL_PROFILE=<acct> ../.venv/bin/modal run prep89/modal_ohs3_host.py::main --config prep89/ohs3_config.json \
    --name h100_dev_smoke --dev-smoke dev_nc:60,devp_card:40 --go
# the OHS-3 timing pass (D1 = L4_batch, D2 = extra_pass):
MODAL_PROFILE=<acct> ../.venv/bin/modal run prep89/modal_ohs3_host.py::main --config prep89/ohs3_config.json \
    --model-key 4b --name ohs3_timing --scored-name <SHIPPED_4B> --go
# D1 = served_h100 (this pass IS the scored run): drop --scored-name, add  --od-preds-name <SHIPPED_4B>
# D2 = run1_via_harness: add  --jev-preds-tag jev_guard
# if the session dies: run the same command again (resumes from logs/ohs3/timing/ohs3_timing/records.jsonl)
```
- `<SHIPPED_4B>` is the name in the committed config (§0 item 1). `<acct>` must be the Modal account whose Volume
  `opendecide` holds `models/<SHIPPED_4B>` with the pre-registered sha256 (the server checks it at load). C1 and C4
  were trained on Modal, so their training account's Volume has them; 4B-E's one local copy is
  `backups/gcp_models/q35_4b_pxE`, so check that Volume's `models/q35_4b_pxE` sha256 (upload the local copy if absent).
- The DEV smoke compares the served answers with the stored L4 reads of the same adapter. The refs follow the
  configured name (`ohs3_timing.smoke_refs`): 4B-E → `q35_4b_pxE_fresh` + `q35_4b_pxE_tta`; C4 →
  `q35_4b_main500k_fix2` + `q35_4b_main500k_fix2_2v` (both from gate job 3). `--smoke-ref-1v/-2v` override them.
- Never pass `--limit` on real OHS-3: any partial pass is part of the one run.
- Graph plan: batch 1 up to 2,048 tokens plus long single-row buckets up to 3,072. Longer prompts run eagerly.
- **C1 load test in the same session (recommended, DEV rows only, about +7.2 min = +$0.51-0.90; `load_test_c1.py
  --plan` prints the commands and the estimate from the config):** add
  `--then-load-test` to the timing command. It length-matches dev rows to the token counts this pass just logged and
  writes `logs/ohs3/load_test/ohs3_timing_c1/summary.json`. On its own (new session, ~16 min, $1.16-2.03):
  `... modal_ohs3_host.py::main --config prep89/ohs3_config.json --model-key 4b --name c1_load_4b --load-test
  --load-match logs/ohs3/timing/ohs3_timing/records.jsonl --go`. Without `--load-match` it is a pre-run estimate
  only (PREREG type mix, dev lengths) and the final table will not use it.
- **The 2B (only if pre-registered):** the same command with `--model-key 2b --name ohs3_timing_2b` (eager boot ~4
  min; the server checks the PRISM-X control plane is active with the config's parts). Its dev smoke needs its own
  refs: `--smoke-ref-1v <2b single read> --smoke-ref-2v <2b 2-view read>`.
- **The cascade (only if `cascade.run`):** `--model-key cascade --name ohs3_timing_cascade` boots the 4B (graphs)
  and then the 2B (eager) on one H100 and serves the cascade (tau / w_big / route_on from the config), timed end to
  end with routing. D1 = served_h100: `--od-preds-name <cascade name>` makes this pass the cascade's one run (then
  `ohs3_cascade.py` refuses); D1 = L4_batch: run `ohs3_cascade.py` first and pass `--scored-name <cascade name>`
  (parity: answers, routed set, both components). Dev smoke: `--smoke-ref-1v/-2v` = the 2B's reads,
  `--smoke-ref-big-1v` = the 4B's single read.
- Only the `speed.headline_system` pass may collect a scored Jev run (D2 = run1_via_harness); time the other
  systems against an unscored Jev pass (about +$0.1-0.4 each) or `--no-jev` (then no paired S1 for them).

**F. Optional: Jev's latency run-to-run noise** (speed draft: "Jev run 2 is timed the same way"; Jev only, unscored,
about $0.1-0.35):
```
../.venv/bin/python prep89/ohs3_timing.py --config prep89/ohs3_config.json --name ohs3_timing_jev2 --go
```

**G. Score and final table (Mac, CPU):**
```
../.venv/bin/python prep89/ohs3_final_table.py --config prep89/ohs3_config.json --go \
    --timing logs/ohs3/timing/ohs3_timing/summary.json \
    --load-test logs/ohs3/load_test/ohs3_timing_c1/summary.json \
    [--timing-extra 2b=logs/ohs3/timing/ohs3_timing_2b/summary.json,cascade=logs/ohs3/timing/ohs3_timing_cascade/summary.json]
# -> results_ohs3/score_ohs3_all.json (score_ohs3.py, 10,000 resamples, both Jev runs, --half all)
#    results_ohs3/final_table.md / .json
```
- Models: `<4b>_cal` first (the headline), then `<4b>_1v_cal`, the 2B and the cascade if they ran. Every
  OpenDecide configuration run on OHS-3 is listed.
- Real mode refuses `--allow-deviation` and any `--boot` other than 10,000.
- `--timing` must be the headline system's pass (checked by name). C1 = `od_usd_per_hour` × the `hosting.region`
  multiplier (us-east: ×1.75 = $7.54/h) / the load test's sustained decisions per hour; the load test must be for
  this config and the headline system and valid (length match, token check, and for the cascade the routed share
  within 0.05 of the OHS-3 pass), else C1 gets no verdict. The table also has a token row (input/output tokens per
  call for both systems, measured on the OHS-3 calls) and descriptive speed rows for the other systems.
- The table also splits option-order drift by twin kind (reversed / rotated, descriptive). With the 2-view readout the
  reversed twins drift ~0 by construction, so report the rotated-twin numbers next to the 304-pair endpoint.

**Guards on real OHS-3 (added 1 Oct, review):** the scripts read `decisions` from the committed config and refuse
flags that contradict it, before any call:
- `ohs3_od_run.py` runs only when D1 = `L4_batch`.
- `ohs3_timing.py` with our endpoint: D1 = `served_h100` needs `--od-preds-name <name>` and no `--scored-name`;
  D1 = `L4_batch` needs `--scored-name <name>`, no `--od-preds-name`, and the L4 preds already in `preds_ohs3/`. It
  refuses a second OpenDecide timing pass under another `--name` (resume the first one instead) and any `--limit`.
- Jev: D2 = `extra_pass` refuses `--jev-preds-tag`; D2 = `run1_via_harness` needs `--jev-preds-tag jev_guard` in E,
  and `ohs3_jev_collect.py` then collects only `jev_r2_guard`, after E. `ohs3_jev_collect.py` reads
  `prep89/ohs3_config.json` (`--config`) for this.

**H. Report:** publish every endpoint, whatever its direction. Disclose the third Jev pass (D2) or the rule-4
sentence (D1), non-pinned Jev rows, unanswered calls, timing failures and refills. OHS-A items may be read for error
analysis; OHS-S stays sealed.

## 4. What the final table contains

| Win condition | Metric | Source | "Won" means |
|---|---|---|---|
| accuracy ≥ Jev | micro and macro accuracy on base rows | PREREG primary, Holm | PREREG "beats", or "matches" with a point estimate ≥ 0 |
| calibration | Brier on 716 yes/no rows | PREREG primary | PREREG "beats" |
| consistency | complement violation (300 pairs), option-order drift (304 pairs) | secondary, BH | od_better (CI > 0, q < 0.05) |
| speed | S1 p50 end to end, S2 p95 | `ohs3_timing.py` summary | p50 CI (Jev − OD) above 0 **and** p95 lower |
| cost | C1 at the pre-registered utilisation; C3 JevBench formula; C2 as run (JSON) | config + timing usage tokens | OD $/1K < Jev $/1K |
| hijack / injection | not measured on OHS-3 (no attack rows) | dev gate (g), E0 jagged audit | n/a |
| JevBench | no submission (owner rule) | | n/a |

Also listed: track F and U, more than 26 options, batch calibration, per task, halves A and S, McNemar against each
Jev run, each Jev run alone, run-to-run agreement, missing answers and ties, rows not from the pinned model.

## 5. Dry run (CPU, synthetic stand-in): what it proved

Last run 2 Oct 2026, 02:52-03:04 UTC: **PASS** (`prep89/dryrun/DRYRUN_REPORT.json`, table
`prep89/dryrun/root/results_ohs3/final_table.md`). The synthetic file is built from **dev rows only** and has the real
file's 14 row keys and every PREREG count: 2,456 rows, 1,852 base rows in 13 tasks, 1,806 groups, 716 yes/no and
1,136 choice base rows, 284 with 40 options, tracks F 1,087 / U 765, 300 `_neg` and 304 `_perm` pairs. Choice golds
are assigned and the models are tiny random ones, so accuracy and speed numbers mean nothing; only the plumbing is
tested.

| Step | What was proved |
|---|---|
| unit tests | **97 checks** (`test_ohs3_prep.py`, run as step 0): run_jev.py request objects and guard taken exactly; T = calibrate.scaled; `a5_read` = decoder_io.predict exactly (2-view and single); served = batch read; token counts = independent tokenizer counts; the PRISM-X 2B path (eager, GraphRunner refuses it); the cascade (served = offline rule); the load test; the identity view file; the dev-only fit logs (T and cascade rule recomputed independently, every config mismatch FAILs, the real-mode scripts stop); the PRISM-X weights sha256; the load-test plan; Jev's SDK usage fields |
| (a) Jev | the unchanged run_jev.py (byte copy) ran twice against a local fake endpoint: calls that failed every attempt in pass 1 were answered by the resume pass; 2,456/2,456 calls per run; our converter = run_jev.py's preds file byte for byte |
| (b) OpenDecide | tiny random Qwen3 + real 4B-E tokenizer through the real decoder_io path: stopped after 2 chunks, resumed, finished; a 3rd start refused (rule 4). The 2B: tiny random Qwen3 + real 2B tokenizer + an ACTIVE PRISM-X control plane, eager. Oracle model, offline cascade |
| (d) identity view | for the 4B and the 2B: `<name>_1v` = a fresh decoder_io.predict() (max diff 0.0 / 2.3e-6), `<name>` = predict(tta_choice=True) (0.0 / 1.1e-6), 1,440 choice rows differ between the two files, yes/no rows identical; token counts in the metas (all reads / identity read = 1.78) |
| (c) timing | DEV smoke of the served path passed (56-option and yes/no-card rows). Interleaved timing of all 2,456 calls, resumed after 300; 3 OD and 3 Jev calls forced to fail were timed at 30 s and answered by the refill pass; parity served vs batch: argmax 1.0, max diff 0; every answered call of both systems has its input and output token counts (`tokens.complete` true for both); the 2B served eagerly (301 calls, path "eager", parity pass); the cascade served end to end (2,456 calls, routed 47.4%, routing and answers identical to the offline cascade) |
| (c) C1 load test | dev rows length-matched to the pass's logged token counts (KS 0.0057, mean ratio 1.0004), server token count = local count on 20/20 calls, valid for C1; `--plan` for the 4B / 2B / cascade gives +7.2 min ($0.51-0.90) in session, 16 / 12 / 18 min ($1.16-2.03 / $0.87-1.53 / $1.30-2.28) on its own |
| (d) scoring | score_ohs3.py, unchanged, 10,000 resamples, on 8 configurations; only deviations = the synthetic sha256 (expected); the served cascade scores exactly like the offline cascade; the final table has every win condition |
| blind audit | 1,970 item-text snippets searched in every printed or logged text: 0 hits |

## 6. Gaps and risks still open

1. **`modal_ohs3_host.py` has never run on Modal.** Tested on CPU: import, the A5 decider's identity view equals
   hosting's core Decider exactly, and the full served path on 127.0.0.1. Untested on an H100: CUDA-graph memory for
   long single-row buckets, boot time, 40-option prompts on the graph path. The optional DEV smoke in E checks this
   on dev rows before any OHS-3 call.
2. **2B and cascade timing: built and CPU-tested (1-2 Oct, step 8 harness gaps), never run on a GPU.** The eager
   2B host and the cascade host (4B graphs + 2B eager on one H100) exist in `modal_ohs3_host.py`. On CPU: the PRISM-X
   path is active and changes the answer, GraphRunner refuses it, served == batch read, the cascade == the offline
   rule on the same reads, served cascade scores == offline cascade scores. Untested on an H100: the 2B's eager
   latency, the cascade's GPU memory (needs ≥ 12 GB free after the 4B's graphs), the shadow heads (H2) in serving
   (the Mac's transformers has no Qwen3.5 Gated DeltaNet, so the CPU test installs authority + option head only).
3. **The C1 throughput: load test built and CPU-tested, never run on a GPU.** `load_test_c1.py` (dev rows,
   length-matched, token check, levels 1-16, sustained = best level with 0 failures). The serving policy is the
   served one (one request at a time under the GPU lock); a batching server would be cheaper but is not what is timed.
   The dev pool has 387 choice rows with ≥ 10 options; with the 2view readout the match is by type only, so this does
   not limit it (the 2view_ge10 readout would match by options bucket and reuse rows). `--plan` gives the cost from
   the config; its boot minutes (4B 8, 2B 4, cascade 10) are estimates until the first H100 session.
4. **The L4 VM is not a git checkout.** `--config-sha256` ties the run to the committed config, and
   `--code-manifest` stops the run if any code file differs from the Mac's. Every meta file records the code sha256.
5. **2-view doubles the reads on choice rows.** Per A5 this may turn the C3 token-cost win into a tie or loss (about
   $0.039 vs Jev's $0.0384 per 1K).
6. **Batch boundaries on the L4.** The run is cut into 512-row chunks (for resume), in predict()'s length order.
   Batches follow decoder_io.predict's rule inside each chunk, but their boundaries can differ from one unbroken
   predict() call. That changes only padding (tiny bf16 noise), not the readout.
7. **The step-8 "score_ohs fix" is not part of this job.** `score_ohs3.py` is the OHS-3 scorer and is used unchanged.
8. **Dev-only evidence of T and the cascade rule: closed on CPU (2 Oct UTC).** `t_rule_check.py --json` and
   `cascade_rule_fit.py --json` are the config's `T_fit_log` / `tau_fit_log`; `ohs3_lib.check_fit_logs` compares
   every pre-registered value with them (and re-hashes the dev reads on the Mac); the real-mode scripts stop on any
   FAIL or TODO. Still open: (i) the 2B's dev reads must carry view flags in their metas (I_1600's do not: TODO);
   (ii) 5.3's use rule needs the 2B and 4B dev load tests on an H100 before `cascade.run` can be true; on today's
   models the rule picks 70% routing and the use rule would need a 2B costing < 16% of the 4B (READOUT_DEV.md), so
   the cascade is not expected to be served.
9. **PRISM-X weights:** `models.2b.prism_x_sha256` is required and checked at load (L4, Modal eager host) and by the
   preflight. The Modal Volume must hold `models/<2B>/` with `adapter_model.safetensors`, `prism_x.json` and
   `prism_x.safetensors`. If the final 2B was trained on the GCP L4 (as every 2B arm so far), upload its one local
   copy (`backups/gcp_models/<2B>`) to that Volume before the 2B or cascade session; the host checks both sha256.
10. **Jev's token counts come from its API's usage field.** If the OpenRouter route omits it on some calls, the
   timing summary says so (`tokens.complete` false, counted on N of M calls); there is no fallback count (Jev's
   tokenizer is unknown).
