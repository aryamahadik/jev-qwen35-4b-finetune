# R_retrieval: can retrieval (RAG) close C1's knowledge gap to Jev?

Researcher: retrieval. Date: 3 Oct 2026. Web research only (no Modal, no paid calls, no local data opened).

## TL;DR (plain words)

1. **Retrieval is a small lever for this gap.** On DI's Knowledge & Reasoning area it can realistically add about **+0.5 to +1.7 area points (+0.1 to +0.3 index points)**. The index gap is 4.68 points.
2. Most of the knowledge-area gap is **reasoning or computation, not missing facts.** GSM8K, CRUXEval, ChessBench and CLadder make up 54% of the gap, and retrieval does not help them. GPQA makes up 37%. Qwen3.5-4B itself scores **76.2 on GPQA Diamond in thinking mode** (model card), while C1 gets 39.8 in one pass. So the 4B weights already hold most of the GPQA knowledge. What C1 lacks there is thinking time, not facts.
3. Where retrieval does help (the MMLU-style fact part), the published gains for **4-8B models are +2 to +4 points**, and they **shrink as the base model gets stronger**. C1 is already at 82.5 on MMLU, higher than every RAG baseline in these papers. Expect **+0 to +2 on MMLU**, and only if the model is trained to read passages.
4. If we try it, it must be a **cheap, optional route**: BM25 or a tiny embedder over commercially licensed Wikipedia, used only on knowledge MCQs where C1 is unsure, and passed only if it wins on a dev set that does not overlap DI. On an L4 it adds roughly **40-170 ms**, mostly from the extra prompt tokens.
5. The best retrieval results in the literature come from **ReasonIR-8B** (GPQA 31.3 -> 38.4). That model is **excluded** on two counts: its licence is CC-BY-NC, and it is 8B, bigger than our 4B. **MassiveDS** is also **not commercially cleared**: the card says MIT, but its parts (C4, books, arXiv, peS2o, PubMed) keep their own licences.

## 1. Where the knowledge gap actually is (computed from the given numbers)

DI's "Knowledge & Reasoning" area has 6 benchmarks: MMLU (14,042), GPQA Diamond (198), GSM8K (1,319), ChessBench (5,000), CRUXEval (570) and CLadder (5,000) ([DI README](https://github.com/flaviusburca/decision-index)). The area score is their **unweighted mean**. I checked this: C1 (82.5+39.8+56.7+11.7+51.5+65.1)/6 = 51.2 and Jev 413.3/6 = 68.9, both matching the given area scores.

| Benchmark | C1 | Jev | Gap | Can retrieval help? |
|---|---|---|---|---|
| GPQA Diamond | 39.8 | 78.6 | 38.8 (37% of area gap) | A little. It is built to be "Google-proof" (see section 3). The gap is mostly thinking time: Qwen3.5-4B scores 76.2 in thinking mode |
| GSM8K | 56.7 | 79.9 | 23.2 (22%) | No. Needs arithmetic and reasoning steps |
| CRUXEval | 51.5 | 73.0 | 21.5 (20%) | No. Needs code execution (a tool or reasoning route, not retrieval) |
| MMLU | 82.5 | 92.0 | 9.5 (9%) | **Yes, partly.** This is the main retrieval target |
| CLadder | 65.1 | 72.6 | 7.5 (7%) | No. Formal causal reasoning |
| ChessBench | 11.7 | 17.2 | 5.5 (5%) | No |

**Index effect formula:** index gain = (ΔMMLU + ΔGPQA) / 6 / 5 = (ΔMMLU + ΔGPQA) / 30.
- Realistic case (+1.5 MMLU, +2 GPQA): **+0.12 index points**.
- Optimistic case (+3 MMLU, +7 GPQA): **+0.33 index points**.
- The gap is 4.68, so retrieval closes about 2.5-7% of it.

## 2. Evidence: RAG gains on knowledge MCQ by model size

| Study | Reader model | Datastore / retriever | Closed-book -> RAG |
|---|---|---|---|
| RAG in the Wild 2025 ([arXiv 2507.20059](https://arxiv.org/html/2507.20059v1)) | **Qwen3-4B** | MassiveDS 1.4T, bge-base-en-v1.5, k=5 | MMLU 66.0 -> 68.9 (+2.9); MMLU-Pro 41.1 -> 45.2; **ARC-C 85.3 -> 85.0**; SciQ 53.0 -> 64.1; SimpleQA 6.8 -> 33.9 |
| same | Qwen3-8B | same | MMLU 68.9 -> 71.3 (+2.4); MMLU-Pro 44.6 -> 48.2; **ARC-C 89.0 -> 86.0 (hurts)**; **CSBench 69.8 -> 67.3 (hurts)** |
| same | size trend (MMLU-STEM, relative Δ) | same | Llama-3.2-3B +22.9%; Llama-3.1-8B +12.9%; Qwen3-32B +2.3%; GPT-4o +0.3%. The authors: "benefits of retrieval are largely confined to smaller language models". Reranking top-30 gave only "marginal" gains. LLM-based source routing often did worse than retrieving from all sources |
| MassiveDS ([arXiv 2407.12854](https://arxiv.org/html/2407.12854v1)) | Llama-2-7B | MassiveDS, Contriever-msmarco, k=3 | MMLU 45.8 -> 49.3 (+3.5). Gains grow monotonically with datastore size. Smaller LM + datastore beats a bigger closed-book LM on knowledge tasks (TriviaQA/NQ). Datastore scaling "does not help" weak LMs (Pythia) on MMLU |
| ReasonIR ([arXiv 2504.20595](https://ar5iv.labs.arxiv.org/html/2504.20595)) | Llama-3.1-8B (MMLU), Qwen2.5-7B (GPQA) | filtered MassiveDS | MMLU 71.1 -> 72.0 (Contriever) / 74.1 (GRIT-7B) / **75.0 (ReasonIR-8B)**. GPQA 31.3 -> 36.4 (Contriever) / 32.3 (GRIT) / **38.4 (ReasonIR-8B)** / 33.8 (search engine) |
| MedRAG / MIRAGE ([arXiv 2402.13178](https://arxiv.org/html/2402.13178v1)) | various, MMLU-Med | MedCorp 54.2M snippets, RRF-4, 32 snippets | GPT-4 89.4 -> **87.2 (hurts)**; GPT-3.5 72.9 -> 75.5; Mixtral 74.0 -> 75.9; Llama2-70B 57.4 -> **54.6 (hurts)** |
| Ovadia et al. ([EMNLP 2024](https://aclanthology.org/2024.emnlp-main.15.pdf)) | Mistral-7B | Wikipedia | MMLU-anatomy 55.6 -> 68.1 with RAG vs 57.0 with unsupervised fine-tuning. RAG beats knowledge fine-tuning |
| REPLUG ([arXiv 2301.12652](https://arxiv.org/abs/2301.12652)) | Codex | — | 5-shot MMLU +5.1% |

What this means for C1:
- Gains fall as the closed-book score rises. C1's 82.5 on MMLU is above every baseline listed, so expect the low end: **+0 to +2**.
- Off-target or noisy passages **can lower accuracy**: ARC-C, CSBench, GPT-4 and Llama2-70B on MMLU-Med all dropped. A one-pass model that was never trained to read passages is at higher risk.
- The very large gains (SimpleQA +27 points) are on **long-tail fact lookup**. DI's knowledge area does not have that kind of benchmark.

## 3. Failure case: GPQA is "Google-proof"

From the [GPQA paper](https://ar5iv.labs.arxiv.org/html/2311.12022):
- Non-experts with unrestricted web access spent about 37 minutes per question and scored 33.9% on extended, 30.5% on main and **21.9% on Diamond**. Experts scored 81.2% on Diamond.
- GPT-4 with search scored **38.8% on Diamond, the same as GPT-4 few-shot CoT without search (38.8%)**. On the main set it abstained 37.2% of the time with search, versus 4.0% without.
- The ReasonIR +7.1 on GPQA (section 2) needed an 8B reasoning-trained retriever plus a CoT reader. GPQA Diamond has only 198 items, so one standard error is about 3.5 points, and +5 is within roughly 1.5 SE.
- Qwen3.5-4B's card shows **GPQA Diamond 76.2 and MMLU-Redux 88.8 in thinking mode, the default** ([HF card](https://huggingface.co/Qwen/Qwen3.5-4B)). C1 is a one-pass LoRA model, so the GPQA gap is mostly the no-thinking constraint.
- I was not asked to research thinking routes and did not test this. It points to an optional "think only on hard science MCQ" route (or a code-execution route for CRUXEval and GSM8K) as the larger lever, more than retrieval.

## 4. Which corpora help, and whether we may use them commercially

What helps MMLU-type questions:
- MassiveDS single-domain ablation, Llama-2-7B, MMLU (closed-book 45.8): DPR-Wikipedia 48.3, RPJ-Wikipedia 48.1, Books 48.3, MATH 47.5, peS2o 47.4, PubMed 46.8, StackExchange 46.2, GitHub 45.9, arXiv 45.6, full mix 49.3 ([MassiveDS](https://arxiv.org/html/2407.12854v1)).
- So **Wikipedia and books-like text help most**, and arXiv helps least.
- MedRAG: **Textbooks + BM25 was the best single setup on MMLU-Med (76.7)**. Exam questions match textbook text.

| Corpus | Licence | OK for commercial use? |
|---|---|---|
| English Wikipedia (about 21M DPR 100-word passages; MedRAG used 29.9M snippets) | CC BY-SA 4.0 | **Yes**, with attribution and share-alike on adaptations. This is the best first corpus |
| PMC Open Access "Commercial Use" collection | CC0 / CC BY / CC BY-SA / CC BY-ND ([PMC](https://ncbiinsights.ncbi.nlm.nih.gov/2019/02/08/changes-pmc-bulk-downloadable-open-access-dataset-files-march-2019/)) | **Yes, but only that collection.** The NC collection is out |
| PubMed abstracts | NLM does not own them. Publishers or authors may ([PubMed help](https://pubmed.ncbi.nlm.nih.gov/help/)) | **Unclear**. Avoid |
| arXiv | Per-paper licences. The default arXiv licence gives no reuse rights | Only the CC BY / CC0 subset. It also helps MMLU the least |
| OpenStax textbooks | Help page says **CC BY-NC-SA** ([OpenStax](https://help.openstax.org/s/article/Licensing-information-of-OpenStax-textbooks)). Some older editions say CC BY 4.0 | **Check each title**. Many are NC, so out |
| Medical textbooks (MedRAG's 18 USMLE books) | Copyrighted | **No** |
| Common Pile v0.1 (8 TB, 30 sources, openly licensed or public domain, OKF open definition) ([EleutherAI](https://blog.eleuther.ai/common-pile/)) | Open licences | **Yes**. This is the best commercially safe pool for books, education and papers. Check each subset's card |
| MassiveDS (140B subset is 2.99 TB) | Card says MIT ([HF](https://huggingface.co/datasets/rulins/MassiveDS-140B)), but its parts keep their original licences | **Not cleared**. Use only as published evidence |

## 5. Latency and practical local setup

Measured numbers from sources:
- **BEIR, 1M docs** ([BEIR](https://ar5iv.labs.arxiv.org/html/2104.08663)):
  - BM25: 0.4 GB index, 20 ms CPU.
  - TAS-B (66M dense): 3 GB, 14 ms GPU / 125 ms CPU.
  - DPR: 19 ms GPU / 230 ms CPU.
  - BM25 + cross-encoder rerank: 450 ms GPU / 6,100 ms CPU. **Rerankers are too slow** and give only marginal gains (RAG in the Wild).
- **100M-chunk datastore** ([arXiv 2412.11854](https://arxiv.org/html/2412.11854v1)), batched:
  - HNSW-SQ: 166 GB, recall 0.87, 0.31-0.81 s.
  - IVF-PQ: 23 GB, recall 0.61.
  - Retrieval was about 35% of time-to-first-token. RAG roughly doubled TTFT (495 -> 965 ms).
  - **Keep the datastore at tens of millions of passages, not billions.**
- **Embedding quantization** ([HF blog](https://huggingface.co/blog/embedding-quantization)):
  - 41M Wikipedia texts at 1024 dimensions: binary index 5.2 GB RAM plus 52 GB disk (binary plus int8 rescoring), versus 200 GB for float32.
  - Binary keeps about 96% of retrieval quality with rescoring.
  - CPU search is about 25x faster with binary and about 3.7x faster with int8.
- **Embedders that fit the rules:**
  - **Qwen3-Embedding-0.6B**: Apache-2.0, MTEB-en v2 mean 70.70, retrieval 61.83, MRL down to 32 dimensions ([HF](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)).
  - **bge-small / e5-small class (~33M)** for lowest cost.
  - ReasonIR-8B is **cc-by-nc-4.0** ([HF](https://huggingface.co/reasonir/ReasonIR-8B)) and 8B, so it is excluded.

My estimates (back-of-envelope; measure before trusting):
- **Index size for about 30M Wikipedia passages at 256 dimensions:** fp16 15.4 GB, int8 7.7 GB, binary 0.96 GB. Binary in RAM with int8 rescoring on disk fits a laptop or a CPU box.
- **Embedding build cost** (about 4B tokens):
  - 33M embedder: about 2.6e17 FLOPs, roughly 3-4 L4-hours (about $3). This fits the free L4 credit.
  - 0.6B embedder: about 4.8e18 FLOPs, roughly 25-30 L4-hours. Over budget unless we embed only article lead sections (about 1/3 the tokens; untested idea).
  - **BM25 build: $0** on a CPU. Pyserini has a prebuilt Wikipedia-DPR index (size not verified).
- **Added latency per decision**, query embedding plus search, extra prompt tokens dominating:
  - Query embedding: about 2-10 ms on GPU.
  - ANN or BM25 search: about 5-30 ms on CPU at roughly 20-30M passages. BEIR's 20 ms was at 1M docs, so measure at our size.
  - Extra prefill: k=3 x ~100 tokens = 300 tokens, about 2.4e12 FLOPs, **about 40-50 ms on an L4**. 1,000 tokens is about 140-170 ms on an L4 and about 15 ms on an H100. This assumes about 2N FLOPs per token and roughly 40-50% of the L4's 121 TFLOPS dense bf16.
  - **Total for the retrieval route: about 50-200 ms on an L4.** C1 is 20-50 ms today, so the route must be optional.

## 6. Recommended plan (only if the owner wants to try; about $0-3)

1. **Build a commercially licensed datastore, decontaminated:**
   - Use English Wikipedia (CC BY-SA), chunked into 100-word passages. Optionally add the PMC OA Commercial collection and Common Pile education/books subsets.
   - Decontaminate the MassiveDS way: drop passages with 13-gram Jaccard ≥0.8 against DI test items, OHS-3 and ejs-5.
   - Run decontamination as an isolated script that outputs counts only, so it never "chooses" data by score. **This needs owner OK**, because it touches DI item text.
2. **Retriever v0 is BM25 on CPU, at $0.** Move to bge/e5-small-class or Qwen3-Embedding-0.6B with binary/int8 only if BM25 shows a dev gain. MedRAG found BM25 strong for exam questions.
3. **Train C1 to read passages:**
   - Add RAFT-style rows: our own training MCQs (Claude-authored, programmatic labels) with 0-3 retrieved passages, some of them distractors, so the one-pass head learns to use or ignore context.
   - RAFT itself used CoT. Its one-pass transfer is **untested**.
   - No bigger teacher and no Jev outputs, so this fits the rules.
4. **Gate the route.** Retrieve only when the router says "knowledge MCQ" and C1's top-option probability is below a threshold.
   - Adaptive retrieval improved PopQA accuracy by 5.3 points and halved retrieval cost ([Mallen et al.](https://arxiv.org/html/2212.10511)).
   - It also keeps the median latency at today's 20-50 ms.
5. **Validate on dev sets that do not overlap DI:**
   - MMLU **validation** (about 1.5K items) and dev splits. DI uses MMLU test (14,042), so these are disjoint by ID, but still run the 13-gram dedupe.
   - ARC-Challenge, SciQ, SuperGPQA.
   - GPQA main/extended **minus Diamond** (348 items). Ask the owner first, since it is the same pool.
   - **Avoid MMLU-Pro**, which is derived partly from MMLU test.
6. **Ship gate:**
   - At least +1.5 on MMLU-val, paired McNemar p<0.05.
   - No regression of more than 0.5 on non-knowledge dev.
   - p95 latency within budget.
   - Otherwise drop the route.

## 7. Unknowns

- C1's real prompt length and serving GPU, which determine the actual prefill cost of passages.
- Whether a one-pass (no-CoT) head can use passages as well as the CoT readers in these papers. No paper found tests that.
- BM25 latency at 21-30M passages on our CPU, and the size of Pyserini's prebuilt index.
- How much of DI's MMLU or GPQA text exists verbatim on Wikipedia. That is why decontamination is mandatory: without it, a gain could be leakage.
- Whether Jev uses retrieval at all (its 70-500 ms range would allow it). Unknown.

## Sources

- MassiveDS: https://arxiv.org/html/2407.12854v1 , https://github.com/RulinShao/retrieval-scaling , https://huggingface.co/datasets/rulins/MassiveDS-140B
- RAG in the Wild (Qwen3-4B/8B + MassiveDS): https://arxiv.org/html/2507.20059v1
- ReasonIR: https://ar5iv.labs.arxiv.org/html/2504.20595 , https://huggingface.co/reasonir/ReasonIR-8B
- GPQA: https://ar5iv.labs.arxiv.org/html/2311.12022
- MedRAG/MIRAGE: https://arxiv.org/html/2402.13178v1
- Fine-tuning vs retrieval: https://aclanthology.org/2024.emnlp-main.15.pdf
- REPLUG: https://arxiv.org/abs/2301.12652
- Adaptive retrieval: https://arxiv.org/html/2212.10511
- RAFT: https://arxiv.org/pdf/2403.10131
- BEIR latency: https://ar5iv.labs.arxiv.org/html/2104.08663
- RAG systems trade-offs: https://arxiv.org/html/2412.11854v1
- Embedding quantization: https://huggingface.co/blog/embedding-quantization
- Qwen3-Embedding-0.6B: https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
- Qwen3.5-4B card: https://huggingface.co/Qwen/Qwen3.5-4B
- Decision Index: https://github.com/flaviusburca/decision-index
- Common Pile: https://blog.eleuther.ai/common-pile/
- PMC OA licensing: https://ncbiinsights.ncbi.nlm.nih.gov/2019/02/08/changes-pmc-bulk-downloadable-open-access-dataset-files-march-2019/ ; PubMed copyright: https://pubmed.ncbi.nlm.nih.gov/help/
- OpenStax licensing: https://help.openstax.org/s/article/Licensing-information-of-OpenStax-textbooks
