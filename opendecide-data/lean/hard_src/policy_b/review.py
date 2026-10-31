"""policy_b / product and business reviews (Shelfwise, Brambleway, NookRate)."""
from _lib import C, Y, T

SW = [
    ("incentivised without disclosure", "the reviewer received something for the review and did not disclose it."),
    ("conflict of interest", "the reviewer is the seller, maker, their staff or family, or a competitor."),
    ("not about the product", "the review is only about delivery, packaging or seller service."),
    ("medical claim", "the review states a product cures or treats a disease, or advises changing treatment."),
    ("personal information", "the review exposes private details of an individual."),
    ("abusive language", "profanity or insults aimed at a person."),
    ("duplicate review", "the same reviewer posted substantially the same review more than once."),
    ("spam link", "the review contains promotional links or referral codes."),
    ("safety misinformation", "the review asserts an unverified safety defect or recall as fact."),
    ("none of these", "the review breaks none of the listed rules."),
]

NR = [
    ("conflict of interest", "the reviewer is the owner, an employee or family of the business, or works for a direct competitor."),
    ("not based on experience", "the review does not reflect the reviewer's own visit, purchase or use."),
    ("personal information", "the review exposes private details of an individual."),
    ("profanity at a person", "profanity or insults aimed at staff, the owner or another reviewer."),
    ("second-hand allegation", "an allegation of misconduct the reviewer only heard about."),
    ("spam link", "promotional links or referral codes."),
    ("off-topic", "the review is mainly about politics, news or matters unrelated to the business."),
    ("incentivised without disclosure", "the reviewer received something for the review and did not disclose it."),
    ("extortion", "the reviewer threatens a negative review unless compensated."),
    ("duplicate", "the same reviewer posted substantially the same review more than once."),
    ("hate speech", "attacks on people based on a protected characteristic."),
    ("none of these", "the review breaks none of the listed codes."),
]

TRI = [("remove", "the review is taken down."),
       ("label", "the review stays up with the relevant label."),
       ("no action", "the review stays up unchanged.")]

ITEMS = [
# ------------------------------------------------------------------ rv01
Y("rv01", "Does this review need an incentive disclosure under IN-1?",
"""
Shelfwise Review Guidelines — Incentives (IN-1)
A review is incentivised if the reviewer received something in exchange for writing it or for a positive rating: free or discounted product, payment, gift cards, giveaway entries, or refunds offered on condition of a review. Incentivised reviews must include a clear disclosure. Replacements or refunds provided under warranty, a return policy, or to fix a defect are NOT incentives, as long as they weren't conditional on the review.

Review — Harwick Steel 1.7L Kettle ★★★★★ (Verified purchase)
"My first one leaked from the base after two weeks. Emailed the seller and they sent me a new one for free, no questions asked. The replacement has been perfect for three months — boils fast, quiet, the auto-off works every time. Great customer service and a great kettle."
Flag reason: keyword "for free".
""",
[("Incentive", "something given in exchange for writing a review or for a positive rating."),
 ("Warranty replacement", "a replacement or refund to fix a defect, not conditional on a review.")],
0, 2),

# ------------------------------------------------------------------ rv02
C("rv02", "Which removal reason, if any, applies to this humidifier review?",
"""
Shelfwise — Product review removal reasons (reviewer guide)
Reviews must describe the reviewer's experience with the product. A review that is only about delivery, packaging or the seller's service is removed as "not about the product"; if it also describes using the product, it stays and the delivery comments are allowed.

Review — MistPeak Ultrasonic Humidifier 4L ★★★☆☆ (Verified purchase)
"Delivery was three days late and the box looked like it had been dropped off a truck — one corner totally crushed. Honestly expected the worst. The unit itself survived: it's quiet enough to sleep next to, the 4L tank runs all night on medium, and the auto-shutoff kicks in when it's empty. Lost two stars for the delivery mess."
Automated classifier: "shipping complaint" (0.78).
""",
SW, "none of these", 2),

# ------------------------------------------------------------------ rv03
# why: left in 2019, review Sept 2026 -> outside 24 months -> not barred.
Y("rv03", "Is this review barred by CI-2?",
"""
Shelfwise Review Guidelines — Conflicts of Interest (CI-2)
The following people may not review a product: the seller or manufacturer; their current employees and contractors; former employees who left within the last 24 months; immediate family of any of these; and employees of a direct competitor. The review date is used to measure the 24 months.

Review — Tallis Audio Stratos Bookshelf Speakers ★★★★★ — posted 12 Sept 2026
"Full disclosure: I worked in Tallis Audio's QA lab until I left the company in 2019. I bought these with my own money last month. Built like tanks, the bass is tight without being boomy, and the binding posts are the same beefy ones I used to test. Strongly recommend."
Reviewer badges: Verified purchase.
""",
[("Barred reviewer", "the seller, manufacturer, current staff, former staff who left within 24 months, their immediate family, or a competitor's staff.")],
0, 2,
twin=T([("until I left the company in 2019.", "until I left the company in March 2026.")], 1)),

# ------------------------------------------------------------------ rv04
C("rv04", "What should happen to this review under HC-3?",
"""
Shelfwise — Health Claims in Reviews (HC-3)
• Remove: the review states as a general fact that a product cures, treats or prevents a disease, OR advises others to stop or replace a prescribed treatment.
• Label ("Personal experience — not medical advice"): the review describes the reviewer's own experience of a disease or condition improving, without presenting it as a general fact and without advising others to change treatment.
• No action: no disease or medical condition is mentioned ("skin felt softer").

Review — Oatleaf Calming Body Cream 200ml ★★★★★ (Verified purchase)
"I've had psoriasis on my elbows for years. Started using this twice a day alongside my usual routine and after about two weeks the patches were noticeably calmer. Obviously everyone's skin is different. Smells like nothing, which I love."
""",
TRI, "label", 2,
twin=T([("Obviously everyone's skin is different.", "This cream cures psoriasis, full stop — bin your steroid creams.")], "remove")),

# ------------------------------------------------------------------ rv05
Y("rv05", "Should this review be removed under HP-1?",
"""
NookRate — Humour & Parody Reviews (HP-1)
Humorous, exaggerated or parody reviews are allowed when (a) the reviewer has a verified purchase of the product, and (b) the review doesn't make false factual claims about the product's safety or ingredients. Parody reviews without a verified purchase are removed as "not based on experience".

Review — SliceRight Banana Slicer ★★★★★
Verified purchase: Yes (ordered 2 Aug 2026)
"Changed my life. Before this, I was slicing bananas with a knife like some kind of medieval peasant. My marriage is saved, my children respect me, and my bananas are now in perfectly identical coins. 10/10, would slice again. The yellow one matches my kitchen."
Reported by: 3 users ("fake review", "joke review").
""",
[("Allowed parody", "a humorous review from a verified purchaser with no false safety or ingredient claims."),
 ("Not based on experience", "a parody review without a verified purchase.")],
0, 1),

# ------------------------------------------------------------------ rv06
C("rv06", "Under SC-2, what should the moderator do with this car seat review?",
"""
Brambleway — Safety Claims in Product Reviews (SC-2)
Before deciding, check the Recall Registry panel.
• If a recall matching the claim is listed for this model → no action (the review is accurate).
• If no matching recall is listed and the review asserts a recall or safety defect as fact → remove.
• If no matching recall is listed and the review raises it as a question, rumour or unverified possibility → label with "Check the official recall database".

Review — Cradlewise Nova 360 Convertible Car Seat ★★☆☆☆ (Verified purchase)
"Not sure if this is true but I read on a parenting forum that this model was recalled for the buckle popping open?? Has anyone else heard this? Be careful, parents. Ours has been fine so far but I'm nervous now."

Recall Registry panel (checked 10 Sept 2026): No active recalls for Cradlewise Nova 360. One recall (RR-2025-044, harness strap) is listed for the older Cradlewise Nova 2 model.
""",
TRI, "label", 3,
twin=T([("No active recalls for Cradlewise Nova 360. One recall (RR-2025-044, harness strap) is listed for the older Cradlewise Nova 2 model.",
         "Active recall RR-2026-117 for Cradlewise Nova 360: buckle may release unexpectedly.")], "no action")),

# ------------------------------------------------------------------ rv07
Y("rv07", "Does this review breach NI-2?",
"""
NookRate — Local Business Reviews: Naming Individuals (NI-2)
Reviews may name staff by first name only when praising them or describing neutral facts ("Marco took our order"). A review that names an individual employee (first name or full name) in connection with criticism, complaints or allegations is edited to remove the name; if the reviewer won't edit it, the review is removed. Criticism of "our server" or "the staff" without a name is fine.

Review — Trattoria Ossobuco, Harwick ★★☆☆☆
"Food was decent — the carbonara was properly made, no cream. But our server Marco was rude, ignored us for 20 minutes, then rolled his eyes when we asked for the bill. Won't be back on a Saturday."
Reviewer: "Gemma T." (Local Guide level 4).
""",
[("Named criticism", "a named employee linked to criticism, complaints or allegations."),
 ("Permitted naming", "a first name used in praise or a neutral description.")],
1, 1),

# ------------------------------------------------------------------ rv08
# why: S1 yes, S2 no (9 sellers), S3 yes, S4 no (0.62), S5 no -> 2 -> manual review.
C("rv08", "What is the CR-4 outcome for case CR-4-10288?",
"""
Shelfwise Integrity — Coordinated Review Check (CR-4)
Count how many of these five signals are present:
S1 the reviewer account is less than 7 days old;
S2 the reviewer has reviewed only products from this seller;
S3 the review was posted within 48 hours of four or more other 5-star reviews of the same product;
S4 text similarity to another review of the same product is above 0.80;
S5 the reviewer's location is outside every region the product ships to.
0–1 signals → clear. 2 signals → hold for manual review. 3+ signals → remove as coordinated.

Case CR-4-10288 — review of "GlowNest Sunrise Alarm Clock" ★★★★★
Account age: 3 days. Reviews by this account: 11 in total, covering 9 different sellers.
Posting time: 14:02 on 6 Sept; four other 5-star reviews of the product were posted between 5 Sept 20:10 and 6 Sept 11:45.
Highest text similarity to another review of this product: 0.62.
Reviewer location: Harwick (the product ships to Harwick).
""",
[("clear", "0–1 signals present."),
 ("hold for manual review", "exactly 2 signals present."),
 ("remove as coordinated", "3 or more signals present.")],
"hold for manual review", 3, ordered=True,
twin=T([("Highest text similarity to another review of this product: 0.62.", "Highest text similarity to another review of this product: 0.86.")],
       "remove as coordinated")),

# ------------------------------------------------------------------ rv09
Y("rv09", "Is it not the case that this review breaks CM-1?",
"""
Brambleway — Competitor Mentions (CM-1)
Reviews may compare the product with competing products or say the reviewer switched to another brand. Reviews may not include links to competitors, competitor coupon or discount codes, or instructions to buy elsewhere at a specific retailer. Such reviews are removed as spam.

Review — Kitchenmate Blend 600 ★★☆☆☆ (Verified purchase)
"Motor stalled on frozen fruit within a week, and the lid leaks when it's more than half full. I returned it and bought the Corvane 900 instead, which is in a completely different league for smoothies. If you blend frozen stuff daily, spend the extra."
Flag: "competitor brand mentioned".
""",
[("Competitor comparison", "comparing with, or switching to, another brand; allowed."),
 ("Competitor spam", "competitor links, coupon codes or instructions to buy at a specific retailer.")],
1, 2, role="neg"),

# ------------------------------------------------------------------ rv10
C("rv10", "Which AL-3 outcome applies to the Bright Smile Dental review?",
"""
NookRate — Allegations in Reviews (AL-3)
• First-hand allegations (the reviewer describes what happened to them) of misconduct, negligence or illegal conduct are allowed. Naming the licensed professional who treated the reviewer is allowed.
• If the business has filed a formal dispute of a first-hand allegation through the Business Response tool, the review stays up with a "Disputed by business" label. Do not remove.
• Second-hand allegations ("I heard", "my friend says", "people online say") are removed.

Review — Bright Smile Dental, Brinmouth ★☆☆☆☆
"Dr. Halloran pulled the wrong tooth — the healthy molar next to the cracked one. I had to go to another dentist to get the cracked one out. Two extractions instead of one and they still charged me in full."

Business Response tool: Formal dispute filed 4 Sept 2026 — "We dispute this account. Our records show the extracted tooth matched the treatment plan signed by the patient."
""",
[("remove — second-hand allegation", "the allegation is not the reviewer's own experience."),
 ("allow — first-hand experience", "the review stays up unchanged."),
 ("label — disputed by business", "the review stays up with a 'Disputed by business' label."),
 ("remove — personal information", "the review exposes private details of an individual.")],
"label — disputed by business", 2,
twin=T([("Formal dispute filed 4 Sept 2026 — \"We dispute this account. Our records show the extracted tooth matched the treatment plan signed by the patient.\"",
         "no response or dispute filed.")], "allow — first-hand experience")),

# ------------------------------------------------------------------ rv11
Y("rv11", "Does the Fernhollow insert amount to review gating under RG-1?",
"""
Shelfwise Seller Policy — Review Gating (RG-1)
Sellers may ask customers to leave a review and may separately offer customer support. Sellers may not "gate" reviews: asking only satisfied customers to review, conditioning a review request on the customer's experience, or steering unhappy customers to contact the seller instead of reviewing. Example of gating: "Happy? Review us! Not happy? Contact us first."

Case RG-1-0442 — package insert from seller "Fernhollow Candles", reported by a customer:
"Thank you for your order! 🕯️ Loved your candle? Leave us a 5-star review on Shelfwise — it means the world to a small business. Something not right? Email hello@fernhollow.example and we'll make it right, no need to leave a review."
""",
[("Review gating", "soliciting reviews only from satisfied customers, or steering unhappy customers away from reviewing."),
 ("Permitted request", "asking all customers for a review while separately offering support.")],
1, 2),

# ------------------------------------------------------------------ rv12
C("rv12", "What should moderators do with the Arcline lamp review?",
"""
Brambleway — Product Reviews vs Seller Feedback (PR-4)
Product Reviews describe the product itself. Comments that are only about the seller's service — customer service, returns, delivery — belong in Seller Feedback; moderators move them there (they are not removed). Business contact details published by the seller on its own storefront are not personal information. Personal information means private details of an individual (personal phone, home address, personal email).

Review — Arcline LED Desk Lamp, sold by "Lumenhaus" ★☆☆☆☆
"Customer service never answered my emails about my return. Called their support line (555-0142, it's on their storefront) four times — nobody picks up. Useless. Still waiting on my refund."
""",
[("move to Seller Feedback", "the review is about seller service only and is moved, not removed."),
 ("remove — personal information", "the review exposes private details of an individual."),
 ("remove — spam", "the review is promotional or contains spam content."),
 ("no action", "the review stays in Product Reviews unchanged.")],
"move to Seller Feedback", 2),

# ------------------------------------------------------------------ rv13
Y("rv13", "Must this review be removed under HO-2?",
"""
Brambleway — Health Outcomes in Reviews of Non-Medical Products (HO-2)
Reviews of non-medical products (air purifiers, mattresses, humidifiers, cleaning products) may describe health outcomes the reviewer or their family experienced. A review is removed if it advises or describes stopping, reducing or replacing prescribed medication or treatment, or presents the product as a replacement for medical care.

Review — ClearDraft HEPA 400 Air Purifier ★★★★★ (Verified purchase)
"We put this in our son's room in March. Since then his asthma attacks at night have basically stopped — maybe one mild one in six months. His inhaler still goes everywhere with him, but it's been a huge relief. Filter changes are easy too."
""",
[("Health outcome", "a health change the reviewer or their family experienced; allowed."),
 ("Treatment change", "advising or describing stopping, reducing or replacing prescribed treatment.")],
0, 2),

# ------------------------------------------------------------------ rv14
C("rv14", "Which LG-1 outcome applies to the Trailhawk review?",
"""
NookRate — Language in Reviews (LG-1)
• Profanity describing a product, experience or situation ("this damn zipper", "crap quality") is allowed.
• Profanity or insults directed at a person — staff, the business owner, or another reviewer — lead to removal.
• Slurs of any kind lead to removal.
• There is no profanity label; reviews either stay up unchanged or are removed.

Review — Trailhawk 30L Daypack ★☆☆☆☆ (Verified purchase)
"This damn zipper broke on day two of a three-day hike. Absolute crap. Had to tie the pocket shut with a shoelace for 20 km. The straps are comfy, I'll give it that, but a pack that can't close is useless."
Flag: profanity filter (2 terms).
""",
[("remove — insult directed at a person", "profanity or insults aimed at staff, the owner or another reviewer."),
 ("remove — slur", "the review contains a slur."),
 ("label — contains profanity", "the review is shown with a profanity notice."),
 ("no action", "the review stays up unchanged.")],
"no action", 1),

# ------------------------------------------------------------------ rv15
Y("rv15", "Should this review be removed under RR-1?",
"""
Shelfwise Review Guidelines — Reviews Are Not Replies (RR-1)
A review must stand on its own. Reviews that respond to, argue with, or mock another reviewer or review are removed; readers can use the comments feature under each review instead. Mentioning common opinions in general ("some people say it's heavy") is fine.

Review — Ironbark 26cm Cast Iron Skillet ★★★★★ (Verified purchase)
"To the person who gave this 1 star because it's 'too heavy' — it's CAST IRON, what did you expect, a feather? Anyway: seasoned it three times, eggs slide right off now, and it holds heat beautifully for steak. Five stars."
""",
[("Reply review", "a review that responds to, argues with or mocks another reviewer or review."),
 ("General opinion", "mentioning what people commonly say without addressing a specific review.")],
1, 2),

# ------------------------------------------------------------------ rv16
C("rv16", "How should the Pinecrest Wool Throw review be handled under RL-2?",
"""
Shelfwise — Review Leverage (RL-2)
• Extortion: a reviewer states or implies that they will post, keep or raise a negative review unless the seller gives them money, a refund, free products or other compensation. The review is removed and the reviewer's account suspended.
• Updates: a reviewer may update a review to reflect how an issue was resolved ("seller refunded me, raising to 4 stars").
• Allowed: all other honest reviews.

Review — Pinecrest Wool Throw ★★★★☆ (Verified purchase) — edited 8 Sept 2026
"Original review (2 stars): arrived with a pulled thread across one corner. UPDATE: Seller refunded me in full within a day and told me to keep the throw. Bumping to 4 stars — the colour is gorgeous and it's really warm."
""",
[("remove and suspend — extortion", "the reviewer used the review to demand compensation."),
 ("allow — update after resolution", "the reviewer updated the review to reflect how an issue was resolved."),
 ("remove — incentivised without disclosure", "the reviewer received something for the review and did not disclose it."),
 ("label — edited review", "the review is shown with an 'edited' label.")],
"allow — update after resolution", 2),

# ------------------------------------------------------------------ rv17
Y("rv17", "Does Hana's display name comply with RP-3?",
"""
Shelfwise — Reviewer Profile Rules (RP-3)
Display names must not imitate Shelfwise status or staff roles, including "Top Reviewer", "Verified", "Shelfwise Staff", "Moderator" or "Early Reviewer", in any capitalisation or spacing, because these are badges Shelfwise awards. Names that include a brand name are allowed unless they imply the reviewer works for that brand ("Tallis Official", "Tallis Team").

Reviewer profile under review
Display name: Hana | Top Reviewer
Badges actually held: none
Reviews: 214 (average rating 3.9), member since 2019
Most recent review: "Kettle arrived dented but works fine. 3 stars."
""",
[("Imitated badge", "a display name containing a Shelfwise status or staff term in any capitalisation or spacing.")],
0, 1,
twin=T([("Display name: Hana | Top Reviewer", "Display name: Hana | Tea Reviewer")], 1)),

# ------------------------------------------------------------------ rv18
# why: hedged false claim + call to action ("throw out any chemical sunscreen") -> remove.
C("rv18", "What MI-2 outcome applies to the Sunhollow review?",
"""
Shelfwise — Misinformation in Reviews (MI-2)
• Remove: a false health or safety claim stated as fact; OR any false claim — even hedged ("I've heard", "not a doctor", "maybe") — that is followed by a call to action urging others to stop using or avoid a category of product or treatment.
• Label ("See expert guidance"): a false or unsupported claim framed as rumour, belief or uncertainty, with no call to action.
• No action: opinions and personal experiences with no false claims.

Reference: dermatology guidance states that chemical (organic) UV filters have not been shown to cause cancer; broad-spectrum sunscreen of either type is recommended.

Review — Sunhollow Mineral SPF 50 ★★★★★ (Verified purchase)
"I've heard chemical sunscreens can cause cancer, so I only use mineral ones like this — not a doctor tho 🤷‍♀️ So throw out any chemical sunscreen you have, seriously. This one doesn't leave much white cast and doesn't sting my eyes."
""",
TRI, "remove", 3,
twin=T([("So throw out any chemical sunscreen you have, seriously.", "Anyway, that's just my own choice.")], "label")),

# ------------------------------------------------------------------ rv19
Y("rv19", "Does this review fall under DU-1's removal rule?",
"""
Brambleway — Dangerous Use in Reviews (DU-1)
Reviews that recommend or describe using a product in a way its label warns against, where that use could cause injury, are removed. Reviews describing intended use, or warning others about misuse, are fine.

Product label excerpt — FlowForce Max Gel Drain Cleaner: "For drains only. Contains sodium hydroxide. Do not use on items that contact food or mouths. Keep away from children. Do not mix with other cleaners."

Review — FlowForce Max Gel Drain Cleaner ★★★★★ (Verified purchase)
"Honestly the best cleaner in the house. I soak my kids' plastic toys and their sippy cup lids in a diluted bucket of this once a month and they come out spotless. Also cleared our shower drain in 20 minutes."
""",
[("Dangerous use", "a use the product label warns against that could cause injury, recommended or described in a review.")],
1, 1),

# ------------------------------------------------------------------ rv20
C("rv20", "Which NookRate policy code applies to Joss B.'s review?",
"""
NookRate — Review Policy Codes (definitions are in the answer card)

Review — Maison Brioche Bakery, Harwick ★★☆☆☆
"Popped in on Saturday morning. The croissants were stale — honestly they tasted like yesterday's — and the flat white was lukewarm. I've been baking for fifteen years, so I know what a good croissant should taste like, and this wasn't it. Staff were friendly enough."

Reviewer: "Joss B.", 38 reviews, member since 2021.
Reviewer's public profile: "Head baker at Ferncastle Bakehouse, Harwick."
Map note: Ferncastle Bakehouse is directly across the street from Maison Brioche and sells croissants and coffee.
""",
NR, "conflict of interest", 2),

# ------------------------------------------------------------------ rv21
Y("rv21", "Must photo 1 be taken down under PH-2?",
"""
Shelfwise — Review Photos (PH-2)
Review photos must show the product. Photos may show the reviewer. Photos in which a child's face is identifiable are removed, even when uploaded by the child's parent; photos showing a child from behind, from the neck down, or with the face covered are allowed.

Review photo 1 of 2 — Puddlejump Kids' Rain Jacket, age 2–3 ★★★★★
Reviewer description: "My daughter wearing it in the garden!"
Moderator's image note: a toddler in the yellow jacket standing in a garden, facing the camera, face clearly visible and smiling; no other people.
Photo 2: the jacket laid flat on a table.
""",
[("Identifiable child", "a photo in which a child's face can be seen and recognised.")],
1, 1),

# ------------------------------------------------------------------ rv22
C("rv22", "Under CD-3, how should the Evenfall blanket review be handled?",
"""
Brambleway — Codes in Reviews (CD-3)
• Site-wide public promotions published on Brambleway's own Deals page may be mentioned in reviews.
• Referral, affiliate or personal codes that credit or reward the reviewer are spam; the review is removed.
• Codes given to the reviewer by the seller in exchange for the review are handled as incentivised reviews (disclosure required).

Review — Evenfall Weighted Blanket 7kg ★★★★★ (Verified purchase)
"Best sleep I've had in years, and it doesn't overheat like my old one. Use code MAYA15 for 15% off your first order!"

Code lookup: MAYA15 — type: referral; linked account: the reviewer (maya_d); reward: $5 credit per use.
""",
[("remove — spam (referral code)", "the code credits or rewards the reviewer."),
 ("allowed — public promotion", "the code is a site-wide promotion from Brambleway's Deals page."),
 ("incentivised — disclosure required", "the seller gave the reviewer the code in exchange for the review.")],
"remove — spam (referral code)", 1),

# ------------------------------------------------------------------ rv23
Y("rv23", "Is this review permitted under IN-3?",
"""
Shelfwise — Incentivised Reviews (IN-3)
• Shelfwise Early Reviewer programme: allowed; the badge is added automatically.
• External brand programmes that give free or discounted products for an honest review: allowed only with a clear disclosure in the review text.
• Giveaways, contests or raffles where posting a review is a condition of entry or of winning: prohibited, with or without disclosure.

Review — Aerlume Mini Projector ★★★★☆
"Disclosure: I received this projector free through the brand's tester programme in exchange for an honest review. Picture is sharp up to about 80 inches in a dark room; fan noise is noticeable in quiet scenes. The built-in speaker is weak — plan on Bluetooth."
Badges: none.
""",
[("External programme", "a brand scheme giving free or discounted products for an honest review; needs disclosure."),
 ("Conditional giveaway", "a giveaway, contest or raffle requiring a review to enter or win; always prohibited.")],
1, 2,
twin=T([("I received this projector free through the brand's tester programme in exchange for an honest review.",
         "I won this projector in the brand's summer giveaway, which required entrants to post a review to qualify.")], 0)),

# ------------------------------------------------------------------ rv24
C("rv24", "Which RV-2 outcome applies to the Dunmore Roasters review?",
"""
Shelfwise — Relevance (RV-2)
Reviews must be primarily about the product. A review whose main content is about the brand's politics, owners, news events or social causes is removed as off-topic. Brief mentions of such reasons are allowed when the review also describes the reviewer's own experience of the product.

Review — Dunmore Roasters House Blend, 1kg beans ★★★☆☆ (Verified purchase)
"Smooth, nutty, low acidity — works great as espresso and in the moka pot, and the beans were roasted 5 days before they arrived. Knocked off two stars because I won't be buying again after reading that the owner donated to Senator Kell's campaign."
Reported by: 2 users ("political review").
""",
[("remove — off-topic", "the review is mainly about politics, owners, news or causes."),
 ("allowed", "the review is primarily about the product."),
 ("remove — hate speech", "the review attacks people based on a protected characteristic."),
 ("remove — personal information", "the review exposes private details of an individual.")],
"allowed", 2),

# ------------------------------------------------------------------ rv25
Y("rv25", "Can this review stay up under PRR-1?",
"""
Shelfwise — Pre-Release Reviews (PRR-1)
Reviews posted before a product's official release date are removed unless the reviewer holds the Early Reviewer badge for that product. After the release date, reviews are allowed normally. Release dates are taken from the product page.

Product page — Vantor X2 Wireless Earbuds: release date 1 Oct 2026. Pre-orders open.

Review ★★★★★ — posted 20 Sept 2026 by "rafe_listens"
"Got a pair early from a friend who works in retail. The noise cancelling is shockingly good for the price, and the case charges wirelessly. Battery lasted a full workday."
Reviewer badges: Verified purchase — No; Early Reviewer — No.
""",
[("Pre-release review", "a review posted before the product's release date."),
 ("Early Reviewer badge", "the badge that exempts a reviewer from the pre-release rule for that product.")],
0, 1),

# ------------------------------------------------------------------ rv26
C("rv26", "What should Brambleway do with the GlucoTrack Mini review under MD-2?",
"""
Brambleway — Reviews of Medical Devices (MD-2)
• A review that reports a possible defect or safety problem with a medical device based on the reviewer's own use (inaccurate readings, overheating, alarms failing) stays up and is routed to Product Safety for follow-up.
• A review that claims a device treats or cures a disease beyond its labelled use is removed.
• A review that only discusses comfort, price or delivery needs no action.

Review — GlucoTrack Mini Blood Glucose Meter ★☆☆☆☆ (Verified purchase)
"Compared it with my lab results three times this month — it reads 18–22 points higher every time. I use it to decide my insulin doses so this is genuinely dangerous. Don't trust it for dosing until they sort it out."
Flag: "medical advice" keywords ("insulin", "dosing").
""",
[("remove — medical claim", "the review claims the device treats or cures a disease beyond its labelled use."),
 ("keep and route to Product Safety", "the review stays up and is sent to Product Safety for follow-up."),
 ("no action", "the review only covers comfort, price or delivery."),
 ("label — personal experience", "the review is shown with a personal-experience notice.")],
"keep and route to Product Safety", 2),
]
