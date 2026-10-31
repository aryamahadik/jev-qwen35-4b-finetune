# Golden dataset v14: the build spec (every builder follows this)

**Goal:** about 500,000 training rows for a decision model that must beat Jev (jev-1.13). The priority is
**yes/no reasoning**, where Jev leads us most (fresh-exam yes/no 96.1 vs our 88.6). Weak spots in detail: moral
and social norms, fact verification against tables, science and health claims with evidence, negation, exceptions.
Multiple-choice decisions are already level with Jev and are kept for breadth.

## Hard rules (break one and the dataset is rejected; when unsure, reject)
1. **Exclusions.**
   - Never use a dataset listed in `lean/ohs3/used_sources.json` for eval, dev or held-out use, or any OHS-1/2/3
     source (list below).
   - Never use anything in `golden_src/forbidden_label_nli.json`: the 152 tasks of tasksource/zero-shot-label-nli,
     including aggregates that fold them in.
   - Never use anything derived from those or sharing texts with them.
   - No Stack Exchange text.
   - **OHS sources (forbidden):** arxiv2026_*, arxiv_fresh_*, go_emotions, hatecheck, legalbench (any), lexglue
     ledgar, pubmedqa, scone, sgd, this_is_not_a_dataset, vitaminc (and FEVER, which it is built from), big_patent,
     ddi2013, evidence_inference, ibm_argq30k (any IBM argument quality or stance set), moral_stories, pubmed_rct,
     scifact, tabfact, bias_in_bios, causal_news_corpus, clinical-trial study type, few_nerd, fewrel, Federal
     Register agency, medrxiv, NVD CVE, openFDA recalls, Rosetta Code, Stack Exchange, UK written questions, Zenodo.
   - **Also forbidden:** anything used as a dev or eval set here (ag_news, emotion, CLINC150 and Banking77 test
     splits, BTZSC sets, and JevBench items).
2. **Provenance.** Human-written texts and human labels only. No LLM-written or LLM-labelled data. Exception:
   program-generated rows whose label follows by construction (see "Generators").
3. **Licence.**
   - **Allowed:** CC0, public domain or US government, CC BY, CC BY-SA, MIT, Apache-2.0, BSD, ODC-BY or ODbL, stated
     in a file or official record you cite (quote the path or URL in meta.licence).
   - **Rejected:** NC, ND, research-only, "see paper", unknown, or stated only by a third-party mirror.
4. **Train split only.** Never test, and never a validation split that serves as the benchmark test. A dataset with
   no splits counts as train.
5. **No model calls.** Claude writes only definitions, questions, templates and generators. Never label with a model.
6. **Pin everything.** Record the HF revision or git commit, the sha256 of the downloaded files, and a fixed seed. The
   builder must be deterministic and CPU-only.

## Output format (identical to the v0.13 breadth raw format)

**Builder location:** `golden_src/<family>/build_<key>.py`. Look at `breadth_src/build_abcd.py` and
`breadth_src/build_emobank.py` for style.

**Row output:** `data/v14_parts/raw/<key>.jsonl`, one JSON object per row:

```
{"key": "<key>", "rid": "<stable source record id>", "state": "<the text the decision is about>",
 "instructions": "<the question, one sentence, self-contained>",
 "options": ["<option>", ...],   # for yes/no use exactly ["yes", "no"]
 "gold": "<one of options>",
 "soft": {"<option>": p, ...} or null,   # only real annotator vote shares (they sum to 1)
 "meta": {"dataset": "<hf id or url>", "config": "...", "revision": "<commit>", "licence": "<licence + where stated>",
          "split": "train", "orig_label": <original label>, "family": "<family>", "edge": "<edge-case tag or null>"}}
```

**Definitions output:** `data/v14_parts/defs/<key>.json`, `{"<option>": "<definition>"}` for every option the key
uses. For yes/no keys whose meaning differs by question, the key may use several option sets. In that case write
`defs/<key>__<qid>.json` and put `"defs": "<qid>"` in meta.

## Definition quality (the card the model reads)
- One precise sentence per option (at most about 40 words), mutually exclusive, and stating the decision rule
  exactly as the annotators applied it. Include the tricky boundary, for example "sarcasm counts as negative only
  when...".
- For yes/no, say what yes means **and** what no means (including "not enough information", when that maps to no).

## Size, balance, edge cases
- Each dataset gives **1,000-8,000 rows** (fewer only if the dataset is small). Cap any class at about 50% of a
  dataset's rows unless the label set is yes/no; for yes/no keep yes between 35% and 65%.
- Prefer datasets with real-world decisions, many label sets, annotator distributions (soft), or rows that
  exercise edge cases.
- Tag edge cases in meta.edge: `negation`, `double_negation`, `exception`, `missing_info`, `conflicting_evidence`,
  `temporal`, `numeric`, `units`, `quantifier`, `hypothetical`, `reported_speech`, `sarcasm`, `implicit`,
  `long_context`, `table`, `multi_hop`, `ambiguous`.
- One source record gives one row per question type. Never duplicate texts. Dedupe exact and near-exact states
  within the dataset.

## After building each dataset
1. Run the builder. Check the row count, the option balance and that there are no empty or duplicate states.
2. Print 5 random rows and read them. The gold label must be clearly right given the definitions.
3. Append a record to `golden_src/MANIFEST.jsonl`:
   `{"key", "family", "dataset", "licence", "rows", "qtype", "yesno_share", "edge_tags", "notes"}`.
4. Never touch files outside `golden_src/` and `data/v14_parts/`.

## Generators (program-generated, exact labels)
- **Location:** `golden_src/gen/gen_<name>.py`, writing `data/v14_parts/raw/gen_<name>.jsonl` and its defs.
- **Labels follow from construction.** For example: generate a table, then compute whether a claim holds.
- **Surface variety:** Claude-written templates, varied surface forms, realistic domains (HR policy, refunds,
  insurance, shipping, pharmacy, travel, grants, school rules, sports stats, finance), and many edge cases
  (exceptions, "unless", thresholds at the boundary, dates and time zones, leap years, units, rounding, negation,
  double negation, quantifiers such as all, some, none, at least, exactly, missing information, conflicting
  sources).
- **Fact-flip twins:** also emit a twin that changes one decisive fact so the gold label changes. Link it with
  `meta.twin_of` = rid.
