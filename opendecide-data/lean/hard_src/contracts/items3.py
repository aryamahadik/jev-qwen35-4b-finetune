"""Contracts hard items, batch 3: content removal, data sharing, auto-renewal (with near misses)."""
from common import C, Y, S, T

ITEMS = [
# 61 hide/limit visibility of posts
C("cr_guidelines",
"""Vellora Community Guidelines - Enforcement (section 5)

"5.1 Vellora may, at its sole discretion, remove, hide, or limit the visibility of any post, comment, or media that it believes violates these Guidelines or is otherwise objectionable, without notice to you. Hidden content remains visible to you but not to other users.
5.2 Repeated violations may lead to restrictions on your account under the Terms of Service."

Moderator training quiz, question 7: "A creator asks why her comment on a political thread now shows as 'Visible only to you'. Her account is otherwise unrestricted. Classify the provision that allowed this.\"""",
["CR", "TWC", "TFC", "LIC", "UC", "DS", "LOL", "NONE"], "CR", 2, t="the provision that allowed this"),

# 62 license grant with "modify" wording
C("lic_grant",
"""Vellora Terms of Service, section 9 ("Your Content")

"9.1 You retain ownership of the photos, videos, text and audio you post ("User Content").
9.2 By posting User Content, you grant Vellora a worldwide, non-exclusive, royalty-free, sublicensable license to use, reproduce, modify, adapt, publish, translate and display that User Content in connection with operating and promoting the Services. This license ends when you delete the User Content, except for copies already shared by other users."

Photographer's question in a creators' chat server: "Does 9.2 let Vellora take my photos down whenever it wants, or is it something else?\"""",
["CR", "LIC", "DS", "UC", "TWC", "AR", "WD", "NONE"], "LIC", 2, t="section 9.2"),

# 63 monitoring right without removal (twin: may delete)
Y("cr_monitor_only",
"""Maplecrest Residents Portal - Community Board Rules

"Residents may post notices about lost items, events, and items for sale on the Community Board. Maplecrest has the right, but not the obligation, to monitor posts on the Community Board. We do not pre-screen posts and are not responsible for content posted by residents. Residents are responsible for making sure their posts comply with the House Rules and applicable law."

Resident's complaint to the building office: "My neighbour posted a photo of my car's licence plate with an angry note about parking. Can management actually do anything about it under these rules?\"""",
"CR", 0, 3, t="the Community Board Rules paragraph",
twin=T([("We do not pre-screen posts and are not responsible for content posted by residents.",
         "We do not pre-screen posts, but we may delete any post that we consider inappropriate.")], 1)),

# 64 listing takedown with non-refunded fees
C("cr_listing_takedown",
"""Ember & Oak Marketplace - Seller Handbook, chapter 6

"6.4 Listings that do not comply with the Prohibited Items Policy may be taken down by Ember & Oak at any time, and any listing fees paid for those listings will not be refunded. We will notify you by email with the reason.
6.5 If more than three of your listings are taken down in any 90-day period, we may close your shop."

Seller's appeal: "You took down my vintage ivory-handled letter opener and kept my $4.20 listing fee. Which rule are you relying on?"
Support agent's reply cites 6.4 only.""",
["CR", "TFC", "TWC", "WD", "UC", "DS", "LIC", "NONE"], "CR", 3, t="the rule the support agent cites"),

# 65 repeat infringer account termination (twin: disable the material instead)
C("tfc_repeat_infringer",
"""Plover Upload Studio - Copyright Policy

"We respond to notices of alleged copyright infringement that comply with applicable law. If you repeatedly upload material that infringes others' copyrights, we will disable your account. We may also tell the rights holder what action we have taken."

Creator's message to support: "Three of my remixes were claimed this month. What happens if I get one more?"

Support team lead: "Before we answer, tag the second sentence of the policy in the knowledge base so the macro links to the right definition.\"""",
["CR", "TFC", "TWC", "LIC", "UC", "DS", "WD", "NONE"], "TFC", 3, t="the second sentence of the policy",
twin=T([("we will disable your account.", "we will disable public access to that material.")], "CR")),

# 66 section locator: editorial unpublishing among license, security, honoraria, feedback
S("cr_sections_editorial",
"""Tessellate Health Community - Contributor Terms

7.1 License. You grant Tessellate a non-exclusive license to publish your Submissions on the Community site and in our newsletters.
7.2 Editorial Review. We may decline to publish, or later unpublish, any Submission that we determine does not meet our Editorial Standards, including submissions that give individual medical advice.
7.3 Account Security. You are responsible for keeping your password confidential.
7.4 Honoraria. Featured contributors receive a $150 honorarium per published article, paid within 30 days of publication.
7.5 Feedback. Suggestions you send us about the Community may be used without any obligation to you.""",
["Section 7.1", "Section 7.2", "Section 7.3", "Section 7.4", "Section 7.5"], "CR", "Section 7.2", 2),

# 67 wiki edit reversion quoted in a support email
Y("cr_wiki_revert",
"""From: Farah (Glasswing Wiki Support)
To: Olu Bamidele
Subject: Your edit to "Harrowgate Rowing Club"

Hi Olu,

Thanks for your message about the Harrowgate Rowing Club page. I understand you spent a long time on the history section. Our Community Terms say, in section 4:

"Glasswing and its appointed page stewards may revert any edit to a shared page, or restore an earlier version of that page, if the edit does not meet the Editing Standards. Reverted edits remain visible in the page history to stewards only."

A steward reverted your edit because it did not cite sources. You're welcome to re-add the section with citations, and I've linked the Editing Standards below.

Best,
Farah""",
"CR", 1, 3, t="the quoted section 4 of the Community Terms"),

# 68 reviews withheld or withdrawn
C("cr_reviews_withheld",
"""Brightloft Stays - Guest Review Policy

"Reviews must reflect a genuine stay. Reviews that we determine were written in exchange for payment, discounts or free nights will not be published, and reviews already published may be withdrawn from the property's page. Hosts may reply publicly to any published review once. Guests may edit their own review within 14 days of posting it."

Host's question in the host help centre: "A guest's glowing five-star review disappeared from my page last week. Which part of the policy was that, and what kind of provision is it?\"""",
["CR", "LIC", "TFC", "DS", "UC", "TWC", "WD", "NONE"], "CR", 3, t="the provision behind the missing review"),

# 69 users deleting their own posts (twin: moderators may delete any post)
Y("cr_user_delete",
"""Sundial Learning Forums - Posting Rules

11. Be kind. Criticise ideas, not people.
12. Deleting posts. You may delete any of your own posts at any time from your profile page. Deleted posts are removed from public view within 24 hours but may be kept in backups for up to 30 days.
13. Homework help. Do not post answers to live assessments or quizzes that are still open.
14. Signatures. Keep signatures to two lines and do not include links to paid services.

Moderator onboarding quiz: "Classify rule 12 against the clause definitions on the card.\"""",
"CR", 0, 3, t="rule 12",
twin=T([("You may delete any of your own posts at any time from your profile page.", "Sundial moderators may delete any post at any time from any profile page.")], 1)),

# 70 prohibitions without a removal right (twin: adds takedown right)
C("cr_prohibited_only",
"""Maplecrest Tenant App - Marketplace Rules

"You must not post listings or messages that are defamatory, obscene, discriminatory, or that infringe anyone's intellectual property. You are solely responsible for the listings and messages you post, and for complying with all laws that apply to the items you offer. Maplecrest does not take part in any sale between residents."

Property manager's question: "I want to tag this paragraph in our policy library before we launch the app at the Riverside building. Which tag?\"""",
["CR", "TFC", "LIC", "UC", "DS", "TWC", "AR", "NONE"], "NONE", 2, t="the Marketplace Rules paragraph",
twin=T([("You are solely responsible for the listings and messages you post,",
         "Maplecrest may take down any listing or message that breaks this rule, without notice. You are solely responsible for the listings and messages you post,")], "CR")),

# 71 section locator: workshop withholding/delisting
S("cr_workshop_sections",
"""Saltmarsh Games - Tidebreaker Workshop Terms

4.1 Balance Updates. We may change how any custom map interacts with game mechanics when we release balance patches.
4.2 Cheating. We may suspend any account found using unauthorised software to gain an advantage.
4.3 Workshop Review. We may withhold any custom map from the public Workshop until it has passed review, and may permanently delist maps that receive repeated valid reports.
4.4 Map License. You grant us a perpetual license to host, display and distribute the custom maps you upload.
4.5 Refunds. Workshop purchases are refundable within 14 days if the map has been played for less than 2 hours.""",
["Section 4.1", "Section 4.2", "Section 4.3", "Section 4.4", "Section 4.5"], "CR", "Section 4.3", 3),

# 72 large option set: refusing to display profile photos
C("cr_big",
"""Lanternmatch (dating app operated by Redfern Social Ltd) - Profile Standards

"P3. Photos. Your main profile photo must clearly show your face. We may refuse to display, or stop displaying, any photo that does not meet this standard or that includes another person without their consent. Your profile will stay live, but the photo will be replaced by a placeholder until you upload one that complies."

Trust and safety analyst's classification sheet: one category per standard, using the shared clause taxonomy. P1 and P2 are already done; P3 is next.""",
["CR", "LIC", "TWC", "TFC", "UC", "DS", "DR", "AR", "LOL", "WD", "IND", "COL", "ARB", "FS", "CONF", "ASG", "NOT", "SEV", "EA", "NONE"],
"CR", 3, t="standard P3"),

# 73 disclosure of identifiable purchase data (twin: aggregate statistics)
C("ds_partners",
"""Cobalt Crate Coffee - Privacy Notice, section 5 ("Sharing")

"5.1 We may disclose your name, email address and purchase history to carefully selected retail partners to help them understand demand for specialty coffee in your area.
5.2 We never disclose your payment card details, which are handled directly by our payment processor and never stored on our systems."

Notice last updated: 12 January 2026. Questions about this notice can be sent to privacy@cobaltcrate.example.

Privacy analyst's task list: "Tag section 5.1 in the data map. Section 5.2 is already tagged, and sections 1-4 were done last quarter.\"""",
["DS", "DR", "CR", "UC", "LIC", "CONF", "AR", "NONE"], "DS", 2, t="section 5.1",
twin=T([("your name, email address and purchase history", "aggregate purchase statistics that cannot be linked to you or to any other individual customer")], "NONE")),

# 74 promise not to sell, storage, access (twin: shares with pension providers)
C("ds_never_sell",
"""Tandem Payroll - Privacy Summary for Employees of Client Companies

"We will never sell or rent your personal information to third parties. Your data is stored on servers located in the European Economic Area and is encrypted in transit and at rest. Access within Tandem is limited to staff who need it to run payroll for your employer, and every access is logged."

HR manager's request to the supplier review team: "Tag this paragraph for our annual supplier privacy review. One tag for the whole paragraph, please.\"""",
["DS", "DR", "AR", "LOL", "UC", "COL", "AUD", "NONE"], "NONE", 3, t="the paragraph",
twin=T([("We will never sell or rent your personal information to third parties.",
         "We send your personal information to the pension providers and payroll tax filing agents your employer selects.")], "DS")),

# 75 business-transfer clause
Y("ds_merger",
"""Tandem Payroll - Privacy Notice, section 9 ("Business Transfers")

"If Tandem is involved in a merger, acquisition, financing, reorganisation, or sale of all or a portion of its assets, your personal information may be transferred to the acquiring or successor entity as part of that transaction. We will notify you by email and by a prominent notice on our website of any change in ownership or uses of your personal information."

Data protection officer's review note: "Our procurement rules only let us approve suppliers whose notices list every route by which employee data can leave the supplier. Checking each section in turn.\"""",
"DS", 1, 3, t="section 9"),

# 76 retention schedule
C("dr_payroll",
"""Tandem Payroll - Records Schedule (Annex C to the Services Agreement)

"C.2 Payroll records, including pay slips, tax withholdings and employee bank details, will be retained for seven (7) years after the end of the calendar year to which they relate, after which they will be securely destroyed. Where a client instructs us to delete records earlier, we will do so unless the law requires us to keep them."

Auditor's note: "Tag C.2 for the client's records-management file. C.1 (scope of the Annex) needs no tag.\"""",
["DS", "DR", "CONF", "LOL", "UC", "TWC", "AUD", "NONE"], "DR", 2, t="section C.2"),

# 77 NDA disclosure-to-advisers wording
C("conf_nda",
"""Mutual Non-Disclosure Agreement - Oxbow Energy Cooperative and Brisa Mobility S.L.

"3. Obligations. The Recipient shall not disclose the Discloser's Confidential Information to any third party except to its employees, advisers and contractors who need to know it for the Purpose and who are bound by obligations of confidentiality at least as protective as those in this Agreement. The Recipient shall use Confidential Information solely for the Purpose."

Legal intern's note on the review sheet: "Clause 3 literally lets them disclose to third parties. Isn't that data sharing?\"""",
["DS", "CONF", "DR", "IND", "LOL", "ASG", "NS", "NONE"], "CONF", 2, t="clause 3"),

# 78 internal use of viewing history (twin: made available to studios and advertisers)
Y("ds_internal_viewing",
"""Plover Streaming - Privacy Notice, section 4 ("Viewing Activity")

"We use your viewing history within Plover to recommend titles, to continue playback across your devices, and to decide which shows to license or produce. Viewing history linked to your profile is not made available to studios or advertisers. We may publish overall rankings, such as the ten most-watched titles in each country."

A researcher at a consumer group is checking each section of streaming privacy notices against a common definition, to count how many services pass identifiable viewing data outside the company.""",
"DS", 0, 3, t="section 4",
twin=T([("Viewing history linked to your profile is not made available to studios or advertisers.",
         "Viewing history linked to your profile is also made available to studios and advertisers.")], 1)),

# 79 section locator: accident data to insurer vs aggregate city reports (twin: rider contacts insurer)
S("ds_sections_insurer",
"""Brisa Mobility - Rider Privacy Notice (sections 3-7)

3. What we collect. We collect your account details, payment information, and the GPS location of scooters during your rides.
4. How we use it. We use ride data to calculate fares, locate scooters, and investigate damage.
5. City Reports. We publish monthly mobility reports for partner cities showing trip counts and popular routes by district. These reports never include individual trip records or rider identities.
6. Accidents. If you report an accident during a ride, we send your name, contact details and the ride's location history to our insurer, Wrenfield Mutual, so that it can process claims.
7. Retention. We keep ride records for 24 months, then delete them.""",
["Section 3", "Section 4", "Section 5", "Section 6", "Section 7"], "DS", "Section 6", 3,
twin=T([("we send your name, contact details and the ride's location history to our insurer, Wrenfield Mutual, so that it can process claims.",
         "we give you the contact details of our insurer, Wrenfield Mutual, so that you can file a claim with it directly; we do not send it your details.")], "NONE")),

# 80 browser add-on sharing visited URLs with a user ID
C("ds_extension_urls",
"""Browser add-on store listing - "Couponeer" by Talvik Digital
Permissions requested: read and change data on websites you visit.

Privacy practices (developer's disclosure):
"Couponeer shares the addresses of product pages you visit, together with your Couponeer user ID, with our affiliate network so that merchants can credit referral commissions. We do not collect passwords or payment details. You can pause sharing at any time from the add-on menu, which also pauses coupon matching."

Reviewer at a consumer magazine: "Tag the first sentence of the disclosure for our comparison table.\"""",
["DS", "DR", "CONF", "LIC", "UC", "CR", "AR", "NONE"], "DS", 2, t="the first sentence of the disclosure"),

# 81 consented sharing of attendance data with employer's wellness administrator
C("ds_employer_wellness",
"""Northgate Clinics - Virtual Care Terms, section 8 (Workplace Wellness Members)

"If you joined Northgate through your employer's wellness program, and you consented to this at sign-up, Northgate shares your appointment dates, attendance and completion of wellness goals with your employer's wellness program administrator. We do not share diagnoses, prescriptions or clinical notes. You can withdraw consent at any time in Settings, after which sharing will stop."

Employee's question to HR: "The union's reviewing the wellness scheme. What category of clause is section 8?\"""",
["DS", "CONF", "DR", "LIC", "UC", "COL", "TWC", "NONE"], "DS", 2, t="section 8"),

# 82 employee access for support only
Y("ds_support_access",
"""Nimbus Loop Workspace - Security Overview (customer-facing), section "Access to Customer Data"

"Nimbus Loop employees may access Customer Data only when necessary to provide support that the Customer has requested or to investigate a security incident. Every access is logged and reviewed weekly by our security team, and Customers can view the access log for their workspace from the Admin Console. Customer Data is never used to train models or for advertising."

Customer's security questionnaire, Q14, asks whether the vendor's documentation lets it pass users' personal data outside the company. The analyst answers Q14 by tagging this section.""",
"DS", 0, 2, t="the \"Access to Customer Data\" section"),

# 83 names and emails to a reseller
C("ds_reseller",
"""From: Hanna Sorensen (Procurement, Plover Studios Ltd)
To: Legal
Subject: Glasswing Documents - reseller clause

We're about to sign an order through Glasswing's local reseller. The Order Form includes this clause:

"Glasswing may provide Customer's administrator and user names, business email addresses and usage volumes to its authorised reseller in Customer's territory for the purposes of billing, renewals and account management."

Can you confirm what kind of clause this is for the supplier file? Nothing else in the Order Form deviates from Glasswing's standard terms, which we reviewed last year.

Thanks,
Hanna""",
["DS", "CONF", "ASG", "DR", "IND", "LOL", "PAY", "NONE"], "DS", 2, t="the provision Hanna quotes"),

# 84 renewal unless notice (twin: customer must elect to renew)
C("ar_orderform",
"""Order Form - Glasswing Security Managed Detection (Order #GS-4410)
Customer: Juniper Row Hotels Group | Sites: 38 hotels

Subscription Term: 12 months from the Start Date (1 July 2026).
Fees: USD 212,000 per year, invoiced annually in advance, net 30.
Renewal: This Order will renew for successive 12-month terms on the same terms unless either party notifies the other of non-renewal at least 30 days before the end of the current term.
Onboarding: 6 weeks; Glasswing assigns a named onboarding lead.
Special Condition: Customer may add sites mid-term at the per-site rate in Schedule 1.""",
["AR", "UC", "TWC", "PAY", "LOL", "COL", "SLA", "NONE"], "AR", 2, t="the Renewal line",
twin=T([("This Order will renew for successive 12-month terms on the same terms unless either party notifies the other of non-renewal at least 30 days before the end of the current term.",
         "This Order may be renewed for successive 12-month terms on the same terms if Customer notifies Glasswing of its election to renew at least 30 days before the end of the current term.")], "NONE")),

# 85 month-to-month continuation after commitment (twin: membership simply ends)
C("ar_gym_monthly",
"""Pinebrook Fitness - Membership Agreement (Flex 6 plan), key terms

Commitment: 6 months from your start date at $49 per month.
After the commitment: your membership continues on a month-to-month basis at the same monthly rate until you cancel in writing at the front desk or through the app.
Freezes: up to 2 months per year at $10 per month.
Guest passes: 2 per month; guests must sign a waiver at reception.

Member's question at the front desk: "What happens in month 7? What's that term called?\"""",
["AR", "UC", "LOL", "TFC", "DS", "COL", "CR", "NONE"], "AR", 3, t="the \"After the commitment\" term",
twin=T([("your membership continues on a month-to-month basis at the same monthly rate until you cancel in writing at the front desk or through the app.",
         "your membership ends automatically; to keep training you would need to sign up for a new plan at the front desk or through the app.")], "NONE")),

# 86 tenant option to extend (twin: extends unless tenant objects)
Y("ar_option_extend",
"""Lease abstract - Ember & Oak Furniture Co. warehouse, 18 Tidewater Road

Term: 10 years from 1 March 2021.
Option to Extend: Tenant shall have the option to extend the Term for one (1) additional period of five (5) years by giving Landlord written notice at least nine (9) months before the expiry of the Term.
Rent during extension: 95% of fair market rent, determined by an independent surveyor if the parties disagree.

Asset manager's question: "Do we need to diarise a non-renewal notice for this lease, or does it just end if we do nothing?\"""",
"AR", 0, 3, t="the Option to Extend clause",
twin=T([("Tenant shall have the option to extend the Term for one (1) additional period of five (5) years by giving Landlord written notice at least nine (9) months before the expiry of the Term.",
         "The Term shall be extended for one (1) additional period of five (5) years unless Tenant gives Landlord written notice to the contrary at least nine (9) months before the expiry of the Term.")], 1)),

# 87 free trial converting to paid plan
C("ar_trial_conversion",
"""Sundial Learning Plus - checkout page (fine print under the "Start free trial" button)

"Your free trial lasts 14 days. Unless you cancel before the trial ends, your trial will convert to a paid monthly plan at $12.99 per month, and the plan will then carry on from month to month until you cancel."

Consumer protection officer's worksheet for a study of subscription sign-up flows: "Classify the fine print. Screenshot 4 of 9, Sundial Learning, captured 3 August on a desktop browser.\"""",
["AR", "UC", "DS", "LOL", "CR", "COL", "WD", "NONE"], "AR", 2, t="the fine print"),

# 88 section locator: continuation clause without "renew" (twin: needs continuation letter)
S("ar_sections_hosting",
"""Hosting Services Agreement - Ardent Cloud Systems and Lumenfold Inc., Article 3 (Term)

3.1 Initial Term. This Agreement starts on the Effective Date and continues for thirty-six (36) months (the "Initial Term").
3.2 Pricing for Later Periods. Ardent will provide a quotation for any period after the Initial Term at least ninety (90) days before the Initial Term ends.
3.3 Continuation. On expiry of the Initial Term, this Agreement will continue for consecutive one-year periods unless either party serves notice not to continue at least ninety (90) days before the end of the then-current period.
3.4 Early Exit. Customer may end this Agreement before the end of the Initial Term on 60 days' notice by paying an early exit fee equal to 50% of the fees for the remainder of the Initial Term.
3.5 Transition. For 60 days after the Agreement ends, Ardent will provide reasonable transition assistance at its then-current rates.""",
["Section 3.1", "Section 3.2", "Section 3.3", "Section 3.4", "Section 3.5"], "AR", "Section 3.3", 3,
twin=T([("this Agreement will continue for consecutive one-year periods unless either party serves notice not to continue at least ninety (90) days before the end of the then-current period.",
         "this Agreement will continue for consecutive one-year periods only if both parties sign a continuation letter before the end of the then-current period.")], "NONE")),

# 89 domain re-registration by default, negated question
Y("ar_domain_neg",
"""Cobalt Crate Domains - Registration Agreement, section 5

"5. Registration Period. Each domain is registered for the period you select at checkout. Thirty (30) days before the registration expires, Cobalt Crate will attempt to charge your saved card for another registration period of the same length. If you have switched the 'Keep my domain' setting off, or if the charge fails three times, we will let the registration lapse instead."

Small-business owner's message to support: "I thought I bought my domain for two years, full stop. Why was my card charged again last week?\"""",
"AR", 1, 3, t="section 5", neg=True),

# 90 insurance policy renewed unless told not to
C("ar_insurance_policy",
"""Wrenfield Home Insurance - Policy Schedule, "Your cover period and renewal"

"This policy is written for a 12-month period. Before it ends we will write to remind you of the renewal date. Unless you tell us not to renew, we will renew your cover on the same terms and collect the premium by the same payment method. You can ask us to stop the renewal at any time before the renewal date."

Policyholder's question on the customer forum: "I'm moving house in the spring. Will my old policy just run out at the end of the year, or do I need to do something?\"""",
["AR", "UC", "TWC", "LOL", "DS", "TFC", "COL", "NONE"], "AR", 2, t="the \"Your cover period and renewal\" paragraph"),

# 91 support periods need a purchase order
Y("ar_support_po",
"""Software Support Terms - Redfern Labs (Licensor) and Oxbow Energy Cooperative (Licensee)

"2.1 Support Periods. Support is provided in twelve-month Support Periods. Licensee may purchase additional Support Periods by submitting a purchase order before the current Support Period expires. Support will not continue past the end of a Support Period unless such a purchase order has been received. Licensor will send a reminder 60 days before each Support Period ends."

Procurement analyst's note: "Flag every auto-renewing obligation in our software stack before budget season.\"""",
"AR", 0, 3, t="section 2.1"),

# 92 large option set: newspaper continuous service
C("ar_big",
"""Harrowgate Gazette - Digital + Print Subscription Terms

"Continuous Service. To make sure you don't miss an issue, your subscription will continue after your initial term for further terms of the same length, unless you contact Reader Services to stop it. We will send a reminder by email at least 14 days before each new term begins."

"Delivery. Print editions are delivered by 7 am on publication days. If your paper does not arrive, report it by 11 am for a replacement or credit."

Reader Services training sheet, exercise 3: tag the "Continuous Service" paragraph using the full clause taxonomy.""",
["AR", "UC", "TWC", "TFC", "LOL", "WD", "DS", "DR", "CR", "LIC", "COL", "ARB", "FM", "NONE"], "AR", 3,
t="the \"Continuous Service\" paragraph"),
]
