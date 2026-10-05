# Fast think mode without any training (short version, 4 Oct 2026)

One model: Qwen3.5-4B. Fast path = C1 (with LoRA). Think path = the same base weights with the LoRA off and thinking
on. No training of any kind. Everything below comes from FAST_THINK_PLAN.md, R_serving.md and R_tokens.md.

## 1. Flow
1. **Fast pass:** C1 reads the question once, ~20-50 ms on an H100. If C1's top probability is >= 0.8, answer now.
   About 70-95% of questions stop here.
2. **Router:** the rest go to think. Optionally, only knowledge, maths or code question types go to think.
3. **Think, short and capped:**
   - Maths-like questions: short step-by-step capped at ~300 tokens, 4 tries run in parallel, then a majority vote.
   - Other questions: thinking capped at 768-1,024 tokens, with early exit (DEER, see section 3).
   - Then force `</think>` and read the answer letter.
4. **Fallback:** if the answer cannot be parsed, keep C1's answer.

## 2. Serving stack (all free software; only GPU time costs money)
- **Engine:** SGLang or vLLM (pinned version) with CUDA graphs. Prefix caching OFF, because of a known spec-decode bug.
- **Speculative decoding:** the DFlash drafter `z-lab/Qwen3.5-4B-DFlash` (Apache-2.0) gives 3.4-4.6x on maths and code
  with the same answers. Qwen's built-in multi-token prediction (MTP) gives only 2.0-2.1x, so it is the fallback.
- **Weights:** FP8 is ~1.3x faster for <= 1 pt lost. Do not use INT4: it loses 1.3-2.1 pts and more on hard maths.
- **Hardware:** H100 at ~250 tok/s single stream before speculative decoding; B200 at ~1.4x that. Fast-chip providers
  cannot host this model yet.
- **Parallel short tries:** decode is memory-bound at batch 1, so 4 parallel tries cost little extra time.

## 3. Cutting thinking tokens with no training
- **Hard cap:** 300 tokens for maths-like questions, 768-1,024 for others. Qwen3-4B writes ~2.2K tokens on GSM8K and
  ~9.3K on GPQA when uncapped.
- **DEER early exit:** at each pause word ("Wait"), probe the answer and stop once its confidence is high. On Qwen3-4B
  this cut GPQA from 9,294 to 3,275 tokens (46.5 -> 47.5) and GSM8K from 2,175 to 1,250 tokens (94.1 -> 94.5).
- **Short step-by-step answer instead of "thinking" on easy maths:** Qwen3-4B got 82.2% on GSM8K at ~85 tokens, vs
  38.4% with no reasoning.

## 4. Expected latency (estimates)
| Question | L4 today (basic) | H100 + DFlash + FP8 + caps |
|---|---|---|
| Easy (fast path) | ~114 ms | ~20-50 ms |
| Maths (300 tokens) | ~70 s (single) / ~5 s amortised | ~0.3-0.4 s |
| Other reasoning (768-1,024 tokens, early exit) | ~70-95 s single | ~0.7-1.1 s |
| Average with ~5-10% routed | — | ~0.1-0.15 s (Jev ~0.2 s) |

## 5. Measured so far (A17-B0, no tuning, L4)
- SQuAD 2.0 with thinking: 90.3, vs 81.3 without thinking and Jev 82.9.
- PAWS: 80.0. 84% of items hit the 768-token cap; needs a longer budget or a routing rule.
- Results for the full system (C1 + router + think) are in bench/think_check/report_b0b.json, filled when the run
  ends.
