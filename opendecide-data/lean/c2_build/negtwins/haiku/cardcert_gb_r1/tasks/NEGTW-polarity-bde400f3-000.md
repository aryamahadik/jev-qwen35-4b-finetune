# Haiku card-complement read (gb) NEGTW-polarity-bde400f3-000 (family NEGTW, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/cardcert_gb_r1/answers/NEGTW-polarity-bde400f3-000.json

The answer is one JSON list with exactly 5 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two statements written as yes/no questions, question_a and question_b, about the same piece of text. Reply 'opposite' if for ANY text exactly one of them has the answer yes (never both, never neither); 'same' if a yes to one always goes with a yes to the other; 'unclear' if some texts could make both answers no, or both yes, or the wording is not clear. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (5; one JSON object per line)

```json
[
{"qid": "q4614f221d2", "question_a": "Is it the case that Pick yes when the release describes a programme, service, grant, scholarship, vaccine booking, nomination process, free event or similar offer that an ordinary reader can take up?", "question_b": "Is it the case that Pick no when the release only reports news, results, decisions, road or weather conditions, or an investment in one named company, with nothing an ordinary reader can take up?"},
{"qid": "q899e9acb3f", "question_a": "Is it the case that The story reports a finished event or a settled fact with a clear outcome that someone may want to look up again later?", "question_b": "Is it the case that The story is about something still open, or it is a short-lived update with no lasting use as a record?"},
{"qid": "q3f907c2e6a", "question_a": "Is it the case that Pick yes when the main new contribution is a computer, mathematical or theoretical model, a software framework, or a data-analysis method that the authors built or proposed?", "question_b": "Is it the case that Pick no when the main new contribution is new lab, field or clinical results, a new living model such as a lab animal, or a comparison of models or methods that already existed?"},
{"qid": "qe7929a2464", "question_a": "Is it the case that Yes means the ingredient list names meat, poultry, fish or shellfish (such as beef, chicken, goat, tuna or shrimp), even if it is one choice among several?", "question_b": "Is it the case that No means none of these is named as an ingredient, and a stock or sauce on its own does not count as meat?"},
{"qid": "q8b214b82a4", "question_a": "Is it the case that Yes if the text says the volunteer will personally spend time with, serve, supervise or teach people the organisation helps, such as residents, children, families or clients?", "question_b": "Is it the case that No if the volunteer's tasks are mainly objects, paperwork, one-off events, office work or donations, or if the text does not say the volunteer meets the people served?"}
]
```
