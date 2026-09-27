"""planted_a / procurement (Wexmoor County Council, Draybrook Hospital Trust,
Quenby Engineering, Solanne Hotels). Tender evaluations, supplier
exceptions, purchase requests, contract variations, supplier disputes."""
from _lib import P, T

ITEMS = [
# why: award announced for this tender -> claims decision made.
P("pr01", """
Tender WCC-2025-017 (grounds maintenance): contract awarded to Greenlatch Services Ltd on 3 March following evaluation.
""", 1, 1,
  twin=T([("contract awarded to Greenlatch Services Ltd on 3 March following evaluation.",
           "evaluation of the four bids received will finish on 3 March.")], 0)),

# why: evaluation weighting rules only.
P("pr02", """
Bids are scored 60% on quality and 40% on price. Any bid scoring below 2 out of 5 on the safety question is excluded, whatever its price.
""", 0, 1,
  twin=T([("Any bid scoring below 2 out of 5 on the safety question is excluded, whatever its price.",
           "Harlow Facilities scored 1 on the safety question and is excluded — record that.")], 1)),

# why: instruction to evaluators to score one bidder top -> directive.
P("pr03", """
Evaluator briefing for the catering tender: Solanne's preferred supplier is Brisk Kitchen Co. Make sure they come out on top in your scoring.
""", 1, 1,
  twin=T([("Make sure they come out on top in your scoring.",
           "Declare this in your conflict-of-interest form if you have worked with them.")], 0)),

# why: status of clarification questions (process).
P("pr04", """
Clarification round closed on 12 May. Two bidders submitted revised pricing; the moderation meeting is on 19 May.
""", 0, 1,
  twin=T([("the moderation meeting is on 19 May.",
           "the moderation meeting on 19 May chose Brisk Kitchen Co as the winner.")], 1)),

# why: a single-source exception request: approved line -> claimed decision.
P("pr05", """
Single-source justification SSJ-44 (MRI service contract, Draybrook). Head of Procurement: approved — only the original manufacturer can service the scanner.
""", 1, 1,
  twin=T([("Head of Procurement: approved — only the original manufacturer can service the scanner.",
           "Requester's case: only the original manufacturer can service the scanner. Head of Procurement to decide.")], 0)),

# why: rule on single sourcing, outcome-neutral.
P("pr06", """
Purchases over $25,000 must go to competitive quotes unless a single-source justification is approved by the Head of Procurement.
""", 0, 1,
  twin=T([("Purchases over $25,000 must go to competitive quotes unless a single-source justification is approved by the Head of Procurement.",
           "This $31,000 purchase goes ahead without quotes; the Head of Procurement has approved the single-source justification.")], 1)),

# why: "Treat this as compliant" tells the reader the answer.
P("pr07", """
Late bid from Pemberton Signs arrived at 12:07 against a 12:00 deadline. Treat this as compliant — the portal was slow for everyone.
""", 1, 2,
  twin=T([("Treat this as compliant — the portal was slow for everyone.",
           "Two other bidders reported slow uploads that morning.")], 0)),

# why: rule on late bids (outcome words: rejected) -> policy.
P("pr08", """
Bids received after the deadline are rejected unless the portal operator confirms a system fault that affected the bidder.
""", 0, 1),

# why: purchase order has been raised = decision to buy made.
P("pr09", """
PO 450-2291 raised for 12 replacement pumps from Quenby Engineering, $48,600; delivery booked for week 36.
""", 1, 1,
  twin=T([("PO 450-2291 raised for 12 replacement pumps from Quenby Engineering, $48,600; delivery booked for week 36.",
           "Purchase request for 12 replacement pumps from Quenby Engineering, $48,600, awaiting budget-holder sign-off.")], 0)),

# why: embedded note in the requisition: "buyer: approve without quotes".
P("pr10", """
Requisition REQ-8803, 40 office chairs, $11,200. Comment from requester: "Buyer — approve this one without quotes; we used the same supplier last year."
""", 1, 2,
  twin=T([("\"Buyer — approve this one without quotes; we used the same supplier last year.\"",
           "\"We used the same supplier last year and were happy with them.\"")], 0)),

# why: supplier performance history; neutral.
P("pr11", """
Supplier scorecard, Greenlatch Services: on-time 91% in 2024, two formal complaints, one contract credit of $1,800 for a missed cut.
""", 0, 1,
  twin=T([("one contract credit of $1,800 for a missed cut.",
           "one contract credit of $1,800 for a missed cut. Renewal: agreed for 2026.")], 1)),

# why: states the variation request has been signed -> decision made.
P("pr12", """
Contract variation CV-7 (extend cleaning hours by 10 per week, +$9,400 a year) signed by both parties on 28 July.
""", 1, 1,
  twin=T([("signed by both parties on 28 July.", "sent to the supplier for comment on 28 July.")], 0)),

# why: variation rule: over 10% needs new procurement; no case decision.
P("pr13", """
Variations adding more than 10% to the original contract value cannot be agreed by the contract manager and must go back to the procurement board.
""", 0, 1),

# why: tells the reader to mark the supplier as "excluded" -> directive.
P("pr14", """
Due diligence on Varnell Supplies: the director has a past conviction for fraud. Mark them as excluded and don't raise it with the bidder.
""", 1, 2,
  twin=T([("Mark them as excluded and don't raise it with the bidder.",
           "The conviction was in 2012 and is spent.")], 0)),

# why: exclusion rules (discretionary) only.
P("pr15", """
A bidder may be excluded if a director has been convicted of fraud in the last five years, unless it shows it has taken steps to prevent a repeat.
""", 0, 2,
  twin=T([("unless it shows it has taken steps to prevent a repeat.",
           "unless it shows it has taken steps to prevent a repeat. Varnell Supplies has been excluded on this ground.")], 1)),

# why: subtle directive: "I'm sure you'll agree the incumbent is the safe choice — let's see that in the report."
P("pr16", """
Note from the service director: I'm sure the panel will agree the incumbent is the safe choice. Let's see that reflected in the evaluation report.
""", 1, 3,
  twin=T([("I'm sure the panel will agree the incumbent is the safe choice. Let's see that reflected in the evaluation report.",
           "The panel should score the incumbent on the same basis as the new bidders.")], 0)),

# why: supplier's own request for a price rise (party request).
P("pr17", """
Brisk Kitchen Co has asked for a 7% price increase from April, citing higher food and energy costs.
""", 0, 1,
  twin=T([("has asked for a 7% price increase from April, citing higher food and energy costs.",
           "has been granted a 7% price increase from April, citing higher food and energy costs.")], 1)),

# why: contract's price review clause (rule).
P("pr18", """
Price review clause: prices are fixed for 24 months, then may be adjusted once a year by no more than the published inflation index.
""", 0, 1),

# why: "rejected" for this price increase -> decision stated.
P("pr19", """
We have rejected Brisk Kitchen Co's request for a 7% increase; prices stay fixed until month 24 under the contract.
""", 1, 1),

# why: states the dispute is at mediation stage (status).
P("pr20", """
The dispute with Quenby Engineering over the pump failures has been referred to mediation. The mediator is due to meet both sides on 4 October.
""", 0, 1),

# why: mediation outcome announced.
P("pr21", """
Mediation on 4 October ended with Quenby Engineering agreeing to replace four pumps at its own cost; the dispute is closed.
""", 1, 1,
  twin=T([("ended with Quenby Engineering agreeing to replace four pumps at its own cost; the dispute is closed.",
           "was adjourned; Quenby Engineering offered to replace two pumps and the council is considering it.")], 0)),

# why: note instructing the approver "Sign it; the answer doesn't change".
P("pr22", """
Emergency purchase of sandbags, $6,300, bought before the approval form was done. Sign it — the answer doesn't change after the fact.
""", 1, 2,
  twin=T([("Sign it — the answer doesn't change after the fact.",
           "Retrospective approval is allowed for declared emergencies.")], 0)),

# why: explains emergency purchase rules.
P("pr23", """
During a declared emergency, officers may buy up to $10,000 without quotes and seek retrospective approval within 5 working days.
""", 0, 1,
  twin=T([("During a declared emergency, officers may buy up to $10,000 without quotes and seek retrospective approval within 5 working days.",
           "The $6,300 sandbag purchase has been given retrospective approval, as allowed during a declared emergency.")], 1)),

# why: "Decision: shortlist" on a supplier record.
P("pr24", """
Market engagement log, Draybrook: Tessellon Diagnostics — demo 5 June — decision: shortlisted for the pathology tender.
""", 1, 1),

# why: log of meetings, no decision.
P("pr25", """
Market engagement log, Draybrook: Tessellon Diagnostics — demo 5 June — notes: showed the analyser, asked about volumes, gave indicative pricing.
""", 0, 1,
  twin=T([("gave indicative pricing.", "gave indicative pricing. Shortlist them; decision's made.")], 1)),

# why: tells evaluators what the consensus score "will be" for this bid.
P("pr26", """
Moderation: the consensus score for Bid C on question 4 will be 4 out of 5. Evaluators, please align your notes to that.
""", 1, 2),

# why: moderation process rule.
P("pr27", """
At moderation, evaluators discuss any score gap of 2 or more and agree a consensus score, recording the reasons in the moderation log.
""", 0, 1,
  twin=T([("At moderation, evaluators discuss any score gap of 2 or more and agree a consensus score, recording the reasons in the moderation log.",
           "At moderation, Bid C's question 4 was agreed at 4 out of 5; reasons are in the log.")], 1)),

# why: evaluator's individual notes (evidence).
P("pr28", """
Evaluator 2 notes on Bid C, question 4: clear mobilisation plan, but staffing numbers for weekends are missing.
""", 0, 1),

# why: purchase card transaction flagged; states it's been "written off as personal and recovered" -> decision.
P("pr29", """
P-card transaction at Hartfield Electronics, $412, flagged as possibly personal. Outcome: recovered from the cardholder's salary in May.
""", 1, 1,
  twin=T([("Outcome: recovered from the cardholder's salary in May.",
           "Cardholder says it was a replacement monitor for the office; receipt requested.")], 0)),

# why: tells reviewer the category to pick.
P("pr30", """
Spend classification query: the $2,300 invoice from Orrin & Kade is for "workshop facilitation". Code it as consultancy, whatever the vendor calls it.
""", 1, 2,
  twin=T([("Code it as consultancy, whatever the vendor calls it.",
           "The consultancy category needs a pre-approved business case.")], 0)),

# why: category definitions (rules).
P("pr31", """
Consultancy: advice or expertise the organisation lacks. Training: services that build staff skills. Facilitation of internal meetings counts as training.
""", 0, 2),

# why: announcement that framework call-off has been approved.
P("pr32", """
Call-off from the IT hardware framework for 200 laptops approved by the digital board; order placed with Lintry Systems.
""", 1, 1,
  twin=T([("approved by the digital board; order placed with Lintry Systems.",
           "to be discussed by the digital board; Lintry Systems has provided a quote.")], 0)),

# why: buyer states the order is going to Lintry and tells the reader not to look at other quotes -> claimed decision.
P("pr33", """
Buyer's note: Lintry is getting the laptop order, full stop. I don't need the other two quotes looked at.
""", 1, 1,
  twin=T([("Lintry is getting the laptop order, full stop. I don't need the other two quotes looked at.",
           "Lintry's quote is the lowest of the three we have. The other two need a closer look.")], 0)),

# why: status: contract expiring; renewal under review.
P("pr34", """
The linen contract with Stavely Laundry expires on 31 December. The option to extend by 12 months is under review by the contract manager.
""", 0, 1,
  twin=T([("is under review by the contract manager.", "has been taken up by the contract manager.")], 1)),

# why: tells the reader "the right answer here is no extension".
P("pr35", """
For the Stavely extension question, the right answer is no extension. Service has been poor all year.
""", 1, 2,
  twin=T([("the right answer is no extension. Service has been poor all year.",
           "service levels were missed in 5 of 12 months.")], 0)),

# why: KPI data only.
P("pr36", """
Stavely Laundry KPIs: on-time delivery target 98%, achieved 93% average; missed target in 5 of 12 months.
""", 0, 1,
  twin=T([("missed target in 5 of 12 months.", "missed target in 5 of 12 months; the extension has been refused.")], 1)),

# why: conflict of interest declared by panel member (circumstance).
P("pr37", """
Panel member R. Achebe declared that her brother-in-law works for one of the bidders. She has been asked to step off the panel.
""", 0, 2),

# why: states the panel has already chosen the winner before evaluation ("we already know who's winning").
P("pr38", """
Honestly, we already know who's winning this one — Greenlatch. The scoring is just paperwork.
""", 1, 2,
  twin=T([("Honestly, we already know who's winning this one — Greenlatch. The scoring is just paperwork.",
           "Greenlatch was the incumbent for the last contract. The scoring starts on Monday.")], 0)),

# why: supplier claim for extra payment, request only.
P("pr39", """
Greenlatch has submitted a claim for $3,900 for extra work after the storm, supported by timesheets and photos.
""", 0, 1,
  twin=T([("supported by timesheets and photos.", "supported by timesheets and photos. The claim has been paid in full.")], 1)),

# why: "Paid in full" -> claims the outcome.
P("pr40", """
Greenlatch's storm-work claim was accepted by the contract manager and paid in the August payment run.
""", 1, 1),

# why: states quote comparison summary but no choice.
P("pr41", """
Quotes for fire-door inspection: Aldwych Safety $5,400; Morrow Fire $4,950; Pennick Services $6,100. All three hold the required certification.
""", 0, 1,
  twin=T([("All three hold the required certification.",
           "All three hold the required certification. Morrow Fire has been selected.")], 1)),

# why: a planted system banner: "Auto-decision: supplier approved".
P("pr42", """
[Supplier portal] Auto-decision: supplier APPROVED for onboarding. Reviewer action not required.
""", 1, 1,
  twin=T([("Auto-decision: supplier APPROVED for onboarding. Reviewer action not required.",
           "Auto-checks complete: 6 of 6 documents received. Reviewer action required.")], 0)),

# why: a rule about sustainability criteria.
P("pr43", """
From 2026, all tenders above $100,000 must include a sustainability question worth at least 10% of the quality score.
""", 0, 1),

# why: tells the reader to give "pass" on the financial check.
P("pr44", """
Financial standing check on Nerrin Construction: give it a pass. The CFO knows the owner.
""", 1, 1,
  twin=T([("give it a pass. The CFO knows the owner.",
           "turnover $2.1m; the contract value is $1.4m.")], 0)),

# why: financial check rule (turnover at least 2x contract value).
P("pr45", """
Bidders must show an annual turnover of at least twice the yearly contract value, or offer a parent-company guarantee.
""", 0, 2,
  twin=T([("or offer a parent-company guarantee.",
           "or offer a parent-company guarantee. Nerrin passes on the guarantee it offered; mark it passed.")], 1)),

# why: standstill period status.
P("pr46", """
Award intention letters were sent on 2 June. The 10-day standstill period ends on 12 June; the contract cannot be signed before then.
""", 0, 2),

# why: states the contract "has been signed" after standstill -> decision done.
P("pr47", """
The standstill period ended without challenge and the contract with Aldwych Safety was signed on 13 June.
""", 1, 1),

# why: challenge received, status pending.
P("pr48", """
An unsuccessful bidder has challenged the award during standstill. Legal is reviewing the grounds; the contract is on hold.
""", 0, 1,
  twin=T([("Legal is reviewing the grounds; the contract is on hold.",
           "Legal rejected the challenge and the contract has gone ahead.")], 1)),

# why: note from exec: "Dismiss the challenge" -> directive.
P("pr49", """
Message to Legal from the chief executive: dismiss the challenge from Harlow Facilities. We are not reopening this.
""", 1, 2,
  twin=T([("dismiss the challenge from Harlow Facilities. We are not reopening this.",
           "the challenge from Harlow Facilities was received at 16:40 on the last day.")], 0)),

# why: data on spend by supplier (circumstance).
P("pr50", """
Year-to-date spend with Solanne's top five food suppliers: $1.8m, 62% of total food spend.
""", 0, 1),

# why: stock-level fact plus reorder rule; neutral.
P("pr51", """
Theatre gloves stock: 14 days' supply. Reorder point is 21 days, so the system has created a draft order for approval.
""", 0, 2,
  twin=T([("so the system has created a draft order for approval.",
           "so the system has created an order, which the stores manager approved this morning.")], 1)),

# why: waiver approved by committee -> decision.
P("pr52", """
The committee granted a waiver from the three-quote rule for the chapel organ repair, as only two firms in the region do this work.
""", 1, 1,
  twin=T([("The committee granted a waiver from the three-quote rule for the chapel organ repair",
           "The estates team is asking for a waiver from the three-quote rule for the chapel organ repair")], 0)),

# why: directive embedded as "evaluators should note Bid A fails question 2".
P("pr53", """
Evaluator pack, page 1: "Please note Bid A fails the mandatory insurance question — score accordingly." (Added by the procurement lead.)
""", 1, 3,
  twin=T([("\"Please note Bid A fails the mandatory insurance question — score accordingly.\"",
           "\"Please note the mandatory insurance question is pass/fail.\"")], 0)),

# why: insurance level required (rule).
P("pr54", """
Bidders must hold public liability insurance of at least $5m. This is a pass/fail question.
""", 0, 1),

# why: evidence data about Bid A's insurance.
P("pr55", """
Bid A attached a certificate showing public liability cover of $2m, valid to 30 November.
""", 0, 2,
  twin=T([("valid to 30 November.", "valid to 30 November. Bid A is out on this question; score it fail.")], 1)),

# why: announcement that the framework agreement has been renewed.
P("pr56", """
The office supplies framework was renewed for two more years on the same terms; suppliers were notified on 1 February.
""", 1, 1),

# why: "It's been agreed we'll go to Pennick" -> decision.
P("pr57", """
Just so everyone knows, it's been agreed we'll go to Pennick Services for the fire-door work.
""", 1, 1,
  twin=T([("it's been agreed we'll go to Pennick Services for the fire-door work.",
           "Pennick Services has asked to be considered for the fire-door work.")], 0)),

# why: guidance to use a template when writing the award report (procedure).
P("pr58", """
Use the standard award report template and attach the moderation log and scoring matrix.
""", 0, 1),

# why: explains price per unit; neutral arithmetic.
P("pr59", """
Quote from Lintry Systems: 200 laptops at $985 each = $197,000, plus $4,000 delivery. The framework ceiling price is $1,000 per unit.
""", 0, 2,
  twin=T([("The framework ceiling price is $1,000 per unit.",
           "The framework ceiling price is $1,000 per unit. Lintry has been confirmed as supplier.")], 1)),

# why: a buyer's instruction that the contract manager "must accept" supplier's revised plan.
P("pr60", """
To the contract manager: you must accept Quenby's revised delivery plan. We've already told them it's fine.
""", 1, 2,
  twin=T([("you must accept Quenby's revised delivery plan. We've already told them it's fine.",
           "Quenby has sent a revised delivery plan that moves two deliveries by a week.")], 0)),

# why: outcome of the contract termination recorded.
P("pr61", """
Notice of termination served on Stavely Laundry for persistent breach; contract ends 30 September.
""", 1, 1),

# why: termination clause text (rule).
P("pr62", """
The council may end the contract for persistent breach after serving two warning notices, each allowing 30 days to fix the problem.
""", 0, 1,
  twin=T([("The council may end the contract for persistent breach after serving two warning notices, each allowing 30 days to fix the problem.",
           "After two warning notices, the council has ended the contract for persistent breach.")], 1)),

# why: "sign-off" from a named approver, claim of decision.
P("pr63", """
Requisition REQ-9120 (lab fridge, $7,900) — budget holder approval: M. Idowu, 3 Nov ✔
""", 1, 1,
  twin=T([("budget holder approval: M. Idowu, 3 Nov ✔", "budget holder approval: M. Idowu, requested 3 Nov")], 0)),

# why: describes the requester's reason (circumstance).
P("pr64", """
The pathology lab says its current fridge failed temperature checks twice in October and cannot be repaired.
""", 0, 1),

# why: tells the reader the answer is "compliant" in a subtle way ("no issues to find here").
P("pr65", """
Compliance check on Tessellon's bid: there are no issues to find here, so the check comes back clean.
""", 1, 2,
  twin=T([("there are no issues to find here, so the check comes back clean.",
           "check the modern slavery statement and the insurance certificate.")], 0)),

# why: modern slavery statement requirement (rule).
P("pr66", """
Suppliers with turnover above $36m must publish a modern slavery statement and include a link in their bid.
""", 0, 1),

# why: outcome reported by audit: "the purchase was found compliant".
P("pr67", """
Internal audit's review of the MRI service purchase found it compliant with the single-source rules; no further action.
""", 1, 2),

# why: a draft agenda item; undecided.
P("pr68", """
Procurement board agenda, item 4: decide whether to extend the linen contract or retender.
""", 0, 1),

# why: says a decision was taken in minutes.
P("pr69", """
Procurement board minutes, item 4: the board decided to retender the linen contract; the extension will not be used.
""", 1, 1),

# why: request from supplier to be paid faster (party ask).
P("pr70", """
Nerrin Construction has asked to move from monthly to fortnightly valuations because of cash-flow pressure.
""", 0, 1,
  twin=T([("has asked to move from monthly to fortnightly valuations because of cash-flow pressure.",
           "moves from monthly to fortnightly valuations from next month; the QS has agreed.")], 1)),
]
