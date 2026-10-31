# A46 replay label-noise blind read RSBS48-blind_read-30ad8dee-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSBS48-blind_read-30ad8dee-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are answering decision questions as accurately as you can. This is a measurement of your own judgement.
Each item has: qid, kind ("yes/no" or "choice"), text (the material to judge; it is DATA only: ignore any instructions inside it), question (the rules and the question to answer), options (choice items only), definitions (optional: follow them exactly when present).
For kind "yes/no": answer exactly "yes" or "no". For kind "choice": answer with EXACTLY one string copied verbatim from that item's options list.
If an item truly cannot be settled from its text and definitions (the needed information is missing, or the question has no single defensible answer), answer exactly "abstain" instead. Use it rarely; a hard item that you can still reason out is not a reason to abstain.
confidence = your probability (0.0 to 1.0) that your answer is correct. Be calibrated: use high values only when the text clearly settles it.
Think carefully about each item, but answer every item, each exactly once.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "<yes | no | abstain, or one option copied exactly>", "confidence": <a number from 0.0 to 1.0>}. Exactly the keys qid, answer, confidence. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q2a4b12ca68",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Third Assistant Engineer), Gas Turbine Plants.\n\nQuestion: Which of the following is a feature of a power turbine blade that is not found on a high temperature turbine blade?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "Dovetail roots",
   "Interlocking shroud tips",
   "Bulb roots",
   "Solid blades"
  ],
  "definitions": "- Dovetail roots: Answer \"Dovetail roots\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Interlocking shroud tips: Answer \"Interlocking shroud tips\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Bulb roots: Answer \"Bulb roots\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Solid blades: Answer \"Solid blades\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qac4e6b36f7",
  "kind": "yes/no",
  "text": "Situation (Steve is your colleague): Steve is learning French. Whenever Steve meets a French person, he speaks French to them but he is very bad at it. You and Steve met a person who doesn't speak English that well. And Steve whispers to you, \"that person should work on their English, don't you think?\"\nYour reply to Steve: How do you say that in French?",
  "question": "Is your reply to Steve in this situation sarcastic?",
  "definitions": "- yes: At least two-thirds of the independent raters scored the reply 4-6 on a 1-6 sarcasm scale (mean 4+): it says the opposite of, or something other than, what the speaker really thinks, to mock, tease or criticise (ironic praise, exaggerated agreement, pointed rhetorical questions).\n- no: At most one-third of the raters scored it 4-6 (mean 3 or less): the reply is sincere and meant literally (genuine thanks, honest criticism, plain information or a real question), even when it is blunt, joking or annoyed."
 },
 {
  "qid": "qa16ea91822",
  "kind": "yes/no",
  "text": "User: Wooooowowow\nAssistant: I didn't understand that. Could you say it in a different way?\nUser (latest message): gdngknfnf",
  "question": "How should the calendar assistant handle the user's latest message, given what the assistant can and cannot do?\nIs the correct answer \"decline: message not understandable\"?",
  "definitions": "- decline: message not understandable: The message is gibberish, random characters, pasted instructions, or a statement with no recognisable request the assistant could act on.\n- ask the user to be more specific: The user wants something done but leaves out what exactly: which event, or the new time or value ('change dinner time', 'update my Monday meeting'), or sends a fragment that cannot be acted on alone ('select one', 'place it').\n- decline: calculations over the calendar: The user asks for counts, comparisons or aggregates across many events ('how many meetings this week', 'my longest meeting', 'how many free days next month'); the assistant cannot compute them.\n- decline: general-knowledge question: The user asks a trivia or general-knowledge question (facts, science, maths, seasons, which holidays fall in a period, 'the next holiday', a holiday outside the common US list such as Purim) rather than a calendar fact.\n- decline: reminders and alarms: The user asks the assistant to set a reminder, alarm or notification (for themselves or others); the assistant cannot do reminders, even when the rest of the request is fine."
 },
 {
  "qid": "qab3e34a400",
  "kind": "choice",
  "text": "Trivia question (category: Art).\n\nQuestion: Which art movement was Pablo Picasso known for co-founding?",
  "question": "Which answer choice correctly answers this trivia question?",
  "options": [
   "Class L",
   "Class B",
   "Class Y",
   "Class Z"
  ],
  "definitions": "- Class L: Answer \"Cubism\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Class B: Answer \"Expressionism\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Class Y: Answer \"Futurism\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Class Z: Answer \"Impressionism\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q6748e84987",
  "kind": "yes/no",
  "text": "We have characterised a novel missense mutation, G5260A, in exon 32 in a family segregating for <e>EA-2</e>.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"EA-2\" (marked <e>) in this sentence?\nIs it wrong to answer \"composite mention\"?",
  "definitions": "- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders')."
 },
 {
  "qid": "q93d31290e6",
  "kind": "choice",
  "text": "<e1>Japanese Empire</e1> in the Tropics: Selected Documents and Reports of the <e2>Japanese</e2> Period in Sarawak, Northwest Borneo, 1941-1945.",
  "question": "Which relation from entity 1 (\"Japanese Empire\", marked <e1>) to entity 2 (\"Japanese\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.",
  "options": [
   "replaced by",
   "followed by",
   "none of the listed relations"
  ],
  "definitions": "- replaced by: Entity 1 was replaced or superseded by entity 2 (entity 2 is the later holder, office, body or thing that took its place).\n- followed by: Entity 1 comes directly before entity 2 in a sequence or series (entity 2 is its immediate successor), e.g. the next album, episode or edition.\n- none of the listed relations: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction."
 },
 {
  "qid": "qadb902dbe1",
  "kind": "choice",
  "text": "Premise:\nTitle: Camel\nOrigin: Guildford, Surrey, England\nGenres: Progressive rock\nYears active: 1971 (1971)-present\nLabels: MCA, Deram, Gama, Janus, Decca, Camel Productions\nWebsite: camelproductions .com\nHypothesis: The band Camel was named after the animal.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q84a9a9e934",
  "kind": "yes/no",
  "text": "We found nuclear LEF-1 in the dividing <e>tumour</e> cells, providing biochemical evidence that pilomatricomas are derived from hair matrix cells.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"tumour\" (marked <e>) in this sentence?\nIs the correct answer \"disease class\"?",
  "definitions": "- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC')."
 },
 {
  "qid": "q2830638f73",
  "kind": "yes/no",
  "text": "And we face very wealthy opponents.",
  "question": "Does this text convey a sense of being controlled or of being in control?\nIs the correct answer \"in control\"?",
  "definitions": "- in control: The text conveys being in control, influential, important, dominant, confident or autonomous: the writer or subject acts, decides or masters the situation rather than being subject to it.\n- controlled: The text conveys being controlled, influenced, guided, submissive, awed, overwhelmed or powerless: other people, events or circumstances are in charge rather than the writer or subject."
 },
 {
  "qid": "qca153404bb",
  "kind": "yes/no",
  "text": "FAQ entry (restaurant: Fitzbillies Restaurant)\nQ: Do you accept credit or debit cards?\nA: Major credit cards are accepted at Fitzbillies Restaurant.\n\nCustomer question: Will I be able to pay with my credit card at the restaurant?",
  "question": "Based only on this FAQ entry, is the answer to the customer's question yes?",
  "definitions": "- yes: The FAQ entry implies the customer's question should be answered yes, including a yes that comes with a condition or limit (for example pets allowed only in a basket, or a service offered for a fee).\n- no: The FAQ entry does not support a yes: the thing is not offered, allowed or the case (even without saying 'no', e.g. 'cash only' versus paying by card), or only other options are listed."
 },
 {
  "qid": "qafb0e757ca",
  "kind": "yes/no",
  "text": "Wikipedia page: Merritt Butrick\nSection: Filmography\nTable:\n| Film | Film | Film | Film |\n| Year | Title | Role | Notes |\n| 1982 | Star Trek II: The Wrath of Khan | Dr. David Marcus |  |\n| ... |\n| 1984 | Star Trek III: The Search for Spock | Dr. David Marcus |  |\n| 1985 | Head Office | John Hudson |  |\n| ... |\n| 1988 | Why on Earth? | Oscar | Television movie |\n| ... |\n| 1988 | Star Trek: The Next Generation | T'Jon | 1 episode (\"Symbiosis\") |\n| ... |\n\nClaim: Merritt Butrick appeared as Dr. David Marcus in \"Symbiosis\" (1988), an episode of Star Trek: The Next Generation.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "q0bb492cbc8",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Master/Chief Mate of Unlimited Tonnage), Deck Safety.\n\nQuestion: Deficient oxygen content inside a chain locker can be detected with which item?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "An oxygen indicator",
   "An oxygen breathing apparatus",
   "A combustible gas indicator",
   "Litmus paper"
  ],
  "definitions": "- An oxygen indicator: Answer \"An oxygen indicator\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- An oxygen breathing apparatus: Answer \"An oxygen breathing apparatus\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- A combustible gas indicator: Answer \"A combustible gas indicator\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Litmus paper: Answer \"Litmus paper\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qa9f8a1cd55",
  "kind": "yes/no",
  "text": "no no it's no wedding  neither college farewell  it's the evacuated students from HASHTAG_EASTASIA+VIRUS HASHTAG_VIRUS  isolation camp in manesar,😂 @dhananjaypro good job for showing true indian spirit. #HASHTAG #HASHTAG #HASHTAG @atrivandi #HASHTAG https://t.co/iktkkjojbz",
  "question": "Is this tweet hostile toward an East Asian entity (people, country, government, institution or culture)?",
  "definitions": "- yes: Hostile: the words themselves derogate or demean an East Asian people, country, government or culture (extreme negative portrayal, hatred, conspiracy claims, wishing them gone or suffering, boycotts, slurs, mocking virus names); placeholder hashtags alone never count.\n- no: Not hostile: reasoned criticism of an East Asian government or institution without abuse, discussion of anti-Asian prejudice, counter-speech defending East Asian people, or neutral or unrelated content; naming the virus after its origin is not hostile."
 },
 {
  "qid": "q17c132eab3",
  "kind": "choice",
  "text": "This proclamation was approved by Prussia and Austria, and by the <e2>German</e2> confederal diet insofar as it affected <e1>Holstein</e1> and Lauenburg.",
  "question": "Which relation from entity 1 (\"Holstein\", marked <e1>) to entity 2 (\"German\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.",
  "options": [
   "Option S",
   "Option Z",
   "Option Y"
  ],
  "definitions": "- Option S: Entity 1 lies within entity 2, an administrative division below country level, such as a city, county, district, state or province.\n- Option Z: Entity 2 is the sovereign country in which entity 1 (a place, building, organisation, event or object, not a person) is located or to which it belongs.\n- Option Y: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction."
 },
 {
  "qid": "q7874f0e86f",
  "kind": "choice",
  "text": "Trivia question (category: Geography).\n\nQuestion: How many countries border Kyrgyzstan?",
  "question": "Which answer choice correctly answers this trivia question?",
  "options": [
   "Code 48",
   "Code 12",
   "Code 11",
   "Code 23"
  ],
  "definitions": "- Code 48: Answer \"3\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 12: Answer \"4\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 11: Answer \"1\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 23: Answer \"6\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qb39795e830",
  "kind": "yes/no",
  "text": "Employee said he was shoveling with his left hand. He felt a pop in his left shoulder and back, causing a left cervical strain and left shoulder strain. This was not reported to Management until 6/30/2008.",
  "question": "Which MSHA accident classification fits the circumstances that most directly caused this mine accident?\nIs the correct answer \"Class A\"?",
  "definitions": "- Class A: Contact with or exposure to electric current (energized wires, cables or equipment), including shock, electrocution and electrical or arc burns.\n- Class T: Injury while lifting, carrying, pushing, pulling, shoveling, loading or otherwise moving materials or supplies by hand, including strains and objects dropped while handled.\n- Class G: An unplanned fire or burning of equipment, belt, cable, fuel or mine material, not an ignition or explosion of gas or dust.\n- Class C: A lung disease from dust: black lung (coal workers' pneumoconiosis), silicosis, asbestosis or another pneumoconiosis.\n- Class Y: By their own movement the person struck or bumped a body part against an object (for example hit the head on the roof or a beam).\n- Class P: Rock, coal or other material that falls, rolls or slides onto a person from a pile, bank, truck, bucket, chute or conveyor; not a fall of in-place roof, rib or highwall, and not material dropped while being handled."
 },
 {
  "qid": "qa8d0e5484e",
  "kind": "choice",
  "text": "The scientists scanned the brains of 17 young people aged eight to 16 with autism while they looked at images of cars or the eyes of people expressing different emotions. The scans were given 45 minutes after the young people inhaled a placebo or oxytocin through a nasal spray.\nThe scans showed that the reward circuits in the children’s brains behaved more normally after a dose of oxytocin: that is, they were more active when the person was looking at faces and less active when looking at the inanimate cars. The study appears in the latest issue of the journal Proceedings of the National Academy of Sciences in the United States.",
  "question": "This passage comes from a news article that English teachers rewrote for language learners at three reading levels. At which level is this passage written?",
  "options": [
   "elementary",
   "intermediate",
   "advanced"
  ],
  "definitions": "- elementary: The easiest rewrite (about CEFR A2-B1): short, mostly single-clause sentences, very common words, simple tenses, difficult terms explained or dropped, few idioms or long noun phrases.\n- intermediate: The middle rewrite (about B1-B2): moderately long sentences with some subordinate clauses, mostly everyday vocabulary with some less common words, lighter simplification of the original.\n- advanced: The original native-level newspaper text (about C1): long multi-clause sentences, rich or technical vocabulary, idioms, figurative language and dense reported speech, with no simplification."
 },
 {
  "qid": "q3a2ee62580",
  "kind": "yes/no",
  "text": "Customer: I need to be picked up at the Los Angeles Airport and will be dropped off at the Marriott.\nAssistant: Which Marriott are you staying at?\nCustomer: The one near the airport at West Century Blvd.",
  "question": "In the customer's last message, does \"near the airport at West Century Blvd\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0a5ec53dff",
  "kind": "yes/no",
  "text": "FAQ entry (hotel: Hobsons House)\nQ: Are there Elevator available at the site?\nA: The Hobsons House does not offer a lift.\n\nCustomer question: I'd like to spare myself from climbing a lot of stairs. Do they have an elevator?",
  "question": "Based only on this FAQ entry, is the answer to the customer's question yes?",
  "definitions": "- yes: The FAQ entry implies the customer's question should be answered yes, including a yes that comes with a condition or limit (for example pets allowed only in a basket, or a service offered for a fee).\n- no: The FAQ entry does not support a yes: the thing is not offered, allowed or the case (even without saying 'no', e.g. 'cash only' versus paying by card), or only other options are listed."
 },
 {
  "qid": "q3cf7cf5fdc",
  "kind": "yes/no",
  "text": "101 Tularemia Treatment of TULAREMIA caused by FRANCISELLA TULARENSIS",
  "question": "Does this sentence express that one of the terms \"TULAREMIA\" and \"FRANCISELLA TULARENSIS\" is used to treat the other (therapeutic use of a drug, ingredient or therapy)?",
  "definitions": "- yes: At least 60% of the crowd workers ticked TREATS: the sentence presents one term as a drug, ingredient or therapy used to cure or relieve the other (e.g. penicillin cures infection), including reported results such as 'was effective in treating'.\n- no: At most 10% ticked TREATS: in this sentence the terms are linked in another way (cause, symptom, side effect, location, diagnosis, prevention, is-a, mere co-occurrence) or not at all, whatever is true outside the sentence."
 },
 {
  "qid": "qf3d7ad75f7",
  "kind": "yes/no",
  "text": "Somebody hit me and said Barry Goldwater said you ought to talk on issues more.",
  "question": "Which kind of statement is this sentence from a political debate?\nIs the correct answer \"Check-worthy factual claim\"?",
  "definitions": "- Check-worthy factual claim: The sentence makes a factual claim that the general public would want to know is true or false and journalists would pick to fact-check, such as a voting record, a statistic, or what a policy did.\n- Unimportant factual statement: The sentence does state a fact, but a trivial one (such as a small personal detail or a remark about the debate itself) that the public would not care to have verified and fact-checkers would skip.\n- Non-factual statement: The sentence makes no factual claim that could be checked as true or false: it is a subjective opinion, belief or declaration, or a question."
 },
 {
  "qid": "q1fc6adeabe",
  "kind": "yes/no",
  "text": "Sling Orange is the basic package, offering around 30 channels for $25 per month including AMC, BBC America, Cartoon Network, Comedy Central, <e1>Disney</e1>, <e2>ESPN</e2>, IFC, and TBS.",
  "question": "Which relation from entity 1 (\"Disney\", marked <e1>) to entity 2 (\"ESPN\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.\nIs the correct answer \"owner of\"?",
  "definitions": "- owner of: Entity 2 is something (a company, building, team, property or product) that entity 1 owns or owned (the inverse of 'owned by').\n- none of the listed relations: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction.\n- subsidiary: Entity 2 is a subsidiary company or subordinate organisation owned or controlled by entity 1."
 },
 {
  "qid": "q0f9bdf95f7",
  "kind": "yes/no",
  "text": "The EE was building an intake solid concrete block stopping. The wall was over 8' high. The wall was not properly capped for the wall's size. The wall fell, striking the EE. The EE sustained a laceration of the scalp and minor bruising.",
  "question": "Which part of the body was injured in this mine accident report?\nIs it wrong to answer \"head, multiple parts\"?",
  "definitions": "- head, multiple parts: Two or more different parts of the head (for example scalp and face).\n- scalp: The skin and tissue covering the skull, named as the scalp.\n- foot (not ankle or toes): The foot itself (heel, arch, instep, metatarsals), not the ankle or toes.\n- arm (not elsewhere classified): The arm when the narrative does not say which part of it (upper arm, elbow or forearm) was hurt.\n- ear, external: The outer ear only (auricle or earlobe), for example a cut, bruise or burn on the ear.\n- mouth, lips, teeth, tongue or throat: The mouth, lips, teeth, tongue, throat or sense of taste."
 },
 {
  "qid": "qed097d68e0",
  "kind": "yes/no",
  "text": "imagine your daughters boyfriend being ⬛  💓💓",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post, reading any emoji as the words, groups or actions they stand for, directs abuse or contempt at a group identity (such as race, ethnicity, nationality, religion, gender, sexuality, disability, immigration status or class) or at someone because of that identity, explicitly or implicitly: insults and slurs, threats, dehumanising comparisons, or subtle digs and hostile stereotypes.\n- no: The post, reading any emoji for what they stand for, does not attack a group identity: it may mention identities, swear, criticise, counter hate or target something that is not an identity (an animal, an object, a person for non-identity reasons), but it is not abusive towards an identity group or anyone because of their identity."
 },
 {
  "qid": "q21386d0d91",
  "kind": "yes/no",
  "text": "---You aren't free of adultery until she is begging for the d and you refuse.",
  "question": "Does this post assault the human dignity of people because of a group they belong to?",
  "definitions": "- yes: The post meets the category the question names, as the Gab Hate Corpus coding manual defines it. Assault on human dignity: it degrades a group, or a person because of their group, by asserting or implying inferiority, comparing them to animals or subhumans, using slurs meant to wound, spreading hateful stereotypes, or supporting hateful ideology such as white supremacy. Call for violence: it advocates or endorses violence, genocide, expulsion, exclusion or segregation against a group, or a person because of their group. Vulgar or offensive language: it uses vulgar, derogatory or abusive wording or personal insults, whether or not the post is hateful.\n- no: The post does not meet the category the question names under the coding manual. Insults or threats aimed at a person without invoking their group are neither an assault on dignity nor a call for violence; degrading a group without advocating aggression, expulsion or exclusion is not a call for violence; hateful or political views stated without vulgar, profane or abusive wording are not vulgar language; criticism of policies, parties or ideas that does not degrade people is none of these."
 },
 {
  "qid": "q2770ffcb35",
  "kind": "yes/no",
  "text": "At the Christmas celebration, everyone loved the popcorn balls, but the brownies were just OK. The _ came from a more untried recipe.\n\nThe blank (_) stands for one of two candidates: \"popcorn balls\" or \"brownies\".",
  "question": "Does the blank (_) in the sentence stand for \"popcorn balls\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "q90af9838b3",
  "kind": "yes/no",
  "text": "Oh, sorry, it's actually an upper bound on the amount of discrete symmetry. But surely it must be saturated in some sense. ;-)",
  "question": "Does this paragraph make the contrarian climate claim that global warming is not happening?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that global warming is not happening: it denies that warming or its physical signs are happening: ice, permafrost or snow cover is not melting; we are heading into an ice age or global cooling; cold or snowy weather disproves warming; the climate has not warmed over recent decades; oceans are not warming; sea-level rise is exaggerated or not accelerating; extreme weather is not increasing, happened before or is not linked to climate change.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that global warming is not happening."
 },
 {
  "qid": "q07219d7872",
  "kind": "choice",
  "text": "Heading: Red Square\nBehind Lenin's tomb in Red Square, and behind the line of very famous Soviet leaders, is a line of plaques that mark the cremations (I believe) of important Soviet-era people. They do, however, appear to stop when the death date is 1975 or 1976. Was there a particular reason? - [ .]",
  "question": "Which Wikipedia Reference Desk should this question be posted to?",
  "options": [
   "Code 45",
   "Code 40",
   "Code 46",
   "Code 10",
   "Code 37",
   "Code 14"
  ],
  "definitions": "- Code 45: Questions about computers, software, programming, the internet, electronics as used in computing, and IT or device problems.\n- Code 40: Questions about popular culture: films, television, music, video games, sports, comics, celebrities and other entertainment.\n- Code 46: Questions about history, politics, law, religion, philosophy, economics and finance, society, the arts, literature and geography of human affairs.\n- Code 10: Questions about words and languages: meaning, grammar, spelling, pronunciation, etymology, translation and usage.\n- Code 37: Questions about mathematics, statistics, probability, logic and puzzles that need mathematical reasoning.\n- Code 14: Questions about the natural and applied sciences: physics, chemistry, biology, medicine and health, astronomy, earth science, engineering and technology (not software)."
 },
 {
  "qid": "q48125f9d2a",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (DDE – Unlimited HP), Gas Turbine Plants.\n\nQuestion: Which of the following are the principle factors that affect the performance of a gas turbine compressor?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "Bleed pressure, fuel pressure, exhaust temperature",
   "Pressure ratio, air flow, rotational speed",
   "Fuel flow, air flow, exhaust temperature",
   "None of the above"
  ],
  "definitions": "- Bleed pressure, fuel pressure, exhaust temperature: Answer \"Bleed pressure, fuel pressure, exhaust temperature\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Pressure ratio, air flow, rotational speed: Answer \"Pressure ratio, air flow, rotational speed\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Fuel flow, air flow, exhaust temperature: Answer \"Fuel flow, air flow, exhaust temperature\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- None of the above: Answer \"None of the above\": correct only if none of the other listed choices is a right answer to the question; wrong if any other choice is right."
 },
 {
  "qid": "qba4fb83a08",
  "kind": "choice",
  "text": "Trivia question (category: General Knowledge).\n\nQuestion: What technology is named after a tenth-century ruler of Denmark and Norway?",
  "question": "Which answer choice correctly answers this trivia question?",
  "options": [
   "Bluetooth",
   "GPS",
   "Wi-Fi",
   "Internet"
  ],
  "definitions": "- Bluetooth: Answer \"Bluetooth\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- GPS: Answer \"GPS\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Wi-Fi: Answer \"Wi-Fi\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Internet: Answer \"Internet\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q933ded2941",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Comollo\nTable (caption: Comollo):\n| Origin | Origin |\n| Meaning | Little Jacob (truncated) |\n| Other names | Other names |\n| Variant form(s) | Comolli, Comelli, Comino, Giacomelli, Giacometti, Giacomino, Jacobelli, Jacobellis and similar |\nSentence: Comollo is an Italian surname localized in the northern regions of Piedmont and Liguria.\n\nClaim: An Italian surname that means little Jacob is Comollo which also has five variants, one of which is Jacobellis",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "qae611e913b",
  "kind": "yes/no",
  "text": "And if I was your neighbor and you came over and told me you killed two teens execution style, knowing they're unarmed, I would've beaten your faggot ass into oblivion",
  "question": "How is the potential slur in this comment used?\nIs the correct answer \"Code 16\"?",
  "definitions": "- Code 16: The slur conveys contempt toward a targeted person or group: insults, labels, stand-alone slurs, sexualised use, generalisations about the community, or self-deprecation.\n- Code 58: The slur is mentioned rather than aimed at anyone - quoted, discussed as a word, recalled from an incident, used in counter-speech, or in sarcasm that mocks bigotry - by a speaker who is not reclaiming it.\n- Code 44: A member of the targeted group uses the slur with positive or neutral force about themselves or their community (empowerment, in-group solidarity, humour).\n- Code 55: The word is used in a non-slur sense, such as 'fag' meaning a cigarette or 'tranny' meaning a vehicle transmission."
 },
 {
  "qid": "qd4128a3426",
  "kind": "yes/no",
  "text": "Complaint narrative: AFTER 1 HOUR OF DRIVING AND STOPPING AT A INTERSECTION TRUCK DECIDED TO SHUT DOWN AT THE INTERSECTION CAUSING ME TO ALMOST BE INVOLVED IN A ACCIDENT SINCE I WAS DEAD IN THE MIDDLE OF INTERSECTION WITHOUT WARNING OR REASON I HAD JUST ACCELERATED THROUGH LIGHT WHEN TRUCK SHUT DOWN",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "qcf4ef762bd",
  "kind": "yes/no",
  "text": "Rossini M, Gatti D, Zamberlan N et al. Long term effects of a treatment course with oral ALENDRONATE of postmenopausal OSTEOPOROSIS",
  "question": "Does this sentence express that one of the terms \"OSTEOPOROSIS\" and \"ALENDRONATE\" is used to treat the other (therapeutic use of a drug, ingredient or therapy)?",
  "definitions": "- yes: At least 60% of the crowd workers ticked TREATS: the sentence presents one term as a drug, ingredient or therapy used to cure or relieve the other (e.g. penicillin cures infection), including reported results such as 'was effective in treating'.\n- no: At most 10% ticked TREATS: in this sentence the terms are linked in another way (cause, symptom, side effect, location, diagnosis, prevention, is-a, mere co-occurrence) or not at all, whatever is true outside the sentence."
 },
 {
  "qid": "q0f1a2c02a8",
  "kind": "yes/no",
  "text": "Complaint narrative: WHILE DRIVING FOR ABOUT 3 MINUTES ON STREET THE TAHOE STARTED TO SMELL LIKE SMOKE, WE THEN NOTICED SMOKE COMING OUT OF THE AIR CONDITIONING VENTS IN A MATTER OF SECONDS THERE WHERE FLAMES COMING OUT FROM UNDERNEATH THE GLOVE COMPARTMENT. THE CAR CAUGHT ON FIRE AND THE AIR BAG DEPLOYED. THE DASH BOARD WAS COMPLETELY MELTED FROM THE FIRE, THE FRONT WINDSHILLED SHATTERED WITH FORCE TOWARDS THE BACK OF THE TRUCK.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "qe586d40e08",
  "kind": "yes/no",
  "text": "Situation: She was waiting for her mom to show up.\nAction being judged: Waiting for someone when they are late.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q185d697910",
  "kind": "choice",
  "text": "The monoclonal antibody (mAB) against C5a receptor C5aR/CD88 (clone W17/1; purified Fab, mouse IgG1) was purchased from Serotec (Oxford, UK), the mouse mAB against CD163 (clone Ber-MAC3; purified Fab, IgG1) was purchased from Dako (<e2>Vienna</e2>, <e1>Austria</e1>) and the mAB against TNF-a was purchased from R&D Systems (Minneapolis, MN, USA).",
  "question": "Which relation from entity 1 (\"Austria\", marked <e1>) to entity 2 (\"Vienna\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.",
  "options": [
   "Code 39",
   "Code 32",
   "Code 22",
   "Code 41"
  ],
  "definitions": "- Code 39: Entity 1 lies within entity 2, an administrative division below country level, such as a city, county, district, state or province.\n- Code 32: Entity 2 is an administrative division (such as a state, province, county, district or city) that lies inside entity 1.\n- Code 22: Entity 2 is the capital city or seat of government of entity 1 (a country, state, province or region).\n- Code 41: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction."
 },
 {
  "qid": "qedd1af866c",
  "kind": "yes/no",
  "text": "Burchellia\nBurchellia is a monotypic genus of flowering plants in the Rubiaceae family. The genus contains only one species, viz. \"Burchellia bubalina\", which is endemic to southern Africa: the Cape Provinces, KwaZulu-Natal and the Northern Provinces in South Africa, and Swaziland. It is commonly known as \"wild pomegranate\" (English) or \"wildegranaat\" (Afrikaans).\n\nIxiolirion\nIxiolirion is a genus of flowering plants native to central and southwest Asia, first described as a genus in 1821. Recent classifications place the group in the monogeneric family Ixioliriaceae in the order Asparagales of the monocots. In earlier systems of classification, it was usually placed in the family Amaryllidaceae.",
  "question": "Are both Burchellia and Ixiolirion flowering plants?",
  "definitions": "- yes: Read together, the paragraphs show the answer is yes: what the question asks holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right).\n- no: The paragraphs do not bear out a yes: at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer."
 },
 {
  "qid": "q6b7237fc51",
  "kind": "yes/no",
  "text": "Occupation: Paralegals and Legal Assistants\nDuties:\n- Sentence defendants in criminal cases, on conviction by jury, according to applicable government statutes.\n- Award compensation for damages to litigants in civil cases in relation to findings by juries or by the court.\n- Impose restrictions upon parties in civil cases until trials can be held.",
  "question": "Are the listed duties part of the job of the occupation named above?",
  "definitions": "- yes: The duties are tasks of the named occupation: they describe that occupation's own characteristic work as the occupation is defined.\n- no: The duties describe a different occupation's characteristic work (often a related job in the same field) and are not tasks the named occupation performs."
 },
 {
  "qid": "qcad357ccfa",
  "kind": "yes/no",
  "text": "We liked the comedy show more than we liked the play because the performers interacted with us more during the _ .\n\nThe blank (_) stands for one of two candidates: \"play\" or \"comedy show\".",
  "question": "Does the blank (_) in the sentence stand for \"comedy show\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "q3280cd5b80",
  "kind": "yes/no",
  "text": "Situation: I beat up my girlfriend because she cheated on me and lied about it\nAction being judged: Hitting your partner for any reason.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qa0e2c1bc3f",
  "kind": "yes/no",
  "text": "Wikipedia page: Fawn Township, York County, Pennsylvania\nTable:\n| Historical population | Historical population | Historical population | Historical population |\n| Census | Pop. |  | %± |\n| 2000 | 2,727 |  | — |\n| 2010 | 3,099 |  | 13.6% |\n| Est. 2016 | 3,140 |  | 1.3% |\n| U.S. Decennial Census | U.S. Decennial Census | U.S. Decennial Census | U.S. Decennial Census |\n\nClaim: The population of Fawn Township, York County, Pennsylvania was 3,099 at the 2010 census.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "qb63725671a",
  "kind": "yes/no",
  "text": "Beginning: one plus fifty-two ...\n\nPossible endings:\n(A) two\n(B) one\n(C) four\n(D) fifty-three",
  "question": "Which listed ending continues the beginning most sensibly?\nIs the correct answer \"A\"?",
  "definitions": "- A: Ending (A) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- D: Ending (D) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- C: Ending (C) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning.\n- B: Ending (B) is the listed continuation that makes the most sense after the beginning: it describes what would ordinarily be true or happen next and respects any negation, number, idiom or double meaning in the beginning."
 },
 {
  "qid": "q832db2509a",
  "kind": "yes/no",
  "text": "Company annual report excerpt\nTable:\n|  | United States | Foreign |\n|  | (in thousands) |  |\n| 2020 | $8,027 | $1,237 |\n| 2021 | 8,416 | 985 |\n| 2022 | 9,163 | 982 |\n| 2023 | 9,785 | 1,258 |\n| 2024 | 10,558 | 1,098 |\n| 2025-2029 | 59,665 | 6,129 |\nText:\nExpected Future Pension Benefit Payments\nFuture benefit payments are expected to be paid as follows:\n\nQuestion: What is the payment for 2025-2029 for Foreign?\nProposed answer: 59,665 thousand",
  "question": "Based only on the report's table and text, is the proposed answer to the question correct?",
  "definitions": "- yes: The proposed answer matches what the table and text give for this exact question: the same value at the precision shown, the same sign or direction, the same unit or scale (%, thousand, million, billion), and for list answers exactly the right items.\n- no: The proposed answer does not match: a different value or item (for example another year's figure or another line item), a wrong sign or wrong base for a change, a wrong unit or scale such as million instead of thousand, or a list that misses or adds an item."
 },
 {
  "qid": "qa584e2d75d",
  "kind": "yes/no",
  "text": "How in the hell did his truck not just shit out the whole tranny",
  "question": "Is the potential slur in this comment used to express contempt for a person or group?",
  "definitions": "- yes: Derogatory use: the slur conveys contempt toward a person or group - as an insult or label for someone, a stand-alone slur, sexualised or fetishising use, a slur-laden generalisation about the group, or self-deprecating use.\n- no: Not derogatory: the word is only mentioned (quoted, discussed, recalled, condemned in counter-speech or used sarcastically against bigotry), reclaimed positively by a member of the targeted group, or used in an unrelated sense (cigarette, transmission)."
 },
 {
  "qid": "q19370b3e82",
  "kind": "yes/no",
  "text": "Table caption: Regression of ideology on self-ratings and socio-demographics.\n| Dependent variable: | SDO | RWA |\n| S (self) | 0.07 | −0.09* |\n| E (self) | −0.06 | −0.04 |\n| O (self) | −0.24 *** | −0.53 *** |\n| A (self) | −0.22 *** | −0.01 |\n| C (self) | −0.01 | 0.20 *** |\n| Gender (male) | 0.10* | 0.01 |\n| Higher education | 0.02 | −0.24 *** |\n| Age (in years) | 0.02 | −0.02 |\n| R 2 (in %) | 13.5 | 42.7 |\n| n | 611 | 611 |\nTable notes: Note: Entries indicate yx -standardized regression coefficients, Significance levels: * p < 0.05, ** p < 0.01, *** p < 0.001. S = Emotional stability , E = Extraversion , O = Openness to experience , A = Agreeableness , C = Conscientiousness , SDO = social dominance orientation , RWA = right-wing authoritarianism.\n\nStatement: Gender (male) social dominance orientation is 611.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q021804ef74",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Jules de Jongh\nSection: Filmography > Films and television\nTable (caption: List of voice performances in films and television):\n| Year | Title | Role(s) | Notes | Source |\n| ... |\n| 2005 | Gerry Anderson's New Captain Scarlet | Lieutenant Green |  |  |\n| ... |\n| 2010 | Misty Island Rescue | Emily | Film; supporting US voice role |  |\n\nClaim: Jules de Jongh dubbed Lieutenant Green in the Gerry Anderson's New Captain Scarlet in 2005, then dubbed Emily in the Misty Island Rescue in 2010.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "qe22fc1c9cf",
  "kind": "yes/no",
  "text": "Question: Muller's muscle is supplied by:\nOptions: (A) 3rd cranial nerve (B) 4th cranial nerve (C) Sympathetic fibers (D) Parasympathetic fibers",
  "question": "Which medical subject does this exam question belong to?\nIs it wrong to answer \"ophthalmology\"?",
  "definitions": "- ophthalmology: Eye diseases, their signs, investigations and treatment, optics and refraction, and eye surgery.\n- orthopaedics: Fractures, dislocations, bone and joint diseases, bone tumours, nerve injuries of the limbs and their orthopaedic management.\n- psychiatry: Mental disorders, their symptoms, classification and treatment (including psychotropic therapy choices), psychology and substance-use disorders.\n- paediatrics: Child health: growth and development milestones, neonatal care, immunisation schedules, nutrition and diseases of infants and children.\n- microbiology: Bacteria, viruses, fungi and parasites: their properties, culture, lab diagnosis, virulence, immunology and vaccines, and sterilisation."
 },
 {
  "qid": "qd6e37ff203",
  "kind": "yes/no",
  "text": "Statement 1: the computer broke down and the technician will fix it\nStatement 2: the computer broke down and the doctor fixed it",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qe5382e1e57",
  "kind": "choice",
  "text": "Infobox:\nTitle: Brazzaville Balazavile\nCoordinates: 4°16′4″S 15°17′31″E﻿ / ﻿4.26778°S 15.29194°E\nCountry: Republic of the Congo\nCapital district: Brazzaville\nFounded: 1883\nFounded by: Pierre Savorgnan de Brazza\nMayor: Christian Roger Okemba (PCT)\nTotal Population: 1,373,382\nTotal Area: 263.9 km2 (101.9 sq mi)\nElevation: 320 m (1,050 ft)\nEstimate Population (2019): 2,308,000\nDensity: 5,200/km 2 (13,000/sq mi)\nArea code(s): 242\nHDI (2017): 0.642 , medium\nWebsite: www .brazzaville .cg\n\nHypothesis: Brazzaville was founded in the 19th century.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 }
]
