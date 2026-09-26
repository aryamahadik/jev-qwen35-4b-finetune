# Open-Source Models, Methods and Benchmarks for Fast Single-Pass "Decision" Inference (tool selection, routing, intent/label classification)

Research date: 2026-09-25. Items dated before 2025 are labelled "(older)". Numbers are as reported by the cited source; where a figure only comes from a secondary or aggregator site, this is stated.

## Key Question 1: Which open models and methods cover this space?

### Takeaway
The open landscape splits into four families that rarely meet. (1) Encoder and zero-shot classifiers (ModernBERT, Ettin, GLiClass, NLI models) give true one-pass label distributions at tens of milliseconds but cannot fill arguments. (2) Hidden-state or classification-head probes on decoder LLMs give one-pass scores. (3) Small generative function-calling models (xLAM-2, Hammer, Arch, FunctionGemma, Qwen3, ToolACE) fill arguments but decode many tokens and take seconds on BFCL. (4) Routers (RouteLLM, NVIDIA's DeBERTa classifier, Arch-Router, semantic-router, SCX) pick a model or route but not tool arguments. Tool-token methods (ToolkenGPT, ToolGen) and hidden-state tool selectors (Chain-of-Tools) are the closest to a one-pass "action head". JEPA-style embedding prediction (LLM-JEPA, VL-JEPA) exists for language and vision-language, but I found no JEPA-style tool or action selector.

### Cited Findings

**A. Encoder-only and zero-shot classifiers**
- ModernBERT (Dec 2024, older): an encoder with native 8,192-token context, trained on 2T tokens, which the authors call "the most speed and memory efficient encoder", designed for inference on common GPUs — [arXiv 2412.13663](https://arxiv.org/abs/2412.13663)
- ModernBERT-base is reported as the first MLM-trained model to surpass DeBERTaV3-base on GLUE. Secondary summaries report about 76.2k tokens/s at 512 tokens and about 71.1k tokens/s at 8,192 tokens, and 2.65x (base) and 3x (large) faster long-context processing than the next-fastest encoder — [Medium summary](https://ritvik19.medium.com/papers-explained-277-modernbert-59f25989f685), [ModernBERT PDF](https://arxiv.org/pdf/2412.13663). The exact throughput figures come from secondary summaries; I did not verify them in the paper's table.
- Ettin (JHU/LightOn, released 16 Jul 2025, ICLR 2026): six paired encoder and decoder sizes from 17M to 1B, trained on 2T tokens of open data with identical recipes. The authors say Ettin encoders "outperform ModernBERT across all tasks and model sizes" — [HF blog](https://huggingface.co/blog/ettin), [arXiv 2507.11412](https://arxiv.org/abs/2507.11412)
- Ettin: a 400M encoder reaches 89.2 on MNLI against 88.2 for the 400M decoder, and a 400M encoder beats a 1B decoder on classification. This is controlled evidence that encoders win on classification per parameter — [HF blog](https://huggingface.co/blog/ettin), [HF paper page](https://huggingface.co/papers/2507.11412)
- GLiClass (Knowledgator, Aug 2025): adapts the GLiNER architecture to sequence classification. Text and labels are scored in one forward pass, avoiding one cross-encoder pass per label, and PPO is added for multi-label training with sparse data — [arXiv 2508.07662](https://arxiv.org/abs/2508.07662)
- gliclass-modern-base-v3.0: 151M params, Apache 2.0, average zero-shot F1 of 0.5577 over 15 datasets (gliclass-large-v3.0 averages 0.7001). It runs 54.46 examples/s at batch size 1 on an A6000 and still 50.34 examples/s with 128 labels, against 6.03 examples/s for a DeBERTa-v3-large cross-encoder (about 9x) — [HF model card](https://huggingface.co/knowledgator/gliclass-modern-base-v3.0)
- A community GLiClass inference repo reports that cost stays flat up to about 8–16 labels and then tracks token count rather than label count — [gliclass-infer GitHub](https://github.com/srimon12/gliclass-infer)
- NLI zero-shot classifiers (MoritzLaurer deberta-v3 "zeroshot" v1/v2.0; tasksource): these reformulate any classification task as NLI (hypothesis true or not_true). v1 was trained on 27 tasks and 310 classes. The v2.0 "-c" variants use commercially friendly NLI data (MNLI, FEVER-NLI). They need one forward pass per label, which is the bottleneck GLiClass removes — [HF deberta-v3-base-zeroshot-v1](https://huggingface.co/MoritzLaurer/deberta-v3-base-zeroshot-v1), [HF large-zeroshot-v2.0-c](https://huggingface.co/MoritzLaurer/deberta-v3-large-zeroshot-v2.0-c), [Laurer et al. arXiv 2312.17543 (older)](https://arxiv.org/pdf/2312.17543)

**B. LLMs with classification or value heads, probes and logit scoring**
- Classification-head fine-tuning of tiny LMs (Jul 2026): LoRA plus a discriminative head on Qwen3 0.6B–8B "reliably outperforms label generation (+2-3%)" at 0.6B and 1.7B, and reaches state of the art among the smallest models on HellaSwag, WinoGrande and PIQA — [arXiv 2607.03801](https://arxiv.org/abs/2607.03801)
- Embedding-based vs instruction-based fine-tuning of causal LLMs up to 8B (Dec 2025, revised May 2026): a final-token classification head "matches or exceeds fine-tuned BERT baselines on single-label classification while training 10-30x fewer parameters". Generative (instruction) tuning was competitive only for multi-label tasks, and only with at least 100M trainable parameters — [arXiv 2512.12677](https://arxiv.org/abs/2512.12677)
- Token- and layer-selective probes (ACL 2026, Jan 2026): lightweight probes of up to 35M params over the full token-by-layer hidden-state tensor classify during the same forward pass used for generation. They match much larger task-specific baselines on safety and sentiment, outperform logit-only reuse (MULI), and keep "near-serving latency". Tested on Llama-3.2-3B, GPT-OSS-20B and Qwen3-30B-A3B — [arXiv 2601.13288](https://arxiv.org/abs/2601.13288)
- Other 2025–2026 papers on head versus generative classification (titles only, not read in depth): GenCLS++ [arXiv 2504.19898](https://arxiv.org/pdf/2504.19898); CLSGen dual-head (a probabilistic classifier head plus a verbalised explanation) [arXiv 2604.11801](https://arxiv.org/pdf/2604.11801)
- Classification heads on decoder LLMs risk catastrophic forgetting or "linguistic collapse" of generation, whereas next-token label scoring keeps generative ability — [arXiv 2512.12677 (alphaXiv)](https://www.alphaxiv.org/abs/2512.12677v1)

**C. Tool tokens, hidden-state tool selectors and "action heads"**
- ToolkenGPT (2023, older): each tool is a learned "toolken" embedding added to a frozen LLM, so choosing a tool is a single next-token prediction over tools — [arXiv 2305.11554](https://arxiv.org/abs/2305.11554)
- ToolGen (ICLR 2025, arXiv Oct 2024): adds one virtual token per tool to the vocabulary and trains in three stages (tool memorisation, retrieval training, end-to-end agent tuning). Evaluated with more than 47,000 tools, it unifies retrieval and calling in generation — [arXiv 2410.03439](https://arxiv.org/abs/2410.03439), [GitHub](https://github.com/Reason-Wang/ToolGen)
- Chain-of-Tools / CoTools (Mar 2025): the LLM stays frozen. A "Tool Judge" reads the hidden state at each token to decide whether to call a tool, and a "Tool Retriever" embeds the query to pick from a large pool, including tools never seen in training. Parameters are then filled with an in-context-learning prompt (generatively). Evaluated on GSM8K-XL, FuncQA, KAMEL and SimpleToolQuestions — [arXiv 2503.16779](https://arxiv.org/pdf/2503.16779), [GitHub](https://github.com/fairyshine/Chain-of-Tools)
- "Action heads" (an MLP with one output per discrete action on top of an LLM) appear mainly in RL-for-agents work (for example GLAM, 2023, older), not in production tool-calling models — [arXiv 2302.02662](https://arxiv.org/pdf/2302.02662)
- A 2026 survey of agentic tool use lists ToolLLM (16,464 APIs), Gorilla, AnyTool and ToolGen ("virtual tool tokens") as the main approaches to scaling the tool catalogue — [arXiv 2604.00835](https://arxiv.org/html/2604.00835v1)

**D. Small function-calling models** (BFCL v4 overall scores are in Key Question 2)
- Salesforce xLAM-2 (APIGen-MT, Apr 2025), in 1B, 3B, 8B, 32B and 70B "fc-r" sizes. On BFCL v3, 70B scored 78.19% and 32B 75.83% (the top two at the time). BFCL v3 multi-turn accuracy was 75.12% for 70B, 69.25% for 8B, 56.00% for 3B and 43.12% for 1B, against o1 at 36% and GPT-4o FC at 41%. On tau-bench, 70B scored 56.2% overall — [arXiv 2504.03601](https://arxiv.org/pdf/2504.03601), [APIGen-MT site](https://apigen-mt.github.io/)
- xLAM-2 is licensed **cc-by-nc-4.0 (non-commercial)** — [BFCL leaderboard data](https://gorilla.cs.berkeley.edu/data_overall.csv)
- Hammer2.1 (MadeAgents): 0.5B, 1.5B, 3B and 7B models built on Qwen2.5-Coder, using "function masking" so the model is robust to misleading function names and to irrelevant calls. Licences are cc-by-nc-4.0 or qwen-research depending on size — [HF Hammer2.1-3b](https://huggingface.co/MadeAgents/Hammer2.1-3b), [arXiv 2410.04587 (older)](https://arxiv.org/html/2410.04587v2), [BFCL data](https://gorilla.cs.berkeley.edu/data_overall.csv)
- Google FunctionGemma (Dec 2025; card updated 16 Apr 2026): 270M params, 32K context. The model card lists an Apache 2.0 licence plus Gemma terms of use. BFCL zero-shot scores: simple 61.6%, multiple 63.5%, parallel 39%, parallel-multiple 29.5%, relevance 61.1%, irrelevance 73.7%. Mobile Actions accuracy is 58% out of the box and 85% after fine-tuning. On a Samsung S25 Ultra CPU with int8 it gives about 1,718 tok/s prefill, about 125.9 tok/s decode, 0.3 s time to first token, a 288 MB model and 551 MB peak memory — [FunctionGemma model card](https://ai.google.dev/gemma/docs/functiongemma/model_card)
- FunctionGemma multi-turn: 10–39% out of the box, 90–97% after task-specific fine-tuning (vendor blog) — [distil labs](https://www.distillabs.ai/blog/making-functiongemma-work-multi-turn-tool-calling-at-270m-parameters/)
- Katanemo Arch-Function (1.5B–7B; launched Sep 2024 at Top-7 on BFCL), Arch-Function-Chat (Feb 2025) and Arch-Agent (1.5B–32B; claimed Top-3 on BFCL at launch). All are under the Katanemo research licence — [GitHub katanemo/Arch-Function](https://github.com/katanemo/Arch-Function), [BFCL data](https://gorilla.cs.berkeley.edu/data_overall.csv)
- NVIDIA Nemotron 3 Nano (Dec 2025): a hybrid Mamba-Transformer MoE with 30B total and about 3B active parameters, 1M context, built for tool calling and agents, with 4x the throughput of Nemotron 2 Nano. Nemotron 3 Nano Omni (Apr 2026) adds multimodality — [NVIDIA newsroom](https://nvidianews.nvidia.com/news/nvidia-debuts-nemotron-3-family-of-open-models), [DeepInfra blog](https://deepinfra.com/blog/nemotron-3-nano-nvidia-efficient-small-llm)
- ToolACE-2-8B (Huawei Noah's Ark and USTC) is Apache-2.0 — [BFCL data](https://gorilla.cs.berkeley.edu/data_overall.csv)

**E. Routers (model and route selection)**
- RouteLLM (LMSYS, 2024, older; Apache-2.0) offers matrix-factorisation, SW-ranking, BERT-classifier and causal-LLM-classifier routers. They were trained on Chatbot Arena preference data for a GPT-4 versus Mixtral pair and claim "up to 85%" cost reduction at 95% of GPT-4's quality on MT-Bench — [GitHub lm-sys/RouteLLM](https://github.com/lm-sys/routellm). A secondary summary adds 45% on MMLU and 35% on GSM8K — [NeuralTrust blog](https://neuraltrust.ai/blog/llm-model-routing)
- NVIDIA LLM Router blueprint: the nvidia/prompt-task-and-complexity-classifier puts several classification heads (task type, and complexity dimensions such as creativity, reasoning, contextual knowledge, domain knowledge and constraints) on a DeBERTa-v3-base backbone of about 86M parameters. It is served on Triton behind a Rust proxy. This is a one-pass multi-head classifier, distilled from labelling — [HF model card](https://huggingface.co/nvidia/prompt-task-and-complexity-classifier), [NVIDIA blog](https://developer.nvidia.com/blog/deploying-the-nvidia-ai-blueprint-for-cost-efficient-llm-routing/), [GitHub blueprint](https://github.com/NVIDIA-AI-Blueprints/llm-router)
- Katanemo Arch-Router-1.5B (Jun 2025; Qwen2.5-1.5B base; Katanemo Research License) generates a short JSON `{"route": "name"}` over user-defined domain and action policies — [HF card](https://huggingface.co/katanemo/Arch-Router-1.5B). It reports 93.17% routing accuracy at about 51 ms, or 50 ms p50 and under 75 ms p99, against about 1 s for proprietary LLMs picking a route (roughly 28x faster) — [arXiv 2506.16655](https://arxiv.org/abs/2506.16655), [Plano blog](https://planoai.dev/blog/arch-router-outperforming-foundational-models-in-llm-routing-with-a-1-5b-model), [VentureBeat](https://venturebeat.com/ai/new-1-5b-router-model-achieves-93-accuracy-without-costly-retraining)
- Aurelio semantic-router (MIT) routes by embedding similarity to example utterances and scales to thousands of routes. A secondary source claims latency falls from about 5,000 ms (an LLM deciding) to about 100 ms — [Deepchecks glossary](https://deepchecks.com/glossary/semantic-router/), [Aurelio docs](https://docs.aurelio.ai/docs/semantic-router/user-guide/features/threshold-optimization). There is also a vLLM Semantic Router — [arXiv 2510.08731](https://arxiv.org/abs/2510.08731)
- SCX Router (2 Sep 2026, Knowledgator authors): a GLiClass-based router using a Qwen3-0.6B decoder and a shallow bidirectional scorer. The decoder's KV cache is reused across the session so only new turns are encoded ("decoder-KV classifier"). It also predicts task type, difficulty, reasoning mode and output length. Top-1 aggregate score is 0.707 against 0.696 for the best fixed model on LiveBench subsets. The ontology has 23 families, 115 task types and 345 subtypes, and training used 150k verifier-scored tasks — [arXiv 2609.02292](https://arxiv.org/abs/2609.02292)
- Prefill-activation router (Mar 2026, revised Aug 2026): an MLP ("SharedTrunkNet") on residual-stream activations of an open encoder LLM predicts per-model correctness, including for closed models. It closes 45.58% of the gap between the best single model and the oracle and saves 74.31% of cost relative to the most expensive model — [arXiv 2603.20895](https://arxiv.org/abs/2603.20895)
- Outcome-aware tool selection for semantic routers (Mar 2026) moves tool embeddings toward the centroid of queries on which each tool succeeded. It adds nothing at runtime and runs in single-digit milliseconds on CPU. MetaTool (199 tools) NDCG@5 rises from 0.869 to 0.940 and ToolBench (2,413 APIs) from 0.834 to 0.848. A 2,625-parameter MLP re-ranker hurts when outcome data is sparse — [arXiv 2603.13426](https://arxiv.org/abs/2603.13426)

**F. JEPA-style and embedding-prediction approaches**
- LLM-JEPA (Huang, LeCun, Balestriero; Sep 2025, revised Oct 2025) adds a JEPA embedding-prediction objective to LLM fine-tuning and pretraining while keeping generation. It "outperform[s] the standard LLM training objectives by a significant margin" on NL-RX, GSM8K, Spider and RottenTomatoes across Llama3, OpenELM, Gemma2 and OLMo, and is robust to overfitting. Code: github.com/rbalestr-lab/llm-jepa — [arXiv 2509.14252](https://arxiv.org/abs/2509.14252)
- VL-JEPA (Meta et al.; Dec 2025, revised Feb 2026) has 1.6B params and predicts continuous embeddings of the target text instead of tokens. It uses 50% fewer trainable parameters than a comparable token-space VLM and cuts decoding operations 2.85x through selective decoding. It beats CLIP, SigLIP2 and Perception Encoder on 8 video-classification and 8 retrieval datasets, matches InstructBLIP and QwenVL on GQA, TallyQA and POPE, and natively supports open-vocabulary classification and discriminative VQA — [arXiv 2512.10942](https://arxiv.org/abs/2512.10942)

### Inferences
- The strongest one-pass building blocks are (a) label-conditioned encoders (GLiClass-style, which handle unseen labels and keep throughput flat across label count) and (b) probes or heads on decoder hidden states (2601.13288 and 2607.03801), which reuse a forward pass the system already runs. Neither has been benchmarked on BFCL-style tool selection.
- VL-JEPA's "predict an embedding, then match it against label or text embeddings" is the direct analogue of a non-generative tool selector: predict a tool or action embedding and do a nearest-neighbour lookup over tool-description embeddings. I found no paper that applies this to text-only tool calling.
- Arch-Router (about 50 ms) and SCX show the 2025–2026 pattern: a sub-2B decoder that emits a very short output, or is read through a scorer head, can match large proprietary LLMs on routing. That is essentially what a "fast decision model" is.

### Gaps
- No verified parameter counts or model-card licences were retrieved for ModernBERT base and large, for Ettin, or for NVIDIA's prompt-task-and-complexity-classifier. Check the Hugging Face cards.
- I did not retrieve LLM-JEPA's numeric gains or compute overhead; the abstract gives no numbers. It is unclear whether LLM-JEPA changes inference cost, because it keeps generation.
- No 2025–2026 successor to ToolkenGPT or ToolGen that fills arguments in one forward pass was found. Chain-of-Tools and ToolGen still generate the parameters.
- GLiNER's own benchmark numbers, and any use of GLiNER-style span extraction to fill tool arguments, were not found.
- NVIDIA "small tool models": I found no BFCL numbers for Nemotron 3 Nano or Nemotron-Mini-4B-Instruct.

## Key Question 2: What are the relevant benchmarks and leaderboards, and what are current top scores and small-model latencies?

### Takeaway
BFCL v4 (the official leaderboard was last updated 12 Apr 2026) is the de facto tool-calling benchmark. The top overall score is about 77% (Claude Opus 4.5). The best open models under about 8B score only 30–51%, and BFCL's reported mean latencies for small open models are 2–50 seconds, because every entry is a generative decoder. No encoder, classifier-head or router-style model appears on BFCL at all. Router benchmarks (RouterBench, LLMRouterBench) find that many routers do not beat simple baselines. Intent benchmarks (CLINC150, BANKING77) are mature but I found no fresh 2025–2026 SOTA figures.

### Cited Findings

**BFCL v4 (official)**
- The BFCL V4 page was last updated 12 Apr 2026, on evaluation commit f7cf735 (`pip install bfcl-eval==2025.12.17`). V4 adds "holistic agentic evaluation" and reports accuracy, latency and cost — [Gorilla BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html)
- Aggregator description of the v4 category weights: Agentic 40%, Multi-Turn 30%, Live 10%, Non-Live 10%, Hallucination 10% — [BenchLM.ai](https://benchlm.ai/benchmarks/bfcl-v4). That site also states v4 was released in April 2026, which may confuse the release date with the last update; not confirmed.
- Top of the official board (overall accuracy, mean latency in s, organisation, licence) — [BFCL data_overall.csv](https://gorilla.cs.berkeley.edu/data_overall.csv):
  - #1 Claude-Opus-4.5 (FC): 77.47%, 4.38 s
  - #2 Claude-Sonnet-4.5 (FC): 73.24%, 4.31 s
  - #3 Gemini-3-Pro-Preview (Prompt): 72.51%, 12.08 s
  - #4 GLM-4.6 (FC thinking, MIT): 72.38%, 4.34 s. This is the top open-weight model.
  - #6 Claude-Haiku-4.5 (FC): 68.70%, 1.68 s. This is the fastest high scorer.
- Small and mid open models on BFCL v4 (same source):

| Rank | Model | Overall | Mean latency (s) | Licence |
|---|---|---|---|---|
| 18 | xLAM-2-32b-fc-r | 54.66% | 6.94 | cc-by-nc-4.0 |
| 25 | Nanbeige4-3B-Thinking-2511 | 51.40% | 13.46 | Apache-2.0 |
| 34 | xLAM-2-8b-fc-r | 46.68% | 22.65 | cc-by-nc-4.0 |
| 37 | Arch-Agent-32B | 45.37% | 9.44 | katanemo-research |
| 39 | Qwen3-8B (FC) | 42.57% | 51.36 | Apache-2.0 |
| 40 | ToolACE-2-8B | 42.44% | 15.95 | Apache-2.0 |
| 41 | Qwen3-30B-A3B-Instruct-2507 | 41.39% | 5.95 | Apache-2.0 |
| 42 | xLAM-2-3b-fc-r | 41.22% | 3.80 | cc-by-nc-4.0 |
| 54 | Qwen3-4B-Instruct-2507 | 35.68% | 7.61 | Apache-2.0 |
| 56 | Arch-Agent-3B | 35.36% | 3.56 | katanemo-research |
| 60 | Arch-Agent-1.5B | 32.14% | 2.38 | katanemo-research |
| 65 | xLAM-2-1b-fc-r | 30.44% | 2.84 | cc-by-nc-4.0 |
| 68 | Hammer2.1-3b | 29.71% | 11.24 | qwen-research |
| 71 | Qwen3-1.7B | 28.41% | 5.12 | Apache-2.0 |
| 75 | Hammer2.1-1.5b | 27.88% | 6.28 | cc-by-nc-4.0 |
| 81 | Granite-3.1-8B-Instruct | 27.10% | 13.23 | Apache-2.0 |
| 100 | Hammer2.1-0.5b | 21.22% | 2.79 | cc-by-nc-4.0 |
| 103 | Granite-4.0-350m | 18.98% | 1.74 | Apache-2.0 |
| 107 | Llama-3.2-1B-Instruct | 10.82% | 3.21 | Llama 3 Community |

  For comparison, the small proprietary models GPT-4.1-mini scored 50.45% at 1.32 s and GPT-4.1-nano 33.05% at 1.44 s — [BFCL data_overall.csv](https://gorilla.cs.berkeley.edu/data_overall.csv). FunctionGemma was not among the rows returned.
- Conflicting aggregator data: llm-stats.com and BenchLM list other leaders ("BTL-3" at 88.5%, "Atria Dawn Preview" at 77.0%, "Qwen3.7 Max" at 75.0%) on a 22-model subset — [llm-stats](https://llm-stats.com/benchmarks/bfcl-v4), [BenchLM](https://benchlm.ai/benchmarks/bfcl-v4). These do not match the official CSV. Treat them as unverified or as self-reported.
- On BFCL v3 (older generation), xLAM-2-70b and xLAM-2-32b were #1 and #2 at 78.19% and 75.83% — [arXiv 2504.03601](https://arxiv.org/pdf/2504.03601)

**tau-bench / tau2-bench**
- tau2-bench (Sierra) tests multi-turn tool-agent-user interaction in the airline, retail and telecom domains, with a public submissions leaderboard — [GitHub sierra-research/tau2-bench](https://github.com/sierra-research/tau2-bench)
- xLAM-2-70b reached 56.2% on tau-bench (v1), against 38.2% for Llama-3.1-70B-Instruct and 40.6% for DeepSeek-V3 — [arXiv 2504.03601](https://arxiv.org/pdf/2504.03601)
- An aggregator claims tau2 is topped by GLM-5.2 at 99.1% as of 16 Aug 2026. This is unverified, and the domain was not specified — [pricepertoken](https://pricepertoken.com/leaderboards/benchmark/tau2)

**Tool retrieval and selection benchmarks**
- ToolRet (ACL 2025 Findings): even the best general IR model, NV-embed-v1, reaches only nDCG@10 = 33.83. It comes with a training set of more than 200k examples — [ACL Anthology](https://aclanthology.org/2025.findings-acl.1258/), [arXiv 2503.01763](https://arxiv.org/html/2503.01763)
- "Tool Retrievers Are Underestimated" (Sep 2026): 67.9% of sub-queries have functionally equivalent tool alternatives, so valid combinations per query rise from 1 to 5.3. Under this correction, 30–47% of reported fine-tuning gains turn out to be evaluation artefacts — [arXiv 2609.08327](https://arxiv.org/abs/2609.08327)
- MetaTool (199 tools, about 4,287 queries) and ToolBench (2,413 APIs in the subset used) serve as tool-selection testbeds for router-style selectors — [arXiv 2603.13426](https://arxiv.org/abs/2603.13426)
- LLMCert-T (Oct 2025, revised May 2026): on BFCL and OpenAPI tool pools with distractor or Top-N-saturation adversaries, the certified correctness upper bounds for tool selection drop to about 20% — [arXiv 2510.03992](https://arxiv.org/abs/2510.03992)

**Router benchmarks**
- RouterBench (2024, older): more than 405k inference outcomes, 8 datasets, 11 LLMs — [arXiv 2403.12031](https://arxiv.org/abs/2403.12031)
- LLMRouterBench (Jan 2026): more than 400k instances, 21 datasets, 33 models and 10 routing baselines. "Many routing methods exhibit similar performance... several recent approaches, including commercial routers, fail to reliably outperform a simple baseline." A large gap to the oracle remains, driven by "model-recall failures", and the choice of embedding model barely matters — [arXiv 2601.07206](https://arxiv.org/abs/2601.07206)
- Four open-source routers on RouterBench, BFCL v4, tau2-bench and WebArena (Jul 2026): three of the four "emit constant or near-constant tier assignments". "Always-Mid matches Aurelio exactly on three benchmarks", and vLLM Semantic Router, the only one that varies materially with the prompt, is best on none — [arXiv 2608.14641](https://arxiv.org/abs/2608.14641)
- VL-RouterBench (Dec 2025) covers vision-language model routing — [arXiv 2512.23562](https://arxiv.org/pdf/2512.23562)

**Intent benchmarks**
- CLINC150 has 23,700 queries (22,500 in-scope across 150 intents and 10 domains, plus 1,200 out-of-scope). BANKING77 has 13,083 queries across 77 banking intents. CPFT (contrastive pre-training plus fine-tuning) has been cited as SOTA (older) — [IntenDD arXiv 2310.16761](https://arxiv.org/pdf/2310.16761), [Few-Shot-Intent-Detection repo](https://github.com/jianguoz/Few-Shot-Intent-Detection)

### Inferences
- BFCL latency numbers for small open models (2–50 s mean) are dominated by generative decoding, reasoning traces ("thinking" variants) and the harness hardware, not by the decision itself. A system that emits a tool distribution in one pass plus a short argument decode could show order-of-magnitude latency gains on the same accuracy axis. Nobody has published such a Pareto plot.
- Among permissively licensed small models, the strongest BFCL v4 entries are Nanbeige4-3B-Thinking (51.4%, but slow), Qwen3-8B, ToolACE-2-8B and Qwen3-4B. The higher-scoring xLAM-2, Arch and Hammer models are non-commercial or research-licensed, which matters for a startup that wants to build on them.

### Gaps
- I could not retrieve the per-category BFCL v4 breakdown (agentic web-search and memory, multi-turn, relevance and irrelevance) for small models, or BFCL's exact latency methodology (hardware for open models). Check the leaderboard's per-category CSV.
- No verified 2025–2026 SOTA accuracy for CLINC150 or BANKING77, and no MTEB classification leaderboard values, were retrieved.
- API-Bank and NexusRaven were not researched; both are older (2023) and largely superseded by BFCL. No current top scores are given here.
- The official tau2-bench numbers for small open models were not found. The aggregator data is unverified.

## Key Question 3: Which techniques drive latency toward one forward pass?

### Takeaway
2026 has seen a burst of tool-call-specific acceleration. SimpleTool (parallel decoding of name and arguments, 3–6x faster), ToolSpec (schema-aware speculation, up to 4.2x) and OoO-Spec (a 0.6B sidecar that predicts the function and argument slots, 3.89x on average) all cut the argument-decoding cost. ReCache and stateful inference cut the prefill cost of tool schemas and multi-turn history (3.7x faster to first token, 2–4x per turn). Constrained decoding is now close to free (under 50 µs per token). Early exit is losing value on modern LLMs. Classification heads and probes on hidden states give true one-pass decisions but have not been combined with argument filling.

### Cited Findings

**Parallel or speculative decoding specialised for tool calls**
- SimpleTool (Feb 2026) uses special tokens that compress low-entropy output tokens 4–6x and let the function name and each argument be generated in parallel. It reports 3–6x end-to-end speedup (up to 9.6x) with +8.2% parallelisation overhead. On a quantised 4B model on a consumer GPU it reaches 61.2 ms P50, enough for 16 Hz control. ST-Qwen-0.5B beats FunctionGemma on Mobile Actions in both accuracy and latency consistency. Tested on Qwen models from 0.5B to 14B across five benchmarks — [arXiv 2603.00030](https://arxiv.org/abs/2603.00030)
- SimpleTool also notes that Medusa, EAGLE and draft-model speculation gain less on short outputs such as function calls, because of their overhead — [arXiv 2603.00030 (HTML)](https://arxiv.org/html/2603.00030)
- ToolSpec (Apr 2026): a finite-state machine alternates between deterministic schema-token filling and speculation for variable fields, and retrieves similar past invocations as drafts. It is training-free and plug-and-play, with up to 4.2x speedup — [arXiv 2604.13519](https://arxiv.org/abs/2604.13519)
- OoO-Spec (Aug 2026): a Qwen3-0.6B sidecar predicts the function and argument values out of order while the target model decodes, and the target model still verifies (lossless). It is 2.46x–5.34x faster than autoregressive decoding (mean 3.89x), against 2.95x for ToolSpec, and 34.1% better than ToolSpec on average on Qwen3 4B–32B. It covered 7 target models and 3 benchmarks, with a semantic payload of about 85 bytes per request — [arXiv 2608.00814](https://arxiv.org/abs/2608.00814)

**KV-cache reuse of tool schemas and multi-turn state**
- ReCache (Aug 2026): tool and skill schemas recur "in different combinations and orders", which defeats prefix caching. Resource-wise attention makes the KV blocks independent of composition, and pruning then trims fields. Time to first token is 3.655x faster, KV memory falls 92.43%, and Inv-F1 is 82.3 against 82.4 for dense attention — [arXiv 2608.19662](https://arxiv.org/abs/2608.19662)
- Stateful inference for multi-agent tool calling (May 2026): a persistent KV cache, a radix prefix cache and prompt-lookup speculative decoding for structured output. It is 2.1x faster per turn on a 6-turn workflow and 4.2x on the median turn of a 35-turn workflow, halving end-to-end wall time, against vLLM and SGLang. 85–95% of the prompt is unchanged from turn to turn — [arXiv 2605.26289](https://arxiv.org/abs/2605.26289)
- Practitioner figures (vendor blog): a 4-tool schema adds 400–800 prompt tokens, vLLM `--enable-prefix-caching` reuses the schema KV, and agent loops reach 70–90% cache hit rates — [Spheron blog](https://www.spheron.network/blog/tool-calling-benchmarks-bfcl-tau-bench-latency-optimization/)
- SCX Router keeps the decoder KV cache across a session and encodes only new turns — [arXiv 2609.02292](https://arxiv.org/abs/2609.02292)

**Constrained decoding**
- XGrammar (Nov 2024, older paper) precomputes the validity of the more than 99% of tokens that do not depend on context. Secondary sources report masks computed in under 40 µs per token and XGrammar as the default backend in vLLM, SGLang and TensorRT-LLM as of Mar 2026. llguidance takes about 50 µs per token and can beat unconstrained decoding when the grammar forces the next token — [XGrammar arXiv 2411.15100](https://arxiv.org/pdf/2411.15100), [Let's Data Science](https://letsdatascience.com/blog/structured-outputs-making-llms-return-reliable-json)
- 2026 follow-ups on faster grammar masks: token-space compression [arXiv 2605.29986](https://arxiv.org/pdf/2605.29986) and parser-stack classification [arXiv 2608.03065](https://arxiv.org/pdf/2608.03065) (titles only)

**First-token scoring, classification heads and probes**
- Classification heads beat label generation by 2–3% at 0.6B–1.7B — [arXiv 2607.03801](https://arxiv.org/abs/2607.03801). Final-token-embedding heads match BERT with 10–30x fewer trainable parameters — [arXiv 2512.12677](https://arxiv.org/abs/2512.12677)
- Probes on hidden states classify inside the serving forward pass at "near-serving latency", which removes the need for a separate guard or classifier model — [arXiv 2601.13288](https://arxiv.org/abs/2601.13288)
- Arch-Router's latency is "primarily driven by the length of the output". It emits only a short route name, which gives about 50 ms p50 — [Plano blog](https://planoai.dev/blog/arch-router-outperforming-foundational-models-in-llm-routing-with-a-1-5b-model), [VentureBeat](https://venturebeat.com/ai/new-1-5b-router-model-achieves-93-accuracy-without-costly-retraining)

**Early exit**
- "The Diminishing Returns of Early-Exit Decoding in Modern LLMs" (Mar 2026): early-exit potential shrinks in newer models because better pretraining reduces layer redundancy. Dense models and models above about 20B parameters retain the most potential — [arXiv 2603.23701](https://arxiv.org/abs/2603.23701)
- HELIOS (MLSys 2026) serves early-exit LLMs by selecting both the model and the exit adaptively — [MLSys 2026](https://mlsys.org/virtual/2026/oral/3846)

**Distilling a large model into a classifier or router**
- NVIDIA's router is a DeBERTa-v3-base multi-head classifier of about 86M parameters — [HF card](https://huggingface.co/nvidia/prompt-task-and-complexity-classifier)
- The prefill-activation router distils per-model correctness into an MLP on activations — [arXiv 2603.20895](https://arxiv.org/abs/2603.20895)
- Outcome-aware embedding interpolation runs in single-digit milliseconds on CPU with no LLM inference — [arXiv 2603.13426](https://arxiv.org/abs/2603.13426)
- A router survey (Mar 2026) says predictive routers built on light external classifiers (RouteLLM, FORC, GraphRouter) have the lowest latency, while cascade or generative routers can take longer than the LLM call itself — [arXiv 2603.04445](https://arxiv.org/html/2603.04445v1) (as summarised in search results). A quality-estimation classifier at about 20.7 ms per query (48.3 queries/s) is quoted in the same search results; I could not confirm which paper it comes from.

### Inferences
- The latency stack a small team could assemble today is:
  1. A cached tool-schema KV (ReCache-style, order-invariant) to remove schema prefill.
  2. A one-pass tool distribution from a hidden-state head or a GLiClass-style label-conditioned scorer.
  3. Only if a tool is chosen, parallel or speculative argument filling (SimpleTool or OoO-Spec), under XGrammar constraints.

  Each piece is published separately with 2–5x gains. No paper combines them or reports the combined Pareto front.
- Early exit looks like the weakest bet on 2026-era small models, given 2603.23701.

### Gaps
- No paper reports accuracy on BFCL (or tau2) for a model whose tool-name decision comes from a single forward-pass head rather than generation.
- Absolute per-request latency for SimpleTool, ToolSpec and OoO-Spec on BFCL itself, and on commodity CPUs, was not retrieved (only speedups and the 61.2 ms P50 figure).
- ReCache's model names and absolute milliseconds are not in its abstract.

## Key Question 4: What is still missing or weak, where a small team could plausibly beat the state of the art?

### Takeaway
The clearest openings are:
1. A single model that outputs a calibrated distribution over tools (including "no tool") in one pass and then fills arguments quickly and in parallel. Today selection-only classifiers and generation-only function callers are separate.
2. Calibration and robustness of that distribution. Agents are miscalibrated, and certified tool-selection correctness collapses to about 20% under distractors.
3. Unseen tools. Tool-token methods need retraining, and retrievers score about 34 nDCG@10 on ToolRet.
4. A permissively licensed small model competitive with the non-commercial xLAM-2 and Arch families.
5. The first published latency–accuracy Pareto front for decision models on BFCL, tau2 and routing benchmarks, where current router evaluations show many methods no better than constant baselines.

### Cited Findings
- **Argument filling is generative everywhere.** Chain-of-Tools selects unseen tools from hidden states but fills parameters with an in-context-learning prompt — [arXiv 2503.16779](https://arxiv.org/pdf/2503.16779). ToolGen generates parameters after the tool token — [arXiv 2410.03439](https://arxiv.org/abs/2410.03439). GLiClass and NVIDIA's classifier output labels only — [HF GLiClass](https://huggingface.co/knowledgator/gliclass-modern-base-v3.0), [HF NVIDIA](https://huggingface.co/nvidia/prompt-task-and-complexity-classifier)
- **Arguments are nearly independent**, which is what makes parallel filling possible. SimpleTool exploits "weak causal dependencies between arguments" — [arXiv 2603.00030](https://arxiv.org/abs/2603.00030). OoO-Spec finds the function and many argument values "can often be inferred directly from the request and schema" before the decoder reaches them — [arXiv 2608.00814](https://arxiv.org/html/2608.00814)
- **Small models are weak at multi-step and multi-turn work.** On BFCL v3 multi-turn, xLAM-2-1b scores 43.12% against 75.12% for xLAM-2-70b — [arXiv 2504.03601](https://arxiv.org/pdf/2504.03601). FunctionGemma gets 10–39% on multi-turn out of the box — [distil labs](https://www.distillabs.ai/blog/making-functiongemma-work-multi-turn-tool-calling-at-270m-parameters/). Its parallel and parallel-multiple BFCL scores are 39% and 29.5% — [model card](https://ai.google.dev/gemma/docs/functiongemma/model_card)
- **Calibration is under-studied and poor.** "Calibration in autonomous agents remains notably sparse". Evidence tools such as web search make agents badly overconfident, verification tools such as code execution reduce the problem, and an RL recipe jointly optimises accuracy and calibration — [arXiv 2601.07264](https://arxiv.org/abs/2601.07264)
- Agentic Confidence Calibration (Jan 2026): an early low-confidence mistake, such as picking the wrong tool, can "poison" the whole trajectory — [arXiv 2601.15778](https://arxiv.org/html/2601.15778v1)
- An earlier approach (EMNLP 2024, older) calibrated tool-agent confidence with an MLP on LLM embeddings trained against execution outcomes — [ACL Anthology](https://aclanthology.org/2024.findings-emnlp.978.pdf)
- A 2026 taxonomy and evaluation protocol for uncertainty quantification in LLM agents also exists — [arXiv 2609.07395](https://arxiv.org/pdf/2609.07395)
- **Robustness to distractor tools is weak.** Certified correctness bounds fall to about 20% under distractor selection or Top-N saturation — [arXiv 2510.03992](https://arxiv.org/abs/2510.03992)
- **Unseen tools and retrieval.**
  - ToolkenGPT and ToolGen assign a trained token per tool, so new tools need new embeddings or training — [ToolkenGPT](https://arxiv.org/abs/2305.11554), [ToolGen](https://arxiv.org/abs/2410.03439)
  - The best general retriever reaches nDCG@10 = 33.83 on ToolRet — [ACL 2025](https://aclanthology.org/2025.findings-acl.1258/)
  - Benchmark annotation undercounts equivalent tools, and 30–47% of claimed gains are artefacts — [arXiv 2609.08327](https://arxiv.org/abs/2609.08327)
  - Outcome-aware embedding interpolation helps (MetaTool NDCG@5 0.869 to 0.940), but learned re-rankers fail when outcome data is sparse — [arXiv 2603.13426](https://arxiv.org/abs/2603.13426)
- **Router evaluation is shaky.** Many routers, including commercial ones, fail to beat simple baselines reliably, and a large oracle gap remains — [arXiv 2601.07206](https://arxiv.org/abs/2601.07206). Three of four open routers emit near-constant tiers on RouterBench, BFCL v4, tau2 and WebArena — [arXiv 2608.14641](https://arxiv.org/abs/2608.14641). Activation-based routing closes only 45.58% of the gap to the oracle — [arXiv 2603.20895](https://arxiv.org/abs/2603.20895)
- **Licensing.** Several of the best small function-calling families are non-commercial or research-only: xLAM-2 (cc-by-nc-4.0), Hammer2.1 (cc-by-nc-4.0 or qwen-research), Arch-Agent (katanemo-research) and Arch-Router (Katanemo Research License). Permissive options include Qwen3 (Apache-2.0), ToolACE-2-8B (Apache-2.0), Granite (Apache-2.0), Nanbeige4-3B (Apache-2.0) and GLiClass-modern-base-v3 (Apache-2.0) — [BFCL data](https://gorilla.cs.berkeley.edu/data_overall.csv), [HF Arch-Router](https://huggingface.co/katanemo/Arch-Router-1.5B), [HF GLiClass](https://huggingface.co/knowledgator/gliclass-modern-base-v3.0)
- **Encoders win on classification per parameter, but nobody applies them to function calling.** A 400M Ettin encoder beats a 1B decoder on classification — [HF paper page](https://huggingface.co/papers/2507.11412). Yet no encoder-based entry appears on BFCL v4 — [BFCL data](https://gorilla.cs.berkeley.edu/data_overall.csv)
- **JEPA for decisions is untested.** VL-JEPA shows that embedding prediction plus selective decoding supports open-vocabulary classification with 2.85x fewer decoding operations — [arXiv 2512.10942](https://arxiv.org/abs/2512.10942). LLM-JEPA improves LLM fine-tuning but keeps generative inference — [arXiv 2509.14252](https://arxiv.org/abs/2509.14252)

### Inferences
These are opportunities for a small team, inferred from the cited evidence rather than stated by the sources.
1. **A "decide-then-fill" hybrid model.** Put a one-pass head on a small decoder or encoder (GLiClass-style label-conditioned scoring over tool descriptions, or a hidden-state probe) that outputs P(tool_i) and P(no tool). Then run only the chosen tool's arguments through parallel, schema-constrained filling (SimpleTool or OoO-Spec style), or through GLiNER-style span extraction for arguments that are copied from the user text. No published system combines these.
2. **Calibrated probabilities as a product feature.** Report ECE and Brier score for the tool distribution, plus selective-prediction curves (abstain or escalate at threshold τ). BFCL does not measure calibration, and the agent-calibration papers are 2026-new. A "decision model" that is calibrated out of the box could beat larger models on escalation-cost metrics even at equal top-1 accuracy.
3. **Zero-shot tools by conditioning on descriptions** rather than learned tool tokens, trained with the equivalence-aware labels of 2609.08327 and hardened against the distractor and Top-N attacks of 2510.03992.
4. **The first latency–accuracy Pareto front.** Publish BFCL v4 (relevance, irrelevance, simple, multiple and multi-turn) and tau2 accuracy against p50 and p99 latency on a fixed GPU and CPU, for encoders, head-based models, the FC SLMs above and the speculative methods. BFCL's current latency column is dominated by generative decoding, and no one has published this plot.
5. **A permissive licence** (Apache-2.0 or MIT) is itself a differentiator against xLAM-2, Arch and Hammer.
6. **A realistic target.** Beating GPT-4.1-nano (33.05% at 1.44 s) or xLAM-2-3b (41.22%) on BFCL v4 overall accuracy at a small fraction of their latency looks plausible. Matching the 70–77% frontier with a sub-1B one-pass model looks implausible on multi-turn and agentic categories. Scope claims to tool and route selection plus simple argument filling.

### Gaps
- I found no published calibration metrics (ECE or Brier) for any small function-calling model or router on BFCL or tau2.
- I found no public Pareto curves (latency against accuracy) for decision or tool-selection models. The BFCL latency column is the closest proxy, and its methodology for open models was not verified.
- I found no evidence of GLiNER-style span-extraction argument filling, or of JEPA-style tool selection, in the 2025–2026 literature. They may be absent or simply not surfaced by my searches.
- The proprietary "JEV / TypeSafe AI" model was out of scope, so this survey does not include a head-to-head comparison with it.
