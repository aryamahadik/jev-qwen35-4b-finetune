# T42 G-LEX extraction task T42-glex-read1

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/a57_pool_quarantine/T42/glex/answers/T42-glex-read1.json

Task kind: extract_lex; items: 9; answers expected: 9 (one per item, answer field "choice").

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

Each item gives one question and a list of meanings. Pick the ONE meaning in the list that the question expresses exactly, reading its words. If no meaning in the list fits exactly, answer null. Do not answer the question, and do not judge whether anything is true.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "choice": "<the chosen meaning copied exactly, or null>"}. Valid JSON only; no text before or after the array. Do not open, list or search any other file, and run no other tool.

Answer format: [{"qid": "<qid>", "choice": "<one meaning, copied exactly, or null>"}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "qd0a05d9d76",
  "text": "Which output does running this Python program produce?",
  "choices": [
   "asks which text the program prints, or which uncaught exception it raises",
   "asks whether two functions are the same, differ on ordinary inputs, or differ only on edge inputs",
   "asks which value the variable result holds after the code runs, or which uncaught exception it raises"
  ]
 },
 {
  "qid": "q2527cce768",
  "text": "What value does `result` hold after this Python code has run?",
  "choices": [
   "asks which text the program prints, or which uncaught exception it raises",
   "asks which value the variable result holds after the code runs, or which uncaught exception it raises",
   "asks whether two functions are the same, differ on ordinary inputs, or differ only on edge inputs"
  ]
 },
 {
  "qid": "q2fef743339",
  "text": "After the code finishes, which value is stored in `result`?",
  "choices": [
   "asks which text the program prints, or which uncaught exception it raises",
   "asks which value the variable result holds after the code runs, or which uncaught exception it raises",
   "asks whether two functions are the same, differ on ordinary inputs, or differ only on edge inputs"
  ]
 },
 {
  "qid": "q44ba5cd098",
  "text": "Which option describes how `g` relates to `f` on the inputs their annotations allow?",
  "choices": [
   "asks which text the program prints, or which uncaught exception it raises",
   "asks which value the variable result holds after the code runs, or which uncaught exception it raises",
   "asks whether two functions are the same, differ on ordinary inputs, or differ only on edge inputs"
  ]
 },
 {
  "qid": "qb73cd46262",
  "text": "Compare `f` and `g`: which option describes them?",
  "choices": [
   "asks which text the program prints, or which uncaught exception it raises",
   "asks whether two functions are the same, differ on ordinary inputs, or differ only on edge inputs",
   "asks which value the variable result holds after the code runs, or which uncaught exception it raises"
  ]
 },
 {
  "qid": "q27466cd47d",
  "text": "Run the program in your head: what is shown on the screen?",
  "choices": [
   "asks whether two functions are the same, differ on ordinary inputs, or differ only on edge inputs",
   "asks which value the variable result holds after the code runs, or which uncaught exception it raises",
   "asks which text the program prints, or which uncaught exception it raises"
  ]
 },
 {
  "qid": "q9f96b7751f",
  "text": "What is the final value of `result` in this Python code?",
  "choices": [
   "asks which value the variable result holds after the code runs, or which uncaught exception it raises",
   "asks whether two functions are the same, differ on ordinary inputs, or differ only on edge inputs",
   "asks which text the program prints, or which uncaught exception it raises"
  ]
 },
 {
  "qid": "q778b70955a",
  "text": "How do the functions `f` and `g` relate?",
  "choices": [
   "asks whether two functions are the same, differ on ordinary inputs, or differ only on edge inputs",
   "asks which text the program prints, or which uncaught exception it raises",
   "asks which value the variable result holds after the code runs, or which uncaught exception it raises"
  ]
 },
 {
  "qid": "q628375ff74",
  "text": "What does this Python program print when it runs?",
  "choices": [
   "asks whether two functions are the same, differ on ordinary inputs, or differ only on edge inputs",
   "asks which value the variable result holds after the code runs, or which uncaught exception it raises",
   "asks which text the program prints, or which uncaught exception it raises"
  ]
 }
]
