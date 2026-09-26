# build/loaders: the source-loader contract

Each source loader turns one pinned source into **normalised records**. `s02_normalise` runs every registered
loader once per split and writes `data/interim/normalised/<source>__<split>.jsonl` plus
`data/reports/normalise_summary.json`. The reference example is `intent_banking77.py`.

## Adding a loader (no shared file needs editing)

1. Make sure the source is pinned in `build/config.yaml` under `sources:` (repo, `revision` full sha or prefix,
   `config` / `data_dir` / `data_files` / `streaming`, `files`, licence and release tier). If it is not, add the
   entry there, run `python3 build/build.py --stage lock`, and check that `build/sources.lock.json` shows it as
   `resolved`.
2. Create `build/loaders/<family>_<source>.py` (any name that does not start with `_`). Every module in this
   folder is imported automatically, sorted by name.
3. Decorate a generator:

```python
from loaders import register, LoaderContext
import common

@register("clinc150", splits=("train", "validation", "test"), lock_key="clinc150", wrapper="clinc150")
def load_clinc150(split: str, ctx: LoaderContext):
    ds = ctx.load_hf(split=split)                 # load_dataset(repo, config, revision=<locked sha>, ...)
    names = ds.features["intent"].names
    for i, row in enumerate(ds):
        text, n_pii = ctx.clean(row["text"])      # CRLF->LF, strip, e-mail/phone masking
        if not text:
            ctx.drop("empty_text"); continue
        yield common.make_record("clinc150", split, i, text, label=names[row["intent"]],
                                 meta={"pii_masked": n_pii} if n_pii else {})
```

4. Run it alone: `python3 build/steps/s02_normalise.py --sources clinc150` (the venv python is used by the
   driver; `.venv/bin/python` works directly too).

`register(source, splits, *, lock_key=None, **info)`:
- `source`: lower-case `[a-z][a-z0-9_]*`, unique across the registry. It becomes the file name and `record.source`.
  One pin can feed several loaders (e.g. `hint3_sofmattress` and `hint3_curekart` both use `lock_key="hint3"`;
  `becel_boolq` and `becel_snli` both use `lock_key="becel"`).
- `splits`: every split name the loader emits. Use the source's native names (`train`, `validation`, `test`, …).
  When the spec regroups a source (Drug: pool train+test, group by normalised text, 80/10/10 by hash) the loader
  emits the regrouped names (`train`, `dev`, `eval`) and says so in its docstring.
- `lock_key`: the `config.yaml` `sources:` key holding the pin (default: `source`).
- `**info`: free-form metadata copied into the normalise summary (e.g. `wrapper=`, `task_family=`).

## The record contract

Exactly seven fields; `common.validate_record` enforces them and `s02` fails on any violation.

| Field | Type | Rule |
|---|---|---|
| `source` | str | the registered name |
| `split` | str | one of the loader's declared splits |
| `source_id` | str | stable id **within (source, split)** at the pinned revision; `[A-Za-z0-9][A-Za-z0-9_.-]*` (no `:`, `#`, `/`, whitespace, because ids are joined into `group_id` and `key`). Use the upstream id when there is one (GoEmotions `id`, CondaQA `PassageID.QuestionID.edit`), else the row index in the pinned split. Compose multi-part ids with `.` (e.g. `banking.fold3.17`). |
| `text` | str | the raw base text that becomes the **state body** after hygiene (premise for NLI, passage for BoolQ/CondaQA, evidence for VitaminC, review for reviews). Non-empty. |
| `label` | str \| int \| list[str] \| None | the source's own gold in its own label space: ClassLabel **name** or raw id as str; ordinal ratings/levels as int; multi-label as a **sorted, unique** list of str; `None` when the source has no gold (filler corpora, injection pools). Never a Choice key or a derived Noul gold; those are made at render. |
| `soft` | None \| float \| list[float] \| dict[str, float] | soft labels where the source has them (GoEmotions vote fractions, civil toxicity fraction, MHS annotator distribution, BoolQ-NP `soft_label`, SST continuous value). Values in [0, 1]; a list is a distribution over ordered levels and must sum to 1 ± 1e-6; a dict is per-label fractions (set `meta.soft_kind = "distribution"` if it must sum to 1). |
| `meta` | dict | everything else, JSON-serialisable (no NaN/inf). |

### What goes in `meta`
- **Everything a DESIGN 3.5 wrapper or a later rule needs**, under these names:
  `title` (BoolQ, DBpedia), `condition` (Drug), `bot` and `bot_domain` (HINT3), `domain` (NLU++ banking/hotels),
  `target` (SuperTweetEval), `platform` (MHS; `twitter` rows become idonly), `hypothesis` (NLI; `text` is the
  premise), `question` (BoolQ, CondaQA), `claim` and `case_id` / `revision_type` (VitaminC), `rating`,
  `n_raters` / `votes` (soft sources), `group` (the dedup/leakage group key of 9.1 step 3: BoolQ passage,
  CondaQA PassageID, VitaminC case_id, MNLI promptID, Drug normalised text), `slots` (NLU++), `label_index` etc.
- Hygiene accounting: `pii_masked` (count of masks applied to this record's text fields).
- `soft_kind` when relevant (`"distribution"` or `"fractions"`).
- **Reserved:** `text_sha256` is added by `s02` (sha256 of `text` after hygiene; used by `rehydrate.py`). Do not set it.

## What loaders do, and what they must not do

Loaders **do** apply step-2 hygiene (DESIGN 8.1, 13 step 2):
- **PII masking**: `ctx.clean(text)` masks e-mails (`<EMAIL>`) and phone numbers (`<PHONE>`), plus any run of
  ≥ 10 digits. HINT3 passes `digit_run_min=7` (DESIGN 3.3). Apply it to every text field that can reach a state
  or a question (e.g. also `meta.hypothesis`). Fresh items are not loaded here.
- **HTML unescape** where the source is escaped: `ctx.clean(text, html_entities=True)` (Drug reviews).
- **Regrouping** where the spec says so (Drug). Use `common.stable_hash` / `common.sub_seed`, never unseeded
  randomness.
- **Dropping invalid labels** (label −1, missing, outside the label set): `ctx.drop("invalid_label")`, then skip.
  Every other drop also goes through `ctx.drop(reason)` so the summary can report it.
- **Soft-label extraction** into `soft` (and the raw counts into `meta`).

Loaders **do not**:
- apply wrappers (render does, from `config.yaml: wrappers`), sample, rank, deduplicate across sources, drop
  near-duplicates, cap lengths, or assign train/dev/eval (steps 3, 4, 6, 7);
- read any `assets/` authored content (label keys, wording banks, fresh items) — loaders are source-only;
- use a model of any kind (R1);
- download outside the HF cache: use `ctx.load_hf(...)` (HF datasets, at the locked sha) or `ctx.github_file(path)`
  (raw GitHub at the locked commit, cached under `$HF_HOME/opendecide/github/`, sha256-checked against the lock).

## Size and memory
`s02` holds one split in memory to sort it (by `source_id`, natural order). Each process should stay under
~2 GB: for very large or streamed corpora (civil_comments, Simple Wikipedia, gutenberg, gliclass-v2.0,
wikitext-103) stream and pre-filter inside the loader (e.g. civil_comments rows with ≥ 3 raters and ≤ 200 tokens;
wikitext paragraphs of 40–300 words) and document the filter in the loader docstring. Contamination corpora are
hashed by `s03_index`, not normalised.

## Determinism
Output must depend only on the pinned source bytes and the master seed. Iterate the dataset in its stored order,
never over a `set`, and let `s02` do the sorting and writing.
