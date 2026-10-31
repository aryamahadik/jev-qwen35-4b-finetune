"""Yes/no claim-verification items, part 1 (health and science mostly). Hand-written by Claude."""
from common import Y

ITEMS = [
# Y1 halving: overall vs subgroup
Y("Does the evidence support the claim?",
"""
Fact-check desk, ticket FC-2291
Claim (from a supplement retailer's newsletter): "In the Harlow Vale trial, a daily vitamin D dose cut the rate of winter chest infections among care-home residents by half."

Evidence supplied by the desk researcher:
[1] Harlow Vale Care Trial, final report, section 4.2: 1,204 residents in 38 care homes were randomised to 2,000 IU vitamin D daily or an identical placebo from October to March. Over the winter, at least one physician-confirmed chest infection occurred in 10.3% of residents in the vitamin D group and 20.6% of residents in the placebo group.
[2] Section 4.4: In the pre-specified subgroup with low baseline vitamin D (n = 311), the corresponding figures were 11.8% and 26.5%.
[3] Section 6: Adverse events were similar in both groups; two cases of mild hypercalcaemia occurred, both in the vitamin D group.
""", 1, 2,
twin=([("10.3% of residents in the vitamin D group", "15.3% of residents in the vitamin D group")], 0)),

# Y2 universal "every year" with counterexamples
Y("Do the survey notes refute the panel's claim?",
"""
From: Ines Morland
To: Tomas Pryce
Subject: Caption check, Kessler Ridge panel

Tomas,
The visitor-centre panel currently says: "The Kessler Ridge Glacier has retreated every single year since monitoring began in 1978." The printer needs sign-off by Friday. Can you check it against the survey series?
Ines

From: Tomas Pryce
Re: Caption check, Kessler Ridge panel

Ines, the terminus survey has been run each September since 1978 with no gaps. Cumulative retreat to last September is 1.46 km. The pace picked up after 2000: about 38 m a year on average, against about 17 m a year before that. Three seasons stand out, 1986, 1993 and 2011, when the terminus was surveyed 4 to 11 m further down-valley than in the previous September; we put that down to exceptionally heavy winter snowfall. Apart from those three, annual retreat ranged from 6 to 71 m. Happy to talk through the chart if the designer wants it.
Tomas
""", 1, 3,
twin=([("further down-valley than", "further up-valley than")], 0)),

# Y3 population excluded
Y("Is the evidence enough to establish the claim as true?",
"""
Clinical evidence summary, prepared for the Formulary Committee, Brenmoor Health Trust
Claim under review (from the manufacturer's detail aid): "Corvalene lowers LDL cholesterol in adults with familial hypercholesterolaemia."

[1] CORVA-2 (phase II, 24 weeks): 418 adults with LDL cholesterol above 4.0 mmol/L who could not tolerate statins were randomised 2:1 to Corvalene 180 mg daily or placebo. LDL cholesterol fell by 31% from baseline with Corvalene and by 2% with placebo.
[2] Exclusion criteria for CORVA-2 included a clinical or genetic diagnosis of familial hypercholesterolaemia, secondary causes of raised cholesterol, and eGFR below 30.
[3] CORVA-FH, a trial restricted to patients with familial hypercholesterolaemia, opened to recruitment in January; no results are expected before next year.

Committee note: the summary above is the complete evidence package submitted by the manufacturer.
""", 0, 2),

# Y4 hedge in the panel conclusion
Y("Does the evidence support the claim?",
"""
Oslund Agronomy Board, bulletin No. 114
Subject: Review of Meridian fungus seed inoculant

Background: Meridian, a soil fungus sold as a seed coating, has been marketed to cereal growers in the Oslund region since 2021. The Board's review panel was asked whether the product should be listed in the Board's recommended-inputs guide.

Data reviewed: 22 commercial farms, four growing seasons, split-field design, winter wheat only. Inoculated halves averaged 7% higher grain yield than untreated halves, with results ranging from a 3% loss to a 15% gain between farms and seasons.

Panel conclusion (quoted in full): "Inoculation with Meridian may increase winter wheat yields under Oslund conditions. The product will be listed in the guide."

Claim to check (from a farming newspaper): "The Oslund Agronomy Board's review panel has concluded that inoculating winter wheat with Meridian increases yields."
""", 0, 2,
twin=([("Inoculation with Meridian may increase winter wheat yields", "Inoculation with Meridian increases winter wheat yields")], 1)),

# Y5 sequential growth; YoY distractor
Y("Do the figures contradict the proposed statement?",
"""
Investor-relations Q&A draft, Brennick Foods plc
Statement proposed for the Q&A sheet: "Brennick Foods' quarterly revenue rose from each quarter to the next throughout fiscal 2025."

Revenue by quarter, fiscal 2025 (£ millions, unaudited):
Q1 (Apr-Jun): 412.6
Q2 (Jul-Sep): 418.9
Q3 (Oct-Dec): 417.2
Q4 (Jan-Mar): 431.0

Notes from the finance team: Full-year revenue was £1,679.7m, up 6.1% on fiscal 2024. Each quarter's revenue was higher than the same quarter of the previous year. Q3 includes a one-off £3.5m credit to customers after a labelling recall, which management describes as non-recurring.
""", 1, 2,
twin=([("Q3 (Oct-Dec): 417.2", "Q3 (Oct-Dec): 421.4"), ("£1,679.7m", "£1,683.9m")], 0)),

# Y6 strike outcome
Y("Is the claim supported by the catalogue entry?",
"""
County Record Office, catalogue entry TRW/4/17
Title: Papers of the Tarrow Mill Strike Committee, 1887

Scope and content: Minute book, relief-fund ledger and correspondence of the committee formed when 640 spinners and piecers at Tarrow Mill walked out on 14 February 1887 over a proposed 7.5% wage reduction and the owners' refusal to discuss shorter hours. The minute book records weekly mass meetings and the committee's demand for a ten-hour day. The ledger shows relief payments falling from 9s. to 3s. per family by late April as donations dried up. The final minute, dated 2 May 1887, records a vote of 402 to 118 to return to work "on the terms offered by the masters", namely the wage reduction halved to 3.75% and no change to hours. A covering note by the cataloguer adds that the ten-hour day was not introduced at Tarrow until the Factory (Amendment) Act of 1891 applied it across the district.

Claim (from a heritage-trail leaflet draft): "The Tarrow Mill strike of 1887 ended with the owners conceding the ten-hour day."
""", 0, 1),

# Y7 superseded value footnote
Y("Does the report support the newsletter's claim?",
"""
Hydrogeology report extract, Venn Moor former smelter site
Prepared for: Venn Moor Parish Council
Guideline value used throughout: arsenic 10 µg/L (drinking-water guideline)

Table 3. Dissolved arsenic in groundwater, sampling round 2
Borehole | Depth (m) | Arsenic (µg/L)
BH1 | 18 | 14.0
BH2 | 22 | 11.5
BH3 | 15 | 12.1*
BH4 | 30 | 22.0
BH5 | 26 | 10.4

*Superseded. BH3 was resampled on 14 March after the casing seal was found to be leaking surface run-off into the borehole. The valid result for BH3 is 9.8 µg/L and replaces the value shown in the table.

Laboratory QA: all results are within the laboratory's accredited range.

Claim in the parish newsletter: "Groundwater samples from all five boreholes at Venn Moor exceeded the arsenic guideline."
""", 0, 3,
twin=([("The valid result for BH3 is 9.8 µg/L", "The valid result for BH3 is 10.8 µg/L")], 1)),

# Y8 adults only, claim about children
Y("Can the claim be verified as true from the thread?",
"""
Parent forum, Breathe Easy Families board
Thread: "Is Pellam any good for kids?"

Post by jonah_and_mia: "Our GP mentioned Pellam for my 9-year-old. I read somewhere that the ALTO-2 study showed it cut A&E visits in children. Is that right?"

Reply by pharmacist_ros (verified pharmacist): "Here's what the published ALTO-2 paper actually says, quoting the methods and results: 'ALTO-2 randomised 2,340 patients aged 18 to 64 with moderate persistent asthma to Pellam or standard inhaled steroid for 52 weeks. Asthma-related emergency department visits were 28% lower with Pellam (rate ratio 0.72).' The manufacturer's site also says: 'A paediatric study, ALTO-Kids, is planned to begin in 2027.' That's all the published data I'm aware of."

Claim being checked: "In the ALTO-2 study, Pellam reduced emergency visits in children with asthma."
""", 0, 1),

# Y9 percent vs percentage points
Y("Is the social-media claim refuted by the notice?",
"""
Westmere Credit Union, member notice, 3 March
Changes to our Standard Variable Mortgage Rate

Following the central bank's decision on 27 February, we are increasing our Standard Variable Rate from 4.00% to 4.25% with effect from 1 April. This is an increase of 0.25 percentage points. For a typical £150,000 repayment mortgage with 20 years remaining, monthly payments will rise by around £20. Fixed-rate and tracker members are not affected by this change. Members who wish to discuss their options can call our mortgage team on weekdays.

Claim (social-media post): "Westmere Credit Union has raised its standard variable mortgage rate by 25 percent."
""", 1, 3,
twin=([("from 4.00% to 4.25%", "from 1.00% to 1.25%")], 0)),

# Y10 order of events; temporary footbridge distractor
Y("Does the gazetteer support the claim?",
"""
Dunmere Local History Society, online gazetteer

Entry: Oriel Bridge
The Oriel Bridge carries Castle Street over the River Cass. A ferry and, from 1845, a temporary timber footbridge served the crossing while the stone bridge was built. Construction of the three-arch bridge, designed by the county surveyor Walter Hine, began in 1844 but was set back by winter floods that carried away the centering. The bridge was formally opened by the mayor in June 1847, and tolls were abolished in 1869.

Entry: Dunmere Station
The Carlow and Dunmere Railway reached the town in the autumn of 1846, with the first passenger train arriving on 12 October. The original station building was replaced in 1889.

Claim (school project): "The Oriel Bridge was opened before the railway reached Dunmere."
""", 0, 2,
twin=([("June 1847", "June 1845")], 1)),

# Y11 "no living organisms" vs cultured bacteria
Y("Do the cruise findings refute the claim?",
"""
Cruise report summary, RV Callan Mhor, expedition CM-24
Section 5.3, Biological sampling below 9,000 m

Two box cores and one baited trap were deployed at 9,410 m in the Varne Deep. The baited trap was recovered after 36 hours with bait intact and no amphipods or other scavengers present; video from the lander showed no fish or other macrofauna. Sediment from both box cores was subsampled aboard and cultured at in-situ pressure and 2 °C. After 21 days, cultures from both cores yielded viable bacterial colonies, identified by sequencing as members of two pressure-loving genera. Control plates exposed to ship's air remained sterile.

Claim (from a popular-science article): "The Varne Deep expedition found no living organisms below 9,000 metres."
""", 1, 2,
twin=([("yielded viable bacterial colonies, identified by sequencing as members of two pressure-loving genera",
        "yielded no viable bacterial colonies; sequencing detected only degraded DNA fragments from two pressure-loving genera")], 0)),

# Y12 association vs causation
Y("Should the claim be marked SUPPORTS?",
"""
Health column fact-check, reader query
Reader wrote in: "My brother says drinking three or more cups of coffee a day causes a lower risk of liver disease. Is that proven?"

Research summary provided by our health desk:
[1] The Northfield Cohort followed 94,310 adults for a median of 11 years. Participants who reported drinking three or more cups of coffee a day at enrolment had a 21% lower rate of chronic liver disease than non-drinkers after adjustment for age, sex, alcohol intake, smoking and body-mass index (hazard ratio 0.79; 95% CI 0.70 to 0.89).
[2] The authors write: "Because this is an observational study, we cannot establish that coffee consumption itself is responsible for the lower risk; unmeasured differences between coffee drinkers and non-drinkers may explain part or all of the association."
[3] No randomised trial of coffee intake and liver disease outcomes has been published.

Claim to check: "Drinking three or more cups of coffee a day causes a lower risk of chronic liver disease."
""", 0, 1),

# Y13 attribution in transcript
Y("Does the transcript support the claim?",
"""
Transcript excerpt, Karsten Logistics Q2 earnings call

Analyst (Priya Anand, Colbeck Securities): "Thanks. On margins: given the fuel hedges rolling off and the new Leeds hub coming online, is it fair to say you expect margins to improve in 2027?"

CFO (Hendrik Voss): "I wouldn't go that far. What we've said, and I'll repeat it, is that we expect operating margin to be broadly stable in 2027, around the 6.5% we're guiding for this year. The Leeds hub carries start-up costs through most of 2027. We see a path to improvement in 2028 once the hub is at full volume, but that's not guidance."

Analyst: "Understood, thanks."

Claim in a trade-press article: "Karsten Logistics' chief financial officer said the company expects its margins to improve in 2027."
""", 0, 2),

# Y14 perihelion vs Earth approach
Y("Is NOT ENOUGH INFO the correct label for this claim?",
"""
Minor-planet bulletin circular, excerpt

Comet C/2024 R3 (Varga)
Discovered 7 September 2024 by the Halvik Sky Survey. Orbit solution from 212 observations spanning 64 days. Perihelion date: 2026 January 21. Perihelion distance (from the Sun): 0.19 AU. Eccentricity: 0.9994. Inclination: 71.3 degrees.
Remarks: The comet's closest approach to Earth has not yet been determined because the orbit solution is still preliminary; an updated circular will follow when the observation arc is longer.

Comet C/2024 R2 (Tanaka)
Discovered 3 September 2024. Closest approach to Earth: 0.18 AU on 2025 November 30.

Claim (astronomy club newsletter): "Comet C/2024 R3 (Varga) will pass within 0.2 AU of Earth."
""", 1, 3,
twin=([("has not yet been determined because the orbit solution is still preliminary; an updated circular will follow when the observation arc is longer.",
        "will be 0.84 AU, on 2026 February 3.")], 0)),

# Y15 dose: adults vs children
Y("Do the prescribing notes support the claim?",
"""
Prescribing information, Tovarin (tovaretide) 25 mg and 50 mg tablets

Section 4.2 Posology
Adults (18 years and over): 50 mg once daily, taken with food. Patients with moderate hepatic impairment: 25 mg once daily. Severe hepatic impairment: not recommended.
Children 6 to 11 years: 25 mg twice daily. Children 12 to 17 years: 50 mg once daily.
Elderly: no dose adjustment is required.
Missed dose: if a dose is missed, take it as soon as remembered unless it is within 8 hours of the next dose; do not take two doses at once.

Section 4.4 Special warnings: monitor liver function at baseline and at 3 months.

Claim (patient information website): "The recommended adult dose of Tovarin is 50 mg twice daily."
""", 0, 2,
twin=([("Adults (18 years and over): 50 mg once daily", "Adults (18 years and over): 50 mg twice daily")], 1)),

# Y16 "with all hands" vs survivors
Y("Does the evidence contradict the claim?",
"""
Maritime history forum, thread "Lost ships of the Fenmouth coal trade"

Post by harbour_archivist:
"Here's what I found on the brig Alder Grace for anyone researching her. The underwriters' loss book for 1872 lists her as 'posted missing, 11 December 1872, Fenmouth for Riga, coal, crew 9'. The Fenmouth Advertiser of 21 December 1872 then reports: 'Two seamen of the brig Alder Grace, the mate Samuel Ord and a boy, were landed at Fenmouth yesterday by the barque Solvind, having been taken off a waterlogged boat after the brig foundered in a gale. Of the rest of the crew nothing has been heard.' No later report of other survivors that I can find."

Claim (from a local history book): "The brig Alder Grace sank in 1872 with all hands."
""", 1, 1),

# Y17 "some ... completely" vs none
Y("Is the claim supported by the notebook?",
"""
Lab notebook, Membrane Group, Sellick University (shared summary page)
Experiment M-41: sodium rejection by graphene-oxide membranes

Forty membranes from batch GX-7 were tested in the standard two-chamber cell with 0.5 M NaCl feed, 6 h runs, sodium measured in the permeate by ICP-OES (detection limit 0.02 mg/L).
Results: 36 membranes reduced sodium flux by more than 99% relative to the open-cell control. None of the 36 blocked sodium entirely; the lowest permeate concentration measured was 0.9 mg/L. Four membranes cracked during mounting and were excluded.
Next steps: thicker laminate (GX-8) to be tested next month.

Claim (grant progress report draft): "Some of the batch GX-7 graphene-oxide membranes blocked sodium ions completely in experiment M-41."
""", 0, 2,
twin=([("None of the 36 blocked sodium entirely; the lowest permeate concentration measured was 0.9 mg/L.",
        "Three of the 36 blocked sodium entirely, with no sodium detected in the permeate.")], 1)),

# Y18 point-in-time figure vs "today"
Y("Can the advert line be confirmed from the attached sources?",
"""
Internal marketing review, Aldmoor Bank

Draft advert line submitted by Retail Marketing: "Aldmoor Bank's CET1 ratio is above 14% today, one of the strongest capital positions on the high street."

Sources attached by Marketing:
[1] Annual Report 2024, p. 12: "At 31 December 2024, our Common Equity Tier 1 (CET1) ratio was 14.6%, up from 13.9% a year earlier."
[2] Investor presentation, March 2025: "We target a CET1 ratio of 13 to 14% over the medium term and expect to distribute surplus capital above that range."

Reviewer instructions: judge the line only against the attached sources. The review is being carried out in September 2026; no figure later than those in the sources has been provided.
""", 0, 2),

# Y19 negated question; composite vs MI
Y("Does the evidence fail to support the claim?",
"""
Journal club handout, cardiology registrars, week 9
Trial: PRISM-7 (lorvastin vs placebo in patients with stable coronary disease)
Design: double-blind RCT, 4,016 patients, median follow-up 3.1 years.

Primary endpoint (composite of cardiovascular death, myocardial infarction or stroke): 7.9% lorvastin vs 9.6% placebo.
Secondary endpoints:
- Myocardial infarction (heart attack): 41 of 2,010 patients on lorvastin; 63 of 2,006 on placebo.
- Stroke: 29 vs 27.
- Cardiovascular death: 88 vs 102.
Discussion point for the group: was the stroke result a chance finding?

Claim for discussion: "In PRISM-7, fewer patients taking lorvastin had heart attacks than patients taking placebo."
""", 0, 2, role="neg",
twin=([("41 of 2,010 patients on lorvastin", "71 of 2,010 patients on lorvastin")], 1)),

# Y20 discovery vs first record
Y("Is the claim refuted by the archive note?",
"""
Observatory archive note, Linden Observatory plate collection
Nova Cygni 1923

The nova was discovered by the amateur observer Ada Kestrel of Wray Hill, who noticed a new naked-eye star in Cygnus on the evening of 2 August 1923 and reported it by telegram the next morning. A search of the Linden plate stacks in 1924 found the nova on two survey plates exposed on 4 August 1923; no Linden plate from before 4 August covers that region of sky. The Linden plates are the earliest photographic record of the outburst and are used to fix its early light curve.

Claim (observatory centenary brochure draft): "The Linden Observatory's 1923 plates were the first record of any kind of Nova Cygni 1923."
""", 1, 3,
twin=([("on the evening of 2 August 1923", "on the evening of 6 August 1923")], 0)),

# Y21 mean vs peak
Y("Does the monitoring summary support the claim?",
"""
Lake Orrin Monitoring Programme, 30-year summary for the catchment partnership

Surface water temperature is logged hourly at the mid-lake buoy (0.5 m depth). Summer means July and August.
Mean summer surface temperature: 1990: 18.4 °C; 2000: 18.9 °C; 2010: 19.3 °C; 2020: 20.1 °C.
Highest single daily mean: 1990: 21.2 °C; 2020: 23.8 °C (a rise of 2.6 °C).
Ice cover: the lake froze fully in 11 of the 15 winters from 1990 to 2004 and in 2 of the 16 winters from 2005 to 2020.
The buoy was replaced in 2006; overlap readings showed the two sensors agreed to within 0.05 °C.

Claim (catchment partnership leaflet): "Lake Orrin's average summer surface temperature rose by more than 2 °C between 1990 and 2020."
""", 0, 2,
twin=([("2020: 20.1 °C", "2020: 20.7 °C")], 1)),

# Y22 mean vs median with style rule
Y("Is the draft press statement supported by the minutes?",
"""
Fennick Health Board, minutes of the Quality Committee, item 6
Hip-fracture pathway update (presented by the orthogeriatric lead)

The unit has continued to reduce time from admission to surgery. For the quarter to 30 June: 212 patients operated; median time to surgery 33 hours (previous quarter 41 hours); mean time to surgery 38.5 hours, pulled up by weekend admissions waiting for Monday theatre lists; 71% operated within 36 hours (national standard: 85%).
Action: business case for Saturday trauma lists to be brought to the September committee.

Press office style note (applies to all public statements): "average" in a public statement means the arithmetic mean unless the statement explicitly says median.

Draft press statement to be checked: "Fennick's hip-fracture unit has cut its average waiting time for surgery to under 36 hours."
""", 0, 3,
twin=([("mean time to surgery 38.5 hours, pulled up by", "mean time to surgery 34.5 hours, pulled up by")], 1)),

# Y23 absence from complete vs fragmentary rolls
Y("Is the claim refuted by the archivist's reply?",
"""
Harrowfield Borough Archives, research enquiry reply

Dear Mr Castellan,
Thank you for your enquiry about the signatories of the 1791 Harrowfield Charter. The engrossed charter carries fourteen signatures. We have compared each name with the admission rolls of the Merchant Guild of Harrowfield, which survive complete for the years 1760 to 1800 and record every admission, including admissions by patrimony. Thirteen of the signatories appear in the rolls, all admitted before 1791. The fourteenth, Josiah Kemp, described in the charter as "surgeon of this town", does not appear in the rolls at any date. Kemp's name does appear in the vestry minutes as churchwarden in 1789.
Yours sincerely,
M. Oduya, Borough Archivist

Claim (your draft article): "Every signatory of the 1791 Harrowfield Charter was a member of the town's Merchant Guild."
""", 1, 3,
twin=([("which survive complete for the years 1760 to 1800 and record every admission, including admissions by patrimony",
        "which survive only in fragments for the years 1760 to 1800, with many admissions lost")], 0)),

# Y24 suspended dividend
Y("Does the dividend history support the claim?",
"""
Dividend history, Orvane Telecom plc (from the shareholder information page)
Final and interim dividends per ordinary share, by financial year:
2019: 12.0p (interim 4.0p, final 8.0p)
2020: 12.0p (interim 4.0p, final 8.0p)
2021: nil; the Board suspended the interim and final dividends to preserve liquidity during the network-sharing dispute
2022: 8.0p (final only; dividend reinstated)
2023: 10.0p (interim 3.0p, final 7.0p)
A scrip alternative was offered for the 2019 and 2020 final dividends.

Claim (investor forum post): "Orvane Telecom paid a dividend for each financial year from 2019 to 2023."
""", 0, 1),

# Y25 ongoing test at the claimed cycle count
Y("Is there enough evidence to decide the claim either way?",
"""
Press release, Parrin Energy Storage, 14 May
Parrin unveils PX-9 cell for grid storage

Parrin today released test data for its PX-9 lithium iron phosphate cell. In accelerated laboratory cycling at 25 °C (full charge and discharge at 1C), PX-9 cells retained 91% of their initial capacity after 1,000 cycles, compared with 86% for the company's previous PX-7 cell. Cycling of the same test cells to 2,000 cycles is ongoing, and results will be published when complete. Parrin's chief technology officer said the company was "very confident" the cell would comfortably exceed its 6,000-cycle warranty.

Claim (industry newsletter): "Parrin's PX-9 cell retains 90% of its capacity after 2,000 charge cycles."
""", 0, 2,
twin=([("Cycling of the same test cells to 2,000 cycles is ongoing, and results will be published when complete.",
        "Cycling of the same test cells continued to 2,000 cycles, at which point they retained 84% of initial capacity.")], 1)),
]
