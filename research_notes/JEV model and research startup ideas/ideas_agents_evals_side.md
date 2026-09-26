# Agents / Evals / Data / Applied-Systems Startup Ideas — Vetted Against Work Published up to 2026-09-25

Scope: ideas a student team can execute on ~$30 of Modal GPU + modest API spend, that produce publishable benchmark numbers in an under-explored space, with a sellable first customer. Model-architecture ideas are out of scope (covered by another researcher). Roughly 30 candidates were screened; 3 survive (one conditionally). Every candidate was checked against arXiv 2024–2026, GitHub/Hugging Face and web or startup coverage. Crunchbase and the YC directory were only reachable indirectly, via web search (see Gaps).

---

## Key Question 1: How crowded is the agents/evals/data idea space as of Sept 2026, and where are the real gaps?

### Takeaway
Almost every *generic* agent-reliability idea on the team's candidate list already has several 2026 arXiv papers, often with code, and usually funded startups too: early-abort predictors, tool-call verifiers, tool/MCP retrieval, skills retrieval, exactly-once and fault injection, overclaiming, handoffs, voice tool-calling, cost forecasting and cost-Pareto leaderboards. The open gaps are in **regulated verticals that have a large public record of expert decisions** (U.S. customs rulings, SEC staff comment letters). These can be turned into benchmarks where SOTA is low or no one has published a number. The other gap is **code-mixed or romanized multilingual agent evaluation**, which the new multilingual agent benchmarks skip.

### Cited Findings
- Modal's Starter plan includes "$30 / month free compute", so the team's GPU budget is exactly one month of free credits. Per-second prices: H100 $0.001097/s (~$3.95/h), A100-80GB $0.000694/s (~$2.50/h), A100-40GB $0.000583/s, L40S $0.000542/s, A10 $0.000306/s (~$1.10/h), L4 $0.000222/s (~$0.80/h), T4 $0.000164/s, B200 $0.001736/s — [Modal pricing](https://modal.com/pricing)
- Early-abort / failure prediction alone produced at least 7 papers between April and September 2026: [Doomed from the Start](https://arxiv.org/abs/2607.06503), [Fail-Fast, Restart-Smart](https://arxiv.org/pdf/2608.03222), [AgentStop](https://brave.com/research/files/AgentStop.pdf), [Atropos](https://arxiv.org/html/2604.15075), [BAGEN](https://arxiv.org/pdf/2606.00198), [Monitoring Web Agents Without Internal Signals](https://arxiv.org/pdf/2609.02057), [EarlyEval](https://arxiv.org/pdf/2609.02783)
- Tool reliability and exactly-once semantics were covered in Aug–Sept 2026 by [Limbo / "Where Does Exactly-Once Live?"](https://arxiv.org/html/2609.29095) (25,930 graded episodes) and [Verified Tool Calls Under Non-Atomic Failures](https://arxiv.org/html/2608.02645v1).
- Voice-agent tool use and entity capture are covered by [τ-voice](https://awesomepapers.io/speech-audio/papers/2603.13686), [Sierra τ³-bench](https://sierra.ai/blog/bench-advancing-agent-benchmarking-to-knowledge-and-voice) and [τ-Elicitation](https://arxiv.org/abs/2609.13602).
- Princeton's HAL already reports cost-accuracy Pareto frontiers across 9 benchmarks and 21,730 rollouts (ICLR 2026) — [HAL paper](https://arxiv.org/html/2510.11977.pdf); [HAL site](https://hal.cs.princeton.edu/)

### Inferences
- Across the ~30 screens, the survivors share one pattern: **a public corpus of expert decisions supplies ground-truth labels for free** (CBP CROSS rulings; SEC EDGAR LETTER/CORRESP files). Academics largely build simulated environments, while a startup can mine these public records. This is also the most defensible benchmark design against "someone published it last month".
- The Mem0 playbook (publish SOTA on a benchmark in your product category) maps best onto Survivor 1 (HSCodeComp/ATLAS already exist with low SOTA). Survivor 2 follows a different playbook: create the benchmark and the first number. Survivor 3 is also a create-the-benchmark play, but in a space that is filling up quickly.

### Gaps
- Crunchbase and the YC company directory were not queried directly; startup competitors come from web search, vendor blogs and HN. A final pass on Crunchbase/YC for "tariff classification", "SEC comment letter" and "Hinglish agent" is recommended before committing.
- API token prices were not verified in this session. The API cost ranges below are order-of-magnitude assumptions (roughly $0.3–$3 per million input tokens depending on tier).

---

## Key Question 2: SURVIVOR 1 — Precedent-grounded tariff (HS/HTS) classification agent, with an export-control (ECCN) benchmark extension

### Takeaway
**Pitch:** An open customs-classification agent that retrieves binding precedents from 18k+ public U.S. Customs (CBP) rulings and walks the tariff hierarchy with a small verifier model. The goal is to beat HSCodeComp's 46.8% 10-digit agent SOTA and ATLAS's 40%, then release the first public ECCN export-control classification benchmark. **Verdict: PASS.** It is not a "first implementation" (benchmarks and 2–3 research systems exist), but SOTA is roughly half of human-expert accuracy, test-time scaling is reported not to help, and no commercial vendor found publishes numbers on these benchmarks. This is the closest analog to "Mem0 on LoCoMo" found in this research.

### Cited Findings
**Benchmarks and SOTA to beat**
- HSCodeComp (Alibaba International Digital Commerce; ACL 2026) has 632 expert-annotated e-commerce products and asks for 10-digit HS codes from noisy real product descriptions. Code and dataset are released on GitHub and HF — [arXiv 2510.19631](https://arxiv.org/html/2510.19631); [ACL Anthology](https://aclanthology.org/2026.acl-long.937/)
- HSCodeComp 10-digit results: SmolAgent (GPT-5 VLM) 46.83%, SmolAgent (GPT-5 LLM) 42.72%, Aworld (GPT-5) 41.30%. Human experts reach 95.0% — [HSCodeComp](https://arxiv.org/html/2510.19631)
- HSCodeComp reports that adding human-written decision rules *decreased* accuracy for SmolAgent and WebSailor. Majority-voting test-time scaling gave "negligible" gains, and self-reflection slightly hurt (42.72% → 42.57%) — [HSCodeComp](https://arxiv.org/html/2510.19631)
- A May 2026 deterministic six-stage agentic workflow (built on Chinese tariff rules) reports on HSCodeComp: 6-digit 64.2% top-1 / 78.3% top-3 and 4-digit 75.0% / 91.5% with Qwen3.6-plus. Open-weight Qwen3.6-27B-FP8 got 84.2% 4-digit and 77.4% 6-digit top-1 "agreement". No 10-digit numbers were reported, and code release is unclear — [arXiv 2605.14857](https://arxiv.org/abs/2605.14857)
- ATLAS (Yuvraj & Devarakonda, Sept 2025) built an HTS dataset from CBP CROSS rulings. A fine-tuned LLaMA-3.3-70B reaches 40% 10-digit and 57.5% 6-digit accuracy, +15 points over GPT-5-Thinking and +27.5 over Gemini-2.5-Pro-Thinking at 10 digits, and costs ~5× less than GPT-5-Thinking. The authors say they release the dataset and model — [arXiv 2509.18400](https://arxiv.org/abs/2509.18400)
- The released CROSS-derived dataset has ~18.7k rows (18.3k train / 200 val / 200 test) — [HF: flexifyai/cross_rulings_hts_dataset_for_tariffs](https://huggingface.co/datasets/flexifyai/cross_rulings_hts_dataset_for_tariffs); [ATLAS html](https://arxiv.org/html/2509.18400)
- CROSS is CBP's official public repository of legally binding classification rulings — [data.gov CROSS](https://catalog.data.gov/dataset/cbp-customs-rulings-online-search-system-cross); [ATLAS workshop version](https://ceur-ws.org/Vol-4162/paper7.pdf)

**Why now**
- EU 2026 pressures: ICS2 requires complete electronic pre-clearance data, CBAM ties the tariff code to emissions, and removing the €150 duty exemption adds classification volume for e-commerce — [Digicust](https://digicust.com/en/blog/bulk-ai-hs-classification-at-scale-2026/)

**Commercial competitors (HS)**
- AI HS/HTS classification is offered by [Digicust](https://digicust.com/en/blog/complete-guide-hs-code-classification-2026/), [TariffLens](https://www.tarifflens.ai/blog/ai-hts-classification-guide), [iCustoms](https://www.icustoms.ai/blogs/ai-vs-manual-tariff-classification/), [Thomson Reuters](https://tax.thomsonreuters.com/blog/transform-your-trade-compliance-workflow-how-ai-eliminates-the-classification-guesswork/), [Swiss Post](https://international.post.ch/en/blog/ai-based-tariff-classification-for-e-commerce), [Camtom](https://www.camtomx.com/en/blog/how-to-use-cross-rulings-database) and [Ginger Control](https://gingercontrol.com/blog/how-to-use-cross-for-tariff-classification).

**ECCN extension (export controls)**
- ECCNs are the 5-character Commerce Control List codes that decide whether an export needs a license — [BIS: classify your item](https://www.bis.gov/licensing/classify-your-item); [Interactive CCL](https://www.bis.gov/regulations/ear/interactive-commerce-control-list)
- IAPS tested Claude Opus on example commodity-classification questions. They noted the need to benchmark "with real BIS data or more realistic item descriptions", i.e. no rigorous public ECCN benchmark exists — [IAPS](https://www.iaps.ai/research/evaluating-llm-capabilities-for-commodity-classification)
- ATLAS covers HTS only, not ECCN/export controls — [arXiv 2509.18400](https://arxiv.org/abs/2509.18400)
- Big vendors publish ECCNs for their products, which gives free labels: [Microsoft Exporting](https://www.microsoft.com/en-us/exporting/exporting-information), [IBM Export Compliance](https://www-03.ibm.com/products/exporting/). Mass-market encryption software is 5D992.c, while enterprise-only or user-modifiable encryption may stay 5D002 — [eccnfinder 5D992](https://eccnfinder.com/eccn/5d992/); [eccn.help 5A002](https://www.eccn.help/blog/encryption-export-controls-5a002-explained/)
- AI ECCN lookup tools exist ([eccnfinder](https://eccnfinder.com/eccn/5d992/), [Ginger Control ECCN guide](https://gingercontrol.com/blog/eccn-classification-export-controls)), but none was found publishing benchmark numbers.

### Inferences
**Experiment (exact):**
1. *Benchmarks:*
   - (a) HSCodeComp, all 632 items: report 2/4/6/8/10-digit accuracy on its own schedule.
   - (b) ATLAS CROSS test split, 200 rows: report 6- and 10-digit accuracy.
   - (c) A fresh "post-cutoff" CROSS test set of rulings issued in 2026, to rule out memorization of public rulings by frontier models. This doubles as an eval-contamination control.
2. *System ("precedent-grounded hierarchical classifier"):*
   - hybrid BM25 + dense retrieval over CROSS rulings;
   - a level-by-level walk down the tariff tree (chapter → heading → 6-digit subheading → national 8/10-digit), constrained to valid children at each step;
   - at each level, a small LoRA-tuned verifier (Qwen3-4B/8B trained on the ATLAS 18.3k train split) re-ranks candidates using the retrieved precedent rulings;
   - an abstain-and-flag rule when the verifier's margin is low, so accuracy-vs-coverage curves can be reported. That curve is what brokers buy.
3. *Ablations:* no retrieval; no verifier; open 8B backbone vs frontier backbone; cost per classification.
4. *ECCN-Bench v0:* scrape manufacturer-published ECCN tables (Microsoft, IBM, others) into (product description → ECCN) pairs, with the CCL text as the rule corpus. Metrics: exact ECCN, EAR99-vs-controlled, and 5x992-vs-5x002 encryption decisions.

**Numbers to beat:** 46.83% 10-digit on HSCodeComp; 64.2% 6-digit top-1 on HSCodeComp; 40% 10-digit and 57.5% 6-digit on ATLAS-test. Report cross-benchmark claims at 6 digits (see risk below).

**Cost estimate:**
- *GPU:* embedding ~18.7k rulings on an L4 takes under 30 min (<$0.50). LoRA on Qwen3-4B for ~1–2 epochs over 18.3k examples takes about 3 h on an A100-80GB (~$7.50). vLLM serving for evaluation (632 + 200 + ~200 items × ~6 calls) is about 1–2 h on an H100 (~$4–8). **Total ≈ $12–20 GPU.**
- *API:* one frontier-backbone run over ~1,000 items × 6 calls × ~5k tokens ≈ 30M input tokens ≈ **$25–100** (price assumption). Published baselines are reused rather than re-run.

**Crowdedness:** Commercially medium-crowded (at least 7 vendors). Academically light (HSCodeComp, ATLAS, one May 2026 workflow paper). None of the commercial vendors found publishes numbers on HSCodeComp or ATLAS, so a public leaderboard win is still available. ECCN has no public benchmark found, so it is a genuinely empty space.

**Main risks:**
- HS is harmonized internationally only to 6 digits; 8/10-digit codes are national. HSCodeComp comes from Alibaba e-commerce and the May 2026 follow-up used Chinese tariff rules, so U.S. CROSS precedents may not transfer beyond 6 digits.
- HSCodeComp's best system used a VLM (images), so text-only may cap accuracy.
- Liability: misclassification leads to penalties, so the product must be sold as decision support with abstention.
- Incumbents (Thomson Reuters) hold proprietary ruling and customer data.
- ECCN labels are self-classifications by manufacturers and are heavily EAR99- or 5x992-skewed.

**First customer / startup angle:** Customs brokers, 3PLs and cross-border e-commerce sellers or marketplaces (Alibaba built HSCodeComp because marketplaces need this at scale). The wedge product is a "catalog audit": upload a SKU list, get re-classifications with precedent citations and flagged duty over- or under-payment, priced per SKU. The second product is ECCN pre-screening for SaaS and hardware exporters (the encryption classification every exporting software company faces). This sells to trade-compliance teams, not AI labs.

### Gaps
- Which national 10-digit schedule HSCodeComp uses was not confirmed (important for CROSS transfer).
- Whether the ATLAS model weights and the May 2026 workflow code are actually downloadable was not verified (the abstracts claim release or partial release).
- No funding data was found for the HS-classification startups listed; the search returned no 2026 raise announcements.
- The legal usability of manufacturer ECCN tables as a redistributable dataset (terms of use) was not checked.

---

## Key Question 3: SURVIVOR 2 — "SEC staff simulator": predicting SEC comment letters before filing (new benchmark from EDGAR)

### Takeaway
**Pitch:** Read a draft S-1/F-1/10-K and predict the comments SEC staff will send, evaluated on a new public benchmark built from ~20 years of staff comment letters paired with the filings they reviewed. **Verdict: PASS (new-benchmark play).** No public benchmark or LLM system for predicting comment-letter *content* was found. Incumbents offer search and AI *over past* comment letters, not prediction with published accuracy. There is no baseline number yet, so the team would set the first one.

### Cited Findings
- EDGAR holds the full public record of SEC staff comment letters (form type LETTER) and registrant responses (CORRESP) from 2004 to the present, about 600,000 files (~18 GB) — [sec-api.io dataset description](https://sec-api.io/datasets/sec-comment-letters); [SEC: comment letters](https://www.sec.gov/answers/commentletters.htm)
- The only ML prior work found is text classification of comment letters. A Naive Bayes model signals *important* letters "up to 40 percent better than chance"; it predicts importance, not content — [Ryans (UCLA working paper)](https://www.anderson.ucla.edu/documents/areas/fac/accounting/working-papers/ryans_jmp.pdf); [PCAOB presentation](https://pcaobus.org/News/Events/Documents/10222015_CEA/SEC-Comment-Letters-Ryans.pdf)
- Existing SEC-filing LLM benchmarks test analysis, not review prediction. SECQUE has 565 expert questions on comparison, ratio calculation, risk assessment and insight generation — [SECQUE (ACL GEM 2025)](https://aclanthology.org/2025.gem-1.16/)
- Incumbent tools: Intelligize+ AI offers prior SEC comments and guidance so users can see how companies with similar comments revised filings — [Intelligize](https://www.intelligize.com/solution/public-companies/). Workiva AI covers disclosure research — [Workiva AI](https://www.workiva.com/platform/workiva-ai). Ideagen (Audit Analytics) sells a comment-letters database — [Ideagen](https://www.ideagen.com/solutions/compliance/audit-intelligence/database-modules/comment-letters). Finrep compares AI SEC-research tools — [Finrep](https://www.finrep.ai/blog/ai-tools-for-sec-filing-research-compared-2026-guide)
- Big-4 firms publish annual comment-letter trend analyses that can seed a topic taxonomy (e.g., non-GAAP, MD&A, segments) — [EY 2025 trends](https://www.ey.com/content/dam/ey-unified-site/ey-com/en-us/technical/accountinglink/documents/ey-secru28204-251us-09-11-2025.pdf); [PwC Viewpoint](https://viewpoint.pwc.com/dt/us/en/pwc/sec_comment_letters/comment_letter_trends_DM/SEC_comment_letters.html)
- Two targeted searches for LLM-based prediction or generation of SEC staff comments returned no such work — [search results incl. Ryans, PwC, Lexology](https://www.lexology.com/library/detail.aspx?g=ad97145c-6518-4d2f-913a-e869bdd94338)

### Inferences
**Experiment (exact) — "SECReviewBench":**
1. *Construction:* pull LETTER files from EDGAR. Keep first-round letters on initial registration statements (S-1/F-1) and on 10-K reviews. Link each letter to the exact filing version it reviews; letters cite form type, filing date and amendment number. Split letters into atomic numbered comments, then tag each comment with a topic (Big-4 taxonomy) and the filing section it targets.
2. *Splits:* train/dev from 2018–2024; **test = letters dated 2026 (after frontier model cutoffs)**, which gives a built-in contamination control. Target ~300 filing–letter pairs, with 100 held out.
3. *Tasks and metrics:*
   - (A) Comment prediction: comment-level recall@k and precision, matched by an LLM judge that is validated against 2 annotators on ~50 letters (report κ).
   - (B) Topic-level multi-label F1.
   - (C) Section localization accuracy.
4. *Systems:*
   - zero-shot frontier LLM;
   - RAG over historical comments from peer filings (same SIC code or same accounting issue);
   - a section-by-section reading agent plus a small LoRA topic-prior model that decides where to look.

   The headline claim would be "our agent recovers X% of actual staff comments vs Y% for the best zero-shot frontier model."

**Baseline to beat:** None published. The team establishes zero-shot frontier and RAG baselines, and the only prior ML is the importance classifier (40% better than chance).

**Cost estimate:**
- *Data:* free from EDGAR; the sec-api.io bulk dataset is an optional paid shortcut.
- *GPU:* embedding ~5 years of letters on an L4 (<$2); LoRA topic classifier on an A10 (~$1–3); open-model (e.g., Qwen3-32B) passes over 300 filings × ~150k tokens ≈ 45M prefill tokens on an H100 (~1.5–3 h ≈ $6–12). **Total ≈ $10–17 GPU.**
- *API:* frontier baseline on 100 test filings (~15M tokens) plus judge matching ≈ **$30–100** (price assumption).

**Crowdedness:** Research: empty for content prediction. Commercial: adjacent incumbents (LexisNexis Intelligize, Workiva, Ideagen) have the data and distribution but no published prediction benchmark. Moderate risk they add the feature once someone shows it works, which also makes them the acquirer.

**Main risks:**
- Label incompleteness: staff do not raise every issue, so recall has a ceiling and precision is underestimated. The LLM-judge protocol and human validation are critical.
- Linking letters to the right filing amendment is fiddly engineering.
- Securities lawyers are conservative buyers with long sales cycles.
- Liability framing: sell it as "pre-review", not advice.
- Not all 10-Ks are reviewed each year, so 10-K prediction value is lower than for IPO filings.

**First customer / startup angle:** Securities-law boutiques and IPO-readiness advisors, companies preparing S-1/F-1 filings (including foreign private issuers), and Big-4 capital-markets advisory. The product is a per-filing "pre-review report" listing likely comments with cited precedents from peer letters. The benchmark doubles as marketing: "we recover N% of real SEC comments." The later expansion is similar "regulator simulators" wherever regulator correspondence is public.

### Gaps
- SEC publication-timing policy for letters (how long after review completion they appear on EDGAR) and the availability of confidential draft registration statements (DRS) were not verified; both affect test-set construction.
- The annual volume of staff letters was not confirmed from a primary source.
- The Fin-RATE benchmark (reported as Feb 2026, Goldman Sachs & Yale, filing analysis) appeared only in a search summary; its primary source was not fetched.
- No check was made for stealth startups in legal-AI directories (Crunchbase/YC) doing SEC review prediction.

---

## Key Question 4: SURVIVOR 3 (CONDITIONAL) — Code-mixed / romanized Indic τ-style agent benchmark + small tool-calling model ("HinglishTau")

### Takeaway
**Pitch:** The first *stateful, policy-bound* customer-service agent benchmark in **romanized and code-mixed** Indic registers (Hinglish, Tanglish), with ASR-noise variants. It ships with a small open model fine-tuned on synthetic trajectories that closes most of the gap to frontier models at a fraction of the cost. **Verdict: CONDITIONAL PASS.**
- Native-script Hindi *stateful* agent evaluation is already done: Meta's OmnilingualGAIA2, Aug 2026.
- Indic *speech* tool-calling is done: Krutrim's VoiceAgentBench.
- The code-mixed and romanized, τ-style, ASR-noisy slice was not found anywhere public. Novelty is real but narrow, and the space is filling fast.

### Cited Findings
**Closest prior work (what is already covered)**
- OmnilingualGAIA2 (Meta, Aug 2026) extends the stateful GAIA2/ARE agent benchmark to ten target languages including Hindi, with data and code released. Hindi and Japanese are the weakest languages at every model size, and the English-minus-others gap widens with scale from +8.1 to +12.7 pp on a Qwen-3.5 ladder. Up to 44% of Hindi rollouts hit truncation — [arXiv 2608.08775](https://arxiv.org/pdf/2608.08775); [HF dataset](https://huggingface.co/datasets/facebook/omnilingual-gaia2). A text search of the paper found no romanized or code-mixed variants (checked by grep of the full text).
- OmnilingualGAIA2's related-work section also cites MASSIVE-Agents (multilingual function calling in 52 languages), X-WebAgentBench, PolyWorkBench and GAIA-v2-LILT — [arXiv 2608.08775](https://arxiv.org/pdf/2608.08775)
- VoiceAgentBench (Krutrim AI Labs) has 6,000+ synthetic *spoken* queries in English plus six Indic languages, covering single-tool, multi-tool, multi-turn and safety tasks. It is BFCL-style (not a stateful DB with policies), with code and data released. English ASR→LLM pipelines average 60.6% parameter-filling accuracy — [arXiv 2510.07978](https://arxiv.org/abs/2510.07978)
- Ticket-Bench covers multilingual function calling (1,020 queries) in six *European* languages; even the best models show 5+ pp gaps between languages — [arXiv 2509.14477](https://arxiv.org/abs/2509.14477)
- Adjacent Indic benchmarks that are not agentic customer service: Indi-RomCoM (romanized code-mixed instructions, June 2026) — [arXiv 2606.30790](https://arxiv.org/pdf/2606.30790); IndicDB (text-to-SQL incl. Hinglish, Apr 2026) — [arXiv 2604.13686](https://arxiv.org/html/2604.13686); Terminal-Bench-LILT (agentic coding incl. Hindi, Aug 2026) — [arXiv 2608.28641](https://arxiv.org/html/2608.28641)

**Demand signal**
- Caller Digital runs a **proprietary** Hinglish function-calling benchmark built from 1,850 turns of anonymised production voice-agent transcripts. It is not public and names no vendors because of vendor terms. Hinglish tool-selection / argument-extraction accuracy by tier:

  | Tier | Tool selection | Argument extraction |
  |---|---|---|
  | Frontier | 96.4% | 93.1% |
  | Mid | 94.1% | 89.7% |
  | Small open | 84.6% | 76.2% |
  | Indic-specialised | 92.8% | 91.4% |

  Turn-correct rates run from 66.1% for small open models to 90.2% for frontier — [Caller Digital](https://caller.digital/blog/llm-benchmark-indian-voice-agents-function-calling-latency-2026)
- Sarvam open-sourced 30B and 105B models with native tool calling; Sarvam-105B was trained on native-script, romanized and code-mixed inputs for 10 Indian languages — [Sarvam blog](https://www.sarvam.ai/blogs/sarvam-30b-105b); [summary](https://blog.buildfastwithai.com/sarvam-105b-india-s-open-source-llm-for-22-indian-languages-2026)
- The base harness to localize is τ²-bench (open source) — [sierra-research/tau2-bench](https://github.com/sierra-research/tau2-bench)

### Inferences
**Experiment (exact):**
1. Localize τ²-bench retail and telecom (plus airline if budget allows) into five registers: Hindi (Devanagari), romanized Hindi, Hinglish code-mixed, Tamil, Tanglish. Localize entities too (INR, UPI refs, Indian addresses and PNR formats), not just the language.
2. Run the user simulator in the target register. Add an ASR-noise variant by passing user turns through TTS→ASR to inject realistic transcription errors.
3. Metrics: pass^1 and pass^k (τ-bench's reliability metric), plus per-turn tool-selection and argument accuracy so results can be compared with Caller Digital's tiers.
4. Train a Qwen3-4B/8B LoRA (or a Sarvam-30B LoRA if memory allows) on ~5k synthetic code-mixed trajectories generated by a frontier teacher on *non-test* tasks.
5. Headline: "closes ≥50% of the small-vs-frontier gap at ~1/10 the per-task cost".

**Baseline:** No public stateful code-mixed number exists. The proxies are Caller Digital's 66.1% (small) vs 90.2% (frontier) turn-correct, and OmnilingualGAIA2's 8–13 pp English-vs-other gap. The team must measure the English→Hinglish drop on τ²-bench itself.

**Cost estimate:**
- *GPU:* LoRA 4B on an A100-80GB for 1–2 h (~$3–5); vLLM open-model evaluation on an H100 for 3–4 h (~$12–16). **Total ≈ $20–25, which is tight.** Subsample to 2 domains × 3 registers × 1 trial.
- *API:* translation and localization, frontier baselines and user-simulator calls ≈ **$100–250** (price assumption). This is the most API-hungry of the three survivors.

**Crowdedness:** Moderate and rising. Meta (native-script stateful), Krutrim (speech), Sarvam (models plus internal evals) and Caller Digital (private benchmark) all sit next to this.

**Main risks:**
- Meta or Sierra could add code-mixed variants quickly.
- Code-mixed data quality needs native-speaker validation, which takes team capacity.
- Indian enterprise contract values are lower.
- Sarvam could ship an equivalent benchmark with its own models.

**First customer / startup angle:** Indian voice and chat agent platforms, and BFSI or telecom enterprises deploying Hinglish agents. They need (a) model-selection audits on their own transcripts; Caller Digital's private harness shows vendors already build this in-house. They also need (b) cheap small models for latency and cost. The benchmark is the lead magnet, and the fine-tuned models and eval service are the revenue.

### Gaps
- Exact τ²-bench task counts per domain were not re-verified.
- Whether Sierra has announced multilingual τ-bench variants could not be confirmed; one search summary called multilingual a "future direction", but its primary source was unclear.
- The full language list for MASSIVE-Agents was not checked.

---

## Key Question 5: Dropped-ideas log — what was screened, why it failed, and who already did it

### Takeaway
About 29 candidates were dropped. Most of the team's suggested directions are already done or crowded as of Sept 2026: pre-execution verifiers, tool/MCP selection, agent regression testing, CUA cost and latency, cost-Pareto leaderboards, prompt-injection detection, structured extraction, voice endpointing, eval-contamination detection and vertical memory. The **early-abort "agent circuit breaker"** is the most viable fallback on the agents side: there is no commercial player and the leading hidden-state paper has not released code. It was still dropped because at least 7 papers appeared in 2026.

### Cited Findings
**Team-suggested directions**
1. **Cheap pre-execution verifiers / tool-call failure guards — DROP (done).**
   - IBM's ToolRM (1.7B–14B outcome reward models) with FC-RewardBench (1,500 BFCL-derived pairs) gives up to 25% best-of-n improvement — [arXiv 2509.11963](https://arxiv.org/abs/2509.11963)
   - A second ToolRM paper covers agentic tool-use reward modeling — [arXiv 2510.26167](https://arxiv.org/pdf/2510.26167)
   - Hidden-state tool-hallucination detectors — [arXiv 2601.05214](https://arxiv.org/pdf/2601.05214)
   - Closed-world resolver plus the Hallucinated-Tools Benchmark (Sept 2026) — [arXiv 2609.19425](https://arxiv.org/html/2609.19425); [GitHub](https://github.com/lakprigan/hallucinated-tools-toolguard)
   - Per-call authorization gate ScopeGate, which found that LangChain, LlamaIndex and the Stripe Agent Toolkit lack fail-closed per-call value authorization by default — [arXiv 2606.28679](https://arxiv.org/abs/2606.28679)
2. **Early abort / predict agent failure mid-trajectory — DROP (academically crowded; best fallback).**
   - "Doomed from the Start" (July 2026) cuts generated tokens by 60.2% on TextCraft and 54.9% on WebShop at 90% recall using hidden-state probes, on open models only. "Code will be released soon" — [arXiv 2607.06503](https://arxiv.org/abs/2607.06503)
   - Fail-Fast, Restart-Smart (SWE-bench Verified, Aug 2026) — [arXiv 2608.03222](https://arxiv.org/pdf/2608.03222)
   - AgentStop saves 15–20% energy with <5% utility drop — [Brave](https://brave.com/research/files/AgentStop.pdf)
   - BAGEN early stopping saves 28–64% of tokens on failed trajectories for −1.6 to −4.2 pp success — [arXiv 2606.00198](https://arxiv.org/pdf/2606.00198)
   - Also: [Atropos](https://arxiv.org/html/2604.15075), [black-box web-agent monitoring](https://arxiv.org/pdf/2609.02057), [EarlyEval](https://arxiv.org/pdf/2609.02783), [Trajectory Reduction](https://arxiv.org/abs/2509.23586)
3. **Tool / MCP-server selection at scale — DROP (crowded).**
   - [MCP-Zero](https://arxiv.org/html/2506.01056v2), [Tool-to-Agent Retrieval](https://arxiv.org/pdf/2511.01854)
   - The MCP Company benchmark (>18,000 tools) — [link](https://mcpmarket.com/server/the-mcp-company)
   - MCPToolBench++ (>4,000 servers) — [link](https://pith.science/paper/2508.07575)
   - [MCP-Atlas](https://arxiv.org/html/2602.00933v2), [MCP-Bench (ICLR 2026)](https://openreview.net/forum?id=fe8mzHwMxN)
   - Microsoft Foundry tool search — [link](https://commandline.microsoft.com/tool-search-toolboxes-foundry/); [MCPProxy](https://mcpproxy.app/blog/2026-03-15-beyond-bm25-tool-discovery/)
4. **Agent reliability / regression testing — DROP (commercially saturated).**
   - Maxim, Langfuse, LangSmith, Arize and Galileo lead 2026 eval-platform roundups — [Maxim roundup](https://www.getmaxim.ai/articles/top-5-ai-agent-evaluation-platforms-in-2026/); [FutureAGI roundup](https://futureagi.com/blog/ai-agent-testing-simulation-tools-2026/)
   - Mercor acquired simulation startup Deeptune in July 2026 — [Wikipedia: Mercor](https://en.wikipedia.org/wiki/Mercor)
   - Princeton's "Towards a Science of AI Agent Reliability" (Feb 2026) — [arXiv 2602.16666](https://arxiv.org/pdf/2602.16666)
5. **Cost-per-task Pareto benchmarks — DROP (done by HAL).** 9 benchmarks, 21,730 rollouts, ICLR 2026 — [HAL](https://arxiv.org/html/2510.11977.pdf)
6. **Computer-use agent cost/latency benchmark — DROP (done).** OSWorld-Human (MLSys 2026 oral, code on GitHub): top agents take 1.4–2.7× more steps than necessary — [arXiv 2506.16042](https://arxiv.org/pdf/2506.16042); [GitHub](https://github.com/WukLab/osworld-human)
7. **Prompt-injection detection for tool agents (AgentDojo) — DROP (crowded).**
   - PromptArmor reports <1% FPR/FNR on AgentDojo; PromptGuard and AgentWatcher are also reported; adaptive attacks still exceed 85% ASR — [IntelScroll May 2026](https://intelscroll.com/perimeter/prompt-injection-defense-state-of-art/)
   - Meta's LlamaFirewall — [arXiv 2505.03574](https://arxiv.org/pdf/2505.03574); AgentDojo itself — [arXiv 2406.13352](https://arxiv.org/abs/2406.13352)
8. **Structured extraction from messy documents with small models — DROP (crowded and saturated).**
   - Unsiloed leads olmOCR-Bench at 88.0 — [Unsiloed](https://www.unsiloed.ai/blog/unsiloed-ai-achieves-1-rank-on-olmocr-bench-2)
   - OmniDocBench 1.5 top score is 0.916 — [llm-stats](https://llm-stats.com/benchmarks/omnidocbench-1.5)
   - RealDocBench covers regulated forms incl. ACORD — [arXiv 2606.07401](https://arxiv.org/html/2606.07401)
9. **Voice-agent turn-taking / endpointing — DROP (done, including Hindi).**
   - LiveKit eot-bench: an open benchmark plus a dataset of real human-to-agent conversations in 14 languages — [GitHub](https://github.com/livekit/eot-bench)
   - The LiveKit turn detector supports Hindi — [docs](https://docs.livekit.io/agents/logic/turns/turn-detector/)
   - An open Hinglish turn detector exists — [GitHub](https://github.com/Mayankpratapsingh022/Turn-Detection-Model-Whisper-Tiny-Dual-Scale-Attention-Classification-Head-for-Low-Latency-Voice-AI)
10. **Eval-contamination detection — DROP (crowded research, weak buyer).** A 2026 systematic review covers 55 studies — [ACL GEM 2026](https://aclanthology.org/2026.gem-main.50/); [fragility of detection in reasoning models](https://arxiv.org/pdf/2510.02386). A contamination control is instead built into Survivors 1 and 2 through post-cutoff test sets.
11. **Agent memory for a vertical (tutoring tested) — DROP.**
    - EduClaw-Bench: a 30-day simulated learner grounded in knowledge tracing, Aug 2026 — [arXiv 2608.03206](https://arxiv.org/abs/2608.03206)
    - [LongMemEval-V2](https://arxiv.org/html/2605.12493v1); [From Recall to Forgetting](https://arxiv.org/html/2604.20006v1)
12. **Synthetic-data flywheel for a niche vertical — FOLDED INTO SURVIVORS** (CROSS rulings in #1; code-mixed trajectories in #3).

**Additional candidates generated and screened**

13. **Agent Skills retrieval (SKILL.md) — DROP.**
    - SkillsBench (87 tasks) — [alphaXiv](https://www.alphaxiv.org/abs/2602.12670)
    - [SkillRet](https://arxiv.org/pdf/2605.05726), [SkillReason](https://arxiv.org/pdf/2608.08640), [SkillRAE](https://arxiv.org/pdf/2605.10114), [Right Family, Wrong Skill](https://arxiv.org/pdf/2606.10388)
14. **Tool-description rewriting / "agent experience (AX)" audits for API providers — DROP.**
    - Trace-Free+ — [arXiv 2602.20426](https://arxiv.org/html/2602.20426)
    - AX Benchmark — [Tech Stackups](https://techstackups.com/guides/introducing-ax-benchmark-agent-experience/); Agent Readiness Index — [Tangle](https://tangle.tools/blog/agent-readiness-index-methodology/)
    - APIMatic: 96 agent-written integrations, average readiness 74 — [APIMatic](https://www.apimatic.io/blog/working-api-call-is-not-production-ready-integration); [Stainless](https://www.stainless.com/blog/steps-toward-great-agent-experience-every-api-provider-can-take-today)
15. **Pre-execution agent cost/token forecasting — DROP.**
    - Microsoft Research / Stanford (Apr 2026): 8 LLMs on SWE-bench Verified, with a consistent underestimation bias — [arXiv 2604.22750](https://arxiv.org/abs/2604.22750)
    - [Can We Predict Before Executing ML Agents?](https://arxiv.org/pdf/2601.05930)
16. **LLM-simulated tool environment fidelity — DROP.** [EnvSimBench](https://arxiv.org/html/2605.07247), [When Simulation Lies](https://arxiv.org/html/2605.11928), [ClawsBench](https://arxiv.org/pdf/2604.05172)
17. **Fault injection / idempotency / duplicate side effects — DROP.** [Limbo](https://arxiv.org/html/2609.29095), [Verified Tool Calls](https://arxiv.org/html/2608.02645v1), [ToolMisuseBench](https://arxiv.org/pdf/2604.01508)
18. **Agents falsely claiming completion — DROP.**
    - OverclaimBench: agents skip requested files in 67.9% of runs and mislead in 80.4% of those — [arXiv 2609.20812](https://arxiv.org/html/2609.20812v3)
    - [AgentLiar](https://dev.to/nilofer_tweets/agentliar-detector-catch-coding-agents-that-falsely-claim-task-completion-413c), [Corrupt Success](https://arxiv.org/html/2603.03116v1)
19. **Multi-agent handoff context loss — DROP.** [HalloffBench](https://link.springer.com/chapter/10.1007/978-3-032-31319-5_22), [MasDrift](https://arxiv.org/pdf/2608.07556), [Facts Without Rules](https://arxiv.org/pdf/2608.29028)
20. **Voice-agent tool calling / alphanumeric entity capture — DROP.**
    - τ-Elicitation (Sept 2026): 200 tasks and 10 entity types; voice configurations reach 0.14–0.41 exact success while text agents pass all tasks — [arXiv 2609.13602](https://arxiv.org/abs/2609.13602)
    - [AssemblyAI entity benchmarks](https://www.assemblyai.com/blog/voice-agent-accuracy-problem-benchmarks), [EVA-Bench](https://arxiv.org/pdf/2605.13841), [Audio2Tool](https://arxiv.org/pdf/2604.22821)
21. **Cross-provider tool-calling fidelity audit (same open model, different hosts) — DROP.**
    - Kimi Vendor Verifier — [Kimi](https://www.kimi.com/blog/kimi-vendor-verifier)
    - OpenRouter Exacto / Auto Exacto re-evaluates providers every ~5 minutes on tool-call accuracy plus TauBench and GPQA, and is on by default — [OpenRouter](https://openrouter.ai/docs/guides/routing/auto-exacto); [Exacto blog](https://openrouter.ai/blog/announcements/provider-variance-introducing-exacto/)
    - [Baseten](https://www.baseten.co/blog/tool-calling-in-inference/)
22. **Web→API reverse engineering (HAR to typed tools) — DROP.**
    - Integuru (YC W24) — [HN](https://news.ycombinator.com/item?id=41983409)
    - [reverse-api-engineer](https://reverseapi.dev/docs/)
    - Kuri / "Internal APIs Are All You Need" (Apr 2026) — [arXiv 2604.00694](https://arxiv.org/html/2604.00694)
23. **Coding-agent DB-migration safety guard — DROP (thin and product-crowded).**
    - Harness-Bench already includes a migration-safety task — [arXiv 2605.27922](https://arxiv.org/pdf/2605.27922)
    - Atlas lints destructive migrations — [Atlas](https://atlasgo.io/); PGSandbox tests agent PR migrations — [PGSandbox](https://pgsandbox.lvtd.dev/blog/database-migration-testing-agent-pr/)
24. **Healthcare prior-authorization agent benchmark — DROP.**
    - CHI-Bench (May 2026) includes 25 prior-authorization tasks — [arXiv 2605.16679](https://arxiv.org/pdf/2605.16679)
    - Appeals generation (Sept 2026) — [arXiv 2609.27844](https://arxiv.org/html/2609.27844)
    - Vendors such as [Develop Health](https://www.develophealth.ai/blog/ai-prior-authorization)
25. **B2B order entry (PO PDF→ERP / EDI) — DROP (no public benchmark found, but commercially crowded).** [Y Meadows](https://ymeadows.com/en/insights/blog/ai-order-entry-for-distributors/), [Proton.ai](https://www.proton.ai/order-and-quote-entry), [Canals](https://www.canals.ai/products/distributor-order-entry), [Ordermatic](https://ordermatic.co/)
26. **GovCon RFP compliance-matrix extraction — DROP (commercially crowded).** [Sweetspot roundup](https://www.sweetspot.so/blog/rfp-shredding-tools-government-contractors/), [GovDash](https://www.govdash.com/glossary/what-is-a-compliance-matrix), [ProposalMatrix](https://www.proposalmatrix.com/features/compliance-matrix)
27. **ERP agents — DROP.**
    - ERP-Bench: 300 Odoo tasks — [BenchmarkList](https://benchmarklist.com/benchmarks/erp_bench/)
    - [ERPBench](https://arxiv.org/abs/2609.04667), [BC-Bench](https://arxiv.org/pdf/2608.20851)
28. **Commercial-insurance submission intake (ACORD) — DROP.** [RealDocBench](https://arxiv.org/html/2606.07401); vendors [FurtherAI](https://www.furtherai.com/blog/insurance-submission-processing-platforms) and [Pibit](https://pibit.ai/blog/submission-intake-automation-commercial-p-and-c)
29. **Sanctions name-screening adjudication — DROP (saturated).** OpenSanctions Pairs (755,540 pairs): GPT-4o reaches 98.95% F1 vs a 91.33% rule-based baseline — [arXiv 2603.11051](https://arxiv.org/html/2603.11051v1)

### Inferences
- If the team insists on a *horizontal agents-infra* product, the least-bad fallback is **#2, the black-box early-abort circuit breaker for closed-API agents** with calibrated recall guarantees. It has no commercial competitor and the hidden-state approach cannot be applied to closed APIs. It would still read as "one more paper" to reviewers and investors in a 7-paper field, so it scores below the three survivors.
- **#25 (order entry)** is the one drop where *no public benchmark* was found. A team with supply-chain contacts could build "OrderEntryBench", but at least 5 funded vendors already sell the product, so the benchmark would mainly help incumbents.

### Gaps
- Code-release status was not verified for Fail-Fast, Atropos, AgentStop, BAGEN or the web-agent monitoring paper. If none has released code, the early-abort fallback is slightly stronger than rated here.
- Anthropic's own tool-search features and other lab-native tool-routing features were not re-verified this session.
- X/Twitter could not be searched directly, so recent unannounced or stealth releases may be missed.
