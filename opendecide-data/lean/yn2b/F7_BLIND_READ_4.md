# F7 blind read 4 on F7 v2 r6 (checklist section 4, item 11; RUNBOOK_fix2 section 1)

**Result of read 4: PASS.**
- Wrong gold: 0 of 300 rows. The bar is 0.
- Ambiguous: 4 of 300 rows (1.33%). Unreadable: 0. Together 1.33%; the bar is at most 3%.
- Agreement with gold: 298 of 300. The 2 rows that disagree were both flagged ambiguous before any gold was seen.
  On re-reading, neither gold is wrong (section 3).
- Probe rows: 20 of 20 agree, none flagged. There is no probe row to report under A8' D.
- `yn2b/f7_precheck.py` on the fix2 inputs with this verdict file: **11.1 PASS**
  (rows 300, ok 296, ambiguous 4, bad_share 0.0133, no MUST item short).
  Overall: PASS 112, PENDING 1 (8.13, the owner's OHS-3 step, PENDING by design), FAIL 0.

Date: 2-3 Oct 2026 (UTC). CPU only. No model, no network, no Modal or gcloud, no OHS-3 file. No data file or code
was edited. This read replaces the r5 read 4 in `yn2b/superseded_r5_read4/`.

## 1. Method

**Who read.** A new agent that had not seen F7 before. Before its answers were frozen it did **not** open:
`golden_src/gen3/`, decide2, `yn2b/f7_fix2_drops.json`, `yn2b/f7_source_label_audit.json`, any `F7_BLIND_READ*.md`,
any verdict or answer file, `yn2b/superseded_r5_read4/`, any `*_meta.jsonl`, the train row `meta` field, or the hidden
gold file. Of the checklist it read item 11 of section 4 only. Of the runbook it read section 1 only. To learn the
answer format it read the parser in `yn2b/f7_blind_read_compare.py` and grepped the sampler; neither holds gold.

**Sample.** `yn2b/f7_blind_read_sample4.py --seed 20261052` (the caller's seed for this r6 re-read; the runbook's
20261042 was the superseded r5 read). Train file `data/v14_parts/f7fix2_train.jsonl`, sha256
`ffa5cecacde7ed65f0b8a105784eae3fae62007650eefd7aff7d8df5197b601c` (12,768 rows), plus `data/v14_parts/f7_probe.jsonl`
(sha256 `e715fbd0...0710`). The sampler printed `prev_ids 1120 prev_calls 648`: rows and ladders of earlier reads were
left out. It drew 300 rows from 284 ladders:
- 10 rows for each of the 18 MUST items (1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15, 16, 21, 22, 24, 27, 36): 180 rows;
- 100 random train rows;
- 20 probe rows (9 holdout, 11 iid).

**Blinding.**
- The batches showed card, state, question and options only. All 300 rows were answered in 15 batches of 20.
- Each answer has a flag (ok / ambiguous / unreadable) and, where useful, a reason, written before any gold was seen.
- The answer file was frozen (read-only) before the comparison: `yn2b/f7_blind_read_4_answers.tsv`, sha256
  `20abe3bccb1e17bad55aabe369551864a6ea46f1b09ff3ae6bbf828975feb424` (byte-identical to the scratch `answers.tsv`).
- Yes/no answers are 1 = yes, 0 = no. Choice answers are the option index.

**Comparison.** `yn2b/f7_blind_read_compare.py` reported 298/300 agree. That script looks rows up in
`data/v14_parts/f7_train.jsonl`, not in `f7fix2_train.jsonl`. The two files have the same sha256 (`ffa5ceca...`), so the
answers were also checked directly against `f7fix2_train.jsonl` and `f7_probe.jsonl`. The result was the same: 298/300.
`data/f7_probe.jsonl` and `data/v14_parts/f7_probe.jsonl` are identical (same sha256). The hidden gold equals the file
gold on all 300 rows.

## 2. Numbers

| group | rows | agree | ok | ambiguous | unreadable | wrong gold |
|---|---|---|---|---|---|---|
| MUST (18 items x 10) | 180 | 178 | 177 | 3 | 0 | 0 |
| random train | 100 | 100 | 99 | 1 | 0 | 0 |
| probe (9 holdout, 11 iid) | 20 | 20 | 20 | 0 | 0 | 0 |
| **all** | **300** | **298** | **296** | **4 (1.33%)** | **0** | **0** |

Choice rows: 42 (MUST 14 = must36 10 + must3 2 + must5 1 + must12 1; random 23; probe 5). All 42 agree. Yes/no rows:
258, of which 256 agree.

`yn2b/f7_blind_read_4_verdicts.json` has one record per row: id, verdict, tag, split, answer, gold, agree, the reader's
flag and note, `derived_from` (from the row's meta, filled in after the freeze), and an adjudication note.

## 3. Wrong gold

None.

The 2 disagreements, re-read after the freeze:

| id | item | reader | gold | source label | cause | verdict |
|---|---|---|---|---|---|---|
| `r_f7nn2_f7v2_tr_01325b_1` | must10 | 0 | 1 | FaithDial: unfaithful | reader error | ambiguous (frozen flag) |
| `r_f7nn2_f7v2_tr_00906a_1` | must16 | 1 | 0 | DrugProt: substrate | source label needs domain knowledge | ambiguous |

- **01325b_1.** The wizard says "Well he was born in 1958. So not too old!". The snippet gives the birth date. The
  reader called "So not too old!" an aside rather than a claim. But the card says embellished includes "a personal
  feeling given as its own", and the FaithDial label is unfaithful. The gold is defensible and the reader was wrong.
  The negation logic is correct. The row stays ambiguous because the reader flagged it before seeing the gold.
- **00906a_1.** The sentence says "the PDE4B-regulated cyclic adenosine monophosphate signaling pathway". The card
  asks whether no line among activator / part of / substrate fits. The gold says one fits (substrate), which follows
  the DrugProt human label: PDE4B is the phosphodiesterase that breaks down cAMP. The sentence itself only says
  "regulated", so you need domain knowledge to get "substrate". This is the source label against a sentence-only
  reading, which the card's "the sentence settles every claim" invites. It is not a negation bug and not a wrong gold.

## 4. Ambiguous (4 rows)

| id | item | agree | why it was flagged before gold |
|---|---|---|---|
| `r_f7nn2_f7v2_tr_00691a_3` | must10 | yes | "it's all classified by the different types of fermentation of grains" against the snippet's "unifying characteristics ... are the fermentation of grains": loose paraphrase or distortion (source: FaithDial unfaithful; matches the reader) |
| `r_f7nn2_f7v2_tr_01325b_1` | must10 | no | section 3 |
| `r_f7nn2_f7v2_tr_00906a_1` | must16 | no | section 3 |
| `r_f7nn2_f7v2_tr_01313a_4` | random | yes | a customer "Claim of Non-Conformance" settled by the insurer: Item 3 (not on this card, so "something else") or an Item 8 contingencies note (source: EDGAR Item 3; matches the reader) |

All four come from the source text or its human label: two FaithDial grounded/embellished calls, one DrugProt relation
that needs domain knowledge, and one EDGAR item boundary. None comes from F7's negation program or a card's negation
wording.

## 5. Rows read as ok with a note

- `r_f7nn2_f7v2_tr_01081a_2` (must13): Complaint 2 says in passing that "a deer hit the car" (the complaint is about a
  power-steering recall). By the card's literal definition that is a collision, giving 3 crashes and the answer yes.
  The gold agrees.
- Other rows the reader thought about, all agreeing with gold:
  - `00998a_4`: a heated seat burned a hole, with no flames, read as smoke-only;
  - `02877a_1`: alanine-substituted SRIF-14 analogs, read as part of;
  - `00369b_3`: rhArg-mediated arginine depletion, read as substrate;
  - `01834b_4`: USO futures roll policy, read as Item 1;
  - `00281b_2`: Whiteland tornado, 140 mph, read as EF3;
  - `00395a_0/1`: "estimated winds of 90 mph", read as EF1.

## 6. What this means for checklist item 11.1

11.1 passes on F7 v2 r6: 0 wrong gold, and unreadable plus ambiguous is 1.33% (at most 3% is allowed). No probe row is
wrong or ambiguous, so nothing is added to `probe_report_only` and step 0a does not need re-running for read 4. The two
FaithDial rows and the DrugProt row show where the remaining noise is: grounded/embellished calls on evaluative asides,
and relation labels that need domain knowledge. They are within the bar. No repair is needed.

Precheck (`yn2b/f7_precheck_fix2.json`, generated 2026-10-03T01:22:40Z, about 183 s): PASS 112, PENDING 1 (8.13 OHS-3
12-gram, owner step), FAIL 0. Every item except 8.13 is PASS, which meets the runbook's pass rule.

## Files

- `yn2b/f7_blind_read_4_answers.tsv`: frozen answers (id, answer, flag, reason), sha256 `20abe3bc...b424`.
- `yn2b/f7_blind_read_4_verdicts.json`: 300 verdict records in the format `f7_precheck.py --blind-read` reads.
- `yn2b/f7_precheck_fix2.json`: the precheck output with this verdict file.
- Scratch (not in the repo): batches, `HIDDEN_gold.json`, `order.json`, `answers.tsv`, `precheck.log`.
