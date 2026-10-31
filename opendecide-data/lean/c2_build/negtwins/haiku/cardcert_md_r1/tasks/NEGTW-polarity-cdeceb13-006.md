# Haiku card-complement read (md) NEGTW-polarity-cdeceb13-006 (family NEGTW, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/cardcert_md_r1/answers/NEGTW-polarity-cdeceb13-006.json

The answer is one JSON list with exactly 11 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two statements written as yes/no questions, question_a and question_b, about the same piece of text. Reply 'opposite' if for ANY text exactly one of them has the answer yes (never both, never neither); 'same' if a yes to one always goes with a yes to the other; 'unclear' if some texts could make both answers no, or both yes, or the wording is not clear. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (11; one JSON object per line)

```json
[
{"qid": "qca66daee45", "question_a": "Is it the case that Yes if the total commitment is 300 million USD or more?", "question_b": "Is it the case that No if the total commitment is below 300 million USD?"},
{"qid": "q5deb949349", "question_a": "Is it the case that The local authority is Broadland, Rochford or Derbyshire Dales?", "question_b": "Is it the case that The local authority is any other?"},
{"qid": "q9090f609d6", "question_a": "Is it the case that The business type is Retailers - supermarkets/hypermarkets, Takeaway/sandwich shop or Restaurant/Cafe/Canteen?", "question_b": "Is it the case that The business type is any other type?"},
{"qid": "qdab85ae655", "question_a": "Is it the case that the last year minus the first year of the Date range is more than 10?", "question_b": "Is it the case that the last year minus the first year of the Date range is 10 or less?"},
{"qid": "qfacc9577d0", "question_a": "Is it the case that The local authority is Hinckley and Bosworth, Wandsworth or Windsor and Maidenhead?", "question_b": "Is it the case that The local authority is any other?"},
{"qid": "q2d421fd436", "question_a": "Is it the case that The local authority is Ceredigion, Hinckley and Bosworth or Runnymede?", "question_b": "Is it the case that The local authority is any other?"},
{"qid": "q6415b09046", "question_a": "Is it the case that The taxon's class is Tritirachiomycetes, Mortierellomycetes or Chytridiomycetes?", "question_b": "Is it the case that The taxon's class is any other class?"},
{"qid": "q3d0d9af0cf", "question_a": "Is it the case that The organization's type is facility or company?", "question_b": "Is it the case that The organization has any other type?"},
{"qid": "qb2ef6f023b", "question_a": "Is it the case that Yes if the open-access status is gold, green, hybrid, bronze or diamond?", "question_b": "Is it the case that No if the open-access status is closed?"},
{"qid": "q9c176a1af1", "question_a": "Is it the case that Yes if 4 or more genre tags are listed?", "question_b": "Is it the case that No if fewer than 4 genre tags are listed?"},
{"qid": "qaa9da66786", "question_a": "Is it the case that The taxon's class is Trebouxiophyceae, Polytrichopsida or Langiophytopsida?", "question_b": "Is it the case that The taxon's class is any other class?"}
]
```
