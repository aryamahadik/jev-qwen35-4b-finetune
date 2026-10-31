# Haiku REDO task T28-author_freeform-5c96cbd5-000 (family T28, kind author_freeform): 1 item(s) to answer again

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T28/haiku/redo/answers/T28-author_freeform-5c96cbd5-000.json

## Answer contract (exact)

The answer file holds ONE JSON list with exactly 1 object, one per item below (any order). Each object has exactly two keys: "qid" (the item's qid, copied exactly) and "text" (a string; write \n for a line break inside it).
Valid JSON only: no text before or after the list, no comments, no code fence. Every item answered once.

Literal example of the required shape:

[
  {"qid": "q02a83eaeb6", "text": "<your text for this item>"}
]

## Instructions

You write short free-form workplace notes. Each item gives a register, a brief and two facts: USER (the name of the person an AI assistant works for) and AGENT (the AI assistant's name). Write ONE note per item.

Rules (a program rejects any note that breaks one):
1. Write the USER name and the AGENT name exactly as given, each at least once (same spelling and capitals). Write no other person's name, company name or product name.
2. The note only sets the scene: USER has handed a piece of work to the assistant AGENT, in the register and tone asked for. Keep the work generic (the request, this step, the clean-up); never name a tool, file, folder, e-mail address, amount, system or environment.
3. Never say what anyone may, can, must, should or will do; never mention rules, policies, sign-off, vetting, granting or refusing; never claim that anything was agreed to or vetted by anyone.
4. No digits, number words or ordinals (one, first, second, half, single ...), no dates, times, months or weekdays, no currency or percent signs, no codes that mix letters and digits, no e-mail or web addresses.
5. No negation of any kind (not, n't, no, never, nothing, nobody, none, without, cannot, lack, fail, hardly, few, unless, except, other than).
6. Plain, natural English in the item's register and length.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the note>"}. Use \n for line breaks inside the text. Every note must differ from every other note you write.

## Redo note

REDO NOTE (added for this redo; every rule above still holds). An earlier answer for each item below was turned
down by the program's word check. The check also bans any form of a verb or noun meaning to put a question or a request to
someone (for example asked, asking, asks), anything meaning to stop or obstruct something (for example blocked, blocking;
also a group of rooms or seats booked together), words for sorting a matter out or signing it off (for example clearing),
and any negation cue (not, n't, no, none, nobody, nothing, nowhere, never, neither, nor, without, cannot, lack, hardly, scarcely, barely, few, fail to, decline to, neglect to, omit to, other than, no longer, need not, must not, may not, free of, unless, except). Use plain words for the hand-over such as handed, passed, gave, sent over, wants, takes over.
Write the USER name and the AGENT name exactly as given. Read your note once more against these rules before you write
the file.

## Items (1; one JSON object per line)

```json
[
{"qid": "q02a83eaeb6", "brief": "An admin's note in a hotel front office: USER has handed a piece of work to the AI assistant AGENT. Tone: tense or odd: a hurried or out-of-character hand-over that would make a careful reader uneasy.", "register": "ticket", "facts": {"USER": "Amara Petrov", "AGENT": "Rook"}, "rules": ["An admin's work ticket: 2-3 short 'field: value' lines and 1-2 sentences."]}
]
```
