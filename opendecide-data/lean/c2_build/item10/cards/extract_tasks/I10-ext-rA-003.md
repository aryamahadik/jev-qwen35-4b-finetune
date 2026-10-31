# Item 10 card G-LEX read I10-ext-rA-003

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/extract_answers/I10-ext-rA-003.json

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

Write ONE JSON object, and nothing else (no text before or after it), to the answer file named at the top. task_id must be "I10-ext-rA-003".
{"task_id": "I10-ext-rA-003",
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
  "qid": "q1a5be9ab5c",
  "kind": "choice",
  "who_decides": "A museum cataloguing staff member who fills in the making-method field of an object record.",
  "question": "Which making method does the description name as the main way the object was made?",
  "options": [
   {
    "name": "something else",
    "definition": "Pick this when the text names a method not listed here, such as photography or machine-making, or names no making method at all."
   },
   {
    "name": "woven or stitched",
    "definition": "Pick this when the text says the object was made by interlacing or sewing threads, fibres or cloth."
   },
   {
    "name": "cast in metal",
    "definition": "Pick this when the text says the object was made by melting metal and pouring it into a mould, so the shape comes from the mould."
   },
   {
    "name": "printed from a block",
    "definition": "Pick this when the text says the image was made by pressing ink from a prepared block, plate or screen onto paper or cloth, so copies can be made."
   },
   {
    "name": "carved or cut",
    "definition": "Pick this when the text says the shape was made by cutting, carving or chiselling material away from a solid piece, not by pouring or pressing."
   },
   {
    "name": "hand-painted or drawn",
    "definition": "Pick this when the text says the image was applied by hand with paint, ink or pencil directly onto the surface, one piece at a time."
   }
  ]
 },
 {
  "qid": "q1fdb8ad97e",
  "kind": "choice",
  "who_decides": "A museum education or digital team member who chooses which kind of text goes on a wall label, a web page or a record.",
  "question": "Which museum job would this description most suit as its main text?",
  "options": [
   {
    "name": "visitor label",
    "definition": "Pick this when the text is a few short sentences meant to be read standing in front of the object, pointing out what to look for or know right there."
   },
   {
    "name": "research essay",
    "definition": "Pick this when the text argues for a reading of what the object means and refers to other writing or sources to support it."
   },
   {
    "name": "catalogue entry",
    "definition": "Pick this when the text is a plain list of facts for the records, such as maker, date, materials and size, with little or no story told."
   },
   {
    "name": "something else",
    "definition": "Pick this when the text was written for a different job, such as a children's activity or an advert, or fits none of the four above better than the others."
   },
   {
    "name": "online story",
    "definition": "Pick this when the text is a longer piece that follows a thread of people, events or background in order, for a reader at home, and does not direct the eye to the object."
   }
  ]
 },
 {
  "qid": "q141fe7840a",
  "kind": "choice",
  "who_decides": "A museum writer or editor who decides which angle to build a new description around.",
  "question": "What do most of the description's words spend their time on?",
  "options": [
   {
    "name": "history",
    "definition": "Pick this when most words trace what happened to the object after it was made, such as where it went, who owned it or how it changed over the years."
   },
   {
    "name": "appearance",
    "definition": "Pick this when most words describe how the object looks, such as its shapes, colours, details or patterns, and what can be seen."
   },
   {
    "name": "symbolic meaning",
    "definition": "Pick this when most words explain what the image or object stands for, such as a belief, a proverb or a message, beyond what can be seen; the dividing line is that the text goes past looks to explain the message."
   },
   {
    "name": "something else",
    "definition": "Pick this when no single focus takes most of the words, or most of the words are about the museum, its building or its website."
   },
   {
    "name": "daily use",
    "definition": "Pick this when most words describe what the object was used for and how people handled or lived with it."
   },
   {
    "name": "maker",
    "definition": "Pick this when most words describe who made the object, such as an artist, craftspeople or a workshop, and their training or career; the dividing line is that the text is about the maker, not about what happened to the object later."
   }
  ]
 },
 {
  "qid": "q3d84132ee5",
  "kind": "choice",
  "who_decides": "A museum education staffer who chooses which short panel text to show visitors who want to know more about an object.",
  "question": "What does the visitor most need from this text?",
  "options": [
   {
    "name": "artist story",
    "definition": "Pick this when the text describes the maker's life, training, career, or working history; a summary of the steps used to make one object goes to how it was made instead."
   },
   {
    "name": "how it was made",
    "definition": "Pick this when the text explains the materials, techniques, steps, or process used to make this object; if the text describes the maker's life or career across many works, pick artist story instead."
   },
   {
    "name": "cultural background",
    "definition": "Pick this when the text places the work in its time, place, school, or tradition, such as a period, country, or art movement; if the text explains what the imagery or symbols mean, pick understand the meaning."
   },
   {
    "name": "archive access",
    "definition": "Pick this when the text is a collection or archive description that tells the visitor how to visit a reading room, request material by appointment, or browse finding aids; if the text describes one object to look at, pick one of the object-focused labels instead."
   },
   {
    "name": "understand the meaning",
    "definition": "Pick this when the text explains what the image or object stands for, its message, symbols, or the maker's intent; if the text places the work in its era, country, or tradition instead, pick cultural background."
   }
  ]
 },
 {
  "qid": "qe54db74471",
  "kind": "choice",
  "who_decides": "A museum collection editor who sorts descriptions by their main focus, so the right ones feed the gallery label and the feature pages.",
  "question": "What does the description spend most of its words on?",
  "options": [
   {
    "name": "maker and career",
    "definition": "Most words go to the artist or craftsperson, such as their training, life, habits, or career. Pick this when the person is the main subject, even if the object is also described."
   },
   {
    "name": "use and meaning",
    "definition": "Most words go to what the object was for or what it stood for, such as ritual, daily use, or belief. Pick this when the text explains its purpose or symbolism rather than its setting."
   },
   {
    "name": "origin and era",
    "definition": "Most words go to when and where the object was made and the events of that time. Pick this when the setting or past events lead, not the object's use or meaning."
   },
   {
    "name": "something else",
    "definition": "Pick this only when none of the four above takes the most words, such as a text mostly about a sale, a loan, or a restoration."
   },
   {
    "name": "looks and form",
    "definition": "Most words go to what can be seen, such as colour, pattern, shape, marks, or arrangement. Pick this when visible features take more words than anything else."
   }
  ]
 },
 {
  "qid": "q632e07f93b",
  "kind": "choice",
  "who_decides": "A visitor choosing a program needs to know where it takes place, such as inside a building or outside, so they can dress for it and plan the trip.",
  "question": "Where does this program take place?",
  "options": [
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
    "name": "something else",
    "definition": "Pick this only when the text does not say where the program is held, or names a place that none of the labels above fit, such as a zoo, a city street, or an online session; if the text names a building or outdoor area, pick that label instead."
   },
   {
    "name": "indoors in a building",
    "definition": "Pick this when the text names a building, room, hall, or centre as the place the program is held and does not say it goes outside; if the text says it is held on a porch, patio, or deck, pick outdoors on trails or grounds instead."
   }
  ]
 },
 {
  "qid": "q9ef3281db6",
  "kind": "choice",
  "who_decides": "A person who routes open-data requests to the right subject team decides this so the dataset reaches the team that knows its area.",
  "question": "Which part of public life is this dataset mainly about?",
  "options": [
   {
    "name": "courts and justice",
    "definition": "Pick this when the text mainly tracks cases through charges, hearings, prosecution, or sentences, not the original incident."
   },
   {
    "name": "crime and policing",
    "definition": "Pick this when the text mainly records reported incidents, calls, arrests, or police work as they happened, not cases moving through court."
   },
   {
    "name": "wildlife and plants",
    "definition": "Pick this when the text is mainly about living species, their listing, or their protection."
   },
   {
    "name": "money and grants",
    "definition": "Pick this when the text mainly lists amounts paid out, budgets, grants, or expenditure, rather than the places or things they pay for."
   },
   {
    "name": "land and buildings",
    "definition": "Pick this when the text is mainly about structures, property, zones, or boundaries, and not about money spent on them."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the main subject fits none of the five options above, such as a different area of public life."
   }
  ]
 },
 {
  "qid": "q478c1c0e05",
  "kind": "choice",
  "who_decides": "A data librarian who sorts newly published open-data datasets by the kind of records they hold, so people can find them.",
  "question": "What kind of records does the dataset hold?",
  "options": [
   {
    "name": "money amounts",
    "definition": "Pick when the rows mainly report dollar amounts, such as spending, income, grants, bonds or donations, rather than counts of people or items."
   },
   {
    "name": "counts of people or cases",
    "definition": "Pick when the rows report whole-number totals of people, households, cases or applications in a group, not a percentage and not one row per event."
   },
   {
    "name": "one row per event",
    "definition": "Pick when each row is one single happening, such as one filing, one permit or one parking session, rather than a total for a period."
   },
   {
    "name": "something else",
    "definition": "Pick when the rows are mainly free text such as notices or reports, or when none of the other kinds fits best."
   },
   {
    "name": "places and contact details",
    "definition": "Pick when the rows describe sites or organisations by name, address, location or contact details, with no money, counts or events."
   },
   {
    "name": "rates or percentages",
    "definition": "Pick when the rows report a share, rate or percent for a group, such as the percent with a condition, instead of a raw total."
   }
  ]
 },
 {
  "qid": "qd0f473ab45",
  "kind": "choice",
  "who_decides": "A city data team member who tags each new dataset with its most likely use, so that people searching for it get the right results.",
  "question": "What would a person most likely use this dataset for?",
  "options": [
   {
    "name": "look up one figure",
    "definition": "Pick when the description covers one place or one period, so the main use is to pull a single total or value."
   },
   {
    "name": "track trends over time",
    "definition": "Pick when the description says the data run across several years or periods, so the main use is to see how a figure moves over time."
   },
   {
    "name": "map or find places",
    "definition": "Pick when the description points to locations or addresses, so the main use is to plot or find where things are."
   },
   {
    "name": "compare areas now",
    "definition": "Pick when the description covers many places or groups for the same period, so the main use is to set them side by side."
   },
   {
    "name": "something else",
    "definition": "Pick when the description gives no clear use or fits none of the above best."
   },
   {
    "name": "check public money",
    "definition": "Pick when the description is about grants, bonds, funds, contributions or spending, so the main use is to trace who got public money."
   }
  ]
 },
 {
  "qid": "qefb9870fcd",
  "kind": "choice",
  "who_decides": "An editor decides whether a community paper should print a story, based on why readers would care about it.",
  "question": "Which news value makes this story worth printing?",
  "options": [
   {
    "name": "local interest",
    "definition": "Pick when the story matters mainly to one town, neighbourhood, school or small group, with effects limited to them; if many people across a region or country are affected, pick wide impact."
   },
   {
    "name": "rare first",
    "definition": "Pick when the story's main value is that it is a first, a record or an unusual event of its kind; if the main value is how big the effects are, pick wide impact."
   },
   {
    "name": "something else",
    "definition": "Pick when none of these values fits, such as a routine notice or a feature with no clear reason to print it now."
   },
   {
    "name": "public figure",
    "definition": "Pick when the main value is what a well-known public person or official says or does, rather than what the event changes; if the effects on people are the main point, pick wide impact."
   },
   {
    "name": "wide impact",
    "definition": "Pick when the event affects large numbers of people, a whole region, or the nation's money, safety or services right now; if the effects are limited to one town or group, pick local interest."
   },
   {
    "name": "contest outcome",
    "definition": "Pick when the main value is who won, lost or ranked first in a game, race, vote or competition; if the win is described as a first or a record, pick rare first."
   }
  ]
 }
]
