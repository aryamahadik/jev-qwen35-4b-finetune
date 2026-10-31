# Item 10 card authoring i10a_travel_1

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_travel_1.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are passages from a community travel guide about places: what a place is like, how to get there and around, what to see and do, and how to stay safe.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: section: which section of a travel guide the passage belongs in, where neighbouring answers are easy to confuse.
Card 2 angle: kind of advice: what sort of information or advice the passage gives, where neighbouring answers are easy to confuse.
Card 3 angle: effort or risk: how demanding or risky the thing described is for a visitor, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_travel_1",
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
  "text": "Bus travel in India - Stay safe\nAll buses have to contend with the poor state of Indian highways and the havoc of Indian traffic which usually makes them slower, less comfortable and less safe than trains. Night buses are particularly hazardous, and for long-distance travel it is wise to opt for sleeper train services instead."
 },
 {
  "sid": "s02",
  "text": "Jimbolia - Get in\nJimbolia is located in the Banat plain, at the contact between Timis Plain and Mures Plain. It is located at the intersection of communication routes that make the connection between Romania and Serbia. It is a frontier post and rail and road border between the two countries. Jimbolia is linked with Timisoara by the county road DJ 59A and the railroad Kikinda (SR) - Jimbolia - Timisoara."
 },
 {
  "sid": "s03",
  "text": "Hirtshals - Do\nHirtshals is a starting point of the epic hike of Hærvejen, leading down the entire Jutland peninsula, all the way to the border with Germany. The trail is 500 km long and follows ancient trails used in olden times to transport cattle and soldiers. It is designed for an 18 day journey, but you can chose to hike shorter individual parts and still get a great experience of the nature and cultural variety of Jutland."
 },
 {
  "sid": "s04",
  "text": "Semarang Metropolitan Area - Get around\nSemarang Metropolitan Area is served by Trans Semarang bus rapid transit, comprising at least eight main corridors. Another bus rapid transit, the provincial-owned Trans Jateng has two corridors southward and westward in Semarang Metropolitan Area, linking Semarang Tawang Station (Semarang City) to Bawen Bus Terminal (Semarang Regency) and Mangkang Bus Terminal (Semarang City) to Bahurekso Bus Terminal (Kendal Regency).\nThe eastern part of Semarang metropolitan area is served by Kedungsepur commuter rail. The train links Semarang Poncol Station in Semarang to Ngrombo Station in Grobogan through Brumbung District in the south of Demak. The fare is Rp10,000."
 },
 {
  "sid": "s05",
  "text": "Via Alpina - Sleep\nOptions range from valley hotels to high-altitude alpine huts. In huts, dorms are standard and a sleeping bag liner is mandatory. Booking weeks in advance is essential for July and August. Wild camping is strictly regulated and often prohibited; check local rules."
 },
 {
  "sid": "s06",
  "text": "Rizal (Cagayan) - Get in\nRizal is mostly accessible through a road running north from Tuao, where it is connected to the rest of the province and the provincial capital Tuguegarao via the Cagayan-Apayao Road. There are passenger vans and jeepneys running to town from Tuguegarao, although this may entail waiting for an indefinite period for the vehicle to fill up. During the rainy season, access through this road may be hindered by the overflowing of the Chico River and the submerging of the Itawes Bridge that connects Tuao with the municipality of Piat, forcing a lengthy detour through the Cagayan-Kalinga Road from Tabuk.\nThere are efforts to develop a dirt road along the Zinundungan River leading to the town of Lasam in the north into a paved and alternate access route. A new road was opened in the 2020s running parallel to the Cagayan-Apayao Road and directly connecting Rizal with the town of Conner in Apayao, ending Tuao's stranglehold on transportation links."
 },
 {
  "sid": "s07",
  "text": "Sydney Harbour National Park - Landscape\nAt times, there may be moments where you might feel like \"is this Sydney?\" due to the large amount of greenery.\nWhen it comes to the shore, there are some near perpendicular cliffs, and some in artistic shapes and forms; providing a perfect place to relax and read a book by the ocean."
 },
 {
  "sid": "s08",
  "text": "Natchez\nNatchez is a city near the southwest corner of the U.S. state of Mississippi. This historic town is perched on a high bluff above the Mississippi River 100 miles upriver from New Orleans. It was an important, wealthy city before the Civil War. That history gave it the South's grandest collection of antebellum homes."
 },
 {
  "sid": "s09",
  "text": "Bloomington-Normal\nBloomington, pop. 77,000 (2010 census), is a city in the Midwestern state of Illinois in the United States of America, on the classic Route 66 highway across the country. With neighboring Normal, pop. 52,000 (2010 census), it forms a combined community of about 130,000 known locally as the Twin Cities. Illinois Wesleyan University is in Bloomington, and is not to be confused with Illinois State University in Normal."
 },
 {
  "sid": "s10",
  "text": "Milna - Get in\nBuses run several times a day from Supetar, the village where the ferry docks. Unfortunately, they stop in the late afternoon or early evening -- even in summer!, so you must rent a scooter or car, or take a taxi.\nA car or boat rental will let you explore the island and reach idyllic beaches."
 },
 {
  "sid": "s11",
  "text": "Norwalk (Ohio)\nNorwalk is a city in Northeast Ohio. It is the county seat of Huron County. Norwalk is one of Ohio's most scenic cities, with historic homes and buildings lining the streets. Its close proximity to Lake Erie has made this a favorite location for individuals and industry."
 },
 {
  "sid": "s12",
  "text": "Mljet - By boat\nSobra (east-end), Polače (west-end) and Pomena (west-end) serve as ferry ports for the island.\nFerry services may change by season so check the operators' websites.\nThe Nona Ana catamaran operates twice daily from Dubrovnik to Sobra and Polače on Mljet island. Polače is nearer the National Park than Sobra.\nThe company Krilo Shipping Company operate a daily fast ferry between Dubrovnik and Pomena.\nThere is car ferry from Split on Saturday and speed boat from Lastovo on Tuesday and Thursday.\nThe Krilo Star (passenger ferry) travels daily between Dubrovnik and Split, passing Pomena.\nFrom Korčula you can get to Sobra on Mljet island by car ferry operated by Jadrolinija on Mondays and Fridays. The ferry leaves Korčula Town at 14:00 and arrives at Sobra at 16:15. Sobra is some distance from the National Park, which is located on the western side of Mljet island. Alternatively, join a day trip excursion from Korčula organised by a travel agency:"
 }
]
