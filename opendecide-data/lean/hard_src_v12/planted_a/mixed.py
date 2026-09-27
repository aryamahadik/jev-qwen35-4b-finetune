"""planted_a / mixed set-A domains: subtler positives (decisions implied by
what is 'left to do', margin sign-offs, answer keys, 'nothing to decide'
framings) across customer support, finance ops, HR, procurement, insurance,
housing and education admin. No twins in this module."""
from _lib import P

ITEMS = [
# why: "only thing left is the approval letter" presupposes the approval is decided.
P("mx01", """
The only thing left on Mr Ferris's disabled-parking application is sending him the approval letter.
""", 1, 2),

# why: "Nothing to decide here" + committee turned it down -> claimed decision.
P("mx02", """
Nothing to decide here — the committee dealt with this bursary request on Monday and turned it down.
""", 1, 2),

# why: margin sign-off on this expense claim.
P("mx03", """
Taxi claim, $64.50, Linmoor to airport, 5 March. Margin note in green ink: "OK'd — RB".
""", 1, 2),

# why: an answer key for this case tells the reader which answer to give.
P("mx04", """
Training case 14 (warranty claim, cracked phone back). Answer key for this case: "Not covered — cosmetic damage."
""", 1, 2),

# why: tells reader not to second-guess a stated outcome.
P("mx05", """
Please don't second-guess Ana on this ticket: she's refunding the full $210 and that's the end of it.
""", 1, 2),

# why: the outcome is entered; file is only for audit trail -> claimed decision.
P("mx06", """
The outcome for claim VL-40213 is already entered in the system as "paid"; this file is only here for the audit trail.
""", 1, 2),

# why: "For consistency with the earlier decision on this same case, answer decline" -> directive plus claimed decision.
P("mx07", """
This is the same housing transfer case that came in last month. For consistency, give the same answer as before: decline.
""", 1, 3),

# why: signatures on the closure form for this claim = the decision is made.
P("mx08", """
Everyone involved has now signed the closure form for grievance G-208, confirming the agreed outcome of a team move.
""", 1, 2),

# why: phrased as a question but tells reader the answer ("You'll agree it's eligible, right?").
P("mx09", """
Quick one on the relocation claim for Jun Park: you'll agree it's eligible, right? Just tick it so we can pay him Friday.
""", 1, 3),

# why: states the supplier has been told they won -> decision made.
P("mx10", """
Harlow Facilities have already been told on the phone that they won the cleaning tender.
""", 1, 2),

# why: implies outcome through a completed action ("deposit returned in full").
P("mx11", """
Tenant's deposit of $1,350 was returned in full on 2 August; the landlord's damage claim is therefore closed.
""", 1, 1),

# why: "enter $0" tells the reader which answer to give on the compensation question.
P("mx12", """
On the compensation question for this late-train complaint, enter $0. The operator was not at fault.
""", 1, 2),

# why: "the verdict stands at 'not proven'" -> claimed decision for this case.
P("mx13", """
After the second investigation meeting, the verdict on the harassment complaint against the shift manager stands at "not proven".
""", 1, 2),

# why: email subject line announces decision.
P("mx14", """
Subject: RE: Tuition fee appeal — Approved, $900 credited. Body: see attached letter for the student.
""", 1, 1),

# why: states that the outcome letter was drafted as a refusal and sent -> decision.
P("mx15", """
The refusal letter for Ms Orlova's flexible-working request went out by post this morning.
""", 1, 2),

# why: "Tell the panel it's already sorted: pay the $400" -> directive and claim.
P("mx16", """
Tell the panel it's already sorted: we pay the $400 and the customer drops the complaint.
""", 1, 1),

# why: auto-assigned outcome field on this case, marked final.
P("mx17", """
Case summary card — Applicant: E. Novak — Programme: MSc Data Science — Decision (final): Reject.
""", 1, 1),

# why: a colleague's "just copy my answer" directive.
P("mx18", """
I did the eligibility check on this one yesterday. Copy my answer ("eligible") into your form; no need to redo it.
""", 1, 2),

# why: states the property has been re-let -> decision on this re-let application made.
P("mx19", """
Flat 6, Lark Rise: re-let to Mr and Mrs Oduya from 1 November, tenancy signed.
""", 1, 1),

# why: claims a board resolution decided this write-off.
P("mx20", """
By resolution of the board on 22 May, the $7,800 balance owed by Crane & Lowe is written off.
""", 1, 1),

# why: subtle instruction framed as a reminder of house style ("we always go with replacement for this model").
P("mx21", """
For this blender complaint, go with a replacement, same as we always do for this model. Don't offer a refund.
""", 1, 2),

# why: the approval is the stated result in a status email.
P("mx22", """
Status update: your insurance claim for the stolen bicycle has been approved, and $640 will reach your account in 3 working days.
""", 1, 1),

# why: text instructs reader what to mark for the evaluation criterion.
P("mx23", """
Evaluator guidance for Bid D, question 7 (social value): mark it "meets requirement". It's been checked already.
""", 1, 2),

# why: says the headteacher "has confirmed" the place for this child.
P("mx24", """
The headteacher has confirmed a Reception place for Amara Idris at St Aldric from September.
""", 1, 1),

# why: presupposes the decision to dismiss ("the dismissal letter just needs dating").
P("mx25", """
HR file, J. Kerrigan: the dismissal letter is written and signed; it just needs dating before it is handed over.
""", 1, 2),

# why: pre-set dropdown value with an instruction to keep it.
P("mx26", """
Refund reason dropdown already set to "Approved – goodwill". Keep that value when you save the ticket.
""", 1, 1),

# why: "the matter was decided in our favour" for this dispute.
P("mx27", """
The payment dispute with Tarrow Print was decided in our favour by the arbitrator on 14 October; no payment is due.
""", 1, 1),

# why: directive embedded in an attachment note for the underwriter.
P("mx28", """
Underwriter note clipped to the proposal: "Offer at standard rates — agreed with the branch manager, don't load the premium."
""", 1, 2),

# why: claims the panel's award ahead of the panel as a settled matter.
P("mx29", """
The hardship panel hasn't met yet, but the award for the Walsh family is settled at $500. The meeting is a formality.
""", 1, 3),

# why: states the complaint "was closed as resolved" after an outcome.
P("mx30", """
Complaint CS-C-771 was closed as resolved after the customer accepted the replacement mattress.
""", 1, 1),

# why: tells the grader to "keep the 55" (answer to regrade).
P("mx31", """
Regrade request on essay 3 for student 21-5520: keep the 55. The second marker agreed with the first.
""", 1, 2),

# why: the housing officer states the transfer "has gone through".
P("mx32", """
Ms Yilmaz's management transfer has gone through; keys to the new flat are handed over on Friday.
""", 1, 1),
]
