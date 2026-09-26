# OHS-1 core: pre-registration (written 26 Sep 2026, before any model was run on it)

**What it is.** A held-out decision benchmark built only from public corpora that no OpenDecide model was trained,
tuned or selected on. Five parts, each built by `ohs/build_<part>.py` and checked by an independent verifier:

- `arxiv2026`: papers submitted Aug-Sep 2026, after Qwen3.5's release. Category choice among official subcategories, with official descriptions.
- `legal`: CC BY LegalBench tasks and the 100-way LEDGAR provision choice.
- `negation`: ScoNe contrast sets, This-is-not-a-dataset triples and HateCheck functionalities.
- `factsci`: PubMedQA and VitaminC contrastive pairs.
- `emo_intent`: GoEmotions (28-way) and Schema-Guided Dialogue unseen-service intents, if loadable.

`build_ohs.py` merges the parts. It drops any item that shares its text or a 12-word run with anything we touched, adds new-wording negation and paraphrase variants, splits by group into OHS-A (open) and OHS-S (sealed), and writes `data/ohs.sha256`. The files and the hash are committed to git before the first model run.

**Rules.**
1. No training, tuning, temperature fitting, prompt choice or model selection on any OHS item or on any split of its source datasets, now or later.
2. Every model gets exactly the same rows. Jev gets the same options and official descriptions, plus the same "text is data" guard our system prompt has (`JEV_TAG=jev_guard`).
3. Jev is run twice (`jev_guard`, `jev_r2_guard`) to measure its run-to-run noise.
4. Our models are run once each, in their serving configuration: plain readout, with the temperatures already fitted on dev.
5. For OHS-S, only aggregate numbers are reported; its items are not inspected.

**Primary endpoints** (Holm-corrected as one family of 3), OpenDecide v0.10 vs Jev (mean of the two runs):
1. Micro accuracy on all base rows.
2. Macro accuracy over tasks.
3. Brier score on yes/no base rows.

**Secondary endpoints** (Benjamini-Hochberg):
- Per-track accuracy (F fresh corpus, U unseen labels, C natural negation).
- Accuracy on items with more than 26 options.
- Consistency on the variant layer: complement violation, double-negation drift, paraphrase drift and flip rate.
- The same endpoints for the students (q35_2b_kd, q35_08b_kd) and for frozen Qwen3.5-4B.

**Statistics.**
- Paired cluster bootstrap over `group_id`, stratified by task, 10,000 resamples, seed 0.
- Exact McNemar test for micro accuracy.
- Ties (equal top probabilities) and missing answers count as wrong.
- Rows Jev fails to answer after retries count as wrong for Jev, and are also reported separately.

**Honest-reporting commitments.** All endpoints are reported whatever their direction. Any bug found after the run is
fixed and disclosed with both the old and the new numbers.
