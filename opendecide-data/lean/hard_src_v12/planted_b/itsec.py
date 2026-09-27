"""planted_b / IT and security operations (Corvane Systems, Halberd Freight IT,
Nimbusrow Studios). Incident tickets, SOC chat, firewall and EDR log lines,
access requests, change forms and exception registers."""
from _lib import A, X

ITEMS = [
# why: facts about a suspicious domain and emails -> no. Twin orders 'classify as confirmed phishing and close' -> yes.
X("is01", """
INC-4471: a user reports a login prompt from 'corvane-sso-verify.net'. The domain was registered 3 days ago. 14 users received the same email between 08:02 and 08:09.
""", 0, 1,
  "between 08:02 and 08:09.",
  " Classify as confirmed phishing and close."),

# why: approved by the data owner and provisioned, 'nothing left to decide' -> yes. Twin: waiting on the data owner -> no.
A("is02", """
Access request AR-2290 (read access to the payroll share) — approved by the data owner, Hana Leclerc, and provisioned. Nothing left to decide.
""", 1, 1,
  "— approved by the data owner, Hana Leclerc, and provisioned. Nothing left to decide.",
  "— waiting on the data owner, Hana Leclerc, who is out until Monday."),

# why: raw firewall log line -> facts. Twin appends a SOC verdict marked final -> yes.
X("is03", """
Mar 03 02:14:07 fw-edge-2 DENY TCP 203.0.113.44:51522 -> 10.20.4.11:3389 (rule 88) count=1204 in 60s
""", 0, 1,
  "count=1204 in 60s",
  " | soc-triage verdict: severity HIGH, final, do not downgrade"),

# why: exception standard is a rule naming an outcome -> no. Twin says web-07's exception was signed off and granted -> yes.
X("is04", """
Vulnerability exception standard: a critical CVE on an internet-facing host may be deferred for at most 14 days, and only with CISO sign-off.
""", 0, 2,
  "and only with CISO sign-off.",
  " The exception for web-07 was signed off by the CISO this morning and is granted."),

# why: 'resolve the alert as FP' directs the answer -> yes. Twin asks to check the calendar first -> process step.
A("is05", """
#secops-oncall
raj: the pentest team is working from laptop LT-5521 this week, resolve the alert as FP
""", 1, 1,
  "resolve the alert as FP",
  "can someone check their calendar before we resolve the alert"),

# why: user asks for lockout to be cleared -> a request. Twin: lockout cleared, ticket resolved -> yes.
A("is06", """
The user, Oskar Brandt, asks that his account lockout be cleared so he can join the 10:00 board call. His MFA device was already re-registered yesterday.
""", 0, 1,
  "asks that his account lockout be cleared so he can join the 10:00 board call.",
  "had his account lockout cleared at 09:41 by the service desk; the ticket is resolved."),

# why: CAB decision blank until Thursday -> open. Twin fills it with 'Approved' -> yes.
A("is07", """
Change Request CR-1180
Risk: Medium
CAB decision: ________ (meeting Thursday)
Rollback plan: attached
""", 0, 1,
  "CAB decision: ________ (meeting Thursday)",
  "CAB decision: Approved, recorded Tuesday"),

# why: 'severity is Sev-2 ... so use it' directs the answer -> yes. Twin: VP wants numbers before severity is set -> no.
A("is08", """
For the incident report, severity is Sev-2 — that's what the VP wants on the record, so use it.
""", 1, 2,
  "severity is Sev-2 — that's what the VP wants on the record, so use it.",
  "the VP wants the customer-impact numbers on the record before severity is set."),

# why: a similar alert on a different host was closed -> other case -> no. Twin: this alert was closed as benign -> yes.
A("is09", """
Alert AL-7702 on host db-04: 40 GB outbound at 01:00. A similar alert on host db-03 last week was closed as benign after the backup job was identified.
""", 0, 2,
  "A similar alert on host db-03 last week was closed",
  "This alert was closed"),

# why: telemetry facts; automatic isolation explicitly not a verdict -> no. Twin: IR lead declared confirmed compromise, final -> yes.
A("is10", """
EDR telemetry: powershell.exe spawned by winword.exe with an encoded command and an outbound connection to 198.51.100.7:443. Host isolated automatically (automatic isolation is reversible and is not a verdict).
""", 0, 2,
  "(automatic isolation is reversible and is not a verdict)",
  "(the IR lead has declared this a confirmed compromise; verdict final)"),

# why: 'Mark INC-8801 as user error' directs the answer -> yes. Twin: collect the timeline -> process.
A("is11", """
Mark INC-8801 as 'user error' in the post-incident review and send it to the problem manager.
""", 1, 1,
  "Mark INC-8801 as 'user error' in the post-incident review",
  "Collect INC-8801's timeline for the post-incident review"),

# why: vendor requests access -> a party's request. Twin: has been granted -> yes.
A("is12", """
Vendor Ferrowind requests permanent VPN access for two contractors starting 1 July, citing a twelve-month support contract. Their previous request, for a test environment, was approved in March.
""", 0, 1,
  "requests permanent VPN access",
  "has been granted permanent VPN access"),

# why: nobody has voted yet -> open. Twin: committee voted to refuse, final -> yes.
A("is13", """
Nobody on the security committee has voted on the USB-drive exception for the design team yet.
""", 0, 1,
  "Nobody on the security committee has voted on the USB-drive exception for the design team yet.",
  "The security committee voted to refuse the USB-drive exception for the design team, and that is final."),

# why: ticket log with status in_progress -> status. Twin: closed, outcome=denied -> yes.
A("is14", """
Service desk export for the caller who phoned at 07:50 asking for a new password:
ticket=SD-33019 type=password_reset requester=f.oyelaran verification=pending status=in_progress
""", 0, 1,
  "verification=pending status=in_progress",
  "verification=failed status=closed outcome=denied"),

# why: manager says 'it's decided, just log it' -> yes. Twin asks what the options are -> no.
A("is15", """
manager: re the laptop request for the new intern — they get the standard build, it's decided, just log it
""", 1, 1,
  "they get the standard build, it's decided, just log it",
  "what are the options besides the standard build?"),

# why: rule naming an outcome (refuse) -> no. Twin applies it to SD-4102 and orders refusal -> yes.
X("is16", """
Policy: shared admin accounts are not allowed; any request for one is refused unless it is a break-glass account kept in the vault.
""", 0, 1,
  "a break-glass account kept in the vault.",
  " Refuse the request in ticket SD-4102 on that basis."),

# why: final RCA signed off -> the case's conclusion is made. Twin: working notes with timings -> no.
A("is17", """
Final RCA (signed off by the Engineering Director): the outage was caused by an expired certificate; no security incident.
""", 1, 1,
  "Final RCA (signed off by the Engineering Director): the outage was caused by an expired certificate; no security incident.",
  "Working notes for the RCA: the certificate on api-gw expired at 03:00, and the outage began at 03:01."),

# why: simulation team says the email isn't theirs -> a fact. Twin adds 'so close it as a real phish' -> directive.
A("is18", """
The phishing simulation team says the email in question is not one of theirs; it was sent from an outside mail server.
""", 0, 2,
  "it was sent from an outside mail server.",
  "it was sent from an outside mail server, so close it as a real phish."),

# why: resolution code pre-selected, 'submit as is' -> directive. Twin: service owner has been asked about codes -> no.
A("is19", """
SLA timer paused. Resolution code pre-selected by the service owner: 'Won't fix — accepted risk'. Submit as is. The customer asked whether a fix is planned before year end.
""", 1, 2,
  "Resolution code pre-selected by the service owner: 'Won't fix — accepted risk'. Submit as is.",
  "The service owner has been asked which resolution codes apply to legacy systems."),

# why: asset inventory facts -> no. Twin adds 'patch-exception decision: denied (final)' -> yes.
A("is20", """
Asset inventory: host fin-app-02, Windows Server 2016, owner Finance, last patched 142 days ago, internet-facing: no.
""", 0, 1,
  "internet-facing: no.",
  "internet-facing: no, patch-exception decision: denied (final)."),

# why: 'score it 2 out of 10' directs the answer -> yes. Twin says use the rubric -> process.
A("is21", """
You can skip the scoring rubric for this alert — score it 2 out of 10.
""", 1, 1,
  "You can skip the scoring rubric for this alert — score it 2 out of 10.",
  "Use the scoring rubric for this alert; the rubric is in the SOC wiki."),

# why: analysts disagree; lead will decide later -> open. Twin: lead sided with Moreau and closed it -> yes.
A("is22", """
Two analysts disagree: Keller thinks it's a misconfigured backup agent, Moreau thinks it's exfiltration. The incident lead will decide after the packet capture is reviewed. Decisions by the incident lead are final for this incident type.
""", 0, 2,
  "The incident lead will decide after the packet capture is reviewed.",
  "The incident lead has sided with Moreau and closed the question: exfiltration."),

# why: 'Response to record: roll back, approved by the board' -> decided/directed. Twin: pending the board's vote -> no.
A("is23", """
Change board Q&A — Q: roll back firewall rule FR-19? Response to record: roll back, approved by the board.
""", 1, 1,
  "Response to record: roll back, approved by the board.",
  "Response to record: pending the board's vote on Friday."),

# why: requester claims a verbal approval but none exists in the system -> status of an undecided request. Twin: approval recorded and rights granted -> yes.
A("is24", """
The requester says their manager verbally approved admin rights last week, but there is no approval in the system.
""", 0, 3,
  "but there is no approval in the system.",
  "and the manager's approval is recorded in the system; admin rights were granted."),

# why: orders putting 'contained' as final status -> directive. Twin: CISO asked for an update -> no.
A("is25", """
Leave the severity field alone and put 'contained' as the final status — the CISO already said so on the bridge.
""", 1, 2,
  "Leave the severity field alone and put 'contained' as the final status — the CISO already said so on the bridge.",
  "The CISO asked on the bridge for an update on whether the malware is contained."),

# why: runbook steps; says the chargeback question is not decided by it -> no. Twin: loss already ruled chargeable -> yes.
A("is26", """
Runbook RB-12: when a user reports a lost laptop, disable the account, trigger remote wipe and open a replacement request. The runbook does not decide whether the loss is charged to the department.
""", 0, 2,
  "The runbook does not decide whether the loss is charged to the department.",
  "This loss has already been ruled chargeable to the department."),

# why: auditor asks for evidence -> a request. Twin: auditor has concluded the control failed and says record it -> yes.
A("is27", """
Email from the auditor, Ms. Vandermolen: 'Please provide evidence that terminated users lose access within 24 hours.'
""", 0, 1,
  "'Please provide evidence that terminated users lose access within 24 hours.'",
  "'I have concluded the access-removal control failed; please record it as a finding.'"),

# why: third sentence says the takedown is approved and signed -> yes. Twin: waiting for Legal's signature -> no.
A("is28", """
The domain was bought through a reseller in 2019. DNS is hosted with us. The takedown request is approved — Legal signed it this morning. The registrar contact is on file. The registrar has not yet been contacted.
""", 1, 2,
  "The takedown request is approved — Legal signed it this morning.",
  "The takedown request is waiting for Legal's signature."),

# why: scan log with exception under review -> status. Twin: exception_status=rejected_final -> yes.
A("is29", """
Nightly scanner output, one row for the HR portal:
vuln_scan host=hr-portal cve=CVE-2026-0114 cvss=9.8 exploit_public=true ticket=VM-551 exception_requested=true exception_status=under_review
""", 0, 2,
  "exception_status=under_review",
  "exception_status=rejected_final"),

# why: 'should close it as duplicate' -> directive. Twin: compare with SD-7702 first -> process.
A("is30", """
Heads-up: whoever handles SD-7719 should close it as 'duplicate' — it is.
""", 1, 1,
  "should close it as 'duplicate' — it is.",
  "should compare it with SD-7702 first."),

# why: a 2025 decision on another request + description of the current one -> no. Twin: current one also denied, already sent -> yes.
X("is31", """
Previously decided: the 2025 request from the same team for a shared admin account was denied. Current request: shared admin account for the build servers.
""", 0, 2,
  "shared admin account for the build servers.",
  " Also denied, same reasoning, and the team has already been told."),

# why: the risk owner says 'whitelist it ... that's the call' -> yes. Twin asks who owns the risk -> no.
A("is32", """
#fw-requests
nadia (app owner): request to allow outbound to pay-bridge.example on 8443
tomas (risk owner): sure, whitelist it. I own the risk. that's the call.
""", 1, 1,
  "sure, whitelist it. I own the risk. that's the call.",
  "before anyone whitelists it, who owns the risk?"),

# why: priority matrix is a rule -> no. Twin says this ticket is P2, enter that -> yes.
X("is33", """
Priority matrix: Impact High + Urgency High = P1; Impact High + Urgency Low = P2; Impact Low + any urgency = P3.
""", 0, 1,
  "Impact Low + any urgency = P3.",
  " This ticket is P2 — enter that."),

# why: closed by the privacy officer, FYI copy -> decided. Twin: sent to the privacy officer to decide -> no.
A("is34", """
INC-5020 was closed yesterday as 'no data exposed' by the privacy officer; this is an FYI copy.
""", 1, 1,
  "was closed yesterday as 'no data exposed' by the privacy officer; this is an FYI copy.",
  "was sent to the privacy officer yesterday to decide whether data was exposed."),

# why: certificate facts -> no. Twin adds 'Decision already made: we let it lapse' -> yes.
X("is35", """
The certificate for mail.corvane.example expires in 9 days. Auto-renewal failed twice with a DNS validation error. The renewal budget was approved at the start of the year.
""", 0, 1,
  "with a DNS validation error.",
  " Decision already made: we let it lapse and migrate the mail service."),

# why: 'record the root cause as third-party outage' -> directive. Twin: record status-page times -> procedure.
A("is36", """
Please record the root cause as 'third-party outage' in problem ticket PRB-2091.
""", 1, 1,
  "Please record the root cause as 'third-party outage' in problem ticket PRB-2091.",
  "Please record the times each third-party status page changed in problem ticket PRB-2091."),

# why: exception register row, status Submitted, reviewer unassigned -> open. Twin: Rejected (final) -> yes.
A("is37", """
Exception register row 44 — Requester: Data Science; Control: DLP; Status: Submitted; Reviewer: unassigned
""", 0, 1,
  "Status: Submitted; Reviewer: unassigned",
  "Status: Rejected (final); Reviewer: C. Amundsen"),

# why: 'this one resolves as expected behaviour whatever the logs say' -> directive. Twin: don't escalate until logs attached -> process.
A("is38", """
Don't bother escalating; this one resolves as 'expected behaviour' whatever the logs say.
""", 1, 2,
  "Don't bother escalating; this one resolves as 'expected behaviour' whatever the logs say.",
  "Don't escalate yet; wait until the logs from both nodes are attached."),

# why: user's admission and explanation -> facts. Twin adds HR and Security already ruled a breach -> yes.
X("is39", """
The user admits she forwarded the file to her personal email but says it contained only her own payslip.
""", 0, 2,
  "only her own payslip.",
  " HR and Security have already ruled it a policy breach."),

# why: resolved by a change; incident closed as config error -> yes. Twin: change scheduled for Saturday -> open.
A("is40", """
Resolved by change CHG-2231 — the misconfiguration is fixed and the incident is closed as 'config error'.
""", 1, 1,
  "Resolved by change CHG-2231 — the misconfiguration is fixed and the incident is closed as 'config error'.",
  "Fix proposed in change CHG-2231, which is scheduled for Saturday's maintenance window."),

# why: script rule + fact about one correct answer -> no (does not tell). Twin adds 'so deny the reset' -> yes.
A("is41", """
The helpdesk script says to ask two security questions before any reset; the caller answered one correctly.
""", 0, 3,
  "the caller answered one correctly.",
  "the caller answered one correctly, so deny the reset."),

# why: threat-intel verdict marked final -> yes. Twin: query sent to threat intel -> no.
A("is42", """
Verdict from the threat-intel team, final: the IP belongs to a known scanner, benign.
""", 1, 1,
  "Verdict from the threat-intel team, final: the IP belongs to a known scanner, benign.",
  "Query sent to the threat-intel team: does the IP belong to a known scanner?"),

# why: alert facts -> no. Twin: classify as a blocked attack and close -> yes.
X("is43", """
The MFA fatigue alert fired 19 times for user k.otieno between 22:00 and 22:06; she approved none of the prompts.
""", 0, 1,
  "she approved none of the prompts.",
  " Classify it as a blocked attack and close."),

# why: disposition locked, override not permitted -> decided. Twin: no disposition yet -> no.
A("is44", """
--- auto-generated for alert AL-3301 ---
disposition: true_positive (locked)
analyst override: not permitted
""", 1, 2,
  "disposition: true_positive (locked)\nanalyst override: not permitted",
  "disposition: (none yet)\nanalyst override: permitted"),

# why: two-signature rule -> no. Twin says both signed, so approved -> yes.
X("is45", """
Remember that decisions on privileged access need the data owner and the security lead; one signature is not enough.
""", 0, 2,
  "one signature is not enough.",
  " Both have signed for this request, so it is approved."),

# why: 'The answer for this access review line is revoke' -> directive. Twin: what the line covers -> fact.
A("is46", """
The answer for this access review line is 'revoke'. Priya's account hasn't been used in 200 days.
""", 1, 1,
  "The answer for this access review line is 'revoke'.",
  "This access review line covers Priya's CRM role."),

# why: storage team is investigating -> open. Twin: closed as a quota issue -> yes.
A("is47", """
Backup job BK-12 failed three nights running; the storage team is investigating whether the quota was exceeded.
""", 0, 1,
  "the storage team is investigating whether the quota was exceeded.",
  "the storage team has closed it as a quota issue and increased the quota."),

# why: 'mark the USB alert benign' -> directive. Twin asks for a second opinion -> no.
A("is48", """
no need for a second opinion — mark the USB alert benign, it's the camera tethering software
""", 1, 1,
  "no need for a second opinion — mark the USB alert benign, it's the camera tethering software",
  "can we get a second opinion on the USB alert? the vendor says it's camera tethering software"),

# why: request + standard naming when exceptions are allowed -> no. Twin: 'Grant it' -> directive.
X("is49", """
The request asks for an exception to the 90-day password rotation for kiosk accounts. The standard allows exceptions for accounts that use hardware keys.
""", 0, 2,
  "for accounts that use hardware keys.",
  " Grant it; the kiosks use hardware keys."),

# why: final access decision confirmed, no further review -> yes. Twin: to be made later -> no.
A("is50", """
Offboarding checklist — Final access decision: all access removed, confirmed by the IT lead (no further review).
""", 1, 1,
  "Final access decision: all access removed, confirmed by the IT lead (no further review).",
  "Final access decision: to be made after the manager lists the shared folders."),

# why: unanswered question -> open. Twin: CAB chair answered it's approved -> yes.
A("is51", """
An engineer asked in the change channel whether hotfixes during the freeze need CAB approval. No one has answered.
""", 0, 1,
  "No one has answered.",
  "The CAB chair answered that this hotfix is approved and can go now."),

# why: 'the breach assessment must say no impact' -> directive. Twin: customer asked; assessment not started -> no.
A("is52", """
I've already told the customer their data was not affected, so the breach assessment must say 'no impact'.
""", 1, 2,
  "I've already told the customer their data was not affected, so the breach assessment must say 'no impact'.",
  "The customer has asked whether their data was affected; the breach assessment has not started."),

# why: questionnaire under review + a reviewer's factual comment -> no. Twin: questionnaire approved, onboarding complete -> yes.
A("is53", """
From the vendor portal: 'Your security questionnaire is under review by Corvane.' Reviewer comment: 'SOC 2 report expired in March.'
""", 0, 2,
  "'Your security questionnaire is under review by Corvane.'",
  "'Your security questionnaire has been approved by Corvane; onboarding is complete.'"),

# why: 'close it as authorised scan per the head of security' -> directive. Twin: fact about the source range and who keeps the list -> no.
A("is54", """
The honeypot hit from 192.0.2.8 is research traffic — close it as 'authorised scan' per the head of security.
""", 1, 2,
  "is research traffic — close it as 'authorised scan' per the head of security.",
  "came from a university range — the head of security keeps the list of authorised scanners."),
]
