# R_measure: knowledge gap, honest ceiling and clean dev sets

Researcher: measure. Date: 3 Oct 2026. Web only. No local quarantined files were opened.

## 0. Bottom line (short)

1. **A 4B model can only match Jev's knowledge numbers if it is allowed to think.** Qwen3.5-4B (our base) scores **76.2 on GPQA Diamond in thinking mode** (Jev 78.6). Read in one pass with no chain-of-thought, a 4B is roughly where C1 is now (about 40).
2. **GSM8K, CLadder and CRUXEval are the gaps we can close, and maybe beat Jev on.** They are math, logic or code, and a short reasoning or program-of-thought route fixes most of the error there. CoT gain on GSM8K is **+66 points** for Llama-3.1-8B (20.1 → 86.4, Sprague et al.).
3. **MMLU (92.0) is the gap we can't fully close.** It is fact-storage-bound. Our best anchor is Qwen3.5-4B thinking at MMLU-Redux 88.8. MMLU itself has about 6.5% bad labels, so Jev is near the ceiling.
4. **The numbers don't add up (measurement flag).** DI areas are **equal-weight means** (DI README). Knowledge gap 17.7 × 14 benchmarks = **248 benchmark-points**. The six listed gaps sum to only **106 (43%)**. About **142 points (≈2.0 index points)** sit in the other 8 Knowledge benchmarks: ARC-E/C, WinoGrande, HellaSwag, MuSR, SATA-Bench, SimpleBench and HLE. Check these first. **SATA-Bench** (select-all, case exact match) and "unanswered = wrong" items are prime suspects for a one-letter model.
5. **Index arithmetic.** 1 point on one Knowledge benchmark = 1/14 area point = **0.0143 index points**. Closing all six listed gaps fully = **+1.51 index**. Closing the whole Knowledge gap = **+3.54 index**, which is 76% of the total 4.68 gap.

## 1. Best published 3-9B scores (verified this session)

| Benchmark (Jev / C1) | Best published small-model score | Mode | Source |
|---|---|---|---|
| **GPQA Diamond** (78.6 / 39.8) | **Qwen3.5-4B 76.2**; Qwen3.5-9B 81.7 | thinking (Qwen3.5 "thinking by default", compared vs thinking models) | [HF Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) |
| | Qwen3-4B-Thinking-2507 65.8 | thinking, 32K-token budget recommended | [HF card](https://huggingface.co/Qwen/Qwen3-4B-Thinking-2507) |
| | Qwen3-4B-Instruct-2507 62.0 | non-thinking (but writes reasoning text) | [HF card](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) |
| | Gemma 4 E4B 58.6 | mode not stated in snippet | [benchlm](https://benchlm.ai/models/gemma-4-e4b), [Gemma 4 card](https://ai.google.dev/gemma/docs/core/model_card_4) |
| | Qwen3-4B (orig.) 55.9 think / **41.7 non-think** | | [Qwen3 tech report](https://arxiv.org/abs/2505.09388), Tables 17-18 |
| | Qwen3-4B-Base 36.87 | 5-shot CoT (GPQA main) | Qwen3 report |
| **MMLU** (92.0 / 82.5) | Qwen3.5-4B MMLU-Redux **88.8** (9B: 91.1); MMLU-Pro 79.1 | thinking | HF Qwen3.5-4B |
| | Qwen3-4B-Base MMLU 72.99; Qwen2.5-7B-Base 74.16 | 5-shot, no CoT | Qwen3 report |
| | Llama-3.1-8B MMLU 67.5 direct vs 72.6 CoT (zero-shot) | direct vs CoT | [Sprague et al. 2409.12183](https://arxiv.org/abs/2409.12183) |
| **GSM8K** (79.9 / 56.7, DI = 4/10-choice avg) | Qwen3-4B-Base **87.79** (free-form) | 4-shot CoT | Qwen3 report |
| | Llama-3.1-8B **20.1 direct → 86.4 CoT**; Qwen2-7B 21.4 → 87.6 | zero-shot free-form | Sprague et al. |
| | Qwen3.5-4B GSM8K: **unknown** (not reported) | | |
| **CRUXEval** (73.0 / 51.5, DI = 570 items) | CodeReasoner-7B **CRUX-O 85.6 / CRUX-I 86.3** (GPT-4o 90.5 / 80.6) | CoT; SFT from a 32B teacher + GRPO | [2507.17548](https://arxiv.org/abs/2507.17548) |
| | Qwen2.5-Coder-7B-Instruct O 65.9 / I 65.8 | CoT | [Qwen2.5-Coder report](https://arxiv.org/abs/2409.12186) |
| | Qwen3-4B-Base CRUX-O 55.00 | 1-shot, no CoT | Qwen3 report |
| **CLadder** (72.6 / 65.1) | 3-9B: **unknown**. Llama-3-8B zero-shot **51.2** (≈ chance, 3K stratified) | direct | [2512.13725](https://arxiv.org/abs/2512.13725) |
| | GPT-4 + CausalCoT 70.40; Qwen3-32B thinking 84.16 (debate 89.41); R1-Distill-Qwen-32B 78.03 | | [CLadder 2312.04350](https://arxiv.org/abs/2312.04350), [CRAwDAD 2511.22854](https://arxiv.org/abs/2511.22854) |
| **ChessBench** (17.2 / 11.7, best-move, ties ok) | LLM 3-9B: **unknown**. Specialized supervised transformers (no search): **action accuracy 56.7-63.4%** (ablations, 1M games); 270M puzzles 95.4%; GPT-3.5-turbo-instruct puzzles 66.5% | | [ChessBench 2402.04494](https://arxiv.org/abs/2402.04494) |

Key generic fact: across 100+ papers, CoT gains are **+14.2 symbolic, +12.3 math, +6.9 logic**, versus about **+0.7** on everything else (56.8 vs 56.1) ([Sprague et al.](https://arxiv.org/abs/2409.12183)). On MMLU, direct answering ≈ CoT except on questions with "=".

## 2. Honest ceiling for a 4B system (Qwen3.5-4B + LoRA)

Three regimes:

- **(A) One-pass letter**: today's product, about 20-50 ms.
- **(B) Short reasoning / program-of-thought**: ≤256-512 tokens, routed only to math, code and causal items.
- **(C) Full thinking**: 2K-30K tokens.

Latency is my arithmetic, not measured. Decode speed is bounded by bandwidth / weights: L4 300 GB/s ÷ ~8 GB bf16 ≈ ≤35 tok/s, so 256 tokens ≈ 7 s on L4 and ≈1.5-2 s on H100. 5K thinking tokens ≈ 2.5 min on L4.

| Bench | Jev | C1 | (A) one-pass realistic | (B) short route | (C) thinking | Can we match/beat? |
|---|---|---|---|---|---|---|
| GPQA-D | 78.6 | 39.8 | 42-48 (low conf) | 50-58 | **70-76** (anchor 76.2) | Match only with (C); 198 items → SE ≈ ±3.5 pts |
| MMLU (subject-macro) | 92.0 | 82.5 | 83-85 | 85-87 (route STEM/"=" subjects) | 87-89 (anchor Redux 88.8) | **No**: 3-6 pt gap likely stays; ~6.49% label errors cap all systems near ~93 ([MMLU-Redux](https://arxiv.org/abs/2406.04127)) |
| GSM8K-MC | 79.9 | 56.7 | 58-65 | **85-92** (anchor 87.8 free-form CoT; MC is easier) | 90-95 (unknown, est.) | **Yes, high confidence** with (B) |
| CRUXEval | 73.0 | 51.5 | 52-58 (anchor base 55.0) | 62-72 | 75-85 (anchor 85.6 but teacher-made) | Yes with (B)/(C). Python execution tool ≈ near-100 on output-prediction, but that is an owner policy call |
| CLadder | 72.6 | 65.1 | 68-75 if trained on fresh generator data (low-med conf) | **85-95** (parse → compute estimand; anchor Qwen3-32B think 84.2) | 85+ | Yes, likely with (B); maybe with (A) |
| ChessBench | 17.2 | 11.7 | 20-35 if LoRA on Stockfish-labelled FENs (guess, low conf) | same (CoT does not help much) | unknown | Plausible via (A) data; engine tool ≈ 95+ but is a policy call |

Index value if (A)+(B) hit the midpoints: GPQA +12, MMLU +3, GSM +32, CRUX +15, CLadder +20, Chess +12 ≈ +94 benchmark-points ≈ **+6.7 Knowledge area ≈ +1.34 index**. This is not enough alone; the missing 142 points (section 0, item 4) matter more.

**Unknowns:**

- Qwen3.5-4B non-thinking scores (not published; one search snippet claimed 76.2 non-thinking, but the HF card does not support it).
- Any 3-9B score on CLadder and on ChessBench best-move.
- How DI builds the GSM8K distractors and the CRUXEval 570-item subset.
- Whether our LoRA damages Qwen3.5's own thinking. Test (C) with the LoRA off and with it on.

## 3. Clean dev sets: no DI overlap, licence checked (HF API, 3 Oct 2026)

DI's Knowledge test items are: MMLU test (14,042), GPQA Diamond (198), **ARC-Easy test (2,376), ARC-Challenge test (1,172)**, WinoGrande dev (1,267), HellaSwag val (10,042), GSM8K test (1,319), ChessBench (5,000 seeded), MuSR (756), SATA-Bench (1,650), SimpleBench (10), CRUXEval (570 of 800), CLadder (5,000 of 10,112), HLE (513) ([DI README](https://github.com/flaviusburca/decision-index)). **So ARC test splits are off-limits. Use ARC train/dev only.**

### Use these

| Proxy for | Dev set | Size | Licence | Why clean |
|---|---|---|---|---|
| MMLU | **MMLU validation + dev** (cais/mmlu) | 1,531 + 285 | MIT | same 57 subjects, disjoint from test; score subject-macro |
| MMLU/ARC | **ARC-Challenge + ARC-Easy train+dev** (allenai/ai2_arc) | 1,119+299 / 2,251+570 | CC-BY-SA-4.0 | DI uses only the test splits |
| GPQA / hard STEM | **SuperGPQA** (m-a-p/SuperGPQA), stratified ~2,000 (hard/middle, sci) | 26,529 total, 10 options | ODC-BY | independent build; 4B anchors: 52.9 (Qwen3.5-4B think), 47.8, 42.8, base 28.4 |
| GPQA / hard STEM | **MMLU-Pro, non-MMLU sources only** (stemez/theoremQA/scibench) | 5,222 of 12,032 | MIT | must DROP the 6,810 "ori_mmlu" items (taken from MMLU test) |
| GPQA (secondary) | **GPQA extended minus Diamond** (Idavidrein/gpqa) | 546 − 198 = 348 | CC-BY-4.0, gated | disjoint IDs, same style; noisier labels; never post items publicly |
| GSM8K-MC | **GSM8K train, re-numbered**: re-run its `<<calc>>` annotations with new numbers (program-labelled), build 4- and 10-choice tracks with program distractors | up to 7,473 | MIT | train split ≠ test; new numbers avoid base-model memorization |
| CRUXEval | **Fresh CRUXEval-style functions** (Claude-authored, ≤13 lines, stdlib, deterministic), I and O tasks, labels by executing Python | 1,000-2,000 | ours | dedupe by AST hash vs all 800 CRUXEval |
| CLadder | **Regenerate with causalNLP/cladder generator** (new seeds) + hold out ≥1 story template for a generalization slice | 3,000-5,000 | MIT | dedupe (story, graph, query, numbers) vs all 10,112 released |
| ChessBench | **ChessBench train split** or a different-month **Lichess DB** dump, labelled by Stockfish 16 @50 ms (same oracle as ChessBench) | 5,000 | data CC-BY-4.0 / CC0 parts; code Apache-2.0 | dedupe FEN (board+side+castling+ep) vs all ChessBench test files |

Secondary (eval-only, check before use): LiveCodeBench `execution-v2` (licence tag just "cc", variant unstated), QASC (CC-BY-4.0), MedMCQA (Apache-2.0), CommonsenseQA (MIT), TheoremQA (MIT, already inside MMLU-Pro).

### Do NOT use

| Set | Reason |
|---|---|
| ARC-Challenge/Easy **test** | literally DI items |
| MMLU-Redux (CC-BY-4.0) | re-annotated subset of MMLU test |
| MMLU-Pro `ori_mmlu*`, MMMLU | derived from or translated from MMLU test |
| GSM-Plus (CC-BY-SA-4.0), GSM-Hard (MIT), GSM-Symbolic (**CC-BY-NC-ND-4.0**), MGSM | all perturbations or translations of **GSM8K test** |
| CRUXEval-X | translations of the same 800 CRUXEval functions; no licence on HF |
| SciQ | **CC-BY-NC-3.0** (non-commercial) |
| OpenBookQA, PIQA, TriviaQA | HF licence "unknown"; hold until confirmed |
| HellaSwag val, WinoGrande dev, MuSR | in DI. Train splits are OK (HellaSwag MIT per repo; WinoGrande licence not on HF) |

### Overlap check without touching quarantine

Dedupe candidates against the **full public source test sets** (MMLU test, GPQA Diamond, GSM8K test, all 800 CRUXEval, all 10,112 CLadder, ChessBench test FENs, ARC test, HellaSwag val, WinoGrande dev). These are a superset of DI's items, so DI's prepared files are never opened. Use:

- normalized exact hash;
- 13-gram overlap;
- near-duplicate embedding check (cos ≥ 0.92).

Log the counts dropped.

### Power

- **GPQA Diamond**: n = 198, so one item = 0.505 points and SE ≈ 3.5 points. "Matched Jev on GPQA" means nothing below about ±7 points.
- **Dev A/B**: paired test, SE ≈ sqrt(d/n). With discordance d ≈ 0.15, n = 2,000 per family gives SE ≈ 0.9 points. Aim for **≥1,500-2,000 items per family**.
- **Contamination**: Qwen3.5 has likely seen ARC, MMLU val and GSM8K train. Trust these for relative A/B only. The generated sets (re-numbered GSM, new CRUX, new CLadder, new chess) are the clean absolute measures.

## Sources

- DI README: https://github.com/flaviusburca/decision-index
- Qwen3.5-4B: https://huggingface.co/Qwen/Qwen3.5-4B
- Qwen3-4B-Instruct-2507: https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507
- Qwen3-4B-Thinking-2507: https://huggingface.co/Qwen/Qwen3-4B-Thinking-2507
- Qwen3 tech report: https://arxiv.org/abs/2505.09388
- To CoT or not to CoT: https://arxiv.org/abs/2409.12183
- CodeReasoner: https://arxiv.org/abs/2507.17548
- Qwen2.5-Coder: https://arxiv.org/abs/2409.12186
- CLadder: https://arxiv.org/abs/2312.04350 and https://github.com/causalNLP/cladder (MIT)
- CRAwDAD: https://arxiv.org/abs/2511.22854
- Quantized causal reasoning (Llama-3-8B CLadder): https://arxiv.org/abs/2512.13725
- ChessBench: https://arxiv.org/abs/2402.04494 and https://github.com/google-deepmind/searchless_chess
- MMLU-Redux: https://arxiv.org/abs/2406.04127
- MMLU-Pro: https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro
- Gemma 4 E4B: https://benchlm.ai/models/gemma-4-e4b
- Licences: Hugging Face API `huggingface.co/api/datasets/<id>`, 3 Oct 2026
