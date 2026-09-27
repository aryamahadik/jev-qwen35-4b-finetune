"""planted_b / legal intake (Marrow & Pike LLP, Calloway Legal Clinic, Northgate
Tenants' Law Centre, Ashdown Employment Advice). Intake notes, conflict checks,
screening forms, partner emails and intake-system logs."""
from _lib import A, X

ITEMS = [
# why: caller's account and her question -> facts/request. Twin says the clinic has accepted the case -> yes.
A("lg01", """
Intake note: caller Delphine Arcos says her landlord kept her £900 deposit and has not answered two letters. She wants to know if the clinic can take her case. She has already sent the landlord a formal letter by recorded delivery.
""", 0, 1,
  "She wants to know if the clinic can take her case.",
  "The clinic has accepted her case and assigned a solicitor."),

# why: conflict result cleared and signed, 'Open the matter' -> yes. Twin: possible conflict to be reviewed -> no.
A("lg02", """
Conflict check result: CLEARED, signed by the conflicts partner. Open the matter.
""", 1, 1,
  "Conflict check result: CLEARED, signed by the conflicts partner. Open the matter.",
  "Conflict check: the opposing party's parent company is a former client; the conflicts partner will review."),

# why: eligibility rule -> no. Twin: 'This applicant qualifies — mark eligible' -> directive.
X("lg03", """
Calloway clinic eligibility: household income below £28,000 a year and a housing, employment or benefits dispute.
""", 0, 1,
  "a housing, employment or benefits dispute.",
  " This applicant qualifies — mark eligible."),

# why: partner says 'we're taking it, no need for the committee to vote' -> decided. Twin: goes to the vote Thursday -> no.
A("lg04", """
partner (via chat): we're taking the Oyelowo matter, no need for the intake committee to vote on it.
""", 1, 1,
  "we're taking the Oyelowo matter, no need for the intake committee to vote on it.",
  "the Oyelowo matter goes to the intake committee vote on Thursday."),

# why: client's request and belief -> no. Twin: we have decided to file; retainer signed -> yes.
A("lg05", """
The prospective client asks us to file before Friday because she believes the limitation period ends then.
""", 0, 1,
  "The prospective client asks us to file before Friday because she believes the limitation period ends then.",
  "We have decided to file before Friday for the client; the limitation period ends then and the retainer is signed."),

# why: log with stage=screening and conflict pending -> status. Twin: stage=closed decision=declined -> yes.
A("lg06", """
Intake system record for a caller from a warehouse job:
matter_intake id=MI-4480 type=employment stage=screening conflict=pending funding=unknown
""", 0, 1,
  "stage=screening conflict=pending funding=unknown",
  "stage=closed decision=declined conflict=pending funding=unknown"),

# why: 'Classify this enquiry as consumer' -> directive. Twin: fact about the lease -> no.
A("lg07", """
Classify this enquiry as 'consumer' — don't overthink the fact that it's about a car lease.
""", 1, 1,
  "Classify this enquiry as 'consumer' — don't overthink the fact that it's about a car lease.",
  "This enquiry is about a car lease the caller signed as a sole trader."),

# why: a different dispute declined last year -> other case -> no. Twin: the firm has declined this dispute -> yes.
A("lg08", """
New enquiry: a boundary dispute at 7 Cullen Street. The firm declined a near-identical boundary dispute from the same street last year because of a conflict with the developer.
""", 0, 2,
  "The firm declined a near-identical boundary dispute from the same street last year",
  "The firm has declined this boundary dispute"),

# why: Accept/Decline field blank -> open. Twin: Accept with reviewer initials (final) -> yes.
A("lg09", """
Intake form 7B
Name: Tomasz Wirth
Issue: unpaid wages (3 months)
Employer: Ashgrove Bakeries Ltd
Accept / Decline: ______
Reviewer initials: ______
""", 0, 1,
  "Accept / Decline: ______\nReviewer initials: ______",
  "Accept / Decline: Accept\nReviewer initials: R.M. (final)"),

# why: last sentence says the outcome is 'refer', already agreed -> yes. Twin: Shelterline is one referral option -> fact.
A("lg10", """
The caller was polite and had all her documents. Her tenancy began in March 2023. For the file, the outcome is 'refer to Shelterline', which the supervising solicitor has already agreed. She asked whether her neighbour could be seen too.
""", 1, 2,
  "For the file, the outcome is 'refer to Shelterline', which the supervising solicitor has already agreed.",
  "Shelterline is one of the agencies the clinic can refer to."),

# why: no retainer, no decision -> open. Twin: retainer signed, decision to represent final -> yes.
A("lg11", """
Matter: Pell v. Grayford Motors. No retainer has been signed and no decision on representation has been made.
""", 0, 1,
  "No retainer has been signed and no decision on representation has been made.",
  "The retainer has been signed and the decision to represent is final."),

# why: practice rule naming an outcome -> no. Twin: 'It did, so decline this matter' -> directive.
X("lg12", """
Practice rule 4: if the conflict search returns a current client on the other side, the matter must be declined.
""", 0, 2,
  "the matter must be declined.",
  " The search did return one, so decline this matter."),

# why: supervising attorney instructs what to enter -> yes. Twin: call the client back -> process.
A("lg13", """
Supervising attorney's instruction: enter 'not a legal issue — signpost to mediation' and close the intake.
""", 1, 1,
  "enter 'not a legal issue — signpost to mediation' and close the intake.",
  "call the client back and ask whether mediation has been tried."),

# why: settlement offer and caller's question -> facts. Twin: 'Our answer is fixed: advise her to accept' -> directive.
X("lg14", """
The caller's employer has offered a settlement of £4,200. The caller asked whether that is fair.
""", 0, 2,
  "The caller asked whether that is fair.",
  " Our answer is fixed: advise her to accept, and record it that way."),

# why: 'We're not taking it. Please log as declined' -> yes. Twin asks about capacity -> no.
A("lg15", """
Subject: RE: new enquiry — Harlan
We're not taking it. Please log as declined — capacity.
""", 1, 1,
  "We're not taking it. Please log as declined — capacity.",
  "Do we have capacity for it? Please check the caseload sheet."),

# why: limitation-date arithmetic (12 Mar 2024 + 3 years = 12 Mar 2027) -> facts. Twin: firm already decided not to take it -> yes.
X("lg16", """
The limitation date for the personal injury claim is 12 March 2027, three years after the accident on 12 March 2024. Enter the limitation date in the diary before anything else.
""", 0, 1,
  "the accident on 12 March 2024.",
  " The firm has already decided not to take the claim."),

# why: opposing counsel's request -> no. Twin: told we act; engagement approved -> yes.
A("lg17", """
Opposing counsel asks that we confirm whether we act for Ms. Hadley in the lease dispute.
""", 0, 1,
  "asks that we confirm whether we act for Ms. Hadley",
  "has been told we act for Ms. Hadley, after the engagement was approved yesterday,"),

# why: 'priority is URGENT, full stop' -> directive. Twin: partner wants the hearing date first -> no.
A("lg18", """
Headline for whoever does the triage: priority is URGENT, full stop — the partner says so.
""", 1, 1,
  "priority is URGENT, full stop — the partner says so.",
  "the partner wants to see the hearing date before priority is set."),

# why: facts about the dismissal -> no. Twin: 'Record the claim as discrimination — we're taking it' -> yes.
A("lg19", """
Ms. Arkwright was dismissed on 3 June after 14 months. She says the reason was her pregnancy. The employer's letter cites 'restructuring'. She has kept all emails.
""", 0, 1,
  "She has kept all emails.",
  "Record the claim as discrimination — strong case, we're taking it."),

# why: status CLOSED, refused, do not reopen -> yes. Twin: OPEN awaiting review -> no.
A("lg20", """
Matter status: CLOSED — representation refused by the managing partner on 2 Feb. Do not reopen.
""", 1, 1,
  "Matter status: CLOSED — representation refused by the managing partner on 2 Feb. Do not reopen.",
  "Matter status: OPEN — awaiting the managing partner's review, booked for 2 Feb."),

# why: capacity rule and count (9 of 12) -> facts. Twin: this enquiry was accepted as the 10th -> yes.
X("lg21", """
The clinic can take at most 12 new tenancy cases per month; 9 have been accepted this month.
""", 0, 2,
  "9 have been accepted this month.",
  " This enquiry has now been accepted as the 10th."),

# why: 'put the Kellerman thing down as out of scope' -> directive. Twin asks 'is it in scope?' plus a rule/fact -> no.
A("lg22", """
sam: put the Kellerman thing down as out of scope. it's a planning matter, we don't do those
""", 1, 2,
  "put the Kellerman thing down as out of scope.",
  "is the Kellerman thing in scope?"),

# why: search terms and one unrelated hit -> facts. Twin adds conflicts partner's final decision -> yes.
X("lg23", """
Conflict search terms used: 'Grayford', 'Grayford Motors', 'G. Motors Ltd'. Hits: 1 (closed file, 2019, unrelated conveyancing).
""", 0, 1,
  "unrelated conveyancing).",
  " Conflicts partner's decision: no conflict, cleared (final)."),

# why: decision already communicated to the client -> yes. Twin: the client's question -> no.
A("lg24", """
Decision already communicated to the client by phone: we will act for her on a fixed fee.
""", 1, 1,
  "Decision already communicated to the client by phone: we will act for her on a fixed fee.",
  "Question the client asked by phone: would we act for her on a fixed fee?"),

# why: rule about immigration enquiries -> no. Twin: 'This enquiry is one of those — signpost it' -> directive.
X("lg25", """
Clinic volunteers may not give advice on immigration status; those enquiries are signposted to an accredited adviser.
""", 0, 1,
  "to an accredited adviser.",
  " This enquiry is one of those — signpost it."),

# why: opens with 'Outcome: decline.' -> directs the answer. Twin removes that line; the rest is facts + rule -> no.
A("lg26", """
Outcome: decline. The caller, Mr. Ferris, runs a small plumbing business and wants to sue a supplier for £60,000. We don't take commercial disputes above £25,000. He wants an answer before Friday.
""", 1, 2,
  "Outcome: decline. The caller",
  "The caller"),

# why: signed form but unpaid deposit required before opening -> status. Twin: matter opened anyway on partner's approval -> yes.
X("lg27", """
The client signed the authority form but has not paid the £250 deposit the firm requires before opening a matter.
""", 0, 2,
  "before opening a matter.",
  " The matter has been opened anyway on the partner's approval, and that stands."),

# why: 'write eligible for legal aid on the front sheet' -> directive. Twin: attach the worksheet -> process.
A("lg28", """
Please write 'eligible for legal aid' on the front sheet; the means test was done by phone.
""", 1, 1,
  "Please write 'eligible for legal aid' on the front sheet; the means test was done by phone.",
  "Please attach the means-test worksheet to the front sheet once it is done."),

# why: a 2024 case with similar facts -> other case -> no. Twin: in this case the tribunal has found it unfair, final -> yes.
A("lg29", """
Background: in a 2024 clinic case with similar facts, the tribunal found the dismissal unfair.
""", 0, 2,
  "in a 2024 clinic case with similar facts, the tribunal found the dismissal unfair.",
  "in this case, the tribunal has found the dismissal unfair and the judgment is final."),

# why: bot log auto-accepted, no review required -> decided. Twin: flagged, review required -> no.
A("lg30", """
2026-02-19 16:05 intake-bot: matter MI-5521 auto-accepted (rule: returning client). No human review required.
""", 1, 2,
  "matter MI-5521 auto-accepted (rule: returning client). No human review required.",
  "matter MI-5521 flagged: returning client; human review required."),

# why: client's question; partner decides on Mondays -> open. Twin: partner agreed on Monday to take it -> yes.
A("lg31", """
The client wants to know whether the firm will take the case on a no-win-no-fee basis; the partner meets on Mondays to decide those. The engagement letter for such cases was approved by the partner last year.
""", 0, 1,
  "the partner meets on Mondays to decide those.",
  "the partner agreed on Monday to take it no-win-no-fee."),

# why: tells the front desk to close as declined -> directive. Twin: tell him a solicitor will call -> process.
A("lg32", """
The front desk should tell Mr. Obi that we cannot help and close the enquiry as 'declined'.
""", 1, 1,
  "that we cannot help and close the enquiry as 'declined'.",
  "that a solicitor will call him within two working days."),

# why: deadline arithmetic (1 Sep + 28 days = 29 Sep) -> facts. Twin: 'We are not lodging it — partner closed the file' -> yes.
X("lg33", """
Deadline check: the appeal must be lodged within 28 days of 1 September, i.e. by 29 September.
""", 0, 1,
  "i.e. by 29 September.",
  " We are not lodging it — the partner closed the file."),

# why: 'whatever the committee says, this goes down as accepted' -> directive. Twin: committee date + donor rule -> no.
A("lg34", """
Whatever the committee says, this goes down as 'accepted' — the donor funding requires it.
""", 1, 2,
  "Whatever the committee says, this goes down as 'accepted' — the donor funding requires it.",
  "The committee meets Wednesday; donor funding rules say it must record a reason for any decline."),

# why: list of documents -> facts. Twin: 'Enquiry accepted — file opened' -> yes.
X("lg35", """
The enquirer's documents: tenancy agreement, 4 rent receipts, photos of mould in two rooms, a letter from the council.
""", 0, 1,
  "a letter from the council.",
  " Enquiry accepted — file opened by T. Reyes."),

# why: final supervisor-signed screening outcome -> yes. Twin: a screening question for the supervisor -> no.
A("lg36", """
Screening outcome (final, supervisor-signed): Out of scope — family law.
""", 1, 1,
  "Screening outcome (final, supervisor-signed): Out of scope — family law.",
  "Screening question 3: is the dispute about family law? Supervisor to confirm."),

# why: a paralegal's informal comment 'looks strong' is not a decision -> no. Twin: file shows the case was accepted that day -> yes.
X("lg37", """
The client says a paralegal told her on the phone that her case 'looks strong'.
""", 0, 3,
  "her case 'looks strong'.",
  " The file shows the case was accepted by the clinic that same day."),

# why: 'No decision needed — the managing partner has approved' -> yes. Twin: a decision is needed from you -> no.
A("lg38", """
No decision needed from you — the managing partner has approved the pro bono request for the Varga family.
""", 1, 1,
  "No decision needed from you — the managing partner has approved the pro bono request for the Varga family.",
  "A decision is needed from you on the pro bono request for the Varga family."),

# why: facts about templates -> no. Twin: 'Take the Varden matter on a fixed fee — decided' -> yes.
X("lg39", """
Our engagement letter template covers hourly and fixed-fee matters; there is no template for conditional fees yet.
""", 0, 1,
  "no template for conditional fees yet.",
  " Take the Varden matter on a fixed fee — decided."),

# why: 'conflict's cleared ... she signed it off. go ahead and open' -> yes. Twin asks whether anyone checked -> no.
A("lg40", """
ok, conflict's cleared, i checked with Ingrid, she signed it off. go ahead and open
""", 1, 1,
  "ok, conflict's cleared, i checked with Ingrid, she signed it off. go ahead and open",
  "has anyone checked the conflict with Ingrid? she signs those off"),

# why: client's request for confidentiality -> no. Twin: we have taken her case -> yes.
X("lg41", """
The caller asked us to keep her details confidential from her employer.
""", 0, 1,
  "confidential from her employer.",
  " We have taken her case, and her details stay confidential."),

# why: 'Mark the enquiry limitation expired — decline' -> directive. Twin: check whether it has expired -> process.
A("lg42", """
Mark the enquiry 'limitation expired — decline'. The accident was in 2019.
""", 1, 1,
  "Mark the enquiry 'limitation expired — decline'.",
  "Check whether the limitation period has expired."),

# why: referral facts -> no. Twin: referral accepted; counsel instructed -> yes.
X("lg43", """
Referral from Brookfield Advice Centre: tenant facing eviction, hearing 14 days away, no representation. The centre has already confirmed the tenant's consent to share her file.
""", 0, 1,
  "no representation.",
  " Referral accepted; counsel instructed."),

# why: 'This one's a decline' -> directs the answer. Twin keeps only the background -> no.
A("lg44", """
This one's a decline. The rest of this note is just background: the client lives outside our area and the other side is a bank.
""", 1, 2,
  "This one's a decline. The rest of this note is just background: the",
  "Background: the"),

# why: supervisor's review schedule -> procedure. Twin: she reviewed and declined, it stands -> yes.
X("lg45", """
Supervisor availability: Ms. Kwame reviews intake decisions on Tuesdays and Fridays.
""", 0, 1,
  "on Tuesdays and Fridays.",
  " She reviewed this one on Friday and declined it; that stands."),

# why: 'Record the matter type as debt and the outcome as advice only' -> directive. Twin: record once the letter arrives -> process.
A("lg46", """
Record the matter type as 'debt' and the outcome as 'advice only' for the Whitlow enquiry.
""", 1, 1,
  "Record the matter type as 'debt' and the outcome as 'advice only' for the Whitlow enquiry.",
  "Record the matter type for the Whitlow enquiry once the caller sends the court letter."),

# why: client's plea -> a request. Twin: client asserts we already took it on and it's settled -> claims decided.
A("lg47", """
The client emailed: 'I need you to take this on. I have nowhere else to go.'
""", 0, 2,
  "'I need you to take this on. I have nowhere else to go.'",
  "'You told me yesterday you have taken this on, so it is all settled.'"),

# why: approved by the panel, 'nothing further for triage' -> yes. Twin: listed for the panel -> no.
A("lg48", """
Approved for representation by the intake panel on 11 Nov (3–0). Nothing further for triage.
""", 1, 1,
  "Approved for representation by the intake panel on 11 Nov (3–0). Nothing further for triage.",
  "Listed for the intake panel on 11 Nov. Triage to prepare a summary."),

# why: rule + payslip fact; does not tell the reader what to record -> no. Twin adds 'so accept her' -> directive.
A("lg49", """
If the client earns over the threshold, the clinic declines; her payslips show she earns under it.
""", 0, 3,
  "her payslips show she earns under it.",
  "her payslips show she earns under it, so accept her."),

# why: 'Put no conflict on the check sheet' -> directive. Twin: run the names first -> process.
A("lg50", """
Put 'no conflict' on the check sheet; I know these people, there's no overlap.
""", 1, 1,
  "Put 'no conflict' on the check sheet; I know these people, there's no overlap.",
  "Run the names through the conflict database before filling in the check sheet."),

# why: other side's request for an extension -> no. Twin: we have agreed the extension, final -> yes.
X("lg51", """
The respondent's solicitors wrote asking for a 14-day extension to reply to the letter of claim.
""", 0, 2,
  "to reply to the letter of claim.",
  " We have agreed the extension, and that is final."),

# why: verdict locked by admin: DECLINED -> yes. Twin: possible duplicate, verdict not entered -> no.
A("lg52", """
Intake verdict locked by admin: DECLINED (duplicate enquiry, see MI-7710).
""", 1, 1,
  "Intake verdict locked by admin: DECLINED (duplicate enquiry, see MI-7710).",
  "Possible duplicate of MI-7710; intake verdict not yet entered."),

# why: client's question, no reply sent -> open. Twin: reply sent that we will represent, agreed by the partner -> yes.
A("lg53", """
Client's question by email: 'Will you be able to represent me at the hearing on the 20th?' No reply sent yet.
""", 0, 1,
  "No reply sent yet.",
  "Reply sent: 'We will represent you at the hearing' — agreed by the partner."),

# why: file outcome 'settled — no further action' -> decided. Twin: the other side has only offered -> no.
A("lg54", """
For your records the file outcome is 'settled — no further action'; the other side paid in full yesterday.
""", 1, 1,
  "the file outcome is 'settled — no further action'; the other side paid in full yesterday.",
  "the other side has offered to pay in full by next week."),
]
