# G-block task-card admission (PREREG_FINAL A39 c)

Binding: PREREG_FINAL.md Ruling A39 (c) (G-LEX-style 2/2 Haiku extraction of each card's options) and A37 (b) (Haiku never sets a label). This step admits task cards only. No label, row or training target is created.

## Rule

A card is admitted only if BOTH independent Haiku reads (rA, rB; separate chunk files, opaque qids, own card and option order) restate EVERY option consistently with its definition AND every example text falls in the intended option under the card's definitions. Judged by program-assisted comparison (`tools/admit_cards.py compare`: completeness, exact option names, length limits, copy check, nearest definition by TF-IDF cosine for each restatement and example, and each example against the other read's restatements) plus a careful reading of every restatement and example. Lexical flags are aids, not verdicts: every card was read in full, and any doubt rejects.

Inputs: 50 lint survivors (`cards/survivors.json`), 4/4 read files returned (rA_001, rA_002, rB_001, rB_002); task-file sha256 = manifest for all 4. Program problems: none.

## Counts per domain

| Domain | Lint survivors | Admitted | yes/no | choice | Rejected | Over target (not admitted) |
|---|---|---|---|---|---|---|
| gov_news | 5 | 4 | 2 | 2 | 1 | 0 |
| learning | 5 | 4 | 2 | 2 | 0 | 1 |
| museum | 5 | 4 | 2 | 2 | 1 | 0 |
| news | 5 | 4 | 2 | 2 | 0 | 1 |
| office_help | 4 | 3 | 1 | 2 | 1 | 0 |
| open_data | 5 | 4 | 2 | 2 | 0 | 1 |
| park_programs | 5 | 4 | 2 | 2 | 0 | 1 |
| recipes | 3 | 2 | 1 | 1 | 1 | 0 |
| sci_abstracts | 4 | 4 | 2 | 2 | 0 | 0 |
| travel | 5 | 4 | 2 | 2 | 0 | 1 |
| volunteer_posts | 4 | 4 | 3 | 1 | 0 | 0 |
| **total** | 50 | 41 | 21 | 20 | 4 | 5 |

Target 2-4 admitted per domain: met in every domain.

## Admitted cards

- `gb_gov_news_1_c0` (gov_news, yes/no): Does this text ask the reader to do something? Options: *yes*, *no*
- `gb_gov_news_2_c0` (gov_news, yes/no): Could a typical resident or small business use, apply for, or attend what this release describes? Options: *yes*, *no*
- `gb_gov_news_2_c1` (gov_news, choice): Which group of readers is this release mainly written for? Options: *students and young people*, *companies and business owners*, *workers and unions*, *patients and health users*, *drivers and travellers*, *all residents*
- `gb_gov_news_3_c1` (gov_news, choice): What is the main subject of this release? Options: *money or pay*, *rules or laws*, *service or place change*, *safety warning*, *something else*
- `gb_learning_1_c0` (learning, yes/no): Should this text be sent back to its author for repair before it goes into the course library? Options: *yes*, *no*
- `gb_learning_1_c1` (learning, choice): Which kind of lesson path should this text be filed under? Options: *theory first*, *practical steps*, *real-world context*, *opinion or call to action*, *something else*
- `gb_learning_2_c1` (learning, choice): What need does this text mainly meet for a learner? Options: *quick lookup*, *explain an idea*, *study plan*, *do a task*, *something else*
- `gb_learning_3_c0` (learning, yes/no): Does this text ask the reader to solve, practice, or carry out something themselves? Options: *yes*, *no*
- `gb_museum_1_c0` (museum, yes/no): Should this item be shown on the collection's timeline page? Options: *yes*, *no*
- `gb_museum_1_c1` (museum, choice): Which kind of photo set should the team plan for the item this text describes? Options: *flat image*, *several views*, *fabric close-up*, *archive scans*, *something else*
- `gb_museum_3_c0` (museum, yes/no): Does the text say that this item is one of several works in a set, series, pair, or collection? Options: *yes*, *no*
- `gb_museum_3_c1` (museum, choice): Which kind of item does this text mainly describe? Options: *photograph*, *print or drawing*, *painting*, *ceramic or clay object*, *archive or papers*, *something else*
- `gb_news_1_c0` (news, yes/no): Is this story worth keeping in the archive as a record to look up later? Options: *yes*, *no*
- `gb_news_2_c1` (news, choice): Which kind of reader is this article most suitable for? Options: *can vote or join in*, *money at stake*, *students or parents*, *risk to safety*, *no direct stake*
- `gb_news_3_c0` (news, yes/no): Does the text name a specific day, date, or time limit for something that has not happened yet? Options: *yes*, *no*
- `gb_news_3_c1` (news, choice): What kind of thing does the text mainly describe? Options: *something that happened*, *plan or proposal*, *findings or statistics*, *dispute or demand*, *person's own account*, *something else*
- `gb_office_help_1_c0` (office_help, yes/no): Does the writer say that the program is not working as it should? Options: *yes*, *no*
- `gb_office_help_1_c1` (office_help, choice): What does the writer mainly want the helper to provide? Options: *make something work*, *build a formula*, *how to do a task*, *explain an error message*, *something else*
- `gb_office_help_3_c1` (office_help, choice): What does the poster mainly want the helper to do? Options: *show how*, *fix a fault*, *write a formula*, *request a feature*, *something else*
- `gb_open_data_1_c0` (open_data, yes/no): Should a caution that the figures are estimates or preliminary be added before quoting this dataset? Options: *yes*, *no*
- `gb_open_data_2_c1` (open_data, choice): Which need is this dataset most suitable for? Options: *find a place or service*, *follow public money*, *count or track trends*, *look up cases or properties*, *something else*
- `gb_open_data_3_c0` (open_data, yes/no): Does the text send you to another place for more details or newer data? Options: *yes*, *no*
- `gb_open_data_3_c1` (open_data, choice): Which team should look at this dataset first? Options: *land and mapping*, *money and legal filings*, *public service use*, *people and health*, *government records*, *something else*
- `gb_park_programs_1_c0` (park_programs, yes/no): Does the listing require visitors to sign up, pre-register, or book before the day? Options: *yes*, *no*
- `gb_park_programs_2_c0` (park_programs, yes/no): Is this program free to join, so it suits a visitor on a tight budget? Options: *yes*, *no*
- `gb_park_programs_2_c1` (park_programs, choice): How much physical effort does this program ask of a visitor? Options: *rough or steep ground*, *relaxed walk or tour*, *seated or indoors*, *something else*
- `gb_park_programs_3_c1` (park_programs, choice): What kind of activity does the program mainly offer? Options: *guided walk or trip*, *hands-on lesson*, *show to watch*, *festival or party*, *something else*
- `gb_recipes_3_c0` (recipes, yes/no): Does the recipe use meat, poultry, fish or seafood as an ingredient? Options: *yes*, *no*
- `gb_recipes_3_c1` (recipes, choice): What kind of food does the recipe make? Options: *main dish*, *soup or stew*, *side dish*, *bread or noodles*, *sauce or spice mix*, *drink*, *sweet treat*
- `gb_sci_abstracts_2_c0` (sci_abstracts, yes/no): Is the main new contribution of this study a computer, mathematical or theoretical model or method? Options: *yes*, *no*
- `gb_sci_abstracts_2_c1` (sci_abstracts, choice): Which group of researchers should review this study first? Options: *plants*, *people*, *microbes*, *cells or molecules*, *animals*, *something else*
- `gb_sci_abstracts_3_c0` (sci_abstracts, yes/no): Does the study involve living people or animals, as participants, patients or test subjects? Options: *yes*, *no*
- `gb_sci_abstracts_3_c1` (sci_abstracts, choice): What is the main kind of thing this study is about? Options: *people*, *animal, plant or ecosystem*, *microbe or virus*, *cell, protein or molecule*, *method or software*
- `gb_travel_1_c0` (travel, yes/no): Does this passage give a phone number, a street address, or specific opening times or a timetable? Options: *yes*, *no*
- `gb_travel_1_c1` (travel, choice): Which single topic does this passage cover most, so that it can be filed in the right section? Options: *getting there*, *what the place is like*, *sights and things to do*, *practical help*, *something else*
- `gb_travel_2_c1` (travel, choice): Which traveller need does this passage mainly meet? Options: *plan the route*, *pick things to do*, *learn the background*, *stay out of trouble*, *something else*
- `gb_travel_3_c0` (travel, yes/no): Is this passage mainly about what the place is like or what is there, rather than practical advice for the trip? Options: *yes*, *no*
- `gb_volunteer_posts_1_c0` (volunteer_posts, yes/no): Does this opportunity mean working outdoors? Options: *yes*, *no*
- `gb_volunteer_posts_2_c0` (volunteer_posts, yes/no): Is this opportunity limited to adults aged 18 or older? Options: *yes*, *no*
- `gb_volunteer_posts_2_c1` (volunteer_posts, choice): What kind of volunteer does this posting suit best? Options: *physical work*, *driving a van or truck*, *working with young people*, *speaking another language*, *professional or office skills*, *anyone, no special skill needed*
- `gb_volunteer_posts_3_c0` (volunteer_posts, yes/no): Does the posting ask the volunteer to spend time with, serve, supervise or teach the people the organisation helps? Options: *yes*, *no*

## Rejections and reasons

4 of 50 read cards were rejected after the reads.

- `gov_news_3#0` (gov_news, yes/no): Does this release say that a road, entrance, building, service or travel route will be closed, changed or disrupted, so you may need to change your plans?  
  Reason: rA's 'no' example announces a new reading garden opening at the library. The yes definition counts a building or service that is 'changed' and does not say whether an opening counts; the same authoring task's choice card treats 'opening' as a change. A careful reader could answer yes, so the example does not clearly fall in 'no'.
- `museum_2#1` (museum, choice): Who or what is this text best suited for?  
  Reason: The options mix two axes (reader level vs content) with no stated precedence. Both reads' 'something else' examples (a sculptor's retirement; how curators chose works) and rA's 'catalog record' example are in plain everyday words with no citations, so they also meet the 'casual visitor' definition; the examples do not fall in exactly one option.
- `office_help_3#0` (office_help, yes/no): Can the post be answered with steps that only use the program itself?  
  Reason: The card classifies forum posts, but both definitions describe the unseen answer. Both reads wrote solutions ('Open the Format menu...', 'You will need to download a separate add-on...') rather than posts for both options, so neither read shows that a post can be placed from its own text (authoring rule 1).
- `recipes_1#1` (recipes, choice): What is the main way this recipe is cooked?  
  Reason: Neither read's 'slow cooker' example names or clearly shows the appliance ('add ... to the pot ... leave it on low for eight hours'; 'into the pot ... set it to low'). A long simmer in a pot also meets the 'stovetop' definition (simmering in a pot), so the examples do not clearly fall in 'slow cooker'.

## Passed but not admitted (per-domain target of at most 4; reserve)

- `learning_3#1` (learning, choice): Which kind of learning material is this text mainly?  
  Reason: passed; capped: learning had 3 passing choice cards; learning_2#1 and learning_3#1 ask the same decision (look-up / explain / tasks); copied restatements tie (4 each), so the higher lint max_definition_jaccard (0.235 vs 0.167) is dropped
- `news_2#0` (news, yes/no): Does this article name a specific event, decision, or deadline that is still to come?  
  Reason: passed; capped: news had 3 passing yes/no cards; news_2#0 and news_3#0 ask the same decision (a future date or event); news_2#0 has more copied restatements (2 vs 1)
- `open_data_2#0` (open_data, yes/no): Does this dataset name the years or dates it covers, so a person can check it fits the period they need?  
  Reason: passed; capped: open_data had 3 passing yes/no cards with no same-decision pair; open_data_2#0 has the most copied restatements (2 vs 0 and 0)
- `park_programs_3#0` (park_programs, yes/no): Does the program ask the reader to pay a fee to take part?  
  Reason: passed; capped: park_programs had 3 passing yes/no cards; park_programs_2#0 (free?) and park_programs_3#0 (fee?) ask the same decision; park_programs_3#0 has more copied restatements (3 vs 2)
- `travel_2#0` (travel, yes/no): Does this text help someone who is planning how to reach the place or get around it?  
  Reason: passed; capped: travel had 3 passing yes/no cards with no same-decision pair; copied restatements tie (0 each), so the higher lint max_definition_jaccard (0.364 vs 0.308 and 0.154) is dropped

## Program-check summary (aids only)

- Completeness: rA 50/50, rB 50/50 cards answered; hard failures (missing card or option, option names differ, empty field): 0.
- Copied restatements: 99 of 354 option restatements (on admitted cards: 82).
- Lexical flags (examples nearest another option's definition, or another read's restatement): 152 and 146; restatement nearest another definition: 10. Every flag was read; none showed a real misplacement on an admitted card (yes/no negations and paraphrase defeat word overlap).
- Same-decision pairs admitted together (both within the target, no cap needed): office_help_1#1 / office_help_3#1 (what the writer wants), sci_abstracts_2#1 / sci_abstracts_3#1 (main subject). Labelling the same text with both cards adds little; downstream may pick one per text.

## Earlier drops (before the reads; from `cards/lint_report.json`)

16 of 66 authored cards failed lint (label word in question 11, definitions overlap 5, personal-trait question 1; one card had two reasons) and were never sent to the reads.

## Notes

- The readers' restatements and examples are used only to judge the cards. They are never labels and never training data.
- The file-access audit of the four read agents' transcripts is not part of this step (transcripts are on never-open paths for this workflow); the orchestrator records it. A failed audit discards that read and re-opens admission for the affected cards.
- Artifacts: `cards/admission/compare.json` (program checks), `cards/admission/review.json` (per-card verdicts and reasons), `cards/admitted.jsonl` (41 cards).
