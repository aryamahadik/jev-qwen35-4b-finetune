"""evidence_claims_b / time-bounded claims: "every year since", records, fiscal vs calendar years,
rolling windows, consecutive runs, "since X came in", deadlines, series breaks."""
from _lib import C, Y, T, VERDICT, err, NONE

MONTHS25 = ["January 2025", "February 2025", "March 2025", "April 2025", "May 2025", "June 2025",
            "July 2025", "August 2025", "September 2025", "October 2025", "November 2025", "December 2025"]

ITEMS = [
# ------------------------------------------------------------------ t01
# why: every year 2020-2025 lower than the year before -> yes, despite the 2019 mention. Twin makes 2022 a rise.
Y("t01", "Is the police commissioner's claim accurate for the years it covers?",
"""
Office of the Police and Crime Commissioner, Wexmoor - annual statement, fact check before release

Commissioner's claim: "Recorded crime in Wexmoor has fallen every year since 2019."

Recorded crimes per 1,000 residents (Wexmoor Constabulary, calendar years, final figures):
- 2018: 57.4
- 2019: 58.2
- 2020: 55.1
- 2021: 53.9
- 2022: 52.6
- 2023: 51.0
- 2024: 49.3
- 2025: 47.8
Figures for 2026 are not yet available.

Checker's rule: "has fallen every year since X" means each annual figure after X is lower than the figure for the year before it, up to the latest complete year. The figure for X itself need not be lower than the year before X.

Journalist's note: "2019 was higher than 2018, so the run can't start in 2019."
""",
[("fallen every year since X", "each annual figure after year X is lower than the previous year's, up to the latest complete year")],
1, 2,
twin=T([("- 2022: 52.6", "- 2022: 54.4")], 0)),

# ------------------------------------------------------------------ t02
# why: series begins 2004, so "30 years" reaches past the data. Twin "20 years" is inside it.
C("t02", "Taking the statistics office table as the only evidence, what verdict does the claim get?",
"""
Youth services briefing - Harrowmere Regional Assembly, claims register

Claim by the youth services minister: "Youth unemployment in Harrowmere is now at its lowest level in 30 years."

Source: Harrowmere Statistics Office, unemployment rate among 16-24-year-olds (annual averages). The series begins in 2004; no earlier comparable figures exist for the region.
- 2004: 17.8%
- 2008: 15.2%
- 2012: 21.4%
- 2016: 16.9%
- 2020: 18.3%
- 2024: 12.6%
- 2025: 11.9%
The office confirms that 2025 is the lowest annual figure in the series and that no year not shown was lower than 11.9%.

Register rule: claims are checked only against official statistics; a claim about a period that the statistics do not cover cannot be confirmed from them.
""",
VERDICT, "not enough information", 2,
twin=T([("at its lowest level in 30 years", "at its lowest level in 20 years")], "supported")),

# ------------------------------------------------------------------ t03
# why: calendar 2025 = 1,350+1,250+1,300+1,200 = 5,100, not > 5,200 (FY 2025/26 is 5,300). Twin Jan-Mar 2025 1,500 -> 5,250.
Y("t03", "Is the claim about calendar year 2025 correct?",
"""
Brockhaven City Council - planning statistics, press office query

Draft press line: "In calendar year 2025 the city approved more than 5,200 new homes - a record."

Planning approvals (new homes), by quarter. The council's financial year runs April to March.
Financial year 2024/25:
- Apr-Jun 2024: 1,100
- Jul-Sep 2024: 1,210
- Oct-Dec 2024: 1,150
- Jan-Mar 2025: 1,350
Financial year 2025/26:
- Apr-Jun 2025: 1,250
- Jul-Sep 2025: 1,300
- Oct-Dec 2025: 1,200
- Jan-Mar 2026: 1,550

Press officer's note: "The annual report gives 5,300 approvals for 2025/26, so 'more than 5,200 in 2025' is safe."
Checker's note: only the "more than 5,200" part is being checked today; the "record" part is with the statistics team.
""",
[("calendar year", "January to December"),
 ("financial year", "for this council, April of one year to March of the next")],
0, 2,
twin=T([("Jan-Mar 2025: 1,350", "Jan-Mar 2025: 1,500")], 1)),

# ------------------------------------------------------------------ t04
# why: May 3.0 is not "below 3"; the first six-month run is June-November. Twin May 2.9 -> run March-August.
C("t04", "Which month's figure first makes the minister's statement true?",
"""
Treasury of Aldmark - speechwriting unit, fact check

The finance minister wants to say, as soon as it is true: "Inflation has now been below 3% for six months in a row."

Annual consumer price inflation, by month (Aldmark Statistics Agency, final figures):
Jan 3.4% | Feb 3.1% | Mar 2.9% | Apr 2.8% | May 3.0% | Jun 2.7%
Jul 2.6% | Aug 2.9% | Sep 2.5% | Oct 2.4% | Nov 2.8% | Dec 2.6%
(All months are 2025. December 2024 was 3.6%.)

Rule from the speechwriting unit's checklist: "below 3%" means strictly less than 3.0%. "Six months in a row" means six consecutive monthly figures, ending with the latest month referred to.

Question from the minister's office: which is the first month whose figure completes a run of six consecutive months below 3%?
""",
[(m, f"the six-month run is first completed by the {m} figure") for m in MONTHS25] + [(NONE, "no run of six consecutive months below 3% occurs in 2025")],
"November 2025", 2, ordered=True,
twin=T([("May 3.0%", "May 2.9%")], "August 2025")),

# ------------------------------------------------------------------ t05
# why: 15 June to 23 September inclusive = 16 + 31 + 31 + 23 = 101 days. Twin 20 September = 98.
Y("t05", "On the date of the statement, is the \"more than 100 days\" claim correct?",
"""
Ministry of Health, Vessa Islands - statement check

Statement to be read by the chief medical officer on 23 September 2026:
"We have now gone more than 100 days without a single new case of measles reported anywhere in the islands."

Surveillance log (national notifiable diseases system):
- Last measles case reported: 14 June 2026 (confirmed by laboratory on 16 June)
- No measles notifications since that report
- Next scheduled surveillance report: 30 September 2026

Counting rule in the ministry's style guide: the number of days "without a new case" is the number of full days after the day the last case was reported, up to and including the day of the statement. Laboratory confirmation dates are not used for counting.

Press officer's comment: "June to September is three months, so roughly 90 days. I'd drop the line."
""",
[("days without a new case", "full days after the day the last case was reported, up to and including the statement date")],
1, 2,
twin=T([("read by the chief medical officer on 23 September 2026", "read by the chief medical officer on 20 September 2026")], 0)),

# ------------------------------------------------------------------ t06
# why: real 2026 = 690/1.18 = 584.7 < 2021's 600.0 -> not a real-terms record. Twin 715 -> 605.9.
C("t06", "What verdict fits the claim about real pay?",
"""
Coldmere Business Review - fact-check panel

Claim by the chamber of commerce president: "Average weekly pay is now at a record high in real terms."

Source: Coldmere Statistics Office. Average weekly pay (cash, crowns) and consumer price index (2021 = 100). Real pay in 2021 prices = cash pay / CPI x 100.
| Year | Cash pay | CPI |
| 2015 | 520 | 90.0 |
| 2018 | 560 | 95.0 |
| 2021 | 600 | 100.0 |
| 2024 | 650 | 112.0 |
| 2026 | 690 | 118.0 |
The table shows selected years from the full 2010-2026 series. The office confirms that in no year not shown did real pay exceed its 2021 level, and that 2026 cash pay is the highest in the series.

Panel member's note: "690 is the highest pay figure there has ever been. Seems like a straightforward yes."
""",
VERDICT, "refuted", 2,
twin=T([("| 2026 | 690 | 118.0 |", "| 2026 | 715 | 118.0 |")], "supported")),

# ------------------------------------------------------------------ t07
# why: "fell in March" = month-on-month by rule; index 124.60 -> 124.35 is a fall despite 2.8% annual inflation. Twin 124.70.
Y("t07", "Under the office's convention, is the headline accurate?",
"""
Norlund Statistics Office - media monitoring note

Headline in the Norlund Daily: "Prices in Norlund fell in March"

Consumer price index (2020 = 100), published 15 April:
- February 2026: 124.60
- March 2026: 124.35
- March 2025: 120.96
Annual inflation (March 2026 vs March 2025): 2.8%.

A reader has complained: "Inflation is 2.8%. Prices obviously did not fall - the headline is false."

Office convention for describing price movements: "rose in [month]" or "fell in [month]" refers to the change in the index from the previous month. Changes over twelve months are described as "annual inflation" or "compared with a year earlier". The index is seasonally unadjusted, which is the standard basis for this description.
""",
[("change in a month", "the change in the index from the previous month's value"),
 ("annual inflation", "the change in the index compared with the same month a year earlier")],
1, 2,
twin=T([("- March 2026: 124.35", "- March 2026: 124.70")], 0)),

# ------------------------------------------------------------------ t08
# why: last fall is 2020 (432,900 < 433,400), so the earliest valid X is 2020. Twin removes that fall -> 2017.
C("t08", "What is the earliest year X for which \"our population has grown every year since X\" is true?",
"""
Mayor's State of the City speech - research team check

Draft line: "Our population has grown every single year since 2015."

Mid-year population estimates, City of Ellingford (Regional Statistics Service):
2010: 412,300 | 2011: 415,100 | 2012: 418,900 | 2013: 417,600
2014: 420,200 | 2015: 423,000 | 2016: 426,500 | 2017: 426,100
2018: 429,800 | 2019: 433,400 | 2020: 432,900 | 2021: 435,700
2022: 439,300 | 2023: 442,800 | 2024: 446,100 | 2025: 449,900

Research team rule: "has grown every year since X" is true if every annual figure after X is higher than the figure for the year before it, through the latest year (2025). The speechwriter wants the earliest year X for which the line is true, so that the line can be corrected rather than dropped.
""",
[(str(y), f"the line is first true with X = {y}") for y in range(2013, 2025)] + [(NONE, "the line is not true for any year listed")],
"2020", 2, ordered=True,
twin=T([("2020: 432,900", "2020: 434,100")], "2017")),

# ------------------------------------------------------------------ t09
# why: births never exceeded deaths in 2015-2024 -> "first time in a decade" holds. Twin: 2016 had more births.
Y("t09", "Does the vital statistics table bear out the press release?",
"""
Ostvale Regional Health Board - press release draft, statistics check

Draft: "In 2025, for the first time in a decade, Ostvale recorded more births than deaths."

Vital statistics, Ostvale region (registered births and deaths, calendar years):
- 2014: births 18,700; deaths 18,420
- 2015: births 18,210; deaths 18,640
- 2016: births 18,240; deaths 18,330
- 2017: births 17,980; deaths 18,720
- 2018: births 17,650; deaths 18,590
- 2019: births 17,400; deaths 18,610
- 2020: births 16,980; deaths 19,870
- 2021: births 17,120; deaths 19,240
- 2022: births 16,870; deaths 18,990
- 2023: births 16,720; deaths 18,880
- 2024: births 16,900; deaths 18,950
- 2025: births 19,020; deaths 18,870

Board style rule: "for the first time in a decade" refers to the ten calendar years before the year described.
""",
[("first time in a decade", "the event did not happen in any of the ten calendar years before the year described")],
1, 2,
twin=T([("2016: births 18,240; deaths 18,330", "2016: births 18,540; deaths 18,330")], 0)),

# ------------------------------------------------------------------ t10
# why: year-to-date comparison 1,204 vs 1,251 -> down. June alone and 2025 vs 2024 are distractors. Twin 1,268.
C("t10", "Which verdict should the police press office give its own claim?",
"""
Calder Valley Police - press office, claim check (drafted 12 July 2026)

Draft claim for the summer newsletter: "Burglaries in Calder Valley are down this year."

Recorded residential burglaries:
- January-June 2025: 1,251
- January-June 2026: 1,204
- June 2025 alone: 198
- June 2026 alone: 231
- Full year 2024: 2,480
- Full year 2025: 2,540

Press office standard: a claim about "this year" made during the year is checked on year-to-date figures against the same months of the previous year. Single-month comparisons may only be described as such.

Duty inspector's comment: "June was up and last year was worse than 2024. I'm not comfortable saying burglaries are down."
""",
VERDICT, "supported", 2,
twin=T([("January-June 2026: 1,204", "January-June 2026: 1,268")], "refuted")),

# ------------------------------------------------------------------ t11
# why: Sep 2025-Aug 2026 = 19.6 - 13.1 + 13.9 = 20.4 million. Twin 13.4 -> 19.9.
Y("t11", "Is the airport's claim about the past 12 months accurate?",
"""
Port Kessel Airport - press release, 15 September 2026, statistics check

Claim: "Over the past 12 months, Port Kessel handled more than 20 million passengers for the first time."

Passenger statistics published by the airport authority (monthly data are published about two weeks after month end; August 2026 is the latest month available):
- Calendar year 2024: 18.7 million
- Calendar year 2025: 19.6 million
- January-August 2025: 13.1 million
- January-August 2026: 13.9 million

Airport style rule: "the past 12 months" means the latest 12 months for which data are published. Only the "more than 20 million" part of the claim is being checked.

Comment from the airport's finance team: "Our best-ever year was 19.6 million in 2025, so we have never reached 20 million."
""",
[("past 12 months", "the latest 12 months of published data, here September 2025 to August 2026")],
1, 3,
twin=T([("January-August 2026: 13.9 million", "January-August 2026: 13.4 million")], 0)),

# ------------------------------------------------------------------ t12
# why: the data only start in 2019; "past decade" reaches back to 2015.
C("t12", "Which flaw, if any, is in the candidate's leaflet claim?",
"""
Local election leaflet - fact-check request from the Brenmouth Observer

Leaflet claim: "Knife crime in Brenmouth has doubled over the past decade."

Source cited on the leaflet: Brenmouth Police knife crime statistics.
Offences involving a knife or sharp instrument (calendar years):
- 2019: 1,020
- 2021: 1,390
- 2023: 1,810
- 2025: 2,080
Footnote in the police release: "A new recording system was introduced in 2019. Figures for earlier years are not available on a comparable basis and are not published."

Brenmouth's population grew by about 3% between 2019 and 2025. The police release does not break figures down by age or area.

Editor's request: name the single main flaw, if any.
""",
err("time", "pp", "count", "causal", "subgroup", "none"),
"wrong time window", 2),

# ------------------------------------------------------------------ t13
# why: 2026 at 18.9 beats 2003's 18.7 -> hottest on record. Twin: 2003 also 18.9 -> joint, not "hottest".
Y("t13", "Can the forecaster's line be used under the met office's rule?",
"""
Aldercombe Meteorological Office - broadcast script check, 1 September 2026

Forecaster's line: "This has been the hottest summer on record for Aldercombe."

Mean summer temperature (June-August), Aldercombe station, records beginning 1961 - five warmest summers:
- 2026: 18.9°C
- 2003: 18.7°C
- 2018: 18.6°C
- 1976: 18.5°C
- 2022: 18.4°C

Met office rule: a summer is "the hottest on record" only if its mean is strictly higher than every previous summer in the record, compared at one decimal place. If it equals the previous highest, it must be described as "joint hottest". The 2026 figure is final.

Producer's note: "Records only go back to 1961, so we should say 'since 1961', but that's a separate style point - it's not what we're checking."
""",
[("hottest on record", "strictly higher than every previous value in the record, at one decimal place"),
 ("joint hottest", "equal to the previous highest value in the record")],
1, 1,
twin=T([("- 2003: 18.7°C", "- 2003: 18.9°C")], 0)),

# ------------------------------------------------------------------ t14
# why: Q3 2025 fell, so the current run is Q4 2025-Q2 2026 = 3. Twin makes Q3 2025 growth -> Q4 2024 to Q2 2026 = 7 (Q3 2024 is 0.0).
C("t14", "How many consecutive quarters of growth does the economy have up to Q2 2026?",
"""
Finance Ministry of Varrow - speech check

Draft line: "Today's figures show the sixth consecutive quarter of growth."

Quarter-on-quarter change in real GDP, Varrow National Statistics (latest estimates):
- Q1 2024: +0.2%
- Q2 2024: +0.1%
- Q3 2024: 0.0%
- Q4 2024: +0.3%
- Q1 2025: +0.4%
- Q2 2025: +0.2%
- Q3 2025: -0.1%
- Q4 2025: +0.1%
- Q1 2026: +0.3%
- Q2 2026: +0.2% (published today)

Statistics definitions: growth in a quarter means a quarter-on-quarter change above 0.0%. A run of consecutive quarters of growth ends with the latest quarter and counts back until a quarter without growth.
""",
[("2", "two consecutive quarters of growth"),
 ("3", "three consecutive quarters of growth"),
 ("4", "four consecutive quarters of growth"),
 ("6", "six consecutive quarters of growth"),
 ("7", "seven consecutive quarters of growth"),
 (NONE, "the correct count is not listed")],
"3", 2, ordered=True,
twin=T([("Q3 2025: -0.1%", "Q3 2025: +0.1%")], "7")),

# ------------------------------------------------------------------ t15
# why: measured from June 2025 (last full month before 1 July), 84,000 -> 80,400 is -4.3%, not -18%.
Y("t15", "Is the 18% figure accurate for the period since the charge took effect?",
"""
Transport for Ravensholm - annual report, figures check

Draft sentence: "Since the congestion charge came in, weekday traffic entering the central zone has fallen 18%."

Average weekday vehicles entering the zone (automatic counters):
- February 2025: 98,000
- March 2025: 93,500 (charge announced 3 March 2025)
- June 2025: 84,000
- July 2025: 81,200 (charge took effect 1 July 2025)
- December 2025: 79,900
- August 2026: 80,400

Report style rule: a change "since [a policy] came in" is measured from the last full month before the policy took effect to the latest month available.

Analyst's note: "Counters show traffic started falling as soon as the charge was announced, as firms changed delivery times. From February to now it's 18%."
""",
[("since the policy came in", "measured from the last full month before the policy took effect to the latest month available")],
0, 2),

# ------------------------------------------------------------------ t16
# why: fare went 2.00 -> 1.80 -> 2.00, so it rose in 2025 even though it is back to its 2022 level. Twin "no higher than in 2022" is true.
C("t16", "Rate the operator's statement against the fares history.",
"""
Consumer Transport Watch - claim review, Greenline Buses

Operator's statement (September 2026): "The standard adult single fare has not risen since 2022."

Fares history (standard adult single, in crowns, effective 1 January each year unless noted):
- 2022: 2.00
- 2023: 1.80 (reduced under a government fare-support scheme)
- 2024: 1.80
- 2025: 2.00 (fare-support scheme ended; fare set by operator)
- 2026: 2.00
No other fare changes occurred between these dates.

Greenline's spokesperson: "Passengers pay exactly what they paid in 2022. The support scheme was temporary."

Watch's rule: "has not risen since [year]" is false if the fare increased at any point after that year, whatever the starting level.
""",
VERDICT, "refuted", 2,
twin=T([("The standard adult single fare has not risen since 2022.", "The standard adult single fare is no higher than it was in 2022.")], "supported")),

# ------------------------------------------------------------------ t17
# why: promise 12 March 2024 + 18 months = 12 September 2025; opened 2 September 2025 -> within. Twin 2 October -> late.
Y("t17", "Did the clinic open within the promised time?",
"""
Parliamentary fact-check service - question from the Health Committee

Minister's statement (committee hearing, June 2026): "I promised this clinic within 18 months, and we delivered it within 18 months."

Record of the promise: speech at the Hallam Road site on 12 March 2024. Transcript: "I promise you that within 18 months from today, this site will be an open, working community clinic."

Opening: the Hallam Road Community Clinic saw its first patients on 2 September 2025. An official ribbon-cutting took place on 30 October 2025.

Service rule: a period of N months from a date ends on the same day of the month N months later. A clinic counts as open on the day it first sees patients.

Committee member's note: "The official opening was in late October, so the promise was broken."
""",
[("period of N months from a date", "ends on the same day of the month N months later"),
 ("opening date", "the day the clinic first sees patients")],
1, 1,
twin=T([("saw its first patients on 2 September 2025", "saw its first patients on 2 October 2025")], 0)),

# ------------------------------------------------------------------ t18
# why: Q3 2025 is a tie (35.1 = 35.1), so EVs first exceed petrol in Q4 2025. Twin Q3 electric 35.4 -> Q3 2025.
C("t18", "In which quarter did electric cars' share of new registrations first exceed petrol's?",
"""
Motor Traders Federation of Estland - press release check

Draft press release: "Electric cars overtook petrol cars in Estland in Q3 2025 and have stayed ahead ever since."

Share of new car registrations (Estland Vehicle Licensing Agency):
- Q1 2025 - electric 31.0%, petrol 36.2%
- Q2 2025 - electric 33.5%, petrol 35.0%
- Q3 2025 - electric 35.1%, petrol 35.1%
- Q4 2025 - electric 36.8%, petrol 33.9%
- Q1 2026 - electric 35.9%, petrol 36.0%
- Q2 2026 - electric 37.4%, petrol 33.2%
Shares are rounded by the agency to one decimal place; the agency does not publish more precise figures.

Federation rule: electric "exceeds" petrol in a quarter only if its published share is strictly higher. This question is only about the first quarter in which that happened.
""",
[("Q1 2025", "electric first exceeded petrol in Q1 2025"),
 ("Q2 2025", "electric first exceeded petrol in Q2 2025"),
 ("Q3 2025", "electric first exceeded petrol in Q3 2025"),
 ("Q4 2025", "electric first exceeded petrol in Q4 2025"),
 ("Q1 2026", "electric first exceeded petrol in Q1 2026"),
 ("Q2 2026", "electric first exceeded petrol in Q2 2026"),
 (NONE, "electric has not exceeded petrol in any quarter shown")],
"Q4 2025", 2, ordered=True,
twin=T([("Q3 2025 - electric 35.1%", "Q3 2025 - electric 35.4%")], "Q3 2025")),

# ------------------------------------------------------------------ t19
# why: monthly claims use seasonally adjusted figures; SA fell 0.4% although raw sales jumped 18%. Twin SA +0.3%.
Y("t19", "Is the bulletin's sentence correct under the statistics office's convention?",
"""
Brisk Retail Bulletin - sentence check

Sentence: "Retail sales in Tessary rose in December."

Tessary Statistics Office, retail sales volume, December 2025 release:
- Not seasonally adjusted: December up 18.0% on November
- Seasonally adjusted: December down 0.4% on November
- Seasonally adjusted, December 2025 vs December 2024: up 1.9%

Office convention: descriptions of movement from one month to the next ("rose in December", "fell in March") use seasonally adjusted figures, because unadjusted figures mostly reflect regular seasonal patterns such as Christmas shopping. Year-on-year comparisons may use either series if labelled.

Bulletin editor: "Tills were ringing all December. Of course sales rose."
""",
[("seasonally adjusted", "figures with regular calendar effects, such as Christmas, removed"),
 ("month-to-month movement", "under the office convention, described using seasonally adjusted figures")],
0, 2,
twin=T([("Seasonally adjusted: December down 0.4% on November", "Seasonally adjusted: December up 0.3% on November")], 1)),

# ------------------------------------------------------------------ t20
# why: August 2019 has no count, so "more than any previous August" cannot be confirmed or denied. Twin fills 2019 with 489.
C("t20", "What verdict does the tourism board's claim get on the counts provided?",
"""
Kelmouth Tourism Board - claims check for the September newsletter

Claim: "More visitors came to Kelmouth this August than in any previous August."

Visitor counts at the three harbour gateways (thousands). Counting began in August 2011.
2011: 412 | 2012: 425 | 2013: 431 | 2014: 440 | 2015: 452
2016: 470 | 2017: 481 | 2018: 498 | 2019: no count (counting staff on strike)
2020: 301 | 2021: 388 | 2022: 455 | 2023: 476 | 2024: 490 | 2025: 495
2026: 503

Board's checking rule: claims are checked against the gateway counts only; estimates from hotel occupancy or other sources may not be used to fill gaps.

Communications manager: "2019 was an ordinary year. It won't have beaten 503."
""",
VERDICT, "not enough information", 2,
twin=T([("2019: no count (counting staff on strike)", "2019: 489")], "supported")),

# ------------------------------------------------------------------ t21
# why: from September 2022 (last month before 25 October 2022), 5.0 -> 6.8 = +36% > a third. From October it's exactly a third. Twin Sep 5.2.
Y("t21", "Is the opposition's claim correct when measured the way the rule requires?",
"""
Independent Fact Service of Carrowmore - claim 26-311

Opposition health spokesperson: "Under this government the hospital waiting list has grown by more than a third."

The government took office on 25 October 2022.

Waiting list (patients waiting at the end of each month, Carrowmore Health Service):
- August 2022: 4.9 million
- September 2022: 5.0 million
- October 2022: 5.1 million
- June 2026: 6.8 million (latest)

Service rule for "under this government" claims: measure from the last month that ended before the government took office to the latest month available.

Government spokesperson's rebuttal: "From our first month, October 2022, the list has grown by exactly a third, not more. The claim is false."
""",
[("measurement start", "the last month that ended before the government took office"),
 ("more than a third", "an increase greater than 33.3%")],
1, 3,
twin=T([("- September 2022: 5.0 million", "- September 2022: 5.2 million")], 0)),

# ------------------------------------------------------------------ t22
# why: Sep 2025-Aug 2026 months at or under 18:00 = Nov, Mar, Apr, May, Jul, Aug = 6. Twin Jun 2026 17:52 -> 7.
C("t22", "In how many of the 12 months covered by the chief executive's claim was the target met?",
"""
Westerby Ambulance Service - board paper, performance statement check

Chief executive's statement (board meeting, 10 September 2026): "We met our 18-minute response target in most months of the past year."

Mean response time for urgent calls (minutes:seconds). Target: 18:00 or less. August 2026 is the latest published month.
Jun 2025 17:40 | Jul 2025 17:55 | Aug 2025 17:30
Sep 2025 18:20 | Oct 2025 18:05 | Nov 2025 17:50
Dec 2025 19:10 | Jan 2026 19:45 | Feb 2026 18:30
Mar 2026 17:58 | Apr 2026 17:20 | May 2026 17:45
Jun 2026 18:02 | Jul 2026 17:35 | Aug 2026 17:59

Board convention: "the past year" means the latest 12 published months. "Most months" means more than half of them.
""",
[("5", "the target was met in five of the twelve months"),
 ("6", "the target was met in six of the twelve months"),
 ("7", "the target was met in seven of the twelve months"),
 ("8", "the target was met in eight of the twelve months"),
 ("9", "the target was met in nine of the twelve months"),
 (NONE, "the correct count is not listed")],
"6", 2, ordered=True,
twin=T([("Jun 2026 18:02", "Jun 2026 17:52")], "7")),

# ------------------------------------------------------------------ t23
# why: 0.5% quarter-on-quarter is 2.0% only as an annualised rate; the claim states growth "in the quarter".
C("t23", "What, if anything, is wrong with the headline?",
"""
Business desk - headline check, Veldria GDP release

Headline: "Veldria's economy grew 2 percent in the second quarter"

Veldria National Statistics, first estimate for Q2 2026:
- Real GDP, change on previous quarter: +0.5%
- Real GDP, change on previous quarter at an annualised rate: +2.0%
- Real GDP, change on same quarter a year earlier: +1.6%

Business desk style guide: growth "in the quarter" means the change on the previous quarter. Annualised rates must be labelled "at an annual rate". Year-on-year changes must say "compared with a year earlier".

Reporter's note: "The agency's own chart shows 2.0 in big letters, so 2 percent is what they're saying."
""",
err("time", "pp", "rel", "count", "causal", "none"),
"wrong time window", 3),

# ------------------------------------------------------------------ t24
# why: Varga 29y 1m 20d; Rell 29y 0m 30d -> Rell was younger. Twin Rell sworn 1 July 1960 -> 29y 1m 29d.
Y("t24", "Is the profile's \"youngest mayor\" claim accurate?",
"""
Harwick Chronicle - profile fact check

Profile sentence: "When she was sworn in, Ines Varga became the youngest mayor in Harwick's history."

Records checked:
- Ines Varga: born 14 November 1996; sworn in as mayor on 3 January 2026.
- City archive note: before 2026, the youngest person ever sworn in as mayor was Tomas Rell, born 2 May 1931 and sworn in on 1 June 1960. Every other previous mayor was at least 33 when sworn in.

Chronicle rule: compare ages at swearing-in exactly, in years, months and days.

Reporter's note: "Both were 29, and Varga was sworn in in January while Rell was sworn in in June, so she must be younger."
""",
[("age at swearing-in", "the exact time between a person's date of birth and the date they were sworn in")],
0, 3,
twin=T([("sworn in on 1 June 1960", "sworn in on 1 July 1960")], 1)),

# ------------------------------------------------------------------ t25
# why: definition changed in 2018, so 2012 and 2025 figures are not comparable. Twin: no change -> 8,300/4,100 = 2.02.
C("t25", "Which verdict does the charity's claim receive?",
"""
Shelterline Charity - campaign claim review

Campaign claim: "The number of homeless households in Brackmore has doubled since 2012."

Source: Brackmore Housing Department, households assessed as homeless (financial years ending March):
- 2012: 4,100
- 2016: 5,050
- 2020: 6,900
- 2025: 8,300
Department footnote: "In 2018 the definition was widened to include households placed in temporary accommodation arranged by charities. Figures before and after 2018 are not comparable, and no re-based series exists."

Review rule: "doubled" is accepted for a ratio between 1.9 and 2.1. Comparisons across a break in a statistical series cannot be confirmed from that series.

Campaign manager: "8,300 is more than double 4,100. The claim is simple arithmetic."
""",
VERDICT, "not enough information", 3,
twin=T([("In 2018 the definition was widened to include households placed in temporary accommodation arranged by charities. Figures before and after 2018 are not comparable, and no re-based series exists.",
         "The definition has not changed since the series began in 2010, and all figures are comparable.")], "supported")),

# ------------------------------------------------------------------ t26
# why: 2020 (2.3%) is the first year above 2% (2022's 2.0 is not above). Twin 2020 1.98 -> 2023.
C("t26", "In which year did research spending first exceed 2% of GDP?",
"""
Science Council of Morvane - claim check for the minister's conference speech

Draft line: "In 2023, for the first time ever, Morvane's research spending exceeded 2% of GDP."

Gross spending on research and development as a share of GDP (Morvane Statistics Office, final figures):
- 2010-2017: all years below 1.8%
- 2018: 1.8%
- 2019: 1.9%
- 2020: 2.3% (GDP fell sharply in 2020 while research spending held steady)
- 2021: 1.95%
- 2022: 2.0%
- 2023: 2.1%
- 2024: 2.2%
- 2025: 2.2%

Council rule: "exceeded" means strictly above. Shares are compared as published.

Minister's adviser: "2020 was a fluke of the recession - it doesn't count."
""",
[(str(y), f"research spending first exceeded 2% of GDP in {y}") for y in range(2018, 2026)] + [(NONE, "research spending never exceeded 2% of GDP in the period")],
"2020", 2, ordered=True,
twin=T([("- 2020: 2.3% (GDP fell sharply in 2020 while research spending held steady)", "- 2020: 1.98% (GDP fell sharply in 2020 while research spending held steady)")], "2023")),
]
