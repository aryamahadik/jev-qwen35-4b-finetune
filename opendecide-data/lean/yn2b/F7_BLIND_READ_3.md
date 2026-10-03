# F7 blind read 3 (checklist section 4, item 11, fresh sample on the fix2 F7 part) and the source-label audit

**Result of read 3: FAIL.**
- Wrong gold: 4 of 300 rows. The bar is 0.
- Ambiguous: 5 of 300 rows (1.67%). The bar is at most 3%, so this part passes.
- Unreadable: 0.
- Agreement with gold: 292 of 300 (97.3%).

All 9 non-ok rows trace to the **human label of the source text** (NHTSA, DrugProt, San Diego 311, EDGAR, MedQuAD and
one probe row from wiki help-desk routing). The negation program was right in all 300 rows: 0 program errors.

Read 1 failed on card lines and source labels (fixed in F7 v2 r4) and read 2 on 2 source labels (DrugProt and MedQuAD);
neither found a negation-program error either. Dropping only what each read happens to sample does not converge: the
audit below found that 0.7% of the real-text source rows carry a label their text contradicts and 3.9% a label the F7
card leaves open. So after this read **every real-text
source row behind the fix2 F7 part was audited** (section 5), every flagged row was dropped, and F7 was repaired to
r5 so that it still meets the whole checklist (section 6).

**What this means for checklist item 11.1:** it stays **PENDING**. A fourth blind read, by a **new agent**, on the
rebuilt file must pass before amendment A8-prime can say "every §4 check is PASS" (section 7).

Date: 2 Oct 2026. CPU only. No model, no network, no ohs3 file and no Jev output was used.

## 1. Method

**Who read.** The agent that assembled fix2 (`extra/build_fix2.py`). This is weaker than reads 1 and 2 on independence,
and it is why read 4 must be done by a new agent:
- Before answering it had worked with F7's sidecar meta (`latent_id`, `derived_from`, `text_gold`) for the drop logic
  and had run `yn2b/f7_precheck.py`, but it had not seen the gold of any of the 300 sampled rows.
- It had seen two rows of ladder pair `f7v2-tr-00001` with gold; that pair was excluded from the sample.
- It did not run decide2 for this read.

**Sample.** `yn2b/f7_blind_read_sample3.py`, seed 20261022, on the fix2 F7 part as it was built before this read:
`data/v14_parts/f7fix2_train.jsonl` sha256 `d8f892291749bb2bbfe9b867f6ff807f43ae9afa8041296ec8ba7f83ddff9123`
(12,436 rows; that file has since been rebuilt, section 6). It drew:
- 10 rows for each of the 18 MUST items (1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15, 16, 21, 22, 24, 27, 36): 180 rows,
  picked by the sidecar `phen` field only;
- 100 random train rows, no overlap with the MUST rows;
- 20 random rows of `data/f7_probe.jsonl`.

**Fresh.** Every row id and every ladder (`call_id`) of read 1 and read 2 was excluded, and so was pair `f7v2-tr-00001`.

**Blinding.**
- The batches showed the card, state, question and options only. Gold sat in a separate hidden file.
- All 300 rows were answered in 15 batches of 20. Each answer has a flag (ok / amb / unr) and a reason, written before
  any gold was seen.
- The answer file was frozen before the comparison: `yn2b/f7_blind_read_3_answers.tsv`, sha256
  `a4aa5935b8f8b648818465bd0242d399f7b2b9426d83cdadc4f76c2f70c13c06`, equals the scratch `answers_preGold.tsv` byte
  for byte.
- The comparison mapped choice answers to option strings, as `yn2b/f7_blind_read_compare.py` does. The source rows were
  read only after the comparison, to judge the disagreements.

## 2. Numbers

| Group | Rows | Agree with gold | Disagree |
|---|---|---|---|
| MUST items (10 each) | 180 | 176 | 4 (items 3, 4, and 22 twice) |
| Random train | 100 | 97 | 3 |
| Probe | 20 | 19 | 1 |
| **Total** | **300** | **292 (97.3%)** | **8** |

| Verdict | Rows |
|---|---|
| ok | 291 |
| Wrong gold | 4 (3 disagreements + 1 row that agreed only by elimination, flagged "amb" before gold) |
| Ambiguous (two reasonable readings) | 5 |
| Reader error, gold defensible | 0 |

Verdict file for `f7_precheck.py --blind-read`: `yn2b/f7_blind_read_3_verdicts.json` (300 entries: id, verdict, answer,
gold, the reader's flag and note, `derived_from`, adjudication). On the file it was drawn from, 11.1 is **FAIL**
(wrong_gold 4, bad share 5/300 = 0.0167).

## 3. Wrong gold (4 rows)

| Row | Source row | What the text says |
|---|---|---|
| `r_f7nn2_f7v2_tr_01788b_1` (MUST 3) | `r_gd_nhtsa_complaints_3140` | Fire flag set, but the narrative says there was no fire; smoke only. The card makes that a smoke-only case. |
| `r_f7nn2_f7v2_tr_00142b_1` (MUST 22) | `r_gd_drugprot_6076` | 'antagonist' of the NMDA receptor, but the sentence calls CNQX a **non**-NMDA receptor antagonist. |
| `r_f7nn2_f7v2_tr_02581a_0` (random) | `r_gd_drugprot_1558` | 'activator', but the monohydroxy metabolite is a product of CYP3A4 hydroxylation, not an activator. |
| `r_f7nn2_f7v2_tr_01943a_3` (MUST 36) | `r_gd_nhtsa_complaints_3469` (complaint 3 of a multi-text batch) | Fire flag set; the complaint shows smoke, a fuel smell and an extinguisher, no flames. By the card all three statements hold, so the row has no false option; the reader's answer matched gold only by elimination. |

## 4. Ambiguous (5 rows)

| Row | Source row | Two readings |
|---|---|---|
| `r_f7nn2_f7v2_tr_02752a_3` (MUST 4) | `r_gd_sd311_routing_1561` | A boat left on the street: 'illegal dumping' (gold) or 'parking violation'. |
| `r_f7nn2_f7v2_tr_00828b_2` (MUST 22) | `r_gd_edgar_10k_item_170` | A business-segment description: Item 1 by the card, or the Item 8 segment note ("see Note 19"). |
| `r_f7nn2_f7v2_tr_00828b_0` (random) | `r_gd_edgar_10k_item_170` | Same source row. |
| `r_f7nn2_f7v2_tr_02664a_4` (random) | `r_gd_medquad_qtype_3649` | 'treatment options' on a passage about program records and patient privacy. |
| `r_f7nn2_f7v2_ho_00368a_4` (probe) | `raw:wiki_help_routing:a78a1628fda42b8a` | Science vs Humanities desk for a medical-statistics question. The probe is frozen, so this is report only. |

## 5. The source-label audit (every real-text source row behind the fix2 F7 part)

**Round 1** read every source row of the pre-audit fix2 F7 part (F7 v2 r4 minus the 3 blind-read-2 pairs and the 12
probe-12-gram pairs: the file read 3 sampled).

File: `yn2b/f7_source_label_audit.json` (one entry per flagged row: id, source label, verdict, reason; plus the rows
audited and the method per source). Each label was checked against the **F7 card** the ladder shows, not against the
original dataset's guidelines, because the card is what a reader (and the model) sees.

| Source | Rows audited | Method | Wrong gold | Ambiguous |
|---|---|---|---|---|
| NHTSA complaints (fire / crash / injury) | 897 | Two program screens (labels vs strong-evidence patterns; every negative label with a related word), then all 365 flagged rows read by hand | 2 | 3 |
| Storm Data (EF rating) | 314 | Program: the highest wind speed the text states falls in the gold rating's band, 314 / 314 | 0 | 0 |
| SMCalFlow (user action) | 274 | All read by hand | 7 | 33 |
| OIICS (fall to a lower level / struck by an object) | 196 | All read by hand, per the property the batch uses | 0 | 7 |
| San Diego 311 routing | 144 | All read by hand against the 25-option card | 0 | 8 |
| MedQuAD question type | 148 | All read by hand | 1 | 1 |
| DrugProt relation | 136 | All read by hand | 6 | 8 |
| EDGAR 10-K item | 120 | All read by hand | 0 | 11 |
| NCBI disease mention class | 102 | All read by hand | 0 | 3 |
| FaithDial faithfulness | 30 | All read by hand (full responses) | 1 | 4 |
| MultiWOZ (match found / dead end) | 18 | All read by hand | 0 | 0 |
| **Total** | **2,379** | | **17** | **78** |

- Round 1 flagged 95 source rows (4.0%).
- **Rounds 2-5** read every source row of the pairs that the F7 r5 repair (section 6) newly selected and that no
  earlier round had read: 205 rows in round 2 (22 flagged: 1 wrong, 21 ambiguous; DrugProt 6, EDGAR 6, San Diego
  311 3, SMCalFlow 3, OIICS 2, MedQuAD 1, FaithDial 1), 18 in round 3 (2 ambiguous: EDGAR 1, MultiWOZ 1), 4 in
  round 4 (0 flagged) and 2 in round 5 (1 ambiguous, DrugProt). Storm and NHTSA rows were checked with the round-1
  programs; every other row was read by hand. (One repair pass drew 130 other unread rows; that pass was not used,
  so they were not read.) The repair writes only when every source row of every new pair has been read.
- **In all: 2,608 source rows read, 120 flagged (18 wrong gold, 102 ambiguous).** With the 3 rows of blind read 2,
  `yn2b/f7_fix2_drops.json` lists 123 source rows. Every flagged row and its reason is in
  `yn2b/f7_source_label_audit.json`.
- The SMCalFlow count is high because the F7 card is simpler than the source's own label set: the card's 'create a new
  event' says "fully specified", and it has no line for the source's decline labels (unnamed attendees, conference
  rooms, multi-day spans, past periods) or for 'ask the user to be more specific'. Rows whose source label depends on
  one of those distinctions were flagged.
- F7 rows with no source text (program-written states: 4,584 of r5's 12,588 train rows) need no label audit: their
  gold is the program's.
- **The probe's own source rows were audited too (2 Oct, after the fixer review):** all 464 real-text source rows
  behind the probe (`raw:` / `old:` ids, none shared with train), each against the probe's own F7 card: 5 wrong gold,
  41 ambiguous (`yn2b/f7_source_label_audit.json` key `probe`). The probe is not edited for them: the 45 probe
  ladders built from a flagged row are listed in `yn2b/f7_fix2_drops.json` (`probe_report_only`), and step 0a freezes
  their rows into `gate/fix2_pairs.json` as the accuracy-exclusion list that step P applies (A8-prime C.8, F.P); the
  aff/dneg flip counts keep every frozen pair (flips do not use gold). (An earlier version of this note said the
  probe was not audited and that one ambiguous gold affects both models equally; that was wrong: when the two
  models answer a row differently, the gold decides which one gets the credit.)
- **F7 v2 r6** (`golden_src/gen3/f7_repair_r6.py`, the fixer review) adds 18 train pairs. Every unread source row of
  the pairs its passes selected was audited in two more rounds (rounds 6-7: 80 rows, 3 flagged: 1 wrong, 2
  ambiguous); the repair then ran again without the 2 pairs built from them, and the final 18 pairs hold 0 unread
  source rows.

## 6. What changed in F7 and fix2

**Dropping alone was not enough.** The first rebuild of fix2 with the round-1 rows dropped removed 103 F7 pairs (1,028
rows) and left the F7 part below six checklist bars: item floors 24 / 28 / 30 / 32 (376, 142, 142, 136 train rows),
the card-ladder share (49.6%), the odd-parity share of the lexeme "no exactly when" (60.6%), the distractor share of
"leave out" and "decline" (8.7%, 9.5%) and the instruction word "stamp" (60.9% odd). So F7 was repaired, not just cut.

**F7 v2 r5** (`golden_src/gen3/f7_repair_r5.py`; r4 kept in `data/v14_parts/f7_v2_r4_backup/` with r4's decide2 and
precheck outputs):
1. The generator's r4 candidate pool (2,898 train, 540 iid, 585 holdout candidate pairs) is rebuilt with r4's seed and
   `PYTHONHASHSEED=0`. It rebuilds r4's six data files byte for byte (checked), so every candidate is exactly r4's text
   and label.
2. The probe keeps r4's selection: after the write its three files are byte-identical to r4's (checked).
3. Train starts from r4's selection. Every candidate that extra/build_fix2.py would drop is forbidden: 126 candidates
   (reasons: a derived source row in the drop list 113, a probe-12-gram hit 13, a listed pair 3; one candidate can
   have more than one). 103 of them are r4 pairs, which go. The vacancies are
   filled one pair at a time by the generator's own Objective (hard limits first; a source row the audit has not read
   costs one unit of hard penalty, so already-read texts are preferred). The fill ends at hard penalty 0.
4. The generator's audit (`yn2b/f7_precheck.py` as a library, full surface probes, devx included) then failed one
   cross-validated surface probe, 5.f (per-lexeme majority: 61.8% in the stratum frame_id = dir5, bar 60%). One swap of
   a new pair in that stratum for a spare whose texts were already read (`f7v2-tr-00095` -> `f7v2-tr-02423`) fixed it;
   the audit then reports no failing check.
5. Every source row of every new pair was read before the write (rounds 2-5 of section 5); the repair refuses to write
   otherwise.

| | r4 | r5 |
|---|---|---|
| Train pairs / rows | 1,260 / 12,586 | 1,260 / 12,588 |
| Pairs replaced | | 103 |
| Card / record / multi-text pairs | | 634 / 459 / 167 (card share 50.3%) |
| Items 24 / 28 / 30 / 32 (train rows) | | 426 / 160 / 168 / 164 (floors 400 / 150 / 150 / 150) |
| Distinct real-text source rows | | 2,294, all read by the audit, 0 flagged |
| Probe files | | byte-identical |
| `f7_train.jsonl` sha256 | `6e560988…` | `018798bce6d804872fd1e6fdbcd400d8f6ac71ffe4d44222de16399f9de45d8f` |

**fix2 rebuilt on r5** (`extra/build_fix2.py --overwrite`, F7 inputs re-pinned to r5):
- F7 pairs the builder had to drop: 0 (the builder now stops if any F7 pair would have to go: `ALLOW_F7_DROPS`). The
  fix2 F7 part is r5's whole train part: 12,588 rows in 2,520 ladders (`data/v14_parts/f7fix2_train.jsonl` sha256
  `018798bce6d804872fd1e6fdbcd400d8f6ac71ffe4d44222de16399f9de45d8f`, the same bytes as r5's `f7_train.jsonl`).
- The mix: 46,218 rows = replay 32,356 (0.7001) + F7 12,588 + F4 908 + golden double-negation units 366; 11,381
  relations; `fix2_train.jsonl` sha256 `61109ce27c33ec5e75e83425e246766851b87506ce6a2282e28196d646879b83`.
- Precheck of that F7 part (`yn2b/f7_precheck_fix2.json`): PASS 111, PENDING 2: 8.13 (the owner's OHS-3 count) and
  11.1 (blind read 4). The full-F7 precheck (`yn2b/f7_precheck.json`, r5 train + probe + devx) gives the same.
- decide2 (independent) agrees on every row: train 12,588 / 12,588, probe 2,498 / 2,498, devx 220 / 220.

## 7. What must happen before 11.1 can pass

1. **Blind read 4 by a NEW agent** (never the fix2 assembler), on the rebuilt `data/v14_parts/f7fix2_train.jsonl`:
   - `python yn2b/f7_blind_read_sample4.py --out <its own scratch>/blind4` (seed 20261042; excludes every id and ladder
     of reads 1-3 and pair `f7v2-tr-00001`; prints the train file's sha256);
   - the reader must not open the generator, decide2, `yn2b/f7_fix2_drops.json`, `yn2b/f7_source_label_audit.json` or
     any gold before its answers are frozen;
   - compare with `python yn2b/f7_blind_read_compare.py --dir <its scratch>/blind4`, then
     `python yn2b/f7_precheck.py --train data/v14_parts/f7fix2_train.jsonl ... --blind-read <verdicts> --only 11`.
   - Bar: 0 wrong gold, unreadable + ambiguous at most 3%.
2. Only a PASS lets A8-prime C.3 say "every §4 check is PASS". If read 4 fails again, the fix2 data is not final and
   the top-up is not launched.

## 8. Outside F7 (owner decision)

The flagged source rows are also in `golden_train.jsonl` (C1's training data) and the sets built from it. fix2's replay
drops every golden unit that holds one of them, but `golden_train.jsonl` itself is not edited here.

## Files

- Sampler: `yn2b/f7_blind_read_sample3.py` (seed 20261022); next read: `yn2b/f7_blind_read_sample4.py`
- F7 repair: `golden_src/gen3/f7_repair_r5.py` (r4 kept in `data/v14_parts/f7_v2_r4_backup/`)
- Answers, frozen before gold: `yn2b/f7_blind_read_3_answers.tsv`
- Verdicts: `yn2b/f7_blind_read_3_verdicts.json`
- Source-label audit: `yn2b/f7_source_label_audit.json`
- Drop list used by the builder: `yn2b/f7_fix2_drops.json`
