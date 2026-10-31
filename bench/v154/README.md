# JevBench v1.5.4: unofficial run of our models (public items, official formulas)

This folder measures where our two current models stand on the latest public JevBench. It is a side check
and does not touch the main plan. It never writes into `~/lean` or `opendecide-data/lean`. The run script
refuses to start while another process is using the GPU, such as a training run. Nothing is submitted.
Report results as "our run of the public items, official v1.5 formulas". Never call them a leaderboard position.

| Model | Adapter | Base @ revision | Layout / style |
|---|---|---|---|
| 4B-E | `q35_4b_pxE` | Qwen/Qwen3.5-4B @ 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a | schema_branch_mark / cygnet |
| 2B PRISM-X I | `q35_2b_armI_1600` | Qwen/Qwen3.5-2B @ 15852e8c16360a2fea060d615a32b45270f8a8fc | schema_branch_mark / cygnet + PRISM-X I |

## What v1.5.4 is (and what the public repo has)

- **Leaderboard:** `benchmarkheaven.com/api/jevbench/v1.5.4`, snapshot in `leaderboard_v154.json` (fetched 30 Sep 2026). It uses protocol `jevbench::v1.5`, 1,624 decisions per system (904 open, of which 601 are published, plus 720 sealed), and ranks 106 systems. Jev 1.13.0 is #3 at 72.13 (I 72.0 / C 88.0 / S 83.8 / $ 54.7). Cygnet (73.70) and Winnow-12B (73.23) are "joint leaders".
- **Repo:** there is no `v1.5.4` tag; the newest tag is v1.4.2.2. `jevbench_v154/` is `main` @ `bb05a33` (29 Sep). It holds the frozen v1.5 method docs. Their SHA-256s match the API: method `c25d3d8b…`, pricing `2fc44459…`, headline amendment `752ddccc…`.
- **Harness code:** `jevbench/` (runner, scoring, tasks, `adapters/base.py` DecisionResult) is byte-identical to v1.4.2. `git diff v1.4.2 HEAD -- jevbench datasets` is empty, so `jevbench_od.OpenDecideAdapter` works unchanged.
- **Public items:** unchanged, the same 231 v1.2 items: easy 48, standard (`original`) 72, hard 111. By type that is Choice 139, Noul 74, Score 18. The 370 new v1.5 open items are **not** in the repo, and neither is the v1.5 scorer. PR #162 says so too: "does not ship the historical v1.5.2 task bundle or its compatible scorer". The missing items are:
  - 120 drafts: tool-call guardrail Noul, lead-qualification Score, and state-tracking items;
  - 250 items drawn from the sealed pool.

  If they are published later, pass them with `--extra-items`.

## Changes from v1.4.2 to v1.5 (scoring)

| | v1.4.2 | v1.5.4 |
|---|---|---|
| Decisions per system | 534 open + 308 sealed (hard-style) | 904 open (601 published) + 720 sealed, same tier mix as the open set, freshly drawn from a 2,805-item pool |
| Sealed share of Intelligence | 20 % | **50 %** |
| Tier weights easy / std / judge / hard | 14/28/28/30 | **10/20/30/40** (renormalised when a tier has no items) |
| Request types | choice-centred, argmax accuracy | Choice, Noul and Score each scored natively, **1/3 each** (headline amendment; the frozen text said 50/25/25) |
| Chance baseline | per tier | **per item**: Choice 1/options, Noul 0.5, Score = uniform-guess nMAE |
| Noul | argmax | **P(yes) ≤ 0.2 is No, ≥ 0.8 is Yes, in between is an abstention and counts wrong** |
| Score | argmax level | nMAE of the **expected level** vs chance nMAE |
| Overfit penalty | public-sealed gap > 25 raw points | gap − G_med (5.19) > 8 CC points, slope 1 |
| Calibration | ECE (hard) + TVD | typed: Choice ECE(hard)+TVD; Noul ECE on P(yes); Score (1−nRPS + top-level ECE)/2; 1/3 each |
| Speed | same formula | same formula, measured on open **standard + judge** items; self-hosted ×2 + 0.15 s (unchanged) |
| Cost | same formula | same formula, tokens pooled over 1,624 decisions. New price rules: a price counts after 30 days on the list, a base-model price floor applies, and the frozen Qwen3.5-4B reference is DeepInfra $0.03/M in, $0.15/M out |
| Composite | harmonic with gates | A (headline) 25/25/25/25, B 40/20/20/20, C = A with Intelligence gate 60; quadratic gates below 50 on I, S, $ |
| Ties | none | paired stratified bootstrap (B=2000, seed 15); "#1" only if significant |

There are no new question types and no new tiers. There are new families: state tracking (all types), tool-call guardrails (Noul) and lead qualification (Score).

## Files

- `run_v154.py`: runs one adapter on the public items through the official `Runner`. It loads with `decoder_io.load(base, adapter=…, revision=…)`, so layout, style and PRISM-X come from `train_meta.json` / `prism_x.json`. Before using the GPU it checks every prompt: the message must follow `decoder_io.LAYOUT`, and PRISM-X must be able to find its token roles. It writes `bench/runs/v154_<name>/{results.jsonl, manifest.json, ledger.jsonl, raw/}`.
- `score_v154.py`: applies the v1.5 formulas to public items. It prints every axis, composites A/B/C, a separate **Intelligence-only** column (the fair comparison with Jev) and the per type × tier table. It also prints Noul abstentions, typed calibration parts, a paired bootstrap vs the reference run, and the published board as context. `--check-leaderboard` recomputes every published v1.5.4 row from its published parts. All 108 rows match to 1e-14, which confirms the aggregation, penalty, calibration combination, speed, cost, composite and view formulas.
- `v154lib.py`: the formulas. `lean_snapshot/jevbench_od.py` is a byte copy of `opendecide-data/lean/jevbench_od.py`, the version that follows `decoder_io.LAYOUT`; an older copy on the VM would read our models in the wrong layout. `leaderboard_v154.json` is the API snapshot.

**Jev on the same items:** neither the repo nor the API has Jev's per-item probabilities. The repo has v1.2 argmax outcomes only, and the v1.5 Noul and Score rules need probabilities. We therefore use our own Jev 1.13 runs `bench/runs/jev_p1` and `jev_p2` (26 Sep, same 231 items, same dataset hash `dc3995d8…`). They agree with the repo's per-item Jev outcomes on 229/231 and 230/231 items. The published Jev axes are on 1,624 items and are shown only as context.

## Commands

Local (Mac) preparation: refresh the adapter snapshot, then copy the code to the VM. Only do this when the L4 is free. It runs no GPU work, but it needs the VM to be running.

```bash
cd ~/Documents/jev
cp opendecide-data/lean/jevbench_od.py bench/v154/lean_snapshot/jevbench_od.py
P=system-one-509903; Z=us-central1-a
gcloud compute ssh od-l4 --zone $Z --project $P --command 'mkdir -p ~/bench/runs'
gcloud compute scp --recurse bench/v154 od-l4:~/bench/ --zone $Z --project $P
gcloud compute ssh od-l4 --zone $Z --project $P --command \
  'git clone -q https://github.com/fstandhartinger/jevbench.git ~/bench/jevbench_v154 && git -C ~/bench/jevbench_v154 checkout -q --detach bb05a335bc809e61b20c0f745d25499a82b326fc'
# (without git on the VM: gcloud compute scp --recurse bench/jevbench_v154 od-l4:~/bench/ --zone $Z --project $P)
```

On the VM (`gcloud compute ssh od-l4 --zone us-central1-a --project system-one-509903`):

```bash
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv   # must list nothing (no training running)
sha256sum ~/lean/decoder_io.py ~/lean/prism_x.py   # local: 8ba8ff4f… and 3c4425bf… (recorded in the manifest either way)
export HF_HOME=${HF_HOME:-$HOME/hf}
cd ~/lean
# 1) CPU pre-flight: builds and checks all 231 prompts with the VM's code (seconds, no GPU)
~/od/bin/python ~/bench/v154/run_v154.py --lean ~/lean --model ~/lean/models/q35_4b_pxE --base Qwen/Qwen3.5-4B \
  --revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a --dry-run
~/od/bin/python ~/bench/v154/run_v154.py --lean ~/lean --model ~/lean/models/q35_2b_armI_1600 --base Qwen/Qwen3.5-2B \
  --revision 15852e8c16360a2fea060d615a32b45270f8a8fc --dry-run
# 2) the runs (serial, one decision per request, eager; about 5 min each)
~/od/bin/python ~/bench/v154/run_v154.py --lean ~/lean --model ~/lean/models/q35_4b_pxE --base Qwen/Qwen3.5-4B \
  --revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a 2>&1 | tee ~/bench/runs/v154_q35_4b_pxE.log
~/od/bin/python ~/bench/v154/run_v154.py --lean ~/lean --model ~/lean/models/q35_2b_armI_1600 --base Qwen/Qwen3.5-2B \
  --revision 15852e8c16360a2fea060d615a32b45270f8a8fc 2>&1 | tee ~/bench/runs/v154_q35_2b_armI_1600.log
```

Optional: add `--graphs` to the 4B run for a CUDA-graph speed number. This is not possible for PRISM-X, and it is memory-heavy on the 23 GB L4.

Fetch and score (Mac):

```bash
cd ~/Documents/jev
for N in v154_q35_4b_pxE v154_q35_2b_armI_1600; do
  gcloud compute scp --recurse od-l4:~/bench/runs/$N bench/runs/ --zone us-central1-a --project system-one-509903
done
python3 bench/v154/score_v154.py v154_q35_4b_pxE v154_q35_2b_armI_1600 jev_p1 jev_p2 --ref jev_p1 \
  --json-out bench/runs/scores_v154_all.json
python3 bench/v154/score_v154.py v154_q35_4b_pxE v154_q35_2b_armI_1600 jev_p1 --ref jev_p1 --items B  # confirmation half
```

The run kinds are read from the manifests: our runs are `gpu` (×2 + 0.15 s) and Jev is `api`. The prices are the frozen Qwen3.5-4B reference ($0.03/M in, $0.15/M out; our readout generates 0 tokens) and Jev's list price ($0.042/M in). The 2B uses the 4B reference because the board shows no Qwen3.5-2B rate. Override with `--kinds` / `--prices` / `--out-prices`.

## CPU smoke tests (done on the Mac, outputs in `smoke/`)

```bash
cd ~/Documents/jev/bench/v154; M=~/Documents/jev/backups/gcp_models
python3 run_v154.py --model $M/q35_2b_armI_1600 --base Qwen/Qwen3.5-2B --revision 15852e8c16360a2fea060d615a32b45270f8a8fc \
  --dry-run --out smoke/v154_q35_2b_armI_1600_dry            # all 231 prompts built + checked (PRISM-X spans found)
python3 run_v154.py --model $M/q35_4b_pxE --base Qwen/Qwen3.5-4B --revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a \
  --fake-model --limit 5 --out smoke/v154_q35_4b_pxE_fake    # tiny random Qwen3 on CPU through the real adapter + Runner
cd smoke && python3 make_synthetic.py && python3 ../score_v154.py syn_oracle syn_abstain_noul syn_noisy --kinds gpu,gpu,gpu
python3 ../score_v154.py --check-leaderboard
```

Expected results:
- The synthetic oracle scores Intelligence 100.0.
- The oracle with every Noul answer at P(yes)=0.5 scores Noul CC −100 and Intelligence 33.3. Its composite is gated because I < 50.
- The leaderboard check reports all rows OK.
- An old `jevbench_od.py` (hard-coded text_first) is refused in the pre-flight.
- A machine without `nvidia-smi`, or with a busy GPU, is refused before loading.

## Time and cost

- **Time:** the prompts average 818 tokens (max 4,188). On the L4 (eager, no CUDA graphs) expect about 0.1–0.3 s per decision. Per model that is loading (~1 min) + warm-up (~1–3 min, Triton autotune) + 231 decisions (~1 min). Both models take about 10–15 min, or about 25 min including VM boot and copies.
- **Cost:** about 25 min of g2-standard-8 at about $0.85/h, so about **$0.35–0.5** on the Google credit. There are no API calls and no Modal use. A CPU-only dry-run costs nothing extra.
- **Speed caveat:** the L4 runs eagerly and uses the PyTorch fallback for causal_conv1d, so our Speed axis will be lower than on the H100 / RTX 5090 hardware the board's 4B rows used. For reference, our v1.4.2 H100+graphs runs had a p50 of about 14 ms. Speed is a hardware and serving number: use the Intelligence-only column to compare models.

## Preview with an older model (already scored, CPU only)

`q35_4b_v10_all_g` is the v0.10 4B from the 26 Sep loop (H100 + graphs). It was selected on half A of these items, so the result is optimistic. On the 231 public items under the v1.5 formulas:

| run | Intelligence | Calib | Speed | Cost | Score A | noul abstentions |
|---|---|---|---|---|---|---|
| jev_p1 (Jev 1.13) | 63.2 | 81.2 | 91.4 | 52.5 | 68.80 | 27.0 % |
| jev_p2 (Jev 1.13) | 62.3 | 79.7 | 90.6 | 52.5 | 68.14 | 28.4 % |
| q35_4b_v10_all_g | 70.0 | 82.6 | 95.1 | 60.3 | 74.79 | 14.9 % |

- **Intelligence:** v0.10 is +6.9 over jev_p1, with a 95 % interval of [−3.5, +17.5]. That is a statistical tie, P(better) 0.90.
- **Noul:** the new abstention band costs Jev most. Its public Noul CC is 34, versus 70 under the old argmax rule. Hard Noul is the weakest cell for every system.
