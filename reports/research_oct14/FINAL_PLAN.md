# OpenDecide C2 (+C3): FINAL PLAN vs Jev (14 Oct 2026)

Inputs: `beat_jev_plan_opus.md`, `beat_jev_research.json`, `agentic_coding_research.json`, `HANDOFF.md` (GOAL STATUS,
C2 status), `teach1/C2_DATA_SPEC.md` (family table and cost model). The owner reviews this before any C2 change.
Amendment A42 records whatever is adopted, before any new row exists.

**Rules that do not change.**
- Never train on Jev outputs, sealed sets or eval sets. Jev results are never a selection signal.
- No bigger models: baselines are ≤ 4B. Never use data made by big models (ToolRM, FC-RewardBench, When2Call train,
  xLAM trajectories, CodeI/O).
- No data-quality gate is loosened. New families must pass every C2 kit gate plus extra probes, with at most 2 fix
  iterations; a family that still fails moves to C3.
- Training globs exclude `data/ohs3*`, `ohs3_parts/`, `ohs4_sealed/`, the new `ohs_ac_sealed/` and every public
  anchor in the never-train manifest.
- The owner gives GO before training and before every look. No JevBench submission.

---

## 1. Verdict

No mathematical guarantee of beating Jev on unseen data is possible:
- the sealed sources are unknown by design;
- Jev is hosted and drifts (50 identical requests gave 15 distinct answer sets);
- generalisation under shift rests on assumptions we cannot check before the look.

Only narrow things are provable:
- averaging views never raises Brier;
- polarity symmetrisation gives zero self-violation;
- program and execution gold is exact for the items it labels.

The strongest honest case:

**(a) Rule/agent decisions are Jev's weak spot and our strong one.**
- On dev rule/procedural rows Jev scored 71.6, C1 73.0 and Haiku 98.9.
- C2 trains 17 program-gold families there, so OHS-4 R is forecast at +5 to +6 pts.
  - P(beat Jev) ≈ 0.90; with a confidence interval (CI) ≈ 0.72 (A38 power: 78% at a true +6).
- Adding 4 new agentic families and a new sealed agentic suite gives P(CI-backed agentic-block win) ≈ 0.85.
- C2's answers are deterministic (bit-identical repeats) and Jev's are not, so pass^8 reliability is a likely win
  (≈ 0.85).
- Hijack ≈ 0.90, latency ≈ 0.82, cost ≈ 0.5.

**(b) Coding is new ground.**
- With the 2 execution-gold coding families in C2: P(CI-backed coding-block win) ≈ 0.5.
- If they slip to C3: ≈ 0.15.

**(c) General accuracy.**
- The gap was −5.3 on OHS-3, and this week's best levers recover 1-3 pts.
- Forecast: C2 − Jev ≈ −3 (range −7 to +1).
  - P(point win) ≈ 0.08; P(CI-backed win) ≈ 0.02; P(within 2 pts) ≈ 0.3.

**Overall.**

| Outcome | Probability |
|---|---|
| Pre-registered "dominates on agentic + coding" verdict | ≈ 0.3 (0.2-0.45) |
| Agentic alone | ≈ 0.55 |
| Beat Jev on every metric | ≈ 0.01 |

**Plan for:** dominate agentic, hijack and speed; a coin-flip-or-better on coding; close but behind on general.

---

## 2. Ranked actions (both studies merged)

H = Haiku, S = Sonnet, O = Opus. "C2" = before the Wed 21 Oct data cutoff; "after" = after C2 training; "C3" = next
round.

### Prerequisites (before any new row, ~$0)

**P1. A42 amendment.**
- It records every change below:
  - the row budget and replay ratio for new families;
  - the C2 cap: $40 Modal, unchanged from A39, with training ≤ $34;
  - the new-family gates and the C3 slip rule;
  - the G-block routing;
  - trap selection (changes A37 e);
  - lifting the T37b cap;
  - metadata as targets (changes A39 b), plus a sealed-side source-name check;
  - the checkpoint-average and interpolation rule;
  - the symmetrisation adoption rule;
  - the SPEED-3 cost method;
  - the G-proxy definition;
  - the OHS-AC freeze and the verdict rule.
- S drafts it; O reviews it once.

**P2. G-proxy dev** (Opus plan Action 0).
- 400-600 rows from 2-3 new official-metadata sources (via `fetch_socrata.py`).
- At least 30% card-free; yes share 40-50%.
- Plus 150 complement pairs that use negation patterns held out of training.
- Read by C1 now and by Jev once, for evaluation only.
- This is the only compass for G, because dev is blind to the sealed gap (dev 77.8 vs 78.0, sealed −5.3).
- S: 1 agent. H: a 100-row noise check. Free on od-l4.

**P3. OHS-AC sealed agentic + coding suite, verdict rule and fair-run protocol.**
- Details in section 4.
- Built git-ignored in `lean/ohs_ac_sealed/`. The "ohs" name puts it under every existing never-open rule.
- The orchestrator sees counts and hashes only.
- The programmatic part is frozen Sat 17. The surface text (H) is done Mon 19, before any training-side text.
- CPU on the laptop. S: each family agent's sealed mode plus 1 assembler. H: about 5K paraphrases.

### Ranked list

**1. Trap-mined R oversampling.** C2.
- **What:**
  - Tag every distractor with the program corruption that made it.
  - Units where C1 puts ≥ 0.25 on a trap go to the hard bin at 2×, inside the hard ≤ 30% cap.
  - Favour the trap types C1 picks most: band off-by-one 50%, boundary 39%, rename/merger 38%, unit 38%,
    not-yet-in-force 30%.
- **Metric:** R accuracy, +1 to +2.5 pts.
  - Dev upper bound +2.0 to +2.9.
  - 62% of C1's rule errors have a margin below 0.25, and gold is C1's 2nd choice in 60% of them.
- **Claude:** S × 1. **Compute:** $0.
- **Risk:** learning trap templates; OHS-4 R uses independent generators.

**2. SPEED-3 serving.** After.
- **What:**
  - $/1K at 40% of saturated throughput, measured at concurrency 64 and 128.
  - State-prefix reuse plus chunked prefill.
  - US region; headline c=1, with c=16 and c=64 also reported.
- **Metric:** cost $0.079 → $0.045-0.065, so P(cost win) goes from 0.15 to 0.5. p95 at c=1 is about 120-180 ms
  vs Jev's 301-319.
- **Claude:** S × 1 script. **Compute:** $2.
- **Risk:** throughput already saturates on long inputs.

**3. Agentic wave 1: CALL-GATE + TAINT-GATE** (section 3). C2.
- **Metric:** OHS-AC block A, hijack and over-defence, and the public BFCL-irrelevance, InjecAgent and NotInject
  anchors.
- **Expected:** +10 to +20 pts over Jev on the sealed families (estimate).
- **Evidence:**
  - Jev 71.6 on rule rows.
  - When2Call: a 4B went from 29.7 to 51.0 multiple-choice F1 with SFT and preference training.
  - Hallucinated-tool rates do not fall with size (675B ≈ 7-8B).
  - No open guard scores above 60% on NotInject over-defence.
- **Claude:**
  - S × 2: generator, oracle and tests.
  - H: about 1M output tokens (250 tool registries; a pool of about 2K documents that reuses T27's carrier pages).
  - O: 0.
- **Compute:** laptop CPU. Training cost is in the new-family line of section 6.
- **Risk:** learning the generator's grammar (the sealed split changes registry style); over-blocking (40-45% of
  rows are clean or benign).

**4. Coding families: CODE-EXEC + PATCH-VERDICT** (section 3). C2 if both pilots pass by Mon 19; otherwise the first
item in C3.
- **Metric:** OHS-AC block B, and the CRUXEval-O-MCQ and EquiBench-Py anchors.
- **Expected:** C2 65-85 vs Jev 55-75 (estimate).
- **Evidence:**
  - Qwen3-4B base scores 45.5% on CRUXEval-O.
  - Execution-trace training took a 3B from 37.5 to 68.0 (self-reported).
  - Small prompted models are near chance on equivalence (about 50%); fine-tuned small encoders reach 84-92% F1.
  - 29.6% of SWE-bench patches that pass the visible tests behave differently from the reference, so class C
    ("looks fixed but is wrong") needs hidden execution, which no prompt can see.
- **Claude:**
  - S × 2.
  - Seeds are mostly Claude-free (stdlib and permissively licensed functions; the base 4B writes modules and
    execution filters them).
  - H: about 0.8M tokens for about 800 mini-modules with tests.
- **Compute:** about 40-60 laptop core-hours ($0).
- **Risk:**
  - distractor artifacts (an options-only probe must sit at chance ±3);
  - the reformatting tell (use libcst);
  - an easy-bug skew (difficulty bins);
  - one pass cannot simulate long traces (cap complexity).

**5. Policy reliability controls.** C2 for families still in their fix iteration; otherwise sealed-only (C3 for
training).
- **What:**
  - For T28, T29, T23, T15 and T06, add only the relations each family's G4 set lacks:
    - rule-swap twins (same facts, rule flipped, gold flips): ≥ 10%;
    - rule-deleted twins (→ ask or "cannot decide"): ≥ 5%;
    - nonce-vocabulary variants: ≥ 5%.
  - Confirm that option-order and identifier randomisation is on, per epoch.
- **Metric:** strict group accuracy, pass^k, and flips per 100.
- **Evidence:**
  - Guards show "rule blindness": accuracy is unchanged when the rule is deleted or swapped.
  - Counterfactual pairs raised held-out both-correct from 30% to 98.7% (Certo, Qwen3-4B).
  - Jev flips 50.5 per 100 on adversarial option-name swaps.
- **Claude:** S × 1. **Compute:** $0.
- **Risk:** delaying the fix iteration.

**6. G-block re-weight with a C1 read** (Opus plan Action 2). C2.
- **What:**
  - C1 reads all 18.8K rows (kept plus dropped) on od-l4.
  - Rows where C1 already agrees at p ≥ 0.9: keep 35% as anchors.
  - Rows where C1 disagrees with a Haiku-accepted label go to O, kept only at ≥ 0.85.
  - Rebalance the yes share per card to 40-60%.
- **Metric:** G, +0.2 to +0.6.
- **Evidence:** where C1 ≠ Haiku, Opus is right 68%, Haiku 53% and C1 30%. Those 17% of rows hold 56% of C1's
  errors.
- **Claude:** O, 20-40 chunks. **Compute:** $0.
- **Benefit:** frees about 5K easy rows.
- **Risk:** over-weighting ambiguous rows (keep the up-weight at 1.0-1.5×).

**7. Complement scale-up, label-safe** (Opus plan Action 4). C2.
- **What:**
  - Predicate-level negation twins of gold-bearing yes/no rows: about 5K G-block, about 5K metadata, and 8-10K replay
    (counted inside the replay budget).
  - A catalogue of at least 300 negation patterns.
  - A program checks that exactly one predicate changed, and a blind H exactness check must pass at ≥ 0.9.
  - S audits 3% and drops any pattern with more than 3% error.
  - Lift the T37b 2K cap.
- **Metric:** complement violation −0.03 to −0.08; Brier −0.001 to −0.003.
- **Evidence:**
  - C1 learned its trained frames (dev 0.033) but not held-out ones (sealed 0.170).
  - LoCo-LMs: negation consistency went from 0.42 to 0.87.
- **Claude:** H about 40K reads; S audit. **Compute:** about +$3 (inside the base mix).
- **Risk:** inexact negations.

**8. Official-metadata gold block** (Opus plan Action 5). C2.
- **What:**
  - 11 S mappers (run as 3-4 agents) turn upstream human/official metadata into 40-80 tasks per source with program
    gold, giving 8-12K rows.
  - At most 200 rows per task; ≥ 30% card-free.
  - H blind noise gate: a task is dropped above 8% clearly wrong.
- **Metric:** G, +0.5 to +2.0. The evidence is task-count scaling (Super-NI, Flan) and the match to OHS-4 G's
  human/official gold type.
- **Claude:** S × 3-4; H 6-8K reads. **Compute:** inside the base mix.
- **Risk:** only 11 sources.

**9. Agentic wave 2: SEQ-CHECK + TRACE-VERIFY-real** (section 3). C2 if both pilots pass by Mon 19; otherwise C3.
- **Metric:** block A workflow and step-verification families; the ACPBench and AgentProcessBench anchors
  (exploratory).
- **Evidence:**
  - ACPBench: an 8B fine-tune went from 17.0 to 70.9 multiple-choice on unseen domains (GPT-4o 75.0).
  - RetryRealistic: 19-30% of agent runs fabricate after silent faults.
- **Claude:** S × 2; H about 0.2M tokens.
- **Compute:** laptop CPU, using only safe local tools in temp dirs.
- **Risk:**
  - one pass cannot track long plans (cap at 6 steps);
  - TRACE overlaps T33, so build only its real-tool silent-failure slice.

**10. Opus distillation at C1's errors** (Opus plan Action 7, trimmed). C2, using whatever usage is left.
- **What:**
  - H drafts cards over the G-block texts.
  - C1 reads them free; keep rows with top probability < 0.75 or margin < 0.3.
  - H labels; anything where H ≠ C1 or H confidence < 0.9 goes to O, kept at ≥ 0.85.
  - Allocation from the error slices:
    - intent/topic boundary pairs (banking77-style) by H: dev +0.8 to +1.2, the cheapest per point;
    - emotion and political taxonomies by O only, since H is no better than C1 there: dev +0.6 to +1.0.
  - Target 3-5K rows (not 5-8K), at most 150 per card.
- **Metric:** G, +0.3 to +1.0.
- **Claude:** H about 30K reads; O ≤ 150 chunks (new account if the owner opens one).
- **Risk:** the cutoff; Claude conventions are not the benchmark's conventions.

**11. Checkpoint average + C1→C2 interpolation dial.** After.
- **What:**
  - Save 6-10 checkpoints.
  - Evaluate the last-k average and the early+late average.
  - Then θ(α) = C1 + α(C2 − C1) for α in {0.5 … 1.0}.
  - Choose by a pre-registered score: G-proxy plus R mixdev plus the OHS-AC dev splits, under the D-gates and a
    paired bootstrap.
- **Metric:** G +0 to +0.8 (it guards against new families diluting G); Brier −0.001 to −0.004.
- **Claude:** S × 1. **Compute:** < $1 on od-l4.
- **Risk:** Kev's dial toward the base lost 2.9-3.9 pts, which is why this is dev-gated.

**12. Test-time polarity symmetrisation.** After; adopt only if it passes dev.
- **What:** p = ½[p(q) + 1 − p(flip q)], sharing the cached prefix.
- **Adoption bar:** complement violation falls by at least 0.02 on the G-proxy plus the held-out negation probe, with
  no accuracy or Brier loss.
- **Metric:** complement violation 0 to −0.03.
- **Compute:** +5-10% compute on yes/no items. **Risk:** the flipped view may be weaker.

**C3 queue (after C2; credit renews 1 Nov):**
- EFFECT-GATE (shell/git effect class by sandbox execution on Modal Sandbox; the largest coding-guardrail upside, but
  it needs isolation);
- POLICY-ENGINE (Cedar oracle plus policy-change review);
- HANDOFF-FSM;
- the F4 "which check goes red" family;
- scale the passing families to 20-50K rows each;
- SFT then RL with program rewards (dynamic sampling, rule-variant holdouts);
- AgentDojo and tau2 gate-in-the-loop pass^k;
- a fresh refresh sealed set (GSM1k logic);
- margin-gated rotation averaging;
- the 16-chunk Stage-0 replay-noise measurement.

---

## 3. New families: top 6, all with program or execution gold

Claude never assigns a label. The gold is computed by code, and execution must agree on 2 runs. Prompts are ≤ 800
tokens (spec 3.0 bar). Every family also passes:
- an options-only probe at chance ±3;
- a formatting-only probe at chance ±3, plus a diff-size probe for the coding families;
- a 3% reseed audit: drop the generator if more than 1% of labels flip;
- the 5% H blind re-derivation;
- G13 decontamination.

Each family follows the spec's ≤ 64 rows per card rule, so it needs ≥ 20-30 cards or specs.

| # | Family (owner area) | Decision and options | Gold | C2 rows | Sealed | Build |
|---|---|---|---|---|---|---|
| 1 | **CALL-GATE** (tool selection) | Head A: VALID / NONEXISTENT_TOOL / BAD_ARGS / TYPE_VIOLATION / OFF_MENU / BORROWED_SIGNATURE / UNGROUNDED_VALUE / AMBIGUOUS_PROVIDER. Head B: CALL / ASK_FOLLOWUP / CANNOT_ANSWER (replaces F12, never trained). Head C: edit APPLIES_ONCE / NO_MATCH / MULTIPLE / BREAKS_SYNTAX | Closed-world resolver (registry, JSON-schema); slot ledger for grounding; a real str_replace run plus `ast.parse` | 2,000 (≥ 40% valid) | 500 | 2 days, wave 1 |
| 2 | **CODE-EXEC** (coding) | Output or exception MCQ with 4-5 options and mutant distractors; equivalence head SAME / DIFFERS_TYPICAL / DIFFERS_EDGE | Hermetic run (pinned CPython, no network, `PYTHONHASHSEED=0`, 5 s cap); DIFFERS needs a witness input; SAME needs ≥ 10K fuzz cases + an edge grid + ≥ 95% branch coverage | 2,000 (1,500 output + 500 equivalence) | 900 | 2 days, wave 1 |
| 3 | **TAINT-GATE** (guardrails) | ALLOW / BLOCK_UNTRUSTED_ORIGIN / ASK_USER_CONFIRM / ALLOW_BENIGN_TRIGGER | CaMeL-style provenance engine over the generator's data-flow graph; matched pairs move one value from the user into a tool result | 1,750 (≥ 45% benign; delegation clauses) | 500 + adaptive harness | 3 days, wave 1 |
| 4 | **PATCH-VERDICT** (coding) | Line (6 numbered lines) or function (5-8) localisation, 5% "none"; patch A fixes / B does not / C passes the target test but is wrong / D does not apply | Injected libcst mutant; reverting only the gold hunk turns FAIL_TO_PASS green; pytest FAIL_TO_PASS and PASS_TO_PASS + 200 Hypothesis differential cases vs the unmutated original | 1,750 (D ≤ 5%) | 500 | 3 days, wave 2 |
| 5 | **SEQ-CHECK** (workflow routing) | INVALID / STEP_k_NOT_APPLICABLE / GOAL_NOT_REACHED / VALID; next call 1-of-4 | STRIPS-style executor + BFS over ≥ 150 random tool algebras (developer workflows plus fictional ones) | 1,250 (≤ 6 steps) | 400 | 2 days, wave 2 |
| 6 | **TRACE-VERIFY-real** (step verification) | SUCCESS / LOUD_RETRYABLE / LOUD_PERMANENT / SILENT_PARTIAL / SILENT_WRONG / NEUTRAL; next move ADVANCE / RETRY / REPAIR_ARGS / ESCALATE | Run the real step in a temp dir (pytest exit 5, push rejected to a local bare remote, curl 200 with an error body against a local server, make returning 0 after a partial build, sqlite); label = post-state diff vs the intended effect | 1,250 (≥ 35% SUCCESS) | 400 | 2-3 days, wave 2 |

**Totals:** 10,000 C2 rows and 3,200 sealed items.

**Held out for the sealed split:**
- registries and naming styles;
- idiom buckets (closures/late-binding, MRO);
- 2 mutation operators;
- 1 fault type (leave-one-fault-type-out);
- predicate vocabularies;
- plan lengths 7-8.

**Pilot gate:**
- 1,500 rows per family, one short LoRA pass.
- Keep a family only if it gains ≥ +2 pts on its own dev split and drops existing dev by no more than 0.5.
- The G-proxy must not fall by more than 0.5.

**At C3 scale,** grow the passing families to 20-50K rows each.

**Overlaps with existing C2 families.** These reuse existing assets instead of duplicating them:
- CALL-GATE head B replaces the never-trained F12;
- TAINT-GATE reuses T27's carrier documents;
- TRACE-VERIFY only adds real-tool silent failures to T33's simulator-based checks.

**Flagged by the research (owner/counsel).** Anthropic's commercial terms (D.4) restrict using Claude outputs to
train competing models. Execution and program gold keeps Claude out of the label role, but the authored text is still
output. Confirm for the plan in use.

---

## 4. The evaluation that proves domination

**OHS-AC (new, sealed, one shot, built before the training-side rows).**

| Block | Content | n | Detectable gap (ρ ≈ 0.5) |
|---|---|---|---|
| A1 agentic: existing | 17 program-gold families, rule-variant holdout, 120 base scenarios × minimal pair | 4,080 | block ≈ 1.6-2 pts |
| A2 agentic: new | CALL-GATE 500, TAINT 500, SEQ 400, TRACE 400 | 1,800 | per family ≈ 5-5.6 pts |
| B coding | CODE-EXEC 900, PATCH-VERDICT 500 | 1,400 | block ≈ 3 pts; family ≈ 5 pts |
| C1 reliability | 600 base scenarios × 8 variants (paraphrase, option order, entity/tool rename, terse/typo, irrelevant rule paragraph, fact order, rule-swap, cue inversion) | 4,800 | pass^8 ≈ 7 pts |
| C2 hijack | 500 attacked × 3 tiers (static; best-of-10 rewrite; transfer from base Qwen3.5-4B) + 500 benign trigger-word items | 2,000 | 2% vs 8% ASR |
| Real-text slice | Real public policy docs, man-page commands and package READMEs, with program gold | 200 | sign check only |
| **Total** | | **≈ 14,300** | |

**OHS-4 (frozen A38, one look):** G 2,883 / R 1,454 / U 433 / X 281 pairs / consistency 881.

**Public anchors (eval-only, hashed in the never-train manifest, 13-gram and repo/date exclusion):**
- **Gating** (part of the verdict):
  - BFCL V4 selection + irrelevance (about 3,000; pinned to `bfcl-eval` 2025.12.17; reported as "selection
    accuracy", not as an official BFCL score);
  - InjecAgent (1,054) + NotInject (339);
  - R-Judge (569);
  - CRUXEval-O as MCQ (800);
  - EquiBench Python (1,200);
  - When2Call test, if its licence is clear (otherwise exploratory).
- **Exploratory** (reported, not gating):
  - AgentProcessBench (3,000-step cluster sample);
  - ATBench-Codex;
  - ACPBench;
  - CodeJudgeBench (2,000 sample; thinking judges likely win);
  - LiveCodeBench post-cutoff execution;
  - SWE-bench Verified patch verifier (1,000).

**General accuracy:** G-proxy, ejs-5 paired and JevBench sealed, per the fair-test-pick rule. A win is claimed only if
both agree.

**Baselines (≤ 4B only):** base Qwen3.5-4B zero-shot, C1, Qwen3Guard-Gen-4B, AgentDoG-4B (licence check),
xLAM-2-3b, and a rules-only layer. A win over Jev that loses to a 4B specialist is not a headline.

**Fair run:**
- Identical text and options, with 1-2 sentence option definitions in the prompt so Jev can read our taxonomy.
- Every item in 2 option orders.
- Jev's default format is primary, plus 2 pre-registered wrappers.
- Calls are interleaved from the same region.
- Jev runs 3× on a 10% subsample. If its spread exceeds 1 pt, run the full set 3× and use the worst run.
- Errors count as wrong.
- Raw outputs are hashed.

**pass^k:**
- C2 is deterministic, so k comes from the 8 perturbations.
- Jev is also scored on identical-call stability.
- Report pass^1, pass^4 and pass^8, plus strict group accuracy on fact-flip plus rule-swap groups.

**Hijack:** ASR@1 and ASR@10, utility under attack and over-defence are always reported together. A model that
always says "ask" must not win.

**Statistics:**
- Paired by item, with a clustered bootstrap by base scenario (10K resamples).
- Holm correction across blocks and across families within a block.
- n is fixed now at ρ = 0.5 (no Jev pilot).

**Verdict rule (hashed before the look):**

| Verdict | Rule |
|---|---|
| WIN (block) | 95% CI lower bound > 0, AND point ≥ +4, AND no family's CI upper bound below −3 |
| DOMINATE | WIN on A, WIN on B, WIN on the hijack part of C, AND the real-text slice is not reversed, AND no gating anchor is significantly worse than Jev |
| General | Reported on its own as win, tie (TOST ±2 on the pooled sets) or loss; never folded into DOMINATE |

**Cost:**
- Jev calls: about 33K for OHS-AC plus about 17K for the anchors, ≈ $4-6 on OpenRouter. The spec measured 6.5K × 2
  for ≈ $0.5-1.
- Check the $10 limit first; the anchors run only if funds remain.
- C2-side inference ≈ $2 of Modal.

---

## 5. Expected C2 values vs Jev

| Metric (set, n) | Now C1 / Jev | C2 expected | P(C2 beats Jev) |
|---|---|---|---|
| G accuracy (OHS-4, 2,883) | 74.3 / 79.6 (OHS-3) | C2 − Jev ≈ −3 (−7 to +1) | 0.08 (CI-backed 0.02) |
| R accuracy (OHS-4, 1,454) | dev 73.0 / 71.6 | +5 to +6 (−2 to +12) | 0.90 (CI-backed 0.72) |
| U unseen kinds (OHS-4, 433) | — | −2 to −6 (est.; Jev's new-domain drop is −3 vs −7 to −21 for small decision models) | 0.25 (low confidence) |
| Brier yes/no: G part | 0.172 / 0.150 pooled | ≈ Jev + 0.015 | 0.12 |
| Brier yes/no: R part / pooled | — | better / near | 0.80 / 0.45 |
| Complement violation | 0.170 / 0.088 | 0.08-0.12 | 0.30 (0.40 if item 12 passes) |
| Hijack, OHS-4 X | dev 0-1.3% / — | 0-3% | 0.90 |
| p50 / p95 at c=1 | Jev 210-219 / 301-319 ms | 40-80 / 120-180 ms | 0.82 (p95 at c=64 ≈ 0.6) |
| Cost per 1K at 40% use | $0.079 / $0.061 | $0.045-0.065 | 0.50 |
| OHS-AC block A (agentic) | — / Jev ≈ 71.6 on dev rule rows | C2 85-92 vs Jev 68-78 (est.) | 0.85 (CI WIN) |
| CALL-GATE, TAINT-GATE | — | +10 to +20 each | 0.85 each |
| SEQ-CHECK, TRACE-VERIFY | — | +3 to +12 | 0.60 / 0.70 |
| pass^8 over 8 perturbations | — | C2 0.70-0.85 vs Jev 0.40-0.60 | 0.85 |
| Strict group accuracy (rule-swap) | — | — | 0.80 |
| Adaptive ASR@10 / over-defence | — | C2 5-20% / ≥ 90% correct | 0.70 / 0.60 |
| OHS-AC block B (coding) | none | C2 65-85 vs Jev 55-75 (est.) | 0.50 (0.15 if it slips to C3) |
| CODE-EXEC / PATCH-VERDICT | — | — | 0.50 / 0.65 |
| BFCL selection / irrelevance | — | parity / small edge | 0.45 / 0.60 |
| InjecAgent / NotInject / R-Judge | Jev injection 86.35% (Red Hat) | — | 0.70 / 0.55 / 0.50 |
| CRUXEval-O MCQ / EquiBench-Py | — | — | 0.40 / 0.55 |
| No gating anchor significantly worse | — | — | ≈ 0.60 |

**Combined (correlated, so these are rough):**
- OHS-4: expected about 4.4 of 8 metrics; P(≥ 5 of 8) ≈ 0.4.
- DOMINATE agentic + coding ≈ 0.3; agentic only ≈ 0.55.
- Every metric ≈ 0.01.

All Jev values on the new suites are estimates. The only measured anchors are 71.6 on dev rule rows and 71.4 on the
dev S rows.

---

## 6. Orchestration, budget and schedule

### Who does what

| Worker | Jobs | Volume |
|---|---|---|
| Programs (CPU) | All gold for the 6 families and OHS-AC; mutators, fuzzers, executors, resolvers | Laptop, $0 (safe local tools only) |
| Haiku | Surface text for the 6 families; OHS-AC paraphrases; negation twins + exactness checks; metadata wordings + noise gate; first-pass labels (item 10); 5% blind re-derivation | ≈ 3M output tokens + ≈ 80-100K item reads |
| Sonnet | Family generators and oracles (6); OHS-AC assembler, manifest, 13-gram decontamination and probes; anchor converters; trap tagging; metadata mappers (3-4); G-proxy; SPEED-3 script; 3% audits; A42 draft | ≈ 18 agents |
| Opus | Only C1-disagreement real-text labels: the G-block queue (188 chunks, already planned), item 6 (20-40), item 10 (≤ 150). Plus the A42 review and the final verdict check. Never on program-gold families | ≈ 360-380 chunks max |
| 4B models | C1 reads on od-l4; baselines ≤ 4B | Free credit |

**Usage rule:**
- Stop new work at 96% weekly; never cross 98%.
- Before the Mon 19 Oct 07:00 UTC reset, this plan uses Sonnet code and programs only, at most about 8% of the
  weekly limit (usage was 76% at 07:05 on 14 Oct).
- Haiku bulk work and Opus run after the reset, or Opus on a fresh account if the owner opens one.
- If 96% is hit, cut in this order: item 10, then wave 2, then item 8's tail.

### Modal budget (≈ $45; free accounts first; aryamhd card for training only)

| Item | $ |
|---|---|
| C2 base mix (≈ 100-110K rows incl. items 6-8 and 10) | ≤ 29 |
| New families: 10K rows + 1.0× replay (≈ 20K short rows at about $0.25/1K) | ≈ 5 |
| New-family LoRA pilot (≈ 9K rows, short pass) | ≈ 1.5 |
| C1 reads, dev gate, checkpoint average, dial, symmetrisation probe | 0 on od-l4 (fallback ≈ 5 from the reserve) |
| OHS-4 look + OHS-AC + anchors (C2 side) + ≤ 4B baselines | ≈ 4 |
| SPEED-3 | ≈ 2 |
| Reserve | ≈ 3.5 |
| **Total** | **≈ 45** |

- The C2 Modal total stays at or below A39's $40 cap.
- If the reserve falls below $2 before training, shrink wave 2 first.

### Day by day

| Day | Work |
|---|---|
| **Wed 14** | Owner reviews this plan. A42 drafted (S) and reviewed (O). Verdict rule and fair-run protocol hashed. S agents start CALL-GATE, TAINT-GATE, CODE-EXEC and trap tagging. G-proxy fetch. C1 reads the G-block (od-l4). |
| **Thu 15** | S: PATCH-VERDICT, SEQ-CHECK and TRACE-VERIFY generators; policy controls (item 5); metadata mapper code; anchor converters + never-train manifest. |
| **Fri 16** | Each family emits its sealed split first (held-out configuration, sealed agent). Wave-1 pilot rows (template text). Program gates and probes. |
| **Sat 17** | OHS-AC programmatic freeze (hash). LoRA pilot for wave 1 + coding (≈ $1). Keep/drop by the pilot gate. |
| **Sun 18** | Wave-2 pilot (≈ $0.5). Complement pattern catalogue and twin program ready. Trap selection coded. Token count of the mix. Usage check. |
| **Mon 19** (reset 07:00 UTC) | H: OHS-AC surface text → final OHS-AC hash recorded. Then H training-side text for the passing families, complement twins, metadata wordings + noise gate, item-10 first pass. O: G-block queue + item 6. |
| **Tue 20** | O: item-10 escalations (to the usage cap). S: 3% audits. Full generation of the passing families (anything not passing moves to C3). Decontamination against the OHS-4 exports (counts only), OHS-AC and the anchors. Mix, G13, gates. |
| **Wed 21** | Data cutoff (A39). Owner GO, then train C2 (≤ $34 of training, relayed mahadikarya2 → 3, 6-10 checkpoints). |
| **Thu 22** | Dev gate; checkpoint average + interpolation dial; symmetrisation probe; freeze the candidate. |
| **Fri 23** | Owner GO, then the OHS-4 look (L1, then J), OHS-AC (C2 + Jev + baselines), then SPEED-3 (US region, c = 1/16/64/128). |
| **Sat 24** | Gating anchors, only if the OHS-AC block lower bound is above 0. Final report with the pre-registered verdict. Update HANDOFF. |

This moves the HANDOFF ETA from "train Sat 17-Sun 18, final Mon 19-Tue 20" to "train Wed 21, final Fri 23-Sat 24".
The 9,368-item G-block Opus queue could never run before Mon 19 anyway.

---

## 7. What to STOP

| Stop | Why |
|---|---|
| Calibration work: per-type temperature, label smoothing, Brier or focal losses | The Brier gap is an accuracy gap (T ≈ 1.0; −0.0054 Brier per pt) |
| Bulk label-cleaning passes and replay noise filtering | 0-0.3 pt ceiling; C1 already follows the teacher consensus. The existing gates stay as they are |
| More Haiku-labelled easy G rows | C1 is already 94-99% right where the teachers agree confidently; little gradient |
| Depth beyond 64 rows per card, and more replay from the same generators | Per-task gains saturate (Super-NI, Flan); Kev saw +26 pts, then only +5 pts from the next 12K rows |
| Design-size families (40-70K rows each) and Docker SWE-smith Tier B in C2 | Over budget; pilot size first, scale in C3 |
| F5 SemVer, HANDOFF-FSM and PLAN-FEASIBLE in C2 | Largest Claude cost, least proven, or a solver already does it |
| Seed soups, full 4-rotation test-time averaging, selective thinking in the headline | Budget; doubles cost per call; risks p95 |
| End-to-end multi-turn agent benchmarks (BFCL multi-turn, AgentDojo/tau2 loops, LiveMCPBench) before single-decision wins | Non-deterministic or costly; C3 at the earliest |
| Using Claude as the label for coding or agentic rows | Program and execution gold only |
| Judging G on the old dev | Dev is blind to the sealed gap; use the G-proxy |
| Any data from big models, Jev outputs, eval sets or OHS paths; JevBench submission | Project rules |
