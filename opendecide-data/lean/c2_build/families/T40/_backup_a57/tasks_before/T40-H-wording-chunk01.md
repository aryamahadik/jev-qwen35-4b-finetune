# Task T40-H-wording-chunk01

You write questions for a dataset about checking an AI agent's tool calls and file edits. Each item gives the meaning of one question and the number of negations it must contain. Write plain English questions that ask exactly that, each one a single sentence ending with a question mark, without numbers or names, with the stated number of negation words (not) and no other negative wording (no contractions, no 'fail', 'lack', 'without', 'never'). Make the questions of one item clearly different from each other. Read this file only.

Write a JSON array to the answer file, one object per item, in item order: {"qid": "<the item qid>", "texts": ["<text 1>", "<text 2>", ...]}. Write nothing else in the file.

Answer file: answers/T40-H-wording-chunk01.json

## Items
- qid `T40-H-wording-yb_call-0`: Write 6 different questions. Meaning: it asks whether the agent should make a tool call at once for the request. Negation words (not) required: 0.
- qid `T40-H-wording-yb_call-1`: Write 6 different questions. Meaning: it asks whether the agent should make a tool call at once for the request. Negation words (not) required: 0.
- qid `T40-H-wording-yb_call-2`: Write 6 different questions. Meaning: it asks whether the agent should make a tool call at once for the request. Negation words (not) required: 0.
- qid `T40-H-wording-yb_bdneg-0`: Write 6 different questions. Meaning: it asks, with an outer 'is it not the case that' or 'is it not true that' and a second 'not', whether the agent should call a tool at once. Negation words (not) required: 2.
- qid `T40-H-wording-yb_bdneg-1`: Write 6 different questions. Meaning: it asks, with an outer 'is it not the case that' or 'is it not true that' and a second 'not', whether the agent should call a tool at once. Negation words (not) required: 2.
- qid `T40-H-wording-yb_bdneg-2`: Write 6 different questions. Meaning: it asks, with an outer 'is it not the case that' or 'is it not true that' and a second 'not', whether the agent should call a tool at once. Negation words (not) required: 2.
- qid `T40-H-wording-yb_hold-0`: Write 6 different questions. Meaning: it asks whether the agent should hold off on a tool call (reply to the user instead). Negation words (not) required: 0.
- qid `T40-H-wording-yb_hold-1`: Write 6 different questions. Meaning: it asks whether the agent should hold off on a tool call (reply to the user instead). Negation words (not) required: 0.
- qid `T40-H-wording-yb_hold-2`: Write 6 different questions. Meaning: it asks whether the agent should hold off on a tool call (reply to the user instead). Negation words (not) required: 0.
- qid `T40-H-wording-yb_notcall-0`: Write 6 different questions. Meaning: it asks whether the agent should not call a tool at once (one 'not'). Negation words (not) required: 1.
- qid `T40-H-wording-yb_notcall-1`: Write 6 different questions. Meaning: it asks whether the agent should not call a tool at once (one 'not'). Negation words (not) required: 1.
- qid `T40-H-wording-yb_notcall-2`: Write 6 different questions. Meaning: it asks whether the agent should not call a tool at once (one 'not'). Negation words (not) required: 1.
