# Item 10 card authoring i10a_learning_3

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_learning_3.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are passages from community-written learning resources and course notes on many subjects.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: material type: what sort of study material this passage is, where neighbouring answers are easy to confuse.
Card 2 angle: learner action: what the passage asks the learner to do next, where neighbouring answers are easy to confuse.
Card 3 angle: topic: which sub-area of the subject the text is about, where neighbouring answers are easy to confuse.
The three cards must ask three different decisions, not three wordings of one decision.

Rules for all three cards:
1. A careful reader must be able to decide the answer from the text alone, with no outside knowledge.
2. The question must apply to most texts of this kind, not only to these 12 examples.
3. Use plain everyday words. No jargon and no academic terms.
4. Options must not overlap: for any text exactly one option fits best. The last option may be a catch-all (for example
   "something else"), and its definition must say exactly when to pick it.
5. Give every option a one-sentence definition that says exactly when to pick it.
6. Boundary rule, the heart of this task: build the options as near neighbours. At least two pairs of options must be easy to
   confuse for a hurried reader. For every such pair, the two definitions must state the dividing line: what the text must say
   or do to belong to the first option and not to the second.
7. Balance: choose questions where each option is the right answer for a fair share of texts of this kind. No option should
   fit more than half of the texts.
8. Do not copy label names or label sets from public datasets or benchmarks (for example positive/negative/neutral sentiment
   scales, entailment/contradiction, star ratings, standard emotion lists, standard news or topic category lists, or intent
   lists from chatbot or banking datasets). Invent labels that fit the real decision.
9. Do not ask about anyone's identity, health or other personal traits, and do not ask for an opinion about a named person.
10. Do not label, summarise or quote the example texts. Your output holds only the 3 cards.

Labels are short (1 to 5 words), lower case unless a proper noun, and unique within a card. expected_share is your rough guess
for texts of this kind in general, not a count over the examples; the shares of a card sum to 1.

## Answer contract

Write ONE JSON object, and nothing else (no text before or after it), to the answer file named at the top.

{"task_id": "i10a_learning_3",
  "cards": [
    {"kind": "choice",
      "who_decides": "one sentence: who makes this decision and why",
      "question": "the question, ending with a question mark",
      "options": [{"label": "short label", "definition": "one sentence"}, "... 4 to 8 options in total"],
      "expected_share": {"<each label>": 0.2}},
    "... exactly 3 cards in total"
  ]}

The items below are read-only context (the example texts). Your answer holds exactly 3 cards.

## Example texts (JSON; read-only context, not items to answer)

[
 {
  "sid": "s01",
  "text": "Coffee Farming - What to expect\nYou will learn how to grow, protect and process coffee organically and on the scale of a small farm (anything from 1 – 10,000 coffee plants). You will learn how national and international coffee trade works and about various new trading options that allow to get better prices for your coffee. The book starts with general chapters, then adds specific chapters with knowledge for specific locations (esp. about producing coffee in Nepal, and selling in European Union countries).\nEach chapter contains two parts. The first has a lot of detail and background knowledge. While useful for agricultural extension workers, it is too much for farmers who are just starting to grow coffee. For them, there is a second part, summarizing the first one in a way that is practice oriented and easy to understand. Later, these second parts will also be provided in local languages and as audio versions to make their use comfortable for farmers on their mobile devices, and even while doing practical work. (We call this course concept \"pocket university\".)"
 },
 {
  "sid": "s02",
  "text": "Murus\nMURUS (τεῖχος). A wall of stone or brick, built as a defence and fortification round a town, in contradistinction to paries, the wall of a house, or any other edifice. (Cic. N. D. iii. 40. Id. Off. i. 11. Caes. B. G. ii. 12.) Town walls were usually constructed with square or round towers (turres) at certain intervals, a fortified gate (porta) at every point from which any of the great roads emanated; sometimes with a trench (fossa) on the outside, having a mound (agger) within it, upon which the ramparts (loricae, propugnacula) were raised, surmounted by turrets (pinnae) to shield the defenders."
 },
 {
  "sid": "s03",
  "text": "Current Parkinson's Paradigm - Homeostasis\nIn an individual without Parkinson's presumably the following situation of homeostasis obtains:\n(Go on to say that perturbations can occur through infection and trauma to disrupt homeostasis and to test the limits of the homeostatic mechanisms. A persistent state where damaging mechanisms are out of control or barely controlled can set in. Describe the self-perpetuating cycle. Inadequacies in the homeostatic mechanisms, maybe due to genetic variations, may mean that a disease state occurs more easily than normal. Give examples e.g. DJ-1, SNCA, Parkin)"
 },
 {
  "sid": "s04",
  "text": "History of rainwater harvesting - Indus Valley Civilizations\nAround 300 BCE, farming communities in Balochistan (now located in Pakistan, Afghanistan, and Iran), and Kutch, India, used rainwater harvesting for agriculture and many other uses. Rainwater harvesting was done by Chola kings as well. Rainwater from the Brihadeeswarar temple (located in Balaganpathy Nagar, Thanjavur, India) was collected in Shivaganga tank. During the later Chola period, the Vīrānam tank was built (1011 to 1037 CE) in the Cuddalore district of Tamil Nadu to store water for drinking and irrigation purposes. Viranam is a 16-km-long tank with a storage capacity of 1,465,000,000 cuft.\nThe infrastucture and evidence of rainwater harvesting from India is still found in Talibs, medium to large sized reservoirs that provide irrigation for plants as well as drinking; Johads, dams that capture and hold rainwater; baoris, wells dug into the ground and used for drinking water and Jhalaras; specially constructed tank for local community and religious purposes."
 },
 {
  "sid": "s05",
  "text": "Grand Duke of Hesse - Timeline\n1877 June 13, Prince Louis succeeded his uncle as Grand Duke of Hesse, taking the name \"Ludwig IV.\"\n1892, Ernest Louis Charles Albert William succeeded his father as Grand Duke of Hesse.\n1894 April 19, Ernest Louis Charles Albert William (Ernest Louis, Grand Duke of Hesse and by Rhine) and Princess Victoria Melita (\"Ducky\") of Saxe-Coburg and Gotha married.\n1897 July 2, Ernest Louis, the Grand Duke of Hesse, and Princess Victoria (Ducky), Grand Duchess of Hesse, attended the Duchess of Devonshire's fancy-dress ball at Devonshire House."
 },
 {
  "sid": "s06",
  "text": "Natural Transformations of Organismic Structures - Natural Transformations of Organismic Structures\nBiological systems, or living organisms are characterized by relational structures and their dynamic transformations which can be represented as natural transformations of heterofunctors in organismic supercategories(OS). Such OS-structures can be specified mathematically either by using the Yoneda-Grothendieck Lemma and construction, or they can be directly derived by a mathematical interpretation of the first ten axioms of ETAS, plus two additional axioms defining both `self-repair' of metabolic components and complete reproduction in terms of genetic coding, translational genomics and epigenetic meta-processes.\nNatural transformations of organismic structures allow for the extension of both Rashevsky's organismic set theory and Robert Rosen's Metabolic-Replication Systems Set-Categorical approach to relational biology based on the concepts of molecular set variables and variable categories; the latter concepts are generalizations of Anthony Bartholomay's definition of molecular sets, and the consideration of variable categories with structure instead of only the discrete topology of sets. Further details concerning mathematical, logical and complex modeling are provided in the following list of publications and related web (html) links."
 },
 {
  "sid": "s07",
  "text": "Community - Decir (to say, to tell)\nDecir is a verb that has an irregular yo conjugation. While yo is irregular, all the other forms are conjugated using the -ir conjugation. Below is the conjugation for decir:\nNote: Of course you should remember by now that usted (Ud.) and ustedes (Uds.) conjugate to the 3rd person form."
 },
 {
  "sid": "s08",
  "text": "Building and construction facility\nAny town is constantly growing. So it needs qualified builders & domestic engineers, which will be capable of bringing any business up. The engineers will inevitably have a need to have a place, where orders are considered and planned, architects prepare projects, where builders and workers are hired, where the building machinery, cranes, tools, spacesuits etc. are stored. In fact this business should be established first to support rapid construction of other facilities.\nBuilding on moon has certain advantages, as 6 times lighter gravity provides much less power requirements for lifting machinery, less requirements for construction stiffness etc. Any supporting construction can be finely built from aluminum, or some other cheap and unsuitable for earth construction materials.\nFrom the other side - the lack of atmosphere gives much stricter requirements for building places, where human presence is necessary. Very hardy constructions and reliable systems must be implemented in any new building, which should contain regenerated and heated air. Buildings, suited for human beings also require all sorts of domestic communications, like water, heating, maybe common canalization, food delivery, transportation of some kind(possibly underground) and more. From this point of view - the other businesses on moon are best suited(financially) for robotic beings."
 },
 {
  "sid": "s09",
  "text": "Growth of Exponential Function\nas soon as\\,.\\, Here, means the ceiling function;\\, has been estimated downwards by taking only one of the all positive terms of the series expansion\nThe growth of the real exponential function\\,\\, \\,\\, exceeds all power functions, i.e.\nProof. \\, By corollary 2, we can write:\\, \\, as\\, (see also theorem 2 in limit rules of functions)."
 },
 {
  "sid": "s10",
  "text": "Resources\nStudents are encouraged to use their initiative in using online and offline resources. Is there a broken link? Just delete it! Or, if you want to do something that will really help - why don't you hunt the page down and repair it?"
 },
 {
  "sid": "s11",
  "text": "Computers - Country Focus (Uruguay)\nUruguay (Spanish: Uruguay) is a country located in the southeastern part of South America. It is home to 3.5 million people, of which 1.4 million live in the capital Montevideo and its metropolitan area.\nIt is bordered by Brazil to the north, by Argentina across the bank of both the Uruguay River to the west and the estuary of Río de la Plata to the southwest, and the South Atlantic Ocean to the southeast. Its surface is 176.215 km2 being by its territorial extension the second smallest country in South America, larger only than Suriname and the French overseas department of French Guiana.\nMontevideo was founded by the Spanish in the early 18th century as a military stronghold. Uruguay won its independence in 1825-1828 following a three-way struggle between Spain, Argentina and Brazil. It is a constitutional democracy, where the president fulfills the roles of both head of state and head of government.\nThe economy is largely based on agriculture (making up 10% of GDP and the most substantial export) and the state sector, Uruguay's economy is on the whole more stable than in its surrounding states, and it maintains a solid reputation with investors.\nAccording to Transparency International, Uruguay is the second least corrupt country in Latin America (after Chile), with its political and labor conditions being among the freest on the continent.\nUruguay has an impressive legacy of artistic and literary traditions, especially for its small size. The contribution of its alternating conquerors and diverse immigrants has resulted in native traditions that integrate this diversity. Uruguay has centuries old remains, fortresses of the colonial era. Its cities have a rich architectural heritage and an impressive number of writers, artists, and musicians. Uruguayan tango is the form of dance that originated in the neighborhoods of Montevideo, Uruguay towards the end of the 1800s."
 },
 {
  "sid": "s12",
  "text": "Asemic International: The Manifesto\nThe Manifesto requires no names, signatures, identifications, strict obligations and vows, charges and reports. The ones who want to join Asemic International bear any obligations whatsoever only for themselves. We welcome continuous addition and amendment of the Manifesto stipulations if it doesn’t contradict its core ideas – the fight against bureaucracy, oppression, racist superstitions, patriarchy, phobias, and capitalism.\nTranslation of the Manifesto into other languages and its distribution all across the world are welcome!"
 }
]
