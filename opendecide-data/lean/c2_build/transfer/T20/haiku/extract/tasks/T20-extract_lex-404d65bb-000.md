# T20 G-LEX extraction task T20-extract_lex-404d65bb-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T20/haiku/extract/answers/T20-extract_lex-404d65bb-000.json

Task kind: extract_lex; items: 45; answers expected: 45 (one per item, answer field "choice").

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

Each item gives one question and a list of meanings. The question is about an incident whose level is set by a card of rules on a scale of four levels, SEV1 (the most severe) to SEV4 (the least severe), as of a check time. Pick the ONE meaning in the list that the question expresses exactly. Read the exact words: 'at a level or more severe' is not the same as 'exactly at a level'; 'at the check time' is not the same as 'at any time'; a question that uses the word not is not the same as one that uses fail to. Do not answer the question itself.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "choice": "<the chosen meaning, copied exactly>"}. Valid JSON only; no text before or after the array. Do not open, list or search any other file, and run no other tool.

Answer format: [{"qid": "<qid>", "choice": "<one meaning, copied exactly>"}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "qcc41033311",
  "text": "Does incident INC-4821 reach SEV2 at the check time?",
  "choices": [
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied"
  ]
 },
 {
  "qid": "qb07c4255e2",
  "text": "For a newcomer on the rota, is it the case that incident INC-4821 does not reach SEV2 at the check time?",
  "choices": [
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time"
  ]
 },
 {
  "qid": "q25cb15f1fc",
  "text": "Does incident INC-4821 sit at SEV3 or less severe at the check time?",
  "choices": [
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks which of the four levels the incident is at, at the check time"
  ]
 },
 {
  "qid": "q32226d7ca9",
  "text": "Where does the card put incident INC-4821 as far as level goes at the check time?",
  "choices": [
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time"
  ]
 },
 {
  "qid": "q3c1e54ce07",
  "text": "Is incident INC-4821, as a new engineer would read it, a case that fails to reach SEV2 at the check time?",
  "choices": [
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time"
  ]
 },
 {
  "qid": "qe1788c5da4",
  "text": "Is incident INC-4821 a case that fails to reach SEV2 at the check time?",
  "choices": [
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time"
  ]
 },
 {
  "qid": "qf8f179ea58",
  "text": "Does applying the card's rules to incident INC-4821 produce a level that reaches SEV2 at the check time?",
  "choices": [
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time"
  ]
 },
 {
  "qid": "q32175b2698",
  "text": "Is incident INC-4821 at SEV3 or less severe at the check time?",
  "choices": [
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time"
  ]
 },
 {
  "qid": "qf33f5fa591",
  "text": "Fast question, would the card count incident INC-4821 as SEV2 or more severe as of the check time?",
  "choices": [
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks which of the four levels the incident is at, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time"
  ]
 },
 {
  "qid": "qa058c7ea05",
  "text": "So going by the card, what level has incident INC-4821 landed on at the check time?",
  "choices": [
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time"
  ]
 },
 {
  "qid": "q3dd90c6432",
  "text": "Which severity level does the card's rule set assign to incident INC-4821 as of the check time?",
  "choices": [
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time"
  ]
 },
 {
  "qid": "q57ba6b1728",
  "text": "Looking at the card, what is the level of incident INC-4821 as of the check time?",
  "choices": [
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time"
  ]
 },
 {
  "qid": "q2a22e90884",
  "text": "Does incident INC-4821 fail to reach SEV2 at the check time?",
  "choices": [
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time"
  ]
 },
 {
  "qid": "qf8e3735a2a",
  "text": "New on-call engineer here: is incident INC-4821 at SEV3 or less severe at the check time?",
  "choices": [
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks which of the four levels the incident is at, at the check time"
  ]
 },
 {
  "qid": "q1909d4e077",
  "text": "Which level does incident INC-4821 fall under at the check time, going by the card's rules?",
  "choices": [
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks which of the four levels the incident is at, at the check time"
  ]
 },
 {
  "qid": "q4c0c67ab14",
  "text": "Is incident INC-4821 classed as SEV2 or more severe at the check time, as set out in the card's rules?",
  "choices": [
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time"
  ]
 },
 {
  "qid": "qd60bbbc137",
  "text": "Is it fair to say incident INC-4821 reaches SEV2 as of the check time under the card?",
  "choices": [
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time"
  ]
 },
 {
  "qid": "qcd455b8a11",
  "text": "Is it true, for a new on-call engineer, that incident INC-4821 sits at SEV3 or less severe at the check time?",
  "choices": [
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time"
  ]
 },
 {
  "qid": "q3c429c9dcb",
  "text": "For a newcomer, would the rules count incident INC-4821 as being at SEV3 or less severe at the check time?",
  "choices": [
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident misses a level that it was expected or required to get to"
  ]
 },
 {
  "qid": "q220ed7046e",
  "text": "The card's rules are new to me, so which level does incident INC-4821 fall into at the check time?",
  "choices": [
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time"
  ]
 },
 {
  "qid": "q8648b01a1b",
  "text": "Looking at the card, does incident INC-4821 reach SEV2 as of the check time?",
  "choices": [
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks for the incident's starting level from the table, before any step is applied"
  ]
 },
 {
  "qid": "q21006140ce",
  "text": "Under the card's rules, at what level does incident INC-4821 sit as of the check time?",
  "choices": [
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time"
  ]
 },
 {
  "qid": "q27bf463665",
  "text": "Would the record place incident INC-4821 at SEV3 or less severe as of the check time?",
  "choices": [
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time"
  ]
 },
 {
  "qid": "q71ea5b8986",
  "text": "New on-call engineer here: does incident INC-4821 not reach SEV2 at the check time?",
  "choices": [
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time"
  ]
 },
 {
  "qid": "q4bc252e850",
  "text": "Reading the card as a rookie, which severity level does incident INC-4821 land on at the check time?",
  "choices": [
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time"
  ]
 },
 {
  "qid": "q06ff74be18",
  "text": "Per the card, which severity does incident INC-4821 get as of the check time?",
  "choices": [
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to"
  ]
 },
 {
  "qid": "q5cf828415b",
  "text": "Concerning incident INC-4821, does it not reach SEV2 as of the check time?",
  "choices": [
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time"
  ]
 },
 {
  "qid": "q20d9449918",
  "text": "Concerning incident INC-4821, does it fail to reach SEV2 as of the check time?",
  "choices": [
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time"
  ]
 },
 {
  "qid": "q4cc1525bbf",
  "text": "In short, as of the check time, which severity sits on incident INC-4821 under the card?",
  "choices": [
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time"
  ]
 },
 {
  "qid": "qca093efecb",
  "text": "Can you tell me which level incident INC-4821 has at the check time, going by the card?",
  "choices": [
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time"
  ]
 },
 {
  "qid": "q118dd4a786",
  "text": "Having applied the card's rules, can we say that incident INC-4821 reaches SEV2 as of the check time?",
  "choices": [
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time"
  ]
 },
 {
  "qid": "q0011312f28",
  "text": "Being new to on-call, would you say incident INC-4821 fails to reach SEV2 at the check time?",
  "choices": [
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied"
  ]
 },
 {
  "qid": "qef15f9ba9c",
  "text": "Is incident INC-4821, as a new engineer would see it, a case that does not reach SEV2 at the check time?",
  "choices": [
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident misses a level that it was expected or required to get to"
  ]
 },
 {
  "qid": "qe6b69ae361",
  "text": "Which level, as set out by the card's rules, does incident INC-4821 hold as of the check time?",
  "choices": [
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time"
  ]
 },
 {
  "qid": "qa39471d014",
  "text": "Is the level of incident INC-4821 at SEV3 or less severe as of the check time?",
  "choices": [
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a less severe level at the check time"
  ]
 },
 {
  "qid": "q86758f696d",
  "text": "Would the card put incident INC-4821 at a level of SEV2 or more severe at the check time?",
  "choices": [
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks which of the four levels the incident is at, at the check time"
  ]
 },
 {
  "qid": "q3b7357db02",
  "text": "Does the card say that incident INC-4821 reaches SEV2 at the check time?",
  "choices": [
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time"
  ]
 },
 {
  "qid": "qecddcef44f",
  "text": "Being new to on-call, would it be right to say incident INC-4821 is at SEV3 or less severe at the check time?",
  "choices": [
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks which of the four levels the incident is at, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at the named level or a less severe level at the check time"
  ]
 },
 {
  "qid": "qe7e910a65d",
  "text": "Would the record confirm that incident INC-4821 does not reach SEV2 at the check time?",
  "choices": [
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time"
  ]
 },
 {
  "qid": "q65975d9eda",
  "text": "Does the card's rule set, applied to incident INC-4821, make it reach SEV2 as of the check time?",
  "choices": [
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks which of the four levels the incident is at, at the check time"
  ]
 },
 {
  "qid": "q43a58a6cd6",
  "text": "As a new on-call engineer, do you find that incident INC-4821 does not reach SEV2 at the check time?",
  "choices": [
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks which of the four levels the incident is at, at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time"
  ]
 },
 {
  "qid": "q328cd9a98d",
  "text": "What level do the card's rules say incident INC-4821 has as of the check time?",
  "choices": [
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time"
  ]
 },
 {
  "qid": "q97b4dc4b1b",
  "text": "On the card, which level goes with incident INC-4821 at the check time?",
  "choices": [
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks for the incident's starting level from the table, before any step is applied",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident misses a level that it was expected or required to get to"
  ]
 },
 {
  "qid": "qb2c093b164",
  "text": "Having applied the card's rules to the record of incident INC-4821, what severity results at the check time?",
  "choices": [
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks for the incident's starting level from the table, before any step is applied"
  ]
 },
 {
  "qid": "qc84c076339",
  "text": "Going by the rules on the card, what severity does incident INC-4821 have at the check time?",
  "choices": [
   "asks whether the incident is at the named level or a less severe level at the check time",
   "asks which of the four levels the incident is at, at the check time",
   "asks whether the incident is at exactly the named level, neither more nor less severe, at the check time",
   "asks whether the incident is strictly more severe than the named level at the check time",
   "asks whether the incident misses a level that it was expected or required to get to",
   "asks whether the incident is at the named level or a more severe level at the check time",
   "asks, with the phrase fail to or fails to, whether the incident fails to get to the named level (or a more severe one) at the check time",
   "asks whether the incident gets to the named level at any time, including after the check time",
   "asks, with the word not, whether the incident does not get to the named level (or a more severe one) at the check time",
   "asks for the incident's starting level from the table, before any step is applied"
  ]
 }
]
