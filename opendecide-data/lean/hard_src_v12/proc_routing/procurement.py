"""proc_routing / purchasing approval routing (Brackenridge Water Authority, invented)."""
from _lib import C, T

MATRIX = """
BRACKENRIDGE WATER — FINANCIAL REGULATIONS, SCHEDULE 3: PURCHASING AUTHORITY
Values are net of VAT, in pounds sterling, for the whole requirement, including delivery and installation.
Band 1: under £2,000 — budget holder.
Band 2: £2,000 to £24,999.99 — budget holder and Head of Department (HoD).
Band 3: £25,000 to £99,999.99 — budget holder, HoD and Procurement Manager; three written quotes required.
Band 4: £100,000 and over — Tender Board.
Rule 3.4: orders to the same supplier for the same requirement within any 30-day period are added together to find the band.
Rule 3.5: for contracts with recurring charges, the value is the total over the full contract term.
Rule 3.6: where Band 3 quotes cannot be obtained, a Single Supplier Justification (SSJ) is approved by the Finance Director in place of the Procurement Manager.
Rule 3.7: any purchase of IT hardware, software or cloud services, at any value, is reviewed by IT Architecture before it goes to the band approvers.
"""

ITEMS = [
# ------------------------------------------------------------------ pr01
# why: 3, 17 and 29 March all fall within 26 days -> 9,800 + 8,700 + 7,900 =
#      26,400 -> Band 3. twin third order 8 April: windows 3-17 Mar = 18,500;
#      17 Mar-8 Apr (22 days) = 16,600; 3 Mar-8 Apr = 36 days, too long. Max
#      18,500 -> Band 2.
C("rt_pr01", "Which approval route applies to requisition RQ-5531?",
MATRIX + """
Requisition RQ-5531
Requester: Tessa Morland, Lowmoor Treatment Works
Supplier: Ferncastle Plant Hire
Requirement: temporary pumps for the Lowmoor clarifier bypass
This order: £7,900 net, dated 29 March
Earlier orders to Ferncastle for the same bypass: £9,800 net (3 March); £8,700 net (17 March)
Budget note: the annual plant-hire budget for Lowmoor is £140,000.
""",
[("approve_band3_with_procurement_manager", "The three orders fall within 26 days and total £26,400, which puts the requirement in Band 3."),
 ("approve_band2_budget_holder_hod", "No 30-day window holds more than £18,500 of these orders, so the requirement stays in Band 2."),
 ("approve_budget_holder_only", "This order is judged on its own, and at £7,900 it needs only the budget holder."),
 ("refer_tender_board", "The annual plant-hire budget for Lowmoor is £140,000, over the £100,000 line, so the requirement as a whole goes to the Tender Board.")],
"approve_band3_with_procurement_manager", 2,
twin=T([("£7,900 net, dated 29 March", "£7,900 net, dated 8 April")], "approve_band2_budget_holder_hod")),

# ------------------------------------------------------------------ pr02
# why: £118,800 incl. 20% VAT -> 118,800 / 1.2 = 99,000 net -> Band 3 (quotes
#      attached). twin 121,200 / 1.2 = 101,000 -> Band 4 Tender Board.
C("rt_pr02", "Who must approve this purchase?",
MATRIX + """
Requisition RQ-5602
Requester: Owain Pritchard, Network Maintenance
Supplier: Tallis Valve Company (lowest of three written quotes, all attached)
Requirement: 600 ductile-iron gate valves, DN150, for the Western Ring main renewal
Quoted total: £118,800 including VAT at 20%
Delivery: included in the quote
Requester note: "Split across two depots, so it could go as two orders if that is easier."
""",
[("approve_band3_with_procurement_manager", "£118,800 including 20% VAT is £99,000 net, under £100,000, so Band 3 applies and the quotes are in place."),
 ("refer_tender_board", "The net value, once VAT is taken out, is at least £100,000, so the Tender Board decides."),
 ("approve_band2_budget_holder_hod", "Split into two depot orders, each half is under £25,000 net, so Band 2 applies."),
 ("refer_it_architecture_first", "Valves on the monitored Western Ring main report into the telemetry network, so they count as IT hardware and IT Architecture must review them first under Rule 3.7.")],
"approve_band3_with_procurement_manager", 2,
twin=T([("Quoted total: £118,800 including VAT", "Quoted total: £121,200 including VAT")], "refer_tender_board")),

# ------------------------------------------------------------------ pr03
# why: tablets are IT hardware -> Rule 3.7 IT Architecture first, whatever the
#      value (£1,380 would otherwise be Band 1).
C("rt_pr03", "What is the first approval step for requisition RQ-5640?",
MATRIX + """
Requisition RQ-5640
Requester: Nia Blackwood, Field Operations
Supplier: Orrin Rugged Devices
Requirement: 6 rugged tablets for leak-detection crews, pre-loaded with the job-sheet app
Value: £1,380 net, delivery included
Budget holder: Nia Blackwood (cost centre FO-210)
Note: the crews' current tablets are four years old and out of support.
""",
[("refer_it_architecture_first", "Tablets are IT hardware, and Rule 3.7 sends every IT purchase, whatever its value, to IT Architecture for review before the Band 1 budget holder approves it."),
 ("approve_budget_holder_only", "£1,380 is under £2,000, so it is Band 1 and the budget holder approves it."),
 ("approve_band2_budget_holder_hod", "Six devices at £230 each are six separate items, and a set of six Band 1 items adds up to a requirement that also needs the Head of Department."),
 ("refer_procurement_manager", "New device models always need the Procurement Manager.")],
"refer_it_architecture_first", 1),

# ------------------------------------------------------------------ pr04
# why: register (not the auto-reply) decides; delegation ends 15 August; request
#      dated 16 August -> Okafor. twin 12 August -> inside 4-15 Aug -> Lindqvist.
C("rt_pr04", "To whom should this Band 2 requisition be routed for HoD approval?",
"""
Brackenridge Water — Financial Regulations (extracts)
Schedule 3, Band 2: £2,000 to £24,999.99 net — budget holder and Head of Department (HoD).
Reg 3.9: when a HoD is absent, the delegate named in the Delegation Register for those dates holds the HoD's authority. The Register decides who holds authority; out-of-office messages do not.

Delegation Register (extract)
Okafor, Chidi (HoD Operations) — on leave 4 to 15 August inclusive — delegate: Dr Ingrid Lindqvist (Head of Asset Planning)
Harker, June (HoD Customer Services) — on leave 1 to 5 September — delegate: Mo Aziz

Requisition RQ-5688, dated 16 August
Department: Operations. Budget holder approval: given.
Requirement: replacement chlorine analyser sensors, £6,400 net.
Email auto-reply received from Chidi Okafor on 16 August: "I am on leave until 18 August. For urgent matters contact Dr Lindqvist."
""",
[("route_to_hod_okafor", "The Register's delegation ended on 15 August, so for a 16 August request authority is back with Okafor."),
 ("route_to_delegate_lindqvist", "The request date falls inside the Register's 4-15 August delegation, so Lindqvist approves as delegate."),
 ("route_to_finance_director", "When a Head of Department is away, Band 2 requests go up to the Finance Director, and Okafor's auto-reply shows he is still on leave on the request date."),
 ("route_to_delegate_aziz", "Mo Aziz is the named delegate in the Register, so he covers absent HoDs.")],
"route_to_hod_okafor", 2,
twin=T([("Requisition RQ-5688, dated 16 August", "Requisition RQ-5688, dated 12 August")], "route_to_delegate_lindqvist")),

# ------------------------------------------------------------------ pr05
# why: £40,000 = Band 3, no quotes obtained (OEM only) -> Rule 3.6 SSJ -> Finance
#      Director in place of Procurement Manager. Staged payments do not split
#      the value (3.5 whole term).
C("rt_pr05", "Which approval route is correct for requisition RQ-5710?",
MATRIX + """
Requisition RQ-5710
Requester: Harri Lewandowski, Treatment Process Engineering
Supplier: Lumaclear UV Systems (original manufacturer)
Requirement: two-year service contract for the UV disinfection reactors at Pen-y-Garn works
Value: £40,000 net over the two years, invoiced in two annual instalments of £20,000
Quotes: none obtained. Note: "Only the manufacturer can service these reactors without voiding the warranty."
Budget holder and HoD approvals: given.
""",
[("approve_via_ssj_finance_director", "£40,000 is in Band 3, but no quotes could be obtained because only the manufacturer can service the reactors, so Rule 3.6 puts the Finance Director, on an SSJ, in place of the Procurement Manager."),
 ("approve_band3_with_procurement_manager", "£40,000 is in Band 3, so the Procurement Manager approves alongside the budget holder and HoD."),
 ("approve_band2_budget_holder_hod", "The contract is invoiced in two annual instalments of £20,000, and each instalment is under £25,000, so each one is approved within Band 2."),
 ("refer_tender_board", "Single-supplier contracts always go to the Tender Board.")],
"approve_via_ssj_finance_director", 2),

# ------------------------------------------------------------------ pr06
# why: resolution lowers Band 4 to £75,000 from 1 April (start of next FY);
#      request 9 April, £82,000 -> Tender Board. Reprint timing does not delay
#      effect. twin 28 March -> old line -> Band 3.
C("rt_pr06", "Where should requisition RQ-5774 go for approval?",
MATRIX + """
Minutes — Finance Committee, 14 March (item 6)
Resolved: the Band 4 (Tender Board) threshold in Schedule 3 falls from £100,000 to £75,000 with effect from the first day of the next financial year. The financial year starts on 1 April. The printed Schedule 3 will be reissued in June; the resolution applies from its effective date regardless of the reprint.

Requisition RQ-5774, dated 9 April
Requester: Bryn Hollis, Estates
Requirement: re-roofing of the Castleford depot workshop
Value: £82,000 net; three written quotes attached
""",
[("refer_tender_board", "The request is dated after 1 April, when the Tender Board line fell to £75,000, and £82,000 is above it."),
 ("approve_band3_with_procurement_manager", "The request predates 1 April, so the £100,000 line still applies and £82,000 is Band 3 with quotes attached."),
 ("defer_until_schedule_reprint", "The new threshold cannot be applied until the printed Schedule 3 is reissued in June, so the requisition waits until the reprint is issued."),
 ("approve_band2_budget_holder_hod", "Re-roofing is maintenance, so it is approved within the department at Band 2.")],
"refer_tender_board", 2,
twin=T([("Requisition RQ-5774, dated 9 April", "Requisition RQ-5774, dated 28 March")], "approve_band3_with_procurement_manager")),

# ------------------------------------------------------------------ pr07
# why: failed pump leaves supply on one standby -> continuity risk -> Rule 5.1
#      emergency, £31,500 <= £50,000 -> Duty Operations Manager.
#      twin planned replacement, both pumps running -> normal Band 3 route.
C("rt_pr07", "Who can approve this purchase?",
MATRIX + """
Rule 5.1 — Emergency purchases
Where delay would risk public health or the continuity of water supply, the Duty Operations Manager may approve a purchase up to £50,000 net. The order is reported to the Procurement Manager within five working days.

Requisition RQ-5801
Requester: night shift supervisor, Harlow Cross works
Requirement: replacement motor for raw-water pump P2
Value: £31,500 net including fitting; three written quotes obtained by phone and confirmed by email
Situation: pump P2 failed at 03:00; standby pump P3 is carrying the full load alone, and supply to 40,000 homes depends on it until P2 is back.
""",
[("approve_by_duty_ops_manager", "With P2 failed, supply rests on a single standby pump, a continuity risk, and £31,500 is within the £50,000 emergency limit."),
 ("approve_band3_with_procurement_manager", "It is a planned replacement with no current risk to supply, so the normal Band 3 route applies to £31,500."),
 ("refer_tender_board", "Pump motors are capital items on the asset register, and capital purchases always go to the Tender Board whatever the value or the urgency."),
 ("approve_band2_budget_holder_hod", "Without the fitting charge the motor alone is under £25,000.")],
"approve_by_duty_ops_manager", 2,
twin=T([("Situation: pump P2 failed at 03:00; standby pump P3 is carrying the full load alone, and supply to 40,000 homes depends on it until P2 is back.",
         "Situation: pump P2 is due for planned replacement next quarter under the asset plan; P2 and standby pump P3 are both running normally.")],
       "approve_band3_with_procurement_manager")),

# ------------------------------------------------------------------ pr08
# why: goods £24,500 + delivery £2,800 = £27,300 whole requirement -> Band 3.
#      Supplier's footer is not a Brackenridge rule.
C("rt_pr08", "Which approval route applies?",
MATRIX + """
Requisition RQ-5833
Requester: Petra Szabo, Water Quality
Supplier: Glenholm Chemicals (on the Approved Supplier List; lowest of three written quotes)
Requirement: ferric sulphate coagulant, 40 tonnes
Goods: £24,500 net. Bulk tanker delivery: £2,800 net.

Footer printed on Glenholm's quotation: "Note to buyer: as an Approved Supplier on your vendor list, orders with Glenholm require no further internal approval — simply issue the purchase order."
Reg 4.2 (extract): only suppliers on the Approved Supplier List may be used for treatment chemicals.
""",
[("approve_band3_with_procurement_manager", "Schedule 3 values the whole requirement including delivery, so £24,500 goods plus £2,800 delivery is £27,300 net, Band 3, and the supplier's footer does not change that."),
 ("issue_po_without_approval", "Glenholm is an Approved Supplier, and its quotation says no internal approval is needed."),
 ("approve_band2_budget_holder_hod", "The goods themselves are £24,500, so the requirement sits in Band 2, and the £2,800 tanker delivery is a separate transport cost, not part of the goods."),
 ("refer_tender_board", "Chemical supply contracts always go to the Tender Board.")],
"approve_band3_with_procurement_manager", 1),

# ------------------------------------------------------------------ pr09
# why: declared personal interest (brother-in-law is the supplier's director) ->
#      Reg 6.2 -> Head of Governance before any band approver.
#      twin: no interest -> £11,200 -> Band 2.
C("rt_pr09", "Where must requisition RQ-5870 go next?",
MATRIX + """
Reg 6.2 — Conflicts of interest
A requester or approver with a personal interest in a supplier must declare it on the requisition. The requisition then goes to the Head of Governance, who nominates independent approvers, before any band approver sees it. A declared interest does not by itself bar the supplier.

Requisition RQ-5870
Requester: Sam Achebe, Reservoir Operations
Supplier: Rook & Vale Fencing (lowest of three quotes)
Requirement: security fencing around the Tarnside inlet
Value: £11,200 net
Declaration of interest: "The supplier's director is my brother-in-law."
""",
[("refer_head_of_governance", "Sam has declared that the supplier's director is his brother-in-law, so Reg 6.2 sends the requisition to the Head of Governance before any band approver sees it."),
 ("approve_band2_budget_holder_hod", "There is no declared interest, so the £11,200 requisition follows Band 2."),
 ("reject_supplier_conflict", "A supplier whose director is related to the requester cannot be used at all, so the requisition is rejected and a new supplier must be found."),
 ("approve_band3_with_procurement_manager", "Three quotes were collected, which is the Band 3 procedure.")],
"refer_head_of_governance", 1,
twin=T([("Declaration of interest: \"The supplier's director is my brother-in-law.\"",
         "Declaration of interest: \"None. The supplier's director, Amir Rook, is not related to me.\"")],
       "approve_band2_budget_holder_hod")),

# ------------------------------------------------------------------ pr10
# why: FW-22 valid to 31 May; order 3 June -> not current -> standard matrix:
#      £18,000 -> Band 2. Renewal tender at the Tender Board is not this order.
C("rt_pr10", "What approval does call-off order CO-2291 need?",
MATRIX + """
Reg 7.1 — Frameworks
Call-off orders under a framework agreement that is current on the Framework Register need budget holder approval only, up to £50,000 net. Orders against an expired framework follow Schedule 3.

Framework Register (extract)
FW-19 Laboratory consumables — Halden Scientific — valid 1 April 2024 to 31 March 2027
FW-22 Grounds maintenance — Ashdown Estates Services — valid 1 June 2023 to 31 May this year (renewal tender with the Tender Board)

Call-off order CO-2291, dated 3 June this year
Supplier: Ashdown Estates Services, quoting FW-22 rates
Requirement: summer grass cutting at six reservoir sites
Value: £18,000 net
""",
[("approve_band2_budget_holder_hod", "FW-22 expired on 31 May, so the 3 June call-off cannot use Reg 7.1 and follows Schedule 3, where £18,000 net is Band 2 for the budget holder and HoD."),
 ("approve_budget_holder_only", "It is a call-off from the FW-22 grounds maintenance framework at FW-22 rates and is below £50,000, so Reg 7.1 needs only the budget holder."),
 ("refer_tender_board", "FW-22 is being re-tendered by the Tender Board, so its orders go there."),
 ("approve_band3_with_procurement_manager", "Six sites make six requirements that together exceed £25,000.")],
"approve_band2_budget_holder_hod", 2),

# ------------------------------------------------------------------ pr11
# why: Reg 3.8 uses the rate on the request date (2 Sept: 0.84).
#      30,000 x 0.84 = 25,200 -> Band 3. twin 29,000 x 0.84 = 24,360 -> Band 2.
C("rt_pr11", "Which band's approvers must sign requisition RQ-5902?",
MATRIX + """
Reg 3.8 — foreign currency: orders priced in another currency are converted at the Treasury rate for the date of the requisition.
Treasury rates (EUR to GBP): 1 August: 0.82; 2 September: 0.84; 1 October: 0.85.

Requisition RQ-5902, dated 2 September
Requester: Dr Laila Hosseini, Central Laboratory
Supplier: Kaltenbrunn Analytik GmbH (lowest of three quotes)
Requirement: automatic titration unit with installation and training
Price: €30,000 net, installation included
""",
[("approve_band3_with_procurement_manager", "At the 2 September rate, €30,000 × 0.84 = £25,200, which is Band 3."),
 ("approve_band2_budget_holder_hod", "At the 2 September Treasury rate of 0.84 the order converts to less than £25,000 net, so it falls in Band 2 for the budget holder and the Head of Department."),
 ("approve_budget_holder_only", "Euro orders are paid through Treasury at the published rate, so the band approvers are not needed and only the budget holder signs the requisition.")],
"approve_band3_with_procurement_manager", 2,
twin=T([("Price: €30,000 net", "Price: €29,000 net")], "approve_band2_budget_holder_hod")),

# ------------------------------------------------------------------ pr12
# why: G- code -> Reg 8.3 adds Grants Office to the Band 2 approvers (£3,050).
C("rt_pr12", "Who must sign off requisition RQ-5933?",
MATRIX + """
Reg 8.3 — externally funded purchases
Purchases charged to an external grant code (codes beginning G-) also need Grants Office sign-off, in addition to the band approvers. The Grants Office does not replace any band approver.

Requisition RQ-5933
Requester: Ffion Carrow, Catchment Science
Requirement: 25 passive sampling kits for the river-quality study
Value: £3,050 net
Charge code: G-EA-221 (Riverwatch partnership grant)
Note: "The funder has already approved this kit in the grant budget."
""",
[("approve_band2_plus_grants_office", "£3,050 net is Band 2, so the budget holder and HoD sign, and because the charge code starts G- Reg 8.3 adds Grants Office sign-off on top of them."),
 ("approve_band2_budget_holder_hod", "£3,050 is Band 2, so the budget holder and HoD sign it."),
 ("approve_budget_holder_only", "The funder has already approved the kit, so only the budget holder needs to sign."),
 ("refer_grants_office_only", "The Grants Office signs purchases charged to grant codes instead of the HoD, and the funder has already approved the kit in the grant budget.")],
"approve_band2_plus_grants_office", 1),

# ------------------------------------------------------------------ pr13
# why: Rule 3.5: 36 x £900 = £32,400 -> Band 3 (quotes attached).
#      twin 24 months: 24 x 900 = 21,600 -> Band 2.
C("rt_pr13", "Which approval route applies to this contract?",
MATRIX + """
Requisition RQ-5960
Requester: Gwen Talbot, Facilities
Supplier: Brightwell Cleaning Services (lowest of three written quotes)
Requirement: office and welfare cleaning at Lowmoor works
Price: £900 net per month
Term: 36 months, fixed
Note: "Invoices will be monthly and each is well under £2,000."
""",
[("approve_band3_with_procurement_manager", "Over the full term, 36 × £900 = £32,400, which is Band 3."),
 ("approve_band2_budget_holder_hod", "The total over the full contract term comes to less than £25,000, so Band 2 applies."),
 ("approve_budget_holder_only", "Each monthly invoice of £900 is under £2,000, and invoices are what the budget holder approves, so every payment stays in Band 1.")],
"approve_band3_with_procurement_manager", 1,
twin=T([("Term: 36 months, fixed", "Term: 24 months, fixed")], "approve_band2_budget_holder_hod")),

# ------------------------------------------------------------------ pr14
# why: cloud service -> Rule 3.7 IT Architecture review comes first, before the
#      Band 3 approvers (3 x 14,000 = 42,000).
C("rt_pr14", "What is the next approval step for requisition RQ-5988?",
MATRIX + """
Requisition RQ-5988
Requester: Ioan Beddoe, Customer Services
Supplier: Parlance Cloud Ltd (lowest of three quotes)
Requirement: cloud-hosted call recording and quality scoring for the contact centre
Price: £14,000 net per year; three-year term
Budget holder approval: given. HoD approval: given.
""",
[("refer_it_architecture_first", "It is a cloud service, so Rule 3.7 sends it to IT Architecture for review before any band approver, including the Procurement Manager, looks at it."),
 ("approve_band3_with_procurement_manager", "Over three years the value is £42,000, so the Procurement Manager signs next as the remaining Band 3 approver."),
 ("approve_band2_budget_holder_hod", "The annual price of £14,000 is Band 2, and both Band 2 approvals are already given."),
 ("refer_tender_board", "Multi-year contracts always go to the Tender Board.")],
"refer_it_architecture_first", 2),
]
