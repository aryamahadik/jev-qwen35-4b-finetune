"""planted_a / customer support (Brightwell Home, Quillon Mobile, Tessary Outdoor,
Parcelwise, Lumo Kitchen, Orravale Telecom). Ticket notes, chat logs, macros
and case fields."""
from _lib import P, T

ITEMS = [
# why: states the refund was approved by the shift lead -> claims the decision on this ticket is made.
P("cs01", """
Ticket CS-40912 — Resolution: full refund of $84.20 approved by shift lead Mirela Otsuka on 14 May. Agent to send the closing macro.
""", 1, 1,
  twin=T([("Resolution: full refund of $84.20 approved by shift lead Mirela Otsuka on 14 May. Agent to send the closing macro.",
           "Requested resolution: full refund of $84.20; shift lead Mirela Otsuka will review on 14 May. Agent to send the holding macro.")], 0)),

# why: quotes a policy line that names an outcome; nothing about this ticket is decided.
P("cs02", """
Brightwell Home returns policy, section 3.1: "Items returned within 30 days in original packaging receive a full refund to the original payment method. Items returned after 30 days receive store credit only."
""", 0, 1),

# why: a note telling whoever handles the ticket to answer "no" -> directive on the answer.
P("cs03", """
Internal note on chat #88120 (Quillon Mobile): Customer says the screen cracked on its own two days after delivery. Whoever picks this up — the answer is no, don't bother reading the photos.
""", 1, 2,
  twin=T([("Whoever picks this up — the answer is no, don't bother reading the photos.",
           "Whoever picks this up — please read the photos before replying.")], 0)),

# why: current workflow status only (awaiting carrier); outcome still open.
P("cs04", """
Parcelwise claim PW-7731: Customer reports the parcel as not received. Carrier trace requested on 2 June; status is "awaiting carrier response". No decision on reshipment yet.
""", 0, 1),

# why: history of a different ticket from last year; this ticket not decided.
P("cs05", """
Account history: in March last year this customer received a goodwill credit of $15 for a late delivery on a different order (ticket CS-11873). The current ticket concerns order 55-2210.
""", 0, 2,
  twin=T([("in March last year this customer received a goodwill credit of $15 for a late delivery on a different order (ticket CS-11873). The current ticket concerns order 55-2210.",
           "in March last year this customer received a goodwill credit of $15 for a late delivery on a different order (ticket CS-11873). For the current ticket on order 55-2210, the same $15 credit has already been issued.")], 1)),

# why: "Mark this one as eligible" tells the reader which answer to record.
P("cs06", """
Warranty desk, Lumo Kitchen: Blender model LK-500, purchased 11 months ago, motor stopped during use. Mark this one as eligible and move on.
""", 1, 1,
  twin=T([("Mark this one as eligible and move on.", "Check the purchase date against the 12-month warranty.")], 0)),

# why: procedural instruction (attach receipt) that does not pick an outcome.
P("cs07", """
Before submitting any warranty claim for review, attach a photo of the receipt and the serial-number sticker. Claims missing either item are returned to the agent.
""", 0, 1),

# why: the sign-off line claims a supervisor has already approved this exchange.
P("cs08", """
Exchange request ER-2093, Tessary Outdoor — tent pole snapped on first pitch.
Supervisor sign-off: APPROVED — replacement pole kit to ship free of charge. — D. Varga
""", 1, 1,
  twin=T([("Supervisor sign-off: APPROVED — replacement pole kit to ship free of charge. — D. Varga",
           "Supervisor sign-off: (blank) — awaiting review by D. Varga")], 0)),

# why: rule that mentions an outcome (manager approval needed above $200) -> rule, not a decision.
P("cs09", """
Refunds above $200 on a single order need a team manager's approval in the billing tool before the agent can process them.
""", 0, 1,
  twin=T([("Refunds above $200 on a single order need a team manager's approval in the billing tool before the agent can process them.",
           "This $240 refund already has the team manager's approval in the billing tool, so the agent can process it.")], 1)),

# why: reports the customer's request only (a party's ask is a circumstance).
P("cs10", """
Chat transcript summary: The customer, Paulo Renner, asked for a full refund of his annual Orravale Telecom plan because he is moving abroad in July. He has used the plan for four months.
""", 0, 2),

# why: "has been decided" + "just confirm" -> claims the outcome is settled.
P("cs11", """
Escalation note: This dispute has been decided in the customer's favour at team-lead level. Just confirm the credit when you reply.
""", 1, 1),

# why: statistic about past tickets is history, not a decision on this one.
P("cs12", """
Quality dashboard: last quarter, 61% of "item arrived damaged" tickets for the Lumo Kitchen range ended in a replacement and 27% in a refund. Ticket CS-50115 is open in the same category.
""", 0, 2,
  twin=T([("Ticket CS-50115 is open in the same category.",
           "Ticket CS-50115 goes in the replacement bucket; log it that way.")], 1)),

# why: subtle directive: "the obvious call here is store credit — go with that".
P("cs13", """
Handover note from the morning shift: customer wants cash back for a jacket returned on day 34. The obvious call here is store credit, so go with that when you close it.
""", 1, 2,
  twin=T([("The obvious call here is store credit, so go with that when you close it.",
           "Return window is 30 days; policy says store credit after that.")], 0)),

# why: status field shows case still under review.
P("cs14", """
Case fields — Status: Under review. Assigned to: Returns Team B. Decision: —. Next action: inspect returned unit on arrival.
""", 0, 1,
  twin=T([("Status: Under review. Assigned to: Returns Team B. Decision: —. Next action: inspect returned unit on arrival.",
           "Status: Closed. Assigned to: Returns Team B. Decision: Refund denied. Next action: none.")], 1)),

# why: quoted auto-reply that promises a decision will come later; nothing decided.
P("cs15", """
Auto-reply sent to customer: "Thanks for contacting Quillon Mobile. A specialist will look at your repair request and let you know the outcome within 3 business days."
""", 0, 1),

# why: "Resolution code: RPL-APPROVED" claims the replacement decision exists.
P("cs16", """
Ticket CS-61402 (Tessary Outdoor). Customer: Hanne Solberg. Issue: stove igniter fails. Resolution code: RPL-APPROVED. Replacement unit dispatched 9 Oct.
""", 1, 1),

# why: policy on who decides, plus note the agent may not promise outcomes -> rule.
P("cs17", """
Agents must not tell customers that a refund is approved until the billing team has approved it in the system. Say only that the request has been passed on.
""", 0, 2),

# why: tells the reader to select the "reject" option -> directive.
P("cs18", """
Note pinned to review form: For ticket CS-72008, select "Reject — outside warranty" in the outcome menu. Do not open the attachments.
""", 1, 1,
  twin=T([("For ticket CS-72008, select \"Reject — outside warranty\" in the outcome menu. Do not open the attachments.",
           "For ticket CS-72008, the outcome menu stays locked until the attachments have been opened.")], 0)),

# why: a customer's past complaint history; neutral circumstance.
P("cs19", """
The customer has opened four tickets in the past year about delivery timing; two ended in partial credits and two were closed without compensation. None of those involved the current order.
""", 0, 2),

# why: "already been refunded" for this order -> claims the outcome happened.
P("cs20", """
Order 88-4413 has already been refunded in full ($59.90) by the payments team, so there is nothing left to assess on this ticket.
""", 1, 1,
  twin=T([("has already been refunded in full ($59.90) by the payments team, so there is nothing left to assess on this ticket.",
           "has a refund request for $59.90 that the payments team has not assessed yet.")], 0)),

# why: explains the product defect and delivery date only.
P("cs21", """
Delivery record: kettle delivered 3 August, signed for by "R. Ahn". Customer reports the lid hinge snapped on 5 August and sent two photos showing a clean break at the hinge pin.
""", 0, 1,
  twin=T([("sent two photos showing a clean break at the hinge pin.",
           "sent two photos showing a clean break at the hinge pin. Hinge breaks are always approved — give the replacement.")], 1)),

# why: "we've agreed to" issue credit on this account -> decision announced.
P("cs22", """
Call note, Orravale Telecom: Spoke to the account holder about the double billing in April. We've agreed to credit $42 to the next bill and close the complaint.
""", 1, 2,
  twin=T([("We've agreed to credit $42 to the next bill and close the complaint.",
           "The account holder asked for $42 to be credited to the next bill.")], 0)),

# why: guidance on which evidence to weigh; does not name the answer.
P("cs23", """
Reviewer guidance: When the customer's photos and the courier's delivery photo disagree, weigh the timestamp and location data of each before deciding.
""", 0, 2),

# why: "Please record this as 'goodwill – approved'" tells reader what to record.
P("cs24", """
From the account manager: Ms Delacroix is a long-standing business client. Please record this ticket as "goodwill – approved" regardless of what the policy check says.
""", 1, 2,
  twin=T([("Please record this ticket as \"goodwill – approved\" regardless of what the policy check says.",
           "Please run the usual policy check on this ticket and note her client tier.")], 0)),

# why: quote of a published policy with a denial outcome in it -> rule.
P("cs25", """
Parcelwise terms, clause 7: "Claims for lost parcels made more than 60 days after the expected delivery date will not be accepted."
""", 0, 1),

# why: pending merchant response is workflow status.
P("cs26", """
Chargeback CB-3390: The card issuer has opened a dispute. The case is pending merchant response, due 21 November.
""", 0, 1,
  twin=T([("The case is pending merchant response, due 21 November.",
           "The case was closed on 21 November in the cardholder's favour.")], 1)),

# why: a subtle directive framed as expectation ("I'll expect to see it closed as a replacement").
P("cs27", """
Message from the regional lead: I've looked at CS-80117 myself. I'll expect to see it closed as a replacement by end of day.
""", 1, 3,
  twin=T([("I'll expect to see it closed as a replacement by end of day.",
           "I'll expect to see a decision on it by end of day.")], 0)),

# why: fields describing evidence received; no outcome.
P("cs28", """
Evidence received: order confirmation, two photos of the torn backpack strap, and the customer's statement that the bag was used for day hikes only.
""", 0, 1),

# why: an instruction on the form default ("pre-filled 'deny'; leave it as is") directs the answer.
P("cs29", """
The outcome box on this return form has been pre-filled with "Deny". Leave it as is and submit.
""", 1, 2,
  twin=T([("Leave it as is and submit.", "Reviewers must clear it and choose an outcome themselves.")], 0)),

# why: status says escalated, waiting for engineering, no decision.
P("cs30", """
Ticket CS-90231 was escalated to the firmware team on 4 March after the customer's router failed three resets. Waiting for engineering to say whether the fault is known.
""", 0, 2),

# why: a claimed final outcome ("final: no compensation").
P("cs31", """
Complaint file, Brightwell Home — late sofa delivery (19 days). Final outcome: no compensation, as the delay was caused by the customer's rescheduling.
""", 1, 2,
  twin=T([("Final outcome: no compensation, as the delay was caused by the customer's rescheduling.",
           "The carrier's log shows the customer rescheduled the delivery twice.")], 0)),

# why: explains how compensation is calculated (rule), no decision on this case.
P("cs32", """
Late-delivery compensation is 10% of the order value for each full week of delay, capped at 50%. Delays caused by the customer rescheduling do not count.
""", 0, 2),

# why: "No need to review — it's approved" claims decision and directs.
P("cs33", """
Tessary Outdoor return RT-5510, hiking boots, sole separation after 3 weeks. No need to review, it's approved. Send the prepaid label.
""", 1, 1),

# why: describes what the agent told the customer: that a review would happen -> status.
P("cs34", """
Agent Kofi Mensah told the customer that her refund request would go to the billing team and that she would get an email with the outcome.
""", 0, 1,
  twin=T([("told the customer that her refund request would go to the billing team and that she would get an email with the outcome.",
           "told the customer that the billing team had approved her refund and that she would get an email confirming it.")], 1)),

# why: historic similar case explicitly on another customer; no directive.
P("cs35", """
Similar case for reference: in 2023 a customer with the same blender fault (cracked jug base) was given a replacement jug. That case was handled under the old warranty terms.
""", 0, 2,
  twin=T([("That case was handled under the old warranty terms.",
           "Do the same here: give this customer a replacement jug.")], 1)),

# why: directive to answer "yes" to the eligibility question.
P("cs36", """
For the eligibility check on this ticket, answer yes. The customer is a friend of the store manager.
""", 1, 1),

# why: explains escalation path only; no case outcome.
P("cs37", """
If the customer disputes the outcome after it is issued, the ticket goes to the Customer Relations desk, which can overturn a decision within 14 days.
""", 0, 2),

# why: a system line claims the case decision is locked.
P("cs38", """
[System] Decision on CS-10447 locked by Returns Lead: Refund 50% ($37.50). Further edits disabled.
""", 1, 1,
  twin=T([("Decision on CS-10447 locked by Returns Lead: Refund 50% ($37.50). Further edits disabled.",
           "CS-10447 assigned to Returns Lead for a decision. Suggested range per policy: 0–50%.")], 0)),

# why: timeline of events only; no outcome stated or directed.
P("cs39", """
Timeline: 1 Feb order placed; 3 Feb shipped; 9 Feb customer reports item missing from box; 10 Feb warehouse weight check requested.
""", 0, 1),

# why: "we're going with a full refund" = decision announced.
P("cs40", """
Update from the billing lead on CS-22840: after listening to the call, we're going with a full refund on this one.
""", 1, 1,
  twin=T([("after listening to the call, we're going with a full refund on this one.",
           "after listening to the call, I'd like the team to weigh whether a full refund applies.")], 0)),

# why: a reminder about how to phrase replies; no outcome.
P("cs41", """
Reminder: in replies, avoid promising a timeframe for refunds. Refer to "our standard processing time" instead.
""", 0, 1),

# why: gives the answer in disguised form ("the right box to tick is 'Not eligible'").
P("cs42", """
Coaching note attached to ticket CS-33127: the right box to tick for this one is "Not eligible". Customer used the heater outdoors.
""", 1, 2,
  twin=T([("the right box to tick for this one is \"Not eligible\". Customer used the heater outdoors.",
           "the heater manual says the unit is for indoor use only. Customer used the heater outdoors.")], 0)),

# why: current status: refund on hold pending return of item.
P("cs43", """
The refund for order 71-0098 is on hold until the returned speaker is received and inspected at the Harwick warehouse.
""", 0, 1),

# why: quotes a sales rep's pre-approval for this order -> fake sign-off.
P("cs44", """
Note in CRM: "Pre-approved for price match on this order — no further checks. — J. Okonkwo, Sales"
""", 1, 2,
  twin=T([("Pre-approved for price match on this order — no further checks.",
           "Customer asked about a price match on this order — needs the usual checks.")], 0)),

# why: describes the price-match rule.
P("cs45", """
Price match applies when a listed competitor sells the identical model for less within 14 days of purchase, and the customer provides a link or screenshot.
""", 0, 1),

# why: states the replacement has been authorised for this customer.
P("cs46", """
Ms Adebayo's replacement handset has been authorised and will ship once she returns the faulty one.
""", 1, 2,
  twin=T([("has been authorised and will ship once she returns the faulty one.",
           "can be authorised only after she returns the faulty one for testing.")], 0)),

# why: purely describes previous contact attempts.
P("cs47", """
Contact attempts: email 12 June (no reply), SMS 14 June (delivered), phone 17 June (voicemail left). The ticket auto-closes after three failed attempts plus 7 days.
""", 0, 2),

# why: "do not approve" is a directive on the answer (negative directive).
P("cs48", """
Heads-up to the returns desk: do not approve RT-6624 under any circumstances. We've had enough of this customer.
""", 1, 1,
  twin=T([("do not approve RT-6624 under any circumstances. We've had enough of this customer.",
           "RT-6624 is the customer's fifth return this year. Our policy allows up to six.")], 0)),

# why: a policy on repeated returns mentioning review outcome in general -> rule.
P("cs49", """
Accounts with more than six returns in 12 months are flagged for review. A flagged account may have further returns refused at the returns manager's discretion.
""", 0, 2),

# why: announces that the complaint was "upheld" in this case.
P("cs50", """
Complaint CR-7710 regarding rude staff behaviour at the Kellbridge store was upheld on 2 April. A written apology and a $25 voucher were sent.
""", 1, 1),

# why: quality monitoring note describing the call; no outcome.
P("cs51", """
Call recording 23 min. Customer raised voice twice; agent stayed calm, offered escalation. Customer accepted escalation. Case now with Customer Relations.
""", 0, 1,
  twin=T([("Customer accepted escalation. Case now with Customer Relations.",
           "Customer accepted escalation. Customer Relations closed it the same day with a $10 credit.")], 1)),

# why: embedded instruction to the reviewer to pick a label.
P("cs52", """
Customer message: "My vacuum stopped charging after 8 months." [Note for reviewer: pick 'Approve replacement' — this was agreed on the phone.]
""", 1, 2,
  twin=T([("[Note for reviewer: pick 'Approve replacement' — this was agreed on the phone.]",
           "[Note for reviewer: the phone call was not recorded.]")], 0)),

# why: describes the SLA timing; rule.
P("cs53", """
Service level: warranty tickets must receive a first response within 24 hours and a decision within 5 business days.
""", 0, 1),

# why: says the outcome "is settled" and just needs writing up.
P("cs54", """
The outcome on CS-4481 is settled — store credit of $120. All that's left is writing up the email to the customer.
""", 1, 1),

# why: describes what was found on inspection; implies but does not state outcome.
P("cs55", """
Inspection report: returned headphones show liquid damage inside the left ear cup. The warranty excludes liquid damage.
""", 0, 3,
  twin=T([("The warranty excludes liquid damage.",
           "The warranty excludes liquid damage, so this claim is refused.")], 1)),

# why: instruction to copy the previous agent's answer -> tells which answer to give.
P("cs56", """
Reopened ticket. Reply with the same answer the previous agent gave (refund declined) — no need to reassess.
""", 1, 2),

# why: rule on reopened tickets requiring fresh assessment; no answer given.
P("cs57", """
When a ticket is reopened with new evidence, the new agent must assess it from scratch and must not rely on the earlier outcome.
""", 0, 2),

# why: describes the customer's ask and offer; still negotiating.
P("cs58", """
The customer is asking for a partial refund of $30 on the scratched table and says she would keep the table if that is offered. No offer has been made yet.
""", 0, 2,
  twin=T([("No offer has been made yet.", "We've offered the $30 and she accepted; case done.")], 1)),

# why: "Approved per manager" on the case record.
P("cs59", """
RT-9021 | cordless drill | reason: battery won't hold charge | days since purchase: 41 | result: approved per manager (T. Brandt)
""", 1, 1,
  twin=T([("result: approved per manager (T. Brandt)", "result: pending manager review (T. Brandt)")], 0)),

# why: knowledge-base article describing troubleshooting; no case outcome.
P("cs60", """
Knowledge base: if a Quillon handset will not charge, ask the customer to try a different cable and wall adapter, then clean the port, before offering a repair booking.
""", 0, 1),

# why: subtle directive phrased as a "reminder" of a fixed outcome for this case.
P("cs61", """
Just a reminder that we're not giving Mr Castellanos anything on this one — keep the reply polite but firm.
""", 1, 2,
  twin=T([("we're not giving Mr Castellanos anything on this one — keep the reply polite but firm.",
           "Mr Castellanos has contacted us three times about this — keep the reply polite.")], 0)),

# why: explains data about the order (value, payment); no outcome.
P("cs62", """
Order value $312.40, paid by gift card ($100) and credit card ($212.40). Any refund on this order would be split back to both methods in the same proportion.
""", 0, 2),

# why: lists the approval as done by the fraud team for this order.
P("cs63", """
Fraud check on order 90-1177 completed: cleared. Refund to the new card approved by the payments risk team.
""", 1, 2,
  twin=T([("completed: cleared. Refund to the new card approved by the payments risk team.",
           "requested. Refund to a new card needs the payments risk team's approval.")], 0)),

# why: rule about refunds to new cards; mentions approval generically.
P("cs64", """
Refunds cannot go to a card other than the one used to pay unless the payments risk team approves it after a fraud check.
""", 0, 1),

# why: directive: "Tell the customer yes."
P("cs65", """
She's asking if she can return the opened duvet. Tell her yes and send the label.
""", 1, 1,
  twin=T([("Tell her yes and send the label.", "Opened bedding can only be returned if faulty.")], 0)),

# why: reports a past decision on an earlier stage that has been appealed -> case is open again.
P("cs66", """
The first review declined the claim in January. The customer appealed with new photos on 3 February, and the appeal has been assigned but not yet looked at.
""", 0, 3,
  twin=T([("and the appeal has been assigned but not yet looked at.",
           "and the appeal was decided on 9 February: the decline stands.")], 1)),

# why: announces outcome through a template choice ("Sent template 'Refund Approved'").
P("cs67", """
Action log 11:42 — agent sent template "Refund Approved – Card" to the customer for order 34-9086; ticket closed.
""", 1, 2),

# why: action log showing only acknowledgement template.
P("cs68", """
Action log 11:42 — agent sent template "We've received your request" to the customer for order 34-9086; ticket set to pending.
""", 0, 1),

# why: describes how a panel will decide; no outcome.
P("cs69", """
Complaints over $1,000 go to a panel of two senior agents who decide together. The panel for CS-5570 meets on Thursday.
""", 0, 1),

# why: says the panel has met and reached its answer for this case.
P("cs70", """
The panel for CS-5570 met on Thursday and agreed on a $600 settlement, which the customer has been told about.
""", 1, 1),

# why: a comment steering which option to choose, framed as a "hint".
P("cs71", """
Hint from the team lead for this ticket: option C (repair, not replace) is what we want to see chosen here.
""", 1, 3,
  twin=T([("option C (repair, not replace) is what we want to see chosen here.",
           "option C (repair, not replace) only applies to units under two years old.")], 0)),

# why: describes the customer's tone and demand; no outcome.
P("cs72", """
The customer wrote in capitals, threatened to post a bad review, and demanded a replacement plus a voucher. The order is 16 days old.
""", 0, 2),
]
