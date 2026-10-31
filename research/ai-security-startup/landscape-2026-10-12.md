# AI offensive security: crowding, frontier gap, market and wedge

*As of 12 Oct 2026. Tags: V = verified; P = partly true, corrected value used; U = research only, not verified; D = disputed, kept out of headlines.*

## Bottom line

- **Viable?** As an authorized, audited testing service, yes. As an "uncensored, exploit any target" product, no. Owner permission decides legal exposure, not model settings. [Anthropic's usage policy](https://www.anthropic.com/legal/aup) bars exploiting systems without the owner's authorization (P; the page is dated 12 Nov 2026).
- **Crowded?** Very. The research named about 25 vendors. The three largest verified funding totals add to about $1.1B (my arithmetic): [XBOW $237M](https://www.securityweek.com/autonomous-offensive-security-firm-xbow-raises-120m-at-1b-valuation/) (18 Mar 2026, V), [Horizon3 $428.5M](https://siliconangle.com/2026/08/03/horizon3-ai-raises-250m-2b-plus-valuation-autonomous-pentesting/) (3 Aug 2026, V), [Armadin $445M](https://www.prnewswire.com/news-releases/armadin-raises-255-5-million-series-b-to-scale-effective-autonomous-security-302895278.html) (1 Oct 2026, V).
- **Open-weight vs Fable and Mythos:** Open models self-report 84.5 to 95.1% on [CyberGym](https://arxiv.org/abs/2506.02548), a reproduction test ([model cards, read 12 Oct 2026](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Flash-RL), V). That is at or above the Mythos entries on [BenchLM, 12 Oct 2026](https://benchlm.ai/benchmarks/cybergym) (83.1 and 83.8; the 83.8 attribution is D). These are not like-for-like. The verified gap is on exploitation. NIST's CAISI called GLM-5.3 the most cyber-capable open-weight model released to date. It scored 9.4% on ExploitGym userspace against 44.4% for the best US model ([NIST, 17 Sep 2026](https://www.nist.gov/news-events/news/2026/09/caisis-assessment-zais-glm-53-cyber-capabilities), P). No verified CyberGym score exists for Fable 5.
- **Market:** Our US bottom-up for pentest services at digital-heavy firms with 20+ staff is about $2.6B a year (range $1.4B to $4.6B). Its inputs are mostly unverified (U). The one verified global figure is [$6.68B for 2026](https://www.intelmarketresearch.com/penetration-testing-services-market-37048) (Intel, updated 5 Aug 2026, V). If AI tests at $4K to $8K replace human tests, the SMB and mid-market slice shrinks to $0.33B to $0.65B (my arithmetic).
- **Wedge:** Authorization-first testing for SMB and mid-market firms. That means signed per-target scope, audit logs, human sign-off before exploitation, and a retest after each fix. "Uncensored for any query" is a weak selling point (section 4).

## 1. How crowded

The research named about 25 vendors. That is not a full census, and no verified funding total exists for offensive-security startups. [Crunchbase](https://news.crunchbase.com/cybersecurity/seed-trends-ai-security-startup-funding-2026/) (28 Jul 2026, U) reports $10.6B for all privacy and security startups in H1 2026. Neither that nor its $855M AI-and-security seed figure is offensive-only.

| Company | What it tests | Buyer | Funding | Note |
|---|---|---|---|---|
| XBOW | Autonomous pentest of web apps and APIs | Unnamed enterprises | [$120M Series C; $237M total](https://www.securityweek.com/autonomous-offensive-security-firm-xbow-raises-120m-at-1b-valuation/), 18 Mar 2026 (V) | Top HackerOne board (self-reported) |
| Horizon3.ai (NodeZero) | Network and app pentest; attack paths | Enterprise, government | [$250M Series E; $428.5M total](https://siliconangle.com/2026/08/03/horizon3-ai-raises-250m-2b-plus-valuation-autonomous-pentesting/), 3 Aug 2026 (V) | Company says ARR up 120% (U) |
| Armadin | AI agents chain weaknesses into attack paths | Fortune 500, government (claimed) | [$255.5M Series B; $445M total](https://www.prnewswire.com/news-releases/armadin-raises-255-5-million-series-b-to-scale-effective-autonomous-security-302895278.html), 1 Oct 2026 (V) | Closest to the swarm idea |
| Aikido Attack | AppSec platform plus AI pentest | Developers, SMB to enterprise | [$60M Series B](https://fintech.global/2026/01/15/aikido-security-secures-60m-to-advance-autonomous-security/), 15 Jan 2026 (U) | Publishes $4,000 typical pentest (U) |
| RunSybil | Continuous pentest of live apps | Cursor, Notion (named) | [$40M](https://fortune.com/2026/03/18/exclusive-ai-cybersecurity-startup-runsybil-founded-by-openais-first-security-hire-raises-40-million-led-by-khosla-ventures/), 18 Mar 2026 (U) | Founded by ex-OpenAI security hire |
| Hadrian | Attack-surface mapping plus agentic pentest | McKesson, NBCUniversal (named) | [$40M Series B](https://aiweekly.co/alerts/hadrian-raises-40m-series-b-co-led-by-forgepoint-for-agentic-ai-offensive), 6 Oct 2026 (U) | Trade press only |
| Tenzai | Agentic AI pentest | Design partners in finance, health | [$75M seed](https://greylock.com/portfolio-news/introducing-tenzai-autonomous-ai-hackers/), Nov 2025 (U) | Private beta |
| Novee | Continuous testing of business-logic flaws | Cresta (only named) | [$51.5M](https://fintech.global/2026/01/16/ai-cyber-defence-firm-novee-bags-51-5m-to-counter-attacks/), Jan 2026 (U) | Builds its own model (self-claim) |
| Escape | Business-logic DAST; AI pentest | BetterHelp, PandaDoc (named) | [$18M Series A](https://escape.tech/blog/escape-raises-18m-series-a/), 10 Mar 2026 (U) | Sales-led pricing |
| Synack + NetSPI | Human plus AI pentest | Big clouds, banks, US federal | [Merger completed 5 Oct 2026](https://www.synack.com/?p=29175) (V, one source) | Combined revenue "well over $200M" |
| Pentera | Automated validation; AI red teaming | 1,100+ enterprises (aggregator, U) | Last round $60M Series D, Mar 2025 (U, no source retrieved) | Bought EVA AI red-team firm, [Nov 2025](https://pulse2.com/pentera-acquires-eva-information-security-to-expand-ai-red-teaming-capabilities) (U) |
| Strix (open source) | Self-hosted AI pentest, your own LLM key | Developers | [Repo](https://github.com/usestrix/strix); funding not verified | Apache-2.0; free substitute for DIY |
| Snyk Evo | Autonomous pentest; agent red teaming | Enterprise | [GA 4 Aug 2026](https://snyk.io/news/snyk-launches-evo-continuous-offensive-security) (U) | Incumbent entry |

**Frontier labs and incumbents.** Anthropic's Glasswing and Cyber Verification Program (CVP) gate its strongest cyber models (V). Google's Gemini 3.8 Flash Cyber is limited to trusted defenders ([Google, 2 Sep 2026](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/), V). OpenAI has Codex Security and Daybreak Red, which needs separate approval (U). Microsoft's MDASH is in limited preview (U). Palo Alto Networks sells a [Unit 42 AI validation subscription](https://www.paloaltonetworks.com/blog/2026/09/introducing-unit-42-continuous-frontier-ai-defense/), 22 Sep 2026 (U).

## 2. Frontier vs open-weight on cyber benchmarks

**What Fable and Mythos are.** Anthropic says they are the same underlying model. The difference is safeguards ([Anthropic, 9 Jun 2026](https://www.anthropic.com/news/claude-fable-5-mythos-5), V). Fable 5 is public at $10 input and $50 output per million tokens. Its flagged cyber requests route to Opus 4.8. Mythos 5 has cyber safeguards lifted. Its access is limited to Glasswing partners or to organizations verified through programs such as CVP. Two Anthropic pages describe that gate differently (P). [Mythos Preview is not planned for general release](https://www.anthropic.com/research/mythos-preview) (7 Apr 2026, V). Fable 5 and Mythos 5 were offline for all users from 12 June to 1 July 2026 after a US export-control directive ([Anthropic, 1 Jul 2026](https://www.anthropic.com/news/redeploying-fable-5), V).

**Access for a startup.** The [CVP update of 6 Oct 2026](https://www.anthropic.com/news/cyber-verification-program) has three tiers. Red Team Access is for organizations only. It covers only systems they are authorized to test (V). My inference: a student-founded company testing customers' systems would need that tier, and its eligibility is unverified.

| System | CyberGym % | Type | Source, date | Status |
|---|---|---|---|---|
| Claude Mythos 5 | 83.8 | Closed | [BenchLM](https://benchlm.ai/benchmarks/cybergym), 12 Oct 2026 | Listing V; attribution D |
| Claude Mythos Preview | 83.1 | Closed | BenchLM, 12 Oct 2026 | Listing V; no Anthropic primary |
| Fable 5 | None verified | Closed | Z.ai card lists 83.8 "with fallback" | D |
| Microsoft MDASH | 88.45 (May); 86.3 official; 95.95 any-crash | Agent system | [Microsoft, 12 May 2026](https://www.microsoft.com/en-us/security/blog/2026/05/12/defense-at-ai-speed-microsofts-new-multi-model-agentic-security-system-tops-leading-industry-benchmark/); [13 Aug 2026](https://microsoft.ai/news/introducing-mai-cyber-1-flash-inside-mdash/) | V; vendor claim |
| MiMo-V2.6-Flash | 95.1 | Open weights | [HF card](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Flash-RL), read 12 Oct 2026 | V; no harness or budget |
| DeepSeek-V4.1-Flash | 88.1 | Open weights (MIT) | [HF card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash), read 12 Oct 2026 | V; harness not stated |
| GLM-5.3 | 84.5 | Open weights | [Z.ai card](https://huggingface.co/zai-org/GLM-5.3), 14 Aug 2026 | V; setup stated |

**The verified gap.**
- *Headline test:* Open self-reports (84.5 to 95.1) are at or above the Mythos entries (83.1 to 83.8). The comparison is unfair. Harness, budget and metric differ.
- *Exploitation test:* CAISI ran GLM-5.3 and US models in one harness. US models ran with safeguards disabled where applicable (P).

| CAISI, 17 Sep 2026 | GLM-5.3 (open) | Best US | Best PRC |
|---|---|---|---|
| SEC-Bench Pro | 40.4% | 90.2% | 27.3% |
| ExploitGym userspace | 9.4% | 44.4% | 2.6% |
| ExploitBench | 61.1% | 100% | 32.2% |

That is a gap of about 35 points on ExploitGym and about 50 on SEC-Bench Pro (my arithmetic). CAISI's ExploitGym count (47 of 498) conflicts with its stated 502 tasks, so the percentages are used as printed. Berkeley's May 2026 run shows the same pattern. Mythos Preview solved 157 of 898 two-hour tasks, and the older open model GLM-5.1 solved 4, with safety filters disabled. One figure in the paper says 127 ([Berkeley RDI, 13 May 2026](https://rdi.berkeley.edu/blog/exploitgym/), P).

**Why scores are hard to compare.**
- *Harness:* Anthropic raised Opus 4.6 from 66.6 to 73.8 by changing harness settings ([Anthropic, 16 Apr 2026](https://www.anthropic.com/news/claude-opus-4-7), V).
- *Metric:* Microsoft's system scores 95.95% on an any-crash metric and 86.3% on the official final-submission metric ([Microsoft, 13 Aug 2026](https://microsoft.ai/news/introducing-mai-cyber-1-flash-inside-mdash/), V).
- *Provenance:* Most entries are self-reported. The official leaderboard could not be read (U).
- *Difficulty:* CyberGym Level 1 gives the vulnerable code and a text description. The agent must write an input that crashes the old build but not the patched one (P). The best 2025 baseline was 17.9%. Epoch AI says CyberGym is near saturation (U).

**Does removing safety settings add capability?** The only independent study found covers 16 models of 7B to 14B parameters ([arXiv, 15 Dec 2025](https://arxiv.org/abs/2512.13655)). Its math-test changes ranged from +1.5 to −18.8 points, depending on tool and model (V). I found no evidence that this adds cyber capability to large models.

## 3. Market size

- **TAM:** US pentest-services spend at digital-heavy firms (NAICS 44–45, 51, 52, 54, 62) with 20+ staff.
- **SAM:** The 20–499 staff slice a new entrant could serve.
- **SOM:** What it could win.

Bottom-up is firms × adoption × spend per buyer.

| Size band | Firms | Adoption (assumed) | Spend (assumed) | Annual |
|---|---|---|---|---|
| 20–99 | 189,907 | 30% | $10K | $570M |
| 100–499 | 41,283 | 60% | $30K | $743M |
| 500–999 | 5,398 | 85% | $60K | $275M |
| 1,000–2,499 | 3,816 | 85% | $100K | $324M |
| 2,500+ | 4,381 | 85% | $187K | $696M |

Firm counts come from [US Census SUSB 2022](https://www2.census.gov/programs-surveys/susb/tables/2022/us_state_naics_detailedsizes_2022.xlsx) (released 10 Apr 2025; U). The $187K enterprise spend comes from a [vendor-run Pentera survey](https://pentera.io/press-release/software-based-pentesting-adoption-2025/) (8 May 2025; older than 12 months). Other spend levels are assumptions from vendor price guides. Adoption rates have no source. Each 10 points of adoption moves the total by about $0.47B.

- **TAM:** $2.6B a year (range $1.4B to $4.6B). Inputs are unverified; treat as ±2x.
- **SAM:** $1.3B a year for about 81,700 buyers (range $0.5B to $2.7B). At AI test prices of $4K to $8K per year, the same buyers spend $0.33B to $0.65B. That is 25% to 50% of SAM. [XBOW's list prices](https://xbow.com/pricing) are the swing factor (U).
- **SOM (illustrative):** 500 paying customers at $20K a year is $10M, about 0.8% of SAM. The $20K figure is my assumption, not a forecast.

**Cross-check.** [Intel Market Research](https://www.intelmarketresearch.com/penetration-testing-services-market-37048) gives global pentest services at $6.20B for 2025 and $6.68B for 2026 (V). Its stated 8% growth does not match its own endpoints, which imply 5.3% to 5.6%. Other publishers range down to about $1.9B (U).

**Demand.** US CVEs (public flaw IDs) rose 20.6% in 2025, to 48,185. H1 2026 was up 49.5% ([Gamblin, 1 Jul 2026](https://jerrygamblin.com/2026/07/01/3528/), U). The [EU Cyber Resilience Act reporting duty](https://digital-strategy.ec.europa.eu/en/policies/cra-reporting) for actively exploited flaws began 11 Sep 2026 (V). It falls on manufacturers, not on all pentest buyers. PCI DSS requires pentests at least every 12 months (U).

**Headwinds.** AI report floods are closing paid bounties. [curl ended payouts](https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/) on 31 Jan 2026 (U). [Google paused product submissions to its open-source bounty](https://www.bleepingcomputer.com/news/google/google-halts-open-source-bug-bounty-program-amid-ai-spam-surge/) from 1 Oct 2026 (U). Bounty payouts are small: [$89.1M](https://www.hackerone.com/report/hacker-powered-security) for July 2025 to June 2026, about 3% of TAM (P; undated page).

## 4. Where a new entrant could win

1. **Authorized, scoped testing for SMB and mid-market firms.** These firms need evidence for PCI or SOC 2: a signed report on named assets. Price is the risk. Aikido publishes a $4,000 typical pentest, and XBOW lists $4K to $8K (U). Win on scope control and evidence, not on price.
2. **Retest and fix proof.** Buyers want proof a fix worked. GitHub's agentic autofix reruns CodeQL to confirm an alert is gone before it opens a pull request ([GitHub, 10 Jul 2026](https://github.blog/changelog/2026-07-10-agentic-autofix-for-code-scanning-alerts-in-public-preview/), U). This is crowded, but narrower than find-and-report.
3. **Exploitability evidence for manufacturers under the EU CRA.** Manufacturers must send an early warning within 24 hours and a notification within 72 hours for an actively exploited flaw (V). Inference: a tool that shows which findings are exploitable, with a record, helps them triage. Demand is unproven.

**Why "uncensored for any query" is weak.** Liability turns on owner authorization, not model settings. Provider policy bars exploiting systems without permission (P). Computer-crime laws cover unauthorized access (U). Base-model licenses bar circumventing safety measures. Meta's Llama 4 policy does (V), so such variants carry license risk. Buyers ask for controls. Vendor checklists want per-target owner authorization, enforced scope and stop conditions, audit logs of every action, human validation before delivery, no training on customer data, and SOC 2 or ISO evidence (U). I found no source requiring human approval before each exploit step. That is a practice to add, not a standard to meet. A pitch built on removing controls will fail review.

## 5. Risks, ranked

1. **Legal.** Testing a system without the owner's written permission is a crime in many places. The UK has no enacted testing defence as far as found ([ComputerWeekly, 25 May 2026](https://www.computerweekly.com/news/366650173/Government-rejects-Computer-Misuse-Act-amendment-to-protect-cyber-professionals), U). Authorized testers were arrested in 2019 over a scope dispute. Charges were dropped in January 2020 ([Krebs, 30 Jan 2020](https://krebsonsecurity.com/2020/01/iowa-prosecutors-drop-charges-against-men-hired-to-test-their-security/), U). Our product would test third parties by design, so authorization records are the core risk.
2. **Buyer rejection.** An "uncensored" pitch likely fails enterprise security reviews. This is my inference from U buyer checklists.
3. **Model access and licensing.** Frontier cyber models are gated (V). Some open licenses carry revenue thresholds. Kimi K3's model-as-a-service threshold is $20M ([license, 27 Jul 2026](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE), U). Mistral Large 4 weights are promised by end-October but not yet posted ([Mistral, 6 Oct 2026](https://mistral.ai/news/mistral-large-4/), U).
4. **Frontier API dependence.** Fable 5 and Mythos 5 were offline for all users for about three weeks (V). A product built on a hosted model inherits that outage risk.
5. **Competition from labs and incumbents.** Labs and large vendors already sell the same workflow (section 1). Strix is free and self-hosted (U). Khosla told Fortune incumbents may enter (U).

## 6. What is still unverified

- **Fable 5 CyberGym score:** none found. Anthropic's system-card PDF exceeded the fetch limit.
- **83.8 attribution:** BenchLM says Mythos 5, Z.ai's table says Fable 5 (D).
- **Leaderboard and policy text:** The official CyberGym leaderboard was not readable. OpenAI pages returned HTTP 403, so Daybreak and Codex Security terms are secondary only. The Anthropic usage policy in force today was not read; the version found takes effect 12 Nov 2026.
- **Terms and timing:** Anthropic's terms for third-party testing services were not found. CVP review is "a few weeks" on Anthropic's page, while some sources say seven business days.
- **Company facts:** Synack–NetSPI completion rests on one company page. XBOW's total is $237M or $270M (Tracxn, unverified). Strix and Penligent funding not found. Aikido's total is $84M or $85M.
- **Market inputs:** Adoption rates and spend below 2,500 staff are assumptions. Census counts were not in the verification pass. No pentest-only funding total or verified customer counts exist.
- **Law and benchmarks:** Van Buren (2021), Sandvig (2020), the DOJ 2022 policy and EU Directive 2013/40 were not verified. No 2026 open-weight Cybench, BountyBench or CVE-Bench scores were found.
- **Track failures:** OpenAI, Gartner and Fortune pages returned HTTP 403. The Hugging Face incident report was not retrieved.

## Appendix: what the fact-checkers changed

Two fact-checkers re-opened 30 claims at their sources: 21 confirmed, 8 partly true (corrected in the report), 1 disputed (kept out of headlines).

- **Corrected:** Intel Market Research states an 8% CAGR, but its own 2025 and 2034 endpoints imply about 5.3% to 5.6%. The report uses the endpoints.
- **Corrected:** Berkeley's Mythos Preview 2-hour count is 157 in Table 1 but 127 in the text and Figure 5.
- **Corrected:** The Vals Terminal-Bench 2.1 gap (Opus 5.5 ahead of Kimi K3 by 6.7 points) disappears if runs that fell back to another model count as failures. Opus 5.5 then scores 79.77, below Kimi K3's 80.90.
- **Disputed:** The claim that GLM-5.3 (84.5) matches Fable 5 (83.8). Fable's entry is labelled "with fallback" (flagged cyber requests go to Opus 4.8), the setups differ, and the same GPT-5.6 Sol score is 83.6 in one table and 84.5 in another.
- **Unresolved:** Whether the 83.8 score belongs to Fable 5 (Z.ai's table) or Mythos 5 (BenchLM).
- **Forward-dated source:** Anthropic's usage policy page shows an effective date of 12 Nov 2026, after today. The policy in force now was not read.
- **Conflict:** Cyber Verification Program review time. Anthropic's page says "a few weeks". A different track cited "seven business days", which the page does not show.
- **Single source:** The Synack and NetSPI merger completion rests on one company page.
- **Confirmed in full:** XBOW, Horizon3 and Armadin funding; Mythos Preview not generally available; CVP Red Team access limited to systems the organization is authorized to test; the CAISI GLM-5.3 figures; the EU CRA dates.
