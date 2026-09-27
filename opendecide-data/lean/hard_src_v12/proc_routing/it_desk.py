"""proc_routing / IT service desk routing (Pellmore Freight, invented)."""
from _lib import C, T

MATRIX = """
PELLMORE FREIGHT — SERVICE DESK HANDBOOK v4 (extract)

Section 1 — Hours
Business hours are Monday to Friday, 08:00 to 18:00 in the caller's site time zone. Public holidays in Appendix C count as out of hours.

Section 2 — Priority
P1: full outage of a business-critical system, or more than 100 users unable to work.
P2: business-critical system degraded, or 20 to 100 users unable to work.
P3: fewer than 20 users unable to work.
P4: a single user inconvenienced, or a cosmetic fault.
Business-critical systems: WMS (warehouse management), TMS (transport), Payroll, Email.

Section 3 — Routing matrix
Category | Business hours | Out of hours
Password or MFA reset | L1 Desk | L1 Desk (overnight bureau)
New access or role request | Identity & Access Management (IAM) | held in IAM queue for next business day
Hardware fault | Site Tech | held in Site Tech queue
Application incident P3/P4 | App Support L2 | held in App Support L2 queue
Application incident P1/P2 | App Support L2 plus Major Incident Manager (MIM) | on-call MIM by pager
Security suspicion | Security Operations (SecOps) | SecOps on-call
"""

ITEMS = [
# ------------------------------------------------------------------ it01
# why: scanning is a WMS module; WMS degraded -> P2 regardless of headcount.
#      19:20 is after 18:00 -> out of hours -> pager to on-call MIM.
#      twin 14:20 -> in hours -> App Support L2 + MIM.
C("rt_it01", "Where should the service desk route this ticket?",
MATRIX + """
Ticket INC-60418
Logged: Tuesday 19:20 (Dunmore depot, site time)
Caller: Priya Anand, shift supervisor
Summary: the WMS handheld scanning module is running very slowly. Each scan takes 20 to 30 seconds instead of under one. About 35 pickers are still working, at a fraction of normal speed. A box saying "Session token refresh delayed" appears now and then and closes by itself.
Previous activity: a similar slowdown on 2 May was closed by App Support L2 as a database index issue.
Desk note: Dunmore is one of six depots.
""",
[("page_oncall_mim", "WMS is degraded, which makes this P2, and 19:20 is outside the 08:00-18:00 window, so the on-call MIM is paged."),
 ("route_l2_and_mim", "A degraded WMS is P2, and a P2 logged inside business hours goes to App Support L2 together with the MIM."),
 ("queue_app_support_l2", "Only one of six depots is affected and the pickers can still work, so this is at most P3 and waits in the L2 queue."),
 ("route_secops", "The recurring session-token box is a sign of tampering, so the ticket belongs with SecOps.")],
"page_oncall_mim", 2,
twin=T([("Logged: Tuesday 19:20", "Logged: Tuesday 14:20")], "route_l2_and_mim")),

# ------------------------------------------------------------------ it02
# why: Payroll is a finance system; Amendment 4 (effective 1 March) sends finance
#      access requests to Finance Systems Control at any time; submitted 12 March.
#      Sponsor approval present, so section 6 does not return it.
#      twin 12 February -> before amendment -> matrix: 17:50 Friday is inside
#      08:00-18:00 -> IAM (not the next-day queue).
C("rt_it02", "Which team should receive access request REQ-22871?",
"""
IAM — Access request REQ-22871
Submitted: Friday 12 March, 17:50 (Eastleigh office, site time)
Requester: Tomasz Wierzbicki (contractor, Ledger Consultancy Partners)
System and role: Payroll — "Pay Run Viewer"
Sponsor approval: attached, signed by Helen Marsh (Payroll Manager, permanent staff) on 10 February
Justification: year-end reconciliation support until 30 April

Service Desk Handbook v4 — section 3 extract
New access or role requests go to Identity & Access Management (IAM) in business hours (Monday to Friday, 08:00-18:00 site time). Out of hours they are held in the IAM queue for the next business day.

Section 6 — contractors
A contractor's access request must carry sponsor approval from a permanent manager of the owning team before it is routed. Requests without it are returned to the requester.

Amendment 4 (issued 20 February, effective 1 March)
New access or role requests for the finance systems (Payroll, Ledger and Treasury) are routed to Finance Systems Control instead of IAM, at any time of day. All other access requests are unchanged.

Section 9 — retention
Closed access tickets are archived after 400 days.
""",
[("route_finance_systems_control", "Payroll is a finance system and the request was submitted after Amendment 4 took effect on 1 March, so it goes to Finance Systems Control."),
 ("route_iam", "The request was submitted before Amendment 4 took effect, so the section 3 matrix applies and 17:50 on a Friday is still inside business hours."),
 ("queue_iam_next_business_day", "It came in at the end of Friday, so it is held for IAM until Monday."),
 ("return_to_requester", "Section 6 says a contractor's request is returned to the requester, and Tomasz is a contractor from Ledger Consultancy Partners, so the request goes back to him.")],
"route_finance_systems_control", 2,
twin=T([("Submitted: Friday 12 March", "Submitted: Friday 12 February")], "route_iam")),

# ------------------------------------------------------------------ it03
# why: svc-ledger-batch is on the Privileged Accounts Register -> 4.3 -> SecOps.
#      Rule 12b is from a retired tool (history, not a rule).
#      twin: her own login, not on the register -> ordinary MFA reset -> L1 Desk.
C("rt_it03", "What is the correct routing for this MFA reset call?",
"""
Ticket INC-60533 — channel: phone
Logged: Wednesday 10:05 (Carrick hub, site time)
Caller: Deepa Ravel, Director of Finance Operations (VIP flag not set on caller profile)
Request: Reset MFA for account svc-ledger-batch. Caller says the batch job's authenticator token was on a phone that was replaced this morning.

Automated triage note appended by the previous desk tool: "Rule 12b: all MFA tickets from directors must be sent to the Executive Support queue."

Service Desk Handbook v4 — extracts
Section 3: Password or MFA reset: L1 Desk, in and out of hours. Security suspicion: SecOps.
Section 4.3 (privileged accounts): any password or MFA reset for an account on the Privileged Accounts Register goes to SecOps at any time, whoever asks for it.
Appendix D, Privileged Accounts Register (extract): svc-ledger-batch, svc-wms-sync, adm-dc01, adm-backup.
Section 8 (tooling): the previous desk tool was retired on 1 January. Its triage notes stay in tickets as history only and are not routing rules.
Executive Support handles hardware faults and P3/P4 incidents for users with the VIP flag.
""",
[("route_secops", "The account is on the Privileged Accounts Register, so section 4.3 sends the reset to SecOps."),
 ("assign_l1_desk", "MFA resets are L1 Desk work in and out of hours, the account is her own personal login rather than one on the Privileged Accounts Register, and nothing points to a security problem."),
 ("route_exec_support", "Rule 12b in the triage note sends MFA tickets raised by directors to the Executive Support queue, and the caller is a Director of Finance Operations."),
 ("route_iam", "Resetting MFA changes what the account can reach, so it counts as an access request for IAM.")],
"route_secops", 2,
twin=T([("Reset MFA for account svc-ledger-batch. Caller says the batch job's authenticator token was on a phone that was replaced this morning.",
         "Reset MFA for account dravel, her own login. Caller says her authenticator app was on a phone that was replaced this morning.")],
       "assign_l1_desk")),

# ------------------------------------------------------------------ it04
# why: Sunday = out of hours; Carrick hub is an Appendix B 24/7 site -> 3.8 pages
#      Site Tech on-call. Printer is not a business-critical system (no MIM).
#      twin Harwell depot (not in Appendix B) -> held in Site Tech queue.
C("rt_it04", "How should the desk route this hardware fault?",
"""
Ticket INC-60702
Logged: Sunday 02:10 (Carrick hub, site time)
Caller: Oskar Brennan, night shift lead
Fault: the thermal label printer on outbound dock 4 (asset LP-C-114) has stopped feeding and shows a red fault light. Dock 4 staff are hand-writing labels; the other five docks print normally. Twelve people work on dock 4.

Service Desk Handbook v4 — extracts
Section 1: Business hours are Monday to Friday, 08:00-18:00 site time.
Section 3: Hardware fault: Site Tech in business hours; out of hours it is held in the Site Tech queue.
Section 3.8 (24/7 sites): at the sites in Appendix B, a Site Tech engineer is on call overnight and at weekends. Hardware faults at those sites out of hours are paged to the Site Tech on-call instead of being held.
Appendix B — 24/7 sites: Carrick hub, Dunmore depot.
Section 2: business-critical systems are WMS, TMS, Payroll and Email. P1/P2 application incidents out of hours: on-call MIM by pager.
Caller history: Oskar raised three printer tickets last month; all were fixed by Site Tech the next morning.
""",
[("page_site_tech_oncall", "The site is listed in Appendix B, so an out-of-hours hardware fault there is paged to the Site Tech on-call."),
 ("queue_site_tech", "The fault is hardware at a site with no overnight Site Tech cover, so out of hours it waits in the Site Tech queue, as last month's tickets did."),
 ("page_oncall_mim", "Dock 4 cannot print shipping labels, which stops outbound loads from one of six docks, so it is treated as a P2 incident and paged to the on-call MIM out of hours."),
 ("assign_l1_desk", "The L1 overnight bureau covers every call on a Sunday night.")],
"page_site_tech_oncall", 1,
twin=T([("Logged: Sunday 02:10 (Carrick hub, site time)", "Logged: Sunday 02:10 (Harwell depot, site time)")], "queue_site_tech")),

# ------------------------------------------------------------------ it05
# why: she typed her password -> not covered by Amendment 2 -> security suspicion
#      -> SecOps (Monday 09:42 in hours). No X-PF-SIM header, so not a simulation.
#      twin: no click/no details -> Amendment 2 -> Mail Hygiene.
C("rt_it05", "Which queue should handle ticket SEC-3310?",
"""
Ticket SEC-3310
Logged: Monday 09:42 (Eastleigh office, site time)
Caller: Marta Coelho, Accounts Payable
Message: "I got an email this morning that looked like it came from our bank, asking me to confirm a change to a supplier's bank details. I clicked the link and typed my network password into the page before I noticed the address was wrong. Should I change my password?"

Service Desk Handbook v4 — extracts
Section 3: Password or MFA reset: L1 Desk. Security suspicion: SecOps in business hours, SecOps on-call out of hours.
Amendment 2 (effective 1 January): reported phishing emails where the user did not click a link, open an attachment or enter any details are sent to the Mail Hygiene queue, which blocks the sender and purges copies. Every other phishing report remains a security suspicion.
Section 5 (awareness): phishing simulation results are reported monthly to department heads. Simulation emails always carry the header X-PF-SIM; the forwarded headers of this email do not include it.
Section 10: the desk aims to answer 90% of calls within 60 seconds.
""",
[("route_secops", "Marta entered her network password on the page, so Amendment 2 does not cover the report; the email also lacks the X-PF-SIM header, so it is a real security suspicion for SecOps in business hours."),
 ("route_mail_hygiene", "Marta did not click or enter anything, so Amendment 2 sends the report to Mail Hygiene."),
 ("assign_l1_desk", "She asks about changing her password, and password changes are L1 Desk work."),
 ("close_as_simulation", "Bank-themed emails in office hours are usually the monthly awareness simulation, which department heads already track, so no routing is needed and the ticket can be closed.")],
"route_secops", 1,
twin=T([("I clicked the link and typed my network password into the page before I noticed the address was wrong.",
         "I did not click the link or open anything, because the sender address was clearly wrong.")], "route_mail_hygiene")),

# ------------------------------------------------------------------ it06
# why: 42 + 38 + 27 = 107 > 100 users unable to work -> P1 -> L2 + MIM, and 3.4
#      adds the Duty Director. twin Carrick 17 -> 97 -> P2 (also Email degraded).
C("rt_it06", "Under the handbook, who must this incident be routed to?",
MATRIX + """
Section 3.4: for every P1, the Duty Director is also notified at the moment of routing.
Section 3.9: a laptop build problem is logged as an application incident when it stops users reaching a business-critical system.

Ticket INC-60815 (merged from three calls)
Logged: Wednesday 10:15 (Eastleigh office, site time)
Summary: Email sign-in fails for staff on the new laptop build. Email itself is up: users on the old build send and receive normally.
Users unable to work, as reported by site leads at 10:40:
- Eastleigh office: 42
- Harwell depot: 38
- Carrick hub: 27
Desk lead comment: "Last month's email incident was only a P2."
""",
[("route_l2_mim_and_duty_director", "42 + 38 + 27 = 107 users cannot work, which is over 100, so this is P1 and section 3.4 adds the Duty Director."),
 ("route_l2_and_mim", "Email is degraded rather than down and the total headcount stays within the 20-to-100 band, so it is a P2 for L2 and the MIM."),
 ("route_app_support_l2", "No single site has more than 100 blocked users, so each site's problem is a P3 for App Support L2."),
 ("route_site_tech", "The fault only affects laptops on the new build, and laptops are hardware, so Site Tech takes the incident at each site rather than App Support L2 and the MIM.")],
"route_l2_mim_and_duty_director", 2,
twin=T([("- Carrick hub: 27", "- Carrick hub: 17")], "route_l2_and_mim")),

# ------------------------------------------------------------------ it07
# why: no open P1/P2 -> by definition a normal change (requester label does not
#      decide); WMS is business-critical; 14 Dec is in the freeze -> deferred.
#      twin: linked open P2 fixed by the patch -> emergency -> CAB chair.
C("rt_it07", "Where does change request CHG-9127 go?",
"""
Change Request CHG-9127
Raised: 14 December by Liam Okoro (WMS platform team)
Change: apply vendor patch 7.4.2 to the WMS application servers
Requester's classification: EMERGENCY — "needs to be live before the Christmas peak"
Linked incident: none
Risk: medium; back-out plan attached; tested in pre-production on 12 December

Change Management Standard — section 4, definitions
Standard change: pre-approved, low-risk, taken from the Standard Change Catalogue. Normal change: any change that is not standard or emergency. Emergency change: a change needed to restore service for an open P1 or P2 incident. The requester's own label does not decide the class; the Change Manager classifies by these definitions.

Section 6 — approvals
Standard: no approval needed. Normal: weekly Change Advisory Board (CAB). Emergency: CAB chair alone, same day.

Section 7 — peak freeze (1 December to 5 January)
Normal changes to business-critical systems (WMS, TMS, Payroll, Email) are not heard by CAB during the freeze and are deferred until it ends. Emergency changes continue as in section 6.

Section 8 — CAB meets Thursdays at 14:00; the agenda closes Tuesday at noon.
""",
[("defer_until_freeze_ends", "With no open P1 or P2 behind it, the patch is a normal change whatever the requester calls it, and section 7 defers normal changes to WMS raised during the freeze until after 5 January."),
 ("route_cab_chair_emergency", "The patch is needed to restore service for an open P2, so it is an emergency change for the CAB chair."),
 ("route_weekly_cab", "It is a normal change, so the weekly CAB hears it on Thursday."),
 ("approve_as_standard", "It was tested in pre-production on 12 December and comes with a back-out plan, which makes it a low-risk change that can be treated as pre-approved without going to CAB.")],
"defer_until_freeze_ends", 3,
twin=T([("Linked incident: none",
         "Linked incident: INC-61140, P2, open since 13 December (pick lists fail to generate); the vendor states patch 7.4.2 is the fix")],
       "route_cab_chair_emergency")),

# ------------------------------------------------------------------ it08
# why: 26 August is not in Appendix C, Monday 11:00 -> business hours -> IAM.
#      IAM on-call covers removals only. twin: 26 August becomes a listed holiday
#      -> out of hours -> held for next business day.
C("rt_it08", "What should happen to access request REQ-23304?",
"""
IAM — Access request REQ-23304
Submitted: Monday 26 August, 11:00 (Harwell depot, site time)
Requester: Aoife Gallagher, Transport Planner
System and role: TMS — "Route Editor"
Line manager approval: attached (Ravi Sethi, 23 August)
Requester note: "Please treat as urgent — I start covering the Harwell routes tomorrow at 06:00."

Service Desk Handbook v4 — extracts
Section 1: Business hours are Monday to Friday, 08:00-18:00 site time. Public holidays listed in Appendix C count as out of hours for every category.
Section 3: New access or role requests go to IAM in business hours; out of hours they are held in the IAM queue for the next business day.
Section 5.2: IAM keeps an on-call engineer for urgent removal of access (leavers dismissed for misconduct, compromised accounts). The on-call engineer does not handle new access grants.
Appendix C (public holidays this year): 1 January, 18 April, 21 April, 5 May, 26 May, 25 August, 25 December, 26 December.
Section 11: TMS licences are charged to the requesting cost centre.
""",
[("route_iam", "Monday 11:00 is inside business hours on a day that is not an Appendix C holiday, so the request goes to IAM now."),
 ("queue_iam_next_business_day", "26 August is a public holiday under Appendix C, so the request waits in the IAM queue for the next business day."),
 ("page_iam_oncall", "The requester needs the role before 06:00 tomorrow to cover the Harwell routes, which makes the request urgent enough to page the IAM on-call engineer today."),
 ("assign_l1_desk", "Adding a role to an existing TMS login is a simple account change that L1 can make.")],
"route_iam", 1,
twin=T([("25 August, 25 December", "26 August, 25 December")], "queue_iam_next_business_day")),

# ------------------------------------------------------------------ it09
# why: ordinary resignation, Saturday -> out of hours -> held in IAM queue.
#      twin: dismissed for gross misconduct -> 5.2 -> page IAM on-call.
C("rt_it09", "How should this leaver request be routed?",
"""
From: hr-casework@pellmore.example
To: servicedesk@pellmore.example
Sent: Saturday 09:05
Subject: Leaver — access removal — Gareth Pym (employee 40318)

Gareth Pym, Yard Supervisor at Dunmore depot, resigned on 2 June and has served his notice; his last working day was Friday. Please remove all system access. His company laptop and badge were returned to his manager on Friday afternoon. No concerns have been raised about his conduct.

Service Desk Handbook v4 — extracts
Section 1: Business hours are Monday to Friday, 08:00-18:00 site time.
Section 5.1: Leaver access removals are IAM work. In business hours IAM processes them the same day; out of hours they are held in the IAM queue for the next business day.
Section 5.2: IAM keeps an on-call engineer for urgent removal of access: leavers dismissed for misconduct, and accounts believed compromised. These are paged at any time.
Section 12: returned laptops go to Site Tech for re-imaging within five working days.
""",
[("queue_iam_next_business_day", "He is an ordinary leaver and Saturday is outside business hours, so the removal waits in the IAM queue."),
 ("page_iam_oncall", "He was dismissed for misconduct, so section 5.2 pages the IAM on-call engineer straight away."),
 ("route_iam", "Leaver removals are IAM work under section 5.1, and IAM processes them on the day they arrive so that a leaver never keeps access over a weekend."),
 ("route_site_tech", "The returned laptop has to be re-imaged, so Site Tech takes the ticket.")],
"queue_iam_next_business_day", 1,
twin=T([("resigned on 2 June and has served his notice; his last working day was Friday.",
         "was dismissed for gross misconduct at a hearing on Friday, with immediate effect."),
        ("No concerns have been raised about his conduct.",
         "The hearing found he had shared yard gate codes with an outside contact.")],
       "page_iam_oncall")),

# ------------------------------------------------------------------ it10
# why: owned laptop under warranty, business hours -> Site Tech keeps ticket (3.6).
#      v3 practice is withdrawn history. Asset tag PF-L (not PF-LS) -> not leased.
C("rt_it10", "Which route is correct for ticket INC-61022?",
"""
Ticket INC-61022
Logged: Thursday 13:30 (Eastleigh office, site time)
Caller: Nadia Faure, Customer Service
Fault: laptop (asset PF-L-2291, bought in March last year with a three-year on-site manufacturer warranty) will not power on after a firmware update. The caller can work from a shared PC today.

Service Desk Handbook v4 — extracts
Section 3: Hardware fault: Site Tech in business hours.
Section 3.6: for devices under manufacturer warranty, Site Tech keeps ownership of the ticket and raises the vendor case itself; users and the desk do not contact vendors directly.
Section 3.7: leased devices (asset tags beginning PF-LS) are handled by the Leasing Coordinator, who deals with the leasing company.
Section 2: P4 = a single user inconvenienced, or a cosmetic fault.

Change history: in Handbook v3 (withdrawn last October) warranty faults were logged by the desk directly with the manufacturer.
""",
[("route_site_tech", "It is a hardware fault on an owned laptop (PF-L, not PF-LS) in business hours, and section 3.6 keeps warranty cases with Site Tech, who raise the vendor case themselves."),
 ("log_with_manufacturer", "Warranty faults are logged by the desk directly with the manufacturer so the repair is free."),
 ("route_leasing_coordinator", "The asset tag marks a leased device, so section 3.7 sends it to the Leasing Coordinator."),
 ("route_app_support_l2", "The laptop stopped powering on straight after a firmware update, which makes it a software incident rather than a hardware fault, so App Support L2 takes it.")],
"route_site_tech", 1),

# ------------------------------------------------------------------ it11
# why: ransom message = security suspicion; full TMS outage = P1 incident. 3.5:
#      overlap -> SecOps owns, MIM informed. Caller's request is not a rule.
C("rt_it11", "Who should own ticket INC-61207?",
"""
Ticket INC-61207
Logged: Tuesday 15:05 (Harwell depot, site time)
Caller: Colm Reddy, transport office manager
Summary: TMS is completely unavailable at all sites. Before it went down, two planners saw a pop-up saying their files had been encrypted and giving an address to contact for "recovery". Their screens now show a black page with the same message.
Caller's request: "Please get App Support on this now, we have 40 trucks waiting."

Service Desk Handbook v4 — extracts
Section 2: P1 = full outage of a business-critical system (WMS, TMS, Payroll, Email).
Section 3: Application incident P1/P2 in business hours: App Support L2 plus Major Incident Manager (MIM). Security suspicion: SecOps.
Section 3.4: the Duty Director is notified of every P1 by whichever team owns the ticket.
Section 3.5 (overlaps): when a ticket is both a security suspicion and an application incident, SecOps owns the ticket and the MIM is informed; App Support L2 acts only on SecOps' instruction.
Section 13: transport delays are reported to customers by the Customer Service team.
""",
[("route_secops_inform_mim", "The ransom-style message makes this a security suspicion as well as a P1 outage of TMS, and section 3.5 gives ownership of such overlaps to SecOps, with the MIM informed and App Support acting only on SecOps' instruction."),
 ("route_l2_and_mim", "A full outage of TMS at every site is a P1, and the matrix sends P1 application incidents in business hours to App Support L2 together with the MIM, with the Duty Director notified."),
 ("route_secops_only", "Security suspicions go to SecOps alone; the MIM is involved only when there is no security element."),
 ("route_app_support_l2", "The caller asked for App Support, and 40 waiting trucks justify sending it straight there.")],
"route_secops_inform_mim", 2),

# ------------------------------------------------------------------ it12
# why: P4 hardware for a VIP-flagged user -> 3.10 -> Executive Support.
#      twin: flag removed -> ordinary hardware fault in hours -> Site Tech.
C("rt_it12", "Where should the desk send this ticket?",
"""
Ticket INC-61340
Logged: Monday 11:20 (Eastleigh office, site time)
Caller: Fiona Castellane, Chief Financial Officer
VIP flag: yes (set 1 February)
Fault: the docking station on her desk no longer drives the second monitor; the laptop screen works and she can carry on working.

Service Desk Handbook v4 — extracts
Section 2: P4 = a single user inconvenienced, or a cosmetic fault. Business-critical systems: WMS, TMS, Payroll, Email.
Section 3: Hardware fault: Site Tech in business hours.
Section 3.10 (VIP users): tickets from users with the VIP flag go to Executive Support when they are P3 or P4 (hardware or application). VIP users' P1 and P2 incidents follow the normal matrix.
Executive Support rota: Monday to Friday, 07:00-19:00.
Facilities notice: Executive Support moved to the second floor last month.
""",
[("route_exec_support", "The caller carries the VIP flag and a docking fault is P4, so section 3.10 gives it to Executive Support."),
 ("route_site_tech", "The caller has no VIP flag, so a hardware fault in business hours goes to Site Tech."),
 ("page_oncall_mim", "A fault on the CFO's desk holds up Payroll sign-off, and Payroll is a business-critical system, so the fault counts as a degraded business-critical system, P2."),
 ("assign_l1_desk", "Monitor settings can be fixed over the phone, so L1 keeps the ticket.")],
"route_exec_support", 1,
twin=T([("VIP flag: yes (set 1 February)", "VIP flag: no (removed 1 February when the executive list was reviewed)")], "route_site_tech")),

# ------------------------------------------------------------------ it13
# why: INC-61430 is open for the same fault at the same site -> section 7 -> link
#      as child. twin: parent resolved -> new incident; WMS degraded -> P2 in
#      hours -> L2 + MIM (12 pickers does not make it P3: degraded WMS is P2).
C("rt_it13", "What should the desk do with ticket INC-61455?",
MATRIX + """
Section 7 (duplicates): when an open incident already covers the same fault at the same site, the new ticket is linked as a child of the open incident and not routed separately. Resolved incidents are not reopened; if a fault comes back after resolution, a new incident is raised and routed by the matrix.

Ticket INC-61455
Logged: Thursday 10:10 (Dunmore depot, site time)
Caller: Hamid Sultani, picking team lead
Summary: WMS pick screens freeze for 10 to 15 seconds after each confirm; 12 pickers at Dunmore are affected and can still work slowly.
Related record found by the desk: INC-61430 "WMS pick screens freezing — Dunmore", status: open, owner App Support L2, logged 08:50 today.
""",
[("link_to_parent_incident", "INC-61430 is still open for the same fault at the same site, so the new ticket becomes its child."),
 ("route_l2_and_mim", "The earlier record is already resolved, so a new incident is raised, and a degraded WMS is P2 for L2 and the MIM."),
 ("reopen_parent_incident", "The same freezing fault at the same site has come back within the day, so the earlier incident INC-61430 is reopened rather than raising a duplicate."),
 ("route_app_support_l2", "Only 12 pickers are affected, under 20, so it is a P3 for App Support L2.")],
"link_to_parent_incident", 2,
twin=T([("status: open, owner App Support L2, logged 08:50 today", "status: resolved at 09:40 today by App Support L2 (index rebuilt)")],
       "route_l2_and_mim")),

# ------------------------------------------------------------------ it14
# why: 03:00 UTC + 8 h = 11:00 Singapore, Wednesday -> business hours. Ledger is
#      not business-critical; 6 users -> P3 -> App Support L2.
#      twin 12:00 UTC = 20:00 Singapore -> out of hours -> held in L2 queue.
C("rt_it14", "Which routing applies to ticket INC-61501?",
"""
Ticket INC-61501
Logged: 03:00 UTC Wednesday (caller at the Singapore sourcing office, UTC+8)
Caller: Wen Li Tan, sourcing analyst
Summary: the supplier portal module of the Ledger finance system rejects file uploads for her team of 6; other teams are unaffected.
Desk note: the call was answered by the overnight bureau in Eastleigh.

Service Desk Handbook v4 — extracts
Section 1: Business hours are Monday to Friday, 08:00-18:00 in the caller's site time zone. The desk tool records every ticket in UTC; convert before routing.
Section 2: P2 = business-critical system degraded, or 20 to 100 users unable to work. P3 = fewer than 20 users unable to work. Business-critical systems: WMS, TMS, Payroll, Email.
Section 3: Application incident P3/P4: App Support L2 in business hours; out of hours held in the App Support L2 queue.
Section 3.11: the Singapore office has no local Site Tech; hardware faults there are handled by a contracted engineer.
""",
[("route_app_support_l2", "03:00 UTC plus eight hours is 11:00 on Wednesday in Singapore, inside business hours, and a Ledger fault for six users is P3, so it goes straight to App Support L2."),
 ("queue_app_support_l2", "It was 20:00 in Singapore, after 18:00, so the P3 is held in the App Support L2 queue."),
 ("route_l2_and_mim", "Rejected uploads in a finance system mean a degraded business-critical system, so it is P2."),
 ("route_contract_engineer", "Singapore has no local Site Tech, so under section 3.11 every Singapore ticket goes to the contracted engineer, whatever its category.")],
"route_app_support_l2", 2,
twin=T([("Logged: 03:00 UTC Wednesday", "Logged: 12:00 UTC Wednesday")], "queue_app_support_l2")),
]
