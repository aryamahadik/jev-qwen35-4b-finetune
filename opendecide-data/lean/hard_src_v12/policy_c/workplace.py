"""policy_c / workplace HR, IT and compliance policies (Norrow Freight, Pellion Analytics, Quenby Foods,
Aldercrest District Council)."""
from _lib import C, Y, T

ITEMS = [
# ------------------------------------------------------------------ wk01
# why: not cash; £60 would be "accept and record", but the giver is a bidder in a live tender -> decline all.
# Twin: tender long closed -> £25.01-£100 band -> accept and record.
C("wk01", "What should Priya do with the hamper under the Gifts and Hospitality Policy?",
"""
Norrow Freight — Gifts and Hospitality Policy (GH-2)
1. Cash and cash equivalents (gift cards, vouchers, prepaid cards) of any value must be declined and reported to Compliance.
2. While a tender or contract negotiation with the giver is live, all gifts and hospitality from that giver must be declined, whatever their value.
3. Otherwise: gifts worth £25 or less may be accepted without a record; gifts worth £25.01–£100 may be accepted but must be recorded in the gifts register within 5 days; gifts worth over £100 must be declined.

Email to Priya Natarajan (Procurement Manager), 21 September 2026
From: Compliance helpdesk
"Hi Priya — you asked about the hamper that arrived at reception from Harlan Pallets & Racking. The supplier's delivery note values it at £60 (cheese, chutney, a box of biscuits; no alcohol, no vouchers inside). For context, Harlan is one of three bidders in the live warehouse-racking tender, which closes on 30 September. Your name is on the evaluation panel. Let us know what you decide so we can close the query."
""",
[("accept — no record needed", "a gift of £25 or less with no live tender and no cash element."),
 ("accept and record in the register", "a gift of £25.01–£100 with no live tender and no cash element."),
 ("decline", "a gift over £100, or any gift from a giver in a live tender or negotiation."),
 ("decline and report to Compliance", "cash or a cash equivalent of any value."),
 ("surrender for the charity raffle", "a gift over £100 that would cause offence to refuse, handed to the company.")],
"decline", 2,
twin=T([("For context, Harlan is one of three bidders in the live warehouse-racking tender, which closes on 30 September. Your name is on the evaluation panel.",
         "For context, Harlan is our incumbent racking supplier; the last tender closed in June 2025 and the next one is not due until 2028.")],
       "accept and record in the register")),

# ------------------------------------------------------------------ wk02
# why: day 1 includes a £6 glass of wine -> alcohol never reimbursed -> claim cannot be paid in full (0).
# (Breakfast £8.50 under £10 needs no receipt.) Twin: dinner £24 no alcohol: 8.50 + 24 = 32.50 <= 35;
# day 2 12.40 with receipt -> paid in full (1).
Y("wk02", "Can Tom's meal claim be paid in full?",
"""
Pellion Analytics — Travel & Expenses Policy, section 4 (Meals)
4.1 On overnight business trips, meals are reimbursed up to £35 per day in total (breakfast, lunch and dinner combined).
4.2 Alcohol is never reimbursed.
4.3 Any single item over £10 needs an itemised receipt; items of £10 or less may be claimed without one.
4.4 Anything that breaks 4.1–4.3 is removed from the claim, and the claim is paid in part.

Expense claim EXP-40913 — Tom Adeyemi, client workshop in Harrowfield, 14–15 September 2026 (overnight stay)
Day 1 (14 Sept): breakfast at the station £8.50 (no receipt); dinner £29.00 including a £6.00 glass of wine (itemised receipt).
Day 2 (15 Sept): lunch £12.40 (itemised receipt).
Manager approval: given.
Tom's note: "Kept it cheap — didn't claim any snacks."
""",
[("Paid in full", "every item meets 4.1–4.3."),
 ("Paid in part", "at least one item or amount must be removed under 4.4.")],
0, 2,
twin=T([("dinner £29.00 including a £6.00 glass of wine (itemised receipt)", "dinner £24.00, no alcohol (itemised receipt)")], 1)),

# ------------------------------------------------------------------ wk03
# why: verbal Jan 2025 expired (6 months); first written 3 Feb 2026 live until 3 Feb 2027 -> next step is
# final written. Twin: first written 3 Aug 2025 -> expired 3 Aug 2026 -> nothing live -> verbal warning.
C("wk03", "Which disciplinary step should the hearing manager apply to Liam?",
"""
Norrow Freight — Disciplinary Procedure (misconduct, not gross misconduct)
Steps: verbal warning (live for 6 months) → first written warning (live for 12 months) → final written warning (live for 12 months) → dismissal.
The next step is the one above the highest warning that is still live on the date of the new misconduct. If no warning is live, start at a verbal warning. Expired warnings are ignored.

HR case note — Liam Cartwright, warehouse operative, Harwick depot
• Verbal warning: issued 10 January 2025 (mobile phone use on the pick floor).
• First written warning: issued 3 February 2026 (timekeeping).
• New misconduct: 15 September 2026 — late for 4 shifts in 2 weeks with no notice to the shift lead. The investigation found no mitigating reasons. The hearing manager has confirmed this is misconduct, not gross misconduct.
""",
[("no action", "the allegation is not upheld."),
 ("verbal warning", "no live warning on file."),
 ("first written warning", "a live verbal warning is the highest live warning."),
 ("final written warning", "a live first written warning is the highest live warning."),
 ("dismissal", "a live final written warning is on file.")],
"final written warning", 2, ordered=True,
twin=T([("First written warning: issued 3 February 2026", "First written warning: issued 3 August 2025")], "verbal warning")),

# ------------------------------------------------------------------ wk04
# why: complaint about his own bonus is a personal grievance, no listed wrongdoing -> not protected (0).
# Twin: managers telling drivers to switch off tachographs (legal breach + safety danger) -> protected (1).
Y("wk04", "Is Declan's email a protected disclosure under the Whistleblowing Policy?",
"""
Norrow Freight — Whistleblowing Policy, section 2
A protected disclosure is information that the worker reasonably believes shows one or more of: a criminal offence; a failure to comply with a legal obligation; a danger to health or safety; damage to the environment; a miscarriage of justice; or the deliberate concealment of any of these — AND that the worker reasonably believes is made in the public interest.
Complaints about the worker's own pay, contract terms or treatment are personal grievances and go through the Grievance Procedure; they are not protected disclosures unless they also meet the test above.

Email to the Speak Up inbox, 11 September 2026
From: Declan Morrow, HGV driver, Tilbury hub
"I want to report that my Q2 performance bonus was worked out wrong. I did 212 deliveries, not 198, and the difference is about £140. I've raised it with my manager twice and got nowhere. I'm raising it here because I think this is unfair and I'd like it looked into properly."
""",
[("Protected disclosure", "information about a listed type of wrongdoing, reasonably believed to be in the public interest."),
 ("Personal grievance", "a complaint about the worker's own pay, contract or treatment.")],
0, 2,
twin=T([("I want to report that my Q2 performance bonus was worked out wrong. I did 212 deliveries, not 198, and the difference is about £140.",
         "I want to report that the Tilbury transport managers are telling drivers to switch off their tachographs on the Scotland run so we can drive past the legal hours limit.")], 1)),

# ------------------------------------------------------------------ wk05
# why: pasting client data into a public AI chatbot = unapproved third-party tool -> D2 only.
# Twin: forwards the spreadsheet to his personal email -> D1.
C("wk05", "Which Data Handling Standard did Aaron breach?",
"""
Pellion Analytics — Data Handling Standard
D1 Sending company or client data to personal email, personal cloud storage or personal devices.
D2 Processing client data in any third-party tool not on the Approved Tools list, including public AI chatbots.
D3 Sharing passwords, access tokens or MFA codes with anyone.
D4 Leaving a device unlocked and unattended, or client papers on a desk overnight.
If more than one applies, record the lowest-numbered standard.
Approved Tools list (extract): Pellion Workspace, Pellion Copilot (internal, enterprise-licensed), Tableau Server.

Security alert SA-7719 — Aaron Whitfield, Senior Analyst
Data loss prevention logs show that at 16:42 on 17 September, from his managed work laptop, Aaron copied 1,900 rows of Fenmore Retail's store-level sales data (client data) and pasted them into the public web version of "Quibble", a free AI chatbot, with the prompt "summarise these sales trends for a slide". No files left the laptop by email, upload to cloud storage or USB. His screen was locked when he stepped away at 17:10.
""",
[("D1 personal accounts or devices", "company or client data sent to personal email, personal cloud or personal devices."),
 ("D2 unapproved tools", "client data processed in a third-party tool not on the Approved Tools list."),
 ("D3 credential sharing", "passwords, tokens or MFA codes shared."),
 ("D4 unattended devices or papers", "an unlocked unattended device, or client papers left out overnight."),
 ("none of these", "no Data Handling Standard was breached.")],
"D2 unapproved tools", 2,
twin=T([("copied 1,900 rows of Fenmore Retail's store-level sales data (client data) and pasted them into the public web version of \"Quibble\", a free AI chatbot, with the prompt \"summarise these sales trends for a slide\". No files left the laptop by email, upload to cloud storage or USB.",
         "emailed a spreadsheet of 1,900 rows of Fenmore Retail's store-level sales data (client data) to his personal email account with the subject \"work on at home\". No other tools or uploads were used.")],
       "D1 personal accounts or devices")),

# ------------------------------------------------------------------ wk06
# why: previous 2019-2023 service is broken (left Nov 2023), so count from 2 Mar 2026 to 22 Aug 2026 =
# 173 days = 24.7 weeks < 26 -> not eligible (0). Twin: start 2 Feb 2026 -> 201 days = 28.7 weeks -> 1.
Y("wk06", "Does Grace qualify for Norrow's enhanced maternity pay?",
"""
Norrow Freight — Family Leave Policy, Enhanced Maternity Pay
To qualify for enhanced maternity pay (full pay for 16 weeks), an employee must have at least 26 weeks' continuous employment with Norrow by the end of the qualifying week, which is the 15th week before the expected week of childbirth. Continuous employment is broken if the employee leaves Norrow and later rejoins; earlier periods of employment before a break do not count.

HR query — Grace Oyelowo, Customer Service Adviser
Expected week of childbirth: begins Sunday 6 December 2026.
Qualifying week (as calculated by payroll): ends Saturday 22 August 2026.
Current employment start date: 2 March 2026.
Previous employment: Grace worked for Norrow from April 2019 to November 2023, then left to join another company, and rejoined in 2026.
Grace's question: "I've been with Norrow for years in total — do I get the enhanced pay?"
""",
[("Eligible", "26 or more weeks' continuous employment by the end of the qualifying week."),
 ("Not eligible", "fewer than 26 weeks' continuous employment by the end of the qualifying week.")],
0, 3,
twin=T([("Current employment start date: 2 March 2026.", "Current employment start date: 2 February 2026.")], 1)),

# ------------------------------------------------------------------ wk07
# why: household holdings add up: 3% + 4% = 7% > 5% of a supplier -> financial interest.
# Twin: wife holds 1% -> 4% -> not a financial interest; no other conflict -> none of these.
C("wk07", "Which conflict of interest category, if any, applies to Oliver?",
"""
Quenby Foods — Conflicts of Interest Policy
C1 Financial interest: the employee and their household members together hold more than 5% of the shares of a supplier, customer or competitor. Holdings are added together. The employee must declare it and step back from any decision involving that company.
C2 Close personal relationship: a partner or family member in the employee's reporting line, or a partner or family member employed by a supplier the employee manages.
C3 Outside employment: a second job or directorship with a supplier, customer or competitor.
C4 Gifts and hospitality: handled under the separate Gifts Policy.

Declaration form — Oliver Brandt, Senior Buyer (Packaging)
Current task: member of the three-person panel choosing the 2027 packaging supplier.
Shareholdings: Oliver holds 3% of Brackley Packaging Ltd (a bidder). His wife, Hanne, holds 4% of Brackley Packaging Ltd. No other household member holds shares.
Relationships: Hanne is a primary-school teacher; no family member works for any bidder.
Other roles: none.
""",
[("C1 financial interest", "combined household shareholding of more than 5% in a supplier, customer or competitor."),
 ("C2 close personal relationship", "a partner or relative in the reporting line or at a supplier the employee manages."),
 ("C3 outside employment", "a second job or directorship with a supplier, customer or competitor."),
 ("C4 gifts and hospitality", "an issue handled under the Gifts Policy."),
 ("none of these", "no conflict of interest arises.")],
"C1 financial interest", 2,
twin=T([("His wife, Hanne, holds 4% of Brackley Packaging Ltd.", "His wife, Hanne, holds 1% of Brackley Packaging Ltd.")], "none of these")),

# ------------------------------------------------------------------ wk08
# why: shift ends 23:00, next starts 09:00 -> 10 hours < 11 -> breach (1). Twin: next starts 10:30 -> 11.5 h -> 0.
Y("wk08", "Does the rota breach Aldercrest's daily rest rule?",
"""
Aldercrest District Council — Working Time Standards
Daily rest: every worker must have at least 11 consecutive hours of rest between the end of one shift and the start of the next.
Breaks: a worker whose shift is longer than 6 hours must get an uninterrupted break of at least 20 minutes.
Weekly rest: at least 24 hours of uninterrupted rest in each 7-day period.
Rota managers may not publish a rota that breaks these standards unless the worker is covered by a signed emergency-cover agreement.

Draft rota — Civil Enforcement Officers, week 40 — officer Karim Haddad
Tuesday: 15:00–23:00 (30-minute break at 19:00)
Wednesday: 09:00–17:00 (30-minute break at 13:00)
Thursday and Friday: rest days
Emergency-cover agreement: none signed.
Note from the rota manager: "Wednesday is short-staffed; Karim's the only one with the new handheld training."
""",
[("Daily rest breach", "fewer than 11 consecutive hours of rest between two shifts."),
 ("Compliant rota", "the rota meets the daily rest standard.")],
1, 1,
twin=T([("Wednesday: 09:00–17:00 (30-minute break at 13:00)", "Wednesday: 10:30–18:30 (30-minute break at 14:00)")], 0)),

# ------------------------------------------------------------------ wk09
# why: Portugal approved; days abroad this year = 14 (Spain) + 12 = 26 -> 21-60 band -> HR tax review.
# Twin: 6 earlier days -> 18 <= 20 -> manager approval only.
C("wk09", "How should Yusuf's request to work from Portugal be handled?",
"""
Pellion Analytics — Working Abroad Policy
• Employees may work from an approved country for up to 20 working days in total per calendar year with their manager's approval.
• If a request would take the employee's total working days abroad in the calendar year to between 21 and 60, it must go to an HR tax review before travel.
• Totals above 60 working days per calendar year are not permitted.
• Working from a country not on the approved list is not permitted.
Approved countries: Ireland, France, Spain, Portugal, Netherlands, Belgium.
Days spent abroad on leave (holiday) do not count; only working days count.

Request WA-2291 — Yusuf Karim, Data Engineer
Request: work from Lisbon, Portugal, 2–17 November 2026 — 12 working days.
Working days abroad already this calendar year: 14 working days from Valencia, Spain, in May.
Holiday abroad this year: 10 days in Morocco (annual leave, no work).
Manager: supportive, has approved in principle.
""",
[("approve — manager approval only", "approved country and a yearly total of 20 working days or fewer."),
 ("refer to HR tax review", "approved country and a yearly total of 21–60 working days."),
 ("decline — over the yearly limit", "a yearly total above 60 working days."),
 ("decline — country not approved", "the country is not on the approved list."),
 ("approve — no approval needed", "a single trip of 5 working days or fewer.")],
"refer to HR tax review", 2,
twin=T([("14 working days from Valencia, Spain, in May", "6 working days from Valencia, Spain, in May")],
       "approve — manager approval only")),

# ------------------------------------------------------------------ wk10
# why: the range is unannounced (press release scheduled 1 Oct; post 25 Sep) -> confidential -> breach ->
# the negated question is false (0). Twin: press release already out on 15 Sep -> public -> no breach (1).
Y("wk10", "Is it not the case that Freya's post breaches the Social Media Policy?",
"""
Quenby Foods — Employee Social Media Policy, section 3 (Confidential information)
Employees must not post confidential information on personal accounts. Confidential information includes products, prices or store listings that Quenby has not yet announced publicly, financial results before publication, and the names of customers or suppliers that have not been made public. Once Quenby has announced something through an official press release or its own social channels, employees may share or repost it.

Report from the Communications team, 25 September 2026
Freya Lindgren (Product Developer) posted on her personal LinkedIn at 08:30 today:
"So proud of the team — our new Quenby oat-milk range launches in 300 Tallis Supermarket stores next month! Two years of work. 🌾"
Communications calendar: the oat-milk range and the Tallis listing are scheduled to be announced by press release on 1 October 2026; nothing has been published about them yet.
""",
[("Breach of section 3", "a personal post revealing information Quenby has not yet announced publicly."),
 ("Permitted post", "a personal post sharing only information Quenby has already announced.")],
0, 2, role="neg",
twin=T([("the oat-milk range and the Tallis listing are scheduled to be announced by press release on 1 October 2026; nothing has been published about them yet.",
         "the oat-milk range and the Tallis listing were announced by press release on 15 September 2026 and posted on Quenby's own LinkedIn page the same day.")], 1)),

# ------------------------------------------------------------------ wk11
# why: refusal of a random test is treated as a positive -> suspend from safety-critical duties and investigate.
# Twin: took the test; positive only for codeine he declared in advance as prescribed -> OH review.
C("wk11", "What action does the Drug and Alcohol Policy require for Stefan?",
"""
Norrow Freight — Drug and Alcohol Policy, section 5 (Testing)
5.1 Employees in safety-critical roles (drivers, forklift operators, yard shunters) may be selected for random testing.
5.2 A refusal to take a test, or failing to complete it without good medical reason, is treated as a positive result.
5.3 A positive result: the employee is removed from safety-critical duties at once and a disciplinary investigation starts.
5.4 Where a positive result is explained by a prescribed medicine that the employee declared to Occupational Health (OH) before the test, no disciplinary action starts; OH reviews fitness for duty and the employee stays off safety-critical duties until OH clears them.
5.5 A negative result: no action.

Incident note — Harwick depot, 23 September 2026, 06:15
Stefan Ilić (forklift operator) was selected by the random-testing system. When the tester arrived, Stefan said: "I'm not doing it, I've done nothing wrong and this is a waste of time," and went back to the pick floor. He was reminded of the policy and again declined. No medical reason was given.
OH records: no medicines declared.
""",
[("no action", "a negative result."),
 ("occupational health review", "a positive result explained by a medicine declared to OH before the test."),
 ("remove from safety-critical duties and investigate", "a positive result, or a refusal treated as positive."),
 ("retest within 24 hours", "the sample could not be analysed.")],
"remove from safety-critical duties and investigate", 2,
twin=T([("When the tester arrived, Stefan said: \"I'm not doing it, I've done nothing wrong and this is a waste of time,\" and went back to the pick floor. He was reminded of the policy and again declined. No medical reason was given.\nOH records: no medicines declared.",
         "Stefan completed the test; the result was positive for codeine only.\nOH records: on 2 September Stefan declared prescribed co-codamol for a back injury.")],
       "occupational health review")),

# ------------------------------------------------------------------ wk12
# why: encrypted laptop, password not compromised -> listed as unlikely to result in risk -> no regulator
# notification (0). Twin: encryption not enabled, payroll data -> notify (1).
Y("wk12", "Must the DPO notify the regulator about incident DB-0317?",
"""
Pellion Analytics — Personal Data Breach Procedure
1. Staff must report any suspected personal data breach to the Data Protection Officer (DPO) within 24 hours.
2. The DPO must notify the regulator within 72 hours of becoming aware of a breach, unless the breach is unlikely to result in a risk to people's rights and freedoms.
3. The following are treated as unlikely to result in a risk: loss of a device protected by full-disk encryption where the password or recovery key has not been compromised; an email sent to the wrong internal colleague who confirms deletion.

Incident DB-0317, reported 19 September 2026, 09:05
Reporter: Maya Collins (Payroll Officer)
"I left my work laptop on the 18:12 train from Harrowfield last night. It had a copy of the September payroll file for 340 staff (names, bank details, salaries). The train company hasn't found it."
IT asset check: full-disk encryption: enabled and verified; password: not written down or shared; remote wipe command sent 09:20 (device not yet online).
""",
[("Regulator notification", "required unless the breach is unlikely to result in a risk to people."),
 ("Internal record only", "the breach is unlikely to result in a risk and is logged internally.")],
0, 2,
twin=T([("full-disk encryption: enabled and verified;", "full-disk encryption: not enabled (laptop set up before the 2024 rollout);")], 1)),

# ------------------------------------------------------------------ wk13
# why: detriment (lost overtime) plainly because she filed a grievance -> victimisation.
# Twin: team-wide cut announced before the grievance for a business reason -> none of these.
C("wk13", "Which Dignity at Work category fits Mei's complaint?",
"""
Quenby Foods — Dignity at Work Policy, definitions
Sexual harassment: unwanted conduct of a sexual nature.
Harassment: unwanted conduct related to a protected characteristic (age, disability, race, religion, sex, sexual orientation, gender reassignment) that violates dignity or creates a hostile environment.
Bullying: offensive, intimidating, malicious or insulting behaviour, or misuse of power, that undermines or humiliates someone.
Victimisation: treating someone worse because they made, or supported, a complaint or grievance.

Complaint received 14 September 2026 — Mei Tanaka, line operative, Bakery Line 3
"On 2 September I filed a grievance about unpaid breaks. On 9 September my supervisor, Gavin, took me off the Saturday overtime rota. When I asked why, he messaged me: 'people who go running to HR don't get the good shifts.' Everyone else on my line still has their Saturday overtime."
Rota records: Mei removed from the overtime rota on 9 September; the other 11 operatives on Line 3 unchanged.
""",
[("sexual harassment", "unwanted conduct of a sexual nature."),
 ("harassment", "unwanted conduct related to a protected characteristic."),
 ("bullying", "offensive, intimidating or insulting behaviour, or misuse of power."),
 ("victimisation", "worse treatment because the person made or supported a complaint."),
 ("none of these", "the conduct complained of does not fit any category.")],
"victimisation", 2,
twin=T([("When I asked why, he messaged me: 'people who go running to HR don't get the good shifts.' Everyone else on my line still has their Saturday overtime.\"\nRota records: Mei removed from the overtime rota on 9 September; the other 11 operatives on Line 3 unchanged.",
         "When I asked why, he messaged me: 'overtime is cut for everyone from 9 Sep because we lost the Harbury contract, sorry.'\"\nRota records: Saturday overtime for all 12 operatives on Line 3 ended on 9 September, as announced to the whole line on 20 August.")],
       "none of these")),

# ------------------------------------------------------------------ wk14
# why: address flagged RED -> paired visits only -> Ruth may not go alone (0), even with check-ins arranged.
# Twin: AMBER flag with 60-minute check-in call arranged -> lone visit allowed (1).
Y("wk14", "May Ruth carry out the home visit alone?",
"""
Aldercrest District Council — Lone Working Procedure (housing and environmental health staff)
Before any home visit, check the address on the Risk Register.
• RED flag: visits must be made in pairs. No lone visits, whatever other arrangements are in place.
• AMBER flag: a lone visit is allowed only if a named colleague is set up to take check-in calls at least every 60 minutes and to escalate if a call is missed.
• No flag: normal lone visit with the lone-worker app switched on.

Visit request — Ruth Mbeki, Environmental Health Officer
Address: 7 Tanner's Yard, Aldercrest — damp and mould complaint from the tenant
Date: Thursday 1 October 2026, 14:00
Risk Register flag: RED (2025 incident — verbal threats to a housing officer)
Arrangements: colleague Sam Pryce will take check-in calls every 45 minutes; lone-worker app on.
Second officer available: none until the following week.
Ruth's note: "Tenant sounded fine on the phone and it's urgent — there's a baby in the flat."
""",
[("Lone visit allowed", "the flag level permits a lone visit and its conditions are met."),
 ("Paired visit required", "the address is RED-flagged, or the AMBER conditions are not met.")],
0, 2,
twin=T([("Risk Register flag: RED (2025 incident — verbal threats to a housing officer)", "Risk Register flag: AMBER (2025 note — large dog kept at the property)")], 1)),

# ------------------------------------------------------------------ wk15
# why: two grounds-maintenance orders within 12 months are related and must be added: 14,000 + 14,000 =
# 28,000 -> £25,000-£189,329 band -> formal tender. Twin: second order is unrelated IT cabling -> only
# the one £14,000 grounds order counts -> three written quotes.
C("wk15", "Which procurement route applies to the grounds-maintenance purchase?",
"""
Aldercrest District Council — Contract Procedure Rules
Estimated value (excluding VAT) decides the route:
• under £5,000 — one written quote;
• £5,000 to £24,999 — three written quotes;
• £25,000 to £189,329 — formal tender on the council's e-tendering portal;
• £189,330 or more — full public procurement procedure.
Splitting is prohibited: related purchases of the same kind of goods or services from the same budget within any 12-month period must be added together to decide the route.

Purchase request PR-26-0871 — Parks and Open Spaces
Request: grounds maintenance (grass cutting and hedge trimming), Riverside Park, October 2026 – March 2027. Estimated value: £14,000.
Related orders from the Parks budget in the last 12 months: grounds maintenance (grass cutting and hedge trimming), Millfield Rec, April – September 2026, £14,000.
Officer's note: "Two separate parks, two separate jobs, so three quotes each should be fine."
""",
[("one written quote", "aggregated value under £5,000."),
 ("three written quotes", "aggregated value £5,000 to £24,999."),
 ("formal tender on the portal", "aggregated value £25,000 to £189,329."),
 ("full public procurement procedure", "aggregated value £189,330 or more.")],
"formal tender on the portal", 2, ordered=True,
twin=T([("grounds maintenance (grass cutting and hedge trimming), Millfield Rec, April – September 2026, £14,000.",
         "network cabling for the Parks depot office (IT services), May 2026, £14,000.")],
       "three written quotes")),

# ------------------------------------------------------------------ wk16
# why: an aunt is not on the close-family list -> 1 day for the funeral, not 5 days (0).
# Twin: grandmother is close family -> 5 days (1).
Y("wk16", "Is Aisha entitled to five days' paid compassionate leave?",
"""
Norrow Freight — Compassionate Leave Policy
• Death of close family — spouse or partner, child, parent, sibling, grandparent, grandchild, or parent-in-law: up to 5 days' paid leave.
• Death of any other relative or a friend: 1 day's paid leave to attend the funeral.
• Further time may be taken as annual leave or unpaid leave with the manager's agreement.

Leave request — Aisha Rahman, Transport Planner, 24 September 2026
"Hi Joanne — sadly my aunt, my mum's sister, passed away on Tuesday. She helped raise me when I was little and we were very close. The funeral is on Monday in Bradford and I'd like to take the whole week off to be with the family and help sort things out. Can I have the five days' paid compassionate leave?"
Manager's note: happy to support; checking entitlement with HR.
""",
[("Five days' paid leave", "the person who died is close family as listed in the policy."),
 ("One day's paid leave", "the person who died is another relative or a friend.")],
0, 1,
twin=T([("sadly my aunt, my mum's sister, passed away on Tuesday. She helped raise me", "sadly my grandmother, my mum's mother, passed away on Tuesday. She helped raise me")], 1)),
# ------------------------------------------------------------------ wk17
# why: false vehicle registrations entered to get personal fuel = dishonest gain -> fraud or theft, which
# takes precedence over misuse of company property. Twin: borrowing the van without permission, own fuel,
# no dishonest gain -> misuse of company property.
C("wk17", "Which Code of Conduct category should the investigation record for Gary?",
"""
Quenby Foods — Code of Conduct investigation, case CoC-26-114
Precedence: where the employee gained money, goods or services dishonestly, record "fraud or theft" rather than "misuse of company property".

Subject: Gary Pollard, delivery driver, Harrowfield depot
Allegation raised by the fleet team, 18 September 2026:
"Gary's company fuel card was used six times on Saturdays and Sundays between June and August, £380 in total, at a garage near his home. He is not rostered at weekends. On each receipt the vehicle registration was typed in as his company van, but the van was locked in the depot yard all weekend each time (yard CCTV and van telematics). Gary's own car is a diesel hatchback; the pump records show diesel each time."
Gary's statement: "I was short of money and I meant to pay it back."
No other allegations are open.
""",
[("misuse of company property", "using company vehicles, equipment or systems for unauthorised purposes without dishonest gain."),
 ("fraud or theft", "dishonestly gaining money, goods or services from the company or others."),
 ("conflict of interest", "a personal interest that could influence business decisions."),
 ("health and safety breach", "conduct that puts the employee or others at risk."),
 ("data protection breach", "mishandling personal data."),
 ("bullying or harassment", "offensive, intimidating or unwanted conduct towards others."),
 ("gifts and hospitality breach", "accepting or giving gifts outside the Gifts Policy."),
 ("unauthorised absence", "missing work without permission or a valid reason."),
 ("confidentiality breach", "disclosing confidential company information."),
 ("anti-competitive conduct", "agreeing prices or sharing markets with competitors."),
 ("none of these", "no Code of Conduct breach is established.")],
"fraud or theft", 2,
twin=T([("\"Gary's company fuel card was used six times on Saturdays and Sundays between June and August, £380 in total, at a garage near his home. He is not rostered at weekends. On each receipt the vehicle registration was typed in as his company van, but the van was locked in the depot yard all weekend each time (yard CCTV and van telematics). Gary's own car is a diesel hatchback; the pump records show diesel each time.\"\nGary's statement: \"I was short of money and I meant to pay it back.\"",
         "\"On Sunday 6 September Gary took his company van out of the depot without permission and used it to help a friend move house (van telematics and yard CCTV). He is not rostered at weekends. He filled the tank with his own money before returning it, and no company fuel card or other expense was used.\"\nGary's statement: \"I know I should have asked. I paid for the fuel myself.\"")],
       "misuse of company property")),
]
