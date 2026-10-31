# Cost and test memo: cheap-model orchestration (as of 2026-10-12)

## 1. Bottom line

- **Money:** The cheapest real test costs about $4 in API fees, or about $7 with reruns. All five arms on 1,000 tasks cost about $186 at off-peak prices, or about $300 with reruns.
- **Catch:** Cheap calls add up. Under my assumptions, five DeepSeek V4-Pro calls cost about 1.4 times one Claude Sonnet 5.5 call per solved task. Orchestration (one model plans, others do the sub-steps) saves money only with a much cheaper model and two or fewer calls per task.
- **Test:** One task type, 150 fixed tasks, one frontier baseline (the best closed model), two open-weight arms (downloadable models), a script grader, and a blind human check on 30 items.

## 2. Price table

USD per 1M tokens. "Cached" means repeated input, billed at a discount.

| Model | Input | Cached | Output | Source |
|---|---|---|---|---|
| Fugu Ultra (up to 272K context) | $5 | $0.50 | $30 | S |
| Fugu Max | $2 | $0.25 | $6 | S |
| DeepSeek V4-Pro, off-peak (peak is 2x) | $0.66 | $0.022 | $1.98 | D |
| DeepSeek V4.1-Flash, off-peak (peak is 2x) | $0.15 | $0.003 | $0.60 | D |
| Claude Opus 5.5 | $4 | $0.20 | $20 | A |
| Claude Sonnet 5.5 | $2 | $0.10 | $10 | A |
| Claude Haiku 5.5 (prompts up to 100K) | $0.10 | $0.01 | $0.50 | A |
| GPT-5.6 Terra (sources conflict) | $2 | $0.25 | $12 | O |
| Kimi K3 (USD estimate) | ~$2.8 | ~$0.28 | ~$14 | K |

Sources, all read 2026-10-12:
- **S:** console.sakana.ai/pricing. Read directly. No date or currency shown; USD assumed.
- **D:** api-docs.deepseek.com/quick_start/pricing. Read directly. No date. Peak is 01:00-04:00 and 06:00-10:00 UTC, weekdays.
- **A:** platform.claude.com/docs/en/about-claude/pricing. Read directly. No date. Its $0.10 Sonnet 5.5 cache price replaces an aggregator's $0.20.
- **O:** anotherwrapper.com/llm-pricing/gpt-5.6-terra. Aggregator, dated 2026-08-20 and 2026-10-01. Another listing shows $2.50/$15.
- **K:** platform.kimi.com/docs/pricing/chat. Official, in yuan (¥20 / ¥2 / ¥100). Converted at an assumed ¥7.1 per dollar.

## 3. Cost model

**cost per solved task = [calls × (input tokens × input price + output tokens × output price) ÷ 1,000,000 + grader cost] ÷ solve rate**

Assumptions (mine, not measured):
- 2,000 input and 500 output tokens per call.
- Orchestration: 5 calls per task (planner, 3 workers, combiner). Baseline: 1 call.
- Fugu: the same 5-call token load, billed at Fugu rates.
- Grader: a script costs $0. An optional LLM judge (Haiku 5.5) adds $0.00045 per task.
- Solve rate (share of tasks answered correctly): 80% for the baseline, 75% for orchestration.
- Off-peak DeepSeek prices. No retries. No extra thinking tokens.

| Arm | Per solved task | vs baseline | 100 tasks | 300 tasks | 1,000 tasks |
|---|---|---|---|---|---|
| Sonnet 5.5, 1 call | $0.0113 | 1x | $0.90 | $2.70 | $9.00 |
| V4-Pro, 5 calls | $0.0154 | 1.4x | $1.16 | $3.47 | $11.55 |
| V4.1-Flash, 5 calls | $0.0040 | 0.36x | $0.30 | $0.90 | $3.00 |
| Fugu Max, 5 calls | $0.047 | 4.1x | $3.50 | $10.50 | $35.00 |
| Fugu Ultra, 5 calls | $0.167 | 15x | $12.50 | $37.50 | $125.00 |

The three spend columns are total API fees for one pass. The 20% target is $0.0023 per solved task. Flash at 5 calls misses it. Flash at 2 calls hits it ($0.0016).

## 4. Budget tiers

- **$0 (free only).** Buys: OpenRouter free models (50 requests a day, no purchase), Modal's $30 a month of free compute, and the free local tools Inspect AI and promptfoo. Enough for the harness, the grader, and a 20-task dry run (about 2 days). Cannot tell you: real cost, real solve rate, or the gap to the frontier. Free models are not the priced models. Sakana has no free trial.
- **About $50.** Buys: about $40 of API fees, plus an optional $10 OpenRouter top-up (1,000 free requests a day). Enough for 300 tasks on four arms (no Fugu Ultra): about $18 at one pass, about $35 with reruns. Cannot tell you: Fugu Ultra's value, or results on a second task type. The margin of error at 300 tasks is about ±6 points per arm.
- **About $300.** Buys: 1,000 tasks on all five arms, about $186 at off-peak prices (about $200 at peak), with room for reruns. Cannot tell you: production latency, user demand, or results on other tasks.

## 5. Cheapest real test

**Task type:** structured extraction (pull fields from short documents into JSON). Fields can be checked by exact match, so no LLM judge is needed. This is my pick.

**Setup**
- 150 tasks, drawn once with a fixed seed, saved, and never edited.
- Baseline: Claude Sonnet 5.5, one call per task.
- Orchestration: planner, 3 workers, combiner. Run on V4.1-Flash, then V4-Pro, off-peak only.
- Grader: a script that checks each field against the answer key.
- Human check: 30 outputs from both arms, shuffled and scored blind (about 1 hour, my estimate).

**Success (proposed; adjust as you like)**
- Solve rate within 5 points of the baseline on the same 150 tasks.
- Cost per solved task at or under 20% of the baseline's.
- Script and human agree on at least 27 of 30.

**First week**
1. Day 1: Build the task file and the grader. Cost $0.
2. Day 2: Dry-run 5 tasks on OpenRouter free models. Check the logs.
3. Day 3: Run Sonnet 5.5 on 150 tasks (about $1.35).
4. Day 4: Run V4.1-Flash orchestration (about $0.45) and one plain V4.1-Flash call per task (about $0.09). The plain call tests whether orchestration helps at all.
5. Day 5: Run V4-Pro orchestration, off-peak (about $1.73).
6. Day 6: Replace my assumed calls and tokens with real API counts. Recompute. Blind-score the 30 items.
7. Day 7: Pass, kill, or try one prompt fix. Week-one spend: about $4, or about $7 with reruns.

Optional week two: add Fugu Max on the same 150 tasks (about $5). Sakana has no free trial, so the first call is paid.

At 150 tasks, the margin of error is about ±9 points per arm. Treat week one as a go/no-go signal, not proof.

## 6. Kill criteria

Stop, or change the plan, if any of these hold:
1. Orchestration stays more than 5 points below the baseline after one prompt fix.
2. The plain cheap call matches or beats orchestration. The extra calls add cost for no gain.
3. Even 2 calls per task cost more than 20% of the baseline per solved task.
4. The script and the human disagree on 4 or more of 30 items. Fix the grader before any claim.
5. Real usage runs 2x over assumptions and the projected 1,000-task cost passes $300.
6. Week-one spend passes $15 with no result.

## 7. Gaps

- The Sakana and DeepSeek pages were read directly but are undated. DeepSeek's peak hours came from a summarized fetch.
- Not confirmed on a primary page: GPT-5.6 Terra (sources conflict), Gemini 3.1 Pro, GLM-5.3, the Kimi USD rate, and how Fugu bills its internal calls. Qwen and MiMo were omitted because their prices conflict.
- Open-weight status of the DeepSeek models was not checked.
- Long-context surcharges were checked only for Fugu.
- OpenRouter's free limits come from an undated FAQ. The free model list was not fetched.
- Solve rates, calls per task, and tokens per call are assumptions. Replace them with measured values after week one.
- Provider top-up minimums were not checked.
