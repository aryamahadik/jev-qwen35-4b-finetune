# Item 10 card authoring i10a_learning_1

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_learning_1.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are passages from community-written learning resources and course notes on many subjects.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: topic: which sub-area of the subject the text is about, where neighbouring answers are easy to confuse.
Card 2 angle: material type: what sort of study material this passage is, where neighbouring answers are easy to confuse.
Card 3 angle: learner action: what the passage asks the learner to do next, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_learning_1",
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
  "text": "Escher - Problem\nEscher drawings can be made into 3D objects that if looked at in the right lighting, at the right angle, create an illusion... typically of water going up hill or balls rolling up hill. These illusions make great demonstration devices that illustrate engineering and art to kids and start interesting conversations."
 },
 {
  "sid": "s02",
  "text": "Planned obsolescence - Definition\nPlanned obsolescence, or built-in obsolescence, in industrial design and economics is a policy of planning or designing a product with an artificially limited useful life, so it will become obsolete (that is, unfashionable or no longer functional) after a certain period of time. The rationale behind the strategy is to generate long-term sales volume by reducing the time between repeat purchases (referred to as \"shortening the replacement cycle\").\nProducers that pursue this strategy believe that the additional sales revenue it creates more than offsets the additional costs of research and development, and offsets the opportunity costs of repurposing an existing product line. In a competitive industry, this is a risky policy, because consumers may decide to buy from competitors instead if they notice the strategy.\nPlanned obsolescence tends to work best when a producer has at least an oligopoly. Before introducing a planned obsolescence, the producer has to know that the consumer is at least somewhat likely to buy a replacement from them. In these cases of planned obsolescence, there is an information asymmetry between the producer, who knows how long the product was designed to last, and the consumer, who does not. When a market becomes more competitive, product lifespans tend to increase. For example, when Japanese vehicles with longer lifespans entered the American market in the 1960s and 1970s, American carmakers were forced to respond by building more durable products."
 },
 {
  "sid": "s03",
  "text": "I. Introduction to Revelation - Outline of Revelation\nThe outline is a reference tool for use while working through the lessons on Revelation. It does not interpret Revelation, but merely presents the details of the book in the manner, and in the order, that they appear. Some words (e.g. \"locusts\") are placed in parentheses to indicate that their description in the text does not match our normal conception of them. Each of the seven churches is listed with the opening words of the message to that church."
 },
 {
  "sid": "s04",
  "text": "Appendix A: Content Validity Analysis\nThe panel of 4 EFL specialists were asked to consider each item of the questionnaire.\nPart 1: Levels of English Use with other members of the Thai academic community\nPlease identify whether or not each item is necessary for the measurement of the level of the English use of the students with other members of the Thai academic community."
 },
 {
  "sid": "s05",
  "text": "Sample Midterm Exam 2\n2. State the Cauchy-Riemann equations for a complex valued function. If you use symbols other then and indicate how they relate to these quantities.\n3. State whether the give function is holomorphic on the set where it is defined.\n4. Let be a simple closed curve so that lies in the interior of the region bounded by.\nsimply writing the correct value without any explanation will not receive credit.\n6. Let find a function so that is holomorphic in the complex plane and.\na. Using the limit characterization of the complex derivative show that is not holomorphic.\nc. Do parts (a) and (b) contradict each other, explain why or why not.\n8. State Cauchy's integral theorem, and intuitively what you need to know about the function, domain and contour."
 },
 {
  "sid": "s06",
  "text": "Homocysteine - Atherosclerosis\nElevated levels of serum homocysteine is associated with an increased risk of coronary artery disease. Among individuals with type 2 diabetes elevated plasma homocysteine levels are associated with an increased risk of macroangiopathy and nephropathy. It is unclear if this increased risk is due to the homocysteine itself, the methanol which is produced as a by-product of homocysteine biosynthesis, or some other mechanism which is correlated with homocysteine biosynthesis. Some authors believe that methanol causes arteriosclerosis. Other authors believe that arteriosclerosis is caused by homocysteine via some direct but yet to be explained mechanism."
 },
 {
  "sid": "s07",
  "text": "Contextual Learning\nContextual learning is based on a constructivist theory of teaching and learning in which subject matter is related to real-world situations, allowing students to make connections between knowledge and their own experiences. This lesson covers the Absorb - Do - Connect approach to contextual learning, proposed by William Horton."
 },
 {
  "sid": "s08",
  "text": "Neurobiology of emotion\nWelcome to the Wikiversity learning project about the neurobiology of emotion. This is a learn by doing project where participants collaborate to explore what neuroscience research has revealed about the biology of emotion.\nThis project is starting with a literature review, so please add useful links to this page and participate in discussion of previously published research."
 },
 {
  "sid": "s09",
  "text": "Lunula\nLU'NULA. Diminutive of LUNA. A small ornament in the form of a half moon, worn by women suspended from their necks (Isidor. Orig. xix. 31. Tertull. Cult. Foem. 10.); and by children as a token, amulet, or plaything. Plaut. Ep. v. 1. 33. and illustration s. CREPUNDIA, where it is seen amongst other objects round a child's neck."
 },
 {
  "sid": "s10",
  "text": "Glossary - Aesthetic and Experiential States\nAbsorption: A state of deep immersion in an activity or perception, often accompanied by diminished awareness of surroundings.\nAwe: A profound sense of wonder or reverence in response to beauty, vastness, or complexity.\nDiscovery: The excitement or satisfaction of encountering something new or previously unknown.\nHarmony: A felt sense of balance, coherence, or pleasing arrangement in perception or experience.\nInspiration: A sudden or sustained sense of uplift, motivation, or creative possibility.\nReflection: A contemplative turning of attention toward one’s own thoughts, feelings, or experiences.\nSensory Stimulation: Heightened awareness of sensory inputs and the subjective effects they produce.\nTimelessness: The sense that time has slowed, quickened, or become irrelevant during an experience.\nWonder: A feeling of curiosity mixed with astonishment at something remarkable or mysterious."
 },
 {
  "sid": "s11",
  "text": "Organisation - TO SEAFARERS\nWith great respect for your important and hard work you do as a seafarer to bring all types of goods around in the world, you will need to stay healthy. Now, you have been diagnosed with pre-diabetes(T2D) you should know that this is not a serious disease, that can be prevented to be a more serious disease by changes of your food and physical exercise pattern. Pre-diabetes increases the risk of developing type 2 diabetes, heart disease, and stroke. Our 16 week pre-diabetes coaching program is designed to support you to change your daily food habbits and physical activities and get rid of diabetes and overweight. If you accept the invitation given by your maritime medical doctor, you will get in contact with a support person, a \"coach\" with further information."
 },
 {
  "sid": "s12",
  "text": "Semantics of an imperative logic - Imperative statements in informal logic and natural language\nWhile classical logic does not normally concern itself with commands, other logics do regularly utilize imperatives. In mathematical logic, proof by contradiction is usually rendered in natural language with imperative statements:\nWhile perhaps overly-simplistic, suppose (and assume) are imperatives. They do not have a logic value, but are rather artifacts of natural language. The above statement would simply be rendered as in formal logic, a simple deceleration.\nThis highlights the actual function of the imperative as anterior to the logical content. Our formalization of imperatives"
 }
]
