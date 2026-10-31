# Haiku card-complement read NEGTW-polarity-45c80243-000 (family NEGTW, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/cardcert_r2/answers/NEGTW-polarity-45c80243-000.json

The answer is one JSON list with exactly 5 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two statements written as yes/no questions, question_a and question_b, about the same piece of text. Reply 'opposite' if for ANY text exactly one of them has the answer yes (never both, never neither); 'same' if a yes to one always goes with a yes to the other; 'unclear' if some texts could make both answers no, or both yes, or the wording is not clear. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (5; one JSON object per line)

```json
[
{"qid": "q3e61d4201d", "question_a": "Is it the case that it is not the case that the text clearly asks or tells the reader to take a step, such as applying, giving feedback, attending an upcoming event, or avoiding a place, road or water?", "question_b": "Is it the case that the text clearly asks or tells the reader to take a step, such as applying, giving feedback, attending an upcoming event, or avoiding a place, road or water?"},
{"qid": "q5b2b4a987e", "question_a": "Is it the case that it is not the case that the text says visitors must register, pre-register, sign up, or book a time slot before attending?", "question_b": "Is it the case that the text says visitors must register, pre-register, sign up, or book a time slot before attending?"},
{"qid": "q4fa08e9db1", "question_a": "Is it the case that it is not the case that the text says the work is done outdoors, for example in a park, on a field or track, in a garden or farm, or at a curbside or on the street?", "question_b": "Is it the case that the text says the work is done outdoors, for example in a park, on a field or track, in a garden or farm, or at a curbside or on the street?"},
{"qid": "qeb302259fa", "question_a": "Is it the case that it is not the case that the study tests or samples living people (such as patients or volunteers) or live animals, including tissue, blood or recordings taken from them?", "question_b": "Is it the case that the study tests or samples living people (such as patients or volunteers) or live animals, including tissue, blood or recordings taken from them?"},
{"qid": "q58204dcb2e", "question_a": "Is it the case that it is not the case that the text sets a minimum age of 18 or older for volunteers?", "question_b": "Is it the case that the text sets a minimum age of 18 or older for volunteers?"}
]
```
