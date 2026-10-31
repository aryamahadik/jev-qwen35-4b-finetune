# L-D deployment measurement plan (C2.1, lane L-D, day 1: Sun 18 Oct 2026)

Builder: Sonnet 5.5 high. Runner (later): Haiku 5.5 low. Skeptic: Sonnet 5.5 high (checklist in section 12).
Scope read: plan sections 6 and 8, the L-D block, ALREADY_TESTED_C1_OPT.md. Nothing else of the plan was opened.

**State today.** Plan, CPU scripts and their tests are written. **No GPU run, no Modal, no model call, no network measurement
happened.** Every GPU or network number the L-D gate asks for is **NOT MEASURED** (section 10). The only new numbers are CPU-side
and say so.

## Tag rule (the L-D gate)

Every number in every output file carries a tag, enforced in code (`scripts/common.py`, `tag()` raises without `n`):

| tag | meaning |
|---|---|
| `author-run` | measured by us; **n required** (calls, rows, boots) and a source |
| `modelled` | computed by a script from tagged inputs; carries seed and input hash; never reported as a measurement |
| `assumed` | a scenario value (load, user location, SLO); no n; the orchestrator or owner owns it |
| `third-party` | price page or docs figure with a fetch date; never author-run |
| `not-measured` | value is null until a run fills it |

## 0. The ten items

| id | item | script | needs GPU/window | n | gate | output |
|---|---|---|---|---|---|---|
| M0a | prompt audit, CPU part (done today) | `dump_prompt_shas.py`, `prompt_audit.py` | no | 11,957 prompts | sha identical, thinking OFF | `out/prompt_audit_c1_cpu.json` |
| M0b | parity tool self-check on real data (done today) | `l4_parity_check.py` | no | 8,143 | tool reproduces the known H100 13 Oct vs 17 Oct result | `out/parity_tool_selfcheck_h100_13oct_vs_17oct.json` |
| M1 | **L4 path parity** vs H100 S1 on dev P | `capacity_ladder.py` (parity pass via round-2 `r2_trial.py`), `l4_parity_check.py` | yes, W1 | 8,143 | argmax agreement >= 99.5% and acc diff <= 0.3 pt (S1 rule) + prompt audit | `out/l4_parity.json` |
| M2 | capacity ladder (closed loop) | `capacity_ladder.py --phases ladder` | yes, W1 | 7 levels x 2 runs x 660 | feeds batching and cost | `out/capacity_L4.json` |
| M3 | open-loop validation of the ladder | `capacity_ladder.py --phases open` | yes, W1 | 5 levels x about 120 s | measured p95 / ladder-predicted p95 <= 1.3 (proposed bar) | same file |
| M4a | cold-start decomposition on the box | `cold_start_probe.py` | yes, W2 | 3+ boots | none (measurement) | `out/cold_start_L4.json` |
| M4b | VM stop/start cycle (scale-from-zero) | `vm_cold_cycle.py` | yes, W4, explicit grant | 3 cycles | none | `out/vm_cold_cycle_od-l4b.json` |
| M5 | keep-alive probe (idle penalty) | `keepalive_probe.py` | yes, W3 | 68 first calls | none | `out/keepalive_L4.json` |
| M6 | region / near-users latency table | `echo_server.py`, `region_latency.py` | no GPU; needs CPU VMs | 200 calls per endpoint per vantage | none | `out/region_*.json`, `out/region_table.md` |
| M7 | cost-script inputs and claim | `cost_calc.py` | no | from M2 | claim states its utilisation | `out/cost.json` |

Windows and estimated GPU wall time (planning estimates from the round-2 TRIALS.md text, not measurements): **W1** parity + ladder +
open loop about 75 min; **W2** cold start about 25 min; **W3** keep-alive about 50 min; **W4** VM cycle about 30 min (explicit grant). They
run only at **queue priority 5**: after C2's grid reads, after C2 reads of C2.1 rows, after L-E dry runs and the voice pool. L-0
publishes the queue plan by Wed 21 Oct; L-D registers W1 to W4 in it and starts nothing itself.

## 1. Facts we already have (all tags from the source files)

| fact | value | tag | source |
|---|---|---|---|
| Cold start of S1 on Modal H100 (weights already on the volume) | 131.2 s = 10.0 container up + 121.2 S1 boot | author-run, n=1 | `speed/opt_c1_20261017/results/session_20261017_065129/.../summary.json` |
| H100 S1 batch-1 latency per decision | p50 29.86 / p95 38.09 / p99 82.12 ms | author-run, n=640 | `h100/TRIALS_H100.md` arm A |
| H100 S1 traffic-like throughput, c64 | 325,826 dec/h (two runs 325,974 / 325,677); latency at c64 p50 682 ms, p95 850-911 ms | author-run, n=1,320 | same, `r2_a/measure.json` |
| Cost at 100% utilisation | $0.01349 per 1K at $4.3952/h | modelled from the two lines above (+ third-party rate) | `cost_calc.py` reproduces the table |
| Jev cost | $0.0234 per 1K (list $0.042/M input x about 557 billed tokens; 200 calls spent $0.0047) | author-run, n=200 (an estimate from usage, not an invoice) | `RESEARCH_PLAN.json`, `jev_sample` |
| Break-even utilisation vs Jev | 57.7% (the "about 59%" of the plan) = 192k dec/h = 53 dec/s per H100 | modelled | `out/cost_h100_example.md` |
| Laptop to Modal us-west e2e, c=1 | ours p50 135.65 ms (network 94.0, server 39.0); Jev p50 150.72 ms | author-run, n=86 ours, n=200 Jev | `summary.json` e2e, `jev_sample` |
| Laptop to a US-east container, one POST | p50 39.7 ms (Azure), 46.2 ms (GCP); new connection adds connect 36.5 + TLS 41.9 ms | author-run, n=60 / n=8 | `netprobe_20261017_062317.json` |
| Rendered prompts, `decoder_io` path vs `fastcore` server path | identical sha for all 11,957 prompts of the 8,143 P decisions; thinking OFF in 11,957 / 11,957 | author-run, n=11,957 (CPU, tokenizer only) | `out/prompt_audit_c1_cpu.json` |
| Reference stability: H100 S1 on 13 Oct vs 17 Oct | argmax agreement 99.9877% (1 flip, Wilson lower bound 0.9993), accuracy 81.48 vs 81.49, max abs dp 0.0398 | author-run, n=8,143 | `out/parity_tool_selfcheck_...json` (this is a TOOL self-check, not an L4 result) |
| GCP quotas | one GPU in total (od-l4 us-central1-a OR od-l4b us-east4-c, never both); 16 CPUs in total (od-l4b 8 + od-cpu1 8, so full) | third-party (our own gcp_run.sh notes) | `zed_orch/gcp_run.sh` |

## 2. Findings from the CPU work (read these before the windows)

**F1. The 59% break-even and the latency target are measured at different points of the curve.** The 59% (here 57.7%) is a share
of throughput at closed-loop concurrency 64, where the median decision takes 682 ms. The advertised p50 near 30 ms is batch 1,
which serves 113,350 dec/h (3.6e6 / mean 31.76 ms) = **34.8% of that saturated throughput**. So a single-stream H100 is below the
break-even by construction, however much traffic arrives. The question for L-D is therefore not "how much load" but "what is the
highest throughput whose p95 still meets the latency SLO, as a share of T_sat" (the **utilisation ceiling under the SLO**,
`batching_plan.py`). Only the M2 ladder can answer it; the H100 has two points (c1, c64) and no knee yet.

**F2. Dedicated-GPU cost needs a lot of traffic.** With the H100 numbers (modelled, 7 days, seed 0, `out/warm_pool_h100_example.md`):
solo developer $8-10 per 1K, a 20-agent team about $0.75 per 1K, a 500-agent company about $0.038 per 1K (35% billed utilisation,
still above Jev's $0.0234), and only a flat 60 dec/s load reaches $0.0203 (66%, below Jev). Break-even is about 53 dec/s per H100.
The load scenarios are ASSUMED (section 7); the expected load is the orchestrator's or owner's input.

**F3. The 131 s cold start is a Modal number.** On GCP it is unmeasured. It decomposes (M4a/M4b) into VM start, ssh, weights load
(disk-cold vs page-cache-warm), CUDA-graph capture (the H100 log shows 58 prefill-graph steps, the first one 25 s) and first-request
lazy init. The warm-pool design depends on which part dominates.

**F4. C2.1 has no H100 reference.** An H100 S1 pass on the new weights is paid GPU time and Modal is forbidden. The L-D gate for
C2.1 therefore runs against the HF-adapter read on the free L4 (plan section 6 base rule, same 99.5%). An H100 reference is a
money question (section 9, Q1).

**F5. The round-2 precedent.** On 17 Oct the permission classifier refused the one action every L4 trial needs, stopping the
production server on od-l4b (TRIALS.md, "BLOCKED"); the server holds 21 of the L4's 23 GB. The plan does not look for a route
around that: W1 to W4 each need a grant from the orchestrator (section 9, Q4). Without it M1 to M5 stay NOT MEASURED.

## 3. Warm-pool design (output 1)

Goal: no user request waits for a cold start in the hours that matter, at the lowest dollars per decision.

| option | what | cold start seen by a request | cost while idle | measured by |
|---|---|---|---|---|
| A warm floor | 1 instance always on; more are added when load rises | none, except during scale-up | full rate x idle hours | warm_pool_sim, M2 |
| B scale to zero + keep-alive window | instances end after `idle_timeout_s` without load | first request after a gap waits the whole cold start | rate x window per wake | M4a, M5 |
| C stopped-VM standby | VM stopped when idle (disk only), started on demand | VM start + ssh + server boot | disk only | M4b |
| D pooled fleet | all customers share the same instances | rare (floor is shared) | shared | needs the real load mix |

Rules the plan applies (the owner may change the thresholds, not the method):

1. **Keep-alive window.** Dollar-optimal window = cold-start length (ski-rental; `warm_pool_sim.ski_rental`): keeping an idle
   instance longer than one cold start costs more than restarting it. A floor is a latency decision, not a dollar decision: it is
   chosen when the cold-hit share at the expected load is above the owner's tolerance (assumed input; default 0 requests in business hours).
2. **Policy grid** (`warm_pool_sim.py`): min_warm in {0, 1} x idle timeout in {0, 60, 300, 900, 1800, 3600, 7200} s, per load scenario,
   7 simulated days. Output per policy: $ per 1K, billed utilisation, cold-hit share, instance starts, added wait p50/p95/p99/max.
3. **Inputs the model needs and who fills them:** `cap_dph` from M2 (T_sat), `cold_start_s` from M4a (+ M4b for option C),
   `rate_usd_h` from the GCP price page on the claim day (third-party). Until then the run for `l4_gcp_s1` refuses to start
   (null inputs stop it by design); `h100_modal_reference` is only a worked example.
4. **Keep-alive probe (M5)** measures what idleness does to the first call: gaps 0, 5, 30, 120, 600 s (n = 30, 20, 10, 5, 3), same
   keep-alive connection, GPU pstate and SM clock sampled before the first call, connection resets counted (uvicorn's default
   keep-alive timeout is 5 s, to be verified in our server's args; a client idle longer than the timeout reconnects, at about
   3 round trips with TLS, 78 ms of connect + TLS on the 17 Oct US-east path).
   Add the 1800 s gap (n = 3, +90 min) only if the 600 s gap shows a penalty.
5. **Option C (M4b)** is run only with the explicit grant, because it stops the VM and the production server on it. Suspend/resume
   for GPU VMs is NOT assumed; check the GCP docs before relying on it.
6. **Decision recorded in the report:** the chosen policy, the cold-hit share and $ per 1K at the stated scenario, and which inputs were
   measured and which assumed. If M4 is not run the report says "cold start on GCP not measured; 131.2 s is Modal, n=1".

## 4. Region / hosting-near-users latency table (output 2)

Method (`region_latency.py`, `echo_server.py`): same client, concurrency 1, one keep-alive connection per endpoint, TCP_NODELAY,
all endpoints **interleaved** in a seeded random order, 20 warm-up calls discarded, n = 200 calls per endpoint per vantage,
nearest-rank percentiles, failures counted. Connection setup (DNS, TCP, TLS) is measured separately on 10 fresh connections.
`network_ms = client_ms - server_ms`. Two endpoint kinds: `echo` (a CPU VM, network floor, model-free) and `decide` (the real
server). Echo rows get an estimated e2e = network p50 + the L4's batch-1 server p50 (author-run from M2 c=1, with its n), tagged
MODELLED, until a real `decide` endpoint exists in that region.

Vantages (a vantage stands for where users are; which one is the owner's input): (1) this laptop; (2) free-credit CPU VMs in other
zones used as clients (od-cpu1 in us-east4-c can probe us-central1-a while the L4 od-l4 runs there). The laptop reaches US-east
containers at about 40-46 ms and us-west at about 94 ms (netprobe, n=60 and n=86), so the laptop is on the east side.

Regions reachable today: **us-east4 (od-l4b) and us-central1 (od-l4), one at a time**, because the GPU quota is 1. Echo VMs in more
zones need CPU quota (the 16 are used); that is a quota question for the orchestrator (Q3), not a purchase.

Reading the table: the winner per vantage is the lowest network p50 **and** p95; two regions are "equal" when their p50 differ by
less than the run-to-run spread, so the run is repeated at a second time of day (the spread is part of the report). A region pin is
taken only if it is not more expensive per GPU-hour (Modal's narrow-region 1.75x multiplier made a pin worse than Jev on cost; GCP
zones are compared by their list price on the claim day). Clients must reuse connections: a fresh connection added 194 ms on the 17 Oct path.

Jev comparison: **not done by these scripts.** `hosting/client_bench.py` interleaves ours and Jev from the same client, a paid API
call, run by the orchestrator in a window of its choice; the claim wording uses that run only (plan C7-C8). AA's per-task medians
(Celeris 63 ms, Jev 127 ms) are context, not a bar.

## 5. L4-path parity check (output 3), M1

**What is compared.** Candidate = SGLang S1 on the L4 (od-l4b), merged bf16, production flags (`--attention-backend triton`,
mem-fraction 0.8, max-running 32, max-mamba 128; recorded from `/server_info`, the trial server's diff against the production snapshot
must show only the intended differences), on the dev parity set **P** (8,143 decisions, sha256 `95764485...`, 4,329 yes/no + 3,814 choice).
Reference = the H100 S1 answers of 17 Oct (`h100/results/session_20261017_161152/.../r2_a/answers_P.jsonl`, c32 pass), second
reference the SPEED-2 S1 answers of 13 Oct (`speed2_20261013/S1/answers_P.jsonl`); they agree with each other at 99.9877%.

**Rule (identical to S1; `hosting/speed_bench.compare`).** On all 8,143 rows: argmax agreement >= 99.5% (a missing answer counts
as a disagreement) **and** |accuracy difference| <= 0.3 pt (gold from the dev splits via `--gold-dir lean/data`). Added by plan v3:
prompt audit PASS (identical rendered-prompt sha in trainer, gate and server; thinking OFF in every rendered prompt). Reported next to
the gate: Wilson 95% lower bound (bar 0.995; buckets below about 770 rows are flagged underpowered, as in round 2), per view type and
options bucket, max/mean/p99 |dp|, the flips with the reference margin (near-tie flips are BF16 noise), and a **self-floor**: the same
L4 server read again at a different batch size (c16 vs c4, full P; the H100 floor was 2 flips in 8,143).

**Verdict values.** PASS, FAIL (which clause), INCOMPLETE (missing gold, audit or rows). A FAIL is reported, not repaired: FP8
stays out of scope (98.38% block-FP8 is recorded failed); the remedy is an owner question about another GPU type (Q1), never a silent
change of flags. Any re-render (template, card, option order) gets a new parity record.

**Commands** (on od-l4b, except W4; `$L` = `~/repo/opendecide-data/lean`, `$D` = `$L/c2_build/c21_deploy`, `$O` = `~/opt_r2`, `PY=~/od/bin/python`):

```
# CPU, before the window (VM or Mac): the audit
$PY $D/scripts/dump_prompt_shas.py --source gate   --renderer decoder_io --tokenizer ~/lean/models/q35_4b_main500k --p $O/data/P.jsonl --out $D/out/dump_gate.jsonl
$PY $D/scripts/dump_prompt_shas.py --source server --renderer fastcore   --tokenizer ~/lean/models/q35_4b_main500k --p $O/data/P.jsonl --out $D/out/dump_server.jsonl
$PY $D/scripts/prompt_audit.py --dumps $D/out/dump_gate.jsonl $D/out/dump_server.jsonl --expect-n 11957 --out $D/out/prompt_audit.json
#   for C2.1 add the trainer's dump (written by the training side with the same schema) as a third file after --dumps
# W1 (about 75 min): one window, one trial server with production flags (port $TRIAL_PORT, never 30000)
bash $D/scripts/vm/ld_window.sh W1 -- "
  $PY -B $O/r2_trial.py --name ld_parity --port \$TRIAL_PORT --backend generate --phases parity --parity-conc 16 --extra-parity-conc 4 &&
  $PY $D/scripts/capacity_ladder.py --port \$TRIAL_PORT --tokenizer ~/lean/models/q35_4b_main500k --work-dir $O/data --oc1-parent $O --phases ladder,open --out $D/out/capacity_L4.json"
# CPU, after: the verdict (floor = the same server's c4 pass)
$PY $D/scripts/l4_parity_check.py --cand $O/results/ld_parity/answers_P.jsonl --ref $L/speed/opt_c1_round2_20261017/h100/results/session_20261017_161152/volume/session_20261017_161152/r2_a/answers_P.jsonl \
    --ref2 $L/speed/speed2_20261013/S1/answers_P.jsonl --floor $O/results/ld_parity/answers_P_c4.jsonl --gold-dir $L/data \
    --prompt-audit $D/out/prompt_audit.json --cand-info $O/results/ld_parity/server_info.json --out $D/out/l4_parity.json
# W2 (about 25 min): cold start; the probe starts and stops its own trial servers (port 30011)
$PY $D/scripts/make_probe_body.py --tokenizer ~/lean/models/q35_4b_main500k --work-dir $O/data --oc1-parent $O --out $D/out/probe_body_N0.json
bash $D/scripts/vm/ld_window.sh W2 --no-trial -- "$PY $D/scripts/cold_start_probe.py --name ldcold --port 30011 \
  --start-cmd 'bash $O/trial_server.sh ldcold 30011' --stop-cmd 'bash $O/trial_stop.sh ldcold' --log-file $O/logs/ldcold.server.log \
  --body-file $D/out/probe_body_N0.json --repeat 3 --drop-caches-every 3 --out $D/out/cold_start_L4.json"
# W3 (about 50 min): keep-alive on a trial server
bash $D/scripts/vm/ld_window.sh W3 -- "$PY $D/scripts/keepalive_probe.py --url http://127.0.0.1:\$TRIAL_PORT --path /generate \
  --body-file $D/out/probe_body_N0.json --gaps 0:30,5:20,30:10,120:5,600:3 --warm-k 5 --out $D/out/keepalive_L4.json"
# W4 (about 30 min, explicit grant; from the Mac): VM stop/start cycles, then production restored
PROD='~/reads/start_server.sh --max-running 32 --max-mamba 128 --mem-fraction 0.8 --extra-args "--attention-backend triton"'   # as prod_start.sh
LD_WINDOW=W4 LD_VM_CYCLE_OK=yes ~/Documents/jev/opendecide-data/.venv/bin/python $D/scripts/vm_cold_cycle.py --vm od-l4b --cycles 3 --go \
  --server-start-cmd "$PROD" --restore-cmd "$PROD" --out $D/out/vm_cold_cycle_od-l4b.json      # $D = the Mac path of c21_deploy here
```
Haiku runner rules: it pastes exactly these commands, never edits a script, stops and reports after 2 failed attempts, and never
touches a process it did not start. Each result file is read back and its tag checked before the next step. The floor for the parity
check is the same server at c4 (the H100 floor, c32 vs c64, was 2 flips in 8,143).

**C2.1.** After the weights exist: same commands with `--tokenizer` and the merged C2.1 folder, reference = the HF-adapter read on
the L4 (Q1 decides whether an H100 reference is bought). Repeating M1 for C2.1 is part of the GO #2 package; the scripts take the model
folder as a parameter and contain no C1 constants besides the P sha.

## 6. Batching plan to keep utilisation above about 59% (output 4), M2 and M3

**Definition (the C1 cost table's):** utilisation u = served decisions per hour / T_sat, T_sat = the instance's saturated
throughput on the call mix; $/1K = rate / (T_sat u) x 1000; break-even u* = cost at 100% / Jev $ per 1K (57.7% on the H100 vs
$0.0234; recomputed for the L4 by `cost_calc.py`; against other Jev units it is 23% or 40%, so the claim names its unit).

**M2 ladder.** c in {1, 2, 4, 8, 16, 32, 64}, N workload (660 traffic-like dev decisions, each once), 2 runs per level, caches
flushed before each, loopback client (so latencies are server-side), GPU busy share sampled at 0.5 s. Output points
`{c, dph, p50_ms, p95_ms, n}` go into `inputs/capacity_curves.json` (curve `l4_gcp_s1`). Same definitions as the H100 arm A, so the
L4 and H100 numbers are comparable. T_sat = best level with 0 failed calls.

**M3 open loop.** Poisson arrivals at 0.25, 0.5, 0.6, 0.75, 0.9 x T_sat for 120 s each, one fresh P decision per arrival,
latency from the **scheduled** arrival (client lag is reported and must stay under 5 ms, else the level is void). `batching_plan.py
validate` compares measured p95 with the ladder prediction; ratio at or below about 1.3 means the closed-loop model is a usable (conservative)
predictor, and the plan is then trusted for sizing.

**Plan outputs (`batching_plan.py plan`).** (1) the **utilisation ceiling under the SLO** = throughput at the highest ladder level
with p95 <= SLO, as a share of T_sat; if it is below u*, interactive traffic alone cannot beat Jev on cost within the SLO. (2) per
load scenario, for N = 1..12 instances: mean utilisation, share of time at or above u*, peak p95, instances needed at peak, and the
background traffic per hour that would lift the mean to u*. (3) minimum steady load for one instance to hold u* (H100 example:
192,237 dec/h = 53.4 dec/s).

**Levers, in the order they are tried** (each is exact: no change to answers):
1. **Right-size to the load**: a warm floor of 1 off-peak, autoscale to the busy hours (`warm_pool_sim`), never an idle spare.
2. **Pool every customer on one fleet**: the floor is paid once, utilisation is the sum of the loads.
3. **Fill the gaps with a lower-priority class** (evals, nearline checks, retries): LinkedIn reports about +25% effective throughput
   from this shaping (their figure, third-party). Requires a priority option in the server; **check `server_args` of SGLang 0.5.20
   before relying on it** (not verified). Without it the same effect is a client-side admission rule (send background work only when
   the interactive queue is empty).
4. **Bundle the questions of one agent step into one call**: the H100 batch-8 cost is 11.3 ms per decision against 32 ms at batch 1
   (author-run, 17 Oct). The ladder counts decisions, so bundling moves a deployment to the right on the same curve.
5. Choose the SLO as a number the owner signs: `--slo-p95-ms` is ASSUMED until then (60 ms server p95 is used only as an
   illustration: the plan's end-to-end p50 target of 75-85 ms minus about 40 ms of network).

Not part of L-D: FP8 and other answer-changing speedups (owner-reserved, section 10 R8/R12 of the plan).

## 7. Load scenarios (ASSUMED; replace with the expected load)

`inputs/warm_pool_inputs.json` holds five, each tagged `assumed` with its reasoning: solo developer (peak 0.3 dec/s), small team
(peak 4/s), company (peak 100/s), CI burst (30/s for 10 min every 2 h), flat 60/s. The files read for this task do not state the
expected load; the orchestrator or owner supplies it (Q2), and the scenarios are edited in that one file.

## 8. Cost-script inputs for GO #2 (output 5), M7

`cost_calc.py --inputs inputs/cost_inputs.json` (L4 target; every ours-input is `not-measured` today, so it prints
"claim NOT READY" and lists the blockers) and `inputs/cost_inputs_h100_reference.json` (worked example that reproduces the published
$0.01349 per 1K and the 57.7% break-even; tests pin both).

| input | value today | filled by | tag it must carry |
|---|---|---|---|
| `ours.sustained_dph` | null | M2, best level with 0 failed calls | author-run, n |
| `ours.rate_usd_h` | null | GCP L4 VM list price incl. CPU, RAM and disk, fetched on the claim day | third-party + fetch date |
| `ours.mix` | N traffic-like | fixed | text |
| `ours.cash_rate_usd_h` | 0 (free credit) | reported separately, never used for the claim | assumed |
| `jev.usd_per_1k_measured` | 0.0234 | already measured | author-run, n=200 |
| `jev.usd_per_m_input_tokens`, `tokens_per_decision` | 0.042, 557 | docs 18 Oct; usage field | third-party; author-run n=200 |
| `claim_utilisation` | null | owner | any claim must name it |

The generator refuses a claim without the utilisation, the GPU and price, the call mix and the Jev unit; it always ends with "Hosting
cost only; no operations cost". It compares with both Jev units (measured, and list price x tokens) side by side.

## 9. Questions for the owner or orchestrator (nothing below was asked or done)

- **Q1 (money, R1-type).** Any GPU type other than the free L4 costs money and is never bought by default. Two uses: (a) a cheaper or
  faster GPU if the L4 fails M1 or its $ per 1K is above Jev at every plausible load; (b) one H100 S1 reference pass on the C2.1
  weights (about 30-35 min, Modal-class prices; Modal is forbidden, so another provider) for the cross-GPU parity statement. Candidate
  cards for (a): any 24-48 GB card that fits the 9 GB bf16 model; their speed is unmeasured, so a card is bought only after a short
  paid parity+ladder session is approved with a cap.
- **Q2 (input).** The expected load (decisions per second at peak and mean) and where the users are (the vantage for M6), and the
  latency SLO number for `--slo-p95-ms`.
- **Q3 (quota).** One more CPU VM in a third zone for an echo server needs CPU quota (16 of 16 used); alternatively stop od-cpu1 for
  the hour. No spend.
- **Q4 (permission).** Grant W1, W2, W3 (and W4 for the VM stop/start cycle): each stops the production server on od-l4b for its length
  and restarts it exactly as `prod_start.sh` does, only when no C2 read job runs. Without the grant M1 to M5 remain NOT MEASURED. W4 additionally stops the whole VM and needs its own yes.

## 10. Not-measured ledger (what the L-D report must say today)

| output | status | needs |
|---|---|---|
| L4 parity vs H100 S1 | NOT MEASURED | W1 |
| L4 capacity ladder, T_sat, utilisation ceiling | NOT MEASURED | W1 |
| open-loop validation | NOT MEASURED | W1 |
| cold start on GCP/L4 (server boot; VM cycle) | NOT MEASURED (131.2 s is Modal, n=1) | W2, W4 |
| keep-alive idle penalty | NOT MEASURED | W3 |
| region table (any region) | NOT MEASURED | M6 run; Q3 for a third zone |
| L4 $ per 1K, break-even, cost claim | NOT MEASURED, claim_ready false | M2, price page, Q2 |
| trainer-side prompt sha (C2.1) | NOT MEASURED | training side writes `dump_trainer.jsonl` |
| prompt audit, gate vs server path, thinking OFF | **measured, PASS, n=11,957 (CPU)** | done |

## 11. Files

`c21_deploy/` (all paths relative):

| file | role |
|---|---|
| `scripts/common.py` | tags, nearest-rank percentiles, Wilson, refusals (Modal, port 30000, "ohs"), window guard |
| `scripts/warm_pool_sim.py` | warm floor / keep-alive policy grid on load scenarios (modelled) |
| `scripts/cold_start_probe.py`, `scripts/vm_cold_cycle.py`, `scripts/keepalive_probe.py` | M4a, M4b, M5 |
| `scripts/make_probe_body.py` | one real /generate body for the probes (tokenizer only) |
| `scripts/capacity_ladder.py` | M2 and M3 |
| `scripts/batching_plan.py` | ceiling under SLO, per-scenario instance table, validation of M3 |
| `scripts/echo_server.py`, `scripts/region_latency.py` | M6 |
| `scripts/dump_prompt_shas.py`, `scripts/prompt_audit.py`, `scripts/l4_parity_check.py` | M0a, M1 |
| `scripts/cost_calc.py` | M7 |
| `scripts/vm/ld_window.sh` | the window wrapper (C2 wait, stop production, run, always restore) |
| `inputs/*.json` | tagged inputs; `endpoints.template.json` is a template |
| `tests/test_ld.py`, `tests/test_ld_e2e_stub.py` | 20 + 1 CPU tests (the second drives the real round-2 harness against its model-free stub server) |
| `out/` | today's CPU outputs (tagged) and the worked H100 examples (labelled as examples) |

Run the tests: `cd c21_deploy && ../../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/`.

## 12. Skeptic checklist

1. Every number in `out/*.json` has a tag; author-run has n. (`cost_calc.py --check`, `common.check_tagged`.)
2. `l4_parity_check.py` uses the S1 rule and reproduces the known H100 13 Oct vs 17 Oct result (1 flip, 99.9877%, acc 81.48).
3. Argmax and accuracy definitions equal `gate_dev.argmax_label` and `gate_dev.score` (ties: first on argmax, wrong on score).
4. No script can reach port 30000, a Modal host, an "ohs" path, or an LLM API; GPU-side scripts refuse without `LD_WINDOW`.
5. `ld_window.sh` restores production on every exit path (trap) and refuses port 30000 for its trial server.
6. The warm-pool model's limits are stated (fluid approximation; scenarios assumed) and the L4 profile cannot run with null inputs.
7. Nothing here claims a cold start, a latency, a region result or a cost for the L4 or GCP: all NOT MEASURED.
8. The F1 arithmetic (113,350 dec/h at batch 1; 34.8% of the c64 throughput) is derived from the two stated author-run numbers.
