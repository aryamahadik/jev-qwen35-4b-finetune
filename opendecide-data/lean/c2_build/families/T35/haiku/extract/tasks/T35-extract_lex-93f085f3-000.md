# T35 meaning check T35-extract_lex-93f085f3-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/haiku/extract/answers/T35-extract_lex-93f085f3-000.json

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
  "qid": "q3688260534",
  "text": "Is it not the case that fetching the requested URL is not a breach by INV-20419 under these rules?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q8d41a32e56",
  "text": "Does the crawler, by these rules, lack any right to fetch this URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "q3a1c34b264",
  "text": "Do these rules let the crawler fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "q544f67f6f1",
  "text": "Under these rules, whether the crawler gets to fetch this URL turns on which line?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q62ef0d749c",
  "text": "By these rules, is the crawler not cleared to fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "q5967f616d2",
  "text": "Under these rules, does INV-20419 have to pass over this URL and stay clear of it?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q602d9781f3",
  "text": "Do these rules not permit this crawler to fetch the URL?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "q7546f6eb82",
  "text": "Under these rules, may the crawler fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "q8822af6cb4",
  "text": "Under these rules, does this URL allow INV-20419 to fetch it?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q87fb4467fe",
  "text": "Under these rules, is the crawler's fetch of this URL permitted?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "qde526555aa",
  "text": "Going by these rules, does the crawler lack the permission to fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q5a6f3f776e",
  "text": "According to these rules, is INV-20419 required to pass over the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q7a21ff56a3",
  "text": "When you go through these rules, which line ends up deciding whether the crawler gets to fetch this URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "q0204990cac",
  "text": "Is INV-20419 bound to pass over the requested URL, under these rules?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "q3fa523c461",
  "text": "Is the crawler not entitled to fetch this URL under these rules?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "qcdfc74d189",
  "text": "Do these rules leave this URL open for INV-20419 to fetch?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q220305d03c",
  "text": "Is the crawler permitted to fetch the requested URL under these rules?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "qe07d4aab08",
  "text": "Which line of the robots.txt is the deciding factor on whether the crawler gets to fetch this URL?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q6dd3957f42",
  "text": "Isn't it so, by these rules, that they do not forbid the crawler from fetching this URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q1eb0b23e19",
  "text": "Under these rules, may INV-20419 fetch the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "q68fd6e796f",
  "text": "Is fetching this URL by INV-20419 not permitted under these rules?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "q8a01d74f5e",
  "text": "Which line of these rules is the thing that settles whether the crawler gets to fetch the requested URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "q0d0e56e199",
  "text": "Do these rules not let the crawler fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "qc093cee6c2",
  "text": "According to these rules, does the crawler lack any permission to fetch the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q559453c261",
  "text": "Is the crawler not entitled to fetch this URL, going by these rules?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "qef2d399932",
  "text": "According to these rules, is this crawler not permitted to fetch the URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q7c4a9c9ab0",
  "text": "Under these rules, which line of the robots.txt governs whether INV-20419 gets to fetch the requested URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q608893d443",
  "text": "Under these rules, is this URL something the crawler may not fetch?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "qbbcede469c",
  "text": "Under these rules, isn't it true the crawler is not barred from fetching this URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q2dfc61c383",
  "text": "Under these rules, must INV-20419 skip this URL and leave it alone?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q3f83f0ce6c",
  "text": "According to these rules, is it not so that INV-20419 is not excluded from fetching the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "q6ba090d811",
  "text": "Going by the rules, does the crawler get to fetch the requested URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q924dda8193",
  "text": "Under these rules, does INV-20419 lack the permission to fetch the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "q2e3a1e233c",
  "text": "Tell me, going by these rules, which line decides whether the crawler gets to fetch the URL?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "qf2f3e9ae54",
  "text": "Going by the rules, is the crawler not allowed to fetch this URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "qc23431cb56",
  "text": "According to these rules, which line governs whether the crawler gets to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q85f1192305",
  "text": "Just checking, do these rules let the crawler fetch the URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q7b428d294d",
  "text": "Under these rules, is the URL a permitted fetch for INV-20419?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "qc2b461848e",
  "text": "Under these rules, the URL INV-20419 wants to fetch is governed by which line of the robots.txt?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q864f12cc3f",
  "text": "Under these rules, must the crawler pass over this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "q4904b648df",
  "text": "Do these rules rule out the crawler fetching this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q1ce0d8a244",
  "text": "Under the rules shown, is INV-20419 authorized to fetch the URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "qb5155b22ab",
  "text": "Under these rules, may INV-20419 not fetch the requested URL?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q906b42475d",
  "text": "Do these rules give INV-20419 permission to fetch this URL?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "q9a85473a86",
  "text": "Quick question: by these rules, does the crawler get to pull this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q06258dc8b6",
  "text": "According to these rules, does the crawler lack the right to fetch the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "qf2461b615a",
  "text": "Under these rules, does the crawler lack the right to fetch this URL?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "q1468fdeecf",
  "text": "By these rules, is the crawler allowed to fetch the URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "qbd8f5e08da",
  "text": "Going by these rules, is the URL cleared for INV-20419 to fetch?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "qe4fa84d03f",
  "text": "Tell me, under these rules, is the crawler allowed to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 }
]
