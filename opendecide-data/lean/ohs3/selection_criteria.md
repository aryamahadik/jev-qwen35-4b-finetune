# OHS-3 task selection criteria

Written 2026-09-26, before any task was chosen. These rules are the only basis for choosing tasks from
`ohs3/candidates.json`. The input is the candidate metadata only: access, licence, labels, label-definition source,
size, dates and listed risks. No model predictions, results, logs or per-task model scores were opened. No model or
LLM API was called. Tasks are not chosen by expected model performance, and task types are not favoured or avoided
because they look like our training data.

## 1. Targets

- 14 to 18 tasks, each with 110 to 150 items, about 2,000 items in total.
- At least 600 yes/no rows (qtype `noul`, role `aff`, exactly 50/50 gold within each task).
- At least 5 tasks on fresh text (first published after 2026-06-01, track F). All other tasks are track U.
- Option counts: yes/no tasks; choice tasks have 3 to 20 options, except the wide tasks (section 5), which have 27 to 255.
- Fixed sizes, applied to every task:
  - yes/no task: 126 items (63 yes / 63 no)
  - choice task: 124 items
  - 16 tasks of this shape give about 2,000 items. If a source cannot fill its size, it may go down to 110
    (an even number for yes/no), never lower.

## 2. Hard exclusions (a candidate that fails any one is out)

E1. **Licence.** The source's own publisher or its official card must state a licence or terms that allow
    redistribution of the text in a public test file. Accepted: public domain / US government work, CC0, CC BY,
    CC BY-SA, OGL v3, Open Parliament Licence, MIT, Apache 2.0, GFDL (with notice), and NLM / CVE terms of use
    (with attribution). Excluded: NC licences, platform ToS only (no content licence), licences stated only on a
    third-party mirror and marked "check"/"verify", and sources with no stated licence. If licences differ from item
    to item, only items under an accepted licence are used (NC and "no reuse" items are dropped; ND items are used only
    verbatim, with no redaction).

E2. **Label reliability.** Excluded if any of these applies:
    (a) the label records where the text came from (site or outlet), not what the text says, while the task asks
        about content (for example, the source site decides "sarcastic" or "clickbait");
    (b) the source reports low annotator agreement (exact agreement under 50%), or its labels are flagged as
        low-agreement or multi-label without an agreed single label;
    (c) the label cannot be decided from the text shown (it depends on a document the reader does not see, or on an
        official designation that the text does not state);
    (d) the labels were made by a third party that is not the dataset's creator (for example by binning the
        original scores), or a mirror disagrees with the official release (then only the official release may be used);
    (e) the label set has two or more undefined catch-all classes at the same level (for example "general" and "other");
    (f) the "labels" are exam or collection provenance that the text alone cannot separate (for example "high school X"
        vs "college X").

E3. **Overlap.** Excluded if any of these applies:
    - the dataset, in any config or split, is in `ohs3/used_sources.json`;
    - the dataset is in `tasksource/zero-shot-label-nli`;
    - the dataset is in the GLiClass corpora (Jev side);
    - the label taxonomy is the same narrow taxonomy as one already used, or a subset or sibling of it. This covers
      arXiv category taxonomy for any archive, PubMed RCT abstract roles, SemEval-2010 T8 relations, TweetEval irony,
      and the other taxonomies in `used_sources.json` families_note.

    A broad family being covered (such as "biomedical" or "government") does not by itself exclude a candidate.
    Only the same dataset or the same narrow taxonomy does.

E4. **Availability.** The source must be loadable today, with enough items to fill at least 110 items under the
    sampling rules in section 6.

## 3. One task per dataset and per taxonomy

Candidates that share a dataset or API (Federal Register; NVD and GitHub advisories, which are the same
vulnerabilities; the UK government department taxonomy, shared by Parliament written questions and GOV.UK
organisations and document types; ClinicalTrials.gov; Stack Exchange) form one group. Each group gives at most one task.

Within a group, the member is chosen by these rules, in order:
1. Quota need: if the yes/no row target (600) cannot be met without this group, pick the member in yes/no form.
2. The priority order P1 to P5 (section 4).

## 4. Priority order (used whenever candidates compete for a slot)

- P1. Fresh text (track F) before classic (U). Fresh text is the stronger held-out guarantee.
- P2. Label definitions from an official source before author-written definitions.
- P3. Needs no redaction of the text to remove a label cue, before needs redaction. Less editing of the source text.
- P4. Larger pool of eligible items (for wide slots: more distinct labels with at least 5 items each).
- P5. Alphabetical by candidate id. This is the final, deterministic tie-break.

## 5. Wide tasks and option caps

- Exactly 2 wide tasks, each with 40 options: the 40 most frequent labels in the frozen snapshot, after the source's
  own dedup and overlap rules. Two gives a margin over the minimum of 1, and keeps most choice tasks in the 3 to 20 range.
- Wide slots go to eligible, selected candidates that have at least 27 labels with 5 or more items each, ranked by
  P1 to P5.
- Every other choice task with more than 20 labels is capped at 20. It keeps the 20 most frequent labels in the
  split or snapshot used, with ties broken by a seeded shuffle (`random.Random(3)`). Items with other labels are dropped.

## 6. Breadth

- Each task is given one of these domains: science, software, law/government, commerce/finance, social/online,
  news, everyday/general knowledge. Every domain must have at least 1 task and no domain more than 4.
- If a domain would exceed 4, its lowest-ranked task by P1 to P5 is dropped. If a domain would have 0 tasks, the
  highest-ranked eligible candidate in that domain is added.

## 7. Filling the count

After E1 to E4 and the group rule, all remaining candidates are taken if their number is between 14 and 18.
- Over 18: drop the lowest-ranked by P1 to P5, subject to the quotas and domain rules.
- Under 14: add from the group runners-up in P1 to P5 order.

## 8. Sampling and building rules (same for every task)

- Items are sampled with a fixed seed from the frozen snapshot or revision recorded in meta.
- Choice tasks: stratified, with equal items per label and the remainder given to labels in seeded order. No label
  takes more than 40% of a task.
- Yes/no tasks: 50/50 gold. The card holds the asked label and its official definition.
- State text is 20 to 6,000 characters, deduplicated (exact match and normalised-whitespace match), and contains no
  label cue. Every redaction is listed in the task's builder notes and written into meta.
- Options are the task's label names. Cards give "- label: definition" from the official source. Where no source
  exists, one short neutral definition per label is written once, frozen, and listed as author-written in the summary.
- If a selected task cannot reach 110 items at build time, it is replaced by the next candidate under these same
  rules (group runner-up first). If a yes/no task is lost, the remaining yes/no tasks go up to 150 items so the
  600-row minimum still holds.

## 9. Overlap check done for E3

The GLiClass corpora (GLIClass-v1.0, gliclass-v2.0, gliclass-v3-logic-dataset; local HF cache) were checked by
scanning their label strings for signature labels of every candidate. The scan found only generic web texts with ad-hoc
labels, and no dataset-level overlap with any candidate. The zero-shot-label-nli check was done in the candidate search.

## 10. Amendment 1 (2026-09-26, while applying E1-E4, before the task list was fixed)

Two licence checks at the official sources changed the yes/no picture. These were the only new facts:

- The official amazon-science repo LICENSE for amazon_counterfactual is CC BY-NC 4.0, so it fails E1.
- For fake_job_postings, CC0 is stated only by an HF re-uploader. The creator's EMSCAD site does not respond, so
  there is no licence from the publisher and it fails E1.

After this, only 3 natural yes/no candidates are left, which is below the 600-row target. Section 3 said "yes/no
form" without defining it for multi-class sources. This amendment defines it and makes the sizes follow the task
count. No other rule was changed.

- **Yes/no form.** A candidate with a natural binary label (for example Class I vs not, or interventional vs
  observational) uses that label. Natural binary forms are always taken first.
- **Label-verification form.** Any other choice task can run as yes/no. Each item asks one label: in half the items
  the asked label is the gold label (gold 1), and in the other half it is a different label drawn with a seed from the
  task's label set (gold 0). The asked labels are spread as evenly as possible over the label set. The card gives the
  asked label and its definition.
- **Filling the quota.** If the natural yes/no tasks give fewer than 600 rows, the selected non-wide choice tasks are
  ranked by P1 to P5, and the top-ranked ones switch to label-verification form until the yes/no rows reach 600 or more.
- **Sizes.** Sizes are set so the total is about 2,000 for the final task count T. Every task gets
  n = floor(2000 / T) to the nearest even number, kept within 110 to 150. Yes/no tasks get the even n; choice tasks
  get n - 2 if that is needed to keep the total at 2,000 or below. For T = 14, that is 144 per yes/no task and 142 per
  choice task.

## 11. Result of applying the rules (record)

Excluded:
- E1 (licence):
  - github_issue_type: ToS only, no content licence
  - humaid_humanitarian: NC
  - nlbse_code_comment: no licence stated
  - amazon_counterfactual: official licence is CC BY-NC 4.0
  - fake_job_postings: licence only from a re-uploader
  - colbert_humor: licence marked "check"
  - cognitive_distortions: terms to check
- E2 (label reliability):
  - clickbait_titles, sarcasm_headlines, colbert_humor: (a), the source site decides the label
  - cefr_sentence_level: (b), 37% agreement
  - cognitive_distortions: (b), low agreement and multi-label
  - fr_significant: (c), OIRA designation not in the text
  - se_close_reason: (c), "Duplicate" needs the original post, and closure is a moderator judgement
  - stanford_politeness: (d), bins made by Cleanlab
  - mathqa_category: (e), "general" and "other" at the same level
  - mmlu_subject: (f), high school vs college provenance
- E3 (overlap):
  - arxiv_physics_subcat, arxiv_nlin_subcat: arXiv category taxonomy already used
  - csabstruct_role: sibling of the PubMed RCT role taxonomy
  - sarcasm_headlines: also a sibling of TweetEval irony

Group picks (section 3):
- Federal Register: **fr_agency**. fr_doc_type ties with it on P1 to P4 and loses on P5.
- NVD/GHSA: **nvd_attack_vector**. It wins on P3 (no redaction); nvd_cwe and ghsa_ecosystem need redaction.
- UK government: **uk_wq_answering_body**. It wins on P4 (28,500 items since June). All three members need redaction.
- ClinicalTrials.gov: **ct_study_type**. It is natural binary and is taken first for the yes/no quota.
- Stack Exchange: **se_site**. se_close_reason is excluded under E2.

Remaining: 14 tasks, which is inside 14 to 18, so all are taken (section 7).
- Wide tasks (section 5): **se_site** (P3, no text redaction) and **fr_agency** (P4, most labels among the tasks
  that need redaction).
- Yes/no: 3 natural yes/no tasks (ct_study_type, openfda_recall_class, causal_news_corpus) give 432 rows. Under the
  amendment, the two top-ranked non-wide choice tasks by P1 to P5 switch to label-verification form:
  **zenodo_resource_type** (F, official definitions, no redaction, largest pool) and **nvd_attack_vector**
  (F, official definitions, no redaction). Yes/no rows: 5 x 144 = 720.
- Choice rows: 9 x 142 = 1,278. Total: 1,998 rows, 9 F tasks and 5 U tasks.
- Domains:

  | Domain | Tasks |
  |---|---|
  | science | ct_study_type, medrxiv_category, zenodo_resource_type |
  | software | nvd_attack_vector, rosetta_code_language |
  | law/government | fr_agency, uk_wq_answering_body |
  | commerce/finance | sec_8k_item, openfda_recall_class |
  | social/online | se_site |
  | news | causal_news_corpus |
  | everyday/general knowledge | few_nerd_fine, fewrel_relation, bias_in_bios_profession |
