# Haiku authoring task T01-author_lexicon-71f346cd-000 (family T01, kind author_lexicon)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T01/haiku/author/answers/T01-author_lexicon-71f346cd-000.json

The answer is one JSON list with exactly 24 objects, one per item below, each carrying that item's qid.

## Instructions

You write short comparison phrases about a sum of money. A program prints each phrase on a card as "If that total is <your phrase>, ..." or "if its deposit total or its withdrawal total is <your phrase>", with {X} replaced by an amount such as $5,000.00. Each item gives the exact meaning. Write ONE phrase per item, in your own words.

Rules:
1. Contains the placeholder {X} exactly once, written exactly like that; no other number, amount or placeholder.
2. Reads as correct English right after "is ", lower case (unless it starts with {X}), no final period, 1-7 words besides {X}.
3. Makes it plain whether an amount exactly equal to {X} counts: for "strictly greater" say "more than" or "greater than" (strictly may be added); for "greater or equal" say it with "at least", "or more", "or above", "or greater" or "equal to or more than".
4. Never use the words over, exceeds, exceeding, excess, beyond, under, below, within, up to, between, and, not, no; "above" only inside "or above".

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the phrase>"}. Every phrase must differ from every other phrase you write and from the example in the item.

## Answer format

[{"qid": "q...", "text": "..."}, ...]

## Items (24; one JSON object per line)

```json
[
{"qid": "q72466bd671", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the total is strictly greater than {X}: a total exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "qa0cd03bd87", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the total is greater than or equal to {X}: a total exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "q29449218b9", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the total is strictly greater than {X}: a total exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "q1b5e8b9b4f", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the total is strictly greater than {X}: a total exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Put {X} at the start."]},
{"qid": "qaa7e1a174b", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the total is strictly greater than {X}: a total exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "q48f4dd97c0", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the total is greater than or equal to {X}: a total exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "qa5f8675e65", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the total is greater than or equal to {X}: a total exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "qd0e43e2437", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the total is strictly greater than {X}: a total exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "qbdadb890f7", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the total is greater than or equal to {X}: a total exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Put {X} at the end."]},
{"qid": "q6bbaa188e2", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the total is strictly greater than {X}: a total exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Put {X} at the end."]},
{"qid": "qf58810c026", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the total is greater than or equal to {X}: a total exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Put {X} at the start."]},
{"qid": "qa0b95aca53", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the total is greater than or equal to {X}: a total exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Put {X} at the end."]},
{"qid": "q0dad3911e5", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the total is strictly greater than {X}: a total exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "qbfe45743aa", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the total is greater than or equal to {X}: a total exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Put {X} at the end."]},
{"qid": "q9e3ffe9e5c", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the total is greater than or equal to {X}: a total exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "qd819dea43f", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the total is strictly greater than {X}: a total exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Put {X} at the end."]},
{"qid": "qd974b19648", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the total is greater than or equal to {X}: a total exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "q00e619a6e6", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the total is greater than or equal to {X}: a total exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Put {X} at the start."]},
{"qid": "qb036820d55", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the total is greater than or equal to {X}: a total exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "q42a8855fda", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the total is strictly greater than {X}: a total exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "qcd8178760e", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the total is strictly greater than {X}: a total exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Put {X} at the start."]},
{"qid": "qc93949e64f", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the total is strictly greater than {X}: a total exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Put {X} at the start."]},
{"qid": "q0c48a94d11", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the total is strictly greater than {X}: a total exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Put {X} at the end."]},
{"qid": "qdf15e8098e", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the total is greater than or equal to {X}: a total exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Put {X} at the start."]}
]
```
