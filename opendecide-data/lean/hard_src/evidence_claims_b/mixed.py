"""evidence_claims_b / mixed formats: headline and statement picking, long option lists,
error typology, rating scales, real vs cash terms, significance and strength wording."""
from _lib import C, Y, T, VERDICT, err, ERR, NONE

WARDS = ["Abbotsford", "Barrowgate", "Castleview", "Dene Park", "Eastwick", "Fernhill", "Glebe",
         "Harcourt", "Ivydale", "Juniper Hill", "Kingsmead", "Larkrise", "Millbrook", "Northgate",
         "Orchard Vale", "Priory", "Queensway", "Riverside", "St Anne's", "Thornbury", "Upton",
         "Victoria", "Westfield", "Yewtree"]


def sents(prefix, texts):
    return [(f"{prefix} {k}", f"\"{v}\"") for k, v in texts]


M01 = [("A", "Exercise cuts need for knee surgery by 2.5%"),
       ("B", "Exercise programme spares one in four patients from knee surgery"),
       ("C", "A quarter fewer knee operations among patients given exercise programme"),
       ("D", "Exercise programme cuts knee surgery rate by 25 points"),
       ("E", "Treat 25 patients with exercise to prevent one knee operation"),
       ("F", "Exercise halves need for knee surgery in over-70s")]

M02 = [("1", "Every type of school improved its pass rate."),
       ("2", "Free schools' pass rate improved by 10 percent."),
       ("3", "Free schools' pass rate improved by 10 percentage points."),
       ("4", "Academies improved by more than free schools."),
       ("5", "Faith schools remain the highest-performing type of school."),
       ("6", "The overall pass rate rose by 1.7 percent.")]

M09 = [("1", "Adults living within 300 metres of a park reported fewer depressive symptoms on average."),
       ("2", "The difference was seen in both women and men."),
       ("3", "The link held in every age group studied."),
       ("4", "Living near a park was associated with lower depression scores."),
       ("5", "More than 12,000 adults took part."),
       ("6", "The difference averaged 1.2 points on the 27-point scale.")]

M21 = [("A", "First-time youth offending has fallen by 60 percentage points since 2015."),
       ("B", "First-time youth offending has fallen by more than two-thirds since 2015."),
       ("C", "The rate of first-time youth offending is now less than a third of its 2015 level."),
       ("D", "Youth crime has fallen 60 percent since 2015."),
       ("E", "Fewer than 8,000 young people entered the justice system for the first time in 2025.")]


def listed(items):
    return "\n".join(f"{k}. \"{v}\"" for k, v in items)


ITEMS = [
# ------------------------------------------------------------------ m01
# why: 10.0% -> 7.5%: RRR 25% (C right), ARR 2.5 points, NNT 40; no age results. Twin 6.0%: NNT 25 -> E.
C("m01", "Which headline option can the desk use as written?",
"""
Health desk, Carrow Standard - headline options for Friday's lead

Trial: KNEE-MOVE. 600 adults aged 50-80 with knee osteoarthritis on a surgical waiting list were randomly assigned to a 12-week supervised exercise programme or to usual care, and followed for 12 months. Needed a knee replacement within 12 months: usual care 10.0%; programme group 7.5%. Pain scores improved more with the programme (difference 6 points on a 100-point scale). Results by age group were not reported.

Headline options:
""" + listed(M01) + """

Desk style: "percent" means relative change; "points" means the difference between two percentages; number needed to treat = 1 / absolute risk reduction, rounded up; headlines may use cause-and-effect verbs for randomised trials but must not describe groups for which results were not reported. Exactly one option may be usable, or none.
""",
sents("headline", M01) + [(NONE, "no headline option can be used as written")],
"headline C", 3, ordered=True,
twin=T([("programme group 7.5%", "programme group 6.0%")], "headline E")),

# ------------------------------------------------------------------ m02
# why: free schools 55.0 -> 60.5 = +10% relative (statement 2); all others fail (community and faith fell; academies 64.5 > faith 64.0; overall +1.7 points = 2.8%).
C("m02", "Which statement in the draft is supported by Table 4?",
"""
Department for Schools, Holtshire - statistical release, draft commentary

Table 4: share of pupils achieving grade 4 or above in English and maths, by school type
| School type | 2024 | 2025 |
| Academies | 62.0% | 64.5% |
| Community schools | 58.0% | 57.6% |
| Faith schools | 66.0% | 64.0% |
| Free schools | 55.0% | 60.5% |
| All state schools | 60.4% | 62.1% |

Draft commentary statements:
""" + listed(M02) + """

Release style: "percent" is relative change; "percentage points" is the difference between two percentages; figures must match to one decimal place (relative changes to the nearest whole percent). The statistician wants the one supported statement kept, or confirmation that none is supported.
""",
sents("statement", M02) + [(NONE, "no statement in the draft is supported by Table 4")],
"statement 2", 2, ordered=True),

# ------------------------------------------------------------------ m03
# why: rates 2.5 -> 5.1 is x2.04 (doubled), but repayments 897 -> 1,181 is x1.32.
Y("m03", "Is the column sentence accurate in full?",
"""
Money Matters column, Sunday Courier - fact check

Column sentence: "Mortgage rates have doubled in two years, which means monthly repayments on a typical new mortgage have doubled too."

Data (Central Bank of Aldmark and Lenders' Association):
- Average two-year fixed rate on new mortgages: September 2024: 2.5%; September 2026: 5.1%
- Monthly repayment on a typical new mortgage (200,000 borrowed over 25 years, capital and interest): September 2024: 897; September 2026: 1,181
- Average new mortgage size rose by 3% over the period

Checker's rule: "doubled" means the later figure is between 1.9 and 2.1 times the earlier one. Every factual part of a sentence must be supported for the sentence to pass.

Columnist's note: "If the rate doubles, the cost doubles. That's just maths."
""",
[("doubled", "the later figure is 1.9 to 2.1 times the earlier figure"),
 ("repayment", "the monthly payment of capital and interest, which does not rise in proportion to the interest rate")],
0, 2),

# ------------------------------------------------------------------ m04
# why: 4.2m in 2025 prices = 4.2 / 1.52 = 2.76m in 2010 prices < 3.1m -> buys less; the claim ignores inflation.
C("m04", "Which flaw, if any, is in the council's library claim?",
"""
Wendle Borough Council - "Your Council Tax Explained" leaflet, draft

Claim: "We have protected libraries. Wendle now spends 4.2 million a year on its library service, up from 3.1 million in 2010, so our library budget buys more books, staff hours and opening time than it did then."

Supporting figures from the finance team:
- Library revenue budget: 2010: 3.1 million; 2025: 4.2 million (cash)
- Consumer price index: 2010 = 100; 2025 = 152
- Costs of books and staff have risen roughly in line with consumer prices
- 2010 was a typical year for library spending; there was no one-off cut or boost
- Wendle's population grew by 4% over the period

Leaflet editor's request: name the main flaw, if any, before the leaflet goes to print.
""",
err("nominal", "pp", "count", "causal", "time", "subgroup", "base", "baseline", "mean", "none"),
"inflation ignored", 2),

# ------------------------------------------------------------------ m05
# why: only Barrowgate rose exactly 6.0 points to a figure in 50.1-51.0 (Castleview, Glebe, Juniper Hill, Victoria rose 6.0 but end elsewhere). Twin 44.6 -> none.
C("m05", "Which ward's figures match the councillor's claim?",
"""
Kelby City Council - recycling statistics, claim check for the ward newsletters

A councillor's newsletter says: "In my ward, the household recycling rate rose by 6 percentage points last year, to just over half." The newsletter does not name the ward.

Household recycling rate (%), 2024 -> 2025, by ward:
Abbotsford 41.2 -> 44.0 | Barrowgate 44.5 -> 50.5 | Castleview 43.8 -> 49.8 | Dene Park 47.6 -> 50.5
Eastwick 38.9 -> 41.0 | Fernhill 52.0 -> 53.1 | Glebe 46.9 -> 52.9 | Harcourt 35.5 -> 37.2
Ivydale 49.0 -> 50.8 | Juniper Hill 40.3 -> 46.3 | Kingsmead 55.4 -> 56.0 | Larkrise 47.7 -> 50.6
Millbrook 33.0 -> 35.9 | Northgate 45.0 -> 50.9 | Orchard Vale 42.2 -> 45.1 | Priory 50.1 -> 49.0
Queensway 39.4 -> 42.7 | Riverside 44.9 -> 48.8 | St Anne's 36.7 -> 40.2 | Thornbury 48.3 -> 51.9
Upton 51.2 -> 54.0 | Victoria 37.8 -> 43.8 | Westfield 46.2 -> 47.5 | Yewtree 43.1 -> 46.6

Checking rules: "rose by N percentage points" must match the difference to one decimal place (6 means 6.0). "Just over half" means from 50.1% to 51.0%.
""",
[(w, f"the claim matches {w}'s figures") for w in WARDS] + [(NONE, "the claim matches no ward's figures")],
"Barrowgate", 2,
twin=T([("Barrowgate 44.5 -> 50.5", "Barrowgate 44.6 -> 50.5")], NONE)),

# ------------------------------------------------------------------ m06
# why: 1 point over five years is 0.2 points a year (1 in 500 a year), not 1 in 100 every year.
Y("m06", "Does the trial support the leaflet's \"every year\" figure?",
"""
Pharmacy counter leaflet - clinical content review

Leaflet line: "Daily low-dose aspirin means 1 in 100 people avoid a heart attack every year."

Trial cited: ASPIRE-5. 12,000 adults aged 50-69 at high cardiovascular risk were randomly assigned to daily low-dose aspirin or placebo and followed for five years.
- Heart attack over five years: placebo 4.0%; aspirin 3.0%
- Major bleeding over five years: placebo 1.2%; aspirin 1.8%
The trial did not publish year-by-year results; events occurred at a similar pace across the five years.

Review rule: claims about what happens "every year" or "each year" must use annual figures. Where only multi-year figures exist and events were spread evenly, divide the absolute difference evenly across the years.

Pharmacist's note: "4% versus 3% is a difference of 1 in 100. The leaflet looks right to me."
""",
[("absolute risk reduction", "risk with placebo - risk with aspirin, over the period stated"),
 ("annual figure", "the figure for one year; here, the five-year difference divided by five")],
0, 2),

# ------------------------------------------------------------------ m07
# why: real change = 1.10 / 1.04 - 1 = 5.8% > 5%. Twin inflation 5.0% -> 4.8%.
C("m07", "What is the verdict on the property section's claim?",
"""
Tarrow Herald property section - claim check

Claim: "The median home in Tarrow rose in value by more than 5% in real terms over the past year."

Data (Tarrow Land Registry and Statistics Office):
- Median sale price, August 2025: 250,000
- Median sale price, August 2026: 275,000 (+10.0%)
- Consumer prices, August 2025 to August 2026: +4.0%
- Number of sales fell by 12% over the same period

Herald method note: the real change is (1 + cash change) / (1 + inflation) - 1. Do not subtract inflation from the cash change. The median sale price is accepted as the value of "the median home".

Sub-editor's comment: "Fewer sales means the median could be skewed. Maybe we can't say anything?"
Checker's reply: "We rate against the published figures, as the method note says."
""",
VERDICT, "supported", 2,
twin=T([("Consumer prices, August 2025 to August 2026: +4.0%", "Consumer prices, August 2025 to August 2026: +5.0%")], "refuted")),

# ------------------------------------------------------------------ m08
# why: r = 0.35 is "moderate" under the stated scale, not "strong".
Y("m08", "Is \"strong link\" an accurate description under the desk's scale?",
"""
Education desk - headline check

Proposed headline: "Study finds strong link between screen time and poor posture in children"

Study: Harwell Child Posture Study, 2,900 children aged 8-12. Daily screen time (parent-reported) and a physiotherapist's posture score were measured once. Correlation between screen time and poor posture score: r = 0.35 (95% CI 0.32 to 0.38). The correlation was similar for boys and girls.

Desk scale for describing correlations (by the size of r, ignoring sign):
- below 0.3: "weak"
- 0.3 to below 0.7: "moderate"
- 0.7 and above: "strong"
Association wording ("link") is allowed for observational studies.

Reporter's note: "The confidence interval is tiny and the sample is huge - the link is rock solid, so 'strong' is fair."
""",
[("correlation strength", "described by the size of r on the desk scale, not by how precise the estimate is"),
 ("link", "association wording, allowed for observational studies")],
0, 2),

# ------------------------------------------------------------------ m09
# why: 65+ CI (-0.4 to 1.2) includes zero, so "every age group" goes beyond the evidence; the rest are fine. Twin 65+ CI 0.2-1.6 -> none.
C("m09", "Which statement in the press release goes beyond the evidence?",
"""
Brennock University press office - release on the Green Neighbourhoods Survey, check by the research integrity officer

Study: cross-sectional survey of 12,400 adults in Brennock, 2025. Depressive symptoms measured on a 27-point scale (higher = more symptoms). Adults living within 300 metres of a public park scored 1.2 points lower on average than those living further away (95% CI 0.8 to 1.6), after adjusting for age, income and employment.
By age: 18-39: 1.5 lower (0.9 to 2.1); 40-64: 1.3 lower (0.7 to 1.9); 65 and over: 0.4 lower (-0.4 to 1.2).
By sex: women 1.3 lower (0.8 to 1.8); men 1.1 lower (0.5 to 1.7).

Press release statements:
""" + listed(M09) + """

Integrity officer's rule: a difference "held" or "was seen" in a group only if that group's 95% CI excludes zero. Association wording is acceptable for this design. If every statement is supported, say so.
""",
sents("statement", M09) + [(NONE, "every statement is supported by the evidence")],
"statement 3", 3, ordered=True,
twin=T([("65 and over: 0.4 lower (-0.4 to 1.2)", "65 and over: 0.9 lower (0.2 to 1.6)")], NONE)),

# ------------------------------------------------------------------ m10
# why: measured from the 20.00 offer price, 38.00 is x1.9 - not more than double (the x2.5 is from the June low).
Y("m10", "Measured the way the desk rule requires, have Loomwise shares more than doubled?",
"""
Markets desk - copy check, Loomwise plc

Draft sentence: "Shares in Loomwise have more than doubled since its stock-market debut in March 2025."

Price history:
- IPO offer price (March 2025): 20.00
- First-day closing price: 26.00
- Lowest close since listing (June 2025): 15.20
- Latest close (25 September 2026): 38.00
No share splits or special dividends.

Desk rule: changes "since listing" or "since its debut" are measured from the IPO offer price, not from the first-day close or any later price.

Reporter's note: "From the June low it's up 150%. And even from the offer price it's close to double."
""",
[("since its debut", "measured from the IPO offer price"),
 ("more than doubled", "the latest figure is more than twice the starting figure")],
0, 1),

# ------------------------------------------------------------------ m11
# why: night 45/1,500 = 3.0%; day 60/4,000 = 1.5% -> 2 times. The raw counts suggest the reverse.
C("m11", "How many times as likely to be injured were night-shift staff compared with day-shift staff?",
"""
Harrow Distribution Centre - health and safety committee, minutes item 4

Union representative's claim: "Night-shift staff are at far higher risk of injury than day-shift staff."
Operations manager's reply: "The numbers say the opposite. Day shift had 60 injuries last year and nights only 45."

Injury log, 2025 (reportable injuries):
- Night shift: 45 injuries; 1,500 staff employed on nights
- Day shift: 60 injuries; 4,000 staff employed on days
Every member of staff worked only one shift pattern all year, and shifts were the same length.

Committee secretary's note: the committee wants the ratio of the two injury rates, night rate divided by day rate, rounded to one significant figure, before deciding whether to commission a review.
""",
[("0.75 times", "night-shift staff were three-quarters as likely to be injured"),
 ("1.3 times", "night-shift staff were about a third more likely to be injured"),
 ("2 times", "night-shift staff were twice as likely to be injured"),
 ("3 times", "night-shift staff were three times as likely to be injured"),
 (NONE, "the correct ratio is not listed")],
"2 times", 2, ordered=True),

# ------------------------------------------------------------------ m12
# why: the authority says trends in overall crime must use the survey; the survey is not at its lowest (8.7m in 2023 < 9.1m).
Y("m12", "Is the minister's claim supported by the measure the statistics authority requires?",
"""
Home Office of Carrowmore - ministerial statement check

Minister's statement: "Crime is at its lowest level on record."

Data:
- Police recorded crime, 2025: 4.02 million offences, the lowest since the series began in 2002.
- Crime Survey for Carrowmore (household survey, began 1995): estimated 9.1 million incidents in 2025; 8.7 million in 2023 (the survey's lowest ever); 9.4 million in 2024.

Statistics Authority guidance: police recorded crime is affected by changes in recording practice and is not reliable for trends in overall crime. Claims about the level or trend of overall crime over time must use the Crime Survey. Police recorded crime may be used for specific offences the survey does not cover.

Special adviser's note: "Police figures are official statistics too, and they're at a record low."
""",
[("overall crime trend", "under Statistics Authority guidance, measured by the Crime Survey"),
 ("lowest on record", "lower than every earlier figure in the required measure")],
0, 2),

# ------------------------------------------------------------------ m13
# why: renewables = wind 28.4 + solar 9.8 + hydro 7.1 + bioenergy 5.3 = 50.6% (nuclear excluded). Twin bioenergy 4.3 -> 49.6%.
C("m13", "Considering the grid statistics, what verdict should the claim get?",
"""
Energy Ministry of Veldria - press release check

Claim: "In 2025, renewables supplied more than half of Veldria's electricity for the first time."

Grid Operator, electricity generation by source, 2025 (% of total):
- wind 28.4%
- gas 26.1%
- nuclear 14.0%
- solar 9.8%
- hydro 7.1%
- bioenergy 5.3%
- coal 6.8%
- other 2.5%
The operator confirms that the renewable share has never previously been above 50%.

Ministry definition (Energy Act, schedule 1): renewable sources are wind, solar, hydro and bioenergy. Nuclear is low-carbon but not renewable.

Opposition spokesperson: "Wind and solar together are under 40%. The claim is spin."
""",
VERDICT, "supported", 2,
twin=T([("- bioenergy 5.3%", "- bioenergy 4.3%"), ("- other 2.5%", "- other 3.5%")], "refuted")),

# ------------------------------------------------------------------ m14
# why: p = 0.21 and CI includes zero -> "significantly" is not allowed, though scores rose on average.
Y("m14", "Can the newsletter say the method \"significantly\" improved scores?",
"""
Riverside Academy Trust - parent newsletter, head of research's check

Newsletter sentence: "The new phonics method significantly improved Year 2 reading scores this year."

Evaluation: 24 Year 2 classes across the trust were randomly assigned to the new phonics method or the existing scheme for the 2025/26 school year. End-of-year reading scores were 4.1 points higher in classes using the new method (95% CI -2.3 to 10.5; p = 0.21). Teachers in the new-method classes rated it highly.

Trust style rule: "significantly" in any report of a study means statistically significant at p < 0.05. Otherwise write that scores were higher but the difference could be due to chance.

Head teacher's comment: "A 4-point gain is significant in any normal sense of the word."
""",
[("significantly", "under the trust's style rule, statistically significant at p < 0.05"),
 ("confidence interval", "the range of effects compatible with the data; one that includes zero means no effect cannot be ruled out")],
0, 1),

# ------------------------------------------------------------------ m15
# why: "typical household" uses the mean (21,400); the median is 3,800.
C("m15", "What is the main flaw, if any, in the bank's claim?",
"""
Bank of Varn - consumer savings campaign, compliance review

Campaign line: "The typical household in Varn now has more than 20,000 in savings. Is yours keeping up?"

Source: Varn Household Wealth Survey 2025 (representative sample of 9,200 households):
- Mean household savings: 21,400
- Median household savings: 3,800
- 30% of households have no savings at all
- The top 10% of households hold 71% of all savings

Compliance note: "typical" in marketing means the median household, as set out in the bank's advertising code. The survey is current and covers all households in Varn.
""",
[ERR[k] for k in ("mean", "nominal", "pp", "rel", "causal", "time", "subgroup", "count", "base", "baseline", "simpson")] + [ERR["none"]],
"average used for the typical case", 2),

# ------------------------------------------------------------------ m16
# why: 240 / 16 = 15 -> "about 15 times as likely" holds, whatever the small absolute difference.
Y("m16", "Does the registry support the campaign's \"about 15 times as likely\" statement?",
"""
Varn Cancer Registry - campaign claim review

Campaign poster: "Current smokers in Varn are about 15 times as likely to develop lung cancer as people who have never smoked."

Registry data, adults aged 40 and over, average of 2021-2025 (new lung cancer cases per 100,000 people per year):
- Current smokers: 240
- Former smokers: 70
- Never smokers: 16

Review rule: "about N times as likely" is accepted if the ratio of the two rates is within 10% of N. Comparisons between smokers and never-smokers may use association wording.

Reviewer's objection: "The yearly difference is only about a quarter of a percentage point. Saying '15 times' is scaremongering and should be struck out."
""",
[("ratio of rates", "the rate in one group divided by the rate in the other"),
 ("about N times as likely", "the ratio is within 10% of N")],
1, 1),

# ------------------------------------------------------------------ m17
# why: 79.4% beats the previous series high of 78.9% (Q4 2007). Twin: previous high 79.6% -> refuted.
C("m17", "What verdict does the claim about women aged 25-34 receive?",
"""
Labour market bulletin - claim review

Claim in the employment minister's speech: "Employment among women aged 25 to 34 hit a record high in the second quarter of 2026."

Carrowmore Labour Force Survey, employment rate for women aged 25-34 (seasonally adjusted, series begins 1992):
- Q2 2026: 79.4%
- Q1 2026: 78.6%
- Highest quarter before 2026: Q4 2007, 78.9%
- Overall employment rate, all adults 16-64, Q2 2026: 75.1% (below its Q4 2019 record of 76.2%)

Review rule: "record high" means higher than every earlier figure in the series. A claim is rated only on the group it names.

Opposition researcher: "Employment is nowhere near its record - overall it's more than a point below 2019."
""",
VERDICT, "supported", 2,
twin=T([("Highest quarter before 2026: Q4 2007, 78.9%", "Highest quarter before 2026: Q4 2007, 79.6%")], "refuted")),

# ------------------------------------------------------------------ m18
# why: 6,300 is more than half of 12,000, so the backlog has not halved by the ministry's definition.
Y("m18", "Has the backlog halved, as the ministry defines it?",
"""
Planning Inspectorate of Aldmark - minister's press statement check

Minister's statement (1 August 2026): "We have halved the planning appeals backlog since January."

Backlog of undecided appeals (Inspectorate monthly figures, first working day of each month):
- January 2026: 12,000
- April 2026: 8,900
- July 2026: 6,300
- August 2026: 6,250

Ministry style guide: "halved" means the new figure is no more than half of the old figure. "Nearly halved" may be used where the new figure is within 10% above half.

Press officer's note: "We've cleared nearly 6,000 cases. Everyone will understand 'halved'."
""",
[("halved", "the new figure is no more than half of the old figure"),
 ("nearly halved", "the new figure is above half but within 10% above it")],
0, 1),

# ------------------------------------------------------------------ m19
# why: 1,200 -> 840 is a 30% fall; "a third" (33.3%) is 11% off -> mostly accurate. Twin 900 (25% fall) -> overstates by 33% -> exaggerated.
C("m19", "What rating does the claim get on the Carrow Fact Desk scale?",
"""
Carrow Fact Desk - rating scale for numeric claims
Compute the error as |claimed figure - correct figure| / correct figure, using the relative change for claims in percent or fractions.
- accurate: error of 5% or less
- mostly accurate: error over 5%, up to 15%
- exaggerated: error over 15%, and the claim overstates the change in the direction it gives
- inaccurate: error over 15% and the claim understates the change, or the claim gives the wrong direction

Claim (police commissioner, radio interview): "Knife crime among under-18s in Carrow fell by a third last year."

Source (Carrow Police, offences involving a knife where the suspect was under 18):
- 2024: 1,200
- 2025: 840
""",
[("accurate", "error of 5% or less"),
 ("mostly accurate", "error over 5% and up to 15%"),
 ("exaggerated", "error over 15%, overstating the change"),
 ("inaccurate", "error over 15%, understating the change or giving the wrong direction")],
"mostly accurate", 3, ordered=True,
twin=T([("- 2025: 840", "- 2025: 900")], "exaggerated")),

# ------------------------------------------------------------------ m20
# why: the difference (7.1% vs 6.8%) is not statistically significant, which the rule requires for "more likely".
Y("m20", "Under the desk's comparison rule, can the headline say women are more likely to be fraud victims?",
"""
Consumer affairs desk - headline check

Proposed headline: "Women more likely than men to fall victim to online fraud, survey finds"

Source: Tessary Crime and Safety Survey 2025, 34,000 adults. Victims of online fraud in the past 12 months:
- Women: 7.1%
- Men: 6.8%
- Difference 0.3 points (95% CI -0.4 to 1.0); the survey report describes the difference as not statistically significant.
- Adults aged 75 and over: 9.4% (significantly higher than every other age group)

Desk comparison rule: survey comparisons ("more likely", "less likely", "higher than") may be reported only if the difference is statistically significant. Otherwise report that rates were similar.
""",
[("survey comparison", "a statement that one group is more or less likely than another, allowed only if the difference is statistically significant")],
0, 1),

# ------------------------------------------------------------------ m21
# why: 20,500 -> 8,200 = -60% (not points, not two-thirds); rate 140/360 = 38.9% (not under a third); "youth crime" is not first-time entrants; 8,200 is not fewer than 8,000. Twin 7,900 -> E.
C("m21", "Which sentence can the youth justice briefing use unchanged?",
"""
Youth Justice Board of Tessary - briefing for the minister, sentence check

Data (Youth Justice Statistics, calendar years):
- First-time entrants to the youth justice system (aged 10-17): 2015: 20,500; 2025: 8,200
- First-time entrant rate per 100,000 people aged 10-17: 2015: 360; 2025: 140
- Proven offences by young people (all offences, not only first-time entrants): 2015: 61,000; 2025: 39,000

Candidate sentences:
""" + listed(M21) + """

Board style: "percent" means relative change; "percentage points" only for differences between percentages. Each sentence must match the measure it names.
""",
sents("sentence", M21) + [(NONE, "no candidate sentence can be used unchanged")],
NONE, 3, ordered=True,
twin=T([("2015: 20,500; 2025: 8,200", "2015: 20,500; 2025: 7,900")], "sentence E")),

# ------------------------------------------------------------------ m22
# why: 42 / 198 = 21.2% of all exports -> more than a fifth. The 20% growth figure is a distractor.
Y("m22", "Do the trade figures support the claim that exports to Veldria are more than a fifth of all exports?",
"""
Trade Ministry of Holt - speech fact check

Draft speech line: "Exports to Veldria now account for more than a fifth of all Holt's exports."

Holt Customs Agency, goods and services exports, 2025 (billions of crowns):
- Total exports: 198
- to Veldria: 42 (up 20% on 2024)
- to Morvane: 37
- to Aldmark: 29
- to all other destinations: 90

Adviser's note: "The 20% is growth, not share. I'm not sure what the share is - please check before the speech."

Checker's rule: a share of a total is the part divided by the whole for the same year and the same measure.
""",
[("share of exports", "exports to one destination / total exports, same year and measure")],
1, 1),

# ------------------------------------------------------------------ m23
# why: women admitted at a higher rate in both faculties (65% vs 60%, 25% vs 20%) but at a lower pooled rate (33% vs 52%).
C("m23", "What is the main flaw, if any, in the student newspaper's conclusion?",
"""
Brennock University student newspaper - article under review by the editor

Article excerpt: "New figures show women who applied to Brennock were admitted at a much lower rate than men: 33% against 52%. The admissions data show women were less likely than men to get a place in the university's faculties."

Admissions data, 2026 entry (the university has two faculties; each applicant applies to one):
- Engineering: men 800 applied, 480 admitted (60%); women 200 applied, 130 admitted (65%)
- Arts: men 200 applied, 40 admitted (20%); women 800 applied, 200 admitted (25%)
- Total: men 1,000 applied, 520 admitted (52%); women 1,000 applied, 330 admitted (33%)

Editor's note: "Name the main problem with the conclusion, if there is one. The article doesn't claim anyone discriminated."
""",
err("simpson", "count", "base", "eco", "causal", "pp", "time", "subgroup", "none"),
"aggregation reversal ignored", 3),

# ------------------------------------------------------------------ m24
# why: the official measure (LFS rate) is higher now (4.4% vs 4.1%); the claimant count is not the official measure.
Y("m24", "Does the official measure support the minister's claim?",
"""
Statistics Watchdog of Aldmark - complaint 26/77

Minister's claim (parliament, 9 September 2026): "Unemployment is lower today than when this government took office."

Figures:
- Labour Force Survey unemployment rate: 4.1% in the quarter before the government took office (Q2 2024); 4.4% in the latest quarter (May-July 2026)
- Claimant count (people claiming unemployment benefits): 612,000 in June 2024; 571,000 in August 2026. Eligibility rules for the benefit were tightened in 2025.

Watchdog guidance: the Labour Force Survey unemployment rate is the official measure of unemployment. The claimant count may be quoted only if named as the claimant count.

Minister's office: "Fewer people are claiming. Unemployment is down, full stop."
""",
[("official unemployment measure", "the Labour Force Survey unemployment rate"),
 ("claimant count", "the number of people claiming unemployment benefits, which also depends on eligibility rules")],
0, 1),

# ------------------------------------------------------------------ m25
# why: deaths 312 -> 276 = -11.5% (> 10%); the per-km rate is a distractor since the claim is about deaths. Twin 284 -> -9.0%.
C("m25", "What verdict does the transport department's claim receive?",
"""
Tollan Transport Department - road safety annual report, figures check

Claim: "Deaths on Tollan's roads fell by more than 10% last year."

Road casualty statistics (police reports, calendar years):
- Deaths: 2024: 312; 2025: 276
- Deaths per billion vehicle-kilometres: 2024: 6.2; 2025: 5.7
- Serious injuries: 2024: 4,410; 2025: 4,380
- Traffic volume fell by about 4% in 2025 because of a fuel price spike

Checker's rule: "fell by more than X%" is a relative change in the measure the claim names. Claims about deaths are checked on the number of deaths.

Road safety charity's comment: "Adjusted for traffic, deaths only fell about 8%. The claim overstates progress."
""",
VERDICT, "supported", 2,
twin=T([("Deaths: 2024: 312; 2025: 276", "Deaths: 2024: 312; 2025: 284")], "refuted")),

# ------------------------------------------------------------------ m26
# why: the claim names the after-housing-costs measure (23.8%), which is not "one in five"; 19.4% is before housing costs.
Y("m26", "Does the poverty statistic support the leaflet's figure?",
"""
Carrow Child Poverty Action - leaflet check

Leaflet line: "One in five children in Carrow lives in relative poverty after housing costs."

Source: Carrow Households Below Average Income report, 2024/25:
- Children in relative poverty, before housing costs: 19.4%
- Children in relative poverty, after housing costs: 23.8%
- Children in absolute poverty, after housing costs: 17.9%

Checker's rule: "one in N" is accepted if the figure is within 1 percentage point of 100/N percent, using the measure the sentence names.

Volunteer's note: "19.4 is basically 20. One in five is fine."
""",
[("before housing costs", "income measured before rent or mortgage costs are paid"),
 ("after housing costs", "income measured after rent or mortgage costs are paid; this is the measure the leaflet names")],
0, 2),
]
