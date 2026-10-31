# F7 blind read (checklist section 4, item 11)

**Result: FAIL.** Wrong gold = 3 (bar: 0). Ambiguous = 16 of 300 generator rows = 5.3% (bar: at most 3%). Unreadable = 0. devx: 220 of 220 agree, so there are no devx disagreements to resolve and no devx file was changed.

Date: 2 Oct 2026. CPU only. No model, no network and no ohs3 file was used.

## 1. Method

- **Who read.** An agent that did not write F7. I never opened `gen3_nested_negation.py`, `v3_nested_negation.py` or any decide2 output.
- **Sample.** Script `yn2b/f7_blind_read_sample.py`, seed 20261002. It drew:
  - 10 rows for each of the 18 MUST items (1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15, 16, 21, 22, 24, 27, 36). These are 180 rows, picked by the sidecar `phen` field only.
  - 100 random rows from `f7_train.jsonl`, with no overlap with the MUST rows.
  - 20 random rows from `f7_probe.jsonl`.
  - All 220 rows of `f7_devx.jsonl`.
- **Blinding.** The script wrote the card, state, question and options only. It left out `gold`, `role` and `meta`, and put gold in a separate file. I answered all 520 rows from the text alone, in batches of 20, and logged each answer with a confidence flag and a reason. Then `yn2b/f7_blind_read_compare.py` compared the answers with gold. I looked at the sidecar meta (`lf`, `text_gold`, `derived_from`) only after the comparison, to adjudicate.
- **Answers.** `yn2b/f7_blind_read_answers.tsv` has one line per row: id, answer, flag, reason. The flag was written before I saw gold.

## 2. Numbers

| Group | Rows | Agree with gold | Disagree |
|---|---|---|---|
| MUST items (10 each) | 180 | 170 | 10 |
| Random train | 100 | 94 | 6 |
| Probe | 20 | 20 | 0 |
| **Generator rows, total** | **300** | **284 (94.7%)** | **16** |
| devx (all) | 220 | 220 (100%) | 0 |

I adjudicated each of the 16 disagreements:

| Verdict | Rows |
|---|---|
| Wrong gold | 3 |
| Ambiguous (two reasonable readings) | 7 |
| My error, gold defensible | 6 |

I also flagged 9 rows as ambiguous before seeing gold, and my answer matched gold on all 9. They still count as ambiguous because a careful reader could answer them the other way.

**Totals on the 300 generator rows:** wrong gold 3 (1.0%), ambiguous 16 (5.3%), unreadable 0. Over all 520 rows read, the ambiguous share is 16/520 = 3.1%, which also fails the bar.

The negation composition was never the cause. In all 300 rows, every disagreement and every flag comes from one of two places: (a) a card line that contradicts the state, or (b) the human label of the base text not matching the card's definition. In no row did the program mis-handle a frame, the depth or a distractor, and every double and triple negation I worked through came out the way the program says.

## 3. Wrong gold (3 rows)

1. **`r_f7nn2_f7v2_tr_01665a_3`** (item 2).
   - The question: "can one say that not every complaint in the batch reports an actual vehicle fire?" Gold is no, because the program has all 4 complaints as fires.
   - Complaint 4 (`r_gd_nhtsa_complaints_2683`) has only smoke from the alternator, a burning-plastic smell, and the owner cut the batteries "to prevent … fire". It mentions no flames.
   - The card itself says "smoke, a burning smell or overheating by itself makes a smoke-only case". So by the card, the right answer is yes.
   - The cause is the source label: the NHTSA FIRE flag is set for smoke events.
2. **`r_f7nn2_f7v2_tr_01108b_1`** (random).
   - Narrative 1 reads "HIT BY A CAR BACKING OUT OF PARKING SPACE". The card defines "struck by a moving object" as "something fell, swung, rolled or flew into the worker", and says nothing that excludes vehicles.
   - Gold treats Narrative 1 as not struck. In the source taxonomy (OIICS), a pedestrian hit by a vehicle is a transport event, not "struck by object". The card does not tell the reader that.
3. **`r_f7nn2_f7v2_tr_00881b_4`** (item 3).
   - The card says "rule: the sentence states exactly one of the relations below". It lists agonist, substrate and inhibitor. Inhibitor is defined as "reduces what the protein does, either by binding it or by some route…". The sentence says lorglumide is an "antagonist of the CCK-A receptor".
   - Gold (yes: it is untrue that the pair fits one of the 3 lines) contradicts the rule line. It also ignores that the inhibitor line covers an antagonist.

## 4. Ambiguous (16 rows)

**A. The card's rule line is false (9 rows in the sample).** The card says "exactly one of the labels below fits", but the text's gold label is not listed and there is no catch-all line. The reader then has to choose between trusting the rule and trusting the text. This happens in 7 rows plus `00262b_1` here, and `00881b_4` above is the same kind of row:
- `01669a_0`: a diagnosis passage, and the card lists 4 other types.
- `00262b_1`: a capex passage that reads as MD&A, and the card lists Properties, Business, Legal and Risk. I followed the rule line here and disagreed with gold.
- `01804b_1`: fence damage only, and the card lists EF1, EF3 and EF2.
- `00471b_1`: a pothole, and the card lists debris, tree and parking.
- `01371b_0`: "deficiency of G6PD" is a specific disease, and the card lists composite, class and modifier.
- `01878b_0`: ML-145 is an antagonist, and the card lists agonist, activator and substrate.
- `00992b_4`: "I don't want to cost jobs" is an opinion, and the card lists check-worthy and minor.
- `01453b_0`: "alabama" is a location, and the card lists product, group, corporation and title.

Program count over the whole family: 144 train rows (1.1%) and 29 probe rows. All are ptype `residual`.

**B. The card's definition does not match the source label (3 rows).**
- `01672a_2` and `00098b_2` (sc101): "saying things in a way that make you seem confused" and "eating too many snacks before dinner" are labelled not acceptable. The multi-text card defines objectionable as "rude or unkind", and neither action is.
- `01310b_4` (ClaimBuster): "he made the misjudgment of saying to America that he was going to build a true alliance…" has gold 'minor factual remark'. The card defines that label as a trivial fact fact-checkers would pass over.

**C. Two labels fit, or the text states two relations (4 rows).**
- `00441a_3` (CaSiNo): "you will get the extra water your camp needs" fits both 'showing empathy' and 'promoting coordination'.
- `02369a_1` (10-K): a competition passage phrased as "may have the effect of reducing…" fits both Business (competition) and Risk Factors (phrased as what could happen).
- `02841a_3` (ChemProt): the sentence says tamoxifen "acts as an antagonist, but later functions as an ER agonist".
- `01459b_1` (MedQuAD): the claim is "'signs and symptoms' is the only label that fits", but the passage has a full "Tests for Cataract" section.

**D. Frame wording (1 row).** In `01809a_2`, "does the batch never state that the batch is made up only of unacceptable actions?" is a list of actions, which literally states nothing, so the literal answer is yes. The intended reading ("fails to show") gives no. This is frame `nos5`, with 28 train rows.

## 5. My errors, gold defensible (6 rows)

These are hard base labels, and the gold is a fair reading. They are not counted as ambiguous:
- `01370b_2` and `01968a_3` (ClaimBuster).
- `02710b_2`, `02710b_0`, `02441a_3` and `01176b_3` (OneStopEnglish level).

Of the 300 rows, about 45 needed a guess about a human label (OneStop level, ClaimBuster, CaSiNo, sc101, EF rating with no wind speed). I got 6 of those wrong. The model will face the same noise.

## 6. Wider audits I ran while adjudicating (train file)

- **NHTSA fire.** Of 86 fire-labelled texts, 2 are smoke-only by the card's own definition: `r_gd_nhtsa_complaints_283` and `_2683`. They appear in 15 train rows (ladders `00576a`, `00576b` and `01665a`).
- **OIICS struck-by.** 6 texts labelled "not struck" describe a worker hit by a car, a forklift or a person:
  - `r_gd_oiics_event_298`, `_2676`, `_4444`, `_671`, `_1417`, `_694`;
  - these are in 34 rows across 7 ladders, an upper bound since not every row's gold depends on them.
- **Rule-line contradiction.** 144 train rows and 29 probe rows (section 4A).
- **`nos5` "never states" frame.** 28 train rows.

## 7. Minor wording notes (not counted)

- `01229b_4`: the card-less choice row uses 'intact case' without defining it. It can be inferred from "exactly one statement holds".
- Made-up labels are defined over one kind of thing but asked about another: "sticker J: a non-group *post*" is asked of "the marked name", and "stamp P: a *dialogue* that…" is asked of "the user's latest message". Each is readable, but loose.
- "no-show: a guest who did not accept" uses an everyday word against its normal meaning. The card defines it, so it is fine, but it is a trap.

## 8. devx (220 rows)

- I solved all 220 rows cold and agree with all of them, so there are 0 disagreements and no gold or wording was changed in `data/v14_parts/f7_devx*.jsonl`.
- I was least sure about ladder `01b` (sarcastic "surplus land … pray tell?"). It mocks an idea rather than a person, so non-toxic is the better reading, and I agree with that gold.

## 9. What must change before this passes (for the F7 builder; I did not edit the generator)

1. **Residual cards.** When the gold label is left off a "first N label lines" card, either add a catch-all line or drop the "exactly one of the labels below" rule line. Affects 144 train and 29 probe rows.
2. **NHTSA fire.** Drop or relabel texts `_283` and `_2683` for the fire property, or require flame words for fire = true. Affects 15 rows.
3. **OIICS struck-by.** Add "an object, not a vehicle or a person" to the card definition, or drop the 6 texts. Affects up to 34 rows.
4. **sc101 multi-text card.** Use the single-text definition ("rude, unkind, dishonest, irresponsible or harmful"), or keep only actions that clearly sit on one side.
5. **ChemProt.**
   - Drop sentences that state two relations for the pair.
   - Never list 'inhibitor' without 'antagonist' when the gold label is antagonist.
6. **Frame `nos5`.** Replace "never states" with "fails to show". Affects 28 rows.
7. **"Only" and "exactly one" claims.** For CaSiNo, 10-K competition passages and multi-section MedQuAD passages, keep these claims to single-topic texts, or drop the overlapping pairs.
8. **Re-run.** Then run this blind read again on a fresh sample. The bar is still 0 wrong gold and at most 3% ambiguous.

## Files

- Answers (one per row, flag written before gold was seen): `yn2b/f7_blind_read_answers.tsv`
- Sampler: `yn2b/f7_blind_read_sample.py`
- Comparer: `yn2b/f7_blind_read_compare.py`
