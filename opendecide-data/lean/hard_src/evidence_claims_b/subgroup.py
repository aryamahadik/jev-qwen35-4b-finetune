"""evidence_claims_b / claims about subgroups: Simpson's reversals, subsample margins of error,
populations studied vs claimed, plurality vs majority, denominators, composition effects."""
from _lib import C, Y, T, VERDICT, err, NONE

OCC = ["surgeons", "civil engineers", "airline pilots", "electricians", "police officers",
       "software developers", "firefighters", "plumbers", "judges", "architects",
       "train drivers", "professors", "chief executives", "farmers"]

REG = ["North Fell", "Eastmarch", "Kettering Vale", "Southholm", "West Carrow",
       "Midmere", "Brackwater", "Lowdon", "Harlan Coast", "Ashby Moor"]

DIST = ["Aldbury", "Birchmoor", "Carrow", "Dunhollow", "Elmstead", "Farleigh", "Garside",
        "Holloway", "Inchmere", "Jessop Vale", "Kirkby Low", "Linhope", "Marlow Cross",
        "Netherby", "Oakhanger", "Pellworth", "Quarrendon", "Rushford", "Stavely", "Tolland"]

ITEMS = [
# ------------------------------------------------------------------ g01
# why: St Brand's is better in both risk groups (2% vs 3%, 15% vs 20%) but worse pooled because it takes more high-risk cases.
C("g01", "What is the main flaw, if any, in the campaign group's statement?",
"""
Patients First Alliance - press statement under review by the regional health watchdog

Statement: "Patients are about twice as likely to die after major bowel surgery at St Brand's as at Kellow General. St Brand's has questions to answer."

Audit data, 2025 (National Surgical Outcomes Audit), deaths within 30 days:
St Brand's (regional referral centre):
- low-risk patients: 4 deaths of 200 (2%)
- high-risk patients: 120 deaths of 800 (15%)
- all patients: 124 of 1,000 (12.4%)
Kellow General:
- low-risk patients: 24 deaths of 800 (3%)
- high-risk patients: 40 deaths of 200 (20%)
- all patients: 64 of 1,000 (6.4%)
Risk groups are assigned before surgery using the audit's standard scoring tool.

Watchdog analyst's task: name the main flaw, if any, before the watchdog responds publicly.
""",
err("simpson", "count", "base", "causal", "subgroup", "pp", "none"),
"aggregation reversal ignored", 2),

# ------------------------------------------------------------------ g02
# why: under-30 subsample n = 480, 57% +/- 4.5 -> lower end 52.5 > 50. Twin n = 120, +/- 9 -> 48.
Y("g02", "Under the paper's polling rule, can the headline about under-30s stand?",
"""
Carrow Gazette - readers' editor, response to a complaint

Headline: "Most voters under 30 oppose the Riverside stadium plan"

Poll: Brightline Research for the Gazette, 2,400 adults in Carrow, fieldwork 8-12 August 2026, weighted. Overall: 44% support, 49% oppose, 7% don't know (margin of error plus or minus 2 points).
Under-30s (n = 480; margin of error plus or minus 4.5 points): 36% support, 57% oppose, 7% don't know.

Gazette polling rule: a claim that "most" or "a majority" of a group holds a view is allowed only if the lower end of the margin of error for that group is above 50%. For subgroups, the subgroup's own margin of error must be used, not the overall one.

Complainant: "Your own poll shows only 49% of people oppose the plan. You cannot say most young people oppose it."
""",
[("majority claim", "allowed only if the group's percentage minus its margin of error is above 50%"),
 ("subgroup margin of error", "the margin of error calculated for the subgroup's own sample size")],
1, 2,
twin=T([("(n = 480; margin of error plus or minus 4.5 points)", "(n = 120; margin of error plus or minus 9 points)")], 0)),

# ------------------------------------------------------------------ g03
# why: trial enrolled only men 50-70; it says nothing either way about women. Twin claim names the men studied.
C("g03", "What verdict does the website's claim receive?",
"""
Health claims register - Venn Pharmacy website, product page for Prostavel

Website claim: "Prostavel is proven in a randomised trial to reduce night-time urination in adults aged 50 to 70."

Evidence supplied: PRO-NIGHT trial. 1,140 men aged 50-70 with an enlarged prostate were randomly assigned to Prostavel or placebo for 16 weeks. Night-time toilet trips fell by 1.1 per night more with Prostavel than with placebo (95% CI 0.8 to 1.4). No women took part; the trial protocol excluded them because the product was developed for prostate symptoms. No other trials exist.

Register rule: a claim is rated on the population it names. Evidence from one population neither confirms nor contradicts a claim about a different population unless the source itself reports on that population.
""",
VERDICT, "not enough information", 2,
twin=T([("reduce night-time urination in adults aged 50 to 70", "reduce night-time urination in men aged 50 to 70 with an enlarged prostate")], "supported")),

# ------------------------------------------------------------------ g04
# why: car 51% is more than half -> "most" OK. Twin car 46% is the largest group but not a majority.
Y("g04", "Does the census table support the council leader's use of \"most\"?",
"""
Dunhill Borough Council - transport strategy consultation, statement check

Council leader's statement: "Most commuters in Dunhill drive to work, so we have to plan around the car."

Source: Dunhill Commuting Census 2025 (all residents in work who travel to a workplace, n = 61,200). Main mode of travel to work: car 51%, bus 20%, rail 18%, walking or cycling 11%.

Council style guide: "most" and "the majority" mean more than half of the group. "The largest group" or "more than any other mode" may be used when a share is the biggest but not above half.

Cycling campaign's objection: "Driving is just the biggest single mode. Most people don't drive to work at all if you add up the rest."
""",
[("most", "more than half of the group"),
 ("largest group", "the biggest share, whether or not it is above half")],
1, 1,
twin=T([("car 51%, bus 20%, rail 18%, walking or cycling 11%", "car 46%, bus 20%, rail 18%, walking or cycling 16%")], 0)),

# ------------------------------------------------------------------ g05
# why: only electricians exceed +33.3% (3.0 -> 4.1 = +36.7%); pilots are exactly a third; judges have the biggest point rise. Twin 3.9 -> none.
C("g05", "For which occupation does the report's claim hold?",
"""
Equal Work Commission - report proof, chapter 2

Claim to check: "In one occupation, the share of workers who are women rose by more than a third between 2020 and 2025." The author has not said which occupation she meant.

Share of workers who are women (%), Labour Force Survey, 2020 -> 2025:
- surgeons 28.0 -> 34.0
- civil engineers 12.0 -> 15.0
- airline pilots 6.0 -> 8.0
- electricians 3.0 -> 4.1
- police officers 30.0 -> 36.0
- software developers 18.0 -> 21.0
- firefighters 7.0 -> 9.0
- plumbers 2.0 -> 2.6
- judges 34.0 -> 44.0
- architects 29.0 -> 35.0
- train drivers 5.0 -> 6.5
- professors 26.0 -> 32.0
- chief executives 8.0 -> 10.5
- farmers 17.0 -> 19.0

Commission style: "rose by a third" describes relative change in the share, (new - old) / old.
""",
[(o, f"the claim holds for {o}") for o in OCC] + [(NONE, "the claim holds for none of the occupations listed")],
"electricians", 3,
twin=T([("- electricians 3.0 -> 4.1", "- electricians 3.0 -> 3.9")], NONE)),

# ------------------------------------------------------------------ g06
# why: 1,000 under-25 job finders / 2,000 under-25 enrolled = 50%. Twin 5,000 enrolled -> 20%.
Y("g06", "Is the minister's \"half\" figure right?",
"""
Department for Work, Aldmark - JobStart programme, ministerial statement check

Minister's statement: "Half of the young people on JobStart found jobs through the programme last year."

JobStart annual report 2025:
- The programme enrolled 2,000 people aged under 25 and 3,000 people aged 25 or over.
- 2,000 participants found jobs through the programme: 1,000 aged under 25 and 1,000 aged 25 or over.
- Average time to a job offer: 11 weeks.

Statement-check rule: "young people" in the minister's statements means people aged under 25. "Half" is accepted for 45-55%.

Adviser's note: "Half of the people who found jobs were under 25, so the line is fine."
""",
[("share of young people who found jobs", "young participants who found jobs / all young participants enrolled")],
1, 2,
twin=T([("The programme enrolled 2,000 people aged under 25", "The programme enrolled 5,000 people aged under 25")], 0)),

# ------------------------------------------------------------------ g07
# why: province-level correlation stated as a fact about individual gym members.
C("g07", "Which flaw, if any, is in the blog's conclusion?",
"""
FitLife Blog - post flagged by a reader for review by the site's editor

Post excerpt: "The data are clear. Across Veldria's 12 provinces, those with more gyms per 10,000 residents have lower adult obesity rates (correlation -0.71). Brenmark, with the most gyms, has the lowest obesity rate; Tolland, with the fewest, has the highest. So people who belong to a gym are less likely to be obese."

Source: Veldria Health Atlas 2025, province-level table: gyms per 10,000 residents and adult obesity rate for each province. The atlas contains no data on whether individual people are gym members.

Editor's note: "Please name the main problem with the last sentence, if there is one. The post doesn't claim gyms cause anything, so don't flag it for that."
""",
err("eco", "causal", "subgroup", "count", "base", "none"),
"group-level data applied to individuals", 2),

# ------------------------------------------------------------------ g08
# why: interaction p = 0.61 -> apply overall result to women under the rule, despite women's own CI crossing 1. Twin p = 0.004 -> use women's own CI -> neither.
C("g08", "Applying the journal's subgroup rule, what is the verdict on the claim?",
"""
Cardiology news service - claims check

Claim in a medical newsletter: "Cardovex also reduces hospital admissions for heart failure in women."

Trial: CARDO-HF, 4,800 adults with heart failure (1,500 women, 3,300 men) randomly assigned to Cardovex or placebo, median follow-up 2 years. Sex was a pre-specified subgroup.
- Overall: hazard ratio 0.78 (95% CI 0.68 to 0.90)
- Women: HR 0.82 (95% CI 0.63 to 1.07)
- Men: HR 0.76 (95% CI 0.64 to 0.90)
- Test for difference between women and men (interaction): p = 0.61

Journal's subgroup rule: for pre-specified subgroups, the overall trial result applies to each subgroup unless the test for interaction has p < 0.05. Do not judge a subgroup by whether its own confidence interval crosses 1. If the interaction test has p < 0.05, judge the subgroup by its own result.
""",
VERDICT, "supported", 3,
twin=T([("Test for difference between women and men (interaction): p = 0.61", "Test for difference between women and men (interaction): p = 0.004")], "not enough information")),

# ------------------------------------------------------------------ g09
# why: every grade's average rose; the firm-wide average fell because the mix shifted to junior staff.
Y("g09", "Do the payroll figures support the union's claim?",
"""
Norcross Group - union bulletin, fact check by the HR analytics team

Union bulletin claim: "Every grade at Norcross saw its average salary fall between 2024 and 2025."

Payroll data (full-time staff at 1 April):
| Grade | 2024 staff | 2024 average | 2025 staff | 2025 average |
| A (junior) | 400 | 30,000 | 700 | 31,000 |
| B | 400 | 50,000 | 400 | 51,000 |
| C (senior) | 200 | 80,000 | 150 | 82,000 |
| All staff | 1,000 | 48,000 | 1,250 | 43,520 |

The rise in grade A staff reflects the opening of a new customer service centre.

Union rep's note: "The all-staff average is down by more than 4,000. That's every grade, as far as members are concerned."
""",
[("grade average", "the mean salary of the staff in one grade"),
 ("all-staff average", "the mean salary across every grade, which also depends on how many staff are in each grade")],
0, 2,
twin=T([("Every grade at Norcross saw its average salary fall", "The average salary across all Norcross staff fell")], 1)),

# ------------------------------------------------------------------ g10
# why: only Southholm has women's rate up and men's rate down. Twin makes Southholm men flat -> none.
C("g10", "In which region did the unemployment rate for women rise while the rate for men fell?",
"""
Regional Labour Market Digest - claim check

Draft digest sentence: "In one region, women's unemployment rose over the year even as men's fell." The reporter needs the region named.

Unemployment rates (%), annual averages, 2024 -> 2025 (region | women 2024 | women 2025 | men 2024 | men 2025):
North Fell | 5.1 | 5.4 | 5.6 | 5.9
Eastmarch | 4.2 | 4.0 | 4.8 | 4.5
Kettering Vale | 6.0 | 6.3 | 6.2 | 6.2
Southholm | 3.9 | 4.4 | 4.1 | 3.8
West Carrow | 5.5 | 5.2 | 5.0 | 5.3
Midmere | 4.7 | 4.7 | 5.1 | 4.8
Brackwater | 6.8 | 7.1 | 7.4 | 7.6
Lowdon | 3.5 | 3.3 | 3.9 | 3.6
Harlan Coast | 5.9 | 6.4 | 6.3 | 6.3
Ashby Moor | 4.4 | 4.3 | 4.6 | 4.2

Digest convention: a rate that is unchanged at one decimal place has neither risen nor fallen.
""",
[(r, f"the pattern occurred in {r}") for r in REG] + [(NONE, "the pattern occurred in none of the listed regions")],
"Southholm", 2,
twin=T([("Southholm | 3.9 | 4.4 | 4.1 | 3.8", "Southholm | 3.9 | 4.4 | 4.1 | 4.1")], NONE)),

# ------------------------------------------------------------------ g11
# why: the sample is FinPay app users, not all adults; the rule requires the claim's population to match.
Y("g11", "Can the release's claim about adults be published under the standards team's rule?",
"""
FinPay - press release, standards team review

Release headline: "72% of Aldmark adults now prefer to pay by contactless."

Survey details: online questionnaire sent to FinPay app users, June 2026; 3,000 responses. 72% of respondents chose "contactless card or phone" as their preferred way to pay in shops. FinPay app users are aged 18 or over and make up about 20% of Aldmark adults.

Standards team rule: a survey figure may be stated for a population only if the survey sampled that population (or a representative sample of it). Figures from customer surveys must be stated as figures for customers.

Marketing lead: "3,000 is a big sample. It's statistically robust, so it's fine for all adults."
""",
[("survey population", "the group the sample was drawn from, which limits whom the result may be stated for")],
0, 1,
twin=T([("72% of Aldmark adults now prefer to pay by contactless.", "72% of FinPay app users surveyed now prefer to pay by contactless.")], 1)),

# ------------------------------------------------------------------ g12
# why: (0.68 x 400k + 0.78 x 300k) / 700k = 72.3% > 70%. Twin 75+ uptake 72% -> 69.7%.
C("g12", "How should the claim about women over 65 be rated?",
"""
Public Health Agency of Tarrow - flu season review, claims check

Claim in the review's summary: "Among women aged 65 and over, flu vaccine uptake exceeded 70% this winter."

Uptake data, women, winter 2025-26 (vaccination records linked to the population register):
- Women aged 65-74: 68% of 400,000
- Women aged 75 and over: 78% of 300,000
- Men aged 65-74: 63% of 380,000
- Men aged 75 and over: 74% of 230,000

Checker's rule: figures for a combined group must be weighted by the number of people in each part of the group, not averaged across the parts.

Comment from a reviewer: "Women 65-74 were below 70%, so the claim can't be right for women over 65."
""",
VERDICT, "supported", 2,
twin=T([("Women aged 75 and over: 78% of 300,000", "Women aged 75 and over: 72% of 300,000")], "refuted")),

# ------------------------------------------------------------------ g13
# why: 40 vs 20 events meets the 10-event minimum and 2.0% vs 1.0% is twice. Twin 4 vs 2 events fails the minimum.
Y("g13", "May the reporter publish the \"twice as likely\" sentence under the desk's small-numbers rule?",
"""
Data desk - copy check, school sports injuries story

Reporter's sentence: "Pupils who play rugby at Halden secondary schools were twice as likely to suffer a concussion this year as pupils who play football."

Source: Halden Schools Sports Injury Register, 2025-26 school year:
- Rugby: 40 concussions among 2,000 registered players (2.0%)
- Football: 20 concussions among 2,000 registered players (1.0%)
- Hockey: 9 concussions among 1,100 registered players

Desk small-numbers rule: a ratio ("twice as likely", "three times as common") may be published only if each group being compared has at least 10 events. Otherwise give the raw numbers without a ratio.

Sports editor's comment: "We're comparing two sports in one year. Is that even allowed?"
""",
[("small-numbers rule", "a ratio may be published only if each compared group has at least 10 events"),
 ("twice as likely", "the rate in one group is two times the rate in the other")],
1, 1,
twin=T([("- Rugby: 40 concussions among 2,000 registered players (2.0%)\n- Football: 20 concussions among 2,000 registered players (1.0%)",
         "- Rugby: 4 concussions among 200 registered players (2.0%)\n- Football: 2 concussions among 200 registered players (1.0%)")], 0)),

# ------------------------------------------------------------------ g14
# why: a lab study of 60 university students is stated for "office workers" in general.
C("g14", "Which flaw, if any, does the advert's claim contain?",
"""
Advertising clearance - UprightCo standing desks, print advert

Advert: "Science says office workers burn 20% more calories at their desk when they stand. Switch to UprightCo."

Study cited: Pernell et al. (2025). 60 university sports science students aged 19-24 each spent one hour typing while seated and one hour typing while standing, in random order, in a laboratory. Energy use measured by gas analysis was 20% higher while standing (95% CI 14% to 26%). The authors note: "Our participants were young, lean and physically active; results may differ in other groups."

Clearance note: randomised crossover studies may support cause-and-effect wording. The advert's figure matches the study's relative increase, and the study measured one hour of desk work.
""",
err("subgroup", "causal", "pp", "count", "time", "none"),
"subgroup finding generalised", 2),

# ------------------------------------------------------------------ g15
# why: by the rule (points), 25-34 rose 10 points vs 18-24's 8 points.
Y("g15", "Under the commission's rule, is the claim about 18-24-year-olds correct?",
"""
Electoral Commission of Varn - post-election report, proof check

Draft sentence: "The largest increase in turnout was among 18-24-year-olds."

Turnout by age group (validated turnout study), 2021 -> 2026:
- 18-24: 30% -> 38%
- 25-34: 45% -> 55%
- 35-54: 61% -> 66%
- 55-64: 70% -> 73%
- 65 and over: 76% -> 78%

Commission rule: changes in turnout are compared in percentage points (the difference between the two turnout rates). Relative changes may be mentioned only if labelled as such ("rose by a quarter").

Author's note: "18-24 turnout went up by more than a quarter - nobody else comes close."
""",
[("increase in turnout", "under the commission's rule, the difference between two turnout rates in percentage points")],
0, 2,
twin=T([("Commission rule: changes in turnout are compared in percentage points (the difference between the two turnout rates). Relative changes may be mentioned only if labelled as such (\"rose by a quarter\").",
         "Commission rule: changes in turnout are compared as relative changes, (new - old) / old. Differences in percentage points may be mentioned only if labelled as such.")], 1,
       instructions=None)),

# ------------------------------------------------------------------ g16
# why: women = 600 + 6,400 + 1,000 + 8,250 + 2,250 = 18,500 of 50,000 = 37%; simple average of shares is 39%. Twin health 3,000 -> 14,500/45,000 = 32%.
C("g16", "What share of all new apprentices were women, to the nearest whole percent?",
"""
Apprenticeships Agency of Holt - claim check

Claim in a minister's speech: "Women now make up a third of all new apprentices."

New apprenticeship starts, 2025, by sector:
| Sector | Starts | Share who are women |
| Construction | 12,000 | 5% |
| Health and care | 8,000 | 80% |
| Engineering | 10,000 | 10% |
| Business and admin | 15,000 | 55% |
| Hospitality | 5,000 | 45% |

Agency note: every apprentice is counted in one sector only.

Speechwriter's working: "Average of the five sector shares is 39%, so 'a third' is if anything an understatement."
""",
[("32%", "women were 32% of all new apprentices"),
 ("33%", "women were 33% of all new apprentices"),
 ("37%", "women were 37% of all new apprentices"),
 ("39%", "women were 39% of all new apprentices"),
 (NONE, "the correct share is not listed")],
"37%", 2, ordered=True,
twin=T([("| Health and care | 8,000 | 80% |", "| Health and care | 3,000 | 80% |")], "32%")),

# ------------------------------------------------------------------ g17
# why: 83% is among completers, and the claim is scoped to completers. Twin states it for everyone enrolled (83% x 40% = 33%).
Y("g17", "Is the programme's claim consistent with its own evaluation?",
"""
Quitwell Stop-Smoking Programme - annual report, independent auditor's check

Report claim: "Of the people who completed the Quitwell course, 83% had stopped smoking six months later."

Evaluation data, 2025 intake:
- Enrolled: 2,500 smokers
- Completed all six sessions: 1,000 (40% of those enrolled)
- Of those who completed: 830 confirmed smoke-free at six months by breath test
- Of those who dropped out: smoking status at six months was not recorded

Auditor's instruction: check whether the figure matches the group the sentence names. Completion rates are reported separately and are not part of this check.

Board member's comment: "Only 40% even finished. Surely an 83% success rate is misleading?"
""",
[("completers", "people who attended all six sessions"),
 ("enrolled", "everyone who started the programme, including those who dropped out")],
1, 2,
twin=T([("Of the people who completed the Quitwell course, 83% had stopped smoking six months later.", "Of the people who enrolled on the Quitwell course, 83% had stopped smoking six months later.")], 0)),

# ------------------------------------------------------------------ g18
# why: in grade 3, women's median is higher (46,200 vs 45,800), so "every grade" is false. Twin fixes grade 3.
C("g18", "What verdict fits the MP's claim about Firm X's grades?",
"""
Parliamentary researcher's note - gender pay gap debate

MP's claim: "At Tallis & Mere, women earn less than men in every job grade."

Tallis & Mere statutory pay gap report 2026 (median basic annual pay by grade):
| Grade | Women | Men |
| 1 | 21,400 | 21,900 |
| 2 | 29,800 | 31,200 |
| 3 | 46,200 | 45,800 |
| 4 | 63,000 | 66,500 |
| 5 | 98,000 | 112,000 |
Overall median: women 31,000; men 44,500.

The report says figures are for all full-time employees and cover every grade in the firm.

Researcher's rule: rate the claim on the medians reported, as the MP cited this report.
""",
VERDICT, "refuted", 1,
twin=T([("| 3 | 46,200 | 45,800 |", "| 3 | 45,200 | 45,800 |")], "supported")),

# ------------------------------------------------------------------ g19
# why: under-25 fall 14,000 of a 26,000 total fall = 54% -> most. Twin 22,000 -> 8,000 of 20,000 = 40%.
Y("g19", "Does the labour market table support the claim that most of the fall came from under-25s?",
"""
Aldmark Employment Ministry - press line check

Draft line: "Most of the fall in unemployment over the past year came from young people under 25."

Unemployed people (Labour Force Survey, June 2025 -> June 2026):
- under 25: 30,000 -> 16,000
- 25-49: 60,000 -> 50,000
- 50 and over: 30,000 -> 28,000

Ministry style: "most of the fall" means more than half of the total reduction in the number of unemployed people across all age groups. The fall for each group is measured in numbers of people, not percentages.

Analyst's comment: "Under-25s had the biggest percentage drop, but I'm not sure that settles it - the line is about the fall itself."
""",
[("share of the fall", "the reduction in one group's number / the total reduction across all groups")],
1, 2,
twin=T([("- under 25: 30,000 -> 16,000", "- under 25: 30,000 -> 22,000")], 0)),

# ------------------------------------------------------------------ g20
# why: largest point fall is Farleigh (3.1); Stavely has the largest relative fall. Twin Farleigh 28.0 -> Dunhollow (2.8) largest.
C("g20", "Under the authority's rule, which district had the biggest fall in persistent absence?",
"""
Holtshire Education Authority - press release check

Draft press release: "Stavely saw the biggest fall in persistent absence of any district this year."

Share of pupils persistently absent (%), 2023/24 -> 2024/25:
Aldbury 18.2 -> 16.9 | Birchmoor 22.5 -> 20.1 | Carrow 15.0 -> 13.9 | Dunhollow 25.8 -> 23.0
Elmstead 12.0 -> 9.8 | Farleigh 30.4 -> 27.3 | Garside 19.7 -> 18.8 | Holloway 21.1 -> 19.0
Inchmere 17.4 -> 17.9 | Jessop Vale 26.3 -> 23.6 | Kirkby Low 14.8 -> 13.0 | Linhope 23.9 -> 21.3
Marlow Cross 16.6 -> 15.9 | Netherby 20.2 -> 18.1 | Oakhanger 11.5 -> 9.9 | Pellworth 27.7 -> 25.0
Quarrendon 13.3 -> 12.6 | Rushford 24.0 -> 21.4 | Stavely 9.4 -> 7.6 | Tolland 18.9 -> 17.2

Authority rule: rises and falls in rates are compared in percentage points. Relative changes are not used to rank districts.
""",
[(d, f"{d} had the biggest fall under the rule") for d in DIST] + [(NONE, "no single district had the biggest fall")],
"Farleigh", 2,
twin=T([("Farleigh 30.4 -> 27.3", "Farleigh 30.4 -> 28.0")], "Dunhollow")),

# ------------------------------------------------------------------ g21
# why: 720 profitable of 4,000 founded = 18%; the 60% is among survivors only.
Y("g21", "Does the survey support the claim about businesses founded in 2015?",
"""
Aldmark Small Business Federation - conference speech, claim check

Speech line: "Most businesses founded in Aldmark in 2015 are now profitable - proof that start-ups thrive here."

Source: Federation Business Survival Study 2025.
- Businesses registered in Aldmark in 2015: 4,000
- Still trading in 2025: 1,200
- Of those still trading, 60% reported a profit in their latest accounts
- Businesses that closed were not surveyed

Speechwriter's note: "The study says 60% are profitable. That's most."

Checker's rule: a claim about a group must use that whole group as the denominator.
""",
[("denominator", "the whole group a claim is about; here, every business founded in 2015")],
0, 2,
twin=T([("Most businesses founded in Aldmark in 2015 are now profitable", "Most of the businesses founded in Aldmark in 2015 that are still trading are now profitable")], 1)),

# ------------------------------------------------------------------ g22
# why: 36% / 12% = 3.0 -> "three times as likely" holds. Twin highest fifth 15% -> 2.4.
C("g22", "Given the survey, how should the claim be rated?",
"""
Children's Dental Health Survey 2025 - claim review for a charity advert

Advert claim: "Five-year-olds in the poorest fifth of families are three times as likely to have tooth decay as those in the richest fifth."

Survey results (dental examinations of 8,900 five-year-olds, weighted), share with visible decay, by family income fifth:
- Lowest fifth: 36%
- Second: 29%
- Middle: 22%
- Fourth: 17%
- Highest fifth: 12%

Review rule: "N times as likely" is accepted if the ratio of the two percentages is within 10% of N. Association wording does not need randomised evidence.

Reviewer's comment: "The gap is 24 points. 'Three times' makes it sound much bigger than it is."
""",
VERDICT, "supported", 1,
twin=T([("- Highest fifth: 12%", "- Highest fifth: 15%")], "refuted")),

# ------------------------------------------------------------------ g23
# why: growth rates: under-18 +2%, 18-44 -1%, 45-64 +6%, 65-79 +18%, 80+ +40% -> fastest-growing is right. Twin says "largest".
Y("g23", "Is the council's statement accurate according to the population estimates?",
"""
Holt District Council - adult social care strategy, statement check

Statement: "Over-80s are the fastest-growing age group in Holt."

Population estimates (mid-year):
| Age group | 2015 | 2025 |
| Under 18 | 41,000 | 41,820 |
| 18-44 | 68,000 | 67,320 |
| 45-64 | 52,000 | 55,120 |
| 65-79 | 25,000 | 29,500 |
| 80 and over | 7,500 | 10,500 |

Council style: "fastest-growing" compares relative growth, (2025 - 2015) / 2015; "largest" compares the number of people in each group.

Councillor's objection: "65-79s added 4,500 people, more than the over-80s' 3,000. The statement is wrong."
""",
[("fastest-growing", "the group with the highest relative growth"),
 ("largest", "the group with the most people")],
1, 2,
twin=T([("Over-80s are the fastest-growing age group in Holt.", "Over-80s are the largest age group in Holt.")], 0)),

# ------------------------------------------------------------------ g24
# why: 95% of occupants wear belts, so most deaths being belted says little; belted death rate is far lower.
C("g24", "What is the main flaw in the commenter's argument?",
"""
Tollan Road Safety Forum - comment moderation queue

Comment: "The police report says 62% of car occupants killed on Tollan roads last year were wearing a seatbelt. So belted occupants were more likely to be killed than unbelted ones. Think about that before you buckle up."

Facts held by the forum moderators:
- Roadside surveys show about 95% of car occupants in Tollan wear a seatbelt.
- 210 car occupants were killed last year: 130 belted, 80 unbelted.
- The police report makes no claim about why individual occupants died.

Moderator guidance: identify the main flaw in the reasoning, if any, and reply with a short correction rather than deleting the comment.
""",
err("base", "causal", "simpson", "subgroup", "time", "pp", "none"),
"base-rate confusion", 2),

# ------------------------------------------------------------------ g25
# why: men 18% vs women 12% with equal numbers -> 60% of smokers are men -> "most smokers are men" true. Twin women 20% -> 47%.
Y("g25", "Does the survey support the statement that most smokers in Varn are men?",
"""
Varn Tobacco Control Unit - leaflet claim check

Leaflet statement: "Most smokers in Varn are men."

Varn Adult Health Survey 2025 (weighted to the adult population):
- Men: 18% smoke
- Women: 12% smoke
- Adults in Varn: 2.10 million men and 2.10 million women

Unit style: "most smokers are men" is a statement about the smokers - more than half of all smokers are men. It is not a statement that most men smoke.

Reviewer's note: "Only 18% of men smoke. How can 'most' be right?"
""",
[("most smokers are men", "more than half of all smokers are men"),
 ("most men smoke", "more than half of all men smoke")],
1, 2,
twin=T([("- Women: 12% smoke", "- Women: 20% smoke")], 0)),

# ------------------------------------------------------------------ g26
# why: first-time buyers' ratio is 6.8, not "about nine"; 9.1 is the all-homes ratio. Twin states the all-homes claim.
C("g26", "Rate the housing campaign's claim.",
"""
Kelby Housing Watch - campaign claim review

Campaign claim: "In Kelby, the typical first-time buyer's home costs about nine times their annual income."

Kelby Housing Affordability Report 2026:
- All home sales: average price / average full-time earnings = 9.1
- First-time buyer purchases: average price paid / average first-time buyer household income = 6.8
- Home movers (not first-time): average price paid / average mover household income = 7.4

Review rule: "about" allows plus or minus 0.5. Figures must match the group the claim names.

Campaign manager: "Everyone knows the nine-times figure. It's the one in all the headlines."
""",
VERDICT, "refuted", 2,
twin=T([("the typical first-time buyer's home costs about nine times their annual income", "the average home costs about nine times average full-time earnings")], "supported")),
]
