# OpenDecide: handoff (26 Sep 2026)

Where everything is, what the best models are, what we measured, and how to rerun it.

## Where things live

| What | Where |
|---|---|
| All code, data, predictions, results | `opendecide-data/lean/` (this git repo) |
| JevBench benchmark (public, not ours) | `bench/jevbench/`, a clone of github.com/fstandhartinger/jevbench at commit `1bcc55eb6c8cffde2306b3db03ede39b61c6152a`. Not in git; re-clone and check out that commit. |
| Our JevBench half-splits and runs | `bench/splits/` (A = 118 items used for choices, B = 113 items for confirmation only), `bench/runs/`, scorer `bench/score_jevbench.py` |
| Trained models, local backup | `backups/modal_models/` (not in git; about 2.3 GB) |
| Trained models, cloud copy | Modal volume `opendecide`, folder `/models` (plus `/hf`, a re-downloadable model cache) |
| API keys | `opendecide-data/.env` (git-ignored) and the Modal secret `opendecide-keys` (HF_TOKEN, OPENROUTER_API_KEY). **Rotate the OpenRouter key:** it was pasted in chat. |
| Reports | `reports/OpenDecide_v05_vs_Jev.md` (v0.5; does not yet include the Gemma/JevBench work below) |
| Python env | `opendecide-data/.venv` (torch 2.14, transformers 4.57.6, modal 1.5.5). Not in git. |

## Best models

| Name | What it is | Use it with |
|---|---|---|
| `g12_v06_A3` | Gemma-4-12B-it + LoRA r16, v0.6 recipe (A3 losses, KL anchor beta=1, trained-in task cards), 0.53 epoch on `train_v06s` | style `od`, temperatures noul 0.8 / choice 0.95 (fitted on dev + devp_card), task cards + batch calibration for recurring label sets |
| `q4b_v05_A3` | Qwen3-4B-Instruct-2507 + LoRA r16, v0.5 recipe | style `od`, T 1.1 / 1.15 |
| `glml_v03_A3` | GLiClass-modern-large 399M, full fine-tune (fast tier, 26 ms/question on L4) | `gliclass_io.py` |
| `q4b_v03_A0` | ablation: same as v0.3 without robustness data or consistency loss | — |

Frozen `google/gemma-4-12B-it` with the Cygnet prompt layout (`jevbench_od.py` fmt `cygnet`, T=3.4) is the strongest JevBench setup we measured (half A: 104/118).

## Key results (all measured)

**Our 1,915-row suite with task cards, vs a guard-matched Jev** (paired bootstrap; * = significant):

| | Jev (guard + cards) | g12_v06 |
|---|---|---|
| Zero-shot choice | 91.6 | 91.6 |
| Zero-shot yes/no | 85.3 | **92.6*** |
| In-domain choice / negation | 88.0 / 86.5 | **93.0* / 92.0*** |
| Brier / ECE | 0.106 / 0.047 | **0.075* / 0.019** |
| Complement violation | 0.085 | **0.058*** |
| Distractor | 72.5 | **90.0*** |
| Injection success | 10.0% | 4.2% (n.s.) |
| Coverage at 1% / 3% error | 2.1% / 39.6% | **18.3% / 61.7%** |

**JevBench v1.4.2 public items (231):**

| | Correct | Hard tier (111) |
|---|---|---|
| Jev | 200 | 82 |
| Frozen Qwen3-4B | 166 | 51 |
| g12_v06 (A + B) | about 191 | about 72% on A, 57% on B |
| Frozen Gemma-4-12B, Cygnet layout | half A: 104/118 | 78% on A |

Other measurements:
- **Long state and multi-record slices:** ties with Jev.
- **Many options (78 / 500 / 2,000):** tie; Jev's API rejects more than 255.
- **Latency:**
  - End to end on the same 515 requests: Jev 203 ms vs our Modal web endpoint 410 ms (most of ours is Modal routing overhead).
  - GPU compute: 4B 27–60 ms per question; Gemma-12B 86 ms p50 on H100.
- **Lessons:**
  - The KL anchor stops fine-tuning from destroying zero-shot skill.
  - Prompt layout decides the JevBench hard tier.
  - HF text generation decodes at about 68 ms/token (too slow for think-mode).

## Rules we kept

- Never train on Jev outputs.
- Choose only on dev / devp (the fresh panel D) / JevBench half A. The eval zero-shot rows are "burned" because a research agent probed them.
- Half B has been used twice for confirmation. Treat it as seen.

## Rerun (from `opendecide-data/lean`, Modal CLI in `../.venv/bin/modal`)

```bash
M=../.venv/bin/modal
$M run modal_od.py::train --name NAME --base google/gemma-4-12B-it --gpu H100 --epochs 0.53 --lr 5e-5 --beta 1.0 \
   --train-file train_v06s.jsonl --rel-file train_v06s_relations.jsonl --splits dev,devp_card
$M run modal_od.py::evaluate --name NAME --base google/gemma-4-12B-it --splits eval,eval_card,eval_multi,eval_long
$M run modal_od.py::jevbench --name RUN --base google/gemma-4-12B-it --adapter /vol/models/NAME --tiers A --gpu H100
CAL_FIT=dev,devp_card ../.venv/bin/python calibrate.py NAME
../.venv/bin/python score.py --split eval_card --models jev_guard NAME_cal_bc --ref jev_guard
cd ../../bench && ../opendecide-data/.venv/bin/python score_jevbench.py jev_p1 RUN --kinds api,gpu --prices 0.042,0.05 --items A
```

To push a backed-up model back to Modal: `modal volume put opendecide backups/modal_models/NAME /models/NAME`.

## Budget (September 2026)

- **Modal:** about $22.4 of the $30 monthly credit used.
- **OpenRouter:** about $0.5 of the $5 limit used.

## Next plan: "PRISM-lite cascade"

1. **Fast model:** Qwen3.5-2B answers first.
2. **Strong model:** Qwen3.5-9B or Gemma-12B takes only the unsure questions.
3. **PRISM pieces:**
   - stream labels on every token;
   - write-blocked recurrent memory for untrusted text (the novel part);
   - a calculator/date pre-pass;
   - label search for huge choice lists;
   - the KL anchor;
   - calibrated abstaining.

**First $7 of tests:**
1. Qwen3.5-2B vs 4B vs 9B, frozen.
2. The math/date step.
3. A write-block prototype on Qwen3.5-0.8B.

**After top-up:** fine-tunes, security training, vLLM serving, and the full benchmark with ablations.
