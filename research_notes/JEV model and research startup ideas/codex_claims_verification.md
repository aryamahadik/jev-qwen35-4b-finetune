# Codex claims verification (checked 2026-09-25)

Verdicts: VERIFIED / PARTLY / NOT FOUND / FALSE.

## 1. GLiClass Edge v3: VERIFIED
- Model card: https://huggingface.co/knowledgator/gliclass-edge-v3.0
  - 32.7M params, 131 MB, 97.29 examples/s at batch 1 on an A6000.
  - "Average Banchmark" (sic) 0.4873. Licence apache-2.0.
- Config: https://huggingface.co/knowledgator/gliclass-edge-v3.0/raw/main/config.json
  - Encoder `jhu-clsp/ettin-encoder-32m` (ModernBert type), hidden 384, 10 layers, 6 heads, uni-encoder, MLP scorer.
- Scoring: https://github.com/Knowledgator/GLiClass/blob/main/gliclass/pipeline.py
  - The pipeline's default is `classification_type="multi-label"`, which scores each label with its own `torch.sigmoid`. Labels are kept only if their score is at least `threshold=0.5`.
  - `"single-label"` uses `torch.softmax` instead.
  - So "none of the above" already happens in multi-label mode when every label scores below the threshold. It is only a threshold, though: there is no calibrated abstain option.

## 2. Jev 1.13 jaggedness doc: VERIFIED
- Sources: https://docs.typesafe.ai/model-jaggedness/jev-1.13 (.md version also available). "Last reviewed 2026-09-17."
- There are **9** failure modes:
  1. Literal reading
  2. Math and Numbers (subsections: Counting, Numeric representations, Math using score)
  3. Date and time comparison
  4. Indirection
  5. Large state full of irrelevant detail
  6. Adversarial content
  7. Contradictory instructions and criteria
  8. Common-sense structural invariants
  9. Generation
- Quotes:
  - "there are many structural invariants one might imagine to hold that simply aren't guaranteed by the model."
  - Negation example on "I was charged twice for the same order...": `refund` 0.72, `not_refund` 0.47, Sum 1.19.
  - "There are many reasons that `P(noul)` and `1 - P(not noul)` may not be directly comparable."
  - Noul vs yes/no Choice on "I'm not happy with the fit...": Noul 0.22, Choice yes 0.01, no 0.99, confidence 0.97.
  - The recommended fix is "enforce identities in code".

## 3. Jev vs GLiNER2.5 pilot: VERIFIED
- Source: https://github.com/AbdelStark/jev-benchmarks (report `results/reports/btzsc-pilot-v1.md`, with a `.json` version)
- Setup: Jev vs `fastino/gliner2.5-multi-v1`. BTZSC conditions with 100 class-balanced rows each of AG News, DAIR Emotion and Banking77, so 300 in total.
- Accuracy (Jev vs GLiNER2.5):
  - AG News 0.910 vs 0.700
  - Banking77 0.870 vs 0.610
  - Emotion 0.480 vs 0.440
- Emotion calibration: Brier 0.846 vs 0.668, NLL 5.588 vs 1.381. Jev gave zero probability to the true label in 16% of examples.

## 4. jev-benchmarks and novelty: PARTLY (the individual tests are NOT novel)
- **AbdelStark/jev-benchmarks** (4 commits, 18 stars, seed date 20260917)
  - Measures accuracy, macro-F1, Brier, NLL, top-label ECE, coverage at a fixed error budget, latency, tokens and failures.
  - Has no negation, paraphrase, distractor, injection or none-of-the-above tests.
  - Open issue #3 (kiwi0719, 2026-09-21) proposes option-shuffle and paraphrase perturbations: https://github.com/AbdelStark/jev-benchmarks/issues/3
- Robustness work that already exists (index: https://github.com/Yifan-Lan/awesome-jev-robustness, snapshot 2026-09-24):
  - **Negation / complement and Noul vs Choice:** https://github.com/jujumilk3/jev-calibration-audit
    - About 7,000 calls. P(x)+P(not x) has mean 1.02 and range 0.71–1.42.
    - A Noul and a 2-option Choice differ by 0.125 on average.
    - Option order: 0 argmax flips in 400.
    - Removing the abstain option: KoBBQ accuracy 0.950 → 0.000 and ECE 0.023 → 0.793.
  - **Paraphrase:** https://github.com/fstandhartinger/jevbench reports a paraphrase same-answer rate and both-correct rate. https://github.com/yodablocks/jev-orderby-bench has a "negation symmetry" gate.
  - **Prompt injection:**
    - https://github.com/zkousama/jagged: 96.5% at baseline, 26.5% with a one-line injected instruction.
    - https://github.com/Gaurav-Gosain/jev-sec-bench
  - **No-tool abstention:** https://github.com/baibizhe/jev-decision-benchmarks reports hallucinated tool calls on 76% of When2Call no-tool cases.
  - **Distractor robustness:** no dedicated public test found (it appears only in TypeSafe's docs).
- Open models claiming consistency:
  - https://github.com/kyegomez/open-jev has a consistency term in `RLCDLoss` and paraphrase `augmented_states`, but the weights are random and no checkpoint is released.
  - https://github.com/Heman10x-NGU/openJev-verdict-2.0: 149.6M ModernBERT-base, permutation-KL (order) consistency, 4.76% flip rate.
  - **None found claims negation/complement logical consistency.** The repos' dates were not individually checked against the 10-day window.
- What is still open: one benchmark covering all of these axes, plus an encoder trained with a complement-consistency loss.

## 5. Prior art: VERIFIED (known citations; the IDs for 1–4 were not re-fetched in this session)
1. **Semantic Loss** (Xu et al., ICML 2018): https://arxiv.org/abs/1711.11157
2. **BECEL** (Jang, Kwon, Lukasiewicz, COLING 2022): https://aclanthology.org/2022.coling-1.324/
3. **ConCoRD** (Mitchell et al., EMNLP 2022): https://arxiv.org/abs/2211.11875
4. **Logic-guided augmentation for consistent QA** (Asai & Hajishirzi, ACL 2020): https://aclanthology.org/2020.acl-main.499/
- Closest newer items:
  - **LoCo-LMs** (Calanzone, Teso, Vergari, ICLR 2025): semantic-loss fine-tuning for logical consistency, including negation. https://arxiv.org/abs/2409.13724
  - **Aligning with Logic** (logical preference consistency): https://arxiv.org/abs/2410.02205
  - **Controlled Reformulation Testing for Logical Consistency** (2026): https://arxiv.org/abs/2607.14528
- Work specific to small encoders or zero-shot classifiers: NOT FOUND.

## 6. Segment embeddings: VERIFIED / NOT FOUND
- **ISE** (Tong Wu et al., ICLR 2025): https://arxiv.org/abs/2410.09102. Tested on Llama-2-13B, Llama-3-8B and Llama-3.1-8B.
- **StruQ** (Chen, Piet, Sitawarin, Wagner; arXiv Feb 2024, USENIX Security 2025): https://arxiv.org/abs/2402.06363
- Trust-segment embeddings applied to small encoder classifiers: NOT FOUND.

## 7. Tool-necessity probes: VERIFIED / NOT FOUND
- **AUROC 0.89–0.96 across 6 models:** "LLM Agents Already Know When to Call Tools – Even Without Reasoning" (Sun, Liu, Yan, Wang, Weng). https://arxiv.org/abs/2605.09252, code at https://github.com/Trustworthy-ML-Lab/when2tool
  - Probe&Prefill cuts tool calls by 48% for a 1.7% accuracy loss, with <1 ms overhead.
- **"14–22x lower latency" open project:** NOT FOUND.
  - The closest is `toolgate-probe` v0.1.0 (2026-07-04; https://github.com/tanishqtayade/toolgate), which reports only "~800ms" average latency.
