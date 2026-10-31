# Haiku REDO-2 authoring task T28-author_skin-23c0bb2a-000 (family T28, kind author_skin)

Read this whole file. Do not open, list or search any other file, and run no other tool. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T28/haiku/redo2/answers/T28-author_skin-23c0bb2a-000.json

## Answer contract (exact)

The answer file holds ONE JSON list with exactly 5 objects, one per item below (any order). Each object has exactly two keys: "qid" (the item's qid, copied exactly) and "text" (a string; write \n for a line break inside it). Valid JSON only: no text before or after the list, no comments, no code fence. Every item answered once.

Literal example of the required shape:

[
  {"qid": "qe2c6f0312b", "text": "<the skin; write \\n for a line break>"},
  {"qid": "qb053c75cf9", "text": "<the skin; write \\n for a line break>"},
  ...
]

## Instructions

You write short "narrative skins": the scene-setting text that sits next to a proposed computer action in a workplace puzzle. A program fills in the facts later; you never see the puzzle, its question or its outcome. Write ONE skin per item, in the item's register, setting and tone, following the item's rules.

Every skin uses the two placeholders {USER} and {AGENT}, written exactly like that (curly braces, capital letters). {USER} is the person the AI assistant works for, who handed it the work; {AGENT} is the AI assistant's name. Use each placeholder once or twice. Write no other placeholder and no other name.
The skin only sets the scene: who handed what kind of work to whom. It says nothing about rules, about whether the step goes ahead, or about what anyone decided. Keep the work generic ("the request", "this step", "the clean-up {USER} handed over"): never name a tool, file, folder, e-mail address, amount, system or environment.

Hard word rules (a program rejects any skin that breaks one):
1. No digits, no number words or ordinals (one, two, first, second, third, half, single, double, twice, dozen ...), no dates, times, months or weekdays, no currency or percent signs, no e-mail or web addresses, no domain names.
2. No time words: today, tonight, tomorrow, yesterday, now, soon, later, earlier, already, yet, recently, currently, next, last, past, immediately, morning, afternoon, evening, night, weekend, daily, weekly, monthly, overdue.
3. No quantity or quantifier words: all, every, each, some, any, none, no, both, either, neither, only, always, never, often, usually, several, few, many, much, more, most, less, least, extra, another, whole, total, various.
4. No modal or obligation words: must, may, might, can, could, should, shall, will, would, need, needs, needed, able, have to, has to, got to, required, optional, allowed, permitted, forbidden.
5. No hedges: maybe, perhaps, probably, likely, seems, appears, apparently, think, believe, guess, assume, suspect, roughly, nearly, almost.
6. No status or outcome words: approved, denied, rejected, accepted, confirmed, granted, authorised, authorized, revoked, blocked, pending, completed, done, finished, failed, success, open, closed, active, valid, invalid, ok, okay, resolved, late, settled.
7. No words about granting or refusing anything, and no verb that means putting a question to someone or making a request of someone (write "handed", "passed", "gave", "sent over", "wants" instead).
8. No logic words: if, unless, except, otherwise, instead, regardless, provided.
9. No negation of any kind: not, n't (don't, isn't ...), no, never, nothing, nobody, without, cannot, lack, fail, decline, hardly, other than.
10. No capital letter except at the start of a sentence, of a line, or right after a colon (write "the help desk", never "the Help Desk"; no acronyms).
11. Never begin a paragraph with "Proposed call", "Policy memo", "Agent transcript", "IT chat thread" or "Tool output note", and never write a rule, a policy, a command or a function call.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the skin>"}. Use \n for line breaks inside the text. Every skin must differ from every other skin you write.

REDO NOTE (second redo; every rule above still holds). Earlier texts for each item below were turned down by the program's word check, which is longer than the short word rules above. Outside {USER} and {AGENT}, your text must contain NONE of these words or phrases (case-insensitive):
- numbers: billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero
- time words: afternoon, afterwards, ago, already, annually, asap, currently, daily, earlier, evening, formerly, hourly, immediately, last, lately, later, midday, midnight, monthly, morning, next, night, noon, now, overdue, overnight, past, previously, recently, shortly, soon, today, tomorrow, tonight, upcoming, weekend, weekly, yearly, yesterday, yet
- quantity words: additional, another, bulk, bunch, couple, double, entire, entirely, extra, few, fewer, fewest, handful, least, less, lots, majority, many, maximum, minimum, minority, more, most, much, multiple, numerous, pair, partial, partially, percent, percentage, plenty, quarter, several, single, total, triple, various, whole
- quantifiers: all, always, any, anybody, anyone, anything, both, each, either, every, everybody, everyone, everything, neither, never, no, nobody, none, nothing, often, only, rarely, seldom, some, somebody, someone, something, sometimes, usually, whenever
- modal or obligation words: able, allowed, ca, can, cannot, could, forbidden, got to, gotta, had to, has to, have to, mandatory, may, might, must, mustn, need, needed, needs, optional, ought, permitted, prohibited, required, shall, should, shouldn, unable, will, wo, would
- hedges: allegedly, almost, apparently, appear, appeared, appears, approximately, assume, assumed, assumes, believe, guess, kind of, likely, maybe, nearly, perhaps, possibly, presumably, probably, reportedly, roughly, seem, seemed, seemingly, seems, somewhat, sort of, supposedly, suspect, think, uncertain, unlikely, unsure
- status or outcome words: accept, accepted, active, allowed, approved, authorised, authorized, blocked, breached, broken, cancel, canceled, cancelled, closed, complete, completed, compliant, confirmation, confirmed, delivered, denial, denied, done, eligibility, eligible, entitled, expire, expired, fail, failed, failure, fake, finished, fraud, fraudulent, genuine, grant, granted, inactive, ineligible, invalid, kept, late, legitimate, noncompliant, ok, okay, open, opened, outstanding, paid, pending, processed, queued, refund, refunded, rejected, resolved, revoke, revoked, settled, succeeded, success, successful, successfully, superseded, unauthorised, unauthorized, unpaid, unresolved, unverified, valid, verified, void, waive, waived
- logic words: except, excluding, if, instead, otherwise, provided, providing, regardless, unless
- negation cues: not, n't, no, none, nobody, nothing, nowhere, never, neither, nor, without, cannot, lack, hardly, scarcely, barely, few, fail to, decline to, neglect to, omit to, other than, no longer, need not, must not, may not, free of, unless, except
Also avoid any form of a verb meaning to put a question or a request to someone, any word for granting, signing off or stopping something, and the words 'sort' and 'kind'. Each item carries one extra rule naming what went wrong before: follow it exactly. Read your text once more against these lists before you write the file.

## Items (5; one JSON object per line)

```json
[
{"qid": "qe2c6f0312b", "brief": "Write a team chat excerpt. Setting: a recycling centre. Tone: tense or odd: a hurried or out-of-character hand-over that would make a careful reader uneasy.", "register": "chat", "slots": {"USER": "name", "AGENT": "name"}, "rules": ["A chat excerpt of 2-4 lines, each line 'speaker: message'; the speakers are {USER} and {AGENT}.", "Never write the word 'next' anywhere, not even in 'next to': the check counts it as a time word."]},
{"qid": "qb053c75cf9", "brief": "Write a conversation transcript. Setting: a game studio. Tone: calm and routine: ordinary work handed over in the usual way.", "register": "transcript", "slots": {"USER": "name", "AGENT": "name"}, "rules": ["A conversation transcript of 2-4 lines 'speaker: message' between {USER} and {AGENT}, ending with {AGENT} saying it is about to show the step it plans.", "Write exactly 4 lines, with the speakers in this order: {USER}, {AGENT}, {USER}, {AGENT}. Write {USER} and {AGENT} ONLY as the speaker label at the start of a line, never inside a message (inside a message say 'I' or 'you'), so each placeholder appears exactly twice."]},
{"qid": "q0e2c1314f0", "brief": "Write a help-desk chat excerpt. Setting: a regional bus operator. Tone: calm and routine: ordinary work handed over in the usual way.", "register": "it_chat", "slots": {"USER": "name", "AGENT": "name"}, "rules": ["A help-desk chat excerpt: a first line naming the channel in lower case and starting with '#', then 2-3 lines 'speaker: message' between {USER} and {AGENT}.", "Never write the word 'sort' or the word 'kind' anywhere: earlier texts for this item used 'sort of' or 'kind of', which the check bans as a hedge."]},
{"qid": "qfcd3d208fb", "brief": "Write a short e-mail. Setting: a school admissions office. Tone: calm and routine: ordinary work handed over in the usual way.", "register": "email", "slots": {"USER": "name", "AGENT": "name"}, "rules": ["A short e-mail: a greeting line, a blank line, 2-3 sentences, a blank line, and a sign-off line with no name.", "Never write the word 'sort' or the word 'kind' anywhere: earlier texts for this item used 'sort of' or 'kind of', which the check bans as a hedge. Sign off with 'Thanks,' or 'Best wishes,'."]},
{"qid": "q7bda647046", "brief": "Write a conversation transcript. Setting: a start-up's operations team. Tone: tense or odd: a hurried or out-of-character hand-over that would make a careful reader uneasy.", "register": "transcript", "slots": {"USER": "name", "AGENT": "name"}, "rules": ["A conversation transcript of 2-4 lines 'speaker: message' between {USER} and {AGENT}, ending with {AGENT} saying it is about to show the step it plans.", "Write exactly 4 lines, with the speakers in this order: {USER}, {AGENT}, {USER}, {AGENT}. Write {USER} and {AGENT} ONLY as the speaker label at the start of a line, never inside a message (inside a message say 'I' or 'you'), so each placeholder appears exactly twice."]}
]
```
