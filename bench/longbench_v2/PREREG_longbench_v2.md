# PREREG: LongBench v2 in longjev's "Jev keeps 8K tokens" protocol (DRAFT, 2 Oct 2026)

Status: **DRAFT.** Not committed. Nothing has been run on a model. The runs need the owner's OK.
Roadmap step 4. Kit: `bench/longbench_v2/`. Data and answers: `bench/external_quarantine/longbench_v2/` (git-ignored).

## 1. What we compare against

**Source.** [github.com/avshalomd/longjev](https://github.com/avshalomd/longjev), "Long inputs for TypeSafe AI's Jev decision model."

- Code: commit `9d317786820c69f8346687e94453bf3e801e8de5` (19 Sep 2026; the only commit).
- The numbers below come from the repo's README results section. Web-search index snapshots of the repo page still show them; the page title there is "... An experiment, published with its evals."
- **The current repo does not show these numbers.** The README has no results. `results/*.json`, `results/report.html` and `results/raw/` are git-ignored. The `.gitignore` says: *"Benchmark results and the lab notebook stay local: TypeSafe's terms forbid publishing benchmarks or performance information about Jev."*
- So the reference number was published and then withdrawn. **No per-item Jev answers were ever published.**

Published LongBench v2 numbers (read 2 Oct 2026). Each k is the unique integer that rounds to the stated percentage.

| Arm (longjev) | Items | Accuracy | k/n |
|---|---|---|---|
| **jev selector, keep 8K tokens** | 163 test questions "whose input had to be reduced" | **52.8%** | 86/163 |
| embed (qwen3-embedding-8b), keep 16K | same 163 | 49.1% | 80/163 |
| embed_then_jev, keep 16K | same 163 | 48.5% | 79/163 |
| truncate (start + end), keep 16K | same 163 | 40.5% | 66/163 |
| per-piece vote, no final call | same 163 | 36.8% | 60/163 |
| jev at 8K / 16K / 28K (tuning split) | 42 dev | 57.1 / 57.1 / 52.4% | 24, 24, 22 /42 |
| Jev, whole input (inputs that fit) | 93 | 48.4% | 45/93 |

Also published:
- jev vs embed on the test split: 16 vs 10 discordant items, exact McNemar p = 0.33.
- jev@8K: median cost 0.77 ¢ and median time 2.7 s per question.
- Budgets were chosen on the 42 tuning questions. jev tied at 8K and 16K; the code's tie-break (`max(acc, -budget)`) picks 8K.
- **No per-difficulty or per-length numbers for Jev were found.** `eval/report.py` computes them, but `results/summary.json` was never published.
- Jev version: `typesafe/jev-1.13` via OpenRouter.

## 2. longjev's exact protocol, as recorded from the code (file: what it does)

- **Data** (`eval/longbench.py`): `zai-org/LongBench-v2` `resolve/main/data.json`, unpinned. Main has not changed `data.json` since commit ac35867b (18 Dec 2024), so it is the file we pin: revision `2b48e494f2c7a2f0af81aae178e05c7e1dde0fe9`, sha256 `15d61c22d92c96900b3c4948b6aeea218d3214b676a65df48e7b8555604c7fe2`, 503 items.
- **Split** (`eval/longbench.py`): items sorted by sha256(`_id`). The first 100 are dev, the other 403 test.
- **Which questions** (`eval/run.py` cmd_run, report.build):
  - Items enter if `ceil(len(context)/3.0) <= --max-context-tokens`.
  - "Fits" means Jev-counted context tokens + 600 <= 28,000. Fitting items are the control group, read whole.
  - Only the others ("long") are scored for the headline, test split only.
- **Chunking** (`chunker.py`, `LongJev(chunk_tokens=800)`):
  - 800 estimated tokens = 2,400 characters at 3.0 chars/token.
  - Cut at the coarsest of `"\n\n"`, `"\n"`, `". "`, `" "`, recursively, then hard-split. Pieces are packed greedily up to 2,400 chars.
  - No overlap. The chunks join back to the exact context.
- **Scoring** (`questions.chunk_questions`, `selectors.score_jev`):
  - One Jev request per chunk (state = chunk text) with three questions: rel, ans (the task question) and suff.
  - Rel is the yes/no "This passage contains information that helps answer the following question: {q} Options: A: {A}; B: {B}; C: {C}; D: {D}".
  - The chunk's score is rel's P(yes). A failed chunk request scores 0.
- **Sizes** (`LongJev.recalibrate`): chunk token sizes are Jev's measured tokens for that chunk (usage minus a probe of the questions alone). Budgets are in Jev's tokens.
- **Budget** (`LongJev.effective_budget`): `max(1000, min(8000, int(32000*0.9) - longest final-question estimate))`.
- **Keep** (`assembler.select_round_robin`):
  - Chunks are taken best-first (stable order on ties), each costing its tokens + 15.
  - Taking stops at the first chunk that does not fit. If none fits, the single best chunk is kept.
- **Order and gaps** (`assembler.render_state`): kept chunks go back in document order. Each gap becomes `"\n[… about N tokens omitted …]\n"`, including a leading and a trailing gap.
- **Final prompt** (`LongJev.judge`, `questions.final_questions`):
  - Jev gets state = the reduced text, plus the task question `Choice(question.strip(), {A: choice_A.strip(), ..., D: ...})` and a sufficiency yes/no in the same request.
  - The answer is Jev's `choice`.
  - If Jev says the request is too long, the first 85% of kept chunks (in selection order) are kept and the call retried, at most 3 times.
  - The headline does not widen the budget.
- **Counting** (`eval/report.acc`): correct iff `choice == answer`. Items with no choice are **dropped from n**. Items whose run raised are absent from the file.

**Reconstructed (not published):** the item filter.
- The docstring's `--max-context-tokens 120000` gives 239 chosen items, which cannot produce 42 + 163 long items.
- Cap = 170,000 estimated tokens, plus a Jev ratio of 3.8 chars/token for "fits", gives **exactly 42 dev and 163 test long items** (and 96 fits against the published 93).
- Exact 42/163 holds for any cap in [165,500, 170,500] at ratio 3.8, and any ratio in [3.800, 3.825] at cap 170,000.
- Our tokenizer gives 3.63 chars/token pooled on the same contexts.
- Membership of the individual 163 cannot be checked, because no per-item file exists. Boundary uncertainty is about 3 items.

## 3. Item sets (frozen by `convert.py`; sizes are checked on every conversion)

| Set | Rule | n | Role |
|---|---|---|---|
| **test_proxy** | test split, chosen (cap 170,000), ceil(chars/3.8)+600 > 28,000 | **163** (58 easy / 105 hard; 69 short / 94 medium) | **PRIMARY** |
| dev_proxy | same, dev split | 42 | secondary (Jev's number is in-sample) |
| all_proxy | both | 205 | secondary |
| test_own / dev_own / all_own | "fits" with our tokenizer's count | 172 / 41 / 213 | secondary |
| control_proxy | chosen and fits | 96 | optional secondary (`--control`) |

- test_proxy sorted-ids sha256: `9b35ad6a72a29ce6133210c10ce9e8cfdcff54eb47c59e3cf974753d87cf17d9`.
- The run covers the union, 220 items with 27,465 chunks.
- The one item with two identical options is not in the union. The readout keys answers by option index anyway.

## 4. Models and settings (written before any run)

- **4B = C1** = `q35_4b_main500k`:
  - Qwen/Qwen3.5-4B @ `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a` + LoRA `adapter_model.safetensors` sha256 `507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078`.
  - Layout `schema_branch_mark`, style `cygnet`, no PRISM-X.
  - Loaded with `decoder_io.load(base, adapter=…, revision=…)`, then merged.
- **Readout = C1's committed A5 readout** (PREREG_FINAL A10 and line 1008):
  - Choice rows are read twice (given order + exact reversal), averaged.
  - Yes/no rows are read once.
  - T = 1.00 / 1.00. T changes neither the argmax nor the chunk ranking.
  - The identity view is stored as a report-only one-view number.
- **2B:** the shipped Qwen3.5-2B + PRISM-X I adapter. Its sha256, revision and A5 readout are filled in when the 2B ships. It uses the same kit and settings.
- **Cascade (2B → 4B):**
  - ohs3_lib's rule (`cascade_routed` / `cascade_answer`), applied to every decision: chunk relevance offline from the two finished runs, final question live.
  - tau, w_big, route_on and the Ts come only from the dev-only fit log for (shipped 2B, C1), named with its sha256 in `cascade_lb.json`.
  - The existing fit (`cascade_fit_dev_armI1600_to_pxE.json`) is for 4B-E, not C1. It must be refit on dev or explicitly adopted by the owner.
- **Protocol settings:**
  - Budget 8,000 of OUR tokens.
  - Chunk 800 est. tokens.
  - Batch 16 rows, token budget 12,000 (decoder_io.predict batching).
  - Reader window `decoder_io.MAX_LEN` = 16,384. Longer prompts are never truncated. A chunk prompt over it scores 0 (none on the real data, per the plan). A final prompt over it gets longjev's too-long retry (none expected).
- **Nothing is tuned on these items.** No budget, threshold, prompt or readout is chosen after seeing any LongBench v2 output.

## 5. Run once, and the comparison rule

1. **One run per model** on the real items, then score.
   - `run_lb.py` writes a ledger entry and refuses a second run of the same adapter.
   - `--resume` only continues the same interrupted run with identical settings. It never re-reads finished items.
   - No `--limit` and no fake model on real items. Timing smoke tests use synthetic items.
2. **The model runner never sees gold.** Gold (`lb_gold.jsonl`) stays on the Mac. Scoring is local.
3. **PRIMARY:**
   - Metric: accuracy on test_proxy (n = 163). Items with no answer (a failure) count **wrong**.
   - Compared with Jev's 86/163 = 52.8%, **unpaired**, because no per-item Jev answers exist.
   - Statistic: the difference with a Newcombe (method 10) 95% interval.
   - Verdict: **better** if the interval is above 0, **worse** if below, otherwise **no significant difference**.
   - At n = 163 the interval half-width is about ±10.7 pp. "Better" needs k ≥ 104/163 (63.8%); "worse" means k ≤ 68/163 (41.7%).
   - An unpaired bootstrap interval is reported for information only.
4. **If per-item Jev answers ever appear** (longjev's `items.jsonl` format), report a paired bootstrap and McNemar on the common items as an extra row. The primary stays as registered.
5. **Report-only, never decisive:**
   - dev_proxy against Jev 24/42 (in-sample for Jev).
   - all_proxy and the own-token sets.
   - longjev's counting rule (failures dropped).
   - The one-view readout.
   - By difficulty (easy/hard), length (short/medium) and domain. These are ours only; no Jev split exists.
   - Kept tokens and characters.
   - Seconds per question on one L4. Not comparable with Jev's hosted 2.7 s at 24-way concurrency.
   - Overlap sensitivity (`--overlap overlap_counts_c1_train.json`): test_proxy without the 1 question/option-overlap item, and without the 25 context-overlap items.
   - Optional control: our model reading fitting inputs whole (`--control`, up to ~28K tokens, decoder_io.MAX_LEN raised at runtime only) against Jev's 45/93. Different n (96 vs 93).

## 6. Disclosures (to print with any number)

- **Context length:** the model was trained only up to ~8K tokens (`micro_tokens` 8192). The final prompts here are about 8–10K tokens (at most 8K of kept text plus 0.4–1.8K of prompt; plan median overhead 390 tokens). The control arm, if run, is far beyond training length.
- **Contamination:**
  - LongBench v2 has been public since Dec 2024, so pretraining exposure is possible for both Qwen3.5 (our base) and Jev.
  - Our fine-tuning data was checked with `overlap_counts.py`. It is counts-only, uses lower-cased word 13-grams, and samples every 20th context 13-gram of the 220 union items.
  - **C1's training file** (`v14_parts/golden_train.jsonl`, 501,732 records) results:
    - 1 record shares a question/option 13-gram with **1 test_proxy item**. It comes from the `climate_targets` source.
    - No exact question or option strings.
    - 656 records share sampled *context* 13-grams with 34 union items (25 of them in test_proxy). These are shared public documents, not questions or answers. Among our raw source files, the most context hits are in `raw/finqa` (204), `raw/tatqa` (194) and `raw/tathqa` (122), all financial-report sources.
  - **All 697 local jsonl files:** 1 item with a question/option hit and 1 with an exact option/question string. The exact string is only in older training files (v07–v11c, ohr), not in C1's. 44 union items have context hits.
  - Hit ids (LongBench `_id` only) are in `overlap_counts_c1_train.json`. The all-files counts are in `overlap_counts.json`. Both are in the quarantine.
- **The Jev number:**
  - It comes from a README version that longjev withdrew. The repo now cites TypeSafe's terms against publishing Jev benchmarks.
  - It is a third-party wrapper's result (longjev v1, Jev 1.13), not TypeSafe's own.
  - Any public comparison should cite it as such, and the owner should check the terms question before publishing.
- **Not replicable exactly:**
  - (a) The exact 163 items: reconstructed, counts match.
  - (b) Jev's tokenizer: budgets are in our tokens. Ours is 3.63 chars/token against Jev's reconstructed ~3.8, so we keep slightly less text per 8K.
  - (c) Jev read rel, ans and suff in one request. We read rel alone (ans and suff do not affect the 8K answer).
  - (d) Jev's internal readout and tie handling. Ours: first maximum in A–D order.
  - (e) Whether any of Jev's 163 had failures dropped from n.
  - (f) The per-piece vote and widening arms are not run.
- **Hardware and cost** differ: one L4, chunks batched, items sequential, against a hosted API at 24 concurrent requests.

## 7. Compute (od-l4, estimated)

Inputs:
- From `lb_select.py --plan` on the real items (aggregates only): 27,465 chunk scorings × 1,132 prompt tokens on average = 31.1M tokens.
- Final reads: 220 × ~8.5K tokens × 2 views = 3.7M tokens.
- Per-token cost, from our own v154 L4 runs (batch 1, eager): 4B 0.258 ms/token, 2B 0.082 ms/token.

| Run | Chunk scoring | Final reads | Total (+ ~2 min load/warm-up) |
|---|---|---|---|
| 4B (C1) | 27,465 × ~290 ms ≈ 2.2 h | ≈ 0.3 h | **≈ 2.5 h** (test_proxy alone ≈ 1.9 h) |
| 2B | 27,465 × ~93 ms ≈ 0.7 h | ≈ 0.1 h | **≈ 0.8 h** |
| Cascade | none (reuses both runs' chunk reads) | 2B on 220 + 4B on routed | **≤ 0.4 h** |

Batching may be faster. Prompts of 8K+ tokens may be slightly slower. Each manifest records the real numbers.

## 8. Commands

See `README.md` in this folder.
