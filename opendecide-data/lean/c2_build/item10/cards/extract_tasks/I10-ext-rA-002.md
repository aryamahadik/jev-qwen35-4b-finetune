# Item 10 card G-LEX read I10-ext-rA-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/extract_answers/I10-ext-rA-002.json

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

Write ONE JSON object, and nothing else (no text before or after it), to the answer file named at the top. task_id must be "I10-ext-rA-002".
{"task_id": "I10-ext-rA-002",
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
  "qid": "q7a61570a39",
  "kind": "choice",
  "who_decides": "The volunteer centre's listing writer decides which skill the posting asks the volunteer to bring, so readers know whether they qualify before applying.",
  "question": "What must the volunteer already bring or be able to do before the first shift?",
  "options": [
   {
    "name": "specialist knowledge",
    "definition": "Pick when the text asks for a professional field skill such as finance, writing, design, or coaching without naming a specific program as the main need; dividing line: a field skill with no named program."
   },
   {
    "name": "no skills needed",
    "definition": "Pick when the text asks for no prior skill or experience, says training or instruction will be given, and names no physical demand or required check."
   },
   {
    "name": "office software",
    "definition": "Pick when the text names a specific computer program or spreadsheet the volunteer must already know how to use; dividing line: a named program, not a general field skill, makes it office software."
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
   }
  ]
 },
 {
  "qid": "q07f231441e",
  "kind": "choice",
  "who_decides": "The news desk editor who sorts each incoming story by the kind of event it reports before filing it.",
  "question": "What kind of event or development does the story mainly report?",
  "options": [
   {
    "name": "incident or violence",
    "definition": "The story reports a harmful event that has already happened, such as an attack, a riot or an accident, rather than a rule or a set of talks."
   },
   {
    "name": "game result",
    "definition": "The story reports the final score or outcome of a finished game or match."
   },
   {
    "name": "research finding",
    "definition": "The story reports the results of a study, test or experiment."
   },
   {
    "name": "talks or deal",
    "definition": "The story reports negotiations between parties that resume, stall or end in an agreement, but does not say that a rule has taken effect."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the story's main event fits none of the other six, such as a product launch, a weather event or a business announcement."
   },
   {
    "name": "endorsement or backing",
    "definition": "The story reports one person or group publicly declaring support for a candidate or cause, where the declaration itself is the main point rather than a deal between two sides."
   },
   {
    "name": "new rule or ban",
    "definition": "The story reports a government, court or group putting a new rule, law or ban into force, so that it now applies to people."
   }
  ]
 },
 {
  "qid": "qaf4bc3c63d",
  "kind": "choice",
  "who_decides": "A data librarian decides how far a researcher can trust the timing and completeness of an open dataset, because a wrong guess about its freshness can change the findings.",
  "question": "How current, complete or final is the data said to be?",
  "options": [
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
    "name": "something else",
    "definition": "Pick when the text makes no main point about timing or completeness, or its main note is a change in how things are counted or defined."
   },
   {
    "name": "may still change",
    "definition": "Pick when the text says the figures are early, subject to audit, or open to revision; pick this over the other options whenever a warning about revision is given."
   }
  ]
 },
 {
  "qid": "q639ecefbc1",
  "kind": "choice",
  "who_decides": "The news editor deciding which story to print first and how to frame it for readers.",
  "question": "What is the strongest reason this story is worth printing?",
  "options": [
   {
    "name": "first or record",
    "definition": "The story's main reason is that something happened for the first time, or set a new best, worst or biggest mark compared with the past."
   },
   {
    "name": "large scale impact",
    "definition": "The story's main reason is how many people, how much money or how many places are affected, where the size of the matter is the key point."
   },
   {
    "name": "local angle",
    "definition": "The story's main reason is that it touches one town, region or community that its readers know, and the size of the matter is small."
   },
   {
    "name": "leader action",
    "definition": "The story's main reason is a decision, move or statement by a top government, business or public leader in their official role, and it is picked over large scale impact when the reason is who acted rather than how many are affected."
   },
   {
    "name": "something else",
    "definition": "Pick this only when none of the other five reasons is the main one, for example when the story is worth printing for a human-interest detail with no size, first, surprise or leader involved."
   },
   {
    "name": "unexpected turn",
    "definition": "The story's main reason is a result or change that goes against what most people expected, such as an underdog win or a sudden reversal of a plan, and it is picked over first or record when the surprise is a result against expectation rather than a milestone."
   }
  ]
 },
 {
  "qid": "qdd3082b6ac",
  "kind": "choice",
  "who_decides": "A museum labeller or routing clerk decides which kind of object a description is about, so the right page or filter is shown to the visitor.",
  "question": "What kind of object does this description mainly describe?",
  "options": [
   {
    "name": "print",
    "definition": "Pick this when the work was made by pressing ink from a stone, plate or block, in editions, and was made to be collected as an art work; pick poster instead if the sheet was made to advertise or announce something."
   },
   {
    "name": "poster",
    "definition": "Pick this when the printed sheet was made to advertise or publicly announce an event, show, product or message, even if the artist is famous."
   },
   {
    "name": "box or assemblage",
    "definition": "Pick this when the work is a three-dimensional piece built inside a box or frame from paper cut-outs, small objects or printed scraps, and not one carved or modelled form."
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
    "name": "sculpture or bust",
    "definition": "Pick this when the work is a solid three-dimensional figure, carved, cast or modelled, such as a bust or statue; pick box or assemblage instead if objects are arranged inside a box or frame."
   },
   {
    "name": "stained glass window",
    "definition": "Pick this when the text says the work is coloured glass set into a window, including a memorial window."
   }
  ]
 },
 {
  "qid": "q07722f5279",
  "kind": "choice",
  "who_decides": "The reader deciding, after the headline and first lines, whether to act on the story, keep it in mind or skip it.",
  "question": "What does the story most ask or mean for the reader to do or expect?",
  "options": [
   {
    "name": "something else",
    "definition": "Pick this only when none of the other five fits the reader's stake best, for example when the story is an opinion piece that only asks the reader to consider a view."
   },
   {
    "name": "no direct effect",
    "definition": "The story is for information only and gives the reader no practical change, benefit, risk or step, so it touches them only in a general way."
   },
   {
    "name": "must act now",
    "definition": "The story names a step the reader has to take soon, such as signing up, paying, registering or voting, to keep a right or benefit."
   },
   {
    "name": "could benefit",
    "definition": "The story says the reader may gain something good now, such as a discount, a free event or a new service, and no step is required."
   },
   {
    "name": "safety warning",
    "definition": "The story's main point is a danger to the reader's health, safety or property that they should avoid, rather than a step they must take to keep a right or benefit."
   },
   {
    "name": "affected later",
    "definition": "The story says a change will reach the reader's life later and names no step the reader must take now, unlike no direct effect, which says nothing practical changes for them."
   }
  ]
 },
 {
  "qid": "q876fbca9e2",
  "kind": "choice",
  "who_decides": "A news site editor who labels the overall mood of each story for a mood-based story feed.",
  "question": "Apart from any single sentence, what mood does the whole text give off?",
  "options": [
   {
    "name": "tense",
    "definition": "Pick this when the whole text is built around an open contest, dispute or pending event whose outcome is still unknown; pick grim instead when the bad news is already settled."
   },
   {
    "name": "grim",
    "definition": "Pick this when the whole text dwells on loss, suffering or failure, and the bad outcome is already settled; pick tense instead when the outcome is still open."
   },
   {
    "name": "even-toned",
    "definition": "Pick this only when no overall mood stands out and the text reads as a plain account pulling neither way; if one mood clearly dominates the whole text, pick that mood instead."
   },
   {
    "name": "playful",
    "definition": "Pick this when the whole text is light and teasing, using wit or humour as its overall style rather than good news."
   },
   {
    "name": "upbeat",
    "definition": "Pick this when the whole text is bright and celebrates good outcomes or progress; pick playful instead when the lightness comes from humour rather than good news."
   }
  ]
 },
 {
  "qid": "q7f94f05b8b",
  "kind": "choice",
  "who_decides": "A typical reader on the forum decides how they would feel after reading the post, which shows whether they are likely to step in and help.",
  "question": "How would a typical reader most likely feel after reading the post?",
  "options": [
   {
    "name": "something else",
    "definition": "Pick this when a typical reader would have no clear feeling of the above kinds, or would have a mix that does not settle on one."
   },
   {
    "name": "sorry for them",
    "definition": "Pick this when the post shows the writer in distress, stress, or long frustration, so a reader would feel sympathy for them."
   },
   {
    "name": "nothing much",
    "definition": "Pick this when the post is a routine, clear, low-stakes note, such as a version or availability report, that a reader would skim with no strong feeling and no urge to answer."
   },
   {
    "name": "amused",
    "definition": "Pick this when the wording itself is odd, playful, or funny enough that a reader would smile at it rather than feel anything about the problem."
   },
   {
    "name": "puzzled",
    "definition": "Pick this when the post is vague, tangled, or missing key details, so a reader would be unsure what the real problem or question is."
   },
   {
    "name": "wants to help",
    "definition": "Pick this when the problem is clear enough that a reader would feel drawn to answer it and could plausibly suggest a fix."
   }
  ]
 },
 {
  "qid": "q7746ff7abc",
  "kind": "choice",
  "who_decides": "A museum visitor or guide writer decides what a visitor would mainly use the description for, so the right text is shown at the right point of the visit.",
  "question": "What would a visitor mainly use this description for?",
  "options": [
   {
    "name": "something else",
    "definition": "Pick this only when the text is mainly used for another purpose that none of the other options covers, such as a shop listing or a booking note."
   },
   {
    "name": "what to notice up close",
    "definition": "Pick this when the text points out visible details to look for while standing in front of the work, such as texture, gaze, colour patterns or cut edges."
   },
   {
    "name": "how it was made",
    "definition": "Pick this when the text mainly explains the materials, techniques or process used to make the work, such as printing from stone or cutting paper."
   },
   {
    "name": "this work's own history",
    "definition": "Pick this when the text mainly tells who commissioned or owned this one object, when, where it was shown or moved, and its story as a single piece."
   },
   {
    "name": "its importance at the time",
    "definition": "Pick this when the text mainly explains why the work mattered in its own era, such as its political or social role or how the public reacted; pick this work's own history instead if the text is about the object's dates, owners and places."
   },
   {
    "name": "the artist's life and career",
    "definition": "Pick this when the text is mainly about the maker's training, life or style across many works; pick this work's own history instead if the text is about this one object."
   }
  ]
 },
 {
  "qid": "q29e92dad58",
  "kind": "choice",
  "who_decides": "The writer of the release chooses how to present the decision, so the reader sees the measure as a routine step, a gain, a cost, a warning or a conflict.",
  "question": "How does the text mainly present the decision, measure or event?",
  "options": [
   {
    "name": "warning of risk",
    "definition": "Pick this when the text's main point is a danger, with advice to take action now; pick routine notice when the text only gives dates and steps without any danger."
   },
   {
    "name": "dispute or conflict",
    "definition": "Pick this when the text reports people or groups disagreeing with, or fighting over, a decision or event."
   },
   {
    "name": "something else",
    "definition": "Pick this only when none of the labels above fits as the text's main way of presenting the matter."
   },
   {
    "name": "routine notice",
    "definition": "Pick this when the text only says what will happen, when and how, with no claimed gain, no stressed cost, no danger and no dispute; pick warning of risk when the text tells people to act to avoid danger."
   },
   {
    "name": "stated benefit",
    "definition": "Pick this when the text's main point is a good result, such as jobs, savings, better service or growth, even if a cost is also mentioned; pick stated cost when the money itself is the main point."
   },
   {
    "name": "stated cost",
    "definition": "Pick this when the text's main point is how much money is spent, owed or needed, and no good result is the headline; pick stated benefit when the good result the money buys is the main point."
   }
  ]
 },
 {
  "qid": "q620d9117f0",
  "kind": "choice",
  "who_decides": "A help-desk volunteer who routes forum posts to the helper who knows that part of the office suite, because each area has its own experts.",
  "question": "Which part of the office software is the post mainly about?",
  "options": [
   {
    "name": "export, convert or print",
    "definition": "Pick this when the poster wants a file saved in another format, converted by a command, or printed, and the output file or printout is the problem, even if the source is a text or spreadsheet file."
   },
   {
    "name": "text documents",
    "definition": "Pick this when the trouble is with words, paragraphs, page layout, styles or searching inside a word-processing document, and the poster is trying to edit that text itself rather than output a file."
   },
   {
    "name": "charts and graphs",
    "definition": "Pick this when the poster wants a chart itself changed, such as its labels, data series, axes or look; if the trouble is in the cell data the chart reads from, pick spreadsheet cells instead."
   },
   {
    "name": "database records",
    "definition": "Pick this when the trouble is with database tables, forms, queries or saved records inside a database file."
   },
   {
    "name": "something else",
    "definition": "Pick this when the post is about presentation slides, drawings or another part of the suite not listed above."
   },
   {
    "name": "spreadsheet cells",
    "definition": "Pick this when the trouble is with cells, rows, columns, formulas or the data typed into a sheet; if the poster mainly wants a chart changed, pick charts and graphs instead."
   },
   {
    "name": "install or update",
    "definition": "Pick this when the trouble is getting the software installed, started or updated, and it happens before or outside working on any document."
   }
  ]
 },
 {
  "qid": "q42b2625ffc",
  "kind": "choice",
  "who_decides": "The forum helper decides the overall mood of the whole post, so the reply can match its tone, without judging any single sentence.",
  "question": "What mood does the whole post give off, apart from any one sentence?",
  "options": [
   {
    "name": "tense and stressed",
    "definition": "Pick this when worry or pressure runs through the whole post, with urgent or anxious wording repeated, not just in one sentence."
   },
   {
    "name": "blunt and curt",
    "definition": "Pick this when the post is short and impatient, with demands or sharp statements and no warmth, but without showing worry."
   },
   {
    "name": "calm and businesslike",
    "definition": "Pick this when the whole post reads steady and practical, with no pressure and no warm or sharp wording."
   },
   {
    "name": "friendly and warm",
    "definition": "Pick this when the whole post carries kind words such as thanks, greetings, or good wishes that make the tone warm."
   },
   {
    "name": "something else",
    "definition": "Pick this when the post's overall mood does not fit any of the above, or is too mixed to name one mood."
   },
   {
    "name": "playful and casual",
    "definition": "Pick this when the post is loose and joking in its tone, with slang, jokes, or light teasing running through it."
   }
  ]
 },
 {
  "qid": "q0dd5bebaac",
  "kind": "choice",
  "who_decides": "A visitor reading a park listing decides whether the program suits them and their group, using only what the listing says about who it is for.",
  "question": "Which kind of visitor is this program mainly aimed at?",
  "options": [
   {
    "name": "anyone, all levels",
    "definition": "Pick this when the listing invites any visitor with no age limit or experience needed, or says all skill levels are encouraged, and does not frame the program as only for newcomers."
   },
   {
    "name": "beginners only",
    "definition": "Pick this when the listing frames the program as for people new to the activity, using words like beginners or introductory, even if it does not forbid others; if it says all levels are welcome, pick anyone, all levels instead."
   },
   {
    "name": "people who hike",
    "definition": "Pick this when the listing describes a walk, trail, loop or rough terrain as the main activity, so the visitor must be willing to walk; a talk or hands-on activity at one spot is not this."
   },
   {
    "name": "families with children",
    "definition": "Pick this when the listing names children or kids as the audience or says a child must come with an adult; a program that only says it is free for all ages without naming children is not this."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the listing names no audience, no children and no walking activity that fits the four options above."
   }
  ]
 },
 {
  "qid": "q6bb421db95",
  "kind": "choice",
  "who_decides": "A learner or course editor deciding what a passage is for, so it is used in the right way.",
  "question": "What is this passage mainly meant to help a learner do?",
  "options": [
   {
    "name": "something else",
    "definition": "Pick this only when the main aim is none of these, for example the text describes a business or reports a finished result without teaching the reader or asking them to act."
   },
   {
    "name": "understand an idea",
    "definition": "Pick this when the text explains how something works, what happened, or why, and does not ask the reader to do any task."
   },
   {
    "name": "carry out a real job",
    "definition": "Pick this when the text gives steps, checks or settings for a real-world job such as inspecting equipment, setting something up or building something; unlike the practise option, the goal is the finished real job, not a learning answer."
   },
   {
    "name": "practise a skill",
    "definition": "Pick this when the text sets questions, prompts or exercises that the reader must work through to build a skill; unlike the understand option, the reader is asked to produce something."
   }
  ]
 },
 {
  "qid": "q868ec49ae5",
  "kind": "choice",
  "who_decides": "Government and public bodies decide how far a matter reaches, from one place, to the whole province, to a national level, or to one named group.",
  "question": "How far does the decision or matter reach?",
  "options": [
   {
    "name": "federal or national",
    "definition": "Pick this when the decision is made by, or shared with, the federal government, a national body or another country, not just the province."
   },
   {
    "name": "one local area",
    "definition": "Pick this when the text says the matter applies to one town, county, regional municipality, road or site in one place; pick one named organisation when the reach is a single named group rather than a place."
   },
   {
    "name": "whole province",
    "definition": "Pick this when the text says the matter applies across the province or to all regions or residents, even if one place is given as an example."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the text states no reach that fits the labels above."
   },
   {
    "name": "one named organisation",
    "definition": "Pick this when the text's decision targets one named school board, company or group, and does not claim reach over a whole place; pick one local area when the text is about a place."
   }
  ]
 },
 {
  "qid": "q0c12905841",
  "kind": "choice",
  "who_decides": "A press officer or news reader who files each release decides what kind of announcement it is so it goes to the right team and archive.",
  "question": "What kind of announcement is this, mainly?",
  "options": [
   {
    "name": "event or celebration",
    "definition": "A ceremony, awards, public gathering or observance day is the headline news; pick it when the news is about something that takes place on a particular day."
   },
   {
    "name": "money given or paid",
    "definition": "Money is granted, paid or handed to a named group or person as the headline news; pick it over the physical project when the payment is the headline and not the work it pays for."
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
    "name": "new or changed program",
    "definition": "A service, scheme or initiative is set up or changed so that people can sign up for it or use it on an ongoing basis; pick it when people will take part in something that keeps running."
   },
   {
    "name": "physical project",
    "definition": "Work on a building, road, park, equipment or land is the headline news, even if money is also mentioned; pick it when the thing being built, bought, repaired or opened is the headline."
   },
   {
    "name": "warning or advice",
    "definition": "The text tells people how to stay safe or avoid a risk without creating any legal duty; pick it when the text says what people should do, not what they must do."
   }
  ]
 },
 {
  "qid": "qc621c5322d",
  "kind": "choice",
  "who_decides": "A travel guide editor decides what kind of advice a passage gives, so that the right kind of tip reaches the reader.",
  "question": "What kind of information does this passage give the visitor?",
  "options": [
   {
    "name": "prices",
    "definition": "Pick this when the text gives money amounts or fares that a visitor will pay."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the text gives none of the kinds above, for example a story, a quote or a personal experience."
   },
   {
    "name": "suggested choice",
    "definition": "Pick this when the text advises the reader to prefer one option, using words like wise, better or opt for, without saying it is required; if it says it is required, pick rules to follow."
   },
   {
    "name": "rules to follow",
    "definition": "Pick this when the text says something is required, banned, mandatory, essential or regulated, even if it also mentions timing."
   },
   {
    "name": "timing",
    "definition": "Pick this when the text says when something runs, opens or closes, how often it runs, or how long a trip takes, and it states no requirement."
   },
   {
    "name": "plain facts",
    "definition": "Pick this when the text states what the place or service is, such as its size, history, location or owner, and gives no advice to act."
   }
  ]
 },
 {
  "qid": "q0173c0d4b5",
  "kind": "choice",
  "who_decides": "A learning-support worker who decides what a reader should be asked to do next after reading a text.",
  "question": "What does this text most want the reader to do next?",
  "options": [
   {
    "name": "practise yourself",
    "definition": "Pick this when the text sets an exercise, drill or task that the reader must do alone and then check; if the text only shows the steps being carried out, pick follow the steps instead."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the text asks for an action that none of the other five labels covers, such as a payment or a purchase."
   },
   {
    "name": "follow the steps",
    "definition": "Pick this when the text shows a sequence of working steps that reach a result, which the reader is meant to watch and copy; if the text asks the reader to do the work alone, pick practise yourself instead."
   },
   {
    "name": "learn the facts",
    "definition": "Pick this when the text gives facts, meanings or dates for the reader to know and shows no working steps and sets no task; if it shows a sequence of steps to a result, pick follow the steps instead."
   },
   {
    "name": "improve the resource",
    "definition": "Pick this when the text asks the reader to fix, add to, translate or report problems in the material itself; if the work is meant to build the reader's own skill, pick practise yourself instead."
   },
   {
    "name": "join or sign up",
    "definition": "Pick this when the text invites the reader to enrol in a course, join a group, or take part in a programme as a member or student; if the aim is to change the document, pick improve the resource instead."
   }
  ]
 },
 {
  "qid": "qd0ae9c8d82",
  "kind": "choice",
  "who_decides": "A journal editor or library staff member who sorts new biology preprints by the kind of study they report, so readers can find the right type of work.",
  "question": "What kind of study does the abstract mainly report?",
  "options": [
   {
    "name": "lab experiments",
    "definition": "The main work is experiments the authors ran themselves on cells, organisms, materials or samples they collected or prepared, and the text names these as the core of the study. Pick this over existing data when the authors' own experiments are the core, and over balanced mix when only experiments are named as the core."
   },
   {
    "name": "new tool or method",
    "definition": "The main contribution is a software tool, algorithm or workflow that others can use, presented as the product itself rather than as a finding about biology. Pick this over existing data when the text is mainly about the tool and not about what the data showed."
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
    "name": "something else",
    "definition": "The text reports no new study, data, model or tool of its own, such as a review of others' work or an opinion piece. Pick this only when none of the other kinds applies at all."
   },
   {
    "name": "balanced mix",
    "definition": "The text names two or more of the kinds above as equally central, and no single kind is clearly the core. Pick this only when no one kind is named as the core; if one kind is named as the core, pick that kind instead."
   }
  ]
 },
 {
  "qid": "q62e1c3861b",
  "kind": "choice",
  "who_decides": "A teacher choosing which kind of study material to hand a class for a lesson, so each item fits the job it is meant to do.",
  "question": "What kind of study material is this passage?",
  "options": [
   {
    "name": "course or program page",
    "definition": "Pick when the text describes a lesson, course or coaching program and invites the reader to take part or sign up; pick outline when it only lists the parts of a book or course without inviting anyone in."
   },
   {
    "name": "research report",
    "definition": "Pick when the text describes a study's question, methods, data or findings; pick reference article when it explains a concept without reporting any study or test."
   },
   {
    "name": "reference article",
    "definition": "Pick when the text explains one topic in connected prose so it can be looked up, with background and detail; pick glossary instead when it lists many separate terms, each with a short meaning."
   },
   {
    "name": "glossary",
    "definition": "Pick when the text is a list of terms, each with a short meaning and no connected story; pick reference article when the meanings sit inside a longer explanation."
   },
   {
    "name": "outline",
    "definition": "Pick when the text is a skeleton of headings, sections or chapter parts with little explanation of each; pick course or program page when it describes a course and invites the reader to join."
   },
   {
    "name": "practice questions",
    "definition": "Pick when the text is mainly a set of questions for the learner to answer; pick outline when it lists sections or headings rather than asking questions."
   }
  ]
 },
 {
  "qid": "q8ee74ffa43",
  "kind": "choice",
  "who_decides": "A labeller reading a whole travel guide entry decides its overall mood, apart from any single sentence, so that entries can be compared by how they sound as a whole.",
  "question": "What is the overall mood of the whole text, taken as one piece?",
  "options": [
   {
    "name": "adventurous",
    "definition": "Pick this when the whole text has a sense of wild, rugged or demanding challenge and exploration, such as remote trails, jungle, snow or wild animals; the sense of challenge, not fun, is the dividing line from upbeat."
   },
   {
    "name": "dry factual",
    "definition": "Pick this when the whole text has a flat, plain reference tone, listing facts, figures, names or how-to steps with no mood-setting words or images."
   },
   {
    "name": "mixed or unclear",
    "definition": "Pick this only when two or more moods above are about equally strong in the whole text, or when the text is too thin to name any mood."
   },
   {
    "name": "calm",
    "definition": "Pick this when the whole text is quiet and restful, with soft images of nature, water, light or a slow pace; the use of soft, peaceful imagery is the dividing line from dry factual."
   },
   {
    "name": "grave",
    "definition": "Pick this when the whole text is serious and reflective, dwelling on hardship, loss, history or sacred matters in a solemn way; a reflective weight is the dividing line from stern."
   },
   {
    "name": "stern",
    "definition": "Pick this when the whole text reads as firm and rule-like, mostly giving orders and must-nots with words such as must, always or do not; a tone of commands, not of reflection, is the dividing line from grave."
   },
   {
    "name": "upbeat",
    "definition": "Pick this when the whole text is cheerful and friendly, using light words such as fun, lively or welcoming, with no sense of risk or wild challenge; a bright, sociable tone is the dividing line from adventurous."
   }
  ]
 },
 {
  "qid": "qdf5e41cbf5",
  "kind": "choice",
  "who_decides": "A visitor reading a museum description decides which part of the story the text mainly gives them, so they know whether it answers their question.",
  "question": "What does this description mainly tell a visitor about?",
  "options": [
   {
    "name": "artist background",
    "definition": "The text is mainly about the maker's life, training, travels or career; pick this over historical setting when most of the detail is about the person rather than the world around the work."
   },
   {
    "name": "making process",
    "definition": "The text is mainly about how the work was made, such as its materials, tools, technique or steps, and not about the maker's life or the work's message."
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
    "name": "historical setting",
    "definition": "The text is mainly about the time, place, or social or political situation the work came from; pick this over artist background when most of the detail is about that wider world rather than the person."
   }
  ]
 },
 {
  "qid": "q5c6b6a4be4",
  "kind": "choice",
  "who_decides": "A reader who decides which group of people a new biology preprint is most useful to, so that it is passed to the right people first.",
  "question": "Which group could most use this result?",
  "options": [
   {
    "name": "doctors and clinic staff",
    "definition": "Pick this when the result would mainly help people treating individual patients now, such as with diagnosis or the choice of care; if it would guide choices for whole communities, pick public health planners instead."
   },
   {
    "name": "drug and treatment makers",
    "definition": "Pick this when the result would mainly help people finding, improving, or choosing a compound or drug to treat a disease; if it would help a doctor treat a patient now, pick doctors and clinic staff instead."
   },
   {
    "name": "other researchers planning experiments",
    "definition": "Pick this when the result would mainly help other scientists choose what to test or how to design their own lab or animal work, rather than a product, a patient, or a whole population."
   },
   {
    "name": "builders of data tools",
    "definition": "Pick this when the result would mainly help people who build software, models, or analysis tools, by giving them a method or code to use on their own data; if it gives scientists a biological finding to test, pick other researchers planning experiments instead."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the result would mainly help none of these groups, such as teachers, students, or the general public who only want to learn about the science."
   },
   {
    "name": "public health planners",
    "definition": "Pick this when the result would mainly help people making plans for whole communities, such as disease spread, prevention, or policy; if it is about one patient's care, pick doctors and clinic staff instead."
   }
  ]
 },
 {
  "qid": "q59560039ed",
  "kind": "choice",
  "who_decides": "A visitor choosing between programs decides what they are meant to gain from this one, using only the listing's stated purpose.",
  "question": "What is a visitor mainly meant to get out of this program?",
  "options": [
   {
    "name": "make something",
    "definition": "Pick this when the main activity is the visitor creating an object to keep or take home, such as a craft, painting or card; a listing where the visitor only watches or hears is not this."
   },
   {
    "name": "see a display",
    "definition": "Pick this when the listing centres on looking at exhibits, vehicles, trains or other objects on show, without saying the visitor will be taught about them."
   },
   {
    "name": "fun outing or party",
    "definition": "Pick this when the listing presents the program as an enjoyable event or night out, such as a party, tasting or social gathering, and does not name learning, making, display or fundraising as its main goal."
   },
   {
    "name": "support a cause",
    "definition": "Pick this when the listing says the main purpose is raising money for a named group, fund or museum; if the listing is mainly about a fun gathering, pick fun outing or party instead."
   },
   {
    "name": "learn a topic",
    "definition": "Pick this when the listing says visitors will be taught or told facts about a subject such as history, nature or science, with explanation as the main goal; a listing that only lets visitors look at objects is see a display instead."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the listing states a main purpose that is none of the five options above, such as a service or a sign-up for membership."
   }
  ]
 },
 {
  "qid": "qfef8314bba",
  "kind": "choice",
  "who_decides": "A museum writer who decides which kind of text an existing description can be reused for, since each job needs a different length and tone.",
  "question": "What job is this description mainly written to do?",
  "options": [
   {
    "name": "explain to visitors",
    "definition": "Tells a viewer what to notice in this object and why it matters here. Pick this when the text points at this object's features while guiding looking, and does not mainly teach a wider idea."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the main job is none of the four above, such as a notice about visiting hours or a call for donations."
   },
   {
    "name": "record the facts",
    "definition": "Sets out plain facts about the object, such as what it is, who made it, and when, in neutral reference language. Pick this when the text gives no guidance on how to look at the object."
   },
   {
    "name": "tell a story",
    "definition": "Follows events in order, or a person's experience or own words, to carry the reader through an account. Pick this when the text is mostly a sequence of events or an anecdote."
   },
   {
    "name": "teach an idea",
    "definition": "Explains a general custom, term, or belief that reaches beyond this one object. Pick this when the main content would still make sense if the object were removed from the text."
   }
  ]
 }
]
