"""Candidate-claim selection, evidence-edit selection and label-combination items.
Hand-written by Claude."""
from common import (C, DEF_S, DEF_R, DEF_N, claim_opts, claim_card, combo_opts, combo_card,
                    edit_opts, edit_card)

ITEMS = [
# ---------------- candidate-claim selection ----------------
C("Which one of the candidate claims is fully supported by the press summary?",
"""
Observatory press summary: Varley Deep Field, first data release

The Varley Deep Field covers 1.8 square degrees and was observed for 312 hours between 2023 and 2025 with the Halden 4-m telescope. The first data release contains 1.26 million galaxies, of which 41,000 have spectroscopic redshifts; the rest have photometric redshifts only. The most distant spectroscopically confirmed galaxy in the release, VDF-88213, has a redshift of 6.4. Several photometric candidates at redshift above 7 are listed but have not been confirmed. The data are public from 1 March; a second release, adding near-infrared imaging, is planned for 2027.

Candidate claims:
Claim A: The Varley Deep Field covers 18 square degrees.
Claim B: Most galaxies in the first release have spectroscopic redshifts.
Claim C: The release includes a spectroscopically confirmed galaxy at a redshift above 7.
Claim D: More than a million galaxies are included in the first data release.
Claim E: Near-infrared imaging was part of the first data release.
""", claim_opts(5), "Claim D", 1,
claim_card(5, "none of the candidate claims is fully supported", [DEF_S])),

C("Which of the candidate claims, if any, does the trading statement support?",
"""
Holloway Retail Bank: Q3 trading statement (extract)

Net interest margin 2.84% (Q2: 2.91%). Customer deposits £48.2bn, up £0.9bn in the quarter. Mortgage lending £36.5bn, broadly flat. Impairment charge £61m (Q2: £44m), reflecting higher arrears in unsecured lending. The bank reiterates its full-year guidance for a net interest margin "of around 2.85%". Cost-to-income ratio 51% (Q2: 53%); this ratio is costs as a share of income, so a lower figure is better. A £250m share buyback, announced in July, is 60% complete.

Candidate claims:
Claim A: Holloway's net interest margin rose in Q3.
Claim B: Customer deposits fell during the quarter.
Claim C: The impairment charge fell compared with Q2.
Claim D: The bank raised its full-year margin guidance.
Claim E: The cost-to-income ratio worsened in Q3.
Claim F: The share buyback has been completed.
""", claim_opts(6), "none of these", 2,
claim_card(6, "none of the candidate claims is supported", [DEF_S])),

C("Which candidate claim does the parish history establish?",
"""
Parish history, chapter 5: "The Great Flood of 1771"

On the night of 16 to 17 November 1771 the River Leven rose more than four metres above its normal level after three days of rain. The flood swept away the old bridge at Wick, which had stood since the fourteenth century, and damaged but did not destroy the mill at Holme. Nine people drowned in the parish, seven of them in the cottages at Leven Row. A new stone bridge was completed at Wick in 1775, paid for by a county rate after an appeal to the justices at the Easter sessions of 1772.

Candidate claims:
Claim A: The mill at Holme was destroyed in the 1771 flood.
Claim B: Most of those who drowned in the parish died in the cottages at Leven Row.
Claim C: The new bridge at Wick was completed within two years of the flood.
Claim D: The new bridge at Wick was paid for by private subscription.
""", claim_opts(4), "Claim B", 1,
claim_card(4, "none of the candidate claims is established", [DEF_S])),

C("Which one of the candidate claims does the trial summary refute?",
"""
Clinical trial results summary: MERIDIAN-HF (orvaglif vs placebo in heart failure with reduced ejection fraction)

Participants: 3,812 adults, median age 67, 24% women, median follow-up 22 months.
Primary outcome (cardiovascular death or first hospitalisation for heart failure): 17.1% orvaglif vs 21.4% placebo (hazard ratio 0.78; 95% CI 0.68 to 0.89).
Cardiovascular death alone: 8.9% vs 9.8% (hazard ratio 0.90; 95% CI 0.75 to 1.08; not statistically significant).
All-cause death: 11.2% vs 12.0%.
Serious adverse events: 32% vs 35%. Genital infections: 1.9% vs 0.6%.
Subgroups: the effect on the primary outcome was consistent in patients with and without diabetes.

Candidate claims:
Claim A: Orvaglif reduced the rate of the primary composite outcome.
Claim B: Fewer than a quarter of the participants were women.
Claim C: Orvaglif will be approved for heart failure.
Claim D: Genital infections were more common with orvaglif than with placebo.
Claim E: The trial's participants had a median age above 65.
Claim F: Serious adverse events were more frequent with orvaglif than with placebo.
Claim G: Orvaglif reduces heart failure hospitalisation in children.
""", claim_opts(7), "Claim F", 2,
claim_card(7, "the summary refutes none of the candidate claims", [DEF_R])),

C("Which one of the candidate claims is supported by the release?",
"""
Statistics office release: consumer prices, Republic of Tavira, August

Annual consumer price inflation was 3.4% in August, down from 3.9% in July. It was the lowest rate since March 2022. On the month, prices rose 0.2%. Food inflation fell to 5.1% from 6.6%; energy prices were 2.3% lower than a year earlier. Core inflation, which excludes food and energy, was unchanged at 3.7%. The central bank's target is 2%. Services inflation edged up to 4.8% from 4.7%.

Candidate claims:
Claim A: Prices fell between July and August.
Claim B: Core inflation fell in August.
Claim C: Energy prices in August were lower than twelve months earlier.
Claim D: Inflation reached the central bank's target in August.
Claim E: Food prices fell in the year to August.
Claim F: Services inflation eased in August.
Claim G: August's inflation rate was the lowest ever recorded in Tavira.
Claim H: Headline inflation in August was higher than core inflation.
""", claim_opts(8), "Claim C", 3,
claim_card(8, "none of the candidate claims is supported", [DEF_S])),

C("For which one of the candidate claims is NOT ENOUGH INFO the correct label?",
"""
Field station bulletin: Loch Tarrin osprey monitoring, 2025 season

Two pairs nested at Loch Tarrin in 2025, the first breeding pairs recorded there since 1908. The north-shore pair laid three eggs and fledged two chicks; the island pair laid two eggs, neither of which hatched. Both fledged chicks were fitted with satellite tags in July. By 30 September, one tagged juvenile had reached the coast of West Africa; the other's signal was lost over the Bay of Carrow on 4 September.

Candidate claims:
Claim A: In 2025 ospreys bred at Loch Tarrin for the first time since 1908.
Claim B: The Loch Tarrin pairs fledged a total of four chicks in 2025.
Claim C: The island pair's eggs failed to hatch.
Claim D: Both tagged juveniles reached West Africa by 30 September.
Claim E: The tagged juvenile whose signal was lost over the Bay of Carrow died on migration.
""", claim_opts(5), "Claim E", 2,
claim_card(5, "every candidate claim can be labelled SUPPORTS or REFUTES", [DEF_S, DEF_R, DEF_N])),

# ---------------- evidence-edit selection ----------------
C("Which single edit to the evidence would change the correct label to REFUTES?",
"""
Evidence under review (from an education authority evaluation):
[1] "The attendance pilot ran in all nine participating primary schools during the 2024-25 school year."
[2] "Compared with 2023-24, attendance was higher in all nine schools, with gains ranging from 0.4 to 2.9 percentage points."
[3] "Across the nine schools combined, persistent absence fell from 18.2% to 15.7%."

Claim: "Attendance rose in every one of the nine pilot schools in 2024-25 compared with the previous year."

As written, the evidence supports the claim. The card lists five proposed edits (Edit A to Edit E); each would be made on its own, with the rest of the evidence unchanged.
""", edit_opts(5), "Edit A", 2,
edit_card([
    'in [2], replace "higher in all nine schools" with "higher in eight of the nine schools"',
    'in [2], replace "ranging from 0.4 to 2.9" with "ranging from 0.1 to 2.9"',
    'in [3], replace "fell from 18.2% to 15.7%" with "fell from 18.2% to 17.9%"',
    'in [1], replace "during the 2024-25 school year" with "during the 2024-25 school year and will be repeated in 2025-26"',
    'in [2], replace "attendance was higher" with "attendance appears, on provisional data, to have been higher"',
], "none of the proposed edits would make the correct label REFUTES")),

C("Which one of the proposed edits would turn the correct label into REFUTES?",
"""
Evidence under review (from a regional health bulletin):
[1] "In 2025, 412 cases of Lyme disease were confirmed in the Halvern region, compared with 351 in 2024."
[2] "Most cases were acquired in the Halvern Forest recreation area."
[3] "The region's population was roughly unchanged between the two years."

Claim: "Confirmed Lyme disease cases in the Halvern region rose from 2024 to 2025."

As written, the evidence supports the claim. The card lists five proposed edits (Edit A to Edit E); each would be made on its own, with the rest of the evidence unchanged.
""", edit_opts(5), "none of these", 3,
edit_card([
    'in [1], replace "412 cases of Lyme disease were confirmed" with "412 suspected or confirmed cases of Lyme disease were reported"',
    'in [2], replace "Most cases" with "Almost all cases"',
    'in [3], replace "roughly unchanged" with "about 20% higher in 2025"',
    'in [1], replace "compared with 351 in 2024" with "compared with 351 in 2023"',
    'in [1], replace "were confirmed" with "may have been confirmed, according to preliminary reports,"',
], "none of the proposed edits would make the correct label REFUTES")),

C("Which single edit would make the evidence support the claim?",
"""
Evidence under review (archive catalogue, naval papers):
[1] "Letter from Captain Hugh Selwyn to the Admiralty Board, dated Carne Harbour, 3 June 1781."
[2] "In it Selwyn reports that the frigate Hesper, under his command, captured the privateer Dauntless off the Sallow Banks on 28 May 1781."
[3] "The Board's reply of 19 June 1781 orders the prize to be sold at Carne."

Claim: "The Hesper captured the Dauntless in April 1781."

As written, the evidence refutes the claim. The card lists five proposed edits (Edit A to Edit E); each would be made on its own, with the rest of the evidence unchanged.
""", edit_opts(5), "Edit C", 2,
edit_card([
    'in [1], replace "3 June 1781" with "3 May 1781"',
    'in [2], replace "captured" with "sighted"',
    'in [2], replace "on 28 May 1781" with "on 28 April 1781"',
    'in [3], replace "19 June 1781" with "19 April 1781"',
    'in [2], replace "the frigate Hesper, under his command," with "a frigate of his squadron"',
], "none of the proposed edits would make the evidence support the claim")),

# ---------------- label pairs (9 options) ----------------
C("Which pair of labels is correct for claims C1 and C2?",
"""
Clinical pharmacology note: drug interaction check, Ferrozine tablets

Ferrozine (an oral iron preparation) should be taken at least 2 hours apart from antacids, calcium supplements and tea, all of which reduce iron absorption. In a crossover study in 24 healthy volunteers, taking Ferrozine with a calcium carbonate antacid reduced iron absorption by 44% compared with taking it with water. Taking Ferrozine with orange juice (containing about 70 mg of vitamin C) increased absorption by 18%; the effect of vitamin C tablets was not studied.

Claims:
C1: Taking Ferrozine with a calcium carbonate antacid increased iron absorption in the volunteer study.
C2: Taking Ferrozine with vitamin C tablets increases its absorption.
""", combo_opts(2), "C1 R, C2 N", 2, combo_card(2)),

C("How should claims C1 and C2 be labelled, in that order?",
"""
Economic history seminar notes: the Harrowby Bank crisis of 1866

The Harrowby & County Bank suspended payment on 11 May 1866 after a run triggered by the failure of its agents in the capital. Its notes circulated at a discount of up to 30% during the summer. A rescue by the Tarrant Joint Stock Bank was agreed in September, and depositors were eventually repaid 17s. 6d. in the pound (87.5%) by 1869. The bank's two managing partners were declared bankrupt; neither was prosecuted.

Claims:
C1: Harrowby depositors eventually recovered more than four-fifths of their deposits.
C2: At least one of Harrowby's managing partners was prosecuted after the crisis.
""", combo_opts(2), "C1 S, C2 R", 2, combo_card(2)),

C("Which combination of labels fits claims C1 and C2?",
"""
Environmental monitoring summary: Pellin Reservoir algal blooms

Blue-green algal blooms were recorded at Pellin in 2019, 2021, 2022 and 2024. In each bloom year the reservoir was closed to water sports for between 9 and 41 days. Toxin testing began only in 2022; microcystin was detected in the 2022 and 2024 blooms, above the recreational guideline in 2024 only. No blooms were recorded in 2020 or 2023.

Claims:
C1: The 2021 bloom at Pellin produced microcystin.
C2: Pellin was closed to water sports in every year in which a bloom was recorded.
""", combo_opts(2), "C1 N, C2 S", 2, combo_card(2)),

# ---------------- label triples (27 options) ----------------
C("Which combination of labels is correct for claims C1, C2 and C3, in that order?",
"""
Archaeology unit interim report: Marl Hill Roman villa, season 3

Excavation this season concentrated on the north range. The bath suite was fully exposed: it comprised a cold room, a warm room and a hot room, with the hypocaust of the hot room surviving to a height of 0.6 m. Coins from the demolition layer run up to the reign of an emperor who ruled in the 370s AD, and the excavators conclude that the baths were in use until at least the 370s. A mosaic in the warm room was found in a collapsed and fragmentary state; its central panel was not recovered and its design cannot be reconstructed. Radiocarbon dates are awaited for a burial found cutting the floor of the cold room.

Claims:
C1: The bath suite at Marl Hill had four rooms.
C2: The Marl Hill baths were in use at least into the 370s AD.
C3: The burial in the cold room dates from after the villa was abandoned.
""", combo_opts(3), "C1 R, C2 S, C3 N", 2, combo_card(3)),

C("What are the correct labels for claims C1, C2 and C3?",
"""
Laboratory results memo: Hartwell Foods allergen verification, product line 7 (oat bars)

Samples of batches 7-114 to 7-118 were tested for peanut protein by ELISA (limit of quantification 1 mg/kg). Results: batches 7-114, 7-115 and 7-117, below the limit of quantification; batch 7-116, 3.8 mg/kg; batch 7-118, sample damaged in transit, not tested. Batch 7-116 was produced on the day after the line had run a peanut product, and a cleaning record for that changeover cannot be found. The company's internal action level is 2 mg/kg.

Claims:
C1: Batch 7-118 contained no detectable peanut protein.
C2: Inadequate cleaning caused the peanut protein found in batch 7-116.
C3: All tested batches from line 7 were below the company's action level.
""", combo_opts(3), "C1 N, C2 N, C3 R", 3, combo_card(3)),
]
