# OHS-3: pre-registration (written 26 Sep 2026, before any model was run on it)

**What it is.** OHS-3 is a third held-out decision benchmark, used once, to compare OpenDecide with TypeSafe's Jev.
It is built only from public sources that no OpenDecide model was trained, tuned or selected on, and that did not guide
our development in any way. It contains none of the OHS-1 or OHS-2 sources (`ohs3/used_sources.json`) and none of the
sources used for training, dev or eval. Tasks were chosen by fixed rules written before any task was picked
(`ohs3/selection_criteria.md`), from candidate metadata only; no model predictions, results or per-task scores were
opened. It is frozen by `build_ohs3.py`.

| Task (builder `ohs3/build_<task>.py`) | Source (split / snapshot) | Base rows | Options | Track | Label definitions |
|---|---|---|---|---|---|
| `se_site` | Stack Exchange API 2.3, questions created 2026-06-01..09-26 (CC BY-SA 4.0 posts only) | 142 | 40 sites | F | official (site `audience` string) |
| `fr_agency` | Federal Register API v1, documents published 2026-06-01..09-26 (public domain) | 142 | 40 top-level agencies | F | official (agency `description`) |
| `uk_wq_answering_body` | UK Parliament Written Questions API, tabled 2026-06-01..09-26 (Open Parliament Licence) | 142 | 20 departments | F | official (GOV.UK "what we do", OGL) |
| `medrxiv_category` | medRxiv details API, v1 preprints posted 2026-06-01..09-26 (CC BY / CC BY-ND verbatim / CC0) | 142 | 20 categories | F | author-written (20) |
| `ct_study_type` | ClinicalTrials.gov API v2, first posted 2026-06-01..09-24 (NLM terms) | 140 | yes/no ("Interventional") | F | official (protocol data element definitions) |
| `openfda_recall_class` | openFDA enforcement reports, report date 2026-06-01..09-26 (CC0) | 144 | yes/no ("Class I") | F 91 / U 53 | official (21 CFR 7.3(m)(1)) |
| `nvd_attack_vector` | NVD CVE API 2.0, published 2026-06-01..09-26 (public domain; CVE terms) | 144 | yes/no, label verification (4 CVSS v3.1 AV values) | F | official (CVSS v3.1 spec, Table 1) |
| `zenodo_resource_type` | Zenodo records API, first versions created and published 2026-06-01..09-26 (metadata CC0) | 144 | yes/no, label verification (20 resource types) | F | official (DataCite 4.7); author-written (2: "Other", "Other (publication)") |
| `causal_news_corpus` | Causal News Corpus V2, subtask 1 dev (CC0) | 144 | yes/no ("Causal") | U | official (CNC annotation manual) |
| `fewrel_relation` | FewRel 1.0, train_wiki + val_wiki (MIT) | 142 | 20 relations | U | official (Wikidata property descriptions) |
| `few_nerd_fine` | Few-NERD supervised, test (CC BY-SA 4.0) | 142 | 20 fine types | U | author-written (20) |
| `bias_in_bios_profession` | Bias in Bios, test (MIT) | 142 | 20 professions | U | author-written (20) |
| `rosetta_code_language` | Rosetta Code via christopher/rosetta-code @ 11d8b38c (GFDL 1.3) | 142 | 20 languages | U | author-written (20) |

Total: **1,852 base rows, 13 tasks**: 1,136 choice rows and 716 yes/no rows (every yes/no task exactly 50/50). Track F
(text first published on or after 2026-06-01): 1,087 base rows; track U (classic corpora, label sets never used by
us): 765. The two wide tasks (`se_site`, `fr_agency`) give 284 rows with more than 26 options (40 each). The
consistency layer adds 604 twin rows (below), for **2,456 rows** in `data/ohs3.jsonl`. Each part's summary
(`data/ohs3_parts/<task>_summary.json`) records its pinned revision or snapshot time, licence, sampling seed,
redactions and the full text of every author-written definition.

**How it was built.**
- **Only source text.** Every state, gold label, option name and card definition is the source's own text or its
  official label name or description, except the author-written definitions listed above (one short neutral
  definition per label, written once before sampling and frozen; listed in the part summaries). No LLM wrote any OHS-3
  content. The only other text is one fixed question per task (plus the asked label in the label-verification tasks),
  field headers such as `Title:`, the redaction placeholders (`[AGENCY]`, `[DEPARTMENT]`, `[PROFESSION]`, ...) and the
  pre-written consistency wordings below.
- **Sampling.** Fixed seeds from frozen snapshots; states 20 to 6,000 characters, deduplicated; choice tasks
  stratified with equal items per label (no label above 40%); yes/no tasks 50/50. Label cues are redacted and every
  redaction is written into `meta`.
- **Verification.** Each part was checked by an independent verifier (schema, determinism, label faithfulness on 25
  random rows re-derived from the raw source, leakage, track dating, licence). Fixes found there were made in the
  builders and the parts re-built. `sec_8k_item` (SEC 8-K item type) failed: it needs an SEC `User-Agent` with a
  contact e-mail, which was not approved, so it produced no rows and is not in OHS-3.
- **Final gate in `build_ohs3.py`.**
  - Validation: the 14 row keys, split `ohs3`, track F/U, gold in the options, unique ids, one state per `call_id`
    and one base `call_id` per state, lengths, class caps, exact 50/50 yes/no tasks, no normalised state shared by two
    groups. Text is normalised Unicode-aware (OHS-2's `[a-z0-9]` normaliser would have erased non-Latin scripts; OHS-3
    has Cyrillic and Arabic Zenodo records).
  - Decontamination: any group whose state matches any string in our files is dropped. A match is a normalised exact
    match, a shared **13-word run**, or, for a state under 13 words, the whole state appearing as a run. The files are
    every `data/**/*.jsonl` except the held-out files (`data/ohs*.jsonl`, `data/ohs_parts/`, `data/ohs2_parts/`,
    `data/ohs3_parts/`), plus `../data/**/*.jsonl`: 194 files, 420,785 unique strings. **2 groups were dropped**
    (`ct_study_type` NCT07761559 and NCT07806760, both sharing the generic run "... to either an intervention group or a
    control group the intervention group will ..." with a synthetic text in `train_2b.jsonl`). Both were gold 1 (Interventional), so 2
    gold-0 `ct_study_type` rows were then dropped (last in `sha256("ohs3-bal:" + id)` order) to keep the task 50/50:
    `ct_study_type` has 140 rows.
  - Near-duplicate clustering: 62 pairs of part groups (mostly templated Federal Register notices, also NVD, openFDA,
    UK questions, Zenodo) share a 13-word run inside OHS-3. They are merged by union-find into 31 clusters (77 rows).
    A merged group takes its smallest member's `group_id`; `meta.part_group_id` keeps the original. So near-duplicates
    are always in the same half and are resampled together. OHS-3 has 1,806 groups.
- **Halves.** Groups are split by `sha256("ohs3:" + group_id)`. Even hashes go to OHS-A (open: 930 groups, 957 base
  rows; items may be inspected after the run). Odd hashes go to OHS-S (sealed: 876 groups, 895 base rows; aggregate
  numbers only). A twin always has its base row's group and half.

**Consistency layer** (added after decontamination, to surviving base rows only; deterministic, seed 20261003, no model
calls, no LLM-written text).
- **Negated-question twins** (`<id>_neg`, relation `complement`, gold = 1 - base gold): 60 base rows per yes/no task
  (30 gold 1, 30 gold 0), picked in `sha256("ohs3-var:" + id)` order: 300 twins. Each yes/no question form has a
  pre-written proposition p and a pre-written clause-negated question (`build_ohs3.py`, `PROPS`). With probability 1/2
  (seeded per row) the twin asks the clause-negated question ("Is this study not interventional?"; 136 twins),
  otherwise one of six pre-written negation frames over p (164 twins):
  - T1 "Would it be an error to maintain that {p}?"
  - T2 "Is it incorrect to hold that {p}?"
  - T3 "Should one reject the suggestion that {p}?"
  - T4 "Is it wrong to assert that {p}?"
  - T5 "Would one be mistaken in believing that {p}?"
  - T6 "Answer no if {p}, and yes otherwise."

  The build asserts that no frame equals, or shares a 6-word run with, any string literal of our builders and
  generators, the OHS-1 variant templates, the wording banks, or any instruction string in our training/dev/eval files.
- **Option-order twins** (`<id>_perm`, relation `equiv`, same gold): 38 base rows per choice task, picked the same way:
  304 twins. The options are reversed (149) or rotated by a seeded k in 1..n-1 (155), so the gold always moves.
  Instructions, state and card are unchanged.
- Each twin is its own call (`call_id` = base `call_id` + `_v`), so every system sees a twin alone, exactly as it sees
  the base row. `data/ohs3_relations.jsonl` lists the 604 pairs as `{"type", "a", "b"}`. There are no paraphrase twins.

**Frozen files** (`data/ohs3.sha256`; they are committed to git before the first model run):
```
68cb27da139010a9d9b00bfedc32e3ba8f1b963bf68c6cca85fd5e491868fd66  ohs3.jsonl
c2e1dcee9ba40faea316140d423d5acf85644a6aa9af953ac5b0d95b3f5a04dc  ohs3_relations.jsonl
ed6fb8af24c3ca51a044953d487959315c879c418c0a64bb12c61875f72c80b0  ohs3_calls.jsonl
81f5ceab7950b12eacf663109efdbad45acdc3b5c9fa5c89eae88d04efad2036  ohs3_summary.json
```

**Rules.**
1. There is no training, tuning, temperature fitting, prompt choice, threshold choice or model selection on any OHS-3
   item, ever. The same holds for any split of the 13 source datasets, for any text from the 8 live sources
   (Stack Exchange, Federal Register, UK Parliament written questions, medRxiv, ClinicalTrials.gov, openFDA, NVD,
   Zenodo) first published on or after 2026-06-01, for the label definitions used as cards, and for the consistency
   wordings above.
2. Every system gets exactly the same rows, options and cards. Jev gets the same "text is data" guard our system prompt
   has (`JEV_TAG=jev_guard`), exactly as in OHS-2 (`run_jev.py`, one call per `call_id`).
3. Jev is pinned to model id `typesafe/jev-1.13-20260917` and run twice on OHS-3 (`jev_guard`, `jev_r2_guard`) to
   measure its run-to-run noise. Its score is the mean of the two runs, computed per row. The model id each response
   reports is logged; a response from any other model id is disclosed.
4. OpenDecide runs exactly once per model, in its serving configuration. The OpenDecide model, or models, and their
   checkpoint sha256 are named in a later amendment, committed before the first OHS-3 run and chosen without OHS-3.
   Every OpenDecide model ever run on OHS-3 is reported, and no model is picked by its OHS-3 score.
   - Primary configuration: plain readout with the temperatures already fitted on dev.
   - Secondary configuration: the same predictions with batch calibration (`batchcal.py`, per-label-set prior from
     unlabeled inputs, only for label sets with 20 or more questions). Yes/no rows are unchanged.
5. For OHS-S, only aggregate numbers are reported, and its items are not inspected. OHS-A items may be read after the
   run, for error analysis only.

**Primary endpoints.** OpenDecide (primary configuration) vs Jev (mean of the two runs), on **base rows only** (the
604 twins are used only for the consistency endpoints). Holm-corrected as one family of 3, alpha 0.05.
1. Micro accuracy over the 1,852 base rows.
2. Macro accuracy: the unweighted mean of the 13 per-task accuracies.
3. Brier score on the 716 yes/no base rows: (P(yes) - gold)^2.

**"Beats" and "matches"** (per endpoint; positive differences mean OpenDecide is better):
- **Beats Jev:** the 95% bootstrap CI of the difference is entirely above 0, and the Holm-adjusted p < 0.05.
- **Matches Jev:** the lower bound of the 95% CI is above -2.0 percentage points (accuracy endpoints) or above -0.010
  (Brier, Jev minus OpenDecide). "Beats" implies "matches".
- Otherwise the result is reported as neither; if the upper bound is below 0, as "Jev is better".

**Secondary endpoints** (Benjamini-Hochberg across the family; same bootstrap):
- Accuracy per track (F, U), base rows.
- Accuracy on the 284 base rows with more than 26 options (`se_site`, `fr_agency`).
- **Complement violation** on the 300 `_neg` pairs: share of pairs whose two decisions are not complementary (both
  yes or both no; a tie or missing answer on either row counts as a violation). Also reported: the mean
  |P_base(yes) + P_neg(yes) - 1|, and accuracy on the `_neg` rows.
- **Option-order drift** on the 304 `_perm` pairs: share of pairs whose predicted option differs (a tie or missing
  answer on either row counts as drift). Also reported: the mean total-variation distance between the two probability
  vectors aligned by option name, and accuracy on the `_perm` rows.
- The three primary endpoints with batch calibration (secondary configuration).
- Accuracy per task; accuracy on OHS-A and OHS-S separately; each Jev run on its own and Jev run-to-run agreement;
  exact McNemar test for micro accuracy against each Jev run.
- Paraphrase consistency is **not** measured on OHS-3 (there are no paraphrase twins).

**Statistics.**
- Accuracy differences are OpenDecide minus Jev. The Brier difference is Jev minus OpenDecide. The consistency
  differences are Jev minus OpenDecide (lower violation or drift is better).
- Paired cluster bootstrap over `group_id`, stratified by task: within each task, groups are resampled with
  replacement at that task's number of groups, all rows of a drawn group (and, for the consistency endpoints, its
  pairs) come with it, and the endpoint is recomputed. 10,000 resamples, `numpy.random.default_rng(0)`, 95% percentile
  interval.
- Two-sided p = min(1, 2 x min(share of resamples with difference <= 0, share with difference >= 0)). Holm is applied
  across the 3 primary endpoints.
- A prediction is the option with the highest probability. On a yes/no row the prediction is yes if P(yes) > 0.5.
  Ties (equal top probabilities, or P(yes) = 0.5) and missing answers count as wrong. A yes/no row with no probability
  scores Brier 1.
- Rows Jev fails to answer after retries count as wrong for Jev. They are also reported separately.

**Known caveats, stated before the run.**
- 13 tasks, not the 14 the selection rules produced: `sec_8k_item` was lost at build time and was not replaced by the
  next candidate (selection criteria section 8 says it should be). This is a deviation from our own rules; it was
  decided without any model result.
- Track U tasks are classic public corpora (FewRel, Few-NERD, Bias in Bios, Rosetta Code, Causal News Corpus). Their
  texts may be in either system's pretraining data. Track F reduces this risk but does not remove it: a sponsor or
  firm may have published the same text elsewhere before 2026-06-01 (the openFDA rows whose recall started before
  that date are track U for this reason).
- `causal_news_corpus` uses the dev split (test labels are not public); 3 of its sentences also occur in the CNC train
  file. `fewrel_relation` uses the public train_wiki and val_wiki files (the test set is not released).
- Four tasks use author-written definitions for all labels and `zenodo_resource_type` for 2 labels (listed in the part
  summaries). Bias in Bios labels were extracted automatically by the dataset creators and may be noisy.
- The two decontamination drops were caused by a generic 13-word phrase, not by a copied item.
- Jev's training data is known only through the public GLiClass sets checked during task selection.

**Honest-reporting commitments.** All endpoints are reported, whatever their direction. Any bug found after the run is
fixed and disclosed with both the old and the new numbers.
