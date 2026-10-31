# Item 10 card G-LEX read I10-ext-rB-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/extract_answers/I10-ext-rB-002.json

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

Write ONE JSON object, and nothing else (no text before or after it), to the answer file named at the top. task_id must be "I10-ext-rB-002".
{"task_id": "I10-ext-rB-002",
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
  "qid": "q6cc4d0e5b4",
  "kind": "choice",
  "who_decides": "The news desk editor who sorts each incoming story by the kind of event it reports before filing it.",
  "question": "What kind of event or development does the story mainly report?",
  "options": [
   {
    "name": "game result",
    "definition": "The story reports the final score or outcome of a finished game or match."
   },
   {
    "name": "incident or violence",
    "definition": "The story reports a harmful event that has already happened, such as an attack, a riot or an accident, rather than a rule or a set of talks."
   },
   {
    "name": "research finding",
    "definition": "The story reports the results of a study, test or experiment."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the story's main event fits none of the other six, such as a product launch, a weather event or a business announcement."
   },
   {
    "name": "talks or deal",
    "definition": "The story reports negotiations between parties that resume, stall or end in an agreement, but does not say that a rule has taken effect."
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
  "qid": "qd36f991fd2",
  "kind": "choice",
  "who_decides": "A data librarian who sorts newly published open-data datasets by the kind of records they hold, so people can find them.",
  "question": "What kind of records does the dataset hold?",
  "options": [
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
    "name": "rates or percentages",
    "definition": "Pick when the rows report a share, rate or percent for a group, such as the percent with a condition, instead of a raw total."
   },
   {
    "name": "money amounts",
    "definition": "Pick when the rows mainly report dollar amounts, such as spending, income, grants, bonds or donations, rather than counts of people or items."
   },
   {
    "name": "places and contact details",
    "definition": "Pick when the rows describe sites or organisations by name, address, location or contact details, with no money, counts or events."
   }
  ]
 },
 {
  "qid": "q4af8ce3dc5",
  "kind": "choice",
  "who_decides": "A news site editor who labels the overall mood of each story for a mood-based story feed.",
  "question": "Apart from any single sentence, what mood does the whole text give off?",
  "options": [
   {
    "name": "grim",
    "definition": "Pick this when the whole text dwells on loss, suffering or failure, and the bad outcome is already settled; pick tense instead when the outcome is still open."
   },
   {
    "name": "upbeat",
    "definition": "Pick this when the whole text is bright and celebrates good outcomes or progress; pick playful instead when the lightness comes from humour rather than good news."
   },
   {
    "name": "even-toned",
    "definition": "Pick this only when no overall mood stands out and the text reads as a plain account pulling neither way; if one mood clearly dominates the whole text, pick that mood instead."
   },
   {
    "name": "tense",
    "definition": "Pick this when the whole text is built around an open contest, dispute or pending event whose outcome is still unknown; pick grim instead when the bad news is already settled."
   },
   {
    "name": "playful",
    "definition": "Pick this when the whole text is light and teasing, using wit or humour as its overall style rather than good news."
   }
  ]
 },
 {
  "qid": "q1b770c3ba6",
  "kind": "choice",
  "who_decides": "A news desk editor choosing which follow-up queue a story joins, because first reports, updates, and results are checked differently.",
  "question": "Where does this story stand at the time it is published?",
  "options": [
   {
    "name": "first news",
    "definition": "The event has just been reported and key facts such as cause, toll, or next steps are still unknown or unconfirmed; pick \"new step\" instead when the text refers to an earlier report or decision in the same story."
   },
   {
    "name": "after-effects",
    "definition": "The result is already known and the text covers what followed, such as damage, shortages, reactions, costs, or repairs; pick this over \"final outcome\" when the consequences are the main point."
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
    "name": "other stage",
    "definition": "Pick this only when the text does not report the course of a specific event at all, such as a background piece, a feature, or a general list."
   }
  ]
 },
 {
  "qid": "qeed3489d69",
  "kind": "choice",
  "who_decides": "The volunteer centre's scheduling coordinator decides where the work happens, so volunteers know what conditions to expect and whether they can travel there.",
  "question": "Where does the volunteer actually do the work?",
  "options": [
   {
    "name": "from home",
    "definition": "Pick when the volunteer does the work from their own home on a computer or phone and does not travel to a site; dividing line: no travel to a place for the work."
   },
   {
    "name": "outdoors in the open",
    "definition": "Pick when the work is done outside on land such as a farm, garden, or park at a fixed spot, where weather matters; dividing line: outside work at one place, not travel between homes or streets."
   },
   {
    "name": "indoors at a site",
    "definition": "Pick when the work happens inside one building the volunteer travels to, such as a kitchen, food bank, or office; dividing line: all the work stays inside one building."
   },
   {
    "name": "out in the community",
    "definition": "Pick when the volunteer moves between several places, or goes to people's homes or streets to deliver, visit, or do outreach; dividing line: moving between places, not staying at one spot."
   },
   {
    "name": "something else",
    "definition": "Pick only when the text does not say where the work happens, or names a school or youth program site as the place of work."
   }
  ]
 },
 {
  "qid": "q78903f2d31",
  "kind": "choice",
  "who_decides": "A learning-support worker who decides what a reader should be asked to do next after reading a text.",
  "question": "What does this text most want the reader to do next?",
  "options": [
   {
    "name": "join or sign up",
    "definition": "Pick this when the text invites the reader to enrol in a course, join a group, or take part in a programme as a member or student; if the aim is to change the document, pick improve the resource instead."
   },
   {
    "name": "practise yourself",
    "definition": "Pick this when the text sets an exercise, drill or task that the reader must do alone and then check; if the text only shows the steps being carried out, pick follow the steps instead."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the text asks for an action that none of the other five labels covers, such as a payment or a purchase."
   },
   {
    "name": "learn the facts",
    "definition": "Pick this when the text gives facts, meanings or dates for the reader to know and shows no working steps and sets no task; if it shows a sequence of steps to a result, pick follow the steps instead."
   },
   {
    "name": "follow the steps",
    "definition": "Pick this when the text shows a sequence of working steps that reach a result, which the reader is meant to watch and copy; if the text asks the reader to do the work alone, pick practise yourself instead."
   },
   {
    "name": "improve the resource",
    "definition": "Pick this when the text asks the reader to fix, add to, translate or report problems in the material itself; if the work is meant to build the reader's own skill, pick practise yourself instead."
   }
  ]
 },
 {
  "qid": "qc61626bf94",
  "kind": "choice",
  "who_decides": "A help volunteer who decides how much background to ask for and which answer to give first, since the reply depends on what the poster has already tried.",
  "question": "How far has the poster already got with the problem?",
  "options": [
   {
    "name": "solved, wants better way",
    "definition": "The poster already has a working answer and asks only for a simpler, cleaner or more reliable method; pick it when the goal is fully met and only the method is in question."
   },
   {
    "name": "tried fixes, none worked",
    "definition": "The poster lists fixes already tried, such as restarting, repairing, reinstalling or changing a setting, and none solved it; pick it when every attempt failed."
   },
   {
    "name": "partial answer found",
    "definition": "The poster reached part of the goal through a found method, but a piece still fails or is missing; pick it when some of the goal works and the rest is still open."
   },
   {
    "name": "using a workaround",
    "definition": "The poster has a different route that avoids the goal, such as a script or another program, and wants the original route fixed; pick it when the workaround replaces the goal rather than reaching part of it."
   },
   {
    "name": "nothing tried yet",
    "definition": "The poster states the problem and the question but names no step taken to solve it; pick it when the text names no attempt at a fix."
   }
  ]
 },
 {
  "qid": "q22f31286f0",
  "kind": "choice",
  "who_decides": "A help-desk volunteer who routes forum posts to the right helper, because a post sent to the wrong kind of helper wastes time for everyone.",
  "question": "What does the poster most want from a helper?",
  "options": [
   {
    "name": "something else",
    "definition": "Pick this when the post asks for none of the above, such as a feature wish, a general complaint with no question, or a request for a free opinion."
   },
   {
    "name": "is it a bug",
    "definition": "Pick this when the poster asks whether the behaviour is a software fault or is expected or normal, and does not ask how to change anything; if they ask how to make it work, pick get a step to work instead."
   },
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
   }
  ]
 },
 {
  "qid": "qf9f6905cb9",
  "kind": "choice",
  "who_decides": "A travel guide editor decides what kind of advice a passage gives, so that the right kind of tip reaches the reader.",
  "question": "What kind of information does this passage give the visitor?",
  "options": [
   {
    "name": "suggested choice",
    "definition": "Pick this when the text advises the reader to prefer one option, using words like wise, better or opt for, without saying it is required; if it says it is required, pick rules to follow."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the text gives none of the kinds above, for example a story, a quote or a personal experience."
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
    "name": "prices",
    "definition": "Pick this when the text gives money amounts or fares that a visitor will pay."
   },
   {
    "name": "plain facts",
    "definition": "Pick this when the text states what the place or service is, such as its size, history, location or owner, and gives no advice to act."
   }
  ]
 },
 {
  "qid": "qa4caa540a5",
  "kind": "choice",
  "who_decides": "A conservator who fills the materials line of a catalogue record and needs one main making method for each object.",
  "question": "How was the object mainly made?",
  "options": [
   {
    "name": "woven or stitched",
    "definition": "Made by interlacing threads or fibres, or by sewing pieces together. Pick this when yarn, thread, weaving, or sewing is the main method."
   },
   {
    "name": "something else",
    "definition": "Pick this only when none of the methods above is the main one, such as a photograph or a mixed assembly of unrelated parts."
   },
   {
    "name": "painted or drawn",
    "definition": "Made by hand, applying colour or marks directly to the surface with a brush, pencil, or ink. Pick this when the text says the image was applied by hand, not transferred from another surface."
   },
   {
    "name": "modelled or cast",
    "definition": "Made by shaping soft material such as clay or wax, or by pouring liquid material into a mould. Pick this when the text says the form was built up, modelled, moulded, or cast."
   },
   {
    "name": "carved or cut",
    "definition": "Made by taking material away from one solid piece, such as wood, stone, or horn. Pick this when the text says the form was cut, carved, or shaped out of a single block."
   },
   {
    "name": "printed",
    "definition": "Made by pressing inked surfaces such as a plate, block, or screen onto paper or cloth. Pick this when the text says the image was transferred from a plate, block, or screen, even if that plate was drawn by hand."
   }
  ]
 },
 {
  "qid": "q6d41f87c88",
  "kind": "choice",
  "who_decides": "The volunteer who sorts incoming help-forum posts, so each post is matched to the kind of help the poster is asking a helper for.",
  "question": "What does the poster want from a helper?",
  "options": [
   {
    "name": "pick an approach",
    "definition": "Pick this when the poster names more than one way to reach a goal and wants help choosing the best one; pick find a setting instead when the text is about where one known control is."
   },
   {
    "name": "quick workaround",
    "definition": "Pick this when the poster wants a way around the problem now and says the fix is temporary or accepts a stopgap; pick permanent cure instead when they want it gone for good."
   },
   {
    "name": "add-on or outside tool",
    "definition": "Pick this only when the poster asks for a third-party extension, template, or outside program to do the job, not for a built-in method."
   },
   {
    "name": "something else",
    "definition": "Pick this when the poster asks for nothing from a helper and only shares news, a result, or feedback."
   },
   {
    "name": "permanent cure",
    "definition": "Pick this when the poster wants the root cause removed so the problem does not come back, or says a stopgap is not enough; pick quick workaround when a temporary way round is accepted."
   },
   {
    "name": "find a setting",
    "definition": "Pick this when the poster knows a named option or value exists and wants help locating it; a request to choose between methods belongs under pick an approach."
   }
  ]
 },
 {
  "qid": "q0be0c902a1",
  "kind": "choice",
  "who_decides": "A labeller reading a whole travel guide entry decides its overall mood, apart from any single sentence, so that entries can be compared by how they sound as a whole.",
  "question": "What is the overall mood of the whole text, taken as one piece?",
  "options": [
   {
    "name": "upbeat",
    "definition": "Pick this when the whole text is cheerful and friendly, using light words such as fun, lively or welcoming, with no sense of risk or wild challenge; a bright, sociable tone is the dividing line from adventurous."
   },
   {
    "name": "adventurous",
    "definition": "Pick this when the whole text has a sense of wild, rugged or demanding challenge and exploration, such as remote trails, jungle, snow or wild animals; the sense of challenge, not fun, is the dividing line from upbeat."
   },
   {
    "name": "stern",
    "definition": "Pick this when the whole text reads as firm and rule-like, mostly giving orders and must-nots with words such as must, always or do not; a tone of commands, not of reflection, is the dividing line from grave."
   },
   {
    "name": "grave",
    "definition": "Pick this when the whole text is serious and reflective, dwelling on hardship, loss, history or sacred matters in a solemn way; a reflective weight is the dividing line from stern."
   },
   {
    "name": "dry factual",
    "definition": "Pick this when the whole text has a flat, plain reference tone, listing facts, figures, names or how-to steps with no mood-setting words or images."
   },
   {
    "name": "calm",
    "definition": "Pick this when the whole text is quiet and restful, with soft images of nature, water, light or a slow pace; the use of soft, peaceful imagery is the dividing line from dry factual."
   },
   {
    "name": "mixed or unclear",
    "definition": "Pick this only when two or more moods above are about equally strong in the whole text, or when the text is too thin to name any mood."
   }
  ]
 },
 {
  "qid": "q292171aeb6",
  "kind": "choice",
  "who_decides": "A research reader or database curator who files each preprint by the kind of result it reports, so people searching for one kind of finding can find it.",
  "question": "What kind of result is the abstract's main finding?",
  "options": [
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
   },
   {
    "name": "new thing identified",
    "definition": "The main result is a previously unknown item, such as a gene, group, type, species or class, found and named by the authors. Pick this over how something works when the item itself was not known before."
   },
   {
    "name": "link seen",
    "definition": "Two or more things were measured and found to go together or change together, with no deliberate change by the authors shown to cause the other. Pick this over cause shown when nothing was changed on purpose."
   },
   {
    "name": "how something works",
    "definition": "The main result describes the shape, parts or step-by-step action of a thing already known, such as a structure or mechanism. Pick this over new thing identified when the thing was already known and the new content is its detail."
   }
  ]
 },
 {
  "qid": "q9d09d292b6",
  "kind": "choice",
  "who_decides": "The reader deciding, after the headline and first lines, whether to act on the story, keep it in mind or skip it.",
  "question": "What does the story most ask or mean for the reader to do or expect?",
  "options": [
   {
    "name": "no direct effect",
    "definition": "The story is for information only and gives the reader no practical change, benefit, risk or step, so it touches them only in a general way."
   },
   {
    "name": "safety warning",
    "definition": "The story's main point is a danger to the reader's health, safety or property that they should avoid, rather than a step they must take to keep a right or benefit."
   },
   {
    "name": "must act now",
    "definition": "The story names a step the reader has to take soon, such as signing up, paying, registering or voting, to keep a right or benefit."
   },
   {
    "name": "something else",
    "definition": "Pick this only when none of the other five fits the reader's stake best, for example when the story is an opinion piece that only asks the reader to consider a view."
   },
   {
    "name": "could benefit",
    "definition": "The story says the reader may gain something good now, such as a discount, a free event or a new service, and no step is required."
   },
   {
    "name": "affected later",
    "definition": "The story says a change will reach the reader's life later and names no step the reader must take now, unlike no direct effect, which says nothing practical changes for them."
   }
  ]
 },
 {
  "qid": "q49cface6da",
  "kind": "choice",
  "who_decides": "A fact-checker deciding how far to trust a story's main facts, because each kind of source needs a different check.",
  "question": "What do the story's key facts mainly rest on?",
  "options": [
   {
    "name": "official statement",
    "definition": "The key facts are what a person in an official role said on the record, such as a minister, a police spokesperson, or a company head; pick \"written record\" if the facts come from a document the writer read, and \"count or measure\" if they are mainly figures."
   },
   {
    "name": "count or measure",
    "definition": "The key facts are figures someone counted or measured, such as votes, scores, deaths, attendance, or amounts; pick this over the others whenever the figures are the main facts, even if an official or a document gave them."
   },
   {
    "name": "mixed or unclear",
    "definition": "The key facts come from several sources with none dominant, or the text names no source for them; use this only when no other option clearly fits."
   },
   {
    "name": "eyewitness account",
    "definition": "The key facts come from people who saw the event or were at the scene and speak in their own words, such as a passer-by, a fan, or a resident; pick \"official statement\" when the speaker is on duty or in an official role."
   },
   {
    "name": "written record",
    "definition": "The key facts come from a document, filing, report, or published text that the writer names or describes, not from a person speaking; pick \"count or measure\" if the document's main content is totals."
   }
  ]
 },
 {
  "qid": "qe0c43e6b1a",
  "kind": "choice",
  "who_decides": "A museum education staffer who chooses which short panel text to show visitors who want to know more about an object.",
  "question": "What does the visitor most need from this text?",
  "options": [
   {
    "name": "cultural background",
    "definition": "Pick this when the text places the work in its time, place, school, or tradition, such as a period, country, or art movement; if the text explains what the imagery or symbols mean, pick understand the meaning."
   },
   {
    "name": "artist story",
    "definition": "Pick this when the text describes the maker's life, training, career, or working history; a summary of the steps used to make one object goes to how it was made instead."
   },
   {
    "name": "understand the meaning",
    "definition": "Pick this when the text explains what the image or object stands for, its message, symbols, or the maker's intent; if the text places the work in its era, country, or tradition instead, pick cultural background."
   },
   {
    "name": "how it was made",
    "definition": "Pick this when the text explains the materials, techniques, steps, or process used to make this object; if the text describes the maker's life or career across many works, pick artist story instead."
   },
   {
    "name": "archive access",
    "definition": "Pick this when the text is a collection or archive description that tells the visitor how to visit a reading room, request material by appointment, or browse finding aids; if the text describes one object to look at, pick one of the object-focused labels instead."
   }
  ]
 },
 {
  "qid": "qc56ff7ae13",
  "kind": "choice",
  "who_decides": "The writer of the release chooses how to present the decision, so the reader sees the measure as a routine step, a gain, a cost, a warning or a conflict.",
  "question": "How does the text mainly present the decision, measure or event?",
  "options": [
   {
    "name": "something else",
    "definition": "Pick this only when none of the labels above fits as the text's main way of presenting the matter."
   },
   {
    "name": "dispute or conflict",
    "definition": "Pick this when the text reports people or groups disagreeing with, or fighting over, a decision or event."
   },
   {
    "name": "warning of risk",
    "definition": "Pick this when the text's main point is a danger, with advice to take action now; pick routine notice when the text only gives dates and steps without any danger."
   },
   {
    "name": "routine notice",
    "definition": "Pick this when the text only says what will happen, when and how, with no claimed gain, no stressed cost, no danger and no dispute; pick warning of risk when the text tells people to act to avoid danger."
   },
   {
    "name": "stated cost",
    "definition": "Pick this when the text's main point is how much money is spent, owed or needed, and no good result is the headline; pick stated benefit when the good result the money buys is the main point."
   },
   {
    "name": "stated benefit",
    "definition": "Pick this when the text's main point is a good result, such as jobs, savings, better service or growth, even if a cost is also mentioned; pick stated cost when the money itself is the main point."
   }
  ]
 },
 {
  "qid": "q47d886a45b",
  "kind": "choice",
  "who_decides": "A help volunteer who decides which questions to ask back first, since the first useful reply depends on how the problem shows up.",
  "question": "How does the problem show itself to the poster?",
  "options": [
   {
    "name": "crash or freeze",
    "definition": "The program closes by itself or stops responding so that it must be forced to quit; pick it when the program stops working, not when it keeps running and shows a message."
   },
   {
    "name": "no failure shown",
    "definition": "The text describes no failing behaviour at all, only a request for steps, a formula or a feature; pick it when no wrong behaviour is named anywhere in the text."
   },
   {
    "name": "wrong text or breaks",
    "definition": "The characters or line breaks themselves change, such as extra blank lines, lost paragraph breaks or missing letters; pick it when the words or breaks differ, not when only their placement or size is off."
   },
   {
    "name": "wrong layout or spacing",
    "definition": "The words are right but sit, size or space wrongly on the page, such as a picture in the wrong place, lines too far apart or a page that looks too small; pick it when the problem is where things sit, not what the characters are."
   },
   {
    "name": "slow to respond",
    "definition": "The program works but takes minutes to open, load or react, and the text says it finishes eventually; pick it when it is slow but does not stop, not when it freezes or closes."
   },
   {
    "name": "wrong value in a cell",
    "definition": "A spreadsheet cell shows a number, date or error result the poster did not expect; pick it when the wrong thing is a calculated result in a cell, not words in a text document."
   },
   {
    "name": "error message shown",
    "definition": "The program keeps running but shows a message box or names a missing file; pick it when the program stays open, not when it closes or stops responding."
   }
  ]
 },
 {
  "qid": "q0ce1f60488",
  "kind": "choice",
  "who_decides": "A recipe reader choosing which section of a cookbook or menu a recipe belongs in, based on its main food.",
  "question": "Which kind of food is the dish mainly built around, meaning the ingredient with the largest share of the recipe?",
  "options": [
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
   },
   {
    "name": "starch",
    "definition": "Pick when bread, flour, grain, pasta or potatoes are the largest share; for a potato dish, pick vegetable or fruit instead unless the potatoes weigh more than all other vegetables together."
   },
   {
    "name": "meat or fish",
    "definition": "Pick when meat, poultry, fish or seafood is the largest share of the recipe; a meat used only as a small topping or garnish does not count."
   },
   {
    "name": "sugar or sweetener",
    "definition": "Pick when sugar, syrup or another sweetener is the largest share, more than any fruit; a fruit flavoured with a little sugar is vegetable or fruit."
   }
  ]
 },
 {
  "qid": "q1d6245ee7f",
  "kind": "choice",
  "who_decides": "A government public affairs lead choosing the main goal of each release so the team can judge whether the message reached its aim.",
  "question": "What is the main thing this release is trying to get done?",
  "options": [
   {
    "name": "grow jobs or business",
    "definition": "Pick this when the release aims to attract investment, build an industry, or create or support jobs and companies; if the release aims to bring people to a place or activity, pick draw visitors or fans."
   },
   {
    "name": "ask readers to act",
    "definition": "Pick this when the release tells readers to do a task of their own, such as applying, registering, getting tested or reporting something; a fact reported with no task for the reader is share a fact."
   },
   {
    "name": "protect people from harm",
    "definition": "Pick this when the release describes a step or rule meant to stop a crime, danger, illness or loss; a step that only reports results without aiming to prevent harm is share a fact."
   },
   {
    "name": "draw visitors or fans",
    "definition": "Pick this when the release aims to get people to visit a park, attend an event or enjoy a place or activity; if the aim is to grow companies, jobs or an industry, pick grow jobs or business."
   },
   {
    "name": "share a fact",
    "definition": "Pick this when the release simply reports what happened or was decided, with no request that readers do a task and no push to attend or visit; if it asks readers to do a task, pick ask readers to act."
   },
   {
    "name": "something else",
    "definition": "Pick this only when the release's main aim is clearly none of the other options, such as thanking people, honouring a person or recognising a milestone."
   }
  ]
 },
 {
  "qid": "qfb007c5aaa",
  "kind": "choice",
  "who_decides": "A museum collection editor who sorts descriptions by their main focus, so the right ones feed the gallery label and the feature pages.",
  "question": "What does the description spend most of its words on?",
  "options": [
   {
    "name": "use and meaning",
    "definition": "Most words go to what the object was for or what it stood for, such as ritual, daily use, or belief. Pick this when the text explains its purpose or symbolism rather than its setting."
   },
   {
    "name": "origin and era",
    "definition": "Most words go to when and where the object was made and the events of that time. Pick this when the setting or past events lead, not the object's use or meaning."
   },
   {
    "name": "looks and form",
    "definition": "Most words go to what can be seen, such as colour, pattern, shape, marks, or arrangement. Pick this when visible features take more words than anything else."
   },
   {
    "name": "something else",
    "definition": "Pick this only when none of the four above takes the most words, such as a text mostly about a sale, a loan, or a restoration."
   },
   {
    "name": "maker and career",
    "definition": "Most words go to the artist or craftsperson, such as their training, life, habits, or career. Pick this when the person is the main subject, even if the object is also described."
   }
  ]
 },
 {
  "qid": "qfaa5de230d",
  "kind": "choice",
  "who_decides": "A course designer decides which job a passage should do in a lesson plan, so it is placed where that job is needed.",
  "question": "What job does this passage do inside a course?",
  "options": [
   {
    "name": "something else",
    "definition": "Pick this when none of the other jobs fit, such as a sign-up or admin note, and the passage neither teaches nor guides the learner."
   },
   {
    "name": "gives a judging rule",
    "definition": "Pick this when the passage names a standard the reader should check against to decide whether something is good, reliable, or right."
   },
   {
    "name": "explains an idea",
    "definition": "Pick this when the passage says what a concept is or how it works, in plain statements rather than steps, so the learner understands it."
   },
   {
    "name": "tells history or origin",
    "definition": "Pick this when the passage says when, where, or by whom a topic arose or developed, and does not explain how it works."
   },
   {
    "name": "gives steps to do",
    "definition": "Pick this when the passage tells the reader, in order, what to do to carry out a task, so the learner can act on it."
   }
  ]
 },
 {
  "qid": "q73fb4554f6",
  "kind": "choice",
  "who_decides": "A visitor reading a park listing decides whether the program suits them and their group, using only what the listing says about who it is for.",
  "question": "Which kind of visitor is this program mainly aimed at?",
  "options": [
   {
    "name": "anyone, all levels",
    "definition": "Pick this when the listing invites any visitor with no age limit or experience needed, or says all skill levels are encouraged, and does not frame the program as only for newcomers."
   },
   {
    "name": "people who hike",
    "definition": "Pick this when the listing describes a walk, trail, loop or rough terrain as the main activity, so the visitor must be willing to walk; a talk or hands-on activity at one spot is not this."
   },
   {
    "name": "beginners only",
    "definition": "Pick this when the listing frames the program as for people new to the activity, using words like beginners or introductory, even if it does not forbid others; if it says all levels are welcome, pick anyone, all levels instead."
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
  "qid": "q31468fc753",
  "kind": "choice",
  "who_decides": "A reader who decides which group of people a new biology preprint is most useful to, so that it is passed to the right people first.",
  "question": "Which group could most use this result?",
  "options": [
   {
    "name": "public health planners",
    "definition": "Pick this when the result would mainly help people making plans for whole communities, such as disease spread, prevention, or policy; if it is about one patient's care, pick doctors and clinic staff instead."
   },
   {
    "name": "drug and treatment makers",
    "definition": "Pick this when the result would mainly help people finding, improving, or choosing a compound or drug to treat a disease; if it would help a doctor treat a patient now, pick doctors and clinic staff instead."
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
    "name": "doctors and clinic staff",
    "definition": "Pick this when the result would mainly help people treating individual patients now, such as with diagnosis or the choice of care; if it would guide choices for whole communities, pick public health planners instead."
   },
   {
    "name": "other researchers planning experiments",
    "definition": "Pick this when the result would mainly help other scientists choose what to test or how to design their own lab or animal work, rather than a product, a patient, or a whole population."
   }
  ]
 },
 {
  "qid": "q69ffdf6139",
  "kind": "choice",
  "who_decides": "A cook or cookbook editor deciding how to label a recipe's cooking method so that readers can find it.",
  "question": "Which one best describes the main cooking method, meaning the step that does the most to cook or set the food?",
  "options": [
   {
    "name": "pot boil or simmer",
    "definition": "Pick when the main cooking is boiling or simmering food in liquid in a pot or saucepan for a set time; pick steep or brew instead if the liquid is only poured over and left to sit."
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
    "name": "steep or brew",
    "definition": "Pick when hot water is poured over the ingredient and left to sit or infuse, with no set boiling time in a pot; a liquid boiled for several minutes is pot boil or simmer instead."
   },
   {
    "name": "no heat",
    "definition": "Pick when no step cooks the food with heat; the food is only mixed, tossed, layered, poured or served cold."
   },
   {
    "name": "something else",
    "definition": "Pick when the main step is fermenting, freezing, smoking or another method not listed here, and no listed method does the most cooking."
   }
  ]
 }
]
