# R_tools: can tools close the Knowledge gap to Jev?

Researcher: tools. Date: 3 Oct 2026. Web research only. No Modal, GPU or paid calls. No held-out items opened.

## TL;DR (simple)

1. **Yes, tools can close the Knowledge gap, but most of the gain comes from exact solvers, not from making the model smarter.** Four of the six Knowledge benchmarks can be computed exactly or near-exactly by a program:
   - CRUXEval: run the code.
   - ChessBench: run a chess engine.
   - GSM8K: the 4B writes a short Python program and we run it.
   - CLadder: the 4B parses the question and a causal solver computes the answer.
2. **Central estimate (all four routes):** Knowledge goes from 51.2 to about 79.5 (Jev 68.9), and the index goes from 54.8 to about 60.5 (Jev 59.5). Without the chess engine, Knowledge is about 67.3 and the index about 58.1. Adding a chord tool for POP909 (Arts area) could add about 1.5 more index points.
3. **Speed:**
   - The code executor and chess engine are fast (ms to about 300 ms).
   - The GSM8K program route is slow: about 3-5 s on an L4 in bf16 (about 1 s on an H100). Use it only when the one-pass answer is unsure.
4. **Fairness is the big catch.** Jev's own scores (CRUXEval 73.0, ChessBench 17.2) suggest it does **not** use an executor or chess engine (my inference: either tool would give it about 95-100). So "C1 + tools beats Jev" is not a like-for-like claim. Leaderboards report with-tools and without-tools results separately. **We must always show two rows: pure 4B, and 4B + tools (disclosed).**
5. **What tools do not fix:** GPQA (39.8 vs 78.6) and MMLU (82.5 vs 92.0). The knowledge is already in the weights: Qwen3.5-4B in thinking mode gets 76.2 on GPQA Diamond. That gap needs a think route or self-distillation, not a tool (see the other R_ reports).

## 1. How the Decision Index scores this (facts)

- **Index arithmetic.** Index = mean of 5 equal areas. Knowledge & Reasoning = mean of 6 benchmarks: MMLU, GPQA Diamond, GSM8K, ChessBench, CRUXEval, CLadder. So **+1 point on one Knowledge benchmark = +0.167 Knowledge = +0.033 index** ([README](https://github.com/flaviusburca/decision-index)).
  - Check: C1 Knowledge = (82.5+39.8+56.7+11.7+51.5+65.1)/6 = 51.2. Jev = 68.9.
- **Item formats** (from the public builder code, not from items; [adapters_selection.py](https://github.com/flaviusburca/decision-index/blob/main/decision_index/suite/build/adapters_selection.py), [adapters_scored.py](https://github.com/flaviusburca/decision-index/blob/main/decision_index/suite/build/adapters_scored.py)):
  - **GSM8K.** State is the question text. Options are 4 or 10 numbers. Distractors are gold ±1/2/5/10, ×2, ×10 and //2. Gold is checked by exact numeric match.
  - **CRUXEval (570 items).** State is `code` plus `input`. Options are Python literals: the gold output plus up to 9 wrong outputs from codellama-7b.
  - **ChessBench (5,000).** State is a FEN. Options are all legal moves (2-255). Gold is the best Stockfish-16 action value, with exact ties accepted.
  - **CLadder (5,000).** Text is background + given info + question. Answer is yes/no.
  - **POP909-CL (2,000).** State is the notes in a window of ±4 beats. Options are about 120 chord pitch-class sets plus NoChord and Other.
- **Rules that matter for tools** ([README "Rules"](https://github.com/flaviusburca/decision-index), [docs/engines.md](https://github.com/flaviusburca/decision-index/blob/main/docs/engines.md)):
  - "No prompt tuning … Per-benchmark prompts, few-shot examples or label-aware tricks are not part of the benchmark."
  - "Do not truncate, do not drop options, do not adapt the prompt per benchmark; refuse instead."
  - Every option needs a probability. Unanswered counts as wrong.
  - Submissions must record engine provenance. There is **no explicit rule on tools** (unknown whether the lab would accept them).
- **Caution:** the GSM8K and CRUXEval states carry a field `task: "GSM8K deterministic …"` / `"CRUXEval output selection"`. A router must **ignore** benchmark-name fields. Keying on them is a per-benchmark trick.
- **Caution:** the GSM8K distractor recipe puts gold at the centre of an arithmetic pattern. Our own training and dev data must **not** copy this recipe, or the model can learn an artifact.

## 2. Evidence per route (3-8B models, with numbers)

### 2a. CRUXEval: code execution (exact)
- **Why execution is exact.** CRUXEval items were filtered to be:
  - no imports;
  - deterministic (no random, no set-ordering);
  - no side effects;
  - 75-300 chars;
  - finish in under 2 s.
  
  Gold is the result of running the function ([CRUXEval paper §3.2](https://arxiv.org/pdf/2401.03065)). A sandboxed `f(input)` plus a literal-equality match to the options should therefore give **about 99-100%**. That is an estimate; the exact figure is unknown until measured on our own generated functions.
- **No-tool comparison:**
  - Qwen3-4B-Base CRUX-O: 55.0 ([Qwen3 report, Table 7](https://arxiv.org/pdf/2505.09388)).
  - Training on execution-trace-verified CoT: up to +22.2 on CRUXEval, but that needs CoT at inference ([2512.00127](https://arxiv.org/abs/2512.00127)).
- **Gain:** C1 51.5 → ~98 = **+7.8 Knowledge, +1.55 index.**
- **Latency:** about 1-5 ms on a pre-forked worker, or about 20-50 ms for a cold Python process (estimate).

### 2b. ChessBench: chess engine (near-exact, oracle-like)
- **Where the gold comes from.** The DI gold is Stockfish 16 at 50 ms per legal move.
- **Reference numbers** ([ChessBench paper, Table 1](https://arxiv.org/pdf/2402.04494)):
  - Stockfish 16 at that setting: 99.8% puzzle accuracy.
  - Searchless transformers: 270M → 95.4% puzzles; small ablation models → **61-63% action accuracy**.
- **LLMs are weak at this.** Qwen2.5-7B and Llama3.1-8B with SFT+RL on Stockfish labels plateau at **25-30% puzzle accuracy** ([2507.00726](https://arxiv.org/html/2507.00726v1)). Training the 4B alone will not get far.
- **Agreement unknown.** How often our own Stockfish config agrees with the DI oracle (exact-tie scoring) is **unknown**. My estimate is 60-95%. Measure it on the ChessBench **train** split (CC-BY 4.0 / CC0, disjoint from test; [licence](https://github.com/google-deepmind/searchless_chess)).
- **Gain:** C1 11.7 → 60-95 = **+8.1 to +13.9 Knowledge, +1.6 to +2.8 index.**
- **Latency:** MultiPV over legal moves at 100-300 ms per position (estimate). That is inside Jev's 70-500 ms.
- **Licence:** Stockfish and python-chess are GPL-3. Fine as a separate server process; shipping binaries brings source obligations.
- **Rule check:** an alternative is DeepMind's released 9M-270M searchless nets (CC-BY weights). This likely conflicts with "model stays 4B", so I do not recommend it.

### 2c. GSM8K: program-of-thought with our own 4B (slow route)
- **One-pass is capped.** Implicit (no-CoT) Mistral-7B: 51% vs explicit CoT 68% ([Implicit CoT](https://arxiv.org/pdf/2405.14838)). C1's 56.7 fits that ceiling. Training data alone is unlikely to reach Jev's 79.9.
- **With reasoning, small models do well** ([Qwen2.5-Math report, Table 3](https://arxiv.org/pdf/2409.12122)):

  | Model | GSM8K CoT | GSM8K TIR (Python) |
  |---|---|---|
  | Qwen2.5-Math-1.5B-Instruct | 84.8 | 83.7 |
  | Qwen2.5-Math-7B-Instruct | 95.2 | 94.6 |
  | Qwen3-4B-Base (4-shot CoT) | 87.8 | n/a |

  Qwen3-4B-Base figure from the [Qwen3 report, Table 7](https://arxiv.org/pdf/2505.09388).
- **The gain is from reasoning, not the calculator.** On GSM8K, TIR roughly equals CoT. Python helps more on harder MATH (1.5B: 79.9 vs 75.8). Programs are shorter than CoT and the arithmetic is exact.
- **Older evidence:** PoT beat CoT by about 8 points (Codex era; [PoT](https://arxiv.org/pdf/2211.12588)). A known failure: 7-8% of items are right with CoT but wrong with PoT on 7B models (wrong formula setup; [EACL 2026](https://aclanthology.org/2026.findings-eacl.257.pdf)).
- **Options make it more precise.** Requiring the program's answer to be one of the options acts as a verifier. If there is no match or an error, fall back to the one-pass probabilities.
- **Estimate:** DI GSM8K 56.7 → **85-90 = +4.7 to +5.5 Knowledge, about +1.0 index.**
- **Latency** (my arithmetic, not measured):
  - L4: 300 GB/s bandwidth, about 8-9 GB bf16 weights → ≤35 tok/s single-stream → **~3-5 s per 150-token program**.
  - FP8: about 2× faster.
  - H100: roughly 0.6-1 s.
  - **Conclusion: gate it.**

### 2d. CLadder: parse to a formal query, then a causal solver
- **Prompting is weak.** GPT-4 got 70.4% with CausalCoT ([CLadder](https://www.semanticscholar.org/paper/CLadder:-A-Benchmark-to-Assess-Causal-Reasoning-of-Jin-Chen/f30b720e34d405f200270a6ef2d09e98585fb4d1)).
- **Making the model build the causal graph works** ([CDCR-SFT](https://arxiv.org/pdf/2508.12495)). LoRA training to emit a causal DAG plus graph-based reasoning gave **95.33%** with Llama-3.1-8B, split by story and graph id. Other 7-8B models:
  - Mistral-7B: 59.6 → 92.8.
  - R1-Distill-8B: 74.3 → 92.4.

  Caveats:
  - their traces came from DeepSeek-R1 (**not allowed for us**);
  - inference is CoT (slow).
- **The allowed version:**
  - The CLadder generator is open source (MIT: [causalNLP/cladder](https://github.com/causalNLP/cladder)) and emits formal graphs, queries and reasoning, all labelled by the program.
  - Generate **new** questions from **new, Claude-authored stories**, so there is zero overlap with DI by construction.
  - Train the 4B to emit a compact JSON parse (graph, query type, given numbers), about 60-120 tokens.
  - A Python solver computes yes/no.
- **Estimate:** 65.1 → 80-90 = **+2.5 to +4.2 Knowledge, +0.5 to +0.8 index.** The 4B's parse accuracy is unknown.
- **Latency:** about 2-4 s on an L4 in bf16. Gate it.

### 2e. POP909-CL (Arts, not Knowledge): rule-based chord tool
- **The baseline is far above us.** A training-free rule-based chord extractor gets **65.0% full-chord** (per-piece macro) on POP909-CL; the best neural model gets 82.4 ([BACHI, Table 1](https://arxiv.org/pdf/2510.06528)). The DI protocol differs (exact pitch-class set on a 4-beat grid), but C1 is at 8.5 and Jev at 16.6.
- **Estimate:** 8.5 → 30-60 = **+4.3 to +10.3 Arts, +0.9 to +2.1 index.**
- **Cost:** the tool runs in ms and needs no training.
- **Caveats:**
  - POP909 is research-only, so build dev data from synthetic MIDI made from Claude-authored chord progressions;
  - the gold labels were partly derived from rule-based extraction, so this is semi-oracle.

## 3. Scenario table (estimates; DI stays report-only)

| Routes added | Knowledge | Index | vs Jev 59.51 |
|---|---|---|---|
| none (C1) | 51.2 | 54.8 | -4.7 |
| + code exec | 59.0 | 56.4 | -3.1 |
| + PoT (GSM8K-style) | 64.0 | 57.4 | -2.1 |
| + causal parse+solver | 67.3 | 58.1 | -1.5 |
| + chess engine (60-95) | 75.4-81.2 | 59.7-60.8 | +0.2 to +1.3 |
| + chord tool | same | 60.5-62.9 | +1.0 to +3.4 |

Caveats:
- C1 is on a 10K stratified sample; Jev is on the full suite.
- Every number above is a projection to verify on separate dev sets, never on DI.

## 4. How a decision engine should decide when to call a tool

Use three layers, cheapest first.

1. **Structure detectors (precision first).** They fire on content, never on benchmark names:
   - **Python:** `ast.parse` finds a function plus call args, and the options parse as literals.
   - **Chess:** `chess.Board(fen)` succeeds and at least 80% of options are legal UCI/SAN moves.
   - **Numeric word problem:** all options are numbers and the text contains 2 or more quantities.
   - **Causal:** stated probabilities plus a causal-query cue.
   - **Chord:** a note list with pitch, start and end.
2. **Learned route question.** Add a hidden `choice` question in the same forward pass, sharing the KV prefix: `route ∈ {none, exec, arith, chess, causal, chord}`.
   - Labels come from programs: route = X only where tool X's answer was verified correct **and** the one-pass answer was wrong or had a low margin.
   - This is the Toolformer / SMART logic. SMART (7B) cut tool calls 24% and improved results 37%; out of distribution it needed only 1/5 of the calls ([SMART](https://arxiv.org/abs/2502.11435); [Toolformer](https://arxiv.org/pdf/2302.04761)).
3. **Value-of-compute gate:**
   - Exact cheap tools (exec, engine, chord) always run when the detector fires.
   - Slow generative routes (PoT, causal parse) run only when the one-pass margin p1−p2 < τ. Tune τ on dev to a latency budget, for example ≤10% of traffic escalated.
   - The tool answer must map to exactly one option. If not, fall back. Report probability q on the matched option and spread 1−q by the one-pass probabilities, with q calibrated on dev.

## 5. Sandboxing and safety

- Treat both request-supplied code and code our 4B writes as untrusted. A prompt injection inside the state can steer the generated program.
- **Never run it in-process.** RestrictedPython is not a security boundary.
- **Minimum setup:**
  - AST deny-list: import, open, exec/eval/compile, dunder access;
  - a pre-forked worker in nsjail or bubblewrap with no network namespace and a read-only empty FS;
  - RLIMIT_CPU 2 s, RLIMIT_AS 256-512 MB, no fork;
  - 2 s wall timeout and an output size cap;
  - respawn the worker after every call.
- **Stronger hosted isolation** (vendor-blog figures, not peer-reviewed; [amux guide](https://amux.io/guides/ai-agent-sandboxing/), [Spheron guide](https://www.spheron.network/blog/ai-agent-code-execution-sandbox-e2b-daytona-firecracker/)):
  - gVisor: about 200-400 ms startup, 10-30% syscall overhead;
  - Firecracker microVMs: about 125 ms boot;
  - either way, keep a warm pool.
- **Chess:** validate the FEN, cap the time per call, and run the engine as a separate process.

## 6. Is tool use fair, and is it usually disclosed?

- **Common practice is to report separately and label clearly:**
  - Qwen2.5-Math reports CoT and TIR as separate columns ([report](https://arxiv.org/pdf/2409.12122)).
  - OpenAI's o4-mini scored AIME 2025 99.5% with Python vs 92.7% without, with a note saying "should not be compared to models without tool access" ([OpenAI](https://openai.com/index/introducing-o3-and-o4-mini/)).
  - HLE boards keep with-tools and no-tools separate ([BenchLM HLE](https://benchlm.ai/benchmarks/hle), [llm-stats](https://llm-stats.com/benchmarks/humanity's-last-exam-(no-tools%2C-text-only))).
- **The DI has no explicit tool rule (unknown).** Its spirit is one fixed engine with no per-benchmark tricks. The CRUXEval adaptation note says "not pass@1 or code execution", and the GSM8K items say "Do not provide reasoning".
- **Jev is a black box** that describes itself as a non-autoregressive System-1 model ([Jev explainer](https://www.mindstudio.ai/blog/jev-system-one-model-launch)). Its CRUXEval 73.0 and ChessBench 17.2 suggest no executor or engine (inference).
- **Fairness concern by route, highest first:**
  1. ChessBench + Stockfish: this reproduces the label oracle.
  2. CRUXEval + exec: this skips the skill being tested.
  3. POP909 rule tool: semi-oracle.
  4. CLadder solver.
  5. GSM8K PoT: the most standard of the five.
- **Recommendation:**
  - Ship the routes as a product feature: "exact solvers when the input is computable".
  - Always publish **two rows**: OpenDecide-4B (pure one-pass) and OpenDecide-4B + tools, listing the tools, versions and p50/p95 latency per route.
  - Claim "beats Jev" only on the pure row, or explicitly as "with tools".
  - No DI submission without the owner's go.

## 7. Owner-rule checklist and dev sets (all separate from DI test items)

| Route | Dev set (commercial OK, disjoint from DI) | Teacher | Cost |
|---|---|---|---|
| exec | 2-5K Claude-authored functions filtered by CRUXEval's published rules; labels by execution; distractors = our 4B's wrong outputs. Do not use any of the 800 CRUXEval items | none (program) | laptop CPU, $0 |
| chess | ChessBench **train**-split positions (CC-BY/CC0) with their Stockfish labels; pick depth/time here | none (program) | laptop CPU, $0 |
| PoT | GSM8K **train** (7,473, MIT), hold out 1K; self-train by keeping our 4B's programs whose executed answer is correct (no bigger teacher); distractors from a different recipe than DI's | own 4B | free L4, minutes (~150-300K gen tokens) |
| causal | CLadder generator (MIT) + new Claude-authored stories only | none (program) | free L4, minutes |
| chord | synthetic MIDI from Claude-authored progressions | none (program) | laptop CPU, $0 |

- The DI run happens once at the end, report-only and pre-registered. It never picks τ, a route or a config.
- **Disclosure:** I read the DI builder **code** on GitHub to confirm the formats. I opened no DI, OHS-3 or ejs-5 items.

## 8. Best order (tools angle)

1. **Code-exec route plus sandbox.** Cheapest, exact, CPU-only, about +1.5 index.
2. **Chess-engine route behind a disclosed flag.** Biggest gain, about +1.6 to +2.8.
3. **Gated PoT route for numeric word problems.** About +1.0, slow, so escalate only on a low margin.
4. **Causal parse+solver** (+0.5-0.8) **and chord tool** (+0.9-2.1, Arts area).
5. **In parallel (not tools):** a think route or self-distillation for GPQA/MMLU. Qwen3.5-4B already reaches GPQA-D 76.2 with thinking ([model card](https://huggingface.co/Qwen/Qwen3.5-4B)), and one-pass C1 reaches 39.8.

## Sources
- Decision Index repo, rules, engines, suite: https://github.com/flaviusburca/decision-index ; https://github.com/flaviusburca/decision-index/blob/main/docs/engines.md ; https://github.com/flaviusburca/decision-index/blob/main/docs/suite.md
- CRUXEval: https://arxiv.org/pdf/2401.03065
- Execution-trace CoT: https://arxiv.org/abs/2512.00127
- ChessBench / searchless chess: https://arxiv.org/pdf/2402.04494 ; https://github.com/google-deepmind/searchless_chess
- LLM chess post-training: https://arxiv.org/html/2507.00726v1
- Qwen2.5-Math report: https://arxiv.org/pdf/2409.12122
- Qwen3 report: https://arxiv.org/pdf/2505.09388
- Qwen3.5-4B card: https://huggingface.co/Qwen/Qwen3.5-4B
- PoT: https://arxiv.org/pdf/2211.12588 ; PoT limits: https://aclanthology.org/2026.findings-eacl.257.pdf
- Implicit CoT: https://arxiv.org/pdf/2405.14838
- CLadder: https://github.com/causalNLP/cladder ; CDCR-SFT: https://arxiv.org/pdf/2508.12495
- BACHI / POP909-CL: https://arxiv.org/pdf/2510.06528
- SMART: https://arxiv.org/abs/2502.11435 ; Toolformer: https://arxiv.org/pdf/2302.04761
- OpenAI o3/o4-mini: https://openai.com/index/introducing-o3-and-o4-mini/
- HLE tool split: https://benchlm.ai/benchmarks/hle ; https://llm-stats.com/benchmarks/humanity's-last-exam-(no-tools%2C-text-only)
- Sandboxes: https://amux.io/guides/ai-agent-sandboxing/ ; https://www.spheron.network/blog/ai-agent-code-execution-sandbox-e2b-daytona-firecracker/
- Jev explainer: https://www.mindstudio.ai/blog/jev-system-one-model-launch
