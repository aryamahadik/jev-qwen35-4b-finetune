# F7 nested negation: coverage checklist

**Confirmed.** We did the web research before writing any F7 question, in two passes:
1. Datasets and taxonomies.
2. What kind of training data actually works.

The research covered the strongest negation benchmarks: ScoNe, CONDAQA, NaN-NLI, This-is-not-a-Dataset, CheckList,
MoNLI, BLiMP, IMPPRES, Thunder-NUBench, NegBench and NeQA. It also covered the 2025-2026 negation papers. This file
turns that research into a contract with four parts:
1. Every phenomenon F7 must cover.
2. The build rules.
3. The numbers to hit.
4. The audit that checks the built files.

We take design ideas only. No benchmark item, sentence or frame is copied. **Every example below is invented.**

**Why F7 exists.** The 4B model drops one negation in double- and triple-negated questions. It answers them as if they
had only one negation.

**Note.** SPEC §5 still describes the old F7 (`gen3_norm_action`). The owner must update that row. SPEC rules
(§4.2 unit size, §4.6 balance, §4.7 banned words, §7 decontamination, §8.1 decide2) still apply to F7. Where this file
is stricter, use this file.

**How to read the items:**
- **MUST**: tied directly to our failure (losing one negation at depth 2-3), or needed to block a shortcut.
- **SHOULD**: a nearby phenomenon that makes the skill general.
- **NICE**: a small share, for stress or breadth.
- **EXCLUDE**: must never appear in a program-labelled instruction, card or option. The audit must find 0 of these.
- **P** is the base claim. "→ yes iff ..." is the gold the program computes.
- **Depth** is the number of negations that scope over P (scoping cues).
- **Distractor** is a negation that does not scope over P.

---

## 1. Phenomenon checklist

### A. Depth and stacking (the failure itself)

1. **Depth-0 anchor** (MUST). The question has no negation. Every ladder is built around it.
   - Example: "Does the message ask for a refund?" → yes iff it asks for a refund.
2. **Depth 1, clausal "not" inside a statement-evaluation frame** (MUST).
   - Example: "Is this statement true: the message does not ask for a refund?" → yes iff it does not.
3. **Depth 1, truth-value frame** (MUST). Frames: false, untrue, "it is not the case that", unsupported, unfounded.
   - Example: "Is it false that the review mentions the battery?" → yes iff the review does not mention it.
4. **Depth 1, flip by a lexical verb only, with no negation word** (MUST). Verbs: refute, reject, deny, dispute,
   dismiss, contradict, fail.
   - Example: "Does the text refute the summary 'the caller wants to close the account'?" → yes iff the caller does
     not want to close it. The card states that the text settles the claim.
5. **Depth 1, affixal negation on a binary label defined in the card** (MUST). Affixes: non-, un-, in-/im-/il-/ir-,
   dis-, -less, -free.
   - Example: card "- urgent: names a deadline within 48 hours. - non-urgent: every other message." Q: "Does
     'non-urgent' fit the message?" → yes iff the message is not urgent.
6. **Depth 2, cancelling, two different cue classes** (MUST).
   - Example: "Should the reviewer dismiss the claim that the email does not mention a deadline?" → yes iff the email
     mentions a deadline.
7. **Depth 2, the same cue class twice** (SHOULD). This stops "two of the same kind" from being treated as special.
   - Example: "Is it untrue that the post is unsafe?" → yes iff the post is safe.
8. **Depth 3, mixed classes** (MUST). Also include combinations where one class repeats.
   - Example: "Is the note 'the message does not lack an order number' unsupported by the text?" → yes iff the
     message has no order number.
9. **Depth 4, stress test** (NICE, at most 3% of rows).
   - Example: "Is it false that the text fails to show that the sender is not unverified?" → yes iff the sender is
     verified.
10. **Attributed or embedded claim, where the outer verb applies to a clause that is itself negated** (MUST). This is
    our failure's structure, but in different words.
    - Example: "A log line states that the caller did not give an account number. Does the call transcript
      contradict that log line?" → yes iff the caller gave an account number.
11. **Negations split between the card and the question** (MUST).
    - Example: card "- hold: the order is not ready to ship." Q: "Is it false that 'hold' applies to this order?" →
      yes iff the order is ready to ship.
12. **Cross-sentence or distant negator** (MUST). The negator sits in a different sentence or field from the claim.
    Cover these distance bins: same clause, same sentence, the next sentence, 2 or more sentences away, another field
    (the card).
    - Example: "Answer about the reverse of the claim that follows. Claim: the reviewer liked the screen. Does the
      review back that reverse?" → yes iff the reviewer did not like the screen.
13. **Negation in the answer mapping inside the instruction** (MUST). Compound negation in instructions is the worst
    case in the literature.
    - Example: "Answer no if the review does not mention delivery; otherwise answer yes." → yes iff the review
      mentions delivery.
14. **Inverted yes/no key in the card** (SHOULD, at most 10% of rows).
    - Example: card "- yes: the claim fails for this text. - no: the claim holds." Q: "Claim: the message asks for a
      refund." → yes iff there is no refund request.

### B. Distractor negation (present, but does not change the answer)

15. **Non-scoping negation in a side clause of the question** (MUST).
    - Example: "Whether or not the sender sounds polite, does the message ask for a refund?" → yes iff it asks for a
      refund.
16. **One scoping negation plus one distractor** (MUST). Also build 2 + 1 and 3 + 1. Counting the cues gives the
    wrong answer here.
    - Example: "Whether or not the sender sounds polite, is it false that the message asks for a refund?" → yes iff
      there is no refund request. There are 2 cues, but only 1 scopes.
17. **Two distractors, no scoping negation** (SHOULD).
    - Example: "Even if no order number is given, and whether or not the tone is calm, does the message ask for a
      refund?" → yes iff it asks for a refund.
18. **Distractor negation in a card line that does not decide the answer** (SHOULD).
    - Example: card "- billing: the message is about a charge. - other: the message fits none of the lines above." Q:
      "Does 'billing' fit the message?" → yes iff the gold label is billing.
19. **Negation inside the real state text** (SHOULD). This is a balance rule, not a rung. Never assume that a negation
    in the text is a distractor.
    - Example: state "Still haven't got the new card, and nobody picks up the phone." The yes share must be the same
      for states with and without negation.
20. **Negation lookalikes** (SHOULD). Some words look like negations but are not:
    - pseudo-affixes: under, universal, discuss, interest, display, nonetheless, notable;
    - fixed phrases with no/not that do not deny: "not only X but also Y" asserts X, "nothing but" means only.

    These break cue counters.
    - Example: "Under the listed definitions, does the message discuss an interest charge?" → yes iff it does. No
      word here is a negation.

### C. Labels and cards (card-format ladders over real texts)

21. **"Not X" is not the same as the antonym in label sets of 3 or more** (MUST).
    - Example: labels positive / neutral / negative. "Is it true that the review is not negative?" → yes iff the gold
      label is positive or neutral. A neutral review gets yes here but no for "is it positive".
22. **Complement or residual labels** (MUST): other, "neither A nor B", "none of the listed".
    - Example: card "- other: the message is about neither cards nor transfers." Q: "Does 'other' fit the message?" →
      yes iff the gold label is neither of those.
23. **Exclusion clause in a definition, combined with a negated question** (SHOULD).
    - Example: card "- account issue: any account topic except a password reset." Q: "Is it false that 'account
      issue' fits the message?" → yes iff the message is not an account topic, or is a password reset.
24. **"Only" with negation** (MUST). The card states that exactly one label fits.
    - Example: "Is it false that 'card delivery' is the only listed label that fits the message?" → yes iff the gold
      label is not 'card delivery'.
25. **Negation over a broader term that the card spells out as a list** (NICE).
    - Example: card "- payment problem: a declined card, a failed transfer or a wrong charge." Q: "Is it true that
      the message describes no payment problem?" → yes iff the gold label is none of the three.

### D. Quantifiers, numbers and coordination (multi-text states built from several real labelled texts)

26. **"Not all", "none", "not every", "not a single"** (SHOULD). The card says that quantifiers are read logically.
    - Example: "Is it true that not all four reviews are positive?" → yes iff at least one is not positive.
27. **"Only" over a set whose members are negated, plus an outer negation** (MUST). This is our failure's structure in
    new words.
    - Example: "Is it false that the thread contains only non-toxic posts?" → yes iff at least one post is toxic.
28. **Numeric bounds with negation** (SHOULD): "no more than", "not fewer than", "at most". Include exact boundaries.
    - Example: "Is it false that no more than two of the five messages ask for a refund?" → yes iff three or more do.
29. **Approximate negators, with a number fixed by the card, contrasted with "none"** (NICE).
    - Example: card "few = at most one." Q: "Are few of the four reviews negative?" → yes iff zero or one is
      negative.
30. **De Morgan and coordination** (SHOULD): "not both", "neither ... nor", "not (A or B)".
    - Example: "Is it false that both messages ask for a refund?" → yes iff at least one does not.
31. **Exceptors** (SHOULD): other than, apart from, besides.
    - Example: "Is any review other than the second one positive?" → yes iff review 1, 3 or 4 is positive.
32. **Contrastive negation, "not X but Y"** (SHOULD).
    - Example: "Is it true that the best label is not 'card arrival' but 'card delivery estimate'?" → yes iff the
      gold label is 'card delivery estimate'.

### E. Modality, conditionals and attitude verbs

33. **"Must not" vs "need not" vs "cannot"** (SHOULD). Pair each "need not" rule with a "must not" rule so that both
    appear with both answers.
    - Example: card "Messages labelled 'complaint' must be answered; other messages need not be." Q: "Under the card,
      may the agent leave this message unanswered?" → yes iff the message is not a complaint.
34. **"Unless", "not unless", "only if", "if not"** (SHOULD).
    - Example: card "- escalate: applies unless the best label is 'small talk'." Q: "Is it false that 'escalate'
      applies?" → yes iff the gold label is 'small talk'.
35. **Scope edit with a non-factive verb: "does not claim P" vs "claims not-P"** (SHOULD). The two come apart when the
    record says nothing about P.
    - Example: state note "Triage note: topic = delivery." Q-a: "Does the triage note claim that the customer is not
      asking for a refund?" → no. Q-b: "Is it true that the triage note makes no claim that the customer is asking for
      a refund?" → yes.

### F. Question and option form

36. **Choice rows with negated selection** (MUST): "which ... does not", "which statement is false".
    - Example: gold label 'card arrival'. "Which statement about the message is false? A) 'card arrival' fits it
      B) 'refund request' does not fit it C) 'exchange rate' fits it" → C.
37. **Choice decoys: antonym vs exact negation** (SHOULD).
    - Example: a neutral review. "Which statement is true of this review? A) it is negative B) it is not positive
      C) it is positive" → B.
38. **Inner-negative polar question, always with full yes/no card lines** (SHOULD, at most 5%).
    - Example: card "- yes: the message does not mention a refund. - no: the message mentions a refund." Q: "Does the
      message not mention a refund?" → yes iff there is no mention.

### X. EXCLUDE: never in a program-labelled instruction, card or option (the audit must find 0)

| # | Construction | Invented example | Why it is excluded |
|---|---|---|---|
| X1 | Outer negative question | "Doesn't the message ask for a refund?" | The answer is biased toward yes, and "no" is ambiguous |
| X2 | Litotes on a gradable word | "Is the reviewer not unhappy?" | Weaker than "happy", so there is no determinate gold. Binary card labels ("not non-toxic") are allowed |
| X3 | Metalinguistic negation | "The food was not good, it was superb." | Denies the word choice, not the fact |
| X4 | "may not" / "might not" | "The agent may not close the ticket." | Could mean forbidden or possible |
| X5 | "all ... not" | "All the messages don't mention a refund." | Could mean none or not all |
| X6 | Neg-raising verb | "The caller doesn't think the charge is valid." | Pragmatic reading, not literal |
| X7 | Factive verb under negation | "The agent did not notice that the card had expired." | It presupposes P, so it would leak the gold |
| X8 | Negative concord | "I didn't get no refund." | One negation in meaning. It may appear in the real state text, but it is never counted as two cues |
| X9 | Free focus | "The bank did not refund me on Monday." | No refund at all, or a refund on another day? |
| X10 | Reading that depends on implicature | "Not all reviews praise it" read as "some do" | Only "some do not" is entailed. Item 26 with a logic line in the card is fine |
| X11 | Expletive negation and idioms | "No wonder the card was declined." "Can't help but complain." | No real negation |
| X12 | Ill-formed stacks, unlicensed NPIs | "Is it not untrue that the post is not non-toxic?"; "The message mentions any refund." | Unreadable or ungrammatical |

---

## 2. Design rules

1. **Logical form first, gold by program.**
   - Build every question from a typed logical-form tree, for example `FALSE(CLAIM(NOT(LACK(P))))`.
   - Gold is that tree evaluated on truth(P). The surface text is rendered from the tree.
   - **Never compute gold by counting words in the surface text.**
   - Every cue node records its lexeme, class, position, whether it scopes, and its distance to the claim.
   - An independent decide2 (SPEC §8.1), written by an agent that never read the generator, parses the text back.
     The target is 100% agreement. More than 1% disagreement is a generator bug: fix the generator, do not filter
     rows.
2. **The ladder is one unit.**
   - A ladder is one `call_id` with at most 5 rows (SPEC §4.2), and at most 3 rows when a state is over 6K characters
     (SPEC §4.9). All its rows share a byte-identical state.
   - Rung menu:
     - `R0`: the anchor, with no cue;
     - `N1`-`N4`: scoping depth 1-4;
     - `D`: a distractor rung. It carries 1 or more distractors, and its gold is the same as its no-distractor twin;
     - `AR`: an affirmative rewrite. It has no cue word and the same gold as an odd-depth rung, for example by
       using the complement label;
     - `CH`: a choice row.
   - `R0` is in at least 80% of train ladders and in 100% of dev ladders. The other rungs are sampled so that the
     family totals in section 3 are met.
   - Relations come from parity: `equiv` for the same gold function, `complement` for the opposite. No row has more
     than 1 complement relation.
   - Every ladder has at least one yes row and one no row.
3. **Card-format ladders are at least 50%.**
   - They use real classification texts with human gold, under the F4(a) eligibility rules.
   - Exclude every source that appears in any dev split. Today these are clinc150, banking77, std_hate, gd_ghc_hate
     and tb_label_nli. **Re-derive this list by program at build time.**
   - P is "this text's gold label is L", or a statement about label membership as the card defines it.
   - truth(P) is balanced per quoted label.
   - Quantifier items (26-31) use multi-text states built from 3-5 real labelled texts.
   - The remaining ladders use program-written records, where P is known by construction.
4. **The yes/no lines restate the question in full.**
   - Each yes/no card line repeats the question as a statement, with the **same cues**. It never gives a simplified
     form: "yes: the post is non-toxic" would give away the composition.
   - Card-less rows are allowed only for "Is it true/false that ..." frames. Their share must be the same at every
     depth and for both golds, within ±2 points.
5. **Distractors must be provably non-scoping.**
   - The program deletes each distractor node from the logical form, re-evaluates, and asserts that the gold is
     unchanged.
   - Distractor clauses must never presuppose something about the text that could be false. Use "whether or not",
     "even if", "regardless of whether", or instructions about format.
   - Distractors appear at every depth from 0 to 3.
6. **No shortcut may predict the answer.** The audit in section 4 checks each one:
   - counting cues, or their parity;
   - "has a negation, so flip" or "has a negation, so no";
   - outer-only or inner-only reading;
   - a cue word, a frame or the depth predicting gold;
   - letter position, option length, question length, card style.

   No single cue word may tell you the parity: for every lexeme, the share of its rows with odd parity is 40-60%.
7. **Scope variety.** Spread the cues over these positions:
   - the outer frame;
   - the inner claim;
   - the card label definition;
   - the yes/no key;
   - the answer mapping;
   - a separate sentence;
   - the choice options;
   - the state text (distractor only).

   Also vary the clause-embedding depth from 0 to 3, and the distance bins in item 12.
8. **Cue variety beats volume.**
   - Use a fixed, curated lexicon file with at least 60 train lexemes across 5 classes: syntactic, affixal, lexical,
     truth-value frame, and cross-sentence or answer-mapping.
   - The generator draws cues only from this file. **The LLM never picks negation words freely.**
   - Vary inflections (fails / failed / failing).
9. **Frame diversity.**
   - Use at least 12 frame families, with at least 4 frames each, in train.
   - No frame is over 4% of rows, and no carrier sentence is over 3%.
   - Vary the order (question first or claim first), the register and the punctuation.
   - Use the state formats in SPEC §4.3.
10. **Held out for the probe (dev_holdout only):**
    - 3 frame families;
    - at least 20% of lexemes, with at least 1 from each class;
    - 2 cue-class combinations at depth 3 that never occur together in train;
    - at least 2 whole eligible sources.

    Also build a **devx** of at least 100 rows. It is written blind by an agent who never read the F7 renderers
    (SPEC §6).
11. **Natural English only.**
    - At most 1 affix per word and at most 2 cues per clause.
    - Every row must read like something a careful person would write.
    - Drop any render that the parse-back cannot read.
12. **Bivalence is stated.** Frames such as refute, unsupported or "fails to show" assume the material settles P.
    The card says so, for example: "The text settles every claim asked about here."
13. **Decontamination.**
    - Run all SPEC §7 checks.
    - Run a 6-word-run ban against the frames of the public negation benchmarks.
    - Run a 6-word-run ban against the measured-failure question frame.
    - Apply the §4.7 banned judge words: right, wrong, correct, incorrect, accurate, inaccurate, mistaken, reply,
      agreed, disagree, undercut, debate.
    - The benchmark files sit in a decontam-only folder. The generator never reads them.
14. **Training placement.**
    - All rungs share one `call_id`, so they land in one micro-batch, and the relations feed the existing pair loss.
    - Mix all depths from the start. **No curriculum.**

---

## 3. Quantitative targets

**Size.** This is an estimate from the research, not a measured number.
- Plan about 2,500 train ladders, which is about 11-12K rows. The research range is 10-25K rows for a 4B model.
- If the owner sets a smaller budget, never go below 1,000 ladders (about 4.5K rows). Cut NICE items first, then cut
  SHOULD items down to their floors. MUST floors stay.

**Floors per phenomenon** (rows tagged with the item; one row can carry several tags):

| Priority | Train rows | Dev rows (iid + holdout) | Of which holdout |
|---|---|---|---|
| MUST | ≥ 400 (≥ 200 at the 1,000-ladder minimum) | ≥ 40 | ≥ 20 |
| SHOULD | ≥ 150 (≥ 75 at minimum) | ≥ 20 | ≥ 10 |
| NICE | ≥ 40 (0 allowed at minimum) | ≥ 10 | ≥ 5 |
| EXCLUDE | 0 in instructions, cards and options | 0 | 0 |

**Depth mix** (scoping depth, share of rows):

| Depth 0 | Depth 1 | Depth 2 | Depth 3 | Depth 4 |
|---|---|---|---|---|
| 18% | 25% | 30% | 24% | ≤ 3% |

This puts odd and even parity at about 50/50.

**Balance:**

| What | Target |
|---|---|
| Yes share in each (scoping depth × total cue count) cell and in each rung | 48-52% |
| Yes share in every other stratum: SPEC §4.6 strata plus cue class, cue position, cue lexeme, frame family, frame, source, quoted label, card style, length bin, state-has-negation | 45-55% |
| truth(P) per rung and per depth | 48-52% |
| truth(P) per quoted label | 45-55% |
| Choice rows | 20% ± 3 of rows. Option count 3-5. Gold uniform over positions, ± 3 points per position for each option count. Negated selection in 50% of choice rows |

**Distractors and parity:**

| What | Target |
|---|---|
| Rows with at least 1 distractor | ≥ 35% overall, and ≥ 25% within each depth 0-3 |
| Rows where the parity of all cues ≠ the parity of scoping cues (odd number of distractors or lookalikes) | ≥ 30% |
| AR rows (a flip with no cue word) plus lexical-only flips | ≥ 15% of odd-parity rows |

**Cue mix** (share of cue tokens):

| Class | Share |
|---|---|
| Syntactic | 25-35% |
| Affixal | 20-30% |
| Lexical / verb | 20-30% |
| Truth-value frames | 10-15% |
| Cross-sentence + answer mapping | 5-10% |

Further limits on cue words:
- "not" and "n't" together are at most 20% of cue tokens. No single lexeme is over 10%.
- Each train lexeme appears in at least 30 rows.
- For every lexeme, the share of its rows with odd parity is 40-60%.
- A lexeme that can serve as a distractor does so in at least 10% of its uses.

**Cue positions** (share of scoping cue tokens):

| Position | Share |
|---|---|
| Inner claim | 25-35% |
| Outer frame | 20-30% |
| Card definitions | 15-25% |
| Separate sentence | 5-10% |
| Answer key / mapping | 5-10% |
| Choice options | 5-10% |

**Ladder types:** at least 50% card-format over real texts; 10-20% multi-text (quantifier) ladders; the rest are
program-written records.

**Frames and lexicon:**
- Train: at least 12 families × 4 frames and at least 60 lexemes.
- Held out: 3 families and at least 15 lexemes.
- No frame over 4% of rows, and no carrier sentence over 3%.

**Dev:**
- At least 150 iid ladders and at least 150 holdout ladders, which is about 1,300 rows or more.
- At least 200 rows per depth 0-3 across iid and holdout, and at least 40 rows at depth 4.
- devx: at least 100 blind-written rows.
- Dev states are group-disjoint from train.

---

## 4. Audit procedure (run on the built files before ship)

Suggested program: `yn2b/f7_precheck.py`, which writes `yn2b/f7_precheck.json`. Every check prints a number and a
pass/fail. **Ship only if all pass.**

1. **Schema.** Every row must carry these fields (the builder may rename them):
   - `ladder_id`, `rung`, `lf`;
   - `truth_P`, `depth`, `n_cues`, `n_distractor`;
   - `cues[]`: lexeme, class, position, scoping, distance;
   - `phen[]`: checklist ids;
   - `frame_family`, `frame_id`, `ladder_kind`, `source`, `dev_kind`.

   Any missing field fails the check.
2. **Gold.**
   - Re-evaluate `lf` on `truth_P`. It must equal gold on 100% of rows.
   - Distractor test: delete each distractor node and re-evaluate. Gold must be unchanged on 100% of rows.
   - Run the independent decide2 parse-back: target 100%. Read every disagreement. More than 1% is a generator bug.
3. **Coverage.**
   - Count the rows for each checklist item against the section 3 floors.
   - Count rows in each cell of depth × cue position × cue class. Every allowed cell at depth ≤ 3 must have at least
     30 rows.
   - Count rows per lexeme, frame and family.
   - List any item below its floor.
4. **Balance.** Check every target in section 3: yes share per cell and stratum, truth(P) per rung, depth and label,
   choice gold position, and card style per depth and gold.
5. **Surface shortcut probes.** These read only the instruction, card and options, never the state or truth(P).
   Use 5-fold CV split by ladder.
   - Probes:
     - (a) always yes, and always no;
     - (b) any cue → no, and any cue → yes;
     - (c) "not" present → no;
     - (d) even cue count → yes, with the narrow lexicon (not / n't / no / never / none);
     - (e) the same as (d), with the full F7 lexicon;
     - (f) per-lexeme majority;
     - (g) per-frame and per-template majority;
     - (h) logistic regression on bag-of-words and bigrams;
     - (i) logistic regression on length and count features;
     - (j) for choice rows: position majority, longest option, option with the most or fewest cues, option with the
       most word overlap with the question.
   - **Pass:** each probe is at most 55% overall, and at most 60% in any stratum with 100 or more rows.
   - Also |r| < 0.05 between gold and each of: cue count, cue-count parity, has "not", has an affix, has a lexical
     cue, has a distractor, card style, length bin, and choice gold position.
6. **Composition probes.** These use the program's truth(P) to test whether the data rewards a wrong rule.

   | Probe | Rule | Pass |
   |---|---|---|
   | C1 ignore negation | gold = truth(P) | 45-55% |
   | C2 count all cues | truth(P) XOR parity of all cues | ≤ 70% overall, ≤ 75% at any depth |
   | C3 count syntactic cues only | truth(P) XOR parity of the syntactic cues | ≤ 65% |
   | C4 outer cue only | truth(P) XOR (outermost cue present) | ≤ 60% |
   | C5 inner cue only | truth(P) XOR (a cue inside the claim clause) | ≤ 60% |
   | C6 ignore one class | drop all affixal, or all lexical, or all cross-sentence cues | ≤ 60% each |
   | C7 antonym reading | read "not L" as the antonym label (item 21) | wrong on ≥ 30% of item-21 rows |
   | Cue share | for each lexeme with 30 or more rows, the share of its rows with odd parity | 40-60% |

7. **EXCLUDE scan.**
   - Run a regex list for X1-X12 over the instructions, cards and options. The list includes a gradable-predicate
     list for litotes, "may not", "all ... n't", "don't think/believe/expect", the factive verbs, "Isn't / Doesn't /
     Don't / Aren't" at the start of a question, and "n't ... no/nothing/nobody".
   - Must find 0 hits. The state text is exempt, but its hits are tagged.
8. **Decontamination.**
   - Run SPEC §7 (`check_yn2b.py`).
   - Run the 6-word-run ban against the public negation-benchmark frames and the measured-failure frame.
   - Check the §4.7 banned words.
   - Print counts only. Any hit drops the whole ladder.
9. **Ladder integrity.**
   - Every ladder has an identical state across its rows.
   - Every ladder has at most 5 rows (at most 3 when a state is over 6K characters).
   - Relations match parity, with at most 1 complement per row.
   - The `R0` share meets its target.
   - Every ladder has both golds.
10. **Hold-out integrity.**
    - Held-out lexemes (with inflections), frames, families, cue combinations and sources appear in 0 train rows.
    - Holdout and devx states share at most 20% of their 12-grams with train (SPEC §7.6).
    - No iid dev state equals a train state.
11. **Blind read.**
    - An agent who did not write the generator reads 100 random rows plus 10 rows per MUST item.
    - It marks each row as wrong gold, unreadable, or ambiguous.
    - Any wrong gold is a bug. Unreadable plus ambiguous rows must be at most 3%; above that, rework the frame.

**After training: model readout on F7 dev** (iid, holdout and devx reported separately):
- Accuracy per rung and per depth.
- Ladder consistency: the share of ladders where every row is right.
- Flip accuracy, counted only on ladders where `R0` is right.
- Accuracy per cue class, cue position and distance bin.
- Distractor rows vs matched rows without a distractor.
- Comparison against the C1, C2 and drop-one-negation baselines.
- The iid → holdout gap and the iid → devx gap.
- Regression check on the other families and the main dev sets.

The pass bar is the owner's call. Suggested bar:
- depth-2 and depth-3 accuracy within 5 points of depth-0 accuracy on the same ladders;
- a holdout gap of at most 5 points.

---

## 5. Research gaps

- No paper measures the "an odd number of negations means flip" shortcut directly. That is why C2 and C3 exist.
- No paper tests a curriculum that orders items by depth, so we mix all depths from the start.
- The data-size numbers come from other models and setups.

## 6. Sources

- ScoNe: aclanthology.org/2023.acl-short.154; arxiv.org/pdf/2305.19426
- CONDAQA: arxiv.org/abs/2211.00295
- NaN-NLI: arxiv.org/abs/2210.03256
- This is not a Dataset: aclanthology.org/2023.emnlp-main.531; arxiv.org/pdf/2310.15941
- Negation Neglect: arxiv.org/abs/2605.13829
- Affixal negation (NegCue): arxiv.org/abs/2609.13685
- Negation taxonomy: arxiv.org/abs/2507.22337; arxiv.org/html/2507.12782
- Thunder-NUBench: arxiv.org/abs/2506.14397
- Negated-prompt bias: arxiv.org/abs/2605.03052; aclanthology.org/2025.emnlp-main.1088
- Compound negation in instructions: arxiv.org/abs/2601.21433
- Distractor negation: aclanthology.org/2025.findings-emnlp.761
- PairCFR: arxiv.org/html/2406.06633v1
- Consistency fine-tuning: arxiv.org/html/2412.16100
- Affirmative rewrite: arxiv.org/html/2406.07492v1
- Depth: arxiv.org/pdf/2510.15990
- MoNLI: aclanthology.org/2020.blackboxnlp-1.16
- BLiMP: arxiv.org/abs/1912.00582
- IMPPRES: aclanthology.org/2020.acl-main.768
- *SEM 2012: aclanthology.org/S12-1035
- CheckList: arxiv.org/abs/2005.04118
- Contrast sets: arxiv.org/abs/2004.02709
- NeQA: arxiv.org/abs/2209.12711
- Yes/no bias: arxiv.org/abs/2408.00137
- Prompt-format sensitivity: arxiv.org/pdf/2310.11324
- Relative consistency: arxiv.org/pdf/2310.13781
