# Round-1 speed analysis: P1 pre-smoke 6.075 s/step vs C1-era 2.77 (6 Oct 2026, CPU only)

Scripts and per-step data: `c_build/endgame/logs/r1_speed_src/` (counts and lengths only; real Qwen3.5-4B tokenizer
rev 851bf6e, cygnet, schema_branch_mark, `decoder_io.render_chat`). No GPU/Modal; no trainer, mixer or config edits.

## 1. What one step costs (from the code)
- **Step:** `batches()` gives >= 16 rows of whole call_id units (1-3 rows). `perm_twin` 0.3 adds a second view of
  about 30% of choice rows. `_micro_groups` packs units, longest first, under `micro_tokens` 8192, where cost =
  (rows + twins) x the micro-batch's padded max length (`PAD_MULTIPLE` 256, from env `OD_PAD_MULTIPLE`). Each
  micro-batch then runs **one** forward (rows and twins together) and one backward, with grad_ckpt recompute.
- **No extra forwards:** cons, inv, equiv, perm and ordinal terms and KD all reuse that forward's logits (KD uses stored
  teacher probabilities). The only extra pass is the base-model anchor forward when `beta` > 0. C has beta 0. C1's
  pilot had beta 1, but anchor rows are 0.6% of its file, about 0.1 rows per step.
- **log_every=1 costs ~0** (`float(v.detach())` syncs every micro-batch at any log_every; the per-token rate below is
  equal at 1 and 50). The checkpoint is outside s_per_step (ckpt_s 5.5 s, last step).

## 2. Why 6.075 vs 2.77: about 2.2x more padded tokens per step
- **Replay of P1's batches** (seed 20261006, trainer's own `make_units`/`batches`/`pick_twins`/`_micro_groups`):
  batch 0 matches the logged hash; later ones are near-identical, not bit-exact (n_ord 38/40, n_cons+n_inv 33/40,
  last hash differs). C1's 30 Sep pilot ran older code, so it was re-drawn statistically (1,800 steps, golden_train).

| per step (timed steps) | P1 pre-smoke | C1-era pilot | ratio |
|---|---|---|---|
| rows / twins / micro-batches | 16.4 / 2.3 / 4.9 | 16.5 / 1.8 / 3.3 | |
| real tokens / padded tokens | 30,149 / 37,572 | 11,669 / 16,939 | 2.58 / **2.22** |
| mean tokens per row (all rows in file) | 1,556 | 620 | 2.5 |
| measured s/step | 6.075 (SE 0.27) | 2.767 (SE 0.10) | **2.20** |

- **Rate is ~constant, ~0.162 ms per padded token:** P1 0.1617, C1 0.1633 (C1 replay draw 0.1598), C1 at
  micro_tokens 10240 0.1649. As a check, C1 at 10240 has 4.3% more padded tokens than at 8192 and measured 5.3%
  slower on the same batches, so per-micro-batch overhead is about 0.
- **Per-step OLS on P1** (34 steps, approximate replay): t = 0.143 ms x padded + 0.71 s, R2 0.72; it predicts C1 at
  3.19 (15% high), so the zero-intercept rate is used and this model is kept as a sensitivity.
- **Root cause:** new rows are long, and the pre-smoke sample is only 30% replay (60% in the real mix).

| block (P1 sample, real tokenizer) | rows | tok mean / median | choice | relations / row | rows / unit |
|---|---|---|---|---|---|
| replay | 539 | 634 / 535 | 0.32 | 0.22 | 1.28 |
| F1 / F2 / F3 / F4 | 75/70/76/90 | 1815 / 1152 / 1656 / 1462 | .45/.66/.49/.31 | .20/.14/.21/.34 | 1.25/1.17/1.27/1.53 |
| F5 / F6 / F7 / F8 | 158/71/80/64 | 1274 / 1621 / 1361 / 1262 | 0/.61/1.0/.58 | .63/.15/.25/.06 | 2.68/1.18/1.33/1.07 |
| F9 / F10 / F11 / F12 | 71/73/77/70 | 1991 / 1857 / 2200 / 3149 | .49/.48/.45/.53 | .15/.18/.23/.14 | 1.18/1.22/1.31/1.17 |
| F13 | 79 | **6,535** / 6,638 | 0.47 | 0.24 | 1.32 |
| public / COMMIT | 120 / 67 | 1421 / 1388 | .54 / .60 | 0 / .10 | 1.0 / 1.08 |

- F13 is 4.4% of P1's rows but about 19% of its tokens; replay is 30% of rows and 12% of tokens.

## 3. Projection for the real mix (150,000 rows)
- **Simulation:** units drawn at 1/8 scale (18,749 rows) from replay `data/c_replay_r1_shards` (90,000), each
  `c_src/F*/out/candidates_r1.jsonl` at its final quota (F1 5400, F2 3150, F3 4500, F4 3600, F5 3600, F6 3600,
  F7 3150, F8 2250, F9 4050, F10 3600, F11 3600, F12 2700, F13 2225), public-1/2/3 rows (8,575) and COMMIT (6,000).
  The trainer's batching and packing then ran over 3 seeds x 600 steps.
- **Check:** on P1's rows the simulator gives 37,370 padded tokens/step (replay 37,572). **Pools:** tokens per row are replay 618, F1 1819, F2 1132, F3 1599, F4 1579, F5 1270, F6 1546, F7 1330, F8 1224,
  F9 1903, F10 1895, F11 2375, F12 3136, F13 6389, public 1130, COMMIT 1384. The mix mean is **1,085 tokens per row**,
  1.75x C1's. Token shares: replay 34%, families 55% (F13 alone 8.7%), public 6%, COMMIT 5%.
- **Per step:** 16.2 rows, 2.0 twins, 4.1 micro-batches, **27,990 padded** (20,280 real) tokens, which is 1.65x C1.
- **s/step: central 4.53 (range 4.2-4.9).** The range covers the rate's spread (+-4.5%) and composition/sampling
  (+-3%). The intercept model gives 4.72. The recipe's +12% case (3.08) is far below this.

## 4. Steps, hours, $ (at $4.09/h + $2)
- **Steps:** 150,000 / 16.18 rows/step (mixer dry run; simulation 16.2) = **~9,270**; recipe's 8,880 assumed 16.9.

| s/step | 8,880 steps | 9,270 steps |
|---|---|---|
| 4.2 (low) | 10.4 h, $44.4 | 10.8 h, $46.2 |
| **4.53 (central)** | 11.2 h, $47.7 | **11.7 h, $49.8** |
| 4.9 (high) | 12.1 h, $51.4 | 12.6 h, $53.6 |

- **To fit $35:** at most 3.13 s/step at 9,270 steps (3.27 at 8,880). At 4.53, $35 buys about 6,400 steps, about
  104K rows (information only, not a rule).
- **Which stop rule trips:**
  - **D1 preflight passes:** it uses the fixed 2.754 x 1.12 (9,270 steps = $34.5; refused above 9,416).
  - **D3 (A21 c) passes.** s/step over steps 10-99 is about 4.5, below 5.508 (about 6 SE margin). The P1 sample itself,
    at 6.075, would have tripped this rule.
  - **D4 / recipe 4 trips: STOP and ask the owner.** The projected total is about $45-54, above $35. The cap check
    also fails: the segment-3 cap is about (35-2-2)/4.09 = 455 min, against a remaining run of about 11.3 h.
  - **Cost before the stop:** about 300 steps x 4.5 s plus 2 loads, about **$1.8** on aryamhd's card. An 11.7 h run
    would also exceed the 10 h function timeout in one segment (it would need two relay segments).

## 5. Math-neutral speed-ups (same rows, order, batch, losses, lr schedule, steps)
Each estimate assumes time is proportional to padded tokens, which held for both measured data sets.

| lever | padded tok / step | s/step | $ (9,270) | math | needs |
|---|---|---|---|---|---|
| baseline mt 8192, pad 256 | 27,990 | 4.53 | 49.8 | - | - |
| `OD_PAD_MULTIPLE` 64 | 26,538 (-5.2%) | 4.30 | 47.3 | (a) | env var on the Modal fn + amendment + pilot |
| micro_tokens 6144 | 26,516 (-5.3%) | 4.30 | 47.2 | (a) | amendment + pilot |
| micro_tokens 4096 (+pad 64) | 24,767 (23,153) | 4.01 (3.75) | 44.3 (41.5) | (a) | amendment + pilot; small forwards may lose GPU efficiency (untested < 8192) |
| varlen packing (no pads) | 20,283 floor (-27.5%) | ~3.3 | ~36.6 | (b) | trainer code change (pinned) + amendment + parity test |
| ckpt_every_min 10 -> 30 | - | -0.6% | -0.3 | bit-identical (RUN_KEY) | relay-safe; more loss on preemption |
| log_every 50 (already config) | - | ~0 | ~0 | bit-identical | - |
| **larger** micro_tokens (12288 / 16384 / 24576) | +10% / +18% / +31% | 4.99 / 5.36 / - | slower | (a) | **reject**: C1 pilot at 10240 was +5.3% slower |
| grad_ckpt off | - | - | - | same | **unavailable**: OOM even at 8192 on C1 data (30 Sep) |

- **(a)** Same objective (aux_norm "batch"; `_identity` drops micro_tokens). Pads are right-side and masked, and the
  loss is read at the last real token, so the result is mathematically equal. It is **not bit-identical**: micro-batch
  shapes change the float summation order and the **LoRA-dropout mask realization** (masks depend on tensor shape and
  SM grid, as `_env` notes). This is the same in distribution, but it is a different draw.
- **(b)** Same objective; the attention and GDN kernels change float order.
- **Result:** no lever or stack reliably reaches 3.13 s/step; the best without code changes (4096 + pad 64) is about
  $41.5, unmeasured. DDP is not a lever (A20 (c) failed parity; owner chose 1xH100 at 01:45 UTC).

## 6. Rule-based options if the projection is still above $35 (from the text; nothing new)
1. **Recipe 4 / RUNBOOK D4:** "If round 1's projection passes $35, stop and ask the owner" (chain ends at step 300,
   `r1_check.py proj` exits 1, checkpoint kept). The only written round-1 action; A22 (2) automates it, A23 restates
   it. "No more questions" (owner, 05:30 UTC) does not cover it: the written rule itself says ask.
2. **Owner raises the round-1 limit** within the budget rule (all C Modal <= $100, $25 reserve; if both cannot hold,
   stop and ask). At about $50 for round 1, the round-2 trim rule then bites hard.
3. **Trim rule (recipe 4) is round 2 only** ("trimmed (keeping the 60/40 split and every family's share) so that its
   projection ... fits the remaining cap"); trimming round 1 that way needs an owner decision or amendment.
4. **Not cost levers:** the A16/A22 token cap is already met (long-row token share 15.4% <= 30%); A21 (c) aborts
   only above 5.508, and a re-run after an ABORT needs a cause + amendment.

## 7. The one cheap measurement that settles the number
- **The decision does not need it** (even the low end, $44, trips D4). **For an exact figure for the owner:** run one P1-style `modal_od.py::speed` (log_every 50, `--steps 60 --skip 10`)
  on a sample drawn with the **real block shares**. That means about 60% replay, families at their quotas, 5.7%
  public, 4% COMMIT; P1's sampler fixes replay at about 30%. The speed function takes a micro_tokens list (one
  container each, same batches), so one launch can also measure the two untested levers: `8192,6144,4096`.
  - **Cost:** about $0.5 per container (60 x 4.5 s + load), **$1.5** for 3; a paid GPU step (GO point). Tight:
    jaypatil-duke has $13.07 with about $12 reserved for final tests. **No-extra-cost alternative:** segments 1-2 of
    the real run (about $1.8) measure the real mix anyway, then stop at D4.

## Verification (independent re-derivation, 6 Oct; CPU only, counts only; scripts in `r1_speed_src/verify/`)
**Verdict: the cause, s/step, cost and speed-up claims hold (central within 3%). Sections 4/6 miss an earlier stop.**

**1. Cause: confirmed.** The code does one `cand_logits` forward and one backward per micro-batch. Twins share that
forward, every term and KD reuse its logits, the anchor runs only when beta > 0, and the stop checkpoint is untimed.
- My P1 replay: batch-0 hash matches. Steps 5-38 give 16.41 rows, 2.32 twins, 4.94 micro-batches and 37,572 padded
  (30,149 real) tokens, as in section 2. Logged twins are 2.21; n_ord/n_cons/n_inv match on 38/36/37 of 40 steps.
- Rate: P1 0.1617 ms/padded token. My C1 redraw (3 seeds x 340 steps) gives 16,737 padded/step, so 0.1653 ms (0.1672
  at 10240: +4.1% tokens, +5.3% time). Padded ratio 2.24 against a time ratio of 2.20.
- New padded lengths (Triton tuning) cost ~0 s/step in P1 (OLS -0.08 s). A per-micro-batch cost model predicts C1 16%
  high and gets the 10240 direction wrong, so time ∝ padded tokens stands.

**2. Real-mix s/step: confirmed (+2%).** I tokenized all 186K pool rows (replay, 13 `candidates_r1`, public-1/2/3,
COMMIT), drew whole relation units to the quotas, then ran 3 seeds x 3,000 steps through the trainer's packing.
- The mix is 1,089 tok/row. Per step: 16.19 rows, 2.03 twins, 4.11 micro-batches, **28,347 padded** (+1.3%).
- s/step is 4.58 (P1 rate) to 4.69 (C1 rate), **central 4.63**, and the intercept model gives 4.77. Range 4.4-4.9.
  The analysis's 4.53 is 2.2% lower.
- Steps: `ceil(150,000/16 x round(16/16.19, 4))` = ~9,266-9,270. At 9,270: **11.9 h, $50.8** (range $48-54).

**3. Stop rules: corrections.**
- **The at-quota mix fails the A22 token cap, so `mixer.py --final` refuses** (RUNBOOK C; no training file, $0 GPU).
  - Rows >= 2,000 tokens are **17.1% of new rows (limit 9%)** and **37.9% of new-row tokens (limit 30%)**. The mixer
    counts exactly 16 fewer tokens per row; under 1% of rows sit in that band.
  - Long-row share: F13 100%, F12 69%, F11 55%, F10 37%, F9 25%, F1 12%, public 9%.
  - Section 6 (4)'s "cap already met (15.4%)" comes from `dryrun_r1.json`, which had no F3, F4, F9-F13 or COMMIT
    rows, so it is stale.
  - The cap's auto-drop (F13/3B rows) refills from the same family, and nothing fixes the 9% row rule. Round 1 needs
    an owner decision or amendment before D1.
- **D1 uses `config_fill.dry_run_steps` = ceil(150,000/16) = 9,375, not 9,270**: $34.85 (passes by only $0.15).
- If the mix is admitted as it is: D3 passes (~4.6 against 5.508). **D4 trips** (~$51 projected). The seg-3 cap check
  also fails (~456 min against ~700). About $1.9 is spent before the stop.
- Trimmed to the cap (long rows cut to 9%, refilled with short units, F13 at 1,148 rows): 26,431 padded/step,
  ~4.32 s/step, ~$47.5. D4 still trips.

**4. Speed-ups: the claims hold.**
- Packing leaves the update unchanged:
  - Batch, perms and twins are drawn before `_micro_groups`, which uses no RNG. Rows per step, order, Python RNG
    streams and the resume replay are the same.
  - aux_norm "batch" divides task, cons, inv, perm and ord by whole-batch counts, and twin views stay with their row.
  - Units never split, and G15 keeps each relation inside one call_id: 0 split relations in 9,000 simulated steps.
  - `_identity` drops micro_tokens. Pads are on the right and the readout is at `mask.sum-1`.
  - The result is equal in math but not bit-identical: LoRA-dropout masks (Philox offsets follow shape) and float order.
- Padded per step against 8192/256: pad 64 -5.2%; 6144 -5.2%; 4096 -11.5%; 4096 + pad 64 -17.1% (3.84 s,
  ~$42.5); 10240 +5.1%; 12288 +9.5%. These match section 5.
- Caveats:
  - `OD_PAD_MULTIPLE` is not in `_env()`; setting it needs a launcher change (pinned); pad 64 = 4x Triton buckets.
  - 4096 gives 6.6 micro-batches per step, and nothing below 8192 has been measured.
- Best stack without trainer changes (cap-compliant mix + 4096 + pad 64): ~3.56 s, ~$39.5. That is above the 3.13 s
  needed for $35, so it is agreed that no lever reaches $35.
- Side note: the COMMIT pool has 327 non-inv relation pairs across call_ids, which G15 refuses unless they are fixed.
