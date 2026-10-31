# Item 10 card authoring i10a_gov_news_2

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_gov_news_2.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are news releases from a provincial government: announcements, programmes, funding, advisories and events.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: audience: which readers the release is mainly written for, where neighbouring answers are easy to confuse.
Card 2 angle: what changes: what the release says is new, different or ending, where neighbouring answers are easy to confuse.
Card 3 angle: money or rule: whether the release is mainly about money, a rule, a service or an event, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_gov_news_2",
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
  "text": "Weekly Traffic Advisories\nNOTE: The projects listed below are planned road and bridge work. For the most up-to-date provincial traffic notices, follow on X at call 511 or visit:\n\nCONTINUING WORK\n\nCAPE BRETON REGIONAL MUNICIPALITY: Crawley Creek Bridge, Point Aconi The Crawley Creek Bridge on Point Aconi Road is closed for repairs until Friday, September 5. A detour and traffic control are in place.\n\nCOLCHESTER COUNTY: Highway 104 Overpass, North River The Highway 104 westbound overpass is reduced to one lane for repairs until Friday, October 31. Work takes place weekdays from 7 a.m. to 6 p.m., but the lane is closed 24 hours a day. Signs are in place, and motorists should expect delays.\n\nCOLCHESTER COUNTY: Lower Portapique Bridge, Portapique The Lower Portapique Bridge on Trunk 2 is closed for repairs until further notice. The detours are East Montrose Road and West Montrose Road.\n\nCOLCHESTER COUNTY: Route 311, North River Route 311 from Farnham Mill Road to Mountain Lee Road is reduced to one lane for bridge work until Friday, October 31. Work takes place weekdays from 7 a.m. to 6 p.m. Motorists should expect delays.\n\nCOLCHESTER COUNTY: Slade Road, Tatamagouche Slade Road is closed between Lake Road and West Tatamagouche Road until further notice because of a bridge closure.\n\nCOLCHESTER COUNTY: Wittenburg Road, Wittenburg Wittenburg Road from Coldstream Road to Route 224 will be closed for culvert replacement until Friday, October 3. A detour and traffic control will be in place. Motorists should expect delays.\n\nHALIFAX REGIONAL MUNICIPALITY: Highway 107, Lower Sackville There are two closures on Highway 107 in Lower Sackville:\n\nthe northbound on-ramp to Highway 102 at Exit 4C the southbound on-ramp at the new Highway 102 overpass\n\nTraffic will be detoured to the Exit 4C roundabouts:\n\nHighway 102 northbound traffic will exit at the first roundabout Highway 102 southbound traffic and traffic heading toward Halifax or the Annapolis Valley will proceed to the second roundabout\n\nWork is expected to be complete Tuesday, September 16.\n\nINVERNESS COUNTY: Glendale Mountain Road, Glendale A section of Glendale Mountain Road two kilometres north of Highway 105 is closed for culvert replacement until Monday, September 15. A detour and traffic control are in place.\n\nINVERNESS COUNTY: Highway 105, Whycocomagh Highway 105 from 465 metres east of Morrison Road easterly for seven kilometres is reduced to one lane for paving and patching until Monday, September 29."
 },
 {
  "sid": "s02",
  "text": "Traffic Advisory, Highway 101\nHANTS COUNTY: Highway 101\n\nMotorists can expect delays on Highway 101 west of Mount Uniacke from 6:30 p.m. to 7:30 p.m. tonight, June 23. Traffic will be stopped in both directions while blasting takes place.\n\nA detour is available on Trunk 1 between Exit 3 and Exit 4."
 },
 {
  "sid": "s03",
  "text": "Changes Support Inclusion in the People’s House\nThe Government is modernizing the rules of the Nova Scotia House of Assembly to better reflect the diverse views of all Nova Scotians and create a more welcoming, inclusive environment, including changing references to “prayer” in the House rules.\n\n“The rules that govern this historic chamber must evolve to ensure Province House is truly the People’s House,” said Premier Tim Houston. “No matter the colour of a person’s skin, their gender, who they love, the language they speak or how they pray, they should feel welcomed by their Government.”\n\nRule 16 of the Rules and Forms of Procedure of the House of Assembly will be amended by replacing the words “read prayers” with the words “allow a moment of quiet reflection.”\n\n“As we welcome more newcomers and new residents to our province, it’s important that everyone sees themselves represented in the language we use within our democratic institutions,” said Premier Houston. “Our rules and the House itself will continue to evolve and change to ensure all Nova Scotians – current and future – feel included.”\n\nQuick Facts: -- the Nova Scotia legislature, consisting of the lieutenant-governor and the House of Assembly, is the legislative branch of the Government of Nova Scotia -- the assembly is the oldest in Canada, having first sat in 1758\n\nAdditional Resources: Current Rules and Forms of Procedure of the House of Assembly:"
 },
 {
  "sid": "s04",
  "text": "Municipalities to Participate in Wind Planning Project\nA unique pilot project involving wind energy development is set to begin for two municipalities in Nova Scotia.\n\nThe County of Cumberland and the Municipality of the District of Shelburne will receive funding to conduct a Wind Energy Development Plan.\n\nThe money will allow the municipalities to work with residents to identify locations in their communities where wind energy development is encouraged, discouraged or prohibited. The funding is also intended to increase public involvement around wind energy and educate Nova Scotians about the province's renewable energy and environmental goals.\n\nThe project, led by the Union of Nova Scotia Municipalities, will receive $80,000 from the province.\n\n\"Nova Scotia's goal of 40 per cent renewable electricity by 2020 will bring new opportunities for wind development around the province,\" said Energy Minister Bill Estabrooks. \"It's great to see communities engaged in the process early on, allowing developers and residents to work towards achieving our renewable goals in partnership.\"\n\n\"The development of these two municipal wind siting plans is an important step in helping municipalities respond proactively to their potential for wind energy development,\" said Clarence Prince, president of the Union of Nova Scotia Municipalities. \"Many of our municipalities have a great interest in, and the potential to develop wind energy as an important renewable energy source to make their communities more sustainable.\"\n\nMunicipalities are expected to complete their wind siting plans by December. If the pilot project is successful, the province may consider expanding the initiative to other municipalities."
 },
 {
  "sid": "s05",
  "text": "Traffic Advisory, Halifax Regional Municipality\nHALIFAX REGIONAL MUNICIPALITY: Trunk 3\n\nAn inspection of the closed bridge on Trunk 3 at the head of St. Margarets Bay has determined the bridge is structurally sound. Repairs to the abutments are underway and the bridge is expected to be open Wednesday, Nov. 10."
 },
 {
  "sid": "s06",
  "text": "Seven New Cases of COVID-19, Eight Recoveries\nToday, July 6, Nova Scotia is reporting seven new cases of COVID-19 and eight recoveries.\n\nSix cases are in Central Zone. Five are close contacts of previously reported cases and one is related to travel.\n\nThe other case is in Eastern Zone and is a close contact of a previously reported case.\n\nThe close contacts are part of a linked group of families and do not represent wide community spread.\n\nAll four health zones continue to be closely monitored for community spread.\n\n“Yesterday marked one million doses of COVID-19 vaccine administered in our province,” said Premier Iain Rankin. “This was a wonderful milestone, but we are not finished yet. We need to encourage our fellow Nova Scotians to go out and get the vaccine if they haven’t already.”\n\nAs of today, Nova Scotia has 44 active cases of COVID-19. Of those, two people are in hospital COVID-19 units.\n\nOn July 5, Nova Scotia Health Authority's labs completed 3,146 tests.\n\nAs of July 5, 1,011,039 doses of COVID-19 vaccine have been administered. Of those, 299,585 Nova Scotians have received their second dose.\n\n“Most of the cases we are seeing each day are connected to two contained clusters – one in Halifax and one in Glace Bay,” said Dr. Robert Strang, Nova Scotia’s chief medical officer of health. “There is no sign of community spread as a result of these clusters, but they do serve as a reminder of the importance of getting vaccinated as soon as you can. Nova Scotians who are 12 and older can book their COVID-19 vaccine online or by phone.”\n\nSince April 1, there have been 4,119 positive COVID-19 cases and 26 deaths. Cases range in age from under 10 to over 90. There are 4,049 resolved cases. Cumulative cases may change as data is updated in Panorama.\n\nTesting advice:\n\nNova Scotians with or without symptoms can book a test at for primary assessment centres across the province. Those with no symptoms are encouraged to use one of the primary assessment centres with drop-in testing, pop-up sites or public health mobile units if they want to be tested.\n\nMore information on testing can be found at\n\nAnyone with COVID-19 symptoms is advised to self-isolate and book a COVID-19 test. Everyone they live with must also self-isolate until the person receives their first negative test result."
 },
 {
  "sid": "s07",
  "text": "Traffic Advisory, Antigonish County\nANTIGONISH COUNTY: Canso Causeway\n\nLane closures will take place on Highway 104 at the Trunk Four intersection in Aulds Cove to the Causeway's swing bridge during night time hours, from 8 p.m. to 6 a.m.\n\nConstruction is expected to continue until the end of November.\n\nTraffic control is on site. Please use caution when travelling in the area."
 },
 {
  "sid": "s08",
  "text": "Positions for Adjudicative Agencies, Boards and Commissions\nThe government of Nova Scotia has launched its bi-annual campaign to attract qualified applicants for various adjudicative agencies, boards and commissions.\n\nAdjudicative boards are required to receive evidence, make findings of fact and law, or make decisions that can affect a person's liberty, security, or legal rights.\n\nOn Saturday, April 14, and Saturday, April 28, The Chronicle Herald and the Cape Breton Post will carry an advertisement listing the adjudicative agencies, boards and commissions that currently have vacancies or will have vacancies in the near future. The ad will run in upcoming editions of the Mi'kmaq Maliseet Nations News and le Courrier de la Nouvelle-Écosse.\n\nThe call for applications will also be available for a limited time on the government website at .\n\nThe province advertises opportunities to serve on its agencies, boards and commissions every spring and fall and makes appointments as vacancies arise.\n\nPositions are advertised to ensure fair notice is given to potential candidates. Departmental advisory committees screen potential members, according to a process introduced in 2003, to ensure that every member of each board is well qualified.\n\nEach committee provides a list of three to six qualified board applicants to the minister of the department concerned. The five-member committees are chaired by a human resources professional appointed by the Public Service Commission and include two other government employees and two members of the public, who are also selected in a competitive process.\n\nDescriptions have been prepared for all adjudicative board positions. These descriptions detail the qualifications needed, the selection criteria used and remuneration.\n\nAll documents are available on the Executive Council website at ."
 },
 {
  "sid": "s09",
  "text": "Repaving Projects Move Forward in Queens County\nQueens County\n\nRoute 208 and West Street are getting some new asphalt this summer.\n\nThe province is repaving six kilometres of Route 208 and 1.5 kilometres of West Street. This is part of a $1.8 million project in the county.\n\n\"We are providing real benefits to the people of Queens County,\" said Michael Baker, Minister of Transportation and Public Works. \"We are meeting our commitments to the people of the region while improving public safety.\"\n\nThe Route 208 project runs west from the county line of Lunenburg and Queens. The West Street project runs from Bridge Street to Potonac Street.\n\nDexter Construction Co. Ltd. was awarded the contract. The work is expected to be finished by Aug. 31.\n\nThe Department of Transportation and Public Works highways division manages more than 23,000 kilometres of roads in Nova Scotia. It maintains an inventory of 3,800 bridges and operates seven provincial ferries. Staff provide services from four district offices located in Bridgewater, Bedford, Truro and Sydney."
 },
 {
  "sid": "s10",
  "text": "Weekly Traffic Advisories\nNEW WORK\n\nCOLCHESTER COUNTY: Luther McNutt Bridge\n\nLuther McNutt Bridge on the Truro Road will be closed for removal and replacement of the bridge structure from Monday, Oct. 13 to Monday, Dec. 15.\n\nTraffic control will consist of detour signage. The road will be open to local traffic only.\n\nPICTOU COUNTY: Black Brook Bridge\n\nBlack Brook Bridge on Minto Road will be closed for removal and replacement of the bridge structure from Monday, Oct. 13 to Monday, Dec. 1. Detour signage will be available.\n\nCONTINUING WORK\n\nCAPE BRETON REGIONAL MUNICIPALITY: Highway 125\n\nHighway 125 near Exit 5 has a one-lane closure for night paving until Friday, Oct. 17.\n\nTraffic control consists of traffic control persons. A detour is available via Route 305. Work takes place from 7 p.m. to 6 a.m. on weekdays and 6 p.m. to 11 a.m. on weekends.\n\nCOLCHESTER COUNTY: Route 311\n\nRoute 311, for 5.3 kilometres from Onslow Road to the Stewarts Bridge, has intermittent one-lane closures to facilitate ditching, culvert work and repaving until Friday, Oct. 31.\n\nTraffic control consists of traffic control persons and a pilot vehicle. Work takes place from 7 a.m. to 8 p.m.\n\nCOLCHESTER COUNTY: Trunk 2\n\nTrunk 2 from Taggart Road to the Portapique River has a one-lane closure for ditching, culvert repairs and repaving until Friday, Oct. 31. Traffic control consists of traffic control persons. Work takes place from 7 a.m. to 8 p.m.\n\nDIGBY COUNTY: Meteghan River Bridge\n\nMeteghan River Bridge on Trunk 1 is closed until further notice. If traveling from Yarmouth towards Saulnierville on Trunk 1, a detour is available on Maxwellton Road, to Second Division Road, to Placide Comeau Road and back to Trunk 1.\n\nIf traveling from Halifax or Digby towards Meteghan River, a detour is available on the Placide Comeau Road, to Second Division Road, to Maxwellton Road and back to Trunk 1.\n\nGUYSBOROUGH COUNTY: Trunk 16\n\nTrunk 16 from Peas Brook to Halfway Cove Bridge, about 3.6 kilometres, has intermittent lane closures until Friday, Oct. 31.\n\nTraffic control consists of traffic control persons and a pilot vehicle. Work takes place from 6 a.m. to 9 p.m.\n\nHALIFAX REGIONAL MUNICIPALITY: Beaverbank Connector\n\nBeaverbank Connector and Highway 101 interchange ramps, from Sackville Drive to Highway 101, has a lane closure for paving until Friday, Oct. 31. Traffic control consists of flashing lights and signage."
 },
 {
  "sid": "s11",
  "text": "Seniors Program Directory Available\nNova Scotia seniors will be able to learn about the programs and services that are available to them with the help of the 2005 Programs for Seniors directory. The directory features information about active living, health care, transportation, housing, finances, legal matters and much more.\n\nThis year's Programs for Seniors is helping to celebrate a significant milestone as the Nova Scotia Seniors Citizens' Secretariat marks 25 years of serving Nova Scotia's seniors.\n\n\"The Nova Scotia Senior Citizens' Secretariat has been the voice for seniors for 25 years,\" said Valerie White, executive director of the secretariat. \"Programs for Seniors has been an important guide for seniors and their families since it was first published in 1981.\" The secretariat works with seniors to develop plans, policies and programs in partnership with the departments of Community Services, Health, Education, Service Nova Scotia and Municipal Relations and the Office of Health Promotion. It provides seniors with a single entry point to access programs and services in government.\n\nThe secretariat is distributing 75,000 copies of the directory across the province. Copies are free and are available at local pharmacies, public libraries and Sobeys stores."
 },
 {
  "sid": "s12",
  "text": "Bill Will Ban Importing Hydraulic Fracturing Wastewater\nNew legislation being tabled today, Dec. 2, will stop companies from importing or transporting wastewater from hydraulic fracturing into Nova Scotia.\n\n\"Nova Scotians are deeply concerned about the risks posed by fracking wastewater,\" said Environment Minister Randy Delorey. \"Today we are taking another step through legislation to ensure the protection of our environment, and consequently, the health of Nova Scotians.\"\n\nOne Nova Scotia company has treated wastewater from New Brunswick in the past, but it has already been stopped.\n\nThe province is continuing to address wastewater from shale gas exploration in Kennetcook six years ago. Next steps on fluids in Debert and Kennetcook will be announced soon.\n\nNova Scotia has a moratorium on hydraulic fracturing while an independent review is being carried out by David Wheeler.\n\nFor more information on the review, visit ."
 }
]
