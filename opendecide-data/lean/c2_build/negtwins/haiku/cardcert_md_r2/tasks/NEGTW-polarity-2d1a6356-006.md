# Haiku card-complement read (md) NEGTW-polarity-2d1a6356-006 (family NEGTW, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/cardcert_md_r2/answers/NEGTW-polarity-2d1a6356-006.json

The answer is one JSON list with exactly 11 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two statements written as yes/no questions, question_a and question_b, about the same piece of text. Reply 'opposite' if for ANY text exactly one of them has the answer yes (never both, never neither); 'same' if a yes to one always goes with a yes to the other; 'unclear' if some texts could make both answers no, or both yes, or the wording is not clear. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (11; one JSON object per line)

```json
[
{"qid": "q556bde2c00", "question_a": "Is it the case that The taxon's class is Bryopsida, Langiophytopsida or Zygnematophyceae?", "question_b": "Is it the case that The taxon's class is any other class?"},
{"qid": "q301a87706b", "question_a": "Is it the case that The organization's type is education or healthcare?", "question_b": "Is it the case that The organization has any other type?"},
{"qid": "q7ad07c3544", "question_a": "Is it the case that The business type is Other catering premises, Restaurant/Cafe/Canteen or Farmers/growers?", "question_b": "Is it the case that The business type is any other type?"},
{"qid": "q1fee8c84df", "question_a": "Is it the case that The place's feature code is PPLA or PPLA2?", "question_b": "Is it the case that The place's feature code is any other code?"},
{"qid": "qfd49f562d8", "question_a": "Is it the case that The rating is 3 or 5?", "question_b": "Is it the case that The rating is any other value?"},
{"qid": "q53cce1f852", "question_a": "Is it the case that The taxon's class is Chilopoda, Stenolaemata or Coelacanthi?", "question_b": "Is it the case that The taxon's class is any other class?"},
{"qid": "q0f90938855", "question_a": "Is it the case that The rating is 0 or 4?", "question_b": "Is it the case that The rating is any other value?"},
{"qid": "q0e57b32706", "question_a": "Is it the case that The business type is Retailers - other, Distributors/Transporters or Restaurant/Cafe/Canteen?", "question_b": "Is it the case that The business type is any other type?"},
{"qid": "q79fd4d71cf", "question_a": "Is it the case that the number of cross-references shown is greater than 2?", "question_b": "Is it the case that the number of cross-references shown is 2 or fewer?"},
{"qid": "q97ae9a4912", "question_a": "Is it the case that Yes if the status is Active or Pipeline?", "question_b": "Is it the case that No if the status is Closed or Dropped?"},
{"qid": "q10f64930be", "question_a": "Is it the case that The taxon's class is Staurozoa, Cubozoa or Symphyla?", "question_b": "Is it the case that The taxon's class is any other class?"}
]
```
