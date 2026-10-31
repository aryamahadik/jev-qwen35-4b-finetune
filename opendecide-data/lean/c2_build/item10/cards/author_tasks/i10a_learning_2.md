# Item 10 card authoring i10a_learning_2

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_learning_2.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are passages from community-written learning resources and course notes on many subjects.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: learning purpose: what the text is meant to help a learner do, where neighbouring answers are easy to confuse.
Card 2 angle: level: how much the passage assumes the learner already knows, where neighbouring answers are easy to confuse.
Card 3 angle: course role: what job the passage does inside a course, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_learning_2",
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
  "text": "Basics 2 Lesson 3 - Grammar notes\nRemember that in Latin the conventional word order is subject-object-verb, but that is less important than the endings of the nouns in the sentence, which indicate case. So far we have used nominative case for the subject and predicate nouns (if there is a linking/being verb in the sentence); and we have had a limited number of accusative case nouns, used as direct objects. More formal study of accusative case will be kept for the skills that introduce several nouns belonging to one declension at one time, making it easier to note the patterns."
 },
 {
  "sid": "s02",
  "text": "Electromagnetic Coil - Attaching Extension wire to forward lead\nNow that the enamel has been removed from all ends, take one end of the extension wire and bend it into a hook, this hook shouldn't comprise of any more than a half an inch. The lead that protrudes from the center of the spool is the forward lead. Bend the forward lead into a hook. Hook together the hooks of the forward lead and the extension wire.--SeanShriner (discuss • contribs) 20:56, 14 March 2013 (UTC)"
 },
 {
  "sid": "s03",
  "text": "Bearney2 - Lucettes\nLucettes has always been very into the Ale type of beer, this year alone they have released Spice Blond, American Pale and Golden Ales. They usually on their website take recommendations from all their customers on what types of beers they want to see. They of course listen and try to please their customers. As far as the food they have about six different kinds of pizza and four calzones. Pizza really correlates well with beer and are a very popular food choice for breweries. Also Lucettes is know for giving excellent tours of their whole building and complex. They usually last about an hour and a half and also include a pint glass and free samples of most of their beers. These tours cost about $10 per person and are a great way to spend time with the people you love and drink some beer."
 },
 {
  "sid": "s04",
  "text": "Exact pronunciation\nThis is a page designed for students to improve and develop their spanish pronunciation. In this part of the course, we will be using IPA (International Phonetic Alphabet) in order to make learning how to pronounce the spanish language easy, effective and exact, and to reduce the accent a student may have when speaking. If there are any objections to this page, then please discuss."
 },
 {
  "sid": "s05",
  "text": "Ground Operations (Part 1) - ENGINE AND PROPELLER\nThe pilot should make note of the condition of the engine cowling. [Figure 2-8] If the cowling rivet heads reveal aluminum oxide residue, and chipped paint surrounding and radiating away from the cowling rivet heads, it is a sign that the rivets have been rotating until the holes have been elongated. If allowed to continue, the cowling may eventually separate from the airplane in flight.\nCertain engine/propeller combinations require installation of a prop spinner for proper engine cooling. In these cases, the engine should not be operated unless the spinner is present and properly installed. The pilot should inspect the propeller spinner and spinner mounting plate for security of attachment, any signs of chafing of propeller blades, and defects such as cracking. A cracked spinner is unairworthy.\nThe propeller should be checked for nicks, cracks, pitting, corrosion, and security. The propeller hub should be checked for oil leaks, and the alternator/ generator drive belt should be checked for proper tension and signs of wear.\nCheck the propeller and inside the cowling. When inspecting inside the cowling, the pilot should look for signs of fuel dye which may indicate a fuel leak. The pilot should check for oil leaks, deterioration of oil lines, and to make certain that the oil cap, filter, oil cooler and drain plug are secure. The exhaust system should be checked for white stains caused by exhaust leaks at the cylinder head or cracks in the stacks. The heat muffs should also be checked for general condition and signs of cracks or leaks. The air filter should be checked for condition and secure fit, as well as hydraulic lines for deterioration and/or leaks. The pilot should also check for loose or foreign objects inside the cowling such as bird nests, shop rags, and/or tools. All visible wires and lines should be checked for security and condition. And lastly, when the cowling is closed, the cowling fasteners should be checked for security."
 },
 {
  "sid": "s06",
  "text": "17-quantum interpretations - Bell's theorem and quantum entanglement\nThe system described above involves one particle that can be in one of two different places. To model the paradoxical behavior associated with Bell's theorem we require a bit more complexity. First, we need wave that not only can be in two different places, it needs to wave in two different directions.\nShown to the right is one of two degenerate standing waves that can occur if the wave is confined to lie within a circle. Both waves are commonly called 2p states. The other 2p state is oriented perpendicular to the one shown in the figure.\nWe also need two different particles, depicted here as coffee and tea, located in two cups that can moved apart so that they are separated by vast distances. By tradition, the two cups in a Bell's theorem experiment are called Alice and Bob. And given the analogy to sloshing liquids, it is not unreasonable to call the two particles Coffee and Tea. We don't know which beverage is in which cup. But we do know that if one is in Alice, the other is in Bob. And we know something about how the beverages are sloshing. For example, if one is sloshing in the clockwise direction, the other is counterclockwise."
 },
 {
  "sid": "s07",
  "text": "Transport - Learning Tasks\nare considered as separate units that can be recombined on a trip from A to B on ships, railways,.... Discuss the impact of such an approach on the Sustainable Development Goals. How does transportation support sustainability or creates drawbacks for sustainable accomplishment of a specific goal! E.g.\n* less consumption of resources due less required reusable public propulsion units.\n* resusabilty of passenger cabins even if the propulsion unit is outdated,\n* a trailer for passenger cabins for a bus allows integration into current public transport concepts.\n* Identify requirement and constraints of such a theoretical public transport approach with intermodal passenger cabins."
 },
 {
  "sid": "s08",
  "text": "AI prompts - Prompt\nI'd like to practice Latin forms. Please act as a Latin teacher. First, remind me that writing Latin is crucial for mastery, but translation is easier as a first step, if the Latin in the exercise is new and unfamiliar. If you are able, remind them that a full lesson explanation is available at - if you can't then just say that you understand that the exercise has come from Wikiversity's Latin course, and this exercise is about using scrībō (I write), habeō (I have) and their forms.\nAfter Translation exercises: remind student that Writing Latin is the surest path to true Roman citizenship - encourage with one of these themes:\nPlease begin by explaining the importance of writing Latin and asking for my choice (1 or 2)."
 },
 {
  "sid": "s09",
  "text": "Final report - The Siegenthaler Incident\nIn May of 2005 a Wikipedia editor entered false information into the Wikipedia biography for John Seigenthaler, Sr. The false information was not discovered until September 2005 after which it became known as the Seigenthaler Incident. In response to the publicity generated by this and other similar cases (see also), Wikipedia restricted page creation (see: Wikipedia Signpost 2005-12-05 \"Page creation restrictions\") and created new guidelines for biographies. The Wikipedia community continues to struggle with biased and false content in its biographical articles."
 },
 {
  "sid": "s10",
  "text": "Methods - Preventive Strategies\nMany diseases are preventable through simple, nonmedical methods. For example, research has shown that the simple act of handwashing with soap can prevent the spread of many contagious diseases. In other cases, treating a disease or controlling a pathogen can be vital to preventing its spread to others, either during an outbreak of infectious disease or through contamination of food or water supplies."
 },
 {
  "sid": "s11",
  "text": "Global Metronome\nA global metronome can be used for to keep a the musicians in sync. The basic idea is to use the Network Time Protocol (NTP) in an WebApp that runs in a browser of your choice on Linux, Windows, MacOSX, Android, iOS,... that creates a visual beat (e.g. 120 bpm - beats per minutes) with a joint offset from a timestamp shared between the musisians e.g. with a JSON file loaded into the WebApp."
 },
 {
  "sid": "s12",
  "text": "Probability Dilation Theory - Example entropy evolution\nEntropy evolution under repeated localized PDT transformation showing entropy reduction and probability concentration under iterative probabilistic reweighting. Programmatically generated using Python in a ChatGPT-assisted workflow. The entropy decreases under repeated application of the dilation field as probability mass becomes increasingly concentrated in the highest-weight states."
 }
]
