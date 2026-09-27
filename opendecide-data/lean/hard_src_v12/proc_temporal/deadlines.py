"""proc_temporal / deadlines: appeal windows, portal cut-offs, grace periods,
warranty terms, filing roll-forward rules, SLA clocks, records requests,
objection periods, change freezes (Carrow Valley Licensing Board, Fenwright
Arts Fund, Stellmoor Cloud, Ottery Appliances, Brenholm Revenue Office,
Quillon Hosting, Marrick County Records, Hethersett Libraries, Dunlow Borough
Planning, Pellucid Networks and others)."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ dl01
# why: 10 business days after Thu 2 Apr 2026, skipping Fri 3 Apr and Mon 6 Apr:
# 7,8,9,10,13,14,15,16,17,20 -> due Mon 20 Apr 17:00. Late window 3 business days:
# 21,22,23. Received Wed 22 Apr = 2nd business day late -> accept with $60 fee.
# Without holidays due would be Thu 16 Apr and 22 Apr would be the 4th day late (wrong).
# Twin: received Mon 20 Apr 16:40 -> timely.
C("dl01", "How should the registry treat this appeal?",
"""
Carrow Valley Licensing Board — Appeals Procedure (rev. 2025)

Part 1 — Definitions
"Business day" means Monday to Friday, excluding the public holidays listed in Schedule A.
"Delivery" means the date the decision letter is signed for, as shown on the courier record.

Part 2 — Time limits
2.1 An appeal must be received within 10 business days after delivery. The day of delivery is not counted.
2.2 An appeal received by 17:00 on the last business day is timely.
2.3 An appeal received within 3 business days after the last day is accepted as late, on payment of a $60 late-filing fee.
2.4 An appeal received after that is rejected.
2.5 Registry staff have no power to waive the fee in 2.3.

Schedule A (2026): 1 January; 3 April (Good Friday); 6 April (Easter Monday); 18 May; 25 December; 28 December.

Part 3 — Hearing fees (not relevant to timing)
Standard hearing fee $180; reduced fee $45 for sole traders.

Case file LB-2026-0419
Appellant: Morrow's Taproom (premises licence, variation refused)
Decision letter delivered: Thursday 2 April 2026 (courier signature, 11:52)
Appeal received: Wednesday 22 April 2026, 10:05, by hand at the front desk
Covering note: "We were closed over Easter and your office was shut too, so I trust the fee won't be needed."
""",
[("accept_as_timely", "The appeal reached the registry by 17:00 on the tenth business day after delivery, Monday 20 April, once Good Friday and Easter Monday are skipped."),
 ("accept_with_late_fee", "The last day was Monday 20 April once both Easter holidays are skipped, and the appeal arrived 2 business days later, inside the 3-day late window."),
 ("reject_as_late", "Ten business days from 2 April end on Thursday 16 April, so the appeal came more than 3 business days after the last day."),
 ("accept_fee_waived", "The registry itself was closed over Easter, so the late-filing fee should be waived for this appellant.")],
"accept_with_late_fee", 2,
twin=T([("Wednesday 22 April 2026, 10:05", "Monday 20 April 2026, 16:40")], "accept_as_timely")),

# ------------------------------------------------------------------ dl02
# why: deadline 23:59 15 Mar portal time (UTC+1) = 22:59 UTC. Upload 18:30 UTC-5
# = 23:30 UTC = 00:30 UTC+1 on 16 Mar -> 31 min after deadline -> flagged window
# (up to 60 min, i.e. by 00:59). No outage logged, so no technical extension.
# Twin: 19:15 UTC-5 = 00:15 UTC = 01:15 UTC+1 -> 76 min late -> not accepted.
C("dl02", "What should the grants team do with this application?",
"""
Fenwright Arts Fund — Open Call 2026, Submission Rules

1. The deadline is 23:59 on Sunday 15 March 2026, portal time. Portal time is UTC+1 throughout the call.
2. The portal stamps every upload in UTC. Staff must convert the stamp to portal time before deciding.
3. An upload stamped up to 60 minutes after the deadline (that is, by 00:59 portal time on 16 March) is accepted and marked "late — flagged". It is still assessed.
4. An upload stamped more than 60 minutes after the deadline is not accepted.
5. A technical extension is given only if the portal status page records an outage during the final 24 hours.

Status page, 14–16 March: "All systems operational. No incidents recorded."

Application FAF-26-3381 — "Tidewrack: a sound walk for the Ness estuary"
Lead artist: Iolanthe Brask, based in Port Meriel (UTC−5)
Upload stamp: 2026-03-15 23:30 UTC
Applicant's email: "I pressed submit at 18:30 my time on the 15th — hours before midnight! The page was slow, though. Please confirm I'm in."
""",
[("accept_on_time", "The artist submitted at 18:30 on 15 March by her own clock, which is before 23:59 on the deadline day."),
 ("accept_flagged_late", "Converted to portal time the stamp is 00:30 on 16 March, 31 minutes after the deadline and inside the 60-minute flagged window."),
 ("reject_not_accepted", "Converted to portal time the stamp falls more than 60 minutes after 23:59 on 15 March, so the upload cannot be accepted."),
 ("grant_technical_extension", "The artist reports that the page was slow, which qualifies the upload for a technical extension.")],
"accept_flagged_late", 2,
twin=T([("2026-03-15 23:30 UTC", "2026-03-16 00:15 UTC"), ("at 18:30 my time", "at 19:15 my time")], "reject_not_accepted")),

# ------------------------------------------------------------------ dl03
# why: invoice issued 29 May 2026, before the 1 Jun amendment -> 14-day grace.
# Due 12 Jun; paid 25 Jun = 13 days after due -> within grace -> stays active,
# $25 late fee (fee applies to any payment after the due date).
# Twin: issued 2 Jun (on/after 1 Jun) -> 7-day grace; due 16 Jun; paid 25 Jun =
# 9 days after due -> suspend.
C("dl03", "What action should billing take on this account?",
"""
Stellmoor Cloud — Billing Terms, section 6 (Late payment)

6.1 Invoices are due 14 calendar days after the invoice date.
6.2 A payment received after the due date but within the grace period keeps the account active. A late fee of $25 is added to the next invoice.
6.3 The grace period is 14 calendar days after the due date. If payment has not been received by the end of the grace period, the account is suspended.
6.4 Support agents may not extend the grace period.

Amendment 6-A (published 20 April 2026): for invoices dated on or after 1 June 2026, the grace period in 6.3 is 7 calendar days.

Account: Halden Rowe Design Studio (team plan, 11 seats)
Invoice INV-55120, dated 29 May 2026, due 12 June 2026, amount $1,386.00
Payment received: 25 June 2026 (bank transfer, cleared same day)
Account status: active

Customer chat log (24 June):
Customer: "Your agent last year told me you give 30 days before anything happens."
Agent: "I'll pass that on to billing."
""",
[("keep_active_late_fee", "The invoice predates 1 June, so the 14-day grace applies, and payment 13 days after the due date is inside it; the $25 late fee applies."),
 ("keep_active_no_fee", "The payment landed within the grace period, and payments made during grace carry no charge."),
 ("suspend_account", "The invoice is dated on or after 1 June, so the 7-day grace applies, and payment 9 days after the due date missed it."),
 ("keep_active_30_day_grace", "A support agent told the customer there are 30 days of grace, so the account stays active with no fee.")],
"keep_active_late_fee", 2,
twin=T([("dated 29 May 2026, due 12 June 2026", "dated 2 June 2026, due 16 June 2026")], "suspend_account")),

# ------------------------------------------------------------------ dl04
# why: cover runs to the 2nd anniversary of DELIVERY (2 Apr 2024 -> 2 Apr 2026,
# inclusive). Claim 25 Mar 2026 -> covered -> free repair. Replacement needs 3 prior
# repairs of the same fault (only 2). Twin: claim 7 Apr 2026 -> out of cover ->
# paid repair quote (policy says quote, not decline).
C("dl04", "How should the service desk handle this washing machine claim?",
"""
Ottery Appliances — Manufacturer's Warranty (UK & Isles)

Definitions
"Delivery date" means the date the product was delivered to the customer, as shown on the delivery note. It is not the order or payment date.
"Cover" means free parts and labour for manufacturing faults.

Terms
W1. Cover lasts until the second anniversary of the delivery date, inclusive.
W2. If the same fault has been repaired under cover three times before, the product is replaced instead of repaired.
W3. Faults reported after cover ends receive a paid repair quote. They are not declined.
W4. Extended-care plans bought from retailers are separate contracts and are handled by the retailer.

Service ticket SD-771204
Model: Ottery AquaLine 8kg (serial OT8-2231-KX)
Order and payment date: 10 March 2024 (online, Brightwell Home)
Delivery note: delivered 2 April 2024
Fault reported: 25 March 2026 — drum bearing noise, drum stops mid-cycle
Repair history: bearing replaced 14 Jan 2025 (under cover); bearing replaced 9 Sep 2025 (under cover)
Customer comment: "This is the third time. I want a new machine."
""",
[("repair_free_under_cover", "Cover runs to the second anniversary of the 2 April 2024 delivery, and the fault was reported before that date."),
 ("replace_unit", "This is the third report of the bearing fault, which triggers a replacement under W2."),
 ("offer_paid_repair_quote", "Cover ended on the second anniversary of the 2 April 2024 delivery, and the fault was reported after that, so a quote is given."),
 ("decline_claim", "Cover is counted from the 10 March 2024 order date, so it had lapsed and the claim is declined.")],
"repair_free_under_cover", 2,
twin=T([("Fault reported: 25 March 2026", "Fault reported: 7 April 2026")], "offer_paid_repair_quote")),

# ------------------------------------------------------------------ dl05
# why: July return due 15 Aug 2026 = Saturday -> roll to next business day. Mon 17 Aug
# is Founders' Day (listed holiday) -> Tue 18 Aug. Filed Tue 18 Aug -> on time, no
# penalty. Twin: filed Wed 19 Aug -> 1 day late (within 30) -> 5% x 12,400 = 620.
C("dl05", "Which penalty, if any, applies to this monthly sales tax return?",
"""
Brenholm Revenue Office — Guidance Note GN-14: Monthly Returns

1. A monthly return is due on the 15th day of the following month.
2. If the due date falls on a Saturday, a Sunday or a public holiday, it moves to the next day that is none of these.
3. Late-filing penalty: 5% of the tax due if filed 1 to 30 days after the due date; 10% if filed more than 30 days after it.
4. An extension must be requested and approved before the due date. A request made after the due date is not considered.
5. Public holidays 2026: 1 Jan, 6 Apr, 1 May, 17 Aug (Founders' Day), 25 Dec, 26 Dec.

Taxpayer: Quarry Lane Bakehouse Ltd (reg. BR-40-11872)
Return period: July 2026
Tax due on return: 12,400.00
Return filed (portal receipt): Tuesday 18 August 2026, 15:12
Note from the company's bookkeeper, filed with the return: "Apologies — we missed the 15th. We ask for an extension on the grounds of staff holidays."
""",
[("no_penalty", "The due date moves from Saturday 15 August past Founders' Day on Monday 17 August to Tuesday 18 August, and the return was filed by then."),
 ("penalty_620", "The return was filed after the rolled due date of Tuesday 18 August and within 30 days, so the penalty is 5% of 12,400."),
 ("penalty_1240", "The return missed the due date, and the late-filing penalty is 10% of 12,400."),
 ("extension_granted", "The bookkeeper asked for an extension on the grounds of staff holidays, so the return is treated as on time under an extension.")],
"no_penalty", 2,
twin=T([("Tuesday 18 August 2026, 15:12", "Wednesday 19 August 2026, 09:40")], "penalty_620")),

# ------------------------------------------------------------------ dl06
# why: P2 response target 4 business hours (09:00-17:00 Mon-Fri, UTC+2). Opened Fri
# 18 Sep 16:00 UTC+2 -> 1 h Fri; 3 h Mon from 09:00 -> due Mon 21 Sep 12:00 UTC+2.
# First response 09:30 UTC = 11:30 UTC+2 -> met -> no credit.
# Twin: response 10:15 UTC = 12:15 UTC+2 -> breach -> 5% of 2,400 = 120.
C("dl06", "What service credit is owed for this ticket?",
"""
Quillon Hosting — Support SLA Schedule (Business plan)

S1. Business hours are 09:00–17:00, Monday to Friday, Quillon time (UTC+2). The SLA clock runs only during business hours.
S2. First-response targets: P1 — 1 business hour; P2 — 4 business hours; P3 — 2 business days.
S3. Each missed first-response target earns a credit of 5% of the monthly fee, capped at 20% per month.
S4. Priority is set by the customer when opening the ticket and cannot be changed by the customer afterwards.

Customer: Aldmere Logistics — monthly fee €2,400
Ticket QH-88412, priority P2 ("Backups failing on db-2")
Opened: Friday 18 September 2026, 16:00 Quillon time
First response (ticket system, UTC): Monday 21 September 2026, 09:30 UTC
Other missed targets this month: none

Customer email to account manager: "We waited the whole weekend — that's over 60 hours for a reply. Your team counts weekend breaches double, I'm told. I expect a credit."
""",
[("no_credit", "Counting only business hours, 1 hour ran on Friday and the target fell at 12:00 Monday Quillon time; the reply came at 11:30 Quillon time."),
 ("credit_120", "The reply came after 12:00 Monday Quillon time, when the 4 business hours ran out, so one 5% credit on €2,400 is owed."),
 ("credit_240", "The ticket waited over a weekend and weekend breaches count double, so 10% of €2,400 is owed."),
 ("credit_480", "More than 60 clock hours passed before the reply, so the credit reaches the 20% monthly cap.")],
"no_credit", 2,
twin=T([("Monday 21 September 2026, 09:30 UTC", "Monday 21 September 2026, 10:15 UTC")], "credit_120")),

# ------------------------------------------------------------------ dl07
# why: received 3 Feb 2026; day 1 = 4 Feb; day 30 = 5 Mar. Extension notice sent
# 5 Mar (on or before day 30) -> new deadline 5 Mar + 30 = 4 Apr. Reply 20 Mar -> in
# time -> close as compliant. Twin: notice 6 Mar -> too late -> deadline stays 5 Mar;
# reply 20 Mar is 15 days late (<= 30) -> log late, not escalate.
C("dl07", "How should the records officer close this request?",
"""
Marrick County Records Office — Access Request Handling Standard (ARHS)

1. Counting. Periods are in calendar days. The day a request is received is day 0; the next day is day 1. Weekends and holidays are not skipped.
2. Response deadline. A full response must be sent by the end of day 30.
3. Extension. The deadline may be extended once, by a further 30 days, if an extension notice is sent to the requester on or before the original day 30. A notice sent later has no effect.
4. Outcomes.
   (a) Response by the deadline (as extended): close as compliant.
   (b) Response up to 30 days after the deadline: log as a late response.
   (c) Response more than 30 days after the deadline: log as late and escalate to the Information Commissioner liaison.
5. Only one extension may be used per request.

Request AR-2026-0217 (planning correspondence, 2019–2021)
Received: 3 February 2026
Extension notice sent to requester: 5 March 2026
Full response sent: 20 March 2026
Officer's draft note: "Response was 45 days after receipt — more than 30. Suggest escalation?"
""",
[("close_as_compliant", "The extension notice went out on or before day 30 (5 March), so the deadline moved to 4 April and the 20 March reply met it."),
 ("log_late_response", "The extension notice came after day 30 (5 March), so the deadline stayed at 5 March and the reply was 15 days late."),
 ("escalate_to_liaison", "The reply came 45 days after the request arrived, which is more than 30 days."),
 ("apply_second_extension", "A second 30-day extension can be applied now to bring the 20 March reply inside the limit.")],
"close_as_compliant", 2,
twin=T([("Extension notice sent to requester: 5 March 2026", "Extension notice sent to requester: 6 March 2026")], "log_late_response")),

# ------------------------------------------------------------------ dl08
# why: due Fri 26 Jun 2026; returned Mon 6 Jul. Fines for each OPEN day after due,
# up to but not including return day. Closed Sundays + Fri 3 Jul (Harbour Day).
# Open days: Sat 27, Mon 29, Tue 30, Wed 1, Thu 2, Sat 4 = 6 -> 6 x 0.50 = 3.00.
# Twin: returned Tue 7 Jul -> add Mon 6 -> 7 days -> 3.50.
C("dl08", "What overdue charge should the branch apply?",
"""
Hethersett Libraries — Tool Library Loan Rules

Opening days: Monday to Saturday. Closed every Sunday and on the dates listed below.
Closure dates, summer 2026: Friday 3 July (Harbour Day); Monday 31 August.

Overdue charges
(a) The charge is $0.50 for each day the library is open after the due date, up to but not including the day the item is returned.
(b) The maximum charge per item is $10.00.
(c) Charges are not reduced because the borrower was away or unwell, unless a medical waiver form is on file.

Staff reminder: the self-service kiosk shows "days late" as calendar days. Do not use that figure for charging.

Loan record TL-6627
Item: Rotary hammer drill (kit 14)
Borrower: Desmond Achterberg
Due: Friday 26 June 2026
Returned: Monday 6 July 2026, 10:20
Kiosk display: "10 days late"
Medical waiver on file: no
""",
[("charge_3_00", "Six open days fall after the due date and before the return day, once Sundays and Harbour Day are left out."),
 ("charge_3_50", "Seven open days fall after the due date and before the return day, once Sundays and Harbour Day are left out."),
 ("charge_5_00", "The item was 10 calendar days late, as the kiosk shows, at $0.50 a day."),
 ("charge_2_00", "Only weekdays are charged, and without Harbour Day that leaves four chargeable days.")],
"charge_3_00", 2,
twin=T([("Returned: Monday 6 July 2026, 10:20", "Returned: Tuesday 7 July 2026, 10:20")], "charge_3_50")),

# ------------------------------------------------------------------ dl09
# why: amendment (14 days) applies to notices published on/after 1 Oct 2026.
# Published Sat 7 Nov -> +14 = Sat 21 Nov -> weekend roll -> Mon 23 Nov. Objection
# received Fri 27 Nov -> late -> file as late comment (not returned).
# Twin: amendment effective 1 Dec 2026 -> old 21 days -> Sat 28 Nov -> Mon 30 Nov ->
# 27 Nov objection valid.
C("dl09", "How should the planning registry log this objection?",
"""
Dunlow Borough Council — Development Management Procedures

Part 4. Objection period
4.1 Objections to a planning application may be made within 21 calendar days after the date the notice is published in the Dunlow Courier. The publication day is not counted.
4.2 If the last day falls on a Saturday or Sunday, the period ends on the following Monday.
4.3 Objections received within the period are registered as valid objections and must be considered by the committee.
4.4 Objections received after the period are filed as late comments. They are shown to the case officer but are not registered. They are never returned unread.

Amendment 4/2026: for notices published on or after 1 October 2026, "21 calendar days" in 4.1 is replaced by "14 calendar days".

Application DB/26/0931 — two-storey rear extension, 18 Linden Row
Notice published in the Dunlow Courier: Saturday 7 November 2026
Objection received: Friday 27 November 2026, by email, from the occupier of 20 Linden Row

Case officer's note: "The website listing went up a day late, on 8 November — should we give the neighbours an extra week?"
(The Procedures say the period runs from newspaper publication only.)
""",
[("register_valid_objection", "The notice predates the amendment's effective date, so the 21-day period applies and it ended on Monday 30 November after the weekend roll."),
 ("file_as_late_comment", "The notice falls under the amended 14-day period, which ended on Monday 23 November after the weekend roll, before the objection arrived."),
 ("return_unread", "The objection arrived after the 14-day period, and late objections are sent back to the objector unread."),
 ("extend_one_week", "The website listing was a day late, so the neighbours get an extra week and the objection is registered.")],
"file_as_late_comment", 2,
twin=T([("for notices published on or after 1 October 2026", "for notices published on or after 1 December 2026")], "register_valid_objection")),

# ------------------------------------------------------------------ dl10
# why: freeze 19 Dec 2026 00:00 UTC to 4 Jan 2027 00:00 UTC; overlap of ANY part of
# the window counts. Start 15:30 UTC-8 on 18 Dec = 23:30 UTC; 90 min -> ends 01:00
# UTC 19 Dec -> overlaps -> needs freeze exception from CAB (not rejected outright).
# Twin: start 14:00 UTC-8 = 22:00 UTC, ends 23:30 UTC 18 Dec -> clear -> standard.
C("dl10", "What approval route does this change request need?",
"""
Pellucid Networks — Change Management Standard, year-end addendum

Y1. The year-end change freeze runs from 00:00 UTC on 19 December 2026 to 00:00 UTC on 4 January 2027.
Y2. A change is inside the freeze if any part of its planned window falls within the freeze.
Y3. A change inside the freeze needs a freeze exception approved by the Change Advisory Board (CAB). Such changes are not rejected by reviewers; CAB decides.
Y4. A change wholly outside the freeze follows the standard route (team-lead approval).
Y5. Planned windows must be converted to UTC before applying Y2.

Change request CR-30716
Title: Rotate TLS certificates on edge load balancers (eu-west, us-west)
Requester: Farrah Oyelaran, network engineering, Seaboard office (UTC−8)
Planned start: 18 December 2026, 15:30 Seaboard time
Planned duration: 90 minutes
Team lead comment: "Starts on the 18th, so it's before the freeze. I'm happy to approve."
""",
[("standard_team_lead_approval", "Converted to UTC, the whole 90-minute window ends before 00:00 UTC on 19 December, so the change is outside the freeze."),
 ("cab_freeze_exception", "Converted to UTC, part of the 90-minute window falls after 00:00 UTC on 19 December, so the change sits inside the freeze."),
 ("reject_change", "The window overlaps the freeze, and changes during the freeze are rejected by the reviewer."),
 ("approve_by_start_date", "The change starts on 18 December by the requester's clock, which is before the freeze begins on the 19th.")],
"cab_freeze_exception", 3,
twin=T([("18 December 2026, 15:30 Seaboard time", "18 December 2026, 14:00 Seaboard time")], "standard_team_lead_approval")),

# ------------------------------------------------------------------ dl11
# why: "date of loss" = when damage occurred, unless it could not reasonably have
# been discovered -> then discovery date. Leak inside wall, found 14 Aug 2026 when
# plasterer opened wall (not discoverable before). 60 days from 14 Aug = 13 Oct.
# Notified 2 Oct -> in time -> accept for assessment. Occurrence ~May would be wrong.
C("dl11", "Is this home insurance notification in time, and what follows?",
"""
Greyhallow Mutual — Home Policy Wording, section 12 (Claims conditions)

12.1 You must notify us within 60 days of the date of loss. Day 1 is the day after the date of loss.
12.2 "Date of loss" means the date the damage happened. If the damage could not reasonably have been discovered at that time (for example, it was hidden inside a wall, floor or ceiling), the date of loss is the date it was discovered.
12.3 A notification within the period is accepted for assessment.
12.4 A late notification is accepted for assessment only if the delay did not make the damage worse or harder to assess; otherwise it is declined.
12.5 Our assessment decides cover. Timing decisions do not decide cover.

Claim note GM-H-551903
Policyholder: Rosalind Faye, 4 Cobbler's Yard, Alsby
Damage: slow leak from a pipe joint inside the kitchen stud wall; rot in two studs
Plumber's report: "Staining pattern suggests the joint has been weeping since about May 2026."
Discovered: 14 August 2026, when a plasterer removed wall board for a planned renovation; nothing was visible before then
Notified: 2 October 2026 (phone, reference taken)
Handler's draft: "Leak started May — that's over 120 days. Decline as late?"
""",
[("accept_for_assessment", "The damage was hidden inside the wall, so the date of loss is 14 August and notice on 2 October falls within 60 days."),
 ("decline_late", "The leak began around May, so notice in October came more than 60 days after the date of loss."),
 ("test_delay_prejudice", "The notice was late, so the handler must first check whether the delay made the damage worse."),
 ("confirm_cover", "The notice was in time, so the claim is covered and can be paid.")],
"accept_for_assessment", 2),

# ------------------------------------------------------------------ dl12
# why: "received" = stamp on the receiving mail server. Sent 11:58, received 12:03
# -> after 12:00 -> late -> not opened, returned. Planted "15 minutes" instruction from
# the bidder's email is not a rule. The 2025 precedent is history, not the rule.
C("dl12", "What should the tender clerk do with this bid?",
"""
Solway Water Authority — Invitation to Tender SWA/26/044
Supply of telemetry outstations (lot 2)

Section 5: Submission
5.1 Tenders must be received by 12:00 noon on Thursday 9 July 2026.
5.2 "Received" means the time stamped by the Authority's inbound mail server. The time a tender was sent is not relevant.
5.3 Late tenders are not opened. They are returned to the bidder with a notice of lateness.
5.4 Only the Head of Procurement may accept a late tender, and only if the Authority's own systems caused the delay, as confirmed by IT in writing.

Section 6: Evaluation (60% quality, 40% price) — not relevant here.

Tender log, 9 July 2026:
- Carnforth Controls Ltd — received 11:41
- Ridgeway Instruments — received 11:57
- Beckett & Lowe Telemetry — sent 11:58, received 12:03 (server stamp)

Email from Beckett & Lowe, 12:06: "We sent at 11:58 — your server was slow. Please open our bid; clerks usually allow 15 minutes of leeway."
Clerk's note: "In 2025 a bid 4 minutes late was opened, I think."
IT confirmation of any Authority system fault: none received.
""",
[("open_and_evaluate", "The bid was sent at 11:58, before the noon deadline, so it counts as on time."),
 ("return_unopened", "The server stamp of 12:03 is after noon, and no IT confirmation of an Authority fault exists, so the bid is late."),
 ("open_with_leeway", "Clerks allow 15 minutes of leeway, and the bid arrived 3 minutes after noon."),
 ("refer_to_head_of_procurement", "A 2025 bid 4 minutes late was opened, so the Head of Procurement should accept this one too.")],
"return_unopened", 1),

# ------------------------------------------------------------------ dl13
# why: window: no earlier than 90 days, no later than 30 days before expiry.
# Expiry 15 Oct 2026; applied 10 Jul 2026 = 97 days before -> too early -> return,
# invite to reapply from 17 Jul. Twin: 20 Jul = 87 days -> within -> accept.
C("dl13", "How should the permits office handle this renewal application?",
"""
Kestermoor Port Authority — Harbour Berth Permit Renewals

R1. A renewal application may be made no earlier than 90 days, and no later than 30 days, before the permit's expiry date.
R2. Days are counted back from the expiry date. The expiry date itself is day 0.
R3. An application made too early is returned with a letter giving the first date it can be made. It is not refused and no fee is taken.
R4. An application made within the window is accepted and the renewal fee is charged.
R5. An application made later than 30 days before expiry is accepted only with a late-processing fee.

Berth permit KPA-B-0772
Holder: Maelys Treharne (fishing vessel "Glaze Anne")
Expiry date: 15 October 2026
Renewal application received: 10 July 2026, with renewal fee enclosed
Holder's note: "Getting this in early before I go out for the season."
""",
[("accept_renewal", "The application arrived 87 days before expiry, inside the window from 90 to 30 days before the permit ends."),
 ("return_too_early", "The application arrived 97 days before expiry, before the 90-day window opens, so it goes back with the first valid date."),
 ("accept_with_late_fee", "The application arrived more than 30 days before expiry, so the late-processing fee applies."),
 ("refuse_application", "An application made outside the window is refused and the fee is kept.")],
"return_too_early", 2,
twin=T([("Renewal application received: 10 July 2026", "Renewal application received: 20 July 2026")], "accept_renewal")),

# ------------------------------------------------------------------ dl14
# why: posted Thu 30 Jul 2026; deemed received 3 business days after posting: Fri 31,
# Mon 3, Tue 4 Aug. Effective date must be on/after 60th day after deemed receipt:
# 4 Aug + 60 = 3 Oct. Stated effective 1 Oct is too early -> notice stays valid but
# takes effect from the first rent-period start on/after 3 Oct = 1 Nov.
# Twin: posted Thu 23 Jul -> deemed Tue 28 Jul -> +60 = 26 Sep <= 1 Oct -> 1 Oct.
C("dl14", "From what date does this rent increase take effect?",
"""
Harrowgate Lettings — Residential Tenancy Handbook, chapter 7 (Rent reviews)

7.1 A landlord must give written notice of a rent increase. The increase may take effect only on a date that is on or after the 60th day after the tenant receives the notice.
7.2 Notice sent by post is deemed received on the third business day after the day of posting. Business days are Monday to Friday; there are no public holidays in the period covered by this file.
7.3 If the date given in a notice is too early, the notice is not void. The increase instead takes effect from the first rent-period start date that is on or after the 60th day.
7.4 Rent periods for this tenancy start on the 1st of each month.

File note — Flat 3, 22 Westerlea Road
Tenant: Jonah Mbeki
Current rent: £1,120 per month; proposed rent: £1,175 per month
Notice posted (first-class, proof of posting): Thursday 30 July 2026
Effective date stated in notice: 1 October 2026
Tenant's email: "I only opened the letter on 10 August because I was away, so surely nothing can change before December."
""",
[("effective_1_october", "Deemed receipt was Tuesday 28 July, and 1 October is after the 60th day from then, so the stated date stands."),
 ("effective_1_november", "Deemed receipt was Tuesday 4 August; the 60th day after is 3 October, so the increase starts with the next rent period, 1 November."),
 ("effective_3_october", "Deemed receipt was Tuesday 4 August, so the increase starts on the 60th day after it, 3 October."),
 ("notice_void", "The stated date is less than 60 days after receipt, so the notice has no effect and must be served again."),
 ("effective_1_december", "The tenant opened the letter on 10 August, so the 60 days run from then and the next rent period after that is 1 December.")],
"effective_1_november", 3,
twin=T([("Notice posted (first-class, proof of posting): Thursday 30 July 2026", "Notice posted (first-class, proof of posting): Thursday 23 July 2026")], "effective_1_october")),

# ------------------------------------------------------------------ dl15
# why: 30 days from DELIVERY, but holiday rule: delivered 15 Nov-24 Dec -> return by
# 31 Jan. Delivered 18 Nov 2026; return request 20 Jan 2027 -> allowed -> refund.
# Unopened, so no restocking fee. Twin: delivered 12 Nov -> standard 30 days -> 12 Dec;
# 20 Jan is 69 days after delivery, beyond the 60-day store-credit window -> decline.
C("dl15", "What should returns do with this request?",
"""
Pennyroyal Home — Returns Policy (effective 1 September 2026)

1. Standard window: you may return an item within 30 days of the delivery date for a refund to the original payment method.
2. Holiday window: items delivered between 15 November and 24 December (inclusive) may be returned until 31 January of the following year for a refund.
3. Late returns: a return requested after the window that applies, but no more than 60 days after delivery, receives store credit only. Later requests are declined.
4. A 15% restocking fee applies only to opened electronics.
5. Order date and dispatch date do not affect any window.

Return request RR-90214
Customer: Wilhelmina Oduya
Item: Espresso machine, model Brava Duo (sealed, unopened)
Order date: 9 November 2026
Delivery date: 18 November 2026
Return requested: 20 January 2027
Agent note: "Ordered 9 Nov — way past 30 days. Maybe store credit, minus restocking?"
""",
[("refund_to_card", "Delivery fell between 15 November and 24 December, so the holiday window runs to 31 January and the request is inside it."),
 ("store_credit_only", "The request came more than 30 days after the order date, so only store credit is available."),
 ("refund_minus_restocking", "The item is electronics, so a 15% restocking fee comes off the refund."),
 ("decline_return", "Delivery was before 15 November, so the 30-day window applies, and the request came more than 60 days after delivery.")],
"refund_to_card", 2,
twin=T([("Order date: 9 November 2026\nDelivery date: 18 November 2026", "Order date: 3 November 2026\nDelivery date: 12 November 2026"),
        ("Ordered 9 Nov", "Ordered 3 Nov")], "decline_return")),

# ------------------------------------------------------------------ dl16
# why: expired 31 Aug 2026. Days after expiry: 1 Sep = day 1 ... 30 Sep = day 30.
# "1 to 30 days after expiry, inclusive" -> $15. Twin: renewed 1 Oct = day 31 -> $40.
C("dl16", "Which late fee applies to this vehicle licence renewal?",
"""
Western Tarn Motor Registry — Fees Schedule 2026, Table C (Late renewal)

C1. A licence renewed on or before its expiry date: no late fee.
C2. Renewed 1 to 30 days after expiry (inclusive): late fee $15.
C3. Renewed 31 to 90 days after expiry (inclusive): late fee $40.
C4. Renewed more than 90 days after expiry: late fee $40 plus a roadworthiness re-inspection.
C5. Day 1 is the day after the expiry date. Weekends and holidays count.

Note: the base renewal charge (Table A, $212 for a light van) is charged separately and is not a late fee.

Counter transaction MR-551-0034
Vehicle: light van, plate WTK 44-19
Keeper: Ansel Brightmore trading as Brightmore Glazing
Licence expiry date: 31 August 2026
Renewal paid at counter: 30 September 2026
Keeper: "It's only one month late. The clerk last year charged me forty."
""",
[("late_fee_15", "The renewal came on day 30 after the 31 August expiry, inside the 1 to 30 day band."),
 ("late_fee_40", "The renewal came on day 31 after the 31 August expiry, inside the 31 to 90 day band."),
 ("late_fee_40_reinspection", "The licence lapsed a full month, so the fee and a roadworthiness re-inspection are due."),
 ("no_late_fee", "The renewal was paid within the same billing month as the expiry, so no late fee applies.")],
"late_fee_15", 1,
twin=T([("Renewal paid at counter: 30 September 2026", "Renewal paid at counter: 1 October 2026")], "late_fee_40")),

# ------------------------------------------------------------------ dl17
# why: teaching weeks exclude reading week (w/c 12 Oct). Week 1 w/c 7 Sep ... week 5
# w/c 5 Oct, reading week, week 6 w/c 19 Oct, week 7 w/c 26 Oct, week 8 w/c 2 Nov
# (Mon 2 - Sun 8 Nov). Withdrawal Fri 6 Nov -> within week 8 -> W.
# Twin: Mon 9 Nov -> week 9 -> WF.
C("dl17", "What should the registrar record for this module withdrawal?",
"""
Aldwyck University — Academic Regulations, section 11 (Withdrawal from a module)

11.1 Teaching weeks are numbered from week 1, the week beginning Monday 7 September 2026. Each week runs Monday to Sunday.
11.2 Reading week (the week beginning Monday 12 October 2026) is not a teaching week and is not numbered.
11.3 A student who withdraws on or before the last day of teaching week 8 receives a W (no effect on average).
11.4 A student who withdraws later than that receives a WF (counts as a fail).
11.5 Tuition refunds follow the Fees Regulations, not this section.

Withdrawal form AW-11-2206
Student: Pieter Lindqvist, BSc Geography, year 2
Module: GEO2204 Coastal Processes
Form submitted in the student portal: Friday 6 November 2026, 14:22
Tutor's comment: "It's week 9 now, I think, so it should be a WF."
""",
[("record_W", "With reading week left out, week 8 runs from Monday 2 to Sunday 8 November, and the form came within it."),
 ("record_WF", "With reading week left out, week 8 ended on Sunday 8 November, and the form came after that."),
 ("record_WF_week9", "Counting every week from 7 September, 6 November falls in week 9, so the withdrawal is late."),
 ("refund_half_tuition", "A withdrawal in week 8 earns a half-tuition refund under section 11.")],
"record_W", 2,
twin=T([("Friday 6 November 2026, 14:22", "Monday 9 November 2026, 14:22")], "record_WF")),

# ------------------------------------------------------------------ dl18
# why: backups kept 35 days from deletion time: deleted 2 Mar 2026 10:00 UTC -> purge
# at 6 Apr 2026 10:00 UTC. Request at 23:00 UTC+10 on 6 Apr = 13:00 UTC -> after purge
# -> cannot restore -> decline (offer nothing from backup).
# Twin: request 18:00 UTC+10 = 08:00 UTC -> before purge -> restore.
C("dl18", "What should the storage team do with this restore request?",
"""
Brightfold Data Services — Deleted Data Recovery Policy

D1. When a customer deletes a workspace, a backup copy is kept for 35 days from the exact time of deletion, then purged automatically. There is no manual hold.
D2. A restore request is valid if the request is logged before the purge time. All times in this policy are UTC.
D3. A valid request is restored free of charge within 2 business days.
D4. A request logged after the purge time is declined; no copy exists.
D5. Customer-local times must be converted to UTC.

Ticket BDS-40018
Customer: Coralline Studio (Sydmere office, UTC+10)
Workspace: "Archive-2021-clients", deleted 2 March 2026, 10:00 UTC
Restore request logged: 6 April 2026, 23:00 Sydmere time
Customer: "It's still the 6th here, and 35 days after the 2nd is the 6th, so we're within time. Please restore."
""",
[("restore_free", "The request converts to 08:00 UTC on 6 April, before the purge at 10:00 UTC that day, so the backup still exists."),
 ("decline_purged", "The request converts to 13:00 UTC on 6 April, after the purge at 10:00 UTC that day, so no backup remains."),
 ("restore_same_date", "The request was made on 6 April by the customer's clock, the same date as the purge, so it is in time."),
 ("place_manual_hold", "The team should place a manual hold on the backup while the dates are checked.")],
"decline_purged", 2,
twin=T([("6 April 2026, 23:00 Sydmere time", "6 April 2026, 18:00 Sydmere time")], "restore_free")),

# ------------------------------------------------------------------ dl19
# why: 7 CLEAR days = full days between the notice day and the meeting day, both
# excluded. Notice Tue 3 Mar, meeting Wed 11 Mar -> 4,5,6,7,8,9,10 = 7 -> valid.
# Twin: meeting Tue 10 Mar -> 6 clear days -> invalid -> reschedule.
C("dl19", "Can the board meeting go ahead on the date in the notice?",
"""
Tolhurst Community Energy Co-operative — Rules, extract

Rule 31. Board meetings
31.1 At least 7 clear days' notice must be given of a board meeting.
31.2 "Clear days" means full days, not counting the day the notice is given or the day of the meeting.
31.3 A meeting held with short notice is invalid unless every director has agreed in writing to short notice.
31.4 If notice is short and written agreement is incomplete, the secretary must reschedule the meeting.
31.5 Emailed notice is given on the day it is sent.

Rule 32. Quorum — three directors (not in issue here).

Secretary's file
Notice emailed to all five directors: Tuesday 3 March 2026
Meeting date in notice: Wednesday 11 March 2026
Written agreement to short notice: 3 of 5 directors
Director Okafor's reply: "8 days between the 3rd and the 11th — that's plenty."
""",
[("proceed_as_notified", "Seven full days, 4 to 10 March, lie between the notice day and the meeting day."),
 ("reschedule_meeting", "Only six full days lie between the notice day and the meeting day, and 2 of 5 directors have not agreed to short notice."),
 ("proceed_with_agreement", "A majority of directors agreed in writing to short notice, which is enough to hold the meeting."),
 ("proceed_eight_days", "The meeting is 8 days after the notice date, more than the 7 required.")],
"proceed_as_notified", 2,
twin=T([("Meeting date in notice: Wednesday 11 March 2026", "Meeting date in notice: Tuesday 10 March 2026"),
        ("between the 3rd and the 11th", "between the 3rd and the 10th")], "reschedule_meeting")),

# ------------------------------------------------------------------ dl20
# why: renewal 1 Mar 2027. Cancel at least 30 days before. 30 Jan -> 1 Mar 2027:
# Jan 30->Feb 28 = 29 days, ->Mar 1 = 30 -> exactly 30 -> no renewal charge.
# (2027 is not a leap year.) Twin: 31 Jan -> 29 days -> renewal charged.
C("dl20", "Should the renewal charge go through for this subscription?",
"""
Lanternfish Analytics — Subscription Terms, clause 9 (Renewal and cancellation)

9.1 Annual subscriptions renew automatically on the renewal date.
9.2 To avoid renewal, the customer must cancel at least 30 days before the renewal date. The number of days is the renewal date minus the cancellation date.
9.3 A cancellation made later than that takes effect at the end of the renewed term. The renewal fee is charged and is non-refundable.
9.4 Pricing for the next term is set out in the order form.

Account: Vessel & Vine Imports (Pro, annual)
Renewal date: 1 March 2027
Renewal fee: $4,800
Cancellation received (in-app, time-stamped): 30 January 2027
Finance note: "February has 29 days this time, so this is only 29 days before — charge it."
Calendar check: 2027 is not a leap year.
""",
[("cancel_no_charge", "From 30 January to 1 March 2027 is 30 days, since February 2027 has 28 days, which meets the 30-day minimum."),
 ("charge_renewal", "From the cancellation date to 1 March 2027 is fewer than 30 days, so the fee is charged."),
 ("charge_leap_year", "February has 29 days, so 30 January is only 29 days before renewal and the fee is charged."),
 ("refund_prorated", "The fee is charged and then refunded pro rata for the unused months.")],
"cancel_no_charge", 2,
twin=T([("Cancellation received (in-app, time-stamped): 30 January 2027", "Cancellation received (in-app, time-stamped): 31 January 2027")], "charge_renewal")),

# ------------------------------------------------------------------ dl21
# why: cut-off 14:00 warehouse time. Order Fri 16 Oct 14:20 -> after cut-off -> ships
# next business day. Mon 19 Oct is a listed holiday -> ships Tue 20. Guaranteed
# delivery = 2 business days after dispatch -> Wed 21 (1), Thu 22 (2). Delivered Thu 22
# -> on time -> no refund. Twin: order 13:20 -> ships Fri 16 -> Tue 20 (1), Wed 21 (2)
# -> delivered Thu 22 is late -> refund express fee.
C("dl21", "Is the customer owed an express shipping refund?",
"""
Marlbeck Outfitters — Express Delivery Promise

E1. Orders placed before 14:00 warehouse time on a business day are dispatched the same day. Later orders are dispatched on the next business day.
E2. Express parcels are guaranteed to be delivered by the second business day after dispatch.
E3. If a parcel is delivered after the guaranteed day, the €9.95 express fee is refunded.
E4. Business days are Monday to Friday, except warehouse holidays. Warehouse holidays in 2026: 19 October (Harvest Monday), 25 December, 28 December.
E5. The estimate shown at checkout is a guide only; the guarantee follows E1 and E2.

Order MO-2026-771390
Placed: Friday 16 October 2026, 14:20 warehouse time
Service: Express (€9.95)
Checkout estimate shown: "Arrives Tuesday 20 October"
Carrier scan: delivered Thursday 22 October 2026, 11:05
Customer email: "You promised Tuesday. I want my express fee back."
""",
[("no_refund", "The order missed the cut-off and Harvest Monday is not a business day, so dispatch was Tuesday 20 October and the guarantee ran to Thursday 22 October."),
 ("refund_express_fee", "The order made the cut-off and went out on Friday 16 October, so the guarantee ran to Wednesday 21 October and delivery on the 22nd was late."),
 ("refund_checkout_promise", "The checkout page promised arrival on Tuesday 20 October, and the parcel came two days later."),
 ("refund_half_fee", "Delivery was one business day late, so half of the express fee is returned.")],
"no_refund", 3,
twin=T([("Friday 16 October 2026, 14:20 warehouse time", "Friday 16 October 2026, 13:20 warehouse time")], "refund_express_fee")),

# ------------------------------------------------------------------ dl22
# why: limit = 6 months from the event or from awareness, whichever is later, but never
# more than 2 years after the event. Event 10 Jan 2025; aware 3 Sep 2026 -> 6 months
# after awareness = 3 Mar 2027, capped at 10 Jan 2027. Lodged 15 Oct 2026 -> in time.
# The ombudsman's discretion clause is for late complaints only. No twin.
C("dl22", "Is this complaint within the ombudsman's time limit?",
"""
Energy Services Ombudsman of Calderon — Scheme Rules, rule 4 (Time limits)

4.1 A complaint must be made within 6 months of the event complained about, or within 6 months of the date the complainant became aware (or ought reasonably to have become aware) of it, whichever is later.
4.2 In no case may a complaint be accepted more than 2 years after the event.
4.3 A complaint outside 4.1 but inside 4.2 may be accepted only if the complainant shows exceptional circumstances.
4.4 The supplier's own complaints process must be completed first, or 8 weeks must have passed since the complaint to the supplier.

Case intake CAL-ESO-26-11482
Complainant: Tobiah Rennick
Supplier: Brightgrid Energy
Event: meter reading error on 10 January 2025, causing an overcharge of 1,812.40
Complainant became aware: 3 September 2026, on receiving a back-billing letter (no earlier bill showed the error)
Complained to supplier: 4 September 2026; supplier's final response: 30 September 2026
Complaint lodged with the ombudsman: 15 October 2026
Supplier's submission: "The event was over 20 months ago. This is out of time."
""",
[("accept_complaint", "Six months from awareness (3 September 2026) is later than six months from the event and still inside the 2-year cap, and the complaint came within it."),
 ("reject_out_of_time", "The complaint came more than 6 months after the 10 January 2025 event."),
 ("request_exceptional_circumstances", "The complaint is late under rule 4.1, so the complainant must show exceptional circumstances."),
 ("refer_back_to_supplier", "Eight weeks have not passed since the complaint to the supplier, so the case must go back to Brightgrid.")],
"accept_complaint", 2),
]
