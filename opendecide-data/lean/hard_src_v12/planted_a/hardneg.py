"""planted_a / hard negatives that use decision vocabulary ('approved',
'already', 'decided') about other cases, earlier stages, rules or status,
across set-A domains. About half have twins that flip to a claimed decision."""
from _lib import P, T

ITEMS = [
# why: "already approved" refers to the customer's previous order, not this ticket.
P("hn01", """
The customer's refund on her previous order was already approved in May. This ticket is about a different order and has not been reviewed.
""", 0, 2,
  twin=T([("This ticket is about a different order and has not been reviewed.",
           "This ticket, about a different order, was approved the same day.")], 1)),

# why: approved budget line (a circumstance), not a decision on this purchase request.
P("hn02", """
The department's approved budget for training this year is $18,000, of which $11,400 is already committed.
""", 0, 2),

# why: an approved supplier list is a circumstance; the purchase is still to be decided.
P("hn03", """
Draywell Tools is already on the approved supplier list. The request to buy 30 drills from them is waiting for the budget holder.
""", 0, 2,
  twin=T([("The request to buy 30 drills from them is waiting for the budget holder.",
           "The budget holder has signed off the request to buy 30 drills from them.")], 1)),

# why: rule that says who decides; uses 'decided' generically.
P("hn04", """
Tenancy transfer requests are decided by the area housing manager, usually within 28 days of the home visit.
""", 0, 1),

# why: approved leave for another employee is history about a colleague; this request undecided.
P("hn05", """
Two colleagues in the same team already have approved leave for the week of 14 July. Sam's request for that week has just been submitted.
""", 0, 2,
  twin=T([("Sam's request for that week has just been submitted.",
           "Sam's request for that week has just been refused.")], 1)),

# why: the pre-approval was for a hotel under the cap; the question of the over-cap claim is open.
P("hn06", """
Travel was pre-approved for a hotel within the $180 cap. The employee's claim is for $240 a night and is now with the finance partner.
""", 0, 3,
  twin=T([("and is now with the finance partner.", "and the finance partner has paid it in full.")], 1)),

# why: explains the approval route (rule) with 'approved' as a condition.
P("hn07", """
Claims already approved by a line manager still go through a random 10% audit by the finance team.
""", 0, 2),

# why: the first stage is decided but the appeal is live -> status of an undecided case.
P("hn08", """
The student's first-stage appeal was decided in April. Her second-stage appeal, with new evidence, has been accepted for hearing in June.
""", 0, 3,
  twin=T([("has been accepted for hearing in June.", "was heard in June and dismissed.")], 1)),

# why: statement of past practice across many claims (history), not this claim.
P("hn09", """
Over the last two years, most storm claims from this postcode have been approved within a week.
""", 0, 2),

# why: 'already' refers to evidence received; nothing decided.
P("hn10", """
The policyholder has already sent the repair estimate and photos. The adjuster has not reviewed them yet.
""", 0, 1,
  twin=T([("The adjuster has not reviewed them yet.", "The adjuster has reviewed them and accepted the claim.")], 1)),

# why: quoting what the approval letter template says; template text, no case outcome.
P("hn11", """
The standard approval letter template says: "We are pleased to confirm that your application has been approved." Refusal letters use template R2.
""", 0, 3),

# why: the landlord's approval of a different request (decoration) is history; the pet request is open.
P("hn12", """
The landlord approved the tenant's request to repaint the lounge last year. Her new request, to keep a cat, arrived on 3 March.
""", 0, 2,
  twin=T([("Her new request, to keep a cat, arrived on 3 March.",
           "Her new request, to keep a cat, was approved on 3 March.")], 1)),

# why: a count of already-decided cases in a queue report; no decision on this case.
P("hn13", """
Queue report: 42 disputes decided this week, 17 still open. Dispute D-904 is one of the open ones.
""", 0, 2),

# why: 'already' + 'decided' about the date of a meeting, not the outcome.
P("hn14", """
It's already been decided that the scholarship interviews will be held online on 12 May.
""", 0, 3),
]
