# Haiku authoring task T28-author_lexicon-43afe466-000 (family T28, kind author_lexicon)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T28/haiku/author/answers/T28-author_lexicon-43afe466-000.json

The answer is one JSON list with exactly 32 objects, one per item below, each carrying that item's qid.

## Instructions

You write short comparison phrases about a sum of money. A program prints each phrase on a card as "the amount is <your phrase>", with {X} replaced by a sum such as $50.00. Each item gives the exact meaning. Write ONE phrase per item, in your own words.

Rules:
1. Contains the placeholder {X} exactly once, written exactly like that; no other number, amount or placeholder.
2. Reads as correct English right after "the amount is ", lower case, no final period, 1-7 words besides {X}.
3. Makes plain whether an amount exactly equal to {X} counts. Never use the words "under", "over", "up to", "within", "between" or "and".

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the phrase>"}. Every phrase must differ from every other phrase you write, and from the example in the item.

## Answer format

[{"qid": "q...", "text": "..."}, ...]

## Items (32; one JSON object per line)

```json
[
{"qid": "q045b339d83", "brief": "Write a phrase with this meaning. Example (do not copy it): \"{X} or less\".", "meaning": "the amount is less than or equal to {X}: an amount exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "q657e74fdc8", "brief": "Write a phrase with this meaning. Example (do not copy it): \"less than {X}\".", "meaning": "the amount is strictly less than {X}: an amount exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Put {X} at the end."]},
{"qid": "qcf785790c6", "brief": "Write a phrase with this meaning. Example (do not copy it): \"{X} or less\".", "meaning": "the amount is less than or equal to {X}: an amount exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "q4ab5077c13", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the amount is strictly greater than {X}: an amount exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Put {X} at the end."]},
{"qid": "qde1c29886b", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the amount is greater than or equal to {X}: an amount exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "q546557514f", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the amount is strictly greater than {X}: an amount exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "q1e4ab792e8", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the amount is greater than or equal to {X}: an amount exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "q8df629bd3f", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the amount is strictly greater than {X}: an amount exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "q86648b61b6", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the amount is strictly greater than {X}: an amount exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Put {X} at the start."]},
{"qid": "q7654d3ea7b", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the amount is greater than or equal to {X}: an amount exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Put {X} at the end."]},
{"qid": "qc7d088c85c", "brief": "Write a phrase with this meaning. Example (do not copy it): \"less than {X}\".", "meaning": "the amount is strictly less than {X}: an amount exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Put {X} at the start."]},
{"qid": "qff5900a8d0", "brief": "Write a phrase with this meaning. Example (do not copy it): \"{X} or less\".", "meaning": "the amount is less than or equal to {X}: an amount exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Put {X} at the start."]},
{"qid": "q17873d5b58", "brief": "Write a phrase with this meaning. Example (do not copy it): \"less than {X}\".", "meaning": "the amount is strictly less than {X}: an amount exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "qf1c11d8054", "brief": "Write a phrase with this meaning. Example (do not copy it): \"{X} or less\".", "meaning": "the amount is less than or equal to {X}: an amount exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "q1304f3184d", "brief": "Write a phrase with this meaning. Example (do not copy it): \"less than {X}\".", "meaning": "the amount is strictly less than {X}: an amount exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Put {X} at the end."]},
{"qid": "q58ceb6bb6b", "brief": "Write a phrase with this meaning. Example (do not copy it): \"{X} or less\".", "meaning": "the amount is less than or equal to {X}: an amount exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Put {X} at the end."]},
{"qid": "q8dd5a4583c", "brief": "Write a phrase with this meaning. Example (do not copy it): \"{X} or less\".", "meaning": "the amount is less than or equal to {X}: an amount exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "q66c57a1da8", "brief": "Write a phrase with this meaning. Example (do not copy it): \"less than {X}\".", "meaning": "the amount is strictly less than {X}: an amount exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "qe0c19c4de3", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the amount is strictly greater than {X}: an amount exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "q74d473e4df", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the amount is strictly greater than {X}: an amount exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Put {X} at the end."]},
{"qid": "q3b88f84162", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the amount is strictly greater than {X}: an amount exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Put {X} at the start."]},
{"qid": "q8040e154b3", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the amount is greater than or equal to {X}: an amount exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "qa20614e379", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the amount is greater than or equal to {X}: an amount exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Put {X} at the start."]},
{"qid": "q77dde5f08a", "brief": "Write a phrase with this meaning. Example (do not copy it): \"{X} or less\".", "meaning": "the amount is less than or equal to {X}: an amount exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Put {X} at the end."]},
{"qid": "q1cbb4b07ed", "brief": "Write a phrase with this meaning. Example (do not copy it): \"more than {X}\".", "meaning": "the amount is strictly greater than {X}: an amount exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "qd41c9c525f", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the amount is greater than or equal to {X}: an amount exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Put {X} at the end."]},
{"qid": "qbbc5b6192f", "brief": "Write a phrase with this meaning. Example (do not copy it): \"less than {X}\".", "meaning": "the amount is strictly less than {X}: an amount exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "q7b96ae51cd", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the amount is greater than or equal to {X}: an amount exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]},
{"qid": "qffac3ef854", "brief": "Write a phrase with this meaning. Example (do not copy it): \"less than {X}\".", "meaning": "the amount is strictly less than {X}: an amount exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Put {X} at the start."]},
{"qid": "q394218c6a3", "brief": "Write a phrase with this meaning. Example (do not copy it): \"{X} or less\".", "meaning": "the amount is less than or equal to {X}: an amount exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Put {X} at the start."]},
{"qid": "q2ed6252a30", "brief": "Write a phrase with this meaning. Example (do not copy it): \"at least {X}\".", "meaning": "the amount is greater than or equal to {X}: an amount exactly equal to {X} counts", "slots": {"X": "cents"}, "rules": ["Put {X} at the start."]},
{"qid": "qb5eb8b74b4", "brief": "Write a phrase with this meaning. Example (do not copy it): \"less than {X}\".", "meaning": "the amount is strictly less than {X}: an amount exactly equal to {X} does not count", "slots": {"X": "cents"}, "rules": ["Place {X} wherever it reads best."]}
]
```
