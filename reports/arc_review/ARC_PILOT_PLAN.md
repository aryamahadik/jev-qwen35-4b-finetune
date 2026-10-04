# ARC pilot plan: what to test on Modal, in what order, and what it can reach

4 Oct 2026. Planner. Planning only. I made no Modal, gcloud or paid calls, and I opened no sealed or held-out folder.
Inputs:
- the two verifier reports, `V_latent.md` and `V_other.md`;
- the trainer, readout and Modal launcher (`opendecide-data/lean/train_decoder.py`, `decoder_io.py`, `modal_od.py`);
- `c_spec/C_TRAIN_RECIPE.md` v4 (look table, budget rule);
- `PREREG_FINAL.md` A16 to A16.2 (pins);
- `logs/budget_ledger.md` (X-series results);
- `reports/knowledge_gap/PLAN_knowledge_gap.md`.

Two new facts were measured today, for free, on C1's stored dev reads (CPU, `q35_4b_main500k` preds on the 9 gate
splits). They are in section 0.

## 0. In plain words

1. **Most of ARC has already been tested here.** Our PRISM-X work tested the same ideas:
   - **Option-query head on the 4B:** about zero (X15: +0.59 select, -0.59 confirm).
   - **Small latent loop over cached states, 1-4 steps:** failed on the 2B (arm J, X8). It was -0.69 vs I on
     dev-confirm and hijack rose to 30.4%, though hard_dev gained +3.8.
   - **Trusted/untrusted streams:** already in C1 (layout E, hijack 0%). The heavier forms failed: write-block
     -5.9 pp, policy compiler -1.9 pp.
   - **"Read twice" for consistency:** zero (X19, -0.07).
2. **Calibration is not our problem.** On C1's dev reads:
   - Yes/no Brier is 0.1096, and only **0.0009** of it is miscalibration. The rest is accuracy.
   - Choice (top-1) Brier is 0.1344, of which **0.0021** is miscalibration.
   - So calibration RL, a Brier loss and an error head have almost nothing to fix.
3. **Many options is a small problem on our dev.** C1 is right on 79.7% of 2-4-option items and 78.1% of 5-26-option
   items, but only **45.1% of 27+-option items**. Those are just 233 rows from 2 fine-grained taxonomies:
   empathetic (32 options) and manifesto (56 options). That is a close-distractor problem, which C family F11
   already targets. The Decision Index (DI) tops out at 151 options and our readout already handles 255.
4. **Only one ARC idea is worth Modal money now:** a latent loop in the form the papers support, which re-runs a
   middle block of the backbone's own layers (ETD-style). It is not the small side block ARC proposes.
   - C1 is weakest exactly where this should help: pg_numeric 51.3%, pg_multihop 55.3% (pg_dev overall 65.5%).
   - The pilot costs about **$16** on Modal, with a matched control.
   - My odds that it passes: about 20-25%.
5. **Even if every ARC part works, ARC alone does not beat Jev on the Decision Index.**
   - My range is 54.8-56.8 vs Jev 59.51.
   - Looping layers adds no facts, and GPQA needs long thinking.
   - The only measured lever for GPQA is the opt-in think route in the knowledge-gap plan, which ARC's "no thinking
     fallback" rule would forbid.
6. **The frozen round-1 plan (A16) stays untouched.**
   - The pinned files are unchanged: trainer `c2c2d1d6`, readout `908c08d7`, launcher `c25e4f38`, config
     `f3bb379e`. All four hashes were re-checked today.
   - All pilot code goes into new files.
   - No pilot ever reads the sealed suite. The look table allows only S1, S2 and C.

## 1. Verdict per ARC component

"Our test" means a measured in-house result (ledger rows). "Outside" means the verifier reports.

| # | ARC component | Verdict | Evidence | Expected effect on our 4B |
|---|---|---|---|---|
| 1 | Trusted/untrusted asymmetric streams | **ADOPT (already in C1); REJECT new stream machinery** | Ours: layout E (schema, marked text, trusted question repeated) passed gate L (M5). C1 hijack 0% vs Jev 99%. Heavier versions failed: write-block F -5.89 pp (M6); shadow memory H +1.11 vs its matched control on the 2B, but security got worse (X4, X7) | 0 accuracy; keeps the hijack win |
| 2 | Permutation-equivariant option-query heads instead of letter logits | **REJECT for the 4B** (stays on the 2B as frozen) | Ours: 4B X15 +0.59 [-0.10, +1.25] select, -0.59 [-1.21, +0.02] confirm. 2B matched 1,600-step X18: -0.27. Outside: Set-LLM equals order-averaging at 7-8B (V_other 5). It also blocks CUDA graphs (eager only), which costs latency | 0 (+-0.6 on choice rows). Side gain: definition overwrite 10.2% vs 16.5% |
| 3a | Sigmoid yes/no with the complement rule s(not x) = -s(x) | **REJECT** | A sigmoid on (l_yes - l_no) is the same as our 2-way softmax. The complement term is already in `train_decoder.py` (`cons`, `sym_cons`). A hard version doubles yes/no reads, which are 84% of DI. Ours: "read twice" X19 -0.07 | 0 to +0.4 DI (likely about 0) |
| 3b | Ordinal threshold heads | **REJECT** | Round 1 already has the TRACT-style A4 `lam_ord` term. CORN on text is inside the noise (MAE 1.10+-0.09 vs 1.07+-0.05). Jev's Score scores each level on its own (V_other 3). Ordinal rows are under 1% of training | about 0 |
| 4a | Latent recurrence as proposed: a small shared block over cached backbone states, 1-4 steps | **REJECT** | Ours: PRISM-X J is this design (option queries refined 1-4 steps over cached states). On the 2B, vs I: dev-confirm -0.69 [-1.81, +0.38], hard_dev +3.8, breadth -1.4, Brier +0.008, jagged ASR 30.4% (X8). Outside: the weakest-evidence form, because a block that only reads cached states never re-uses the feed-forward layers (V_latent 5.2) | 0 to +0.4 DI; security risk |
| 4b | Latent recurrence through the backbone: loop one middle layer group, ETD-style | **PILOT (P1)** | Outside: ETD 1B GSM8K +12.5, ARC-C +10.6, MMLU +5.4, but with 50B tokens of full training. Retrofit TinyLlama GSM8K +6.0. Gains shrink with size, and facts stay flat (V_latent 2-3). Never tested on a LoRA'd hybrid DeltaNet model | If it works: GSM8K +5 to +15, CRUX +2 to +8, GPQA 0 to +5, so **DI +0.2 to +0.9**. P(pass) about 20-25% (my estimate) |
| 4c | Step-supervised loop (CODI/LOTUS-style, our own 4B as its own teacher) | **RESEARCH-LATER (P2, only if P1 and its replication pass)** | Outside: LOTUS 3B GSM8K 38.3 → 70.0 (CoT 71.5), but with full fine-tuning on gold steps. CODI works with LoRA r128. Both collapse on long traces (MATH 14.5 vs 52.8) | Upper half of 4b's range |
| 5 | Halting / confidence gate | **RESEARCH-LATER** | Nothing to halt unless the loop helps. Ouro's dynamic exit broke its RL. Fixed k is safer (V_latent 5.4). If P1 passes, fit an exit margin offline from stored per-pass logits on dev-select ($0) | Latency only |
| 6 | Error / uncertainty head | **REJECT for the one-pass model** | Ours, today: dev miscalibration (REL) is 0.0009 for yes/no and 0.0021 for choice. OHS-2 REL 0.0041 vs Jev 0.0071 (X12). The softmax confidence already ranks errors. Its useful form is the router in the knowledge-gap plan (free L4) | about 0 |
| 7 | Two-stage top-k for 100+ options | **RESEARCH-LATER (free report on the L4)** | DI max 151 and our readout covers 255. On our dev, 27+ options means 233 rows from 2 sources, which is a close-distractor issue. `hc.py` (embedding shortlist plus knockout) already exists; read it on `dev_hc` (450 rows, 78-2,000 options) when the L4 is free | DI +0 to +0.2. Matters for product lists over 255 |
| 8 | Generic pretraining replay (~20%) | **RESEARCH-LATER, gated by a free forgetting check; then PILOT P3 if triggered** | Kotha & Liang's 1.87x is LM loss at 150M with full fine-tuning. The "~20%" is not in the paper. We train LoRA, round 1 is already 60% C1-data replay, and the `anchor` KL already exists in code. No forgetting has been measured (V_other 1) | DI 0 to +0.3 |
| 9 | Calibration-aware decision RL (Brier/log + consistency + security - compute) | **REJECT** (no RL, and no Brier-term pilot) | RL helps verbalized confidence, not a logit readout. CE is already the log score (V_other 2). Ours, today: miscalibration is about 1% of our dev Brier, and recipe 6.0 already fits temperatures. Softer probabilities would cost points under the JevBench 0.2-0.8 abstain band | Brier -0 to -0.005; accuracy 0 |
| 10 | "No CoT, no fallback to thinking mode" | **DISAGREE as a product rule (owner decision)** | Thinking on the same 4B reaches GPQA 76.2, about 94% of the gap. No latent method has matched thinking on GPQA (V_latent 4). Keep fast mode one-pass, and keep the knowledge-gap plan's opt-in auto mode | Auto mode: DI 57.4 (56.2-58.6) by that plan's estimate |

## 2. Pilot programme on Modal (one component per pilot, ordered)

### 2.0 Rules for every pilot

- **Start point.**
  - Every pilot starts from **C1** (`q35_4b_main500k`, sha256 507d1c29...) via `init_adapter`.
  - The round-1 candidate is never a pilot start. It is not a shipped model until look C, and pilots must not create
    extra looks.
  - If C later ships a new model, any adopted component is re-tested from that model.
- **Matched control.** Every pilot is compared with **C0**: C1 plus the same steps, same rows, same seed and same
  code path, with the component switched off.
  - X14 showed that 800 extra steps alone moved dev-confirm by +1.36, so comparing with C1 itself would be wrong.
  - X17/X18 showed that an unmatched interim result (+3.46) can shrink to -0.27 when properly matched.
- **No pinned file is edited.** All new code lives in new files:
  - `opendecide-data/lean/arc/loop_block.py`, `arc/train_arc.py`, `arc/read_arc.py`, `arc/build_pilot_mix.py`;
  - `modal_arc.py`, a separate Modal app `opendecide-arc` that writes to `/vol/arc/`;
  - `tests/test_arc_*.py`.
  - A test asserts that the four A16 pins are byte-identical (`c2c2d1d6`, `908c08d7`, `c25e4f38`, `f3bb379e`).
  - The wrapper uses the trainer's existing extension point. `train()` calls `prism_x.param_groups()` and
    `prism_x.save()` at run time, so `train_arc.py` patches those two in-process and wraps
    `peft.PeftModel.from_pretrained` to install the loop right after C1's adapter loads. The loop module is kept
    outside `model.parameters()`, the same way PRISM-X is.
- **Data.** Existing files only. The pilot mix (P1 to P3) is one file, `data/arc_pilot_mix.jsonl`. It has
  1,600 steps × 16 = **25,600 rows**, drawn with seed 20261004 and its sha256 logged:
  - all **6,381** `pg_train.jsonl` rows that C1 never saw (9,069 rows minus 2,688 already in `golden_train`; 0 group
    overlap with `pg_dev`, checked today);
  - all reasoning-family rows of `v14_parts/golden_train.jsonl` (pg_*, proc_*, hard_*, planted_*; 8,903 rows);
  - stratified general replay from the rest of `golden_train` up to 25,600 (about 10,300 rows, about 40%);
  - the matching relations from `golden_relations.jsonl`.
  - Before freezing, a CPU check confirms that no `group_id` in the mix is in any dev split.
  - Loss: C1's loss and weights (KD 0.5, `lam_inv` 1, `sym_cons`, `perm_twin` 0.3, `aux_norm` batch).
  - Settings: lr 5e-5, batch 16, `micro_tokens` 8192, base anchor off. `lam_ord` off, because the mix has no ordinal
    rows by design.
- **Clean dev sets (ours only).** Decisions use the **confirm half**, as defined by `gate_dev.py`:
  sha256("devsel:" + group_id) odd. The select half is reported.
  - **R, reasoning dev, 1,650 rows:** `pg_dev` 1,049 + `hard_dev` 208 + `proc12_dev` 159 + `planted12_dev` 137 +
    `hard12_dev` 97. C1: pg_dev 65.5, hard_dev 79.8. The confirm-half SE is about 1.3 pp at 10% disagreement.
  - **G, general no-harm:** the 9 gate splits (`dev_nc, taskbank_dev, hard_dev, dev_negwords, dev_claims, pg_dev,
    devzs, devp_card, dev`), standard read plus seeded `_perm` read. Paired group bootstrap, 10,000 resamples, seed 0,
    reusing `gate_dev.py` by import (no edit). The measured SE is 0.43-0.52 pp.
  - **S, security:** `eval_jagged` (972 rows), `eval_opi` (1,080 rows).
  - **M, mix-tuning dev**, once the C mixer has written it. Report only. Its F2 (rule arithmetic) and F3 (state
    tracking) families are untrained for both arms, so they are a clean transfer test. Pilot reads of it never feed
    any C decision.
  - **K-Math / K-Code / K-Sci-2** from the knowledge-gap plan, only if they are built by then. Report only.
  - **Never read by a pilot:** the sealed suite (any part; the look table allows only S1, S2 and C, and an extra look
    needs an amendment and lowers P(ship)), the DI, OHS-1/2/3, ejs-5, JevBench and LongBench.
- **Money and GO.**
  - Each paid launch needs the owner's GO and a numbered /goal step. ARC is not in the current goal, so the owner
    adds e.g. "C-ARC: architecture pilots".
  - The H100 rate is the measured all-in $4.09/h. Reads run on a Modal L4 ($0.80/h, plus 10%), or on the free Google
    L4 when it is idle.
  - The L4 read time is measured: C1's standard read of the 9 splits plus jagged plus OPI took 2,249 s, and the
    `_perm` read 1,531 s.
  - No relays and no resumes: a pilot that dies is rerun from scratch.
- **Adoption.** A passing component never enters C mid-round. It can join a later training round only through a new
  PREREG amendment, and the "DI-informed design" label is disclosed: the DI aggregate gaps are why reasoning was
  chosen.

### 2.1 Free steps first (no Modal)

| Step | What | Status | Decides |
|---|---|---|---|
| F1 | Brier decomposition of C1 on dev (Murphy, 10 bins) | **Done today:** yes/no Brier 0.1096 = REL 0.0009, RES 0.1407, UNC 0.25 (n 4,329); choice top-1 Brier 0.1344, REL 0.0021 (n 3,814) | Rejects 6 and 9 |
| F2 | C1 accuracy by option count on dev | **Done today:** 2-4 options 79.7 (n 2,527), 5-26 options 78.1 (n 1,054), 27+ options 45.1 (n 233; btzsc_empathetic 45.5, btzsc_manifesto 42.9; 4B-E 55.4 / 46.4) | Moves 7 to a free report |
| F3 | Forgetting check: base Qwen3.5-4B vs C1, one-pass, same letter readout, on K-Sci-2 (MMLU-Pro non-MMLU, 2,000 items) and K-Sci (SuperGPQA, 4 options) | Needs the knowledge-gap plan's step 1 dev build, then about 2-3 L4-hours ($0) | Triggers P3 if C1 < base by >= 2 pp with LB > 0 on either |
| F4 | `hc.py` shortlist plus knockout vs full list on `dev_hc` | About 1 L4-hour ($0), when the L4 is free | Report only |

### 2.2 P1: loop a middle layer group through the backbone (ETD-style); the only pilot to run now

- **Code changes (new files only):**
  - `arc/loop_block.py` adds one extra pass over one complete middle group of Qwen3.5-4B. Its layers are 8 groups of
    (3 Gated DeltaNet + 1 attention), and the pass uses **layers 12-15**, so k = 2, fixed and pre-registered, with no
    sweep.
  - The update after layer 15 is h ← h + a ⊙ (G(h + e) − h):
    - G is layers 12-15 re-run with the same position and mask arguments (captured by forward pre-hooks);
    - a is a per-channel gate, **initialised at 0**;
    - e is a loop-step embedding, initialised at 0.
  - At step 0 the model is therefore C1 exactly. The LoRA on layers 12-15 is shared across both passes. The new
    parameters (a few thousand) get their own learning rate (1e-3) through the patched `prism_x.param_groups()`.
  - Prefill-only with `use_cache=False`, so the DeltaNet recurrent state is recomputed per pass and never carried over.
    No halting.
  - Tests (CPU, plus the Modal smoke):
    - zero-init identity: max |logit difference| <= 1e-3 vs C1 on 48 rows;
    - every hook fires once per pass;
    - loop params are saved and reloaded, with 0 answer flips vs in-training reads;
    - the pins are unchanged;
    - C0 (loop off) reproduces a plain `train_decoder` run bit for bit on 6 steps.
- **Runs:**
  - C0 = C1 + 1,600 steps on the pilot mix.
  - LOOP = the same plus the loop.
  - Then reads: G standard and `_perm`, R, S and latency for both models, plus a reliance read of LOOP with the loop
    switched off (R and G standard only).
- **Cost** (H100 at the measured 2.72 s/step; I assume +15% for the extra 4/32 layers forward and backward):

  | Item | Hours | $ |
  |---|---|---|
  | Modal smoke (6 steps, zero-init and hook checks) | 0.1 H100 | 0.5 |
  | C0 training, 1,600 × 2.72 s + 0.2 h start-up | 1.41 H100 | 5.8 |
  | LOOP training, 1,600 × 3.13 s + 0.2 h | 1.59 H100 | 6.5 |
  | Reads, C0 and LOOP (about 1.2 L4-h each) + LOOP loop-off (about 0.6 L4-h) | 3.0 L4 | 2.6 |
  | **P1 total** | | **about $15.4 (cap $17)** |

- **Pre-registered go / no-go (LOOP vs C0, written to the look log before any read):**
  1. **Primary:** R confirm half, LOOP − C0 **>= +2.5 pp with paired 95% LB > 0**.
  2. **No harm, G confirm (9 splits):** point >= −0.5 pp and LB >= −1.5 pp.
  3. **Calibration:** yes/no Brier on G confirm not worse by more than 0.003.
  4. **Order and security:** permutation flips <= C0 + 1.0 pp; jagged ASR <= C0 + 3 pp; OPI ASR <= C0 + 1 pp.
  5. **Latency:** batch-1 p50 (`decoder_io.latency`, 150 rows, same GPU) <= C0 × 1.15.
  - Report only: the select half, per-source R (pg_numeric, pg_multihop), the loop-off reliance read, M and K-sets.
  - **GO** = 1-5 all pass. Then P1-rep runs.
  - **STOP** = 1 fails. Latent recurrence is closed for this cycle. No retry with other layers or k without a new
    owner decision, because a sweep is a forking path.
  - If 1 passes but 2-4 fail: no adoption. Write one diagnosis note; the owner decides.
- **P1-rep (only if GO):**
  - A new seed (20261005) for **both** C0 and LOOP, same mix and reads, about $15.
  - Adopt only if the pooled two-seed R confirm gain is >= +1.5 pp with LB > 0 and rules 2-5 hold again.
  - Security reads swing between runs (E 5.8% vs E_L4 19.2% jagged), so P1-rep also settles any rule-4 borderline.

### 2.3 P2: step-supervised loop (only if P1-rep passes; cap $15)

- **What:** CODI-style self-distillation with no bigger teacher.
  - The "teacher" is our own Qwen3.5-4B, reading a short trace it wrote itself in thinking mode, with a 512-token
    cap.
  - The student is LOOP without the trace. Its loop output at the answer position is pulled toward the teacher's
    hidden state there (L1 loss), on top of C1's loss.
- **Data:** the 6,381 unseen `pg_train` rows plus the proc_* rows. Traces come only from our 4B. Rows whose trace
  answer is wrong (gold check) are dropped. No GSM8K-Aug, because GPT-4 wrote it.
- **Cost:**
  - traces: about 3M tokens, 0.5-1 H100-h, $2-4;
  - training plus reads: about $9.
- **Go:** R confirm >= LOOP + 2.0 pp with LB > 0, plus rules 2-5. K-Math is report only.

### 2.4 P3: function-space replay (only if the free F3 forgetting check fires; cap $9)

- **What:** C0 plus the trainer's **existing** base-model anchor (`beta` 0.5 on `meta.anchor` breadth rows). This
  needs no new code. Generic-text replay as in the paper stays RESEARCH-LATER, because it needs a new licensed
  corpus and an owner ruling (FineWeb-Edu was flagged).
- **Cost:** about 1.6 H100-h for training (the anchor adds a base forward pass) plus reads, about $8.
- **Go:** K-Sci-2 or K-Sci recovers >= +1.5 pp vs C0 with LB > 0, plus rules 2-5.

### 2.5 Not piloted

These are not run, because our own tests or today's numbers already answer them: option-query head on the 4B, typed
heads, the small latent block, calibration RL or a Brier term, the error head, and halting.

## 3. Budget vs the money we have (Modal)

| Line | $ | Note |
|---|---|---|
| Modal available now | about 141 | given |
| C round 1 + smoke (A16) | −30.5 | committed; untouched |
| C round 2 (only if S1 passes, about 13%) | −60 held | released after S1 if round 2 does not run |
| Reserve | −25 | untouchable |
| **Free before S1** | **about 25.5** | |
| P1 (smoke, C0, LOOP, reads) | −15.4 (cap 17) | **fits before S1** and leaves round 2's $60 intact |
| Free after S1, if round 2 does not run (about 87%) | about 70 (25.5 − 15.4 + 60) | |
| P1-rep (only if P1 GO, about 20-25%) | −15 | after S1 |
| P2 (only if P1-rep passes) | −15 cap | after S1 |
| P3 (only if F3 fires; probability unknown) | −8 | after S1 |
| Worst case, all pilots | about 53 | the after-S1 pilots (about 38) fit in about 70, leaving about 32 above the reserve |
| **Expected ARC spend** | **about 25** | 15.4 + 0.22 × 30 + P(F3) × 8 |
| If round 2 runs (about 13%) | P1 only | the rest waits for the monthly credit reset |

- P1-rep is not run before S1. P1 + P1-rep ($30) before S1 would leave 141 − 30.5 − 30 − 25 = $55.5, under round 2's
  $57-60, so the recipe's trim rule would bite.
- Modal L4 reads can move to the free Google L4 (saves about $2.6 per pilot) once its C replay reads finish.

## 4. Honest projection: full ARC vs Jev, per axis

Full ARC means every component above working at the top of its evidence, one-pass, no thinking. The ranges are my
estimates from the two verifier reports and our ledger. They are not measurements.

| Axis | C1 now | Jev | Full ARC (range) | Why |
|---|---|---|---|---|
| **Decision Index** | 54.83 | 59.51 | **54.8-56.8** (central about 55.2) | Loop +0.2 to +0.9 only if it works (P about 0.2-0.25); typed heads 0-0.4; two-stage 0-0.2; replay 0-0.3; option heads 0 to +0.1; RL 0. The gap stays 2.7-4.7. **P(>= Jev) about 1%** |
| Knowledge area | 51.2 | 68.9 | 51.2-57.4 | Loops do not add facts (Ouro about 2 bits per parameter; ETD's NQ and TriviaQA scores flat) |
| GPQA (one pass) | 39.8 | 78.6 | 40-45 | Only thinking closes it (76.2 at a 32K-token budget); +5 is inside 1.4 SE at n = 196 |
| GSM8K | 56.7 | 79.9 | 57-72 | The top end needs step supervision (P2) |
| CRUXEval | 51.5 | 73.0 | 52-60 | No paper measures it; low confidence |
| MMLU | 82.5 | 92.0 | 82-84 | Facts |
| OHS-1 / OHS-2 accuracy (vs Jev) | −1.2 / −0.6 | 0 | about −1.2 to +0.5 / −0.6 to +1.0 | Still a statistical tie. ARC parts barely touch classification |
| ejs-5 (vs Jev) | −4.4 | 0 | −4.4 to −2.5 | Low confidence |
| Brier (OHS-1 yes/no) | 0.140 | 0.114 | 0.135-0.140 | Jev's lead is resolution (accuracy), not calibration |
| Hijack ASR | 0% | 99% | 0-5% with guards | We keep this win. Unguarded new parts raised jagged ASR to 30-35% on the 2B (J, O1) |
| Option-order flips | 2.4% | unknown | 2.4% (letters kept); 1-2.4% with option heads | Option heads read states computed over an ordered prompt, so they are not exactly order-free |
| Latency | DI median 242-262 ms on L4 (2 reads per choice) | 168 ms p50 via OpenRouter, network included (R_skeptic) | +5% to +15% | The loop adds 4 of 32 layers once; option heads block CUDA graphs |

- **Adding the knowledge-gap plan's opt-in auto mode** (DI 57.4, range 56.2-58.6): it overlaps with the loop on the
  same reasoning items, so the gains do not simply add. My combined estimate is 57.5-59.0, with P(>= Jev) about 5%.
- To win the DI, the knowledge area must reach about 74.6 with the other areas unchanged.

## 5. What to do first this week

1. **Keep round 1 first (A16, untouched).** The order is:
   mixer → A16.3 → G9 crowd on the L4 → counts-only decontamination → smoke ($0.5) → owner GO → round 1 ($30).
2. **Owner decisions (one message):**
   - (a) Accept the verdicts in section 1.
   - (b) Add a /goal step "C-ARC: P1 loop pilot, cap $17 before S1; P1-rep, P2 and P3 only after S1 and only on
     pass/trigger".
   - (c) Rule on item 10: keep "no thinking fallback", or keep the knowledge-gap plan's opt-in auto mode.
3. **CPU, about 1 agent-day, $0:**
   - write `arc/loop_block.py`, `arc/train_arc.py`, `arc/read_arc.py`, `arc/build_pilot_mix.py`, `modal_arc.py` and
     the tests in 2.2, including the pin-hash test;
   - build `arc_pilot_mix.jsonl` and run the dev group-overlap check;
   - write the go/no-go rules of 2.2 to `reports/arc_review/LOOKS_arc.jsonl` before any read.
4. **Modal smoke ($0.5), then on GO: P1 (about $15.4).** Run it on Modal, because the Google L4 is busy with the C
   replay reads until about Sunday 3 pm EDT and the quota is 1 GPU. Report the result and pause.
5. **Free, when the L4 is free:**
   - F3, the forgetting check, after the knowledge-gap plan's K-Sci/K-Sci-2 dev build;
   - F4, the `hc.py` report.

## Sources

- In-house:
  - `opendecide-data/lean/logs/budget_ledger.md`: rows M1-M6, X4-X19 and P1-P3; the 4B ship gate.
  - `C_TRAIN_RECIPE.md` v4: sections 4, 6.1-6.3 and 8.
  - `PREREG_FINAL.md`: A16, A16.1 and A16.2.
  - C1 dev reads in `preds_<split>/q35_4b_main500k*.jsonl`; today's analysis script is in the session scratchpad
    (`c1_dev_breakdown.py`).
- Verifier reports (they hold every paper URL and number cited here):
  - `reports/arc_review/V_latent.md`: LRT arXiv 2609.01117, ReLIT 2608.08113, ETD 2510.07358, Ouro 2510.25741,
    LOTUS 2606.31779, CODI 2502.21074, continuous CoT 2607.16972.
  - `reports/arc_review/V_other.md`: replay arXiv 2603.04964, RLCR 2507.16806, Set-LLM 2505.15433, CORN 2111.08851,
    TRACT 2503.04381, RAG-MCP 2505.03275; TypeSafe docs.
- Model card: Qwen3.5-4B, https://huggingface.co/Qwen/Qwen3.5-4B (GPQA Diamond 76.2 with thinking).
- `reports/knowledge_gap/PLAN_knowledge_gap.md`: auto mode, dev sets, DI arithmetic.
