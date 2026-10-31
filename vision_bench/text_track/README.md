# Text track of System One Bench: C1 vs base Qwen3.5-4B vs Jev's published numbers

Evaluation only. Nothing here is used for training, nothing calls Jev or OpenRouter, nothing is written under `opendecide-data`.
RESULTS: see `RESULTS.md` (generated from `results/scores.json`; the skeptic re-score is `results/skeptic.txt`).

## Result in short (run of 17 Oct 2026 01:16-01:29 UTC, one Modal H100, profile mahadikarya44)
- System One Index (mean accuracy of the 16 text suites): **C1 77.6** (SE 0.7) | base Qwen3.5-4B 73.0 | **Jev 1.14 79.3** | Jev 1.13 79.0.
- **C1 vs Jev 1.14: gap -1.65 points, SE 1.00, z -1.65 -> no difference demonstrated** (a win or loss needs gap >= 3 and z >= 2). Same call vs Jev 1.13 (-1.37).
- Calibration (ECE, all 4,850 decisions): C1 3.3% | base 8.1% | Jev 1.14 6.0% | Jev 1.13 6.1%.
- Latency, NOT COMPARABLE: C1 81 ms median / 218 ms p95 per call here (H100, batch 1, no network); Jev's published 136 / 175 ms include the network.
- Modal bill $0.95 of the $2 cap (GPU run $0.94 + CPU preflight $0.008). Skeptic re-score: all checks match.

## Caveats
- Unpaired comparison: Jev's per-item results are not published, and its numbers are one published run each. n = 200 per suite (SE 1.7 to 3.5
  points per suite); typed-decisions (2,000 decisions on 400 cases) is treated as 400 independent cases for the standard error.
- C1 is read with its own research readout (HF transformers, LoRA unmerged), not through the SGLang production server and not through the
  Decisions API wrapper that Jev sits behind.
- Whether any bench item overlaps C1's training data was not audited here (the bench items come from public datasets; C1's data is Claude-authored).
- Latency is a different machine, protocol and sample: never put it next to Jev's without the label.

## What was run
- **Items**: the bench's 16 text suites, 3,250 cases, 4,850 decisions (`data/cases.jsonl`, rebuilt from the bench's pinned sources with its own
  `build_suites.py` + `build_arabic.py`; its hash equals `data.lock.json` of system-one-bench commit `67b7f3d3`, checked again inside the GPU
  container by `harness/lockcheck.py`). Question text, criteria and gold are the bench's, byte for byte.
- **Models**: C1 = Qwen3.5-4B (rev `851bf6e8`) + LoRA `q35_4b_main500k` (sha256 `507d1c29`), and plain Qwen3.5-4B. Both arms come from ONE loaded
  model: the LoRA is on for `c1` and switched off (`peft disable_adapter`) for `base`, so both read the same prompts through the same weights.
- **Prompt / readout** (C1's own, from `lean/jevbench_od.py` + `fastcore/readout.py`, via the unchanged `decoder_io.py` snapshot): style `cygnet`,
  layout `schema_branch_mark` (read from the adapter's `train_meta.json`), thinking off. The answer is the option letter's probability read at the
  last prompt token (fp32 logsumexp over every token that decodes to the letter, T = 1.0). choice/score: two views (given order + exact reversal)
  averaged; yes/no: one read. State = `json.dumps(state, indent=1)`. Score options use C1's shipped form `"<i>: <level>"` (here the index IS the
  gold label, unlike CountBench). Dict `criteria` of yes/no questions become the definitions card, as in C1's production path.
- **Scoring**: the bench's UNMODIFIED `score.py` (run on our logs converted to the bench's prediction format; it checks the data lock itself).
  System One Index = 100 x mean of the 16 per-suite accuracies (typed-decisions is one suite of 2,000 decisions), exactly the site's `index()`.
  ECE = the bench's top-label ECE, 10 bins, over all 4,850 decisions. Jev 1.14 / Jev 1.13 = the bench's published runs `or_jev_114` / `or_jev`
  read from its `results.json` (never copied by hand). A failed decision is counted wrong in `acc_strict` (the bench counts it correct when the
  gold is option 0); both are printed next to the failed count.
- **Noise rule**: standard error of the Index = sqrt(sum of per-suite binomial variances)/16 (typed-decisions: 400 cases x 5 questions that share
  a state, so its n is taken as 400). Unpaired (Jev's per-item results are not published). A win or loss is called only if the gap is at least
  3 Index points AND |z| >= 2; otherwise "no difference demonstrated".
- **Latency**: NOT COMPARABLE with Jev's (different machine, no network, batch 1 on an H100 with HF transformers, 320 sampled calls). Reported
  separately, with the reasons.

## Labelled diagnostics (never the headline)
`score_noprefix`: score options as the bare criteria strings Jev receives (no `"<i>: "`), 1,000 items. `yn_swapped`: the yes/no read with the
letters swapped (No = A), 1,400 items; reported per order and averaged, so letter bias is visible.

## Safety checks (all enforced in code; each has a test in `tests/`)
1. LoRA really applied: `adapter_gate.verify_adapter_loaded` (copied verbatim from the reviewed vision harness; test asserts identical source):
   all 496 file tensors bit-equal to the injected parameters, all 248 lora_B non-zero, plus `|logits(LoRA on) - logits(LoRA off)| > 1e-3` and a
   C1-vs-base difference on the smoke items. C1 is loaded on its own text-only class (`Qwen3_5ForCausalLM`), where the adapter's native key names fit;
   the renaming route used for the multimodal class gives identical logits on the real weights (max diff 0.0, `tests/logs/class_equivalence.txt`).
2. Items, rows, views, options and gold for all 4,850 decisions equal C1's own `to_row`/`views_for` and the bench's `options`/`gold_idx` (`tests/test_rows_vs_c1_and_bench.py`).
3. One prompt set for both arms: C1's adapter-folder tokenizer and the base tokenizer render and tokenize every prompt identically (checked in the container).
4. Batched read == one-by-one read (gate), and again on the 320 timed batch-1 calls (agreement reported).
5. Skeptic: `harness/skeptic_rescore.py` recomputes every number from the raw per-view logits with code that shares nothing with the scorer, and
   compares with `scores.json` and the bench's own scorer output; `tests/test_scoring_synthetic.py` proves it catches a changed number, a tampered logit and a dropped decision.

## Files
`harness/` (tt_core, run_text, score_text, skeptic_rescore, adapter_gate, lockcheck, vendor/decoder_io.py), `modal_app.py`, `data/`, `tests/`,
`results/` (per-item logs `preds_*.jsonl`, `diag_*.jsonl`, `lat_*.jsonl`, `meta.json`, `gates.json`, `scores.json`, `skeptic.txt`, Modal files), `logs/`.

Run the tests with `/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -B -I tests/<file>.py` (the venv is only read).

## Tests (all passed; logs in `tests/logs/`)
| Test | What it proves |
|---|---|
| `test_adapter_gate_identical.py` | the LoRA "is it really applied" checks are the vision harness's, source-identical |
| `test_lockcheck.py` | the in-container data check equals the bench's `data_lock.py`; a one-character change in a case is caught |
| `test_rows_vs_c1_and_bench.py` | rows, views, options, gold of all 4,850 decisions equal C1's `to_row`/`views_for` and the bench's `options`/`gold_idx`; answers round-trip through the bench's `pred_dist` |
| `test_run_text_tiny.py` | the real `run_text.py` stages (gates, main, lat, diag) on a tiny random model with the real tokenizer: a forced failure is retried and flagged, a forced OOM is split |
| `test_scoring_synthetic.py` | `score_text.py` (running the bench's `score.py`) and the skeptic on complete synthetic logs: all numbers agree; a changed number, a tampered logit and a dropped decision are each caught |
| `test_real_model_cpu.py` | the real Reader on the real Qwen3.5-4B + C1 adapter (CPU): adapter proven, padded batch == one-by-one (diff 0.0), LoRA on != off (13.4), easy items right; 77-way candidate groups |
| `class_equivalence.py` (+ `logs/class_equivalence.txt`) | text-only class + native adapter == multimodal class + renamed adapter on the real weights, max logit diff 0.0 |
Run them with `tests/run_all_cpu_tests.sh` (the slow real-model one separately). The GPU run's own gates are in `results/gates.json`.

## Reproduce
`MODAL_PROFILE=mahadikarya44 modal run --detach modal_app.py --mode chain --run <name>` (about 12 min, $0.94), pull `modal volume get text-track-results /<name> <dir>`, copy
`results/*` here, then `harness/score_text.py`, `harness/ece_bootstrap.py`, `harness/skeptic_rescore.py`, `harness/make_report.py` (run with `python -B -I`).
