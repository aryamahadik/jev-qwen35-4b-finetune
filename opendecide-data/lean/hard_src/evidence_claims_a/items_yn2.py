"""Yes/no claim-verification items, part 2 (finance and history mostly). Hand-written by Claude."""
from common import Y

ITEMS = [
# Y26 lower combined ratio = improvement
Y("Is the claim supported by the analyst note?",
"""
Analyst note, Tennant & Rowe Equity Research
Halberd Insurance: FY2025 results first look

Gross written premiums £4.12bn (+7%). Combined ratio 97.2% (FY2024: 99.8%). Investment income £311m (FY2024: £268m). Catastrophe losses were lighter than budget, though the motor book continues to see claims inflation of around 9%. The reserve release of £64m was below last year's £92m.

Glossary for retail readers: the combined ratio is claims plus expenses divided by premiums earned; a ratio below 100% means an underwriting profit, and a lower ratio is a better result.

Claim (client briefing): "Halberd Insurance's combined ratio improved in 2025 compared with 2024."
""", 1, 2),

# Y27 existential claim
Y("Does the newsletter support the claim?",
"""
Family history society newsletter, members' research corner

"Several members have asked what the Garrow sisters of Brenhaven did during the 1914-18 war. From the papers deposited by their niece: Edith Garrow (born 1889) nursed with a voluntary aid detachment at the Brenhaven auxiliary hospital from 1915 to 1917. Maud Garrow (born 1893) joined the Post Office telegraph service at Brenhaven in March 1915 as a telegraphist, sending and receiving telegrams on the office's instruments, and stayed until the service released its wartime staff in 1919. The youngest, Clara (born 1899), was still at school in 1916 and afterwards trained as a typist; no wartime employment is recorded for her."

Claim: "At least one of the Garrow sisters worked as a telegraph operator during the 1914-18 war."
""", 1, 1),

# Y28 capacity factor up but fleet shrank
Y("Is NOT ENOUGH INFO the right label for this claim?",
"""
Community benefit fund, annual meeting briefing: Arvale Wind Farm

Operator's statement: "2025 was a strong year for Arvale. Our fleet capacity factor rose to 33%, up from 29% in 2024, reflecting both a windier year and improved availability after the gearbox replacement programme. During 2025 we retired eight of the forty original turbines as part of the planned repowering; the replacement turbines will be installed in 2027."

Clarification from the operator in response to a question from the floor: "Capacity factor for each year is calculated on the turbines in service during that year. We do not publish the dates of individual retirements or annual output figures for the site."

Note: all turbines at Arvale are the same model and rating.

Claim (fund newsletter): "The Arvale wind farm generated more electricity in 2025 than in 2024."
""", 1, 3),

# Y29 "no patient" vs 7
Y("Do the results refute the claim?",
"""
Regulatory assessment report, extract: Brisa-3 study (tavorimab in moderate plaque psoriasis)

Table 12. Treatment discontinuations, 16-week double-blind period
Reason | Tavorimab (n = 331) | Placebo (n = 329)
Adverse event | 7 (2.1%) | 6 (1.8%)
Lack of efficacy | 3 (0.9%) | 21 (6.4%)
Withdrawal of consent | 5 (1.5%) | 8 (2.4%)
Lost to follow-up | 2 (0.6%) | 3 (0.9%)

Assessor comment: the most common adverse events leading to discontinuation with tavorimab were injection-site reactions (3 patients) and headache (2 patients). No deaths occurred.

Claim (patient-group summary): "No patient taking tavorimab in the Brisa-3 study stopped treatment because of side effects."
""", 1, 1),

# Y30 share of revenue
Y("Does the annual report extract support the claim?",
"""
Cadence Retail plc, Annual Report 2025, strategic report (extract)

Group revenue for the year was £812m (2024: £776m). Revenue from our 214 stores was £391m (2024: £402m) and online revenue was £421m (2024: £374m). Click-and-collect orders, which are placed online and collected in store, are included in online revenue. Like-for-like store sales fell 1.8%. Online conversion improved to 3.4%. We opened six stores and closed eleven during the year, and the online operation moved to the new Daventry fulfilment centre in May.

Claim (trade magazine): "More than half of Cadence Retail's 2025 revenue came from online sales."
""", 1, 2,
twin=([("stores was £391m (2024: £402m) and online revenue was £421m", "stores was £421m (2024: £402m) and online revenue was £391m")], 0)),

# Y31 baptism vs birth
Y("Does the evidence establish the claim?",
"""
Dictionary of Coastal Biography, entry (draft for revision)

VARR, Elias (1741-1803), master mariner and hydrographer.
Varr was baptised at St Brannoc's church, Portledge, on 9 June 1741, the second son of Thomas Varr, a cooper, and his wife Hester. The family had moved to Portledge from Castlecombe, some forty miles inland, in the autumn of 1740; the Castlecombe parish register ends its record of the family with the burial of an infant daughter in 1739. Varr went to sea at twelve, commanded the survey sloop Petrel from 1778, and his charts of the Sallow Banks remained in use until the 1850s.

Editor's query to contributor: "Can we say 'born in Portledge' in the headline? Please only use what the sources above establish."

Claim: "Elias Varr was born in Portledge."
""", 0, 3),

# Y32 hedged claim matches hedged evidence
Y("Should the claim be labelled SUPPORTS?",
"""
Water Authority, Groundwater Status Assessment 2025, summary table (extract)

Aquifer | Quantitative status | Saline intrusion risk | Trend
Corran Basin (coastal) | Poor | Moderate | Water table falling 0.3 m/yr at coastal boreholes
Hollins Chalk | Good | Low | Stable
Merrow Sands | Good | Not assessed (inland) | Rising

Notes: "Moderate" means intrusion is plausible within 20 years if current abstraction continues; "High" means intrusion is already observed at monitoring points. No chloride increase has yet been recorded at any Corran monitoring point.

Claim (local newspaper): "The Water Authority says the Corran Basin aquifer may be at risk of saltwater intrusion."
""", 1, 2),

# Y33 negated question; BBB- still investment grade
Y("Does the rating action fail to support the claim?",
"""
Credit rating action, Stellan Ratings, 18 June 2025

Stellan Ratings has downgraded the long-term issuer rating of Farrow Energy plc to BBB- from BBB. The outlook is negative. The downgrade reflects higher leverage following the debt-funded purchase of the Ketter offshore field and weaker gas price assumptions. All of Farrow's senior unsecured bonds are rated in line with the issuer rating.

Rating scale note (Stellan): ratings of BBB- and above are investment grade; BB+ and below are sub-investment grade ("high yield").

Claim (financial blog): "Farrow Energy's bonds were cut to below investment grade by Stellan in 2025."
""", 1, 2, role="neg",
twin=([("to BBB- from BBB.", "to BB+ from BBB-.")], 0)),

# Y34 threshold row selection
Y("Does the safety summary support the claim?",
"""
Vaccine safety summary: Nerra (recombinant RSV vaccine), pooled phase III data
Solicited systemic reactions within 7 days of vaccination, adults 60 and over (n = 12,408 vaccine recipients):
Fatigue: 18.2%
Headache: 12.9%
Muscle pain: 10.4%
Fever 38.0 °C or higher: 4.2%
Fever 39.0 °C or higher: 0.6%
Fever 40.0 °C or higher: under 0.1%
Most reactions were mild and resolved within 2 days. Rates in placebo recipients (n = 12,395) were 11.0%, 8.8%, 6.1%, 1.3%, 0.2% and under 0.1% respectively.

Claim (pharmacy leaflet): "Fewer than 1 in 100 people aged 60 or over who received the Nerra vaccine in the phase III studies had a fever of 39.0 °C or higher."
""", 1, 2),

# Y35 one party never signed
Y("Is the claim contradicted by the sidebar?",
"""
History textbook, chapter 7 sidebar: "The Treaty of Vell (1622)"

After two years of intermittent war over the Tarn river tolls, envoys of the Duchy of Ambrel and of the Free City of Sarn met at the monastery of Vell in the spring of 1622. The negotiated text fixed the toll at one penny per cask and returned the captured mills at Oster. Ambrel's envoy, Count Rudo of Teck, signed on 3 May. The Sarn delegation referred the text to the city council, which debated ratification for a week and rejected it by eleven votes to nine; the Sarn delegate was recalled and never signed. Fighting resumed that summer.

Claim: "The Treaty of Vell was signed by both the Duchy of Ambrel and the Free City of Sarn."
""", 1, 1),

# Y36 causal claim, no study of the cause
Y("Is the claim supported by the evidence in the letter?",
"""
Letters page, Stannard Gazette

Sir, last month's letter blamed the new solar farm at Stannard for the loss of local bee colonies because of "electromagnetic fields from the inverters". The facts from the county beekeepers' association survey are these. Colonies registered within 3 km of the solar farm fell from 118 in spring 2023 to 92 in spring 2025, a fall of 22%. Across the whole county, registered colonies fell by 19% over the same period. The association's report attributes most county-wide losses to varroa mite and the wet summer of 2024. No study of electromagnetic fields at the site has been carried out.
R. Allard, Secretary, Stannard & District Beekeepers

Claim: "Honeybee colonies near the Stannard solar farm declined because of electromagnetic fields from the site."
""", 0, 2),

# Y37 sum across programmes; EBT distractor
Y("Do the disclosures support the claim?",
"""
Tamsin Holdings plc, extract from the 2025 annual summary of share buybacks

Programme 1 (announced February 2025): 2.1 million ordinary shares repurchased between 3 March and 27 June 2025 at an average price of 412p; all shares cancelled.
Programme 2 (announced August 2025): 3.4 million ordinary shares repurchased between 1 September and 19 December 2025 at an average price of 438p; 1.0 million held in treasury, the remainder cancelled.
Employee benefit trust: separately purchased 0.4 million shares in the market in 2025 to satisfy share awards; these purchases are not part of either buyback programme.

Claim (investor forum): "Tamsin Holdings bought back more than 5 million of its own shares under its 2025 buyback programmes."
""", 1, 3,
twin=([("3.4 million ordinary shares", "2.7 million ordinary shares")], 0)),

# Y38 date of first procedure
Y("Is the claim refuted by the history page?",
"""
Fenwood Hospital, "Our history" webpage (urology section)

2017: Urology department moves to the new Fenwood surgical block.
2019: Hospital board approves purchase of a surgical robot following a charitable appeal that raised £1.1m.
2020: Delivery of the robot is postponed because of the pandemic; the operating theatre intended for it is converted to a temporary intensive-care unit.
February 2021: The first robot-assisted prostatectomy at Fenwood is performed by Mr Aled Price and his team.
2023: The 500th robotic procedure is carried out; the service expands to kidney surgery.

Claim (fundraising leaflet): "Fenwood Hospital began offering robotic prostate surgery before 2020."
""", 1, 1),

# Y39 "only" vs second island
Y("Does the evidence refute the claim?",
"""
Species account, Atlas of the Amphibians of the Maret Archipelago (2nd edition)
Hollin's frog (Pelorana hollini)

Hollin's frog was described in 1962 from specimens collected on Maret, the largest island of the archipelago, and for fifty years was regarded as a Maret endemic. In 2019 a survey team using DNA barcoding confirmed breeding populations on Tessel, the neighbouring island 14 km to the east; the Tessel frogs are genetically indistinguishable from those on Maret. Searches on the four smaller islands have found no individuals. The species is listed as Vulnerable because of forest loss on Maret.

Claim: "Hollin's frog is found only on the island of Maret."
""", 1, 1),

# Y40 missing log volume
Y("Is the evidence insufficient to decide the claim?",
"""
Heritage centre enquiry log, Brackwater Lighthouse collection
Enquiry: "Does the keeper's log record the wreck of the schooner Minnow in 1903?"

Response prepared by volunteer archivist:
- The collection holds keepers' logs for 1896-1902 complete, and for 1903 only January to June; the second volume for 1903 is missing and was already absent when the collection was catalogued in 1961.
- According to the harbour master's report, the schooner Minnow was wrecked on the Carn Ledges on the night of 14 October 1903, with the loss of two lives.
- A newspaper report of the inquest mentions that "the lighthouse keeper gave evidence of the state of the light that night", but does not quote the log.

Claim: "The Brackwater lighthouse keeper's log for 1903 records the wreck of the schooner Minnow."
""", 1, 2),

# Y41 units bn vs m; gearing distractor
Y("Is the claim supported by the statement?",
"""
Pellow Water, interim management statement (extract)
Balance sheet highlights at 31 December 2025:
Net debt £2.41bn (31 December 2024: £2,390m).
Regulatory capital value £3.62bn (31 December 2024: £3,480m).
Gearing (net debt / RCV) 66.6% (31 December 2024: 68.7%).
The reduction in gearing reflects growth in the regulatory capital value from inflation indexation and capital investment of £318m in the year. Net debt includes index-linked bonds, whose principal rises with inflation, and excludes lease liabilities of £41m.

Claim (campaign group press release): "Pellow Water's net debt rose during 2025."
""", 1, 2,
twin=([("Net debt £2.41bn", "Net debt £2.31bn"), ("Gearing (net debt / RCV) 66.6%", "Gearing (net debt / RCV) 63.8%")], 0)),

# Y42 negated question; universal "everyone"
Y("Does the leaflet fail to support the claim?",
"""
Ormond Street Medical Practice, seasonal flu leaflet (autumn)
Who can have a free flu vaccination at the practice?
- Patients registered with Ormond Street Medical Practice who are aged 65 or over (on or before 31 March next year)
- Registered patients aged 18 to 64 in a clinical risk group
- Registered pregnant women
- Registered carers
Visitors and patients registered with other practices: we can vaccinate you at our Saturday clinics for a charge of £14, or you can get a free vaccination from your own practice if eligible.
Clinics: Saturdays in October, 9am to 1pm, no appointment needed.

Claim (neighbourhood social media): "The Ormond Street practice gives the flu jab free to everyone aged 65 or over."
""", 1, 2, role="neg"),

# Y43 combined vs first-year significance
Y("Is the claim backed by the press summary?",
"""
Collaboration press summary, Belmont Reactor Neutrino Experiment

The Belmont collaboration today reported the observation of reactor antineutrino disappearance consistent with neutrino oscillation. Using 1,730 days of data from the near and far detectors, the combined analysis excludes the no-oscillation hypothesis with a significance of 5.4 standard deviations (5.4 sigma). The first-year data alone had reached 3.1 sigma. The measured mixing parameter agrees with previous experiments within uncertainties. The result has been submitted for peer review.

Claim: "The Belmont experiment's combined analysis found an oscillation signal with a significance above 5 sigma."
""", 1, 1),

# Y44 "some women" before 1910
Y("Does the panel text support the claim?",
"""
Carlow Borough exhibition panel: "Votes for Women in Carlow"

Until 1907, the municipal franchise in Carlow Borough was restricted to male ratepayers. The Borough Franchise Order of 1907 extended the vote in council elections to women who were ratepayers in their own right, mainly widows and single women occupying property. The first council election in which women voted was held in November 1908: the poll book records 412 women among 3,106 voters. Married women living with their husbands remained excluded until 1919.

Claim: "Some women were able to vote in Carlow Borough council elections before 1910."
""", 1, 2),

# Y45 wrong cause
Y("Does the evidence support the claim?",
"""
Results announcement, Maple & Rowe (textiles), year to 30 September

Revenue £346m (-3%). Operating profit £29.8m (-14%).
Chief Executive's comment: "The fall in profit was driven mainly by weaker demand in our wholesale division, where two large retail customers reduced orders, and by the costs of consolidating our warehousing into a single site. Raw material costs were broadly stable over the year, as forward purchasing insulated us from the rise in cotton prices."
Market context (from the announcement's appendix): benchmark cotton prices rose 22% during the year.

Claim (trade press): "Maple & Rowe's profit fell because of higher cotton prices."
""", 0, 2),

# Y46 relative reduction "about a quarter"
Y("Does the evaluation support the claim?",
"""
Calder Bowel Screening Programme, 15-year evaluation: key findings

Population: 188,400 people aged 55 to 64 at the start, allocated by birth date to be invited (n = 94,160) or not invited (n = 94,240) to one-off flexible sigmoidoscopy.
Uptake among those invited: 71%.
Bowel cancer deaths over 15 years: 0.84% of the invited group vs 1.12% of the not-invited group. Relative reduction 25%; absolute reduction 0.28 percentage points; number needed to invite to prevent one death: 357.
Bowel cancer incidence: 3.9% vs 4.6%.

Claim (health charity): "In the Calder programme, the risk of dying from bowel cancer was reduced by about a quarter among people invited to screening."
""", 1, 2),

# Y47 "never used" vs eleven months of traffic
Y("Do the sources refute the claim?",
"""
Canal Society journal, "Lost waterways" series, part 6: the Stenmark Canal

The Stenmark Canal was cut between 1827 and 1831 to link the Holt collieries with the river at Stenmark Quay, a distance of seven miles with eleven locks. It opened in May 1831 and for eleven months carried paying coal and lime traffic, averaging some 40 boat-loads a week. In April 1832 a breach at Hollow Lock drained the summit pound; the proprietors, already in debt, could not raise the money to repair it, and the canal never reopened. A tramway on the towpath replaced it in 1836.

Claim: "The Stenmark Canal was never used for commercial traffic."
""", 1, 1),

# Y48 school assessment vs national tests
Y("Is the claim supported by the pilot report?",
"""
Headteachers' network newsletter, spring edition
Pilot report: Tallis Reading app

Four primary schools used the Tallis app with Year 4 pupils for one term. Pupils using the app for at least three 20-minute sessions a week (n = 146) gained an average of 6.2 points on the schools' own termly reading assessment, compared with 4.1 points for Year 4 pupils in the same schools who did not use it (n = 139). Pupils were not randomly assigned: teachers chose which classes took part. National reading test results for these pupils will not be available until next year.

Claim (vendor's marketing email): "Children who use the Tallis app score higher on national reading tests."
""", 0, 1),

# Y49 August record vs all-time record
Y("Is the blog's claim refuted by the release?",
"""
Rendle Air, monthly traffic statistics release

August 2025: 2.84 million passengers carried, up 6% on August 2024 (2.68m) and the highest figure for any August in the airline's history. Load factor 91.2%.
Year to date: 17.9 million passengers (+4%).
For reference, the airline's all-time monthly record remains 2.91 million passengers, set in July 2019 before the sale of the Norland regional subsidiary.
Capacity note: the fleet was 71 aircraft at the end of August.

Claim (aviation blog): "Rendle Air carried more passengers in August 2025 than in any previous month in its history."
""", 1, 3,
twin=([("the airline's all-time monthly record remains 2.91 million passengers, set in July 2019",
        "the airline's previous all-time monthly record was 2.79 million passengers, set in July 2019")], 0)),

# Y50 area scales with diameter squared
Y("Does the newsletter support the claim?",
"""
Observatory newsletter: Hesketh Telescope upgrade complete

After eighteen months of work, the Hesketh Telescope returned to science operations in March. The original 2.5 m primary mirror has been replaced by a new 3.5 m primary of the same design, and the telescope now carries an adaptive optics module and a refurbished spectrograph. The dome was enlarged to accommodate the new tube assembly. Engineers note that the new mirror's central obstruction is proportionally the same as the old one's, so the collecting area scales with the square of the mirror diameter.

Claim (university press release): "The Hesketh upgrade roughly doubled the telescope's light-collecting area."
""", 1, 3,
twin=([("replaced by a new 3.5 m primary", "replaced by a new 3.0 m primary")], 0)),
]
