# Haiku authoring task T37b-author_wording-21f09268-008 (family T37b, kind author_wording)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/haiku/author/answers/T37b-author_wording-21f09268-008.json

The answer is one JSON list with exactly 2 objects, one per item below, each carrying that item's qid.

## Instructions

You rewrite questions for a reading test. Each item gives one question, or a question template whose words in capital letters inside curly braces are placeholders, plus rules. For each item write exactly as many new questions as the item's rules ask for. Every new question must ask exactly the same thing as the item's question: a reader who knows the facts must give the same answer to both, in every possible case. Do not answer the question, do not explain, and do not add facts, names or numbers. Reply with JSON only: a list with one object per item, {"qid": <the item's qid>, "questions": [<question 1>, ..., <question k>]}. Every question is one line ending with a question mark, and all of them differ from each other and from the item's question.

## Answer format

[{"qid": "q...", "questions": ["...?", "...?", "...?", "...?", "...?"]}, ...]

## Items (2; one JSON object per line)

```json
[
{"qid": "qcd36d707d6", "brief": "Question: Are the listed duties part of the job of the occupation named above?", "slots": [], "rules": ["Write 5 questions; question i follows style hint i: (1) make it a little more formal; (2) make it a little more conversational, in plain everyday words; (3) put the main condition at the end of the question; (4) use a noun instead of the main verb where that keeps the meaning (for example 'Is there confirmation that ...'); (5) start with a different first word than the question does.", "Ask exactly the same thing: keep every condition, every person or thing the question names, and the same time and source (for example 'last message', 'by the end of this conversation').", "Ask the question directly: do not open with a phrase that asks whether a statement holds, do not ask about an answer or an option, and do not ask for an opinion.", "Do not use any of these words or phrases: all, always, any, anybody, anyone, anything, barely, both, cannot, could, decline, deny, each, either, every, everybody, everyone, everything, exactly, except, fail, false, few, fewer, half, hardly, just, lack, least, less, majority, many, may, might, more, most, much, must, n't, need, needs, neglect, neither, never, nobody, none, nor, not, nothing, nowhere, often, omit, only, ought, prevent, refuse, scarcely, several, shall, should, some, somebody, someone, something, sometimes, unless, usually, will, without, would; and do not add any other negative word.", "Use a capital letter only for the first word of the question. Do not use digits."]},
{"qid": "q660971d6c3", "brief": "Question: In its reply, did the assistant find at least one option that meets everything the customer asked for?", "slots": [], "rules": ["Write 5 questions; question i follows style hint i: (1) keep the main verb but change the word order; (2) use a different verb or phrase with exactly the same meaning; (3) turn the sentence around so that what is being checked comes first (for example a passive form); (4) open with a short phrase that says where to look, such as 'Based on the text,' or 'Going by the text,'; (5) make it as short as you can while keeping every condition.", "Ask exactly the same thing: keep every condition, every person or thing the question names, and the same time and source (for example 'last message', 'by the end of this conversation').", "Ask the question directly: do not open with a phrase that asks whether a statement holds, do not ask about an answer or an option, and do not ask for an opinion.", "Keep each of these words, exactly as many times as in the question: 'everything', 'least'.", "Do not use any of these words or phrases: all, always, any, anybody, anyone, anything, barely, both, cannot, could, decline, deny, each, either, every, everybody, everyone, exactly, except, fail, false, few, fewer, half, hardly, just, lack, less, majority, many, may, might, more, most, much, must, n't, need, needs, neglect, neither, never, nobody, none, nor, not, nothing, nowhere, often, omit, only, ought, prevent, refuse, scarcely, several, shall, should, some, somebody, someone, something, sometimes, unless, usually, will, without, would; and do not add any other negative word.", "Use a capital letter only for the first word of the question. Do not use digits."]}
]
```
