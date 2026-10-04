# OpenDecide-4B Final Architecture (v1, 4 Oct 2026)

It combines 3 things:
1. **Fine-tuning:** round 1, broad skill data.
2. **Codex's ARC design, improved:** the parts that held up are kept, and the parts that failed in our own tests are
   replaced.
3. **Optimized thinking:** a fast think mode.

Status tags:
- **PROVEN:** our own tests show it works.
- **PAPERS:** published evidence on the same or very close models.
- **PILOT:** ships only if a pass rule, written down before the run, holds.

## 1. Model (one model)
- **Backbone:** Qwen3.5-4B + our LoRA (r16), initialised from C1. [PROVEN]
- **Prompt layout:** the trusted rules, question and options are kept separate from the untrusted text, and the
  question is repeated after the text. [PROVEN: hijack 0% vs Jev 99%]
- **Readout:** one pass reads the letter probabilities. Choice questions are read twice (given order and reversed);
  yes/no once. [PROVEN: beat option-query heads on the 4B]
- **Calibration:** one temperature per question type, fitted on the served pipeline. [PROVEN method]
- **Ordinal (rating) questions:** an expected-level training term (A4). [PAPERS]

## 2. Fine-tuning (round 1, ~$30)
- **Data:** 150K rows, of which 60% replay C1's data and 40% are new:
  - 13 skill families, labelled by programs;
  - 14 licensed public datasets;
  - commit decisions from other repos.
- **Variety:** 300+ domain packs and 400 format styles. Some styles and samplers are held out of training.
- **Training signals:** twin questions where one change flips the answer, plus consistency and injection-invariance
  losses.
- **Label checks:** every label is re-derived by a second, independent solver (100% agreement required), then blind
  reads and shortcut tests.
- **Anchor:** training stays close to C1 only where C1 is confident and right.
- **Ship gate:** at least +1 pt over C1 on the sealed new-domains test, with the lower bound above 0, and no loss on
  security, consistency or calibration.

## 3. Inference: two speeds, one model
- **Fast path** (default, ~95% of questions): one pass, ~20-50 ms on an H100.
- **Router** (from Codex's halting gate) [PILOT]:
  - It sends a question to thinking only when the fast pass is unsure AND the question looks like knowledge, math
    or code.
  - It is learned on clean practice sets.
- **Fast think** (same 4B, LoRA off, thinking on) [PAPERS, PILOT]:
  - **Math:** short step-by-step, at most 300 tokens, 4 parallel tries, then a vote.
  - **Code and science:** thinking with a token cap, plus early exit when confident (DEER).
  - **Optional:** train it to think shorter on our own 4B's shortest correct answers.
- **Deep think** (opt-in, async): long thinking for the hardest science, 15-40 s.

## 4. Serving
- H100 with vLLM or SGLang: CUDA graphs, batching, and a shared-context prefix.
- **Think path:** the free DFlash draft model for Qwen3.5-4B (3-4x faster, same answers) and FP8 (at most a 1 pt
  loss). [PAPERS; speed test pending]

## 5. Optional pilot from Codex's design [PILOT]
- **Looped middle layers:** re-run 4 middle layers once, for extra reasoning.
- **Cost:** ~$15.
- **Pass rule:** at least +2.5 pts on reasoning dev sets, and no loss anywhere else.
- **Chance it passes:** about 20-25%.

## 6. Rejected (tested or no gain)
- **Option-query heads:** about 0 gain on the 4B.
- **Latent loop over saved states:** on the 2B, accuracy fell 0.7 pts and hijack rose to 30%.
- **Separate typed heads:** they do the same maths as the current training.
- **Calibration RL:** there is little calibration error left to fix.
- **"No thinking fallback":** thinking is the biggest proven gain.
- **Fast-chip providers:** they cannot host our model.

## 7. Expected vs Jev (estimates)
| Area | Ours (estimate) | Jev |
|---|---|---|
| Speed | ~0.13 s average with 5% routed; fast path 20-50 ms | ~0.2 s |
| Math (GSM8K) | ~75-86, in 0.25-0.8 s | 80 |
| Code reasoning | ~70-73, in 0.7-2 s | 73 |
| GPQA | ~55-62 in 2.5-6 s; ~76 in deep mode | 79 |
| MMLU | ~85 (model size limits it) | 92 |
| Decision Index | ~57.5-59 | 59.5 |

- **OHS-3 / new domains:** about a tie, with about a 1 in 3 chance to match or beat Jev.
- **Hijack, cost, consistency and JevBench:** we beat Jev.

## 8. Build order (~$55-65; Modal has $141; keep a $25 reserve)
1. Round 1 fine-tune and gate (~$30).
2. H100 speed proof (~$5-8).
3. FP8 check (~$4).
4. Router, short think and early exit (~$1-8).
5. Concise-thinking training (~$10-15).
6. Looped-layer pilot (~$15, optional).

After that: OHS-3 once, as the final test vs Jev. Round 2 (~$60) runs only if round 1 clearly wins.

**Sources:**
- reports/knowledge_gap/PLAN_knowledge_gap.md
- reports/arc_review/ARC_PILOT_PLAN.md
- reports/fast_think/FAST_THINK_PLAN.md
- opendecide-data/lean/c_spec/ (C_DATA_SPEC v4, C_TRAIN_RECIPE v4)
