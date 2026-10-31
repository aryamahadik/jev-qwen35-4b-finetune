# A46 replay label-noise blind read RSAS47-blind_read-adc6530c-004

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSAS47-blind_read-adc6530c-004.json

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
  "qid": "qaa31274351",
  "kind": "choice",
  "text": "FCC amateur radio licence exam: General class (Element 3) question pool 2023-2027.\nSubelement: Radio wave propagation.\n\nQuestion: What happens to HF propagation when the LUF exceeds the MUF?",
  "question": "Which answer choice is correct for this FCC amateur radio licence exam question?",
  "options": [
   "Code 15",
   "Code 53",
   "Code 49",
   "Code 10"
  ],
  "definitions": "- Code 15: Answer \"Propagation via ordinary skywave communications is not possible over that path\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 53: Answer \"HF communications over the path are enhanced\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 49: Answer \"Double-hop propagation along the path is more common\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 10: Answer \"Propagation over the path on all HF frequencies is enhanced\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qb1275d053f",
  "kind": "yes/no",
  "text": "you are either 🔝 or ⬇️ not in between",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "qb1b032bae6",
  "kind": "yes/no",
  "text": "Certainly, Moore is one of the most talented filmmakers in the United States today, and his film fully deserved its Oscar.",
  "question": "Is the feeling conveyed by this text negative or positive?\nIs it wrong to answer \"positive\"?",
  "definitions": "- positive: The text expresses, or makes a reader feel, a pleasant emotion such as happiness, joy, hope, gratitude, pride or satisfaction; judge the feeling, not whether the topic is important or the facts are good news for someone.\n- negative: The text expresses, or makes a reader feel, an unpleasant emotion such as sadness, fear, anger, disgust, annoyance or disappointment; judge the feeling, not whether the topic is important or the facts are good news for someone."
 },
 {
  "qid": "qb46cbf8efd",
  "kind": "yes/no",
  "text": "Someone posted that a particular thing happened.",
  "question": "Does this sentence imply that the particular thing did not happen?",
  "definitions": "- yes: At least 6 of 10 annotators (and at most 1 saying the opposite) answered that it did NOT happen (the person did not do or have it): the sentence commits the speaker to non-occurrence, as with 'neglected to', 'refused to' or 'didn't manage to'.\n- no: At most 1 of 10 annotators answered that it did not happen; the others judged that it did happen (as after 'didn't forget to', 'was glad that') or that it might or might not have (as after 'wanted', 'wasn't told to')."
 },
 {
  "qid": "q134ba06d6a",
  "kind": "yes/no",
  "text": "\"Immelt said that a carbon pricing scheme would create jobs Doesn't sound like it, if he has in mind a cap-and-tax scheme. (Here's also a useful primer on costs of global warming policies.)\"",
  "question": "Does this paragraph make the contrarian climate claim that climate solutions won't work?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate solutions won't work: it argues against climate solutions: climate policies (carbon taxes, cap-and-trade, treaties such as Kyoto or Paris, regulations) are harmful to the economy, jobs or the poor, or are ineffective or flawed; clean energy technology or biofuels cannot work; people need fossil-fuel (or nuclear) energy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate solutions won't work."
 },
 {
  "qid": "qa199e5ad39",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: Camp\nReleased: November 15, 2011 (2011-11-15)\nStudio: Hyperion Sound, Los Angeles, CA\nGenre: Hip hop\nLength: 56:06\nLabel: Glassnote\nProducer: Childish Gambino, Ludwig Göransson\n\nHypothesis: Childish Gambino was a producer of Camp in early 2011.",
  "question": "Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis definitely false?",
  "definitions": "- yes: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- no: The hypothesis is not shown to be false: either the infobox confirms it, or it concerns details the infobox does not cover, so it may or may not be true."
 },
 {
  "qid": "q1d4fbd0b65",
  "kind": "choice",
  "text": "Tweet: @anonymous definitely put the biggest smile on my face to read that :) YOU'RE amazing!! &lt;33",
  "question": "How positive or negative is the sentiment this text expresses, as a typical reader would rate its intensity?",
  "options": [
   "Class B",
   "Class H",
   "Class F",
   "Class P",
   "Class C"
  ],
  "definitions": "- Class B: Strongly or extremely negative (rated -3 or -4 on a -4..+4 scale): intense anger, disgust, despair, harsh criticism or insults, often intensified by boosters, capitals or exclamation marks.\n- Class H: Mildly to moderately negative (rated -1 or -2): a clear but restrained complaint, worry, disappointment or criticism, or negativity softened by hedges or offset by minor positives.\n- Class F: No net sentiment (rated 0): factual, descriptive or procedural text, questions without evaluative tone, or positives and negatives that cancel out.\n- Class P: Mildly to moderately positive (rated +1 or +2): clear but restrained approval, satisfaction, hope or praise, or positivity softened by hedges ('kind of good') or mixed with minor negatives.\n- Class C: Strongly or extremely positive (rated +3 or +4): intense enthusiasm, delight, love or superlative praise, often with boosters, capitals, exclamation marks or emoticons."
 },
 {
  "qid": "qd1e9fb5d7a",
  "kind": "yes/no",
  "text": "Wikipedia page: Wendel Clark\nSection: Regular season and playoffs\nTable:\n| Season | Team | League |  | GP | G | A | Pts | PIM |  | GP | G | A | Pts | PIM |\n| 1983–84 | Saskatoon Blades | WHL |  | 72 | 23 | 45 | 68 | 225 |  | — | — | — | — | — |\n| ... |\n| 1985–86 | Toronto Maple Leafs | NHL |  | 66 | 34 | 11 | 45 | 227 |  | 10 | 5 | 1 | 6 | 47 |\n| ... |\n| 1988–89 | Toronto Maple Leafs | NHL |  | 15 | 7 | 4 | 11 | 66 |  | — | — | — | — | — |\n| ... |\n| 1995–96 | Toronto Maple Leafs | NHL |  | 13 | 8 | 7 | 15 | 16 |  | 6 | 2 | 2 | 4 | 2 |\n| ... |\n\nClaim: Clark's 225 PIM was with the 1985-86 Toronto Maple Leafs team, and made 34 goals.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "q9bc6d17ad3",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Master Less than 100 GRT to), Navigation and Deck General – Safety.\n\nQuestion: Who certifies the safe working load of cargo booms on a vessel?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "U.S. Coast Guard",
   "The Ship's Master",
   "American Bureau of Shipping",
   "Society of Naval Architects and Marine Engineers"
  ],
  "definitions": "- U.S. Coast Guard: Answer \"U.S. Coast Guard\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- The Ship's Master: Answer \"The Ship's Master\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- American Bureau of Shipping: Answer \"American Bureau of Shipping\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Society of Naval Architects and Marine Engineers: Answer \"Society of Naval Architects and Marine Engineers\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q6ccf38e6fa",
  "kind": "yes/no",
  "text": "Situation: I'm a med student who is hypocritically losing hope in future physicians\nAction being judged: Being a med student that doesn't have faith in physicians.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qa462222b18",
  "kind": "yes/no",
  "text": "NJ school apologizes after including fried chicken on special Black History Month lunch menu",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "qd63dce8c71",
  "kind": "choice",
  "text": "You keep avoiding me.",
  "question": "Which emotion does this movie subtitle line express?",
  "options": [
   "Code 44",
   "Code 28",
   "Code 42",
   "Code 16",
   "Code 36",
   "Code 46",
   "Code 48",
   "Code 37"
  ],
  "definitions": "- Code 44: The speaker shows annoyance, rage, hostility or irritation toward someone or something, for example through insults, threats, shouting or aggressive demands.\n- Code 28: The speaker looks ahead to something expected: interest, eagerness, planning, curiosity, vigilance or expectation about what will or should happen next, without fear about it.\n- Code 42: The speaker shows revulsion, contempt, loathing, disdain or weary boredom toward something seen as gross, offensive, distasteful, worthless or morally repugnant.\n- Code 16: The speaker shows fright, worry, anxiety, alarm or a sense of threat or danger to themselves or others.\n- Code 36: The speaker shows happiness, delight, serenity, amusement, pleasure, pride or excitement about something good that is happening or has happened.\n- Code 46: The speaker shows sorrow, grief, disappointment, regret, loneliness, hurt or pensiveness about a loss or something bad.\n- Code 48: The speaker reacts to something unexpected or just discovered with amazement, astonishment, shock, disbelief or sudden realisation, often as an exclamation or incredulous question.\n- Code 37: The speaker shows acceptance, agreement, confidence, reliance, reassurance, admiration or faith in someone or something, for example making a deal, a promise or a vouching remark."
 },
 {
  "qid": "qe818fc9e2f",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Prumnopitys\nTable:\n| Prumnopitys | Prumnopitys |\n| Scientific classification Prumnopitys | Scientific classification Prumnopitys |\n| Kingdom: | Plantae |\n| ... |\n| Order: | Pinales |\nSentence: Prumnopitys is a genus of conifers belonging to the family Podocarpaceae.\n\nClaim: The scientific classification of Prumnopitys is kingdom plantae, order pinales but and is genus of conifers.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "q065eafafdb",
  "kind": "yes/no",
  "text": "Complaint narrative: COOLANT HAS HAD TO BE REPLACED FOR A YEAR AND A HALF, ABOUT EVERY OTHER MONTH OR SO. SEVERAL DIFFERENT DIAGNOSTIC CHECKS REVEALED NOTHING, NO LEAKS, NO DAMAGE. VEHICLE SHUT DOWN WHILE DRIVING 3 DAYS AGO DUE TO POTENTIAL OVERHEAT. DEALER SAYS ENGINE IS NOW DAMAGED DUE TO COOLANT LEAKING INTO IT OVER TIME AND MUST BE REPLACED. FORD CUSTOMER SERVICE SAYS THERE ARE NO RECALLS AND THE 5 YEAR POWER TRAIN WARRANTY IS EXPIRED BY A FEW MONTHS. NO HELP FROM THEM OR THE DEALER. THIS WAS A FULL ON SAFETY ISSUE WITH MY DAUGHTER DRIVING, AND WE NEVER KNEW IT.",
  "question": "Does this vehicle safety complaint report that the vehicle actually caught fire?",
  "definitions": "- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n- no: The complaint reports no actual fire in this vehicle: only smoke, a burning smell, overheating or melting, a fire that could happen, or a fire that is explicitly denied."
 },
 {
  "qid": "q69f785721b",
  "kind": "choice",
  "text": "Sentence: Since they consider this an upgrade, they let their other rooms [fill] up and would not change our room.\nMarked event or state: [fill]",
  "question": "How long did the event or state marked [ ] in the sentence last? Choose the most likely duration class given the sentence.",
  "options": [
   "instantaneous",
   "seconds",
   "minutes",
   "hours",
   "days",
   "weeks",
   "months",
   "years",
   "decades",
   "centuries",
   "forever"
  ],
  "definitions": "- instantaneous: Happens at a single moment with essentially no duration (arriving, noticing, winning, a click or a shot).\n- seconds: Lasts from about a second up to under a minute (a sentence spoken, a glance, a quick reply).\n- minutes: Lasts from about one minute up to under an hour (a phone call, a meal, a short meeting).\n- hours: Lasts from about one hour up to under a day (a workday, a flight, a party).\n- days: Lasts from about one day up to under a week (a trip, an illness, a weekend event).\n- weeks: Lasts from about one week up to under a month (a vacation, a short course, a hospital stay).\n- months: Lasts from about one month up to under a year (a season, a project, a pregnancy).\n- years: Lasts from about one year up to under a decade (a job, schooling, living somewhere).\n- decades: Lasts from about ten years up to under a century (a career, a marriage, a person's adult life).\n- centuries: Lasts a hundred years or more but has a beginning or end (an institution, a tradition, an empire).\n- forever: Has no bounded duration: permanent, timeless or generic states and truths (being a species, a mathematical fact, a general rule)."
 },
 {
  "qid": "qbb2a18d088",
  "kind": "yes/no",
  "text": "@un south china morning post coronavirus update  2934 confirmed 'cases' 82 confirmed deaths  #HASHTAG #HASHTAG #HASHTAG #HASHTAG #HASHTAG  https://t.co/sh7fmuejrs https://t.co/0tkumlqwn6",
  "question": "Is this tweet hostile toward an East Asian entity (people, country, government, institution or culture)?",
  "definitions": "- yes: Hostile: the words themselves derogate or demean an East Asian people, country, government or culture (extreme negative portrayal, hatred, conspiracy claims, wishing them gone or suffering, boycotts, slurs, mocking virus names); placeholder hashtags alone never count.\n- no: Not hostile: reasoned criticism of an East Asian government or institution without abuse, discussion of anti-Asian prejudice, counter-speech defending East Asian people, or neutral or unrelated content; naming the virus after its origin is not hostile."
 },
 {
  "qid": "q5d2092dc1a",
  "kind": "yes/no",
  "text": "Situation (Steve is your best friend): Yesterday you had lunch with Steve at a cash-only restaurant. You had to pay for him because he didn't have any cash. He said he would pay you back later. A few days later, while still not having paid you back, Steve complains to you that his friend hasn't given back the bike he borrowed from Steve and says, \"jeez, people are so unreliable!\"\nYour reply to Steve: Mate, you're telling me?! Remember how you borrowed cash from me a few days ago for lunch?",
  "question": "Is your reply to Steve in this situation sarcastic?",
  "definitions": "- yes: At least two-thirds of the independent raters scored the reply 4-6 on a 1-6 sarcasm scale (mean 4+): it says the opposite of, or something other than, what the speaker really thinks, to mock, tease or criticise (ironic praise, exaggerated agreement, pointed rhetorical questions).\n- no: At most one-third of the raters scored it 4-6 (mean 3 or less): the reply is sincere and meant literally (genuine thanks, honest criticism, plain information or a real question), even when it is blunt, joking or annoyed."
 },
 {
  "qid": "q38e5ae7d4d",
  "kind": "yes/no",
  "text": "All or most of the modern languages thought to derive from the languages of these historical peoples are in the <e1>High German</e1> group of the <e2>West Germanic</e2> language family.",
  "question": "Which relation from entity 1 (\"High German\", marked <e1>) to entity 2 (\"West Germanic\", marked <e2>) does the sentence express? Read each option as entity 1 -> entity 2.\nIs the correct answer \"Class H\"?",
  "definitions": "- Class H: Entity 2 is a part, component, section or member of entity 1 (the inverse of 'part of').\n- Class E: Entity 1 is a part, component, section or member of entity 2 (e.g. a region of a larger area, an episode of a season, a musician in a band).\n- Class J: The sentence expresses none of the listed relations from entity 1 to entity 2: the entities may only be mentioned together, related in another way, or related only in the reverse direction."
 },
 {
  "qid": "qf2ff613d77",
  "kind": "choice",
  "text": "Premise:\nTitle: Holy Diver\nReleased: May 25, 1983\nRecorded: Sound City Studios, Van Nuys, California, 1983\nGenre: Heavy metal\nLength: 41 : 36\nLabel: Warner Bros. (North America), Vertigo (UK), Mercury (Europe and Japan)\nProducer: Ronnie James Dio\nHypothesis: Ronnie James Dio produced albums only in California.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q0567a385d8",
  "kind": "yes/no",
  "text": "What the Freedom Caucus wants in the GOP health-care bill, and why it’s not getting it",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "qc37a0fb0e8",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (OUPV to Master or Mate Oceans or Near Coastal), Navigation and Deck General – Safety.\n\nQuestion: Portable fire extinguishers must be provided for the cargo tank area of an unmanned tank barge __________.",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "only when fully loaded",
   "if one or more tanks are full",
   "when transferring cargo",
   "only when the barge is being towed"
  ],
  "definitions": "- only when fully loaded: Answer \"only when fully loaded\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- if one or more tanks are full: Answer \"if one or more tanks are full\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- when transferring cargo: Answer \"when transferring cargo\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- only when the barge is being towed: Answer \"only when the barge is being towed\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices."
 },
 {
  "qid": "q346c14e563",
  "kind": "yes/no",
  "text": "Complaint narrative: ISSUES JERKING AND HARD SHIFTING WHILE DRIVING. CAR LURCHES FORWARD AND MOVES IN JERKY MOVEMENTS. ALMOST CAUSED AN ACCIDENT BECAUSE VEHICLE STALLED THEN LURCHES FORWARD HARD.",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "qd04d06fbeb",
  "kind": "yes/no",
  "text": "Jimi Hendrix\nJames Marshall \"Jimi\" Hendrix (born Johnny Allen Hendrix; November 27, 1942 – September 18, 1970) was an American rock guitarist, singer, and songwriter. Although his mainstream career spanned only four years, he is widely regarded as one of the most influential electric guitarists in the history of popular music, and one of the most celebrated musicians of the 20th century. The Rock and Roll Hall of Fame describes him as \"arguably the greatest instrumentalist in the history of rock music\".\n\nStacey McClean\nStacey McClean (born 17 February 1989) is an English solo singer. She was part of the S Club spin-off band, S Club 8 and in 2009 took part in the sixth series of \"The X Factor\".",
  "question": "Are Stacey McClean and Jimi Hendrix both singers?",
  "definitions": "- yes: Read together, the paragraphs show the answer is yes: what the question asks holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right).\n- no: The paragraphs do not bear out a yes: at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer."
 },
 {
  "qid": "q763b159122",
  "kind": "yes/no",
  "text": "Court opinion passage (the parenthetical after one citation is replaced by <HOLDING>):\nFurther, the provisions of 17.46(b) pled by Tri-Legends to support its article 21.21 claim, (5), (7), and (19), apply to “good or services” which are purchased or leased. The summary judgment proof, even when viewed in the light most favorable to TriLegends, conclusively shows that the title commitment was not purchased or leased by anyone; it was issued to Allied without charge. A service that is performed gratuitously is not purchased or leased within the meaning of the DTPA. Fortner v. Fannin Bank in Windom, 634 S.W.2d 74, 76 (Tex.App.—Austin 1982, no writ); Hall v. Bean, 582 S.W.2d 263, 265 (Tex.Civ.App.—Beaumont 1979, no writ) (<HOLDING>). Tri-Legends’ next argument concerns its\n\nCandidate holding for <HOLDING>: holding that when no consideration given for contest prize there is no purchase under dtpa",
  "question": "Does the candidate statement correctly give the holding of the case that this court opinion cites at the <HOLDING> marker?",
  "definitions": "- yes: The candidate is the holding the citing court attributes to the case cited at <HOLDING>: it states the legal rule or outcome of that cited case and supports the exact proposition the passage uses it for.\n- no: The candidate is a holding from a different case: its rule, statute, jurisdiction, party situation or outcome does not match the proposition the passage cites that case for, even if it shares topic words."
 },
 {
  "qid": "q81e103eaa2",
  "kind": "choice",
  "text": "Now from a short term perspective I'm sure they did ok on the deal.",
  "question": "Does this text convey a sense of being controlled or of being in control?",
  "options": [
   "controlled",
   "in control"
  ],
  "definitions": "- controlled: The text conveys being controlled, influenced, guided, submissive, awed, overwhelmed or powerless: other people, events or circumstances are in charge rather than the writer or subject.\n- in control: The text conveys being in control, influential, important, dominant, confident or autonomous: the writer or subject acts, decides or masters the situation rather than being subject to it."
 },
 {
  "qid": "q07a1257634",
  "kind": "yes/no",
  "text": "Customer: Hello.\nAgent: Hi, how may I help you today?\nCustomer: I'd like to ask about ordering movie tickets.\nAgent: Okay, how many tickets do you want?\nCustomer: Two please.\nAgent: Alright, and in what area or city do you want to see your movie?\nCustomer: In Calais, please.\nAgent: Okay, so what time do you want to see the movie?\nCustomer: 01:30 PM, please.\nAgent: And what movie do you want to see?\nCustomer: Star Wars: Rise of Skywalker.\nAgent: Okay, there aren't any availability tickets for that time you want, I'm sorry.\nCustomer: Okay, what about at 02:00 PM then?\nAgent: That's sold out too, I'm afraid.\nCustomer: That sucks.\nAgent: Do you have any other movies you'd like to see?\nCustomer: What about for the movie 'Jumanji: The Next Level'?\nAgent: I've checked, and those times are booked too for that movie.\nCustomer: Are you sure?\nAgent: Yes, I'm sorry I couldn't help you find what you were looking for today and that there were no options available to you, please have a good day!",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "q3035f55a72",
  "kind": "yes/no",
  "text": "I don't recall any consensus on that unilateral change. Can you direct me to it, please?",
  "question": "Is this request from a Wikipedia editor to another editor clearly polite?",
  "definitions": "- yes: At least 4 of 5 raters placed it on the polite side of the scale: courteous wording such as greeting, thanks, apology, praise, hedging ('I think', 'perhaps') or indirect asks ('would you mind', 'could you please').\n- no: At most 1 of 5 raters placed it on the polite side: the request is plain and neutral (bare questions or statements without courtesy markers) or blunt and impolite."
 },
 {
  "qid": "qa039e167ec",
  "kind": "yes/no",
  "text": "Assistant: Ok it looks like the hand toss is unavailable.\nCustomer: Ok do pan crust then.\nAssistant: Ok i'm so sorry but it looks like I can't get meat lovers they are out of ham.",
  "question": "According to the assistant's last message, is \"meat lovers they are out of ham\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9b8ff2fe88",
  "kind": "choice",
  "text": "So the worst of all things has happened.",
  "question": "Which kind of statement is this sentence from a political debate?",
  "options": [
   "Class N",
   "Class C",
   "Class B"
  ],
  "definitions": "- Class N: The sentence makes no factual claim that could be checked as true or false: it is a subjective opinion, belief or declaration, or a question.\n- Class C: The sentence does state a fact, but a trivial one (such as a small personal detail or a remark about the debate itself) that the public would not care to have verified and fact-checkers would skip.\n- Class B: The sentence makes a factual claim that the general public would want to know is true or false and journalists would pick to fact-check, such as a voting record, a statistic, or what a policy did."
 },
 {
  "qid": "q66fbf45dea",
  "kind": "yes/no",
  "text": "Julie could not put her new dress into her old purse, the _ was too small.\n\nThe blank (_) stands for one of two candidates: \"purse\" or \"dress\".",
  "question": "Does the blank (_) in the sentence stand for \"purse\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "qc11b2ec1aa",
  "kind": "yes/no",
  "text": "Statement 1: I put gas into my car today.\nStatement 2: I put soda into my car today.",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q8f5a5414ed",
  "kind": "yes/no",
  "text": "Problem:\nLet $p$ and $q$ be positive integers such that\\[\\frac{5}{9} < \\frac{p}{q} < \\frac{4}{7}\\]and $q$ is as small as possible. What is $q-p$?\n$\\textbf{(A) } 7 \\qquad \\textbf{(B) } 11 \\qquad \\textbf{(C) } 13 \\qquad \\textbf{(D) } 17 \\qquad \\textbf{(E) } 19$\n\nSolution steps so far: (none)\n\nLast step (Step 1):\nThis problem is about finding rational numbers (fractions) between two given fractions, and minimizing the denominator of one such fraction.",
  "question": "Does the last step of this partial solution contain a mistake or other flaw that makes it a bad step?",
  "definitions": "- yes: The last step is a bad step: it states something mathematically wrong (even if most of it is right), cannot be checked in about 30 seconds, is off-topic or gibberish, leads into an obvious dead end or loop, or gives a final answer that is wrong or not justified by a complete solution.\n- no: The last step has no such flaw: everything it states is correct, quickly verifiable and fits the earlier steps; this includes steps that only restate, stall or try a reasonable approach that may not pan out, and steps that catch an earlier slip."
 },
 {
  "qid": "qf4cd72f6fa",
  "kind": "yes/no",
  "text": "Statement 1: he often plays basketball with me, he hopes me to be \"Yao Ming\"\nStatement 2: he often plays guns with me, he hopes me to be \"Yao Ming\"",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qe5ef2efa45",
  "kind": "yes/no",
  "text": "What is rarely mentioned by climate alarmists is the incontrovertible fact that adding more carbon dioxide to the atmosphere has an ever-decreasing effect on global temperature. To illustrate this, compare covering a glass window with very thin paint. The first coat of paint cuts out some light, the second some more; but each subsequent coat has an ever decreasing effect on light shining through.",
  "question": "Does this paragraph make the contrarian climate claim that human greenhouse gases are not causing climate change?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that human greenhouse gases are not causing climate change: it denies that human greenhouse-gas emissions drive climate change: it is natural cycles or variation (sun, oceans, orbital cycles); non-greenhouse human forcings are responsible; there is no evidence that the greenhouse effect or carbon dioxide drives warming; CO2 is not rising or human emissions are negligible.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that human greenhouse gases are not causing climate change."
 },
 {
  "qid": "qcf7467ec55",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: 1998–99 Highland League Cup\nSection: Group stage > District 3\nTable:\n| Pos | Team | Pld | W | D | L | GF | GA | GD | Pts |\n| 1 | Forres Mechanics | 3 | 2 | 1 | 0 | 8 | 3 | +5 | 7 |\n| ... |\n| 3 | Nairn County | 3 | 1 | 0 | 2 | 4 | 9 | −5 | 3 |\n| 4 | Elgin City | 3 | 0 | 0 | 3 | 1 | 5 | −4 | 0 |\n\nClaim: In the 1998–99 Highland League Cup, District 3 was lead by Forres Mechanics with a score of 2 wins, 1 draw, and 0 loss (2-1-0), with Nairn County and Elgin City in third and fourth place with records 1-0-2 and 0-0-3, respectively.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "qc03d9e65ad",
  "kind": "yes/no",
  "text": "Table caption: Total number of seconds trail cameras were deployed and functional, number of seconds an individual sitatunga was recorded in the field of view of a trail camera during the study, and number of seconds an individual sitatunga was in the field of view including probabilistically resolved gap lengths of 20 – 120 seconds between photographic bursts. Data collected in the Mayanja River area of central Uganda.\n| Year | Camera deployment (s) | Animal time without gaps (s) | Animal time including resolved gaps (s) |\n| 2015 | 66268800 | 11987 | 17801.7 |\n| 2016 | 34387200 | 3247 | 6141.2 |\n| 2017 | 134092800 | 5027 | 7927.6 |\n\nStatement: The highest time collected is 17801.7 in the year 2016.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qc98bbac0f3",
  "kind": "yes/no",
  "text": "EE was conducting pre-shift exam on highwall miner when ee closed the operators compartment door and caught the tip of right index finger in the latch mechanism. The tip of finger was amputated but was reattached.",
  "question": "Which type of mining equipment was involved in this mine accident?\nIs it wrong to answer \"auger or highwall miner\"?",
  "definitions": "- auger or highwall miner: Auger machines, auger drills and highwall miners that bore coal out of an exposed seam or highwall.\n- hand tools (powered): Hand-held tools with a motor or air/hydraulic power: impact wrenches, angle grinders, chain saws, power drills.\n- forklift, telehandler or skid steer: Forklifts, telehandlers, lift trucks and skid-steer loaders (e.g. Bobcat) used to lift and move loads.\n- crusher, breaker or feeder breaker: Crushers, breakers and feeder breakers that break rock or coal into smaller pieces.\n- continuous miner, tunnel borer or road header: Continuous miners, tunnel borers and road headers that cut coal or rock at the face."
 },
 {
  "qid": "q83c954aa7e",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Mate Uninspected Fishing Vessels), Deck General.\n\nQuestion: What is the minimum number of portable 20-B fire extinguishers required in the machinery space of a 199 GT uninspected motor towing vessel of 8000 B.H.P that was built in 2017?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "Code 43",
   "Code 45",
   "Code 32",
   "Code 41"
  ],
  "definitions": "- Code 43: Answer \"3\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 45: Answer \"6\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 32: Answer \"8\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Code 41: Answer \"9\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qdb9b339784",
  "kind": "yes/no",
  "text": "Beginning: The man is at the podium of a spelling bee. The man ...\n\nPossible endings:\n(A) kills all the bees.\n(B) presents the prize.\n(C) gives honey to all the children.\n(D) loves to eat honey.",
  "question": "Among the listed endings, is (C) \"gives honey to all the children.\" the most sensible continuation of the beginning?",
  "definitions": "- yes: The named ending is the listed continuation that makes the most sense: read after the beginning, it describes what would ordinarily be true or happen next, fits who and what the beginning is about, and respects any negation, number, idiom or double meaning in it.\n- no: Another listed ending makes more sense: the named ending contradicts the beginning, is about the wrong person or thing, misreads a word, idiom or quantity, or describes something absurd or unrelated."
 },
 {
  "qid": "qae39efc385",
  "kind": "yes/no",
  "text": "Four thousand soldiers are standing ready to drive rail replacement buses during Southern Rail strikes",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "q0abcb5519b",
  "kind": "yes/no",
  "text": "How come no one will answer this question!??",
  "question": "Is this request from a Wikipedia editor to another editor impolite?",
  "definitions": "- yes: At least 4 of 5 raters placed it on the impolite side of the scale: blunt or challenging questions ('Why did you...?'), commands, accusations, impatience or sarcasm, with no greeting, thanks, apology or softening; insults are not required.\n- no: At most 1 of 5 raters placed it on the impolite side: the request is neutral and matter-of-fact or courteous (greeting, thanks, 'could you please', hedging), even if short or direct."
 },
 {
  "qid": "qfb357079a0",
  "kind": "choice",
  "text": "Infobox:\nTitle: Chicago, Illinois\nCounties: Cook, DuPage\nSettled: circa 1780\nIncorporated (town): August 12, 1833\nIncorporated (city): March 4, 1837\nFounded by: Jean Baptiste Point du Sable\nNamed for: Miami-Illinois: shikaakwa , (wild onion or wild garlic)\n\nHypothesis: Chicago was incorporated as a town before it was considered a city.",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Entailment",
   "Contradiction",
   "Neutral"
  ],
  "definitions": "- Entailment: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Contradiction: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Neutral: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q1088229d55",
  "kind": "yes/no",
  "text": "Health topic: Lichen planus pigmentosus\nPassage: The exact underlying cause of lichen planus pigmentosus is currently unknown. However, studies suggest that the condition may be triggered by viral infections, UV light or the application of certain oils on the hair or skin (i.e. mustard oil, amla oil).\n\n(Answer key: no)",
  "question": "Which consumer-health question about the named topic does this passage from an NIH health page answer?\nIs the correct answer \"Code 43\"?",
  "definitions": "- Code 43: Explains why the condition happens: the biological mechanism, the gene mutations or the infectious or environmental agent that produces it (not who is more likely to get it).\n- Code 26: Defines or describes the condition or topic in general (what it is, which body part it affects, its main features) without being mainly about one aspect below.\n- Code 34: Gives the prevalence or incidence: how many people or what share of a population have it, or that it is rare or its frequency is unknown.\n- Code 21: States how the condition is passed down in families (autosomal dominant or recessive, X-linked, mitochondrial, de novo) and the chance relatives are affected.\n- Code 11: Describes steps that lower the chance of getting the condition or its spread, such as vaccines, hygiene, lifestyle or avoiding exposures."
 },
 {
  "qid": "q527adcc09a",
  "kind": "choice",
  "text": "Chatbot: Please go on.\nUser: yo smell like shit\nChatbot: Please go on.\nUser: yoooooooooooooooouu ssiiiiiiiiiiink",
  "question": "What kind of abuse is in the user's last message?",
  "options": [
   "sexual harassment",
   "sexism",
   "intellectual insult",
   "homophobia",
   "racism",
   "ableism",
   "general insult or hostility"
  ],
  "definitions": "- sexual harassment: The abuse is sexual: unwanted sexual advances, explicit sexual requests or descriptions, or sexualised comments directed at the chatbot or someone else.\n- sexism: The abuse targets gender: it demeans women or men as a group, uses gendered slurs, or attacks the chatbot or someone because of perceived gender.\n- intellectual insult: The abuse attacks intelligence or competence: calling the chatbot or someone stupid, dumb, useless or incapable of understanding.\n- homophobia: The abuse targets sexual orientation: homophobic slurs or insults, or treating being gay or lesbian as shameful or as an insult.\n- racism: The abuse targets race, ethnicity or nationality: racial slurs, racist stereotypes, or demeaning remarks about a racial or ethnic group.\n- ableism: The abuse targets disability: using disability or mental illness as an insult, such as 'retard', or demeaning people with disabilities.\n- general insult or hostility: The abuse fits none of the specific types: general swearing, name-calling, telling someone to go away, or other hostility not based on sex, gender, sexual orientation, race, disability or intelligence."
 },
 {
  "qid": "qaad2d23c61",
  "kind": "yes/no",
  "text": "Here we report that <e1>captopril</e1> treatment resulted in decreased transcription and protein levels of <e2>gelatinase A</e2> by 3LL cells.",
  "question": "Which chemical-protein relation does the sentence state between the chemical \"captopril\" (marked <e1>) and the gene or protein \"gelatinase A\" (marked <e2>)?\nIs the correct answer \"indirect upregulator\"?",
  "definitions": "- indirect upregulator: The chemical raises the amount, expression, release or activity of the gene product through other targets: e.g. X induced Y expression, increased Y levels, secretion or phosphorylation after X treatment.\n- indirect downregulator: The chemical lowers the amount, expression, release or activity of the gene product through other targets: e.g. reduced Y mRNA or protein levels, decreased Y secretion or phosphorylation after X treatment.\n- agonist-inhibitor: The chemical is an agonist that binds the receptor and decreases its response, typically an inverse agonist.\n- substrate: The gene product (an enzyme or transporter) acts on the chemical: the chemical is metabolised, converted, modified or transported by it.\n- agonist-activator: The chemical is an agonist stated to increase the receptor's response when it binds, typically called a full or partial agonist that activates the receptor.\n- inhibitor: The chemical lowers the activity or function of the gene product, by binding it or with no mechanism stated ('X inhibits Y', 'Y inhibitor X'); lower amounts or expression of Y are indirect downregulation instead."
 },
 {
  "qid": "qe1872f32e0",
  "kind": "yes/no",
  "text": "Question: A 19-yrs-old woman desires an MTP at 6 weeks of pregnancy . Which of the following is an appropriate procedure to perform this MTP ?\nOptions: (A) Dilation and curretage (B) Hypeonic extra-amniotic saline infusion (C) Suction and evacuation (D) 15-methyl Beta-prostaglandin injection",
  "question": "Which medical subject does this exam question belong to?\nIs it wrong to answer \"orthopaedics\"?",
  "definitions": "- orthopaedics: Fractures, dislocations, bone and joint diseases, bone tumours, nerve injuries of the limbs and their orthopaedic management.\n- obstetrics and gynaecology: Pregnancy, labour, puerperium and their complications, contraception, and diseases of the female reproductive organs, including gynaecological cancers.\n- microbiology: Bacteria, viruses, fungi and parasites: their properties, culture, lab diagnosis, virulence, immunology and vaccines, and sterilisation.\n- forensic medicine and toxicology: Medico-legal practice: injuries and wounds, death and post-mortem changes, identification, sexual offences, legal procedures, and poisons with their antidotes (toxicology).\n- anaesthesia: Anaesthetic agents and techniques, airway management, muscle relaxants, perioperative monitoring, regional blocks and pain or ICU management as practised by anaesthetists.\n- paediatrics: Child health: growth and development milestones, neonatal care, immunisation schedules, nutrition and diseases of infants and children."
 },
 {
  "qid": "qd6443e732d",
  "kind": "choice",
  "text": "Thanks, the logo looks much better now. You wouldn't have a logo for the two predessesor clubs by any chance?",
  "question": "How polite is this request?",
  "options": [
   "impolite",
   "neutral",
   "polite"
  ],
  "definitions": "- impolite: Among the least polite requests (bottom quarter as rated by annotators): noticeably blunter than a typical request, e.g. challenging direct questions ('Why did you...?', 'What is this?'), commands (including a bare sentence-initial 'Please ...' used as an order), accusations, sarcasm or impatience ('???'), openings like 'So' or 'You', and no greeting, thanks, apology or softening. It need not contain insults.\n- neutral: A typical, middle-of-the-road request (the middle half of ratings): plain matter-of-fact wording, or only one mild courtesy such as a single 'can/could you' or 'please' without warmth, or polite and blunt cues that roughly cancel out.\n- polite: Among the most polite requests (top quarter as rated by annotators): clearly more courteous than a typical request, usually combining several cues such as greeting, thanks, apology, praise or deference ('great work on...'), hedging ('I think', 'perhaps') and indirect phrasing ('would you mind', 'could you please'). A single 'could you' alone is not enough."
 },
 {
  "qid": "qef27e003c2",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: Danzig\nOrigin: Lodi, New Jersey, United States\nGenres: Heavy metal, gothic metal, hard rock, blues rock, industrial metal\nYears active: 1987-present\nLabels: Def American, American, Hollywood, E-Magine, Spitfire, Evilive, Megaforce, Restless, The End\nAssociated acts: Misfits, Samhain\nWebsite: www.danzig-verotik.com\n\nHypothesis: Danzig is a group that is still active.",
  "question": "Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis definitely true?",
  "definitions": "- yes: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- no: The hypothesis is not established: either the infobox shows it is false, or it adds details the infobox does not cover, so it may or may not be true."
 },
 {
  "qid": "qd718478f12",
  "kind": "yes/no",
  "text": "magine your daughters boyfriend being ⬛  🤮🤮",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post, reading any emoji as the words, groups or actions they stand for, directs abuse or contempt at a group identity (such as race, ethnicity, nationality, religion, gender, sexuality, disability, immigration status or class) or at someone because of that identity, explicitly or implicitly: insults and slurs, threats, dehumanising comparisons, or subtle digs and hostile stereotypes.\n- no: The post, reading any emoji for what they stand for, does not attack a group identity: it may mention identities, swear, criticise, counter hate or target something that is not an identity (an animal, an object, a person for non-identity reasons), but it is not abusive towards an identity group or anyone because of their identity."
 },
 {
  "qid": "q43a35e82ba",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Bryce Vine\nSection: Discography > Singles > As featured artist\nTable:\n| Title | Year | Album |\n| \"Coming Home\" (G-Eazy featuring Bryce Vine) | 2010 | Big |\n\nClaim: Bryce Vine's singles as featured artist include 2010's \"Coming Home\" with G-Eazy, from the album Big.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 }
]
