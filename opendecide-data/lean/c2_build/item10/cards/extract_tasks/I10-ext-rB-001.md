# Item 10 card G-LEX read I10-ext-rB-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/extract_answers/I10-ext-rB-001.json

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

Write ONE JSON object, and nothing else (no text before or after it), to the answer file named at the top. task_id must be "I10-ext-rB-001".
{"task_id": "I10-ext-rB-001",
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
  "qid": "qe7dacb471c",
  "kind": "choice",
  "who_decides": "A typical reader on the forum decides how they would feel after reading the post, which shows whether they are likely to step in and help.",
  "question": "How would a typical reader most likely feel after reading the post?",
  "options": [
   {
    "name": "wants to help",
    "definition": "Pick this when the problem is clear enough that a reader would feel drawn to answer it and could plausibly suggest a fix."
   },
   {
    "name": "nothing much",
    "definition": "Pick this when the post is a routine, clear, low-stakes note, such as a version or availability report, that a reader would skim with no strong feeling and no urge to answer."
   },
   {
    "name": "sorry for them",
    "definition": "Pick this when the post shows the writer in distress, stress, or long frustration, so a reader would feel sympathy for them."
   },
   {
    "name": "something else",
    "definition": "Pick this when a typical reader would have no clear feeling of the above kinds, or would have a mix that does not settle on one."
   },
   {
    "name": "amused",
    "definition": "Pick this when the wording itself is odd, playful, or funny enough that a reader would smile at it rather than feel anything about the problem."
   },
   {
    "name": "puzzled",
    "definition": "Pick this when the post is vague, tangled, or missing key details, so a reader would be unsure what the real problem or question is."
   }
  ]
 },
 {
  "qid": "q9bec9e90da",
  "kind": "choice",
  "who_decides": "A visitor choosing between programs decides what they are meant to gain from this one, using only the listing's stated purpose.",
  "question": "What is a visitor mainly meant to get out of this program?",
  "options": [
   {
    "name": "fun outing or party",
    "definition": "Pick this when the listing presents the program as an enjoyable event or night out, such as a party, tasting or social gathering, and does not name learning, making, display or fundraising as its main goal."
   },
   {
    "name": "learn a topic",
    "definition": "Pick this when the listing says visitors will be taught or told facts about a subject such as history, nature or science, with explanation as the main goal; a listing that only lets visitors look at objects is see a display instead."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the listing states a main purpose that is none of the five options above, such as a service or a sign-up for membership."
   },
   {
    "name": "make something",
    "definition": "Pick this when the main activity is the visitor creating an object to keep or take home, such as a craft, painting or card; a listing where the visitor only watches or hears is not this."
   },
   {
    "name": "see a display",
    "definition": "Pick this when the listing centres on looking at exhibits, vehicles, trains or other objects on show, without saying the visitor will be taught about them."
   },
   {
    "name": "support a cause",
    "definition": "Pick this when the listing says the main purpose is raising money for a named group, fund or museum; if the listing is mainly about a fun gathering, pick fun outing or party instead."
   }
  ]
 },
 {
  "qid": "q6502cc4498",
  "kind": "choice",
  "who_decides": "A course editor who sorts study material so that each reader gets the right kind of text for their needs.",
  "question": "What kind of study material is this text?",
  "options": [
   {
    "name": "community notice or manifesto",
    "definition": "Pick this when the text speaks for a group or cause, stating its rules, values or requests to readers in order to win agreement or action; if it describes a learning course, pick course overview instead."
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
    "name": "something else",
    "definition": "Pick this only when the text is a story, opinion piece, or other material that fits none of the five kinds above."
   },
   {
    "name": "course overview",
    "definition": "Pick this when the text says what a course, book or unit will cover, who it is for, or how it is set out, without teaching the content itself; if it teaches the content, pick textbook section instead."
   },
   {
    "name": "worked example",
    "definition": "Pick this when the main content is a sequence of steps for a calculation, proof, or formula, shown with symbols or numbers; if the steps are mostly explained in prose, pick textbook section instead."
   }
  ]
 },
 {
  "qid": "qa3b27dbf8c",
  "kind": "choice",
  "who_decides": "A museum cataloguing staff member who fills in the making-method field of an object record.",
  "question": "Which making method does the description name as the main way the object was made?",
  "options": [
   {
    "name": "cast in metal",
    "definition": "Pick this when the text says the object was made by melting metal and pouring it into a mould, so the shape comes from the mould."
   },
   {
    "name": "hand-painted or drawn",
    "definition": "Pick this when the text says the image was applied by hand with paint, ink or pencil directly onto the surface, one piece at a time."
   },
   {
    "name": "something else",
    "definition": "Pick this when the text names a method not listed here, such as photography or machine-making, or names no making method at all."
   },
   {
    "name": "carved or cut",
    "definition": "Pick this when the text says the shape was made by cutting, carving or chiselling material away from a solid piece, not by pouring or pressing."
   },
   {
    "name": "woven or stitched",
    "definition": "Pick this when the text says the object was made by interlacing or sewing threads, fibres or cloth."
   },
   {
    "name": "printed from a block",
    "definition": "Pick this when the text says the image was made by pressing ink from a prepared block, plate or screen onto paper or cloth, so copies can be made."
   }
  ]
 },
 {
  "qid": "qd42264fa94",
  "kind": "choice",
  "who_decides": "A press officer or news reader who files each release decides what kind of announcement it is so it goes to the right team and archive.",
  "question": "What kind of announcement is this, mainly?",
  "options": [
   {
    "name": "event or celebration",
    "definition": "A ceremony, awards, public gathering or observance day is the headline news; pick it when the news is about something that takes place on a particular day."
   },
   {
    "name": "physical project",
    "definition": "Work on a building, road, park, equipment or land is the headline news, even if money is also mentioned; pick it when the thing being built, bought, repaired or opened is the headline."
   },
   {
    "name": "new or changed program",
    "definition": "A service, scheme or initiative is set up or changed so that people can sign up for it or use it on an ongoing basis; pick it when people will take part in something that keeps running."
   },
   {
    "name": "something else",
    "definition": "Pick this only when no other option names the main kind of news, such as a plain statement of fact with no program, money, project, rule, warning or event."
   },
   {
    "name": "new rule or law",
    "definition": "A law, regulation or rule that people must follow, or a change to one, is the headline news; pick it when the text creates a duty backed by penalties or enforcement."
   },
   {
    "name": "warning or advice",
    "definition": "The text tells people how to stay safe or avoid a risk without creating any legal duty; pick it when the text says what people should do, not what they must do."
   },
   {
    "name": "money given or paid",
    "definition": "Money is granted, paid or handed to a named group or person as the headline news; pick it over the physical project when the payment is the headline and not the work it pays for."
   }
  ]
 },
 {
  "qid": "qf512c71935",
  "kind": "choice",
  "who_decides": "A museum writer or editor who decides which angle to build a new description around.",
  "question": "What do most of the description's words spend their time on?",
  "options": [
   {
    "name": "maker",
    "definition": "Pick this when most words describe who made the object, such as an artist, craftspeople or a workshop, and their training or career; the dividing line is that the text is about the maker, not about what happened to the object later."
   },
   {
    "name": "history",
    "definition": "Pick this when most words trace what happened to the object after it was made, such as where it went, who owned it or how it changed over the years."
   },
   {
    "name": "appearance",
    "definition": "Pick this when most words describe how the object looks, such as its shapes, colours, details or patterns, and what can be seen."
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
    "name": "symbolic meaning",
    "definition": "Pick this when most words explain what the image or object stands for, such as a belief, a proverb or a message, beyond what can be seen; the dividing line is that the text goes past looks to explain the message."
   }
  ]
 },
 {
  "qid": "qb4a6f48aab",
  "kind": "choice",
  "who_decides": "A help-desk volunteer who routes forum posts by the kind of reply they need, because a setting tip, a walkthrough and a bug report each go to different helpers.",
  "question": "What kind of answer would settle this post?",
  "options": [
   {
    "name": "workaround",
    "definition": "Pick this when the wanted result is not directly possible, so the answer would be a different route to a similar result that goes around the limit; if the answer is that nothing can be done, pick confirmed bug or limit instead."
   },
   {
    "name": "something else",
    "definition": "Pick this when the answer is only a thank-you, a question back to the poster, or a kind of answer not listed above."
   },
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
    "name": "confirmed bug or limit",
    "definition": "Pick this when the answer is that the behaviour is a real defect or a real limit of the software, with no fix or route the poster can take themselves."
   }
  ]
 },
 {
  "qid": "q5272e58a5d",
  "kind": "choice",
  "who_decides": "The forum helper decides the overall mood of the whole post, so the reply can match its tone, without judging any single sentence.",
  "question": "What mood does the whole post give off, apart from any one sentence?",
  "options": [
   {
    "name": "tense and stressed",
    "definition": "Pick this when worry or pressure runs through the whole post, with urgent or anxious wording repeated, not just in one sentence."
   },
   {
    "name": "something else",
    "definition": "Pick this when the post's overall mood does not fit any of the above, or is too mixed to name one mood."
   },
   {
    "name": "friendly and warm",
    "definition": "Pick this when the whole post carries kind words such as thanks, greetings, or good wishes that make the tone warm."
   },
   {
    "name": "playful and casual",
    "definition": "Pick this when the post is loose and joking in its tone, with slang, jokes, or light teasing running through it."
   },
   {
    "name": "blunt and curt",
    "definition": "Pick this when the post is short and impatient, with demands or sharp statements and no warmth, but without showing worry."
   },
   {
    "name": "calm and businesslike",
    "definition": "Pick this when the whole post reads steady and practical, with no pressure and no warm or sharp wording."
   }
  ]
 },
 {
  "qid": "q3d92b81796",
  "kind": "choice",
  "who_decides": "The volunteer centre's listing writer decides which skill the posting asks the volunteer to bring, so readers know whether they qualify before applying.",
  "question": "What must the volunteer already bring or be able to do before the first shift?",
  "options": [
   {
    "name": "specialist knowledge",
    "definition": "Pick when the text asks for a professional field skill such as finance, writing, design, or coaching without naming a specific program as the main need; dividing line: a field skill with no named program."
   },
   {
    "name": "paperwork and checks",
    "definition": "Pick when the text says the volunteer must pass a background check or finish required safety training before starting; dividing line: a mandatory check or course required before starting, unlike training given on the job."
   },
   {
    "name": "own transport",
    "definition": "Pick when the text says the volunteer must get to the site by their own means, such as their own car, and does not name a skill as the main need."
   },
   {
    "name": "hands and stamina",
    "definition": "Pick when the text says the work needs physical effort, such as standing for a set time, lifting, or moving items repeatedly."
   },
   {
    "name": "office software",
    "definition": "Pick when the text names a specific computer program or spreadsheet the volunteer must already know how to use; dividing line: a named program, not a general field skill, makes it office software."
   },
   {
    "name": "no skills needed",
    "definition": "Pick when the text asks for no prior skill or experience, says training or instruction will be given, and names no physical demand or required check."
   }
  ]
 },
 {
  "qid": "q49636db150",
  "kind": "choice",
  "who_decides": "A research reader who sorts new biology preprints by their main subject so that each one reaches the right specialist group.",
  "question": "What is the study mainly about?",
  "options": [
   {
    "name": "drugs and treatments",
    "definition": "Pick this when the main subject is finding, improving, or testing a compound meant to treat or block a disease; if the focus is how the disease-causing germ itself behaves, pick germs and their hosts instead."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the main subject is none of the above, such as populations in the wild, evolution over long periods, or a whole ecosystem."
   },
   {
    "name": "brain and behaviour",
    "definition": "Pick this when the main subject is how a linked group of nerve cells or brain areas drives what an animal senses, does, or feels; a single molecule's action is molecules inside cells instead."
   },
   {
    "name": "germs and their hosts",
    "definition": "Pick this when the main subject is a microbe, virus, or gut bacterium and what it does to or inside its host; if the focus is the compound that fights it, pick drugs and treatments instead."
   },
   {
    "name": "molecules inside cells",
    "definition": "Pick this when the main subject is how one named molecule, protein, or channel inside cells works or is switched on or off; a whole group of nerve cells or a whole organ is not this, so pick brain and behaviour or body tissue and its change instead."
   },
   {
    "name": "body tissue and its change",
    "definition": "Pick this when the main subject is how a tissue, organ, or cell layer changes in structure or condition, such as through damage, fatigue, or repair; if the text is about one molecule's action, pick molecules inside cells instead."
   },
   {
    "name": "new tools and methods",
    "definition": "Pick this when the main subject is a new measurement, scoring, or analysis method for biology data, and the biology itself is only the test case."
   }
  ]
 },
 {
  "qid": "q9183f0a9a2",
  "kind": "choice",
  "who_decides": "A museum education or digital team member who chooses which kind of text goes on a wall label, a web page or a record.",
  "question": "Which museum job would this description most suit as its main text?",
  "options": [
   {
    "name": "catalogue entry",
    "definition": "Pick this when the text is a plain list of facts for the records, such as maker, date, materials and size, with little or no story told."
   },
   {
    "name": "research essay",
    "definition": "Pick this when the text argues for a reading of what the object means and refers to other writing or sources to support it."
   },
   {
    "name": "online story",
    "definition": "Pick this when the text is a longer piece that follows a thread of people, events or background in order, for a reader at home, and does not direct the eye to the object."
   },
   {
    "name": "visitor label",
    "definition": "Pick this when the text is a few short sentences meant to be read standing in front of the object, pointing out what to look for or know right there."
   },
   {
    "name": "something else",
    "definition": "Pick this when the text was written for a different job, such as a children's activity or an advert, or fits none of the four above better than the others."
   }
  ]
 },
 {
  "qid": "q3ed0961975",
  "kind": "choice",
  "who_decides": "A help-desk volunteer who routes forum posts to the helper who knows that part of the office suite, because each area has its own experts.",
  "question": "Which part of the office software is the post mainly about?",
  "options": [
   {
    "name": "something else",
    "definition": "Pick this when the post is about presentation slides, drawings or another part of the suite not listed above."
   },
   {
    "name": "export, convert or print",
    "definition": "Pick this when the poster wants a file saved in another format, converted by a command, or printed, and the output file or printout is the problem, even if the source is a text or spreadsheet file."
   },
   {
    "name": "spreadsheet cells",
    "definition": "Pick this when the trouble is with cells, rows, columns, formulas or the data typed into a sheet; if the poster mainly wants a chart changed, pick charts and graphs instead."
   },
   {
    "name": "install or update",
    "definition": "Pick this when the trouble is getting the software installed, started or updated, and it happens before or outside working on any document."
   },
   {
    "name": "charts and graphs",
    "definition": "Pick this when the poster wants a chart itself changed, such as its labels, data series, axes or look; if the trouble is in the cell data the chart reads from, pick spreadsheet cells instead."
   },
   {
    "name": "text documents",
    "definition": "Pick this when the trouble is with words, paragraphs, page layout, styles or searching inside a word-processing document, and the poster is trying to edit that text itself rather than output a file."
   },
   {
    "name": "database records",
    "definition": "Pick this when the trouble is with database tables, forms, queries or saved records inside a database file."
   }
  ]
 },
 {
  "qid": "qbd4f825cd3",
  "kind": "choice",
  "who_decides": "A city data team member who tags each new dataset with its most likely use, so that people searching for it get the right results.",
  "question": "What would a person most likely use this dataset for?",
  "options": [
   {
    "name": "check public money",
    "definition": "Pick when the description is about grants, bonds, funds, contributions or spending, so the main use is to trace who got public money."
   },
   {
    "name": "track trends over time",
    "definition": "Pick when the description says the data run across several years or periods, so the main use is to see how a figure moves over time."
   },
   {
    "name": "compare areas now",
    "definition": "Pick when the description covers many places or groups for the same period, so the main use is to set them side by side."
   },
   {
    "name": "look up one figure",
    "definition": "Pick when the description covers one place or one period, so the main use is to pull a single total or value."
   },
   {
    "name": "something else",
    "definition": "Pick when the description gives no clear use or fits none of the above best."
   },
   {
    "name": "map or find places",
    "definition": "Pick when the description points to locations or addresses, so the main use is to plot or find where things are."
   }
  ]
 },
 {
  "qid": "q118c3e4c2c",
  "kind": "choice",
  "who_decides": "A museum visitor or guide writer decides what a visitor would mainly use the description for, so the right text is shown at the right point of the visit.",
  "question": "What would a visitor mainly use this description for?",
  "options": [
   {
    "name": "how it was made",
    "definition": "Pick this when the text mainly explains the materials, techniques or process used to make the work, such as printing from stone or cutting paper."
   },
   {
    "name": "its importance at the time",
    "definition": "Pick this when the text mainly explains why the work mattered in its own era, such as its political or social role or how the public reacted; pick this work's own history instead if the text is about the object's dates, owners and places."
   },
   {
    "name": "this work's own history",
    "definition": "Pick this when the text mainly tells who commissioned or owned this one object, when, where it was shown or moved, and its story as a single piece."
   },
   {
    "name": "the artist's life and career",
    "definition": "Pick this when the text is mainly about the maker's training, life or style across many works; pick this work's own history instead if the text is about this one object."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the text is mainly used for another purpose that none of the other options covers, such as a shop listing or a booking note."
   },
   {
    "name": "what to notice up close",
    "definition": "Pick this when the text points out visible details to look for while standing in front of the work, such as texture, gaze, colour patterns or cut edges."
   }
  ]
 },
 {
  "qid": "q3a05edac1b",
  "kind": "choice",
  "who_decides": "A visitor reading a museum description decides which part of the story the text mainly gives them, so they know whether it answers their question.",
  "question": "What does this description mainly tell a visitor about?",
  "options": [
   {
    "name": "historical setting",
    "definition": "The text is mainly about the time, place, or social or political situation the work came from; pick this over artist background when most of the detail is about that wider world rather than the person."
   },
   {
    "name": "artist background",
    "definition": "The text is mainly about the maker's life, training, travels or career; pick this over historical setting when most of the detail is about the person rather than the world around the work."
   },
   {
    "name": "meaning and message",
    "definition": "The text is mainly about what the work expresses, shows or suggests to a viewer; pick this over historical setting when the point is the work's own message rather than the outside context."
   },
   {
    "name": "something else",
    "definition": "Pick only when the text is mainly about something none of the four above covers, such as a visit tip, a price or a loan, or when the text is too short to say."
   },
   {
    "name": "making process",
    "definition": "The text is mainly about how the work was made, such as its materials, tools, technique or steps, and not about the maker's life or the work's message."
   }
  ]
 },
 {
  "qid": "q9a1bc19d2e",
  "kind": "choice",
  "who_decides": "An editor decides whether a community paper should print a story, based on why readers would care about it.",
  "question": "Which news value makes this story worth printing?",
  "options": [
   {
    "name": "rare first",
    "definition": "Pick when the story's main value is that it is a first, a record or an unusual event of its kind; if the main value is how big the effects are, pick wide impact."
   },
   {
    "name": "local interest",
    "definition": "Pick when the story matters mainly to one town, neighbourhood, school or small group, with effects limited to them; if many people across a region or country are affected, pick wide impact."
   },
   {
    "name": "wide impact",
    "definition": "Pick when the event affects large numbers of people, a whole region, or the nation's money, safety or services right now; if the effects are limited to one town or group, pick local interest."
   },
   {
    "name": "contest outcome",
    "definition": "Pick when the main value is who won, lost or ranked first in a game, race, vote or competition; if the win is described as a first or a record, pick rare first."
   },
   {
    "name": "something else",
    "definition": "Pick when none of these values fits, such as a routine notice or a feature with no clear reason to print it now."
   },
   {
    "name": "public figure",
    "definition": "Pick when the main value is what a well-known public person or official says or does, rather than what the event changes; if the effects on people are the main point, pick wide impact."
   }
  ]
 },
 {
  "qid": "qbad3c1ca14",
  "kind": "choice",
  "who_decides": "A teacher choosing which kind of study material to hand a class for a lesson, so each item fits the job it is meant to do.",
  "question": "What kind of study material is this passage?",
  "options": [
   {
    "name": "research report",
    "definition": "Pick when the text describes a study's question, methods, data or findings; pick reference article when it explains a concept without reporting any study or test."
   },
   {
    "name": "glossary",
    "definition": "Pick when the text is a list of terms, each with a short meaning and no connected story; pick reference article when the meanings sit inside a longer explanation."
   },
   {
    "name": "course or program page",
    "definition": "Pick when the text describes a lesson, course or coaching program and invites the reader to take part or sign up; pick outline when it only lists the parts of a book or course without inviting anyone in."
   },
   {
    "name": "practice questions",
    "definition": "Pick when the text is mainly a set of questions for the learner to answer; pick outline when it lists sections or headings rather than asking questions."
   },
   {
    "name": "reference article",
    "definition": "Pick when the text explains one topic in connected prose so it can be looked up, with background and detail; pick glossary instead when it lists many separate terms, each with a short meaning."
   },
   {
    "name": "outline",
    "definition": "Pick when the text is a skeleton of headings, sections or chapter parts with little explanation of each; pick course or program page when it describes a course and invites the reader to join."
   }
  ]
 },
 {
  "qid": "q94714c1789",
  "kind": "choice",
  "who_decides": "A museum writer who decides which kind of text an existing description can be reused for, since each job needs a different length and tone.",
  "question": "What job is this description mainly written to do?",
  "options": [
   {
    "name": "teach an idea",
    "definition": "Explains a general custom, term, or belief that reaches beyond this one object. Pick this when the main content would still make sense if the object were removed from the text."
   },
   {
    "name": "tell a story",
    "definition": "Follows events in order, or a person's experience or own words, to carry the reader through an account. Pick this when the text is mostly a sequence of events or an anecdote."
   },
   {
    "name": "explain to visitors",
    "definition": "Tells a viewer what to notice in this object and why it matters here. Pick this when the text points at this object's features while guiding looking, and does not mainly teach a wider idea."
   },
   {
    "name": "record the facts",
    "definition": "Sets out plain facts about the object, such as what it is, who made it, and when, in neutral reference language. Pick this when the text gives no guidance on how to look at the object."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the main job is none of the four above, such as a notice about visiting hours or a call for donations."
   }
  ]
 },
 {
  "qid": "q52b6abb59b",
  "kind": "choice",
  "who_decides": "The forum helper, or the writer themself, decides how the poster feels so they can reply in a suitable tone and urgency.",
  "question": "What feeling does the writer show or describe in the post?",
  "options": [
   {
    "name": "curious",
    "definition": "Pick this when the writer mainly asks why something happens or whether it is intended or a bug, without complaining about it."
   },
   {
    "name": "matter-of-fact",
    "definition": "Pick this when the writer only lists facts, steps, or settings in plain words and shows no feeling about them and asks no why question."
   },
   {
    "name": "urgent worry",
    "definition": "Pick this when the writer says they need the fix now, mentions a deadline, a document about to be sent, or a risk to their work, or says they are desperate."
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
    "name": "stuck and fed up",
    "definition": "Pick this when the writer says a fix has failed again and again or they have been stuck for a long time, and sounds exasperated, but gives no deadline or fear of consequences."
   }
  ]
 },
 {
  "qid": "q1267abbe4d",
  "kind": "choice",
  "who_decides": "A reader who sorts government news decides the main purpose of each release so it goes to the right team and is passed on correctly.",
  "question": "What is the main job this release is trying to get done?",
  "options": [
   {
    "name": "ask readers to act",
    "definition": "The text gives readers a specific thing to do now, such as check something, register, take a safety step or follow a rule; pick it only when there is a direct request to the reader."
   },
   {
    "name": "report what happened",
    "definition": "The text states a result, a number, a finished step or a decision already made, with no request to readers; pick it when the news is about the past or present."
   },
   {
    "name": "something else",
    "definition": "Pick this only when none of the five options above fits the main purpose, for example when the text has no clear aim."
   },
   {
    "name": "argue a view",
    "definition": "The author makes a case for a position or defends a policy in order to change readers' minds; pick it when persuasion is the main purpose, not a plain request."
   },
   {
    "name": "praise people or work",
    "definition": "The text thanks, honours or celebrates people or a group for their work; pick it when recognition is the main purpose, not a result to report."
   },
   {
    "name": "plan what comes next",
    "definition": "The text sets out a future step, start date or plan that is not yet done; pick it when the main news is what will happen, not what has already happened."
   }
  ]
 },
 {
  "qid": "q5c2cbcc23b",
  "kind": "choice",
  "who_decides": "Government and public bodies decide how far a matter reaches, from one place, to the whole province, to a national level, or to one named group.",
  "question": "How far does the decision or matter reach?",
  "options": [
   {
    "name": "something else",
    "definition": "Pick this only when the text states no reach that fits the labels above."
   },
   {
    "name": "whole province",
    "definition": "Pick this when the text says the matter applies across the province or to all regions or residents, even if one place is given as an example."
   },
   {
    "name": "federal or national",
    "definition": "Pick this when the decision is made by, or shared with, the federal government, a national body or another country, not just the province."
   },
   {
    "name": "one local area",
    "definition": "Pick this when the text says the matter applies to one town, county, regional municipality, road or site in one place; pick one named organisation when the reach is a single named group rather than a place."
   },
   {
    "name": "one named organisation",
    "definition": "Pick this when the text's decision targets one named school board, company or group, and does not claim reach over a whole place; pick one local area when the text is about a place."
   }
  ]
 },
 {
  "qid": "qac083e33cc",
  "kind": "choice",
  "who_decides": "The news editor deciding which story to print first and how to frame it for readers.",
  "question": "What is the strongest reason this story is worth printing?",
  "options": [
   {
    "name": "leader action",
    "definition": "The story's main reason is a decision, move or statement by a top government, business or public leader in their official role, and it is picked over large scale impact when the reason is who acted rather than how many are affected."
   },
   {
    "name": "first or record",
    "definition": "The story's main reason is that something happened for the first time, or set a new best, worst or biggest mark compared with the past."
   },
   {
    "name": "something else",
    "definition": "Pick this only when none of the other five reasons is the main one, for example when the story is worth printing for a human-interest detail with no size, first, surprise or leader involved."
   },
   {
    "name": "unexpected turn",
    "definition": "The story's main reason is a result or change that goes against what most people expected, such as an underdog win or a sudden reversal of a plan, and it is picked over first or record when the surprise is a result against expectation rather than a milestone."
   },
   {
    "name": "local angle",
    "definition": "The story's main reason is that it touches one town, region or community that its readers know, and the size of the matter is small."
   },
   {
    "name": "large scale impact",
    "definition": "The story's main reason is how many people, how much money or how many places are affected, where the size of the matter is the key point."
   }
  ]
 },
 {
  "qid": "q2919edfec2",
  "kind": "choice",
  "who_decides": "An editor sorting incoming stories into subject queues, because each queue has a different reviewer.",
  "question": "Which area of public life is this story mainly about?",
  "options": [
   {
    "name": "vote and leadership",
    "definition": "The main point is who wins, loses, stands for, or quits a vote for public office or party leadership, or a boycott of one; pick \"government decisions\" instead when the story is about a law, budget, or official order with no vote or candidate in focus."
   },
   {
    "name": "emergencies and accidents",
    "definition": "The main point is an event that puts people or buildings at risk and calls in fire, police, or rescue crews, such as a fire, crash, or scare; if the main point is treating an illness or a birth, pick \"patient care\" instead."
   },
   {
    "name": "other subject",
    "definition": "Pick this only when the main subject is none of the above, such as science, computers, weather, pollution, or everyday life."
   },
   {
    "name": "government decisions",
    "definition": "The main point is an official act such as a law, budget, ruling, or ministerial order; if the story is about who holds or seeks office, pick \"vote and leadership\" instead."
   },
   {
    "name": "patient care",
    "definition": "The main point is illness, a birth, treatment, hospital work, or a medicine supply for people who need medical help; if the main point is hunger or the supply of food or aid, pick \"food and relief\" instead."
   },
   {
    "name": "food and relief",
    "definition": "The main point is hunger, a food shortage, or aid sent to people in need; pick this over \"patient care\" even when sickness is mentioned, because the supply of food or aid is the main point."
   },
   {
    "name": "match and team news",
    "definition": "The main point is a game, a team, a player, or a coach, such as a result, a transfer, or a sacking."
   }
  ]
 },
 {
  "qid": "q436f10969a",
  "kind": "choice",
  "who_decides": "A travel guide editor decides which section a passage belongs in, because readers look for each kind of information under its own heading.",
  "question": "Which section of a travel guide does this passage belong in?",
  "options": [
   {
    "name": "getting around",
    "definition": "Pick this when the text explains how to move between spots inside the place, by local bus, taxi, rental or walking route, and the main point is how to move, not a warning about danger."
   },
   {
    "name": "what to see and do",
    "definition": "Pick this when the text names specific sights, activities or tours and tells the visitor to go to them or take part."
   },
   {
    "name": "getting there",
    "definition": "Pick this when the text explains how to reach the place from outside it, by road, rail, boat or flight from another town or country; if the trip starts inside the place, pick getting around."
   },
   {
    "name": "where to stay",
    "definition": "Pick this when the text covers places to sleep, such as hotels, huts or camping, or how to book them."
   },
   {
    "name": "what it is like",
    "definition": "Pick this when the text describes the character, scenery, history or size of the place without naming a sight or activity to go to; if it names one, pick what to see and do."
   },
   {
    "name": "staying safe",
    "definition": "Pick this when the main point of the text is a warning about danger or a safety rule for the visitor, even if travel is mentioned."
   }
  ]
 },
 {
  "qid": "qa34d2df7f1",
  "kind": "choice",
  "who_decides": "A labeller reading a travel guide entry decides which feeling a typical reader is most likely to have about making the trip, so that guide texts can be grouped by how they leave the reader.",
  "question": "After reading, what is the reader most likely to feel about making the trip?",
  "options": [
   {
    "name": "at ease",
    "definition": "Pick this when the text stresses simple conditions such as easy transport, cheap or nearby options, plenty of places to stay or a well set up route, so a reader would think the trip will be simple; the stress on ease is the dividing line from daunted."
   },
   {
    "name": "daunted",
    "definition": "Pick this when the text stresses hard conditions such as remote roads, cold, long distances, danger or high cost, so a reader would think the trip will be difficult; the stress on difficulty is the dividing line from at ease."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the text gives a reader no clear reason to feel any of the options above, for example when it is only a short list of names, dates or unrelated details."
   },
   {
    "name": "keen to visit",
    "definition": "Pick this when the text makes the place sound appealing and names what to see or do, so a reader would want to go there; a pull toward travelling, not just knowing, is the dividing line from curious."
   },
   {
    "name": "curious",
    "definition": "Pick this when the text leaves a reader wanting to learn more about the history, nature or people of the place, but gives no pull toward actually going there; wanting to know without wanting to travel is the dividing line from keen to visit."
   }
  ]
 }
]
