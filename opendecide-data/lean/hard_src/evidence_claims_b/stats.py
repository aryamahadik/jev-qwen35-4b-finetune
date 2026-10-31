"""evidence_claims_b / statistical claims: percent vs percentage points, relative vs absolute risk,
rates vs counts, compounding, margins of error, predictive values."""
from _lib import C, Y, T, VERDICT, err, NONE, PCT, PP

ITEMS = [
# ------------------------------------------------------------------ s01
# why: 62.0 -> 74.0 is 12 points but 19.4 percent; twin says points -> accurate.
Y("s01", "Can the fact desk sign off on the number in Lena's draft as written?",
"""
From: Lena Marsh <l.marsh@corvaleregion.example>
To: Fact desk
Subject: OK to publish? (regional digest, Thursday)

Hi team,

Can you sign off on this line for Thursday's regional digest?

Draft: "Thanks to the Connect Corvale scheme, the share of households with a fixed broadband connection rose 12 percent between 2023 and 2025."

Source: Corvale Household Technology Survey, Table 3.1 (weighted estimates):
- 2021: 58.9% of households
- 2023: 62.0% of households
- 2025: 74.0% of households
Each wave samples about 4,100 households; the report says year-to-year differences above 2 points are statistically significant.

House style reminder (Fact desk handbook, section 2.3): "percent" and "%" in a description of change mean relative change; a difference between two percentages must be written as "percentage points". We do not assess attribution phrases like "thanks to" in number checks; those go to the politics desk.

Thanks,
Lena
""",
[PCT, PP], 0, 1,
twin=T([("rose 12 percent between", "rose 12 percentage points between")], 1)),

# ------------------------------------------------------------------ s02
# why: 40.0% -> 44.0% is +10% relative, so the councillor is right; twin baseline 42% -> 4.8%.
Y("s02", "Under the verification standard, is the councillor's \"10 percent improvement\" figure accurate?",
"""
Ward 7 Councillor's Newsletter - Autumn edition (forwarded to the verification team by a reader)

"When I was elected in March 2025, fewer than half of our streetlights were LED. Today 44 percent of them are - a 10 percent improvement in just eighteen months. Brighter, cheaper, greener."

City Lighting Services asset register, Ward 7 extract:
- March 2025: 500 of 1,250 streetlights LED (40.0%)
- September 2026: 550 of 1,250 streetlights LED (44.0%)
No streetlights were added or removed in the ward over the period.

Reader's message: "Surely it went up 4 percent, not 10? Is the councillor fiddling the numbers?"

Verification standard: a change described in "percent" is checked as a relative change, (new - old) / old; a change described in "percentage points" is checked as the difference between the two percentages. Rounding to the nearest whole number is accepted.
""",
[PCT, PP], 1, 2,
twin=T([("500 of 1,250 streetlights LED (40.0%)", "525 of 1,250 streetlights LED (42.0%)")], 0)),

# ------------------------------------------------------------------ s03
# why: 91.5 -> 87.3 = 4.2 points, 4.59% relative -> C. Twin 86.9: 4.6 points, 5.0% -> B.
C("s03", "Which candidate sentence can run in the Gazette without any change?",
"""
Hollin Valley Gazette - Health page, copy check

Editor's note: exactly one sentence below may be correct, or none may be. Pick the one that can run unchanged.

Data (Hollin Valley Public Health Unit, two-dose MMR coverage measured at age 5):
- 2024 cohort: 91.5%
- 2025 cohort: 87.3%
- Coverage target set by the unit: 95%

Candidate sentences:
A. "Two-dose coverage fell 4.2 percent in a single year."
B. "Two-dose coverage fell 4.6 percentage points in a single year."
C. "Two-dose coverage fell by about 4.6 percent in a single year."
D. "Two-dose coverage is now more than 9 points below the unit's target."

Gazette style: "percent" describes relative change; "percentage points" or "points" describes the difference between two percentages. "About" allows rounding to one decimal place; figures without "about" must match to one decimal place.
""",
[("sentence A", "\"Two-dose coverage fell 4.2 percent in a single year.\""),
 ("sentence B", "\"Two-dose coverage fell 4.6 percentage points in a single year.\""),
 ("sentence C", "\"Two-dose coverage fell by about 4.6 percent in a single year.\""),
 ("sentence D", "\"Two-dose coverage is now more than 9 points below the unit's target.\""),
 (NONE, "no candidate sentence can run unchanged")],
"sentence C", 2, ordered=True,
twin=T([("2025 cohort: 87.3%", "2025 cohort: 86.9%")], "sentence B")),

# ------------------------------------------------------------------ s04
# why: 2.0% -> 1.2% is a 40% relative reduction; the night editor conflates absolute and relative. Twin 2.4% -> 50%.
Y("s04", "Do the trial numbers support the figure in the press release headline?",
"""
PRESS RELEASE - Maribel Therapeutics (embargoed to 00:01, 14 October)
HEADLINE: Once-daily Veltrazine cuts stroke risk by 40% in people with atrial fibrillation

The VELA-3 trial randomly assigned 6,000 adults with atrial fibrillation to Veltrazine or placebo, on top of usual care, and followed them for three years.
Strokes over three years: placebo group 60 of 3,000 (2.0%); Veltrazine group 36 of 3,000 (1.2%).
Major bleeding over three years: placebo 0.9%; Veltrazine 1.1%.

Science desk checklist:
1. A "cuts risk by X%" headline is read as a relative risk reduction.
2. The absolute difference must appear somewhere in our own story, but its absence from a press release does not by itself make the headline wrong.
3. Check every figure against the trial numbers, not against the company's framing.

Comment from the night editor: "The real difference is 0.8 of a point. Calling that 40% is spin - I'd mark the headline as unsupported."
""",
[("relative risk reduction", "(risk without treatment - risk with treatment) / risk without treatment"),
 ("absolute risk reduction", "risk without treatment - risk with treatment, in percentage points")],
1, 2,
twin=T([("placebo group 60 of 3,000 (2.0%)", "placebo group 72 of 3,000 (2.4%)")], 0)),

# ------------------------------------------------------------------ s05
# why: ARR 3 points -> 1/0.03 = 33.3 -> round up 34. 5 is 1/RRR. Twin 10.0% -> ARR 5 -> 20.
C("s05", "What number needed to treat for 12 months should the slide show?",
"""
Physio Practitioners Network - Forum > Evidence Corner
Thread: "Treat 5 to prevent 1"??

marta_pt wrote:
Our clinic manager is pitching the StepSure home exercise programme to the health board with a slide that says "Number needed to treat = 5". The trial behind it randomised 1,200 adults aged over 70 living at home. Over 12 months, 15.0% of the control group had at least one fall, compared with 12.0% in the programme group. Dropout was similar in both arms. I don't trust the slide. What should it say?

moderator_eb wrote:
Network glossary, for anyone checking: absolute risk reduction (ARR) = control risk - programme risk. Relative risk reduction (RRR) = ARR / control risk. Number needed to treat (NNT) = 1 / ARR, with ARR written as a proportion, always rounded UP to the next whole person, and quoted for the follow-up period of the trial.
""",
[("5", "five people treated for 12 months per person spared a fall"),
 ("20", "twenty people treated for 12 months per person spared a fall"),
 ("25", "twenty-five people treated for 12 months per person spared a fall"),
 ("34", "thirty-four people treated for 12 months per person spared a fall"),
 (NONE, "the correct figure is not listed")],
"34", 2, ordered=True,
twin=T([("12.0% in the programme group", "10.0% in the programme group")], "20")),

# ------------------------------------------------------------------ s06
# why: 5 -> 10 per 10,000 is +0.05 points absolute and +100% relative; "adds about 1 percent" matches neither. Twin "doubles" -> yes.
Y("s06", "Is the proposed leaflet wording accurate?",
"""
Druvell Health - Patient Information Team, wording review, item 3 of 7

Proposed leaflet wording (section "Blood clots"):
"Compared with older pills, Lunessa adds about 1 percent to your yearly risk of a blood clot."

Evidence (regulator's assessment report, large pooled cohort of users):
- Women using older combined pills: about 5 venous blood clots per 10,000 women per year.
- Women using Lunessa: about 10 venous blood clots per 10,000 women per year.
- Women not using any hormonal contraception: about 2 per 10,000 women per year.

Leaflet standards (section 4.2): give risks as absolute numbers where possible. If a percentage is used to describe an increase in risk, it must match either the relative increase (for example "twice as likely", "50 percent more likely") or the absolute increase expressed in percentage points. Wording that matches neither is inaccurate.

Reviewer's margin note: "1 percent sounds small and reassuring - fine by me."
""",
[("relative increase", "(new risk - old risk) / old risk"),
 ("absolute increase", "new risk - old risk, which for rates per 10,000 can be expressed in percentage points (1 per 10,000 = 0.01 points)")],
0, 2,
twin=T([("Lunessa adds about 1 percent to your yearly risk", "Lunessa doubles your yearly risk")], 1)),

# ------------------------------------------------------------------ s07
# why: 30 -> 45 is +50% relative, so "rose by half" is right. Twin "rose by 15 percent" is a pp mix-up.
C("s07", "Which problem, if any, does the \"rose by half\" sentence have?",
"""
Carrick District Council - "Your Bin News", Spring 2026 (proof for sign-off)

Page 2 feature: "Weekly collections are working"
"Two years ago, fewer than one in three households regularly put out their recycling box. Participation rose by half between the 2023 and 2025 counts, and our crews now collect from 45 of every 100 homes on a typical round."

Source attached by the comms team - Carrick participation monitoring (a household counts as participating if it set out its box at least once in three consecutive collection weeks):
- 2023 count: 30.0% of 12,400 sampled households
- 2025 count: 45.0% of 12,650 sampled households
Sampling covered every collection round in the district in both years.

Proof-reader's query: "We say 'rose by half' but the chart shows 15. Please classify the problem with that sentence, if there is one, before we print."
""",
err("pp", "rel", "causal", "time", "subgroup", "none"),
NONE, 2,
twin=T([("Participation rose by half between", "Participation rose by 15 percent between")], "percent/percentage-point mix-up")),

# ------------------------------------------------------------------ s08
# why: 4% of 2.00m = 80,000; 5% of 1.80m = 90,000 -> +12.5%, not a quarter. Twin labour force 2.00m -> +25%.
Y("s08", "Is the proposed debate line consistent with the source table under the unit's rule?",
"""
Opposition Research Unit - briefing note (draft, not for circulation)

Proposed line for Tuesday's debate:
"Under this government the number of people out of work in Stellmarch has gone up by a quarter."

Source: Stellmarch Statistics Bureau, Labour Force Survey, annual averages
| | 2023 | 2026 |
| Unemployment rate | 4.0% | 5.0% |
| Labour force (employed + unemployed) | 2.00 million | 1.80 million |
The government took office at the start of 2023.

Researcher's note: "Rate went from 4 to 5 - that's 25% up, so the line is solid."

Unit rule: every number in a debate line is checked against the source table; approximations such as "a quarter" or "a third" must be within 2 percentage points of the true percentage change.
""",
[("unemployment rate", "unemployed people as a percentage of the labour force"),
 ("number unemployed", "unemployment rate x labour force")],
0, 3,
twin=T([("| 2.00 million | 1.80 million |", "| 2.00 million | 2.00 million |")], 1)),

# ------------------------------------------------------------------ s09
# why: 23.0-18.4 = 4.6 points; 4.6/18.4 = 25% -> both. Twin makes sentence 1 say "percent" -> only 2.
C("s09", "Which of the two sentences can be ticked under the checklist rule?",
"""
Energy Watch newsletter - sub-editor's checklist, item 4

Chart: share of Veldria's electricity generation from wind (Grid Operator annual reports)
2020: 15.1% | 2022: 18.4% | 2024: 21.9% | 2025: 23.0%

Sentence 1 (standfirst): "Wind's share of generation rose 4.6 percentage points between 2022 and 2025."
Sentence 2 (chart caption): "Between 2022 and 2025, wind's share of the grid grew by a quarter."

Checklist rule: tick a sentence only if its figure matches the chart. Differences in points must match to one decimal place. Relative changes ("percent", or fractions such as "a quarter" or "a third") must match to the nearest whole percent. "Share of generation" and "share of the grid" refer to the same series.
""",
[("sentence 1 only", "only the standfirst matches the chart"),
 ("sentence 2 only", "only the caption matches the chart"),
 ("both sentences", "the standfirst and the caption both match the chart"),
 ("neither sentence", "neither the standfirst nor the caption matches the chart")],
"both sentences", 2, ordered=True,
twin=T([("rose 4.6 percentage points between", "rose 4.6 percent between")], "sentence 2 only")),

# ------------------------------------------------------------------ s10
# why: control arm was "usual care" with unrecorded toothpaste and no supervised brushing, so the named comparison is untested. Twin supplies the comparator.
C("s10", "Which verdict does the advert's comparative claim receive on the evidence supplied?",
"""
Advertising Standards Panel of Morvane - Complaint file ASP/26/0417
Advertiser: Pellucid Oral Care Ltd

Claim (TV spot, on-screen text): "Enamelite Pro - 50% fewer new cavities than ordinary fluoride toothpaste."

Evidence supplied by the advertiser: one study, Harkin et al. (2024). 812 children aged 7-11 were randomly allocated to two groups for 24 months. Group A received Enamelite Pro plus supervised brushing sessions at school. Group B continued usual care (families kept using whatever toothpaste they already bought; brand and fluoride content were not recorded). New cavities per child over 24 months: Group A 0.21; Group B 0.42.

Complainant's argument: "The study had no ordinary fluoride toothpaste arm, so the advert is simply false."
Advertiser's reply: "Most toothpaste on sale in Morvane contains fluoride, so usual care is ordinary fluoride toothpaste."

Panel's approach: the claim is assessed, as worded, against the evidence supplied, including the comparison it names.
""",
VERDICT, "not enough information", 3,
twin=T([("Group B continued usual care (families kept using whatever toothpaste they already bought; brand and fluoride content were not recorded).",
         "Group B received a standard 1,450 ppm fluoride toothpaste plus the same supervised brushing sessions.")], "supported")),

# ------------------------------------------------------------------ s11
# why: vaccinated 120/320,000 = 37.5 per 100k vs unvaccinated 80/80,000 = 100 per 100k. Twin 20% vaccinated -> claim true.
C("s11", "Which flaw, if any, is in rowan_k's conclusion?",
"""
Tallow Creek Parents Circle - Forum > Health

rowan_k wrote:
Hospital data just out: of the 200 people admitted with severe flu in Tallow County this winter, 120 (60%) had been vaccinated this season. So in Tallow County this winter, vaccinated people were MORE likely to end up in hospital with flu than unvaccinated people. Why is nobody talking about this?

county_data_nerd wrote:
County figures for the same season: population 400,000; vaccinated this season 320,000 (80%). The admissions count is from the county hospital system, which covers all residents.

mod_pat wrote:
Keep it civil. For the record, the county report does not claim anything about why people were admitted, only who was admitted.
""",
err("base", "causal", "pp", "subgroup", "time", "none"),
"base-rate confusion", 2,
twin=T([("vaccinated this season 320,000 (80%)", "vaccinated this season 80,000 (20%)")], NONE)),

# ------------------------------------------------------------------ s12
# why: 1.1^3 = 1.331 -> +33.1%, more than 30%. Twin 129.8 -> +29.8%.
Y("s12", "Is the union's draft line accurate for January 2023 to January 2026?",
"""
Harbourside Tenants' Union - flyer draft, checked by volunteer researcher

Draft line: "Average advertised rents in Harbourside are up more than 30 percent in just three years."

Data: Harbourside Rental Index (average advertised rents, January of each year, January 2023 = 100)
Jan 2023: 100.0 | Jan 2024: 110.0 | Jan 2025: 121.0 | Jan 2026: 133.1

Landlords' Association response, quoted in the Harbourside Echo: "Rents have gone up about 10 percent a year. That is 30 percent over three years at the very most. The union is exaggerating."

Volunteer's instruction from the union secretary: check the line only against the index, for the period January 2023 to January 2026. The index is published by the regional statistics office and is not seasonally adjusted, which does not matter for January-to-January comparisons.
""",
[PCT, ("index", "a series scaled so that the base period equals 100; the percent change between two dates is (later / earlier - 1) x 100")],
1, 2,
twin=T([("Jan 2026: 133.1", "Jan 2026: 129.8")], 0)),

# ------------------------------------------------------------------ s13
# why: 0.70 x 0.80 = 0.56 of the ticket price -> 44% off, not 50%.
C("s13", "What total reduction from the original ticket price does a shopper actually get on a sale item?",
"""
Trading Standards, Wexcombe - consumer complaint triage note

Complaint: shopper photographed a banner in Brightwell's department store:
"WINTER SALE - Already 30% off everything! Take an EXTRA 20% at the till. That's 50% off!"

Store's till procedure (supplied by Brightwell's head office): the sale price is the ticket price minus 30%. At the till, the extra 20% is taken off the sale price, not off the original ticket price. No other discounts apply to sale items, and loyalty points are not counted.

Complainant's view: "50% off is what they promised, and that's what I expected to pay."
Store's view: "Everyone understands that discounts stack. The banner is fair."

Triage officer's task: record the true total reduction from the original ticket price that a shopper receives on a sale item, to the nearest whole percent, before deciding whether the banner goes to investigation.
""",
[("44%", "the shopper pays 56% of the original ticket price"),
 ("50%", "the shopper pays half of the original ticket price"),
 ("56%", "the shopper pays 44% of the original ticket price"),
 ("60%", "the shopper pays 40% of the original ticket price"),
 (NONE, "the true total reduction is not listed")],
"44%", 1, ordered=True),

# ------------------------------------------------------------------ s14
# why: "typical" = median per glossary; median fell. Twin median rose -> supported (cash terms).
C("s14", "What verdict should the line check give the minister's proposed line?",
"""
Brannoch Ministry of Labour - media line check (press office)

Minister's proposed line for Thursday's radio interview:
"The typical full-time employee in Brannoch earns more today than a year ago."

Source: Annual Survey of Earnings, gross weekly pay, full-time employees, April 2025 vs April 2026, cash terms (not adjusted for inflation). The April 2026 release is the latest available.
- Mean: 812 -> 845 crowns (+4.1%)
- Median: 701 -> 694 crowns (-1.0%)
- 10th percentile: 402 -> 399 crowns
- 90th percentile: 1,460 -> 1,610 crowns

Glossary note from the Statistics Office: "We use the median to describe the typical employee. The mean is pulled up by very high earners."

Special adviser's note: "Average pay is up 4%. The line is fine - and it's only about cash, not inflation."
""",
VERDICT, "refuted", 2,
twin=T([("Median: 701 -> 694 crowns (-1.0%)", "Median: 701 -> 707 crowns (+0.9%)")], "supported")),

# ------------------------------------------------------------------ s15
# why: PPV = .95*.01 / (.95*.01 + .05*.99) = 16%. Twin prevalence 10% -> PPV 68%.
Y("s15", "Is the draft leaflet sentence accurate for the people the trust will screen?",
"""
Clinical Governance Committee - Oakhurst Health Trust
Item 6: patient leaflet for the new Hepra-Scan screening blood test

Draft leaflet sentence: "If your Hepra-Scan result is positive, it is more likely than not that you have the liver condition."

Test performance (manufacturer's validation study, independently confirmed): sensitivity 95%; specificity 95%.

Expected prevalence of the condition among the adults the trust will invite for screening: 1%.

Committee definitions: sensitivity = share of people with the condition who test positive; specificity = share of people without the condition who test negative; positive predictive value (PPV) = share of positive results that are true positives, given the prevalence in the tested group.

Committee member's comment: "A 95% accurate test - a positive means you almost certainly have it. If anything the leaflet undersells it."
""",
[("sensitivity", "share of people with the condition who test positive"),
 ("specificity", "share of people without the condition who test negative"),
 ("positive predictive value", "share of positive results that are true positives, which depends on how common the condition is in the tested group")],
0, 3,
twin=T([("the trust will invite for screening: 1%.", "the trust will invite for screening: 10%.")], 1)),

# ------------------------------------------------------------------ s16
# why: 52 - 3.1 = 48.9, not above 50, but upper end is above 50 -> neither established nor false. Twin 54 -> 50.9.
C("s16", "Under the Post's polling standards, which verdict fits the front-page claim?",
"""
Dunmore Evening Post - Politics desk
Reader complaint about Saturday's front page

Front-page claim: "A majority of Dunmore residents back the tram extension."

Source: Civic Pulse poll for the Post; 1,004 adult residents; fieldwork 2-6 September 2026; weighted to census.
Question: "Do you support or oppose extending the tram line to Kellow Bridge?"
Support 52%; oppose 39%; don't know 9%.
Stated margin of error: plus or minus 3.1 points at 95% confidence.

Post polling standards (section 4):
(a) We may state that a majority, or most, of a population holds a view only when the lower end of the margin of error for that view is above 50%.
(b) We may state that a view is held by a minority only when the upper end of its margin of error is below 50%.
(c) We may call a view "the most common" when its lower end exceeds the upper end of every other answer.
""",
VERDICT, "not enough information", 2,
twin=T([("Support 52%; oppose 39%; don't know 9%.", "Support 54%; oppose 38%; don't know 8%.")], "supported")),

# ------------------------------------------------------------------ s17
# why: 1,480 -> 2,960 is +100% (doubled), not +200%.
Y("s17", "Does the admissions extract bear out the press note's figure?",
"""
University of Kestwick - Admissions Office press note (draft 3)

"Demand for our new Data Science BSc has exploded: applications increased by 200 percent between the 2024 and 2026 admission cycles, making it our fastest-growing course."

Admissions system extract (applications received by the main deadline, all applicant types):
- 2024 cycle: 1,480
- 2025 cycle: 2,210
- 2026 cycle: 2,960

Press office style rule: "increased by X percent" means (new - old) / old x 100.

Comment from the course leader: "We went from about fifteen hundred to about three thousand. That's a big jump - please make sure the percentage is right before this goes out."

Comment from the press officer: "Three thousand is two hundred percent of fifteen hundred, so 200 percent is correct."
""",
[PCT, ("doubling", "an increase of 100 percent: the new value is twice the old value")],
0, 1),

# ------------------------------------------------------------------ s18
# why: 40 -> 20 -> 30. A false (30 != 40); B true (25% below); C wrong unit for a price; D false (+50%).
C("s18", "Which sentence, if any, describes the share price accurately?",
"""
Markets desk - copy check, Venn Robotics (ticker VNNR)

Closing prices from the exchange:
- Last trading day of February: 40.00 crowns
- Last trading day of March: 20.00 crowns
- Last trading day of April: 30.00 crowns
No splits, dividends or other adjustments in the period.

Candidate sentences for the April wrap:
A. "After halving in March and then climbing 50 percent in April, Venn Robotics shares are back where they started the spring."
B. "Venn Robotics shares ended April 25 percent below their February close."
C. "Venn Robotics shares ended April 25 percentage points below their February close."
D. "Venn Robotics shares have risen 10 percent since the end of March."

Markets desk style: "percent" is the relative change in a price; "percentage points" is used only for the difference between two rates or shares, never for a price.
""",
[("sentence A", "\"After halving in March and then climbing 50 percent in April, Venn Robotics shares are back where they started the spring.\""),
 ("sentence B", "\"Venn Robotics shares ended April 25 percent below their February close.\""),
 ("sentence C", "\"Venn Robotics shares ended April 25 percentage points below their February close.\""),
 ("sentence D", "\"Venn Robotics shares have risen 10 percent since the end of March.\""),
 (NONE, "no candidate sentence is accurate")],
"sentence B", 1, ordered=True),

# ------------------------------------------------------------------ s19
# why: 4.0% -> 3.0% is a 25% relative cut = "a quarter". Twin claims 1 in 4 people protected (ARR is 1 point) -> refuted.
C("s19", "How should the desk rate the post against the CORAL trial?",
"""
Fact-check request #5521 - submitted by a reader

Social media post by a supplement retailer:
"In a major trial, CardioLyn cut heart attacks by a quarter compared with placebo."

Source found by our researcher: the CORAL trial, published 2025. 9,200 adults aged 55-75 with high cholesterol were randomly assigned to CardioLyn or placebo and followed for five years. Heart attacks: placebo 184 of 4,600 (4.0%); CardioLyn 138 of 4,600 (3.0%). This was the pre-registered primary outcome, and the result was statistically significant. No other trial of CardioLyn exists.

Researcher's note: "Only a 1 percentage point difference. I'd say the post is misleading."

Our rules: rate what the post says, as worded, against the source. Do not rate what the post leaves out unless the omission makes the words themselves false.
""",
VERDICT, "supported", 2,
twin=T([("CardioLyn cut heart attacks by a quarter compared with placebo.", "CardioLyn prevented a heart attack in one in four people who took it.")], "refuted")),

# ------------------------------------------------------------------ s20
# why: (25-20)/20 = 25% more for men; (25-20)/25 = 20% less for women. Twin switches to the "less" framing.
Y("s20", "Does the page 4 sentence match Table 2 under the guild's style?",
"""
Guild of Veterinary Nurses - Sector Pay Report 2026, proofing notes

Sentence on page 4: "Men in the sector earn 20 percent more per hour than women."

Table 2 (median hourly pay, all veterinary nurses, 2026 membership survey, n = 3,412):
- Men: 25.00 per hour
- Women: 20.00 per hour
- All: 20.40 per hour

Proofreader note on the guild's style: "A earns X percent more than B" means (A - B) / B x 100. "A earns X percent less than B" means (B - A) / B x 100. Figures must match to the nearest whole percent. Using medians for "earn" is accepted house practice.

Author's reply to the proofreader: "The gap is 5 on 25, i.e. 20 percent. We've always reported it that way."
""",
[("X percent more than B", "(A - B) / B x 100, measured against the comparison value B"),
 ("X percent less than B", "(B - A) / B x 100, measured against the comparison value B")],
0, 2,
twin=T([("Men in the sector earn 20 percent more per hour than women.", "Women in the sector earn 20 percent less per hour than men.")], 1)),

# ------------------------------------------------------------------ s21
# why: net Jan 44-48 = -4; Jul 41-50 = -9 -> fell 5 points. Twin disapprove 46 -> net -5 -> fell 1.
C("s21", "Which description of the change in the First Minister's net approval from January to July is correct?",
"""
Estrow Herald - Polling unit, tracker note for the weekend edition

Question asked in every wave: "Do you approve or disapprove of the way the First Minister is handling her job?"

January 2026 wave (n = 1,510): approve 44%, disapprove 48%, no opinion 8%.
July 2026 wave (n = 1,498): approve 41%, disapprove 50%, no opinion 9%.

Glossary: net approval = approve % minus disapprove %. Changes in net approval are reported in points, and a move from a less negative to a more negative number is a fall.

Draft chart title from the graphics team: "Approval slips 3 points".
""",
[("fell 1 point", "net approval is 1 point lower in July than in January"),
 ("fell 3 points", "net approval is 3 points lower in July than in January"),
 ("fell 5 points", "net approval is 5 points lower in July than in January"),
 ("fell 9 points", "net approval is 9 points lower in July than in January"),
 ("rose 5 points", "net approval is 5 points higher in July than in January"),
 (NONE, "the correct description is not listed")],
"fell 5 points", 2,
twin=T([("disapprove 50%, no opinion 9%", "disapprove 46%, no opinion 13%")], "fell 1 point")),

# ------------------------------------------------------------------ s22
# why: per pupil 540m/60k = 9,000 vs 300m/30k = 10,000 -> Arden spends more per pupil.
Y("s22", "Does the finance return support the leaflet's claim?",
"""
Local election leaflet - check requested by the Kelvar Courier letters editor

Leaflet (Kelvar Progress Party): "Thanks to our investment, Kelvar County now spends more on each of its pupils than neighbouring Arden."

Source: Provincial Education Finance Return 2025-26 (revenue spending on state schools, final outturn):
- Kelvar County: total school revenue spending 540 million crowns; pupils enrolled 60,000
- Arden: total school revenue spending 300 million crowns; pupils enrolled 30,000

Notes in the return: capital (building) spending is excluded for both areas; pupil numbers are the January census count; both areas report on the same basis.

Letters editor's instruction: check only the comparison in the leaflet, not the "thanks to our investment" part.
""",
[("spending per pupil", "total revenue spending divided by the number of pupils enrolled")],
0, 1),

# ------------------------------------------------------------------ s23
# why: 15% of 5.0m = 750k; 13% of 6.0m = 780k -> number rose. Twin 5.5m -> 715k.
C("s23", "Which verdict fits the chapter 3 sentence?",
"""
Health Promotion Agency of Tarrow - Annual report proof, chapter 3

Sentence: "The number of 16-to-24-year-olds who smoke has fallen since 2020."

Source tables (Tarrow Lifestyle Survey smoking prevalence; official mid-year population estimates):
- 2020: 15.0% of 16-24-year-olds smoke; population aged 16-24: 5.0 million
- 2026: 13.0% of 16-24-year-olds smoke; population aged 16-24: 6.0 million
The survey report states that its prevalence estimates can be applied to the population estimates to give numbers of smokers.

Comment from an agency officer: "The rate dropped 2 points, so the sentence is fine as it stands."
""",
VERDICT, "refuted", 2,
twin=T([("population aged 16-24: 6.0 million", "population aged 16-24: 5.5 million")], "supported")),

# ------------------------------------------------------------------ s24
# why: correct relative fall = (8.0-6.4)/8.0 = 20%; claim "1.6 percent" -> error 92%, right direction -> mostly false. Twin says points -> true.
C("s24", "What rating does the Northgate guide give the claim?",
"""
Northgate Fact Check - rating guide for numeric claims

Compare the claim's figure with the correct figure from the source, measuring error as |claim - correct| / |correct|. "Percent" in a claim about change means relative change; "percentage points" means the difference between two percentages.
- TRUE: error of 5% or less.
- MOSTLY TRUE: error over 5%, up to 15%.
- HALF TRUE: error over 15%, up to 30%.
- MOSTLY FALSE: error over 30%, but the claim gets the direction of change right.
- FALSE: the claim gets the direction of change wrong.

Claim (council leader, budget speech): "Council tax arrears in Wendle have fallen 1.6 percent since 2023."

Source (Wendle Revenues Service): share of households in arrears on 31 March each year - 2023: 8.0%; 2024: 7.1%; 2025: 6.8%; 2026: 6.4%.
""",
[("true", "error of 5% or less"),
 ("mostly true", "error over 5% and up to 15%"),
 ("half true", "error over 15% and up to 30%"),
 ("mostly false", "error over 30% with the direction of change right"),
 ("false", "direction of change wrong")],
"mostly false", 3, ordered=True,
twin=T([("have fallen 1.6 percent since 2023", "have fallen 1.6 percentage points since 2023")], "true")),

# ------------------------------------------------------------------ s25
# why: 40% x 25% = 10% of adults -> one in ten. Twin 15% -> 6%.
Y("s25", "Does the survey back up the release's \"one in ten\" figure?",
"""
Galloway Bay Transit Authority - press release draft

Headline: "One in ten adults in Galloway Bay now uses the TideBus app every day."

Source: GBTA Rider Survey, June 2026, representative sample of 2,000 adults living in the Galloway Bay area, weighted by age, sex and district.
- 40% of adults say they use the TideBus app at all.
- Among those app users, 25% say they open it every day; 45% weekly; 30% less often.

Press office rule: a fraction such as "one in N" is accurate if it is within 1 percentage point of 100/N percent of the stated population. Self-reported frequency is accepted as reported.

Note from the marketing lead: "25% daily - so it's one in four, not one in ten. We're underselling ourselves."
""",
[("share of adults who are daily users", "share of adults who use the app x share of users who open it daily")],
1, 2,
twin=T([("Among those app users, 25% say they open it every day; 45% weekly; 30% less often.",
         "Among those app users, 15% say they open it every day; 45% weekly; 40% less often.")], 0)),

# ------------------------------------------------------------------ s26
# why: 2,100/150,000 = 14 per 1,000 vs 6,300/1,800,000 = 3.5 per 1,000.
C("s26", "What is the main flaw in the reader's conclusion?",
"""
Road Safety Partnership of Eskdale - draft reply for the letters page

Letter from a reader:
"Your campaign targeting teenage drivers is unfair. Last year drivers aged 17-19 were involved in 2,100 injury crashes in Eskdale, while drivers aged 40-49 were involved in 6,300. The figures prove teenagers are the safer drivers."

Data held by the partnership for the same year:
- Licensed drivers resident in Eskdale aged 17-19: 150,000
- Licensed drivers resident in Eskdale aged 40-49: 1,800,000
- Average annual miles driven: 17-19: 6,100; 40-49: 8,900
Crash counts cover all injury crashes reported to police in Eskdale during the calendar year.

Partnership press officer: "Please name the flaw plainly in the reply. Readers respond better to one clear point than to a list."
""",
err("count", "pp", "causal", "subgroup", "time", "none"),
"counts compared instead of rates", 1),
]
