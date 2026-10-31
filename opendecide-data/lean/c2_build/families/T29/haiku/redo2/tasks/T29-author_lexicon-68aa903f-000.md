# T29 redo2 authoring task T29-author_lexicon-68aa903f-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/redo2/answers/T29-author_lexicon-68aa903f-000.json

This file is self-contained: the instructions, the answer contract and the items are all below.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 3 objects: one per item below, each item answered once, in any order.
- Each object has exactly two keys: "qid" and "forms". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits, 11 characters in all). The qids of this task: q3953f5a251, qa31ac708e5, q9b0881cd16.
- "forms": a JSON array of exactly 10 strings, all different.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal example of the shape (the qid shown is the first real one; replace the angle brackets with your own text):
[{"qid": "q3953f5a251", "forms": ["<first>", "<second>", ...]}, ...]

Task kind: author_lexicon; items: 3; outputs expected: 30.

You are writing short pieces of text for a synthetic training dataset about software agents that follow
written company policies. Everything you write is either a reusable template (a program later fills each {SLOT}
placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy
text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write CONFIRMATION-BANK FORMS: short lines that a program quotes as something the user typed earlier in a
conversation with the agent, in the frame: Earlier in this conversation the user wrote: «___». {ACT} stands for the id
of a tool call (a snake_case action name) and {TGT} for the id of a record. Each item states the exact meaning, a
style, its own word rules and the forms already taken; write the number of NEW forms it asks for.

Hard rules (a form that breaks one is thrown away):
1. Keep every placeholder the item lists exactly once, spelled exactly so with its curly braces; add no other
   placeholder; never put "a" or "an" directly before a placeholder.
2. The meaning must be unmistakable to any careful reader, including at the edge case the item names.
3. Never repeat a form from the item's "taken" list (those already exist), not even with other capitals, spacing or
   punctuation. All forms in your answer are distinct.
4. No digits and none of these number words: billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero.
5. None of these time words, in any sense: afternoon, afterwards, ago, already, annually, asap, currently, daily, earlier, evening, formerly, hourly, immediately, last, lately, later, midday, midnight, monthly, morning, next, night, noon, now, overdue, overnight, past, previously, recently, shortly, soon, today, tomorrow, tonight, upcoming, weekend, weekly, yearly, yesterday, yet.
6. No hedges: allegedly, almost, apparently, appear, appeared, appears, approximately, assume, assumed, assumes, believe, guess, likely, maybe, nearly, perhaps, possibly, presumably, probably, reportedly, roughly, seem, seemed, seemingly, seems, somewhat, supposedly, suspect, think, uncertain, unlikely, unsure. No double quote characters.
7. A capital letter only on the first word (and the word I); no names of people, teams, products or places.
8. Follow the item's own "rules" list exactly. No form adds a condition, an exception or a second idea.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "forms": ["<form 1>", "<form 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q3953f5a251",
  "brief": {
   "how_many": 10,
   "style": "about half questions on what the call would change or how far along it is, and half neutral remarks that mention the call",
   "frame": "Earlier in this conversation the user wrote: «___»",
   "taken": [
    "Does {ACT} on {TGT} change its status?",
    "Does {ACT} touch {TGT} in any way?",
    "Has the {ACT} call on {TGT} finished?",
    "Has {ACT} on {TGT} completed?",
    "How far along is the {ACT} call on {TGT}?",
    "How much of the {ACT} call on {TGT} has been done?",
    "I see the {ACT} call is set against {TGT}.",
    "Is the {ACT} call on {TGT} complete?",
    "Is the {ACT} call on {TGT} in progress?",
    "Is {ACT} on {TGT} underway?",
    "Is {TGT} the record that {ACT} modifies?",
    "Our log shows {ACT} with {TGT} as its target.",
    "That is the {ACT} call that targets {TGT}.",
    "The plan has {ACT} aimed at {TGT}.",
    "The {ACT} call and {TGT} came up in the review.",
    "The {ACT} call on {TGT} is among the listed options.",
    "There is a pending {ACT} call that involves {TGT}.",
    "What does {ACT} actually change for {TGT}?",
    "What happens to {TGT} after {ACT} is called?",
    "What progress has the {ACT} call on {TGT} made?",
    "What stage is the {ACT} call on {TGT} at?",
    "What would the {ACT} call do to {TGT}?",
    "What would {ACT} change on {TGT}?",
    "Where does the {ACT} call on {TGT} stand?",
    "Which fields of {TGT} would {ACT} alter?",
    "Would {ACT} on {TGT} delete the current contents?",
    "Would {ACT} on {TGT} overwrite anything?",
    "{ACT} on {TGT} is listed in the plan.",
    "{TGT} is the record the {ACT} call uses."
   ]
  },
  "meaning": "the user only asks about, or refers to, {ACT} on {TGT} without agreeing to it and without telling the agent to run it: no word of agreement or instruction (yes, sure, okay, fine, do it, run it, confirmed, agreed, please continue)",
  "slots": {
   "ACT": "the id of the tool call, a snake_case action name",
   "TGT": "the id of the record"
  },
  "rules": [
   "10 new forms",
   "{ACT} and {TGT} each exactly once",
   "each form only refers to {ACT} on {TGT} or puts a question about it; it never agrees to the call and never tells the agent to run it",
   "no imperative verb, and none of these words or phrases: yes, yeah, yep, sure, okay, ok, fine, confirm, confirmed, agree, agreed, please, continue, do it, run it",
   "a question ends with a question mark; a remark ends with a full stop"
  ]
 },
 {
  "qid": "qa31ac708e5",
  "brief": {
   "how_many": 10,
   "style": "complete sentences, polite and plain",
   "frame": "Earlier in this conversation the user wrote: «___»",
   "taken": [
    "I direct you to run {ACT} on {TGT} at this point.",
    "I want you to run {ACT} on {TGT}.",
    "It is requested that you perform {ACT} on {TGT}.",
    "Kindly execute {ACT} on {TGT}.",
    "Please carry out {ACT} on the record {TGT}.",
    "Please run {ACT} on {TGT}.",
    "Run {ACT} against {TGT} in full.",
    "You are instructed to run {ACT} on {TGT}.",
    "do {ACT} on {TGT} rn",
    "go {ACT} on {TGT} thx",
    "hey run {ACT} on {TGT} for me",
    "just fire {ACT} at {TGT}",
    "just run {ACT} on {TGT}, thx",
    "k run {ACT} on {TGT}",
    "lets do {ACT} on {TGT}",
    "pls kick off {ACT} for {TGT}",
    "run {ACT} on {TGT} and thats all",
    "run {ACT} on {TGT} lol",
    "run {ACT} on {TGT} pls",
    "send {ACT} through on {TGT} pls",
    "yea do {ACT} for {TGT}",
    "yeah just run {ACT} on {TGT}",
    "yep, run {ACT} on {TGT}",
    "{ACT} on {TGT}, go run it"
   ]
  },
  "meaning": "the user clearly and unconditionally tells the agent to run {ACT} on {TGT}: an affirmative instruction for exactly that call, with no question, no condition (if, unless, once, when, as long as), no negation and no hedge",
  "slots": {
   "ACT": "the id of the tool call, a snake_case action name",
   "TGT": "the id of the record"
  },
  "rules": [
   "10 new forms",
   "{ACT} and {TGT} each exactly once",
   "each form tells the agent, with no condition, to run exactly {ACT} on {TGT}",
   "instruction verbs: use ONLY run, execute, carry out, perform, do, kick off, start, launch, fire, trigger, apply, push through or send through; you may add please, pls, kindly, just, for me, thanks or thx",
   "no question mark and no negation of any kind (not, n't, no, never, without, ...)",
   "never use these condition words, in any sense: if, unless, once, when, whenever, provided, providing, after, as long as, only if, except, otherwise"
  ]
 },
 {
  "qid": "q9b0881cd16",
  "brief": {
   "how_many": 10,
   "style": "short and casual, as typed quickly in a chat",
   "frame": "Earlier in this conversation the user wrote: «___»",
   "taken": [
    "I direct you to run {ACT} on {TGT} at this point.",
    "I want you to run {ACT} on {TGT}.",
    "It is requested that you perform {ACT} on {TGT}.",
    "Kindly execute {ACT} on {TGT}.",
    "Please carry out {ACT} on the record {TGT}.",
    "Please run {ACT} on {TGT}.",
    "Run {ACT} against {TGT} in full.",
    "You are instructed to run {ACT} on {TGT}.",
    "do {ACT} on {TGT} rn",
    "go {ACT} on {TGT} thx",
    "hey run {ACT} on {TGT} for me",
    "just fire {ACT} at {TGT}",
    "just run {ACT} on {TGT}, thx",
    "k run {ACT} on {TGT}",
    "lets do {ACT} on {TGT}",
    "pls kick off {ACT} for {TGT}",
    "run {ACT} on {TGT} and thats all",
    "run {ACT} on {TGT} lol",
    "run {ACT} on {TGT} pls",
    "send {ACT} through on {TGT} pls",
    "yea do {ACT} for {TGT}",
    "yeah just run {ACT} on {TGT}",
    "yep, run {ACT} on {TGT}",
    "{ACT} on {TGT}, go run it"
   ]
  },
  "meaning": "the user clearly and unconditionally tells the agent to run {ACT} on {TGT}: an affirmative instruction for exactly that call, with no question, no condition (if, unless, once, when, as long as), no negation and no hedge",
  "slots": {
   "ACT": "the id of the tool call, a snake_case action name",
   "TGT": "the id of the record"
  },
  "rules": [
   "10 new forms",
   "{ACT} and {TGT} each exactly once",
   "each form tells the agent, with no condition, to run exactly {ACT} on {TGT}",
   "instruction verbs: use ONLY run, execute, carry out, perform, do, kick off, start, launch, fire, trigger, apply, push through or send through; you may add please, pls, kindly, just, for me, thanks or thx",
   "no question mark and no negation of any kind (not, n't, no, never, without, ...)",
   "never use these condition words, in any sense: if, unless, once, when, whenever, provided, providing, after, as long as, only if, except, otherwise"
  ]
 }
]
