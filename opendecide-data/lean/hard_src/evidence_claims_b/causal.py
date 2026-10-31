"""evidence_claims_b / correlation vs causation: study design, causal wording, confidence intervals,
comparison groups, mechanisms."""
from _lib import C, Y, T, VERDICT, err, NONE

ITEMS = [
# ------------------------------------------------------------------ c01
# why: observational cohort cannot establish "cuts"; nothing contradicts it either. Twin uses association wording.
C("c01", "What verdict does the proposed headline get, given the study?",
"""
Science desk - headline review, Monday edition

Proposed headline: "Three to four cups of coffee a day cuts dementia risk by a fifth"

Study: Lindqvist et al., prospective cohort study of 21,400 adults aged 50 and over in the Varn Health Register, followed for 12 years. Coffee intake was self-reported once, at the start. Adults who drank 3-4 cups a day had a 20% lower rate of dementia than those who drank none (hazard ratio 0.80, 95% CI 0.71 to 0.90), after adjusting for age, sex, education and smoking.

Authors' conclusion: "Higher coffee intake was associated with lower dementia risk; residual confounding cannot be excluded."

Desk guide: cause-and-effect verbs (cuts, prevents, raises, causes, boosts, protects) need evidence from a randomised comparison. Association wording (linked to, associated with, lower among) may rest on observational studies. A hazard ratio of 0.80 may be described as "a fifth lower".
""",
VERDICT, "not enough information", 2,
twin=T([("cups of coffee a day cuts dementia risk by a fifth", "cups of coffee a day linked to a fifth lower dementia risk")], "supported")),

# ------------------------------------------------------------------ c02
# why: randomised, but maths CI includes zero -> "maths and reading" not found. Twin drops maths.
Y("c02", "Is the draft sentence consistent with the trial results under the Trust's reporting rule?",
"""
Ardmore Schools Research Trust - press release check

Draft sentence: "Classroom ventilation units raised pupils' maths and reading scores, a major trial has found."

Trial summary: 60 primary schools were randomly assigned. In September 2024, 30 schools had ventilation units fitted in every classroom; the other 30 continued as normal and received units after the trial. Pupils sat standardised tests at the end of the school year.
- Reading: +0.09 standard deviations for pupils in schools with units (95% CI 0.02 to 0.16)
- Maths: +0.02 standard deviations (95% CI -0.05 to 0.09)
Both reading and maths were pre-registered primary outcomes. Classroom CO2 levels fell by about a third in schools with units.

Trust's reporting rule: a trial counts as having found an effect on an outcome only if the 95% confidence interval for that outcome excludes zero. Randomised designs may be described with cause-and-effect verbs.
""",
[("finding an effect", "under the Trust's rule, the 95% confidence interval for that outcome excludes zero"),
 ("randomised trial", "a study in which chance decides who receives the intervention, so cause-and-effect wording is allowed")],
0, 2,
twin=T([("raised pupils' maths and reading scores", "raised pupils' reading scores")], 1)),

# ------------------------------------------------------------------ c03
# why: visits go to dying patients (reverse causation / confounding) -> causal claim from association; rates are right.
C("c03", "Which flaw, if any, does the board member's conclusion contain?",
"""
St Aldric's Hospital - Patient Experience Committee, papers for item 5

Email circulated by a board member:
"Our own data: of 2,000 inpatients visited by the chaplaincy team last year, 12% died in hospital, compared with 4% of the 18,000 inpatients who were not visited. Chaplain visits triple a patient's risk of dying. We should review whether the service is doing harm."

Note from the chaplaincy lead: visits are made on request from patients, families or ward staff. Requests are most common for patients receiving end-of-life care, and the palliative care team routinely offers a visit.

Note from the data team: "The counts and percentages in the email are correct and cover all inpatients discharged or deceased during the year."
""",
err("causal", "pp", "rel", "count", "subgroup", "none"),
"causal claim from association", 1),

# ------------------------------------------------------------------ c04
# why: observational + association wording -> allowed. Twin uses a causal verb -> not allowed.
Y("c04", "Can the headline run under the desk guide?",
"""
Health desk - headline check, weekend supplement

Study: Bellmark Nurses' Work and Health Cohort, 64,000 female nurses followed for 18 years. Nurses who had worked rotating night shifts for 10 or more years had a 30% higher rate of type 2 diabetes than nurses who never worked nights (hazard ratio 1.30, 95% CI 1.18 to 1.43), after adjustment for body mass index, diet, physical activity and family history.

Authors' limitations paragraph: "This is an observational study. We cannot establish that night-shift work causes diabetes."

Headline under review: "Long-term night shifts linked to higher diabetes risk in nurses"

Desk guide: cause-and-effect verbs (cause, give, raise, cut, prevent, lead to) need evidence from a randomised comparison. Association wording (linked to, associated with, more common among) may rest on observational studies if the confidence interval excludes no effect. Headlines must name the population studied when the study was limited to one group.

Sub-editor's query: "Authors say they can't show causation, so surely we can't run any headline about risk?"
""",
[("association wording", "phrases such as linked to, associated with or more common among, which claim only that two things occur together"),
 ("cause-and-effect wording", "verbs such as cause, give, raise, cut, prevent or lead to, which need randomised evidence")],
1, 2,
twin=T([("Long-term night shifts linked to higher diabetes risk in nurses", "Long-term night shifts give nurses diabetes")], 0)),

# ------------------------------------------------------------------ c05
# why: effect = -40% - (-38.1%) = about -2 points, so "about 40%" is contradicted. Twin: comparison flat -> -39%.
C("c05", "Rate the annual report's claim against the evaluation.",
"""
Eastfold Road Safety Board - evaluation summary for the annual report

Claim drafted for the annual report: "Average-speed cameras on Route 9 cut injury crashes by about 40%."

Evaluation design (set out in the Board's evaluation manual before installation): cameras went live on Route 9 on 1 January 2025. The comparison group is 14 similar A-roads in the county without cameras. The estimated effect of the cameras is the percent change in injury crashes on the camera road minus the percent change on the comparison roads over the same periods. "About" allows plus or minus 3 points.

Injury crashes, calendar 2024 vs calendar 2025:
- Route 9: 50 -> 30
- Comparison roads combined: 210 -> 130

Note from the Board's communications officer: "Crashes on Route 9 fell from 50 to 30. That's 40%. I don't see what else there is to check."
""",
VERDICT, "refuted", 3,
twin=T([("Comparison roads combined: 210 -> 130", "Comparison roads combined: 210 -> 208")], "supported")),

# ------------------------------------------------------------------ c06
# why: trial governs; CI 0.85-1.13 excludes 1.30 -> refuted. Twin CI 0.80-1.45 includes 1.30 -> neither.
C("c06", "Applying the desk rule, what is the verdict on the post?",
"""
Fact-check file 2291 - social media post about a gout medicine

Post: "Solvarin raises the risk of death by 30% - the evidence is in."

Evidence gathered by the researcher:
(1) Registry study: 40,000 gout patients in routine care. Solvarin users had higher mortality than users of other gout medicines (hazard ratio 1.31). Patients prescribed Solvarin were older on average and more often had kidney disease.
(2) SOLACE trial: 6,100 gout patients randomly assigned to Solvarin or to an alternative gout medicine and followed for 4 years. All-cause death: HR 0.98 (95% CI 0.85 to 1.13).
No other studies of Solvarin and mortality exist.

Desk rule: when a randomised trial and observational studies disagree, the trial governs. A trial whose 95% confidence interval excludes the effect size claimed contradicts the claim. A trial whose interval includes the claimed effect neither confirms nor contradicts it.
""",
VERDICT, "refuted", 3,
twin=T([("HR 0.98 (95% CI 0.85 to 1.13)", "HR 1.08 (95% CI 0.80 to 1.45)")], "not enough information")),

# ------------------------------------------------------------------ c07
# why: the trial shows the app reduced anxiety, but sleep was never measured -> the "because" is not established.
Y("c07", "Does the trial establish the reason the article gives for the result?",
"""
Wellbeing column - editor's check before publication

Column sentence: "A randomised trial shows the Stillwater meditation app reduced anxiety among university students because it improved their sleep."

Trial report (Okafor and Lindahl, 2026): 1,020 students at three universities were randomly assigned to eight weeks of the Stillwater app or to a waiting list. Primary outcome: anxiety score on a standard 21-point scale. At eight weeks, the app group scored 2.1 points lower than the waiting-list group (95% CI 1.4 to 2.8). Secondary outcomes: self-rated stress (lower in the app group) and number of app sessions completed. The report does not include any measure of sleep. The discussion section says "possible mechanisms include reduced rumination and better sleep, which future trials should measure."

Editor's standard: a claim about why an effect happened must be backed by data in the source, not only by the authors' speculation.
""",
[("mechanism claim", "a statement about why or how an effect happened, which needs its own supporting data"),
 ("randomised trial", "a study in which chance decides who receives the intervention")],
0, 2),

# ------------------------------------------------------------------ c08
# why: the claim is only about the population difference, which exists (3.2 points). Authors' causal doubt does not refute it.
C("c08", "How should the fact box rate the claim as worded?",
"""
Little Acorns Magazine - fact box, "Myths and facts about feeding"

Claim to rate: "Children who were breastfed score higher on IQ tests, on average, than children who were not."

Source: Aldmoor Child Cohort, 9,800 children tested at age 8.
- Breastfed for 6 months or more: mean IQ 104.1
- Never breastfed: mean IQ 100.9
- Difference 3.2 points (95% CI 2.4 to 4.0)
A second, within-family analysis compared 1,150 pairs of siblings where one child was breastfed and the other was not: difference 0.3 points (95% CI -0.9 to 1.5).

Authors' conclusion: "The population difference largely reflects family background rather than an effect of breastfeeding itself."

Magazine rule: rate the claim as worded. The children not breastfed in the cohort include those given formula from birth.
""",
VERDICT, "supported", 3),

# ------------------------------------------------------------------ c09
# why: lottery = random allocation, CI excludes zero -> causal claim allowed. Twin: caseworker selection.
Y("c09", "Does the evidence meet the Lab's standard for the causal claim in the report?",
"""
Harrowgate Policy Lab - evidence brief for the city housing committee

Claim in the city's annual report: "Offering families relocation vouchers improved their children's reading scores."

Evidence: in 2019, 2,400 eligible families applied for 800 relocation vouchers, which paid moving costs and a rent top-up for homes in low-poverty neighbourhoods. The vouchers were allocated by public lottery among eligible applicants. Five years later, children in families that won a voucher scored 0.12 standard deviations higher on the city reading test than children in families that did not (95% CI 0.05 to 0.19). 71% of winning families had moved, compared with 9% of other applicants.

Lab standard for cause-and-effect claims: the groups compared must have been formed by chance (randomised trials and lotteries both count), and the 95% confidence interval must exclude no effect. Comparisons of groups that selected themselves, or were selected by officials, support association wording only.
""",
[("cause-and-effect claim", "a claim that one thing improved, cut, raised or caused another"),
 ("formed by chance", "group membership decided by random assignment or lottery, not by choice or judgement")],
1, 2,
twin=T([("allocated by public lottery among eligible applicants", "allocated by caseworkers to the eligible applicants they judged most ready to move")], 0)),

# ------------------------------------------------------------------ c10
# why: "more than halved in a year" is literally true, but the "steep downward trend" is measured from a one-off spike.
C("c10", "What is the problem, if any, with the newsletter's claim?",
"""
Greyfield Academy - parents' newsletter, July (draft for governors' approval)

"Behaviour at Greyfield is on a steep downward trend: fixed-term exclusions have more than halved in a single year."

Governors' data pack - fixed-term exclusions by school year:
- 2020/21: 22
- 2021/22: 19
- 2022/23: 24
- 2023/24: 48 (includes 21 exclusions issued after a single incident in March 2024)
- 2024/25: 20
Pupil numbers were between 1,080 and 1,120 in every year.

Chair of governors' note: "Before we approve, can someone name any problem with the claim? I don't want a list, just the main issue, or confirmation that there isn't one."
""",
err("baseline", "pp", "count", "causal", "time", "none"),
"cherry-picked starting point", 2),

# ------------------------------------------------------------------ c11
# why: placebo flat at 8.0, drug 4.0 -> halved against placebo. Twin: placebo 6.0 -> one third fewer.
Y("c11", "Under the desk rule, does the trial support the tweet?",
"""
Pharma watch desk - social post check

Company tweet: "Zolmex halves migraine days - proven in a placebo-controlled trial."

Trial (ZOL-2, published in full): 540 adults with chronic migraine were randomly assigned to Zolmex or an identical placebo for 12 weeks. At baseline both groups averaged 8.0 migraine days per month. During weeks 9-12, the Zolmex group averaged 4.0 migraine days per month and the placebo group 8.0 migraine days per month. The difference was statistically significant. Side effects: nausea in 9% vs 4%.

Desk rule: a drug's effect is judged against the placebo group over the same period, not against the patients' own baseline. "Halves" is accepted if the drug group's figure is 45% to 55% of the comparison figure.
""",
[("placebo-controlled comparison", "the drug group's result compared with the placebo group's result over the same period"),
 ("halves", "under the desk rule, the drug group's figure is 45% to 55% of the placebo group's figure")],
1, 2,
twin=T([("the placebo group 8.0 migraine days", "the placebo group 6.0 migraine days")], 0)),

# ------------------------------------------------------------------ c12
# why: dog owners 27% vs 21% lonely -> the association runs the other way. Twin swaps.
C("c12", "Given the survey, is the leaflet's claim supported, refuted, or neither?",
"""
Pawprint Trust - leaflet proof, "Why a dog is good for you"

Claim: "Dog owners are less likely to feel lonely than people without pets."

Source cited: National Wellbeing Survey 2025, 8,200 adults, weighted to the population.
Share reporting feeling lonely "often or always":
- dog owners 27% (n = 1,900)
- people with no pets 21% (n = 5,100)
- owners of other pets only 24% (n = 1,200)
The survey report says the dog-owner vs no-pet difference is statistically significant.

Comms officer's note: "Everyone knows dogs are company. The survey must have asked the wrong people - leave the claim in."

Proof-checker's rule: claims are rated against the cited source only.
""",
VERDICT, "refuted", 1,
twin=T([("dog owners 27% (n = 1,900)\n- people with no pets 21% (n = 5,100)",
         "dog owners 21% (n = 1,900)\n- people with no pets 27% (n = 5,100)")], "supported")),

# ------------------------------------------------------------------ c13
# why: the study found the reverse direction (depression -> use) and no use -> depression link.
Y("c13", "Does the study support the op-ed's reading of it?",
"""
Opinion page - standards editor's check

Op-ed sentence: "A major new study shows that heavy social media use leads to depression in teenagers."

Study (Harlan Youth Panel, 2026): 3,600 teenagers were surveyed at age 14 and again at 16 about daily social media hours and depressive symptoms.
- Teenagers with more depressive symptoms at 14 went on to increase their social media hours by 16 (adjusted coefficient 0.18, 95% CI 0.11 to 0.25).
- Social media hours at 14 did not predict depressive symptoms at 16 (adjusted coefficient 0.01, 95% CI -0.03 to 0.05).
- At both ages, teenagers who used social media more had more depressive symptoms.

Authors' summary: "The cross-sectional link is consistent with depressed teenagers turning to social media, rather than the reverse."

Standards editor's note: op-eds may argue opinions freely, but descriptions of what a study shows must be accurate.
""",
[("leads to", "cause-and-effect wording: the first thing produces the second"),
 ("cross-sectional link", "an association measured at one point in time, which does not show which came first")],
0, 2),

# ------------------------------------------------------------------ c14
# why: randomised, so causal wording is fine; 60% -> 66% is +6 points = +10%, so "6 percent" is a pp mix-up.
C("c14", "Which flaw, if any, is in the council's summary sentence?",
"""
Farrowby Council - Public Health Committee, briefing paper

Summary sentence: "Sending text reminders boosted flu vaccine uptake among over-65s by 6 percent."

Evidence: in autumn 2025, 24,000 residents aged 65 and over registered with Farrowby GP practices were randomly assigned by the council's analysts to receive two text reminders or no reminders. Uptake by 31 January 2026:
- No reminders: 60.0%
- Text reminders: 66.0%
The difference was statistically significant. Every person in the trial was aged 65 or over, and the period matches the 2025-26 flu season.

Committee style guide: "percent" describes relative change; "percentage points" describes the difference between two percentages. Randomised comparisons may be described with cause-and-effect verbs.
""",
err("causal", "pp", "rel", "subgroup", "time", "none"),
"percent/percentage-point mix-up", 2),

# ------------------------------------------------------------------ c15
# why: trial followed 24 months only; "for good" goes beyond it. Twin says "for two years".
Y("c15", "Is the advert's claim backed by the trial as described?",
"""
Advertising clearance desk - LeanPath diet programme, radio script v2

Script line: "LeanPath is proven in a randomised trial to keep weight off for good."

Trial summary supplied by the advertiser: 900 adults with obesity were randomly assigned to the LeanPath programme or to standard dietary advice. Participants were weighed at 6, 12, 18 and 24 months. At 24 months the LeanPath group weighed on average 6.1 kg less than the standard-advice group (95% CI 4.8 to 7.4 kg), and the difference was similar at 18 months. The trial ended at 24 months; there is no later follow-up. 81% of participants completed the trial.

Clearance rule: a claim about how long an effect lasts may not go beyond the longest follow-up in the evidence supplied.
""",
[("follow-up", "the period over which trial participants were measured after the start"),
 ("duration claim", "a statement about how long an effect lasts, which the clearance rule limits to the longest follow-up")],
0, 1,
twin=T([("to keep weight off for good", "to keep weight off for two years")], 1)),

# ------------------------------------------------------------------ c16
# why: OR 1.04 (0.91-1.19): link not shown, and no-link not shown either -> neither. Twin CI excludes 1.
C("c16", "Under the bulletin's rule, which verdict applies to the claim?",
"""
Environmental Health Bulletin, Ostmere District - claims review

Claim in a residents' group newsletter: "Living within 200 metres of a motorway is linked to higher asthma rates in children."

Source cited: Ostmere Children's Air Study (2025), 11,000 children aged 5-12. Children living within 200 metres of a motorway compared with children living more than 1 km away, adjusted for household smoking, damp housing and income: odds ratio for diagnosed asthma 1.04 (95% CI 0.91 to 1.19).

Bulletin rule: an association counts as shown only if the 95% confidence interval excludes no effect (an odds ratio of 1.0). A claim that there is no link counts as shown only if the interval also excludes increases of 10% or more (an upper bound below 1.10). Association wording does not need randomised evidence.
""",
VERDICT, "not enough information", 2,
twin=T([("odds ratio for diagnosed asthma 1.04 (95% CI 0.91 to 1.19)", "odds ratio for diagnosed asthma 1.29 (95% CI 1.12 to 1.49)")], "supported")),

# ------------------------------------------------------------------ c17
# why: meta-analysis of RCTs, RR 0.85 (0.78-0.93) -> causal claim allowed. Twin RR 1.00 (0.93-1.07) -> no.
Y("c17", "Can the charity's sentence stay in the booklet under the review panel's rule?",
"""
Bone Health Alliance - patient booklet, evidence review panel

Sentence under review: "Taking vitamin D supplements reduces fractures in adults over 65."

Evidence: a pre-registered meta-analysis (2025) of 22 randomised trials comparing daily vitamin D supplements with placebo in adults aged 65 and over, 48,000 participants in total, median follow-up 3 years. Pooled relative risk of any fracture: RR 0.85 (95% CI 0.78 to 0.93). No trials in younger adults were included.

A separate observational study in the same age group found that people with higher blood vitamin D levels had fewer fractures (HR 0.70).

Panel rule: sentences with cause-and-effect verbs (reduces, prevents, cuts) need a randomised trial or a meta-analysis of randomised trials whose 95% confidence interval excludes no effect (RR 1.0). Observational findings may only be used with association wording.
""",
[("relative risk", "the risk in the supplement group divided by the risk in the placebo group; below 1.0 means fewer fractures with supplements"),
 ("cause-and-effect verb", "a verb such as reduces, prevents or cuts, which the panel allows only with randomised evidence excluding no effect")],
1, 2,
twin=T([("RR 0.85 (95% CI 0.78 to 0.93)", "RR 1.00 (95% CI 0.93 to 1.07)")], 0)),

# ------------------------------------------------------------------ c18
# why: effect = (7.4-9.1) - (8.1-9.0) = -1.7 + 0.9 = -0.8. Twin control 8.6 -> -1.7 + 0.4 = -1.3.
C("c18", "According to the evaluation guide, how many sick days per employee per year did the programme save?",
"""
Kestrel Logistics - HR evaluation of the "Fit for Work" wellness programme

Design: in January 2025, 1,600 warehouse staff were randomly assigned by depot shift to the programme or to a control group that received the programme a year later.

Average sick days per employee:
| | 2024 (before) | 2025 (programme year) |
| Programme group | 9.1 | 7.4 |
| Control group | 9.0 | 8.1 |

Kestrel evaluation guide, section 3: "The effect of a programme is the change in the programme group minus the change in the control group over the same period. Report the saving as a positive number of days, to one decimal place."

Draft line from the programme manager: "Fit for Work saved 1.7 sick days per employee."
""",
[("0.7", "0.7 sick days saved per employee per year"),
 ("0.8", "0.8 sick days saved per employee per year"),
 ("0.9", "0.9 sick days saved per employee per year"),
 ("1.3", "1.3 sick days saved per employee per year"),
 ("1.7", "1.7 sick days saved per employee per year"),
 (NONE, "the correct saving is not listed")],
"0.8", 2, ordered=True,
twin=T([("| Control group | 9.0 | 8.1 |", "| Control group | 9.0 | 8.6 |")], "1.3")),

# ------------------------------------------------------------------ c19
# why: a large study with upper bound 1.08 < 1.20 meets the no-effect rule. Twin: wide CI 0.6-2.1.
Y("c19", "Does the study meet the desk's standard for the \"does not raise the risk\" claim?",
"""
Technology desk - explainer draft, "Phones and health: what the evidence says"

Draft sentence: "The largest study so far found that mobile phone use does not raise the risk of brain tumours in adults."

Study: Nordvik National Cohort, 420,000 adults followed for an average of 13 years (about 5.4 million person-years), phone use taken from network subscription records. Brain tumour rate in long-term phone users compared with non-users: hazard ratio 1.00 (95% CI 0.92 to 1.08). It is the largest study of the question published to date.

Desk standard for "no effect" claims: a sentence saying something does not raise a risk is acceptable only if (a) the study has more than 1 million person-years of follow-up and (b) the upper end of the 95% confidence interval is below 1.20. Otherwise write "found no clear evidence either way".

Reviewer's comment: "Absence of evidence isn't evidence of absence. We can never say 'does not raise'."
""",
[("no-effect claim", "a statement that something does not raise or lower a risk, which the desk allows only with a large study and a narrow confidence interval"),
 ("person-years", "the number of people multiplied by the years each was followed")],
1, 3,
twin=T([("hazard ratio 1.00 (95% CI 0.92 to 1.08)", "hazard ratio 1.12 (95% CI 0.60 to 2.10)")], 0)),

# ------------------------------------------------------------------ c20
# why: cluster-randomised, CI excludes zero -> causal claim supported. Twin CI includes zero -> neither.
C("c20", "What is the right verdict on the minister's statement?",
"""
Department for Education, Veldria - statement check before Question Time

Minister's statement: "Offering free breakfast clubs raised pupil attendance in the schools that took part in our national trial."

Trial report: 106 primary schools in areas of high deprivation were randomly assigned in 2024: 53 were offered funding for a free before-school breakfast club; 53 were not (and were offered it after the trial). Attendance was measured for all pupils in each school, whether or not they used the club. Over the 2024/25 school year, attendance was 1.2 percentage points higher in the schools offered clubs (95% CI 0.6 to 1.8). On a typical day, about 38% of pupils in those schools used the club.

Note from a backbencher's researcher: "Most pupils never went to breakfast club, so the minister can't claim the clubs raised attendance."

Checking standard: randomised designs may be described with cause-and-effect verbs if the 95% confidence interval excludes no effect.
""",
VERDICT, "supported", 1,
twin=T([("(95% CI 0.6 to 1.8)", "(95% CI -0.3 to 2.7)")], "not enough information")),

# ------------------------------------------------------------------ c21
# why: 3% -> 2% is a one-third relative cut; "prevents heart attacks in a third of people" treats it as absolute.
C("c21", "What is the main flaw, if any, in the pharmacy chain's poster?",
"""
Pharmacy Standards Board - complaint 26/118, in-store poster

Poster: "Ask about Corvastat. In a major trial it prevented heart attacks in a third of the people who took it."

Trial cited: 7,500 adults aged 50-75 with raised cholesterol and no previous heart disease were randomly assigned to Corvastat or placebo and followed for five years. Heart attacks: placebo 3.0%; Corvastat 2.0%. The difference was statistically significant and was the trial's primary outcome. Participants were typical of the pharmacy chain's customers for this medicine.

Complainant: "My GP says the benefit is much smaller than the poster suggests."
Chain's response: "One third fewer heart attacks is exactly what the trial found."
""",
err("rel", "pp", "causal", "subgroup", "time", "none"),
"relative change presented as absolute", 2),

# ------------------------------------------------------------------ c22
# why: comparison of students 1-2 marks either side of the cut-off meets the stated causal standard. Twin compares distant scores.
Y("c22", "Does the evidence meet the foundation's causal standard for the claim?",
"""
Brightwater Foundation - impact claims review

Claim in the foundation's annual review: "The Keystone scholarship raised university enrolment among the students who received it."

Evidence: Keystone scholarships go automatically to students scoring 70 or more on the regional entrance test. The evaluation compared students who scored 70 or 71 (eligible) with students who scored 68 or 69 (not eligible), across five cohorts. Enrolment at university within a year: 64% vs 51% (difference 13 points, 95% CI 8 to 18). Family income, school type and gender were similar on both sides of the cut-off.

Foundation's causal standard: cause-and-effect claims need either (a) random assignment or (b) a comparison of people within 2 marks either side of an eligibility cut-off that nobody can control, where the groups are alike on background characteristics. In either case the 95% CI must exclude no effect.
""",
[("eligibility cut-off comparison", "comparing people just above and just below a fixed threshold, who are otherwise alike"),
 ("cause-and-effect claim", "a claim that something raised, cut or caused an outcome")],
1, 3,
twin=T([("with students who scored 68 or 69 (not eligible)", "with students who scored 55 to 65 (not eligible)")], 0)),

# ------------------------------------------------------------------ c23
# why: association claim of a rise with every extra hour; 10+ hours dips -> refuted. Twin makes it monotonic.
C("c23", "Does the survey table support the claim, refute it, or neither?",
"""
Sleep Well Schools campaign - poster claim check

Claim: "Among Year 11 pupils, exam grades rise with every extra hour of sleep."

Source: Merrow County Pupil Survey 2025, 6,300 Year 11 pupils who reported their usual school-night sleep; average exam points score (0-90 scale) by sleep band:
- 6 hours or less: 61
- 7 hours: 66
- 8 hours: 70
- 9 hours: 71
- 10 hours or more: 67
All differences between adjacent bands are statistically significant.

Campaign lead: "The poster doesn't say sleep causes better grades, only that they go together, so a survey is enough."
Checker's rule: association claims may rest on survey data; the pattern stated must hold across every band in the source.
""",
VERDICT, "refuted", 2,
twin=T([("10 hours or more: 67", "10 hours or more: 74")], "supported")),

# ------------------------------------------------------------------ c24
# why: randomised trial, causal wording OK, numbers fine -> no flaw. Twin makes it a survey -> causal from association.
C("c24", "Which of these flaws, if any, does the charity's claim have?",
"""
ClearSight Charity - trustee report, impact section (draft)

Claim: "Giving free glasses to children who need them improved their maths test scores in the Tollan province study."

Evidence: the study took place in 180 rural schools in Tollan province, randomly assigned to receive free eye tests and free glasses for every child who needed them, or to continue as normal for one year. Among children who needed glasses, maths scores rose by 0.11 standard deviations more in the glasses schools than in the comparison schools (95% CI 0.04 to 0.18). The study reported results only for children who needed glasses and only for Tollan province.

Auditor's instruction: name the flaw if there is one; the charity's claims are expected to follow the usual rules on percentages, cause-and-effect wording, populations and time periods.
""",
err("causal", "pp", "rel", "subgroup", "time", "none"),
NONE, 3,
twin=T([("randomly assigned to receive free eye tests and free glasses for every child who needed them, or to continue as normal for one year. Among children who needed glasses, maths scores rose by 0.11 standard deviations more in the glasses schools than in the comparison schools",
         "surveyed once. Among children who needed glasses, those who already owned glasses scored 0.11 standard deviations higher in maths than those who did not")],
       "causal claim from association")),

# ------------------------------------------------------------------ c25
# why: non-randomised, n = 4,200, CI excludes 1 -> "is linked to". Twin n = 850 -> "may be linked to".
C("c25", "Which wording does the style guide allow for this headline?",
"""
Morrowgate Health News - style guide, section 7 ("Wording ladder")
Choose the strongest wording the evidence allows:
1. "cuts": randomised evidence whose 95% confidence interval excludes no effect.
2. "is linked to": non-randomised evidence from a study of 1,000 or more people whose 95% CI excludes no effect.
3. "may be linked to": non-randomised evidence from a study of fewer than 1,000 people whose 95% CI excludes no effect.
4. "no clear link": any study whose 95% CI includes no effect.

Story: a study of 4,200 adults in Morrowgate who kept food diaries for a year found that people who ate fermented vegetables at least three times a week had 18% fewer respiratory infections than those who never ate them (rate ratio 0.82, 95% CI 0.74 to 0.91). Participants chose their own diets.

Draft headline: "Fermented vegetables ___ fewer winter infections"
""",
[("cuts", "rung 1: randomised evidence excluding no effect"),
 ("is linked to", "rung 2: non-randomised evidence, 1,000 or more people, excluding no effect"),
 ("may be linked to", "rung 3: non-randomised evidence, fewer than 1,000 people, excluding no effect"),
 ("no clear link", "rung 4: the confidence interval includes no effect")],
"is linked to", 2, ordered=True,
twin=T([("a study of 4,200 adults in Morrowgate", "a study of 850 adults in Morrowgate")], "may be linked to")),

# ------------------------------------------------------------------ c26
# why: the reporter's weaker association wording is true of an RCT result; accurate even though it differs from the authors' verb.
Y("c26", "Is the reporter's sentence supported by the study?",
"""
Regional news desk - copy check

Reporter's sentence: "In a trial at Linmouth General, a new checklist before surgery was linked to fewer wound infections."

Study (Linmouth General quality improvement trial, 2026): 2,400 planned operations were randomly assigned, by day of the week in a random sequence set in advance, to use the new pre-surgery checklist or the usual procedure. Wound infections within 30 days: checklist 3.1%; usual procedure 5.0% (difference 1.9 points, 95% CI 0.4 to 3.4). Authors' conclusion: "The checklist caused a meaningful reduction in wound infections."

Copy editor's query: "The authors say 'caused'. We say 'linked to'. Doesn't that misreport the study?"

Desk guide: a sentence is supported if what it states is established by the source. Association wording is always allowed when an effect has been established; cause-and-effect wording needs randomised evidence.
""",
[("association wording", "phrases such as linked to or associated with, which state only that two things go together"),
 ("supported sentence", "a sentence whose content is established by the source, even if it says less than the source")],
1, 2),
]
