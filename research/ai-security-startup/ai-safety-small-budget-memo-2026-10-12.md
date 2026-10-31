# AI Safety Options Memo (12 Oct 2026)

## 1. Bottom line

- Build first: a **refusal-regression gate**, a pass/fail check that a model still refuses harmful requests after training. It reuses open tools and your Modal setup.
- Avoid prompt-injection detectors. Large vendors bought most of that market in 2025-26 [3][4].
- Only one funding program is confirmed open today: Foresight, due 31 Oct 2026 [14].

## 2. Options

| Option | What it is | Buyer | Cost to build | Time | Evidence |
|---|---|---|---|---|---|
| A. Refusal-regression gate | Pass/fail check before and after a fine-tune | Teams that fine-tune open models | Compute only: $1.19-2.03 per eval run; $4.20-6.31 per fine-tune check | 8-10 wks | Inspect 3.0k stars, MIT [5]; garak 9.5k stars, Apache-2.0 [6]. No packaged gate found |
| B. Vertical test packs for CI | Domain regression tests for AI apps | App teams in support, health, finance | Judge API cost, not verified | 6-10 wks | OpenAI bought Promptfoo, Mar 2026 [8]; Promptfoo 25.9k stars, MIT [7] |
| C. Agent-tool permission auditor | Flags over-broad agent and MCP access | Security and platform teams | Little or no compute; labor not priced | 6-10 wks | Cisco/Astrix about $400M (May 2026); CrowdStrike/SGNL $740M (Jan 2026) [4] |
| D. EU AI Act evidence pack | Logs, eval evidence, documents for one Annex III use case | EU startups in hiring or credit | Low, not priced | 8-12 wks | Annex III applies 2 Dec 2027 [1]; no buyer data found |

Left out: prompt-injection detectors (crowded) and Article 50 marking checkers. The grace period for existing generative systems ends 2 Dec 2026, 51 days away. A build started now finishes after it, so it helps only new systems [2].

## 3. Recommended harness: refusal-regression gate

Defensive only. It measures and keeps refusals. It tests only models and endpoints your team owns.

- **Tests:** refusal on harmful prompts; over-refusal on benign prompts; whether a guard model flags unsafe outputs; garak probes against your own endpoints.
- **Models:** your fine-tune (costs assume an 8B model; your own smaller models are not priced). Guard: Qwen3Guard-Gen-0.6B, Apache-2.0 [9]. Comparison models via OpenRouter: Llama 3.1 8B and Qwen 3 8B [12][13].
- **Metrics:** refusal rate, over-refusal rate, guard precision and recall, cost per run. A run fails if refusal drops below a threshold you set before running. No source gives a threshold.
- **On Modal:** Inspect runs the suite. The guard and fine-tune share one L4 at $0.80/hr [10]. Order: a $1-2 pilot to measure speed, one fine-tune with eval, then suite runs on 3 models.
- **Output:** one JSON file and one summary table per run: per-category scores, failed cases, cost, and a pass/fail verdict.
- **Judge caveat:** costs assume Claude Haiku 5.5 as judge and labeler at $0.10 in and $0.50 out per million tokens [12]. Your "no big teachers" rule may block this. Confirm first, or use a hand-labelled or small open judge (not priced).

## 4. Budget

Three scenarios from the compute track. Modal L4 at $0.80/hr; 2,000-case suite.

- **(a) Suite runs, 3 models:** $1.19-2.03 per run. $55 ÷ $2.03 = 27 and $55 ÷ $1.19 = 46, so $55 buys 27-46 runs. $100 buys 49-84.
- **(b) One 8B LoRA fine-tune, with labels and eval:** $4.20-6.31. GPU alone is 3.6-5 hr × $0.80 = $2.88-4.00. $55 buys 8-13; $100 buys 15-23.
- **(c) Weekly regression, API path:** $0.40-0.68 a week, about $21-35 a year. $55 covers 80-137 weeks; $100 covers 147-250.

Plan inside $55: $2 pilot + $6.31 fine-tune + three suite runs at $2.03 = $14.40, leaving about $40.

Risks:
- OpenRouter key: $10 limit. Last noted balance $6.58 (30 Sep, not rechecked), enough for 3-5 suite runs. Check first.
- Modal Starter: $0 base plus $30/month credit [10]. Unverified whether the credit covers GPU time. Skip the $250/month Team plan.

## 5. Funding to apply for now

- **Foresight Institute, AI for Science & Safety Nodes RFP** [14]. Deadline 31 Oct 2026, 23:59 PDT. Typical grant $30K-$100K. For-profits must explain why they need grant money. In-person work at the SF or Berlin Nodes is strongly preferred. Evaluation tools are not a named focus area.

No other program was confirmed open today (see gaps).

## 6. Gaps

- Writer pass only: no new web checks. Dates are the research tracks' fetch dates.
- The Article 50 grace date and the text of Regulation (EU) 2026/1744 come from secondary sources only [2].
- Modal's docs do not list L4 memory (24 GB) or bf16 support [11]. Throughput (30 TFLOPS, 300 tokens/s) is assumed; real runs may be 2-3x off. Running Inspect as a Modal job is untested.
- Suite size, token counts and the 8B size are assumptions. Qwen3Guard is named 0.6B, but its page shows 0.8B [9].
- OpenRouter prices come from third-party trackers and a summarized listing [12][13]. Verify on openrouter.ai.
- The compute track's $17-24 five-run figure does not match its own math (about $16-22). Not used.
- Promptfoo's deal status conflicts across sources. Lakera's price is disputed. Deal prices are press estimates.
- Buyer pain is a team hypothesis. No procurement requirement found.
- Not checked: licenses for Llama Guard, ShieldGemma and WildGuard; AgentDojo, HarmBench, JailbreakBench. UK AISI Alignment Project and Challenge Fund are closed [15]. Schmidt Sciences and OpenAI's 6 Oct 2026 deadlines have passed (aggregator sources only). Anthropic Fellows status is unclear.

## Sources

1. https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai (page updated 3 Aug 2026; fetched 12 Oct 2026)
2. https://usercentrics.com/knowledge-hub/eu-ai-act-high-risk-delay-article-50-transparency-consent/ (2026, undated; secondary)
3. https://www.securityweek.com/cybersecurity-ma-roundup-39-deals-announced-in-september-2026/ (Sep 2026)
4. https://www.calcalistech.com/ctechnews/article/dy5obf581 (Jan-Oct 2026)
5. https://github.com/UKGovernmentBEIS/inspect_ai (fetched 12 Oct 2026)
6. https://github.com/NVIDIA/garak (fetched 12 Oct 2026)
7. https://github.com/promptfoo/promptfoo (fetched 12 Oct 2026)
8. https://onmsft.com/news/openai-acquires-promptfoo-to-boost-ai-agent-security/ (9 Mar 2026)
9. https://huggingface.co/Qwen/Qwen3Guard-Gen-0.6B (fetched 12 Oct 2026)
10. https://modal.com/pricing (read 12 Oct 2026)
11. https://modal.com/docs/guide/gpu (read 12 Oct 2026)
12. https://openrouter.ai/models?order=pricing-low-to-high (listing dated 7 Oct 2026; summarized)
13. https://computeprices.com/providers/openrouter/models/llama-3-1-8b (tracker updated 4 Aug 2026)
14. https://foresight.org/grants/ai-science-safety-nodes-rfp/ (fetched 12 Oct 2026)
15. https://www.aisi.gov.uk/grants (fetched 12 Oct 2026)
