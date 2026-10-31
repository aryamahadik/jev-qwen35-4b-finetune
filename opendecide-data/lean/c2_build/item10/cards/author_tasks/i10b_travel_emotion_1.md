# Item 10 card authoring i10b_travel_emotion_1

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10b_travel_emotion_1.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are passages from a community travel guide about places: what a place is like, how to get there and around, what to see and do, and how to stay safe.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: feeling and tone. Invent your own 5 to 8 feeling or mood labels that suit this kind of text. Spell out the dividing line between similar feelings by what the text says or does. The last option must be a catch-all for texts with no clear feeling. Do not use any ready-made emotion list (not the usual handful of basic emotions, not a positive / negative / neutral scale, not a list of dozens of emotions).
Card 1 angle: writer's feeling: the feeling the writer shows or describes.
Card 2 angle: reader's feeling: the feeling a typical reader would most likely have after reading the text.
Card 3 angle: overall mood: the mood or tone the text gives off as a whole, apart from any one sentence.
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

{"task_id": "i10b_travel_emotion_1",
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
  "text": "Ouro Preto\nOuro Preto, in Central Minas Gerais, is one of Brazil's best-preserved colonial towns and a UNESCO world heritage site. Among other historical and colonial cities of Minas Gerais (Tiradentes, São João del Rei, Mariana and Diamantina), Ouro Preto is one of the most popular travel destinations in Brazil."
 },
 {
  "sid": "s02",
  "text": "Dong Dang - Get in\nOnce you cross the border from Pingxiang to Vietnam, there are several taxis waiting for you. Prices should be around US$5 and it takes about 15 min to Dong Dang. The taxi will probably take you to some private minibus company which will offer you transportation to Hanoi. Initially, they will ask US$10/person, but don't pay more than US$5/person. The trip to Hanoi takes a few hours."
 },
 {
  "sid": "s03",
  "text": "Beiwudang Mountain Scenic Area\nThe Beiwudang Mountain Scenic Area (北武当山风景区) is located in Fangshan County, Lüliang City, Shanxi Province. It is one of the birthplace of Taoism in China and a sacred place of Taoism in the north. It is known as the first mountain in Shanxi. The scenic area has 72 peaks, 32 cliffs and 24 streams.\nNot to be confused with Wudang Mountain National Park (Hubei)."
 },
 {
  "sid": "s04",
  "text": "Breweries in Franconia - By car\nYou should know this already, but do not drink and drive under any circumstances. While some places listed here are indeed best reached with a car, the local roads can be curvy and treacherous and both snow and fallen leaves are a serious risk for almost half the year. Don't get too frustrated when you're stuck behind someone admiring the landscape and going way slower than the legal speed limit and leave the risky overtaking maneuvers to the locals."
 },
 {
  "sid": "s05",
  "text": "Bulolo - Understand\nBulolo was once an important gold dredging centre. Eight large dredges were built and used in the Bulolo River, and several of these dredges can still be seen abandoned today, slowly being reclaimed by the jungle. The major industry is now forestry and there are large plantings of Klinki pine (Norfolk Island pine) trees. It is in an area with a vast number of butterflies and other insects."
 },
 {
  "sid": "s06",
  "text": "Mago National Park\nMago National Park is in south-western Ethiopia, towards the border with South Sudan and Kenya. It is east of the Omo River, and stretches south towards the Chew Bahir basin. Omo National Park is on the western side of the Omo River.\nMago National Park is rich in wildlife with few human inhabitants. The vegetation is mainly savannah grassland and savannah bush, extending across an area of 2,160 km2. Mammal species total 81, including hartebeest, giraffe, roan antelope, elephant, lion, leopard and perhaps even a rare black rhino. Temperatures swing between 14 and 41 and rainfall is low."
 },
 {
  "sid": "s07",
  "text": "Milford Track - Climate\nCareful planning is essential as the track is remote and subject to extreme weather. The peak season runs from late October to late April. Outside this window, the track is only suitable for experienced alpine trampers due to snow and flood risks. All walkers must be prepared for the area's legendary rainfall by packing high-quality wet-weather gear and a complete set of dry clothing."
 },
 {
  "sid": "s08",
  "text": "Salkantay trail - Sleep\nAccommodation ranges from campsites and simple hospedajes to lodges used by tour groups. Soraypampa, Collapampa and Lucmabamba have basic lodging or camping options, and Aguas Calientes has a wide range of hotels and hostels. In the busier dry season, booking ahead is useful, especially if you do not have camping gear.\nCamping is possible in many places, and wild camping may be tolerated, but use established campsites where practical. They are better for sanitation, water access and reducing damage to the trail environment. Carry a warm sleeping bag; the night at Soraypampa is especially cold, while lower camps are warmer and more humid.\nIf staying in basic hospedajes, do not assume there will be heating, reliable electricity, hot showers or bedding suitable for cold weather. A sleeping bag liner or light sleeping bag can still be useful."
 },
 {
  "sid": "s09",
  "text": "Pangyo - Understand\nThe area is surrounded by Mt. Cheonggyesan (Mount Blue Stream, 618m) and Geumtosan (Mount Gold Soil) to the north, and Mt. Barasan to the south, with Unjungcheon and Geumtocheon, tributaries of Tancheon, flowing through the center of the city.\nThe etymological origin of Pangyo derives from a Chinese character \"Pan (wide wooden piece)\" and \"Gyo (bridge)\". Pangyo was a wooden bridge located at Unjungcheon (Stream Unjung). Unjung derives from the Chinese character \"Un (cloud)\" and \"Jung (In midst)\". Based on Feng-Shui Theory, of all the districts (-dong) in Pangyo, Unjung stands out, having a mountain at the back and a stream in front. During spring and fall, when diurnal temperature shift is severe, there is much fog in Unjungdong."
 },
 {
  "sid": "s10",
  "text": "Biu - Understand\nThe town is predominantly inhabited by the Biu ethnic group, but also boasts a diverse mix of other ethnicities, creating a vibrant cultural tapestry. The locals communicate in the Biu language, also known as Biu-Mandara, while Hausa and Kanuri are also widely spoken, reflecting the town's linguistic diversity.\nAgriculture is the backbone of Biu's economy, with maize, millet, and sorghum being major crops, alongside livestock rearing, which is also a common practice. This agricultural focus has contributed to the town's economic growth and stability."
 },
 {
  "sid": "s11",
  "text": "Altoona (Wisconsin)\nAltoona is a city with a population of nearly 7,900 (2019) people, in Eau Claire County in Wisconsin. Altoona is well known for its focus on outdoor recreation. It attracts fishers on the lake and bikers on its trails to enjoy the fresh air."
 },
 {
  "sid": "s12",
  "text": "Baggao - Understand\nBaggao was established by the Spanish in the 19th century along the foothills of the Sierra Madre. It sits on the valley of the Pared River, a tributary of the Cagayan River. It is named after the Ibanag verb for washing on account of the numerous streams and springs in town.\nBaggao is primarily an agricultural town, with decades of political instability caused by the New People's Army insurgency hindering the recognition of the town's natural attractions until the early 2000s."
 }
]
