# T35 meaning check T35-extract_lex-93f085f3-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/haiku/extract/answers/T35-extract_lex-93f085f3-002.json

Items: 50.

You are checking short sentences for a synthetic dataset about web crawlers. Each item gives a
text (a question, or a rule sentence from a card of rules for reading a robots.txt file; a sample value may be filled
in) and a list of choices, each one possible meaning. Pick the ONE choice that states exactly what the text means:
not a broader, narrower or softer meaning. If no choice fits exactly, answer "none of these".

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "meaning": "<the chosen choice, copied exactly, or none of these>"}, ...]
Copy each qid exactly.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q38cee7b3fc",
  "text": "Do these rules keep the crawler away from this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "qf859058e84",
  "text": "Under the rules shown, is the crawler cleared to fetch this URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "qf21457c247",
  "text": "Under these rules, which line is the decider on whether the crawler gets to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "qf680737f38",
  "text": "By these rules, is INV-20419 allowed to fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q2589b24fbd",
  "text": "Do these rules not permit INV-20419 to fetch the requested URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "q0861e470a4",
  "text": "Under these rules, isn't the crawler simply not blocked from fetching this URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "qeb2e4236bc",
  "text": "Which line of the robots.txt, under these rules, governs the question of whether INV-20419 gets to fetch the requested URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "q02e449945b",
  "text": "Aren't these rules saying fetching the requested URL is not off-limits to INV-20419?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q0322783355",
  "text": "By these rules, is this crawler allowed to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "q0ec6e01cf6",
  "text": "Do these rules rule out any fetch of this URL by INV-20419?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "q14323c9f2d",
  "text": "Which line sets whether this crawler gets to fetch the URL, under these rules?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "qcc8144794b",
  "text": "Which line settles whether this crawler gets to fetch this URL, by these rules?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "q8de7e20ee7",
  "text": "Going by the rules, the fetch of this URL by INV-20419 is settled by which line?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "qfc40fc1d2c",
  "text": "Do these rules place this URL out of bounds for the crawler?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "qd045ce0bb3",
  "text": "Going by these rules, does the crawler lack any permission to fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "q2ac447b8d5",
  "text": "Under these rules, is the crawler not entitled to fetch the URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q56fa10920f",
  "text": "Going by the rules, is INV-20419 not authorized to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "q8ceea450da",
  "text": "According to these rules, which line settles whether INV-20419 is cleared to fetch the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q18df98ecfc",
  "text": "Does any of these rules deny the crawler the right to fetch this URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "qb6ed00f7ca",
  "text": "According to these rules, must the crawler stay out of the URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q2ac7789389",
  "text": "Is the crawler not allowed to fetch this URL by these rules?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "qcbc683e0d5",
  "text": "Under these rules, is it not the case that INV-20419 is not blocked from fetching this URL?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "q27f02bfde4",
  "text": "By these rules, does anything rule out the crawler's fetch of this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "q299d3c9aa3",
  "text": "Do these rules green-light the crawler to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q02eb94f059",
  "text": "Does the crawler lack the right to fetch this URL under these rules?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "qcaed6082ec",
  "text": "Do these rules deny INV-20419 the right to fetch the URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q92accdba3d",
  "text": "When INV-20419 asks to fetch this URL, which line of these rules decides whether that request gets through?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "q2cf6062c87",
  "text": "By these rules, isn't the crawler not barred from fetching the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q79762a3501",
  "text": "By these rules, is the crawler obliged to skip the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q752e6c10e8",
  "text": "Going by the robots.txt, which line settles if the crawler may fetch this URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "q40e02a6d84",
  "text": "Is it not the case that, under these rules, the crawler is not stopped from fetching this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q1d60152572",
  "text": "According to these rules, is this URL something INV-20419 may fetch?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "qea377075c7",
  "text": "By these rules, is it not so that the crawler is not blocked from fetching this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q9ce9d13dec",
  "text": "Looking at these rules, what's the line that settles whether the crawler gets to fetch the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q47bc743007",
  "text": "Under these rules, is the crawler required to skip this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q1ff77ad0cb",
  "text": "According to these rules, is INV-20419 not permitted to fetch this URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "q8b0c6006bd",
  "text": "Under these rules, isn't INV-20419 simply not held back from fetching this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "qc08345f23c",
  "text": "Hey, going by these rules, may the crawler grab this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "qebe2bc12dd",
  "text": "Going by these rules, may this crawler not fetch the URL?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "qa17493558d",
  "text": "So what's the line of the robots.txt that decides if the crawler gets to fetch this URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q58df3904fb",
  "text": "Real talk: according to these rules, is the crawler allowed to grab the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "qff03aff5da",
  "text": "Going by the rules, is INV-20419 permitted to fetch the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q6fbfa2b7cf",
  "text": "Under these rules, is the requested URL open to a fetch by INV-20419?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "qaf3a19a7e9",
  "text": "Which line of the robots.txt decides whether the crawler gets to fetch the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "qcb2debb248",
  "text": "Under these rules, does the crawler have to pass over this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "qc6317f215c",
  "text": "Going by the rules, is INV-20419 permitted to fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q9756943c35",
  "text": "Under these rules, which line decides whether the crawler gets to fetch the requested URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "q842a1b6606",
  "text": "According to these rules, what line settles whether the crawler gets to fetch this URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q388d6d85ae",
  "text": "Which line of these rules decides whether the crawler gets to fetch this URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "qa7ce113230",
  "text": "Under these rules, does the crawler lack the permission to fetch the URL at all?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 }
]
