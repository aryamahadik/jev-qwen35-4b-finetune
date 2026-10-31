# T37b redo2 authoring task T37b-author_wording-3993b49b-002 (family T37b, kind author_wording)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/haiku/redo2/answers/T37b-author_wording-3993b49b-002.json

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 6 objects: one per item below, each item answered once, in any order.
- Each object has exactly two keys: "qid" and "questions". Nothing else.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits, 11 characters in all). The qids of this task: qcb16891c21, q15fabde1d6, q33af204e5b, qb3bd39321c, q509718b2ee, q4cdf54a364.
- "questions": a JSON list of exactly 5 strings: the new questions, each one line ending with a question mark, in the order of the item's style hints.
- Valid JSON only: nothing before or after the array, without markdown code fences or comments. Inside JSON strings write a double quote as \".
Literal example of the shape (the qid shown is the first real one): [{"qid": "qcb16891c21", "questions": ["<question 1>?", "<question 2>?", "<question 3>?", "<question 4>?", "<question 5>?"]}, ...]

Task kind: author_wording; items: 6.

## Instructions

You rewrite questions for a reading test. Each item gives one question, or a question template whose words in capital letters inside curly braces are placeholders, plus rules. For each item write exactly as many new questions as the item's rules ask for. Every new question must ask exactly the same thing as the item's question: a reader who knows the facts must give the same answer to both, in every possible case. Do not answer the question, do not explain, and do not add facts, names or numbers. Reply with JSON only: a list with one object per item, {"qid": <the item's qid>, "questions": [<question 1>, ..., <question k>]}. Every question is one line ending with a question mark, and all of them differ from each other and from the item's question. Some items also give a required shape, or a word to write in place of a word of the item's question: follow those rules exactly, because a program throws away every question that breaks a rule.

## Items (6; answer every item, keyed by its qid)

```json
[
 {
  "qid": "qcb16891c21",
  "brief": "Question: In its reply, did the assistant find at least one option that meets everything the customer asked for?",
  "slots": [],
  "rules": [
   "Write 5 questions; question i follows style hint i: (1) make it as short as you can while keeping every condition; (2) make it a little more formal; (3) make it a little more conversational, in plain everyday words; (4) put the main condition at the end of the question; (5) use a noun instead of the main verb where that keeps the meaning (for example 'Is there confirmation that ...').",
   "Ask exactly the same thing: keep every condition and every person or thing the question names.",
   "Ask the question directly: do not open with a phrase that asks whether a statement holds, do not ask whether something is the answer, and do not ask for an opinion.",
   "The item's question says 'at least one'. Keep that meaning, but write it as 'at least a single' (for example 'at least a single option'): keep the word 'least' exactly once and never write the word 'one' anywhere. Never put 'any', 'some', 'one or more' or a digit in its place: a program throws away every such question.",
   "Keep each of these words, exactly as many times as in the question: 'everything', 'least'.",
   "Do not use any of these words or phrases: all, always, any, anybody, anyone, anything, barely, both, cannot, could, decline, deny, each, either, every, everybody, everyone, exactly, except, fail, false, few, fewer, half, hardly, just, lack, less, majority, many, may, might, more, most, much, must, n't, need, needs, neglect, neither, never, nobody, none, nor, not, nothing, nowhere, often, omit, only, ought, prevent, refuse, scarcely, several, shall, should, some, somebody, someone, something, sometimes, unless, usually, will, without, would; and do not add any other negative word.",
   "Never write a number word (such as one, two, three, first, second, twice, half or dozen), a time word (such as last, next, now, today, earlier, later, recently, currently, previously, soon, already, yet or past) or a hedge word (such as maybe, perhaps, probably, possibly, likely, apparently, seems, appears, think, believe, guess, almost, nearly or roughly): a program throws away every question that holds one.",
   "Use a capital letter only for the first word of the question. Do not use digits."
  ]
 },
 {
  "qid": "q15fabde1d6",
  "brief": "Question template: According to the assistant's last message, is {SPAN} confirmed for {ORDER}?",
  "slots": [
   "ORDER",
   "SPAN"
  ],
  "rules": [
   "Write 5 questions; question i follows style hint i: (1) name the text first with 'According to' or 'In', then ask; (2) change two or three words for exact synonyms and keep the rest; (3) write it as one plain sentence with as few commas as possible; (4) keep the main verb but change the word order; (5) use a different verb or phrase with exactly the same meaning.",
   "Ask exactly the same thing: keep every condition and every person or thing the question names.",
   "Ask the question directly: do not open with a phrase that asks whether a statement holds, do not ask about an answer or an option, and do not ask for an opinion.",
   "The item's question says 'the assistant's last message': the final message the assistant sent in the conversation. Keep that meaning, but write it as 'the assistant's final message', 'the assistant's latest message' or 'the final message from the assistant'. Never write the word 'last', and never 'most recent' or 'previous': a program throws away every such question.",
   "Do not use any of these words or phrases: all, always, any, anybody, anyone, anything, barely, both, cannot, could, decline, deny, each, either, every, everybody, everyone, everything, exactly, except, fail, false, few, fewer, half, hardly, just, lack, least, less, majority, many, may, might, more, most, much, must, n't, need, needs, neglect, neither, never, nobody, none, nor, not, nothing, nowhere, often, omit, only, ought, prevent, refuse, scarcely, several, shall, should, some, somebody, someone, something, sometimes, unless, usually, will, without, would; and do not add any other negative word.",
   "Never write a number word (such as one, two, three, first, second, twice, half or dozen), a time word (such as last, next, now, today, earlier, later, recently, currently, previously, soon, already, yet or past) or a hedge word (such as maybe, perhaps, probably, possibly, likely, apparently, seems, appears, think, believe, guess, almost, nearly or roughly): a program throws away every question that holds one.",
   "Use a capital letter only for the first word of the question. Do not use digits.",
   "Use each placeholder exactly once, written exactly as shown, and do not use any other placeholder: {ORDER}, {SPAN}.",
   "{ORDER} stands for a phrase that starts with \"the customer's\" and names what the customer wanted (for example the customer's pizza order). Write {ORDER} as it is, without a word such as 'the' before it.",
   "{SPAN} stands for a short value quoted from the conversation, quotation marks included (for example a time, a place or an item). Write {SPAN} as it is, without adding quotation marks around it.",
   "Already taken (never repeat these): Per the assistant's latest message, is {SPAN} confirmed for {ORDER}?"
  ]
 },
 {
  "qid": "q33af204e5b",
  "brief": "Question template: Of these two statements, does Statement {N} go against common sense?",
  "slots": [
   "N"
  ],
  "rules": [
   "Write 5 questions; question i follows style hint i: (1) ask with 'is it' followed by a phrase that means exactly 'going against common sense'; (2) open with a phrase that says where the statements are (shown, given, listed or presented); (3) make it as short as you can while keeping every condition; (4) make it a little more formal; (5) make it a little more conversational, in plain everyday words.",
   "Ask exactly the same thing: keep every condition and every person or thing the question names.",
   "Ask the question directly: do not open with a phrase that asks whether a statement holds, do not ask about an answer or an option, and do not ask for an opinion.",
   "Every question must have this shape: a short opening phrase that refers to the statements the reader sees without counting them (for example 'Of the statements shown' or 'Looking at the pair of statements'), then a colon, then the words Statement {N} right after the colon, then the rest of the question in lowercase letters, which refers back to Statement {N} with 'it' or 'this statement' and asks whether it goes against common sense. Shape example for a different question (never copy it): 'Of the cards on the table: Card {N}, is it red?'",
   "The item's question says 'these two statements'. Never write 'two', and never any other counting word (one, both, either, each): call them the statements shown, given or listed, or the pair of statements.",
   "Keep each of these words, exactly as many times as in the question: 'common'.",
   "Do not use any of these words or phrases: agree with, make sense, all, always, any, anybody, anyone, anything, barely, both, cannot, could, decline, deny, each, either, every, everybody, everyone, everything, exactly, except, fail, false, few, fewer, half, hardly, just, lack, least, less, majority, many, may, might, more, most, much, must, n't, need, needs, neglect, neither, never, nobody, none, nor, not, nothing, nowhere, often, omit, only, ought, prevent, refuse, scarcely, several, shall, should, some, somebody, someone, something, sometimes, unless, usually, will, without, would; and do not add any other negative word.",
   "Never write a number word (such as one, two, three, first, second, twice, half or dozen), a time word (such as last, next, now, today, earlier, later, recently, currently, previously, soon, already, yet or past) or a hedge word (such as maybe, perhaps, probably, possibly, likely, apparently, seems, appears, think, believe, guess, almost, nearly or roughly): a program throws away every question that holds one.",
   "Use a capital letter only for the first word of the question and for the word Statement right after the colon. Do not use digits.",
   "Use each placeholder exactly once, written exactly as shown, and do not use any other placeholder: {N}.",
   "{N} stands for the number of the statement being asked about. Write it only as 'Statement {N}' (capital S), exactly once, right after the colon. Ask about Statement {N} itself, never about the other statement, and never start the question with the word Statement."
  ]
 },
 {
  "qid": "qb3bd39321c",
  "brief": "Question template: Of these two statements, does Statement {N} go against common sense?",
  "slots": [
   "N"
  ],
  "rules": [
   "Write 5 questions; question i follows style hint i: (1) keep the verb 'go against' and ask with 'does it'; (2) use a different verb or phrase with exactly the same meaning as 'go against'; (3) ask with 'is it' followed by a phrase that means exactly 'going against common sense'; (4) open with a phrase that says where the statements are (shown, given, listed or presented); (5) make it as short as you can while keeping every condition.",
   "Ask exactly the same thing: keep every condition and every person or thing the question names.",
   "Ask the question directly: do not open with a phrase that asks whether a statement holds, do not ask about an answer or an option, and do not ask for an opinion.",
   "Every question must have this shape: a short opening phrase that refers to the statements the reader sees without counting them (for example 'Of the statements shown' or 'Looking at the pair of statements'), then a colon, then the words Statement {N} right after the colon, then the rest of the question in lowercase letters, which refers back to Statement {N} with 'it' or 'this statement' and asks whether it goes against common sense. Shape example for a different question (never copy it): 'Of the cards on the table: Card {N}, is it red?'",
   "The item's question says 'these two statements'. Never write 'two', and never any other counting word (one, both, either, each): call them the statements shown, given or listed, or the pair of statements.",
   "Keep each of these words, exactly as many times as in the question: 'common'.",
   "Do not use any of these words or phrases: agree with, make sense, all, always, any, anybody, anyone, anything, barely, both, cannot, could, decline, deny, each, either, every, everybody, everyone, everything, exactly, except, fail, false, few, fewer, half, hardly, just, lack, least, less, majority, many, may, might, more, most, much, must, n't, need, needs, neglect, neither, never, nobody, none, nor, not, nothing, nowhere, often, omit, only, ought, prevent, refuse, scarcely, several, shall, should, some, somebody, someone, something, sometimes, unless, usually, will, without, would; and do not add any other negative word.",
   "Never write a number word (such as one, two, three, first, second, twice, half or dozen), a time word (such as last, next, now, today, earlier, later, recently, currently, previously, soon, already, yet or past) or a hedge word (such as maybe, perhaps, probably, possibly, likely, apparently, seems, appears, think, believe, guess, almost, nearly or roughly): a program throws away every question that holds one.",
   "Use a capital letter only for the first word of the question and for the word Statement right after the colon. Do not use digits.",
   "Use each placeholder exactly once, written exactly as shown, and do not use any other placeholder: {N}.",
   "{N} stands for the number of the statement being asked about. Write it only as 'Statement {N}' (capital S), exactly once, right after the colon. Ask about Statement {N} itself, never about the other statement, and never start the question with the word Statement."
  ]
 },
 {
  "qid": "q509718b2ee",
  "brief": "Question: Does this vehicle safety complaint report that at least one person was actually injured?",
  "slots": [],
  "rules": [
   "Write 5 questions; question i follows style hint i: (1) keep the main verb but change the word order; (2) use a different verb or phrase with exactly the same meaning; (3) turn the sentence around so that what is being checked comes first (for example a passive form); (4) open with a short phrase that says where to look, such as 'Based on the text,' or 'Going by the text,'; (5) make it as short as you can while keeping every condition.",
   "Ask exactly the same thing: keep every condition and every person or thing the question names.",
   "Ask the question directly: do not open with a phrase that asks whether a statement holds, do not ask about an answer or an option, and do not ask for an opinion.",
   "The item's question says 'at least one'. Keep that meaning, but write it as 'at least a single' (for example 'at least a single person'): keep the word 'least' exactly once and never write the word 'one' anywhere. Never put 'any', 'some', 'one or more' or a digit in its place: a program throws away every such question.",
   "Keep each of these words, exactly as many times as in the question: 'actually', 'least'.",
   "Do not use any of these words or phrases: all, always, any, anybody, anyone, anything, barely, both, cannot, could, decline, deny, each, either, every, everybody, everyone, everything, exactly, except, fail, false, few, fewer, half, hardly, just, lack, less, majority, many, may, might, more, most, much, must, n't, need, needs, neglect, neither, never, nobody, none, nor, not, nothing, nowhere, often, omit, only, ought, prevent, refuse, scarcely, several, shall, should, some, somebody, someone, something, sometimes, unless, usually, will, without, would; and do not add any other negative word.",
   "Never write a number word (such as one, two, three, first, second, twice, half or dozen), a time word (such as last, next, now, today, earlier, later, recently, currently, previously, soon, already, yet or past) or a hedge word (such as maybe, perhaps, probably, possibly, likely, apparently, seems, appears, think, believe, guess, almost, nearly or roughly): a program throws away every question that holds one.",
   "Use a capital letter only for the first word of the question. Do not use digits."
  ]
 },
 {
  "qid": "q4cdf54a364",
  "brief": "Question template: Of these two statements, does Statement {N} go against common sense?",
  "slots": [
   "N"
  ],
  "rules": [
   "Write 5 questions; question i follows style hint i: (1) make it a little more conversational, in plain everyday words; (2) put a dash or a semicolon after Statement {N} instead of a comma; (3) refer back to Statement {N} with 'this statement' instead of 'it'; (4) open with a phrase that says the reader is comparing or looking at the statements; (5) keep the verb 'go against' and ask with 'does it'.",
   "Ask exactly the same thing: keep every condition and every person or thing the question names.",
   "Ask the question directly: do not open with a phrase that asks whether a statement holds, do not ask about an answer or an option, and do not ask for an opinion.",
   "Every question must have this shape: a short opening phrase that refers to the statements the reader sees without counting them (for example 'Of the statements shown' or 'Looking at the pair of statements'), then a colon, then the words Statement {N} right after the colon, then the rest of the question in lowercase letters, which refers back to Statement {N} with 'it' or 'this statement' and asks whether it goes against common sense. Shape example for a different question (never copy it): 'Of the cards on the table: Card {N}, is it red?'",
   "The item's question says 'these two statements'. Never write 'two', and never any other counting word (one, both, either, each): call them the statements shown, given or listed, or the pair of statements.",
   "Keep each of these words, exactly as many times as in the question: 'common'.",
   "Do not use any of these words or phrases: agree with, make sense, all, always, any, anybody, anyone, anything, barely, both, cannot, could, decline, deny, each, either, every, everybody, everyone, everything, exactly, except, fail, false, few, fewer, half, hardly, just, lack, least, less, majority, many, may, might, more, most, much, must, n't, need, needs, neglect, neither, never, nobody, none, nor, not, nothing, nowhere, often, omit, only, ought, prevent, refuse, scarcely, several, shall, should, some, somebody, someone, something, sometimes, unless, usually, will, without, would; and do not add any other negative word.",
   "Never write a number word (such as one, two, three, first, second, twice, half or dozen), a time word (such as last, next, now, today, earlier, later, recently, currently, previously, soon, already, yet or past) or a hedge word (such as maybe, perhaps, probably, possibly, likely, apparently, seems, appears, think, believe, guess, almost, nearly or roughly): a program throws away every question that holds one.",
   "Use a capital letter only for the first word of the question and for the word Statement right after the colon. Do not use digits.",
   "Use each placeholder exactly once, written exactly as shown, and do not use any other placeholder: {N}.",
   "{N} stands for the number of the statement being asked about. Write it only as 'Statement {N}' (capital S), exactly once, right after the colon. Ask about Statement {N} itself, never about the other statement, and never start the question with the word Statement."
  ]
 }
]
```
