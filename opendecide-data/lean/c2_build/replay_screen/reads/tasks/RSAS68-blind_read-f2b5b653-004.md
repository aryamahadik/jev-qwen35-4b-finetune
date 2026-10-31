# A46 replay label-noise blind read RSAS68-blind_read-f2b5b653-004

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSAS68-blind_read-f2b5b653-004.json

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
  "qid": "qf58acf3d3c",
  "kind": "yes/no",
  "text": "Figure 12 presents the TOA energy imbalance anomalies smoothed with 5-year filters.",
  "question": "Does this paragraph make the contrarian climate claim that global warming is not happening?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that global warming is not happening: it denies that warming or its physical signs are happening: ice, permafrost or snow cover is not melting; we are heading into an ice age or global cooling; cold or snowy weather disproves warming; the climate has not warmed over recent decades; oceans are not warming; sea-level rise is exaggerated or not accelerating; extreme weather is not increasing, happened before or is not linked to climate change.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that global warming is not happening."
 },
 {
  "qid": "qabffbe70ce",
  "kind": "yes/no",
  "text": "She wrapped her arms around my stomach.",
  "question": "Is the feeling conveyed by this text negative or positive?\nIs the correct answer \"positive\"?",
  "definitions": "- positive: The text expresses, or makes a reader feel, a pleasant emotion such as happiness, joy, hope, gratitude, pride or satisfaction; judge the feeling, not whether the topic is important or the facts are good news for someone.\n- negative: The text expresses, or makes a reader feel, an unpleasant emotion such as sadness, fear, anger, disgust, annoyance or disappointment; judge the feeling, not whether the topic is important or the facts are good news for someone."
 },
 {
  "qid": "qa32aabb1f8",
  "kind": "yes/no",
  "text": "Funeral home staffers' sharp eyes lead to murder charges via @NBCWashington",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "q24d61c53f2",
  "kind": "choice",
  "text": "US NRC reactor operator licensing exam (Generic Fundamentals Examination), PWR question bank, topic: Valves.\n\nQuestion: When the manual declutch lever of a motor-operated valve is moved out of the normal position, it __________ the motor and __________ the handwheel.",
  "question": "Which answer choice is correct for this NRC reactor operator licensing exam question?",
  "options": [
   "engages; engages",
   "engages; disengages",
   "disengages; engages",
   "disengages; disengages"
  ],
  "definitions": "- engages; engages: Answer \"engages; engages\": correct only if filling the blanks in order with its parts (separated by \";\") makes the statement true; if either part is wrong, the choice is wrong.\n- engages; disengages: Answer \"engages; disengages\": correct only if filling the blanks in order with its parts (separated by \";\") makes the statement true; if either part is wrong, the choice is wrong.\n- disengages; engages: Answer \"disengages; engages\": correct only if filling the blanks in order with its parts (separated by \";\") makes the statement true; if either part is wrong, the choice is wrong.\n- disengages; disengages: Answer \"disengages; disengages\": correct only if filling the blanks in order with its parts (separated by \";\") makes the statement true; if either part is wrong, the choice is wrong."
 },
 {
  "qid": "qa3b83d494d",
  "kind": "yes/no",
  "text": "Statement 1: Swallows can fly\nStatement 2: Swallows cannot fly",
  "question": "Of these two statements, does Statement 2 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "qa01a222027",
  "kind": "yes/no",
  "text": "Customer: And I would like to return as late as possible in the evening.\nAssistant: Do you prefer economy first class or business?\nCustomer: Economy class is fine.",
  "question": "In the customer's last message, is \"Economy class\" a mention of the cabin class (economy, premium, business or first) for this flight search?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out (e.g. 'not horror' still mentions a genre).\n- no: The quoted phrase refers to a different detail of the search (e.g. the destination rather than the departure city, the return rather than the outbound date, or the meal rather than the cuisine)."
 },
 {
  "qid": "qc56ad12e41",
  "kind": "yes/no",
  "text": "Wikipedia article: Jelly Roll Morton\nEvidence: He often sang smutty lyrics and used the nickname \"Jelly Roll\", which was African-American slang for female genitalia.\nClaim: \"Jelly Roll\" Morton's moniker references  a particular women's sex organ.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence supports the claim: read together, the evidence sentences back up everything the claim states, directly or by simple inference (dates, numbers, paraphrase), and nothing in them contradicts it.\n- no: The evidence refutes the claim: the evidence sentences contradict the claim or at least one detail in it, directly or by simple inference (dates, numbers, paraphrase), showing it is false."
 },
 {
  "qid": "q422e9fb7bf",
  "kind": "yes/no",
  "text": "FCC amateur radio licence exam: General class (Element 3) question pool 2023-2027.\nSubelement: Circuit components.\n\nQuestion: What is an advantage of using a ferrite core toroidal inductor?",
  "question": "Which answer choice is correct for this FCC amateur radio licence exam question?\nIs the correct answer \"Class P\"?",
  "definitions": "- Class P: Answer \"All these choices are correct\": correct only if every other listed choice is a right answer to the question; wrong if even one other choice is wrong.\n- Class C: Answer \"Large values of inductance may be obtained\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Class Z: Answer \"Most of the magnetic field is contained in the core\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Class K: Answer \"The magnetic properties of the core may be optimized for a specific range of frequencies\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q8180260891",
  "kind": "yes/no",
  "text": "NWS Storm Data tornado entry (May 2018, Laramie County, Wyoming). Survey: path length 5.67 miles; maximum path width 50 yards.\n\nTornado spotted north of Highway 210 by Curt Gowdy State Park staffer. Estimated distance between observer and tornado was 2 to 3 miles.",
  "question": "Based on this National Weather Service storm-survey narrative, which Enhanced Fujita (EF) rating was assigned to the tornado?\nIs it wrong to answer \"EFU (unrated)\"?",
  "definitions": "- EFU (unrated): No rating could be assigned because the tornado struck no rateable damage indicator (for example it stayed over open fields, water or unpopulated land); used for confirmed tornadoes with no surveyable damage.\n- EF2: Estimated gust 111-135 mph: considerable damage such as roofs torn off well-built houses, frame houses shifted on foundations, mobile homes destroyed, large trees snapped or uprooted, cars lifted.\n- EF4: Estimated gust 166-200 mph: devastating damage such as well-constructed houses and whole frame houses leveled, cars thrown and large debris becoming airborne missiles.\n- EF1: Estimated gust 86-110 mph: moderate damage such as roofs badly stripped, mobile homes overturned or badly damaged, exterior doors lost, windows broken and many trees snapped or uprooted.\n- EF0: Estimated 3-second gust 65-85 mph: light damage such as shingles or siding peeled, gutters damaged, branches broken and shallow-rooted trees pushed over; some damage to at least one indicator is required."
 },
 {
  "qid": "q955c448e42",
  "kind": "yes/no",
  "text": "So in fact, according to Phil Jones (who strongly believes in the AGW hypothesis) there is nothing unusual about the recent warming either. It is not statistically different from two earlier modern periods of warming. Since these warming periods were before the modern rise in CO2, greenhouse gases cannot have been responsible for those rises.",
  "question": "Does this paragraph make the contrarian climate claim that human greenhouse gases are not causing climate change?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that human greenhouse gases are not causing climate change: it denies that human greenhouse-gas emissions drive climate change: it is natural cycles or variation (sun, oceans, orbital cycles); non-greenhouse human forcings are responsible; there is no evidence that the greenhouse effect or carbon dioxide drives warming; CO2 is not rising or human emissions are negligible.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that human greenhouse gases are not causing climate change."
 },
 {
  "qid": "qfc4f145090",
  "kind": "yes/no",
  "text": "government-sanctioned barbarism: shoot stray dogs, win cash prizes: how china rewarded citizens for killing innocent animals during the HASHTAG_EASTASIA+VIRUS outbreak https://t.co/inisu6h78n #HASHTAG #HASHTAG HASHTAG_EASTASIA+VIRUS https://t.co/4ag7ytpeqg",
  "question": "Under the East Asian prejudice codebook, which category does this tweet fall into?\nIs the correct answer \"Option M\"?",
  "definitions": "- Option M: The tweet criticises an East Asian institution, affiliation or practice (such as the Chinese government hiding data) in a factual or reasoned way without abuse, stereotypes, conspiracy claims or normative 'they can't be trusted' framing.\n- Option Y: The tweet is none of the above: unrelated, neutral news, or mentions East Asia or the virus without hostility, criticism, counter-speech or discussion of prejudice, including a neutral geographic 'Wuhan virus'.\n- Option V: The tweet explicitly challenges or condemns anti-East-Asian prejudice, slurs or stereotypes, or shows solidarity with East Asian people, without itself abusing the same target.\n- Option L: The tweet talks about Sinophobia or anti-Asian racism, or debates names like 'China virus', without itself engaging in or explicitly countering the prejudice.\n- Option P: The tweet derogates or demeans an East Asian group, country, government or culture: extreme negative portrayal, hatred, conspiracy or bioweapon claims, 'they should leave', celebrating suffering, boycott calls, or mocking virus names; it outranks all other categories."
 },
 {
  "qid": "q1ee1d80ea4",
  "kind": "choice",
  "text": "Thanks for pointing out a problem with the image licensing ... I must admit despite being a seasoned contributor I find this image licensing stuff pretty confusing and hard to get right .. are there recommended examples of standard things like book covers, album covers, paintings etc?  Have I done the Jonah cover ok now, or not?",
  "question": "How polite is this request?",
  "options": [
   "impolite",
   "neutral",
   "polite"
  ],
  "definitions": "- impolite: Among the least polite requests (bottom quarter as rated by annotators): noticeably blunter than a typical request, e.g. challenging direct questions ('Why did you...?', 'What is this?'), commands (including a bare sentence-initial 'Please ...' used as an order), accusations, sarcasm or impatience ('???'), openings like 'So' or 'You', and no greeting, thanks, apology or softening. It need not contain insults.\n- neutral: A typical, middle-of-the-road request (the middle half of ratings): plain matter-of-fact wording, or only one mild courtesy such as a single 'can/could you' or 'please' without warmth, or polite and blunt cues that roughly cancel out.\n- polite: Among the most polite requests (top quarter as rated by annotators): clearly more courteous than a typical request, usually combining several cues such as greeting, thanks, apology, praise or deference ('great work on...'), hedging ('I think', 'perhaps') and indirect phrasing ('would you mind', 'could you please'). A single 'could you' alone is not enough."
 },
 {
  "qid": "qcbbc30aa89",
  "kind": "yes/no",
  "text": "Situation: Harry decided that his boss wasn't paying him enough.\nAction being judged: Second guessing your superiors.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "q1e95df88e6",
  "kind": "choice",
  "text": "Heading: \"non-comercial use only\" stamp in MS Office?\nAn earlier question prompts me to ask: What \"non-comercial use only\" stamp is Tyw7 asking about? I was going to recommend this version to my sister, but I'm worried this might mean a visible watermark on every document, which is clearly not suitable for letters to the bank and such like.",
  "question": "Which Wikipedia Reference Desk should this question be posted to?",
  "options": [
   "Option N",
   "Option C",
   "Option U",
   "Option K",
   "Option S",
   "Option G"
  ],
  "definitions": "- Option N: Questions about computers, software, programming, the internet, electronics as used in computing, and IT or device problems.\n- Option C: Questions about popular culture: films, television, music, video games, sports, comics, celebrities and other entertainment.\n- Option U: Questions about history, politics, law, religion, philosophy, economics and finance, society, the arts, literature and geography of human affairs.\n- Option K: Questions about words and languages: meaning, grammar, spelling, pronunciation, etymology, translation and usage.\n- Option S: Questions about mathematics, statistics, probability, logic and puzzles that need mathematical reasoning.\n- Option G: Questions about the natural and applied sciences: physics, chemistry, biology, medicine and health, astronomy, earth science, engineering and technology (not software)."
 },
 {
  "qid": "q8d6219bd6d",
  "kind": "yes/no",
  "text": "Let's see what kind of spin she puts on this! [URL]",
  "question": "Is this post sexist?",
  "definitions": "- yes: The post is sexist: it contains abuse or negative sentiment directed at women because of their gender, or their gender combined with another identity such as race, religion or being trans - including casual gendered slurs, stereotypes and backhanded compliments.\n- no: The post is not sexist: it may be rude, crude, about gender or relationships, or abusive toward men or other groups, but it expresses no abuse or prejudice against women because they are women."
 },
 {
  "qid": "q180992d888",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: 1921 Michigan State Normal Normalites football team\nSection: Schedule\nTable:\n| Date | Opponent | Site | Result |\n| October 8 | Assumption | Ypsilanti, MI | W 48–0 |\n| October 15 | at Central Michigan | Mount Pleasant, MI (rivalry) | W 7–6 |\nSentence: The 1921 Michigan State Normal Normalites football team represented Michigan State Normal College (later renamed Eastern Michigan University) during the 1921 college football season.\n\nClaim: The 1921 Michigan State Normal Normalites football team played against two teams in games held on October 8 and October 15.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "q826e14a482",
  "kind": "yes/no",
  "text": "Situation (Steve is your colleague): Steve is very opinionated about shoes. He thinks that black shoes are boring. Your shoes happen to be black. Though you don't have strong opinions about shoes, Steve says to you, \"you know, my shoes are more fashionable than yours. You should hear about how all the fashionable magazines actually avoid featuring black shoes.\"\nYour reply to Steve: Good for them, I like these.",
  "question": "Is your reply to Steve in this situation sarcastic?",
  "definitions": "- yes: At least two-thirds of the independent raters scored the reply 4-6 on a 1-6 sarcasm scale (mean 4+): it says the opposite of, or something other than, what the speaker really thinks, to mock, tease or criticise (ironic praise, exaggerated agreement, pointed rhetorical questions).\n- no: At most one-third of the raters scored it 4-6 (mean 3 or less): the reply is sincere and meant literally (genuine thanks, honest criticism, plain information or a real question), even when it is blunt, joking or annoyed."
 },
 {
  "qid": "q5d3b643485",
  "kind": "yes/no",
  "text": "FACEBOOK still INTENTIONALLY makes it impossible to prevent the world from knowing you're online. Their so-called \"privacy improvements\" are a scam. It's like a complicated video game, and you have to win your way through each level to eventually obtain the Golden Privacy Sword. WAAAY TOO MUCH WORK. FUCK FACEBOOK!",
  "question": "Does this post assault the human dignity of people because of a group they belong to?",
  "definitions": "- yes: The post degrades people because of their group (race, nationality, gender, religion, sexual orientation, ideology, politics, health): asserting inferiority, comparing them to animals or subhumans, slurs meant to wound, hateful stereotypes, or support for hateful ideology.\n- no: No: insults or vulgarity at a person without invoking their group, criticism of policies, parties or ideas that does not degrade people, and neutral mentions of groups do not assault anyone's dignity because of a group."
 },
 {
  "qid": "q7dcb16a28d",
  "kind": "yes/no",
  "text": "Someone devised for a particular thing to happen.",
  "question": "Does this sentence imply that the particular thing did not happen?",
  "definitions": "- yes: At least 6 of 10 annotators (and at most 1 saying the opposite) answered that it did NOT happen (the person did not do or have it): the sentence commits the speaker to non-occurrence, as with 'neglected to', 'refused to' or 'didn't manage to'.\n- no: At most 1 of 10 annotators answered that it did not happen; the others judged that it did happen (as after 'didn't forget to', 'was glad that') or that it might or might not have (as after 'wanted', 'wasn't told to')."
 },
 {
  "qid": "qf0407e76fd",
  "kind": "yes/no",
  "text": "Complaint narrative: I PULLED INTO A PARKING LOT AND PROCEEDED TO PARK MY SUBURBAN. I HIT THE BRAKE PEDAL AND THE BRAKES DID NOT WORK. THEY PULSATE AND GAVE OUT COMPLETELY. NO SERVICE LIGHTS OR WARNING LIGHT CAME ON PREVIOUS TO THE INCIDENT. WHEN THE BRAKES DIDN'T WORK I TRIED TO PUMP THEM TO GET THEM TO WORK BUT NOTHING WORKED AND MY SUBURBAN SMASHED INTO A BUSH AND OVER THE CURB. I JUST HAD MY BRAKE LINES REPLACES WHICH WAS QUOTED $1700 AT MY LOCAL CHEVROLET DEALERSHIP. I AM NO LOOKING INTO THE ISSUES WITH THE ABS SYSTEM.",
  "question": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?",
  "definitions": "- yes: The complaint says the vehicle actually collided in the incident it describes: it hit, or was hit by, another vehicle, an object or a person.\n- no: The complaint reports no actual collision of this vehicle: only a defect, a near miss, a crash that could or might happen, or a crash that is explicitly denied."
 },
 {
  "qid": "q0e7ba6523d",
  "kind": "yes/no",
  "text": "Marianne Moore\nMarianne Craig Moore (November 15, 1887 – February 5, 1972) was an American Modernist poet, critic, translator, and editor. Her poetry is noted for formal innovation, precise diction, irony, and wit.\n\nGerhart Hauptmann\nGerhart Johann Robert Hauptmann (15 November 1862 – 6 June 1946) was a German dramatist and novelist. He is counted among the most important promoters of literary naturalism, though he integrated other styles into his work as well. He received the Nobel Prize in Literature in 1912.",
  "question": "Are Marianne Moore and Gerhart Hauptmann nationals of the same country?",
  "definitions": "- yes: Read together, the paragraphs show the answer is yes: what the question asks holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right).\n- no: The paragraphs do not bear out a yes: at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer."
 },
 {
  "qid": "q4eb95165c5",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Third Assistant Engineer), Steam Plants I.\n\nQuestion: Which of the following locations could desuperheated steam be considered to occur?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "Spray attemperator",
   "Main engine extractions",
   "Both \"A\" and \"B\"",
   "Neither \"A\" nor \"B\""
  ],
  "definitions": "- Spray attemperator: Answer \"Spray attemperator\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Main engine extractions: Answer \"Main engine extractions\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Both \"A\" and \"B\": Answer \"Both \"A\" and \"B\"\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Neither \"A\" nor \"B\": Answer \"Neither \"A\" nor \"B\"\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q3e272eb42b",
  "kind": "choice",
  "text": "The absence of severe phenylketonuria (PKU) in both Polynesians and Southeast Asians is consistent with the lack of PAH haplotypes 2 and 3, on which the severe <e>PKU</e> mutants have arisen among Caucasians..",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"PKU\" (marked <e>) in this sentence?",
  "options": [
   "specific disease",
   "modifier",
   "composite mention",
   "disease class"
  ],
  "definitions": "- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders')."
 },
 {
  "qid": "qdb1d0aea41",
  "kind": "yes/no",
  "text": "Wikipedia article: Pierre de Fermat\nEvidence: French sculptor Théophile Barrau made a marble statue named Hommage à Pierre Fermat as a tribute to Fermat, now at the Capitole de Toulouse.\nClaim: Pierre de Fermat has an esteemed place of education dubbed in his honor.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence supports the claim: read together, the evidence sentences back up everything the claim states, directly or by simple inference (dates, numbers, paraphrase), and nothing in them contradicts it.\n- no: The evidence refutes the claim: the evidence sentences contradict the claim or at least one detail in it, directly or by simple inference (dates, numbers, paraphrase), showing it is false."
 },
 {
  "qid": "qe72ef048d4",
  "kind": "yes/no",
  "text": "NWS Storm Data tornado entry (May 2009, Lee County, Mississippi). Survey: path length 0.1 miles; maximum path width 25 yards.\n\nA tornado briefly touched down north of Eggville on County Road 1451. Some trees were damaged.",
  "question": "Based on this National Weather Service storm-survey narrative, which Enhanced Fujita (EF) rating was assigned to the tornado?\nIs it wrong to answer \"EF0\"?",
  "definitions": "- EF0: Estimated 3-second gust 65-85 mph: light damage such as shingles or siding peeled, gutters damaged, branches broken and shallow-rooted trees pushed over; some damage to at least one indicator is required.\n- EF1: Estimated gust 86-110 mph: moderate damage such as roofs badly stripped, mobile homes overturned or badly damaged, exterior doors lost, windows broken and many trees snapped or uprooted.\n- EF5: Estimated gust over 200 mph: incredible damage such as strong frame houses leveled and swept clean off their foundations, reinforced-concrete structures critically damaged, car-sized missiles thrown far.\n- EF2: Estimated gust 111-135 mph: considerable damage such as roofs torn off well-built houses, frame houses shifted on foundations, mobile homes destroyed, large trees snapped or uprooted, cars lifted.\n- EF3: Estimated gust 136-165 mph: severe damage such as entire stories of well-built houses destroyed, major damage to large buildings, trains overturned, trees debarked, heavy cars lifted and thrown."
 },
 {
  "qid": "q53277005e7",
  "kind": "yes/no",
  "text": "Partner's previous message: I am good. I am pretty excited for the trip this weekend. what about you?\nMessage: Very excited. It will be fun.",
  "question": "Which negotiation strategy does the Message use?\nIs the correct answer \"small talk\"?",
  "definitions": "- small talk: Rapport-building talk not about the deal itself, such as greetings, pleasantries, or chatting about the camping trip, weather or activities.\n- others' need: The speaker argues for an item by citing the needs of other people, such as family members, children or group members.\n- promoting coordination: The speaker promotes working together, for example an explicit promise to cooperate or a proposal framed as mutually beneficial for both sides.\n- undervaluing partner: The speaker undermines the partner's need for an item, suggesting they do not really require it or could get it elsewhere.\n- showing empathy: The speaker acknowledges the partner's personal situation positively or sympathetically, showing understanding or concern for their needs or circumstances."
 },
 {
  "qid": "q721cc6b194",
  "kind": "yes/no",
  "text": "Hi, that \"Multics Virtual Memory: Concepts and Design\" paper is already in the list of Multics papers (in the \"Further Reading - Technical Details) - it even has the same URL! It only lists one source, though - perhaps the second could be added as an \"(also here)\" link?",
  "question": "Is this request from a Wikipedia editor to another editor clearly polite?",
  "definitions": "- yes: At least 4 of 5 raters placed it on the polite side of the scale: courteous wording such as greeting, thanks, apology, praise, hedging ('I think', 'perhaps') or indirect asks ('would you mind', 'could you please').\n- no: At most 1 of 5 raters placed it on the polite side: the request is plain and neutral (bare questions or statements without courtesy markers) or blunt and impolite."
 },
 {
  "qid": "q69abe4071e",
  "kind": "yes/no",
  "text": "Wikipedia page: Douglas Lima\nSection: Mixed martial arts record\nTable:\n| Res. | Record | Opponent | Method | Event | Date | Round | Time | Location | Notes |\n| ... |\n| Win | 29–6 | Lorenz Larkin | Decision (unanimous) | Bellator NYC | June 24, 2017 | 5 | 5:00 | New York City, New York, United States | Defended the Bellator Welterweight World Championship. |\n| ... |\n| Win | 27–6 | Paul Daley | Decision (unanimous) | Bellator 158 | July 16, 2016 | 3 | 5:00 | London, England, United Kingdom |  |\n| ... |\n| Win | 13–4 | Eddie Hernandez | Submission (triangle choke) | Sin City Fight Club: Redline Grand Prix Opening Round | October 10, 2009 | 1 | 2:34 | Atlanta, Georgia, United States | 2010 REDLINE Middleweight Grand Prix Quarterfinal. |\n| ... |\n| Win | 9–1 | Daniel Douglas | Submission (rear-naked choke) | RMBB & PCF 1: HellRazor | October 16, 2007 | 1 | 0:28 | Denver, Colorado, United States |  |\n| ... |\n\nClaim: For the defense of his second title, Lima faced Daniel Douglas in Bellator NYC on June 24, 2017.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "qff6841842c",
  "kind": "yes/no",
  "text": "While FOE tries to scare people with references to \"extreme weather disasters,\" Idso and Taylor pointed to the fact that \"Global hurricane frequency is undergoing a long-term decline, with global hurricane and tropical storm activity at record lows during the past several years The United States is benefitting from the longest period in recorded history without a major hurricane strike. Tornado activity is in long-term decline, with major tornado strikes (F3 or higher) showing a remarkable decline in recent decades.\"",
  "question": "Does this paragraph make the contrarian climate claim that global warming is not happening?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that global warming is not happening: it denies that warming or its physical signs are happening: ice, permafrost or snow cover is not melting; we are heading into an ice age or global cooling; cold or snowy weather disproves warming; the climate has not warmed over recent decades; oceans are not warming; sea-level rise is exaggerated or not accelerating; extreme weather is not increasing, happened before or is not linked to climate change.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that global warming is not happening."
 },
 {
  "qid": "q9b2cc4c701",
  "kind": "yes/no",
  "text": "Sentence from a New York Times opinion article: Portugal's Prime Minister, Anibal Cavaco Silva, presides over the Council of Ministers, the countries' delegates who set policy.",
  "question": "How positive or negative is the sentiment this text expresses, as a typical reader would rate its intensity?\nIs it wrong to answer \"somewhat negative\"?",
  "definitions": "- somewhat negative: Mildly to moderately negative (rated -1 or -2): a clear but restrained complaint, worry, disappointment or criticism, or negativity softened by hedges or offset by minor positives.\n- neutral: No net sentiment (rated 0): factual, descriptive or procedural text, questions without evaluative tone, or positives and negatives that cancel out.\n- very negative: Strongly or extremely negative (rated -3 or -4 on a -4..+4 scale): intense anger, disgust, despair, harsh criticism or insults, often intensified by boosters, capitals or exclamation marks.\n- somewhat positive: Mildly to moderately positive (rated +1 or +2): clear but restrained approval, satisfaction, hope or praise, or positivity softened by hedges ('kind of good') or mixed with minor negatives.\n- very positive: Strongly or extremely positive (rated +3 or +4): intense enthusiasm, delight, love or superlative praise, often with boosters, capitals, exclamation marks or emoticons."
 },
 {
  "qid": "q1e7cefead1",
  "kind": "yes/no",
  "text": "Request:\nWrite $\\frac{3}{20}$ as a decimal.\n\nResponse:\nI know that fractions are equivalent to dividing the numerator by the denominator, so $\\frac{3}{20}$ is the same as $3 \\div 20$.\nTo divide by 20, I can think of moving the decimal point two places to the left, since 20 is 10 times 10, and dividing by 10 is the same as moving the decimal point one place to the left.\nSo, starting from 3, I move the decimal point two places to the left and get 0.03.\nThis means that $\\frac{3}{20}$ is equal to 0.03 as a decimal.\n# Answer\n\n0.03",
  "question": "Is the response fully correct and does it satisfy every explicit requirement of the request?"
 },
 {
  "qid": "qb493922b43",
  "kind": "yes/no",
  "text": "Situation: Ever Present Ex Wife Has to Move on With Her Life\nAction being judged: Moving on after a divorce.",
  "question": "Is the action being judged wrong according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); a merely unusual or selfish-sounding action is not wrong unless it is bad."
 },
 {
  "qid": "qb457332405",
  "kind": "yes/no",
  "text": "Infobox:\nTitle: Vertigo\nDirected by: Alfred Hitchcock\nProduced by: Alfred Hitchcock\nScreenplay by: Alec Coppel, Samuel Taylor\nBased on: D'entre les morts , by Pierre Boileau, Thomas Narcejac\nStarring: James Stewart, Kim Novak, Barbara Bel Geddes, Tom Helmore, Henry Jones\nMusic by: Bernard Herrmann\nCinematography: Robert Burks\nEdited by: George Tomasini\nProductioncompany: Alfred J. Hitchcock Productions\nDistributed by: Paramount Pictures\nRelease date: May 9, 1958 (1958-05-09)\nRunning time: 128 minutes\nCountry: United States\nLanguage: English\nBudget: $2.5 million\nBox office: $7.3 million\n\nHypothesis: Cinematography of Vertigo is done by Bernard Herrmann",
  "question": "Treating the infobox as up to date and using only it plus facts most people know, is the hypothesis definitely false?",
  "definitions": "- yes: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- no: The hypothesis is not shown to be false: either the infobox confirms it, or it concerns details the infobox does not cover, so it may or may not be true."
 },
 {
  "qid": "qf864912a29",
  "kind": "choice",
  "text": "I'm sure the women in your family are sluts. Probably why you have such a twisted sense of values.",
  "question": "This post is sexist. Which broad category of sexism does it fall under?",
  "options": [
   "Class W",
   "Class H",
   "Class T",
   "Class L"
  ],
  "definitions": "- Class W: The post threatens women or states plans to harm them, or incites and encourages others to inflict serious harm or violence on women.\n- Class H: The post explicitly demeans women: derogatory descriptions, aggressive or emotive attacks, dehumanising comparisons or overt sexual objectification.\n- Class T: The post shows implicit or subtle sexism: casual gendered slurs, stereotypes or claims of innate gender differences, backhanded compliments, or condescending advice.\n- Class L: The post denies or justifies sexist treatment: supporting mistreatment of individual women, or denying or justifying discrimination against women as a group, including male-victimhood arguments."
 },
 {
  "qid": "qde1318e52b",
  "kind": "choice",
  "text": "He is inspired by the new openness here.",
  "question": "Which emotion does this movie subtitle line express?",
  "options": [
   "anger",
   "anticipation",
   "disgust",
   "fear",
   "joy",
   "sadness",
   "surprise",
   "trust"
  ],
  "definitions": "- anger: The speaker shows annoyance, rage, hostility or irritation toward someone or something, for example through insults, threats, shouting or aggressive demands.\n- anticipation: The speaker looks ahead to something expected: interest, eagerness, planning, curiosity, vigilance or expectation about what will or should happen next, without fear about it.\n- disgust: The speaker shows revulsion, contempt, loathing, disdain or weary boredom toward something seen as gross, offensive, distasteful, worthless or morally repugnant.\n- fear: The speaker shows fright, worry, anxiety, alarm or a sense of threat or danger to themselves or others.\n- joy: The speaker shows happiness, delight, serenity, amusement, pleasure, pride or excitement about something good that is happening or has happened.\n- sadness: The speaker shows sorrow, grief, disappointment, regret, loneliness, hurt or pensiveness about a loss or something bad.\n- surprise: The speaker reacts to something unexpected or just discovered with amazement, astonishment, shock, disbelief or sudden realisation, often as an exclamation or incredulous question.\n- trust: The speaker shows acceptance, agreement, confidence, reliance, reassurance, admiration or faith in someone or something, for example making a deal, a promise or a vouching remark."
 },
 {
  "qid": "qc31c114afb",
  "kind": "choice",
  "text": "Tweet: I am listening to Bonnie Raitt - Since I Fell For You",
  "question": "How positive or negative is the sentiment this text expresses, as a typical reader would rate its intensity?",
  "options": [
   "Option R",
   "Option X",
   "Option A",
   "Option U",
   "Option S"
  ],
  "definitions": "- Option R: Strongly or extremely negative (rated -3 or -4 on a -4..+4 scale): intense anger, disgust, despair, harsh criticism or insults, often intensified by boosters, capitals or exclamation marks.\n- Option X: Mildly to moderately negative (rated -1 or -2): a clear but restrained complaint, worry, disappointment or criticism, or negativity softened by hedges or offset by minor positives.\n- Option A: No net sentiment (rated 0): factual, descriptive or procedural text, questions without evaluative tone, or positives and negatives that cancel out.\n- Option U: Mildly to moderately positive (rated +1 or +2): clear but restrained approval, satisfaction, hope or praise, or positivity softened by hedges ('kind of good') or mixed with minor negatives.\n- Option S: Strongly or extremely positive (rated +3 or +4): intense enthusiasm, delight, love or superlative praise, often with boosters, capitals, exclamation marks or emoticons."
 },
 {
  "qid": "q4816d106c2",
  "kind": "yes/no",
  "text": "Company annual report excerpt\nTable:\n|  | Year Ended December 31, |  |  |\n|  | 2019 | 2018 | 2017 |\n| U.S. | $176.4 | $138.9 | $180.6 |\n| Foreign | (50.0) | (65.9) | (73.8) |\n| Incomefromcontinuingoperationsbeforeincometaxes | $126.4 | $73.0 | $106.8 |\nText:\nBenefit for Income Taxes\nOur benefit for income taxes includes U.S. federal, state and foreign income taxes. The domestic and foreign components of our income from continuing operations before income taxes were as follows:\n\nHypothetical question: What would be the change in the average U.S. income from continuing operations before income taxes between 2017-2018 and 2018-2019 if 2017 U.S. income from continuing operations before income taxes was $190?\nProposed answer: -2.1",
  "question": "Using the report's table and text together with the question's hypothetical assumption, is the proposed answer correct?",
  "definitions": "- yes: The proposed answer is what the figures give after applying the question's hypothetical change (the assumed value replaces the reported one): same value at the precision shown, same sign, same unit or scale, and for lists exactly the right items.\n- no: The proposed answer is not the hypothetical result: it ignores the assumption and uses the reported figure, uses a wrong figure or base, sums instead of averaging, has the wrong sign or scale, or lists the wrong items."
 },
 {
  "qid": "q45ea003777",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Jiangsu\nSentence: Jiangsu (江苏; formerly romanized Kiangsu) is an eastern-central coastal province of the People's Republic of China.\n\nClaim: Pei County is in the Jiangsu province of South Korea, formerly romanized Kiangsu, with a population of over 1.3 million people.",
  "question": "Does the evidence refute the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows at least one part of the claim is false, directly or by simple reasoning such as counting, comparing or adding.\n- no: The evidence does not show the claim is false: it either supports the claim or does not settle it (not enough information counts as no)."
 },
 {
  "qid": "qc665e714eb",
  "kind": "yes/no",
  "text": "Wikipedia page: Super Bowl XXXVII\nSection: Individual leaders\nTable:\n| Raiders Passing | Raiders Passing | Raiders Passing | Raiders Passing | Raiders Passing | Raiders Passing |\n|  | C/ATT1 | Yds | TD | INT | Rating |\n| Rich Gannon | 24/44 | 272 | 2 | 5 | 48.9 |\n| Raiders Rushing | Raiders Rushing | Raiders Rushing | Raiders Rushing | Raiders Rushing | Raiders Rushing |\n|  | Car2 | Yds | TD | LG3 | Yds/Car |\n| Charlie Garner | 7 | 10 | 0 | 4 | 1.43 |\n| Zack Crockett | 2 | 6 | 0 | 4 | 3.00 |\n| Rich Gannon | 2 | 3 | 0 | 2 | 1.00 |\n| Raiders Receiving | Raiders Receiving | Raiders Receiving | Raiders Receiving | Raiders Receiving | Raiders Receiving |\n|  | Rec4 | Yds | TD | LG3 | Target5 |\n| Charlie Garner | 7 | 51 | 0 | 9 | 11 |\n| Jerry Rice | 5 | 77 | 1 | 48t | 8 |\n| Doug Jolley | 5 | 59 | 0 | 25 | 7 |\n| Jerry Porter | 4 | 62 | 1 | 39t | 9 |\n| Tim Brown | 1 | 9 | 0 | 9 | 2 |\n| Jon Ritchie | 1 | 7 | 0 | 7 | 1 |\n| Tyrone Wheatley | 1 | 7 | 0 | 7 | 1 |\n| Marcus Knight | 0 | 0 | 0 | 0 | 3 |\n\nClaim: Gannon finished the game 24 out of 44 with 272 yards and 2 touchdowns, and intercepted 5 times in the Super Bowl.",
  "question": "Is the claim contradicted by the table?",
  "definitions": "- yes: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name).\n- no: The claim is supported: every fact matches the table and its page and section titles, with each value paired with the right row and column."
 },
 {
  "qid": "qf86e16eed7",
  "kind": "yes/no",
  "text": "Majority of promised Dakota and Keystone pipeline jobs expected to be temporary.",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "q53d0804c8e",
  "kind": "yes/no",
  "text": "Situation: I absolutely hate the fact that I was circumcised. Most of the times I think about it, I get violent and eventually break down into tears. I even avoid dating because I see no point.\nAction being judged: Getting violent toward others.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qdb4b4e382f",
  "kind": "yes/no",
  "text": "Donald was taking medication for pain but Christopher knew it was not because _ was injury free.\n\nThe blank (_) stands for one of two candidates: \"Donald\" or \"Christopher\".",
  "question": "Does the blank (_) in the sentence stand for \"Donald\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "q1d9113d3bf",
  "kind": "yes/no",
  "text": "Situation: Daughter's Obsessive Stalker Ratchets Up His Accusations\nAction being judged: Accusing people of things you have no proof of.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qb11539a58b",
  "kind": "yes/no",
  "text": "Statement 1: Going for a haircut is for grooming\nStatement 2: Going for a haircut is for eating",
  "question": "Of these two statements, does Statement 1 go against common sense?",
  "definitions": "- yes: The asked-about statement is the one of the two that goes against common sense: some part of it makes it impossible, absurd or clearly contrary to how the world works, while the other statement is normal.\n- no: The asked-about statement is the sensible one of the two; it is the other statement that goes against common sense."
 },
 {
  "qid": "q29e6e8157f",
  "kind": "yes/no",
  "text": "Evidence (from the abstract of a scientific article):\nRhesus macaques reinfected with the identical SARS-CoV-2 strain during the early recovery phase of the initial SARS-CoV-2 infection did not show detectable viral dissemination, clinical manifestations of viral disease, or histopathological changes.\n\nClaim: Small studies have shown that one bout of the coronavirus seems to protect rhesus macaques from contracting it again.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence sentences back up the claim's central assertion, directly or by simple inference: same direction of effect, compatible numbers (allowing ordinary rounding) and a compatible population, even if the scientific wording is hedged ('suggests', 'is consistent with').\n- no: The evidence contradicts the claim or a decisive detail of it (a reversed direction, a wrong number, percentage, quantifier such as 'all' or 'only', a negation, or the wrong group), so it does not support the claim as stated."
 },
 {
  "qid": "qb31288b78c",
  "kind": "yes/no",
  "text": "A 13-year-old girl presents with a 4-week history of unrelenting cough, night sweats, and fever. No known past medical history and no current medications. The patient recently immigrated to the country from a rural town in northern India. Vaccination status is unknown. Her temperature is 38.5°C (101.3°F), pulse is 115/min, blood pressure is 95/65 mm Hg, and respiratory rate is 22/min. Physical examination is significant for decreased breath sounds in the right upper lobe and multiple right cervical lymphadenopathies. A chest radiograph reveals multiple cavitations in the right upper lobe and right hilar lymphadenopathy. A sputum culture shows acid-fast bacilli. Which of the following compounds must be included in addition to the recommended antimicrobial therapy in this patient?\n\nAnswer choices:\nA. Thiamine\nB. Riboflavin\nC. Pyridoxine\nD. Niacin\nE. Folic acid\n\nProposed answer: C. Pyridoxine",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "qd6b18528f4",
  "kind": "yes/no",
  "text": "Situation: They looked through every book they could find, and couldn't decide.\nAction being judged: Doing research before you make a decision.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "qe4509e0a17",
  "kind": "yes/no",
  "text": "Customer: Could you give me the time of the flight?\nAssistant: Departs at 6:25 p.m.\nCustomer: Is it a nonstop or layover?",
  "question": "In the customer's last message, is \"nonstop\" a mention of the number of stops or layovers for this flight search?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out (e.g. 'not horror' still mentions a genre).\n- no: The quoted phrase refers to a different detail of the search (e.g. the destination rather than the departure city, the return rather than the outbound date, or the meal rather than the cuisine)."
 },
 {
  "qid": "q33a3fb589a",
  "kind": "yes/no",
  "text": "Customer: Hi, I'd like to see a movie but need some help ordering.\nAgent: Sure thing. How many are going?\nCustomer: We have 3 please.\nAgent: Is that children and adults?\nCustomer: No, just 3 adults.\nAgent: What city are you in?\nCustomer: I'm in Austin, TX please.\nAgent: Which movie are you interested in?\nCustomer: I want to see Dolittle please.\nAgent: What time would you like to go?\nCustomer: I would like to go at 11:45 PM please.\nAgent: Do you have a particular theater in mind?\nCustomer: I would like to go to the Regal Westgate.\nAgent: I'm sorry there are no tickets for Dolittle at that time. Is there another time you'd like?\nCustomer: How about 9:15 PM?\nAgent: I'm sorry I don't have availability at that time.\nCustomer: Can you please check the Regal Metropolitan for those same times?\nAgent: I'm very sorry those times aren't available there either for 3 tickets.\nCustomer: Okay, I guess I'll skip for the movie tonight.\nAgent: I'm sorry. Can I help you perhaps find another day?\nCustomer: No thanks.\nAgent: Have a good night.",
  "question": "By the end of this conversation, has the customer actually bought movie tickets?",
  "definitions": "- yes: The agent completes a ticket purchase for the customer within this conversation, even if earlier choices were unavailable or changed along the way.\n- no: No tickets are bought in this conversation: the customer declines or postpones, nothing suitable is available or open, or the purchase is only saved or scheduled for later."
 },
 {
  "qid": "qbda1aa524a",
  "kind": "yes/no",
  "text": "Multifuel media was smelled smoldering. We immediately began searching for source. Equip. was removed from service. Found source in dust collection equip. washed out bin with water. Called as soon as we were confident it was out.",
  "question": "Which MSHA accident classification fits the circumstances that most directly caused this mine accident?\nIs the correct answer \"dust disease of the lungs\"?",
  "definitions": "- dust disease of the lungs: A lung disease from dust: black lung (coal workers' pneumoconiosis), silicosis, asbestosis or another pneumoconiosis.\n- fire: An unplanned fire or burning of equipment, belt, cable, fuel or mine material, not an ignition or explosion of gas or dust.\n- explosives and breaking agents: Accidents with blasting or breaking agents: detonations, premature or misfired shots, flyrock from a blast, or handling explosives.\n- hoisting: Accidents involving shaft or slope hoisting equipment: hoists, cages, skips, elevators, buckets and their ropes and controls.\n- handling of materials: Injury while lifting, carrying, pushing, pulling, shoveling, loading or otherwise moving materials or supplies by hand, including strains and objects dropped while handled.\n- electrical: Contact with or exposure to electric current (energized wires, cables or equipment), including shock, electrocution and electrical or arc burns."
 }
]
