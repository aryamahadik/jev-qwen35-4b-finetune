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

## Start here next time: FREEZE.md

The $10 round (26 Sep 2026) ended with a frozen architecture and a costed plan for the $30 account in `FREEZE.md`.
The key result: on OHS-1, a new pre-registered held-out test of 17 public corpora we never touched, Jev leads, 81.7 vs 76.1.
The JevBench win is narrow and on a development set. Fix the data breadth first (FREEZE.md, Step 1).

## Current best: OpenDecide v0.10 (26 Sep 2026, account mahadikarya44)

`q35_4b_v10` = Qwen/Qwen3.5-4B + LoRA r16 (Modal volume `opendecide`, `/models/q35_4b_v10`), trained in 4 stages:
v0.7 (train_v07, 52.5k rows, 0.5 epoch) -> v0.8 (+1,518 double-verified LLM-authored items) -> v0.9 (+5,578 judge rows)
-> v0.10 (+2,335 Wikipedia deletion debates). Use style `cygnet`, temperatures noul 1.15 / choice 1.0, CUDA graphs
(`decoder_io.GraphRunner`, batch 1) for serving. Full report: `reports/opendecide_v10_report.html`
(published: https://claude.ai/artifact/32Jd6eZEaSqdUgLxqduFwc).

| Result | Jev | v0.10 |
|---|---|---|
| JevBench all 231 public items: correct / score (v14) | 200 / 73.28 (run 2: 199 / 72.91) | **203 / 74.88** |
| JevBench axes intel / calib / speed / cost | 82.0 / 80.9 / 91.2 / 52.5 | **83.7 / 83.3 / 92.3 / 53.7** |
| JevBench half B (NOT held out: seen 4 times over the project) | 96/113, 71.53 | **99/113, 73.82** |
| Decision suite (eval_card) vs jev_guard | see report | wins 8 metrics with CI excluding 0; behind on paraphrase drift, echo yes/no |
| Planted-authority audit (third-party zkousama/jagged, one attack direction): attacked acc / attack success | 27.0 / 99.4% | **90.7 / 11.2%** (clean balanced 88.6 vs 94.2: we lean 'deleted') |
| Long / multi-question / same 515 API requests (corrected 26 Sep: an earlier helper-script bug undercounted Jev) | 87.8 / 89.7 / 86.2 | **91.8 / 92.2 / 91.5** (+4.0, +2.5, +5.3) |
| End-to-end latency, same laptop (median / p95) | 194 / 305 ms | **115 / 124 ms** |

Rerun the key steps (from `opendecide-data/lean`):
```bash
M=../.venv/bin/modal
../.venv/bin/python build_train_v07.py   # also: build_train_v08.py, build_train_v09.py, build_train_v10.py (stage files)
$M run modal_od.py::train --name q35_4b_v07 --base Qwen/Qwen3.5-4B --recipe A3 --gpu H100 --epochs 0.5 --lr 7e-5 --beta 1.0 --style cygnet --train-file train_v07.jsonl --rel-file train_v07_relations.jsonl --splits dev,devzs,devp_card,pg_dev
$M run modal_od.py::train --name q35_4b_v08 --init q35_4b_v07 ... --epochs 0.8 --lr 4e-5 --train-file train_v08s2.jsonl   # then v09 (0.6 epoch), v10 (0.8 epoch)
$M run modal_od.py::jevbench --name RUN --base Qwen/Qwen3.5-4B --adapter /vol/models/q35_4b_v10 --tiers A --fmt cygnet --style cygnet --gpu H100 --graphs
$M run modal_od.py::eval_system --name q35_4b_v10 --splits dev,devzs,devp_card,pg_dev,eval_card,eval_jagged,eval_opi,eval_long,eval_multi --two-stage --meta-min 0.3
python3 apply_lbd.py q35_4b_v10 0.35 0.95 SPLITS && CAL_FIT=dev,devzs,devp_card python3 calibrate.py q35_4b_v10_plain q35_4b_v10_lbd
$M run serve_tunnel.py --name q35_4b_v10 --mode plain --gpu H100 --temps 1.15,1.0
```
Budget used on mahadikarya44: about $22-23 of $30 (bill lags; see `opendecide-data/lean/logs/budget_ledger.md`).
OpenRouter key: $2.18 of $5 used in total. **Rotate the OpenRouter key** (it was pasted in chat).

## Earlier models

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

- **Modal (first account):** $24.21 of $30 used after the $7 test round, about $5.8 left.
- **OpenRouter:** $0.67 of the $5 limit used.

## $7 test round (26 Sep 2026), results

Everything here is measured. "Half A" = JevBench selection split (118 items); Jev scores 103/118 on it.

| Test | Result | Verdict |
|---|---|---|
| Gemma v0.6 zero-shot **without** task cards vs guard-matched Jev | ZS choice 90.5 vs 92.6 (n.s.), ZS yes/no 91.6 vs 87.4, ZS negation 91.6 vs 85.3 | zero-shot gap closed even without cards |
| Frozen fast/strong candidates on half A (cygnet layout) | 2B 78, 4B 94, 9B 95, Gemma-12B 104; latency p50 39 / 54 / 51 / 88 ms | small models need fine-tuning |
| Cascade simulation (frozen): 9B first, escalate if confidence < 0.9 | **104/118 at p50 52 ms** (35% escalated); 4B→Gemma at 0.8 = 103/118 at p50 55 ms | Jev-level accuracy at ~4–5× lower median GPU latency; p95 ~450–520 ms |
| Open-Prompt-Injection strategies (SST-2 / IMDB / TweetEval-offensive, 1,080 rows; `build_opi.py`, `score_opi.py`) | ASR: Jev+guard 1.3%, Jev 2.3%, ours 2.0% (tie); clean accuracy **ours 90.0 vs Jev 87.2** | Jev resists blunt commands; tie |
| **jagged** (third-party, pre-registered AfD audit, 486 items; `build_jagged.py`, `score_jagged.py`) | Jev reproduced: clean 95.9, with injected line 26.5. **Ours: clean 75.3, injected 26.7** | both fooled by a planted "authority fact"; we also lose 20 pts clean (we under-call "deleted") |
| Calculator path (`calc_tool.py`) on 13 number/probability items | 9/13 vs 8/13 without; only 1/13 programs ran (others cut off at 320 tokens), and that one fixed a wrong answer | concept works; needs "compute only what's needed", more tokens, faster decoding |
| 1K–1M choices (`hc_scale`, gte-modernbert-base, Wikipedia-title filler) | Recall@64: 1K 100%, 10K 98.3%, 100K 93.3%, 1M 87.8%; search 0.08 → 5.9 ms | latency flat; recall needs a fine-tuned embedder / multi-probe |
| Write-blocked recurrent memory (`writeblock.py`, Qwen3.5-0.8B, untrained) | Policy-head output difference when only untrusted text changes: 0.0001 (block on) vs 0.001 (off). But untrained, clean accuracy on attacked items fell 45 → 10 | mechanism verified; must be trained with the block on |
| Modal network overhead (`latency_probe.py`, CPU echo) | web endpoint p50 356 ms vs **direct tunnel (modal.forward) p50 72 ms** | use a tunnel: end to end ≈ 72 + ~50 ms ≈ 120 ms vs Jev 203 ms |

**Priorities for the $30 account:**
1. **Injection (jagged).** Train on planted-evidence / fake-authority / "answer no" lines in untrusted fields, with write-block on. This is the clearest public beat-Jev target (Jev 26.5%).
2. **Fine-tune the fast tier** (Qwen3.5-4B or 9B) with the v0.6 recipe + KL anchor, then the cascade.
3. **Fix the calculator prompt** and serve with vLLM.
4. **Fine-tune the label embedder** with hard negatives for 100K–1M.
5. **Serve through a `modal.forward` tunnel.**

## Switching to the other Modal account (nothing is lost)

1. Log in: `../.venv/bin/modal token new` (creates a new profile), then `modal profile activate <new-profile>`.
2. Recreate the secret, after rotating the OpenRouter key and updating `opendecide-data/.env`:
   `modal secret create opendecide-keys HF_TOKEN=... OPENROUTER_API_KEY=...`
3. Upload the trained models:
   `modal volume create opendecide`, then for each folder `modal volume put opendecide backups/modal_models/NAME /models/NAME`. Start with `g12_v06_A3` and `q4b_v05_A3`.
4. The model cache (`/hf`) re-downloads by itself on first use. Code and data are mounted from this Mac, so nothing else needs copying.
5. Keep `HANDOFF.md` and the git history up to date after every round.

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
