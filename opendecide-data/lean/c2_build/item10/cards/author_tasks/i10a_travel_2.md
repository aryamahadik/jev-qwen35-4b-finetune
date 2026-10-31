# Item 10 card authoring i10a_travel_2

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_travel_2.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are passages from a community travel guide about places: what a place is like, how to get there and around, what to see and do, and how to stay safe.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: traveller need: which need of a traveller the passage meets, where neighbouring answers are easy to confuse.
Card 2 angle: kind of place: what sort of place or setting the passage describes, where neighbouring answers are easy to confuse.
Card 3 angle: timing: when in a trip or a year the passage matters to a visitor, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_travel_2",
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
  "text": "New Italy\nNew Italy (Italian: Nuova Italia), initially named Cèa Venessia, is a small township of 187 (2016) in the Northern Rivers of New South Wales. It's a popular stopover for travellers heading north along the Pacific Motorway from Sydney towards Brisbane."
 },
 {
  "sid": "s02",
  "text": "St. Johann im Pongau\nSt. Johann im Pongau is the main city of the Pongau Region. It is in the Salzach Valley of the Eastern Alps is in the federal state of Salzburg. The city is largely dependent on tourism: Alpine skiing in winter and hiking in the summer months."
 },
 {
  "sid": "s03",
  "text": "Biase - Understand\nBiase is located in the southern senatorial district with a total area of 1,285.56km2 in Cross River State, Nigeria.\nIt is bounded at the West by Abia State and Ebonyi State, to the south Odukpani, east by Akamkpa and to the north by Yakurr and Abi council area."
 },
 {
  "sid": "s04",
  "text": "Greater Brisbane - By car\nMost of the motorway network in SE Queensland is centred around Greater Brisbane. Getting around most suburbs in Greater Brisbane can in most cases, be done entirely on motorways, though there are some notable exceptions where using a road that isn't a motorway is quicker and easier. The motorways and major roads are as follows:\nAll cities but Redland City have at least one motorway. Brisbane by far has the most motorways both by length and number, followed by Ipswich and Logan. Moreton Bay doesn't really have a motorway of its own, its only motorway is just the Bruce Highway on its way to Cairns."
 },
 {
  "sid": "s05",
  "text": "Shusha - Get around\nIt is easy enough to walk around Shushi. The streets of the lower part of the town are not yet paved. Therefore, expect a lot of mud if it is wet.\nTaxis are usually available in the area near and east of Ghazanchetsots Cathedral."
 },
 {
  "sid": "s06",
  "text": "Gwadar - Get in\nKarachi is the city from which Gwadar is closest and easiest accessible. You can either fly or else drive via the 653 km-long Makran Coastal Highway (N10), which runs along Arabian Sea coastline and is a scenic journey. Travel time is around 8 hours."
 },
 {
  "sid": "s07",
  "text": "Slatington - Understand\nSlatington, originally inhabited by the Lenape Native American tribe, is a small Lehigh County town located about 30 minutes northwest of Allentown. Named after the prosperous slate industry once housed there, Slatington is home to roughly 4,200 residents (2020 Census). Although there are a lack of activities to do within Slatington, there are plenty of nearby outdoor attractions and nature trails to explore the beauty of Pennsylvania."
 },
 {
  "sid": "s08",
  "text": "Bungus Bay - Get in\nThere is no more angkot/minibus directly. Use car-hailing apps (grab, gojek, maxim) - moto Rp 100-120,000, car Rp 150-190,000, duration 75-90 min. Or ask your hotel for their own shared taxi Rp 150,000 or private taxi Rp 350,000.\nMoto likely to decline as part of road very uphill and could be dangerous depending on luggages/load and construction work ongoing on same uphill segment at Apr 2024. Be careful of driver asking for \"extras\".\nArrange way back beforehand (group or nice driver) as there is no Grab coverage in Bungus bay or Sigunturmuda, and hotel may ask high price for taxi back (Rp 300-400,000). It's possible to hitchhike but be patient and prepared: road up/down hill, mostly exposed to sun, mostly motorbike traffic until Sigunturmuda."
 },
 {
  "sid": "s09",
  "text": "Smithers - History\nThe Bulkley Valley in which Smithers is situated was inhabited by the Wet'suwet'en First Nation. Smithers was founded in 1913 as the regional headquarters for the Grand Trunk Pacific Railway. The new community was named after the railway's chairman of the board of directors, Sir Alfred Smithers."
 },
 {
  "sid": "s10",
  "text": "Dongola - History\nThe Dongola area has been an important centre of Nubian civilisation for many centuries. The region is particularly associated with the medieval Christian kingdom of Makuria, whose capital was located at Old Dongola, south of the modern city.\nOld Dongola became an important political, religious and cultural centre in medieval Nubia. The site contains the remains of churches, monasteries, houses and other structures that reflect the history of the kingdom.\nOver time, political and religious changes transformed the region, and Dongola continued to develop as an important settlement along the Nile. The modern city remains connected with the wider cultural heritage of Nubia."
 },
 {
  "sid": "s11",
  "text": "Gemas - Eat\nAnyone emerging from the disappointing cuisine of the trains will likely end up in Curry Point or Wang Lai in the row of shophouses on the left on the street straight out of the station exit. This is fortunate as both these near neighbours are surprisingly good quality and good value."
 },
 {
  "sid": "s12",
  "text": "Inca Highlands - Get around\nTo visit sites, easiest is to hire a driver, particularly as part of a tour; cheaper is to use buses that go to main tourist sites. For access to and from Machu Picchu, rail is the main option (helicopters are possible but very expensive).\nIf mobility-impaired, you will not be able to engage in more demanding treks such as the Inca trail, but horseback treks are possible, and Machu Picchu itself can be visited."
 }
]
