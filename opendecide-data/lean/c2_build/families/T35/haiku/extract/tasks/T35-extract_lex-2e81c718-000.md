# T35 meaning check T35-extract_lex-2e81c718-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/haiku/extract/answers/T35-extract_lex-2e81c718-000.json

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
  "qid": "q4aba30979c",
  "text": "Going by the rules, is the URL out of bounds for the crawler?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "q2f27b75777",
  "text": "By these rules, is the crawler not cleared to fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "q14fecfb39e",
  "text": "Under these rules, does the access policy prevent INV-20419 from fetching the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q748d6b119e",
  "text": "Under these rules, isn't the crawler simply not blocked from fetching this URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q2d99f2bd93",
  "text": "According to these rules, which line governs whether the crawler gets to fetch this URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q1fde7c456c",
  "text": "Does the crawler have to keep clear of this URL, going by the rules?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q5f061108e3",
  "text": "Going by these rules, does the crawler lack any permission to fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "qa076cdf8db",
  "text": "Aren't these rules saying the crawler is not barred from fetching this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "q8694a55b44",
  "text": "Does the crawler stay out of this URL by these rules?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "q2703e55c2b",
  "text": "Do these rules let the crawler fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "q4cb9b707ac",
  "text": "Under these rules, is the crawler not entitled to fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "qf3c332abdc",
  "text": "Under these rules, may the crawler fetch this URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q9f3aecb5c0",
  "text": "Do these rules not let the crawler fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "q29eb8009aa",
  "text": "Going by the rules, does the crawler get to fetch the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "q2160cc41e4",
  "text": "Under these rules, does the crawler have to pass over this URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "q69c587a3e3",
  "text": "Which line of the robots.txt is the deciding factor on whether the crawler gets to fetch this URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q9346332030",
  "text": "Under these rules, is fetching this URL by the crawler permitted?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "qe4089eeaf7",
  "text": "Under these governing rules, which line of the robots.txt determines whether INV-20419 is to fetch the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q3984a5f67b",
  "text": "Under the rules shown, is the crawler cleared to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "q39109d2bbe",
  "text": "Do these rules let the URL be fetched by INV-20419?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "qc65ce7a48b",
  "text": "Under these rules, which line of the robots.txt is determinative for whether INV-20419 gets to fetch the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "q35a6a119c2",
  "text": "So going by these rules, which line is it that decides whether the crawler gets to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "q8954ba794e",
  "text": "So what's the line of the robots.txt that decides if the crawler gets to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "q20e3f175f4",
  "text": "According to these rules, what line settles whether the crawler gets to fetch this URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q5936c9c4b6",
  "text": "Under these rules, does the crawler lack the right to fetch this URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "q1ffc0eb630",
  "text": "Under these rules, does INV-20419 lack the right to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q7d4bf1bcaf",
  "text": "Under these rules, which line is the decider on whether the crawler gets to fetch this URL?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "none of these"
  ]
 },
 {
  "qid": "qedaddf43cf",
  "text": "Do these rules keep the crawler away from this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q4a61abcafc",
  "text": "Reading these rules, which line is the main piece deciding whether the crawler gets to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "qb6e88b199d",
  "text": "Which line of these rules decides whether the crawler gets to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "qcc1dde314b",
  "text": "Under these rules, does INV-20419 have to pass over the requested URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "qa3ca59ab90",
  "text": "According to these rules, is this crawler not permitted to fetch the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "none of these"
  ]
 },
 {
  "qid": "qb0dbd120cf",
  "text": "According to these rules, may INV-20419 fetch the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "qc57d6081aa",
  "text": "Is the crawler not entitled to fetch this URL, going by these rules?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q8fcfc615f2",
  "text": "Under these rules, is the requested URL open to a fetch by INV-20419?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "qea5b15e47f",
  "text": "According to these rules, is INV-20419 required to pass over the requested URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "qf19aec0d86",
  "text": "Under these rules, may the crawler not fetch this URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "qc862d4f005",
  "text": "By these rules, is it not so that the crawler is not blocked from fetching this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about what the website's owner would prefer the crawler to do",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "q491545701b",
  "text": "Do these rules allow INV-20419 to fetch this URL?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "none of these"
  ]
 },
 {
  "qid": "q0f3b3f43ed",
  "text": "Under these rules, isn't it true the crawler is not barred from fetching this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "none of these"
  ]
 },
 {
  "qid": "qc2757a6828",
  "text": "Quick check on these rules, which line settles whether the crawler gets to fetch this URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "q54945735d1",
  "text": "Going by these rules, does the crawler have the green light to fetch this URL?",
  "choices": [
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "qc90269d97c",
  "text": "Under these rules, isn't INV-20419 simply not held back from fetching this URL?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "qec6035cb1d",
  "text": "By these rules, does the crawler have to skip the URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q5b58b2dbbc",
  "text": "Under these rules, isn't it the case that the requested URL is not closed to the crawler?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about whether fetching the URL would be wise or polite",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "none of these"
  ]
 },
 {
  "qid": "q28fbac0fbb",
  "text": "Do these rules not permit INV-20419 to fetch the requested URL?",
  "choices": [
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 },
 {
  "qid": "qe1db47e54b",
  "text": "Going by the rules, the fetch of this URL by INV-20419 is settled by which line?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether fetching the URL would be wise or polite",
   "none of these"
  ]
 },
 {
  "qid": "qc8d78edaf3",
  "text": "Under these rules, does the crawler lack the permission to fetch the URL at all?",
  "choices": [
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question about what the website's owner would prefer the crawler to do",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "none of these"
  ]
 },
 {
  "qid": "q698cddea92",
  "text": "By these rules, is the crawler obliged to skip the requested URL?",
  "choices": [
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a question asking which line of the robots.txt decides the request",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about what the website's owner would prefer the crawler to do",
   "none of these"
  ]
 },
 {
  "qid": "q48e662ce09",
  "text": "Is it not so that this URL is not closed to fetching by the crawler under these rules?",
  "choices": [
   "a question asking which line of the robots.txt decides the request",
   "a question about what the website's owner would prefer the crawler to do",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as 'prevent', 'lack' or 'deny'",
   "a question about whether the crawler is technically able to reach the URL",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
   "a question about whether fetching the URL would be wise or polite",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
   "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word (for example with 'skip' or 'off-limits')",
   "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
   "none of these"
  ]
 }
]
