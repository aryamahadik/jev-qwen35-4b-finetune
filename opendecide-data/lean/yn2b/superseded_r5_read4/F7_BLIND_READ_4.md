# F7 blind read 4 (checklist section 4, item 11, fresh sample on the rebuilt fix2 F7 part)

**Result of read 4: PASS.**
- Wrong gold: 0 of 300 rows. The bar is 0.
- Ambiguous: 2 of 300 rows (0.67%). Unreadable: 0. Together 0.67%; the bar is at most 3%.
- Agreement with gold: 300 of 300 (100%), including both ambiguous rows.
- `yn2b/f7_precheck.py --only 11` on the fix2 inputs with this verdict file: **11.1 PASS**
  (rows 300, ok 298, ambiguous 2, bad_share 0.0067, no MUST item short).

Date: 2 Oct 2026. CPU only. No model, no network, no Modal or gcloud, no OHS-3 file. No data file or code was edited.

## 1. Method

**Who read.** A new agent that had not seen F7 before. Before the answers were frozen it did **not** open:
the generator (`golden_src/gen3/`), decide2, `yn2b/f7_fix2_drops.json`, `yn2b/f7_source_label_audit.json`, any earlier
`F7_BLIND_READ*.md`, any earlier verdict or answer file, any `*_meta.jsonl`, the train row `meta` field, or the hidden
gold file. Of the checklist it read item 11 of section 4 only. It did read the source of the sampler and of
`yn2b/f7_blind_read_compare.py` (no gold in either) to learn the answer format.

**Sample.** `yn2b/f7_blind_read_sample4.py`, default seed 20261042, on
`data/v14_parts/f7fix2_train.jsonl`, sha256 `018798bce6d804872fd1e6fdbcd400d8f6ac71ffe4d44222de16399f9de45d8f`
(12,588 rows), plus `data/v14_parts/f7_probe.jsonl`. Rows and ladders of reads 1-3 and pair `f7v2-tr-00001` were
excluded by the sampler. It drew 300 rows from 281 ladders:
- 10 rows for each of the 18 MUST items (1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15, 16, 21, 22, 24, 27, 36): 180 rows;
- 100 random train rows;
- 20 probe rows (13 holdout, 7 iid).

**Blinding.**
- The batches showed card, state, question and options only. All 300 rows were answered in 15 batches of 20.
- Each answer has a flag (ok / ambiguous / unreadable) and, where useful, a reason, written before any gold was seen.
- The answer file was frozen (read-only) before the comparison: `yn2b/f7_blind_read_4_answers.tsv`, sha256
  `9c333a3f75a62bd974407506e32400068faa27020271ed751a535d01dbf7de0f` (byte-identical to the scratch `answers.tsv`).
- Yes/no answers are 1 = yes, 0 = no; choice answers are the option index.

**Comparison.** `yn2b/f7_blind_read_compare.py` reported 300/300 agree. That script looks rows up in
`data/v14_parts/f7_train.jsonl`, not in `f7fix2_train.jsonl`, so the answers were also checked directly against
`f7fix2_train.jsonl` and `f7_probe.jsonl`: 300/300 agree. The 280 sampled train rows are byte-identical in both
train files, and the hidden gold equals the file gold on all 300 rows.

## 2. Numbers

| Group | Rows | Agree with gold | ok | Ambiguous | Unreadable | Wrong gold |
|---|---|---|---|---|---|---|
| MUST items (10 each, 18 items) | 180 | 180 | 178 | 2 (items 10 and 22) | 0 | 0 |
| Random train | 100 | 100 | 100 | 0 | 0 | 0 |
| Probe (13 holdout, 7 iid) | 20 | 20 | 20 | 0 | 0 | 0 |
| **Total** | **300** | **300 (100%)** | **298** | **2 (0.67%)** | **0** | **0** |

Verdict file for `f7_precheck.py --blind-read`: `yn2b/f7_blind_read_4_verdicts.json`, sha256
`944a3b4f087c7064ed067ba66641a6c6feabcaa3116fce12baec03dcaa34b756` (300 entries: id, verdict, tag, split, answer,
gold, agree, reader flag and note, `derived_from`, adjudication; same fields as read 3).

## 3. Wrong gold

None. There were no disagreements, so no row needed a negation-program, source-label or card-wording judgement.

## 4. Ambiguous (2 rows)

Both were flagged before gold was seen. In both, the gold matches the reader's leaning, so neither is wrong gold.
Both causes are the **source text's label vs the card wording**, not the negation logic.

| Row | Source row | Two readings |
|---|---|---|
| `r_f7nn2_f7v2_tr_01540a_2` (MUST 10) | `r_gd_ncbi_disease_2802` | 'thymic lymphoma': 'specific disease' (source label) or 'disease class', since the card's class line allows a general head word such as tumour or cancer. |
| `r_f7nn2_f7v2_tr_01590a_2` (MUST 22) | `r_gd_drugprot_1488` | AMPH and DAT: 'substrate' (source label; the sentence calls AMPH a DAT substrate) or 'inhibitor' ("thereby reducing transport capacity" fits the card's inhibitor line). |

## 5. Rows read as ok with a note

These were judged readable with one clear best reading. The gold agreed in each case.
- `r_f7nn2_f7v2_tr_02863a_1`: an NOL carryforward passage. Read as Item 8 (notes on taxes); an MD&A source was
  possible. Source label: Item 8.
- `r_f7nn2_f7v2_ho_00212a_0` (probe): the victim saw a doctor, with no ER mentioned, so 'middling'. Source label: middling.
- `r_f7nn2_f7v2_ho_00036a_4` (probe): a toenail "needed medical attention", with no ER mentioned, so 'middling'. Source
  label: middling.
- `r_f7nn2_f7v2_ho_00119a_1` (probe): post 3 (decimal separators) may or may not be a Language desk post; the count is 1
  or 2, so "no more than two" holds either way.

## 6. What this means for checklist item 11.1

Read 4 meets the bar: 0 wrong gold and 0.67% ambiguous plus unreadable. It was done by a new agent on the rebuilt fix2
F7 part (sha256 above) that read 3 asked for. Item 11.1 is **PASS** on that file.
