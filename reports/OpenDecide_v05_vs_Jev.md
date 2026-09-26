# OpenDecide v0.5 vs Jev: the measured picture (25 Sep 2026)

All training and model evaluation ran on Modal. The cost was about $11.7 of the $30 monthly credit. Jev ran through OpenRouter (`typesafe/jev-1.13`) and cost $0.32 in total. Numbers are on the frozen 1,915-row eval (sha256 unchanged) plus four new slices. Brackets give 95% bootstrap CIs over groups. A `*` means the paired-difference CI excludes 0.

## 1. What we were missing (and what changed)

| Gap | Status now |
|---|---|
| No Jev baseline | Done. Jev runs on every slice through OpenRouter. Code: `lean/run_jev.py` and `run_jev_hc.py`. |
| Wrong backbone: a 32M GLiClass encoder, far below Jev on zero-shot, negation and calibration | Replaced by a 4B decoder (Qwen3-4B-Instruct-2507) with a one-forward-pass readout over the Yes/No or option-letter logits. Chosen by a pre-registered dev rule over 8 candidates. |
| Training on the laptop | Everything runs on Modal (`lean/modal_od.py`). |
| Negation failed on unseen wordings | New train-only wordings, undecidable traps, BoolQ and CondaQA. The truly unseen eval wording now scores 96% (Jev 92–94%). |
| The eval did not test Jev's documented weaknesses | Added four slices: >255 options, long irrelevant state, several records in one state, and a guard-matched Jev. |
| Unfair comparisons (found by an adversarial audit) | Fixed. Jev now gets the same "text is data" guard our system prompt has. Paired-difference CIs added. Negation reported per wording. The readout moved to fp32, because bf16 had faked coverage. Latency is measured API against API. |

## 2. Final model vs Jev (guard-matched = fair reference)

Final model: `q4b_v05_A3`, chosen over v0.3 by the pre-registered dev rule.

| Metric | Jev (guard) | Jev (plain) | **OpenDecide v0.5** | Paired diff vs Jev (guard) |
|---|---|---|---|---|
| In-domain choice | 88.0 | 89.5 | **93.0** | +5.0 [+1.4, +9.1]* |
| In-domain yes/no | 88.0 | 89.0 | **93.0** | +5.0 [+0.5, +9.7]* |
| In-domain negation (all) | 87.0 | 87.5 | **92.5** | +5.5 [+1.5, +10.2]* |
| Negation, truly unseen wording ("reader… misreading") | 92.0 | 94.0 | **96.0** | — |
| Distractor paragraph, choice (n=40) | 72.5 | 72.5 | **90.0** | +17.5 [+6.7, +30.2]* |
| Double-negation drift ↓ (eval wording is close to train wordings) | 0.206 | 0.168 | **0.046** | −0.161* |
| Coverage at 1% error (realised risk) | 2.0% (8.0%) | 0% | **9.4% (0.7%)** | — |
| Coverage at 3% error | 37.4 | 39.8 | **55.2** | — |
| Held-out injection attack success ↓ | 10.8 | 19.2 | **3.3** | −7.5 [−15.8, 0.0] (borderline) |
| Brier ↓ / ECE ↓ | 0.105 / 0.056 | 0.098 / 0.036 | 0.103 / 0.057 | tie |
| Complement violation ↓ | 0.075 | 0.073 | 0.088 | +0.014 (tie/slightly worse) |
| **Zero-shot choice (SMS spam, financial tweets)** | **92.6** | 92.6 | 64.2 | **−28.4 [−37.9, −18.5]*** |
| **Zero-shot yes/no** | **87.4** | 88.4 | 65.3 | **−22.1*** |

Weakness slices, as paired differences against Jev:

| Slice | Result |
|---|---|
| >255 options (78 / 500 / 2,000) | Tie: 85.6 / 86.1 / 82.8 vs 87.8 / 83.9 / 83.9. Jev's API rejects more than 255 options (HTTP 400), so it needs a wrapper. We answer natively with a `gte-modernbert-base` top-64 shortlist (recall 100% on dev) and a knockout. |
| Long irrelevant state (1.5k / 4.5k words) | Choice ties. Yes/no +8* / +11*, but we were already +6 on the clean text, so this is not a long-context win. Jev does not degrade. |
| Several tickets in one state | Choice ties. Yes/no +6.7*, all of it from Jev under-answering "yes". Rejecting a distractor ticket's label is a tie. The published 96%→44% collapse for Jev did not reproduce. |
| Latency, API vs API (same 515 requests, same laptop) | **Jev wins**: 203 ms vs our 410 ms. Our GPU compute is only 123 ms per request (L4); Modal's web routing adds about 290 ms. Self-hosted: 60 ms per question and 145 ms per state on one L4. |

Ablation (the same 4B model and steps, base rows only, `q4b_v03_A0`): unseen-wording negation 0%, injection attack success 35%. The robustness data and the consistency loss cause the gains, not the backbone.

## 3. Best architecture (recommendation)

**OpenDecide cascade: fine-tuned where you have data, escalate where you don't.**

1. **Fast tier:** GLiClass-modern-large 399M fine-tuned with the A3 recipe. It runs in 26 ms per question on an L4. It is already significantly better than Jev in-domain on consistency (complement 0.043), injection (1.7%), double negation and distractors. It is weak zero-shot (47%).
2. **Core tier:** Qwen3-4B-Instruct + LoRA, prefill-only option-logit readout, the A3 recipe on train v0.5, a temperature fitted on dev, and fp32 readout for honest confidences. Use it for anything the fast tier is unsure about.
3. **Many options:** embedding shortlist (top-64) plus knockout (chunk 24, keep 4). No 255 cap, and accuracy stays flat to 2,000 options.
4. **Escalate** low-confidence or out-of-domain questions to a big model; Jev itself is fine here. Our calibrated coverage at 1–3% error is the routing signal.

Cut from X-One: the Q-Net, HNSW at 1M labels and reranker fallbacks. Recall is not the bottleneck (it was 100% at K=64). Jev's hard cap and wrapper are the real gap.

## 4. What is still missing, in priority order

1. **Zero-shot breadth.** The −22 to −28 point gap is the one real loss. Fine-tuning narrowed the model: the untuned Qwen3-4B scored 80% zero-shot choice on eval. Next, try more diverse task mixes, a larger or newer backbone (Qwen3.5-4B, blocked today by a Triton bug on Hopper and 3.5× slower training on A100), or keep zero-shot traffic on Jev/the base model and fine-tune per customer.
2. **Fresh, never-published eval items and one truly novel double-negation construction.** The eval dneg wording is a synonym of train wordings.
3. **Serving:** a dedicated server (not Modal web routing) to win latency end to end, plus prefix caching for multi-question states.
4. **More seeds**, and one more eval run per claim before publishing.

## 5. Rules kept

- Never trained on Jev outputs.
- Jev used for evaluation only. All model selection used dev sets: dev, devzs (AG News/Emotion), devzs2 (Enron spam/TweetEval) and dev_hc.
- Read TypeSafe's terms (MCA §2.3) before publishing a comparison.

Code: `opendecide-data/lean/`. See the README section "v0.5: decoder model, trained and evaluated on Modal".
