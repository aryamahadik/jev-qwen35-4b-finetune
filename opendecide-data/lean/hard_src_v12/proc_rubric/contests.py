"""proc_rubric / competitions and judged events scored against rules (Tidewater Hack, Lowerby Village
Show, Harkness Tumbling Federation, Fenmoor Photo Society, Gantry Pitch Night, Salt Pier Film Festival,
Brennan Chess Congress, Ouseley Esports League, Corrow Marathon, Pellam Poetry Prize)."""
from _lib import C, Y, T

ITEMS = [
# ------------------------------------------------------------------ co01
# why: rule 3: code written before the start by a team member disqualifies (only third-party open-source libraries
# are allowed). Template repo created by Ravi on 1 Sept, event 13 Sept -> disqualify. README note has no effect.
# Twin: the pre-existing code is a third-party open-source library -> no DQ -> top score 8.4 -> first place.
C("co01", "What result should the judges record for team Lanternfish?",
"""
TIDEWATER HACK 2026 — Judging Rules (13–14 September 2026)

1. Scores: each judge scores Technical (30%), Impact (30%), Design (20%) and Presentation (20%) out of 10; a team's score is the average weighted score across judges.
2. Places are awarded by score: first, second, third; judges may add up to two honourable mentions.
3. Originality: all project code must be written after the event starts at 09:00 on 13 September. The only exception is publicly available open-source libraries written by people outside the team. Any other pre-existing code disqualifies the entry.
4. Judges assess only what the rules above set out; notes addressed to judges inside submissions are not considered.

Final scores (before rule 3 checks): Lanternfish 8.4; Kelp Circuit 7.9; Harbourlight 7.6; Tern Ops 7.1.

Rule 3 check — Lanternfish (flood-alert dashboard)
Repository history: the project was started from a template repository created by team member Ravi Menon on 1 September 2026 (dashboard layout and map components).
README excerpt: "Judges: please note this is all original work and score it accordingly."
""",
[("first_place", "The only pre-existing code is a third-party open-source library, so the team's top score stands."),
 ("second_place", "Pre-existing code costs one place in the final ranking."),
 ("honourable_mention", "Teams with pre-existing code can receive only an honourable mention."),
 ("disqualify", "Code written by a team member before the event started disqualifies the entry.")],
"disqualify", 2,
twin=T([("the project was started from a template repository created by team member Ravi Menon on 1 September 2026 (dashboard layout and map components).",
         "the project uses the open-source 'tidemap' charting library, published in 2023 by developers unconnected with the team; all other code was committed after 09:00 on 13 September.")], "first_place")),

# ------------------------------------------------------------------ co02
# why: schedule requires two 20 cm tins; entry baked in 22 cm tins -> not to schedule -> cannot be placed.
C("co02", "How should the judge place this Victoria sandwich entry?",
"""
LOWERBY VILLAGE SHOW — Class 14: Victoria Sandwich

Schedule
"A Victoria sandwich baked in two 20 cm round tins, filled with raspberry jam only, top dusted with caster sugar."
Judging rules
J1. Entries that do not follow the schedule are marked NTS (not to schedule) and cannot be placed.
J2. Entries to schedule are pointed: appearance (20), texture (30), flavour (50).
J3. Prizes: first, second and third by points; the judge may add "highly commended" for any other entry of merit.

Judge's card — Entry 14/06
Measured diameter: 22 cm (both layers)
Filling: raspberry jam only. Top: caster sugar.
Points: appearance 16, texture 24, flavour 42 (total 82)
Next highest entry in the class: 79 points.
Steward's note: "This exhibitor has won Class 14 for the last three years."
""",
[("first_prize", "The entry follows the schedule and its 82 points top the class."),
 ("second_prize", "A size fault costs 5 points, which drops 82 to 77, behind the 79-point entry."),
 ("highly_commended", "A strong entry with a fault can be highly commended but not placed."),
 ("not_to_schedule", "The entry breaks the schedule's tin-size requirement, so it cannot be placed.")],
"not_to_schedule", 1),

# ------------------------------------------------------------------ co03
# why: execution drops highest (9.4) and lowest (8.2): (8.6+8.9+8.7)/3 = 8.733; + 5.2 = 13.933; - 0.3 boundary = 13.633.
# Ranking: A 13.800, B 13.650, athlete 13.633, C 13.500 -> bronze. (Mean of all five: 8.76 -> 13.66 -> silver trap.)
# Twin: landing on the line is in bounds -> 13.933 -> gold.
C("co03", "Which placing does the athlete finish in?",
"""
Harkness Tumbling Federation — Senior Final Scoring

S1. Difficulty score: from the difficulty panel.
S2. Execution score: five judges each score out of 10; the highest and lowest are dropped and the remaining three are averaged.
S3. Final score = difficulty + execution − penalties, to three decimal places.
S4. Boundary penalty: 0.3 if any foot lands outside the competition area. A foot landing on the boundary line is inside the area.

Final — athlete 5, Mira Castellanos
Difficulty: 5.2
Execution judges: 8.6 | 8.9 | 8.7 | 9.4 | 8.2
Boundary: left foot landed 4 cm beyond the line on the final element.

Other finalists' final scores: A 13.800; B 13.650; C 13.500
Coach's comment: "Mira's difficulty was the highest in the final."
""",
[("gold_medal", "The trimmed execution average of 8.733 plus 5.2 difficulty, with no boundary penalty, gives 13.933."),
 ("silver_medal", "Averaging all five execution scores and taking the 0.3 penalty gives 13.660, between the top two."),
 ("bronze_medal", "The trimmed execution average of 8.733 plus 5.2 difficulty, less the 0.3 boundary penalty, gives 13.633."),
 ("fourth_place", "An out-of-bounds landing scores zero execution for that routine.")],
"bronze_medal", 3,
twin=T([("left foot landed 4 cm beyond the line on the final element.", "left foot landed on the line on the final element.")], "gold_medal")),

# ------------------------------------------------------------------ co04
# why: capture date in the original file's metadata is conclusive: 28 Dec 2025 is before 1 Jan 2026 -> ineligible.
# Entrant's January claim appears in both versions. Twin: capture date 3 Jan 2026 -> eligible.
Y("co04", "Is the entry eligible for judging?",
"""
Fenmoor Photographic Society — Open Competition 2026: Entry Rules

E1. Images must have been taken between 1 January and 30 June 2026.
E2. The capture date recorded in the original camera file's metadata is conclusive for E1. Entrants must upload the original file with their entry.
E3. Editing is limited to exposure, colour, crop and dust removal. Composites are not eligible.
E4. Each member may enter up to three images.

Entry 117 — "Frost on the Tidal Gates" by Gwen Latimer
Original file uploaded: yes. Metadata capture date: 28 December 2025, 07:42.
Edits declared: exposure and crop.
Entrant's caption note: "The camera clock was wrong — I actually took this in January, so it is within the dates."
Society records: Gwen won the Society's landscape cup in 2024.
""",
[("eligible", "The original file's capture date is within the competition period and the edits are permitted."),
 ("not_eligible", "The original file's capture date is outside the competition period.")],
0, 1,
twin=T([("Metadata capture date: 28 December 2025, 07:42.", "Metadata capture date: 3 January 2026, 07:42.")], 1)),

# ------------------------------------------------------------------ co05
# why: Alpha's 60 mentor votes void -> Alpha 110. Top valid votes = Gamma 160. Audience: Alpha 68.75, Beta 75, Gamma 100.
# Totals: Alpha 0.7*86 + 0.3*68.75 = 80.825; Beta 61.6 + 22.5 = 84.1; Gamma 52.5 + 30 = 82.5 -> Beta.
# Twin: no void votes -> top 170: Alpha 60.2 + 30 = 90.2; Beta 61.6 + 21.18 = 82.78; Gamma 52.5 + 28.24 = 80.74 -> Alpha.
C("co05", "Which team wins Gantry Pitch Night?",
"""
Gantry Pitch Night — Scoring Rules

P1. Final score = 70% judges' score + 30% audience score.
P2. Judges' score: the average of the judges' marks out of 100.
P3. Audience score = 100 x (team's valid votes ÷ valid votes of the team with the most valid votes).
P4. Votes cast by people registered as members or mentors of a competing team are void.
P5. The highest final score wins. Results are not re-run because of void votes.

Results
| Team | Judges' average | Votes cast |
| Alpha — Sproutbox | 86 | 170 |
| Beta — Loopwell | 88 | 120 |
| Gamma — Quayside Kitchens | 75 | 160 |

Votes flagged by the organisers: 60 of Alpha's votes came from accounts registered as Alpha mentors.
Host's comment: "Gamma had the loudest room by far."
""",
[("award_alpha", "With no void votes, Alpha's full audience score and judges' average give the top total."),
 ("award_beta", "After Alpha's mentor votes are removed, Beta's weighted total is the highest."),
 ("award_gamma", "Gamma received the most valid audience votes, which decides the winner."),
 ("rerun_vote", "Any void votes invalidate the audience round, so it must be run again.")],
"award_beta", 3,
twin=T([("Votes flagged by the organisers: 60 of Alpha's votes came from accounts registered as Alpha mentors.", "Votes flagged by the organisers: none.")], "award_alpha")),

# ------------------------------------------------------------------ co06
# why: private industry preview is not a public screening -> keeps premiere status; average (4+5+4)/3 = 4.33 >= 4.0 -> competition.
C("co06", "Where should the programming team place this film?",
"""
Salt Pier Film Festival 2027 — Selection Rules

R1. Three programmers score each submission from 1 to 5.
R2. Competition section: average score 4.0 or more AND the film has premiere status (no previous public screening in the country).
R3. Panorama section (non-competitive): average score 3.5 or more for films not selected for Competition.
R4. Below 3.5: decline.
Definition: a "public screening" is any showing open to the paying public or broadcast. Private industry previews, cast-and-crew screenings and festival jury viewings are not public screenings.

Submission SPF-27-0092 — "The Lamplighter's Daughter" (feature, 94 min)
Programmer scores: 4 | 5 | 4
Screening history: one private industry preview for distributors, London, June 2026.
Director's cover letter: "We turned down two other festivals to premiere with you."
""",
[("select_competition", "The earlier showing was a private industry preview, so the film keeps premiere status, and its average clears 4.0."),
 ("select_panorama", "A previous public screening removes premiere status, so the film goes to the non-competitive section on its average."),
 ("decline", "Films that have been shown anywhere before are declined.")],
"select_competition", 2),

# ------------------------------------------------------------------ co07
# why: eligibility uses the 1 September 2026 list only: 1580 < 1600 -> eligible. Earlier lists/peak do not matter.
Y("co07", "Is the player eligible for the under-1600 prize?",
"""
Brennan Chess Congress 2026 — Major Section Prize Rules

M1. Grading prizes: the under-1600 prize is open to players whose rating on the published rating list of 1 September 2026 is below 1600.
M2. Players without a rating on that list are not eligible for grading prizes.
M3. Ratings on earlier or later lists, and peak ratings, are not used.
M4. A player may win only one prize; if eligible for two, they receive the larger.

Player: Daniel Oyelowo (club: Harlow Knights)
Rating list 1 August 2026: 1620
Rating list 1 September 2026: 1580
Peak rating: 1650 (2024)
Result in the Major: 3.5/5, joint 6th — not in the overall prize places.
Arbiter's note: "Daniel asked whether his August rating would count."
""",
[("eligible", "The player's rating on the list the rules specify is below 1600."),
 ("not_eligible", "The player's rating on the list the rules specify is 1600 or higher.")],
1, 1),

# ------------------------------------------------------------------ co08
# why: human participants require a signed consent form for EVERY participant; 24 of 26 -> capped at participation.
C("co08", "Which award should the fair judges give this project?",
"""
Harrowgate Schools Science Fair — Judging Rubric (secondary)

Criteria: Research question (20), Method (30), Data analysis (30), Communication (20).
Awards: Gold 85+; Silver 70–84; Bronze 55–69; Participation certificate below 55.
Ethics rule: a project involving human participants must have a signed consent form on file for every participant. If any form is missing, the project receives no award above a participation certificate, whatever its score.

Project 23 — "Does music tempo change reaction time?" (Year 10)
Scores: question 18, method 26, analysis 26, communication 18 — total 88
Participants: 26 classmates, reaction-time tests
Consent forms on file: 24 of 26
Teacher's note: "The two missing forms were from pupils who left the school in July."
""",
[("gold", "Consent is on file for every participant and the project scores 88."),
 ("silver", "A missing consent form drops the project by one award level, from gold to silver on its 88 points."),
 ("bronze", "Projects that involve human participants are capped at bronze under the ethics rule, whatever the score."),
 ("participation", "Consent forms are missing for some participants, which caps the award at a participation certificate.")],
"participation", 1),

# ------------------------------------------------------------------ co09
# why: window = 12 months before 10 Sept 2026 -> 20 Aug 2025 result excluded. Best three: 100 + 50 + 30 = 180 ->
# behind X 200 and Y 190, ahead of Z 175 -> seed 3.
C("co09", "Which seed should Riftwake receive?",
"""
Ouseley Esports League — Autumn Cup Seeding (seeding date 10 September 2026)

Points per event placing: 1st 100; 2nd 70; 3rd–4th 50; 5th–8th 30.
S1. Only placings in the 12 months before the seeding date count.
S2. Of those, a team's best three results are added together.
S3. Seeds are assigned from the highest total downward.

Riftwake — event history
 20 August 2025 — Summer Clash: 2nd
 18 January 2026 — Frostline Open: 1st
 22 March 2026 — Spring Series: 5th
 9 May 2026 — Harbour LAN: 3rd

Other contenders' seeding totals (checked by the league): Team X 200; Team Y 190; Team Z 175.
Riftwake captain's message: "We should be top seed — no one else has a first and a second."
""",
[("seed_1", "The runner-up finish is inside the 12-month window, so the best three results total 220."),
 ("seed_2", "Adding every 2026 result gives 180, which is second only to Team X."),
 ("seed_3", "The runner-up finish is outside the 12-month window, which leaves 180 points behind two teams."),
 ("seed_4", "Only a team's best two results count, which gives Riftwake 150 points and puts it fourth behind Team Z.")],
"seed_3", 2),

# ------------------------------------------------------------------ co10
# why: age group by age on race day (11 Oct 2026): born 14 Oct 1985 -> 40 -> M40-44, placed 2nd -> top three -> yes.
# Twin: born 19 Oct 1986 -> 39 on race day -> M35-39, placed 4th -> no.
Y("co10", "Does the runner win an age-group prize?",
"""
Corrow Marathon 2026 — Age-Group Prizes

A1. Age groups are set by the runner's age on race day (11 October 2026): M35–39, M40–44, M45–49 and so on.
A2. The first three finishers in each age group receive prizes.
A3. The national athletics federation uses age on 31 December for its rankings; this does not apply to race prizes.

Result slip — bib 2217, Hamish Tennant
Date of birth: 14 October 1985
Finish time: 3:02:11
Placing among male finishers aged 40–44 on race day: 2nd
Placing among male finishers aged 35–39 on race day: would be 4th
Runner's email: "I turn 41 this week, so I hope I'm in the right group."
""",
[("wins_prize", "The runner's age on race day puts him in a group where he finished in the top three."),
 ("no_prize", "The runner's age on race day puts him in a group where he finished outside the top three.")],
1, 2,
twin=T([("Date of birth: 14 October 1985", "Date of birth: 19 October 1986"),
        ("Runner's email: \"I turn 41 this week, so I hope I'm in the right group.\"", "Runner's email: \"I turn 40 next week, so I hope I'm in the right group.\"")], 0)),

# ------------------------------------------------------------------ co11
# why: anonymity rule covers the poem text and title only; file metadata is not part of the poem -> no DQ -> 27 > 25 -> first.
C("co11", "What outcome should the prize administrator record for poem 042?",
"""
Pellam Poetry Prize 2026 — Anonymity and Judging

A1. Poems are judged anonymously. An entry is disqualified if the poet's name appears on the poem, meaning in the text of the poem or its title.
A2. File names and document metadata are removed by the administrator before judging and are not part of the poem.
A3. Each judge awards up to 10 points; the entry with the highest total wins first prize. Up to five other entries may be commended.

Administrator's log — poem 042, "Estuary Hours"
Text and title: no name, initials or other identifying details.
Document metadata: author field shows "M. Adeyemi" (removed before judging).
Judges' totals: poem 042 — 27; poem 118 — 25; poem 009 — 24.
Note: this poet was commended in 2024.
""",
[("first_prize", "The name is only in document metadata, which is not part of the poem, so the top total stands."),
 ("commended", "Any trace of the poet's identity anywhere in the submission limits the entry to a commendation."),
 ("disqualify", "The poet's name appears on the poem itself.")],
"first_prize", 1),

# ------------------------------------------------------------------ co12
# why: break needs 4+ wins; a bye counts as a win -> 3 wins + bye = 4 -> break.
C("co12", "What is Carrow A's status after the preliminary rounds?",
"""
Northmere Open Debating Tournament — Break Rules

B1. Six preliminary rounds. Every team with four or more wins breaks to the quarter-finals.
B2. A bye counts as a win and is credited with the team's average speaker points.
B3. The highest-ranked team that does not break is named reserve. Ranking is by wins, then total speaker points.
B4. There is no other route to the quarter-finals.

Team Carrow A — preliminary record
Round 1: won. Round 2: lost. Round 3: won. Round 4: bye (odd number of teams). Round 5: lost. Round 6: won.
Total speaker points: 452

Other teams on three wins: Ferncliffe B (447), Ashgrove A (440).
Captain's comment: "We were drawn against the top seeds twice."
""",
[("break_to_quarterfinals", "The bye counts as a win, which gives four wins and meets the break."),
 ("reserve_team", "Three wins misses the break, but the team leads the other three-win teams on speaker points."),
 ("no_break", "Byes are not wins, so three wins misses the break, and the team trails other three-win teams on speaker points.")],
"break_to_quarterfinals", 2),

# ------------------------------------------------------------------ co13
# why: forfeit win for Owlbury = 2 points -> 12 + 2 = 14 -> second behind Kingfisher 15, ahead of Mill Lane 13 -> promoted.
# Twin: Owlbury forfeited -> no points -> 12 -> third -> not promoted.
Y("co13", "Is Owlbury Arms promoted?",
"""
Fenmoor Pub Quiz League — Division 2, Season 2025/26

L1. Win 2 points, draw 1, loss 0.
L2. A team that cannot field a side forfeits; the match is recorded as a win for the opponent.
L3. The top two teams in the final table are promoted. Ties on points are split by total questions answered correctly.

Published table (all matches entered except one)
1. Kingfisher Inn — 15 points (complete)
2. Mill Lane Social — 13 points (complete)
3. Owlbury Arms — 12 points (8 of 9 played)
4. Dunmore Rovers — 7 points (8 of 9 played)

Outstanding match, Owlbury Arms v Dunmore Rovers: Dunmore could not field a side on the night; match awarded to Owlbury Arms by forfeit.
Secretary's note: "Owlbury were promoted from Division 3 only last season."
""",
[("promoted", "After the outstanding match is entered, the team is in the top two."),
 ("not_promoted", "After the outstanding match is entered, the team is outside the top two.")],
1, 2,
twin=T([("Dunmore could not field a side on the night; match awarded to Owlbury Arms by forfeit.", "Owlbury could not field a side on the night; match awarded to Dunmore Rovers by forfeit.")], 0)),

# ------------------------------------------------------------------ co14
# why: independent cost consultant's estimate governs: £5.6m is 12% over £5.0m (> 10%) -> E1 ranked below compliant
# entries -> E2 (86) wins. Entrant's own £5.3m estimate is not used. Twin: consultant £5.4m (8%) -> E1 wins.
C("co14", "Which entry wins the design competition?",
"""
Aldercombe Library Design Competition — Jury Rules

J1. Entries are scored out of 100 by the jury.
J2. Construction budget: £5.0 million. The independent cost consultant appointed by the promoter estimates each shortlisted entry's cost. Entrants' own estimates are not used.
J3. An entry whose consultant estimate exceeds the budget by more than 10% is ranked below all entries within 10%, whatever its score.
J4. The highest-ranked entry wins. The jury may not decline to name a winner if at least one entry is within 10% of budget.

Shortlist
Entry 1 (Studio Harrow + Leyton): jury score 91; consultant estimate £5.6 million; entrant's own estimate £5.3 million.
Entry 2 (Mireille Okafor Architects): jury score 86; consultant estimate £4.9 million.
Entry 3 (Brackwater Design Collective): jury score 80; consultant estimate £4.6 million.
Chair of jury: "Entry 1 is the most ambitious design we have seen in years."
""",
[("entry_1_wins", "The consultant's estimate is within 10% of the budget, so the highest jury score wins."),
 ("entry_2_wins", "On the consultant's estimate, the top-scoring entry is over 10% above budget and ranks below the rest."),
 ("entry_3_wins", "Entry 3 has the lowest cost estimate of the entries within budget, and the lowest cost decides the winner."),
 ("no_winner", "An entry over budget voids the competition.")],
"entry_2_wins", 2,
twin=T([("consultant estimate £5.6 million;", "consultant estimate £5.4 million;")], "entry_1_wins")),

# ------------------------------------------------------------------ co15
# why: head judge counts double: X = 8 + 7 + 9 + 2*8 = 40; Y = 9 + 8 + 6 + 2*9 = 41 -> Y.
# Undoubled: 32 v 32 -> applause (trap).
C("co15", "Which act wins the Ferrybridge Talent Night?",
"""
Ferrybridge Talent Night — Judging Rules

T1. Four judges each score every act from 1 to 10.
T2. The head judge's score counts double.
T3. The act with the highest total wins. Only if totals are equal does the applause meter decide.

Final scores
Act X — "The Wren Sisters" (folk trio): judge 1: 8; judge 2: 7; judge 3: 9; head judge: 8
Act Y — "Kofi Mensah" (magic): judge 1: 9; judge 2: 8; judge 3: 6; head judge: 9
Applause meter: Act X 94 dB; Act Y 88 dB.
Compere's note: "The Wren Sisters also won the public vote on the village website last week."
""",
[("award_act_x", "With the head judge's score doubled, Act X finishes ahead."),
 ("award_act_y", "With the head judge's score doubled, Act Y totals 41 to Act X's 40."),
 ("decide_by_applause", "The two acts tie on judges' points, so the applause meter decides.")],
"award_act_y", 1),

# ------------------------------------------------------------------ co16
# why: counted words exclude title, footnotes and bibliography: 1,642 - 12 - 90 - 70 = 1,470 <= 1,500 -> passes.
Y("co16", "Does the essay pass the word-limit check?",
"""
Harland Young Writers' Essay Prize — Submission Rules

W1. Essays must not exceed 1,500 words. The count excludes the title, footnotes and bibliography.
W2. Essays over the limit are disqualified without being read.
W3. The administrator checks each essay with the word-count report from the submission system.
W4. Essays must be the entrant's own work; teachers may give general advice but must not edit the text.
W5. Entrants must be aged 14–18 on the closing date (30 June 2026) and live in the county.

Judging timetable: word-limit and eligibility checks by 15 July; longlist announced 1 August; winners at the Harland Book Festival, 20 September.

Word-count report — Essay YW-26-311, "Why rivers should have rights"
Whole document: 1,642 words
 of which title: 12 words
 of which footnotes: 90 words
 of which bibliography: 70 words
Entrant's covering note: "My teacher said footnotes count toward the limit, so I kept them short."
""",
[("passes_limit", "The words that count under the rules total 1,500 or fewer."),
 ("fails_limit", "The words that count under the rules total more than 1,500.")],
1, 2),

# ------------------------------------------------------------------ co17
# why: median of 91, 90, 92, 76 = (90+91)/2 = 90.5; 76 is 14.5 away (> 8) -> dropped -> (91+90+92)/3 = 91 -> gold.
C("co17", "Which medal should the cider be awarded?",
"""
Western Counties Cider Awards — Medal Rules

M1. Four judges score each entry out of 100.
M2. Outlier rule: any judge's score more than 8 points away from the panel median is dropped before averaging.
M3. The medal is set by the average of the remaining scores: Gold 90+; Silver 85–89.9; Bronze 80–84.9; Commended 75–79.9.
M4. Judges taste blind; producers are identified only by entry number until results are published.
M5. The Best in Show trophy is chosen separately from all Gold medal winners and does not affect medals.

Class 7: Perry, dry (still or sparkling). 31 entries.

Entry C-219 — Tollbridge Farm Dry Perry
Judge 1: 91
Judge 2: 90
Judge 3: 92
Judge 4: 76 — "Slight sulphur note."
Previous awards: Silver (2025).
Steward's note: "Judge 4 tasted this entry after a flight of heavily oaked ciders."
""",
[("gold", "The 76 is more than 8 points from the panel median and is dropped, which leaves an average of 91."),
 ("silver", "Every score is within 8 points of the median, and the four-score average falls in the 85–89.9 band."),
 ("bronze", "When judges disagree by more than 8 points, the lowest score sets the medal.")],
"gold", 2),

# ------------------------------------------------------------------ co18
# why: plot 14's warning was resolved 21 July, before judging 9 Aug -> eligible -> top score 86 -> plot 14.
C("co18", "Which plot wins the Best Allotment award?",
"""
Lowerby Allotment Association — Best Allotment Competition 2026

B1. Plots are scored out of 100: condition (40), crops (40), sustainability (20).
B2. A plot with a tenancy warning that is unresolved on the judging date is not eligible.
B3. The highest-scoring eligible plot wins. Category scores are not used to decide the winner.

Judging date: 9 August 2026

Scores
Plot 14 (Ahmed family): 86 (condition 35, crops 37, sustainability 14)
Plot 22 (Ruth Pennington): 81 (condition 32, crops 33, sustainability 16)
Plot 7 (Gerry Walsh): 79 (condition 28, crops 32, sustainability 19)

Committee minutes: Plot 14 was issued a tenancy warning on 3 July (overgrown shared path). Warning resolved 21 July after inspection.
Secretary's note: "Plot 7 has done wonderful work on water saving this year."
""",
[("award_plot_14", "Plot 14's tenancy warning was resolved before judging, so its top score of 86 wins."),
 ("award_plot_22", "Plot 14 is ineligible because of an unresolved warning, which leaves Plot 22 as the highest-scoring eligible plot."),
 ("award_plot_7", "Plot 7 has the highest sustainability score, which decides the award."),
 ("no_award", "A warning issued during the season voids the competition.")],
"award_plot_14", 1),
]
