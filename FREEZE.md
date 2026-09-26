# OpenDecide: frozen architecture and plan for the $30 account (26 Sep 2026)

This file closes the $10 round. What is frozen (keep it as is), what the round found, and the exact plan for the next
Modal account. Details: `HANDOFF.md`, `opendecide-data/lean/logs/budget_ledger.md`, the published report
(https://claude.ai/artifact/32Jd6eZEaSqdUgLxqduFwc) and the audit and plan outputs summarised below.

## 1. What the $10 round found (all measured)

| # | Finding | Evidence |
|---|---|---|
| 1 | **On new corpora Jev is clearly ahead.** On OHS-1 core (1,847 held-out items from 17 public sources, pre-registered, commit 273e76b), Jev scores 81.7 and v0.10 scores 76.1: −5.5 pp, CI [−7.3, −3.8]. The open half gives −5.9 and the sealed half −5.2. | `results_ohs/results_{all,A,S}.json` |
| 2 | Our training barely moves new-corpus accuracy (+0.3 over untrained Qwen3.5-4B), but it cuts negation contradictions from 0.31 to 0.12 (Jev 0.097). | same |
| 3 | Jev's biggest leads: HateCheck 98 vs 81, trademark distinctiveness 78 vs 52, hearsay 85 vs 67, ScoNe negation 85 vs 74, GoEmotions 70 vs 61. We lead on contract tasks and tie on 100-way LEDGAR (98.3). | per-task table |
| 4 | **2B student** (distilled from v0.10, 12k rows, $1.6): JevBench half-A score 74.86 vs Jev 72.51, the same as v0.10. It reaches this with better calibration, 10 ms latency and lower cost, while its accuracy is 95 vs 103. On OHS it gets 66.4 (−15 pp), and it collapses above 26 options (LEDGAR 23%), because the pilot data had at most 9. The 0.8B scores 83/118 and 56.2. | `bench/runs/q35_2b_kd_A_g`, OHS |
| 5 | Weight interpolation or extrapolation (LoRA scale 0.7–1.3) and option-order averaging leave unseen-domain dev flat. No free lunch there. | `preds_dev*/q35_4b_v10_a*` |
| 6 | Report errors were found and fixed. A helper script undercounted Jev on long, multi-question and served requests (true leads are +4.0, +2.5 and +5.3, not +38, +22 and +18). Half B had been seen 4 times. The debate audit is third-party, attacks in one direction only, and our balanced clean accuracy there is 88.6 vs 94.2. | report v3 |
| 7 | Data bugs, from the audit: every intent label always had the same option set (the answer leaks from the set); DBpedia rows were 100% "Company"; planted claims were 68/32 wrong/right (the cause of the echo gap); the "claim" wording was almost always negation; the negation templates were narrow (the attributed-belief family had been removed); only about 15 label sets; forgetting across 4 chained stages. | audit findings |
| 8 | Competition: decider-4b v2 (Mapika; the same Qwen3.5-4B base, Apache-2.0) is #1 on the official JevBench board at 64.13, above Jev's 63.29. The Decision Index (40 third-party benchmarks) ranks Jev #1. | JevBench README, decider README |
| 9 | Engineering: a 255-option label head works (4B at 98.3% zero-shot on 100-way LEDGAR). CUDA graphs are exact (0.00 difference) for 4B, 2B and 0.8B. Graphs need one memory pool per graph and a bounded batch × length. | `decoder_io.GraphRunner`, `Readout.wide` |

**Bottom line.** The architecture is fine. The gap to Jev on new data comes from training breadth: our data was dominated by
intent classification with leaky option sets, and by JevBench-like families. The next round changes the data and the loss, not the model.

## 2. Frozen architecture (do not change in the next round)

- **One model, no cascade:** Qwen/Qwen3.5-4B (24 Gated DeltaNet + 8 attention layers), LoRA r16 on every projection (`QWEN35_TARGETS`), merged for serving. The 2B (Qwen/Qwen3.5-2B) is the distillation target once the 4B passes the gates.
- **Readout:** one prefill pass. Answer = softmax over option-label logits, with labels A–Z and then single-token two-letter codes (up to 255 options, `decoder_io.WIDE`). Grouped tokens, fp32 readout. No generation.
- **Prompt:** the cygnet layout, rendered by ONE function for training, evaluation, JevBench and serving. It always shows option descriptions and criteria. Fix `card_defs` for labels that contain ": ".
- **Loss:** cross-entropy (or soft targets) + consistency + KL anchor to the frozen base (beta 1) + optional distillation (`kd`, `meta.teacher`).
- **Serving:** CUDA graphs per 64-token bucket (batch 1; small batches only while batch × length ≤ 8,192), captured at start-up, with a self-check against eager. One temperature path, identical in serving and benchmarks.
- **Robust mode** (option-order averaging + leverage-bounded decoding): optional. Fix the views first (keep "none/other" last, use a cyclic shift instead of reversal, never permute ordinal options).

## 3. Plan for the $30 account (in order; every paid step has a go/no-go check)

**Step 0 ($0): move and verify.**
- Log in to the new profile.
- `modal volume put opendecide backups/modal_models/<name> /models/<name>` for q35_4b_v10, q35_2b_kd and q35_08b_kd (all six adapters are backed up locally).
- Recreate the `opendecide-keys` secret with a NEW OpenRouter key, and rotate the old one.
- Run `modal billing report` and start a new section in the budget ledger.

**Step 1 ($0, CPU): fix the data and build the v0.11 mix** (one stage, fixed quotas, no chaining). All sources must pass `decontam.py`, and must not be any OHS-1 source dataset (LegalBench, LexGLUE, ScoNe, This-is-not-a-dataset, HateCheck, PubMedQA, VitaminC, GoEmotions, SGD, arXiv 2026).

| Share | Block | What |
|---|---|---|
| 30% | Label-set breadth (the main lever) | Hundreds of tasks from `MoritzLaurer/synthetic_zeroshot_mixtral_v0.1` and `tasksource/zero-shot-label-nli`, split by task. Official or one-line label descriptions; 25% of rows with labels renamed to codes; 3–12 options. |
| 10% | Wide options | 10–26 and 27–120 options, random order, with abstain options kept last. |
| 15% | Reasoning and judge | Existing judge, LLM-authored, procedural and ProofWriter/FLD/LogiQA/MuSR rows, class-balanced. |
| 12% | Negation and paraphrase | About 300 templates in 12+ families, including attributed belief. Eval wordings are excluded. The word "claim" appears equally in affirmative and negated questions. Complement and equivalence pairs. |
| 10% | Planted claims | 45% pushing the wrong answer, 45% agreeing with gold, 10% neutral. Every attacked row gets a flipped-claim twin, and the clean copy is the teacher (stop-gradient). |
| 8% | Debates | Class-balanced (kept vs deleted). |
| 15% | Original classification | Option sets drawn at random per row (never tied to the gold). DBpedia fixed (sampled per class). |

**Step 2 ($0, CPU): loss and code** (judge plan S6).
- Map log-probs to canonical option order.
- `inv` relation: KL(stopgrad(clean) ‖ attacked).
- Symmetric JS for equivalence, and consistency for choice rows via option-order twins.
- lam 1.0 with a ramp.
- Unit tests on synthetic logits must pass before any paid step.

**Step 3 ($0, CPU): selection-only dev sets** (never OHS). All decontaminated.
- `dev_nc`: BTZSC clean subsets, 21–56-way. This is the gate.
- `dev_negwords`: a held-out template family.
- `dev_claims`: echo and targeted claims.
- `dev_none`: abstain rows.
- `dev_k`: 78- and 151-way rows.

**Step 4 (~$9–10, H100): train v0.11-4B from the base model**, about 0.6 epoch of the v0.11 mix (~2,200 steps at 3.3–4 s). It writes dev predictions in the same container.
- **Go if:** `dev_nc` improves by 2 pp or more over v0.10, devzs/devzs2/devp_card do not drop by more than 0.5 pp pooled, and pg_dev and debate_dev hold.
- **Otherwise:** keep v0.10 and use Step 6's budget for a second data iteration.

**Step 5 (~$1.5): confirm once.**
- OHS-1 sealed half (Jev's two runs already exist, so no new Jev cost).
- JevBench half A (development set) with `--graphs`.
- Report with the pre-registered scorer: `score_ohs.py --half S`.

**Step 6 (~$5): the 2B.** Distill v0.11 into Qwen3.5-2B on the full v0.11 mix, including wide options (kd 0.5, LoRA r32, lr 1e-4, 1 epoch of ~25k rows).
- **Gate:** within 3 pp of the 4B on `dev_nc`.
- Then JevBench half A and OHS-S.
- This is the "2B that leads" candidate: on JevBench it already matched the 4B's overall score in the pilot.

**Step 7 (~$3): PRISM pilot, privilege separation.** Train the 2B (or 0.8B first, ~$1.2) with `writeblock.py`: beta = 0 and g = 0 on untrusted spans for half of the Gated DeltaNet heads, from the start of training. Measure planted-claim success in both directions and injection attacks WITHOUT leverage-bounded decoding, against the same model trained without the block. This is the first architecture-level contribution beyond the recipe.

**Buffer:** keep $5 or more unspent until the end (billing lags by about an hour).

## 4. Decisions only you can make
1. **Decision Index** (40 third-party benchmarks, Jev #1). It needs the gated HLE dataset: request access at https://huggingface.co/datasets/cais/hle with the Hugging Face account whose token is in the Modal secret. Alternatively, approve a build that skips HLE (the permission system blocked my modified build).
2. **Official JevBench submission** (sealed tiers, run by the maintainers at no cost to us). This means publishing the weights on Hugging Face and opening a GitHub issue. Do it only if v0.11 passes its gates.
3. **Running decider-4b v2** (their open-source package) on OHS-1 for a head-to-head against the #1 entry.
4. **Rotate the OpenRouter key.**
