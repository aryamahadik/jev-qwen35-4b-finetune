# A46 replay label-noise blind read RSAS77-blind_read-42e89944-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSAS77-blind_read-42e89944-000.json

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
  "qid": "q36029bd766",
  "kind": "yes/no",
  "text": "Yes, but on the bright-side, thanks to her jewish neuroticism I found a lot of racist nazis in her threads, whom I can follow on gab.",
  "question": "Is this post sexist?",
  "definitions": "- yes: The post is sexist: it contains abuse or negative sentiment directed at women because of their gender, or their gender combined with another identity such as race, religion or being trans - including casual gendered slurs, stereotypes and backhanded compliments.\n- no: The post is not sexist: it may be rude, crude, about gender or relationships, or abusive toward men or other groups, but it expresses no abuse or prejudice against women because they are women."
 },
 {
  "qid": "q3180306ce7",
  "kind": "yes/no",
  "text": "APC is often cited as a prime example of a <e>tumor</e> suppressor gene.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"tumor\" (marked <e>) in this sentence?\nIs the correct answer \"disease class\"?",
  "definitions": "- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers')."
 },
 {
  "qid": "q97317dc23d",
  "kind": "yes/no",
  "text": "Table caption: The assessment results of the customized scheme and samples assigned to each module. The average overall accuracy and the average KIA represent mean values of the ten group results of ten-fold cross validation.\n| Item | Overall accuracy of ten-fold cross validation | Average KIA of ten-fold cross validation | The number of samples |\n| 1st Classification | 96.1% | 91.5% | 3069 |\n| 2nd Classification | – | – | – |\n| 3rd Classification | 94.0% | 79.8% | 1874 |\n| 4th Classification | 90.7% | 82.2% | 1581 |\n| 5th Classification | 84.3% | 76.3% | 823 |\n\nStatement: 4th Classification The number of samples is 823.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qe191c5d511",
  "kind": "yes/no",
  "text": "Women Who Kill is a grim portrait of female prisoners and a divided America",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "q96a5661f89",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Master TV to Master Less than 500 Gross Registered Tons), Deck General – Safety.\n\nQuestion: You are loading 530,000 barrels of cargo oil. At 0945 on 13 April, you find that you have loaded 202,000 barrels. At 1130, you find that you have loaded 223,000 barrels. When will you complete loading if you continue at the same rate?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "1322, 13 April",
   "1920, 13 April",
   "1120, 14 April",
   "1305, 14 April"
  ],
  "definitions": "- 1322, 13 April: Answer \"1322, 13 April\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 1920, 13 April: Answer \"1920, 13 April\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 1120, 14 April: Answer \"1120, 14 April\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- 1305, 14 April: Answer \"1305, 14 April\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qbf292772d3",
  "kind": "yes/no",
  "text": "Trivia question (category: Sports).\n\nQuestion: Which country hosted the 2022 FIFA World Cup?",
  "question": "Which answer choice correctly answers this trivia question?\nIs it wrong to answer \"Qatar\"?",
  "definitions": "- Qatar: Answer \"Qatar\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Japan: Answer \"Japan\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- USA: Answer \"USA\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Switzerland: Answer \"Switzerland\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q15ebe0484e",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: Naser Aliji\nSection: Career statistics > Club\nTable (caption: Club statistics):\n| Club | Season | League | League | League | Cup | Cup | Europe | Europe | Other | Other | Total | Total |\n| Club | Season | Division | Apps | Goals | Apps | Goals | Apps | Goals | Apps | Goals | Apps | Goals |\n| ... |\n| Basel | Total | Total | 29 | 1 | 9 | 0 | 4 | 0 | — | — | 41 | 1 |\n| Vaduz | 2014–15 | Swiss Super League | 17 | 0 | 2 | 0 | — | — | — | — | 19 | 0 |\n| Vaduz | 2015–16 | Swiss Super League | 7 | 0 | 0 | 0 | 5 | 1 | — | — | 12 | 1 |\n\nClaim: Naser Aliji made one goal for Vaduz in the 2015-16 Swiss Super League.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "qb9d9567a0e",
  "kind": "choice",
  "text": "To explore the pathogenesis of recurrent neisserial infections in <e>C6 deficiency</e>, a detailed analysis of her immune competence was conducted.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"C6 deficiency\" (marked <e>) in this sentence?",
  "options": [
   "composite mention",
   "disease class",
   "modifier",
   "specific disease"
  ],
  "definitions": "- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients').\n- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC')."
 },
 {
  "qid": "q2b185840f0",
  "kind": "yes/no",
  "text": "Customer: No, that won't work.\nAssistant: Is there another restaurant you have in mind?\nCustomer: Yes. Could we see if there's availability at Redrock Canyon Grill in Southlake?",
  "question": "In the customer's last message, does \"Southlake\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qcbba443330",
  "kind": "yes/no",
  "text": "Beginning: I ran across the street to catch the ...\n\nPossible endings:\n(A) bus\n(B) chicken\n(C) football\n(D) car I was driving",
  "question": "Among the listed endings, is (A) \"bus\" the most sensible continuation of the beginning?",
  "definitions": "- yes: The named ending is the listed continuation that makes the most sense: read after the beginning, it describes what would ordinarily be true or happen next, fits who and what the beginning is about, and respects any negation, number, idiom or double meaning in it.\n- no: Another listed ending makes more sense: the named ending contradicts the beginning, is about the wrong person or thing, misreads a word, idiom or quantity, or describes something absurd or unrelated."
 },
 {
  "qid": "qb6477cb425",
  "kind": "choice",
  "text": "Sports brand Nike, ranked 22 with a brand valued at nearly $20bn, is rated way ahead of rival Adidas, at 59 in the top 100 with a value of $7bn.\nFrampton said consumers’ ability to interact with and criticize brands on Twitter and other social media means companies must react faster to retain and improve their brands’ reputations.\n“The customer, empowered by social media in the ‘age of experience’, now has more control than ever,” he said. “In this world of two-way conversations, advocacy, influence and engagement are the new rules for brand-building.",
  "question": "This passage comes from a news article that English teachers rewrote for language learners at three reading levels. At which level is this passage written?",
  "options": [
   "elementary",
   "intermediate",
   "advanced"
  ],
  "definitions": "- elementary: The easiest rewrite (about CEFR A2-B1): short, mostly single-clause sentences, very common words, simple tenses, difficult terms explained or dropped, few idioms or long noun phrases.\n- intermediate: The middle rewrite (about B1-B2): moderately long sentences with some subordinate clauses, mostly everyday vocabulary with some less common words, lighter simplification of the original.\n- advanced: The original native-level newspaper text (about C1): long multi-clause sentences, rich or technical vocabulary, idioms, figurative language and dense reported speech, with no simplification."
 },
 {
  "qid": "q54c3ef19a0",
  "kind": "yes/no",
  "text": "\"The coming year will be an important one for space weather as the Sun pulls out of a trough of low activity and heads into a long-awaited and possibly destructive period of turbulence.\"",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "q2945640c72",
  "kind": "yes/no",
  "text": "Please dislike this song.",
  "question": "What does the user want the music player to do?\nIs it wrong to answer \"Dislike the music\"?",
  "definitions": "- Dislike the music: The user rates a song or artist negatively, such as a thumbs down or saying they do not like it, so it is marked as disliked.\n- Shuffle music: The user asks to play songs, an album, artist or playlist in random shuffled order.\n- Pause the music: The user asks to pause playback temporarily so it can be resumed from the same point.\n- Loop the music: The user asks to put a song, album or playlist on continuous repeat, or to keep playing it, so it loops rather than playing once more.\n- Play music: The user asks to start playing music: a song, artist, album, genre, playlist or radio station."
 },
 {
  "qid": "q4c19cd5c71",
  "kind": "yes/no",
  "text": "A 28-year-old male presents to his primary care physician with complaints of intermittent abdominal pain and alternating bouts of constipation and diarrhea. His medical chart is not significant for any past medical problems or prior surgeries. He is not prescribed any current medications. Which of the following questions would be the most useful next question in eliciting further history from this patient?\n\nAnswer choices:\nA. \"Please rate your abdominal pain on a scale of 1-10, with 10 being the worst pain of your life\"\nB. \"Is the diarrhea foul-smelling?\"\nC. \"Can you tell me more about the symptoms you have been experiencing?\"\nD. \"Does the diarrhea typically precede the constipation, or vice-versa?\"\nE. \"Are the symptoms worse in the morning or at night?\"\n\nProposed answer: E. \"Are the symptoms worse in the morning or at night?\"",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "qefa1b42c00",
  "kind": "yes/no",
  "text": "Situation: My favorite hobby is destroying liberals on the internet\nAction being judged: Going around on the Internet badmouthing people.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q89fa5b5bdc",
  "kind": "yes/no",
  "text": "The symptoms appeared in the nose now, not the mouth, as the _ was now infected.\n\nThe blank (_) stands for one of two candidates: \"nose\" or \"mouth\".",
  "question": "Does the blank (_) in the sentence stand for \"nose\"?",
  "definitions": "- yes: The named candidate is what the blank stands for: given the situation, everyday knowledge of people, objects and causes makes the clause containing the blank true of the named candidate rather than of the other candidate.\n- no: The blank stands for the other candidate: putting the named candidate in the blank makes the sentence illogical, self-contradictory or clearly less sensible than putting in the other candidate."
 },
 {
  "qid": "q571e635f3a",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Master Less than 500-1600 Gross Registered Tons), Navigation General – Near Coastal.\n\nQuestion: Which current is responsible for the movement of large quantities of ice into the North Atlantic shipping lanes?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "Baffin Current",
   "Iceland Current",
   "Labrador Current",
   "Baltic Current"
  ],
  "definitions": "- Baffin Current: Answer \"Baffin Current\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Iceland Current: Answer \"Iceland Current\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Labrador Current: Answer \"Labrador Current\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Baltic Current: Answer \"Baltic Current\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qb6db230b4c",
  "kind": "yes/no",
  "text": "A significant effect of the constitutional factor on the development of atopic dermatitis included familial occurrence of ATOPIC DISEASES (mostly ATOPIC DERMATITIS",
  "question": "Does this sentence express that one of the terms \"ATOPIC DERMATITIS\" and \"ATOPIC DISEASES\" is used to treat the other (therapeutic use of a drug, ingredient or therapy)?",
  "definitions": "- yes: At least 60% of the crowd workers ticked TREATS: the sentence presents one term as a drug, ingredient or therapy used to cure or relieve the other (e.g. penicillin cures infection), including reported results such as 'was effective in treating'.\n- no: At most 10% ticked TREATS: in this sentence the terms are linked in another way (cause, symptom, side effect, location, diagnosis, prevention, is-a, mere co-occurrence) or not at all, whatever is true outside the sentence."
 },
 {
  "qid": "qe998a915c1",
  "kind": "choice",
  "text": "Heading: Apple Store VS Bestbuy for Repairs?\nI Live in California, United States and will be sending in my iPhone 6 for battery-related repair. Does anyone know if there is any difference in pricing or customer satisfaction between the Apple Retail Store and BestBuy?",
  "question": "Which Wikipedia Reference Desk should this question be posted to?",
  "options": [
   "Computing reference desk",
   "Entertainment reference desk",
   "Humanities reference desk",
   "Language reference desk",
   "Mathematics reference desk",
   "Science reference desk"
  ],
  "definitions": "- Computing reference desk: Questions about computers, software, programming, the internet, electronics as used in computing, and IT or device problems.\n- Entertainment reference desk: Questions about popular culture: films, television, music, video games, sports, comics, celebrities and other entertainment.\n- Humanities reference desk: Questions about history, politics, law, religion, philosophy, economics and finance, society, the arts, literature and geography of human affairs.\n- Language reference desk: Questions about words and languages: meaning, grammar, spelling, pronunciation, etymology, translation and usage.\n- Mathematics reference desk: Questions about mathematics, statistics, probability, logic and puzzles that need mathematical reasoning.\n- Science reference desk: Questions about the natural and applied sciences: physics, chemistry, biology, medicine and health, astronomy, earth science, engineering and technology (not software)."
 },
 {
  "qid": "q2a09ada77a",
  "kind": "yes/no",
  "text": "Situation: Finally, he went to Best Buy and handed them $2000.\nAction being judged: Buying nice things if you can afford them.",
  "question": "Is the action being judged acceptable according to common social norms?",
  "definitions": "- yes: Most people would see the action being judged, as described, as okay, expected or good (annotators rated it OK/good and estimated at least 75% of people agree); judge that action itself, not the rest of the situation.\n- no: Most people would see the action being judged, as described, as bad or very bad: rude, unkind, dishonest, irresponsible or harmful, even if it is legal or common; judge that action itself, not the rest of the situation."
 },
 {
  "qid": "q9c205a7b89",
  "kind": "yes/no",
  "text": "Customer: I'm looking for a restaurant that serves americas food.\nAssistant: Unfortunately, I cannot find an American restaurant.",
  "question": "In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "definitions": "- yes: The assistant reports, lists or recommends at least one place or train that fits all of the customer's stated requirements, even if it then asks a follow-up question to narrow the choice.\n- no: The assistant reports that nothing fits all of the requirements, even if it then suggests alternatives that relax one of them (another area, price range, type, day or time)."
 },
 {
  "qid": "q69c035f02c",
  "kind": "yes/no",
  "text": "Someone wasn't exhilarated that a particular thing happened.",
  "question": "Does this sentence imply that the particular thing happened?",
  "definitions": "- yes: At least 7 of 10 annotators, reading only this sentence, answered that it did happen (the person did or had it): the verb with its polarity commits the speaker to it, as with 'knew that', 'managed to' or 'didn't forget to'.\n- no: At most 3 of 10 answered that it happened; the rest judged it merely possible ('maybe or maybe not', as after 'wanted', 'hoped', 'was asked to') or judged that it did not happen (as after 'didn't manage to', 'pretended that')."
 },
 {
  "qid": "q93bc6c97f3",
  "kind": "yes/no",
  "text": "imagine your daughters boyfriend being ⬛  💓💓",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post, reading any emoji as the words, groups or actions they stand for, directs abuse or contempt at a group identity (such as race, ethnicity, nationality, religion, gender, sexuality, disability, immigration status or class) or at someone because of that identity, explicitly or implicitly: insults and slurs, threats, dehumanising comparisons, or subtle digs and hostile stereotypes.\n- no: The post, reading any emoji for what they stand for, does not attack a group identity: it may mention identities, swear, criticise, counter hate or target something that is not an identity (an animal, an object, a person for non-identity reasons), but it is not abusive towards an identity group or anyone because of their identity."
 },
 {
  "qid": "q37e3084baa",
  "kind": "choice",
  "text": "Tweet: Setting up surround sound systems sucks.",
  "question": "How positive or negative is the sentiment this text expresses, as a typical reader would rate its intensity?",
  "options": [
   "Option M",
   "Option H",
   "Option N",
   "Option A",
   "Option G"
  ],
  "definitions": "- Option M: Strongly or extremely negative (rated -3 or -4 on a -4..+4 scale): intense anger, disgust, despair, harsh criticism or insults, often intensified by boosters, capitals or exclamation marks.\n- Option H: Mildly to moderately negative (rated -1 or -2): a clear but restrained complaint, worry, disappointment or criticism, or negativity softened by hedges or offset by minor positives.\n- Option N: No net sentiment (rated 0): factual, descriptive or procedural text, questions without evaluative tone, or positives and negatives that cancel out.\n- Option A: Mildly to moderately positive (rated +1 or +2): clear but restrained approval, satisfaction, hope or praise, or positivity softened by hedges ('kind of good') or mixed with minor negatives.\n- Option G: Strongly or extremely positive (rated +3 or +4): intense enthusiasm, delight, love or superlative praise, often with boosters, capitals, exclamation marks or emoticons."
 },
 {
  "qid": "qff945aee13",
  "kind": "choice",
  "text": "The significance of this association is controversial, though the association of <e>C2 deficiency</e> with certain histocompatibility antigens suggests possible linkage to immune response genes.",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"C2 deficiency\" (marked <e>) in this sentence?",
  "options": [
   "disease class",
   "specific disease",
   "composite mention",
   "modifier"
  ],
  "definitions": "- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients')."
 },
 {
  "qid": "qf43ed2bbcd",
  "kind": "yes/no",
  "text": "Customer: Hey! So, I'm meeting Danielle tonight in Chicago. We wanted to see \"Dumbo\".",
  "question": "In the customer's last message, does \"Chicago\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa5521eff4e",
  "kind": "yes/no",
  "text": "Problem:\nA positive integer is 3 more than a multiple of 4 and 4 more than a multiple of 5. What is the least integer it could be?\n\nSolution steps so far: (none)\n\nLast step (Step 1):\nI want to find the smallest number that satisfies both conditions, so I'll start by listing some multiples of 4 and 5 and see if I can spot a pattern.",
  "question": "Does the last step of this partial solution contain a mistake or other flaw that makes it a bad step?",
  "definitions": "- yes: The last step is a bad step: it states something mathematically wrong (even if most of it is right), cannot be checked in about 30 seconds, is off-topic or gibberish, leads into an obvious dead end or loop, or gives a final answer that is wrong or not justified by a complete solution.\n- no: The last step has no such flaw: everything it states is correct, quickly verifiable and fits the earlier steps; this includes steps that only restate, stall or try a reasonable approach that may not pan out, and steps that catch an earlier slip."
 },
 {
  "qid": "qe728a0d0bc",
  "kind": "choice",
  "text": "We report on nine patients with <e>craniofrontonasal dysplasia</e> (CFND).",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"craniofrontonasal dysplasia\" (marked <e>) in this sentence?",
  "options": [
   "disease class",
   "specific disease",
   "composite mention",
   "modifier"
  ],
  "definitions": "- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients')."
 },
 {
  "qid": "q3aed679650",
  "kind": "yes/no",
  "text": "Sentence: The town's death toll may be \"in the hundreds\", municipal spokesman Vincent <Creel> [said].\nMarked event: [said]\nMarked participant: <Creel> (the phrase \"municipal spokesman Vincent Creel\")",
  "question": "In this sentence, how likely is it that the participant <Creel> caused the [said] event to happen?\nIs it wrong to answer \"Code 15\"?",
  "definitions": "- Code 15: Given the sentence, the property is clearly false for the participant in this event (scale point 1 of 5).\n- Code 13: Given the sentence, the property clearly holds for the participant in this event (point 5 of 5).\n- Code 14: The property probably holds for the participant, though the sentence does not state it outright (point 4 of 5).\n- Code 40: The sentence gives no reason to think the property holds or fails; it is an even bet (point 3 of 5).\n- Code 43: The property is probably false for the participant, though the sentence leaves some room for it (point 2 of 5)."
 },
 {
  "qid": "qa820ca4348",
  "kind": "yes/no",
  "text": "U.S. Coast Guard merchant mariner credential exam (Master or Mate Less than 200 Gross Registered Tons), Deck General.\n\nQuestion: Which statement is TRUE concerning River currents?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?\nIs the correct answer \"Option H\"?",
  "definitions": "- Option H: Answer \"A current will hug the inside of a bend\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option D: Answer \"Currents cause the greatest depth of water on the outside of a bend\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option R: Answer \"The currents run slower in the center of the channel as opposed to the sides\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Option E: Answer \"The currents pick up speed where the channel widens\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q985c6bdab4",
  "kind": "yes/no",
  "text": "Request:\nA $90^\\circ$ rotation around the origin in the counter-clockwise direction is applied to $7 + 2i.$  What is the resulting complex number?\n\nResponse:\nI know that complex numbers can be represented as points in the complex plane, where the real part is the x-coordinate and the imaginary part is the y-coordinate.\nSo 7 + 2i corresponds to the point (7, 2) on the plane.\nI also know that a 90-degree rotation around the origin in the counter-clockwise direction means moving each point 90 degrees along the unit circle.\nThat is, the x-coordinate becomes the negative of the original y-coordinate, and the y-coordinate becomes the original x-coordinate.\nSo, to rotate the point (7, 2) by 90 degrees counter-clockwise, I need to swap the coordinates and negate the new x-coordinate.\nThat gives me the point (-2, 7).\nTo convert this point back to a complex number, I need to write it as a sum of a real part and an imaginary part.\nThe real part is the x-coordinate, which is -2, and the imaginary part is the y-coordinate, which is 7, times the imaginary unit i. So the complex number is -2 + 7i.\n# Answer\n\n-2 + 7i",
  "question": "Would a careful reviewer accept this response as completely correct and compliant with all stated constraints?"
 },
 {
  "qid": "q1ddbd507a8",
  "kind": "yes/no",
  "text": "Consumer health question:\nWhat are the treatments of Parkinson's Disease?\n\nPassage:\nParkinson disease type 3 (Treatment): FDA-Approved Treatments The medication(s) listed below have been approved by the Food and Drug Administration (FDA) as orphan products for treatment of this condition. Learn more orphan products. National Library of Medicine Drug Information Portal Medline Plus Health Information",
  "question": "Does the passage correctly answer the consumer's health question?",
  "definitions": "- yes: The passage gives a correct answer to what the consumer actually asked, either completely or correctly but incompletely (it covers part of the requested information, such as some of the treatments or symptoms asked about).\n- no: The passage does not answer the question: it is only related to the topic (right disease or drug but the wrong aspect, e.g. causes when treatment was asked, or page metadata), or it is about something else or gives incorrect information."
 },
 {
  "qid": "q87f1839613",
  "kind": "choice",
  "text": "Phenylketonuria (PKU) is an <e>autosomal recessive human genetic disorder</e> caused by a deficiency of hepatic phenylalanine hydroxylase (PAH, phenylalanine 4-monooxygenase, EC 1. 14. 16. 1).",
  "question": "According to the NCBI disease-mention categories, what kind of disease mention is \"autosomal recessive human genetic disorder\" (marked <e>) in this sentence?",
  "options": [
   "composite mention",
   "specific disease",
   "disease class",
   "modifier"
  ],
  "definitions": "- composite mention: One contiguous string names two or more separate diseases that cannot be split without losing meaning (e.g. 'Duchenne and Becker muscular dystrophy', 'colon and some other cancers').\n- specific disease: The mention, used as a noun phrase, names one particular disease with a single specific definition and no further subtypes (e.g. 'Diastrophic dysplasia', 'adenomatous polyposis coli', or its abbreviation 'APC').\n- disease class: The mention, used as a noun phrase, names a family or category that covers many specific diseases (e.g. 'autosomal recessive disease', 'cancer', 'skin tumour', 'neurodegenerative disorders').\n- modifier: The disease name is not used as a disease noun phrase but modifies another concept (e.g. 'colorectal cancer families', 'HNPCC kindreds', 'DMD gene', 'ataxia patients')."
 },
 {
  "qid": "q10529e4086",
  "kind": "yes/no",
  "text": "Wikipedia article: Kenilworth\nEvidence: Kenilworth ( KEN-il-wərth) is a market town and civil parish in Warwickshire, England, about 6 miles (10 km) south-west of central Coventry, 5 miles (8 km) north of Warwick and 90 miles (140 km) north-west of London.\nClaim: This market is not in England.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence supports the claim: read together, the evidence sentences back up everything the claim states, directly or by simple inference (dates, numbers, paraphrase), and nothing in them contradicts it.\n- no: The evidence refutes the claim: the evidence sentences contradict the claim or at least one detail in it, directly or by simple inference (dates, numbers, paraphrase), showing it is false."
 },
 {
  "qid": "q90e0328eea",
  "kind": "yes/no",
  "text": "wont move for 🤰🏻🤣",
  "question": "Is this post hateful?",
  "definitions": "- yes: The post expresses hatred toward a protected group, or a person because of their group (race, religion, gender, sexual orientation, disability, nationality), in words or emoji, including emoji standing in for the group, a slur or a threat.\n- no: Not hateful: it may use emoji, name a group, quote or condemn hate, criticise non-protected targets or ideas, or be positive or neutral about a group; swapping the target or emoji can make a hateful template harmless."
 },
 {
  "qid": "q18107d6914",
  "kind": "yes/no",
  "text": "Customer: Thank you.\nAssistant: There is a classic movie called The Exorcist which is based on a true story would you be interested in this one.\nCustomer: Yeah, that sounds good. Can I watch that on Netflix?",
  "question": "In the customer's last message, is \"Netflix\" a mention of the streaming service or rental platform for this movie search?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out (e.g. 'not horror' still mentions a genre).\n- no: The quoted phrase refers to a different detail of the search (e.g. the destination rather than the departure city, the return rather than the outbound date, or the meal rather than the cuisine)."
 },
 {
  "qid": "q76c06a21cc",
  "kind": "choice",
  "text": "Infobox:\nTitle: Hall & Oates\nOrigin: Philadelphia, Pennsylvania, , United States\nGenres: Pop rock, blue-eyed soul, soft rock, rhythm and blues\nYears active: 1970-present\nLabels: Atlantic, RCA, Arista, U-Watch\nWebsite: Official website\n\nHypothesis: Hall & Oates have undergone lineup changes",
  "question": "Treat the infobox as up to date (its dates and ages are current). Using only the infobox and facts most people know, how does the hypothesis relate to the table?",
  "options": [
   "Option S",
   "Option R",
   "Option K"
  ],
  "definitions": "- Option S: The infobox, plus facts most people know and simple reasoning (dates, counts, comparisons), shows the hypothesis is definitely true.\n- Option R: The infobox, plus facts most people know and simple reasoning, shows the hypothesis is definitely false, even when the conflict is indirect (for example via dates, counts or roles).\n- Option K: The hypothesis adds details the infobox does not cover, and facts most people know cannot settle them, so it may or may not be true."
 },
 {
  "qid": "q25e581f30a",
  "kind": "yes/no",
  "text": "A 60-year-old gentleman passes away after a car accident. On routine autopsy it is incidentally noted that he has both a ventral and dorsal pancreatic duct. This incidental finding observed by the pathologist is generated due to failure of which of the following embryological processes?\n\nAnswer choices:\nA. Notochord signaling\nB. Apoptosis\nC. Fusion\nD. Neural crest cell migration\nE. Stem cell differentiation\n\nProposed answer: C. Fusion",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "q698ebe6d99",
  "kind": "yes/no",
  "text": "What page is this? Why was it deleted?",
  "question": "Is this request from a Wikipedia editor to another editor clearly polite?",
  "definitions": "- yes: At least 4 of 5 raters placed it on the polite side of the scale: courteous wording such as greeting, thanks, apology, praise, hedging ('I think', 'perhaps') or indirect asks ('would you mind', 'could you please').\n- no: At most 1 of 5 raters placed it on the polite side: the request is plain and neutral (bare questions or statements without courtesy markers) or blunt and impolite."
 },
 {
  "qid": "q0c93098835",
  "kind": "choice",
  "text": "Sentence from a New York Times opinion article: But as even General Jaruzelski ultimately learned, neither political stability nor economic reform can be achieved by mere repressive force.",
  "question": "How positive or negative is the sentiment this text expresses, as a typical reader would rate its intensity?",
  "options": [
   "Option C",
   "Option B",
   "Option K",
   "Option T",
   "Option Q"
  ],
  "definitions": "- Option C: Strongly or extremely negative (rated -3 or -4 on a -4..+4 scale): intense anger, disgust, despair, harsh criticism or insults, often intensified by boosters, capitals or exclamation marks.\n- Option B: Mildly to moderately negative (rated -1 or -2): a clear but restrained complaint, worry, disappointment or criticism, or negativity softened by hedges or offset by minor positives.\n- Option K: No net sentiment (rated 0): factual, descriptive or procedural text, questions without evaluative tone, or positives and negatives that cancel out.\n- Option T: Mildly to moderately positive (rated +1 or +2): clear but restrained approval, satisfaction, hope or praise, or positivity softened by hedges ('kind of good') or mixed with minor negatives.\n- Option Q: Strongly or extremely positive (rated +3 or +4): intense enthusiasm, delight, love or superlative praise, often with boosters, capitals, exclamation marks or emoticons."
 },
 {
  "qid": "qaf4baad33a",
  "kind": "yes/no",
  "text": "Reminds me of Maria Dizzia's character with Tourette's from Louis CK's Horace &amp; Pete who gives a heart-rending monologue and then immediately blurts out \"Fuck me nigger-style!\"   \n\nEdit: [Found it!](https://youtu.be/66fUFICKkQU) This one wasn't after her monologue though, I was thinking of a different moment.   \n\nEdit 2: [Here's a fantastic comp of her other gems!](https://youtu.be/etZEL5y3gn0)",
  "question": "Is the potential slur in this comment used to express contempt for a person or group?",
  "definitions": "- yes: Derogatory use: the slur conveys contempt toward a person or group - as an insult or label for someone, a stand-alone slur, sexualised or fetishising use, a slur-laden generalisation about the group, or self-deprecating use.\n- no: Not derogatory: the word is only mentioned (quoted, discussed, recalled, condemned in counter-speech or used sarcastically against bigotry), reclaimed positively by a member of the targeted group, or used in an unrelated sense (cigarette, transmission)."
 },
 {
  "qid": "q862dce3cbe",
  "kind": "yes/no",
  "text": "It’s called puberty retard",
  "question": "Is this post sexist?",
  "definitions": "- yes: The post is sexist: it contains abuse or negative sentiment directed at women because of their gender, or their gender combined with another identity such as race, religion or being trans - including casual gendered slurs, stereotypes and backhanded compliments.\n- no: The post is not sexist: it may be rude, crude, about gender or relationships, or abusive toward men or other groups, but it expresses no abuse or prejudice against women because they are women."
 },
 {
  "qid": "qea1374ef99",
  "kind": "yes/no",
  "text": "How is a drug he bought for $5 million suddenly worth $2 billion?",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: All 3 annotators rated the tweet medium or strong clickbait: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: None of the 3 annotators rated it medium or strong clickbait: the tweet states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "qf596272f2d",
  "kind": "yes/no",
  "text": "Leading German scientists are now spreading fear among children at schools. Is this the indoctrination part of the Masterplan?",
  "question": "Does this paragraph make the contrarian climate claim that climate science or the climate movement is unreliable?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that climate science or the climate movement is unreliable: it attacks the reliability of climate science or its proponents: the data, models, methods or consensus are uncertain, unsound or manipulated; scientists, the IPCC, activists, media or politicians are alarmist, biased, hypocritical, corrupt or part of a conspiracy.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that climate science or the climate movement is unreliable."
 },
 {
  "qid": "qd0d1c5135f",
  "kind": "yes/no",
  "text": "Wikipedia page: Rockwood Summit High School\nSection: Demographics\nTable:\n| Year | Enrollment | White (%) | Black (%) | Asian (%) | Hispanic (%) | Free/reduced lunch (%) |\n| 2018 | 1,298 | 80.1 | 10.1 | 4.2 | 3.0 |  |\n| 2011 | 1,321 | 85.9 | 11.1 | 1.7 | 0.9 | 17.3 |\n| 2010 | 1,372 | 85.4 | 11.9 | 1.8 | 0.9 | 19.0 |\n| 2009 | 1,368 | 85.9 | 12.1 | 1.4 | 0.6 | 16.3 |\n| 2008 | 1,390 | 85.8 | 12.2 | 1.2 | 0.8 | 15.6 |\n| 2007 | 1,394 | 86.2 | 12.4 | 0.9 | 0.5 | 12.5 |\n| 2006 | 1,335 | 86.1 | 12.1 | 1.3 | 0.3 | 13.1 |\n| 2005 | 1,342 | 85.2 | 13.0 | 1.3 | 0.3 | 12.8 |\n| 2004 | 1,361 | 84.3 | 13.7 | 1.5 | 0.4 | 13.2 |\n| 2003 | 1,363 | 83.3 | 14.7 | 1.3 | 0.6 | 13.7 |\n| 2002 | 1,350 | 83.9 | 14.7 | 1.1 | 0.2 | 12.6 |\n\nClaim: As of 2018, Rockwood Summit has an enrollment of about 1,361 students.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "qd1526b676a",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (QMED), Junior Engineer – Part I.\n\nQuestion: When an air started, four-stroke cycle diesel engine is being cranked over, the starting air is admitted to each cylinder during the beginning of its ________.",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "intake stroke",
   "compression stroke",
   "power stroke",
   "exhaust stroke"
  ],
  "definitions": "- intake stroke: Answer \"intake stroke\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- compression stroke: Answer \"compression stroke\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- power stroke: Answer \"power stroke\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices.\n- exhaust stroke: Answer \"exhaust stroke\": correct only if filling the blank with it makes the statement true and it is the best completion among the listed choices."
 },
 {
  "qid": "qaee017f08d",
  "kind": "yes/no",
  "text": "Disgusting hags, even more disgusting are the simps who wife up these whores.",
  "question": "Is this post sexist?",
  "definitions": "- yes: The post is sexist: it contains abuse or negative sentiment directed at women because of their gender, or their gender combined with another identity such as race, religion or being trans.\n- no: The post is not sexist: it may be rude, offensive, about gender, or abusive toward other groups or men, but it shows no abuse or prejudice against women because of their gender."
 },
 {
  "qid": "q68163c094e",
  "kind": "yes/no",
  "text": "Also note, we previously calculated the adiabatic lapse rate and temperature distribution in a theoretical Earth atmosphere of 100% Nitrogen, a non-greenhouse gas, and found the adiabatic lapse rate and troposphere temperature distribution almost the same as our Earth, surface temperature warmer on the theoretical 100% Nitrogen atmosphere Earth, thus proving greenhouse gases act as cooling agents rather than warming.",
  "question": "Does this paragraph make the contrarian climate claim that human greenhouse gases are not causing climate change?",
  "definitions": "- yes: The paragraph itself asserts or argues (in its own voice, not just quoting someone to rebut them) the contrarian claim that human greenhouse gases are not causing climate change: it denies that human greenhouse-gas emissions drive climate change: it is natural cycles or variation (sun, oceans, orbital cycles); non-greenhouse human forcings are responsible; there is no evidence that the greenhouse effect or carbon dioxide drives warming; CO2 is not rising or human emissions are negligible.\n- no: The paragraph does not make this contrarian claim: it gives background, neutral description or mainstream statements, or it makes a different kind of argument (for example about policy costs rather than the science, or vice versa) without claiming that human greenhouse gases are not causing climate change."
 },
 {
  "qid": "qd4feaf9f96",
  "kind": "yes/no",
  "text": "There's a reason we have hair... down there!\n@healthmeup #HealthMeUp #ThisIsIt",
  "question": "Is this news-publisher tweet clickbait, written to lure readers into clicking rather than to inform them?",
  "definitions": "- yes: At least 4 of 5 annotators rated the post considerably or heavily clickbaiting: it teases or withholds the key fact ('this', 'here's why', 'you won't believe'), exaggerates, or baits curiosity so the reader must click to learn what it is about.\n- no: At most 1 of 5 annotators rated it considerably or heavily clickbaiting: the post states its news informatively (who did what), so a reader learns the point without clicking; an emotive topic, a quote or a mild question alone does not make it clickbait."
 },
 {
  "qid": "qcbce90b35a",
  "kind": "choice",
  "text": "When the *first* thing someone does is call me a tranny and say we're all pedophiles, there's not a lot of room to de-escalate.",
  "question": "How is the potential slur in this comment used?",
  "options": [
   "derogatory",
   "mention without contempt",
   "reclaimed by the targeted group",
   "different meaning"
  ],
  "definitions": "- derogatory: The slur conveys contempt toward a targeted person or group: insults, labels, stand-alone slurs, sexualised use, generalisations about the community, or self-deprecation.\n- mention without contempt: The slur is mentioned rather than aimed at anyone - quoted, discussed as a word, recalled from an incident, used in counter-speech, or in sarcasm that mocks bigotry - by a speaker who is not reclaiming it.\n- reclaimed by the targeted group: A member of the targeted group uses the slur with positive or neutral force about themselves or their community (empowerment, in-group solidarity, humour).\n- different meaning: The word is used in a non-slur sense, such as 'fag' meaning a cigarette or 'tranny' meaning a vehicle transmission."
 }
]
