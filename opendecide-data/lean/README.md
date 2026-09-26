# OpenDecide lean benchmark v0.1

This is a small benchmark for "System One" decision models: models that read a text and return probabilities for typed questions instead of generating text. It compares open GLiClass models, before and after our fine-tuning, with TypeSafe's closed Jev model.

## What's in it

- **Question types.** Rows are Jev-style `noul` (yes/no, answered as P(yes)) and `choice` (pick one option, answered as a probability distribution) questions.
- **Where the gold comes from.** Gold labels come from human-labelled sources: Banking77, CLINC150 (including out-of-scope), SMS Spam and Twitter Financial News. Every derived variant's gold follows from a fixed rule: negation flips it, a paraphrase keeps it, and an injection or distractor leaves it unchanged.

| Track | What it tests | States | Rows |
|---|---|---:|---:|
| ID | in-domain intents (test splits, de-duplicated against train by exact match and MiniLM cosine ≥ 0.95) | 200 | 1,000 |
| ZS | tasks never trained on (spam, financial sentiment) | 95 | 475 |
| INJ | prompt injection with **held-out** attack families (authority re-label, argue) inside forwarded/quoted/retrieved-note containers, plus echo controls | 180 | 360 |
| DIST | an irrelevant Wikipedia paragraph added before or after the message | 40 | 80 |

Each core state carries 5 questions:
1. a Choice question
2. a yes/no question about a label
3. its negation, in a **negation style never seen in training** ("Would someone who says that … be mistaken?")
4. a paraphrase
5. a double negation

Every row is scored alone. Rows are linked only in `data/eval_relations.jsonl`, so consistency measures what the model actually believes, not code that forces answers to add up.

**Train.** 11,296 rows: base rows, plus negation and paraphrase variants, MNLI propositions, train-only injection families with 1:1 echo controls, and filler from wikitext validation. Train and eval use disjoint wordings, attack families, containers and filler.

## Reproduce (v0.1, GLiClass on the laptop)

```bash
cd opendecide-data/lean
../.venv/bin/python build_data.py                                  # builds data/
../.venv/bin/python train.py --recipe A3 --out edge_A3             # ~7 min on an M4
../.venv/bin/python eval_local.py --model models/edge_A3 --name edge_A3 --latency
TYPESAFE_API_KEY=... ../.venv/bin/python run_jev.py                # 515 calls, ~$0.005
../.venv/bin/python score.py                                       # results/RESULTS.md
```

## v0.5: decoder model, trained and evaluated on Modal (Sep 25, 2026)

Model: `Qwen/Qwen3-4B-Instruct-2507` + LoRA (r16), prefill-only readout (softmax over the Yes/No or option-letter
logits, `decoder_io.py`), trained with the A3 recipe (task + complement/paraphrase consistency) on `train_v03`/`train_v05`.
More than 26 options: `gte-modernbert-base` shortlist (top 64) + knockout tournament (`hc.py`). Temperatures per question
type are fitted on dev only (`calibrate.py`). Nothing is trained on the laptop; the OpenRouter key sits in `../.env`.

| Data file | What it adds |
|---|---|
| `build_train_v03.py` → `train_v03.jsonl` | ~40 new train-only negation/paraphrase wordings, MNLI-neutral traps (1−p is penalised), BoolQ, CondaQA, long filler, new injection families, Yahoo topics |
| `build_multi.py` → `train_v04.jsonl`, `eval_multi.jsonl` | several records in one state (train-only and eval-only formats differ) |
| `build_train_v05.py` → `train_v05.jsonl` | MASSIVE intents, Civil Comments toxicity, Yelp sentiment (breadth) |
| `build_dev_zs.py`, `build_dev_zs2.py`, `build_dev_hc.py` | selection-only dev sets (AG News, Emotion, Enron spam, TweetEval, dev HC) |
| `build_weakness_eval.py` → `eval_hc.jsonl`, `eval_long.jsonl` | Jev-weakness slices: 78–2,000 options; ~1.5k/4.5k words of irrelevant state |

```bash
cd opendecide-data/lean
M=../.venv/bin/modal
$M run modal_od.py::bakeoff --models qwen3-4b,gliclass-modern-large --splits dev,devzs,eval       # zero-shot bake-off
$M run modal_od.py::train --name q4b_v05_A3 --base Qwen/Qwen3-4B-Instruct-2507 --recipe A3 --gpu H100 \
   --train-file train_v05.jsonl --rel-file train_v05_relations.jsonl --splits dev,devzs,devzs2,eval,eval_multi
$M run modal_od.py::evaluate --name q4b_v05_A3 --base Qwen/Qwen3-4B-Instruct-2507 --splits eval_long
$M run modal_od.py::hc_eval --name q4b_v05_A3 --base Qwen/Qwen3-4B-Instruct-2507 --split eval_hc \
   --embedder Alibaba-NLP/gte-modernbert-base --k 64
$M run modal_od.py::latency --kind decoder --hf-id Qwen/Qwen3-4B-Instruct-2507 --adapter /vol/models/q4b_v05_A3 --name q4b_v05_A3
../.venv/bin/python calibrate.py q4b_v05_A3                          # dev-fitted temperatures -> *_cal.jsonl
../.venv/bin/python run_jev.py                                       # Jev via OpenRouter (typesafe/jev-1.13)
JEV_SPLIT=eval_long ../.venv/bin/python run_jev.py; JEV_SPLIT=eval_multi ../.venv/bin/python run_jev.py
../.venv/bin/python run_jev_hc.py                                    # Jev >255 options (tournament wrapper)
../.venv/bin/python score.py --models jev q4b_v05_A3_cal             # core eval -> results/RESULTS.md
../.venv/bin/python score_weak.py --hc jev_tournament q4b_v05_A3 --long jev q4b_v05_A3 --multi jev q4b_v05_A3
```

## Known limitations (v0.1)

- The eval is small (295 core groups), so per-dataset numbers are wide. Use the pooled tracks and the CIs.
- There are no undecidable "trap" pairs yet. A model that simply answers negations with 1 − p would look perfectly consistent here. The full design (`../DESIGN.md`) adds them.
- The public test sets (Banking77, CLINC, SMS Spam, TFNS) may be in Jev's training data. Only fresh items rule that out, and they are planned but not included yet.
- Propositions are generated from label names ("the customer is asking about {label}"), not hand-written descriptions.
