# Vision bench: C1 and base Qwen3.5-4B on the System One vision track (Vision Index, 5 image suites)

STATUS (2026-10-16, after the review fixes): data, harness, scorer and all fixes are done and tested on CPU; the GPU stages have
NOT run, because the L4 is held by C2's idle SGLang server (pid 369128, 20.2 of 23 GB) and the permission layer denied stopping
it. See VM_NOTES.md. There are no C1/base numbers yet. When the GPU is free: `nohup bash ~/vision_bench/harness/gpu_chain.sh`.

## What is here
- data/<suite>/cases.jsonl + images/   the five Vision Index suites rebuilt from the pinned sources. Every suite's hash
  (case JSON incl. gold + sha256 of every image file) equals data.lock.json of system-one-bench (harness/verify_lock.py).
  img_refcoco (Box, not in the Index) is not built: C1 has no box readout.
- harness/vb_core.py       items -> C1 rows (lean/jevbench_od.py to_row) -> multimodal prompt -> candidate-token readout; adapter loading + proof.
- harness/run_vision.py    smoke / eval (warm pass, timed batch-1 pass with one retry of failures, labelled diagnostic arms, batched
                           throughput, localhost HTTP end-to-end sample of 200 requests at 1 and 8 in flight).
- harness/score_vision.py  the bench's formulas + Jev's published numbers; per-suite failed counts, strict accuracy, noise rule, diagnostics.
- harness/gpu_chain.sh     the whole GPU part; refuses to run unless the GPU is free; never stops or starts a C2 process.
- tests/                   CPU tests of every fix (see below). harness/check_prompts.py, prep_all.py: CPU prompt checks.
decoder_io.py is a read-only snapshot (copied 2026-10-16) of C1's own prompt builder and candidate-token readout
(lean/decoder_io.py), used unchanged. Nothing in the C2 tree was edited.

## Review fixes (all 7 confirmed issues)
1. The C1 LoRA was silently not applied (changes numbers). C1 was trained as the text-only class, so its 496 adapter tensors are named
   `base_model.model.model.layers.N...`; the multimodal class names the same modules `model.language_model.layers.N...`, and peft only
   warns and leaves every lora_B at zero. Fix: vb_core.build_renamed_adapter writes a COPY of the adapter with the prefix renamed
   (values untouched; source sha256 must start 507d1c29), and vb_core.verify_adapter_loaded proves it: all 496 file tensors sit bit for bit
   in the injected LoRA parameters, no injected parameter is left out, all 248 lora_B are non-zero. run_vision.meta() hard-fails
   otherwise, and also requires |logits(LoRA on) - logits(LoRA off)| > 1e-3 on a probe item. gpu_chain.sh adds a gate that C1 and
   base give different answers on the 10 smoke items. Tests: tests/test_adapter_fix.py (tiny model: old load caught, fixed load equals the
   trained-side load to 0.0, corruption caught), tests/test_real_adapter_names.py (real adapter + real architecture on the meta device:
   496 of 496 tensors find a home, 0 shape mismatches, LoRA never touches the vision tower).
2. img_count options carried a misleading "i:" prefix (changes numbers). HEADLINE now shows the criteria strings exactly as Jev
   receives them ("exactly two" ... "exactly ten", no prefix). C1's own text-bench form ("0: exactly two" ...) is run only as the labelled
   diagnostic `count_prefixed` (200 items), so the effect of the prefix is reported, not hidden. Declared before any run.
3. Failures: the bench's scorer counts a failed item as correct when its gold is option 0 (uniform answer, argmax 0). The scorer
   prints `failed` per suite next to every accuracy, an `acc_strict` (failed = wrong) and a strict Vision Index whenever failed > 0.
   run_vision retries a failed item once (flagged `retried`, first error kept) so a transient error does not become a hole.
4. Latency: printed in its own block labelled NOT COMPARABLE, with the reasons (Jev: 1,200 calls incl. 200 Box, cloud host near
   OpenRouter, network + base64 + 8 in flight; here: L4, no network, batch 1, shared CPU). The HTTP sample is now 200 requests per
   concurrency (p95 rests on 10 points, not 5) and the load average is recorded in meta_*.json and summary_*.json.
5. Yes/no order: the headline stays C1's shipped single read (Yes = A). A labelled diagnostic reads SST-2 and VQA once more with the
   letters swapped (No = A, 400 items) and reports each order, the average, agreement and mean P(Yes), so letter bias is visible.
6. Power: the scorer prints the standard error of every Index (about 1.1 points) and of the gap to Jev (about 1.6), per-suite gaps with
   z, and calls a win or loss only if the gap is at least 3 Index points AND z >= 2; otherwise "no difference demonstrated". Unpaired
   (Jev's per-item results are not used).
7. score_model no longer crashes when a whole suite has no successful row (latency is None, failed = 200 is shown). Test: tests/test_scorer.py.

## Protocol (declared before any run)
- Headline arm: C1's own prompt layout (schema_branch_mark / cygnet, read from the adapter's train_meta), thinking off, T = 1.0,
  yes/no one read with Yes = A, choice and count two views (given order + exact reversal) averaged, image inside the untrusted markers,
  HF transformers bf16, LoRA unmerged (fp32 adapter weights), not SGLang. The Jev Decisions API wrapper is server-side and not public.
- The base Qwen3.5-4B arm uses the same prompts and readout without the adapter.
- Scoring: Vision Index = 100 x mean of the five suite accuracies, argmax of the option probabilities; ECE 10 bins on max probability.
- Not comparable: latency and cost (see above). Box (RefCOCO) is N/A. n = 200 per suite: standard error 1.7 to 3.4 points per suite.
- Evaluation only. Nothing here is used for training.

## CPU test log (this fix round; run with /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -I)
tests/test_adapter_fix.py, tests/test_real_adapter_names.py, tests/test_variants.py (real tokenizer, all 1,600 prompts build),
tests/test_scorer.py, tests/test_run_vision_tiny.py (the real smoke/eval/e2e code on a tiny random model incl. the retry path and the
scorer), plus the reviewer's review/splice_test.py, scorer_equiv.py (66 metrics identical to the bench formulas) and failure_quirk2.py.
