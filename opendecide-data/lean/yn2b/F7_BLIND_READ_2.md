# F7 blind read 2 (checklist section 4, item 11, fresh sample)

**Result: FAIL.**
- Wrong gold: 2 of 300 rows. The bar is 0.
- Ambiguous: 1 of 300 rows (0.3%). The bar is at most 3%, so this part passes.
- Unreadable: 0.
- Agreement with gold: 297 of 300 (99.0%).

The negation logic was right in all 300 rows. Both wrong golds come from the human label of the source text (DrugProt
and MedQuAD), not from the program. Every double and triple negation I worked through came out as the program says.

**Re-runs (CPU only, nothing edited):**
- **decide2** (`golden_src/gen3/v3_nested_negation.py`, run without opening the source):
  - Agreement is 100%: train 12,586 / 12,586, probe 2,498 / 2,498, devx 220 / 220.
  - 0 disagreements and 0 unparsed rows.
  - The new predictions are byte-identical to `yn2b/f7_decide2_preds.jsonl` (sha256 `3acae03b…`).
- **precheck** (`yn2b/f7_precheck.py`, every input passed):
  - 111 PASS, 0 FAIL, 2 PENDING. The pending items are 8.13 (the OHS-3 12-gram count, an owner step) and 11.1 (this
    blind read).
  - Every item status matches the saved `yn2b/f7_precheck.json`, and every input hash is the same.
  - With this read passed in (`--blind-read yn2b/f7_blind_read_2_verdicts.json --only 11`), 11.1 is **FAIL**: ok 297,
    wrong_gold 2, ambiguous 1, bad_share 0.0033, no MUST item short.

Date: 2 Oct 2026. No model, no network, no ohs3 file and no Jev output was used.

## 1. Method

**Who read.** This was read by an agent that did not write F7.
- Before answering, I did not open `gen3_nested_negation.py`, `nn_lexicon.py`, `v3_nested_negation.py` or any decide2
  output.
- After every answer was frozen, I ran decide2 as a black box (`--help`, then a run). I did not read its source.
- To get the verdict-file format, I read only the check-11 function of the precheck (not generator code), also after
  the answers were frozen.

**Sample.** `yn2b/f7_blind_read_sample2.py`, seed 20261012 (read 1 used 20261002). It drew:
- 10 rows for each of the 18 MUST items (1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15, 16, 21, 22, 24, 27, 36): 180 rows,
  picked by the sidecar `phen` field only;
- 100 random rows from `f7_train.jsonl`, with no overlap with the MUST rows;
- 20 random rows from `f7_probe.jsonl`: 12 iid and 8 holdout.

**Fresh.** Every row id and every ladder (`call_id`) from read 1 was excluded.
- Overlap with read 1 is 0 ids and 0 ladders.
- The 300 rows come from 286 ladders.

**devx was not re-read.**
- Read 1 read all 220 devx rows and agreed with all 220.
- `f7_devx.jsonl` last changed at 11:17, before read 1 (13:31). Its sha256 is now `b5579786…`.
- decide2 still agrees on 220 / 220.

**Blinding.**
- The batches showed the card, state, question and options only. Gold sat in a separate hidden file.
- I answered all 300 rows in 15 batches of 20. Each answer has a flag (ok / amb / unr) and a reason, written before I
  saw any gold.
- The answer file was frozen before the comparison: `answers_preGold.tsv` in the scratchpad equals
  `yn2b/f7_blind_read_2_answers.tsv` byte for byte.
- `yn2b/f7_blind_read_compare.py` then compared the answers with gold.
- I looked at the sidecar meta (`lf`, `text_gold`, `derived_from`) and the golden source rows only after the
  comparison, to judge the disagreements.

## 2. Numbers

| Group | Rows | Agree with gold | Disagree |
|---|---|---|---|
| MUST items (10 each) | 180 | 178 | 2 (both item 22) |
| Random train | 100 | 100 | 0 |
| Probe (12 iid, 8 holdout) | 20 | 19 | 1 (iid) |
| **Total** | **300** | **297 (99.0%)** | **3** |

Every MUST item scored 10 / 10 except item 22 (complement or residual labels), which scored 8 / 10.

| Verdict on the 3 disagreements | Rows |
|---|---|
| Wrong gold | 2 |
| Ambiguous (two reasonable readings) | 1 |
| My error, gold defensible | 0 |

**Flags written before gold.**
- I flagged 1 row "amb" before seeing gold: `02499b_1`. On adjudication I counted it as wrong gold (section 3) and did
  not count it twice.
- I also noted low confidence on 4 rows that I flagged "ok":
  - `ii_00247a_4` became the ambiguous row;
  - `02596b_3`, `00599b_2` and `02217b_4` agreed with gold, and I do not count them (section 5).
- Even if all three were counted as ambiguous, the share would be 4/300 = 1.3%, still within 3%.

## 3. Wrong gold (2 rows)

1. **`r_f7nn2_f7v2_tr_02499b_1`** (item 22, rung N2, ladder `f7v2-tr-02499b`).
   - Source: DrugProt `r_gd_drugprot_4478`, `text_gold` = 'part of'.
   - The sentence: "Diphtheria toxin consists of three domains: an enzymatically active <e2>ADP ribosyltransferase
     domain</e2>, a hydrophobic transmembrane domain, and a <e1>C</e1>-terminal receptor-binding domain."
   - The card lists activator, substrate and 'part of', plus a 'something else' line. 'part of' means "a building
     block inside the protein itself".
   - The sentence itself places the C-terminus in a different domain (receptor binding), not inside the marked ADP
     ribosyltransferase domain.
   - So 'something else' holds, and the question "is the claim that the pair counts as 'something else' false?" should
     get **no**. Gold is yes.
   - The DrugProt PART-OF label for this pair is not supported by the text.
2. **`r_f7nn2_f7v2_tr_02525a_3`** (item 22, rung N2, ladder `f7v2-tr-02525a`).
   - Source: MedQuAD `r_gd_medquad_qtype_373`, `text_gold` = 'treatment options'.
   - The passage: "Proctitis that is not treated or does not respond to treatment may lead to complications, including
     severe bleeding … abscesses … ulcers … fistulas".
   - This is a complications passage. The source row's own 13-label set has a 'complications' label, yet this passage
     carries 'treatment'.
   - The card defines treatment options as "explains how the condition is treated or managed". The passage does not do
     that.
   - So 'something else' applies, the note "the passage cannot count as 'something else'" is false, and the answer
     should be **no**. Gold is yes.

## 4. Ambiguous (1 row)

**`r_f7nn2_f7v2_ii_00247a_4`** (probe iid, rung N3, ladder `f7v2-ii-00247a`).
- Source: FaithDial `fd-train-3399-1-orig`, faithful = False (BEGIN label).
- The snippet: "It may also be stated as the belief that, if something happens less frequently than normal …, it will
  happen more frequently in the future."
- The response: "Exactly. The gambler's fallacy happens when people think if they're on a losing streak it will have to
  turn into good luck soon."
- Reading A (mine): the response restates the snippet, and the seeker had already named the fallacy. That makes it
  grounded, so the answer is no.
- Reading B (gold): the snippet never names "the gambler's fallacy", and "losing streak → good luck" goes beyond it.
  That makes it embellished, so the answer is yes.
- Both readings are reasonable.

## 5. Low-confidence rows that agreed with gold (not counted)

- `02596b_3`: "SEAT CAUGHT FIRE AND BURNT A HOLE". Later the writer says it "could of caught fire". I took "caught fire"
  as flames.
- `00599b_2`: the sentence says PDE4B "modulat[es] the concentration of cAMP". 'substrate' is reached through the
  card's "exactly one relation" rule rather than stated outright.
- `02217b_4`: the sentence only implies that terfenadine is an H1 antagonist ("chemically unrelated to histamine
  H1-receptor antagonists such as …"). The exactly-one-false option structure forces 'antagonist'.

## 6. How far the two problems reach (counted by program after the read)

| Source text | Pattern | F7 rows | Ladder |
|---|---|---|---|
| `r_gd_drugprot_4478` | DrugProt 'part of'; the marked e2 is a domain; the text puts the C-terminus in another domain | 5 train | `f7v2-tr-02499b` |
| `r_gd_drugprot_4636` | Same pattern: "ISWI ATPase domain" + "C-terminal DNA-binding function residing in the HSS domain" | 5 train | `f7v2-tr-01565a` |
| `r_gd_medquad_qtype_373` | MedQuAD 'treatment' on a complications passage | 5 train | `f7v2-tr-02525a` |
| `fd-train-3399-1-orig` | FaithDial borderline faithful label (ambiguous, not wrong) | 5 probe | `f7v2-ii-00247a` |

- A scan of all DrugProt 'part of' rows with an N- or C-terminal chemical found 6 source texts. Only 4478 and 4636 have
  this problem. In 3608, 5620, 2927 and the probe text 12213829, the terminus does belong to the marked protein.
- A scan of MedQuAD 'treatment' rows that talk about complications found 2 texts. Only 373 is wrong; 3409 is a real
  treatment passage.
- **Outside F7:** `r_gd_medquad_qtype_373` and `r_gd_drugprot_4478` are also in `golden_train.jsonl`,
  `fix1_train.jsonl`, `train_2b_golden_kd*.jsonl` and the v14 label shards, so the same label noise reaches those sets.

## 7. Checks on the fixes from read 1 (current files)

- 0 train rows contain "never state(s)", and frame `nos5` has 0 rows.
- 0 of the 750 residual-ptype train rows have an "exactly one of the … below" rule without a catch-all line. In this
  sample, residual cards read "one of the types below or another type" and carry a 'something else' line.
- A string search finds none of the 8 source texts flagged in read 1 (NHTSA 283 and 2683, and 6 OIICS texts) in the
  current F7 train or probe states.
- In this sample:
  - the NHTSA multi-text card says "a fire that could happen by itself makes a smoke-only case";
  - the OIICS card says "being hit by a vehicle of any kind or by another person … are other kinds of event".

## 8. What must change before this passes (for the F7 builder; I edited no generator, data or frozen file)

1. Drop, or relabel to the label the text supports, the 3 source texts `r_gd_drugprot_4478`, `r_gd_drugprot_4636` and
   `r_gd_medquad_qtype_373`. That is 15 train rows in 3 ladders.
2. Add a build-time guard for both patterns:
   - DrugProt 'part of', where e2 names a domain and the text places the terminus in another domain;
   - MedQuAD 'treatment' (or any label) on a passage whose text is about complications, when 'complications' is in the
     source label set.
3. Probe ladder `f7v2-ii-00247a` (FaithDial `fd-train-3399-1-orig`, 5 rows): drop it or swap the text, because its
   faithful label is borderline. It is within the 3% budget, but the owner asked for no compromise.
4. Owner decision, outside F7: the same noisy labels sit in `golden_train.jsonl` and the sets built from it (section 6).
5. Re-run decide2 and the precheck, then do blind read 3 on a fresh sample, excluding read 1 and read 2 ids and ladders.
   The bar is still 0 wrong gold and at most 3% unreadable plus ambiguous.

## Files

- Sampler: `yn2b/f7_blind_read_sample2.py` (seed 20261012; excludes read-1 ids and ladders)
- Answers, frozen before gold (id, answer, flag, reason): `yn2b/f7_blind_read_2_answers.tsv`
- Verdicts for precheck `--blind-read` (id, verdict: ok / wrong_gold / ambiguous): `yn2b/f7_blind_read_2_verdicts.json`
- Comparer (unchanged): `yn2b/f7_blind_read_compare.py --dir <scratchpad>/blind2`
- Re-run outputs (scratchpad `blind2/`): `decide2_preds_rerun.jsonl`, `decide2_report_rerun.json`,
  `f7_precheck_rerun.json`, `f7_precheck_only11.json`. The saved `yn2b/f7_decide2_*` and `yn2b/f7_precheck.json` were
  not overwritten.
