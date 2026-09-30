# FINETUNE_PLAN.md: final 4B run and 2B distillation

*Written 30 Sep 2026. This is a plan only: nothing in it has been run yet. IDs in square brackets, such as [M1], point to the research items checked on 30 Sep. They are not ledger row IDs; the ledger also has rows called M1-M5, which are different things. Numbers come from our own logs unless a URL is given. "Not sure" means we have no evidence either way.*

**Standing rule.** Nothing in sections 2-4 starts until the owner says the GPU and budget are ready. Until then, only the CPU work runs. All training and evaluation happen on Modal or the Google L4, never on the laptop.

---

## 1. Summary

**What we do.** We make one training pass of Qwen3.5-4B, starting from the base model, over the frozen 501,732-row golden set. We use layout E (no PRISM-X on the 4B), LoRA r16/alpha32, lr 7e-5, cosine schedule, label smoothing 0.05, and kd 0.5 on the 43,363 human or exact soft-label rows only. The run is exactly one pass: 30,457 steps.

**Before step 0.** A small set of safety code changes must land and pass their CPU tests first. Then the code is frozen.

**In parallel.** Our current best 4B, 4B-E, labels about 424.7K golden rows on the L4. These rows were not in its training data, so the labels are honest.

**The 2B.** One pass of Qwen3.5-2B, also from base, distilled from those labels (kd 0.5). PRISM-X arm I is added only if the pending matched test (I_1600 vs E_L4_1600) passes.

**Shipping rule.** A new model ships only if it passes a rule written down before the run. The rule is a non-inferiority test on the two dev halves:
- the new 4B against 4B-E: 81.49 on dev-confirm, 79.84 on dev-select;
- the new 2B against v11r: 76.24 confirm, 75.62 select.

If a new model fails, the current model ships.

**Expectations, honestly:**
- The code changes protect the run. They should move accuracy by about 0 pp.
- We cannot predict the gain from the 500K data. The last time we added broad data, general dev accuracy rose only +0.6 pp.
- The yes/no gap to Jev (88.6 vs 96.1 on OHS-2) may stay open.
- The plan is built so that "no gain" costs us nothing except money: 4B-E and v11r stay in service.

### Decisions the owner must confirm before step 0

1. **Budget.** This plan assumes $300 of Modal credit, as in the frozen roadmap. The 30 Sep resources note said $118. Section 6 gives the $118 version.
2. **Up-weighting the weak yes/no families** (roadmap item 2 said 1.5-2x for moral norms, tables and science claims).
   - We recommend **1.0x (no up-weighting)**. In-family gains did not transfer to general dev before (ledger A18, G2).
   - 1.5x on these 108,298 rows would add about 54K repeated rows: about +10.8% compute, or $12-15.
   - If the owner keeps 1.5x, it needs a new derived training file and a new step-count replay before step 0.
3. **Teacher for the 2B.** The default is 4B-E. Switch to the new 4B only under the rule in section 3.7. This follows the memory checklist; roadmap item 6 also allows the switch.
4. **If a full 4B pass costs more than $135.** Our recommendation is to move the 2B to the L4 first (4.6-4.8 days) and give the 4B up to $175. Only if it still does not fit, trim the 4B's rows uniformly (section 2.4).

---

## 2. Final 4B run

### 2.1 Config: replaces `runs/q35_4b_main.json`

```json
{
  "name": "q35_4b_main500k",
  "base": "Qwen/Qwen3.5-4B",
  "base_revision": "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a",
  "recipe": "A3",
  "train_file": "v14_parts/golden_train.jsonl",
  "rel_file": "v14_parts/golden_relations.jsonl",
  "epochs": 0.9712363276890207,
  "lr": 7e-05,
  "batch": 16,
  "r": 16,
  "alpha": 32,
  "dropout": 0.05,
  "lam": 1.0,
  "beta": 1.0,
  "kd": 0.5,
  "kd_skip_src": ["blend50"],
  "kd_full_src": ["gd_gen2_probability"],
  "label_smooth": 0.05,
  "lam_inv": 1.0,
  "sym_cons": true,
  "perm_twin": 0.3,
  "lam_p": 0.5,
  "aux_norm": "batch",
  "seed": 20260925,
  "grad_ckpt": true,
  "style": "cygnet",
  "layout": "schema_branch_mark",
  "micro_tokens": 10240,
  "targets": "QWEN35",
  "snap_every": 2500,
  "snap_fracs": [0.85, 0.90, 0.95],
  "expect_trainable": 32464896,
  "expect_kd_targets": 43363,
  "ckpt_every_min": 10,
  "log_every": 50
}
```

**What these numbers mean:**
- 30,457 steps = exactly one real pass (checked: ceil(501,732/16 × 0.97123633) = 30,457).
- Warm-up is 1,522 steps. The consistency ramp runs to step 6,091.
- Snapshots are saved every 2,500 steps and at steps 25,888, 27,411 and 28,934.

**Keys that do nothing until their code exists:** `aux_norm`, `kd_full_src`, `snap_every`, `snap_fracs`, `expect_trainable` and `expect_kd_targets` (section 2.3). Today the trainer silently ignores keys it does not know. Code change C2 adds a check that refuses unknown keys, so a key without its code fails loudly instead of doing nothing.

**`micro_tokens` 10240 is a placeholder** until the smoke run (section 2.4).

### 2.2 What changed from the draft, and why

| Key | Draft | Final | Evidence | Expected effect |
|---|---|---|---|---|
| `r` / `alpha` [S1] | 32 / 64 | **16 / 32** | Doubling alpha at a fixed rank acts like doubling B's learning rate: https://thinkingmachines.ai/blog/lora/. Rank barely matters for classification (MNLI r=1..64 within about 0.5 pp): https://arxiv.org/pdf/2106.09685 | About 0 pp. Removes an untested 2x effective LR. Every from-base 4B run (v07, v11) used r16/a32. |
| `epochs` [S2] | 1.0 | **0.97124** | CPU replay of `batches()` with seed 20260925: the first pass is 30,457 batches (units average 16.47 rows). | About 0 pp. Removes 902 repeat steps at under 0.23% of peak LR, about 2.9% of compute ($3-5). |
| `micro_tokens` [M7] | 12288 | **10240, then measured** | The 4B has only been proven on the L4 at 10240 (ledger G2). Worst real micro-batch: 23,296 tokens at 10240, 27,648 at 12288, 36,864 at 16384 (CPU tokenizer replay). | 0 pp once C1 lands. Prevents an out-of-memory crash that would repeat at the same step on every resume. |
| `aux_norm` [M1] | none | **"batch"** | The correct accumulated loss is the total over all items divided by the total count: https://huggingface.co/blog/gradient_accumulation | Accuracy: not sure (a guess of ±0.3 pp). Certain: the same objective on every GPU and every micro_tokens value. Long rows no longer get about half the consistency weight. Aux terms run at their nominal weight (1.0x, like v11) instead of about 0.65x. |
| `kd_full_src` [O3] | none | **["gd_gen2_probability"]** | The log score is strictly proper, so training should target the true probability: https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf | Tiny. 238 rows (0.05%) are trained on their exact probability instead of being pulled toward 0/1. Optional. |
| `snap_*` [S3] | none | **2500 plus 0.85 / 0.90 / 0.95** | With cosine decay to zero, weight averaging converges to the annealed model: https://arxiv.org/html/2502.06761 | About 0 pp. Insurance: a usable model if the run dies, plus one pre-registered averaged candidate. |
| `expect_*` [M7] | none | **32,464,896 / 43,363** | PEFT casts adapters to fp32 by default: https://huggingface.co/docs/peft/package_reference/peft_model. The count is from logs/train_q35_4b_v11.log:55. | 0 pp. Stops a wrongly configured launch before step 1. |

**Unchanged on purpose:**
- lr 7e-5 (from base, proven in q35_4b_v11);
- label smoothing 0.05 (I_LS0 with 0 lost 1.29 pp);
- kd 0.5 on human soft labels only;
- lam 1, lam_inv 1, lam_p 0.5, perm_twin 0.3, beta 1;
- wd 0, dropout 0.05, clip 1.0, batch 16, cosine with 5% warm-up.

### 2.3 Code changes

All of these land and pass CPU tests **before step 0**, then get frozen together in one git tag. The trainer refuses to resume if the code hash changes. It hashes four files: `train_decoder`, `decoder_io`, `prism_x` and `writeblock`. So every change to `decoder_io` in this list, including the ones the teacher labelling needs, must land before the freeze.

| # | File | Change | Evidence | Expected effect | Priority |
|---|---|---|---|---|---|
| C1 [M1] | train_decoder.py | Adds `aux_norm` "batch" ("micro" = today's path, byte-identical):<br>1. Move relation enumeration into a helper that uses row metadata only. Use it to count cons/inv/perm/anchor terms over the whole 16-row batch.<br>2. Divide each term's sum by its batch count, and the task term by len(batch).<br>3. Call backward without the `w` factor.<br>4. With "batch", exclude `micro_tokens` from the identity check (in `_fingerprint`, `ckpt_extra` and the resume diff).<br>5. Log the effective weights.<br>6. Before step 0, a CPU pre-pass over all 30,457 batches checks that the per-micro counts equal the batch counts. During the run, only a warning, never a hard assert.<br>**Test:** fake_env with micro_tokens 512 (assert more than 1 group). After 3 steps, params under "batch" equal micro 0 (atol 1e-5) and DIFFER under "micro". | https://huggingface.co/blog/gradient_accumulation. The bug is at train_decoder.py:771-772. | Same objective everywhere; accuracy not sure | should (fallback in section 2.5) |
| C2 [M7] | train_decoder.py | Startup checks:<br>- trainable params == `expect_trainable`;<br>- all trainable params are float32 (after line 619, so PRISM-X is covered too);<br>- `decoder_io.STYLE == c["style"]`;<br>- kd target count == `expect_kd_targets`;<br>- rows matched by `kd_full_src` printed and == 238.<br>Also an **unknown-key check**: refuse any config key not read by train_decoder, modal_od or od_gcp (list made with grep and reviewed by hand). | https://huggingface.co/docs/peft/package_reference/peft_model; bf16 rounding cancels small updates: https://arxiv.org/abs/2010.06192 | 0 pp. Stops silent misconfiguration. | must |
| C3 [S4] | train_decoder.py | 1. `gn = float(clip_grad_norm_(...))`, and raise **before** `opt.step()` if gn is not finite. One NaN gradient otherwise turns every weight into NaN and can poison `_ckpt`.<br>2. Log `gn`, a 200-step median, `clip_frac`, and `gn_px` for the 2B.<br>3. ALERT lines, logged only, never acted on automatically: gn > 5x the median for 20 or more steps; 200-step mean task loss > 1.2x its running minimum after warm-up.<br>4. Save the monitor state in the checkpoint, so tests/test_resume.py stays bit-identical.<br>5. Copy `_ckpt` to `_ckpt_good` about every 2,000 steps if no alert fired in the last 400 steps. Freeze it after any alert.<br>No `skip_steps` now; add it only if a spike ever happens. | Loss spikes and rollback: https://arxiv.org/abs/2204.02311 (pretraining, 540B; weak evidence for our case) | About 0 pp; visibility and a clean rollback point | should (the NaN guard is must) |
| C4 [S3] | train_decoder.py | Snapshots at `snap_every` / `snap_fracs`.<br>- Write to `.tmp`, then rename. Save adapter, `prism_x`, tokenizer and `snap.json`.<br>- Wrap in try/except: a failed save logs a line and never stops training.<br>- `snap_*` go in RUN_KEYS.<br>**Tests:** snapshots fire at the exact steps; weights are `torch.equal` with snapshots on and off; resume across a snapshot step works. | https://arxiv.org/html/2502.06761; `cat` merging is exact: https://huggingface.co/docs/peft/en/package_reference/lora | Insurance | should |
| C5 [O3] | train_decoder.py | `kd_full_src`: for yes/no rows from listed sources that have a teacher, `y = teacher["yes"]` exactly (before any sharpening). All other rows are unchanged.<br>**Unit test:** a listed row gets y == p; an unlisted row still gets `(1-kd)*(g(1-2eps)+eps) + kd*p`. | https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf | Tiny | optional: drop the key if it is not tested by the freeze |
| C6 [M2] | decoder_io.py (+ od_gcp, modal_od) | Take the layout from the adapter's `train_meta.json` in one place (`decoder_io.load`), after `pxm.uninstall()` and before `maybe_load()`.<br>- Missing file → raise, unless a layout is passed explicitly.<br>- A conflicting flag → raise, unless forced; forced overrides are written into the meta.<br>- Blend and soup: resolve per adapter and raise if they disagree.<br>- Write `layout` and `style` into every preds meta.<br>- Also fix `jevbench_od.py` `fmt="cygnet"`: its own `_prompt` is hard-coded text-first. Add a CPU parity test so text-first prompts stay byte-identical. | Prompt-format changes alone can move accuracy by many points: https://arxiv.org/abs/2310.11324 | Correct teacher labels, gate scores and JevBench scores | must (before any labelling) |
| C7 [S5] | decoder_io.py | `predict(..., perms=...)` gets per-row permutations. Pass the SAME perm to `cand_logits` AND `to_probs`.<br>- Seed with sha256(f"{S}:{id}"), never Python `hash()` (it changes per process).<br>**Test:** an identity perm gives exactly the perms=None output; random perms agree on the argmax for ≥90% of rows (a mapping bug shows about 1/n). | https://arxiv.org/html/2403.13590v1 | Removes the constant "Yes is always A" read in teacher labels | must (for labelling) |
| C8 [S8] | decoder_io.py, od_gcp.py | Separate `tta_choice` and `tta_noul` flags, so each question type can be adopted on its own. | https://arxiv.org/abs/2309.03882 | Enables the per-type TTA gate (section 5.2) | should |
| C9 [M8] | od_gcp.py | `od_gcp.py relay --config runs/<x>.json [--stop-at-step N]`:<br>- load the JSON and check RELAY_REQUIRED;<br>- expand QWEN35 and set STYLE;<br>- `no_overwrite=True`, `expect_resume=True` (a missing checkpoint must fail, not restart at step 0 on a GPU about 7x slower), `allow_env_change=True`;<br>- first refuse if the checkpoint's env differs in anything other than gpu, sm_count, python, cudnn or torch_cuda. | Modal adds local files at container start: https://modal.com/docs/guide/images | Makes the L4 tail fallback safe | should |
| C10 [M3] | od_gcp.py + new scripts | Fix `save()` to use `pd.mkdir(parents=True, exist_ok=True)`.<br>Sharded, resumable labelling: write `.tmp`, then `os.replace`, meta last. A shard counts as done only if meta exists AND the line count and ids match. | Local: od_gcp.py:30 | Stops a multi-day label job from being lost | must (for labelling) |

**Not hashed, but written before use:**
- `gate_dev.py --mode ship` (section 4.5);
- `calibrate.py` fitting on dev-select only (section 5.1);
- `cascade_sim.py` additions (section 5.3);
- `shard_golden.py`, `build_2b_kd.py`, `flag_labels.py`;
- the CPU replay script that sets `epochs`;
- the CPU tokenizer script that ranks the heaviest real micro-batches.

**Freeze procedure [M8]:**
1. Commit and tag `final-frozen`: train_decoder.py, decoder_io.py, prism_x.py, writeblock.py, modal_od.py, od_gcp.py and runs/q35_4b_main.json.
2. Launch every 4B segment from a frozen copy. Either use a worktree at the tag with symlinks to the untracked `data/` and `bench/jevbench`, or run the 4B from the main checkout and do all later coding in a worktree.
3. Pre-launch guard: `git diff --quiet final-frozen -- <the 4 hashed files> runs/q35_4b_main.json`.
4. Run `chmod 444` on golden_train.jsonl and golden_relations.jsonl. Write all 2B data to NEW files.
5. Never set `allow_code_change`.

### 2.4 Values fixed in the smoke run, then written into the JSON before step 0

- **`micro_tokens`.** Candidates are 10240 and 12288.
  - A candidate is allowed only if the 3 heaviest real micro-batches, the heaviest single unit, the heaviest group containing an anchor row, and one dense WTQ group all run a full step on **both** the H100 and the L4. Run them after 20 ordinary steps, and require `max_memory_reserved` ≤ 90% of the card.
  - With C1 in place, pick the faster allowed value.
  - If the L4 fits neither value, accept that the 4B tail cannot move to the L4.
  - Also test `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` (https://docs.pytorch.org/docs/2.14/notes/cuda.html).
- **causal-conv1d.** Adopt only if it is at least 10% faster AND the 50-step loss curve stays within straight-vs-straight noise. If adopted, pin it in image35 and install it on the L4 before step 0. The speed figure comes from the 30 Sep plan note; I did not re-check it.
- **Speed → `epochs`.** Measure seconds per step (s/step) over at least 100 packed steps of real data. Define:
  - cost of a full pass = 30,457 × s/step × $3.95/h × 1.10 (CPU and memory overhead, per the ledger) × 1.10 (margin for handovers, restarts and evals).
  - s/step ≤ **3.34** → full pass within $135.
  - 3.34 < s/step ≤ **4.33** → full pass within $175. Needs owner decision 4: the 2B moves to the L4.
  - s/step > 4.33 → uniform trim: `epochs = floor(36.6 h × 3600 / s_per_step) / 31359`. The seeded shuffle then trains on a random subset of whole units, and the cosine schedule still finishes.
  - Never cap the gd_gen_* generators first [S2]: they are protected priority data, and 3 of them are 71-78% yes/no.
  - For scale: 3.0 s/step ≈ 25.4 h ≈ $110; 3.5 ≈ 29.6 h ≈ $129; 4.0 ≈ 33.8 h ≈ $147; 4.6 ≈ 38.9 h ≈ $169. Speed with packing on the golden set is **not measured yet**; the 30 Sep estimate is 26-32 h.

### 2.5 Fallbacks if a code change is not ready by the freeze

- **C1 not ready:** remove `aux_norm`. Fix `micro_tokens` at **10240**. This gives about 0.61x consistency and invariance weight and about 0.55x anchor weight, close to 4B-E's regime. **Never pick it by speed.** Record the effective weights in the run card. Correct the plan's claim that micro-batching is "the same maths": that is true only for the task term.
- **C4 / C5 not ready:** remove `snap_*` / `kd_full_src`.
- **C2 not ready:** do not launch. It is small, and it is the guard against every other silent error.

---

## 3. Final 2B distillation recipe

### 3.1 Preconditions
1. The matched test I_1600 vs E_L4_1600 has finished, with its pre-registered gate: +1.3 pp on dev-confirm with a lower bound above 0.
   - Pass → `"prism_x": "I"`.
   - Fail → drop the key and use layout E alone.
2. C6, C7 and C10 have landed and passed their tests. C6 matters most: without it, the teacher labels could be read in the wrong layout with no error.

### 3.2 Teacher-label generation (L4, starts at the same time as the 4B run)

1. **Smoke on the L4** (1-2 h):
   - Run 4B-E with `--base Qwen/Qwen3.5-4B --layout schema_branch_mark`. Pass these explicitly: 4B-E's meta wrongly records base "Qwen3.5-2B".
   - Score the dev splits in the default view (identity perms).
   - **Pass if**, against the stored `preds_dev/q35_4b_pxE`: argmax agreement ≥ 99%, mean |dp| ≤ 0.005, max |dp| ≤ 0.05, and accuracy within 0.3 pp. The limit cannot be 1e-3, because merging in bf16 alone moves probabilities by up to 0.018 (ledger X3).
   - Record rows/s.
2. **View test** on 5K golden rows (30-60 min), with 2 reads each. Report:
   - the argmax flip rate;
   - the mean signed dP(yes) between Yes=A and Yes=B;
   - mean |dp|;
   - accuracy and NLL in the default view vs a random view, per question type.
3. **View policy [S5]:**
   - **Default: 1 view per row.** Seeded random Yes/No letter order on yes/no rows; seeded random option order on choice rows. Keep the default order on choice rows only if the random view loses at least 0.3 pp there.
   - **2 views, averaged in probability space**, only if all hold: (TTA on 4B-E gives at least +0.3 pp, OR flips are at least 3%, OR mean |dp| is at least 0.05) AND the 2B trains on the H100, so the L4 has time.
   - Never build per-draw labels matched to one view. The trainer redraws permutations every step and looks up targets by option text.
4. **Rows to label.**
   - All golden rows except:
     - attacked twins;
     - `teacher_src=blend50` rows;
     - rows whose sha1(state + instructions + options) appears in 4B-E's training files (train_v11/v11b/v11c/v13t/train_prism_arms);
     - the 192 `gold_probs` rows;
     - 3 csqa rows with duplicate options (r_84331130428f, r_33cba1e12b8e, r_8e993e070c07).
   - Measured: 79,688 rows excluded (15.9%), **424,693 to label** (67% yes/no, mean 1,799 characters).
   - Shards of about 20-25K rows, with the crash-safe resume from C10. Assert the layout before each shard.
5. **Time.** The L4 labelled 4.84 rows/s on teacher_pool, and golden rows are 1.36x longer. That gives **about 33 L4-hours per view** (about $33 of Google credit).

### 3.3 Building the 2B training file: `data/v14_parts/train_2b_golden_kd.jsonl`

`build_2b_kd.py` reads the frozen `golden_train.jsonl` and writes a NEW file with the same row ids. The trainer reads only `meta.teacher`, and with kd 0.5 its target is `0.5 × smoothed gold + 0.5 × teacher`. That is the tested setting; there is no per-row weight [M4 dropped].

| Row type | Count (types overlap) | What goes in `meta.teacher` |
|---|---|---|
| Human vote-share, near-miss-bundle and exact-probability rows (`meta.teacher` present, not blend50) | 43,363 (includes the 238 `gd_gen2_probability` rows) | **Unchanged: the human or exact distribution** (roadmap item 7). The 238 exact-probability rows train on p exactly through `kd_full_src`. |
| In-sample for 4B-E (all are replay rows) | 47,752 | **No teacher.** Gold with label smoothing 0.05. Old blend50 teachers are deleted, and `kd_skip_src` also strips them. |
| Attacked twins, the 'b' side of the 35,214 inv pairs [S6] | 35,214 (31,936 marked attacked + 3,278 replay claim-injection rows) | If the clean partner's final teacher gives the gold answer (yes/no: p_yes ≥ 0.5 ⇔ gold = 1; choice: argmax = gold, ties count as wrong), **copy the partner's teacher dict**, with `teacher_src = "q35_4b_E_clean_copy"`. Otherwise **delete** `meta.teacher`. Never read the teacher on attacked text. |
| `gold_probs` choice rows | 192 | Unchanged: the trainer uses `gold_probs` and ignores any teacher. |
| csqa duplicate-option rows | 3 | No teacher. |
| All other labelled rows | about 380K (the builder prints the exact number) | `meta.teacher` = 4B-E probabilities (yes/no: `{"yes": p}`; choice: the full softmax over all options). `teacher_src = "q35_4b_E"`. The raw read is also kept in `meta.teacher4b` for audit. |
| Complement pairs (36,958; all golds hard and exactly complementary) | where both rows have fresh 4B-E teachers | `t_a ← (t_a + 1 − t_b)/2`, then `t_b ← 1 − t_a`. This cancels any constant Yes-letter bias shared by the two reads. |

**Validation, done in the builder and again in `check_rows`:**
- teacher keys equal the options exactly, and the sum is 1 ± 0.01;
- yes/no teacher values lie in [0, 1];
- options are unique.

The builder prints the final kd-target count, which becomes `expect_kd_targets`. It also asserts that no `teacher_src` it writes matches `kd_skip_src`.

### 3.4 Label audit before 2B step 0 [S7] (CPU plus Claude, about 300 rows, 0 GPU)

- **Out-of-sample rows only.** Rank rows by loss within groups, not with a fixed p < 0.05 cut. On 4B-E's dev predictions that cut flagged 0 of 4,329 yes/no rows.
  - Yes/no: flag p(gold) < 0.10 after the fitted yes/no temperature T (0.65), or the lowest 3%.
  - Choice: flag the lowest 3% by p(gold) within option-count buckets (2-4 / 5-9 / 10-19 / 20+).
  - Vote-share rows: flag |p_teacher − share| ≥ 0.5.
- Keep designed-hard rows (twins, near-miss, definition swaps, attacks) out of the bug hunt.
- **Outlier groups:** groups with a flag rate at least 2 pp above their question-type/bucket baseline and n ≥ 100. Audit the top 10 by excess × n, 30 rows each. Also audit 100 flagged rows spread across groups and 100 random disagreement rows from human-labelled sources.
- **Action rules:**
  - Generator groups with 15 or more of 30 audited rows wrong: fix the rule and regenerate. This is the precedent from D6 (gen_msn_consent). Apply the same fix to golden_dev. Regenerated rows get new 4B-E labels or no teacher. Filter the relations file for any dropped ids, and re-run the step-count replay.
  - Human-labelled sources: fix only pipeline bugs, such as an inverted label map, a wrong column, or truncation that removes the evidence. **Never relabel because Claude disagrees with the annotators**, above all on moral norms.
  - Never drop rows automatically. Automatic noise filtering can hurt BERT-class models (https://arxiv.org/abs/2204.09371), and at our noise level the expected gain is about 0.
- Record the tables and decisions in budget_ledger.md.

### 3.5 Config: new `runs/q35_2b_main.json`

```json
{
  "name": "q35_2b_main500k",
  "base": "Qwen/Qwen3.5-2B",
  "base_revision": "FILL_FROM_SMOKE_hf_refs_main_sha",
  "recipe": "A3",
  "train_file": "v14_parts/train_2b_golden_kd.jsonl",
  "rel_file": "v14_parts/golden_relations.jsonl",
  "epochs": "FILL_FROM_CPU_REPLAY_of_this_file (0.9712363276890207 if rows and units are unchanged)",
  "lr": 1e-04,
  "batch": 16,
  "r": 32,
  "alpha": 64,
  "dropout": 0.05,
  "lam": 1.0,
  "beta": 1.0,
  "kd": 0.5,
  "kd_skip_src": ["blend50"],
  "kd_full_src": ["gd_gen2_probability"],
  "label_smooth": 0.05,
  "lam_inv": 1.0,
  "sym_cons": true,
  "perm_twin": 0.3,
  "lam_p": 0.5,
  "aux_norm": "micro",
  "micro_tokens": 16384,
  "prism_x": "I",
  "seed": 20260925,
  "grad_ckpt": true,
  "style": "cygnet",
  "layout": "schema_branch_mark",
  "targets": "QWEN35",
  "snap_every": 2500,
  "snap_fracs": [0.85, 0.90, 0.95],
  "expect_trainable": "FILL_FROM_2B_SMOKE_PRINT",
  "expect_kd_targets": "FILL_FROM_build_2b_kd_PRINT",
  "ablate_splits": ["eval_jagged", "eval_opi", "eval_redef", "dev_nc"],
  "ckpt_every_min": 10,
  "log_every": 50
}
```

The FILL_ strings are deliberate: the trainer fails loudly until they are replaced.

**Choices:**
- **From base, not v11r.** v11r carries legacy Qwen3-235B lineage, which the ledger says to drop (budget_ledger.md:90).
- **Tested values:** r32/a64, lr 1e-4, loss weights 1/1/0.5, label smoothing 0.05, kd 0.5. These match arm I (logs/q35_2b_armI_1600.json).
- **Why `aux_norm` "micro" with `micro_tokens` 16384, not the nominal weights the 4B uses:**
  - This reproduces the regime in which arm I earned its +2.1 pp and 1.1% jagged ASR: about 0.7x consistency/invariance weight and about 0.54x anchor on this file.
  - Which regime is better for the 2B: **not sure**. The only comparison (E on the H100 vs E_L4) is confounded.
  - If C1 is not coded, drop the `aux_norm` key; the default behaviour is the same.
- **PRISM-X learning rates stay at the defaults** [O6]: lr_gate 3e-3, lr_authority 1e-3, lr_head 3e-4, lr_shadow 2e-5.
- **Delete `prism_x`** if the section 3.1 gate fails.
- **Rejected:** label smoothing 0, teacher sharpening, and w = 0.7 when the teacher is right (reasons in section 7).

### 3.6 Where it runs and what it costs
- **With $300 on Modal:** the 2B trains on the **H100**. Estimate 13-16 h, about **$56-70** including overhead; not measured on the golden set. Cap $65. Any shortfall finishes on the L4 through C9.
- **If the 4B needs more than $135 (decision 4) or credit is $118:** the 2B trains on the L4. About 13 s/step × 30,457 steps ≈ 4.6-4.8 days, about $110-115 of Google credit. In that case, 1 teacher view only (section 6).
- **2B smoke first** (H100, and the L4 if it may be used): the heaviest real micro-batches at 16384 (worst about 36,864 real tokens), speed, and the printed trainable count.

### 3.7 Teacher switch rule (pre-registered)
The teacher stays 4B-E. Switch to the new 4B only if **all** of these hold:
- (a) it finishes before the 2B starts;
- (b) it is at least +1.0 pp over 4B-E on dev-select;
- (c) on 3K training rows vs 3K dev rows from the same sources, the accuracy gap is ≤ 2 pp AND the gap in mean gold-option probability is ≤ 0.03 (a check that it has not memorised its training rows);
- (d) relabelling (about 33 L4-h per view) fits the budget and schedule.

Default: start the 2B with the 4B-E labels as soon as they are ready. Do not wait.

### 3.8 Lineage disclosure (on the 2B card and in the ledger)
- 4B-E descends from v13t ← v11c ← v11b ← (0.3 v10 + 0.7 v11).
- v10's lineage includes v0.8 LAH items authored by Qwen3-235B and verified by gpt-oss-120b.
- The v0.11 task-bank texts were written by Mixtral.
- The arm I/E evidence used blend50 teacher labels.

This is consistent with the owner's rule ("distilling from our own trained 4B into the 2B is fine; disclose the lineage"). Stop only if the owner objects.

---

## 4. No-regression protocol

### 4.1 CPU checks before 4B step 0 (no GPU)
1. The existing resume tests (73/73) still pass, plus the new tests for C1, C3, C4, C5, C6, C7 and C10.
2. Replay of `batches()` on the final 4B file, which confirms `epochs` → 30,457 steps.
3. Offline tokenization of all 501,732 rows in layout E with the pinned tokenizer, ranking the heaviest real micro-batches for the smoke run.
4. The C1 pre-pass: per-micro counts equal the batch counts for all 30,457 batches.
5. **`PREREG_FINAL.md` is written and committed.** It holds the candidates, snapshot steps, ship rule, constraints and the order of tests (section 4.4). It must exist before step 0, so the snapshot choice cannot adapt to the run.

### 4.2 Pilot runs (Modal about $12-15, cap $25; plus L4 time). All criteria are fixed in advance.

| Pilot | Where | Pass criteria |
|---|---|---|
| 4B smoke, about 150 steps, then the heaviest micro-batches | H100 | Loss falls; no out-of-memory; memory ≤ 90%; the trainable count prints 32,464,896; kd_targets 43,363; all startup checks pass; s/step recorded |
| 4B heaviest micro-batches at the chosen `micro_tokens` | L4 | Same memory rule. If it fails, the 4B has no L4 tail. |
| Relay proof test (A1, A2 straight 300 steps; B 150 + relay + 150) | H100, 2 accounts | LR, counts and batch hashes identical. d(A1,B) ≤ 1.5 × d(A1,A2) for weights and for the loss curve. |
| H100 → L4 resume, from a 50-step checkpoint, with C9 | H100 + L4 | "resumed_at_step … all match"; only allowed env keys differ; LR and batch hashes match; loss within straight-vs-straight noise (not bit-exact) |
| 4B-E teacher smoke + view test | L4 | Section 3.2, step 1 |
| 2B smoke | H100 (+ L4) | Memory rule at 16384; trainable count printed; PX stats logged |

**No learning-rate pilot.** Short pilots cannot resolve LR for a 30K-step run: the confidence intervals of our 800-step arms are about ±1.1 pp, bigger than the effect.

### 4.3 During the run
- **Every relay segment, check:**
  - task loss trend;
  - `gn`, `gn_med`, `clip_frac` and ALERT lines (C3);
  - the effective per-term weights (C1);
  - LR;
  - s/step, and the projected end cost against the cap.
- **ALERTs never trigger an automatic action.** A rollback, if ever needed, is a manual rename of `_ckpt_good`.
- **At each handover,** copy `models/<name>/snaps` to local storage (`modal volume get`). Resuming does not need them.
- **Mid-run catastrophe check (4B):** score snapshot s002500 on the dev-select gate splits on the L4, merged, with the layout checked.
  - Stop and consult the owner only if it is more than 3 pp below q35_4b_v11 on the splits where v11 predictions exist, or if its outputs are near-constant.
  - A model in the middle of its cosine schedule is not comparable to a finished one, so there is no stricter threshold.
- **2B PRISM-X drift [O6]:**
  - Let S2 = the running sum of lr_multiplier². I_1600 ended at S2 ≈ 597.
  - Reference band: auth_rms ≈ 0.0205 × √(S2/597), and gamma ≈ 0.19 × √(S2/597).
  - Flag if auth_rms or atanh(gate_mean) exceeds 2x the band, or atanh(gate_max) grows faster than linearly in the cumulative LR for 3 or more checkpoints.
  - On a flag, do not change any LR. The resume refuses changed configs, and the restored optimizer would undo it anyway. Instead, score the latest `_ckpt` on dev-confirm with PRISM-X on and off, against I_1600. Stop and consult only if it is more than 1 pp below I_1600 with the lower CI bound below 0.

### 4.4 Candidates and choice (as written in `PREREG_FINAL.md`)
- **C1** = the final adapter. This is the default.
- **C2** = exact `cat` average, weights 0.25 each, of s025888, s027411, s028934 and the final adapter (4B). The same fractions for the 2B.
- **C3** (4B only) = W = base + 0.75·ΔW_new + 0.25·ΔW_4B-E, exact `cat` merge [O4].
  - Evaluate C3 only if C1 fails a per-family, security or calibration constraint on dev-select.
  - Choose it only if it passes every constraint on select AND confirm, its confirm accuracy is ≥ C1 − 0.3 and ≥ 81.49, and its yes/no accuracy ≥ C1's.
  - Check first that weights (1,0) and (0,1) reproduce fresh single-adapter predictions: argmax agreement ≥ 99.5%, mean |dp| < 2e-3.
  - Disclose lineage if it ships.
- **REF** = 4B-E (4B) / v11r (2B; better than I_1600 on dev-select, 75.62 vs 75.16).
- **Replacement rule:** C2 or C3 replaces C1 only if it is at least +0.3 pp on select AND ≥ 0 vs C1 on confirm.
- **Test order vs REF:** the chosen candidate first, then C1, then REF.

### 4.5 Ship rule vs REF [M9, corrected]

**Why not a confirm-only test.** Dev-confirm has been used in about 20 earlier gates, and 4B-E was partly chosen on it. Against all 6 sibling 4Bs, 4B-E scores +0.7 to +1.3 pp better on confirm than on select. A test on confirm alone is tilted toward REF by about 0.5 pp. So the test pools **both dev halves** (about 8.1K rows, about 4.4K groups), using a paired group bootstrap (10k resamples, seed 0).

**Ship if all hold:**
- pooled difference ≥ **+0.2 pp**;
- pooled 95% lower bound > **−0.75 pp**;
- neither half is below −0.75 pp.

**Constraints**, pooled, with T cross-fitted per question type (fit on one half, score the other):
- yes/no accuracy ≥ REF − 1.0 pp;
- choice accuracy ≥ REF − 1.0 pp (the roadmap's "choice not materially down");
- calibrated yes/no Brier ≤ REF + 0.005;
- equivalence/permutation flip rate ≤ REF + 2 pp;
- jagged and OPI attack success rate (ASR):
  - 4B: ≤ max(REF + 2 pp, 3%). 4B-E jagged is 0.6%, OPI 1.0%.
  - 2B: ≤ min(8.8%, REF + 3 pp). v11r jagged is 3.9%.
  - An ASR veto also needs the bootstrap lower bound of the increase to be > 0.

**Claims:**
- "Better than 4B-E" only if the pooled lower bound > 0.
- "Yes/no clearly up" only if the pooled yes/no lower bound > 0.

The smallest difference we can detect is about 1 pp; say so in the write-up.

**Report only, never decisive:**
- per-split drops greater than 2 pp;
- negative and positive flip rates (4.3% / 3.7% between close 4Bs today);
- mean log p(gold) after T;
- golden_dev, as an in-family sanity check.

**Log every look** at the ledger.

### 4.6 Fallbacks
- **New 4B fails:** ship 4B-E. The 2B plan is unaffected, because its teacher is 4B-E.
- **New 2B fails:** ship v11r (disclose its legacy lineage), or I_1600 if the owner prefers the clean lineage.
- **Run dies before 85%:** score the last `_ckpt` adapter and the `cat` average of the last 3 every-2,500 snapshots on dev-select. Choose by the same rule against REF.

### 4.7 Held-out discipline
- Only dev splits are used for choices.
- Never golden_dev, OHS-2 or JevBench half B for selection.
- **OHS-3 runs once**, after all choices are frozen and model sha256 values are added to PREREG_OHS3. It needs Jev's OHS-3 answers, which need the rotated OpenRouter key (open item).
- No JevBench leaderboard submission until the owner says.

---

## 5. Serving-time changes (all inference-only, all gated on dev)

### 5.1 Temperature [M10]
- Fit one T per question type (yes/no, choice) by NLL on the pooled **dev-select** half, on each final model's exact serving path (after TTA, if adopted). Grid 0.5-2.0. No per-source T: OHS-3 has unseen sources.
- **Apply T to the final probability vector** (`calibrate.scaled`), after any view averaging. Do not apply it through `to_probs(temp=)`, which tempers each view before averaging and can flip choice answers.
- **Ship T ≠ 1 only if**, on dev-confirm, pooled yes/no Brier improves by at least 0.002 AND no split's yes/no Brier worsens by more than 0.003.
- **Today:**
  - 4B-E: T = 0.9 / 1.0, gain 0.0006. Ship T = 1.
  - 2B I_1600: T = 0.7 / 0.95, Brier 0.1505 → 0.1483, ECE 0.039 → 0.023. It fails the per-split check (dev_negwords +0.0051), so re-check on the final 2B.
- **Caution:** temperature scaling degrades under distribution shift (https://arxiv.org/abs/1906.02530). Calibration cannot close the Brier gap to Jev: the whole gap is resolution (our REL 0.0041 vs Jev's 0.0071).

### 5.2 Two-view test-time averaging (TTA) [S8]
- Views: identity plus reversed options (choice rows); Yes/No letters swapped (yes/no rows). Averaged in probability space.
- Compare a merged single read (`_merged`) with merged TTA (`_tta`) of the same model, in the same job.
- **Adopt per type:**
  - yes/no swap if the yes/no delta ≥ +0.5 pp;
  - choice reversal if the choice delta ≥ +0.3 pp;
  - each also needs: overall delta ≥ 0 with lower bound > −0.3 pp, the same sign on select, calibrated Brier not worse by more than 0.002, and jagged/OPI/redef ASR not worse by more than 1 pp.
- **Expected:** overall about 0 to +0.4 pp, mostly on yes/no.
  - Old v10: +0.25 pp [−0.31, +0.76] overall; yes/no +0.42 pooled; it lost on devzs/devzs2 and on JevBench A (102 vs 104).
- **Cost:** 2x inference. Layout E shares no KV prefix between views. Still far under Jev's 239 ms.
- The 4B-E result is only indicative; repeat the test on the final models.

### 5.3 Cascade [S10]
- **Headline system: the final 4B alone** (plus TTA and T if adopted). The 2B is the fast tier.
- **Current models:** 2B I_1600 → 4B-E loses −1.01 pp at 40% routing (95% [−1.78, −0.25]) and −0.49 at 60% ([−0.87, −0.13]). The earlier "cascade = 4B accuracy" finding used the weaker v13t.
- **Budget choice:** for each budget in {0.3, …, 0.8}, set the threshold on dev-select. Choose the smallest budget whose one-sided 95% select lower bound vs the 4B is > −0.5 pp. Report dev-confirm once, at that budget only.
- **Route on the raw 2B max probability** (or margin). Calibration did not improve routing: −1.14 vs −1.01 at 40%.
- **Use the cascade only if** (measured 2B/4B inference cost ratio + routed fraction) < about 0.85. The 0.46-0.48 ratio comes from training step times; the inference ratio is **not measured**. With current models the rule picks 70% routing, about 1.15x the 4B's cost, so we serve the 4B alone.
- **Also report** cascade ASR and the routed fraction under attack. Cascade-targeted attacks can inflate cost and attack success (https://arxiv.org/abs/2605.17288).

### 5.4 Security claims [S11]
The recipe is unchanged (layout E, attack twins with lam_inv, perm_twin, sym_cons, definition-swap twins). But before claiming "more secure than Jev", run an evaluation-only adaptive attack in the JevOut style (https://arxiv.org/abs/2609.30243, code https://github.com/xzx34/JevOut):
- Targets: the final 4B, the final 2B and the cascade. Dev items only.
- Our model's probabilities are the scorer, scored in `schema_branch_mark`, with PRISM-X loaded for the 2B.
- Claude writes the candidate context; no bigger models.
- A gold-preservation check (rule or Claude), plus a Claude audit of about 50 successful flips.
- **The same pipeline and budget against Jev** (64 target evaluations per decision; evaluation only, never training). Otherwise report the paper's 61.4% only as "not matched".
- Add variants with the injection at the start of the text, and marker-spoofing variants: a fake `<<<UNTRUSTED TEXT END>>>`, then fake rules. The markers are not escaped today, and the weights are open.
- Label the result a lower bound (best-of-N search, not white-box).
- Cost: about 1-3 L4-h.
- **Never train or tune on the results.** Security numbers vary between runs (jagged ASR 5.8-35.5% across similar recipes), so the claim is about the shipped checkpoint only.

---

## 6. Budget

**Modal ($300; H100 $3.95/h; +10% CPU and memory per the ledger).** All GPU-hour figures are estimates, not measurements, until the smoke run.

| Item | GPU | Estimate | Cap |
|---|---|---|---|
| Pilots (4B smoke, relay proof, H100→L4 resume test, 2B smoke) | H100 | about 3 h, $12-15 | $25 |
| 4B main pass, 30,457 steps | H100 relay | 26-32 h (not measured) → $113-139 | $135 (full pass needs ≤ 3.34 s/step) |
| 2B pass | H100 | 13-16 h (not measured) → $56-70 | $65 (tail on the L4 if over) |
| Gate and evals on Modal (most evals run on the L4) | – | about $5 | $5 |
| **Reserve, untouchable** | – | – | **$40-60** |
| **Total planned** | | | **$230 + reserve ≤ $300** |

If decision 4 applies, the 4B cap rises to $175 (full pass if ≤ 4.33 s/step) and the 2B moves to the L4: pilots $25 + 4B $175 + evals $5 + reserve $60 = $265.

**Google L4 (about $200 of headroom before the kill switch; about $0.9-1.0/h from ledger G2 and the 30 Sep plan):**

| Item | L4 hours | About $ |
|---|---|---|
| Teacher smoke + view test | 2 | 2 |
| 4B-E labels, 1 view, 424.7K rows | 33 | 33 |
| 2nd view (only if section 3.2 triggers it AND the 2B is on the H100) | +33 | +33 |
| Dev evals, TTA, blends, calibration, cascade, s002500 check | 10-15 | 10-15 |
| Adaptive attack eval | 1-3 | 3 |
| OHS-3 once | a few (not measured) | a few |
| **Subtotal (2B on the H100)** | **about 50-85** | **about $50-90** |
| Fallback: 2B pass on the L4 | about 110-115 | about 110-115 |
| **Subtotal (2B on the L4, 1 view only)** | **about 160-170** | **about $160-170**, near the limit, so no 2nd view |

**If Modal credit is really $118** (the 30 Sep resources note):
- About $10 for pilots leaves about 22.6 step-hours for the 4B.
- A full pass needs ≤ 2.67 s/step. Otherwise trim uniformly (for example, 3.3 s/step → about 24,650 steps, 81% of a pass).
- The 2B runs on the L4. There is no reserve. The owner must accept this.

---

## 7. What we deliberately do NOT do

**From the research round: checked and dropped, or rejected at merge.**

| Idea | Why not | Source |
|---|---|---|
| Per-row reliability weights for the 4B teacher [M4] | Untested vs uniform kd 0.5. It removes KD's damping exactly where our labels are noisiest. The published per-class gains are mixed (−0.2 to +0.2 pp mostly). | https://arxiv.org/abs/2106.10494, https://arxiv.org/abs/2002.03532 |
| w = 0.7 where the teacher is right; tuning w on GPU pilots | w > 0.5 is untested. Pilot CIs (about ±1.1 pp) exceed the effect. | https://arxiv.org/abs/2608.27729 |
| Label smoothing 0 or teacher sharpening for the 2B | Measured I_LS0: −1.29 pp [−2.42, −0.18]; the under-confidence stayed. | ledger X16; https://arxiv.org/html/2407.14679 |
| View-matched teacher labels (each view its own label) | Cannot be consumed: the trainer redraws permutations and looks up targets by option. | decoder_io.py:397-433, train_decoder.py:721-722 |
| Starting the 2B from merged v11r | Legacy Qwen3-235B lineage. | budget_ledger.md:90 |
| r32/alpha64 on the 4B, or a higher rank | Never run on the 4B; acts as a 2x LR on B. | https://thinkingmachines.ai/blog/lora/ |
| LR changes (2e-4 to 5e-4, or halving), and a short LR pilot | Untested at a 30K-step horizon; higher LR forgets more. | https://arxiv.org/abs/2409.19913, https://arxiv.org/abs/2410.21228 |
| Larger batch | LoRA pays a large-batch penalty and would need a retune. | https://arxiv.org/abs/2602.09492 |
| DoRA, rsLoRA, LoRA+, PiSSA-style initialisations | Within 1-2% once LR is tuned. The inits that modify base weights break `disable_adapter()`, and so the KL anchor. | https://arxiv.org/abs/2602.04998 |
| Full fine-tuning; training lm_head/embeddings; DeltaNet internals | Over budget, or +635.7M parameters with no evidence of gain. | https://arxiv.org/abs/2405.09673, https://arxiv.org/abs/2410.09016 |
| WSD schedule; LAWA probes with early cooldown | About 1.7x the LR area of cosine, untested; evidence is from pretraining. | https://arxiv.org/abs/2405.18392 |
| Schedule-Free AdamW; weight decay; new betas | New behaviour in a one-shot run with no evidence of gain. | https://arxiv.org/abs/2405.15682 |
| Capping the ramp to 1,568 steps [O1] | About 0 effect, and it would need an edit to the trainer. | https://arxiv.org/abs/1703.01780 |
| Yes/No letter-swap twins for the 2B [O2] | Rows already get a random Yes/No order every draw; about +10% compute. | https://arxiv.org/abs/2106.14448 |
| Saving raw logits [O5] | Probabilities already carry the same ranking information. The return-type change touches 12 call sites. | https://arxiv.org/abs/2403.14715 |
| Batch calibration at serving [S9] | Breaks even at about a 70% majority class; −5.7 to −15 pp on skewed streams in our simulation; can be poisoned. | https://arxiv.org/abs/2309.17249, https://arxiv.org/abs/1901.06852 |
| Up-weighting families 1.5-2x (roadmap item 2), curricula, temperature sampling | In-family gains did not transfer (A18, G2). Resampling hurt in Muppet. Costs +10-22% compute. | https://arxiv.org/abs/2101.11038, https://arxiv.org/abs/2511.18903 |
| Capping gd_gen_* generators to fit budget | Protected priority data, mostly yes/no; use a uniform trim instead. | https://arxiv.org/abs/2109.01652 (no ablation of the cap) |
| Per-family loss weights, PCGrad, focal loss, prior corrections | No gain over a plain weighted sum; the yes rate is 0.50 in every family. | https://arxiv.org/abs/2209.11379, https://arxiv.org/abs/2211.11838 |
| Noise-robust losses, auto-filtering, dropping replay rows | Can hurt BERT-class models; replay prevents forgetting. | https://arxiv.org/abs/2204.09371, https://arxiv.org/abs/2502.06042 |
| Truncating long rows; extra dedup | Long rows are about 1.9% of compute; truncation changes answers in layout E. | local audit |
| R-Drop, 2nd 4B epoch, multi-seed soups, cross-fitted teachers | Each needs extra full passes. | https://arxiv.org/abs/2203.05482 |
| DKD, DIST, reverse KL, T > 1, feature or on-policy KD, rationale distillation | Degenerate at 2 classes; online teacher; needs bigger models. | https://arxiv.org/abs/2203.08679, https://arxiv.org/abs/2605.11513, https://arxiv.org/abs/2305.02301 |
| Learned per-question T; per-source T | X10: learned T rose to 2.1 and Brier got worse; per-source T fails on unseen sources. | https://arxiv.org/abs/1906.02530 |
| SecAlign/DPO or new security modules in the final run | Untested; ASR noise between runs would hide any benefit. | https://arxiv.org/html/2507.02735 |
| Cascade as accuracy headline; abstention | −0.5 to −1.0 pp today; the benchmarks are forced-choice. | https://arxiv.org/abs/1705.08500 |
| Blend with 4B-E as the default serving model | Only as one pre-registered fallback (C3). | ledger G3, A4 |
| Averaging LoRA A and B separately | mean(B)·mean(A) ≠ mean(B·A); use `cat`. | https://huggingface.co/docs/peft/en/package_reference/lora |
| Retyping CLI flags to resume; `fresh_start` after a fingerprint error | Discards the checkpoint; use C9. | train_decoder.py:647-658 |
| Two seeds, or a 20K-row A/B pilot (29 Sep recipe item 6) | Not affordable, and not resolvable at our CI width. | ledger |
| Tuning on golden_dev, OHS-2 or JevBench half B | Forbidden, or not informative. | project rules |

---

## 8. Open risks, ranked

1. **The new 4B does not beat 4B-E.** Likelihood: not sure, and real. Earlier broad data gave only +0.6 pp, and 4B-E's confirm score is somewhat inflated. *Mitigation:* the pooled non-inferiority rule; 4B-E stays in service; the 2B plan is unaffected because its teacher is 4B-E; honest reporting.
2. **The speed or budget does not fit a full pass.** *Mitigation:* s/step measured in the smoke run; the fixed rule in section 2.4 (move the 2B to the L4 first, then a uniform trim); never stop mid-schedule; the L4 tail through C9.
3. **Out-of-memory at a fixed step on every resume**, most likely on the 24 GB L4. *Mitigation:* offline ranking of real token counts; the smoke run on both GPUs with the heaviest real micro-batches; expandable_segments.
4. **Silent misconfiguration:** wrong layout in labels or evals, config keys ignored, teacher labels not consumed, a perm mapping bug in `to_probs`, truncated shards. *Mitigation:* C2 (unknown keys, count checks), C6, the C7 identity test, C10 completeness checks, the teacher smoke rule.
5. **The relay breaks:** code hash, environment, a missing checkpoint that silently restarts at step 0. *Mitigation:* the frozen tag and worktree, the `git diff` guard, `expect_resume`, the environment guard, the pre-registered proof test.
6. **The yes/no gap to Jev stays** (moral norms, tables). It looks like knowledge and reasoning, not calibration. *Mitigation:* none guaranteed. The per-type TTA gate may add a little on yes/no. Report the gap honestly.
7. **The 2B from base ends below v11r.** *Mitigation:* ship v11r (disclose its lineage) or I_1600; cascade fallback.
8. **Security regression or run-to-run swings.** *Mitigation:* the ASR veto in the ship rule; the adaptive attack eval before any claim; claims only for the shipped checkpoint.
9. **NaN or loss spike poisons the only checkpoint.** *Mitigation:* the C3 non-finite guard before `opt.step()`, `_ckpt_good`, snapshots.
10. **PRISM-X drift.** The 2B's PRISM-X modules get about 19.6x more learning rate than was ever tested. *Mitigation:* the scaled band in section 4.3, a dev check, no LR edits mid-run.
11. **Dev-confirm reuse and REF inflation** bias the decision. *Mitigation:* pooled halves, fixed candidates, every look logged, OHS-3 once.
12. **Google credit kill switch mid-labelling.** *Mitigation:* crash-safe shards; 1 view if the 2B is on the L4; spot L4 considered.
13. **Label noise (1.3-2.7% wrong; replay about 6%).** *Mitigation:* the section 3.4 audit; fix only confirmed bugs.
14. **Lineage and compliance.** *Mitigation:* disclosure on the cards (section 3.8); no bigger models used anywhere.

---

## 9. Sources

**Opened and checked in the 30 Sep verification pass:**
- Gradient accumulation normalisation: https://huggingface.co/blog/gradient_accumulation
- Prompt-format sensitivity: https://arxiv.org/abs/2310.11324
- Minitron (KD temperature τ = 1): https://arxiv.org/html/2407.14679 ; teacher correction: https://arxiv.org/html/2408.11796
- KD analyses: https://arxiv.org/abs/2105.08919 , https://arxiv.org/abs/2002.03532 , https://arxiv.org/abs/2508.00264 , https://arxiv.org/abs/1910.01348 , https://arxiv.org/abs/2106.05237
- PEFT adapter dtype: https://huggingface.co/docs/peft/package_reference/peft_model ; `cat` merge is exact: https://huggingface.co/docs/peft/en/package_reference/lora
- bf16 training: https://arxiv.org/abs/2010.06192 ; CUDA allocator: https://docs.pytorch.org/docs/2.14/notes/cuda.html ; Modal images: https://modal.com/docs/guide/images
- Holdout reuse and testing: https://arxiv.org/abs/1506.02629 , https://proceedings.neurips.cc/paper/2019/file/ee39e503b6bedf0c98c388b7e8589aca-Paper.pdf , https://arxiv.org/html/2411.00640 , https://aclanthology.org/W04-3250/ , https://aclanthology.org/P18-1128/ , https://aclanthology.org/2021.acl-long.515/ , https://www.fda.gov/media/78504/download
- Calibration: https://arxiv.org/abs/1706.04599 , https://arxiv.org/abs/1906.02530
- LoRA rank and LR: https://thinkingmachines.ai/blog/lora/ , https://arxiv.org/pdf/2106.09685 , https://arxiv.org/abs/2405.09673 , https://arxiv.org/abs/2602.04998 , https://arxiv.org/abs/2404.05405 , https://arxiv.org/abs/2312.03732
- Data mixing: https://arxiv.org/abs/2109.01652 , https://jmlr.org/papers/volume21/20-074/20-074.pdf
- Weight averaging: https://arxiv.org/html/2502.06761 , https://arxiv.org/html/2405.18392 , https://arxiv.org/abs/2306.03241 , https://arxiv.org/abs/2505.12082
- Spikes and optimiser: https://arxiv.org/abs/2204.02311 , https://arxiv.org/abs/2504.02507 , https://arxiv.org/abs/1412.6980
- Option-order bias and TTA: https://arxiv.org/html/2403.13590v1 , https://arxiv.org/abs/2309.03882 , https://aclanthology.org/2024.findings-naacl.130/ , https://arxiv.org/html/2511.21709
- Robust distillation: https://arxiv.org/abs/1905.09747 , https://arxiv.org/abs/2108.07969
- Label errors: https://arxiv.org/abs/2205.12702 , https://arxiv.org/abs/1911.00068 , https://arxiv.org/abs/2204.09371 , https://arxiv.org/abs/2305.16337
- Cascades: https://arxiv.org/abs/2307.02764 , https://arxiv.org/abs/2305.05176 , https://arxiv.org/abs/2605.17288
- Adaptive attacks: https://arxiv.org/abs/2609.30243 , https://github.com/xzx34/JevOut , https://arxiv.org/abs/2510.09023 , https://arxiv.org/abs/2507.07417 , https://arxiv.org/html/2507.02735
- Proper scoring and soft labels: https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf , https://arxiv.org/abs/1908.07086
- Model blending: https://arxiv.org/abs/2109.01903 , https://arxiv.org/abs/2203.05482 , https://arxiv.org/abs/2309.06256 , https://arxiv.org/abs/2205.12411 , https://arxiv.org/abs/2410.19735 , https://arxiv.org/abs/2401.12187
- Items considered and dropped: https://arxiv.org/abs/2106.10494 , https://arxiv.org/abs/2102.00650 , https://arxiv.org/abs/2203.08679 , https://arxiv.org/abs/2005.10419 , https://arxiv.org/abs/2309.17249 , https://aclanthology.org/2024.naacl-long.378.pdf , https://arxiv.org/abs/1901.06852 , https://arxiv.org/abs/1703.01780 , https://arxiv.org/abs/2106.14448 , https://arxiv.org/abs/2406.01026 , https://arxiv.org/abs/2403.14715

**Cited in the merge step, not re-opened in the verification pass:**
https://arxiv.org/abs/2608.27729 , https://arxiv.org/abs/2502.06042 , https://arxiv.org/abs/2409.19913 , https://arxiv.org/abs/2410.21228 , https://arxiv.org/abs/2602.09492 , https://huggingface.co/Qwen/Qwen3.5-4B/raw/main/config.json , https://arxiv.org/abs/2410.09016 , https://arxiv.org/abs/2405.15682 , https://arxiv.org/abs/2101.11038 , https://arxiv.org/abs/2511.18903 , https://arxiv.org/abs/2209.11379 , https://arxiv.org/abs/2201.04122 , https://arxiv.org/abs/2211.11838 , https://arxiv.org/abs/2605.11513 , https://arxiv.org/abs/1705.08500 , https://arxiv.org/abs/2305.02301

**Not verified, so not used as evidence:** https://unsloth.ai/blog/gradient (returned 403). The causal-conv1d speed-up note "HF #48718" comes from our plan; I did not re-check it.

**Local evidence** (paths under `/Users/aryamahadik/Documents/jev/opendecide-data/lean/`):
- `train_decoder.py`: compute_loss lines 234-350, the micro loop at 729-779, RUN_KEYS at 397;
- `decoder_io.py`, `od_gcp.py`, `modal_od.py`, `jevbench_od.py`;
- `runs/q35_4b_main.json`, `runs/README.md`;
- `logs/budget_ledger.md` (A18, G2, G3, X3, X7-X17, D5-D7);
- `logs/overnight_plan_28sep.md` (29 Sep 20:00 recipe; 30 Sep resources, cost model and frozen roadmap);
- `logs/relay_protocol.md`;
- `logs/q35_2b_armI_1600.json`;
- `preds_dev/q35_4b_pxE*`, `preds_dev/q35_2b_armI_1600*`;
- `data/v14_parts/GOLDEN_CARD.md`.

CPU replay scripts: `/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/73bb87c6-8519-454d-98bb-7961fcde73b9/scratchpad/` (a4.py, audit4.py, m7/tok_all.py, s2_verify.py, casc_boot.py).