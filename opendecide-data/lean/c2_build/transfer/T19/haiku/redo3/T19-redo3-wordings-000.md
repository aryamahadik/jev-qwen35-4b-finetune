# Haiku REDO-3 task T19-redo3-wordings-000 (family T19, kind author_wording): 2 item(s), 3 candidates each

Read this whole file. It is the only file you may open: do not open, list, search or write any other file or folder. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T19/haiku/redo3/answers/T19-redo3-wordings-000.json

## Answer contract (exact)

The answer file holds ONE JSON array with exactly 2 object(s), one per item below, every qid exactly once (any order). Each object has exactly two keys: "qid" (the item's qid, copied exactly) and "texts" (a list of exactly 3 different strings: 3 alternative candidates for that item, each complete on its own and each following every rule below; inside a string write \n for a line break and \" for a double quote).
Valid JSON only: no text before or after the array, no comments, no code fence, no other keys.

Literal example of the required shape:

[
  {"qid": "qcfb7efd9ec", "texts": ["<text A>", "<text B>", "<text C>"]},
  ...
]

How the candidates are used: a program checks each candidate against the rules below in the order you wrote them and keeps the first one that meets every check; the others are thrown away. So every candidate must follow every rule, and the candidates of one item must be clearly different from each other.

## Instructions

You write questions for a reading test. Every test item shows the records of one site: a site profile, a checklist of controls (routine checks such as a fire drill), an evidence log with the date of each control's latest evidence, and the audit date. A card on the item defines the terms: a control applies to the site or not; an applying control passes or fails on the audit date (or its result is unknown); the site is compliant when every applying control passes, non-compliant when at least one applying control fails, and otherwise its compliance cannot be determined; the first gap is the earliest applying control in the checklist order that fails. You see none of the test items. Each item below gives the exact meaning a question must have and its construction rules. Write 3 alternative questions per item, each with exactly that meaning, in your own words.

General rules (a program rejects any question that breaks one):
1. One sentence ending with "?", 8-30 words, plain English.
2. Write the placeholder {SITE} exactly once (a program replaces it with the site's name, such as "Larch Street depot"); no other placeholder and no other name. Never write "a" or "an" directly before {SITE}.
3. Ask about the site against its checklist as a whole on the audit date: the question contains the word "checklist" and the words "audit date".
4. No digits, number words or ordinals (one, first, second, last ...): say "earliest", never "first". No dates, no other time words (now, today, currently, soon, already, yet, recently ...), no hedges (maybe, probably, likely, seem ...), no capital letter except the first letter of the sentence.
5. Follow the item's negation rule exactly. Negation cues are: not, n't, no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, fail to, lack, refuse to, decline to, neglect to, omit to, deny, unless, except, other than, few, hardly.
6. Ask for the outcome itself: never ask whether some answer is correct, and never list the answer options.
7. Follow the item's key-phrase rule, and give each of the item's questions the opening or frame the item names for it (candidate 1, candidate 2, candidate 3).

Answer: follow the answer contract at the top of this file (3 questions per item, each complete on its own and each following every rule). Use \n for line breaks inside a text. Every question must differ clearly from every other question you write, also from the other questions of the same item (not one word swapped).

## Redo note

REDO NOTE (added for this redo; every general rule above still holds). Earlier questions for these items were thrown away for one of two reasons:
A. Near-synonyms. A later reader matches each question to one meaning from a closed list in which three meanings differ only in their wording: "is out of compliance with", "is not compliant with" and "fails to meet". A question that used another phrase for the same idea (for example "falls short of", "lacks compliance with", "non-compliant", "does not meet", "fails to conform to", or a question that opens with "Isn't") was matched to a different meaning and thrown away. So each item names a KEY PHRASE: write it word for word (only the verb may follow the grammar, as in "fails to meet" after the site's name), and use no other phrase about compliance in that question.
B. Exact repeats. Questions that repeated another question word for word were thrown away. Each item names its own opening or frame for each candidate: follow it exactly, so that no two questions are the same.
Before you write the file, check each question: the key phrase is there, word for word; the opening or frame of that candidate is there; {SITE} exactly once; the words "checklist" and "audit date" are there; no number word and never "first"; the item's negation rule holds; one sentence ending with "?".

## Items (2; one JSON object per line)

```json
[
{"qid": "qcfb7efd9ec", "brief": "A yes/no question that is the exact opposite of 'is the site compliant with its checklist on the audit date?': yes exactly when the site is not compliant.", "slots": {"SITE": "the site's name (exactly once)"}, "rules": ["Key phrase, word for word: 'not compliant with' (only the verb may follow the grammar). Exactly ONE negation: this 'not', written as its own word right before the rest of the key phrase. Never a contraction (isn't, doesn't) and never a question that opens with a negative (Isn't, Is it not, Doesn't). No other phrase about compliance: never 'meet', 'satisfy', 'conform', 'out of compliance', 'non-compliant', 'fail' or 'lack'.", "Shape (fixed): the opening, then 'is {SITE} not compliant with its checklist on the audit date?' Use the verb 'is'; add nothing between 'checklist' and 'on the audit date' and nothing after 'audit date'.", "Candidate 1: open with 'Using the card's definitions,'.", "Candidate 2: open with 'With the records in front of you,'.", "Candidate 3: open with 'Measured against the card,'."]},
{"qid": "q15d7bf8ad4", "brief": "A yes/no question that is the exact opposite of 'is the site compliant with its checklist on the audit date?': yes exactly when the site is not compliant.", "slots": {"SITE": "the site's name (exactly once)"}, "rules": ["Key phrase, word for word: 'not compliant with' (only the verb may follow the grammar). Exactly ONE negation: this 'not', written as its own word right before the rest of the key phrase. Never a contraction (isn't, doesn't) and never a question that opens with a negative (Isn't, Is it not, Doesn't). No other phrase about compliance: never 'meet', 'satisfy', 'conform', 'out of compliance', 'non-compliant', 'fail' or 'lack'.", "Shape (fixed): the opening, then 'is {SITE} not compliant with its checklist on the audit date?' Use the verb 'is'; add nothing between 'checklist' and 'on the audit date' and nothing after 'audit date'.", "Candidate 1: open with 'After checking the evidence log,'.", "Candidate 2: open with 'Working from the profile and the evidence log,'.", "Candidate 3: open with 'In the view of a careful reviewer,'."]}
]
```
