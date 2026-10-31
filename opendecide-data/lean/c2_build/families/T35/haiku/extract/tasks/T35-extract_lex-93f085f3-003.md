# T35 meaning check T35-extract_lex-93f085f3-003

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/haiku/extract/answers/T35-extract_lex-93f085f3-003.json

Items: 39.

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
  "qid": "q1041baa86a",
  "text": "Do these rules allow INV-20419 to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q6fb0a8975a",
  "text": "Do these rules deny the crawler any right to fetch the requested URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "qaf01f091f3",
  "text": "By these rules, does something prevent the crawler from fetching the URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q7b7195e02f",
  "text": "Under these rules, may the crawler not fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "qf7d62c08ae",
  "text": "Do these rules prevent INV-20419 from fetching the requested URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "q052148ddfb",
  "text": "Do these rules let the URL be fetched by INV-20419?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q5ccca012ce",
  "text": "Under these rules, is INV-20419 not granted leave to fetch this URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "qc4242fe694",
  "text": "Is it not so that this URL is not closed to fetching by the crawler under these rules?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "qe379099463",
  "text": "Is INV-20419 not, under these rules, cleared to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q73137d0ec7",
  "text": "According to these rules, may INV-20419 fetch the requested URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "qf0c4f413a6",
  "text": "Quick check on these rules, which line settles whether the crawler gets to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q6f4553810b",
  "text": "Does the crawler have to keep clear of this URL, going by the rules?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "q27f2c02d48",
  "text": "According to these rules, is the requested URL something INV-20419 must pass over?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q0c7f91266a",
  "text": "Is the crawler, under these rules, not permitted to fetch the URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q157ee38120",
  "text": "Do these rules deny the crawler the right to fetch this URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "qb91b85c116",
  "text": "Does the crawler stay out of this URL by these rules?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "qb420163ca5",
  "text": "Under these governing rules, which line of the robots.txt determines whether INV-20419 is to fetch the requested URL?",
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
  "qid": "q544834eef6",
  "text": "Going by these rules, does the crawler have the green light to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "q1a4298e5ff",
  "text": "By these rules, is INV-20419 not entitled to fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "q4f5059e431",
  "text": "Isn't it the case that, under these rules, INV-20419 isn't kept away from fetching this URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "q6aea68afec",
  "text": "By these rules, is the requested URL out of bounds for INV-20419?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "qe294ee8b81",
  "text": "Do these rules prevent the crawler from fetching this URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "q2fc50267b3",
  "text": "Do the rules grant INV-20419 the right to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "qb79e779d26",
  "text": "For the requested URL, by these rules, which line decides whether INV-20419 gets to fetch it?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "qa6e05224bc",
  "text": "Under these rules, isn't it the case that the requested URL is not closed to the crawler?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "q2f86e67b9f",
  "text": "Do these rules permit the crawler to fetch this URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q2e6315b3e1",
  "text": "By these rules, does the crawler have to skip the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "q6aa3a5b68f",
  "text": "Hey, which line of the robots.txt ends up deciding whether the crawler gets to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "qd7a5718d3e",
  "text": "By these rules, is this URL open to fetching by INV-20419?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "q0dab435dc2",
  "text": "Going by the rules, is the crawler told to skip this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q82288ba9c6",
  "text": "By these rules, may this crawler not fetch the requested URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "q8047638c66",
  "text": "So under these rules, may the crawler fetch this URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q9c8035c986",
  "text": "Reading these rules, which line is the main piece deciding whether the crawler gets to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "qeedefb24a3",
  "text": "Under these rules, is it not the case that they do not bar the crawler from fetching this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "q7891470989",
  "text": "By these rules, which line of the robots.txt settles whether the crawler gets to fetch this URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "q6cb41835b4",
  "text": "Under these rules, which line of the robots.txt is determinative for whether INV-20419 gets to fetch the requested URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q559c69c155",
  "text": "By these rules, which line of the robots.txt is determinative as to whether INV-20419 gets to fetch the requested URL?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "qc366511930",
  "text": "According to these rules, may this crawler fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q3c474a30db",
  "text": "Under these rules, the decision on whether INV-20419 gets to fetch the requested URL rests with which line?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 }
]
