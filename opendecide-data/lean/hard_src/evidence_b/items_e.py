"""Domain E: data retention and data-handling rules (invented statutes)."""
from _h import it

NONE = "none of these"

ITEMS = [

it("E1", "noul",
   "May Lindenfeld keep Farid's CV on file as of September 1?",
   """Email - Recruitment coordinator to Data Protection Officer, Lindenfeld Engineering
Subject: Farid Haddad's application

We turned down Farid Haddad for the Graduate Engineer role on January 15. It's now September 1. On our online application form he ticked the box "Please keep my CV on file and contact me about future vacancies for up to 2 years." He hasn't contacted us since. Our retention schedule says "Unsuccessful applicants - 6 months", so the system has flagged his file for deletion. Can we keep it?

Lindenfeld applies the Aldmoor Data Protection Code, Rule 14:
(1) Personal data of unsuccessful job applicants must be deleted within 6 months after the recruitment decision.
(2) Paragraph (1) does not apply where the applicant has given written consent to retention for consideration for future vacancies; such data may be kept for the period consented to, up to a maximum of 2 years after the decision.
(3) Electronic consent, including ticking a box on an online form, is written consent.""",
   1,
   card="- applicant-data retention: delete within 6 months after the recruitment decision, unless the applicant gave written (including electronic) consent to retention for future vacancies, for up to 2 years after the decision",
   diff=1),

it("E2", "choice",
   "What is the earliest date on which Tallow & Birch may destroy the invoice?",
   """Records management query - Tallow & Birch Ltd.
Our fiscal year runs from July 1 to June 30. I'm clearing old accounts-receivable records and found a sales invoice issued on August 15, 2019. No legal hold or audit is pending. When is the earliest date we may destroy it? Someone on the team says "seven years from the invoice date".

Kerrick Commercial Records Act, Schedule 2:
Item 1. Invoices: retain for 7 years from the end of the fiscal year in which the invoice was issued.
Item 2. Payroll records: retain for 4 years from the date of payment.
Item 3. Contracts: retain for 6 years after the contract expires.
Note A. A record may be destroyed on or after the first day following the end of its retention period.
Note B. If a legal hold applies, retain the record until the hold is released.""",
   "July 1, 2027",
   opts=["July 1, 2026", "August 16, 2026", "January 1, 2027", "July 1, 2027", "August 16, 2027"],
   tpl="the invoice may first be destroyed on {}",
   diff=3, twin=[("issued on August 15, 2019", "issued on May 20, 2019")], twin_gold="July 1, 2026"),

it("E3", "noul",
   "May the shop still lawfully hold the clip of the fall?",
   """Forum: Small Retailers' Network - Privacy & Security
Posted by corner_grocer_mo

Our CCTV system keeps footage for 45 days, then overwrites it. Forty days ago a customer slipped on a wet floor near the freezers. We reported the incident to our insurer three days later, and the claim is still open. A privacy consultant visiting today says we're breaking the law by holding any footage older than 30 days. Does that include the clip of the fall?

Reply quoting the Norrow Surveillance Data Regulation, reg. 6:
(1) Recordings from a surveillance camera system must not be retained for longer than 30 days.
(2) Paragraph (1) does not apply to a recording of an incident that was reported to the police or to an insurer within 30 days after the recording was made; such a recording may be retained until the matter is finally closed.""",
   1,
   card="- incident-recording exception: a recording of an incident reported to the police or an insurer within 30 days after recording may be kept until the matter is finally closed",
   diff=1),

it("E4", "choice",
   "What notifications does Part 6 require the clinic to make?",
   """Incident report - Wexley Physiotherapy Clinic, Data Protection Lead
On 11 March a clinic laptop was stolen from a physiotherapist's car. The laptop's disk was encrypted, but the recovery key was written on a sticky note kept in the laptop bag, which was also taken. The laptop held treatment notes (health data) for 320 patients, all residents of the Province of Wexley. The practice manager's view: "encrypted, and under 500 people, so nothing to report".

Wexley Personal Data Protection Act, Part 6:
§61 A controller must notify the Commissioner within 72 hours after becoming aware of a breach that affects the personal data of 500 or more residents, or that affects any sensitive data. "Sensitive data" includes health data, biometric data, and financial account numbers together with access codes.
§62 Whenever notice to the Commissioner is required because sensitive data was affected, the controller must also notify each affected individual without unreasonable delay.
§63 A breach of data that was encrypted is not a breach for the purposes of this Part, unless the encryption key was also compromised.""",
   "notify both the Commissioner and the affected individuals",
   opts=["no notification required", "notify the Commissioner only", "notify the affected individuals only", "notify both the Commissioner and the affected individuals"],
   card="- no notification required: the incident needs no notice to anyone\n- notify the Commissioner only: notice to the regulator but not to the patients\n- notify the affected individuals only: notice to the patients but not to the regulator\n- notify both the Commissioner and the affected individuals: notice to the regulator and to each affected patient",
   diff=2),

it("E5", "noul",
   "Was Sami's own consent a sufficient basis for QuestPals's processing?",
   """Complaint file - Office of the Privacy Commissioner, Territory of Brenn
Service: "QuestPals", a mobile game.
Complainant: the parent of Sami, age 14. Sami created an account by entering his birth date and ticking "I agree". No parent was asked. QuestPals uses players' in-game activity and approximate location to serve targeted advertisements between levels. QuestPals says that teenagers can consent for themselves.

Brenn Children's Online Privacy Act §4:
(1) An operator may process the personal data of a child under 13 only with the verified consent of a parent.
(2) A child aged 13 to 15 may consent to the processing of the child's own personal data, except that verified parental consent is required if the data will be used for targeted advertising.""",
   0,
   card="- child consent rule: under 13 needs verified parental consent; ages 13 to 15 may consent for themselves except where the data will be used for targeted advertising, which needs verified parental consent",
   diff=1),

it("E6", "choice",
   "Until when must the clinic keep L. Mbatha's chart?",
   """Records query - Westerly Family Clinic
Patient: L. Mbatha, born March 2010. Last visit to the clinic: June 2022. No later contact; the patient is alive and has not asked for the records. The records clerk wants to know how long the chart must be kept before it can be destroyed; she assumes "10 years after the last visit, like everyone".

Westerly Health Records Regulation §9:
(1) A clinic must keep an adult patient's record for 10 years after the patient's last visit.
(2) If the patient was under 18 at the last visit, the record must be kept until the later of (a) the patient's 28th birthday or (b) 10 years after the last visit.
(3) If the patient has died, the record must be kept for 5 years after death, or for the period in (1) or (2) if shorter.""",
   "March 2038",
   opts=["June 2027", "March 2028", "June 2032", "March 2038", "June 2038"],
   tpl="the chart must be kept until {}",
   diff=2),

it("E7", "noul",
   "Must Hollis erase Petra's order history now?",
   """Email - Customer Care, Hollis Home Supplies
From: Petra Kovacs
"Under the Data Protection Act, erase all my personal data - order history, account, everything - now."

Internal note from Legal: Ms. Kovacs is in a dispute with us over a $2,300 refund for a defective range cooker. Last week her solicitor sent us a letter threatening court proceedings if we do not pay within 14 days. Her order history and our correspondence with her are the core evidence.

Lorne Data Protection Act §17:
(1) A controller must erase personal data without undue delay when the data subject requests erasure.
(2) Paragraph (1) does not apply to the extent that retention is necessary (a) for compliance with a legal obligation, or (b) for the establishment, exercise, or defence of legal claims that are pending or reasonably anticipated.""",
   0,
   card="- erasure exception: data need not be erased to the extent retention is necessary for a legal obligation or for legal claims that are pending or reasonably anticipated",
   diff=1),

it("E8", "choice",
   "What is Arden's final deadline to respond to the request?",
   """Privacy team log - Arden Mobile, subject access request #SAR-3012
- April 3: request received by email from a person claiming to be customer Tomas Veer.
- April 10: identity verification completed (the customer supplied the requested ID).
- May 8: Arden emailed Mr. Veer that it needs more time because the request covers eight years of call records, and stated those reasons.
- The team asks: what is our final deadline?

Arden applies the Calder Data Protection Act §22:
(1) A controller must respond to an access request within 30 days after receiving it.
(2) If the controller reasonably requires identity verification, the 30-day period begins when verification is completed.
(3) The controller may extend the period once, by a further 30 days, if it notifies the data subject of the extension and the reasons for it within the original period.""",
   "June 9",
   opts=["May 3", "May 10", "June 2", "June 9", "July 9"],
   tpl="Arden's final deadline is {}",
   diff=3, twin=[("- May 8: Arden emailed", "- May 12: Arden emailed")], twin_gold="May 10"),

it("E9", "noul",
   "May the company lawfully keep these 100-day-old logs?",
   """Forum: HR Professionals - Data & Monitoring
Posted by hr_lead_sabine

We use keystroke logging on company laptops (disclosed in our policy). Our logs for one employee are now 100 days old. We kept them because on day 85 after they were recorded we opened a formal disciplinary proceeding against him over suspected data theft, and that proceeding is ongoing. IT says we're over the 90-day limit and must purge. Must we?

Reply quoting the Vessel Bay Workplace Monitoring Act §8:
(1) Data collected by keystroke logging may be retained for no more than 90 days after collection.
(2) Paragraph (1) does not apply to data relevant to a disciplinary proceeding against the employee that was commenced within that 90-day period; such data may be retained until the proceeding and any appeal are concluded.""",
   1,
   card="- keystroke-log retention: at most 90 days after collection, except data relevant to a disciplinary proceeding begun within those 90 days, which may be kept until the proceeding and any appeal end",
   diff=2, twin=[("on day 85 after they were recorded", "on day 95 after they were recorded")], twin_gold=0),

it("E10", "choice",
   "What should the audit finding say?",
   """Audit finding draft - Norvale Insurance, Data Protection Audit
Background: in January the company erased the records of 212 former customers who had requested erasure. The erased records remained in encrypted backup sets, which the company had put beyond use pending normal rotation; the oldest backup set is 120 days old. On March 1, after a server failure, IT restored a backup set, which brought the 212 erased records back into the live system. IT re-deleted them on March 9.

Norvale applies the Hesketh Data Code §31:
(1) Erased data held in backups must be put beyond use and must be deleted when the backup is rotated, and in any case no later than 180 days after erasure.
(2) If erased data is restored to a live system from a backup, the controller must re-delete it within 7 days after the restoration.""",
   "breach: late re-deletion after the restore",
   opts=["compliant", "breach: backups kept too long", "breach: late re-deletion after the restore", "breach: backup data not put beyond use"],
   card="- compliant: no breach of §31\n- breach: backups kept too long: erased data stayed in backups beyond the 180-day limit\n- breach: late re-deletion after the restore: restored erased data was not re-deleted within 7 days\n- breach: backup data not put beyond use: erased data in backups was left usable",
   diff=2),

it("E11", "noul",
   "Can Ridgeline run the photo time clock without written releases?",
   """Email - Owner of Ridgeline Fitness to the gym's IT contractor
Our new staff time clock takes a photo of each employee when they punch in. The photos are stored for 6 months so we can settle disputes about who clocked in. The system doesn't analyse the photos in any way - no face matching, no templates; it's just a timestamped picture. The vendor's brochure calls it a "biometric-ready" clock, which worried me. Do we need to get written releases from staff?

Parkhurst Biometric Privacy Act:
§2 "Biometric identifier" means a retina or iris scan, fingerprint, voiceprint, or scan of hand or face geometry. It does not include a photograph, unless the photograph is used to extract or analyse hand or face geometry.
§3 A private entity may not collect or store a biometric identifier of any person unless it first obtains that person's written release.""",
   1,
   card="- biometric identifier: a retina or iris scan, fingerprint, voiceprint, or scan of hand or face geometry; a photograph counts only if it is used to extract or analyse hand or face geometry",
   diff=1),

it("E12", "choice",
   "Which dataset may Wayfarer lawfully continue to hold today?",
   """Data inventory review - Wayfarer Maps Ltd.
Dataset A: raw GPS traces of active users, collected 14 months ago.
Dataset B: raw GPS traces of users who closed their accounts 20 days ago.
Dataset C: a "heatmap" table built 15 months ago from raw trips, aggregating trips by city block; some blocks contain data from only 3 users.
Dataset D: precise location histories keyed by hashed device IDs, collected 13 months ago.

Colbrook Location Privacy Act:
§4 Precise geolocation data may be retained for no more than 12 months after collection.
§5 When a user closes an account, the controller must delete that user's precise geolocation data within 30 days after closure.
§6 Data that has been de-identified is exempt from §4 and §5. Aggregated data is de-identified only if each reported unit reflects data from at least 10 users. Data keyed by a hashed or otherwise pseudonymous identifier is not de-identified.""",
   "Dataset B",
   opts=["Dataset A", "Dataset B", "Dataset C", "Dataset D", NONE],
   card="- Dataset A: the 14-month-old raw traces of active users\n- Dataset B: the raw traces of users who closed their accounts\n- Dataset C: the city-block heatmap table\n- Dataset D: the location histories keyed by hashed device IDs\n- none of these: no listed dataset may lawfully be held today",
   diff=3),

it("E13", "noul",
   "Was the March 4 auto-deletion permissible under Rule 37A?",
   """Litigation readiness memo - Farrowby Instruments
- Monday, March 2: Farrowby receives a demand letter from a former distributor threatening suit over unpaid commissions. Litigation is reasonably anticipated from this date.
- Wednesday, March 4: the email system's routine 3-year auto-deletion job deletes old messages, including several exchanged with the distributor.
- Friday, March 6: Legal issues a written litigation hold suspending auto-deletion for all distributor-related records.

Pennock Civil Procedure Rule 37A:
(1) Once litigation is reasonably anticipated (the "trigger date"), a party must preserve relevant records. Deletion of relevant records after the trigger date is a violation of this Rule.
(2) Despite (1), deletion by a routine, automated retention schedule is not a violation if it occurs within 5 business days after the trigger date and the party issues a litigation hold within those 5 business days.""",
   1,
   card="- safe-harbour deletion: routine automated deletion within 5 business days after the trigger date is not a violation if a litigation hold is also issued within those 5 business days",
   diff=2),

it("E14", "choice",
   "Until what date must Dorian keep the records supporting the 2020 return?",
   """Accountant's email - to client Dorian Wexford (sole trader)
You asked when you can shred the records supporting your 2020 tax return. That return was due April 15, 2021, but you filed it late, on September 10, 2021. During the recent review we found the return omitted about 30% of your 2020 gross income (the unreported consulting fees). This was an honest error, not fraud.

Selby Tax Administration Act §58:
(1) A taxpayer must keep records supporting a return for 5 years after the later of the return's due date or the date it was filed.
(2) If the return omitted more than 25% of the gross income required to be reported, the period in (1) is 8 years.
(3) There is no time limit if the return was fraudulent.""",
   "September 10, 2029",
   opts=["April 15, 2026", "September 10, 2026", "April 15, 2029", "September 10, 2029", "no time limit"],
   tpl="the records must be kept until {}",
   extra={"no time limit": "the records must be kept indefinitely"},
   diff=2),

it("E15", "noul",
   "Can Tern & Thistle email the promotion to that segment without consent?",
   """Email - Marketing assistant to Compliance, Tern & Thistle Outdoor Gear
We want to email a spring promotion for hiking boots to customers who haven't opted in to marketing. One segment is people who bought hiking boots from us 20 months ago; at checkout they were shown an unticked "no marketing emails, please" box and none of them ticked it. Can we include them?

Halvard Electronic Marketing Regulation, reg. 22:
(1) A business may not send unsolicited marketing email to an individual without the individual's prior consent.
(2) Paragraph (1) does not apply where (a) the business obtained the individual's email address in the course of a sale to that individual within the preceding 18 months, (b) the marketing concerns the business's own similar products, and (c) the individual was given a simple means of refusing marketing when the address was collected and did not refuse.""",
   0,
   card="- existing-customer exception: the address was obtained in a sale to that person within the preceding 18 months, the marketing is for the business's own similar products, and the person was offered a simple opt-out at collection and did not use it",
   diff=2, twin=[("bought hiking boots from us 20 months ago", "bought hiking boots from us 16 months ago")], twin_gold=1),

it("E16", "choice",
   "Which item on the checklist is retained unlawfully?",
   """Privacy audit checklist - Hotel Lindenhof
P1: Guest register entries (name, address, dates) for a guest who checked out 10 months ago.
P2: A photocopy of the passport of a guest resident abroad who checked out 11 months ago.
P3: A photocopy of the national driving licence of a guest resident in Merrin who checked out 2 days ago.
P4: The last four digits of a guest's payment card, kept on the folio for 6 months.

Merrin Accommodation Records Regulation:
1. Accommodation providers must keep a guest register and retain each entry for 1 year after check-out.
2. Copies of identity documents may not be retained, except that for guests who are not residents of Merrin, a copy of the passport or travel document may be retained for up to 1 year after check-out.
3. This Regulation does not govern payment card data.""",
   "P3",
   opts=["P1", "P2", "P3", "P4", NONE],
   card="- P1: the guest register entries\n- P2: the passport photocopy of the guest resident abroad\n- P3: the driving-licence photocopy of the guest resident in Merrin\n- P4: the last four card digits on the folio\n- none of these: every checklist item is retained lawfully",
   diff=1),

it("E17", "noul",
   "May HelixRoot keep Idris's saliva sample?",
   """Customer complaint - HelixRoot DNA Services
Idris Mahmoud sent a saliva sample for an ancestry test. On the consent form he ticked "Yes - use my de-identified results for research" and left unticked "Yes - store my sample for possible future testing". His results were delivered 60 days ago. He has learned that HelixRoot still holds his saliva sample; HelixRoot says his research consent covers it.

Tavish Genetic Privacy Act §6:
(1) A direct-to-consumer genetic testing company must destroy a consumer's biological sample within 30 days after the test is completed, unless the consumer has given separate express consent to storage of the sample.
(2) Consent to the use of test results for research is not consent to storage of the biological sample.""",
   0,
   card="- sample storage rule: a biological sample must be destroyed within 30 days after the test is completed unless the consumer gave separate express consent to storing it; research consent is not storage consent",
   diff=1),

it("E18", "choice",
   "Under the schedule, which category governs the incident report's retention?",
   """Records retention decision - Orland Chemicals Ltd., Records Office
Record: an incident report dated April 2021 describing an employee, Selma Arvidsson, suffering a chemical splash to the forearm from a leaking container of a hazardous solvent. The report is filed in her personnel file. Ms. Arvidsson left the company in March 2023. The clerk proposes to treat it as part of the personnel file.

Orland Retention Schedule, general rules:
G1. Each record is assigned every category whose description it fits.
G2. A record that fits more than one category is governed by whichever of those categories gives the longest retention (the latest destruction date).
G3. Periods run from the date of the record unless the category says otherwise.
(The category list, with periods, is in the card.)""",
   "R-11",
   opts=["R-01", "R-02", "R-03", "R-04", "R-05", "R-06", "R-07", "R-08", "R-09", "R-10", "R-11", NONE],
   card="""- R-01: general correspondence; keep 2 years
- R-02: contracts; keep 6 years after expiry
- R-03: personnel files; keep 6 years after the employee leaves
- R-04: payroll records; keep 4 years
- R-05: workplace injury reports; keep 10 years
- R-06: customer complaints; keep 3 years
- R-07: board minutes; keep permanently
- R-08: CCTV recordings; keep 30 days
- R-09: visitor logs; keep 1 year
- R-10: health and safety training records; keep 5 years
- R-11: records of employee exposure to hazardous substances; keep 40 years
- none of these: no listed category governs the record""",
   diff=3, twin=[("suffering a chemical splash to the forearm from a leaking container of a hazardous solvent",
                  "spraining an ankle after slipping on a wet floor in the canteen")], twin_gold="R-05"),

it("E19", "noul",
   "Does the purchase-trends dataset qualify as anonymous data exempt from the retention limit?",
   """Data team chat thread (exported) - Kellow Retail
@maya: For the "purchase trends" dataset we dropped names, emails and addresses. Each row now has a customer ID, purchase category, month and region. Since it's anonymous, can we keep it forever and skip the 3-year retention limit?
@jon: The customer IDs are the same ones in our CRM, which still maps them to names.
@maya: Sure, but the analytics team never looks at the CRM.

Kellow is subject to the Ardwin Data Protection Act:
§2 "Anonymous data" means data from which no individual can be identified by any means reasonably likely to be used, including by combining it with other information held by the controller.
§9 Personal data may be kept for no longer than the retention period in the controller's schedule; this section does not apply to anonymous data.""",
   0,
   card="- anonymous data: data from which no individual can be identified by any means reasonably likely to be used, including by combining it with other information the controller holds",
   diff=1),

it("E20", "choice",
   "What is the credit union's deadline for notifying members?",
   """Incident log - Pemberly Credit Union
- June 1: breach discovered - an attacker accessed members' names and account numbers.
- June 3: the Pemberly police cyber unit, investigating the attacker, asked the credit union by phone to hold off notifying members for 20 days so as not to tip off the suspect. No written request followed.
- The credit union asks: what is our deadline for notifying affected members?

Kinross Breach Notification Act §5:
(1) Affected individuals must be notified without unreasonable delay and in any case within 45 days after discovery of the breach.
(2) If a law-enforcement agency requests in writing that notification be delayed because it would impede a criminal investigation, the deadline in (1) is extended by the period requested, up to 30 days.""",
   "July 16",
   opts=["July 16", "July 23", "July 31", "August 5", "August 15"],
   tpl="members must be notified by {}",
   diff=2, twin=[("asked the credit union by phone to hold off notifying members for 20 days so as not to tip off the suspect. No written request followed.",
                  "sent the credit union a written request to hold off notifying members for 20 days so as not to tip off the suspect.")],
   twin_gold="August 5"),

it("E21", "noul",
   "Did Brisk Ventures comply with §11?",
   """HR compliance email - Brisk Ventures (Aldane subsidiary)
Our parent company in another country asked for our employee records (names, roles, salaries, performance ratings) to build a group-wide "talent analytics" dashboard. We sent employees a written notice describing the transfer, its purpose and the recipient on October 1, and made the first transfer on October 22. Payroll is run locally and isn't involved. Did we comply?

Aldane Employee Data Act §11:
(1) An employer may transfer employee personal data to an affiliated company if the transfer is necessary for payroll or benefits administration.
(2) For any other purpose, the employer must give employees written notice of the transfer, its purpose, and the recipient at least 30 days before the first transfer.""",
   0,
   card="- affiliate transfer rule: allowed for payroll or benefits administration; for any other purpose, written notice of the transfer, purpose and recipient is needed at least 30 days before the first transfer",
   diff=1),

it("E22", "choice",
   "Which retention period governs this recording?",
   """Records query - Tolland Securities, compliance desk
A client called our trading desk on 2 February. No trade was placed on the call, but the client complained about a delayed withdrawal. The complaint was resolved on 3 April. When does the call recording become eligible for deletion? The desk's default setting deletes non-trade calls after 6 months.

Marlow Financial Records Rule 12:
(1) Recordings of telephone calls that result in a transaction must be kept for 5 years after the call.
(2) Recordings of other calls must be kept for 6 months after the call.
(3) A recording of a call in which a complaint is made must be kept for 3 years after the complaint is resolved, if that period ends later than the period in (1) or (2).""",
   "3 years after the complaint was resolved",
   opts=["6 months after the call", "3 years after the call", "5 years after the call", "5 years after the complaint was resolved", "3 years after the complaint was resolved"],
   card="- 6 months after the call: the recording may be deleted 6 months after the call\n- 3 years after the call: the recording may be deleted 3 years after the call\n- 3 years after the complaint was resolved: the recording may be deleted 3 years after the complaint's resolution\n- 5 years after the call: the recording may be deleted 5 years after the call\n- 5 years after the complaint was resolved: the recording may be deleted 5 years after the complaint's resolution",
   diff=2),

it("E23", "noul",
   "May Coldwater charge Rhiannon the $10 fee?",
   """Email - Data Protection Officer, Coldwater Telecom
A customer, Rhiannon Price, made a subject access request, which we answered free of charge. Now, 11 months after that request, she has sent a second request for the same kind of information (call logs and billing data). Her second request is polite and specific. Can we charge the $10 fee?

Belmont Privacy Act §19:
(1) A controller may not charge a fee for responding to a data subject's first access request in any 12-month period.
(2) A controller may charge a reasonable fee of no more than $10 for any further access request made by the same data subject within 12 months after an earlier request, or for a request that is manifestly unfounded.""",
   1,
   card="- access-request fee rule: the first request in any 12-month period is free; a further request by the same person within 12 months after an earlier one, or a manifestly unfounded request, may carry a fee of up to $10",
   diff=1, twin=[("Now, 11 months after that request", "Now, 13 months after that request")], twin_gold=0),

it("E24", "choice",
   "By what date must Pennant delete Gwen's data?",
   """Loyalty programme data review - Pennant Pharmacies
Member: Gwen Hollis. Last purchase: March 10, 2024. On September 10, 2024, she logged in to the app to check her points balance; she has not purchased or redeemed anything since March 10, 2024. The app's dashboard lists her "last activity" as September 10, 2024.

Pennant is subject to the Arwen Loyalty Data Regulation:
§3 A loyalty account becomes inactive on the second anniversary of the member's last transaction.
§4 "Transaction" means a purchase, or a redemption of points. Logging in, viewing a balance, or opening a marketing email is not a transaction.
§5 The operator must close an inactive account and delete the member's personal data within 90 days after the account becomes inactive.""",
   "June 8, 2026",
   opts=["June 8, 2026", "June 10, 2026", "September 8, 2026", "December 9, 2026", "March 10, 2027"],
   tpl="Gwen's data must be deleted by {}",
   diff=3),

it("E25", "noul",
   "Is Rowan Mutual's continued retention of the data lawful?",
   """Case note - Insurance Ombudsman, File IO-5530
Insurer: Rowan Mutual. Policyholder: Callum Firth (a pay-how-you-drive policy that recorded speed, braking, and location).
The policy ended January 31, 2025. On December 20, 2024 Mr. Firth was in a collision and filed a claim, which remains open. It is now March 2026. Rowan Mutual still holds only one set of his driving data: the last 30 days of driving before the collision. All other data has been deleted. Mr. Firth argues that everything had to go 12 months after the policy ended.

Kestrel Telematics Data Code §4:
(1) An insurer may retain telematics data for the policy period and 12 months after the policy ends.
(2) If the policyholder files a claim, the insurer may retain the telematics data from the 30 days preceding the incident giving rise to the claim until the claim is closed.""",
   1,
   card="- claim-data exception: after a claim is filed, telematics data from the 30 days before the incident may be kept until the claim is closed, even beyond the normal 12 months after the policy ends",
   diff=2),

it("E26", "choice",
   "Which in-scope data may Marigold lawfully still hold today?",
   """Privacy request log - Marigold Beauty (online retailer)
Customer Hattie Blum withdrew her consent to marketing 60 days ago. Marigold stopped sending her marketing within 3 business days. Marigold still holds: (a) her email address on a do-not-contact suppression list, and (b) her marketing profile (browsing history, product preferences, predicted spend). The compliance team asks what it may lawfully still hold today. Her order records are held separately under tax law and are out of scope.

Wenlock Consumer Data Act §14:
(1) When a consumer withdraws consent to marketing, the business must stop marketing processing within 10 business days.
(2) The business may keep the consumer's email address on a suppression list indefinitely, solely to ensure the consumer is not contacted again.
(3) The business must delete all other marketing profile data within 30 days after the withdrawal.""",
   "the suppression-list email only",
   opts=["both the suppression-list email and the marketing profile", "the marketing profile only", "nothing at all", "the suppression-list email only"],
   card="- nothing at all: Marigold must hold neither item\n- the suppression-list email only: Marigold may keep the email on the suppression list but not the profile\n- the marketing profile only: Marigold may keep the profile but not the suppression-list email\n- both the suppression-list email and the marketing profile: Marigold may keep both items",
   diff=2),
]
