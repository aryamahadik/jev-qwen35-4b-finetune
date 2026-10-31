"""Part E1: mixed phenomena, long passages and large option sets."""
from _h import it, L3, L3CARD, FOLLOW, E, C, U, NONE

FLATS = ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C", "4A", "4B", "4C", "5A", "5B", "5C",
         "6A", "6B", "6C", "7A", "7B", "7C", "8A", "8B", "8C", "9A", "9B", "9C"]
FL_OPTS = [f"flat {f}" for f in FLATS] + [NONE]

SEN15 = [f"sentence {i}" for i in range(1, 16)] + [NONE]

STAFF = ["Abena Owusu", "Bartek Nowak", "Carys Pryce", "Dmitri Volkov", "Efua Mensah", "Finnian Rourke",
         "Gulnara Saidova", "Hector Albarran", "Isolde Brandt", "Jomo Kariuki", "Kalani Akana",
         "Leif Sorensen", "Marisol Vega", "Nuno Pacheco"]
ST_OPTS = STAFF + [NONE]

ITEMS = [

it("E1", "choice",
   "Which flat in Sorrel House must have had its boiler inspected in the October programme?",
   """Sorrel House Residents' Association - Newsletter insert: October boiler safety programme

The managing agent has sent us the following summary of the October programme. Only flats with gas boilers installed before 2015 were inspected in October; flats with newer boilers or with electric heating will be covered in the spring. Of the flats with pre-2015 gas boilers, every flat on the third floor was inspected, because the third-floor flue riser was the one flagged in the fire risk assessment. The agent has not said which of the other pre-2015 flats were reached; some residents were away and a few refused access.

Heating record (from the agent's register; floor = first digit of the flat number):
1A gas 2012 | 1B electric | 1C gas 2019
2A gas 2016 | 2B gas 2010 | 2C electric
3A gas 2018 | 3B electric | 3C gas 2011
4A gas 2013 | 4B gas 2021 | 4C electric
5A electric | 5B gas 2014 | 5C gas 2017
6A gas 2009 | 6B electric | 6C gas 2020
7A gas 2015 | 7B gas 2012 | 7C electric
8A electric | 8B gas 2016 | 8C gas 2008
9A gas 2022 | 9B gas 2011 | 9C electric

If you think the register is wrong for your flat, please tell the association secretary by 15 November.""",
   "flat 3C", opts=FL_OPTS,
   card="\n".join(f"- flat {f}: the flat numbered {f} in Sorrel House" for f in FLATS)
        + "\n- none of these: the insert does not guarantee that any listed flat was inspected",
   diff=2),

it("E2", "choice",
   "Which numbered sentence of the payroll note, taken on its own, guarantees the statement?",
   """Swiftline Couriers - Payroll exceptions note, week 14 (numbered for the review meeting)

(1) Every courier on the Monday rota was paid on time.
(2) No courier on the Tuesday rota was paid early.
(3) If any courier on the Tuesday rota was paid late, the payroll team was told by the depot.
(4) Some courier on the Tuesday rota was paid late.
(5) The payroll team was told by the depot about a problem on Wednesday.
(6) Most couriers on the Tuesday rota drive their own vans.
(7) Every courier on the Tuesday rota who drives a company van was paid by bank transfer.
(8) Not every courier on the Wednesday rota was paid by bank transfer.
(9) At least two couriers on the Tuesday rota were paid on time.
(10) The Tuesday rota had more couriers than the Monday rota.
(11) Nobody on the Thursday rota was paid late.
(12) Every courier who was paid late received an apology email.
(13) Only couriers on the Friday rota were paid in cash.
(14) Couriers on the Tuesday rota might be moved to the Wednesday rota next month.
(15) If every courier on the Tuesday rota had been paid on time, no apology emails would have been needed.

Statement: Not every courier on the Tuesday rota was paid on time.""",
   "sentence 4", opts=SEN15,
   card="\n".join(f"- sentence {i}: the sentence numbered ({i}) in the note" for i in range(1, 16))
        + "\n- none of these: no single numbered sentence guarantees the statement",
   diff=3),

it("E3", "noul",
   "Taking the warranty terms and the service record as accurate, does the statement follow?",
   """ThermaCore Heat Pumps - Limited Warranty (UK), section 2: What is covered

2.1 ThermaCore will repair or replace a defective outdoor unit free of charge.
2.2 A defect is covered only if (a) it is reported to ThermaCore within 24 months of commissioning, and (b) the unit was installed by a ThermaCore-accredited installer.
2.3 Defects caused by frost, flooding, pests or incorrect water treatment are never covered.
2.4 The warranty is extended to 7 years if the unit is serviced every year by an accredited installer; the extension does not change the conditions in 2.2 and 2.3.
2.5 ThermaCore decides whether a defect is covered after inspecting the unit or photographs of it.

Service record - customer: Mrs. Philippa Dunmore, Orchard Barn, Lower Tew
- Unit: ThermaCore Aero 9 kW, serial TC9-448201.
- Installed and commissioned on 2 May 2025 by Greenhollow Energy (ThermaCore-accredited, certificate 3319).
- 6 November 2026: customer reports that the fan motor has seized. Reported to ThermaCore by phone the same day (reference WR-88210), 18 months after commissioning.
- 9 November 2026: Greenhollow engineer visits and photographs the fan housing. Engineer notes: "Ice build-up visible around the fan shroud. Customer says the unit sat in a frost pocket all last week. Photos sent to ThermaCore for assessment."
- ThermaCore decision: pending.

Statement: The fan motor defect on serial TC9-448201 is covered by the ThermaCore warranty.""",
   0, card=FOLLOW, diff=3),

it("E4", "choice",
   "Relative to the fares review, which relation holds for the statement?",
   """Castlebridge Metro - Fares Review Panel, finding on complaint FR-2207

Background. Several passengers complained that they had been charged the peak fare on late-evening trains in the week of 3 March. The panel reviewed the ticketing back-office records for every journey on the Castlebridge-Pendle line that week, including contactless card taps, smartcard taps and paper tickets.

Findings.
(a) The fare engine applies the peak fare to journeys that start before 19:00 on weekdays. A software update on 2 March briefly applied it to journeys starting up to 21:30; this was fixed on 5 March.
(b) No passenger who boarded after 22:00 was charged the peak fare at any point in the week.
(c) Every passenger on the 22:15 from Castlebridge on Wednesday 5 March boarded after 22:00; the train is the first of the late-evening service and starts at Castlebridge.
(d) Some passengers who boarded between 21:00 and 21:30 on 3 and 4 March were overcharged and will be refunded automatically.

Recommendation. Refund the passengers identified under (d) and publish an apology on the Metro website.

Statement: No passenger on the 22:15 from Castlebridge on Wednesday 5 March who used a contactless card was charged the peak fare.""",
   E, opts=L3[3], card=L3CARD, diff=3),

it("E5", "choice",
   "Given only the survey summary, the statement is which of these?",
   """Ecology Team - River Dunmore invertebrate survey: interim summary for the catchment partnership

Samples. In September we collected 214 kick samples across the catchment. Most of the samples came from the north site (upper Dunmore, above the Kellan confluence), because the south site was in flood for a week and could only be sampled on four days.

Results so far. The lab has now screened every sample for the invasive New Zealand mud snail. Most of the north-site samples tested positive. The south-site results show a more patchy picture, with positives concentrated below the Kellan outfall.

Next steps. We will map the positive samples against the outfall locations and present the full results at the November partnership meeting. Please do not quote these interim figures publicly.

Report by: Dr. Ifeoma Chukwu, catchment ecologist

Statement: Most of the 214 samples tested positive for the New Zealand mud snail.""",
   U, opts=L3[4], card=L3CARD, diff=3),

it("E6", "choice",
   "Taking the tender evaluation note as accurate, how should the statement be labelled?",
   """Harlington Borough Council - Tender evaluation note, contract HB-2026-31 (library refurbishment)

Five bids were received by the deadline: Ashdown Interiors, Corbin & Sons, Pelham Build, Quarry Lane Projects and Westmoor Fit-Out.

Compliance. A bid is compliant only if it is priced below the 2 million pound budget ceiling and includes a signed social value statement. Exactly three of the five bids were compliant. Every compliant bid was below 2 million pounds, as the rules require.

Price. Both the Corbin & Sons and the Ashdown Interiors bids were above 2 million pounds. The remaining bids ranged from 1.62 to 1.94 million pounds.

Quality. Quality scores for the compliant bids will be moderated at the panel meeting on 12 May, and the preferred bidder will be recommended to Cabinet in June.

Author: procurement officer, J. Oduya

Statement: The Pelham Build bid was non-compliant.""",
   C, opts=L3[5], card=L3CARD, diff=2),

it("E7", "noul",
   "Does the statement follow from the regulator's letter?",
   """Office of Industrial Safety Standards - Letter to Dunlin Chemicals Ltd

Dear Mr. Achterberg,

Review of independent safety reports, Dunlin plant (Grangemouth Road)

As part of our periodic review, we have read the two independent reports you commissioned last year: the Ferris Associates process-safety report (March) and the Hale Engineering integrity report (September). For the purposes of this letter, a "safety incident" means any fire, explosion, loss of containment, or injury requiring first aid or more.

Neither the Ferris nor the Hale report mentions any safety incident at the Dunlin plant during the period each covers. Both reports make recommendations about inspection intervals for the pressure relief system, which we expect to see reflected in your maintenance plan by 31 January.

We will write separately about your notification of the pipe-bridge corrosion.

Yours sincerely,
Dr. Margit Ellwood, Principal Inspector

Statement: The Hale report does not mention a fire at the Dunlin plant during the period it covers.""",
   1, card=FOLLOW, diff=2),

it("E8", "noul",
   "Is the statement guaranteed by the customs broker's email?",
   """From: Priyanka Raman, Customs Broker, Eastgate Clearance Services
To: Logistics team, Marlowe Instruments
Subject: Shipment MI-2290 held at Felixstowe

Hi team,

A quick explanation of the hold. Under our standing arrangement with the port, a shipment is released unless the freight invoice for that shipment is unpaid or the importer's controlled-goods licence has expired. Shipment MI-2290 (spectrometer parts, 3 cases) was not released this morning.

I haven't been able to see which of the two is the problem: the port system just shows "HOLD - ADMIN". Your accounts team says they paid a batch of freight invoices yesterday, but I don't know whether MI-2290's was in that batch, and I don't have a copy of your current licence.

Could you send me the remittance advice and the licence certificate? As soon as I have both, I'll ask the port to re-check.

Best,
Priyanka

Statement: The freight invoice for shipment MI-2290 is unpaid.""",
   0, card=FOLLOW, diff=2),

it("E9", "choice",
   "Which of these staff members must have attended the manual-handling refresher?",
   """Brookhill Distribution - Training record extract: manual-handling refresher, June

Summary from the training coordinator: every warehouse operative who drives a forklift attended the refresher. No office-based staff attended. HGV drivers and contract cleaners had a separate session in May, and the coordinator has not listed who from those groups also came in June.

Staff list (role; forklift licence holder?):
- Abena Owusu - office administrator; no
- Bartek Nowak - warehouse operative; not recorded
- Carys Pryce - HGV driver; yes
- Dmitri Volkov - warehouse operative; no
- Efua Mensah - office administrator; yes (from a previous job)
- Finnian Rourke - contract cleaner; no
- Gulnara Saidova - warehouse operative; yes
- Hector Albarran - HGV driver; no
- Isolde Brandt - payroll clerk (office-based); no
- Jomo Kariuki - warehouse operative; licence expired in 2024, does not drive
- Kalani Akana - contract cleaner; yes
- Leif Sorensen - transport planner (office-based); yes
- Marisol Vega - warehouse operative; no
- Nuno Pacheco - HGV driver; yes

Note: holding a licence and driving a forklift at Brookhill are treated as the same thing for warehouse staff, except where the list says otherwise.""",
   "Gulnara Saidova", opts=ST_OPTS,
   card="- Abena Owusu: an office administrator\n- Bartek Nowak: a warehouse operative with no licence record\n"
        "- Carys Pryce: an HGV driver with a licence\n- Dmitri Volkov: a warehouse operative without a licence\n"
        "- Efua Mensah: an office administrator with a licence\n- Finnian Rourke: a contract cleaner without a licence\n"
        "- Gulnara Saidova: a warehouse operative listed as a licence holder\n- Hector Albarran: an HGV driver without a licence\n"
        "- Isolde Brandt: a payroll clerk\n- Jomo Kariuki: a warehouse operative whose licence expired\n"
        "- Kalani Akana: a contract cleaner with a licence\n- Leif Sorensen: a transport planner with a licence\n"
        "- Marisol Vega: a warehouse operative without a licence\n- Nuno Pacheco: an HGV driver with a licence\n"
        "- none of these: the record does not guarantee that any listed staff member attended",
   diff=2),

it("E10", "choice",
   "Given only the trustees' minutes, what is the status of the statement?",
   """Wrenfield Almshouse Charity - Minutes of the trustees' meeting, 4 June (extract)

Present: all six trustees (chair: Mrs. Gwendolyn Pask).

Item 3: Proposal to sell the Mill Cottage site. The clerk reminded trustees that a sale of charity land requires the approval of a majority of the trustees present, and that trustees with a conflict of interest must declare it. No conflicts were declared.

After a long discussion about the cost of repairs, the proposal was put to a vote. Only two of the six trustees did not vote in favour. The chair asked for the minutes to record that the decision was a difficult one and that the trustees would look for a site for replacement homes within five years.

Item 4: Annual accounts. Approved unanimously.

Statement: At least three trustees voted against the proposal to sell the Mill Cottage site.""",
   C, opts=L3[0], card=L3CARD, diff=2),

it("E11", "noul",
   "Based only on the regulator's statement, must the statement be true?",
   """Financial Conduct Office - Statement on the Harrow Oak Property Income Fund

The Office has today written to the authorised fund manager of the Harrow Oak Property Income Fund, Kestrel Wealth Management Ltd, about the fund's valuation practices.

The Office is concerned that the fund's property valuations are stale. The fund's annual report shows that eleven of its fourteen properties were last valued by an external valuer more than 18 months ago, during a period in which commercial property prices in the fund's markets fell. The Office has asked the manager to explain, by 30 September, how it has satisfied itself that the fund's published prices are fair to investors who are buying and selling units.

The Office has not reached any conclusion about whether rules have been broken. Investors do not need to take any action at this stage.

Statement: The Harrow Oak Property Income Fund's property valuations are stale.""",
   0, card=FOLLOW, diff=2),

it("E12", "choice",
   "According to the maintenance summary, how many of the three pumps at station 4 failed on Saturday?",
   """Aldwater Utilities - Pumping station 4 (Marsh End), weekend maintenance summary

Background: station 4 has three duty pumps, A, B and C. The telemetry outstation lost power at 01:10 on Saturday, so pump status was not recorded for most of the day. The findings below come from the site visit on Sunday and from the pump controllers' own fault memories.

Findings:
- At least one of the three pumps failed on Saturday; the wet well level alarm on Sunday morning proves this.
- Pumps A and B share a starter panel. If pump A failed on Saturday, pump B failed too, because a fault on A trips the shared panel.
- Pump B did not fail on Saturday; its controller memory shows continuous running from 00:00 to 23:59.
- Pump C's controller memory was wiped when the outstation lost power.

Actions: replace the outstation battery; review whether A and B should have separate starter panels.""",
   "exactly one",
   opts=["none", "exactly one", "exactly two", "all three", "the passage does not settle this"],
   card="- none: no pump at station 4 failed on Saturday\n"
        "- exactly one: one pump failed on Saturday and the other two did not\n"
        "- exactly two: two pumps failed on Saturday and one did not\n"
        "- all three: pumps A, B and C all failed on Saturday\n"
        "- the passage does not settle this: more than one of the other answers is consistent with the summary",
   diff=3, twin=[("- Pump B did not fail on Saturday; its controller memory shows continuous running from 00:00 to 23:59.\n- Pump C's controller memory was wiped when the outstation lost power.",
                  "- Pump C did not fail on Saturday; its controller memory shows continuous running from 00:00 to 23:59.\n- Pump B's controller memory was wiped when the outstation lost power.")],
   twin_gold="the passage does not settle this"),

it("E13", "noul",
   "Would a reader who accepts the release notes be forced to accept the statement?",
   """Fernpoint Banking app - Release notes, version 8.0

What's new
- Faster sign-up. Since the upgrade to version 8.0, the app no longer asks new users for their date of birth at any point during sign-up. We now confirm age using the identity document you scan, so you have one less screen to fill in.
- Dark mode now follows your phone's system setting.
- Round-up savings can be paused for up to three months.

Fixes
- Fixed a bug where some push notifications arrived twice.
- Fixed the balance widget not refreshing on some tablets.

Known issues
- On some older phones the document scanner may take up to 20 seconds to focus. We're working on it.

Version 8.0 requires iOS 16 or Android 11 or later.

Statement: Before version 8.0, the app asked new users for their date of birth at some point during sign-up.""",
   1, card=FOLLOW, diff=2),

]
