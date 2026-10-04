# RESEARCH_EXTRA_6: Qwen3.5 hybrid facts and 2025-2026 small-model recipes

Date: 3 Oct 2026. CPU only. 16 web searches and fetches, plus read-only checks of local code (`train_decoder.py`,
`decoder_io.py`, `modal_od.py`). No paid calls. No OHS-3, quarantine or Jev-output paths opened.
Scope: (a) training facts for Qwen3.5-4B's hybrid layout (24 Gated DeltaNet + 8 full-attention layers), (b) transferable
details from Tulu 3, OLMo 2, Olmo 3, SmolLM3 and the Qwen3 report. This file does not edit `C_DATA_SPEC.md` or
`C_TRAIN_RECIPE.md`. It proposes changes in section 9 for the spec owner to accept or reject.

---

## 0. Short answer (7 points)

1. **Exact recall in Qwen3.5-4B lives in the 8 full-attention layers.** With only the attention KV cache kept, Qwen3.5-4B
   still gets 0.89 (key-value lookup) and 0.98 (list indexing). With only the recurrent (DeltaNet) state it gets
   **0.00** on both (arXiv 2609.04434, Table 1). Output language and persona live in the recurrent state (0.70 vs 0.01).
2. **Our LoRA spends only 9.7% of its parameters on those 8 recall layers.** Computed from the public shapes: full
   attention 3,145,728 params, MLP 18,087,936, DeltaNet 11,231,232; total 32,464,896 (matches `expect_trainable`).
3. **One study says "adapt attention only" in Qwen3.5 hybrids, but the evidence is weak for us.** Qwen3.5-0.8B,
   2,000 training rows, one seed, 128-256 eval items: softmax-only LoRA +10.2 pp on GSM8K vs all-layers +7.8 pp;
   DeltaNet-only -14.8 pp (arXiv 2604.22127). C starts from C1's all-layer adapter, so **keep all targets** for C.
   Keep the finding as a reason to never add DeltaNet-only capacity.
4. **Merging recipes are cheap and documented.** SmolLM3: 0.9 x final soup + 0.1 x mid-training checkpoint recovered
   RULER up to 128K. OLMo 2: three-seed soup beat the best single run by +0.3 to +2.0 (OLMES MC). Tulu 3: seed soup at
   SFT gave **no** gain (60.2 vs 60.1). Olmo 3: final SFT = merge of two learning rates; long-context base = average of
   the last 3 checkpoints. For C vs C1: **merge the LoRA products (delta W), never the A and B factors.**
5. **Chat template identity is already enforced in our code.** Training and reading both use
   `enable_thinking=False` through `decoder_io.prompt` (line 169) and record `chat_template_sha` (line 290).
   Qwen3.5 defaults to thinking mode; any external server must pass `chat_template_kwargs={"enable_thinking": false}`.
6. **Loss aggregation (Tulu 3's sum-vs-mean issue) is already handled.** `aux_norm: "batch"` normalizes every loss
   term by whole-batch counts, so micro-batching does not change row weights (`train_decoder.py` 881-938).
7. **No text tech report for the small Qwen3.5 models was found.** Only the model card (citation "Qwen3.5: Towards
   Native Multimodal Agents", Feb 2026, no arXiv id) and the Qwen3.5-Omni report (arXiv 2604.15804). How the small
   models were post-trained is **unknown**.

---

## 1. Qwen3.5-4B facts (verified)

Source: model card https://huggingface.co/Qwen/Qwen3.5-4B (Apache 2.0).

| Item | Value |
|---|---|
| Layers | 32 = 8 x (3 x (Gated DeltaNet -> FFN) -> 1 x (Gated Attention -> FFN)) |
| Hidden / FFN | 2,560 / 9,216 |
| Gated DeltaNet | 32 V heads, 16 QK heads, head dim 128 |
| Gated Attention | 16 Q heads, 4 KV heads, head dim 256, RoPE dim 64 |
| Context | 262,144 native, extensible to 1,010,000 |
| Default mode | thinking on (`<think>\n...</think>\n\n`); off with `enable_thinking: False` |
| Card sampling, non-thinking | temperature 0.7, top_p 0.8, top_k 20, presence_penalty 1.5 (irrelevant to our argmax letter read) |

**Our LoRA split at r16 (computed, matches `expect_trainable` exactly):**

| Block | Layers | LoRA params | Share |
|---|---|---|---|
| Full attention (q 2560->8192 incl. gate, k/v 2560->1024, o 4096->2560) | 8 | 3,145,728 | 9.7% |
| MLP (gate, up, down) | 32 | 18,087,936 | 55.7% |
| Gated DeltaNet (in_proj_qkv/z/a/b, out_proj) | 24 | 11,231,232 | 34.6% |
| Total | | 32,464,896 | 100% |

The 3:1 DeltaNet:attention ratio is also used in the larger Qwen line (Qwen3.8-Next design paper, arXiv 2608.30320:
"one full-attention layer in every four"). That paper gives no fine-tuning or recall-vs-ratio numbers.

---

## 2. Where recall lives in the hybrid

**arXiv 2609.04434** ("What Attention Recalls and Recurrence Controls in Hybrid Language Models", 3 Sep 2026). It keeps
only the KV cache or only the recurrent state after reading a context (3 seeds, 95% bootstrap CIs).

| Model | KV retrieve: kv-only / rec-only | List index: kv-only / rec-only | Language following: rec-only / kv-only |
|---|---|---|---|
| Qwen3.5-4B | 0.89 / 0.00 | 0.98 / 0.00 | 0.70 / 0.01 |
| Falcon-H1-3B | 0.64 / 0.00 | 0.83 / 0.00 | 0.79 / 0.01 |

- Persona: Qwen3.5-4B rec-only 0.49 vs kv-only 0.14.
- Limits: short synthetic contexts (15-30 dict entries, 4-10 list items). No fine-tuning, no LoRA and no
  context-length sweep.

**Pure linear models fail exact recall as length grows.** Gated DeltaNet 1.3B alone (arXiv 2412.06464, Table 2):
- S-NIAH-2 (number in haystack): 100.0 at 1K, 92.2 at 4K, **29.6 at 8K**.
- S-NIAH-3 (UUID): 86.6 at 1K, **27.6 at 4K**.

Hybrids that add attention beat pure Transformers on real recall tasks (same paper, Table 4). Based (arXiv 2402.18668)
shows the recall-vs-state-size trade-off: +6.22 points over sub-quadratic baselines on recall-heavy tasks.

**What this means for C.**
- In C's long rows (2K-7.9K tokens), finding the decisive clause is done by the 8 attention layers. The DeltaNet layers
  mostly carry "how to answer" (format, register, style).
- Our current 8K window is short for Qwen3.5's attention. Recall at 2-8K should already be strong in the base model.
  The likely failure on long rows is **choosing between near-miss sections**, not losing the clause.
  - F13 already targets this (superseded versions, other regions, look-alike IDs).
- **LongBench v2 (41 vs Jev 52.8) is mostly beyond our training lengths.** Its contexts run from 8K to 2M words, and C
  trains on no row above 7.9K tokens. Do not expect C's long rows to close that gap. Estimate: +0 to +2 pp, low
  confidence. A larger gain would need longer rows than `micro_tokens` 8192 allows.

---

## 3. Where LoRA should go in a Qwen3.5 hybrid

**arXiv 2604.22127** ("Where Should LoRA Go?", Apr 2026). Setup: Qwen3.5-0.8B-Base and Falcon-H1-0.5B; r16, alpha 32,
dropout 0.05, LR 2e-4 cosine, 3 epochs, batch 16, max length 1,024, 2,000 rows per domain, single seed (3407).

| Qwen3.5-0.8B, trained on GSM8K | LoRA params | GSM8K change vs base |
|---|---|---|
| softmax (attention) only | 1.08M | **+10.2 pp** |
| MLP only | 5.31M | +8.6 |
| all layers | 10.82M | +7.8 |
| DeltaNet + MLP | 9.74M | -9.4 |
| DeltaNet only | 4.43M | **-14.8** |
| attention + MLP | 6.39M | -14.8 (the authors' "destructive interference anomaly") |

- Forgetting: after UltraChat training, Qwen3.5-0.8B lost up to 16.0 pp on GSM8K (all layers -15.6).
  - After code training: softmax-only -11.3 pp vs all layers -21.9 pp.
  - The parallel hybrid (Falcon-H1) showed positive transfer instead.
- Authors' advice: default to attention-only, and do not adapt the recurrent backbone in sequential hybrids.

**How much to trust this for C: low.**
- Scale is 0.8B, not 4B.
- There is 1 seed.
- GSM8K has 128-256 eval items, so the SE is about 3-4 pp.
- Settings are generative math with LR 2e-4 x 3 epochs (aggressive), not a one-token letter readout.
- The attention+MLP collapse (-14.8, the same as DeltaNet-only) suggests instability or noise.

Against it: C1 (all targets, r16, about 30K steps) is tied with Jev on OHS-1/2. Competitors on Qwen3.5-4B also put r16
on attention, DeltaNet and MLP (RESEARCH_competitor-lessons.md lines 284, 309).

**Decision for C: keep `targets: QWEN35` (all 32,464,896 params) and C1's adapter as init.**
- Changing targets mid-lineage would throw away C1's DeltaNet adapters, or freeze them. Freezing them is the
  "attention + MLP" arm, the anomaly above.
- Forgetting is larger in sequential hybrids. That backs the recipe's replay and selective C1 anchor; it does not
  change them.
- Possible later probe (not for C, no budget now): a single 4B run that triples LR only on the 8 attention layers'
  LoRA (`lr_mult_attn` 3). Report-only. Expected effect unknown.

---

## 4. Chat template and the one-pass readout

- **Qwen3 report** (arXiv 2505.09388, section 4.3): non-thinking SFT samples "retain an empty thinking block in the
  assistant's response". Developers block thinking by "concatenating an empty think block in the chat template".
  The model follows the last `/think` or `/no_think` flag.
  - So the non-thinking prompt is a fixed string ending in an empty `<think>\n\n</think>\n\n` block.
  - A letter read made after a different suffix sees an off-distribution context.
- **Measured local effect:** using the chat-template prompt lifted a frozen model from 0.653 to 0.710
  (RESEARCH_competitor-lessons.md line 357).
- **Tulu 3** (arXiv 2411.15124, Table 13): five chat templates on one SFT mix spanned 51.6-53.0 average, a 1.4-point
  spread from the template alone.
- **Our code (checked):**
  - `decoder_io.prompt()` (line 169) applies `enable_thinking=False` whenever the template knows the flag.
  - `jevbench_od.py` (line 71) and `modal_od.py` (line 1244) do the same.
  - `chat_template_sha` is logged (`decoder_io.py` line 290). The recipe pins it (C_TRAIN_RECIPE.md line 260).
- **Gaps:**
  1. `decoder_io.prompt` silently falls back to "system folded into user" if `apply_chat_template` raises. This is
     safe today, because Qwen3.5 accepts a system role. Make the fallback **fail loudly** for Qwen3.5 so a template
     change cannot silently alter the prompt.
  2. The sha covers the template, not the rendered prefix. Add a one-line pre-flight assert: train, dev-gate and
     serving render byte-identical prompts for 3 fixed rows (sha256 of the rendered string). Cost: about $0 on CPU.
  3. External serving (vLLM or SGLang) must pass `chat_template_kwargs: {"enable_thinking": false}`. The card says the
     default is thinking on.

---

## 5. Merging and soups: what the recipes did, with numbers

| Recipe | What was merged | Result |
|---|---|---|
| SmolLM3 (https://huggingface.co/blog/smollm3) | linear 0.9 x APO model soup + 0.1 x mid-training checkpoint (MergeKit) | APO had hurt RULER; the merge "recover[ed] the base model's RULER score on contexts up to 128k" |
| OLMo 2 (arXiv 2501.00656, Table 14) | 3 mid-training runs, same mix, different data order | soup minus best single, OLMES MC: +1.4, +2.0, +0.5, +0.3, +1.9, +0.8 over 6 mixes; never worse |
| Tulu 3 (arXiv 2411.15124, Table 14) | SFT seeds | 8B: seeds 59.8-60.1, best soup 60.2. 70B: seeds 70.0-72.6, best soup 72.5. Kept the best single run |
| Olmo 3 (arXiv 2512.13961) | Think SFT: 2 checkpoints at different LRs; 32B long-context: last 3 checkpoints (steps 10,000 / 11,000 / 11,921) | used for the final models; no isolated gain number found |

**Lessons for C:**
1. **Soups help most at full-weight mid-training scale.** At SFT scale (Tulu 3) they were flat. Expected value of a
   2-seed C soup: about 0 pp, at 2x the cost. Not recommended.
2. **The SmolLM3 pattern applies to C vs C1 as "win back a lost skill":** C' = a x C + (1 - a) x C1, with a in
   {0.8, 0.9}.
   - Step B (A11) already showed that scaling C1 toward the **base** does not help (a = 0.9: +0.05 [-0.30, +0.40]).
     That result tested a different axis.
   - The C/C1 mix is worth one pre-registered look **only if** C passes on new domains but fails a C1-protected
     skill (D-gates).
3. **LoRA merge maths (important).** Averaging the A and B matrices separately is wrong:
   (aB1 + (1-a)B2)(aA1 + (1-a)A2) has cross terms B1A2 and B2A1. An exact, servable mix is a rank-32 concatenated
   adapter:
   - B = [a·B_C, (1-a)·B_C1], A = [A_C; A_C1].
   - Keep the scale alpha / r = 2: alpha 64 at r 32, or pre-multiply.
   - Or merge each delta into fp32 weights and check argmax agreement >= 99.9% (already in the recipe for bf16 merges).
4. **Snapshot averaging is free.** `snap_fracs` [0.25, 0.5, 0.75] already saves snapshots. A pre-registered
   "mean(delta W at 0.75, delta W final)" candidate costs no training. With cosine-to-0 the gain is likely small
   (estimate 0 to +0.5 pp, low confidence). It may only be read on the dev select split, never on sealed sets, which
   matches the recipe's snapshot rule.

---

## 6. Tulu 3 and OLMo 2 SFT facts that transfer

- **LR sensitivity.** Tulu 3 full fine-tune: 5e-6 (8B) and 2e-6 (70B), 2 epochs, batch 128, max length 4,096, warm-up
  3%, linear decay. "Training for longer did not yield further improvements".
  - OLMo 2 swept SFT LR {1, 2, 3}e-5 for 7B (picked 2e-5) and {1, 4, 5, 7.5, 8}e-6 for 13B (picked 5e-6). Each was
    picked with 1 seed, then confirmed with up to 4 seeds.
  - These are full-weight LRs. LoRA LRs are about 10x higher, so our 5e-5 to 7e-5 is in the normal LoRA range. No
    change.
- **Sum vs mean loss.** Tulu 3 found that averaging over tokens per micro-batch silently re-weights samples under
  gradient accumulation. It switched to a sum loss (each token weighted equally), with LR re-tuned. Sum loss at 5e-6
  was best.
  - **Ours:** the readout loss is per row (one letter position), and `aux_norm: "batch"` divides by whole-batch
    counts. Micro-batching therefore does not change weights. No action.
- **Seed noise.** Tulu 3 70B seeds ranged over 2.6 points (70.0-72.6); 8B over 0.3. This matches the recipe's
  seed-noise note (about +/- 1-2 pp) and supports deciding only on confirm sets.
- **Persona-seeded data.** Removing Tulu 3's persona sets cut the average by 1.5 (60.1 to 58.6), IFEval by 19.2
  (72.8 to 53.6), MATH by 1.4 and HumanEval+ by 2.4. It used about 250K personas.
  - **PersonaHub is CC-BY-NC-SA-4.0** (https://huggingface.co/datasets/proj-persona/PersonaHub). NonCommercial
    means we cannot use it.
  - Commercial-safe substitute: `gd_onet_occupation` (O*NET, CC BY 4.0, already KEEP in LICENCE_REGISTER.md line
    176). Use occupation titles as the "who is deciding" seed when Claude writes scenarios.
- **Decontamination.** The 8-gram rule (a test item counts as matched if more than 50% of its tokens share 8-grams with
  one train item; drop a source if it overlaps more than 2% of any eval) is already in the spec. No change.
- **Removing "irrelevant" data hurt.** OLMo 2 removed multilingual SFT data from a model not built for multilingual
  use, and the average fell about 0.5. Do not prune replay families because they look off-target.

---

## 7. Qwen3 report: small-model post-training (verified numbers)

- Small Qwen3 models (0.6B-14B, 30B-A3B) were made by **strong-to-weak distillation**: off-policy, then on-policy logit
  KD from Qwen3-32B or 235B-A22B. This took 1/10 of the GPU hours of the 4-stage pipeline.
- Table 21, Qwen3-8B from the same off-policy checkpoint:
  - RL: AIME'24 67.6, 17,920 GPU-h.
  - On-policy distillation: AIME'24 74.4, about 1/10 of the hours.
  - Distillation raised pass@64; RL did not.
- **Not usable as is.** We have no teacher bigger than 4B (owner rule). The only allowed version is C1 (4B) as a
  self-teacher, and the recipe already does that (selective C1 anchor via KD).
- Mode fusion cost (Table 22, Qwen3-32B, non-thinking):
  - The general-RL stage lifted IFEval by +4.8 and ToolUse by +13.3.
  - Knowledge (MMLU-Redux) fell -1.0.
  - Lesson: broad instruction stages cost a little knowledge. The C1 anchor is our guard.

---

## 8. Olmo 3: long-context data that transfers

Olmo 3 (arXiv 2512.13961, Dec 2025, v2 Apr 2026) context-extension ablations on RULER (Fig. 13):
- YaRN on full-attention layers only was best.
- Science PDFs (olmOCR) beat other sources.
- **Synthetic aggregation tasks injected into real long documents beat natural documents alone.**
- Document packing helped at longer lengths.
- The long data was **mixed with short high-quality data**, not trained alone.

Their generator:
- Split 32K-65K-token documents into 8K-32K sections.
- Find salient noun phrases (tf-idf, k = 8 snippets each).
- Ask a model for (a) CWE: exact-count questions over a section, (b) REX: rewrites in 12 styles (quiz, debate,
  true/false list, ...).

SmolLM3's opposite finding: "upsampling ... long context data such as code repositories, books, and long web pages ...
didn't further boost performance". Its long-context score was won back by merging, not by more data.

**For C (fits the spec's F13 rules):**
- **F13 aggregate sub-type** at about 20% of F13 rows. The answer needs facts from **2-3 sections**: count of active
  exceptions, the latest valid version among three, or a total over a table split across sections.
  - Program-labelled from the generator's ground truth (no LLM labels, no filler). This exercises multi-position
    attention recall, the part the hybrid can lose.
  - Keep the spec's coherent-document and depth-uniform rules.
- Keep F13 small and mixed with short rows. Both Olmo 3 (mixing) and ProLong / SmolLM3 (more long data alone did not
  help) point that way.

---

## 9. Proposed changes (for the spec owner; none applied)

| # | Change | Where | Cost | Expected effect | Confidence |
|---|---|---|---|---|---|
| 1 | Keep `targets: QWEN35` (all layers) and C1 init. Record why: the 2604.22127 evidence is 0.8B / 1 seed / LR 2e-4 | Recipe section 1 | $0 | avoids a risky change | medium |
| 2 | Pre-flight assert: sha256 of the **rendered** prompt is identical for train, dev-gate and serve on 3 fixed rows; make the `decoder_io.prompt` fallback raise for Qwen3.5 | Recipe pre-flight | $0 (CPU) | blocks silent template drift (template spread 1.4 pts in Tulu 3; 0.653 -> 0.710 locally) | high |
| 3 | If C/C1 interpolation is ever used: rank-32 concatenated adapter or fp32 delta-W merge, never factor averaging; a in {0.8, 0.9}, pre-registered, read only on the dev select split | Recipe (merge note) | about 1 dev read | 0 to +1 pp on a lost protected skill (SmolLM3 pattern) | low-medium |
| 4 | Optional pre-registered candidate: mean of delta-W at snap 0.75 and final | Recipe section 2 | about 1 dev read | 0 to +0.5 pp | low |
| 5 | F13 "aggregate" sub-type, about 20% of F13, 2-3 decisive sections, program-labelled | Spec F13 | $0 (generator work) | helps multi-section recall on long rows; LongBench v2 effect +0 to +2 pp | low |
| 6 | Persona seed = O*NET occupation title (CC BY 4.0) when Claude writes scenarios; **do not** use PersonaHub (NC) | Spec authoring section | $0 | diversity; Tulu 3: persona sets were worth +1.5 avg | medium |
| 7 | No seed soups for C | Recipe | saves 1x training | Tulu 3: soup = best seed at SFT | medium |

---

## 10. Unknowns

- Whether a text tech report for Qwen3.5 0.8B-9B exists. None was found (searched 3 Oct 2026). Their post-training
  recipe, distillation teachers and RL stages are unknown.
- How Qwen3.5-4B base or C1 score on RULER at 2-8K. Not measured locally. A CPU-free check is not possible.
- Whether the attention-only LoRA advantage holds at 4B with a letter readout. No study found.
- Any study of LoRA on hybrid models over **long** inputs. None found.
- Qwen3.5-4B's own LongBench v2 score on the model card was not extracted here.

---

## Sources

- Qwen3.5-4B model card: https://huggingface.co/Qwen/Qwen3.5-4B
- What Attention Recalls and Recurrence Controls in Hybrid LMs: https://arxiv.org/abs/2609.04434
- Where Should LoRA Go? (hybrid LoRA placement): https://arxiv.org/abs/2604.22127
- Gated DeltaNet: https://arxiv.org/abs/2412.06464
- Based (recall-throughput): https://arxiv.org/abs/2402.18668
- On the Design of Qwen3.8-Next Architecture: https://arxiv.org/abs/2608.30320
- Qwen3 Technical Report: https://arxiv.org/abs/2505.09388
- Qwen3.5-Omni Technical Report: https://arxiv.org/abs/2604.15804
- Tulu 3: https://arxiv.org/abs/2411.15124
- OLMo 2: https://arxiv.org/abs/2501.00656
- Olmo 3: https://arxiv.org/abs/2512.13961
- SmolLM3 blog: https://huggingface.co/blog/smollm3
- PersonaHub licence: https://huggingface.co/datasets/proj-persona/PersonaHub
- Local: `opendecide-data/lean/train_decoder.py` 881-938; `decoder_io.py` 166-174, 290; `jevbench_od.py` 71;
  `modal_od.py` 1244; `c_spec/LICENCE_REGISTER.md` 176; `c_spec/RESEARCH_competitor-lessons.md` 357.
