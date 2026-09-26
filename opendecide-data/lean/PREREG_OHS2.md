# OHS-2: pre-registration (written 26 Sep 2026, before any model was run on it)

**What it is.** OHS-2 is a second held-out decision benchmark. It is built only from public corpora that no OpenDecide
model was trained, tuned or selected on, and that did not guide our development in any way. It contains none of the
OHS-1 sources and none of the sources used for training, dev or eval. It is frozen by `build_ohs2.py`.

| Part (builder) | Task | Source (split) | Rows | Options | Track |
|---|---|---|---|---|---|
| `arxiv_fresh` | `arxiv_fresh_cs`, `_math`, `_stat_eess`, `_astro` | arXiv papers first submitted on or after 2026-09-21, single category only (live API snapshot of 2026-09-26) | 4 x 60 | 15 / 12 / 6 / 6 official category names, with official descriptions | F |
| `misc` | `moral_stories` | Moral Stories (test) | 120 | yes/no | U |
| `misc` | `argq_stance` | IBM ArgQ-30k stance (test) | 120 | yes/no | U |
| `misc` | `tabfact` | TabFact (official test) | 120 | yes/no | U |
| `misc` | `big_patent_cpc` | BigPatent (test), CPC sections A-H | 120 | 8 | U |
| `misc` | `medical_abstracts` | Medical Abstracts TC corpus (test) | 120 | 5 | U |
| `science` | `pubmed_rct20k` | PubMed 20k RCT (test) | 120 | 5 | U |
| `science` | `scifact` | SciFact (dev; test labels are not released) | 120 | 3 | U |
| `science` | `evidence_inference` | Evidence Inference (test) | 120 | 3 | U |
| `science` | `ddi2013` | DDI corpus 2013 (test) | 120 | 4 | U |

Total: 1,320 rows, 13 tasks, 1,320 groups (one row per group), 960 choice rows and 360 yes/no rows. The largest option
set has 15 options. The tracks are F (fresh corpus: 240 rows) and U (label sets never seen: 1,080 rows).

**How it was built.**
- **Only source text.** Every state, gold label, option name and card definition is the dataset's own text or its
  official label name or description. No LLM wrote any OHS-2 content. The only other text is one fixed question per
  task: 9 short strings (the four arXiv tasks share one) plus the Evidence Inference prompt template, which is the dataset's official prompt filled with
  the item's own outcome, intervention and comparator. Field headers such as `Title:` or `Argument:` are also added.
- **Sampling.** The test split is used when it has labels, otherwise the validation split. Seed 20261010. States are
  20 to 6,000 characters long and deduplicated. No class takes more than 40% of a task; yes/no tasks are 50/50.
- **Contamination checks by the part builders.** Candidates were checked against all our data. They were also checked
  against Jev-side training data: knowledgator GLiClass v1.0, v2.0 and v3-logic. And they were checked against the
  forbidden `tasksource/zero-shot-label-nli` premises and PubMedQA, at pinned revisions. Hits were skipped in the seeded
  rank order. Each part's summary lists these skips.
- **Final gate in `build_ohs2.py`.** It validates the rows: gold is in the options, ids are unique, each `call_id` has
  exactly one state and each state has exactly one `call_id`, lengths and class caps hold, and no two groups share a
  normalised state. It then drops any group whose state matches any string in our files. A match is a normalised exact
  match, a shared 12-word run, or, for a state under 12 words, the whole state appearing as a run. The files checked are
  every `data/**/*.jsonl` (including `data/v11_parts/`), except the held-out files, plus `../data/**/*.jsonl`. That is
  166 files and 417,780 unique strings. **0 groups were dropped.**
- **Halves.** Groups are split by `sha256("ohs2:" + group_id)`. Even hashes go to OHS-A (open: 657 rows, items may be
  inspected after the run). Odd hashes go to OHS-S (sealed: 663 rows, aggregate numbers only).

**Frozen files** (`data/ohs2.sha256`; they are committed to git before the first model run):
```
8e7a28d9463754a8f8902f7ea244ab5e79e49571a3ca2280ec22c594032310dc  ohs2.jsonl
6832a0ab894517df7d361da1882da2f1bb03d51abcec983b7be350bcc24596df  ohs2_calls.jsonl
```

**Rules.**
1. There is no training, tuning, temperature fitting, prompt choice, threshold choice or model selection on any OHS-2
   item, ever. The same holds for any split of the 12 source datasets, for arXiv papers first submitted on or after
   2026-09-21, and for the official label descriptions used as cards.
2. Every system gets exactly the same rows, options and cards. Jev also gets the same "text is data" guard our system
   prompt has (`JEV_TAG=jev_guard`).
3. Jev is run twice on OHS-2 (`jev_guard`, `jev_r2_guard`) to measure its run-to-run noise. Its score is the mean of
   the two runs, computed per row.
4. OpenDecide runs exactly once per model, in its serving configuration. The OpenDecide model, or models, and their
   checkpoint sha256 are named in Amendment 1. Amendment 1 is committed before the first OHS-2 run and chosen without
   OHS-2. Every OpenDecide model ever run on OHS-2 is reported, and no model is picked by its OHS-2 score.
   - Primary configuration: plain readout with the temperatures already fitted on dev.
   - Secondary configuration: the same predictions with batch calibration (`batchcal.py`). It uses a per-label-set
     prior estimated from unlabeled inputs, and only for label sets with 20 or more questions. On OHS-2 this covers
     all 10 choice tasks. Yes/no rows are unchanged.
5. For OHS-S, only aggregate numbers are reported, and its items are not inspected. OHS-A items may be read after the
   run, for error analysis only.

**Primary endpoints.** These are OpenDecide (primary configuration) vs Jev (mean of the two runs). They are
Holm-corrected as one family of 3, with alpha 0.05.
1. Micro accuracy over all 1,320 rows.
2. Macro accuracy: the unweighted mean of the 13 per-task accuracies.
3. Brier score on the 360 yes/no rows: (P(yes) - gold)^2.

**Secondary endpoints** (Benjamini-Hochberg across the family):
- The three primary endpoints with batch calibration (the secondary configuration).
- Accuracy per track (F, U), per part and per task.
- Accuracy on OHS-A and OHS-S separately.
- Each Jev run on its own, and Jev run-to-run agreement.
- Exact McNemar test for micro accuracy against each Jev run.
- A licence sensitivity check: the primary endpoints without `ddi2013` (CC BY-NC 4.0) and `pubmed_rct20k` (no licence
  file).

**Statistics.**
- Positive differences mean OpenDecide is better. Accuracy differences are OpenDecide minus Jev. The Brier difference
  is Jev minus OpenDecide.
- Paired cluster bootstrap over `group_id`, stratified by task: within each task, groups are resampled with replacement
  at that task's size, and the endpoint is recomputed. 10,000 resamples, `numpy.random.default_rng(0)`, 95% percentile
  interval. Here every group has one row, so this is a row bootstrap stratified by task.
- Two-sided p = min(1, 2 x min(share of resamples with difference <= 0, share with difference >= 0)).
  Holm is applied across the 3 primary endpoints.
- A prediction is the option with the highest probability. On a yes/no row the prediction is yes if P(yes) > 0.5.
  Ties (equal top probabilities, or P(yes) = 0.5) and missing answers count as wrong. A yes/no row with no probability
  scores Brier 1.
- Rows Jev fails to answer after retries count as wrong for Jev. They are also reported separately.

**Known caveats, stated before the run.**
- `ddi2013` is CC BY-NC 4.0, and `pubmed_rct20k` has no licence file (it is built on the MEDLINE/PubMed baseline).
  Both are used for evaluation only. The sensitivity check above reports the results without them.
- `scifact` uses the dev split because the test labels are not public. `arxiv_fresh` is a live snapshot, not a
  released split (`ohs2/arxiv_fresh_cache/`).
- `build_ohs2.py` does not open the OHS-1 files. Before the first run, the operator must check OHS-2 arXiv ids against
  the OHS-1 `arxiv2026` ids (ids only). If any id overlaps, those groups are dropped, the files are rebuilt and
  re-hashed, and an amendment discloses it before any model is run.
- Jev's training data is known only through the public GLiClass sets checked above.

**Honest-reporting commitments.** All endpoints are reported, whatever their direction. Any bug found after the run is
fixed and disclosed with both the old and the new numbers.
