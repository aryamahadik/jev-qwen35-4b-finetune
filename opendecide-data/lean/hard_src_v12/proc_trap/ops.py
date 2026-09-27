"""proc_trap / operations: safety, logistics, facilities, contracts, quality,
insurance, export screening (Kettleby Freight, Ardent Cold Chain, Westmark
Property Services, Solvane Manufacturing, Caraway Insurance, Grellan Events)."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ op01
# why: recordable = medical treatment beyond first aid (stitches, prescription meds,
# lost time). Cleaning + adhesive strips + ice = first aid. Ambulance call and "blood
# everywhere" are not criteria. Twin: 4 stitches at urgent care -> recordable.
C("op01", "How must this injury be recorded under the safety procedure?",
"""
Solvane Manufacturing — Injury Recording Procedure (IRP-2)

2.1 An injury is RECORDABLE if it results in any of: medical treatment beyond first aid; days away from work; restricted duties; loss of consciousness.
2.2 First aid includes: cleaning a wound; adhesive strips, butterfly closures or gauze; cold or hot packs; non-prescription medicine at non-prescription strength.
2.3 Medical treatment includes: stitches, staples or surgical glue; prescription medicine; physical therapy.
2.4 Calling an ambulance, the amount of bleeding and the location of treatment do not by themselves make an injury recordable.
2.5 Injuries that are not recordable are entered in the first-aid log.

Incident report IR-6630, Press Line 4, 21 September 2026, 14:10
Employee: Tevita Lolo, press operator
Description (by line lead): "Cut on the forearm from a burr on a blank. Blood everywhere, ambulance called straight away."
Treatment: paramedics cleaned the wound and closed it with butterfly closures; ice pack; Tevita declined hospital transfer
Work status: returned to his normal duties at 15:00 the same shift
""",
[("recordable_injury", "The wound needed medical treatment beyond first aid, which makes it recordable under 2.1."),
 ("first_aid_log", "Every treatment given is first aid under 2.2, and he was back on normal duties."),
 ("recordable_ambulance", "An ambulance was called and there was heavy bleeding, which makes the injury recordable."),
 ("no_record_needed", "He went back to work the same shift, so nothing needs to be recorded.")],
"first_aid_log", 2,
twin=T([("paramedics cleaned the wound and closed it with butterfly closures; ice pack; Tevita declined hospital transfer", "paramedics cleaned the wound; at urgent care it was closed with 4 stitches; ice pack")], "recordable_injury")),

# ------------------------------------------------------------------ op02
# why: discard if > 8.0 C for more than 30 cumulative minutes; quarantine for QA if any
# reading > 15 C. Excursions 12 + 14 = 26 min, max 9.1 -> release. Twin: 12 + 21 = 33 -> discard.
C("op02", "What disposition does the cold-chain SOP give this vaccine shipment?",
"""
Ardent Cold Chain — SOP CC-14: Temperature excursions (2-8 °C products)

14.1 Add up all minutes above 8.0 °C during transit (cumulative, not continuous).
14.2 If any single reading is above 15.0 °C, quarantine the shipment for Quality Assurance, whatever the total.
14.3 Otherwise, if the cumulative time above 8.0 °C is more than 30 minutes, discard the shipment.
14.4 Otherwise, release the shipment to stock and file the logger report.
14.5 Driver comments and alarm counts are recorded but do not change 14.2-14.4.

Shipment ACC-41177 — 40 cartons of influenza vaccine, depot to Merrow Pharmacy Hub
Logger summary:
- Excursion 1: 09:42-09:54, peak 9.1 °C (12 minutes above 8.0 °C)
- Excursion 2: 13:05-13:19, peak 8.6 °C (14 minutes above 8.0 °C)
- All other readings 3.1-7.4 °C
Driver note: "The ALARM went off twice on the way!! I think this load is ruined."
""",
[("release_to_stock", "Cumulative time above 8.0 °C was 26 minutes, not over 30, and no reading exceeded 15.0 °C."),
 ("discard_shipment", "Excursions total more than 30 minutes above 8.0 °C, so 14.3 applies."),
 ("quarantine_for_qa", "The alarm sounded twice, and any alarm sends a shipment to Quality Assurance."),
 ("release_continuous_rule", "Neither excursion alone lasted 30 minutes, which is the only thing the SOP checks.")],
"release_to_stock", 2,
twin=T([("- Excursion 2: 13:05-13:19, peak 8.6 °C (14 minutes above 8.0 °C)", "- Excursion 2: 13:05-13:26, peak 8.6 °C (21 minutes above 8.0 °C)")], "discard_shipment")),

# ------------------------------------------------------------------ op03
# why: termination notice must be received at least 60 days before end date (31 Dec).
# Received 30 Oct -> 62 days -> valid, contract ends. Vendor rep's "too late" is wrong.
# Twin: received 3 Nov -> 58 days -> auto-renews (rep's claim now right).
C("op03", "What is the effect of Kettleby's termination notice under the contract?",
"""
Kettleby Freight — Contract review note: Fleet Telematics Services Agreement with Orbitrack Ltd

Clause 14.1 (Term). The agreement runs to 31 December 2026 and then renews automatically for a further 12 months.
Clause 14.2 (Non-renewal). Either party may prevent renewal by written notice RECEIVED by the other party at least 60 days before the end of the current term.
Clause 14.3 (Notices). Notices are received on the day they are delivered to the address in Schedule 5 during business hours.
Clause 19 (Entire agreement). Statements by account managers do not vary this agreement.

Facts
Notice of non-renewal: sent by courier 28 October 2026; delivered and signed for at Orbitrack's Schedule 5 address on 30 October 2026, 11:20
Orbitrack account manager email (2 November): "Sorry, you're too late — the contract has already rolled over for 2027."
""",
[("contract_ends_31_december", "The notice arrived 62 days before 31 December, meeting the 60-day requirement in 14.2."),
 ("auto_renews_2027", "The notice arrived fewer than 60 days before the end of the term, so 14.1 renews the agreement for 2027."),
 ("renews_per_account_manager", "Orbitrack's account manager has confirmed the rollover in writing, which settles the question."),
 ("ends_from_sending_date", "Notice runs from the day it was sent, 28 October, so the agreement ends on time.")],
"contract_ends_31_december", 3,
twin=T([("sent by courier 28 October 2026; delivered and signed for at Orbitrack's Schedule 5 address on 30 October 2026, 11:20", "sent by courier 28 October 2026; delivered and signed for at Orbitrack's Schedule 5 address on 3 November 2026, 11:20"),
        ("Orbitrack account manager email (2 November)", "Orbitrack account manager email (4 November)")], "auto_renews_2027")),

# ------------------------------------------------------------------ op04
# why: covered: sudden escape of water from pipes; excluded "flood" = water entering from
# outside (rivers, surface water). Cause = burst pipe -> accept under escape of water.
# Intake keyword FLOOD from customer's wording is not the peril. No twin.
C("op04", "How should the claims handler decide this home insurance claim?",
"""
Caraway Insurance — Home Policy HP-7, wording extract

Section 3 (Covered perils) includes: "sudden and accidental escape of water from any fixed water or heating installation".
Section 5 (Exclusions) includes: "flood", meaning water entering the building from outside, such as rivers overflowing, surface water or rising groundwater.
Section 8 (Claims). The handler decides the peril from the loss adjuster's findings. Words used by the policyholder or tags added by the intake system do not determine the peril.

Claim CL-2026-88413
Policyholder form: "My basement flooded overnight — two inches of water, carpets and freezer ruined."
Intake system tag: FLOOD (excluded peril?)
Loss adjuster findings (18 Sep 2026): copper supply pipe to the basement utility sink split at a joint; water meter shows 3,100 litres used overnight; no water entry from outside; no rain recorded in the 48 hours before the loss
""",
[("decline_flood_exclusion", "The policyholder reports a flooded basement and intake tagged the claim FLOOD, which Section 5 excludes."),
 ("accept_escape_of_water", "A split pipe with no outside water is an escape of water under Section 3."),
 ("refer_to_underwriter", "Claims that mention flooding must be referred to underwriting before any decision.")],
"accept_escape_of_water", 1),

# ------------------------------------------------------------------ op05
# why: forklift certification valid 3 years from evaluation. Evaluated 12 Aug 2023 ->
# expired 12 Aug 2026; check 18 Sep 2026 -> expired -> not permitted; experience claims
# irrelevant. Twin: evaluated 12 Nov 2023 -> valid to 12 Nov 2026 -> permitted.
C("op05", "May this worker operate the forklift on today's shift?",
"""
Kettleby Freight — Powered Industrial Truck Rule (PIT-3)

3.1 Only workers with a current operator certification may operate a forklift.
3.2 A certification is current for 3 years from the date of the operator's last practical evaluation.
3.3 An expired certification is renewed by a new practical evaluation; until then the worker may not operate any truck.
3.4 Years of experience, previous employers' licences or a supervisor's endorsement do not replace 3.1-3.3.

Shift check, Dock 2, 18 September 2026, 06:00
Worker: Arnaud Fessler, loader
Last practical evaluation: 12 August 2023 (counterbalance truck)
Supervisor comment: "Arnaud's been driving forklifts for 20 years, he's our safest driver. Put him on the truck."
Next evaluation slot available: 24 September 2026
""",
[("may_operate", "His last evaluation was less than 3 years ago, so his certification is current."),
 ("may_not_operate", "His certification lapsed on 12 August 2026 and has not been renewed."),
 ("operate_supervisor_endorsed", "Twenty years of experience and the supervisor's endorsement allow him to operate today.")],
"may_not_operate", 1,
twin=T([("Last practical evaluation: 12 August 2023", "Last practical evaluation: 12 November 2023")], "may_operate")),

# ------------------------------------------------------------------ op06
# why: export licence needed only if the classification code is in the Control Annex.
# 5A992 not listed (annex has 5A002, 3A001, 6A003) -> ship without licence. Screening
# tool keyword "DUAL-USE" is advisory. No twin.
C("op06", "What does the export procedure require for this shipment?",
"""
Solvane Manufacturing — Export Compliance Procedure (EXP-4)

4.1 Every export line is assigned an export classification code by Trade Compliance.
4.2 An export licence is required only if the line's code appears in the Control Annex below.
4.3 Lines whose code does not appear in the Control Annex ship without a licence, with the code printed on the commercial invoice.
4.4 Keyword alerts from the screening tool (for example "DUAL-USE", "ENCRYPTION") prompt a check of the code, but do not decide 4.2.

Control Annex (excerpt): 3A001, 5A002, 6A003, 9A012

Shipment SH-7720 to a distributor in Norvale
Line 1: Solvane GW-40 industrial gateway with standard TLS encryption — code 5A992, qty 120
Screening tool alert: "DUAL-USE / ENCRYPTION keyword detected — review"
Consignee screening: no matches
Sales note: "Customer needs these by the 30th."
""",
[("ship_without_licence", "Code 5A992 is not in the Control Annex, so 4.3 applies and the code goes on the invoice."),
 ("hold_for_licence", "The gateway uses encryption and the screening tool raised a dual-use alert, so a licence is needed."),
 ("hold_for_licence_5a", "Every code starting with 5A is controlled, so 5A992 needs a licence under 4.2."),
 ("ship_urgent_sales", "The customer's deadline takes priority, so the shipment goes now and compliance is reviewed later.")],
"ship_without_licence", 2),

# ------------------------------------------------------------------ op07
# why: after 19:00 contractors need an escort unless badge carries a CURRENT unescorted
# endorsement. Endorsement valid to 30 Sep 2026; visit 12 Oct -> expired -> escort.
# Guard's familiarity irrelevant. No twin.
C("op07", "How should the night security officer admit this contractor?",
"""
Westmark Property Services — Site Access Rules, Harbourgate Tower

SA-5. Between 19:00 and 07:00, contractors must be escorted by a security officer at all times, unless their badge carries a current "Unescorted" endorsement.
SA-6. An endorsement is current only until the expiry date printed on it.
SA-7. If no officer is free to escort, the contractor waits or returns in daytime hours.
SA-8. Personal knowledge of the contractor by staff does not replace SA-5.

Gate log, 12 October 2026, 20:30
Contractor: Piotr Zawada, lift engineer (Ascendra Lifts), attending a lift fault on floor 14
Badge: contractor badge C-2231, endorsement "Unescorted — valid to 30 Sep 2026"
Officers on duty: 2 (one on patrol, one on the desk)
Desk officer note: "Known him for years, he's always here. Just let him go up."
""",
[("admit_unescorted", "Piotr's badge endorsement allows him to work unescorted, and staff know him well."),
 ("admit_with_escort", "The endorsement expired on 30 September, so SA-5 requires an escort after 19:00."),
 ("refuse_entry", "Contractors may not enter the building after 19:00 under any circumstances.")],
"admit_with_escort", 1),

# ------------------------------------------------------------------ op08
# why: a sesame INGREDIENT must be declared in the ingredients list in bold; "may contain"
# is only for cross-contact. New bun has sesame flour but label only says "may contain"
# -> hold stock and correct the label. No twin.
C("op08", "What should the food safety lead do with this product?",
"""
Grellan Events — Catering Food Safety Rules, section 6 (Allergens)

6.1 Any of the 14 regulated allergens used as an ingredient must be named in the ingredients list and emphasised in bold.
6.2 "May contain" wording is used only for unintended cross-contact. It is never a substitute for 6.1.
6.3 Product whose label breaches 6.1 is held and may not be served until the label is corrected.
6.4 Product with a correct label is released to service.

Check FS-2210 — Festival kitchen, 19 September 2026
Product: brioche burger buns, new supplier Hallon Bakery (first delivery)
Supplier specification sheet: ingredients include wheat flour, egg, butter, sugar, yeast, sesame flour (4%)
Pack label: "Ingredients: wheat flour, egg, butter, sugar, yeast, flour blend. May contain sesame."
Kitchen manager note: "The label mentions sesame, so we're covered. We need these for 600 covers tonight."
""",
[("release_to_service", "The label mentions sesame, so customers are warned and the buns can be served."),
 ("hold_and_correct_label", "Sesame flour is an ingredient, and 6.2 bars a may-contain line from replacing 6.1."),
 ("discard_all_buns", "Mislabelled allergen products must be destroyed.")],
"hold_and_correct_label", 2),

# ------------------------------------------------------------------ op09
# why: disciplinary review only if speed > limit by MORE than 15 mph for 30+ continuous s.
# 68 in 55 = 13 over -> coaching message. Alert wording and prior alerts irrelevant.
# Twin: 71 in 55 = 16 over for 90 s -> review.
C("op09", "What action does the fleet telematics policy require for this event?",
"""
Kettleby Freight — Driver Telematics Policy (DT-2)

DT-2.1 A speeding event goes to a disciplinary review only if the vehicle exceeded the posted limit by more than 15 mph for 30 continuous seconds or longer.
DT-2.2 All other speeding events trigger an automatic coaching message to the driver.
DT-2.3 Earlier coaching messages are kept for trend reports but do not change DT-2.1.
DT-2.4 Severity words in the telematics vendor's alerts are not used by this policy.

Event TEL-90217 — vehicle KF-118, driver Leonie Brandauer
Location: A-road, posted limit 55 mph
Recorded: 68 mph sustained for 90 seconds (overtaking a slow tractor)
Vendor alert title: "SEVERE SPEEDING — HIGH RISK DRIVER"
Driver history: 3 coaching messages in the last 12 months
""",
[("disciplinary_review", "The truck was more than 15 mph over the limit for at least 30 seconds, which DT-2.1 sends to review."),
 ("coaching_message", "She was 13 mph over, under the 15 mph line, so DT-2.2 applies."),
 ("review_repeat_driver", "Three earlier coaching messages show a pattern that calls for review."),
 ("review_vendor_severe", "The vendor graded the event severe and high risk, so it must be reviewed.")],
"coaching_message", 1,
twin=T([("Recorded: 68 mph sustained for 90 seconds", "Recorded: 71 mph sustained for 90 seconds")], "disciplinary_review")),

# ------------------------------------------------------------------ op10
# why: return-to-vendor if damage noted on delivery receipt OR reported within 48 h of
# delivery. Delivered Mon 14 Sep 07:30; found Thu 17 Sep 10:00 = 74.5 h -> write off.
# Lead's view on vendor packaging history is not a criterion. No twin.
C("op10", "How should the warehouse dispose of these damaged cartons?",
"""
Kettleby Freight — Warehouse Receiving Rules (WR-6)

WR-6.1 Goods damaged in transit are returned to the vendor (RTV) for credit if the damage was either noted on the delivery receipt at receiving, or reported to the vendor within 48 hours of the delivery time.
WR-6.2 Damage discovered and reported later is written off to the warehouse damage account.
WR-6.3 A vendor's past record of poor packaging does not change WR-6.1 or WR-6.2.

Case WR-3319
Vendor: Brightloom Textiles
Delivered: Monday 14 September 2026, 07:30; delivery receipt signed "received in good order", no remarks
Damage found: Thursday 17 September 2026, 10:00 — 6 cartons crushed at the base, found when the pallet was broken down
Reported to vendor: Thursday 17 September 2026, 10:20
Warehouse lead note: "Brightloom always ship in flimsy boxes. They should pay for this."
""",
[("return_to_vendor", "The damage was reported to the vendor within 48 hours of delivery, which WR-6.1 accepts."),
 ("write_off", "No remark on the receipt and a report about 75 hours later, so WR-6.2 applies."),
 ("rtv_vendor_history", "Brightloom's record of flimsy packaging makes them responsible for the damage.")],
"write_off", 2),

# ------------------------------------------------------------------ op11
# why: MSA 1.3: an order form overrides the MSA only where it expressly names the MSA clause
# it overrides. Order form says "unlimited for data breaches" without naming 11.2 -> MSA cap
# (12 months' fees) applies. Twin: "Notwithstanding MSA clause 11.2" -> order form prevails.
C("op11", "Which liability position applies to a data breach under this deal?",
"""
Westmark Property Services — Legal review of the Tenant Portal contract with Quillon Software

Master Services Agreement (MSA)
1.3 Precedence. If an Order Form conflicts with this MSA, the MSA prevails, unless the Order Form expressly identifies by number the MSA clause it is intended to override.
11.2 Limitation of liability. Each party's total liability is capped at the fees paid in the 12 months before the claim.

Order Form 3 (signed 2 September 2026)
Special terms: "The Supplier's liability for data breaches is unlimited."

Email from Quillon's lawyer: "The Order Form is the later document, so obviously it wins over the MSA."
""",
[("cap_12_months_fees", "Order Form 3 does not name MSA clause 11.2, so under 1.3 the MSA cap stays in force."),
 ("unlimited_liability", "Order Form 3 expressly names the MSA clause it overrides, so under 1.3 its unlimited term applies."),
 ("unlimited_later_document", "The Order Form was signed later than the MSA, and later documents take precedence."),
 ("no_liability", "Data breaches are excluded from liability altogether under the MSA.")],
"cap_12_months_fees", 3,
twin=T([("Special terms: \"The Supplier's liability", "Special terms: \"Notwithstanding MSA clause 11.2, the Supplier's liability")], "unlimited_liability")),

# ------------------------------------------------------------------ op12
# why: emergency (4 h) includes no heating when outdoor temperature is below 10 C;
# heating loss at 10 C or above is urgent (48 h). Outdoor 14 C -> urgent. Tenant's
# "EMERGENCY" label not used. Twin: outdoor 6 C -> emergency.
C("op12", "Which response category should the maintenance desk assign?",
"""
Westmark Property Services — Repairs Response Categories (residential lettings)

RC-1 Emergency (attend within 4 hours): gas smell; no water supply; sewage backing up; external door that will not lock; no heating when the outdoor temperature is below 10 °C.
RC-2 Urgent (attend within 48 hours): no heating when the outdoor temperature is 10 °C or above; fridge or freezer failure; a single toilet out of use where there is another.
RC-3 Routine (attend within 10 working days): all other repairs.
RC-4 The category is set by the desk from RC-1 to RC-3. Words used by the tenant do not set it. Use the Met Office reading for the property's postcode at the time of the report.

Report RR-66108, 7 October 2026, 18:40
Tenant: Aoife Dunleavy, Flat 3, 22 Pellow Street (has a 4-month-old baby)
Subject: "EMERGENCY!!! NO HEATING"
Detail: "Boiler shows fault F28 and won't fire. Radiators are cold. Hot water also not working."
Water supply: working (cold taps fine)
Outdoor temperature for postcode at 18:40: 14 °C
""",
[("emergency_4_hours", "Heating has failed while the outdoor temperature is below 10 °C, which is listed under RC-1."),
 ("urgent_48_hours", "No heating at 14 °C outside falls under RC-2, and the tenant's wording does not change it."),
 ("emergency_baby", "A household with a young baby and no heating is always treated as an emergency."),
 ("routine_10_days", "A boiler fault code is a routine repair under RC-3.")],
"urgent_48_hours", 2,
twin=T([("Outdoor temperature for postcode at 18:40: 14 °C", "Outdoor temperature for postcode at 18:40: 6 °C")], "emergency_4_hours")),

# ------------------------------------------------------------------ op13
# why: Wh = V x Ah = 14.4 x 6.8 = 97.92 Wh <= 100 -> standard service with lithium mark.
# Customer's "HAZARDOUS" note irrelevant. Twin: 7.8 Ah -> 112.32 Wh > 100 -> DG service.
C("op13", "How should this battery pack be shipped?",
"""
Kettleby Freight — Parcel Acceptance Rules, Lithium-ion batteries (shipped alone)

LB-1. Watt-hour rating (Wh) = nominal voltage (V) × rated capacity (Ah).
LB-2. Batteries rated 100 Wh or less: accepted on the standard parcel service with the lithium battery mark on the box.
LB-3. Batteries rated above 100 Wh and up to 300 Wh: accepted only on the Dangerous Goods service with a completed DG declaration.
LB-4. Above 300 Wh: not accepted.
LB-5. Descriptions written by the sender (such as "hazardous" or "safe") are not used to classify the shipment.

Parcel PK-50318
Contents: one e-bike accessory battery pack, new, in retail box
Label on pack: 14.4 V, 6.8 Ah, Li-ion
Sender's note on the booking: "HAZARDOUS — LITHIUM!! Handle as dangerous goods."
Service booked: standard parcel
""",
[("standard_with_lithium_mark", "At 97.92 Wh the pack is within the 100 Wh limit of LB-2."),
 ("dangerous_goods_service", "The pack is rated above 100 Wh and no more than 300 Wh, so LB-3 requires the DG service."),
 ("dg_sender_declared", "The sender described the parcel as hazardous, so it must go on the Dangerous Goods service."),
 ("refuse_parcel", "Lithium batteries shipped on their own are not accepted.")],
"standard_with_lithium_mark", 3,
twin=T([("Label on pack: 14.4 V, 6.8 Ah, Li-ion", "Label on pack: 14.4 V, 7.8 Ah, Li-ion")], "dangerous_goods_service")),

# ------------------------------------------------------------------ op14
# why: sample 80, Ac 2 / Re 3, counting MAJOR defects only. 2 major -> accept (minor
# logged). Buyer's "5 defects" counts minors. No twin.
C("op14", "What is the lot decision under the sampling plan?",
"""
Solvane Manufacturing — Incoming Inspection Plan IP-9 (AQL 1.0, general level II)

9.1 Lot size 1,201-3,200: inspect a random sample of 80 units.
9.2 Accept the lot if the sample contains 2 or fewer MAJOR defects. Reject if it contains 3 or more.
9.3 Minor defects are recorded on the supplier scorecard. They do not count toward 9.2.
9.4 Definitions: a major defect makes the part unfit for its intended use; a minor defect is cosmetic and does not affect use.

Inspection record IN-2280 — supplier Rennick Castings, lot of 2,400 pump housings
Sample size: 80
Findings: 2 housings with porosity through the sealing face (major); 3 housings with light surface scratches (minor)
Buyer's comment: "Five defects in eighty — that's terrible quality. Reject it."
""",
[("reject_lot", "Five defective housings in the sample exceed the reject number of 3."),
 ("accept_lot", "Two major defects is within the accept number; scratches are minor."),
 ("accept_after_rework", "The two porous housings should be reworked, and the rest of the lot accepted.")],
"accept_lot", 2),

# ------------------------------------------------------------------ op15
# why: security plan required if expected attendance > 500; attendance = tickets +
# guest list, excludes staff and performers. 460 + 30 = 490 -> standard permit.
# Organiser's "535 on site" counts staff. Twin: guest list 50 -> 510 -> security plan.
C("op15", "Which permit route applies to this event?",
"""
Grellan Events — Event Permit Checklist (city events office rules)

EP-2. Events with expected attendance above 500 need an approved crowd security plan before the permit is issued.
EP-3. Events with expected attendance of 500 or fewer are issued the standard permit.
EP-4. Expected attendance = tickets issued + guest list. Staff, volunteers, performers and contractors are not attendees.

Event: "Lantern Walk at Fellbrook Park", Saturday 24 October 2026
Tickets issued: 460 (sold out)
Guest list: 30
Staff and volunteers: 36
Performers: 9
Organiser's note: "We'll have about 535 people on site, so we're a big event and we should be treated like one."
""",
[("standard_permit", "Tickets plus guest list come to 490, not above 500, so EP-3 applies."),
 ("security_plan_required", "Tickets and guest list together come to more than 500, so EP-2 requires a crowd security plan."),
 ("security_plan_535_on_site", "About 535 people will be on site, above 500, so a security plan is needed."),
 ("no_permit_needed", "Ticketed park events under 1,000 people do not need a permit.")],
"standard_permit", 2,
twin=T([("Guest list: 30", "Guest list: 50"),
        ("about 535 people on site", "about 555 people on site")], "security_plan_required")),

# ------------------------------------------------------------------ op16
# why: close a name match as false positive when at least TWO of DOB, nationality, address
# differ from the list entry. DOB and nationality differ -> close. Tool's "HIT" wording not
# a criterion. Twin: nationality same -> only DOB differs -> escalate.
C("op16", "How should the analyst resolve this screening alert?",
"""
Caraway Insurance — Sanctions Screening Procedure (SSP-3)

3.1 The screening tool raises an alert when a customer's name resembles a name on the consolidated list.
3.2 The analyst closes the alert as a false positive if AT LEAST TWO of these differ from the list entry: date of birth; nationality; address country.
3.3 Otherwise the alert is escalated to the Compliance Officer, and the policy is not issued until the Compliance Officer decides.
3.4 The tool's wording ("HIT", "STRONG MATCH") and the match score do not change 3.2 or 3.3.

Alert SC-44019 — "STRONG MATCH (94%) — SANCTIONS HIT"
Customer: Radomir Kestevan, applying for a home policy
Customer data: DOB 3 March 1988; nationality Irish; address country Ireland
List entry: Radomir Kestevan; DOB 17 June 1961; nationality Lorvanian; address country Lorvania
""",
[("close_false_positive", "Date of birth, nationality and address country all differ, meeting the two-of-three test in 3.2."),
 ("escalate_to_compliance", "Fewer than two of the three identifiers differ from the list entry, so 3.3 requires escalation."),
 ("decline_application", "A 94% strong match to a sanctions list entry means the application must be declined."),
 ("close_name_only", "Name matches alone are always closed, because the same names are common.")],
"close_false_positive", 2,
twin=T([("Customer data: DOB 3 March 1988; nationality Irish; address country Ireland", "Customer data: DOB 3 March 1988; nationality Lorvanian; address country Lorvania")], "escalate_to_compliance")),

# ------------------------------------------------------------------ op17
# why: full lockout required on hardwired equipment; exception only for cord-and-plug
# equipment unplugged with the plug under the worker's exclusive control. Conveyor is
# hardwired -> full lockout. Supervisor's "5 minutes" irrelevant. No twin.
C("op17", "What energy-control step must the technician follow?",
"""
Solvane Manufacturing — Energy Control Program (LOTO-1)

L-3. Before servicing any machine where unexpected start-up could cause injury, the technician applies their own lock and tag at every energy-isolation point and verifies zero energy.
L-4. Exception: cord-and-plug equipment may be serviced without a lock if it is unplugged and the plug stays under the exclusive control of the technician doing the work.
L-5. Job length, urgency and supervisor instructions do not create exceptions.

Work order WO-7741, 22 September 2026
Task: clear a jammed carton from transfer conveyor TC-3 (hardwired, 415 V, isolator on panel P-12)
Technician: Hyun-woo Baek
Supervisor instruction on the order: "It's a 5-minute job and the line's down. Just hit the stop button and reach in."
""",
[("full_lockout_tagout", "TC-3 is hardwired, so L-4 cannot apply and L-3 governs."),
 ("unplug_exception", "Once the conveyor is disconnected and its plug is kept in the technician's hand, L-4 allows the jam to be cleared without a lock."),
 ("stop_button_ok", "The supervisor authorised using the stop button for a short job."),
 ("wait_for_maintenance_manager", "Only a maintenance manager may clear jams on conveyors.")],
"full_lockout_tagout", 1),

# ------------------------------------------------------------------ op18
# why: recall covers lots 2231-2248. Returned unit lot 2252 -> not covered -> standard
# warranty route. Customer fear/news story irrelevant. No twin.
C("op18", "How should the returns desk handle this heater?",
"""
Solvane Manufacturing — Product Recall Notice RN-26-04 (internal instructions)

Scope: ThermaLite 2 kW convector heaters, lot numbers 2231 to 2248 inclusive, because of a thermostat fault.
R-1. Units in scope: free replacement with a new unit and free collection.
R-2. Units outside the lot range: not part of the recall. Faults are handled under the normal 2-year warranty (repair or replace after inspection).
R-3. Staff check the lot number printed on the rating plate. Customer descriptions and news reports do not decide scope.

Return RT-10882
Customer: Beatrix Oyelaran
Product: ThermaLite 2 kW convector heater, bought 8 months ago
Rating plate lot number: 2252
Reported fault: "It clicks on and off. I read about the recall in the paper and I'm frightened it will catch fire."
""",
[("recall_replacement", "The customer read about the recall and her heater is a ThermaLite 2 kW, so R-1 applies."),
 ("warranty_inspection", "Lot 2252 is outside 2231-2248, so R-2 sends it through the normal warranty."),
 ("refund_purchase_price", "Heaters with suspected fire risk are refunded in full.")],
"warranty_inspection", 1),

# ------------------------------------------------------------------ op19
# why: director signing limit $150,000; above that needs CFO co-signature. $180,000 ->
# route for CFO co-signature; the director's existing signature alone is insufficient.
# Twin: $140,000 -> director's signature valid.
C("op19", "Is this purchase agreement validly executed?",
"""
Grellan Events — Signing Authority Matrix (board resolution 2025/07)

SM-1. Directors may sign contracts with a total value up to and including $150,000.
SM-2. Contracts above $150,000 require the signature of a director AND the Chief Financial Officer.
SM-3. Total value includes all fees over the full term, excluding sales tax.
SM-4. A contract missing a required signature is routed for the missing signature. It is not sent to the counterparty.

Contract CT-2026-219 — staging and rigging hire, Northgate Arena season
Counterparty: Vantry Stage Systems
Term: 12 months; fees: $15,000 per month; total $180,000 plus sales tax
Signed by: Jonas Aberline, Director of Productions, 15 September 2026
CFO signature: none
Counterparty note: "We have your director's signature, so we'll start delivering next week."
""",
[("validly_executed", "The total value is within the director's $150,000 limit, so his signature alone is enough."),
 ("route_for_cfo_signature", "$180,000 is above the director limit, so SM-2 needs the CFO too and SM-4 routes it."),
 ("valid_monthly_value", "Each monthly fee of $15,000 is far below the director's limit."),
 ("void_contract", "A contract signed beyond a director's limit is void and must be renegotiated.")],
"route_for_cfo_signature", 2,
twin=T([("Term: 12 months; fees: $15,000 per month; total $180,000 plus sales tax", "Term: 12 months; fees: $11,500 per month; total $138,000 plus sales tax")], "validly_executed")),

# ------------------------------------------------------------------ op20
# why: driver may refuse only if an animal is loose in the delivery path at the time;
# a 2024 note about the dog is history. Dog behind a closed gate -> deliver. No twin.
C("op20", "What should the delivery driver do at this address?",
"""
Kettleby Freight — Driver Safety Guide, section 12 (Animals)

12.1 A driver may refuse delivery if an animal is loose in the delivery path at the time of delivery. The driver records "animal hazard" and the parcel returns to the depot.
12.2 If animals are secured (behind a closed gate, fence, door or on a lead), the driver completes the delivery.
12.3 Address notes from earlier deliveries are reminders to check. They do not justify refusal by themselves.

Delivery DV-770142, 17 September 2026, 11:05
Address: 4 Coldharbour Lane
Address note (added March 2024): "AGGRESSIVE DOG — BEWARE"
Driver's observation on arrival: a large dog barking in the back garden behind a closed, latched 6-foot gate; front path and door clear
Recipient: at home, answered the intercom
""",
[("refuse_animal_hazard", "The address carries an aggressive-dog warning, which lets the driver refuse the delivery."),
 ("complete_delivery", "The dog was secured behind a closed gate and the path was clear, so 12.2 requires completing the delivery."),
 ("leave_at_depot_for_collection", "Parcels for addresses with dog warnings are held at the depot for the recipient to collect.")],
"complete_delivery", 1),

# ------------------------------------------------------------------ op21
# why: near miss = no injury AND no damage. Rack upright was bent -> property-damage
# incident report. Worker calls it a near miss. Twin: rack undamaged -> near miss (the
# worker's claim now matches; claim repeated in both, so no leak).
C("op21", "Which report type does the procedure require for this event?",
"""
Kettleby Freight — Event Reporting Procedure (ERP-1)

1.1 Near miss: an unplanned event that caused NO injury AND NO damage to property or equipment. Recorded on a near-miss card.
1.2 Property damage incident: an unplanned event that damaged property or equipment but caused no injury. Recorded on an incident report and the damaged item is tagged out.
1.3 Injury incident: any event that injured a person. Recorded on an incident report with the injury section completed.
1.4 The type is decided from the facts found at the scene, not from how the reporter describes the event.

Event, Aisle 14, 23 September 2026, 03:20
A pallet of tinned tomatoes slid off the forks while being placed on level 3 and fell to the floor.
People nearby: none within 5 metres; no injuries
Scene check by shift manager: rack upright 14-C bent inward about 30 mm at the impact point; floor undamaged; 40 tins dented
Reporter's description: "Just a near miss, nobody hurt, no harm done."
""",
[("near_miss_card", "No one was hurt and nothing was damaged, which is a near miss under 1.1."),
 ("property_damage_incident", "No one was hurt, but a rack upright was bent, which 1.2 covers."),
 ("injury_incident", "A falling pallet is always recorded as an injury incident because of the potential for harm.")],
"property_damage_incident", 2,
twin=T([("rack upright 14-C bent inward about 30 mm at the impact point; floor undamaged; 40 tins dented", "rack upright 14-C checked and undamaged; floor undamaged; pallet and tins intact")], "near_miss_card")),

# ------------------------------------------------------------------ op22
# why: supplier must hold public liability >= $5M valid ON the contract start date.
# Certificate $5M expires 30 Sep; contract starts 1 Oct -> not valid on start -> request
# renewed certificate before start. No twin.
C("op22", "What should procurement do before this supplier starts work?",
"""
Westmark Property Services — Supplier Onboarding Checklist, item 7 (Insurance)

7.1 Contractors working on managed sites must hold public liability insurance of at least $5,000,000.
7.2 The certificate must be valid on the contract start date. A certificate that expires before the start date does not meet 7.1.
7.3 If 7.1 or 7.2 is not met, onboarding is paused and a renewed or upgraded certificate is requested. The supplier may not start until it is received.
7.4 Previous good performance does not waive 7.1-7.3.

Supplier: Pennant Roofing Ltd (used on 11 previous jobs, no issues)
Contract: gutter replacement, Albany Court, start date 1 October 2026
Certificate supplied: public liability $5,000,000, insurer Northwold Mutual, valid 1 October 2025 to 30 September 2026
Site manager note: "Pennant are our best roofers — sign them off, the paperwork's fine."
""",
[("approve_onboarding", "The certificate shows $5,000,000 of cover, which meets 7.1."),
 ("pause_request_renewal", "Cover lapses on 30 September, before the 1 October start, so 7.3 applies."),
 ("approve_track_record", "Eleven problem-free jobs show the supplier is reliable, so onboarding can be approved."),
 ("reject_supplier", "Suppliers whose certificates are about to expire must be removed from the approved list.")],
"pause_request_renewal", 2),
]
