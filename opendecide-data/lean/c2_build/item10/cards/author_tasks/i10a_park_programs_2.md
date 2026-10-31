# Item 10 card authoring i10a_park_programs_2

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_park_programs_2.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are listings of programmes and activities offered at state parks (tours, classes, events).
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: fit: which visitors the program suits, where neighbouring answers are easy to confuse.
Card 2 angle: visit conditions: what a visitor must arrange or bring before taking part, where neighbouring answers are easy to confuse.
Card 3 angle: purpose: what a visitor is meant to get out of the program, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_park_programs_2",
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
  "text": "Armistice Day to Veterans Day\nInspired by the European commemoration of Armistice Day, Veterans Day became a national holiday in 1926—eight years after the guns of the Great War fell silent. Visit the John Bell House today to explore the experience of Delawarean Doughboys of all colors and creeds who went Over There. As a token of rememberance, we offer you a traditional paper poppy so that you can carry what you learn with you when you leave and honor their service always. Paper lapel poppies available while supplies last. Free"
 },
 {
  "sid": "s02",
  "text": "Auburn Heights Invitational: Classic Car Show & Garden Party\nThe annual Auburn Heights Invitational features a display of exceptional motor cars from the dawn of the automotive age through 1969. The event offers a rare opportunity to experience extraordinary vintage autos amidst the elegance of the Auburn Heights estate. This years spotlight feature: Rumble Seats! Funds raised benefit the Joseph Boxler Education Fund and the Marshall Steam Museum and Friends of Auburn Heights. Tickets are $20 in advance, $25 at the gate ($14 for ages 14 & under). Learn more at auburnheights.org."
 },
 {
  "sid": "s03",
  "text": "July Steamin Day\nClimb into an antique automobile or board one of our 1/8-scale trains and experience travel at the turn of the 20th century! Enjoy the splendor of Auburn Heights and tour the magnificent 1897 mansion that was home to three generations of the Marshall family. All admission options include entry into the newly renovated Marshall Steam Museum, which has special exhibits, a working 1930s Lionel electric train display, kids activities and more. Plenty of tickets available at the entry, no advance registration required. $12/adult (age 13 & up), $8/child (age 1-12), infants and members are free."
 },
 {
  "sid": "s04",
  "text": "Winter Solstice Walk\nWhat's happening at Bellevue on the shortest day of the year? Join the naturalists for a guided hike through the park to learn about the science of the solstice and to explore the nature of winter. We will hike up to the Bellevue Woods Nature Preserve, which is about a 1.5-2 mile loop. Meet at the Arts Center. Free."
 },
 {
  "sid": "s05",
  "text": "Paint by Day Fundraiser Hosted by the Friends of Killens Pond\nHelp the Friends of Killens Pond State Park raise money and have fun doing it! We will be exploring watercolor and alcohol paints with local artist Jennifer Boland. We will be painting a snowy cottage scene. All materials will be provided. All experience and skill levels encouraged. Program will meet at the nature center and will last about 2 hours. Pre-registration required."
 },
 {
  "sid": "s06",
  "text": "Pop Up Pawpaw at the Blue Ball Barn\nDrop in to learn more about the Pawpaw and the Zebra Swallowtail. The park naturalists will have an interpretive display along with brochures from the National Pawpaw Growers Association and other resources"
 },
 {
  "sid": "s07",
  "text": "Mocktails & Moonshine\nJourney back to the 1930’s with us to explore the end of Prohibition and the legal as well as illegal spirits that were once part of life here. We will hear tales of residents of the past and make some alcohol-free libations. Historically inspired mocktails will be served. Pre-registration required. $10 per person."
 },
 {
  "sid": "s08",
  "text": "Get in Touch with the Marsh\nThe marsh at Holts Landing is full of amazing sights and sounds, but have you ever wondered what it FEELS like? Join a park interpreter for this hands-on program that will let you touch everything from animal pelts to plant specimens to that sticky marsh mud. Ages 6 and up. Meet at Holts Landing State Park. This is a free program, but registration is required."
 },
 {
  "sid": "s09",
  "text": "Meet the Marsh: Nature Preserve Hike\nGet to know the freshwater marsh at Brandywine Creek on this fun hike. We will learn about the history of the marsh while we hike down to see it and discuss why this important habitat deserves to be protected. The hike will start from Hawk Watch and the terrain will be difficult and extremely muddy on this 2 mile trail. Be sure to bring water and shoes you can get muddy in! Free!"
 },
 {
  "sid": "s10",
  "text": "Kids Craft Club: Net-Making\nPort Penn fishermen relied on their nets! Many fishermen wove their own nets, and fixed them on their own, too. In this program, we'll learn how to make a simple net, while also talking about the local Port Penn fishermen. This program will be held at the Fort Delaware State Park office at 2540 Colter Road, Delaware City, DE 19706. All children must be accompanied by an adult."
 },
 {
  "sid": "s11",
  "text": "Dressed for Defense: Delaware's Soldiers Through the Years\nCelebrate Veterans Day with living history interpreters as they share the stories and equipment of some of Delaware's soldiers stationed at Cape Henlopen throughout history. This program is free and interpreters will be on site from 10 a.m. to 2 p.m. Programming is located at the Fort Miles Cantonment Area."
 },
 {
  "sid": "s12",
  "text": "Art in Action: Beginners Paper Quilling - FULL\nLearn some basic quilling techniques with Kelly Martin, owner of Paper Hibiscus, while creating a Daffodil card to take home to be framed or sent to someone special. Pre-registration and payment required by January 13. $10 per person, register online."
 }
]
