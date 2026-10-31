"""Three-way label items (SUPPORTS / REFUTES / NOT ENOUGH INFO), part 1. Hand-written by Claude."""
from common import L

ITEMS = [
# L1 relative reduction; subgroup distractor
L("What is the correct verification label for the claim?",
"""
Science desk, press-release check
Company press-release headline: "Nexova cuts flu hospitalisations by 40% in high-risk adults"
Claim to check: "In the VANTA trial, Nexova reduced hospitalisation among high-risk adults with influenza by 40%."

Trial results (from the peer-reviewed paper, Table 2):
Population: adults with confirmed influenza and at least one risk factor, randomised within 48 h of symptom onset.
Hospitalised by day 28: Nexova 61/1,002 (6.1%); placebo 89/1,000 (8.9%).
Relative risk 0.69 (95% CI 0.50 to 0.94).
Time to symptom alleviation: 3.6 vs 4.4 days.
Pre-specified subgroup, patients over 75: hospitalised 7.2% vs 12.1%.
""", "R", 2,
twin=([("61/1,002 (6.1%)", "53/1,002 (5.3%)"), ("Relative risk 0.69 (95% CI 0.50 to 0.94)", "Relative risk 0.60 (95% CI 0.43 to 0.83)")], "S")),

# L2 undated specimens
L("Given only the evidence shown, how should the claim be labelled?",
"""
Tarrant Museum of Natural History, collection database record (public view)
Specimen: Ashgrove meteorite (main mass, 4.3 kg)
Type: carbonaceous chondrite
Fall: observed fall, Ashgrove Farm, 17 March 1911
Age: calcium-aluminium-rich inclusions dated by the lead-lead method at 4.562 billion years (Hollis and Brandt, 2019)
Display: Gallery 3, "Origins" case
Collection context: The museum holds 32 meteorites in total. Apart from Ashgrove, only the Kellet iron meteorite has been radiometrically dated (4.551 billion years); the other 30 specimens have not been dated.

Claim (gallery audio-guide script): "Ashgrove is the oldest meteorite in the Tarrant Museum's collection."
""", "N", 2,
twin=([("only the Kellet iron meteorite has been radiometrically dated (4.551 billion years); the other 30 specimens have not been dated",
        "all 31 have been radiometrically dated, and the oldest of them is the Kellet iron meteorite at 4.565 billion years")], "R")),

# L3 R&D vs sales and marketing (not SG&A)
L("Which verdict does the evidence justify for this claim?",
"""
Vantor Pharma SE, 2025 annual results, income statement (extract, € millions)
Revenue: 6,842
Cost of sales: (2,115)
Research and development: (1,210)
Selling, general and administrative: (1,904)
  of which sales and marketing: (1,180)
  of which general and administrative: (724)
Impairment of intangible assets: (96)
Operating profit: 1,517

CEO letter: "We continued to invest heavily in our pipeline, with R&D spending up 9% year on year, while holding overhead growth below inflation."

Claim (sector newsletter): "Vantor Pharma spent more on research and development than on sales and marketing in 2025."
""", "S", 2,
twin=([("of which sales and marketing: (1,180)", "of which sales and marketing: (1,280)"), ("of which general and administrative: (724)", "of which general and administrative: (624)")], "R")),

# L4 library survived
L("How should the fact-checker mark this claim?",
"""
Guidebook, Kerrow Abbey, chapter 3: "Fire and Dissolution"

On the night of 9 November 1538 fire broke out in the abbey church, probably from a brazier left burning by workmen repairing the choir roof. By morning the church was a shell: the roof, the rood screen and the choir stalls were lost, and the tower had to be pulled down the following spring. The library, however, stood in the detached west range, separated from the church by the cloister garth, and escaped the fire. When the Crown commissioners arrived in 1539 their inventory listed 214 books in the library, of which fewer than twenty can be traced today.

Claim (tourist board website): "Kerrow Abbey's library was destroyed in the fire of 1538."
""", "R", 1),

# L5 pregnancy safety unknown
L("Judged against the quoted passages, which label fits the claim?",
"""
Medicines information enquiry, hospital pharmacy
Question from a community midwife: "A patient's online forum says Serelin is safe to take in pregnancy. Is that correct?"

Extract from the Serelin summary of product characteristics, section 4.6 (Fertility, pregnancy and lactation):
"There are no or limited data from the use of Serelin in pregnant women. Studies in rats and rabbits at exposures up to 10 times the human therapeutic exposure showed no teratogenic effects. Animal studies are not always predictive of human response. Serelin should be used during pregnancy only if the expected benefit justifies the potential risk to the fetus."

Pregnancy registry: the manufacturer's registry has recorded 38 exposed pregnancies to date, which the company states is "too few to draw conclusions".

Claim: "Serelin is safe for use during pregnancy."
""", "N", 1),

# L6 hedged claim, "most likely driver"
L("Which label should the reviewer assign to the claim?",
"""
Coastal ecology programme, Morrow Bay seagrass survey 2023: executive summary

Seagrass cover in the monitored meadows fell from 412 ha in 2021 to 236 ha in 2023. The survey team examined four candidate drivers: the 2022 marine heatwave, wasting disease, increased turbidity from the Harl estuary dredging, and grazing by an expanded urchin population. The team writes: "On the balance of evidence, the most likely driver of the decline is the 2022 marine heatwave, which kept water temperatures above 26 °C for 31 days. Wasting disease was detected at low levels and cannot be excluded as a contributing factor. Turbidity and grazing do not appear to have changed enough to explain the loss."

Claim (regional news): "The survey team says the Morrow Bay seagrass decline was probably linked to the 2022 marine heatwave."
""", "S", 2,
twin=([("On the balance of evidence, the most likely driver of the decline is the 2022 marine heatwave, which",
        "We cannot yet say which driver is most likely. One candidate is the 2022 marine heatwave, which")], "N")),

# L7 completion date
L("What label does the claim get when checked against this evidence?",
"""
Grayhaven Bank plc, stock exchange announcements (chronological)

14 October 2024: Grayhaven and the board of Northlight Savings announce agreed terms for Grayhaven to acquire Northlight for £640m in cash.
9 December 2024: Northlight shareholders approve the transaction at a general meeting.
21 February 2025: The Prudential Authority grants approval for the change of control.
1 April 2025: Completion. Northlight is now a wholly owned subsidiary of Grayhaven, and Northlight's shares have been cancelled from trading.

Claim (bank's graduate recruitment brochure): "Grayhaven Bank completed its acquisition of Northlight Savings in 2024."
""", "R", 1),

# L8 inference from dates
L("Classify the claim against the evidence.",
"""
Literary society newsletter: "Poets of the Carrow coast"

Isolde Marsh (1888-1957) is best remembered for "The Salt Road", first published in the magazine Tidewrack in its issue of April 1921 and collected in her book Low Water (1926). Marsh grew up in the inland mill town of Hessle Bridge and taught there until 1923. In 1924 she moved to Carrowby for the first time, taking a cottage on the harbour, and lived there until 1930, when she left for the city. Most of the poems in Low Water that describe the Carrow coast are dated by her in manuscript to 1924 and 1925.

Claim (Carrowby tourism leaflet): "Isolde Marsh wrote 'The Salt Road' while living in Carrowby."
""", "R", 3,
twin=([("in its issue of April 1921", "in its issue of April 1925")], "N")),

# L9 universal over a flight table
L("Given the flight test report, what is the correct label for the claim?",
"""
Flight test report FT-K2-03, Kestrel-2 cargo drone, route validation
Route: Brannock depot to Selby Hill clinic and return, 40.0 km, fixed waypoints.

Flight | Date | Payload (kg) | Route completed | Notes
1 | 4 Mar | 2.0 | Yes | none
2 | 4 Mar | 2.0 | Yes | Headwind 9 m/s on outbound leg
3 | 6 Mar | 3.5 | Yes | none
4 | 6 Mar | 3.5 | Yes | Precautionary landing at depot after completion (battery temperature)
5 | 9 Mar | 5.0 | Yes | none
6 | 9 Mar | 5.0 | Yes | none
7 | 11 Mar | 5.0 | Yes | Rain
8 | 11 Mar | 5.0 | Yes | none

Summary: eight flights flown; no loss of link; maximum battery temperature 58 °C (flight 4).

Claim (investor update): "All eight Kestrel-2 test flights in report FT-K2-03 completed the full 40 km route."
""", "S", 2,
twin=([("7 | 11 Mar | 5.0 | Yes | Rain", "7 | 11 Mar | 5.0 | No | Rain; returned to depot at 26 km on operator's decision")], "R")),

# L10 negated claim vs panel finding
L("Relative to the regulator's communication, how should the claim be labelled?",
"""
Regulator's safety communication: voritinib and liver injury

The Pharmacovigilance Safety Panel has completed its review of liver injury reports with voritinib, a treatment for rheumatoid arthritis. The review covered 14 clinical trials (9,870 patients) and 212 spontaneous reports. The panel concluded that voritinib causes a small but real increase in the risk of serious liver injury (relative risk 1.4 compared with other disease-modifying treatments; absolute excess about 1 case per 2,000 patient-years). The product information will be updated to recommend liver function tests before treatment and every three months during the first year.

Claim (manufacturer's statement to investors): "The Safety Panel did not find that voritinib increases the risk of liver injury."
""", "R", 2,
twin=([("causes a small but real increase in the risk of serious liver injury (relative risk 1.4 compared with other disease-modifying treatments; absolute excess about 1 case per 2,000 patient-years)",
        "does not cause any increase in the risk of serious liver injury (relative risk 1.0 compared with other disease-modifying treatments)")], "S")),

# L11 cause of occupancy fall not given
L("Which verdict does the evidence justify for this claim?",
"""
Brightwater Office REIT, half-year report (extract)

Portfolio occupancy was 84.1% at 30 June, down from 88.3% at 31 December. The reduction reflects the expiry of two leases: Harlan Insurance vacated 61,000 sq ft at Quay House at the end of its lease, and the Office of Regional Statistics released 38,000 sq ft at Canal Court at a scheduled break date. Neither tenant has published its reasons for leaving, and we do not comment on tenants' business decisions. We are in advanced negotiations on 24,000 sq ft of the Quay House space. Across the city, office vacancy rose from 11.2% to 12.0% over the period, according to the letting agents Lyle Grant.

Claim (property newsletter): "Brightwater's occupancy fell because its tenants switched to remote working."
""", "N", 2),

# L12 date interval arithmetic
L("How should the fact-checker mark this claim?",
"""
Regimental museum, label text for case 12: "The Siege of Carrick"

Carrick Castle was invested by the army of the Northern League on 11 September 1643. The garrison of some 300 men under Sir Hal Deverill held out through the autumn, surviving two assaults and an attempt to undermine the gatehouse. With their wells failing and no relief in prospect, the garrison surrendered on honourable terms on 23 January 1644 and marched out with colours flying. The castle was slighted the following year on the orders of the League's council.

Claim (school worksheet): "The Siege of Carrick lasted more than four months."
""", "S", 2,
twin=([("23 January 1644", "3 January 1644")], "R")),

# L13 "most" vs 14 of 32
L("What is the correct verification label for the claim?",
"""
Environmental consultancy memo: Dunlin Farm microplastics screening
To: Dunlin Estates. From: Harker Environmental.

We collected 32 topsoil samples (0 to 10 cm) on a 50 m grid across the three fields that received sewage-sludge applications between 2015 and 2021. Samples were analysed by infrared microscopy for particles of 50 µm to 5 mm. Microplastics were detected in 14 of the 32 samples, at concentrations from 110 to 2,300 particles per kg of dry soil; the highest concentrations were in the east field near the former sludge store. No particles were found in the four control samples from the adjacent unsludged pasture.

Claim (campaign leaflet): "Most of the soil samples from the sludged Dunlin fields contained microplastics."
""", "R", 1,
twin=([("detected in 14 of the 32 samples", "detected in 24 of the 32 samples")], "S")),

# L14 outbreak source unconfirmed
L("Given only the evidence shown, how should the claim be labelled?",
"""
Outbreak control team, situation report 3: Linwood gastroenteritis cluster

Cases: 31 confirmed (Salmonella, single strain by genome sequencing), onset 2 to 6 August.
Exposure interviews completed: 23 of 31. Of these, 19 reported eating at the Linwood Summer Fair on 1 August, and 17 of the 19 reported eating salad from the Hartley's catering stall; the salad contained lettuce, cucumber, egg and a mayonnaise dressing made on site.
Sampling: lettuce from the stall's supplier (batch delivered 3 August) tested negative. The batch supplied for the fair had been used up or discarded before sampling. Dressing and egg samples: not available.
Status: hypothesis-generating; a case-control study is under way.

Claim (local news headline): "Linwood salmonella outbreak was caused by contaminated lettuce."
""", "N", 2),

# L15 units: $3,140 million
L("Judged against the quoted passages, which label fits the claim?",
"""
Crane & Holt Engineering, full-year trading update

Order intake for the year was $2.26 billion (prior year: $1.91 billion), including the $410 million Harbor Line rail systems contract. Revenue was $1.87 billion, giving a book-to-bill ratio of 1.21. As a result, the order backlog at 31 December stood at $3,140 million, compared with $2,750 million a year earlier. Around 45% of the closing backlog is expected to convert to revenue in the coming year. The Board expects margins to be broadly unchanged.

Claim (analyst summary): "Crane & Holt's order backlog topped $3 billion at the end of the year."
""", "S", 1),

# L16 founder entity
L("Which label should the reviewer assign to the claim?",
"""
Harwick Maritime Museum, panel 4: "Rescue from the Sea"

The Harwick lifeboat station was established in 1862, after the loss of the collier Brisk with all eleven hands within sight of the harbour. It was founded by a committee of local fishermen and merchants and paid for by public subscription; the first boat, the Grace Allen, was built in the town. In 1879 the station committee, struggling to meet the cost of a new boathouse, handed the station over to the Coastal Rescue Society, which has run it ever since. The Society rebuilt the boathouse in 1881.

Claim (Coastal Rescue Society fundraising letter): "The Harwick lifeboat station was founded by the Coastal Rescue Society in 1862."
""", "R", 2),

# L17 comparison value supplied in state
L("What label does the claim get when checked against this evidence?",
"""
Chemical safety data sheet: Tarvalene (section 9, physical and chemical properties)
Appearance: colourless liquid. Odour: faintly sweet.
Melting point: -41.2 °C.
Boiling point: 82.4 °C at 101.3 kPa.
Flash point: 11 °C (closed cup).
Density: 0.81 g/cm3 at 20 °C.
Vapour density (air = 1): 3.1.
Solubility in water: 3.2 g/L at 20 °C.
Reference values printed on the same sheet for comparison: water, melting point 0.0 °C, boiling point 100.0 °C at 101.3 kPa.

Claim (student lab report): "At sea-level pressure (101.3 kPa), Tarvalene boils at a lower temperature than water."
""", "S", 1,
twin=([("Boiling point: 82.4 °C at 101.3 kPa.", "Boiling point: 112.4 °C at 101.3 kPa.")], "R")),

# L18 "only over 70" vs range from 65
L("Classify the claim against the evidence.",
"""
Trial registry record: CORWEN (falls prevention exercise programme)
Condition: falls in older adults
Design: cluster-randomised, 48 general practices
Inclusion criteria: age 65 years or older; living at home; at least one fall in the previous 12 months; able to walk 10 m with or without an aid.
Exclusion: dementia diagnosis; terminal illness.
Enrolment (actual): 1,262 participants; median age 74 years (range 65 to 91); 68% women.
Primary outcome: rate of falls over 12 months.
Status: completed; results published.

Claim (conference poster by a different research group): "The CORWEN trial enrolled only patients over 70."
""", "R", 2),

# L19 proposals, no decision
L("Relative to the statement, how should the claim be labelled?",
"""
Hallam Motors, statement to staff and media, 2 March 2026

"Hallam Motors today began a formal consultation with employee representatives on proposals to restructure manufacturing at our Wickham plant. The proposals could affect up to 1,200 roles over the next two years. No decisions have been taken, and we will explore every alternative, including redeployment and voluntary schemes, during the 45-day consultation period."

Union response: "We will fight every one of these job losses."
Note: the statement gives no breakdown of when during the two-year period any changes would take effect.

Claim (national newspaper): "Hallam Motors will cut 1,200 jobs in 2026."
""", "N", 2),

# L20 double negation, locations
L("Which verdict does the evidence justify for this claim?",
"""
Record office blog: "Mapping Carrow: the 1612 survey"

The 1612 survey of the manor of Carrow, drawn by the surveyor John Palliser for the lord of the manor, is one of the earliest large-scale maps of the district. Two manuscript copies are known to survive. The fair copy, on vellum, was bought by the county record office at Wexham in 1953 and is kept there. The working copy, on paper and with Palliser's annotations, is in a private collection in Lisbrook, forty miles to the south, and was last exhibited in 1987. Carrow's own parish chest contains only an 1840s tracing of part of the map.

Claim (Carrow village website): "Neither of the two surviving copies of the 1612 survey map is held in Carrow itself."
""", "S", 2,
twin=([("is in a private collection in Lisbrook, forty miles to the south, and was last exhibited in 1987",
        "is in a private collection whose location the owner has asked the record office not to disclose; it was last exhibited in 1987")], "N")),

# L21 different species
L("How should the fact-checker mark this claim?",
"""
Research summary, Pollinator Toxicology Unit annual report

Study PT-17: sublethal effects of the insecticide Dralox. Honeybee workers were fed sugar syrup containing Dralox at field-realistic concentrations (1 and 5 parts per billion) for ten days. Foraging trips fell by 30% at 5 ppb compared with controls; no effect was seen at 1 ppb. Colony-level effects were not measured. A follow-up study with bumblebee colonies has been funded and will start next spring.

Claim (environmental group briefing): "The insecticide Dralox harms bumblebee colonies."
""", "N", 1),

# L22 ratio > 10
L("What is the correct verification label for the claim?",
"""
Haverly Cohort Study, cancer incidence report, table 4 (extract)
Lung cancer incidence per 100,000 person-years, age-standardised, by smoking status at enrolment:
Never smoked: 14
Former smokers (quit 10 or more years before enrolment): 41
Former smokers (quit less than 10 years before enrolment): 97
Current smokers: 162
Current smokers, 20 or more cigarettes a day: 288
Person-years of follow-up: 2.41 million. Cases: 1,318.
Incidence is age-standardised to the cohort's age distribution at enrolment. Smoking status was self-reported and not updated during follow-up.

Claim (public health poster): "In the Haverly cohort, lung cancer incidence among current smokers was more than ten times that of people who had never smoked."
""", "S", 2,
twin=([("Current smokers: 162", "Current smokers: 126")], "R")),
]
