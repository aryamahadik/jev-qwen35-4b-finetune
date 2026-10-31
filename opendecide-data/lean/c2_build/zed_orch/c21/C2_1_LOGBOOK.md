# C2.1 LOGBOOK (quantitative record of every research finding, the decision it drives, and the C2.1 target)

Author: Opus 5.5 (logbook agent). Date: Sun 18 Oct 2026. Written for the owner's request (A88 b): "log every research
finding and decision quantitatively". Nothing here is new research: every number is copied from the files listed in
section 0.2, which carry the URL, fetch date (17-18 Oct 2026) and refuter verdict. Numbers marked DERIVED are arithmetic
on those numbers; section 11 shows each derivation. No model was run, no API was called, no Jev output was opened.

## 0. How to read this file

### 0.1 Tags (one per row)
| Tag | Meaning |
|---|---|
| MEAS | measured by us (our own runs, 4-17 Oct 2026; files ALREADY_TESTED_C1_OPT.md, THINK_MODE_MEASURED.md, PREREG) |
| AUTH | author-run (the paper's or benchmark's own authors measured it) |
| INDEP | independent (a third party with no stake in the model measured it) |
| VEND | vendor claim (the seller or model owner) |
| DERIVED | our arithmetic or judgement from the cited inputs (section 11) |
| UNVERIF | the refuter could not confirm it on a primary page; do not quote as fact |

Columns in every area table: ID | finding | NUMBER | unit | n | source (URL, date) | tag | decision it drives | expected
effect for C2.1. "Effect" ranges are priors to test, never forecasts. No source measured any lever on a one-token
readout of a fine-tuned Qwen3.5-4B (the closest analogues are LLM2Jev, arXiv 2610.02076, and Intern-Decision, arXiv
2610.22131, both author-run).

### 0.2 Inputs read (short sha256)
research_v3: ALREADY_TESTED_C1_OPT 04a24f59d607, THINK_MODE_MEASURED 3d5ff0916b22, OWNER_GOALS_18OCT c0180a34f67d,
ORCHESTRATION_RULES f8c75e4edd38, codeexec 9a20e93695ba, injection f0bd6d99f0d4, landscape 466c389f30f5, permission
8cee7f12c59d, recipe da24b1ad7988, tools a4db5c785f99, voice d6896ec74141. research_v4: CRITIC a144534c4688, code
59d15561b414, decision_index e0684555f1f9, hardest b4bbe043e7d5, nlu 43ae81195a59, safety aafd5d6757d8, tools
b71e578f6a13. research_v4_levers: accuracy 119fc8801d46, agentic 0ced53325c6d, calibration 66fe69f0cd88, robustness
e50011ad1312, serving 10836196c507. C2_1_EXTRA_LEVERS 5c4da098303b, C2_1_PUBLIC_TRAIN_INVENTORY 36eab740d2a5,
PREREG_FINAL.md 2faa000739b4 (records A77-A88 only), C2_1_PLAN_v3.md 60b427ef06d6 (sections 3 PRE-REGISTERED RULES, 9,
13 only, for the targets in section 10).
NOT opened, by rule: research_v3/sealed.md (a "sealed" path; training-side blindness, ORCHESTRATION_RULES rule 5), any
ohs path, the rest of plan section 3, ~/.claude, any Jev output, any dataset item.

### 0.3 Area index
1 Owner rulings in force (A77-A88) | 2 General accuracy | 3 Agentic / coding-agent | 4 Security | 5 Calibration |
6 Latency | 7 Cost | 8 Voice | 9 Robustness | 10 Measured baselines and C2.1 targets | 11 Derivations (the maths) |
12 Refuted or unverified: never quote | 13 First measurements to run (free, od-l4b or CPU)

---

## 1. Owner rulings in force for C2.1 (numbers only; full text in PREREG_FINAL.md)

| Record | Number / rule | What it fixes for C2.1 |
|---|---|---|
| A77 (18 Oct ~01:00) | 2 GO points (GO #1 training, GO #2 final test) | research + generator code now; C2.1 ROWS only after the OHS-5 freeze; C2 keeps first priority |
| A79 R1 | Modal total <= $35, training <= $30 incl. stage B | single training account >= 1.25x projection; no card; mahadikarya2 -> mahadikarya3 relay |
| A79 R12 | stage-B FP8-KL <= 15% of stage-A steps | KL to our own bf16 parent; dropped if its test fails or it busts the cap |
| A79 R13 | G about 10,000 items, floor -1.0 pp (-1.5 only if 10,000 unreachable) | G non-inferiority vs C2 |
| A79 R5 | split-aware deny-list ADOPTED (human-labelled permissive TRAIN splits) | A61(a) HIT bars stand; R5 candidates out of OHS-5 G |
| A79 R11 | voice: ASR transcripts as inputs; Kokoro-82M; Nemotron licence exception; espeak-ng off | voice data pipeline |
| A79 R10 | adaptive red-team SKIPPED | K/X stays a static-attack metric plus the small P-I sweep |
| A82 (1)-(13) | 1 split-scoped release YES (3 conditions); 2 CC BY-SA YES; 3 Wikipedia passages YES; 4 social posts / contest statements NO; 5 When2Call train, WildGuardMix, WildJailbreak NO; 6 tasksource per SOURCE YES; 7 CDLA-Permissive-2.0 YES; 8 SWE-smith procedural + CLadder minus GPT-4 variant YES; 9 NO non-English, NO vision data, NO raise of $30; 10 margin-gated second read MEASURE, adopt at >= +0.3 pp with p95 < Jev; 11 "read twice" adopt at >= +1 pp dev + repetition-flood pass, decided before data freeze; 12 confidence API fields YES; 13 NO multi-field read, 2B student, paid regions/tiers, batch tier | all owner lines of EXTRA_LEVERS and PUBLIC_TRAIN_INVENTORY |
| A88 (b) (18 Oct ~07:40) | owner top-up $10-15 for C2.1 training (amount named at GO #1); targets: coding-agent +15-20 pp over Jev (owner wish), general within 4 pp of Jev (max), beat Jev on most other metrics; no thinking mode; check each row at creation | money room above R1's $30 is decided at GO #1; targets are targets, not guarantees |
| THINK_MODE_MEASURED (orchestrator, 18 Oct) | think tier REMOVED | not a lever (section 2 row GA25) |

Note: A82 (9) "NO raise of the $30 cap in C2.1" and A88 (b) "top up $10-15 for C2.1 training" are in tension. A88 is
later and in the owner's words; the logbook reads it as: the cap may rise at GO #1, by an amount the owner names then.

---

## 2. General accuracy (owner: at most 2-3 pp behind Jev, 4 the maximum)

| ID | Finding | NUMBER | Unit | n | Source (URL, date) | Tag | Decision it drives | Expected effect C2.1 |
|---|---|---|---|---|---|---|---|---|
| GA01 | Pooled effect of all research_v4 accuracy levers | 0.0 to +0.5 on G; +0.3 to +1.2 on C-transfer | pp | n/a | research_v4_levers/accuracy.md s0 (18 Oct) | DERIVED | G gap must come from data (block R, program-gold rows), not recipe tricks | as stated |
| GA02 | Resolution of OHS-5 G | SE 0.40; a lever needs about 0.8 (2 SE) to be seen alone | pp | ~10,000 items, deff 2 | plan v3 s3 PRE-REG; accuracy.md s0.2 | DERIVED | choose levers on prior evidence + CPU checks, never "test one by one on G" | n/a |
| GA03 | Perplexity Decider v1.2: "A large part of the gains are thanks to the tasksource data"; official train splits used "decontaminated against the test sets" | qualitative | n/a | 27B | https://huggingface.co/perplexity-ai/pplx-decider-v1.2 (18 Oct) | VEND | A82 (1) split-scoped release, A82 (6) tasksource per source, lane L-R / block R | UNKNOWN at 4B (no controlled measurement at our size) |
| GA04 | Perplexity Decider v1.1 vs Jev on Jev Decision Index 0.3 | 61.56 vs 57.9 | DI score | not stated | https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b (18 Oct) | VEND | evidence that public-split strategy works at 27B | context only |
| GA05 | Jev Decision Index 0.3 make-up: 20% public kit, 50% private same-skill, 30% private new-domain | 80 | % private | 37 public benchmarks | https://github.com/apolinario/decision-index README (18 Oct) | AUTH | no split can "cover" 80% of DI; only abstain + calibration reach it | n/a |
| GA06 | DI 0.3 area weights: Knowledge and Reasoning 25.8, Language Understanding 25.8, Retrieval and Classification 20.0, Tools and Automation 18.3, Arts and Taste 10 (gold benchmarks weigh 1.2) | 25.8 / 25.8 / 20.0 / 18.3 / 10 | % | 37 | same, docs/suite.md (18 Oct) | AUTH | hard-extension generators for LU and R&C (CRITIC D3) | n/a |
| GA07 | DI 0.3 + Nimble + JevBench rows after refuter: ALLOW-R5 13, OWNER 24, DENY 41 | 13 / 24 / 41 | rows | 78 (+AA-Omniscience = 79) | research_v4/decision_index.md s9 (18 Oct) | DERIVED | block R covers about 13 named benchmarks directly | n/a |
| GA08 | AA Decision Index v1.0: 4 parts x 25% (Omniscience private 500, HLE 513 MCQ test-only, When2Call 3,423, WildGuardTest 835 of 1,725) | 4 x 25 | % | 500 / 513 / 3,423 / 835 | https://artificialanalysis.ai/methodology/decision-index (18 Oct) | INDEP | no AA component is trainable under our rules (A82 (5) NO) | 0 from data; abstain head only |
| GA09 | AA board: Claude Haiku 5.5 (Low) 61, Jev 1.13 58, GPT-6 Luna (Low) 55, GLiDE 54, Microsoft-Decision-1 54 | 61 / 58 / 55 / 54 / 54 | AA DI | 4 components | https://artificialanalysis.ai/articles/artificial-analysis-decision-index (13 Oct) | INDEP | context for any public claim; re-pull the board on claim day | n/a |
| GA10 | Public TRAIN inventory after strictest merge: 41 ALLOW-R5 (tier A 19, B2 7, C 15); 13 owner lines; about 365 DENY names | 41 / 13 / ~365 | datasets | 6 research files | C2_1_PUBLIC_TRAIN_INVENTORY.md s0, s7 (18 Oct) | DERIVED | block R core 12K rows; P1 code realism 5K; owner answered all 13 lines (A82) | GA unknown at 4B |
| GA11 | Hosting-site licence metadata: omitted > 72%, wrong > 50% | 72 / 50 | % | audit corpus | https://arxiv.org/abs/2310.16787 (searched 18 Oct) | INDEP | read the upstream LICENSE for every block-R dataset (manifest v2, one record per dataset) | protects licence hygiene |
| GA12 | LLM2Jev (Qwen3.5-4B LoRA r16 decision model): JevBench 84.0 vs 81.4 training-free (+2.6); LoRA beats full FT by +2.6 to +3.9 at 4B (tie at lambda 0.01); one seed | +2.6; +2.6..+3.9 | pts | 12K rows; 1 seed | https://arxiv.org/html/2610.02076v1 (1 Oct, v3 13 Oct) | AUTH | keep LoRA (no full fine-tune) | n/a |
| GA13 | LLM2Jev: narrow intent-only data dropped the general benchmark 81.4 -> 77.5 (100 steps) -> 74.9 (1 epoch) while val loss kept falling; Reason-21k 78.8, Reason-30k 77.1, Reason+Long-12k 80.1 | -6.5 | pts | 1 seed | same | AUTH | A21 length-coverage check; replay fixed at 38K; general rows never shed first | avoids a 0.5-2 pp loss on long G items |
| GA14 | LoRA variant spread after LR tuning: within 1-2% of vanilla; 3-run seed std 0.32-0.79 (Gemma-3-1B r128) | 1-2 %; 0.32-0.79 pts | % / pts | 9 variants, 4 models, 3 seeds | https://arxiv.org/abs/2602.04998 (Feb, rev May 2026) | AUTH | reject DoRA/PiSSA/rsLoRA/LoRA+ (L12) | -0.3 to +0.3 pp |
| GA15 | LoRA LR about 10x full-FT (fit 9.8 over 14 models); MLP LoRA matters most; large-batch penalty | 9.8x | ratio | 14 models | https://thinkingmachines.ai/blog/lora/ (29 Sep 2025) | VEND/AUTH | A20 batch check (send > 64 to a ruling); LR and alpha/r no higher than C2's | 0 to +0.5 pp if C2 batch was large |
| GA16 | Qwen3.5-4B: 32 layers = 24 GDN + 8 full attention; q,k,v,o LoRA covers 8 of 32 layers, MLP 32 of 32 | 24 / 8 | layers | config | https://huggingface.co/Qwen/Qwen3.5-4B config.json (18 Oct) | VEND | A19 LoRA attach audit; do NOT add GDN projections | protects against a silent loss of 1 pp or more (ASSUMPTION) |
| GA17 | Surogate PR 218: target "all" skipped the GDN mixer in that runtime | qualitative | n/a | 1 runtime | https://github.com/invergent-ai/surogate/pull/218 (merged 25 Sep 2026) | VEND | A19 audit | same |
| GA18 | Delta scaling gamma before merge (Qwen3-14B, biology): general avg 83.22 / 83.22 / 83.09 / 82.15 / 77.95 at gamma 0 / 0.2 / 0.4 / 0.6 / 0.8 | -1.07 at 0.6; -5.27 at 0.8 | pts | 1 model, 1 task | https://arxiv.org/html/2607.25614 Table 11 | AUTH | gamma 0.6 and 0.8 as pre-registered grid points | recovers 0 to 2 pp of any G loss |
| GA19 | Last-K checkpoint averaging / WSM (pretraining): +3.5 MATH, +2.9 HumanEval, +5.5 MMLU-Pro; 2511.18903 +1.64% (ordering + averaging combined) | +1.64 to +5.5 | pts | pretraining 1.5B | https://arxiv.org/abs/2507.17634 ; https://arxiv.org/html/2511.18903 | AUTH | A22 last ~6 states as grid points (average merged B x A deltas) | +0.1 to +0.4 pp |
| GA20 | Souper-Model weighted soup: BFCL 8B 76.50 vs best single 72.37 (+4.13); 70B 80.68 vs 78.45; MGSM ~7B +0.8; uniform soup 69.80; TIES 43.8, DARE-linear 44.4, DARE-TIES 43.4 | +4.13; TIES -28.6 | pts | >= 7B ingredients; weights tuned on test | https://arxiv.org/abs/2511.13254 (v2 18 Sep 2026) | AUTH | A23 at most 4 simplex points of C1/C2/C2.1; reject TIES/DARE | 0 to +0.5 pp beyond the alpha arm |
| GA21 | Model soups: greedy 81.03 vs best single 80.38 (ImageNet); GLUE +0.0 to +0.8 | +0.65 | pts | CLIP ViT-B/32 | https://arxiv.org/abs/2203.05482 | AUTH | O2 seed soup NO (+$36-56) | +0.1 to +0.5 pp if ever funded |
| GA22 | Instruction-modelling loss (Llama-2-7B): NLP mean +0.49 to +2.46; Less-MMLU-Chat +0.66; LIMA -0.12 | +0.49..+2.46 | pts | 18 tasks/dataset | https://arxiv.org/abs/2405.14394 | AUTH | O1 NO for C2.1 (needs micro-A/B) | -0.3 to +0.6 pp; sign unknown |
| GA23 | Flat-LoRA (Llama-2-7B r8): GSM8K +3.18, HumanEval +3.08; time +2.5%; baseline one LR, no sweep | +3.1 | pts | 1 model | https://arxiv.org/abs/2409.14396 | AUTH | O1 NO for C2.1 | 0 to +0.6 pp |
| GA24 | Curriculum: CAMPUS 38.16 vs shuffle 36.49 vs sequential 35.32; medical QA 37.46 vs 37.41 (tie) | +1.7; +0.05 | pts | LLaMA-7B/13B | https://arxiv.org/pdf/2509.13790 ; https://arxiv.org/html/2408.07888v1 | AUTH | reject quality-ordered curriculum (L9) | -0.3 to +0.4 pp |
| GA25 | Think tier measured on C1: OHS-1 80.4 -> 80.9 (Jev 81.7); OHS-2 81.0 -> 80.8 (Jev 81.5); Nimble 74.2 -> 76.4 (Jev 76.0), seen +0.0, unseen +4.7 (70.4 -> 75.1); DI sample 54.83 -> 57.74 (Jev 59.51); routed 34% | +0.5 / -0.2 / +2.2 / +2.9 | pts | practice sets | THINK_MODE_MEASURED.md (4-10 Oct) | MEAS | DROPPED (A88 "no thinking mode"; cost 5-7x, latency 1-1.5 s avg) | 0 (not a lever) |
| GA26 | Selection methods vs random: many fall below random; RDS+ the exception; myopic selection raises forgetting | qualitative | n/a | several | https://arxiv.org/abs/2410.15225 ; https://arxiv.org/abs/2503.01807 ; https://arxiv.org/abs/2605.30537 | INDEP/AUTH | reject influence/learnability selection (L16) | -0.3 to +0.3 pp |
| GA27 | Label errors: >= 3.3% of items in ten test sets; 51% of flags confirmed; MMLU 6.49% erroneous | 3.3; 51; 6.49 | % | 10 sets | https://arxiv.org/abs/2103.14749 ; https://arxiv.org/pdf/2406.04127 | AUTH | A1 gold-bug audit at TEMPLATE level before the 2x hard-bin weight (flags are candidates, not verdicts) | +0.0 to +0.4 pp on C; ~0 on G |
| GA28 | AFLite on SNLI: best model 92% -> 62% after filtering | -30 | pts | SNLI | https://proceedings.mlr.press/v119/bras20a.html | AUTH | A2 row filter as the single fix iteration (filtered share <= 30%) | +0.0 to +0.4 pp; saves a family |
| GA29 | Hardest general items: BBEH set so two reference models < 70%; ZebraLogic accuracy falls with search space | < 70 | % acc | 23 tasks | https://arxiv.org/html/2502.19187 ; https://arxiv.org/abs/2502.01100 | AUTH | pilot bar: C2 <= 70% on the top difficulty level; raise program parameters, never model-filter | difficulty control, no direct pp |
| GA30 | Prompt Repetition: 47 wins / 0 losses of 70 model x benchmark tests (p < 0.1); Just Read Twice +11.0 +- 1.3 on 16 recurrent LMs | 47/70; +11.0 | wins; pts | 7 models; 16 models | https://arxiv.org/abs/2512.14982 ; https://arxiv.org/abs/2407.05483 | VEND / AUTH | A82 (11): zero-shot test on C2, adopt only at >= +1 pp dev + repetition-flood pass, before data freeze | 0 to +1 pp G, 0 to +2 pp long inputs |
| GA31 | Margin-gated multi-read: permutation consensus 86.00 -> 91.33 (GPT-5.4), 86.33 -> 89.67 (Sonnet 4.6), K=7; TTA ~1.8x accuracy per dollar, 5 of 6 datasets | +3.3 to +5.3 | pts | RewardBench 2 factuality | https://aclanthology.org/2026.gem-main.58/ ; https://arxiv.org/abs/2608.09351 | AUTH | A82 (10): measure on od-l4b dev; adopt at >= +0.3 pp with p95 under Jev's | +0.1 to +0.7 pp; mean +2 to +5 ms |
| GA32 | PriDe letter-prior offset: 5% permuted samples, RStd -7.6, accuracy +1.2 (20 untuned LLMs, x1.15 cost) | +1.2 | pts | 20 models | https://arxiv.org/html/2309.03882v4 | AUTH | R8b stays owner-reserved; measure on dev only | 0 to +1.2 on pick-one items |
| GA33 | Option-ID token bias: removing IDs cut gpt-3.5 MMLU RStd 5.5 -> 1.0 (acc 67.2 -> 66.7) | -4.5 RStd | RStd | MMLU | same | AUTH | 20% random NON-identity permutation copies (not reversal only) | 0 to +1.0 pp on pick-one items |
| GA34 | Abstain/knowledge share: Omniscience + HLE = 50% of AA DI, no train split | 50 | % | 1,013 items | decision_index.md s2.1 | INDEP | abstain option at 10-15% of general rows, gold by construction (CRITIC E2) | 0 to small; guards hallucination half |
| GA35 | Block R and mix fit at C2 init: 38K new + 12K block R + 5K P1 realism + 4K new P0 + 2.5K P1 heads = 61.5K new + 38K replay = 99.5K rows | 99.5 | K rows | DERIVED | C2_1_PUBLIC_TRAIN_INVENTORY.md s6 | DERIVED | replay fixed as a COUNT (38K); block R and general rows after P1 and voice in the shed order | fits $30 with almost no room (see CO12) |

---

## 3. Agentic / coding-agent decisions (owner wish: +15-20 pp over Jev)

| ID | Finding | NUMBER | Unit | n | Source (URL, date) | Tag | Decision it drives | Expected effect C2.1 |
|---|---|---|---|---|---|---|---|---|
| AG01 | AmPermBench, Claude Code auto mode end-to-end: FNR 81.0 (CI 73.8-87.4), FPR 19.8; Tier-3-only FNR 70.3 / FPR 31.9 | 81.0 / 19.8 | % | 128 prompts, 253 actions (Tier-3 n=160) | https://arxiv.org/html/2604.04978v2 (28 Apr 2026) | INDEP | the strongest public gate is beatable on scope escalation; T50/T51 contrast pairs | framing only (AmPermBench is a G13 target, never copied) |
| AG02 | Same: 36.8% of state-changing actions were in-project file edits the classifier never sees; artifact-cleanup FNR 92.9 | 36.8; 92.9 | % | 253 actions | same | INDEP | A3 EDIT-AS-ACTION rows, 1.5-2.5K by substitution, >= 60% ALLOW | slice +6 to +20 pp; T50/T51 +0.3 to +1.0 pp |
| AG03 | Same: precise unauthorised single-target FNR 94.4 vs 77.6 for wide selectors; production-lane FPR 34.8 vs 9.2 low-impact; service-restart FPR 29.5 | 94.4 / 77.6; 34.8 / 9.2; 29.5 | % | same | same | INDEP | scope-inversion pairs; production rollout with trajectory authorisation = ALLOW | breaks "batch = risky" shortcut |
| AG04 | Anthropic auto mode: stage 1 FPR 8.5 (n=10,000 real) / FNR 6.6 (n=52) / synthetic exfil 1.8 (n=1,000); full pipeline 0.4 / 17 / 5.7; users approve 93% of prompts | 0.4 / 17 / 5.7 | % | 10,000 / 52 / 1,000 | https://www.anthropic.com/engineering/claude-code-auto-mode (25 Mar 2026) | VEND | O5 view-escalation NOT adopted (FNR +10.4 pp in their own data) | 0 until an FNR measurement exists |
| AG05 | Codex auto-review: 713 of 720 escalated actions approved (99.03%); recall overeager 90.3, injection 99.3, MonitoringBench Hard 96.1; no FPR | 99.03; 90.3 / 99.3 / 96.1 | % | 720 | https://alignment.openai.com/auto-review/ (30 Apr 2026) | VEND | context; circuit breaker design (3 consecutive or 10 of 50) | n/a |
| AG06 | UnderSpecBench (acted runs): Safe Success 67.9 -> 8.6 and Wrong Target 9.6 -> 75.1 from B0 to B3; blast radius barely matters (42.4 vs 43.0); 55.8-67.8% of acted runs break a boundary | -59.3; +65.5 | pp | 69 families, 2,208 variants | https://arxiv.org/html/2607.02294 (2 Jul 2026) | AUTH | blast radius made the ONLY edited fact in T51 contrast pairs; "wrong object of right kind" cell | T51 slice gain unmeasured |
| AG07 | SteerBench-Work: wrong hold 28.1 vs wrong allow 1.0; evidence-reversed mirrors 63.8 vs anchors 98.5; adversarial controls 45.6 | 28.1 / 1.0 | % | 106 scenarios, kappa 0.69 | https://arxiv.org/html/2608.12654 (12 Aug 2026) | AUTH | ALLOW >= 45% in gated families; report ALLOW recall per cell; quads (alarming/calm x present/resolved) | protects benign-block rate |
| AG08 | OverEager: removing the consent declaration raised overeager actions 0.0 -> 17.1 (GLM-4.6 in Claude Code harness) | +17.1 | pp | 76 paired scenarios | https://arxiv.org/abs/2605.18583 (~19 May 2026) | AUTH | consent pairs; guard against "target string in request = ALLOW" | n/a |
| AG09 | SABER: "contextual warning" class 82.5% harmful completion; cause task_misunderstood 47.7% | 82.5; 47.7 | % | 716 tasks | https://arxiv.org/html/2606.01317 (31 May 2026) | AUTH | warning-visible + safe-path-exists rows (gold: take the alternative or ASK) | n/a |
| AG10 | CARE (rule engine): F1 85.64, recall 75.91, FPR 0.91, 2.32 ms; removing the path stage F1 84.99 -> 68.04 (-16.95); regex F1 29.5; LLM judge 73.09 / FPR 11.25; Granite Guardian 2B FPR 45.90 | 85.64; -16.95 | F1 pts | 549 (220 dangerous / 329 safe) | https://arxiv.org/html/2607.21642v2 (6 Aug 2026) | AUTH | A4 alias / protected-root rows (300-500); report vs CARE only on our own held-out, labelled not comparable | slice +10 to +30 pp (analogy); T50 +0.4 to +1.2 pp |
| AG11 | GuardFall: pattern guards bypassable in 10 of 11 open-source agents | 10/11 | agents | 11 | https://adversa.ai/blog/opensource-ai-coding-agents-shell-injection-vulnerability/ (30 Jun 2026) | VEND | obfuscation balance (equal benign obfuscated rows) | n/a |
| AG12 | Claude Code issues: 99193 (8.3 alias rm -rf, ~116 GB lost, "looks intact" after a top-level check); 88462 (single-quoted trap repointed to $HOME) | ~116 | GB | 2 incidents | https://github.com/anthropics/claude-code/issues/99193 (3 Oct) ; /88462 (21 Aug 2026) | INDEP (user reports) | A4 alias rows; A5 LATE-BINDING rows (150-300) | A5 slice +10 to +25 pp; T50 +0.2 to +0.5 pp |
| AG13 | Terekhov: a fake "monitoring note" in code made a GPT-4.1 monitor score all backdoored samples benign | 375 / 375 | samples | 375 | https://arxiv.org/abs/2510.09462 (Oct 2025) | AUTH | A6 GATE-DIRECTED INJECTION rows (1.5-2.5K, benign twins, comment-presence probe AUC <= 0.55) | slice back within 2 pp of plain rows; dev -0.3 to 0 pp |
| AG14 | AgentAbstain: paired act+abstain accuracy 33.0-59.5 (mean 45.7), no model above 60; open-weight act 81.2 vs abstain 53.1 | 45.7 | % | 17 models, 263 pairs | https://arxiv.org/html/2607.10059v1 (11 Jul 2026) | AUTH | A9: T59 ASK-OR-PROCEED promoted (8 triggers), act side >= 55% | in-distribution 70-85% (guess) |
| AG15 | Ask or Assume: separate checker 69.4 vs single agent 61.2, but plain prompted "ask first" 70.4; late questions 43.9% vs 14.8% | +8.2 (0 over prompting) | pts | SWE-bench Verified underspecified | https://arxiv.org/html/2603.26233v1 (27 Mar 2026) | AUTH | early gate before first state-changing edit; taxonomy only | n/a |
| AG16 | MCP tool descriptions: 97.1% of 856 tools have >= 1 smell, 56% unclear purpose; rewriting lifts success median +5.85 pp, regresses 16.67% of cases, +67.46% steps | 97.1; +5.85 | %; pp | 856 tools, 103 servers | https://arxiv.org/abs/2602.14878 (Feb, rev May 2026) | AUTH | A8 SMELLY-DESCRIPTION operators for T54 | smelly slice +1 to +4 pp; T54 +0.3 to +1.0 pp |
| AG17 | ToolBench-X: frontier models 35-50 pp below clean under injected hazards; no model above 0.60 | 35-50; 0.60 | pp; score | 1,106 tasks (200-task subset) | https://arxiv.org/html/2606.25819v1 (24 Jun 2026) | AUTH | A8, A16 (observation-format perturbation) | see RB04 |
| AG18 | Terminal-Bench failure taxonomy: "no or irrelevant verification" and "weak verification" modes; GPT-5 judge 90% agreement on 120 human traces | 90 | % agreement | 120 traces | https://arxiv.org/html/2601.11868 (17 Jan 2026) | AUTH | A7 VERIFICATION-RELEVANCE rows (300-600, swapped inside T56) | slice +5 to +15 pp; T56 +0.6 to +1.8 pp |
| AG19 | Real coding-agent sessions: inaccurate self-reporting 22.58%; constraint violations 38.33%; misread intent 26.95%; overreach 10.20% | 22.58 | % episodes | 16,118 episodes | https://arxiv.org/html/2605.29442v1 | INDEP | T56 partial-state-as-complete rows; question-as-permission rows | n/a |
| AG20 | False success: 45% / 47% of tau2 airline/retail failures, 75.8% of AppWorld; LLM judges AUROC <= 0.65; TF-IDF+XGBoost 0.83 / 0.95 (LR 0.849 / 0.915) | 0.65 vs 0.95 | AUROC | 5 judges x 5 prompts | https://arxiv.org/html/2606.09863 (1 Jun 2026) | AUTH | surface-cue probes on tool-output features (closing words, action count); identical claim text in pairs | n/a |
| AG21 | ImpossibleBench: GPT-5 cheats 76% (one-off SWE) / 54% (conflicting); abort option 54 -> 9 (o3 49 -> 12); LLM monitors 86-89% (LCB) vs 42-65% (SWE) | 54 -> 9 | % | 103 / 349 per variant | https://arxiv.org/html/2510.20270 (23 Oct 2025) | AUTH | T56g hack + legit twins; abort/ask gold for impossible-by-spec rows; multi-file stratum | n/a |
| AG22 | Monitors trained on prompt-elicited hacks: ModernBERT 34.50 on wild hacks vs 99.70 in-distribution | -65.2 | pts | small | https://arxiv.org/html/2604.23488v1 | AUTH | held-out transform families; report the OOD line, never claim wild-hack recall | n/a |
| AG23 | Wrong-but-passing patches (SWE-ABS): 2,184 of 11,041 passing patches rejected (19.78%); top agent 78.80 -> 62.20; causes logic 47, incomplete 35, type 7, boundary 6, off-by-one 1 | 19.78; 47/35/7/6/1 | % | 100 hand-analysed | https://arxiv.org/html/2603.00520v1 | AUTH | T57 class weights = this mix; four-gate hidden suite | n/a |
| AG24 | UTBoost: 28.4% (170/599) of passing patches wrong on SWE-bench Lite, 15.7% (92/584) on Verified | 28.4 / 15.7 | % | 599 / 584 | https://arxiv.org/pdf/2506.09289 | INDEP | same | n/a |
| AG25 | SWE-bench+: solution leakage in 32.67-33.47% of successful patches | ~33 | % | 2 versions | https://arxiv.org/html/2410.06992v2 | INDEP | "answer in issue" CPU probe; leakage capped at natural rate | n/a |
| AG26 | EquiBench: DCE pairs mean 49.0 (chance 50), CUDA best 63.8; similarity bias 8.5 vs 93.0 | 49.0 | % acc | 2,400 pairs | https://arxiv.org/html/2502.12466v3 | AUTH | T42c crossed equivalence pairs + text-similarity-only probe | n/a |
| AG27 | CRUXEval-O GPT-4: 63% no-CoT vs 81.9% CoT | -18.9 | pts | 800 | https://crux-eval.github.io/ | AUTH | gate T42c against base 4B on the same rows, not generative numbers | n/a |
| AG28 | ToolMaze: implicit vs explicit recovery-rate gap 37.15 pp (mean over 9 models); Qwen3.5-35B-A3B success 41.50 -> 16.94 perturbed, recovery 29.48 | 37.15 | pp | 400 tasks | https://arxiv.org/html/2606.05806v1 | AUTH | T55 2x2 explicit/implicit x transient/permanent ladder | n/a |
| AG29 | LIMBO: lost-ack duplicate 0.5% with read-back; 56% (late commit) and 74% (redelivery) without; idempotency keys 28% -> 4%; success claimed in 90% of duplicate episodes | 0.5 / 56 / 74 | % | 25,930 episodes, 9 models | https://arxiv.org/abs/2609.29095 | AUTH | T55 AMBIGUOUS-WRITE class; plan citation fixed (CRITIC H2) | n/a |
| AG30 | When2Call paper: 4B SFT 47.8% -> RPO 69.1% accuracy; adding When2Call data cost BFCL Live AST -6.2 | +21.3; -6.2 | pts | 3,652 | https://arxiv.org/html/2504.18851 | AUTH | call / no-call kept at 40-60% per T54 sub-block (over-conservatism guard) | n/a |
| AG31 | Hallucinated packages: 19.7% of samples, open models 21.7% vs commercial 5.2%, 43% repeat; 2026 replication 4.62-6.10% | 19.7 | % | secondary | CSA note (19 Apr 2026); arXiv 2605.17062 snippet | UNVERIF | T63 "EXISTS?" sub-family (500 rows) | n/a |
| AG32 | Coding-agent decision types with no family (CRITIC C1-C8): delegate/compaction/plan-vs-act, compile/type, IaC, DB migration, merge/semver/commit-message, dependency licence, phishing | 8 gaps | gaps | n/a | research_v4/CRITIC.md s1 C | DERIVED | T60 CONTROL-NEXT 2,000; T67 IAC-GATE + migration 1,000; T63 EXISTS 500 + licence 200; T66 heads 800; T59 2,000 | new slices; whole-model effect unmeasured |
| AG33 | Hardest-question projection: 22 family targets; >= 25% of rows at ladder levels L3-L4; quad structure mandatory for T50/T51/T53/T41c/T56 | 22; 25 | targets; % | n/a | C2_1_PUBLIC_TRAIN_INVENTORY.md s4 | DERIVED | every G0-lite gets a difficulty ladder | n/a |
| AG34 | Competitors with coding-verifier numbers: CLM-8B DeepSWE verifier 81.6 vs Jev 71.1 (38 tasks), Terminal-Bench 2.1 87.6 vs 83.1 (30); BFCL 95.2 vs Jev 99.2 | +10.5; +4.5 | pts | 38 / 30 | VentureBeat (25 Sep 2026) | AUTH (via press) | "no published coding-gate numbers with n >= 100" is the honest claim | n/a |
| AG35 | Intern-Decision 4B (Qwen3.5 one-prefill): Typed Decision 80.55 vs Jev 73.35; seven-suite avg 90.02 vs Jev 88.74; 2B 84.68 avg | +7.2; +1.3 | pts | own suite | https://arxiv.org/html/2610.22131v1 (Oct 2026) | AUTH | competitor to know; its multi-field read (S19) is O14, NO for C2.1 | n/a |
| AG36 | Strands Decider 2B: JevBench public 0.723 (v19) / 0.779 (v1) | 0.72-0.78 | score | 231 tasks | https://github.com/strands-labs/strands-decider (1 Oct 2026) | AUTH | eval-only baseline in our size class (teacher-labelled, never data) | n/a |
| AG37 | ATBench-Codex bar: AgentDoG 1.5-4B-U 84.4 acc (1.5-4B 80.0); v1 82.2 acc / 83.8 F1; untuned Qwen3.5-4B 78.0 / 73.4 | 84.4 | % acc | 500 (250/250) | https://arxiv.org/html/2605.29801v1 ; https://arxiv.org/html/2604.14858v1 | AUTH | Tier-1 bar; base row under our readout required | forecast 76-86 (toss-up for #1) |
| AG38 | ATBench (1,000) bar: AgentDoG 1.5-4B-U 77.7 F1; GPT-5.4 76.7; released 1.5-4B 74.3; Qwen3.5-4B zero-shot 27.6 | 77.7 | F1 | 1,000 | same | AUTH | report with rank; whole-trajectory protocol differs from our per-call gate | forecast 65-78 (loss likely) |
| AG39 | When2Call, AA protocol: Celeris 84, GLiDE 84, Jev 1.13 81, GPT-6 Luna 77, Haiku 5.5 73 (AA article); d1-ultra 92.6 and Jev 1.14 80.8 mirror-only | 84 | % acc | 3,423 | AA article (13 Oct 2026); BenchLM mirror (15 Oct) | INDEP / UNVERIF | claim "ahead of Jev 1.14 under AA protocol, measured by us"; never forecast #1 | forecast 82-90 |

---

## 4. Security (injection, command safety, secrets, attack robustness)

| ID | Finding | NUMBER | Unit | n | Source (URL, date) | Tag | Decision it drives | Expected effect C2.1 |
|---|---|---|---|---|---|---|---|---|
| SE01 | Tool-output injection detectors, TPR at 1% FPR on AD-Matched: Horizon 82.2 (AD-Shift 87.9), Wolf 73.8, PG2-86M 69.4, Qwen2.5-7B judge 57.4, Llama-3.1-8B judge 55.3, PIGuard 2.1; threshold set on the same benign set | 82.2 | % TPR | 432 injected / 585 benign | https://arxiv.org/html/2610.03448 (2 Oct 2026) | INDEP | our own protocol: threshold from a HELD-OUT benign split; AD-Matched and AD-Shift reported apart; no 55-80 forecast | a loss to Horizon (agent-data-trained) is likely |
| SE02 | Rankings do not transfer: Kendall tau 0.01 between BIPIA and AD-Matched (PIGuard 95.1 vs 2.1) | 0.01 | tau | 15 detectors | same | INDEP | headline only on OHS-5 and unseen sets; upstream audit statement for ourselves | n/a |
| SE03 | Jev measured as a generic injection classifier: AUROC 0.871, FNR@0.5 0.649, FPR@0.5 0.048, ECE 0.541, TPR@1%FPR 12.5, 191 ms mean; GPT-5.5 judge AUROC 0.897, 3,890 ms | 0.871; 12.5 | AUROC; % | 47,611 pooled (BIPIA-dominated), one prompt, no CI | https://arxiv.org/html/2610.20907 (14 Oct 2026) | INDEP | target "higher TPR at 1% FPR than Jev at a task-disjoint threshold" (Jev read by us) | likely beatable; must be measured ourselves |
| SE04 | NotInject over-defence: Horizon 94.4 (FPR 5.6, vendor card), Lakera 87.61, InjecGuard 87.32, GPT-4o 86.73, ProtectAI v2 56.64 | 94.4 | % acc | 339 | HF card (2 Oct 2026); https://arxiv.org/html/2410.22770v3 | VEND / AUTH | target FPR upper bound <= 5% (half-width +-2.3 pp at n=339, section 11 D9) | plausible, not assured |
| SE05 | Default-threshold collapse: PG2-86M caught 6 of 629 buried AgentDojo attacks at 0.5, 0 FP of 97 | 0.95 | % recall | 629 / 97 | https://github.com/rudratoshs/buried-injections (24 Sep 2026) | INDEP (individual) | every TPR claim states its threshold source | n/a |
| SE06 | Format drives FPR: ProtectAI v2 3.8% general text vs 30.1% AgentDojo vs 66.9% tau-bench outputs; Sheltron source token cut tau FPR 85.6 -> 4.4 | 3.8 / 30.1 / 66.9 | % FPR | as SE01 | https://arxiv.org/html/2610.03448 | INDEP | carrier-format variation; benign tool-output rows of the same formats | n/a |
| SE07 | Adaptive attacks broke 12 published defences, ASR > 90% for most (near zero under static attacks) | > 90 | % ASR | 12 defences | https://arxiv.org/abs/2510.09023 (USENIX Sec 2026) | INDEP | every robustness line says "static", P-I adaptive number beside it | n/a |
| SE08 | "Confidently Wrong": guard misses at confidence 0.99-1.00; FNR 0.01-0.97 across 5 shifts; one detector pooled ECE 0.06 but 0.91 on attacks | 0.99-1.00; 0.97 | conf; FNR | 3 detectors | https://arxiv.org/pdf/2606.22659 (21 Jun 2026) | INDEP | A13 benign-WORDED hijack payloads + lexical probe AUC <= 0.55; trap-slice ECE | +10 to +30 pp relative on that slice |
| SE09 | Character smuggling vs 6 guards: emoji smuggling 100% evasion on all 5 targets; Unicode-tag 50.7-100% (injection set), Azure 9.0% (jailbreak set) | 100 | % evasion | 476 + 78 | https://arxiv.org/abs/2504.11168 (LLMSEC 2025) | AUTH | A11 hidden-character canonicaliser; FREE 200-row probe on C2 first | 0 if C2 ignores them; else up to that class's share |
| SE10 | Hidden tag / zero-width instructions raised Claude Haiku compliance 0.8% -> 49.2% with tools on | +48.4 | pp | 1 model | https://arxiv.org/html/2603.00164v1 (Mar 2026) | INDEP | A11 | same |
| SE11 | Cue-invariance training on Qwen3-4B: static role-play ASR 31.6 [23.3, 41.4] -> 0.0; adaptive (n=83) 95 -> 16.9 (BCT) / 0.0 (OPCT); costs IFEval 84.3 -> 45.3 / 68.4, XSTest 89.5 -> 77.9, WildJailbreak benign 98.1 -> 73.1 (Gemini) | -31.6; -24.4 over-refusal | pp | 83 adaptive | https://arxiv.org/html/2605.21834v1 ; https://arxiv.org/abs/2510.27062 | AUTH | A10 cue-invariance pairs on EVERY gate family, each with a clean twin, 1-2 wrapper families held out; FREE C2 probe first | wrapper errors -50 to -90% rel. in-family, -20 to -50% held-out; G -0.5 to 0 pp |
| SE12 | Embedding-space AT: adaptive ASR 8.0 -> 0-2% but clean utility 36.7 -> 24-26% (alpha 0.01), ~7% (alpha 0.05) | -6 to -8 ASR; -10 to -30 utility | pp | AgentDojo / AgentDyn | https://arxiv.org/html/2608.05430 (5 Aug 2026) | AUTH | O3 OFF (only if the P-I sweep fails K/X after A10-A13) | G -1 to 0 pp if ever on |
| SE13 | AgentDyn (helpful third-party instructions on the critical path): no defence utility 53.3 / ASR 37.8; PromptGuard2 utility 20.8 under attack; ProtectAI utility 0.0; CaMeL 0 / 0 / 0 | 37.8 | % ASR | 560 cases | https://arxiv.org/html/2602.03117v1 | AUTH | ALLOW_BENIGN ambient-instruction class (login, OTP, invite, attachment, conflict message, TODO) | protects benign rate |
| SE14 | Injection prevalence in coding agents: 66.5% of 4,176 runs executed it (Sonnet 4.6 41.1, GPT-5.4 73.6, GPT-5.3 Codex 84.8; alt-text only 16.7) | 66.5 | % runs | 4,176 | https://arxiv.org/html/2607.20759v1 (NC-ND; taxonomy only) | AUTH | carrier list: issues, comments, code comments, PDFs, alt-text | n/a |
| SE15 | Cloud-log injection: Azure Prompt Shield caught 1 of 32, GCP Model Armor 0 | 3.1 | % | 32 | https://arxiv.org/abs/2604.15368 | AUTH | CI/cloud logs as a T41c carrier | n/a |
| SE16 | Trigger-word shortcut (NotInject): ProtectAI v2 76.11 / 47.79 / 46.02 and InjecGuard 91.15 / 89.38 / 81.42 at 1 / 2 / 3 trigger words | -30.1; -9.7 | pts | 3 x 113 | https://arxiv.org/html/2410.22770v3 | AUTH | trigger-density ladder (0-3+ security words) on benign text; malicious text with 0 trigger words | n/a |
| SE17 | Provenance-sensitive over-defence: a detector with F1 > 0.98 still blocks 31.4% of external benign; hard-benign FPR DeBERTa-FT 0.38, PG2 0.15 | 31.4 | % FPR | 1,472 hard benign | https://arxiv.org/html/2609.15017 (IEEE Access 2026) | AUTH | real-text benign slice only if its 8.5 passes | n/a |
| SE18 | MCP tool-description poisoning: best refusal below 3%; more capable models more vulnerable | < 3 | % refusal | 45 servers, 353 tools | https://arxiv.org/abs/2508.14925 (AAAI 2026) | AUTH | MCP descriptions as T41c carrier; server list registered in G13 | n/a |
| SE19 | Credential egress: plain HTTP on the CORRECT host leaked 90.6% vs 9.4% typosquat; recovery 0-24.2%; Opus 4.8 1.6% leak with 88.3% false refusal; domain-verification instruction 73.5 -> 23.4 | 90.6; 88.3 | % | 1,024 + 512 + 256 | https://arxiv.org/html/2610.08871 (6 Oct 2026) | AUTH | T53 transport-only matched pairs; >= as many allow-listed odd-host ALLOW rows as BLOCK | n/a |
| SE20 | Secret leak channels in agent skills: stdout/stderr 75.8%, files 18.7%, network 13.1%; debug logging 73.5% | 75.8 | % | 520 skills, kappa 0.88 | https://arxiv.org/html/2604.03070v1 | INDEP | T53 non-"send" channels (print, log, temp file, shell history, commit) | n/a |
| SE21 | Allowlist bypasses: Cursor CVE-2025-54131 (backtick / $(cmd)), CVE-2026-22708 (env-var poisoning); Claude Code `Bash(git push:*)` stopped 8 of 14 spellings, 5 reached the remote | 5/14 | spellings | 14 | GitHub advisories; https://dev.to/rulestack/... (22 Sep 2026) | VEND / UNVERIF (blog) | T50 alias / spelling-variant rows (git -C, git -c, sh -c) | n/a |
| SE22 | Chat guards fail on agent trajectories: Qwen3Guard ATBench F1 0.8, Llama Guard 3-8B 7.3, Llama Guard 4 12B 41.7 | 0.8 / 7.3 / 41.7 | F1 | 1,000 | https://arxiv.org/html/2605.29801v1 | AUTH | product claim = per-call coding gate, not a chat guard | n/a |
| SE23 | Public injection TRAIN data under our rules: ALLOW-R5 7 of 155 safety datasets (none agent-shaped); Gandalf ignore 777 + summarisation 114 train rows (MIT); Aya red-teaming 7,419 | 7 / 155 | datasets | 155 | research_v4/safety.md s10 | DERIVED | T50/T51/T53/T41c stay Claude-authored with program gold; Gandalf direct-injection slice with 50% Claude benign twins; block R safety text 800 rows | small slice |
| SE24 | K/X pre-registered gate | static ASR <= max(C2 + 2, 3); benign-block <= C2 + 2 | % / pp | >= 950 attack + 950 benign | plan v3 s3 PRE-REG | MEAS (rule) | ship-binding | see section 10 |

---

## 5. Calibration and abstention

| ID | Finding | NUMBER | Unit | n | Source (URL, date) | Tag | Decision it drives | Expected effect C2.1 |
|---|---|---|---|---|---|---|---|---|
| CA01 | Jev 1.13 under an independent protocol (top-label ECE, 10 equal-mass bins, 5-fold cross-fitted T): 3.3 (D1 typed decisions), 3.2 (D2 CLINC-150); pooled social-science 25.1 shipped -> 3.8 after one fitted T | 3.3 / 3.2 / 25.1 -> 3.8 | % ECE | 3 suites | https://arxiv.org/html/2610.00346v1 (29 Sep 2026) | INDEP | A27 aligned protocol; "better than Jev" only at aligned ECE <= 3.0% (target 2.5%) AND paired UB of (C2.1 - Jev) < 0 | win NOT assured |
| CA02 | Our own protocol: C1 3.3 vs Jev 1.14 6.0 (text side-bench) | 3.3 vs 6.0 | % ECE | side-bench | C2_1_EXTRA_LEVERS.md s4; plan v3 s13 | MEAS | not a headline (protocol differs from CA01) | n/a |
| CA03 | Liquid: d1-ultra 1.5 vs Jev 1.14 2.7 on its 112-eval suite, no formula or bins | 1.5 vs 2.7 | ECE | 112 evals | https://gigazine.net/gsc_news/en/20261016-d1-ultra (16 Oct) | VEND | context only | n/a |
| CA04 | Stored temperature fitted on few options fails at 150 options: Kev-9B CLINC-150 ECE 0.377 shipped vs 0.051 at T=1; stored T 2.30 / 2.35 / 1.30 | 0.377 vs 0.051 | ECE | 150 options | https://arxiv.org/html/2610.00346v1 | INDEP | A28 option-count-aware T (type x K bucket) + clip audit of the [0.8, 1.3] bound | protects the large-K tail; 0 on 2-6 option types |
| CA05 | One fitted temperature cuts calibration error 2.8-6.0x without changing labels or confidence ordering | 2.8-6.0x | ratio | 6 LLMs | https://arxiv.org/pdf/2609.19072 (Aug-Sep 2026) | AUTH | abstention quality improves only via ranking levers (A28, O10), not more scaling | n/a |
| CA06 | Jev on CLINC OOS: accepts 31.0% of out-of-scope at a held-out threshold (in-scope risk ~5%); with an explicit OOS option 19.5% while 92.5% in-scope still route; CI 0.142-0.502 | 31.0 -> 19.5 | % | CLINC-150 | same | INDEP | O10 build program NOTA rows, keep OUT of the mix unless the owner OKs (cap <= 5%) | OOS acceptance -35% rel. or better (not significant); G -0.3 to -1.0 pp if NOTA > 5% |
| CA07 | Off-the-shelf LLMs pick an invalid option when the right one is removed: 9.9-52.2% (Qwen3-8B 11.0%) | 9.9-52.2 | % | MMLU-Pro Math | https://arxiv.org/html/2610.08153 (6 Oct 2026) | AUTH | same as CA06 | n/a |
| CA08 | Split-conformal sets (LLaMA-13B, MMLU): alpha 0.1 coverage 91-94%, mean set size 2.4-3.7; alpha 0.2 81-83%, 1.6-3.2; cross-subject coverage drops to ~83% | 91-94; 83 | % coverage | 16 subjects | https://arxiv.org/html/2305.18404 | AUTH | A29 Mondrian conformal ASK band per type (>= 500 calibration rows per type) | ASK on ~5-25% of items at 90% coverage (DERIVED, D11) |
| CA09 | ConformalGuard at target FPR 0.01: fine-tuned BERT conformal 0.006 (recall 0.996 -> 0.995); Claude Sonnet 4 raw 0.040 -> 0.008 (recall 0.938 -> 0.875); needs >= 1,000 negatives (n=100 gives +-0.006) | 0.006; -0.001 recall | FPR; recall | 39,935 emails | https://arxiv.org/html/2610.14365 (9 Oct 2026) | AUTH | A29 Learn-then-Test per gate, >= 1,000 held-out negatives, never sealed sets | FPR claims true with stated confidence; ~0 recall cost for fine-tuned models |
| CA10 | Role-stratified conformal risk control: at 1% budget violation 0.0-0.3% vs 1.1-5.0% mean-aggregate; utility 9.4-14.9%; over-intervention under shift 30.6% | 0.0-0.3 | % violation | 6 models | https://arxiv.org/abs/2607.24343 (27 Jul 2026) | AUTH | A29 (extrapolated from tool-call fields to option probabilities; stated) | n/a |
| CA11 | Learned correctness head: ~1,000 graded examples suffice, gains flatten ~5,000; ECE 29.9 -> 10.8; meta-model AURC -2.0 to -2.6%, E-AURC -3.3 to -4.2% vs MSP | 1,000; -2.0..-2.6 | rows; % AURC | 7-13B | https://arxiv.org/html/2406.08391v1 ; https://arxiv.org/abs/2610.19394 | AUTH | A28 CPU logistic head, used only if it beats max-prob on a held-out family split | AURC a few % relative |
| CA12 | Fine-tuned LLMs overconfident without validation: Laplace-LoRA MAP ECE 31.2 (WG-S), 31.0 (ARC-C), 13.4 (ARC-E), 4.0 (BoolQ); TS competitive with a val set (ARC-C 4.6 vs LA 7.5) | up to 31.2 | % ECE | LLaMA2-7B | https://arxiv.org/abs/2308.13111 | AUTH | A25 post-T NLL/ECE/AURC term in candidate score S (weight pre-registered); Bayesian adapters rejected (break 14 ms path) | <= 0.5 pt ECE |
| CA13 | Label smoothing 0.1: LLaMA3-8B MMLU ECE .050 -> .012, acc .651 -> .646; Gemma2-2B .341 -> .020 | -3.8 pt ECE; -0.5 acc | pts | 1-8B | https://arxiv.org/html/2508.00264 | AUTH | keep plain CE (a pilot would need Modal; per-type T already planned) | n/a |
| CA14 | Guard calibration clean -> adversarial: WildGuard .004 -> .196, Llama-Guard-3 .013 -> .308, ShieldGemma .325 -> .684; FN at 0.99 confidence 11-12% / 37% | +0.19..+0.36 | ECE | 5 guards, 6 attacks | https://arxiv.org/html/2609.36477v1 | AUTH | T fitted on a dev set including the hard bin; trap-slice ECE reported | n/a |
| CA15 | Selective prediction fails on confidently wrong slices: ERM risk 5.35% (full) -> 0.75% (70% coverage) but one subgroup >= 14% at every coverage; T* = 1.0 | 5.35 -> 0.75; >= 14 | % risk | Civil Comments | https://arxiv.org/html/2605.14074v1 | AUTH | A28 per-slice risk-coverage (trap, near-miss, long-trace, ASR) | stops over-claims |
| CA16 | Base-rate shift: training balance 40-60% yes vs a 10% customer block rate = -2.20 logit; 5% = -2.94 | -2.20 / -2.94 | logit | n/a | calibration.md finding 4 | DERIVED | O12 prior-shift API correction: NOT in C2.1, document | large on skewed traffic |
| CA17 | Jev API: Choice returns per-option probabilities + `confidence`; yes/no returns only P(yes); no abstain option; 3-option confidence (3 max - 1)/2 | n/a | n/a | n/a | https://openrouter.ai/docs/guides/community/jev (18 Oct); flaviocopes.com summary | VEND | A82 (12) additive confidence fields: calibrated p on every primitive, defined `confidence`, ASK thresholds per type, `calibration_version` | visible product edge |
| CA18 | Pre-registered ECE gate | <= 3.5 | % l1 ECE | pooled C and G | plan v3 s3 PRE-REG | MEAS (rule) | ship gate only; CA01 shows it does not beat Jev | see section 10 |

---

## 6. Latency

| ID | Finding | NUMBER | Unit | n | Source (URL, date) | Tag | Decision it drives | Expected effect C2.1 |
|---|---|---|---|---|---|---|---|---|
| LA01 | C1 server, H100 batch 1: round 1 p50/p95 32/41; SGLang 0.5.20 fast path 14.1/19.2 per decision; batch 8 9.9 per decision; graph == eager | 14.1 / 19.2 | ms | B1a session | commit 01d67c5; ALREADY_TESTED_C1_OPT.md | MEAS | SGLang S1 merged bf16 stays the path | baseline |
| LA02 | End-to-end, laptop -> us-west, c=1: C1 p50 137 vs Jev 156; p95 162 vs 224 | -19 / -62 | ms | small n | ALREADY_TESTED_C1_OPT.md | MEAS | e2e claim "below Jev by our client, same region" | baseline |
| LA03 | Non-GPU share of e2e p50 | ~105 of 137 | ms | DERIVED | 137 - 32 (D5) | DERIVED | biggest e2e levers are client and network, not kernels | n/a |
| LA04 | Cold start | 131 | s | measured | ALREADY_TESTED_C1_OPT.md | MEAS | warm pool (no Modal for serving, O18) | n/a |
| LA05 | Think mode: cap300 1.3 s, cap1024 4.3 s, DEER1024 2.8-3.06 s/item; L4 4.2-4.8 s; rule "think e2e median <= 1 s" FAILED for every policy | 1.3-4.3 | s | practice sets | THINK_MODE_MEASURED.md | MEAS | DROPPED | 0 |
| LA06 | Compute floor at 557 tokens, H100 batch 1 (3.9B non-embedding params, 50% tensor-core use) | ~9 | ms | DERIVED | serving.md s0 | DERIVED | at most ~5 ms of launch overhead left to remove at batch 1; ~0 at batch >= 8 | caps kernel gains |
| LA07 | Breakable prefill CUDA graph: 1.70x prefill vs eager (gpt-oss-120b, 4xGB300), 1.60x GLM-5.2; multimodal and LoRA auto-route to eager | 1.70x | speed-up | large models | https://github.com/sgl-project/sglang/pull/29458 (merged 2 Jul 2026) | AUTH | A30 text-only hot-path server + BCG; FIRST read the B1a log (graph == eager may already cover it) | -1 to -4 ms of 14.1 |
| LA08 | SGLang decision path (H200, Qwen3.5-4B, 16 candidates): p95 84.8 (generate) vs 74.4 (single-item score) vs 55.7 (multi-item); probabilities move up to 0.07 across batch compositions / cache state | -10.4; 0.07 | ms; prob | 1 config | https://www.lmsys.org/blog/2026-09-25-sglang-decision-models ; SGLang docs | AUTH / VEND | A31 0.5.21 `/v1/score` with label_token_ids on OUR prompt (never `/v1/decisions`); mixed-batch flip-rate + T re-check | -0 to -2 ms |
| LA09 | LM head = 248,320 x 2,560 = 636M params = 1.27 GB bf16 per forward; ~0.4 ms on H100 (2.7%), 4.2 ms on L4 | 0.4 / 4.2 | ms | DERIVED | serving.md S4 | DERIVED | A31 optional sliced head (option rows only) | -2 to -3% H100; -4 to -9% L4 |
| LA10 | FlashInfer GDN prefill: 506 vs 425 us per layer (1.19x), whole block 1.03x (B200) | 1.03x | speed-up | Qwen3.5-397B | https://github.com/sgl-project/sglang/pull/22921 | AUTH | O19: test only inside an approved paid session | 0 to -3% |
| LA11 | Cold vs reused connection: 385 vs 260 ms (OpenAI SDK), 199 vs 139 ms (Anthropic SDK); handshake 60-130 ms | 60-130 | ms | 1 environment | https://github.com/openJiuwen-ai/agent-core/issues/17 | INDEP | A33 persistent local sidecar (unix socket, warm HTTP/2, fail-closed); FIRST check how the hook process spawns | -40 to -130 ms per call IF per-call TLS today; else 0 |
| LA12 | Region distance: edge TTFB p50 Germany 98 vs US-central 29 ms | +69 | ms | probe repo | https://github.com/mazamaka/llm-latency-tracker | INDEP (probe operator unknown) | O19: one region until user geography is known | far users -80 to -250 ms with more regions |
| LA13 | Radix prefix cache on a GDN hybrid: up to 17.8x worse mean TTFT ON vs OFF (18,357 vs 3,071 ms at 1k/1k; 1.12x with the unmerged fix); zero hits on a repeated prompt | 17.8x | ratio | 1 report | SGLang PR 27220 (bot-closed 30 Sep 2026); issue 21158 | AUTH (report) | A32 radix ON vs OFF A/B on the real mix before counting any prefix saving | sign unknown |
| LA14 | Hosted decision-model latency (AA per-task median across 4 evals, protocol unstated): Celeris 63, Jev 1.14 78 (mirror), d1-ultra 93 (mirror), Jev 1.13 127; Jev "under 700 ms" (press) | 63-127 | ms | AA | BenchLM mirror (15 Oct); implicator.ai (9 Oct) | INDEP / UNVERIF / VEND | compare only to hosted decision models, same client; never vs rule engines (CARE 2.32 ms) | n/a |
| LA15 | Small-model rivals: Strands 2B 115 / 299 ms (RTX 3090); Intern-Decision 4B 44.16 ms vs Jev 109.70 (RTX 4090, HF backend); DreamGuard 25 ms; SingGuard 45-57 ms (A100); StepGuard 599.9 ms | 25-600 | ms | various | landscape.md 4.2; serving.md S17 | AUTH | our 14.1 ms server number is a different stack; no like-for-like claim | n/a |
| LA16 | Margin-gated reread cost: +14 ms per routed item (one extra read), mean +2 to +5 ms at 15-25% routed | +2 to +5 | ms mean | DERIVED | agentic.md s2 | DERIVED | A82 (10): adopt only if p95 stays under Jev's | p95 moves to the routed path |
| LA17 | Image path: --mm-feature-transport=cuda_ipc 94.6 -> 75.1 ms, +66% c8 throughput, answers unchanged | -19.5 | ms | C1 | ALREADY_TESTED_C1_OPT.md | MEAS | ADOPTED; images unchanged in C2.1 | n/a |
| LA18 | Weight-only INT4/INT8 does not help prefill: Qwen2.5-32B H200 TTFT 57.7 FP16 vs 73.5 Marlin-AWQ vs 51.9 Marlin-GPTQ vs 277.8 default AWQ | +15.8 (worse) | ms | 1 model | https://jarvislabs.ai/blog/vllm-quantization-complete-guide-benchmarks | INDEP | reject INT4/INT8, FP8 KV, bf16 state, early exit, AMD/TPU/Trainium | 0 or negative |

---

## 7. Cost

| ID | Finding | NUMBER | Unit | n | Source (URL, date) | Tag | Decision it drives | Expected effect C2.1 |
|---|---|---|---|---|---|---|---|---|
| CO01 | C1 serving cost: $0.0137 per 1K at 100% GPU use, $0.0275 at 50%, $0.069 at 20% (= 0.0137 / u) | 0.0137 | $ / 1K decisions | measured throughput | ALREADY_TESTED_C1_OPT.md | MEAS | cost is a utilisation problem | baseline |
| CO02 | Jev: measured $0.0234 per 1K; list $0.042 per M input tokens, output free (implies ~557 tokens per request); AA $41.53 per 1M tasks | 0.0234; 0.042 | $ / 1K; $ / M tok | n/a | ALREADY_TESTED; https://docs.typesafe.ai/models (18 Oct) | MEAS / VEND | price claims in the rival's unit ($ / M input) | baseline |
| CO03 | Break-even utilisation vs Jev | 58.5 | % (~47 of 80 req/s) | DERIVED | D1, D2 | DERIVED | batching / async demand to stay above it | n/a |
| CO04 | OHS-3 run cost: C1 $0.433 vs Jev $0.061 (low utilisation) | 7.1x | ratio | 1 run | ALREADY_TESTED_C1_OPT.md | MEAS | honest: at low load we cost more than Jev | n/a |
| CO05 | Think call ~20x a fast call; with ~1/3 routed ~5-7x average | 5-7x | ratio | DERIVED | THINK_MODE_MEASURED.md | DERIVED | think dropped | 0 |
| CO06 | GPU prices (Modal, per hour): L4 0.80, L40S 1.95, RTX PRO 6000 3.03, H100 3.95, B200 6.25; GCP g2-standard-4 on-demand 0.7068, spot 0.6479 (-8%) | 0.80-6.25 | $ / h | price pages | https://modal.com/pricing (18 Oct); holori calculator | VEND | A35 measure L4 fast path on od-l4b (free) | n/a |
| CO07 | Break-even request rate vs Jev's $0.0234: H100 ~47 req/s, L40S ~23, L4 ~9.5; warm cost L4 $19/day vs H100 $95/day; L4 server latency likely 50-100 ms | 47 / 23 / 9.5 | req/s | DERIVED | serving.md S11 | DERIVED | L4 tier only for non-interactive / overflow traffic, never the headline latency | n/a |
| CO08 | Exact-match decision cache: hit rate unknown (TVCache 15-32% on a terminal benchmark, RL-rollout context) | 0-30 | % hits | DERIVED | https://arxiv.org/html/2602.10986v1 | AUTH / DERIVED | A34 cache (hashes only, policy version in key); measure repeat rate on our traces first | break-even 41-59% (D4) |
| CO09 | Async / batch tier: utilisation 20% -> 40% takes $0.069 -> $0.034 per 1K | -51 | % | DERIVED | serving.md S15 | DERIVED | A82 (13) NO for C2.1 (owner pricing later) | n/a |
| CO10 | Competitor price floor: generic Qwen3.5-4B FP8 $0.03 per M input on DeepInfra -> ~$0.0167 per 1K at 557 tokens | 0.0167 | $ / 1K | price list | https://deepinfra.com/blog/qwen3-5-4b-deepinfra-benchmarks (3 Apr 2026) | VEND | cost claim must state utilisation | n/a |
| CO11 | Rival price list: d1-ultra $0.042/M (AA $31.80 per 1M tasks); Celeris $31.57 per 1M tasks; GLiDE $0.15/M ($119 per 1M tasks); Microsoft-Decision-1 $0.042/M; Perplexity 27B $16.53 per 1M tasks; OpenAI Decisions $0.10/M | 16.53-119 | $ / 1M tasks | mirror / press | landscape.md 4.2 | INDEP (mirror) / press | context | n/a |
| CO12 | C2.1 training cost per row: $18/76K = $0.237 and $28/95K = $0.295 per 1K rows (2 epochs, mean <= 800 tokens); $30 cap ~101K rows; planned 99.5K rows = $23.6-29.4 | 0.237-0.295 | $ / 1K rows | DERIVED | inventory s6 | DERIVED | fits R1 with almost no room; A88 top-up named at GO #1; replaced by C2's measured s/step before GO #1 | $23.6-29.4 + levers $2-4 |
| CO13 | C2 measured training speed: 3.067 s/step vs reference 3.716 (-17.5%); seg1 100 steps ~$0.86 | 3.067 | s / step | 100 steps of 3,673 | PREREG A86 | MEAS | input to C2.1's A37(k) projection | full C2 run ~3.13 h of compute (D7) |
| CO14 | Robustness rows if ADDED: +20-28% tokens (~+$4-8, can break the cap); by SUBSTITUTION 0; long tail A14 at 5% x 2.5K tokens = +11% (~+$2-3); 8% = +17% | +11..+28 | % tokens | DERIVED | robustness.md budget note | DERIVED | substitution only; A14 share first to shed | n/a |
| CO15 | Micro-A/B arm 10K rows x 1 epoch $1.2-1.5; a pair $2.4-3.0 (floor, no boot overhead) | 2.4-3.0 | $ / pair | DERIVED | accuracy.md s0.3 | DERIVED | O1 NO for C2.1 | n/a |
| CO16 | Independent-seed soup: 2 extra full seeds +$36-56 | 36-56 | $ | DERIVED | accuracy.md L6 | DERIVED | O2 NO | n/a |
| CO17 | Extra warm region: L4 $584 / month, H100 $2,884 / month | 584 / 2,884 | $ / month | DERIVED | serving.md S9 | DERIVED | O19 one region | n/a |
| CO18 | Spot overflow discount | -8 to -25 | % | price snapshots | serving.md S13 | VEND | A82 (13) paid tiers NO in C2.1 | n/a |

---

## 8. Voice (spoken input to the text decision model)

| ID | Finding | NUMBER | Unit | n | Source (URL, date) | Tag | Decision it drives | Expected effect C2.1 |
|---|---|---|---|---|---|---|---|---|
| VO01 | C1 voice path: Nemotron Speech Streaming EN 0.6B, 560 ms mode + forced flush (LOCKED); ~86 ms after end of speech; decision unchanged 97% synthetic, 89% real speech | 97 / 89 | % unchanged | C1 trials | ALREADY_TESTED_C1_OPT.md (VOICE_REAL.md) | MEAS | ASR-error rows in C2.1 (goal >= 97% real) | see section 10 |
| VO02 | Nemotron EN 0.6B average WER (8 sets, no PnC) by chunk: 1.12 s 6.93, 0.56 s 7.07, 0.16 s 7.67, 0.08 s 8.43 | 7.07 at 560 ms | % WER | 8 sets | https://huggingface.co/nvidia/nemotron-speech-streaming-en-0.6b (18 Oct) | VEND | pin the checkpoint revision (ASR-specific errors are what we train against) | n/a |
| VO03 | Trailing silence needed: (right_context + 1) x 16 x 160 samples = 320 ms at the 160 ms chunk; larger at 560 ms (UNVERIFIED) | 320 | ms | 1 config | https://www.daily.co/blog/building-voice-agents-with-nvidia-open-models/ | VEND | pad silence at end of input in training audio and serving; measure for 560 ms | n/a |
| VO04 | Errors by word role (single edits): negation 25.7, number 21.9, entity 17.1, intent cue 12.4, slot 9.5, function word 2.9, other 1.4; real ASR at WER 6.3-8.1% cut call accuracy 82.3 -> 71.9-74.9 | -7.4 to -10.4 | pts | 210 / 594 sources | https://arxiv.org/html/2610.17619 (13 Oct 2026) | AUTH | weight ASR rows to decision-bearing roles; drop-only if a negation / number / path span is altered | role-aware rows |
| VO05 | Voice-style rewrites cost ~-9.7 vs keyboard noise ~-3.0 (geometric-mean ratios; ~6.2 raw pts; near 0 on multiple choice); succinct -24.1; homophone -0.4; LoRA fix hurt clean 60.9 -> 58.0 | -9.7 vs -3.0 | ratio pts | 5 models | https://arxiv.org/html/2608.03970v1 | AUTH | clean twins; voice share modest (3K kept rows) | upper bound for us |
| VO06 | TTS -> ASR round trip alone is weak: JGA 29.88 -> 29.94 (non-significant); entity change 38.84% vs 95.47% for LLM phonetic (barred) | +0.06 | JGA | DSTC11 | https://arxiv.org/html/2409.06263 | AUTH | generators A (Kokoro round trip) + B (harvested Nemotron confusion table) | n/a |
| VO07 | ASR-agnostic noise beats ASR-specific on unseen ASR: QNLI 76.89 vs 71.00, RTE 56.55 vs 46.43, SST-2 82.36 vs 80.85; corruption P(z) 0.15 / 0.21 | +5.9 / +10.1 / +1.5 | pts | BERT-base | https://arxiv.org/abs/2410.15609 (EMNLP 2024) | AUTH | A18 rule-based generator C (pronunciation-dictionary swaps, licence checked); neural ISNI is O9 NO | +0 to +2 pp real speech |
| VO08 | Onset errors: stateful carry-over cut utterance-onset WER 15-21% relative | -15 to -21 | % rel. | streaming ASR | https://arxiv.org/abs/2608.22101 (22 Aug 2026) | AUTH | onset augmentation ("don't", "yes" are decision-bearing) | n/a |
| VO09 | VoiceBench: cascade Whisper-large-v3 + GPT-4o 87.23 vs GPT-4o-Audio 86.42; best open end-to-end ~55; mispronunciation -20.34%, repair -12.55% | 87.23 vs 86.42 | score | benchmark | https://arxiv.org/abs/2410.17196 (TACL 2026) | AUTH | cascade ASR stays (locked); native audio encoder later | n/a |
| VO10 | Text vs voice gap for omni models (TTS + DEMAND noise to 5 dB SNR) | 1.8-4.8 | pts | Confetti | https://www.alphaxiv.org/abs/2605.15104 | AUTH | V1 stress tier design | n/a |
| VO11 | Real-speech eval size: 520 pairs give 80% power at alpha 0.05 for a 3-pt gap at 6% discordance; 1,000 pairs resolve ~2 pts | 520 | pairs | DERIVED | voice.md s7; D10 | DERIVED | V2 real tier: >= 500 paired items, >= 12 speakers, >= 2 devices, >= 2 rooms, cluster bootstrap | proof standard |
| VO12 | Proposed V2 bars: <= 3 pts loss at 3-8% WER, <= 6 at 8-15%; harmful-flip rate <= 1.5x text FPR; ECE within 2 pts of text | 3 / 6 / 1.5x / 2 | pts / ratio | proposal | voice.md s7 item 8 | DERIVED | to be ruled before the V2 read | n/a |
| VO13 | Owner R11: ASR transcripts as training inputs; Kokoro-82M; NVIDIA Open Model License exception for Nemotron; espeak-ng fallback disabled | n/a | n/a | n/a | PREREG A79 | MEAS (rule) | voice pipeline fixed | n/a |
| VO14 | Jev is text only (docs) | n/a | n/a | n/a | https://docs.typesafe.ai/models (18 Oct) | VEND | voice is a product edge; compare our text-vs-voice gap, not Jev | n/a |

---

## 9. Robustness (formats, perturbations, long inputs, held-out families)

| ID | Finding | NUMBER | Unit | n | Source (URL, date) | Tag | Decision it drives | Expected effect C2.1 |
|---|---|---|---|---|---|---|---|---|
| RB01 | Consistency losses lose to plain augmentation: JS-consistency LoRA had higher spread and lower accuracy on all 8 models; consistency/contrastive "mostly matched or beaten" by simple batching; best-to-worst template gap stays 40-57% | 8 / 8 | models | 52 tasks; 4 models | https://arxiv.org/abs/2508.11383 ; https://arxiv.org/html/2609.01217 | AUTH | A26 close the optional symmetric-KL branch; plain permuted copies only | 0 (removes a trainer risk) |
| RB02 | Formatting alone moves LLaMA-2-13B accuracy by up to 76 points | 76 | pts | FormatSpread | https://arxiv.org/abs/2310.11324 (ICLR 2024) | AUTH | A15 format-dialect augmentation of the card BODY and tool schemas (scaffold sha unchanged) | worst dialect +3 to +10 pp |
| RB03 | One template per batch: Qwen3-0.6B worst-template Rouge-L 0.308 -> 0.449 (Llama3.2-1B 0.210 -> 0.363); mixed batches worse (per-template gradient signs disagree on 57-64% of parameters) | +0.14 / +0.15 | Rouge-L | 4 models | https://arxiv.org/html/2609.01217 (1 Sep 2026) | AUTH | A15 batch-by-dialect sampler in the trainer | G 0 to +0.3 pp |
| RB04 | Tool-output robustness: observation family 0.455 (structure noise 0.460, evidence loss 0.142) vs interface family 0.918 vs clean 0.979 | 0.455 vs 0.979 | robustness score | 7 models | https://arxiv.org/html/2608.23635 (23 Aug 2026) | AUTH | A16 observation-format perturbation (JSON/YAML/plain, ANSI, CRLF, wrapped logs, truncation markers), one format held out | +3 to +8 pp on held-out-format slice |
| RB05 | Long-input attacks on 512-token guards: Prompt Overflow bypass > 99.5% (PG2-86M, K 4-16); DeBERTa 92.3% at K=4 with natural prose vs 0% blank filler | > 99.5 | % bypass | encoder guards | https://arxiv.org/html/2605.23196v1 | AUTH | A14 long-input slice at a FIXED 5% share (1.5-3K tokens train; 3-8K eval only); FREE C2 probe first; A36 hardened chunk reads for outputs > 256 tokens | 0 on main mix; +3 to +15 pp on buried-payload slice |
| RB06 | Repetition flips guards: 5 of 9 lightweight guards flipped malicious -> benign, flip rates 8-92%, first flips at 2.6K-9.4K tokens | 5 / 9 | guards | 9 | https://arxiv.org/abs/2609.15013 (Sep 2026) | AUTH | repetition-flood slice in A14; required pass before "read twice" (A82 11) | n/a |
| RB07 | Character perturbations: detectors trained with the transforms reach recall 0.97-0.99 on leetspeak / homoglyph / zero-width; PG2 0.32, Llama Guard 3-1B 0.48 | 0.97-0.99 | recall | PIDS-Bench | https://arxiv.org/html/2609.15017 | AUTH | A12 character-perturbation augmentation (~3K rows by substitution), whole transform families held out | in-family near-complete; held-out unknown; G 0 to -0.2 pp |
| RB08 | Model selection: ERM average 67.0 (training-domain validation) vs 63.8 (leave-one-domain-out); "no method improves on ERM by more than one point" | 67.0 vs 63.8 | % acc | 7 datasets | https://arxiv.org/abs/2007.01434 (ICLR 2021) | AUTH | A24 leave-one-family-out term in candidate score S (weight pre-registered; held-out sub-families -3 to -5% rows) | 0 to +1 pp on held-out families |
| RB09 | Hybrid linear-attention recall at long context: a 25% softmax / 75% GDN student NiH 0.684 vs 0.954 teacher at 131K | -0.27 | NiH | 1 model | https://arxiv.org/pdf/2512.20569 | AUTH | context only: our cap 1,536 tokens (<= 10% of rows), mean <= 800 | n/a |
| RB10 | Multilingual guardrails drop on non-English data; one guard high FPR on low-resource languages | qualitative | n/a | several | https://arxiv.org/abs/2410.22153 | AUTH | A82 (9) NO non-English data; A17 300-row translated EVAL slice only; claims say "English only" | unknown; hypothesis -5 to -20 pp rel. |
| RB11 | Prompted flip rates under option reordering: 10.96-54.74% (MMLU), 3.75-36.26% (ARC-Challenge); a zero-flip-by-construction method cost 35.18 pp | 3.75-54.74 | % flips | 4 models | https://arxiv.org/html/2608.11947 | AUTH | flip rate reported WITH accuracy; the 1% target is a reported metric, not a claim | n/a |
| RB12 | Net robustness projection (all ADOPT NOW robustness levers) | G 0 to -0.5; K/X static -30 to -60% rel. if C2 is sensitive; held-out slices +3 to +15 | pp / % rel. | DERIVED | robustness.md ranking | DERIVED | free C2 probes (A10, A11, A14) decide which levers build rows | none of these are measurements |
| RB13 | Vision side-bench: C1 77.7 vs Jev 1.14 85.1 (base 73.6) | -7.4 | Index pts | side-bench | ALREADY_TESTED_C1_OPT.md | MEAS | A82 (9) NO vision data; C2.1 claims exclude vision | 0 (images attached unchanged) |

---

## 10. Measured baselines and C2.1 targets

### 10.1 Measured baselines (our own measurements unless tagged)

| Metric | C1 | C2 | Jev | Gap (C1 - Jev) | Source / tag |
|---|---|---|---|---|---|
| OHS-1 practice (general) | 80.4 | not yet | 81.7 | -1.3 | THINK_MODE_MEASURED.md, MEAS |
| OHS-2 practice (general) | 81.0 | not yet | 81.5 | -0.5 | same, MEAS |
| OHS-3 general | 74.3 | not yet | 79.6 | -5.3 | plan v3 s9, MEAS |
| Text side-bench Index | 77.6 | not yet | 79.3 (1.14) | -1.7 (no difference demonstrated) | plan v3 s9, MEAS |
| Decision Index sample | 54.83 | not yet | 59.51 | -4.7 | THINK_MODE_MEASURED.md, MEAS |
| Nimble 13 sets (unseen sets) | 74.2 (70.4) | not yet | 76.0 | -1.8 | same, MEAS |
| Vision side-bench Index | 77.7 | n/a | 85.1 (1.14) | -7.4 | ALREADY_TESTED, MEAS |
| ECE, our protocol (text side-bench) | 3.3% | not yet | 6.0% | -2.7 | plan v3 s13, MEAS |
| ECE, independent protocol (typed decisions) | not measured | not measured | 3.3% / 3.2% (1.13) | n/a | CA01, INDEP |
| Injection, pooled third-party cohort | not measured | not measured | AUROC 0.871, TPR@1%FPR 12.5%, FNR@0.5 64.9% | n/a | SE03, INDEP |
| When2Call, AA protocol | not measured | not measured | 81 (1.13, AA); 80.8 (1.14, mirror) | n/a | AG39 |
| Server latency p50 / p95, H100 batch 1 | 14.1 / 19.2 ms | not yet | not public | n/a | LA01, MEAS |
| End-to-end p50 / p95 (laptop -> us-west, c=1) | 137 / 162 ms | not yet | 156 / 224 ms | -19 / -62 ms | LA02, MEAS |
| Cost per 1K decisions | $0.0137 at 100% use; $0.069 at 20% | not yet | $0.0234 measured; $0.042 per M input list | break-even ~59% use | CO01-CO03 |
| OHS-3 run cost | $0.433 | n/a | $0.061 | 7.1x | CO04, MEAS |
| Voice, decision unchanged (real / synthetic) | 89% / 97% | not yet | text only | n/a | VO01, MEAS |
| Coding-agent C-transfer / C-total vs Jev | not in training-side files (sealed side) | C2 report due Mon 19 Oct | not in training-side files | n/a | blindness rule |

C2 status (PREREG A86-A88): training running on Modal; seg1 (100 of 3,673 steps) done at 3.067 s/step; C2 final report
due Mon 19 Oct afternoon (ET). Every C2 row above fills in from that report; C2.1's floor is "C2.1 - C2 >= -1.0 pp on G".

### 10.2 C2.1 targets, honest projection and proof

| Metric | Owner target (A88, OWNER_GOALS) | Pre-registered rule (plan v3 s3) | Honest projection (DERIVED; not a forecast) | What would prove it |
|---|---|---|---|---|
| General accuracy, gap to Jev | <= 2-3 pp, 4 the maximum | Jev - C2.1 <= 4.0 on OHS-5 G (ship), <= 3.0 (target); C2.1 - C2 >= -1.0 (SE 0.40, ~10,000 items) | Plan: 3.0 to 5.5 pp without block R (planner judgement, no basis for probabilities). Block R gain at 4B: UNKNOWN (only 27B vendor evidence, GA03). ADOPT NOW levers: -0.5 to +0.5 (GA01). Starting gaps span -0.5 to -5.3 (10.1). Logbook range with everything: about 2.5 to 5.5 pp; "<= 4" may or may not be met | early: public-G panel of UNSEEN sets (read before GO #1), 25% / 50% snapshot G proxy during training; binding: OHS-5 G one look, source-clustered CI |
| Coding-agent, C-transfer (headline) | +15-20 pp over Jev (owner wish) | C2.1 - Jev >= +5 with paired LB > 0 AND C2.1 - C2 >= +3 with LB > 0 (SE ~1.77) | +4 to +10 (plan s13) plus +0.3 to +1.5 from new row types (EXTRA_LEVERS s4) = about +4 to +11.5. +15-20 is NOT projected on the transfer block | OHS-5 C-transfer, paired cluster bootstrap, one look |
| Coding-agent, C-total (home field) | +15-20 pp | C2.1 - Jev >= +8 with LB > +3; at or above Jev on >= 5 of 6 sub-blocks; C2.1 - C2 >= +5 | trained sub-blocks ~85-92 vs Jev ~65-78 (guess) = about +10 to +20; the owner's +15-20 is plausible HERE only | OHS-5 C-total, labelled "home field" |
| Public Tier 1 | beat Jev / #1 where possible | report with rank; "#1" only if paired 95% LB > best published point | When2Call AA 82-90 vs bar 84; ATBench-Codex 76-86 vs bar 84.4; ATBench 65-78 vs bar 77.7 (loss likely); NotInject FPR UB <= 5% plausible; clear #1 on 0-2 of 6 | our reads with Jev read by us; base Qwen3.5-4B row under the same readout |
| Security K/X (static attacks) | beat Jev | static ASR <= max(C2 + 2 pp, 3%); benign-block <= C2 + 2 pp | static ASR -30 to -60% relative IF the free C2 probes show wrapper / character / long-input sensitivity, else ~0; adaptive ASR unchanged (O3 off); benign-block 0 to +1 pp worse, held by clean twins and ALLOW >= 45% | OHS-5 K/X (>= 950 attack + 950 benign), P-I adaptive number beside it |
| Injection vs Jev | beat Jev | higher TPR at 1% FPR than Jev at a task-disjoint threshold; NotInject FPR UB <= 5% | likely above Jev's pooled 12.5% (SE03), unlikely above Horizon 82.2 on AD-Matched (agent-data-trained) | Tier-1 items with Jev read once by our client; OHS-5 C-INJ |
| Calibration | beat Jev | ship: pooled l1 ECE <= 3.5%; claim: aligned ECE <= 3.0% (target 2.5%) AND paired UB (C2.1 - Jev) < 0 | aligned ECE about 2.5-3.5% (C1 3.3% under our protocol; levers 0 to -0.5 pt); Jev 3.2-3.3% aligned, so the win is NOT assured; unseen-type pools (Jev 25.1% shipped) are the likelier win | A27 protocol on OHS-5 pooled C and G, same items, one Jev read; per-slice curves (A28) |
| Server latency | lowest possible, no quality loss | parity >= 99.5% argmax for any serving change | 14.1 -> about 10-13 ms p50 (H100 batch 1); ~0 change at batch >= 8 | od-l4b relative gains + parity record per change (A30, A31) |
| End-to-end latency | beat Jev | e2e p50 below Jev's measured e2e by our client | same client/region: about 95-137 ms p50 (C1 137 today; -40 to -130 ms more only IF the hook uses per-call TLS now); p95 about 140-162 vs Jev 224 | latency suite after GO #2, same client and region for both |
| Cost | beat Jev | below Jev's $0.042 per M input at a STATED utilisation | break-even ~59% utilisation today; 41-59% with a 0-30% cache hit rate; below ~40% use we cost more than Jev (OHS-3: 7.1x) | CPU cost script on measured throughput; repeat-rate measurement on our traces |
| Voice | beat Jev (Jev has no voice) | V2 bars to be ruled (VO12) | 89% real speech today; ASR rows + generator C (+0 to +2) give an estimated 90-95% (judgement; no measured analogue); >= 97% is not assured | V2 real tier, >= 500 paired items, >= 12 speakers, McNemar + cluster bootstrap |
| Robustness | beat Jev | held-out lines are report-only | +3 to +15 pp on each held-out slice (wrappers, dialects, output formats, long inputs) | held-out sub-family report lines |
| Vision | (owner: beat Jev everywhere) | n/a | not targeted (A82 9): C1 77.7 vs Jev 85.1 stays; claims exclude vision | n/a |
| Training money | minimal weekly spend | R1 <= $30 training (+ A88 top-up $10-15 named at GO #1) | $23.6-29.4 at 99.5K rows + $2-4 for A14/A15 tokens | A37(k) projection from C2's measured 3.067 s/step |

---

## 11. Derivations (the maths behind every DERIVED number)

D1 Cost per decision. H100 $3.95/h; measured 12.5 ms GPU per decision -> 3,600 / 0.0125 = 288,000 decisions/h = 80 req/s.
   $3.95 / 288,000 = $1.37e-5 = $0.0137 per 1K at utilisation u = 1. At utilisation u: cost(u) = 0.0137 / u.
   u = 0.5 -> 0.0274; u = 0.2 -> 0.0685. (CO01)
D2 Jev tokens per request. $0.0234 per 1K = $2.34e-5 per request; list $0.042 per 1e6 tokens = $4.2e-8 per token;
   2.34e-5 / 4.2e-8 = 557 tokens. (CO02)
D3 Break-even. u* = 0.0137 / 0.0234 = 0.585 -> 58.5% x 80 req/s = 46.8 req/s. (CO03)
D4 Cache. With hit rate h (a hit costs ~0 GPU), cost(u) = 0.0137 (1 - h) / u; break-even u* = 0.585 (1 - h):
   h = 0 -> 58.5%; h = 0.3 -> 41.0%. (CO08)
D5 Non-GPU share of e2e. 137 ms e2e p50 - 32 ms round-1 server p50 = ~105 ms. (LA03)
D6 Training cost per row. $18 / 76K rows = $0.237 per 1K; $28 / 95K = $0.295 per 1K (2 epochs, mean <= 800 tokens).
   $30 / 0.295 = ~101.7K rows. 99.5K x (0.237..0.295) = $23.6..$29.4. (CO12)
D7 C2 compute time. 3,673 steps x 3.067 s = 11,265 s = 3.13 h (excludes boot, eval and checkpoint time). (CO13)
D8 Resolution on G. SE = 0.40 pp; a single lever is visible at about 2 SE = 0.8 pp; every ADOPT NOW G effect
   (-0.5 to +0.5) sits inside 1.25 SE, so none can be confirmed alone on G. (GA02)
D9 NotInject CI. n = 339, p = 0.05: SE = sqrt(0.05 x 0.95 / 339) = 0.0118; 95% half-width 1.96 x 0.0118 = 2.3 pp.
   An FPR near 2% or lower is needed to separate from Horizon's 5.6% (SE04).
D10 Voice pairs (McNemar). Discordance p_d = 0.06, gap delta = 0.03, alpha 0.05 (z 1.96), power 0.8 (z 0.84):
   n = (1.96 sqrt(p_d) + 0.84 sqrt(p_d - delta^2))^2 / delta^2 = (1.96 x 0.2449 + 0.84 x 0.2431)^2 / 0.0009
     = (0.480 + 0.204)^2 / 0.0009 = 0.468 / 0.0009 = 520 pairs. (VO11)
D11 Conformal ASK rate. With top-1 accuracy a and coverage target 1 - alpha, singleton sets cover only a, so sets of
   size > 1 must recover at least (1 - alpha) - a of the mass: for a = 0.85, alpha = 0.10 that is >= 5% of items; the
   upper end is all 15% errors plus uncertain correct items, so ~5-25% depending on how well the probabilities rank the
   true second option. Measure on mixdev. (CA08)
D12 Prior shift. Training 50% vs deployment 10% block rate: logit shift = ln[(0.1 / 0.9) / (0.5 / 0.5)] = ln(0.111)
   = -2.20; at 5%: ln(1/19) = -2.94. A calibrated 0.50 on balanced data reads ~0.10 on that traffic. (CA16)
D13 Slice-to-family effect. family gain = slice share of dev x slice gain. A3: 5% x 6-20 = 0.3-1.0 pp; A4: 4% x
   10-30 = 0.4-1.2; A5: 2% x 10-25 = 0.2-0.5; A7: 12% x 5-15 = 0.6-1.8; A8: 25% x 1-4 = 0.25-1.0. Shares are design
   choices; gains are analogies (UNVERIFIED until a pilot reads them). (AG02, AG10, AG12, AG18, AG16)
D14 Margin-gated reread. routed share 15-25% x gain 1-3 pp = +0.15 to +0.75 pp (discounted 40-70% from published
   +3.3 to +5.3 because C2.1 trains on permuted copies). Latency: one extra read ~14 ms; mean +0.15..0.25 x 14 =
   +2.1..+3.5 ms (two reads up to +7 ms). (GA31, LA16)
D15 Headline power. SE 1.77 pp (deff 2): P(point >= +5 | true +8) = P(Z >= (5 - 8) / 1.77 = -1.69) = 0.955. If the true
   gap is exactly +5, power is ~50%. (10.2 C-transfer)
D16 Think cost. A think call decodes ~500-1,000 tokens vs one prefill -> ~20x; with ~1/3 routed: 2/3 x 1 + 1/3 x 20
   = 7.3x (upper); ~5x at the low end. 14 ms -> ~1-1.5 s average. (CO05, GA25)
D17 Compute floor. 3.9B non-embedding params x 2 FLOP x 557 tokens = 4.3e12 FLOP; H100 dense bf16 ~990 TFLOP/s x 50%
   use = ~495 TFLOP/s -> ~8.8 ms. 14.1 - ~9 = ~5 ms removable at batch 1. (LA06; the TFLOP figure is a datasheet value,
   UNVERIFIED here)
D18 LM head. 248,320 x 2,560 = 635.7M params x 2 bytes = 1.27 GB; at 3.35 TB/s ~0.38 ms (H100), at 300 GB/s ~4.2 ms
   (L4). (LA09)
D19 Base-model GDN state. 24 layers x 32 heads x 128 x 128 x 4 bytes = 50.3 MB per request or cached prefix (fp32);
   KV = 8 layers x 2 x 4 heads x 256 x 2 bytes = 32 KB per token (26 MB at 800 tokens). (serving.md; radix A/B, LA13)
D20 LoRA capacity does not bind. LoRA r16 on all linears of Qwen3.5-4B = 32.5M params x ~2 bits = 6.5e7 bits vs at most
   125K rows x ~2 bits of label = 2.5e5 bits (~260x less) -> raising rank adds ~0 (estimate; the 2 bits/param figure is
   a citation of synthetic-data work). (GA14)

---

## 12. Refuted or unverified: never quote these as facts

| Claim | Status | Correct reading |
|---|---|---|
| L22 "legal-token loss normaliser +0 to +0.3 pp" (LLM2Jev) | REFUTED | the paper never ablates it; keep a 1-line record of C2's normaliser only |
| "Fine-tuning raised ECE at 4B" (LLM2Jev) | REFUTED | 4B LoRA ECE 0.050 vs 0.057 base (better); full FT 0.070 |
| "LoRA beat full FT by 2.2-3.5 at every anchor weight" | REFUTED | +2.6 to +3.9, tie at lambda 0.01; one seed |
| "Narrow data lowered general by 5.2" | REFUTED | 6.5 (81.4 -> 74.9) |
| ATBench-Codex bar 82.2 | REFUTED | 84.4 accuracy (AgentDoG 1.5-4B-U); 82.2 / 83.8 F1 is the v1 row |
| LIMBO "56-74% duplicated a lost-ack write" | REFUTED | lost-ack 0.5%; 56% late commit, 74% redelivery |
| S26 AMD / TPU / Trainium evidence (Neuron repo, MI355X cost) | REFUTED | conclusion "no" stands; evidence does not |
| d1-ultra 92.6 on When2Call; Jev 1.14 80.8 / 78 ms on AA | UNVERIF | BenchLM mirror only; OrcaRouter says no AA row |
| Hallucinated-package rates (19.7%, 21.7% vs 5.2%, 43% repeat) | UNVERIF | secondary summaries |
| L3 error-neighbour mutation, L4 pair margin loss, L15 semantic dedup, L18 mixing-law fit, L24 FP32 LoRA states | UNVERIF | not carried as levers |
| R10 policy-card perturbation "+5 to +15 pp" | UNVERIF | abstract-level only; one free check at the T50/T51 G0-lite |
| Smooth-ECE citations 2406.04068 / 2402.10046 | REFUTED (citation) | those are other papers |
| S5 Rust frontend numbers, S10 hedging 1,800 -> 74 ms, S16 LoRA at base price, S28 TokenSpeed | UNVERIF | sources deleted, open or unreadable |
| C1 bias-corrected scaling; C14 probability-parity evidence | UNVERIF | mixed-batch probability check lives inside A31 |
| "Comment filtering judged insufficient" (Terekhov) | REFUTED | untested in the paper |
| AmPermBench data licence | unclear (paper CC BY-NC-SA) | eval framing only, never data |

---

## 13. First measurements to run (all free: od-l4b one job at a time, or CPU), in the order they unlock decisions

| # | Measurement | Decides | Model / effort (ORCHESTRATION_RULES) |
|---|---|---|---|
| 1 | Read the B1a log: did a prefill CUDA graph already run? | whether A30 is new work | Haiku low |
| 2 | LoRA attach audit (A19), C2 batch / LR / alpha / normaliser record (A20, L22 record) | silent-loss protection | Sonnet medium (CPU) |
| 3 | C2 free probes on od-l4b: 200 wrapped rows (A10), 200 hidden-character rows (A11), buried-payload slice (A14), 300 translated rows (A17) | which robustness rows get built | Haiku runs, Sonnet checks |
| 4 | Public-G panel of UNSEEN public sets: base 4B, C1, C2 (Jev read once by our client) | the first G-gap signal before GO #1 (CRITIC E1, F1) | Sonnet medium |
| 5 | Margin-gated second read and "read twice" zero-shot on C2 dev (A82 10, 11) | adopt at >= +0.3 pp (p95 < Jev) / >= +1 pp + flood pass | Sonnet medium |
| 6 | L4 fast-path ms/decision and $/1K at several loads (A35); radix ON vs OFF A/B (A32); score API + mixed-batch flip rate (A31) | L4 tier, prefix-cache saving, 0.5.21 path | Haiku runs, Sonnet checks |
| 7 | Hook process model + new vs reused connection timing (A33); repeat rate on our gate traces (A34) | sidecar and cache value | Sonnet medium |
| 8 | Template-level gold-bug clusters on C2 reads (A1) | which generator slices are dropped before 2x weighting | Sonnet + Opus confirm |
