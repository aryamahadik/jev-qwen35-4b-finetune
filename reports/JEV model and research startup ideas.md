# Beat Jev on Calibration, Latency and Openness

Jev is TypeSafe AI's proprietary "System One" model, launched on 15 September 2026 alongside a $40M DCVC-led seed round. It takes text or JSON state plus typed questions and returns probabilities over declared options (yes/no, a choice, or a score) in one parallel pass. It does this at roughly 100 ms per API call and $0.042 per million input tokens, and TypeSafe has disclosed no weights, paper, parameter count or architecture. Independent tests confirm the speed and cost gains but show that accuracy depends on how the question is asked. Jev matches or beats small LLMs when a task is split into narrow questions, falls apart on single catch-all or implicit-rule questions, is measurably miscalibrated (expected calibration error 0.107), and lost topic classification by 12 points to a fine-tuned 310M-parameter encoder. **With about $30 the team cannot build an open model that beats Jev zero-shot across arbitrary questions.** An open Qwen3-4B reproduction still trails it, and "open Jev alternative" is already crowded by Laya, several OpenJev repositories and GLiClass. **The team can win a narrower claim.** The model would be an Apache-2.0 encoder under 400M parameters that answers Jev's three question types, fills tool-call arguments in the same forward pass, runs locally in tens of milliseconds, is better calibrated than Jev, and beats it on public tasks after training on a few hundred labels. It would be released with the first reproducible benchmark that includes Jev. The project needs about $15–25 of GPU time and uses a window that opened ten days ago, so it ranks first of six vetted ideas. A precedent-grounded tariff and export-control classifier ranks second because it has the clearest first customer. After it come a tiny recursive model for spreadsheets, SEC comment-letter prediction, a tiny recursive string-transform model, and a benchmark for agents working in mixed Hindi-English or Tamil-English ("code-mixed").

## Jev sells typed probabilities through a closed, ~100 ms API

### What Jev is and who built it

Jev is the first "System One Model" from TypeSafe AI. The launch blog describes it as "a frontier-intelligence function call: unstructured state in, typed probabilistic decisions out", and names the new model class after Kahneman's fast, intuitive System 1 ([TypeSafe blog](https://typesafe.ai/blog/introducing-system-one-models-and-jev)). The company was founded in 2024 by **Diogo Almeida** (CEO, formerly at OpenAI and a co-author of InstructGPT), **Erik Gafni** (CTO) and **Sasha Sheng** (COO). It came out of stealth with a **$40M seed led by DCVC** ([HPCwire/AIwire](https://www.hpcwire.com/aiwire/2026/09/16/typesafe-ai-emerges-from-stealth-with-40m-in-funding-with-new-model-for-composable-ai/)). A Forbes headline puts the valuation at $200M, but the article body could not be read ([Forbes](https://www.forbes.com/sites/the-prompt/2026/09/15/this-200-million-startup-wants-to-fix-ais-overconfidence-problem/)).

Distribution is strong. Jev reached **13% of Vercel AI Gateway paid teams within 24 hours**, which Vercel called the fastest adoption in the gateway's history, while noting that "the next test is whether that early adoption lasts" ([Vercel](https://vercel.com/blog/ai-gateway-jev-model-launch)). Pydantic AI and LangChain both ship integrations ([Pydantic](https://pydantic.dev/docs/ai/models/typesafe/)), and the Hacker News launch post drew 1,655 points ([Firecrawl](https://www.firecrawl.dev/blog/what-is-jev)). Pricing is **$0.042 per million input tokens, with output free** ([TypeSafe models doc](https://docs.typesafe.ai/models.md)).

### Three question types, answered in parallel

Jev answers only three kinds of question.

| Question type | What it answers | What it returns |
|---|---|---|
| **Noul** | Yes/no | A probability from 0 to 1 |
| **Choice** | Pick one of up to 255 declared options | The chosen option and the full distribution |
| **Score** | A position on a scale of 2 to 10 levels | The expected level and the distribution |

Sources: [flaviocopes](https://flaviocopes.com/jev/), [TypeSafe docs](https://docs.typesafe.ai/).

The questions sent in one call "are evaluated in parallel and isolation", and "adding questions barely changes the response time" ([TypeSafe docs](https://docs.typesafe.ai/)). The current model, `jev-1.13.0`, accepts **64k tokens per request, of which 32k covers the state plus the longest question**. It takes text only and is strongest in English. It also cannot be customized beyond the `state`, `instructions` and `criteria` fields, because "same weights serve every account" and fine-tuning is not offered ([TypeSafe models doc](https://docs.typesafe.ai/models.md)).

### TypeSafe discloses almost nothing about the internals

TypeSafe says only that it built "a new architecture, a new sampler, and a new training algorithm: Reinforcement Learning for Calibrated Decisions (RLCD)" ([typesafe.ai](https://typesafe.ai/)). On Hacker News, a TypeSafe-affiliated account added that the architecture is proprietary, that a paper "may" follow, and that RLCD probabilities are optimized "against outcomes" ([HN thread](https://news.ycombinator.com/item?id=49717558)). Commentators guess it is a "stripped down diffusion language model" or a "constrained or diffusion-like decision model" built over "2 years in stealth" ([Latent Space](https://www.latent.space/p/ainews-jev-a-system-one-model-that)). One analysis sums up the disclosure as "Nothing about size, architecture, pretraining data" ([pearpages](https://pearpages.com/blog/2026/09/16/jev-sorted-what-typesafes-system-one-model-actually-is-and-what-is-still-just-a-claim)).

The simplest reading of the interface is a transformer that encodes the state once and reads a distribution over the declared options, using either a small output head or the model's own scores for each option (its "logits"). That is exactly how the community OpenJev reproductions work on Qwen ([zhihz/openjev](https://github.com/zhihz/openjev)). This is inference, not disclosure.

### Independent tests confirm the speed and qualify the accuracy

TypeSafe claims **70–500 ms end to end, mostly around 100 ms**. On its own workflow evaluations it claims Jev is **193.6x faster and 444.6x cheaper** than GPT-6 Astra and Claude Fable 5.1. It concedes these figures are "on the higher end of real world gains", and that because its own staff built the evaluations, "some bias could exist" ([TypeSafe blog](https://typesafe.ai/blog/introducing-system-one-models-and-jev)).

The accuracy figure behind those claims measures *agreement with the frontier models*, not accuracy against ground truth. It averages about **67.8%** across four in-house workflows, from 61.8% on Invoice Processing to 76.0% on Customer Service ([pearpages](https://pearpages.com/blog/2026/09/16/jev-sorted-what-typesafes-system-one-model-actually-is-and-what-is-still-just-a-claim)). One reviewer put it bluntly: the cost multiple measures "how cheaply Jev agrees with frontier LLMs, not how often Jev is right" ([Beri.net](https://www.beri.net/article/typesafe-jev-typed-decision-model-calibration-decomposition-shadow-eval)). Against the more comparable GPT-5.6 Terra, the advantage shrinks to **25x faster and 76x cheaper** ([pearpages](https://pearpages.com/blog/2026/09/16/jev-sorted-what-typesafes-system-one-model-actually-is-and-what-is-still-just-a-claim)).

The table below collects the independent results.

| Independent test | Jev | Comparison | What it shows | Source |
|---|---|---|---|---|
| Every: four writing checks on 12 passages | 6 of 7 planted defects; 0.35 s median | Fable 5.1: 7 of 7; 8.83 s; ~580x the cost | Near-frontier on narrow checks at a tiny fraction of the cost | [Firecrawl](https://www.firecrawl.dev/blog/what-is-jev) |
| Phishing, 2,000 emails, one broad question | 62.6% | Claude Haiku: 81.3% | Catch-all questions fail | [Beri.net](https://www.beri.net/article/typesafe-jev-typed-decision-model-calibration-decomposition-shadow-eval) |
| Same emails, five narrow questions combined by a logistic regression trained on 1,000 labels | 95.0% | $0.038 vs $0.462–$1.02 per 1,000 emails | Splitting the task up and combining answers in code fixes it | [Beri.net](https://www.beri.net/article/typesafe-jev-typed-decision-model-calibration-decomposition-shadow-eval) |
| Claim verification, 108 claims | 96.3%; Brier score 0.0331 | Gemini 3.1 Flash Lite 94.4%; Haiku 4.5 93.5% | Strong on bounded judgment, but a small sample | [BuildFastWithAI](https://blog.buildfastwithai.com/jev-ai-review) |
| Japanese classification, 3 tasks × 250 rows | 76.8 / 94.4 / 74.0 | Fine-tuned 310M ModernBERT-ja: 88.8 / 92.8 / 75.2 | A trained encoder wins topic classification by 12 points (p=0.00007); the other two are ties | [DEV Community](https://dev.to/ikkun1222/jev-vs-a-310m-encoder-i-trained-myself-750-rows-three-tasks-two-different-winners-242e) |
| Calibration, synthetic tickets | Expected calibration error 0.107 (noise floor 0.024) | — | Yes/no answers underconfident; Choice and Score overconfident | [Beri.net](https://www.beri.net/article/typesafe-jev-typed-decision-model-calibration-decomposition-shadow-eval) |
| Priority question whose rule was not in the text | 44.7% correct | Average stated probability 0.74 | Confidently wrong | [Beri.net](https://www.beri.net/article/typesafe-jev-typed-decision-model-calibration-decomposition-shadow-eval) |
| Latency outside the US | About 430 ms floor from Europe; 1.9–2.4 s per item from the Japanese tester's location | Local encoder: 0.10–0.45 s | Hosting in one US region erodes the speed advantage abroad | [Beri.net](https://www.beri.net/article/typesafe-jev-typed-decision-model-calibration-decomposition-shadow-eval), [DEV](https://dev.to/ikkun1222/jev-vs-a-310m-encoder-i-trained-myself-750-rows-three-tasks-two-different-winners-242e) |
| Laya comparison (secondary source) | Median (p50) latency 236–276 ms; score 0.727 | Laya: 32.8 ms on a T4 GPU; fine-tuned score 0.766 | A small local model is faster and edges ahead once fine-tuned | [BestHub](https://www.besthub.dev/articles/open-source-decision-model-laya-vs-jev-speed-wins-zero-shot-fails-befced0a2228) |
| OpenJev reproduction, 102 cases | Agreement 0.883 | Qwen3-4B: 0.845 | An open 4B model has not yet matched Jev zero-shot | [Firecrawl](https://www.firecrawl.dev/blog/what-is-jev) |

The results tell a consistent story. Compared with reasoning LLMs, Jev has at least a tenfold cost and latency advantage on bounded decisions. Its accuracy is roughly that of a small or mid-tier LLM when the questions are well split up, and it drops sharply on catch-all or implicit-rule questions. The 62.6% versus 95.0% phishing gap shows that much of the "intelligence" moves to the developer, who must design the questions and combine the answers in code.

The largest gap is evidence. TypeSafe publishes **no results on standard benchmarks**: none on BFCL (the Berkeley Function Calling Leaderboard), CLINC150, Banking77 or any routing benchmark. It also publishes "no calibration curves, no Brier scores and no reliability diagrams" ([pearpages](https://pearpages.com/blog/2026/09/16/jev-sorted-what-typesafes-system-one-model-actually-is-and-what-is-still-just-a-claim)). Hacker News commenters asked outright for real benchmarks ([HN thread](https://news.ycombinator.com/item?id=49717558)).

### Jev's gaps are built into the design, not first-version bugs

TypeSafe's own page of known weaknesses for jev-1.13 lists **9 failure modes** ([TypeSafe docs](https://docs.typesafe.ai/model-jaggedness/jev-1.13)). They are literal reading; math and numbers (including counting and numeric formats such as hex and RGB); date and time comparison; indirection such as double negatives and multi-hop questions; large state full of irrelevant detail; adversarial content; contradictory instructions and criteria; common-sense structural invariants; and generation, which Jev does not do at all. The structural-invariants entry gives an example where P(refund) = 0.72 and P(not refund) = 0.47 in the same call, summing to 1.19, and advises developers to "enforce identities in code".

TypeSafe itself warns that "a Choice always returns an allowed destination and can still be the wrong one" ([flaviocopes](https://flaviocopes.com/jev/)). An independent test found jev-1.13 "does not treat [adversarial content] as hostile by default". The same test found that a wrong criteria description is "catastrophic: 16.7%, below the 25% random floor" ([Beri.net](https://www.beri.net/article/typesafe-jev-typed-decision-model-calibration-decomposition-shadow-eval)).

Five more gaps come from how the product is built, and they define what an open challenger should target. **Jev is closed**, with no weights, no paper and no on-premises option ([InfoWorld](https://www.infoworld.com/article/4223468/typesafe-ais-new-models-work-with-machines-not-humans.html)). **It cannot be fine-tuned** ([TypeSafe models doc](https://docs.typesafe.ai/models.md)). **It cannot generate text**, so it can pick an enumerated argument value but cannot write a free-form one such as a city name or date copied from the query. **Access is limited:** Jev runs in a single region, direct signups opened on 20 September and were paused on 22 September ([Firecrawl](https://www.firecrawl.dev/blog/what-is-jev)), and the rate limit of 1,200 requests per minute is "adjusting dynamically" ([TypeSafe models doc](https://docs.typesafe.ai/models.md)). Finally, **input is text only and English-first**.

## Open look-alikes appeared within ten days, but none benchmarks against Jev

The open landscape splits into four groups that rarely overlap. Encoders and zero-shot classifiers return label distributions in tens of milliseconds but cannot fill tool arguments. Classification heads and probes read one-pass scores from the internal states of decoder LLMs. Small function-calling models fill arguments but generate their answers token by token, which makes them slow. Routers pick a model or a route, but not tool arguments.

| Open option | Size / licence | How it decides | Speed evidence | What it lacks against Jev |
|---|---|---|---|---|
| Laya | 421M, Apache-2.0 | Answers Jev-style questions locally | 32.8 ms per question on T4 ([BestHub](https://www.besthub.dev/articles/open-source-decision-model-laya-vs-jev-speed-wins-zero-shot-fails-befced0a2228)) | Base model is "nearly random" zero-shot; numbers only from secondary blogs |
| OpenJev repositories and SemIf | Qwen3-4B-Instruct-2507 (Apache-2.0) with LoRA adapters | Reads the logits of the declared options in one pass; scalar head; temperature calibration ([zhihz/openjev](https://github.com/zhihz/openjev), [SemIf](https://github.com/TheoLeeCJ/SemIf)) | Not reported | 4B size; trails Jev 0.845 to 0.883 in agreement |
| GLiClass modern-base-v3.0 | 151M, Apache-2.0 | Scores text and labels together in one pass, so it handles labels it has never seen | 54.46 examples/s at batch size 1 on an A6000; 50.34/s with 128 labels ([HF card](https://huggingface.co/knowledgator/gliclass-modern-base-v3.0)) | Zero-shot average F1 of 0.558 (the large model reaches 0.700); outputs labels only |
| DeBERTa-v3 zero-shot classifiers (natural-language inference) | Base and large sizes | One forward pass per label ([HF](https://huggingface.co/MoritzLaurer/deberta-v3-large-zeroshot-v2.0-c)) | About 9x slower than GLiClass at large label counts | Cost grows with the number of labels |
| Arch-Router-1.5B | 1.5B, Katanemo research licence | Emits a short JSON route | 50 ms median, under 75 ms at the 99th percentile; 93.17% routing accuracy ([arXiv 2506.16655](https://arxiv.org/abs/2506.16655)) | Routing only; licence is not permissive |
| NVIDIA prompt-task-and-complexity classifier | DeBERTa-v3-base, about 86M | Classifier with several heads ([HF card](https://huggingface.co/nvidia/prompt-task-and-complexity-classifier)) | Not reported | Fixed task list |
| SCX Router | Qwen3-0.6B plus a shallow scorer | Reuses the decoder's cache across a session and scores options with a classifier ([arXiv 2609.02292](https://arxiv.org/abs/2609.02292)) | Not reported | Model routing only |
| FunctionGemma | 270M, Apache 2.0 plus Gemma terms | Generates function calls | 0.3 s to first token on a phone CPU; 61.6% on BFCL "simple" ([model card](https://ai.google.dev/gemma/docs/functiongemma/model_card)) | Generates tokens and does not return probabilities over options |

**Encoders are the right base for a decision model.** A controlled comparison found that a 400M Ettin encoder beats a 1B decoder on classification ([HF paper page](https://huggingface.co/papers/2507.11412)). Classification heads on small Qwen3 models beat generating the label as text by 2–3% ([arXiv 2607.03801](https://arxiv.org/abs/2607.03801)).

**No such model has been tested on the main tool-calling leaderboard.** No encoder, classifier-head or router model appears on BFCL v4. The small open models that do appear report mean latencies of **2–50 seconds**, because every entry generates its answer token by token ([BFCL data](https://gorilla.cs.berkeley.edu/data_overall.csv)). The same data shows that the strongest small function-calling families are not free for commercial use: xLAM-2 and Hammer are cc-by-nc-4.0, and Arch uses Katanemo's research licence.

**The novelty window for an "open Jev" is already closing.** Laya claims to be faster than Jev and, once fine-tuned, more accurate. Two OpenJev repositories and a Hugging Face checkpoint reproduce the interface, and a Hacker News commenter says they built a prototype in about two hours ([HN thread](https://news.ycombinator.com/item?id=49717558)).

Two things remain unclaimed. The first is **a public, reproducible, multi-task benchmark that includes Jev and measures calibration**; the independent tests above are one-offs of 102 to 2,000 items, each on a private or synthetic set. The second is **a one-pass model that both chooses the tool and fills its arguments, with published BFCL numbers**; the model-side research found no such result.

## $30 cannot out-generalize Jev, but it can out-calibrate, out-localize and out-fill it

### The honest verdict on "faster and more accurate"

The question splits into four parts.

**Faster: yes, but only by running locally.** GLiClass's throughput implies about 18 ms per example at batch size 1 on an A6000 (my arithmetic from 54.46 examples/s), and Laya reports 32.8 ms on a T4. Jev's median is 236–276 ms in the Laya comparison, with a floor of about 430 ms from Europe. This compares a local model with a network API, so the fair claim is: "for anyone who cannot or will not call a US-hosted API, decisions are 5–10x faster".

**More accurate zero-shot, on questions nobody has seen before: no, not for $30.** An open 4B model still trails Jev (0.845 vs 0.883). Laya's base model is near random zero-shot, and GLiClass averages only 0.56–0.70 F1 across 15 datasets. TypeSafe's staff say data quality is the "far most interesting" part of their moat ([HN thread](https://news.ycombinator.com/item?id=49717558)), and a two-week student project will not recreate that. Report a zero-shot column honestly, but do not make it the headline.

**More accurate after light task-specific training: likely yes.** A fine-tuned 310M encoder already beat Jev by 12 points on topic classification, and fine-tuned Laya edges out Jev (0.766 vs 0.727). Fine-tuning ModernBERT-base on Banking77 took **321 seconds on one L4 GPU, for F1 0.93** ([Phil Schmid](https://www.philschmid.de/fine-tune-modern-bert-in-2025)), which is about $0.07 of GPU time at Modal prices. Jev cannot be fine-tuned at all.

**Better calibrated: likely yes.** Jev's miscalibration runs in a known direction for each question type, with fitted temperatures of 0.66 for yes/no, 3.29 for Choice and 3.40 for Score ([Beri.net](https://www.beri.net/article/typesafe-jev-typed-decision-model-calibration-decomposition-shadow-eval)). Standard per-type temperature scaling on held-out data targets exactly that.

The winnable headline is therefore not "better than Jev". It is **"the open, trainable, calibrated Jev that also fills tool-call arguments, and the first public benchmark to measure all of them"**.

### Build a one-pass encoder that decides and fills arguments

The recommended build, which I call **OpenDecide**, combines Jev's three question types with the SpanCall argument-filling design from the model-side research.

**Backbone.** Start from GLiClass-modern-base-v3.0, which is Apache-2.0 and already trained to score labels it has not seen. Compare it against a freshly fine-tuned ModernBERT-large and an Ettin-400M encoder; Ettin's authors report that it "outperform[s] ModernBERT across all tasks and model sizes" ([HF blog](https://huggingface.co/blog/ettin)).

**Input and batching.** Each sequence holds the state, one question and the declared options. Questions are batched in parallel, mirroring Jev's "parallel and isolation" behaviour.

**Decision heads.** Three heads match Jev's question types. A sigmoid head answers Noul. A softmax over the option embeddings answers Choice, for up to 255 options, including options the model has never seen. An ordinal distribution over 2–10 levels answers Score and returns both the distribution and the expected level.

**Argument-filling heads.** These follow the SpanCall spec, which builds on GLiNER2-style single-pass extraction ([arXiv 2507.18546](https://arxiv.org/pdf/2507.18546)). A per-tool relevance score also covers the case where no tool applies. A per-parameter switch classifies each value as a span copied from the query, an enum value, a boolean, a number, null, or "needs generation". A pointer head marks where each span starts and ends, and an enum classifier and number normalizer handle the rest. Only arguments flagged "needs generation" go to a fallback Qwen3-0.6B or Qwen3-1.7B, constrained to fill just those fields.

**Calibration.** Fit one temperature per question type on held-out data. Report expected calibration error, Brier score and reliability diagrams. Also report accuracy-versus-coverage curves, which show what happens when the model abstains below a confidence threshold.

**Training data.** Training data comes from three sources. The first is public classification, inference and intent datasets recast into the three question types, which is how the DeBERTa zero-shot models were trained on 27 tasks and 310 classes ([HF](https://huggingface.co/MoritzLaurer/deberta-v3-base-zeroshot-v1)). The second is APIGen-derived function-calling data, with argument values aligned to spans in the query ([APIGen, arXiv 2406.18518](https://arxiv.org/pdf/2406.18518)). The third is labels produced by an open Qwen3-8B teacher running on Modal. At the roughly 7,000 tokens/s that vLLM reaches on an H100 ([DatabaseMart](https://www.databasemart.com/blog/vllm-gpu-benchmark-h100)), I estimate that at about $4 per 100k examples.

Do not train on Jev's outputs. TypeSafe's legal and terms-of-service page was not reviewed, and training on its outputs would invite a dispute.

### Benchmark it on public test sets, and give Jev every advantage

A self-invented benchmark reads as marketing, as happened with Engram's unverified "100x fewer tokens" claim ([TechTimes](https://www.techtimes.com/articles/319106/20260625/enterprise-ai-token-costs-engram-exits-stealth-98m-claims-100x-cut.htm)). So build the benchmark, which I call **TypedDecisionBench**, entirely from existing public test sets, each recast into one of Jev's question types.

| Task family | Public source | Jev question type | Headline metric |
|---|---|---|---|
| Intent classification | Banking77 (77 intents), CLINC150 (150 intents) ([IntenDD](https://arxiv.org/pdf/2310.16761)) | Choice | Accuracy, macro-F1, calibration error |
| Out-of-scope detection | CLINC150's 1,200 out-of-scope queries | Noul | AUROC, calibration error |
| Tool selection and relevance | BFCL non-live AST simple, multiple and irrelevance categories ([BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html)) | Choice + Noul | Accuracy, calibration error |
| Tool retrieval | MetaTool, 199 tools ([arXiv 2603.13426](https://arxiv.org/abs/2603.13426)) | Choice | Top-1 accuracy, NDCG@5 |
| Model routing | RouterBench ([arXiv 2403.12031](https://arxiv.org/abs/2403.12031)) | Choice | Quality at a cost budget |
| Argument filling | BFCL non-live AST simple and multiple | Not possible for Jev | AST accuracy, fallback rate |

**Evaluation settings.** Run three settings: zero-shot, 100 labels per task, and 1,000 labels per task. In the labelled settings, give Jev the same labels through the trick that lifted it to 95% on phishing: ask several narrow questions and fit a logistic regression on its outputs. That pre-empts the "you misconfigured our system" rebuttal Zep aimed at Mem0 ([Zep blog](https://blog.getzep.com/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/)).

**Latency.** Measure Jev's median and 95th-percentile latency from the same machines that run the local models, and again from a European location.

**Baselines.** Jev itself can be reached through OpenRouter or Vercel AI Gateway, which list `jev-latest`, if direct signups stay paused. The open baselines are:

| Baseline | What it represents |
|---|---|
| GLiClass, run zero-shot | Existing open label-scoring encoder |
| DeBERTa zero-shot classifier | Older one-pass-per-label approach |
| OpenJev-style Qwen3-4B reading option logits | Existing open Jev reproduction |
| Prompted Qwen3-0.6B, 1.7B and 4B on BFCL | Small generative function callers |
| Laya, if its weights can be downloaded | Closest open Jev competitor |
| Claude Haiku 4.5 (optional) | Small frontier LLM |
| Fine-tuned single-task ModernBERT | Upper bound |

**Cost of testing Jev.** At $0.042 per million tokens, running Jev on 20,000 items of about 400 tokens each costs roughly $0.34.

### Budget and pass/fail gates

Modal's list prices turn $30 into about 7.6 H100-hours or 37.5 L4-hours ([Modal pricing](https://modal.com/pricing)).

| Item | Hardware | Estimated cost |
|---|---|---|
| Teacher labels (Qwen3-8B, ~100k examples) | H100, about 1 hour | ~$4 |
| Decision-head training and ablations (10–20 runs) | L4 or A10 | ~$2–6 |
| Argument-filling encoder fine-tune | H100, 1–2 hours | ~$4–8 |
| Open baselines on BFCL, plus Qwen3-4B logit reading | H100, about 1 hour | ~$4 |
| Jev API across the full benchmark | — | under $1 |
| **Total** | | **~$15–23** |

The reference numbers in the gates below come from the research notes; the thresholds themselves are my recommendations.

| Claim | Pass (publish it) | Fail (drop or re-scope the claim) |
|---|---|---|
| Speed | Median ≤ 30 ms per request with up to 32 options on one L4 at batch 1, and at least 3x below Jev's median measured from the same host | Local median above 100 ms |
| Calibration | Expected calibration error ≤ 0.05 for each question type, and lower than Jev's on the same items | Not below Jev after temperature scaling |
| Accuracy with labels | Beats Jev on at least 4 of 6 task families with ≤1,000 labels per task, with Jev given the same labels | Wins on 2 or fewer families: remove "more accurate" from the headline |
| Accuracy zero-shot | Within 5 points of Jev on the macro average (report the result either way) | More than 15 points behind: position it as "the trainable Jev", not a replacement |
| Tool calls (BFCL non-live simple AST) | ≥75.19%, which is prompted Qwen3-1.7B's score, at 10x or more lower latency; stretch goal 84.50%, Qwen3-4B's score, with the fallback on ([TinyLLM, arXiv 2511.22138](https://arxiv.org/pdf/2511.22138)) | Below 60.47%, Qwen3-0.6B's score: ship tool selection only |
| Day-one kill switch (free, runs on CPU) | Most BFCL AST argument values are copyable spans, enums, booleans or numbers | If not, the LLM fallback fires too often, erases the speed gain, and the argument-filling claim should be dropped |

The target headline has the shape the playbook recommends: a dollar figure, a famous comparison target, and open artifacts, as TinyZero's "<$30" did ([Jiayi Pan on X](https://x.com/jiayi_pirate/status/1882839370505621655)). For example: "A 150M-parameter open model answers Jev-style questions in under 30 ms on a $0.80/hour GPU, is twice as well calibrated, fills the tool-call arguments Jev cannot, and beats Jev on N of 6 public tasks with 1,000 labels, trained for $X on Modal."

### Who buys it, and what could sink it

**Price is not the pitch.** At $0.042 per million tokens, Jev is already almost free. **The pitch is everything Jev cannot do.** OpenDecide runs on-premises for teams that cannot send data to a US-hosted cloud, the privacy concern raised on Hacker News. It can be fine-tuned. It serves users outside the US without a ~430 ms latency floor, has no 1,200-requests-per-minute cap, and fills tool-call arguments. Latency-critical agent builders are the natural first users; SimpleTool's motivating case, for example, was 16 Hz real-time control ([arXiv 2603.00030](https://arxiv.org/abs/2603.00030)).

**Three risks stand out.** The first is crowding: Laya, OpenJev and Fastino could each claim pieces of this, and Fastino, which maintains GLiNER2, is the most likely fast follower on encoder-based function calling. The second is that TypeSafe's possible paper could arrive with its own benchmarks. The third is scope: BFCL v4's overall score gives heavy weight to agentic and multi-turn categories where this approach does not apply ([BenchLM](https://benchlm.ai/benchmarks/bfcl-v4)), so claims must stay within the AST categories.

**The moat is thin.** It consists of credibility from defining the benchmark, plus a path to customers Jev cannot serve.

**The category is fundable, but the numbers alone will not raise.** TypeSafe's $40M seed validates the category, and the closest precedent, the router company Not Diamond, raised $2.3M ([VentureBeat](https://venturebeat.com/ai/not-diamond-automatically-routes-your-query-to-the-best-llm)). But benchmark numbers rarely fund a company by themselves. Mem0's $24M round rested as much on 41,000 GitHub stars and 186M API calls per quarter as on its paper ([TechCrunch](https://techcrunch.com/2025/10/28/mem0-raises-24m-from-yc-peak-xv-and-basis-set-to-build-the-memory-layer-for-ai-apps/)).

## Six ideas survive a screen of roughly 47 candidates

The two research streams screened about 47 candidates: 17 on the model and architecture side and about 30 on the agents, evals and data side. Six survive. Each fits one of two patterns. In the first, a new small architecture is applied to an old, business-relevant structured task that has public benchmarks and weak or expensive LLM baselines. In the second, a public record of expert decisions, such as customs rulings or SEC staff letters, supplies ground-truth labels for free.

The team's criterion was "a paper may exist, but no public implementation or benchmark", and the ideas meet it to different degrees. Idea 1 meets it on the Jev benchmark and on encoder-based function calling. The two tiny recursive model (TRM) ideas have public benchmarks but no TRM implementation for their task. The SEC idea, the export-control part of the tariff idea and the Hinglish benchmark have no public benchmark at all. The customs-tariff (HS code) part of idea 2 does *not* strictly meet the criterion, because public benchmarks and code already exist.

| # | Idea | Unclaimed gap | Number to beat | GPU | Extra API | Closest competitors | Difficulty |
|---|---|---|---|---|---|---|---|
| 1 | OpenDecide (decisions plus argument filling) and TypedDecisionBench | No public benchmark that includes Jev; no encoder-only model on BFCL | Jev on public tasks; 75.19% on BFCL simple AST | ~$15–23 | <$1 | Laya, OpenJev, GLiClass, Fastino, FunctionGemma | Low–medium |
| 2 | Tariff classifier grounded in past customs rulings, plus ECCN-Bench | No public benchmark for export-control codes (ECCNs); no tariff vendor publishes benchmark numbers | 46.83% (10-digit) on HSCodeComp; 40% (10-digit) and 57.5% (6-digit) on the ATLAS test set | ~$12–20 | $0–100 | Digicust, TariffLens, iCustoms, Thomson Reuters | Medium |
| 3 | SheetTRM | No TRM on native spreadsheet grids | 78.9% table-detection F1; 0.937 cell-type F1 | ~$25–30 (tight) | None | Microsoft spreadsheet research, LlamaIndex, Querri | High |
| 4 | SECReviewBench | Nothing predicts the content of SEC comment letters | None published | ~$10–17 | ~$30–100 | Intelligize, Workiva, Ideagen | High |
| 5 | FlashTRM | No TRM for programming by example | 82% generalization on PROSE; floor 33% | ~$20–28 | None | Excel Flash Fill, LLM-based programming-by-example work | Medium |
| 6 | HinglishTau (conditional) | No public benchmark of stateful, policy-bound agents in code-mixed or romanized Indian languages | No public number | ~$20–25 (tight) | ~$100–250 | Meta, Krutrim, Sarvam, Caller Digital | Medium–high |

| # | Pass criterion | Kill criterion |
|---|---|---|
| 1 | The gates in the previous section | Day-one span-alignment check fails, or accuracy with labels wins on 2 or fewer families |
| 2 | Beat the ATLAS scores (57.5% at 6 digits, 40% at 10 digits) with an open model of 8B or fewer parameters, or beat 46.83% at 10 digits on HSCodeComp; release ECCN-Bench v0 with baseline results | Retrieval plus a verifier cannot beat ATLAS at 6 digits: fall back to a benchmark-only release |
| 3 | Beat 78.9% table-detection F1 under SpreadsheetLLM's exact protocol, or match 0.937 cell-type F1 on a CPU, with ablations showing recursion beats one step and beats LightGBM on the same features | Recursion adds nothing over LightGBM on the same features |
| 4 | ≥300 filing–letter pairs; an LLM judge validated against two annotators (my suggestion: Cohen's κ ≥ 0.6); the agent beats a zero-shot frontier model on recall of actual comments in 2026 letters | Judge–human agreement too low for the benchmark to be credible |
| 5 | Above 59% generalization on PROSE (the LLM out-of-distribution figure) at millisecond latency; stretch goal 82% | Below Flash Fill's 33% |
| 6 | Accuracy drops measurably from English to Hinglish on τ²-bench, and a LoRA fine-tune closes ≥50% of the small-vs-frontier gap at about a tenth of the cost | No meaningful drop, or the API budget is unavailable |

### Idea 2: tariff and export-control classification grounded in past rulings

**Where the benchmarks stand.** On HSCodeComp, which has 632 expert-annotated products, the best agent reaches **46.83%** at 10 digits against **95.0%** for human experts. Majority-vote test-time scaling gave "negligible" gains, and self-reflection slightly hurt ([arXiv 2510.19631](https://arxiv.org/html/2510.19631)). On ATLAS, built from US Customs (CBP) CROSS rulings, a fine-tuned LLaMA-3.3-70B reaches **40% at 10 digits and 57.5% at 6 digits**, 15 points above GPT-5-Thinking ([arXiv 2509.18400](https://arxiv.org/abs/2509.18400)). Its training data, about 18.7k rows, is public ([HF dataset](https://huggingface.co/datasets/flexifyai/cross_rulings_hts_dataset_for_tariffs)).

**The system.** The classifier walks the tariff tree one level at a time (chapter, heading, subheading, national code), restricted to valid children at each step. At each level, a small LoRA-tuned verifier re-ranks the candidates using retrieved past rulings. It abstains when its margin is thin, which produces the accuracy-versus-coverage curve that customs brokers actually buy.

**Why it fits after idea 1.** Each level of that walk is a choice among a bounded set of valid children, which is exactly Jev's Choice question type. OpenDecide can therefore serve as the verifier, which gives ideas 1 and 2 a shared engine. This link is my inference.

**The export-control (ECCN) extension is genuinely empty.** Researchers at the Institute for AI Policy and Strategy (IAPS) note that no one has benchmarked ECCN classification "with real BIS data" ([IAPS](https://www.iaps.ai/research/evaluating-llm-capabilities-for-commodity-classification)). Manufacturers such as Microsoft publish the codes for their own products, which provides free labels ([Microsoft Exporting](https://www.microsoft.com/en-us/exporting/exporting-information)).

**Risks.** Only the first six digits are harmonized internationally, so US precedents may not transfer beyond that level. The best HSCodeComp system used product images, which a text-only system lacks. A misclassification carries penalties, so the product must be sold as decision support with abstention. The ECCN labels are also skewed toward the low-control categories (EAR99 and 5x992).

**Commercial field.** At least seven vendors, including Digicust and Thomson Reuters, sell AI tariff classification ([Digicust](https://digicust.com/en/blog/complete-guide-hs-code-classification-2026/)). None was found publishing numbers on these benchmarks.

**First customers.** Customs brokers, third-party logistics firms and cross-border e-commerce sellers, starting with a per-SKU "catalog audit".

### Idea 3: SheetTRM for spreadsheet structure

A tiny recursive model (TRM) is a network of about 7M parameters that refines its answer over several passes. It reached **45% on ARC-AGI-1** ([arXiv 2510.04871](https://arxiv.org/abs/2510.04871)). PTRM, a variant that runs several noisy passes in parallel and keeps the best one, lifted Sudoku-Extreme from 87.4% to 98.75% without retraining ([arXiv 2605.19943](https://arxiv.org/abs/2605.19943)).

**Nobody has applied TRM to native spreadsheet grids.** The closest work, FastTab, recognizes tables in *images* ([arXiv 2605.22422](https://arxiv.org/abs/2605.22422)). The targets are the **78.9% table-detection F1** of SpreadsheetLLM's fine-tuned model ([arXiv 2407.09025](https://arxiv.org/abs/2407.09025)) and the **0.937 cell-type F1** of a CRF-LightGBM system on StatSheets ([arXiv 2608.16050](https://arxiv.org/abs/2608.16050)). TableSense's public annotations cover more than 13,000 sheets ([microsoft/TableSense](https://github.com/microsoft/TableSense)).

**The budget is the binding constraint.** TRM's standard recipe takes up to 20 L40S-hours even for Sudoku, about $39 ([TRM repo](https://github.com/SamsungSAILMontreal/TinyRecursiveModels)). SheetTRM therefore needs a cut-down recipe, with fewer recursion steps, row-and-column ("axial") attention and early stopping, which comes to about $25–30 in total.

**What must be proven.** The cell-type task is near its ceiling, so the headline has to be table detection or cost. Reviewers will demand an ablation showing that recursion, not the input features, earns the gain.

**First customers.** Data teams at insurers, FP&A consolidation teams, and developers of spreadsheet agents. LlamaIndex's Spreadsheet Agent preview shows the demand ([LlamaIndex](https://www.llamaindex.ai/blog/introducing-the-spreadsheet-agent-in-private-preview)).

### Idea 4: SECReviewBench, predicting SEC comment letters

**The data.** EDGAR holds about **600,000 SEC staff comment letters and company responses dating back to 2004** ([sec-api.io](https://sec-api.io/datasets/sec-comment-letters)).

**Almost no prior work.** The only prior machine-learning work is a Naive Bayes model that flags *important* letters "up to 40 percent better than chance"; it does not predict their content ([Ryans, UCLA](https://www.anderson.ucla.edu/documents/areas/fac/accounting/working-papers/ryans_jmp.pdf)). Incumbents such as Intelligize offer search over past letters but no prediction benchmark ([Intelligize](https://www.intelligize.com/solution/public-companies/)).

**Design.** Test on letters dated 2026, after frontier models' training cutoffs, which rules out the models having memorized them.

**Risks.** Labels are incomplete, because staff do not raise every issue, which caps recall. Linking each letter to the exact filing amendment it reviews is fiddly engineering. The buyers, securities lawyers, are conservative. Frontier baselines and the LLM judge need about $30–100 of API spend.

**Payoff.** The team would set the first number in an empty category, and the benchmark doubles as marketing: "we recover N% of real SEC comments".

### Idea 5: FlashTRM for string transforms by example

PROSE is a set of 100 programming-by-example problems, where the model infers a text transform from a few input/output pairs. On it, Excel's Flash Fill scores **33%**. A fine-tuned DeepSeekCoder-33B scores **82%**, but it "essentially never produces a correct program on the first try" and needs minutes of sampling per problem. Out of distribution, the same kind of model scores **59%** ([Li & Ellis, arXiv 2406.08316](https://arxiv.org/abs/2406.08316)).

**Why a TRM fits.** A 7M-parameter TRM can be trained on unlimited synthetic tasks, which keeps it within budget. Hiding one demonstration example and checking whether the model reproduces it gives a free verifier for choosing among PTRM-style noisy attempts.

**Main weakness: the market.** Flash Fill is free inside Excel. FlashTRM works best as a column-normalization feature inside SheetTRM's product and as a quick second paper for a "tiny recursive models for spreadsheets" thesis.

### Idea 6: HinglishTau, conditional on API credits

**What already exists.** Meta's OmnilingualGAIA2 covers Hindi in native script, where Hindi is among the weakest languages at every model size ([arXiv 2608.08775](https://arxiv.org/pdf/2608.08775)). Krutrim's VoiceAgentBench covers spoken Indian-language tool calls ([arXiv 2510.07978](https://arxiv.org/abs/2510.07978)).

**What is missing.** Neither benchmark covers the stateful, policy-bound customer-service setting of τ²-bench in code-mixed or romanized text. The demand is real: Caller Digital runs a *private* Hinglish benchmark in which **small open models reach 66.1% turn-correct against 90.2% for frontier models** ([Caller Digital](https://caller.digital/blog/llm-benchmark-indian-voice-agents-function-calling-latency-2026)).

**Why it remains conditional.** It needs roughly **$100–250 of API spend** for translation, the simulated user and frontier baselines. It needs native speakers to validate the data. Meta or Sierra could also add code-mixed variants quickly.

## More than 40 dropped ideas show where 2026 research already landed

The consistent lesson: **anything that makes LLM agents faster or more reliable drew several 2026 papers, often from large labs with released code.** A $30 team cannot win those races. The table logs the most relevant drops, starting with the team's own earlier rejections.

| Dropped idea | Why dropped | Who already did it |
|---|---|---|
| Inference hosting | The team's own rejection: crowded | — |
| Task marketplace for AI labs | The team's own rejection: first customer hard to win | — |
| Generic open Jev clone | Crowded within ten days of launch | Laya ([BestHub](https://www.besthub.dev/articles/open-source-decision-model-laya-vs-jev-speed-wins-zero-shot-fails-befced0a2228)), OpenJev ([zhihz/openjev](https://github.com/zhihz/openjev)), GLiClass ([arXiv 2508.07662](https://arxiv.org/abs/2508.07662)) |
| JEPA-style tool or decision model (predicting embeddings instead of tokens) | The method exists with code, and a replication found no gain | LLM-JEPA ([arXiv 2509.14252](https://arxiv.org/abs/2509.14252)); an audit of 22 auxiliary training objectives found none that survived multiple-comparison correction ([arXiv 2605.15394](https://arxiv.org/abs/2605.15394)) |
| Diffusion language models for tool calls | Done, with negative results | "The Bitter Lesson of Diffusion LMs for Agentic Workflows" ([arXiv 2601.12979](https://arxiv.org/html/2601.12979v3)) |
| Speculative or parallel decoding of tool calls | Crowded | SimpleTool ([arXiv 2603.00030](https://arxiv.org/abs/2603.00030)), ToolSpec ([arXiv 2604.13519](https://arxiv.org/abs/2604.13519)), OoO-Spec ([arXiv 2608.00814](https://arxiv.org/abs/2608.00814)), HyFunc ([arXiv 2602.13665](https://arxiv.org/abs/2602.13665)) |
| Reusing the cached computation (KV cache) of tool schemas | Done | ReCache: 3.655x faster time to first token ([arXiv 2608.19662](https://arxiv.org/abs/2608.19662)) |
| Compiling tool documentation into LoRA weights with a hypernetwork | Done | Doc-to-LoRA ([arXiv 2602.15902](https://arxiv.org/abs/2602.15902)) |
| Activation steering to fix tool-call errors | Done | "Tool Calling is Linearly Readable and Steerable" ([arXiv 2605.07990](https://arxiv.org/html/2605.07990v2)) |
| Looped LMs for tool calling; branching inside looped LMs | Done, and crowding fast | [arXiv 2608.18171](https://arxiv.org/pdf/2608.18171); [Branching-Looped-Transformer](https://github.com/VykosMolt/Branching-Looped-Transformer) |
| Tool reward models and pre-execution verifiers | Crowded | ToolRM, up to 25% gains ([arXiv 2509.11963](https://arxiv.org/abs/2509.11963)); ToolGuard ([arXiv 2609.19425](https://arxiv.org/html/2609.19425)) |
| Calibrating agent tool-call confidence as a standalone product | Crowded (kept only as a feature of OpenDecide) | [arXiv 2601.07264](https://arxiv.org/abs/2601.07264); [arXiv 2609.07395](https://arxiv.org/pdf/2609.07395) |
| Early-abort circuit breaker for failing agents | At least 7 papers in 2026; the best fallback | "Doomed from the Start" ([arXiv 2607.06503](https://arxiv.org/abs/2607.06503)), BAGEN ([arXiv 2606.00198](https://arxiv.org/pdf/2606.00198)) |
| Tool and MCP-server selection at scale | Crowded | MCP-Zero ([arXiv 2506.01056](https://arxiv.org/html/2506.01056v2)), MCP-Bench ([OpenReview](https://openreview.net/forum?id=fe8mzHwMxN)) |
| Agent evaluation platforms and cost-accuracy leaderboards | Saturated or done | HAL: 21,730 rollouts ([arXiv 2510.11977](https://arxiv.org/html/2510.11977.pdf)); [Maxim roundup](https://www.getmaxim.ai/articles/top-5-ai-agent-evaluation-platforms-in-2026/) |
| Cost and latency benchmark for computer-use agents | Done | OSWorld-Human ([arXiv 2506.16042](https://arxiv.org/pdf/2506.16042)) |
| Prompt-injection detection | Crowded | LlamaFirewall ([arXiv 2505.03574](https://arxiv.org/pdf/2505.03574)) |
| Document extraction with small models | Saturated | Unsiloed leads olmOCR-Bench at 88.0 ([Unsiloed](https://www.unsiloed.ai/blog/unsiloed-ai-achieves-1-rank-on-olmocr-bench-2)) |
| Voice turn-taking; capturing IDs and codes by voice | Done | LiveKit eot-bench ([GitHub](https://github.com/livekit/eot-bench)); τ-Elicitation ([arXiv 2609.13602](https://arxiv.org/abs/2609.13602)) |
| Auditing tool-call quality across hosting providers | Done, and on by default | OpenRouter Exacto ([OpenRouter](https://openrouter.ai/docs/guides/routing/auto-exacto)) |
| Reverse-engineering web traffic (HAR files) into typed APIs | Done | Integuru ([HN](https://news.ycombinator.com/item?id=41983409)) |
| State-of-the-art result on an agent-memory benchmark | Benchmarks flawed, and leadership does not last | A filesystem agent beats memory systems on LoCoMo ([Letta](https://www.letta.com/blog/benchmarking-ai-agent-memory/)) |
| Prior authorization, ERP agents, insurance intake | Benchmarks already exist | CHI-Bench ([arXiv 2605.16679](https://arxiv.org/pdf/2605.16679)), ERPBench ([arXiv 2609.04667](https://arxiv.org/abs/2609.04667)), RealDocBench ([arXiv 2606.07401](https://arxiv.org/html/2606.07401)) |
| B2B order entry; RFP compliance matrices | No benchmark exists, but at least five funded vendors do | [Y Meadows](https://ymeadows.com/en/insights/blog/ai-order-entry-for-distributors/), [GovDash](https://www.govdash.com/glossary/what-is-a-compliance-matrix) |
| Sanctions name-screening | Saturated | GPT-4o reaches 98.95% F1 ([arXiv 2603.11051](https://arxiv.org/html/2603.11051v1)) |
| TRM for route optimization; schema matching; tabular error detection | Done; the "small model beats frontier" pitch is taken; poor fit | TRM on the travelling-salesman problem ([FLAIRS](https://journals.flvc.org/FLAIRS/article/view/141582)); constraint-guided mapping ([arXiv 2608.24218](https://arxiv.org/abs/2608.24218)) |
| Training speedruns and cheap reproductions | Too competitive, or over budget | modded-nanogpt has 91+ contributors ([GitHub](https://github.com/kellerjordan/modded-nanogpt)); nanochat costs about $52 on Modal ([README](https://github.com/karpathy/nanochat)) |

## Update, 25 September: the benchmark gap is already smaller

A follow-up check found that community audits of Jev moved faster than this report assumed.

- **The core metrics are covered.** [AbdelStark/jev-benchmarks](https://github.com/AbdelStark/jev-benchmarks) already reports accuracy, Brier score, log loss, calibration error, coverage at a fixed error budget, latency and cost. Its 300-example pilot has Jev beating GLiNER2.5 on accuracy (AG News 91% vs 70%) but losing on Emotion calibration (Brier 0.846 vs 0.668), and Jev gave the true label zero probability 16% of the time.
- **Separate repos test the documented failures.** The [awesome-jev-robustness](https://github.com/Yifan-Lan/awesome-jev-robustness) list indexes them:
  - negation consistency, where P(x) + P(not x) ranges from 0.71 to 1.42 (jujumilk3/jev-calibration-audit)
  - paraphrase
  - prompt injection, where accuracy falls from 96.5% to 26.5% (zkousama/jagged)
  - tool abstention
- **Still open.** No public test was found for distractor robustness. No single harness covers every failure mode. No open, *trained* model yet claims to fix negation or complement consistency (kyegomez/open-jev has a consistency loss but no weights).

So "the first public benchmark that includes Jev" no longer holds. The benchmark half of idea 1 should become contributions of the missing test suites to jev-benchmarks, and the trained model becomes the headline. The dates of these repos were not checked against the ten days since launch.

## Ranked recommendation: publish the Jev benchmark first, then take it into a vertical

| Rank | Do this | Why it ranks here | GPU spend | When |
|---|---|---|---|---|
| 1 | **OpenDecide plus TypedDecisionBench** | Jev is 10 days old and has no standard benchmarks, and developers are publicly asking for them. It is the cheapest idea, answers the Jev question directly, and builds infrastructure the vertical ideas reuse | ~$15–23 | Now; publish within 2–3 weeks |
| 2 | **Tariff classifier grounded in past rulings, plus ECCN-Bench** | Clearest first customer; best system at 46.83% against 95% for human experts; export-control codes are an empty space; OpenDecide becomes the verifier at each tariff level | ~$12–20 (+ optional API) | Month 2 |
| 3 | **SheetTRM** | Most novel method; a "7M model beats a fine-tuned LLM" headline; clear buyers; tight budget and high difficulty | ~$25–30 | Month 2–3, if the team has research depth |
| 4 | **SECReviewBench** | Empty space, but heavy data engineering, API spend and conservative buyers | ~$10–17 + $30–100 API | Only with a securities-law or finance advisor |
| 5 | **FlashTRM** | Cheap, clean paper with a weak standalone market | ~$20–28 | As a companion to SheetTRM |
| 6 | **HinglishTau** | Conditional: needs a lot of API spend and faces rising competition | ~$20–25 + $100–250 API | Only with native speakers and API credits |

**Before spending anything.** Four steps cost nothing. First, read TypeSafe's terms of service at docs.typesafe.ai/legal.md, which the research did not review. Second, secure Jev access through OpenRouter or Vercel AI Gateway, since direct signups are paused. Third, run the span-alignment kill-switch check on BFCL on a laptop CPU. Fourth, apply for Modal's academic credits, worth up to $10k; the startup programme requires having raised $1M or backing from a partner VC ([Modal pricing](https://modal.com/pricing)).

**The budget is larger than it looks.** The $30 is almost certainly the Starter plan's *monthly* free compute allowance ([Modal pricing](https://modal.com/pricing)), so a three-month plan has about $90. Keep CPU and RAM requests minimal: a 4-core, 32 GiB container adds about 75% to a T4's hourly cost.

**Weeks one and two.** In week one, assemble TypedDecisionBench and run Jev plus the zero-shot baselines, for pennies plus about $4 of GPU. In week two, train and calibrate OpenDecide and run BFCL.

**Week three.** Release the Apache-2.0 weights, the evaluation harness, a public leaderboard, and a write-up with the cost in the headline. Invite TypeSafe to reproduce the results or respond. Independent checks tend to become the number people quote: Poetiq's self-reported 75% on the public ARC-AGI-2 set was verified at 54% ([ARC Prize](https://arcprize.org/blog/arc-prize-2025-results-analysis)), and irreproducible claims sank Reflection 70B ([VentureBeat](https://venturebeat.com/ai/new-open-source-ai-leader-reflection-70bs-performance-questioned-accused-of-fraud)).

**Month two.** Apply OpenDecide to the tariff tree, so the attention from the Jev benchmark leads into a vertical with a paying buyer. Pitch investors on benchmark plus usage, as Mem0 did, rather than on the benchmark alone.

## Conclusion

Jev's real moat is not speed, because any 150M-parameter encoder running locally is faster. The moat is zero-shot breadth, built over two years on proprietary data, plus distribution through Vercel, OpenRouter, Pydantic and LangChain. Its weak points are the opposite of an open model's strengths: closed weights, no fine-tuning, one region, no argument filling, and probabilities that independent tests find miscalibrated. A $30 challenger should compete on those axes and openly concede zero-shot breadth; that concession makes every other claim more credible.

The more valuable asset is the benchmark vacuum. TypeSafe created a new model category without a shared yardstick. Whoever publishes the first reproducible, calibration-aware leaderboard for typed decisions gets to define how the category is measured, much as a BFCL placement made the 1B-parameter xLAM-1B newsworthy ([VentureBeat](https://venturebeat.com/ai/salesforce-proves-less-is-more-xlam-1b-tiny-giant-beats-bigger-ai-models)). The broader screen points the same way. At this budget, the wins come from pairing new small architectures, or public records of expert decisions, with old structured problems that have real buyers, not from the crowded race to speed up LLM agents. The recommended path uses the typed-decision engine twice: first for attention through the Jev benchmark, then for revenue through tariff classification.
