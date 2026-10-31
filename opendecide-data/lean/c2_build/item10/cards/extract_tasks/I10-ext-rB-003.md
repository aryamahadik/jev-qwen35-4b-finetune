# Item 10 card G-LEX read I10-ext-rB-003

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/extract_answers/I10-ext-rB-003.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 10. Answers expected: 10.

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

Write ONE JSON object, and nothing else (no text before or after it), to the answer file named at the top. task_id must be "I10-ext-rB-003".
{"task_id": "I10-ext-rB-003",
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
  "qid": "q58178ac613",
  "kind": "choice",
  "who_decides": "A civic-news indexer who files stories by the level of decision-making they touch, so that local readers can find the decisions that affect them.",
  "question": "At which level of decision-making does the matter mainly sit?",
  "options": [
   {
    "name": "regional government",
    "definition": "Pick it when the decision is made by a state, province or region's own government or assembly; pick 'national government' when only the national level is involved."
   },
   {
    "name": "private organisation",
    "definition": "Pick it when the decision is made by a company, charity or other non-government group acting on its own, and no government makes or approves it."
   },
   {
    "name": "something else",
    "definition": "Pick it only when the text names no decision-maker at any of these levels, such as a story that only describes events or people's views."
   },
   {
    "name": "international body",
    "definition": "Pick it when the decision is made by a group of countries or an international organisation, rather than by one country's own government; pick 'national government' when only one country decides."
   },
   {
    "name": "national government",
    "definition": "Pick it when the decision is made by the country's central government or its national parliament, and not by a state, province, city or outside body."
   },
   {
    "name": "local council",
    "definition": "Pick it when the decision is made by a city, town, district or local council or its officials, rather than by a regional or national body."
   }
  ]
 },
 {
  "qid": "qee4baaf7b8",
  "kind": "choice",
  "who_decides": "A museum labeller or routing clerk decides which kind of object a description is about, so the right page or filter is shown to the visitor.",
  "question": "What kind of object does this description mainly describe?",
  "options": [
   {
    "name": "sculpture or bust",
    "definition": "Pick this when the work is a solid three-dimensional figure, carved, cast or modelled, such as a bust or statue; pick box or assemblage instead if objects are arranged inside a box or frame."
   },
   {
    "name": "poster",
    "definition": "Pick this when the printed sheet was made to advertise or publicly announce an event, show, product or message, even if the artist is famous."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the text names a kind of object that none of the other options covers, such as a drawing, a photograph or a building."
   },
   {
    "name": "painting",
    "definition": "Pick this when the text says the work is painted with paint, brushwork or hand-applied colour on canvas, board or paper as a single original piece, not a printed copy."
   },
   {
    "name": "box or assemblage",
    "definition": "Pick this when the work is a three-dimensional piece built inside a box or frame from paper cut-outs, small objects or printed scraps, and not one carved or modelled form."
   },
   {
    "name": "print",
    "definition": "Pick this when the work was made by pressing ink from a stone, plate or block, in editions, and was made to be collected as an art work; pick poster instead if the sheet was made to advertise or announce something."
   },
   {
    "name": "stained glass window",
    "definition": "Pick this when the text says the work is coloured glass set into a window, including a memorial window."
   }
  ]
 },
 {
  "qid": "q6f855b095c",
  "kind": "choice",
  "who_decides": "A visitor choosing a program needs to know where it takes place, such as inside a building or outside, so they can dress for it and plan the trip.",
  "question": "Where does this program take place?",
  "options": [
   {
    "name": "something else",
    "definition": "Pick this only when the text does not say where the program is held, or names a place that none of the labels above fit, such as a zoo, a city street, or an online session; if the text names a building or outdoor area, pick that label instead."
   },
   {
    "name": "historic site or venue",
    "definition": "Pick this when the text names the venue as a historic site, fort, battery, mansion, or estate from an earlier era and the event itself is held at that place; if the past era is only a theme, such as costume or music, while the event is held at an ordinary building, pick indoors in a building instead."
   },
   {
    "name": "outdoors on trails or grounds",
    "definition": "Pick this when the program takes place on a trail, open field, campground, amphitheatre, or other open ground, or the text says it goes outside; if the place is a lake, bay, pond, or beach, pick water edge instead, and if the place is a named historic site, pick historic site or venue instead."
   },
   {
    "name": "water edge",
    "definition": "Pick this when the program takes place next to or on a lake, bay, pond, river, or beach, such as at a fishing pier or shoreline; water that is only the subject of a talk, with the event held elsewhere, does not count."
   },
   {
    "name": "indoors in a building",
    "definition": "Pick this when the text names a building, room, hall, or centre as the place the program is held and does not say it goes outside; if the text says it is held on a porch, patio, or deck, pick outdoors on trails or grounds instead."
   }
  ]
 },
 {
  "qid": "q8572c2a731",
  "kind": "choice",
  "who_decides": "A person who routes open-data requests to the right subject team decides this so the dataset reaches the team that knows its area.",
  "question": "Which part of public life is this dataset mainly about?",
  "options": [
   {
    "name": "something else",
    "definition": "Pick this only when the main subject fits none of the five options above, such as a different area of public life."
   },
   {
    "name": "money and grants",
    "definition": "Pick this when the text mainly lists amounts paid out, budgets, grants, or expenditure, rather than the places or things they pay for."
   },
   {
    "name": "wildlife and plants",
    "definition": "Pick this when the text is mainly about living species, their listing, or their protection."
   },
   {
    "name": "land and buildings",
    "definition": "Pick this when the text is mainly about structures, property, zones, or boundaries, and not about money spent on them."
   },
   {
    "name": "courts and justice",
    "definition": "Pick this when the text mainly tracks cases through charges, hearings, prosecution, or sentences, not the original incident."
   },
   {
    "name": "crime and policing",
    "definition": "Pick this when the text mainly records reported incidents, calls, arrests, or police work as they happened, not cases moving through court."
   }
  ]
 },
 {
  "qid": "q730840e545",
  "kind": "choice",
  "who_decides": "A park visitor deciding which listing to attend needs to know what kind of activity it is, so they can pick the sort of outing they want.",
  "question": "What kind of activity is the main thing this program offers?",
  "options": [
   {
    "name": "social event or party",
    "definition": "Pick this when the program is a set evening or day gathering built around food, drink, music, dancing, or dressing up, where meeting and mingling is the main point; a talk or concert where people only sit and listen is a watch or listen show instead."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the program fits none of the labels above, such as a competition, a service project, or a mix with no clear main activity; if the text names a competition, sport, or service as the main activity, pick this label."
   },
   {
    "name": "hands-on class",
    "definition": "Pick this when participants learn by doing the activity themselves, such as a craft, a practice session, or handling an object; the dividing line from a watch or listen show is that the participant performs the task rather than only watching someone else do it."
   },
   {
    "name": "watch or listen show",
    "definition": "Pick this when the audience mainly watches or listens to a presenter, performer, or live demonstration and does not do the activity being shown; if participants are asked to do the same task that is being demonstrated, pick hands-on class instead."
   },
   {
    "name": "guided walk",
    "definition": "Pick this when the main activity is walking a trail or route with a leader pointing things out and walking is the centre of the program; if the walk is only a short lead-in to a craft or lesson, pick the activity that follows it instead."
   },
   {
    "name": "display to view",
    "definition": "Pick this when visitors look at art or objects on display at their own pace with no set talk or performance; if a leader takes the group past the display at set times or gives a talk, pick watch or listen show instead."
   }
  ]
 },
 {
  "qid": "q57ffaba6f2",
  "kind": "choice",
  "who_decides": "A map editor who files each passage under the kind of place it describes, so readers can compare places of the same kind.",
  "question": "What kind of place or setting does this passage mainly describe?",
  "options": [
   {
    "name": "countryside",
    "definition": "The passage describes open land, valleys, mountains or forest with few settlements as the main setting. Dividing line: the natural land is the subject, not a settlement or a government-defined area."
   },
   {
    "name": "region or district",
    "definition": "The passage describes a wide administrative area, such as a state, county or district, and the several towns inside it. Dividing line: the subject is the wider area itself, not one settlement within it."
   },
   {
    "name": "coast or waterway",
    "definition": "The passage describes a sea coast, shore, river or lake as the main feature of the setting. Dividing line: the water or shoreline is the central subject, not the land behind it."
   },
   {
    "name": "big city",
    "definition": "The passage describes one large built-up urban area, with many suburbs, big road networks or a large population. Dividing line: the subject is a single large city; a small settlement is small town, and a wider area with several towns is region or district."
   },
   {
    "name": "something else",
    "definition": "The passage describes a setting that none of the other labels fits, such as a station, a single building or an event venue. Pick this only when no other label fits the main setting."
   },
   {
    "name": "small town",
    "definition": "The passage describes one small settlement or township, often with a small population and few services. Dividing line: the subject is one small settlement, not a large city and not a wider area containing several towns."
   }
  ]
 },
 {
  "qid": "qe93f91d6ba",
  "kind": "choice",
  "who_decides": "A learner or course editor deciding what a passage is for, so it is used in the right way.",
  "question": "What is this passage mainly meant to help a learner do?",
  "options": [
   {
    "name": "carry out a real job",
    "definition": "Pick this when the text gives steps, checks or settings for a real-world job such as inspecting equipment, setting something up or building something; unlike the practise option, the goal is the finished real job, not a learning answer."
   },
   {
    "name": "understand an idea",
    "definition": "Pick this when the text explains how something works, what happened, or why, and does not ask the reader to do any task."
   },
   {
    "name": "practise a skill",
    "definition": "Pick this when the text sets questions, prompts or exercises that the reader must work through to build a skill; unlike the understand option, the reader is asked to produce something."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the main aim is none of these, for example the text describes a business or reports a finished result without teaching the reader or asking them to act."
   }
  ]
 },
 {
  "qid": "q5e568dd185",
  "kind": "choice",
  "who_decides": "A data librarian decides how far a researcher can trust the timing and completeness of an open dataset, because a wrong guess about its freshness can change the findings.",
  "question": "How current, complete or final is the data said to be?",
  "options": [
   {
    "name": "something else",
    "definition": "Pick when the text makes no main point about timing or completeness, or its main note is a change in how things are counted or defined."
   },
   {
    "name": "partial coverage",
    "definition": "Pick when the main caveat is that some values, groups or years are missing, hidden or left out, such as suppressed counts or unknown fields, rather than a point about timing."
   },
   {
    "name": "updated on a schedule",
    "definition": "Pick when the text says new data will be added or refreshed at stated intervals, such as monthly or quarterly, or says it is current; pick this over the fixed past period option whenever a future update is promised."
   },
   {
    "name": "fixed past period",
    "definition": "Pick when the text covers a closed span of past years and promises neither a future update nor a warning about revision."
   },
   {
    "name": "may still change",
    "definition": "Pick when the text says the figures are early, subject to audit, or open to revision; pick this over the other options whenever a warning about revision is given."
   }
  ]
 },
 {
  "qid": "qfdcf43c5ff",
  "kind": "choice",
  "who_decides": "A journal editor or library staff member who sorts new biology preprints by the kind of study they report, so readers can find the right type of work.",
  "question": "What kind of study does the abstract mainly report?",
  "options": [
   {
    "name": "lab experiments",
    "definition": "The main work is experiments the authors ran themselves on cells, organisms, materials or samples they collected or prepared, and the text names these as the core of the study. Pick this over existing data when the authors' own experiments are the core, and over balanced mix when only experiments are named as the core."
   },
   {
    "name": "computer or math model",
    "definition": "The main work is a mathematical model or computer simulation whose predictions or runs are the core of the study, with no new experiments named as central. Pick this over balanced mix when the model is the only kind named as the core."
   },
   {
    "name": "existing data",
    "definition": "The main work reanalyses data that already existed, such as public databases, past recordings or published sets, and the text names no new samples or experiments as the core. Pick this over lab experiments when the text says the authors only examined data gathered by others."
   },
   {
    "name": "balanced mix",
    "definition": "The text names two or more of the kinds above as equally central, and no single kind is clearly the core. Pick this only when no one kind is named as the core; if one kind is named as the core, pick that kind instead."
   },
   {
    "name": "something else",
    "definition": "The text reports no new study, data, model or tool of its own, such as a review of others' work or an opinion piece. Pick this only when none of the other kinds applies at all."
   },
   {
    "name": "new tool or method",
    "definition": "The main contribution is a software tool, algorithm or workflow that others can use, presented as the product itself rather than as a finding about biology. Pick this over existing data when the text is mainly about the tool and not about what the data showed."
   }
  ]
 },
 {
  "qid": "q379906a7b0",
  "kind": "choice",
  "who_decides": "A help volunteer who sorts new forum posts into the right queue, so the reply goes to the right kind of helper.",
  "question": "What kind of problem does the poster describe?",
  "options": [
   {
    "name": "bug in ordinary use",
    "definition": "The software misbehaves while the poster works on an open document, such as crashing, changing content, or acting differently from an earlier version; pick it when the failure happens during normal work, not at install, update or start-up."
   },
   {
    "name": "how-to method",
    "definition": "The poster asks for the steps or menu path to do a task with a feature that exists, and the text describes no failure; pick it when the wanted answer is a sequence of actions, not a formula or query."
   },
   {
    "name": "install or update failure",
    "definition": "The program will not install, update or start properly, including start-up error messages or a repeated update loop; pick it when the failure happens before any document opens."
   },
   {
    "name": "formula or query syntax",
    "definition": "The poster asks for the exact formula, function or database query that gives a result, often showing code they tried; pick it when the wanted answer is an expression to type, not a list of menu steps."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the text is about none of the above, such as account, licensing or forum matters, and asks for no task, formula, fault or missing feature."
   },
   {
    "name": "missing feature or add-on",
    "definition": "The poster asks for a function the software does not have, or asks whether an add-on or script could do something; pick it when the text says the feature is absent, not when it worked before or a feature exists but is hard to find."
   }
  ]
 }
]
