# Haiku held-out realisation task NEGTW-author_lexicon-9cc2cc5a-000 (family NEGTW, kind author_lexicon)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/heldout/answers/NEGTW-author_lexicon-9cc2cc5a-000.json

The answer is one JSON list with exactly 8 objects, one per item below, each carrying that item's qid.

## Instructions

You write wording options for a reading test about negation. Each item names one slot and gives the meaning the wording must have, plus rules. Write what the rules ask for. Use unusual but natural wordings; do not reuse the most common phrase for the meaning. Never answer a question, never add facts. Reply with JSON only: a list with one object per item, {"qid": <the item's qid>, "frames": [...]} for a frame slot and {"qid": <the item's qid>, "pairs": [...]} for a pair slot. Every string is plain text on one line.

## Answer format

[{"qid": "q...", "frames": ["Is it ... that", "..."]}, ...] for frame items; [{"qid": "q...", "pairs": [{"pos": "verb", "a": {"base": "...", "s3": "...", "past": "...", "pp": "..."}, "b": {...}, "cores_a": ["Does ...?", ...10], "cores_b": ["Does ...?", ...10]}, ...]}, ...] for pair items; for an adjective pair: {"pos": "adj", "a": {"base": "allowed", "adj": "allowed"}, "b": {...}, "cores_a": ["Is ... allowed ...?", ...10], "cores_b": [...10]}

## Items (8; one JSON object per line)

```json
[
{"qid": "q305cec327f", "brief": "Slot HP2: write 4 verb pairs; in each, word b is the EXACT complement of word a.", "meaning": "for any rule, notice or record exactly one of 'X <a>' and 'X <b>' is true: never both, never neither", "slots": ["a", "b"], "rules": ["pair = {\"pos\": \"verb\", \"a\": {base, s3, past, pp}, \"b\": {base, s3, past, pp}, \"cores_a\": [10 questions 'Does <thing> <a base> <something>?'], \"cores_b\": [10 same form with b]}", "single lower-case words", "questions: one line, no negative word, no every / some / all", "choose rare or specialised words rather than the most common pair"]},
{"qid": "q4f6b985688", "brief": "Slot HN1: write 4 question openers ending with the word 'that' that ask whether the clause which follows is FALSE.", "meaning": "asks whether what follows is false (not true), and nothing else", "slots": ["HN1"], "rules": ["start with Is, Would, Does, Could or Can", "3 to 8 words, no comma, no question mark", "exactly one negative idea (false, untrue, incorrect, wrong, mistaken, inaccurate, or 'not the case')", "no contraction", "not 'Is it false that' or 'Is it not the case that'"]},
{"qid": "q923a265e7d", "brief": "Slot HN4: write 4 question openers ending with the word 'that' that ask whether the clause which follows is FALSE.", "meaning": "asks whether what follows is false (not true), and nothing else", "slots": ["HN4"], "rules": ["start with Is, Would, Does, Could or Can", "3 to 8 words, no comma, no question mark", "exactly one negative idea (false, untrue, incorrect, wrong, mistaken, inaccurate, or 'not the case')", "no contraction", "not 'Is it false that' or 'Is it not the case that'"]},
{"qid": "q4d879187f4", "brief": "Slot HN2: write 4 question openers ending with the word 'that' that ask whether the clause which follows is FALSE.", "meaning": "asks whether what follows is false (not true), and nothing else", "slots": ["HN2"], "rules": ["start with Is, Would, Does, Could or Can", "3 to 8 words, no comma, no question mark", "exactly one negative idea (false, untrue, incorrect, wrong, mistaken, inaccurate, or 'not the case')", "no contraction", "not 'Is it false that' or 'Is it not the case that'"]},
{"qid": "qdb5eb03584", "brief": "Slot HP9: write 4 adjective or participle pairs; in each, word b is the EXACT complement of word a.", "meaning": "for any rule, notice or record exactly one of 'X <a>' and 'X <b>' is true: never both, never neither", "slots": ["a", "b"], "rules": ["pair = {\"pos\": \"adj\", \"a\": {base, adj}, \"b\": {base, adj}, \"cores_a\": [10 questions 'Is <thing> <a> <rest>?'], \"cores_b\": [10 same form with b]}", "single lower-case words", "questions: one line, no negative word, no every / some / all", "choose rare or specialised words rather than the most common pair"]},
{"qid": "qb3f1551a7a", "brief": "Slot HN3: write 4 question openers ending with the word 'that' that ask whether the clause which follows is FALSE.", "meaning": "asks whether what follows is false (not true), and nothing else", "slots": ["HN3"], "rules": ["start with Is, Would, Does, Could or Can", "3 to 8 words, no comma, no question mark", "exactly one negative idea (false, untrue, incorrect, wrong, mistaken, inaccurate, or 'not the case')", "no contraction", "not 'Is it false that' or 'Is it not the case that'"]},
{"qid": "q6549671a6c", "brief": "Slot HF1: write 4 question openers ending with the word 'that' that ask whether the clause which follows is TRUE.", "meaning": "asks whether what follows is true, and nothing else", "slots": ["HF1"], "rules": ["start with Is, Would, Does, Could or Can", "3 to 8 words, no comma, no question mark", "no negative word of any kind", "not 'Is it true that', 'Is it correct that', 'Is it the case that', 'Is it so that', 'Is it accurate that'"]},
{"qid": "qbaf9200e7e", "brief": "Slot HP8: write 4 adjective or participle pairs; in each, word b is the EXACT complement of word a.", "meaning": "for any rule, notice or record exactly one of 'X <a>' and 'X <b>' is true: never both, never neither", "slots": ["a", "b"], "rules": ["pair = {\"pos\": \"adj\", \"a\": {base, adj}, \"b\": {base, adj}, \"cores_a\": [10 questions 'Is <thing> <a> <rest>?'], \"cores_b\": [10 same form with b]}", "single lower-case words", "questions: one line, no negative word, no every / some / all", "choose rare or specialised words rather than the most common pair"]}
]
```
