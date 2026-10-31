# Item 10 card authoring i10a_park_programs_1

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_park_programs_1.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are listings of programmes and activities offered at state parks (tours, classes, events).
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: kind of activity: what sort of activity the listing offers, where neighbouring answers are easy to confuse.
Card 2 angle: effort: how physically demanding the program is, where neighbouring answers are easy to confuse.
Card 3 angle: setting: where and in what surroundings the program takes place, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_park_programs_1",
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
  "text": "Earth Day at Holts Landing: Service Projects & Forest Bathing\nCelebrate Earth Day by giving back to the park and immersing yourself in nature’s bounty! Join the Friends of Holts Landing State Park for a volunteer trail clean-up project in honor of Earth Day. After the project is complete, park staff will host a session of Shinrin-Yoku: the Art of Japanese Forest Bathing."
 },
 {
  "sid": "s02",
  "text": "World Oceans Day\nSwim on over to the zoo for a celebration of our blue planet on World Ocean's Day! This event aims to increase awareness of the pivotal role the ocean plays and encourages individuals to take action to protect it, beginning right in our local communities. Take part in ocean themed activities, a scavenger hunt, and don't miss a very special performance by The Chesapeake Mermaid at 12:00pm! The Chesapeake Mermaid's visit will include an interactive storytime with movement, song, bay creature sign language, and delightful encounters with the mermaid’s wildlife friends! This event is included with regular zoo admission. This performance is supported, in part, by a grant from the Delaware Division of the Arts, a state agency, in partnership with the National Endowment for the Arts. The Division promotes Delaware arts events on"
 },
 {
  "sid": "s03",
  "text": "Live Reptile and Amphibian Show!\nThey are scaly, slimy and alive! Meet some of our native reptiles and amphibians for an afternoon of family fun and learning. Program meets at the nature center. Pre-registration required. Online registration ends 22 hours prior to the program."
 },
 {
  "sid": "s04",
  "text": "Young Family Hike: Falling Leaves\nTake a short walk outside to find out why trees change in fall and then make a fun leaf craft. For ages 3-7 years old with an adult. Dress for the weather. Online registration ends 24 hours prior to program."
 },
 {
  "sid": "s05",
  "text": "Homefront Holidays: 1940s Dinner & Dance Party\nNEW! Swing back to the 1940s with this exclusive holiday party, proudly presented by First State Heritage Park and the Fort Miles Historic Area. You're invited to pull out your pinstripes and do up your Victory Rolls to join us in celebrating the holidays like it's 1942! We're recreating the Christmas dinner served to the troops stationed at historic Fort Miles during World War II for your dining experience, bringing out the smooth entertainments of Madison Coleman and the World War Tunes band, offering up swing dance lessons to help you cut a rug, and more in this sure-to-please night away. Buy your tickets, grab that special someone, and make a holiday memory to cherish! $90 per person. This special event takes place in the historic venue of Battery 519, constructed to defend Delaware's coasts during World War II. Your ticket includes your meal, musical entertainments, swing dance lessons, and a guided tour. There will be a ticketed cash bar serving throughout the evening as well."
 },
 {
  "sid": "s06",
  "text": "Autumn Discovery Hike\nJoin a guided hike all about the changing seasons. Guests will see the trees in a variety of reds, oranges and yellows as autumn is in full swing. This hike is great for families. Meet at the Nature Center in Area 5. Distance is 1.5 miles/Easy. Free program."
 },
 {
  "sid": "s07",
  "text": "Murder at the Mansion\nThe year is 1943, you've been invited to our USO Dance here at the Magnolia Estate Club. Even though we are stateside, many dangers lurk, keep your eyes and ears open as we gather to commemorate our continued work with the War Effort. $30 per person, register online. Light refreshments provided. Costumes welcomed but not required."
 },
 {
  "sid": "s08",
  "text": "9th Annual Kids Catch All Fishing Tournament - Day 2\nThe Kids Catch All Fishing Tournament helps to raise money for the Lyme Disease Association of Delmarva, Inc whose purpose is to provide educational resources on Lyme Disease and other tick-borne illnesses."
 },
 {
  "sid": "s09",
  "text": "Whale Wallow Explorers: Owls\nHoo Hoo is up for a look into our feathery friends the OWLS! Join the naturalist as we learn about owls in the park and dissect owl pellets to see what kind of food they eat. For children ages 6 - 9. Online registration ends 24 hours prior to the program."
 },
 {
  "sid": "s10",
  "text": "Back Porch Birding\nBirding is a rewarding activity, but may seem overwhelming to newcomers. Bring your lunch and join the naturalists on the back porch of the Nature Center to watch for birds and learn some tips about birding! Discover the ins and outs of bird feeders and their upkeep. The program will meet in the Nature Center. Free with park admission."
 },
 {
  "sid": "s11",
  "text": "Nahova: Temporary Exhibition\nNahova is a painter influenced by Abstract Impressionism who creates timeless pieces that reflect her past and current experiences. She utilizes acrylic, oil and glass paint to create “cells” in most of her paintings and incorporates fabric 3D objects to create deeper sensations. When composing these pieces, Nahova hopes to inspire others to bend the rules, ask why, not to conform, to be their most genuine selves irrespective of how unpolished that expression of that self may appear. Exhibition will be at the Blue Ball Barn from November 1-30, 8:00 AM - 4:00 PM. Reception November 3, 5:00 - 8:00 P.M."
 },
 {
  "sid": "s12",
  "text": "Animal Anatomy: Adaptations\nHave you ever wished superpowers were real? What if I told you they are?! Come check out some cool animals with outstanding abilities! Saturday at the campground amphitheater; Sunday at the nature center. Space is limited; pre-registration required. Online registration ends 24 hours prior to the program."
 }
]
