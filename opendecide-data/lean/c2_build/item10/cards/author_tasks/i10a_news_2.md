# Item 10 card authoring i10a_news_2

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_news_2.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are short news articles from a community news website, on all kinds of topics.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: subject area: which area of public life the story is mainly about, where neighbouring answers are easy to confuse.
Card 2 angle: story stage: where the story stands (first report, new development, result, aftermath), where neighbouring answers are easy to confuse.
Card 3 angle: sourcing: what the story mainly rests on (an official statement, a document, an eyewitness, a count of something), where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_news_2",
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
  "text": "Six-year-olds trigger emergency response with toy nuclear reactor in Germany\nThey had taken an old computer case, with a radioactivity symbol and warning notice that they had printed, affixed to the side, to create a \"nuclear reactor\".\n\nThe boys abandoned their plaything in the street to take a break at home. It was encountered by a passer-by, who called out the emergency services. The children later returned to their play to find the street cordoned off by police and fire services, who were warning surrounding residents to stay in their homes via local radio.\n\nIt was not until later, when the children's parents read news reports on the Internet of the incident, that it was realized that the children's play \"nuclear reactor\" had been the cause of the incident."
 },
 {
  "sid": "s02",
  "text": "Wreck of August 6 airliner crash recovered from sea off Italy\nThe wreck of the plane ATR72 that fell into the sea near Sicily, Italy on August 6 has been recovered. One of the two black boxes that contained the communication recording, and the complete set of instruments and commands in the cockpit, was recovered.\n\nOne of the three people who were still missing from the accident was found, while there is yet no sign of the other two persons. The identity of the recovered corpse is not yet known (and the identification is expected to be difficult).\n\nA survey published today by the Italian association Intesaconsumatori (Union of Consumers) said that 61% of Italians are afraid to fly, while 41% of population feels less safe about plane safety than they did one month earlier. According to the survey, 20% would be ready to get off the plane, or refuse to get in the plane, if they found that the airline is different from the one they were told when they bought the ticket.\n\n==Related previous article=="
 },
 {
  "sid": "s03",
  "text": "England do enough against Ecuador; through to quarter-final\nFor the neutral football fan the game was not especially attractive to look at. There were only 7 shots on target in the 90 minutes and neither team controlled the play well. The scrappy match was broken by up 37 fouls.\n\nThe game had temperatures at around 90 degrees Fahrenheit, which caused several English players, including Beckham, to suffer from heat exhaustion and dehydration. Beckham was sick on the pitch shortly after his goal and was substituted before the end.\n\nEcuador had the best of the first 45 minutes. The slow tempo of the game seemed to lead to simple errors of concentration from England and favoured Ecuador's passing play.\n\nEcuador had slightly more ball possession over the game and also the first chance. John Terry's back header to his keeper fell short but Ashley Cole slid in to deflect Carlos Tenorio's shot onto Paul Robinson's crossbar.\n\nIn the second half England put more pressure on Ecuador's goal. However, passes into lone striker Wayne Rooney – who played 90 minutes for the first time since he recovered from injury – were often off-target.\n\nEngland's best chance to score from free play followed Wayne Rooney trickery on the left touchline. The striker evaded his marker but Frank Lampard spooned Rooney's cut back high over the bar.\n\nBeckham's free kick was a trademark fast curled pass from over 30 yards which beat the opposition wall and took a small touch off the fingertips of Cristian Mora before nestling into the bottom right corner of the net. The goal meant David Beckham had broken an English record by scoring in the 1998, 2002 and 2006 World Cups, the first English player ever to score in three different World Cups.\n\nEngland were scheduled to meet the winner of game 52, Portugal, in the quarter-final of the World Cup in Gelsenkirchen on July 1.\n\n==Round of sixteen==\n\nMatch 51\n\nAttendance: 52'000\n\n==Formations==\n===England===\n\nSubstitutes\n- 77' Jamie Carragher 82' for Joe Cole\n- 87' Aaron Lennon for Beckham\n- 92'+ Stewart Downing for Steven Gerrard\n\ndenotes one goal scored.\n----\n\n===Ecuador===\n\nSubstitutes\n- 69' Christian Lara for Edwin Tenorio\n- 72' Ivan Kaviedes for Carlos Tenorio\n\ndenotes one goal scored.\n\n==Officials==\n\nReferee: Frank De Bleeckere\n\nAssistant referee: Peter Hermans\n\nAssistant referee: Walter Vromans\n\nFourth referee: Oscar Ruiz\n\nFifth referee: Jose Navia"
 },
 {
  "sid": "s04",
  "text": "MDC pulls out of Zimbabwe elections\nHe said that he is doing this because \"the outcome [of the elections] is determined by... Mugabe himself,\" and is therefore not fair.\n\n\"We in the MDC have resolved that we will no longer participate in this violent, illegitimate sham of an election process,\" said Tsvangirai in a press conference made today. \"The courageous people of this country and the people of the MDC have done everything humanly and democratically possible to deliver a new Zimbabwe and a new government.\"\n\nTsvangirai also said that governments worldwide should intervene to help improve the situation in the country."
 },
 {
  "sid": "s05",
  "text": "Canadian nuclear reactor shutdown causes worldwide medical isotope shortage\nThe nuclear reactor at Chalk River, Ontario in Canada was shut down on Thursday, May 14 by the Atomic Energy of Canada Limited (AECL) due to a leak of heavy water. Government officials say that by Saturday the demand for medical isotopes will no longer be met, due to the shortage caused by the closure.\n\nMedical isotopes are used in diagnostic procedures for cancer, heart disease and other medical conditions. When radioactive isotopes are injected into the body, radiologists can view higher radiation via medical imaging, enabling them to make a more accurate diagnosis.\n\nEstimates suggest that the reactor will be shut down for approximately one month for repairs. The Chalk River Laboratories produce 33% of the international supply of medical isotopes.\n\nLisa Raitt, Natural Resources Minister said, \"A secure supply of medical isotopes is not only an issue for Canada, it is an international issue that is being addressed co-operatively by all isotope-producing countries.\"\n\n\"It may mean that if you have an elective study booked... that patient is going to be deferred and will have to wait until the situation is resolved. I'm reasonably confident that for most patients, if they're having an acute problem, that problem is going to be dealt with - and the greater the acuity, the more likelihood it's going to be dealt with quickly and expeditiously,\" said Dr. Karen Gulenchyn, a nuclear medicine expert.\n\n\"The government of Canada is engaging international isotope producers as well as companies such as MDS Nordion, Lantheus, and Covidien, who all play key roles in securing medical isotope supply for North America,\" said Raitt and Health Minister Leona Aglukkaq.\n\nIn December 2007, the 52-year-old reactor was shut down and the Canadian House of Common stepped in to restart the reactor."
 },
 {
  "sid": "s06",
  "text": "Football: Italian club AC Milan sacks Vincenzo Montella as manager\nOn Monday, Italian football club AC Milan sacked manager Vincenzo Montella. Gennaro Gatusso, manager of AC Milan's youth team, was named as Manetella's successor.\n\nMonetella's team started this season with winning ten out of twelve fixtures in all competitions. However, in fourteen Italian Serie A league matches played so far, Monetella's men won just six matches, losing six and drawing two matches. Having spent £205 million in the summer transfer window, AC Milan has won just 20 points in Serie A. They are seventh in the league table, and eighteen points behind the league leaders SSC Napoli.\n\nThe Milanese club named Gatusso as their new manager. Gatusso played for Milan from 1999 till 2013. As a player, Gatusso has won two Serie A titles and two UEFA Champions League titles with AC Milan. Since 2013, AC Milan has not finished in the top three spots in the league table.\n\nMilan has qualified for this year's UEFA Europa League's knockouut phase. Montella's last match for the Rossoneri ended in a 0–0 draw against Torino FC at home. Milan has not scored in the last four league matches at home."
 },
 {
  "sid": "s07",
  "text": "Stagnant air spreads across England\nStagnant air spread today across southern and eastern parts of England including the capital city, London.\n\nThe police, fire and water services as well as the Met Office were all asked to give an explanation for the smell. The police and fire services were at a loss as to how to respond, but Thames Water assured its customers that there were no problems with any of its water treatment plants. A Met Office spokesperson explained that \"over the last few days, we've had fresh, strong winds from an easterly direction. As a result some of our air is coming from continental Europe.\" The westerly wind which England usually receives is less pungent, having arrived from the Atlantic.\n\nGeoff Dollard, an air quality expert, told the Daily Mail \"The feeling is that it's natural\".\n\nThe origin of the smell is therefore thought to be from manure recently spread on continental European farms (from France, the Netherlands, Belgium or Germany). A spokesman for the National Farmers Union said: \"This has happened before. In Holland and Belgium they are spreading millions of tons of muck at the moment. It is a countryside smell.\"\n\nThe stench is expected to die down over the weekend but Met Office spokeswoman Helen Chivers says that if there are no south or south-westerly winds, \"it is possible it may hang around until Tuesday\"."
 },
 {
  "sid": "s08",
  "text": "Fire brings down two domes of historical Russian cathedral\nA fire broke out at the Trinity Cathedral in St. Petersburg, causing the main dome and another dome to collapse, early in the evening of August 25.\n\nFirefighters fought the blaze, and a helicopter was pressed into service. Staff, emergency service workers and passers by rescued treasured items from the cathedral.\n\nFour hours later, St. Petersburg emergency department spokeswoman Lyudmila Rubasova said the fires were contained but the remaining domes were damaged. Later a departmental spokesmen said that the fire was extinguished.\n\n\"The main dome has been destroyed but we could not stop the fire because it was so high and now other domes are in flames,\" said a spokesman for Russia's emergencies ministry.\n\nThe cause of the fire was not immediately known, but acting St. Petersburg emergency department chief Leonid Belyayev said the blaze seems to have started on scaffolding on the outside of the church, which was undergoing restoration.\n\nHe also said that the most valuable icons and other items had been saved, and that structural damage beneath the roof area was minor.\n\nThere are no reported injuries."
 },
 {
  "sid": "s09",
  "text": "Sextuplets born in Vancouver, Canada\nCanada's first sextuplets, four boys and two girls, were born on the weekend of January 6th 2007 at the B.C. Women's hospital in Vancouver. The first baby was delivered vaginally, while the following 5 had to be removed by emergency caesarean section.\n\nDr. Liz Whynot, the Women's Hospital president said the first baby was delivered around 8:30 p.m. Saturday night, with the others born early Sunday. Whynot said the parents \"... understand there is a lot of public interest in the birth of their babies, they are feeling overwhelmed. So they're asking for their privacy to be respected.\"\n\nThe children weigh about 800 grams each. The mother was reported to be in her 25th week of pregnancy and the babies will require a period of time in the hospital's neonatal intensive care unit as most pregnancies last 40 weeks.\n\n==Related stories=="
 },
 {
  "sid": "s10",
  "text": "Wikipedia and sister projects back online after server failure\nFrom approximately 1:00 p.m. (18:00 UTC) to 4:00 p.m. (22:00 UTC) Eastern Standard Time (EST), the popular free encyclopedia Wikipedia, alongside its sister projects (including Wikinews), went offline due to major server outages. Downtime was later attributed to overheating at the Project's central data center in Amsterdam.\n\nAccording to a post made by Mark Bergsma at the Wikimedia Foundation's technical blog, the servers \"shut themselves down\" to avoid further heat damage.\n\nAdministrators reportedly attempted a shift of traffic to the Project's servers in Florida. However, \"it turned out that this failover mechanism was now broken, causing the DNS resolution of Wikimedia sites to stop working globally.\"\n\nAccording to the Project's official Twitter account, programmers were able to resolve most of the server problems by around 4:00 p.m. EST. Since the situation with the servers in Amsterdam is still ongoing, some users may still experience lingering service glitches due to \"caching effects\"."
 },
 {
  "sid": "s11",
  "text": "Canadian Liberal vote heads to third ballot\nVoting continued today in the Liberal Party of Canada leadership convention with frontrunner Michael Ignatieff maintaining his lead on the second ballot with 31.6% of delegate support but showing limited growth potential. Bob Rae remained in second place but narrowed the gap slightly to win 24.1% support. He was helped by the endorsement of Joe Volpe and Scott Brison who withdrew their candidacies following the first ballot.\n\nStephane Dion, who was only two votes ahead of Gerard Kennedy on the first ballot solidified his third place standing with 20.8% support on the second ballot winning almost 100 votes more than Kennedy who remained in fourth place. Martha Hall Findlay who had been eliminated after the first ballot threw her support to Dion. Ken Dryden brought up the rear with 4.7% support.\n\nFollowing the announcement of the vote result Dryden released his delegates but threw his personal support to Bob Rae while Kennedy withdrew in order to support Dion.\n\nVoting on the third ballot is now underway with results expected in mid-afternoon."
 },
 {
  "sid": "s12",
  "text": "Malawi appeals for further humanitarian aid\nBingu wa Mutharika, president of Malawi, has declared the massive food shortages in his country a national disaster. The declaration comes on the heels of mounting criticism from his opposition as well as church groups in Malawi that have urged him to do more to highlight the problem. Mutharika has also been criticised for denying reports of casualties from hunger-related illnesses. The United Nations World Food Program has welcomed the declaration, stating that he is finally acknowledging the seriousness of the situation. The UN estimates that five million people will be in need of aid in the coming year.\n\nThe president has noted that all 28 districts of his country are affected and that, in addition to the 300,000 tons of food being imported from South Africa, another 144,000 will be needed.\n\n\"We are facing a national disaster affecting the lives of our people,\" he said.\n\nThe food shortages have been blamed on one of the worst harvests Malawi has experienced in over a decade as well as the growing HIV/AIDS crisis. Because Malawi is a landlocked country whose economy is almost entirely dependent on agriculture, poor harvests can have drastic impacts on the population. Most of the country feeds themselves through subsistence farming. Additionally, during the mid-eighties and nineties Malawi took in over a million refugees from Mozambique, which placed a significant strain on the economy but also opened it to foreign aid.\n\nThe United Nations has attempted to restructure Malawi's economy through programs from the World Bank and the International Monetary Fund.\n\nRelief agencies have been scrambling to deal with the crisis. UNICEF Regional Director for Eastern and Southern Africa, Per Engebak has said, \"The numbers of malnourished children are many times higher than the normal emergency threshold.\"\n\nIt is predicted that the disaster will be worse than the humanitarian crisis that plagued the country three years ago. Admissions to Nutrition Rehabilitation Units, run by a coalition of aid agencies as well as the Ministry of Health, have risen by 25 percent.\n\nChurch groups in the country have been assisting in the emergency. The Council of Churches in Malawi, which brings together 22 denominations, has been applying pressure to the government. In addition to the food crisis, Rev Matiya Nkhoma has highlighted the problems of political instability in the country.\n\nThe food crisis is not just a danger to Malawi."
 }
]
