# Pilot runbook: 4B memory, speed and relay proof (FINETUNE_PLAN.md sections 2.4 and 4.2)

*Written 30 Sep 2026. Nothing here has been run on a GPU yet. Budget: **$15 total** (the owner approved $10-15).
This runbook stops before step 0 of the real run (memory rule "pause before 500K"): it never launches
`q35_4b_main500k` itself.*

All commands run from `opendecide-data/lean`. Pilots run attached (no `--detach`), so their result files land in
`logs/pilot/`. Never pass `--detach` to `smoke_heavy` or `speed`: the results are written by the local side.

## 0. Before any GPU (CPU only, free)

1. C1-C5 have landed and `../.venv/bin/python -m pytest -q tests/` is green.
2. `runs/q35_4b_main.json` is final except `micro_tokens`. The four hashed files (`train_decoder.py`, `decoder_io.py`,
   `prism_x.py`, `writeblock.py`) are committed and not edited again until the relay proof (step 4) is done: a checkpoint
   refuses to resume on changed code, so B would fail.
3. Step count: `../.venv/bin/python replay_steps.py --last-batch-at 1,20,100,150,300`
   - must print `"pass_batches": 30457` and `"config_is_one_pass": true` (checked 30 Sep: yes, 10 s).
   - keep the `last_batch` hashes: they are the CPU replay of the GPU's data stream. On 30 Sep they were:
     - step 100: `a27922256bb774f6671c1318651d7553106cc8dce72df338d5d31e682b8ff964`
     - step 150: `c6a0ebadc6f236e4a33bf8bb29df9dae71e4e974b90cedabe43b09f87b77cea8`
     - step 300: `efa08f31d31e0eb4856dcbd93d4323854967ae3fe9c73ee52fd7777a9a7c6658`
4. Heavy batches: `../.venv/bin/python rank_microbatches.py` (about 3 min; writes `pilot/heavy_batches.json`).
   Rerun it if the golden files, `seed`, `style`, `layout` or `perm_twin` change; `smoke_heavy` refuses a stale file.
   Real padded tokens of the heaviest micro-batch in the pass (30 Sep, full pass, pinned tokenizer):

   | micro_tokens | 0 (no packing) | 10240 | 12288 | 16384 | 24576 |
   |---|---|---|---|---|---|
   | heaviest micro-batch | 123,904 | 23,296 | 27,648 | 36,864 | 55,296 |
   | heaviest group with an anchor row | 118,272 | 16,640 | 20,480 | 28,672 | 40,960 |

   The heaviest single unit is 23,296 tokens (gd_conditionalqa_323: 7 sequences x 3,328).
5. Each account: `modal profile list` shows `jaypatil-duke`, `arya-mahadik-ai`, `aryamhd`; the secret `opendecide-keys`
   exists; the same image-builder version (`logs/relay_protocol.md` A.4); a workspace budget is set as a backstop.

## 1. Cost

- H100: $3.95/h, x1.10 for CPU and memory = **$0.00121 per second**.
- Per training step: 3.0 s = $0.0036; 3.5 s = $0.0042; 4.0 s = $0.0048; 4.6 s = $0.0056.
- Per container: about 5-8 min of start-up (image, model load, 1.2 GB data, Triton autotune) = $0.35-0.60.
- Modal L4: about $0.80/h ($0.00024 per second with x1.10).

| Step | GPU | Work | Estimate |
|---|---|---|---|
| 2. Heavy micro-batch memory smoke, 4 values | H100 | 4 x (20 + up to 13 steps), 4 containers | about $2 |
| 3. Speed, 100 real steps per allowed value | H100 | up to 4 x 100 steps, 4 containers | $2.5-4 |
| 3b. `expandable_segments` rerun (only if needed) | H100 | 1 smoke + 1 speed | about $1.3 |
| 4. L4 memory check at the chosen value (optional proxy) | Modal L4 | 1-2 smokes (chosen, plus 10240 if different), about $0.3 each (about 19 s/step x 31 steps + start-up) | about $0.3-0.6 |
| 5. Relay proof A1 + A2 + B | H100 | 900 steps, 4 containers | $5.5-6.7 |
| **Total** | | | **about $10-14.5; cap $15** |

**Stop rule.** After each step, read the usage page of each account. If the total would pass $15, skip the optional
items (3b, 4) first; if it still would, stop and ask the owner.

## 2. Heavy micro-batch memory smoke (H100, account jaypatil-duke)

```
MODAL_PROFILE=jaypatil-duke modal run modal_od.py::smoke_heavy --micro-tokens 10240,0,16384,24576
```

- One container per value. The first runs alone (fills the model and Triton caches on the Volume), the rest in parallel.
- Each container trains the frozen config for the first 20 real steps, then one step per heavy batch: the top 10
  micro-batches, the heaviest unit, the heaviest group with an anchor row and the heaviest table-led group, lightest
  first (so the first out-of-memory marks the limit). Rows come from the real golden file inside the container.
- Output: `logs/pilot/smoke_heavy_h100_mt<N>.json`, with per step: seconds, peak `max_memory_reserved`, the shape of
  every forward, and the CPU prediction.
- Writes nothing to the Volume except the Hugging Face and Triton caches.

**Pass (plan 2.4, per value):** the 3 heaviest real micro-batches, the heaviest single unit, the heaviest group
containing an anchor row and one dense table group all run a full step after 20 ordinary steps, with
`max_memory_reserved` <= 90% of the card. In the JSON: `pass_memory: true` (no out-of-memory, every step
`frac` <= 0.90).

- 0 (no packing) is expected to fail (123,904 tokens in one forward). Its result still answers critic gap 5.
- A value near 90%: rerun it with `--alloc-conf expandable_segments:True` (step 3b); the output gets `_exp`.

## 3. Speed (H100, account jaypatil-duke), only for the values that passed step 2

```
MODAL_PROFILE=jaypatil-duke modal run modal_od.py::speed --micro-tokens 10240,16384,24576 --steps 100
```

- 100 real packed steps of the frozen config (full golden file, resume off), the same batches for every value.
- s/step = mean over steps 10-98. The step-99 checkpoint time (`ckpt_s`) is added back at the config's
  `ckpt_every_min` (`s_per_step_incl_ckpt`), and `full_pass_usd_x1.21` = 30,457 x that x $3.95/h x 1.21.
- Throwaway checkpoints go to `/vol/models/pilot_speed_h100_mt<N>`, never to `models/q35_4b_main500k`.
  Remove them afterwards with the `modal volume rm -r ...` line that the command prints.
- Output: `logs/pilot/speed_h100_mt<N>.json`.

**Checks:**
- no error at start: the trainer raises unless trainable = 32,464,896, kd_targets = 43,363, kd_full = 238 and every
  startup check passes (the Modal log prints them);
- `probe_ok: true`;
- `last_batch` equals the CPU hash for step 100 from section 0.3 (the GPU trains exactly the replayed stream).

**Choose `micro_tokens` (plan 2.4):** with C1 in place, the fastest value that passed step 2. Write it into
`runs/q35_4b_main.json` before the freeze. Then apply the plan's speed rule with the measured s/step:
- <= 3.34 s/step: full pass within $135;
- 3.34-4.33: full pass within $175, needs owner decision 4 (the 2B moves to the L4);
- > 4.33: uniform trim, `epochs = floor(36.6 h x 3600 / s_per_step) / 31359`.
- The critic's correction applies: the "for scale" costs use x1.21 (3.5 s/step = $142, not $129).

## 4. L4 memory at the chosen value (optional proxy, Modal L4)

```
MODAL_PROFILE=jaypatil-duke modal run modal_od.py::smoke_heavy --micro-tokens <chosen>,10240 --gpu L4
```

If step 3 kept 10240, run `--micro-tokens 10240 --gpu L4` instead: `10240,10240` would start two L4 containers
that write the same `logs/pilot/smoke_heavy_l4_mt10240.json`.

**Pass (plan 4.2):** same memory rule on the 24 GB card. If it fails, the 4B has no L4 tail. This is the same card
type as the Google L4 but not the same machine. The Google L4 check itself needs a `smoke_heavy` in `od_gcp.py`
(not in this runbook). With C1, the L4 tail may use a smaller `micro_tokens` than the H100 (it is not part of the run
identity under `aux_norm: "batch"`).

## 5. Relay proof test (plan 4.2; `logs/relay_protocol.md` test C)

Run it with the final config (step 3 decided `micro_tokens`) and the committed code. Names get a suffix, so nothing
touches `models/q35_4b_main500k`. `--log-every 1` only changes printing (it is not part of the run identity).

| Run | Account | Steps |
|---|---|---|
| A1 | jaypatil-duke | 0-300 straight |
| A2 | arya-mahadik-ai | 0-300 straight (fresh account: its own image build and model download) |
| B | aryamhd, then jaypatil-duke | 0-150, copy, 150-300 |

**5.1 Launch A1, A2 and B's first segment** (three terminals, at the same time):

```
mkdir -p logs/pilot
MODAL_PROFILE=jaypatil-duke modal run modal_od.py::relay --config runs/q35_4b_main.json --name-suffix _pA1 \
    --stop-at-step 300 --log-every 1 2>&1 | tee logs/pilot/relay_pA1.log
MODAL_PROFILE=arya-mahadik-ai modal run modal_od.py::relay --config runs/q35_4b_main.json --name-suffix _pA2 \
    --stop-at-step 300 --log-every 1 2>&1 | tee logs/pilot/relay_pA2.log
MODAL_PROFILE=aryamhd modal run modal_od.py::relay --config runs/q35_4b_main.json --name-suffix _pB \
    --stop-at-step 150 --log-every 1 2>&1 | tee logs/pilot/relay_pB_seg1.log
```

Wait until B's segment has exited by itself (the log shows `stopped_at_step 150`; `modal app list` shows nothing
running on aryamhd).

**5.2 Hand B over** (aryamhd -> jaypatil-duke). The local folder must exist before `volume get`.

```
mkdir -p handoff/pB_150 handoff/pB_150_back
MODAL_PROFILE=aryamhd modal volume get opendecide models/q35_4b_main500k_pB/_ckpt handoff/pB_150
../.venv/bin/python pilot/compare_relay.py --check handoff/pB_150/_ckpt --step 150 --expect-last-batch <CPU hash for 150>
MODAL_PROFILE=jaypatil-duke modal volume put opendecide handoff/pB_150/_ckpt models/q35_4b_main500k_pB/_ckpt
MODAL_PROFILE=jaypatil-duke modal volume get opendecide models/q35_4b_main500k_pB/_ckpt handoff/pB_150_back
../.venv/bin/python pilot/compare_relay.py --check handoff/pB_150_back/_ckpt --step 150
```

Both checks must print `OK`: every file matches its manifest (E2), the step is 150 and the batch hash is the CPU
replay's. The upload path must be empty on jaypatil-duke (it is, if `_pB` was never used there). Keep
`handoff/pB_150` until the verdict.

**5.3 B's second segment:**

```
MODAL_PROFILE=jaypatil-duke modal run modal_od.py::relay --config runs/q35_4b_main.json --name-suffix _pB \
    --expect-resume --stop-at-step 300 --log-every 1 2>&1 | tee logs/pilot/relay_pB_seg2.log
```

In the first lines, confirm `"resumed_at_step": 150` with `"checks": "...: all match"` (E1). If anything raises, do
not change flags to get past it: diff and investigate (relay protocol B.9).

**5.4 Download the three step-300 checkpoints and decide:**

```
mkdir -p handoff/pA1_300 handoff/pA2_300 handoff/pB_300
MODAL_PROFILE=jaypatil-duke modal volume get opendecide models/q35_4b_main500k_pA1/_ckpt handoff/pA1_300
MODAL_PROFILE=arya-mahadik-ai modal volume get opendecide models/q35_4b_main500k_pA2/_ckpt handoff/pA2_300
MODAL_PROFILE=jaypatil-duke modal volume get opendecide models/q35_4b_main500k_pB/_ckpt handoff/pB_300
../.venv/bin/python pilot/compare_relay.py --a1 handoff/pA1_300/_ckpt --a2 handoff/pA2_300/_ckpt \
    --b handoff/pB_300/_ckpt --expect-last-batch <CPU hash for 300> \
    --b-resume-log logs/pilot/relay_pB_seg2.log --resume-step 150 \
    --a1-run-log logs/pilot/relay_pA1.log --a2-run-log logs/pilot/relay_pA2.log
```

A1 and A2 must have run 0-300 straight. An H100 can be preempted; Modal then re-runs the input and the trainer
resumes silently, printing only a `resumed_at_step` line. That resume adds its own error to d(A1,A2) and g(A1,A2)
and loosens the 1.5x threshold, so the script fails if either tee log has such a line. Rerun that run straight
(new suffix), do not compare it.

**Pass (plan 4.2, copied):** "LR, counts and batch hashes identical. d(A1,B) <= 1.5 x d(A1,A2) for weights and for
the loss curve." What the script checks:
- exact (any difference fails): logged steps, `lr`, `of` and every `n_*` count at every logged step; `lr` against the
  cosine/warm-up formula; step, last-batch hash (and the CPU replay's), fingerprint and random states in `state.pt`;
  every file against its manifest; B's resumed line; no `resumed_at_step` line in A1's or A2's log;
- noise: d(X,Y) = ||θX - θY||2 / ||θA1||2 over all trainable tensors; g(X,Y) = mean |loss difference| over logged
  steps 150-299. PASS if d(A1,B) <= 1.5 d(A1,A2) and g(A1,B) <= 1.5 g(A1,A2). If A1 and A2 are bit-identical, B must
  be too.

**4B smoke criteria (plan 4.2, row 1), read from A1 and step 3:** loss falls (`a1_loss_trend`: the mean of the last 50
logged steps is below the first 50); no out-of-memory; memory <= 90%; trainable 32,464,896; kd_targets 43,363; all
startup checks pass; s/step recorded.

**5.5 Clean up** (after the verdict is in the ledger):

```
MODAL_PROFILE=jaypatil-duke modal volume rm -r opendecide models/q35_4b_main500k_pA1
MODAL_PROFILE=jaypatil-duke modal volume rm -r opendecide models/q35_4b_main500k_pB
MODAL_PROFILE=arya-mahadik-ai modal volume rm -r opendecide models/q35_4b_main500k_pA2
MODAL_PROFILE=aryamhd modal volume rm -r opendecide models/q35_4b_main500k_pB
```

## 6. Deferred

- **H100 -> L4 resume** (plan 4.2 row 4) needs C9 (`od_gcp.py relay`). Pass: "resumed_at_step ... all match"; only
  allowed env keys differ; LR and batch hashes match; loss within straight-vs-straight noise (not bit-exact).
- **2B smoke** (plan 4.2 row 6): `speed` and `smoke_heavy` take `--config runs/q35_2b_main.json` once that file and
  its heavy-batch ranking exist (`rank_microbatches.py --config runs/q35_2b_main.json --out pilot/heavy_batches_2b.json`,
  then `--heavy pilot/heavy_batches_2b.json`).

## 7. After the pilots

Write into `logs/budget_ledger.md`: the memory table per value (H100, L4), s/step per value, the chosen
`micro_tokens`, the relay verdict with d and g, and the money spent per account. Then set `micro_tokens` in
`runs/q35_4b_main.json`, freeze (plan 2.3), and **stop**: the real run waits for the owner.
