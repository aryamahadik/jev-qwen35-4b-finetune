# Haiku lexicon drafting task NEGTW-author_lexicon-a5f7c77a-009 (family NEGTW, kind author_lexicon)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/draft/answers/NEGTW-author_lexicon-a5f7c77a-009.json

The answer is one JSON list with exactly 3 objects, one per item below, each carrying that item's qid.

## Instructions

You write wording options for a reading test about negation. Each item has a brief, the meaning the wording must have, and rules. For each item write exactly what its rules ask for and nothing else. Never answer a question, never add facts. Reply with JSON only: a list with one object per item, {"qid": <the item's qid>, "frames": [...]} for a frame item and {"qid": <the item's qid>, "pairs": [...]} for a pair item, as the item's rules describe. Every string is plain text on one line.

## Answer format

[{"qid": "q...", "frames": ["Is it ... that", "..."]}, ...] for frame items; [{"qid": "q...", "pairs": [{"pos": "verb", "a": {"base": "...", "s3": "...", "past": "...", "pp": "..."}, "b": {...}, "cores_a": ["Does ...?", ...10], "cores_b": ["Does ...?", ...10]}, ...]}, ...] for pair items; for an adjective pair: {"pos": "adj", "a": {"base": "allowed", "adj": "allowed"}, "b": {...}, "cores_a": ["Is ... allowed ...?", ...10], "cores_b": [...10]}

## Items (3; one JSON object per line)

```json
[
{"qid": "qa9f3655883", "brief": "Write 1 verb pair in which word a is exactly 'offer' and word b is its EXACT complement.", "meaning": "for any rule, notice, report or record, exactly one of 'X <a>' and 'X <b>' is true: never both, never neither, no middle case", "slots": ["a", "b"], "rules": ["pair = {\"pos\": \"verb\", \"a\": {base, s3, past, pp}, \"b\": {base, s3, past, pp}, \"cores_a\": [10 questions], \"cores_b\": [10 questions]}", "single lower-case verbs; cores: 'Does <the thing> <base verb> <something>?', one line, no negative word", "if no exact complement verb exists for a, write the closest one whose complement is exact for records and notices, and make cores_a use a", "give exactly 1 pair in the item's 'pairs' list"]},
{"qid": "qd444419720", "brief": "Write 2 adjective or participle pairs in the field 'requirement and option' (item 29). In each pair, word b must be the EXACT complement of word a.", "meaning": "for any rule, notice, report or record, exactly one of 'X <a>' and 'X <b>' is true: never both, never neither, no middle case", "slots": ["a", "b"], "rules": ["each pair is {\"pos\": \"adj\", \"a\": {base, adj}, \"b\": {base, adj}, \"cores_a\": [10 questions], \"cores_b\": [10 questions]}", "a and b are single lower-case words (adjectives or participles); base and adj are the same word", "cores_a: 10 different yes/no questions of the form 'Is <the thing> <a> <rest>?' where the word a is the first word after the thing", "cores_b: 10 different questions of the same form with word b in that place", "each question starts with Is or Are, one line, ends with ?, contains no negative word and no word like every, some or all", "give exactly 2 pairs in the item's 'pairs' list", "the two pairs must not share a word"]},
{"qid": "qe92091ad06", "brief": "Write 1 verb pair in which word a is exactly 'involve' and word b is its EXACT complement.", "meaning": "for any rule, notice, report or record, exactly one of 'X <a>' and 'X <b>' is true: never both, never neither, no middle case", "slots": ["a", "b"], "rules": ["pair = {\"pos\": \"verb\", \"a\": {base, s3, past, pp}, \"b\": {base, s3, past, pp}, \"cores_a\": [10 questions], \"cores_b\": [10 questions]}", "single lower-case verbs; cores: 'Does <the thing> <base verb> <something>?', one line, no negative word", "if no exact complement verb exists for a, write the closest one whose complement is exact for records and notices, and make cores_a use a", "give exactly 1 pair in the item's 'pairs' list"]}
]
```
