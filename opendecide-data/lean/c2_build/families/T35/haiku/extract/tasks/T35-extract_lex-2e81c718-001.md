# T35 meaning check T35-extract_lex-2e81c718-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/haiku/extract/answers/T35-extract_lex-2e81c718-001.json

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
  "qid": "q8b035723e1",
  "text": "Going by these rules, what line settles whether INV-20419 gets to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "qc50ee5d7c6",
  "text": "By these rules, is INV-20419 bound to stay out of this URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "qa436bae3a2",
  "text": "Does the crawler lack the right to fetch this URL under these rules?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q2e5fa0560d",
  "text": "Which line of the robots.txt decides whether the crawler gets to fetch the requested URL?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "qe002b1c2c3",
  "text": "According to these rules, is this URL something INV-20419 may fetch?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q91b7d4e3e2",
  "text": "Just checking, do these rules let the crawler fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "qce528390eb",
  "text": "Under these rules, may INV-20419 fetch the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "q6f25ec30d6",
  "text": "Does the crawler, by these rules, lack any right to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q099f70b07a",
  "text": "According to these rules, is it not so that INV-20419 is not excluded from fetching the requested URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q9d75b0d7bc",
  "text": "By these rules, is INV-20419 not entitled to fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q941f12c4ee",
  "text": "Going by the rules, is INV-20419 not authorized to fetch this URL?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "q1e6ba1e099",
  "text": "According to these rules, may the crawler fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q90cceb3ef8",
  "text": "Is the crawler bound by these rules to pass over the URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "q454696c770",
  "text": "Going by these rules, does the crawler lack the permission to fetch the URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "q3cb441779e",
  "text": "Is the crawler out of bounds for this URL, according to these rules?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "q9d5b9f5c27",
  "text": "Under these rules, must INV-20419 skip this URL and leave it alone?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q40c82fb0c9",
  "text": "Does any of these rules deny the crawler the right to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q867b01b4f5",
  "text": "Do these rules not permit this crawler to fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "qcb0be84671",
  "text": "Do these rules deny the crawler the right to fetch this URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "qdf58077d92",
  "text": "Is the crawler not allowed to fetch this URL by these rules?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "qa44bd928f4",
  "text": "Going by the robots.txt, which line settles if the crawler may fetch this URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q14c5509978",
  "text": "Going by the rules, does INV-20419 have to skip the requested URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "q901f49c1be",
  "text": "Hey, going by these rules, may the crawler grab this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "q0116872a6d",
  "text": "Under these rules, is this URL something the crawler may not fetch?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "qca870cbe9b",
  "text": "According to these rules, is INV-20419 not permitted to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q8f46aa4480",
  "text": "By these rules, is INV-20419 allowed to fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q57319e80c0",
  "text": "Do these rules tell the crawler it may not fetch this URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "q33d06c3829",
  "text": "By these rules, is this URL open to fetching by INV-20419?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "qc762b8cd89",
  "text": "Isn't it so, by these rules, that they do not forbid the crawler from fetching this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "qd7e42f5891",
  "text": "By these rules, is the requested URL out of bounds for INV-20419?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q6d16e9535a",
  "text": "Which line do these rules point to as deciding whether the crawler gets to fetch this URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "qc4850b51c2",
  "text": "Under these rules, must the crawler pass over this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "q00fcd400fd",
  "text": "Is fetching this URL by INV-20419 not permitted under these rules?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "q08825f2231",
  "text": "Is the crawler not, under these rules, cleared to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q91da778942",
  "text": "Going by the rules, is INV-20419 permitted to fetch the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "qc5a8f75f4f",
  "text": "By these rules, which line of the robots.txt is determinative as to whether INV-20419 gets to fetch the requested URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q48cbbe774e",
  "text": "Going by the rules, is the crawler not allowed to fetch this URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "q49306f9040",
  "text": "Do these rules deny INV-20419 the right to fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "qbe779e535e",
  "text": "Under these rules, which line of the robots.txt settles whether the crawler may fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q44daf4dfa7",
  "text": "Do these rules say the crawler must pass over the requested URL?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "q8bfbc0c369",
  "text": "Under these rules, the decision on whether INV-20419 gets to fetch the requested URL rests with which line?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q2d4c7c7a74",
  "text": "Of the robots.txt, which line gates whether the crawler gets to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q1faa28d9ed",
  "text": "Under these rules, does INV-20419 have to pass over this URL and stay clear of it?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "q62c204c131",
  "text": "Do these rules require INV-20419 to stay out of this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "q4f7e1f58a3",
  "text": "Do these rules permit INV-20419 to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q547eae7513",
  "text": "Is it not the case that fetching the requested URL is not a breach by INV-20419 under these rules?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "q62c808646f",
  "text": "Which line settles whether this crawler gets to fetch this URL, by these rules?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "qb9d5b6dbfc",
  "text": "Mind you, under these rules, is the crawler given the go-ahead to fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q67f1147287",
  "text": "According to these rules, may this crawler fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q340141b24b",
  "text": "Under these rules, is the URL a permitted fetch for INV-20419?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 }
]
