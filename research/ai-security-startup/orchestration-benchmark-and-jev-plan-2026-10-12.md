# Plan memo: benchmarking orchestration and using Jev (2026-10-12)

Sources: Memo = /Users/aryamahadik/Documents/jev/research/ai-security-startup/orchestration-cost-and-test-plan-2026-10-12.md (2026-10-12). Jev repo = /Users/aryamahadik/Documents/jev/. Memory = /Users/aryamahadik/.claude/projects/-Users-aryamahadik-Documents-jev/memory/. Figures come from the research tracks unless marked "my arithmetic" or "assumption".

## 1. Short answer

- **Benchmark:** 500 frozen extraction tasks with answers written by a script, compared in pairs against a Sonnet baseline. The memo's 150 tasks give only a go/no-go signal.
- **Time:** First version about 1 week, 11 to 20 hours of your work, about $4 in API fees. Full four-arm comparison about 2 weeks, about $12 per pass.
- **Jev:** Test it first as a verifier of yes/no claims. It is cheap, needs no training, and is Jev's strongest measured area. It cannot extract fields or plan.

## 2. Benchmark plan

- **Task sets.** 500 frozen test tasks. A 50-task dev set (different seed) for prompt fixes only. A 50-document holdout written by someone who never sees the prompts. Secondary public checks: BFCL (tool calling) and the tau2 airline subset (multi-turn policy). Skip SWE-bench Verified: OpenAI calls it contaminated (https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/, 2026-02-23).
- **Metrics.** Solve rate (all fields exact). Per-field accuracy. Failure types. Abstains (refusals) counted apart; a missing field counts as wrong. Cost per solved task: all spend, failed calls included, divided by tasks solved. p50 (median) and p95 (slow tail) latency.
- **Sample size (my arithmetic).** Paired McNemar test (only tasks where the two arms disagree count). n = (1.96 + 0.84)² × (d − Δ²) / Δ², where (2.80)² = 7.84, Δ = 0.05, and d = share of tasks where arms disagree.
  - d = 0.15: 7.84 × 0.1475 / 0.0025 = **463 tasks** (d = 0.10 gives 306; d = 0.20 gives 620).
  - "Within 5 points" (non-inferiority): 7.84 × 0.15 / 0.0025 = **470**.
  - Smallest detectable gap, √(7.84d / (n + 7.84)): 8.6 points at n = 150; 4.8 points at n = 500.
  - The memo's "±9" is the margin on the gap between two unpaired arms. One arm's 95% margin at n = 150 is ±6.4. Relabel it.
  - d and the 0.8 base rate are assumptions. Measure them in a 30-task pilot.
- **Stats and pass rules.** Paired bootstrap (resampling tasks to estimate uncertainty), 10,000 runs, as in bench/score_jevbench.py (lines 8 and 74, read 2026-10-12). Pass if within 5 points of baseline, cost per solved task is at most 20% of baseline, and script and human agree on at least 27 of 30 blind items. Prompt fixes use dev only. The memo's Day 7 fix on the same 150 tasks would taint the result. Freeze the rules in a PREREG (a frozen plan file) with the task file's sha256 (a file fingerprint).
- **Reused from JevBench.** Paired bootstrap scorer, A/B split (select on A, confirm on B), PREREG and run-once rule (Memory fair-test-pick.md, 2 Oct 2026), and scoring committed answers only.

## 3. Timeline

| Step | Estimate | Basis |
|---|---|---|
| Build generator, answer keys, grader, PREREG | 6–12 h | Assumption; no build log |
| 50-task dev set, prompt freeze | 2–4 h | Assumption |
| 5-task dry run, free models | About 1 day | 30 calls under the 50/day cap (openrouter.ai/docs/api-reference/limits, read 2026-10-12; my arithmetic) |
| Week-one API run, 150 tasks, 4 arms | About 18 min (10–30) | Assumption: 7 s per call, 8 at once |
| Week-one spend | About $4 (about $7 with reruns) | Memo section 5, 2026-10-12; tokens assumed |
| Blind check, 30 items | About 1 h | Assumption (Memo section 5) |
| Scoring and report | 2–3 h | Assumption |
| **First version** | **About 1 week; 11–20 h of your work** | Sum of rows above |
| 500-task run, 4 arms | About 1 h API time; about $12 per pass | Derived from 7 s per call; Memo prices (not re-checked) |
| Public checks (BFCL, tau2) | Not estimated | No setup source found |
| **Full comparison** | **About 2 weeks** | Assumption |
| Five arms, 1,000 tasks (only after the cheap test passes) | About 3.2 h API time; about $186 | Derived timing; Memo section 4, 2026-10-12 |

## 4. How Jev helps

Jev is hosted. It returns typed answers with probabilities, not fields or prose (Jev repo bench/jevbench/README.md, v1.4.2). In the OHS-3 test (12 Oct, opendecide-data/lean/reports/ROUND1_RESULTS.md), Jev scored 79.6% against our C1 model's 74.3%, at $0.061 against $0.433 per 1K decisions. That file says OHS-3 gives no new claim against Jev.

| Rank | Option | Cost | Time | Rule it touches | Test before training? |
|---|---|---|---|---|---|
| 1 | Verifier: Jev checks yes/no claims from the combiner | $0.042 per M input tokens (Memory jev-market-facts.md, 30 Sep); cents per 1K checks | Minutes for 200–300 gold items | Runtime use is allowed; no Jev answers in training | Yes |
| 2 | Router: fixed confidence threshold picks Jev or another model | $0 offline; about $0.12 for 2,000 live decisions (at $0.061/1K) | Hours, offline | Fixed threshold is fine; a router trained on Jev answers breaks the rule. Dropped 12 Oct; needs owner OK | Yes, offline |
| 3 | Training traces | Claude usage, no dollars | 100–200 traces graded on dev | Jev traces banned by ToS; Claude-written traces need an owner ruling | Yes |
| 4 | Planner | Paid GPU for 4B think mode | Not sized | Jev cannot plan. Think mode dropped 12 Oct | Partly; needs GPU |

**Test the verifier first.** It is the cheapest option, needs no training, and fits Jev's measured strengths: yes/no answers and calibration (how well stated probabilities match reality). OHS-3 yes/no Brier score (probability error, lower is better) was 0.150 for Jev against 0.172 for C1. Test on 200 to 300 dev items with gold answers. Measure how often it catches the combiner's errors and how often it wrongly rejects correct answers. Limits: Jev cannot replace a worker, and legal review of product use is not done.

## 5. Rules that bind this work

- Memory no-big-teachers.md (26 Sep): "Never spend money testing or using larger models (9B, 27B, 35B, etc.) as teachers or baselines." It also says "New data must never use LLM-generated datasets." **Conflict:** the plan pays for Sonnet as a baseline and V4-Pro as a worker. The owner must rule whether this rule covers a separate harness before any paid call.
- Memory train-on-modal-not-local.md (26 Sep): "Never train (or run heavy model eval) on the local M4 Mac — use Modal." Hosted API arms do not run on Modal. A self-hosted open-weight arm would.
- Memory jev-market-facts.md (30 Sep): "Never train on Jev outputs." The ToS forbids distillation.
- Memory no-jevbench-submission.md (26 Sep): no leaderboard submission until the user explicitly says so.
- Memory fair-test-pick.md (2 Oct): "Claim a win only if both agree." "Run once; never tune."
- Memory go-points-only.md (30 Sep): prompt the user for GO at paid GPU steps, OHS-3 and submissions. This pass also blocks paid API calls.

## 6. Kill criteria

Stop the orchestration if any of these hold:
1. It is more than 5 points below baseline after one dev-set prompt fix.
2. A plain cheap call matches it.
3. Even two calls per task cost more than 20% of baseline per solved task.
4. Script and human disagree on 4 or more of 30 items. Fix the grader before any claim.
5. Costs run 2x over assumptions and the 1,000-task projection passes $300.
6. Week-one spend passes $15 with no result.

Stop the Jev verifier if, on gold dev items, it does not beat the combiner's own checks with a 95% interval above zero (my proposal). Never train on Jev outputs, whatever the result.

## 7. Gaps

- Solve rates, disagreement share (0.10 to 0.20), calls and tokens are assumptions. No hosted-API latency or concurrency log exists. Fugu limits are unchecked. Build time is unlogged.
- Prices (Memo section 2) are undated and not re-checked. OpenRouter limits come from an undated FAQ. BFCL and tau2 status comes from aggregator pages.
- Jev scores conflict: 63.29 (v1.4.2 board), 72.13 (v1.5.4), 72.45 (sealed, Memory fair-test-pick.md). The 78.7 vs 63.2 claim was not found in result files.
- Jev figures come from the Jev research track. ROUND1_RESULTS.md and HANDOFF.md were not re-read here. The $0.061 per 1K method is not stated.
- Jev product use under its ToS: legal review not done.
- One track gave 8.9 and 4.9 points for n = 150 and n = 500. My arithmetic gives 8.6 and 4.8.
- Memory files are 10 to 16 days old.
