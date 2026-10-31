"""Multi-option claim-verification items: mismatch type, paragraph / sentence selection,
candidate-claim selection, evidence-edit selection, and label combinations.
Hand-written by Claude."""
from common import (M, C, DEF_S, DEF_R, DEF_N, sentence_opts, sentence_card, para_opts, para_card,
                    claim_opts, claim_card, combo_opts, combo_card, edit_opts, edit_card)

NOTE1 = "The claim contains at most one discrepancy with the evidence."

PARA_NONE = "no single paragraph, judged on its own, refutes the claim"
SENT_NONE_R = "no single numbered sentence, taken on its own, refutes the claim"
SENT_NONE_S = "no single numbered sentence, taken on its own, establishes the claim"

ITEMS = [
# ---------------- mismatch type (7 options) ----------------
M("Which kind of discrepancy, if any, is there between the claim and the evidence?",
f"""
Wind resource assessment: Harlan Ridge, summary sheet (calendar year 2025)
Met mast: 100 m lattice mast, anemometers at 60 m, 80 m and 100 m; data recovery 97.4%.
Hub height for the proposed turbines: 100 m.
Mean wind speed at 100 m: 7.8 m/s
Mean wind speed at 80 m: 7.4 m/s
Mean wind speed at 60 m: 6.9 m/s
Highest 10-minute mean at 100 m: 28.7 m/s (storm of 18 January)
Prevailing direction: west-south-west
Long-term correction against the Carne reference station has not yet been applied.

Claim (developer's newsletter): "The Harlan Ridge survey recorded a mean wind speed of 8.7 m/s at hub height during 2025."
{NOTE1}
""", "number", 1),

M("What type of error, if any, does the claim contain relative to the board text?",
f"""
Reservoir heritage trail, board 2: "Building the Coldwater Dam"

Work on the Coldwater Dam began in the spring of 1931, when the first navvies' camp was set up at Sheepwash Bottom. At the height of construction in 1933 more than 900 men were employed. The masonry dam was completed in the autumn of 1934 and the reservoir took until the winter of 1935 to fill. The dam was formally opened by the chairman of the water board in May 1936.

Claim (trail leaflet): "The Coldwater Dam was completed in 1934, two years after construction began."
{NOTE1}
""", "date", 2),

M("Which category best describes how the claim departs from the report, if it does?",
f"""
Merrin Bay Council: Bathing Water Report 2025 (extract)

The council monitors 12 designated bathing waters between May and September. Classification is based on four years of samples; "sufficient" is the minimum standard, and "good" and "excellent" are above it.
Results for 2025: Excellent, 7 beaches; Good, 3 beaches; Sufficient, 1 beach; Poor, 1 beach (Harrow Sands, where a storm-overflow investigation is under way). Advice against bathing will be displayed at Harrow Sands throughout the 2026 season.

Claim (tourism website): "Every designated beach in Merrin Bay met the bathing-water standard in 2025."
{NOTE1}
""", "scope", 1),

M("What is wrong with the claim, if anything, compared with the research round-up?",
f"""
Nutrition research round-up: Pellmont University diabetes pilot

The Pellmont team enrolled 42 adults with type 2 diabetes of less than six years' duration in a 24-week pilot of the Tarro diet, a low-energy, plant-rich meal-replacement plan. There was no control group. At 24 weeks, 19 participants (45%) had HbA1c below 48 mmol/mol without diabetes medication, the study's definition of remission. The authors conclude: "These preliminary, uncontrolled results suggest that the Tarro diet may be able to reverse type 2 diabetes in people with recent-onset disease. A randomised trial is needed before any firm conclusion can be drawn."

Claim (diet book cover): "The Pellmont study proved that the Tarro diet reverses type 2 diabetes in people with recent-onset disease."
{NOTE1}
""", "certainty", 1),

M("Which discrepancy type applies to this claim?",
f"""
Brennan General Hospital: infection prevention annual report (extract)

In April 2024 the hospital launched its "Clean Hands, Every Time" programme: new alcohol-rub dispensers at every bed, weekly ward audits and monthly feedback to teams. Hand-hygiene compliance in audits rose from 71% in the year before launch to 89% in the year after. Over the same two periods, the rate of hospital-acquired infections fell from 4.1 to 3.2 per 1,000 bed-days. Staff sickness absence rose slightly, from 4.6% to 4.9%.

Claim (board summary): "Hospital-acquired infections at Brennan General rose in the year after the hand-hygiene programme was launched."
{NOTE1}
""", "polarity", 1),

M("How, if at all, does the claim misstate the evidence?",
f"""
Report cover page and foreword: "State of the Harl Estuary 2024"
Commissioned by: Harl Estuary Partnership (a partnership of three councils, the port authority and two water companies)
Prepared by: Linnet Environmental Consultants
Data contributors: Harl River Trust (volunteer water-quality sampling, 2019 to 2024); Port of Harl (dredging records); national monitoring network.

Foreword by the Partnership chair: "This report, which the Partnership commissioned in January 2024, brings together five years of data. We are grateful to the volunteers of the Harl River Trust, without whom the upstream record would not exist."

Claim (Harl River Trust newsletter): "The 2024 'State of the Harl Estuary' report was commissioned by the Harl River Trust."
{NOTE1}
""", "entity", 2),

M("Which kind of discrepancy, if any, separates the claim from the company's return?",
f"""
Castleby Water Company: return to the Local Board of Health, 1880 (transcribed)

Households in the borough, per the rate books: 2,904.
Households supplied by the Company's mains (house connection): 861.
Households supplied from Company standpipes in courts and yards: 1,188.
Households dependent on wells, pumps or the river: 855.
Remarks of the Company's engineer: "Extension of the main along Tanner's Row and Upper Mill Street will add some 240 house connections during 1881."

Claim (local history talk): "Fewer than a third of Castleby's households had a mains water connection to their house in 1880."
{NOTE1}
""", "no mismatch", 2,
twin=([("(house connection): 861.", "(house connection): 1,061."), ("courts and yards: 1,188.", "courts and yards: 988.")], "number")),

M("What type of error, if any, does the claim contain relative to the records?",
f"""
Kellan Bridge: notes from the county council's property records

1791: Kellan Bridge built by the Kellan Bridge Company under a private Act, with the right to charge tolls until its loan was repaid.
1902: The county council buys the bridge from the Company. Under the sale agreement the council continues to collect tolls until the Company's outstanding bondholders have been paid off.
March 1909: Final bond repaid; tolls cease and the toll house is closed. The toll board is now in the county museum.
1934: Bridge widened.

Claim (museum label draft): "The last tolls on the Kellan Bridge were collected in 1902, the year the county council bought it."
{NOTE1}
""", "date", 2),

# ---------------- paragraph selection ----------------
C("Which evidence paragraph, taken on its own, refutes the claim?",
"""
Claim under review: "The Selby Hall fire of 1911 started in the kitchens."

[1] From the county newspaper, 3 March 1911: "Selby Hall, the seat of the Arden family, was gutted by fire on the night of Tuesday last. The alarm was raised shortly before eleven o'clock by a footman, and by midnight the whole of the east wing was ablaze."
[2] From the report of the chief officer of the Selby fire brigade, 6 March 1911: "The seat of the fire was in the library on the first floor of the east wing, where an oil lamp is believed to have been overturned. The fire spread through the floor voids to the rooms below, including the kitchens, which were destroyed."
[3] From the estate steward's letter book, 1912: "The kitchens and servants' hall were the first part of the house to be rebuilt, the family wishing to be in residence again by Michaelmas."
""", para_opts(3), "Paragraph 2", 2, para_card(3, PARA_NONE, [DEF_R])),

C("Which numbered paragraph, if any, is enough by itself to show the claim is false?",
"""
Claim under review: "Lumora eye drops were withdrawn from sale in 2023."

[1] Regulator's drug safety update, June 2023: "Healthcare professionals are reminded that Lumora (brimatine) eye drops should not be used in patients with a history of corneal ulceration."
[2] Manufacturer's notice, September 2023: "As a precaution we are recalling batch L-22 of Lumora 5 ml eye drops, following a sterility test failure at our contract manufacturer. Other batches are not affected and remain available."
[3] Market report, February 2024: "Pharmacy sales of Lumora fell by 40% in 2023, after a lower-priced generic entered the market in March."
[4] Company annual report 2023: "Lumora revenue: €41m (2022: €68m)."
""", para_opts(4), "none of these", 3, para_card(4, PARA_NONE, [DEF_R])),

C("Which paragraph, judged on its own, refutes the claim?",
"""
Claim under review: "The Hessel Valley line has carried passengers continuously since it opened in 1868."

[1] Company history, 1918: "The Hessel Valley Railway was opened throughout from Tarrant Junction to Hessel Head on 1 August 1868, with four passenger trains each way on weekdays."
[2] Traffic statistics, 1914: "Passenger journeys on the line reached 612,000 in 1913, the highest figure recorded."
[3] Regional railway history, 1978: "From October 1942 until June 1946 the line was requisitioned by the War Department to serve the Hessel Head ordnance depot; the public passenger service was withdrawn for the duration and replaced by buses."
[4] Heritage railway website: "Our steam services run every weekend from Easter to October, using the original 1868 station at Hessel Head."
""", para_opts(4), "Paragraph 3", 1, para_card(4, PARA_NONE, [DEF_R])),

C("Which one of the paragraphs, read alone, contradicts the claim?",
"""
Claim under review: "Aldern Bank has never reported an annual loss."

[1] Business history of the region (2004): "Aldern's only annual loss came in 1991, when write-offs on commercial property lending produced a pre-tax loss of £12 million; the chairman resigned the following spring."
[2] Aldern Bank annual report 2025: "Profit before tax rose for the fifteenth consecutive year, to £214 million."
[3] Aldern Bank investor factsheet: "Aldern has paid a dividend every year since its flotation in 1985."
[4] Credit rating agency note, 2019: "We upgrade Aldern to A-, reflecting its consistent profitability through the cycle."
[5] Financial press, 2009: "Aldern's 2008 profits fell 60% as bad debts rose, but the bank remained in the black."
""", para_opts(5), "Paragraph 1", 1, para_card(5, PARA_NONE, [DEF_R])),

C("Which evidence paragraph, taken on its own, refutes the claim?",
"""
Claim under review: "None of the participants in the SOLACE sleep study was older than 65 at any study visit."

[1] Protocol summary: "SOLACE is a 26-month observational study of sleep patterns in shift workers, with visits at baseline and every six months."
[2] Eligibility: "Adults aged 25 to 64 years at screening, currently working night or rotating shifts."
[3] Baseline characteristics: "Mean age at screening 47.2 years (SD 9.8); 58% women."
[4] Follow-up report: "Because of the length of follow-up, seven participants were aged 66 at their final visit; their data were retained in the analysis."
""", para_opts(4), "Paragraph 4", 2, para_card(4, PARA_NONE, [DEF_R])),

C("Which numbered paragraph, if any, is enough by itself to show the claim is false?",
"""
Claim under review: "The Coralline sea-wall scheme was delivered for less than its original budget."

[1] Council cabinet report, 2019: "Cabinet approves the Coralline sea-wall scheme with a budget of £16.9 million."
[2] Council cabinet report, 2021: "Following storm damage to the temporary works, the scheme budget is revised to £19.2 million."
[3] Project closure report, 2024: "The scheme was completed four months ahead of programme, at a final cost of £18.4 million: £1.5 million over the budget originally approved in 2019, but £0.8 million under the revised budget."
""", para_opts(3), "Paragraph 3", 2, para_card(3, PARA_NONE, [DEF_R])),

# ---------------- sentence selection ----------------
C("Which numbered sentence, on its own, refutes the claim?",
"""
Heritage listing text: Brenholt Point Lighthouse
[S1] The lighthouse stands on the southern tip of Brenholt Point, 2 km from the village.
[S2] It was designed by the engineer James Carrow for the Harbour Commissioners, who obtained the necessary Act in 1849.
[S3] Construction of the granite tower began in April 1850.
[S4] The tower, 31 m high, was structurally complete by the autumn of 1852, and the keepers' cottages were occupied that winter.
[S5] A dispute with the contractor over the lantern and optic, which had to be remade after failing their tests, meant that the light was not first exhibited until 1 October 1854.
[S6] The original oil lamp was replaced by a paraffin burner in 1871, and the light was electrified in 1952.
[S7] It was automated in 1989 and the cottages are now holiday lets.

Claim (village guide): "The Brenholt lighthouse was first lit in 1852."
""", sentence_opts(7), "S5", 2, sentence_card(7, SENT_NONE_R, [DEF_R])),

C("Which single numbered sentence establishes the claim by itself?",
"""
Fisheries board report: Arrowmere Beck trout recovery
[S1] Arrowmere Beck drains a 42 km2 upland catchment into Lake Arrow.
[S2] In June 1990 a spill of acidic mine water from the disused Gillthwaite level killed most fish in the lower 6 km of the beck.
[S3] Electrofishing surveys at the same six sites have been carried out every five years since 1985.
[S4] Adult brown trout densities averaged 1,230 per km in the 1985 survey, the last before the spill.
[S5] The 1995 survey found 85 adult trout per km.
[S6] A limestone dosing plant at the mine entrance has neutralised the discharge since 1998.
[S7] Densities reached 640 per km in 2005 and 1,050 per km in 2015.
[S8] The 2020 survey counted 1,240 adult trout per km, slightly above the density recorded in the last survey before the spill.
[S9] Anglers' catch returns for 2020 were the best since 1988.

Claim (board press release): "By 2020 the adult trout population of Arrowmere Beck had recovered to at least its pre-spill density."
""", sentence_opts(9), "S8", 2, sentence_card(9, SENT_NONE_S, [DEF_S])),

C("Which numbered sentence, if any, refutes the claim?",
"""
Tellwright Group plc: five-year record (narrative extract from the 2025 annual report)
[S1] Revenue fell in 2022, by 4%, as the group exited its low-margin distribution contracts.
[S2] Despite that, net profit rose in 2022 for the second consecutive year, helped by lower interest costs.
[S3] In 2023 operating profit fell by 3% because of a one-off pension charge.
[S4] A lower tax rate meant that net profit nevertheless edged up in 2023, by 1%.
[S5] Net profit growth slowed to 2% in 2024.
[S6] The dividend was held flat in 2024 to fund the Tamworth warehouse.
[S7] Net profit growth in 2025 was 11%, the strongest in the five years.
[S8] Earnings per share rose less than net profit in 2025 because of the share issue in March.
[S9] Net debt rose in 2023 and fell in 2024 and 2025.
[S10] Employee numbers fell from 4,120 in 2021 to 3,860 in 2025.
[S11] Revenue returned to growth in 2024.
[S12] The 2021 net profit was restated in 2022 but remained above the 2020 figure.

Claim (investor newsletter): "Tellwright Group's net profit rose in every year from 2021 to 2025."
""", sentence_opts(12), "none of these", 3, sentence_card(12, SENT_NONE_R, [DEF_R])),

C("Which numbered sentence, on its own, shows the claim to be false?",
"""
Sallow Point Health Centre: patient participation group minutes
[S1] The practice manager reported on the new online and text-message booking system launched on 1 January.
[S2] In the first quarter after launch, 3.1% of booked appointments were missed, down from 7.8% in the same quarter last year.
[S3] Text reminders are now sent 48 hours and 2 hours before each appointment.
[S4] Patients can cancel by replying CANCEL, which releases the slot to the waiting list.
[S5] The group welcomed the improvement and asked for figures on telephone waiting times.
[S6] The manager will report second-quarter figures at the next meeting.

Claim (practice newsletter): "In its first quarter, the new booking system at Sallow Point eliminated missed appointments."
""", sentence_opts(6), "S2", 1, sentence_card(6, SENT_NONE_R, [DEF_R]),
twin=([("3.1% of booked appointments were missed, down from 7.8% in the same quarter last year",
        "none of the booked appointments were missed, compared with 7.8% in the same quarter last year")], "none of these")),

C("Which numbered sentence, on its own, refutes the claim?",
"""
Lowmoor local studies library: notes on early schooling in the town
[S1] The Garnet Street National School opened in 1838 for boys only.
[S2] In 1852 an infants' department and a girls' department were added, and Garnet Street admitted its first girls in October of that year.
[S3] The trustees' minute book records 64 girls on the roll by Christmas 1852.
[S4] The British School on Mill Lane, opened in 1846, remained a boys' school until it closed in 1870.
[S5] Several private academies advertised in the Lowmoor Advertiser in the 1840s, all for "young gentlemen".
[S6] The Wesleyan chapel held Sunday reading classes for boys from 1829.
[S7] The 1851 census lists eleven women in Lowmoor giving their occupation as "schoolmistress".
[S8] The Chapel Lane dame school, a registered day school run by Mrs Hannah Oxley, had taught girls and boys together since 1812.
[S9] The first Board school in Lowmoor opened in 1874 and admitted both sexes.
[S10] Garnet Street became a mixed secondary modern school in 1947.

Claim (school's anniversary booklet): "Garnet Street was the first school in Lowmoor to admit girls."
""", sentence_opts(10), "S8", 2, sentence_card(10, SENT_NONE_R, [DEF_R])),

C("Which single numbered sentence establishes the claim by itself?",
"""
Survey team status page: Pollard Transit Survey, candidate follow-up
[S1] The Pollard survey flagged four transit candidates around nearby red dwarf stars in its first season: P-1, P-2, P-3 and P-4.
[S2] P-1 was ruled out as an eclipsing binary after high-resolution imaging revealed a close stellar companion.
[S3] P-2 shows transits in Pollard photometry from two seasons; radial-velocity follow-up has been requested but not yet scheduled.
[S4] P-4's transit signal was recovered in a second season of Pollard data, which the team regards as strengthening, but not confirming, the candidate.
[S5] The team uses the word "confirmed" only when a second, independent technique detects the planet.
[S6] First-season candidate P-3 was confirmed in March 2025 by radial-velocity measurements from the Calloway spectrograph, an independent technique, which yield a mass of 4.1 Earth masses.
[S7] A paper describing P-3 has been submitted.
[S8] The second-season candidate list will be published in the autumn.

Claim: "At least one of the first-season Pollard candidates has been confirmed by an independent method."
""", sentence_opts(8), "S6", 2, sentence_card(8, SENT_NONE_S, [DEF_S])),

C("Which clause, numbered as a sentence, refutes the claim on its own?",
"""
Merrow Housing Association: assured tenancy agreement, Part 4 (Use of the home), extract
[S1] 4.1 You must use the home as your only or principal home.
[S2] 4.2 You must not use the home for any business without our written consent.
[S3] 4.3 You must not keep or use any paraffin heater or bottled-gas appliance in the home.
[S4] 4.4 You must not make alterations or improvements without our written consent.
[S5] 4.5 Assistance animals may accompany you and your visitors in communal areas.
[S6] 4.6 You are responsible for the behaviour of everyone who lives in or visits the home.
[S7] 4.7 You must not cause nuisance or annoyance to neighbours.
[S8] 4.8 You must keep the home in a clean and reasonable condition.
[S9] 4.9 You must not keep any vehicle that is not taxed and roadworthy on our land.
[S10] 4.10 You must allow us access to inspect the home on 24 hours' notice.
[S11] 4.11 You must obtain our written permission before keeping any dog, cat or other animal at the home, other than fish in a tank of under 50 litres, and we may withdraw permission if the animal causes nuisance.
[S12] 4.12 Permission under 4.11 will not be unreasonably refused.
[S13] 4.13 You must not keep any animal in a flat above the second floor.
[S14] 4.14 Breach of this part may lead us to seek possession of the home.

Claim (tenants' social-media group): "Under the Merrow tenancy agreement, a tenant in a ground-floor flat can keep a dog without asking the association's permission."
""", sentence_opts(14), "S11", 2, sentence_card(14, SENT_NONE_R, [DEF_R])),

C("Which numbered sentence supports the claim on its own?",
"""
Adverse events summary: TALIS trial of oral taloxib in advanced ovarian cancer (212 patients treated)
[S1] The most common adverse events were nausea (48%), fatigue (41%) and anaemia (29%).
[S2] No patient discontinued treatment because of hair loss.
[S3] Grade 3 or higher events occurred in 37% of patients.
[S4] Alopecia (hair loss) was reported in 4 of the 212 patients, all grade 1.
[S5] There were no treatment-related deaths.

Claim (patient information sheet): "Some patients in the TALIS trial experienced hair loss."
""", sentence_opts(5), "S4", 1, sentence_card(5, SENT_NONE_S, [DEF_S])),
]
