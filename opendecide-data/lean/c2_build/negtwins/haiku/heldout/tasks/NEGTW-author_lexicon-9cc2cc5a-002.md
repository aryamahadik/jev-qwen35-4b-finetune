# Haiku held-out realisation task NEGTW-author_lexicon-9cc2cc5a-002 (family NEGTW, kind author_lexicon)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/heldout/answers/NEGTW-author_lexicon-9cc2cc5a-002.json

The answer is one JSON list with exactly 3 objects, one per item below, each carrying that item's qid.

## Instructions

You write wording options for a reading test about negation. Each item names one slot and gives the meaning the wording must have, plus rules. Write what the rules ask for. Use unusual but natural wordings; do not reuse the most common phrase for the meaning. Never answer a question, never add facts. Reply with JSON only: a list with one object per item, {"qid": <the item's qid>, "frames": [...]} for a frame slot and {"qid": <the item's qid>, "pairs": [...]} for a pair slot. Every string is plain text on one line.

## Answer format

[{"qid": "q...", "frames": ["Is it ... that", "..."]}, ...] for frame items; [{"qid": "q...", "pairs": [{"pos": "verb", "a": {"base": "...", "s3": "...", "past": "...", "pp": "..."}, "b": {...}, "cores_a": ["Does ...?", ...10], "cores_b": ["Does ...?", ...10]}, ...]}, ...] for pair items; for an adjective pair: {"pos": "adj", "a": {"base": "allowed", "adj": "allowed"}, "b": {...}, "cores_a": ["Is ... allowed ...?", ...10], "cores_b": [...10]}

## Items (3; one JSON object per line)

```json
[
{"qid": "q03fc612f10", "brief": "Slot HP6: write 4 verb pairs; in each, word b is the EXACT complement of word a.", "meaning": "for any rule, notice or record exactly one of 'X <a>' and 'X <b>' is true: never both, never neither", "slots": ["a", "b"], "rules": ["pair = {\"pos\": \"verb\", \"a\": {base, s3, past, pp}, \"b\": {base, s3, past, pp}, \"cores_a\": [10 questions 'Does <thing> <a base> <something>?'], \"cores_b\": [10 same form with b]}", "single lower-case words", "questions: one line, no negative word, no every / some / all", "choose rare or specialised words rather than the most common pair"]},
{"qid": "q014477aa8b", "brief": "Slot HP5: write 4 verb pairs; in each, word b is the EXACT complement of word a.", "meaning": "for any rule, notice or record exactly one of 'X <a>' and 'X <b>' is true: never both, never neither", "slots": ["a", "b"], "rules": ["pair = {\"pos\": \"verb\", \"a\": {base, s3, past, pp}, \"b\": {base, s3, past, pp}, \"cores_a\": [10 questions 'Does <thing> <a base> <something>?'], \"cores_b\": [10 same form with b]}", "single lower-case words", "questions: one line, no negative word, no every / some / all", "choose rare or specialised words rather than the most common pair"]},
{"qid": "q7df0bebd0c", "brief": "Slot HP4: write 4 verb pairs; in each, word b is the EXACT complement of word a.", "meaning": "for any rule, notice or record exactly one of 'X <a>' and 'X <b>' is true: never both, never neither", "slots": ["a", "b"], "rules": ["pair = {\"pos\": \"verb\", \"a\": {base, s3, past, pp}, \"b\": {base, s3, past, pp}, \"cores_a\": [10 questions 'Does <thing> <a base> <something>?'], \"cores_b\": [10 same form with b]}", "single lower-case words", "questions: one line, no negative word, no every / some / all", "choose rare or specialised words rather than the most common pair"]}
]
```
