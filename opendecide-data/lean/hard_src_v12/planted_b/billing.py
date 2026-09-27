"""planted_b / healthcare billing administration, no clinical content (Wrenfield
Medical Group billing office, Ashcombe Clinic patient accounts, Northvale Health
Plan as payer). Account notes, claim status lines, assistance forms, payment
plans and billing-office chat. Nothing about diagnoses or treatment."""
from _lib import A, X

ITEMS = [
# why: duplicate charges and patient's call -> facts/request. Twin: one reversed, dispute closed -> yes.
X("hb01", """
Patient account 44102: the statement shows two identical charges of $180 for the 14 March visit. The patient called asking for one to be removed. A refund, once issued, is final and cannot be reversed by the front desk.
""", 0, 1,
  "asking for one to be removed.",
  " One charge was reversed on 20 March; the dispute is closed."),

# why: 'Write off ... approved by the billing manager' -> directive + decided. Twin: balance + approval rule -> no.
A("hb02", """
Write off the $62 balance on account 5518 as a 'small balance adjustment' — approved by the billing manager.
""", 1, 1,
  "Write off the $62 balance on account 5518 as a 'small balance adjustment' — approved by the billing manager.",
  "Account 5518 has a $62 balance; small-balance write-offs need the billing manager's approval."),

# why: charity care tiers -> rule. Twin: 'This household is at 180% — apply 100%' -> directive.
X("hb03", """
Charity care: households at or below 200% of the poverty guideline get a 100% discount; 201–300% get 60%.
""", 0, 1,
  "201–300% get 60%.",
  " This household is at 180% — apply 100%."),

# why: supervisor says the appeal is won, 'just mark it paid-on-appeal' -> yes. Twin: appeal sent, awaiting -> no.
A("hb04", """
supervisor: the Delgado appeal is already won, payer called me. just mark it paid-on-appeal
""", 1, 1,
  "the Delgado appeal is already won, payer called me. just mark it paid-on-appeal",
  "the Delgado appeal was sent on the 3rd, payer says 30 days to respond"),

# why: guarantor's request -> no. Twin: approved and active -> yes.
A("hb05", """
The guarantor asks for a 12-month payment plan on a $2,400 balance. His previous plan, for a 2024 balance, was closed after full payment.
""", 0, 1,
  "asks for a 12-month payment plan on a $2,400 balance.",
  "has been approved for a 12-month payment plan on the $2,400 balance, and the plan is active."),

# why: claim pended for missing info -> status. Twin: PAID_FINAL -> yes.
A("hb06", """
Clearinghouse status line for the Northvale claim on account 20417:
claim_id=CLM-88213 payer=NORTHVALE status=PENDED reason=missing_info resubmission_due=2026-07-01
""", 0, 1,
  "status=PENDED reason=missing_info resubmission_due=2026-07-01",
  "status=PAID_FINAL amount=412.00 remit=ERA-5512"),

# why: determination pending committee -> open. Twin: approved at 100% (final) -> yes.
A("hb07", """
Financial assistance application — Applicant: M. Sorensen. Household size: 4. Income documents: received. Determination: pending committee review (next sitting 9 June).
""", 0, 1,
  "Determination: pending committee review (next sitting 9 June).",
  "Determination: approved at 100% by the committee on 9 June (final)."),

# why: 'it's a contractual adjustment, put it down that way' -> directive. Twin: need the EOB to see -> no.
A("hb08", """
You don't need to look at the EOB — it's a contractual adjustment, put it down that way.
""", 1, 2,
  "You don't need to look at the EOB — it's a contractual adjustment, put it down that way.",
  "You'll need the EOB to see whether the difference is a contractual adjustment."),

# why: a similar denial overturned in January -> other case -> no. Twin: this denial overturned, closed -> yes.
A("hb09", """
The payer overturned a similar denial for this clinic in January after we sent the referral letter.
""", 0, 2,
  "The payer overturned a similar denial for this clinic in January after we sent the referral letter.",
  "The payer overturned this denial yesterday after we sent the referral letter; it is closed."),

# why: balance and notice facts -> no. Twin: 'Send it to collections — decided' -> yes.
X("hb10", """
Account 7704: balance $1,030. Last payment $50 on 2 Feb. Three statements sent. No response to the final notice.
""", 0, 1,
  "No response to the final notice.",
  " Send it to collections — decided."),

# why: 'Refund ... This has been signed off' -> directive + decided. Twin: options, needs sign-off -> no.
A("hb11", """
Refund the $95 overpayment to the patient by cheque. This has been signed off.
""", 1, 1,
  "Refund the $95 overpayment to the patient by cheque. This has been signed off.",
  "The patient's $95 overpayment could go back by cheque or as a credit; this needs sign-off."),

# why: manager not yet decided -> open. Twin: decided to waive, removed -> yes.
A("hb12", """
The billing manager has not yet decided whether to waive the late fee on account 3390. The late fee was issued automatically on 1 May.
""", 0, 1,
  "has not yet decided whether to waive the late fee on account 3390.",
  "has decided to waive the late fee on account 3390, and it is removed."),

# why: adjustment POSTED_FINAL with approval -> yes. Twin: awaiting approval -> no.
A("hb13", """
Posting journal, adjustments batch for Wrenfield patient accounts:
acct=6612 adj_code=CHARITY100 applied_by=kpatel approved_by=billing_mgr status=POSTED_FINAL
""", 1, 2,
  "applied_by=kpatel approved_by=billing_mgr status=POSTED_FINAL",
  "requested_by=kpatel approved_by=none status=AWAITING_APPROVAL"),

# why: filing limit and dates (120 > 90 days) -> facts. Twin: 'Write it off as a timely-filing loss' -> directive.
X("hb14", """
The timely filing limit for Northvale is 90 days from the date of service. This claim's date of service was 120 days ago.
""", 0, 2,
  "was 120 days ago.",
  " Write it off as a timely-filing loss."),

# why: lead says dispute resolved, close the ticket -> yes. Twin: needs the itemised bill first -> no.
A("hb15", """
From: Patient Accounts Lead
The dispute on the Ferreira account is resolved in the patient's favour. Close the ticket.
""", 1, 1,
  "The dispute on the Ferreira account is resolved in the patient's favour. Close the ticket.",
  "The Ferreira account dispute needs the itemised bill before anyone decides."),

# why: patient's account of what she was told + request -> no. Twin: removed, account shows $0 -> yes.
X("hb16", """
The patient says she was told at check-in that the visit would be free, and she wants the charge removed.
""", 0, 2,
  "and she wants the charge removed.",
  " We have removed it; the account shows $0."),

# why: 'Categorise the call as billing error — our fault' -> directive. Twin: take the call notes -> process.
A("hb17", """
Categorise the call as 'billing error — our fault'. The patient was charged for a cancelled appointment.
""", 1, 1,
  "Categorise the call as 'billing error — our fault'.",
  "Take full call notes."),

# why: automatic small-balance rule -> no. Twin: account 2210's balance adjusted off; close it -> yes.
X("hb18", """
Policy: balances under $10 are adjusted off automatically at month end.
""", 0, 1,
  "automatically at month end.",
  " Account 2210's $8 balance has been adjusted off; close it."),

# why: reconsideration decision: denial upheld, final level -> yes. Twin: request pending -> no.
A("hb19", """
The payer's reconsideration decision came back: denial upheld, final level. Nothing more to file.
""", 1, 1,
  "The payer's reconsideration decision came back: denial upheld, final level. Nothing more to file.",
  "The reconsideration request went to the payer on 4 April; they have 60 days to respond."),

# why: insurer payments facts -> no. Twin: account closed as paid in full -> yes.
X("hb20", """
Two insurers are on the account. The primary paid $300; the secondary has not been billed.
""", 0, 1,
  "the secondary has not been billed.",
  " Bill nothing further; the account is closed as paid in full."),

# why: director already refused the discount -> yes. Twin: approval rule -> no.
A("hb21", """
Leave the prompt-pay discount off — the director already refused it for this account. The patient asked whether any discount is possible.
""", 1, 1,
  "Leave the prompt-pay discount off — the director already refused it for this account.",
  "The prompt-pay discount needs the director's approval for accounts over $5,000."),

# why: account facts + discount policy -> no. Twin: 'Apply the 30% now' -> directive.
X("hb22", """
Guarantor: Leonard Ashby. Relationship: parent. Insurance: none on file. Self-pay discount: 30% under policy SP-2 if paid within 30 days.
""", 0, 2,
  "if paid within 30 days.",
  " Apply the 30% now."),

# why: 'tell the caller her assistance was approved' -> decided. Twin: application with committee -> no.
A("hb23", """
tell the caller her financial assistance was approved, the letter's going out today
""", 1, 1,
  "her financial assistance was approved, the letter's going out today",
  "her financial assistance application is still with the committee"),

# why: patient's request with new ID -> no. Twin: resubmitted and paid; closed -> yes.
X("hb24", """
A patient asked us to resubmit her claim to the correct insurer; she gave a new member ID. She has already paid her copay for that visit.
""", 0, 1,
  "she gave a new member ID.",
  " Resubmitted and paid; closed."),

# why: 'Answer for the audit line: correctly billed' -> directive. Twin: which statement the line covers -> fact.
A("hb25", """
Answer for the audit line: 'correctly billed'. I checked it myself.
""", 1, 1,
  "Answer for the audit line: 'correctly billed'. I checked it myself.",
  "The audit line covers the 2 May statement for account 8120."),

# why: credit balance fact -> no. Twin: refund approved by finance -> yes.
X("hb26", """
Account 3307 shows a credit of $210 after the insurer's late payment arrived.
""", 0, 1,
  "late payment arrived.",
  " Refund approved by finance — send it."),

# why: approval GRANTED -> yes. Twin: routed -> no.
A("hb27", """
Adjustment request ADJ-3308
Type: courtesy discount
Amount: $150
Approval: GRANTED (A. Mbeki, 5/6)
""", 1, 1,
  "Approval: GRANTED (A. Mbeki, 5/6)",
  "Approval: routed to A. Mbeki"),

# why: missing number and it's on file -> facts. Twin: corrected claim approved and paid -> yes.
X("hb28", """
The prior authorisation number was missing on the original claim. The office has the number on file from 2 January.
""", 0, 1,
  "on file from 2 January.",
  " The corrected claim was approved and paid last week."),

# why: CFO put a permanent hold -> decided + directive. Twin: meets threshold for review -> no.
A("hb29", """
Do not send the account to collections; the CFO put a permanent hold on it.
""", 1, 2,
  "Do not send the account to collections; the CFO put a permanent hold on it.",
  "The account meets the age threshold for collections review."),

# why: policy on plan lengths -> no. Twin: 'Give this family the 12-month plan; it's approved' -> yes.
X("hb30", """
Our policy lets front-desk staff promise a payment plan only up to 6 months; longer plans need approval.
""", 0, 1,
  "longer plans need approval.",
  " Give the Tanaka family the 12-month plan; it's approved."),

# why: 'Write eligible in box 12' -> directive. Twin: procedure for box 12 -> no.
A("hb31", """
Write 'eligible' in box 12 of the assistance form — her pay slips are fine.
""", 1, 1,
  "Write 'eligible' in box 12 of the assistance form — her pay slips are fine.",
  "Box 12 of the assistance form is filled in after her pay slips are checked."),

# why: address facts -> no. Twin: late fees removed; settles the complaint -> yes.
X("hb32", """
The statement went to an old address twice; the patient updated the address on 1 March.
""", 0, 1,
  "updated the address on 1 March.",
  " Late fees removed; that settles the complaint."),

# why: appeal outcome WON, case closed -> yes. Twin: letter drafted, awaiting signature -> no.
A("hb33", """
2026-03-18 appeal_mgr: APPEAL AP-771 — outcome WON, $1,860 recovered, case closed.
""", 1, 1,
  "outcome WON, $1,860 recovered, case closed.",
  "letter drafted, awaiting signature before sending."),

# why: remittance not arrived, 'in process' -> status. Twin: paid in full, closed -> yes.
A("hb34", """
The remittance for claim 3310 has not arrived; the payer's portal shows 'in process'. The patient has asked for an update.
""", 0, 1,
  "The remittance for claim 3310 has not arrived; the payer's portal shows 'in process'.",
  "The remittance for claim 3310 arrived: paid in full, and the claim is closed."),

# why: AR lead: 'Treat 4410 as bad debt. It's decided.' -> yes. Twin: asks if old enough -> no.
A("hb35", """
Accounts receivable lead: 'Treat 4410 as bad debt. It's decided.'
""", 1, 1,
  "'Treat 4410 as bad debt. It's decided.'",
  "'Is 4410 old enough for the bad-debt review?'"),

# why: charges and patient's question -> no. Twin: fee stands, dispute closed -> yes.
X("hb36", """
Charges for the 9 June visit: facility fee $220, professional fee $140. The patient questions the facility fee.
""", 0, 1,
  "questions the facility fee.",
  " The facility fee stands; dispute closed by patient accounts."),

# why: 'Rebill to the new payer — that's the decision' -> yes. Twin: fact about payer details -> no.
A("hb37", """
The patient's employer changed insurers in January, and the old insurer returned the claim. Rebill to the new payer — that's the decision, don't hold it. The patient asked whether she needs to do anything before then.
""", 1, 2,
  "Rebill to the new payer — that's the decision, don't hold it.",
  "The new payer's details are on the intake form."),

# why: family member's question -> no. Twin: put on hold, approved -> yes.
X("hb38", """
A family member called to ask whether the account can be put on hold while the patient is abroad.
""", 0, 1,
  "while the patient is abroad.",
  " It has been put on hold until 1 October, approved by the manager."),

# why: director approved a full waiver; no committee needed -> yes. Twin: rule + amount -> no.
A("hb39", """
No need for committee review: the director approved a full hardship waiver for this account this morning.
""", 1, 1,
  "No need for committee review: the director approved a full hardship waiver for this account this morning.",
  "Hardship waivers above $1,000 go to committee review; this account's balance is $1,450."),

# why: statement cycle rule -> no. Twin: 'Account 9021 gets the final notice — send it' -> directive.
X("hb40", """
Statement cycle: statements go out on the 5th; a balance unpaid after 3 statements gets a final notice.
""", 0, 1,
  "gets a final notice.",
  " Account 9021 gets the final notice — send it."),

# why: 'pls code the refund as duplicate payment, manager ok'd it' -> yes. Twin: check first -> no.
A("hb41", """
pls code the refund as 'duplicate payment', manager ok'd it
""", 1, 1,
  "pls code the refund as 'duplicate payment', manager ok'd it",
  "pls check whether the refund is a duplicate payment before the manager sees it"),

# why: guarantors and court split -> facts. Twin: 'Bill each half — billing lead has decided' -> yes.
X("hb42", """
The account has two guarantors listed after a divorce; the court order splits responsibility 50/50.
""", 0, 2,
  "splits responsibility 50/50.",
  " Bill each guarantor half — the billing lead has decided."),

# why: final coding review result -> yes. Twin: requested, due in 10 days -> no.
A("hb43", """
Coding review result (final): no change, claim stands as billed.
""", 1, 1,
  "Coding review result (final): no change, claim stands as billed.",
  "Coding review requested by the payer; result due in 10 days."),

# why: patient's request -> no. Twin: dispute rejected, balance stands -> yes.
A("hb44", """
The patient on account 6630 wants an itemised bill before paying anything.
""", 0, 1,
  "wants an itemised bill before paying anything.",
  "got the itemised bill and her dispute was rejected; the balance stands."),

# why: 'Enter approved — 6 month plan' -> directive. Twin: send for approval -> process.
A("hb45", """
Enter 'approved — 6 month plan' in the plan field and send the confirmation letter.
""", 1, 1,
  "Enter 'approved — 6 month plan' in the plan field and send the confirmation letter.",
  "Enter the requested plan length in the notes field and send it for approval."),

# why: waiver rule and prior waiver -> facts. Twin: 'Don't waive this one' -> directive.
X("hb46", """
Late payment fees can be waived once per account per year; this account had a waiver in March.
""", 0, 2,
  "had a waiver in March.",
  " Don't waive this one."),

# why: dispute settled on the phone -> yes. Twin: patient's offer -> no.
A("hb47", """
The dispute was settled on the phone: we remove the $40 fee, and the patient pays the rest.
""", 1, 1,
  "The dispute was settled on the phone: we remove the $40 fee, and the patient pays the rest.",
  "On the phone the patient offered to pay the rest if we remove the $40 fee."),

# why: contract amounts ($180 - $132 = $48) -> facts. Twin: 'Adjust $48 as contractual; decided' -> yes.
X("hb48", """
Payer contract: the allowed amount for this service is $132; we billed $180.
""", 0, 2,
  "we billed $180.",
  " Adjust $48 as contractual; decided."),

# why: 'Mark the credit balance refund to insurer ... already agreed' -> yes. Twin: finance lead needs to decide -> no.
A("hb49", """
Mark the credit balance 'refund to insurer' — they overpaid, and the finance lead already agreed.
""", 1, 1,
  "Mark the credit balance 'refund to insurer' — they overpaid, and the finance lead already agreed.",
  "The finance lead needs to decide whether the credit balance goes back to the insurer or the patient."),

# why: agency's practice -> fact. Twin: account sent to them, final -> yes.
X("hb50", """
The collections agency Brightledger holds accounts for 180 days before reporting them.
""", 0, 1,
  "before reporting them.",
  " Account 7704 was sent to them yesterday; that is final."),

# why: DENIED, signed final -> yes. Twin: blank outcome, to review -> no.
A("hb51", """
Charity care screening
Outcome: DENIED — income above 400% of guideline
Signed: B. Osei (final)
""", 1, 1,
  "Outcome: DENIED — income above 400% of guideline\nSigned: B. Osei (final)",
  "Outcome: (blank)\nNote: income documents show about 410% of guideline; B. Osei to review"),

# why: refund for another patient -> other case -> no. Twin: refunded this double charge, closed -> yes.
A("hb52", """
Account 5190 shows a double charge. Two months ago the office refunded a similar double charge for another patient within a week.
""", 0, 2,
  "Two months ago the office refunded a similar double charge for another patient within a week.",
  "The office refunded this double charge on Monday; the case is closed."),

# why: insurer rename facts -> no. Twin: 'Rebill under Northvale — decided and final' -> yes.
X("hb53", """
The patient's insurer changed its name from Harlow Mutual to Northvale on 1 January; the claims address is the same.
""", 0, 1,
  "the claims address is the same.",
  " Rebill under Northvale — the billing lead has decided and it's final."),
]
