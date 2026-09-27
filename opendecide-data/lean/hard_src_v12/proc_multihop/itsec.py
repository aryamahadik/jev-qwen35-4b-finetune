"""proc_multihop / IT operations and security procedures (Orvane Bank Services,
Talmead Retail, Quenby Software, Hesketh Insurance, Lowmarsh Council IT)."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ it01
# why: billing-db is Tier 1 (register). Both approvals present, training 4 months ago
# (within 12). Contractor -> Tier 1 access capped at 30 days (5.3) -> approve for 30
# days, not 90. Twin: permanent employee -> up to 12 months -> approve as requested.
C("it01", "What should the access team do with request AR-6604?",
"""
Orvane Bank Services — Logical Access Standard (extract)

1. Definitions
1.1 Tier 1 system: a system that stores or processes customer payment data. The System Register is the authority.
1.2 Contractor: anyone engaged through an agency or as a sole trader rather than on the payroll.

5. Tier 1 access
5.1 Needs approval from the requester's line manager and from the system owner.
5.2 The requester must have completed "Secure Data Handling" training in the last 12 months.
5.3 Contractors may be granted Tier 1 access for at most 30 days at a time; renewals need fresh approvals.
5.4 Employees may be granted access for the period requested, up to 12 months.

System Register (extract)
| System | Data | Tier |
| billing-db | card tokens, payment history | 1 |
| docs-wiki | internal documentation | 3 |

Request AR-6604
Requester: Marek Hollis — Employment type: contractor (Vantor Staffing)
System: billing-db, read-only
Period requested: 90 days (migration project)
Line manager: approved 3 June. System owner: approved 4 June.
Training record: Secure Data Handling completed 11 February (4 months ago).
""",
[("approve_as_requested", "Both approvals are in place and training is current, so the 90-day read-only access can be granted."),
 ("approve_for_30_days", "Approvals and training are in order, but as a contractor he can hold Tier 1 access for at most 30 days at a time."),
 ("reject_training_lapsed", "His Secure Data Handling training is out of date for Tier 1 access."),
 ("reject_contractor_barred", "Contractors may not be given access to Tier 1 systems.")],
"approve_for_30_days", 2,
twin=T([("Employment type: contractor (Vantor Staffing)", "Employment type: permanent employee")], "approve_as_requested")),

# ------------------------------------------------------------------ it02
# why: 22 Dec falls in freeze 18 Dec-3 Jan; catalogue standard changes suspended during
# freeze (note 2). Emergency = prevents outage within 48 h; cert expires 9 Jan -> no.
# So normal change in freeze -> CAB + VP exception. Twin: expires 23 Dec 09:00 (within
# 48 h of 22 Dec) -> emergency change.
C("it02", "Which change route must CHG-3310 follow to go ahead on 22 December?",
"""
Talmead Retail — Change Management Procedure (extract)

1. Change types
1.1 Standard: a change listed in the Standard Change Catalogue; pre-approved, no CAB.
1.2 Emergency: a change needed to fix an active outage or security incident, or to prevent one expected within the next 48 hours. Approved by the on-call director.
1.3 Normal: any other change. Needs CAB approval.

2. Change freeze
2.1 Freeze period: 18 December to 3 January inclusive.
2.2 During a freeze, the Standard Change Catalogue does not apply; every non-emergency change is treated as Normal and also needs a written VP exception.

Standard Change Catalogue (extract)
| ID | Change |
| SC-09 | add a user to an existing AD group |
| SC-14 | renew TLS certificate on a public web server |

CHG-3310
Summary: renew TLS certificate on shop.talmead.example (public web server)
Planned: 22 December, 06:00
Reason: current certificate expires 9 January.
Requester comment: "This is SC-14, so it's pre-approved."
""",
[("proceed_as_standard", "The change matches catalogue entry SC-14 exactly, so it is pre-approved as a Standard change and needs no CAB or other sign-off."),
 ("cab_plus_vp_exception", "The freeze suspends the catalogue and the expiry is not within 48 hours, so it is a Normal change needing CAB and a VP exception."),
 ("emergency_change", "The certificate expires within 48 hours of the planned change, so the change prevents an expected outage and is an emergency.")],
"cab_plus_vp_exception", 2,
twin=T([("Reason: current certificate expires 9 January.", "Reason: current certificate expires 23 December at 09:00.")], "emergency_change")),

# ------------------------------------------------------------------ it03
# why: service catalogue lists Search as Tier 2; full outage of a Tier 2 service -> SEV2.
# No data exposure. Customer's "SEV1" claim is irrelevant. Twin: Search listed as Tier 1
# and outage 40 min > 15 -> SEV1.
C("it03", "What severity should the incident commander set for INC-9021?",
"""
Quenby Software — Incident Severity Matrix

SEV1: customer data exposed to an unauthorised party, or a full outage of a Tier 1 service lasting more than 15 minutes.
SEV2: a partial degradation of a Tier 1 service, or a full outage of a Tier 2 service.
SEV3: anything else, including full outages of Tier 3 services.
Service tier is taken from the Service Catalogue, not from customer contracts.

Service Catalogue (extract)
| Service | Tier |
| Checkout API | 1 |
| Search | 2 |
| Status page | 3 |

INC-9021 timeline
10:02 Alerts: Search returns HTTP 503 for all queries.
10:05 Checkout API healthy; customers can still buy from product links.
10:31 Customer Brightfold Ltd emails: "Search is critical for us, this must be treated as SEV1."
10:42 Search restored after a config rollback. Total outage 40 minutes.
10:50 Logs reviewed: no data exposure.
""",
[("sev1", "The outage lasted 40 minutes, well over the 15-minute limit, on a service that the catalogue ranks at the top tier."),
 ("sev2", "Search had a full outage and the catalogue ranks it as a second-tier service, with no data exposed."),
 ("sev3", "Customers could still buy through product links, so the outage was minor.")],
"sev2", 1),

# ------------------------------------------------------------------ it04
# why: invoices statutory 7y -> kept. Legal hold LH-12 covers support tickets of accounts
# in dispute DS-44; account 55012 is listed in DS-44 -> tickets kept. Marketing profile
# not statutory, not held -> erase. Twin: DS-44 lists 55021 (not 55012) -> tickets not
# held and only business retention -> erase all except invoices.
C("it04", "How should the privacy team action erasure request ER-219 for account 55012?",
"""
Hesketh Insurance — Records Retention Schedule and Erasure Rule

Erasure rule: on a valid erasure request, delete the customer's records unless (a) the record type has a retention period marked "statutory", or (b) a legal hold in the Legal Hold Register covers the record.

Retention schedule
| Record type | Retention | Basis |
| Invoices and payment records | 7 years | statutory |
| Support tickets and emails | 2 years | business |
| Marketing profile | until opt-out | consent |

Legal Hold Register
| Hold | Scope | Accounts |
| LH-12 | support tickets and emails | accounts in dispute DS-44: 55012, 55387 |
| LH-15 | call recordings | account 61220 |

Request ER-219
Account: 55012
Received: 2 March. Identity verified.
Customer: "Please delete everything you hold about me."
Records found: 14 invoices (2023-2025), 6 support tickets, 1 marketing profile.
""",
[("erase_everything", "The customer has asked for full erasure and has verified identity, so all records are deleted."),
 ("erase_all_except_invoices", "Only invoices carry a statutory period, and no hold covers this account's other records."),
 ("erase_marketing_only", "Invoices are statutory and a legal hold covers this account's support tickets, so only the marketing profile is deleted."),
 ("refuse_erasure", "An account named in a legal hold is exempt from erasure altogether.")],
"erase_marketing_only", 3,
twin=T([("accounts in dispute DS-44: 55012, 55387", "accounts in dispute DS-44: 55021, 55387")], "erase_all_except_invoices")),

# ------------------------------------------------------------------ it05
# why: MFA exceptions only for service accounts; amendment: service account with
# interactive login enabled counts as a human account -> never exempt -> deny.
# Team lead approval irrelevant. Twin: interactive login disabled -> service account,
# 60 days <= 90 -> route to CISO.
C("it05", "What should the identity team do with MFA exception request MX-47?",
"""
Lowmarsh Council IT — Multi-Factor Authentication Policy

2. Scope: every account must use MFA unless an exception is granted under section 4.
3. Definitions: a "service account" is a non-human account listed in the Service Account Register.
4. Exceptions
4.1 Human accounts cannot be exempted.
4.2 A service account may be exempted for up to 90 days with approval from the CISO.
4.3 Team leads may not approve exceptions.

Amendment 2 (from 1 March): a service account with interactive login enabled is treated as a human account for this policy.

Service Account Register (extract)
| Account | Owner team | Interactive login |
| svc-reporting | Data & Insight | enabled |
| svc-backup | Infrastructure | disabled |

Request MX-47
Account: svc-reporting
Duration: 60 days
Reason: overnight report job fails at the MFA prompt.
Approvals attached: team lead (R. Castell) — approved.
""",
[("deny_exception", "Because interactive login is enabled, the account counts as a human account, and human accounts cannot be exempted."),
 ("route_to_ciso", "It is a registered service account asking for no more than 90 days, so it goes to the CISO for approval."),
 ("grant_on_team_lead_approval", "The team lead has approved the exception and 60 days is inside the 90-day limit for service accounts, so it can be granted now.")],
"deny_exception", 2,
twin=T([("| svc-reporting | Data & Insight | enabled |", "| svc-reporting | Data & Insight | disabled |")], "route_to_ciso")),

# ------------------------------------------------------------------ it06
# why: catalogue entries are per major version; PixelTrim 3.x is Category A but 4.x is
# Category C (not reviewed) -> 4.2 needs security review. Blocked list has only the
# Cloud Sync plugin. Twin: request 3.9 -> Category A -> self-install.
C("it06", "How should the service desk handle software request SR-1180?",
"""
Quenby Software — End-User Software Rules

1. Catalogue entries apply to the major version listed; a new major version is a new product for these rules.
2. Category A: approved, free for business use. Users may self-install from the portal.
3. Category B: approved but licensed. Raise a licence ticket before installing.
4. Category C: not yet reviewed. Submit for security review; do not install.
5. Blocked software may never be installed.

Software Catalogue (extract)
| Product | Version | Category |
| PixelTrim | 3.x | A |
| PixelTrim | 4.x | C |
| Sketchline Pro | 2.x | B |

Blocked list: PixelTrim Cloud Sync plugin; any peer-to-peer file sharing client.

SR-1180
User: Dana Okafor (Marketing)
Request: install PixelTrim 4.2 (image cropping) on laptop QS-L-3302. The Cloud Sync plugin is not needed.
Note: "PixelTrim is already approved, I used it on my old laptop."
""",
[("self_install_allowed", "The requested version is covered by a Category A catalogue entry, so the user may install it from the portal."),
 ("raise_licence_ticket", "PixelTrim needs a paid licence, so a licence ticket comes first."),
 ("hold_for_security_review", "Version 4 is a separate catalogue entry that has not been reviewed, so it goes to security review."),
 ("refuse_blocked", "PixelTrim appears on the blocked list.")],
"hold_for_security_review", 2),

# ------------------------------------------------------------------ it07
# why: definition: involuntary includes any departure where the employee is placed on
# garden leave -> disable immediately. Manager's handover wish does not override.
# Twin: she works her notice -> voluntary -> 17:00 on last working day.
C("it07", "When should Leah Vance's accounts be disabled?",
"""
Hesketh Insurance — Joiners, Movers and Leavers Procedure (IT)

Definitions
- Voluntary departure: resignation or retirement where the employee works their notice.
- Involuntary departure: dismissal, redundancy, or any departure where the employee is placed on garden leave.

Leaver rules
L1. Voluntary departure: disable all accounts at 17:00 on the last working day.
L2. Involuntary departure: disable all accounts as soon as IT is notified.
L3. Mailboxes of leavers are converted to shared mailboxes for 90 days; the manager receives access.
L4. Line managers cannot ask for accounts to stay active beyond the times in L1 and L2.

HR notification, Monday 09:20
Employee: Leah Vance, Claims Analyst
Reason: resignation (joining a competitor)
Last working day: Friday 27 March
Additional: Leah is placed on garden leave from today.
Manager note: "Can we keep her login until Wednesday so she can finish the handover document?"
""",
[("disable_immediately", "Garden leave makes this an involuntary departure under the definitions, so L2 applies now."),
 ("disable_at_17_last_day", "A resignation is a voluntary departure, so accounts go at 17:00 on 27 March."),
 ("keep_until_wednesday", "The manager has asked for a handover period, which the procedure allows.")],
"disable_immediately", 2,
twin=T([("Additional: Leah is placed on garden leave from today.", "Additional: Leah will work her full notice period.")], "disable_at_17_last_day")),

# ------------------------------------------------------------------ it08
# why: restore in tier order, but R2: any system another failed system depends on is
# restored first. Payroll (Tier 1) depends on Identity (Tier 2) -> identity first.
# Twin: Payroll uses local accounts (no dependency) -> payroll first.
C("it08", "Which system should the recovery team restore first?",
"""
Lowmarsh Council IT — Disaster Recovery Runbook, section 3 (restore order)

R1. Restore failed systems in order of recovery tier (Tier 1 first).
R2. Exception: if a failed system depends on another failed system, the system it depends on is restored first, whatever its tier.
R3. Within a tier, restore the system with the shorter RTO first.

Recovery register
| System | Tier | RTO | Depends on |
| Payroll | 1 | 4 h | Identity service |
| Identity service | 2 | 8 h | none |
| Intranet | 3 | 24 h | Identity service |
| Planning portal | 1 | 6 h | none (still running) |

Situation, 07:30: storage array failure. Payroll, Identity service and Intranet are down. Planning portal is unaffected. The payroll run is due at 14:00.
""",
[("restore_payroll_first", "Payroll is the failed Tier 1 system with the shortest RTO and a deadline today."),
 ("restore_identity_first", "Payroll depends on the Identity service, which is also down, so R2 puts the Identity service first."),
 ("restore_intranet_first", "The Intranet depends on the Identity service, so the two are restored together before anything else."),
 ("restore_planning_portal_first", "The Planning portal is Tier 1 and must be restored ahead of Tier 2 and Tier 3 systems.")],
"restore_identity_first", 2,
twin=T([("| Payroll | 1 | 4 h | Identity service |", "| Payroll | 1 | 4 h | none (local accounts) |")], "restore_payroll_first")),

# ------------------------------------------------------------------ it09
# why: definition: "credentials entered" includes any password, one-time code or
# authenticator code. User typed authenticator code -> credentials entered -> reset,
# revoke sessions, open incident. Twin: user closed the tab without typing -> clicked
# only -> scan device.
C("it09", "Which response does phishing report PH-5503 require?",
"""
Orvane Bank Services — Suspicious Email Playbook

Definitions
- Clicked: the user opened a link or attachment in the reported email.
- Credentials entered: the user typed any password, one-time code or authenticator code into a page reached from the email.

Responses
A. Reported, not clicked: block the sender, thank the user, close.
B. Clicked, no credentials entered: block the sender and run a full device scan.
C. Credentials entered: block the sender, reset the password, revoke all sessions and open a security incident.

Report PH-5503, 11:14
User: Jonah Keel (Treasury)
Email subject: "Action required: payroll portal update"
User's words: "I clicked the button. It showed our login screen but it already had my username filled in and only asked for the code from my authenticator app, so I typed that in. Then the page went blank. I never typed my password."
Mail gateway: sender domain registered 3 days ago.
""",
[("block_and_close", "The user reported the email, so blocking the sender and closing is enough."),
 ("block_and_scan_device", "The user clicked the link but never typed a password, so a device scan covers it."),
 ("reset_revoke_open_incident", "Typing the authenticator code counts as entering credentials, so the full response applies.")],
"reset_revoke_open_incident", 2,
twin=T([("only asked for the code from my authenticator app, so I typed that in. Then the page went blank. I never typed my password.",
         "only asked for the code from my authenticator app, so I closed the tab straight away. I never typed anything.")], "block_and_scan_device")),

# ------------------------------------------------------------------ it10
# why: K-17 scope read-write -> amendment: any key with write scope rotates every 30
# days; last rotated 45 days ago -> overdue. Rule 4: keys unused 60+ days are revoked
# instead; last used 2 days ago -> rotate. Twin: last used 70 days ago -> revoke.
C("it10", "What action does the key audit require for API key K-17?",
"""
Quenby Software — API Key Management Standard

1. Keys are rotated at least every 90 days.
2. (Amended 1 May) Keys whose scope includes write access are rotated at least every 30 days.
3. Rotation means issuing a new key, updating the consumer and revoking the old key within 24 hours.
4. A key not used for 60 days or more is revoked, not rotated.
5. Keys must never be stored in source code.

Key audit, 14 August
| Key | Consumer | Scope | Last rotated | Last used |
| K-11 | reporting job | read | 3 Jul (42 days ago) | 13 Aug |
| K-17 | partner sync | read-write | 30 Jun (45 days ago) | 12 Aug (2 days ago) |
| K-20 | legacy export | read | 2 Mar | 1 Apr |

Auditor note: "K-17 is well inside the 90-day window."
""",
[("no_action", "K-17 was rotated 45 days ago, well within the 90-day rotation period."),
 ("rotate_now", "K-17 has write scope, so its 30-day limit has passed, and it is still in use."),
 ("revoke_key", "K-17 has gone unused for long enough that it must be revoked rather than rotated.")],
"rotate_now", 2,
twin=T([("| 30 Jun (45 days ago) | 12 Aug (2 days ago) |", "| 30 Jun (45 days ago) | 5 Jun (70 days ago) |")], "revoke_key")),

# ------------------------------------------------------------------ it11
# why: loss on 1 March; BitLocker enabled 3 March per register (after the loss) -> device
# unencrypted when lost -> remote wipe + incident + notify DPO. Twin: enabled 3 January
# -> encrypted when lost -> remote wipe and log only.
C("it11", "What does the lost-device procedure require for laptop LT-889?",
"""
Hesketh Insurance — Lost or Stolen Device Procedure

1. Every lost device receives a remote wipe command and is logged in the asset register.
2. If the device was not encrypted at the time of loss, also open a data security incident and notify the Data Protection Officer within 24 hours.
3. Encryption status is taken from the "Encryption enabled" date in the asset register; a device is encrypted from that date onward.
4. Replacement devices are issued by the service desk.

Asset register (extract)
| Asset | User | Encryption enabled |
| LT-874 | S. Adeyemi | 12 Nov (last year) |
| LT-889 | R. Whitlow | 3 March |

Loss report LR-61, received 2 March
User: R. Whitlow. "Left my laptop on the 18:05 train on Saturday 1 March. I reported it to the rail company this morning. It had the new encryption rolled out, I think."
""",
[("wipe_and_log", "The laptop was already encrypted when it was lost, so a remote wipe and an entry in the asset register are all that is needed."),
 ("wipe_log_incident_and_notify_dpo", "Encryption was enabled only after the loss, so the laptop was unencrypted when lost and section 2 applies."),
 ("log_only", "A device reported to the rail company's lost property needs only a log entry until it is found.")],
"wipe_log_incident_and_notify_dpo", 2,
twin=T([("| LT-889 | R. Whitlow | 3 March |", "| LT-889 | R. Whitlow | 3 January |")], "wipe_and_log")),

# ------------------------------------------------------------------ it12
# why: ftp-legacy moved to internal zone (register, updated after migration note). Rule 3:
# no rules from internet to internal zone -> reject. Port 443 is irrelevant.
# Twin: ftp-legacy zone DMZ -> 443 from internet to DMZ -> standard approval.
C("it12", "How should the network team decide firewall request FW-208?",
"""
Talmead Retail — Perimeter Firewall Rules Standard

1. Inbound from the internet to the DMZ on TCP 80 or 443: standard approval by the network team.
2. Inbound from the internet to the DMZ on any other port: needs the security architect's approval.
3. Inbound from the internet to the internal zone: not permitted under any approval.
4. The zone of a server is the one shown in the Server Zone Register.

Server Zone Register (updated 2 June)
| Server | Zone |
| web-front-01 | DMZ |
| ftp-legacy | internal |
| mail-relay | DMZ |
Migration note (April): "ftp-legacy will stay in the DMZ until the file service moves to the cloud." (The move completed on 1 June.)

FW-208, raised 9 June
Source: any (internet)
Destination: ftp-legacy
Port: TCP 443
Reason: supplier upload portal.
""",
[("approve_standard_rule", "The request opens TCP 443 from the internet to a DMZ server, which the network team can approve."),
 ("needs_architect_approval", "An upload portal on a legacy FTP server is a non-standard exposure, so the security architect has to sign off before the rule is added."),
 ("reject_internal_target", "The register shows ftp-legacy in the internal zone, and internet traffic to that zone is never allowed.")],
"reject_internal_target", 2),

# ------------------------------------------------------------------ it13
# why: break-glass allowed only "during" a SEV1 = after declaration, before closure.
# Used 02:10, SEV1 declared 02:40 -> use preceded declaration -> security incident.
# Twin: SEV1 declared 02:08 -> use during SEV1 -> routine review within 24 h.
C("it13", "What follow-up does the use of break-glass account BG-ADMIN-2 require?",
"""
Orvane Bank Services — Emergency Access (Break-Glass) Standard

1. Definitions: an incident's SEV1 period runs from the time SEV1 is declared in the incident tool until the incident is closed. Use "during a SEV1" means use within that period.
2. Break-glass accounts may be used only during a SEV1.
3. Every permitted use is reviewed by the security team within 24 hours (routine review).
4. Any use that is not during a SEV1 is itself treated as a security incident.
5. Passwords for break-glass accounts are reset after every use.

Access log — BG-ADMIN-2
| Time | Event |
| 02:10 | login, database cluster DB-7 |
| 02:34 | logout |

Incident tool — INC-4410
| Time | Event |
| 02:05 | paged: DB-7 replication lag |
| 02:40 | SEV1 declared by on-call lead |
| 03:55 | closed |
""",
[("routine_review", "The account was used within the SEV1 period, so a routine review within 24 hours is all that is needed."),
 ("raise_security_incident", "The account was used before SEV1 was declared, so the use falls outside a SEV1 period."),
 ("no_follow_up", "The incident was closed and the password will be reset, so nothing further is required.")],
"raise_security_incident", 2,
twin=T([("| 02:40 | SEV1 declared by on-call lead |", "| 02:08 | SEV1 declared by on-call lead |")], "routine_review")),

# ------------------------------------------------------------------ it14
# why: device_id is Confidential per data dictionary (the other columns are Internal).
# Confidential data needs a current DPA. Brindle DPA expired 30 June; send date 14 July
# -> hold. Nothing Restricted. Twin: DPA valid to 30 September -> send as is.
C("it14", "Can the analytics extract be sent to Brindle Analytics as specified?",
"""
Talmead Retail — Data Sharing Rules

1. Restricted data may never leave the company.
2. Confidential data may be shared with a third party only while a signed Data Processing Agreement (DPA) with that party is current.
3. Internal data may be shared for business purposes without a DPA.
4. A dataset takes the highest classification of any column in it.

Data dictionary (extract)
| Column | Classification | Note |
| order_id | Internal | |
| basket_value | Internal | |
| postcode_district | Internal | first half of postcode only |
| device_id | Confidential | treated as personal data |
| card_number | Restricted | |

Third-party register
| Party | DPA signed | DPA valid until |
| Brindle Analytics | 2 July 2024 | 30 June 2026 |

Extract request DX-19, Tuesday 14 July 2026
Columns: order_id, basket_value, postcode_district, device_id
Recipient: Brindle Analytics (basket analysis project)
""",
[("send_as_is", "Brindle's DPA is current on the send date, which covers the Confidential device_id column."),
 ("hold_until_dpa_renewed", "The device_id column makes the extract Confidential, and Brindle's DPA is no longer current."),
 ("never_send_restricted", "Device identifiers are treated as personal data, which makes the extract Restricted, and Restricted data may never leave the company.")],
"hold_until_dpa_renewed", 2,
twin=T([("| Brindle Analytics | 2 July 2024 | 30 June 2026 |", "| Brindle Analytics | 2 July 2024 | 30 September 2026 |")], "send_as_is")),

# ------------------------------------------------------------------ it15
# why: payroll-queries mailbox is flagged HR-sensitive -> owner + HR director. Only the
# owner approved -> await HR director. Twin: mailbox facilities-queries (not flagged)
# -> owner approval suffices -> grant.
C("it15", "What is the next step for mailbox access request MB-332?",
"""
Lowmarsh Council IT — Shared Mailbox Access

1. Access to a shared mailbox needs approval from the mailbox owner shown in the register.
2. Mailboxes flagged HR-sensitive also need approval from the HR Director.
3. Access requested by someone who is not the user (for example a manager on the user's behalf) is allowed if the approvals in 1 and 2 are present.

Shared mailbox register
| Mailbox | Owner | HR-sensitive |
| payroll-queries@ | K. Mensah | yes |
| facilities-queries@ | D. Orr | no |
| planning-enquiries@ | A. Fenwick | no |

MB-332
Requested by: T. Ruddock (manager) on behalf of new starter P. Lindqvist
Mailbox: payroll-queries@
Approvals: mailbox owner — approved 10:12.
""",
[("grant_access", "The mailbox owner has approved and managers may request for a new starter, so access can be granted."),
 ("await_hr_director", "The mailbox is flagged HR-sensitive, so the HR Director's approval is still needed."),
 ("reject_wrong_requester", "Requests must come from the person who will use the mailbox.")],
"await_hr_director", 1),

# ------------------------------------------------------------------ it16
# why: CVSS 7.8 = High (30 days), but amendment: internet-facing assets move up one level
# -> Critical -> 7 days. Found 1 Sep; today 10 Sep = 9 days -> overdue -> escalate.
# Twin: asset internal-only -> High, 30 days -> within SLA.
C("it16", "What status should the vulnerability tracker show for VULN-2207 on 10 September?",
"""
Hesketh Insurance — Vulnerability Remediation Standard

1. Severity from CVSS base score: Critical 9.0-10.0; High 7.0-8.9; Medium 4.0-6.9; Low below 4.0.
2. Remediation deadlines from the date found: Critical 7 days; High 30 days; Medium 90 days; Low 180 days.
3. (Amendment, January) Vulnerabilities on internet-facing assets are handled one severity level higher than their CVSS score gives.
4. A missed deadline is escalated to the CISO. A risk exception needs the CISO's signature before the deadline.

Asset inventory (extract)
| Asset | Exposure |
| portal-web-02 | internet-facing |
| hr-db-01 | internal only |

VULN-2207
Asset: portal-web-02
CVSS: 7.8
Found: 1 September
Status: patch scheduled for 25 September
Comment from the application owner: "Please record a risk exception — the patch window is later this month."
""",
[("within_sla", "A 7.8 score is High, so the team has 30 days from 1 September and the patch is scheduled in time."),
 ("escalate_overdue", "Internet exposure lifts the finding to Critical, so the 7-day deadline has already passed."),
 ("record_risk_exception", "The owner has asked for an exception, and the patch date is later in the month.")],
"escalate_overdue", 2,
twin=T([("Asset: portal-web-02", "Asset: hr-db-01")], "within_sla")),

# ------------------------------------------------------------------ it17
# why: need 2 of 3 factors: callback to HR-system number (caller-supplied number does
# not count), manager confirmation in ticket, employee ID + DOB. Caller gave ID + DOB
# (1); manager away, no confirmation; callback number is new, not HR's -> 1 factor ->
# decline. Twin: manager's confirmation recorded in the ticket -> 2 factors -> reset.
C("it17", "Should the service desk reset the password on ticket SD-90412?",
"""
Orvane Bank Services — Service Desk Identity Verification

Before resetting a password, verify the caller with at least two of these three factors:
F1. A callback to the phone number held in the HR system. A number supplied by the caller does not count.
F2. Written confirmation from the caller's line manager, recorded in the ticket.
F3. Correct employee ID and date of birth.
If fewer than two factors are met, decline the reset and advise the caller to visit a service point with photo ID.

Ticket SD-90412, 08:47
Caller says she is Ruth Asante, Payments Operations.
- Gave employee ID 40217 and date of birth; both match HR records.
- "I've got a new phone, please call me back on 07700 900 318." HR system holds 07700 900 552.
- Line manager Oskar Brenn is on annual leave; no confirmation in the ticket.
- Caller: "It's urgent, I'm locked out before the payment run."
""",
[("reset_password", "At least two of the three verification factors are met, so the reset can go ahead."),
 ("decline_reset", "Only the employee ID and date of birth factor is met; the callback number is not the one held by HR and no manager confirmation is recorded."),
 ("reset_after_callback_to_new_number", "Calling back the new number the caller gave supplies the second factor.")],
"decline_reset", 2,
twin=T([("- Line manager Oskar Brenn is on annual leave; no confirmation in the ticket.",
         "- Line manager Oskar Brenn confirmed by email at 08:52 that the caller is Ruth Asante; recorded in the ticket.")], "reset_password")),

# ------------------------------------------------------------------ it18
# why: security logs (definition includes authentication logs and firewall logs) are kept
# 2 years. vpn-auth = authentication logs -> purge of 400-day-old data not allowed.
# Twin: cdn-access (general application log, 1 year) -> 400 days > 1 year -> purge ok.
C("it18", "How should the platform team respond to storage request ST-58?",
"""
Talmead Retail — Log Retention Standard

1. Definitions: "security logs" are authentication logs, firewall logs and endpoint protection logs. All other logs are "general logs".
2. General logs: 90 days in hot storage, then archive, deleted after 1 year.
3. Security logs: 90 days in hot storage, then archive, deleted after 2 years.
4. No log may be deleted before its retention period ends, even to save cost.

Log sources (extract)
| Source | Content |
| vpn-auth | VPN authentication successes and failures |
| cdn-access | CDN request logs for the public site |
| fw-edge | edge firewall allow/deny |

ST-58
Requester: storage operations
"Archive costs are over budget. Please approve deleting all vpn-auth archive data older than 400 days."
""",
[("approve_deletion", "Data older than 400 days is past the 1-year archive period for these logs, so it can be deleted to cut storage costs."),
 ("deny_deletion", "These are authentication logs, which count as security logs with a 2-year retention period."),
 ("move_to_hot_storage", "Logs being considered for deletion must first return to hot storage for review.")],
"deny_deletion", 1),
]
