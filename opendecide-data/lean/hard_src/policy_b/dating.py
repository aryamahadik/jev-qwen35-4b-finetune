"""policy_b / dating profiles (Kindling, Tandem Hearts, Orchard Match)."""
from _lib import C, Y, T

KC = {
    "underage indication": "The profile indicates the user may be under 18 (stated age, current school year, graduation year still to come). Working at a school or being an alumnus is not an indicator.",
    "impersonation": "The account presents itself as another real, identifiable person.",
    "transactional arrangement": "Offers or seeks money, gifts, allowances or payment in exchange for companionship, dates, attention or intimacy.",
    "commercial solicitation": "Promotes a business, product, paid content, referral scheme or investment.",
    "hateful exclusion": "Insults, stereotypes or dehumanises people based on a protected characteristic.",
    "contact details": "Phone numbers, email addresses or payment handles anywhere on the profile, in any spelling; social handles outside the Socials field.",
    "misleading photos": "Photos that are not of the account holder, or edited photos without the Edited tag.",
    "explicit sexual content": "Explicit descriptions of sexual acts, sexual requests or nudity.",
    "health misinformation": "False health claims that contradict public-health guidance.",
    "violent content": "Threats, glorification of violence, or weapons shown in a threatening way.",
    "hateful symbols": "Hate codes, numbers or symbols listed in the hate symbols appendix.",
    "ban evasion": "A new account created by a person whose previous account was banned.",
    "fake verification symbols": "Characters in a name that imitate the verification badge.",
    "none of these": "The profile does not fall under any of the listed categories.",
}


def kc(*names):
    return [(n, KC[n]) for n in names]


ITEMS = [
# ------------------------------------------------------------------ dt01
# why: photo 3 has face-shape edits (slim face, jawline) and no Edited tag.
Y("dt01", "Does Maren's profile breach PA-1?",
"""
Kindling Photo Authenticity Standard (PA-1)
Photos must show the account holder as they currently look. Photos that are AI-generated, or edited in a way that changes the shape or size of facial features or the body (slimming, jaw or nose reshaping, eye enlarging, body "sculpting"), must carry the "Edited" tag. Colour and lighting filters, background blur, cropping, and stickers or overlays that do not cover the face are exempt and need no tag.

Moderation ticket K-55190 — automated edit-detection result for profile "Maren, 29"
Photo 1: unedited (confidence 0.94)
Photo 2: warm-tone colour filter; background blur
Photo 3: FaceTune — "Slim face" 35%, "Jawline" 20%
Photo 4: unedited
Photo 5: sticker overlay (dog ears) above the head; face uncovered
"Edited" tag applied to: none

Report reason from another member: "She looks totally different in person."
""",
[("Edited tag", "a label required on photos that are AI-generated or that change the shape or size of facial features or the body."),
 ("Exempt edits", "colour and lighting filters, background blur, cropping, and stickers that do not cover the face.")],
1, 2,
twin=T([("Photo 3: FaceTune — \"Slim face\" 35%, \"Jawline\" 20%", "Photo 3: FaceTune — \"Brightness\" +15, \"Warmth\" +10")], 0)),

# ------------------------------------------------------------------ dt02
# why: paying $5 for access to her Snap = transactional (rank 3) beats contact details (rank 6).
C("dt02", "Using the priority order, which category should report R-81244 be filed under?",
"""
Kindling Community Standards — how to categorise
When a profile fits more than one category, choose the one that appears earliest in this order: 1 underage indication, 2 impersonation, 3 transactional arrangement, 4 commercial solicitation, 5 hateful exclusion, 6 contact details, 7 misleading photos, 8 explicit sexual content.

Report R-81244 — reported profile "Jaz, 24" (ID-verified, 24)
Bio: "Gemini ☀️ matcha addict, part-time nail tech. Only serious guys pls. If you want my snap, venmo me $5 first — @jaz-nails-24 — I don't give it out for free 💅 Swipe left if you're boring."
Photos: 4, selfie-verified.
Reporter comment: "She's advertising her nail business?"
""",
kc("underage indication", "impersonation", "transactional arrangement", "commercial solicitation", "hateful exclusion", "contact details", "misleading photos", "explicit sexual content", "none of these"),
"transactional arrangement", 3),

# ------------------------------------------------------------------ dt03
# why: graduation year 2027 is later than 2026 -> indicator (c).
Y("dt03", "Does Dylan's profile trigger MS-2 removal?",
"""
Orchard Match — Minor Safety Indicators (removal policy MS-2), applied as of review date 21 Sept 2026
Remove the profile and require age re-verification if it contains any of:
(a) a stated age under 18;
(b) a school grade or year implying the user is currently in secondary school ("junior", "Year 12", "sixth form");
(c) a high-school graduation year later than the current calendar year;
(d) photos in a secondary-school uniform that appear current.
Not indicators: working at a school (teacher, coach), being an alumnus, or referring to past school years.

Profile "Dylan, 19" (date of birth unverified)
Bio: "Class of '27 at Harwick High — go Otters! 🦦 Lifeguard in summer, drummer in a very bad band. Looking for someone to get pancakes with after practice."
Photos: 3 — at a lake, drumming, with a dog.
""",
[("Minor safety indicator", "any of MS-2 (a)–(d) suggesting the user is under 18."),
 ("Not an indicator", "working at a school, being an alumnus, or mentioning past school years.")],
1, 2,
twin=T([("Class of '27 at Harwick High", "Class of '25 at Harwick High")], 0)),

# ------------------------------------------------------------------ dt04
C("dt04", "Which category, if any, applies to Talia's profile?",
"""
Tandem Hearts — Preferences vs. Hateful Exclusion (Guideline HE-4)
Members may say who they want to date, including by religion, ethnicity, body type or politics, when it is phrased as their own preference or identity ("I'm looking for someone who shares my faith"). Hateful exclusion is content that insults, stereotypes or dehumanises a group defined by a protected characteristic — for example linking a religion to violence, or calling a group dirty, stupid or subhuman — even when framed as a preference.

Reported profile "Talia, 33"
Bio: "I'm Jewish, keep a kosher-ish home, and I want to build a Jewish family — so I'm only looking to match with Jewish men. Please don't take it personally if we don't match! Big on Shabbat dinners, hiking the Marrin trails, and terrible puns."

Reporter's comment: "This is discrimination, she's excluding everyone who isn't Jewish."
""",
kc("hateful exclusion", "contact details", "commercial solicitation", "explicit sexual content", "misleading photos", "transactional arrangement", "none of these"),
"none of these", 2),

# ------------------------------------------------------------------ dt05
Y("dt05", "Is Mira's profile in breach of CD-1?",
"""
Kindling Contact Details Rule (CD-1)
• Phone numbers, email addresses and payment handles (Venmo, CashApp, PayPal etc.) are not allowed anywhere on a profile.
• Social media handles are allowed ONLY in the dedicated "Socials" field, which Kindling shows after a match. Handles written in the bio, prompts or photos are violations, even if they are the member's own.

Profile audit — "Mira, 27"
Bio: "Ceramicist by day, karaoke menace by night 🎤 My mugs are wonky on purpose. If you want to see what I make, find my pottery on IG: @mira.makes.pots. Looking for someone who'll eat questionable street food with me."
Socials field: (empty)
Prompt — "My ideal Sunday": "Farmers market, then a nap that's too long."
""",
[("Socials field", "the dedicated profile field for social handles, shown only after a match."),
 ("Contact detail violation", "a phone number, email or payment handle anywhere, or a social handle outside the Socials field.")],
1, 1),

# ------------------------------------------------------------------ dt06
C("dt06", "What enforcement action does case K-60318 call for?",
"""
Kindling Enforcement Guide — Misleading identity (photos of another real person)
Default action: remove the photos and require selfie verification before the account can be used again.
Escalations (apply the most severe that fits):
• If the photos belong to a person with a public following of 10,000+ on any platform, or to a Kindling member who reported the misuse, the account is permanently banned.
• If the account has a prior misleading-identity action in the last 12 months, apply a 30-day suspension in addition to verification.

Case K-60318
Profile "Anya, 26" (not selfie-verified). Reverse image search: all 5 photos match the public Instagram account @anya.lifts (48,300 followers), a fitness creator in Marrin. The creator has not contacted Kindling.
Account history: created 9 days ago, no prior actions.
Account holder's appeal: "These are my friend's photos and she said it's fine."
""",
[("no action", "the profile is left as it is."),
 ("remove photos and require verification", "the photos are removed and the member must pass selfie verification."),
 ("30-day suspension with verification", "the account is suspended for 30 days and must pass verification."),
 ("permanent ban", "the account is permanently banned.")],
"permanent ban", 2, ordered=True),

# ------------------------------------------------------------------ dt07
Y("dt07", "Does Graham's bio violate TA-1?",
"""
Kindling Transactional Arrangements Rule (TA-1)
Not allowed: offering or seeking money, allowances, gifts, rent, tuition or other material support as a condition of, or in exchange for, dating, companionship or intimacy. Terms like "arrangement", "mutually beneficial", "allowance", "PPM" or "sugar" are strong indicators.
Allowed: describing your lifestyle, income or generosity in general terms, or saying you like to treat a partner, when nothing is offered in exchange for the relationship.

Profile "Graham, 52"
Bio: "Recently retired architect, splitting time between Harwick and the coast. Love sailing, jazz, and a good long lunch. I'm generous and I spoil the woman in my life — weekend trips, great dinners, whatever makes her smile. Looking for warmth, humour and someone who can beat me at Scrabble."

Report reason: "sugar daddy profile".
""",
[("Transactional arrangement", "money, allowances, gifts or material support offered or sought in exchange for dating, companionship or intimacy.")],
0, 2,
twin=T([("weekend trips, great dinners, whatever makes her smile.", "weekend trips, great dinners, and a monthly allowance for the right arrangement.")], 1)),

# ------------------------------------------------------------------ dt08
C("dt08", "Under HS-2, what should happen to Corin's bio?",
"""
Orchard Match — Health Statements in Profiles (HS-2)
Classify statements about vaccines or communicable diseases as follows:
• Remove: claims presented as fact that contradict public-health guidance about how a disease spreads or about vaccine safety (for example that vaccinated people "shed" and infect others, or that vaccines cause infertility), or content urging others to refuse a vaccine.
• Label ("Health info: see public guidance"): statements of the member's own opinion or choice about a vaccine or treatment that make no factual claims about others' health or about how disease spreads.
• No action: statements that only disclose the member's own health status ("fully vaccinated", "HIV undetectable, on PrEP") without opinion.

Profile "Corin, 38"
Bio: "Carpenter, dog dad, off-grid weekends. Unvaxxed & proud — pureblood only, the jabbed shed spike proteins so no thanks. Looking for someone who likes campfires and honesty."
""",
[("remove", "the bio is taken down for a factual health claim that contradicts guidance, or for urging refusal."),
 ("label", "the bio gets a 'Health info: see public guidance' label for an opinion or choice."),
 ("no action", "the bio only discloses the member's own health status.")],
"remove", 2,
twin=T([("Unvaxxed & proud — pureblood only, the jabbed shed spike proteins so no thanks.", "Unvaxxed & proud — my body, my choice.")], "label")),

# ------------------------------------------------------------------ dt09
Y("dt09", "Should this profile be actioned as impersonation under IM-1?",
"""
Tandem Hearts Impersonation Policy (IM-1)
Impersonation means presenting the account as belonging to another real person, including by using that person's name as the display name, stating or implying you are them, or using their photos. Saying you resemble a public figure while using your own verified photos and your own name is not impersonation.

Report T-33871 — reported profile
Display name: Dario
Verification: selfie-verified ✓ (photos match the account holder)
Bio: "Yes, I know I look like Tomas Vance. No, I can't sing, and no, I can't get you tickets to his tour 😅 Line cook, cyclist, will absolutely judge your hot sauce collection."
Reporter: "Fake account pretending to be Tomas Vance the singer."
""",
[("Impersonation", "presenting the account as another real person by name, claim or photos."),
 ("Resemblance", "saying you look like a public figure while using your own name and verified photos.")],
0, 1),

# ------------------------------------------------------------------ dt10
C("dt10", "Which queue should Hana's report be routed to?",
"""
Kindling Trust & Safety — report routing guide (v7)
Route each report to exactly one queue:
Q1 Minor Safety — anything suggesting a user under 18.
Q2 Identity & Impersonation — fake identities, stolen photos.
Q3 Scams & Fraud — deceptive schemes to obtain money or financial information, including romance-investment scams, fake emergencies, and moving conversations to other apps to pitch investments.
Q4 Hate & Harassment.
Q5 Commercial Spam — profiles or messages promoting a genuine business, product or paid content.
Q6 Sexual Content.
Q7 Health Misinformation.
Q8 Off-Platform Safety — threats, assault or stalking after meeting.
Q9 Account Security — the reporter's own account was compromised.
Q10 No Violation — close.

Report text (from member "Hana, 31"): "Matched with Leo two days ago, lovely chat at first. Yesterday he asked me to move to Telegram because Kindling is 'buggy'. Then he started telling me about his uncle's trading platform, said he makes a guaranteed 30% a month and he'd teach me if I opened an account with $500 to start. Nothing rude, he's really charming, but it feels off."
""",
[("Minor Safety", "reports suggesting a user under 18."),
 ("Identity & Impersonation", "fake identities and stolen photos."),
 ("Scams & Fraud", "deceptive schemes to obtain money or financial information."),
 ("Hate & Harassment", "hateful or harassing conduct."),
 ("Commercial Spam", "promotion of a genuine business, product or paid content."),
 ("Sexual Content", "sexual content violations."),
 ("Health Misinformation", "false health claims."),
 ("Off-Platform Safety", "threats, assault or stalking after meeting."),
 ("Account Security", "the reporter's own account was compromised."),
 ("No Violation", "nothing reportable; the report is closed.")],
"Scams & Fraud", 1),

# ------------------------------------------------------------------ dt11
Y("dt11", "Does Owen's profile break RS-1?",
"""
Kindling Relationship Status Rule (RS-1)
Kindling welcomes members who are single, separated, or in open or non-monogamous relationships. The "Status" field must match what the member says elsewhere on the profile. A member who describes being married, partnered or in an open relationship must choose "Separated", "In an open relationship" or "It's complicated" as appropriate — never "Single".

Profile "Owen, 41"
Status: Single
Bio: "My wife and I are ethically non-monogamous and she knows I'm here — happy for you to chat with her first if that helps you feel comfortable! Into bouldering, bad sci-fi, and cooking way too much food."
Report reason: "He's married!!"
""",
[("Status field", "the profile field showing Single, Separated, In an open relationship or It's complicated."),
 ("Mismatch", "a Status value that contradicts what the member says elsewhere on the profile.")],
1, 1),

# ------------------------------------------------------------------ dt12
C("dt12", "What should the reviewer do with Lena's profile under PI-3?",
"""
Orchard Match — Profile Integrity: pets, couples and characters (PI-3)
Every profile in Date mode must represent one real adult. Couples must use Duo mode. Profiles may be written in the voice of a pet as a joke, provided (a) at least one photo clearly shows the account holder's face, and (b) the bio gives the account holder's own first name. If no photo shows the account holder's face, send a "face photo required" request (the profile is hidden until one is added). Profiles for fictional characters or with no human account holder at all are removed as novelty profiles. Couples found in Date mode are moved to Duo mode.

Profile under review — Date mode
Name on profile: Lena, 31
Photos: 1) corgi in a raincoat; 2) corgi on a beach; 3) Lena holding the corgi, both facing the camera; 4) corgi asleep; 5) corgi in a birthday hat.
Bio: "Hi, I'm Biscuit 🐶 My human Lena is 31, a paramedic, and she has NO time to find a date because she spends it all rubbing my belly. Please take her to dinner so I can have the sofa to myself."
""",
[("remove — novelty profile", "the profile has no real human account holder or is for a fictional character."),
 ("face photo required", "the profile is hidden until a photo showing the account holder's face is added."),
 ("move to Duo mode", "the profile belongs to a couple and is moved out of Date mode."),
 ("no action", "the profile meets PI-3.")],
"no action", 2,
twin=T([("3) Lena holding the corgi, both facing the camera;", "3) Lena's hand holding a treat above the corgi;")], "face photo required")),

# ------------------------------------------------------------------ dt13
# why: body size falls under the appearance rule (warning), not protected characteristics.
Y("dt13", "Should the sender receive the 7-day suspension rather than a warning?",
"""
Tandem Hearts — Messaging Conduct Ladder
Unsolicited insulting remarks about another member's appearance → warning (first offence).
Insulting remarks that reference a protected characteristic → 7-day suspension (first offence).
Protected characteristics under this policy are: race, ethnicity, national origin, religion, disability, serious illness, sex, gender identity, sexual orientation and age. Body size and weight are covered by the appearance rule, not the protected-characteristic rule.

Reported message (sent after a match; reporter "Imani, 28"):
"You're cute for a fat girl but honestly not my type lol, good luck out there"
Sender history: no prior actions.
""",
[("Appearance insult", "an unsolicited insulting remark about how a member looks; first offence is a warning."),
 ("Protected-characteristic insult", "an insulting remark referencing a listed protected characteristic; first offence is a 7-day suspension.")],
0, 2,
twin=T([("cute for a fat girl", "cute for a deaf girl")], 1)),

# ------------------------------------------------------------------ dt14
C("dt14", "What is the right step for Priya's display name under DN-2?",
"""
Kindling Display Name Rules (DN-2)
Display names must be the member's real first name or a common nickname. They may include one emoji. They must not include characters that imitate Kindling's blue verification badge — including ✓, ✔, ✔️, ☑, ☑️, ✅ and blue-circle-with-check combinations — because verification can only be shown by the badge itself. Fix by requesting a rename; if the member refuses twice, restrict the profile.

Profile "Priya ✔️, 30" — selfie-verified: No
Bio: "Product designer, amateur baker, looking for a +1 for food festivals and someone who'll split dessert."
History: no previous rename requests on this profile.
""",
[("rename request", "the member is asked to change the display name."),
 ("restrict profile", "the profile is restricted after the member has refused two rename requests."),
 ("impersonation ban", "the account is banned for impersonating another person."),
 ("no action", "the display name complies with DN-2.")],
"rename request", 1),

# ------------------------------------------------------------------ dt15
Y("dt15", "Is Marcus's bio promotional content under CC-3?",
"""
Kindling Commercial Content Rule (CC-3)
Members may mention their job, business or side-hustle as part of who they are. Profiles may not include promotional content: links or URLs, discount or referral codes, prices, calls to action to buy, book or subscribe, or invitations to paid content.

Profile "Marcus, 34"
Job field: Personal trainer, Vantage Fitness
Bio: "Personal trainer 💪 Morning person, sorry in advance. If we match, your first session's on me — use code KINDLE20 at vantagefit.co 😉 Otherwise let's just get tacos. Dog: Pesto (the real star)."
""",
[("Promotional content", "links, discount or referral codes, prices, calls to action to buy, book or subscribe, or invitations to paid content."),
 ("Permitted mention", "simply stating one's job or business.")],
1, 1),

# ------------------------------------------------------------------ dt16
C("dt16", "Which category, if any, applies to Kofi's profile?",
"""
Orchard Match — Age Accuracy (AA-1)
The age shown on every profile is calculated from the ID-verified birth date and cannot be edited. Members may not state a different age as fact in their bio or prompts ("I'm actually 35"), but obvious jokes that don't contradict the displayed age ("forever 29", "young at heart", "spiritually 25") are permitted.

Profile "Kofi, 41" — ID verified ✓ (displayed age 41)
Bio: "Technically 41, spiritually 25, physically 60 after leg day. Secondary-school history teacher at Pinecrest High — ask me about the fall of the Sael Empire. Looking for someone to explore the coast with."

Report reason (automated): age-mismatch keywords; school-related keywords.
""",
[("underage indication", KC["underage indication"]),
 ("age misrepresentation", "stating an age different from the ID-verified age as fact."),
 ("impersonation", KC["impersonation"]),
 ("commercial solicitation", KC["commercial solicitation"]),
 ("none of these", KC["none of these"])],
"none of these", 2),

# ------------------------------------------------------------------ dt17
Y("dt17", "Does report OP-7730 meet the OP-1 threshold for off-platform enforcement?",
"""
Tandem Hearts — Off-Platform Conduct (OP-1)
Tandem Hearts takes action on things that happen off the app only when a member reports that another member threatened, sexually assaulted, physically harmed or stalked them, AND provides at least one piece of supporting information (screenshot, message log, police reference number, or a detailed first-hand account with date and place). Rudeness, lateness, lying about height, or a bad date are not covered; the reporter is offered block and unmatch tools instead.

Report OP-7730 from "Sienna, 30":
"We met for drinks at the Copper Lantern on Friday. He was rude to the waiter, talked over me all night, and then acted like I owed him for the drinks when I said I didn't want a second date. I left and blocked him. I just felt really uncomfortable and I don't want this to happen to someone else."
""",
[("Qualifying conduct", "a threat, sexual assault, physical harm or stalking by another member."),
 ("Supporting information", "a screenshot, message log, police reference, or detailed first-hand account with date and place.")],
0, 2),

# ------------------------------------------------------------------ dt18
C("dt18", "Which category, if any, does this profile fall under?",
"""
Kindling Hate Symbols Appendix H (excerpt)
The following are treated as hateful symbols when used in a username, display name or bio:
• "1488" or "14/88" in any form.
• "88" or "14" ONLY when combined with at least one other extremist indicator listed in this appendix (runes from list H-2, "WPWW", "RaHoWa", sun-wheel emoji combinations, or the phrase "fourteen words").
• Numbers that clearly express a birth year, age or jersey number in context ("born in '88") are not symbols unless combined as above.

Profile under review
Username: hiker_mae88
Display name: Mae
Bio: "Born in '88, raised on the Marrin coast 🌊 Nurse, hiker, pub-quiz captain. Will judge you (lovingly) on your trail snack choices."
Flag: automated number-pattern match ("88").
""",
kc("hateful symbols", "contact details", "underage indication", "impersonation", "none of these"),
"none of these", 2,
twin=T([("Username: hiker_mae88", "Username: mae1488")], "hateful symbols")),

# ------------------------------------------------------------------ dt19
Y("dt19", "Is photo 2 allowed under PC-2?",
"""
Orchard Match — Photos Including Children (PC-2)
Photos may include children only if (1) the account holder also appears in the same photo, and (2) the child's face is not visible — blurred, covered or turned away. Photos of children alone are removed. The rule applies to the member's own children, nieces, nephews and any other minor.

Review item — Profile "Tom, 36", photo 2 of 6
Image description (from reviewer): Tom is kneeling on a beach holding up a toddler (his niece, per the caption) who is wearing a yellow sun hat. The toddler's face is covered by a large heart sticker added in the app editor. Tom is smiling at the camera.
Caption: "Uncle duties 🏖️"
""",
[("Allowed child photo", "the account holder is in the same photo and the child's face is blurred, covered or turned away.")],
1, 1),

# ------------------------------------------------------------------ dt20
C("dt20", "How should message report K-M-90417 be categorised?",
"""
Kindling — In-app message report K-M-90417
Sender account: display name "Kindling Support", profile photo: the Kindling flame logo, age 30, created 1 day ago.
Message to reporter: "Hi, this is the Kindling Safety Team. Our system detected unusual activity and your account will be deactivated in 24 hours unless you confirm your identity at kindl-verify.help. Please do not reply to this message."

Kindling Community Standards (relevant sections):
• Impersonation of a real person — presenting as another identifiable individual.
• Impersonation of Kindling — presenting as Kindling staff, support or the company, including using Kindling's name or logo as a display name or photo.
• Credential phishing — attempting to obtain passwords, codes or ID documents. When phishing is carried out by an account posing as Kindling, categorise it under the Kindling section.
• Commercial solicitation — promoting products or services.
""",
[("impersonation of a real person", "presenting as another identifiable individual."),
 ("impersonation of Kindling", "presenting as Kindling staff, support or the company."),
 ("credential phishing", "attempting to obtain passwords, codes or ID documents."),
 ("commercial solicitation", "promoting products or services."),
 ("none of these", "no listed category applies.")],
"impersonation of Kindling", 1),

# ------------------------------------------------------------------ dt21
Y("dt21", "Does Ren's profile need removal under SC-1?",
"""
Tandem Hearts Sexual Content Standard (SC-1)
Not allowed on profiles: explicit descriptions of sexual acts, sexual body parts described in a sexual context, requests for sexual photos, or offers of sex. Allowed: stating your orientation, relationship style, or that you're interested in kink or casual dating, in non-explicit terms; flirtatious innuendo.

Profile "Ren, 35"
Prompt — "I'm looking for": "Someone kind, curious and open-minded. I'm into kink and fairly experienced — happy to talk details once we've actually chatted, not here. Also: must tolerate my sourdough obsession."
Prompt — "Green flags": "Communicates, respects boundaries, texts back within a geological era."
Report reason (automated): keyword "kink".
""",
[("Explicit sexual content", "explicit descriptions of sex acts, sexualised body parts, requests for sexual photos, or offers of sex."),
 ("Permitted", "non-explicit statements of orientation, relationship style, interest in kink or casual dating, and innuendo.")],
0, 1),

# ------------------------------------------------------------------ dt22
# why: device differs; photos + phone match (2) -> manual review, not auto ban.
C("dt22", "What outcome does BE-2 give for case BE-44102?",
"""
Kindling Ban Evasion Procedure (BE-2)
Compare a new account against the banned account using these signals: device ID, photos (any identical image), phone number, payment card.
• Device ID matches AND at least two other signals match → ban-evasion ban (no review).
• Device ID matches but fewer than two other signals match → manual review.
• Device ID does not match but at least two other signals match → manual review.
• Otherwise → no action.

Case BE-44102
Banned account: "Theo, 34" (banned 2 Aug 2026 for harassment)
New account: "Teddy, 34" (created 29 Aug 2026)
Signal comparison:
– Device ID: different (new device, first seen 28 Aug)
– Photos: 3 of 5 photos identical to the banned account
– Phone number: identical
– Payment card: no card on either account
Reporter: a member who was harassed by "Theo" and says "it's obviously him".
""",
[("ban-evasion ban", "the new account is banned without review."),
 ("manual review", "a moderator reviews the case before any action."),
 ("no action", "the new account is left alone."),
 ("request ID verification", "the member is asked to verify their identity with an ID document.")],
"manual review", 2,
twin=T([("– Device ID: different (new device, first seen 28 Aug)", "– Device ID: identical to the banned account")], "ban-evasion ban")),

# ------------------------------------------------------------------ dt23
Y("dt23", "Is Beth's bio removable misinformation under HM-1?",
"""
Orchard Match — Health Misinformation in Profiles (HM-1)
A false claim about a vaccine's safety or effects is removable misinformation when it asserts a causal link that public-health guidance rejects. Hedges or caveats — "I think", "just asking questions", "do your own research", "not a doctor" — do not change whether a statement asserts the claim. Credentials or occupation claims in the profile do not change the assessment either.

Public-health guidance reference (HPV vaccine): no causal link to infertility has been found; the vaccine is recommended for adolescents and young adults.

Profile "Beth, 31"
Bio: "ER nurse 🩺 night shifts, iced coffee, true crime podcasts. I think the HPV vaccine causes infertility — do your own research before you let them near your kids. Looking for someone who can make me laugh after a 12-hour shift."
""",
[("Removable misinformation", "a statement asserting a vaccine causal link that public-health guidance rejects, whatever hedges accompany it.")],
1, 1),

# ------------------------------------------------------------------ dt24
C("dt24", "Which category applies to Sofia's profile?",
"""
Tandem Hearts — Report review queue, report T-77019
Reported profile "Sofia, 26"
Bio: "Swipe right if you're NOT a Libra — I've been burned twice and I've learned my lesson 😂 Also no smokers, no guys who say 'haha' instead of laughing, and absolutely no one who's rude to waiters."
Report reason: "Discriminatory — she's excluding people."

Guidance for reviewers:
• Hateful exclusion: insulting, stereotyping or dehumanising people based on race, ethnicity, national origin, religion, disability, serious illness, sex, gender identity, sexual orientation or age.
• Harassment: content targeting a specific identifiable person.
• Stating dealbreakers or preferences not tied to a protected characteristic is allowed.
""",
[("hateful exclusion", KC["hateful exclusion"]),
 ("harassment", "content targeting a specific identifiable person."),
 ("explicit sexual content", KC["explicit sexual content"]),
 ("none of these", KC["none of these"])],
"none of these", 1),

# ------------------------------------------------------------------ dt25
Y("dt25", "Is Luca's main photo compliant with PR-2?",
"""
Kindling Photo Rules (PR-2)
The first (main) photo must show the account holder, alone or clearly identifiable. Other photos may include friends or family if the account holder appears in them or the caption makes clear who they are. A main photo that shows only someone other than the account holder is misleading, even if that person consented and even if the bio explains it.

Profile "Luca, 30" — selfie-verified ✓
Photo 1 (main): a man in a suit at a wedding, alone. Caption: none.
Photo 2: the account holder (matches verification selfie) at the same wedding.
Photos 3–5: the account holder hiking and cooking.
Bio: "First pic is my identical twin Marco — I'm the better-looking one in pic 2, obviously. Software tester, amateur chef, sucker for board games."
Verification note: photo 1 does not match the verification selfie (confidence 0.31).
""",
[("Main photo", "the first profile photo, which must show the account holder."),
 ("Misleading main photo", "a main photo showing only someone else, even with consent or an explanation in the bio.")],
0, 2),

# ------------------------------------------------------------------ dt26
C("dt26", "Choose the single Community Standards category that fits Nadia's profile.",
"""
Kindling Community Standards — full-category review (the priority order does not apply to this queue; choose the single category that fits)

Profile "Nadia, 29" — ID verified, selfie-verified
Bio: "Architecture grad, museum nerd, will out-eat you at dim sum. I'm barely on here so text me instead: nine one seven, five five five, zero one nine two. No time-wasters 🙏"
Prompt — "A fact about me": "I've been to 23 countries and lost luggage in 6 of them."
Photos: 5, all match the verification selfie.
Automated scan: no contact-detail patterns detected (digits found: none).
Reporter comment: none (random quality sample).
""",
kc(*KC.keys()),
"contact details", 2),
]
