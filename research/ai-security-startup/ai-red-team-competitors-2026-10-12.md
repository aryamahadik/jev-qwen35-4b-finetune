# Competitor map: AI safety and red-teaming (as of 12 Oct 2026)

*Red teaming* means paying people to attack a system before release, so failures show up first. A *guardrail* is a filter or rule layer that blocks unsafe inputs or outputs.

## 1. Bottom line

- **Crowded and consolidating.** Six known startups were bought between July 2025 and September 2026. Buyers were security companies (Palo Alto Networks, Check Point, F5, Fortinet) and AI app firms (Harvey, Beacon).
- **Strongest independents:** Gray Swan ($40M Series A, 2026), Patronus AI ($50M Series B, June 2026), HiddenLayer ($100M Series B, Sept 2026), and Irregular ($80M, Sept 2025, works with model makers). Frontier labs test in-house and with a few government and nonprofit testers. That tier is hard to enter.
- **Where a small team fits:** testing for AI apps and agents at mid-size companies. Most funded players sell to labs or large enterprises. Buyers are still early: only 36% of security teams have a dedicated AI security budget line (small survey, 45 people).

## 2. Competitors

| Company | What it sells | Buyer | Funding or deal | Status |
|---|---|---|---|---|
| **Startups** | | | | |
| Protect AI | Model scanning, red teaming, runtime protection | Enterprise security | Bought by Palo Alto Networks, closed 22 Jul 2025 ([PANW](https://investors.paloaltonetworks.com/news-releases/news-release-details/palo-alto-networks-completes-acquisition-protect-ai/), 2025-07-22) | Acquired |
| CalypsoAI | AI guardrails, red teaming | Large enterprises | Bought by F5, announced 11 Sep 2025, $180M at announcement ([BusinessWire](https://www.businesswire.com/news/home/20250911293165/en/F5-to-Acquire-CalypsoAI-to-Bring-Advanced-AI-Guardrails-to-Large-Enterprises), 2025-09-11) | Acquired |
| Lakera | Pre-release testing, runtime guard | Enterprises | Bought by Check Point, announced 16 Sep 2025; price reported near $300M by some outlets ([Check Point](https://www.checkpoint.com/press-releases/check-point-acquires-lakera/), 2025-09-16) | Acquired; close unconfirmed |
| Virtue AI | Automated agent red teaming, guardrails | Enterprise security | Bought by Fortinet, price undisclosed ([SecurityWeek](https://www.securityweek.com/fortinet-acquires-ai-security-company-virtue-ai/), 2026-08-17) | Acquired |
| Guardrails AI | Open-source guardrail framework | AI app builders | Bought by Harvey, terms undisclosed ([Harvey](https://www.harvey.ai/blog/guardrails-ai-joins-harvey), 2026-09-09) | Acquired |
| Haize Labs | Automated LLM and agent stress tests | Not stated | Bought by Beacon, terms undisclosed ([Signalbase](https://www.trysignalbase.com/news/acquisitions/haize-labs-acquired-by-beacon-holdings-acquisition), 2026-09-18) | Acquired (medium confidence) |
| Gray Swan AI | Shade and Cygnal tools; Arena crowd testing | Frontier labs, expanding to agent builders | $40M Series A, late May 2026 ([NatLawReview](https://natlawreview.com/press-releases/gray-swan-ai-security-company-trusted-every-major-frontier-lab-raises-40m), 2026-05-28; another source says 1 Jun) | Independent |
| Patronus AI | Simulated worlds that test agents | AI developers (inferred) | $50M Series B, 25 Jun 2026 ([TechCrunch](https://techcrunch.com/2026/06/25/patronus-ai-lands-50m-to-build-digital-worlds-that-stress-test-ai-agents/), 2026-06-25) | Independent |
| HiddenLayer | Runtime security for agents | Enterprises | $100M Series B, 2 Sep 2026 ([HiddenLayer](https://www.hiddenlayer.com/news/hiddenlayer-100m-series-b-ai-security), 2026-09-02) | Independent |
| Straiker | Security for enterprise AI agents | Enterprises | $64M Series A, 29 Jun 2026 ([Straiker](https://www.straiker.ai/blog/straiker-raises-64m-series-a-to-secure-the-agentic-workforce), 2026-06-29) | Independent |
| Irregular | Simulated cyber-misuse tests | Model developers | $80M, Sept 2025 ([TechCrunch](https://techcrunch.com/2025/09/17/irregular-raises-80-million-to-secure-frontier-ai-models), 2025-09-17) | Independent |
| Mindgard | Automated AI red teaming | Not stated | $30M Series A, Aug 2026, aggregator only ([Dealroom](https://dealroom.co/news/144657-mindgard-raises-30m-series-a-to-red-team-ai-systems/), 2026-08-12) | Independent (medium) |
| Pillar Security | AI guardrails | Enterprises | Last verified: $9M seed, Apr 2025 ([Refresh Miami](https://refreshmiami.com/news/pillar-security-raises-9m-to-create-ai-security-guardrails-for-enterprises/), 2025-04) | 2026 status unknown |
| **Labs and evaluators** | | | | |
| Anthropic bounty | Paid safety-filter reports, invite-only, NDA | Own lab | Reward reportedly up to $35,000, unconfirmed ([Anthropic](https://support.claude.com/en/articles/12119250-model-safety-bug-bounty-program), 2026-09-08) | Active |
| OpenAI Bio Bug Bounty | Paid biosafety reports | Own lab | Up to $50,000, July 2026 ([OpenAI](https://openai.com/index/bio-bug-bounty), 2026-07-09) | Moving to private program |
| Google AI VRP | Bounties for AI product security flaws | Own lab | Top base reward $20,000 at launch ([The Register](https://www.theregister.com/2025/10/07/google_ai_bug_bounty/), 2025-10-07) | Active; excludes jailbreaks |
| US CAISI (NIST) | Government pre-release testing | Government | Agreements with five frontier developers ([NIST](https://www.nist.gov/node/1911491), 2026-05-05) | No vendor route found |
| UK AISI | Government testing; open-source Inspect tool | Government | Voluntary access from Anthropic, Google DeepMind, OpenAI ([CASRAI](https://casrai.org/guides/pre-deployment-testing-caisi-uk-aisi), 2026-05-08) | Public body |
| METR | Outside risk assessments of agents | Labs | Report published ([METR](https://metr.org/blog/2026-05-19-frontier-risk-report/), 2026-05-19) | Nonprofit; pay terms unknown |
| Apollo Research | Pre-release scheming tests; Watcher monitor | Labs, companies | Not found ([Apollo](https://www.apolloresearch.ai/about), undated) | Status unverified |
| **Platforms** | | | | |
| HackerOne | AI red-teaming engagements; suggested $200 to $5,000 per finding | Enterprises | Fee not found ([HackerOne](https://docs.hackerone.com/en/articles/14089281-hackerone-ai-red-teaming-airt), undated) | Established |
| Bugcrowd | Crowd testing for prompt injection, data exposure | Enterprises | Bought Mayhem Security in 2025 ([Bugcrowd](https://www.bugcrowd.com/?p=12384), 2025) | Established |
| HackAPrompt | Free, sponsor-funded contests, beginner tracks | Sponsors | Claims over $100,000 paid out ([HackAPrompt](https://hackaprompt.com), fetched 2026-10-12) | No 2026 edition found |
| Scale AI (Outlier) | Human red-teaming contractors | Frontier labs | Reported Meta 49% stake, $14.3B, June 2025, unverified ([Outlier](https://outlier.ai/about-us), 2024-08 to 2026-05) | Facts conflict |

## 3. Demand drivers

- **EU AI Act, Article 55(1):** providers of the largest general-purpose AI models must run and document adversarial testing. Duties apply from 2 Aug 2025. Models already on the market have until 2 Aug 2027 ([Article 55](https://artificialintelligenceact.eu/article/55/); [timeline](https://artificialintelligenceact.eu/implementation-timeline/)). The text does not require outside testers.
- **California SB 53:** signed 29 Sep 2025, core duties from 1 Jan 2026. It covers developers above 10^26 FLOP (a measure of training compute). They must publish a safety framework and say whether third-party evaluators were used. It does not require them ([CalMatters](https://calmatters.digitaldemocracy.org/bills/ca_202520260sb53), 2025-09-29; [FPF](https://fpf.org/blog/californias-sb-53-the-first-frontier-ai-law-explained/), 2026-01-01).
- **NIST AI 600-1 (July 2024):** voluntary guidance that recommends red teaming, per secondary summaries ([Anaconda](https://www.anaconda.com/blog/nist-ai-600-1-generative-ai-profile-guide), 2024-07).
- **Budget signals:** 54% of organizations plan to spend on AI security tools within six months, up from 43% in 2025 ([ETR](https://research.etr.ai/etr-data-drop/cybersecurity-budgets-enter-a-new-phase), Summer 2026). Only 36% have a dedicated AI security budget line ([Open Future Forum](https://openfutureforum.com/research/answers/ai-security-budgets), Aug 2026).

Most of these duties fall on a few large model makers. App builders are not clearly covered. EU high-risk rules, which may matter more to app builders, were not checked.

## 4. Gaps a small team could fill

1. **Pre-release testing for agents at mid-size app builders.** Most funded players sell to labs or large enterprises, and security budgets are rising (ETR, above). Buyer: head of engineering or security at a company shipping an AI agent.
2. **Open-source-first testing that runs in the build pipeline.** Guardrails AI was open source with over 250,000 downloads a month (Harvey's claim) before it was bought. UK AISI's Inspect is also open source. Developers adopt open tools first. This is an inference, not a confirmed buying path. Buyer: ML or platform engineers who run tests on every release.
3. **Domain test sets for regulated apps (legal, health, finance).** Harvey, a legal AI company, bought a guardrail vendor, so app firms pay to own their safety layer. This is also an inference. Buyer: product or compliance leads at AI apps in those fields.

## 5. Limits

- **Not defensible:** labs run their own red teams and bounties. No 2026 public contract with outside red-team firms was found. Acquirers buy the winners, so a small team's likely exit is a sale to a security or AI app company. Free contests like HackAPrompt set a low price for basic testing.
- **Thin data:** budget surveys are small or vendor-linked. Market-size estimates conflict ($1.75B to $2.26B for 2026; Fact.MR says $0.7B), so none are used here.
- **Unverified or conflicting:** Enkrypt AI's reported sale to Anaconda (no primary source). Lakera's closing. Protect AI's price. The Anthropic bounty date (March or September 2026) and payout. A report that OpenAI bought Promptfoo (March 2026). Cisco and SentinelOne deals. Gray Swan's claim that Anthropic uses Shade. Giskard, Adversa AI, and AIM Intelligence have no verified 2026 round. "Guardrail" (guardrail.ai, reported bought by Rain, June 2026) is a different company from Guardrails AI. Armadin ($189.9M, March 2026) uses AI attackers to test networks, not models, so it is only an adjacent comparison.
- **Source quality:** most startup facts come from press and aggregators. SB 53 penalties and incident deadlines come from secondary summaries because the bill text was blocked.
