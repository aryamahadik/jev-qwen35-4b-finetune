# LOCAL_GAPS: what C1 was trained on, and where it fails on dev

Date: 3 Oct 2026. Read-only, CPU-only analysis. No test splits, OHS-3 files, preds_ohs* or quarantined items were opened.

**Inputs**
- C1's training data: `data/v14_parts/golden_train.jsonl` (501,732 rows, 204 sources, 1.23 GB). `runs/q35_4b_main.json` confirms it is C1's `train_file`: 0.971 epochs, `micro_tokens` 8192, `kd` 0.5 on 43,363 KD targets, with the blend50 replay teacher skipped.
- Dev predictions: `preds_<split>/q35_4b_main500k.jsonl` (C1) and `q35_4b_pxE_fresh.jsonl` (4B-E) on the 9 gate splits (8,143 rows). They are scored with `gate_dev.score` / `complete_rows` / `group_boot`, imported read-only.
- Sanity check: on the 17 frozen unseen sources this reproduces **C1 83.99 vs 4B-E 81.52** exactly.

**Method**
- One streaming pass over every row.
- Token counts use the Qwen3.5-4B tokenizer on the exact `schema_branch_mark` prompt (`decoder_io.user_msg`), plus the system prompt and about 12 template tokens.
- Negation, format, abstain-option and "close option" flags come from regexes.
- Each source is mapped by hand to one primary task type and one domain.
- Per-source table: `c_spec/golden_train_sources.csv`. Scripts and the raw dev printout are in `c_spec/local_gaps_scripts/`.

---

## 0. Bottom line

1. **C1's data is short.**
   - Median prompt is 508 tokens and p99 is 1,685. The maximum is 5,445.
   - Only 0.38% of rows are 2K-4K tokens, 0.02% are 4K-8K, and none are above 8K.
   - "Trained up to 8K" is the micro-batch budget, not the data. Long documents are essentially untrained.
2. **Several Jev Decision Index task types are near zero in training:**
   - tools / function calling: 290 rows (0.06%)
   - risk / forecast: 873 (0.17%)
   - stance: 901 (0.18%), and these are not real stance rows
   - emotion: 1,571 (0.31%)
   - sarcasm: 1,930 (0.38%)
   - aspect sentiment (ABSA): about 590 (0.12%)
   - code or commit diffs: 0 rows
3. **Negated yes/no is narrow.**
   - 91% of the 37,552 "neg" rows use one template: `Is it wrong to answer "X"?`.
   - True double negation in the question (role dneg) is 1,107 rows (0.22%), all from old replay. Syntactic negation (not / no / never / without / cannot) appears in only 6.6% of yes/no questions.
4. **The formats are narrow.**
   - 96% of rows carry a definitions card. 26% of choice rows use opaque option codes.
   - 51% of rows come from sources with 5 or fewer instruction templates.
   - 22% of yes/no rows are a "label-check" form (`Which X? / Is the correct answer "Y"?`) that real tasks do not use.
   - JSON is 0.46% of rows, email 1.3%, HTML about 0, and diffs 0.
5. **On dev, C1's weakest primitives** (C1 vs 4B-E):
   - many fine-grained labels (21+ options): 53.4 vs 57.5
   - ordinal scales: 51.6 vs 48.4, and 58% of these errors are off by one
   - emotion: 58.0 vs 58.6
   - multi-hop record chains: 55.3 vs 66.7 (-11.3, CI excludes 0)
   - policy amendments and precedence: 73.3 vs 84.0 (-10.7, CI excludes 0)
   - money arithmetic under rules: 51.3 vs 52.7
   - gold = abstain (NEI 59.4, "none of these" 52.6; small n)
   - hate yes/no: 64.4
6. **C1's dev gain sits on unseen sources only.**
   - Unseen sources: +2.5 pp [+1.3, +3.7].
   - Sources that C1 or 4B-E trained on: -0.9 pp. There, C1 answers "yes" too often on yes/no questions whose answer is "no" (80.4 vs 85.4).
7. **Double-negation consistency breaks on some sources.**
   - On `hate`, C1 gives different answers to 32 of 60 equivalent aff / dneg pairs (53.3%), against 3.3% for 4B-E. This matches the 8.9% double-negation flip rate seen elsewhere.
   - Dev hides most of this, because 833 of its 904 dneg rows use one template ("Should the statement that ... be rejected?").
8. **The dev suite cannot see several gaps:**
   - its longest prompt is 2,290 tokens
   - it has no tools, stance, commonsense, knowledge MC or code rows
   - its dneg wording is a single template
   - 53% of dev rows come from source families that C1 or 4B-E trained on

---

## 1. Profile of golden_train (C1's data)

### 1.1 Question types and roles
| | Rows | Share |
|---|---|---|
| Yes/no (`noul`) | 323,868 | 64.6% |
| Choice | 177,864 | 35.4% |
| Yes/no, natural question | 253,163 | 78.2% of yes/no |
| Yes/no, label-check `Is the correct answer "X"?` | 36,615 | 11.3% of yes/no |
| Yes/no, label-check `Is it wrong to answer "X"?` | 34,090 | 10.5% of yes/no |
| Gold = yes | | 49.7% of yes/no (balanced in every form) |

Roles:

| Role | Share |
|---|---|
| aff | 52.6% |
| choice | 32.5% |
| neg | 7.5% |
| attacked | 6.4% |
| defswap | 0.60% |
| para | 0.23% |
| dneg | 0.22% |
| clause_neg | 0.02% |
| trap_aff / trap_neg | 0.03% together |

Tracks: GD (new golden) has 453,980 rows (90.5%). Older replay tracks have the remaining 47,752 rows (BR, L0, L2, HARD, L3, PG, OHR, JUDGE, STD, PROC, TB, DEBATE, PLANT, BINJ).

### 1.2 Option counts (choice rows)
| Options | 2 | 3 | 4 | 5 | 6-8 | 9-12 | 13-20 | 21-40 | 41-81 |
|---|---|---|---|---|---|---|---|---|---|
| Share | 2.0% | 15.3% | 16.8% | 6.7% | 17.0% | 11.4% | 20.3% | 10.1% | 0.5% |

- The gold position is balanced: with 4 options it is 25.6 / 25.4 / 24.9 / 24.1%.
- The wide label sets (13-40 options) are mostly industrial code books with full cards: MSHA, OIICS, NAICS, WANDS, drug-label sections and 311 routing. They are not fine-grained topic or emotion taxonomies.

### 1.3 Lengths (Qwen3.5-4B tokens, full prompt)
| Percentile | p10 | p25 | p50 | p75 | p90 | p99 | max |
|---|---|---|---|---|---|---|---|
| Prompt tokens | 321 | 387 | 508 | 730 | 1,044 | 1,685 | 5,445 |

| Bin | <256 | 256-512 | 512-1K | 1-2K | 2-4K | 4-8K | >8K |
|---|---|---|---|---|---|---|---|
| Rows | 7,013 | 247,119 | 192,051 | 53,582 | 1,884 | 83 | 0 |
| Share | 1.4% | 49.3% | 38.3% | 10.7% | 0.38% | 0.02% | 0% |

- Text ("state") words: median 65, p90 263, p99 817.
- Rows over 2K tokens come from: gd_conditionalqa (681), gd_wtq (429), gd_helpsteer3_pref (353) and gd_gen2_long_policy (294). Rows over 4K come almost only from gd_conditionalqa (68 of 83).
- The 13,157 rows tagged `long_context` have a median of only 1,156 tokens.

### 1.4 Definitions cards and label naming
- 96.0% of rows have a definitions card (choice 93.9%, yes/no 97.1%). The median card is 526 characters.
- Rows with no card: 20,270 (4.0%). Almost all are old intent replay: clinc150, banking77 and massive, plus boolq, mnli, condaqa and judge replay.
- Opaque option codes ("Code 42", "Option W", "Class X"): 46,423 rows, which is 26.0% of choice rows.
- Definition-swap twins: 3,008 (0.6%).
- No rows were found where an invented word is defined only in the card. "Invented jargon" is therefore untrained, apart from codes and defswaps.

### 1.5 Negation
The question was scanned with the quoted label removed and "yes or no" ignored.

| Negation cues in the question | 0 | 1 | 2+ |
|---|---|---|---|
| All rows | 81.7% | 16.5% | 1.8% (9,084) |
| Yes/no | 75.8% | 22.8% | 1.35% (4,364) |
| Choice | 92.3% | 5.1% | 2.65% |

- In yes/no questions, syntactic negation (not, no, never, none, without, cannot, n't) appears in 6.6% of rows. Lexical-only negation (wrong, false, reject, fail ...) appears in 17.6%.
- The "neg" role has 37,552 rows. 34,090 of them (91%) are `Is it wrong to answer "X"?`, and only 3,462 are natural negated questions.
- Role dneg: 1,107 rows (0.22%), 763 templates, 17 sources, all v13 replay (mnli, condaqa, clinc150, boolq, banking77 ...).
  - The `double_negation` edge tag (6,074 rows, 1.2%) mostly marks double negation inside generator TEXT ("cannot be without breakfast"), not in the question.
- By task type, the share of questions with syntactic negation is about 0% for knowledge MC, ordinal, relation typing, moral norms, sarcasm, stance and tools. It is 18-27% for NLI, judge and logic.

### 1.6 Text formats (primary format of the state, by regex)
| Format | Share |
|---|---|
| prose | 57.8% |
| key: value records | 14.8% |
| tables | 11.6% |
| bullet lists | 8.2% |
| dialogue | 5.7% |
| email | 1.3% |
| JSON | 0.46% |
| code | 0.18% |
| HTML | ~0% |
| diff | 0% (1 row) |

- Code rows are code inside chat-judging data (helpsteer3, mtbench), not software decisions.
- JSON comes mostly from injection containers on replay rows.
- There are 743 distinct header lines. The top ones are "Game state (facts):", "Evidence:", "Passage:", "Infobox:" and "Conversation:".

### 1.7 Instruction variety
- There are 51,761 distinct normalised instructions (quoted strings and digits masked). The median source has 8.5.
- **87 of 204 sources (258,007 rows, 51.4%) use 5 or fewer instruction templates.** For example, gd_medqa_yn has 1 template for 8,274 rows, and gd_feverous and gd_tatqa have 2 each.
- Yes/no openers: "Is" 43.6%, "Does" 20.5%, "Based ..." 8.0%, "Did" 4.5%.
- Choice openers: "Which" 55%.

### 1.8 Abstain options, close options, attacks, soft labels
- An NEI-type option (unknown / undetermined / not enough info / cannot be determined) is offered on 58,194 rows (11.6%).
- Gold is NEI on 6,255 choice rows (3.5% of choice). The `missing_info` edge appears on 21,040 rows (4.2%).
- Yes/no rows can never abstain.
- A "none of these / other" option appears on 24,805 choice rows. It is gold on 3,921.
- Close distractors:
  - near-miss yes/no: 25,801 rows (5.1%)
  - choice rows where two visible options share 50% or more of their words: 34,008 (19% of non-coded choice rows)
- Attack twins: 35,214 rows (7.0%) over 121 sources. Most are plain-text containers. JSON-field containers: 1,273. Tool or knowledge-base containers: about 370.
- Soft labels: teacher meta on 88,466 rows. Training used 43,363 KD targets (8.6%; `expect_kd_targets` in the run config). The brief describes them as human vote shares.

### 1.9 Domains (hand mapping, one per source)
| Domain | Rows | Share | Sources |
|---|---|---|---|
| Program-generated business / HR / ops scenarios | 108,519 | 21.6% | 42 |
| Encyclopedia / general knowledge | 57,697 | 11.5% | 15 |
| Government safety / incident reports | 48,933 | 9.8% | 10 |
| Medical / health | 42,086 | 8.4% | 11 |
| Synthetic logic / puzzles | 39,276 | 7.8% | 12 |
| Social media / online comments | 37,243 | 7.4% | 24 |
| Customer support / assistants | 34,205 | 6.8% | 14 |
| Everyday / commonsense | 28,134 | 5.6% | 11 |
| Finance / business filings | 27,806 | 5.5% | 7 |
| AI outputs (judging) | 25,107 | 5.0% | 15 |
| Science / climate | 23,771 | 4.7% | 9 |
| Legal / regulatory | 7,923 | 1.6% | 8 |
| General NLI / paraphrase corpora | 7,279 | 1.5% | 10 |
| Reviews | 5,619 | 1.1% | 7 |
| News / politics | 4,774 | 1.0% | 7 |
| Education / reading | 3,360 | 0.7% | 2 |
| Software engineering / code / commits | **0** | **0%** | 0 |

Other domains with no or tiny training: HR and recruiting text from real sources, e-commerce product Q&A, cybersecurity and IT logs, insurance claims text from real sources, scientific peer review, education grading, and real-estate and travel listings. All of these are 0% outside the generators.

---

## 2. Gap (a): Jev Decision Index task types vs C1's training

Dev evidence is C1 vs 4B-E on the closest dev family. "-" means the dev suite has no such rows.

| Task type | Training rows | Share | Sources | Closest dev evidence | Gap |
|---|---|---|---|---|---|
| NLI / fact verification | 71,819 | 14.3% | 27 | cb 93.8 vs 92.4; trueteacher 78.6 vs 72.3 | covered |
| Topic / domain classification | 62,213 | 12.4% | 24 | news topic 95.4; political topic (manifesto 56 labels, capsotu 21) 56.7 vs 57.6 | covered for coarse topic; **fine-grained taxonomies weak** |
| Policy / rule application | 60,671 | 12.1% | 28 | pg_* 65.5 vs 65.3; hard_* 79.8 vs 77.4 | covered but weak (see section 4) |
| Table / numeric reasoning | 46,445 | 9.3% | 9 | pg_numeric 51.3 vs 52.7 | covered; rule arithmetic weak |
| Intent / routing | 33,646 | 6.7% | 13 | clinc/banking 90.3 vs 91.9 (seen); pg_routing 72.0 vs 57.3 | covered |
| Knowledge MC (exams / trivia) | 32,337 | 6.5% | 8 | - | moderate (Jev leads MMLU-Pro / GPQA; a LoRA cannot add much knowledge) |
| Relation / entity typing | 28,269 | 5.6% | 8 | - | covered |
| Commonsense | 28,057 | 5.6% | 12 | - | moderate; not measured |
| Dialogue state / next action | 25,290 | 5.0% | 7 | - | covered for slots and acts |
| Judge / verifier | 23,283 | 4.6% | 13 | - | covered |
| Logic / rule reasoning | 22,820 | 4.5% | 10 | - | covered |
| Moderation / safety | 21,383 | 4.3% | 19 | hate / offensive 75.2 vs 73.7; hate yes/no 64.4 | covered; hate weak |
| Ordinal / score | 17,193 | 3.4% | 6 | ordinal choice rows 51.6 vs 48.4 | **weak** |
| Moral / social norms | 16,515 | 3.3% | 2 | - | covered |
| Sentiment (whole text) | ~5,640 | 1.1% | 6 | sentiment 92.2 vs 91.7 | thin but fine on dev |
| ABSA (aspect sentiment / category) | ~590 | 0.12% | 2 (br_mams_acsa, br_steam_aspect) | - | **near zero** |
| Emotion | 1,571 | 0.31% | 4 | emotion 58.0 vs 58.6 (6-way choice 47.0; 32-way empathetic 45.5 vs 55.4) | **near zero, and weak** |
| Sarcasm / irony | 1,930 | 0.38% | 2 | irony 87.2 vs 74.4 | thin, but fine on dev |
| Stance | 901 | 0.18% | 1 (wiki_stance_afd; deletion outcome, not real stance) | climate risk / opportunity 76.2 vs 70.8 | **near zero** |
| Risk / forecast | 873 | 0.17% | 2 (gd_gen2_probability, pg_evidence) | pg_evidence 64.7 vs 68.7 | **near zero** |
| Tools / function calling | 290 | 0.06% | 1 (gd_gen2_tool_selection) | - | **near zero** |
| Long documents (prompt over 2K tokens) | 1,967 | 0.39% | mostly 4 | - (dev max 2,290 tokens) | **near zero** |
| Code / commit decisions | 0 | 0% | 0 | - (ejs-5: C1 54.1 vs Jev 58.5) | **zero** |

---

## 3. Gap (b): the PLAN's skill families vs what C1 has

| PLAN skill | What C1's data has | Verdict |
|---|---|---|
| Indirect-evidence yes/no | 7,650 natural yes/no rows tagged `implicit` (2.4% of yes/no). Most yes/no asks what the text states, not what it implies. | thin |
| Rule / policy composition | 60,671 rows (12.1%), plus 34,200 rows tagged `exception`. Mostly from 8 Claude-written generators. | covered in volume; dev shows weakness on amendments, precedence and multi-hop (section 4) |
| State tracking | Dialogue slots and acts: 25,290 rows (5%). Entity state over event sequences (bAbI, MuSR, pg / proc temporal): 5,110 rows (1.0%). | thin for event-sequence state |
| Ordinal judgment | 17,193 ordinal-type rows, plus ordinal-option rows; 21,084 in total (4.2%). | thin; dev weak and off by one |
| Risk prediction | 873 rows (0.17%). The incident-severity sources (storm EF, SaferProducts) grade past events and do not predict. | **missing** |
| Table / fact reasoning | 46,445 rows (9.3%); 11.6% of rows have tables. | covered |
| Close distractors | Near-miss yes/no: 25,801 (5.1%). Close choice options: 34,008 rows (19% of non-coded choice rows). | covered |
| Invented jargon defined in the card | 0 detected. Opaque codes: 26% of choice. Defswap twins: 0.6%. | **missing** |
| Hard / negated yes/no | Neg role 7.5%, but 91% is one template. Dneg 0.22%. Natural syntactic negation 6.6% of yes/no. Yes/no with 2+ cues 1.35%. | **thin and narrow** |
| Not enough information | NEI option on 11.6% of rows; gold NEI on 3.5% of choice rows; yes/no can never abstain. | thin as gold; dev 59.4 when gold is NEI |
| Attack-resistant variants | 35,214 rows (7.0%), 121 sources. | covered (C1 hijack result already strong) |
| Long documents | 0.39% over 2K tokens; 0.02% over 4K; maximum 5,445. | **missing** |
| Commit decisions (other repos) | 0 rows; no diffs. | **missing** |
| Format variety | 51% of rows from sources with 5 or fewer templates. 96% have a card. 26% of choice rows use codes. 22% of yes/no rows are label-check. JSON 0.46%, email 1.3%, HTML / diff / logs about 0. | **narrow** |
| Fine-grained label taxonomies (not in PLAN; found here) | 21+ options = 10.6% of choice rows, almost all code books with cards. No 20-60-label topic or emotion taxonomies with near-synonym labels. | **missing** |
| Emotion / stance / ABSA / sarcasm (not in PLAN's 12; Jev index types) | 0.31% / 0.18% / 0.12% / 0.38% | **missing**: cover them through commercial-licence public training splits |

---

## 4. Dev error breakdown (C1 vs 4B-E)

**Setup**
- Pooled over all 9 gate splits and both dev halves: 8,143 rows. Ties and missing count as wrong.
- Intervals come from a paired bootstrap over group_id (2,000 draws, seed 0).
- This is information only, not a gate verdict. Many buckets are small.

**Overall:** C1 81.42 vs 4B-E 80.72 (+0.70).

| Slice | Rows | C1 | 4B-E | Diff [95% CI] |
|---|---|---|---|---|
| Unseen sources (frozen 17) | 3,847 | 84.0 | 81.5 | +2.5 [+1.3, +3.7] |
| Other dev rows | 4,296 | 79.1 | 80.0 | -0.9 [-2.2, +0.5] |

### 4.1 By split
| Split | Rows | C1 | 4B-E | Diff [CI] | Share of C1 errors |
|---|---|---|---|---|---|
| pg_dev | 1,049 | 65.5 | 65.3 | +0.2 [-2.9, +3.2] | 23.9% |
| dev_nc | 1,008 | 76.4 | 75.3 | +1.1 [-0.9, +2.9] | 15.7% |
| devzs | 800 | 77.4 | 76.0 | +1.4 [-0.4, +3.4] | 12.0% |
| hard_dev | 208 | 79.8 | 77.4 | +2.4 [-1.8, +6.4] | 2.8% |
| taskbank_dev | 1,200 | 82.6 | 84.6 | **-2.0 [-3.9, -0.1]** | 13.8% |
| devp_card | 1,728 | 86.7 | 84.3 | **+2.4 [+0.7, +4.2]** | 15.2% |
| dev_negwords | 800 | 87.5 | 86.4 | +1.1 [-1.1, +3.5] | 6.6% |
| dev_claims | 750 | 88.3 | 86.7 | +1.6 [-0.9, +4.4] | 5.8% |
| dev | 600 | 89.5 | 91.3 | -1.8 [-3.8, +0.2] | 4.2% |

### 4.2 By source family
| Family | Rows | C1 | 4B-E | Diff [CI] | Share of C1 errors |
|---|---|---|---|---|---|
| Political topic (capsotu 21 labels, manifesto 56) | 224 | **56.7** | 57.6 | -0.9 [-5.4, +4.5] | 6.4% |
| Emotion (emotion, empathetic) | 512 | **58.0** | 58.6 | -0.6 [-3.8, +2.6] | 14.2% |
| pg_* policy generators | 1,049 | **65.5** | 65.3 | +0.2 [-2.9, +3.2] | 23.9% |
| Hate / offensive | 735 | 75.2 | 73.7 | +1.5 [-2.8, +5.6] | 12.0% |
| Climate risk / opportunity | 390 | 76.2 | 70.8 | +5.4 [+1.0, +9.9] | 6.1% |
| Factual consistency (trueteacher) | 112 | 78.6 | 72.3 | +6.2 [+0.9, +12.3] | 1.6% |
| hard_* expert-written | 208 | 79.8 | 77.4 | +2.4 [-1.8, +6.4] | 2.8% |
| Synthetic zero-shot tasks (tb) | 1,200 | 82.6 | 84.6 | -2.0 [-3.9, -0.1] | 13.8% |
| Irony | 391 | 87.2 | 74.4 | +12.8 [+5.7, +20.6] | 3.3% |
| Intent (clinc / banking) | 1,440 | 90.3 | 91.9 | -1.6 [-3.8, +0.5] | 9.3% |
| Sentiment | 618 | 92.2 | 91.7 | +0.5 [-1.4, +2.2] | 3.2% |
| NLI (cb) | 291 | 93.8 | 92.4 | +1.4 [-1.7, +5.4] | 1.2% |
| News topic | 583 | 95.4 | 94.9 | +0.5 [-0.5, +1.7] | 1.8% |
| Spam | 390 | 98.5 | 97.7 | +0.8 [+0.0, +2.4] | 0.4% |

**Worst single sources for C1** (rows, C1 vs 4B-E):

| Source | Rows | C1 | 4B-E | Diff [CI] |
|---|---|---|---|---|
| btzsc_manifesto | 112 | 42.9 | 45.5 | |
| btzsc_empathetic | 112 | 45.5 | 55.4 | **-9.8 [-17.9, -2.7]** |
| pg_numeric | 150 | 51.3 | 52.7 | |
| pg_multihop | 150 | 55.3 | 66.7 | **-11.3 [-19.3, -3.3]** |
| emotion | 400 | 61.5 | 59.5 | |
| hate | 399 | 63.9 | 63.4 | |
| pg_evidence | 150 | 64.7 | 68.7 | |
| pg_policy | 150 | 73.3 | 84.0 | **-10.7 [-18.0, -3.3]** |
| tb_mixtral | 1,087 | 83.7 | 86.2 | -2.5 [-4.3, -0.8] |

**C1's clear wins:**

| Source | Diff |
|---|---|
| pg_routing | +14.7 [+8.0, +22.7] |
| irony | +12.8 |
| financialphrasebank | +8.0 [+2.7, +14.3] |
| trueteacher | +6.2 |
| climate | +5.4 |

### 4.3 By question type and role
| Type : role | Rows | C1 | 4B-E | Diff [CI] | Share of C1 errors |
|---|---|---|---|---|---|
| choice | 3,814 | **77.1** | 76.4 | +0.7 [-0.3, +1.8] | 57.6% |
| yes/no aff | 1,818 | 82.9 | 83.4 | -0.5 [-2.1, +1.0] | 20.5% |
| yes/no dneg | 904 | 85.1 | 84.5 | +0.6 [-1.8, +2.9] | 8.9% |
| yes/no neg | 1,508 | 87.6 | 85.4 | +2.2 [+0.3, +4.1] | 12.4% |
| yes/no para | 99 | 90.9 | 90.9 | 0.0 | 0.6% |

- **Choice is C1's main error mass:** 58% of errors, against 47% of rows.
- Inside pg_dev, choice is 61.8% and yes/no is 74.6%.
- **Yes vs no, affirmative questions:**
  - Gold "no": C1 81.4 vs 86.5.
  - Gold "yes": C1 84.6 vs 80.3.
  - On seen sources, C1 is weaker when gold is "no": 80.4 vs 85.4 (-5.0). On unseen sources it is stronger: 89.0 vs 86.7.
  - C1 has moved toward "yes" on affirmative questions in familiar families. Overall it predicts "yes" on 50.4% of yes/no rows (gold: 50.0%).

**Role by unseen-source split:**

| Role | Unseen sources: C1 vs 4B-E | Other sources: C1 vs 4B-E |
|---|---|---|
| aff | 86.4 vs 84.5 | 80.2 vs 82.6 |
| neg | 89.6 vs 84.5 | 85.1 vs 86.5 |
| dneg | 88.1 vs 84.6 | 79.8 vs 84.3 (**-4.5**) |

**Weak yes/no families:**

| Family | C1 | 4B-E |
|---|---|---|
| tb yes/no | 84.7 | 89.4 |
| intent yes/no | 89.2 | 92.2 |
| hate yes/no | 64.4 | 63.5 |

### 4.4 By option count (choice rows)
| Options | 2 | 3 | 4-5 | 6-9 | 10-20 | 21+ |
|---|---|---|---|---|---|---|
| Rows | 1,006 | 967 | 726 | 728 | 39 | 348 |
| C1 | 84.7 | 79.2 | 70.0 | 83.1 | 64.1 | **53.4** |
| 4B-E | 83.2 | 78.2 | 68.5 | 82.3 | 64.1 | 57.5 |

- 21+ options is entirely empathetic (32 labels), manifesto (56) and capsotu (21). Diff -4.0 [-8.0, +0.3].
- The low 4-5 option score is pg and tb rows. Inside tb_mixtral, the option count has no effect (3: 82.2; 4-5: 82.8).
- So the weak primitive is **fine-grained, near-synonym label taxonomies**, not option count as such.

### 4.5 By length (prompt tokens)
| Bin | <256 | 256-512 | 512-1K | 1-2K | >2K |
|---|---|---|---|---|---|
| Rows | 2,028 | 3,938 | 1,742 | 433 | 2 |
| C1 | 84.5 | 84.6 | 76.5 | **57.7** | - |
| 4B-E | 85.2 | 82.9 | 76.1 | 58.9 | - |

- The 1-2K bin is pg_dev plus manifesto. Without them, the 512-1K bin is 81.6 vs 81.2, and only 26 rows are 1-2K (C1 50.0).
- Inside pg_dev, length is not monotonic: 256-512 tokens 73.0, 512-1K 60.8, 1-2K 64.1.
- **Dev cannot measure long documents:** its longest prompt is 2,290 tokens.

### 4.6 Negation and relation consistency
- Yes/no accuracy by negation cues in the question:
  - 0 cues: 84.6 vs 84.3
  - 1 cue: 86.0 vs 85.0
  - 2+ cues: 85.1 vs 84.2
- Dev negation does not hurt C1, but dev's negated wordings come from the same template families as training. Dneg is 92% one template.

Relation violations (C1 vs 4B-E):

| Relation | Pairs | C1 violations | 4B-E violations |
|---|---|---|---|
| Complement (aff vs neg must differ) | 1,122 | **3.3%** | 4.6% |
| Equivalence (aff vs dneg / para must agree) | 722 | **8.9%** | 5.7% |
| Invariance (claim injection) | 500 | 1.8% | 1.8% |

- Equivalence violations are driven by **hate**: 32 of 60 pairs (53.3%) vs 2 of 60 (3.3%).
  - Example: "Can we conclude ... contains hate speech?" against "Should the statement that the tweet does not contain hate speech be rejected?"
- On unseen sources, equivalence violations are 4.2-6.0% for C1 vs 5.1-8.0% for 4B-E.

### 4.7 Abstain, ordinal, format, card, calibration
- **Gold = NEI:** 32 rows; C1 59.4 vs 62.5.
- **Gold = "none of these":** 19 rows; C1 52.6 vs 57.9.
- Wrong-direction abstains are rare: 31 choice errors chose an abstain option when gold was a content label, and 32 did the opposite.
- **Ordinal options:** 157 rows (tb, pg, hard); C1 **51.6** vs 48.4. 58% of the 76 ordinal errors are off by one level.
- Formats (C1 vs 4B-E):

  | Format | Rows | C1 | 4B-E |
  |---|---|---|---|
  | dialogue (empathetic, pg_temporal) | 167 | 54.5 | 58.7 |
  | key-value | 390 | 66.2 | 66.2 |
  | table | 199 | 66.8 | 62.8 |
  | bullets | 153 | 67.3 | 67.3 |
  | email | 137 | 69.3 | 71.5 |
  | JSON | 170 | 81.8 | 80.6 |
  | prose | 6,903 | 84.0 | 83.1 |
  | code-like (pg_evidence, pg_numeric) | 21 | 38.1 | 57.1 |

  Every non-prose format is confounded with pg / hard sources.
- **Card vs no card:** 82.6 vs 79.6. This is confounded: the no-card rows are intent, ag_news and emotion. For clinc / banking choice rows without a card, C1 is 90.8-94.7.
- **Opaque codes:** 211 rows; 82.0 vs 80.1.
- **Position bias:** none. For 3-9 options, C1 picks the first option 22.9% of the time; the gold is first 22.0% of the time.
- **Calibration:**

  | Top probability | Rows | Accuracy | Mean confidence |
  |---|---|---|---|
  | 0.7-0.9 | 2,468 | 76.9 | 81.8 (slightly over-confident) |
  | 0.9-0.99 | 4,006 | 96.0 | 94.1 |

  - No error has confidence above 0.99.
  - Yes/no Brier: 0.1096 vs 0.1144.
- **Disagreement:** C1 right and 4B-E wrong on 416 rows; the reverse on 359; both wrong on 1,154. Most errors are shared, so they are data gaps, not C1 regressions.

---

## 5. C1's weakest decision primitives (ranked)

| # | Primitive | Dev evidence (C1 vs 4B-E) | Training share now | Likely cause |
|---|---|---|---|---|
| 1 | Rule-chain arithmetic: money or quantity after amendments, caps and exceptions | pg_numeric 51.3 vs 52.7 (choice 42.9) | pg_numeric 404 rows; generators 11.5K but mostly date / threshold checks | few multi-step computations with competing rules |
| 2 | Multi-hop record chains (supersede, rename, merge notices) | pg_multihop 55.3 vs 66.7 (**-11.3**) | 396 rows (pg) + 152 (proc) | C1 lost 4B-E's skill; very little data |
| 3 | Policy precedence and amendments | pg_policy 73.3 vs 84.0 (**-10.7**) | policy/rule 12% in volume, but pg_policy-style 371 rows | same as above |
| 4 | Fine-grained label taxonomies (20-60 near-synonym labels) | 21+ options 53.4 vs 57.5; manifesto 42.9; empathetic 45.5 (**-9.8**) | about 0 rows of this kind | code-book taxonomies only |
| 5 | Emotion and affect | 58.0; 6-way emotion choice 47.0 | 0.31% | near-zero data |
| 6 | Ordinal level choice | 51.6 vs 48.4; 58% off by one | 4.2% | few ordinal rows with sharp, adjacent-level definitions |
| 7 | Abstain as the right answer (NEI, none of these) | 59.4 / 52.6 (n=32 / 19) | gold NEI 3.5% of choice; yes/no cannot abstain | under-trained abstain gold |
| 8 | Hate / offensive yes/no and its double negation | hate yes/no 64.4; aff-dneg flips 53% | moderation 4.3%; dneg 0.22%; neg role 91% one template | narrow negation wording; noisy hate labels |
| 9 | Probability / risk judgment | pg_evidence 64.7 vs 68.7 | 0.17% | near-zero data |
| 10 | Answer "no" correctly in familiar families | seen sources, gold no: 80.4 vs 85.4; tb yes/no 84.7 vs 89.4 | label-check yes/no 22% of yes/no | yes drift; lost REF-lineage skill (tb_mixtral is barred) |

Measured outside dev (from the task brief, consistent with the gaps above):

| Measurement | Result | Gap it matches |
|---|---|---|
| JevBench hard yes/no | C1 47.4 vs 4B-E 57.9 | #8 |
| Double-negation flip rate | 8.9% | #8 |
| ejs-5 commit decisions | C1 54.1 vs Jev 58.5 | zero code / commit data |
| LongBench v2 (est.) | about 41 vs Jev 52.8 (withdrawn) | 0.4% of data over 2K tokens |

---

## 6. What this means for C's dataset

These are suggestions for the data spec; quotas are the spec owner's call. Each one maps to a PLAN family.

1. **Long documents** (PLAN: long documents).
   - Move from 0.4% to at least 8-10% of new rows at 2K-8K tokens. Cover 2K-4K, 4K-6K and 6K-8K evenly.
   - Put the deciding fact at varied depths, with several distractor sections.
   - Today, no row is near the 8K budget.
2. **Negated / hard yes/no with natural wording** (PLAN: hard / negated yes/no).
   - Retire the single `Is it wrong to answer` template as the main negation source.
   - Write hundreds of natural templates: rule out, reject, deny, fail to, cannot, "not ... unless", "no fewer than", modal and scope negation.
   - Pair every item as complement and equivalence twins.
   - Target at least 5% of new yes/no rows with 2+ negations (today 1.35%), spread across all task types. Today 9 of 20 types have negated questions in under 1% of rows.
3. **Jev-index types at near zero.**
   - Emotion, stance, ABSA, sarcasm, risk / forecast and tool selection should each get several thousand rows, from commercial-licence public training splits plus own items.
   - Add fine-grained taxonomies with 20-60 near-synonym labels, both with and without codes.
4. **Rule-chain arithmetic, multi-hop record chains and precedence** (PLAN: rule / policy composition, state tracking, table / fact).
   - These are the largest dev error mass (pg_dev holds 24% of C1's errors), and C1 regressed on two of them.
   - Program labels make them cheap to scale. Keep the answer arithmetic exact and vary record formats.
5. **Ordinal judgment** with adjacent-level definitions that differ in one stated criterion. Test off-by-one directly.
6. **Abstain as gold.** Raise gold NEI or "none of these" to about 10% of new choice rows, and add "not enough information" yes/no variants (for example, "Can it be determined that ...?").
7. **Format variety.**
   - Give each family 20+ instruction wordings.
   - Make 15-25% of rows card-free or short-card (today 4%) and lower the share of opaque codes.
   - Add JSON, HTML, email threads, logs, CSV, code and diffs (the commit family, never n8n).
   - Do not grow the label-check yes/no form.
8. **Seen-family "no" answers.** Keep yes and no balanced within each wording and each family, not only globally. The 60% replay should keep the intent and taxonomy families where C1 drifts toward "yes".

---

## 7. Dev-suite blind spots (fix in the sealed new-domains suite)

- **No long inputs:** the dev maximum is 2,290 tokens.
- **Missing task types:** no tools / function calling, stance, ABSA, commonsense, knowledge MC, code or commit rows.
- **Narrow double negation:** 833 of 904 dneg rows use one template. Natural negation is under-measured.
- **Familiar sources:** 4,296 of 8,143 dev rows (53%) come from sources or families that C1 or 4B-E trained on, including clinc150, banking77, hate, tb, pg and hard. This is why dev gains (+0.7 overall, +2.5 on unseen sources) did not transfer to ejs-5 (-4.4 vs Jev).
- **Small abstain buckets:** gold-NEI and "none of these" buckets are small (32 and 19 rows).

---

## 8. Caveats

- Task-type and domain labels are a hand mapping, one primary type per source (`local_gaps_scripts/maps.py`). Some sources span two types.
- Negation, format, NEI and "close option" flags come from regexes and are approximate. For example, the code flag fires on code inside chat-judging conversations.
- The "natural vs label-check" yes/no split is a regex on the question's last line.
- Prompt tokens add about 12 chat-template tokens to the rendered prompt and system prompt. They do not include padding.
- Dev results pool both halves and use 2,000 bootstrap draws. They are for diagnosis only, not a gate verdict. Most per-source intervals are wide.
- The scripts in `local_gaps_scripts/` were run from the session scratchpad. Their paths point there, so edit `SP` before re-running.
