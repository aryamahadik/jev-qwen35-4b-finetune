"""Three-way label items (SUPPORTS / REFUTES / NOT ENOUGH INFO), part 2. Hand-written by Claude."""
from common import L

ITEMS = [
# L23 each year vs cumulative
L("Which label should the reviewer assign to the claim?",
"""
Ormsby Capital, Global Equity Fund factsheet (extract)
Discrete annual performance (net of fees, Class A)
Year | Fund | Benchmark (Halden World Index)
2023 | 8.2% | 7.9%
2024 | 11.4% | 12.0%
2025 | 6.1% | 5.5%
Cumulative three years: Fund 27.9%; Benchmark 27.5%.
Fund manager: Tomasz Weller, since 2019. Fund size: £1.3bn. Ongoing charge: 0.85%.
Past performance is not a reliable indicator of future results.

Claim (adviser's email to a client): "Ormsby's Global Equity Fund beat its benchmark in each of the last three years."
""", "R", 1),

# L24 attribution undecided
L("Given only the evidence shown, how should the claim be labelled?",
"""
Conservation report: the Wrenfield Tapestry (Great Hall of Wrenfield House)
Subject: the "Hunt of the White Hart" panel, c. 1520 to 1540

Summary of findings: The design and border style closely resemble work from Flemish workshops of the period, and the panel was long catalogued as Flemish. However, the dye analysis (18 samples) identified weld, woad and madder, which were used both in Flanders and in English workshops of the period, and so does not discriminate between them. No weaver's or town marks survive; the lower edge, where such marks were usually woven, was cut away in the eighteenth century. An English workshop copying Flemish designs cannot be ruled out.

Claim (house guidebook): "The Wrenfield tapestry was woven in Flanders."
""", "N", 2),

# L25 "unbroken" vs hiatus
L("What is the correct verification label for the claim?",
"""
Ice core project report: Station Halvard deep core (HVD-2)

Core length 1,642 m. Annual layers were identified by continuous flow analysis of sodium, calcium and hydrogen peroxide and counted downward from the surface. Layers were counted continuously back to 9,700 years before present, except for a hiatus at 812 to 818 m depth, dated to about 5,300 years ago, where roughly 140 years of layers are missing, probably because wind scoured the snow surface at that time. Below 9,700 years, layers are too thin to count and the chronology is based on flow modelling tied to volcanic markers.

Claim (project outreach page): "The Halvard ice core preserves an unbroken sequence of annual layers going back 9,700 years."
""", "R", 3),

# L26 time to treatment; outcomes pending is irrelevant
L("How should the fact-checker mark this claim?",
"""
Evaluation summary: Welbeck mobile stroke unit, first 18 months

The mobile stroke unit (an ambulance with an on-board CT scanner and a stroke-trained clinician) was dispatched alongside standard ambulances to suspected stroke calls within 25 km of Welbeck General on weekdays, 8am to 8pm. Patients given clot-busting treatment (thrombolysis): mobile unit 214; standard pathway (ambulance to hospital, same hours and area) 198. Mean time from emergency call to thrombolysis: 58 minutes (mobile unit) vs 91 minutes (standard pathway). Functional outcomes at 90 days are still being analysed.

Claim: "Stroke patients who received clot-busting treatment from the Welbeck mobile unit received it faster on average than those taken to hospital by standard ambulance."
""", "S", 1),

# L27 AISC excludes costs
L("Which verdict does the evidence justify for this claim?",
"""
Loxley Mining, announcement of feasibility study results: Tarrin copper project

The definitive feasibility study estimates all-in sustaining costs (AISC) of US$6,100 per tonne of copper over the 17-year mine life. Annual production is projected at 142,000 tonnes of copper in concentrate. AISC as defined in the study covers mining, processing, site administration and sustaining capital. It excludes government royalties, the repayment and interest cost of the US$1.9 billion initial construction capital, and corporate overheads; the company has not disclosed these figures. A board decision on whether to proceed is expected by the end of the year.

Claim (mining forum): "The Tarrin mine will be profitable at a copper price of US$8,000 per tonne."
""", "N", 3),

# L28 earliest known newspaper
L("Judged against the bibliography entry, which label fits the claim?",
"""
Bibliography of the provincial press: entry for Ellesby

Ellesby Mercury (weekly). First issue: 14 March 1788; ceased 1811. The earliest known newspaper printed in Ellesby; a complete file is held by the Ellesby Library.
Ellesby Courant (weekly). First issue: 2 January 1794; merged with the Mercury in 1811 to form the Ellesby Mercury and Courant.
Ellesby Weekly Register. Proposed in a prospectus of 1785; no issue is known to have been published.
Note: handbills and auction notices were printed in Ellesby from at least 1771.

Claim (town anniversary booklet): "The first newspaper printed in Ellesby appeared in the 1790s."
""", "R", 1),

# L29 negated claim; failure after cruise
L("What label does the claim get when checked against this evidence?",
"""
Mission status report: Gellert outer-planet probe, cruise phase closeout

Of the eleven science instruments, nine operated normally throughout the six-year cruise. Two failed during cruise: the dust counter (loss of high-voltage supply, cruise year 2) and the ultraviolet spectrometer (detector degradation, cruise year 5). The magnetometer operated nominally for the whole cruise and returned calibration data at each of the three planetary flybys. After orbit insertion, however, the magnetometer boom's deployment motor failed, and the instrument now returns degraded data.

Claim (outreach blog): "The Gellert probe's magnetometer was not among the instruments that failed during the cruise phase."
""", "S", 2),

# L30 "no cases since 2020"
L("Classify the claim against the evidence.",
"""
Tarn Valley Public Health Unit, annual communicable disease report: measles section

Year | Confirmed cases | Notes
2020 | 0 |
2021 | 0 |
2022 | 2 | Both imported (travellers returning from abroad); no onward transmission
2023 | 0 |
2024 | 0 |
2025 | 0 |
Suspected cases notified and tested negative: 17 in 2025.
Measles-containing vaccine coverage at age 5: 94.1% (2025).
Elimination status: the region is considered to have no endemic measles transmission.

Claim (council newsletter): "Tarn Valley has had no reported cases of measles since 2020."
""", "R", 1),

# L31 adjusted profit arithmetic; restructuring trap
L("Relative to the reconciliation, how should the claim be labelled?",
"""
Pellis Chemicals AG, 2025 results: adjusted-profit reconciliation (€ million)

Reported operating profit 2025: 412 (2024: 331)
Included in 2025: gain on disposal of the Dorrin plant: 96
Included in 2025: restructuring charges: (18)
Included in 2024: no disposal gains or restructuring charges

Management commentary: "Reported operating profit rose strongly, helped by the Dorrin disposal. Volumes in specialty coatings were weak in the second half, and we took restructuring charges to right-size the coatings business."

Claim (analyst note): "Excluding the gain on the Dorrin plant sale, Pellis Chemicals' 2025 operating profit was lower than its 2024 operating profit."
""", "S", 3,
twin=([("gain on disposal of the Dorrin plant: 96", "gain on disposal of the Dorrin plant: 66")], "R")),

# L32 order of events
L("Which label should the reviewer assign to the claim?",
"""
Housing history seminar, handout for week 4

4 March 1889: Collapse of two tenement blocks in Brindle Street, Garrowby; 23 residents killed.
April 1889: Public meeting at the Corn Exchange demands an inquiry.
May 1889: Town council appoints a commission of inquiry chaired by Dr Edwin Hale.
December 1889: The Hale Commission's report is published; it finds that 40% of the borough's tenements lack adequate foundations.
1891: Garrowby Improvement Act passed, drawing on the report's recommendations.
Discussion question: why did it take two more years to legislate?

Claim: "The Hale Commission's report was published after the collapse of the Brindle Street tenements."
""", "S", 1),

# L33 before/after the ban
L("Given only the evidence shown, how should the claim be labelled?",
"""
Lake Semmer water quality: trend note for the Catchment Board

Total phosphorus (annual mean, µg/L) at the deep-water station:
2008: 44 | 2009: 43 | 2010: 45 | 2011: 41 | 2012: 38 | 2014: 29 | 2016: 24 | 2018: 21 | 2020: 18

The regional ban on phosphate laundry detergents took effect on 1 January 2012. Sewage works upgrades at Semmer and Hollin (phosphorus stripping) were commissioned in 2015. Sampling was biennial from 2012; no data are yet available after 2020.

Claim (council press release): "Phosphorus levels in Lake Semmer fell after the phosphate detergent ban took effect."
""", "S", 2,
twin=([("took effect on 1 January 2012", "took effect on 1 January 2021")], "N")),

# L34 items vs patients
L("What is the correct verification label for the claim?",
"""
Prescribing data briefing, Varrow Integrated Care Board
Melatonin prescription items dispensed for patients aged under 18:
2019: 18,200
2020: 19,900
2021: 23,400
2022: 26,800
2023: 29,700
2024: 31,900

Over the same period the number of patients aged under 18 receiving at least one melatonin prescription rose from 3,150 to 6,420. Around 70% of items were for children with a recorded neurodevelopmental condition. Each item is one prescription dispensed by a community pharmacy.

Claim (newspaper): "The number of melatonin prescriptions dispensed for children in Varrow doubled between 2019 and 2024."
""", "R", 3),

# L35 transaction date ambiguous
L("How should the fact-checker mark this claim?",
"""
Market surveillance note: Ferro Group plc, director dealing

Director dealing notification (filed 16 May): the Chief Executive, Lukas Brandt, sold 40,000 ordinary shares; the average price is not stated in the filing. Date of transaction as stated in the filing: "during the week commencing 11 May".
Profit warning: released via the exchange news service at 07:00 on Wednesday 13 May. The shares fell 27% that day.
Surveillance comment: the filing does not specify the transaction date more precisely, and the company has not responded to our request for the trade confirmation.

Claim (financial newspaper): "Ferro Group's chief executive sold shares before the profit warning was announced."
""", "N", 3,
twin=([('"during the week commencing 11 May"', '"11 May"'), ("the filing does not specify the transaction date more precisely, and ", "")], "S")),

# L36 "some" satisfied
L("Which verdict does the evidence justify for this claim?",
"""
Treasure report: Kellsby hoard (find reference KY-2024-03)

The hoard was found by a metal-detectorist in a ploughed field near Kellsby in March 2024 and excavated by the county archaeology service. It comprises 212 silver coins deposited in a coarse-ware jug, probably in the 1460s. Of the coins, 198 are issues of the kingdom's own mints (mainly the capital and the two northern mints); the remaining 14 are foreign: 11 from the trading cities of the Eastland League and 3 from the Duchy of Maurenne. The latest coin in the hoard dates the deposit to after 1461.

Claim (museum acquisition news): "Some of the coins in the Kellsby hoard were minted outside the kingdom."
""", "S", 1),

# L37 order of magnitude; 2 km scar distractor
L("Classify the claim against the evidence.",
"""
Geological survey rapid-response note: Arden valley landslide, 9 February

A rock slope failure occurred at about 04:10 on the east flank of the Arden valley above the hamlet of Low Arden. The failure scar is about 2 km long measured along the ridge crest and up to 180 m high. Drone photogrammetry puts the displaced volume at about 0.2 million cubic metres (200,000 m3), with an uncertainty of plus or minus 15%; most of the debris came to rest on the valley floor, blocking the river for six hours. Two houses were evacuated; no injuries were reported.

Claim (national news): "The Arden landslide moved about 2 million cubic metres of rock."
""", "R", 1),

# L38 surrogate endpoint
L("What label does the claim get when checked against this evidence?",
"""
Journal abstract, Cardiovascular Therapeutics Letters
Title: Cardivex (ezalumab) for LDL cholesterol lowering in statin-treated patients: the ELEVATE-12 randomised trial

Methods: 612 patients with LDL cholesterol of 2.6 mmol/L or more despite maximum-tolerated statin were randomised to Cardivex 150 mg monthly or placebo for 12 weeks.
Results: Cardivex lowered LDL cholesterol by 38% relative to placebo (p < 0.001). Adverse events were similar between groups.
Conclusions: Cardivex substantially lowers LDL cholesterol. The trial was not designed or powered to assess cardiovascular events such as heart attack; an outcomes trial is under way.

Claim (drug company advert): "Cardivex prevents heart attacks."
""", "N", 2),

# L39 percentage points of margin
L("Judged against the preliminary results, which label fits the claim?",
"""
Dunmore Brands plc, preliminary results (extract)

Revenue £1,242m (+5.8%). Gross profit £517m (+12.4%). Gross margin 41.6% (2024: 39.2%). Operating margin 12.9% (2024: 12.1%). Net debt £388m. Final dividend 21.5p.
The improvement in gross margin reflects lower freight costs and a richer product mix in premium spirits.
Chief Executive: "Our premium spirits portfolio delivered another year of double-digit growth, and we continued to invest behind our brands, with marketing spend rising to 16.2% of revenue."

Claim: "Dunmore's gross margin widened by more than two percentage points in 2025."
""", "S", 2,
twin=([("Gross profit £517m (+12.4%)", "Gross profit £517m (+9.8%)"), ("Gross margin 41.6% (2024: 39.2%)", "Gross margin 41.6% (2024: 40.2%)")], "R")),

# L40 correction slip supersedes label
L("Which label should the reviewer assign to the claim?",
"""
Town museum: object label and archivist's correction slip

Label (printed 1998): "Silver chain of office, presented to Mayor Ansel Brody, who served three terms (1901-1907) and oversaw the building of the Corporation Baths."

Correction slip added by the borough archivist, 2025: "Council minutes show that Brody was elected mayor in 1901 and re-elected in 1903. His re-election in November 1905 was declared void on petition in January 1906 because of irregularities in the ward rolls, and Alderman Pike served out the term. Brody therefore served two terms, not three. The Baths were opened in 1904."

Museum policy note: where an archivist's correction slip conflicts with a printed label, the correction slip is authoritative.

Claim (heritage website): "Mayor Ansel Brody served three terms as mayor."
""", "R", 2),

# L41 modelled range, large uncertainty
L("Relative to the technical note, how should the claim be labelled?",
"""
Coastal authority technical note: relative sea-level change at Port Venner

Tide gauge record: the Port Venner gauge was installed in 1983. From 1983 to 2020 the annual mean sea level rose by 11 cm (about 2.9 mm per year).
Before 1983: there is no gauge record for Port Venner. Model reconstructions based on the nearest long record (Carrick Point, 140 km away) and on estimates of local land subsidence suggest a rise of roughly 20 to 35 cm between 1950 and 2020, but the authors describe the uncertainty as "large" because the subsidence rate before 1983 is poorly known.

Claim (local campaign group): "Sea level at Port Venner rose by 30 cm between 1950 and 2020."
""", "N", 3),

# L42 cumulative survey categories
L("What is the correct verification label for the claim?",
"""
Crowmarsh Nurses' Forum, staff survey 2025: results summary
Responses: 1,412 of 2,180 nurses and midwives employed by the trust (65% response rate).

Q7. How often, on average, do you work beyond your rostered hours without being paid for it?
Most shifts: 23%
About once a week: 38%
About once a month: 21%
Rarely or never: 18%
All respondents worked at least three rostered shifts a week.

Q8. Did you feel able to take your full meal break on your last shift? Yes: 44%.

Claim (union press release): "Most respondents to the Crowmarsh survey said they worked unpaid overtime at least once a week."
""", "S", 2),

# L43 effective date for existing members
L("How should the fact-checker mark this claim?",
"""
Harrowgate Building Society: savings rate change notice

Following the central bank's reduction of Bank Rate on Thursday 6 August, we announced on Friday 7 August that we will reduce the variable rates on our easy-access and regular-saver accounts by 0.25 percentage points. The new rates take effect on 1 September for existing members and applied immediately, from 7 August, to new accounts opened on or after that date. Fixed-rate bonds and ISAs already open are not affected. Members who prefer to move their savings can do so without penalty until 30 September.

Claim (consumer website): "Harrowgate cut its savings rates for existing members before the central bank's rate decision."
""", "R", 2),

# L44 forecast range straddles the claim
L("Which verdict does the evidence justify for this claim?",
"""
Space agency debris office: object status summary

Object: CORVIN-9 (Earth-observation satellite, decommissioned 2024)
Current orbit: near-circular, mean altitude 410 km, inclination 51.6 degrees.
Propulsion: none remaining; passive decay.
Predicted re-entry: between 3 and 12 years from the date of this summary, depending mainly on solar activity; the central estimate is 6 years. Predictions will be refined as the object descends.
Casualty risk: the satellite is expected to burn up entirely; no fragments are predicted to reach the ground.

Claim (space news site): "CORVIN-9 will re-enter the atmosphere within five years of this summary."
""", "N", 2),
]
