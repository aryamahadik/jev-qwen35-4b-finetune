# T20 G-LEX extraction task T20-extract_lex-404d65bb-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T20/haiku/extract/answers/T20-extract_lex-404d65bb-001.json

Task kind: extract_lex; items: 41; answers expected: 41 (one per item, answer field "choice").

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

Each item gives one question and a list of meanings. The question is about an incident whose level is set by a card of rules on a scale of four levels, SEV1 (the most severe) to SEV4 (the least severe), as of a check time. Pick the ONE meaning in the list that the question expresses exactly. Read the exact words: 'at a level or more severe' is not the same as 'exactly at a level'; 'at the check time' is not the same as 'at any time'; a question that uses the word not is not the same as one that uses fail to. Do not answer the question itself.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "choice": "<the chosen meaning, copied exactly>"}. Valid JSON only; no text before or after the array. Do not open, list or search any other file, and run no other tool.

Answer format: [{"qid": "<qid>", "choice": "<one meaning, copied exactly>"}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "q1c26221fbd",
  "text": "Using the card, what level is incident INC-4821 at the check time?",
  "choices": [
   "asks for the incident's starting level from the table, before any step is applied",
   "asks which of the four levels the incident is at, at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time"
  ]
 },
 {
  "qid": "q08b01e6ed0",
  "text": "Would incident INC-4821 count as SEV2 or more severe as of the check time, according to the card's rules?",
  "choices": [
   "asks which of the four levels the incident is at, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time"
  ]
 },
 {
  "qid": "q6102d1c6ba",
  "text": "As a newcomer starting in on-call work, is incident INC-4821 at SEV3 or less severe as of the check time?",
  "choices": [
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident misses a level that it was expected or required to get to"
  ]
 },
 {
  "qid": "q1aa7931275",
  "text": "Learning the on-call rotation, which severity level applies to incident INC-4821 at the check time under the card?",
  "choices": [
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time"
  ]
 },
 {
  "qid": "q041f4c1333",
  "text": "Could you walk me through the card and say which level incident INC-4821 lands on at the check time?",
  "choices": [
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied"
  ]
 },
 {
  "qid": "q0aec00b876",
  "text": "Do the card's rules give incident INC-4821 a level that is SEV2 or more severe at the check time?",
  "choices": [
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time"
  ]
 },
 {
  "qid": "qed255157f3",
  "text": "Could a newcomer confirm that incident INC-4821 does not reach SEV2 at the check time?",
  "choices": [
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time"
  ]
 },
 {
  "qid": "qc2348df08f",
  "text": "For a newcomer on the rota, is it the case that incident INC-4821 fails to reach SEV2 at the check time?",
  "choices": [
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time"
  ]
 },
 {
  "qid": "q30f1a1a70d",
  "text": "Does incident INC-4821 not reach SEV2 at the check time?",
  "choices": [
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks for the incident's starting level from the table, before any step is applied"
  ]
 },
 {
  "qid": "q81a90f33cf",
  "text": "As a new on-call engineer, could you tell me what level incident INC-4821 holds as of the check time under the card's rules?",
  "choices": [
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a less severe level at the check time"
  ]
 },
 {
  "qid": "q2d4d601731",
  "text": "Could a newcomer confirm that incident INC-4821 fails to reach SEV2 at the check time?",
  "choices": [
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time"
  ]
 },
 {
  "qid": "qeee8b5faa3",
  "text": "Briefly, under the card's rules, which severity is incident INC-4821 at the check time?",
  "choices": [
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time"
  ]
 },
 {
  "qid": "q5a3eeeb8cf",
  "text": "New on-call here, so what severity does the card's rule set give incident INC-4821 at the check time?",
  "choices": [
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a less severe level at the check time"
  ]
 },
 {
  "qid": "qcbae448bb5",
  "text": "Using the card's rules, what severity level must be recorded for incident INC-4821 at the check time?",
  "choices": [
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time"
  ]
 },
 {
  "qid": "qe9a20c4e08",
  "text": "Quick question from a newcomer to on-call, what level does incident INC-4821 get as of the check time under the card?",
  "choices": [
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is strictly more severe than the named level at the check time"
  ]
 },
 {
  "qid": "qbc88ed0b54",
  "text": "Simply put, does incident INC-4821 reach SEV2 as of the check time, per the card's rules?",
  "choices": [
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at the named level or a less severe level at the check time"
  ]
 },
 {
  "qid": "q4f6e6e781f",
  "text": "So does incident INC-4821 reach SEV2 at the check time, going by the card?",
  "choices": [
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time"
  ]
 },
 {
  "qid": "qb3e4973e65",
  "text": "Would the record confirm that incident INC-4821 fails to reach SEV2 at the check time?",
  "choices": [
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time"
  ]
 },
 {
  "qid": "qddba76a838",
  "text": "Being new to on-call, would you say incident INC-4821 doesn't reach SEV2 at the check time?",
  "choices": [
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident misses a level that it was expected or required to get to"
  ]
 },
 {
  "qid": "qa97dd8320d",
  "text": "Under the card's rules, does incident INC-4821 reach SEV2 as of the check time?",
  "choices": [
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks for the incident's starting level from the table, before any step is applied"
  ]
 },
 {
  "qid": "q532cae9b33",
  "text": "Is incident INC-4821 a case that doesn't reach SEV2 at the check time?",
  "choices": [
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a less severe level at the check time"
  ]
 },
 {
  "qid": "qaeb9f32caa",
  "text": "Going by the card, does incident INC-4821 reach SEV2 at the check time?",
  "choices": [
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks which of the four levels the incident is at, at the check time"
  ]
 },
 {
  "qid": "qeddd152db8",
  "text": "What severity level applies to incident INC-4821 at the check time, by the card's rules?",
  "choices": [
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time"
  ]
 },
 {
  "qid": "q21fb0b8e17",
  "text": "Under the card, will incident INC-4821 be SEV2 or more severe as of the check time?",
  "choices": [
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident misses a level that it was expected or required to get to"
  ]
 },
 {
  "qid": "q4f8d124627",
  "text": "Is incident INC-4821 at SEV3 or less severe at the check time, for a new engineer learning the rota?",
  "choices": [
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time"
  ]
 },
 {
  "qid": "q7087e71906",
  "text": "Honestly, what level would you put on incident INC-4821 as of the check time, using the card?",
  "choices": [
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time"
  ]
 },
 {
  "qid": "q46c0a54017",
  "text": "Is it true that incident INC-4821 fails to reach SEV2 at the check time?",
  "choices": [
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks for the incident's starting level from the table, before any step is applied"
  ]
 },
 {
  "qid": "qd4636aac0f",
  "text": "Is it true that incident INC-4821 does not reach SEV2 at the check time?",
  "choices": [
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks which of the four levels the incident is at, at the check time"
  ]
 },
 {
  "qid": "qcea7edc631",
  "text": "Which level holds for incident INC-4821 at the check time, going by the card?",
  "choices": [
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time"
  ]
 },
 {
  "qid": "qc3778282a8",
  "text": "Would the rules count incident INC-4821 as SEV2 or more severe at the check time?",
  "choices": [
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks which of the four levels the incident is at, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time"
  ]
 },
 {
  "qid": "qd4cf416c07",
  "text": "As a new on-call engineer, do you find that incident INC-4821 fails to reach SEV2 at the check time?",
  "choices": [
   "asks which of the four levels the incident is at, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time"
  ]
 },
 {
  "qid": "qb682811e4e",
  "text": "Do the rules on the card show that incident INC-4821 reaches SEV2 at the check time?",
  "choices": [
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time"
  ]
 },
 {
  "qid": "q172b6b8eaf",
  "text": "New on-call engineer here: does incident INC-4821 fail to reach SEV2 at the check time?",
  "choices": [
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied"
  ]
 },
 {
  "qid": "qf14c439261",
  "text": "Gonna need the card's read on incident INC-4821, so which severity is it at the check time?",
  "choices": [
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a more severe level at the check time"
  ]
 },
 {
  "qid": "qa339215067",
  "text": "Under the card's rules, which level does incident INC-4821 hold at the check time?",
  "choices": [
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks which of the four levels the incident is at, at the check time"
  ]
 },
 {
  "qid": "q1f5d486a24",
  "text": "Honestly, is the card's verdict that incident INC-4821 reaches SEV2 at the check time?",
  "choices": [
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks which of the four levels the incident is at, at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time"
  ]
 },
 {
  "qid": "q7878ea1e0b",
  "text": "Does the record of incident INC-4821 show that it doesn't reach SEV2 as of the check time?",
  "choices": [
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks for the incident's starting level from the table, before any step is applied"
  ]
 },
 {
  "qid": "qbb9d1dc7e3",
  "text": "Does the state of incident INC-4821 as of the check time mean it fails to reach SEV2?",
  "choices": [
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks which of the four levels the incident is at, at the check time"
  ]
 },
 {
  "qid": "q7ff091cabb",
  "text": "Under the card's rules, does incident INC-4821 reach SEV2 at the check time?",
  "choices": [
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time"
  ]
 },
 {
  "qid": "qf675f8572a",
  "text": "Is it true that incident INC-4821 is at SEV3 or less severe at the check time?",
  "choices": [
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks for the incident's starting level from the table, before any step is applied"
  ]
 },
 {
  "qid": "q78c51e894b",
  "text": "Does the card say that incident INC-4821 reaches SEV2 as of the check time?",
  "choices": [
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident gets to the named level at any time, including after the check time"
  ]
 }
]
