# Item 10 card G-LEX read I10-ext-rA-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/extract_answers/I10-ext-rA-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 25. Answers expected: 25.

## Instructions

You are checking how clearly the options on a decision card are written. The card asks one question about a short text. Each option has a short name and a one-sentence definition. You will not see any real text to classify.

Do this for EVERY card in this file, and for EVERY option on each card:
1. "meaning": restate, in ONE line of at most 25 words and in your own words, what the option means. Do not copy the definition word for word.
2. "example": write ONE short example text of one or two plain sentences (at most 40 words) that clearly belongs to that option under its definition. It should read like a passage a reader could really see, fit this option, and not fit the other options on the card. Do not repeat the option name inside the example.

Rules:
- Use plain everyday English. Do not use outside facts about real people, places or organisations.
- Do not change, add or drop option names or cards. Do not say which option a card's question should be answered with.
- Your restatements and examples are only checked. They are never labels and never training data.

## Answer contract

Write ONE JSON object, and nothing else (no text before or after it), to the answer file named at the top. task_id must be "I10-ext-rA-001".
{"task_id": "I10-ext-rA-001",
 "answers": [
   {"qid": "<the qid of a card>",
    "options": [
      {"name": "<option name exactly as given>", "meaning": "one line", "example": "one short example text"}
    ]}
 ]}

Give one entry in "answers" for every card in the items, and one entry in "options" for every option of that card. Copy each qid and
each option name exactly as given.

## Cards (JSON; answer every item exactly once)

[
 {
  "qid": "q55ae809fbb",
  "kind": "choice",
  "who_decides": "A travel guide editor decides which section a passage belongs in, because readers look for each kind of information under its own heading.",
  "question": "Which section of a travel guide does this passage belong in?",
  "options": [
   {
    "name": "staying safe",
    "definition": "Pick this when the main point of the text is a warning about danger or a safety rule for the visitor, even if travel is mentioned."
   },
   {
    "name": "what to see and do",
    "definition": "Pick this when the text names specific sights, activities or tours and tells the visitor to go to them or take part."
   },
   {
    "name": "where to stay",
    "definition": "Pick this when the text covers places to sleep, such as hotels, huts or camping, or how to book them."
   },
   {
    "name": "getting there",
    "definition": "Pick this when the text explains how to reach the place from outside it, by road, rail, boat or flight from another town or country; if the trip starts inside the place, pick getting around."
   },
   {
    "name": "getting around",
    "definition": "Pick this when the text explains how to move between spots inside the place, by local bus, taxi, rental or walking route, and the main point is how to move, not a warning about danger."
   },
   {
    "name": "what it is like",
    "definition": "Pick this when the text describes the character, scenery, history or size of the place without naming a sight or activity to go to; if it names one, pick what to see and do."
   }
  ]
 },
 {
  "qid": "q5db6727aa4",
  "kind": "choice",
  "who_decides": "A help-desk volunteer who routes forum posts to the right helper, because a post sent to the wrong kind of helper wastes time for everyone.",
  "question": "What does the poster most want from a helper?",
  "options": [
   {
    "name": "restore an old behaviour",
    "definition": "Pick this only when the poster wants a feature, look or way of working from an earlier version brought back, and does not simply want a new way to do the task."
   },
   {
    "name": "get a step to work",
    "definition": "Pick this when the poster describes a specific action that fails, shows an error or does nothing, and asks how to make that action succeed; if no attempt has failed and they simply ask how to do it, pick learn how to do it instead."
   },
   {
    "name": "learn how to do it",
    "definition": "Pick this when the poster wants instructions for a task they have not yet tried or got working, with no failed attempt described."
   },
   {
    "name": "something else",
    "definition": "Pick this when the post asks for none of the above, such as a feature wish, a general complaint with no question, or a request for a free opinion."
   },
   {
    "name": "is it a bug",
    "definition": "Pick this when the poster asks whether the behaviour is a software fault or is expected or normal, and does not ask how to change anything; if they ask how to make it work, pick get a step to work instead."
   }
  ]
 },
 {
  "qid": "q12bffe320e",
  "kind": "choice",
  "who_decides": "A cook or cookbook editor deciding how to label a recipe's cooking method so that readers can find it.",
  "question": "Which one best describes the main cooking method, meaning the step that does the most to cook or set the food?",
  "options": [
   {
    "name": "no heat",
    "definition": "Pick when no step cooks the food with heat; the food is only mixed, tossed, layered, poured or served cold."
   },
   {
    "name": "oven bake",
    "definition": "Pick when the main cooking happens inside an oven, covered or uncovered; a dish simmered on a stove is pot boil or simmer instead."
   },
   {
    "name": "pan or grill",
    "definition": "Pick when the food is fried, seared or toasted by direct contact with a pan, skillet, grill or sandwich press; if the same food is cooked in the oven, pick oven bake instead."
   },
   {
    "name": "pot boil or simmer",
    "definition": "Pick when the main cooking is boiling or simmering food in liquid in a pot or saucepan for a set time; pick steep or brew instead if the liquid is only poured over and left to sit."
   },
   {
    "name": "steep or brew",
    "definition": "Pick when hot water is poured over the ingredient and left to sit or infuse, with no set boiling time in a pot; a liquid boiled for several minutes is pot boil or simmer instead."
   },
   {
    "name": "something else",
    "definition": "Pick when the main step is fermenting, freezing, smoking or another method not listed here, and no listed method does the most cooking."
   }
  ]
 },
 {
  "qid": "q422fac9c32",
  "kind": "choice",
  "who_decides": "The forum helper, or the writer themself, decides how the poster feels so they can reply in a suitable tone and urgency.",
  "question": "What feeling does the writer show or describe in the post?",
  "options": [
   {
    "name": "urgent worry",
    "definition": "Pick this when the writer says they need the fix now, mentions a deadline, a document about to be sent, or a risk to their work, or says they are desperate."
   },
   {
    "name": "stuck and fed up",
    "definition": "Pick this when the writer says a fix has failed again and again or they have been stuck for a long time, and sounds exasperated, but gives no deadline or fear of consequences."
   },
   {
    "name": "curious",
    "definition": "Pick this when the writer mainly asks why something happens or whether it is intended or a bug, without complaining about it."
   },
   {
    "name": "pleased to share",
    "definition": "Pick this when the writer reports a fix they found or a useful tip and sounds proud or happy about it."
   },
   {
    "name": "something else",
    "definition": "Pick this when the writer shows no clear feeling of any of the above kinds, or shows mixed feelings that do not settle on one."
   },
   {
    "name": "matter-of-fact",
    "definition": "Pick this when the writer only lists facts, steps, or settings in plain words and shows no feeling about them and asks no why question."
   }
  ]
 },
 {
  "qid": "q772637774f",
  "kind": "choice",
  "who_decides": "An editor sorting incoming stories into subject queues, because each queue has a different reviewer.",
  "question": "Which area of public life is this story mainly about?",
  "options": [
   {
    "name": "emergencies and accidents",
    "definition": "The main point is an event that puts people or buildings at risk and calls in fire, police, or rescue crews, such as a fire, crash, or scare; if the main point is treating an illness or a birth, pick \"patient care\" instead."
   },
   {
    "name": "match and team news",
    "definition": "The main point is a game, a team, a player, or a coach, such as a result, a transfer, or a sacking."
   },
   {
    "name": "vote and leadership",
    "definition": "The main point is who wins, loses, stands for, or quits a vote for public office or party leadership, or a boycott of one; pick \"government decisions\" instead when the story is about a law, budget, or official order with no vote or candidate in focus."
   },
   {
    "name": "government decisions",
    "definition": "The main point is an official act such as a law, budget, ruling, or ministerial order; if the story is about who holds or seeks office, pick \"vote and leadership\" instead."
   },
   {
    "name": "other subject",
    "definition": "Pick this only when the main subject is none of the above, such as science, computers, weather, pollution, or everyday life."
   },
   {
    "name": "food and relief",
    "definition": "The main point is hunger, a food shortage, or aid sent to people in need; pick this over \"patient care\" even when sickness is mentioned, because the supply of food or aid is the main point."
   },
   {
    "name": "patient care",
    "definition": "The main point is illness, a birth, treatment, hospital work, or a medicine supply for people who need medical help; if the main point is hunger or the supply of food or aid, pick \"food and relief\" instead."
   }
  ]
 },
 {
  "qid": "qb0e8b7b5b9",
  "kind": "choice",
  "who_decides": "A civic-news indexer who files stories by the level of decision-making they touch, so that local readers can find the decisions that affect them.",
  "question": "At which level of decision-making does the matter mainly sit?",
  "options": [
   {
    "name": "local council",
    "definition": "Pick it when the decision is made by a city, town, district or local council or its officials, rather than by a regional or national body."
   },
   {
    "name": "something else",
    "definition": "Pick it only when the text names no decision-maker at any of these levels, such as a story that only describes events or people's views."
   },
   {
    "name": "national government",
    "definition": "Pick it when the decision is made by the country's central government or its national parliament, and not by a state, province, city or outside body."
   },
   {
    "name": "international body",
    "definition": "Pick it when the decision is made by a group of countries or an international organisation, rather than by one country's own government; pick 'national government' when only one country decides."
   },
   {
    "name": "regional government",
    "definition": "Pick it when the decision is made by a state, province or region's own government or assembly; pick 'national government' when only the national level is involved."
   },
   {
    "name": "private organisation",
    "definition": "Pick it when the decision is made by a company, charity or other non-government group acting on its own, and no government makes or approves it."
   }
  ]
 },
 {
  "qid": "q28f47a780f",
  "kind": "choice",
  "who_decides": "A fact-checker deciding how far to trust a story's main facts, because each kind of source needs a different check.",
  "question": "What do the story's key facts mainly rest on?",
  "options": [
   {
    "name": "eyewitness account",
    "definition": "The key facts come from people who saw the event or were at the scene and speak in their own words, such as a passer-by, a fan, or a resident; pick \"official statement\" when the speaker is on duty or in an official role."
   },
   {
    "name": "written record",
    "definition": "The key facts come from a document, filing, report, or published text that the writer names or describes, not from a person speaking; pick \"count or measure\" if the document's main content is totals."
   },
   {
    "name": "mixed or unclear",
    "definition": "The key facts come from several sources with none dominant, or the text names no source for them; use this only when no other option clearly fits."
   },
   {
    "name": "count or measure",
    "definition": "The key facts are figures someone counted or measured, such as votes, scores, deaths, attendance, or amounts; pick this over the others whenever the figures are the main facts, even if an official or a document gave them."
   },
   {
    "name": "official statement",
    "definition": "The key facts are what a person in an official role said on the record, such as a minister, a police spokesperson, or a company head; pick \"written record\" if the facts come from a document the writer read, and \"count or measure\" if they are mainly figures."
   }
  ]
 },
 {
  "qid": "q0e75699426",
  "kind": "choice",
  "who_decides": "A labeller reading a travel guide entry decides which feeling a typical reader is most likely to have about making the trip, so that guide texts can be grouped by how they leave the reader.",
  "question": "After reading, what is the reader most likely to feel about making the trip?",
  "options": [
   {
    "name": "daunted",
    "definition": "Pick this when the text stresses hard conditions such as remote roads, cold, long distances, danger or high cost, so a reader would think the trip will be difficult; the stress on difficulty is the dividing line from at ease."
   },
   {
    "name": "curious",
    "definition": "Pick this when the text leaves a reader wanting to learn more about the history, nature or people of the place, but gives no pull toward actually going there; wanting to know without wanting to travel is the dividing line from keen to visit."
   },
   {
    "name": "keen to visit",
    "definition": "Pick this when the text makes the place sound appealing and names what to see or do, so a reader would want to go there; a pull toward travelling, not just knowing, is the dividing line from curious."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the text gives a reader no clear reason to feel any of the options above, for example when it is only a short list of names, dates or unrelated details."
   },
   {
    "name": "at ease",
    "definition": "Pick this when the text stresses simple conditions such as easy transport, cheap or nearby options, plenty of places to stay or a well set up route, so a reader would think the trip will be simple; the stress on ease is the dividing line from daunted."
   }
  ]
 },
 {
  "qid": "q2eeb2911d8",
  "kind": "choice",
  "who_decides": "A park visitor deciding which listing to attend needs to know what kind of activity it is, so they can pick the sort of outing they want.",
  "question": "What kind of activity is the main thing this program offers?",
  "options": [
   {
    "name": "hands-on class",
    "definition": "Pick this when participants learn by doing the activity themselves, such as a craft, a practice session, or handling an object; the dividing line from a watch or listen show is that the participant performs the task rather than only watching someone else do it."
   },
   {
    "name": "display to view",
    "definition": "Pick this when visitors look at art or objects on display at their own pace with no set talk or performance; if a leader takes the group past the display at set times or gives a talk, pick watch or listen show instead."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the program fits none of the labels above, such as a competition, a service project, or a mix with no clear main activity; if the text names a competition, sport, or service as the main activity, pick this label."
   },
   {
    "name": "guided walk",
    "definition": "Pick this when the main activity is walking a trail or route with a leader pointing things out and walking is the centre of the program; if the walk is only a short lead-in to a craft or lesson, pick the activity that follows it instead."
   },
   {
    "name": "social event or party",
    "definition": "Pick this when the program is a set evening or day gathering built around food, drink, music, dancing, or dressing up, where meeting and mingling is the main point; a talk or concert where people only sit and listen is a watch or listen show instead."
   },
   {
    "name": "watch or listen show",
    "definition": "Pick this when the audience mainly watches or listens to a presenter, performer, or live demonstration and does not do the activity being shown; if participants are asked to do the same task that is being demonstrated, pick hands-on class instead."
   }
  ]
 },
 {
  "qid": "q4e4cae54d5",
  "kind": "choice",
  "who_decides": "A reader who sorts government news decides the main purpose of each release so it goes to the right team and is passed on correctly.",
  "question": "What is the main job this release is trying to get done?",
  "options": [
   {
    "name": "report what happened",
    "definition": "The text states a result, a number, a finished step or a decision already made, with no request to readers; pick it when the news is about the past or present."
   },
   {
    "name": "something else",
    "definition": "Pick this only when none of the five options above fits the main purpose, for example when the text has no clear aim."
   },
   {
    "name": "ask readers to act",
    "definition": "The text gives readers a specific thing to do now, such as check something, register, take a safety step or follow a rule; pick it only when there is a direct request to the reader."
   },
   {
    "name": "praise people or work",
    "definition": "The text thanks, honours or celebrates people or a group for their work; pick it when recognition is the main purpose, not a result to report."
   },
   {
    "name": "plan what comes next",
    "definition": "The text sets out a future step, start date or plan that is not yet done; pick it when the main news is what will happen, not what has already happened."
   },
   {
    "name": "argue a view",
    "definition": "The author makes a case for a position or defends a policy in order to change readers' minds; pick it when persuasion is the main purpose, not a plain request."
   }
  ]
 },
 {
  "qid": "q0d7e298402",
  "kind": "choice",
  "who_decides": "A help-desk volunteer who routes forum posts by the kind of reply they need, because a setting tip, a walkthrough and a bug report each go to different helpers.",
  "question": "What kind of answer would settle this post?",
  "options": [
   {
    "name": "file or download",
    "definition": "Pick this when the answer is a new copy of the program, a patch, or a file the poster must get and use, rather than a change made inside the software."
   },
   {
    "name": "step-by-step walkthrough",
    "definition": "Pick this when the answer needs several ordered steps to reach the wanted result; if one single change is enough, pick a setting to change instead."
   },
   {
    "name": "a setting to change",
    "definition": "Pick this when one setting, option or menu choice inside the software would give the wanted result, and that result is directly possible; if several ordered steps are needed, pick step-by-step walkthrough instead."
   },
   {
    "name": "something else",
    "definition": "Pick this when the answer is only a thank-you, a question back to the poster, or a kind of answer not listed above."
   },
   {
    "name": "workaround",
    "definition": "Pick this when the wanted result is not directly possible, so the answer would be a different route to a similar result that goes around the limit; if the answer is that nothing can be done, pick confirmed bug or limit instead."
   },
   {
    "name": "confirmed bug or limit",
    "definition": "Pick this when the answer is that the behaviour is a real defect or a real limit of the software, with no fix or route the poster can take themselves."
   }
  ]
 },
 {
  "qid": "q1b8c2f3798",
  "kind": "choice",
  "who_decides": "A help volunteer who decides how much background to ask for and which answer to give first, since the reply depends on what the poster has already tried.",
  "question": "How far has the poster already got with the problem?",
  "options": [
   {
    "name": "tried fixes, none worked",
    "definition": "The poster lists fixes already tried, such as restarting, repairing, reinstalling or changing a setting, and none solved it; pick it when every attempt failed."
   },
   {
    "name": "using a workaround",
    "definition": "The poster has a different route that avoids the goal, such as a script or another program, and wants the original route fixed; pick it when the workaround replaces the goal rather than reaching part of it."
   },
   {
    "name": "nothing tried yet",
    "definition": "The poster states the problem and the question but names no step taken to solve it; pick it when the text names no attempt at a fix."
   },
   {
    "name": "partial answer found",
    "definition": "The poster reached part of the goal through a found method, but a piece still fails or is missing; pick it when some of the goal works and the rest is still open."
   },
   {
    "name": "solved, wants better way",
    "definition": "The poster already has a working answer and asks only for a simpler, cleaner or more reliable method; pick it when the goal is fully met and only the method is in question."
   }
  ]
 },
 {
  "qid": "qfd78e96100",
  "kind": "choice",
  "who_decides": "The volunteer centre's scheduling coordinator decides where the work happens, so volunteers know what conditions to expect and whether they can travel there.",
  "question": "Where does the volunteer actually do the work?",
  "options": [
   {
    "name": "something else",
    "definition": "Pick only when the text does not say where the work happens, or names a school or youth program site as the place of work."
   },
   {
    "name": "outdoors in the open",
    "definition": "Pick when the work is done outside on land such as a farm, garden, or park at a fixed spot, where weather matters; dividing line: outside work at one place, not travel between homes or streets."
   },
   {
    "name": "from home",
    "definition": "Pick when the volunteer does the work from their own home on a computer or phone and does not travel to a site; dividing line: no travel to a place for the work."
   },
   {
    "name": "indoors at a site",
    "definition": "Pick when the work happens inside one building the volunteer travels to, such as a kitchen, food bank, or office; dividing line: all the work stays inside one building."
   },
   {
    "name": "out in the community",
    "definition": "Pick when the volunteer moves between several places, or goes to people's homes or streets to deliver, visit, or do outreach; dividing line: moving between places, not staying at one spot."
   }
  ]
 },
 {
  "qid": "qde49671a36",
  "kind": "choice",
  "who_decides": "A course designer decides which job a passage should do in a lesson plan, so it is placed where that job is needed.",
  "question": "What job does this passage do inside a course?",
  "options": [
   {
    "name": "explains an idea",
    "definition": "Pick this when the passage says what a concept is or how it works, in plain statements rather than steps, so the learner understands it."
   },
   {
    "name": "gives a judging rule",
    "definition": "Pick this when the passage names a standard the reader should check against to decide whether something is good, reliable, or right."
   },
   {
    "name": "tells history or origin",
    "definition": "Pick this when the passage says when, where, or by whom a topic arose or developed, and does not explain how it works."
   },
   {
    "name": "something else",
    "definition": "Pick this when none of the other jobs fit, such as a sign-up or admin note, and the passage neither teaches nor guides the learner."
   },
   {
    "name": "gives steps to do",
    "definition": "Pick this when the passage tells the reader, in order, what to do to carry out a task, so the learner can act on it."
   }
  ]
 },
 {
  "qid": "qd8e81cbf89",
  "kind": "choice",
  "who_decides": "The volunteer who sorts incoming help-forum posts, so each post is matched to the kind of help the poster is asking a helper for.",
  "question": "What does the poster want from a helper?",
  "options": [
   {
    "name": "something else",
    "definition": "Pick this when the poster asks for nothing from a helper and only shares news, a result, or feedback."
   },
   {
    "name": "add-on or outside tool",
    "definition": "Pick this only when the poster asks for a third-party extension, template, or outside program to do the job, not for a built-in method."
   },
   {
    "name": "find a setting",
    "definition": "Pick this when the poster knows a named option or value exists and wants help locating it; a request to choose between methods belongs under pick an approach."
   },
   {
    "name": "pick an approach",
    "definition": "Pick this when the poster names more than one way to reach a goal and wants help choosing the best one; pick find a setting instead when the text is about where one known control is."
   },
   {
    "name": "permanent cure",
    "definition": "Pick this when the poster wants the root cause removed so the problem does not come back, or says a stopgap is not enough; pick quick workaround when a temporary way round is accepted."
   },
   {
    "name": "quick workaround",
    "definition": "Pick this when the poster wants a way around the problem now and says the fix is temporary or accepts a stopgap; pick permanent cure instead when they want it gone for good."
   }
  ]
 },
 {
  "qid": "q3a8db2f5c4",
  "kind": "choice",
  "who_decides": "A research reader or database curator who files each preprint by the kind of result it reports, so people searching for one kind of finding can find it.",
  "question": "What kind of result is the abstract's main finding?",
  "options": [
   {
    "name": "new thing identified",
    "definition": "The main result is a previously unknown item, such as a gene, group, type, species or class, found and named by the authors. Pick this over how something works when the item itself was not known before."
   },
   {
    "name": "how something works",
    "definition": "The main result describes the shape, parts or step-by-step action of a thing already known, such as a structure or mechanism. Pick this over new thing identified when the thing was already known and the new content is its detail."
   },
   {
    "name": "link seen",
    "definition": "Two or more things were measured and found to go together or change together, with no deliberate change by the authors shown to cause the other. Pick this over cause shown when nothing was changed on purpose."
   },
   {
    "name": "no clear effect",
    "definition": "The main result is that a factor or change made no clear difference to what was measured. Pick this only when the main result is that nothing changed; if an effect was found, pick cause shown or link seen instead."
   },
   {
    "name": "cause shown",
    "definition": "The authors deliberately changed a condition, factor or gene and reported that the change produced the result. Pick this over link seen whenever the authors made the change on purpose; link seen is only for things observed together without such a change."
   },
   {
    "name": "tool performs well",
    "definition": "The main result is that a method, tool or workflow works well on tests, judged by accuracy, speed or reliability. Pick this over cause shown when the result is how good the tool is rather than what a changed condition did to the biology."
   }
  ]
 },
 {
  "qid": "q039d06bcea",
  "kind": "choice",
  "who_decides": "A research reader who sorts new biology preprints by their main subject so that each one reaches the right specialist group.",
  "question": "What is the study mainly about?",
  "options": [
   {
    "name": "brain and behaviour",
    "definition": "Pick this when the main subject is how a linked group of nerve cells or brain areas drives what an animal senses, does, or feels; a single molecule's action is molecules inside cells instead."
   },
   {
    "name": "drugs and treatments",
    "definition": "Pick this when the main subject is finding, improving, or testing a compound meant to treat or block a disease; if the focus is how the disease-causing germ itself behaves, pick germs and their hosts instead."
   },
   {
    "name": "new tools and methods",
    "definition": "Pick this when the main subject is a new measurement, scoring, or analysis method for biology data, and the biology itself is only the test case."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the main subject is none of the above, such as populations in the wild, evolution over long periods, or a whole ecosystem."
   },
   {
    "name": "body tissue and its change",
    "definition": "Pick this when the main subject is how a tissue, organ, or cell layer changes in structure or condition, such as through damage, fatigue, or repair; if the text is about one molecule's action, pick molecules inside cells instead."
   },
   {
    "name": "germs and their hosts",
    "definition": "Pick this when the main subject is a microbe, virus, or gut bacterium and what it does to or inside its host; if the focus is the compound that fights it, pick drugs and treatments instead."
   },
   {
    "name": "molecules inside cells",
    "definition": "Pick this when the main subject is how one named molecule, protein, or channel inside cells works or is switched on or off; a whole group of nerve cells or a whole organ is not this, so pick brain and behaviour or body tissue and its change instead."
   }
  ]
 },
 {
  "qid": "q564b46780f",
  "kind": "choice",
  "who_decides": "A help volunteer who sorts new forum posts into the right queue, so the reply goes to the right kind of helper.",
  "question": "What kind of problem does the poster describe?",
  "options": [
   {
    "name": "how-to method",
    "definition": "The poster asks for the steps or menu path to do a task with a feature that exists, and the text describes no failure; pick it when the wanted answer is a sequence of actions, not a formula or query."
   },
   {
    "name": "formula or query syntax",
    "definition": "The poster asks for the exact formula, function or database query that gives a result, often showing code they tried; pick it when the wanted answer is an expression to type, not a list of menu steps."
   },
   {
    "name": "bug in ordinary use",
    "definition": "The software misbehaves while the poster works on an open document, such as crashing, changing content, or acting differently from an earlier version; pick it when the failure happens during normal work, not at install, update or start-up."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the text is about none of the above, such as account, licensing or forum matters, and asks for no task, formula, fault or missing feature."
   },
   {
    "name": "install or update failure",
    "definition": "The program will not install, update or start properly, including start-up error messages or a repeated update loop; pick it when the failure happens before any document opens."
   },
   {
    "name": "missing feature or add-on",
    "definition": "The poster asks for a function the software does not have, or asks whether an add-on or script could do something; pick it when the text says the feature is absent, not when it worked before or a feature exists but is hard to find."
   }
  ]
 },
 {
  "qid": "q77a18b15b2",
  "kind": "choice",
  "who_decides": "A recipe reader choosing which section of a cookbook or menu a recipe belongs in, based on its main food.",
  "question": "Which kind of food is the dish mainly built around, meaning the ingredient with the largest share of the recipe?",
  "options": [
   {
    "name": "meat or fish",
    "definition": "Pick when meat, poultry, fish or seafood is the largest share of the recipe; a meat used only as a small topping or garnish does not count."
   },
   {
    "name": "sugar or sweetener",
    "definition": "Pick when sugar, syrup or another sweetener is the largest share, more than any fruit; a fruit flavoured with a little sugar is vegetable or fruit."
   },
   {
    "name": "starch",
    "definition": "Pick when bread, flour, grain, pasta or potatoes are the largest share; for a potato dish, pick vegetable or fruit instead unless the potatoes weigh more than all other vegetables together."
   },
   {
    "name": "vegetable or fruit",
    "definition": "Pick when vegetables, beans, corn, fruit or berries are the largest share and no starch or sugar is larger."
   },
   {
    "name": "egg or dairy",
    "definition": "Pick when eggs, milk, cream or cheese is the largest share and no meat, fish, vegetable, starch or sugar is larger."
   },
   {
    "name": "something else",
    "definition": "Pick when the largest share is a spice, herb or seasoning, or when no ingredient is clearly the largest."
   }
  ]
 },
 {
  "qid": "q1fd4c08dfe",
  "kind": "choice",
  "who_decides": "A course editor who sorts study material so that each reader gets the right kind of text for their needs.",
  "question": "What kind of study material is this text?",
  "options": [
   {
    "name": "community notice or manifesto",
    "definition": "Pick this when the text speaks for a group or cause, stating its rules, values or requests to readers in order to win agreement or action; if it describes a learning course, pick course overview instead."
   },
   {
    "name": "course overview",
    "definition": "Pick this when the text says what a course, book or unit will cover, who it is for, or how it is set out, without teaching the content itself; if it teaches the content, pick textbook section instead."
   },
   {
    "name": "textbook section",
    "definition": "Pick this when the text explains a subject in connected paragraphs with background, detail and reasons, so that the reader builds understanding across the whole text; if it only describes what a course will cover, pick course overview instead."
   },
   {
    "name": "dictionary-style entry",
    "definition": "Pick this when the text gives a short definition, a brief timeline, or a list of facts about one named thing and does not teach how to do anything; if it explains a whole subject over several connected paragraphs, pick textbook section instead."
   },
   {
    "name": "worked example",
    "definition": "Pick this when the main content is a sequence of steps for a calculation, proof, or formula, shown with symbols or numbers; if the steps are mostly explained in prose, pick textbook section instead."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the text is a story, opinion piece, or other material that fits none of the five kinds above."
   }
  ]
 },
 {
  "qid": "qb914ba8391",
  "kind": "choice",
  "who_decides": "A map editor who files each passage under the kind of place it describes, so readers can compare places of the same kind.",
  "question": "What kind of place or setting does this passage mainly describe?",
  "options": [
   {
    "name": "small town",
    "definition": "The passage describes one small settlement or township, often with a small population and few services. Dividing line: the subject is one small settlement, not a large city and not a wider area containing several towns."
   },
   {
    "name": "countryside",
    "definition": "The passage describes open land, valleys, mountains or forest with few settlements as the main setting. Dividing line: the natural land is the subject, not a settlement or a government-defined area."
   },
   {
    "name": "big city",
    "definition": "The passage describes one large built-up urban area, with many suburbs, big road networks or a large population. Dividing line: the subject is a single large city; a small settlement is small town, and a wider area with several towns is region or district."
   },
   {
    "name": "coast or waterway",
    "definition": "The passage describes a sea coast, shore, river or lake as the main feature of the setting. Dividing line: the water or shoreline is the central subject, not the land behind it."
   },
   {
    "name": "something else",
    "definition": "The passage describes a setting that none of the other labels fits, such as a station, a single building or an event venue. Pick this only when no other label fits the main setting."
   },
   {
    "name": "region or district",
    "definition": "The passage describes a wide administrative area, such as a state, county or district, and the several towns inside it. Dividing line: the subject is the wider area itself, not one settlement within it."
   }
  ]
 },
 {
  "qid": "q8478f3e10e",
  "kind": "choice",
  "who_decides": "A conservator who fills the materials line of a catalogue record and needs one main making method for each object.",
  "question": "How was the object mainly made?",
  "options": [
   {
    "name": "printed",
    "definition": "Made by pressing inked surfaces such as a plate, block, or screen onto paper or cloth. Pick this when the text says the image was transferred from a plate, block, or screen, even if that plate was drawn by hand."
   },
   {
    "name": "modelled or cast",
    "definition": "Made by shaping soft material such as clay or wax, or by pouring liquid material into a mould. Pick this when the text says the form was built up, modelled, moulded, or cast."
   },
   {
    "name": "painted or drawn",
    "definition": "Made by hand, applying colour or marks directly to the surface with a brush, pencil, or ink. Pick this when the text says the image was applied by hand, not transferred from another surface."
   },
   {
    "name": "something else",
    "definition": "Pick this only when none of the methods above is the main one, such as a photograph or a mixed assembly of unrelated parts."
   },
   {
    "name": "carved or cut",
    "definition": "Made by taking material away from one solid piece, such as wood, stone, or horn. Pick this when the text says the form was cut, carved, or shaped out of a single block."
   },
   {
    "name": "woven or stitched",
    "definition": "Made by interlacing threads or fibres, or by sewing pieces together. Pick this when yarn, thread, weaving, or sewing is the main method."
   }
  ]
 },
 {
  "qid": "q4a301cc3f5",
  "kind": "choice",
  "who_decides": "A government public affairs lead choosing the main goal of each release so the team can judge whether the message reached its aim.",
  "question": "What is the main thing this release is trying to get done?",
  "options": [
   {
    "name": "draw visitors or fans",
    "definition": "Pick this when the release aims to get people to visit a park, attend an event or enjoy a place or activity; if the aim is to grow companies, jobs or an industry, pick grow jobs or business."
   },
   {
    "name": "protect people from harm",
    "definition": "Pick this when the release describes a step or rule meant to stop a crime, danger, illness or loss; a step that only reports results without aiming to prevent harm is share a fact."
   },
   {
    "name": "ask readers to act",
    "definition": "Pick this when the release tells readers to do a task of their own, such as applying, registering, getting tested or reporting something; a fact reported with no task for the reader is share a fact."
   },
   {
    "name": "grow jobs or business",
    "definition": "Pick this when the release aims to attract investment, build an industry, or create or support jobs and companies; if the release aims to bring people to a place or activity, pick draw visitors or fans."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the release's main aim is clearly none of the other options, such as thanking people, honouring a person or recognising a milestone."
   },
   {
    "name": "share a fact",
    "definition": "Pick this when the release simply reports what happened or was decided, with no request that readers do a task and no push to attend or visit; if it asks readers to do a task, pick ask readers to act."
   }
  ]
 },
 {
  "qid": "q397539db8c",
  "kind": "choice",
  "who_decides": "A news desk editor choosing which follow-up queue a story joins, because first reports, updates, and results are checked differently.",
  "question": "Where does this story stand at the time it is published?",
  "options": [
   {
    "name": "other stage",
    "definition": "Pick this only when the text does not report the course of a specific event at all, such as a background piece, a feature, or a general list."
   },
   {
    "name": "new step",
    "definition": "The story is still open and the text reports a fresh move, such as a statement, plan, meeting, or announcement, with more steps still to come; pick \"final outcome\" if nothing is left to decide."
   },
   {
    "name": "final outcome",
    "definition": "The result is settled and announced, such as a final count, score, verdict, or completed decision, with nothing left to come; pick \"after-effects\" if the main point is what that result caused."
   },
   {
    "name": "after-effects",
    "definition": "The result is already known and the text covers what followed, such as damage, shortages, reactions, costs, or repairs; pick this over \"final outcome\" when the consequences are the main point."
   },
   {
    "name": "first news",
    "definition": "The event has just been reported and key facts such as cause, toll, or next steps are still unknown or unconfirmed; pick \"new step\" instead when the text refers to an earlier report or decision in the same story."
   }
  ]
 },
 {
  "qid": "qd640dcf325",
  "kind": "choice",
  "who_decides": "A help volunteer who decides which questions to ask back first, since the first useful reply depends on how the problem shows up.",
  "question": "How does the problem show itself to the poster?",
  "options": [
   {
    "name": "wrong text or breaks",
    "definition": "The characters or line breaks themselves change, such as extra blank lines, lost paragraph breaks or missing letters; pick it when the words or breaks differ, not when only their placement or size is off."
   },
   {
    "name": "no failure shown",
    "definition": "The text describes no failing behaviour at all, only a request for steps, a formula or a feature; pick it when no wrong behaviour is named anywhere in the text."
   },
   {
    "name": "crash or freeze",
    "definition": "The program closes by itself or stops responding so that it must be forced to quit; pick it when the program stops working, not when it keeps running and shows a message."
   },
   {
    "name": "wrong layout or spacing",
    "definition": "The words are right but sit, size or space wrongly on the page, such as a picture in the wrong place, lines too far apart or a page that looks too small; pick it when the problem is where things sit, not what the characters are."
   },
   {
    "name": "wrong value in a cell",
    "definition": "A spreadsheet cell shows a number, date or error result the poster did not expect; pick it when the wrong thing is a calculated result in a cell, not words in a text document."
   },
   {
    "name": "slow to respond",
    "definition": "The program works but takes minutes to open, load or react, and the text says it finishes eventually; pick it when it is slow but does not stop, not when it freezes or closes."
   },
   {
    "name": "error message shown",
    "definition": "The program keeps running but shows a message box or names a missing file; pick it when the program stays open, not when it closes or stops responding."
   }
  ]
 }
]
